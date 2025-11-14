"""
Voice Service
Integrates Whisper AI (speech-to-text) and Edge TTS (text-to-speech)
"""

import os
import base64
import asyncio
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any

# Try to import Whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper AI not available. Install: pip install openai-whisper")

# Try to import Edge TTS
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ Edge TTS not available. Install: pip install edge-tts")

from backend.config import settings, get_voice_data_path


class WhisperService:
    """Speech-to-Text service using Whisper AI"""

    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model

        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None

        if WHISPER_AVAILABLE:
            self._load_model()
        else:
            print("❌ Whisper AI not available")

    def _load_model(self):
        """Load Whisper model"""
        try:
            print(f"🎤 Loading Whisper model: {self.model_size}...")
            self.model = whisper.load_model(self.model_size)
            print(f"✅ Whisper model loaded: {self.model_size}")
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            self.model = None

    def transcribe(self, audio_path: str, language: str = "de") -> Dict[str, Any]:
        """
        Transcribe audio file

        Args:
            audio_path: Path to audio file
            language: Language code (de, en, etc.)

        Returns:
            Dictionary with transcription result
        """
        if not self.model:
            return {
                "success": False,
                "error": "Whisper model not loaded",
                "text": "",
                "language": language
            }

        try:
            # Transcribe
            result = self.model.transcribe(
                audio_path,
                language=language,
                fp16=False  # CPU compatibility
            )

            return {
                "success": True,
                "text": result["text"],
                "language": result.get("language", language),
                "segments": result.get("segments", [])
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": "",
                "language": language
            }

    def transcribe_from_base64(self, audio_base64: str, language: str = "de") -> Dict[str, Any]:
        """
        Transcribe audio from base64 string

        Args:
            audio_base64: Base64 encoded audio
            language: Language code

        Returns:
            Dictionary with transcription result
        """
        try:
            # Decode base64
            audio_data = base64.b64decode(audio_base64)

            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name

            # Transcribe
            result = self.transcribe(temp_path, language)

            # Cleanup
            try:
                os.remove(temp_path)
            except:
                pass

            return result

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to decode audio: {e}",
                "text": "",
                "language": language
            }


class EdgeTTSService:
    """Text-to-Speech service using Microsoft Edge TTS"""

    def __init__(self, personality: str = "megumin"):
        """
        Initialize Edge TTS service

        Args:
            personality: Voice personality (megumin, harley, shiro, melissa)
        """
        self.personality = personality

        # Voice configurations (from najika_tts_edge.py)
        self.voice_config = {
            'megumin': {
                'voice': 'de-DE-AmalaNeural',
                'rate': '+15%',
                'volume': '+10%',
                'pitch': '+5Hz',
            },
            'harley': {
                'voice': 'de-DE-AmalaNeural',
                'rate': '+25%',
                'volume': '+15%',
                'pitch': '+12Hz',
            },
            'shiro': {
                'voice': 'de-DE-AmalaNeural',
                'rate': '-10%',
                'volume': '+0%',
                'pitch': '-8Hz',
            },
            'melissa': {
                'voice': 'de-DE-AmalaNeural',
                'rate': '+5%',
                'volume': '+5%',
                'pitch': '+2Hz',
            }
        }

        self.config = self.voice_config.get(personality, self.voice_config['megumin'])

        if not EDGE_TTS_AVAILABLE:
            print("❌ Edge TTS not available")

    async def speak_async(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Convert text to speech (async)

        Args:
            text: Text to speak
            output_path: Optional output file path

        Returns:
            Path to generated audio file
        """
        if not EDGE_TTS_AVAILABLE:
            raise Exception("Edge TTS not available")

        # Generate output path if not provided
        if not output_path:
            voice_dir = Path(get_voice_data_path())
            voice_dir.mkdir(parents=True, exist_ok=True)
            output_path = voice_dir / f"tts_{self.personality}_{hash(text) % 10000}.mp3"
            output_path = str(output_path)

        # Create Edge TTS communicator
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.config['voice'],
            rate=self.config['rate'],
            volume=self.config['volume'],
            pitch=self.config['pitch']
        )

        # Generate audio
        await communicate.save(output_path)

        return output_path

    def speak(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Convert text to speech (sync wrapper)

        Args:
            text: Text to speak
            output_path: Optional output file path

        Returns:
            Path to generated audio file
        """
        return asyncio.run(self.speak_async(text, output_path))

    async def speak_to_base64_async(self, text: str) -> str:
        """
        Convert text to speech and return as base64

        Args:
            text: Text to speak

        Returns:
            Base64 encoded audio
        """
        # Generate audio file
        output_path = await self.speak_async(text)

        # Read and encode
        with open(output_path, 'rb') as f:
            audio_data = f.read()

        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        # Cleanup temp file
        try:
            os.remove(output_path)
        except:
            pass

        return audio_base64

    def speak_to_base64(self, text: str) -> str:
        """
        Convert text to speech and return as base64 (sync wrapper)

        Args:
            text: Text to speak

        Returns:
            Base64 encoded audio
        """
        return asyncio.run(self.speak_to_base64_async(text))

    def set_personality(self, personality: str):
        """Change voice personality"""
        if personality in self.voice_config:
            self.personality = personality
            self.config = self.voice_config[personality]
            print(f"🎤 Voice personality changed to: {personality}")
        else:
            print(f"⚠️ Unknown personality: {personality}")


class VoiceService:
    """Unified voice service combining Whisper and Edge TTS"""

    def __init__(
        self,
        whisper_model: str = "base",
        tts_personality: str = "megumin"
    ):
        """
        Initialize unified voice service

        Args:
            whisper_model: Whisper model size
            tts_personality: TTS personality
        """
        self.whisper = WhisperService(model_size=whisper_model)
        self.tts = EdgeTTSService(personality=tts_personality)

        print("🎤 Voice Service initialized")
        print(f"  Whisper: {whisper_model}")
        print(f"  TTS: {tts_personality}")

    def transcribe(self, audio_path: str, language: str = "de") -> Dict[str, Any]:
        """Transcribe audio file"""
        return self.whisper.transcribe(audio_path, language)

    def transcribe_base64(self, audio_base64: str, language: str = "de") -> Dict[str, Any]:
        """Transcribe audio from base64"""
        return self.whisper.transcribe_from_base64(audio_base64, language)

    def speak(self, text: str, output_path: Optional[str] = None) -> str:
        """Convert text to speech (sync)"""
        return self.tts.speak(text, output_path)

    def speak_base64(self, text: str) -> str:
        """Convert text to speech and return base64 (sync)"""
        return self.tts.speak_to_base64(text)

    async def speak_async(self, text: str, output_path: Optional[str] = None) -> str:
        """Convert text to speech (async)"""
        return await self.tts.speak_async(text, output_path)

    async def speak_base64_async(self, text: str) -> str:
        """Convert text to speech and return base64 (async)"""
        return await self.tts.speak_to_base64_async(text)

    def set_tts_personality(self, personality: str):
        """Change TTS personality"""
        self.tts.set_personality(personality)

    def get_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "whisper_available": WHISPER_AVAILABLE,
            "whisper_model": self.whisper.model_size if WHISPER_AVAILABLE else None,
            "edge_tts_available": EDGE_TTS_AVAILABLE,
            "tts_personality": self.tts.personality,
            "tts_voice": self.tts.config['voice']
        }


# Global instance
voice_service = VoiceService(
    whisper_model=settings.WHISPER_MODEL,
    tts_personality="megumin"
)
