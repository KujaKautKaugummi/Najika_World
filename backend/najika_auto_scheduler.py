#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA AUTO SCHEDULER - Trainiert automatisch zu festgelegten Zeiten

ZEITEN:
- Nacht: 00:00-08:00 (JEDEN TAG)
- Tag: 08:00-15:00 (Mo-Fr)

USAGE:
  Als Windows Task Scheduler Task alle 30 Minuten ausführen
  Oder manuell: python najika_auto_scheduler.py
"""

import sys
import io
import subprocess
from pathlib import Path
from datetime import datetime, time
import pytz

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Paths
BACKEND_DIR = Path(__file__).resolve().parent
VIDEO_TRAINING_SCRIPT = BACKEND_DIR / 'NAJIKA_REAL_TRAINING.py'  # Personality Videos (PRIORITÄT!)
SESSION_TRAINING_SCRIPT = BACKEND_DIR / 'NAJIKA_SESSION_TRAINING.py'  # Session-Daten
CODE_TRAINING_SCRIPT = BACKEND_DIR / 'NAJIKA_CODE_TRAINING.py'  # Code-Training
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# Welches Training-Script nutzen? (Priorität: Video > Session > Code)
# Videos haben Vorrang, weil sie die Personalities trainieren!
if VIDEO_TRAINING_SCRIPT.exists():
    TRAINING_SCRIPT = VIDEO_TRAINING_SCRIPT
elif SESSION_TRAINING_SCRIPT.exists():
    TRAINING_SCRIPT = SESSION_TRAINING_SCRIPT
else:
    TRAINING_SCRIPT = CODE_TRAINING_SCRIPT

# Training Schedule
NIGHT_START = time(0, 0)   # 00:00
NIGHT_END = time(8, 0)     # 08:00
DAY_START = time(8, 0)     # 08:00
DAY_END = time(15, 0)      # 15:00
WEEKDAYS = [0, 1, 2, 3, 4]  # Mo-Fr

def get_berlin_time():
    """Aktuelle Berlin Zeit"""
    return datetime.now(BERLIN_TZ)

def is_training_time():
    """Prüft ob JETZT Trainingszeit ist"""
    now = get_berlin_time()
    current_time = now.time()
    current_day = now.weekday()

    # Nacht-Training (JEDEN TAG!)
    if NIGHT_START <= current_time < NIGHT_END:
        return True, "NACHT"

    # Tag-Training (nur Mo-Fr)
    if DAY_START <= current_time < DAY_END and current_day in WEEKDAYS:
        return True, "TAG"

    return False, None

def check_ollama():
    """Prüft ob Ollama läuft"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'http://127.0.0.1:11434/api/tags'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def main():
    print()
    print("=" * 70)
    print("NAJIKA AUTO SCHEDULER")
    print("=" * 70)

    now = get_berlin_time()
    print(f"Zeit: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Wochentag: {now.strftime('%A')}")
    print()

    # Prüfe Trainingszeit
    is_time, session_type = is_training_time()

    if not is_time:
        print("❌ Keine Trainingszeit")
        print()
        print("Trainingszeiten:")
        print("  - Nacht: 00:00-08:00 (Mo-So)")
        print("  - Tag: 08:00-15:00 (Mo-Fr)")
        print("=" * 70)
        return

    print(f"✅ Trainingszeit: {session_type}-TRAINING")
    print()

    # Prüfe Ollama
    print("Prüfe Ollama...", end=" ")
    if not check_ollama():
        print("❌ FEHLER!")
        print()
        print("Ollama läuft nicht!")
        print("Bitte starte Ollama: ollama serve")
        print("=" * 70)
        return
    print("✅ OK")
    print()

    # Starte Training
    if TRAINING_SCRIPT == VIDEO_TRAINING_SCRIPT:
        training_type = "VIDEO-PERSONALITY"
    elif TRAINING_SCRIPT == SESSION_TRAINING_SCRIPT:
        training_type = "SESSION"
    else:
        training_type = "CODE"

    print("=" * 70)
    print(f"🚀 STARTE {session_type}-TRAINING ({training_type})")
    print(f"Script: {TRAINING_SCRIPT.name}")
    print("=" * 70)
    print()

    try:
        result = subprocess.run(
            [sys.executable, str(TRAINING_SCRIPT)],
            cwd=str(BACKEND_DIR),
            timeout=3600  # 1 Stunde max
        )

        if result.returncode == 0:
            print()
            print("=" * 70)
            print("✅ TRAINING ERFOLGREICH ABGESCHLOSSEN!")
            print("=" * 70)
        else:
            print()
            print("=" * 70)
            print(f"⚠️  TRAINING BEENDET (Exit Code: {result.returncode})")
            print("=" * 70)

    except subprocess.TimeoutExpired:
        print()
        print("=" * 70)
        print("⏱️  TRAINING TIMEOUT (1 Stunde)")
        print("=" * 70)
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ FEHLER: {e}")
        print("=" * 70)

if __name__ == '__main__':
    main()
