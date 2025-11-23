#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA HISTORY CLEANUP - AUTOMATIC (NO PROMPTS)

ACHTUNG: Löscht History SOFORT ohne zu fragen!
Aber: Erstellt automatisch Backup.
"""

import json
import shutil
import sys
import io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Paths
STATE_FILE = Path(__file__).resolve().parent / 'saves' / 'najika_state.json'
BACKUP_DIR = Path(__file__).resolve().parent / 'saves' / 'backups'

def main():
    print("=" * 60)
    print("NAJIKA HISTORY CLEANUP - AUTOMATIC")
    print("=" * 60)

    # Check if file exists
    if not STATE_FILE.exists():
        print(f"[ERROR] {STATE_FILE} nicht gefunden!")
        return False

    # Create backup directory
    BACKUP_DIR.mkdir(exist_ok=True)

    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = BACKUP_DIR / f'najika_state_BACKUP_{timestamp}.json'

    print(f"\n[BACKUP] Erstelle Backup: {backup_file.name}")
    shutil.copy(STATE_FILE, backup_file)
    print("[OK] Backup erstellt!")

    # Load state
    print(f"\n[LOAD] Lade {STATE_FILE.name}...")
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        state = json.load(f)

    # Analyze current history
    history_count = len(state.get('history', []))
    assistant_count = sum(1 for msg in state.get('history', []) if msg.get('role') == 'assistant')
    user_count = sum(1 for msg in state.get('history', []) if msg.get('role') == 'user')

    print(f"[INFO] Aktuelle History: {history_count} Messages")
    print(f"   - User Messages: {user_count}")
    print(f"   - Assistant Messages: {assistant_count}")

    # Clean history
    print(f"\n[CLEANUP] Bereinige History...")
    state['history'] = []

    # Add reset marker
    state['history_reset_at'] = datetime.now().isoformat()
    state['history_reset_reason'] = 'Contaminated training data cleanup - AUTOMATIC'

    # Save cleaned state
    print(f"[SAVE] Speichere bereinigte State...")
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] CLEANUP ERFOLGREICH!")
    print(f"\n[STATS] VORHER:")
    print(f"   - History Messages: {history_count}")
    print(f"   - User Messages: {user_count}")
    print(f"   - Assistant Messages: {assistant_count}")
    print(f"\n[STATS] NACHHER:")
    print(f"   - History Messages: 0")
    print(f"\n[BACKUP]:")
    print(f"   - {backup_file}")
    print(f"\n[NEXT] NAECHSTE SCHRITTE:")
    print(f"   1. Teste Najika mit sauberer History")
    print(f"   2. Beobachte Verhalten (sollte besser sein!)")
    print(f"   3. Bei Problemen: Restore Backup")
    print(f"\n[RESTORE] RESTORE COMMAND:")
    print(f"   copy {backup_file} {STATE_FILE}")
    print("=" * 60)

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
