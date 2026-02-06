#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA SESSION IMPORTER
Importiert Claude-Code Sessions als Training-Daten

Features:
1. Liest ALLE .jsonl Session-Dateien
2. Extrahiert Code, Konversationen, Problemlösungen
3. Formatiert als Training-Daten (Llama3.1 Template)
4. Speichert in ChromaDB für Training
5. Automatischer täglicher Import

Ziel: Najika lernt aus ALLEN Claude-Sessions!
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import glob
from datetime import datetime
from pathlib import Path

# ChromaDB Import
from najika_memory import NajikaMemory

class NajikaSessionImporter:
    """Importiert Claude-Sessions als Training-Daten"""

    def __init__(
        self,
        sessions_dir="C:/Users/0KKK0/.claude/projects",
        import_log="C:/Najika_World/session_import_log.json"
    ):
        self.sessions_dir = sessions_dir
        self.import_log_file = import_log

        # Memory System
        self.memory = NajikaMemory()

        # Lade Import-Log (bereits importierte Sessions)
        self.import_log = self._load_import_log()

        print("=" * 60)
        print("NAJIKA SESSION IMPORTER")
        print("=" * 60)
        print(f"Sessions-Verzeichnis: {sessions_dir}")
        print(f"Import-Log: {import_log}")
        print()

    def _load_import_log(self):
        """Lädt Log der bereits importierten Sessions"""
        if os.path.exists(self.import_log_file):
            with open(self.import_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"imported_sessions": [], "last_import": None}

    def _save_import_log(self):
        """Speichert Import-Log"""
        with open(self.import_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.import_log, f, indent=2, ensure_ascii=False)

    def find_all_sessions(self):
        """Findet ALLE .jsonl Session-Dateien"""
        pattern = os.path.join(self.sessions_dir, "**", "*.jsonl")
        sessions = glob.glob(pattern, recursive=True)

        print(f"🔍 Gefundene Sessions: {len(sessions)}")

        # Filter bereits importierte
        new_sessions = [
            s for s in sessions
            if s not in self.import_log['imported_sessions']
        ]

        print(f"📥 Neue Sessions: {len(new_sessions)}")
        print()

        return new_sessions

    def parse_session(self, session_file):
        """
        Parst eine Session-Datei

        Extrahiert:
        - User-Fragen
        - Assistant-Antworten
        - Code-Blöcke
        - Tool-Nutzung
        - Problemlösungen
        """
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            conversations = []

            for line in lines:
                try:
                    entry = json.loads(line)

                    # User Message
                    if entry.get('type') == 'user':
                        message = entry.get('message', {})

                        # Content kann String oder Liste sein
                        content = message.get('content', '')
                        if isinstance(content, list):
                            # Extrahiere Text aus Content-Blocks
                            texts = [block.get('text', '') for block in content if block.get('type') == 'text']
                            user_text = '\n'.join(texts)
                        else:
                            user_text = content

                        # Filtere Metadaten und Command-Messages
                        if user_text and not entry.get('isMeta') and '<command-message>' not in user_text:
                            conversations.append({
                                'type': 'user',
                                'text': user_text.strip(),
                                'timestamp': entry.get('timestamp')
                            })

                    # Assistant Message
                    elif entry.get('type') == 'assistant':
                        message = entry.get('message', {})
                        content = message.get('content', [])

                        # Extrahiere Text aus Content-Blocks
                        if isinstance(content, list):
                            texts = [block.get('text', '') for block in content if block.get('type') == 'text']
                            assistant_text = '\n'.join(texts)
                        else:
                            assistant_text = str(content)

                        if assistant_text.strip():
                            conversations.append({
                                'type': 'assistant',
                                'text': assistant_text.strip(),
                                'timestamp': entry.get('timestamp')
                            })

                except json.JSONDecodeError:
                    continue

            return conversations

        except Exception as e:
            print(f"❌ Fehler beim Parsen {session_file}: {e}")
            return []

    def format_as_training_data(self, conversations):
        """
        Formatiert Konversationen als Llama3.1 Training-Daten

        Paart User + Assistant Messages
        """
        training_samples = []

        i = 0
        while i < len(conversations) - 1:
            if (conversations[i]['type'] == 'user' and
                conversations[i+1]['type'] == 'assistant'):

                user_msg = conversations[i]['text']
                assistant_msg = conversations[i+1]['text']

                # Llama3.1 Template
                formatted = f"""<|start_header_id|>user<|end_header_id|>

{user_msg}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{assistant_msg}<|eot_id|>"""

                training_samples.append({
                    'text': formatted,
                    'timestamp': conversations[i].get('timestamp')
                })

                i += 2
            else:
                i += 1

        return training_samples

    def import_session(self, session_file):
        """
        Importiert eine Session komplett

        1. Parse Session
        2. Format als Training-Daten
        3. Speichere in ChromaDB
        """
        print(f"📥 Importiere: {os.path.basename(session_file)}")

        # Parse
        conversations = self.parse_session(session_file)

        if not conversations:
            print("   ⚠️  Keine Konversationen gefunden")
            return 0

        # Format
        training_samples = self.format_as_training_data(conversations)

        if not training_samples:
            print("   ⚠️  Keine Training-Samples erstellt")
            return 0

        # Speichere in ChromaDB (als Konversationen)
        imported_count = 0

        for sample in training_samples:
            try:
                # Erstelle eindeutige ID
                timestamp = sample.get('timestamp', datetime.now().isoformat())
                conv_id = f"session_import_{timestamp}_{imported_count}"

                # Speichere in conversations Collection
                self.memory.conversations.add(
                    ids=[conv_id],
                    documents=[sample['text']],
                    metadatas=[{
                        'source': 'claude_session',
                        'session_file': os.path.basename(session_file),
                        'timestamp': timestamp,
                        'imported_at': datetime.now().isoformat()
                    }]
                )

                imported_count += 1

            except Exception as e:
                print(f"   ❌ Fehler: {e}")
                continue

        print(f"   ✅ {imported_count} Training-Samples importiert")

        # Update Import-Log
        self.import_log['imported_sessions'].append(session_file)
        self.import_log['last_import'] = datetime.now().isoformat()
        self._save_import_log()

        return imported_count

    def import_all_new_sessions(self):
        """
        Importiert ALLE neuen Sessions

        Hauptfunktion für täglichen Auto-Import
        """
        print("🚀 Starte Session-Import...\n")

        # Finde neue Sessions
        new_sessions = self.find_all_sessions()

        if not new_sessions:
            print("✅ Keine neuen Sessions - alles aktuell!")
            return

        # Importiere alle
        total_samples = 0

        for session in new_sessions:
            samples = self.import_session(session)
            total_samples += samples
            print()

        print("=" * 60)
        print("✅ IMPORT ABGESCHLOSSEN!")
        print("=" * 60)
        print(f"Sessions importiert: {len(new_sessions)}")
        print(f"Training-Samples: {total_samples}")
        print()
        print("NÄCHSTER SCHRITT: Training ausführen!")
        print("python najika_lora_training.py")
        print()


# MAIN
if __name__ == "__main__":
    importer = NajikaSessionImporter()
    importer.import_all_new_sessions()
