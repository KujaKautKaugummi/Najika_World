#!/usr/bin/env python3
"""
NAJIKA: Sammle ALLE Roadmaps + Zusammenfassungen
Speichere auf Desktop in EINEM Dokument
"""
from pathlib import Path
import json

NAJIKACORE = Path('C:/NajikaCore')
ZIP_DIR = Path('C:/Users/0KKK0/Desktop/zip')
JETZT_DIR = Path('C:/Users/0KKK0/Desktop/jetzt')
DESKTOP = Path('C:/Users/0KKK0/Desktop')

OUTPUT = DESKTOP / 'NAJIKA_ALLE_ROADMAPS_UND_ZUSAMMENFASSUNGEN.txt'

print('='*80)
print('NAJIKA: Sammle ALLE Roadmaps + Zusammenfassungen')
print('='*80)

content = []
content.append('='*80)
content.append('NAJIKA - ALLE ROADMAPS & ZUSAMMENFASSUNGEN')
content.append('='*80)
content.append(f'Erstellt: 2025-10-19')
content.append('')
content.append('---')
content.append('')

# Zähler
docs_found = 0

# 1. NajikaCore durchsuchen
print('\n[1/3] Durchsuche NajikaCore...')
for pattern in ['*roadmap*', '*zusammenfassung*', '*übersicht*', '*summary*', '*master*']:
    for file in NAJIKACORE.glob(pattern):
        if file.suffix in ['.md', '.txt'] and file.stat().st_size > 100:
            docs_found += 1
            content.append(f'\n{"#"*80}')
            content.append(f'DOKUMENT {docs_found}: {file.name}')
            content.append(f'Quelle: NajikaCore')
            content.append(f'Größe: {file.stat().st_size:,} bytes')
            content.append(f'{"#"*80}\n')

            try:
                text = file.read_text(encoding='utf-8', errors='ignore')
                content.append(text)
            except:
                content.append('[FEHLER beim Lesen]')

            content.append('\n')
            print(f'  [OK] {file.name}')

# 2. ZIP-Ordner durchsuchen
print('\n[2/3] Durchsuche ZIP-Ordner...')
if ZIP_DIR.exists():
    for pattern in ['*roadmap*', '*zusammenfassung*', '*übersicht*', '*projekt*', '*plan*']:
        for file in ZIP_DIR.glob(pattern):
            if file.suffix in ['.txt'] and file.stat().st_size > 500:
                docs_found += 1
                content.append(f'\n{"#"*80}')
                content.append(f'DOKUMENT {docs_found}: {file.name}')
                content.append(f'Quelle: ZIP-Ordner')
                content.append(f'Größe: {file.stat().st_size:,} bytes')
                content.append(f'{"#"*80}\n')

                try:
                    text = file.read_text(encoding='utf-8', errors='ignore')
                    # Max 20.000 chars pro Dokument
                    if len(text) > 20000:
                        content.append(text[:20000])
                        content.append('\n\n[... GEKÜRZT - Zu lang, erste 20.000 chars gezeigt ...]')
                    else:
                        content.append(text)
                except:
                    content.append('[FEHLER beim Lesen]')

                content.append('\n')
                print(f'  [OK] {file.name}')

# 3. JETZT-Ordner durchsuchen
print('\n[3/3] Durchsuche JETZT-Ordner...')
if JETZT_DIR.exists():
    for pattern in ['*roadmap*', '*zusammenfassung*', '*übersicht*']:
        for file in JETZT_DIR.glob(pattern):
            if file.suffix in ['.txt'] and file.stat().st_size > 500:
                docs_found += 1
                content.append(f'\n{"#"*80}')
                content.append(f'DOKUMENT {docs_found}: {file.name}')
                content.append(f'Quelle: JETZT-Ordner')
                content.append(f'Größe: {file.stat().st_size:,} bytes')
                content.append(f'{"#"*80}\n')

                try:
                    text = file.read_text(encoding='utf-8', errors='ignore')
                    if len(text) > 20000:
                        content.append(text[:20000])
                        content.append('\n\n[... GEKÜRZT - Zu lang, erste 20.000 chars gezeigt ...]')
                    else:
                        content.append(text)
                except:
                    content.append('[FEHLER beim Lesen]')

                content.append('\n')
                print(f'  [OK] {file.name}')

