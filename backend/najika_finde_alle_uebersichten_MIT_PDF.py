#!/usr/bin/env python3
"""
NAJIKA AUFGABE 1 FIXED: Finde ALLE Übersichten/Roadmaps/Zusammenfassungen
MIT PDF-SUPPORT!
"""
from pathlib import Path
import PyPDF2

SEARCH_DIRS = [
    Path('C:/Najika_World'),
    Path('C:/Users/0KKK0/Desktop'),
    Path('C:/Users/0KKK0/Desktop/zip'),
    Path('C:/Users/0KKK0/Desktop/jetzt'),
    Path('C:/Users/0KKK0/.claude')
]

DESKTOP = Path('C:/Users/0KKK0/Desktop')
OUTPUT = DESKTOP / 'NAJIKA_ALLE_UEBERSICHTEN_KOMPLETT.txt'

# Nur diese Schlagwörter
KEYWORDS = [
    'zusammenfassung', 'zusammenfassungen',
    'übersicht', 'uebersicht',
    'roadmap',
    'projekt', 'project',
    'final', 'finale',
    'master',
    'complete', 'komplett',
    'summary'
]

print('='*80)
print('NAJIKA: Finde ALLE Übersichten/Roadmaps/Zusammenfassungen (MIT PDF!)')
print('='*80)

gefunden = []

for search_dir in SEARCH_DIRS:
    if not search_dir.exists():
        print(f'[SKIP] {search_dir} existiert nicht')
        continue

    print(f'\n[SUCHE] {search_dir}...')

    # Durchsuche rekursiv
    for pattern in ['*.txt', '*.md', '*.pdf']:
        for file in search_dir.rglob(pattern):
            # Ignoriere zu kleine Files
            if file.stat().st_size < 500:
                continue

            # Prüfe ob Dateiname eines der Keywords enthält
            file_name_lower = file.name.lower()

            for keyword in KEYWORDS:
                if keyword in file_name_lower:
                    gefunden.append({
                        'file': file,
                        'name': file.name,
                        'size': file.stat().st_size,
                        'keyword': keyword,
                        'quelle': str(search_dir)
                    })
                    print(f'  [GEFUNDEN] {file.name} ({keyword})')
                    break

# Dedupliziere (gleiche Files)
unique = {}
for item in gefunden:
    key = f"{item['name']}_{item['size']}"
    if key not in unique:
        unique[key] = item

gefunden = list(unique.values())

# Sortiere nach Größe (größere zuerst = mehr Inhalt)
gefunden.sort(key=lambda x: x['size'], reverse=True)

print(f'\n[OK] Insgesamt {len(gefunden)} Dokumente gefunden!')

# Erstelle Ausgabe
lines = []
lines.append('='*80)
lines.append('NAJIKA - ALLE UEBERSICHTEN/ROADMAPS/ZUSAMMENFASSUNGEN')
lines.append('='*80)
lines.append(f'Gefunden: {len(gefunden)} Dokumente')
lines.append('')
lines.append('='*80)
lines.append('')

for idx, item in enumerate(gefunden, 1):
    lines.append(f'\n{"#"*80}')
    lines.append(f'DOKUMENT {idx}: {item["name"]}')
    lines.append(f'Quelle: {item["quelle"]}')
    lines.append(f'Groesse: {item["size"]:,} bytes')
    lines.append(f'Keyword: {item["keyword"]}')
    lines.append(f'{"#"*80}\n')

    try:
        # PDF lesen
        if item['file'].suffix == '.pdf':
            try:
                with open(item['file'], 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text_parts = []

                    # Lese alle Seiten
                    for page_num, page in enumerate(reader.pages):
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)

                    full_text = '\n\n'.join(text_parts)

                    # Max 25.000 chars
                    if len(full_text) > 25000:
                        lines.append(full_text[:25000])
                        lines.append(f'\n\n[... GEKUERZT - Original {len(full_text):,} chars, {len(reader.pages)} Seiten ...]')
                    else:
                        lines.append(full_text)

                    print(f'    [PDF OK] {item["name"]} - {len(reader.pages)} Seiten extrahiert')

            except Exception as e:
                lines.append(f'[FEHLER beim PDF-Lesen: {e}]')
                print(f'    [PDF FEHLER] {item["name"]} - {e}')

        # TXT/MD lesen
        else:
            text = item['file'].read_text(encoding='utf-8', errors='ignore')

            # Max 25.000 chars pro Dokument
            if len(text) > 25000:
                lines.append(text[:25000])
                lines.append(f'\n\n[... GEKUERZT - Original {len(text):,} chars ...]')
            else:
                lines.append(text)

    except Exception as e:
        lines.append(f'[FEHLER beim Lesen: {e}]')

    lines.append('\n')

# Abschluss
lines.append('\n' + '='*80)
lines.append(f'ENDE - {len(gefunden)} Dokumente')
lines.append('='*80)

# Speichern
OUTPUT.write_text('\n'.join(lines), encoding='utf-8', errors='ignore')

print('\n' + '='*80)
print('FERTIG!')
print('='*80)
print(f'\nGespeichert: {OUTPUT}')
print(f'Dokumente: {len(gefunden)}')
print(f'Groesse: {OUTPUT.stat().st_size:,} bytes')
print('='*80)
