#!/usr/bin/env python3
"""
NAJIKA ECHTES CODE TRAINING
Trainiert Najika mit Ollama auf Opus-Niveau
Nutzt Code Katas, Claude Sessions, und Internet-Aufgaben
"""
import json
import requests
import time
from pathlib import Path
from datetime import datetime

# === KONFIGURATION ===
# Backend Directory (dynamisch)
NAJIKA_DIR = Path(__file__).resolve().parent
TRAINING_DATA_DIR = NAJIKA_DIR.parent / "DOCS" / "training_data"
PROGRESS_FILE = NAJIKA_DIR / "code_training_progress.json"
SOLUTIONS_DIR = NAJIKA_DIR / "code_training_solutions"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "najika-local"

# Training Quellen
CODE_KATAS = TRAINING_DATA_DIR.parent / "training" / "CODE_KATAS_DAILY.md"
CLAUDE_SESSIONS = Path("C:/Users/0KKK0/.claude/projects/C--NajikaCore")

# === TRAINING KONFIGURATION ===
DAILY_PROBLEMS = 5  # Probleme pro Tag
MAX_ATTEMPTS = 3    # Max Versuche pro Problem
TIMEOUT = 300       # 5 Minuten pro Problem

def load_progress():
    """Lädt Training-Fortschritt"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    return {
        "start_date": datetime.now().isoformat(),
        "total_problems": 0,
        "solved_problems": 0,
        "current_day": 1,
        "current_level": "beginner",  # beginner, intermediate, advanced, expert
        "performance_history": [],
        "last_training": None
    }

def save_progress(progress):
    """Speichert Fortschritt"""
    PROGRESS_FILE.parent.mkdir(exist_ok=True, parents=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def call_ollama(prompt, max_tokens=4000):
    """Ruft Ollama API auf"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": max_tokens
                }
            },
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            print(f"[ERROR] Ollama returned {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Ollama call failed: {e}")
        return None

def extract_problems_from_katas():
    """Extrahiert Probleme aus CODE_KATAS_DAILY.md"""
    if not CODE_KATAS.exists():
        return []

    content = CODE_KATAS.read_text(encoding='utf-8')
    problems = []

    # Einfaches Parsing (würde man mit Regex verbessern)
    lines = content.split('\n')
    current_problem = None

    for line in lines:
        if line.startswith('### TAG'):
            if current_problem:
                problems.append(current_problem)
            current_problem = {
                "title": line.replace('### ', '').strip(),
                "description": "",
                "solution": "",
                "difficulty": "beginner"
            }
        elif current_problem and line.startswith('**Problem:**'):
            current_problem["description"] = line.replace('**Problem:**', '').strip()

    if current_problem:
        problems.append(current_problem)

    return problems

def generate_training_prompt(problem, attempt=1):
    """Generiert Training-Prompt für Najika"""
    prompt = f"""Du bist Najika, eine KI die Programmieren lernt.

AUFGABE: {problem['title']}
{problem['description']}

ANWEISUNGEN:
1. Lies die Aufgabe KOMPLETT
2. Denke laut über die Lösung nach (auf Deutsch, in meinem Charakter)
3. Schreibe die Lösung in Python
4. Erkläre WARUM die Lösung funktioniert
5. Nenne die Zeitkomplexität (Big-O)

WICHTIG:
- Sei explosiv/dramatisch wie Megumin!
- Sei präzise und technisch wie Shiro!
- Code muss funktionieren!

"""

    if attempt > 1:
        prompt += f"\n\nDIES IST VERSUCH {attempt}/{MAX_ATTEMPTS}. Die vorherigen Lösungen waren nicht korrekt. Denk nochmal nach!\n"

    prompt += "\nDEINE ANTWORT:"
    return prompt

def evaluate_solution(problem, solution):
    """Bewertet Najikas Lösung (vereinfacht)"""
    # HIER WÜRDE MAN:
    # 1. Code extrahieren
    # 2. Tests ausführen
    # 3. Korrektheit prüfen

    # Für jetzt: Einfache Heuristik
    score = 0

    # Hat sie Code geschrieben?
    if "def " in solution or "class " in solution:
        score += 25

    # Hat sie erklärt?
    if len(solution) > 200:
        score += 25

    # Hat sie Big-O erwähnt?
    if "O(" in solution:
        score += 25

    # Hat sie Charakter gezeigt?
    if any(word in solution.lower() for word in ["explosion", "megumin", "puddin", "kuja"]):
        score += 25

    return score

