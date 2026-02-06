#!/usr/bin/env python3
"""
NAJIKA WORK MANAGER
Zentrale Stelle für alle Najika-Aufgaben
Spart Claude-Tokens durch automatische Script-Ausführung
"""
from pathlib import Path
import subprocess
import sys

NAJIKA_DIR = Path('C:/Najika_World')

AVAILABLE_TASKS = {
    '1': {
        'name': 'Smart Update',
        'script': 'najika_smart_update_v2.py',
        'desc': 'Lädt Session-Kontext, Todos, erwähnte Files'
    },
    '2': {
        'name': 'Technisches Inventar',
        'script': 'najika_technical_inventory.py',
        'desc': 'Scannt NajikaCore - NUR Fakten, keine Interpretationen'
    },
    '3': {
        'name': 'Lesbare Übersicht',
        'script': 'najika_create_readable_overview.py',
        'desc': 'Erstellt verständliche Übersicht aus technischen Daten'
    },
    '4': {
        'name': 'Verbesserungsideen finden',
        'script': 'najika_find_improvements.py',
        'desc': 'Durchsucht ALLE Sessions nach Features/Ideen'
    },
    '5': {
        'name': 'Session-Keyword Suche',
        'script': 'najika_search_all_sessions_for_keywords.py',
        'desc': 'Sucht in allen Sessions nach Keywords'
    },
    '6': {
        'name': 'Zusammenfassungen extrahieren',
        'script': 'najika_extract_summaries_to_desktop.py',
        'desc': 'Extrahiert alle Zusammenfassungen/Roadmaps'
    },
    '7': {
        'name': 'Training starten',
        'script': 'najika_training_scheduler.py',
        'desc': 'Generiert aktuelle Training-Session'
    },
    '8': {
        'name': 'Training abschließen',
        'script': 'najika_complete_training_session.py',
        'desc': 'Markiert Session als erledigt, lädt nächste'
    }
}

def run_task(task_id):
    """Führt Najika-Task aus"""
    if task_id not in AVAILABLE_TASKS:
        print(f"[ERROR] Task {task_id} nicht gefunden!")
        return False

    task = AVAILABLE_TASKS[task_id]
    script = NAJIKA_DIR / task['script']

    if not script.exists():
        print(f"[ERROR] Script nicht gefunden: {script}")
        return False

    print(f"\n{'='*80}")
    print(f"NAJIKA: {task['name']}")
    print(f"{'='*80}\n")
    print(f"Beschreibung: {task['desc']}")
    print(f"Script: {task['script']}")
    print(f"\n{'='*80}\n")

    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(NAJIKA_DIR),
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def show_menu():
    """Zeigt verfügbare Tasks"""
    print("\n" + "="*80)
    print("NAJIKA WORK MANAGER")
    print("="*80 + "\n")
    print("Verfügbare Tasks:\n")

    for task_id, task in sorted(AVAILABLE_TASKS.items()):
        print(f"  [{task_id}] {task['name']}")
        print(f"      → {task['desc']}")
        print()

    print("="*80)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Direkt Task ausführen
        task_id = sys.argv[1]
        success = run_task(task_id)
        sys.exit(0 if success else 1)
    else:
        # Menü zeigen
        show_menu()
        print("\nVerwendung: python najika_work_manager.py <task-nummer>")
        print("Beispiel: python najika_work_manager.py 1")
