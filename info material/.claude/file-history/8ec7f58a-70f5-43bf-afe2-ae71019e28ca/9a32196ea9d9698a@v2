#!/usr/bin/env python3
"""
NAJIKA: Extrahiere alle Zusammenfassungen/Roadmaps aus Sessions
Erstelle kompakte TXT auf Desktop
"""
import json
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path('C:/Users/0KKK0/.claude/projects/C--NajikaCore')
REPORT_FILE = Path('C:/NajikaCore/ALLE_SESSIONS_KEYWORD_FUNDE.md')
OUTPUT_FILE = Path('C:/Users/0KKK0/Desktop/NAJIKA_ALLE_ZUSAMMENFASSUNGEN.txt')

# Keywords für relevante Inhalte
PRIORITY_KEYWORDS = [
    'zusammenfassung',
    'roadmap',
    'übersicht',
    'master',
    'vollständig',
    'komplett'
]

def extract_relevant_messages(session_file, min_length=500):
    """
    Extrahiert relevante Messages aus Session
    - Nur User + Assistant Messages
    - Nur wenn Keywords enthalten
    - Mindestlänge 500 Zeichen (substantielle Inhalte)
    """
    relevant = []

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    msg_type = entry.get('type')

                    if msg_type not in ['user', 'assistant']:
                        continue

                    content = entry.get('message', {}).get('content', [])

                    # Text extrahieren
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text_parts.append(item.get('text', ''))

                    full_text = ' '.join(text_parts)

                    # Prüfe ob relevant
                    if len(full_text) < min_length:
                        continue

                    text_lower = full_text.lower()
                    has_keyword = any(kw in text_lower for kw in PRIORITY_KEYWORDS)

                    if has_keyword:
                        relevant.append({
                            'type': msg_type,
                            'text': full_text,
                            'timestamp': entry.get('timestamp', '')[:19],
                            'length': len(full_text)
                        })

                except:
                    continue
    except Exception as e:
        print(f"[ERROR] {session_file.name}: {e}")

    return relevant

def main():
    print('='*80)
    print('NAJIKA: Extrahiere Zusammenfassungen aus ALLEN Sessions')
    print('='*80)

    # Alle Sessions finden (sortiert nach Datum)
    sessions = sorted(SESSIONS_DIR.glob('*.jsonl'),
                     key=lambda p: p.stat().st_ctime)

    print(f'\n[INFO] Sessions gefunden: {len(sessions)}')
    print(f'[INFO] Älteste: {sessions[0].name[:12]}...')
    print(f'[INFO] Neueste: {sessions[-1].name[:12]}...')
    print('\n[INFO] Extrahiere relevante Inhalte...\n')

    all_extracts = {}
    total_messages = 0

    for i, session in enumerate(sessions, 1):
        print(f'[{i:2d}/{len(sessions)}] {session.name[:12]}... ', end='', flush=True)

        messages = extract_relevant_messages(session)

        if messages:
            all_extracts[session.name] = messages
            total_messages += len(messages)
            print(f'OK {len(messages)} Messages')
        else:
            print('-')

    print(f'\n[INFO] Extraktion abgeschlossen!')
    print(f'[INFO] Sessions mit Inhalt: {len(all_extracts)}')
    print(f'[INFO] Gesamt Messages: {total_messages}')

    # TXT generieren
    lines = []
    lines.append('='*80)
    lines.append('NAJIKA - ALLE ZUSAMMENFASSUNGEN & ROADMAPS AUS ALLEN CLAUDE SESSIONS')
    lines.append('='*80)
    lines.append('')
    lines.append(f'Generiert: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append(f'Sessions durchsucht: {len(sessions)}')
    lines.append(f'Sessions mit Inhalt: {len(all_extracts)}')
    lines.append(f'Relevante Messages: {total_messages}')
    lines.append('')
    lines.append('Keywords: zusammenfassung, roadmap, übersicht, master, vollständig, komplett')
    lines.append('')
    lines.append('='*80)
    lines.append('')

    # Pro Session (chronologisch)
    for session_name in sorted(all_extracts.keys()):
        messages = all_extracts[session_name]
        session_id = session_name.replace('.jsonl', '')

        lines.append('')
        lines.append('#'*80)
        lines.append(f'# SESSION: {session_id}')
        lines.append(f'# Messages: {len(messages)}')
        lines.append('#'*80)
        lines.append('')

        # Sortiere nach Timestamp
        messages_sorted = sorted(messages, key=lambda x: x['timestamp'])

        for j, msg in enumerate(messages_sorted, 1):
            lines.append('-'*80)
            lines.append(f'[{j}/{len(messages)}] {msg["type"].upper()} | {msg["timestamp"]} | {msg["length"]} chars')
            lines.append('-'*80)
            lines.append('')

            # Text (max 10000 chars pro Message)
            text = msg['text'][:10000]
            lines.append(text)

            if len(msg['text']) > 10000:
                lines.append('')
                lines.append(f'... [GEKÜRZT - Original {msg["length"]} chars]')

            lines.append('')
            lines.append('')

    # Footer
    lines.append('')
    lines.append('='*80)
    lines.append('ENDE - ALLE ZUSAMMENFASSUNGEN')
    lines.append('='*80)

    # Speichern
    OUTPUT_FILE.write_text('\n'.join(lines), encoding='utf-8')

    # Stats
    total_chars = sum(len(line) for line in lines)

    print('\n' + '='*80)
    print('ERGEBNIS')
    print('='*80)
    print(f'\n[OK] TXT erstellt: {OUTPUT_FILE}')
    print(f'[OK] Größe: {total_chars:,} Zeichen')
    print(f'[OK] Zeilen: {len(lines):,}')
    print(f'[OK] Sessions: {len(all_extracts)}')
    print(f'[OK] Messages: {total_messages}')
    print('')

    # Top Sessions
    print('Top 5 Sessions (nach Messages):')
    top_sessions = sorted(all_extracts.items(),
                         key=lambda x: len(x[1]),
                         reverse=True)[:5]
    for name, msgs in top_sessions:
        session_id = name.replace('.jsonl', '')[:12]
        print(f'  - {session_id}... {len(msgs)} Messages')
    print('')

if __name__ == '__main__':
    main()
