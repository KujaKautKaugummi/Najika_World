#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA WORLD - Slime Evolution System
=====================================
Basiert auf Digimon V-Pet Mechanik:
- 6 Evolution-Stufen
- Care Mistakes beeinflussen Evolution-Pfad
- Effort Hearts fuer beste Evolutionen
- Zeit-basierte Evolution

Erstellt: 2026-01-28
"""

import time
import random
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass

from najika_slime_system import (
    SlimeState, SlimeType, EvolutionStage,
    EVOLUTION_TIMES, get_slime_system
)


# =============================================================================
# EVOLUTION PATHS
# =============================================================================

class EvolutionPath(Enum):
    """Evolution-Pfade basierend auf Pflege"""
    PERFECT = "perfect"      # 0 Care Mistakes
    GOOD = "good"           # 1-2 Care Mistakes
    NORMAL = "normal"       # 3-5 Care Mistakes
    BAD = "bad"             # 6+ Care Mistakes
    SPECIAL = "special"     # Spezielle Bedingungen


# Evolution Requirements pro Stage und Pfad
# Format: {stage: {path: {requirements}}}
EVOLUTION_REQUIREMENTS = {
    # Stage 2 (Baby) -> Stage 3 (Kind)
    2: {
        EvolutionPath.PERFECT: {
            "care_mistakes_max": 0,
            "effort_hearts_min": 4,
            "description": "Perfekte Pflege!"
        },
        EvolutionPath.GOOD: {
            "care_mistakes_max": 2,
            "effort_hearts_min": 2,
            "description": "Gute Pflege"
        },
        EvolutionPath.NORMAL: {
            "care_mistakes_max": 5,
            "effort_hearts_min": 0,
            "description": "Normale Pflege"
        },
        EvolutionPath.BAD: {
            "care_mistakes_max": 999,
            "effort_hearts_min": 0,
            "description": "Vernachlaessigt..."
        }
    },
    # Stage 3 (Kind) -> Stage 4 (Reif)
    3: {
        EvolutionPath.PERFECT: {
            "care_mistakes_max": 1,
            "effort_hearts_min": 10,
            "win_rate_min": 0.8,  # Optional, nur wenn gekaempft
            "description": "Perfekte Entwicklung!"
        },
        EvolutionPath.GOOD: {
            "care_mistakes_max": 3,
            "effort_hearts_min": 5,
            "description": "Gute Entwicklung"
        },
        EvolutionPath.NORMAL: {
            "care_mistakes_max": 6,
            "effort_hearts_min": 0,
            "description": "Normale Entwicklung"
        },
        EvolutionPath.BAD: {
            "care_mistakes_max": 999,
            "effort_hearts_min": 0,
            "description": "Schwache Entwicklung"
        }
    },
    # Stage 4 (Reif) -> Stage 5 (Champion)
    4: {
        EvolutionPath.PERFECT: {
            "care_mistakes_max": 2,
            "effort_hearts_min": 20,
            "level_min": 15,
            "description": "Champion-Qualitaet!"
        },
        EvolutionPath.GOOD: {
            "care_mistakes_max": 4,
            "effort_hearts_min": 10,
            "level_min": 10,
            "description": "Starker Champion"
        },
        EvolutionPath.NORMAL: {
            "care_mistakes_max": 7,
            "effort_hearts_min": 5,
            "description": "Normaler Champion"
        },
        EvolutionPath.BAD: {
            "care_mistakes_max": 999,
            "effort_hearts_min": 0,
            "description": "Schwacher Champion"
        }
    },
    # Stage 5 (Champion) -> Stage 6 (Ultimativ)
    5: {
        EvolutionPath.PERFECT: {
            "care_mistakes_max": 3,
            "effort_hearts_min": 40,
            "level_min": 25,
            "battles_min": 20,  # Optional
            "description": "ULTIMATIV! Legendaer!"
        },
        EvolutionPath.GOOD: {
            "care_mistakes_max": 5,
            "effort_hearts_min": 25,
            "level_min": 20,
            "description": "Starker Ultimativ"
        },
        EvolutionPath.NORMAL: {
            "care_mistakes_max": 8,
            "effort_hearts_min": 15,
            "description": "Normaler Ultimativ"
        },
        EvolutionPath.BAD: {
            "care_mistakes_max": 999,
            "effort_hearts_min": 0,
            "description": "Schwacher Ultimativ"
        }
    }
}


# Evolution-Formen pro Typ und Pfad
# Format: {slime_type: {stage: {path: form_name}}}
EVOLUTION_FORMS = {
    SlimeType.MOOS.value: {
        3: {
            EvolutionPath.PERFECT: "Wald-Geist",
            EvolutionPath.GOOD: "Moos-Krieger",
            EvolutionPath.NORMAL: "Gruener Schleim",
            EvolutionPath.BAD: "Fauler Schleim"
        },
        4: {
            EvolutionPath.PERFECT: "Druiden-Schleim",
            EvolutionPath.GOOD: "Waldlaeufer-Schleim",
            EvolutionPath.NORMAL: "Grosser Moos-Schleim",
            EvolutionPath.BAD: "Verrotteter Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Natur-Geist",
            EvolutionPath.GOOD: "Wald-Beschuetzer",
            EvolutionPath.NORMAL: "Champion Moos",
            EvolutionPath.BAD: "Sumpf-Schleim"
        },
        6: {
            EvolutionPath.PERFECT: "Yggdrasil-Schleim",
            EvolutionPath.GOOD: "Wald-Titan",
            EvolutionPath.NORMAL: "Ultimativer Moos",
            EvolutionPath.BAD: "Gift-Moos"
        }
    },
    SlimeType.FROST.value: {
        3: {
            EvolutionPath.PERFECT: "Eis-Geist",
            EvolutionPath.GOOD: "Frost-Krieger",
            EvolutionPath.NORMAL: "Eis-Schleim",
            EvolutionPath.BAD: "Matsch-Schleim"
        },
        4: {
            EvolutionPath.PERFECT: "Blizzard-Schleim",
            EvolutionPath.GOOD: "Gletscher-Schleim",
            EvolutionPath.NORMAL: "Grosser Frost",
            EvolutionPath.BAD: "Schmelz-Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Eis-Drache-Schleim",
            EvolutionPath.GOOD: "Frost-Ritter",
            EvolutionPath.NORMAL: "Champion Frost",
            EvolutionPath.BAD: "Kalt-Schleim"
        },
        6: {
            EvolutionPath.PERFECT: "Ewiger-Frost-Schleim",
            EvolutionPath.GOOD: "Eis-Titan",
            EvolutionPath.NORMAL: "Ultimativer Frost",
            EvolutionPath.BAD: "Schnee-Schleim"
        }
    },
    SlimeType.WASSER.value: {
        3: {
            EvolutionPath.PERFECT: "Wellen-Geist",
            EvolutionPath.GOOD: "Strom-Schleim",
            EvolutionPath.NORMAL: "Wasser-Schleim",
            EvolutionPath.BAD: "Pfuetzen-Schleim"
        },
        4: {
            EvolutionPath.PERFECT: "Ozean-Schleim",
            EvolutionPath.GOOD: "Flut-Schleim",
            EvolutionPath.NORMAL: "Grosser Wasser",
            EvolutionPath.BAD: "Trueber Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Leviathan-Schleim",
            EvolutionPath.GOOD: "Tiefsee-Schleim",
            EvolutionPath.NORMAL: "Champion Wasser",
            EvolutionPath.BAD: "Sumpf-Wasser"
        },
        6: {
            EvolutionPath.PERFECT: "Poseidon-Schleim",
            EvolutionPath.GOOD: "Ozean-Titan",
            EvolutionPath.NORMAL: "Ultimativer Wasser",
            EvolutionPath.BAD: "Teich-Schleim"
        }
    },
    SlimeType.BLITZ.value: {
        3: {
            EvolutionPath.PERFECT: "Donner-Geist",
            EvolutionPath.GOOD: "Blitz-Krieger",
            EvolutionPath.NORMAL: "Elektro-Schleim",
            EvolutionPath.BAD: "Statik-Schleim"
        },
        4: {
            EvolutionPath.PERFECT: "Sturm-Schleim",
            EvolutionPath.GOOD: "Gewitter-Schleim",
            EvolutionPath.NORMAL: "Grosser Blitz",
            EvolutionPath.BAD: "Funken-Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Raijin-Schleim",
            EvolutionPath.GOOD: "Donner-Drache",
            EvolutionPath.NORMAL: "Champion Blitz",
            EvolutionPath.BAD: "Schwach-Strom"
        },
        6: {
            EvolutionPath.PERFECT: "Zeus-Schleim",
            EvolutionPath.GOOD: "Blitz-Titan",
            EvolutionPath.NORMAL: "Ultimativer Blitz",
            EvolutionPath.BAD: "Entladen-Schleim"
        }
    },
    SlimeType.GIFT.value: {
        3: {
            EvolutionPath.PERFECT: "Gift-Geist",
            EvolutionPath.GOOD: "Toxin-Schleim",
            EvolutionPath.NORMAL: "Gift-Schleim",
            EvolutionPath.BAD: "Schwach-Gift"
        },
        4: {
            EvolutionPath.PERFECT: "Venom-Schleim",
            EvolutionPath.GOOD: "Seuchen-Schleim",
            EvolutionPath.NORMAL: "Grosser Gift",
            EvolutionPath.BAD: "Verdorbener Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Basilisk-Schleim",
            EvolutionPath.GOOD: "Gift-Hydra",
            EvolutionPath.NORMAL: "Champion Gift",
            EvolutionPath.BAD: "Faeulnis-Schleim"
        },
        6: {
            EvolutionPath.PERFECT: "Nidhogg-Schleim",
            EvolutionPath.GOOD: "Gift-Titan",
            EvolutionPath.NORMAL: "Ultimativer Gift",
            EvolutionPath.BAD: "Schwach-Toxin"
        }
    },
    SlimeType.MAGMA.value: {
        3: {
            EvolutionPath.PERFECT: "Feuer-Geist",
            EvolutionPath.GOOD: "Flammen-Schleim",
            EvolutionPath.NORMAL: "Lava-Schleim",
            EvolutionPath.BAD: "Glut-Schleim"
        },
        4: {
            EvolutionPath.PERFECT: "Inferno-Schleim",
            EvolutionPath.GOOD: "Vulkan-Schleim",
            EvolutionPath.NORMAL: "Grosser Magma",
            EvolutionPath.BAD: "Asche-Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Phoenix-Schleim",
            EvolutionPath.GOOD: "Feuer-Drache",
            EvolutionPath.NORMAL: "Champion Magma",
            EvolutionPath.BAD: "Erkalteter Schleim"
        },
        6: {
            EvolutionPath.PERFECT: "Ifrit-Schleim",
            EvolutionPath.GOOD: "Magma-Titan",
            EvolutionPath.NORMAL: "Ultimativer Magma",
            EvolutionPath.BAD: "Schwach-Feuer"
        }
    },
    SlimeType.SAND.value: {
        3: {
            EvolutionPath.PERFECT: "Wuesten-Geist",
            EvolutionPath.GOOD: "Duenen-Schleim",
            EvolutionPath.NORMAL: "Sand-Schleim",
            EvolutionPath.BAD: "Staub-Schleim"
        },
        4: {
            EvolutionPath.PERFECT: "Oasen-Schleim",
            EvolutionPath.GOOD: "Sturm-Sand",
            EvolutionPath.NORMAL: "Grosser Sand",
            EvolutionPath.BAD: "Trockener Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Sphinx-Schleim",
            EvolutionPath.GOOD: "Wuesten-Krieger",
            EvolutionPath.NORMAL: "Champion Sand",
            EvolutionPath.BAD: "Schwach-Sand"
        },
        6: {
            EvolutionPath.PERFECT: "Anubis-Schleim",
            EvolutionPath.GOOD: "Sand-Titan",
            EvolutionPath.NORMAL: "Ultimativer Sand",
            EvolutionPath.BAD: "Verweht-Schleim"
        }
    },
    SlimeType.KRISTALL.value: {
        3: {
            EvolutionPath.PERFECT: "Kristall-Geist",
            EvolutionPath.GOOD: "Edelstein-Schleim",
            EvolutionPath.NORMAL: "Kristall-Schleim",
            EvolutionPath.BAD: "Trueber Kristall"
        },
        4: {
            EvolutionPath.PERFECT: "Diamant-Schleim",
            EvolutionPath.GOOD: "Prisma-Schleim",
            EvolutionPath.NORMAL: "Grosser Kristall",
            EvolutionPath.BAD: "Bruch-Kristall"
        },
        5: {
            EvolutionPath.PERFECT: "Quarz-Drache",
            EvolutionPath.GOOD: "Leucht-Kristall",
            EvolutionPath.NORMAL: "Champion Kristall",
            EvolutionPath.BAD: "Stumpf-Kristall"
        },
        6: {
            EvolutionPath.PERFECT: "Weltenkristall",
            EvolutionPath.GOOD: "Kristall-Titan",
            EvolutionPath.NORMAL: "Ultimativer Kristall",
            EvolutionPath.BAD: "Verblasst-Kristall"
        }
    },
    SlimeType.GOETTER.value: {
        3: {
            EvolutionPath.PERFECT: "Heiliger Geist",
            EvolutionPath.GOOD: "Goetter-Kind",
            EvolutionPath.NORMAL: "Regenbogen-Schleim",
            EvolutionPath.BAD: "Verblasster Schleim"
        },
        4: {
            EvolutionPath.PERFECT: "Engel-Schleim",
            EvolutionPath.GOOD: "Himmels-Schleim",
            EvolutionPath.NORMAL: "Grosser Goetter",
            EvolutionPath.BAD: "Gefallener Schleim"
        },
        5: {
            EvolutionPath.PERFECT: "Seraph-Schleim",
            EvolutionPath.GOOD: "Goetterbote",
            EvolutionPath.NORMAL: "Champion Goetter",
            EvolutionPath.BAD: "Schwacher Goetter"
        },
        6: {
            EvolutionPath.PERFECT: "Gott-Schleim",
            EvolutionPath.GOOD: "Goetter-Titan",
            EvolutionPath.NORMAL: "Ultimativer Goetter",
            EvolutionPath.BAD: "Sterblicher Schleim"
        }
    }
}


# =============================================================================
# EVOLUTION SYSTEM CLASS
# =============================================================================

class SlimeEvolutionSystem:
    """
    Evolution-System basierend auf Digimon V-Pet Mechanik
    """

    def __init__(self):
        self.slime_system = get_slime_system()

    def check_evolution_ready(self, slime_id: str) -> Dict[str, Any]:
        """
        Prueft ob ein Slime zur Evolution bereit ist

        Returns:
            Dict mit Status und moeglichen Pfaden
        """
        slime_data = self.slime_system.get_slime(slime_id)
        if not slime_data:
            return {"ready": False, "reason": "Slime nicht gefunden"}

        current_stage = slime_data["stage"]
        if current_stage >= 6:
            return {"ready": False, "reason": "Bereits maximale Stufe"}

        # Zeit-Check (Digimon V-Pet: Evolution braucht Zeit)
        if not slime_data.get("can_evolve", False):
            remaining = slime_data.get("evolution_time", 0) - time.time()
            hours = max(0, remaining / 3600)
            return {
                "ready": False,
                "reason": f"Noch {hours:.1f} Stunden bis zur Evolution",
                "remaining_hours": hours
            }

        # Ermittle moegliche Pfade
        possible_paths = self._get_possible_paths(slime_data)

        return {
            "ready": True,
            "current_stage": current_stage,
            "next_stage": current_stage + 1,
            "possible_paths": possible_paths,
            "recommended_path": possible_paths[0] if possible_paths else None
        }

    def _get_possible_paths(self, slime_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Ermittelt moegliche Evolution-Pfade basierend auf Stats"""
        current_stage = slime_data["stage"]
        requirements = EVOLUTION_REQUIREMENTS.get(current_stage, {})

        paths = []
        care_mistakes = slime_data.get("care_mistakes", 0)
        effort_hearts = slime_data.get("effort_hearts", 0)
        level = slime_data.get("level", 1)
        battles = slime_data.get("battles", 0)
        win_rate = slime_data.get("win_rate", 0)

        for path, reqs in requirements.items():
            # Check Care Mistakes
            if care_mistakes > reqs.get("care_mistakes_max", 999):
                continue

            # Check Effort Hearts
            if effort_hearts < reqs.get("effort_hearts_min", 0):
                continue

            # Check Level (optional)
            if level < reqs.get("level_min", 0):
                continue

            # Check Battles (optional, nur wenn requirement existiert UND gekaempft wurde)
            if "battles_min" in reqs and battles > 0:
                if battles < reqs["battles_min"]:
                    continue

            # Check Win Rate (optional, nur wenn gekaempft)
            if "win_rate_min" in reqs and battles > 0:
                if win_rate < reqs["win_rate_min"]:
                    continue

            # Pfad ist moeglich!
            slime_type = slime_data.get("slime_type", SlimeType.MOOS.value)
            form_name = self._get_evolution_form(slime_type, current_stage + 1, path)

            paths.append({
                "path": path.value,
                "description": reqs.get("description", ""),
                "form_name": form_name,
                "requirements_met": True
            })

        # Fallback: Immer mindestens BAD Pfad moeglich
        if not paths:
            bad_form = self._get_evolution_form(
                slime_data.get("slime_type", SlimeType.MOOS.value),
                current_stage + 1,
                EvolutionPath.BAD
            )
            paths.append({
                "path": EvolutionPath.BAD.value,
                "description": "Schwache Entwicklung",
                "form_name": bad_form,
                "requirements_met": True
            })

        return paths

    def _get_evolution_form(self, slime_type: str, stage: int, path: EvolutionPath) -> str:
        """Gibt den Namen der Evolution-Form zurueck"""
        type_forms = EVOLUTION_FORMS.get(slime_type, {})
        stage_forms = type_forms.get(stage, {})
        return stage_forms.get(path, f"Stufe-{stage} Schleim")

    def evolve(self, slime_id: str, chosen_path: str = None) -> Dict[str, Any]:
        """
        Fuehrt Evolution durch

        Args:
            slime_id: ID des Slimes
            chosen_path: Gewaehlter Pfad (optional, sonst bester moeglicher)

        Returns:
            Ergebnis der Evolution
        """
        check = self.check_evolution_ready(slime_id)
        if not check.get("ready"):
            return {"success": False, "message": check.get("reason", "Nicht bereit")}

        slime = self.slime_system.slimes.get(slime_id)
        if not slime:
            return {"success": False, "message": "Slime nicht gefunden"}

        # Waehle Pfad
        possible_paths = check.get("possible_paths", [])
        selected_path = None

        if chosen_path:
            for p in possible_paths:
                if p["path"] == chosen_path:
                    selected_path = p
                    break
        else:
            # Bester moeglicher Pfad
            selected_path = possible_paths[0] if possible_paths else None

        if not selected_path:
            return {"success": False, "message": "Ungueltiger Evolution-Pfad"}

        # Evolution durchfuehren!
        old_stage = slime.stage
        old_name = slime.name

        slime.stage += 1

        # Neuer Name basierend auf Form
        new_form = selected_path["form_name"]
        slime.name = new_form

        # Stats-Bonus bei Evolution
        slime.level += 2

        # Naechste Evolution-Zeit setzen
        next_stage = EvolutionStage(slime.stage + 1) if slime.stage < 6 else None
        if next_stage:
            slime.evolution_time = time.time() + EVOLUTION_TIMES.get(next_stage, 999999)
        else:
            slime.evolution_time = 0  # Keine weitere Evolution

        # Neuer Skill bei Evolution
        new_skill = self._get_evolution_skill(slime.slime_type, slime.stage)
        if new_skill and new_skill not in slime.skills:
            slime.skills.append(new_skill)

        self.slime_system.save()

        return {
            "success": True,
            "message": f"EVOLUTION! {old_name} hat sich zu {new_form} entwickelt!",
            "old_stage": old_stage,
            "new_stage": slime.stage,
            "old_name": old_name,
            "new_form": new_form,
            "path": selected_path["path"],
            "new_skill": new_skill,
            "slime": slime.to_dict()
        }

    def _get_evolution_skill(self, slime_type: str, stage: int) -> Optional[str]:
        """Gibt neuen Skill fuer Evolution zurueck"""
        evolution_skills = {
            SlimeType.MOOS.value: {
                3: "nature_blessing",
                4: "forest_armor",
                5: "life_drain",
                6: "yggdrasil_root"
            },
            SlimeType.FROST.value: {
                3: "ice_shield",
                4: "blizzard",
                5: "absolute_zero",
                6: "eternal_frost"
            },
            SlimeType.WASSER.value: {
                3: "tidal_wave",
                4: "whirlpool",
                5: "tsunami",
                6: "ocean_wrath"
            },
            SlimeType.BLITZ.value: {
                3: "chain_lightning",
                4: "thunder_storm",
                5: "raijin_strike",
                6: "divine_thunder"
            },
            SlimeType.GIFT.value: {
                3: "toxic_cloud",
                4: "venom_surge",
                5: "plague",
                6: "death_touch"
            },
            SlimeType.MAGMA.value: {
                3: "lava_burst",
                4: "eruption",
                5: "meteor",
                6: "hellfire"
            },
            SlimeType.SAND.value: {
                3: "sand_storm",
                4: "quicksand",
                5: "desert_mirage",
                6: "time_erosion"
            },
            SlimeType.KRISTALL.value: {
                3: "prism_beam",
                4: "crystal_prison",
                5: "rainbow_refraction",
                6: "singularity"
            },
            SlimeType.GOETTER.value: {
                3: "holy_light",
                4: "divine_protection",
                5: "miracle",
                6: "genesis"
            }
        }

        type_skills = evolution_skills.get(slime_type, {})
        return type_skills.get(stage)


