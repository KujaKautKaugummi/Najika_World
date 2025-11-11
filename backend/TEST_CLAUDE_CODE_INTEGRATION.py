#!/usr/bin/env python3
"""
TEST: Claude Code Integration
Prüft ob Najika nahtlos Claude Code nutzen kann
"""

import sys
sys.path.insert(0, 'C:/Najika_World/backend')

from najika_claude_code import call_ai_with_hierarchy, CLAUDE_CODE_INSTANCE

print("="*80)
print("NAJIKA CLAUDE CODE INTEGRATION TEST")
print("="*80)
print()

# 1. Check ob Claude Code verfügbar
print("[1] Claude Code Verfügbarkeit:")
print(f"   Available: {CLAUDE_CODE_INSTANCE.available}")
print()

# 2. Test-Prompt (einfach)
print("[2] Test: Einfache Frage")
print("   Prompt: 'Was ist 2+2?'")
print()

response, provider = call_ai_with_hierarchy(
    prompt="Was ist 2+2? Antworte als Najika (Megumin-Style)!",
    context=None,
    ollama_callback=lambda p, w: "Fallback: 4"
)

print(f"   Provider: {provider}")
print(f"   Response: {response[:200]}...")
print()

# 3. Test-Prompt (Code)
print("[3] Test: Code-Frage")
print("   Prompt: 'Schreibe Python Hello World'")
print()

response2, provider2 = call_ai_with_hierarchy(
    prompt="Schreibe mir Python Code für Hello World. Kurz und knapp!",
    context=None,
    ollama_callback=lambda p, w: "Fallback: print('Hello')"
)

print(f"   Provider: {provider2}")
print(f"   Response: {response2[:200]}...")
print()

# 4. Statistiken
print("[4] Statistiken:")
stats = CLAUDE_CODE_INSTANCE.get_stats()
for key, value in stats.items():
    print(f"   {key}: {value}")
print()

print("="*80)
print("TEST ABGESCHLOSSEN!")
print("="*80)
