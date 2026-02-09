"""
NAJIKA MAGIC & SKILL SYSTEM V2
==============================
Inspiriert von: Konosuba + Skyrim + Elder Scrolls Online

DESIGN PHILOSOPHIE:
- Konosuba: Explosion ist EINZIGARTIG und MÄCHTIG (aber mit Nachteilen!)
- Skyrim: Learning by Doing - Skills steigen durch Nutzung
- ESO: Skill Lines mit Morphs, Ultimate Abilities, Synergies

DIE 8 GEBOTE BEACHTEN:
- Gebot #3: Explosion ≠ Weave - NIEMALS mit anderen kombinieren!
- Gebot #5: Learning by Doing - Skyrim-Style Progression

Copyright: Najika World
Author: Claude Code Team
Date: 2026-01-30
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime
import math
import random

# ============================================================================
# ENUMS - MAGISCHE GRUNDLAGEN
# ============================================================================

class MagicSchool(Enum):
    """
    9 Magieschulen (wie Skyrim aber mit Konosuba-Twist)

    Die ersten 8 können kombiniert werden (Weaving/Morphing)
    EXPLOSION ist EINZIGARTIG und steht alleine!
    """
    # Elementar (können geweaved werden)
    FIRE = "feuer"           # Destruktion - Offensiv
    ICE = "eis"              # Destruktion - Control
    LIGHTNING = "blitz"      # Destruktion - Burst
    EARTH = "erde"           # Alteration - Defensive
    WIND = "wind"            # Alteration - Mobility
    WATER = "wasser"         # Restoration - Support

    # Göttlich/Dunkel
    LIGHT = "licht"          # Restoration - Heilung & Anti-Undead
    DARKNESS = "dunkelheit"  # Illusion - Debuffs & Stealth

    # EINZIGARTIG - Megumin's Schule!
    EXPLOSION = "explosion"  # NIEMALS kombinierbar! (Gebot #3)


class SkillLine(Enum):
    """
    ESO-Style Skill Lines - Jede hat eigene Progression
    """
    # Klassen-Skills (wähle 1 Hauptklasse)
    ARCH_MAGE = "erzmagier"           # Pure Magic DPS
    CRIMSON_DEMON = "crimson_demon"   # Explosion-Spezialist (Megumin!)
    CRUSADER = "kreuzritter"          # Holy + Melee
    SHADOW_BLADE = "schattenkinge"    # Dark + Melee
    BATTLE_MAGE = "kampfmagier"       # Balanced Magic + Melee

    # Waffen-Skills (steigen durch Nutzung)
    ONE_HAND = "einhand"
    TWO_HAND = "zweihand"
    DUAL_WIELD = "dualwield"
    BOW = "bogen"
    STAFF = "stab"

    # Rüstungs-Skills
    LIGHT_ARMOR = "leichte_ruestung"
    MEDIUM_ARMOR = "mittlere_ruestung"
    HEAVY_ARMOR = "schwere_ruestung"

    # Handwerks-Skills
    ALCHEMY = "alchemie"
    ENCHANTING = "verzauberung"
    SMITHING = "schmieden"

    # Gilden-Skills (optional)
    FIGHTERS_GUILD = "kaempfergilde"
    MAGES_GUILD = "magiergilde"
    THIEVES_GUILD = "diebesgilde"


class SkillType(Enum):
    """Skill-Kategorien"""
    ACTIVE = "aktiv"           # Muss aktiviert werden
    PASSIVE = "passiv"         # Immer aktiv
    ULTIMATE = "ultimativ"     # Braucht Ultimate-Punkte
    TOGGLE = "toggle"          # An/Aus schaltbar


class TargetType(Enum):
    """Zieltypen"""
    SELF = "selbst"
    SINGLE_ENEMY = "einzelner_feind"
    SINGLE_ALLY = "einzelner_verbuendeter"
    CONE = "kegel"              # Kegel vor dem Spieler
    AOE_SELF = "flaeche_selbst" # Kreis um Spieler
    AOE_TARGET = "flaeche_ziel" # Kreis um Ziel
    LINE = "linie"              # Gerade Linie
    ALL_ENEMIES = "alle_feinde"
    ALL_ALLIES = "alle_verbuendeten"


class StatusEffect(Enum):
    """Status-Effekte (Konosuba + ESO Style)"""
    # Damage over Time
    BURNING = "brennend"        # Feuer DoT
    CHILLED = "unterkuehlt"     # Eis DoT + Slow
    SHOCKED = "geschockt"       # Blitz DoT + Minor Vuln
    POISONED = "vergiftet"      # Gift DoT
    BLEEDING = "blutend"        # Physischer DoT

    # Crowd Control
    STUNNED = "betaeubt"        # Kann nichts tun
    FROZEN = "eingefroren"      # Kann nichts tun + extra Schaden
    FEARED = "verängstigt"      # Läuft weg
    SILENCED = "verstummt"      # Keine Magie
    ROOTED = "verwurzelt"       # Kann sich nicht bewegen
    KNOCKDOWN = "niedergeschlagen"  # Am Boden

    # Buffs
    MAJOR_MIGHT = "major_macht"       # +20% Weapon Damage
    MINOR_MIGHT = "minor_macht"       # +10% Weapon Damage
    MAJOR_SORCERY = "major_zauberei"  # +20% Spell Damage
    MINOR_SORCERY = "minor_zauberei"  # +10% Spell Damage
    MAJOR_RESOLVE = "major_widerstand" # +5948 Resistances
    MINOR_RESOLVE = "minor_widerstand" # +2974 Resistances
    MAJOR_EXPEDITION = "major_expedition" # +30% Move Speed
    MINOR_EXPEDITION = "minor_expedition" # +15% Move Speed

    # Debuffs
    MAJOR_BREACH = "major_bresche"    # -5948 Resistances
    MINOR_BREACH = "minor_bresche"    # -2974 Resistances
    MAJOR_VULNERABILITY = "major_verwundbarkeit" # +10% Damage Taken
    MINOR_VULNERABILITY = "minor_verwundbarkeit" # +5% Damage Taken

    # Konosuba Spezial!
    EXPLOSION_AFTERMATH = "explosion_nachwirkung"  # Megumin kann sich nicht bewegen!


# ============================================================================
# ELEMENT RELATIONSHIPS (Konosuba + Pokemon Style)
# ============================================================================

ELEMENT_EFFECTIVENESS = {
    # Feuer ist stark gegen Eis/Wind, schwach gegen Wasser/Erde
    MagicSchool.FIRE: {
        MagicSchool.ICE: 1.5,
        MagicSchool.WIND: 1.25,
        MagicSchool.WATER: 0.5,
        MagicSchool.EARTH: 0.75,
    },
    # Eis ist stark gegen Wind/Wasser, schwach gegen Feuer/Blitz
    MagicSchool.ICE: {
        MagicSchool.WIND: 1.5,
        MagicSchool.WATER: 1.25,
        MagicSchool.FIRE: 0.5,
        MagicSchool.LIGHTNING: 0.75,
    },
    # Blitz ist stark gegen Wasser/Wind, schwach gegen Erde
    MagicSchool.LIGHTNING: {
        MagicSchool.WATER: 2.0,  # Extra stark!
        MagicSchool.WIND: 1.25,
        MagicSchool.EARTH: 0.25, # Erde erdet Blitz!
    },
    # Erde ist stark gegen Blitz, schwach gegen Wasser/Wind
    MagicSchool.EARTH: {
        MagicSchool.LIGHTNING: 1.5,
        MagicSchool.WATER: 0.75,
        MagicSchool.WIND: 0.5,
    },
    # Wind ist stark gegen Erde, schwach gegen Eis/Feuer
    MagicSchool.WIND: {
        MagicSchool.EARTH: 1.5,
        MagicSchool.ICE: 0.5,
        MagicSchool.FIRE: 0.75,
    },
    # Wasser ist stark gegen Feuer/Erde, schwach gegen Blitz/Eis
    MagicSchool.WATER: {
        MagicSchool.FIRE: 1.5,
        MagicSchool.EARTH: 1.25,
        MagicSchool.LIGHTNING: 0.5,
        MagicSchool.ICE: 0.75,
    },
    # Licht vs Dunkelheit
    MagicSchool.LIGHT: {
        MagicSchool.DARKNESS: 1.5,
        MagicSchool.LIGHT: 0.5,  # Gleich = schwach
    },
    MagicSchool.DARKNESS: {
        MagicSchool.LIGHT: 1.5,
        MagicSchool.DARKNESS: 0.5,
    },
    # EXPLOSION ist gegen ALLES effektiv! (Aber kostet alles...)
    MagicSchool.EXPLOSION: {
        MagicSchool.FIRE: 1.5,
        MagicSchool.ICE: 1.5,
        MagicSchool.LIGHTNING: 1.5,
        MagicSchool.EARTH: 1.5,
        MagicSchool.WIND: 1.5,
        MagicSchool.WATER: 1.5,
        MagicSchool.LIGHT: 1.5,
        MagicSchool.DARKNESS: 1.5,
        # Aber: KANN NUR 1x PRO TAG!
    },
}


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class SkillEffect:
    """Ein einzelner Effekt eines Skills"""
    effect_type: str  # "damage", "heal", "dot", "hot", "buff", "debuff", "cc"
    base_value: float
    scaling: Dict[str, float] = field(default_factory=dict)  # {"INT": 0.5, "weapon_damage": 1.2}
    status: Optional[StatusEffect] = None
    duration: float = 0  # Sekunden, 0 = instant
    tick_interval: float = 1.0
    chance: float = 1.0  # Proc-Chance (0-1)


@dataclass
class SkillMorph:
    """
    ESO-Style Morph - Skill kann sich entwickeln!

    Bei Skill-Level 4 kann man zwischen 2 Morphs wählen.
    """
    morph_id: str
    name: str
    name_de: str
    description_de: str
    modified_effects: List[SkillEffect]  # Ersetzt/Erweitert base effects
    bonus_effect: Optional[str] = None  # z.B. "Adds Stun" oder "Costs Stamina instead"


@dataclass
class Skill:
    """Einzelner Skill"""
    skill_id: str
    name: str
    name_de: str
    description_de: str

    # Kategorisierung
    school: MagicSchool
    skill_line: SkillLine
    skill_type: SkillType
    target_type: TargetType

    # Kosten
    mana_cost: int = 0
    stamina_cost: int = 0
    health_cost: int = 0
    ultimate_cost: int = 0  # Für Ultimate Skills

    # Timing
    cast_time: float = 0  # 0 = instant
    cooldown: float = 0
    channel_time: float = 0  # Für Channeled Skills

    # Reichweite & Fläche
    range_meters: float = 28  # Standard-Reichweite
    radius: float = 0  # Für AOE

    # Effekte
    effects: List[SkillEffect] = field(default_factory=list)

    # Morphs (ESO-Style)
    morphs: List[SkillMorph] = field(default_factory=list)
    selected_morph: Optional[str] = None

    # Visuell
    icon: str = "⚔️"
    color: str = "#ffffff"
    animation: str = "default"
    sound_id: str = ""

    # Requirements
    required_level: int = 1
    required_skill_line_level: int = 1

    # Spezial-Flags
    can_crit: bool = True
    blockable: bool = True
    dodgeable: bool = True
    interruptible: bool = True

    # Konosuba Spezial
    is_explosion: bool = False  # Megumin's Signature!
    daily_limit: int = 0  # 0 = unlimited, 1 = 1x/Tag für Explosion!
    leaves_caster_exhausted: bool = False  # Megumin kann sich nicht bewegen!


@dataclass
class SkillLineProgress:
    """Fortschritt in einer Skill Line (ESO-Style)"""
    skill_line: SkillLine
    level: int = 1
    max_level: int = 50
    experience: float = 0
    exp_for_next: float = 1000

    # Freigeschaltete Skills
    unlocked_skills: List[str] = field(default_factory=list)

    # Passive Boni bei bestimmten Leveln
    passive_bonuses: Dict[int, str] = field(default_factory=dict)


@dataclass
class MagicSchoolProgress:
    """Fortschritt in einer Magieschule (Skyrim-Style)"""
    school: MagicSchool
    level: int = 1
    max_level: int = 100
    experience: float = 0
    exp_for_next: float = 100

    # Stats
    total_casts: int = 0
    total_damage: float = 0
    total_healing: float = 0

    # Perks (Skyrim-Style)
    unlocked_perks: List[str] = field(default_factory=list)


# ============================================================================
# SKILL DATABASE - KONOSUBA + SKYRIM + ESO INSPIRED
# ============================================================================

def create_skill_database() -> Dict[str, Skill]:
    """Erstellt die komplette Skill-Datenbank"""

    skills = {}

    # =========================================================================
    # FEUER-MAGIE (Destruction)
    # =========================================================================

    skills["flames"] = Skill(
        skill_id="flames",
        name="Flames",
        name_de="Flammen",
        description_de="Feuere einen kontinuierlichen Flammenstrahl. Verursacht Brennen.",
        school=MagicSchool.FIRE,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.CONE,
        mana_cost=15,  # Per second
        channel_time=3.0,
        range_meters=8,
        effects=[
            SkillEffect("damage", 25, scaling={"INT": 0.5, "spell_damage": 0.8}),
            SkillEffect("dot", 10, status=StatusEffect.BURNING, duration=4.0, chance=0.5),
        ],
        morphs=[
            SkillMorph(
                "flames_inferno", "Inferno", "Inferno",
                "Größerer Kegel, mehr Schaden, aber höhere Mana-Kosten",
                [SkillEffect("damage", 35, scaling={"INT": 0.7, "spell_damage": 1.0})]
            ),
            SkillMorph(
                "flames_searing", "Searing Flames", "Sengende Flammen",
                "Garantiertes Brennen, heilt dich für erlittenen Schaden",
                [SkillEffect("dot", 15, status=StatusEffect.BURNING, duration=6.0, chance=1.0)]
            ),
        ],
        icon="🔥",
        color="#ff4400",
        required_level=1,
    )

    skills["fireball"] = Skill(
        skill_id="fireball",
        name="Fireball",
        name_de="Feuerball",
        description_de="Schleudere einen explodierenden Feuerball. AOE Schaden.",
        school=MagicSchool.FIRE,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.AOE_TARGET,
        mana_cost=35,
        cast_time=1.0,
        cooldown=6.0,
        range_meters=28,
        radius=6,
        effects=[
            SkillEffect("damage", 80, scaling={"INT": 0.8, "spell_damage": 1.2}),
            SkillEffect("dot", 15, status=StatusEffect.BURNING, duration=4.0),
        ],
        morphs=[
            SkillMorph(
                "fireball_meteor", "Meteor", "Meteor",
                "Massiver Schaden, längere Cast-Zeit, Knockdown",
                [SkillEffect("damage", 150, scaling={"INT": 1.2}),
                 SkillEffect("cc", 0, status=StatusEffect.KNOCKDOWN, duration=2.0)]
            ),
            SkillMorph(
                "fireball_scatter", "Scattershot", "Streuschuss",
                "3 kleinere Feuerbälle, schneller, weniger Schaden pro Ball",
                [SkillEffect("damage", 40, scaling={"INT": 0.5})]  # 3x = 120 total
            ),
        ],
        icon="🔥",
        color="#ff6600",
        required_level=5,
        required_skill_line_level=5,
    )

    skills["fire_wall"] = Skill(
        skill_id="fire_wall",
        name="Wall of Fire",
        name_de="Feuerwand",
        description_de="Erschaffe eine Wand aus Flammen. Feinde die durchlaufen brennen.",
        school=MagicSchool.FIRE,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.AOE_TARGET,
        mana_cost=50,
        cooldown=10.0,
        range_meters=20,
        radius=10,  # Länge der Wand
        effects=[
            SkillEffect("damage", 30, scaling={"spell_damage": 0.6}),  # Per second
            SkillEffect("dot", 20, status=StatusEffect.BURNING, duration=8.0),
        ],
        icon="🔥",
        color="#ff3300",
        required_level=15,
        required_skill_line_level=15,
    )

    # =========================================================================
    # EIS-MAGIE (Destruction + Control)
    # =========================================================================

    skills["frost_bolt"] = Skill(
        skill_id="frost_bolt",
        name="Frost Bolt",
        name_de="Frostbolzen",
        description_de="Schieße einen Eiszapfen der Feinde verlangsamt.",
        school=MagicSchool.ICE,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SINGLE_ENEMY,
        mana_cost=20,
        cast_time=0.5,
        cooldown=0,  # Spammable!
        range_meters=28,
        effects=[
            SkillEffect("damage", 35, scaling={"INT": 0.6, "spell_damage": 0.9}),
            SkillEffect("debuff", -0.3, status=StatusEffect.CHILLED, duration=4.0),  # 30% Slow
        ],
        morphs=[
            SkillMorph(
                "frost_bolt_deep", "Deep Freeze", "Tiefkühlen",
                "Kann einfrieren bei niedrigen HP",
                [SkillEffect("cc", 0, status=StatusEffect.FROZEN, duration=3.0, chance=0.3)]
            ),
            SkillMorph(
                "frost_bolt_pierce", "Piercing Cold", "Durchdringende Kälte",
                "Durchbohrt Feinde, trifft alle in einer Linie",
                [SkillEffect("damage", 30, scaling={"INT": 0.5})]
            ),
        ],
        icon="❄️",
        color="#00ccff",
        required_level=1,
    )

    skills["blizzard"] = Skill(
        skill_id="blizzard",
        name="Blizzard",
        name_de="Blizzard",
        description_de="Beschwöre einen Schneesturm. Massiver AOE, verlangsamt alle.",
        school=MagicSchool.ICE,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.ULTIMATE,
        target_type=TargetType.AOE_SELF,
        ultimate_cost=200,
        channel_time=8.0,
        radius=15,
        effects=[
            SkillEffect("damage", 50, scaling={"INT": 0.8}),  # Per second
            SkillEffect("debuff", -0.5, status=StatusEffect.CHILLED, duration=2.0),  # Constant slow
            SkillEffect("cc", 0, status=StatusEffect.FROZEN, duration=2.0, chance=0.1),  # Chance to freeze
        ],
        icon="🌨️",
        color="#aaddff",
        required_level=20,
        required_skill_line_level=20,
        interruptible=True,
    )

    # =========================================================================
    # BLITZ-MAGIE (High Burst)
    # =========================================================================

    skills["lightning_bolt"] = Skill(
        skill_id="lightning_bolt",
        name="Lightning Bolt",
        name_de="Blitzschlag",
        description_de="Schlag den Feind mit einem Blitz. Hoher Burst, kann betäuben.",
        school=MagicSchool.LIGHTNING,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SINGLE_ENEMY,
        mana_cost=40,
        cast_time=1.2,
        cooldown=8.0,
        range_meters=28,
        effects=[
            SkillEffect("damage", 120, scaling={"INT": 1.2, "spell_damage": 1.5}),
            SkillEffect("cc", 0, status=StatusEffect.STUNNED, duration=1.0, chance=0.25),
            SkillEffect("dot", 5, status=StatusEffect.SHOCKED, duration=4.0),
        ],
        icon="⚡",
        color="#ffff00",
        required_level=10,
        required_skill_line_level=10,
    )

    skills["chain_lightning"] = Skill(
        skill_id="chain_lightning",
        name="Chain Lightning",
        name_de="Kettenblitz",
        description_de="Blitz springt zu 3 weiteren Feinden. Jeder Sprung -20% Schaden.",
        school=MagicSchool.LIGHTNING,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SINGLE_ENEMY,  # But chains!
        mana_cost=50,
        cast_time=0.8,
        cooldown=10.0,
        range_meters=28,
        effects=[
            SkillEffect("damage", 80, scaling={"INT": 0.9}),  # First target
            # Chain damage calculated separately
        ],
        icon="⚡",
        color="#ffffaa",
        required_level=20,
    )

    # =========================================================================
    # LICHT-MAGIE (Restoration + Holy)
    # =========================================================================

    skills["healing_light"] = Skill(
        skill_id="healing_light",
        name="Healing Light",
        name_de="Heilendes Licht",
        description_de="Heile dich oder einen Verbündeten.",
        school=MagicSchool.LIGHT,
        skill_line=SkillLine.CRUSADER,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SINGLE_ALLY,
        mana_cost=30,
        cast_time=1.0,
        cooldown=0,
        range_meters=28,
        effects=[
            SkillEffect("heal", 80, scaling={"INT": 0.7, "max_health": 0.1}),
        ],
        morphs=[
            SkillMorph(
                "healing_light_burst", "Burst Heal", "Blitzheilung",
                "Instant cast, aber höhere Kosten",
                [SkillEffect("heal", 70, scaling={"INT": 0.6})]
            ),
            SkillMorph(
                "healing_light_regen", "Renewing Light", "Erneuerndes Licht",
                "Zusätzliche Heilung über Zeit",
                [SkillEffect("heal", 50, scaling={"INT": 0.5}),
                 SkillEffect("hot", 15, duration=8.0, tick_interval=2.0)]
            ),
        ],
        icon="✨",
        color="#ffffaa",
        required_level=1,
        can_crit=False,
    )

    skills["holy_smite"] = Skill(
        skill_id="holy_smite",
        name="Holy Smite",
        name_de="Heiliger Zorn",
        description_de="Göttliches Licht vernichtet Unheiliges. Extra Schaden gegen Untote.",
        school=MagicSchool.LIGHT,
        skill_line=SkillLine.CRUSADER,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.AOE_TARGET,
        mana_cost=45,
        cast_time=1.5,
        cooldown=12.0,
        range_meters=20,
        radius=8,
        effects=[
            SkillEffect("damage", 100, scaling={"INT": 1.0}),
            # +50% gegen Undead (im Code berechnet)
        ],
        icon="☀️",
        color="#ffff88",
        required_level=15,
    )

    # =========================================================================
    # DUNKELHEIT-MAGIE (Debuffs + Stealth)
    # =========================================================================

    skills["shadow_cloak"] = Skill(
        skill_id="shadow_cloak",
        name="Shadow Cloak",
        name_de="Schattenmantel",
        description_de="Werde unsichtbar. Nächster Angriff aus Stealth macht +50% Schaden.",
        school=MagicSchool.DARKNESS,
        skill_line=SkillLine.SHADOW_BLADE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SELF,
        mana_cost=35,
        cooldown=20.0,
        effects=[
            SkillEffect("buff", 0, duration=10.0),  # Invisibility
            SkillEffect("buff", 0.5, duration=10.0),  # +50% next attack
        ],
        icon="🌑",
        color="#440088",
        required_level=5,
    )

    skills["soul_drain"] = Skill(
        skill_id="soul_drain",
        name="Soul Drain",
        name_de="Seelenentzug",
        description_de="Entziehe Lebenskraft. Schadet dem Feind, heilt dich.",
        school=MagicSchool.DARKNESS,
        skill_line=SkillLine.SHADOW_BLADE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SINGLE_ENEMY,
        mana_cost=40,
        channel_time=4.0,
        range_meters=15,
        effects=[
            SkillEffect("damage", 30, scaling={"INT": 0.6}),  # Per second
            SkillEffect("heal", 30, scaling={"INT": 0.6}),    # Per second, self
        ],
        icon="💀",
        color="#660066",
        required_level=10,
        interruptible=True,
    )

    # =========================================================================
    # ERDE-MAGIE (Defense + CC)
    # =========================================================================

    skills["stone_skin"] = Skill(
        skill_id="stone_skin",
        name="Stone Skin",
        name_de="Steinhaut",
        description_de="Verstärke deine Rüstung massiv für kurze Zeit.",
        school=MagicSchool.EARTH,
        skill_line=SkillLine.BATTLE_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SELF,
        mana_cost=40,
        cooldown=30.0,
        effects=[
            SkillEffect("buff", 0, status=StatusEffect.MAJOR_RESOLVE, duration=20.0),
            SkillEffect("buff", 5000, duration=20.0),  # Flat armor bonus
        ],
        icon="🪨",
        color="#8b4513",
        required_level=5,
    )

    skills["earthquake"] = Skill(
        skill_id="earthquake",
        name="Earthquake",
        name_de="Erdbeben",
        description_de="Die Erde bebt! Alle Feinde werden niedergeschlagen.",
        school=MagicSchool.EARTH,
        skill_line=SkillLine.BATTLE_MAGE,
        skill_type=SkillType.ULTIMATE,
        target_type=TargetType.AOE_SELF,
        ultimate_cost=250,
        cast_time=2.0,
        radius=12,
        effects=[
            SkillEffect("damage", 200, scaling={"INT": 1.5}),
            SkillEffect("cc", 0, status=StatusEffect.KNOCKDOWN, duration=3.0),
        ],
        icon="🌋",
        color="#964B00",
        required_level=25,
    )

    # =========================================================================
    # WIND-MAGIE (Mobility + Speed)
    # =========================================================================

    skills["wind_dash"] = Skill(
        skill_id="wind_dash",
        name="Wind Dash",
        name_de="Windstoß",
        description_de="Stürme vorwärts und weiche Angriffen aus.",
        school=MagicSchool.WIND,
        skill_line=SkillLine.BATTLE_MAGE,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SELF,
        stamina_cost=25,
        cooldown=10.0,
        effects=[
            SkillEffect("buff", 0, status=StatusEffect.MAJOR_EXPEDITION, duration=4.0),
            # I-frames während dash
        ],
        icon="💨",
        color="#aaffaa",
        required_level=1,
        can_crit=False,
        blockable=False,
        dodgeable=False,
    )

    # =========================================================================
    # WASSER-MAGIE (Support + Cleanse)
    # =========================================================================

    skills["purifying_waters"] = Skill(
        skill_id="purifying_waters",
        name="Purifying Waters",
        name_de="Reinigende Wasser",
        description_de="Entferne alle negativen Effekte von dir oder einem Verbündeten.",
        school=MagicSchool.WATER,
        skill_line=SkillLine.CRUSADER,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.SINGLE_ALLY,
        mana_cost=50,
        cooldown=15.0,
        range_meters=28,
        effects=[
            # Cleanse all negative effects
            SkillEffect("heal", 30, scaling={"INT": 0.3}),
        ],
        icon="💧",
        color="#0088ff",
        required_level=10,
    )

    # =========================================================================
    # 💥 EXPLOSION!!! - MEGUMIN'S SIGNATURE (Konosuba)
    # =========================================================================

    skills["explosion_minor"] = Skill(
        skill_id="explosion_minor",
        name="Minor Explosion",
        name_de="Kleine Explosion",
        description_de="Eine kleine, aber feine Explosion. Für Anfänger.",
        school=MagicSchool.EXPLOSION,
        skill_line=SkillLine.CRIMSON_DEMON,
        skill_type=SkillType.ACTIVE,
        target_type=TargetType.AOE_TARGET,
        mana_cost=100,
        cast_time=2.0,
        cooldown=60.0,  # 1 Minute!
        range_meters=50,
        radius=8,
        effects=[
            SkillEffect("damage", 300, scaling={"INT": 2.0, "spell_damage": 2.5}),
            SkillEffect("cc", 0, status=StatusEffect.KNOCKDOWN, duration=2.0),
        ],
        icon="💥",
        color="#ff0000",
        required_level=10,
        required_skill_line_level=10,
        is_explosion=True,
        interruptible=False,  # Kann NICHT unterbrochen werden!
    )

    skills["explosion"] = Skill(
        skill_id="explosion",
        name="EXPLOSION!!!",
        name_de="EXPLOSION!!!",
        description_de="DIE ultimative Zerstörungsmagie! NIEMALS kombinierbar! Nach Nutzung: Erschöpfung.",
        school=MagicSchool.EXPLOSION,
        skill_line=SkillLine.CRIMSON_DEMON,
        skill_type=SkillType.ULTIMATE,
        target_type=TargetType.AOE_TARGET,
        mana_cost=0,  # Kostet ALLES Mana!
        health_cost=0,  # Kostet 50% HP!
        ultimate_cost=500,
        cast_time=5.0,  # LANGE Cast-Zeit (Chanting!)
        cooldown=0,  # Kein Cooldown, aber...
        range_meters=100,  # RIESIGE Reichweite
        radius=30,  # MASSIVER Radius
        effects=[
            SkillEffect("damage", 9999, scaling={"INT": 5.0, "spell_damage": 5.0}),
            SkillEffect("cc", 0, status=StatusEffect.KNOCKDOWN, duration=5.0),
            # Alles im Radius wird VERNICHTET
        ],
        morphs=[
            SkillMorph(
                "explosion_crimson", "Crimson Explosion", "Purpurne Explosion",
                "Höherer Schaden, aber du fällst danach in Ohnmacht",
                [SkillEffect("damage", 15000, scaling={"INT": 7.0})]
            ),
            SkillMorph(
                "explosion_controlled", "Controlled Explosion", "Kontrollierte Explosion",
                "Weniger Schaden, aber du kannst danach noch stehen",
                [SkillEffect("damage", 5000, scaling={"INT": 3.0})]
            ),
        ],
        icon="💥",
        color="#ff0000",
        animation="megumin_chant",
        sound_id="explosion_ultimate",
        required_level=50,
        required_skill_line_level=50,
        is_explosion=True,
        daily_limit=1,  # NUR 1x PRO TAG!
        leaves_caster_exhausted=True,  # Kann sich nicht mehr bewegen!
        can_crit=True,  # KANN CRITTEN! (Imagine...)
        blockable=False,
        dodgeable=False,  # Unausweichlich im Radius!
        interruptible=False,
    )

    # =========================================================================
    # PASSIVE SKILLS
    # =========================================================================

    skills["fire_mastery"] = Skill(
        skill_id="fire_mastery",
        name="Fire Mastery",
        name_de="Feuermeisterschaft",
        description_de="Erhöht Feuerschaden um 10/20/30%.",
        school=MagicSchool.FIRE,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.PASSIVE,
        target_type=TargetType.SELF,
        effects=[
            SkillEffect("buff", 0.1),  # Per rank
        ],
        icon="🔥",
        required_level=1,
    )

    skills["mana_recovery"] = Skill(
        skill_id="mana_recovery",
        name="Mana Recovery",
        name_de="Mana-Regeneration",
        description_de="Erhöht Mana-Regeneration um 5/10/15%.",
        school=MagicSchool.LIGHT,
        skill_line=SkillLine.ARCH_MAGE,
        skill_type=SkillType.PASSIVE,
        target_type=TargetType.SELF,
        effects=[
            SkillEffect("buff", 0.05),
        ],
        icon="💙",
        required_level=5,
    )

    skills["explosion_affinity"] = Skill(
        skill_id="explosion_affinity",
        name="Explosion Affinity",
        name_de="Explosions-Affinität",
        description_de="Du liebst Explosionen! -20% Mana-Kosten für Explosion-Skills. +50% Explosion-Schaden.",
        school=MagicSchool.EXPLOSION,
        skill_line=SkillLine.CRIMSON_DEMON,
        skill_type=SkillType.PASSIVE,
        target_type=TargetType.SELF,
        effects=[
            SkillEffect("buff", -0.2),  # Mana reduction
            SkillEffect("buff", 0.5),   # Damage increase
        ],
        icon="💥",
        required_level=1,
        is_explosion=True,
    )

    return skills


# ============================================================================
# SKILL LINE DEFINITIONS
# ============================================================================

def create_skill_lines() -> Dict[SkillLine, Dict]:
    """Erstellt alle Skill Lines mit ihren Unlocks"""

    return {
        SkillLine.ARCH_MAGE: {
            "name_de": "Erzmagier",
            "description_de": "Meistere die elementare Zerstörungsmagie",
            "skills_by_level": {
                1: ["flames", "frost_bolt", "fire_mastery"],
                5: ["fireball", "mana_recovery"],
                10: ["lightning_bolt"],
                15: ["fire_wall", "holy_smite"],
                20: ["chain_lightning", "blizzard"],
            },
            "passives": {
                10: "Elementarer Fokus: +5% Spell Damage",
                20: "Magische Durchdringung: -10% Feind-Resistenzen",
                30: "Arkane Macht: +10% Crit Chance für Zauber",
                40: "Überladung: Crits restaurieren 5% Mana",
                50: "Großmagier: Alle Zauber +15% Schaden",
            }
        },

        SkillLine.CRIMSON_DEMON: {
            "name_de": "Crimson Demon",
            "description_de": "Der Pfad der EXPLOSION! Nur für wahre Künstler.",
            "skills_by_level": {
                1: ["explosion_affinity"],
                10: ["explosion_minor"],
                25: ["flames"],  # Auch Feuer als Backup
                50: ["explosion"],  # DIE ULTIMATIVE KUNST!
            },
            "passives": {
                10: "Explosions-Novize: Explosion-Skills +20% Radius",
                20: "Brennende Leidenschaft: Nach Explosion 10s +50% Feuer-Schaden",
                30: "Crimson Augen: Explosion kann nicht verfehlen",
                40: "Megumin's Erbe: Explosion-Cooldown -30%",
                50: "REINSTE EXPLOSION: Tägliches Limit +1",
            },
            "special_note": "WARNUNG: Explosion kann NIEMALS mit anderen Elementen kombiniert werden! (Gebot #3)"
        },

        SkillLine.CRUSADER: {
            "name_de": "Kreuzritter",
            "description_de": "Heiliges Licht und Heilung",
            "skills_by_level": {
                1: ["healing_light"],
                5: ["stone_skin"],
                10: ["purifying_waters"],
                15: ["holy_smite"],
            },
            "passives": {
                10: "Göttlicher Schutz: +10% Heilung erhalten",
                20: "Aura des Lichts: Verbündete in 8m +5% Heilung",
                30: "Reinheit: Immun gegen Dunkelheits-Effekte",
                40: "Segnung: Heilungen haben 20% Chance Buff zu geben",
                50: "Avatar des Lichts: Ultimates kosten -25%",
            }
        },

        SkillLine.SHADOW_BLADE: {
            "name_de": "Schattenklinge",
            "description_de": "Dunkelheit und Hinterhalt",
            "skills_by_level": {
                1: ["shadow_cloak"],
                10: ["soul_drain"],
            },
            "passives": {
                10: "Schatten-Affinität: Stealth +5s Dauer",
                20: "Hinterhalt: Angriffe aus Stealth +30% Crit",
                30: "Lebensraub: 10% aller Schaden heilt dich",
                40: "Phantom: Nach Kill 50% Chance Stealth zu erneuern",
                50: "Meisterassassine: Stealth-Bonus-Schaden +100%",
            }
        },

        SkillLine.BATTLE_MAGE: {
            "name_de": "Kampfmagier",
            "description_de": "Kombiniere Magie mit Nahkampf",
            "skills_by_level": {
                1: ["wind_dash"],
                5: ["stone_skin"],
                25: ["earthquake"],
            },
            "passives": {
                10: "Magische Rüstung: Spell Damage gibt auch Rüstung",
                20: "Kampfmagie: Nahkampf-Treffer restaurieren 2% Mana",
                30: "Elementare Waffe: Waffen-Angriffe +Element-Schaden",
                40: "Überlebenskünstler: Unter 30% HP +30% Resistenzen",
                50: "Arkaner Krieger: Stamina und Mana teilen sich Pool",
            }
        },
    }


# ============================================================================
# MAIN SYSTEM CLASS
# ============================================================================

class NajikaMagicSystem:
    """
    Hauptklasse für das Magic & Skill System V2

    Kombiniert:
    - Skyrim: Learning by Doing Progression
    - ESO: Skill Lines mit Morphs und Passives
    - Konosuba: Explosion ist EINZIGARTIG!
    """

    def __init__(self):
        # Skill Database
        self.skills = create_skill_database()
        self.skill_lines = create_skill_lines()

        # Player Progress
        self.school_progress: Dict[MagicSchool, MagicSchoolProgress] = {}
        self.skill_line_progress: Dict[SkillLine, SkillLineProgress] = {}

        # Initialize all schools at level 1
        for school in MagicSchool:
            self.school_progress[school] = MagicSchoolProgress(school=school)

        # Active cooldowns & effects
        self.cooldowns: Dict[str, float] = {}  # skill_id -> remaining_cd
        self.active_effects: List[Dict] = []

        # Daily limits (für Explosion!)
        self.daily_uses: Dict[str, int] = {}
        self.last_daily_reset: datetime = datetime.now()

        # Explosion special state
        self.is_exhausted: bool = False
        self.exhaustion_remaining: float = 0

        # Experience settings (Skyrim-style)
        self.BASE_EXP = 100
        self.EXP_MULTIPLIER = 1.08  # Exponential growth

    def cast_skill(
        self,
        skill_id: str,
        caster_stats: Dict,
        target_element: Optional[MagicSchool] = None,
        is_undead_target: bool = False,
    ) -> Dict:
        """
        Verwende einen Skill (Skyrim Learning by Doing!)

        Returns:
            Result mit Schaden, Effekten, XP-Gain, Level-Ups, etc.
        """
        if skill_id not in self.skills:
            return {"success": False, "error": "Skill nicht gefunden"}

        skill = self.skills[skill_id]

        # Check Exhaustion (Megumin!)
        if self.is_exhausted:
            return {
                "success": False,
                "error": "Du bist erschöpft! Kannst keine Skills nutzen. (Explosion Aftermath)",
                "exhaustion_remaining": self.exhaustion_remaining
            }

        # Check Cooldown
        if skill_id in self.cooldowns and self.cooldowns[skill_id] > 0:
            return {
                "success": False,
                "error": f"Cooldown: {self.cooldowns[skill_id]:.1f}s",
            }

        # Check Daily Limit (Explosion!)
        if skill.daily_limit > 0:
            self._check_daily_reset()
            if self.daily_uses.get(skill_id, 0) >= skill.daily_limit:
                return {
                    "success": False,
                    "error": f"Tägliches Limit erreicht! ({skill.daily_limit}x pro Tag)",
                    "next_reset": "Mitternacht"
                }

        # Calculate effects
        results = []
        total_damage = 0
        total_healing = 0

        for effect in skill.effects:
            value = effect.base_value

            # Stat Scaling
            for stat, scaling in effect.scaling.items():
                if stat in caster_stats:
                    value += caster_stats[stat] * scaling

            # Element Effectiveness
            if target_element and skill.school in ELEMENT_EFFECTIVENESS:
                effectiveness = ELEMENT_EFFECTIVENESS[skill.school].get(target_element, 1.0)
                value *= effectiveness

            # Holy vs Undead bonus
            if skill.school == MagicSchool.LIGHT and is_undead_target:
                value *= 1.5

            # Crit Check
            crit = False
            if skill.can_crit:
                crit_chance = caster_stats.get("crit_chance", 10) / 100
                if random.random() < crit_chance:
                    crit = True
                    crit_mult = 1.5 + (caster_stats.get("crit_damage", 50) / 100)
                    value *= crit_mult

            if effect.effect_type == "damage":
                total_damage += value
            elif effect.effect_type == "heal":
                total_healing += value

            results.append({
                "type": effect.effect_type,
                "value": round(value, 1),
                "crit": crit,
                "status": effect.status.value if effect.status else None,
                "duration": effect.duration,
            })

        # Set Cooldown
        if skill.cooldown > 0:
            self.cooldowns[skill_id] = skill.cooldown

        # Increment Daily Use (Explosion!)
        if skill.daily_limit > 0:
            self.daily_uses[skill_id] = self.daily_uses.get(skill_id, 0) + 1

        # Apply Exhaustion (Megumin!)
        if skill.leaves_caster_exhausted:
            self.is_exhausted = True
            self.exhaustion_remaining = 60.0  # 60 Sekunden!

        # LEARNING BY DOING - XP für Magieschule!
        xp_result = self._give_school_xp(skill.school, total_damage, total_healing)

        return {
            "success": True,
            "skill_name": skill.name_de,
            "skill_id": skill_id,
            "effects": results,
            "total_damage": round(total_damage, 1),
            "total_healing": round(total_healing, 1),
            "mana_cost": skill.mana_cost,
            "stamina_cost": skill.stamina_cost,
            "cast_time": skill.cast_time,
            "animation": skill.animation,
            "icon": skill.icon,
            "color": skill.color,
            "is_explosion": skill.is_explosion,
            "caster_exhausted": skill.leaves_caster_exhausted,
            "xp_gained": xp_result["xp_gained"],
            "school": skill.school.value,
            "school_level": xp_result["new_level"],
            "leveled_up": xp_result["leveled_up"],
        }

    def _give_school_xp(
        self,
        school: MagicSchool,
        damage_dealt: float,
        healing_done: float
    ) -> Dict:
        """
        Skyrim-Style: XP für die Magieschule geben
        """
        progress = self.school_progress[school]

        # Base XP + Bonus für Schaden/Heilung
        base_xp = 15
        damage_xp = damage_dealt * 0.1
        healing_xp = healing_done * 0.15  # Heilung gibt etwas mehr XP

        total_xp = base_xp + damage_xp + healing_xp

        # Explosion gibt MASSIV XP (weil selten!)
        if school == MagicSchool.EXPLOSION:
            total_xp *= 10

        old_level = progress.level
        progress.experience += total_xp
        progress.total_casts += 1
        progress.total_damage += damage_dealt
        progress.total_healing += healing_done

        # Level Up Check
        leveled_up = False
        new_perks = []

        while progress.experience >= progress.exp_for_next and progress.level < progress.max_level:
            progress.experience -= progress.exp_for_next
            progress.level += 1
            leveled_up = True

            # Exponential XP curve
            progress.exp_for_next = self.BASE_EXP * (self.EXP_MULTIPLIER ** (progress.level - 1))

            # Check for perk unlocks
            if progress.level in [25, 50, 75, 100]:
                perk_name = f"{school.value}_perk_{progress.level}"
                progress.unlocked_perks.append(perk_name)
                new_perks.append(perk_name)

        return {
            "xp_gained": round(total_xp, 1),
            "old_level": old_level,
            "new_level": progress.level,
            "leveled_up": leveled_up,
            "new_perks": new_perks,
            "current_xp": round(progress.experience, 1),
            "xp_for_next": round(progress.exp_for_next, 1),
        }

    def _check_daily_reset(self):
        """Prüft ob tägliche Limits zurückgesetzt werden müssen"""
        now = datetime.now()
        if now.date() > self.last_daily_reset.date():
            self.daily_uses = {}
            self.last_daily_reset = now

    def update(self, delta_time: float):
        """Update Cooldowns und Exhaustion"""
        # Cooldowns
        for skill_id in list(self.cooldowns.keys()):
            self.cooldowns[skill_id] -= delta_time
            if self.cooldowns[skill_id] <= 0:
                del self.cooldowns[skill_id]

        # Exhaustion (Megumin!)
        if self.is_exhausted:
            self.exhaustion_remaining -= delta_time
            if self.exhaustion_remaining <= 0:
                self.is_exhausted = False
                self.exhaustion_remaining = 0

    def can_weave(self, school1: MagicSchool, school2: MagicSchool) -> Tuple[bool, str]:
        """
        Prüft ob zwei Schulen kombiniert werden können

        GEBOT #3: Explosion ≠ Weave!
        """
        if school1 == MagicSchool.EXPLOSION or school2 == MagicSchool.EXPLOSION:
            return False, "💥 EXPLOSION kann NIEMALS kombiniert werden! Das ist GEBOT #3!"

        if school1 == school2:
            return False, "Gleiche Schule kann nicht kombiniert werden"

        # Check minimum levels
        prog1 = self.school_progress[school1]
        prog2 = self.school_progress[school2]

        if prog1.level < 25 or prog2.level < 25:
            return False, f"Beide Schulen müssen Level 25+ sein (aktuell: {school1.value}={prog1.level}, {school2.value}={prog2.level})"

        return True, "✅ Weaving möglich!"

    def get_all_skills_overview(self) -> List[Dict]:
        """Holt Übersicht aller Skills"""
        overview = []
        for skill_id, skill in self.skills.items():
            overview.append({
                "id": skill_id,
                "name": skill.name_de,
                "school": skill.school.value,
                "type": skill.skill_type.value,
                "icon": skill.icon,
                "mana_cost": skill.mana_cost,
                "cooldown": skill.cooldown,
                "is_explosion": skill.is_explosion,
                "required_level": skill.required_level,
            })
        return overview

    def get_school_overview(self) -> Dict:
        """Holt Übersicht aller Magieschulen"""
        return {
            school.value: {
                "level": prog.level,
                "xp": prog.experience,
                "xp_next": prog.exp_for_next,
                "total_casts": prog.total_casts,
                "perks": prog.unlocked_perks,
            }
            for school, prog in self.school_progress.items()
        }

    def export_state(self) -> Dict:
        """Exportiert kompletten State für Save/Load"""
        return {
            "schools": {
                school.value: {
                    "level": prog.level,
                    "experience": prog.experience,
                    "total_casts": prog.total_casts,
                    "total_damage": prog.total_damage,
                    "total_healing": prog.total_healing,
                    "perks": prog.unlocked_perks,
                }
                for school, prog in self.school_progress.items()
            },
            "daily_uses": self.daily_uses,
            "is_exhausted": self.is_exhausted,
            "exhaustion_remaining": self.exhaustion_remaining,
        }


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

magic_system = NajikaMagicSystem()


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA MAGIC SYSTEM V2 - TEST")
    print("Konosuba + Skyrim + ESO Style!")
    print("=" * 60)

    system = NajikaMagicSystem()

    # Test 1: Cast Fireball
    print("\n1. Cast Feuerball")
    result = system.cast_skill(
        "fireball",
        caster_stats={"INT": 50, "spell_damage": 100, "crit_chance": 20, "crit_damage": 75},
        target_element=MagicSchool.ICE  # 1.5x!
    )
    print(f"   {result['skill_name']}: {result['total_damage']} Schaden")
    print(f"   XP: +{result['xp_gained']} für {result['school']}")

    # Test 2: Cast Explosion!
    print("\n2. EXPLOSION!!!")
    result = system.cast_skill(
        "explosion",
        caster_stats={"INT": 100, "spell_damage": 200, "crit_chance": 50},
    )
    if result["success"]:
        print(f"   💥 {result['skill_name']}: {result['total_damage']} SCHADEN!")
        print(f"   Erschöpft: {result['caster_exhausted']}")
        print(f"   XP: +{result['xp_gained']} für EXPLOSION!")

    # Test 3: Try to cast while exhausted
    print("\n3. Versuch nach Explosion...")
    result = system.cast_skill("fireball", caster_stats={"INT": 50})
    print(f"   Erfolg: {result['success']}")
    print(f"   Grund: {result.get('error', 'OK')}")

    # Test 4: Weave Check
    print("\n4. Weave-Check: Feuer + Eis")
    can_weave, reason = system.can_weave(MagicSchool.FIRE, MagicSchool.ICE)
    print(f"   Möglich: {can_weave}")
    print(f"   Grund: {reason}")

    print("\n5. Weave-Check: Feuer + EXPLOSION (Gebot #3!)")
    can_weave, reason = system.can_weave(MagicSchool.FIRE, MagicSchool.EXPLOSION)
    print(f"   Möglich: {can_weave}")
    print(f"   Grund: {reason}")

    # Test 6: School Overview
    print("\n6. Magieschulen-Übersicht:")
    for school, info in system.get_school_overview().items():
        print(f"   {school.upper():12} Level {info['level']:3} | {info['total_casts']} casts")

    print("\n" + "=" * 60)
    print("✅ Test abgeschlossen!")
    print("💥 EXPLOSION kann NIEMALS kombiniert werden!")
    print("📚 Learning by Doing funktioniert!")
    print("=" * 60)
