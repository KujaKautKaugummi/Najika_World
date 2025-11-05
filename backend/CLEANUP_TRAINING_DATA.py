#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 TRAINING DATA CLEANUP - GRÜNDLICH FÜR MONTAG
Entfernt erfundene User/Kuja-Dialoge aus ALLEN Training-Daten

PROBLEM: Najika hat gelernt User-Antworten zu erfinden
LÖSUNG: Cleane ALLE Training-Daten + Re-Train komplett neu

ZEIT: ~2 Stunden Cleanup + 8 Stunden Training = Montag fertig!
"""

import json
import re
import sys
import io
from pathlib import Path
from datetime import datetime
import pytz
import shutil

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

NAJIKA_DIR = Path('C:/Najika-World')
BACKEND_DIR = NAJIKA_DIR / 'backend'
SAVES_DIR = BACKEND_DIR / 'saves'
BACKUP_DIR = NAJIKA_DIR / 'training_data_backup'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] [{level}] {message}')

def clean_najika_text(text):
    """
    Entfernt erfundene User/Kuja-Dialoge aus Najika's Text

    PATTERNS ZU ENTFERNEN:
    - "Kuja:" oder "*Kuja " (User-Dialog erfunden)
    - "*Kuja lächelt*" (User-Action erfunden)
    - "User:" (Meta-Text)
    - "Ich kann als Najika antworten:" (Meta-Text)
    """

    if not text or not isinstance(text, str):
        return text

    original_length = len(text)

    # Entferne "Ich kann als Najika antworten:" Präfix
    patterns_remove = [
        r'^Ich kann als Najika antworten:\s*',
        r'^Ich kann als Najika sagen:\s*',
        r'^Als Najika antworte ich:\s*',
    ]

    for pattern in patterns_remove:
        text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)

    # Entferne Anführungszeichen wenn GANZE Antwort in Quotes
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

    # Entferne "Ich habe folgende Persönlichkeit gewählt:" Suffix
    text = re.sub(r'\n+Ich habe folgende Persönlichkeit gewählt:.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)

    # 🚫 KRITISCH: Schneide erfundene Kuja/User-Dialoge ab!
    kuja_patterns = [
        r'\*Kuja\s+(lächelt|nickt|grinst|springt|läuft|sagt|antwortet|schaut|lacht|weint|küsst|umarmt)',
        r'\*User\s+(lächelt|nickt|grinst|springt|läuft|sagt|antwortet|schaut|lacht)',
        r'Kuja:',
        r'User:',
        r'\nKuja\s+',
        r'\nUser\s+',
    ]

    kuja_pos = -1
    for pattern in kuja_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            kuja_pos = match.start()
            break

    if kuja_pos > 0:
        # Schneide ALLES ab der erfundenen Action
        text = text[:kuja_pos].strip()

        # Entferne unvollständige Sätze am Ende
        if text.count('*') % 2 == 1:  # Ungerade Anzahl = nicht geschlossen
            last_closed = text.rfind('*', 0, len(text)-1)
            if last_closed > 0:
                text = text[:last_closed+1].strip()

    # Entferne "Najika:" Präfix (Najika soll direkt sprechen)
    text = re.sub(r'^Najika:\s*', '', text, flags=re.MULTILINE)

    cleaned_text = text.strip()

    if len(cleaned_text) < original_length * 0.5:
        # Wenn mehr als 50% entfernt → Zu aggressiv, behalte Original
        log(f"⚠️  Text zu stark reduziert ({original_length} → {len(cleaned_text)}), behalte Original", 'WARNING')
        return text  # Rückgabe des teilweise gecleanten

    return cleaned_text

def find_training_data_files():
    """Findet ALLE JSON Files mit Training-Daten"""

    log("Suche nach Training-Data Files...", 'INFO')

    files = []

    # 1. Saves Directory (najika_state*.json)
    if SAVES_DIR.exists():
        saves = list(SAVES_DIR.glob('najika_state*.json'))
        files.extend(saves)
        log(f"  📁 Saves: {len(saves)} Files", 'INFO')

    # 2. Backend Root (najika_state.json, conversation*.json)
    backend_jsons = list(BACKEND_DIR.glob('*.json'))
    backend_jsons = [f for f in backend_jsons if 'state' in f.name.lower() or 'conversation' in f.name.lower()]
    files.extend(backend_jsons)
    log(f"  📁 Backend: {len(backend_jsons)} Files", 'INFO')

    # 3. ChromaDB Memory (falls JSON-Export existiert)
    chromadb_dir = BACKEND_DIR / 'chromadb_data'
    if chromadb_dir.exists():
        chromadb_jsons = list(chromadb_dir.glob('**/*.json'))
        files.extend(chromadb_jsons)
        log(f"  📁 ChromaDB: {len(chromadb_jsons)} Files", 'INFO')

    log(f"✅ Gesamt: {len(files)} Training-Data Files gefunden", 'SUCCESS')
    return files

def backup_file(file_path):
    """Erstellt Backup bevor Änderung"""
    backup_path = BACKUP_DIR / file_path.relative_to(NAJIKA_DIR)
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    if not backup_path.exists():
        shutil.copy2(file_path, backup_path)
        return True
    return False

def clean_json_file(file_path):
    """Cleant ein JSON File (najika_state.json Format)"""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False
        cleaned_messages = 0

        # Format 1: najika_state.json mit "history" Array
        if 'history' in data and isinstance(data['history'], list):
            for msg in data['history']:
                if msg.get('role') == 'assistant' and 'content' in msg:
                    original = msg['content']
                    cleaned = clean_najika_text(original)

                    if cleaned != original:
                        msg['content'] = cleaned
                        modified = True
                        cleaned_messages += 1

        # Format 2: Direkte conversation Array
        if 'conversation' in data and isinstance(data['conversation'], list):
            for msg in data['conversation']:
                if msg.get('role') == 'najika' and 'text' in msg:
                    original = msg['text']
                    cleaned = clean_najika_text(original)

                    if cleaned != original:
                        msg['text'] = cleaned
                        modified = True
                        cleaned_messages += 1

        if modified:
            # Backup erstellen
            backup_file(file_path)

            # Speichere gecleanteVersion
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True, cleaned_messages

        return False, 0

    except Exception as e:
        log(f"❌ Fehler bei {file_path.name}: {e}", 'ERROR')
        return False, 0

def main():
    """Hauptfunktion"""

    log("="*60, 'INFO')
    log("🧹 TRAINING DATA CLEANUP - GRÜNDLICH", 'INFO')
    log("="*60, 'INFO')

    # Erstelle Backup Directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    log(f"📁 Backup-Verzeichnis: {BACKUP_DIR}", 'INFO')

    # Finde alle Files
    files = find_training_data_files()

    if not files:
        log("⚠️  Keine Training-Data Files gefunden!", 'WARNING')
        return False

    log("", 'INFO')
    log("🧹 Starte Cleanup...", 'INFO')

    total_files = len(files)
    modified_files = 0
    total_cleaned_messages = 0

    for i, file_path in enumerate(files, 1):
        log(f"[{i}/{total_files}] {file_path.name}...", 'INFO')

        modified, cleaned_count = clean_json_file(file_path)

        if modified:
            modified_files += 1
            total_cleaned_messages += cleaned_count
            log(f"  ✅ {cleaned_count} Messages gecleant", 'SUCCESS')
        else:
            log(f"  ⏭️  Keine Änderungen nötig", 'INFO')

    log("", 'INFO')
    log("="*60, 'INFO')
    log("✅ CLEANUP KOMPLETT!", 'SUCCESS')
    log("="*60, 'INFO')
    log(f"📊 Statistik:", 'INFO')
    log(f"  - Files geprüft: {total_files}", 'INFO')
    log(f"  - Files modifiziert: {modified_files}", 'INFO')
    log(f"  - Messages gecleant: {total_cleaned_messages}", 'INFO')
    log(f"  - Backup erstellt in: {BACKUP_DIR}", 'INFO')
    log("="*60, 'INFO')
    log("", 'INFO')
    log("🎯 NÄCHSTER SCHRITT:", 'INFO')
    log("  1. Prüfe Backups in: C:\\NajikaFinal\\training_data_backup", 'INFO')
    log("  2. Starte Re-Training: python najika_daily_training.py", 'INFO')
    log("  3. Warte 8 Stunden", 'INFO')
    log("  4. Teste Najika (sollte KEINE User-Dialoge mehr erfinden!)", 'INFO')
    log("="*60, 'INFO')

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
