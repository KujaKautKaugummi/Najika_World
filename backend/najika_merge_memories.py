#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA MEMORY MERGE
Fügt Video-Transkripte + KERN in das bestehende Memory-System ein
"""

import chromadb
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

def merge_memories():
    """Zusammenführen der beiden ChromaDB Systeme"""

    print("=" * 60)
    print("NAJIKA MEMORY MERGE")
    print("Füge Video-Transkripte + KERN in bestehendes System")
    print("=" * 60)
    print()

    # Load altes System (memory_db)
    old_client = chromadb.PersistentClient(path="C:/Najika_World/memory_db")

    # Load neues System (chroma_db)
    new_client = chromadb.PersistentClient(path="C:/Najika_World/chroma_db")

    # Get Collections aus neuem System
    personalities_new = new_client.get_collection("najika_personalities")
    core_new = new_client.get_collection("najika_core")

    print("📊 Neues System:")
    print(f"  - Persönlichkeiten: {personalities_new.count()} Einträge")
    print(f"  - KERN: {core_new.count()} Einträge")
    print()

    # Erstelle neue Collections im alten System
    try:
        personalities_old = old_client.get_collection("najika_personalities")
        print("✅ Persönlichkeits-Collection existiert bereits")
    except:
        personalities_old = old_client.create_collection("najika_personalities")
        print("✅ Persönlichkeits-Collection erstellt")

    try:
        core_old = old_client.get_collection("najika_core")
        print("✅ KERN-Collection existiert bereits")
    except:
        core_old = old_client.create_collection("najika_core")
        print("✅ KERN-Collection erstellt")

    print()

    # Kopiere KERN
    print("💖 Kopiere KERN (Kuja + Najika untrennbar)...")
    core_data = core_new.get()

    for i in range(len(core_data['ids'])):
        try:
            core_old.add(
                ids=[core_data['ids'][i]],
                documents=[core_data['documents'][i]],
                metadatas=[core_data['metadatas'][i]]
            )
            print(f"  ✅ {core_data['ids'][i]}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"  ⚠️  {core_data['ids'][i]}: Bereits vorhanden")
            else:
                print(f"  ❌ {core_data['ids'][i]}: {e}")

    print()

    # Kopiere Persönlichkeiten
    print("🎭 Kopiere Video-Transkripte (74 Stück)...")
    pers_data = personalities_new.get()

    copied = 0
    for i in range(len(pers_data['ids'])):
        try:
            personalities_old.add(
                ids=[pers_data['ids'][i]],
                documents=[pers_data['documents'][i]],
                metadatas=[pers_data['metadatas'][i]]
            )
            copied += 1
            if copied % 10 == 0:
                print(f"  ✅ {copied}/{len(pers_data['ids'])} kopiert...")
        except Exception as e:
            if "already exists" not in str(e):
                print(f"  ❌ Fehler bei {pers_data['ids'][i]}: {e}")

    print(f"  ✅ {copied} Transkripte kopiert!")
    print()

    # Statistik
    print("=" * 60)
    print("FINALES MEMORY SYSTEM (memory_db)")
    print("=" * 60)
    print()

    all_collections = {
        "Konversationen": old_client.get_collection("conversations"),
        "Emotionen": old_client.get_collection("emotions"),
        "Relationships": old_client.get_collection("relationships"),
        "Events": old_client.get_collection("events"),
        "KERN": core_old,
        "Persönlichkeiten": personalities_old
    }

    for name, coll in all_collections.items():
        print(f"  {name}: {coll.count()} Einträge")

    print()
    print("✅ MERGE ABGESCHLOSSEN!")
    print("💖 Najika hat jetzt ALLES:")
    print("   - Emotions & Beziehungs-Tracking")
    print("   - 74 Video-Transkripte")
    print("   - KERN: Kuja + Najika = untrennbar")
    print()


if __name__ == "__main__":
    merge_memories()
