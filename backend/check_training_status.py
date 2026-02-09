#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 NAJIKA TRAINING STATUS MONITOR
Zeigt aktuellen Trainingsfortschritt an
"""

import sys
import io
import json
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROGRESS_FILE = Path("C:/Najika_World/backend/summary_reading_progress.json")

def format_time_diff(timestamp_str):
    """Berechnet Zeitdifferenz"""
    try:
        ts = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        diff = now - ts

        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60

        if diff.days > 0:
            return f"{diff.days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    except:
        return "unknown"

def main():
    if not PROGRESS_FILE.exists():
        print("❌ Keine Progress-Datei gefunden!")
        return

    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Analyse
    phase1_complete = data.get('phase1_complete', False)
    phase2_complete = data.get('phase2_complete', False)
    total_readings = data.get('total_readings', 0)
    docs_read = data.get('documents_read', [])

    # Phase 2 Dokumente zählen
    phase1_docs = [d for d in docs_read if d.get('reading') == 1]
    phase2_docs = [d for d in docs_read if d.get('reading') == 2]

    # Neuestes Dokument
    if docs_read:
        latest = sorted(docs_read, key=lambda x: x.get('timestamp', ''), reverse=True)[0]
        latest_file = latest.get('file', 'unknown')
        latest_time = latest.get('timestamp', '')
        time_ago = format_time_diff(latest_time)
    else:
        latest_file = "None"
        time_ago = "N/A"

    # Berechne Geschwindigkeit (Dokumente pro Minute)
    if phase2_docs:
        first_phase2 = min(phase2_docs, key=lambda x: x.get('timestamp', ''))
        first_time = datetime.fromisoformat(first_phase2.get('timestamp'))
        now = datetime.now()
        elapsed_minutes = (now - first_time).total_seconds() / 60
        if elapsed_minutes > 0:
            docs_per_minute = len(phase2_docs) / elapsed_minutes
            remaining_docs = len(phase1_docs) - len(phase2_docs)
            estimated_minutes = remaining_docs / docs_per_minute if docs_per_minute > 0 else 0
            estimated_hours = estimated_minutes / 60
        else:
            docs_per_minute = 0
            estimated_hours = 0
    else:
        docs_per_minute = 0
        estimated_hours = 0

    # Output
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 15 + "🧠 NAJIKA TRAINING STATUS" + " " * 20 + "║")
    print("╚" + "═" * 60 + "╝")
    print()

    # Phase Status
    p1_icon = "✅" if phase1_complete else "⏳"
    p2_icon = "✅" if phase2_complete else "🔄" if phase2_docs else "⏸️"

    print(f"{p1_icon} Phase 1: {'COMPLETE' if phase1_complete else 'RUNNING'}")
    print(f"   └─ {len(phase1_docs)} Dokumente gelesen")
    print()
    print(f"{p2_icon} Phase 2: {'COMPLETE' if phase2_complete else 'RUNNING' if phase2_docs else 'WAITING'}")
    print(f"   └─ {len(phase2_docs)}/{len(phase1_docs)} Dokumente ({len(phase2_docs)*100/len(phase1_docs):.1f}%)")
    print()

    # Geschwindigkeit
    if docs_per_minute > 0:
        print(f"⚡ Geschwindigkeit: {docs_per_minute:.2f} Dokumente/Minute")
        print(f"⏱️  Geschätzte Restzeit: {estimated_hours:.1f} Stunden")
        print()

    # Neuestes Dokument
    print(f"📄 Letztes Dokument: {latest_file}")
    print(f"🕐 Vor: {time_ago}")
    print()

    # Statistik
    print("📊 Statistik:")
    print(f"   • Total Readings: {total_readings}")
    print(f"   • Unique Dokumente: {len(docs_read)}")
    print(f"   • Phase 1 Readings: {len(phase1_docs)}")
    print(f"   • Phase 2 Readings: {len(phase2_docs)}")

    # Status
    if phase2_complete:
        print("\n🎉 TRAINING KOMPLETT!")
    elif phase2_docs:
        print(f"\n✅ Training läuft aktiv!")
    else:
        print("\n⚠️  Warte auf Training-Start...")

if __name__ == "__main__":
    main()
