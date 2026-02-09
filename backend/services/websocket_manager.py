"""
WebSocket Manager
Real-time communication system for Najika World
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import asyncio
import logging

logger = logging.getLogger(__name__)


@dataclass
class Connection:
    """WebSocket connection wrapper"""
    websocket: WebSocket
    user_id: int
    username: str
    connected_at: datetime = field(default_factory=datetime.utcnow)
    subscribed_channels: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)


class WebSocketManager:
    """
    Manages WebSocket connections and real-time messaging
    """

    def __init__(self):
        # Active connections: user_id -> Connection
        self.connections: Dict[int, Connection] = {}

        # Channels: channel_name -> set of user_ids
        self.channels: Dict[str, Set[int]] = {
            'global': set(),
            'battle': set(),
            'arena': set(),
            'evolution': set(),
            'admin': set(),
            # Lebensraum channels (for building/gathering sync)
            'lebensraum': set(),
            'building': set(),
            'gathering': set(),
            'crafting': set(),
            # Region channels for Boss broadcasts
            'region:samtmoos_tiefwald': set(),
            'region:reich_der_drei': set(),
            'region:salzwind_kueste': set(),
            'region:blitzebene': set(),
            'region:gruenschlamm_sumpf': set(),
            'region:magmastroeme': set(),
            'region:heisse_duenen': set(),
            'region:tiefenhoehlen': set()
        }

        # User presence tracking
        self.user_presence: Dict[int, Dict[str, Any]] = {}

        # Battle spectators: battle_id -> set of user_ids
        self.battle_spectators: Dict[str, Set[int]] = {}

        logger.info("WebSocket Manager initialized")

    async def connect(
        self,
        websocket: WebSocket,
        user_id: int,
        username: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Accept and register a new WebSocket connection
        """
        await websocket.accept()

        connection = Connection(
            websocket=websocket,
            user_id=user_id,
            username=username,
            metadata=metadata or {}
        )

        self.connections[user_id] = connection

        # Auto-subscribe to global channel
        self.subscribe_to_channel(user_id, 'global')

        # Update presence
        self.update_user_presence(user_id, {
            'status': 'online',
            'username': username,
            'connected_at': datetime.utcnow().isoformat()
        })

        # Broadcast user joined
        await self.broadcast_to_channel('global', {
            'type': 'user_joined',
            'user_id': user_id,
            'username': username,
            'timestamp': datetime.utcnow().isoformat()
        }, exclude_users={user_id})

        logger.info(f"WebSocket connected: {username} (user_id={user_id})")

        return connection

    async def disconnect(self, user_id: int):
        """
        Disconnect and cleanup a WebSocket connection
        """
        connection = self.connections.get(user_id)
        if not connection:
            return

        username = connection.username

        # Remove from all channels
        for channel in list(connection.subscribed_channels):
            self.unsubscribe_from_channel(user_id, channel)

        # Remove from battle spectators
        for battle_id in list(self.battle_spectators.keys()):
            if user_id in self.battle_spectators[battle_id]:
                self.battle_spectators[battle_id].remove(user_id)

        # Update presence
        self.user_presence[user_id] = {
            'status': 'offline',
            'last_seen': datetime.utcnow().isoformat()
        }

        # Broadcast user left
        await self.broadcast_to_channel('global', {
            'type': 'user_left',
            'user_id': user_id,
            'username': username,
            'timestamp': datetime.utcnow().isoformat()
        })

        # Remove connection
        del self.connections[user_id]

        logger.info(f"WebSocket disconnected: {username} (user_id={user_id})")

    def subscribe_to_channel(self, user_id: int, channel: str):
        """
        Subscribe user to a channel
        """
        if channel not in self.channels:
            self.channels[channel] = set()

        self.channels[channel].add(user_id)

        connection = self.connections.get(user_id)
        if connection:
            connection.subscribed_channels.add(channel)

        logger.debug(f"User {user_id} subscribed to channel: {channel}")

    def unsubscribe_from_channel(self, user_id: int, channel: str):
        """
        Unsubscribe user from a channel
        """
        if channel in self.channels and user_id in self.channels[channel]:
            self.channels[channel].remove(user_id)

        connection = self.connections.get(user_id)
        if connection and channel in connection.subscribed_channels:
            connection.subscribed_channels.remove(channel)

        logger.debug(f"User {user_id} unsubscribed from channel: {channel}")

    def update_user_presence(self, user_id: int, presence: Dict[str, Any]):
        """
        Update user presence information
        """
        if user_id not in self.user_presence:
            self.user_presence[user_id] = {}

        self.user_presence[user_id].update(presence)

    async def send_to_user(self, user_id: int, message: Dict[str, Any]):
        """
        Send message to a specific user
        """
        connection = self.connections.get(user_id)
        if not connection:
            logger.warning(f"Cannot send to user {user_id}: not connected")
            return

        try:
            await connection.websocket.send_json(message)
        except Exception as e:
            logger.error(f"Failed to send message to user {user_id}: {e}")
            await self.disconnect(user_id)

    async def broadcast_to_channel(
        self,
        channel: str,
        message: Dict[str, Any],
        exclude_users: Optional[Set[int]] = None
    ):
        """
        Broadcast message to all users in a channel
        """
        if channel not in self.channels:
            logger.warning(f"Channel {channel} does not exist")
            return

        exclude_users = exclude_users or set()
        user_ids = self.channels[channel] - exclude_users

        # Add channel to message
        message['channel'] = channel

        # Send to all users in channel
        tasks = [
            self.send_to_user(user_id, message)
            for user_id in user_ids
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_all(
        self,
        message: Dict[str, Any],
        exclude_users: Optional[Set[int]] = None
    ):
        """
        Broadcast message to all connected users
        """
        exclude_users = exclude_users or set()
        user_ids = set(self.connections.keys()) - exclude_users

        tasks = [
            self.send_to_user(user_id, message)
            for user_id in user_ids
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_region(
        self,
        region_code: str,
        message: Dict[str, Any],
        exclude_users: Optional[Set[int]] = None
    ):
        """
        Broadcast message to all users in a specific region

        Args:
            region_code: Region code (e.g., "samtmoos_tiefwald")
            message: Message to broadcast
            exclude_users: Optional set of user IDs to exclude
        """
        channel = f"region:{region_code}"
        await self.broadcast_to_channel(channel, message, exclude_users)

    async def notify_battle_start(self, battle_id: str, participants: List[Dict[str, Any]]):
        """
        Notify about battle start
        """
        await self.broadcast_to_channel('battle', {
            'type': 'battle_start',
            'battle_id': battle_id,
            'participants': participants,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def notify_battle_action(
        self,
        battle_id: str,
        action: Dict[str, Any],
        spectators_only: bool = False
    ):
        """
        Notify about battle action
        """
        message = {
            'type': 'battle_action',
            'battle_id': battle_id,
            'action': action,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Send to battle channel
        await self.broadcast_to_channel('battle', message)

        # Also send to spectators
        if battle_id in self.battle_spectators:
            tasks = [
                self.send_to_user(user_id, message)
                for user_id in self.battle_spectators[battle_id]
            ]
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def notify_battle_end(self, battle_id: str, result: Dict[str, Any]):
        """
        Notify about battle end
        """
        await self.broadcast_to_channel('battle', {
            'type': 'battle_end',
            'battle_id': battle_id,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })

        # Clean up spectators
        if battle_id in self.battle_spectators:
            del self.battle_spectators[battle_id]

    def add_battle_spectator(self, battle_id: str, user_id: int):
        """
        Add user as battle spectator
        """
        if battle_id not in self.battle_spectators:
            self.battle_spectators[battle_id] = set()

        self.battle_spectators[battle_id].add(user_id)
        logger.info(f"User {user_id} spectating battle {battle_id}")

    def remove_battle_spectator(self, battle_id: str, user_id: int):
        """
        Remove user from battle spectators
        """
        if battle_id in self.battle_spectators and user_id in self.battle_spectators[battle_id]:
            self.battle_spectators[battle_id].remove(user_id)
            logger.info(f"User {user_id} stopped spectating battle {battle_id}")

    async def notify_evolution(self, user_id: int, evolution_data: Dict[str, Any]):
        """
        Notify about Digimon evolution
        """
        await self.broadcast_to_channel('evolution', {
            'type': 'evolution',
            'user_id': user_id,
            'username': self.connections.get(user_id, {}).username if user_id in self.connections else 'Unknown',
            'evolution': evolution_data,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def notify_finisher(self, user_id: int, finisher_data: Dict[str, Any]):
        """
        Notify about finisher execution
        """
        await self.broadcast_to_channel('arena', {
            'type': 'finisher',
            'user_id': user_id,
            'username': self.connections.get(user_id, {}).username if user_id in self.connections else 'Unknown',
            'finisher': finisher_data,
            'timestamp': datetime.utcnow().isoformat()
        })

    # =========================================================================
    # LEBENSRAUM / BUILDING NOTIFICATIONS
    # =========================================================================

    async def notify_gather_complete(
        self,
        user_id: int,
        action: str,
        resources: Dict[str, int],
        duration: int
    ):
        """
        Notify about completed gathering session
        """
        await self.broadcast_to_channel('gathering', {
            'type': 'gather_complete',
            'user_id': user_id,
            'action': action,
            'resources': resources,
            'duration_seconds': duration,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def notify_craft_complete(
        self,
        user_id: int,
        recipe_id: str,
        quantity: int,
        outputs: Dict[str, int]
    ):
        """
        Notify about completed crafting
        """
        await self.broadcast_to_channel('crafting', {
            'type': 'craft_complete',
            'user_id': user_id,
            'recipe_id': recipe_id,
            'quantity': quantity,
            'outputs': outputs,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def notify_building_placed(
        self,
        user_id: int,
        building_type: str,
        position: Dict[str, float],
        rotation: float = 0
    ):
        """
        Notify about placed building (for multiplayer sync)
        """
        await self.broadcast_to_channel('building', {
            'type': 'building_placed',
            'user_id': user_id,
            'building_type': building_type,
            'position': position,
            'rotation': rotation,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def notify_building_removed(
        self,
        user_id: int,
        building_type: str,
        position: Dict[str, float]
    ):
        """
        Notify about removed building
        """
        await self.broadcast_to_channel('building', {
            'type': 'building_removed',
            'user_id': user_id,
            'building_type': building_type,
            'position': position,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def notify_inventory_update(self, user_id: int, inventory: Dict[str, int]):
        """
        Notify user about inventory update
        """
        await self.send_to_user(user_id, {
            'type': 'inventory_update',
            'inventory': inventory,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def notify_world_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        region: Optional[str] = None
    ):
        """
        Notify about world events (weather, boss spawn, etc.)
        """
        message = {
            'type': 'world_event',
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }

        if region:
            await self.broadcast_to_region(region, message)
        else:
            await self.broadcast_to_channel('lebensraum', message)

    async def send_notification(
        self,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Send notification to specific user
        """
        await self.send_to_user(user_id, {
            'type': 'notification',
            'notification_type': notification_type,
            'title': title,
            'message': message,
            'data': data or {},
            'timestamp': datetime.utcnow().isoformat()
        })

    def get_online_users(self) -> List[Dict[str, Any]]:
        """
        Get list of online users
        """
        return [
            {
                'user_id': user_id,
                'username': conn.username,
                'connected_at': conn.connected_at.isoformat(),
                'channels': list(conn.subscribed_channels)
            }
            for user_id, conn in self.connections.items()
        ]

    def get_channel_users(self, channel: str) -> List[int]:
        """
        Get list of users in a channel
        """
        return list(self.channels.get(channel, set()))

    def get_connection_count(self) -> int:
        """
        Get total connection count
        """
        return len(self.connections)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get WebSocket manager statistics
        """
        return {
            'total_connections': self.get_connection_count(),
            'online_users': self.get_online_users(),
            'channels': {
                channel: len(users)
                for channel, users in self.channels.items()
            },
            'active_battles': len(self.battle_spectators),
            'total_spectators': sum(
                len(spectators)
                for spectators in self.battle_spectators.values()
            )
        }


# Global WebSocket manager instance
websocket_manager = WebSocketManager()
