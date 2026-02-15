#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script zum Auslesen echter Najika-Konversationen aus ChromaDB
Fokus: Dezember 2025 / Januar 2026 Zeitraum
"""

import chromadb
from datetime import datetime
import json
import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_conversations():
    """Liest die conversations Collection aus ChromaDB"""

    # ChromaDB Client initialisieren
    client = chromadb.PersistentClient(path="C:/Najika_World/memory_db")

    # Liste aller Collections
    print("=" * 80)
    print("📚 VERFÜGBARE COLLECTIONS:")
    print("=" * 80)
    collections = client.list_collections()
    for col in collections:
        print(f"  - {col.name} ({col.count()} Einträge)")
    print()

    # Conversations Collection laden
    try:
        conv_collection = client.get_collection("conversations")
        print(f"✅ conversations Collection geladen: {conv_collection.count()} Einträge")
        print()
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return

    # Alle Conversations abrufen
    print("=" * 80)
    print("💬 LETZTE 20 NAJIKA↔KUJA GESPRÄCHE:")
    print("=" * 80)

    # Get all conversations
    results = conv_collection.get(
        limit=20,
        include=["metadatas", "documents"]
    )

    if not results or not results['documents']:
        print("❌ Keine Conversations gefunden!")
        return

    # Parse und zeige Conversations
    for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
        print(f"\n{'─' * 80}")
        print(f"📝 CONVERSATION #{i+1}")
        print(f"{'─' * 80}")

        # Metadata
        if metadata:
            if 'timestamp' in metadata:
                ts = metadata['timestamp']
                try:
                    dt = datetime.fromtimestamp(float(ts))
                    print(f"🕐 Zeitstempel: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    print(f"🕐 Zeitstempel: {ts}")

            if 'role' in metadata:
                print(f"👤 Rolle: {metadata['role']}")

            if 'mood' in metadata:
                print(f"😊 Stimmung: {metadata['mood']}")

        # Document (Conversation Text)
        print(f"\n💬 Inhalt:")
        print(f"{doc}")
        print()

    print("=" * 80)
    print("✅ FERTIG!")
    print("=" * 80)

def search_december_january():
    """Sucht speziell nach Dez/Jan Conversations"""

    client = chromadb.PersistentClient(path="C:/Najika_World/memory_db")

    try:
        conv_collection = client.get_collection("conversations")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return

    print("=" * 80)
    print("🔍 SUCHE: DEZEMBER 2025 / JANUAR 2026 GESPRÄCHE")
    print("=" * 80)

    # Query für relevante Zeiträume
    # Dezember 2025: 1733011200 - 1735689599
    # Januar 2026: 1735689600 - 1738367999

    results = conv_collection.get(
        where={
            "$and": [
                {"timestamp": {"$gte": "1733011200"}},  # >= 1. Dez 2025
                {"timestamp": {"$lte": "1738367999"}}   # <= 31. Jan 2026
            ]
        },
        limit=50,
        include=["metadatas", "documents"]
    )

    if not results or not results['documents']:
        print("❌ Keine Dez/Jan Conversations gefunden!")
        print("\n🔄 Zeige stattdessen ALLE Conversations...")
        read_conversations()
        return

    print(f"\n✅ {len(results['documents'])} Conversations gefunden!")

    for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
        print(f"\n{'─' * 80}")
        print(f"📝 CONVERSATION #{i+1}")
        print(f"{'─' * 80}")

        if metadata:
            if 'timestamp' in metadata:
                ts = metadata['timestamp']
                try:
                    dt = datetime.fromtimestamp(float(ts))
                    print(f"🕐 Datum: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    print(f"🕐 Timestamp: {ts}")

            print(f"👤 Rolle: {metadata.get('role', 'N/A')}")
            print(f"😊 Stimmung: {metadata.get('mood', 'N/A')}")

        print(f"\n💬 Nachricht:")
        print(f"{doc}")
        print()

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║          NAJIKA CHROMADB CONVERSATION READER                  ║
║          Liest echte Najika↔Kuja Gespräche aus               ║
╚══════════════════════════════════════════════════════════════╝
    """)

    try:
        # Versuche zuerst Dez/Jan zu finden
        search_december_january()
    except Exception as e:
        print(f"\n⚠️ Fehler bei Dez/Jan Suche: {e}")
        print("\n🔄 Versuche allgemeine Suche...")
        read_conversations()
