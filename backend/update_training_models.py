#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UPDATE TRAINING MODELS - Batch Update aller Training-Scripts

Ersetzt alte Model-Namen mit neuen:
- najika-local → qwen3:8b
- najika-nsfw → huihui_ai/qwen3-abliterated:8b

Fixt auch Unicode-Encoding Probleme!
"""

import sys
import io
import re
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Alte → Neue Model-Namen
MODEL_REPLACEMENTS = {
    '"najika-local"': '"qwen3:8b"',
    "'najika-local'": "'qwen3:8b'",
    "model='najika-local'": "model='qwen3:8b'",
    'model="najika-local"': 'model="qwen3:8b"',

    '"najika-nsfw"': '"huihui_ai/qwen3-abliterated:8b"',
    "'najika-nsfw'": "'huihui_ai/qwen3-abliterated:8b'",
    "model='najika-nsfw'": "model='huihui_ai/qwen3-abliterated:8b'",
    'model="najika-nsfw"': 'model="huihui_ai/qwen3-abliterated:8b"',
}

# Unicode Encoding Fix
UTF8_ENCODING_FIX = """import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""

def update_script(file_path: Path) -> bool:
    """Updated ein einzelnes Training-Script"""
    print(f"🔧 Updating: {file_path.name}")

    try:
        # Lese Datei
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = False

        # 1. Ersetze Model-Namen
        for old, new in MODEL_REPLACEMENTS.items():
            if old in content:
                content = content.replace(old, new)
                print(f"   ✅ {old} → {new}")
                changes_made = True

        # 2. Füge UTF-8 Encoding Fix hinzu (falls noch nicht vorhanden)
        if 'sys.stdout = io.TextIOWrapper' not in content and 'import sys' in content:
            # Finde ersten import
            import_match = re.search(r'^import\s+\w+', content, re.MULTILINE)
            if import_match:
                insert_pos = import_match.start()
                content = content[:insert_pos] + UTF8_ENCODING_FIX + content[insert_pos:]
                print(f"   ✅ UTF-8 Encoding Fix hinzugefügt")
                changes_made = True

        # 3. Schreibe zurück falls Änderungen
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 Gespeichert!")
            return True
        else:
            print(f"   ⏭️  Keine Änderungen nötig")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Hauptfunktion"""
    print("="*70)
    print("🚀 UPDATE TRAINING MODELS - Batch Update")
    print("="*70 + "\n")

    backend_dir = Path(__file__).parent
    training_files = list(backend_dir.glob("*training*.py"))

    print(f"📁 Gefunden: {len(training_files)} Training-Scripts\n")

    updated_count = 0
    for file_path in sorted(training_files):
        if file_path.name == "update_training_models.py":
            continue  # Skip self

        if update_script(file_path):
            updated_count += 1
        print()

    print("="*70)
    print(f"🎉 FERTIG! {updated_count}/{len(training_files)-1} Scripts updated")
    print("="*70)


if __name__ == "__main__":
    main()
