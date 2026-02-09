#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=======================================================================
NAJIKA WICHTIGE DATEIEN IMPORT - NUR DIE WIRKLICH RELEVANTEN!
=======================================================================

Importiert nur die WICHTIGEN Dateien:
- Hauptordner (C:/Najika_World) MD-Dateien
- Wichtige Unterordner (zip, wissen, finale)
- Die kritischen TXT-Dateien (ultimative giga explosion!)

KEINE:
- node_modules
- Tausende README-Duplikate
- Externe Framework-Dokumentation

Erstellt: 2025
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import chromadb
from pathlib import Path
from datetime import datetime
import hashlib

# ========== KONFIGURATION ==========
NAJIKA_WORLD = Path("C:/Najika_World")
CHROMADB_PATH = "C:/Najika_World/memory_db"
COLLECTION_NAME = "najika_wichtige_docs"

CHUNK_SIZE = 8000
CHUNK_OVERLAP = 500

# WICHTIGE ORDNER - nur diese durchsuchen!
WICHTIGE_ORDNER = [
    NAJIKA_WORLD,                          # Hauptordner (direkt)
    NAJIKA_WORLD / "zip",                  # ZIP-Archiv mit wichtigen Dokumenten
    NAJIKA_WORLD / "wissen",               # Wissens-Ordner
    NAJIKA_WORLD / "finale",               # Finale Dokumente
    NAJIKA_WORLD / "web modelle",          # Web-Modelle Knowledge Base
    NAJIKA_WORLD / "backend",              # Backend-Dokumentation (ohne node_modules)
    NAJIKA_WORLD / "digivice",             # Digivice-Dokumentation
    NAJIKA_WORLD / "app",                  # Flutter App
]

# SPEZIFISCH WICHTIGE DATEIEN (immer importieren!)
KRITISCHE_DATEIEN = [
    NAJIKA_WORLD / "zip" / "ultimative giga explosion.txt",
    NAJIKA_WORLD / "NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md",
    NAJIKA_WORLD / "CLAUDE.md",
    NAJIKA_WORLD / "MASTER_TODO_TEAM.md",
]

# SKIP PATTERNS
SKIP_PATTERNS = [
    "node_modules",
    ".git",
    "__pycache__",
    "package-lock",
    ".lock",
    "android",   # Android build files
    "ios",       # iOS build files
    "build",
    "dist",
]

stats = {
    "files_imported": 0,
    "chunks_created": 0,
    "bytes_imported": 0,
    "skipped": 0,
    "errors": []
}

def log(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")

def get_doc_id(content, filepath, chunk_idx):
    hash_input = f"{filepath}_{chunk_idx}_{content[:50]}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:16]

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
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

def should_skip(filepath):
    fp_str = str(filepath).lower()
    return any(pattern in fp_str for pattern in SKIP_PATTERNS)

def get_category(filepath):
    fp_lower = str(filepath).lower()
    name_lower = filepath.name.lower()

    if "ultimative" in name_lower or "giga" in name_lower:
        return "KRITISCH_HAUPTDOKUMENT"
    if "zusammenfassung" in name_lower:
        return "ZUSAMMENFASSUNG"
    if "skill" in name_lower or "kampf" in name_lower:
        return "SPIELSYSTEM"
    if "explosion" in name_lower:
        return "EXPLOSION_SYSTEM"
    if "kb_part" in name_lower:
        return "KNOWLEDGE_BASE"
    if "todo" in name_lower:
        return "TODO"
    if "bug" in name_lower or "fix" in name_lower:
        return "BUG_FIX"
    if "training" in name_lower:
        return "TRAINING"
    if "web" in fp_lower:
        return "WEB_MODELLE"
    if "zip" in fp_lower:
        return "ZIP_ARCHIV"
    if "wissen" in fp_lower:
        return "WISSEN"

    return "ALLGEMEIN"

def import_file(collection, filepath):
    global stats

    try:
        try:
            content = filepath.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = filepath.read_text(encoding='latin-1')

        if len(content.strip()) < 50:
            stats["skipped"] += 1
            return

        category = get_category(filepath)
        chunks = chunk_text(content)

        log(f"  → {filepath.name}: {len(chunks)} Chunks ({len(content):,} Zeichen) [{category}]")

        for i, chunk in enumerate(chunks):
            doc_id = get_doc_id(chunk, str(filepath), i)

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
                    "zeichen": str(len(chunk)),
                    "import_datum": datetime.now().isoformat()
                }]
            )
            stats["chunks_created"] += 1

        stats["files_imported"] += 1
        stats["bytes_imported"] += len(content)

    except Exception as e:
        stats["errors"].append(f"{filepath.name}: {str(e)}")

