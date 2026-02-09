"""
NAJIKA COMBAT BALANCING SYSTEM
==============================

Skyrim + Dark Souls inspiriertes Damage-System:
- Level-Skalierung
- Waffen-Typen mit unterschiedlichen Multiplikatoren
- Elemental Damage (Fire, Ice, Lightning, etc.)
- Resistenzen
- Kritische Treffer mit Skill-basierter Chance
- Combo-System Multiplikatoren
- Status-Effekte (Burn, Freeze, Poison, etc.)

Erstellt: 2026-01-29
"""

import random
import math
from typing import Dict, List, Optional, Tuple
from enum import Enum

# ===== ENUMS =====

class DamageType(Enum):
    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    DARK = "dark"
    HOLY = "holy"
    EXPLOSION = "explosion"  # Najika Special!


class WeaponType(Enum):
    SWORD = "sword"         # Balanced
    GREATSWORD = "greatsword"  # Slow, high damage
    DAGGER = "dagger"       # Fast, low damage, high crit
    STAFF = "staff"         # Magic damage
    BOW = "bow"             # Ranged
    FIST = "fist"           # Combo-focused
    SCYTHE = "scythe"       # AoE


class StatusEffect(Enum):
    BURN = "burn"           # DoT Fire
    FREEZE = "freeze"       # Slow + DoT
    SHOCK = "shock"         # Stun chance
    POISON = "poison"       # DoT + Heal reduction
    BLEED = "bleed"         # DoT scales with movement
    CURSE = "curse"         # Reduced stats
    BLESS = "bless"         # Increased stats


# ===== WEAPON TYPE STATS =====

WEAPON_TYPE_STATS = {
    WeaponType.SWORD: {
        "damage_mult": 1.0,
        "speed": 1.0,
        "crit_chance": 0.05,
        "crit_mult": 2.0,
        "combo_max": 3
    },
    WeaponType.GREATSWORD: {
        "damage_mult": 1.5,
        "speed": 0.6,
        "crit_chance": 0.03,
        "crit_mult": 2.5,
        "combo_max": 2
    },
    WeaponType.DAGGER: {
        "damage_mult": 0.6,
        "speed": 1.8,
        "crit_chance": 0.15,
        "crit_mult": 3.0,
        "combo_max": 5
    },
    WeaponType.STAFF: {
        "damage_mult": 0.4,
        "speed": 1.0,
        "crit_chance": 0.05,
        "crit_mult": 2.0,
        "magic_mult": 1.5,
        "combo_max": 2
    },
    WeaponType.BOW: {
        "damage_mult": 0.8,
        "speed": 0.8,
        "crit_chance": 0.10,
        "crit_mult": 2.5,
        "combo_max": 1
    },
    WeaponType.FIST: {
        "damage_mult": 0.5,
        "speed": 2.0,
        "crit_chance": 0.08,
        "crit_mult": 2.0,
        "combo_max": 8,
        "combo_damage_increase": 0.1  # +10% per combo hit
    },
    WeaponType.SCYTHE: {
        "damage_mult": 1.2,
        "speed": 0.7,
        "crit_chance": 0.07,
        "crit_mult": 2.2,
        "aoe_mult": 0.7,  # 70% damage to nearby enemies
        "combo_max": 2
    }
}

# ===== ELEMENTAL EFFECTIVENESS =====

# Rock-Paper-Scissors style elemental system
ELEMENTAL_EFFECTIVENESS = {
    DamageType.FIRE: {
        "strong_against": [DamageType.ICE],
        "weak_against": [DamageType.ICE],
        "multiplier_strong": 1.5,
        "multiplier_weak": 0.5
    },
    DamageType.ICE: {
        "strong_against": [DamageType.LIGHTNING],
        "weak_against": [DamageType.FIRE],
        "multiplier_strong": 1.5,
        "multiplier_weak": 0.5
    },
    DamageType.LIGHTNING: {
        "strong_against": [DamageType.FIRE],
        "weak_against": [DamageType.ICE],
        "multiplier_strong": 1.5,
        "multiplier_weak": 0.5
    },
    DamageType.DARK: {
        "strong_against": [DamageType.HOLY],
        "weak_against": [DamageType.HOLY],
        "multiplier_strong": 2.0,
        "multiplier_weak": 0.25
    },
    DamageType.HOLY: {
        "strong_against": [DamageType.DARK],
        "weak_against": [DamageType.DARK],
        "multiplier_strong": 2.0,
        "multiplier_weak": 0.25
    },
    DamageType.EXPLOSION: {
        # Najika's Explosion is strong against everything!
        "strong_against": [DamageType.PHYSICAL, DamageType.FIRE, DamageType.ICE],
        "weak_against": [],
        "multiplier_strong": 1.3,
        "multiplier_weak": 1.0,
        "base_crit_bonus": 0.15  # +15% crit chance!
    }
}

