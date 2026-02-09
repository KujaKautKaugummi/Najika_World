#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA SEARCH ONLY - Nutzt EXISTIERENDE ChromaDB

Die DB ist bereits indexiert (2.1 GB)!
Wir müssen nur noch suchen!
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

from najika_project_analyzer import NajikaProjectAnalyzer


class NajikaSearchOnly:
    """Nutzt existierende ChromaDB zum Suchen"""

    def __init__(self):
        self.project_root = Path("C:\\Najika_World")
        print("📚 Lade existierende ChromaDB...")
        self.analyzer = NajikaProjectAnalyzer(str(self.project_root))
        print("✅ ChromaDB geladen!\n")

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
        """Führt NUR SEARCHES durch"""
        print("="*70)
        print("🔍 NAJIKA SEARCH-ONLY ANALYZER")
        print("="*70 + "\n")

        print("📋 PHASE 1: ZUSAMMENFASSUNGEN")
        self._phase1()

        print("\n🗺️  PHASE 2: ROADMAPS & TODOs")
        self._phase2()

        print("\n✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN")
        self._phase3()

        print("\n🎯 PHASE 4: THEMEN")
        self._phase4()

        print("\n🔍 PHASE 5: VERGESSENES")
        self._phase5()

        print("\n💾 EXPORT")
        self._export()

        return self.results

    def _phase1(self):
        """Zusammenfassungen"""
        queries = [
            "Zusammenfassung Projekt Najika",
            "NAJIKA ULTIMATIVE ZUSAMMENFASSUNG",
            "Master Overview Najika World",
            "Complete Project Najika",
            "Projekt Übersicht"
        ]

        for query in queries:
            print(f"  🔍 {query[:40]}...")
            try:
                results = self.analyzer.search(query, n_results=3)
                for result in results:
                    self.results["phase1_overview"].append({
                        "query": query,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:500]
                    })
            except Exception as e:
                print(f"     ⚠️  Error: {e}")

        print(f"  ✅ {len(self.results['phase1_overview'])} Dokumente")

    def _phase2(self):
        """Roadmaps"""
        queries = [
            "Roadmap Najika",
            "TODO Liste Najika",
            "MEGA TODO",
            "NICHTS VERGESSEN",
            "Aufgaben Liste"
        ]

        for query in queries:
            print(f"  🔍 {query[:40]}...")
            try:
                results = self.analyzer.search(query, n_results=3)
                for result in results:
                    self.results["phase2_roadmaps"].append({
                        "query": query,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:500]
                    })
            except Exception as e:
                print(f"     ⚠️  Error: {e}")

        print(f"  ✅ {len(self.results['phase2_roadmaps'])} Dokumente")

    def _phase3(self):
        """Vollständige Versionen"""
        queries = [
            "Vollständig Najika",
            "Complete Version",
            "Final Version Najika",
            "Finale Najika",
            "Alles zusammen"
        ]

        for query in queries:
            print(f"  🔍 {query[:40]}...")
            try:
                results = self.analyzer.search(query, n_results=3)
                for result in results:
                    self.results["phase3_complete"].append({
                        "query": query,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:500]
                    })
            except Exception as e:
                print(f"     ⚠️  Error: {e}")

        print(f"  ✅ {len(self.results['phase3_complete'])} Dokumente")

    def _phase4(self):
        """Themen"""
        themes = {
            "schwarze_muehle": [
                "Schwarze Mühle Najika",
                "Schwarze Windmühle",
                "Gesichtern Bereich",
                "Mühle Digivice"
            ],
            "digivice": [
                "Digivice Najika",
                "najika_world_UNIFIED.html",
                "3D Scene Najika",
                "Terminal Digivice"
            ],
            "handy_app": [
                "Flutter App Najika",
                "Handy Spiel Najika",
                "Mobile App Najika",
                "Android APK Najika"
            ],
            "uefn": [
                "UEFN Najika",
                "Fortnite Creative Najika",
                "Verse Code Najika",
                "Unreal Editor Najika"
            ]
        }

        for theme_key, queries in themes.items():
            print(f"  🎯 {theme_key.upper()}")
            for query in queries:
                try:
                    results = self.analyzer.search(query, n_results=2)
                    for result in results:
                        self.results["phase4_themes"][theme_key].append({
                            "query": query,
                            "file": result['metadata']['file_path'],
                            "text": result['text'][:300]
                        })
                except Exception as e:
                    print(f"     ⚠️  Error in '{query}': {e}")

            count = len(self.results["phase4_themes"][theme_key])
            print(f"     ✅ {count} Dokumente")

    def _phase5(self):
        """Vergessenes"""
        queries = [
            "TODO implementieren Najika",
            "fehlt noch Najika",
            "muss noch Najika",
            "geplant aber Najika",
            "später hinzufügen"
        ]

        for query in queries:
            print(f"  🔍 {query[:40]}...")
            try:
                results = self.analyzer.search(query, n_results=3)
                for result in results:
                    self.results["phase5_missing"].append({
                        "query": query,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:500]
                    })
            except Exception as e:
                print(f"     ⚠️  Error: {e}")

        print(f"  ✅ {len(self.results['phase5_missing'])} Dokumente")

    def _export(self):
        """Export Report"""
        # JSON
        json_file = self.project_root / "NAJIKA_ANALYSIS_REPORT.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"  ✅ JSON: NAJIKA_ANALYSIS_REPORT.json")

        # Markdown (KURZ & ÜBERSICHTLICH)
        md_file = self.project_root / "NAJIKA_ANALYSIS_REPORT.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("# 🧠 NAJIKA ANALYSIS REPORT\n\n")
            f.write("Strukturierte Projekt-Analyse basierend auf existierender ChromaDB\n\n")
            f.write("="*70 + "\n\n")

            # Phase 1
            f.write("## 📋 PHASE 1: ZUSAMMENFASSUNGEN & ÜBERSICHTEN\n\n")
            seen_files = set()
            for item in self.results["phase1_overview"]:
                if item['file'] not in seen_files:
                    seen_files.add(item['file'])
                    f.write(f"### 📄 {item['file']}\n")
                    f.write(f"**Query:** {item['query']}\n\n")
                    f.write(f"```\n{item['text']}\n```\n\n")
                    f.write("-"*70 + "\n\n")

            # Phase 2
            f.write("## 🗺️ PHASE 2: ROADMAPS & TODOs\n\n")
            seen_files = set()
            for item in self.results["phase2_roadmaps"]:
                if item['file'] not in seen_files:
                    seen_files.add(item['file'])
                    f.write(f"### 📄 {item['file']}\n")
                    f.write(f"**Query:** {item['query']}\n\n")
                    f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 3
            f.write("## ✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN\n\n")
            seen_files = set()
            for item in self.results["phase3_complete"]:
                if item['file'] not in seen_files:
                    seen_files.add(item['file'])
                    f.write(f"### 📄 {item['file']}\n")
                    f.write(f"**Query:** {item['query']}\n\n")
                    f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 4
            f.write("## 🎯 PHASE 4: THEMEN-SPEZIFISCH\n\n")
            for theme_key, items in self.results["phase4_themes"].items():
                f.write(f"### {theme_key.upper().replace('_', ' ')}\n\n")
                seen_files = set()
                for item in items:
                    if item['file'] not in seen_files:
                        seen_files.add(item['file'])
                        f.write(f"#### 📄 {item['file']}\n")
                        f.write(f"**Query:** {item['query']}\n\n")
                        f.write(f"```\n{item['text']}\n```\n\n")
                f.write("\n")

            # Phase 5
            f.write("## 🔍 PHASE 5: VERGESSENE FEATURES & TODOs\n\n")
            seen_files = set()
            for item in self.results["phase5_missing"]:
                if item['file'] not in seen_files:
                    seen_files.add(item['file'])
                    f.write(f"### 📄 {item['file']}\n")
                    f.write(f"**Query:** {item['query']}\n\n")
                    f.write(f"```\n{item['text']}\n```\n\n")

        print(f"  ✅ Markdown: NAJIKA_ANALYSIS_REPORT.md")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA SEARCH-ONLY ANALYZER                                 ║
╚══════════════════════════════════════════════════════════════╝

Nutzt existierende ChromaDB (2.1 GB bereits indexiert)!
Führt NUR Searches durch - kein Re-Indexing nötig.

""")

    analyzer = NajikaSearchOnly()
    analyzer.run()

    print("\n" + "="*70)
    print("🎉 FERTIG!")
    print("="*70)
    print("\n📄 REPORTS erstellt:")
    print("   - NAJIKA_ANALYSIS_REPORT.md (Hauptdokument)")
    print("   - NAJIKA_ANALYSIS_REPORT.json (Rohdaten)")
    print("\n💡 Lies zuerst die .md Datei für die Zusammenfassung!")


if __name__ == "__main__":
    main()
