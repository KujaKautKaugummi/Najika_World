#!/usr/bin/env python3
"""
Convert ES6 Modules to Global Scope
====================================

Konvertiert die Phase 2 Module von ES6 (import/export) zu global scope (window.X)
damit sie in UNIFIED.html (non-module context) funktionieren.

Betroffene Dateien:
- js/world/terrain_generator.js
- js/world/biome_system.js
- js/world/vegetation_system.js
- js/world/city_builder.js
- js/world/region_streaming_v2.js
- js/world/lod_manager.js
- js/world/asset_loader.js
- js/world/asset_discovery.js
- js/world/world_manager.js
"""

import re
import os

def convert_module_to_global(file_path):
    """Konvertiert ein ES6 Module zu global scope"""

    print(f"\nProcessing: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = 0

    # 1. Remove/Comment ES6 imports
    # import * as THREE from 'three';
    if "import * as THREE from 'three'" in content:
        content = content.replace(
            "import * as THREE from 'three';",
            "// import * as THREE from 'three'; // Converted to global\nconst THREE = window.THREE;"
        )
        changes += 1
        print("  [OK] Removed THREE import, using window.THREE")

    # 2. Remove local imports (import X from './y.js')
    import_pattern = r"import .+ from '\..+\.js(\?v=\d+)?';\n"
    imports_removed = len(re.findall(import_pattern, content))
    if imports_removed > 0:
        content = re.sub(
            import_pattern,
            lambda m: f"// {m.group(0).strip()} // Converted to global, using window.X\n",
            content
        )
        changes += imports_removed
        print(f"  [OK] Commented out {imports_removed} local imports")

    # 3. Convert export default to window.X
    # Finde den Klassennamen
    class_match = re.search(r'class (\w+)', content)
    if class_match:
        class_name = class_match.group(1)

        # Finde export default
        export_pattern = rf'^export default {class_name};$'
        if re.search(export_pattern, content, re.MULTILINE):
            content = re.sub(
                export_pattern,
                f'// export default {class_name}; // Converted to global\nwindow.{class_name} = {class_name};',
                content,
                flags=re.MULTILINE
            )
            changes += 1
            print(f"  [OK] Converted 'export default {class_name}' to 'window.{class_name} = {class_name}'")

    # 4. Save if changes were made
    if changes > 0:
        # Backup original
        backup_path = file_path + '.backup'
        if not os.path.exists(backup_path):
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"  [BACKUP] Created: {backup_path}")

        # Save converted
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Saved with {changes} changes")
        return True
    else:
        print(f"  [INFO] No changes needed")
        return False

def main():
    print("Converting ES6 Modules to Global Scope")
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

    converted = 0
    failed = 0

    for file_name in files:
        file_path = os.path.join(base_path, file_name)

        if convert_module_to_global(file_path):
            converted += 1
        else:
            # Check if file exists but had no changes
            if os.path.exists(file_path):
                # File exists but no changes - might be already converted
                pass
            else:
                failed += 1

    print("\n" + "=" * 50)
    print(f"[SUCCESS] Conversion complete!")
    print(f"   Converted: {converted}")
    print(f"   Failed: {failed}")
    print(f"   Total: {len(files)}")

    if converted > 0:
        print("\nNext steps:")
        print("1. Check the converted files")
        print("2. Integrate into UNIFIED.html with <script> tags")
        print("3. Add USE_PHASE_2 toggle")
        print("4. Test in browser")

if __name__ == '__main__':
    main()