# ===== STATUS EFFECT STATS =====

STATUS_EFFECT_STATS = {
    StatusEffect.BURN: {
        "dot_percent": 0.03,  # 3% max HP per tick
        "duration": 5,
        "tick_rate": 1.0  # 1 tick per second
    },
    StatusEffect.FREEZE: {
        "dot_percent": 0.01,
        "slow_percent": 0.3,  # 30% slower
        "duration": 4,
        "tick_rate": 1.0
    },
    StatusEffect.SHOCK: {
        "stun_chance": 0.2,  # 20% chance to stun per hit
        "duration": 3,
        "damage_amp": 0.1  # +10% damage taken
    },
    StatusEffect.POISON: {
        "dot_percent": 0.02,
        "heal_reduction": 0.5,  # 50% less healing
        "duration": 8,
        "tick_rate": 1.0
    },
    StatusEffect.BLEED: {
        "dot_flat": 5,  # Flat damage per tick
        "movement_mult": 2.0,  # 2x damage if moving
        "duration": 6,
        "tick_rate": 0.5  # 2 ticks per second
    },
    StatusEffect.CURSE: {
        "stat_reduction": 0.2,  # -20% all stats
        "duration": 10
    },
    StatusEffect.BLESS: {
        "stat_increase": 0.2,  # +20% all stats
        "duration": 10
    }
}


# ===== DAMAGE CALCULATOR =====