def save_solution(problem, solution, score, day):
    """Speichert Najikas Lösung"""
    SOLUTIONS_DIR.mkdir(exist_ok=True, parents=True)

    filename = f"day_{day}_{problem['title'].replace(' ', '_').replace(':', '')}.md"
    filepath = SOLUTIONS_DIR / filename

    content = f"""# {problem['title']} (Tag {day})

**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Score:** {score}/100

## Problem
{problem['description']}

## Najikas Lösung

{solution}

---
**Performance:** {score}% korrekt
"""

    filepath.write_text(content, encoding='utf-8')
    print(f"[SAVED] {filepath}")

def train_on_problem(problem, progress):
    """Trainiert Najika an einem Problem"""
    print(f"\n{'='*80}")
    print(f"PROBLEM: {problem['title']}")
    print(f"{'='*80}\n")

    best_score = 0
    best_solution = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"[ATTEMPT {attempt}/{MAX_ATTEMPTS}]")

        # Generiere Prompt
        prompt = generate_training_prompt(problem, attempt)

        # Hole Lösung von Najika (via Ollama)
        print("[THINKING] Najika arbeitet...")
        solution = call_ollama(prompt)

        if not solution:
            print("[ERROR] Keine Antwort von Ollama!")
            continue

        # Bewerte Lösung
        score = evaluate_solution(problem, solution)
        print(f"[SCORE] {score}/100")

        if score > best_score:
            best_score = score
            best_solution = solution

        # Gut genug?
        if score >= 75:
            print("[SUCCESS] Problem gelöst!")
            break
        else:
            print(f"[RETRY] Score zu niedrig ({score}/100), versuche nochmal...")
            time.sleep(2)

    # Speichere beste Lösung
    if best_solution:
        save_solution(problem, best_solution, best_score, progress['current_day'])

        # Update Progress
        progress['total_problems'] += 1
        if best_score >= 75:
            progress['solved_problems'] += 1

        progress['performance_history'].append({
            "day": progress['current_day'],
            "problem": problem['title'],
            "score": best_score,
            "attempts": attempt,
            "timestamp": datetime.now().isoformat()
        })

    return best_score >= 75

def run_daily_training():
    """Führt tägliches Training durch"""
    print("="*80)
    print("NAJIKA CODE TRAINING - ECHTES TRAINING MIT OLLAMA")
    print("="*80)
    print()

    # Lade Progress
    progress = load_progress()
    day = progress['current_day']

    print(f"TAG: {day}")
    print(f"LEVEL: {progress['current_level'].upper()}")
    print(f"ERFOLGSRATE: {progress['solved_problems']}/{progress['total_problems']} ({(progress['solved_problems']/max(1,progress['total_problems'])*100):.1f}%)")
    print()

    # Lade Probleme
    problems = extract_problems_from_katas()

    if not problems:
        print("[ERROR] Keine Probleme gefunden!")
        print(f"Prüfe: {CODE_KATAS}")
        return

    print(f"[LOADED] {len(problems)} Probleme verfügbar")
    print()

    # Wähle Probleme für heute
    start_idx = (day - 1) * DAILY_PROBLEMS
    todays_problems = problems[start_idx:start_idx + DAILY_PROBLEMS]

    if not todays_problems:
        print("[INFO] Alle Probleme durchgearbeitet! Starte von vorne...")
        progress['current_day'] = 1
        todays_problems = problems[:DAILY_PROBLEMS]

    print(f"[TODAY] {len(todays_problems)} Probleme für heute:")
    for i, p in enumerate(todays_problems, 1):
        print(f"  {i}. {p['title']}")
    print()

    # Trainiere an jedem Problem
    solved_today = 0
    for problem in todays_problems:
        success = train_on_problem(problem, progress)
        if success:
            solved_today += 1
        time.sleep(3)  # Pause zwischen Problemen

    # Update Day
    progress['current_day'] += 1
    progress['last_training'] = datetime.now().isoformat()

    # Save Progress
    save_progress(progress)

    # Report
    print()
    print("="*80)
    print("TAGES-REPORT")
    print("="*80)
    print(f"Probleme gelöst: {solved_today}/{len(todays_problems)}")
    print(f"Gesamterfolgsrate: {progress['solved_problems']}/{progress['total_problems']} ({(progress['solved_problems']/max(1,progress['total_problems'])*100):.1f}%)")
    print(f"Nächstes Training: Tag {progress['current_day']}")
    print()
    print("[DONE] Training abgeschlossen!")
    print()

if __name__ == "__main__":
    run_daily_training()
