#!/usr/bin/env python3
"""
NAJIKA: Komprimiere 500k Zeichen auf 25k für Claude
"""
from pathlib import Path
import re

INPUT_FILES = [
    'C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT1.txt',
    'C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT2.txt',
    'C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT3.txt'
]

OUTPUT = 'C:/Users/0KKK0/Desktop/NAJIKA_FUER_CLAUDE.txt'

CATEGORIES = ['SKILLS', 'KAMPF', 'WELT', 'FORTNITE', 'BEGLEITER', 'CRAFTING', 'EQUIPMENT', 'KLASSEN']

print('NAJIKA: Komprimiere 500k -> 25k für Claude...\n')

# Lese alle 3 Dateien
all_content = ''
for fpath in INPUT_FILES:
    try:
        content = Path(fpath).read_text(encoding='utf-8', errors='ignore')
        all_content += content + '\n\n'
        print(f'Gelesen: {Path(fpath).name} ({len(content)} chars)')
    except:
        pass

print(f'\nGesamt: {len(all_content)} Zeichen\n')

# Extrahiere pro Kategorie
results = {}

for category in CATEGORIES:
    results[category] = {
        'mechaniken': set(),
        'quellen': set(),
        'wichtige_punkte': []
    }

    # Finde Abschnitte zu dieser Kategorie
    pattern = rf'(?i)(#{{1,3}}\s*{category}|KATEGORIE:\s*{category})(.*?)(?=#{{1,3}}|KATEGORIE:|$)'
    matches = re.findall(pattern, all_content, re.DOTALL)

    for match in matches:
        section_text = match[1] if len(match) > 1 else ''

        # Extrahiere Bullet Points
        bullets = re.findall(r'(?:^|\n)\s*[-*•]\s*(.+)', section_text)
        for bullet in bullets[:15]:  # Max 15 pro Kategorie
            if len(bullet) > 20 and len(bullet) < 300:  # Sinnvolle Länge
                results[category]['wichtige_punkte'].append(bullet.strip())

        # Extrahiere Mechanik-Beschreibungen
        mechanik_patterns = [
            r'(?:Mechanik|System|Feature):\s*(.+?)(?:\n|$)',
            r'(?:Funktioniert|Ablauf|Prozess):\s*(.+?)(?:\n|$)',
            r'(?:\d+\.\s*)(.+?)(?:\n|$)'
        ]
        for pattern in mechanik_patterns:
            mechs = re.findall(pattern, section_text)
            for mech in mechs[:10]:
                if len(mech) > 30 and len(mech) < 400:
                    results[category]['mechaniken'].add(mech.strip())

        # Finde Quell-Dokumente
        docs = re.findall(r'(?:DOKUMENT|Datei):\s*([^\n]+)', section_text)
        results[category]['quellen'].update(docs[:5])

# Schreibe komprimierte Version
with open(OUTPUT, 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA ULTRA-KOMPAKT-ÜBERSICHT FÜR CLAUDE\n')
    out.write('='*80 + '\n')
    out.write(f'Komprimiert von {len(all_content)} auf max 25.000 Zeichen\n')
    out.write('='*80 + '\n\n')

    for category in CATEGORIES:
        data = results[category]

        out.write(f'\n{"#"*80}\n')
        out.write(f'{category}\n')
        out.write(f'{"#"*80}\n\n')

        # Quellen
        if data['quellen']:
            out.write('GEFUNDEN IN:\n')
            for doc in list(data['quellen'])[:3]:
                out.write(f'  - {doc}\n')
            out.write('\n')

        # Mechaniken
        if data['mechaniken']:
            out.write('MECHANIKEN:\n')
            for mech in list(data['mechaniken'])[:8]:
                out.write(f'  • {mech}\n')
            out.write('\n')

        # Wichtige Punkte
        if data['wichtige_punkte']:
            out.write('WICHTIGE PUNKTE:\n')
            unique_points = list(set(data['wichtige_punkte']))[:10]
            for point in unique_points:
                out.write(f'  → {point}\n')
            out.write('\n')

        if not (data['quellen'] or data['mechaniken'] or data['wichtige_punkte']):
            out.write('  (Keine Details gefunden)\n\n')

        out.write('\n')

# Füge Zusammenfassung hinzu
with open(OUTPUT, 'a', encoding='utf-8') as out:
    out.write('\n' + '='*80 + '\n')
    out.write('ZUSAMMENFASSUNG DER GEFUNDENEN SPIEL-IDEEN\n')
    out.write('='*80 + '\n\n')

    # Suche nach "3 Spiel-Ideen" oder ähnlichen Erwähnungen
    spiel_ideen = re.findall(r'(?i)(spiel.?idee?[^\n]{0,200})', all_content)
    if spiel_ideen:
        out.write('ERWÄHNTE SPIEL-KONZEPTE:\n')
        unique_ideas = list(set(spiel_ideen))[:5]
        for idea in unique_ideas:
            out.write(f'  • {idea}\n')
        out.write('\n')

final_size = Path(OUTPUT).stat().st_size
print(f'\nFERTIG!')
print(f'Komprimiert: {len(all_content)} -> {final_size} chars')
print(f'Gespeichert: {OUTPUT}')
