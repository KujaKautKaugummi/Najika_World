#!/usr/bin/env python3
"""
NAJIKA SMART UPDATE SYSTEM V2
Verbesserte Version mit:
- Task-Tracking über Sessions
- Automatische File-Read Liste
- Kontext-Caching
- Noch token-effizienter
"""

import json
import re
from pathlib import Path
from datetime import datetime

NAJIKA_DIR = Path("C:/Najika_World")
CLAUDE_PROJECTS = Path("C:/Users/0KKK0/.claude/projects/C--NajikaCore")
CLAUDE_TODOS = Path("C:/Users/0KKK0/.claude/todos")
UPDATE_FILE = NAJIKA_DIR / "CLAUDE_SMART_UPDATE.md"
TASK_TRACKING = NAJIKA_DIR / "knowledge" / "task_tracking.json"

class SmartUpdateV2:
    def __init__(self):
        self.current_session = None
        self.previous_session = None
        self.open_tasks = []
        self.completed_tasks = []
        self.files_to_read = []
        self.tracked_tasks = self.load_tracked_tasks()
        self.previous_todos = []

    def load_tracked_tasks(self):
        """Lädt gespeicherte Tasks"""
        if TASK_TRACKING.exists():
            try:
                with open(TASK_TRACKING, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"open": [], "completed": []}
        return {"open": [], "completed": []}

    def save_tracked_tasks(self):
        """Speichert Tasks für nächste Session"""
        TASK_TRACKING.parent.mkdir(parents=True, exist_ok=True)
        with open(TASK_TRACKING, 'w', encoding='utf-8') as f:
            json.dump({
                "open": self.open_tasks,
                "completed": self.completed_tasks,
                "last_update": datetime.now().isoformat()
            }, f, indent=2)

    def find_sessions(self):
        """Findet aktuelle und vorherige Session"""
        sessions = sorted(CLAUDE_PROJECTS.glob("*.jsonl"),
                         key=lambda p: p.stat().st_mtime, reverse=True)

        if len(sessions) >= 2:
            self.current_session = sessions[0]
            self.previous_session = sessions[1]
            print(f"[OK] Aktuelle: {self.current_session.name[:12]}...")
            print(f"[OK] Vorherige: {self.previous_session.name[:12]}...")

            # Lade Todo-Liste der vorherigen Session
            self.load_previous_todos()
            return True
        else:
            print("[WARNING] Nicht genug Sessions")
            return False

    def load_previous_todos(self):
        """Lädt Todo-Liste aus vorheriger Session"""
        if not self.previous_session:
            return

        session_id = self.previous_session.stem

        # Suche nach Todo-Files für diese Session
        for todo_file in CLAUDE_TODOS.glob(f"{session_id}*.json"):
            try:
                with open(todo_file, 'r', encoding='utf-8') as f:
                    todos = json.load(f)
                    if todos:  # Nur wenn nicht leer
                        self.previous_todos = todos
                        print(f"[OK] Todos geladen: {len(todos)} Aufgaben")
                        break
            except Exception as e:
                continue

    def extract_user_messages(self, session_file, max_messages=5):
        """Extrahiert User-Messages TOKEN-EFFIZIENT (max 5, max 800 chars pro msg)"""
        user_messages = []

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if entry.get('type') == 'user':
                            msg = entry.get('message', {})
                            content = msg.get('content', [])

                            text_parts = []
                            for item in content:
                                if isinstance(item, dict) and item.get('type') == 'text':
                                    text_parts.append(item.get('text', ''))

                            if text_parts:
                                full_text = ' '.join(text_parts)
                                # Max 800 chars pro Message - verhindert Speicher-Overflow
                                truncated = full_text[:800]
                                user_messages.append({
                                    'timestamp': entry.get('timestamp', '')[:19],
                                    'text': truncated,
                                    'was_truncated': len(full_text) > 800
                                })
                    except:
                        continue

            return user_messages[-max_messages:]
        except Exception as e:
            print(f"[ERROR] Session lesen: {e}")
            return []

    def detect_files_mentioned(self, messages):
        """Erkennt welche Files erwähnt werden -> Auto-Read Liste"""
        file_patterns = [
            r'(najika_\w+\.py)',
            r'(index\.html)',
            r'(3d_scene\.js)',
            r'(najika_\w+\.md)',
            r'(/digivice/\S+)',
            r'(\.env)',
            r'(CLAUDE\.md)'
        ]

        files = set()
        for msg in messages:
            text = msg['text']
            for pattern in file_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                files.update(matches)

        return list(files)[:5]  # Max 5 Files

    def detect_open_tasks(self, messages):
        """Verbesserte Task-Erkennung"""
        task_keywords = [
            # Direkte Befehle
            (r"(mach|erstell|bau|füg|änder|fix|korrigier)\w*\s+\w+", "direct"),
            # Probleme
            (r"(fehler|problem|bug|geht nicht|funktioniert nicht)", "issue"),
            # Wünsche
            (r"(soll|muss|brauch|möcht)\w*\s+\w+", "requirement"),
            # Priorität
            (r"(wichtig|prio|dringend|schnell)", "priority"),
            # UI-Spezifisch
            (r"(w-taste|ui|button|icon|chat|terminal|raum)", "ui_change")
        ]

        tasks = []
        for msg in messages:
            text = msg['text']

            # Zeilenweise durchgehen (besser als Sätze)
            for line in text.split('\n'):
                line = line.strip()
                if len(line) < 10 or len(line) > 200:  # Nur sinnvolle Längen
                    continue

                for pattern, category in task_keywords:
                    if re.search(pattern, line, re.IGNORECASE):
                        tasks.append({
                            'text': line[:150],  # Max 150 chars
                            'category': category,
                            'timestamp': msg['timestamp']
                        })
                        break

        # Dedupliziere + nach Kategorie sortiert
        unique_tasks = []
        seen = set()
        for task in tasks:
            if task['text'] not in seen:
                seen.add(task['text'])
                unique_tasks.append(task)

        return unique_tasks[:8]  # Max 8 Tasks

    def generate_smart_update(self):
        """Generiert OPTIMALES Update"""
        lines = []

        # Kompakter Header
        lines.append("# NAJIKA SMART UPDATE V2")
        lines.append(f"**{datetime.now().strftime('%H:%M:%S')}**")
        lines.append("")

        # Vorherige Session
        if self.previous_session:
            lines.append("## VORHERIGE SESSION KONTEXT")
            lines.append("")

            prev_messages = self.extract_user_messages(self.previous_session, max_messages=5)

            if prev_messages:
                # Alle letzten 5 Messages (max 800 chars pro msg bereits in extract)
                lines.append("### Letzte 5 User-Nachrichten:")
                lines.append("")
                for i, msg in enumerate(prev_messages, 1):
                    lines.append(f"**{i}. Zeit:** {msg['timestamp']}")
                    lines.append("```")
                    lines.append(msg['text'])
                    if msg.get('was_truncated'):
                        lines.append("\n... [GEKÜRZT auf 800 chars]")
                    lines.append("```")
                    lines.append("")

                # Erkannte Tasks
                self.open_tasks = self.detect_open_tasks(prev_messages)
                if self.open_tasks:
                    lines.append("### ERKANNTE OFFENE AUFGABEN:")
                    lines.append("")
                    for task in self.open_tasks:
                        category_icon = {
                            'direct': '🔨',
                            'issue': '🐛',
                            'requirement': '📋',
                            'priority': '⚡',
                            'ui_change': '🎨'
                        }.get(task['category'], '•')
                        lines.append(f"{category_icon} {task['text']}")
                    lines.append("")

                # File-Read Liste
                self.files_to_read = self.detect_files_mentioned(prev_messages)
                if self.files_to_read:
                    lines.append("### FILES DIE ERWÄHNT WURDEN (Read empfohlen):")
                    lines.append("")
                    for f in self.files_to_read:
                        lines.append(f"- `{f}`")
                    lines.append("")

                # Todo-Liste der vorherigen Session
                if self.previous_todos:
                    lines.append("### TODO-LISTE VORHERIGE SESSION:")
                    lines.append("")
                    pending = [t for t in self.previous_todos if t.get('status') == 'pending']
                    in_progress = [t for t in self.previous_todos if t.get('status') == 'in_progress']
                    completed = [t for t in self.previous_todos if t.get('status') == 'completed']

                    if in_progress:
                        lines.append("**⏳ IN ARBEIT:**")
                        for todo in in_progress:
                            lines.append(f"- {todo.get('content', todo.get('activeForm', 'N/A'))}")
                        lines.append("")

                    if pending:
                        lines.append("**📋 OFFEN:**")
                        for todo in pending:
                            lines.append(f"- {todo.get('content', 'N/A')}")
                        lines.append("")

                    if completed:
                        lines.append(f"**✓ ERLEDIGT:** {len(completed)} Aufgaben")
                        lines.append("")

            lines.append("---")
            lines.append("")

        # Claude Anweisungen - KOMPAKT
        lines.append("## ANWEISUNGEN FÜR CLAUDE:")
        lines.append("")
        lines.append("**PFLICHT:**")
        lines.append("1. Lies Files aus 'FILES DIE ERWÄHNT WURDEN' KOMPLETT (Read ohne offset)!")
        lines.append("2. Prüfe 'ERKANNTE OFFENE AUFGABEN' - was ist noch zu tun?")
        lines.append("3. Frage User kurz was als nächstes (max 2 Sätze!)")
        lines.append("")
        lines.append("**TOKEN-EFFIZIENZ:**")
        lines.append("- Read IMMER komplett vor Edit")
        lines.append("- Grep für Suchen, nicht File-Reading")
        lines.append("- User-Textstück? → `grep -F 'TEXT' SESSION.jsonl`")
        lines.append("- Kurze Antworten - User kennt Kontext!")
        lines.append("")

        # Speichern
        UPDATE_FILE.write_text('\n'.join(lines), encoding='utf-8')
        print(f"\n[OK] Smart Update V2: {UPDATE_FILE}")

        # Task-Tracking speichern
        self.save_tracked_tasks()

    def run(self):
        """Führt Smart Update durch"""
        print("\n" + "="*60)
        print("NAJIKA SMART UPDATE V2")
        print("="*60 + "\n")

        if not self.find_sessions():
            print("[ERROR] Sessions nicht gefunden!")
            return

        self.generate_smart_update()

        print("\n" + "="*60)
        print("FERTIG!")
        print("="*60)
        print(f"\nClaude liest: {UPDATE_FILE}")
        print(f"Tasks getrackt: {len(self.open_tasks)}")
        print(f"Files erwähnt: {len(self.files_to_read)}")
        print(f"Todos geladen: {len(self.previous_todos)}\n")

if __name__ == "__main__":
    updater = SmartUpdateV2()
    updater.run()