# Spezielle Dokumente
print('\n[BONUS] Füge spezielle Dokumente hinzu...')

# GRUNDSTEIN_INVENTAR
grundstein = NAJIKACORE / 'GRUNDSTEIN_INVENTAR.md'
if grundstein.exists():
    docs_found += 1
    content.append(f'\n{"#"*80}')
    content.append(f'DOKUMENT {docs_found}: GRUNDSTEIN_INVENTAR.md')
    content.append(f'Quelle: NajikaCore (WICHTIG!)')
    content.append(f'{"#"*80}\n')
    content.append(grundstein.read_text(encoding='utf-8'))
    content.append('\n')
    print('  [OK] GRUNDSTEIN_INVENTAR.md')

# MASTER_ZUSAMMENFASSUNG
master = NAJIKACORE / 'NAJIKA_MASTER_ZUSAMMENFASSUNG.md'
if master.exists():
    docs_found += 1
    content.append(f'\n{"#"*80}')
    content.append(f'DOKUMENT {docs_found}: NAJIKA_MASTER_ZUSAMMENFASSUNG.md')
    content.append(f'Quelle: NajikaCore (MASTER)')
    content.append(f'{"#"*80}\n')
    content.append(master.read_text(encoding='utf-8'))
    content.append('\n')
    print('  [OK] NAJIKA_MASTER_ZUSAMMENFASSUNG.md')

# GELERNT_AUS_ALLEN_SESSIONS
learned = NAJIKACORE / 'GELERNT_AUS_ALLEN_SESSIONS.md'
if learned.exists():
    docs_found += 1
    content.append(f'\n{"#"*80}')
    content.append(f'DOKUMENT {docs_found}: GELERNT_AUS_ALLEN_SESSIONS.md')
    content.append(f'Quelle: NajikaCore (Lektionen)')
    content.append(f'{"#"*80}\n')
    content.append(learned.read_text(encoding='utf-8'))
    content.append('\n')
    print('  [OK] GELERNT_AUS_ALLEN_SESSIONS.md')

# VOLLSTÄNDIGE_BASIS (wenn vorhanden)
vollstaendig = Path('C:/Users/0KKK0/Desktop/NAJIKA_VOLLSTAENDIGE_BASIS.txt')
if vollstaendig.exists():
    docs_found += 1
    content.append(f'\n{"#"*80}')
    content.append(f'DOKUMENT {docs_found}: NAJIKA_VOLLSTAENDIGE_BASIS.txt')
    content.append(f'Quelle: Desktop (5 PDFs + 3 TXTs)')
    content.append(f'Größe: {vollstaendig.stat().st_size:,} bytes')
    content.append(f'{"#"*80}\n')

    text = vollstaendig.read_text(encoding='utf-8', errors='ignore')
    # Diese ist wichtig - erste 30k chars
    if len(text) > 30000:
        content.append(text[:30000])
        content.append('\n\n[... GEKÜRZT - Erste 30.000 chars gezeigt ...]')
    else:
        content.append(text)
    content.append('\n')
    print('  [OK] NAJIKA_VOLLSTAENDIGE_BASIS.txt')

# Abschluss
content.append('\n')
content.append('='*80)
content.append(f'ENDE - Insgesamt {docs_found} Dokumente gesammelt')
content.append('='*80)

# Speichern
OUTPUT.write_text('\n'.join(content), encoding='utf-8', errors='ignore')

print('\n' + '='*80)
print('FERTIG!')
print('='*80)
print(f'\nGespeichert: {OUTPUT}')
print(f'Dokumente gesammelt: {docs_found}')
print(f'Größe: {OUTPUT.stat().st_size:,} bytes')
print('\n✓ Bereit zum Durchlesen!')
print('='*80)
