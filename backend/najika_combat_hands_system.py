"""
NAJIKA COMBAT HANDS SYSTEM
===========================
Zwei-Hand-Combat + Schnellzauber + Waffen-Anforderungen

FEATURES:
- Linke/Rechte Hand separat oder zusammen
- Dual-Cast (gleicher Zauber = stärker aber langsamer)
- Schnellzauber-Perks (Cast-Zeit reduzieren durch Skill)
- Waffen-Anforderungen (Stärke/Geschick/INT für Nutzung)
- Selbstverletzung bei zu schweren Waffen!
- Skyrim Learning-by-Doing

DESIGN PHILOSOPHIE:
- Jeder kann JEDE Waffe HALTEN - aber nicht effektiv NUTZEN
- Ohne Training: unkontrolliert, wenig Schaden, Selbstverletzungsgefahr
- Mit Training: volle Kontrolle, voller Schaden
- Realismus wie im echten Leben!

Author: Claude Code Team
Date: 2026-02-02
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any
import random
import math
from datetime import datetime, timedelta


# =============================================================================
# ENUMS
# =============================================================================

class HandSlot(Enum):
    """Welche Hand"""
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"  # Für Dual-Cast oder Zwei-Hand-Waffen


class AttackType(Enum):
    """Angriffsart"""
    LIGHT = "light"
    HEAVY = "heavy"
    DUAL_CAST = "dual_cast"  # Beide Hände gleicher Zauber
    COMBO = "combo"  # Beide Hände unterschiedlich


class WeaponCategory(Enum):
    """Waffen-Kategorien mit unterschiedlichen Anforderungen"""
    # Einhand-Waffen
    SWORD = "sword"
    DAGGER = "dagger"
    AXE = "axe"
    MACE = "mace"

    # Zweihand-Waffen (brauchen BEIDE Hände)
    GREATSWORD = "greatsword"
    GREATAXE = "greataxe"
    WARHAMMER = "warhammer"
    SPEAR = "spear"

    # Fernkampf
    BOW = "bow"
    CROSSBOW = "crossbow"
    GUN = "gun"
    RIFLE = "rifle"

    # Magie
    STAFF = "staff"
    WAND = "wand"
    TOME = "tome"  # Zauberbuch

    # Defensiv
    SHIELD = "shield"

    # Spezial
    FIST = "fist"
    WHIP = "whip"
    LASSO = "lasso"


class DamageType(Enum):
    """Schadenstypen"""
    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    POISON = "poison"
    SHADOW = "shadow"
    LIGHT = "light"
    ARCANE = "arcane"
    EXPLOSION = "explosion"


# =============================================================================
# WAFFEN-ANFORDERUNGEN DATABASE
# =============================================================================

@dataclass
class WeaponRequirements:
    """
    Anforderungen um eine Waffe EFFEKTIV zu nutzen

    Ohne diese Stats:
    - Weniger Schaden (bis zu -90%)
    - Langsamere Angriffe
    - Chance auf Selbstverletzung
    - Chance Waffe fallen zu lassen
    """
    strength: int = 0      # Körperkraft
    agility: int = 0       # Geschicklichkeit
    intelligence: int = 0  # Für Magie-Waffen
    skill_level: int = 1   # Mindest-Skill-Level in dieser Waffe

    # Gewicht beeinflusst Stamina
    weight: float = 1.0

    # Zwei-Hand erforderlich?
    two_handed: bool = False


# Waffen-Anforderungen Database
WEAPON_REQUIREMENTS: Dict[str, WeaponRequirements] = {
    # ========== EINHAND SCHWERTER ==========
    "rusty_sword": WeaponRequirements(strength=3, agility=2, skill_level=1, weight=2.0),
    "iron_sword": WeaponRequirements(strength=5, agility=3, skill_level=5, weight=3.0),
    "steel_sword": WeaponRequirements(strength=7, agility=4, skill_level=10, weight=3.5),
    "flame_blade": WeaponRequirements(strength=6, agility=4, intelligence=3, skill_level=15, weight=3.0),
    "frost_edge": WeaponRequirements(strength=6, agility=4, intelligence=3, skill_level=15, weight=3.2),
    "lightning_saber": WeaponRequirements(strength=5, agility=6, intelligence=4, skill_level=20, weight=2.5),
    "katana": WeaponRequirements(strength=4, agility=8, skill_level=25, weight=2.0),

    # ========== ZWEIHAND SCHWERTER (SEHR HOHE ANFORDERUNGEN) ==========
    "zweihander": WeaponRequirements(strength=15, agility=5, skill_level=20, weight=12.0, two_handed=True),
    "claymore": WeaponRequirements(strength=18, agility=4, skill_level=25, weight=15.0, two_handed=True),
    "demon_blade": WeaponRequirements(strength=20, agility=6, skill_level=35, weight=18.0, two_handed=True),
    "dragon_slayer": WeaponRequirements(strength=25, agility=5, skill_level=50, weight=25.0, two_handed=True),

    # ========== DOLCHE (NIEDRIGE STR, HOHE AGI) ==========
    "rusty_dagger": WeaponRequirements(strength=1, agility=3, skill_level=1, weight=0.5),
    "assassin_blade": WeaponRequirements(strength=2, agility=8, skill_level=15, weight=0.8),
    "poison_dagger": WeaponRequirements(strength=2, agility=6, intelligence=2, skill_level=10, weight=0.6),
    "soul_knife": WeaponRequirements(strength=3, agility=7, intelligence=5, skill_level=25, weight=0.7),

    # ========== ÄXTE ==========
    "wood_axe": WeaponRequirements(strength=5, agility=2, skill_level=1, weight=3.5),
    "battle_axe": WeaponRequirements(strength=10, agility=3, skill_level=10, weight=6.0),
    "executioner_axe": WeaponRequirements(strength=18, agility=2, skill_level=25, weight=14.0, two_handed=True),
    "frost_axe": WeaponRequirements(strength=12, agility=3, intelligence=3, skill_level=20, weight=7.0),

    # ========== HÄMMER (HÖCHSTE STR-ANFORDERUNGEN) ==========
    "wooden_hammer": WeaponRequirements(strength=6, agility=2, skill_level=1, weight=4.0),
    "war_hammer": WeaponRequirements(strength=20, agility=2, skill_level=20, weight=18.0, two_handed=True),
    "thunder_hammer": WeaponRequirements(strength=22, agility=3, intelligence=5, skill_level=30, weight=20.0, two_handed=True),
    "titan_crusher": WeaponRequirements(strength=30, agility=2, skill_level=50, weight=35.0, two_handed=True),

    # ========== SPEERE ==========
    "wooden_spear": WeaponRequirements(strength=4, agility=5, skill_level=1, weight=2.5, two_handed=True),
    "iron_spear": WeaponRequirements(strength=6, agility=6, skill_level=10, weight=4.0, two_handed=True),
    "trident": WeaponRequirements(strength=8, agility=7, intelligence=3, skill_level=20, weight=5.0, two_handed=True),

    # ========== STÄBE (INT-BASIERT) ==========
    "wooden_staff": WeaponRequirements(strength=2, agility=2, intelligence=5, skill_level=1, weight=1.5),
    "fire_staff": WeaponRequirements(strength=2, agility=2, intelligence=10, skill_level=10, weight=2.0),
    "ice_staff": WeaponRequirements(strength=2, agility=2, intelligence=10, skill_level=10, weight=2.0),
    "lightning_staff": WeaponRequirements(strength=2, agility=3, intelligence=12, skill_level=15, weight=2.2),
    "necro_staff": WeaponRequirements(strength=3, agility=2, intelligence=15, skill_level=25, weight=3.0),
    "megumin_staff": WeaponRequirements(strength=1, agility=1, intelligence=25, skill_level=50, weight=1.0),

    # ========== SCHILDE ==========
    "wooden_shield": WeaponRequirements(strength=4, agility=2, skill_level=1, weight=3.0),
    "iron_shield": WeaponRequirements(strength=8, agility=2, skill_level=10, weight=8.0),
    "tower_shield": WeaponRequirements(strength=15, agility=1, skill_level=20, weight=15.0),
    "magic_shield": WeaponRequirements(strength=5, agility=3, intelligence=8, skill_level=15, weight=4.0),

    # ========== BÖGEN (AGI + STR für Spannkraft) ==========
    "wooden_bow": WeaponRequirements(strength=4, agility=5, skill_level=1, weight=1.5, two_handed=True),
    "longbow": WeaponRequirements(strength=8, agility=8, skill_level=15, weight=2.5, two_handed=True),
    "crossbow": WeaponRequirements(strength=6, agility=4, skill_level=10, weight=4.0, two_handed=True),

    # ========== SCHUSSWAFFEN ==========
    "rusty_revolver": WeaponRequirements(strength=2, agility=5, skill_level=1, weight=1.0),
    "colt_peacemaker": WeaponRequirements(strength=3, agility=8, skill_level=15, weight=1.2),
    "dual_revolvers": WeaponRequirements(strength=4, agility=10, skill_level=25, weight=2.4, two_handed=True),
    "winchester_rifle": WeaponRequirements(strength=6, agility=6, skill_level=15, weight=4.0, two_handed=True),
    "sawed_off_shotgun": WeaponRequirements(strength=8, agility=4, skill_level=10, weight=3.5),

    # ========== FÄUSTE ==========
    "bare_fists": WeaponRequirements(strength=1, agility=1, skill_level=1, weight=0),
    "brass_knuckles": WeaponRequirements(strength=3, agility=4, skill_level=5, weight=0.5),
    "combat_gloves": WeaponRequirements(strength=5, agility=6, skill_level=15, weight=0.3),
    "titan_gauntlets": WeaponRequirements(strength=15, agility=5, skill_level=30, weight=5.0),

    # ========== SPEZIAL ==========
    "whip": WeaponRequirements(strength=3, agility=8, skill_level=10, weight=1.0),
    "lasso": WeaponRequirements(strength=4, agility=7, skill_level=5, weight=0.8),
    "dynamite": WeaponRequirements(strength=2, agility=5, skill_level=5, weight=0.5),
}


# =============================================================================
# WAFFEN DATABASE
# =============================================================================

@dataclass
class WeaponData:
    """Komplette Waffen-Definition"""
    weapon_id: str
    name: str
    name_de: str
    category: WeaponCategory

    # Basis-Schaden (bei 100% Effektivität)
    damage_light: int
    damage_heavy: int

    # Kosten
    stamina_light: int
    stamina_heavy: int
    mana_light: int = 0
    mana_heavy: int = 0

    # Timing (Sekunden)
    speed_light: float = 0.4
    speed_heavy: float = 0.8
    cast_time: float = 0.0  # Für Zauber

    # Reichweite
    range_meters: float = 2.0

    # Element
    damage_type: DamageType = DamageType.PHYSICAL

    # Spezial-Effekte
    special: Optional[str] = None
    crit_chance: float = 0.05

    # Für welche Hand?
    hand_slot: HandSlot = HandSlot.RIGHT


# Waffen Database (Auszug - erweitert die JS-Version)
WEAPONS_DB: Dict[str, WeaponData] = {
    # Schwerter
    "rusty_sword": WeaponData(
        "rusty_sword", "Rusty Sword", "Rostiges Schwert",
        WeaponCategory.SWORD, 15, 30, 10, 25,
        speed_light=0.4, speed_heavy=0.8, range_meters=2.5
    ),
    "iron_sword": WeaponData(
        "iron_sword", "Iron Sword", "Eisenschwert",
        WeaponCategory.SWORD, 22, 45, 12, 28,
        speed_light=0.4, speed_heavy=0.8, range_meters=2.8
    ),
    "steel_sword": WeaponData(
        "steel_sword", "Steel Sword", "Stahlschwert",
        WeaponCategory.SWORD, 28, 55, 14, 30,
        speed_light=0.38, speed_heavy=0.75, range_meters=3.0
    ),
    "flame_blade": WeaponData(
        "flame_blade", "Flame Blade", "Flammenklinge",
        WeaponCategory.SWORD, 18, 38, 15, 32,
        damage_type=DamageType.FIRE, special="burn"
    ),
    "katana": WeaponData(
        "katana", "Katana", "Katana",
        WeaponCategory.SWORD, 24, 48, 10, 22,
        speed_light=0.25, speed_heavy=0.5, crit_chance=0.2, special="iai_slash"
    ),

    # Zweihand
    "zweihander": WeaponData(
        "zweihander", "Zweihander", "Zweihänder",
        WeaponCategory.GREATSWORD, 35, 80, 25, 50,
        speed_light=0.8, speed_heavy=1.5, range_meters=4.0,
        hand_slot=HandSlot.BOTH, special="stagger"
    ),
    "dragon_slayer": WeaponData(
        "dragon_slayer", "Dragon Slayer", "Drachentöter",
        WeaponCategory.GREATSWORD, 80, 180, 40, 80,
        speed_light=1.2, speed_heavy=2.5, range_meters=5.0,
        hand_slot=HandSlot.BOTH, special="dragon_bane", crit_chance=0.15
    ),

    # Hämmer
    "war_hammer": WeaponData(
        "war_hammer", "War Hammer", "Kriegshammer",
        WeaponCategory.WARHAMMER, 35, 85, 28, 55,
        speed_light=0.8, speed_heavy=1.6, range_meters=2.8,
        hand_slot=HandSlot.BOTH, special="crush"
    ),
    "titan_crusher": WeaponData(
        "titan_crusher", "Titan Crusher", "Titanenbrecher",
        WeaponCategory.WARHAMMER, 60, 150, 50, 100,
        speed_light=1.5, speed_heavy=3.0, range_meters=3.5,
        hand_slot=HandSlot.BOTH, special="earthquake", crit_chance=0.25
    ),

    # Dolche
    "assassin_blade": WeaponData(
        "assassin_blade", "Assassin Blade", "Assassinenklinge",
        WeaponCategory.DAGGER, 12, 28, 6, 14,
        speed_light=0.18, speed_heavy=0.35, range_meters=1.8,
        damage_type=DamageType.SHADOW, special="backstab", crit_chance=0.25,
        hand_slot=HandSlot.LEFT  # Kann in beiden
    ),

    # Stäbe
    "fire_staff": WeaponData(
        "fire_staff", "Fire Staff", "Feuerstab",
        WeaponCategory.STAFF, 18, 50, 5, 15, 15, 35,
        speed_light=0.6, speed_heavy=1.5, cast_time=0.8,
        range_meters=10, damage_type=DamageType.FIRE,
        special="fireball_aoe", hand_slot=HandSlot.LEFT
    ),
    "megumin_staff": WeaponData(
        "megumin_staff", "Megumin's Explosion Staff", "Megumins Explosionsstab",
        WeaponCategory.STAFF, 5, 999, 5, 100, 5, 100,
        speed_light=0.3, speed_heavy=3.0, cast_time=5.0,
        range_meters=15, damage_type=DamageType.EXPLOSION,
        special="EXPLOSION", hand_slot=HandSlot.LEFT
    ),
}


# =============================================================================
# SPIELER STATS
# =============================================================================

@dataclass
class PlayerCombatStats:
    """Spieler Combat-Stats (Fallout SPECIAL erweitert)"""
    # Basis-Stats
    strength: int = 5       # Körperkraft - Waffen-Anforderungen, Schaden
    perception: int = 5     # Wahrnehmung - Trefferchance, Reichweite
    endurance: int = 5      # Ausdauer - Stamina, HP
    charisma: int = 5       # Charisma - NPC-Interaktion
    intelligence: int = 5   # Intelligenz - Magie, Cast-Zeit
    agility: int = 5        # Beweglichkeit - Angriffs-Speed, Dodge
    luck: int = 5           # Glück - Crit, Drops

    # Ressourcen
    hp: int = 100
    max_hp: int = 100
    stamina: int = 100
    max_stamina: int = 100
    mana: int = 100
    max_mana: int = 100

    # Waffen-Skill-Levels (Skyrim Learning by Doing)
    weapon_skills: Dict[str, int] = field(default_factory=lambda: {
        "sword": 1, "dagger": 1, "axe": 1, "hammer": 1, "spear": 1,
        "staff": 1, "shield": 1, "fist": 1, "bow": 1, "gun": 1,
        "greatsword": 1, "greataxe": 1, "warhammer": 1
    })

    # Magie-Skill-Levels
    magic_skills: Dict[str, int] = field(default_factory=lambda: {
        "fire": 1, "ice": 1, "lightning": 1, "light": 1, "shadow": 1,
        "arcane": 1, "explosion": 1, "restoration": 1, "alteration": 1
    })

    # XP für Skills
    weapon_xp: Dict[str, int] = field(default_factory=dict)
    magic_xp: Dict[str, int] = field(default_factory=dict)


# =============================================================================
# EFFEKTIVITÄTS-BERECHNUNG
# =============================================================================

@dataclass
class WeaponEffectiveness:
    """Ergebnis der Effektivitäts-Berechnung"""
    effectiveness: float  # 0.0 - 1.0+ (kann über 100% mit Buffs)
    damage_multiplier: float
    speed_multiplier: float
    stamina_multiplier: float

    # Risiken
    self_damage_chance: float  # Chance sich selbst zu verletzen
    drop_weapon_chance: float  # Chance Waffe fallen zu lassen
    fumble_chance: float  # Chance auf Fumble (Angriff verfehlt)

    # Feedback
    warnings: List[str] = field(default_factory=list)
    can_use_effectively: bool = True


def calculate_weapon_effectiveness(
    weapon_id: str,
    player: PlayerCombatStats
) -> WeaponEffectiveness:
    """
    Berechnet wie effektiv ein Spieler eine Waffe nutzen kann

    OHNE ANFORDERUNGEN = GEFÄHRLICH!
    - Zu schwach? Waffe unkontrolliert, Selbstverletzung möglich
    - Zu ungeschickt? Langsam, Drop-Chance
    - Kein Skill? Minimaler Schaden
    """

    if weapon_id not in WEAPON_REQUIREMENTS:
        # Unbekannte Waffe = volle Effektivität (Fallback)
        return WeaponEffectiveness(1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0)

    reqs = WEAPON_REQUIREMENTS[weapon_id]
    warnings = []

    # Kategorie für Skill-Lookup
    weapon_data = WEAPONS_DB.get(weapon_id)
    if weapon_data:
        skill_name = weapon_data.category.value
    else:
        skill_name = "sword"  # Fallback

    player_skill = player.weapon_skills.get(skill_name, 1)

    # ========== STÄRKE-CHECK ==========
    str_ratio = player.strength / max(reqs.strength, 1)
    if str_ratio < 0.5:
        # Viel zu schwach - GEFÄHRLICH
        str_effectiveness = 0.1
        self_damage = 0.3  # 30% Chance
        warnings.append(f"⚠️ WARNUNG: Du bist viel zu schwach für diese Waffe! (Brauchst STR {reqs.strength}, hast {player.strength})")
    elif str_ratio < 0.75:
        # Zu schwach
        str_effectiveness = 0.4
        self_damage = 0.15
        warnings.append(f"Die Waffe ist zu schwer. STR {reqs.strength} empfohlen.")
    elif str_ratio < 1.0:
        # Knapp unter Anforderung
        str_effectiveness = 0.7
        self_damage = 0.05
        warnings.append(f"Etwas mehr Stärke würde helfen.")
    else:
        # Anforderung erfüllt
        str_effectiveness = min(1.0 + (str_ratio - 1.0) * 0.1, 1.2)  # Max 20% Bonus
        self_damage = 0.0

    # ========== GESCHICKLICHKEIT-CHECK ==========
    agi_ratio = player.agility / max(reqs.agility, 1)
    if agi_ratio < 0.5:
        # Viel zu ungeschickt
        agi_effectiveness = 0.2
        drop_chance = 0.25
        fumble = 0.3
        warnings.append(f"⚠️ WARNUNG: Dir fehlt die Kontrolle! (Brauchst AGI {reqs.agility}, hast {player.agility})")
    elif agi_ratio < 0.75:
        agi_effectiveness = 0.5
        drop_chance = 0.1
        fumble = 0.15
        warnings.append(f"Mehr Geschick würde Kontrolle verbessern.")
    elif agi_ratio < 1.0:
        agi_effectiveness = 0.8
        drop_chance = 0.03
        fumble = 0.05
    else:
        agi_effectiveness = min(1.0 + (agi_ratio - 1.0) * 0.1, 1.2)
        drop_chance = 0.0
        fumble = 0.0

    # ========== INTELLIGENZ-CHECK (für Magie-Waffen) ==========
    if reqs.intelligence > 0:
        int_ratio = player.intelligence / max(reqs.intelligence, 1)
        if int_ratio < 0.5:
            int_effectiveness = 0.1
            warnings.append(f"⚠️ WARNUNG: Du verstehst diese Waffe nicht! (Brauchst INT {reqs.intelligence})")
        elif int_ratio < 1.0:
            int_effectiveness = 0.6 + (int_ratio * 0.4)
            warnings.append(f"Mehr Intelligenz würde die Magie verstärken.")
        else:
            int_effectiveness = min(1.0 + (int_ratio - 1.0) * 0.15, 1.3)  # Magie skaliert stärker
    else:
        int_effectiveness = 1.0

    # ========== SKILL-LEVEL-CHECK ==========
    skill_ratio = player_skill / max(reqs.skill_level, 1)
    if skill_ratio < 0.3:
        # Kaum Erfahrung
        skill_effectiveness = 0.1
        warnings.append(f"⚠️ Du hast kaum Erfahrung mit dieser Waffe! (Skill {player_skill}/{reqs.skill_level})")
        # Erhöht alle Risiken
        self_damage += 0.1
        drop_chance += 0.1
        fumble += 0.2
    elif skill_ratio < 0.6:
        skill_effectiveness = 0.4
        warnings.append(f"Mehr Training würde helfen. (Skill {player_skill}/{reqs.skill_level})")
    elif skill_ratio < 1.0:
        skill_effectiveness = 0.7 + (skill_ratio * 0.3)
    else:
        # Überqualifiziert = Bonus
        skill_effectiveness = min(1.0 + (skill_ratio - 1.0) * 0.2, 1.5)  # Max 50% Bonus

    # ========== GEWICHT-CHECK (beeinflusst Stamina) ==========
    weight_factor = reqs.weight / max(player.strength, 1)
    if weight_factor > 2.0:
        stamina_mult = 2.5  # 150% mehr Stamina
        warnings.append("Die Waffe ist extrem schwer für dich.")
    elif weight_factor > 1.0:
        stamina_mult = 1.0 + (weight_factor - 1.0) * 0.5
    else:
        stamina_mult = 1.0

    # ========== GESAMT-EFFEKTIVITÄT ==========
    # Kombiniere alle Faktoren
    total_effectiveness = (
        str_effectiveness * 0.3 +
        agi_effectiveness * 0.25 +
        int_effectiveness * 0.2 +
        skill_effectiveness * 0.25
    )

    # Damage Multiplier (basierend auf Effektivität)
    if total_effectiveness < 0.3:
        damage_mult = 0.1  # Fast kein Schaden
    elif total_effectiveness < 0.5:
        damage_mult = 0.3
    elif total_effectiveness < 0.75:
        damage_mult = 0.6
    elif total_effectiveness < 1.0:
        damage_mult = 0.85
    else:
        damage_mult = total_effectiveness  # Kann über 1.0 sein

    # Speed Multiplier (langsamer wenn ungeschickt)
    speed_mult = min(1.0, agi_effectiveness)  # Nie schneller als normal

    # Kann effektiv nutzen?
    can_use = total_effectiveness >= 0.5 and len([w for w in warnings if "WARNUNG" in w]) == 0

    return WeaponEffectiveness(
        effectiveness=round(total_effectiveness, 2),
        damage_multiplier=round(damage_mult, 2),
        speed_multiplier=round(speed_mult, 2),
        stamina_multiplier=round(stamina_mult, 2),
        self_damage_chance=round(min(self_damage, 0.5), 2),  # Max 50%
        drop_weapon_chance=round(min(drop_chance, 0.4), 2),  # Max 40%
        fumble_chance=round(min(fumble, 0.5), 2),  # Max 50%
        warnings=warnings,
        can_use_effectively=can_use
    )


# =============================================================================
# SCHNELLZAUBER SYSTEM
# =============================================================================

@dataclass
class QuickCastPerk:
    """Schnellzauber-Perk Definition"""
    perk_id: str
    name: str
    name_de: str
    description_de: str

    # Effekte
    cast_time_reduction: float  # -10% = 0.1
    applies_to: List[str]  # Welche Magie-Schulen

    # Anforderungen
    required_skill: str
    required_level: int
    required_int: int = 0


QUICKCAST_PERKS: Dict[str, QuickCastPerk] = {
    # Allgemeine Schnellzauber
    "quickcast_novice": QuickCastPerk(
        "quickcast_novice", "Quick Cast I", "Schnellzauber I",
        "Reduziert Cast-Zeit aller Zauber um 10%",
        cast_time_reduction=0.1,
        applies_to=["all"],
        required_skill="arcane", required_level=10
    ),
    "quickcast_apprentice": QuickCastPerk(
        "quickcast_apprentice", "Quick Cast II", "Schnellzauber II",
        "Reduziert Cast-Zeit aller Zauber um 20%",
        cast_time_reduction=0.2,
        applies_to=["all"],
        required_skill="arcane", required_level=25
    ),
    "quickcast_adept": QuickCastPerk(
        "quickcast_adept", "Quick Cast III", "Schnellzauber III",
        "Reduziert Cast-Zeit aller Zauber um 30%",
        cast_time_reduction=0.3,
        applies_to=["all"],
        required_skill="arcane", required_level=50
    ),
    "quickcast_expert": QuickCastPerk(
        "quickcast_expert", "Quick Cast IV", "Schnellzauber IV",
        "Reduziert Cast-Zeit aller Zauber um 40%",
        cast_time_reduction=0.4,
        applies_to=["all"],
        required_skill="arcane", required_level=75
    ),
    "quickcast_master": QuickCastPerk(
        "quickcast_master", "Quick Cast V", "Schnellzauber V",
        "Reduziert Cast-Zeit aller Zauber um 50%",
        cast_time_reduction=0.5,
        applies_to=["all"],
        required_skill="arcane", required_level=100
    ),

    # Schul-spezifische Schnellzauber
    "fire_quickcast": QuickCastPerk(
        "fire_quickcast", "Flame Adept", "Flammenexperte",
        "Feuer-Zauber 30% schneller",
        cast_time_reduction=0.3,
        applies_to=["fire"],
        required_skill="fire", required_level=30
    ),
    "ice_quickcast": QuickCastPerk(
        "ice_quickcast", "Frost Adept", "Frostexperte",
        "Eis-Zauber 30% schneller",
        cast_time_reduction=0.3,
        applies_to=["ice"],
        required_skill="ice", required_level=30
    ),
    "lightning_quickcast": QuickCastPerk(
        "lightning_quickcast", "Storm Adept", "Sturmexperte",
        "Blitz-Zauber 35% schneller (Blitz ist natürlich schnell!)",
        cast_time_reduction=0.35,
        applies_to=["lightning"],
        required_skill="lightning", required_level=30
    ),

    # INT-basierte Schnellzauber
    "brilliant_mind": QuickCastPerk(
        "brilliant_mind", "Brilliant Mind", "Brillanter Geist",
        "Bei INT > 15: Alle Zauber -25% Cast-Zeit",
        cast_time_reduction=0.25,
        applies_to=["all"],
        required_skill="arcane", required_level=20, required_int=15
    ),
    "genius": QuickCastPerk(
        "genius", "Genius", "Genie",
        "Bei INT > 20: Alle Zauber -40% Cast-Zeit",
        cast_time_reduction=0.4,
        applies_to=["all"],
        required_skill="arcane", required_level=40, required_int=20
    ),

    # Instant Cast Chance
    "lucky_cast": QuickCastPerk(
        "lucky_cast", "Lucky Cast", "Glückszauber",
        "5% Chance auf Instant-Cast",
        cast_time_reduction=1.0,  # Wird als Chance interpretiert
        applies_to=["all"],
        required_skill="arcane", required_level=50
    ),

    # EXPLOSION Spezial (aber NIEMALS instant!)
    "explosion_chanting": QuickCastPerk(
        "explosion_chanting", "Chanting Mastery", "Beschwörungs-Meisterschaft",
        "EXPLOSION Cast-Zeit -40% (aber nie unter 3 Sekunden!)",
        cast_time_reduction=0.4,
        applies_to=["explosion"],
        required_skill="explosion", required_level=50
    ),
}


# =============================================================================
# DUAL-CAST SYSTEM
# =============================================================================

@dataclass
class DualCastResult:
    """Ergebnis eines Dual-Cast"""
    success: bool
    damage: int
    cast_time: float  # Erhöht!
    mana_cost: int  # Erhöht!
    bonus_effect: Optional[str] = None
    message: str = ""


def calculate_dual_cast(
    spell_school: str,
    base_damage: int,
    base_cast_time: float,
    base_mana: int,
    player: PlayerCombatStats,
    active_perks: List[str]
) -> DualCastResult:
    """
    Dual-Cast: Beide Hände casten den gleichen Zauber

    Effekt:
    - +100% Schaden (oder mehr mit Perks)
    - +50% Cast-Zeit
    - +200% Mana-Kosten
    - Spezial-Effekte möglich
    """

    # Basis Dual-Cast Multiplikatoren
    damage_mult = 2.0  # +100%
    cast_time_mult = 1.5  # +50%
    mana_mult = 3.0  # +200% (beide Hände + Synergie)

    # Skill-Bonus für Dual-Cast
    skill_level = player.magic_skills.get(spell_school, 1)
    if skill_level >= 50:
        damage_mult += 0.5  # +150% total bei Skill 50+
    if skill_level >= 75:
        cast_time_mult -= 0.2  # Nur +30% Cast-Zeit
    if skill_level >= 100:
        mana_mult -= 0.5  # "Nur" +150% Mana

    # INT-Bonus
    if player.intelligence >= 15:
        damage_mult += 0.2
    if player.intelligence >= 20:
        cast_time_mult -= 0.1

    # Perks anwenden
    for perk_id in active_perks:
        if perk_id == "dual_cast_mastery":
            damage_mult += 0.5
            cast_time_mult -= 0.2
        elif perk_id == "efficient_dual_cast":
            mana_mult -= 0.5

    # Berechne Endwerte
    final_damage = int(base_damage * damage_mult)
    final_cast_time = base_cast_time * max(cast_time_mult, 1.1)  # Mindestens +10%
    final_mana = int(base_mana * mana_mult)

    # Bonus-Effekte basierend auf Schule
    bonus_effect = None
    if spell_school == "fire":
        bonus_effect = "Großflächige Explosion, garantiertes Brennen"
    elif spell_school == "ice":
        bonus_effect = "Einfrieren garantiert bei Treffern unter 50% HP"
    elif spell_school == "lightning":
        bonus_effect = "Kettenblitz trifft bis zu 5 Ziele"
    elif spell_school == "light":
        bonus_effect = "AoE Heilung für Verbündete in der Nähe"
    elif spell_school == "shadow":
        bonus_effect = "Totale Dunkelheit, Feinde geblendet"
    elif spell_school == "explosion":
        bonus_effect = "MEGA-EXPLOSION: 3x Radius, aber Selbst-Knockback!"

    return DualCastResult(
        success=True,
        damage=final_damage,
        cast_time=round(final_cast_time, 2),
        mana_cost=final_mana,
        bonus_effect=bonus_effect,
        message=f"Dual-Cast {spell_school.upper()}: {final_damage} Schaden!"
    )


# =============================================================================
# HAND-COMBAT SYSTEM
# =============================================================================

@dataclass
class HandLoadout:
    """Was in welcher Hand ist"""
    left_hand: Optional[str] = None   # Waffen-ID oder None
    right_hand: Optional[str] = None

    # Für Zwei-Hand-Waffen
    using_two_handed: bool = False
    two_handed_weapon: Optional[str] = None


@dataclass
class AttackResult:
    """Ergebnis eines Angriffs"""
    success: bool
    damage: int
    damage_type: DamageType

    # Timing
    attack_time: float
    recovery_time: float

    # Kosten
    stamina_cost: int
    mana_cost: int

    # Effekte
    special_effect: Optional[str] = None
    applied_status: Optional[str] = None

    # Risiken (bei schlechter Effektivität)
    self_damage: int = 0
    dropped_weapon: bool = False
    fumbled: bool = False

    # Feedback
    message: str = ""
    warnings: List[str] = field(default_factory=list)

    # XP
    xp_gained: Dict[str, int] = field(default_factory=dict)


class HandCombatSystem:
    """
    Haupt-Combat-System für Zwei-Hand-Kampf

    Features:
    - Separate Aktionen pro Hand
    - Dual-Cast für Magie
    - Waffen-Anforderungen mit Konsequenzen
    - Schnellzauber-Perks
    - Skyrim Learning-by-Doing
    """

    def __init__(self):
        self.players: Dict[str, PlayerCombatStats] = {}
        self.loadouts: Dict[str, HandLoadout] = {}
        self.active_perks: Dict[str, List[str]] = {}  # player_id -> perk_ids

        # Cooldowns
        self.attack_cooldowns: Dict[str, Dict[str, float]] = {}  # player -> hand -> timestamp

        # Daily limits
        self.daily_explosion_used: Dict[str, bool] = {}
        self.last_daily_reset: datetime = datetime.now()

    def register_player(self, player_id: str, stats: Optional[PlayerCombatStats] = None) -> PlayerCombatStats:
        """Registriert einen Spieler"""
        if player_id not in self.players:
            self.players[player_id] = stats or PlayerCombatStats()
            self.loadouts[player_id] = HandLoadout()
            self.active_perks[player_id] = []
            self.attack_cooldowns[player_id] = {"left": 0, "right": 0}
        return self.players[player_id]

    def equip_weapon(
        self,
        player_id: str,
        weapon_id: str,
        hand: HandSlot
    ) -> Dict:
        """
        Rüstet eine Waffe aus

        Prüft Anforderungen und gibt Warnungen!
        """
        if player_id not in self.players:
            return {"success": False, "error": "Spieler nicht registriert"}

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        # Waffen-Daten
        weapon_data = WEAPONS_DB.get(weapon_id)
        if not weapon_data:
            return {"success": False, "error": f"Waffe {weapon_id} nicht gefunden"}

        # Zwei-Hand Check
        reqs = WEAPON_REQUIREMENTS.get(weapon_id)
        if reqs and reqs.two_handed:
            # Zwei-Hand-Waffe übernimmt beide Hände
            loadout.left_hand = None
            loadout.right_hand = None
            loadout.using_two_handed = True
            loadout.two_handed_weapon = weapon_id
        else:
            # Einhand-Waffe
            loadout.using_two_handed = False
            loadout.two_handed_weapon = None

            if hand == HandSlot.LEFT:
                loadout.left_hand = weapon_id
            elif hand == HandSlot.RIGHT:
                loadout.right_hand = weapon_id
            else:
                # BOTH für Einhand = beide Hände gleiche Waffe (Dual-Wield)
                loadout.left_hand = weapon_id
                loadout.right_hand = weapon_id

        # Effektivitäts-Check
        effectiveness = calculate_weapon_effectiveness(weapon_id, player)

        result = {
            "success": True,
            "weapon": weapon_id,
            "weapon_name": weapon_data.name_de,
            "hand": hand.value,
            "two_handed": reqs.two_handed if reqs else False,
            "effectiveness": effectiveness.effectiveness,
            "damage_multiplier": effectiveness.damage_multiplier,
            "can_use_effectively": effectiveness.can_use_effectively,
            "warnings": effectiveness.warnings
        }

        if not effectiveness.can_use_effectively:
            result["critical_warning"] = "⚠️ Du kannst diese Waffe NICHT effektiv nutzen!"

        return result

    def attack(
        self,
        player_id: str,
        hand: HandSlot,
        attack_type: AttackType,
        target_distance: float = 2.0
    ) -> AttackResult:
        """
        Führt einen Angriff aus

        Berücksichtigt:
        - Welche Hand (links/rechts/beide)
        - Angriffstyp (leicht/schwer/dual-cast)
        - Waffen-Anforderungen
        - Risiken bei schlechter Effektivität
        """
        if player_id not in self.players:
            return AttackResult(False, 0, DamageType.PHYSICAL, 0, 0, 0, 0,
                              message="Spieler nicht registriert")

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        # Bestimme Waffe
        if loadout.using_two_handed:
            weapon_id = loadout.two_handed_weapon
            actual_hand = HandSlot.BOTH
        elif hand == HandSlot.LEFT:
            weapon_id = loadout.left_hand
            actual_hand = HandSlot.LEFT
        elif hand == HandSlot.RIGHT:
            weapon_id = loadout.right_hand
            actual_hand = HandSlot.RIGHT
        else:
            # Dual-Cast/Combo
            weapon_id = loadout.right_hand or loadout.left_hand
            actual_hand = HandSlot.BOTH

        if not weapon_id:
            # Faust-Kampf
            weapon_id = "bare_fists"

        weapon_data = WEAPONS_DB.get(weapon_id)
        if not weapon_data:
            return AttackResult(False, 0, DamageType.PHYSICAL, 0, 0, 0, 0,
                              message=f"Waffe {weapon_id} nicht in DB")

        # Effektivität berechnen
        effectiveness = calculate_weapon_effectiveness(weapon_id, player)

        # Basis-Werte
        if attack_type == AttackType.HEAVY:
            base_damage = weapon_data.damage_heavy
            base_stamina = weapon_data.stamina_heavy
            base_mana = weapon_data.mana_heavy
            base_time = weapon_data.speed_heavy
        else:
            base_damage = weapon_data.damage_light
            base_stamina = weapon_data.stamina_light
            base_mana = weapon_data.mana_light
            base_time = weapon_data.speed_light

        # ========== DUAL-CAST HANDLING ==========
        if attack_type == AttackType.DUAL_CAST and weapon_data.category == WeaponCategory.STAFF:
            dual_result = calculate_dual_cast(
                weapon_data.damage_type.value,
                base_damage,
                weapon_data.cast_time or base_time,
                base_mana,
                player,
                self.active_perks.get(player_id, [])
            )

            if player.mana < dual_result.mana_cost:
                return AttackResult(False, 0, weapon_data.damage_type, 0, 0, 0, 0,
                                  message=f"Nicht genug Mana! Brauche {dual_result.mana_cost}")

            player.mana -= dual_result.mana_cost

            # XP für beide Hände
            xp_gained = self._gain_xp(player_id, weapon_data.category.value, 30)
            magic_xp = self._gain_magic_xp(player_id, weapon_data.damage_type.value, 25)

            return AttackResult(
                success=True,
                damage=dual_result.damage,
                damage_type=weapon_data.damage_type,
                attack_time=dual_result.cast_time,
                recovery_time=0.5,
                stamina_cost=0,
                mana_cost=dual_result.mana_cost,
                special_effect=dual_result.bonus_effect,
                message=dual_result.message,
                xp_gained={"weapon": xp_gained, "magic": magic_xp}
            )

        # ========== NORMALE ANGRIFFE ==========

        # Effektivität anwenden
        final_damage = int(base_damage * effectiveness.damage_multiplier)
        final_stamina = int(base_stamina * effectiveness.stamina_multiplier)
        attack_time = base_time / effectiveness.speed_multiplier  # Langsamer wenn uneffektiv

        # ========== WEAPON INFUSE BONUS ==========
        # Prüfe ob die Waffe mit einem Element infust ist
        infuse_bonus = 1.0
        infuse_element = None
        actual_damage_type = weapon_data.damage_type

        try:
            infuse_sys = get_infuse_system()
            infuse_bonus, infuse_element = infuse_sys.get_infuse_damage_bonus(player_id, weapon_id)
            if infuse_element:
                # Element-Schaden hinzufügen!
                final_damage = int(final_damage * infuse_bonus)
                # Damage Type aendern zum Element
                element_to_damage = {
                    MagicElement.FIRE: DamageType.FIRE,
                    MagicElement.ICE: DamageType.ICE,
                    MagicElement.LIGHTNING: DamageType.LIGHTNING,
                    MagicElement.WATER: DamageType.PHYSICAL,  # Wasser macht keinen direkten Schaden
                    MagicElement.EARTH: DamageType.PHYSICAL,
                    MagicElement.WIND: DamageType.PHYSICAL,
                    MagicElement.LIGHT: DamageType.LIGHT,
                    MagicElement.DARK: DamageType.SHADOW,
                    MagicElement.NATURE: DamageType.POISON,
                }
                actual_damage_type = element_to_damage.get(infuse_element, weapon_data.damage_type)
        except Exception:
            pass  # Infuse System nicht verfuegbar, ignorieren

        # Schnellzauber-Perks für Magie
        if weapon_data.cast_time > 0:
            cast_reduction = self._get_cast_time_reduction(
                player_id,
                weapon_data.damage_type.value,
                player.intelligence
            )
            attack_time = weapon_data.cast_time * (1 - cast_reduction)

            # EXPLOSION nie unter 3 Sekunden!
            if weapon_data.damage_type == DamageType.EXPLOSION:
                attack_time = max(attack_time, 3.0)

        # Ressourcen-Check
        if player.stamina < final_stamina:
            return AttackResult(False, 0, weapon_data.damage_type, 0, 0, 0, 0,
                              message="Nicht genug Stamina!")
        if base_mana > 0 and player.mana < base_mana:
            return AttackResult(False, 0, weapon_data.damage_type, 0, 0, 0, 0,
                              message="Nicht genug Mana!")

        # Ressourcen abziehen
        player.stamina -= final_stamina
        if base_mana > 0:
            player.mana -= base_mana

        # ========== RISIKO-CHECKS ==========
        self_damage = 0
        dropped = False
        fumbled = False
        warnings = list(effectiveness.warnings)

        # Fumble Check (Angriff verfehlt)
        if random.random() < effectiveness.fumble_chance:
            fumbled = True
            final_damage = 0
            warnings.append("💨 Du hast den Angriff verfehlt! (Mangelnde Kontrolle)")

        # Selbstverletzungs-Check
        if not fumbled and random.random() < effectiveness.self_damage_chance:
            self_damage = int(base_damage * 0.3 * (1 - effectiveness.effectiveness))
            player.hp = max(0, player.hp - self_damage)
            warnings.append(f"💥 Du hast dich selbst verletzt! ({self_damage} Schaden)")

        # Drop-Weapon Check
        if random.random() < effectiveness.drop_weapon_chance:
            dropped = True
            # Waffe aus Loadout entfernen
            if actual_hand == HandSlot.LEFT:
                loadout.left_hand = None
            elif actual_hand == HandSlot.RIGHT:
                loadout.right_hand = None
            else:
                loadout.two_handed_weapon = None
                loadout.using_two_handed = False
            warnings.append("🗡️ Du hast die Waffe fallen gelassen!")

        # ========== XP VERGEBEN (Skyrim!) ==========
        xp_gained = {}
        if not fumbled:
            xp_weapon = self._gain_xp(player_id, weapon_data.category.value,
                                      15 if attack_type == AttackType.HEAVY else 5)
            xp_gained["weapon"] = xp_weapon

            if weapon_data.damage_type != DamageType.PHYSICAL:
                xp_magic = self._gain_magic_xp(player_id, weapon_data.damage_type.value, 10)
                xp_gained["magic"] = xp_magic

        # Nachricht zusammenbauen
        if fumbled:
            message = f"Angriff verfehlt! (Effektivität: {int(effectiveness.effectiveness*100)}%)"
        elif self_damage > 0:
            message = f"{final_damage} Schaden (aber {self_damage} Selbstverletzung!)"
        else:
            message = f"{final_damage} Schaden mit {weapon_data.name_de}"

        return AttackResult(
            success=not fumbled,
            damage=final_damage,
            damage_type=weapon_data.damage_type,
            attack_time=round(attack_time, 2),
            recovery_time=0.3,
            stamina_cost=final_stamina,
            mana_cost=base_mana,
            special_effect=weapon_data.special,
            self_damage=self_damage,
            dropped_weapon=dropped,
            fumbled=fumbled,
            message=message,
            warnings=warnings,
            xp_gained=xp_gained
        )

    def _get_cast_time_reduction(
        self,
        player_id: str,
        magic_school: str,
        player_int: int
    ) -> float:
        """Berechnet Cast-Zeit-Reduktion durch Perks"""
        total_reduction = 0.0

        perks = self.active_perks.get(player_id, [])

        for perk_id in perks:
            perk = QUICKCAST_PERKS.get(perk_id)
            if not perk:
                continue

            # Prüfe ob Perk anwendbar
            if "all" in perk.applies_to or magic_school in perk.applies_to:
                # INT-Anforderung
                if perk.required_int > 0 and player_int < perk.required_int:
                    continue

                # Lucky Cast = Chance auf Instant
                if perk_id == "lucky_cast":
                    if random.random() < 0.05:
                        return 1.0  # Instant!
                else:
                    total_reduction += perk.cast_time_reduction

        return min(total_reduction, 0.7)  # Max 70% Reduktion

    def _gain_xp(self, player_id: str, skill_name: str, amount: int) -> int:
        """Gibt Waffen-XP (Skyrim Learning by Doing)"""
        player = self.players[player_id]

        # Map category to skill
        skill_map = {
            "greatsword": "sword",
            "greataxe": "axe",
            "warhammer": "hammer",
        }
        mapped_skill = skill_map.get(skill_name, skill_name)

        if mapped_skill not in player.weapon_skills:
            player.weapon_skills[mapped_skill] = 1
        if mapped_skill not in player.weapon_xp:
            player.weapon_xp[mapped_skill] = 0

        player.weapon_xp[mapped_skill] += amount

        # Level-Up Check
        xp_needed = 100 + (player.weapon_skills[mapped_skill] * 50)
        while player.weapon_xp[mapped_skill] >= xp_needed:
            player.weapon_xp[mapped_skill] -= xp_needed
            player.weapon_skills[mapped_skill] += 1
            xp_needed = 100 + (player.weapon_skills[mapped_skill] * 50)

        return amount

    def _gain_magic_xp(self, player_id: str, school: str, amount: int) -> int:
        """Gibt Magie-XP"""
        player = self.players[player_id]

        if school not in player.magic_skills:
            player.magic_skills[school] = 1
        if school not in player.magic_xp:
            player.magic_xp[school] = 0

        player.magic_xp[school] += amount

        # Level-Up
        xp_needed = 150 + (player.magic_skills[school] * 75)
        while player.magic_xp[school] >= xp_needed:
            player.magic_xp[school] -= xp_needed
            player.magic_skills[school] += 1
            xp_needed = 150 + (player.magic_skills[school] * 75)

        return amount

    def unlock_perk(self, player_id: str, perk_id: str) -> Dict:
        """Schaltet einen Perk frei"""
        if player_id not in self.players:
            return {"success": False, "error": "Spieler nicht registriert"}

        perk = QUICKCAST_PERKS.get(perk_id)
        if not perk:
            return {"success": False, "error": f"Perk {perk_id} nicht gefunden"}

        player = self.players[player_id]

        # Anforderungen prüfen
        skill_level = player.magic_skills.get(perk.required_skill, 1)
        if skill_level < perk.required_level:
            return {
                "success": False,
                "error": f"Brauche {perk.required_skill} Level {perk.required_level} (hast {skill_level})"
            }

        if perk.required_int > 0 and player.intelligence < perk.required_int:
            return {
                "success": False,
                "error": f"Brauche INT {perk.required_int} (hast {player.intelligence})"
            }

        # Perk freischalten
        if player_id not in self.active_perks:
            self.active_perks[player_id] = []

        if perk_id not in self.active_perks[player_id]:
            self.active_perks[player_id].append(perk_id)

        return {
            "success": True,
            "perk": perk_id,
            "perk_name": perk.name_de,
            "effect": perk.description_de
        }

    def get_player_status(self, player_id: str) -> Dict:
        """Holt kompletten Spieler-Status"""
        if player_id not in self.players:
            return {"error": "Spieler nicht registriert"}

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        # Effektivität für ausgerüstete Waffen
        left_eff = None
        right_eff = None
        two_hand_eff = None

        if loadout.left_hand:
            left_eff = calculate_weapon_effectiveness(loadout.left_hand, player)
        if loadout.right_hand:
            right_eff = calculate_weapon_effectiveness(loadout.right_hand, player)
        if loadout.two_handed_weapon:
            two_hand_eff = calculate_weapon_effectiveness(loadout.two_handed_weapon, player)

        return {
            "stats": {
                "strength": player.strength,
                "perception": player.perception,
                "endurance": player.endurance,
                "charisma": player.charisma,
                "intelligence": player.intelligence,
                "agility": player.agility,
                "luck": player.luck,
            },
            "resources": {
                "hp": player.hp,
                "max_hp": player.max_hp,
                "stamina": player.stamina,
                "max_stamina": player.max_stamina,
                "mana": player.mana,
                "max_mana": player.max_mana,
            },
            "loadout": {
                "left_hand": loadout.left_hand,
                "right_hand": loadout.right_hand,
                "two_handed": loadout.using_two_handed,
                "two_handed_weapon": loadout.two_handed_weapon,
            },
            "effectiveness": {
                "left": {
                    "value": left_eff.effectiveness if left_eff else None,
                    "warnings": left_eff.warnings if left_eff else []
                } if left_eff else None,
                "right": {
                    "value": right_eff.effectiveness if right_eff else None,
                    "warnings": right_eff.warnings if right_eff else []
                } if right_eff else None,
                "two_handed": {
                    "value": two_hand_eff.effectiveness if two_hand_eff else None,
                    "warnings": two_hand_eff.warnings if two_hand_eff else []
                } if two_hand_eff else None,
            },
            "weapon_skills": player.weapon_skills,
            "magic_skills": player.magic_skills,
            "active_perks": self.active_perks.get(player_id, []),
        }

    def get_weapon_preview(self, player_id: str, weapon_id: str) -> Dict:
        """
        Zeigt Vorschau einer Waffe BEVOR sie ausgerüstet wird

        Wichtig für Spieler um zu sehen ob sie die Waffe nutzen können!
        """
        if player_id not in self.players:
            return {"error": "Spieler nicht registriert"}

        player = self.players[player_id]

        weapon_data = WEAPONS_DB.get(weapon_id)
        if not weapon_data:
            return {"error": f"Waffe {weapon_id} nicht gefunden"}

        reqs = WEAPON_REQUIREMENTS.get(weapon_id)
        if not reqs:
            return {"error": f"Keine Anforderungen für {weapon_id}"}

        effectiveness = calculate_weapon_effectiveness(weapon_id, player)

        return {
            "weapon_id": weapon_id,
            "weapon_name": weapon_data.name_de,
            "category": weapon_data.category.value,
            "two_handed": reqs.two_handed,
            "requirements": {
                "strength": {"required": reqs.strength, "player": player.strength, "met": player.strength >= reqs.strength},
                "agility": {"required": reqs.agility, "player": player.agility, "met": player.agility >= reqs.agility},
                "intelligence": {"required": reqs.intelligence, "player": player.intelligence, "met": player.intelligence >= reqs.intelligence},
                "skill_level": {"required": reqs.skill_level, "player": player.weapon_skills.get(weapon_data.category.value, 1), "met": player.weapon_skills.get(weapon_data.category.value, 1) >= reqs.skill_level},
            },
            "weight": reqs.weight,
            "effectiveness": {
                "total": effectiveness.effectiveness,
                "damage_multiplier": effectiveness.damage_multiplier,
                "speed_multiplier": effectiveness.speed_multiplier,
                "stamina_multiplier": effectiveness.stamina_multiplier,
            },
            "risks": {
                "self_damage_chance": f"{int(effectiveness.self_damage_chance * 100)}%",
                "drop_weapon_chance": f"{int(effectiveness.drop_weapon_chance * 100)}%",
                "fumble_chance": f"{int(effectiveness.fumble_chance * 100)}%",
            },
            "can_use_effectively": effectiveness.can_use_effectively,
            "warnings": effectiveness.warnings,
            "base_stats": {
                "damage_light": weapon_data.damage_light,
                "damage_heavy": weapon_data.damage_heavy,
                "your_damage_light": int(weapon_data.damage_light * effectiveness.damage_multiplier),
                "your_damage_heavy": int(weapon_data.damage_heavy * effectiveness.damage_multiplier),
            }
        }

    def export_state(self, player_id: str) -> Dict:
        """Exportiert Spieler-State für Save"""
        if player_id not in self.players:
            return {}

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        return {
            "stats": {
                "strength": player.strength,
                "perception": player.perception,
                "endurance": player.endurance,
                "charisma": player.charisma,
                "intelligence": player.intelligence,
                "agility": player.agility,
                "luck": player.luck,
            },
            "resources": {
                "hp": player.hp,
                "max_hp": player.max_hp,
                "stamina": player.stamina,
                "max_stamina": player.max_stamina,
                "mana": player.mana,
                "max_mana": player.max_mana,
            },
            "weapon_skills": player.weapon_skills,
            "weapon_xp": player.weapon_xp,
            "magic_skills": player.magic_skills,
            "magic_xp": player.magic_xp,
            "loadout": {
                "left_hand": loadout.left_hand,
                "right_hand": loadout.right_hand,
                "two_handed_weapon": loadout.two_handed_weapon,
            },
            "perks": self.active_perks.get(player_id, []),
        }

    def import_state(self, player_id: str, state: Dict):
        """Importiert Spieler-State"""
        if player_id not in self.players:
            self.register_player(player_id)

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        # Stats
        if "stats" in state:
            for stat, value in state["stats"].items():
                if hasattr(player, stat):
                    setattr(player, stat, value)

        # Resources
        if "resources" in state:
            for res, value in state["resources"].items():
                if hasattr(player, res):
                    setattr(player, res, value)

        # Skills
        if "weapon_skills" in state:
            player.weapon_skills = state["weapon_skills"]
        if "weapon_xp" in state:
            player.weapon_xp = state["weapon_xp"]
        if "magic_skills" in state:
            player.magic_skills = state["magic_skills"]
        if "magic_xp" in state:
            player.magic_xp = state["magic_xp"]

        # Loadout
        if "loadout" in state:
            loadout.left_hand = state["loadout"].get("left_hand")
            loadout.right_hand = state["loadout"].get("right_hand")
            loadout.two_handed_weapon = state["loadout"].get("two_handed_weapon")
            loadout.using_two_handed = loadout.two_handed_weapon is not None

        # Perks
        if "perks" in state:
            self.active_perks[player_id] = state["perks"]


# =============================================================================
# SPELL SLOT SYSTEM (Skyrim-Style: Zauber in Hand, kein Stab noetig!)
# =============================================================================

class MagicElement(Enum):
    """Magie-Elemente fuer Zauber und Infuse"""
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    WATER = "water"
    EARTH = "earth"
    WIND = "wind"
    LIGHT = "light"
    DARK = "dark"
    NATURE = "nature"
    EXPLOSION = "explosion"  # NIEMALS mit anderen kombinieren!


@dataclass
class SpellData:
    """Ein Zauber der in der Hand ausgeruestet werden kann"""
    spell_id: str
    name: str
    name_de: str
    element: MagicElement

    # Kosten
    mana_cost: int = 20
    stamina_cost: int = 5

    # Effekte
    base_damage: int = 0
    base_heal: int = 0

    # Timing
    cast_time: float = 0.5

    # Infuse-Eigenschaften (wenn auf Waffe angewendet)
    infuse_duration: float = 30.0  # Sekunden
    infuse_damage_bonus: float = 0.2  # +20% Element-Schaden
    infuse_mana_cost: int = 30  # Extra Mana fuer Infuse


# Zauber-Datenbank (Skyrim-Style)
SPELLS_DB: Dict[str, SpellData] = {
    # FEUER
    "flames": SpellData("flames", "Flames", "Flammen", MagicElement.FIRE,
                        mana_cost=8, base_damage=15, cast_time=0.0,  # Channeling
                        infuse_duration=20, infuse_damage_bonus=0.25),
    "fireball": SpellData("fireball", "Fireball", "Feuerball", MagicElement.FIRE,
                          mana_cost=25, base_damage=40, cast_time=0.8,
                          infuse_duration=30, infuse_damage_bonus=0.3),
    "fire_storm": SpellData("fire_storm", "Fire Storm", "Feuersturm", MagicElement.FIRE,
                            mana_cost=60, base_damage=80, cast_time=2.0,
                            infuse_duration=45, infuse_damage_bonus=0.4),

    # EIS
    "frostbite": SpellData("frostbite", "Frostbite", "Frostbiss", MagicElement.ICE,
                           mana_cost=10, base_damage=12, cast_time=0.0,
                           infuse_duration=20, infuse_damage_bonus=0.2),
    "ice_spike": SpellData("ice_spike", "Ice Spike", "Eiszapfen", MagicElement.ICE,
                           mana_cost=20, base_damage=35, cast_time=0.6,
                           infuse_duration=30, infuse_damage_bonus=0.25),
    "blizzard": SpellData("blizzard", "Blizzard", "Schneesturm", MagicElement.ICE,
                          mana_cost=55, base_damage=70, cast_time=2.5,
                          infuse_duration=45, infuse_damage_bonus=0.35),

    # BLITZ
    "sparks": SpellData("sparks", "Sparks", "Funken", MagicElement.LIGHTNING,
                        mana_cost=12, base_damage=18, cast_time=0.0,
                        infuse_duration=20, infuse_damage_bonus=0.25),
    "lightning_bolt": SpellData("lightning_bolt", "Lightning Bolt", "Blitz", MagicElement.LIGHTNING,
                                mana_cost=30, base_damage=45, cast_time=0.3,
                                infuse_duration=30, infuse_damage_bonus=0.3),
    "chain_lightning": SpellData("chain_lightning", "Chain Lightning", "Kettenblitz", MagicElement.LIGHTNING,
                                 mana_cost=65, base_damage=60, cast_time=1.0,
                                 infuse_duration=45, infuse_damage_bonus=0.4),

    # WASSER (Heilung)
    "healing": SpellData("healing", "Healing", "Heilung", MagicElement.WATER,
                         mana_cost=15, base_heal=30, cast_time=1.0,
                         infuse_duration=0, infuse_damage_bonus=0),  # Kann nicht infusen
    "regeneration": SpellData("regeneration", "Regeneration", "Regeneration", MagicElement.WATER,
                              mana_cost=40, base_heal=10, cast_time=0.5,  # HoT
                              infuse_duration=0, infuse_damage_bonus=0),

    # ERDE
    "stone_flesh": SpellData("stone_flesh", "Stone Flesh", "Steinhaut", MagicElement.EARTH,
                             mana_cost=25, cast_time=1.0,
                             infuse_duration=60, infuse_damage_bonus=0.15),
    "rock_throw": SpellData("rock_throw", "Rock Throw", "Steinwurf", MagicElement.EARTH,
                            mana_cost=20, base_damage=30, cast_time=0.7,
                            infuse_duration=30, infuse_damage_bonus=0.2),

    # WIND
    "gust": SpellData("gust", "Gust", "Windstoss", MagicElement.WIND,
                      mana_cost=15, base_damage=15, cast_time=0.3,
                      infuse_duration=25, infuse_damage_bonus=0.15),
    "haste": SpellData("haste", "Haste", "Eile", MagicElement.WIND,
                       mana_cost=30, cast_time=0.5,
                       infuse_duration=0, infuse_damage_bonus=0),  # Buff, kein Infuse

    # LICHT
    "light_beam": SpellData("light_beam", "Light Beam", "Lichtstrahl", MagicElement.LIGHT,
                            mana_cost=20, base_damage=25, cast_time=0.4,
                            infuse_duration=30, infuse_damage_bonus=0.25),
    "blessing": SpellData("blessing", "Blessing", "Segen", MagicElement.LIGHT,
                          mana_cost=35, cast_time=1.5,
                          infuse_duration=0, infuse_damage_bonus=0),

    # DUNKEL
    "shadow_bolt": SpellData("shadow_bolt", "Shadow Bolt", "Schattenblitz", MagicElement.DARK,
                             mana_cost=22, base_damage=30, cast_time=0.5,
                             infuse_duration=30, infuse_damage_bonus=0.25),
    "life_drain": SpellData("life_drain", "Life Drain", "Lebensraub", MagicElement.DARK,
                            mana_cost=35, base_damage=25, base_heal=20, cast_time=0.0,
                            infuse_duration=25, infuse_damage_bonus=0.2),

    # NATUR
    "vine_whip": SpellData("vine_whip", "Vine Whip", "Rankenpeitsche", MagicElement.NATURE,
                           mana_cost=18, base_damage=22, cast_time=0.4,
                           infuse_duration=30, infuse_damage_bonus=0.2),
    "thorn_armor": SpellData("thorn_armor", "Thorn Armor", "Dornenpanzer", MagicElement.NATURE,
                             mana_cost=40, cast_time=1.2,
                             infuse_duration=45, infuse_damage_bonus=0.15),

    # EXPLOSION (Konosuba! - NIEMALS kombinieren!)
    "explosion": SpellData("explosion", "Explosion", "EXPLOSION!!!", MagicElement.EXPLOSION,
                           mana_cost=100, stamina_cost=50, base_damage=300, cast_time=3.0,
                           infuse_duration=0, infuse_damage_bonus=0),  # NIEMALS infusen!
}


@dataclass
class WeaponInfuseState:
    """Status eines infusten (verzauberten) Waffe"""
    weapon_id: str
    element: MagicElement
    spell_id: str
    damage_bonus: float
    remaining_duration: float  # Sekunden
    applied_at: datetime = field(default_factory=datetime.now)

    def is_active(self) -> bool:
        elapsed = (datetime.now() - self.applied_at).total_seconds()
        return elapsed < self.remaining_duration

    def get_remaining_time(self) -> float:
        elapsed = (datetime.now() - self.applied_at).total_seconds()
        return max(0, self.remaining_duration - elapsed)


@dataclass
class ExtendedHandLoadout(HandLoadout):
    """Erweitertes Loadout mit Zauber-Slots"""
    left_spell: Optional[str] = None   # Spell-ID
    right_spell: Optional[str] = None

    # Aktive Weapon Infuses
    weapon_infuses: Dict[str, WeaponInfuseState] = field(default_factory=dict)


class WeaponInfuseSystem:
    """
    WEAPON INFUSE SYSTEM
    ====================
    Zauber auf Waffe wirken = Temporaerer Element-Buff

    Beispiel:
    - Links: Feuerball ausgeruestet
    - Rechts: Eisenschwert
    - Aktion: Feuerball auf Schwert wirken
    - Ergebnis: Flammenschwert fuer 30 Sekunden (+30% Feuerschaden)

    WICHTIG: Explosion kann NIEMALS auf Waffen angewendet werden!
    """

    def __init__(self, combat_system: 'HandCombatSystem'):
        self.combat_system = combat_system
        self.loadouts: Dict[str, ExtendedHandLoadout] = {}
        self.learned_spells: Dict[str, List[str]] = {}  # player_id -> spell_ids

    def get_or_create_loadout(self, player_id: str) -> ExtendedHandLoadout:
        """Holt oder erstellt erweitertes Loadout"""
        if player_id not in self.loadouts:
            # Konvertiere bestehendes Loadout
            old_loadout = self.combat_system.loadouts.get(player_id)
            if old_loadout:
                self.loadouts[player_id] = ExtendedHandLoadout(
                    left_hand=old_loadout.left_hand,
                    right_hand=old_loadout.right_hand,
                    using_two_handed=old_loadout.using_two_handed,
                    two_handed_weapon=old_loadout.two_handed_weapon
                )
            else:
                self.loadouts[player_id] = ExtendedHandLoadout()
        return self.loadouts[player_id]

    def learn_spell(self, player_id: str, spell_id: str) -> Dict:
        """Zauber lernen (Skyrim Learning by Doing)"""
        if spell_id not in SPELLS_DB:
            return {"success": False, "error": f"Zauber '{spell_id}' existiert nicht!"}

        if player_id not in self.learned_spells:
            self.learned_spells[player_id] = []

        if spell_id in self.learned_spells[player_id]:
            return {"success": False, "error": "Zauber bereits gelernt!"}

        spell = SPELLS_DB[spell_id]
        self.learned_spells[player_id].append(spell_id)

        return {
            "success": True,
            "spell_id": spell_id,
            "spell_name": spell.name_de,
            "element": spell.element.value
        }

    def equip_spell(self, player_id: str, spell_id: str, hand: HandSlot) -> Dict:
        """Zauber in Hand ausruesten (Skyrim-Style)"""
        if spell_id not in self.learned_spells.get(player_id, []):
            return {"success": False, "error": f"Zauber '{spell_id}' nicht gelernt!"}

        if spell_id not in SPELLS_DB:
            return {"success": False, "error": f"Zauber '{spell_id}' nicht gefunden!"}

        loadout = self.get_or_create_loadout(player_id)
        spell = SPELLS_DB[spell_id]

        if hand == HandSlot.LEFT:
            loadout.left_spell = spell_id
            loadout.left_hand = None  # Waffe in dieser Hand entfernen
        elif hand == HandSlot.RIGHT:
            loadout.right_spell = spell_id
            loadout.right_hand = None
        else:
            loadout.left_spell = spell_id
            loadout.right_spell = spell_id
            loadout.left_hand = None
            loadout.right_hand = None

        return {
            "success": True,
            "spell_id": spell_id,
            "spell_name": spell.name_de,
            "element": spell.element.value,
            "hand": hand.value
        }

    def infuse_weapon(self, player_id: str, spell_hand: HandSlot, weapon_hand: HandSlot) -> Dict:
        """
        ZAUBER AUF WAFFE WIRKEN = TEMPORAERER BUFF

        Beispiel:
        - spell_hand=LEFT (Feuerball)
        - weapon_hand=RIGHT (Schwert)
        - Ergebnis: Flammenschwert fuer X Sekunden

        EXPLOSION kann NIEMALS auf Waffen angewendet werden!
        """
        if player_id not in self.combat_system.players:
            return {"success": False, "error": "Spieler nicht registriert!"}

        player = self.combat_system.players[player_id]
        loadout = self.get_or_create_loadout(player_id)

        # Welcher Zauber?
        spell_id = loadout.left_spell if spell_hand == HandSlot.LEFT else loadout.right_spell
        if not spell_id:
            return {"success": False, "error": f"Kein Zauber in {spell_hand.value} Hand!"}

        spell = SPELLS_DB.get(spell_id)
        if not spell:
            return {"success": False, "error": f"Zauber '{spell_id}' nicht gefunden!"}

        # EXPLOSION kann NIEMALS auf Waffen angewendet werden!
        if spell.element == MagicElement.EXPLOSION:
            return {
                "success": False,
                "error": "EXPLOSION kann NIEMALS auf Waffen angewendet werden! (8 Gebote!)"
            }

        # Kann dieser Zauber infusen?
        if spell.infuse_duration <= 0:
            return {"success": False, "error": f"{spell.name_de} kann nicht auf Waffen angewendet werden!"}

        # Welche Waffe?
        weapon_id = loadout.right_hand if weapon_hand == HandSlot.RIGHT else loadout.left_hand
        if not weapon_id:
            return {"success": False, "error": f"Keine Waffe in {weapon_hand.value} Hand!"}

        weapon = WEAPONS_DB.get(weapon_id)
        if not weapon:
            return {"success": False, "error": f"Waffe '{weapon_id}' nicht gefunden!"}

        # Mana-Kosten pruefen
        total_mana = spell.infuse_mana_cost
        if player.mana < total_mana:
            return {"success": False, "error": f"Nicht genug Mana! ({player.mana}/{total_mana})"}

        # Mana abziehen
        player.mana -= total_mana

        # Infuse erstellen
        infuse = WeaponInfuseState(
            weapon_id=weapon_id,
            element=spell.element,
            spell_id=spell_id,
            damage_bonus=spell.infuse_damage_bonus,
            remaining_duration=spell.infuse_duration
        )

        loadout.weapon_infuses[weapon_id] = infuse

        # Magic Skill XP (Learning by Doing!)
        skill_name = spell.element.value
        if skill_name not in player.magic_skills:
            player.magic_skills[skill_name] = 1
        if skill_name not in player.magic_xp:
            player.magic_xp[skill_name] = 0

        player.magic_xp[skill_name] += 20  # Infuse gibt XP!

        # Level-Up Check
        xp_needed = 150 + (player.magic_skills[skill_name] * 75)
        leveled_up = False
        while player.magic_xp[skill_name] >= xp_needed:
            player.magic_xp[skill_name] -= xp_needed
            player.magic_skills[skill_name] += 1
            leveled_up = True
            xp_needed = 150 + (player.magic_skills[skill_name] * 75)

        # Generiere passenden Namen
        element_names = {
            MagicElement.FIRE: "Flammen",
            MagicElement.ICE: "Frost",
            MagicElement.LIGHTNING: "Blitz",
            MagicElement.WATER: "Wasser",
            MagicElement.EARTH: "Stein",
            MagicElement.WIND: "Wind",
            MagicElement.LIGHT: "Licht",
            MagicElement.DARK: "Schatten",
            MagicElement.NATURE: "Natur",
        }
        element_prefix = element_names.get(spell.element, spell.element.value)

        return {
            "success": True,
            "weapon_id": weapon_id,
            "weapon_name": weapon.name_de,
            "element": spell.element.value,
            "infused_name": f"{element_prefix}-{weapon.name_de}",  # z.B. "Flammen-Eisenschwert"
            "damage_bonus": f"+{int(spell.infuse_damage_bonus * 100)}%",
            "duration": spell.infuse_duration,
            "mana_cost": total_mana,
            "leveled_up": leveled_up,
            "message": f"✨ {weapon.name_de} ist jetzt ein {element_prefix}-{weapon.name_de}!"
        }

    def get_active_infuses(self, player_id: str) -> List[Dict]:
        """Alle aktiven Weapon Infuses fuer einen Spieler"""
        loadout = self.loadouts.get(player_id)
        if not loadout:
            return []

        active = []
        expired = []

        for weapon_id, infuse in loadout.weapon_infuses.items():
            if infuse.is_active():
                weapon = WEAPONS_DB.get(weapon_id)
                active.append({
                    "weapon_id": weapon_id,
                    "weapon_name": weapon.name_de if weapon else weapon_id,
                    "element": infuse.element.value,
                    "damage_bonus": f"+{int(infuse.damage_bonus * 100)}%",
                    "remaining_time": round(infuse.get_remaining_time(), 1)
                })
            else:
                expired.append(weapon_id)

        # Abgelaufene entfernen
        for weapon_id in expired:
            del loadout.weapon_infuses[weapon_id]

        return active

    def get_infuse_damage_bonus(self, player_id: str, weapon_id: str) -> Tuple[float, Optional[MagicElement]]:
        """
        Holt Damage-Bonus und Element fuer eine infuste Waffe
        Returns: (bonus_multiplier, element) oder (1.0, None) wenn nicht infust
        """
        loadout = self.loadouts.get(player_id)
        if not loadout:
            return 1.0, None

        infuse = loadout.weapon_infuses.get(weapon_id)
        if not infuse or not infuse.is_active():
            return 1.0, None

        return 1.0 + infuse.damage_bonus, infuse.element


# =============================================================================
# GRAB & THROW SYSTEM (Wrestling-Style!)
# =============================================================================

class GrabMoveType(Enum):
    """Verfuegbare Griff-Moves"""
    SUPLEX = "suplex"           # Skill Level 15 noetig
    CHOKESLAM = "chokeslam"     # Skill Level 10 noetig
    THROW_OBJECT = "throw_object"
    THROW_ENEMY = "throw_enemy"
    RELEASE = "release"


@dataclass
class GrabState:
    """Status eines Griffs"""
    is_grabbing: bool = False
    grabbed_target: Optional[str] = None
    grab_start_time: Optional[datetime] = None
    grab_duration_limit: float = 5.0  # Max 5 Sekunden halten


@dataclass
class GrabMoveResult:
    """Ergebnis eines Griff-Moves"""
    success: bool
    move_type: GrabMoveType
    damage: int = 0
    stun_duration: float = 0.0  # Sekunden
    grounded_duration: float = 0.0  # Am Boden
    environment_bonus: int = 0  # Extra Schaden durch Umgebung
    xp_gained: Dict[str, int] = field(default_factory=dict)
    message: str = ""


# Skill-Anforderungen fuer Griff-Moves
GRAB_MOVE_REQUIREMENTS = {
    GrabMoveType.SUPLEX: {"throw": 15, "strength": 12},
    GrabMoveType.CHOKESLAM: {"throw": 10, "strength": 10},
    GrabMoveType.THROW_OBJECT: {"throw": 5, "agility": 8},
    GrabMoveType.THROW_ENEMY: {"throw": 8, "strength": 10},
    GrabMoveType.RELEASE: {},  # Keine Anforderungen
}


class GrabThrowSystem:
    """
    GRAB & THROW SYSTEM
    ===================
    Wrestling-Style Greifen und Werfen!

    Features:
    - Gegner greifen (braucht Staerke + Skill)
    - Suplex (hoher Schaden, braucht Skill 15)
    - Chokeslam (Gegner am Boden, braucht Skill 10)
    - In Objekte werfen (Umgebungs-Interaktion)
    - Gegner auf andere Gegner werfen!

    Learning by Doing:
    - throw Skill
    - grab Skill
    - environment Skill
    """

    def __init__(self, combat_system: 'HandCombatSystem'):
        self.combat_system = combat_system
        self.grab_states: Dict[str, GrabState] = {}
        self.throw_skills: Dict[str, int] = {}  # player_id -> skill level
        self.throw_xp: Dict[str, int] = {}

    def grab(self, player_id: str, target_id: str) -> Dict:
        """
        Gegner greifen

        Erfolg basiert auf:
        - Staerke des Spielers
        - Grab-Skill Level
        - Gegner-Groesse/Staerke
        """
        if player_id not in self.combat_system.players:
            return {"success": False, "error": "Spieler nicht registriert"}

        player = self.combat_system.players[player_id]

        # Bereits am Greifen?
        if player_id in self.grab_states and self.grab_states[player_id].is_grabbing:
            return {"success": False, "error": "Du haeltst bereits jemanden!"}

        # Stamina-Kosten
        stamina_cost = 20
        if player.stamina < stamina_cost:
            return {"success": False, "error": f"Nicht genug Stamina! ({player.stamina}/{stamina_cost})"}

        # Erfolgs-Chance berechnen
        grab_skill = self.throw_skills.get(player_id, 1)
        base_chance = 0.5  # 50% Basis
        skill_bonus = grab_skill * 0.02  # +2% pro Level
        str_bonus = (player.strength - 10) * 0.02  # +2% pro STR ueber 10

        success_chance = min(0.95, base_chance + skill_bonus + str_bonus)

        # Stamina abziehen
        player.stamina -= stamina_cost

        # Wuerfel!
        import random
        if random.random() > success_chance:
            # XP auch bei Fehlschlag (weniger)
            self._gain_throw_xp(player_id, 5)
            return {
                "success": False,
                "error": "Griff verfehlt!",
                "stamina_cost": stamina_cost,
                "xp_gained": 5
            }

        # Erfolg!
        self.grab_states[player_id] = GrabState(
            is_grabbing=True,
            grabbed_target=target_id,
            grab_start_time=datetime.now()
        )

        # XP fuer erfolgreichen Griff
        xp = self._gain_throw_xp(player_id, 15)

        return {
            "success": True,
            "grabbed": target_id,
            "available_moves": ["suplex", "chokeslam", "throw_object", "throw_enemy", "release"],
            "time_limit": 5.0,  # Sekunden zum Entscheiden
            "stamina_cost": stamina_cost,
            "xp_gained": xp,
            "message": f"Gegner gegriffen! Waehle Follow-Up!"
        }

    def execute_grab_move(self, player_id: str, move: str) -> GrabMoveResult:
        """
        Fuehrt einen Griff-Move aus

        Moves:
        - suplex: Hoher Schaden, 2s Stun (Skill 15)
        - chokeslam: Mittlerer Schaden, 3s am Boden (Skill 10)
        - throw_object: In Umgebungs-Objekt werfen
        - throw_enemy: Auf anderen Gegner werfen
        - release: Loslassen
        """
        if player_id not in self.grab_states:
            return GrabMoveResult(False, GrabMoveType.RELEASE, message="Kein Griff aktiv!")

        grab_state = self.grab_states[player_id]
        if not grab_state.is_grabbing:
            return GrabMoveResult(False, GrabMoveType.RELEASE, message="Kein Griff aktiv!")

        # Zeit-Limit pruefen
        elapsed = (datetime.now() - grab_state.grab_start_time).total_seconds()
        if elapsed > grab_state.grab_duration_limit:
            self._release_grab(player_id)
            return GrabMoveResult(False, GrabMoveType.RELEASE, message="Griff-Zeit abgelaufen!")

        player = self.combat_system.players[player_id]
        throw_skill = self.throw_skills.get(player_id, 1)

        try:
            move_type = GrabMoveType(move)
        except ValueError:
            return GrabMoveResult(False, GrabMoveType.RELEASE, message=f"Unbekannter Move: {move}")

        # Anforderungen pruefen
        reqs = GRAB_MOVE_REQUIREMENTS.get(move_type, {})
        if reqs:
            if throw_skill < reqs.get("throw", 0):
                return GrabMoveResult(
                    False, move_type,
                    message=f"{move} benoetigt Wurf-Skill Level {reqs['throw']}! (Hast: {throw_skill})"
                )
            if player.strength < reqs.get("strength", 0):
                return GrabMoveResult(
                    False, move_type,
                    message=f"{move} benoetigt STR {reqs['strength']}! (Hast: {player.strength})"
                )

        # Move ausfuehren
        result = self._execute_move(player_id, move_type, player, throw_skill)

        # Griff beenden
        self._release_grab(player_id)

        return result

    def _execute_move(self, player_id: str, move_type: GrabMoveType,
                      player: PlayerCombatStats, throw_skill: int) -> GrabMoveResult:
        """Fuehrt den eigentlichen Move aus"""

        str_bonus = 1.0 + (player.strength - 10) * 0.03  # +3% pro STR ueber 10
        skill_bonus = 1.0 + throw_skill * 0.02  # +2% pro Skill Level

        if move_type == GrabMoveType.SUPLEX:
            damage = int(50 * str_bonus * skill_bonus)
            xp = self._gain_throw_xp(player_id, 25)
            return GrabMoveResult(
                success=True,
                move_type=move_type,
                damage=damage,
                stun_duration=2.0,
                xp_gained={"throw": xp},
                message=f"SUPLEX! {damage} Schaden + 2s Stun!"
            )

        elif move_type == GrabMoveType.CHOKESLAM:
            damage = int(40 * str_bonus * skill_bonus)
            xp = self._gain_throw_xp(player_id, 20)
            return GrabMoveResult(
                success=True,
                move_type=move_type,
                damage=damage,
                grounded_duration=3.0,
                xp_gained={"throw": xp},
                message=f"CHOKESLAM! {damage} Schaden + 3s am Boden!"
            )

        elif move_type == GrabMoveType.THROW_OBJECT:
            damage = int(30 * str_bonus * skill_bonus)
            env_bonus = int(20 * skill_bonus)  # Extra Objekt-Schaden
            xp = self._gain_throw_xp(player_id, 15)
            return GrabMoveResult(
                success=True,
                move_type=move_type,
                damage=damage,
                environment_bonus=env_bonus,
                stun_duration=1.5,
                xp_gained={"throw": xp},
                message=f"In Objekt geworfen! {damage}+{env_bonus} Schaden!"
            )

        elif move_type == GrabMoveType.THROW_ENEMY:
            damage = int(25 * str_bonus * skill_bonus)
            xp = self._gain_throw_xp(player_id, 20)
            return GrabMoveResult(
                success=True,
                move_type=move_type,
                damage=damage,  # Beide Gegner nehmen Schaden!
                grounded_duration=2.0,
                xp_gained={"throw": xp},
                message=f"Gegner auf Gegner geworfen! {damage} Schaden an beide!"
            )

        else:  # RELEASE
            return GrabMoveResult(
                success=True,
                move_type=GrabMoveType.RELEASE,
                message="Gegner losgelassen."
            )

    def _release_grab(self, player_id: str):
        """Griff beenden"""
        if player_id in self.grab_states:
            self.grab_states[player_id] = GrabState()

    def _gain_throw_xp(self, player_id: str, amount: int) -> int:
        """XP fuer Wurf-Skill (Learning by Doing!)"""
        if player_id not in self.throw_skills:
            self.throw_skills[player_id] = 1
        if player_id not in self.throw_xp:
            self.throw_xp[player_id] = 0

        self.throw_xp[player_id] += amount

        # Level-Up Check
        xp_needed = 100 + (self.throw_skills[player_id] * 50)
        while self.throw_xp[player_id] >= xp_needed:
            self.throw_xp[player_id] -= xp_needed
            self.throw_skills[player_id] += 1
            xp_needed = 100 + (self.throw_skills[player_id] * 50)

        return amount

    def get_throw_skill(self, player_id: str) -> Dict:
        """Aktueller Wurf-Skill Status"""
        level = self.throw_skills.get(player_id, 1)
        xp = self.throw_xp.get(player_id, 0)
        xp_needed = 100 + (level * 50)

        return {
            "level": level,
            "xp": xp,
            "xp_needed": xp_needed,
            "unlocked_moves": self._get_unlocked_moves(level)
        }

    def _get_unlocked_moves(self, level: int) -> List[str]:
        """Welche Moves sind bei diesem Level freigeschaltet?"""
        unlocked = ["release", "throw_object"]
        if level >= 5:
            unlocked.append("throw_enemy")
        if level >= 10:
            unlocked.append("chokeslam")
        if level >= 15:
            unlocked.append("suplex")
        return unlocked


# =============================================================================
# TIDS - TRITT IN DEN SCHRITT (Gag Move!)
# =============================================================================

@dataclass
class TIDSResult:
    """Ergebnis eines TIDS-Angriffs"""
    success: bool
    damage: int = 1  # Symbolischer Schaden
    stun_duration: float = 3.0  # 3 Sekunden Stun
    flee_bonus: float = 0.9  # +90% Flucht-Chance
    flee_duration: float = 5.0  # 5 Sekunden
    message: str = ""
    gag_message: str = ""  # Lustige Reaktion des Gegners
    cooldown_remaining: float = 0.0
    is_gag: bool = True  # Immer ein Gag!


# Lustige Reaktionen je nach Monster-Typ
TIDS_GAG_REACTIONS: Dict[str, List[str]] = {
    "slime": [
        "Der Slime wabbelt verwirrt... Wo sollte das treffen?!",
        "Dein Fuss versinkt im Slime... IGITT!",
        "Der Slime teilt sich kurz und formt sich wieder. Er sieht... beleidigt aus?",
        "*PLATSCH* Der Slime ist jetzt an deinem Bein. Toll gemacht.",
        "Der Slime gluckert fragend. Hat er ueberhaupt einen Schritt?",
    ],
    "skeleton": [
        "Dein Fuss geht zwischen den Knochen durch. Der Skelett lacht klapprig.",
        "*KLAPPER* Die Beckenknochen fallen ab! ...und stehen wieder auf.",
        "Das Skelett schaut runter: 'Da war mal was, glaub ich...'",
        "KRITISCHER TREFFER! ...auf nichts. Skelette haben da nichts.",
    ],
    "ghost": [
        "Dein Fuss geht durch den Geist. Er guckt dich mitleidig an.",
        "Der Geist seufzt: 'Ich bin seit 300 Jahren tot. Das juckt mich nicht mehr.'",
        "Du trittst durch Ektoplasma. Dein Schuh ist jetzt klebrig.",
        "*WUUUUSCH* Der Geist weht kurz auseinander und formt sich wieder.",
    ],
    "golem": [
        "*KRACKS* AUTSCH! Dein Fuss tut weh! Der Golem ist aus STEIN!",
        "Der Golem merkt es nicht mal. Du humpelst jetzt.",
        "Granit. Du hast gegen Granit getreten. Gute Entscheidung.",
        "Der Golem: '...?' Er versteht nicht was du wolltest.",
    ],
    "dragon": [
        "Der Drache schaut verwirrt runter. Du bist winzig fuer ihn.",
        "Du erreichst nicht mal sein Knie. Peinlich.",
        "Der Drache lacht dich aus. FEURIG.",
        "Der Drache: 'War das ein Angriff? Niedlich.'",
    ],
    "spider": [
        "Welches Bein? Sie hat ACHT! Du trittst ins Leere.",
        "Die Spinne hat keine Ahnung was du wolltest.",
        "Du verhedderst dich in einem Netz. Toll gemacht.",
    ],
    "wolf": [
        "Der Wolf weicht aus und beisst dir ins Bein. AU!",
        "Woelfe sind zu schnell fuer TIDS!",
        "Der Wolf guckt dich an: 'Ernsthaft?'",
    ],
    "elemental": [
        "Du trittst in pures Feuer/Wasser/Erde/Luft. Das war dumm.",
        "Elementare haben keine Anatomie du Idiot!",
        "Das Elemental ist verwirrt ueber deine Lebensenscheidungen.",
    ],
    "humanoid": [
        "TIDS! Tritt in den Schritt! KRITISCHER TREFFER!",
        "DIREKT INS SCHWARZE! Der Gegner klappt zusammen!",
        "Das hat gesessen! 3 Sekunden pure Agonie!",
        "Der Gegner macht ein Geraeusch das nur Hunde hoeren koennen.",
        "FATALITY! ...Naja, fast. Aber es tut SEHR weh.",
    ],
    "robot": [
        "*CLONK* Metall. Du hast gegen Metall getreten.",
        "Der Roboter: 'SCHADEN ERKANNT: 0.001%' ...Peinlich.",
        "Dein Fuss tut weh. Der Roboter analysiert deine dumme Entscheidung.",
    ],
    "plant": [
        "Die Pflanze hat keinen Schritt. Sie ist eine PFLANZE.",
        "Du trittst in Dornen. AU AU AU!",
        "Die Pflanze ist verwirrt. Pflanzen sind immer verwirrt.",
    ],
    "fish": [
        "...Der Fisch ist im Wasser. Wie sollte das funktionieren?",
        "Der Fisch hat keine Beine. Und keinen Schritt.",
        "*BLUBB BLUBB* (Fisch-Lachen)",
    ],
    "blob": [
        "Dein Fuss versinkt. Der Blob absorbiert deinen Schuh.",
        "Der Blob teilt sich und reformiert. Er sieht gluecklich aus?",
        "TIDS gegen Blob = Blob gewinnt deinen Schuh.",
    ],
}


class TIDSSystem:
    """
    TIDS - TRITT IN DEN SCHRITT
    ===========================
    Der ultimative Gag-Move!

    JETZT MIT MONSTER-REAKTIONEN!
    - Funktioniert bei ALLEN Gegnern (ausser Bosse)
    - Unterschiedliche lustige Reaktionen je nach Typ
    - Bei Humanoiden: Voller Effekt (Stun + Flucht)
    - Bei Monstern: Gag-Reaktion (oft zum Nachteil des Spielers!)

    24 Stunden Cooldown!
    """

    def __init__(self):
        self.last_used: Dict[str, datetime] = {}
        self.cooldown_hours = 24

    def use_tids(self, player_id: str, target_type: str = "humanoid",
                 is_boss: bool = False, target_name: str = "") -> TIDSResult:
        """
        TIDS ausfuehren!

        Funktioniert bei ALLEN Gegnern - aber mit unterschiedlichen Effekten!
        - Humanoid: Voller Effekt (Stun + Flucht-Bonus)
        - Monster: Gag-Reaktion (meistens zum Nachteil des Spielers!)
        """
        now = datetime.now()
        import random

        # Cooldown pruefen
        if player_id in self.last_used:
            elapsed = (now - self.last_used[player_id]).total_seconds()
            cooldown_seconds = self.cooldown_hours * 3600
            if elapsed < cooldown_seconds:
                remaining = cooldown_seconds - elapsed
                remaining_hours = remaining / 3600
                return TIDSResult(
                    success=False,
                    cooldown_remaining=remaining_hours,
                    message=f"TIDS Cooldown! Noch {remaining_hours:.1f} Stunden."
                )

        # Nicht gegen Bosse! (Die haben zu viel Wuerde)
        if is_boss:
            return TIDSResult(
                success=False,
                message="Der Boss ist immun gegen TIDS! (Zu viel Wuerde... oder zu gross?)"
            )

        # Cooldown setzen (wird bei JEDEM Versuch verbraucht!)
        self.last_used[player_id] = now

        # Gag-Reaktion basierend auf Gegner-Typ
        target_lower = target_type.lower()
        reactions = TIDS_GAG_REACTIONS.get(target_lower, TIDS_GAG_REACTIONS.get("humanoid"))
        gag_message = random.choice(reactions)

        # Effekte basierend auf Gegner-Typ
        if target_lower == "humanoid":
            # Voller Effekt bei Humanoiden!
            return TIDSResult(
                success=True,
                damage=1,
                stun_duration=3.0,
                flee_bonus=0.9,
                flee_duration=5.0,
                message="TIDS! Tritt in den Schritt!",
                gag_message=gag_message,
                is_gag=True
            )

        elif target_lower in ["slime", "blob", "ghost", "elemental"]:
            # Koerperlose/Formlose: Kein Effekt, aber lustig
            return TIDSResult(
                success=True,  # "Erfolg" im Sinne von: Es passiert was Lustiges
                damage=0,
                stun_duration=0,
                flee_bonus=0,
                flee_duration=0,
                message=f"TIDS gegen {target_name or target_type}!",
                gag_message=gag_message,
                is_gag=True
            )

        elif target_lower in ["golem", "robot"]:
            # Harte Gegner: Spieler nimmt Schaden!
            return TIDSResult(
                success=True,
                damage=-5,  # NEGATIV = Spieler nimmt Schaden!
                stun_duration=0,
                flee_bonus=0,
                flee_duration=0,
                message=f"TIDS gegen {target_name or target_type}... AUTSCH!",
                gag_message=gag_message,
                is_gag=True
            )

        elif target_lower in ["skeleton"]:
            # Skelette: Kein Effekt, sie haben da nichts mehr
            return TIDSResult(
                success=True,
                damage=0,
                stun_duration=0.5,  # Kurz verwirrt
                flee_bonus=0,
                flee_duration=0,
                message=f"TIDS gegen {target_name or target_type}!",
                gag_message=gag_message,
                is_gag=True
            )

        elif target_lower in ["wolf", "spider", "dragon"]:
            # Schnelle/Grosse Tiere: Konter-Angriff!
            return TIDSResult(
                success=True,
                damage=-10,  # Konter-Schaden!
                stun_duration=0,
                flee_bonus=-0.2,  # MINUS Flucht-Chance (Gegner ist sauer!)
                flee_duration=3.0,
                message=f"TIDS gegen {target_name or target_type}... Das war keine gute Idee!",
                gag_message=gag_message,
                is_gag=True
            )

        elif target_lower in ["plant", "fish"]:
            # Absurde Ziele: Einfach nur lustig
            return TIDSResult(
                success=True,
                damage=0,
                stun_duration=0,
                flee_bonus=0,
                flee_duration=0,
                message=f"TIDS gegen {target_name or target_type}?! Warum?!",
                gag_message=gag_message,
                is_gag=True
            )

        else:
            # Unbekannter Typ: Standard-Gag
            return TIDSResult(
                success=True,
                damage=0,
                stun_duration=1.0,  # Bisschen verwirrt
                flee_bonus=0.3,  # Etwas Flucht-Bonus
                flee_duration=3.0,
                message=f"TIDS gegen {target_name or target_type}!",
                gag_message=f"Der {target_type} ist sehr verwirrt ueber deine Kampftechnik.",
                is_gag=True
            )

    def get_cooldown(self, player_id: str) -> Optional[float]:
        """Verbleibender Cooldown in Stunden"""
        if player_id not in self.last_used:
            return None

        now = datetime.now()
        elapsed = (now - self.last_used[player_id]).total_seconds()
        cooldown_seconds = self.cooldown_hours * 3600

        if elapsed >= cooldown_seconds:
            return None

        return (cooldown_seconds - elapsed) / 3600


# =============================================================================
# GLOBAL INSTANCES
# =============================================================================

_grab_system: Optional[GrabThrowSystem] = None
_tids_system: Optional[TIDSSystem] = None
_combat_system: Optional[HandCombatSystem] = None
_infuse_system: Optional[WeaponInfuseSystem] = None


def get_combat_system() -> HandCombatSystem:
    """Singleton fuer Combat System"""
    global _combat_system
    if _combat_system is None:
        _combat_system = HandCombatSystem()
    return _combat_system


def get_infuse_system() -> WeaponInfuseSystem:
    """Singleton fuer Weapon Infuse System"""
    global _infuse_system, _combat_system
    if _infuse_system is None:
        if _combat_system is None:
            _combat_system = HandCombatSystem()
        _infuse_system = WeaponInfuseSystem(_combat_system)
    return _infuse_system


def get_grab_system() -> GrabThrowSystem:
    """Singleton fuer Grab & Throw System"""
    global _grab_system, _combat_system
    if _grab_system is None:
        if _combat_system is None:
            _combat_system = HandCombatSystem()
        _grab_system = GrabThrowSystem(_combat_system)
    return _grab_system


def get_tids_system() -> TIDSSystem:
    """Singleton fuer TIDS System (Tritt In Den Schritt)"""
    global _tids_system
    if _tids_system is None:
        _tids_system = TIDSSystem()
    return _tids_system


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("NAJIKA COMBAT HANDS SYSTEM - TEST")
    print("=" * 70)

    system = get_combat_system()

    # Spieler erstellen
    print("\n--- Spieler erstellen ---")

    # Schwacher Spieler
    weak_player = PlayerCombatStats(
        strength=3, agility=3, intelligence=3,
        hp=80, max_hp=80, stamina=60, max_stamina=60, mana=40, max_mana=40
    )
    system.register_player("weak_guy", weak_player)

    # Starker Spieler
    strong_player = PlayerCombatStats(
        strength=15, agility=10, intelligence=8,
        hp=150, max_hp=150, stamina=120, max_stamina=120, mana=80, max_mana=80
    )
    strong_player.weapon_skills["sword"] = 25
    strong_player.weapon_skills["greatsword"] = 30
    system.register_player("strong_guy", strong_player)

    # Magier
    mage_player = PlayerCombatStats(
        strength=5, agility=6, intelligence=20,
        hp=70, max_hp=70, stamina=50, max_stamina=50, mana=200, max_mana=200
    )
    mage_player.magic_skills["fire"] = 40
    mage_player.magic_skills["arcane"] = 35
    system.register_player("mage", mage_player)

    # Test 1: Schwacher Spieler mit Zweihänder
    print("\n--- Test 1: Schwacher Spieler + Zweihänder ---")
    preview = system.get_weapon_preview("weak_guy", "zweihander")
    print(f"Waffe: {preview['weapon_name']}")
    print(f"Anforderungen: STR {preview['requirements']['strength']['required']} (hast {preview['requirements']['strength']['player']})")
    print(f"Effektivität: {preview['effectiveness']['total']*100:.0f}%")
    print(f"Dein Schaden: {preview['base_stats']['your_damage_heavy']} (Basis: {preview['base_stats']['damage_heavy']})")
    print(f"Risiken: Selbstverletzung {preview['risks']['self_damage_chance']}, Fumble {preview['risks']['fumble_chance']}")
    print(f"Warnungen: {preview['warnings']}")

    # Ausrüsten trotzdem
    system.equip_weapon("weak_guy", "zweihander", HandSlot.BOTH)

    # Angriff versuchen
    print("\n--- Schwacher Spieler greift an ---")
    for i in range(3):
        result = system.attack("weak_guy", HandSlot.BOTH, AttackType.HEAVY)
        print(f"  Angriff {i+1}: {result.message}")
        if result.warnings:
            for w in result.warnings:
                print(f"    {w}")

    # Test 2: Starker Spieler mit Zweihänder
    print("\n--- Test 2: Starker Spieler + Zweihänder ---")
    preview = system.get_weapon_preview("strong_guy", "zweihander")
    print(f"Effektivität: {preview['effectiveness']['total']*100:.0f}%")
    print(f"Dein Schaden: {preview['base_stats']['your_damage_heavy']}")
    print(f"Kann effektiv nutzen: {preview['can_use_effectively']}")

    system.equip_weapon("strong_guy", "zweihander", HandSlot.BOTH)

    print("\n--- Starker Spieler greift an ---")
    for i in range(3):
        result = system.attack("strong_guy", HandSlot.BOTH, AttackType.HEAVY)
        print(f"  Angriff {i+1}: {result.message}")

    # Test 3: Magier mit Dual-Cast
    print("\n--- Test 3: Magier + Dual-Cast ---")
    system.equip_weapon("mage", "fire_staff", HandSlot.LEFT)
    system.equip_weapon("mage", "fire_staff", HandSlot.RIGHT)

    # Schnellzauber-Perk freischalten
    system.unlock_perk("mage", "quickcast_apprentice")
    system.unlock_perk("mage", "fire_quickcast")

    result = system.attack("mage", HandSlot.BOTH, AttackType.DUAL_CAST)
    print(f"Dual-Cast: {result.message}")
    print(f"Schaden: {result.damage}")
    print(f"Cast-Zeit: {result.attack_time}s")
    print(f"Mana-Kosten: {result.mana_cost}")
    print(f"Spezial-Effekt: {result.special_effect}")

    # Test 4: Status anzeigen
    print("\n--- Status: Starker Spieler ---")
    status = system.get_player_status("strong_guy")
    print(f"Stats: STR {status['stats']['strength']}, AGI {status['stats']['agility']}")
    print(f"Waffen-Skills: {status['weapon_skills']}")

    print("\n" + "=" * 70)
    print("✅ Test abgeschlossen!")
    print("💪 Waffen-Anforderungen funktionieren!")
    print("⚠️ Schwache Spieler verletzen sich selbst!")
    print("🔮 Dual-Cast verstärkt Magie!")
    print("=" * 70)
