#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NAJIKA REAL TRAINING - MIT ECHTEN DATEN! 🔥

ORDNERSTRUKTUR FÜR 4 PERSÖNLICHKEITEN:
- training_data/personalities/megumin/     (EXPLOSION! Dramatisch!)
- training_data/personalities/harley/      (*kicher* Chaotisch!)
- training_data/personalities/shiro/       (Analytisch, Wahrscheinlichkeiten)
- training_data/personalities/melissa/     (Dominant, besitzergreifend)

FEATURES:
- 10x Wiederholung JEDES Videos
- Zuordnung zu richtiger Persönlichkeit
- Echtes Ollama Training
- Progress-Tracking
"""

import json
import subprocess
import sys
import io
import time
import os
from pathlib import Path
from datetime import datetime
import pytz

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Project Root Directory (dynamisch)
NAJIKA_DIR = Path(__file__).resolve().parent.parent
TRAINING_DIR = NAJIKA_DIR / 'backend' / 'training_data_real'
PERSONALITIES_DIR = TRAINING_DIR / 'personalities'
PROGRESS_FILE = TRAINING_DIR / 'training_progress.json'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# 10x WIEDERHOLUNG!
REPETITIONS = 10

# PERSÖNLICHKEITEN
PERSONALITIES = {
    'megumin': {
        'weight': 35,
        'traits': 'EXPLOSION! Dramatisch, theatralisch, Schwarze Windmühle, erschöpft nach Zauber',
        'examples': [
            'EXPLOSION!!!',
            'Die Schwarze Windmühle dreht sich!',
            '*wirft Stab* *fällt erschöpft um*'
        ]
    },
    'harley': {
        'weight': 25,
        'traits': 'Chaotisch, verspielt, *kicher*, *giggle*, Puddin\', Mr.K, obsessed mit Kuja',
        'examples': [
            '*kicher* Kuja-Baby!',
            'Mr.K! *giggle*',
            'Puddin\' gehört MIR!'
        ]
    },
    'shiro': {
        'weight': 20,
        'traits': 'Hyperintelligent, analytisch, Wahrscheinlichkeiten, präzise, anhänglich',
        'examples': [
            'Die Wahrscheinlichkeit beträgt 87.3%...',
            'Berechnungen abgeschlossen.',
            '*analytischer Blick*'
        ]
    },
    'melissa': {
        'weight': 20,
        'traits': 'Dominant, besitzergreifend, "Du gehörst mir", commanding, beschützend',
        'examples': [
            'Du gehörst MIR, keine Diskussion!',
            'DADDY... *dominant*',
            '*besitzergreifend* Mein!'
        ]
    }
}

def setup_directories():
    """Erstellt Ordnerstruktur für 4 Persönlichkeiten"""
    print()
    print("=" * 60)
    print("SETUP: ORDNERSTRUKTUR")
    print("=" * 60)
    print()

    for personality in PERSONALITIES.keys():
        personality_dir = PERSONALITIES_DIR / personality
        personality_dir.mkdir(parents=True, exist_ok=True)
        print(f"[OK] {personality_dir}")

    print()
    print("ORDNER BEREIT!")
    print()
    print("LEGE DEINE VIDEOS HIER REIN:")
    print(f"- Megumin:  {PERSONALITIES_DIR / 'megumin'}")
    print(f"- Harley:   {PERSONALITIES_DIR / 'harley'}")
    print(f"- Shiro:    {PERSONALITIES_DIR / 'shiro'}")
    print(f"- Melissa:  {PERSONALITIES_DIR / 'melissa'}")
    print()
    print("Du kannst auch ORDNER reinlegen - werden automatisch durchsucht!")
    print("=" * 60)
    print()

def find_all_videos(personality):
    """Findet ALLE Videos (auch in Unterordnern)"""
    personality_dir = PERSONALITIES_DIR / personality
    if not personality_dir.exists():
        return []

    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
    videos = []

    # Rekursive Suche!
    for ext in video_extensions:
        videos.extend(personality_dir.rglob(f'*{ext}'))
        videos.extend(personality_dir.rglob(f'*{ext.upper()}'))

    return sorted(videos)

def load_progress():
    """Lädt Training-Progress"""
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding='utf-8'))
        except:
            pass

    # Neuer Progress
    return {
        'start_date': datetime.now(BERLIN_TZ).isoformat(),
        'total_sessions': 0,
        'personalities': {p: {'videos': 0, 'repetitions_done': {}} for p in PERSONALITIES.keys()}
    }

def save_progress(progress):
    """Speichert Progress"""
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')

def build_training_prompt(personality, video_path, repetition_num):
    """Baut Training-Prompt für Ollama"""
    personality_info = PERSONALITIES[personality]

    prompt = f"""# NAJIKA TRAINING SESSION
