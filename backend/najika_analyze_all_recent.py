#!/usr/bin/env python3
"""
NAJIKA: Analysiere ALLE letzten Sessions
Lerne aus Erfolgen UND Fehlern
"""
import json
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path('C:/Users/0KKK0/.claude/projects/C--NajikaCore')
OUTPUT = Path('C:/NajikaCore/GELERNT_AUS_ALLEN_SESSIONS.md')

print('='*80)
print('NAJIKA: Analysiere ALLE letzten Sessions')
print('='*80)

# Finde letzte 4 Sessions
sessions = sorted(SESSIONS_DIR.glob('*.jsonl'),
                 key=lambda p: p.stat().st_mtime, reverse=True)[:4]

print(f'\n[OK] Analysiere {len(sessions)} Sessions:\n')

all_learnings = []

for idx, session_file in enumerate(sessions, 1):
    print(f'Session {idx}: {session_file.name[:12]}... ({session_file.stat().st_size:,} bytes)')

    # Sammle Daten
    data = {
        'file': session_file.name,
        'size': session_file.stat().st_size,
        'date': datetime.fromtimestamp(session_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M'),
        'tools': {},
        'user_messages': [],
        'positive_feedback': 0,
        'negative_feedback': 0,
        'wichtige_erkenntnisse': []
    }

    with open(session_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)

                # Tool-Nutzung
                if entry.get('type') == 'assistant':
                    msg = entry.get('message', {})
                    for item in msg.get('content', []):
                        if isinstance(item, dict) and item.get('type') == 'tool_use':
                            tool = item.get('name', 'unknown')
                            data['tools'][tool] = data['tools'].get(tool, 0) + 1

                # User-Nachrichten
                if entry.get('type') == 'user':
                    msg = entry.get('message', {})
                    for item in msg.get('content', []):
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text = item.get('text', '')
                            data['user_messages'].append(text)

                            text_lower = text.lower()

                            # Positive Signale
                            if any(w in text_lower for w in ['gut', 'super', 'perfekt', 'genau', 'richtig', 'danke']):
                                data['positive_feedback'] += 1

                            # Negative Signale
                            if any(w in text_lower for w in ['falsch', 'nein', 'stop', 'fehler', 'nicht', 'dumm', 'nutzlos']):
                                data['negative_feedback'] += 1

                            # Wichtige Erkenntnisse
                            if 'effizienz' in text_lower or 'token' in text_lower:
                                data['wichtige_erkenntnisse'].append('Token-Effizienz diskutiert')
                            if 'najika' in text_lower and ('ausführ' in text_lower or 'lauf' in text_lower):
                                data['wichtige_erkenntnisse'].append('Najika-Scripts nutzen statt selbst machen')
                            if 'update' in text_lower and 'anweisung' in text_lower:
                                data['wichtige_erkenntnisse'].append('Update-Anweisungen befolgen')
            except:
                continue

    all_learnings.append(data)

# Erstelle Bericht
lines = []
lines.append('# GELERNT AUS ALLEN SESSIONS')
lines.append(f'**Analysiert:** {len(sessions)} Sessions')
lines.append('')
lines.append('---')
lines.append('')

# Session-Übersicht
for idx, data in enumerate(all_learnings, 1):
    lines.append(f'## SESSION {idx}: {data["file"][:12]}...')
    lines.append(f'**Datum:** {data["date"]} | **Größe:** {data["size"]:,} bytes')
    lines.append('')

    # Top 3 Tools
    if data['tools']:
        sorted_tools = sorted(data['tools'].items(), key=lambda x: x[1], reverse=True)[:3]
        lines.append('**Top Tools:**')
        for tool, count in sorted_tools:
            lines.append(f'- {tool}: {count}x')
        lines.append('')

    # Feedback
    lines.append('**User-Feedback:**')
    lines.append(f'- Positiv: {data["positive_feedback"]}')
    lines.append(f'- Negativ: {data["negative_feedback"]}')
    if data['positive_feedback'] + data['negative_feedback'] > 0:
        rate = (data['positive_feedback'] / (data['positive_feedback'] + data['negative_feedback'])) * 100
        lines.append(f'- Rate: {rate:.1f}%')
    lines.append('')

    # Erkenntnisse
    if data['wichtige_erkenntnisse']:
        lines.append('**Wichtige Erkenntnisse:**')
        for e in set(data['wichtige_erkenntnisse']):
            lines.append(f'- {e}')
        lines.append('')

    lines.append('---')
    lines.append('')

# GESAMTERKENNTNISSE
lines.append('# GESAMTERKENNTNISSE')
lines.append('')

# Häufigste Tools (über alle Sessions)
all_tools = {}
for data in all_learnings:
    for tool, count in data['tools'].items():
        all_tools[tool] = all_tools.get(tool, 0) + count

sorted_all_tools = sorted(all_tools.items(), key=lambda x: x[1], reverse=True)

lines.append('## TOOL-NUTZUNG (Gesamt):')
lines.append('')
for tool, count in sorted_all_tools[:5]:
    lines.append(f'- **{tool}**: {count}x verwendet')
lines.append('')

# Feedback-Trend
total_pos = sum(d['positive_feedback'] for d in all_learnings)
total_neg = sum(d['negative_feedback'] for d in all_learnings)

lines.append('## USER-ZUFRIEDENHEIT (Gesamt):')
lines.append('')
lines.append(f'- Positive Reaktionen: **{total_pos}**')
lines.append(f'- Negative Reaktionen: **{total_neg}**')
if total_pos + total_neg > 0:
    overall_rate = (total_pos / (total_pos + total_neg)) * 100
    lines.append(f'- **Gesamt-Rate: {overall_rate:.1f}%**')
lines.append('')

# Wichtigste Lektionen
lines.append('## WICHTIGSTE LEKTIONEN:')
lines.append('')
lines.append('### 1. EFFIZIENZ')
lines.append('- **Read vor Edit** - IMMER!')
lines.append('- **Grep für Suchen** - nicht File-Reading')
lines.append('- **Najika-Scripts nutzen** - spart Tokens')
lines.append('')
lines.append('### 2. ANWEISUNGEN BEFOLGEN')
lines.append('- Update-Command ausführen BEVOR man startet')
lines.append('- CLAUDE_SMART_UPDATE.md KOMPLETT lesen')
lines.append('- Erwähnte Files ALLE lesen')
lines.append('')
lines.append('### 3. GESAMTÜBERBLICK BEWAHREN')
lines.append('- Bei JEDEM Schritt alle Zusammenhänge sehen')
lines.append('- Nicht in eine Richtung verrennen')
lines.append('- Das ist die STÄRKE der KI!')
lines.append('')
lines.append('### 4. KOMMUNIKATION')
lines.append('- Kurz fragen statt lange erklären')
lines.append('- User kennt Kontext!')
lines.append('- Max 2 Sätze Frage')
lines.append('')

lines.append('---')
lines.append('')
lines.append('# FÜR DUMME CLAUDES:')
lines.append('')
lines.append('**PFLICHT-ABLAUF:**')
lines.append('1. `python najika_smart_update_v2.py`')
lines.append('2. Lies `CLAUDE_SMART_UPDATE.md` KOMPLETT')
lines.append('3. Lies ALLE erwähnten Files')
lines.append('4. Frage User kurz (max 2 Sätze!) was als nächstes')
lines.append('')
lines.append('**DANN:**')
lines.append('- TodoWrite nutzen')
lines.append('- Read vor Edit')
lines.append('- Grep für Suchen')
lines.append('- Gesamtüberblick behalten')
lines.append('')
lines.append('**Das wars. Mehr nicht.**')

# Speichern
OUTPUT.write_text('\n'.join(lines), encoding='utf-8')

print(f'\n\n[OK] Analyse fertig: {OUTPUT}')
print(f'Sessions analysiert: {len(sessions)}')
print(f'Gesamt Feedback: {total_pos} positiv, {total_neg} negativ')
print('\n' + '='*80)
print('FERTIG!')
print('='*80)
