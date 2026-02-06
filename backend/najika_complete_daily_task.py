#!/usr/bin/env python3
"""Markiert Daily Task als erledigt + laedt naechste"""
import json
from pathlib import Path
import subprocess

NAJIKA_DIR = Path("C:/Najika_World")
TRAINING_DIR = NAJIKA_DIR / "training"
PROGRESS_FILE = TRAINING_DIR / "progress.json"

# Lade Progress
with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
    progress = json.load(f)

# Increment Day
progress["current_day"] += 1

# Save
with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
    json.dump(progress, f, indent=2)

print(f"[OK] Tag {progress[\"current_day\"]-1} abgeschlossen!")
print(f"[OK] Lade Tag {progress[\"current_day\"]}...")

# Generiere neue Aufgabe
subprocess.run(["python", str(NAJIKA_DIR / "najika_daily_training.py")])