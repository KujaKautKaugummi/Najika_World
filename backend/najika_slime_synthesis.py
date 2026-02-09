#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA WORLD - Slime Synthesis/Fusion System
============================================
Basiert auf Dragon Quest Monsters Mechanik:
- 2 Monster Level 10+ → 1 neues Monster
- Originale sind WEG (wichtige Entscheidung!)
- Plus-Wert System (+N)
- Skill-Vererbung
- 4-Eltern Spezial-Synthesen

Erstellt: 2026-01-28
"""

import time
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from najika_slime_system import (
    SlimeState, SlimeType, EvolutionStage,
    get_slime_system, SLIME_COLORS
)


# =============================================================================
# SYNTHESIS RECIPES
# =============================================================================

# Basis-Synthesen: Type1 + Type2 = Result
# Format: frozenset({type1, type2}): result_type
BASIC_SYNTHESIS = {
    frozenset({SlimeType.MOOS.value, SlimeType.WASSER.value}): "sumpf_schleim",
    frozenset({SlimeType.FROST.value, SlimeType.MAGMA.value}): "dampf_schleim",
    frozenset({SlimeType.BLITZ.value, SlimeType.SAND.value}): "glas_schleim",
    frozenset({SlimeType.GIFT.value, SlimeType.KRISTALL.value}): "toxin_kristall",
    frozenset({SlimeType.MOOS.value, SlimeType.GIFT.value}): "pilz_schleim",
    frozenset({SlimeType.KRISTALL.value, SlimeType.SAND.value}): "juwelen_schleim",
    frozenset({SlimeType.FROST.value, SlimeType.WASSER.value}): "eisberg_schleim",
    frozenset({SlimeType.BLITZ.value, SlimeType.WASSER.value}): "sturm_schleim",
    frozenset({SlimeType.MAGMA.value, SlimeType.SAND.value}): "obsidian_schleim",
    frozenset({SlimeType.MOOS.value, SlimeType.FROST.value}): "winter_gruen",
}

# Hybrid Slime Daten
HYBRID_SLIMES = {
    "sumpf_schleim": {
        "name": "Sumpf-Schleim",
        "color": "#5D4037",  # Braun-Gruen
        "base_skills": ["mud_trap", "swamp_gas"],
        "passive_bonus": {
            "farming_speed": 0.15,
            "fishing_luck": 0.15,
            "description": "Kombination aus Moos und Wasser Boni"
        }
    },
    "dampf_schleim": {
        "name": "Dampf-Schleim",
        "color": "#B0BEC5",  # Grau
        "base_skills": ["steam_burst", "temperature_shift"],
        "passive_bonus": {
            "smithing_bonus": 0.15,
            "cold_resistance": 0.10,
            "fire_resistance": 0.10,
            "description": "Kann Hitze UND Kaelte nutzen"
        }
    },
    "glas_schleim": {
        "name": "Glas-Schleim",
        "color": "#FFF176",  # Hellgelb
        "base_skills": ["light_refraction", "cutting_edge"],
        "passive_bonus": {
            "crafting_speed": 0.20,
            "treasure_find": 0.15,
            "description": "Praezise Lichtmanipulation"
        }
    },
    "toxin_kristall": {
        "name": "Toxin-Kristall",
        "color": "#7B1FA2",  # Dunkelviolett
        "base_skills": ["poison_crystal", "toxic_shine"],
        "passive_bonus": {
            "poison_immunity": 0.40,
            "mining_speed": 0.15,
            "description": "Giftiger Kristall-Hybrid"
        }
    },
    "pilz_schleim": {
        "name": "Pilz-Schleim",
        "color": "#795548",  # Braun
        "base_skills": ["spore_cloud", "mushroom_shield"],
        "passive_bonus": {
            "herb_quality": 0.25,
            "stealth": 0.15,
            "description": "Pilz-basierte Faehigkeiten"
        }
    },
    "juwelen_schleim": {
        "name": "Juwelen-Schleim",
        "color": "#E91E63",  # Pink
        "base_skills": ["gem_blast", "treasure_sense"],
        "passive_bonus": {
            "treasure_find": 0.35,
            "trade_discount": 0.10,
            "description": "Findet Schaetze wie kein anderer"
        }
    },
    "eisberg_schleim": {
        "name": "Eisberg-Schleim",
        "color": "#4FC3F7",  # Eisblau
        "base_skills": ["iceberg_crash", "deep_freeze"],
        "passive_bonus": {
            "fishing_luck": 0.25,
            "cold_resistance": 0.30,
            "description": "Meister der kalten Gewaesser"
        }
    },
    "sturm_schleim": {
        "name": "Sturm-Schleim",
        "color": "#5C6BC0",  # Indigo
        "base_skills": ["thunderstorm", "lightning_wave"],
        "passive_bonus": {
            "movement_speed": 0.20,
            "swimming_speed": 0.20,
            "description": "Elektrisierende Geschwindigkeit"
        }
    },
    "obsidian_schleim": {
        "name": "Obsidian-Schleim",
        "color": "#212121",  # Fast Schwarz
        "base_skills": ["obsidian_blade", "volcanic_armor"],
        "passive_bonus": {
            "smithing_bonus": 0.30,
            "fire_resistance": 0.25,
            "description": "Ultimativer Schmied-Begleiter"
        }
    },
    "winter_gruen": {
        "name": "Winter-Gruen",
        "color": "#00897B",  # Tuerkis
        "base_skills": ["frost_leaf", "evergreen_shield"],
        "passive_bonus": {
            "farming_speed": 0.15,
            "cold_resistance": 0.20,
            "herb_quality": 0.10,
            "description": "Pflanzen gedeihen auch im Winter"
        }
    }
}

# Legendaere 4-Eltern Synthesen
# Format: ((parent1, parent2), (parent3, parent4)): result
LEGENDARY_SYNTHESIS = {
    # [Frost + Magma] = Dampf    [Blitz + Wasser] = Sturm
    # [Dampf + Sturm] = WETTER-GOTT
    (frozenset({"dampf_schleim", "sturm_schleim"})): {
        "result": "wetter_gott_schleim",
        "requirements": {
            "grandparents": [
                (SlimeType.FROST.value, SlimeType.MAGMA.value),
                (SlimeType.BLITZ.value, SlimeType.WASSER.value)
            ]
        }
    },
    # [Moos + Gift] = Pilz    [Kristall + Sand] = Juwel
    # [Pilz + Juwel] = NATUR-GEIST
    (frozenset({"pilz_schleim", "juwelen_schleim"})): {
        "result": "natur_geist_schleim",
        "requirements": {
            "grandparents": [
                (SlimeType.MOOS.value, SlimeType.GIFT.value),
                (SlimeType.KRISTALL.value, SlimeType.SAND.value)
            ]
        }
    }
}

# Legendaere Slime Daten
LEGENDARY_SLIMES = {
    "wetter_gott_schleim": {
        "name": "Wetter-Gott-Schleim",
        "color": "rainbow",
        "base_skills": ["weather_control", "divine_storm", "elemental_mastery"],
        "passive_bonus": {
            "all_bonus": 0.15,
            "luck": 0.20,
            "description": "Kontrolliert das Wetter selbst!"
        }
    },
    "natur_geist_schleim": {
        "name": "Natur-Geist-Schleim",
        "color": "#00C853",  # Neon-Gruen
        "base_skills": ["nature_wrath", "crystal_garden", "life_force"],
        "passive_bonus": {
            "farming_speed": 0.30,
            "herb_quality": 0.30,
            "treasure_find": 0.25,
            "description": "Meister von Natur und Erde"
        }
    }
}


# =============================================================================
# SYNTHESIS SYSTEM CLASS
# =============================================================================

class SlimeSynthesisSystem:
    """
    Synthese-System basierend auf Dragon Quest Monsters

    Hauptfunktionen:
    - 2 Slimes fusionieren → 1 neuer Slime
    - Plus-Wert berechnen (+N)
    - Skills vererben
    - Legendaere Synthesen (4-Eltern)
    """

    MIN_LEVEL = 10  # Minimum Level fuer Synthese

    def __init__(self):
        self.slime_system = get_slime_system()

    def check_synthesis(self, slime1_id: str, slime2_id: str) -> Dict[str, Any]:
        """
        Prueft ob zwei Slimes fusioniert werden koennen

        Returns:
            Dict mit moeglichen Ergebnissen
        """
        slime1 = self.slime_system.get_slime(slime1_id)
        slime2 = self.slime_system.get_slime(slime2_id)

        if not slime1 or not slime2:
            return {"can_synthesize": False, "reason": "Slime nicht gefunden"}

        if not slime1.get("is_alive") or not slime2.get("is_alive"):
            return {"can_synthesize": False, "reason": "Einer der Slimes ist tot"}

        if slime1["level"] < self.MIN_LEVEL or slime2["level"] < self.MIN_LEVEL:
            return {
                "can_synthesize": False,
                "reason": f"Beide Slimes muessen mindestens Level {self.MIN_LEVEL} sein",
                "slime1_level": slime1["level"],
                "slime2_level": slime2["level"]
            }

        # Berechne moegliches Ergebnis
        result = self._calculate_synthesis_result(slime1, slime2)

        return {
            "can_synthesize": True,
            "slime1": {
                "id": slime1["id"],
                "name": slime1["name"],
                "type": slime1["slime_type"],
                "level": slime1["level"],
                "plus_value": slime1["plus_value"]
            },
            "slime2": {
                "id": slime2["id"],
                "name": slime2["name"],
                "type": slime2["slime_type"],
                "level": slime2["level"],
                "plus_value": slime2["plus_value"]
            },
            "result": result,
            "warning": "ACHTUNG: Beide Eltern-Slimes werden bei der Synthese GELOESCHT!"
        }

    def _calculate_synthesis_result(self, slime1: Dict, slime2: Dict) -> Dict[str, Any]:
        """Berechnet das Synthese-Ergebnis"""
        type1 = slime1["slime_type"]
        type2 = slime2["slime_type"]

        # Plus-Wert: Hoechster Eltern-Wert + 1
        plus1 = slime1.get("plus_value", 0)
        plus2 = slime2.get("plus_value", 0)
        new_plus = max(plus1, plus2) + 1

        # Skills kombinieren (max 4)
        skills1 = slime1.get("skills", [])
        skills2 = slime2.get("skills", [])
        inherited_skills = list(set(skills1 + skills2))[:3]  # Max 3 vererbt

        # Bestimme Ergebnis-Typ
        result_type = None
        result_name = None
        result_color = None
        is_legendary = False
        new_skills = []

        # Check: Gleiche Typen
        if type1 == type2:
            result_type = type1
            result_name = f"{type1.replace('_schleim', '').capitalize()}-Schleim (+{new_plus})"
            result_color = SLIME_COLORS.get(SlimeType(type1), "#888888")
            new_skills = inherited_skills

        # Check: Basis-Hybrid
        else:
            type_set = frozenset({type1, type2})
            if type_set in BASIC_SYNTHESIS:
                hybrid_type = BASIC_SYNTHESIS[type_set]
                hybrid_data = HYBRID_SLIMES.get(hybrid_type, {})
                result_type = hybrid_type
                result_name = hybrid_data.get("name", f"Hybrid-Schleim (+{new_plus})")
                result_color = hybrid_data.get("color", "#888888")
                new_skills = hybrid_data.get("base_skills", [])[:1] + inherited_skills[:2]

            # Check: Legendaere Synthese (Hybrid + Hybrid)
            elif type_set in [frozenset(k) for k in LEGENDARY_SYNTHESIS.keys()]:
                for key, data in LEGENDARY_SYNTHESIS.items():
                    if type_set == frozenset(key):
                        legendary_type = data["result"]
                        legendary_data = LEGENDARY_SLIMES.get(legendary_type, {})
                        result_type = legendary_type
                        result_name = legendary_data.get("name", f"Legendaer-Schleim (+{new_plus})")
                        result_color = legendary_data.get("color", "rainbow")
                        new_skills = legendary_data.get("base_skills", [])
                        is_legendary = True
                        break

            # Fallback: Random Eltern-Typ
            else:
                result_type = random.choice([type1, type2])
                result_name = f"Misch-Schleim (+{new_plus})"
                result_color = SLIME_COLORS.get(SlimeType(result_type) if result_type in [t.value for t in SlimeType] else None, "#888888")
                new_skills = inherited_skills

        return {
            "type": result_type,
            "name": result_name,
            "color": result_color,
            "plus_value": new_plus,
            "skills": list(set(new_skills))[:4],  # Max 4 Skills
            "is_legendary": is_legendary,
            "inherited_from": [slime1["id"], slime2["id"]]
        }

    def synthesize(self, slime1_id: str, slime2_id: str, new_name: str = None) -> Dict[str, Any]:
        """
        Fuehrt Synthese durch

        WICHTIG: Beide Eltern-Slimes werden GELOESCHT!

        Args:
            slime1_id: ID des ersten Slimes
            slime2_id: ID des zweiten Slimes
            new_name: Optionaler Name fuer neuen Slime

        Returns:
            Ergebnis der Synthese
        """
        check = self.check_synthesis(slime1_id, slime2_id)
        if not check.get("can_synthesize"):
            return {"success": False, "message": check.get("reason", "Synthese nicht moeglich")}

        result_data = check["result"]
        slime1_data = check["slime1"]
        slime2_data = check["slime2"]

        # Neuen Slime erstellen
        new_slime = SlimeState(
            name=new_name or result_data["name"],
            slime_type=result_data["type"],
            stage=EvolutionStage.REIF.value,  # Synthese-Slimes starten als Reif (Stage 4)
            level=1,  # Startet bei Level 1
            plus_value=result_data["plus_value"],
            skills=result_data["skills"],
            inherited_from=result_data["inherited_from"],
            # Reset Care Stats
            hunger_hearts=4,
            strength_hearts=4,
            care_mistakes=0,
            effort_hearts=0,
        )

        # Eltern-Slimes LOESCHEN
        if slime1_id in self.slime_system.slimes:
            del self.slime_system.slimes[slime1_id]
        if slime2_id in self.slime_system.slimes:
            del self.slime_system.slimes[slime2_id]

        # Neuen Slime hinzufuegen
        self.slime_system.slimes[new_slime.id] = new_slime

        # Als aktiv setzen
        self.slime_system.set_active_slime(new_slime.id)

        self.slime_system.save()

        return {
            "success": True,
            "message": f"SYNTHESE ERFOLGREICH! {slime1_data['name']} + {slime2_data['name']} = {new_slime.name}!",
            "sacrificed": [slime1_data["name"], slime2_data["name"]],
            "new_slime": new_slime.to_dict(),
            "is_legendary": result_data.get("is_legendary", False)
        }

    def get_recipes(self) -> Dict[str, Any]:
        """Gibt alle bekannten Synthese-Rezepte zurueck"""
        recipes = []

        # Basis-Rezepte
        for types, result in BASIC_SYNTHESIS.items():
            type_list = list(types)
            hybrid_data = HYBRID_SLIMES.get(result, {})
            recipes.append({
                "type": "basic",
                "parent1": type_list[0] if len(type_list) > 0 else None,
                "parent2": type_list[1] if len(type_list) > 1 else None,
                "result": result,
                "result_name": hybrid_data.get("name", result),
                "result_color": hybrid_data.get("color", "#888888"),
                "description": hybrid_data.get("passive_bonus", {}).get("description", "")
            })

        # Legendaere Rezepte
        for types, data in LEGENDARY_SYNTHESIS.items():
            type_set = frozenset(types) if not isinstance(types, frozenset) else types
            type_list = list(type_set)
            legendary_data = LEGENDARY_SLIMES.get(data["result"], {})
            recipes.append({
                "type": "legendary",
                "parent1": type_list[0] if len(type_list) > 0 else None,
                "parent2": type_list[1] if len(type_list) > 1 else None,
                "result": data["result"],
                "result_name": legendary_data.get("name", data["result"]),
                "result_color": legendary_data.get("color", "rainbow"),
                "description": legendary_data.get("passive_bonus", {}).get("description", ""),
                "grandparents": data.get("requirements", {}).get("grandparents", [])
            })

        return {
            "recipes": recipes,
            "basic_count": len(BASIC_SYNTHESIS),
            "legendary_count": len(LEGENDARY_SYNTHESIS),
            "min_level": self.MIN_LEVEL
        }

    def get_possible_syntheses(self) -> List[Dict[str, Any]]:
        """Gibt alle moeglichen Synthesen mit aktuellen Slimes zurueck"""
        slimes = self.slime_system.get_all_slimes()
        eligible = [s for s in slimes if s["level"] >= self.MIN_LEVEL and s["is_alive"]]

        possible = []
        seen = set()

        for i, s1 in enumerate(eligible):
            for j, s2 in enumerate(eligible):
                if i >= j:  # Keine Duplikate
                    continue

                pair = frozenset({s1["id"], s2["id"]})
                if pair in seen:
                    continue
                seen.add(pair)

                check = self.check_synthesis(s1["id"], s2["id"])
                if check.get("can_synthesize"):
                    possible.append({
                        "slime1": s1,
                        "slime2": s2,
                        "result": check["result"]
                    })

        return possible


# =============================================================================
# SINGLETON
# =============================================================================

_synthesis_system: Optional[SlimeSynthesisSystem] = None

def get_synthesis_system() -> SlimeSynthesisSystem:
    """Gibt Singleton zurueck"""
    global _synthesis_system
    if _synthesis_system is None:
        _synthesis_system = SlimeSynthesisSystem()
    return _synthesis_system


# =============================================================================
# API ENDPOINTS (Add to slime_companion.py)
# =============================================================================

def register_synthesis_routes(slime_bp):
    """
    Registriert Synthese-Routes beim Slime Blueprint

    Sollte in api/slime_companion.py aufgerufen werden:
        from najika_slime_synthesis import register_synthesis_routes
        register_synthesis_routes(slime_bp)
    """
    from flask import jsonify, request

    @slime_bp.route('/synthesis/check', methods=['POST'])
    def check_synthesis():
        """
        Prueft ob Synthese moeglich ist

        POST /api/slime/synthesis/check
        Body: {
            "slime1_id": "uuid",
            "slime2_id": "uuid"
        }
        """
        data = request.get_json() or {}
        slime1_id = data.get("slime1_id")
        slime2_id = data.get("slime2_id")

        if not slime1_id or not slime2_id:
            return jsonify({"success": False, "error": "Beide slime IDs erforderlich"})

        system = get_synthesis_system()
        result = system.check_synthesis(slime1_id, slime2_id)

        return jsonify({"success": True, **result})

    @slime_bp.route('/synthesize', methods=['POST'])
    def synthesize():
        """
        Fuehrt Synthese durch

        POST /api/slime/synthesize
        Body: {
            "slime1_id": "uuid",
            "slime2_id": "uuid",
            "name": "Neuer Name"  (optional)
        }

        WARNUNG: Beide Eltern-Slimes werden GELOESCHT!
        """
        data = request.get_json() or {}
        slime1_id = data.get("slime1_id")
        slime2_id = data.get("slime2_id")
        new_name = data.get("name")

        if not slime1_id or not slime2_id:
            return jsonify({"success": False, "error": "Beide slime IDs erforderlich"})

        system = get_synthesis_system()
        result = system.synthesize(slime1_id, slime2_id, new_name)

        return jsonify(result)

    @slime_bp.route('/synthesis/recipes', methods=['GET'])
    def get_recipes():
        """
        Gibt alle bekannten Rezepte zurueck

        GET /api/slime/synthesis/recipes
        """
        system = get_synthesis_system()
        return jsonify({"success": True, **system.get_recipes()})

    @slime_bp.route('/synthesis/possible', methods=['GET'])
    def get_possible():
        """
        Gibt moegliche Synthesen mit aktuellen Slimes zurueck

        GET /api/slime/synthesis/possible
        """
        system = get_synthesis_system()
        possible = system.get_possible_syntheses()

        return jsonify({
            "success": True,
            "possible_syntheses": possible,
            "count": len(possible)
        })


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA SLIME SYNTHESIS SYSTEM - TEST")
    print("=" * 60)

    from najika_slime_system import SlimeType, get_slime_system

    slime_sys = get_slime_system()
    synth_sys = get_synthesis_system()

    # Test: Zwei Slimes erstellen
    print("\n[TEST] Erstelle zwei Test-Slimes...")
    slime1 = slime_sys.create_egg(SlimeType.MOOS, "Moosy")
    slime2 = slime_sys.create_egg(SlimeType.WASSER, "Aqua")

    # Level auf 10 setzen
    slime_sys.slimes[slime1.id].level = 10
    slime_sys.slimes[slime2.id].level = 10
    slime_sys.save()

    print(f"  Slime 1: {slime1.name} (Level 10, {slime1.slime_type})")
    print(f"  Slime 2: {slime2.name} (Level 10, {slime2.slime_type})")

    # Check Synthese
    print("\n[TEST] Check Synthese...")
    check = synth_sys.check_synthesis(slime1.id, slime2.id)
    print(f"  Moeglich: {check.get('can_synthesize')}")
    if check.get("can_synthesize"):
        result = check["result"]
        print(f"  Ergebnis: {result['name']}")
        print(f"  Plus-Wert: +{result['plus_value']}")
        print(f"  Skills: {result['skills']}")
        print(f"  Legendaer: {result['is_legendary']}")

    # Synthese durchfuehren
    print("\n[TEST] Synthese durchfuehren...")
    result = synth_sys.synthesize(slime1.id, slime2.id, "Sumpfi")
    if result["success"]:
        print(f"  {result['message']}")
        print(f"  Neuer Slime: {result['new_slime']['name']}")
        print(f"  Typ: {result['new_slime']['slime_type']}")
    else:
        print(f"  Fehlgeschlagen: {result['message']}")

    # Rezepte anzeigen
    print("\n[TEST] Verfuegbare Rezepte...")
    recipes = synth_sys.get_recipes()
    print(f"  Basis-Rezepte: {recipes['basic_count']}")
    print(f"  Legendaere Rezepte: {recipes['legendary_count']}")

    print("\n" + "=" * 60)
    print("TEST ABGESCHLOSSEN")
    print("=" * 60)
