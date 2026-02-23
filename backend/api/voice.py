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
from backend.utils import handle_errors

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
        # Request transcription of audio using Whisper AI
        from backend.services.whisper_service import get_whisper_service

        whisper = get_whisper_service()
        if whisper.is_available() and "audio_base64" in message:
            result = whisper.transcribe_base64(
                audio_base64=message["audio_base64"],
                language=message.get("language")
            )

            if result["success"]:
                await manager.send_personal_message(
                    {
                        "type": "transcription",
                        "text": result["text"],
                        "language": result.get("language", "unknown")
                    },
                    user_id
                )
            else:
                await manager.send_personal_message(
                    {"type": "error", "message": f"Transcription failed: {result['error']}"},
                    user_id
                )
        else:
            await manager.send_personal_message(
                {"type": "error", "message": "Whisper AI not available or audio missing"},
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

    # Optional: Save audio for Whisper AI transcription
    # This can be enabled if you want to auto-transcribe voice chat
    if settings.ENABLE_VOICE_CHAT and hasattr(settings, 'AUTO_TRANSCRIBE_VOICE') and settings.AUTO_TRANSCRIBE_VOICE:
        try:
            import tempfile
            from pathlib import Path

            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name

            # Transcribe using Whisper AI in background
            try:
                transcription = transcribe_with_whisper(temp_path)

                if transcription:
                    # Send transcription back to user
                    await manager.send_personal_message({
                        "type": "auto_transcription",
                        "text": transcription,
                        "timestamp": datetime.utcnow().isoformat()
                    }, user_id)

                    print(f"🎤 Auto-transcribed audio from {username}: {transcription[:50]}...")

            finally:
                # Clean up temp file
                try:
                    Path(temp_path).unlink()
                except:
                    pass

        except Exception as e:
            print(f"❌ Auto-transcription failed: {e}")

    # Optional: Voice Activity Detection (VAD)
    # This can be used to detect if audio contains speech
    # Uncomment and implement if needed:
    # try:
    #     import webrtcvad
    #     vad = webrtcvad.Vad()
    #     vad.set_mode(3)  # Aggressiveness mode (0-3)
    #
    #     # Check if audio contains speech
    #     is_speech = vad.is_speech(audio_data, sample_rate=16000)
    #
    #     if not is_speech:
    #         print(f"⚠️ No speech detected in audio from {username}")
    #         # Optionally don't broadcast non-speech audio
    #
    # except ImportError:
    #     pass  # webrtcvad not installed (pip install webrtcvad)


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
@handle_errors()
async def transcribe_audio(request: TranscribeRequest):
    """
    Transcribe audio using Whisper AI

    Request:
        - audio_base64: Base64 encoded audio file

    Response:
        - success: bool
        - transcription: str
        - language: str
    """

    from backend.services.whisper_service import get_whisper_service

    whisper = get_whisper_service()

    if not whisper.is_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Whisper AI service not available"
        )

    # Transcribe audio
    result = whisper.transcribe_base64(
        audio_base64=request.audio_base64,
        audio_format="wav",
        language=None  # Auto-detect
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {result.get('error', 'Unknown error')}"
        )

    return {
        "success": True,
        "transcription": result["text"],
        "language": result.get("language", "unknown"),
    }


class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice: Optional[str] = None


