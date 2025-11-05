#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎤 NAJIKA TTS - COQUI XTTS-v2 (MIT MEGUMIN VOICE CLONE)

ERSETZT: najika_tts_edge.py (Microsoft Neural TTS)
NUTZT: Coqui TTS XTTS-v2 mit Megumin's deutscher Stimme

FEATURES:
- Voice Clone mit echter Megumin-Stimme!
- Lokales Training (kein Cloud!)
- Emotional authentisch
- Deutsche Sprache
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
import pytz

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

NAJIKA_DIR = Path('C:/Najika-World')
VOICE_DIR = NAJIKA_DIR / 'voice_data'
MODELS_DIR = VOICE_DIR / 'models'
OUTPUT_DIR = NAJIKA_DIR / 'digivice' / 'audio'
CONFIG_FILE = MODELS_DIR / 'megumin_voice_config.json'
LOG_FILE = VOICE_DIR / 'tts_coqui.log'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# Globale TTS-Instanz (wird beim ersten Aufruf initialisiert)
_TTS_INSTANCE = None
_REFERENCE_SAMPLE = None

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}'
    print(log_line, file=sys.stderr)  # Nach stderr damit stdout frei bleibt

    VOICE_DIR.mkdir(exist_ok=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
    except:
        pass

def initialize_tts():
    """Initialisiert TTS-Instanz einmalig"""
    global _TTS_INSTANCE, _REFERENCE_SAMPLE

    if _TTS_INSTANCE is not None:
        return _TTS_INSTANCE

    log("Initialisiere Coqui TTS mit Megumin Voice...", 'INFO')

    try:
        from TTS.api import TTS

        # Prüfe ob Voice Config existiert
        if not CONFIG_FILE.exists():
            log(f"Voice Config nicht gefunden: {CONFIG_FILE}", 'ERROR')
            log("Bitte zuerst train_voice_clone_NAJIKA.py ausführen!", 'ERROR')
            return None

        # Lade Config
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        log(f"Voice Config geladen: {config['voice_name']}", 'SUCCESS')
        log(f"Samples: {config['samples_used']} ({config['total_duration']:.1f}s)", 'INFO')
        log(f"Referenz: {config['reference_name']}", 'INFO')

        # Initialisiere XTTS-v2
        _TTS_INSTANCE = TTS(model_name=config['model'])
        _REFERENCE_SAMPLE = config['reference_sample']

        log("TTS initialisiert!", 'SUCCESS')

        return _TTS_INSTANCE

    except ImportError:
        log("Coqui TTS nicht installiert!", 'ERROR')
        log("Installiere mit: pip install TTS", 'ERROR')
        return None

    except Exception as e:
        log(f"TTS Initialisierung Fehler: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        return None

def generate_speech(text, output_filename=None):
    """
    Generiert Speech mit Megumin's geklonter Stimme

    Args:
        text: Text zum Sprechen
        output_filename: Optionaler Dateiname (ohne Pfad)

    Returns:
        Path zur generierten Audio-Datei oder None bei Fehler
    """

    log(f"TTS Request: '{text[:50]}...'", 'INFO')

    # Initialisiere TTS (falls noch nicht geschehen)
    tts = initialize_tts()
    if not tts:
        log("TTS nicht verfügbar - Fallback zu Edge-TTS!", 'ERROR')
        # Fallback zu Edge-TTS
        try:
            from najika_tts_edge import generate_speech as edge_generate
            return edge_generate(text, output_filename)
        except:
            return None

    # Erstelle Output-Datei
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not output_filename:
        timestamp = datetime.now(BERLIN_TZ).strftime('%Y%m%d_%H%M%S')
        output_filename = f'najika_tts_{timestamp}.wav'

    output_path = OUTPUT_DIR / output_filename

    try:
        log("Generiere Audio mit Megumin Voice Clone...", 'INFO')

        # Generiere mit Voice Clone
        tts.tts_to_file(
            text=text,
            speaker_wav=_REFERENCE_SAMPLE,
            language='de',
            file_path=str(output_path)
        )

        if output_path.exists():
            log(f"Audio generiert: {output_path.name}", 'SUCCESS')
            return output_path
        else:
            log("Audio-Generierung fehlgeschlagen!", 'ERROR')
            return None

    except Exception as e:
        log(f"TTS Fehler: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        return None

def main():
    """Test-Funktion"""
    test_text = "EXPLOSION! Ich bin Megumin, Erzmagierin der Crimson Magic Clan! Meine Magie ist unbesiegbar!"

    print("="*60)
    print("NAJIKA TTS - COQUI XTTS-v2 TEST")
    print("="*60)
    print(f"Text: {test_text}")
    print()

    output = generate_speech(test_text)

    if output:
        print()
        print("="*60)
        print(f"ERFOLG! Audio generiert: {output}")
        print("="*60)
    else:
        print()
        print("FEHLER bei Audio-Generierung!")

if __name__ == '__main__':
    main()
