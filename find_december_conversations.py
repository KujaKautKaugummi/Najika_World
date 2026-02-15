#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Findet ALLE Conversations und sortiert sie chronologisch
"""

import chromadb
from datetime import datetime
import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_all_conversations():
    """Liest ALLE Conversations und zeigt Zeitraum"""

    client = chromadb.PersistentClient(path="C:/Najika_World/memory_db")

    try:
        conv_collection = client.get_collection("conversations")
        total = conv_collection.count()
        print(f"✅ Lade {total} Conversations...\n")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return

    # Hole ALLE Conversations
    results = conv_collection.get(
        limit=total,
        include=["metadatas", "documents"]
    )

    if not results or not results['documents']:
        print("❌ Keine Conversations!")
        return

    # Parse Timestamps
    conversations = []
    for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
        ts_str = metadata.get('timestamp', '') if metadata else ''

        # Try to parse timestamp
        dt = None
        try:
            # ISO format
            if 'T' in ts_str:
                dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                # Remove timezone info for comparison
                if dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None)
            else:
                # Unix timestamp
                dt = datetime.fromtimestamp(float(ts_str))
        except:
            pass

        conversations.append({
            'index': i,
            'timestamp': ts_str,
            'datetime': dt,
            'role': metadata.get('role', 'unknown') if metadata else 'unknown',
            'mood': metadata.get('mood', '') if metadata else '',
            'text': doc[:200]  # First 200 chars
        })

    # Sort by datetime
    conversations_with_date = [c for c in conversations if c['datetime'] is not None]
    conversations_without_date = [c for c in conversations if c['datetime'] is None]

    conversations_with_date.sort(key=lambda x: x['datetime'])

    print("=" * 80)
    print("📊 ZEITRAUM ANALYSE")
    print("=" * 80)
    print(f"Total Conversations: {total}")
    print(f"Mit Datum: {len(conversations_with_date)}")
    print(f"Ohne Datum: {len(conversations_without_date)}")

    if conversations_with_date:
        oldest = conversations_with_date[0]['datetime']
        newest = conversations_with_date[-1]['datetime']
        print(f"\n⏰ Zeitraum: {oldest.strftime('%Y-%m-%d')} bis {newest.strftime('%Y-%m-%d')}")

    # Find December 2025 / January 2026
    print("\n" + "=" * 80)
    print("🔍 DEZEMBER 2025 / JANUAR 2026 GESPRÄCHE")
    print("=" * 80)

    dec_jan = [c for c in conversations_with_date
               if c['datetime'].year == 2025 and c['datetime'].month == 12
               or c['datetime'].year == 2026 and c['datetime'].month == 1]

    print(f"\n✅ Gefunden: {len(dec_jan)} Conversations\n")

    if dec_jan:
        # Show first 30
        for i, conv in enumerate(dec_jan[:30]):
            print(f"\n{'─' * 80}")
            print(f"📝 #{i+1} - {conv['datetime'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'─' * 80}")
            print(f"👤 Role: {conv['role']}")
            if conv['mood']:
                print(f"😊 Mood: {conv['mood']}")
            print(f"\n💬 Text:\n{conv['text']}")
    else:
        print("❌ Keine Dez/Jan Conversations gefunden!")
        print("\n🔍 Zeige stattdessen die NEUESTEN 20 Conversations:\n")

        for i, conv in enumerate(conversations_with_date[-20:]):
            print(f"\n{'─' * 80}")
            print(f"📝 #{i+1} - {conv['datetime'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'─' * 80}")
            print(f"👤 Role: {conv['role']}")
            if conv['mood']:
                print(f"😊 Mood: {conv['mood']}")
            print(f"\n💬 Text:\n{conv['text']}")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║          NAJIKA CONVERSATION TIMELINE ANALYZER               ║
║          Findet Dezember/Januar Gespräche                    ║
╚══════════════════════════════════════════════════════════════╝
    """)

    analyze_all_conversations()
