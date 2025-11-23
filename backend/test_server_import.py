#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("SERVER IMPORT DEBUG")
print("=" * 60)

print("\n[1/10] TTS Import...")
from najika_tts_coqui import generate_speech as coqui_generate_speech
print("  ✓ TTS OK")

print("\n[2/10] LoRA Import...")
try:
    from najika_lora_training_3b import NajikaLoRATrainer3B
    print("  ✓ LoRA OK")
except ImportError:
    print("  ⚠ LoRA nicht verfügbar")

print("\n[3/10] Battle System...")
from najika_battle import BATTLE_SYSTEM, SKILL_DB, ITEM_DB
print("  ✓ Battle OK")

print("\n[4/10] Voice Call System...")
from najika_voice_call import VOICE_CALL_SYSTEM
print("  ✓ Voice Call OK")

print("\n[5/10] Claude Code...")
from najika_claude_code import call_ai_with_hierarchy, CLAUDE_CODE_INSTANCE
print("  ✓ Claude Code OK")

print("\n[6/10] Enhanced Personality...")
from najika_enhanced_personality import generate_enhanced_persona
print("  ✓ Personality Import OK")
persona = generate_enhanced_persona()
print(f"  ✓ Persona Generated ({len(persona)} chars)")

print("\n[7/10] Memory System...")
from najika_memory_enhanced import NajikaMemoryEnhanced
print("  ✓ Memory OK")

print("\n[8/10] Living System...")
from najika_living_system import LIVING_STATE
print("  ✓ Living System OK")

print("\n[9/10] Security...")
from najika_security import NajikaSecurity
print("  ✓ Security OK")

print("\n[10/10] Web Search...")
from najika_search import NajikaSearch
print("  ✓ Search OK")

print("\n" + "=" * 60)
print("ALL IMPORTS SUCCESSFUL!")
print("=" * 60)
