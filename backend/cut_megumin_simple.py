#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Megumin Cutter - Nutzt wave (kein ffmpeg nötig!)
WARNUNG: Braucht WAV Input (nicht MP3!)
"""

import sys
import io
import wave
import struct
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# BITTE MP3 zu WAV konvertieren VORHER!
# Mit Windows Media Player / VLC / Audacity
INPUT_FILE = Path(r"C:\Users\0KKK0\Downloads\megumin_voice.wav")

OUTPUT_DIR = Path('C:/Najika-World/voice_data/samples/megumin_reference')

# TIMESTAMPS
SEGMENTS = [
    ("00:30", "00:51"),
    ("01:00", "01:15"),
    ("01:27", "01:31"),
    ("01:49", "02:10"),
    ("02:33", "02:45"),
]

def parse_timestamp(ts):
    """MM:SS → Sekunden"""
    parts = ts.split(':')
    return int(parts[0]) * 60 + int(parts[1])

def cut_wav_segment(input_wav, start_sec, end_sec, output_wav):
    """Schneide WAV-Segment"""

    with wave.open(str(input_wav), 'rb') as wf:
        framerate = wf.getframerate()
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()

        # Berechne Frames
        start_frame = int(start_sec * framerate)
        end_frame = int(end_sec * framerate)

        # Springe zu Start
        wf.setpos(start_frame)

        # Lese Segment
        frames_to_read = end_frame - start_frame
        data = wf.readframes(frames_to_read)

        # Schreibe Output
        with wave.open(str(output_wav), 'wb') as out_wf:
            out_wf.setnchannels(nchannels)
            out_wf.setsampwidth(sampwidth)
            out_wf.setframerate(framerate)
            out_wf.writeframes(data)

def main():
    print("="*60)
    print("MEGUMIN VOICE SEGMENTS CUTTER (WAV)")
    print("="*60)
    print()

    # Prüfe Input
    if not INPUT_FILE.exists():
        print("❌ Input-File nicht gefunden:")
        print(f"   {INPUT_FILE}")
        print()
        print("BITTE:")
        print("1. Konvertiere MP3 zu WAV mit:")
        print("   - Windows Media Player")
        print("   - VLC Media Player")
        print("   - Audacity")
        print("   - Online Converter")
        print()
        print("2. Speichere als: megumin_voice.wav")
        print("3. Kopiere nach: C:\\Users\\0KKK0\\Downloads\\")
        print()
        print("ODER:")
        print("Installiere ffmpeg: choco install ffmpeg")
        return False

    print(f"✅ Input: {INPUT_FILE.name}")
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

        output_file = OUTPUT_DIR / f"megumin_ref_{i:02d}.wav"

        try:
            cut_wav_segment(INPUT_FILE, start_sec, end_sec, output_file)
            print(f"   ✅ {output_file.name}")
        except Exception as e:
            print(f"   ❌ Fehler: {e}")

        print()

    print("="*60)
    print("✅ FERTIG!")
    print("="*60)
    print(f"Output: {OUTPUT_DIR}")
    print(f"Files: {len(SEGMENTS)} WAV-Dateien")
    print()
    print("Nächster Schritt:")
    print("  python train_voice_clone_NAJIKA.py")
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
