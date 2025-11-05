#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎤 VOICE CLONE TRAINING - MIT NAJIKA's AUTONOMEN SAMPLES
Trainiert Megumin Voice Clone mit Coqui TTS XTTS-v2
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
SAMPLES_DIR = VOICE_DIR / 'samples' / 'megumin_reference'  # ← REFERENCE Samples (User's pure Megumin!)
MODELS_DIR = VOICE_DIR / 'models'
OUTPUT_DIR = VOICE_DIR / 'output'
LOG_FILE = VOICE_DIR / 'voice_clone_training.log'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}'
    print(log_line)

    VOICE_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

def check_tts_installed():
    """Prüft ob Coqui TTS installiert ist"""
    try:
        from TTS.api import TTS
        return True
    except ImportError:
        return False

def get_audio_duration(audio_file):
    """Gibt Audio-Dauer in Sekunden zurück"""
    try:
        import wave
        with wave.open(str(audio_file), 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            return duration
    except:
        return 0.0

def train_voice_clone():
    """Trainiert Voice Clone mit Najika's Samples"""

    log("="*60, 'INFO')
    log("🎤 NAJIKA VOICE CLONE TRAINING 🎤", 'INFO')
    log("="*60, 'INFO')

    # Prüfe TTS
    if not check_tts_installed():
        log("❌ Coqui TTS NICHT installiert!", 'ERROR')
        log("", 'INFO')
        log("INSTALLATION:", 'INFO')
        log("pip install TTS", 'INFO')
        log("", 'INFO')
        log("ODER (falls Fehler):", 'INFO')
        log("pip install TTS --no-deps", 'INFO')
        log("pip install numpy scipy librosa soundfile inflect", 'INFO')
        return False

    log("✅ Coqui TTS installiert", 'SUCCESS')

    # Lade Najika's Analyse
    analysis_file = SAMPLES_DIR / 'preparation_log.json'
    if not analysis_file.exists():
        log(f"❌ Najika's Analyse nicht gefunden: {analysis_file}", 'ERROR')
        return False

    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    log(f"📊 Najika's Analyse geladen:", 'INFO')
    log(f"  - Methode: {analysis['method']}", 'INFO')
    log(f"  - Erstellt von: {analysis['created_by']}", 'INFO')
    log(f"  - Samples: {analysis['samples_extracted']}", 'INFO')
    log(f"  - Strategie: {analysis['strategy'][:80]}...", 'INFO')

    # Sammle Samples
    samples = []
    total_duration = 0.0

    for sample_info in analysis['samples']:
        sample_path = Path(sample_info['file'])
        if sample_path.exists():
            duration = get_audio_duration(sample_path)
            samples.append({
                'path': sample_path,
                'name': sample_info['name'],
                'duration': duration,
                'reason': sample_info.get('reason', 'N/A')
            })
            total_duration += duration
            log(f"  ✅ {sample_info['name']}: {duration:.1f}s - {sample_info.get('reason', '')}", 'INFO')
        else:
            log(f"  ❌ Sample nicht gefunden: {sample_path}", 'ERROR')

    if len(samples) < 3:
        log(f"❌ Zu wenig Samples! ({len(samples)}/3 minimum)", 'ERROR')
        return False

    log(f"", 'INFO')
    log(f"✅ {len(samples)} Samples bereit", 'SUCCESS')
    log(f"📊 Gesamt-Dauer: {total_duration:.1f}s (Ø {total_duration/len(samples):.1f}s)", 'INFO')

    # Initialisiere XTTS-v2
    log("", 'INFO')
    log("🔄 Lade XTTS-v2 Model...", 'INFO')
    log("(Beim ersten Mal: ~2GB Download!)", 'INFO')

    try:
        from TTS.api import TTS

        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

        log("✅ XTTS-v2 geladen!", 'SUCCESS')

    except Exception as e:
        log(f"❌ TTS Model Fehler: {e}", 'ERROR')
        return False

    # Wähle bestes Sample als Referenz (längste Dauer = mehr Kontext)
    reference_sample = max(samples, key=lambda s: s['duration'])
    log(f"", 'INFO')
    log(f"🎯 Referenz-Sample: {reference_sample['name']}", 'INFO')
    log(f"  - Dauer: {reference_sample['duration']:.1f}s", 'INFO')
    log(f"  - Grund: {reference_sample['reason']}", 'INFO')

    # Test-Generierung
    log("", 'INFO')
    log("🎤 TESTE VOICE CLONE...", 'INFO')

    test_text = "EXPLOSION! Meine Magie ist unbesiegbar!"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    test_output = OUTPUT_DIR / 'test_megumin_voice.wav'

    try:
        log(f"Text: '{test_text}'", 'INFO')
        log("Generiere Audio...", 'INFO')

        tts.tts_to_file(
            text=test_text,
            speaker_wav=str(reference_sample['path']),
            language='de',
            file_path=str(test_output)
        )

        if test_output.exists():
            duration = get_audio_duration(test_output)
            log(f"✅ ERFOLG! Test-Audio generiert: {duration:.1f}s", 'SUCCESS')
            log(f"📁 Gespeichert: {test_output}", 'SUCCESS')

            # Speichere Konfiguration
            config = {
                'voice_name': 'Megumin (Deutsch)',
                'model': 'tts_models/multilingual/multi-dataset/xtts_v2',
                'reference_sample': str(reference_sample['path']),
                'reference_name': reference_sample['name'],
                'language': 'de',
                'samples_used': len(samples),
                'total_duration': total_duration,
                'created': datetime.now(BERLIN_TZ).isoformat(),
                'samples': [{'name': s['name'], 'duration': s['duration'], 'reason': s['reason']} for s in samples]
            }

            config_file = MODELS_DIR / 'megumin_voice_config.json'
            MODELS_DIR.mkdir(parents=True, exist_ok=True)

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            log(f"📄 Konfiguration gespeichert: {config_file}", 'SUCCESS')

        else:
            log("❌ Audio-Generierung fehlgeschlagen", 'ERROR')
            return False

    except Exception as e:
        log(f"❌ Voice Clone Test Fehler: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        return False

    log("", 'INFO')
    log("="*60, 'INFO')
    log("✅ VOICE CLONE TRAINING ERFOLGREICH!", 'SUCCESS')
    log("="*60, 'INFO')
    log(f"🎤 Voice: Megumin (Deutsch)", 'INFO')
    log(f"📊 Samples: {len(samples)} ({total_duration:.1f}s)", 'INFO')
    log(f"🎯 Referenz: {reference_sample['name']}", 'INFO')
    log(f"📁 Test-Audio: {test_output}", 'INFO')
    log(f"📄 Config: {config_file}", 'INFO')
    log("="*60, 'INFO')
    log("", 'INFO')
    log("NÄCHSTER SCHRITT:", 'INFO')
    log("najika_tts_edge.py → najika_tts_coqui.py umstellen", 'INFO')
    log("="*60, 'INFO')

    return True

if __name__ == '__main__':
    try:
        success = train_voice_clone()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
