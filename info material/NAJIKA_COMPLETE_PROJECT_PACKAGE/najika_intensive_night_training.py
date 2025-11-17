#!/usr/bin/env python3
"""
NAJIKA INTENSIVE NIGHT TRAINING
8 Stunden volles GPU-Training (00:00 - 08:00)
Ziel: In 1 Monat auf Claude-Niveau
"""
import subprocess
import time
from datetime import datetime, timedelta
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).parent
LOG_FILE = BACKEND_DIR / "training_night_log.json"

class NightTrainingSession:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=8)
        self.completed_tasks = []
        self.errors = []

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def run_script(self, script_name, description, duration_minutes=30):
        """Führt Training-Script aus"""
        self.log(f"START: {description}", "TRAIN")
        start = time.time()

        try:
            result = subprocess.run(
                ["python", str(BACKEND_DIR / script_name)],
                capture_output=True,
                text=True,
                timeout=duration_minutes * 60,
                encoding='utf-8',
                errors='replace'
            )

            elapsed = (time.time() - start) / 60

            if result.returncode == 0:
                self.log(f"OK: {description} ({elapsed:.1f}min)", "SUCCESS")
                self.completed_tasks.append({
                    "script": script_name,
                    "description": description,
                    "duration_minutes": elapsed,
                    "status": "success",
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                self.log(f"FEHLER: {description}", "ERROR")
                self.log(f"Output: {result.stderr}", "ERROR")
                self.errors.append({
                    "script": script_name,
                    "error": result.stderr,
                    "timestamp": datetime.now().isoformat()
                })
                return False

        except subprocess.TimeoutExpired:
            self.log(f"TIMEOUT: {description} nach {duration_minutes}min", "WARN")
            return False
        except Exception as e:
            self.log(f"EXCEPTION: {description} - {e}", "ERROR")
            self.errors.append({
                "script": script_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False

    def intensive_training_cycle(self):
        """8-Stunden Trainings-Zyklus (kann bis 10h gehen mit Phase 5)"""

        self.log("="*80)
        self.log("NAJIKA INTENSIVE NIGHT TRAINING - START")
        self.log(f"Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Ende: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("="*80)

        # PHASE 1: LoRA Personality Training (2h)
        self.log("\n[PHASE 1/5] LoRA Personality Training (2h)")
        for i in range(4):  # 4x 30min Sessions
            self.run_script(
                "najika_lora_training_3b.py",
                f"LoRA Training Session {i+1}/4",
                duration_minutes=30
            )
            if datetime.now() >= self.end_time:
                break

        # PHASE 2: Code Training - Intensive (2h)
        self.log("\n[PHASE 2/5] Intensive Code Training (2h)")
        for i in range(8):  # 8x 15min Coding Katas
            self.run_script(
                "najika_code_training_real.py",
                f"Code Kata Session {i+1}/8",
                duration_minutes=15
            )
            if datetime.now() >= self.end_time:
                break

        # PHASE 3: Advanced Training - NEW MODULES! (2h)
        self.log("\n[PHASE 3/5] Advanced Training - NEW 2025 Research-Based! (2h)")
        advanced_scripts = [
            ("najika_advisor_training.py", "Advisor Training (Lebensberatung)", 30),
            ("najika_thought_organizer_training.py", "Thought Organization (Mind-Maps)", 30),
            ("najika_fact_checker_training.py", "Fact Checker (Error Detection)", 30),
            ("najika_emotional_intelligence_training.py", "Emotional Intelligence (RLHF)", 30)
        ]

        for script, desc, duration in advanced_scripts:
            self.run_script(script, desc, duration_minutes=duration)
            if datetime.now() >= self.end_time:
                break

        # PHASE 4: Memory & ChromaDB Enhancement (2h)
        self.log("\n[PHASE 4/5] Memory Enhancement (2h)")
        for i in range(4):
            self.run_script(
                "najika_chromadb_setup.py",
                f"ChromaDB Enhancement {i+1}/4",
                duration_minutes=30
            )
            if datetime.now() >= self.end_time:
                break

        # PHASE 5: Project Knowledge Training (2h) - NEW!
        self.log("\n[PHASE 5/5] Project Knowledge Training - 258M Zeichen! (2h)")
        self.log("Training auf Desktop Projekt-Daten (finale/finalee/zip)")
        for i in range(4):  # 4x 30min Sessions
            self.run_script(
                "najika_project_knowledge_training.py",
                f"Project Knowledge Session {i+1}/4",
                duration_minutes=30
            )
            if datetime.now() >= self.end_time:
                break

        # Finale Stats
        self.log("\n" + "="*80)
        self.log("TRAINING SESSION ABGESCHLOSSEN")
        self.log("="*80)

        total_duration = (datetime.now() - self.start_time).total_seconds() / 3600
        success_count = len(self.completed_tasks)
        error_count = len(self.errors)

        self.log(f"Gesamtdauer: {total_duration:.2f} Stunden")
        self.log(f"Erfolgreiche Tasks: {success_count}")
        self.log(f"Fehler: {error_count}")
        self.log(f"Erfolgsrate: {(success_count/(success_count+error_count)*100):.1f}%")

        # Speichere Log
        log_data = {
            "session_start": self.start_time.isoformat(),
            "session_end": datetime.now().isoformat(),
            "total_hours": total_duration,
            "completed_tasks": self.completed_tasks,
            "errors": self.errors,
            "stats": {
                "success": success_count,
                "errors": error_count,
                "success_rate": (success_count/(success_count+error_count)*100) if (success_count+error_count) > 0 else 0
            }
        }

        # Append to log file
        logs = []
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(log_data)

        # Keep only last 30 sessions
        logs = logs[-30:]

        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

        self.log(f"\nLog gespeichert: {LOG_FILE}")
        self.log("\n🎓 Najika hat heute Nacht HART gelernt! 💪")

if __name__ == "__main__":
    session = NightTrainingSession()
    session.intensive_training_cycle()
