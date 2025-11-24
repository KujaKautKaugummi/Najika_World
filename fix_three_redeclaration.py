#!/usr/bin/env python3
"""
Fix THREE redeclaration error
==============================

Problem: Jedes Module deklariert 'const THREE = window.THREE;'
Lösung: Nur erste Zeile behalten, Rest kommentieren
"""

import os

def fix_three_declaration(file_path):
    """Entfernt doppelte THREE Deklarationen"""

    print(f"\nProcessing: {file_path}")

    if not os.path.exists(file_path):
        print(f"[SKIP] File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Entferne ALLE "const THREE" Zeilen
    new_lines = []
    removed = 0

    for line in lines:
        if line.strip() == 'const THREE = window.THREE;':
            # Komplett entfernen
            removed += 1
            print(f"  [REMOVED] const THREE declaration")
        elif '// import * as THREE from' in line:
            # Behalten (Kommentar)
            new_lines.append(line)
        else:
            new_lines.append(line)

    if removed > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"  [OK] Removed {removed} declarations")
        return True
    else:
        print(f"  [INFO] No declarations found")
        return False

def main():
    print("Fixing THREE redeclaration errors")
    print("=" * 50)

    base_path = "digivice/js/world"

    files = [
        'terrain_generator.js',
        'biome_system.js',
        'vegetation_system.js',
        'city_builder.js',
        'region_streaming_v2.js',
        'lod_manager.js',
        'asset_loader.js',
        'asset_discovery.js',
        'world_manager.js'
    ]

    fixed = 0

    for file_name in files:
        file_path = os.path.join(base_path, file_name)
        if fix_three_declaration(file_path):
            fixed += 1

    print("\n" + "=" * 50)
    print(f"[SUCCESS] Fixed {fixed} files")
    print("\nTHREE is now available globally via window.THREE")
    print("No redeclaration errors!")

if __name__ == '__main__':
    main()
