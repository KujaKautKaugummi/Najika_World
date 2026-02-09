#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA QUICK ANALYZER - Nutzt existierende API direkt

Einfachste Lösung:
1. Nutze index_all_documents() mit scan_all=True
2. Schließe Training Data aus via exclude_dirs
3. Führe dann Searches durch
"""

import sys
import io
import json
from pathlib import Path
from typing import Dict

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Temporärer Workaround: Modifiziere NajikaProjectAnalyzer vor Import
import najika_project_analyzer
original_find = najika_project_analyzer.NajikaProjectAnalyzer.find_documents

def patched_find_documents(self, search_paths=None, scan_all=True):
    """Patched version die training_data_real ausschließt"""
    found_files = []
    extensions = {".txt", ".md", ".pdf", ".py", ".json"}

    if scan_all:
        print(f"🔍 NAJIKA-FOCUSED SCAN: {self.project_root}")

        exclude_dirs = {
            "node_modules", "__pycache__", ".git", ".venv", "venv",
            "chroma_db", "chroma_project_db", ".dart_tool", "build",
            "training_data_real"  # AUSGESCHLOSSEN!
        }

        for file in self.project_root.rglob("*"):
            if any(excluded in file.parts for excluded in exclude_dirs):
                continue
            if file.is_file() and file.suffix in extensions:
                found_files.append(file)

        found_files = list(set(found_files))
        print(f"✅ {len(found_files)} Najika-Dokumente gefunden")
        return found_files

    return original_find(self, search_paths, scan_all)

# Monkey-patch
najika_project_analyzer.NajikaProjectAnalyzer.find_documents = patched_find_documents

from najika_project_analyzer import NajikaProjectAnalyzer


class NajikaQuickAnalyzer:
    """Nutzt bestehende API direkt"""

    def __init__(self):
        self.project_root = Path("C:\\Najika_World")
        self.analyzer = None
        self.results = {
            "phase1_overview": [],
            "phase2_roadmaps": [],
            "phase3_complete": [],
            "phase4_themes": {
                "schwarze_muehle": [],
                "digivice": [],
                "handy_app": [],
                "uefn": [],
            },
            "phase5_missing": []
        }

    def run(self) -> Dict:
        """Führt Analyse durch"""
        print("\n" + "="*70)
        print("🧠 NAJIKA QUICK ANALYZER")
        print("="*70 + "\n")

        # STEP 1: Index (mit Patch - ohne training_data_real)
        print("📊 INDEXING (ohne Training Data)")
        print("-"*70)
        self.analyzer = NajikaProjectAnalyzer(str(self.project_root))
        stats = self.analyzer.index_all_documents()

        print(f"\n✅ Indexing abgeschlossen!")
        print(f"   Files: {stats['files_scanned']:,}")
        print(f"   Chars: {stats['total_chars']:,}")
        print()

        # STEP 2-6: Alle Phasen
        print("📋 PHASE 1: ZUSAMMENFASSUNGEN")
        print("-"*70)
        self._phase1()

        print("\n🗺️  PHASE 2: ROADMAPS & TODOs")
        print("-"*70)
        self._phase2()

        print("\n✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN")
        print("-"*70)
        self._phase3()

        print("\n🎯 PHASE 4: THEMEN")
        print("-"*70)
        self._phase4()

        print("\n🔍 PHASE 5: VERGESSENES")
        print("-"*70)
        self._phase5()

        # STEP 7: Export
        print("\n💾 EXPORT")
        print("-"*70)
        self._export()

        return self.results

    def _phase1(self):
        """Zusammenfassungen"""
        queries = [
            "Zusammenfassung Projekt",
            "NAJIKA ULTIMATIVE ZUSAMMENFASSUNG",
            "Master Overview",
            "Complete Project"
        ]

        for query in queries:
            print(f"  🔍 {query}")
            results = self.analyzer.search(query, n_results=3)
            for result in results:
                self.results["phase1_overview"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500]
                })

        print(f"  ✅ {len(self.results['phase1_overview'])} gefunden")

    def _phase2(self):
        """Roadmaps"""
        queries = ["Roadmap", "TODO", "MEGA TODO", "NICHTS VERGESSEN"]
        for query in queries:
            print(f"  🔍 {query}")
            results = self.analyzer.search(query, n_results=3)
            for result in results:
                self.results["phase2_roadmaps"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500]
                })
        print(f"  ✅ {len(self.results['phase2_roadmaps'])} gefunden")

    def _phase3(self):
        """Vollständige Versionen"""
        queries = ["Vollständig", "Complete", "Final Version", "Finale"]
        for query in queries:
            print(f"  🔍 {query}")
            results = self.analyzer.search(query, n_results=3)
            for result in results:
                self.results["phase3_complete"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500]
                })
        print(f"  ✅ {len(self.results['phase3_complete'])} gefunden")

    def _phase4(self):
        """Themen"""
        themes = {
            "schwarze_muehle": ["Schwarze Mühle", "Gesichtern"],
            "digivice": ["Digivice", "najika_world_UNIFIED"],
            "handy_app": ["Flutter", "Mobile App", "APK"],
            "uefn": ["UEFN", "Fortnite", "Verse"]
        }

        for theme_key, queries in themes.items():
            print(f"  🎯 {theme_key.upper()}")
            for query in queries:
                results = self.analyzer.search(query, n_results=2)
                for result in results:
                    self.results["phase4_themes"][theme_key].append({
                        "query": query,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:300]
                    })
            count = len(self.results["phase4_themes"][theme_key])
            print(f"     ✅ {count} Dokumente")

    def _phase5(self):
        """Vergessenes"""
        queries = ["TODO implementieren", "fehlt noch", "muss noch", "geplant"]
        for query in queries:
            print(f"  🔍 {query}")
            results = self.analyzer.search(query, n_results=3)
            for result in results:
                self.results["phase5_missing"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500]
                })
        print(f"  ✅ {len(self.results['phase5_missing'])} gefunden")

    def _export(self):
        """Export Report"""
        # JSON
        json_file = self.project_root / "NAJIKA_ANALYSIS_REPORT.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"  ✅ JSON: {json_file}")

        # Markdown
        md_file = self.project_root / "NAJIKA_ANALYSIS_REPORT.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("# 🧠 NAJIKA ANALYSIS REPORT\n\n")
            f.write("="*70 + "\n\n")

            # Phase 1
            f.write("## 📋 PHASE 1: ZUSAMMENFASSUNGEN\n\n")
            for item in self.results["phase1_overview"][:15]:
                f.write(f"### {item['file']}\n")
                f.write(f"**Query:** {item['query']}\n\n")
                f.write(f"```\n{item['text']}\n```\n\n")
                f.write("-"*70 + "\n\n")

            # Phase 2
            f.write("## 🗺️ PHASE 2: ROADMAPS\n\n")
            for item in self.results["phase2_roadmaps"][:10]:
                f.write(f"### {item['file']}\n")
                f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 3
            f.write("## ✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN\n\n")
            for item in self.results["phase3_complete"][:10]:
                f.write(f"### {item['file']}\n")
                f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 4
            f.write("## 🎯 PHASE 4: THEMEN\n\n")
            for theme_key, items in self.results["phase4_themes"].items():
                f.write(f"### {theme_key.upper()}\n\n")
                for item in items[:5]:
                    f.write(f"#### {item['file']}\n")
                    f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 5
            f.write("## 🔍 PHASE 5: VERGESSENES\n\n")
            for item in self.results["phase5_missing"][:15]:
                f.write(f"### {item['file']}\n")
                f.write(f"```\n{item['text']}\n```\n\n")

        print(f"  ✅ Markdown: {md_file}")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA QUICK ANALYZER - Einfache Version                   ║
╚══════════════════════════════════════════════════════════════╝

- Scannt NUR Najika-Dokumente (ohne Training Data)
- ~2000 Files statt 33000
- Schneller & stabiler

""")

    analyzer = NajikaQuickAnalyzer()
    analyzer.run()

    print("\n" + "="*70)
    print("🎉 FERTIG!")
    print("="*70)
    print("\nREPORTS:")
    print("- NAJIKA_ANALYSIS_REPORT.md")
    print("- NAJIKA_ANALYSIS_REPORT.json")


if __name__ == "__main__":
    main()
