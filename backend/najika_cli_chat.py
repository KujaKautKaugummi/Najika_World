#!/usr/bin/env python3
"""
NAJIKA CLI CHAT
Direkte Kommunikation mit Najika ueber CLI
Nutzt ChromaDB fuer RAG und Claude Code fuer Antworten
"""

import sys
import os

# UTF-8 fuer Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import chromadb
from datetime import datetime

# Pfade
MEMORY_DB = "C:/Najika_World/memory_db"
PROJECT_ROOT = "C:/Najika_World"


class NajikaCliChat:
    def __init__(self):
        print("=" * 60)
        print("  NAJIKA CLI CHAT")
        print("  Direkte Kommunikation mit Najikas Wissensdatenbank")
        print("=" * 60)
        print()

        # ChromaDB
        self.client = chromadb.PersistentClient(path=MEMORY_DB)
        self.collections = {
            'wichtig': self.client.get_collection('najika_wichtige_docs'),
            'complete': self.client.get_or_create_collection('najika_complete_knowledge'),
            'alle': self.client.get_collection('najika_alle_dokumente'),
            'personalities': self.client.get_collection('najika_personalities'),
        }

        # Stats
        print("[KNOWLEDGE DATABASE]")
        total = 0
        for name, col in self.collections.items():
            count = col.count()
            total += count
            print(f"  {name}: {count} entries")
        print(f"  TOTAL: {total} entries")
        print()

    def search_knowledge(self, query, n_results=5):
        """Sucht in allen Collections nach relevantem Wissen"""
        results = []

        for name, col in self.collections.items():
            try:
                res = col.query(
                    query_texts=[query],
                    n_results=min(n_results, col.count()) if col.count() > 0 else 1,
                    include=['documents', 'metadatas', 'distances']
                )

                if res and res.get('documents') and res['documents'][0]:
                    for i, doc in enumerate(res['documents'][0]):
                        meta = res['metadatas'][0][i] if res.get('metadatas') else {}
                        dist = res['distances'][0][i] if res.get('distances') else 0

                        results.append({
                            'collection': name,
                            'content': doc[:500] if doc else '',
                            'source': meta.get('source', meta.get('pfad', 'unknown')),
                            'distance': dist
                        })
            except Exception as e:
                print(f"  [WARN] {name}: {e}")

        # Sortiere nach Relevanz (niedrigere Distanz = besser)
        results.sort(key=lambda x: x['distance'])
        return results[:n_results]

    def format_context(self, results):
        """Formatiert Suchergebnisse als Kontext"""
        if not results:
            return "Keine relevanten Informationen gefunden."

        context = "RELEVANTES WISSEN AUS NAJIKAS DATENBANK:\n\n"
        for i, r in enumerate(results, 1):
            context += f"[{i}] Quelle: {r['source']}\n"
            context += f"    {r['content'][:300]}...\n\n"

        return context

    def chat(self, user_input):
        """Verarbeitet User-Input und generiert Antwort"""
        print(f"\n[SUCHE] Durchsuche Wissensdatenbank...")

        # Suche relevantes Wissen
        results = self.search_knowledge(user_input, n_results=5)

        if results:
            print(f"[GEFUNDEN] {len(results)} relevante Eintraege")
            for r in results[:3]:
                print(f"  - {r['source'][:50]}... (dist: {r['distance']:.3f})")
        else:
            print("[INFO] Keine direkten Treffer gefunden")

        context = self.format_context(results)

        # Antwort generieren
        print("\n[NAJIKA]")
        print("-" * 40)

        # Einfache Antwort basierend auf Kontext
        if results:
            print(f"Ich habe {len(results)} relevante Informationen gefunden:\n")
            for i, r in enumerate(results[:3], 1):
                source = r['source']
                content = r['content'][:200]
                print(f"{i}. Aus '{source}':")
                print(f"   {content}...")
                print()
        else:
            print("Zu dieser Frage habe ich keine spezifischen Informationen in meiner Datenbank.")
            print("Moechtest du, dass ich nach etwas anderem suche?")

        print("-" * 40)

        return results

    def run(self):
        """Startet interaktiven Chat-Loop"""
        print("\nBereit! Stelle mir eine Frage ueber das Najika-Projekt.")
        print("Befehle: 'quit' zum Beenden, 'stats' fuer Statistiken")
        print()

        while True:
            try:
                user_input = input("DU > ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nAuf Wiedersehen! EXPLOSION!!!")
                    break

                if user_input.lower() == 'stats':
                    print("\n[STATISTIKEN]")
                    for name, col in self.collections.items():
                        print(f"  {name}: {col.count()}")
                    continue

                self.chat(user_input)

            except KeyboardInterrupt:
                print("\n\nAbgebrochen. Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}")


def main():
    chat = NajikaCliChat()
    chat.run()


if __name__ == "__main__":
    main()
