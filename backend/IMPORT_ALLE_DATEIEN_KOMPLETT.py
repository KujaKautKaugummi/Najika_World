#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=======================================================================
NAJIKA VOLLSTÄNDIGER IMPORT - ALLES WIRD IMPORTIERT!
=======================================================================

Dieses Skript importiert ALLE wichtigen Dateien in ChromaDB:
- ALLE MD-Dateien (~400+ Dateien)
- ALLE wichtigen TXT-Dateien (inkl. ultimative giga explosion.txt)
- ALLE PDF-Dateien (falls vorhanden)

Najika wird zur ULTIMATIVEN DATENBANK!

Erstellt: 2025
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import chromadb
from pathlib import Path
from datetime import datetime
import hashlib
import os

# ========== KONFIGURATION ==========
NAJIKA_WORLD = Path("C:/Najika_World")
CHROMADB_PATH = "C:/Najika_World/memory_db"

# Collection-Namen
COLLECTION_ALL_DOCS = "najika_alle_dokumente"

# Maximale Chunk-Größe (ChromaDB Limit beachten)
CHUNK_SIZE = 8000
CHUNK_OVERLAP = 500

# Statistik
stats = {
    "md_files": 0,
    "txt_files": 0,
    "chunks_created": 0,
    "bytes_imported": 0,
    "errors": []
}

