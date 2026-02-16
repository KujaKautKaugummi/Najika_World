"""
Multiplayer API Endpoints
WebSocket endpoints for real-time multiplayer functionality
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from backend.utils import handle_errors
from typing import Optional
import json
import uuid

from backend.services.multiplayer_server import get_multiplayer_server
# from backend.api.auth import get_current_user_from_token  # Not implemented yet
# from backend.models.user import User


router = APIRouter(prefix="/api/multiplayer", tags=["multiplayer"])


@router.websocket("/ws")
async def multiplayer_websocket(
    websocket: WebSocket,
    token: Optional[str] = Query(None)
):
    """
    WebSocket endpoint for multiplayer connections

    Query Parameters:
        token: JWT authentication token (optional for guest play)

    Protocol:
        Client -> Server:
            - {"type": "join", "username": "...", "position": {...}, "character": {...}}
            - {"type": "update", "position": {...}, "rotation": {...}, "animation": "..."}
            - {"type": "chat", "message": "..."}
            - {"type": "action", "action": "...", ...}
            - {"type": "ping"}

        Server -> Client:
            - {"type": "welcome", "player_id": "...", "room_id": "..."}
            - {"type": "player_list", "players": [...]}
            - {"type": "player_joined", "player_id": "...", "username": "..."}
            - {"type": "player_left", "player_id": "...", "username": "..."}
            - {"type": "player_update", "player_id": "...", "position": {...}}
            - {"type": "chat_message", "player_id": "...", "username": "...", "message": "..."}
            - {"type": "action", "player_id": "...", "action": "..."}
            - {"type": "pong"}
    """

    # Get multiplayer server instance
    server = get_multiplayer_server()

    # Generate player ID
    player_id = str(uuid.uuid4())

    # Try to get user from token
    user = None
    username = f"Guest_{player_id[:8]}"

    if token:
        try:
            # This would need to be adapted to work with WebSocket
            # For now, use guest mode
            # user = await get_current_user_from_token(token)
            # username = user.username
            pass
        except:
            pass

    # Connect player
    player = await server.connect(
        websocket=websocket,
        player_id=player_id,
        username=username,
        room_id="main"
    )

    try:
        # Message loop
        while True:
            # Receive message
            data = await websocket.receive_text()

            try:
                message = json.loads(data)

                # Handle join message (set username)
                if message.get("type") == "join" and "username" in message:
                    player.username = message["username"]

                    # Update position and character
                    if "position" in message:
                        player.position = message["position"]
                    if "character" in message:
                        player.character = message["character"]

                    # Notify room about updated player
                    room = server.get_player_room(player_id)
                    if room:
                        await server.broadcast_to_room(room, {
                            "type": "player_update",
                            "player_id": player_id,
                            "username": player.username,
                            "position": player.position,
                            "character": player.character
                        })

                    continue

                # Handle other messages
                await server.handle_message(player_id, message)

            except json.JSONDecodeError:
                print(f"Invalid JSON from player {player_id}")
                continue

            except Exception as e:
                print(f"Error handling message from player {player_id}: {e}")
                continue

    except WebSocketDisconnect:
        # Player disconnected
        await server.disconnect(player_id)

    except Exception as e:
        print(f"WebSocket error for player {player_id}: {e}")
        await server.disconnect(player_id)


@router.get("/stats")
@handle_errors()
async def get_multiplayer_stats():
    """
    Get multiplayer server statistics

    Returns:
        Server stats including player counts, rooms, etc.
    """

    server = get_multiplayer_server()
    return server.get_stats()


@router.get("/rooms")
@handle_errors()
async def get_room_list():
    """
    Get list of active rooms

    Returns:
        Dictionary of room IDs and player counts
    """

    server = get_multiplayer_server()
    return {
        "rooms": server.get_room_list(),
        "total_players": server.get_total_player_count()
    }


@router.get("/rooms/{room_id}")
@handle_errors()
async def get_room_info(room_id: str):
    """
    Get information about a specific room

    Args:
        room_id: Room ID

    Returns:
        Room information
    """

    server = get_multiplayer_server()

    player_count = server.get_room_player_count(room_id)

    return {
        "room_id": room_id,
        "player_count": player_count,
        "max_players": server.max_players_per_room,
        "is_full": player_count >= server.max_players_per_room
    }
