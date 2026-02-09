#!/usr/bin/env python3
"""Test which import is hanging"""
import sys
sys.stdout = sys.stdout  # Unbuffered

print("1. Testing basic imports...")
import os, json, random, hashlib, time, threading
print("   -> Basic imports OK")

print("2. Testing Living System...")
from najika_living_system import LIVING_STATE
print("   -> Living System OK")

print("3. Testing Enhanced Personality...")
from najika_enhanced_personality import generate_enhanced_persona
print("   -> Enhanced Personality OK")

print("4. Testing Memory Enhanced...")
from najika_memory_enhanced import NajikaMemoryEnhanced
print("   -> Memory Enhanced OK")

print("5. Testing Search...")
from najika_search import NajikaSearch
print("   -> Search OK")

print("6. Testing Tor...")
from najika_tor import NajikaTor
print("   -> Tor OK")

print("7. Testing Security...")
from najika_security import NajikaSecurity
print("   -> Security OK")

print("8. Testing TTS...")
try:
    from najika_tts_coqui import generate_speech as coqui_generate_speech
    print("   -> Coqui TTS OK")
except:
    print("   -> Coqui TTS skipped")

print("9. Testing Battle...")
from najika_battle import BATTLE_SYSTEM, SKILL_DB, ITEM_DB
print("   -> Battle OK")

print("10. Testing Skill System...")
from najika_skill_system import SkillSystem, Element, SKILL_DATABASE
print("   -> Skill System OK")

print("11. Testing Temperature...")
from najika_temperature_system import TemperatureSystem, REGIONS as TEMP_REGIONS
print("   -> Temperature OK")

print("12. Testing Minigames...")
try:
    from najika_minigames_api import api_get_all_cards
    print("   -> Minigames OK")
except:
    print("   -> Minigames skipped")

print("13. Testing Slime Arena...")
try:
    from najika_slime_arena_api import api_start_duel
    print("   -> Slime Arena OK")
except:
    print("   -> Slime Arena skipped")

print("14. Testing Claude Code...")
from najika_claude_code import call_ai_with_hierarchy, CLAUDE_CODE_INSTANCE
print("   -> Claude Code OK")

print("15. Testing Nemesis Arena...")
try:
    from najika_nemesis_arena_system import ARENA_MANAGER
    print("   -> Nemesis Arena OK")
except:
    print("   -> Nemesis Arena skipped")

print("16. Testing Finisher...")
try:
    from najika_finisher_system import FINISHER_GENERATOR
    print("   -> Finisher OK")
except:
    print("   -> Finisher skipped")

print("\n✅ ALL IMPORTS COMPLETED!")
