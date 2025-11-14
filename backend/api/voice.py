"""
Voice API Router
Handles voice chat, WebSocket connections, and speech-to-text (Whisper AI)
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import json
import base64

from backend.database import get_db
from backend.models.user import User
from backend.api.auth import decode_token
from backend.config import settings

router = APIRouter(prefix="/voice", tags=["Voice"])


# ============================================================================
# WEBSOCKET CONNECTION MANAGER
# ============================================================================

class ConnectionManager:
    """Manages WebSocket connections for voice chat"""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_info: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str, username: str):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_info[user_id] = {
            "username": username,
            "connected_at": datetime.utcnow().isoformat()
        }
        print(f"✅ Voice: User {username} (ID: {user_id}) connected")

    def disconnect(self, user_id: str):
        """Remove WebSocket connection"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_info:
            del self.user_info[user_id]
        print(f"❌ Voice: User {user_id} disconnected")

    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to specific user"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def broadcast(self, message: dict, exclude_user: Optional[str] = None):
        """Broadcast message to all connected users (optionally exclude one)"""
        for user_id, websocket in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to {user_id}: {e}")

    async def broadcast_audio(self, audio_data: bytes, user_id: str):
        """Broadcast audio to all users except sender"""
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        message = {
            "type": "audio",
            "user_id": user_id,
            "username": self.user_info.get(user_id, {}).get("username", "Unknown"),
            "audio": audio_b64,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast(message, exclude_user=user_id)

    def get_connected_users(self) -> List[Dict]:
        """Get list of connected users"""
        return [
            {"user_id": user_id, **info}
            for user_id, info in self.user_info.items()
        ]


manager = ConnectionManager()


# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@router.websocket("/ws/{token}")
async def voice_websocket(websocket: WebSocket, token: str):
    """
    WebSocket endpoint for voice chat
    Expects JWT token in URL: /voice/ws/{token}
    """

    # Authenticate user via token
    try:
        payload = decode_token(token)
        user_id = str(payload.get("user_id"))
        username = payload.get("username", "Unknown")
    except HTTPException:
        await websocket.close(code=4001)
        return

    # Connect user
    await manager.connect(websocket, user_id, username)

    # Notify others of new connection
    await manager.broadcast({
        "type": "user_joined",
        "user_id": user_id,
        "username": username,
        "timestamp": datetime.utcnow().isoformat()
    }, exclude_user=user_id)

    try:
        while True:
            # Receive data from client
            data = await websocket.receive()

            # Handle text messages (JSON)
            if "text" in data:
                try:
                    message = json.loads(data["text"])
                    await handle_voice_message(message, user_id, username)
                except json.JSONDecodeError:
                    await manager.send_personal_message(
                        {"type": "error", "message": "Invalid JSON"},
                        user_id
                    )

            # Handle binary messages (audio)
            elif "bytes" in data:
                audio_data = data["bytes"]
                await handle_voice_audio(audio_data, user_id, username)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast({
            "type": "user_left",
            "user_id": user_id,
            "username": username,
            "timestamp": datetime.utcnow().isoformat()
        })


async def handle_voice_message(message: dict, user_id: str, username: str):
    """Handle text messages from voice WebSocket"""

    msg_type = message.get("type")

    if msg_type == "ping":
        # Respond to ping
        await manager.send_personal_message(
            {"type": "pong", "timestamp": datetime.utcnow().isoformat()},
            user_id
        )

    elif msg_type == "get_users":
        # Send list of connected users
        users = manager.get_connected_users()
        await manager.send_personal_message(
            {"type": "users_list", "users": users},
            user_id
        )

    elif msg_type == "transcription_request":
        # Request transcription of audio
        # TODO: Integrate Whisper AI
        await manager.send_personal_message(
            {"type": "transcription", "text": "[Whisper AI Placeholder]"},
            user_id
        )

    else:
        # Unknown message type
        await manager.send_personal_message(
            {"type": "error", "message": f"Unknown message type: {msg_type}"},
            user_id
        )


async def handle_voice_audio(audio_data: bytes, user_id: str, username: str):
    """Handle audio data from voice WebSocket"""

    # Broadcast audio to other users
    await manager.broadcast_audio(audio_data, user_id)

    # TODO: Optional - Save audio for Whisper AI transcription
    # TODO: Optional - Voice activity detection (VAD)


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@router.get("/connected_users")
def get_connected_users():
    """Get list of users currently in voice chat"""
    return {"users": manager.get_connected_users()}


@router.get("/status")
def get_voice_status():
    """Get voice chat server status"""
    return {
        "active_connections": len(manager.active_connections),
        "whisper_model": settings.WHISPER_MODEL,
        "tts_engine": settings.TTS_ENGINE,
    }


class TranscribeRequest(BaseModel):
    audio_base64: str


@router.post("/transcribe")
async def transcribe_audio(request: TranscribeRequest):
    """
    Transcribe audio using Whisper AI
    """

    # Import voice service
    from backend.services.voice_service import voice_service

    # Transcribe audio
    result = voice_service.transcribe_base64(request.audio_base64, language="de")

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {result.get('error', 'Unknown error')}"
        )

    return {
        "success": True,
        "transcription": result["text"],
        "language": result.get("language", "de"),
    }


class TTSRequest(BaseModel):
    text: str
    language: str = "de"


@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech using Edge TTS
    """

    # Import voice service
    from backend.services.voice_service import voice_service

    try:
        # Generate audio (returns base64)
        audio_b64 = await voice_service.speak_base64_async(request.text)

        return {
            "success": True,
            "audio_base64": audio_b64,
            "format": "mp3",
            "personality": voice_service.tts.personality
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS failed: {e}"
        )


# ============================================================================
# HELPER FUNCTIONS (to be implemented)
# ============================================================================

def transcribe_with_whisper(audio_path: str) -> str:
    """
    Transcribe audio file using Whisper AI
    TODO: Implement actual Whisper AI integration
    """
    # This should integrate with existing voice scripts:
    # - najika_voice_call.py
    # - NAJIKA_VIDEO_TO_VOICE_TRAINING.py
    pass


def generate_tts_audio(text: str, language: str = "de") -> bytes:
    """
    Generate audio from text using TTS engine
    TODO: Implement TTS engine (Edge TTS or Coqui)
    """
    # This should integrate with existing TTS scripts:
    # - najika_tts_edge.py
    # - najika_tts_coqui.py
    pass
