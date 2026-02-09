#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA PROJECT KNOWLEDGE → CHROMADB IMPORT
Importiert alle 266 JSON-Dateien in Najikas echtes Gedächtnis
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import chromadb
from pathlib import Path
from datetime import datetime
import hashlib

# Pfade
KNOWLEDGE_DIR = Path("C:/Najika_World/backend/najika_project_knowledge")
CHROMADB_PATH = "C:/Najika_World/memory_db"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_doc_id(content, category, filename):
    """Generiert eindeutige ID für Dokument"""
    hash_input = f"{category}_{filename}_{content[:100]}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:16]

def import_knowledge():
    log("=" * 70)
    log("NAJIKA PROJECT KNOWLEDGE -> CHROMADB IMPORT")
    log("=" * 70)

    # ChromaDB verbinden
    log(f"\nVerbinde mit ChromaDB: {CHROMADB_PATH}")
    client = chromadb.PersistentClient(path=CHROMADB_PATH)

    # Collection erstellen/holen für Projekt-Wissen
    try:
        collection = client.get_collection("najika_project_knowledge")
        log(f"Collection 'najika_project_knowledge' existiert bereits: {collection.count()} Eintraege")
    except:
        collection = client.create_collection(
            name="najika_project_knowledge",
            metadata={"description": "Najikas komplettes Projekt-Wissen aus 266 JSON-Dateien"}
        )
        log("Collection 'najika_project_knowledge' erstellt")

    # Kategorien durchgehen
    categories = [
        "game_ideas",
        "development_notes",
        "incomplete_code",
        "complete_implementations",
        "extracted_code",
        "project_concepts"
    ]

    total_imported = 0
    total_skipped = 0

    for category in categories:
        category_dir = KNOWLEDGE_DIR / category
        if not category_dir.exists():
            log(f"\n[SKIP] Kategorie nicht gefunden: {category}")
            continue

        files = list(category_dir.glob("*.json"))
        log(f"\n[IMPORT] {category}: {len(files)} Dateien")

        for i, file in enumerate(files):
            try:
                data = json.loads(file.read_text(encoding='utf-8'))

                # Content extrahieren
                if isinstance(data, dict):
                    content = data.get('content', '')
                    if not content and 'ideas' in data:
                        content = "\n".join(data['ideas'][:50])  # Max 50 Ideen
                    if not content and 'text' in data:
                        content = data['text']

                    source_file = data.get('source_file', str(file.name))
                    title = data.get('title', file.stem)
                elif isinstance(data, list):
                    content = "\n".join([str(item)[:500] for item in data[:20]])
                    source_file = str(file.name)
                    title = file.stem
                else:
                    content = str(data)[:5000]
                    source_file = str(file.name)
                    title = file.stem

                # Leere Inhalte skippen
                if not content or len(content) < 10:
                    total_skipped += 1
                    continue

                # Content auf max 10000 Zeichen begrenzen
                content = content[:10000]

                # ID generieren
                doc_id = get_doc_id(content, category, file.name)

                # In ChromaDB einfuegen (upsert)
                collection.upsert(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[{
                        "category": category,
                        "source_file": source_file,
                        "title": title,
                        "filename": file.name,
                        "import_date": datetime.now().isoformat(),
                        "char_count": str(len(content))
                    }]
                )

                total_imported += 1

                if (i + 1) % 20 == 0:
                    log(f"  ... {i+1}/{len(files)} importiert")

            except Exception as e:
                log(f"  [ERROR] {file.name}: {e}")
                total_skipped += 1

    # Zusammenfassung
    log("\n" + "=" * 70)
    log("IMPORT ABGESCHLOSSEN")
    log("=" * 70)
    log(f"Importiert: {total_imported}")
    log(f"Uebersprungen: {total_skipped}")
    log(f"Collection-Groesse: {collection.count()}")

    # Test-Abfrage
    log("\n[TEST] Suche nach 'Schwarze Muehle'...")
    results = collection.query(
        query_texts=["Schwarze Muehle Windmuehle Najika"],
        n_results=3
    )

    if results['documents'] and results['documents'][0]:
        log(f"Gefunden: {len(results['documents'][0])} Treffer")
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i] if results['metadatas'] else {}
            log(f"  {i+1}. [{meta.get('category', '?')}] {doc[:100]}...")
    else:
        log("Keine Treffer gefunden")

    return total_imported

if __name__ == "__main__":
    import_knowledge()
