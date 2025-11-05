"""
Najika Skill System - Use-Based Progression (Skyrim-Style)
===========================================================

Skill-Kategorien:
- Combat Skills: Schwertkampf, Bogenschießen, Blocken, etc.
- Crafting Skills: Schmiedekunst, Alchemie, Verzauberung, Kochen
- Gathering Skills: Bergbau, Holzfällen, Kräuterkunde, Angeln
- Social Skills: Handel, Überreden, Einschüchtern, Charisma
- Stealth Skills: Schleichen, Taschendiebstahl, Schlösser knacken
- Survival Skills: Jagen, Spurenlesen, Erste Hilfe, Camping

Progression System:
- Skills steigen durch NUTZUNG (wie in Skyrim)
- Level 1-100 pro Skill
- Passive Boni steigen mit Skill-Level
- Manche Skills benötigen Voraussetzungen
- XP-basiertes Leveling: Jede Nutzung gibt XP
"""

from typing import Dict, List, Optional
import json
import math
import random


# ===== SKILL DATABASE =====

SKILL_CATEGORIES = {
    "combat": {
        "name": "Kampf-Fähigkeiten",
        "color": "#FF4444",
        "icon": "⚔️"
    },
    "crafting": {
        "name": "Handwerks-Fähigkeiten",
        "color": "#FF8800",
        "icon": "🔨"
    },
    "gathering": {
        "name": "Sammel-Fähigkeiten",
        "color": "#44FF44",
        "icon": "🌿"
    },
    "social": {
        "name": "Soziale Fähigkeiten",
        "color": "#4444FF",
        "icon": "💬"
    },
    "stealth": {
        "name": "Heimlichkeits-Fähigkeiten",
        "color": "#8844FF",
        "icon": "🥷"
    },
    "survival": {
        "name": "Überlebens-Fähigkeiten",
        "color": "#FF4488",
        "icon": "🏕️"
    }
}


# ===== COMBAT SKILLS =====

COMBAT_SKILLS = {
    "one_handed": {
        "name": "Einhandwaffen",
        "category": "combat",
        "description": "Fähigkeit mit einhandigen Waffen (Schwerter, Äxte, Keulen)",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "weapon_damage_percent": 0.5,  # +0.5% pro Level
            "attack_speed_percent": 0.2,   # +0.2% pro Level
            "crit_chance_percent": 0.1     # +0.1% pro Level
        },
        "use_triggers": ["attack_with_one_handed", "kill_with_one_handed"]
    },
    "two_handed": {
        "name": "Zweihandwaffen",
        "category": "combat",
        "description": "Fähigkeit mit zweihandigen Waffen (Großschwerter, Kriegshämmer)",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "weapon_damage_percent": 1.0,   # +1% pro Level
            "stagger_chance_percent": 0.3,  # +0.3% pro Level
            "crit_damage_percent": 0.5      # +0.5% Crit-Schaden
        },
        "use_triggers": ["attack_with_two_handed", "kill_with_two_handed"]
    },
    "archery": {
        "name": "Bogenschießen",
        "category": "combat",
        "description": "Fähigkeit mit Bögen und Armbrüsten",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "ranged_damage_percent": 0.5,
            "accuracy_percent": 0.3,
            "arrow_recovery_percent": 0.2   # Chance Pfeile zurückzugewinnen
        },
        "use_triggers": ["attack_with_bow", "kill_with_bow"]
    },
    "block": {
        "name": "Blocken",
        "category": "combat",
        "description": "Fähigkeit Angriffe mit Schild oder Waffe zu blocken",
        "base_xp_per_use": 3,
        "passive_bonuses": {
            "block_amount_percent": 0.5,    # +0.5% geblockt
            "block_stamina_cost_percent": -0.3,  # -0.3% Ausdauer-Kosten
            "counter_damage_percent": 0.2   # +0.2% Konter-Schaden
        },
        "use_triggers": ["successful_block", "perfect_block"]
    },
    "heavy_armor": {
        "name": "Schwere Rüstung",
        "category": "combat",
        "description": "Fähigkeit schwere Rüstungen effektiv zu tragen",
        "base_xp_per_use": 2,
        "passive_bonuses": {
            "armor_rating_percent": 0.4,
            "movement_penalty_reduction_percent": 0.2,
            "physical_resistance_percent": 0.1
        },
        "use_triggers": ["take_damage_with_heavy_armor", "kill_with_heavy_armor"]
    },
    "light_armor": {
        "name": "Leichte Rüstung",
        "category": "combat",
        "description": "Fähigkeit leichte Rüstungen effektiv zu tragen",
        "base_xp_per_use": 2,
        "passive_bonuses": {
            "armor_rating_percent": 0.3,
            "dodge_chance_percent": 0.2,
            "stamina_regen_percent": 0.1
        },
        "use_triggers": ["take_damage_with_light_armor", "dodge_with_light_armor"]
    },
    "unarmed": {
        "name": "Waffenloser Kampf",
        "category": "combat",
        "description": "Fähigkeit ohne Waffen zu kämpfen",
        "base_xp_per_use": 4,
        "passive_bonuses": {
            "unarmed_damage_flat": 1.0,     # +1 Schaden pro Level
            "attack_speed_percent": 0.3,
            "stun_chance_percent": 0.1
        },
        "use_triggers": ["unarmed_attack", "unarmed_kill"]
    }
}


