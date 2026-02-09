#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA CLAUDE KNOWLEDGE SYNC
Synchronisiert Wissen zwischen allen Claude Instanzen:
- Desktop Claude Code Sessions
- Online Claude.ai Chats/Code
- ChromaDB Gedächtnis
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import chromadb
from pathlib import Path
from datetime import datetime
import hashlib

# Pfade
SESSIONS_DIR = Path(r"C:\Users\0KKK0\.claude\projects\C--Najika-World")
CHROMADB_PATH = "C:/Najika_World/memory_db"
ONLINE_IMPORT_DIR = Path(r"C:\Najika_World\online_imports")
SYNC_LOG = Path(r"C:\Najika_World\SYNC_LOG.md")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_doc_id(content):
    """Generiert eindeutige ID"""
    return hashlib.md5(content[:200].encode()).hexdigest()[:16]

class ClaudeKnowledgeSync:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMADB_PATH)

        # Session-Knowledge Collection
        try:
            self.sessions = self.client.get_collection("najika_session_knowledge")
            log(f"Session-Knowledge Collection: {self.sessions.count()} Eintraege")
        except:
            self.sessions = self.client.create_collection(
                name="najika_session_knowledge",
                metadata={"description": "Wissen aus Claude Sessions (Desktop + Online)"}
            )
            log("Session-Knowledge Collection erstellt")

    def import_online_chat(self, chat_file):
        """Importiert einen exportierten Online-Chat"""
        if not chat_file.exists():
            log(f"Datei nicht gefunden: {chat_file}")
            return 0

        log(f"Importiere: {chat_file.name}")

        content = chat_file.read_text(encoding='utf-8')

        # Teile in Chunks
        chunks = []
        chunk_size = 3000
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i+chunk_size]
            if chunk.strip():
                chunks.append(chunk)

        imported = 0
        for i, chunk in enumerate(chunks):
            doc_id = get_doc_id(f"online_{chat_file.stem}_{i}_{chunk}")

            self.sessions.upsert(
                ids=[doc_id],
                documents=[chunk],
                metadatas=[{
                    "source": "online_chat",
                    "file": chat_file.name,
                    "chunk_index": str(i),
                    "import_date": datetime.now().isoformat()
                }]
            )
            imported += 1

        log(f"  Importiert: {imported} Chunks")
        return imported

    def import_desktop_session(self, session_file, max_messages=100):
        """Importiert wichtige Nachrichten aus Desktop-Session"""
        if not session_file.exists():
            return 0

        log(f"Importiere Desktop-Session: {session_file.name[:30]}...")

        imported = 0
        message_count = 0

        try:
            with open(session_file, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    if message_count >= max_messages:
                        break

                    try:
                        data = json.loads(line)

                        # Nur wichtige Nachrichten (User + Assistant)
                        if data.get("role") in ["user", "assistant"]:
                            content = str(data.get("content", ""))

                            # Nur Nachrichten > 100 Zeichen
                            if len(content) > 100:
                                doc_id = get_doc_id(f"desktop_{session_file.stem}_{message_count}_{content}")

                                self.sessions.upsert(
                                    ids=[doc_id],
                                    documents=[content[:5000]],  # Max 5000 chars
                                    metadatas=[{
                                        "source": "desktop_session",
                                        "session": session_file.name[:36],
                                        "role": data.get("role", "unknown"),
                                        "import_date": datetime.now().isoformat()
                                    }]
                                )
                                imported += 1
                                message_count += 1

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            log(f"  Error: {e}")

        log(f"  Importiert: {imported} Nachrichten")
        return imported

    def sync_all_desktop_sessions(self, limit=10):
        """Synchronisiert die neuesten Desktop-Sessions"""
        log("\n=== DESKTOP SESSIONS SYNC ===")

        sessions = list(SESSIONS_DIR.glob("*.jsonl"))
        sessions = [s for s in sessions if not s.name.startswith("agent-")]
        sessions.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        total = 0
        for session in sessions[:limit]:
            if session.stat().st_size > 1000:  # Skip empty
                total += self.import_desktop_session(session)

        log(f"Total Desktop: {total} Nachrichten importiert")
        return total

    def sync_online_imports(self):
        """Synchronisiert alle Online-Imports"""
        log("\n=== ONLINE IMPORTS SYNC ===")

        if not ONLINE_IMPORT_DIR.exists():
            ONLINE_IMPORT_DIR.mkdir(parents=True)
            log(f"Import-Ordner erstellt: {ONLINE_IMPORT_DIR}")
            log("Exportiere Online-Chats dorthin als .txt oder .md!")
            return 0

        files = list(ONLINE_IMPORT_DIR.glob("*.txt")) + list(ONLINE_IMPORT_DIR.glob("*.md"))

        if not files:
            log("Keine Online-Imports gefunden.")
            log(f"Exportiere Claude.ai Chats nach: {ONLINE_IMPORT_DIR}")
            return 0

        total = 0
        for f in files:
            total += self.import_online_chat(f)

        log(f"Total Online: {total} Chunks importiert")
        return total

    def get_stats(self):
        """Zeigt aktuelle Statistiken"""
        log("\n=== SYNC STATISTIKEN ===")

        total = self.sessions.count()
        log(f"Session-Knowledge Total: {total}")

        # Nach Source gruppieren
        try:
            all_data = self.sessions.get(include=["metadatas"])
            sources = {}
            for meta in all_data.get("metadatas", []):
                src = meta.get("source", "unknown")
                sources[src] = sources.get(src, 0) + 1

            for src, count in sorted(sources.items()):
                log(f"  - {src}: {count}")
        except:
            pass

        return total

    def write_sync_log(self):
        """Schreibt Sync-Log"""
        content = f"""# 📡 NAJIKA SYNC LOG

**Letzter Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Statistiken

- **Session-Knowledge:** {self.sessions.count()} Eintraege

## 📥 Import-Ordner

Online-Chats exportieren nach:
`{ONLINE_IMPORT_DIR}`

## 🔄 Naechster Sync

```bash
python C:\\Najika_World\\backend\\sync_claude_knowledge.py
```
"""
        SYNC_LOG.write_text(content, encoding='utf-8')
        log(f"\nSync-Log: {SYNC_LOG}")

def main():
    log("=" * 70)
    log("NAJIKA CLAUDE KNOWLEDGE SYNC")
    log("=" * 70)

    sync = ClaudeKnowledgeSync()

    # Sync Desktop Sessions (neueste 5)
    sync.sync_all_desktop_sessions(limit=5)

    # Sync Online Imports
    sync.sync_online_imports()

    # Stats
    sync.get_stats()

    # Log schreiben
    sync.write_sync_log()

    log("\n" + "=" * 70)
    log("SYNC ABGESCHLOSSEN")
    log("=" * 70)

if __name__ == "__main__":
    main()
