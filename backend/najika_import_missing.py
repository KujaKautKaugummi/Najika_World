#!/usr/bin/env python3
"""
NAJIKA IMPORT MISSING DOCUMENTS
Importiert vergessene/fehlende Dokumente in ChromaDB
"""

import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# Wichtig: UTF-8 Encoding fuer Windows
sys.stdout.reconfigure(encoding='utf-8')

try:
    import chromadb
except ImportError:
    print("[ERROR] chromadb nicht installiert! pip install chromadb")
    sys.exit(1)

# Pfade
PROJECT_ROOT = "C:/Najika_World"
MEMORY_DB = "C:/Najika_World/memory_db"

# Ordner mit vergessenen Dokumenten
FORGOTTEN_FOLDERS = [
    "alles wissen",
    "aasd",
    "entwicklung",
]

# Wichtige Root-Dateien
IMPORTANT_ROOT_FILES = [
    "NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md",
    "00_FINALE_KOMPLETT_UEBERSICHT_V7.md",
    "ALLE_UEBERSICHTEN_GESAMMELT.md",
    "CLAUDE_CODE_CLI_NAJIKA_VOLLSTAENDIGE_ANWEISUNG.md",
    "CLAUDE_ULTIMATIVE_UEBERSICHT_2026-01-27.md",
    "GAME_SYSTEMS_COMPLETE_OVERVIEW.md",
    "MASTER_TODO_TEAM.md",
    "SLIME_SYSTEM_V3_DOKUMENTATION.md",
]


class NajikaImportMissing:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=MEMORY_DB)

        # Hole oder erstelle Collection
        try:
            self.collection = self.client.get_or_create_collection(
                name="najika_complete_knowledge",
                metadata={"description": "Komplett-Wissen aus allen Dokumenten"}
            )
        except Exception as e:
            print(f"[ERROR] Collection Fehler: {e}")
            raise

        self.imported = 0
        self.skipped = 0
        self.errors = 0

    def _hash_content(self, content):
        """Erstellt Hash fuer Duplikat-Erkennung"""
        return hashlib.md5(content.encode('utf-8', errors='ignore')).hexdigest()

    def _chunk_text(self, text, chunk_size=4000, overlap=200):
        """Teilt Text in Chunks"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk)
            start = end - overlap
        return chunks if chunks else [text]

    def import_file(self, filepath):
        """Importiert eine einzelne Datei"""
        try:
            # Lese Datei
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if not content.strip():
                return False

            # Relative Pfad
            rel_path = os.path.relpath(filepath, PROJECT_ROOT)
            filename = os.path.basename(filepath)

            # Kategorisiere
            kategorie = self._categorize_file(rel_path, filename)

            # Teile in Chunks
            chunks = self._chunk_text(content)

            for i, chunk in enumerate(chunks):
                chunk_id = f"{self._hash_content(filepath)}_{i}"

                # Pruefe ob schon existiert
                existing = self.collection.get(ids=[chunk_id])
                if existing and existing['ids']:
                    self.skipped += 1
                    continue

                # Importiere
                self.collection.add(
                    ids=[chunk_id],
                    documents=[chunk],
                    metadatas=[{
                        "source": rel_path,
                        "filename": filename,
                        "kategorie": kategorie,
                        "chunk_index": str(i),
                        "total_chunks": str(len(chunks)),
                        "import_datum": datetime.now().isoformat(),
                        "zeichen": str(len(chunk))
                    }]
                )
                self.imported += 1

            return True

        except Exception as e:
            print(f"[ERROR] {filepath}: {e}")
            self.errors += 1
            return False

    def _categorize_file(self, rel_path, filename):
        """Kategorisiert Datei nach Inhalt/Pfad"""
        path_lower = rel_path.lower()
        name_lower = filename.lower()

        if any(kw in name_lower for kw in ['zusammenfassung', 'overview', 'uebersicht']):
            return "ZUSAMMENFASSUNG"
        elif any(kw in name_lower for kw in ['claude', 'handoff', 'team']):
            return "CLAUDE_ANWEISUNG"
        elif any(kw in name_lower for kw in ['slime', 'companion', 'digimon']):
            return "GAME_SYSTEM_SLIME"
        elif any(kw in name_lower for kw in ['combat', 'battle', 'fight']):
            return "GAME_SYSTEM_COMBAT"
        elif any(kw in name_lower for kw in ['training', 'lora']):
            return "KI_TRAINING"
        elif any(kw in name_lower for kw in ['design', 'konzept', 'spec']):
            return "DESIGN_DOKUMENT"
        elif 'alles wissen' in path_lower:
            return "ARCHIV_WISSEN"
        elif 'entwicklung' in path_lower:
            return "ENTWICKLUNG"
        elif '.pdf' in name_lower:
            return "PDF_DOKUMENT"
        else:
            return "ALLGEMEIN"

    def import_forgotten_folders(self):
        """Importiert alle vergessenen Ordner"""
        print("=" * 60)
        print("[IMPORT] NAJIKA IMPORT MISSING DOCUMENTS")
        print("=" * 60)

        for folder in FORGOTTEN_FOLDERS:
            folder_path = os.path.join(PROJECT_ROOT, folder)
            if not os.path.exists(folder_path):
                print(f"[SKIP] Ordner nicht gefunden: {folder}")
                continue

            print(f"\n[SCAN] {folder}")

            for root, dirs, files in os.walk(folder_path):
                # Skip node_modules, .git etc.
                dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]

                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext in ['.md', '.txt', '.json']:
                        filepath = os.path.join(root, file)
                        self.import_file(filepath)

        return self

    def import_root_important(self):
        """Importiert wichtige Root-Dateien"""
        print("\n[IMPORT] Wichtige Root-Dateien")

        for filename in IMPORTANT_ROOT_FILES:
            filepath = os.path.join(PROJECT_ROOT, filename)
            if os.path.exists(filepath):
                if self.import_file(filepath):
                    print(f"  [OK] {filename}")
                else:
                    print(f"  [SKIP] {filename} (leer oder Fehler)")
            else:
                print(f"  [MISS] {filename} nicht gefunden")

        return self

    def import_all_root_md(self):
        """Importiert ALLE .md Dateien im Root"""
        print("\n[IMPORT] Alle Root MD-Dateien")

        for item in os.listdir(PROJECT_ROOT):
            if item.endswith('.md'):
                filepath = os.path.join(PROJECT_ROOT, item)
                self.import_file(filepath)

        return self

    def print_summary(self):
        """Zeigt Zusammenfassung"""
        print("\n" + "=" * 60)
        print("[SUMMARY] IMPORT ABGESCHLOSSEN")
        print("=" * 60)
        print(f"  Importiert: {self.imported} Chunks")
        print(f"  Uebersprungen: {self.skipped} (existieren bereits)")
        print(f"  Fehler: {self.errors}")
        print(f"\n  Collection 'najika_complete_knowledge': {self.collection.count()} Eintraege")

        return self


def main():
    print("\nNajika Import Missing Documents")
    print("================================\n")

    importer = NajikaImportMissing()

    # 1. Importiere wichtige Root-Dateien
    importer.import_root_important()

    # 2. Importiere alle Root MDs
    importer.import_all_root_md()

    # 3. Importiere vergessene Ordner
    importer.import_forgotten_folders()

    # 4. Zusammenfassung
    importer.print_summary()

    print("\n[OK] Import abgeschlossen!")
    print("Najika hat jetzt mehr Wissen!\n")


if __name__ == "__main__":
    main()