@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech using TTS engine

    Request:
        - text: Text to convert
        - language: Language code (default: "en")
        - voice: Optional voice name

    Response:
        - success: bool
        - audio_base64: Base64 encoded audio
        - engine: TTS engine used
    """

    from backend.services.tts_service import get_tts_service

    tts = get_tts_service()

    # Generate speech
    result = await tts.generate_speech(
        text=request.text,
        language=request.language,
        voice=request.voice
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS generation failed: {result.get('error', 'Unknown error')}"
        )

    return {
        "success": True,
        "audio_base64": result["audio_base64"],
        "engine": result["engine"],
        "cached": result.get("cached", False)
    }


@router.get("/voices")
@handle_errors()
async def get_available_voices():
    """
    Get list of available TTS voices

    Response:
        - voices: List of voice dictionaries
    """

    from backend.services.tts_service import get_tts_service

    tts = get_tts_service()
    voices = await tts.get_available_voices()

    return {
        "voices": voices,
        "engine": tts.engine,
        "total": len(voices)
    }


@router.get("/languages")
def get_supported_languages():
    """
    Get list of supported languages for speech recognition

    Response:
        - languages: List of language codes
    """

    from backend.services.whisper_service import get_whisper_service

    whisper = get_whisper_service()

    return {
        "languages": whisper.get_supported_languages(),
        "total": len(whisper.get_supported_languages())
    }


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

    Integrates with:
    - backend/services/whisper_service.py (primary)
    - backend/services/voice_service.py (fallback)

    Args:
        audio_path: Path to audio file

    Returns:
        Transcribed text or empty string if failed
    """
    try:
        # Try using the dedicated Whisper service (preferred)
        from backend.services.whisper_service import get_whisper_service

        whisper = get_whisper_service()

        if whisper.is_available():
            result = whisper.transcribe_file(
                audio_path=audio_path,
                language=None,  # Auto-detect language
                task="transcribe"
            )

            if result["success"]:
                print(f"✅ Whisper transcription successful: {result['text'][:100]}...")
                return result["text"]
            else:
                print(f"❌ Whisper transcription failed: {result.get('error', 'Unknown error')}")
                return ""

        else:
            # Fallback to unified voice service
            print("⚠️ Whisper service not available, trying voice_service fallback...")

            from backend.services.voice_service import voice_service

            result = voice_service.transcribe(audio_path, language="de")

            if result["success"]:
                print(f"✅ Voice service transcription successful: {result['text'][:100]}...")
                return result["text"]
            else:
                print(f"❌ Voice service transcription failed: {result.get('error', 'Unknown error')}")
                return ""

    except ImportError as e:
        print(f"❌ Whisper AI not installed: {e}")
        print("   Install with: pip install openai-whisper")
        return ""

    except Exception as e:
        print(f"❌ Transcription error: {e}")
        import traceback
        traceback.print_exc()
        return ""


def generate_tts_audio(text: str, language: str = "de") -> bytes:
    """
    Generate audio from text using TTS engine

    Integrates with:
    - backend/services/tts_service.py (primary - Edge TTS, gTTS, pyttsx3)
    - backend/services/voice_service.py (fallback - Edge TTS)
    - backend/najika_tts_edge.py (fallback - Megumin personality)

    Args:
        text: Text to convert to speech
        language: Language code (de, en, etc.)

    Returns:
        Audio data as bytes, or empty bytes if failed
    """
    try:
        # Try using the dedicated TTS service (preferred)
        from backend.services.tts_service import get_tts_service
        import asyncio

        tts = get_tts_service()

        # Check if engine is available
        engine_name = settings.TTS_ENGINE.lower()

        if engine_name in tts.engines_available and tts.engines_available[engine_name]:
            print(f"🔊 Using TTS engine: {engine_name}")

            # Generate speech (async)
            result = asyncio.run(tts.generate_speech(
                text=text,
                language=language
            ))

            if result["success"]:
                audio_data = result.get("audio_data")
                if audio_data:
                    print(f"✅ TTS generation successful ({len(audio_data)} bytes)")
                    return audio_data
                else:
                    print("❌ TTS generation returned no audio data")
                    # Try fallback
            else:
                print(f"❌ TTS generation failed: {result.get('error', 'Unknown error')}")
                # Try fallback

        # Fallback 1: Try Edge TTS via unified voice service
        print("⚠️ Primary TTS engine not available, trying Edge TTS fallback...")

        try:
            from backend.services.voice_service import voice_service

            audio_path = voice_service.speak(text)

            if audio_path:
                # Read audio file
                from pathlib import Path
                audio_file = Path(audio_path)

                if audio_file.exists():
                    with open(audio_file, 'rb') as f:
                        audio_data = f.read()

                    print(f"✅ Edge TTS (voice_service) successful ({len(audio_data)} bytes)")
                    return audio_data

        except Exception as e:
            print(f"⚠️ Edge TTS (voice_service) fallback failed: {e}")

        # Fallback 2: Try najika_tts_edge directly
        print("⚠️ Trying najika_tts_edge fallback...")

        try:
            from backend.najika_tts_edge import text_to_speech

            # Generate audio with Megumin personality
            audio_path = text_to_speech(text, personality='megumin')

            if audio_path:
                from pathlib import Path
                audio_file = Path(audio_path)

                if audio_file.exists():
                    with open(audio_file, 'rb') as f:
                        audio_data = f.read()

                    print(f"✅ najika_tts_edge successful ({len(audio_data)} bytes)")
                    return audio_data

        except Exception as e:
            print(f"⚠️ najika_tts_edge fallback failed: {e}")

        # All fallbacks failed
        print("❌ All TTS engines failed")
        return b""

    except ImportError as e:
        print(f"❌ TTS engine not installed: {e}")
        print("   Install with: pip install edge-tts")
        return b""

    except Exception as e:
        print(f"❌ TTS generation error: {e}")
        import traceback
        traceback.print_exc()
        return b""
