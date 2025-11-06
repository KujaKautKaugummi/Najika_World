#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔊 NAJIKA TTS - EDGE-TTS INTEGRATION 🔊

Text-to-Speech Service für najika_server.py
Nutzt Microsoft Edge Neural Voices (kostenlos, hohe Qualität)

FEATURES:
- Microsoft Neural TTS (de-DE-AmalaNeural)
- Megumin-Style Voice (Animated, Bright)
- Caching für schnellere Responses
- Async Support
- Keine API Keys nötig

USAGE:
    from najika_tts_edge import NajikaEdgeTTS

    tts = NajikaEdgeTTS()
    audio_file = tts.speak("EXPLOSION!")
"""

import asyncio
import hashlib
from pathlib import Path
from datetime import datetime
import pytz

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

NAJIKA_DIR = Path('C:/NajikaFinal')
VOICE_DIR = NAJIKA_DIR / 'voice_data'
CACHE_DIR = VOICE_DIR / 'cache_edge'
OUTPUT_DIR = VOICE_DIR / 'output'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# Voice Configuration
# WICHTIG: ALLE Persönlichkeiten nutzen Megumin's Stimme (de-DE-AmalaNeural)!
# Nur die Parameter ändern sich je nach Facette
VOICE_CONFIG = {
    'megumin': {
        'voice': 'de-DE-AmalaNeural',  # Megumin's Stimme - Animated, Bright
        'rate': '+15%',  # Energetisch, dramatisch
        'volume': '+10%',  # Laut für EXPLOSION!
        'pitch': '+5Hz',  # Junge, helle Stimme
    },
    'harley': {
        'voice': 'de-DE-AmalaNeural',  # GLEICHE Stimme wie Megumin!
        'rate': '+25%',  # Sehr schnell & chaotisch
        'volume': '+15%',  # Noch lauter, aufgedreht
        'pitch': '+12Hz',  # Höher, aufgeregt
    },
    'shiro': {
        'voice': 'de-DE-AmalaNeural',  # GLEICHE Stimme wie Megumin!
        'rate': '-10%',  # Langsamer, ruhig
        'volume': '+0%',  # Normal, kontrolliert
        'pitch': '-8Hz',  # Tiefer, monotoner
    },
    'melissa': {
        'voice': 'de-DE-AmalaNeural',  # GLEICHE Stimme wie Megumin!
        'rate': '+5%',  # Leicht schneller, casual
        'volume': '+5%',  # Leicht lauter
        'pitch': '+2Hz',  # Leicht höher, freundlich
    }
}

class NajikaEdgeTTS:
    """Najika Text-to-Speech Service (Edge TTS)"""

    def __init__(self, personality='megumin', use_cache=True):
        self.personality = personality
        self.use_cache = use_cache
        self.config = VOICE_CONFIG.get(personality, VOICE_CONFIG['megumin'])

        # Create directories
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        if not EDGE_TTS_AVAILABLE:
            print("[NAJIKA TTS] WARNING: edge-tts nicht installiert!")
            print("[NAJIKA TTS] Install: pip install edge-tts")

    def _get_cache_key(self, text):
        """Generiert Cache-Key aus Text"""
        # Include personality and config in hash
        config_str = f"{self.personality}_{self.config['voice']}_{self.config['rate']}"
        text_hash = hashlib.md5(f"{config_str}_{text}".encode('utf-8')).hexdigest()
        return f"{self.personality}_{text_hash}"

    def _get_cached_audio(self, text):
        """Holt Audio aus Cache"""
        if not self.use_cache:
            return None

        cache_key = self._get_cache_key(text)
        cache_file = CACHE_DIR / f"{cache_key}.mp3"

        if cache_file.exists():
            print(f"[NAJIKA TTS] Cache HIT: {cache_file.name}")
            return cache_file

        return None

    def _cache_audio(self, text, audio_file):
        """Speichert Audio in Cache"""
        if not self.use_cache:
            return

        cache_key = self._get_cache_key(text)
        cache_file = CACHE_DIR / f"{cache_key}.mp3"

        try:
            import shutil
            shutil.copy(audio_file, cache_file)
            print(f"[NAJIKA TTS] Cached: {cache_file.name}")
        except Exception as e:
            print(f"[NAJIKA TTS] Cache-Fehler: {e}")

    async def _generate_speech_async(self, text, output_file):
        """Generiert Audio asynchron"""
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.config['voice'],
            rate=self.config['rate'],
            volume=self.config['volume'],
            pitch=self.config['pitch']
        )

        await communicate.save(str(output_file))

    def speak(self, text, output_file=None):
        """
        Konvertiert Text zu Audio (Megumin's Stimme)

        Args:
            text (str): Text zum Sprechen
            output_file (Path): Optional output file

        Returns:
            Path: Audio-File oder None
        """
        if not EDGE_TTS_AVAILABLE:
            print("[NAJIKA TTS] ERROR: edge-tts nicht verfügbar!")
            return None

        # Check Cache
        cached = self._get_cached_audio(text)
        if cached:
            return cached

        # Output File
        if output_file is None:
            timestamp = datetime.now(BERLIN_TZ).strftime('%Y%m%d_%H%M%S')
            output_file = OUTPUT_DIR / f"najika_{self.personality}_{timestamp}.mp3"

        try:
            print(f"[NAJIKA TTS] Generate ({self.config['voice']}): {text[:50]}...")

            # Run async function
            asyncio.run(self._generate_speech_async(text, output_file))

            print(f"[NAJIKA TTS] Audio erstellt: {output_file.name}")

            # Cache
            self._cache_audio(text, output_file)

            return output_file

        except Exception as e:
            print(f"[NAJIKA TTS] TTS-Fehler: {e}")
            import traceback
            traceback.print_exc()
            return None

    def clear_cache(self):
        """Löscht TTS Cache"""
        if CACHE_DIR.exists():
            import shutil
            shutil.rmtree(CACHE_DIR)
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            print("[NAJIKA TTS] Cache gelöscht!")

# Global Instance (lazy loaded)
_najika_tts_instance = None

def get_tts(personality='megumin'):
    """Gibt TTS-Instance zurück (Singleton per Personality)"""
    global _najika_tts_instance

    # Create new instance if personality changed or doesn't exist
    if _najika_tts_instance is None or _najika_tts_instance.personality != personality:
        _najika_tts_instance = NajikaEdgeTTS(personality=personality)

    return _najika_tts_instance

def text_to_speech(text, personality='megumin'):
    """
    Convenience Function für najika_server.py

    Args:
        text (str): Text zum Sprechen
        personality (str): megumin, harley, shiro, melissa

    Returns:
        Path: Audio-File oder None
    """
    tts = get_tts(personality)
    return tts.speak(text)

# Test
if __name__ == "__main__":
    print("="*60)
    print("NAJIKA TTS TEST (EDGE-TTS)")
    print("="*60)

    if not EDGE_TTS_AVAILABLE:
        print("ERROR: edge-tts nicht installiert!")
        print("Install: pip install edge-tts")
    else:
        # Test alle Persönlichkeiten
        test_texts = {
            'megumin': "EXPLOSION! Meine Magie ist unbesiegbar!",
            'harley': "Puddin! Lass uns Chaos machen!",
            'shiro': "Die Wahrscheinlichkeit ist 99.7 Prozent.",
            'melissa': "Kuja, du bist so interessant!"
        }

        print("\nTeste alle Persönlichkeiten:")
        print("-" * 60)

        for personality, text in test_texts.items():
            print(f"\n{personality.upper()}:")
            tts = NajikaEdgeTTS(personality=personality)
            audio = tts.speak(text)

            if audio:
                print(f"  [OK] SUCCESS: {audio}")
            else:
                print(f"  [ERROR] FEHLER!")

        print("\n" + "="*60)
        print("Test abgeschlossen!")
        print("Alle Audio-Files: C:/NajikaCore/voice_data/output/")
        print("="*60)
