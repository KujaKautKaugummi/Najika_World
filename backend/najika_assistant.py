#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NAJIKA ASSISTANT - CLI wie Claude Code!

Usage:
    python najika_assistant.py

    Oder mit Start-Script:
    najika.bat

Features:
- ✅ Interaktiver Chat wie Claude Code
- ✅ Durchsucht ALLE Projekt-Daten (ChromaDB Memory)
- ✅ Tools: Read/Write/Execute/Search
- ✅ Ollama Integration (najika-local Model)
- ✅ Session-Speicherung
- ✅ Projekt-Kontext automatisch geladen

Author: Claude Code (CLI) & Kuja
Date: 2025-12-04
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Fix Windows encoding (nur wenn Buffer noch offen ist)
if sys.platform == 'win32':
    import io
    try:
        if hasattr(sys.stdout, 'buffer') and not sys.stdout.buffer.closed:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'buffer') and not sys.stderr.buffer.closed:
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (ValueError, OSError):
        pass

# Imports
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  requests nicht installiert - pip install requests")

try:
    from najika_memory_enhanced import NajikaMemoryEnhanced
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    print("⚠️  najika_memory_enhanced nicht verfügbar")


class NajikaAssistant:
    """Najika als CLI-Assistant wie Claude Code"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.session_file = self.project_root / "backend" / ".najika_session.json"
        self.history = []
        self.memory = None
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = "najika-local"

        # Statistiken
        self.stats = {
            "messages": 0,
            "tool_calls": 0,
            "memory_searches": 0
        }

        # Load Memory System
        if MEMORY_AVAILABLE:
            try:
                self.memory = NajikaMemoryEnhanced()
                print("✅ ChromaDB Memory geladen (alle Projekt-Daten verfügbar)")
            except Exception as e:
                print(f"⚠️  Memory System Fehler: {e}")
                self.memory = None

        # Load Session
        self.load_session()

    def print_header(self):
        """Print welcome header"""
        print("\n" + "=" * 70)
        print("🔥 NAJIKA ASSISTANT - Interactive CLI")
        print("=" * 70)
        print()
        print("Wie Claude Code, aber mit Najika's Megumin-Persönlichkeit!")
        print()
        print("💡 Commands:")
        print("  /help       - Zeige Hilfe")
        print("  /read FILE  - Lies Datei")
        print("  /write FILE - Schreibe Datei")
        print("  /exec CMD   - Führe Command aus")
        print("  /search Q   - Durchsuche Projekt-Memory")
        print("  /stats      - Zeige Statistiken")
        print("  /clear      - Lösche Chat-Historie")
        print("  /save       - Speichere Session")
        print("  /exit       - Beende")
        print()
        print("📚 Projekt-Context:")
        print(f"   Root: {self.project_root}")
        print(f"   Memory: {'✅ Aktiv' if self.memory else '❌ Nicht verfügbar'}")
        print(f"   Session: {len(self.history)} Nachrichten geladen")
        print()
        print("💬 Schreibe einfach deine Nachricht und drücke Enter!")
        print("=" * 70)
        print()

    def load_session(self):
        """Load previous session"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])[-20:]  # Last 20 messages
                    self.stats = data.get('stats', self.stats)
            except Exception as e:
                print(f"⚠️  Session konnte nicht geladen werden: {e}")

    def save_session(self):
        """Save current session"""
        try:
            self.session_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                'history': self.history[-50:],  # Save last 50 messages
                'stats': self.stats,
                'saved_at': datetime.now().isoformat()
            }
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("\n✅ Session gespeichert!")
        except Exception as e:
            print(f"\n❌ Fehler beim Speichern: {e}")

    def search_memory(self, query, k=5):
        """Search project memory"""
        if not self.memory:
            return "❌ Memory System nicht verfügbar"

        self.stats["memory_searches"] += 1

        try:
            results = self.memory.search(query, k=k)

            if not results:
                return "🤷 Keine Ergebnisse gefunden"

            output = [f"📚 Projekt-Memory Suche: '{query}'", ""]

            for i, res in enumerate(results, 1):
                metadata = res.get('metadata', {})
                content = res.get('content', 'No content')[:200]  # First 200 chars

                output.append(f"{i}. {metadata.get('source', 'Unknown')}")
                output.append(f"   {content}...")
                output.append("")

            return "\n".join(output)

        except Exception as e:
            return f"❌ Memory Search Fehler: {e}"

    def read_file(self, filepath):
        """Read file"""
        self.stats["tool_calls"] += 1

        try:
            path = Path(filepath)
            if not path.is_absolute():
                path = self.project_root / filepath

            if not path.exists():
                return f"❌ Datei nicht gefunden: {path}"

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            return f"📄 {path}\n\n{content}"

        except Exception as e:
            return f"❌ Fehler beim Lesen: {e}"

    def write_file(self, filepath, content):
        """Write file"""
        self.stats["tool_calls"] += 1

        try:
            path = Path(filepath)
            if not path.is_absolute():
                path = self.project_root / filepath

            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            return f"✅ Datei geschrieben: {path}"

        except Exception as e:
            return f"❌ Fehler beim Schreiben: {e}"

    def execute_command(self, cmd):
        """Execute shell command"""
        self.stats["tool_calls"] += 1

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.project_root)
            )

            output = []
            if result.stdout:
                output.append("STDOUT:")
                output.append(result.stdout)
            if result.stderr:
                output.append("STDERR:")
                output.append(result.stderr)

            return "\n".join(output) if output else "✅ Command ausgeführt (keine Ausgabe)"

        except subprocess.TimeoutExpired:
            return "⏱️  Timeout - Command dauert zu lange"
        except Exception as e:
            return f"❌ Fehler: {e}"

    def call_ollama(self, prompt):
        """Call Ollama API"""
        if not REQUESTS_AVAILABLE:
            return "❌ requests nicht installiert"

        try:
            # Build context from history
            context_messages = []
            for msg in self.history[-6:]:  # Last 6 messages
                context_messages.append(f"{msg['role']}: {msg['content']}")

            context = "\n".join(context_messages) if context_messages else ""

            full_prompt = f"""Du bist Najika - Kuja's KI-Begleiterin mit Megumin-Persönlichkeit!

KONTEXT:
{context}

USER: {prompt}

NAJIKA:"""

            payload = {
                "model": self.ollama_model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.9,
                    "num_predict": 400
                }
            }

            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()
            return data.get('response', '').strip()

        except requests.exceptions.ConnectionError:
            return "❌ Ollama läuft nicht! Starte mit: ollama serve"
        except requests.exceptions.Timeout:
            return "⏱️  Timeout - Ollama antwortet nicht"
        except Exception as e:
            return f"❌ Ollama Fehler: {e}"

    def handle_command(self, user_input):
        """Handle special commands"""
        if user_input.startswith('/'):
            cmd = user_input.split()[0]
            args = user_input[len(cmd):].strip()

            if cmd == '/help':
                return """
📋 NAJIKA ASSISTANT - Commands:

/help           - Zeige diese Hilfe
/read FILE      - Lies Datei (z.B. /read backend/najika_server.py)
/write FILE     - Schreibe Datei (dann Content eingeben)
/exec CMD       - Führe Shell Command aus
/search QUERY   - Durchsuche Projekt-Memory
/stats          - Zeige Statistiken
/clear          - Lösche Chat-Historie
/save           - Speichere Session
/exit           - Beende Assistant

💬 Oder schreibe einfach deine Nachricht!
"""

            elif cmd == '/read':
                if not args:
                    return "❌ Usage: /read FILE"
                return self.read_file(args)

            elif cmd == '/write':
                if not args:
                    return "❌ Usage: /write FILE"
                print(f"\n📝 Schreibe Content für {args} (Ende mit leerer Zeile):")
                lines = []
                while True:
                    try:
                        line = input()
                        if not line:
                            break
                        lines.append(line)
                    except EOFError:
                        break
                content = "\n".join(lines)
                return self.write_file(args, content)

            elif cmd == '/exec':
                if not args:
                    return "❌ Usage: /exec COMMAND"
                return self.execute_command(args)

            elif cmd == '/search':
                if not args:
                    return "❌ Usage: /search QUERY"
                return self.search_memory(args)

            elif cmd == '/stats':
                return f"""
📊 STATISTIKEN:

Nachrichten: {self.stats['messages']}
Tool Calls: {self.stats['tool_calls']}
Memory Searches: {self.stats['memory_searches']}
History: {len(self.history)} Einträge
Memory: {'✅ Aktiv' if self.memory else '❌ Inaktiv'}
"""

            elif cmd == '/clear':
                self.history = []
                return "🗑️  Chat-Historie gelöscht"

            elif cmd == '/save':
                self.save_session()
                return None  # Already printed message

            elif cmd == '/exit':
                return "EXIT"

            else:
                return f"❌ Unbekannter Command: {cmd}\nTippe /help für Hilfe"

        return None  # Not a command

    def interactive_loop(self):
        """Main interactive loop"""
        self.print_header()

        while True:
            try:
                # Get user input
                user_input = input("💬 DU: ").strip()

                if not user_input:
                    continue

                # Handle commands
                cmd_result = self.handle_command(user_input)
                if cmd_result == "EXIT":
                    print("\n👋 Tschüss! EXPLOSION!!! 💥\n")
                    self.save_session()
                    break
                elif cmd_result:
                    print(f"\n{cmd_result}\n")
                    continue

                # Regular message - call Ollama
                self.stats["messages"] += 1

                print("\n🤔 Najika denkt...\n")
                response = self.call_ollama(user_input)

                # Print response
                print(f"🔥 NAJIKA: {response}\n")

                # Save to history
                self.history.append({"role": "user", "content": user_input})
                self.history.append({"role": "assistant", "content": response})

                # Keep history at max 50 messages
                if len(self.history) > 50:
                    self.history = self.history[-50:]

            except KeyboardInterrupt:
                print("\n\n👋 Tschüss! EXPLOSION!!! 💥\n")
                self.save_session()
                break
            except EOFError:
                print("\n\n👋 Tschüss! EXPLOSION!!! 💥\n")
                self.save_session()
                break
            except Exception as e:
                print(f"\n❌ Fehler: {e}\n")

    def run(self):
        """Start the assistant"""
        self.interactive_loop()


# Global instance
CLAUDE_CODE_INSTANCE = None

def main():
    """Main entry point"""
    global CLAUDE_CODE_INSTANCE

    assistant = NajikaAssistant()
    CLAUDE_CODE_INSTANCE = assistant
    assistant.run()


if __name__ == "__main__":
    main()
