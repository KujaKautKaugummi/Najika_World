#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX: Voice Call Lazy Loading
Verhindert dass Whisper Model beim Server-Start geladen wird
"""

from pathlib import Path

FILE = Path(__file__).parent / "najika_voice_call.py"

content = FILE.read_text(encoding='utf-8')

# Check if already fixed
if "DEAKTIVIERT: Blockiert Server-Start" in content:
    print("✅ Voice Call bereits gefixt!")
else:
    # Replace the problematic line
    old_code = """        print("[VOICE CALL] Initialisiere Voice Call System...")
        self._load_whisper_model()"""

    new_code = """        print("[VOICE CALL] Initialisiere Voice Call System...")
        # Whisper Model wird LAZY geladen (erst beim ersten Call)
        # self._load_whisper_model()  # DEAKTIVIERT: Blockiert Server-Start!"""

    if old_code in content:
        content = content.replace(old_code, new_code)
        FILE.write_text(content, encoding='utf-8')
        print("✅ Voice Call gefixt! Whisper wird jetzt lazy geladen.")
    else:
        print("❌ Code-Pattern nicht gefunden! Manual fix nötig.")

# Füge lazy loading im start_call hinzu
if "def start_call(self):" in content and "# Lazy load Whisper" not in content:
    old_start_call = """    def start_call(self):
        \"\"\"Startet Voice Call Session\"\"\"
        self.is_call_active = True"""

    new_start_call = """    def start_call(self):
        \"\"\"Startet Voice Call Session\"\"\"
        # Lazy load Whisper Model beim ersten Call
        if self.whisper_model is None:
            self._load_whisper_model()

        self.is_call_active = True"""

    content = FILE.read_text(encoding='utf-8')
    if old_start_call in content:
        content = content.replace(old_start_call, new_start_call)
        FILE.write_text(content, encoding='utf-8')
        print("✅ Lazy loading in start_call() hinzugefügt!")

print("\n[DONE] Voice Call System optimiert!")
