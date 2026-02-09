#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA SMART ANALYZER - Strukturierte Projekt-Analyse

STRATEGIE (wie vom User definiert):
1. Scan ALLES (gesamter Najika_World Ordner)
2. Suche ZUERST nach Zusammenfassungen/Übersichten/Roadmaps
3. Suche DANN nach Themen (Schwarze Mühle, Digivice, Handy, UEFN)
4. Finde VERGESSENES (was in Docs steht aber nicht im Code)
5. Falls nötig: Durchgehe REST

→ Strukturierter Report für Claude Code zum Analysieren
"""

import sys
import io
import json
from pathlib import Path
from typing import List, Dict
from najika_project_analyzer import NajikaProjectAnalyzer

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class NajikaSmartAnalyzer:
    """Strukturierte Multi-Phase Analyse"""

    def __init__(self, project_root: str = "C:\\Najika_World"):
        self.project_root = Path(project_root)

        # DREI QUELLEN (wie full_context_analyzer):
        self.sources = {
            "najika_world": self.project_root,
            "claude_worktrees": Path("C:\\Users\\0KKK0\\.claude-worktrees"),
            "claude_conversations": Path("C:\\Users\\0KKK0\\.claude")
        }

        # Analyzers für jede Quelle
        self.analyzers = {}

        # Phase Results
        self.results = {
            "phase1_overview": [],    # Zusammenfassungen/Übersichten
            "phase2_roadmaps": [],    # TODOs/Roadmaps/Pläne
            "phase3_complete": [],    # Vollständige Versionen
            "phase4_themes": {        # Themen-spezifisch
                "schwarze_muehle": [],
                "digivice": [],
                "handy_app": [],
                "uefn": [],
            },
            "phase5_missing": [],     # Vergessene Features
            "source_stats": {}        # Stats pro Quelle
        }

    def run_full_analysis(self) -> Dict:
        """
        Führt VOLLSTÄNDIGE strukturierte Analyse durch

        Returns:
            Dict mit allen Phase-Results
        """
        print("\n" + "="*70)
        print("🧠 NAJIKA SMART ANALYZER - STRUKTURIERTE PROJEKT-ANALYSE")
        print("="*70 + "\n")

        print("📊 DREI QUELLEN:")
        print(f"  1. Najika World:       {self.sources['najika_world']}")
        print(f"  2. Claude Worktrees:   {self.sources['claude_worktrees']}")
        print(f"  3. Claude Conversations: {self.sources['claude_conversations']}")
        print()

        # STEP 1: Index ALLE DREI QUELLEN
        print("="*70)
        print("📊 PHASE 0: VOLLSTÄNDIGES INDEXING (3 QUELLEN)")
        print("="*70 + "\n")

        # Source 1: Najika World
        print("📚 SOURCE 1: NAJIKA WORLD")
        print("-"*70)
        self.analyzers["najika_world"] = NajikaProjectAnalyzer(str(self.sources["najika_world"]))
        stats1 = self.analyzers["najika_world"].index_all_documents()
        self.results["source_stats"]["najika_world"] = stats1

        # Source 2: Claude Worktrees
        print("\n💼 SOURCE 2: CLAUDE CODE WORKTREES")
        print("-"*70)
        if self.sources["claude_worktrees"].exists():
            self.analyzers["claude_worktrees"] = NajikaProjectAnalyzer(str(self.sources["claude_worktrees"]))
            stats2 = self.analyzers["claude_worktrees"].index_all_documents()
            self.results["source_stats"]["claude_worktrees"] = stats2
        else:
            print("⚠️  Pfad existiert nicht - überspringe")
            self.results["source_stats"]["claude_worktrees"] = {"files_scanned": 0}

        # Source 3: Claude Conversations
        print("\n💬 SOURCE 3: CLAUDE CONVERSATIONS")
        print("-"*70)
        if self.sources["claude_conversations"].exists():
            self.analyzers["claude_conversations"] = NajikaProjectAnalyzer(str(self.sources["claude_conversations"]))
            stats3 = self.analyzers["claude_conversations"].index_all_documents()
            self.results["source_stats"]["claude_conversations"] = stats3
        else:
            print("⚠️  Pfad existiert nicht - überspringe")
            self.results["source_stats"]["claude_conversations"] = {"files_scanned": 0}

        print("\n" + "="*70)
        print("📊 INDEXING ABGESCHLOSSEN - ALLE QUELLEN")
        print("="*70)
        total_files = sum(stats.get("files_scanned", 0) for stats in self.results["source_stats"].values())
        total_chars = sum(stats.get("total_chars", 0) for stats in self.results["source_stats"].values())
        print(f"✅ Gesamt-Dateien: {total_files:,}")
        print(f"✅ Gesamt-Zeichen: {total_chars:,}")
        print()

        # STEP 2: Phase 1 - Übersichten
        print("\n📋 PHASE 1: ZUSAMMENFASSUNGEN & ÜBERSICHTEN")
        print("-"*70)
        self.phase1_find_overviews()

        # STEP 3: Phase 2 - Roadmaps
        print("\n🗺️  PHASE 2: ROADMAPS & TODOs")
        print("-"*70)
        self.phase2_find_roadmaps()

        # STEP 4: Phase 3 - Vollständige Versionen
        print("\n✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN")
        print("-"*70)
        self.phase3_find_complete()

        # STEP 5: Phase 4 - Themen
        print("\n🎯 PHASE 4: THEMEN-SPEZIFISCHE SUCHE")
        print("-"*70)
        self.phase4_find_themes()

        # STEP 6: Phase 5 - Vergessenes
        print("\n🔍 PHASE 5: VERGESSENE FEATURES")
        print("-"*70)
        self.phase5_find_missing()

        # STEP 7: Export Report
        print("\n💾 EXPORT REPORT")
        print("-"*70)
        self.export_report()

        return self.results

    def phase1_find_overviews(self):
        """Phase 1: Suche nach Zusammenfassungen & Übersichten (ALLE QUELLEN!)"""
        queries = [
            "Zusammenfassung Projekt",
            "Übersicht Features",
            "Project Summary",
            "Overview Complete",
            "NAJIKA ULTIMATIVE ZUSAMMENFASSUNG",
            "Master Overview"
        ]

        for query in queries:
            print(f"  🔍 Suche: {query}")

            # Suche in ALLEN Quellen!
            for source_name, analyzer in self.analyzers.items():
                results = analyzer.search(query, n_results=2)  # 2 per source

                for result in results:
                    self.results["phase1_overview"].append({
                        "query": query,
                        "source": source_name,  # Track source!
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:500],
                        "relevance": result.get('distance', 0)
                    })

        print(f"  ✅ {len(self.results['phase1_overview'])} Übersichten gefunden")

    def phase2_find_roadmaps(self):
        """Phase 2: Suche nach Roadmaps & TODOs"""
        queries = [
            "Roadmap",
            "TODO Liste",
            "Aufgaben",
            "Plan Implementation",
            "MEGA TODO",
            "NICHTS VERGESSEN",
            "Vollständige Aufgaben"
        ]

        for query in queries:
            print(f"  🔍 Suche: {query}")
            results = self.analyzers["najika_world"].search(query, n_results=3)

            for result in results:
                self.results["phase2_roadmaps"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500],
                    "relevance": result.get('distance', 0)
                })

        print(f"  ✅ {len(self.results['phase2_roadmaps'])} Roadmaps gefunden")

    def phase3_find_complete(self):
        """Phase 3: Suche nach vollständigen Versionen"""
        queries = [
            "Vollständig",
            "Complete Version",
            "Final Version",
            "Master Document",
            "Finale Version",
            "Alles zusammen"
        ]

        for query in queries:
            print(f"  🔍 Suche: {query}")
            results = self.analyzers["najika_world"].search(query, n_results=3)

            for result in results:
                self.results["phase3_complete"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500],
                    "relevance": result.get('distance', 0)
                })

        print(f"  ✅ {len(self.results['phase3_complete'])} Vollständige Versionen gefunden")

    def phase4_find_themes(self):
        """Phase 4: Themen-spezifische Suche"""

        themes = {
            "schwarze_muehle": [
                "Schwarze Mühle",
                "Schwarze Windmühle",
                "Gesichtern Bereich",
                "Digivice Integration Mühle"
            ],
            "digivice": [
                "Digivice",
                "najika_world_UNIFIED.html",
                "3D Scene Digivice",
                "Terminal Interface"
            ],
            "handy_app": [
                "Flutter App",
                "Handy Spiel",
                "Mobile App",
                "najika_digivice Flutter",
                "Android APK"
            ],
            "uefn": [
                "UEFN",
                "Unreal Editor",
                "Fortnite Creative",
                "Verse Code"
            ]
        }

        for theme_key, queries in themes.items():
            print(f"  🎯 Thema: {theme_key.upper()}")
            for query in queries:
                print(f"     🔍 {query}")
                results = self.analyzers["najika_world"].search(query, n_results=2)

                for result in results:
                    self.results["phase4_themes"][theme_key].append({
                        "query": query,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:300],
                        "relevance": result.get('distance', 0)
                    })

            count = len(self.results["phase4_themes"][theme_key])
            print(f"     ✅ {count} Dokumente gefunden")

    def phase5_find_missing(self):
        """Phase 5: Finde vergessene Features"""
        # Suche nach häufigen "geplant aber nicht implementiert" Phrasen
        queries = [
            "TODO implementieren",
            "noch nicht fertig",
            "fehlt noch",
            "muss noch",
            "geplant aber",
            "Phase 2 noch",
            "später hinzufügen"
        ]

        for query in queries:
            print(f"  🔍 Suche: {query}")
            results = self.analyzers["najika_world"].search(query, n_results=3)

            for result in results:
                self.results["phase5_missing"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500],
                    "relevance": result.get('distance', 0)
                })

        print(f"  ✅ {len(self.results['phase5_missing'])} Vergessene Features gefunden")

    def export_report(self):
        """Exportiert strukturierten Report für Claude Code"""

        output_file = self.project_root / "NAJIKA_SMART_ANALYSIS_REPORT.json"

        # Export als JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"  ✅ Report exportiert: {output_file}")

        # Erstelle auch Markdown-Version
        self.export_markdown_report()

    def export_markdown_report(self):
        """Erstellt lesbare Markdown-Version für Claude Code"""

        output_file = self.project_root / "NAJIKA_SMART_ANALYSIS_REPORT.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# 🧠 NAJIKA SMART ANALYSIS REPORT\n\n")
            f.write("Strukturierte Projekt-Analyse für Claude Code\n\n")
            f.write("="*70 + "\n\n")

            # Phase 1
            f.write("## 📋 PHASE 1: ZUSAMMENFASSUNGEN & ÜBERSICHTEN\n\n")
            for item in self.results["phase1_overview"][:10]:  # Top 10
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"**Query:** {item['query']}\n\n")
                f.write(f"```\n{item['text']}\n```\n\n")
                f.write("-"*70 + "\n\n")

            # Phase 2
            f.write("## 🗺️ PHASE 2: ROADMAPS & TODOs\n\n")
            for item in self.results["phase2_roadmaps"][:10]:
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"**Query:** {item['query']}\n\n")
                f.write(f"```\n{item['text']}\n```\n\n")
                f.write("-"*70 + "\n\n")

            # Phase 3
            f.write("## ✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN\n\n")
            for item in self.results["phase3_complete"][:10]:
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"**Query:** {item['query']}\n\n")
                f.write(f"```\n{item['text']}\n```\n\n")
                f.write("-"*70 + "\n\n")

            # Phase 4
            f.write("## 🎯 PHASE 4: THEMEN-SPEZIFISCH\n\n")
            for theme_key, items in self.results["phase4_themes"].items():
                f.write(f"### {theme_key.upper()}\n\n")
                for item in items[:5]:  # Top 5 per theme
                    f.write(f"#### 📄 {item['file']}\n")
                    f.write(f"**Query:** {item['query']}\n\n")
                    f.write(f"```\n{item['text']}\n```\n\n")
                f.write("-"*70 + "\n\n")

            # Phase 5
            f.write("## 🔍 PHASE 5: VERGESSENE FEATURES\n\n")
            for item in self.results["phase5_missing"][:15]:
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"**Query:** {item['query']}\n\n")
                f.write(f"```\n{item['text']}\n```\n\n")
                f.write("-"*70 + "\n\n")

        print(f"  ✅ Markdown Report: {output_file}")


# ===== CLI INTERFACE =====

def main():
    """CLI für Smart Analyzer"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA SMART ANALYZER - Strukturierte Projekt-Analyse      ║
