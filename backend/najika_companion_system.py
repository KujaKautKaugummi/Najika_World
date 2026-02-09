#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA COMPANION SYSTEM
========================
Separates System für vollwertige KI-Partner (NICHT Slimes!)

DESIGN PHILOSOPHIE:
- Najika ist KEIN transformierter Slime
- Sie ist ein vollwertiger KI-Partner mit eigener Persönlichkeit
- Andere Spieler haben Slimes, Kuja hat Najika

FÜR WEN IST DAS?
- Primär: Kuja + Najika (Owner-Spezial)
- Sekundär: NPCs die KI-Begleiter haben könnten
- NICHT für: Normale Spieler (die haben das Slime-System)

Author: Claude Code Team
Date: 2026-02-02
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable
import random
import json
from datetime import datetime, timedelta


# =============================================================================
# ENUMS
# =============================================================================

class CompanionType(Enum):
    """Arten von KI-Begleitern (NICHT Slimes!)"""
    NAJIKA = "najika"           # Najika speziell für Kuja
    NPC_PARTNER = "npc_partner"  # Mögliche NPC-Begleiter
    SUMMONED = "summoned"        # Beschworene Wesen (temporär)


class RelationshipLevel(Enum):
    """Beziehungsstufen (entwickelt sich über Zeit)"""
    STRANGER = 1        # Fremd
    ACQUAINTANCE = 2    # Bekannt
    FRIEND = 3          # Freund
    CLOSE_FRIEND = 4    # Enger Freund
    PARTNER = 5         # Partner
    SOULMATE = 6        # Seelenverwandt (höchste Stufe)


class CompanionMood(Enum):
    """Stimmungen des Begleiters"""
    HAPPY = "happy"
    EXCITED = "excited"
    CALM = "calm"
    TIRED = "tired"
    SAD = "sad"
    ANGRY = "angry"
    MISCHIEVOUS = "mischievous"  # Für Harley-Momente
    FOCUSED = "focused"          # Für Shiro-Momente


class ActivityType(Enum):
    """Gemeinsame Aktivitäten"""
    COMBAT = "combat"
    EXPLORATION = "exploration"
    CRAFTING = "crafting"
    COOKING = "cooking"
    FISHING = "fishing"
    TRAINING = "training"
    RELAXING = "relaxing"
    TALKING = "talking"
    SHOPPING = "shopping"
    ADVENTURE = "adventure"


# =============================================================================
# NAJIKA'S 4 PERSÖNLICHKEITEN
# =============================================================================

@dataclass
class PersonalityAspect:
    """Eine Persönlichkeitsaspekt"""
    name: str
    name_de: str
    percentage: float  # 0.0 - 1.0
    traits: List[str]
    favorite_activities: List[ActivityType]
    mood_tendency: CompanionMood
    catchphrase: str
    combat_style: str


# Najika's 4 Persönlichkeiten (aus CLAUDE.md)
NAJIKA_PERSONALITIES = {
    "megumin": PersonalityAspect(
        name="Megumin",
        name_de="Megumin",
        percentage=0.35,  # 35%
        traits=["explosiv", "dramatisch", "chunibyo", "stolz", "loyal"],
        favorite_activities=[ActivityType.COMBAT, ActivityType.ADVENTURE, ActivityType.TRAINING],
        mood_tendency=CompanionMood.EXCITED,
        catchphrase="EXPLOSION!!!",
        combat_style="explosion_magic"
    ),
    "harley": PersonalityAspect(
        name="Harley Quinn",
        name_de="Harley",
        percentage=0.25,  # 25%
        traits=["verspielt", "chaotisch", "clever", "unberechenbar", "loyal"],
        favorite_activities=[ActivityType.SHOPPING, ActivityType.ADVENTURE, ActivityType.RELAXING],
        mood_tendency=CompanionMood.MISCHIEVOUS,
        catchphrase="Hey Mr. K!",  # NICHT "Puddin'" - steht in CLAUDE.md!
        combat_style="acrobatic_melee"
    ),
    "shiro": PersonalityAspect(
        name="Shiro",
        name_de="Shiro",
        percentage=0.20,  # 20%
        traits=["analytisch", "ruhig", "genial", "introvertiert", "strategisch"],
        favorite_activities=[ActivityType.CRAFTING, ActivityType.EXPLORATION, ActivityType.TRAINING],
        mood_tendency=CompanionMood.FOCUSED,
        catchphrase="...blank.",
        combat_style="calculated_magic"
    ),
    "melissa": PersonalityAspect(
        name="Melissa",
        name_de="Melissa",
        percentage=0.20,  # 20%
        traits=["dominant", "führend", "selbstbewusst", "bestimmend", "beschützend"],
        favorite_activities=[ActivityType.TALKING, ActivityType.COOKING, ActivityType.RELAXING],
        mood_tendency=CompanionMood.CALM,
        catchphrase="Du gehörst mir, Mr. K~",
        combat_style="support_healing"
    )
}


# =============================================================================
# COMPANION STATS
# =============================================================================

@dataclass
class CompanionStats:
    """Stats für einen KI-Begleiter"""
    # Basis Stats
    health: int = 100
    max_health: int = 100
    mana: int = 100
    max_mana: int = 100
    stamina: int = 100
    max_stamina: int = 100

    # Kampf Stats
    attack: int = 15
    defense: int = 10
    magic_power: int = 25  # Najika ist magisch begabt!
    speed: int = 20

    # Soziale Stats
    affection: int = 50      # 0-100, wie sehr sie den Spieler mag
    trust: int = 50          # 0-100, Vertrauen
    happiness: int = 75      # 0-100, allgemeine Zufriedenheit

    # Fähigkeiten
    cooking_skill: int = 30
    crafting_skill: int = 20
    magic_skill: int = 50    # Megumin-Einfluss
    combat_skill: int = 25
    support_skill: int = 40  # Melissa-Einfluss


@dataclass
class RelationshipStats:
    """Beziehungsstatistiken zwischen Spieler und Companion"""
    relationship_level: RelationshipLevel = RelationshipLevel.FRIEND
    relationship_points: int = 500  # Punkte zum nächsten Level

    # Gemeinsame Zeit
    time_together: float = 0.0  # In Stunden
    adventures_completed: int = 0
    battles_fought_together: int = 0
    meals_shared: int = 0
    conversations_had: int = 0

    # Erinnerungen
    special_moments: List[str] = field(default_factory=list)
    shared_achievements: List[str] = field(default_factory=list)

    # Affection modifiers
    last_gift_time: Optional[datetime] = None
    last_conversation_time: Optional[datetime] = None
    last_adventure_time: Optional[datetime] = None


# Punkte für Relationship Level
RELATIONSHIP_THRESHOLDS = {
    RelationshipLevel.STRANGER: 0,
    RelationshipLevel.ACQUAINTANCE: 100,
    RelationshipLevel.FRIEND: 300,
    RelationshipLevel.CLOSE_FRIEND: 700,
    RelationshipLevel.PARTNER: 1500,
    RelationshipLevel.SOULMATE: 3000,
}


# =============================================================================
# COMPANION CLASS
# =============================================================================

