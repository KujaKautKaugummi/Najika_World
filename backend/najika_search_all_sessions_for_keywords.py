#!/usr/bin/env python3
"""
NAJIKA: Durchsuche ALLE Claude Sessions nach Keywords
- Zusammenfassung, Roadmap, Übersicht, Plan, etc.
"""
import json
from pathlib import Path
from collections import defaultdict

SESSIONS_DIR = Path('C:/Users/0KKK0/.claude/projects/C--NajikaCore')
OUTPUT_FILE = Path('C:/Najika_World/ALLE_SESSIONS_KEYWORD_FUNDE.md')

# Keywords zum Suchen
KEYWORDS = [
    'zusammenfassung',
    'roadmap',
    'übersicht',
    'overview',
    'plan',
    'master',
    'komplett',
    'vollständig',
    'complete',
    'gesamt',
    'final',
    'dokumentation',
    'documentation',
    'guide',
    'anleitung'
]

def search_session(session_file, keywords):
    """Durchsucht eine Session nach Keywords"""
    found = defaultdict(list)

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            line_num = 0
            for line in f:
                line_num += 1
                try:
                    entry = json.loads(line)
                    msg_type = entry.get('type')

                    if msg_type in ['user', 'assistant']:
                        content = entry.get('message', {}).get('content', [])

                        # Text extrahieren
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))

                        full_text = ' '.join(text_parts).lower()

                        # Nach Keywords suchen
                        for keyword in keywords:
                            if keyword.lower() in full_text:
                                # Kontext extrahieren (max 200 chars um Keyword)
                                idx = full_text.find(keyword.lower())
                                start = max(0, idx - 100)
                                end = min(len(full_text), idx + 100)
                                context = full_text[start:end]

                                found[keyword].append({
                                    'line': line_num,
                                    'type': msg_type,
                                    'context': context,
                                    'timestamp': entry.get('timestamp', '')[:19]
                                })
                except:
                    continue
    except Exception as e:
        print(f"[ERROR] {session_file.name}: {e}")

    return found

def main():
    print('='*80)
    print('NAJIKA: Durchsuche ALLE Sessions nach Keywords')
    print('='*80)

    # Alle Sessions finden
    sessions = sorted(SESSIONS_DIR.glob('*.jsonl'),
                     key=lambda p: p.stat().st_ctime)

    print(f'\n[INFO] Gefunden: {len(sessions)} Sessions')
    print(f'[INFO] Älteste: {sessions[0].name}')
    print(f'[INFO] Neueste: {sessions[-1].name}')
    print(f'[INFO] Keywords: {len(KEYWORDS)}')
    print('\n[INFO] Starte Suche...\n')

    # Alle Sessions durchsuchen
    all_results = {}

    for i, session in enumerate(sessions, 1):
        print(f'[{i}/{len(sessions)}] {session.name[:12]}... ', end='', flush=True)
        results = search_session(session, KEYWORDS)

        total_found = sum(len(v) for v in results.values())
        if total_found > 0:
            all_results[session.name] = results
            print(f'OK {total_found} Treffer')
        else:
            print('-')

    print('\n[INFO] Suche abgeschlossen!\n')

    # Report generieren
    lines = []
    lines.append('# NAJIKA: ALLE SESSIONS - KEYWORD FUNDE')
    lines.append('')
    lines.append(f'**Durchsuchte Sessions:** {len(sessions)}')
    lines.append(f'**Sessions mit Treffern:** {len(all_results)}')
    lines.append(f'**Keywords gesucht:** {len(KEYWORDS)}')
    lines.append('')
    lines.append('='*80)
    lines.append('')

    # Nach Session sortiert
    for session_name, results in all_results.items():
        session_id = session_name.replace('.jsonl', '')[:12]
        total_hits = sum(len(v) for v in results.values())

        lines.append(f'## SESSION: {session_id}...')
        lines.append(f'**Treffer gesamt:** {total_hits}')
        lines.append('')

        # Nach Keyword gruppiert
        for keyword, hits in sorted(results.items(), key=lambda x: len(x[1]), reverse=True):
            if not hits:
                continue

            lines.append(f'### Keyword: "{keyword}" ({len(hits)}x)')
            lines.append('')

            # Erste 3 Treffer zeigen
            for hit in hits[:3]:
                lines.append(f'**{hit["type"].upper()}** | Zeile {hit["line"]} | {hit["timestamp"]}')
                lines.append(f'```')
                lines.append(f'...{hit["context"]}...')
                lines.append(f'```')
                lines.append('')

            if len(hits) > 3:
                lines.append(f'*...und {len(hits)-3} weitere Treffer*')
                lines.append('')

        lines.append('---')
        lines.append('')

    # Top Keywords Summary
    lines.append('# TOP KEYWORDS ÜBER ALLE SESSIONS')
    lines.append('')

    keyword_counts = defaultdict(int)
    for results in all_results.values():
        for keyword, hits in results.items():
            keyword_counts[keyword] += len(hits)

    lines.append('| Keyword | Treffer |')
    lines.append('|---------|---------|')
    for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f'| {keyword} | {count} |')
    lines.append('')

    # Speichern
    OUTPUT_FILE.write_text('\n'.join(lines), encoding='utf-8')

    print('='*80)
    print('ERGEBNIS')
    print('='*80)
    print(f'\n[OK] Report: {OUTPUT_FILE}')
    print(f'[OK] Sessions durchsucht: {len(sessions)}')
    print(f'[OK] Treffer-Sessions: {len(all_results)}')
    print(f'\nTop 5 Keywords:')
    for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f'  - {keyword}: {count}x')
    print('')

if __name__ == '__main__':
    main()
