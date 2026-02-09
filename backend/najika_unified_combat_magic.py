"""
NAJIKA UNIFIED COMBAT & MAGIC SYSTEM
=====================================
Vereinigt:
- najika_combat_hands_system.py (Zwei-Hand-Kampf, Waffen-Anforderungen)
- najika_magic_system_v3.py (10 Magieschulen, Element-Weaving, Skyrim XP)

REGELN (8 GEBOTE!):
- Explosion = EIGENE Klasse, NIEMALS weaven!
- Skyrim Learning-by-Doing
- Port 8000 (NICHT 5000!)
- VATS ohne Zeitlupe (Pre-Combat Analyse)

Author: Claude Code Team
Date: 2026-02-06
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any, Union
import random
import copy
from datetime import datetime, timedelta


# =============================================================================
# ENUMS - VEREINIGT
# =============================================================================

class HandSlot(Enum):
    """Welche Hand"""
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class AttackType(Enum):
    """Angriffsart"""
    LIGHT = "light"
    HEAVY = "heavy"
    DUAL_CAST = "dual_cast"
    COMBO = "combo"
    SPELL = "spell"  # NEU: Expliziter Zauber


class WeaponCategory(Enum):
    """Waffen-Kategorien"""
    # Einhand-Waffen
    SWORD = "sword"
    DAGGER = "dagger"
    AXE = "axe"
    MACE = "mace"

    # Zweihand-Waffen
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
    TOME = "tome"

    # Defensiv
    SHIELD = "shield"

    # Spezial
    FIST = "fist"
    WHIP = "whip"


class MagicSchool(Enum):
    """Die 10 Magieschulen - ALLE sind fuer JEDEN lernbar!"""
    # Elemente (koennen VERWEBEN - ausser Explosion!)
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    WIND = "wind"
    LIGHTNING = "lightning"
    ICE = "ice"
    NATURE = "nature"
    DARK = "dark"
    LIGHT = "light"

    # EXPLOSION - NICHT verweben! Eigener Pfad
    EXPLOSION = "explosion"


class DamageType(Enum):
    """Schadenstypen - erweitert mit allen Magieschulen"""
    PHYSICAL = "physical"
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    WIND = "wind"
    ICE = "ice"
    LIGHTNING = "lightning"
    NATURE = "nature"
    DARK = "dark"
    LIGHT = "light"
    EXPLOSION = "explosion"

    # Weave-Kombinationen
    STEAM = "steam"         # Fire + Water
    FIRESTORM = "firestorm" # Fire + Wind
    MAGMA = "magma"         # Fire + Earth
    BLIZZARD = "blizzard"   # Water + Wind
    MUD = "mud"             # Water + Earth
    SHOCK = "shock"         # Lightning + Water
    TEMPEST = "tempest"     # Lightning + Wind
    SANDSTORM = "sandstorm" # Earth + Wind
    THERMAL = "thermal"     # Ice + Fire
    VOID = "void"           # Dark + Light


class BodyPart(Enum):
    """Koerperteile fuer VATS-Style Targeting"""
    HEAD = "head"
    TORSO = "torso"
    LEFT_ARM = "left_arm"
    RIGHT_ARM = "right_arm"
    LEFT_LEG = "left_leg"
    RIGHT_LEG = "right_leg"


# =============================================================================
# ELEMENT WEAVING (NICHT fuer Explosion!)
# =============================================================================

ELEMENT_WEAVES: Dict[Tuple[str, str], Dict] = {
    ("fire", "water"): {"result": DamageType.STEAM, "name": "Dampf", "effect": "Blind, AoE Schaden"},
    ("fire", "wind"): {"result": DamageType.FIRESTORM, "name": "Feuersturm", "effect": "Groesserer AoE"},
    ("fire", "earth"): {"result": DamageType.MAGMA, "name": "Magma", "effect": "DoT + Slow"},
    ("water", "wind"): {"result": DamageType.BLIZZARD, "name": "Blizzard", "effect": "AoE Freeze"},
    ("water", "earth"): {"result": DamageType.MUD, "name": "Schlamm", "effect": "Root, Slow"},
    ("lightning", "water"): {"result": DamageType.SHOCK, "name": "Schock", "effect": "Chain Lightning"},
    ("lightning", "wind"): {"result": DamageType.TEMPEST, "name": "Sturm", "effect": "Random Strikes"},
    ("earth", "wind"): {"result": DamageType.SANDSTORM, "name": "Sandsturm", "effect": "Blind, DoT"},
    ("ice", "fire"): {"result": DamageType.THERMAL, "name": "Thermal", "effect": "Bonus vs Armor"},
    ("dark", "light"): {"result": DamageType.VOID, "name": "Leere", "effect": "True Damage"},
}


def get_weave_result(school1: MagicSchool, school2: MagicSchool) -> Optional[Dict]:
    """Prueft ob zwei Schulen verwoben werden koennen"""
    if school1 == MagicSchool.EXPLOSION or school2 == MagicSchool.EXPLOSION:
        return None  # Explosion NIEMALS weaven!

    key1 = (school1.value, school2.value)
    key2 = (school2.value, school1.value)

    return ELEMENT_WEAVES.get(key1) or ELEMENT_WEAVES.get(key2)


# =============================================================================
# FALLOUT S.P.E.C.I.A.L. STATS
# =============================================================================

@dataclass
class PlayerStats:
    """Fallout-Style Basis-Attribute + Ressourcen + Skills"""
    # S.P.E.C.I.A.L. (1-15)
    strength: int = 5
    perception: int = 5
    endurance: int = 5
    charisma: int = 5
    intelligence: int = 5
    agility: int = 5
    luck: int = 5

    # Ressourcen
    hp: int = 100
    max_hp: int = 100
    stamina: int = 100
    max_stamina: int = 100
    mana: int = 100
    max_mana: int = 100

    # Waffen-Skills (Skyrim Learning by Doing) - 1-100
    weapon_skills: Dict[str, int] = field(default_factory=lambda: {
        "sword": 1, "dagger": 1, "axe": 1, "mace": 1, "spear": 1,
        "staff": 1, "shield": 1, "fist": 1, "bow": 1, "gun": 1,
        "greatsword": 1, "greataxe": 1, "warhammer": 1
    })

    # Magie-Skills - 1-100
    magic_skills: Dict[str, int] = field(default_factory=lambda: {
        "fire": 1, "water": 1, "earth": 1, "wind": 1,
        "ice": 1, "lightning": 1, "nature": 1, "dark": 1, "light": 1,
        "explosion": 1, "arcane": 1, "restoration": 1
    })

    # School Mastery (0-100) - fuer Weaving-Boni
    school_mastery: Dict[str, int] = field(default_factory=lambda: {
        school.value: 0 for school in MagicSchool
    })

    # XP-Tracking
    weapon_xp: Dict[str, int] = field(default_factory=dict)
    magic_xp: Dict[str, int] = field(default_factory=dict)

    # Najika-Spezial
    is_najika: bool = False


# =============================================================================
# SKILL SYSTEM (Skyrim + ESO Morphs)
# =============================================================================

@dataclass
class Skill:
    """Ein einzelner Skill (Magie oder Waffentechnik)"""
    id: str
    name: str
    name_de: str
    school: MagicSchool

    # Level (1-100 Skyrim-Style)
    level: int = 1
    xp: int = 0
    xp_to_next: int = 100

    # Kosten
    mana_cost: int = 0
    stamina_cost: int = 0

    # Effekte
    base_damage: int = 0
    base_heal: int = 0
    effect_type: str = "damage"  # damage, heal, buff, debuff, summon

    # Timing
    cast_time: float = 0.5
    cooldown: float = 0.0

    # Range
    range_meters: float = 10.0
    aoe_radius: float = 0.0

    # Morph-System (ESO-Style)
    morph_available_at: int = 25
    morph_chosen: Optional[str] = None
    morph_options: List[str] = field(default_factory=list)

    # Spezial
    status_effect: Optional[str] = None  # burn, freeze, stun, etc.
    status_duration: float = 0.0

    def use(self) -> Dict:
        """Skill nutzen = XP gewinnen (Skyrim!)"""
        xp_gain = random.randint(5, 15)
        self.xp += xp_gain

        leveled_up = False
        new_level = self.level

        while self.xp >= self.xp_to_next and self.level < 100:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.15)
            leveled_up = True
            new_level = self.level

        return {
            "xp_gained": xp_gain,
            "new_level": new_level,
            "leveled_up": leveled_up,
            "morph_available": self.level >= self.morph_available_at and not self.morph_chosen
        }

    def calculate_power(self, stats: PlayerStats) -> int:
        """Berechne Staerke basierend auf Stats"""
        base = self.base_damage or self.base_heal

        if self.school == MagicSchool.EXPLOSION:
            # Explosion skaliert mit INT + LUCK
            multiplier = 1 + (stats.intelligence * 0.05) + (stats.luck * 0.02)
        else:
            # Normale Magie skaliert mit INT
            multiplier = 1 + (stats.intelligence * 0.05)

        # Skill-Level Bonus (+2% pro Level)
        level_bonus = 1 + (self.level * 0.02)

        # School Mastery Bonus
        mastery = stats.school_mastery.get(self.school.value, 0)
        mastery_bonus = 1 + (mastery * 0.005)  # +0.5% pro Mastery

        return int(base * multiplier * level_bonus * mastery_bonus)


@dataclass
class ExplosionSkill(Skill):
    """
    EXPLOSION - Konosuba-Style!
    - Kostet viel Mana + Stamina
    - Finisher 1x pro Tag (nur Najika hat Tier 3!)
    """
    tier: int = 1
    finisher_used_today: bool = False
    finisher_last_used: Optional[datetime] = None
    weapon_morph: Optional[str] = None

    def __post_init__(self):
        self.school = MagicSchool.EXPLOSION
        self.mana_cost = 50 + (self.tier * 30)
        self.stamina_cost = 30 + (self.tier * 20)
        self.base_damage = 100 + (self.tier * 100)
        self.cast_time = 3.0 + (self.tier * 1.0)  # Minimum 3 Sekunden!
        self.aoe_radius = 5.0 + (self.tier * 3.0)

    def can_use_finisher(self) -> bool:
        """Finisher 1x pro Tag"""
        if self.finisher_used_today:
            return False
        if self.finisher_last_used:
            time_since = datetime.now() - self.finisher_last_used
            return time_since > timedelta(hours=24)
        return True

    def use_finisher(self, is_najika: bool = False) -> Dict:
        """FINISHER - 1x pro Tag! Najika hat Tier 3"""
        if not self.can_use_finisher():
            return {"success": False, "error": "Finisher bereits heute genutzt!"}

        self.finisher_used_today = True
        self.finisher_last_used = datetime.now()

        # Najika exklusiv: Tier 3 Omega-Detonation
        finisher_tier = 3 if is_najika else min(self.tier, 2)

        damage_multiplier = {1: 3.0, 2: 5.0, 3: 10.0}[finisher_tier]

        return {
            "success": True,
            "finisher_tier": finisher_tier,
            "damage": int(self.base_damage * damage_multiplier),
            "effect": "EXPLOSION!!!" if finisher_tier < 3 else "OMEGA-DETONATION!!!",
            "aoe_radius": self.aoe_radius * (1 + finisher_tier * 0.5),
            "cooldown_hours": 24,
            "exhaustion": True  # Nach Finisher: erschoepft!
        }


# =============================================================================
# SKILL DATABASE - Alle Magieschulen
# =============================================================================

def create_skill_database() -> Dict[str, Skill]:
    """Erstellt die komplette Skill-Datenbank"""
    return {
        # ========== FEUER ==========
        "fireball": Skill(
            "fireball", "Fireball", "Feuerball", MagicSchool.FIRE,
            mana_cost=15, base_damage=30, effect_type="damage",
            cast_time=0.6, range_meters=12, aoe_radius=2,
            status_effect="burn", status_duration=3.0,
            morph_options=["meteor", "fire_stream"]
        ),
        "fire_shield": Skill(
            "fire_shield", "Fire Shield", "Feuerschild", MagicSchool.FIRE,
            mana_cost=25, effect_type="buff",
            cast_time=0.8, status_duration=30.0,
            morph_options=["flame_cloak", "fire_reflect"]
        ),
        "inferno": Skill(
            "inferno", "Inferno", "Inferno", MagicSchool.FIRE,
            mana_cost=50, base_damage=80, effect_type="damage",
            cast_time=2.0, range_meters=8, aoe_radius=6,
            status_effect="burn", status_duration=6.0,
            morph_options=["hellfire", "flame_pillar"]
        ),

        # ========== WASSER ==========
        "heal": Skill(
            "heal", "Heal", "Heilung", MagicSchool.WATER,
            mana_cost=20, base_heal=40, effect_type="heal",
            cast_time=0.8, range_meters=5,
            morph_options=["greater_heal", "heal_over_time"]
        ),
        "water_shield": Skill(
            "water_shield", "Water Shield", "Wasserschild", MagicSchool.WATER,
            mana_cost=20, effect_type="buff",
            cast_time=0.6, status_duration=20.0,
            morph_options=["absorb_shield", "cleanse_shield"]
        ),
        "tidal_wave": Skill(
            "tidal_wave", "Tidal Wave", "Flutwelle", MagicSchool.WATER,
            mana_cost=45, base_damage=55, effect_type="damage",
            cast_time=1.5, range_meters=15, aoe_radius=8,
            status_effect="slow", status_duration=4.0,
            morph_options=["tsunami", "whirlpool"]
        ),

        # ========== ERDE ==========
        "stone_armor": Skill(
            "stone_armor", "Stone Armor", "Steinpanzer", MagicSchool.EARTH,
            mana_cost=30, effect_type="buff",
            cast_time=1.0, status_duration=45.0,
            morph_options=["obsidian_armor", "earth_spikes"]
        ),
        "earthquake": Skill(
            "earthquake", "Earthquake", "Erdbeben", MagicSchool.EARTH,
            mana_cost=40, base_damage=50, effect_type="damage",
            cast_time=1.8, range_meters=0, aoe_radius=10,
            status_effect="stagger", status_duration=2.0,
            morph_options=["fissure", "tremor"]
        ),
        "rock_throw": Skill(
            "rock_throw", "Rock Throw", "Steinwurf", MagicSchool.EARTH,
            mana_cost=12, stamina_cost=8, base_damage=25, effect_type="damage",
            cast_time=0.4, range_meters=15,
            morph_options=["boulder", "gravel_spray"]
        ),

        # ========== WIND ==========
        "haste": Skill(
            "haste", "Haste", "Eile", MagicSchool.WIND,
            mana_cost=15, effect_type="buff",
            cast_time=0.3, status_duration=20.0,
            morph_options=["group_haste", "combat_speed"]
        ),
        "wind_blade": Skill(
            "wind_blade", "Wind Blade", "Windklinge", MagicSchool.WIND,
            mana_cost=18, base_damage=25, effect_type="damage",
            cast_time=0.25, range_meters=10,
            morph_options=["air_slash", "tornado"]
        ),
        "gust": Skill(
            "gust", "Gust", "Windstoss", MagicSchool.WIND,
            mana_cost=10, base_damage=15, effect_type="damage",
            cast_time=0.2, range_meters=8,
            status_effect="knockback", status_duration=0.5,
            morph_options=["hurricane", "vacuum"]
        ),

        # ========== BLITZ ==========
        "lightning_bolt": Skill(
            "lightning_bolt", "Lightning Bolt", "Blitz", MagicSchool.LIGHTNING,
            mana_cost=25, base_damage=35, effect_type="damage",
            cast_time=0.3, range_meters=20,
            status_effect="stun", status_duration=0.5,
            morph_options=["chain_lightning", "thunder_strike"]
        ),
        "shock_field": Skill(
            "shock_field", "Shock Field", "Schockfeld", MagicSchool.LIGHTNING,
            mana_cost=35, base_damage=20, effect_type="damage",
            cast_time=0.8, range_meters=0, aoe_radius=6,
            status_effect="paralysis", status_duration=1.0,
            morph_options=["static_cage", "lightning_storm"]
        ),

        # ========== EIS ==========
        "frost_spike": Skill(
            "frost_spike", "Frost Spike", "Eiszapfen", MagicSchool.ICE,
            mana_cost=15, base_damage=28, effect_type="damage",
            cast_time=0.5, range_meters=12,
            status_effect="slow", status_duration=3.0,
            morph_options=["ice_lance", "frost_nova"]
        ),
        "freeze": Skill(
            "freeze", "Freeze", "Einfrieren", MagicSchool.ICE,
            mana_cost=35, base_damage=15, effect_type="debuff",
            cast_time=1.2, range_meters=8,
            status_effect="freeze", status_duration=4.0,
            morph_options=["deep_freeze", "ice_prison"]
        ),
        "blizzard_spell": Skill(
            "blizzard_spell", "Blizzard", "Schneesturm", MagicSchool.ICE,
            mana_cost=60, base_damage=45, effect_type="damage",
            cast_time=2.5, range_meters=0, aoe_radius=12,
            status_effect="freeze", status_duration=2.0,
            morph_options=["absolute_zero", "ice_age"]
        ),

        # ========== NATUR ==========
        "summon_wolf": Skill(
            "summon_wolf", "Summon Wolf", "Wolf beschwoeren", MagicSchool.NATURE,
            mana_cost=40, effect_type="summon",
            cast_time=2.0, status_duration=120.0,
            morph_options=["dire_wolf", "pack_wolves"]
        ),
        "entangle": Skill(
            "entangle", "Entangle", "Verstricken", MagicSchool.NATURE,
            mana_cost=20, effect_type="debuff",
            cast_time=0.6, range_meters=10, aoe_radius=4,
            status_effect="root", status_duration=5.0,
            morph_options=["thorns", "vine_grab"]
        ),
        "rejuvenation": Skill(
            "rejuvenation", "Rejuvenation", "Verjuengung", MagicSchool.NATURE,
            mana_cost=30, base_heal=15, effect_type="heal",
            cast_time=0.5, range_meters=8,
            status_effect="regen", status_duration=10.0,
            morph_options=["bloom", "lifebloom"]
        ),

        # ========== DUNKEL ==========
        "drain_life": Skill(
            "drain_life", "Drain Life", "Leben entziehen", MagicSchool.DARK,
            mana_cost=30, base_damage=25, base_heal=20, effect_type="damage",
            cast_time=1.0, range_meters=6,
            morph_options=["soul_drain", "mass_drain"]
        ),
        "curse": Skill(
            "curse", "Curse", "Fluch", MagicSchool.DARK,
            mana_cost=25, effect_type="debuff",
            cast_time=0.8, range_meters=12,
            status_effect="weakness", status_duration=15.0,
            morph_options=["hex", "doom"]
        ),
        "shadow_bolt": Skill(
            "shadow_bolt", "Shadow Bolt", "Schattenblitz", MagicSchool.DARK,
            mana_cost=20, base_damage=32, effect_type="damage",
            cast_time=0.6, range_meters=15,
            morph_options=["void_bolt", "shadow_barrage"]
        ),

        # ========== LICHT ==========
        "blessing": Skill(
            "blessing", "Blessing", "Segen", MagicSchool.LIGHT,
            mana_cost=20, effect_type="buff",
            cast_time=0.5, range_meters=10,
            status_duration=60.0,
            morph_options=["greater_blessing", "aura"]
        ),
        "smite": Skill(
            "smite", "Smite", "Heiliges Licht", MagicSchool.LIGHT,
            mana_cost=25, base_damage=35, effect_type="damage",
            cast_time=0.7, range_meters=12,
            status_effect="blind", status_duration=2.0,
            morph_options=["holy_fire", "purify"]
        ),
        "sanctuary": Skill(
            "sanctuary", "Sanctuary", "Schutzzone", MagicSchool.LIGHT,
            mana_cost=50, effect_type="buff",
            cast_time=1.5, aoe_radius=8,
            status_duration=20.0,
            morph_options=["divine_barrier", "holy_ground"]
        ),

        # ========== EXPLOSION (Konosuba!) ==========
        "explosion_basic": ExplosionSkill(
            id="explosion_basic", name="Explosion", name_de="Explosion",
            school=MagicSchool.EXPLOSION, tier=1,
            morph_options=[]
        ),
        "explosion_advanced": ExplosionSkill(
            id="explosion_advanced", name="EXPLOOOOSION!", name_de="EXPLOOOOSION!",
            school=MagicSchool.EXPLOSION, tier=2,
            morph_options=[]
        ),
        "explosion_ultimate": ExplosionSkill(
            id="explosion_ultimate", name="OMEGA-DETONATION", name_de="OMEGA-DETONATION",
            school=MagicSchool.EXPLOSION, tier=3,
            morph_options=[]
        ),
    }


SKILL_DATABASE = create_skill_database()


# =============================================================================
# WAFFEN-ANFORDERUNGEN (aus combat_hands_system)
# =============================================================================

@dataclass
class WeaponRequirements:
    """Anforderungen um eine Waffe EFFEKTIV zu nutzen"""
    strength: int = 0
    agility: int = 0
    intelligence: int = 0
    skill_level: int = 1
    weight: float = 1.0
    two_handed: bool = False


WEAPON_REQUIREMENTS: Dict[str, WeaponRequirements] = {
    # Schwerter
    "rusty_sword": WeaponRequirements(strength=3, agility=2, skill_level=1, weight=2.0),
    "iron_sword": WeaponRequirements(strength=5, agility=3, skill_level=5, weight=3.0),
    "steel_sword": WeaponRequirements(strength=7, agility=4, skill_level=10, weight=3.5),
    "flame_blade": WeaponRequirements(strength=6, agility=4, intelligence=3, skill_level=15, weight=3.0),
    "katana": WeaponRequirements(strength=4, agility=8, skill_level=25, weight=2.0),

    # Zweihand
    "zweihander": WeaponRequirements(strength=15, agility=5, skill_level=20, weight=12.0, two_handed=True),
    "dragon_slayer": WeaponRequirements(strength=25, agility=5, skill_level=50, weight=25.0, two_handed=True),

    # Haemmer
    "war_hammer": WeaponRequirements(strength=20, agility=2, skill_level=20, weight=18.0, two_handed=True),
    "titan_crusher": WeaponRequirements(strength=30, agility=2, skill_level=50, weight=35.0, two_handed=True),

    # Dolche
    "rusty_dagger": WeaponRequirements(strength=1, agility=3, skill_level=1, weight=0.5),
    "assassin_blade": WeaponRequirements(strength=2, agility=8, skill_level=15, weight=0.8),

    # Staebe (INT-basiert)
    "wooden_staff": WeaponRequirements(strength=2, agility=2, intelligence=5, skill_level=1, weight=1.5),
    "fire_staff": WeaponRequirements(strength=2, agility=2, intelligence=10, skill_level=10, weight=2.0),
    "megumin_staff": WeaponRequirements(strength=1, agility=1, intelligence=25, skill_level=50, weight=1.0),

    # Schilde
    "wooden_shield": WeaponRequirements(strength=4, agility=2, skill_level=1, weight=3.0),
    "tower_shield": WeaponRequirements(strength=15, agility=1, skill_level=20, weight=15.0),

    # Faeuste
    "bare_fists": WeaponRequirements(strength=1, agility=1, skill_level=1, weight=0),
    "brass_knuckles": WeaponRequirements(strength=3, agility=4, skill_level=5, weight=0.5),
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

    # Schaden
    damage_light: int
    damage_heavy: int

    # Kosten
    stamina_light: int
    stamina_heavy: int
    mana_light: int = 0
    mana_heavy: int = 0

    # Timing
    speed_light: float = 0.4
    speed_heavy: float = 0.8
    cast_time: float = 0.0

    # Range
    range_meters: float = 2.0

    # Typ
    damage_type: DamageType = DamageType.PHYSICAL
    magic_school: Optional[MagicSchool] = None

    # Spezial
    special: Optional[str] = None
    crit_chance: float = 0.05

    # Hand
    hand_slot: HandSlot = HandSlot.RIGHT


WEAPONS_DB: Dict[str, WeaponData] = {
    # Schwerter
    "rusty_sword": WeaponData(
        "rusty_sword", "Rusty Sword", "Rostiges Schwert",
        WeaponCategory.SWORD, 15, 30, 10, 25
    ),
    "iron_sword": WeaponData(
        "iron_sword", "Iron Sword", "Eisenschwert",
        WeaponCategory.SWORD, 22, 45, 12, 28
    ),
    "flame_blade": WeaponData(
        "flame_blade", "Flame Blade", "Flammenklinge",
        WeaponCategory.SWORD, 18, 38, 15, 32,
        damage_type=DamageType.FIRE, magic_school=MagicSchool.FIRE
    ),
    "katana": WeaponData(
        "katana", "Katana", "Katana",
        WeaponCategory.SWORD, 24, 48, 10, 22,
        speed_light=0.25, speed_heavy=0.5, crit_chance=0.2
    ),

    # Zweihand
    "zweihander": WeaponData(
        "zweihander", "Zweihander", "Zweihaender",
        WeaponCategory.GREATSWORD, 35, 80, 25, 50,
        speed_light=0.8, speed_heavy=1.5, range_meters=4.0,
        hand_slot=HandSlot.BOTH
    ),
    "dragon_slayer": WeaponData(
        "dragon_slayer", "Dragon Slayer", "Drachentoeter",
        WeaponCategory.GREATSWORD, 80, 180, 40, 80,
        speed_light=1.2, speed_heavy=2.5, range_meters=5.0,
        hand_slot=HandSlot.BOTH, special="dragon_bane"
    ),

    # Staebe
    "fire_staff": WeaponData(
        "fire_staff", "Fire Staff", "Feuerstab",
        WeaponCategory.STAFF, 18, 50, 5, 15, 15, 35,
        speed_light=0.6, speed_heavy=1.5, cast_time=0.8,
        range_meters=10, damage_type=DamageType.FIRE,
        magic_school=MagicSchool.FIRE, hand_slot=HandSlot.LEFT
    ),
    "megumin_staff": WeaponData(
        "megumin_staff", "Megumin's Explosion Staff", "Megumins Explosionsstab",
        WeaponCategory.STAFF, 5, 999, 5, 100, 5, 100,
        speed_light=0.3, speed_heavy=3.0, cast_time=5.0,
        range_meters=15, damage_type=DamageType.EXPLOSION,
        magic_school=MagicSchool.EXPLOSION, hand_slot=HandSlot.LEFT,
        special="EXPLOSION"
    ),

    # Faeuste
    "bare_fists": WeaponData(
        "bare_fists", "Bare Fists", "Blosse Faeuste",
        WeaponCategory.FIST, 5, 12, 5, 12,
        speed_light=0.2, speed_heavy=0.4, range_meters=1.5
    ),
}


# =============================================================================
# EFFEKTIVITAETS-BERECHNUNG
# =============================================================================

@dataclass
class WeaponEffectiveness:
    """Ergebnis der Effektivitaets-Berechnung"""
    effectiveness: float
    damage_multiplier: float
    speed_multiplier: float
    stamina_multiplier: float
    self_damage_chance: float
    drop_weapon_chance: float
    fumble_chance: float
    warnings: List[str] = field(default_factory=list)
    can_use_effectively: bool = True


def calculate_weapon_effectiveness(weapon_id: str, player: PlayerStats) -> WeaponEffectiveness:
    """Berechnet Waffen-Effektivitaet"""
    if weapon_id not in WEAPON_REQUIREMENTS:
        return WeaponEffectiveness(1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0)

    reqs = WEAPON_REQUIREMENTS[weapon_id]
    warnings = []

    weapon_data = WEAPONS_DB.get(weapon_id)
    skill_name = weapon_data.category.value if weapon_data else "sword"
    player_skill = player.weapon_skills.get(skill_name, 1)

    # STR Check
    str_ratio = player.strength / max(reqs.strength, 1)
    if str_ratio < 0.5:
        str_eff, self_damage = 0.1, 0.3
        warnings.append(f"WARNUNG: Zu schwach! (STR {reqs.strength} noetig)")
    elif str_ratio < 0.75:
        str_eff, self_damage = 0.4, 0.15
    elif str_ratio < 1.0:
        str_eff, self_damage = 0.7, 0.05
    else:
        str_eff = min(1.0 + (str_ratio - 1.0) * 0.1, 1.2)
        self_damage = 0.0

    # AGI Check
    agi_ratio = player.agility / max(reqs.agility, 1)
    if agi_ratio < 0.5:
        agi_eff, drop_chance, fumble = 0.2, 0.25, 0.3
        warnings.append(f"WARNUNG: Zu ungeschickt! (AGI {reqs.agility} noetig)")
    elif agi_ratio < 0.75:
        agi_eff, drop_chance, fumble = 0.5, 0.1, 0.15
    elif agi_ratio < 1.0:
        agi_eff, drop_chance, fumble = 0.8, 0.03, 0.05
    else:
        agi_eff = min(1.0 + (agi_ratio - 1.0) * 0.1, 1.2)
        drop_chance, fumble = 0.0, 0.0

    # INT Check (fuer Magie-Waffen)
    if reqs.intelligence > 0:
        int_ratio = player.intelligence / max(reqs.intelligence, 1)
        if int_ratio < 0.5:
            int_eff = 0.1
            warnings.append(f"WARNUNG: Zu dumm fuer diese Waffe! (INT {reqs.intelligence} noetig)")
        elif int_ratio < 1.0:
            int_eff = 0.6 + (int_ratio * 0.4)
        else:
            int_eff = min(1.0 + (int_ratio - 1.0) * 0.15, 1.3)
    else:
        int_eff = 1.0

    # Skill Check
    skill_ratio = player_skill / max(reqs.skill_level, 1)
    if skill_ratio < 0.3:
        skill_eff = 0.1
        warnings.append(f"WARNUNG: Kaum Erfahrung! (Skill {player_skill}/{reqs.skill_level})")
        self_damage += 0.1
        drop_chance += 0.1
        fumble += 0.2
    elif skill_ratio < 0.6:
        skill_eff = 0.4
    elif skill_ratio < 1.0:
        skill_eff = 0.7 + (skill_ratio * 0.3)
    else:
        skill_eff = min(1.0 + (skill_ratio - 1.0) * 0.2, 1.5)

    # Gewicht -> Stamina
    weight_factor = reqs.weight / max(player.strength, 1)
    stamina_mult = 1.0 + max(0, (weight_factor - 1.0) * 0.5) if weight_factor > 1.0 else 1.0

    # Gesamt
    total = (str_eff * 0.3 + agi_eff * 0.25 + int_eff * 0.2 + skill_eff * 0.25)

    if total < 0.3:
        damage_mult = 0.1
    elif total < 0.5:
        damage_mult = 0.3
    elif total < 0.75:
        damage_mult = 0.6
    elif total < 1.0:
        damage_mult = 0.85
    else:
        damage_mult = total

    can_use = total >= 0.5 and len([w for w in warnings if "WARNUNG" in w]) == 0

    return WeaponEffectiveness(
        effectiveness=round(total, 2),
        damage_multiplier=round(damage_mult, 2),
        speed_multiplier=round(min(1.0, agi_eff), 2),
        stamina_multiplier=round(stamina_mult, 2),
        self_damage_chance=round(min(self_damage, 0.5), 2),
        drop_weapon_chance=round(min(drop_chance, 0.4), 2),
        fumble_chance=round(min(fumble, 0.5), 2),
        warnings=warnings,
        can_use_effectively=can_use
    )


# =============================================================================
# VATS-STYLE TARGETING
# =============================================================================

@dataclass
class TargetAnalysis:
    """VATS-Analyse OHNE Zeitlupe - Pre-Combat!"""
    target_name: str
    target_level: int = 1
    body_parts: Dict[BodyPart, Dict] = field(default_factory=dict)
    weakness_revealed: bool = False
    weaknesses: List[str] = field(default_factory=list)
    resistances: List[str] = field(default_factory=list)

    def analyze(self, perception: int, intelligence: int) -> Dict:
        """Analysiere Gegner vor dem Kampf"""
        analysis_skill = perception + (intelligence // 2)

        base_chances = {
            BodyPart.HEAD: 40,
            BodyPart.TORSO: 85,
            BodyPart.LEFT_ARM: 60,
            BodyPart.RIGHT_ARM: 60,
            BodyPart.LEFT_LEG: 55,
            BodyPart.RIGHT_LEG: 55,
        }

        damage_mods = {
            BodyPart.HEAD: 1.5,
            BodyPart.TORSO: 1.0,
            BodyPart.LEFT_ARM: 0.8,
            BodyPart.RIGHT_ARM: 0.8,
            BodyPart.LEFT_LEG: 0.7,
            BodyPart.RIGHT_LEG: 0.7,
        }

        effects = {
            BodyPart.HEAD: "Kritischer Treffer moeglich",
            BodyPart.TORSO: "Standard-Schaden",
            BodyPart.LEFT_ARM: "Kann entwaffnen",
            BodyPart.RIGHT_ARM: "Kann Schild entfernen",
            BodyPart.LEFT_LEG: "Verlangsamt Gegner",
            BodyPart.RIGHT_LEG: "Verlangsamt Gegner",
        }

        for part, base in base_chances.items():
            modified = min(95, base + (perception * 2))
            self.body_parts[part] = {
                "hit_chance": modified,
                "damage_mod": damage_mods[part],
                "effect": effects[part]
            }

        # INT enthuellt Schwaechen
        self.weakness_revealed = analysis_skill >= 12

        quality = "Detailliert" if analysis_skill >= 15 else "Gut" if analysis_skill >= 10 else "Basis"

        return {
            "target": self.target_name,
            "body_parts": {p.value: v for p, v in self.body_parts.items()},
            "weakness_revealed": self.weakness_revealed,
            "weaknesses": self.weaknesses if self.weakness_revealed else [],
            "resistances": self.resistances if self.weakness_revealed else [],
            "analysis_quality": quality
        }


# =============================================================================
# HAND LOADOUT
# =============================================================================

@dataclass
class HandLoadout:
    """Was in welcher Hand ist"""
    left_hand: Optional[str] = None      # Waffen-ID oder None
    right_hand: Optional[str] = None
    left_spell: Optional[str] = None     # Skill-ID
    right_spell: Optional[str] = None
    using_two_handed: bool = False
    two_handed_weapon: Optional[str] = None


# =============================================================================
# ATTACK RESULT
# =============================================================================

@dataclass
class CombatResult:
    """Ergebnis einer Combat-Aktion"""
    success: bool
    damage: int = 0
    heal: int = 0
    damage_type: DamageType = DamageType.PHYSICAL

    # Timing
    action_time: float = 0.0
    recovery_time: float = 0.0

    # Kosten
    stamina_cost: int = 0
    mana_cost: int = 0

    # Effekte
    status_applied: Optional[str] = None
    status_duration: float = 0.0
    special_effect: Optional[str] = None

    # Weaving
    is_weave: bool = False
    weave_type: Optional[str] = None
    weave_bonus: float = 1.0

    # Risiken
    self_damage: int = 0
    dropped_weapon: bool = False
    fumbled: bool = False

    # VATS
    targeted_part: Optional[str] = None

    # XP
    xp_gained: Dict[str, int] = field(default_factory=dict)
    skills_leveled: List[str] = field(default_factory=list)

    # Feedback
    message: str = ""
    warnings: List[str] = field(default_factory=list)


# =============================================================================
# UNIFIED COMBAT MAGIC SYSTEM
# =============================================================================

class UnifiedCombatMagicSystem:
    """
    Das vereinte Combat- und Magie-System fuer Najika World

    Features:
    - Zwei-Hand-Kampf (Waffen + Zauber)
    - 10 Magieschulen mit Element-Weaving
    - EXPLOSION als eigene Klasse (NIEMALS weaven!)
    - Skyrim Learning-by-Doing
    - VATS-Style Targeting (Pre-Combat)
    - Waffen-Anforderungen mit Konsequenzen
    - Schnellzauber-Perks
    """

    def __init__(self):
        self.players: Dict[str, PlayerStats] = {}
        self.loadouts: Dict[str, HandLoadout] = {}
        self.learned_skills: Dict[str, Dict[str, Skill]] = {}  # player_id -> skill_id -> Skill
        self.active_perks: Dict[str, List[str]] = {}

        # Cooldowns
        self.skill_cooldowns: Dict[str, Dict[str, datetime]] = {}

        # Daily limits
        self.daily_explosion_used: Dict[str, bool] = {}

    def register_player(
        self,
        player_id: str,
        stats: Optional[PlayerStats] = None,
        is_najika: bool = False
    ) -> PlayerStats:
        """Registriert einen Spieler"""
        if player_id not in self.players:
            player = stats or PlayerStats()
            player.is_najika = is_najika
            self.players[player_id] = player
            self.loadouts[player_id] = HandLoadout()
            self.learned_skills[player_id] = {}
            self.active_perks[player_id] = []
            self.skill_cooldowns[player_id] = {}
        return self.players[player_id]

    # =========================================================================
    # SKILL-MANAGEMENT
    # =========================================================================

    def learn_skill(self, player_id: str, skill_id: str) -> Dict:
        """Skill lernen"""
        if player_id not in self.players:
            return {"success": False, "error": "Spieler nicht registriert"}

        if skill_id in self.learned_skills.get(player_id, {}):
            return {"success": False, "error": "Skill bereits bekannt!"}

        if skill_id not in SKILL_DATABASE:
            return {"success": False, "error": f"Skill '{skill_id}' existiert nicht!"}

        # Kopie erstellen
        skill = copy.deepcopy(SKILL_DATABASE[skill_id])

        # Explosion Tier 3 nur fuer Najika
        if isinstance(skill, ExplosionSkill) and skill.tier >= 3:
            if not self.players[player_id].is_najika:
                return {"success": False, "error": "OMEGA-DETONATION ist Najika-exklusiv!"}

        self.learned_skills[player_id][skill_id] = skill

        return {
            "success": True,
            "skill_id": skill_id,
            "skill_name": skill.name_de,
            "school": skill.school.value,
            "message": f"Skill '{skill.name_de}' gelernt!"
        }

    def get_learned_skills(self, player_id: str) -> List[Dict]:
        """Alle gelernten Skills abrufen"""
        skills = self.learned_skills.get(player_id, {})
        return [{
            "id": s.id,
            "name": s.name_de,
            "school": s.school.value,
            "level": s.level,
            "mana_cost": s.mana_cost,
            "stamina_cost": s.stamina_cost,
            "morph_available": s.level >= s.morph_available_at and not s.morph_chosen
        } for s in skills.values()]

    # =========================================================================
    # EQUIPMENT
    # =========================================================================

    def equip_weapon(self, player_id: str, weapon_id: str, hand: HandSlot) -> Dict:
        """Waffe ausruesten"""
        if player_id not in self.players:
            return {"success": False, "error": "Spieler nicht registriert"}

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        weapon_data = WEAPONS_DB.get(weapon_id)
        if not weapon_data:
            return {"success": False, "error": f"Waffe '{weapon_id}' nicht gefunden"}

        reqs = WEAPON_REQUIREMENTS.get(weapon_id)
        if reqs and reqs.two_handed:
            loadout.left_hand = None
            loadout.right_hand = None
            loadout.using_two_handed = True
            loadout.two_handed_weapon = weapon_id
        else:
            loadout.using_two_handed = False
            loadout.two_handed_weapon = None
            if hand == HandSlot.LEFT:
                loadout.left_hand = weapon_id
            elif hand == HandSlot.RIGHT:
                loadout.right_hand = weapon_id
            else:
                loadout.left_hand = weapon_id
                loadout.right_hand = weapon_id

        effectiveness = calculate_weapon_effectiveness(weapon_id, player)

        return {
            "success": True,
            "weapon": weapon_id,
            "weapon_name": weapon_data.name_de,
            "hand": hand.value,
            "two_handed": reqs.two_handed if reqs else False,
            "effectiveness": effectiveness.effectiveness,
            "can_use_effectively": effectiveness.can_use_effectively,
            "warnings": effectiveness.warnings
        }

    def equip_spell(self, player_id: str, skill_id: str, hand: HandSlot) -> Dict:
        """Zauber in Hand ausruesten"""
        if player_id not in self.players:
            return {"success": False, "error": "Spieler nicht registriert"}

        if skill_id not in self.learned_skills.get(player_id, {}):
            return {"success": False, "error": f"Skill '{skill_id}' nicht gelernt!"}

        loadout = self.loadouts[player_id]
        skill = self.learned_skills[player_id][skill_id]

        if hand == HandSlot.LEFT:
            loadout.left_spell = skill_id
        elif hand == HandSlot.RIGHT:
            loadout.right_spell = skill_id
        else:
            loadout.left_spell = skill_id
            loadout.right_spell = skill_id

        return {
            "success": True,
            "skill": skill_id,
            "skill_name": skill.name_de,
            "hand": hand.value,
            "school": skill.school.value
        }

    # =========================================================================
    # COMBAT ACTIONS
    # =========================================================================

    def cast_spell(
        self,
        player_id: str,
        skill_id: str,
        hand: HandSlot = HandSlot.RIGHT,
        target: Optional[TargetAnalysis] = None,
        body_part: Optional[BodyPart] = None
    ) -> CombatResult:
        """Zauber wirken"""
        if player_id not in self.players:
            return CombatResult(False, message="Spieler nicht registriert")

        if skill_id not in self.learned_skills.get(player_id, {}):
            return CombatResult(False, message=f"Skill '{skill_id}' nicht gelernt!")

        player = self.players[player_id]
        skill = self.learned_skills[player_id][skill_id]

        # Kosten pruefen
        if player.mana < skill.mana_cost:
            return CombatResult(False, message=f"Nicht genug Mana! ({player.mana}/{skill.mana_cost})")
        if player.stamina < skill.stamina_cost:
            return CombatResult(False, message=f"Nicht genug Stamina!")

        # Explosion Finisher Check
        if isinstance(skill, ExplosionSkill) and skill.tier >= 2:
            if not skill.can_use_finisher():
                return CombatResult(False, message="Explosion-Finisher bereits heute genutzt!")

        # Kosten abziehen
        player.mana -= skill.mana_cost
        player.stamina -= skill.stamina_cost

        # Skill nutzen -> XP!
        use_result = skill.use()

        # School Mastery erhoehen
        school_key = skill.school.value
        player.school_mastery[school_key] = min(100, player.school_mastery.get(school_key, 0) + random.randint(1, 3))

        # Schaden/Heilung berechnen
        power = skill.calculate_power(player)

        # VATS Targeting
        targeted_part = None
        if target and body_part and body_part in target.body_parts:
            part_data = target.body_parts[body_part]
            hit_roll = random.randint(1, 100)
            if hit_roll > part_data["hit_chance"]:
                return CombatResult(
                    success=True,
                    damage=0,
                    message=f"Verfehlt! ({hit_roll} > {part_data['hit_chance']}%)"
                )
            power = int(power * part_data["damage_mod"])
            targeted_part = body_part.value

        # XP
        xp_gained = {"magic": use_result["xp_gained"]}
        skills_leveled = [skill_id] if use_result["leveled_up"] else []

        # Explosion Finisher
        if isinstance(skill, ExplosionSkill) and skill.tier >= 2:
            finisher = skill.use_finisher(is_najika=player.is_najika)
            if finisher["success"]:
                power = finisher["damage"]

        # Damage Type
        damage_type = DamageType[skill.school.value.upper()] if skill.school.value.upper() in DamageType.__members__ else DamageType.PHYSICAL

        return CombatResult(
            success=True,
            damage=power if skill.effect_type == "damage" else 0,
            heal=power if skill.effect_type == "heal" else 0,
            damage_type=damage_type,
            action_time=skill.cast_time,
            recovery_time=0.3,
            mana_cost=skill.mana_cost,
            stamina_cost=skill.stamina_cost,
            status_applied=skill.status_effect,
            status_duration=skill.status_duration,
            targeted_part=targeted_part,
            xp_gained=xp_gained,
            skills_leveled=skills_leveled,
            message=f"{skill.name_de}: {power} {'Schaden' if skill.effect_type == 'damage' else 'Heilung'}"
        )

    def weave_elements(
        self,
        player_id: str,
        skill1_id: str,
        skill2_id: str
    ) -> CombatResult:
        """
        Element-Verweben (ESO-Style)
        NICHT fuer Explosion!
        """
        if player_id not in self.players:
            return CombatResult(False, message="Spieler nicht registriert")

        skills = self.learned_skills.get(player_id, {})
        if skill1_id not in skills or skill2_id not in skills:
            return CombatResult(False, message="Skills nicht gelernt!")

        skill1 = skills[skill1_id]
        skill2 = skills[skill2_id]

        # Explosion NIEMALS weaven!
        if skill1.school == MagicSchool.EXPLOSION or skill2.school == MagicSchool.EXPLOSION:
            return CombatResult(
                False,
                message="EXPLOSION kann NICHT mit anderen Elementen verwoben werden! (8 Gebote!)"
            )

        weave = get_weave_result(skill1.school, skill2.school)
        if not weave:
            return CombatResult(
                False,
                message=f"{skill1.school.value} + {skill2.school.value} koennen nicht verwoben werden!"
            )

        player = self.players[player_id]
        total_mana = skill1.mana_cost + skill2.mana_cost
        total_stamina = skill1.stamina_cost + skill2.stamina_cost

        if player.mana < total_mana:
            return CombatResult(False, message=f"Nicht genug Mana! ({player.mana}/{total_mana})")

        player.mana -= total_mana
        player.stamina -= total_stamina

        # Beide Skills XP
        skill1.use()
        skill2.use()

        # Weave Power (30% Bonus!)
        power1 = skill1.calculate_power(player)
        power2 = skill2.calculate_power(player)
        weave_bonus = 1.3
        total_power = int((power1 + power2) * weave_bonus)

        return CombatResult(
            success=True,
            damage=total_power,
            damage_type=weave["result"],
            action_time=max(skill1.cast_time, skill2.cast_time) * 1.2,
            recovery_time=0.5,
            mana_cost=total_mana,
            stamina_cost=total_stamina,
            is_weave=True,
            weave_type=weave["name"],
            weave_bonus=weave_bonus,
            special_effect=weave["effect"],
            message=f"VERWEBEN: {weave['name'].upper()}! {total_power} Schaden!"
        )

    def weapon_attack(
        self,
        player_id: str,
        hand: HandSlot,
        attack_type: AttackType,
        target: Optional[TargetAnalysis] = None,
        body_part: Optional[BodyPart] = None
    ) -> CombatResult:
        """Waffen-Angriff"""
        if player_id not in self.players:
            return CombatResult(False, message="Spieler nicht registriert")

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        # Waffe bestimmen
        if loadout.using_two_handed:
            weapon_id = loadout.two_handed_weapon
        elif hand == HandSlot.LEFT:
            weapon_id = loadout.left_hand
        elif hand == HandSlot.RIGHT:
            weapon_id = loadout.right_hand
        else:
            weapon_id = loadout.right_hand or loadout.left_hand

        if not weapon_id:
            weapon_id = "bare_fists"

        weapon = WEAPONS_DB.get(weapon_id)
        if not weapon:
            return CombatResult(False, message=f"Waffe '{weapon_id}' nicht in DB")

        effectiveness = calculate_weapon_effectiveness(weapon_id, player)

        # Basis-Werte
        if attack_type == AttackType.HEAVY:
            base_damage = weapon.damage_heavy
            base_stamina = weapon.stamina_heavy
            base_time = weapon.speed_heavy
        else:
            base_damage = weapon.damage_light
            base_stamina = weapon.stamina_light
            base_time = weapon.speed_light

        # Effektivitaet anwenden
        final_damage = int(base_damage * effectiveness.damage_multiplier)
        final_stamina = int(base_stamina * effectiveness.stamina_multiplier)
        attack_time = base_time / effectiveness.speed_multiplier

        # Stamina Check
        if player.stamina < final_stamina:
            return CombatResult(False, message="Nicht genug Stamina!")

        player.stamina -= final_stamina

        # Risiko-Checks
        self_damage = 0
        dropped = False
        fumbled = False
        warnings = list(effectiveness.warnings)

        if random.random() < effectiveness.fumble_chance:
            fumbled = True
            final_damage = 0
            warnings.append("Angriff verfehlt! (Mangelnde Kontrolle)")

        if not fumbled and random.random() < effectiveness.self_damage_chance:
            self_damage = int(base_damage * 0.3 * (1 - effectiveness.effectiveness))
            player.hp = max(0, player.hp - self_damage)
            warnings.append(f"Selbstverletzung! ({self_damage} Schaden)")

        if random.random() < effectiveness.drop_weapon_chance:
            dropped = True
            if hand == HandSlot.LEFT:
                loadout.left_hand = None
            elif hand == HandSlot.RIGHT:
                loadout.right_hand = None
            else:
                loadout.two_handed_weapon = None
                loadout.using_two_handed = False
            warnings.append("Waffe fallen gelassen!")

        # VATS Targeting
        targeted_part = None
        if target and body_part and body_part in target.body_parts and not fumbled:
            part_data = target.body_parts[body_part]
            hit_roll = random.randint(1, 100)
            if hit_roll > part_data["hit_chance"]:
                return CombatResult(
                    success=True,
                    damage=0,
                    message=f"Verfehlt! ({hit_roll} > {part_data['hit_chance']}%)"
                )
            final_damage = int(final_damage * part_data["damage_mod"])
            targeted_part = body_part.value

        # XP (Skyrim!)
        xp_gained = {}
        if not fumbled:
            skill_name = weapon.category.value
            if skill_name in ["greatsword", "greataxe"]:
                skill_name = "sword" if "sword" in skill_name else "axe"

            xp_amount = 15 if attack_type == AttackType.HEAVY else 5
            if skill_name not in player.weapon_xp:
                player.weapon_xp[skill_name] = 0
            player.weapon_xp[skill_name] += xp_amount

            # Level-Up
            xp_needed = 100 + (player.weapon_skills.get(skill_name, 1) * 50)
            while player.weapon_xp[skill_name] >= xp_needed:
                player.weapon_xp[skill_name] -= xp_needed
                player.weapon_skills[skill_name] = player.weapon_skills.get(skill_name, 1) + 1
                xp_needed = 100 + (player.weapon_skills[skill_name] * 50)

            xp_gained["weapon"] = xp_amount

        message = f"Verfehlt!" if fumbled else f"{final_damage} Schaden mit {weapon.name_de}"
        if self_damage > 0:
            message += f" (Selbstverletzung: {self_damage})"

        return CombatResult(
            success=not fumbled,
            damage=final_damage,
            damage_type=weapon.damage_type,
            action_time=round(attack_time, 2),
            recovery_time=0.3,
            stamina_cost=final_stamina,
            special_effect=weapon.special,
            self_damage=self_damage,
            dropped_weapon=dropped,
            fumbled=fumbled,
            targeted_part=targeted_part,
            xp_gained=xp_gained,
            message=message,
            warnings=warnings
        )

    # =========================================================================
    # STATUS & EXPORT
    # =========================================================================

    def get_player_status(self, player_id: str) -> Dict:
        """Kompletter Spieler-Status"""
        if player_id not in self.players:
            return {"error": "Spieler nicht registriert"}

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
                "hp": player.hp, "max_hp": player.max_hp,
                "stamina": player.stamina, "max_stamina": player.max_stamina,
                "mana": player.mana, "max_mana": player.max_mana,
            },
            "loadout": {
                "left_hand": loadout.left_hand,
                "right_hand": loadout.right_hand,
                "left_spell": loadout.left_spell,
                "right_spell": loadout.right_spell,
                "two_handed": loadout.using_two_handed,
                "two_handed_weapon": loadout.two_handed_weapon,
            },
            "weapon_skills": player.weapon_skills,
            "magic_skills": player.magic_skills,
            "school_mastery": player.school_mastery,
            "learned_skills": list(self.learned_skills.get(player_id, {}).keys()),
            "is_najika": player.is_najika,
        }

    def export_state(self, player_id: str) -> Dict:
        """Exportiert Spieler-State fuer Save"""
        if player_id not in self.players:
            return {}

        player = self.players[player_id]
        loadout = self.loadouts[player_id]

        # Skills serialisieren
        skills_data = {}
        for skill_id, skill in self.learned_skills.get(player_id, {}).items():
            skills_data[skill_id] = {
                "level": skill.level,
                "xp": skill.xp,
                "morph_chosen": skill.morph_chosen,
            }
            if isinstance(skill, ExplosionSkill):
                skills_data[skill_id]["finisher_used_today"] = skill.finisher_used_today

        return {
            "stats": {
                "strength": player.strength, "perception": player.perception,
                "endurance": player.endurance, "charisma": player.charisma,
                "intelligence": player.intelligence, "agility": player.agility,
                "luck": player.luck,
            },
            "resources": {
                "hp": player.hp, "max_hp": player.max_hp,
                "stamina": player.stamina, "max_stamina": player.max_stamina,
                "mana": player.mana, "max_mana": player.max_mana,
            },
            "weapon_skills": player.weapon_skills,
            "weapon_xp": player.weapon_xp,
            "magic_skills": player.magic_skills,
            "magic_xp": player.magic_xp,
            "school_mastery": player.school_mastery,
            "loadout": {
                "left_hand": loadout.left_hand,
                "right_hand": loadout.right_hand,
                "left_spell": loadout.left_spell,
                "right_spell": loadout.right_spell,
                "two_handed_weapon": loadout.two_handed_weapon,
            },
            "learned_skills": skills_data,
            "perks": self.active_perks.get(player_id, []),
            "is_najika": player.is_najika,
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
        if "magic_skills" in state:
            player.magic_skills = state["magic_skills"]
        if "school_mastery" in state:
            player.school_mastery = state["school_mastery"]

        # XP
        if "weapon_xp" in state:
            player.weapon_xp = state["weapon_xp"]
        if "magic_xp" in state:
            player.magic_xp = state["magic_xp"]

        # Loadout
        if "loadout" in state:
            loadout.left_hand = state["loadout"].get("left_hand")
            loadout.right_hand = state["loadout"].get("right_hand")
            loadout.left_spell = state["loadout"].get("left_spell")
            loadout.right_spell = state["loadout"].get("right_spell")
            loadout.two_handed_weapon = state["loadout"].get("two_handed_weapon")
            loadout.using_two_handed = loadout.two_handed_weapon is not None

        # Learned Skills
        if "learned_skills" in state:
            for skill_id, skill_data in state["learned_skills"].items():
                if skill_id in SKILL_DATABASE:
                    skill = copy.deepcopy(SKILL_DATABASE[skill_id])
                    skill.level = skill_data.get("level", 1)
                    skill.xp = skill_data.get("xp", 0)
                    skill.morph_chosen = skill_data.get("morph_chosen")
                    if isinstance(skill, ExplosionSkill):
                        skill.finisher_used_today = skill_data.get("finisher_used_today", False)
                    self.learned_skills[player_id][skill_id] = skill

        # Perks
        if "perks" in state:
            self.active_perks[player_id] = state["perks"]

        # Najika
        if "is_najika" in state:
            player.is_najika = state["is_najika"]


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_system: Optional[UnifiedCombatMagicSystem] = None

def get_unified_combat_system() -> UnifiedCombatMagicSystem:
    """Singleton"""
    global _system
    if _system is None:
        _system = UnifiedCombatMagicSystem()
    return _system


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("NAJIKA UNIFIED COMBAT & MAGIC SYSTEM - TEST")
    print("=" * 70)

    system = get_unified_combat_system()

    # Spieler erstellen
    print("\n--- Spieler erstellen ---")

    # Kuja (Krieger-Magier)
    kuja = system.register_player("kuja")
    kuja.strength = 12
    kuja.agility = 10
    kuja.intelligence = 8
    kuja.mana = 150
    kuja.max_mana = 150

    # Najika (Explosion-Meisterin!)
    najika = system.register_player("najika", is_najika=True)
    najika.intelligence = 20
    najika.luck = 15
    najika.mana = 200
    najika.max_mana = 200

    # Skills lernen
    print("\n--- Skills lernen ---")
    print(system.learn_skill("kuja", "fireball"))
    print(system.learn_skill("kuja", "frost_spike"))
    print(system.learn_skill("kuja", "lightning_bolt"))

    print(system.learn_skill("najika", "explosion_basic"))
    print(system.learn_skill("najika", "explosion_advanced"))
    print(system.learn_skill("najika", "explosion_ultimate"))  # Nur Najika!

    # Ausruesten
    print("\n--- Ausruesten ---")
    print(system.equip_weapon("kuja", "flame_blade", HandSlot.RIGHT))
    print(system.equip_spell("kuja", "frost_spike", HandSlot.LEFT))

    print(system.equip_weapon("najika", "megumin_staff", HandSlot.LEFT))

    # Zauber wirken
    print("\n--- Zauber wirken ---")
    result = system.cast_spell("kuja", "fireball")
    print(f"Feuerball: {result.message}, XP: {result.xp_gained}")

    result = system.cast_spell("kuja", "lightning_bolt")
    print(f"Blitz: {result.message}")

    # Element-Weaving
    print("\n--- Element-Weaving ---")
    result = system.weave_elements("kuja", "fireball", "frost_spike")
    print(f"Weave: {result.message}, Bonus: {result.weave_bonus}")

    # Explosion KANN NICHT weaven!
    print("\n--- Explosion NICHT weaven ---")
    system.learn_skill("najika", "fireball")
    result = system.weave_elements("najika", "explosion_basic", "fireball")
    print(f"Explosion+Feuer: {result.message}")

    # Explosion Finisher
    print("\n--- Najika's OMEGA-DETONATION ---")
    result = system.cast_spell("najika", "explosion_ultimate")
    print(f"OMEGA: {result.message}, Schaden: {result.damage}")

    # Waffen-Angriff
    print("\n--- Waffen-Angriff ---")
    result = system.weapon_attack("kuja", HandSlot.RIGHT, AttackType.HEAVY)
    print(f"Schwert: {result.message}")

    # Status
    print("\n--- Status ---")
    status = system.get_player_status("najika")
    print(f"Najika - Mana: {status['resources']['mana']}/{status['resources']['max_mana']}")
    print(f"Skills: {status['learned_skills']}")

    print("\n" + "=" * 70)
    print("EXPLOSION!!! System funktioniert!")
    print("=" * 70)
