#!/usr/bin/env python3
"""
NAJIKA INTELLIGENT GRUNDSTEIN BUILDER
======================================
INTELLIGENTE SUCHE nach Mechaniken/Themen:

1. Extrahiere ALLE Mechaniken/Themen aus 5 BASIS-PDFs
2. Suche in neu neu/ + zip/ nach diesen Themen
3. Lese GANZE ABSCHNITTE (auch wenn neue Mechaniken dabei stehen)
4. Füge als OPTIONAL hinzu wenn NICHT 1:1 Duplikat

BEISPIEL:
- Finde "Oregon Trail" → Lese ganzen Abschnitt (inkl. Ninja-Kampf)
- Finde "Skill-Mechanik" → Lese ganzen Abschnitt (inkl. neue Skills)
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ===== CONFIG =====

GRUNDSTEIN_FILE = Path("C:/NajikaCore/grundstein_output/NAJIKA_FINAL_GRUNDSTEIN.json")
OUTPUT_DIR = Path("C:/NajikaCore/grundstein_output")

# Keywords für Mechaniken (werden aus BASIS extrahiert + diese defaults)
MECHANIC_KEYWORDS = [
    'oregon trail', 'skill', 'mechanik', 'kampf', 'battle', 'hardcore',
    'modus', 'minigame', 'minispiel', 'ui', 'navigation', 'menu',
    'level', 'exp', 'erfahrung', 'training', 'quest', 'mission',
    'item', 'inventar', 'crafting', 'handwerk', 'upgrade',
    'digimon', 'sakura', 'beziehung', 'dialog', 'story',
    'animation', 'grafik', '3d', 'shader', 'effect',
    'sound', 'musik', 'audio', 'voice',
    'multiplayer', 'online', 'save', 'speichern',
    'achievement', 'erfolg', 'badge', 'reward', 'belohnung',
    'ninja', 'kampfsystem', 'combo', 'special', 'explosion'
]

# ===== FUNCTIONS =====

def load_grundstein():
    """Lädt den FINAL GRUNDSTEIN"""
    print("="*80)
    print("NAJIKA INTELLIGENT GRUNDSTEIN BUILDER")
    print("="*80)
    print("\n[1/5] LADE FINAL GRUNDSTEIN")
    print("-"*80)

    with open(GRUNDSTEIN_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ Geladen: {GRUNDSTEIN_FILE}")
    print(f"  BASIS PDFs: {len(data['basis_pdfs'])}")
    print(f"  OPTIONAL neu neu: {len(data['optional_neu_neu'])}")
    print(f"  OPTIONAL zip: {len(data['optional_zip'])}")

    return data

def extract_mechanics_from_basis(grundstein):
    """Extrahiert alle Mechaniken/Themen aus den 5 BASIS-PDFs"""
    print("\n[2/5] EXTRAHIERE MECHANIKEN AUS BASIS-PDFs")
    print("-"*80)

    mechanics = set(MECHANIC_KEYWORDS)  # Start with defaults

    # Durchsuche alle BASIS-PDFs nach Überschriften und wichtigen Begriffen
    for pdf in grundstein['basis_pdfs']:
        content = pdf['content'].lower()

        # Finde Überschriften (# oder ## oder Großbuchstaben)
        headings = re.findall(r'(?:^|\n)#+\s*([^\n]+)', content)
        headings += re.findall(r'(?:^|\n)([A-ZÄÖÜ][A-ZÄÖÜ\s]{3,30})(?:\n|:)', content)

        for heading in headings:
            cleaned = heading.strip().lower()
            if len(cleaned) > 3:
                mechanics.add(cleaned)

        # Finde wichtige Begriffe in Klammern oder nach Doppelpunkt
        terms = re.findall(r'\(([^)]{3,30})\)', content)
        terms += re.findall(r':\s*([a-zäöü\s]{3,30})[,.]', content)

        for term in terms:
            cleaned = term.strip().lower()
            if len(cleaned) > 3 and not cleaned.isdigit():
                mechanics.add(cleaned)

    # Filtere zu generische Begriffe
    filtered_mechanics = set()
    generic = ['das', 'der', 'die', 'und', 'oder', 'ist', 'sind', 'wird', 'werden',
               'kann', 'muss', 'soll', 'hat', 'haben', 'für', 'mit', 'von', 'zu',
               'in', 'an', 'auf', 'bei', 'durch', 'um', 'nach', 'vor']

    for mech in mechanics:
        words = mech.split()
        if not any(g in words for g in generic) or len(words) > 1:
            filtered_mechanics.add(mech)

    print(f"✓ {len(filtered_mechanics)} Mechaniken/Themen gefunden")
    print(f"  Beispiele: {list(filtered_mechanics)[:10]}")

    return list(filtered_mechanics)

def find_sections_in_text(text, mechanics):
    """Findet Abschnitte zu Mechaniken im Text"""
    sections = []
    text_lower = text.lower()

    # Teile Text in Absätze
    paragraphs = text.split('\n\n')

    for i, para in enumerate(paragraphs):
        para_lower = para.lower()

        # Check ob Mechanik vorkommt
        found_mechanics = []
        for mech in mechanics:
            if mech in para_lower:
                found_mechanics.append(mech)

        if found_mechanics:
            # Lese ganzen Kontext (aktueller + vorheriger + nächster Absatz)
            start = max(0, i-1)
            end = min(len(paragraphs), i+2)

            context = '\n\n'.join(paragraphs[start:end])

            sections.append({
                'mechanics': found_mechanics,
                'content': context,
                'paragraph_index': i
            })

    return sections

def is_duplicate(section_content, existing_contents):
    """Prüft ob Abschnitt 1:1 Duplikat ist"""
    # Normalisiere Text
    normalized = re.sub(r'\s+', ' ', section_content.lower().strip())

    for existing in existing_contents:
        existing_normalized = re.sub(r'\s+', ' ', existing.lower().strip())

        # Check exakte Übereinstimmung
        if normalized == existing_normalized:
            return True

        # Check >90% Übereinstimmung
        if len(normalized) > 100:
            # Einfacher Overlap-Check
            overlap = len(set(normalized.split()) & set(existing_normalized.split()))
            total = len(set(normalized.split()) | set(existing_normalized.split()))

            if overlap / total > 0.9:
                return True

    return False

def build_intelligent_grundstein(grundstein, mechanics):
    """Baut intelligenten Grundstein mit gezielten Abschnitten"""
    print("\n[3/5] INTELLIGENTE SUCHE IN OPTIONAL FILES")
    print("-"*80)

    intelligent_optionals = []
    existing_contents = []

    # Speichere BASIS-Inhalte als existing
    for pdf in grundstein['basis_pdfs']:
        existing_contents.append(pdf['content'])

    # Durchsuche neu neu/ Files
    print("\n[SUCHE] neu neu/ Files...")
    for file_data in grundstein['optional_neu_neu']:
        sections = find_sections_in_text(file_data['content'], mechanics)

        for section in sections:
            if not is_duplicate(section['content'], existing_contents):
                intelligent_optionals.append({
                    'source': f"neu neu/{file_data['filename']}",
                    'mechanics': section['mechanics'],
                    'content': section['content'],
                    'type': 'intelligent_addition'
                })
                existing_contents.append(section['content'])
                print(f"  ✓ {file_data['filename']}: {section['mechanics'][:3]}")

    # Durchsuche zip/ Files
    print("\n[SUCHE] zip/ Files...")
    for file_data in grundstein['optional_zip']:
        sections = find_sections_in_text(file_data['content'], mechanics)

        for section in sections:
            if not is_duplicate(section['content'], existing_contents):
                intelligent_optionals.append({
                    'source': f"zip/{file_data['filename']}",
                    'mechanics': section['mechanics'],
                    'content': section['content'],
                    'type': 'intelligent_addition'
                })
                existing_contents.append(section['content'])
                print(f"  ✓ {file_data['filename']}: {section['mechanics'][:3]}")

    print(f"\n✓ {len(intelligent_optionals)} intelligente OPTIONALS gefunden")

    return intelligent_optionals

def save_intelligent_grundstein(grundstein, intelligent_optionals):
    """Speichert intelligenten Grundstein"""
    print("\n[4/5] BAUE FINALEN INTELLIGENT GRUNDSTEIN")
    print("-"*80)

    # Gruppiere nach Mechaniken
    grouped = defaultdict(list)
    for opt in intelligent_optionals:
        for mech in opt['mechanics']:
            grouped[mech].append(opt)

    intelligent_grundstein = {
        'created': datetime.now().isoformat(),
        'description': 'Najika Intelligent Grundstein - BASIS mit intelligenten OPTIONALS nach Mechaniken',
        'master_kern': grundstein['master_kern'],
        'basis_pdfs': grundstein['basis_pdfs'],
        'intelligent_optionals': intelligent_optionals,
        'grouped_by_mechanic': dict(grouped),
        'statistics': {
            'basis_count': len(grundstein['basis_pdfs']),
            'intelligent_optionals_count': len(intelligent_optionals),
            'unique_mechanics': len(grouped),
            'total_sections': sum(len(v) for v in grouped.values())
        }
    }

    print(f"✓ BASIS: {intelligent_grundstein['statistics']['basis_count']} PDFs")
    print(f"✓ Intelligente OPTIONALS: {intelligent_grundstein['statistics']['intelligent_optionals_count']}")
    print(f"✓ Mechaniken abgedeckt: {intelligent_grundstein['statistics']['unique_mechanics']}")

    # Speichern
    print("\n[5/5] SPEICHERN")
    print("-"*80)

    # JSON
    json_output = OUTPUT_DIR / "NAJIKA_INTELLIGENT_GRUNDSTEIN.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(intelligent_grundstein, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON: {json_output}")

    # Markdown (nach Mechaniken gruppiert)
    md_output = OUTPUT_DIR / "NAJIKA_INTELLIGENT_GRUNDSTEIN.md"
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write("# NAJIKA INTELLIGENT GRUNDSTEIN\n\n")
        f.write(f"**Erstellt:** {intelligent_grundstein['created']}\n\n")
        f.write("---\n\n")

        # MASTER-KERN
        f.write("# MASTER-KERN\n\n")
        f.write(intelligent_grundstein['master_kern']['content'])
        f.write("\n\n---\n\n")

        # BASIS PDFs
        f.write("# BASIS: 5 PDFs (MIT MASTER-KERN)\n\n")
        for i, pdf in enumerate(intelligent_grundstein['basis_pdfs'], 1):
            f.write(f"## {i}. {pdf['filename']}\n\n")
            f.write(f"**Größe:** {pdf['integrated_size']} Zeichen\n\n")
            f.write("---\n\n")

        # INTELLIGENTE OPTIONALS (nach Mechaniken gruppiert)
        f.write("# INTELLIGENTE OPTIONALS (NACH MECHANIKEN)\n\n")

        for mechanic, sections in sorted(intelligent_grundstein['grouped_by_mechanic'].items()):
            f.write(f"## Mechanik: {mechanic.upper()}\n\n")
            f.write(f"**Abschnitte:** {len(sections)}\n\n")

            for i, section in enumerate(sections[:5], 1):  # Max 5 pro Mechanik in MD
                f.write(f"### {i}. Aus: {section['source']}\n\n")
                f.write(f"**Mechaniken:** {', '.join(section['mechanics'][:5])}\n\n")
                f.write(section['content'][:1000] + "\n\n[... gekürzt ...]\n\n")

            if len(sections) > 5:
                f.write(f"\n*[... und {len(sections)-5} weitere Abschnitte]*\n\n")

            f.write("---\n\n")

    print(f"✓ MD: {md_output}")

    print("\n" + "="*80)
    print("FERTIG!")
    print("="*80)
    print(f"Intelligente OPTIONALS: {len(intelligent_optionals)}")
    print(f"Mechaniken abgedeckt: {intelligent_grundstein['statistics']['unique_mechanics']}")
    print()

def main():
    # Lade Grundstein
    grundstein = load_grundstein()

    # Extrahiere Mechaniken
    mechanics = extract_mechanics_from_basis(grundstein)

    # Baue intelligenten Grundstein
    intelligent_optionals = build_intelligent_grundstein(grundstein, mechanics)

    # Speichern
    save_intelligent_grundstein(grundstein, intelligent_optionals)

if __name__ == "__main__":
    main()
