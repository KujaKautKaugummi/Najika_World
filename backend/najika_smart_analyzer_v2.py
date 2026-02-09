#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA SMART ANALYZER V2 - Optimiert für große Datenmengen

VERBESSERUNGEN:
- Batch Processing (100 Files pro Batch)
- Progress Tracking
- Training Data OPTIONAL (zu groß für ersten Durchlauf)
- Fokus auf Najika-spezifische Dokumente
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


class NajikaSmartAnalyzerV2:
    """Strukturierte Multi-Phase Analyse (OPTIMIERT)"""

    def __init__(self, project_root: str = "C:\\Najika_World", include_training: bool = False):
        self.project_root = Path(project_root)
        self.include_training = include_training

        # DREI QUELLEN:
        self.sources = {
            "najika_world": self.project_root,
            "claude_worktrees": Path("C:\\Users\\0KKK0\\.claude-worktrees"),
            "claude_conversations": Path("C:\\Users\\0KKK0\\.claude")
        }

        # Analyzers
        self.analyzers = {}

        # Phase Results
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
            "phase5_missing": [],
            "source_stats": {}
        }

    def run_full_analysis(self) -> Dict:
        """Führt VOLLSTÄNDIGE strukturierte Analyse durch (OPTIMIERT)"""
        print("\n" + "="*70)
        print("🧠 NAJIKA SMART ANALYZER V2 - OPTIMIERT")
        print("="*70 + "\n")

        print("📊 DREI QUELLEN:")
        print(f"  1. Najika World:       {self.sources['najika_world']}")
        print(f"  2. Claude Worktrees:   {self.sources['claude_worktrees']}")
        print(f"  3. Claude Conversations: {self.sources['claude_conversations']}")
        print(f"\n⚙️  Training Data: {'INKLUDIERT' if self.include_training else 'EXKLUDIERT (zu groß)'}")
        print()

        # STEP 1: Index NUR NAJIKA-SPEZIFISCHE DOCS (ohne Training Data)
        print("="*70)
        print("📊 PHASE 0: FOKUSSIERTES INDEXING")
        print("="*70 + "\n")

        # Source 1: Najika World (SELECTIVE)
        print("📚 SOURCE 1: NAJIKA WORLD (Najika-spezifisch)")
        print("-"*70)
        self.analyzers["najika_world"] = self._index_najika_specific()

        # Source 2: Claude Worktrees (SELECTIVE)
        print("\n💼 SOURCE 2: CLAUDE CODE WORKTREES (Najika-Projekte)")
        print("-"*70)
        if self.sources["claude_worktrees"].exists():
            self.analyzers["claude_worktrees"] = self._index_claude_worktrees()
        else:
            print("⚠️  Pfad existiert nicht - überspringe")
            self.results["source_stats"]["claude_worktrees"] = {"files_scanned": 0}

        # Source 3: Claude Conversations (SELECTIVE - nur Najika)
        print("\n💬 SOURCE 3: CLAUDE CONVERSATIONS (Najika-Conversations)")
        print("-"*70)
        if self.sources["claude_conversations"].exists():
            self.analyzers["claude_conversations"] = self._index_claude_conversations()
        else:
            print("⚠️  Pfad existiert nicht - überspringe")
            self.results["source_stats"]["claude_conversations"] = {"files_scanned": 0}

        print("\n" + "="*70)
        print("📊 INDEXING ABGESCHLOSSEN")
        print("="*70)
        total_files = sum(stats.get("files_scanned", 0) for stats in self.results["source_stats"].values())
        total_chars = sum(stats.get("total_chars", 0) for stats in self.results["source_stats"].values())
        print(f"✅ Gesamt-Dateien: {total_files:,}")
        print(f"✅ Gesamt-Zeichen: {total_chars:,}")
        print()

        # STEP 2-6: Alle Phasen
        self._run_all_phases()

        # STEP 7: Export
        self.export_report()

        return self.results

    def _index_najika_specific(self) -> NajikaProjectAnalyzer:
        """Indiziert NUR Najika-spezifische Dokumente (ohne Training Data)"""
        analyzer = NajikaProjectAnalyzer(str(self.sources["najika_world"]))

        # Finde Najika-spezifische Files
        extensions = {".txt", ".md", ".pdf", ".py", ".json"}
        exclude_dirs = {
            "node_modules", "__pycache__", ".git", ".venv", "venv",
            "chroma_db", "chroma_project_db", ".dart_tool", "build"
        }

        # EXKLUDIERE Training Data wenn nicht gewünscht
        if not self.include_training:
            exclude_dirs.add("training_data_real")

        found_files = []
        for file in self.sources["najika_world"].rglob("*"):
            if any(excluded in file.parts for excluded in exclude_dirs):
                continue
            if file.is_file() and file.suffix in extensions:
                found_files.append(file)

        print(f"✅ {len(found_files)} Najika-Dateien gefunden")

        # Index in Batches
        batch_size = 100
        for i in range(0, len(found_files), batch_size):
            batch = found_files[i:i+batch_size]
            print(f"  📦 Batch {i//batch_size + 1}/{(len(found_files)-1)//batch_size + 1} ({len(batch)} Files)...", end=" ")

            for file in batch:
                try:
                    analyzer._index_single_document(file)
                except Exception as e:
                    print(f"\n  ⚠️  Error in {file.name}: {e}")
                    continue

            print("✅")

        self.results["source_stats"]["najika_world"] = {
            "files_scanned": len(found_files),
            "total_chars": analyzer.collection.count() * 1000  # Approximation
        }

        return analyzer

    def _index_claude_worktrees(self) -> NajikaProjectAnalyzer:
        """Indiziert Claude Code Worktrees (nur Najika-Projekte)"""
        analyzer = NajikaProjectAnalyzer(str(self.sources["claude_worktrees"]))

        # Finde nur Najika-bezogene Worktrees
        najika_dirs = []
        for path in self.sources["claude_worktrees"].iterdir():
            if path.is_dir():
                path_lower = str(path).lower()
                if "najika" in path_lower or "world" in path_lower:
                    najika_dirs.append(path)

        print(f"✅ {len(najika_dirs)} Najika-Worktrees gefunden")

        # Index MD/TXT files nur
        found_files = []
        for naj_dir in najika_dirs:
            for file in naj_dir.rglob("*"):
                if file.suffix in {".md", ".txt"}:
                    found_files.append(file)

        print(f"  📄 {len(found_files)} Dokumente in Worktrees")

        # Index
        for i, file in enumerate(found_files, 1):
            if i % 50 == 0:
                print(f"  Progress: {i}/{len(found_files)}")
            try:
                analyzer._index_single_document(file)
            except Exception:
                continue

        self.results["source_stats"]["claude_worktrees"] = {
            "files_scanned": len(found_files)
        }

        return analyzer

    def _index_claude_conversations(self) -> NajikaProjectAnalyzer:
        """Indiziert Claude Conversations (nur Najika-bezogen)"""
        analyzer = NajikaProjectAnalyzer(str(self.sources["claude_conversations"]))

        # Finde conversation files
        found_files = []
        for file in self.sources["claude_conversations"].rglob("*.jsonl"):
            # Check if Najika-related by reading first few lines
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    first_lines = f.read(5000).lower()
                    if "najika" in first_lines or "world" in first_lines:
                        found_files.append(file)
            except Exception:
                continue

        print(f"✅ {len(found_files)} Najika-Conversations gefunden")

        # Index
        for i, file in enumerate(found_files, 1):
            print(f"  Progress: {i}/{len(found_files)}")
            try:
                analyzer._index_single_document(file)
            except Exception:
                continue

        self.results["source_stats"]["claude_conversations"] = {
            "files_scanned": len(found_files)
        }

        return analyzer

    def _run_all_phases(self):
        """Führt alle 5 Phasen durch"""
        print("\n📋 PHASE 1: ZUSAMMENFASSUNGEN & ÜBERSICHTEN")
        print("-"*70)
        self.phase1_find_overviews()

        print("\n🗺️  PHASE 2: ROADMAPS & TODOs")
        print("-"*70)
        self.phase2_find_roadmaps()

        print("\n✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN")
        print("-"*70)
        self.phase3_find_complete()

        print("\n🎯 PHASE 4: THEMEN-SPEZIFISCHE SUCHE")
        print("-"*70)
        self.phase4_find_themes()

        print("\n🔍 PHASE 5: VERGESSENE FEATURES")
        print("-"*70)
        self.phase5_find_missing()

    def phase1_find_overviews(self):
        """Phase 1: Zusammenfassungen (ALLE QUELLEN)"""
        queries = [
            "Zusammenfassung Projekt",
            "Übersicht Features",
            "NAJIKA ULTIMATIVE ZUSAMMENFASSUNG",
            "Master Overview",
            "Complete Project Overview"
        ]

        for query in queries:
            print(f"  🔍 Suche: {query}")
            for source_name, analyzer in self.analyzers.items():
                results = analyzer.search(query, n_results=2)
                for result in results:
                    self.results["phase1_overview"].append({
                        "query": query,
                        "source": source_name,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:500]
                    })

        print(f"  ✅ {len(self.results['phase1_overview'])} Übersichten gefunden")

    def phase2_find_roadmaps(self):
        """Phase 2: Roadmaps"""
        queries = ["Roadmap", "TODO Liste", "MEGA TODO", "NICHTS VERGESSEN"]
        for query in queries:
            print(f"  🔍 Suche: {query}")
            results = self.analyzers["najika_world"].search(query, n_results=3)
            for result in results:
                self.results["phase2_roadmaps"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500]
                })
        print(f"  ✅ {len(self.results['phase2_roadmaps'])} Roadmaps gefunden")

    def phase3_find_complete(self):
        """Phase 3: Vollständige Versionen"""
        queries = ["Vollständig", "Complete Version", "Final Version", "Finale Version"]
        for query in queries:
            print(f"  🔍 Suche: {query}")
            results = self.analyzers["najika_world"].search(query, n_results=3)
            for result in results:
                self.results["phase3_complete"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500]
                })
        print(f"  ✅ {len(self.results['phase3_complete'])} Versionen gefunden")

    def phase4_find_themes(self):
        """Phase 4: Themen"""
        themes = {
            "schwarze_muehle": ["Schwarze Mühle", "Gesichtern Bereich"],
            "digivice": ["Digivice", "najika_world_UNIFIED.html", "3D Scene"],
            "handy_app": ["Flutter App", "Handy Spiel", "Mobile App"],
            "uefn": ["UEFN", "Fortnite Creative", "Verse Code"]
        }

        for theme_key, queries in themes.items():
            print(f"  🎯 Thema: {theme_key.upper()}")
            for query in queries:
                results = self.analyzers["najika_world"].search(query, n_results=2)
                for result in results:
                    self.results["phase4_themes"][theme_key].append({
                        "query": query,
                        "file": result['metadata']['file_path'],
                        "text": result['text'][:300]
                    })

    def phase5_find_missing(self):
        """Phase 5: Vergessenes"""
        queries = ["TODO implementieren", "fehlt noch", "muss noch", "geplant aber"]
        for query in queries:
            print(f"  🔍 Suche: {query}")
            results = self.analyzers["najika_world"].search(query, n_results=3)
            for result in results:
                self.results["phase5_missing"].append({
                    "query": query,
                    "file": result['metadata']['file_path'],
                    "text": result['text'][:500]
                })
        print(f"  ✅ {len(self.results['phase5_missing'])} Features gefunden")

    def export_report(self):
        """Exportiert Report"""
        output_file = self.project_root / "NAJIKA_SMART_ANALYSIS_REPORT_V2.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n  ✅ Report: {output_file}")

        self.export_markdown_report()

    def export_markdown_report(self):
        """Markdown Report"""
        output_file = self.project_root / "NAJIKA_SMART_ANALYSIS_REPORT_V2.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# 🧠 NAJIKA SMART ANALYSIS REPORT V2\n\n")
            f.write("Strukturierte Projekt-Analyse (OPTIMIERT)\n\n")
            f.write("="*70 + "\n\n")

            # Phase 1
            f.write("## 📋 PHASE 1: ZUSAMMENFASSUNGEN & ÜBERSICHTEN\n\n")
            for item in self.results["phase1_overview"][:15]:
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"**Query:** {item['query']} | **Source:** {item['source']}\n\n")
                f.write(f"```\n{item['text']}\n```\n\n")
                f.write("-"*70 + "\n\n")

            # Phase 2
            f.write("## 🗺️ PHASE 2: ROADMAPS & TODOs\n\n")
            for item in self.results["phase2_roadmaps"][:10]:
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"**Query:** {item['query']}\n\n")
                f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 3
            f.write("## ✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN\n\n")
            for item in self.results["phase3_complete"][:10]:
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 4
            f.write("## 🎯 PHASE 4: THEMEN-SPEZIFISCH\n\n")
            for theme_key, items in self.results["phase4_themes"].items():
                f.write(f"### {theme_key.upper()}\n\n")
                for item in items[:5]:
                    f.write(f"#### {item['file']}\n")
                    f.write(f"```\n{item['text']}\n```\n\n")

            # Phase 5
            f.write("## 🔍 PHASE 5: VERGESSENE FEATURES\n\n")
            for item in self.results["phase5_missing"][:15]:
                f.write(f"### 📄 {item['file']}\n")
                f.write(f"```\n{item['text']}\n```\n\n")

        print(f"  ✅ Markdown Report: {output_file}")


def main():
    """CLI"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA SMART ANALYZER V2 - OPTIMIERT                       ║
╚══════════════════════════════════════════════════════════════╝

VERBESSERUNGEN:
- Fokus auf Najika-spezifische Dokumente
- Training Data OPTIONAL (Standard: AUS)
- Batch Processing (stabiler)

EXPORT:
- NAJIKA_SMART_ANALYSIS_REPORT_V2.json
- NAJIKA_SMART_ANALYSIS_REPORT_V2.md

""")

    print("⏳ Starte automatisch (ohne Training Data)...\n")

    analyzer = NajikaSmartAnalyzerV2(include_training=False)
    results = analyzer.run_full_analysis()

    print("\n" + "="*70)
    print("🎉 ANALYSE ABGESCHLOSSEN!")
    print("="*70)
    print("\nREPORTS:")
    print("- NAJIKA_SMART_ANALYSIS_REPORT_V2.md")
    print("- NAJIKA_SMART_ANALYSIS_REPORT_V2.json")


if __name__ == "__main__":
    main()
