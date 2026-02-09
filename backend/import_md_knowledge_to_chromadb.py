#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA MD KNOWLEDGE -> CHROMADB IMPORT
Importiert alle wichtigen MD-Dateien in Najikas Gedaechtnis
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import chromadb
from pathlib import Path
from datetime import datetime
import hashlib

# Pfade
NAJIKA_WORLD = Path("C:/Najika_World")
CHROMADB_PATH = "C:/Najika_World/memory_db"

# Wichtige MD-Dateien zum Importieren
MD_FILES = [
    # Knowledge Base Parts 1-10
    NAJIKA_WORLD / "najika_complete_kb_part1.md",
    NAJIKA_WORLD / "najika_complete_kb_part2.md",
    NAJIKA_WORLD / "najika_complete_kb_part3.md",
    NAJIKA_WORLD / "najika_complete_kb_part4.md",
    NAJIKA_WORLD / "najika_complete_kb_part5.md",
    NAJIKA_WORLD / "najika_complete_kb_part6.md",
    NAJIKA_WORLD / "najika_complete_kb_part7.md",
    NAJIKA_WORLD / "najika_complete_kb_part8.md",
    NAJIKA_WORLD / "najika_complete_kb_part9.md",
    NAJIKA_WORLD / "najika_complete_kb_part10.md",
    # V8 Zusammenfassung
    NAJIKA_WORLD / "NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md",
    # Weitere wichtige Docs
    NAJIKA_WORLD / "00_FINALE_KOMPLETT_UEBERSICHT_V7.md",
    NAJIKA_WORLD / "ALLE_UEBERSICHTEN_GESAMMELT.md",
    NAJIKA_WORLD / "NAJIKA_VOLLSTAENDIGE_PROJEKT_UEBERSICHT_V2.md",
    NAJIKA_WORLD / "NAJIKA_PROJEKT_ERGAENZUNGEN_V2.5.md",
    NAJIKA_WORLD / "INSTALLATION_GUIDE.md",
    NAJIKA_WORLD / "README.md",
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_doc_id(content, filename):
    """Generiert eindeutige ID fuer Dokument"""
    hash_input = f"md_{filename}_{content[:100]}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:16]

def chunk_text(text, chunk_size=4000, overlap=200):
    """Teilt langen Text in Chunks auf"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap if end < len(text) else end
    return chunks

def import_md_files():
    log("=" * 70)
    log("NAJIKA MD KNOWLEDGE -> CHROMADB IMPORT")
    log("=" * 70)

    # ChromaDB verbinden
    log(f"\nVerbinde mit ChromaDB: {CHROMADB_PATH}")
    client = chromadb.PersistentClient(path=CHROMADB_PATH)

    # Collection erstellen/holen
    try:
        collection = client.get_collection("najika_md_knowledge")
        log(f"Collection 'najika_md_knowledge' existiert bereits: {collection.count()} Eintraege")
    except:
        collection = client.create_collection(
            name="najika_md_knowledge",
            metadata={"description": "Najikas MD-Dokumentationen (KB Parts, V8, etc.)"}
        )
        log("Collection 'najika_md_knowledge' erstellt")

    total_imported = 0
    total_skipped = 0

    for md_file in MD_FILES:
        if not md_file.exists():
            log(f"[SKIP] Nicht gefunden: {md_file.name}")
            total_skipped += 1
            continue

        log(f"\n[IMPORT] {md_file.name}")

        try:
            content = md_file.read_text(encoding='utf-8')

            # Teile in Chunks auf (max 4000 Zeichen pro Chunk)
            chunks = chunk_text(content, chunk_size=4000, overlap=200)
            log(f"  → {len(chunks)} Chunks erstellt ({len(content)} Zeichen total)")

            for i, chunk in enumerate(chunks):
                doc_id = get_doc_id(chunk, f"{md_file.stem}_{i}")

                # In ChromaDB einfuegen
                collection.upsert(
                    ids=[doc_id],
                    documents=[chunk],
                    metadatas=[{
                        "source_file": md_file.name,
                        "chunk_index": str(i),
                        "total_chunks": str(len(chunks)),
                        "import_date": datetime.now().isoformat(),
                        "char_count": str(len(chunk))
                    }]
                )
                total_imported += 1

            log(f"  ✅ {len(chunks)} Chunks importiert")

        except Exception as e:
            log(f"  [ERROR] {e}")
            total_skipped += 1

    # Zusammenfassung
    log("\n" + "=" * 70)
    log("IMPORT ABGESCHLOSSEN")
    log("=" * 70)
    log(f"Importiert: {total_imported} Chunks")
    log(f"Uebersprungen: {total_skipped}")
    log(f"Collection-Groesse: {collection.count()}")

    # Test-Abfrage
    log("\n[TEST] Suche nach '8 Gebote Explosion'...")
    results = collection.query(
        query_texts=["Die 8 Gebote Explosion darf nicht geweaved werden"],
        n_results=3
    )

    if results['documents'] and results['documents'][0]:
        log(f"Gefunden: {len(results['documents'][0])} Treffer")
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i] if results['metadatas'] else {}
            log(f"  {i+1}. [{meta.get('source_file', '?')}] {doc[:100]}...")
    else:
        log("Keine Treffer gefunden")

    return total_imported

if __name__ == "__main__":
    import_md_files()
