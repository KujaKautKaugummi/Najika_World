#!/usr/bin/env python3
"""
Najika World Map Scaler - Automatische Skalierung auf 9.6km x 9.6km
=================================================================

Input:  digivice/najika_world_UNIFIED.html (133m map)
Output: digivice/najika_world_UNIFIED.html (9600m map)

Änderungen:
1. Map-Größe: 133m → 3200m pro Region (24x)
2. Alle Koordinaten skalieren (x, z)
3. Kamera-Geschwindigkeit erhöhen
4. Enemy-Spawn-Bereiche skalieren
5. World bounds anpassen
6. Minimap-Scale anpassen
"""

import re
import sys
from pathlib import Path

# Konstanten
OLD_REGION_SIZE = 133  # Alte Größe
NEW_REGION_SIZE = 3200  # Neue Größe (3.2km)
SCALE_FACTOR = NEW_REGION_SIZE / OLD_REGION_SIZE  # ~24x

OLD_WORLD_SIZE = 400  # Geschätzt
NEW_WORLD_SIZE = 9600  # 9.6km

def scale_coordinate(value, scale=SCALE_FACTOR):
    """Skaliert einen numerischen Wert"""
    return int(value * scale)

def process_html(content):
    """Verarbeitet HTML und skaliert alle relevanten Werte"""

    print("[+] Starte Map-Skalierung...")
    changes = []

    # 1. REGION_SIZE Konstante ändern (falls vorhanden)
    pattern = r'const\s+REGION_SIZE\s*=\s*(\d+)'
    if re.search(pattern, content):
        content = re.sub(pattern, f'const REGION_SIZE = {NEW_REGION_SIZE}', content)
        changes.append(f"✅ REGION_SIZE: {OLD_REGION_SIZE} → {NEW_REGION_SIZE}")

    # 2. WORLD_SIZE Konstante ändern
    pattern = r'const\s+WORLD_SIZE\s*=\s*(\d+)'
    if re.search(pattern, content):
        content = re.sub(pattern, f'const WORLD_SIZE = {NEW_WORLD_SIZE}', content)
        changes.append(f"✅ WORLD_SIZE: → {NEW_WORLD_SIZE}")

    # 3. PlaneGeometry Größen ändern (133 → 3200)
    pattern = r'new\s+THREE\.PlaneGeometry\s*\(\s*(\d+)\s*,\s*(\d+)'
    matches = re.finditer(pattern, content)
    for match in matches:
        old_w = int(match.group(1))
        old_h = int(match.group(2))
        if old_w == OLD_REGION_SIZE:
            new_w = NEW_REGION_SIZE
            new_h = NEW_REGION_SIZE
            content = content.replace(
                f'new THREE.PlaneGeometry({old_w}, {old_h}',
                f'new THREE.PlaneGeometry({new_w}, {new_h}',
                1
            )
            changes.append(f"✅ PlaneGeometry: {old_w}×{old_h} → {new_w}×{new_h}")

    # 4. Region-Positionen skalieren (x:-66, z:-66 → x:-1600, z:-1600)
    # Pattern: x: -66 oder x: 0 oder x: 66 (und z entsprechend)
    region_coords = [
        (-66, 66, -1600, 1600),   # Top-left
        (0, 66, 0, 1600),         # Top-center
        (66, 66, 1600, 1600),     # Top-right
        (-66, 0, -1600, 0),       # Middle-left
        (0, 0, 0, 0),             # Center (Götterfels)
        (66, 0, 1600, 0),         # Middle-right
        (-66, -66, -1600, -1600), # Bottom-left
        (0, -66, 0, -1600),       # Bottom-center
        (66, -66, 1600, -1600),   # Bottom-right
    ]

    for old_x, old_z, new_x, new_z in region_coords:
        # Suche nach Mustern wie: x: -66, z: 66
        pattern = rf'x:\s*{old_x},\s*z:\s*{old_z}'
        if re.search(pattern, content):
            content = re.sub(pattern, f'x: {new_x}, z: {new_z}', content)
            changes.append(f"✅ Region-Position: ({old_x},{old_z}) → ({new_x},{new_z})")

    # 5. MOVE_SPEED erhöhen (20 → 80)
    pattern = r'const\s+MOVE_SPEED\s*=\s*(\d+)'
    if re.search(pattern, content):
        content = re.sub(pattern, 'const MOVE_SPEED = 80', content)
        changes.append("✅ MOVE_SPEED: 20 → 80 (schneller für große Map)")

    # 6. Enemy-Spawn-Bereich (Math.random() * 100 - 50 → Math.random() * 3000 - 1500)
    # Pattern: Math.random() * 100 - 50
    pattern = r'Math\.random\(\)\s*\*\s*100\s*-\s*50'
    count = len(re.findall(pattern, content))
    if count > 0:
        content = re.sub(pattern, 'Math.random() * 3000 - 1500', content)
        changes.append(f"✅ Enemy-Spawn-Bereich: ±50 → ±1500 ({count} Stellen)")

    # 7. World Bounds anpassen
    bounds_patterns = [
        (r'minX:\s*-\d+', f'minX: -{NEW_WORLD_SIZE // 2}'),
        (r'maxX:\s*\d+', f'maxX: {NEW_WORLD_SIZE // 2}'),
        (r'minZ:\s*-\d+', f'minZ: -{NEW_WORLD_SIZE // 2}'),
        (r'maxZ:\s*\d+', f'maxZ: {NEW_WORLD_SIZE // 2}'),
    ]

    for pattern, replacement in bounds_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes.append(f"✅ World Bounds: {replacement}")

    # 8. Minimap-Scale anpassen (falls vorhanden)
    # Pattern: const minimapScale = 0.05 oder ähnlich
    pattern = r'const\s+minimapScale\s*=\s*[\d.]+'
    if re.search(pattern, content):
        new_scale = 0.02  # Kleinerer Scale für größere Map
        content = re.sub(pattern, f'const minimapScale = {new_scale}', content)
        changes.append(f"✅ Minimap-Scale: → {new_scale}")

    # 9. Title anpassen
    content = re.sub(
        r'<title>.*?</title>',
        '<title>Najika World - 9.6km x 9.6km Open World (Battle Royale Scale)</title>',
        content
    )
    changes.append("✅ Title aktualisiert")

    # 10. Kamera-Start-Position (falls zu nah)
    pattern = r'camera\.position\.set\s*\(\s*0\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
    match = re.search(pattern, content)
    if match:
        old_y = int(match.group(1))
        old_z = int(match.group(2))
        if old_y < 200:  # Zu nah
            new_y = 300
            new_z = 400
            content = re.sub(pattern, f'camera.position.set(0, {new_y}, {new_z})', content)
            changes.append(f"✅ Kamera-Position: y={old_y} → y={new_y} (bessere Übersicht)")

    print("\n[=] Aenderungen:")
    for change in changes:
        print(f"  {change}")

    return content, len(changes)