# ===== CRAFTING SKILLS =====

CRAFTING_SKILLS = {
    "smithing": {
        "name": "Schmiedekunst",
        "category": "crafting",
        "description": "Fähigkeit Waffen und Rüstungen zu schmieden und zu verbessern",
        "base_xp_per_use": 10,
        "passive_bonuses": {
            "crafted_item_quality_percent": 1.0,  # +1% Qualität
            "improvement_effectiveness_percent": 0.5,
            "material_efficiency_percent": 0.2   # -0.2% Material-Verbrauch
        },
        "use_triggers": ["craft_weapon", "craft_armor", "improve_item"],
        "prerequisites": {}
    },
    "alchemy": {
        "name": "Alchemie",
        "category": "crafting",
        "description": "Fähigkeit Tränke und Gifte herzustellen",
        "base_xp_per_use": 8,
        "passive_bonuses": {
            "potion_effectiveness_percent": 0.5,
            "poison_effectiveness_percent": 0.5,
            "ingredient_discovery_chance_percent": 0.1
        },
        "use_triggers": ["craft_potion", "craft_poison", "discover_effect"],
        "prerequisites": {}
    },
    "enchanting": {
        "name": "Verzauberung",
        "category": "crafting",
        "description": "Fähigkeit Gegenstände magisch zu verzaubern",
        "base_xp_per_use": 12,
        "passive_bonuses": {
            "enchantment_strength_percent": 0.5,
            "soul_gem_efficiency_percent": 0.3,
            "double_enchant_chance_percent": 0.05  # Chance auf doppelte Verzauberung
        },
        "use_triggers": ["enchant_item", "disenchant_item"],
        "prerequisites": {"magic_schools_learned": 3}  # Mindestens 3 Magieschulen
    },
    "cooking": {
        "name": "Kochen",
        "category": "crafting",
        "description": "Fähigkeit nahrhafte Mahlzeiten zuzubereiten",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "food_effectiveness_percent": 0.5,
            "buff_duration_percent": 0.3,
            "rare_recipe_discover_chance_percent": 0.1
        },
        "use_triggers": ["cook_food", "cook_gourmet_meal"],
        "prerequisites": {}
    },
    "tailoring": {
        "name": "Schneiderei",
        "category": "crafting",
        "description": "Fähigkeit Kleidung und Stoffrüstungen herzustellen",
        "base_xp_per_use": 7,
        "passive_bonuses": {
            "cloth_armor_quality_percent": 0.8,
            "enchantment_slot_bonus_percent": 0.2,
            "aesthetic_bonus_flat": 0.5  # Aussehen/Fashion
        },
        "use_triggers": ["craft_clothing", "craft_cloth_armor"],
        "prerequisites": {}
    }
}


# ===== GATHERING SKILLS =====

