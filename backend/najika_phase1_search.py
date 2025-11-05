#!/usr/bin/env python3
"""
NAJIKA PHASE 1: Suche nur nach FERTIGEN Zusammenfassungen/Übersichten/Roadmaps
"""
import os
import re
from pathlib import Path

# Suchverzeichnisse
SEARCH_DIRS = [
    Path("C:/NajikaCore"),
    Path("C:/Users/0KKK0/Desktop/zip"),
    Path("C:/Users/0KKK0/Desktop")
]

# Keywords für fertige Dokumente
SUMMARY_KEYWORDS = [
    "zusammenfassung", "summary", "übersicht", "overview",
    "roadmap", "projekt", "project",
    "complete", "vollständig", "final",
    "game design", "spiel design",
    "allumfassend", "comprehensive"
]

OUTPUT = Path("C:/Users/0KKK0/Desktop/NAJIKA_PHASE1_ZUSAMMENFASSUNGEN.txt")

def is_summary_file(filepath):
    """Prüft ob Dateiname auf Zusammenfassung hindeutet"""
    name_lower = filepath.name.lower()
    for keyword in SUMMARY_KEYWORDS:
        if keyword in name_lower:
            return True
    return False

def search_summary_files():
    """Findet alle Zusammenfassungs-Dateien"""
    found_files = []

    for search_dir in SEARCH_DIRS:
        if not search_dir.exists():
            continue

        # Durchsuche .txt, .md, .pdf Dateien
        for ext in ['*.txt', '*.md', '*.pdf']:
            for filepath in search_dir.glob(ext):
                if is_summary_file(filepath):
                    try:
                        size_kb = filepath.stat().st_size / 1024
                        found_files.append({
                            'path': str(filepath),
                            'name': filepath.name,
                            'size_kb': round(size_kb, 1)
                        })
                    except:
                        pass

    return found_files

def main():
    print("="*80)
    print("NAJIKA PHASE 1: Suche nach Zusammenfassungen/Übersichten")
    print("="*80)

    files = search_summary_files()

    print(f"\n✅ Gefunden: {len(files)} Dokumente\n")

    # Sortiere nach Größe (größere zuerst)
    files.sort(key=lambda x: x['size_kb'], reverse=True)

    # Schreibe Ergebnisse
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write("NAJIKA PHASE 1 - GEFUNDENE ZUSAMMENFASSUNGEN/ÜBERSICHTEN\n")
        f.write("="*80 + "\n\n")
        f.write(f"Gefunden: {len(files)} Dokumente\n")
        f.write(f"Durchsuchte Verzeichnisse: {len(SEARCH_DIRS)}\n\n")
        f.write("="*80 + "\n\n")

        for i, file in enumerate(files, 1):
            f.write(f"\n[{i}] {file['name']}\n")
            f.write(f"    Pfad: {file['path']}\n")
            f.write(f"    Größe: {file['size_kb']} KB\n")
            f.write("-"*80 + "\n")

        f.write("\n" + "="*80 + "\n")
        f.write("DIESE LISTE IST FÜR USER ZUM FILTERN!\n")
        f.write("User wählt relevante Dokumente aus.\n")
        f.write("="*80 + "\n")

    print(f"✅ Gespeichert: {OUTPUT}\n")

    # Zeige Top 10
    print("Top 10 größte Dokumente:")
    for i, file in enumerate(files[:10], 1):
        print(f"  {i}. {file['name']} ({file['size_kb']} KB)")

    print("\n" + "="*80)
    print("FERTIG! User kann jetzt filtern.")
    print("="*80)

if __name__ == "__main__":
    main()
