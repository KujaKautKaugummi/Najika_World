#!/usr/bin/env python3
"""
NAJIKA PROJECT ARCHIVE PROCESSOR
Verarbeitet ALLE Najika-Projekt-Daten vom Desktop
- Extrahiert Codes
- Sammelt Spiel-Ideen
- Findet Konzepte
- Prüft Code auf Funktionalität
- 90 Millionen Zeichen Wissen!
"""
import os
import re
import json
from pathlib import Path
from datetime import datetime
import hashlib

# Pfade
DESKTOP = Path.home() / "Desktop"
SOURCE_DIRS = [
    DESKTOP / "finale",
    DESKTOP / "finalee",
    # Weitere Ordner werden automatisch gefunden
]

BACKEND_DIR = Path(__file__).parent
OUTPUT_DIR = BACKEND_DIR / "najika_project_knowledge"
OUTPUT_DIR.mkdir(exist_ok=True)

# Output Kategorien
CATEGORIES = {
    "code": OUTPUT_DIR / "extracted_code",
    "ideas": OUTPUT_DIR / "game_ideas",
    "concepts": OUTPUT_DIR / "project_concepts",
    "uefn": OUTPUT_DIR / "uefn_code",
    "complete": OUTPUT_DIR / "complete_implementations",
    "incomplete": OUTPUT_DIR / "incomplete_code",
    "notes": OUTPUT_DIR / "development_notes"
}

for cat_dir in CATEGORIES.values():
    cat_dir.mkdir(exist_ok=True)

# Stats
STATS = {
    "total_files": 0,
    "total_chars": 0,
    "code_files": 0,
    "idea_files": 0,
    "errors": 0,
    "extracted_codes": 0,
    "game_concepts": 0
}

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

def find_all_source_dirs():
    """Findet alle Ordner auf Desktop die 'final' enthalten"""
    log("Suche Projekt-Ordner auf Desktop...")
    found = []

    for item in DESKTOP.iterdir():
        if item.is_dir():
            name_lower = item.name.lower()
            if any(keyword in name_lower for keyword in ['final', 'najika', 'projekt', 'zip']):
                found.append(item)
                log(f"  Gefunden: {item.name}")

    return found

def is_code_file(filepath):
    """Prüft ob Datei Code enthält"""
    code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.verse', '.java',
                      '.cpp', '.c', '.cs', '.go', '.rust', '.html', '.css',
                      '.json', '.yaml', '.xml', '.sql', '.sh', '.bat'}
    return filepath.suffix.lower() in code_extensions

def is_idea_file(filepath):
    """Prüft ob Datei Ideen/Konzepte enthält"""
    idea_extensions = {'.md', '.txt', '.doc', '.docx', '.pdf'}
    idea_keywords = ['idea', 'konzept', 'plan', 'design', 'spec', 'todo', 'note']

    if filepath.suffix.lower() in idea_extensions:
        return True

    name_lower = filepath.stem.lower()
    return any(kw in name_lower for kw in idea_keywords)

def extract_code_blocks(content):
    """Extrahiert Code-Blöcke aus Text"""
    # Markdown Code Blocks
    md_pattern = r'```(\w+)?\n(.*?)\n```'
    blocks = re.findall(md_pattern, content, re.DOTALL)

    # Python/JS Function Definitions
    func_pattern = r'(def|function|class)\s+\w+.*?(?=\n(?:def|function|class)|\Z)'
    functions = re.findall(func_pattern, content, re.DOTALL)

    return blocks, functions

def analyze_code_completeness(code):
    """Prüft ob Code vollständig ist"""
    incomplete_markers = [
        '# TODO', '// TODO', 'TODO:',
        '...', 'pass  # TODO',
        'NotImplementedError',
        '# FIXME', '// FIXME',
        '# WIP', '// WIP'
    ]

    for marker in incomplete_markers:
        if marker in code:
            return False, f"Unvollständig: {marker}"

    # Check for basic structure
    has_function = any(kw in code for kw in ['def ', 'function ', 'class '])
    has_body = len(code.strip().split('\n')) > 2

    if not (has_function and has_body):
        return False, "Unvollständig: Keine richtige Struktur"

    return True, "Vollständig"

def extract_game_ideas(content):
    """Extrahiert Spiel-Ideen aus Text"""
    ideas = []

    # Suche nach Listen-Items
    list_pattern = r'^[-*]\s+(.+)$'
    for match in re.finditer(list_pattern, content, re.MULTILINE):
        idea = match.group(1).strip()
        if len(idea) > 10:  # Mindestlänge
            ideas.append(idea)

    # Suche nach Überschriften
    heading_pattern = r'^#+\s+(.+)$'
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        heading = match.group(1).strip()
        ideas.append(f"Konzept: {heading}")

    return ideas

