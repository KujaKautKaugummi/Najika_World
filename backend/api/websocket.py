"""
WebSocket API Router
Real-time communication endpoints
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import json
import logging

from backend.database import get_db
from backend.models.user import User
from backend.services.websocket_manager import websocket_manager
from backend.api.auth import get_current_user_from_token

router = APIRouter(prefix="/ws", tags=["WebSocket"])
logger = logging.getLogger(__name__)


# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Main WebSocket connection endpoint

    Usage:
    ws://localhost:8000/ws/connect?token=<auth_token>
    """
    user = None
    user_id = None

    try:
        # Authenticate user from token
        user = await get_current_user_from_token(token, db)

        if not user:
            await websocket.close(code=1008, reason="Authentication failed")
            return

        user_id = user.id

        # Connect to WebSocket manager
        connection = await websocket_manager.connect(
            websocket=websocket,
            user_id=user.id,
            username=user.username,
            metadata={
                'is_admin': user.is_admin
            }
        )

        # Send welcome message
        await websocket.send_json({
            'type': 'connected',
            'message': f'Welcome {user.username}!',
            'user_id': user.id,
            'channels': list(connection.subscribed_channels)
        })

        # Main message loop
        while True:
            # Receive message
            data = await websocket.receive_json()

            # Handle message
            await handle_websocket_message(user.id, data)

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: user_id={user_id}")

    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)

    finally:
        # Cleanup on disconnect
        if user_id:
            await websocket_manager.disconnect(user_id)


async def handle_websocket_message(user_id: int, message: dict):
    """
    Handle incoming WebSocket messages
    """
    message_type = message.get('type')

    if message_type == 'subscribe':
        # Subscribe to channel
        channel = message.get('channel')
        if channel:
            websocket_manager.subscribe_to_channel(user_id, channel)
            await websocket_manager.send_to_user(user_id, {
                'type': 'subscribed',
                'channel': channel
            })

    elif message_type == 'unsubscribe':
        # Unsubscribe from channel
        channel = message.get('channel')
        if channel:
            websocket_manager.unsubscribe_from_channel(user_id, channel)
            await websocket_manager.send_to_user(user_id, {
                'type': 'unsubscribed',
                'channel': channel
            })

    elif message_type == 'spectate_battle':
        # Join battle as spectator
        battle_id = message.get('battle_id')
        if battle_id:
            websocket_manager.add_battle_spectator(battle_id, user_id)
            await websocket_manager.send_to_user(user_id, {
                'type': 'spectating',
                'battle_id': battle_id
            })

    elif message_type == 'stop_spectating':
        # Stop spectating battle
        battle_id = message.get('battle_id')
        if battle_id:
            websocket_manager.remove_battle_spectator(battle_id, user_id)
            await websocket_manager.send_to_user(user_id, {
                'type': 'stopped_spectating',
                'battle_id': battle_id
            })

    elif message_type == 'update_presence':
        # Update user presence
        presence = message.get('presence', {})
        websocket_manager.update_user_presence(user_id, presence)

    elif message_type == 'ping':
        # Respond to ping
        await websocket_manager.send_to_user(user_id, {
            'type': 'pong',
            'timestamp': message.get('timestamp')
        })

    else:
        logger.warning(f"Unknown message type: {message_type}")


# ============================================================================
# REST ENDPOINTS (for triggering WebSocket broadcasts)
# ============================================================================

@router.get("/stats")
async def get_websocket_stats(
    current_user: User = Depends(get_current_user)
):
    """
    Get WebSocket statistics
    """
    return {
        "success": True,
        "stats": websocket_manager.get_stats()
    }


@router.get("/online-users")
async def get_online_users(
    current_user: User = Depends(get_current_user)
):
    """
    Get list of online users
    """
    return {
        "success": True,
        "online_users": websocket_manager.get_online_users()
    }


@router.post("/broadcast")
async def broadcast_message(
    message: dict,
    channel: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Broadcast message to channel or all users (admin only)
    """
    if not current_user.is_admin:
        return {"success": False, "error": "Admin only"}

    if channel:
        await websocket_manager.broadcast_to_channel(channel, {
            'type': 'admin_broadcast',
            'message': message,
            'from': current_user.username
        })
    else:
        await websocket_manager.broadcast_to_all({
            'type': 'admin_broadcast',
            'message': message,
            'from': current_user.username
        })

    return {
        "success": True,
        "message": "Broadcast sent"
    }
