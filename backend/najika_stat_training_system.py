"""
NAJIKA STAT TRAINING SYSTEM
============================
Stats steigen durch TÄTIGKEIT, nicht durch Level-Up-Punkte!

DESIGN PHILOSOPHIE (wie echtes Leben):
- Du wirst stärker indem du schwere Dinge trägst
- Du wirst schlauer indem du lernst
- Du wirst geschickter indem du übst
- KEIN Punkte-Verteilen bei Level-Up!

INSPIRIERT VON:
- Skyrim: Learning by Doing
- Kingdom Come Deliverance: Realistische Progression
- Digimon World: Training erhöht spezifische Stats
- Konosuba: Skill-Punkte für Skills, nicht Stats

FEATURES:
- Aktivitäten erhöhen spezifische Stats
- Diminishing Returns (höher = schwerer zu steigern)
- Tägliches Training-Limit (realistisch)
- Waffen-Skalierung (A-E Ranking)
- Combo-Boni (mehrere Stats gleichzeitig)

Author: Claude Code Team
Date: 2026-02-02
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any, Callable
import random
import math
from datetime import datetime, timedelta
import json


# =============================================================================
# ENUMS
# =============================================================================

class StatType(Enum):
    """Die 7 Basis-Stats (Fallout SPECIAL erweitert)"""
    STRENGTH = "strength"           # Körperkraft
    ENDURANCE = "endurance"         # Ausdauer
    AGILITY = "agility"             # Geschicklichkeit
    INTELLIGENCE = "intelligence"   # Intelligenz
    PERCEPTION = "perception"       # Wahrnehmung
    CHARISMA = "charisma"           # Charisma
    LUCK = "luck"                   # Glück (NICHT normal trainierbar!)


class ActivityCategory(Enum):
    """Kategorien von Aktivitäten"""
    COMBAT = "combat"               # Kämpfen
    LABOR = "labor"                 # Körperliche Arbeit
    CRAFTING = "crafting"           # Handwerk
    MAGIC = "magic"                 # Zaubern
    SOCIAL = "social"               # Soziale Interaktion
    EXPLORATION = "exploration"     # Erkunden
    TRAINING = "training"           # Gezieltes Training
    STUDY = "study"                 # Lernen/Studieren


class ScalingGrade(Enum):
    """Waffen-Skalierung mit Stats (Dark Souls Style)"""
    S = "S"   # 140% Bonus
    A = "A"   # 100% Bonus
    B = "B"   # 75% Bonus
    C = "C"   # 50% Bonus
    D = "D"   # 25% Bonus
    E = "E"   # 10% Bonus
    NONE = "-"  # Kein Bonus


# Skalierungs-Multiplikatoren
SCALING_MULTIPLIERS = {
    ScalingGrade.S: 1.4,
    ScalingGrade.A: 1.0,
    ScalingGrade.B: 0.75,
    ScalingGrade.C: 0.5,
    ScalingGrade.D: 0.25,
    ScalingGrade.E: 0.1,
    ScalingGrade.NONE: 0.0,
}


# =============================================================================
# AKTIVITÄTEN DIE STATS ERHÖHEN
# =============================================================================

@dataclass
class Activity:
    """Eine Aktivität die Stats erhöht"""
    activity_id: str
    name: str
    name_de: str
    description_de: str
    category: ActivityCategory

    # Welche Stats werden erhöht? (stat -> base_xp)
    stat_gains: Dict[StatType, int]

    # Anforderungen
    min_stat_requirements: Dict[StatType, int] = field(default_factory=dict)

    # Kosten
    stamina_cost: int = 0
    mana_cost: int = 0
    time_minutes: int = 10  # Wie lange dauert es?

    # Wiederholbar?
    daily_limit: int = 0  # 0 = unbegrenzt
    cooldown_minutes: int = 0


# Aktivitäten-Datenbank
ACTIVITIES_DB: Dict[str, Activity] = {
    # =====================================================
    # STÄRKE-TRAINING
    # =====================================================
    "chop_wood": Activity(
        "chop_wood", "Chop Wood", "Holz hacken",
        "Bäume fällen und Holz hacken. Gut für die Muskeln!",
        ActivityCategory.LABOR,
        stat_gains={StatType.STRENGTH: 15, StatType.ENDURANCE: 5},
        stamina_cost=30, time_minutes=30
    ),
    "carry_heavy": Activity(
        "carry_heavy", "Carry Heavy Load", "Schwere Last tragen",
        "Schwere Gegenstände von A nach B tragen.",
        ActivityCategory.LABOR,
        stat_gains={StatType.STRENGTH: 20, StatType.ENDURANCE: 10},
        stamina_cost=40, time_minutes=20
    ),
    "mining": Activity(
        "mining", "Mining", "Bergbau",
        "Erze und Mineralien aus dem Felsen schlagen.",
        ActivityCategory.LABOR,
        stat_gains={StatType.STRENGTH: 25, StatType.ENDURANCE: 15, StatType.PERCEPTION: 5},
        stamina_cost=50, time_minutes=60, daily_limit=3
    ),
    "smithing_hammer": Activity(
        "smithing_hammer", "Hammer at Anvil", "Am Amboss hämmern",
        "Metall in Form hämmern. Schwere Arbeit!",
        ActivityCategory.CRAFTING,
        stat_gains={StatType.STRENGTH: 20, StatType.AGILITY: 5},
        stamina_cost=35, time_minutes=45
    ),
    "push_ups": Activity(
        "push_ups", "Push-Ups", "Liegestütze",
        "Klassisches Krafttraining.",
        ActivityCategory.TRAINING,
        stat_gains={StatType.STRENGTH: 10, StatType.ENDURANCE: 5},
        stamina_cost=20, time_minutes=10, cooldown_minutes=30
    ),
    "wrestling": Activity(
        "wrestling", "Wrestling", "Ringen",
        "Nahkampf-Training ohne Waffen.",
        ActivityCategory.COMBAT,
        stat_gains={StatType.STRENGTH: 15, StatType.AGILITY: 10, StatType.ENDURANCE: 10},
        stamina_cost=40, time_minutes=30
    ),

    # =====================================================
    # AUSDAUER-TRAINING
    # =====================================================
    "running": Activity(
        "running", "Running", "Laufen",
        "Ausdauerlauf durch die Gegend.",
        ActivityCategory.TRAINING,
        stat_gains={StatType.ENDURANCE: 20, StatType.AGILITY: 5},
        stamina_cost=30, time_minutes=30
    ),
    "swimming": Activity(
        "swimming", "Swimming", "Schwimmen",
        "Schwimmen trainiert den ganzen Körper.",
        ActivityCategory.TRAINING,
        stat_gains={StatType.ENDURANCE: 25, StatType.STRENGTH: 10, StatType.AGILITY: 5},
        stamina_cost=35, time_minutes=30
    ),
    "climbing": Activity(
        "climbing", "Climbing", "Klettern",
        "Klippen und Wände erklimmen.",
        ActivityCategory.EXPLORATION,
        stat_gains={StatType.ENDURANCE: 15, StatType.STRENGTH: 15, StatType.AGILITY: 10},
        stamina_cost=40, time_minutes=20,
        min_stat_requirements={StatType.STRENGTH: 5}
    ),
    "sparring_long": Activity(
        "sparring_long", "Extended Sparring", "Langes Sparring",
        "Ausgedehnter Trainingskampf ohne Pause.",
        ActivityCategory.COMBAT,
        stat_gains={StatType.ENDURANCE: 30, StatType.STRENGTH: 5, StatType.AGILITY: 5},
        stamina_cost=60, time_minutes=60, daily_limit=2
    ),

    # =====================================================
    # GESCHICKLICHKEIT-TRAINING
    # =====================================================
    "archery_practice": Activity(
        "archery_practice", "Archery Practice", "Bogenschießen üben",
        "Zielübungen mit dem Bogen.",
        ActivityCategory.TRAINING,
        stat_gains={StatType.AGILITY: 20, StatType.PERCEPTION: 10},
        stamina_cost=15, time_minutes=30
    ),
    "lockpicking_practice": Activity(
        "lockpicking_practice", "Lockpicking Practice", "Schlösser knacken üben",
        "An Übungsschlössern die Feinmotorik trainieren.",
        ActivityCategory.TRAINING,
        stat_gains={StatType.AGILITY: 25, StatType.PERCEPTION: 5, StatType.INTELLIGENCE: 5},
        stamina_cost=5, time_minutes=20
    ),
    "knife_juggling": Activity(
        "knife_juggling", "Knife Juggling", "Messer jonglieren",
        "Gefährlich aber effektiv für die Reflexe!",
        ActivityCategory.TRAINING,
        stat_gains={StatType.AGILITY: 30, StatType.PERCEPTION: 10},
        stamina_cost=10, time_minutes=15,
        min_stat_requirements={StatType.AGILITY: 8}
    ),
    "alchemy_brewing": Activity(
        "alchemy_brewing", "Alchemy Brewing", "Tränke brauen",
        "Präzises Mischen von Zutaten.",
        ActivityCategory.CRAFTING,
        stat_gains={StatType.AGILITY: 10, StatType.INTELLIGENCE: 15},
        mana_cost=10, time_minutes=30
    ),
    "sewing": Activity(
        "sewing", "Sewing", "Nähen",
        "Feine Handarbeit für Kleidung und Ausrüstung.",
        ActivityCategory.CRAFTING,
        stat_gains={StatType.AGILITY: 15, StatType.PERCEPTION: 5},
        stamina_cost=5, time_minutes=30
    ),
    "dual_wield_practice": Activity(
        "dual_wield_practice", "Dual Wield Practice", "Beidhändig kämpfen üben",
        "Mit beiden Händen gleichzeitig angreifen.",
        ActivityCategory.COMBAT,
        stat_gains={StatType.AGILITY: 25, StatType.STRENGTH: 5},
        stamina_cost=30, time_minutes=30,
        min_stat_requirements={StatType.AGILITY: 6}
    ),

    # =====================================================
    # INTELLIGENZ-TRAINING
    # =====================================================
    "read_books": Activity(
        "read_books", "Read Books", "Bücher lesen",
        "Wissen aus Büchern aufnehmen.",
        ActivityCategory.STUDY,
        stat_gains={StatType.INTELLIGENCE: 25},
        time_minutes=60
    ),
    "solve_puzzles": Activity(
        "solve_puzzles", "Solve Puzzles", "Rätsel lösen",
        "Das Gehirn mit kniffligen Rätseln trainieren.",
        ActivityCategory.STUDY,
        stat_gains={StatType.INTELLIGENCE: 20, StatType.PERCEPTION: 5},
        time_minutes=30
    ),
    "magic_theory": Activity(
        "magic_theory", "Study Magic Theory", "Magietheorie studieren",
        "Die Grundlagen der Magie verstehen.",
        ActivityCategory.STUDY,
        stat_gains={StatType.INTELLIGENCE: 30, StatType.PERCEPTION: 5},
        mana_cost=5, time_minutes=45
    ),
    "enchanting_study": Activity(
        "enchanting_study", "Study Enchanting", "Verzauberung studieren",
        "Die Kunst der magischen Verbesserung erlernen.",
        ActivityCategory.STUDY,
        stat_gains={StatType.INTELLIGENCE: 25, StatType.AGILITY: 5},
        mana_cost=15, time_minutes=60,
        min_stat_requirements={StatType.INTELLIGENCE: 8}
    ),
    "meditation_focus": Activity(
        "meditation_focus", "Focused Meditation", "Fokussierte Meditation",
        "Den Geist schärfen durch tiefe Konzentration.",
        ActivityCategory.TRAINING,
        stat_gains={StatType.INTELLIGENCE: 15, StatType.PERCEPTION: 10},
        mana_cost=10, time_minutes=30
    ),
    "spell_practice": Activity(
        "spell_practice", "Spell Practice", "Zauber üben",
        "Wiederholtes Zaubern um die Kontrolle zu verbessern.",
        ActivityCategory.MAGIC,
        stat_gains={StatType.INTELLIGENCE: 20, StatType.AGILITY: 5},
        mana_cost=30, time_minutes=30
    ),

    # =====================================================
    # WAHRNEHMUNG-TRAINING
    # =====================================================
    "tracking": Activity(
        "tracking", "Tracking", "Fährten lesen",
        "Spuren von Tieren und Menschen verfolgen.",
        ActivityCategory.EXPLORATION,
        stat_gains={StatType.PERCEPTION: 25, StatType.INTELLIGENCE: 5},
        stamina_cost=10, time_minutes=45
    ),
    "scouting": Activity(
        "scouting", "Scouting", "Spähen",
        "Die Umgebung erkunden und Gefahren erkennen.",
        ActivityCategory.EXPLORATION,
        stat_gains={StatType.PERCEPTION: 20, StatType.AGILITY: 10},
        stamina_cost=15, time_minutes=30
    ),
    "trap_detection": Activity(
        "trap_detection", "Trap Detection Practice", "Fallen suchen üben",
        "Versteckte Fallen in Übungsräumen finden.",
        ActivityCategory.TRAINING,
        stat_gains={StatType.PERCEPTION: 30, StatType.INTELLIGENCE: 5},
        stamina_cost=10, time_minutes=30
    ),
    "stargazing": Activity(
        "stargazing", "Stargazing", "Sterne beobachten",
        "Den Nachthimmel studieren und Muster erkennen.",
        ActivityCategory.STUDY,
        stat_gains={StatType.PERCEPTION: 15, StatType.INTELLIGENCE: 10},
        time_minutes=60
    ),
    "hunting": Activity(
        "hunting", "Hunting", "Jagen",
        "Beute aufspüren und erlegen.",
        ActivityCategory.EXPLORATION,
        stat_gains={StatType.PERCEPTION: 20, StatType.AGILITY: 10, StatType.ENDURANCE: 5},
        stamina_cost=30, time_minutes=90
    ),

    # =====================================================
    # CHARISMA-TRAINING
    # =====================================================
    "haggling": Activity(
        "haggling", "Haggling", "Feilschen",
        "Mit Händlern um Preise verhandeln.",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.CHARISMA: 20, StatType.INTELLIGENCE: 5},
        time_minutes=15
    ),
    "storytelling": Activity(
        "storytelling", "Storytelling", "Geschichten erzählen",
        "Publikum mit Erzählungen fesseln.",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.CHARISMA: 25, StatType.INTELLIGENCE: 5},
        time_minutes=30
    ),
    "perform_music": Activity(
        "perform_music", "Perform Music", "Musik spielen",
        "Ein Instrument vor Publikum spielen.",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.CHARISMA: 30, StatType.AGILITY: 5},
        stamina_cost=10, time_minutes=30
    ),
    "debate": Activity(
        "debate", "Debate", "Debattieren",
        "Argumentieren und überzeugen üben.",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.CHARISMA: 20, StatType.INTELLIGENCE: 10},
        time_minutes=45
    ),
    "flirting": Activity(
        "flirting", "Flirting", "Flirten",
        "Die Kunst der Verführung... ähm, Überzeugung!",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.CHARISMA: 25, StatType.PERCEPTION: 5},
        time_minutes=20
    ),
    "leadership": Activity(
        "leadership", "Lead a Group", "Gruppe anführen",
        "Eine Gruppe durch eine Herausforderung führen.",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.CHARISMA: 30, StatType.INTELLIGENCE: 10},
        stamina_cost=20, time_minutes=60
    ),

    # =====================================================
    # GLÜCK - NICHT NORMAL TRAINIERBAR!
    # =====================================================
    "gambling": Activity(
        "gambling", "Gambling", "Glücksspiel",
        "Dein Glück auf die Probe stellen. VORSICHT: Kann auch sinken!",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.LUCK: 0},  # Speziell behandelt!
        time_minutes=30
    ),
    "find_four_leaf_clover": Activity(
        "find_four_leaf_clover", "Find Four-Leaf Clover", "Vierblättriges Kleeblatt finden",
        "Seltenes Glück! Nur durch Zufall möglich.",
        ActivityCategory.EXPLORATION,
        stat_gains={StatType.LUCK: 50},  # Sehr selten!
        time_minutes=60
    ),
    "pray_at_shrine": Activity(
        "pray_at_shrine", "Pray at Shrine", "Am Schrein beten",
        "Die Götter um Glück bitten.",
        ActivityCategory.SOCIAL,
        stat_gains={StatType.LUCK: 10, StatType.CHARISMA: 5},
        time_minutes=15, daily_limit=1
    ),

    # =====================================================
    # KOMBINATION / ALLROUNDER
    # =====================================================
    "dungeon_crawling": Activity(
        "dungeon_crawling", "Dungeon Crawling", "Dungeon erkunden",
        "Ein ganzes Dungeon durchkämpfen - trainiert alles!",
        ActivityCategory.EXPLORATION,
        stat_gains={
            StatType.STRENGTH: 10,
            StatType.ENDURANCE: 15,
            StatType.AGILITY: 10,
            StatType.PERCEPTION: 15,
            StatType.INTELLIGENCE: 5
        },
        stamina_cost=50, mana_cost=20, time_minutes=120, daily_limit=1
    ),
    "arena_fight": Activity(
        "arena_fight", "Arena Fight", "Arena-Kampf",
        "Ein echter Kampf in der Arena.",
        ActivityCategory.COMBAT,
        stat_gains={
            StatType.STRENGTH: 15,
            StatType.ENDURANCE: 15,
            StatType.AGILITY: 15
        },
        stamina_cost=60, time_minutes=30, daily_limit=3
    ),
}


# =============================================================================
# WAFFEN-SKALIERUNG (Dark Souls Style)
# =============================================================================

@dataclass
class WeaponScaling:
    """Wie eine Waffe mit Stats skaliert"""
    weapon_id: str
    name: str

    # Skalierung pro Stat (A-E oder -)
    strength_scaling: ScalingGrade = ScalingGrade.NONE
    agility_scaling: ScalingGrade = ScalingGrade.NONE
    intelligence_scaling: ScalingGrade = ScalingGrade.NONE

    # Basis-Schaden (ohne Skalierung)
    base_damage: int = 10


WEAPON_SCALING_DB: Dict[str, WeaponScaling] = {
    # Schwerter - STR/AGI balanced
    "rusty_sword": WeaponScaling("rusty_sword", "Rostiges Schwert", ScalingGrade.D, ScalingGrade.D, base_damage=15),
    "iron_sword": WeaponScaling("iron_sword", "Eisenschwert", ScalingGrade.C, ScalingGrade.D, base_damage=22),
    "steel_sword": WeaponScaling("steel_sword", "Stahlschwert", ScalingGrade.C, ScalingGrade.C, base_damage=28),
    "katana": WeaponScaling("katana", "Katana", ScalingGrade.D, ScalingGrade.A, base_damage=24),  # AGI-fokussiert!

    # Zweihänder - STR dominant
    "zweihander": WeaponScaling("zweihander", "Zweihänder", ScalingGrade.A, ScalingGrade.D, base_damage=35),
    "dragon_slayer": WeaponScaling("dragon_slayer", "Drachentöter", ScalingGrade.S, ScalingGrade.E, base_damage=80),

    # Dolche - AGI dominant
    "rusty_dagger": WeaponScaling("rusty_dagger", "Rostiger Dolch", ScalingGrade.E, ScalingGrade.C, base_damage=8),
    "assassin_blade": WeaponScaling("assassin_blade", "Assassinenklinge", ScalingGrade.E, ScalingGrade.A, base_damage=12),

    # Hämmer - Reine STR
    "war_hammer": WeaponScaling("war_hammer", "Kriegshammer", ScalingGrade.A, ScalingGrade.E, base_damage=35),
    "titan_crusher": WeaponScaling("titan_crusher", "Titanenbrecher", ScalingGrade.S, ScalingGrade.NONE, base_damage=60),

    # Stäbe - INT dominant
    "wooden_staff": WeaponScaling("wooden_staff", "Holzstab", ScalingGrade.NONE, ScalingGrade.D, ScalingGrade.C, base_damage=12),
    "fire_staff": WeaponScaling("fire_staff", "Feuerstab", ScalingGrade.NONE, ScalingGrade.D, ScalingGrade.A, base_damage=18),
    "megumin_staff": WeaponScaling("megumin_staff", "Megumins Stab", ScalingGrade.NONE, ScalingGrade.NONE, ScalingGrade.S, base_damage=5),

    # Bögen - AGI + STR (Spannkraft)
    "wooden_bow": WeaponScaling("wooden_bow", "Holzbogen", ScalingGrade.D, ScalingGrade.C, base_damage=18),
    "longbow": WeaponScaling("longbow", "Langbogen", ScalingGrade.C, ScalingGrade.B, base_damage=28),
}


# =============================================================================
# SPIELER STATS
# =============================================================================

@dataclass
class PlayerStats:
    """Spieler-Stats mit Training-Tracking"""
    # Basis-Stats (Fallout SPECIAL Start: 5-10, je nach Verteilung)
    strength: int = 5
    endurance: int = 5
    agility: int = 5
    intelligence: int = 5
    perception: int = 5
    charisma: int = 5
    luck: int = 5  # NICHT normal trainierbar!

    # XP pro Stat (für Level-Up)
    stat_xp: Dict[str, int] = field(default_factory=lambda: {
        "strength": 0, "endurance": 0, "agility": 0,
        "intelligence": 0, "perception": 0, "charisma": 0, "luck": 0
    })

    # Training-Tracking (für Diminishing Returns)
    daily_training: Dict[str, int] = field(default_factory=dict)  # stat -> count today
    last_training_date: str = ""

    # Aktivitäten-Cooldowns
    activity_cooldowns: Dict[str, datetime] = field(default_factory=dict)
    activity_daily_count: Dict[str, int] = field(default_factory=dict)

    def get_stat(self, stat: StatType) -> int:
        """Holt einen Stat-Wert"""
        return getattr(self, stat.value, 5)

    def set_stat(self, stat: StatType, value: int):
        """Setzt einen Stat-Wert (mit Limits)"""
        setattr(self, stat.value, max(1, min(30, value)))  # 1-30 Range


# =============================================================================
# STAT TRAINING SYSTEM
# =============================================================================

class StatTrainingSystem:
    """
    Haupt-System für Stat-Training durch Aktivitäten

    REGELN:
    1. Stats steigen durch Aktivitäten, nicht Punkte-Verteilung
    2. Diminishing Returns - Je höher der Stat, desto mehr XP nötig
    3. Tägliches Limit pro Aktivität
    4. GLÜCK ist NICHT normal trainierbar (nur spezielle Events)
    """

    def __init__(self):
        self.players: Dict[str, PlayerStats] = {}

        # XP-Kurve: Wie viel XP für nächsten Stat-Punkt?
        # Exponentiell: Stat 5->6 braucht weniger als 25->26
        self.BASE_XP_NEEDED = 100
        self.XP_SCALING = 1.15  # +15% pro Level

        # Diminishing Returns: Weniger XP wenn schon viel trainiert heute
        self.DAILY_DIMINISHING = 0.8  # 80% XP ab 2. Training, 64% ab 3., etc.
        self.DAILY_TRAINING_CAP = 5  # Max 5x pro Stat pro Tag

    def register_player(self, player_id: str, initial_stats: Optional[Dict[str, int]] = None) -> PlayerStats:
        """Registriert einen Spieler mit Start-Stats"""
        if player_id not in self.players:
            stats = PlayerStats()

            # Fallout-Style: 21 Punkte verteilen auf 7 Stats (Basis 1, +20 frei)
            if initial_stats:
                for stat_name, value in initial_stats.items():
                    if hasattr(stats, stat_name):
                        setattr(stats, stat_name, max(1, min(10, value)))

            self.players[player_id] = stats

        return self.players[player_id]

    def get_xp_needed(self, current_stat: int) -> int:
        """Berechnet XP für nächsten Stat-Punkt"""
        return int(self.BASE_XP_NEEDED * (self.XP_SCALING ** (current_stat - 1)))

    def perform_activity(
        self,
        player_id: str,
        activity_id: str,
        bonus_multiplier: float = 1.0
    ) -> Dict:
        """
        Führt eine Aktivität aus und gibt Stat-XP

        Returns:
            Dict mit Ergebnis, XP-Gains, Level-Ups, etc.
        """
        if player_id not in self.players:
            return {"success": False, "error": "Spieler nicht registriert"}

        if activity_id not in ACTIVITIES_DB:
            return {"success": False, "error": f"Aktivität {activity_id} nicht gefunden"}

        player = self.players[player_id]
        activity = ACTIVITIES_DB[activity_id]

        # Datum-Check für Daily Reset
        today = datetime.now().strftime("%Y-%m-%d")
        if player.last_training_date != today:
            player.daily_training = {}
            player.activity_daily_count = {}
            player.last_training_date = today

        # Cooldown Check
        if activity_id in player.activity_cooldowns:
            cooldown_end = player.activity_cooldowns[activity_id]
            if datetime.now() < cooldown_end:
                remaining = (cooldown_end - datetime.now()).seconds // 60
                return {
                    "success": False,
                    "error": f"Cooldown! Noch {remaining} Minuten warten.",
                    "cooldown_remaining": remaining
                }

        # Daily Limit Check
        if activity.daily_limit > 0:
            current_count = player.activity_daily_count.get(activity_id, 0)
            if current_count >= activity.daily_limit:
                return {
                    "success": False,
                    "error": f"Tägliches Limit erreicht! ({activity.daily_limit}x/Tag)",
                    "daily_limit": activity.daily_limit
                }

        # Stat-Anforderungen Check
        for stat, min_val in activity.min_stat_requirements.items():
            current = player.get_stat(stat)
            if current < min_val:
                return {
                    "success": False,
                    "error": f"Brauche {stat.value} {min_val}, hast nur {current}",
                    "missing_requirement": {"stat": stat.value, "required": min_val, "current": current}
                }

        # Aktivität durchführen!
        results = {
            "success": True,
            "activity": activity_id,
            "activity_name": activity.name_de,
            "stat_gains": {},
            "level_ups": [],
            "messages": []
        }

        # XP für jeden betroffenen Stat
        for stat, base_xp in activity.stat_gains.items():
            if stat == StatType.LUCK:
                # Glück ist SPEZIELL
                luck_result = self._handle_luck_activity(player, activity_id, base_xp)
                results["luck_special"] = luck_result
                continue

            # Diminishing Returns berechnen
            times_trained_today = player.daily_training.get(stat.value, 0)

            if times_trained_today >= self.DAILY_TRAINING_CAP:
                results["messages"].append(f"{stat.value}: Tägliches Training-Limit erreicht!")
                continue

            diminishing = self.DAILY_DIMINISHING ** times_trained_today
            final_xp = int(base_xp * bonus_multiplier * diminishing)

            # XP hinzufügen
            current_xp = player.stat_xp.get(stat.value, 0)
            player.stat_xp[stat.value] = current_xp + final_xp

            # Level-Up Check
            current_stat = player.get_stat(stat)
            xp_needed = self.get_xp_needed(current_stat)

            leveled_up = False
            while player.stat_xp[stat.value] >= xp_needed and current_stat < 30:
                player.stat_xp[stat.value] -= xp_needed
                current_stat += 1
                player.set_stat(stat, current_stat)
                xp_needed = self.get_xp_needed(current_stat)
                leveled_up = True

            # Tracking
            player.daily_training[stat.value] = times_trained_today + 1

            results["stat_gains"][stat.value] = {
                "xp_gained": final_xp,
                "current_xp": player.stat_xp[stat.value],
                "xp_needed": xp_needed,
                "diminishing_factor": round(diminishing, 2),
                "times_trained_today": times_trained_today + 1
            }

            if leveled_up:
                results["level_ups"].append({
                    "stat": stat.value,
                    "new_value": current_stat
                })
                results["messages"].append(f"🎉 {stat.value.upper()} ist auf {current_stat} gestiegen!")

        # Cooldown setzen
        if activity.cooldown_minutes > 0:
            player.activity_cooldowns[activity_id] = datetime.now() + timedelta(minutes=activity.cooldown_minutes)

        # Daily Count erhöhen
        player.activity_daily_count[activity_id] = player.activity_daily_count.get(activity_id, 0) + 1

        return results

    def _handle_luck_activity(self, player: PlayerStats, activity_id: str, base_xp: int) -> Dict:
        """
        Spezielle Behandlung für GLÜCK

        Glück ist NICHT normal trainierbar!
        - Glücksspiel: Kann steigen ODER sinken!
        - Kleeblatt: Sehr selten, aber großer Boost
        - Schrein: Kleiner garantierter Bonus (1x/Tag)
        """
        if activity_id == "gambling":
            # 40% Glück steigt, 40% Glück sinkt, 20% nichts
            roll = random.random()
            if roll < 0.4:
                # Glück!
                gain = random.randint(5, 15)
                player.stat_xp["luck"] = player.stat_xp.get("luck", 0) + gain
                return {"result": "win", "xp_change": gain, "message": "🍀 Glück gehabt! Luck XP +{gain}"}
            elif roll < 0.8:
                # Pech!
                loss = random.randint(5, 15)
                player.stat_xp["luck"] = max(0, player.stat_xp.get("luck", 0) - loss)
                return {"result": "lose", "xp_change": -loss, "message": f"💔 Pech gehabt! Luck XP -{loss}"}
            else:
                return {"result": "neutral", "xp_change": 0, "message": "😐 Nichts passiert..."}

        elif activity_id == "find_four_leaf_clover":
            # Sehr selten erfolgreich (5% Chance)
            if random.random() < 0.05:
                player.stat_xp["luck"] = player.stat_xp.get("luck", 0) + base_xp
                return {"result": "found", "xp_change": base_xp, "message": f"🍀🍀🍀 VIERBLÄTTRIGES KLEEBLATT! +{base_xp} Luck XP!"}
            else:
                return {"result": "not_found", "xp_change": 0, "message": "Kein Glück beim Suchen..."}

        elif activity_id == "pray_at_shrine":
            # Garantierter kleiner Bonus
            player.stat_xp["luck"] = player.stat_xp.get("luck", 0) + base_xp
            return {"result": "blessed", "xp_change": base_xp, "message": f"✨ Segen erhalten! +{base_xp} Luck XP"}

        return {"result": "unknown", "xp_change": 0}

    def calculate_weapon_damage(
        self,
        player_id: str,
        weapon_id: str,
        base_damage: Optional[int] = None
    ) -> Dict:
        """
        Berechnet Waffen-Schaden mit Stat-Skalierung (Dark Souls Style)

        Formel: base_damage + (stat_bonus * scaling_multiplier)
        """
        if player_id not in self.players:
            return {"error": "Spieler nicht registriert", "damage": 0}

        if weapon_id not in WEAPON_SCALING_DB:
            return {"error": f"Waffe {weapon_id} nicht in Scaling-DB", "damage": base_damage or 10}

        player = self.players[player_id]
        scaling = WEAPON_SCALING_DB[weapon_id]

        use_base = base_damage if base_damage else scaling.base_damage

        # Stat-Boni berechnen
        str_bonus = 0
        agi_bonus = 0
        int_bonus = 0

        if scaling.strength_scaling != ScalingGrade.NONE:
            str_mult = SCALING_MULTIPLIERS[scaling.strength_scaling]
            str_bonus = int((player.strength - 10) * str_mult * 2)  # -10 als Baseline

        if scaling.agility_scaling != ScalingGrade.NONE:
            agi_mult = SCALING_MULTIPLIERS[scaling.agility_scaling]
            agi_bonus = int((player.agility - 10) * agi_mult * 2)

        if scaling.intelligence_scaling != ScalingGrade.NONE:
            int_mult = SCALING_MULTIPLIERS[scaling.intelligence_scaling]
            int_bonus = int((player.intelligence - 10) * int_mult * 2)

        total_bonus = str_bonus + agi_bonus + int_bonus
        final_damage = max(1, use_base + total_bonus)

        return {
            "weapon": weapon_id,
            "weapon_name": scaling.name,
            "base_damage": use_base,
            "scaling": {
                "strength": {"grade": scaling.strength_scaling.value, "bonus": str_bonus},
                "agility": {"grade": scaling.agility_scaling.value, "bonus": agi_bonus},
                "intelligence": {"grade": scaling.intelligence_scaling.value, "bonus": int_bonus},
            },
            "total_bonus": total_bonus,
            "final_damage": final_damage
        }

    def get_player_status(self, player_id: str) -> Dict:
        """Holt kompletten Spieler-Status"""
        if player_id not in self.players:
            return {"error": "Spieler nicht registriert"}

        player = self.players[player_id]

        # Stats mit XP-Progress
        stats_info = {}
        for stat in StatType:
            current = player.get_stat(stat)
            current_xp = player.stat_xp.get(stat.value, 0)
            xp_needed = self.get_xp_needed(current)
            progress = (current_xp / xp_needed) * 100 if xp_needed > 0 else 100

            stats_info[stat.value] = {
                "value": current,
                "xp": current_xp,
                "xp_needed": xp_needed,
                "progress_percent": round(progress, 1),
                "trained_today": player.daily_training.get(stat.value, 0),
                "daily_cap": self.DAILY_TRAINING_CAP
            }

        return {
            "player_id": player_id,
            "stats": stats_info,
            "activities_today": player.activity_daily_count,
            "last_training_date": player.last_training_date
        }

    def get_available_activities(self, player_id: str) -> List[Dict]:
        """Listet alle Aktivitäten mit Verfügbarkeit"""
        if player_id not in self.players:
            return []

        player = self.players[player_id]
        today = datetime.now().strftime("%Y-%m-%d")

        activities = []
        for act_id, activity in ACTIVITIES_DB.items():
            # Cooldown Check
            on_cooldown = False
            cooldown_remaining = 0
            if act_id in player.activity_cooldowns:
                if datetime.now() < player.activity_cooldowns[act_id]:
                    on_cooldown = True
                    cooldown_remaining = (player.activity_cooldowns[act_id] - datetime.now()).seconds // 60

            # Daily Limit Check
            daily_count = player.activity_daily_count.get(act_id, 0) if player.last_training_date == today else 0
            at_daily_limit = activity.daily_limit > 0 and daily_count >= activity.daily_limit

            # Requirement Check
            meets_requirements = True
            missing_reqs = []
            for stat, min_val in activity.min_stat_requirements.items():
                if player.get_stat(stat) < min_val:
                    meets_requirements = False
                    missing_reqs.append({"stat": stat.value, "required": min_val, "current": player.get_stat(stat)})

            activities.append({
                "id": act_id,
                "name": activity.name_de,
                "description": activity.description_de,
                "category": activity.category.value,
                "stat_gains": {s.value: v for s, v in activity.stat_gains.items()},
                "stamina_cost": activity.stamina_cost,
                "mana_cost": activity.mana_cost,
                "time_minutes": activity.time_minutes,
                "available": not on_cooldown and not at_daily_limit and meets_requirements,
                "on_cooldown": on_cooldown,
                "cooldown_remaining": cooldown_remaining,
                "at_daily_limit": at_daily_limit,
                "daily_count": daily_count,
                "daily_limit": activity.daily_limit,
                "meets_requirements": meets_requirements,
                "missing_requirements": missing_reqs
            })

        return activities

    def export_state(self, player_id: str) -> Dict:
        """Exportiert Spieler-State für Save"""
        if player_id not in self.players:
            return {}

        player = self.players[player_id]

        return {
            "stats": {
                "strength": player.strength,
                "endurance": player.endurance,
                "agility": player.agility,
                "intelligence": player.intelligence,
                "perception": player.perception,
                "charisma": player.charisma,
                "luck": player.luck
            },
            "stat_xp": player.stat_xp,
            "daily_training": player.daily_training,
            "last_training_date": player.last_training_date,
            "activity_daily_count": player.activity_daily_count
        }

    def import_state(self, player_id: str, state: Dict):
        """Importiert Spieler-State"""
        if player_id not in self.players:
            self.register_player(player_id)

        player = self.players[player_id]

        if "stats" in state:
            for stat_name, value in state["stats"].items():
                if hasattr(player, stat_name):
                    setattr(player, stat_name, value)

        if "stat_xp" in state:
            player.stat_xp = state["stat_xp"]
        if "daily_training" in state:
            player.daily_training = state["daily_training"]
        if "last_training_date" in state:
            player.last_training_date = state["last_training_date"]
        if "activity_daily_count" in state:
            player.activity_daily_count = state["activity_daily_count"]


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_training_system: Optional[StatTrainingSystem] = None

def get_training_system() -> StatTrainingSystem:
    """Singleton für Training System"""
    global _training_system
    if _training_system is None:
        _training_system = StatTrainingSystem()
    return _training_system


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("NAJIKA STAT TRAINING SYSTEM - TEST")
    print("Stats steigen durch TAETIGKEIT, nicht Level-Up!")
    print("=" * 70)

    system = get_training_system()

    # Spieler mit Fallout-Style Start-Stats
    print("\n--- Spieler erstellen (Fallout-Style) ---")
    system.register_player("kuja", {
        "strength": 6,
        "endurance": 5,
        "agility": 7,
        "intelligence": 8,
        "perception": 6,
        "charisma": 4,
        "luck": 5
    })

    status = system.get_player_status("kuja")
    print("Start-Stats:")
    for stat, info in status["stats"].items():
        print(f"  {stat.upper():12} {info['value']:2}")

    # Training: Holz hacken (STR + END)
    print("\n--- Holz hacken (STR + END Training) ---")
    for i in range(3):
        result = system.perform_activity("kuja", "chop_wood")
        if result["success"]:
            for stat, gain in result["stat_gains"].items():
                print(f"  {stat}: +{gain['xp_gained']} XP (Diminishing: {gain['diminishing_factor']})")
            if result["level_ups"]:
                for lvl in result["level_ups"]:
                    print(f"  LEVEL UP: {lvl['stat']} -> {lvl['new_value']}!")

    # Training: Buecher lesen (INT)
    print("\n--- Buecher lesen (INT Training) ---")
    for i in range(5):
        result = system.perform_activity("kuja", "read_books")
        if result["success"]:
            int_gain = result["stat_gains"].get("intelligence", {})
            print(f"  INT: +{int_gain.get('xp_gained', 0)} XP")
            if result["level_ups"]:
                print(f"  LEVEL UP!")

    # Status nach Training
    print("\n--- Status nach Training ---")
    status = system.get_player_status("kuja")
    for stat, info in status["stats"].items():
        print(f"  {stat.upper():12} {info['value']:2} | XP: {info['xp']:3}/{info['xp_needed']:3} ({info['progress_percent']:.0f}%) | Trained: {info['trained_today']}/{info['daily_cap']}")

    # Waffen-Skalierung Test
    print("\n--- Waffen-Skalierung Test ---")
    weapons_to_test = ["katana", "zweihander", "fire_staff"]
    for wid in weapons_to_test:
        dmg = system.calculate_weapon_damage("kuja", wid)
        print(f"  {dmg['weapon_name']:20} Base: {dmg['base_damage']:3} + Bonus: {dmg['total_bonus']:+3} = {dmg['final_damage']:3} DMG")
        print(f"    Scaling: STR({dmg['scaling']['strength']['grade']}) AGI({dmg['scaling']['agility']['grade']}) INT({dmg['scaling']['intelligence']['grade']})")

    # Glueck Test
    print("\n--- Glueck Test (Gluecksspiel) ---")
    for i in range(3):
        result = system.perform_activity("kuja", "gambling")
        if "luck_special" in result:
            print(f"  {result['luck_special']['message']}")

    print("\n" + "=" * 70)
    print("Test abgeschlossen!")
    print("Stats steigen durch TAETIGKEIT, nicht Punkte-Verteilung!")
    print("=" * 70)