def process_file(filepath):
    """Verarbeitet einzelne Datei"""
    try:
        # Lese Datei
        try:
            content = filepath.read_text(encoding='utf-8')
        except:
            content = filepath.read_text(encoding='latin-1', errors='ignore')

        chars = len(content)
        STATS["total_chars"] += chars

        # Hash für Duplikat-Erkennung
        file_hash = hashlib.md5(content.encode('utf-8', errors='ignore')).hexdigest()

        result = {
            "source_file": str(filepath),
            "hash": file_hash,
            "chars": chars,
            "timestamp": datetime.now().isoformat()
        }

        # CODE DATEI
        if is_code_file(filepath):
            STATS["code_files"] += 1

            # Extrahiere Code-Blöcke
            blocks, functions = extract_code_blocks(content)

            if blocks or functions:
                STATS["extracted_codes"] += 1

                # Prüfe Vollständigkeit
                is_complete, reason = analyze_code_completeness(content)

                result["type"] = "code"
                result["code_blocks"] = len(blocks)
                result["functions"] = len(functions)
                result["complete"] = is_complete
                result["reason"] = reason

                # Speichern
                if is_complete:
                    output_file = CATEGORIES["complete"] / f"{file_hash}.json"
                else:
                    output_file = CATEGORIES["incomplete"] / f"{file_hash}.json"

                # UEFN spezifisch?
                if 'uefn' in filepath.name.lower() or 'verse' in filepath.suffix.lower():
                    output_file = CATEGORIES["uefn"] / f"{file_hash}.json"

            else:
                # Ganzer File ist Code
                output_file = CATEGORIES["code"] / f"{file_hash}.json"

            result["content"] = content[:5000]  # Erste 5000 Zeichen für Index

            output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

        # IDEEN DATEI
        elif is_idea_file(filepath):
            STATS["idea_files"] += 1

            # Extrahiere Ideen
            ideas = extract_game_ideas(content)

            if ideas:
                STATS["game_concepts"] += len(ideas)

                result["type"] = "ideas"
                result["ideas_count"] = len(ideas)
                result["ideas"] = ideas[:50]  # Erste 50 Ideen
                result["content"] = content[:5000]

                output_file = CATEGORIES["ideas"] / f"{file_hash}.json"
                output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

            else:
                # Generelle Notizen
                result["type"] = "notes"
                result["content"] = content[:5000]

                output_file = CATEGORIES["notes"] / f"{file_hash}.json"
                output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

        return True

    except Exception as e:
        STATS["errors"] += 1
        log(f"Fehler bei {filepath.name}: {e}", "ERROR")
        return False

def scan_directory(directory):
    """Scannt Verzeichnis rekursiv"""
    log(f"Scanne: {directory.name}")

    for root, dirs, files in os.walk(directory):
        root_path = Path(root)

        for filename in files:
            filepath = root_path / filename

            # Skip binäre Dateien
            if filepath.suffix.lower() in {'.exe', '.dll', '.so', '.dylib', '.zip', '.tar', '.gz', '.7z'}:
                continue

            STATS["total_files"] += 1

            if STATS["total_files"] % 100 == 0:
                log(f"  Verarbeitet: {STATS['total_files']} Dateien, {STATS['total_chars']:,} Zeichen")

            process_file(filepath)

def create_master_index():
    """Erstellt Master-Index aller Daten"""
    log("\nErstelle Master-Index...")

    index = {
        "created": datetime.now().isoformat(),
        "stats": STATS,
        "categories": {}
    }

    for cat_name, cat_dir in CATEGORIES.items():
        files = list(cat_dir.glob("*.json"))
        index["categories"][cat_name] = {
            "count": len(files),
            "files": [f.stem for f in files[:100]]  # Erste 100 für Index
        }

    master_file = OUTPUT_DIR / "master_index.json"
    master_file.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')

    log(f"[OK] Master-Index: {master_file}")
    return index

def main():
    log("="*80)
    log("NAJIKA PROJECT ARCHIVE PROCESSOR")
    log("="*80)
    log(f"Output: {OUTPUT_DIR}\n")

    # Finde alle Quell-Ordner
    source_dirs = find_all_source_dirs()

    if not source_dirs:
        log("[WARNUNG] Keine Projekt-Ordner auf Desktop gefunden!", "WARN")
        log("Erwartete Ordner: finale, finalee, etc.")
        return

    log(f"\nGefunden: {len(source_dirs)} Ordner\n")

    # Verarbeite alle Ordner
    for source_dir in source_dirs:
        scan_directory(source_dir)

    # Erstelle Index
    index = create_master_index()

    # Finale Stats
    log("\n" + "="*80)
    log("VERARBEITUNG ABGESCHLOSSEN")
    log("="*80)
    log(f"Gesamt Dateien: {STATS['total_files']:,}")
    log(f"Gesamt Zeichen: {STATS['total_chars']:,}")
    log(f"Code-Dateien: {STATS['code_files']}")
    log(f"Ideen-Dateien: {STATS['idea_files']}")
    log(f"Extrahierte Codes: {STATS['extracted_codes']}")
    log(f"Spiel-Konzepte: {STATS['game_concepts']}")
    log(f"Fehler: {STATS['errors']}")

    log(f"\nKATEGORIEN:")
    for cat_name, cat_info in index["categories"].items():
        log(f"  {cat_name}: {cat_info['count']} Dateien")

    log(f"\nDaten bereit für Najika Training!")
    log(f"Location: {OUTPUT_DIR}\n")

if __name__ == "__main__":
    main()