# =============================================================================
# SINGLETON
# =============================================================================

_evolution_system: Optional[SlimeEvolutionSystem] = None

def get_evolution_system() -> SlimeEvolutionSystem:
    """Gibt Singleton zurueck"""
    global _evolution_system
    if _evolution_system is None:
        _evolution_system = SlimeEvolutionSystem()
    return _evolution_system


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA SLIME EVOLUTION SYSTEM - TEST")
    print("=" * 60)

    from najika_slime_system import SlimeType, get_slime_system

    slime_sys = get_slime_system()
    evo_sys = get_evolution_system()

    # Test: Neuen Slime erstellen
    print("\n[TEST] Erstelle Test-Slime...")
    slime = slime_sys.create_egg(SlimeType.FROST, "Frosty")
    print(f"  Erstellt: {slime.name}")

    # Simuliere gute Pflege
    slime.stage = 2  # Baby
    slime.care_mistakes = 0
    slime.effort_hearts = 10
    slime.level = 5
    slime.evolution_time = time.time() - 1  # Sofort bereit
    slime_sys.save()

    # Check Evolution
    print("\n[TEST] Check Evolution...")
    check = evo_sys.check_evolution_ready(slime.id)
    print(f"  Bereit: {check.get('ready')}")
    if check.get("ready"):
        print(f"  Moegliche Pfade:")
        for path in check.get("possible_paths", []):
            print(f"    - {path['path']}: {path['form_name']} ({path['description']})")

    # Evolution!
    print("\n[TEST] Evolution durchfuehren...")
    result = evo_sys.evolve(slime.id)
    if result["success"]:
        print(f"  {result['message']}")
        print(f"  Neuer Skill: {result.get('new_skill')}")
    else:
        print(f"  Fehlgeschlagen: {result['message']}")

    print("\n" + "=" * 60)
    print("TEST ABGESCHLOSSEN")
    print("=" * 60)