GATHERING_SKILLS = {
    "mining": {
        "name": "Bergbau",
        "category": "gathering",
        "description": "Fähigkeit Erze und Edelsteine abzubauen",
        "base_xp_per_use": 6,
        "passive_bonuses": {
            "ore_yield_percent": 0.3,        # +0.3% mehr Erz
            "rare_gem_chance_percent": 0.1,  # +0.1% seltene Edelsteine
            "mining_speed_percent": 0.2      # +0.2% schneller
        },
        "use_triggers": ["mine_ore", "mine_gem", "break_rock"],
        "prerequisites": {}
    },
    "woodcutting": {
        "name": "Holzfällen",
        "category": "gathering",
        "description": "Fähigkeit Bäume zu fällen und Holz zu sammeln",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "wood_yield_percent": 0.3,
            "rare_wood_chance_percent": 0.1,
            "cutting_speed_percent": 0.2
        },
        "use_triggers": ["chop_tree", "gather_wood"],
        "prerequisites": {}
    },
    "herbalism": {
        "name": "Kräuterkunde",
        "category": "gathering",
        "description": "Fähigkeit Kräuter und Pflanzen zu sammeln und zu identifizieren",
        "base_xp_per_use": 4,
        "passive_bonuses": {
            "herb_yield_percent": 0.4,
            "rare_herb_chance_percent": 0.15,
            "herb_quality_percent": 0.2  # Bessere Qualität für Alchemie
        },
        "use_triggers": ["gather_herb", "identify_plant"],
        "prerequisites": {}
    },
    "fishing": {
        "name": "Angeln",
        "category": "gathering",
        "description": "Fähigkeit Fische zu fangen",
        "base_xp_per_use": 3,
        "passive_bonuses": {
            "fish_size_percent": 0.3,
            "rare_fish_chance_percent": 0.2,
            "catch_speed_percent": 0.1
        },
        "use_triggers": ["catch_fish", "catch_rare_fish"],
        "prerequisites": {}
    },
    "skinning": {
        "name": "Kürschnerei",
        "category": "gathering",
        "description": "Fähigkeit Tiere zu häuten und Leder zu gewinnen",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "leather_yield_percent": 0.4,
            "rare_pelt_chance_percent": 0.15,
            "perfect_skin_chance_percent": 0.1
        },
        "use_triggers": ["skin_animal", "process_hide"],
        "prerequisites": {}
    }
}


# ===== SOCIAL SKILLS =====

SOCIAL_SKILLS = {
    "speech": {
        "name": "Redekunst",
        "category": "social",
        "description": "Fähigkeit andere zu überzeugen und zu beeinflussen",
        "base_xp_per_use": 8,
        "passive_bonuses": {
            "persuasion_chance_percent": 0.5,
            "vendor_prices_percent": -0.2,  # Bessere Preise
            "quest_reward_percent": 0.1     # Bessere Quest-Belohnungen
        },
        "use_triggers": ["persuade_success", "persuade_attempt", "complete_dialogue"],
        "prerequisites": {}
    },
    "barter": {
        "name": "Handel",
        "category": "social",
        "description": "Fähigkeit besser zu handeln und Preise zu verhandeln",
        "base_xp_per_use": 6,
        "passive_bonuses": {
            "buy_price_percent": -0.3,      # -0.3% Kaufpreis
            "sell_price_percent": 0.3,      # +0.3% Verkaufspreis
            "haggle_success_percent": 0.2
        },
        "use_triggers": ["buy_item", "sell_item", "haggle"],
        "prerequisites": {}
    },
    "intimidation": {
        "name": "Einschüchterung",
        "category": "social",
        "description": "Fähigkeit andere durch Furcht zu beeinflussen",
        "base_xp_per_use": 7,
        "passive_bonuses": {
            "intimidate_chance_percent": 0.5,
            "enemy_morale_damage_percent": 0.2,
            "flee_chance_bonus_percent": 0.1  # Gegner fliehen eher
        },
        "use_triggers": ["intimidate_success", "intimidate_attempt"],
        "prerequisites": {"combat_level_min": 10}
    },
    "charisma": {
        "name": "Charisma",
        "category": "social",
        "description": "Natürliche Ausstrahlung und Beliebtheit",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "npc_disposition_flat": 1.0,     # +1 Zuneigung pro Level
            "romance_chance_percent": 0.3,
            "fame_gain_percent": 0.2
        },
        "use_triggers": ["positive_interaction", "help_npc", "flirt"],
        "prerequisites": {}
    }
}


