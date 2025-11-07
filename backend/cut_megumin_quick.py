#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Megumin Cutter - Nutzt vordefinierte Timestamps
"""

import sys
import io
from pathlib import Path
from pydub import AudioSegment

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# INPUT FILE (von User bereitgestellt!)
INPUT_FILE = Path(r"C:\Users\0KKK0\Downloads\KONOSUBA Synchronclip #3_ Lea Kalbhenn spricht Megumin(2) (online-audio-converter.com)_Voice Isolation.mp3")

# OUTPUT DIRECTORY (dynamisch)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'voice_data' / 'samples' / 'megumin_reference'

# TIMESTAMPS (von User definiert!)
SEGMENTS = [
    ("00:30", "00:51"),  # 21s
    ("01:00", "01:15"),  # 15s
    ("01:27", "01:31"),  # 4s
    ("01:49", "02:10"),  # 21s
    ("02:33", "02:45"),  # 12s
]

def parse_timestamp(ts):
    """MM:SS → Sekunden"""
    parts = ts.split(':')
    minutes = int(parts[0])
    seconds = int(parts[1])
    return minutes * 60 + seconds

def main():
    print("="*60)
    print("MEGUMIN VOICE SEGMENTS CUTTER")
    print("="*60)
    print()

    # Prüfe Input
    if not INPUT_FILE.exists():
        print(f"❌ Input-File nicht gefunden:")
        print(f"   {INPUT_FILE}")
        print()
        print("Bitte kopiere die MP3 dorthin oder passe INPUT_FILE an!")
        return False

    print(f"✅ Input: {INPUT_FILE.name}")
    print()

    # Lade Audio
    print("Lade Audio...")
    audio = AudioSegment.from_mp3(str(INPUT_FILE))
    print(f"✅ Geladen: {len(audio)/1000:.1f}s")
    print()

    # Erstelle Output Directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Schneide Segmente
    print("Schneide Segmente:")
    print()

    for i, (start_ts, end_ts) in enumerate(SEGMENTS, 1):
        start_sec = parse_timestamp(start_ts)
        end_sec = parse_timestamp(end_ts)
        duration = end_sec - start_sec

        print(f"[{i}/{len(SEGMENTS)}] {start_ts} - {end_ts} ({duration}s)")

        # Schneide (pydub nutzt Millisekunden!)
        start_ms = int(start_sec * 1000)
        end_ms = int(end_sec * 1000)
        segment = audio[start_ms:end_ms]

        # Speichere
        output_file = OUTPUT_DIR / f"megumin_ref_{i:02d}.wav"
        segment.export(
            str(output_file),
            format='wav',
            parameters=['-ar', '22050']  # 22kHz
        )

        print(f"   → {output_file.name}")
        print()

    print("="*60)
    print("✅ FERTIG!")
    print("="*60)
    print(f"Output: {OUTPUT_DIR}")
    print(f"Files: {len(SEGMENTS)} WAV-Dateien")
    print()
    print("Nächster Schritt:")
    print("  python train_voice_clone_NAJIKA.py")
    print("  (Voice Clone Training mit diesen 5 Samples!)")
    print("="*60)

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