class CombatBalancing:
    """
    Zentrales Combat Balancing System für Najika World
    """

    # Level Scaling Constants
    LEVEL_SCALE_FACTOR = 0.1  # 10% increase per level
    BASE_PLAYER_ATK = 10
    BASE_PLAYER_DEF = 5
    BASE_PLAYER_HP = 100
    BASE_PLAYER_MP = 50

    # Combo System
    COMBO_DECAY_TIME = 2.0  # Seconds before combo resets
    COMBO_MAX_MULTIPLIER = 2.0  # Max 2x damage from combos

    def __init__(self):
        self.combo_counter = 0
        self.last_attack_time = 0
        self.active_status_effects: Dict[str, List[dict]] = {}  # target_id -> effects

    def calculate_player_stats(self, level: int, base_stats: dict = None) -> dict:
        """
        Berechnet skalierte Spieler-Stats basierend auf Level

        Formel: stat = base * (1 + level * LEVEL_SCALE_FACTOR)
        """
        base = base_stats or {}

        level_mult = 1 + (level - 1) * self.LEVEL_SCALE_FACTOR

        return {
            "hp": int((base.get("hp", self.BASE_PLAYER_HP)) * level_mult),
            "max_hp": int((base.get("hp", self.BASE_PLAYER_HP)) * level_mult),
            "mp": int((base.get("mp", self.BASE_PLAYER_MP)) * level_mult),
            "max_mp": int((base.get("mp", self.BASE_PLAYER_MP)) * level_mult),
            "atk": int((base.get("atk", self.BASE_PLAYER_ATK)) * level_mult),
            "def": int((base.get("def", self.BASE_PLAYER_DEF)) * level_mult),
            "level": level
        }

    def calculate_enemy_stats(self, base_stats: dict, dungeon_level: int) -> dict:
        """
        Skaliert Enemy Stats basierend auf Dungeon Level
        """
        level_mult = 1 + (dungeon_level - 1) * (self.LEVEL_SCALE_FACTOR * 0.8)  # Etwas weniger als Spieler

        return {
            "name": base_stats.get("name", "Enemy"),
            "hp": int(base_stats.get("hp", 20) * level_mult),
            "max_hp": int(base_stats.get("hp", 20) * level_mult),
            "atk": int(base_stats.get("atk", 5) * level_mult),
            "def": int(base_stats.get("def", 2) * level_mult),
            "gold": int(base_stats.get("gold", 10) * level_mult),
            "xp": int(base_stats.get("xp", 15) * level_mult),
            "resistances": base_stats.get("resistances", {}),
            "weaknesses": base_stats.get("weaknesses", [])
        }

    def calculate_damage(
        self,
        attacker: dict,
        defender: dict,
        weapon_type: WeaponType = WeaponType.SWORD,
        damage_type: DamageType = DamageType.PHYSICAL,
        skill_damage: int = 0,
        is_combo: bool = False,
        combo_count: int = 0
    ) -> Tuple[int, bool, str]:
        """
        Berechnet Schaden mit allen Faktoren

        Returns: (damage, is_critical, message)
        """
        weapon_stats = WEAPON_TYPE_STATS.get(weapon_type, WEAPON_TYPE_STATS[WeaponType.SWORD])

        # 1. Base Damage
        if skill_damage > 0:
            base_damage = skill_damage
        else:
            base_damage = attacker.get("atk", 10)

        # 2. Weapon Multiplier
        damage = base_damage * weapon_stats["damage_mult"]

        # 3. Defense Reduction (Skyrim-Style: diminishing returns)
        defense = defender.get("def", 0)
        damage_reduction = defense / (defense + 100)  # At 100 DEF = 50% reduction
        damage *= (1 - damage_reduction)

        # 4. Elemental Effectiveness
        elemental_mult = self._get_elemental_multiplier(damage_type, defender)
        damage *= elemental_mult

        # 5. Resistance Check
        resistance = defender.get("resistances", {}).get(damage_type.value, 0)
        damage *= (1 - resistance)

        # 6. Combo Multiplier (for fists especially)
        if is_combo and combo_count > 0:
            combo_bonus = weapon_stats.get("combo_damage_increase", 0.05)
            combo_mult = min(
                1 + (combo_count * combo_bonus),
                self.COMBO_MAX_MULTIPLIER
            )
            damage *= combo_mult

        # 7. Critical Hit Check
        crit_chance = weapon_stats["crit_chance"]
        # Explosion gets bonus crit!
        if damage_type == DamageType.EXPLOSION:
            crit_chance += ELEMENTAL_EFFECTIVENESS[DamageType.EXPLOSION].get("base_crit_bonus", 0)

        is_critical = random.random() < crit_chance
        if is_critical:
            damage *= weapon_stats["crit_mult"]

        # 8. Variance (±10%)
        variance = random.uniform(0.9, 1.1)
        damage *= variance

        # 9. Floor and minimum damage
        final_damage = max(1, int(damage))

        # Build message
        msg = ""
        if is_critical:
            msg = "KRITISCH! "
        if elemental_mult > 1.0:
            msg += "Effektiv! "
        elif elemental_mult < 1.0:
            msg += "Nicht sehr effektiv... "

        return (final_damage, is_critical, msg)

    def _get_elemental_multiplier(self, damage_type: DamageType, defender: dict) -> float:
        """
        Berechnet elementaren Multiplikator basierend auf Schwächen/Stärken
        """
        if damage_type == DamageType.PHYSICAL:
            return 1.0

        elem_data = ELEMENTAL_EFFECTIVENESS.get(damage_type)
        if not elem_data:
            return 1.0

        weaknesses = defender.get("weaknesses", [])

        # Check if defender is weak to this element
        for weak_type in elem_data.get("strong_against", []):
            if weak_type.value in weaknesses:
                return elem_data.get("multiplier_strong", 1.5)

        # Check if defender resists this element
        for resist_type in elem_data.get("weak_against", []):
            if resist_type.value in defender.get("resistances", {}):
                return elem_data.get("multiplier_weak", 0.5)

        return 1.0

    def apply_status_effect(
        self,
        target_id: str,
        effect: StatusEffect,
        source_stats: dict = None
    ) -> dict:
        """
        Wendet Status-Effekt auf Ziel an
        """
        effect_data = STATUS_EFFECT_STATS.get(effect)
        if not effect_data:
            return {"success": False, "error": "Unknown effect"}

        if target_id not in self.active_status_effects:
            self.active_status_effects[target_id] = []

        # Check if effect already exists (refresh duration)
        for existing in self.active_status_effects[target_id]:
            if existing["type"] == effect:
                existing["duration"] = effect_data["duration"]
                return {"success": True, "refreshed": True}

        # Apply new effect
        new_effect = {
            "type": effect,
            "duration": effect_data["duration"],
            "data": effect_data.copy(),
            "source_stats": source_stats or {}
        }
        self.active_status_effects[target_id].append(new_effect)

        return {"success": True, "applied": effect.value}

    def process_status_effects(self, target_id: str, target_stats: dict) -> dict:
        """
        Verarbeitet alle aktiven Status-Effekte auf einem Ziel

        Returns: {damage: int, stat_mods: dict, messages: list}
        """
        if target_id not in self.active_status_effects:
            return {"damage": 0, "stat_mods": {}, "messages": []}

        total_dot = 0
        stat_mods = {}
        messages = []
        effects_to_remove = []

        for i, effect in enumerate(self.active_status_effects[target_id]):
            effect_type = effect["type"]
            data = effect["data"]

            # Process DoT
            if "dot_percent" in data:
                dot_damage = int(target_stats.get("max_hp", 100) * data["dot_percent"])
                total_dot += dot_damage
                messages.append(f"{effect_type.value}: -{dot_damage} HP")

            if "dot_flat" in data:
                total_dot += data["dot_flat"]

            # Process stat mods
            if "stat_reduction" in data:
                for stat in ["atk", "def"]:
                    stat_mods[stat] = stat_mods.get(stat, 1.0) * (1 - data["stat_reduction"])

            if "stat_increase" in data:
                for stat in ["atk", "def"]:
                    stat_mods[stat] = stat_mods.get(stat, 1.0) * (1 + data["stat_increase"])

            if "slow_percent" in data:
                stat_mods["speed"] = stat_mods.get("speed", 1.0) * (1 - data["slow_percent"])

            # Reduce duration
            effect["duration"] -= 1
            if effect["duration"] <= 0:
                effects_to_remove.append(i)
                messages.append(f"{effect_type.value} ist abgelaufen")

        # Remove expired effects
        for i in reversed(effects_to_remove):
            self.active_status_effects[target_id].pop(i)

        return {"damage": total_dot, "stat_mods": stat_mods, "messages": messages}

    def get_xp_for_level(self, level: int) -> int:
        """
        XP benötigt für nächstes Level (exponentiell)

        Formel: XP = 100 * level^1.5
        """
        return int(100 * math.pow(level, 1.5))

    def calculate_xp_gain(self, enemy_level: int, player_level: int, base_xp: int) -> int:
        """
        XP Gain mit Level-Differenz Anpassung
        """
        level_diff = enemy_level - player_level

        if level_diff > 5:
            # Viel stärkerer Gegner = Bonus XP
            mult = 1.5
        elif level_diff > 0:
            mult = 1.0 + (level_diff * 0.1)
        elif level_diff > -5:
            # Leicht schwächerer Gegner = weniger XP
            mult = 1.0 + (level_diff * 0.1)
        else:
            # Viel schwächerer Gegner = kaum XP
            mult = 0.1

        return max(1, int(base_xp * mult))