# ===== STEALTH SKILLS =====

STEALTH_SKILLS = {
    "sneak": {
        "name": "Schleichen",
        "category": "stealth",
        "description": "Fähigkeit sich unbemerkt zu bewegen",
        "base_xp_per_use": 4,
        "passive_bonuses": {
            "sneak_effectiveness_percent": 0.5,
            "detection_radius_percent": -0.2,  # -0.2% Entdeckungsreichweite
            "sneak_attack_damage_percent": 0.3
        },
        "use_triggers": ["successful_sneak", "sneak_attack"],
        "prerequisites": {}
    },
    "pickpocket": {
        "name": "Taschendiebstahl",
        "category": "stealth",
        "description": "Fähigkeit anderen unbemerkt Gegenstände zu stehlen",
        "base_xp_per_use": 10,
        "passive_bonuses": {
            "pickpocket_chance_percent": 0.5,
            "detection_chance_percent": -0.3,
            "item_value_limit_percent": 1.0  # Höherer Wert stealbar
        },
        "use_triggers": ["successful_pickpocket", "pickpocket_attempt"],
        "prerequisites": {"sneak": 20}
    },
    "lockpicking": {
        "name": "Schlösser knacken",
        "category": "stealth",
        "description": "Fähigkeit Schlösser zu öffnen",
        "base_xp_per_use": 7,
        "passive_bonuses": {
            "lockpick_success_percent": 0.4,
            "lockpick_break_chance_percent": -0.3,  # Weniger Dietriche brechen
            "unlock_speed_percent": 0.2
        },
        "use_triggers": ["unlock_lock", "break_lockpick"],
        "prerequisites": {}
    },
    "assassination": {
        "name": "Meuchelmord",
        "category": "stealth",
        "description": "Fähigkeit Gegner heimlich auszuschalten",
        "base_xp_per_use": 15,
        "passive_bonuses": {
            "backstab_damage_percent": 1.0,   # +1% Backstab-Schaden
            "silent_kill_chance_percent": 0.2,
            "poison_damage_percent": 0.5
        },
        "use_triggers": ["backstab_kill", "stealth_kill", "assassination"],
        "prerequisites": {"sneak": 30, "one_handed": 20}
    }
}


# ===== SURVIVAL SKILLS =====

SURVIVAL_SKILLS = {
    "hunting": {
        "name": "Jagen",
        "category": "survival",
        "description": "Fähigkeit Tiere zu jagen und zu erlegen",
        "base_xp_per_use": 6,
        "passive_bonuses": {
            "animal_damage_percent": 0.5,
            "tracking_range_percent": 0.3,
            "meat_yield_percent": 0.2
        },
        "use_triggers": ["kill_animal", "track_animal"],
        "prerequisites": {}
    },
    "tracking": {
        "name": "Spurenlesen",
        "category": "survival",
        "description": "Fähigkeit Spuren zu erkennen und zu folgen",
        "base_xp_per_use": 5,
        "passive_bonuses": {
            "track_discovery_percent": 0.4,
            "track_age_detection_flat": 1.0,  # Ältere Spuren erkennbar
            "rare_creature_track_percent": 0.1
        },
        "use_triggers": ["discover_track", "follow_track"],
        "prerequisites": {}
    },
    "first_aid": {
        "name": "Erste Hilfe",
        "category": "survival",
        "description": "Fähigkeit Wunden zu versorgen",
        "base_xp_per_use": 8,
        "passive_bonuses": {
            "healing_effectiveness_percent": 0.5,
            "bandage_efficiency_percent": 0.3,
            "disease_resistance_percent": 0.2
        },
        "use_triggers": ["heal_self", "heal_companion", "cure_disease"],
        "prerequisites": {}
    },
    "camping": {
        "name": "Lagern",
        "category": "survival",
        "description": "Fähigkeit sichere Lager aufzubauen",
        "base_xp_per_use": 4,
        "passive_bonuses": {
            "rest_effectiveness_percent": 0.3,
            "campfire_duration_percent": 0.5,
            "tent_protection_percent": 0.2
        },
        "use_triggers": ["setup_camp", "rest_at_camp"],
        "prerequisites": {}
    },
    "foraging": {
        "name": "Nahrungssuche",
        "category": "survival",
        "description": "Fähigkeit essbare Pflanzen und Pilze zu finden",
        "base_xp_per_use": 4,
        "passive_bonuses": {
            "food_find_chance_percent": 0.4,
            "poison_detection_percent": 0.5,  # Giftige Pflanzen erkennen
            "food_quality_percent": 0.2
        },
        "use_triggers": ["find_food", "identify_plant"],
        "prerequisites": {}
    }
}


