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

    def __init__(self, persist_directory="C:\\Najika_World\\memory_db"):
        super().__init__(persist_directory)

        # Lade KERN + Persönlichkeiten Collections
        try:
            self.core = self.client.get_collection("najika_core")
            self.personalities = self.client.get_collection("najika_personalities")
            print("[MEMORY ENHANCED] KERN + Persoenlichkeiten geladen")
        except Exception as e:
            print(f"[MEMORY ENHANCED] KERN/Persoenlichkeiten fehlen: {e}")
            self.core = None
            self.personalities = None

        # Lade Projekt-Wissen Collection (264 Dateien!)
        try:
            self.project_knowledge = self.client.get_collection("najika_project_knowledge")
            count = self.project_knowledge.count()
            print(f"[MEMORY ENHANCED] Projekt-Wissen geladen: {count} Eintraege")
        except Exception as e:
            print(f"[MEMORY ENHANCED] Projekt-Wissen fehlt: {e}")
            self.project_knowledge = None

        # Lade MD-Knowledge Collection (KB Parts 1-10, V8, etc.)
        try:
            self.md_knowledge = self.client.get_collection("najika_md_knowledge")
            count = self.md_knowledge.count()
            print(f"[MEMORY ENHANCED] MD-Knowledge geladen: {count} Eintraege")
        except Exception as e:
            print(f"[MEMORY ENHANCED] MD-Knowledge fehlt: {e}")
            self.md_knowledge = None

        # NEU: Lade Complete Knowledge Collection (14.000+ Eintraege!)
        try:
            self.complete_knowledge = self.client.get_collection("najika_complete_knowledge")
            count = self.complete_knowledge.count()
            print(f"[MEMORY ENHANCED] Complete-Knowledge geladen: {count} Eintraege")
        except Exception as e:
            print(f"[MEMORY ENHANCED] Complete-Knowledge fehlt: {e}")
            self.complete_knowledge = None

        # NEU: Lade Wichtige Docs Collection (5.700+ Eintraege!)
        try:
            self.wichtige_docs = self.client.get_collection("najika_wichtige_docs")
            count = self.wichtige_docs.count()
            print(f"[MEMORY ENHANCED] Wichtige-Docs geladen: {count} Eintraege")
        except Exception as e:
            print(f"[MEMORY ENHANCED] Wichtige-Docs fehlt: {e}")
            self.wichtige_docs = None

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

    def get_project_knowledge(self, query, n_results=3):
        """Holt relevantes Projekt-Wissen (Code, Ideen, Konzepte)"""
        if not self.project_knowledge:
            return ""

        try:
            results = self.project_knowledge.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results['documents'] or not results['documents'][0]:
                return ""

            knowledge_text = "\n# 📚 MEIN PROJEKT-WISSEN:\n\n"

            for i, doc in enumerate(results['documents'][0], 1):
                metadata = results['metadatas'][0][i-1] if results['metadatas'] else {}
                category = metadata.get('category', 'Unknown')
                title = metadata.get('title', 'Unbenannt')

                # Max 300 Zeichen pro Eintrag
                snippet = doc[:300].replace('\n', ' ')
                knowledge_text += f"{i}. [{category}] {title}: {snippet}...\n\n"

            return knowledge_text

        except Exception as e:
            print(f"[MEMORY ENHANCED] ⚠️  Projekt-Wissen-Fehler: {e}")
            return ""

    def get_md_knowledge(self, query, n_results=3):
        """Holt relevantes MD-Wissen (KB Parts, V8 Zusammenfassung, etc.)"""
        if not self.md_knowledge:
            return ""

        try:
            results = self.md_knowledge.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results['documents'] or not results['documents'][0]:
                return ""

            knowledge_text = "\n# 📖 DOKUMENTATIONS-WISSEN:\n\n"

            for i, doc in enumerate(results['documents'][0], 1):
                metadata = results['metadatas'][0][i-1] if results['metadatas'] else {}
                source = metadata.get('source_file', 'Unknown')

                # Max 400 Zeichen pro Eintrag
                snippet = doc[:400].replace('\n', ' ')
                knowledge_text += f"{i}. [{source}]: {snippet}...\n\n"

            return knowledge_text

        except Exception as e:
            print(f"[MEMORY ENHANCED] ⚠️  MD-Knowledge-Fehler: {e}")
            return ""

    def get_complete_knowledge(self, query, n_results=5):
        """Holt relevantes Wissen aus der Complete Knowledge Collection (14.000+ Eintraege)"""
        if not self.complete_knowledge:
            return ""

        try:
            results = self.complete_knowledge.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results['documents'] or not results['documents'][0]:
                return ""

            knowledge_text = "\n# COMPLETE KNOWLEDGE (30.000+ Eintraege):\n\n"

            for i, doc in enumerate(results['documents'][0], 1):
                metadata = results['metadatas'][0][i-1] if results['metadatas'] else {}
                source = metadata.get('source', metadata.get('filename', 'Unknown'))
                kategorie = metadata.get('kategorie', 'Allgemein')

                # Max 500 Zeichen pro Eintrag
                snippet = doc[:500].replace('\n', ' ')
                knowledge_text += f"{i}. [{kategorie}] {source}:\n   {snippet}...\n\n"

            return knowledge_text

        except Exception as e:
            print(f"[MEMORY ENHANCED] Complete-Knowledge-Fehler: {e}")
            return ""

    def get_wichtige_docs(self, query, n_results=3):
        """Holt relevantes Wissen aus der Wichtige Docs Collection"""
        if not self.wichtige_docs:
            return ""

        try:
            results = self.wichtige_docs.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results['documents'] or not results['documents'][0]:
                return ""

            knowledge_text = "\n# WICHTIGE DOKUMENTATION:\n\n"

            for i, doc in enumerate(results['documents'][0], 1):
                metadata = results['metadatas'][0][i-1] if results['metadatas'] else {}
                source = metadata.get('pfad', metadata.get('source', 'Unknown'))

                # Max 400 Zeichen pro Eintrag
                snippet = doc[:400].replace('\n', ' ')
                knowledge_text += f"{i}. [{source}]: {snippet}...\n\n"

            return knowledge_text

        except Exception as e:
            print(f"[MEMORY ENHANCED] Wichtige-Docs-Fehler: {e}")
            return ""

    def search(self, query, n_results=5):
        """Universelle Suche ueber ALLE Collections"""
        results = {
            "core": [],
            "conversations": [],
            "project_knowledge": [],
            "md_knowledge": [],
            "personalities": [],
            "complete_knowledge": [],
            "wichtige_docs": []
        }

        # Konversationen durchsuchen
        try:
            conv_results = self.retrieve_relevant_memories(query, n_results=n_results)
            results["conversations"] = conv_results
        except:
            pass

        # Projekt-Wissen durchsuchen
        if self.project_knowledge:
            try:
                pk_results = self.project_knowledge.query(
                    query_texts=[query],
                    n_results=n_results
                )
                if pk_results['documents'] and pk_results['documents'][0]:
                    for i, doc in enumerate(pk_results['documents'][0]):
                        meta = pk_results['metadatas'][0][i] if pk_results['metadatas'] else {}
                        results["project_knowledge"].append({
                            "text": doc,
                            "metadata": meta
                        })
            except:
                pass

        # Persönlichkeiten durchsuchen
        if self.personalities:
            try:
                pers_results = self.personalities.query(
                    query_texts=[query],
                    n_results=min(n_results, 3)
                )
                if pers_results['documents'] and pers_results['documents'][0]:
                    for i, doc in enumerate(pers_results['documents'][0]):
                        meta = pers_results['metadatas'][0][i] if pers_results['metadatas'] else {}
                        results["personalities"].append({
                            "text": doc,
                            "metadata": meta
                        })
            except:
                pass

        # MD-Knowledge durchsuchen
        if self.md_knowledge:
            try:
                md_results = self.md_knowledge.query(
                    query_texts=[query],
                    n_results=n_results
                )
                if md_results['documents'] and md_results['documents'][0]:
                    for i, doc in enumerate(md_results['documents'][0]):
                        meta = md_results['metadatas'][0][i] if md_results['metadatas'] else {}
                        results["md_knowledge"].append({
                            "text": doc,
                            "metadata": meta
                        })
            except:
                pass

        # Complete Knowledge durchsuchen (14.000+ Eintraege!)
        if self.complete_knowledge:
            try:
                ck_results = self.complete_knowledge.query(
                    query_texts=[query],
                    n_results=n_results
                )
                if ck_results['documents'] and ck_results['documents'][0]:
                    for i, doc in enumerate(ck_results['documents'][0]):
                        meta = ck_results['metadatas'][0][i] if ck_results['metadatas'] else {}
                        results["complete_knowledge"].append({
                            "text": doc,
                            "metadata": meta
                        })
            except:
                pass

        # Wichtige Docs durchsuchen
        if self.wichtige_docs:
            try:
                wd_results = self.wichtige_docs.query(
                    query_texts=[query],
                    n_results=n_results
                )
                if wd_results['documents'] and wd_results['documents'][0]:
                    for i, doc in enumerate(wd_results['documents'][0]):
                        meta = wd_results['metadatas'][0][i] if wd_results['metadatas'] else {}
                        results["wichtige_docs"].append({
                            "text": doc,
                            "metadata": meta
                        })
            except:
                pass

        return results

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

        # 4. Projekt-Wissen (bei technischen Fragen)
        project_text = ""
        md_text = ""
        complete_text = ""
        wichtig_text = ""
        tech_keywords = ['code', 'funktion', 'feature', 'bug', 'api', 'server', 'game', 'spiel',
                        'digivice', 'flutter', 'android', 'quest', 'npc', 'item', 'skill',
                        'schwarze', 'muehle', 'windmuehle', 'oregon', 'kampf', 'combat',
                        'projekt', 'gebote', 'persoenlichkeit', 'facette', 'explosion',
                        'pvp', 'slime', 'region', 'roadmap', 'status', 'was', 'wie', 'wer',
                        'system', 'training', 'lora', 'modell', 'claude', 'ollama']
        if any(kw in current_message.lower() for kw in tech_keywords):
            project_text = self.get_project_knowledge(current_message, n_results=2)
            md_text = self.get_md_knowledge(current_message, n_results=2)
            # NEU: Complete Knowledge (14.000+ Eintraege!)
            complete_text = self.get_complete_knowledge(current_message, n_results=3)
            wichtig_text = self.get_wichtige_docs(current_message, n_results=2)

        # 5. Aktuelle Emotionen
        emotions = self.get_emotion_summary()
        emotion_text = f"\n# ❤️ AKTUELLE GEFÜHLE:\n"
        emotion_text += f"- Dominante Emotion: {emotions['dominant']} ({emotions['value']}%)\n"
        emotion_text += f"- Beziehungslevel zu Kuja: {emotions['relationship_level']:.1f}/100\n"
        emotion_text += f"- Vertrauen: {emotions['trust']}/100\n"
        emotion_text += f"- Intimität: {emotions['intimacy']}/100\n"

        # Kombiniere ALLES (KERN zuerst!)
        full_context = core_text + personality_text + complete_text + wichtig_text + project_text + md_text + memory_text + emotion_text

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
