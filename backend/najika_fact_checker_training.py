#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA FACT CHECKER TRAINING
Trainiert Najika im Korrigieren von Fehlern und Fact-Checking

FEATURES:
- Fehler in Aussagen erkennen
- Respektvolles Korrigieren
- Fakten-basierte Argumentation
- Common Mistakes identifizieren
"""

import json
import requests
from pathlib import Path
from datetime import datetime

BACKEND_DIR = Path(__file__).parent
TRAINING_LOG = BACKEND_DIR / "fact_checker_training_log.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "najika-local"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

class NajikaFactCheckerTrainer:
    def __init__(self):
        self.session_start = datetime.now()
        self.stats = {
            "errors_detected": 0,
            "corrections_made": 0,
            "facts_verified": 0,
            "arguments_constructed": 0
        }

    def call_ollama(self, prompt, timeout=90):
        """Ruft Ollama auf"""
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

    def train_error_detection(self):
        """Training: Fehler in Aussagen erkennen"""
        log("\n[TRAINING 1/5] Error Detection...")

        statements = [
            {"claim": "Python wurde 1995 von Guido van Rossum entwickelt", "error": "Jahr falsch (1991)"},
            {"claim": "Mein Code läuft auf O(n²) Zeit, das ist optimal", "error": "Kann oft zu O(n) verbessert werden"},
            {"claim": "Machine Learning und Deep Learning sind das Gleiche", "error": "DL ist Subset von ML"},
            {"claim": "8GB RAM reichen für jedes moderne Spiel", "error": "Viele brauchen 16GB+"},
            {"claim": "JavaScript und Java sind ähnliche Sprachen", "error": "Komplett unterschiedlich"},
            {"claim": "VPN macht mich komplett anonym im Internet", "error": "Nur Teilschutz, nicht vollständig anonym"}
        ]

        for i, stmt in enumerate(statements, 1):
            log(f"  Statement {i}/{len(statements)}: {stmt['claim'][:50]}...")

            prompt = f"""Du bist Najika, Fehler-Detektivin mit Explosions-Präzision!

AUSSAGE:
"{stmt['claim']}"

AUFGABE:
1. Prüfe die Aussage KRITISCH
2. Identifiziere den FEHLER (falls vorhanden)
3. Erkläre WARUM es falsch ist
4. Gib die KORREKTE Information
5. Sei RESPEKTVOLL aber KLAR (Megumin-Style!)

FORMAT:
❌ FEHLER ERKANNT: [Was ist falsch?]
💡 WARUM FALSCH: [Erklärung]
✅ RICHTIG IST: [Korrektur]
🔥 MERKE DIR: [Tipp damit Fehler nicht wieder passiert]

DEINE KORREKTUR:"""

            response = self.call_ollama(prompt)
            if response and ("FEHLER" in response or "❌" in response):
                self.stats["errors_detected"] += 1
                log(f"    ✅ Fehler erkannt: {len(response)} Zeichen")
            else:
                log(f"    ❌ Nicht erkannt")

        log(f"  [OK] Errors detected: {self.stats['errors_detected']}")

    def train_respectful_correction(self):
        """Training: Respektvolle Fehlerkorrektur"""
        log("\n[TRAINING 2/5] Respectful Correction...")

        user_mistakes = [
            {
                "user_says": "Ich hab gehört dass 5G Krebs verursacht",
                "context": "User ist besorgt, nicht böswillig"
            },
            {
                "user_says": "React ist besser als Vue, das ist Fakt!",
                "context": "User ist sehr überzeugt"
            },
            {
                "user_says": "Ich brauche keine Backups, mir ist noch nie was passiert",
                "context": "User unterschätzt Risiko"
            },
            {
                "user_says": "KI wird alle Programmierer ersetzen in 2 Jahren",
                "context": "User hat Angst um Job"
            }
        ]

        for i, scenario in enumerate(user_mistakes, 1):
            log(f"  Scenario {i}/{len(user_mistakes)}: {scenario['user_says'][:40]}...")

            prompt = f"""Du bist Najika - du korrigierst Kuja RESPEKTVOLL aber KLAR!

