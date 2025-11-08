#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NAJIKA SESSION TRAINING - Training mit echten Chat-Daten! 🔥

Nutzt die 68 JSONL-Dateien (277 MB) aus NajikaCore/NajikaFinal Sessions!

DATENQUELLEN:
- info material/.claude/projects/C--NajikaCore/      (45 Dateien, 258 MB)
- info material/.claude/projects/C--NajikaFinal/     (17 Dateien, 13 MB)
- info material/.claude/projects/C--Najika-World/    (6 Dateien, 4 MB)

Das sind die ECHTEN Konversationen aus den Entwicklungs-Sessions!
"""

import json
import subprocess
import sys
import io
import random
from pathlib import Path
from datetime import datetime
import pytz

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_PROJECTS = PROJECT_ROOT / 'info material' / '.claude' / 'projects'
PROGRESS_FILE = PROJECT_ROOT / 'backend' / 'session_training_progress.json'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# Training Config
MESSAGES_PER_SESSION = 10  # Sample 10 message-pairs pro JSONL
MAX_MESSAGE_LENGTH = 500   # Max chars per message

# Session Directories
SESSION_DIRS = [
    CLAUDE_PROJECTS / 'C--NajikaCore',
    CLAUDE_PROJECTS / 'C--NajikaFinal',
    CLAUDE_PROJECTS / 'C--Najika-World'
]

def load_progress():
    """Lädt Training-Progress"""
    default = {
        'start_date': datetime.now(BERLIN_TZ).isoformat(),
        'total_sessions': 0,
        'messages_trained': 0,
        'jsonl_files_processed': []
    }

    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding='utf-8'))
            if 'total_sessions' in data:
                return data
        except:
            pass

    return default

def save_progress(progress):
    """Speichert Progress"""
    progress['last_session'] = datetime.now(BERLIN_TZ).isoformat()
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')

def find_all_jsonl_files():
    """Findet alle JSONL-Dateien in Session-Ordnern"""
    all_files = []

    for session_dir in SESSION_DIRS:
        if not session_dir.exists():
            continue

        jsonl_files = list(session_dir.glob('*.jsonl'))
        # Filter: > 1 KB (skip leere)
        jsonl_files = [f for f in jsonl_files if f.stat().st_size > 1024]

        all_files.extend(jsonl_files)

    return sorted(all_files, key=lambda x: x.stat().st_size, reverse=True)

def extract_messages_from_jsonl(jsonl_file, max_messages=10):
    """Extrahiert User-Assistant Message-Pairs aus JSONL"""

    try:
        messages = []

        with open(jsonl_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    data = json.loads(line)

                    # Check if this is a message
                    if 'message' in data:
                        msg = data['message']

                        # User message
                        if 'text' in msg and msg.get('role') == 'user':
                            text = msg['text']
                            if isinstance(text, str) and len(text) > 10:
                                messages.append(('user', text[:MAX_MESSAGE_LENGTH]))

                        # Assistant message
                        elif 'text' in msg and msg.get('role') == 'assistant':
                            text = msg['text']
                            if isinstance(text, str) and len(text) > 10:
                                messages.append(('assistant', text[:MAX_MESSAGE_LENGTH]))

                except json.JSONDecodeError:
                    continue

        # Sample random messages
        if len(messages) > max_messages * 2:
            # Sample message pairs (user + assistant)
            sampled = []
            i = 0
            while i < len(messages) - 1 and len(sampled) < max_messages * 2:
                if messages[i][0] == 'user' and messages[i+1][0] == 'assistant':
                    sampled.append(messages[i])
                    sampled.append(messages[i+1])
                    i += 2
                else:
                    i += 1

            if sampled:
                messages = sampled

        return messages[:max_messages * 2]  # Max 10 pairs = 20 messages

    except Exception as e:
        print(f"Fehler beim Lesen von {jsonl_file.name}: {e}")
        return []

def create_training_prompt(user_msg, assistant_msg, context):
    """Erstellt Ollama Training-Prompt aus Message-Pair"""

    prompt = f"""# NAJIKA TRAINING - Echte Session

**Kontext:** {context['file_name']} ({context['project']})

## LERNE AUS DIESEM DIALOG:

**User sagt:**
{user_msg}