# Kombiniere alle Skills
ALL_SKILLS = {
    **COMBAT_SKILLS,
    **CRAFTING_SKILLS,
    **GATHERING_SKILLS,
    **SOCIAL_SKILLS,
    **STEALTH_SKILLS,
    **SURVIVAL_SKILLS
}


# ===== SKILL SYSTEM CLASS =====

class SkillSystem:
    """
    Use-Based Skill Progression System (Skyrim-Style)

    Features:
    - Skills level 1-100 durch Nutzung
    - Exponentielles XP-System (höhere Level brauchen mehr XP)
    - Passive Boni steigen mit Skill-Level
    - Prerequisites für manche Skills
    - Persistente Speicherung
    """

    def __init__(self):
        """Initialisiere Skill System"""
        self.player_skills = self._initialize_player_skills()

    def _initialize_player_skills(self) -> Dict:
        """Initialisiere alle Skills auf Level 1 mit 0 XP"""
        skills = {}
        for skill_id in ALL_SKILLS.keys():
            skills[skill_id] = {
                "level": 1,
                "xp": 0,
                "xp_to_next_level": self._calculate_xp_needed(1)
            }
        return skills

    def _calculate_xp_needed(self, current_level: int) -> int:
        """
        Berechne XP für nächstes Level (exponentiell steigend)

        Formula: base_xp * (level^1.5)
        Level 1→2: ~25 XP
        Level 50→51: ~885 XP
        Level 99→100: ~2475 XP
        """
        base_xp = 25
        return int(base_xp * (current_level ** 1.5))

    def add_skill_xp(self, skill_id: str, base_xp: Optional[int] = None, multiplier: float = 1.0) -> Dict:
        """
        Füge XP zu einem Skill hinzu (wird bei Nutzung aufgerufen)

        Args:
            skill_id: ID des Skills
            base_xp: Base XP (falls None, wird aus Skill-DB genommen)
            multiplier: XP-Multiplikator (z.B. 2.0 für doppelte XP)

        Returns:
            Dict mit level_up Info und neuen Stats
        """
        if skill_id not in ALL_SKILLS:
            return {"ok": False, "error": "Unknown skill"}

        if skill_id not in self.player_skills:
            self.player_skills[skill_id] = {
                "level": 1,
                "xp": 0,
                "xp_to_next_level": self._calculate_xp_needed(1)
            }

        skill_data = ALL_SKILLS[skill_id]
        player_skill = self.player_skills[skill_id]

        # Bestimme XP-Gewinn
        if base_xp is None:
            base_xp = skill_data.get("base_xp_per_use", 5)

        xp_gained = int(base_xp * multiplier)

        # Füge XP hinzu
        player_skill["xp"] += xp_gained

        # Level Up Check
        leveled_up = False
        levels_gained = 0

        while player_skill["xp"] >= player_skill["xp_to_next_level"] and player_skill["level"] < 100:
            # Level Up!
            player_skill["xp"] -= player_skill["xp_to_next_level"]
            player_skill["level"] += 1
            levels_gained += 1
            leveled_up = True

            # Berechne neue XP-Anforderung
            player_skill["xp_to_next_level"] = self._calculate_xp_needed(player_skill["level"])

        return {
            "ok": True,
            "skill_id": skill_id,
            "skill_name": skill_data["name"],
            "xp_gained": xp_gained,
            "current_level": player_skill["level"],
            "current_xp": player_skill["xp"],
            "xp_to_next_level": player_skill["xp_to_next_level"],
            "leveled_up": leveled_up,
            "levels_gained": levels_gained,
            "bonuses": self.get_skill_bonuses(skill_id) if leveled_up else None
        }

    def get_skill_level(self, skill_id: str) -> int:
        """Gibt aktuelles Skill-Level zurück"""
        if skill_id not in self.player_skills:
            return 1
        return self.player_skills[skill_id]["level"]

    def get_skill_bonuses(self, skill_id: str) -> Dict:
        """
        Berechne aktuelle passive Boni eines Skills basierend auf Level

        Returns:
            Dict mit allen aktiven Boni
        """
        if skill_id not in ALL_SKILLS:
            return {}

        skill_data = ALL_SKILLS[skill_id]
        skill_level = self.get_skill_level(skill_id)

        bonuses = {}
        for bonus_type, bonus_per_level in skill_data.get("passive_bonuses", {}).items():
            bonuses[bonus_type] = round(bonus_per_level * skill_level, 2)

        return bonuses

    def get_all_skill_bonuses(self) -> Dict:
        """Gibt ALLE aktiven Skill-Boni zurück (für Stat-Berechnung)"""
        all_bonuses = {}

        for skill_id in self.player_skills.keys():
            skill_bonuses = self.get_skill_bonuses(skill_id)

            for bonus_type, value in skill_bonuses.items():
                if bonus_type not in all_bonuses:
                    all_bonuses[bonus_type] = 0
                all_bonuses[bonus_type] += value

        return all_bonuses

    def check_prerequisites(self, skill_id: str) -> Dict:
        """
        Prüfe ob Prerequisites für einen Skill erfüllt sind

        Returns:
            {
                "met": bool,
                "missing": List[str]  # Liste fehlender Requirements
            }
        """
        if skill_id not in ALL_SKILLS:
            return {"met": False, "missing": ["Unknown skill"]}

        skill_data = ALL_SKILLS[skill_id]
        prerequisites = skill_data.get("prerequisites", {})

        missing = []

        # Prüfe Skill-Level Requirements
        for req_skill, min_level in prerequisites.items():
            if req_skill.endswith("_min"):
                # Special requirement (z.B. combat_level_min)
                continue

            current_level = self.get_skill_level(req_skill)
            if current_level < min_level:
                missing.append(f"{ALL_SKILLS[req_skill]['name']} Level {min_level} (aktuell {current_level})")

        return {
            "met": len(missing) == 0,
            "missing": missing
        }

    def get_skill_info(self, skill_id: str) -> Dict:
        """Gibt vollständige Info über einen Skill zurück"""
        if skill_id not in ALL_SKILLS:
            return {"ok": False, "error": "Unknown skill"}

        skill_data = ALL_SKILLS[skill_id]
        player_skill = self.player_skills.get(skill_id, {"level": 1, "xp": 0, "xp_to_next_level": 25})

        return {
            "ok": True,
            "id": skill_id,
            "name": skill_data["name"],
            "category": skill_data["category"],
            "category_name": SKILL_CATEGORIES[skill_data["category"]]["name"],
            "description": skill_data["description"],
            "level": player_skill["level"],
            "xp": player_skill["xp"],
            "xp_to_next_level": player_skill["xp_to_next_level"],
            "progress_percent": round((player_skill["xp"] / player_skill["xp_to_next_level"]) * 100, 1),
            "bonuses": self.get_skill_bonuses(skill_id),
            "prerequisites": skill_data.get("prerequisites", {}),
            "prerequisites_met": self.check_prerequisites(skill_id)["met"]
        }

    def get_all_skills_by_category(self) -> Dict:
        """Gibt alle Skills gruppiert nach Kategorie zurück"""
        result = {}

        for category_id, category_data in SKILL_CATEGORIES.items():
            result[category_id] = {
                "name": category_data["name"],
                "color": category_data["color"],
                "icon": category_data["icon"],
                "skills": []
            }

        for skill_id, skill_data in ALL_SKILLS.items():
            category = skill_data["category"]
            skill_info = self.get_skill_info(skill_id)
            result[category]["skills"].append(skill_info)

        return result

    def get_skill_stats_summary(self) -> Dict:
        """Gibt Zusammenfassung aller Skill-Stats zurück"""
        total_levels = sum(skill["level"] for skill in self.player_skills.values())
        avg_level = total_levels / len(self.player_skills) if self.player_skills else 1

        # Finde höchste Skills
        top_skills = sorted(
            [(skill_id, data["level"]) for skill_id, data in self.player_skills.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_skills_formatted = [
            {
                "name": ALL_SKILLS[skill_id]["name"],
                "level": level
            }
            for skill_id, level in top_skills
        ]

        return {
            "total_skill_levels": total_levels,
            "average_skill_level": round(avg_level, 1),
            "skills_at_100": sum(1 for s in self.player_skills.values() if s["level"] == 100),
            "top_skills": top_skills_formatted,
            "total_bonuses": self.get_all_skill_bonuses()
        }

    def export_skills(self) -> str:
        """Exportiere Skill-Daten als JSON"""
        return json.dumps(self.player_skills, indent=2)

    def import_skills(self, skills_json: str) -> bool:
        """Importiere Skill-Daten aus JSON"""
        try:
            imported_skills = json.loads(skills_json)
            self.player_skills = imported_skills
            return True
        except:
            return False


# ===== GLOBAL INSTANCE =====

SKILL_SYSTEM = SkillSystem()


# ===== TEST CODE =====

if __name__ == "__main__":
    print("=" * 80)
    print("NAJIKA SKILL SYSTEM TEST")
    print("=" * 80)

    skill_sys = SkillSystem()

    # Test 1: Skill XP hinzufügen
    print("\n[TEST 1] Skill XP hinzufügen")
    print("-" * 80)

    # Simuliere Kampf mit Einhandwaffe
    for i in range(10):
        result = skill_sys.add_skill_xp("one_handed", base_xp=5)
        if result["leveled_up"]:
            print(f"🎉 LEVEL UP! {result['skill_name']} ist jetzt Level {result['current_level']}!")
            print(f"   Neue Boni: {result['bonuses']}")

    # Zeige finale Stats
    info = skill_sys.get_skill_info("one_handed")
    print(f"\n{info['name']}: Level {info['level']} ({info['xp']}/{info['xp_to_next_level']} XP)")
    print(f"Boni: {info['bonuses']}")

    # Test 2: Skill-Kategorien anzeigen
    print("\n[TEST 2] Alle Skills nach Kategorie")
    print("-" * 80)

    categories = skill_sys.get_all_skills_by_category()
    for cat_id, cat_data in categories.items():
        print(f"\n{cat_data['icon']} {cat_data['name']} ({len(cat_data['skills'])} Skills)")
        for skill in cat_data['skills'][:3]:  # Nur erste 3 anzeigen
            print(f"  - {skill['name']}: Level {skill['level']}")

    # Test 3: Skill-Progression simulieren
    print("\n[TEST 3] Schnelle Progression")
    print("-" * 80)

    # Simuliere intensive Nutzung
    for _ in range(100):
        skill_sys.add_skill_xp("smithing", base_xp=10)

    smithing_info = skill_sys.get_skill_info("smithing")
    print(f"{smithing_info['name']}: Level {smithing_info['level']}")
    print(f"Progress: {smithing_info['progress_percent']}%")
    print(f"Aktive Boni:")
    for bonus_type, value in smithing_info['bonuses'].items():
        print(f"  - {bonus_type}: {value}")

    # Test 4: Gesamt-Stats
    print("\n[TEST 4] Skill-Statistiken")
    print("-" * 80)

    stats = skill_sys.get_skill_stats_summary()
    print(f"Gesamt Skill-Levels: {stats['total_skill_levels']}")
    print(f"Durchschnittliches Level: {stats['average_skill_level']}")
    print(f"Skills auf Level 100: {stats['skills_at_100']}")
    print(f"\nTop 5 Skills:")
    for skill in stats['top_skills']:
        print(f"  - {skill['name']}: Level {skill['level']}")

    print("\n" + "=" * 80)
    print("✅ TEST ABGESCHLOSSEN")
    print("=" * 80)
