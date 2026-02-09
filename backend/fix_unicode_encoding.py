#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UNICODE ENCODING FIX
Fixt die 4 Training-Scripts die UnicodeEncodeError auf Windows haben
"""

from pathlib import Path

BACKEND_DIR = Path(__file__).parent

FILES_TO_FIX = [
    "najika_advisor_training.py",
    "najika_thought_organizer_training.py",
    "najika_fact_checker_training.py",
    "najika_emotional_intelligence_training.py"
]

FIX_CODE = """import sys

# Fix Windows CP1252 encoding issue
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
"""

def fix_file(file_path):
    """Fügt UTF-8 encoding fix zu einem File hinzu"""
    content = file_path.read_text(encoding='utf-8')

    # Check if already fixed
    if 'sys.stdout.reconfigure' in content:
        print(f"✅ {file_path.name} - bereits gefixt!")
        return False

    # Find import block
    lines = content.split('\n')

    # Find last import line
    import_end = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_end = i

    # Check if 'import sys' exists
    has_sys_import = any('import sys' in line for line in lines[:import_end+1])

    if not has_sys_import:
        # Add 'import sys' after other imports
        lines.insert(import_end + 1, 'import sys')
        import_end += 1

    # Add encoding fix after imports
    lines.insert(import_end + 1, '')
    lines.insert(import_end + 2, '# Fix Windows CP1252 encoding issue')
    lines.insert(import_end + 3, "if sys.platform == 'win32':")
    lines.insert(import_end + 4, "    sys.stdout.reconfigure(encoding='utf-8')")

    # Write back
    file_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✅ {file_path.name} - GEFIXT!")
    return True

def main():
    # Fix encoding for this script too!
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("="*60)
    print("UNICODE ENCODING FIX - Windows CP1252 -> UTF-8")
    print("="*60)

    fixed_count = 0
    for filename in FILES_TO_FIX:
        file_path = BACKEND_DIR / filename
        if file_path.exists():
            if fix_file(file_path):
                fixed_count += 1
        else:
            print(f"❌ {filename} - NICHT GEFUNDEN!")

    print("\n" + "="*60)
    print(f"FERTIG! {fixed_count} Files gefixt.")
    print("="*60)

if __name__ == "__main__":
    main()
