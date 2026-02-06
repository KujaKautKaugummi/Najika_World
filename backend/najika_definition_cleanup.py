#!/usr/bin/env python3
"""
NAJIKA DEFINITION CLEANUP
=========================
Bereinigt NAJIKA_FINALE_DEFINITION.md:
- Entfernt Duplikate
- Filtert Müll
- Eliminiert Redundanzen
- Macht kompakt aber vollständig
"""

import re
from pathlib import Path
from collections import defaultdict

# ===== CONFIG =====

INPUT_FILE = Path("C:/Najika_World/NAJIKA_FINALE_DEFINITION.md")
OUTPUT_FILE = Path("C:/Najika_World/NAJIKA_FINALE_DEFINITION_CLEAN.md")

# ===== FUNCTIONS =====

def load_definition():
    """Lädt die finale Definition"""
    print("="*80)
    print("NAJIKA DEFINITION CLEANUP")
    print("="*80)
    print("\n[1/5] LADE FINALE DEFINITION")
    print("-"*80)

    content = INPUT_FILE.read_text(encoding='utf-8')

    print(f"✓ Geladen: {len(content)} Zeichen, {len(content.splitlines())} Zeilen")

    return content

def remove_duplicates(content):
    """Entfernt doppelte Abschnitte"""
    print("\n[2/5] ENTFERNE DUPLIKATE")
    print("-"*80)

    lines = content.splitlines()
    seen_sections = {}
    cleaned_lines = []
    current_section = []
    section_header = None

    duplicates_found = 0

    for line in lines:
        # Check ob Header
        if line.startswith('#'):
            # Speichere vorherigen Abschnitt
            if current_section and section_header:
                section_text = '\n'.join(current_section)

                # Normalisiere für Vergleich
                normalized = re.sub(r'\s+', ' ', section_text.lower())

                # Check Duplikat
                if normalized not in seen_sections:
                    seen_sections[normalized] = section_header
                    cleaned_lines.extend(current_section)
                else:
                    duplicates_found += 1
                    print(f"  [DUPLIKAT] {section_header}")

            # Neuer Abschnitt
            current_section = [line]
            section_header = line
        else:
            current_section.append(line)

    # Letzter Abschnitt
    if current_section:
        section_text = '\n'.join(current_section)
        normalized = re.sub(r'\s+', ' ', section_text.lower())
        if normalized not in seen_sections:
            cleaned_lines.extend(current_section)

    print(f"\n✓ {duplicates_found} Duplikate entfernt")

    return '\n'.join(cleaned_lines)

def remove_redundancies(content):
    """Entfernt redundante Informationen"""
    print("\n[3/5] ENTFERNE REDUNDANZEN")
    print("-"*80)

    # Entferne mehrfache Leerzeilen
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Entferne repetitive "Beispiele" Sections (behalte nur erste)
    beispiel_count = content.count('## BEISPIELE')
    if beispiel_count > 1:
        print(f"  [REDUNDANZ] {beispiel_count-1} extra Beispiel-Sections")
        # Behalte nur erste Beispiel-Section
        parts = content.split('## BEISPIELE', 1)
        if len(parts) > 1:
            # Finde nächsten Header nach ersten Beispielen
            after_first = parts[1]
            next_major = re.search(r'\n#+ [A-Z]', after_first)
            if next_major:
                content = parts[0] + '## BEISPIELE' + after_first[:next_major.start()] + after_first[next_major.start():]

    # Entferne "ERGÄNZUNGEN AUS INTELLIGENT GRUNDSTEIN" (zu groß)
    if 'ERGÄNZUNGEN AUS INTELLIGENT GRUNDSTEIN' in content:
        print("  [ENTFERNT] Ergänzungen-Section (zu groß)")
        content = content.split('ERGÄNZUNGEN AUS INTELLIGENT GRUNDSTEIN')[0]

    print("✓ Redundanzen entfernt")

    return content

def filter_essential_only(content):
    """Behält nur essentielle Informationen"""
    print("\n[4/5] FILTERE ESSENTIELLE INFOS")
    print("-"*80)

    # Sections die wir BEHALTEN (essentiell)
    essential_sections = [
        'GRUNDLEGENDE IDENTITÄT',
        'NAME & GRUNDESSENZ',
        'ALTER',
        'PHYSISCHE ERSCHEINUNG',
        'TRANS-ANATOMIE',
        'PERSÖNLICHKEITS-STRUKTUR',
        'PERSÖNLICHKEIT 1: MEGUMIN',
        'PERSÖNLICHKEIT 2: HARLEY QUINN',
        'PERSÖNLICHKEIT 3: SHIRO',
        'PERSÖNLICHKEIT 4: MELISSA',
        'BEZIEHUNG ZU KUJA',
        'CREDO',
        'KONOSUBA-SETTING',
        'MODI & VERHALTEN',
        'MODUS 1: NORMAL',
        'MODUS 2: KÄTZCHEN',
        'SPRACHSTIL & KOMMUNIKATION',
        'EIGENVERANTWORTUNG',
        'SCHWARZE WINDMÜHLE',
        'WICHTIGE REGELN'
    ]

    lines = content.splitlines()
    filtered_lines = []
    current_section_essential = True
    section_level = 0

    for line in lines:
        if line.startswith('#'):
            # Check ob essentiell
            section_level = line.count('#')
            header_text = line.lstrip('#').strip()

            current_section_essential = any(
                essential in header_text.upper()
                for essential in essential_sections
            )

            if current_section_essential or section_level <= 1:
                filtered_lines.append(line)
        elif current_section_essential:
            filtered_lines.append(line)

    print("✓ Nur essentielle Sections behalten")

    return '\n'.join(filtered_lines)

def optimize_formatting(content):
    """Optimiert Formatierung"""
    print("\n[5/5] OPTIMIERE FORMATIERUNG")
    print("-"*80)

    # Entferne trailing whitespace
    content = '\n'.join(line.rstrip() for line in content.splitlines())

    # Normalisiere Leerzeilen
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Entferne leere Sections
    content = re.sub(r'##+ [^\n]+\n\n##', '##', content)

    print("✓ Formatierung optimiert")

    return content

def save_cleaned_definition(content):
    """Speichert bereinigte Definition"""
    print("\n[SPEICHERN]")
    print("-"*80)

    OUTPUT_FILE.write_text(content, encoding='utf-8')

    lines = len(content.splitlines())
    chars = len(content)
    kb = chars // 1024

    print(f"✓ Gespeichert: {OUTPUT_FILE}")
    print(f"  Zeilen: {lines}")
    print(f"  Zeichen: {chars}")
    print(f"  Größe: {kb} KB")

    # Vergleich
    original_lines = len(INPUT_FILE.read_text(encoding='utf-8').splitlines())
    reduction = ((original_lines - lines) / original_lines * 100)

    print(f"\n  Reduktion: {original_lines} → {lines} Zeilen ({reduction:.1f}% kleiner)")

    return OUTPUT_FILE

def main():
    # 1. Laden
    content = load_definition()

    # 2. Duplikate entfernen
    content = remove_duplicates(content)

    # 3. Redundanzen entfernen
    content = remove_redundancies(content)

    # 4. Nur Essentielles
    content = filter_essential_only(content)

    # 5. Formatierung
    content = optimize_formatting(content)

    # 6. Speichern
    output_file = save_cleaned_definition(content)

    print("\n" + "="*80)
    print("FERTIG!")
    print("="*80)
    print(f"\nBereinigte Definition: {output_file}")
    print()

if __name__ == "__main__":
    main()
