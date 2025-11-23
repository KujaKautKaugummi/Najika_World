"""
Multiplayer Server
WebSocket-based real-time multiplayer server for Digivice Web Game
"""

import asyncio
import json
import time
from typing import Dict, Set, Optional, Any
from dataclasses import dataclass, asdict
from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict


@dataclass
class Player:
    """Player data structure"""
    id: str
    username: str
    websocket: WebSocket
    position: Dict[str, float] = None
    rotation: Dict[str, float] = None
    character: Dict[str, Any] = None
    state: str = "idle"
    animation: str = "idle"
    joined_at: float = 0

    def __post_init__(self):
        if self.position is None:
            self.position = {"x": 0, "y": 0, "z": 0}
        if self.rotation is None:
            self.rotation = {"x": 0, "y": 0, "z": 0}
        if self.character is None:
            self.character = {"species": "Jellysquish", "level": 1, "color": 0xff69b4}
        if self.joined_at == 0:
            self.joined_at = time.time()

    def to_dict(self):
        """Convert to dictionary (excluding websocket)"""
        data = asdict(self)
        del data['websocket']
        return data


class MultiplayerServer:
    """
    Real-time Multiplayer Server

    Features:
    - Player connection management
    - Position/state synchronization
    - Chat system
    - Room/instance support
    - Player actions broadcast
    """

    def __init__(self):
        # Connected players: {player_id: Player}
        self.players: Dict[str, Player] = {}

        # Rooms: {room_id: Set[player_id]}
        self.rooms: Dict[str, Set[str]] = defaultdict(set)

        # Default room
        self.default_room = "main"

        # Statistics
        self.total_connections = 0
        self.total_messages_sent = 0
        self.total_messages_received = 0

        # Server settings
        self.max_players_per_room = 50
        self.update_rate = 20  # Updates per second
        self.ping_interval = 30  # Seconds

    async def connect(
        self,
        websocket: WebSocket,
        player_id: str,
        username: str,
        room_id: str = None
    ) -> Player:
        """
        Handle new player connection

        Args:
            websocket: WebSocket connection
            player_id: Unique player ID
            username: Player username
            room_id: Room to join (default: main)

        Returns:
            Player object
        """

        # Accept WebSocket connection
        await websocket.accept()

        # Create player object
        player = Player(
            id=player_id,
            username=username,
            websocket=websocket
        )

        # Add to players dict
        self.players[player_id] = player

        # Join room
        room = room_id or self.default_room
        self.rooms[room].add(player_id)

        # Update stats
        self.total_connections += 1

        print(f"✅ Player connected: {username} ({player_id}) to room '{room}'")
        print(f"   Total players: {len(self.players)}")

        # Send welcome message
        await self.send_to_player(player_id, {
            "type": "welcome",
            "player_id": player_id,
            "room_id": room,
            "message": f"Welcome {username}!"
        })

        # Notify other players
        await self.broadcast_to_room(room, {
            "type": "player_joined",
            "player_id": player_id,
            "username": username,
            "position": player.position,
            "character": player.character
        }, exclude_player=player_id)

        # Send current player list
        await self.send_player_list(player_id, room)

        return player

    async def disconnect(self, player_id: str):
        """
        Handle player disconnection

        Args:
            player_id: Player ID to disconnect
        """

        if player_id not in self.players:
            return

        player = self.players[player_id]

        # Find player's room
        room = self.get_player_room(player_id)

        # Remove from room
        if room and player_id in self.rooms[room]:
            self.rooms[room].remove(player_id)

        # Remove from players
        del self.players[player_id]

        print(f"❌ Player disconnected: {player.username} ({player_id})")
        print(f"   Total players: {len(self.players)}")

        # Notify other players
        if room:
            await self.broadcast_to_room(room, {
                "type": "player_left",
                "player_id": player_id,
                "username": player.username
            })

    async def handle_message(self, player_id: str, message: Dict[str, Any]):
        """
        Handle incoming message from player

        Args:
            player_id: Player ID
            message: Message data
        """

        if player_id not in self.players:
            print(f"⚠️ Received message from unknown player: {player_id}")
            return

        player = self.players[player_id]
        msg_type = message.get("type")

        self.total_messages_received += 1

        # Handle different message types
        if msg_type == "update":
            await self.handle_player_update(player_id, message)

        elif msg_type == "chat":
            await self.handle_chat_message(player_id, message)

        elif msg_type == "action":
            await self.handle_player_action(player_id, message)

        elif msg_type == "join_room":
            await self.handle_join_room(player_id, message)

        elif msg_type == "leave_room":
            await self.handle_leave_room(player_id, message)

        elif msg_type == "ping":
            await self.send_to_player(player_id, {"type": "pong"})

        else:
            print(f"⚠️ Unknown message type: {msg_type}")

    async def handle_player_update(self, player_id: str, message: Dict[str, Any]):
        """Handle player position/state update"""

        player = self.players[player_id]

        # Update player data
        if "position" in message:
            player.position = message["position"]

        if "rotation" in message:
            player.rotation = message["rotation"]

        if "animation" in message:
            player.animation = message["animation"]

        if "state" in message:
            player.state = message["state"]

        # Broadcast to other players in the same room
        room = self.get_player_room(player_id)
        if room:
            await self.broadcast_to_room(room, {
                "type": "player_update",
                "player_id": player_id,
                "position": player.position,
                "rotation": player.rotation,
                "animation": player.animation,
                "state": player.state
            }, exclude_player=player_id)

    async def handle_chat_message(self, player_id: str, message: Dict[str, Any]):
        """Handle chat message"""

        player = self.players[player_id]
        chat_msg = message.get("message", "")

        if not chat_msg:
            return

        # Broadcast to room
        room = self.get_player_room(player_id)
        if room:
            await self.broadcast_to_room(room, {
                "type": "chat_message",
                "player_id": player_id,
                "username": player.username,
                "message": chat_msg,
                "timestamp": time.time()
            })

        print(f"💬 [{room}] {player.username}: {chat_msg}")

    async def handle_player_action(self, player_id: str, message: Dict[str, Any]):
        """Handle player action (emote, attack, etc.)"""

        player = self.players[player_id]
        action = message.get("action")

        if not action:
            return

        # Broadcast action to room
        room = self.get_player_room(player_id)
        if room:
            await self.broadcast_to_room(room, {
                "type": "action",
                "player_id": player_id,
                "username": player.username,
                "action": action,
                **{k: v for k, v in message.items() if k not in ["type", "action"]}
            }, exclude_player=player_id)

    async def handle_join_room(self, player_id: str, message: Dict[str, Any]):
        """Handle player joining a room"""

        new_room = message.get("room_id")
        if not new_room:
            return

        # Leave current room
        current_room = self.get_player_room(player_id)
        if current_room:
            await self.handle_leave_room(player_id, {"room_id": current_room})

        # Join new room
        self.rooms[new_room].add(player_id)

        player = self.players[player_id]

        # Notify new room
        await self.broadcast_to_room(new_room, {
            "type": "player_joined",
            "player_id": player_id,
            "username": player.username,
            "position": player.position,
            "character": player.character
        }, exclude_player=player_id)

        # Send player list for new room
        await self.send_player_list(player_id, new_room)

        print(f"🚪 {player.username} joined room '{new_room}'")

    async def handle_leave_room(self, player_id: str, message: Dict[str, Any]):
        """Handle player leaving a room"""

        room_id = message.get("room_id")
        if not room_id or player_id not in self.rooms[room_id]:
            return

        player = self.players[player_id]

        # Remove from room
        self.rooms[room_id].remove(player_id)

        # Notify room
        await self.broadcast_to_room(room_id, {
            "type": "player_left",
            "player_id": player_id,
            "username": player.username
        })

        print(f"🚪 {player.username} left room '{room_id}'")

    async def send_to_player(self, player_id: str, message: Dict[str, Any]):
        """Send message to specific player"""

        if player_id not in self.players:
            return

        player = self.players[player_id]

        try:
            await player.websocket.send_json(message)
            self.total_messages_sent += 1
        except Exception as e:
            print(f"❌ Failed to send message to {player.username}: {e}")
            # Disconnect player
            await self.disconnect(player_id)

    async def broadcast_to_room(
        self,
        room_id: str,
        message: Dict[str, Any],
        exclude_player: Optional[str] = None
    ):
        """Broadcast message to all players in a room"""

        if room_id not in self.rooms:
            return

        tasks = []
        for player_id in self.rooms[room_id]:
            if player_id != exclude_player and player_id in self.players:
                tasks.append(self.send_to_player(player_id, message))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_all(
        self,
        message: Dict[str, Any],
        exclude_player: Optional[str] = None
    ):
        """Broadcast message to all connected players"""

        tasks = []
        for player_id in self.players:
            if player_id != exclude_player:
                tasks.append(self.send_to_player(player_id, message))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def send_player_list(self, player_id: str, room_id: str):
        """Send list of players in room to specific player"""

        if room_id not in self.rooms:
            return

        players_data = []
        for pid in self.rooms[room_id]:
            if pid in self.players:
                player = self.players[pid]
                players_data.append({
                    "player_id": pid,
                    "username": player.username,
                    "position": player.position,
                    "rotation": player.rotation,
                    "character": player.character,
                    "state": player.state,
                    "animation": player.animation
                })

        await self.send_to_player(player_id, {
            "type": "player_list",
            "room_id": room_id,
            "players": players_data
        })

    def get_player_room(self, player_id: str) -> Optional[str]:
        """Get the room a player is in"""

        for room_id, players in self.rooms.items():
            if player_id in players:
                return room_id
        return None

    def get_room_player_count(self, room_id: str) -> int:
        """Get number of players in a room"""
        return len(self.rooms.get(room_id, set()))

    def get_total_player_count(self) -> int:
        """Get total number of connected players"""
        return len(self.players)

    def get_room_list(self) -> Dict[str, int]:
        """Get list of rooms with player counts"""
        return {
            room_id: len(players)
            for room_id, players in self.rooms.items()
            if len(players) > 0
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get server statistics"""
        return {
            "total_players": len(self.players),
            "total_rooms": len([r for r in self.rooms.values() if len(r) > 0]),
            "total_connections": self.total_connections,
            "messages_sent": self.total_messages_sent,
            "messages_received": self.total_messages_received,
            "rooms": self.get_room_list()
        }


# Global multiplayer server instance
_multiplayer_server = None


def get_multiplayer_server() -> MultiplayerServer:
    """Get global multiplayer server instance"""
    global _multiplayer_server
    if _multiplayer_server is None:
        _multiplayer_server = MultiplayerServer()
    return _multiplayer_server


if __name__ == "__main__":
    # Test server
    server = MultiplayerServer()
    print("Multiplayer server created")
    print(f"Max players per room: {server.max_players_per_room}")
    print(f"Update rate: {server.update_rate} Hz")
