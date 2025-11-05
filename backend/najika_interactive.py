#!/usr/bin/env python3
"""
NAJIKA INTERACTIVE MODE
Wie Claude Code, aber mit Najika!

Usage:
    najika

Oder:
    python najika_interactive.py
"""

import sys
import json
import os
from pathlib import Path
import codecs

try:
    import requests
except ImportError:
    import urllib.request
    import urllib.parse
    requests = None

# Import Tools
try:
    from najika_tools import NajikaTools
    from knowledge_loader import load_knowledge, get_available_topics
except ImportError:
    NajikaTools = None
    load_knowledge = None
    get_available_topics = None

# Configuration
API_URL = "http://localhost:8000/api/chat"
TIMEOUT = 120
KNOWLEDGE_FILE = Path("knowledge/complete_project_context.json")
SESSION_FILE = Path("knowledge/najika_session.json")

class NajikaInteractive:
    """Interaktive Najika-Session"""

    def __init__(self):
        self.session_id = None
        self.message_count = 0
        self.context_loaded = False
        self.knowledge_context = ""
        self.session_history = []

        # UTF-8 Encoding für Windows
        if sys.platform == 'win32':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

    def start(self):
        """Startet interaktive Session"""
        self.print_header()
        self.load_session()
        self.load_project_knowledge()
        self.interactive_loop()

    def print_header(self):
        """Zeigt Header"""
        print("=" * 70)
        print("NAJIKA - INTERACTIVE CODING ASSISTANT")
        print("=" * 70)
        print()
        print("Wie Claude Code, aber mit Najika's Persönlichkeit!")
        print()
        print("Commands:")
        print("  /help     - Zeige Hilfe")
        print("  /context  - Zeige geladenen Context")
        print("  /tools    - Zeige verfügbare Tools")
        print("  /read <file>   - Lies Datei")
        print("  /write <file>  - Schreibe Datei")
        print("  /list [dir]    - Liste Dateien")
        print("  /analyze       - Analysiere komplettes Projekt")
        print("  /save     - Speichere Session")
        print("  /exit     - Beende Session")
        print()
        print("Oder schreibe einfach deine Nachricht!")
        print("=" * 70)
        print()

    def load_session(self):
        """Lädt letzte Session"""
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.session_history = data.get('history', [])
                    self.message_count = data.get('message_count', 0)
                    print(f"✅ Session geladen ({self.message_count} Nachrichten)")
                    print()
            except Exception as e:
                print(f"⚠️  Session konnte nicht geladen werden: {e}")
                print()

    def save_session(self):
        """Speichert aktuelle Session"""
        try:
            SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {
                'history': self.session_history[-50:],  # Letzte 50 Nachrichten
                'message_count': self.message_count
            }
            with open(SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print()
            print("✅ Session gespeichert!")
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern: {e}")

    def load_project_knowledge(self):
        """Lädt komplettes Projekt-Wissen"""
        print("📚 Lade Projekt-Knowledge...")

        context_parts = []

        # 1. Lade komplette Projekt-Analyse
        if KNOWLEDGE_FILE.exists():
            try:
                with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                    stats = project_data.get('statistics', {})

                    context_parts.append(f"""[PROJEKT-KONTEXT]
Dateien analysiert: {stats.get('files_analyzed', 0)}
Code-Dateien: {stats.get('code_files', 0)}
Zeilen Code: {stats.get('total_lines', 0):,}

Du hast Zugriff auf:
- C:/NajikaCore/ (alle Dateien)
- C:/Users/0KKK0/Desktop/zip/ (alle Dateien)
- C:/Users/0KKK0/.claude/ (alle Dateien)

Du kennst JEDEN Code, JEDEN Fehler, JEDEN Erfolg!
""")
                    print("✅ Projekt-Analyse geladen")
            except Exception as e:
                print(f"⚠️  Projekt-Analyse nicht verfügbar: {e}")

        # 2. Lade Programmier-Knowledge
        if load_knowledge:
            try:
                topics = get_available_topics() if get_available_topics else ["python", "java", "verse"]
                prog_knowledge = load_knowledge(topics, max_chars=4000)
                if prog_knowledge:
                    context_parts.append(prog_knowledge)
                    print(f"✅ Programmier-Knowledge geladen ({len(topics)} Sprachen)")
            except Exception as e:
                print(f"⚠️  Programmier-Knowledge nicht verfügbar: {e}")

        # 3. Lade Session-History
        if self.session_history:
            history_context = "\n[LETZTE SESSION]\n"
            for msg in self.session_history[-5:]:  # Letzte 5 Nachrichten
                history_context += f"{msg.get('role', 'user')}: {msg.get('content', '')[:100]}...\n"
            context_parts.append(history_context)
            print(f"✅ Session-History geladen ({len(self.session_history)} Nachrichten)")

        self.knowledge_context = "\n\n".join(context_parts)
        self.context_loaded = True
        print()

    def interactive_loop(self):
        """Hauptloop für Interaktion"""
        while True:
            try:
                # User Input
                user_input = input("Du: ").strip()

                if not user_input:
                    continue

                # Commands verarbeiten
                if user_input.startswith('/'):
                    if not self.handle_command(user_input):
                        break  # /exit
                    continue

                # Normale Nachricht an Najika
                self.message_count += 1
                print()
                print("Najika: ", end="", flush=True)

                response = self.send_to_najika(user_input)
                print(response)
                print()

                # Speichere in History
                self.session_history.append({
                    'role': 'user',
                    'content': user_input
                })
                self.session_history.append({
                    'role': 'assistant',
                    'content': response
                })

                # Auto-save alle 5 Nachrichten
                if self.message_count % 5 == 0:
                    self.save_session()

            except KeyboardInterrupt:
                print()
                print()
                print("Session unterbrochen. Speichere...")
                self.save_session()
                break
            except EOFError:
                break

    def handle_command(self, command):
        """Verarbeitet Slash-Commands"""
        cmd_parts = command.split(maxsplit=1)
        cmd = cmd_parts[0].lower()
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""

        if cmd == '/help':
            self.print_header()
            return True

        elif cmd == '/exit':
            print()
            print("Beende Session...")
            self.save_session()
            print()
            print("EXPLOSION!!! Bis bald! ✨")
            print()
            return False

        elif cmd == '/save':
            self.save_session()
            return True

        elif cmd == '/context':
            print()
            print("=" * 70)
            print("GELADENER CONTEXT:")
            print("=" * 70)
            print(self.knowledge_context[:2000])
            if len(self.knowledge_context) > 2000:
                print(f"\n... ({len(self.knowledge_context)} Zeichen total)")
            print("=" * 70)
            print()
            return True

        elif cmd == '/tools':
            if NajikaTools:
                print()
                print("Verfügbare Tools:")
                print("  - read_file(path)")
                print("  - write_file(path, content)")
                print("  - list_files(directory)")
                print("  - execute_command(cmd)")
                print()
            else:
                print("⚠️  Tools nicht verfügbar")
            return True

        elif cmd == '/read':
            if not args:
                print("Usage: /read <file_path>")
                return True
            if NajikaTools:
                tools = NajikaTools()
                result = tools.read_file(args)
                print()
                print(result)
                print()
            return True

        elif cmd == '/write':
            print("Usage: /write <file_path>")
            print("(Nutze Chat für Write-Operationen)")
            return True

        elif cmd == '/list':
            directory = args if args else "."
            if NajikaTools:
                tools = NajikaTools()
                result = tools.list_files(directory)
                print()
                print(result)
                print()
            return True

        elif cmd == '/analyze':
            print()
            print("Starte komplette Projekt-Analyse...")
            print("(Dies kann einen Moment dauern)")
            print()
            os.system("python analyze_all.py")
            print()
            print("Lade neuen Context...")
            self.load_project_knowledge()
            return True

        else:
            print(f"Unbekanntes Command: {cmd}")
            print("Verwende /help für Hilfe")
            return True

    def send_to_najika(self, message):
        """Sendet Nachricht an Najika"""
        # Baue vollständigen Prompt mit Context
        full_message = message
        if self.knowledge_context:
            full_message = f"{self.knowledge_context}\n\n[USER REQUEST]\n{message}"

        payload = {"message": full_message}

        if requests:
            try:
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=TIMEOUT
                )
                response.raise_for_status()
                data = response.json()
                return self.clean_unicode(data.get("response", "FEHLER: Keine Response"))
            except requests.exceptions.ConnectionError:
                return "FEHLER: Najika-Server läuft nicht! Starte mit: START_NAJIKA.bat"
            except requests.exceptions.Timeout:
                return "FEHLER: Timeout - Anfrage dauert zu lange"
            except Exception as e:
                return f"FEHLER: {str(e)}"
        else:
            # Fallback zu urllib
            try:
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    API_URL,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return self.clean_unicode(result.get("response", "FEHLER: Keine Response"))
            except urllib.error.URLError:
                return "FEHLER: Najika-Server läuft nicht! Starte mit: START_NAJIKA.bat"
            except Exception as e:
                return f"FEHLER: {str(e)}"

    def clean_unicode(self, text):
        """Entfernt Emoji für CMD"""
        import re
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\u2728"
            u"\u2764"
            u"\U0001F48E"
            u"\U0001F525"
            u"\U0001F4A5"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub('', text)


def main():
    """Main entry point"""
    session = NajikaInteractive()
    session.start()


if __name__ == "__main__":
    main()
