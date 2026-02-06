#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA ↔ CLAUDE CODE SYNC SYSTEM
Automatische Synchronisation zwischen Najika und Claude Code

Funktionen:
- Prüft auf neue Dateien in NajikaCore und .claude
- Erstellt automatische Updates für Claude
- Generiert UPDATE.md für Claude Code
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import hashlib

# Fix für Windows Console Encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Paths
NAJIKA_DIR = Path("C:/Najika_World")
CLAUDE_DIR = Path("C:/Users/0KKK0/.claude")
UPDATE_FILE = NAJIKA_DIR / "CLAUDE_UPDATE.md"
SYNC_STATE = NAJIKA_DIR / "knowledge" / "sync_state.json"

class NajikaClaudeSync:
    """Synchronisiert Najika mit Claude Code"""

    def __init__(self):
        self.previous_state = self.load_previous_state()
        self.current_state = {}
        self.new_files = []
        self.modified_files = []
        self.deleted_files = []

    def load_previous_state(self):
        """Lädt vorherigen Sync-State"""
        if SYNC_STATE.exists():
            try:
                with open(SYNC_STATE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_current_state(self):
        """Speichert aktuellen State"""
        SYNC_STATE.parent.mkdir(parents=True, exist_ok=True)
        with open(SYNC_STATE, 'w', encoding='utf-8') as f:
            json.dump(self.current_state, f, indent=2)

    def get_file_hash(self, file_path):
        """Berechnet Hash einer Datei"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def scan_directory(self, directory):
        """Scannt Verzeichnis nach Dateien"""
        files = {}

        if not directory.exists():
            return files

        # Skip Ordner
        skip_dirs = ['__pycache__', '.git', 'node_modules', '.venv', 'venv', 'knowledge']

        for file_path in directory.rglob('*'):
            if file_path.is_file():
                # Skip
                if any(skip in str(file_path) for skip in skip_dirs):
                    continue

                # Skip große Dateien
                try:
                    if file_path.stat().st_size > 5 * 1024 * 1024:
                        continue
                except:
                    continue

                relative_path = str(file_path.relative_to(directory))
                file_hash = self.get_file_hash(file_path)

                files[relative_path] = {
                    'path': str(file_path),
                    'hash': file_hash,
                    'size': file_path.stat().st_size,
                    'modified': file_path.stat().st_mtime
                }

        return files

    def detect_changes(self):
        """Erkennt Änderungen seit letztem Sync"""
        print("🔍 Scanne NajikaCore...")
        najika_files = self.scan_directory(NAJIKA_DIR)

        print("🔍 Scanne .claude...")
        claude_files = self.scan_directory(CLAUDE_DIR)

        # Merge
        self.current_state = {**najika_files, **claude_files}

        # Vergleiche mit vorherigem State
        for rel_path, file_info in self.current_state.items():
            if rel_path not in self.previous_state:
                # Neue Datei
                self.new_files.append(file_info)
            elif file_info['hash'] != self.previous_state[rel_path].get('hash'):
                # Geänderte Datei
                self.modified_files.append(file_info)

        # Gelöschte Dateien
        for rel_path in self.previous_state:
            if rel_path not in self.current_state:
                self.deleted_files.append(self.previous_state[rel_path])

        print(f"✅ Neue Dateien: {len(self.new_files)}")
        print(f"✅ Geänderte Dateien: {len(self.modified_files)}")
        print(f"✅ Gelöschte Dateien: {len(self.deleted_files)}")

    def generate_claude_update(self):
        """Generiert UPDATE.md für Claude"""
        lines = []

        # Header
        lines.append("# 🔄 NAJIKA → CLAUDE UPDATE")
        lines.append(f"**Generiert:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("Najika hat Änderungen erkannt und bringt dich auf den aktuellen Stand!")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Statistik
        lines.append("## 📊 ÄNDERUNGEN")
        lines.append("")
        lines.append(f"- 🆕 **Neue Dateien:** {len(self.new_files)}")
        lines.append(f"- 📝 **Geänderte Dateien:** {len(self.modified_files)}")
        lines.append(f"- 🗑️  **Gelöschte Dateien:** {len(self.deleted_files)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Neue Dateien
        if self.new_files:
            lines.append("## 🆕 NEUE DATEIEN")
            lines.append("")
            for file_info in self.new_files[:20]:  # Max 20
                path = Path(file_info['path'])
                lines.append(f"### `{path.name}`")
                lines.append(f"**Pfad:** `{file_info['path']}`")
                lines.append(f"**Größe:** {file_info['size']} bytes")
                lines.append("")

                # Preview für kleine Dateien
                if file_info['size'] < 10000:
                    try:
                        content = Path(file_info['path']).read_text(encoding='utf-8')
                        lines.append("**Inhalt:**")
                        lines.append(f"```{path.suffix.replace('.', '')}")
                        lines.append(content[:500])
                        if len(content) > 500:
                            lines.append("\n... (gekürzt)")
                        lines.append("```")
                        lines.append("")
                    except:
                        pass

            if len(self.new_files) > 20:
                lines.append(f"... und {len(self.new_files) - 20} weitere neue Dateien")
                lines.append("")

            lines.append("---")
            lines.append("")

        # Geänderte Dateien
        if self.modified_files:
            lines.append("## 📝 GEÄNDERTE DATEIEN")
            lines.append("")
            for file_info in self.modified_files[:10]:  # Max 10
                path = Path(file_info['path'])
                lines.append(f"- `{path.name}` ({file_info['path']})")

            if len(self.modified_files) > 10:
                lines.append(f"- ... und {len(self.modified_files) - 10} weitere")

            lines.append("")
            lines.append("---")
            lines.append("")

        # Gelöschte Dateien
        if self.deleted_files:
            lines.append("## 🗑️ GELÖSCHTE DATEIEN")
            lines.append("")
            for file_info in self.deleted_files[:10]:
                lines.append(f"- `{file_info['path']}`")

            if len(self.deleted_files) > 10:
                lines.append(f"- ... und {len(self.deleted_files) - 10} weitere")

            lines.append("")
            lines.append("---")
            lines.append("")

        # Zusammenfassung
        lines.append("## 🎯 ZUSAMMENFASSUNG")
        lines.append("")

        if not self.new_files and not self.modified_files and not self.deleted_files:
            lines.append("✅ **Keine Änderungen seit letztem Sync!**")
            lines.append("")
            lines.append("Alles ist auf dem aktuellen Stand.")
        else:
            lines.append("**Wichtigste Änderungen:**")
            lines.append("")

            # Top 5 neue Dateien
            if self.new_files:
                lines.append("**Neue wichtige Dateien:**")
                for file_info in sorted(self.new_files, key=lambda x: x['size'], reverse=True)[:5]:
                    path = Path(file_info['path'])
                    lines.append(f"  - `{path.name}` ({file_info['size']} bytes)")
                lines.append("")

            # Empfehlung
            lines.append("**Empfohlene Aktionen:**")
            if self.new_files:
                lines.append("  1. Prüfe neue Dateien auf Relevanz")
            if self.modified_files:
                lines.append("  2. Review geänderte Dateien")
            if self.deleted_files:
                lines.append("  3. Beachte gelöschte Abhängigkeiten")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("✨ **Generiert von Najika's Auto-Sync System** ✨")
        lines.append("")
        lines.append("_Nächster Sync: Automatisch bei Najika-Start oder manuell mit `python najika_sync.py`_")

        # Speichere
        UPDATE_FILE.write_text('\n'.join(lines), encoding='utf-8')
        print(f"📄 UPDATE.md erstellt: {UPDATE_FILE}")

    def sync(self):
        """Führt kompletten Sync durch"""
        print()
        print("=" * 70)
        print("NAJIKA <-> CLAUDE CODE SYNC")
        print("=" * 70)
        print()

        # Erkenne Änderungen
        self.detect_changes()

        # Generiere Update für Claude
        self.generate_claude_update()

        # Speichere State
        self.save_current_state()

        print()
        print("=" * 70)
        print("SYNC ABGESCHLOSSEN")
        print("=" * 70)
        print()
        print(f"📄 Update für Claude: {UPDATE_FILE}")
        print()
        print("Nächster Schritt:")
        print("  In Claude Code: Lies CLAUDE_UPDATE.md")
        print()


def main():
    """Main entry point"""
    syncer = NajikaClaudeSync()
    syncer.sync()


if __name__ == "__main__":
    main()
