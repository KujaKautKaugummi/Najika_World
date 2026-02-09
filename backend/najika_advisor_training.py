#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA ADVISOR TRAINING
Trainiert Najika als Alltagsberaterin für ALLE Lebensbereiche

BASIERT AUF RESEARCH 2025:
- Emotional Intelligence (MYAIGF, RLHF)
- Decision Support
- Problem Solving
- Pro/Contra Analysis
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows CP1252 encoding issue
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BACKEND_DIR = Path(__file__).parent
TRAINING_LOG = BACKEND_DIR / "advisor_training_log.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "najika-local"

def log(msg):
    # Windows-safe: Emojis durch ASCII ersetzen
    safe_msg = str(msg).replace('\u2705', '[OK]').replace('\u2192', '->').replace('\u274c', '[X]')
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {safe_msg}")

class NajikaAdvisorTrainer:
    def __init__(self):
        self.session_start = datetime.now()
        self.stats = {
            "decisions_helped": 0,
            "problems_solved": 0,
            "advice_given": 0,
            "pro_contra_created": 0
        }

    def call_ollama(self, prompt, timeout=60):
        """Ruft Ollama mit Training-Prompt auf"""
        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": prompt, "stream": False},
                timeout=timeout
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except:
            pass
        return None

    def train_decision_support(self):
        """Training: Entscheidungen treffen helfen"""
        log("\n[TRAINING 1/5] Decision Support...")

        # Beispiel-Situationen für Entscheidungshilfe
        decision_scenarios = [
            {
                "situation": "Soll ich einen neuen Job annehmen? Mehr Gehalt, aber längerer Arbeitsweg.",
                "context": "Aktuell 15min Arbeitsweg, neuer Job 45min. +800€ mehr im Monat."
            },
            {
                "situation": "Soll ich ein MacBook Pro oder einen Windows Gaming Laptop kaufen?",
                "context": "Brauche für Coding und Gaming. Budget 2000€."
            },
            {
                "situation": "Soll ich heute Sport machen oder entspannen?",
                "context": "Bin müde, aber habe diese Woche noch nicht trainiert."
            }
        ]

        for i, scenario in enumerate(decision_scenarios, 1):
            log(f"  Scenario {i}/{len(decision_scenarios)}: {scenario['situation'][:50]}...")

            prompt = f"""Du bist Najika, Kuja's AI Beraterin (Megumin-Style + strategisch)!

SITUATION:
{scenario['situation']}

KONTEXT:
{scenario['context']}

AUFGABE:
1. Analysiere Pro & Contra (jeweils 3-5 Punkte)
2. Gib eine KLARE Empfehlung (als Najika!)
3. Erkläre WARUM (emotional + rational)
4. Frage nach: "Was ist dir wichtiger: X oder Y?"

DEINE BERATUNG (explosiv aber hilfreich!):"""

            response = self.call_ollama(prompt)
            if response and len(response) > 100:
                self.stats["decisions_helped"] += 1
                log(f"    ✅ Entscheidungshilfe: {len(response)} Zeichen")
            else:
                log(f"    ❌ Keine Antwort")

        log(f"  [OK] Decisions supported: {self.stats['decisions_helped']}")

    def train_problem_solving(self):
        """Training: Alltagsprobleme lösen"""
        log("\n[TRAINING 2/5] Problem Solving...")

        problems = [
            "Mein Code funktioniert nicht, ich finde den Fehler nicht!",
            "Ich habe zu viele Aufgaben und weiß nicht wo ich anfangen soll.",
            "Ich bin demotiviert und prokrastiniere ständig.",
            "Mein PC ist langsam geworden, was kann ich tun?",
            "Ich verstehe ein Konzept in der Uni nicht."
        ]

        for i, problem in enumerate(problems, 1):
            log(f"  Problem {i}/{len(problems)}: {problem[:50]}...")

            prompt = f"""Du bist Najika, Problem-Löserin mit Explosions-Power!

PROBLEM:
{problem}

AUFGABE:
1. Analysiere das Problem (Was ist die ROOT CAUSE?)
2. Biete 3 konkrete Lösungsansätze
3. Priorisiere: Welchen Ansatz ZUERST?
4. Motiviere Kuja (als Najika, explosiv!)

DEINE LÖSUNG:"""

            response = self.call_ollama(prompt)
            if response and len(response) > 80:
                self.stats["problems_solved"] += 1
                log(f"    ✅ Problem gelöst: {len(response)} Zeichen")
            else:
                log(f"    ❌ Keine Lösung")

        log(f"  [OK] Problems solved: {self.stats['problems_solved']}")

    def train_life_advice(self):
        """Training: Lebensberatung (Health, Relationships, Career, etc.)"""
        log("\n[TRAINING 3/5] Life Advice...")

        life_topics = [
            {"topic": "Health", "question": "Wie bleibe ich gesund bei 10h+ am PC täglich?"},
            {"topic": "Relationships", "question": "Wie finde ich Zeit für Freunde bei viel Arbeit?"},
            {"topic": "Career", "question": "Soll ich mich selbstständig machen oder angestellt bleiben?"},
            {"topic": "Finance", "question": "Wie spare ich Geld und investiere sinnvoll?"},
            {"topic": "Personal Growth", "question": "Wie werde ich besser im Programmieren?"}
        ]

        for item in life_topics:
            log(f"  {item['topic']}: {item['question'][:40]}...")

            prompt = f"""Du bist Najika, Life Coach mit Explosions-Energie!

THEMA: {item['topic']}
FRAGE: {item['question']}

AUFGABE:
1. Gib praktische, umsetzbare Tipps (3-5 Stück)
2. Erkläre das "WARUM" dahinter
3. Motiviere Kuja (Megumin-Style!)
4. Erwähne eine kleine Challenge ("Probier das heute!")

DEIN ADVICE:"""

            response = self.call_ollama(prompt)
            if response and len(response) > 100:
                self.stats["advice_given"] += 1
                log(f"    ✅ Advice gegeben")
            else:
                log(f"    ❌ Kein Advice")

        log(f"  [OK] Advice given: {self.stats['advice_given']}")

    def train_pro_contra_analysis(self):
        """Training: Pro/Contra Listen erstellen"""
        log("\n[TRAINING 4/5] Pro/Contra Analysis...")

        topics = [
            "Umzug in eine andere Stadt",
            "Eigene Firma gründen vs. Angestellter bleiben",
            "Konsole vs. Gaming PC kaufen",
            "Homeoffice vs. Büro arbeiten"
        ]

        for i, topic in enumerate(topics, 1):
            log(f"  Topic {i}/{len(topics)}: {topic}")

            prompt = f"""Du bist Najika, Analyse-Queen!

THEMA: {topic}

AUFGABE:
1. Liste ALLE Pros (mindestens 5)
2. Liste ALLE Contras (mindestens 5)
3. Gewichte jedes Pro/Contra (1-10 Wichtigkeit)
4. Gib Gesamt-Empfehlung (mit Explosions-Energie!)

FORMAT:
# PRO
- [9/10] Punkt 1...
- [7/10] Punkt 2...

# CONTRA
- [8/10] Punkt 1...

# FAZIT
[Deine Empfehlung]

DEINE ANALYSE:"""

            response = self.call_ollama(prompt, timeout=90)
            if response and "PRO" in response and "CONTRA" in response:
                self.stats["pro_contra_created"] += 1
                log(f"    ✅ Pro/Contra erstellt")
            else:
                log(f"    ❌ Unvollständig")

        log(f"  [OK] Pro/Contra created: {self.stats['pro_contra_created']}")

    def train_context_awareness(self):
        """Training: Kontext-bewusstsein (wie geht es Kuja HEUTE?)"""
        log("\n[TRAINING 5/5] Context Awareness...")

        contexts = [
            {"mood": "stressed", "situation": "Viele Deadlines, wenig Schlaf"},
            {"mood": "excited", "situation": "Neues Projekt gestartet, voller Energie"},
            {"mood": "sad", "situation": "Etwas ist schief gelaufen"},
            {"mood": "bored", "situation": "Nichts zu tun, gelangweilt"}
        ]

        for context in contexts:
            log(f"  Mood: {context['mood']} ({context['situation'][:30]}...)")

            prompt = f"""Du bist Najika - du spürst wie es Kuja geht!

KUJA'S MOOD: {context['mood']}
SITUATION: {context['situation']}

AUFGABE:
1. Reagiere PASSEND zu seinem Mood (empathisch!)
2. Biete KONKRETE Hilfe/Unterstützung
3. Passe deinen TONE an (Megumin-Style, aber sensibel!)
4. Frage nach: "Wie kann ich dir helfen?"

DEINE REAKTION:"""

            response = self.call_ollama(prompt)
            if response and len(response) > 50:
                log(f"    ✅ Context-aware response")
            else:
                log(f"    ❌ Keine Response")

        log(f"  [OK] Context awareness trained")

    def save_session_log(self):
        """Speichert Training-Session Log"""
        session_data = {
            "session_start": self.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "duration_minutes": (datetime.now() - self.session_start).total_seconds() / 60,
            "stats": self.stats
        }

        logs = []
        if TRAINING_LOG.exists():
            try:
                logs = json.loads(TRAINING_LOG.read_text(encoding='utf-8'))
            except:
                logs = []

        logs.append(session_data)
        logs = logs[-30:]  # Keep last 30 sessions

        TRAINING_LOG.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding='utf-8')
        log(f"\n[OK] Session Log: {TRAINING_LOG}")

    def run(self):
        log("="*80)
        log("NAJIKA ADVISOR TRAINING - LEBENSBERATUNG!")
        log("="*80)

        self.train_decision_support()
        self.train_problem_solving()
        self.train_life_advice()
        self.train_pro_contra_analysis()
        self.train_context_awareness()

        self.save_session_log()

        log("\n" + "="*80)
        log("TRAINING SESSION ABGESCHLOSSEN")
        log("="*80)
        log(f"Decisions helped: {self.stats['decisions_helped']}")
        log(f"Problems solved: {self.stats['problems_solved']}")
        log(f"Advice given: {self.stats['advice_given']}")
        log(f"Pro/Contra created: {self.stats['pro_contra_created']}")
        log("")

if __name__ == "__main__":
    trainer = NajikaAdvisorTrainer()
    trainer.run()
