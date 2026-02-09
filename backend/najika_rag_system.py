#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=======================================================================
NAJIKA RAG SYSTEM - Retrieval Augmented Generation
=======================================================================

Dieses Modul ermöglicht Najika, automatisch ihr Wissen aus ChromaDB
abzurufen und in Gespräche einzubauen.

Funktionsweise:
1. User stellt Frage
2. RAG System sucht relevante Chunks in ChromaDB
3. Chunks werden zum Prompt hinzugefügt
4. Ollama generiert Antwort mit dem zusätzlichen Kontext

Erstellt: 2026-01-29
"""

import sys

# HINWEIS: Keine stdout/stderr Manipulation hier!
# Das verursacht "I/O operation on closed file" Fehler im Server-Kontext.

import chromadb
from typing import List, Dict, Optional, Tuple
import re

# ChromaDB Pfad
CHROMADB_PATH = "C:/Najika_World/memory_db"

# Collections die durchsucht werden (in Prioritätsreihenfolge)
SEARCH_COLLECTIONS = [
    "najika_wichtige_docs",      # Alle wichtigen Projekt-Dokumente
    "najika_project_knowledge",  # Projekt-Wissen (JSON)
    "najika_personalities",      # Persönlichkeits-Training
    "najika_core",               # Kern-Wahrheiten (höchste Priorität!)
]

# Maximale Tokens für RAG-Context (ca. 1500 Zeichen = ~400 Tokens)
MAX_RAG_CONTEXT_CHARS = 1500

# Keywords die RAG-Suche triggern
RAG_TRIGGER_KEYWORDS = [
    # Spielsysteme
    "skill", "kampf", "combat", "explosion", "megumin", "omega", "ultima",
    "1-weg", "einweg", "spezialisierung", "trade-off",
    # Lore
    "schwarze mühle", "windmühle", "kuja", "mr. k", "owner",
    "8 gebote", "gebote", "regeln",
    # Technik
    "chromadb", "ollama", "backend", "frontend",
    # Persönlichkeit
    "harley", "shiro", "melissa", "persönlichkeit",
    # Allgemein
    "erkläre", "was ist", "wie funktioniert", "wer ist", "warum",
    "erzähl mir", "weißt du", "erinnerst du dich"
]

class NajikaRAG:
    """RAG System für Najika's Wissensabruf"""

    def __init__(self):
        self.client = None
        self.collections = {}
        self.enabled = False
        self._init_chromadb()

    def _init_chromadb(self):
        """Initialisiert ChromaDB Verbindung"""
        try:
            self.client = chromadb.PersistentClient(path=CHROMADB_PATH)

            # Lade alle Collections
            for name in SEARCH_COLLECTIONS:
                try:
                    self.collections[name] = self.client.get_collection(name)
                    print(f"[RAG] OK Collection '{name}' geladen: {self.collections[name].count()} Eintraege")
                except Exception as e:
                    print(f"[RAG] WARNING Collection '{name}' nicht gefunden: {e}")

            if self.collections:
                self.enabled = True
                print(f"[RAG] OK System aktiviert mit {len(self.collections)} Collections")
            else:
                print("[RAG] WARNING Keine Collections gefunden - RAG deaktiviert")

        except Exception as e:
            print(f"[RAG] ERROR ChromaDB Fehler: {e}")
            self.enabled = False

    def should_search(self, user_message: str) -> bool:
        """Prüft ob RAG-Suche für diese Nachricht sinnvoll ist"""
        if not self.enabled:
            return False

        msg_lower = user_message.lower()

        # Kurze Nachrichten (Smalltalk) brauchen kein RAG
        if len(user_message) < 15:
            return False

        # Prüfe Trigger-Keywords
        for keyword in RAG_TRIGGER_KEYWORDS:
            if keyword in msg_lower:
                return True

        # Fragen triggern immer RAG
        if "?" in user_message:
            return True

        return False

    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """Durchsucht alle Collections nach relevanten Chunks"""
        if not self.enabled:
            return []

        all_results = []

        for name, collection in self.collections.items():
            try:
                results = collection.query(
                    query_texts=[query],
                    n_results=n_results
                )

                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                        distance = results['distances'][0][i] if results.get('distances') else 1.0

                        all_results.append({
                            'content': doc,
                            'collection': name,
                            'metadata': metadata,
                            'distance': distance,
                            'source': metadata.get('dateiname', metadata.get('source_file', 'unbekannt'))
                        })

            except Exception as e:
                print(f"[RAG] WARNING Suche in '{name}' fehlgeschlagen: {e}")

        # Sortiere nach Relevanz (niedrigere Distance = relevanter)
        all_results.sort(key=lambda x: x['distance'])

        return all_results[:n_results * 2]  # Mehr Ergebnisse für bessere Auswahl

    def get_context(self, user_message: str) -> Tuple[str, List[str]]:
        """
        Holt relevanten Kontext für eine User-Nachricht.

        Returns:
            Tuple[str, List[str]]: (Context-String für Prompt, Liste der Quellen)
        """
        if not self.should_search(user_message):
            return "", []

        # Suche nach relevanten Chunks
        results = self.search(user_message, n_results=3)

        if not results:
            return "", []

        # Baue Context zusammen
        context_parts = []
        sources = []
        total_chars = 0

        for result in results:
            content = result['content']
            source = result['source']

            # Kürze Content wenn nötig
            available_chars = MAX_RAG_CONTEXT_CHARS - total_chars
            if len(content) > available_chars:
                content = content[:available_chars] + "..."

            if content.strip():
                context_parts.append(f"[{source}]: {content}")
                sources.append(source)
                total_chars += len(content)

            if total_chars >= MAX_RAG_CONTEXT_CHARS:
                break

        if not context_parts:
            return "", []

        context = "\n\n".join(context_parts)

        # Formatiere als RAG-Context fuer Prompt
        # HINWEIS: Keine Anweisungen hier! Das Model hat die Persona bereits.
        # Dieses Wissen ist nur ZUSATZ-INFO, keine Befehle!
        rag_context = f"""Relevantes Wissen zu diesem Thema:
{context}"""

        return rag_context, list(set(sources))

    def enhance_prompt(self, user_message: str, original_prompt: str) -> str:
        """
        Erweitert den Prompt mit RAG-Kontext.

        Args:
            user_message: Die originale Nachricht des Users
            original_prompt: Der bereits formatierte Prompt

        Returns:
            str: Erweiterter Prompt mit RAG-Kontext
        """
        context, sources = self.get_context(user_message)

        if not context:
            return original_prompt

        # Füge Context VOR der User-Nachricht ein
        enhanced = f"{context}\n\n{original_prompt}"

        print(f"[RAG] CONTEXT Kontext hinzugefuegt von: {', '.join(sources)}")

        return enhanced

    def get_stats(self) -> Dict:
        """Gibt Statistiken über das RAG-System zurück"""
        stats = {
            "enabled": self.enabled,
            "collections": {}
        }

        for name, collection in self.collections.items():
            try:
                stats["collections"][name] = collection.count()
            except:
                stats["collections"][name] = 0

        stats["total_entries"] = sum(stats["collections"].values())

        return stats


