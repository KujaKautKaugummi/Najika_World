#!/usr/bin/env python3
"""
NAJIKA SMART EXTRACT: Ziehe die wichtigsten Absätze raus
"""
from pathlib import Path
import re

INPUT_FILES = [
    'C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT1.txt',
    'C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT2.txt',
    'C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT3.txt'
]

OUTPUT = 'C:/Users/0KKK0/Desktop/NAJIKA_FUER_CLAUDE_V2.txt'

# Keywords mit höherer Priorität
KEYWORDS = {
    'SKILL-SYSTEME': ['skyrim', 'use-based', 'skill progression', 'skill weaving', 'transformation', 'feuer', 'feura', 'feuraga', 'lernen durch'],
    'KAMPF-SYSTEME': ['soulframe', 'digimon world', 'dark souls', 'mortal kombat', 'anfeuern', 'timing', 'stamina', 'dodge'],
    'WELT & GEBIETE': ['8 gebiete', 'crimson desert', 'emerald forest', 'prozedural', 'stadt', 'oregon trail', 'portal'],
    'FORTNITE INTEGRATION': ['fortnite', 'uefn', 'digimon cyber sleuth', 'portal', 'universum', 'welten'],
    'BEGLEITER & PETS': ['slime', 'begleiter', 'companion', 'pet', 'form-wechsel', 'fütterung', 'stimmung'],
    'CRAFTING & NON-COMBAT': ['crafting', 'alchemie', 'housing', 'farming', 'fishing', 'rohstoff', 'rezept'],
    'EQUIPMENT & LOOT': ['equipment', 'loot', 'runen', 'slot', 'waffe', 'weapon morph', 'plündern'],
    'KLASSEN': ['explosion mage', 'warrior', 'healer', 'crafter', 'cross-class', 'megumin']
}

print('NAJIKA SMART EXTRACT...\n')

# Lese alle Dateien
all_text = ''
for fpath in INPUT_FILES:
    try:
        content = Path(fpath).read_text(encoding='utf-8', errors='ignore')
        all_text += content + '\n\n'
    except:
        pass

print(f'Gelesen: {len(all_text)} Zeichen')

# Teile in Absätze
paragraphs = [p.strip() for p in all_text.split('\n\n') if len(p.strip()) > 100]
print(f'Gefunden: {len(paragraphs)} Absätze\n')

# Extrahiere relevante Absätze pro Kategorie
results = {}

for category, keywords in KEYWORDS.items():
    results[category] = []

    for para in paragraphs:
        para_lower = para.lower()

        # Zähle wie viele Keywords vorkommen
        keyword_count = sum(1 for kw in keywords if kw in para_lower)

        if keyword_count > 0:
            # Score: Mehr Keywords = wichtiger
            score = keyword_count
            results[category].append((score, para))

    # Sortiere nach Score, nimm Top 5
    results[category].sort(reverse=True, key=lambda x: x[0])
    results[category] = [para for score, para in results[category][:5]]

# Schreibe Output
with open(OUTPUT, 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA SMART EXTRACT FÜR CLAUDE\n')
    out.write('='*80 + '\n')
    out.write(f'Extrahiert aus {len(all_text)} Zeichen, {len(paragraphs)} Absätzen\n')
    out.write('='*80 + '\n\n')

    for category, paras in results.items():
        out.write(f'\n{"#"*80}\n')
        out.write(f'{category}\n')
        out.write(f'{"#"*80}\n\n')

        if paras:
            for i, para in enumerate(paras, 1):
                out.write(f'[{i}] {para[:500]}\n')  # Max 500 chars pro Absatz
                if len(para) > 500:
                    out.write('    [...]\n')
                out.write('\n')
        else:
            out.write('(Keine relevanten Absätze gefunden)\n\n')

size = Path(OUTPUT).stat().st_size
print(f'FERTIG!')
print(f'Extrahiert: {size} Zeichen')
print(f'Gespeichert: {OUTPUT}')
