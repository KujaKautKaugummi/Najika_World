#!/usr/bin/env python3
"""NAJIKA SCHRITT 3: Allumfassende Übersicht aus ALLEN Dokumenten"""
import os
from pathlib import Path
import time

SEARCH_DIRS = [
    Path('C:/Najika_World'),
    Path('C:/Users/0KKK0/Desktop/zip'),
    Path('C:/Users/0KKK0/Desktop')
]

KEYWORDS = {
    'Skills': ['skill', 'skyrim', 'use-based', 'progression', 'lernen durch benutzen', 'transformation', 'skill-linie', 'feuer', 'feura', 'feuraga', 'weaving'],
    'Kampf': ['kampf', 'combat', 'soulframe', 'digimon world', 'dark souls', 'mortal kombat', 'anfeuern', 'stamina', 'dodge', 'parry'],
    'Welt': ['8 gebiete', 'gebiet', 'crimson desert', 'emerald forest', 'stadt', 'prozedural', 'oregon trail', 'portal', 'universum'],
    'Fortnite': ['fortnite', 'portal', 'digimon cyber sleuth', 'uefn', 'welten'],
    'Begleiter': ['slime', 'begleiter', 'companion', 'pet', 'form-wechsel'],
    'Crafting': ['crafting', 'alchemie', 'housing', 'farming', 'fishing'],
    'Equipment': ['equipment', 'loot', 'runen', 'waffe', 'weapon morph', 'plundern'],
    'Klassen': ['klasse', 'explosion', 'mage', 'warrior', 'healer', 'cross-class']
}

print('NAJIKA SCHRITT 3: Allumfassende Uebersicht aus ALLEN Dokumenten...')
start = time.time()

results = {cat: [] for cat in KEYWORDS.keys()}
all_files = []

# Sammle ALLE Dateien
for search_dir in SEARCH_DIRS:
    if not search_dir.exists():
        continue
    for ext in ['*.txt', '*.md', '*.pdf']:
        all_files.extend(list(search_dir.glob(ext)))

print(f'Durchsuche {len(all_files)} Dateien...')

# Durchsuche
count = 0
for filepath in all_files:
    try:
        # Skip zu große Dateien (>5MB)
        if filepath.stat().st_size > 5*1024*1024:
            continue

        content = filepath.read_text(encoding='utf-8', errors='ignore').lower()

        for category, keywords in KEYWORDS.items():
            found = False
            keywords_found = [kw for kw in keywords if kw.lower() in content]
            if keywords_found:
                results[category].append({
                    'file': filepath.name,
                    'path': str(filepath),
                    'keywords_found': keywords_found
                })

        count += 1
        if count % 20 == 0:
            print(f'  {count}/{len(all_files)} durchsucht...')
    except:
        pass

# Speichere
with open('C:/Users/0KKK0/Desktop/NAJIKA_SCHRITT3_ALLUMFASSEND.txt', 'w', encoding='utf-8') as f:
    f.write('NAJIKA SCHRITT 3 - ALLUMFASSENDE UEBERSICHT\n')
    f.write('='*80 + '\n')
    f.write(f'Durchsuchte Dateien: {count}\n')
    elapsed = round(time.time()-start, 1)
    f.write(f'Zeit: {elapsed}s\n')
    f.write('='*80 + '\n\n')

    for category, findings in results.items():
        f.write(f'\n## {category.upper()}\n')
        f.write('-'*80 + '\n')
        if findings:
            # Dedupliziere
            unique = {}
            for item in findings:
                if item['file'] not in unique:
                    unique[item['file']] = item

            f.write(f'Gefunden in {len(unique)} Dateien:\n\n')
            for item in sorted(unique.values(), key=lambda x: len(x['keywords_found']), reverse=True):
                kw_str = ', '.join(item['keywords_found'][:5])
                f.write(f'  [{len(item["keywords_found"])} Keywords] {item["file"]}\n')
                f.write(f'    Pfad: {item["path"]}\n')
                f.write(f'    Keywords: {kw_str}\n\n')
        else:
            f.write('  (Nichts gefunden)\n\n')

elapsed = round(time.time()-start, 1)
print(f'SCHRITT 3 fertig! ({elapsed}s)')
print('Gespeichert: C:/Users/0KKK0/Desktop/NAJIKA_SCHRITT3_ALLUMFASSEND.txt')