# Globale Instanz
RAG_SYSTEM = NajikaRAG()


def get_rag_context(user_message: str) -> str:
    """Convenience-Funktion für RAG-Kontext"""
    context, _ = RAG_SYSTEM.get_context(user_message)
    return context


def enhance_prompt_with_rag(user_message: str, prompt: str) -> str:
    """Convenience-Funktion für Prompt-Enhancement"""
    return RAG_SYSTEM.enhance_prompt(user_message, prompt)


def rag_enabled() -> bool:
    """Prüft ob RAG aktiviert ist"""
    return RAG_SYSTEM.enabled


def get_rag_stats() -> Dict:
    """Gibt RAG-Statistiken zurück"""
    return RAG_SYSTEM.get_stats()


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA RAG SYSTEM TEST")
    print("=" * 60)

    print(f"\nRAG Enabled: {RAG_SYSTEM.enabled}")
    print(f"Stats: {RAG_SYSTEM.get_stats()}")

    test_queries = [
        "Was sind die 8 Gebote?",
        "Erkläre das 1-Weg-Skill System",
        "Wer ist Mr. K?",
        "Was ist die Schwarze Mühle?",
        "Wie funktioniert Omega-Detonation?"
    ]

    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        context, sources = RAG_SYSTEM.get_context(query)
        if context:
            print(f"Sources: {sources}")
            print(f"Context (erste 300 Zeichen):\n{context[:300]}...")
        else:
            print("Kein Kontext gefunden")
