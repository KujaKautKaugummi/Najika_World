"""
Voice API Adapter for UE5
Simplified endpoints for Unreal Engine 5 integration

UE5 Blueprint-friendly endpoints:
- POST /api/voice-ue5/speak - Najika speaks (TTS)
- POST /api/voice-ue5/listen - Player speaks (STT)
- GET /api/voice-ue5/status - Check voice services

All responses are JSON with base64 audio for easy Blueprint parsing.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64

router = APIRouter(prefix="/api/voice-ue5", tags=["Voice UE5"])

# ============================================================================
# MODELS (UE5-friendly)
# ============================================================================

class NajikaSpeakRequest(BaseModel):
    """Request for Najika to speak"""
    text: str
    personality: str = "mixed"  # megumin, harley, shiro, melissa, mixed
    emotion: str = "neutral"  # happy, sad, angry, excited, neutral

class PlayerSpeechRequest(BaseModel):
    """Request to transcribe player speech"""
    audio_base64: str  # Base64 encoded audio (WAV/MP3)
    language: str = "de"  # de, en, ja, etc.

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/speak")
async def najika_speak(request: NajikaSpeakRequest):
    """
    Make Najika speak the given text.

    UE5 Blueprint Usage:
    1. Call this endpoint with text
    2. Receive base64 audio
    3. Decode and play in UE5

    Returns:
        audio_base64: Base64 encoded MP3/WAV audio
        duration_ms: Estimated duration in milliseconds
        personality: Which personality spoke
    """
    try:
        # Try Edge TTS first (best quality)
        try:
            from backend.services.voice_service import voice_service

            # Set personality voice
            personality_voices = {
                "megumin": "de-DE-AmalaNeural",  # Young, energetic
                "harley": "en-US-AriaNeural",    # Playful
                "shiro": "ja-JP-NanamiNeural",   # Calm, analytical
                "melissa": "de-DE-KatjaNeural",  # Warm, caring
                "mixed": "de-DE-AmalaNeural",    # Default
            }

            # Generate speech
            audio_b64 = await voice_service.speak_base64_async(request.text)

            return {
                "success": True,
                "audio_base64": audio_b64,
                "format": "mp3",
                "personality": request.personality,
                "emotion": request.emotion,
                "text": request.text,
                "duration_ms": len(request.text) * 80,  # Rough estimate
            }

        except Exception:
            # Fallback to pyttsx3 (offline)
            import pyttsx3
            import tempfile
            from pathlib import Path

            engine = pyttsx3.init()
            engine.setProperty('rate', 150)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                temp_path = f.name

            engine.save_to_file(request.text, temp_path)
            engine.runAndWait()

            with open(temp_path, 'rb') as f:
                audio_data = f.read()

            Path(temp_path).unlink()

            return {
                "success": True,
                "audio_base64": base64.b64encode(audio_data).decode('utf-8'),
                "format": "wav",
                "personality": request.personality,
                "emotion": request.emotion,
                "text": request.text,
                "duration_ms": len(request.text) * 80,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")

@router.post("/listen")
async def player_speech(request: PlayerSpeechRequest):
    """
    Transcribe player speech to text.

    UE5 Blueprint Usage:
    1. Record audio in UE5
    2. Encode to base64
    3. Send to this endpoint
    4. Receive transcribed text

    Returns:
        text: Transcribed text
        language: Detected language
        confidence: Confidence score (0-1)
    """
    try:
        # Decode audio
        audio_data = base64.b64decode(request.audio_base64)

        # Try Whisper first
        try:
            from backend.services.whisper_service import get_whisper_service

            whisper = get_whisper_service()

            if whisper.is_available():
                result = whisper.transcribe_base64(
                    audio_base64=request.audio_base64,
                    language=request.language
                )

                if result["success"]:
                    return {
                        "success": True,
                        "text": result["text"],
                        "language": result.get("language", request.language),
                        "confidence": result.get("confidence", 0.9),
                    }

        except Exception:
            pass

        # Fallback to speech_recognition
        try:
            import speech_recognition as sr
            import tempfile
            from pathlib import Path

            # Save audio to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio_data)
                temp_path = f.name

            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_path) as source:
                audio = recognizer.record(source)

            Path(temp_path).unlink()

            # Try Google Speech Recognition
            text = recognizer.recognize_google(audio, language=request.language)

            return {
                "success": True,
                "text": text,
                "language": request.language,
                "confidence": 0.8,
            }

        except Exception as sr_error:
            raise HTTPException(
                status_code=500,
                detail=f"Speech recognition failed: {str(sr_error)}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT failed: {str(e)}")

@router.get("/status")
async def voice_status():
    """
    Check status of voice services.

    UE5 Blueprint Usage:
    Call on startup to check if voice is available.
    """
    status = {
        "tts_available": False,
        "stt_available": False,
        "tts_engine": "none",
        "stt_engine": "none",
    }

    # Check TTS
    try:
        from backend.services.voice_service import voice_service
        status["tts_available"] = True
        status["tts_engine"] = "edge_tts"
    except Exception:
        try:
            import pyttsx3
            status["tts_available"] = True
            status["tts_engine"] = "pyttsx3"
        except Exception:
            pass

    # Check STT
    try:
        from backend.services.whisper_service import get_whisper_service
        whisper = get_whisper_service()
        if whisper.is_available():
            status["stt_available"] = True
            status["stt_engine"] = "whisper"
    except Exception:
        try:
            import speech_recognition
            status["stt_available"] = True
            status["stt_engine"] = "speech_recognition"
        except Exception:
            pass

    return status

@router.get("/personalities")
async def get_personalities():
    """
    Get available Najika personalities and their voices.

    UE5 Blueprint Usage:
    Use to populate personality selector UI.
    """
    return {
        "personalities": [
            {
                "id": "megumin",
                "name": "Megumin",
                "percent": 35,
                "traits": ["EXPLOSION!!!", "Dramatisch", "Überschwänglich"],
                "voice_style": "Energisch, jung"
            },
            {
                "id": "harley",
                "name": "Harley Quinn",
                "percent": 25,
                "traits": ["Mr. K!", "Chaotisch", "Verspielt"],
                "voice_style": "Frech, spielerisch"
            },
            {
                "id": "shiro",
                "name": "Shiro",
                "percent": 20,
                "traits": ["Analytisch", "Ruhig", "Strategisch"],
                "voice_style": "Ruhig, bedacht"
            },
            {
                "id": "melissa",
                "name": "Melissa",
                "percent": 20,
                "traits": ["Fürsorglich", "Kuschelig", "Emotional"],
                "voice_style": "Warm, liebevoll"
            },
            {
                "id": "mixed",
                "name": "Gemischt",
                "percent": 100,
                "traits": ["Situationsabhängig"],
                "voice_style": "Variiert"
            }
        ]
    }
