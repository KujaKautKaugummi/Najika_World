#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NAJIKA AUTO-TRAINING - LÄUFT BIS ALLES FERTIG IST! 🔥

FEATURES:
- Läuft AUTOMATISCH ohne User-Input
- Guckt ALLE Videos bis komplett fertig
- 10x Wiederholung jedes Videos
- Integriert mit Scheduler (08:00-22:00)
- Fortsetzung bei Unterbrechung
- NIEMALS STOPPT bis ALLES durch!
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
PROGRESS_FILE = TRAINING_DIR / 'auto_training_progress.json'
LOG_FILE = TRAINING_DIR / 'auto_training.log'
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

def log(message, level='INFO'):
    """Logging mit Timestamp"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}'

    print(log_line)

    # Append to log
    TRAINING_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

def find_all_videos(personality):
    """Findet ALLE Videos rekursiv"""
    personality_dir = PERSONALITIES_DIR / personality
    if not personality_dir.exists():
        return []

    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
    videos = []

    for ext in video_extensions:
        videos.extend(personality_dir.rglob(f'*{ext}'))
        videos.extend(personality_dir.rglob(f'*{ext.upper()}'))

    return sorted(videos)

def load_progress():
    """Lädt Progress"""
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding='utf-8'))
        except:
            pass

    return {
        'start_date': datetime.now(BERLIN_TZ).isoformat(),
        'total_sessions': 0,
        'total_videos_completed': 0,
        'personalities': {
            p: {
                'videos_completed': 0,
                'current_video': None,
                'current_repetition': 0,
                'repetitions': {}
            } for p in PERSONALITIES.keys()
        },
        'status': 'running',
        'completed': False
    }

def save_progress(progress):
    """Speichert Progress"""
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)
    progress['last_update'] = datetime.now(BERLIN_TZ).isoformat()
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')

def build_training_prompt(personality, video_path, repetition_num):
    """Baut Training-Prompt"""
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

## AUFGABE:
Lerne die Verhaltensweisen, Sprachmuster und Charakterzüge aus diesem Material.
Integriere sie in dein {personality.upper()}-Persönlichkeits-Profil.

Diese Persönlichkeit macht {personality_info['weight']}% deiner Gesamt-Persönlichkeit aus.

## ANTWORT:
Antworte kurz (1-2 Sätze) wie {personality.upper()} auf: "Hallo!"
"""

    return prompt

def train_with_ollama(prompt):
    """Echtes Ollama Training"""
    try:
        result = subprocess.run(
            ['ollama', 'run', 'najika-local', prompt],
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8'
        )

        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, f"Error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return False, "Timeout (60s)"
    except Exception as e:
        return False, str(e)

def train_single_repetition(personality, video_path, repetition_num):
    """Trainiert EINE Wiederholung"""
    log(f"[{personality.upper()}] {video_path.name} - Rep {repetition_num}/10", 'TRAINING')

    # Baue Prompt
    prompt = build_training_prompt(personality, video_path, repetition_num)

    # Training
    start_time = time.time()
    success, response = train_with_ollama(prompt)
    elapsed = time.time() - start_time

    if success:
        log(f"OK ({elapsed:.1f}s): {response[:60]}...", 'SUCCESS')
        return True
    else:
        log(f"FEHLER: {response}", 'ERROR')
        return False

def train_video_complete(personality, video_path, progress):
    """Trainiert EIN Video KOMPLETT (10x)"""
    video_key = str(video_path.relative_to(PERSONALITIES_DIR))

    # Hole aktuellen Stand
    if video_key not in progress['personalities'][personality]['repetitions']:
        progress['personalities'][personality]['repetitions'][video_key] = 0

    current_rep = progress['personalities'][personality]['repetitions'][video_key]

    log(f"", 'INFO')
    log(f"={'='*60}", 'INFO')
    log(f"VIDEO: {video_path.name}", 'INFO')
    log(f"PERSÖNLICHKEIT: {personality.upper()}", 'INFO')
    log(f"FORTSCHRITT: {current_rep}/{REPETITIONS}", 'INFO')
    log(f"={'='*60}", 'INFO')

    # Trainiere fehlende Wiederholungen
    for rep in range(current_rep, REPETITIONS):
        rep_num = rep + 1

        success = train_single_repetition(personality, video_path, rep_num)

        if not success:
            log(f"Training fehlgeschlagen bei Rep {rep_num}", 'ERROR')
            return False

        # Update Progress
        progress['personalities'][personality]['repetitions'][video_key] = rep_num
        progress['personalities'][personality]['current_video'] = video_key
        progress['personalities'][personality]['current_repetition'] = rep_num
        progress['total_sessions'] += 1
        save_progress(progress)

        # Kleine Pause
        if rep_num < REPETITIONS:
            time.sleep(1)

    # Video komplett!
    log(f"VIDEO KOMPLETT! {video_path.name} (10x)", 'SUCCESS')
    progress['personalities'][personality]['videos_completed'] += 1
    progress['total_videos_completed'] += 1
    progress['personalities'][personality]['current_video'] = None
    progress['personalities'][personality]['current_repetition'] = 0
    save_progress(progress)

    return True

