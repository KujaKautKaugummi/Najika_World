#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Voice Separation - Megumin Samples Cleanen
Nutzt Demucs um Vocals von Music/Effects zu trennen

INPUT: C:/Najika-World/voice_data/samples/megumin_najika/*.wav
OUTPUT: C:/Najika-World/voice_data/samples/megumin_clean/*.wav
"""

import subprocess
import sys
import io
from pathlib import Path
from datetime import datetime
import pytz
import shutil

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Project Root Directory (dynamisch für alle Systeme)
NAJIKA_DIR = Path(__file__).resolve().parent.parent
VOICE_DIR = NAJIKA_DIR / 'voice_data'
SAMPLES_DIR = VOICE_DIR / 'samples' / 'megumin_najika'
CLEAN_DIR = VOICE_DIR / 'samples' / 'megumin_clean'
DEMUCS_OUTPUT_DIR = VOICE_DIR / 'demucs_separated'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] [{level}] {message}')

def separate_audio(input_file, output_dir):
    """
    Trennt Audio mit Demucs

    Args:
        input_file: Path zur Input-WAV-Datei
        output_dir: Output-Directory für separated Files

    Returns:
        Path zur vocals.wav oder None bei Fehler
    """

    log(f"Trenne: {input_file.name}", 'INFO')

    try:
        # Demucs Command
        # --two-stems=vocals → Trennt nur Vocals vs. Accompaniment (schneller!)
        # -o output_dir → Output Directory
        cmd = [
            'demucs',
            '--two-stems=vocals',
            '-o', str(output_dir),
            str(input_file)
        ]

        log(f"  Command: {' '.join(cmd)}", 'DEBUG')

        # Führe Demucs aus
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode != 0:
            log(f"  Demucs Fehler: {result.stderr}", 'ERROR')
            return None

        # Demucs Output Pfad: output_dir/htdemucs/{filename_without_ext}/vocals.wav
        stem_dir = output_dir / 'htdemucs' / input_file.stem
        vocals_file = stem_dir / 'vocals.wav'

        if vocals_file.exists():
            log(f"  ✅ Vocals extrahiert: {vocals_file}", 'SUCCESS')
            return vocals_file
        else:
            log(f"  ❌ Vocals nicht gefunden: {vocals_file}", 'ERROR')
            return None

    except Exception as e:
        log(f"  Fehler bei Separation: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        return None

def main():
    """Hauptfunktion"""

    log("="*60, 'INFO')
    log("🎵 VOICE SEPARATION - MEGUMIN SAMPLES", 'INFO')
    log("="*60, 'INFO')

    # Erstelle Output Directories
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    DEMUCS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Finde alle Samples
    samples = list(SAMPLES_DIR.glob('*.wav'))

    if not samples:
        log(f"❌ Keine Samples gefunden in: {SAMPLES_DIR}", 'ERROR')
        return False

    log(f"📁 Gefunden: {len(samples)} Samples", 'INFO')
    log("", 'INFO')

    separated_count = 0

    for i, sample in enumerate(samples, 1):
        log(f"[{i}/{len(samples)}] {sample.name}", 'INFO')

        # Trenne mit Demucs
        vocals_file = separate_audio(sample, DEMUCS_OUTPUT_DIR)

        if vocals_file:
            # Kopiere vocals.wav zu clean samples
            clean_file = CLEAN_DIR / sample.name
            shutil.copy2(vocals_file, clean_file)
            log(f"  💾 Gespeichert: {clean_file.name}", 'SUCCESS')
            separated_count += 1

        log("", 'INFO')

    log("="*60, 'INFO')
    log("✅ SEPARATION KOMPLETT!", 'SUCCESS')
    log("="*60, 'INFO')
    log(f"📊 Statistik:", 'INFO')
    log(f"  - Samples verarbeitet: {len(samples)}", 'INFO')
    log(f"  - Erfolgreich getrennt: {separated_count}", 'INFO')
    log(f"  - Clean Samples in: {CLEAN_DIR}", 'INFO')
    log(f"  - Demucs Output in: {DEMUCS_OUTPUT_DIR}", 'INFO')
    log("="*60, 'INFO')
    log("", 'INFO')
    log("🎯 NÄCHSTER SCHRITT:", 'INFO')
    log("  1. Höre Clean Samples an (sollten NUR Stimmen sein!)", 'INFO')
    log("  2. python train_voice_clone_NAJIKA.py (mit clean samples)", 'INFO')
    log("  3. Teste neue Voice Quality", 'INFO')
    log("="*60, 'INFO')

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
