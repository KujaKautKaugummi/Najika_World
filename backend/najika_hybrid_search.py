#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA HYBRID SEARCH - Best of Both Worlds

Kombiniert GREP (schnell & exakt) mit ChromaDB (semantisch & intelligent)
Auto-Switching basierend auf Query-Typ!
"""

import sys
import io
import re
from pathlib import Path
from typing import List, Dict, Literal

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    from najika_project_analyzer import NajikaProjectAnalyzer
    CHROMADB_AVAILABLE = True
except:
    CHROMADB_AVAILABLE = False


class NajikaHybridSearch:
    """Hybrid Search System - GREP + ChromaDB"""

    def __init__(self, project_root: str = "C:\\Najika_World"):
        self.project_root = Path(project_root)

        # GREP Setup (immer verfügbar)
        self.najika_files = self._find_najika_files()

        # ChromaDB Setup (optional)
        if CHROMADB_AVAILABLE:
            self.analyzer = NajikaProjectAnalyzer(str(project_root))
            print("✅ Hybrid Mode: GREP + ChromaDB")
        else:
            self.analyzer = None
            print("⚠️  Fallback Mode: GREP only (ChromaDB nicht verfügbar)")

    def _find_najika_files(self) -> List[Path]:
        """Findet alle Najika-Dokumente"""
        extensions = {".txt", ".md"}
        exclude_dirs = {
            "node_modules", "__pycache__", ".git", ".venv", "venv",
            "chroma_db", "chroma_project_db", "chroma_project_db_v2",
            ".dart_tool", "build", "training_data_real"
        }

        files = []
        for file in self.project_root.rglob("*"):
            if any(excluded in file.parts for excluded in exclude_dirs):
                continue
            if file.is_file() and file.suffix in extensions:
                files.append(file)

        return files

    def _detect_search_mode(self, query: str) -> Literal["grep", "chromadb"]:
        """
        Entscheidet automatisch zwischen GREP und ChromaDB

        GREP für:
        - Dateinamen (*.py, README.md, etc.)
        - Spezifische Keywords (TODO, FIXME, etc.)
        - Funktionsnamen (def xyz, class ABC)
        - Exakte Strings

        ChromaDB für:
        - Fragen ("Wie funktioniert...?", "Was ist...?")
        - Konzepte ("Battle System", "AI Architecture")
        - Beschreibungen ("System für...")
        """

        query_lower = query.lower()

        # GREP Trigger
        grep_patterns = [
            r'\*\.',  # *.py, *.md
            r'\.py$|\.md$|\.txt$',  # Dateiendungen
            r'^(def|class|import|TODO|FIXME)\s',  # Code-Keywords
            r'filename|dateiname',  # Dateinamen-Suche
        ]

        for pattern in grep_patterns:
            if re.search(pattern, query_lower):
                return "grep"

        # ChromaDB Trigger (wenn verfügbar)
        if self.analyzer:
            chromadb_patterns = [
                r'^(wie|was|warum|wann|wo)',  # Fragen
                r'funktioniert|bedeutet|erkläre|beschreibe',  # Erklärungen
                r'system|architektur|konzept|feature',  # Konzepte
            ]

            for pattern in chromadb_patterns:
                if re.search(pattern, query_lower):
                    return "chromadb"

        # Default: GREP (immer verfügbar)
        return "grep"

    def _grep_search(self, query: str, n_results: int = 10) -> List[Dict]:
        """GREP-basierte Suche"""
        keywords = query.lower().split()
        matches = []

        for file in self.najika_files[:500]:  # Limit für Performance
            try:
                with open(file, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    line_lower = line.lower()

                    if any(kw in line_lower for kw in keywords):
                        # Kontext: 2 Zeilen davor + match + 2 danach
                        start = max(0, line_num - 3)
                        end = min(len(lines), line_num + 2)
                        context = "".join(lines[start:end])

                        matches.append({
                            "file": str(file.relative_to(self.project_root)),
                            "line": line_num,
                            "context": context[:500],
                            "score": sum(1 for kw in keywords if kw in line_lower)
                        })

                        if len(matches) >= n_results * 2:  # Sammle mehr als nötig
                            break

            except Exception:
                continue

            if len(matches) >= n_results * 2:
                break

        # Sortiere nach Score und nimm Top N
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:n_results]

    def _chromadb_search(self, query: str, n_results: int = 10) -> List[Dict]:
        """ChromaDB Semantic Search"""
        if not self.analyzer:
            return []

        try:
            results = self.analyzer.search(query, n_results=n_results)

            # Format ähnlich zu GREP
            formatted = []
            for result in results:
                formatted.append({
                    "file": result['metadata']['file_path'],
                    "context": result['text'][:500],
                    "score": 1.0 - result.get('distance', 0),  # Invert distance
                    "source": "chromadb"
                })

            return formatted

        except Exception as e:
            print(f"⚠️  ChromaDB Error: {e}")
            return []

    def search(self, query: str, n_results: int = 10, mode: str = "auto") -> List[Dict]:
        """
        Hybrid Search

        Args:
            query: Suchbegriff oder Frage
            n_results: Anzahl Ergebnisse
            mode: "auto", "grep", "chromadb"

        Returns:
            Liste von Ergebnissen mit file, context, score
        """

        # Auto-Detect Mode
        if mode == "auto":
            mode = self._detect_search_mode(query)

        print(f"🔍 Search Mode: {mode.upper()}")
        print(f"📝 Query: {query}")
        print()

        # Führe Suche durch
        if mode == "grep":
            results = self._grep_search(query, n_results)
        elif mode == "chromadb":
            results = self._chromadb_search(query, n_results)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        print(f"✅ {len(results)} Ergebnisse gefunden\n")
        return results


def main():
    """CLI für Hybrid Search"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA HYBRID SEARCH - GREP + ChromaDB                     ║
╚══════════════════════════════════════════════════════════════╝

Auto-Switching zwischen:
- GREP: Schnell & exakt (Keywords, Dateinamen)
- ChromaDB: Semantisch & intelligent (Fragen, Konzepte)

""")

    searcher = NajikaHybridSearch()

    # Test-Queries
    test_queries = [
        "najika_server.py",  # GREP
        "Wie funktioniert das Battle System?",  # ChromaDB
        "TODO implementieren",  # GREP
        "Was ist die Schwarze Mühle?",  # ChromaDB
    ]

    for query in test_queries:
        print("="*70)
        results = searcher.search(query, n_results=3)

        for i, result in enumerate(results, 1):
            print(f"[{i}] {result['file']}")
            if 'line' in result:
                print(f"    Line: {result['line']}")
            print(f"    Score: {result['score']:.2f}")
            print(f"    Context: {result['context'][:100]}...")
            print()

        print()


if __name__ == "__main__":
    main()
