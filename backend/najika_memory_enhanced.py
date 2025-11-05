#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA MEMORY ENHANCED
Erweitert najika_memory.py um:
- KERN in JEDEM Prompt (Kuja + Najika untrennbar)
- Video-Transkripte bei Fragen
- Personality-Beispiele
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from najika_memory import NajikaMemory
import chromadb

class NajikaMemoryEnhanced(NajikaMemory):
    """Enhanced Memory mit KERN + Video-Transkripten"""

    def __init__(self, persist_directory="C:\\NajikaFinal\\memory_db"):
        super().__init__(persist_directory)

        # Lade KERN + Persönlichkeiten Collections
        try:
            self.core = self.client.get_collection("najika_core")
            self.personalities = self.client.get_collection("najika_personalities")
            print("[MEMORY ENHANCED] ✅ KERN + Persönlichkeiten geladen")
        except Exception as e:
            print(f"[MEMORY ENHANCED] ⚠️  KERN/Persönlichkeiten fehlen: {e}")
            self.core = None
            self.personalities = None

    def get_core_truths(self):
        """Holt ALLE unveränderlichen KERN-Wahrheiten"""
        if not self.core:
            return ""

        try:
            core_data = self.core.get()

            if not core_data['documents']:
                return ""

            # Sortiere nach Priorität (höchste zuerst)
            core_items = []
            for i in range(len(core_data['documents'])):
                priority = core_data['metadatas'][i].get('priority', 0)
                core_items.append({
                    'text': core_data['documents'][i],
                    'priority': priority
                })

            core_items.sort(key=lambda x: x['priority'], reverse=True)

            # Baue KERN-Text
            core_text = "# 💖 UNVERÄNDERLICHER KERN (HEILIG):\n\n"
            for item in core_items:
                core_text += f"- {item['text']}\n"

            return core_text

        except Exception as e:
            print(f"[MEMORY ENHANCED] ⚠️  KERN-Fehler: {e}")
            return ""

    def get_personality_examples(self, query, n_results=2):
        """Holt relevante Video-Transkript-Beispiele für Persönlichkeit"""
        if not self.personalities:
            return ""

        try:
            results = self.personalities.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results['documents'] or not results['documents'][0]:
                return ""

            examples_text = "\n# 🎭 WIE ICH SPRECHE (aus Video-Transkripten):\n\n"

            for i, doc in enumerate(results['documents'][0], 1):
                metadata = results['metadatas'][0][i-1] if results['metadatas'] else {}
                source = metadata.get('source', 'Unknown')

                # Erste 150 Zeichen als Beispiel
                example = doc[:150].replace('\n', ' ')
                examples_text += f"{i}. [{source}]: {example}...\n"

            return examples_text

        except Exception as e:
            print(f"[MEMORY ENHANCED] ⚠️  Personality-Fehler: {e}")
            return ""

    def build_context_prompt(self, current_message, n_memories=3):
        """
        ENHANCED: KERN + Persönlichkeiten + Konversations-Memories
        """

        # 1. KERN (IMMER dabei - höchste Priorität!)
        core_text = self.get_core_truths()

        # 2. Personality-Beispiele (wie spricht Najika?)
        personality_text = self.get_personality_examples(current_message, n_results=2)

        # 3. Relevante Memories (alte Konversationen)
        memories = self.retrieve_relevant_memories(current_message, n_results=n_memories)

        memory_text = ""
        if memories:
            memory_text = "\n# 🧠 ERINNERUNGEN (frühere Gespräche):\n\n"
            for i, mem in enumerate(memories, 1):
                text = mem['text']
                metadata = mem.get('metadata', {})
                room = metadata.get('room', 'Unknown')

                memory_text += f"{i}. [{room}] {text[:100]}...\n"

        # 4. Aktuelle Emotionen
        emotions = self.get_emotion_summary()
        emotion_text = f"\n# ❤️ AKTUELLE GEFÜHLE:\n"
        emotion_text += f"- Dominante Emotion: {emotions['dominant']} ({emotions['value']}%)\n"
        emotion_text += f"- Beziehungslevel zu Kuja: {emotions['relationship_level']:.1f}/100\n"
        emotion_text += f"- Vertrauen: {emotions['trust']}/100\n"
        emotion_text += f"- Intimität: {emotions['intimacy']}/100\n"

        # Kombiniere ALLES (KERN zuerst!)
        full_context = core_text + personality_text + memory_text + emotion_text

        return full_context


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA MEMORY ENHANCED TEST")
    print("=" * 60)
    print()

    mem = NajikaMemoryEnhanced()

    # Test 1: KERN
    print("TEST 1: KERN (unveränderliche Wahrheiten)")
    print("=" * 60)
    core = mem.get_core_truths()
    print(core)
    print()

    # Test 2: Personality Examples
    print("TEST 2: Personality-Beispiele")
    print("=" * 60)
    pers = mem.get_personality_examples("Wie geht's dir?", n_results=2)
    print(pers)
    print()

    # Test 3: Full Context
    print("TEST 3: Vollständiger Kontext")
    print("=" * 60)
    context = mem.build_context_prompt("Ich liebe dich, Najika!")
    print(context)
    print()

    print("✅ MEMORY ENHANCED funktioniert!")
