#!/usr/bin/env python3
"""
NAJIKA: Erstelle Pyramiden-Zusammenfassungen
- ULTRA-KOMPAKT: 10k chars (Kern-Konzepte)
- MITTEL: 30k chars (Erweiterte Details)
- VOLL: 69k chars (Original)
"""
from pathlib import Path
import re

INPUT = Path('C:/Users/0KKK0/Desktop/NAJIKA_VOLLSTAENDIGE_BASIS.txt')
OUT_ULTRA = Path('C:/Users/0KKK0/Desktop/NAJIKA_ULTRA_KOMPAKT.txt')
OUT_MITTEL = Path('C:/Users/0KKK0/Desktop/NAJIKA_MITTEL.txt')

# Wichtige Keywords für Kern-Konzepte
CORE_KEYWORDS = [
    # Najika Persönlichkeit
    'persönlichkeit', 'personality', 'megumin', 'shiro', 'facetten', 'facets',
    'harley', 'melissa', 'charakterzug', 'trait',

    # Kern-Systeme
    'schwarze windmühle', 'black mill', 'gesichert', 'secure',
    'oregon', 'prozedural', 'procedural',
    'explosion', 'kampf', 'combat',
    'digivice', 'modul', 'module',

    # Skill-Systeme
    'skill', 'skyrim', 'use-based', 'transformation', 'weaving',

    # Spiel-Ideen
    'spiel-idee', 'game concept', '8 gebiete', 'städte', 'cities',
    'fortnite', 'uefn', 'portal',

    # Wichtige Mechaniken
    'crafting', 'alchemie', 'housing', 'slime', 'begleiter'
]

print('NAJIKA PYRAMIDEN-KOMPRIMIERUNG...\n')

# Lese Original
content = INPUT.read_text(encoding='utf-8', errors='ignore')
print(f'Original: {len(content)} chars\n')

# Teile in Dokumente
docs = content.split('################################################################################')
doc_dict = {}

for doc in docs:
    if 'DOKUMENT:' in doc:
        lines = doc.split('\n')
        doc_name = None
        for line in lines:
            if 'DOKUMENT:' in line:
                doc_name = line.replace('DOKUMENT:', '').strip()
                break

        if doc_name:
            doc_dict[doc_name] = doc

print(f'Dokumente gefunden: {len(doc_dict)}\n')

# === ULTRA-KOMPAKT ===
print('Erstelle ULTRA-KOMPAKT (10k chars)...')

with open(OUT_ULTRA, 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA ULTRA-KOMPAKT - KERN-KONZEPTE\n')
    out.write('='*80 + '\n\n')

    for doc_name, doc_content in doc_dict.items():
        # Nur Absätze mit wichtigen Keywords
        paragraphs = [p.strip() for p in doc_content.split('\n\n') if len(p.strip()) > 50]

        important_paras = []
        for para in paragraphs:
            para_lower = para.lower()
            keyword_count = sum(1 for kw in CORE_KEYWORDS if kw in para_lower)

            if keyword_count >= 2:  # Mind. 2 Keywords
                important_paras.append((keyword_count, para))

        # Top 3 pro Dokument
        important_paras.sort(reverse=True, key=lambda x: x[0])
        top_paras = [p for score, p in important_paras[:3]]

        if top_paras:
            out.write(f'\n## {doc_name}\n')
            out.write('-'*80 + '\n\n')
            for para in top_paras:
                out.write(para[:400] + '\n\n')  # Max 400 chars pro Absatz

ultra_size = OUT_ULTRA.stat().st_size
print(f'  ULTRA: {ultra_size} chars\n')

# === MITTEL ===
print('Erstelle MITTEL (30k chars)...')

with open(OUT_MITTEL, 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA MITTEL - ERWEITERTE DETAILS\n')
    out.write('='*80 + '\n\n')

    for doc_name, doc_content in doc_dict.items():
        out.write(f'\n{"#"*80}\n')
        out.write(f'{doc_name}\n')
        out.write(f'{"#"*80}\n\n')

        # Ersten 3500 chars pro Dokument
        out.write(doc_content[:3500])
        if len(doc_content) > 3500:
            out.write('\n\n[...gekürzt...]')
        out.write('\n\n')

mittel_size = OUT_MITTEL.stat().st_size
print(f'  MITTEL: {mittel_size} chars\n')

print('FERTIG!')
print(f'\nPyramide erstellt:')
print(f'  1. ULTRA:  {ultra_size} chars (Kern-Konzepte)')
print(f'  2. MITTEL: {mittel_size} chars (Erweitert)')
print(f'  3. VOLL:   {len(content)} chars (Original)')
