"""
NAJIKA WEB SEARCH MODULE
DuckDuckGo Search Integration für Najika
"""

from ddgs import DDGS
from datetime import datetime
import json
import re


class NajikaSearch:
    def __init__(self):
        """
        Initialisiert das DuckDuckGo Search System
        """
        self.ddgs = DDGS()
        print("[NAJIKA SEARCH] OK Web Search initialisiert")

    def needs_search(self, user_message):
        """
        Erkennt, ob eine Web-Suche notwendig ist
        """
        search_triggers = [
            # Deutsch
            r"\bsuche\b", r"\bfinde\b", r"\bwas ist\b", r"\bwer ist\b",
            r"\bwann\b", r"\bwo\b", r"\bwie\b", r"\bwarum\b",
            r"\bnachrichten\b", r"\bnews\b", r"\baktuell\b",
            r"\bgoogle\b", r"\bwikipedia\b", r"\binfo\b",

            # English
            r"\bsearch\b", r"\bfind\b", r"\bwhat is\b", r"\bwho is\b",
            r"\bwhen\b", r"\bwhere\b", r"\bhow\b", r"\bwhy\b",
            r"\bnews\b", r"\bcurrent\b", r"\blatest\b",
            r"\bwikipedia\b", r"\binfo\b", r"\btell me about\b"
        ]

        user_lower = user_message.lower()
        for trigger in search_triggers:
            if re.search(trigger, user_lower):
                print(f"[SEARCH] >> Trigger erkannt: {trigger}")
                return True

        return False

    def search_web(self, query, max_results=5):
        """
        Führt eine DuckDuckGo Suche aus

        Args:
            query: Suchbegriff
            max_results: Maximale Anzahl Ergebnisse (default: 5)

        Returns:
            List of search results
        """
        try:
            print(f"[SEARCH] >> Suche nach: '{query}'")

            # DuckDuckGo Text Search
            results = []
            for r in self.ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })

            print(f"[SEARCH] OK {len(results)} Ergebnisse gefunden")
            return results

        except Exception as e:
            print(f"[SEARCH] WARNING Fehler bei Web-Suche: {e}")
            return []

    def search_news(self, query, max_results=5):
        """
        Sucht nach aktuellen News
        """
        try:
            print(f"[SEARCH] >> News-Suche: '{query}'")

            results = []
            for r in self.ddgs.news(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("body", ""),
                    "date": r.get("date", ""),
                    "source": r.get("source", "")
                })

            print(f"[SEARCH] OK {len(results)} News gefunden")
            return results

        except Exception as e:
            print(f"[SEARCH] WARNING Fehler bei News-Suche: {e}")
            return []

    def extract_search_query(self, user_message):
        """
        Extrahiert den Suchbegriff aus der User-Nachricht

        Beispiele:
        - "Suche nach Python tutorials" → "Python tutorials"
        - "Was ist Quantum Computing?" → "Quantum Computing"
        - "Finde Informationen über KI" → "KI"
        """
        # Remove common trigger words
        query = user_message

        # Deutsch
        query = re.sub(r"^(suche|finde|zeig mir|was ist|wer ist|erzähl mir über|informationen über)\s+", "", query, flags=re.IGNORECASE)
        query = re.sub(r"\s+(im internet|online|web)$", "", query, flags=re.IGNORECASE)

        # English
        query = re.sub(r"^(search for|find|show me|what is|who is|tell me about|info about|information about)\s+", "", query, flags=re.IGNORECASE)
        query = re.sub(r"\s+(online|on the web|on the internet)$", "", query, flags=re.IGNORECASE)

        # Remove trailing punctuation
        query = re.sub(r"[?.!]+$", "", query).strip()

        return query

    def format_results_for_ai(self, results, query):
        """
        Formatiert die Suchergebnisse für Najika's AI-Kontext
        """
        if not results:
            return f"[SEARCH] Keine Ergebnisse für '{query}' gefunden."

        # Kompakte Formatierung - nur die wichtigsten Infos
        formatted = [f"[SEARCH-CONTEXT für '{query}']"]

        for i, result in enumerate(results[:3], 1):  # Nur Top-3 Ergebnisse
            title = result.get("title", "")
            snippet = result.get("snippet", "")[:200]  # Erste 200 chars

            formatted.append(f"{i}. {title}: {snippet}")

        # WICHTIG: Klare Anweisung an Najika
        formatted.append("\n[ANWEISUNG] Beantworte Kujas Frage NATÜRLICH in DEINER NAJIKA-PERSÖNLICHKEIT basierend auf diesen Infos. KEINE rohen Suchergebnisse ausgeben!")

        return "\n".join(formatted)

    def search_and_format(self, user_message, search_type="text", max_results=5):
        """
        Kompletter Search-Workflow: Erkennung → Suche → Formatierung

        Args:
            user_message: User-Nachricht
            search_type: "text" oder "news"
            max_results: Max Ergebnisse

        Returns:
            Formatierter String für AI-Kontext oder None
        """
        if not self.needs_search(user_message):
            return None

        # Suchbegriff extrahieren
        query = self.extract_search_query(user_message)
        if not query or len(query) < 2:
            print("[SEARCH] WARNING Kein gueltiger Suchbegriff gefunden")
            return None

        # Suche ausführen
        if search_type == "news":
            results = self.search_news(query, max_results)
        else:
            results = self.search_web(query, max_results)

        # Für AI formatieren
        return self.format_results_for_ai(results, query)


# Test-Funktion
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA SEARCH SYSTEM TEST")
    print("=" * 60)

    # Search initialisieren
    search = NajikaSearch()

    # Test 1: Trigger Detection
    print("\n" + "=" * 60)
    print("TEST 1: Trigger Detection")
    print("=" * 60)

    test_messages = [
        "Hallo Najika, wie geht es dir?",  # Kein Trigger
        "Suche nach Python tutorials",  # Trigger
        "Was ist Quantum Computing?",  # Trigger
        "Ich liebe dich",  # Kein Trigger
        "Finde Informationen über KI"  # Trigger
    ]

    for msg in test_messages:
        needs = search.needs_search(msg)
        print(f"'{msg}' → Suche: {needs}")

    # Test 2: Query Extraction
    print("\n" + "=" * 60)
    print("TEST 2: Query Extraction")
    print("=" * 60)

    for msg in ["Suche nach Python tutorials", "Was ist Quantum Computing?", "Finde Informationen über KI im Internet"]:
        query = search.extract_search_query(msg)
        print(f"'{msg}' → Query: '{query}'")

    # Test 3: Real Search (nur wenn ddgs installiert ist)
    print("\n" + "=" * 60)
    print("TEST 3: Real Web Search")
    print("=" * 60)

    try:
        user_msg = "Was ist Ollama?"
        formatted = search.search_and_format(user_msg, max_results=3)
        if formatted:
            print(formatted)
        else:
            print("⚠️ Kein Search durchgeführt")
    except Exception as e:
        print(f"⚠️ Search Test fehlgeschlagen: {e}")
        print("   Möglicherweise ist 'ddgs' noch nicht installiert.")
        print("   Installiere mit: pip install ddgs")

    print("\n" + "=" * 60)
    print("✅ NAJIKA SEARCH TEST ABGESCHLOSSEN")
    print("=" * 60)