# Singleton Instance
_combat_balancing = None

def get_combat_balancing() -> CombatBalancing:
    """Gibt die Combat Balancing Instanz zurück (Singleton)"""
    global _combat_balancing
    if _combat_balancing is None:
        _combat_balancing = CombatBalancing()
    return _combat_balancing


# ===== QUICK ACCESS FUNCTIONS =====

def calc_damage(attacker: dict, defender: dict, **kwargs) -> Tuple[int, bool, str]:
    """Shortcut für damage calculation"""
    return get_combat_balancing().calculate_damage(attacker, defender, **kwargs)

def scale_player_stats(level: int, base_stats: dict = None) -> dict:
    """Shortcut für player stat scaling"""
    return get_combat_balancing().calculate_player_stats(level, base_stats)

def scale_enemy_stats(base_stats: dict, dungeon_level: int) -> dict:
    """Shortcut für enemy stat scaling"""
    return get_combat_balancing().calculate_enemy_stats(base_stats, dungeon_level)


# Test
if __name__ == "__main__":
    cb = get_combat_balancing()

    print("=== COMBAT BALANCING TEST ===\n")

    # Test Player Stats at different levels
    print("Player Stats by Level:")
    for level in [1, 5, 10, 20]:
        stats = cb.calculate_player_stats(level)
        print(f"  Lvl {level}: HP={stats['hp']}, ATK={stats['atk']}, DEF={stats['def']}")

    # Test Damage Calculation
    print("\nDamage Calculation Test:")
    attacker = {"atk": 50}
    defender = {"def": 20, "weaknesses": ["fire"]}

    for weapon in [WeaponType.SWORD, WeaponType.DAGGER, WeaponType.GREATSWORD]:
        damage, crit, msg = cb.calculate_damage(
            attacker, defender,
            weapon_type=weapon,
            damage_type=DamageType.PHYSICAL
        )
        print(f"  {weapon.value}: {damage} damage {msg}")

    # Test Elemental
    print("\nElemental Damage Test:")
    for elem in [DamageType.PHYSICAL, DamageType.FIRE, DamageType.EXPLOSION]:
        damage, crit, msg = cb.calculate_damage(
            attacker, defender,
            damage_type=elem
        )
        print(f"  {elem.value}: {damage} damage {msg}")

    # Test XP Scaling
    print("\nXP for Level:")
    for level in [1, 5, 10, 20, 50]:
        xp = cb.get_xp_for_level(level)
        print(f"  Lvl {level} → {level+1}: {xp} XP needed")
