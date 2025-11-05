#!/usr/bin/env python3
"""
NAJIKA: Finde Verbesserungs-Ideen aus ALLEN Sessions
Vergleicht IST-Zustand mit Ideen aus allen Claude-Sessions
"""
import json
from pathlib import Path
from datetime import datetime

NAJIKA_DIR = Path('C:/NajikaCore')
SESSIONS_DIR = Path('C:/Users/0KKK0/.claude/projects/C--NajikaCore')
IST_OVERVIEW = Path('C:/Users/0KKK0/Desktop/NAJIKA_LESBARE_UEBERSICHT.txt')
OUTPUT_FILE = Path('C:/Users/0KKK0/Desktop/NAJIKA_VERBESSERUNGS_IDEEN.txt')

# IST-Zustand Features (aus der Übersicht)
IST_FEATURES = [
    # Server
    'living system',
    'memory system',
    'chromadb',
    'battle system',
    'private mode',
    'web search',
    'tor browser',
    'security module',
    'ollama',
    '12 räume',
    'room navigation',

    # Frontend
    '3d scene',
    'three.js',
    'kaykit',
    'minigames',
    'chat interface',
    'touch controls',

    # Spezielle
    'najika persönlichkeit',
    'megumin',
    'harley quinn',
    'shiro',
    'melissa',
    'training system'
]

# Such-Begriffe für mögliche Verbesserungen/Ergänzungen
SEARCH_TERMS = {
    'skill_system': ['skill', 'skyrim', 'level', 'xp', 'progression', 'use-based'],
    'combat': ['kampf', 'combat', 'attack', 'damage', 'enemy', 'boss', 'wave'],
    'companion': ['begleiter', 'companion', 'slime', 'pet', 'summon', 'ally'],
    'world': ['welt', 'world', 'gebiet', 'area', 'zone', 'region', 'map'],
    'crafting': ['craft', 'recipe', 'material', 'gather', 'resource'],
    'inventory': ['inventar', 'inventory', 'item', 'loot', 'drop', 'equipment'],
    'quest': ['quest', 'mission', 'aufgabe', 'task', 'objective'],
    'npc': ['npc', 'character', 'vendor', 'shop', 'merchant'],
    'magic': ['magic', 'spell', 'zauber', 'weaving', 'fire', 'ice', 'lightning'],
    'transformation': ['transformation', 'form', 'change', 'morph', 'evolution'],
    'portal': ['portal', 'teleport', 'gate', 'travel', 'warp'],
    'housing': ['housing', 'base', 'home', 'build', 'decoration'],
    'garden': ['garten', 'garden', 'plant', 'grow', 'farm'],
    'cooking': ['cook', 'recipe', 'food', 'meal', 'ingredient'],
    'alchemy': ['alchemy', 'potion', 'brew', 'mix', 'elixir'],
    'ai_enhancement': ['ai', 'personality', 'emotion', 'mood', 'behavior', 'learning'],
    'multiplayer': ['multiplayer', 'co-op', 'pvp', 'online', 'friend'],
    'mobile': ['mobile', 'app', 'android', 'ios', 'phone'],
    'uefn': ['uefn', 'fortnite', 'verse', 'epic'],
    'save': ['save', 'load', 'progress', 'checkpoint', 'backup']
}

def extract_ist_features():
    """Liest IST-Übersicht und extrahiert Features"""
    if not IST_OVERVIEW.exists():
        return []

    content = IST_OVERVIEW.read_text(encoding='utf-8').lower()

    found_features = []
    for feature in IST_FEATURES:
        if feature.lower() in content:
            found_features.append(feature)

    return found_features

def search_in_session(session_file, search_terms):
    """Durchsucht Session nach relevanten Ideen"""
    findings = {category: [] for category in search_terms.keys()}

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            line_num = 0
            for line in f:
                line_num += 1
                try:
                    entry = json.loads(line)

                    if entry.get('type') not in ['user', 'assistant']:
                        continue

                    content = entry.get('message', {}).get('content', [])

                    # Text extrahieren
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text_parts.append(item.get('text', ''))

                    full_text = ' '.join(text_parts)

                    # Nur substantielle Texte (min 300 chars)
                    if len(full_text) < 300:
                        continue

                    text_lower = full_text.lower()

                    # Suche nach Kategorien
                    for category, terms in search_terms.items():
                        term_count = sum(1 for term in terms if term in text_lower)

                        # Wenn mindestens 2 Terms aus Kategorie gefunden
                        if term_count >= 2:
                            findings[category].append({
                                'line': line_num,
                                'type': entry.get('type'),
                                'text': full_text[:1000],  # Erste 1000 chars
                                'term_count': term_count,
                                'timestamp': entry.get('timestamp', '')[:19]
                            })

                except:
                    continue

    except Exception as e:
        print(f"[ERROR] {session_file.name}: {e}")

    return findings

