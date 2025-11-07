#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script zum Automatischen Ersetzen von hardcoded Pfaden in allen Python-Dateien
"""

import sys
import io
from pathlib import Path
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Backend Verzeichnis
BACKEND_DIR = Path(__file__).parent

# Patterns zum Ersetzen
PATTERNS = [
    # Pattern 1: NAJIKA_DIR = Path('C:/Najika-World')
    {
        'old': r"NAJIKA_DIR = Path\('C:/Najika-World'\)",
        'new': "# Project Root Directory (dynamisch für alle Systeme)\nNAJIKA_DIR = Path(__file__).resolve().parent.parent"
    },
    # Pattern 2: NAJIKA_DIR = Path("C:/Najika-World/...")
    {
        'old': r"NAJIKA_DIR = Path\(\"C:/Najika-World/backend/training_data_real\"\)",
        'new': "# Project Root Directory (dynamisch für alle Systeme)\nNAJIKA_DIR = Path(__file__).resolve().parent / 'training_data_real'"
    },
    # Pattern 3: OUTPUT_DIR = Path('C:/Najika-World/voice_data/...')
    {
        'old': r"OUTPUT_DIR = Path\('C:/Najika-World/voice_data/samples_megumin'\)",
        'new': "# Project Root Directory (dynamisch für alle Systeme)\nOUTPUT_DIR = Path(__file__).resolve().parent.parent / 'voice_data' / 'samples_megumin'"
    },
]

def fix_file(file_path):
    """Fixe hardcoded Pfade in einer Datei"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Wende alle Patterns an
        for pattern in PATTERNS:
            content = re.sub(pattern['old'], pattern['new'], content)

        # Nur schreiben wenn geändert
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path.name}")
            return True
        return False

    except Exception as e:
        print(f"❌ Error in {file_path.name}: {e}")
        return False

def main():
    print("🔧 Fixe hardcoded Pfade in Backend-Dateien...")
    print()

    fixed_count = 0

    # Alle .py Dateien im Backend
    for py_file in BACKEND_DIR.glob('*.py'):
        if py_file.name == 'fix_hardcoded_paths.py':
            continue  # Skip this script itself

        if fix_file(py_file):
            fixed_count += 1

    print()
    print(f"✅ {fixed_count} Dateien gefixt!")

if __name__ == '__main__':
    main()