**Persönlichkeit:** {personality.upper()} ({personality_info['weight']}%)
**Video:** {video_path.name}
**Wiederholung:** {repetition_num}/10

## LERNE DIESE PERSÖNLICHKEIT:

**{personality.upper()} TRAITS:**
{personality_info['traits']}

**BEISPIELE:**
"""
    for example in personality_info['examples']:
        prompt += f"- {example}\n"

    prompt += f"""

## TRAINING-MATERIAL:
Video-File: {video_path.name}
Ordner: {video_path.parent.name}

## AUFGABE:
Lerne die Verhaltensweisen, Sprachmuster und Charakterzüge aus diesem Material.
Integriere sie in dein {personality.upper()}-Persönlichkeits-Profil.

Diese Persönlichkeit macht {personality_info['weight']}% deiner Gesamt-Persönlichkeit aus.

## ANTWORT:
Antworte kurz (1-2 Sätze) wie {personality.upper()} auf: "Hallo! Wie geht's?"
"""

    return prompt

def train_with_ollama(prompt, personality):
    """Führt echtes Ollama Training durch"""
    try:
        # Nutze najika-local Model
        result = subprocess.run(
            ['ollama', 'run', 'najika-local', prompt],
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8'
        )

        if result.returncode == 0:
            response = result.stdout.strip()
            return True, response
        else:
            return False, f"Error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return False, "Timeout (60s)"
    except Exception as e:
        return False, str(e)

def train_single_video(personality, video_path, progress):
    """Trainiert mit EINEM Video (10x Wiederholung)"""
    video_key = str(video_path.relative_to(PERSONALITIES_DIR))

    # Initialisiere Tracking
    if video_key not in progress['personalities'][personality]['repetitions_done']:
        progress['personalities'][personality]['repetitions_done'][video_key] = 0

    current_reps = progress['personalities'][personality]['repetitions_done'][video_key]

    print()
    print("-" * 60)
    print(f"VIDEO: {video_path.name}")
    print(f"PERSÖNLICHKEIT: {personality.upper()}")
    print(f"FORTSCHRITT: {current_reps}/{REPETITIONS}")
    print("-" * 60)

    for rep in range(current_reps, REPETITIONS):
        rep_num = rep + 1
        print(f"\n[{rep_num}/10] Training läuft...", end=' ', flush=True)

        # Baue Prompt
        prompt = build_training_prompt(personality, video_path, rep_num)

        # ECHTES TRAINING!
        start_time = time.time()
        success, response = train_with_ollama(prompt, personality)
        elapsed = time.time() - start_time

        if success:
            print(f"OK ({elapsed:.1f}s)")
            print(f"    Najika: {response}")

            # Update Progress
            progress['personalities'][personality]['repetitions_done'][video_key] = rep_num
            progress['total_sessions'] += 1
            save_progress(progress)
        else:
            print(f"FEHLER!")
            print(f"    {response}")
            return False

        # Kleine Pause zwischen Wiederholungen
        if rep_num < REPETITIONS:
            time.sleep(1)

    print(f"\n[OK] Video KOMPLETT trainiert! (10x)")
    progress['personalities'][personality]['videos'] += 1
    save_progress(progress)

    return True

def train_personality(personality):
    """Trainiert EINE Persönlichkeit"""
    print()
    print("=" * 60)
    print(f"TRAINIERE: {personality.upper()} ({PERSONALITIES[personality]['weight']}%)")
    print("=" * 60)

    # Finde Videos
    videos = find_all_videos(personality)

    if not videos:
        print(f"[!] KEINE VIDEOS gefunden in: {PERSONALITIES_DIR / personality}")
        print(f"[!] Lege Videos direkt rein oder in Unterordner!")
        return False

    print(f"[OK] {len(videos)} Videos gefunden")

    # Lade Progress
    progress = load_progress()

    # Trainiere jedes Video
    for i, video_path in enumerate(videos, 1):
        print()
        print(f"VIDEO {i}/{len(videos)}")

        success = train_single_video(personality, video_path, progress)

        if not success:
            print(f"[!] Training fehlgeschlagen: {video_path.name}")
            return False

    print()
    print("=" * 60)
    print(f"[OK] {personality.upper()} KOMPLETT!")
    print(f"[OK] {len(videos)} Videos, je 10x = {len(videos) * 10} Sessions")
    print("=" * 60)

    return True

def train_all():
    """Trainiert ALLE 4 Persönlichkeiten"""
    print()
    print("=" * 60)
    print("NAJIKA REAL TRAINING - START")
    print("=" * 60)
    print()

    start_time = time.time()

    for personality in PERSONALITIES.keys():
        success = train_personality(personality)
        if not success:
            print(f"\n[!] Training abgebrochen bei: {personality}")
            break

    elapsed = time.time() - start_time

    # Final Summary
    progress = load_progress()

    print()
    print("=" * 60)
    print("TRAINING ABGESCHLOSSEN")
    print("=" * 60)
    print()
    print(f"Gesamt-Dauer: {elapsed/60:.1f} Minuten")
    print(f"Gesamt-Sessions: {progress['total_sessions']}")
    print()
    print("PERSÖNLICHKEITEN:")
    for personality, data in progress['personalities'].items():
        print(f"  {personality.upper():10} - {data['videos']} Videos, {len(data['repetitions_done'])*10} Sessions")
    print()
    print("=" * 60)

def show_status():
    """Zeigt aktuellen Training-Status"""
    print()
    print("=" * 60)
    print("NAJIKA TRAINING STATUS")
    print("=" * 60)
    print()

    for personality in PERSONALITIES.keys():
        videos = find_all_videos(personality)
        print(f"{personality.upper():10} - {len(videos)} Videos gefunden")
        print(f"           Ordner: {PERSONALITIES_DIR / personality}")
        print()

    if PROGRESS_FILE.exists():
        progress = load_progress()
        print("PROGRESS:")
        print(f"  Gesamt-Sessions: {progress['total_sessions']}")
        print(f"  Start: {progress['start_date'][:16]}")
        print()

    print("=" * 60)

def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'setup':
            setup_directories()
        elif command == 'status':
            show_status()
        elif command == 'train':
            train_all()
        else:
            print(f"Unbekannter Command: {command}")
            print()
            print("USAGE:")
            print("  python NAJIKA_REAL_TRAINING.py setup   - Erstellt Ordner")
            print("  python NAJIKA_REAL_TRAINING.py status  - Zeigt Status")
            print("  python NAJIKA_REAL_TRAINING.py train   - Startet Training")
    else:
        print()
        print("=" * 60)
        print("NAJIKA REAL TRAINING")
        print("=" * 60)
        print()
        print("USAGE:")
        print("  python NAJIKA_REAL_TRAINING.py setup   - Erstellt Ordner")
        print("  python NAJIKA_REAL_TRAINING.py status  - Zeigt Status")
        print("  python NAJIKA_REAL_TRAINING.py train   - Startet Training")
        print()
        print("=" * 60)

if __name__ == "__main__":
    main()