def main():
    global stats

    log("=" * 70)
    log("NAJIKA WICHTIGE DATEIEN IMPORT")
    log("=" * 70)

    # ChromaDB verbinden
    log("Verbinde mit ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMADB_PATH)

    # Alte Collection löschen falls vorhanden
    try:
        client.delete_collection(COLLECTION_NAME)
        log(f"Alte Collection '{COLLECTION_NAME}' gelöscht")
    except:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"beschreibung": "Nur WICHTIGE Najika-Dokumente (keine Duplikate)"}
    )
    log(f"Collection '{COLLECTION_NAME}' erstellt")

    # ========== KRITISCHE DATEIEN ZUERST ==========
    log("\n" + "=" * 50)
    log("PHASE 1: KRITISCHE DATEIEN")
    log("=" * 50)

    for filepath in KRITISCHE_DATEIEN:
        if filepath.exists():
            import_file(collection, filepath)
        else:
            log(f"  [SKIP] Nicht gefunden: {filepath.name}")

    # ========== WICHTIGE ORDNER DURCHSUCHEN ==========
    log("\n" + "=" * 50)
    log("PHASE 2: WICHTIGE ORDNER")
    log("=" * 50)

    already_imported = set()

    for ordner in WICHTIGE_ORDNER:
        if not ordner.exists():
            log(f"[SKIP] Ordner nicht gefunden: {ordner}")
            continue

        log(f"\n📁 {ordner.name}:")

        # Nur direkte Kinder, nicht rekursiv (für Hauptordner)
        if ordner == NAJIKA_WORLD:
            # Nur Dateien im Hauptordner, keine Unterordner
            files = [f for f in ordner.iterdir() if f.is_file() and f.suffix.lower() in ['.md', '.txt']]
        else:
            # Rekursiv für wichtige Unterordner
            files = list(ordner.rglob("*.md")) + list(ordner.rglob("*.txt"))

        # Filtern
        files = [f for f in files if not should_skip(f) and str(f) not in already_imported]

        log(f"   Gefunden: {len(files)} Dateien")

        for filepath in sorted(files, key=lambda x: x.stat().st_size, reverse=True):
            if str(filepath) not in already_imported:
                import_file(collection, filepath)
                already_imported.add(str(filepath))

    # ========== ZUSAMMENFASSUNG ==========
    log("\n" + "=" * 70)
    log("IMPORT ABGESCHLOSSEN!")
    log("=" * 70)
    log(f"Dateien importiert: {stats['files_imported']}")
    log(f"Chunks erstellt: {stats['chunks_created']}")
    log(f"Bytes importiert: {stats['bytes_imported']:,} ({stats['bytes_imported']/1024/1024:.2f} MB)")
    log(f"Übersprungen: {stats['skipped']}")
    log(f"Collection-Größe: {collection.count()} Einträge")

    if stats["errors"]:
        log(f"\nFehler ({len(stats['errors'])}):")
        for err in stats["errors"][:5]:
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
        "Flutter App Terminal"
    ]

    for query in test_queries:
        log(f"\n[TEST] '{query}'")
        results = collection.query(query_texts=[query], n_results=3)

        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                log(f"  {i+1}. [{meta.get('kategorie', '?')}] {meta.get('dateiname', '?')}")
                log(f"     → {doc[:100]}...")
        else:
            log("  Keine Treffer!")

    log("\n" + "=" * 70)
    log("NAJIKA HAT JETZT EINE SAUBERE WISSENSDATENBANK!")
    log("=" * 70)

    return collection.count()

if __name__ == "__main__":
    main()
