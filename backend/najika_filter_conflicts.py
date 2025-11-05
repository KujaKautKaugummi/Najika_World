#!/usr/bin/env python3
"""
NAJIKA CONFLICT FILTER
Filtert NUR widersprüchliche alte Versionen
Behält valide Dateien auch wenn "fast final"
"""

import os

class NajikaConflictFilter:
    def __init__(self, categorization_file):
        self.categorization_file = categorization_file
        self.conflicts = []
        self.valid = []

    def load_categorization(self):
        """Lädt Najika's Kategorisierung"""

        categories = {
            "design": [],
            "general_nsfw": [],
            "general_sfw": [],
            "megumin_nsfw": [],
            "megumin_sfw": [],
            "harley_nsfw": [],
            "harley_sfw": [],
            "shiro_nsfw": [],
            "shiro_sfw": [],
            "melissa_nsfw": [],
            "melissa_sfw": [],
            "sakura_nsfw": [],
            "sakura_sfw": [],
            "skip": []
        }

        current_cat = None
        with open(self.categorization_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Kategorie erkennen
                if line.startswith("## "):
                    cat_name = line[3:].lower()
                    current_cat = cat_name

                # Dateipfad
                elif line.startswith("- C:/"):
                    filepath = line[2:]
                    if current_cat and current_cat in categories:
                        categories[current_cat].append(filepath)

        return categories

    def identify_conflicts(self, categories):
        """Identifiziert WIRKLICH widersprüchliche Dateien"""

        conflicts = []
        valid = []

        # REGEL 1: Ordner "grund idee ki nicht perfekt" = explizit ALT
        conflict_paths = [
            "grund idee ki nicht perfekt"
        ]

        # REGEL 2: V2 wenn V3 existiert = veraltet
        # Aber NUR wenn V3 existiert!
        has_v3 = False
        has_v2 = False

        for cat, files in categories.items():
            for filepath in files:
                filename = os.path.basename(filepath).lower()

                if "v3" in filename:
                    has_v3 = True
                if "v2" in filename and "v2.5" not in filename:
                    has_v2 = True

        # REGEL 3: Entwurfs-Keywords (wirklich unsicher)
        draft_keywords = [
            "fast ist es so weit gelich",  # Klingt nach Entwurf
            "ich denke fast",  # Unsicher
            "noch bearbeiten",  # Nicht fertig
        ]

        # Filtere jede Datei
        for cat, files in categories.items():
            for filepath in files:
                filename = os.path.basename(filepath).lower()
                is_conflict = False

                # Check Regel 1: Ordner
                for conflict_path in conflict_paths:
                    if conflict_path in filepath:
                        conflicts.append({
                            'file': filepath,
                            'reason': f'Ordner: "{conflict_path}" (explizit nicht perfekt)'
                        })
                        is_conflict = True
                        break

                if is_conflict:
                    continue

                # Check Regel 2: V2 vs V3
                if has_v3 and "v2" in filename and "v2.5" not in filename:
                    # V2 ist veraltet wenn V3 existiert
                    conflicts.append({
                        'file': filepath,
                        'reason': 'V2 vorhanden aber V3 existiert (veraltet)'
                    })
                    is_conflict = True
                    continue

                # Check Regel 3: Entwurfs-Keywords
                for keyword in draft_keywords:
                    if keyword in filename:
                        conflicts.append({
                            'file': filepath,
                            'reason': f'Entwurf-Keyword: "{keyword}"'
                        })
                        is_conflict = True
                        break

                if not is_conflict:
                    valid.append(filepath)

        return conflicts, valid

    def filter_categories(self, categories, conflicts):
        """Erstellt gefilterte Kategorien OHNE Konflikte"""

        conflict_files = [c['file'] for c in conflicts]

        filtered = {}
        for cat, files in categories.items():
            filtered[cat] = [f for f in files if f not in conflict_files]

        return filtered

    def display_report(self, conflicts, valid, filtered_categories):
        """Zeigt Report"""

        print("=" * 60)
        print("NAJIKA CONFLICT FILTER REPORT")
        print("=" * 60)

        print(f"\n[CONFLICTS]: {len(conflicts)} widersprüchliche Dateien gefunden")
        print()
        for conf in conflicts:
            print(f"  [X] {os.path.basename(conf['file'])}")
            print(f"      Grund: {conf['reason']}")
            print()

        print("=" * 60)
        print(f"[VALID]: {len(valid)} valide Dateien")
        print("=" * 60)

        for cat, files in filtered_categories.items():
            if files and cat != "skip":
                print(f"\n[{cat.upper()}]: {len(files)} Dateien")

        total_filtered = sum(len(files) for cat, files in filtered_categories.items() if cat != "skip")
        print(f"\n[OK] Gesamt nach Filterung: {total_filtered} Dateien")

        return filtered_categories

    def save_filtered(self, filtered_categories):
        """Speichert gefilterte Liste"""

        output = []
        output.append("# NAJIKA FILTERED CATEGORIZATION")
        output.append("# OHNE widersprüchliche alte Versionen")
        output.append("# NUR finale/valide Dateien")
        output.append("")

        for cat in sorted(filtered_categories.keys()):
            files = filtered_categories[cat]
            if files:
                output.append(f"## {cat.upper()}")
                output.append(f"Count: {len(files)}")
                output.append("")
                for f in files:
                    output.append(f"- {f}")
                output.append("")

        output_file = "C:/NajikaCore/NAJIKA_CATEGORIZATION_FILTERED.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output))

        print(f"\n[SAVED] Gefiltert: {output_file}")

        return output_file

if __name__ == "__main__":
    filter = NajikaConflictFilter("C:/NajikaCore/NAJIKA_CATEGORIZATION_COMPLETE.md")

    # 1. Lade Kategorisierung
    categories = filter.load_categorization()

    # 2. Identifiziere Konflikte
    conflicts, valid = filter.identify_conflicts(categories)

    # 3. Filtere
    filtered = filter.filter_categories(categories, conflicts)

    # 4. Report
    filter.display_report(conflicts, valid, filtered)

    # 5. Speichere
    filter.save_filtered(filtered)

    print("\n" + "=" * 60)
    print("[OK] KONFLIKT-FILTERUNG ABGESCHLOSSEN!")
    print("=" * 60)
    print("\nNur finale/valide Versionen bleiben.")
    print('"fast final" Dateien sind BEHALTEN (nur Avatar fehlt)')
