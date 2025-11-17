"""
Slime Companion System - Najika World
======================================

Komplettes Slime-System:
- Level 1-49: Fantasy-Tier (Flammen-Hase, Eis-Fuchs, etc.)
- Level 50: Metamorphose → Slime
- 8 Farben (regions-basiert)
- Rainbow-Slime (alle 8 sammeln)
- Minimal Tamagotchi (Hunger/Durst/Schlaf/Stimmung/Kampfeslust)
- Rettungs-Mechanik (1x/24h in Hardcore)
- Learning System (10-15% von Gegnern, 1% vom Spieler!)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
import random


class SlimeColor(Enum):
    """8 Slime-Farben (regions-basiert)"""
    MOSS_GREEN = "moss_green"      # Samtmoos-Tiefwald
    CRYSTAL_WHITE = "crystal_white" # Reich der Drei
    OCEAN_BLUE = "ocean_blue"       # Salzwind-Küste
    LIGHTNING_PURPLE = "lightning_purple"  # Blitzebene
    MIDNIGHT_BLACK = "midnight_black"      # Grünschlamm-Sumpf
    MOLTEN_RED = "molten_red"       # Magmaströme
    DUSTY_GOLD = "dusty_gold"       # Heiße Dünen
    DEEP_PURPLE = "deep_purple"     # Tiefenhöhlen
    RAINBOW = "rainbow"             # Ultimate (alle 8 gesammelt)


class FantasyTier(Enum):
    """Fantasy-Tiere vor Metamorphose (Level 1-49)"""
    FLAMMEN_HASE = "flammen_hase"           # Fire Rabbit
    EIS_FUCHS = "eis_fuchs"                 # Ice Fox
    DONNER_EULE = "donner_eule"             # Thunder Owl
    WASSER_KATZE = "wasser_katze"           # Water Cat
    STEIN_WOLF = "stein_wolf"               # Stone Wolf
    WIND_FALKE = "wind_falke"               # Wind Hawk
    GIFT_SCHLANGE = "gift_schlange"         # Poison Snake
    LICHT_HIRSCH = "licht_hirsch"           # Light Deer


@dataclass
class LearnedMove:
    """Gelernter Move"""
    move_name: str
    move_type: str  # "player" or "enemy"
    learned_from: str  # Player name or enemy name
    learned_at: datetime
    times_used: int = 0
    success_rate: float = 0.0


@dataclass
class TamagotchiStats:
    """Minimal Tamagotchi Stats für Slime"""
    hunger: float = 100.0  # 0-100
    durst: float = 100.0   # 0-100 (Thirst)
    schlaf: float = 100.0  # 0-100 (Sleep)
    stimmung: float = 100.0  # 0-100 (Mood)
    kampfeslust: float = 50.0  # 0-100 (Battle Lust)

    # Decay Rates (pro Stunde, MINIMAL für Slime)
    hunger_decay_rate: float = 2.0
    durst_decay_rate: float = 3.0
    schlaf_decay_rate: float = 1.5
    stimmung_decay_rate: float = 1.0
    kampfeslust_decay_rate: float = 0.5

    last_update: datetime = field(default_factory=datetime.now)


@dataclass
class SlimeCompanion:
    """Slime Companion"""
    companion_id: int
    owner_player_id: int
    name: str

    # Level & Evolution
    level: int = 1
    experience: int = 0
    is_slime: bool = False  # True nach Level 50 Metamorphose

    # Form
    fantasy_tier: Optional[FantasyTier] = None  # Level 1-49
    slime_color: Optional[SlimeColor] = None    # Level 50+

    # Tamagotchi
    tamagotchi: TamagotchiStats = field(default_factory=TamagotchiStats)

    # Learning System
    learned_moves: List[LearnedMove] = field(default_factory=list)
    max_learned_moves: int = 10

    # Rettungs-Mechanik (Hardcore)
    rescue_available: bool = True
    last_rescue_used: Optional[datetime] = None
    rescue_cooldown_hours: int = 24

    # Collections (für Rainbow-Slime)
    collected_colors: List[SlimeColor] = field(default_factory=list)

    # Stats
    battles_fought: int = 0
    rescues_performed: int = 0
    created_at: datetime = field(default_factory=datetime.now)


class SlimeSystem:
    """
    Slime Companion System Manager

    Verwaltet alle Slime-Companions, Evolution, Learning, Tamagotchi
    """

    def __init__(self):
        self.companions: Dict[int, SlimeCompanion] = {}
        self.next_companion_id = 1

        # Learning Chances
        self.LEARN_FROM_ENEMY_CHANCE = 0.125  # 12.5% (10-15%)
        self.LEARN_FROM_PLAYER_CHANCE = 0.01  # 1%

        # Color-Region Mapping
        self.REGION_COLOR_MAP = {
            "samtmoos_tiefwald": SlimeColor.MOSS_GREEN,
            "reich_der_drei": SlimeColor.CRYSTAL_WHITE,
            "salzwind_kueste": SlimeColor.OCEAN_BLUE,
            "blitzebene": SlimeColor.LIGHTNING_PURPLE,
            "gruenschlamm_sumpf": SlimeColor.MIDNIGHT_BLACK,
            "magmastroeme": SlimeColor.MOLTEN_RED,
            "heisse_duenen": SlimeColor.DUSTY_GOLD,
            "tiefenhoehlen": SlimeColor.DEEP_PURPLE
        }


    def create_companion(
        self,
        owner_player_id: int,
        name: str,
        starting_region: str
    ) -> SlimeCompanion:
        """
        Erstellt einen neuen Companion

        Args:
            owner_player_id: Player ID
            name: Companion Name
            starting_region: Region wo erstellt (bestimmt später Slime-Farbe)

        Returns:
            SlimeCompanion
        """
        # Wähle zufälliges Fantasy-Tier
        fantasy_tier = random.choice(list(FantasyTier))

        companion = SlimeCompanion(
            companion_id=self.next_companion_id,
            owner_player_id=owner_player_id,
            name=name,
            fantasy_tier=fantasy_tier
        )

        self.companions[self.next_companion_id] = companion
        self.next_companion_id += 1

        return companion


    def add_experience(
        self,
        companion_id: int,
        exp_amount: int
    ) -> Tuple[bool, Dict]:
        """
        Fügt Erfahrung hinzu und prüft Level-Up

        Returns:
            (leveled_up, result_dict)
        """
        if companion_id not in self.companions:
            return False, {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]
        old_level = companion.level

        companion.experience += exp_amount

        # Einfache Level-Formel: 100 XP pro Level
        exp_for_next_level = companion.level * 100

        leveled_up = False
        metamorphosis = False

        while companion.experience >= exp_for_next_level:
            companion.experience -= exp_for_next_level
            companion.level += 1
            leveled_up = True

            # Check für Metamorphose (Level 50!)
            if companion.level == 50 and not companion.is_slime:
                metamorphosis = True

            exp_for_next_level = companion.level * 100

        result = {
            "companion_id": companion_id,
            "old_level": old_level,
            "new_level": companion.level,
            "leveled_up": leveled_up,
            "experience": companion.experience,
            "exp_for_next_level": exp_for_next_level
        }

        if metamorphosis:
            result["metamorphosis"] = True
            result["message"] = f"🎉 METAMORPHOSE! {companion.name} wird zu Slime!"

        return leveled_up, result


    def perform_metamorphosis(
        self,
        companion_id: int,
        current_region: str
    ) -> Dict:
        """
        Führt Metamorphose durch (Level 50)

        Args:
            companion_id: Companion ID
            current_region: Aktuelle Region (bestimmt Farbe)

        Returns:
            Result dict
        """
        if companion_id not in self.companions:
            return {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]

        if companion.level < 50:
            return {"error": f"Level zu niedrig (Level {companion.level}/50)"}

        if companion.is_slime:
            return {"error": "Bereits ein Slime"}

        # Metamorphose!
        old_form = companion.fantasy_tier
        companion.is_slime = True
        companion.fantasy_tier = None

        # Farbe basiert auf Region
        color = self.REGION_COLOR_MAP.get(current_region, SlimeColor.MOSS_GREEN)
        companion.slime_color = color

        # Füge Farbe zu Collection hinzu
        if color not in companion.collected_colors:
            companion.collected_colors.append(color)

        return {
            "companion_id": companion_id,
            "success": True,
            "message": f"🌟 {companion.name} hat sich verwandelt!",
            "old_form": old_form.value if old_form else None,
            "new_form": "slime",
            "color": color.value,
            "collected_colors": len(companion.collected_colors)
        }


    def collect_color(
        self,
        companion_id: int,
        region: str
    ) -> Dict:
        """
        Sammelt eine Slime-Farbe in einer Region

        Ermöglicht Rainbow-Slime Quest (alle 8 sammeln)

        Returns:
            Result dict
        """
        if companion_id not in self.companions:
            return {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]

        if not companion.is_slime:
            return {"error": "Nur Slimes können Farben sammeln"}

        color = self.REGION_COLOR_MAP.get(region)
        if not color:
            return {"error": f"Ungültige Region: {region}"}

        if color in companion.collected_colors:
            return {
                "already_collected": True,
                "color": color.value,
                "message": f"Farbe {color.value} bereits gesammelt"
            }

        # Sammle Farbe
        companion.collected_colors.append(color)

        result = {
            "companion_id": companion_id,
            "color_collected": color.value,
            "total_colors": len(companion.collected_colors),
            "remaining_colors": 8 - len(companion.collected_colors)
        }

        # Check für Rainbow-Slime
        if len(companion.collected_colors) >= 8:
            companion.slime_color = SlimeColor.RAINBOW
            result["rainbow_slime_unlocked"] = True
            result["message"] = "🌈 RAINBOW-SLIME FREIGESCHALTET!"

        return result


    def try_learn_move(
        self,
        companion_id: int,
        move_name: str,
        move_type: str,
        source_name: str
    ) -> Tuple[bool, Dict]:
        """
        Versucht einen Move zu lernen (Chance-basiert)

        Args:
            companion_id: Companion ID
            move_name: Name des Moves
            move_type: "player" oder "enemy"
            source_name: Von wem gelernt (Player/Enemy Name)

        Returns:
            (learned, result_dict)
        """
        if companion_id not in self.companions:
            return False, {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]

        # Prüfe Chance
        if move_type == "enemy":
            chance = self.LEARN_FROM_ENEMY_CHANCE
        elif move_type == "player":
            chance = self.LEARN_FROM_PLAYER_CHANCE
        else:
            return False, {"error": "Ungültiger move_type"}

        # Roll!
        roll = random.random()

        if roll > chance:
            return False, {
                "learned": False,
                "roll": roll,
                "chance": chance,
                "message": f"Konnte {move_name} nicht lernen ({roll*100:.1f}% > {chance*100:.1f}%)"
            }

        # Check ob Move bereits gelernt
        for learned_move in companion.learned_moves:
            if learned_move.move_name == move_name:
                return False, {
                    "learned": False,
                    "reason": "already_known",
                    "message": f"{move_name} bereits bekannt"
                }

        # Check Move-Limit
        if len(companion.learned_moves) >= companion.max_learned_moves:
            # Ersetze ältesten Move
            oldest_move = min(companion.learned_moves, key=lambda m: m.learned_at)
            companion.learned_moves.remove(oldest_move)

        # Lerne Move!
        new_move = LearnedMove(
            move_name=move_name,
            move_type=move_type,
            learned_from=source_name,
            learned_at=datetime.now()
        )

        companion.learned_moves.append(new_move)

        return True, {
            "learned": True,
            "move": move_name,
            "from": source_name,
            "type": move_type,
            "roll": roll,
            "chance": chance,
            "total_moves": len(companion.learned_moves),
            "message": f"✨ {companion.name} hat {move_name} gelernt!"
        }


    def use_rescue(
        self,
        companion_id: int
    ) -> Tuple[bool, Dict]:
        """
        Nutzt Rettungs-Mechanik (1x/24h in Hardcore)

        Returns:
            (rescued, result_dict)
        """
        if companion_id not in self.companions:
            return False, {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]

        # Prüfe ob Rescue verfügbar
        if not companion.rescue_available:
            # Prüfe Cooldown
            if companion.last_rescue_used:
                time_since = datetime.now() - companion.last_rescue_used
                cooldown = timedelta(hours=companion.rescue_cooldown_hours)

                if time_since < cooldown:
                    remaining = cooldown - time_since
                    hours_remaining = remaining.total_seconds() / 3600

                    return False, {
                        "rescued": False,
                        "reason": "cooldown",
                        "hours_remaining": hours_remaining,
                        "message": f"Rescue in {hours_remaining:.1f}h verfügbar"
                    }
                else:
                    # Cooldown abgelaufen, Rescue wieder verfügbar
                    companion.rescue_available = True

        # Nutze Rescue!
        companion.rescue_available = False
        companion.last_rescue_used = datetime.now()
        companion.rescues_performed += 1

        return True, {
            "rescued": True,
            "companion_name": companion.name,
            "rescues_total": companion.rescues_performed,
            "next_rescue_available_at": (
                datetime.now() + timedelta(hours=companion.rescue_cooldown_hours)
            ).isoformat(),
            "message": f"💚 {companion.name} hat dich gerettet!"
        }


    def update_tamagotchi(
        self,
        companion_id: int,
        delta_hours: Optional[float] = None
    ) -> Dict:
        """
        Updated Tamagotchi-Stats (Decay)

        Args:
            companion_id: Companion ID
            delta_hours: Zeit seit letztem Update (in Stunden)
                        Wenn None, berechne aus last_update

        Returns:
            Updated stats
        """
        if companion_id not in self.companions:
            return {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]
        tama = companion.tamagotchi

        # Berechne Delta
        if delta_hours is None:
            time_since = datetime.now() - tama.last_update
            delta_hours = time_since.total_seconds() / 3600

        # Decay (MINIMAL für Slime!)
        tama.hunger = max(0.0, tama.hunger - (tama.hunger_decay_rate * delta_hours))
        tama.durst = max(0.0, tama.durst - (tama.durst_decay_rate * delta_hours))
        tama.schlaf = max(0.0, tama.schlaf - (tama.schlaf_decay_rate * delta_hours))
        tama.stimmung = max(0.0, tama.stimmung - (tama.stimmung_decay_rate * delta_hours))
        tama.kampfeslust = max(0.0, tama.kampfeslust - (tama.kampfeslust_decay_rate * delta_hours))

        tama.last_update = datetime.now()

        return {
            "companion_id": companion_id,
            "hunger": tama.hunger,
            "durst": tama.durst,
            "schlaf": tama.schlaf,
            "stimmung": tama.stimmung,
            "kampfeslust": tama.kampfeslust,
            "delta_hours": delta_hours
        }


    def feed_companion(self, companion_id: int, amount: float = 30.0) -> Dict:
        """Füttert Companion (Hunger +amount)"""
        if companion_id not in self.companions:
            return {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]
        tama = companion.tamagotchi

        old_hunger = tama.hunger
        tama.hunger = min(100.0, tama.hunger + amount)

        return {
            "companion_id": companion_id,
            "action": "feed",
            "old_hunger": old_hunger,
            "new_hunger": tama.hunger,
            "amount": amount
        }


    def give_water(self, companion_id: int, amount: float = 40.0) -> Dict:
        """Gibt Wasser (Durst +amount)"""
        if companion_id not in self.companions:
            return {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]
        tama = companion.tamagotchi

        old_durst = tama.durst
        tama.durst = min(100.0, tama.durst + amount)

        return {
            "companion_id": companion_id,
            "action": "water",
            "old_durst": old_durst,
            "new_durst": tama.durst,
            "amount": amount
        }


    def let_sleep(self, companion_id: int, hours: float = 8.0) -> Dict:
        """Lässt Companion schlafen (Schlaf +restored)"""
        if companion_id not in self.companions:
            return {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]
        tama = companion.tamagotchi

        restored = hours * 10.0  # 10 pro Stunde
        old_schlaf = tama.schlaf
        tama.schlaf = min(100.0, tama.schlaf + restored)

        return {
            "companion_id": companion_id,
            "action": "sleep",
            "old_schlaf": old_schlaf,
            "new_schlaf": tama.schlaf,
            "hours": hours,
            "restored": restored
        }


    def get_companion_info(self, companion_id: int) -> Dict:
        """Holt komplette Companion-Info"""
        if companion_id not in self.companions:
            return {"error": "Companion nicht gefunden"}

        companion = self.companions[companion_id]

        return {
            "companion_id": companion.companion_id,
            "owner_player_id": companion.owner_player_id,
            "name": companion.name,
            "level": companion.level,
            "experience": companion.experience,
            "is_slime": companion.is_slime,
            "form": {
                "fantasy_tier": companion.fantasy_tier.value if companion.fantasy_tier else None,
                "slime_color": companion.slime_color.value if companion.slime_color else None
            },
            "tamagotchi": {
                "hunger": companion.tamagotchi.hunger,
                "durst": companion.tamagotchi.durst,
                "schlaf": companion.tamagotchi.schlaf,
                "stimmung": companion.tamagotchi.stimmung,
                "kampfeslust": companion.tamagotchi.kampfeslust
            },
            "learning": {
                "moves_learned": len(companion.learned_moves),
                "max_moves": companion.max_learned_moves,
                "moves": [
                    {
                        "name": move.move_name,
                        "type": move.move_type,
                        "from": move.learned_from,
                        "times_used": move.times_used
                    }
                    for move in companion.learned_moves
                ]
            },
            "rescue": {
                "available": companion.rescue_available,
                "total_rescues": companion.rescues_performed,
                "last_used": companion.last_rescue_used.isoformat() if companion.last_rescue_used else None
            },
            "collection": {
                "colors_collected": len(companion.collected_colors),
                "is_rainbow": companion.slime_color == SlimeColor.RAINBOW if companion.slime_color else False,
                "colors": [c.value for c in companion.collected_colors]
            },
            "stats": {
                "battles_fought": companion.battles_fought,
                "created_at": companion.created_at.isoformat()
            }
        }


    def export_state(self) -> Dict:
        """Exportiert kompletten Slime-State"""
        return {
            "companions": {
                comp_id: {
                    "companion_id": comp.companion_id,
                    "owner_player_id": comp.owner_player_id,
                    "name": comp.name,
                    "level": comp.level,
                    "experience": comp.experience,
                    "is_slime": comp.is_slime,
                    "fantasy_tier": comp.fantasy_tier.value if comp.fantasy_tier else None,
                    "slime_color": comp.slime_color.value if comp.slime_color else None,
                    "tamagotchi": {
                        "hunger": comp.tamagotchi.hunger,
                        "durst": comp.tamagotchi.durst,
                        "schlaf": comp.tamagotchi.schlaf,
                        "stimmung": comp.tamagotchi.stimmung,
                        "kampfeslust": comp.tamagotchi.kampfeslust,
                        "last_update": comp.tamagotchi.last_update.isoformat()
                    },
                    "learned_moves": [
                        {
                            "move_name": move.move_name,
                            "move_type": move.move_type,
                            "learned_from": move.learned_from,
                            "learned_at": move.learned_at.isoformat(),
                            "times_used": move.times_used
                        }
                        for move in comp.learned_moves
                    ],
                    "rescue_available": comp.rescue_available,
                    "last_rescue_used": comp.last_rescue_used.isoformat() if comp.last_rescue_used else None,
                    "collected_colors": [c.value for c in comp.collected_colors],
                    "battles_fought": comp.battles_fought,
                    "rescues_performed": comp.rescues_performed,
                    "created_at": comp.created_at.isoformat()
                }
                for comp_id, comp in self.companions.items()
            },
            "next_companion_id": self.next_companion_id
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== Slime Companion System Test ===\n")

    slime_sys = SlimeSystem()

    # Test 1: Create Companion
    print("1. Create Companion (Player 1, Region: Samtmoos-Tiefwald)")
    companion = slime_sys.create_companion(1, "Fluffi", "samtmoos_tiefwald")
    print(f"   → {companion.name} (Level {companion.level})")
    print(f"   → Form: {companion.fantasy_tier.value}\n")

    # Test 2: Add Experience
    print("2. Add Experience (Level-Ups)")
    for i in range(5):
        leveled, result = slime_sys.add_experience(companion.companion_id, 120)
        if leveled:
            print(f"   → Level {result['old_level']} → {result['new_level']}")

    # Test 3: Massive XP für Metamorphose
    print("\n3. Massive XP für Metamorphose (→ Level 50)")
    _, result = slime_sys.add_experience(companion.companion_id, 5000)
    print(f"   → Level: {result['new_level']}")

    if result['new_level'] >= 50:
        meta_result = slime_sys.perform_metamorphosis(companion.companion_id, "samtmoos_tiefwald")
        print(f"   → {meta_result['message']}")
        print(f"   → Farbe: {meta_result['color']}\n")

    # Test 4: Learn Moves
    print("4. Try Learn Moves (from enemies)")
    for i in range(10):
        learned, result = slime_sys.try_learn_move(
            companion.companion_id,
            f"Thunder Strike {i}",
            "enemy",
            f"Goblin {i}"
        )
        if learned:
            print(f"   ✨ {result['message']}")

    # Test 5: Rescue Mechanic
    print("\n5. Use Rescue (Hardcore)")
    rescued, result = slime_sys.use_rescue(companion.companion_id)
    print(f"   → {result['message']}")
    print(f"   → Rescues total: {result['rescues_total']}")
    print(f"   → Next available: {result['next_rescue_available_at']}\n")

    # Test 6: Try Rescue again (should fail - cooldown)
    print("6. Try Rescue again (should fail)")
    rescued, result = slime_sys.use_rescue(companion.companion_id)
    print(f"   → Rescued: {rescued}")
    print(f"   → {result['message']}\n")

    # Test 7: Tamagotchi Update
    print("7. Tamagotchi Update (1 hour passed)")
    tama_result = slime_sys.update_tamagotchi(companion.companion_id, delta_hours=1.0)
    print(f"   → Hunger: {tama_result['hunger']:.1f}")
    print(f"   → Durst: {tama_result['durst']:.1f}")
    print(f"   → Schlaf: {tama_result['schlaf']:.1f}\n")

    # Test 8: Feed Companion
    print("8. Feed Companion")
    feed_result = slime_sys.feed_companion(companion.companion_id, 30.0)
    print(f"   → Hunger: {feed_result['old_hunger']:.1f} → {feed_result['new_hunger']:.1f}\n")

    # Test 9: Collect Colors (Rainbow Quest)
    print("9. Collect Colors (Rainbow-Slime Quest)")
    regions = ["reich_der_drei", "salzwind_kueste", "blitzebene", "gruenschlamm_sumpf",
               "magmastroeme", "heisse_duenen", "tiefenhoehlen"]

    for region in regions:
        result = slime_sys.collect_color(companion.companion_id, region)
        if "rainbow_slime_unlocked" in result:
            print(f"   🌈 {result['message']}")
            break
        else:
            print(f"   → {result.get('color_collected', 'N/A')} ({result['total_colors']}/8)")

    # Test 10: Get Full Info
    print("\n10. Full Companion Info")
    info = slime_sys.get_companion_info(companion.companion_id)
    print(f"   Name: {info['name']}")
    print(f"   Level: {info['level']}")
    print(f"   Form: {info['form']['slime_color']}")
    print(f"   Moves Learned: {info['learning']['moves_learned']}")
    print(f"   Colors Collected: {info['collection']['colors_collected']}/8")
    print(f"   Is Rainbow: {info['collection']['is_rainbow']}")

    print("\n=== Slime System Test Complete ===")
