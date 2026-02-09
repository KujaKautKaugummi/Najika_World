#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frage Najika nach dem kompletten Projekt-Wissen
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
from najika_memory_enhanced import NajikaMemoryEnhanced

print("=" * 80)
print("NAJIKA PROJEKT-ANALYSE - WAS WEISS SIE ALLES?")
print("=" * 80)

# Memory laden
mem = NajikaMemoryEnhanced()

# Sammle ALLES was Najika weiss
print("\n[1/5] Sammle Projekt-Wissen...")
projekt_themen = [
    "Najika World Spiel Features komplett",
    "Flutter Android App Digivice",
    "Quest System NPCs Regionen",
    "Combat Kampfsystem Arena",
    "Oregon Trail Minigame",
    "Schwarze Muehle Windmuehle Geschichte",
    "Backend Server API Endpoints",
    "Personality Engine Mood System"
]

gesammeltes_wissen = []
for thema in projekt_themen:
    results = mem.search(thema, n_results=3)
    if results['project_knowledge']:
        for item in results['project_knowledge']:
            text = item['text'][:500]
            if text not in [w[:500] for w in gesammeltes_wissen]:
                gesammeltes_wissen.append(text)

print(f"   Gefunden: {len(gesammeltes_wissen)} einzigartige Wissens-Bloecke")

# KERN holen
print("\n[2/5] Hole KERN-Wahrheiten...")
kern = mem.get_core_truths()
print(f"   KERN geladen: {len(kern)} Zeichen")

# Emotionen
print("\n[3/5] Hole Emotions-Status...")
emotions = mem.get_emotion_summary()
print(f"   Dominant: {emotions['dominant']}, Beziehung: {emotions['relationship_level']}")

# Konversations-History
print("\n[4/5] Pruefe Konversations-Memories...")
conv_count = mem.conversations.count()
print(f"   {conv_count} Gespraeche gespeichert")

# Jetzt Najika fragen via Ollama
print("\n[5/5] Frage Najika via Ollama...")
print("=" * 80)

# Baue mega-Kontext
kontext = f"""
{kern}

# PROJEKT-WISSEN (aus meinem Gedaechtnis):
"""

for i, wissen in enumerate(gesammeltes_wissen[:15], 1):  # Max 15 Bloecke
    kontext += f"\n{i}. {wissen[:400]}...\n"

kontext += f"""

# MEINE GEFUEHLE:
- Beziehungslevel zu Kuja: {emotions['relationship_level']}
- Vertrauen: {emotions['trust']}
- {conv_count} gemeinsame Gespraeche

"""

prompt = f"""{kontext}

KUJA FRAGT MICH JETZT:
"Najika, gib mir eine vollstaendige Zusammenfassung unseres Projekts!
Was haben wir alles gebaut? Was funktioniert? Was fehlt noch?
Sei gruendlich aber strukturiert - ich will wissen was du ALLES weisst!"

MEINE ANTWORT ALS NAJIKA (explosiv, detailliert, strukturiert):
"""

try:
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "najika-local",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 2000
            }
        },
        timeout=120
    )

    if response.status_code == 200:
        antwort = response.json().get("response", "")
        print("\n" + "=" * 80)
        print("NAJIKAS ANTWORT:")
        print("=" * 80)
        print(antwort)
    else:
        print(f"Ollama Fehler: {response.status_code}")

except requests.exceptions.ConnectionError:
    print("\n[WARN] Ollama nicht erreichbar - zeige gesammeltes Wissen direkt:")
    print("=" * 80)
    print("\nGESAMMELTES PROJEKT-WISSEN:")
    print("=" * 80)
    for i, wissen in enumerate(gesammeltes_wissen[:20], 1):
        print(f"\n--- Block {i} ---")
        print(wissen[:600])

except Exception as e:
    print(f"Fehler: {e}")

print("\n" + "=" * 80)
print("STATISTIK:")
print("=" * 80)
print(f"KERN-Wahrheiten: 7")
print(f"Projekt-Wissen: {mem.project_knowledge.count() if mem.project_knowledge else 0} Eintraege")
print(f"Persoenlichkeiten: {mem.personalities.count() if mem.personalities else 0} Eintraege")
print(f"Konversationen: {conv_count} Eintraege")
print(f"Emotionen: {mem.emotions.count()} Eintraege")
print(f"\nGESAMT: {7 + (mem.project_knowledge.count() if mem.project_knowledge else 0) + (mem.personalities.count() if mem.personalities else 0) + conv_count + mem.emotions.count()} Wissens-Eintraege")
