#!/usr/bin/env python3
"""
NAJIKA SMART UPDATE SYSTEM
Token-effizient + Kontext-aware + Erzwingt Lesen
"""

import json
import re
from pathlib import Path
from datetime import datetime

NAJIKA_DIR = Path("C:/NajikaCore")
CLAUDE_PROJECTS = Path("C:/Users/0KKK0/.claude/projects/C--NajikaCore")
UPDATE_FILE = NAJIKA_DIR / "CLAUDE_SMART_UPDATE.md"

class SmartUpdate:
    def __init__(self):
        self.current_session = None
        self.previous_session = None
        self.open_tasks = []
        self.context_snippets = []

    def find_sessions(self):
        """Findet aktuelle und vorherige Session"""
        sessions = sorted(CLAUDE_PROJECTS.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)

        if len(sessions) >= 2:
            self.current_session = sessions[0]
            self.previous_session = sessions[1]
            print(f"[OK] Aktuelle Session: {self.current_session.name[:8]}...")
            print(f"[OK] Vorherige Session: {self.previous_session.name[:8]}...")
            return True
        else:
            print("[WARNING] Nicht genug Sessions gefunden")
            return False

    def extract_user_messages(self, session_file, max_messages=10):
        """Extrahiert letzte User-Nachrichten TOKEN-EFFIZIENT"""
        user_messages = []

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line)

                        # Nur User-Messages
                        if entry.get('type') == 'user':
                            msg = entry.get('message', {})
                            content = msg.get('content', [])

                            # Text extrahieren
                            text_parts = []
                            for item in content:
                                if isinstance(item, dict) and item.get('type') == 'text':
                                    text_parts.append(item.get('text', ''))

                            if text_parts:
                                full_text = ' '.join(text_parts)
                                # Nur KURZE Zusammenfassung (erste 200 chars)
                                summary = full_text[:200] + ('...' if len(full_text) > 200 else '')
                                user_messages.append({
                                    'timestamp': entry.get('timestamp', ''),
                                    'text': full_text,
                                    'summary': summary
                                })
                    except:
                        continue

            # Nur die letzten N Messages
            return user_messages[-max_messages:]

        except Exception as e:
            print(f"[ERROR] Konnte Session nicht lesen: {e}")
            return []

    def detect_open_tasks(self, messages):
        """Erkennt offene Aufgaben in User-Messages"""
        task_keywords = [
            r"mach\w*\s+(mal|bitte|das)",
            r"(änder|fix|korrigier|optimier)\w*",
            r"(soll|muss|brauch)\w*\s+(noch|jetzt)",
            r"(w-taste|ui|button|icon|kaugummi)",
            r"(terminal|raum|chat|aktionen)",
            r"dann\s+\w+\s+(ich|wir|du)",
            r"wichtig",
            r"top\s+prio"
        ]

        tasks = []
        for msg in messages:
            text = msg['text'].lower()

            # Prüfe Keywords
            for pattern in task_keywords:
                if re.search(pattern, text, re.IGNORECASE):
                    # Extrahiere relevanten Satz
                    sentences = text.split('.')
                    for sentence in sentences:
                        if re.search(pattern, sentence, re.IGNORECASE):
                            tasks.append(sentence.strip())
                            break
                    break

        # Dedupliziere
        return list(set(tasks))[:5]  # Max 5 Tasks

    def generate_smart_update(self):
        """Generiert KOMPAKTES Update mit Kontext"""
        lines = []

        # Header
        lines.append("# NAJIKA SMART UPDATE")
        lines.append(f"**{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
        lines.append("")

        # Vorherige Session Kontext
        if self.previous_session:
            lines.append("## KONTEXT AUS VORHERIGER SESSION")
            lines.append("")

            prev_messages = self.extract_user_messages(self.previous_session, max_messages=10)

            if prev_messages:
                lines.append("### Letzte User-Anforderungen:")
                lines.append("")

                # Nur die letzten 3 VOLLSTÄNDIGEN Messages
                for msg in prev_messages[-3:]:
                    lines.append(f"**{msg['timestamp'][:10]}:**")
                    lines.append("```")
                    lines.append(msg['text'][:500])  # Max 500 chars pro Message
                    if len(msg['text']) > 500:
                        lines.append("... (gekürzt)")
                    lines.append("```")
                    lines.append("")

                # Erkannte Tasks
                self.open_tasks = self.detect_open_tasks(prev_messages)
                if self.open_tasks:
                    lines.append("### ERKANNTE OFFENE AUFGABEN:")
                    lines.append("")
                    for task in self.open_tasks:
                        lines.append(f"- {task}")
                    lines.append("")

            lines.append("---")
            lines.append("")

        # Aktuelle Session Info
        lines.append("## AKTUELLE SESSION")
        lines.append(f"- Session ID: `{self.current_session.name if self.current_session else 'unknown'}`")
        lines.append(f"- Vorherige: `{self.previous_session.name if self.previous_session else 'none'}`")
        lines.append("")

        # CLAUDE ANWEISUNGEN
        lines.append("---")
        lines.append("")
        lines.append("## FÜR CLAUDE CODE:")
        lines.append("")
        lines.append("**PFLICHT-SCHRITTE:**")
        lines.append("")
        lines.append("1. **LIES ZUERST** alle Files die du editieren willst (Read Tool OHNE offset/limit)!")
        lines.append("2. **PRÜFE** die 'ERKANNTE OFFENE AUFGABEN' oben - sind diese erledigt?")
        lines.append("3. **FRAGE** den User was als nächstes zu tun ist!")
        lines.append("")
        lines.append("**TOKEN-EFFIZIENZ:**")
        lines.append("")
        lines.append("- Lies nur RELEVANTE Files komplett")
        lines.append("- Nutze Grep für Suchen statt File-Reading")
        lines.append("- Fasse dich kurz - User kennt den Kontext bereits")
        lines.append("- KEINE Trial-and-Error Edits - lies IMMER zuerst!")
        lines.append("")
        lines.append("**WENN USER TEXTSTÜCK SENDET:**")
        lines.append("")
        lines.append("- Suche SOFORT in vorheriger Session nach dem kompletten Text")
        lines.append("- Nutze: `grep -F 'TEXTSTÜCK' PREVIOUS_SESSION.jsonl`")
        lines.append("- Lies den VOLLSTÄNDIGEN Kontext aus der Session")
        lines.append("")

        # Speichern
        UPDATE_FILE.write_text('\n'.join(lines), encoding='utf-8')
        print(f"\n[OK] Smart Update erstellt: {UPDATE_FILE}")

    def run(self):
        """Führt Smart Update durch"""
        print("="*70)
        print("NAJIKA SMART UPDATE SYSTEM")
        print("="*70)
        print()

        # Sessions finden
        if not self.find_sessions():
            print("[ERROR] Konnte Sessions nicht finden!")
            return

        # Update generieren
        self.generate_smart_update()

        print()
        print("="*70)
        print("FERTIG!")
        print("="*70)
        print()
        print(f"Claude sollte jetzt lesen: {UPDATE_FILE}")
        print()

if __name__ == "__main__":
    updater = SmartUpdate()
    updater.run()
