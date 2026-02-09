#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 NAJIKA COMPLETE NIGHT TRAINING 🌙

Vollständiges nächtliches Training:
1. Persönlichkeits-Training
2. Code-Training
3. Summary Reading (2x alle Zusammenfassungen)
4. Project Knowledge
"""

import sys
import io
import subprocess
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BACKEND_DIR = Path(__file__).parent

def log(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")

def run_training_script(script_name: str) -> bool:
    """Führt ein Training-Script aus"""
    log(f"🚀 Starte: {script_name}")
    log("="*70)

    try:
        script_path = BACKEND_DIR / script_name
        result = subprocess.run(
            ["python", str(script_path)],
            cwd=str(BACKEND_DIR),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=7200  # 2 Stunden max
        )

        if result.returncode == 0:
            log(f"✅ {script_name} erfolgreich!")
            return True
        else:
            log(f"❌ {script_name} fehlgeschlagen!")
            log(f"   Error: {result.stderr[:200]}")
            return False

    except subprocess.TimeoutExpired:
        log(f"⏱️ {script_name} Timeout (2h)")
        return False
    except Exception as e:
        log(f"❌ {script_name} Error: {e}")
        return False

def main():
    log("="*70)
    log("🌙 NAJIKA COMPLETE NIGHT TRAINING 🌙")
    log("="*70)
    log("")

    scripts = [
        ("najika_emotional_intelligence_training.py", "Emotionale Intelligenz"),
        ("najika_fact_checker_training.py", "Fakten-Check"),
        ("najika_thought_organizer_training.py", "Gedanken-Organisation"),
        ("najika_advisor_training.py", "Advisor Skills"),
        ("najika_code_training_real.py", "Code Training"),
        ("najika_summary_reading_training.py", "Summary Reading (2x)"),
        ("najika_project_knowledge_training.py", "Project Knowledge"),
    ]

    results = []
    start_time = datetime.now()

    for script, description in scripts:
        log("")
        log(f"📋 {description}")
        success = run_training_script(script)
        results.append((description, success))
        log("")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60

    # Finale Stats
    log("="*70)
    log("🎉 NIGHT TRAINING ABGESCHLOSSEN!")
    log("="*70)
    log(f"⏱️  Dauer: {duration:.1f} Minuten")
    log("")
    log("📊 Ergebnisse:")

    success_count = sum(1 for _, s in results if s)
    for desc, success in results:
        status = "✅" if success else "❌"
        log(f"   {status} {desc}")

    log("")
    log(f"✅ Erfolg: {success_count}/{len(results)}")
    log("="*70)


if __name__ == "__main__":
    main()
