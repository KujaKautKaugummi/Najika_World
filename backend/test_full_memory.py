#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Najikas KOMPLETTES Gedächtnis inkl. Projekt-Wissen"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from najika_memory_enhanced import NajikaMemoryEnhanced

print("=" * 70)
print("NAJIKA VOLLSTAENDIGES GEDAECHTNIS TEST")
print("=" * 70)

# Lade Memory
mem = NajikaMemoryEnhanced()

# Test 1: Projekt-Wissen abrufen
print("\n1. PROJEKT-WISSEN (Suche: 'Flutter Android Digivice'):")
print("-" * 50)
pk = mem.get_project_knowledge("Flutter Android Digivice App", n_results=3)
print(pk[:800] if pk else "NICHT GEFUNDEN!")

# Test 2: Universelle Suche
print("\n2. UNIVERSELLE SUCHE (Suche: 'Schwarze Muehle'):")
print("-" * 50)
results = mem.search("Schwarze Muehle Windmuehle", n_results=3)
print(f"Konversationen: {len(results['conversations'])} Treffer")
print(f"Projekt-Wissen: {len(results['project_knowledge'])} Treffer")
print(f"Persoenlichkeiten: {len(results['personalities'])} Treffer")

if results['project_knowledge']:
    print("\nErster Projekt-Treffer:")
    print(results['project_knowledge'][0]['text'][:300] + "...")

# Test 3: Vollstaendiger Kontext mit Projekt-Wissen
print("\n3. VOLLSTAENDIGER KONTEXT (technische Frage):")
print("-" * 50)
context = mem.build_context_prompt("Wie funktioniert das Quest-System im Spiel?")
print(context[:1500] if context else "FEHLT!")

# Test 4: Alle Collections zaehlen
print("\n4. SPEICHER-STATISTIK:")
print("-" * 50)
print(f"Konversationen: {mem.conversations.count()} Eintraege")
print(f"Emotionen: {mem.emotions.count()} Eintraege")
if mem.core:
    print(f"KERN: {mem.core.count()} Eintraege")
if mem.personalities:
    print(f"Persoenlichkeiten: {mem.personalities.count()} Eintraege")
if mem.project_knowledge:
    print(f"Projekt-Wissen: {mem.project_knowledge.count()} Eintraege")

print("\n" + "=" * 70)
print("NAJIKA WEISS JETZT ALLES!")
print("=" * 70)
