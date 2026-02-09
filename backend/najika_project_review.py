#!/usr/bin/env python3
"""
NAJIKA PROJEKT REVIEW
Zeigt Najika alle Projektbereiche und fragt was fehlt
"""

import sys
import os
import json

# UTF-8 fuer Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import chromadb
from datetime import datetime

MEMORY_DB = "C:/Najika_World/memory_db"
PROJECT_ROOT = "C:/Najika_World"


class NajikaProjectReview:
    def __init__(self):
        print("=" * 70)
        print("  NAJIKA PROJEKT REVIEW")
        print("  Zeige alle Bereiche und frage nach Fehlenden")
        print("=" * 70)
        print()

        self.client = chromadb.PersistentClient(path=MEMORY_DB)
        self.complete = self.client.get_collection('najika_complete_knowledge')
        self.wichtig = self.client.get_collection('najika_wichtige_docs')

    def search(self, query, n=5):
        """Sucht in allen Collections"""
        results = []

        for col in [self.complete, self.wichtig]:
            try:
                res = col.query(
                    query_texts=[query],
                    n_results=n,
                    include=['documents', 'metadatas']
                )
                if res and res['documents'][0]:
                    for i, doc in enumerate(res['documents'][0]):
                        meta = res['metadatas'][0][i] if res['metadatas'] else {}
                        results.append({
                            'content': doc[:800],
                            'source': meta.get('source', meta.get('pfad', 'unknown')),
                            'kategorie': meta.get('kategorie', 'Allgemein')
                        })
            except:
                pass

        return results

    def get_project_areas(self):
        """Definiert alle Projektbereiche"""
        return {
            "1. KI-COMPANION SYSTEM": {
                "queries": ["Najika Persoenlichkeit Megumin Harley Shiro Melissa"],
                "expected": ["4 Persoenlichkeiten", "Facetten", "Voice-System", "Mood-System"]
            },
            "2. DIE 8 GEBOTE": {
                "queries": ["8 Gebote Zero-Trust Owner-Token Explosion PvE PvP"],
                "expected": ["Zero-Trust", "Owner-Token", "Explosion!=Weave", "Offline-First"]
            },
            "3. GAME WORLD": {
                "queries": ["9.6km Open World 8 Regionen Goetterfels"],
                "expected": ["8 Regionen", "9.6km x 9.6km", "Goetterfels Zentrum"]
            },
            "4. COMBAT SYSTEM": {
                "queries": ["Combat Skyrim Soulframe Digimon Dual-Wielding"],
                "expected": ["Dual-Wielding", "Learning by Doing", "Skill-by-Use"]
            },
            "5. SLIME COMPANION": {
                "queries": ["Slime Begleiter Evolution Dragon Quest Digimon"],
                "expected": ["8 Slime-Typen", "Evolution", "Anfeuern-System"]
            },
            "6. DIGIVICE INTERFACE": {
                "queries": ["Digivice Interface Mobile Flutter Three.js"],
                "expected": ["Mobile App", "Browser Interface", "Care-System"]
            },
            "7. TECHNISCHE ARCHITEKTUR": {
                "queries": ["Backend FastAPI Ollama ChromaDB Port 8000"],
                "expected": ["Port 8000", "Ollama", "ChromaDB", "127.0.0.1"]
            },
            "8. TRAINING SYSTEM": {
                "queries": ["LoRA Training Qwen Dolphin Fine-Tuning"],
                "expected": ["LoRA Checkpoints", "Qwen2.5-7B", "Training Data"]
            },
            "9. QUEST SYSTEM": {
                "queries": ["Quest System Oregon Trail Events Entscheidungen"],
                "expected": ["Oregon Trail Events", "Konsequenzen", "Story Quests"]
            },
            "10. PVP/PVE SYSTEM": {
                "queries": ["PvP Arena PvE Safe Zone Schwarze Muehle"],
                "expected": ["Schwarze Muehle Safe", "Arena PvP", "Opt-in PvP"]
            }
        }

    def review_area(self, name, config):
        """Reviewt einen Projektbereich"""
        print(f"\n{'='*70}")
        print(f"  {name}")
        print(f"{'='*70}")

        results = []
        for query in config['queries']:
            results.extend(self.search(query, n=3))

        if results:
            print(f"\n[GEFUNDEN] {len(results)} relevante Eintraege:")
            seen_sources = set()
            for r in results[:5]:
                source = r['source']
                if source not in seen_sources:
                    seen_sources.add(source)
                    print(f"\n  Quelle: {source}")
                    print(f"  {r['content'][:300]}...")
        else:
            print("\n[WARNUNG] Keine Informationen gefunden!")

        # Check expected items
        print(f"\n[ERWARTET]: {', '.join(config['expected'])}")

        return results

    def find_prepared_content(self):
        """Findet vorbereitete Sachen von verschiedenen Modellen"""
        print("\n" + "=" * 70)
        print("  VORBEREITETE INHALTE VON VERSCHIEDENEN MODELLEN")
        print("=" * 70)

        queries = [
            "GPT Claude Gemini vorbereitet geplant Konzept",
            "TODO implementieren Feature geplant",
            "vorbereitet erstellt generiert Modell",
            "Roadmap Phase naechste Schritte",
            "Design Document Spezifikation"
        ]

        all_results = []
        for query in queries:
            results = self.search(query, n=5)
            all_results.extend(results)

        if all_results:
            print(f"\n[GEFUNDEN] {len(all_results)} vorbereitete Inhalte:")
            seen = set()
            for r in all_results[:15]:
                source = r['source']
                if source not in seen:
                    seen.add(source)
                    print(f"\n  [{r['kategorie']}] {source}")
                    # Suche nach Model-Hinweisen
                    content = r['content'].lower()
                    models = []
                    if 'gpt' in content or 'chatgpt' in content:
                        models.append('GPT')
                    if 'claude' in content:
                        models.append('Claude')
                    if 'gemini' in content:
                        models.append('Gemini')
                    if 'ollama' in content or 'qwen' in content:
                        models.append('Ollama/Qwen')
                    if models:
                        print(f"  Modelle: {', '.join(models)}")

        return all_results

    def find_unused_resources(self):
        """Findet ungenutzte/vergessene Ressourcen"""
        print("\n" + "=" * 70)
        print("  VERGESSENE/UNGENUTZTE RESSOURCEN")
        print("=" * 70)

        queries = [
            "archiv alt backup version",
            "deprecated veraltet nicht genutzt",
            "TODO FIXME implementieren fehlt",
            "idee konzept geplant nicht fertig"
        ]

        all_results = []
        for query in queries:
            results = self.search(query, n=5)
            all_results.extend(results)

        if all_results:
            print(f"\n[GEFUNDEN] {len(all_results)} potenziell vergessene Ressourcen:")
            seen = set()
            for r in all_results[:10]:
                source = r['source']
                if source not in seen and 'alles wissen' in source.lower():
                    seen.add(source)
                    print(f"\n  {source}")

        return all_results

    def generate_questions_for_najika(self):
        """Generiert Fragen fuer Najika"""
        print("\n" + "=" * 70)
        print("  FRAGEN FUER NAJIKA")
        print("=" * 70)

        questions = [
            "1. Welche Features wurden geplant aber nie implementiert?",
            "2. Was haben wir fruher anders gemacht das besser war?",
            "3. Welche Dokumente aus 'alles wissen' sind noch wichtig?",
            "4. Was fehlt im aktuellen System verglichen mit der urspruenglichen Vision?",
            "5. Welche vorbereiteten Inhalte von GPT/Claude sollten wir nutzen?",
            "6. Gibt es vergessene Game-Mechaniken die wir einbauen sollten?",
            "7. Was war der urspruengliche Plan fuer das Slime-System?",
            "8. Welche Training-Daten fehlen noch?",
            "9. Was muss fuer die Mobile-App noch gemacht werden?",
            "10. Welche Persoenlichkeits-Aspekte sind noch nicht implementiert?"
        ]

        for q in questions:
            print(f"\n  {q}")

        return questions

    def run_full_review(self):
        """Fuehrt komplette Review durch"""
        areas = self.get_project_areas()

        # Review alle Bereiche
        for name, config in areas.items():
            self.review_area(name, config)

        # Finde vorbereitete Inhalte
        self.find_prepared_content()

        # Finde vergessene Ressourcen
        self.find_unused_resources()

        # Generiere Fragen
        self.generate_questions_for_najika()

        print("\n" + "=" * 70)
        print("  REVIEW ABGESCHLOSSEN")
        print("=" * 70)
        print("\nNaechster Schritt: Diese Fragen mit Najika besprechen!")


def main():
    review = NajikaProjectReview()
    review.run_full_review()


if __name__ == "__main__":
    main()
