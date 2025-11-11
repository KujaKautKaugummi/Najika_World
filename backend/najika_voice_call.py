#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA VOICE CALL SYSTEM
WebRTC-basierte Voice Calls mit Whisper STT + Coqui TTS

FEATURES:
- Real-time voice input (Whisper STT)
- Najika voice response (Coqui TTS Megumin Voice)
- WebSocket-based audio streaming
- Low latency (<500ms target)
"""

import io
import base64
import numpy as np
import soundfile as sf
from pathlib import Path
import tempfile
import whisper
import threading
import queue
import time
from datetime import datetime

# Import Coqui TTS
try:
    from najika_tts_coqui import generate_speech as coqui_generate_speech
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("[VOICE CALL] ⚠️  Coqui TTS nicht verfügbar!")

class NajikaVoiceCall:
    """Voice Call Handler mit Whisper STT + Coqui TTS"""

    def __init__(self):
        self.whisper_model = None
        self.whisper_model_name = "base"  # base = schnell, medium/large = besser
        self.is_call_active = False
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()

        # Stats
        self.stats = {
            "total_calls": 0,
            "total_duration_sec": 0,
            "avg_stt_latency_ms": 0,
            "avg_tts_latency_ms": 0
        }

        print("[VOICE CALL] Initialisiere Voice Call System...")
        self._load_whisper_model()

    def _load_whisper_model(self):
        """Lädt Whisper Model (lazy loading)"""
        if self.whisper_model is None:
            print(f"[VOICE CALL] Lade Whisper Model ({self.whisper_model_name})...")
            try:
                import whisper
                self.whisper_model = whisper.load_model(self.whisper_model_name)
                print(f"[VOICE CALL] ✅ Whisper Model '{self.whisper_model_name}' geladen!")
            except Exception as e:
                print(f"[VOICE CALL] ❌ Whisper Model Fehler: {e}")
                self.whisper_model = None

    def start_call(self):
        """Startet Voice Call Session"""
        self.is_call_active = True
        self.stats["total_calls"] += 1
        self.call_start_time = time.time()
        print("[VOICE CALL] 📞 Call gestartet!")
        return {
            "status": "call_started",
            "timestamp": datetime.now().isoformat(),
            "tts_available": TTS_AVAILABLE
        }

    def end_call(self):
        """Beendet Voice Call Session"""
        self.is_call_active = False
        call_duration = time.time() - self.call_start_time
        self.stats["total_duration_sec"] += call_duration
        print(f"[VOICE CALL] 📵 Call beendet (Dauer: {call_duration:.1f}s)")
        return {
            "status": "call_ended",
            "duration_sec": call_duration,
            "timestamp": datetime.now().isoformat()
        }

    def process_audio_chunk(self, audio_data_base64):
        """
        Verarbeitet Audio-Chunk (WebRTC → Whisper STT → Text)

        Args:
            audio_data_base64: Base64-encoded audio data (WAV/WebM)

        Returns:
            dict: {"text": "...", "confidence": 0.95, "latency_ms": 234}
        """
        if not self.whisper_model:
            return {"error": "Whisper Model not loaded", "text": ""}

        start_time = time.time()

        try:
            # Decode Base64 audio
            audio_bytes = base64.b64decode(audio_data_base64)

            # Save zu temp file (Whisper braucht File-Path)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name

            # Whisper STT
            result = self.whisper_model.transcribe(
                temp_audio_path,
                language='de',  # Deutsch
                fp16=False  # CPU-kompatibel
            )

            text = result["text"].strip()

            # Cleanup
            Path(temp_audio_path).unlink(missing_ok=True)

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Update stats
            self.stats["avg_stt_latency_ms"] = (
                (self.stats["avg_stt_latency_ms"] * (self.stats["total_calls"] - 1) + latency_ms)
                / self.stats["total_calls"]
            )

            print(f"[VOICE CALL] 🎤 STT: '{text}' ({latency_ms:.0f}ms)")

            return {
                "text": text,
                "language": "de",
                "latency_ms": latency_ms,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[VOICE CALL] ❌ STT Error: {e}")
            return {
                "error": str(e),
                "text": "",
                "latency_ms": 0
            }

    def generate_voice_response(self, text):
        """
        Generiert Najika Voice Response (Coqui TTS)

        Args:
            text: Najika's response text

        Returns:
            dict: {"audio_base64": "...", "duration_sec": 3.5, "latency_ms": 1200}
        """
        if not TTS_AVAILABLE:
            return {
                "error": "TTS not available",
                "audio_base64": "",
                "duration_sec": 0
            }

        start_time = time.time()

        try:
            # Generiere Audio mit Coqui TTS (Megumin Voice!)
            audio_path = coqui_generate_speech(text)

            if not audio_path or not Path(audio_path).exists():
                return {
                    "error": "TTS generation failed",
                    "audio_base64": "",
                    "duration_sec": 0
                }

            # Lese Audio-File
            audio_bytes = Path(audio_path).read_bytes()

            # Encode to Base64
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

            # Get audio duration
            with sf.SoundFile(audio_path) as audio_file:
                duration_sec = len(audio_file) / audio_file.samplerate

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Update stats
            self.stats["avg_tts_latency_ms"] = (
                (self.stats["avg_tts_latency_ms"] * (self.stats["total_calls"] - 1) + latency_ms)
                / self.stats["total_calls"]
            )

            print(f"[VOICE CALL] 🔊 TTS: {len(text)} chars → {duration_sec:.1f}s audio ({latency_ms:.0f}ms)")

            return {
                "audio_base64": audio_base64,
                "duration_sec": duration_sec,
                "latency_ms": latency_ms,
                "text": text,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[VOICE CALL] ❌ TTS Error: {e}")
            return {
                "error": str(e),
                "audio_base64": "",
                "duration_sec": 0
            }

    def get_stats(self):
        """Returns Voice Call Statistics"""
        return {
            **self.stats,
            "is_call_active": self.is_call_active,
            "whisper_model": self.whisper_model_name,
            "tts_available": TTS_AVAILABLE
        }

    def set_whisper_model(self, model_name):
        """
        Ändert Whisper Model

        Args:
            model_name: "tiny", "base", "small", "medium", "large"
        """
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if model_name not in valid_models:
            return {"error": f"Invalid model. Choose from: {valid_models}"}

        self.whisper_model_name = model_name
        self.whisper_model = None  # Force reload
        self._load_whisper_model()

        return {
            "status": "model_changed",
            "model": model_name
        }


# Global instance
VOICE_CALL_SYSTEM = NajikaVoiceCall()


def test_voice_call():
    """Test-Funktion"""
    print("="*80)
    print("NAJIKA VOICE CALL SYSTEM TEST")
    print("="*80)
    print()

    # Start Call
    print("[TEST] Starting call...")
    result = VOICE_CALL_SYSTEM.start_call()
    print(f"  → {result}")
    print()

    # Test STT (würde normalerweise echtes Audio bekommen)
    print("[TEST] Testing STT (skipped - braucht echtes Audio)")
    print()

    # Test TTS
    print("[TEST] Testing TTS...")
    tts_result = VOICE_CALL_SYSTEM.generate_voice_response("EXPLOSION! Das ist ein Test, Kuja!")
    if "error" not in tts_result:
        print(f"  ✅ TTS OK: {tts_result['duration_sec']:.1f}s audio, {tts_result['latency_ms']:.0f}ms latency")
    else:
        print(f"  ❌ TTS Error: {tts_result['error']}")
    print()

    # End Call
    print("[TEST] Ending call...")
    result = VOICE_CALL_SYSTEM.end_call()
    print(f"  → Duration: {result['duration_sec']:.1f}s")
    print()

    # Stats
    print("[TEST] Statistics:")
    stats = VOICE_CALL_SYSTEM.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()

    print("="*80)
    print("TEST COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    test_voice_call()
