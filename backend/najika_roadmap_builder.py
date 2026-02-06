#!/usr/bin/env python3
"""
NAJIKA ROADMAP BUILDER
======================
Analysiert:
1. Aktuelles Digivice (was ist schon da?)
2. Game-Design (was fehlt noch?)
3. Erstellt priorisierte Roadmap

OUTPUT: Entwicklungs-Roadmap mit Phasen
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ===== CONFIG =====

DIGIVICE_DIR = Path("C:/Najika_World/digivice")
GAME_DESIGN_JSON = Path("C:/Najika_World/NAJIKA_GAME_DESIGN.json")
OUTPUT_DIR = Path("C:/Najika_World")

# Aktuelle Features (im Digivice vorhanden)
CURRENT_FEATURES = {
    '3d_scene.js': ['3D Rendering', 'Rooms', 'Character Movement', 'Camera Controls'],
    'battle_core.js': ['Turn-based Combat', 'HP System', 'Attack Mechanics'],
    'chat_ui.js': ['Chat Interface', 'Message Display', 'Najika AI'],
    'minigames.js': ['Rhythm Game', 'Garden Game', 'Reflex Game', 'Cooking', 'Training', 'Crafting'],
    'oregon.js': ['Oregon Trail Events', 'Random Events'],
    'dungeon_generator.js': ['Dungeon Generation', 'Procedural Maps'],
    'dungeon_combat.js': ['Dungeon Combat System'],
    'dungeon_enemies.js': ['Enemy Types', 'Enemy AI'],
    'kaykit_loader.js': ['Asset Loading', 'KayKit Integration'],
    'private_mode.js': ['NSFW Mode Indicator'],
    'room_connector.js': ['Room Navigation'],
    'touch_controls.js': ['Mobile Touch Controls'],
    'terminal_modules.js': ['Terminal Integration'],
    'code_editor.js': ['Code Editor']
}

# ===== FUNCTIONS =====

def analyze_current_digivice():
    """Analysiert aktuelles Digivice"""
    print("="*80)
    print("NAJIKA ROADMAP BUILDER")
    print("="*80)
    print("\n[1/4] ANALYSIERE AKTUELLES DIGIVICE")
    print("-"*80)

    current = {
        'files': [],
        'features': [],
        'categories': defaultdict(list)
    }

    # Durchsuche Digivice-Dateien
    if DIGIVICE_DIR.exists():
        js_files = list(DIGIVICE_DIR.glob('js/*.js'))

        for js_file in js_files:
            filename = js_file.name
            current['files'].append(filename)

            if filename in CURRENT_FEATURES:
                for feature in CURRENT_FEATURES[filename]:
                    current['features'].append(feature)

                    # Kategorisiere
                    if any(word in feature.lower() for word in ['combat', 'battle', 'fight']):
                        current['categories']['combat'].append(feature)
                    elif any(word in feature.lower() for word in ['game', 'mini']):
                        current['categories']['minigames'].append(feature)
                    elif any(word in feature.lower() for word in ['3d', 'render', 'scene']):
                        current['categories']['graphics'].append(feature)
                    elif any(word in feature.lower() for word in ['chat', 'ai', 'najika']):
                        current['categories']['ai'].append(feature)
                    elif any(word in feature.lower() for word in ['dungeon', 'procedural']):
                        current['categories']['dungeon'].append(feature)
                    else:
                        current['categories']['other'].append(feature)

    print(f"✓ Gefunden: {len(current['files'])} JS-Files")
    print(f"✓ Features: {len(current['features'])}")
    print("\nKategorien:")
    for cat, feats in sorted(current['categories'].items()):
        print(f"  {cat}: {len(feats)} Features")

    return current

def load_game_design():
    """Lädt Game-Design JSON"""
    print("\n[2/4] LADE GAME-DESIGN")
    print("-"*80)

    with open(GAME_DESIGN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ Game-Design geladen")
    print(f"  Kategorien: {data['statistics']['total_categories']}")
    print(f"  Sections: {data['statistics']['total_sections']}")

    return data

def identify_missing_features(current, game_design):
    """Identifiziert fehlende Features"""
    print("\n[3/4] IDENTIFIZIERE FEHLENDE FEATURES")
    print("-"*80)

    missing = defaultdict(list)

    # Check alle Game-Design Kategorien
    for category, data in game_design['game_mechanics'].items():
        category_name = category.replace('_', ' ').title()

        # Check ob Kategorie teilweise implementiert
        has_partial = False
        for feature in current['features']:
            if any(keyword in feature.lower() for keyword in data['keywords'][:3]):
                has_partial = True
                break

        if not has_partial:
            missing[category_name] = {
                'priority': 'HIGH' if data['count'] > 5000 else 'MEDIUM' if data['count'] > 1000 else 'LOW',
                'section_count': data['count'],
                'keywords': data['keywords'][:5]
            }

    print(f"✓ {len(missing)} Kategorien fehlen oder unvollständig")
    print("\nTop 10 fehlende Features (nach Priority):")
    for i, (cat, info) in enumerate(sorted(missing.items(), key=lambda x: x[1]['section_count'], reverse=True)[:10], 1):
        print(f"  {i}. {cat} ({info['priority']}) - {info['section_count']} Sections")

    return missing

def build_roadmap(current, missing, game_design):
    """Erstellt Roadmap"""
    print("\n[4/4] BAUE ROADMAP")
    print("-"*80)

    roadmap = {
        'created': datetime.now().isoformat(),
        'phases': []
    }

    # PHASE 1: MVP (Foundation)
    phase1 = {
        'name': 'PHASE 1: MVP (Minimum Viable Product)',
        'duration': '2-4 Wochen',
        'goal': 'Spielbar mit Kern-Features',
        'tasks': [
            {
                'category': 'Combat Enhancement',
                'status': 'PARTIAL' if 'combat' in current['categories'] else 'TODO',
                'priority': 'CRITICAL',
                'tasks': [
                    'Erweitere Combat-System (aktuell basic)',
                    'Füge Skills-System hinzu',
                    'HP/MP Management',
                    'Combo-System'
                ]
            },
            {
                'category': 'Leveling System',
                'status': 'MISSING',
                'priority': 'CRITICAL',
                'tasks': [
                    'XP-System implementieren',
                    'Level-Up Mechanik',
                    'Stat-Progression',
                    'Skill-Unlocks'
                ]
            },
            {
                'category': 'UI/UX Improvements',
                'status': 'PARTIAL',
                'priority': 'HIGH',
                'tasks': [
                    'Digivice UI verbessern',
                    'Stats-Anzeige',
                    'Quest-Log',
                    'Inventory-System'
                ]
            },
            {
                'category': 'Save System',
                'status': 'MISSING',
                'priority': 'HIGH',
                'tasks': [
                    'Save/Load implementieren',
                    'Auto-Save',
                    'Multiple Save-Slots',
                    'Cloud-Save (optional)'
                ]
            }
        ]
    }

    # PHASE 2: Core Features
    phase2 = {
        'name': 'PHASE 2: Core Game Features',
        'duration': '4-6 Wochen',
        'goal': 'Alle Haupt-Mechaniken',
        'tasks': [
            {
                'category': 'Class System',
                'status': 'MISSING',
                'priority': 'HIGH',
                'tasks': [
                    'Klassen-Auswahl',
                    'Skill-Trees pro Klasse',
                    '1-Skill-Spezialisierung (Megumin-Style)',
                    'Klassen-Wechsel-Mechanik'
                ]
            },
            {
                'category': 'Skill Weaving',
                'status': 'MISSING',
                'priority': 'MEDIUM',
                'tasks': [
                    'Skill-Combo System',
                    'Skill-Chains',
                    'Weave-Mechanik',
                    'Combo-Rewards'
                ]
            },
            {
                'category': 'Digimon System',
                'status': 'MISSING',
                'priority': 'HIGH',
                'tasks': [
                    'Digimon Partner',
                    'Anfeuern-Mechanik',
                    'Finisher-Attacks',
                    'Evolution'
                ]
            },
            {
                'category': 'Oregon Trail × Konosuba',
                'status': 'PARTIAL' if 'oregon.js' in current['files'] else 'MISSING',
                'priority': 'HIGH',
                'tasks': [
                    'Oregon Trail Events erweitern',
                    'Konosuba Chaos integrieren',
                    'Absurde Wendungen',
                    'Najika reagiert dramatisch'
                ]
            }
        ]
    }

    # PHASE 3: Advanced Features
    phase3 = {
        'name': 'PHASE 3: Advanced Features & Content',
        'duration': '6-8 Wochen',
        'goal': 'Tiefe und Replay-Wert',
        'tasks': [
            {
                'category': 'Class-Story System',
                'status': 'MISSING',
                'priority': 'HIGH',
                'tasks': [
                    'Story-Linien pro Klasse',
                    'Spezialisierungs-Events',
                    'Unique Dialoge per Build',
                    'Class-specific Oregon Events'
                ]
            },
            {
                'category': 'Companion Creation',
                'status': 'MISSING',
                'priority': 'MEDIUM',
                'tasks': [
                    'Character Creator',
                    'Vorgefertigte Persönlichkeiten',
                    'Custom Personality Builder',
                    'Companion AI'
                ]
            },
            {
                'category': 'Hardcore/Softie Modi',
                'status': 'MISSING',
                'priority': 'MEDIUM',
                'tasks': [
                    'Hardcore Mode (Permadeath)',
                    'Softie Mode (Easy)',
                    'Difficulty Scaling',
                    'Mode-specific Rewards'
                ]
            },
            {
                'category': 'Farming/Fishing/Crafting',
                'status': 'PARTIAL' if 'minigames.js' in current['files'] else 'MISSING',
                'priority': 'MEDIUM',
                'tasks': [
                    'Farming-System',
                    'Fishing-Mechanik',
                    'Crafting erweitern',
                    'Gathering/Resources'
                ]
            }
        ]
    }

    # PHASE 4: Content & Polish
    phase4 = {
        'name': 'PHASE 4: Content Expansion & Polish',
        'duration': '4-6 Wochen',
        'goal': 'Content + Qualität',
        'tasks': [
            {
                'category': 'More Minigames',
                'status': 'PARTIAL',
                'priority': 'LOW',
                'tasks': [
                    'Neue Minigames',
                    'Scoring-System',
                    'Leaderboards',
                    'Minigame-Rewards'
                ]
            },
            {
                'category': 'Story Content',
                'status': 'MISSING',
                'priority': 'MEDIUM',
                'tasks': [
                    'Haupt-Story',
                    'Side-Quests',
                    'NPC-Dialoge',
                    'Cutscenes'
                ]
            },
            {
                'category': 'Animations & Effects',
                'status': 'BASIC',
                'priority': 'MEDIUM',
                'tasks': [
                    'Skill-Animationen',
                    'Particle-Effects',
                    'Combat-Polish',
                    'UI-Transitions'
                ]
            },
            {
                'category': 'Sound & Music',
                'status': 'MISSING',
                'priority': 'LOW',
                'tasks': [
                    'Background Music',
                    'Sound Effects',
                    'Voice Lines (optional)',
                    'Audio-System'
                ]
            }
        ]
    }

    # PHASE 5: Multiplayer & Final Polish
    phase5 = {
        'name': 'PHASE 5: Multiplayer & Launch Prep',
        'duration': '6-8 Wochen',
        'goal': 'Multiplayer + Launch-Ready',
        'tasks': [
            {
                'category': 'Multiplayer',
                'status': 'MISSING',
                'priority': 'LOW',
                'tasks': [
                    'Online Infrastructure',
                    'Co-op Mode',
                    'PvP (optional)',
                    'Friend System'
                ]
            },
            {
                'category': 'Performance',
                'status': 'TODO',
                'priority': 'HIGH',
                'tasks': [
                    'Mobile Optimization',
                    'Loading Times',
                    'Memory Management',
                    'Battery Optimization'
                ]
            },
            {
                'category': 'Testing & Bug Fixes',
                'status': 'ONGOING',
                'priority': 'CRITICAL',
                'tasks': [
                    'Beta Testing',
                    'Bug Fixes',
                    'Balance-Tweaks',
                    'QA'
                ]
            }
        ]
    }

    roadmap['phases'] = [phase1, phase2, phase3, phase4, phase5]

    print("✓ Roadmap erstellt")
    print(f"  Phasen: {len(roadmap['phases'])}")

    return roadmap

def save_roadmap(roadmap):
    """Speichert Roadmap"""
    print("\n[SPEICHERN]")
    print("-"*80)

    # Markdown
    md_lines = []
    md_lines.append("# NAJIKA HANDYSPIEL - ENTWICKLUNGS-ROADMAP")
    md_lines.append("")
    md_lines.append(f"**Erstellt:** {roadmap['created']}")
    md_lines.append("**Status:** Draft")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    for phase in roadmap['phases']:
        md_lines.append(f"## {phase['name']}")
        md_lines.append("")
        md_lines.append(f"**Dauer:** {phase['duration']}")
        md_lines.append(f"**Ziel:** {phase['goal']}")
        md_lines.append("")

        for task_group in phase['tasks']:
            md_lines.append(f"### {task_group['category']}")
            md_lines.append(f"**Status:** {task_group['status']} | **Priority:** {task_group['priority']}")
            md_lines.append("")
            md_lines.append("**Tasks:**")
            for task in task_group['tasks']:
                md_lines.append(f"- [ ] {task}")
            md_lines.append("")

        md_lines.append("---")
        md_lines.append("")

    md_file = OUTPUT_DIR / "NAJIKA_ROADMAP.md"
    md_file.write_text('\n'.join(md_lines), encoding='utf-8')
    print(f"✓ Markdown: {md_file}")

    # JSON
    json_file = OUTPUT_DIR / "NAJIKA_ROADMAP.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(roadmap, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON: {json_file}")

    return md_file

def main():
    # 1. Analysiere aktuelles Digivice
    current = analyze_current_digivice()

    # 2. Lade Game-Design
    game_design = load_game_design()

    # 3. Identifiziere fehlende Features
    missing = identify_missing_features(current, game_design)

    # 4. Baue Roadmap
    roadmap = build_roadmap(current, missing, game_design)

    # 5. Speichern
    roadmap_file = save_roadmap(roadmap)

    print("\n" + "="*80)
    print("FERTIG!")
    print("="*80)
    print(f"\nROADMAP erstellt: {roadmap_file}")
    print()

if __name__ == "__main__":
    main()