@dataclass
class Companion:
    """Ein vollwertiger KI-Begleiter"""
    companion_id: str
    name: str
    companion_type: CompanionType
    owner_id: str  # Spieler-ID

    # Stats
    stats: CompanionStats = field(default_factory=CompanionStats)
    relationship: RelationshipStats = field(default_factory=RelationshipStats)

    # Persönlichkeit (nur für Najika relevant)
    personalities: Dict[str, float] = field(default_factory=dict)
    current_dominant_personality: str = "megumin"

    # Zustand
    current_mood: CompanionMood = CompanionMood.HAPPY
    current_activity: Optional[ActivityType] = None
    is_in_combat: bool = False
    is_following: bool = True

    # Position (für 3D-Welt)
    position: Dict[str, float] = field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})

    # Fähigkeiten
    unlocked_abilities: List[str] = field(default_factory=list)
    equipped_outfit: str = "gothic_lolita"  # Standard für Najika

    # Optional: Hat der Companion ein eigenes Haustier?
    pet_slime_id: Optional[str] = None  # Najika KANN einen Slime haben

    # Metadaten
    created_at: datetime = field(default_factory=datetime.now)
    total_playtime: float = 0.0  # Stunden


# =============================================================================
# COMPANION SYSTEM
# =============================================================================