def main():
    print('='*80)
    print('NAJIKA: Finde Verbesserungen aus ALLEN Sessions')
    print('='*80)
    print('')

    # Schritt 1: IST-Zustand laden
    print('[1/4] Extrahiere IST-Zustand...')
    ist_features = extract_ist_features()
    print(f'      Gefunden: {len(ist_features)} Features im IST-Zustand')

    # Schritt 2: Alle Sessions durchsuchen
    print('[2/4] Durchsuche alle Sessions...')
    sessions = sorted(SESSIONS_DIR.glob('*.jsonl'),
                     key=lambda p: p.stat().st_ctime)

    print(f'      Sessions: {len(sessions)}')
    print('')

    all_findings = {}

    for i, session in enumerate(sessions, 1):
        print(f'      [{i:2d}/{len(sessions)}] {session.name[:12]}... ', end='', flush=True)

        findings = search_in_session(session, SEARCH_TERMS)

        # Zähle Treffer
        total_hits = sum(len(hits) for hits in findings.values())

        if total_hits > 0:
            all_findings[session.name] = findings
            print(f'OK {total_hits} Ideen')
        else:
            print('-')

    print(f'\n[3/4] Auswertung...')
    print(f'      Sessions mit Ideen: {len(all_findings)}')

    # Kategorien-Statistik
    category_totals = {cat: 0 for cat in SEARCH_TERMS.keys()}
    for findings in all_findings.values():
        for cat, hits in findings.items():
            category_totals[cat] += len(hits)

    print(f'      Kategorien mit Funden: {sum(1 for v in category_totals.values() if v > 0)}')

    # Schritt 4: Report erstellen
    print('[4/4] Erstelle Report...')

    lines = []
    lines.append('='*80)
    lines.append('NAJIKA - VERBESSERUNGS-IDEEN AUS ALLEN CLAUDE-SESSIONS')
    lines.append('='*80)
    lines.append('')
    lines.append(f'Erstellt: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append(f'Sessions durchsucht: {len(sessions)} (ALLE)')
    lines.append(f'Sessions mit Ideen: {len(all_findings)}')
    lines.append('')
    lines.append('='*80)
    lines.append('IST-ZUSTAND (AKTUELL VORHANDEN)')
    lines.append('='*80)
    lines.append('')
    for feature in ist_features:
        lines.append(f'  ✓ {feature}')
    lines.append('')
    lines.append('='*80)
    lines.append('GEFUNDENE IDEEN NACH KATEGORIEN')
    lines.append('='*80)
    lines.append('')

    # Sortiere nach Anzahl Funde
    sorted_categories = sorted(category_totals.items(),
                              key=lambda x: x[1],
                              reverse=True)

    for category, total in sorted_categories:
        if total == 0:
            continue

        lines.append('')
        lines.append('#'*80)
        lines.append(f'# {category.upper().replace("_", " ")} ({total} Funde)')
        lines.append('#'*80)
        lines.append('')

        # Such-Begriffe für diese Kategorie
        lines.append('Such-Begriffe: ' + ', '.join(SEARCH_TERMS[category]))
        lines.append('')

        # Sammle alle Funde für diese Kategorie
        category_hits = []
        for session_name, findings in all_findings.items():
            for hit in findings[category]:
                hit['session'] = session_name[:12]
                category_hits.append(hit)

        # Sortiere nach term_count (relevanteste zuerst)
        category_hits.sort(key=lambda x: x['term_count'], reverse=True)

        # Top 10 pro Kategorie
        for i, hit in enumerate(category_hits[:10], 1):
            lines.append(f'[{i}/10] Session: {hit["session"]}... | {hit["type"].upper()} | Terms: {hit["term_count"]}')
            lines.append(f'       Timestamp: {hit["timestamp"]}')
            lines.append('')
            lines.append(hit['text'][:800])  # Max 800 chars
            lines.append('')
            if len(hit['text']) > 800:
                lines.append('       ... [GEKÜRZT]')
                lines.append('')
            lines.append('-'*80)
            lines.append('')

        if len(category_hits) > 10:
            lines.append(f'... und {len(category_hits)-10} weitere Funde in dieser Kategorie')
            lines.append('')

    # Zusammenfassung
    lines.append('')
    lines.append('='*80)
    lines.append('ZUSAMMENFASSUNG')
    lines.append('='*80)
    lines.append('')
    lines.append('**IST-Zustand:**')
    lines.append(f'  - {len(ist_features)} Features vorhanden')
    lines.append('')
    lines.append('**Gefundene Ideen:**')
    lines.append(f'  - {len([c for c in category_totals.values() if c > 0])} Kategorien mit Vorschlägen')
    lines.append(f'  - {sum(category_totals.values())} Gesamt-Funde')
    lines.append('')
    lines.append('**Top 5 Kategorien:**')
    for cat, total in sorted_categories[:5]:
        if total > 0:
            lines.append(f'  - {cat.replace("_", " ").title()}: {total} Funde')
    lines.append('')
    lines.append('='*80)
    lines.append('ENDE')
    lines.append('='*80)

    # Speichern
    OUTPUT_FILE.write_text('\n'.join(lines), encoding='utf-8')

    print('')
    print('='*80)
    print('FERTIG')
    print('='*80)
    print(f'\n[OK] Report: {OUTPUT_FILE}')
    print(f'[OK] Sessions durchsucht: {len(sessions)}')
    print(f'[OK] Ideen gefunden: {sum(category_totals.values())}')
    print(f'[OK] Kategorien: {len([c for c in category_totals.values() if c > 0])}')
    print('')
    print('Top 5 Kategorien:')
    for cat, total in sorted_categories[:5]:
        if total > 0:
            print(f'  - {cat.replace("_", " ").title()}: {total}')
    print('')

if __name__ == '__main__':
    main()