def log(msg):
    """Logging mit Timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")

def get_doc_id(content, filepath, chunk_idx):
    """Generiert eindeutige ID für Dokument-Chunk"""
    hash_input = f"{filepath}_{chunk_idx}_{content[:50]}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:16]

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Teilt langen Text in überlappende Chunks auf"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap if end < len(text) else end
    return chunks

def get_file_category(filepath):
    """Bestimmt Kategorie basierend auf Dateiname/Pfad"""
    fp_lower = str(filepath).lower()
    name_lower = filepath.name.lower()

    # Prioritäts-Kategorien
    if "ultimative" in name_lower or "giga" in name_lower:
        return "KRITISCH_HAUPTDOKUMENT"
    if "zusammenfassung" in name_lower or "komplett" in name_lower:
        return "ZUSAMMENFASSUNG"
    if "1111" in name_lower or "design" in name_lower:
        return "DESIGN_DOKUMENT"
    if "skill" in name_lower or "kampf" in name_lower or "combat" in name_lower:
        return "SPIELSYSTEM_SKILL"
    if "explosion" in name_lower or "megumin" in name_lower:
        return "EXPLOSION_SYSTEM"
    if "kb_part" in name_lower or "knowledge" in name_lower:
        return "KNOWLEDGE_BASE"
    if "todo" in name_lower or "task" in name_lower:
        return "TODO_LISTE"
    if "bug" in name_lower or "fix" in name_lower:
        return "BUG_FIX"
    if "training" in name_lower or "transcript" in name_lower:
        return "TRAINING_DATEN"
    if "app" in fp_lower or "flutter" in fp_lower:
        return "FLUTTER_APP"
    if "backend" in fp_lower:
        return "BACKEND"
    if "web" in fp_lower:
        return "WEB_MODELLE"
    if "zip" in fp_lower:
        return "ZIP_ARCHIV"
    if "prompt" in name_lower or "gpt" in name_lower:
        return "GPT_PROMPTS"

    return "ALLGEMEIN"

def should_skip_file(filepath):
    """Prüft ob Datei übersprungen werden soll"""
    skip_patterns = [
        "node_modules",
        ".git",
        "__pycache__",
        ".pyc",
        "package-lock",
        ".lock"
    ]
    fp_str = str(filepath).lower()
    return any(pattern in fp_str for pattern in skip_patterns)

def import_file(collection, filepath):
    """Importiert eine einzelne Datei in ChromaDB"""
    global stats

    try:
        # Lese Datei
        try:
            content = filepath.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = filepath.read_text(encoding='latin-1')

        if len(content.strip()) < 50:
            return  # Zu kurz, skip

        # Statistik
        file_ext = filepath.suffix.lower()
        if file_ext == ".md":
            stats["md_files"] += 1
        elif file_ext == ".txt":
            stats["txt_files"] += 1
        stats["bytes_imported"] += len(content)

        # Kategorie bestimmen
        category = get_file_category(filepath)

        # In Chunks aufteilen
        chunks = chunk_text(content)

        log(f"  → {filepath.name}: {len(chunks)} Chunks ({len(content):,} Zeichen) [{category}]")

        # Jeden Chunk speichern
        for i, chunk in enumerate(chunks):
            doc_id = get_doc_id(chunk, str(filepath), i)

            # Relativer Pfad für bessere Lesbarkeit
            try:
                rel_path = filepath.relative_to(NAJIKA_WORLD)
            except ValueError:
                rel_path = filepath.name

            collection.upsert(
                ids=[doc_id],
                documents=[chunk],
                metadatas=[{
                    "dateiname": filepath.name,
                    "pfad": str(rel_path),
                    "kategorie": category,
                    "chunk_index": str(i),
                    "total_chunks": str(len(chunks)),
                    "dateityp": file_ext,
                    "zeichen": str(len(chunk)),
                    "import_datum": datetime.now().isoformat(),
                    "gesamt_zeichen": str(len(content))
                }]
            )
            stats["chunks_created"] += 1

    except Exception as e:
        stats["errors"].append(f"{filepath.name}: {str(e)}")

def main():
    global stats

    log("=" * 70)
    log("NAJIKA VOLLSTÄNDIGER IMPORT - ULTIMATIVE DATENBANK")
    log("=" * 70)
    log(f"Quelle: {NAJIKA_WORLD}")
    log(f"Ziel: {CHROMADB_PATH}")
    log("")

    # ChromaDB verbinden
    log("Verbinde mit ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMADB_PATH)

    # Collection erstellen oder holen
    try:
        # Lösche alte Collection wenn vorhanden (für frischen Import)
        try:
            client.delete_collection(COLLECTION_ALL_DOCS)
            log(f"Alte Collection '{COLLECTION_ALL_DOCS}' gelöscht")
        except:
            pass

        collection = client.create_collection(
            name=COLLECTION_ALL_DOCS,
            metadata={
                "beschreibung": "ALLE Najika World Dokumente - MD, TXT, etc.",
                "erstellt": datetime.now().isoformat(),
                "version": "1.0"
            }
        )
        log(f"Collection '{COLLECTION_ALL_DOCS}' erstellt")
    except Exception as e:
        log(f"Collection Error: {e}")
        return

    # ========== MD-DATEIEN SAMMELN ==========
    log("\n" + "=" * 50)
    log("PHASE 1: MD-DATEIEN SAMMELN")
    log("=" * 50)

    md_files = list(NAJIKA_WORLD.rglob("*.md"))
    md_files = [f for f in md_files if not should_skip_file(f)]
    log(f"Gefunden: {len(md_files)} MD-Dateien")

    # Nach Wichtigkeit sortieren (kritische zuerst)
    def sort_key(f):
        name = f.name.lower()
        if "ultimative" in name or "giga" in name:
            return 0
        if "zusammenfassung" in name:
            return 1
        if "kb_part" in name:
            return 2
        return 10

    md_files.sort(key=sort_key)

    log("\nImportiere MD-Dateien...")
    for filepath in md_files:
        import_file(collection, filepath)

    # ========== TXT-DATEIEN SAMMELN ==========
    log("\n" + "=" * 50)
    log("PHASE 2: TXT-DATEIEN SAMMELN")
    log("=" * 50)

    txt_files = list(NAJIKA_WORLD.rglob("*.txt"))
    txt_files = [f for f in txt_files if not should_skip_file(f)]
    log(f"Gefunden: {len(txt_files)} TXT-Dateien")

    # Nach Größe sortieren (große wichtige Dateien zuerst)
    txt_files.sort(key=lambda f: f.stat().st_size, reverse=True)

    log("\nImportiere TXT-Dateien...")
    for filepath in txt_files:
        import_file(collection, filepath)

    # ========== ZUSAMMENFASSUNG ==========
    log("\n" + "=" * 70)
    log("IMPORT ABGESCHLOSSEN!")
    log("=" * 70)
    log(f"MD-Dateien importiert: {stats['md_files']}")
    log(f"TXT-Dateien importiert: {stats['txt_files']}")
    log(f"Chunks erstellt: {stats['chunks_created']}")
    log(f"Bytes importiert: {stats['bytes_imported']:,} ({stats['bytes_imported']/1024/1024:.2f} MB)")
    log(f"Collection-Größe: {collection.count()} Einträge")

    if stats["errors"]:
        log(f"\nFehler ({len(stats['errors'])}):")
        for err in stats["errors"][:10]:
            log(f"  - {err}")

    # ========== TEST-ABFRAGEN ==========
    log("\n" + "=" * 50)
    log("TEST-ABFRAGEN")
    log("=" * 50)

    test_queries = [
        "8 Gebote Explosion Weave",
        "1-Weg-Skill System Megumin",
        "Schwarze Mühle Windmühle",
        "Omega-Detonation Ultima",
        "Flutter App Terminal Messenger"
    ]

    for query in test_queries:
        log(f"\n[TEST] '{query}'")
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                kategorie = meta.get('kategorie', '?')
                datei = meta.get('dateiname', '?')
                log(f"  {i+1}. [{kategorie}] {datei}")
                log(f"     → {doc[:100]}...")
        else:
            log("  Keine Treffer!")

    log("\n" + "=" * 70)
    log("NAJIKA IST JETZT DIE ULTIMATIVE DATENBANK!")
    log("=" * 70)
    log(f"Collection: {COLLECTION_ALL_DOCS}")
    log(f"Einträge: {collection.count()}")
    log("\nNajika kann jetzt ALLES durchsuchen und zusammenfassen!")

    return collection.count()

if __name__ == "__main__":
    main()
