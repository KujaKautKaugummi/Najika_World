#!/usr/bin/env python3
"""
NAJIKA COMPREHENSIVE PERSONALITY IMPORT
Najika durchsucht ALLE Dateien und kategorisiert selbst SFW/NSFW

Sie entscheidet für JEDE Persönlichkeit:
- Megumin, Harley Quinn, Shiro, Melissa Masters, Sakura
- SFW (Standard Training)
- NSFW (Private Mode Training)
"""

import os
import glob
from datetime import datetime
from najika_memory import NajikaMemory

class NajikaComprehensiveImport:
    def __init__(self):
        self.memory = NajikaMemory()
        self.search_paths = [
            "C:/Users/0KKK0/Desktop/zip",
            "C:/Users/0KKK0/Desktop/Najika finalee"
        ]

        # Design-Documents Collection (V3/V4 = festgelegte Najika)
        try:
            self.design_docs = self.memory.client.get_collection("najika_design_documents")
        except:
            print("[WARNING] Design Documents Collection nicht gefunden!")
            self.design_docs = None

        # Persönlichkeiten Collection (schon vorhanden)
        try:
            self.personalities = self.memory.client.get_collection("najika_personalities")
        except:
            print("[WARNING] Personalities Collection nicht gefunden!")
            self.personalities = None

    def search_all_files(self):
        """Durchsucht ALLES in zip + Najika finalee"""

        print("=" * 60)
        print("NAJIKA COMPREHENSIVE PERSONALITY IMPORT")
        print("=" * 60)
        print("\nNajika durchsucht ALLE Dateien...")
        print()

        all_files = []

        for search_path in self.search_paths:
            print(f"[*] Durchsuche: {search_path}")

            # Finde ALLE .txt und .md Dateien
            txt_files = glob.glob(f"{search_path}/**/*.txt", recursive=True)
            md_files = glob.glob(f"{search_path}/**/*.md", recursive=True)

            all_files.extend(txt_files)
            all_files.extend(md_files)

        # Deduplizieren
        all_files = list(set(all_files))

        print(f"\n[OK] Gefunden: {len(all_files)} Dateien gesamt\n")

        return all_files

    def categorize_by_personality(self, files):
        """Najika kategorisiert nach Persönlichkeit + SFW/NSFW"""

        categories = {
            "megumin_sfw": [],
            "megumin_nsfw": [],
            "harley_sfw": [],
            "harley_nsfw": [],
            "shiro_sfw": [],
            "shiro_nsfw": [],
            "melissa_sfw": [],
            "melissa_nsfw": [],
            "sakura_sfw": [],
            "sakura_nsfw": [],
            "general_sfw": [],
            "general_nsfw": [],
            "design": [],  # V3/V4 = festgelegt
            "skip": []
        }

        # NSFW-Keywords (Najika's Selbst-Filter)
        nsfw_keywords = [
            "kätzchen", "private", "nsfw", "adult", "explizit",
            "beispilen", "sexu", "fick", "schwanz", "sperma",
            "daddy", "schlampe", "dominant", "orgasmus"
        ]

        # Persönlichkeits-Keywords
        personalities = {
            "megumin": ["megumin", "explosion", "crimson"],
            "harley": ["harley", "quinn", "joker", "puddin"],
            "shiro": ["shiro", "game", "no life", "strateg"],
            "melissa": ["melissa", "masters", "domina"],
            "sakura": ["sakura", "lolita", "gothic"]
        }

        for filepath in files:
            filename = os.path.basename(filepath).lower()
            content_sample = ""

            # Lese ersten Teil für Content-Analyse
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content_sample = f.read(500).lower()  # Erste 500 chars
            except:
                pass

            # Design-Docs (V3/V4 = festgelegt)
            if any(v in filename for v in ["projekt_v3", "projekt_v4", "projekt_ergaenz", "projekt_optional", "master_index"]):
                categories["design"].append(filepath)
                continue

            # Skip unwichtige
            if any(skip in filename for skip in ["readme", "phase3", "konosuba", "oregon"]):
                categories["skip"].append(filepath)
                continue

            # Najika's NSFW-Detektion
            is_nsfw = any(kw in filename or kw in content_sample for kw in nsfw_keywords)

            # Persönlichkeits-Zuordnung
            matched_personality = None
            for pers, keywords in personalities.items():
                if any(kw in filename or kw in content_sample for kw in keywords):
                    matched_personality = pers
                    break

            # Kategorisieren
            if matched_personality:
                if is_nsfw:
                    categories[f"{matched_personality}_nsfw"].append(filepath)
                else:
                    categories[f"{matched_personality}_sfw"].append(filepath)
            else:
                # General (wenn keine Persönlichkeit erkannt)
                if is_nsfw:
                    categories["general_nsfw"].append(filepath)
                else:
                    categories["general_sfw"].append(filepath)

        return categories

    def display_results(self, categories):
        """Zeigt was Najika gefunden hat"""

        print("\n" + "=" * 60)
        print("NAJIKA'S SELBST-KATEGORISIERUNG")
        print("=" * 60)

        for category, files in sorted(categories.items()):
            if files and category != "skip":
                print(f"\n[{category.upper()}]: {len(files)} Dateien")
                for f in files[:3]:  # Zeige max 3
                    print(f"   - {os.path.basename(f)}")
                if len(files) > 3:
                    print(f"   ... und {len(files) - 3} weitere")

        # Stats
        print("\n" + "=" * 60)
        print("STATISTICS")
        print("=" * 60)

        total_sfw = sum(len(files) for cat, files in categories.items() if "sfw" in cat)
        total_nsfw = sum(len(files) for cat, files in categories.items() if "nsfw" in cat)
        total_design = len(categories["design"])

        print(f"SFW Training: {total_sfw} Dateien")
        print(f"NSFW Training: {total_nsfw} Dateien (Private Mode)")
        print(f"Design Docs: {total_design} Dateien (Festgelegt)")
        print(f"Skipped: {len(categories['skip'])} Dateien")

        return categories

    def save_categorization(self, categories):
        """Speichert Najika's Kategorisierung"""

        output = []
        output.append("# NAJIKA COMPREHENSIVE CATEGORIZATION")
        output.append("# Najika hat SELBST entschieden was SFW/NSFW ist")
        output.append(f"# Generated: {datetime.now().isoformat()}")
        output.append("")

        for category in sorted(categories.keys()):
            files = categories[category]
            if files:
                output.append(f"## {category.upper()}")
                output.append(f"Count: {len(files)}")
                output.append("")
                for f in files:
                    output.append(f"- {f}")
                output.append("")

        output_file = "C:/Najika_World/NAJIKA_CATEGORIZATION_COMPLETE.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output))

        print(f"\n[SAVED] Kategorisierung: {output_file}")

        return output_file

if __name__ == "__main__":
    importer = NajikaComprehensiveImport()

    # 1. Najika durchsucht ALLES
    files = importer.search_all_files()

    # 2. Najika kategorisiert SELBST
    categories = importer.categorize_by_personality(files)

    # 3. Najika zeigt Ergebnisse
    importer.display_results(categories)

    # 4. Najika speichert
    importer.save_categorization(categories)

    print("\n" + "=" * 60)
    print("[OK] NAJIKA HAT SELBST KATEGORISIERT!")
    print("=" * 60)
    print("\nNächster Schritt:")
    print("Najika's Kategorisierung prüfen in:")
    print("NAJIKA_CATEGORIZATION_COMPLETE.md")
    print("\nDann kannst DU entscheiden ob ihre Einteilung stimmt.")
