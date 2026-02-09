"""
NAJIKA MAGIC SYSTEM V3 - VEREINFACHT!
=====================================
Hauptfokus: SKYRIM (Learning by Doing)
+ Konosuba (Explosion-Klasse)
+ ESO (Morphs durch Leveln)
+ Fallout (S.P.E.C.I.A.L. Stats, VATS-Style Targeting)

REGELN:
- Keine Klassen! Jeder kann alles lernen
- Explosion = normale Magieschule (kostet Mana/Stamina)
- Explosion Finisher = 1x pro Tag
- Andere Schulen koennen VERWEBEN (Feuer+Wasser etc.)
- Skills entwickeln sich durch Nutzung (Morphs)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import random
from datetime import datetime, timedelta


# =============================================================================
# FALLOUT S.P.E.C.I.A.L. STATS
# =============================================================================
class SpecialStat(Enum):
    """Fallout-Style Basis-Attribute"""
    STRENGTH = "strength"        # Nahkampf-Schaden, Tragen
    PERCEPTION = "perception"    # VATS-Praezision, Erkennung
    ENDURANCE = "endurance"      # HP, Stamina, Gift-Resistenz
    CHARISMA = "charisma"        # NPC-Preise, Party-Boni
    INTELLIGENCE = "intelligence" # Magie-Schaden, XP-Bonus
    AGILITY = "agility"          # Ausweichen, Kritisch, Initiative
    LUCK = "luck"                # Crit-Chance, Drops, Skill-Lernen


@dataclass
class PlayerStats:
    """Spieler Attribute (1-10 Basis, kann durch Buffs hoeher)"""
    strength: int = 5
    perception: int = 5
    endurance: int = 5
    charisma: int = 5
    intelligence: int = 5
    agility: int = 5
    luck: int = 5

    def get_stat(self, stat: SpecialStat) -> int:
        return getattr(self, stat.value)

    def modify_stat(self, stat: SpecialStat, amount: int):
        current = getattr(self, stat.value)
        setattr(self, stat.value, max(1, min(15, current + amount)))  # 1-15 Range


# =============================================================================
# MAGIESCHULEN (9 Schulen + Explosion als 10.)
# =============================================================================
class MagicSchool(Enum):
    """Die 10 Magieschulen - ALLE sind fuer JEDEN lernbar!"""
    # Elemente (koennen VERWEBEN!)
    FIRE = "fire"           # Schaden, DoT
    WATER = "water"         # Heilung, Debuff-Cleanse
    EARTH = "earth"         # Defense, Stagger
    WIND = "wind"           # Speed, Evasion
    LIGHTNING = "lightning" # Burst, Stun
    ICE = "ice"             # Slow, Freeze
    NATURE = "nature"       # HoT, Summons
    DARK = "dark"           # Debuffs, Lifesteal
    LIGHT = "light"         # Buffs, Anti-Undead

    # EXPLOSION - NICHT verweben! Eigener Pfad
    EXPLOSION = "explosion"


# Element-Verweben Kombinationen (NICHT fuer Explosion!)
ELEMENT_WEAVES = {
    ("fire", "water"): "steam",       # Blind, AoE Schaden
    ("fire", "wind"): "firestorm",    # Groesserer AoE
    ("fire", "earth"): "magma",       # DoT + Slow
    ("water", "wind"): "blizzard",    # AoE Freeze
    ("water", "earth"): "mud",        # Root, Slow
    ("lightning", "water"): "shock",  # Chain Lightning
    ("lightning", "wind"): "tempest", # Random Strikes
    ("earth", "wind"): "sandstorm",   # Blind, DoT
    ("ice", "fire"): "thermal",       # Bonus vs Armor
    ("dark", "light"): "void",        # True Damage
}


# =============================================================================
# SKILL-SYSTEM (Skyrim Learning by Doing)
# =============================================================================
@dataclass
class Skill:
    """Ein einzelner Skill"""
    id: str
    name: str
    school: MagicSchool
    level: int = 1                  # 1-100 (Skyrim-Style)
    xp: int = 0
    xp_to_next: int = 100

    # Kosten
    mana_cost: int = 10
    stamina_cost: int = 0

    # Effekte
    base_damage: int = 0
    base_heal: int = 0
    effect_type: str = "damage"     # damage, heal, buff, debuff

    # Morph-System (ESO-Style)
    morph_available_at: int = 25    # Level fuer Morph-Wahl
    morph_chosen: Optional[str] = None
    morph_options: List[str] = field(default_factory=list)

    def use(self) -> Dict:
        """Skill nutzen = XP gewinnen (Skyrim!)"""
        xp_gain = random.randint(5, 15)
        self.xp += xp_gain

        leveled_up = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.15)  # +15% pro Level
            leveled_up = True

        return {
            "xp_gained": xp_gain,
            "new_level": self.level,
            "leveled_up": leveled_up,
            "morph_available": self.level >= self.morph_available_at and not self.morph_chosen
        }

    def calculate_power(self, stats: PlayerStats) -> int:
        """Berechne Staerke basierend auf Stats"""
        base = self.base_damage or self.base_heal

        # INT fuer Magie, STR fuer physische Skills
        if self.school == MagicSchool.EXPLOSION:
            # Explosion skaliert mit INT + ein bisschen LUCK
            multiplier = 1 + (stats.intelligence * 0.05) + (stats.luck * 0.02)
        else:
            multiplier = 1 + (stats.intelligence * 0.05)

        # Skill-Level Bonus
        level_bonus = 1 + (self.level * 0.02)  # +2% pro Level

        return int(base * multiplier * level_bonus)


# =============================================================================
# EXPLOSION-KLASSE (Konosuba-Style, aber lernbar!)
# =============================================================================
@dataclass
class ExplosionSkill(Skill):
    """
    Explosion - Eine NORMALE Magieschule!
    - Kostet viel Mana + Stamina
    - 1x pro Tag: FINISHER (Omega-Detonation nur Najika!)
    """
    tier: int = 1                   # 1=Basis, 2=Fortgeschritten, 3=Ultima (nur Najika)
    finisher_used_today: bool = False
    finisher_last_used: Optional[datetime] = None

    # Waffen-Morph (Diablo-Style)
    weapon_morph: Optional[str] = None  # sword, spear, axe, bow, etc.

    def __post_init__(self):
        self.school = MagicSchool.EXPLOSION
        self.mana_cost = 50 + (self.tier * 30)      # 80, 110, 140
        self.stamina_cost = 30 + (self.tier * 20)   # 50, 70, 90
        self.base_damage = 100 + (self.tier * 100)  # 200, 300, 400

    def can_use_finisher(self) -> bool:
        """Finisher 1x pro Tag"""
        if self.finisher_used_today:
            return False
        if self.finisher_last_used:
            time_since = datetime.now() - self.finisher_last_used
            return time_since > timedelta(hours=24)
        return True

    def use_finisher(self, is_najika: bool = False) -> Dict:
        """
        FINISHER - 1x pro Tag!
        Najika hat Tier 3 (Omega-Detonation)
        """
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
            "cooldown_hours": 24
        }

    def apply_weapon_morph(self, weapon: str):
        """Waffen-Morph (Diablo-Style)"""
        weapon_effects = {
            "sword": {"name": "Explosion: Klinge", "bonus": "Haltungsbruch"},
            "spear": {"name": "Explosion: Stoss", "bonus": "Linien-Durchdringung"},
            "axe": {"name": "Explosion: Einschlag", "bonus": "Bodenwelle + Stagger"},
            "hammer": {"name": "Explosion: Einschlag", "bonus": "Bodenwelle + Stagger"},
            "shield": {"name": "Explosion: Schildstoss", "bonus": "Konter-Explosion"},
            "bow": {"name": "Explosion: Pfeil", "bonus": "Distanz + Kette"},
            "dagger": {"name": "Explosion: Stich", "bonus": "Mikro-Explosionen"},
            "repeater": {"name": "Explosion: Takt", "bonus": "Kombo-Zaehler"},
            "shotgun": {"name": "Explosion: Schrot", "bonus": "Streu-Explosionen"},
        }

        if weapon in weapon_effects:
            self.weapon_morph = weapon
            return weapon_effects[weapon]
        return None


# =============================================================================
# VATS-STYLE TARGETING (ohne Zeitlupe!)
# =============================================================================
class BodyPart(Enum):
    """Koerperteile fuer gezieltes Angreifen"""
    HEAD = "head"           # +50% Schaden, -30% Trefferchance
    TORSO = "torso"         # Normal
    LEFT_ARM = "left_arm"   # Entwaffnen moeglich
    RIGHT_ARM = "right_arm" # Entwaffnen moeglich
    LEFT_LEG = "left_leg"   # Slow-Effekt
    RIGHT_LEG = "right_leg" # Slow-Effekt


@dataclass
class TargetAnalysis:
    """VATS-Analyse OHNE Zeitlupe - Pre-Combat!"""
    target_name: str
    body_parts: Dict[BodyPart, Dict] = field(default_factory=dict)
    weakness_revealed: bool = False

    def analyze(self, perception: int, intelligence: int) -> Dict:
        """Analysiere Gegner vor dem Kampf"""
        analysis_skill = perception + (intelligence // 2)

        # Basis-Treffchancen
        base_chances = {
            BodyPart.HEAD: 40,
            BodyPart.TORSO: 85,
            BodyPart.LEFT_ARM: 60,
            BodyPart.RIGHT_ARM: 60,
            BodyPart.LEFT_LEG: 55,
            BodyPart.RIGHT_LEG: 55,
        }

        # Perception erhoeht Treffchance
        for part, base in base_chances.items():
            modified = min(95, base + (perception * 2))
            self.body_parts[part] = {
                "hit_chance": modified,
                "damage_mod": 1.5 if part == BodyPart.HEAD else 1.0,
                "effect": self._get_part_effect(part)
            }

        # Intelligence enthuellt Schwaechen
        self.weakness_revealed = analysis_skill >= 12

        return {
            "body_parts": {p.value: v for p, v in self.body_parts.items()},
            "weakness_revealed": self.weakness_revealed,
            "analysis_quality": "Detailliert" if analysis_skill >= 15 else
                               "Gut" if analysis_skill >= 10 else "Basis"
        }

    def _get_part_effect(self, part: BodyPart) -> str:
        effects = {
            BodyPart.HEAD: "Kritischer Treffer moeglich",
            BodyPart.TORSO: "Kein Spezialeffekt",
            BodyPart.LEFT_ARM: "Kann Waffe entwaffnen",
            BodyPart.RIGHT_ARM: "Kann Schild entwaffnen",
            BodyPart.LEFT_LEG: "Verlangsamt Gegner",
            BodyPart.RIGHT_LEG: "Verlangsamt Gegner",
        }
        return effects.get(part, "")


# =============================================================================
# SKILL-DATENBANK
# =============================================================================
SKILL_DATABASE = {
    # FEUER
    "fireball": Skill(
        id="fireball", name="Feuerball", school=MagicSchool.FIRE,
        mana_cost=15, base_damage=30, effect_type="damage",
        morph_options=["meteor", "fire_stream"]
    ),
    "fire_shield": Skill(
        id="fire_shield", name="Feuerschild", school=MagicSchool.FIRE,
        mana_cost=25, effect_type="buff",
        morph_options=["flame_cloak", "fire_reflect"]
    ),

    # WASSER
    "heal": Skill(
        id="heal", name="Heilung", school=MagicSchool.WATER,
        mana_cost=20, base_heal=40, effect_type="heal",
        morph_options=["greater_heal", "heal_over_time"]
    ),
    "water_shield": Skill(
        id="water_shield", name="Wasserschild", school=MagicSchool.WATER,
        mana_cost=20, effect_type="buff",
        morph_options=["absorb_shield", "cleanse_shield"]
    ),

    # BLITZ
    "lightning_bolt": Skill(
        id="lightning_bolt", name="Blitz", school=MagicSchool.LIGHTNING,
        mana_cost=25, base_damage=35, effect_type="damage",
        morph_options=["chain_lightning", "thunder_strike"]
    ),

    # ERDE
    "stone_armor": Skill(
        id="stone_armor", name="Steinpanzer", school=MagicSchool.EARTH,
        mana_cost=30, effect_type="buff",
        morph_options=["obsidian_armor", "earth_spikes"]
    ),
    "earthquake": Skill(
        id="earthquake", name="Erdbeben", school=MagicSchool.EARTH,
        mana_cost=40, base_damage=50, effect_type="damage",
        morph_options=["fissure", "tremor"]
    ),

    # WIND
    "haste": Skill(
        id="haste", name="Eile", school=MagicSchool.WIND,
        mana_cost=15, effect_type="buff",
        morph_options=["group_haste", "combat_speed"]
    ),
    "wind_blade": Skill(
        id="wind_blade", name="Windklinge", school=MagicSchool.WIND,
        mana_cost=18, base_damage=25, effect_type="damage",
        morph_options=["air_slash", "tornado"]
    ),

    # EIS
    "frost_spike": Skill(
        id="frost_spike", name="Eiszapfen", school=MagicSchool.ICE,
        mana_cost=15, base_damage=28, effect_type="damage",
        morph_options=["ice_lance", "frost_nova"]
    ),
    "freeze": Skill(
        id="freeze", name="Einfrieren", school=MagicSchool.ICE,
        mana_cost=35, effect_type="debuff",
        morph_options=["deep_freeze", "ice_prison"]
    ),

    # NATUR
    "summon_wolf": Skill(
        id="summon_wolf", name="Wolf beschwören", school=MagicSchool.NATURE,
        mana_cost=40, effect_type="summon",
        morph_options=["dire_wolf", "pack_wolves"]
    ),
    "entangle": Skill(
        id="entangle", name="Verstricken", school=MagicSchool.NATURE,
        mana_cost=20, effect_type="debuff",
        morph_options=["thorns", "root"]
    ),

    # DUNKEL
    "drain_life": Skill(
        id="drain_life", name="Leben entziehen", school=MagicSchool.DARK,
        mana_cost=30, base_damage=25, base_heal=20, effect_type="damage",
        morph_options=["soul_drain", "mass_drain"]
    ),
    "curse": Skill(
        id="curse", name="Fluch", school=MagicSchool.DARK,
        mana_cost=25, effect_type="debuff",
        morph_options=["hex", "doom"]
    ),

    # LICHT
    "blessing": Skill(
        id="blessing", name="Segen", school=MagicSchool.LIGHT,
        mana_cost=20, effect_type="buff",
        morph_options=["greater_blessing", "aura"]
    ),
    "smite": Skill(
        id="smite", name="Heiliges Licht", school=MagicSchool.LIGHT,
        mana_cost=25, base_damage=35, effect_type="damage",
        morph_options=["holy_fire", "purify"]
    ),

    # EXPLOSION (Konosuba!)
    "explosion_basic": ExplosionSkill(
        id="explosion_basic", name="Explosion", tier=1,
        morph_options=[]  # Explosion morpht durch Waffen, nicht Skills!
    ),
    "explosion_advanced": ExplosionSkill(
        id="explosion_advanced", name="EXPLOOOOSION!", tier=2,
    ),
}


# =============================================================================
# SPIELER-KLASSE
# =============================================================================
@dataclass
class Player:
    """
    Spieler - KEINE Klassen!
    Kann ALLES lernen (Skyrim-Style)
    """
    name: str
    is_najika: bool = False

    # Fallout S.P.E.C.I.A.L.
    stats: PlayerStats = field(default_factory=PlayerStats)

    # Ressourcen
    hp: int = 100
    max_hp: int = 100
    mana: int = 100
    max_mana: int = 100
    stamina: int = 100
    max_stamina: int = 100

    # Skills (Skyrim - Learning by Doing)
    learned_skills: Dict[str, Skill] = field(default_factory=dict)

    # School Mastery (0-100)
    school_mastery: Dict[MagicSchool, int] = field(default_factory=lambda: {
        school: 0 for school in MagicSchool
    })

    def learn_skill(self, skill_id: str) -> Dict:
        """Skill lernen (Konosuba: von Party, Trainern, Grimoires)"""
        if skill_id in self.learned_skills:
            return {"success": False, "error": "Skill bereits bekannt!"}

        if skill_id not in SKILL_DATABASE:
            return {"success": False, "error": "Skill existiert nicht!"}

        # Kopie erstellen (nicht die Originaldaten ändern!)
        import copy
        skill = copy.deepcopy(SKILL_DATABASE[skill_id])
        self.learned_skills[skill_id] = skill

        return {
            "success": True,
            "skill": skill.name,
            "school": skill.school.value,
            "message": f"{self.name} hat {skill.name} gelernt!"
        }

    def use_skill(self, skill_id: str, target: Optional['TargetAnalysis'] = None,
                  body_part: Optional[BodyPart] = None) -> Dict:
        """
        Skill nutzen = XP gewinnen (Skyrim!)
        Optional: VATS-Style Koerperteil-Targeting
        """
        if skill_id not in self.learned_skills:
            return {"success": False, "error": "Skill nicht gelernt!"}

        skill = self.learned_skills[skill_id]

        # Kosten prüfen
        if self.mana < skill.mana_cost:
            return {"success": False, "error": "Nicht genug Mana!"}
        if self.stamina < skill.stamina_cost:
            return {"success": False, "error": "Nicht genug Stamina!"}

        # Kosten abziehen
        self.mana -= skill.mana_cost
        self.stamina -= skill.stamina_cost

        # Skill nutzen (XP!)
        result = skill.use()

        # School Mastery erhoehen
        self.school_mastery[skill.school] = min(100,
            self.school_mastery[skill.school] + random.randint(1, 3))

        # Schaden/Heilung berechnen
        power = skill.calculate_power(self.stats)

        # VATS-Targeting Modifikation
        if target and body_part and body_part in target.body_parts:
            part_data = target.body_parts[body_part]

            # Trefferchance prüfen
            hit_roll = random.randint(1, 100)
            if hit_roll > part_data["hit_chance"]:
                return {
                    "success": True,
                    "hit": False,
                    "message": f"Verfehlt! ({hit_roll} > {part_data['hit_chance']}%)"
                }

            power = int(power * part_data["damage_mod"])
            result["targeted_part"] = body_part.value
            result["special_effect"] = part_data["effect"]

        result["power"] = power
        result["mana_spent"] = skill.mana_cost
        result["stamina_spent"] = skill.stamina_cost
        result["school_mastery"] = self.school_mastery[skill.school]

        return result

    def weave_elements(self, skill1_id: str, skill2_id: str) -> Dict:
        """
        Element-Verweben (ESO-Style)
        NICHT fuer Explosion!
        """
        if skill1_id not in self.learned_skills or skill2_id not in self.learned_skills:
            return {"success": False, "error": "Skills nicht gelernt!"}

        skill1 = self.learned_skills[skill1_id]
        skill2 = self.learned_skills[skill2_id]

        # Explosion kann NICHT verweben!
        if skill1.school == MagicSchool.EXPLOSION or skill2.school == MagicSchool.EXPLOSION:
            return {"success": False, "error": "Explosion kann nicht mit anderen Elementen verwoben werden!"}

        # Kombination suchen
        combo_key = tuple(sorted([skill1.school.value, skill2.school.value]))
        weave_result = ELEMENT_WEAVES.get(combo_key)

        if not weave_result:
            return {"success": False, "error": f"Diese Elemente können nicht verwoben werden!"}

        # Kosten (beide Skills)
        total_mana = skill1.mana_cost + skill2.mana_cost
        total_stamina = skill1.stamina_cost + skill2.stamina_cost

        if self.mana < total_mana:
            return {"success": False, "error": "Nicht genug Mana für Verweben!"}

        self.mana -= total_mana
        self.stamina -= total_stamina

        # Beide Skills bekommen XP
        skill1.use()
        skill2.use()

        # Verwobene Kraft (bonus!)
        base_power = skill1.calculate_power(self.stats) + skill2.calculate_power(self.stats)
        weave_bonus = 1.3  # 30% Bonus für Verweben

        return {
            "success": True,
            "weave_type": weave_result,
            "elements": [skill1.school.value, skill2.school.value],
            "power": int(base_power * weave_bonus),
            "mana_spent": total_mana,
            "message": f"VERWEBEN: {weave_result.upper()}!"
        }

    def use_explosion_finisher(self) -> Dict:
        """Explosion Finisher (1x pro Tag!)"""
        explosion_skill = None
        for skill in self.learned_skills.values():
            if isinstance(skill, ExplosionSkill):
                if not explosion_skill or skill.tier > explosion_skill.tier:
                    explosion_skill = skill

        if not explosion_skill:
            return {"success": False, "error": "Keine Explosion gelernt!"}

        return explosion_skill.use_finisher(is_najika=self.is_najika)

    def morph_skill(self, skill_id: str, morph_choice: str) -> Dict:
        """Skill morphen (ESO-Style) - durch Leveln freigeschaltet"""
        if skill_id not in self.learned_skills:
            return {"success": False, "error": "Skill nicht gelernt!"}

        skill = self.learned_skills[skill_id]

        if skill.level < skill.morph_available_at:
            return {"success": False, "error": f"Skill muss Level {skill.morph_available_at} sein!"}

        if skill.morph_chosen:
            return {"success": False, "error": "Skill bereits gemorpht!"}

        if morph_choice not in skill.morph_options:
            return {"success": False, "error": f"Ungültige Morph-Wahl! Optionen: {skill.morph_options}"}

        skill.morph_chosen = morph_choice

        return {
            "success": True,
            "skill": skill.name,
            "morph": morph_choice,
            "message": f"{skill.name} zu {morph_choice} gemorpht!"
        }


# =============================================================================
# KONOSUBA-STYLE: VON PARTY LERNEN
# =============================================================================
class PartyLearningSystem:
    """
    Konosuba-Mechanik:
    - Party-Mitglied nutzt Skill
    - Du beobachtest
    - Chance zu lernen!
    """

    BASE_LEARN_CHANCE = 2  # 2% pro Beobachtung

    @staticmethod
    def observe_skill_use(observer: Player, user: Player, skill_id: str) -> Dict:
        """Beobachte Party-Mitglied beim Skill-Einsatz"""
        if skill_id not in user.learned_skills:
            return {"learned": False, "error": "User hat diesen Skill nicht"}

        if skill_id in observer.learned_skills:
            return {"learned": False, "reason": "Bereits bekannt"}

        skill = user.learned_skills[skill_id]

        # Explosion Tier 3 (Omega-Detonation) kann NICHT gelernt werden!
        if isinstance(skill, ExplosionSkill) and skill.tier >= 3:
            return {"learned": False, "reason": "Omega-Detonation ist nicht lehrbar!"}

        # Lernchance berechnen
        # Höhere Mastery des Users = höhere Chance
        user_mastery = user.school_mastery.get(skill.school, 0)
        # Observer's Luck hilft
        luck_bonus = observer.stats.luck * 0.5
        # Intelligence hilft auch
        int_bonus = observer.stats.intelligence * 0.3

        learn_chance = PartyLearningSystem.BASE_LEARN_CHANCE + (user_mastery * 0.1) + luck_bonus + int_bonus

        # Würfeln!
        roll = random.uniform(0, 100)

        if roll <= learn_chance:
            observer.learn_skill(skill_id)
            return {
                "learned": True,
                "skill": skill.name,
                "chance_was": f"{learn_chance:.1f}%",
                "message": f"{observer.name} hat {skill.name} durch Beobachtung gelernt!"
            }

        return {
            "learned": False,
            "chance_was": f"{learn_chance:.1f}%",
            "message": "Diesmal nicht gelernt, aber weiter beobachten!"
        }


# =============================================================================
# TEST / DEMO
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA MAGIC SYSTEM V3 - TEST")
    print("=" * 60)

    # Spieler erstellen
    kuja = Player(name="Kuja")
    kuja.stats.intelligence = 8  # Magier-Build
    kuja.stats.luck = 7

    najika = Player(name="Najika", is_najika=True)
    najika.stats.intelligence = 10
    najika.stats.luck = 10

    # Najika lernt Explosion (alle Tiers)
    najika.learn_skill("explosion_basic")
    najika.learn_skill("explosion_advanced")

    # Kuja lernt normale Magie
    kuja.learn_skill("fireball")
    kuja.learn_skill("heal")
    kuja.learn_skill("lightning_bolt")

    print("\n--- Skills nutzen (Skyrim XP!) ---")
    for _ in range(5):
        result = kuja.use_skill("fireball")
        print(f"Feuerball: Level {result['new_level']}, +{result['xp_gained']} XP")

    print("\n--- Element-Verweben ---")
    kuja.learn_skill("frost_spike")
    result = kuja.weave_elements("fireball", "frost_spike")
    print(f"Verweben: {result}")

    print("\n--- Explosion kann NICHT verweben ---")
    najika.learn_skill("fireball")
    result = najika.weave_elements("explosion_basic", "fireball")
    print(f"Explosion+Feuer: {result['error']}")

    print("\n--- VATS-Style Targeting ---")
    target = TargetAnalysis(target_name="Goblin")
    analysis = target.analyze(perception=kuja.stats.perception, intelligence=kuja.stats.intelligence)
    print(f"Analyse: {analysis['analysis_quality']}")
    for part, data in analysis['body_parts'].items():
        print(f"  {part}: {data['hit_chance']}% Treffer, {data['effect']}")

    print("\n--- Konosuba: Von Party lernen ---")
    # Najika nutzt Explosion, Kuja beobachtet
    najika.use_skill("explosion_basic")
    for attempt in range(20):
        result = PartyLearningSystem.observe_skill_use(kuja, najika, "explosion_basic")
        if result.get("learned"):
            print(f"Versuch {attempt+1}: {result['message']}")
            break
    else:
        print("Noch nicht gelernt - weiter beobachten!")

    print("\n--- Najika's Finisher (Omega-Detonation!) ---")
    result = najika.use_explosion_finisher()
    print(f"Finisher: {result}")

    print("\n--- Kuja's Finisher (max Tier 2) ---")
    if "explosion_basic" in kuja.learned_skills:
        result = kuja.use_explosion_finisher()
        print(f"Finisher: {result}")

    print("\n" + "=" * 60)
    print("EXPLOSION!!! System funktioniert!")
    print("=" * 60)
