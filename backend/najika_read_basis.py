#!/usr/bin/env python3
"""
NAJIKA: Lese die BASIS-Dokumente (5 PDFs + 3 TXTs)
Erstelle Zusammenfassung für Claude
"""
from pathlib import Path
import re

JETZT_DIR = Path('C:/Users/0KKK0/Desktop/jetzt')

PDFS = [
    'Projekt Najika – Allumfassende Übersicht.pdf',
    'Najika Projekt – Umfassende Detailübersicht.pdf',
    'Umfassende detaillierte Projektübersicht.pdf',
    'Umfassende Projektübersicht und Replizierungsanleitung.pdf',
    'Projektübersicht __Najika__ – Technik & Konzept.pdf'
]

TXTS = [
    '121.txt',
    'gerade installiert.txt',
    'roadmap.txt'
]

OUTPUT = 'C:/Users/0KKK0/Desktop/NAJIKA_BASIS_FUER_CLAUDE.txt'

# Keywords für wichtige Abschnitte
IMPORTANT_KEYWORDS = [
    'skill system', 'skill-weaving', 'skyrim', 'use-based', 'transformation',
    'soulframe', 'kampfsystem', 'combat', 'digimon world', 'dark souls',
    '8 gebiete', 'crimson desert', 'stadt', 'prozedural',
    'fortnite', 'uefn', 'portal', 'universum',
    'slime', 'begleiter', 'companion', 'pet',
    'klassen', 'explosion', 'megumin',
    'crafting', 'alchemie', 'housing',
    'spiel-idee', 'spiel idee', 'game concept', 'konzept'
]

print('NAJIKA: Lese BASIS-Dokumente...\n')

all_content = {}

# Lese TXTs
print('TXT-Dateien:')
for txt_name in TXTS:
    txt_path = JETZT_DIR / txt_name
    if txt_path.exists():
        try:
            content = txt_path.read_text(encoding='utf-8', errors='ignore')
            all_content[txt_name] = content
            print(f'  ✓ {txt_name} ({len(content)} chars)')
        except Exception as e:
            print(f'  ✗ {txt_name} - Fehler: {e}')

# Lese PDFs (als Text wenn möglich)
print('\nPDF-Dateien:')
for pdf_name in PDFS:
    pdf_path = JETZT_DIR / pdf_name
    if pdf_path.exists():
        try:
            # Versuche PDF als Text zu lesen (funktioniert bei manchen PDFs)
            content = pdf_path.read_text(encoding='utf-8', errors='ignore')
            if len(content) > 1000:  # Wenn genug Text extrahiert
                all_content[pdf_name] = content
                print(f'  ✓ {pdf_name} ({len(content)} chars)')
            else:
                print(f'  ! {pdf_name} - Binär-PDF, kann nicht als Text gelesen werden')
                # Marker setzen dass es existiert
                all_content[pdf_name] = f'[PDF EXISTS: {pdf_name} - Binäres Format]'
        except Exception as e:
            print(f'  ✗ {pdf_name} - Fehler: {e}')

print(f'\nGelesen: {len(all_content)} Dokumente')
total_chars = sum(len(c) for c in all_content.values())
print(f'Gesamt: {total_chars} Zeichen\n')

# Extrahiere wichtige Abschnitte
print('Extrahiere wichtige Abschnitte...')

important_sections = {}

for doc_name, content in all_content.items():
    if '[PDF EXISTS' in content:
        continue  # Skip binäre PDFs

    content_lower = content.lower()

    # Finde Absätze mit wichtigen Keywords
    paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 50]

    relevant_paras = []
    for para in paragraphs:
        para_lower = para.lower()
        # Zähle Keywords
        keyword_count = sum(1 for kw in IMPORTANT_KEYWORDS if kw in para_lower)

        if keyword_count >= 2:  # Mindestens 2 Keywords
            relevant_paras.append((keyword_count, para))

    # Top 10 Absätze pro Dokument
    relevant_paras.sort(reverse=True, key=lambda x: x[0])
    important_sections[doc_name] = [para for score, para in relevant_paras[:10]]

# Schreibe Zusammenfassung
with open(OUTPUT, 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA BASIS-DOKUMENTE - ZUSAMMENFASSUNG FÜR CLAUDE\n')
    out.write('='*80 + '\n')
    out.write(f'Quelle: 5 PDFs + 3 TXTs aus Desktop/jetzt\n')
    out.write(f'Extrahiert: {total_chars} Zeichen komprimiert\n')
    out.write('='*80 + '\n\n')

    for doc_name, sections in important_sections.items():
        if not sections:
            continue

        out.write(f'\n{"#"*80}\n')
        out.write(f'DOKUMENT: {doc_name}\n')
        out.write(f'{"#"*80}\n\n')

        for i, section in enumerate(sections, 1):
            out.write(f'[{i}] {section[:800]}\n')  # Max 800 chars
            if len(section) > 800:
                out.write('    [...gekürzt...]\n')
            out.write('\n')

    # Binäre PDFs hinzufügen
    binary_pdfs = [name for name, content in all_content.items() if '[PDF EXISTS' in content]
    if binary_pdfs:
        out.write(f'\n{"="*80}\n')
        out.write('HINWEIS: Folgende PDFs sind binär und können nicht automatisch gelesen werden:\n')
        out.write('='*80 + '\n\n')
        for pdf in binary_pdfs:
            out.write(f'  - {pdf}\n')
        out.write('\n(User muss diese manuell öffnen oder mit PDF-Tool extrahieren)\n\n')

final_size = Path(OUTPUT).stat().st_size
print(f'\nFERTIG!')
print(f'Zusammenfassung: {final_size} Zeichen')
print(f'Gespeichert: {OUTPUT}')