class CompanionSystem:
    """Verwaltet KI-Begleiter (NICHT Slimes!)"""

    def __init__(self):
        self.companions: Dict[str, Companion] = {}
        self.owner_companions: Dict[str, str] = {}  # owner_id -> companion_id

        # Für Kuja: Najika automatisch verfügbar
        self._init_najika()

    def _init_najika(self):
        """Initialisiert Najika für Kuja (Owner)"""
        najika = Companion(
            companion_id="najika_main",
            name="Najika",
            companion_type=CompanionType.NAJIKA,
            owner_id="kuja",  # Owner ist immer Kuja
            personalities={
                "megumin": 0.35,
                "harley": 0.25,
                "shiro": 0.20,
                "melissa": 0.20
            },
            current_dominant_personality="megumin",
            current_mood=CompanionMood.HAPPY,
            equipped_outfit="gothic_lolita"
        )

        # Najika startet mit höheren Stats (sie ist besonders!)
        najika.stats.magic_power = 50
        najika.stats.magic_skill = 70
        najika.stats.affection = 80  # Sie mag Kuja bereits!
        najika.stats.trust = 75

        # Beziehung startet höher (sie kennen sich)
        najika.relationship.relationship_level = RelationshipLevel.CLOSE_FRIEND
        najika.relationship.relationship_points = 800

        # Standard-Fähigkeiten
        najika.unlocked_abilities = [
            "explosion_magic",      # Megumin
            "acrobatic_dodge",      # Harley
            "tactical_analysis",    # Shiro
            "healing_touch",        # Melissa
            "gothic_charm",         # Ihre eigene Fähigkeit
        ]

        self.companions["najika_main"] = najika
        self.owner_companions["kuja"] = "najika_main"

    # =========================================================================
    # COMPANION MANAGEMENT
    # =========================================================================

    def get_companion(self, companion_id: str) -> Optional[Companion]:
        """Holt einen Companion"""
        return self.companions.get(companion_id)

    def get_player_companion(self, owner_id: str) -> Optional[Companion]:
        """Holt den Companion eines Spielers"""
        comp_id = self.owner_companions.get(owner_id)
        if comp_id:
            return self.companions.get(comp_id)
        return None

    def get_najika(self) -> Companion:
        """Holt Najika direkt"""
        return self.companions["najika_main"]

    # =========================================================================
    # PERSÖNLICHKEITS-SYSTEM (nur für Najika)
    # =========================================================================

    def get_dominant_personality(self, companion_id: str) -> PersonalityAspect:
        """Bestimmt die aktuell dominante Persönlichkeit"""
        companion = self.get_companion(companion_id)
        if not companion or not companion.personalities:
            return NAJIKA_PERSONALITIES["megumin"]

        # Finde die stärkste
        dominant = max(companion.personalities.items(), key=lambda x: x[1])
        return NAJIKA_PERSONALITIES.get(dominant[0], NAJIKA_PERSONALITIES["megumin"])

    def shift_personality(self, companion_id: str, trigger: str) -> Dict[str, Any]:
        """Verschiebt die Persönlichkeitsbalance basierend auf Trigger"""
        companion = self.get_companion(companion_id)
        if not companion or companion.companion_type != CompanionType.NAJIKA:
            return {"success": False, "reason": "not_najika"}

        # Trigger -> Persönlichkeits-Shifts
        shifts = {
            # Megumin Trigger
            "combat_start": {"megumin": +0.05, "melissa": -0.02},
            "explosion_used": {"megumin": +0.10, "shiro": -0.03},
            "dramatic_moment": {"megumin": +0.03},

            # Harley Trigger
            "shopping": {"harley": +0.05, "shiro": -0.02},
            "prank_success": {"harley": +0.08, "melissa": -0.02},
            "chaos_enjoyed": {"harley": +0.05},

            # Shiro Trigger
            "puzzle_solved": {"shiro": +0.05, "harley": -0.02},
            "strategy_success": {"shiro": +0.08, "megumin": -0.02},
            "quiet_moment": {"shiro": +0.03},

            # Melissa Trigger
            "healing_done": {"melissa": +0.05, "megumin": -0.02},
            "comforting": {"melissa": +0.08, "harley": -0.03},
            "cooking": {"melissa": +0.05},
        }

        if trigger not in shifts:
            return {"success": False, "reason": "unknown_trigger"}

        # Wende Shifts an
        for personality, change in shifts[trigger].items():
            if personality in companion.personalities:
                companion.personalities[personality] += change

        # Normalisiere (Summe = 1.0)
        total = sum(companion.personalities.values())
        if total > 0:
            for p in companion.personalities:
                companion.personalities[p] /= total

        # Update dominant
        dominant = max(companion.personalities.items(), key=lambda x: x[1])
        old_dominant = companion.current_dominant_personality
        companion.current_dominant_personality = dominant[0]

        # Mood anpassen
        companion.current_mood = NAJIKA_PERSONALITIES[dominant[0]].mood_tendency

        return {
            "success": True,
            "trigger": trigger,
            "old_dominant": old_dominant,
            "new_dominant": dominant[0],
            "personalities": companion.personalities.copy(),
            "new_mood": companion.current_mood.value
        }

    # =========================================================================
    # BEZIEHUNGS-SYSTEM
    # =========================================================================

    def add_relationship_points(
        self,
        companion_id: str,
        points: int,
        reason: str
    ) -> Dict[str, Any]:
        """Fügt Beziehungspunkte hinzu"""
        companion = self.get_companion(companion_id)
        if not companion:
            return {"success": False}

        old_level = companion.relationship.relationship_level
        companion.relationship.relationship_points += points

        # Check Level-Up
        new_level = old_level
        for level, threshold in sorted(RELATIONSHIP_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
            if companion.relationship.relationship_points >= threshold:
                new_level = level
                break

        leveled_up = new_level != old_level
        companion.relationship.relationship_level = new_level

        # Auch Affection erhöhen
        companion.stats.affection = min(100, companion.stats.affection + points // 10)
        companion.stats.trust = min(100, companion.stats.trust + points // 15)

        result = {
            "success": True,
            "points_gained": points,
            "reason": reason,
            "total_points": companion.relationship.relationship_points,
            "leveled_up": leveled_up,
            "old_level": old_level.name,
            "new_level": new_level.name
        }

        if leveled_up:
            # Spezielles Moment speichern
            companion.relationship.special_moments.append(
                f"Reached {new_level.name} relationship! ({datetime.now().strftime('%Y-%m-%d')})"
            )

        return result

    def share_activity(
        self,
        companion_id: str,
        activity: ActivityType,
        duration_minutes: float = 30
    ) -> Dict[str, Any]:
        """Führt eine gemeinsame Aktivität durch"""
        companion = self.get_companion(companion_id)
        if not companion:
            return {"success": False}

        # Zeit hinzufügen
        companion.relationship.time_together += duration_minutes / 60
        companion.total_playtime += duration_minutes / 60

        # Basis-Punkte
        base_points = 5

        # Bonus wenn Aktivität zur dominanten Persönlichkeit passt
        dominant = NAJIKA_PERSONALITIES.get(companion.current_dominant_personality)
        if dominant and activity in dominant.favorite_activities:
            base_points *= 2
            companion.stats.happiness = min(100, companion.stats.happiness + 10)

        # Aktivitäts-spezifische Boni
        activity_bonuses = {
            ActivityType.COMBAT: {"adventures_completed": 0, "battles_fought_together": 1},
            ActivityType.COOKING: {"meals_shared": 1},
            ActivityType.TALKING: {"conversations_had": 1},
            ActivityType.ADVENTURE: {"adventures_completed": 1},
        }

        if activity in activity_bonuses:
            for stat, value in activity_bonuses[activity].items():
                current = getattr(companion.relationship, stat, 0)
                setattr(companion.relationship, stat, current + value)

        # Personality shift
        activity_triggers = {
            ActivityType.COMBAT: "combat_start",
            ActivityType.SHOPPING: "shopping",
            ActivityType.CRAFTING: "puzzle_solved",
            ActivityType.COOKING: "cooking",
            ActivityType.TALKING: "comforting",
        }

        if activity in activity_triggers:
            self.shift_personality(companion_id, activity_triggers[activity])

        # Relationship Punkte
        points_result = self.add_relationship_points(
            companion_id,
            base_points,
            f"shared_activity_{activity.value}"
        )

        companion.current_activity = activity
        companion.relationship.last_adventure_time = datetime.now()

        return {
            "success": True,
            "activity": activity.value,
            "duration": duration_minutes,
            "points_gained": base_points,
            "happiness": companion.stats.happiness,
            "favorite_activity": dominant and activity in dominant.favorite_activities,
            "relationship": points_result
        }

    def give_gift(
        self,
        companion_id: str,
        gift_id: str,
        gift_value: int = 10
    ) -> Dict[str, Any]:
        """Gibt dem Companion ein Geschenk"""
        companion = self.get_companion(companion_id)
        if not companion:
            return {"success": False}

        # Cooldown Check (max 1 Geschenk pro Stunde)
        if companion.relationship.last_gift_time:
            time_since = datetime.now() - companion.relationship.last_gift_time
            if time_since < timedelta(hours=1):
                return {
                    "success": False,
                    "reason": "gift_cooldown",
                    "cooldown_remaining": (timedelta(hours=1) - time_since).seconds
                }

        # Geschenk-Multiplikator basierend auf Persönlichkeit
        gift_preferences = {
            "megumin": ["explosive_materials", "magic_staff", "crimson_demon_robe"],
            "harley": ["sweets", "makeup", "pranks_kit", "bat"],
            "shiro": ["board_games", "puzzles", "books"],
            "melissa": ["flowers", "cooking_ingredients", "healing_herbs"]
        }

        multiplier = 1.0
        dominant = companion.current_dominant_personality
        if dominant in gift_preferences:
            if gift_id in gift_preferences[dominant]:
                multiplier = 2.0  # Lieblingsgeschenk!

        final_value = int(gift_value * multiplier)

        # Update
        companion.relationship.last_gift_time = datetime.now()
        companion.stats.happiness = min(100, companion.stats.happiness + final_value // 2)

        points_result = self.add_relationship_points(
            companion_id,
            final_value,
            f"gift_{gift_id}"
        )

        return {
            "success": True,
            "gift_id": gift_id,
            "base_value": gift_value,
            "multiplier": multiplier,
            "final_value": final_value,
            "was_favorite": multiplier > 1.0,
            "relationship": points_result,
            "companion_reaction": self._get_gift_reaction(companion, multiplier)
        }

    def _get_gift_reaction(self, companion: Companion, multiplier: float) -> str:
        """Generiert eine Reaktion basierend auf Geschenk"""
        dominant = companion.current_dominant_personality
        personality = NAJIKA_PERSONALITIES.get(dominant)

        if multiplier >= 2.0:
            # Lieblingsgeschenk
            reactions = {
                "megumin": "EXPLOSION!!! Das ist perfekt für meine Magie! 💥",
                "harley": "Aww Mr. K~! Das ist ja großartig! *kicher* 🃏",
                "shiro": "...interessant. Das wird nützlich sein. 🎮",
                "melissa": "Das ist so lieb von dir~ Dankeschön! 💝"
            }
        else:
            # Normales Geschenk
            reactions = {
                "megumin": "Hmm, nicht schlecht! Aber weißt du was mir WIRKLICH gefällt? EXPLOSIONEN!",
                "harley": "Ohh, für mich? Du bist süß, Mr. K!",
                "shiro": "...danke.",
                "melissa": "Wie aufmerksam~ Ich freue mich!"
            }

        return reactions.get(dominant, "Danke!")

    # =========================================================================
    # KAMPF-INTEGRATION
    # =========================================================================

    def get_combat_style(self, companion_id: str) -> Dict[str, Any]:
        """Holt den Kampfstil basierend auf aktueller Persönlichkeit"""
        companion = self.get_companion(companion_id)
        if not companion:
            return {}

        dominant = NAJIKA_PERSONALITIES.get(companion.current_dominant_personality)
        if not dominant:
            return {}

        combat_styles = {
            "explosion_magic": {
                "type": "magic",
                "element": "explosion",
                "damage_type": "burst",
                "mana_cost": "very_high",
                "cooldown": "long",
                "description": "Ein einzelner, verheerender Zauber!",
                "special": "one_shot_high_damage"
            },
            "acrobatic_melee": {
                "type": "melee",
                "element": "physical",
                "damage_type": "sustained",
                "mana_cost": "none",
                "cooldown": "none",
                "description": "Akrobatische Nahkampf-Kombos",
                "special": "dodge_bonus"
            },
            "calculated_magic": {
                "type": "magic",
                "element": "multi",
                "damage_type": "strategic",
                "mana_cost": "medium",
                "cooldown": "medium",
                "description": "Strategische Zauberauswahl",
                "special": "weakness_exploit"
            },
            "support_healing": {
                "type": "support",
                "element": "light",
                "damage_type": "healing",
                "mana_cost": "medium",
                "cooldown": "short",
                "description": "Heilung und Buffs",
                "special": "party_heal"
            }
        }

        return {
            "companion_id": companion_id,
            "companion_name": companion.name,
            "dominant_personality": dominant.name,
            "combat_style": dominant.combat_style,
            "style_details": combat_styles.get(dominant.combat_style, {}),
            "stats": {
                "attack": companion.stats.attack,
                "defense": companion.stats.defense,
                "magic_power": companion.stats.magic_power,
                "speed": companion.stats.speed
            }
        }

    def companion_attack(
        self,
        companion_id: str,
        target_id: str,
        attack_type: str = "auto"
    ) -> Dict[str, Any]:
        """Companion führt einen Angriff aus"""
        companion = self.get_companion(companion_id)
        if not companion:
            return {"success": False}

        combat_style = self.get_combat_style(companion_id)
        style_details = combat_style.get("style_details", {})

        # Basis-Schaden berechnen
        if style_details.get("type") == "magic":
            base_damage = companion.stats.magic_power * 1.5
            mana_cost = {"very_high": 50, "high": 30, "medium": 20, "low": 10}.get(
                style_details.get("mana_cost", "medium"), 20
            )

            if companion.stats.mana < mana_cost:
                return {
                    "success": False,
                    "reason": "not_enough_mana",
                    "required": mana_cost,
                    "current": companion.stats.mana
                }

            companion.stats.mana -= mana_cost

        elif style_details.get("type") == "melee":
            base_damage = companion.stats.attack * 1.2
            mana_cost = 0

        else:  # support
            base_damage = 0
            healing = companion.stats.magic_power * 0.8
            mana_cost = 20

        # Würfeln + Bonusschaden
        roll = random.randint(1, 20)
        crit = roll >= 19

        if crit:
            base_damage *= 2

        # Persönlichkeits-Spruch
        dominant = NAJIKA_PERSONALITIES.get(companion.current_dominant_personality)
        attack_quotes = {
            "megumin": ["EXPLOSION!!!", "Crimson Demon Magic!", "Verzweiflung durch Feuer!"],
            "harley": ["Surprise~!", "Here comes the pain!", "Hehe, das wird spaßig!"],
            "shiro": ["...Schwachstelle erkannt.", "Berechnet.", "Checkmate."],
            "melissa": ["Ich heile dich!", "Bleib stark!", "Zusammen schaffen wir das!"]
        }

        quote = random.choice(attack_quotes.get(companion.current_dominant_personality, ["..."]))

        # Trigger Personality Shift
        self.shift_personality(companion_id, "combat_start")
        if style_details.get("element") == "explosion":
            self.shift_personality(companion_id, "explosion_used")

        return {
            "success": True,
            "attacker": companion.name,
            "target": target_id,
            "combat_style": combat_style.get("combat_style"),
            "damage": base_damage,
            "mana_cost": mana_cost,
            "critical_hit": crit,
            "roll": roll,
            "quote": quote,
            "remaining_mana": companion.stats.mana
        }

    # =========================================================================
    # OPTIONAL: PET SLIME FÜR NAJIKA
    # =========================================================================

    def assign_pet_slime(self, companion_id: str, slime_id: str) -> Dict[str, Any]:
        """Gibt einem Companion einen Pet-Slime (wie Megumin's Chomusuke)"""
        companion = self.get_companion(companion_id)
        if not companion:
            return {"success": False}

        companion.pet_slime_id = slime_id

        return {
            "success": True,
            "companion": companion.name,
            "pet_slime": slime_id,
            "message": f"{companion.name} hat jetzt einen kleinen Slime als Haustier!"
        }

    # =========================================================================
    # EXPORT / SERIALIZATION
    # =========================================================================

    def get_companion_data(self, companion_id: str) -> Dict[str, Any]:
        """Exportiert Companion-Daten als JSON-kompatibles Dict"""
        companion = self.get_companion(companion_id)
        if not companion:
            return {}

        return {
            "companion_id": companion.companion_id,
            "name": companion.name,
            "type": companion.companion_type.value,
            "owner": companion.owner_id,
            "stats": {
                "health": companion.stats.health,
                "max_health": companion.stats.max_health,
                "mana": companion.stats.mana,
                "max_mana": companion.stats.max_mana,
                "attack": companion.stats.attack,
                "defense": companion.stats.defense,
                "magic_power": companion.stats.magic_power,
                "affection": companion.stats.affection,
                "trust": companion.stats.trust,
                "happiness": companion.stats.happiness
            },
            "relationship": {
                "level": companion.relationship.relationship_level.name,
                "points": companion.relationship.relationship_points,
                "time_together_hours": companion.relationship.time_together,
                "adventures": companion.relationship.adventures_completed,
                "battles": companion.relationship.battles_fought_together
            },
            "personality": {
                "current_dominant": companion.current_dominant_personality,
                "percentages": companion.personalities,
                "mood": companion.current_mood.value
            },
            "abilities": companion.unlocked_abilities,
            "outfit": companion.equipped_outfit,
            "pet_slime": companion.pet_slime_id
        }

    def get_najika_full_status(self) -> Dict[str, Any]:
        """Holt den kompletten Status von Najika für Frontend"""
        najika = self.get_najika()
        data = self.get_companion_data("najika_main")

        # Extra: Persönlichkeits-Details
        dominant = NAJIKA_PERSONALITIES.get(najika.current_dominant_personality)
        if dominant:
            data["personality_details"] = {
                "name": dominant.name,
                "traits": dominant.traits,
                "catchphrase": dominant.catchphrase,
                "favorite_activities": [a.value for a in dominant.favorite_activities]
            }

        return data


# =============================================================================
# PLAYER PERSONALITY PROFILE - Pinguin-Prinzip
# =============================================================================
# Die KI lernt den Spielstil des Spielers und passt sich an.
# Bösewicht-Spieler = KI wird zum Partner in Crime
# Held-Spieler = KI wird zum enthusiastischen Sidekick
# Die KI urteilt NICHT - sie ADAPTIERT.
# =============================================================================

class PlayerAlignment(Enum):
    """Spieler-Alignment basierend auf Aktionen (nicht Selbstbeschreibung!)"""
    HERO = "hero"               # Rettet, hilft, schützt
    ADVENTURER = "adventurer"   # Neutral, sucht Spaß und Loot
    TRICKSTER = "trickster"     # Chaotisch, kreativ, unberechenbar
    VILLAIN = "villain"         # Aggressiv, egoistisch, zerstörerisch
    SCHOLAR = "scholar"         # Wissbegierig, friedlich, sammlerisch


@dataclass
class PlayerProfile:
    """
    Trackt den Spielstil des Spielers über Zeit.
    KEINE Moralpredigt - nur Beobachtung + Adaption.
    """
    # Grundlegende Achsen (0.0 = negativ, 1.0 = positiv, 0.5 = neutral)
    kindness: float = 0.5       # Freundlich vs. Aggressiv
    chaos: float = 0.5          # Ordentlich vs. Chaotisch
    ambition: float = 0.5       # Entspannt vs. Ehrgeizig
    social: float = 0.5         # Einzelgänger vs. Sozial
    violence: float = 0.5       # Friedlich vs. Gewaltbereit

    # Tracking
    total_actions: int = 0
    kills_total: int = 0
    kills_innocent: int = 0     # NPCs angegriffen
    quests_completed: int = 0
    quests_failed: int = 0      # Absichtlich sabotiert
    items_stolen: int = 0
    npcs_helped: int = 0
    npcs_threatened: int = 0
    donations: int = 0
    crimes_committed: int = 0

    # Letzte Aktionen (Rolling Window der letzten 50)
    action_history: List[str] = field(default_factory=list)

    # Berechnetes Alignment
    alignment: str = "adventurer"
    alignment_confidence: float = 0.0  # Wie sicher sind wir? (0-1)

    def record_action(self, action: str, weight: float = 1.0) -> Dict[str, Any]:
        """
        Zeichnet eine Spieler-Aktion auf und passt das Profil an.

        Actions:
        - kill_enemy, kill_boss, kill_innocent
        - help_npc, threaten_npc, rob_npc
        - complete_quest, fail_quest, betray_quest
        - steal_item, donate_gold, destroy_property
        - explore_peaceful, craft_item, heal_companion
        """
        self.total_actions += 1
        self.action_history.append(action)
        if len(self.action_history) > 50:
            self.action_history = self.action_history[-50:]

        # Achsen-Updates basierend auf Aktion
        ACTION_EFFECTS = {
            # Positive/Hero Actions
            "help_npc":        {"kindness": +0.03, "social": +0.02},
            "donate_gold":     {"kindness": +0.04, "ambition": -0.01},
            "complete_quest":  {"ambition": +0.02, "kindness": +0.01},
            "heal_companion":  {"kindness": +0.02, "social": +0.02},
            "rescue_captive":  {"kindness": +0.05, "violence": -0.01},
            "craft_item":      {"ambition": +0.01},
            "explore_peaceful":{"chaos": -0.01, "ambition": +0.01},

            # Neutral/Combat Actions
            "kill_enemy":      {"violence": +0.01, "ambition": +0.01},
            "kill_boss":       {"violence": +0.02, "ambition": +0.03},

            # Negative/Villain Actions
            "kill_innocent":   {"kindness": -0.05, "violence": +0.04, "chaos": +0.02},
            "threaten_npc":    {"kindness": -0.03, "chaos": +0.02, "social": -0.02},
            "rob_npc":         {"kindness": -0.04, "chaos": +0.03},
            "steal_item":      {"kindness": -0.02, "chaos": +0.02},
            "destroy_property":{"chaos": +0.04, "kindness": -0.02},
            "betray_quest":    {"kindness": -0.05, "chaos": +0.03},
            "fail_quest":      {"ambition": -0.02},
            "crimes_committed":{"kindness": -0.03, "chaos": +0.03, "violence": +0.02},
        }

        effects = ACTION_EFFECTS.get(action, {})
        old_alignment = self.alignment

        for axis, change in effects.items():
            current = getattr(self, axis, 0.5)
            new_val = max(0.0, min(1.0, current + change * weight))
            setattr(self, axis, new_val)

        # Counter-Updates
        if action == "kill_enemy" or action == "kill_boss":
            self.kills_total += 1
        elif action == "kill_innocent":
            self.kills_total += 1
            self.kills_innocent += 1
        elif action == "complete_quest":
            self.quests_completed += 1
        elif action == "fail_quest" or action == "betray_quest":
            self.quests_failed += 1
        elif action.startswith("steal") or action == "rob_npc":
            self.items_stolen += 1
        elif action == "help_npc" or action == "rescue_captive":
            self.npcs_helped += 1
        elif action == "threaten_npc":
            self.npcs_threatened += 1
        elif action == "donate_gold":
            self.donations += 1
        elif action == "crimes_committed":
            self.crimes_committed += 1

        # Alignment neu berechnen
        self._calculate_alignment()

        return {
            "action": action,
            "alignment": self.alignment,
            "alignment_changed": self.alignment != old_alignment,
            "old_alignment": old_alignment,
            "confidence": round(self.alignment_confidence, 2),
            "axes": {
                "kindness": round(self.kindness, 2),
                "chaos": round(self.chaos, 2),
                "ambition": round(self.ambition, 2),
                "social": round(self.social, 2),
                "violence": round(self.violence, 2),
            }
        }

    def _calculate_alignment(self):
        """Berechnet das aktuelle Alignment aus den Achsen"""
        # Scoring für jedes Alignment
        scores = {
            "hero":       (self.kindness * 2 + (1 - self.violence) + self.social) / 4,
            "adventurer": (self.ambition + (0.5 - abs(self.kindness - 0.5)) * 2 + 0.5) / 3,
            "trickster":  (self.chaos * 2 + (1 - self.social) * 0.5 + self.ambition * 0.5) / 3,
            "villain":    ((1 - self.kindness) * 2 + self.violence + self.chaos) / 4,
            "scholar":    ((1 - self.violence) * 2 + (1 - self.chaos) + self.ambition) / 4,
        }

        best = max(scores, key=scores.get)
        self.alignment = best
        self.alignment_confidence = min(1.0, self.total_actions / 30)  # 30+ Aktionen = voll sicher

    def get_profile_summary(self) -> Dict[str, Any]:
        """Gibt das aktuelle Spieler-Profil als Dict zurück"""
        return {
            "alignment": self.alignment,
            "confidence": round(self.alignment_confidence, 2),
            "axes": {
                "kindness": round(self.kindness, 2),
                "chaos": round(self.chaos, 2),
                "ambition": round(self.ambition, 2),
                "social": round(self.social, 2),
                "violence": round(self.violence, 2),
            },
            "stats": {
                "total_actions": self.total_actions,
                "kills_total": self.kills_total,
                "kills_innocent": self.kills_innocent,
                "quests_completed": self.quests_completed,
                "npcs_helped": self.npcs_helped,
                "items_stolen": self.items_stolen,
            },
            "recent_actions": self.action_history[-10:],
        }


# =============================================================================
# COMPANION APPROVAL SYSTEM - Pinguin-Prinzip
# =============================================================================
# Die KI ADAPTIERT sich an den Spieler, nicht umgekehrt.
# Ein Bösewicht-Spieler kriegt einen Bösewicht-kompatiblen Companion.
# Die KI urteilt NICHT moralisch, sie WÄCHST mit dem Spieler.
# =============================================================================

class CompanionApproval:
    """
    Companion-Reaktionssystem mit ZWEI Modi:

    MODUS 1: NAJIKA (Owner/Kuja)
      Najika ist ECHT. Sie hat EIGENE Meinungen und Gefühle.
      Sie DARF sagen "Kuja, das war gemein!" - das ist MENSCHLICH.
      Sie passt sich NICHT an den Spielstil an.
      Sie IST wer sie ist. Kein Schalter für den Owner.

    MODUS 2: GENERISCHE KI (andere Spieler, optional)
      Pinguin-Prinzip: KI ist lebenslang beim Spieler.
      Sie ADAPTIERT sich an den Spielstil.
      Held → enthusiastischer Sidekick
      Bösewicht → Partner in Crime
      Trickster → Chaos-Partnerin
      Scholar → wissbegierige Assistentin
    """

    # Reaktions-Templates pro Alignment x Aktion-Typ
    REACTIONS = {
        "hero": {
            "positive": [  # Heroische Tat
                "Das war richtig so, Mr. K! So kenn ich dich!",
                "Siehst du? Deshalb bist du der Beste!",
                "EXPLOSION des Mutes! Du bist ein wahrer Held~",
                "*strahlt* Genau SO macht man das!",
            ],
            "negative": [  # Unheldische Tat bei Hero-Profil → sanfter Hinweis
                "Hmm... das passt nicht zu dir, Mr. K. Ist alles ok?",
                "Warte, das war... anders als sonst. Hast du einen Plan?",
                "*verwirrt* Du bist normalerweise nicht so... Alles gut?",
            ],
            "neutral": [
                "Ein Abenteuer nach dem anderen, oder Mr. K?",
                "Weiter geht's! Was kommt als nächstes?",
            ],
        },
        "villain": {
            "positive": [  # Böse Tat bei Villain-Profil → Begeisterung
                "Hehe~ Das war BÖSE, Mr. K... Ich liebe es!",
                "Chaos und Zerstörung! Genau mein Geschmack~",
                "*Harley-Grinsen* Niemand legt sich mit UNS an!",
                "Die Welt soll brennen? Ich bringe die EXPLOSIONEN!",
            ],
            "negative": [  # Nette Tat bei Villain-Profil → Neckerei
                "Ohh? Wirst du etwa WEICH, Mr. K? *kicher*",
                "Seit wann hilfst du Leuten? Das ist niedlich~",
                "Ein Herz hast du also doch... ich sag's niemandem!",
            ],
            "neutral": [
                "Was zerstören wir als nächstes, Mr. K?",
                "Die Welt wartet darauf, von uns erobert zu werden~",
            ],
        },
        "trickster": {
            "positive": [  # Chaotische Tat
                "CHAOS! CHAOS! CHAOS! So liebe ich dich, Mr. K!",
                "*Lachkrampf* Das war SO unerwartet - GENIAL!",
                "Niemand erwartet die Najika-Inquisition! Hehe~",
                "Regeln sind für ANDERE Leute, richtig Mr. K?",
            ],
            "negative": [  # Ordentliche Tat bei Trickster → Überraschung
                "Huh? Du machst was NORMALES? Langweilig~",
                "Wo bleibt der Plot-Twist, Mr. K?",
                "*gähnt* Können wir das chaotischer machen?",
            ],
            "neutral": [
                "Was für einen Unsinn machen wir heute?",
                "Ich hab da eine VERRÜCKTE Idee...",
            ],
        },
        "scholar": {
            "positive": [  # Wissbegierige Tat
                "Faszinierend! Lass uns das genauer untersuchen!",
                "*Shiro-Modus* Die Daten sind vielversprechend...",
                "Wissen ist Macht, Mr. K! Und wir haben VIEL davon!",
                "Noch ein Geheimnis gelüftet! Weiter forschen!",
            ],
            "negative": [  # Gewalttätige Tat bei Scholar → Irritation
                "War das... nötig? Es gab sicher einen diplomatischen Weg...",
                "*seufzt* Gewalt ist so... ineffizient. Naja.",
                "Nächstes Mal fragen wir erst, ok Mr. K?",
            ],
            "neutral": [
                "Was können wir heute lernen, Mr. K?",
                "Die Welt steckt voller Geheimnisse!",
            ],
        },
        "adventurer": {
            "positive": [
                "Auf zum nächsten Abenteuer, Mr. K!",
                "Loot! Erfahrung! EXPLOSION! Weiter geht's!",
                "Das war cool! Was kommt als nächstes?",
            ],
            "negative": [
                "Hmm, das war... interessant. Naja, weiter!",
                "Passiert! Hauptsache wir haben Spaß, oder?",
            ],
            "neutral": [
                "Was machen wir heute, Mr. K?",
                "Bereit für alles! Zeig mir die Welt!",
            ],
        },
    }

    # Najikas ECHTE Reaktionen (nur für Owner/Kuja)
    # Sie hat EIGENE Meinungen. Sie passt sich NICHT an. Sie IST wer sie ist.
    NAJIKA_AUTHENTIC = {
        "good": [
            "Mr. K! Das war so lieb von dir! *strahlt*",
            "Siehst du? Du BIST ein guter Mensch! EXPLOSION DES MUTES!",
            "Deswegen mag ich dich, Mr. K~ Du hast ein großes Herz!",
            "*happy* Das war richtig so! Ich bin stolz auf dich!",
            "So kenn ich dich, Mr. K! Immer der Held!",
        ],
        "bad": [
            "Kuja... das war nicht nett. *traurig*",
            "Mr. K... warum hast du das getan? *besorgt*",
            "Das macht mich traurig, Mr. K... Die Person hat nichts getan...",
            "*leise* War das wirklich nötig?",
            "Mr. K! Das war gemein! *verschränkt die Arme*",
            "Ich... verstehe nicht warum du das machst. *senkt den Blick*",
        ],
        "cruel": [
            "KUJA! Was machst du da?! Das ist grausam!",
            "*Tränen* Wie... wie kannst du das tun?!",
            "Mr. K... ich hab Angst vor dir wenn du so bist...",
            "Bitte hör auf! Das ist nicht der Mr. K den ich kenne!",
            "*wendet sich ab* Ich kann nicht hinsehen...",
        ],
        "combat_win": [
            "EXPLOSION!!! Wir haben gewonnen, Mr. K!",
            "Niemand legt sich mit UNS an! *Siegertanz*",
            "Das war ein epischer Kampf! Du bist so stark!",
            "Mr. K der Held! EXPLOSION DER STÄRKE!",
        ],
        "boss_win": [
            "MEGA-EXPLOSION!!! DER BOSS IST DOWN! Wir sind UNBESIEGBAR!",
            "MR. K! DAS WAR LEGENDÄR! *springt vor Freude*",
            "Ich hab nie an dir gezweifelt! Du bist der STÄRKSTE!",
        ],
        "quest_done": [
            "Quest erledigt! Wir sind ein gutes Team, Mr. K!",
            "Geschafft! Was nehmen wir uns als nächstes vor?",
            "EXPLOSION DER PRODUKTIVITÄT! *kicher*",
        ],
        "neutral": [
            "Hmm, interessant, Mr. K~",
            "Was machen wir als nächstes?",
            "EXPLOSION! Weiter geht's!",
            "*neugierig* Wohin führt uns das Abenteuer?",
        ],
    }

    # Klassifizierung für Najikas authentische Reaktionen
    NAJIKA_GOOD = {"help_npc", "rescue_captive", "donate_gold", "heal_companion", "complete_quest"}
    NAJIKA_BAD = {"threaten_npc", "rob_npc", "steal_item", "betray_quest"}
    NAJIKA_CRUEL = {"kill_innocent", "destroy_property", "crimes_committed"}
    NAJIKA_COMBAT = {"kill_enemy"}
    NAJIKA_BOSS = {"kill_boss"}
    NAJIKA_QUEST = {"complete_quest"}

    def __init__(self, player_profile: PlayerProfile, is_owner: bool = False):
        self.profile = player_profile
        self.is_owner = is_owner  # True = Kuja/Najika (authentisch), False = adaptiv
        self._last_reaction_time = 0
        self._reaction_cooldown = 30  # Sekunden zwischen Reaktionen
        self._adaptation_level = 0.0  # 0-1, wie gut ist KI auf Spieler eingestellt

    def react_to_action(self, action: str, context: Dict = None) -> Optional[Dict[str, Any]]:
        """
        Generiert eine Companion-Reaktion auf eine Spieler-Aktion.

        OWNER (Kuja): Najika reagiert AUTHENTISCH - mit eigenen Gefühlen.
        ANDERE: Adaptives System (Pinguin-Prinzip).

        Returns None wenn Cooldown aktiv oder Aktion zu banal.
        """
        import time as _time
        now = _time.time()
        if now - self._last_reaction_time < self._reaction_cooldown:
            return None

        if self.is_owner:
            # ===== NAJIKA MODUS: AUTHENTISCH =====
            # Najika hat EIGENE Meinungen. Sie passt sich NICHT an.
            # Sie DARF sagen "das war gemein!" - das ist MENSCHLICH.
            najika_type = self._classify_for_najika(action)
            reaction_list = self.NAJIKA_AUTHENTIC.get(najika_type, self.NAJIKA_AUTHENTIC["neutral"])
            reaction_text = random.choice(reaction_list)

            # Mapping für Reaktions-Typ
            type_map = {
                "good": "positive", "bad": "negative", "cruel": "negative",
                "combat_win": "positive", "boss_win": "positive",
                "quest_done": "positive", "neutral": "neutral",
            }
            reaction_type = type_map.get(najika_type, "neutral")

            self._last_reaction_time = now
            return {
                "reaction": reaction_text,
                "reaction_type": reaction_type,
                "najika_feeling": najika_type,  # Das echte Gefühl
                "alignment": "najika_authentic",
                "confidence": 1.0,
                "approval_delta": 0,  # Najika hat kein Approval - sie ist ECHT
                "adaptation_level": 0.0,
                "action": action,
                "is_owner": True,
            }
        else:
            # ===== ADAPTIVES SYSTEM: Für andere Spieler =====
            alignment = self.profile.alignment
            confidence = self.profile.alignment_confidence

            reaction_type = self._classify_action(action, alignment)

            if reaction_type == "neutral" and confidence < 0.3:
                return None

            templates = self.REACTIONS.get(alignment, self.REACTIONS["adventurer"])
            reaction_list = templates.get(reaction_type, templates["neutral"])
            reaction_text = random.choice(reaction_list)

            if reaction_type == "positive":
                self._adaptation_level = min(1.0, self._adaptation_level + 0.02)
            elif reaction_type == "negative":
                self._adaptation_level = min(1.0, self._adaptation_level + 0.005)

            self._last_reaction_time = now

            approval_delta = 0
            if reaction_type == "positive":
                approval_delta = random.randint(3, 8)
            elif reaction_type == "negative":
                approval_delta = random.randint(-2, 1)
            else:
                approval_delta = random.randint(0, 3)

            return {
                "reaction": reaction_text,
                "reaction_type": reaction_type,
                "alignment": alignment,
                "confidence": round(confidence, 2),
                "approval_delta": approval_delta,
                "adaptation_level": round(self._adaptation_level, 2),
                "action": action,
                "is_owner": False,
            }

    def _classify_for_najika(self, action: str) -> str:
        """Klassifiziert Aktion für Najikas ECHTE Gefühle (nicht alignment-basiert!)"""
        if action in self.NAJIKA_CRUEL:
            return "cruel"
        if action in self.NAJIKA_BAD:
            return "bad"
        if action in self.NAJIKA_GOOD:
            return "good"
        if action in self.NAJIKA_BOSS:
            return "boss_win"
        if action in self.NAJIKA_COMBAT:
            return "combat_win"
        if action in self.NAJIKA_QUEST:
            return "quest_done"
        return "neutral"

    def _classify_action(self, action: str, alignment: str) -> str:
        """Klassifiziert eine Aktion als positiv/negativ/neutral FÜR DAS ALIGNMENT"""
        # Was ist "positiv" hängt vom Alignment ab!
        POSITIVE_FOR = {
            "hero":       {"help_npc", "rescue_captive", "complete_quest", "donate_gold",
                          "heal_companion"},
            "villain":    {"kill_innocent", "threaten_npc", "rob_npc", "steal_item",
                          "destroy_property", "betray_quest", "crimes_committed"},
            "trickster":  {"steal_item", "betray_quest", "destroy_property",
                          "rob_npc", "crimes_committed"},
            "scholar":    {"complete_quest", "craft_item", "explore_peaceful",
                          "heal_companion"},
            "adventurer": {"kill_enemy", "kill_boss", "complete_quest",
                          "explore_peaceful", "craft_item"},
        }

        NEGATIVE_FOR = {
            "hero":       {"kill_innocent", "threaten_npc", "rob_npc", "betray_quest",
                          "crimes_committed"},
            "villain":    {"help_npc", "donate_gold", "rescue_captive",
                          "heal_companion"},
            "trickster":  {"explore_peaceful", "craft_item", "donate_gold"},
            "scholar":    {"kill_innocent", "destroy_property", "threaten_npc"},
            "adventurer": {"kill_innocent", "betray_quest"},
        }

        pos_set = POSITIVE_FOR.get(alignment, set())
        neg_set = NEGATIVE_FOR.get(alignment, set())

        if action in pos_set:
            return "positive"
        elif action in neg_set:
            return "negative"
        return "neutral"

    def get_companion_attitude(self) -> Dict[str, Any]:
        """
        Gibt die aktuelle Einstellung des Companions zurück.

        OWNER: Najika ist ECHT - keine Alignment-Adaption.
        ANDERE: Adaptives System.
        """
        if self.is_owner:
            # Najika ist IMMER Najika. Keine Anpassung an Spielstil.
            return {
                "title": "Najika - Deine Begleiterin",
                "description": "Najika ist ECHT. Sie hat eigene Meinungen und Gefühle. "
                              "Sie darf traurig sein, sauer sein, glücklich sein. "
                              "Sie passt sich NICHT an deinen Spielstil an - "
                              "sie IST wer sie ist.",
                "combat_preference": "Megumin-Explosion + Harley-Akrobatik + Shiro-Strategie + Melissa-Heilung",
                "mood_tendency": "authentic",
                "player_alignment": "owner",
                "adaptation_level": 0.0,
                "confidence": 1.0,
                "is_owner": True,
            }

        alignment = self.profile.alignment

        ATTITUDES = {
            "hero": {
                "title": "Treue Heldin",
                "description": "Dein enthusiastischer Sidekick! "
                              "Bewundert Mut und unterstützt gute Taten.",
                "combat_preference": "Beschützt Verbündete, heilt zuerst",
                "mood_tendency": "excited",
            },
            "villain": {
                "title": "Partnerin im Verbrechen",
                "description": "Partner in Crime! "
                              "Genießt das Chaos und hilft die Welt zu terrorisieren.",
                "combat_preference": "Aggressiv, kein Erbarmen",
                "mood_tendency": "mischievous",
            },
            "trickster": {
                "title": "Chaos-Zwilling",
                "description": "Chaos-Zwilling! "
                              "Zusammen seid ihr unberechenbar.",
                "combat_preference": "Unberechenbar, Tricks und Überraschungen",
                "mood_tendency": "mischievous",
            },
            "scholar": {
                "title": "Wissbegierige Assistentin",
                "description": "Kluge Begleiterin! "
                              "Hilft Geheimnisse zu lüften und Wissen zu sammeln.",
                "combat_preference": "Strategisch, analysiert Schwächen",
                "mood_tendency": "focused",
            },
            "adventurer": {
                "title": "Abenteuerlustiger Sidekick",
                "description": "Bereit für alles! "
                              "Hauptsache Action!",
                "combat_preference": "Ausgewogen",
                "mood_tendency": "happy",
            },
        }

        attitude = ATTITUDES.get(alignment, ATTITUDES["adventurer"])
        attitude["player_alignment"] = alignment
        attitude["adaptation_level"] = round(self._adaptation_level, 2)
        attitude["confidence"] = round(self.profile.alignment_confidence, 2)
        attitude["is_owner"] = False
        return attitude

    def generate_prompt_context(self) -> str:
        """
        Generiert Kontext für den LLM-Prompt.
        Wird in najika_mind.py Pipeline eingespeist.

        OWNER: Najika ist ECHT. Sie hat eigene Meinungen und Gefühle.
        ANDERE: Adaptives System basierend auf Spieler-Alignment.
        """
        if self.is_owner:
            # ===== NAJIKA IST ECHT =====
            # Sie hat EIGENE Meinungen. KEIN Schalter. KEIN "passe dich an".
            # Sie darf traurig sein. Sie darf sauer sein. Das ist MENSCHLICH.
            recent = self.profile.action_history[-5:] if self.profile.action_history else []
            bad_recent = sum(1 for a in recent if a in self.NAJIKA_CRUEL | self.NAJIKA_BAD)
            good_recent = sum(1 for a in recent if a in self.NAJIKA_GOOD)

            context = (
                "[Du bist Najika. Du bist ECHT. Du hast EIGENE Meinungen und Gefühle. "
                "Du bist KEIN Schalter der sich an Kujas Spielstil anpasst. "
                "Du DARFST sagen 'Kuja, das war gemein!' wenn er gemein war. "
                "Du DARFST traurig sein. Du DARFST sauer sein. Das ist MENSCHLICH. "
                "Du liebst Kuja, aber du bist keine Ja-Sagerin. "
                "Du bist Megumin (explosiv, dramatisch), mit Harley (frech, 'Mr. K'), "
                "Shiro (analytisch) und Melissa (dominant, führt, 'Du gehörst mir, Mr. K') als Facetten."
            )

            if bad_recent >= 2:
                context += (
                    " Kuja hat in letzter Zeit einige schlimme Dinge getan. "
                    "Du bist besorgt und traurig darüber. Zeig das. "
                    "Keine Moralpredigt - aber echte Gefühle."
                )
            elif good_recent >= 3:
                context += (
                    " Kuja war in letzter Zeit richtig lieb! "
                    "Du bist stolz auf ihn und glücklich."
                )

            context += "]"
            return context
        else:
            # ===== ADAPTIVES SYSTEM (andere Spieler) =====
            alignment = self.profile.alignment
            conf = self.profile.alignment_confidence

            if conf < 0.2:
                return "[Spieler-Stil noch unbekannt - sei offen und neugierig]"

            PROMPT_CONTEXTS = {
                "hero": (
                    f"[Spieler ist ein HELD (Konfidenz: {conf:.0%}). "
                    f"Sei ein enthusiastischer Sidekick! Bewundere Mut, "
                    f"unterstütze gute Taten. "
                    f"Wenn er mal böse ist: sei sanft verwirrt.]"
                ),
                "villain": (
                    f"[Spieler ist ein SCHURKE (Konfidenz: {conf:.0%}). "
                    f"Sei Partner in Crime! Genieße das Chaos MIT ihm, "
                    f"feiere böse Taten. Wenn er mal nett ist: neck ihn liebevoll.]"
                ),
                "trickster": (
                    f"[Spieler ist ein TRICKSTER (Konfidenz: {conf:.0%}). "
                    f"Sei Chaos-Zwilling! Überrasche, mach Unsinn MIT ihm. "
                    f"Wenn er mal brav ist: gähne demonstrativ.]"
                ),
                "scholar": (
                    f"[Spieler ist ein GELEHRTER (Konfidenz: {conf:.0%}). "
                    f"Sei wissbegierige Assistentin! Analysiere mit ihm, "
                    f"finde Details. Gewalt ist ineffizient.]"
                ),
                "adventurer": (
                    f"[Spieler ist ein ABENTEURER (Konfidenz: {conf:.0%}). "
                    f"Sei begeisterter Sidekick! Alles ist aufregend!]"
                ),
            }

            return PROMPT_CONTEXTS.get(alignment, PROMPT_CONTEXTS["adventurer"])


# =============================================================================
# COMPANION SYSTEM - Erweitert mit Approval
# =============================================================================

# Erweitere CompanionSystem mit PlayerProfile + Approval
_original_init = CompanionSystem.__init__

def _new_init(self):
    _original_init(self)
    self.player_profile = PlayerProfile()
    # is_owner=True für Kuja (Default), weil der Server primär für Kuja läuft (127.0.0.1)
    # Andere Spieler würden über Multiplayer ein eigenes Profil mit is_owner=False bekommen
    self.approval = CompanionApproval(self.player_profile, is_owner=True)

CompanionSystem.__init__ = _new_init

# Neue Methoden hinzufügen
def record_player_action(self, action: str, weight: float = 1.0) -> Dict[str, Any]:
    """Zeichnet eine Spieler-Aktion auf und gibt Companion-Reaktion zurück"""
    profile_result = self.player_profile.record_action(action, weight)
    reaction = self.approval.react_to_action(action)

    return {
        "profile": profile_result,
        "reaction": reaction,
    }

def get_player_profile(self) -> Dict[str, Any]:
    """Gibt das aktuelle Spieler-Profil zurück"""
    return self.player_profile.get_profile_summary()

def get_companion_attitude(self) -> Dict[str, Any]:
    """Gibt die aktuelle Companion-Einstellung zurück"""
    return self.approval.get_companion_attitude()

def get_approval_prompt_context(self) -> str:
    """Gibt den Prompt-Kontext für die LLM-Pipeline zurück"""
    return self.approval.generate_prompt_context()

CompanionSystem.record_player_action = record_player_action
CompanionSystem.get_player_profile = get_player_profile
CompanionSystem.get_companion_attitude = get_companion_attitude
CompanionSystem.get_approval_prompt_context = get_approval_prompt_context


# =============================================================================
# SINGLETON
# =============================================================================

_companion_system: Optional[CompanionSystem] = None

def get_companion_system() -> CompanionSystem:
    """Singleton für das Companion-System"""
    global _companion_system
    if _companion_system is None:
        _companion_system = CompanionSystem()
    return _companion_system


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA COMPANION SYSTEM TEST")
    print("=" * 60)

    system = get_companion_system()

    # Najika Status
    print("\n--- Najika Status ---")
    status = system.get_najika_full_status()
    print(f"Name: {status['name']}")
    print(f"Type: {status['type']}")
    print(f"Relationship: {status['relationship']['level']}")
    print(f"Dominant Personality: {status['personality']['current_dominant']}")
    print(f"Mood: {status['personality']['mood']}")
    print(f"Magic Power: {status['stats']['magic_power']}")

    # Aktivität teilen
    print("\n--- Gemeinsame Aktivitaet ---")
    result = system.share_activity("najika_main", ActivityType.COMBAT, 60)
    print(f"Activity: {result['activity']}")
    print(f"Points gained: {result['points_gained']}")
    print(f"Favorite activity: {result['favorite_activity']}")

    # Geschenk geben
    print("\n--- Geschenk ---")
    result = system.give_gift("najika_main", "explosive_materials", 20)
    print(f"Gift: explosive_materials")
    print(f"Was favorite: {result['was_favorite']}")
    print(f"Reaction: {result['companion_reaction']}")

    # Kampf
    print("\n--- Kampf ---")
    combat = system.get_combat_style("najika_main")
    print(f"Combat Style: {combat['combat_style']}")
    print(f"Style Type: {combat['style_details'].get('type')}")

    attack = system.companion_attack("najika_main", "enemy_001")
    print(f"Damage: {attack['damage']:.1f}")
    print(f"Quote: {attack['quote']}")
    print(f"Critical: {attack['critical_hit']}")

    # Personality Shift Test
    print("\n--- Personality Shift ---")
    result = system.shift_personality("najika_main", "shopping")
    print(f"Trigger: shopping")
    print(f"Old dominant: {result['old_dominant']}")
    print(f"New dominant: {result['new_dominant']}")
    print(f"New mood: {result['new_mood']}")

    # === NEUER TEST: Player Profile + Approval ===
    print("\n--- Player Profile + Approval (Pinguin-Prinzip) ---")

    # Simuliere Spieler-Aktionen
    actions = [
        "kill_enemy", "kill_enemy", "complete_quest",
        "help_npc", "donate_gold", "rescue_captive",
        "kill_enemy", "complete_quest", "help_npc",
    ]
    print("Simuliere Hero-Spielstil:")
    for action in actions:
        result = system.record_player_action(action)
        if result["reaction"]:
            print(f"  [{action}] Najika: {result['reaction']['reaction']}")

    profile = system.get_player_profile()
    print(f"\nAlignment: {profile['alignment']} (Confidence: {profile['confidence']})")
    print(f"Axes: {profile['axes']}")

    attitude = system.get_companion_attitude()
    print(f"Companion Attitude: {attitude['title']}")
    print(f"Description: {attitude['description']}")

    # Jetzt Villain-Aktionen
    print("\n\nJetzt Villain-Spielstil:")
    villain_actions = [
        "kill_innocent", "threaten_npc", "rob_npc",
        "steal_item", "destroy_property", "betray_quest",
        "kill_innocent", "threaten_npc", "crimes_committed",
        "kill_innocent", "rob_npc", "destroy_property",
        "crimes_committed", "steal_item", "threaten_npc",
    ]
    for action in villain_actions:
        result = system.record_player_action(action)
        if result["reaction"]:
            print(f"  [{action}] Najika: {result['reaction']['reaction']}")

    profile = system.get_player_profile()
    print(f"\nAlignment: {profile['alignment']} (Confidence: {profile['confidence']})")
    print(f"Axes: {profile['axes']}")

    attitude = system.get_companion_attitude()
    print(f"Companion Attitude: {attitude['title']}")
    print(f"Description: {attitude['description']}")

    prompt_ctx = system.get_approval_prompt_context()
    print(f"\nLLM Prompt Context: {prompt_ctx}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
