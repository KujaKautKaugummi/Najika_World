#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA PERSONALITY IMPORTER
Importiert Text-Dateien als Persönlichkeits-Daten

VERWENDUNG:
1. Lege .txt Dateien in C:/NajikaCore/personality_sources/
2. Benenne sie: CATEGORY_description.txt
   z.B.: SAKURA_beispiel1.txt, HARLEY_witzig.txt
3. Führe dieses Script aus oder nutze IMPORT_PERSONALITIES.bat

Format der TXT-Dateien:
- Einfacher Text
- Dialoge OK
- Transkripte OK
- Beschreibungen OK
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import glob
from datetime import datetime
from najika_memory import NajikaMemory

class PersonalityImporter:
    """Importiert Text-Dateien als Personality-Daten"""

    def __init__(
        self,
        source_dir="C:/NajikaCore/personality_sources",
        import_log="C:/NajikaCore/personality_import_log.json"
    ):
        self.source_dir = source_dir
        self.import_log_file = import_log

        # Erstelle Ordner falls nicht vorhanden
        os.makedirs(source_dir, exist_ok=True)

        # Memory System
        self.memory = NajikaMemory()
        self.personalities = self.memory.client.get_collection("najika_personalities")

        # Import-Log
        import json
        if os.path.exists(import_log):
            with open(import_log, 'r', encoding='utf-8') as f:
                self.import_log = json.load(f)
        else:
            self.import_log = {"imported_files": []}

        print("=" * 60)
        print("NAJIKA PERSONALITY IMPORTER")
        print("=" * 60)
        print(f"Quell-Ordner: {source_dir}")
        print()

    def find_new_files(self):
        """Findet neue TXT-Dateien"""
        pattern = os.path.join(self.source_dir, "**", "*.txt")
        all_files = glob.glob(pattern, recursive=True)

        # Filter bereits importierte
        new_files = [
            f for f in all_files
            if f not in self.import_log['imported_files']
        ]

        print(f"Gefundene Dateien: {len(all_files)}")
        print(f"Neue Dateien: {len(new_files)}")
        print()

        return new_files

    def extract_category(self, filename):
        """Extrahiert Kategorie aus Dateinamen"""
        basename = os.path.basename(filename)

        # Format: CATEGORY_description.txt
        if '_' in basename:
            category = basename.split('_')[0].upper()
        else:
            category = "UNKNOWN"

        return category

    def import_file(self, filepath):
        """Importiert eine einzelne Datei"""
        print(f"📥 {os.path.basename(filepath)}")

        try:
            # Lese Datei mit verschiedenen Encodings
            text = None
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        text = f.read()
                    break
                except UnicodeDecodeError:
                    continue

            if not text:
                print("   ❌ Encoding-Fehler")
                return False

            # Extrahiere Kategorie
            category = self.extract_category(filepath)

            # Speichere in ChromaDB
            doc_id = f"{category}_{os.path.basename(filepath)}_{datetime.now().timestamp()}"

            self.personalities.add(
                ids=[doc_id],
                documents=[text],
                metadatas=[{
                    'source': category,
                    'filename': os.path.basename(filepath),
                    'imported_at': datetime.now().isoformat()
                }]
            )

            # Update Log
            self.import_log['imported_files'].append(filepath)

            print(f"   ✅ Kategorie: {category}")
            return True

        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            return False

    def import_all(self):
        """Importiert alle neuen Dateien"""
        print("🚀 Starte Import...\n")

        new_files = self.find_new_files()

        if not new_files:
            print("✅ Keine neuen Dateien!")
            return

        success_count = 0

        for filepath in new_files:
            if self.import_file(filepath):
                success_count += 1
            print()

        # Speichere Log
        import json
        with open(self.import_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.import_log, f, indent=2, ensure_ascii=False)

        print("=" * 60)
        print("✅ IMPORT ABGESCHLOSSEN!")
        print("=" * 60)
        print(f"Importiert: {success_count}/{len(new_files)}")
        print()


if __name__ == "__main__":
    importer = PersonalityImporter()
    importer.import_all()
