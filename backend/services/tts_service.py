"""
TTS (Text-to-Speech) Service
Multiple TTS engine support: Edge TTS, gTTS, pyttsx3
"""

import os
import io
import base64
import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path
import tempfile

# Try to import TTS engines
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ Edge TTS not available. Install with: pip install edge-tts")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS not available. Install with: pip install gtts")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("⚠️ pyttsx3 not available. Install with: pip install pyttsx3")

from backend.config import settings


class TTSService:
    """
    Text-to-Speech Service

    Features:
    - Multiple TTS engines (Edge TTS, gTTS, pyttsx3)
    - Multiple languages and voices
    - Customizable speech rate and pitch
    - Audio format conversion
    - Voice caching
    """

    def __init__(self, engine: str = "edge"):
        """
        Initialize TTS Service

        Args:
            engine: TTS engine to use ("edge", "gtts", "pyttsx3")
        """

        self.engine = engine
        self.cache_dir = Path(settings.TTS_CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Engine availability
        self.engines_available = {
            "edge": EDGE_TTS_AVAILABLE,
            "gtts": GTTS_AVAILABLE,
            "pyttsx3": PYTTSX3_AVAILABLE
        }

        # Initialize pyttsx3 if needed
        self.pyttsx3_engine = None
        if engine == "pyttsx3" and PYTTSX3_AVAILABLE:
            self.pyttsx3_engine = pyttsx3.init()

        print(f"🔊 TTS Service initialized with engine: {engine}")
        print(f"   Available engines: {[e for e, available in self.engines_available.items() if available]}")

    async def generate_speech_edge(
        self,
        text: str,
        voice: str = "en-US-AriaNeural",
        rate: str = "+0%",
        pitch: str = "+0Hz"
    ) -> bytes:
        """
        Generate speech using Edge TTS

        Args:
            text: Text to convert to speech
            voice: Voice name (e.g., "en-US-AriaNeural", "de-DE-KatjaNeural")
            rate: Speech rate (e.g., "+50%", "-20%")
            pitch: Speech pitch (e.g., "+5Hz", "-10Hz")

        Returns:
            Audio data as bytes
        """

        if not EDGE_TTS_AVAILABLE:
            raise ImportError("Edge TTS not available")

        # Create communicate object
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)

        # Generate audio
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]

        return audio_data

    def generate_speech_gtts(
        self,
        text: str,
        language: str = "en",
        slow: bool = False
    ) -> bytes:
        """
        Generate speech using gTTS

        Args:
            text: Text to convert to speech
            language: Language code (e.g., "en", "de", "es")
            slow: Use slow speech

        Returns:
            Audio data as bytes
        """

        if not GTTS_AVAILABLE:
            raise ImportError("gTTS not available")

        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=slow)

        # Save to bytes
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer.read()

    def generate_speech_pyttsx3(
        self,
        text: str,
        rate: int = 150,
        volume: float = 1.0
    ) -> bytes:
        """
        Generate speech using pyttsx3

        Args:
            text: Text to convert to speech
            rate: Speech rate (words per minute)
            volume: Volume (0.0 to 1.0)

        Returns:
            Audio data as bytes
        """

        if not PYTTSX3_AVAILABLE or not self.pyttsx3_engine:
            raise ImportError("pyttsx3 not available")

        # Set properties
        self.pyttsx3_engine.setProperty('rate', rate)
        self.pyttsx3_engine.setProperty('volume', volume)

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            self.pyttsx3_engine.save_to_file(text, temp_path)
            self.pyttsx3_engine.runAndWait()

            # Read file
            with open(temp_path, 'rb') as f:
                audio_data = f.read()

            return audio_data

        finally:
            # Clean up
            try:
                os.unlink(temp_path)
            except:
                pass

    async def generate_speech(
        self,
        text: str,
        language: str = "en",
        voice: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate speech using configured engine

        Args:
            text: Text to convert to speech
            language: Language code
            voice: Voice name (engine-specific)
            **kwargs: Additional engine-specific parameters

        Returns:
            Result dictionary with audio data
        """

        try:
            # Check cache first
            cache_key = self.get_cache_key(text, language, voice)
            cached_audio = self.get_from_cache(cache_key)

            if cached_audio:
                print(f"🔊 Using cached audio for: {text[:50]}...")
                return {
                    "success": True,
                    "audio_data": cached_audio,
                    "cached": True,
                    "engine": self.engine
                }

            # Generate based on engine
            audio_data = None

            if self.engine == "edge" and EDGE_TTS_AVAILABLE:
                # Default voice if not specified
                if not voice:
                    voice = self.get_default_edge_voice(language)

                audio_data = await self.generate_speech_edge(
                    text=text,
                    voice=voice,
                    rate=kwargs.get("rate", "+0%"),
                    pitch=kwargs.get("pitch", "+0Hz")
                )

            elif self.engine == "gtts" and GTTS_AVAILABLE:
                audio_data = self.generate_speech_gtts(
                    text=text,
                    language=language,
                    slow=kwargs.get("slow", False)
                )

            elif self.engine == "pyttsx3" and PYTTSX3_AVAILABLE:
                audio_data = self.generate_speech_pyttsx3(
                    text=text,
                    rate=kwargs.get("rate", 150),
                    volume=kwargs.get("volume", 1.0)
                )

            else:
                return {
                    "success": False,
                    "error": f"TTS engine '{self.engine}' not available"
                }

            # Cache the result
            self.save_to_cache(cache_key, audio_data)

            print(f"🔊 Generated speech: {text[:50]}... ({len(audio_data)} bytes)")

            return {
                "success": True,
                "audio_data": audio_data,
                "audio_base64": base64.b64encode(audio_data).decode('utf-8'),
                "cached": False,
                "engine": self.engine
            }

        except Exception as e:
            print(f"❌ TTS generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_default_edge_voice(self, language: str) -> str:
        """Get default Edge TTS voice for language"""

        voice_map = {
            "en": "en-US-AriaNeural",
            "de": "de-DE-KatjaNeural",
            "es": "es-ES-ElviraNeural",
            "fr": "fr-FR-DeniseNeural",
            "it": "it-IT-ElsaNeural",
            "pt": "pt-BR-FranciscaNeural",
            "ja": "ja-JP-NanamiNeural",
            "ko": "ko-KR-SunHiNeural",
            "zh": "zh-CN-XiaoxiaoNeural"
        }

        return voice_map.get(language, "en-US-AriaNeural")

    def get_cache_key(
        self,
        text: str,
        language: str,
        voice: Optional[str]
    ) -> str:
        """Generate cache key for text"""

        import hashlib

        cache_string = f"{self.engine}:{language}:{voice}:{text}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    def get_from_cache(self, cache_key: str) -> Optional[bytes]:
        """Get audio from cache"""

        cache_file = self.cache_dir / f"{cache_key}.mp3"

        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return f.read()

        return None

    def save_to_cache(self, cache_key: str, audio_data: bytes):
        """Save audio to cache"""

        cache_file = self.cache_dir / f"{cache_key}.mp3"

        with open(cache_file, 'wb') as f:
            f.write(audio_data)

    async def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voices for current engine"""

        if self.engine == "edge" and EDGE_TTS_AVAILABLE:
            voices = await edge_tts.list_voices()
            return [
                {
                    "name": voice["Name"],
                    "language": voice["Locale"],
                    "gender": voice["Gender"]
                }
                for voice in voices
            ]

        elif self.engine == "gtts":
            # gTTS supports many languages but no voice selection
            return [{"name": "default", "language": lang} for lang in gTTS.LANGUAGES.keys()]

        elif self.engine == "pyttsx3" and self.pyttsx3_engine:
            voices = self.pyttsx3_engine.getProperty('voices')
            return [
                {
                    "name": voice.name,
                    "id": voice.id,
                    "language": voice.languages[0] if voice.languages else "unknown"
                }
                for voice in voices
            ]

        return []

    def clear_cache(self):
        """Clear TTS cache"""

        count = 0
        for cache_file in self.cache_dir.glob("*.mp3"):
            cache_file.unlink()
            count += 1

        print(f"🗑️ Cleared {count} cached TTS files")
        return count


# Global TTS service instance
_tts_service = None


def get_tts_service() -> TTSService:
    """Get global TTS service instance"""
    global _tts_service
    if _tts_service is None:
        engine = getattr(settings, 'TTS_ENGINE', 'edge')
        _tts_service = TTSService(engine=engine)
    return _tts_service


if __name__ == "__main__":
    # Test TTS service
    import asyncio

    async def test():
        service = TTSService(engine="edge")

        result = await service.generate_speech(
            text="Hello, this is a test of the text to speech system.",
            language="en"
        )

        if result["success"]:
            print("✅ TTS generation successful")
            print(f"   Audio size: {len(result['audio_data'])} bytes")
        else:
            print(f"❌ TTS generation failed: {result['error']}")

    asyncio.run(test())
