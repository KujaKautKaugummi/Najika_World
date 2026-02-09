#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA THOUGHT ORGANIZER TRAINING
Trainiert Najika im Strukturieren chaotischer Gedanken

FEATURES:
- Wirre Gedanken → klare Struktur
- Mind-Mapping (textbasiert)
- Prioritäten setzen
- Action Items extrahieren
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
TRAINING_LOG = BACKEND_DIR / "thought_organizer_training_log.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "najika-local"

def log(msg):
    # Windows-safe: Emojis durch ASCII ersetzen
    safe_msg = str(msg).replace('\u2705', '[OK]').replace('\u2192', '->').replace('\u274c', '[X]')
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {safe_msg}")

class NajikaThoughtOrganizerTrainer:
    def __init__(self):
        self.session_start = datetime.now()
        self.stats = {
            "thoughts_organized": 0,
            "mindmaps_created": 0,
            "priorities_set": 0,
            "action_items_extracted": 0
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

    def train_chaos_to_structure(self):
        """Training: Chaotische Gedanken strukturieren"""
        log("\n[TRAINING 1/4] Chaos → Structure...")

        chaotic_thoughts = [
            """Ich muss noch Code schreiben und Tests fixen aber eigentlich sollte ich auch die Doku
            updaten und dann ist da noch das Meeting morgen für das ich mich vorbereiten sollte aber
            ich hab auch noch die Email von Chef nicht beantwortet und mein PC ist langsam geworden
            muss ich mal aufräumen und außerdem will ich heute noch trainieren aber bin müde...""",

            """Najika Projekt läuft aber Handy-App fehlt noch UEFN Spiel muss ich auch machen dann
            Voice Training für TTS vielleicht NVIDIA Jetson für Edge AI kaufen oder warten neue GPU
            kommt bald Security Features fehlen noch Kamera Mikro Scanner Cybersecurity Training...""",

            """Will neue GPU kaufen unter 1000€ aber welche RTX 4070 oder 4080 oder warten auf 5000er
            Serie wann kommt die wie viel VRAM brauche ich für Najika Training vielleicht Jetson Thor
            stattdessen für Edge AI oder beides Budget ist das Problem..."""
        ]

        for i, thought in enumerate(chaotic_thoughts, 1):
            log(f"  Chaos {i}/{len(chaotic_thoughts)}: {thought[:50]}...")

            prompt = f"""Du bist Najika, Gedanken-Organisatorin mit Explosions-Power!

CHAOTISCHE GEDANKEN:
{thought}

AUFGABE:
1. **Identifiziere THEMEN** (gruppiere ähnliche Gedanken)
2. **Strukturiere** in klare Kategorien
3. **Priorisiere** (Was ist WICHTIG vs. DRINGEND?)
4. **Erstelle Action Items** (konkrete Schritte)

FORMAT:
# THEMEN
- Thema 1: [Beschreibung]
- Thema 2: [Beschreibung]

# PRIORITÄTEN
[P1 - JETZT] Item...
[P2 - BALD] Item...
[P3 - SPÄTER] Item...

# ACTION ITEMS
☐ [ ] Konkrete Aufgabe 1
☐ [ ] Konkrete Aufgabe 2

DEINE STRUKTUR (explosiv klar!):"""

            response = self.call_ollama(prompt)
            if response and "THEMEN" in response and "PRIORITÄTEN" in response:
                self.stats["thoughts_organized"] += 1
                log(f"    ✅ Gedanken strukturiert: {len(response)} Zeichen")
            else:
                log(f"    ❌ Unvollständig")

        log(f"  [OK] Thoughts organized: {self.stats['thoughts_organized']}")

    def train_mindmap_creation(self):
        """Training: Mind-Maps erstellen (textbasiert)"""
        log("\n[TRAINING 2/4] Mind-Map Creation...")

        topics = [
            "Najika World - komplettes Projekt",
            "Meine Karriere - nächste 5 Jahre",
            "Gesundheit & Fitness Routine",
            "Neues Spiel-Konzept entwickeln"
        ]

        for i, topic in enumerate(topics, 1):
            log(f"  Topic {i}/{len(topics)}: {topic}")

            prompt = f"""Du bist Najika, Mind-Map Expertin!

THEMA: {topic}

AUFGABE:
Erstelle eine textbasierte MIND-MAP mit:
1. ZENTRUM (Hauptthema)
2. HAUPTZWEIGE (4-6 Kategorien)
3. UNTERZWEIGE (Details pro Kategorie)
4. VERBINDUNGEN (zeige Zusammenhänge!)

FORMAT (ASCII-Art Style):
```
                    [ZENTRUM]
                        |
        +---------------+---------------+
        |               |               |
    [ZWEIG 1]      [ZWEIG 2]       [ZWEIG 3]
        |               |               |
    - Detail        - Detail        - Detail
    - Detail        - Detail        - Detail

VERBINDUNGEN:
→ Zweig 1 beeinflusst Zweig 2 weil...
```

DEINE MIND-MAP:"""

            response = self.call_ollama(prompt, timeout=120)
            if response and "ZENTRUM" in response or "```" in response:
                self.stats["mindmaps_created"] += 1
                log(f"    ✅ Mind-Map erstellt")
            else:
                log(f"    ❌ Keine Mind-Map")

        log(f"  [OK] Mind-Maps created: {self.stats['mindmaps_created']}")

    def train_priority_matrix(self):
        """Training: Eisenhower-Matrix für Prioritäten"""
        log("\n[TRAINING 3/4] Priority Matrix (Eisenhower)...")

        task_lists = [
            [
                "Code-Fehler fixen (Produktion down!)",
                "Meeting vorbereiten (morgen)",
                "Doku schreiben",
                "Email beantworten",
                "Social Media checken",
                "Neue Features planen",
                "Lernen: neue Technologie",
                "Backup erstellen"
            ],
            [
                "Najika Training starten",
                "UEFN Spiel Deadline in 2 Tagen",
                "Grafikkarte recherchieren",
                "Kaffee trinken",
                "Code refactoring",
                "Neue Ideen sammeln",
                "Server-Update durchführen"
            ]
        ]

        for i, tasks in enumerate(task_lists, 1):
            log(f"  Task List {i}/{len(task_lists)}: {len(tasks)} Tasks")

            tasks_str = "\n".join([f"- {t}" for t in tasks])

            prompt = f"""Du bist Najika, Prioritäts-Managerin!

AUFGABEN-LISTE:
{tasks_str}

AUFGABE:
Sortiere in EISENHOWER-MATRIX:

```
        WICHTIG         |      NICHT WICHTIG
    ------------------- | -------------------
D   [DO IT NOW!]       | S  [SCHEDULE IT]
R   Dringend+Wichtig   | C  Wichtig, nicht dringend
I   Sofort tun!        | H  Planen für später
N                      | E
G                      | D
E   [DELEGATE]         | L  [DELETE IT]
N   Dringend, unwichtig| E  Unwichtig+nicht dringend
T   Delegieren/Schnell |    Löschen/Ignorieren
```

Ordne JEDE Aufgabe zu + erkläre WARUM!

DEINE MATRIX:"""

            response = self.call_ollama(prompt, timeout=120)
            if response and ("DO IT NOW" in response or "SCHEDULE" in response):
                self.stats["priorities_set"] += 1
                log(f"    ✅ Prioritäten gesetzt")
            else:
                log(f"    ❌ Keine Matrix")

        log(f"  [OK] Priorities set: {self.stats['priorities_set']}")

    def train_action_item_extraction(self):
        """Training: Konkrete Action Items aus Notizen extrahieren"""
        log("\n[TRAINING 4/4] Action Item Extraction...")

        notes = [
            """Meeting Notes: Projekt X
            - Team ist mit Progress zufrieden
            - Sprint Review nächste Woche
            - Bug in Login-Feature muss gefixt werden
            - Performance-Tests sollten wir auch mal machen
            - Client fragt nach neuer Funktion Y
            - Doku ist veraltet, wäre gut das zu updaten
            - Server manchmal langsam, sollten wir checken
            """,

            """Projekt-Brainstorm:
            Najika braucht noch Voice Calls, AR Mode wäre cool, Computer Vision für Kamera-Scanner,
            Cybersecurity Training fehlt, NVIDIA Jetson evaluieren, neue GPU kaufen (Budget?),
            Training intensiver machen, Memory System optimieren, Reddit Community aufbauen
            """
        ]

        for i, note in enumerate(notes, 1):
            log(f"  Note {i}/{len(notes)}: {note[:40]}...")

            prompt = f"""Du bist Najika, Action-Item-Extraktions-Queen!

NOTIZEN:
{note}

AUFGABE:
1. Extrahiere ALLE Action Items (konkrete Todos)
2. Formuliere als KLARE, UMSETZBARE Aufgaben
3. Schätze AUFWAND (🔥 = 1h, 🔥🔥 = 4h, 🔥🔥🔥 = 1 Tag+)
4. Setze DEADLINE (wenn möglich)

FORMAT:
☐ [AUFWAND] Aufgabe [DEADLINE]

Beispiel:
☐ [🔥] Bug in Login fixen [HEUTE]
☐ [🔥🔥🔥] Performance-Tests implementieren [NÄCHSTE WOCHE]

DEINE ACTION ITEMS:"""

            response = self.call_ollama(prompt)
            if response and "☐" in response or "[ ]" in response:
                self.stats["action_items_extracted"] += 1
                log(f"    ✅ Action Items extrahiert")
            else:
                log(f"    ❌ Keine Items")

        log(f"  [OK] Action Items extracted: {self.stats['action_items_extracted']}")

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
        log("NAJIKA THOUGHT ORGANIZER TRAINING")
        log("="*80)

        self.train_chaos_to_structure()
        self.train_mindmap_creation()
        self.train_priority_matrix()
        self.train_action_item_extraction()

        self.save_session_log()

        log("\n" + "="*80)
        log("TRAINING SESSION ABGESCHLOSSEN")
        log("="*80)
        log(f"Thoughts organized: {self.stats['thoughts_organized']}")
        log(f"Mind-Maps created: {self.stats['mindmaps_created']}")
        log(f"Priorities set: {self.stats['priorities_set']}")
        log(f"Action Items extracted: {self.stats['action_items_extracted']}")
        log("")

if __name__ == "__main__":
    trainer = NajikaThoughtOrganizerTrainer()
    trainer.run()
