#!/usr/bin/env python3
"""
NAJIKA: Lerne vom GUTEN Claude
Extrahiere WIE der gute Claude gearbeitet hat
"""
import json
from pathlib import Path

GOOD_SESSION = Path('C:/Users/0KKK0/.claude/projects/C--NajikaCore/1e75a874-27fc-4133-a038-22081b5aae06.jsonl')
OUTPUT = Path('C:/NajikaCore/WIE_GUTER_CLAUDE_ARBEITET.md')

print('='*80)
print('NAJIKA: Analysiere GUTEN Claude')
print('='*80)

# Sammle Patterns
patterns = {
    'tool_usage': {},
    'antwort_laenge': [],
    'user_zufriedenheit': [],
    'arbeitsmuster': []
}

with open(GOOD_SESSION, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)

            # Assistant Messages analysieren
            if entry.get('type') == 'assistant':
                msg = entry.get('message', {})
                content = msg.get('content', [])

                # Zähle Tool-Nutzung
                for item in content:
                    if isinstance(item, dict):
                        if item.get('type') == 'tool_use':
                            tool_name = item.get('name', 'unknown')
                            patterns['tool_usage'][tool_name] = patterns['tool_usage'].get(tool_name, 0) + 1

                        # Text-Länge
                        if item.get('type') == 'text':
                            text = item.get('text', '')
                            patterns['antwort_laenge'].append(len(text))

            # User Feedback
            if entry.get('type') == 'user':
                msg = entry.get('message', {})
                content = msg.get('content', [])

                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'text':
                        text = item.get('text', '').lower()

                        # Positive Signale
                        if any(word in text for word in ['gut', 'super', 'perfekt', 'danke', 'genau']):
                            patterns['user_zufriedenheit'].append('POSITIV')
                        # Negative Signale
                        elif any(word in text for word in ['falsch', 'nein', 'stop', 'fehler', 'nicht']):
                            patterns['user_zufriedenheit'].append('NEGATIV')

        except:
            continue

# Erstelle Bericht
lines = []
lines.append('# WIE DER GUTE CLAUDE GEARBEITET HAT')
lines.append('**Analysiert aus Session:** 1e75a874 (24MB, 18. Okt 20:02)')
lines.append('')
lines.append('---')
lines.append('')

# Tool-Nutzung
lines.append('## TOOL-NUTZUNG')
lines.append('')
sorted_tools = sorted(patterns['tool_usage'].items(), key=lambda x: x[1], reverse=True)
for tool, count in sorted_tools[:10]:
    lines.append(f'- **{tool}**: {count}x verwendet')
lines.append('')

# Antwort-Länge
if patterns['antwort_laenge']:
    avg_len = sum(patterns['antwort_laenge']) / len(patterns['antwort_laenge'])
    lines.append('## ANTWORT-STIL')
    lines.append('')
    lines.append(f'- Durchschnittliche Text-Länge: **{int(avg_len)} Zeichen**')
    lines.append(f'- Kürzeste Antwort: {min(patterns["antwort_laenge"])} Zeichen')
    lines.append(f'- Längste Antwort: {max(patterns["antwort_laenge"])} Zeichen')
    lines.append('')

# User-Zufriedenheit
positiv = patterns['user_zufriedenheit'].count('POSITIV')
negativ = patterns['user_zufriedenheit'].count('NEGATIV')
lines.append('## USER-ZUFRIEDENHEIT')
lines.append('')
lines.append(f'- Positive Reaktionen: **{positiv}**')
lines.append(f'- Negative Reaktionen: **{negativ}**')
if positiv + negativ > 0:
    zufriedenheit = (positiv / (positiv + negativ)) * 100
    lines.append(f'- **Zufriedenheits-Rate: {zufriedenheit:.1f}%**')
lines.append('')

lines.append('---')
lines.append('')

# ERKENNTNISSE
lines.append('## ERKENNTNISSE FÜR SCHLECHTE CLAUDES')
lines.append('')

# Top-Tool
if sorted_tools:
    top_tool = sorted_tools[0][0]
    lines.append(f'### 1. MEIST-GENUTZTES TOOL: {top_tool}')
    lines.append(f'Der gute Claude nutzte **{top_tool}** am häufigsten ({sorted_tools[0][1]}x).')
    lines.append('**Lektion:** Nutze die richtigen Tools!')
    lines.append('')

# Antwort-Länge
if patterns['antwort_laenge']:
    lines.append(f'### 2. ANTWORT-LÄNGE: ~{int(avg_len)} Zeichen')
    if avg_len < 500:
        lines.append('Der gute Claude war **KURZ UND PRÄZISE**.')
        lines.append('**Lektion:** Keine langen Erklärungen - User kennt Kontext!')
    else:
        lines.append('Der gute Claude gab **DETAILLIERTE ANTWORTEN**.')
        lines.append('**Lektion:** Gründlich sein wenn nötig!')
    lines.append('')

# Zufriedenheit
if positiv > negativ * 2:
    lines.append('### 3. HOHE USER-ZUFRIEDENHEIT')
    lines.append(f'Der gute Claude bekam **{positiv} positive** vs {negativ} negative Reaktionen.')
    lines.append('**Lektion:** User-Anweisungen folgen = Happy User!')
    lines.append('')

lines.append('---')
lines.append('')
lines.append('## ZUSAMMENFASSUNG')
lines.append('')
lines.append('Der GUTE Claude:')
lines.append('1. Nutzte Tools effizient')
lines.append('2. Gab passend-lange Antworten')
lines.append('3. Folgte User-Anweisungen')
lines.append('4. Behielt Gesamtüberblick')
lines.append('')
lines.append('**DU solltest das auch tun!**')

# Speichern
OUTPUT.write_text('\n'.join(lines), encoding='utf-8')

print(f'\n[OK] Analyse fertig: {OUTPUT}')
print(f'Tool-Nutzung analysiert: {len(patterns["tool_usage"])} verschiedene Tools')
print(f'Antworten analysiert: {len(patterns["antwort_laenge"])}')
print(f'User-Feedback: {positiv} positiv, {negativ} negativ')
print('\n' + '='*80)
print('FERTIG!')
print('='*80)
