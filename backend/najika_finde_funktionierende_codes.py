#!/usr/bin/env python3
"""
NAJIKA AUFGABE 2: Finde ALLE funktionierenden Codes
Prüfe ob Code funktioniert (Syntax-Check)
"""
from pathlib import Path
import ast
import json
import re

SEARCH_DIRS = [
    Path('C:/NajikaCore'),
    Path('C:/Users/0KKK0/Desktop/zip')
]

DESKTOP = Path('C:/Users/0KKK0/Desktop')
OUTPUT = DESKTOP / 'NAJIKA_ALLE_FUNKTIONIERENDEN_CODES.txt'

print('='*80)
print('NAJIKA: Finde ALLE funktionierenden Codes')
print('='*80)

gefundene_codes = []

for search_dir in SEARCH_DIRS:
    if not search_dir.exists():
        continue

    print(f'\n[SUCHE] {search_dir}...')

    # Python-Files
    for py_file in search_dir.rglob('*.py'):
        if py_file.stat().st_size < 100:  # Zu klein
            continue

        try:
            code = py_file.read_text(encoding='utf-8')

            # Syntax-Check
            ast.parse(code)

            # Code funktioniert syntaktisch!
            gefundene_codes.append({
                'file': py_file,
                'name': py_file.name,
                'type': 'Python',
                'size': len(code),
                'quelle': str(search_dir),
                'code': code,
                'status': 'SYNTAX OK'
            })

            print(f'  [OK] {py_file.name} - Python Syntax korrekt')

        except SyntaxError as e:
            print(f'  [FEHLER] {py_file.name} - Syntax-Fehler: {e}')
        except Exception as e:
            print(f'  [SKIP] {py_file.name} - {e}')

    # JavaScript-Files
    for js_file in search_dir.rglob('*.js'):
        if js_file.stat().st_size < 100:
            continue

        try:
            code = js_file.read_text(encoding='utf-8', errors='ignore')

            # Basis-Check: Klammern müssen passen
            if code.count('{') == code.count('}') and code.count('(') == code.count(')'):
                gefundene_codes.append({
                    'file': js_file,
                    'name': js_file.name,
                    'type': 'JavaScript',
                    'size': len(code),
                    'quelle': str(search_dir),
                    'code': code,
                    'status': 'KLAMMERN OK'
                })
                print(f'  [OK] {js_file.name} - JavaScript Klammern OK')
            else:
                print(f'  [FEHLER] {js_file.name} - Klammern passen nicht')

        except Exception as e:
            print(f'  [SKIP] {js_file.name} - {e}')

    # HTML-Files (nur die mit vollständiger Struktur)
    for html_file in search_dir.rglob('*.html'):
        if html_file.stat().st_size < 500:
            continue

        try:
            code = html_file.read_text(encoding='utf-8', errors='ignore')

            # Check: Muss <!DOCTYPE>, <html>, <head>, <body> haben
            if all(tag in code.lower() for tag in ['<!doctype', '<html', '<head', '<body']):
                gefundene_codes.append({
                    'file': html_file,
                    'name': html_file.name,
                    'type': 'HTML',
                    'size': len(code),
                    'quelle': str(search_dir),
                    'code': code,
                    'status': 'VOLLSTÄNDIG'
                })
                print(f'  [OK] {html_file.name} - HTML vollständig')

        except Exception as e:
            print(f'  [SKIP] {html_file.name} - {e}')

# Sortiere nach Typ, dann Größe
gefundene_codes.sort(key=lambda x: (x['type'], -x['size']))

print(f'\n[OK] Insgesamt {len(gefundene_codes)} funktionierende Codes gefunden!')
print(f'  - Python: {sum(1 for c in gefundene_codes if c["type"] == "Python")}')
print(f'  - JavaScript: {sum(1 for c in gefundene_codes if c["type"] == "JavaScript")}')
print(f'  - HTML: {sum(1 for c in gefundene_codes if c["type"] == "HTML")}')

# Erstelle Ausgabe
lines = []
lines.append('='*80)
lines.append('NAJIKA - ALLE FUNKTIONIERENDEN CODES')
lines.append('='*80)
lines.append(f'Gefunden: {len(gefundene_codes)} Codes')
lines.append(f'  - Python: {sum(1 for c in gefundene_codes if c["type"] == "Python")}')
lines.append(f'  - JavaScript: {sum(1 for c in gefundene_codes if c["type"] == "JavaScript")}')
lines.append(f'  - HTML: {sum(1 for c in gefundene_codes if c["type"] == "HTML")}')
lines.append('')
lines.append('='*80)
lines.append('')

for idx, item in enumerate(gefundene_codes, 1):
    lines.append(f'\n{"#"*80}')
    lines.append(f'CODE {idx}: {item["name"]} ({item["type"]})')
    lines.append(f'Quelle: {item["quelle"]}')
    lines.append(f'Größe: {item["size"]:,} Zeichen')
    lines.append(f'Status: {item["status"]}')
    lines.append(f'{"#"*80}\n')

    # Code einfügen
    lines.append(f'```{item["type"].lower()}')
    lines.append(item['code'])
    lines.append('```')
    lines.append('\n')

# Abschluss
lines.append('\n' + '='*80)
lines.append(f'ENDE - {len(gefundene_codes)} funktionierende Codes')
lines.append('='*80)

# Speichern
OUTPUT.write_text('\n'.join(lines), encoding='utf-8', errors='ignore')

print('\n' + '='*80)
print('FERTIG!')
print('='*80)
print(f'\nGespeichert: {OUTPUT}')
print(f'Codes: {len(gefundene_codes)}')
print(f'Größe: {OUTPUT.stat().st_size:,} bytes')
print('='*80)