def main():
    """Hauptfunktion"""

    # UTF-8 für Windows Console
    import sys
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

    # Pfad zur HTML-Datei
    html_path = Path(__file__).parent / 'digivice' / 'najika_world_UNIFIED.html'

    if not html_path.exists():
        print(f"[X] Datei nicht gefunden: {html_path}")
        sys.exit(1)

    print(f"[>] Lade: {html_path}")

    # HTML laden
    with open(html_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    print(f"[~] Original-Groesse: {len(original_content):,} Bytes")

    # Backup erstellen
    backup_path = html_path.with_suffix('.html.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"[*] Backup erstellt: {backup_path}")

    # Verarbeiten
    processed_content, change_count = process_html(original_content)

    # Speichern
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)

    print(f"\n[OK] Erfolgreich gespeichert!")
    print(f"[~] Neue Groesse: {len(processed_content):,} Bytes")
    print(f"[+] {change_count} Aenderungen durchgefuehrt")

    print("\n[!] Naechste Schritte:")
    print("  1. Oeffne najika_world_UNIFIED.html im Browser")
    print("  2. Pruefe Console fuer 'REGION_SIZE' und 'WORLD_SIZE' Logs")
    print("  3. Teste WASD-Bewegung (sollte schneller sein)")
    print("  4. Pruefe ob Enemies spawnen (groesserer Bereich)")
    print("  5. Falls Probleme: Backup wiederherstellen aus .html.backup")

    print(f"\n[>>] Map-Groesse: {NEW_REGION_SIZE}m x {NEW_REGION_SIZE}m pro Region")
    print(f"[>>] Gesamt: {NEW_WORLD_SIZE}m x {NEW_WORLD_SIZE}m (9.6km x 9.6km)")
    print(f"[>>] Fortnite BR zum Vergleich: 5.5km x 5.5km -> Najika ist 1.75x groesser!")

if __name__ == '__main__':
    main()
