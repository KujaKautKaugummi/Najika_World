#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎤 VOICE CLONING VORBEREITUNG - MANUELLE VERSION (Claude)
Bereitet Voice Samples aus extrahierten Audio-Dateien vor
"""

import json
import subprocess
import sys
import io
import shutil
from pathlib import Path
from datetime import datetime
import pytz

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Project Root Directory (dynamisch für alle Systeme)
NAJIKA_DIR = Path(__file__).resolve().parent.parent
TRAINING_DIR = NAJIKA_DIR / 'backend' / 'training_data'
AUDIO_DIR = TRAINING_DIR / 'extracted_audio' / 'megumin'
SAMPLES_DIR = NAJIKA_DIR / 'voice_data' / 'samples' / 'megumin_manual'
PROGRESS_FILE = SAMPLES_DIR / 'preparation_log.json'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

FFMPEG_PATH = r"C:\Users\0KKK0\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}'
    print(log_line)

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

def extract_sample_from_audio(audio_file, start_time, duration, output_name):
    """Extrahiert Sample aus bereits extrahiertem Audio"""
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    output_file = SAMPLES_DIR / f"{output_name}.wav"

    if output_file.exists():
        log(f"Sample bereits vorhanden: {output_name}", 'INFO')
        return output_file

    log(f"Extrahiere Sample: {output_name} (Start: {start_time}s, Dauer: {duration}s)...", 'INFO')

    try:
        cmd = [
            FFMPEG_PATH,
            '-i', str(audio_file),
            '-ss', str(start_time),
            '-t', str(duration),
            '-acodec', 'pcm_s16le',  # WAV 16-bit
            '-ar', '22050',  # 22kHz (TTS optimal)
            '-ac', '1',  # Mono
            '-y',
            str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, timeout=60)

        if result.returncode == 0 and output_file.exists():
            duration_actual = get_audio_duration(output_file)
            log(f"✅ Sample extrahiert: {output_name} ({duration_actual:.1f}s)", 'SUCCESS')
            return output_file
        else:
            log(f"❌ FFmpeg Fehler: {result.stderr.decode('utf-8', errors='ignore')[:200]}", 'ERROR')
            return None

    except Exception as e:
        log(f"❌ Sample-Extraktion Fehler: {e}", 'ERROR')
        return None

def prepare_manual_samples():
    """MANUELLE STRATEGIE (Claude):
    - Nehme die ersten 3 Episoden
    - Extrahiere aus jeder Episode 2 Samples (Anfang + Mitte)
    - Jedes Sample 10-15 Sekunden
    - Insgesamt 6 Samples
    """

    log("="*60, 'INFO')
    log("MANUELLE VOICE SAMPLE VORBEREITUNG (by Claude)", 'INFO')
    log("="*60, 'INFO')

    # Liste alle verfügbaren Audio-Dateien
    audio_files = sorted(AUDIO_DIR.glob('KonoSuba*.wav'))

    if not audio_files:
        log("❌ Keine Audio-Dateien gefunden!", 'ERROR')
        return False

    log(f"Gefunden: {len(audio_files)} Audio-Dateien", 'INFO')

    # Strategie: Erste 3 Episoden, jeweils 2 Samples
    samples_to_extract = [
        # Episode 1: Anfang (00:30-00:45 = 15s) + Mitte (10:00-10:15 = 15s)
        {'file_idx': 0, 'start': 30, 'duration': 15, 'name': 'ep1_intro'},
        {'file_idx': 0, 'start': 600, 'duration': 15, 'name': 'ep1_mid'},

        # Episode 2: Anfang (00:30-00:42 = 12s) + Mitte (10:00-10:12 = 12s)
        {'file_idx': 1, 'start': 30, 'duration': 12, 'name': 'ep2_intro'},
        {'file_idx': 1, 'start': 600, 'duration': 12, 'name': 'ep2_mid'},

        # Episode 3: Anfang (00:30-00:40 = 10s) + Mitte (10:00-10:10 = 10s)
        {'file_idx': 2, 'start': 30, 'duration': 10, 'name': 'ep3_intro'},
        {'file_idx': 2, 'start': 600, 'duration': 10, 'name': 'ep3_mid'},
    ]

    extracted_samples = []

    for i, sample_config in enumerate(samples_to_extract, 1):
        log(f"\n[{i}/{len(samples_to_extract)}] Extrahiere Sample: {sample_config['name']}", 'INFO')

        if sample_config['file_idx'] >= len(audio_files):
            log(f"⚠️ Episode {sample_config['file_idx']+1} nicht gefunden, überspringe", 'WARNING')
            continue

        audio_file = audio_files[sample_config['file_idx']]
        log(f"Quelle: {audio_file.name}", 'INFO')

        sample_file = extract_sample_from_audio(
            audio_file,
            sample_config['start'],
            sample_config['duration'],
            sample_config['name']
        )

        if sample_file:
            extracted_samples.append({
                'name': sample_config['name'],
                'file': str(sample_file),
                'source': audio_file.name,
                'duration': get_audio_duration(sample_file)
            })

    # Speichere Ergebnis
    result = {
        'method': 'manual',
        'created_by': 'Claude',
        'timestamp': datetime.now(BERLIN_TZ).isoformat(),
        'samples_extracted': len(extracted_samples),
        'samples': extracted_samples,
        'strategy': 'First 3 episodes, 2 samples each (intro + mid), 10-15s duration'
    }

    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    log("\n" + "="*60, 'INFO')
    log(f"✅ FERTIG! {len(extracted_samples)} Samples extrahiert", 'SUCCESS')
    log(f"📁 Gespeichert in: {SAMPLES_DIR}", 'SUCCESS')
    log(f"📊 Log: {PROGRESS_FILE}", 'SUCCESS')
    log("="*60, 'INFO')

    return True

if __name__ == '__main__':
    try:
        success = prepare_manual_samples()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