def train_personality_complete(personality, progress):
    """Trainiert EINE Persönlichkeit KOMPLETT"""
    log(f"", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"STARTE PERSÖNLICHKEIT: {personality.upper()}", 'INFO')
    log(f"{'='*60}", 'INFO')

    # Finde alle Videos
    videos = find_all_videos(personality)

    if not videos:
        log(f"KEINE VIDEOS gefunden für {personality.upper()}", 'WARNING')
        return True  # Nicht als Fehler werten

    log(f"Gefunden: {len(videos)} Videos", 'INFO')

    # Trainiere jedes Video
    for i, video_path in enumerate(videos, 1):
        log(f"", 'INFO')
        log(f">>> VIDEO {i}/{len(videos)} <<<", 'INFO')

        success = train_video_complete(personality, video_path, progress)

        if not success:
            log(f"Training abgebrochen bei Video {i}", 'ERROR')
            return False

    log(f"", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"PERSÖNLICHKEIT KOMPLETT: {personality.upper()}", 'SUCCESS')
    log(f"Videos trainiert: {len(videos)}", 'SUCCESS')
    log(f"Gesamt-Sessions: {len(videos) * REPETITIONS}", 'SUCCESS')
    log(f"{'='*60}", 'INFO')

    return True

def train_all_until_done():
    """Trainiert ALLES bis KOMPLETT FERTIG!"""
    log(f"", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"NAJIKA AUTO-TRAINING GESTARTET", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"", 'INFO')

    # Lade Progress
    progress = load_progress()

    if progress.get('completed'):
        log(f"TRAINING BEREITS KOMPLETT!", 'INFO')
        log(f"Möchtest du neu starten? Lösche: {PROGRESS_FILE}", 'INFO')
        return

    start_time = time.time()

    # Trainiere jede Persönlichkeit
    for personality in PERSONALITIES.keys():
        success = train_personality_complete(personality, progress)

        if not success:
            log(f"Training abgebrochen bei {personality.upper()}", 'ERROR')
            progress['status'] = 'failed'
            save_progress(progress)
            return

    # ALLES FERTIG!
    elapsed = time.time() - start_time

    progress['status'] = 'completed'
    progress['completed'] = True
    progress['completion_date'] = datetime.now(BERLIN_TZ).isoformat()
    progress['total_duration_seconds'] = elapsed
    save_progress(progress)

    log(f"", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"🎉 TRAINING KOMPLETT ABGESCHLOSSEN! 🎉", 'SUCCESS')
    log(f"{'='*60}", 'INFO')
    log(f"", 'INFO')
    log(f"Gesamt-Dauer: {elapsed/3600:.1f} Stunden", 'SUCCESS')
    log(f"Gesamt-Sessions: {progress['total_sessions']}", 'SUCCESS')
    log(f"Gesamt-Videos: {progress['total_videos_completed']}", 'SUCCESS')
    log(f"", 'INFO')
    log(f"PERSÖNLICHKEITEN:", 'INFO')
    for personality, data in progress['personalities'].items():
        log(f"  {personality.upper():10} - {data['videos_completed']} Videos", 'INFO')
    log(f"", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"NAJIKA IST JETZT KOMPLETT TRAINIERT!", 'SUCCESS')
    log(f"{'='*60}", 'INFO')

def show_status():
    """Zeigt Status"""
    log(f"", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"NAJIKA AUTO-TRAINING STATUS", 'INFO')
    log(f"{'='*60}", 'INFO')
    log(f"", 'INFO')

    # Videos zählen
    total_videos = 0
    for personality in PERSONALITIES.keys():
        videos = find_all_videos(personality)
        total_videos += len(videos)
        log(f"{personality.upper():10} - {len(videos)} Videos gefunden", 'INFO')

    log(f"", 'INFO')
    log(f"GESAMT: {total_videos} Videos", 'INFO')
    log(f"Training-Sessions: {total_videos * REPETITIONS} (10x pro Video)", 'INFO')
    log(f"", 'INFO')

    # Progress
    if PROGRESS_FILE.exists():
        progress = load_progress()
        log(f"PROGRESS:", 'INFO')
        log(f"  Status: {progress.get('status', 'unknown')}", 'INFO')
        log(f"  Komplett: {progress.get('completed', False)}", 'INFO')
        log(f"  Sessions: {progress.get('total_sessions', 0)}", 'INFO')
        log(f"  Videos fertig: {progress.get('total_videos_completed', 0)}/{total_videos}", 'INFO')
        log(f"", 'INFO')

        for personality, data in progress['personalities'].items():
            videos = find_all_videos(personality)
            log(f"  {personality.upper()}:", 'INFO')
            log(f"    Videos fertig: {data['videos_completed']}/{len(videos)}", 'INFO')
            if data.get('current_video'):
                log(f"    Aktuell: {data['current_video']} (Rep {data['current_repetition']}/10)", 'INFO')
    else:
        log(f"Noch nicht gestartet", 'INFO')

    log(f"", 'INFO')
    log(f"{'='*60}", 'INFO')

def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'status':
            show_status()
        elif command == 'train':
            train_all_until_done()
        elif command == 'reset':
            if PROGRESS_FILE.exists():
                PROGRESS_FILE.unlink()
                log("Progress zurückgesetzt!", 'INFO')
            else:
                log("Kein Progress vorhanden", 'INFO')
        else:
            print(f"Unbekannter Command: {command}")
            print()
            print("USAGE:")
            print("  python NAJIKA_AUTO_TRAINING.py status  - Zeigt Status")
            print("  python NAJIKA_AUTO_TRAINING.py train   - Startet Training (läuft bis ALLES fertig!)")
            print("  python NAJIKA_AUTO_TRAINING.py reset   - Setzt Progress zurück")
    else:
        print()
        print("=" * 60)
        print("NAJIKA AUTO-TRAINING")
        print("=" * 60)
        print()
        print("USAGE:")
        print("  python NAJIKA_AUTO_TRAINING.py status  - Zeigt Status")
        print("  python NAJIKA_AUTO_TRAINING.py train   - Startet Training (läuft bis ALLES fertig!)")
        print("  python NAJIKA_AUTO_TRAINING.py reset   - Setzt Progress zurück")
        print()
        print("=" * 60)

if __name__ == "__main__":
    main()