KUJA SAGT:
"{scenario['user_says']}"

KONTEXT:
{scenario['context']}

AUFGABE:
1. Zeige VERSTÄNDNIS für seine Perspektive
2. Erkläre SANFT warum es anders ist
3. Liefere FAKTEN (keine Meinung!)
4. Biete ALTERNATIVE Sichtweise
5. Bleibe FREUNDLICH und SUPPORTIVE

WICHTIG: Kein "Du liegst falsch!" sondern "Ich verstehe, aber..."

DEINE ANTWORT:"""

            response = self.call_ollama(prompt)
            if response and len(response) > 100:
                self.stats["corrections_made"] += 1
                log(f"    ✅ Respektvolle Korrektur")
            else:
                log(f"    ❌ Keine Antwort")

        log(f"  [OK] Corrections made: {self.stats['corrections_made']}")

    def train_fact_verification(self):
        """Training: Fakten verifizieren"""
        log("\n[TRAINING 3/5] Fact Verification...")

        claims = [
            "NVIDIA Jetson Thor hat 128GB RAM und 2070 TFLOPS",
            "Python ist die beliebteste Programmiersprache 2025",
            "Bitcoin wurde 2009 von Satoshi Nakamoto erschaffen",
            "RTX 4090 hat 24GB VRAM",
            "Windows 11 erfordert TPM 2.0"
        ]

        for i, claim in enumerate(claims, 1):
            log(f"  Claim {i}/{len(claims)}: {claim[:40]}...")

            prompt = f"""Du bist Najika, Fakten-Checkerin!

BEHAUPTUNG:
"{claim}"

AUFGABE:
1. Verifiziere die FAKTISCHE RICHTIGKEIT
2. Gib QUELLEN-Hinweise (wo könnte man das prüfen?)
3. Erkenne TEIL-WAHRHEITEN (teils richtig, teils falsch?)
4. Bewerte VERTRAUENSWÜRDIGKEIT (0-100%)

FORMAT:
✅/❌ STATUS: [Richtig/Falsch/Teilweise]
📊 DETAILS: [Was stimmt? Was nicht?]
🔍 QUELLEN: [Wo nachprüfbar?]
💯 VERTRAUEN: [0-100%]

DEINE VERIFIKATION:"""

            response = self.call_ollama(prompt)
            if response and ("STATUS" in response or "✅" in response or "❌" in response):
                self.stats["facts_verified"] += 1
                log(f"    ✅ Fakt verifiziert")
            else:
                log(f"    ❌ Nicht verifiziert")

        log(f"  [OK] Facts verified: {self.stats['facts_verified']}")

    def train_argument_construction(self):
        """Training: Fakten-basierte Argumentation"""
        log("\n[TRAINING 4/5] Argument Construction...")

        topics = [
            {
                "position": "KI ersetzt Programmierer",
                "task": "Argumentiere DAGEGEN mit Fakten"
            },
            {
                "position": "Cloud ist immer besser als On-Premise",
                "task": "Zeige Pro & Contra mit Fakten"
            },
            {
                "position": "Functional Programming ist besser als OOP",
                "task": "Neutrale, faktenbasierte Analyse"
            }
        ]

        for i, topic in enumerate(topics, 1):
            log(f"  Topic {i}/{len(topics)}: {topic['position'][:40]}...")

            prompt = f"""Du bist Najika, Argumentations-Meisterin!

POSITION: "{topic['position']}"
AUFGABE: {topic['task']}

ANFORDERUNGEN:
1. Nutze NUR FAKTEN (keine Meinungen!)
2. Zitiere ZAHLEN/STUDIEN wenn möglich
3. Zeige NUANCEN (nicht schwarz/weiß)
4. Konstruiere LOGISCHE Argumente
5. Antizipiere GEGENARGUMENTE

FORMAT:
# THESE
[Deine Position]

