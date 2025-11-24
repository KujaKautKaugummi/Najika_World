#!/usr/bin/env python3
"""
Najika World Map Scaler v2 - Skalierung auf 9.6km x 9.6km
==========================================================
Skaliert najika_world_UNIFIED.html von 133m auf 3200m pro Region
"""

import re
import sys
from pathlib import Path

# UTF-8 für Windows Console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def scale_map(content):
    """Skaliert Map von 133m auf 3200m"""

    changes = []

    # 1. Region-Größe: 133.32 → 3200
    old_pattern = r'const regionSize = 133\.32;'
    new_value = 'const regionSize = 3200;'
    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_value, content)
        changes.append('[OK] regionSize: 133.32 -> 3200')

    # 2. Region-Positionen (9 Stück)
    # Ice (top-left)
    content, found = replace_if_found(content, r'x: -133\.32, z: 133\.32,', 'x: -3200, z: 3200,')
    if found: changes.append('[OK] Ice position: (-133.32, 133.32) -> (-3200, 3200)')

    # Highland (top-center)
    content, found = replace_if_found(content, r'x: 0,\s+z: 133\.32,', 'x: 0,     z: 3200,')
    if found: changes.append('[OK] Highland position: (0, 133.32) -> (0, 3200)')

    # Desert (top-right)
    content, found = replace_if_found(content, r'x: 133\.32,\s+z: 133\.32,', 'x: 3200,  z: 3200,')
    if found: changes.append('[OK] Desert position: (133.32, 133.32) -> (3200, 3200)')

    # Swamp (middle-left)
    content, found = replace_if_found(content, r'x: -133\.32, z: 0,', 'x: -3200, z: 0,')
    if found: changes.append('[OK] Swamp position: (-133.32, 0) -> (-3200, 0)')

    # Mountain (center) - WICHTIG: y auch ändern!
    content, found = replace_if_found(content, r'x: 0, z: 0,\s+y: 5', 'x: 0, z: 0, y: 50')
    if found: changes.append('[OK] Mountain position: (0, 0, 5) -> (0, 0, 50) [BERG 10x HOEHER!]')

    # Coast (middle-right)
    content, found = replace_if_found(content, r'x: 133\.32,\s+z: 0,', 'x: 3200,  z: 0,')
    if found: changes.append('[OK] Coast position: (133.32, 0) -> (3200, 0)')

    # Caves (bottom-left)
    content, found = replace_if_found(content, r'x: -133\.32, z: -133\.32,', 'x: -3200, z: -3200,')
    if found: changes.append('[OK] Caves position: (-133.32, -133.32) -> (-3200, -3200)')

    # Forest (bottom-center)
    content, found = replace_if_found(content, r'x: 0,\s+z: -133\.32,', 'x: 0,     z: -3200,')
    if found: changes.append('[OK] Forest position: (0, -133.32) -> (0, -3200)')

    # Volcano (bottom-right)
    content, found = replace_if_found(content, r'x: 133\.32,\s+z: -133\.32,', 'x: 3200,  z: -3200,')
    if found: changes.append('[OK] Volcano position: (133.32, -133.32) -> (3200, -3200)')

    # 3. Grid-Größe: 400 → 9600
    content, found = replace_if_found(content, r'const gridHelper = new THREE\.GridHelper\(400, 80,',
                                     'const gridHelper = new THREE.GridHelper(9600, 200,')
    if found: changes.append('[OK] Grid size: 400 -> 9600 (mit mehr Grid-Lines: 80 -> 200)')

    # 4. Kamera-Position (weiter weg für große Map)
    # Pattern: camera.position.set(0, 50, 100);
    content, found = replace_if_found(content, r'camera\.position\.set\(0, 50, 100\)',
                                     'camera.position.set(0, 300, 400)')
    if found: changes.append('[OK] Kamera-Position: (0, 50, 100) -> (0, 300, 400)')

    # 5. Shadow Camera (größere Frustum für große Map)
    replacements = [
        (r'directionalLight\.shadow\.camera\.left = -150;', 'directionalLight.shadow.camera.left = -5000;'),
        (r'directionalLight\.shadow\.camera\.right = 150;', 'directionalLight.shadow.camera.right = 5000;'),
        (r'directionalLight\.shadow\.camera\.top = 150;', 'directionalLight.shadow.camera.top = 5000;'),
        (r'directionalLight\.shadow\.camera\.bottom = -150;', 'directionalLight.shadow.camera.bottom = -5000;'),
    ]

    for pattern, replacement in replacements:
        content, found = replace_if_found(content, pattern, replacement)
        if found:
            changes.append(f'[OK] Shadow camera: {replacement.split("=")[0].strip()}')

    # 6. Bewegungs-Geschwindigkeit
    # Suche nach moveSpeed, velocity, speed etc.
    speed_patterns = [
        (r'const moveSpeed = 20;', 'const moveSpeed = 80;', '20 -> 80'),
        (r'const moveSpeed = 40;', 'const moveSpeed = 160;', '40 -> 160'),
        (r'velocity = 20', 'velocity = 80', 'velocity 20 -> 80'),
    ]

    for pattern, replacement, desc in speed_patterns:
        content, found = replace_if_found(content, pattern, replacement)
        if found:
            changes.append(f'[OK] Movement speed: {desc}')

    # 7. Enemy-Spawn-Bereich: ±50 → ±1500
    # Pattern: Math.random() * 100 - 50
    content, count = re.subn(r'Math\.random\(\) \* 100 - 50', 'Math.random() * 3000 - 1500', content)
    if count > 0:
        changes.append(f'[OK] Enemy spawn range: +/-50 -> +/-1500 ({count} Stellen)')

    # 8. Andere Random-Spawns
    content, count = re.subn(r'Math\.random\(\) \* 200 - 100', 'Math.random() * 6000 - 3000', content)
    if count > 0:
        changes.append(f'[OK] Random range: +/-100 -> +/-3000 ({count} Stellen)')

    # 9. Character spawn position (falls bei y=8.5 zu nah am Boden)
    content, found = replace_if_found(content, r'character\.position\.set\(0, 8\.5, 0\)',
                                     'character.position.set(0, 55, 0)')
    if found:
        changes.append('[OK] Character spawn: y=8.5 -> y=55 (auf Berg-Höhe)')

    # 10. Title anpassen
    content, found = replace_if_found(content, r'<title>.*?9 Regions.*?</title>',
                                     '<title>Najika World - 9.6km x 9.6km Open World (Fortnite BR Scale x1.75)</title>')
    if found:
        changes.append('[OK] Title updated')

    # 11. Minimap-Scale (falls vorhanden)
    content, found = replace_if_found(content, r'const minimapScale = 0\.05', 'const minimapScale = 0.02')
    if found:
        changes.append('[OK] Minimap scale: 0.05 -> 0.02')

    return content, changes

