#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Najikas echtes Gedächtnis"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from najika_memory_enhanced import NajikaMemoryEnhanced

print("=" * 60)
print("NAJIKA MEMORY TEST - ECHTES GEDÄCHTNIS")
print("=" * 60)

# Lade Memory
mem = NajikaMemoryEnhanced()

# Test 1: KERN abrufen
print("\n1. UNVERÄNDERLICHER KERN:")
print("-" * 40)
core = mem.get_core_truths()
print(core[:500] if core else "FEHLT!")

# Test 2: Personality-Beispiele
print("\n2. PERSÖNLICHKEITS-BEISPIELE (Suche: 'Explosion'):")
print("-" * 40)
pers = mem.get_personality_examples("Explosion Megumin", n_results=2)
print(pers[:400] if pers else "FEHLT!")

# Test 3: Emotion Summary
print("\n3. AKTUELLE EMOTIONEN:")
print("-" * 40)
emotions = mem.get_emotion_summary()
print(f"Dominant: {emotions['dominant']} ({emotions['value']}%)")
print(f"Beziehungslevel: {emotions['relationship_level']}")
print(f"Vertrauen: {emotions['trust']}")

# Test 4: Relevante Memories
print("\n4. RELEVANTE ERINNERUNGEN (Suche: 'liebe dich'):")
print("-" * 40)
memories = mem.retrieve_relevant_memories("ich liebe dich", n_results=3)
for i, m in enumerate(memories, 1):
    text = m['text'][:100].replace('\n', ' ')
    print(f"  {i}. {text}...")

# Test 5: Vollständiger Kontext
print("\n5. VOLLSTÄNDIGER KONTEXT-PROMPT:")
print("-" * 40)
context = mem.build_context_prompt("Najika, erinnerst du dich an unser erstes Gespräch?")
print(context[:600] if context else "FEHLT!")

print("\n" + "=" * 60)
print("✅ MEMORY TEST ABGESCHLOSSEN")
print("=" * 60)