╚══════════════════════════════════════════════════════════════╝

Dieser Analyzer führt eine VOLLSTÄNDIGE strukturierte Analyse durch:

PHASE 1: Zusammenfassungen & Übersichten
PHASE 2: Roadmaps & TODOs
PHASE 3: Vollständige Versionen
PHASE 4: Themen (Schwarze Mühle, Digivice, Handy, UEFN)
PHASE 5: Vergessene Features

DAUER: ~10-15 Minuten (abhängig von Dokument-Anzahl)

EXPORT:
- NAJIKA_SMART_ANALYSIS_REPORT.json
- NAJIKA_SMART_ANALYSIS_REPORT.md (für Claude Code)

""")

    # Auto-start (kein input() weil Background-Prozess)
    print("⏳ Starte automatisch...\n")

    analyzer = NajikaSmartAnalyzer()
    results = analyzer.run_full_analysis()

    print("\n" + "="*70)
    print("🎉 ANALYSE ABGESCHLOSSEN!")
    print("="*70)
    print("\nNÄCHSTE SCHRITTE:")
    print("1. Öffne: NAJIKA_SMART_ANALYSIS_REPORT.md")
    print("2. Lese die Top-Ergebnisse jeder Phase")
    print("3. Gib relevante Teile an Claude Code zum Analysieren")
    print("4. Claude erstellt Master-Übersicht basierend darauf")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