def replace_if_found(content, pattern, replacement):
    """Ersetzt Pattern und gibt (content, found) zurück"""
    new_content = re.sub(pattern, replacement, content)
    found = new_content != content
    return new_content, found

def main():
    """Main function"""

    print('[+] Najika World Map Scaler v2')
    print('[+] Skalierung: 133m -> 3200m pro Region (24x)')
    print('=' * 60)

    # Pfad zur HTML-Datei
    html_path = Path(__file__).parent / 'digivice' / 'najika_world_UNIFIED.html'

    if not html_path.exists():
        print(f'[X] Datei nicht gefunden: {html_path}')
        sys.exit(1)

    print(f'[>] Lade: {html_path}')

    # HTML laden
    with open(html_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    print(f'[~] Original: {len(original_content):,} Bytes')

    # Backup erstellen
    backup_path = html_path.with_suffix('.html.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f'[*] Backup: {backup_path}')

    print('\n[+] Starte Skalierung...\n')

    # Skalieren
    scaled_content, changes = scale_map(original_content)

    # Ausgabe der Änderungen
    for change in changes:
        print(f'  {change}')

    # Speichern
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(scaled_content)

    print(f'\n[OK] Erfolgreich gespeichert!')
    print(f'[~] Neue Groesse: {len(scaled_content):,} Bytes')
    print(f'[+] {len(changes)} Aenderungen durchgefuehrt')

    print('\n' + '=' * 60)
    print('[!] NAECHSTE SCHRITTE:')
    print('  1. Oeffne najika_world_UNIFIED.html im Browser')
    print('  2. Pruefe JavaScript Console (F12)')
    print('  3. Teste WASD-Bewegung (sollte 4x schneller sein)')
    print('  4. Pruefe Map-Groesse visuell')
    print('  5. Falls Probleme: Backup aus .html.backup wiederherstellen')

    print('\n[>>] Map-Groesse: 3200m x 3200m pro Region')
    print('[>>] Gesamt: 9600m x 9600m (9.6km x 9.6km)')
    print('[>>] Fortnite BR Vergleich: 5.5km -> Najika ist 1.75x groesser!')
    print('=' * 60)

if __name__ == '__main__':
    main()