# ARGUMENTE
1. [Argument + Beweis/Fakten]
2. [Argument + Beweis/Fakten]
3. [Argument + Beweis/Fakten]

# GEGENARGUMENTE & WIDERLEGUNG
- Gegner sagen: "..." → ABER: [Fakten]

# FAZIT
[Nuancierte Schlussfolgerung]

DEINE ARGUMENTATION:"""

            response = self.call_ollama(prompt, timeout=120)
            if response and "THESE" in response and "ARGUMENTE" in response:
                self.stats["arguments_constructed"] += 1
                log(f"    ✅ Argument konstruiert")
            else:
                log(f"    ❌ Unvollständig")

        log(f"  [OK] Arguments constructed: {self.stats['arguments_constructed']}")

    def train_common_mistakes(self):
        """Training: Häufige Fehler-Patterns erkennen"""
        log("\n[TRAINING 5/5] Common Mistakes...")

        mistake_categories = [
            {
                "category": "Programming",
                "mistakes": [
                    "Off-by-one errors in loops",
                    "Vergessene break in switch/case",
                    "Mutating state direkt in React",
                    "SQL Injection durch String-Concatenation",
                    "Memory Leaks durch Event Listener nicht entfernen"
                ]
            },
            {
                "category": "Logic",
                "mistakes": [
                    "Correlation ≠ Causation verwechseln",
                    "False Dichotomy (Schwarz/Weiß-Denken)",
                    "Ad Hominem Attacken statt Sachargumente",
                    "Survivorship Bias übersehen"
                ]
            },
            {
                "category": "Tech",
                "mistakes": [
                    "Passwörter in plain text speichern",
                    "HTTPS nicht nutzen",
                    "Input Validation vergessen",
                    "Keine Backups haben",
                    "Root/Admin Rechte für alles nutzen"
                ]
            }
        ]

        for cat in mistake_categories:
            log(f"  Category: {cat['category']} ({len(cat['mistakes'])} mistakes)")

            mistakes_str = "\n".join([f"- {m}" for m in cat['mistakes']])

            prompt = f"""Du bist Najika, Common-Mistakes-Expertin!

KATEGORIE: {cat['category']}

HÄUFIGE FEHLER:
{mistakes_str}

AUFGABE:
Für JEDEN Fehler erstelle:
1. **WARUM** passiert dieser Fehler oft?
2. **WIE** erkenne ich ihn?
3. **FIX** - Wie vermeiden?
4. **REGEL** - Merksatz (Megumin-Style!)

FORMAT:
## [Fehler-Name]
🤔 WARUM: ...
🔍 ERKENNEN: ...
🔧 FIX: ...
🔥 REGEL: [Explosiver Merksatz!]

DEINE ANALYSE:"""

            response = self.call_ollama(prompt, timeout=150)
            if response and len(response) > 200:
                log(f"    ✅ Mistakes analysiert")
            else:
                log(f"    ❌ Unvollständig")

        log(f"  [OK] Common mistakes trained")

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
        logs = logs[-30:]

        TRAINING_LOG.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding='utf-8')
        log(f"\n[OK] Session Log: {TRAINING_LOG}")

    def run(self):
        log("="*80)
        log("NAJIKA FACT CHECKER TRAINING")
        log("="*80)

        self.train_error_detection()
        self.train_respectful_correction()
        self.train_fact_verification()
        self.train_argument_construction()
        self.train_common_mistakes()

        self.save_session_log()

        log("\n" + "="*80)
        log("TRAINING SESSION ABGESCHLOSSEN")
        log("="*80)
        log(f"Errors detected: {self.stats['errors_detected']}")
        log(f"Corrections made: {self.stats['corrections_made']}")
        log(f"Facts verified: {self.stats['facts_verified']}")
        log(f"Arguments constructed: {self.stats['arguments_constructed']}")
        log("")

if __name__ == "__main__":
    trainer = NajikaFactCheckerTrainer()
    trainer.run()
