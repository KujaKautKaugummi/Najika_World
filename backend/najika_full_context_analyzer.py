#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA FULL CONTEXT ANALYZER
Scannt ALLES: Najika_World + Claude Code Workspaces + Conversations

DREI QUELLEN:
1. C:\Najika_World (Haupt-Projekt)
2. C:\Users\0KKK0\.claude-worktrees (Claude Code Projekte)
3. C:\Users\0KKK0\.claude (Claude Conversations)

→ Komplettes Projekt-Wissen + Alle Entwicklungs-Konversationen!
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


class NajikaFullContextAnalyzer:
    """Analysiert ALLES: Projekt + Claude Code History"""

    def __init__(self):
        self.sources = {
            "najika_world": Path("C:\\Najika_World"),
            "claude_worktrees": Path("C:\\Users\\0KKK0\\.claude-worktrees"),
            "claude_conversations": Path("C:\\Users\\0KKK0\\.claude")
        }

        # Separate Analyzers für jede Quelle
        self.analyzers = {}

    def run_full_scan(self):
        """Scannt ALLE drei Quellen"""

        print("\n" + "="*70)
        print("🧠 NAJIKA FULL CONTEXT ANALYZER")
        print("="*70 + "\n")

        print("📊 DREI QUELLEN:")
        print(f"  1. Najika_World:       {self.sources['najika_world']}")
        print(f"  2. Claude Worktrees:   {self.sources['claude_worktrees']}")
        print(f"  3. Claude Conversations: {self.sources['claude_conversations']}")
        print()

        # ===== SOURCE 1: NAJIKA WORLD =====
        print("="*70)
        print("📚 SOURCE 1: NAJIKA WORLD")
        print("="*70)

        self.analyzers["najika_world"] = NajikaProjectAnalyzer(
            project_root=str(self.sources["najika_world"])
        )
        stats1 = self.analyzers["najika_world"].index_all_documents()

        # ===== SOURCE 2: CLAUDE WORKTREES =====
        print("\n" + "="*70)
        print("💼 SOURCE 2: CLAUDE CODE WORKTREES")
        print("="*70)

        if self.sources["claude_worktrees"].exists():
            self.analyzers["claude_worktrees"] = NajikaProjectAnalyzer(
                project_root=str(self.sources["claude_worktrees"])
            )
            stats2 = self.analyzers["claude_worktrees"].index_all_documents()
        else:
            print("⚠️  Pfad existiert nicht - überspringe")
            stats2 = {"files_scanned": 0, "total_chars": 0}

        # ===== SOURCE 3: CLAUDE CONVERSATIONS =====
        print("\n" + "="*70)
        print("💬 SOURCE 3: CLAUDE CONVERSATIONS")
        print("="*70)

        if self.sources["claude_conversations"].exists():
            # Claude Conversations sind oft JSON/binär - nur Text-Files
            self.analyzers["claude_conversations"] = NajikaProjectAnalyzer(
                project_root=str(self.sources["claude_conversations"])
            )
            stats3 = self.analyzers["claude_conversations"].index_all_documents()
        else:
            print("⚠️  Pfad existiert nicht - überspringe")
            stats3 = {"files_scanned": 0, "total_chars": 0}

        # ===== GESAMT-STATISTIK =====
        print("\n" + "="*70)
        print("📊 GESAMT-STATISTIK")
        print("="*70)

        total_files = stats1.get("files_scanned", 0) + stats2.get("files_scanned", 0) + stats3.get("files_scanned", 0)
        total_chars = stats1.get("total_chars", 0) + stats2.get("total_chars", 0) + stats3.get("total_chars", 0)

        print(f"✅ Gesamt-Dateien:  {total_files:,}")
        print(f"✅ Gesamt-Zeichen:  {total_chars:,}")
        print(f"✅ In MB:           {total_chars / 1_000_000:.2f} MB")

        print("\n🔍 JETZT DURCHSUCHBAR:")
        print("  - Najika World Projekt")
        print("  - Claude Code Worktrees (alle Projekt-Versionen)")
        print("  - Claude Conversations (alle Chat-Verläufe)")

        print("\n" + "="*70 + "\n")

        return {
            "najika_world": stats1,
            "claude_worktrees": stats2,
            "claude_conversations": stats3,
            "total_files": total_files,
            "total_chars": total_chars
        }

    def search_all(self, query: str, n_results: int = 10):
        """Sucht in ALLEN drei Quellen"""

        print(f"\n🔍 SUCHE: {query}")
        print("="*70)

        all_results = []

        for source_name, analyzer in self.analyzers.items():
            print(f"\n📂 {source_name.upper()}:")
            results = analyzer.search(query, n_results=n_results)

            for r in results:
                r['source'] = source_name  # Tag source
                all_results.append(r)

            print(f"   ✅ {len(results)} Ergebnisse")

        # Sortiere nach Relevanz (kleinste Distance = beste)
        all_results.sort(key=lambda x: x.get('distance', 999))

        print(f"\n📊 GESAMT: {len(all_results)} Ergebnisse gefunden")
        print("="*70)

        return all_results[:n_results]  # Top N

    def export_unified_index(self):
        """Exportiert vereinigten Index"""

        output = {
            "sources": {
                "najika_world": str(self.sources["najika_world"]),
                "claude_worktrees": str(self.sources["claude_worktrees"]),
                "claude_conversations": str(self.sources["claude_conversations"])
            },
            "analyzers_available": list(self.analyzers.keys())
        }

        output_file = Path("C:\\Najika_World\\UNIFIED_INDEX_INFO.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

        print(f"💾 Unified Index Info: {output_file}")


def main():
    """CLI für Full Context Analyzer"""

    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA FULL CONTEXT ANALYZER                               ║
║  Scannt ALLES: Projekt + Claude Code History                ║
╚══════════════════════════════════════════════════════════════╝

DREI QUELLEN:
1. Najika_World (Haupt-Projekt)
2. Claude Worktrees (alle Projekt-Versionen)
3. Claude Conversations (alle Chat-Verläufe)

DAUER: ~15-20 Minuten (viele Quellen!)

DANACH:
- Komplettes Projekt-Wissen durchsuchbar
- Alle Entwicklungs-Konversationen durchsuchbar
- Semantic Search über ALLES

""")

    print("⏳ Starte Full Scan...\n")

    analyzer = NajikaFullContextAnalyzer()
    stats = analyzer.run_full_scan()

    analyzer.export_unified_index()

    print("\n" + "="*70)
    print("🎉 FULL CONTEXT SCAN ABGESCHLOSSEN!")
    print("="*70)
    print("\nJETZT VERFÜGBAR:")
    print("  - Semantic Search über ALLES")
    print("  - Projekt + Alle Claude Code Verläufe")
    print("  - Komplettes Kontext-Wissen")
    print("\nNÄCHSTE SCHRITTE:")
    print("  1. Nutze najika_smart_analyzer.py für strukturierte Analyse")
    print("  2. Oder: python -c \"from najika_full_context_analyzer import *; ...\"")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
