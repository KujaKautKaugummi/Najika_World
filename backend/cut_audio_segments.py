#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Audio Segment Cutter - GENAU nach Timestamps
Schneidet exakte Segmente aus Audio-Files

INPUT: MP3/WAV + Timestamps
OUTPUT: Einzelne WAV-Segmente
"""

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
OUTPUT_DIR = VOICE_DIR / 'samples' / 'megumin_reference'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] [{level}] {message}')

def parse_timestamp(ts):
    """
    Konvertiert Timestamp zu Sekunden

    Formats:
    - "00:30" → 30.0
    - "01:15" → 75.0
    - "1:15" → 75.0
    """
    parts = ts.strip().split(':')

    if len(parts) == 2:
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    else:
        raise ValueError(f"Ungültiges Format: {ts} (erwartet: MM:SS)")

def cut_segment(audio_file, start_ts, end_ts, output_file):
    """
    Schneidet Segment aus Audio

    Args:
        audio_file: Path zur Input-Datei (MP3/WAV)
        start_ts: Start-Zeit (z.B. "00:30")
        end_ts: End-Zeit (z.B. "00:51")
        output_file: Output WAV-Datei
    """

    try:
        from pydub import AudioSegment

        # Parse Timestamps
        start_sec = parse_timestamp(start_ts)
        end_sec = parse_timestamp(end_ts)
        duration = end_sec - start_sec

        log(f"Schneide: {start_ts} - {end_ts} ({duration:.1f}s)", 'INFO')

        # Lade Audio
        if audio_file.suffix.lower() == '.mp3':
            audio = AudioSegment.from_mp3(str(audio_file))
        elif audio_file.suffix.lower() in ['.wav', '.wave']:
            audio = AudioSegment.from_wav(str(audio_file))
        else:
            log(f"Unbekanntes Format: {audio_file.suffix}", 'ERROR')
            return False

        # Schneide Segment (pydub nutzt Millisekunden!)
        start_ms = int(start_sec * 1000)
        end_ms = int(end_sec * 1000)
        segment = audio[start_ms:end_ms]

        # Exportiere als WAV
        segment.export(
            str(output_file),
            format='wav',
            parameters=['-ar', '22050']  # 22kHz Sample Rate (gut für TTS!)
        )

        log(f"Gespeichert: {output_file.name} ({duration:.1f}s)", 'SUCCESS')
        return True

    except ImportError:
        log("pydub nicht installiert!", 'ERROR')
        log("Installiere: pip install pydub", 'ERROR')
        log("Braucht auch: ffmpeg (https://ffmpeg.org/download.html)", 'ERROR')
        return False

    except Exception as e:
        log(f"Fehler: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hauptfunktion"""

    log("="*60, 'INFO')
    log("AUDIO SEGMENT CUTTER", 'INFO')
    log("="*60, 'INFO')

    # Frage nach Input-File
    log("", 'INFO')
    log("INPUT-FILE:", 'INFO')
    log("Pfad zur Audio-Datei (MP3 oder WAV):", 'INFO')
    log("Beispiel: C:/Najika-World/voice_data/raw/megumin_full.mp3", 'INFO')
    log("", 'INFO')

    input_path = input("Pfad: ").strip().strip('"')
    audio_file = Path(input_path)

    if not audio_file.exists():
        log(f"Datei nicht gefunden: {audio_file}", 'ERROR')
        return False

    log(f"Geladen: {audio_file.name}", 'SUCCESS')

    # Frage nach Timestamps
    log("", 'INFO')
    log("="*60, 'INFO')
    log("TIMESTAMPS EINGEBEN", 'INFO')
    log("="*60, 'INFO')
    log("Format: START-END (z.B. 00:30-00:51)", 'INFO')
    log("Mehrere Segmente: Eine Zeile pro Segment", 'INFO')
    log("Beenden: Leere Zeile", 'INFO')
    log("", 'INFO')

    segments = []
    segment_num = 1

    while True:
        ts_input = input(f"Segment {segment_num}: ").strip()

        if not ts_input:
            break

        # Parse "START-END"
        if '-' not in ts_input:
            log("Ungültiges Format! Erwartet: START-END (z.B. 00:30-00:51)", 'ERROR')
            continue

        parts = ts_input.split('-')
        if len(parts) != 2:
            log("Ungültiges Format! Erwartet: START-END", 'ERROR')
            continue

        start_ts, end_ts = parts[0].strip(), parts[1].strip()

        try:
            # Validiere Timestamps
            parse_timestamp(start_ts)
            parse_timestamp(end_ts)

            segments.append({
                'start': start_ts,
                'end': end_ts,
                'num': segment_num
            })

            segment_num += 1

        except ValueError as e:
            log(f"Fehler: {e}", 'ERROR')

    if not segments:
        log("Keine Segmente eingegeben - Abbruch!", 'ERROR')
        return False

    log("", 'INFO')
    log(f"Gesamt: {len(segments)} Segmente", 'SUCCESS')

    # Erstelle Output Directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Schneide Segmente
    log("", 'INFO')
    log("="*60, 'INFO')
    log("SCHNEIDE SEGMENTE", 'INFO')
    log("="*60, 'INFO')

    success_count = 0

    for segment in segments:
        output_file = OUTPUT_DIR / f"megumin_ref_{segment['num']:02d}.wav"

        log(f"[{segment['num']}/{len(segments)}] {segment['start']} - {segment['end']}", 'INFO')

        if cut_segment(audio_file, segment['start'], segment['end'], output_file):
            success_count += 1

        log("", 'INFO')

    log("="*60, 'INFO')
    log("FERTIG!", 'SUCCESS')
    log("="*60, 'INFO')
    log(f"Erfolgreich: {success_count}/{len(segments)}", 'INFO')
    log(f"Output: {OUTPUT_DIR}", 'INFO')
    log("="*60, 'INFO')
    log("", 'INFO')
    log("NAECHSTER SCHRITT:", 'INFO')
    log("Prüfe Samples in:", 'INFO')
    log(f"  {OUTPUT_DIR}", 'INFO')
    log("", 'INFO')
    log("Dann:", 'INFO')
    log("  python extract_megumin_manual.py", 'INFO')
    log("="*60, 'INFO')

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log("\n\nAbgebrochen!", 'ERROR')
        sys.exit(1)
    except Exception as e:
        log(f"FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
