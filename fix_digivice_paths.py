#!/usr/bin/env python3
"""
Fix Digivice index.html Paths
==============================
Problem: Pfade starten mit /digivice/ aber Server läuft IN digivice/
Lösung: Entferne /digivice/ Prefix von allen Pfaden
"""

import re
from pathlib import Path

def fix_paths(content):
    """Fixe alle /digivice/ Pfade"""

    changes = []

    # Pattern: src="/digivice/..." oder href="/digivice/..."
    # Ersetze mit: src="..." oder href="..."

    patterns = [
        (r'src="/digivice/', 'src="'),
        (r'href="/digivice/', 'href="'),
        (r'url\("/digivice/', 'url("'),
    ]

    for old_pattern, new_pattern in patterns:
        count = len(re.findall(old_pattern, content))
        if count > 0:
            content = re.sub(old_pattern, new_pattern, content)
            changes.append(f'[OK] {old_pattern} -> {new_pattern} ({count} Stellen)')

    return content, changes

def main():
    html_path = Path(__file__).parent / 'digivice' / 'index.html'

    if not html_path.exists():
        print(f'[X] Datei nicht gefunden: {html_path}')
        return

    print('[+] Lade index.html...')
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f'[~] Original: {len(content):,} Bytes')

    # Backup
    backup_path = html_path.with_suffix('.html.backup_paths')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'[*] Backup: {backup_path}')

    # Fix
    print('\n[+] Fixe Pfade...\n')
    fixed_content, changes = fix_paths(content)

    for change in changes:
        print(f'  {change}')

    # Save
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f'\n[OK] Gespeichert!')
    print(f'[~] Neue Groesse: {len(fixed_content):,} Bytes')
    print(f'[+] {len(changes)} Aenderungen durchgefuehrt')

    print('\n[!] Naechste Schritte:')
    print('  1. Teste: START_NAJIKA_GAME.bat')
    print('  2. Oeffne: http://localhost:5173/index.html')
    print('  3. Pruefe Console (F12) - sollte keine 404 mehr haben!')

if __name__ == '__main__':
    main()
