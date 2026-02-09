#!/usr/bin/env python3
"""
NAJIKA KNOWLEDGE SCANNER V2
Scannt ALLE Dokumente in Najika_World und vergleicht mit ChromaDB
Findet vergessene/ungenutzte Ressourcen
"""

import os
import glob
import hashlib
from pathlib import Path
from datetime import datetime

# Pfade
PROJECT_ROOT = "C:/Najika_World"
MEMORY_DB = "C:/Najika_World/memory_db"

# Unterstützte Dateitypen
SUPPORTED_EXTENSIONS = ['.md', '.txt', '.json', '.pdf']

# Ordner die übersprungen werden (node_modules, .git, etc.)
SKIP_DIRS = [
    'node_modules', '.git', '__pycache__', '.vscode',
    'venv', 'env', '.next', 'dist', 'build', '.cache'
]

class NajikaKnowledgeScanner:
    def __init__(self):
        self.all_files = []
        self.by_type = {ext: [] for ext in SUPPORTED_EXTENSIONS}
        self.important_docs = []
        self.forgotten_docs = []

    def scan_all(self):
        """Scannt alle Dokumente"""
        print("=" * 60)
        print("[SCAN] NAJIKA KNOWLEDGE SCANNER V2")
        print("=" * 60)
        print(f"\nScanne: {PROJECT_ROOT}")
        print()

        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Skip unwichtige Ordner
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

            for file in files:
                ext = Path(file).suffix.lower()
                if ext in SUPPORTED_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, PROJECT_ROOT)

                    self.all_files.append(rel_path)
                    self.by_type[ext].append(rel_path)

                    # Wichtige Docs erkennen
                    lower_file = file.lower()
                    if any(kw in lower_file for kw in [
                        'zusammenfassung', 'master', 'final', 'komplett',
                        'ultimativ', 'uebersicht', 'overview', 'claude',
                        'roadmap', 'todo', 'wichtig', 'gebot'
                    ]):
                        self.important_docs.append(rel_path)

        return self

    def print_stats(self):
        """Zeigt Statistiken"""
        print("\n[STATS] STATISTIKEN")
        print("-" * 40)
        print(f"Gesamt gefunden: {len(self.all_files)}")
        print()
        for ext, files in self.by_type.items():
            print(f"  {ext}: {len(files)}")
        print()
        print(f"Wichtige Docs erkannt: {len(self.important_docs)}")

        return self

    def find_forgotten(self):
        """Findet vergessene wichtige Dokumente"""
        print("\n[SEARCH] VERGESSENE/UNGENUTZTE RESSOURCEN")
        print("-" * 40)

        # Ordner die oft übersehen werden
        forgotten_paths = []

        for file in self.all_files:
            path_lower = file.lower()

            # Dokumente in "alles wissen" Ordner
            if 'alles wissen' in path_lower:
                forgotten_paths.append(file)

            # Dokumente in "aasd" Ordner (oft übersehen)
            if 'aasd' in path_lower:
                forgotten_paths.append(file)

            # Archive die wichtig sein könnten
            if 'archiv' in path_lower and any(kw in path_lower for kw in ['design', 'code', 'training']):
                forgotten_paths.append(file)

        self.forgotten_docs = list(set(forgotten_paths))

        print(f"Gefunden: {len(self.forgotten_docs)} potenziell vergessene Dokumente")
        print()

        # Gruppiere nach Ordner
        folders = {}
        for doc in self.forgotten_docs[:50]:
            folder = os.path.dirname(doc) or "ROOT"
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(os.path.basename(doc))

        for folder, files in sorted(folders.items())[:10]:
            print(f"\n[FOLDER] {folder}:")
            for f in files[:5]:
                print(f"   - {f}")
            if len(files) > 5:
                print(f"   ... und {len(files) - 5} weitere")

        return self

    def list_important_not_in_chromadb(self):
        """Listet wichtige Docs die vermutlich nicht in ChromaDB sind"""
        print("\n[IMPORTANT] WICHTIGE DOCS ZUM PRUEFEN")
        print("-" * 40)

        # Root-Level wichtige Docs
        root_docs = [f for f in self.important_docs if '/' not in f and '\\' not in f]

        print("\n[ROOT] Root-Level Wichtige Dokumente:")
        for doc in sorted(root_docs)[:20]:
            print(f"   - {doc}")

        return self

    def save_report(self):
        """Speichert Bericht"""
        report_path = os.path.join(PROJECT_ROOT, "KNOWLEDGE_SCAN_REPORT.md")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🔍 NAJIKA KNOWLEDGE SCAN REPORT\n\n")
            f.write(f"**Scan-Datum:** {datetime.now().isoformat()}\n\n")

            f.write("## 📊 Statistiken\n\n")
            f.write(f"- **Gesamt:** {len(self.all_files)} Dateien\n")
            for ext, files in self.by_type.items():
                f.write(f"- **{ext}:** {len(files)}\n")
            f.write(f"- **Wichtige Docs:** {len(self.important_docs)}\n")
            f.write(f"- **Potenziell vergessen:** {len(self.forgotten_docs)}\n\n")

            f.write("## ⚠️ Wichtige Dokumente\n\n")
            for doc in sorted(self.important_docs)[:50]:
                f.write(f"- `{doc}`\n")

            f.write("\n## 🔎 Potenziell vergessene Ressourcen\n\n")
            for doc in sorted(self.forgotten_docs)[:100]:
                f.write(f"- `{doc}`\n")

        print(f"\n[OK] Report gespeichert: {report_path}")
        return report_path


def main():
    scanner = NajikaKnowledgeScanner()
    scanner.scan_all()
    scanner.print_stats()
    scanner.find_forgotten()
    scanner.list_important_not_in_chromadb()
    scanner.save_report()

    print("\n" + "=" * 60)
    print("[OK] SCAN ABGESCHLOSSEN!")
    print("=" * 60)
    print("\nNächster Schritt:")
    print("1. Report prüfen: KNOWLEDGE_SCAN_REPORT.md")
    print("2. Fehlende Docs importieren mit najika_import_missing.py")


if __name__ == "__main__":
    main()
