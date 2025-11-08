#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NAJIKA CODE TRAINING - Training mit echten Code-Daten! 🔥

Nutzt die 71.874 Dateien aus training_data_real/ für Najika's Tech-Wissen!

DATEN:
- 24.272 Markdown-Dateien (Dokumentation)
- 6.421 Java-Dateien
- 6.203 Python-Dateien
- 4.367 C++ Dateien
- 4.251 Go-Dateien
- und viele mehr...

KATEGORIEN:
- Code (LeetCode, Algorithms)
- Best Practices (Clean Code)
- ML/AI (Machine Learning)
- DevOps (Docker, K8s)
- Security (OWASP)
- Patterns (Design Patterns)
- Databases
- System Design
- Web Development

TRAINING-METHODE:
1. Sample zufällige Dateien aus jeder Kategorie
2. Erstelle Frage-Antwort Paare
3. Train mit Ollama
4. Progress-Tracking
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
BACKEND_DIR = Path(__file__).resolve().parent
TRAINING_DIR = BACKEND_DIR / 'training_data_real'
PROGRESS_FILE = BACKEND_DIR / 'code_training_progress.json'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# Training Config
FILES_PER_CATEGORY = 5  # Pro Kategorie
MAX_FILE_SIZE = 50 * 1024  # 50 KB max (damit Prompt nicht zu groß wird)

CATEGORIES = {
    'code': 'Programmierprobleme, Algorithmen, Datenstrukturen',
    'best_practices': 'Clean Code, Best Practices, Code-Qualität',
    'ml_ai': 'Machine Learning, AI, Deep Learning',
    'devops': 'DevOps, Docker, Kubernetes, CI/CD',
    'security': 'Security, OWASP, Penetration Testing',
    'patterns': 'Design Patterns, Architektur-Patterns',
    'databases': 'Datenbanken, SQL, NoSQL',
    'system_design': 'System Design, Skalierung, Architektur',
    'web_dev': 'Web Development, Frontend, Backend',
    'python': 'Python-spezifisches Wissen'
}

def load_progress():
    """Lädt Training-Progress"""
    default_progress = {
        'start_date': datetime.now(BERLIN_TZ).isoformat(),
        'total_sessions': 0,
        'files_trained': 0,
        'categories': {cat: {'files': 0, 'last_trained': None} for cat in CATEGORIES.keys()}
    }

    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding='utf-8'))
            # Validate structure
            if 'total_sessions' in data and 'files_trained' in data:
                return data
        except:
            pass

    return default_progress

def save_progress(progress):
    """Speichert Progress"""
    progress['last_session'] = datetime.now(BERLIN_TZ).isoformat()
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding='utf-8')

def sample_files_from_category(category, count=5):
    """Samplet zufällige Dateien aus einer Kategorie"""
    category_dir = TRAINING_DIR / category
    if not category_dir.exists():
        return []

    # Sammle alle relevanten Dateien
    extensions = ['.md', '.py', '.java', '.cpp', '.go', '.ts', '.js', '.rs', '.swift', '.kt']
    all_files = []

    for ext in extensions:
        all_files.extend(list(category_dir.rglob(f'*{ext}')))

    # Filter nach Größe (nicht zu groß)
    valid_files = [f for f in all_files if f.stat().st_size <= MAX_FILE_SIZE and f.stat().st_size > 100]

    if not valid_files:
        return []

    # Sample zufällig
    sample_count = min(count, len(valid_files))
    return random.sample(valid_files, sample_count)

def create_training_prompt(file_path, category):
    """Erstellt Training-Prompt aus Datei-Inhalt"""

    try:
        # Lese Datei
        content = file_path.read_text(encoding='utf-8', errors='ignore')

        # Truncate wenn zu lang
        if len(content) > 2000:
            content = content[:2000] + "\n... (gekürzt)"

        category_desc = CATEGORIES.get(category, category)

        prompt = f"""# NAJIKA CODE TRAINING SESSION

**Kategorie:** {category.upper()}
**Bereich:** {category_desc}
**Datei:** {file_path.name}
**Typ:** {file_path.suffix}

## LERNE AUS DIESEM CODE/DOKUMENT:

```
{content}
```

## AUFGABE:
Lerne die Konzepte, Patterns und Best Practices aus diesem Material.
Integriere dieses Wissen in dein Tech-Profil als Najika.

## ANTWORT:
Erkläre in 2-3 Sätzen (mit Megumin's Begeisterung!), was du aus diesem Material gelernt hast.
"""

        return prompt

    except Exception as e:
        print(f"Fehler beim Lesen von {file_path.name}: {e}")
        return None

