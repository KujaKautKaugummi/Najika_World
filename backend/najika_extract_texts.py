#!/usr/bin/env python3
"""
NAJIKA - Extrahiere TEXTE (nicht nur Namen!)

SCHRITT 1: Alle Zusammenfassungen als komplette Texte
SCHRITT 2: Zusammenfassungen zu bestimmten Stichwörtern
SCHRITT 3: Alle Schnipsel/Ideen zu Stichwörtern
"""
from pathlib import Path

DIRS = [Path('C:/Najika_World'), Path('C:/Users/0KKK0/Desktop/zip'), Path('C:/Users/0KKK0/Desktop')]

SUMMARY_KW = ['zusammenfassung', 'summary', 'ubersicht', 'overview', 'roadmap', 'projekt', 'project', 'complete', 'final', 'game design']

KEYWORDS = {
    'Skills': ['skill', 'skyrim', 'use-based', 'transformation', 'skill-linie', 'feuer', 'feura', 'feuraga', 'weaving'],
    'Kampf': ['soulframe', 'digimon world', 'dark souls', 'mortal kombat', 'anfeuern'],
    'Welt': ['8 gebiete', 'crimson desert', 'prozedural', 'oregon trail'],
    'Fortnite': ['fortnite', 'portal', 'digimon cyber sleuth', 'uefn'],
    'Begleiter': ['slime', 'begleiter', 'companion', 'pet'],
    'Crafting': ['crafting', 'alchemie', 'housing'],
    'Klassen': ['explosion', 'mage', 'cross-class']
}

print('NAJIKA TEXT-EXTRAKTION...\n')

# SCHRITT 1: Alle Zusammenfassungen komplett
print('SCHRITT 1: Extrahiere alle Zusammenfassungen...')
summaries = []
for d in DIRS:
    if not d.exists(): continue
    for f in list(d.glob('*.txt')) + list(d.glob('*.md')):
        if any(kw in f.name.lower() for kw in SUMMARY_KW):
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                summaries.append((f.name, content))
            except: pass

with open('C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT1.txt', 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA SCHRITT 1: ALLE ZUSAMMENFASSUNGEN (KOMPLETTE TEXTE)\n')
    out.write('='*80 + '\n\n')
    for name, text in summaries:
        out.write(f'\n{"="*80}\n')
        out.write(f'DOKUMENT: {name}\n')
        out.write(f'{"="*80}\n\n')
        out.write(text[:10000])  # Max 10k chars pro Dokument
        if len(text) > 10000:
            out.write(f'\n\n... [GEKUERZT - Original: {len(text)} chars]')
        out.write('\n\n')

print(f'  -> {len(summaries)} Zusammenfassungen extrahiert')

# SCHRITT 2: Zusammenfassungen mit Stichwörtern
print('SCHRITT 2: Zusammenfassungen mit Stichwörtern...')
with open('C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT2.txt', 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA SCHRITT 2: ZUSAMMENFASSUNGEN MIT STICHWÖRTERN\n')
    out.write('='*80 + '\n\n')

    for category, kws in KEYWORDS.items():
        out.write(f'\n{"#"*80}\n')
        out.write(f'KATEGORIE: {category.upper()}\n')
        out.write(f'{"#"*80}\n\n')

        found_any = False
        for name, text in summaries:
            text_lower = text.lower()
            if any(kw in text_lower for kw in kws):
                found_any = True
                out.write(f'\n{"="*80}\n')
                out.write(f'DOKUMENT: {name}\n')
                out.write(f'{"="*80}\n\n')
                out.write(text[:5000])
                if len(text) > 5000:
                    out.write(f'\n\n... [GEKUERZT]')
                out.write('\n\n')

        if not found_any:
            out.write('  (Keine Zusammenfassung zu diesem Thema gefunden)\n\n')

print('  -> Kategorisierte Zusammenfassungen erstellt')

# SCHRITT 3: Alle Schnipsel/Ideen
print('SCHRITT 3: Alle Schnipsel/Ideen zu Stichwörtern...')
all_files = []
for d in DIRS:
    if not d.exists(): continue
    all_files.extend(list(d.glob('*.txt'))[:50])  # Max 50 pro Dir

with open('C:/Users/0KKK0/Desktop/NAJIKA_TEXT_SCHRITT3.txt', 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA SCHRITT 3: SCHNIPSEL/IDEEN ZU STICHWÖRTERN\n')
    out.write('='*80 + '\n\n')

    for category, kws in KEYWORDS.items():
        out.write(f'\n{"#"*80}\n')
        out.write(f'KATEGORIE: {category.upper()}\n')
        out.write(f'{"#"*80}\n\n')

        for f in all_files:
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                if len(content) > 50000: continue  # Skip huge files

                content_lower = content.lower()
                matching_kws = [kw for kw in kws if kw in content_lower]

                if matching_kws:
                    out.write(f'\n{"-"*80}\n')
                    out.write(f'Datei: {f.name}\n')
                    out.write(f'Keywords: {", ".join(matching_kws)}\n')
                    out.write(f'{"-"*80}\n\n')

                    # Extrahiere relevante Schnipsel (Zeilen mit Keywords +/- Kontext)
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if any(kw in line.lower() for kw in matching_kws):
                            # 2 Zeilen Kontext
                            start = max(0, i-2)
                            end = min(len(lines), i+3)
                            snippet = '\n'.join(lines[start:end])
                            out.write(snippet + '\n...\n\n')
                            if i > 100: break  # Max 100 matches pro Datei
            except:
                pass

print('  -> Schnipsel extrahiert\n')
print('FERTIG!')
print('Gespeichert:')
print('  - NAJIKA_TEXT_SCHRITT1.txt (Alle Zusammenfassungen)')
print('  - NAJIKA_TEXT_SCHRITT2.txt (Zusammenfassungen mit Keywords)')
print('  - NAJIKA_TEXT_SCHRITT3.txt (Schnipsel/Ideen)')
