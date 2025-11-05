#!/usr/bin/env python3
"""
NAJIKA GAME DESIGN BUILDER
===========================
Extrahiert KOMPLETTES Spiel aus:
- 5 BASIS-PDFs (alle Mechaniken, Skills, Systeme)
- INTELLIGENT GRUNDSTEIN (15.400 Sections)
- User-Ideen (Oregon Trail × Konosuba, Klassen-Stories, etc.)

SUCHT NACH:
- Digimon World Anfeuern + Finisher
- Skills/Klassen/Waffen-Systeme
- 1-Skill-Weg (Megumin-Style)
- Skill Weaving
- Farming, Fishing, Crafting
- Oregon Trail Mechaniken
- Konosuba Chaos-Events
- Combat/Battle-Systeme
- Quest-Systeme
- Hardcore/Softie Modi
- Character Creation
- Companion Systeme
- UND ALLES ANDERE!

OUTPUT: Komplette Game-Design Dokumentation
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ===== CONFIG =====

INTELLIGENT_GRUNDSTEIN = Path("C:/NajikaCore/grundstein_output/NAJIKA_INTELLIGENT_GRUNDSTEIN.json")
OUTPUT_DIR = Path("C:/NajikaCore")

# ALLE Game-Keywords (umfassend!)
GAME_KEYWORDS = {
    'combat': ['kampf', 'battle', 'combat', 'fight', 'angriff', 'verteidigung', 'damage', 'hp', 'health'],
    'skills': ['skill', 'fähigkeit', 'ability', 'talent', 'move', 'technik', 'zauber', 'magie', 'spell'],
    'classes': ['klasse', 'class', 'job', 'beruf', 'spezialisierung', 'build', 'archetype'],
    'weapons': ['waffe', 'weapon', 'schwert', 'sword', 'bogen', 'bow', 'stab', 'staff', 'axt', 'axe'],
    'digimon': ['digimon', 'anfeuern', 'cheer', 'finisher', 'mega', 'evolution', 'partner'],
    'skill_weaving': ['skill weaving', 'weave', 'combo', 'chain', 'verketten', 'kombinieren'],
    'one_skill': ['1-skill', 'spezialisierung', 'megumin', 'explosion', 'all-in', 'fokus'],
    'farming': ['farming', 'farm', 'garten', 'garden', 'pflanzen', 'ernten', 'anbau'],
    'fishing': ['fishing', 'angeln', 'fisch', 'fish', 'rute', 'köder'],
    'crafting': ['crafting', 'handwerk', 'herstellen', 'bauen', 'rezept', 'recipe'],
    'oregon_trail': ['oregon trail', 'reise', 'journey', 'trail', 'event', 'random', 'zufalls'],
    'konosuba': ['konosuba', 'chaos', 'chaotisch', 'absurd', 'verrückt', 'quest schief'],
    'quests': ['quest', 'mission', 'aufgabe', 'task', 'auftrag', 'guild'],
    'hardcore': ['hardcore', 'schwer', 'hard', 'difficult', 'brutal', 'permadeath'],
    'softie': ['softie', 'soft', 'easy', 'leicht', 'casual', 'entspannt'],
    'character_creation': ['character creation', 'character creator', 'charakter erstellen', 'custom'],
    'companion': ['companion', 'begleiter', 'partner', 'gefährte', 'persönlichkeit'],
    'leveling': ['level', 'exp', 'experience', 'erfahrung', 'xp', 'progression'],
    'items': ['item', 'gegenstand', 'inventar', 'inventory', 'equipment', 'ausrüstung'],
    'economy': ['geld', 'money', 'währung', 'economy', 'shop', 'kaufen', 'verkaufen'],
    'story': ['story', 'geschichte', 'narrative', 'erzählung', 'plot', 'handlung'],
    'multiplayer': ['multiplayer', 'online', 'coop', 'pvp', 'andere spieler'],
    'ui': ['ui', 'interface', 'menu', 'navigation', 'digivice', 'handy'],
    'animations': ['animation', 'grafik', '3d', 'visual', 'effect', 'shader'],
    'sound': ['sound', 'musik', 'audio', 'voice', 'sfx'],
    'rooms': ['raum', 'room', 'ort', 'location', 'area', 'zone'],
    'minigames': ['minigame', 'minispiel', 'rhythm', 'reflex'],
    'training': ['training', 'üben', 'practice', 'lernen'],
    'saving': ['save', 'speichern', 'laden', 'load', 'checkpoint']
}

# User-Ideen (neue Features)
USER_IDEAS = {
    'oregon_konosuba_fusion': {
        'name': 'Oregon Trail × Konosuba Chaos Engine',
        'description': 'Zufällige Reise-Events (Oregon Trail) mit Konosuba-Chaos (absurde Wendungen, alles geht schief)',
        'examples': [
            'Fluss überqueren → Najika nutzt EXPLOSION → Wasser verdampft → Boot zerstört',
            'Wilde Tiere → Nur Frösche → Najika: EXPLOSION! → Ganzes Dorf sauer',
            'Händler treffen → Najika kauft Explosion-Scrolls → Kein Geld für Essen'
        ]
    },
    'class_story_system': {
        'name': 'Klassen-Spezialisierungs-Story-System',
        'description': 'Jede Klasse/Waffe/1-Skill-Spezialisierung hat EIGENE Story-Linie',
        'examples': [
            'EXPLOSION-Weg: Oregon Events drehen sich um Explosion-Chaos',
            'Schwert-Purist: Events um Ehre, Duelle, Schwertmeister',
            'Bogen-Sniper: Stealth-Events, Jagd-Geschichten',
            'Tank-Weg: Beschützer-Events, Leute retten'
        ],
        'effect': 'Jeder Klassen-Neustart = KOMPLETT andere Story, Replay-Wert × 1000'
    },
    'companion_creation': {
        'name': 'Companion Creation System',
        'description': 'Spieler erstellen eigene Begleiter mit Custom-Persönlichkeiten',
        'features': [
            'Vorgefertigte Persönlichkeiten (Ehrenwerter Ritter, Chaotischer Schurke, etc.)',
            'Custom Personality Builder (Mix aus verschiedenen Charakteren)',
            'Slider-System wie bei Najika (20% Megumin + 50% Gandalf + 30% Deadpool)',
            'Eigene Catchphrases definieren'
        ],
        'note': 'Najika = EXKLUSIV für Kuja! Andere Spieler bekommen sie NICHT!'
    },
    'personality_class_combos': {
        'name': 'Persönlichkeit × Klasse = Einzigartige Stories',
        'description': 'Klassen-Spezialisierung kombiniert mit Companion-Persönlichkeit',
        'examples': [
            'Schwert-Purist + Ehrenwerter Ritter = Ritterehre-Story',
            'Schwert-Purist + Chaotischer Schurke = Hinterhältige Tricks-Story',
            'Explosion-Build + Verrückter Wissenschaftler = Wissenschafts-Chaos',
            'Explosion-Build + Süßer Optimist = Wholesome Destruction'
        ]
    }
}

# ===== FUNCTIONS =====

def load_intelligent_grundstein():
    """Lädt den Intelligent Grundstein"""
    print("="*80)
    print("NAJIKA GAME DESIGN BUILDER")
    print("="*80)
    print("\n[1/6] LADE INTELLIGENT GRUNDSTEIN")
    print("-"*80)

    print(f"Lese: {INTELLIGENT_GRUNDSTEIN}")
    print("Das kann ~30-60 Sekunden dauern...")

    with open(INTELLIGENT_GRUNDSTEIN, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\n✓ Geladen!")
    print(f"  BASIS PDFs: {data['statistics']['basis_count']}")
    print(f"  Intelligente OPTIONALS: {data['statistics']['intelligent_optionals_count']}")
    print(f"  Mechaniken: {data['statistics']['unique_mechanics']}")

    return data

def extract_game_mechanics(grundstein):
    """Extrahiert ALLE Game-Mechaniken"""
    print("\n[2/6] EXTRAHIERE GAME-MECHANIKEN")
    print("-"*80)

    game_sections = defaultdict(list)

    # Durchsuche BASIS PDFs
    print("\n[SUCHE] BASIS PDFs...")
    for pdf in grundstein['basis_pdfs']:
        content_lower = pdf['content'].lower()

        for category, keywords in GAME_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    # Finde Absätze mit diesem Keyword
                    paragraphs = pdf['content'].split('\n\n')
                    for para in paragraphs:
                        if keyword in para.lower() and len(para) > 100:
                            game_sections[category].append({
                                'source': f"BASIS/{pdf['filename']}",
                                'keyword': keyword,
                                'content': para[:1000]  # Max 1000 Zeichen
                            })

    # Durchsuche Intelligent Optionals
    print("\n[SUCHE] Intelligent OPTIONALS...")
    for section in grundstein['intelligent_optionals']:
        content_lower = section['content'].lower()

        for category, keywords in GAME_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    game_sections[category].append({
                        'source': section['source'],
                        'keyword': keyword,
                        'mechanics': section['mechanics'][:5],
                        'content': section['content'][:1000]
                    })

    print(f"\n✓ Game-Mechaniken gefunden:")
    for category, sections in sorted(game_sections.items()):
        print(f"  {category}: {len(sections)} Sections")

    return dict(game_sections)

def build_comprehensive_game_doc(game_sections):
    """Baut umfassende Game-Dokumentation"""
    print("\n[3/6] BAUE GAME-DOKUMENTATION")
    print("-"*80)

    doc = []

    # Header
    doc.append("# NAJIKA GAME - KOMPLETTE DESIGN-DOKUMENTATION")
    doc.append("")
    doc.append(f"**Erstellt:** {datetime.now().isoformat()}")
    doc.append("**Quellen:**")
    doc.append("- 5 BASIS-PDFs (komplette Mechaniken)")
    doc.append("- INTELLIGENT GRUNDSTEIN (15.400 Sections)")
    doc.append("- User-Ideen (Oregon × Konosuba, Klassen-Stories, etc.)")
    doc.append("")
    doc.append("**Status:** Komplettes Game-Design mit allen Mechaniken")
    doc.append("")
    doc.append("---")
    doc.append("")

    # User-Ideen ZUERST (wichtig!)
    doc.append("# TEIL 1: NEUE KERN-FEATURES")
    doc.append("")

    for idea_key, idea_data in USER_IDEAS.items():
        doc.append(f"## {idea_data['name'].upper()}")
        doc.append("")
        doc.append(f"**Konzept:** {idea_data['description']}")
        doc.append("")

        if 'examples' in idea_data:
            doc.append("**Beispiele:**")
            for example in idea_data['examples']:
                doc.append(f"- {example}")
            doc.append("")

        if 'features' in idea_data:
            doc.append("**Features:**")
            for feature in idea_data['features']:
                doc.append(f"- {feature}")
            doc.append("")

        if 'effect' in idea_data:
            doc.append(f"**Effekt:** {idea_data['effect']}")
            doc.append("")

        if 'note' in idea_data:
            doc.append(f"**⚠️ WICHTIG:** {idea_data['note']}")
            doc.append("")

        doc.append("---")
        doc.append("")

    # Game-Mechaniken aus PDFs
    doc.append("# TEIL 2: ALLE GAME-MECHANIKEN")
    doc.append("")

    for category, sections in sorted(game_sections.items()):
        doc.append(f"## {category.upper().replace('_', ' ')}")
        doc.append("")
        doc.append(f"**Gefunden:** {len(sections)} Sections")
        doc.append("")

        # Top 5 Sections pro Kategorie
        for i, section in enumerate(sections[:5], 1):
            doc.append(f"### {i}. Aus: {section['source']}")
            doc.append(f"**Keyword:** {section['keyword']}")
            if 'mechanics' in section:
                doc.append(f"**Mechaniken:** {', '.join(section['mechanics'])}")
            doc.append("")
            doc.append(section['content'][:500])
            doc.append("")
            doc.append("[...]")
            doc.append("")

        if len(sections) > 5:
            doc.append(f"\n*[... und {len(sections)-5} weitere Sections]*\n")

        doc.append("---")
        doc.append("")

    print("✓ Dokumentation erstellt")

    return '\n'.join(doc)

def create_compact_overview(game_doc):
    """Erstellt kompakte Übersicht"""
    print("\n[4/6] ERSTELLE KOMPAKTE ÜBERSICHT")
    print("-"*80)

    overview = []

    overview.append("# NAJIKA GAME - KURZ-ÜBERSICHT")
    overview.append("")
    overview.append("**Für:** KI, Najika, Entwickler")
    overview.append("**Zweck:** Schneller Überblick über ALLES")
    overview.append("")
    overview.append("---")
    overview.append("")

    # Kern-Features
    overview.append("## KERN-FEATURES (NEU)")
    overview.append("")
    for idea_key, idea_data in USER_IDEAS.items():
        overview.append(f"**{idea_data['name']}**")
        overview.append(f"- {idea_data['description']}")
        overview.append("")

    # Mechaniken-Kategorien
    overview.append("## ALLE MECHANIKEN (KATEGORIEN)")
    overview.append("")
    overview.append("Das Spiel enthält folgende Systeme:")
    overview.append("")

    for category in sorted(GAME_KEYWORDS.keys()):
        overview.append(f"- **{category.replace('_', ' ').title()}**")

    overview.append("")
    overview.append("Jede Kategorie hat 5-100+ Sections mit Details.")
    overview.append("")

    print("✓ Übersicht erstellt")

    return '\n'.join(overview)

def save_game_documentation(full_doc, overview):
    """Speichert Game-Dokumentation"""
    print("\n[5/6] SPEICHERE DOKUMENTATION")
    print("-"*80)

    # Komplette Doku
    full_file = OUTPUT_DIR / "NAJIKA_GAME_DESIGN_KOMPLETT.md"
    full_file.write_text(full_doc, encoding='utf-8')
    print(f"✓ Komplett: {full_file} ({len(full_doc)//1024} KB)")

    # Übersicht
    overview_file = OUTPUT_DIR / "NAJIKA_GAME_DESIGN_UEBERSICHT.md"
    overview_file.write_text(overview, encoding='utf-8')
    print(f"✓ Übersicht: {overview_file} ({len(overview)//1024} KB)")

    return full_file, overview_file

def create_json_export(game_sections):
    """Erstellt JSON-Export für programmatische Nutzung"""
    print("\n[6/6] ERSTELLE JSON-EXPORT")
    print("-"*80)

    export_data = {
        'created': datetime.now().isoformat(),
        'description': 'Najika Game Design - Alle Mechaniken strukturiert',
        'user_ideas': USER_IDEAS,
        'game_mechanics': {
            category: {
                'count': len(sections),
                'keywords': GAME_KEYWORDS[category],
                'sections': sections[:10]  # Top 10 pro Kategorie
            }
            for category, sections in game_sections.items()
        },
        'statistics': {
            'total_categories': len(game_sections),
            'total_sections': sum(len(s) for s in game_sections.values())
        }
    }

    json_file = OUTPUT_DIR / "NAJIKA_GAME_DESIGN.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"✓ JSON: {json_file}")

    return json_file

def main():
    # 1. Lade Grundstein
    grundstein = load_intelligent_grundstein()

    # 2. Extrahiere Mechaniken
    game_sections = extract_game_mechanics(grundstein)

    # 3. Baue Doku
    full_doc = build_comprehensive_game_doc(game_sections)

    # 4. Übersicht
    overview = create_compact_overview(full_doc)

    # 5. Speichern
    full_file, overview_file = save_game_documentation(full_doc, overview)

    # 6. JSON
    json_file = create_json_export(game_sections)

    print("\n" + "="*80)
    print("FERTIG!")
    print("="*80)
    print(f"\nKOMPLETTE GAME-DESIGN DOKUMENTATION erstellt:")
    print(f"  Komplett: {full_file}")
    print(f"  Übersicht: {overview_file}")
    print(f"  JSON: {json_file}")
    print()

if __name__ == "__main__":
    main()
