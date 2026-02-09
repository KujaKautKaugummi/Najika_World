#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA GREP ANALYZER - Reine Text-Suche ohne ChromaDB

Nutzt einfaches Grep/Text-Search statt Vector DB
Schnell, stabil, keine Dependencies
"""

import sys
import io
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple


# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class NajikaGrepAnalyzer:
    """Einfache Text-basierte Suche"""

    def __init__(self):
        self.project_root = Path("C:\\Najika_World")
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

    def find_najika_files(self) -> List[Path]:
        """Findet alle Najika-Dokumente (ohne Training Data)"""
        print("📂 Sammle Najika-Dokumente...")

        extensions = {".txt", ".md"}  # Nur Text-Files
        exclude_dirs = {
            "node_modules", "__pycache__", ".git", ".venv", "venv",
            "chroma_db", "chroma_project_db", ".dart_tool", "build",
            "training_data_real"  # Exkludiert!
        }

        files = []
        for file in self.project_root.rglob("*"):
            if any(excluded in file.parts for excluded in exclude_dirs):
                continue
            if file.is_file() and file.suffix in extensions:
                files.append(file)

        print(f"✅ {len(files)} Dokumente gefunden\n")
        return files

    def search_in_file(self, file_path: Path, keywords: List[str], case_insensitive: bool = True) -> List[Tuple[str, int]]:
        """
        Sucht Keywords in Datei

        Returns:
            Liste von (context_text, line_number) tuples
        """
        matches = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                line_to_search = line.lower() if case_insensitive else line

                for keyword in keywords:
                    keyword_search = keyword.lower() if case_insensitive else keyword

                    if keyword_search in line_to_search:
                        # Kontext: 2 Zeilen vor + match + 2 Zeilen nach
                        start = max(0, line_num - 3)
                        end = min(len(lines), line_num + 2)
                        context = "".join(lines[start:end])

                        matches.append((context, line_num))
                        break  # Nur eine Match pro Zeile

        except Exception as e:
            pass  # Skip errors

        return matches

    def run(self) -> Dict:
        """Führt Analyse durch"""
        print("="*70)
        print("🔍 NAJIKA GREP ANALYZER - Text-basierte Suche")
        print("="*70 + "\n")

        # Finde Files
        files = self.find_najika_files()

        # Phase 1: Zusammenfassungen
        print("📋 PHASE 1: ZUSAMMENFASSUNGEN")
        print("-"*70)
        keywords = ["zusammenfassung", "übersicht", "ultimative", "master", "overview", "complete"]
        self._search_phase(files, keywords, self.results["phase1_overview"])

        # Phase 2: Roadmaps
        print("\n🗺️  PHASE 2: ROADMAPS & TODOs")
        print("-"*70)
        keywords = ["roadmap", "todo", "aufgaben", "mega todo", "nichts vergessen"]
        self._search_phase(files, keywords, self.results["phase2_roadmaps"])

        # Phase 3: Vollständig
        print("\n✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN")
        print("-"*70)
        keywords = ["vollständig", "complete", "final", "finale version"]
        self._search_phase(files, keywords, self.results["phase3_complete"])

        # Phase 4: Themen
        print("\n🎯 PHASE 4: THEMEN")
        print("-"*70)

        themes = {
            "schwarze_muehle": ["schwarze mühle", "windmühle", "gesichtern"],
            "digivice": ["digivice", "najika_world_unified", "3d scene", "terminal"],
            "handy_app": ["flutter", "handy", "mobile app", "apk", "android"],
            "uefn": ["uefn", "fortnite", "verse", "unreal editor"]
        }

        for theme_key, keywords in themes.items():
            print(f"  🎯 {theme_key.upper()}")
            self._search_phase(files, keywords, self.results["phase4_themes"][theme_key], verbose=False)
            count = len(self.results["phase4_themes"][theme_key])
            print(f"     ✅ {count} Dokumente")

        # Phase 5: Vergessenes
        print("\n🔍 PHASE 5: VERGESSENE FEATURES")
        print("-"*70)
        keywords = ["todo implementieren", "fehlt noch", "muss noch", "geplant aber", "später"]
        self._search_phase(files, keywords, self.results["phase5_missing"])

        # Export
        print("\n💾 EXPORT")
        print("-"*70)
        self._export()

        return self.results

    def _search_phase(self, files: List[Path], keywords: List[str], results_list: List[Dict], verbose: bool = True):
        """Führt Suche für eine Phase durch"""
        found_files = set()

        for file in files:
            matches = self.search_in_file(file, keywords)

            if matches:
                found_files.add(file)

                # Nimm ersten Match
                context, line_num = matches[0]

                results_list.append({
                    "file": str(file.relative_to(self.project_root)),
                    "line": line_num,
                    "context": context[:500],  # Erste 500 chars
                    "matched_keywords": [kw for kw in keywords if kw in context.lower()]
                })

        if verbose:
            print(f"  ✅ {len(found_files)} Dokumente gefunden")

    def _export(self):
        """Export Report"""
        # JSON
        json_file = self.project_root / "NAJIKA_GREP_REPORT.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"  ✅ JSON: NAJIKA_GREP_REPORT.json")

        # Markdown
        md_file = self.project_root / "NAJIKA_GREP_REPORT.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("# 🧠 NAJIKA GREP REPORT\n\n")
            f.write("Strukturierte Projekt-Analyse via Text-Search\n\n")
            f.write("="*70 + "\n\n")

            # Phase 1
            f.write("## 📋 PHASE 1: ZUSAMMENFASSUNGEN & ÜBERSICHTEN\n\n")
            for item in self.results["phase1_overview"][:20]:
                f.write(f"### 📄 {item['file']} (Line {item['line']})\n")
                f.write(f"**Keywords:** {', '.join(item['matched_keywords'])}\n\n")
                f.write(f"```\n{item['context']}\n```\n\n")
                f.write("-"*70 + "\n\n")

            # Phase 2
            f.write("## 🗺️ PHASE 2: ROADMAPS & TODOs\n\n")
            for item in self.results["phase2_roadmaps"][:15]:
                f.write(f"### 📄 {item['file']} (Line {item['line']})\n")
                f.write(f"```\n{item['context']}\n```\n\n")

            # Phase 3
            f.write("## ✅ PHASE 3: VOLLSTÄNDIGE VERSIONEN\n\n")
            for item in self.results["phase3_complete"][:15]:
                f.write(f"### 📄 {item['file']} (Line {item['line']})\n")
                f.write(f"```\n{item['context']}\n```\n\n")

            # Phase 4
            f.write("## 🎯 PHASE 4: THEMEN-SPEZIFISCH\n\n")
            for theme_key, items in self.results["phase4_themes"].items():
                f.write(f"### {theme_key.upper().replace('_', ' ')}\n\n")
                for item in items[:10]:
                    f.write(f"#### 📄 {item['file']} (Line {item['line']})\n")
                    f.write(f"```\n{item['context']}\n```\n\n")
                f.write("\n")

            # Phase 5
            f.write("## 🔍 PHASE 5: VERGESSENE FEATURES & TODOs\n\n")
            for item in self.results["phase5_missing"][:20]:
                f.write(f"### 📄 {item['file']} (Line {item['line']})\n")
                f.write(f"```\n{item['context']}\n```\n\n")

        print(f"  ✅ Markdown: NAJIKA_GREP_REPORT.md")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA GREP ANALYZER - Text-basierte Suche                 ║
╚══════════════════════════════════════════════════════════════╝

Einfache, stabile Text-Suche ohne ChromaDB.
Scannt ~1500 Najika-Dokumente (.md/.txt files).

""")

    analyzer = NajikaGrepAnalyzer()
    analyzer.run()

    print("\n" + "="*70)
    print("🎉 FERTIG!")
    print("="*70)
    print("\n📄 REPORTS erstellt:")
    print("   - NAJIKA_GREP_REPORT.md (Hauptdokument)")
    print("   - NAJIKA_GREP_REPORT.json (Rohdaten)")
    print("\n💡 Lies die .md Datei für die strukturierte Übersicht!")


if __name__ == "__main__":
    main()
