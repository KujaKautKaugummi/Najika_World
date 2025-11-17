"""
Whisper Service
Speech-to-Text using OpenAI's Whisper AI
"""

import os
import io
import base64
from typing import Optional, Dict, Any, List
from pathlib import Path
import tempfile

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper not available. Install with: pip install openai-whisper")

from backend.config import settings


class WhisperService:
    """
    Whisper AI Speech-to-Text Service

    Features:
    - Audio transcription (multiple languages)
    - Audio translation to English
    - Language detection
    - Timestamp support
    - Multiple model sizes
    """

    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper Service

        Args:
            model_name: Model size (tiny, base, small, medium, large)
        """

        self.model_name = model_name
        self.model = None
        self.supported_languages = [
            "en", "de", "es", "fr", "it", "pt", "nl", "pl", "ru",
            "ja", "ko", "zh", "ar", "tr", "hi", "vi", "th", "id"
        ]

        # Model info
        self.model_sizes = {
            "tiny": {"params": "39M", "speed": "~32x"},
            "base": {"params": "74M", "speed": "~16x"},
            "small": {"params": "244M", "speed": "~6x"},
            "medium": {"params": "769M", "speed": "~2x"},
            "large": {"params": "1550M", "speed": "~1x"}
        }

        # Initialize if available
        if WHISPER_AVAILABLE:
            self.load_model()
        else:
            print("❌ Whisper not available - service disabled")

    def load_model(self):
        """Load Whisper model"""

        if not WHISPER_AVAILABLE:
            raise ImportError("Whisper not available")

        print(f"🎤 Loading Whisper model: {self.model_name}...")

        try:
            self.model = whisper.load_model(self.model_name)
            print(f"✅ Whisper model loaded successfully")
            print(f"   Size: {self.model_sizes.get(self.model_name, {}).get('params', 'unknown')}")
            print(f"   Speed: {self.model_sizes.get(self.model_name, {}).get('speed', 'unknown')}")

        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            self.model = None

    def transcribe_file(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        timestamps: bool = False
    ) -> Dict[str, Any]:
        """
        Transcribe audio file

        Args:
            audio_path: Path to audio file
            language: Language code (auto-detect if None)
            task: "transcribe" or "translate"
            timestamps: Include word-level timestamps

        Returns:
            Transcription result
        """

        if not self.model:
            return {
                "success": False,
                "error": "Whisper model not loaded"
            }

        if not os.path.exists(audio_path):
            return {
                "success": False,
                "error": f"Audio file not found: {audio_path}"
            }

        try:
            print(f"🎤 Transcribing: {audio_path}")

            # Transcribe
            result = self.model.transcribe(
                audio_path,
                language=language,
                task=task,
                word_timestamps=timestamps
            )

            # Extract results
            transcription = {
                "success": True,
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "segments": []
            }

            # Add segments with timestamps if requested
            if timestamps and "segments" in result:
                for segment in result["segments"]:
                    transcription["segments"].append({
                        "start": segment["start"],
                        "end": segment["end"],
                        "text": segment["text"].strip()
                    })

            print(f"✅ Transcription complete")
            print(f"   Text: {transcription['text'][:100]}...")
            print(f"   Language: {transcription['language']}")

            return transcription

        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def transcribe_audio_data(
        self,
        audio_data: bytes,
        audio_format: str = "wav",
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> Dict[str, Any]:
        """
        Transcribe audio from bytes

        Args:
            audio_data: Audio data as bytes
            audio_format: Audio format (wav, mp3, etc.)
            language: Language code
            task: "transcribe" or "translate"

        Returns:
            Transcription result
        """

        # Save to temporary file
        with tempfile.NamedTemporaryFile(
            suffix=f".{audio_format}",
            delete=False
        ) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name

        try:
            # Transcribe temp file
            result = self.transcribe_file(
                audio_path=temp_path,
                language=language,
                task=task
            )

            return result

        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass

    def transcribe_base64(
        self,
        audio_base64: str,
        audio_format: str = "wav",
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio from base64 string

        Args:
            audio_base64: Base64 encoded audio
            audio_format: Audio format
            language: Language code

        Returns:
            Transcription result
        """

        try:
            # Decode base64
            audio_data = base64.b64decode(audio_base64)

            # Transcribe
            return self.transcribe_audio_data(
                audio_data=audio_data,
                audio_format=audio_format,
                language=language
            )

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to decode base64: {e}"
            }

    def detect_language(self, audio_path: str) -> Dict[str, Any]:
        """
        Detect language of audio

        Args:
            audio_path: Path to audio file

        Returns:
            Language detection result
        """

        if not self.model:
            return {
                "success": False,
                "error": "Whisper model not loaded"
            }

        try:
            # Load audio
            audio = whisper.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)

            # Make log-Mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

            # Detect language
            _, probs = self.model.detect_language(mel)

            # Get top language
            detected_language = max(probs, key=probs.get)
            confidence = probs[detected_language]

            return {
                "success": True,
                "language": detected_language,
                "confidence": float(confidence),
                "all_probabilities": {lang: float(prob) for lang, prob in probs.items()}
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.supported_languages

    def is_available(self) -> bool:
        """Check if Whisper is available and loaded"""
        return WHISPER_AVAILABLE and self.model is not None


# Global Whisper service instance
_whisper_service = None


def get_whisper_service() -> WhisperService:
    """Get global Whisper service instance"""
    global _whisper_service
    if _whisper_service is None:
        model_name = getattr(settings, 'WHISPER_MODEL', 'base')
        _whisper_service = WhisperService(model_name=model_name)
    return _whisper_service


if __name__ == "__main__":
    # Test Whisper service
    service = WhisperService(model_name="base")

    if service.is_available():
        print("✅ Whisper service is available")
        print(f"Supported languages: {len(service.get_supported_languages())}")
    else:
        print("❌ Whisper service is not available")
