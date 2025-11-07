#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Extract ONLY Megumin's Voice
Nutzt pyannote.audio Speaker Diarization um NUR Megumin zu isolieren

INPUT: C:/Najika-World/voice_data/samples/megumin_clean/*.wav (Vocals only)
OUTPUT: C:/Najika-World/voice_data/samples/megumin_only/*.wav (ONLY Megumin!)
"""

import sys
import io
from pathlib import Path
from datetime import datetime
import pytz
import numpy as np
import wave

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Project Root Directory (dynamisch für alle Systeme)
NAJIKA_DIR = Path(__file__).resolve().parent.parent
VOICE_DIR = NAJIKA_DIR / 'voice_data'
CLEAN_DIR = VOICE_DIR / 'samples' / 'megumin_clean'
MEGUMIN_ONLY_DIR = VOICE_DIR / 'samples' / 'megumin_only'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] [{level}] {message}')

def check_dependencies():
    """Prüft ob pyannote.audio installiert ist"""
    try:
        from pyannote.audio import Pipeline
        return True, None
    except ImportError as e:
        return False, str(e)

def extract_megumin_segments(audio_file, output_file):
    """
    Extrahiert NUR Megumin-Segmente aus Audio

    STRATEGIE:
    1. Speaker Diarization → Findet alle verschiedenen Stimmen
    2. Identifiziere Megumin (meist die HÄUFIGSTE Stimme in diesen Files!)
    3. Extrahiere nur Megumin-Segmente
    4. Concatenate zu einem File
    """

    log(f"Analysiere: {audio_file.name}", 'INFO')

    try:
        from pyannote.audio import Pipeline
        import torch
        import torchaudio

        # Lade Diarization Pipeline
        # WICHTIG: Braucht HuggingFace Token für pretrained model!
        log("  Lade Speaker Diarization Model...", 'DEBUG')
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token="YOUR_HUGGINGFACE_TOKEN_HERE"  # ← User muss Token eintragen!
        )

        # Analysiere Audio
        log("  Analysiere Sprecher...", 'DEBUG')
        diarization = pipeline(str(audio_file))

        # Finde häufigsten Sprecher (= Megumin!)
        speaker_durations = {}
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            duration = turn.end - turn.start
            speaker_durations[speaker] = speaker_durations.get(speaker, 0) + duration

        # Megumin = Sprecher mit längster Redezeit
        megumin_speaker = max(speaker_durations.items(), key=lambda x: x[1])[0]
        megumin_duration = speaker_durations[megumin_speaker]

        log(f"  Identifiziert: {len(speaker_durations)} Sprecher", 'INFO')
        log(f"  Megumin (häufigster): {megumin_speaker} ({megumin_duration:.1f}s)", 'SUCCESS')

        # Lade Original Audio
        waveform, sample_rate = torchaudio.load(str(audio_file))

        # Extrahiere Megumin-Segmente
        megumin_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if speaker == megumin_speaker:
                start_sample = int(turn.start * sample_rate)
                end_sample = int(turn.end * sample_rate)
                segment = waveform[:, start_sample:end_sample]
                megumin_segments.append(segment)

        if not megumin_segments:
            log(f"  Keine Megumin-Segmente gefunden!", 'ERROR')
            return False

        # Concatenate alle Segmente
        megumin_audio = torch.cat(megumin_segments, dim=1)

        # Speichere
        torchaudio.save(str(output_file), megumin_audio, sample_rate)

        final_duration = megumin_audio.shape[1] / sample_rate
        log(f"  Extrahiert: {final_duration:.1f}s Megumin-only", 'SUCCESS')

        return True

    except Exception as e:
        log(f"  Fehler: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hauptfunktion"""

    log("="*60, 'INFO')
    log("EXTRACT ONLY MEGUMIN'S VOICE", 'INFO')
    log("="*60, 'INFO')

    # Prüfe Dependencies
    has_deps, error = check_dependencies()
    if not has_deps:
        log("FEHLER: pyannote.audio nicht installiert!", 'ERROR')
        log("", 'INFO')
        log("INSTALLATION:", 'INFO')
        log("1. pip install pyannote.audio", 'INFO')
        log("2. pip install torchaudio", 'INFO')
        log("", 'INFO')
        log("3. HuggingFace Token benötigt:", 'INFO')
        log("   - Gehe zu: https://huggingface.co/settings/tokens", 'INFO')
        log("   - Erstelle neuen Token (read access)", 'INFO')
        log("   - Akzeptiere: https://huggingface.co/pyannote/speaker-diarization-3.1", 'INFO')
        log("   - Trage Token in Script ein (Zeile 51)", 'INFO')
        log("", 'INFO')
        log(f"Error: {error}", 'DEBUG')
        return False

    log("Dependencies OK", 'SUCCESS')

    # Erstelle Output Directory
    MEGUMIN_ONLY_DIR.mkdir(parents=True, exist_ok=True)

    # Finde clean samples
    samples = list(CLEAN_DIR.glob('*.wav'))

    if not samples:
        log(f"Keine Samples gefunden in: {CLEAN_DIR}", 'ERROR')
        return False

    log(f"Gefunden: {len(samples)} Clean Samples", 'INFO')
    log("", 'INFO')

    extracted_count = 0

    for i, sample in enumerate(samples, 1):
        log(f"[{i}/{len(samples)}] {sample.name}", 'INFO')

        output_file = MEGUMIN_ONLY_DIR / sample.name

        if extract_megumin_segments(sample, output_file):
            extracted_count += 1

        log("", 'INFO')

    log("="*60, 'INFO')
    log("EXTRACTION KOMPLETT!", 'SUCCESS')
    log("="*60, 'INFO')
    log(f"Statistik:", 'INFO')
    log(f"  - Samples verarbeitet: {len(samples)}", 'INFO')
    log(f"  - Erfolgreich extrahiert: {extracted_count}", 'INFO')
    log(f"  - Megumin-only Samples: {MEGUMIN_ONLY_DIR}", 'INFO')
    log("="*60, 'INFO')
    log("", 'INFO')
    log("NAECHSTER SCHRITT:", 'INFO')
    log("  python train_voice_clone_NAJIKA.py", 'INFO')
    log("  (Update SAMPLES_DIR zu megumin_only!)", 'INFO')
    log("="*60, 'INFO')

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