def train_with_ollama(prompt):
    """Führt Training mit Ollama durch"""
    try:
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

def run_training_session():
    """Führt eine komplette Training-Session durch"""

    print()
    print("=" * 70)
    print("🔥 NAJIKA CODE TRAINING SESSION 🔥")
    print("=" * 70)
    print()

    # Load Progress
    progress = load_progress()
    session_start = datetime.now(BERLIN_TZ)

    print(f"📊 Bisheriger Progress:")
    print(f"   - Total Sessions: {progress['total_sessions']}")
    print(f"   - Dateien trainiert: {progress['files_trained']}")
    print()

    # Training für jede Kategorie
    total_trained = 0
    total_errors = 0

    for category in CATEGORIES.keys():
        category_dir = TRAINING_DIR / category

        if not category_dir.exists():
            print(f"⚠️  {category}: Ordner existiert nicht")
            continue

        print(f"📚 Kategorie: {category.upper()}")
        print(f"   {CATEGORIES[category]}")

        # Sample Dateien
        files = sample_files_from_category(category, FILES_PER_CATEGORY)

        if not files:
            print(f"   ⚠️  Keine geeigneten Dateien gefunden")
            print()
            continue

        print(f"   Gefunden: {len(files)} Dateien für Training")

        # Train jede Datei
        for i, file_path in enumerate(files, 1):
            print(f"   [{i}/{len(files)}] Training: {file_path.name}...", end=" ")

            # Erstelle Prompt
            prompt = create_training_prompt(file_path, category)

            if not prompt:
                print("❌ (Fehler beim Lesen)")
                total_errors += 1
                continue

            # Train mit Ollama
            success, response = train_with_ollama(prompt)

            if success:
                print("✅")
                # Zeige erste Zeile der Antwort
                first_line = response.split('\n')[0][:60]
                print(f"        → {first_line}...")
                total_trained += 1
            else:
                print(f"❌ ({response})")
                total_errors += 1

        # Update Progress
        progress['categories'][category]['files'] += len(files)
        progress['categories'][category]['last_trained'] = datetime.now(BERLIN_TZ).isoformat()

        print()

    # Session Summary
    session_end = datetime.now(BERLIN_TZ)
    duration = (session_end - session_start).total_seconds()

    progress['total_sessions'] += 1
    progress['files_trained'] += total_trained
    save_progress(progress)

    print("=" * 70)
    print("📊 SESSION ABGESCHLOSSEN")
    print("=" * 70)
    print(f"✅ Erfolgreich: {total_trained} Dateien")
    print(f"❌ Fehler: {total_errors} Dateien")
    print(f"⏱️  Dauer: {duration:.1f} Sekunden")
    print(f"📈 Gesamt trainiert: {progress['files_trained']} Dateien")
    print("=" * 70)
    print()

def show_stats():
    """Zeigt Training-Statistiken"""
    progress = load_progress()

    print()
    print("=" * 70)
    print("📊 NAJIKA CODE TRAINING STATISTIKEN")
    print("=" * 70)
    print()

    print(f"Start: {progress.get('start_date', 'Unbekannt')}")
    print(f"Sessions: {progress['total_sessions']}")
    print(f"Dateien trainiert: {progress['files_trained']}")
    print()

    print("Kategorie-Details:")
    for category, stats in progress['categories'].items():
        last = stats.get('last_trained', 'Nie')
        if last != 'Nie':
            try:
                dt = datetime.fromisoformat(last)
                last = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass

        print(f"  {category:<20} {stats['files']:>5} Dateien  (Letzte: {last})")

    print()
    print("=" * 70)
    print()

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'stats':
        show_stats()
    else:
        # Prüfe ob Ollama läuft
        try:
            subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
        except:
            print("❌ Ollama läuft nicht! Starte mit: ollama serve")
            sys.exit(1)

        # Starte Training
        run_training_session()
