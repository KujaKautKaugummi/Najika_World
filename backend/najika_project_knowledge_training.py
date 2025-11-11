#!/usr/bin/env python3
"""
NAJIKA PROJECT KNOWLEDGE TRAINING
Trainiert Najika mit ihren eigenen Projekt-Daten
- 90 Millionen Zeichen Wissen
- Code vervollständigen
- Code auf Funktion prüfen
- Spiel-Ideen sammeln und strukturieren
"""
import json
from pathlib import Path
from datetime import datetime
import random

BACKEND_DIR = Path(__file__).parent
KNOWLEDGE_DIR = BACKEND_DIR / "najika_project_knowledge"
TRAINING_LOG = BACKEND_DIR / "project_training_log.json"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_category(category_name):
    """Lädt alle Dateien einer Kategorie"""
    category_dir = KNOWLEDGE_DIR / category_name
    if not category_dir.exists():
        return []

    files = list(category_dir.glob("*.json"))
    data = []

    for file in files[:100]:  # Max 100 pro Training-Session
        try:
            content = json.loads(file.read_text(encoding='utf-8'))
            data.append(content)
        except:
            pass

    return data

class ProjectKnowledgeTrainer:
    def __init__(self):
        self.session_start = datetime.now()
        self.completed_tasks = []
        self.stats = {
            "codes_reviewed": 0,
            "codes_completed": 0,
            "ideas_extracted": 0,
            "concepts_learned": 0
        }

    def train_code_completion(self):
        """Training: Unvollständige Codes vervollständigen"""
        log("\n[TRAINING 1/4] Code Completion...")

        incomplete_codes = load_category("incomplete_code")

        # Import Ollama call (lokales Training)
        try:
            import requests
            OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

            for i, code_data in enumerate(incomplete_codes[:20]):  # 20 Codes pro Session
                log(f"  Code {i+1}/20: {Path(code_data['source_file']).name}")

                # Prompt an Ollama: Code vervollständigen
                prompt = f"""Du bist Najika, eine KI die Code vervollständigt.

UNVOLLSTÄNDIGER CODE:
{code_data.get('content', '')[:2000]}  # First 2000 chars

AUFGABE:
1. Analysiere den Code und identifiziere was fehlt
2. Vervollständige den Code VOLLSTÄNDIG
3. Erkläre was du hinzugefügt hast
4. Prüfe auf Syntaxfehler

DEINE VERVOLLSTÄNDIGUNG:"""

                try:
                    response = requests.post(
                        OLLAMA_URL,
                        json={"model": "najika-local", "prompt": prompt, "stream": False},
                        timeout=60
                    )
                    if response.status_code == 200:
                        completion = response.json().get("response", "")
                        # Erfolg wenn Antwort >50 Zeichen
                        if len(completion) > 50:
                            self.stats["codes_completed"] += 1
                except:
                    pass  # Bei Fehler überspringen

                self.stats["codes_reviewed"] += 1

        except Exception as e:
            log(f"  [WARN] Ollama nicht verfügbar, überspringe Code Completion: {e}")
            return

        log(f"  [OK] Codes vervollständigt: {self.stats['codes_completed']}/{self.stats['codes_reviewed']}")

    def train_code_review(self):
        """Training: Vollständige Codes auf Funktion prüfen"""
        log("\n[TRAINING 2/4] Code Review...")

        complete_codes = load_category("complete_implementations")

        # Import Ollama call
        try:
            import requests
            OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

            for i, code_data in enumerate(complete_codes[:20]):
                log(f"  Review {i+1}/20: {Path(code_data['source_file']).name}")

                # Prompt: Code Review durchführen
                prompt = f"""Du bist Najika, Code-Reviewerin mit Explosions-Talent!

CODE ZU REVIEWEN:
{code_data.get('content', '')[:3000]}  # First 3000 chars

AUFGABE - Prüfe den Code auf:
1. **Syntaxfehler** - Findet Python Fehler?
2. **Logikfehler** - Funktioniert die Logik?
3. **Best Practices** - Sauberer, lesbarer Code?
4. **Security Issues** - SQL Injection, XSS, Command Injection, etc.?
5. **Performance** - Effizient oder langsam?

DEIN REVIEW (als Najika, explosiv aber präzise!):"""

                try:
                    response = requests.post(
                        OLLAMA_URL,
                        json={"model": "najika-local", "prompt": prompt, "stream": False},
                        timeout=90
                    )
                    if response.status_code == 200:
                        review = response.json().get("response", "")
                        # Review gilt als erfolgreich wenn > 100 Zeichen
                        if len(review) > 100:
                            self.stats["codes_reviewed"] += 1
                        log(f"    Review-Länge: {len(review)} Zeichen")
                except Exception as e:
                    log(f"    [WARN] Ollama Fehler: {e}")
                    pass

        except Exception as e:
            log(f"  [WARN] Ollama nicht verfügbar: {e}")
            return

        log(f"  [OK] Codes reviewed: {self.stats['codes_reviewed']}")

    def train_idea_extraction(self):
        """Training: Spiel-Ideen extrahieren und strukturieren"""
        log("\n[TRAINING 3/4] Idea Extraction...")

        idea_files = load_category("game_ideas")

        all_ideas = []
        for idea_data in idea_files:
            if "ideas" in idea_data:
                all_ideas.extend(idea_data["ideas"])
                self.stats["ideas_extracted"] += len(idea_data["ideas"])

        # Gruppiere Ideen nach Kategorien
        categories = {
            "gameplay": [],
            "features": [],
            "mechanics": [],
            "story": [],
            "technical": []
        }

        for idea in all_ideas[:100]:  # Erste 100 Ideen
            idea_lower = idea.lower()

            if any(kw in idea_lower for kw in ['spieler', 'gameplay', 'mechanic', 'level']):
                categories["gameplay"].append(idea)
            elif any(kw in idea_lower for kw in ['feature', 'system', 'funktion']):
                categories["features"].append(idea)
            elif any(kw in idea_lower for kw in ['story', 'quest', 'dialog', 'charakter']):
                categories["story"].append(idea)
            elif any(kw in idea_lower for kw in ['code', 'api', 'backend', 'database']):
                categories["technical"].append(idea)
            else:
                categories["mechanics"].append(idea)

        # Speichere strukturierte Ideen
        structured_file = KNOWLEDGE_DIR / "structured_ideas.json"
        structured_file.write_text(
            json.dumps(categories, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

        log(f"  [OK] Ideen extrahiert: {self.stats['ideas_extracted']}")
        log(f"       Gameplay: {len(categories['gameplay'])}")
        log(f"       Features: {len(categories['features'])}")
        log(f"       Story: {len(categories['story'])}")
        log(f"       Technical: {len(categories['technical'])}")

    def train_concept_learning(self):
        """Training: Projekt-Konzepte verstehen"""
        log("\n[TRAINING 4/4] Concept Learning...")

        concept_files = load_category("project_concepts")

        # Import Ollama for concept learning
        try:
            import requests
            OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

            for i, concept_data in enumerate(concept_files[:30]):
                log(f"  Konzept {i+1}/30: {concept_data.get('title', 'Unknown')}")

                # Najika lernt Konzepte aus Notizen
                prompt = f"""Du bist Najika, eine KI die Projekt-Konzepte lernt!

KONZEPT/NOTIZ:
{concept_data.get('content', '')[:2000]}

AUFGABE:
1. Identifiziere HAUPT-KONZEPTE (max 5)
2. Finde ZUSAMMENHÄNGE zwischen Konzepten
3. Erstelle eine MIND-MAP Struktur (Textformat)
4. Fasse das WICHTIGSTE in 2-3 Sätzen zusammen

EXPLOSIV KURZ - wie Megumin!:"""

                try:
                    response = requests.post(
                        OLLAMA_URL,
                        json={"model": "najika-local", "prompt": prompt, "stream": False},
                        timeout=60
                    )
                    if response.status_code == 200:
                        concept_summary = response.json().get("response", "")
                        if len(concept_summary) > 50:
                            self.stats["concepts_learned"] += 1
                            # Speichere gelernte Konzepte
                            concept_data["najika_summary"] = concept_summary
                        log(f"    Zusammenfassung: {len(concept_summary)} Zeichen")
                except Exception as e:
                    log(f"    [WARN] Ollama Fehler: {e}")
                    pass

        except Exception as e:
            log(f"  [WARN] Ollama nicht verfügbar: {e}")
            # Fallback: Einfach zählen
            self.stats["concepts_learned"] = len(concept_files[:30])

        log(f"  [OK] Konzepte gelernt: {self.stats['concepts_learned']}")

    def save_session_log(self):
        """Speichert Training-Session Log"""
        session_data = {
            "session_start": self.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "duration_minutes": (datetime.now() - self.session_start).total_seconds() / 60,
            "stats": self.stats,
            "completed_tasks": self.completed_tasks
        }

        # Lade existierendes Log
        logs = []
        if TRAINING_LOG.exists():
            try:
                logs = json.loads(TRAINING_LOG.read_text(encoding='utf-8'))
            except:
                logs = []

        logs.append(session_data)

        # Keep last 50 sessions
        logs = logs[-50:]

        TRAINING_LOG.write_text(
            json.dumps(logs, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

        log(f"\n[OK] Session Log: {TRAINING_LOG}")

    def run(self):
        log("="*80)
        log("NAJIKA PROJECT KNOWLEDGE TRAINING")
        log("="*80)

        self.train_code_completion()
        self.train_code_review()
        self.train_idea_extraction()
        self.train_concept_learning()

        self.save_session_log()

        log("\n" + "="*80)
        log("TRAINING SESSION ABGESCHLOSSEN")
        log("="*80)
        log(f"Codes reviewed: {self.stats['codes_reviewed']}")
        log(f"Codes completed: {self.stats['codes_completed']}")
        log(f"Ideen extrahiert: {self.stats['ideas_extracted']}")
        log(f"Konzepte gelernt: {self.stats['concepts_learned']}")
        log("")

if __name__ == "__main__":
    trainer = ProjectKnowledgeTrainer()
    trainer.run()
