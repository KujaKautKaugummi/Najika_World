#!/usr/bin/env python3
"""
NAJIKA: Lese 5 PDFs + 3 TXTs und erstelle Zusammenfassung für Claude
"""
from pathlib import Path
import PyPDF2

JETZT = Path('C:/Users/0KKK0/Desktop/jetzt')
OUTPUT = Path('C:/Users/0KKK0/Desktop/NAJIKA_VOLLSTAENDIGE_BASIS.txt')

PDFS = [
    'Projekt Najika – Allumfassende Übersicht.pdf',
    'Najika Projekt – Umfassende Detailübersicht.pdf',
    'Umfassende detaillierte Projektübersicht.pdf',
    'Umfassende Projektübersicht und Replizierungsanleitung.pdf',
    'Projektübersicht __Najika__ – Technik & Konzept.pdf'
]

TXTS = ['121.txt', 'gerade installiert.txt', 'roadmap.txt']

print('NAJIKA: Extrahiere PDFs + TXTs...\n')

all_content = {}

# Lese TXTs
print('=== TXT-DATEIEN ===')
for txt_name in TXTS:
    txt_path = JETZT / txt_name
    if txt_path.exists():
        try:
            content = txt_path.read_text(encoding='utf-8', errors='ignore')
            all_content[txt_name] = content
            print(f'OK: {txt_name} ({len(content)} chars)')
        except Exception as e:
            print(f'FEHLER: {txt_name} - {e}')

# Lese PDFs
print('\n=== PDF-DATEIEN ===')
for pdf_name in PDFS:
    pdf_path = JETZT / pdf_name
    if pdf_path.exists():
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text_parts = []
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)

                full_text = '\n\n'.join(text_parts)
                all_content[pdf_name] = full_text
                print(f'OK: {pdf_name} ({len(full_text)} chars, {len(reader.pages)} Seiten)')
        except Exception as e:
            print(f'FEHLER: {pdf_name} - {e}')

print(f'\n=== GESAMT ===')
print(f'Dokumente: {len(all_content)}')
total_chars = sum(len(c) for c in all_content.values())
print(f'Zeichen: {total_chars}')

# Schreibe Zusammenfassung
print(f'\n=== ERSTELLE ZUSAMMENFASSUNG ===')

with open(OUTPUT, 'w', encoding='utf-8') as out:
    out.write('='*80 + '\n')
    out.write('NAJIKA VOLLSTAENDIGE BASIS - 5 PDFs + 3 TXTs\n')
    out.write('='*80 + '\n')
    out.write(f'Extrahiert: {total_chars} Zeichen\n')
    out.write('='*80 + '\n\n')

    for doc_name, content in all_content.items():
        out.write(f'\n{"#"*80}\n')
        out.write(f'DOKUMENT: {doc_name}\n')
        out.write(f'{"#"*80}\n\n')

        # Ersten 8000 chars pro Dokument
        out.write(content[:8000])
        if len(content) > 8000:
            out.write(f'\n\n[...GEKUERZT - Original: {len(content)} chars...]')
        out.write('\n\n')

final_size = OUTPUT.stat().st_size
print(f'Fertig! Gespeichert: {OUTPUT}')
print(f'Groesse: {final_size} chars')
