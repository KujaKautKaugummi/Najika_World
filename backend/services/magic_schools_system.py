"""
Magic Schools System - Najika World
====================================

9 Magieschulen mit Skyrim-Style "Learning by Doing"

Die 9 Schulen (alle eigenständig):
1. Feuer - Fire magic
2. Eis - Ice magic
3. Blitz - Lightning magic
4. Wasser - Water magic
5. Erde - Earth magic
6. Wind - Wind magic
7. Licht - Light magic
8. Dunkelheit - Darkness magic
9. Explosion - NIEMALS kombinierbar! (Gebot #3)

Skyrim-Style:
- Skills steigen durch VERWENDUNG
- Jede Nutzung = XP für diese Schule
- Level-Ups freischalten Zauber/Perks
- KEINE Kombination zwischen Schulen (Explosion!)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime
import math


class MagicSchool(Enum):
    """9 Magieschulen"""
    FIRE = "feuer"
    ICE = "eis"
    LIGHTNING = "blitz"
    WATER = "wasser"
    EARTH = "erde"
    WIND = "wind"
    LIGHT = "licht"
    DARKNESS = "dunkelheit"
    EXPLOSION = "explosion"  # NIEMALS kombinierbar!


class SpellTier(Enum):
    """Zauber-Tiers"""
    NOVICE = "novice"        # Level 1-24
    APPRENTICE = "apprentice"  # Level 25-49
    ADEPT = "adept"          # Level 50-74
    EXPERT = "expert"        # Level 75-99
    MASTER = "master"        # Level 100


@dataclass
class Spell:
    """Ein Zauber"""
    spell_id: str
    name: str
    school: MagicSchool
    tier: SpellTier

    # Requirements
    required_level: int
    mana_cost: int

    # Stats
    base_damage: int = 0
    base_healing: int = 0
    duration: float = 0.0  # in seconds
    cooldown: float = 0.0  # in seconds

    # Description
    description: str = ""

    # Special flags
    is_ultimate: bool = False
    can_weave: bool = True  # False für Explosion!


@dataclass
class SchoolProgress:
    """Fortschritt in einer Schule"""
    school: MagicSchool
    level: int = 1
    experience: float = 0.0

    # Experience for next level (exponential)
    exp_for_next_level: float = 100.0

    # Total stats
    total_casts: int = 0
    total_damage_dealt: float = 0.0
    total_mana_spent: int = 0

    # Unlocked spells
    unlocked_spells: List[str] = field(default_factory=list)

    # Timestamps
    first_cast: Optional[datetime] = None
    last_cast: Optional[datetime] = None


class MagicSchoolSystem:
    """
    Magic School System Manager

    Verwaltet 9 Magieschulen mit Skyrim-Style Progression
    """

    def __init__(self):
        # Player progress per school
        self.school_progress: Dict[MagicSchool, SchoolProgress] = {}

        # Spell database
        self.spells: Dict[str, Spell] = {}

        # Initialize all schools at level 1
        for school in MagicSchool:
            self.school_progress[school] = SchoolProgress(school=school)

        # Experience curve settings
        self.BASE_EXP_FOR_LEVEL = 100.0
        self.EXP_MULTIPLIER = 1.05  # Exponential growth

        # Learning rates
        self.BASE_EXP_PER_CAST = 10.0
        self.DAMAGE_TO_EXP_RATIO = 0.1  # 10 damage = 1 XP

        # Spell tier unlock levels
        self.TIER_UNLOCK_LEVELS = {
            SpellTier.NOVICE: 1,
            SpellTier.APPRENTICE: 25,
            SpellTier.ADEPT: 50,
            SpellTier.EXPERT: 75,
            SpellTier.MASTER: 100
        }


    def cast_spell(
        self,
        spell_id: str,
        damage_dealt: float = 0.0
    ) -> Dict:
        """
        Zauber casten und XP geben (Skyrim-Style!)

        Args:
            spell_id: Spell ID
            damage_dealt: Schaden der gemacht wurde

        Returns:
            Result dict mit XP/Level-Up Info
        """
        if spell_id not in self.spells:
            return {"error": "Zauber nicht gefunden"}

        spell = self.spells[spell_id]
        progress = self.school_progress[spell.school]

        # Calculate XP
        base_xp = self.BASE_EXP_PER_CAST
        damage_xp = damage_dealt * self.DAMAGE_TO_EXP_RATIO
        total_xp = base_xp + damage_xp

        # Tier multiplier (higher tiers give more XP)
        tier_mult = {
            SpellTier.NOVICE: 1.0,
            SpellTier.APPRENTICE: 1.5,
            SpellTier.ADEPT: 2.0,
            SpellTier.EXPERT: 2.5,
            SpellTier.MASTER: 3.0
        }
        total_xp *= tier_mult.get(spell.tier, 1.0)

        # Add XP
        old_level = progress.level
        progress.experience += total_xp

        # Update stats
        progress.total_casts += 1
        progress.total_damage_dealt += damage_dealt
        progress.total_mana_spent += spell.mana_cost

        if not progress.first_cast:
            progress.first_cast = datetime.now()
        progress.last_cast = datetime.now()

        # Check for level-up
        leveled_up = False
        new_spells_unlocked = []

        while progress.experience >= progress.exp_for_next_level:
            progress.experience -= progress.exp_for_next_level
            progress.level += 1
            leveled_up = True

            # Calculate next level exp requirement (exponential)
            progress.exp_for_next_level = self._calculate_exp_for_level(progress.level)

            # Check for spell unlocks
            newly_unlocked = self._check_spell_unlocks(spell.school, progress.level)
            new_spells_unlocked.extend(newly_unlocked)
            progress.unlocked_spells.extend(newly_unlocked)

        result = {
            "spell_id": spell_id,
            "spell_name": spell.name,
            "school": spell.school.value,
            "xp_gained": total_xp,
            "current_level": progress.level,
            "current_exp": progress.experience,
            "exp_for_next": progress.exp_for_next_level,
            "leveled_up": leveled_up,
            "old_level": old_level,
            "new_spells_unlocked": new_spells_unlocked
        }

        if leveled_up:
            result["level_up_message"] = (
                f"🎉 {spell.school.value.upper()} Level {progress.level}!"
            )

        return result


    def _calculate_exp_for_level(self, level: int) -> float:
        """
        Berechnet XP für nächstes Level (exponentiell)

        Skyrim-Style: Immer schwerer!
        """
        return self.BASE_EXP_FOR_LEVEL * (self.EXP_MULTIPLIER ** (level - 1))


    def _check_spell_unlocks(
        self,
        school: MagicSchool,
        new_level: int
    ) -> List[str]:
        """
        Prüft welche Zauber freigeschaltet wurden

        Returns:
            Liste von Spell IDs
        """
        unlocked = []

        for spell_id, spell in self.spells.items():
            if spell.school != school:
                continue

            if spell.required_level == new_level:
                unlocked.append(spell_id)

        return unlocked


    def get_school_info(self, school: MagicSchool) -> Dict:
        """Holt Info über eine Schule"""
        progress = self.school_progress[school]

        # Get available spells
        available_spells = [
            {
                "spell_id": spell.spell_id,
                "name": spell.name,
                "tier": spell.tier.value,
                "mana_cost": spell.mana_cost,
                "required_level": spell.required_level,
                "unlocked": spell.spell_id in progress.unlocked_spells
            }
            for spell in self.spells.values()
            if spell.school == school and spell.required_level <= progress.level
        ]

        return {
            "school": school.value,
            "level": progress.level,
            "experience": progress.experience,
            "exp_for_next_level": progress.exp_for_next_level,
            "progress_percent": (progress.experience / progress.exp_for_next_level * 100),
            "total_casts": progress.total_casts,
            "total_damage": progress.total_damage_dealt,
            "total_mana_spent": progress.total_mana_spent,
            "available_spells": available_spells,
            "first_cast": progress.first_cast.isoformat() if progress.first_cast else None,
            "last_cast": progress.last_cast.isoformat() if progress.last_cast else None
        }


    def get_all_schools_overview(self) -> Dict:
        """Holt Übersicht über alle Schulen"""
        overview = {}

        for school in MagicSchool:
            progress = self.school_progress[school]
            overview[school.value] = {
                "level": progress.level,
                "experience": progress.experience,
                "total_casts": progress.total_casts,
                "unlocked_spells": len(progress.unlocked_spells)
            }

        return overview


    def can_weave(self, school1: MagicSchool, school2: MagicSchool) -> Tuple[bool, str]:
        """
        Prüft ob 2 Schulen kombiniert werden können (Weave)

        WICHTIG: Explosion NIEMALS kombinierbar! (Gebot #3)

        Returns:
            (can_weave, reason)
        """
        # Gebot #3: Explosion ≠ Weave!
        if school1 == MagicSchool.EXPLOSION or school2 == MagicSchool.EXPLOSION:
            return False, "EXPLOSION kann NIEMALS kombiniert werden! (Gebot #3)"

        # Same school = no weave
        if school1 == school2:
            return False, "Gleiche Schule kann nicht kombiniert werden"

        # Check levels
        progress1 = self.school_progress[school1]
        progress2 = self.school_progress[school2]

        if progress1.level < 10 or progress2.level < 10:
            return False, "Beide Schulen müssen Level 10+ sein für Weave"

        return True, "Weave möglich"


    def register_spell(self, spell: Spell):
        """Registriert einen Zauber"""
        self.spells[spell.spell_id] = spell

        # Auto-unlock Novice spells
        if spell.tier == SpellTier.NOVICE and spell.required_level == 1:
            progress = self.school_progress[spell.school]
            if spell.spell_id not in progress.unlocked_spells:
                progress.unlocked_spells.append(spell.spell_id)


    def create_default_spells(self):
        """Erstellt Standard-Zauber für alle 9 Schulen"""

        # FEUER
        self.register_spell(Spell(
            spell_id="fire_novice_1",
            name="Flammen",
            school=MagicSchool.FIRE,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=10,
            base_damage=20,
            description="Einfacher Feuerball"
        ))

        self.register_spell(Spell(
            spell_id="fire_master_1",
            name="Inferno",
            school=MagicSchool.FIRE,
            tier=SpellTier.MASTER,
            required_level=100,
            mana_cost=100,
            base_damage=500,
            description="Massiver Feuersturm"
        ))

        # EIS
        self.register_spell(Spell(
            spell_id="ice_novice_1",
            name="Frost",
            school=MagicSchool.ICE,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=10,
            base_damage=18,
            description="Einfacher Eisstrahl"
        ))

        # BLITZ
        self.register_spell(Spell(
            spell_id="lightning_novice_1",
            name="Funken",
            school=MagicSchool.LIGHTNING,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=12,
            base_damage=25,
            description="Elektrischer Schock"
        ))

        # WASSER
        self.register_spell(Spell(
            spell_id="water_novice_1",
            name="Wasser-Geschoss",
            school=MagicSchool.WATER,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=8,
            base_damage=15,
            description="Wasserstrahl"
        ))

        # ERDE
        self.register_spell(Spell(
            spell_id="earth_novice_1",
            name="Stein-Geschoss",
            school=MagicSchool.EARTH,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=15,
            base_damage=30,
            description="Wirft einen Stein"
        ))

        # WIND
        self.register_spell(Spell(
            spell_id="wind_novice_1",
            name="Windstoß",
            school=MagicSchool.WIND,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=8,
            base_damage=12,
            description="Starker Windstoß"
        ))

        # LICHT
        self.register_spell(Spell(
            spell_id="light_novice_1",
            name="Lichtstrahl",
            school=MagicSchool.LIGHT,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=10,
            base_damage=22,
            description="Heiliger Lichtstrahl"
        ))

        # DUNKELHEIT
        self.register_spell(Spell(
            spell_id="darkness_novice_1",
            name="Schatten-Geschoss",
            school=MagicSchool.DARKNESS,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=10,
            base_damage=20,
            description="Dunkle Energie"
        ))

        # EXPLOSION (NIEMALS kombinierbar!)
        self.register_spell(Spell(
            spell_id="explosion_novice_1",
            name="Kleine Explosion",
            school=MagicSchool.EXPLOSION,
            tier=SpellTier.NOVICE,
            required_level=1,
            mana_cost=50,
            base_damage=100,
            description="Kleine Explosion (Megumin-Style)",
            can_weave=False  # NIEMALS kombinierbar!
        ))

        self.register_spell(Spell(
            spell_id="explosion_master_1",
            name="REINSTE EXPLOSION",
            school=MagicSchool.EXPLOSION,
            tier=SpellTier.MASTER,
            required_level=100,
            mana_cost=500,
            base_damage=5000,
            description="Najika's Ultimate - 1x/Tag, für ALLE sichtbar!",
            is_ultimate=True,
            can_weave=False
        ))


    def export_state(self) -> Dict:
        """Exportiert kompletten State"""
        return {
            "schools": {
                school.value: {
                    "level": progress.level,
                    "experience": progress.experience,
                    "exp_for_next_level": progress.exp_for_next_level,
                    "total_casts": progress.total_casts,
                    "total_damage": progress.total_damage_dealt,
                    "total_mana_spent": progress.total_mana_spent,
                    "unlocked_spells": progress.unlocked_spells,
                    "first_cast": progress.first_cast.isoformat() if progress.first_cast else None,
                    "last_cast": progress.last_cast.isoformat() if progress.last_cast else None
                }
                for school, progress in self.school_progress.items()
            }
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== Magic Schools System Test ===\n")

    magic_sys = MagicSchoolSystem()
    magic_sys.create_default_spells()

    # Test 1: Cast Feuer spell
    print("1. Cast Flammen (Feuer Novice)")
    result = magic_sys.cast_spell("fire_novice_1", damage_dealt=20.0)
    print(f"   XP gained: {result['xp_gained']:.1f}")
    print(f"   Level: {result['current_level']}")
    print(f"   Progress: {result['current_exp']:.1f}/{result['exp_for_next']:.1f}\n")

    # Test 2: Cast many times (level up!)
    print("2. Cast 50x Flammen (level ups!)")
    for i in range(50):
        result = magic_sys.cast_spell("fire_novice_1", damage_dealt=25.0)
        if result.get('leveled_up'):
            print(f"   {result['level_up_message']}")

    print(f"   Final Level: {result['current_level']}\n")

    # Test 3: School Info
    print("3. Feuer School Info")
    info = magic_sys.get_school_info(MagicSchool.FIRE)
    print(f"   Level: {info['level']}")
    print(f"   Total Casts: {info['total_casts']}")
    print(f"   Total Damage: {info['total_damage']:.0f}")
    print(f"   Available Spells: {len(info['available_spells'])}\n")

    # Test 4: Weave Check (Feuer + Eis)
    print("4. Weave Check (Feuer + Eis)")
    can_weave, reason = magic_sys.can_weave(MagicSchool.FIRE, MagicSchool.ICE)
    print(f"   Can Weave: {can_weave}")
    print(f"   Reason: {reason}\n")

    # Test 5: Weave Check (Feuer + Explosion) - SHOULD FAIL!
    print("5. Weave Check (Feuer + Explosion) - GEBOT #3!")
    can_weave, reason = magic_sys.can_weave(MagicSchool.FIRE, MagicSchool.EXPLOSION)
    print(f"   Can Weave: {can_weave}")
    print(f"   Reason: {reason}\n")

    # Test 6: All Schools Overview
    print("6. All Schools Overview")
    overview = magic_sys.get_all_schools_overview()
    for school_name, stats in overview.items():
        print(f"   {school_name.upper()}: Level {stats['level']} "
              f"({stats['total_casts']} casts)")

    print("\n=== Magic Schools System Test Complete ===")
    print("✅ Feuer ist NICHT Explosion!")
    print("✅ Explosion kann NIEMALS kombiniert werden!")
    print("✅ Skyrim Learning by Doing funktioniert!")