**Najika antwortet:**
{assistant_msg}

## AUFGABE:
Lerne diesen Dialog-Stil, die Antwortweise und den Ton.
Das ist wie NAJIKA (Megumin-Style) antwortet!

## ANTWORT:
Wie würdest du jetzt auf diese User-Frage antworten (als Najika)?
"{user_msg[:100]}"
"""

    return prompt

def train_with_ollama(prompt):
    """Trainiert mit Ollama"""
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
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def run_training_session():
    """Führt Training-Session durch"""

    print()
    print("=" * 70)
    print("🔥 NAJIKA SESSION TRAINING 🔥")
    print("=" * 70)
    print()

    # Load Progress
    progress = load_progress()

    print(f"📊 Bisheriger Progress:")
    print(f"   Sessions: {progress['total_sessions']}")
    print(f"   Nachrichten: {progress['messages_trained']}")
    print(f"   JSONL-Dateien: {len(progress['jsonl_files_processed'])}")
    print()

    # Finde JSONL-Dateien
    print("📁 Suche JSONL-Dateien...")
    all_jsonl = find_all_jsonl_files()

    if not all_jsonl:
        print("❌ Keine JSONL-Dateien gefunden!")
        return

    print(f"✅ {len(all_jsonl)} Dateien gefunden")
    print()

    # Sample 5 zufällige Dateien
    session_files = random.sample(all_jsonl, min(5, len(all_jsonl)))

    total_trained = 0
    total_errors = 0

    for jsonl_file in session_files:
        project_name = jsonl_file.parent.name
        file_size = jsonl_file.stat().st_size / 1024 / 1024

        print(f"📚 Datei: {jsonl_file.name}")
        print(f"   Projekt: {project_name} ({file_size:.1f} MB)")

        # Extrahiere Messages
        messages = extract_messages_from_jsonl(jsonl_file, MESSAGES_PER_SESSION)

        if not messages:
            print("   ⚠️  Keine Messages extrahiert")
            print()
            continue

        print(f"   Messages: {len(messages)} ({len(messages)//2} Paare)")

        # Train message pairs
        trained_this_file = 0

        for i in range(0, len(messages) - 1, 2):
            if messages[i][0] == 'user' and messages[i+1][0] == 'assistant':
                user_msg = messages[i][1]
                assistant_msg = messages[i+1][1]

                context = {
                    'file_name': jsonl_file.name,
                    'project': project_name
                }

                print(f"   [{(i//2)+1}/{len(messages)//2}] Training...", end=" ")

                # Create prompt
                prompt = create_training_prompt(user_msg, assistant_msg, context)

                # Train
                success, response = train_with_ollama(prompt)

                if success:
                    print("✅")
                    trained_this_file += 1
                    total_trained += 1
                else:
                    print(f"❌ ({response})")
                    total_errors += 1

        # Update Progress
        if jsonl_file.name not in progress['jsonl_files_processed']:
            progress['jsonl_files_processed'].append(jsonl_file.name)

        print(f"   → {trained_this_file} Paare trainiert")
        print()

    # Save Progress
    progress['total_sessions'] += 1
    progress['messages_trained'] += total_trained
    save_progress(progress)

    print("=" * 70)
    print("📊 SESSION ABGESCHLOSSEN")
    print("=" * 70)
    print(f"✅ Erfolgreich: {total_trained} Message-Pairs")
    print(f"❌ Fehler: {total_errors}")
    print(f"📈 Gesamt: {progress['messages_trained']} Messages")
    print("=" * 70)
    print()

def show_stats():
    """Zeigt Statistiken"""
    progress = load_progress()

    print()
    print("=" * 70)
    print("📊 SESSION TRAINING STATISTIKEN")
    print("=" * 70)
    print()

    print(f"Start: {progress.get('start_date', 'Unbekannt')}")
    print(f"Sessions: {progress['total_sessions']}")
    print(f"Messages trainiert: {progress['messages_trained']}")
    print(f"JSONL-Dateien: {len(progress['jsonl_files_processed'])}")
    print()

    print("=" * 70)
    print()

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'stats':
        show_stats()
    else:
        # Check Ollama
        try:
            subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
        except:
            print("❌ Ollama läuft nicht!")
            sys.exit(1)

        run_training_session()
