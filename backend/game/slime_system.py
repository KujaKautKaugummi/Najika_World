"""
Najika Slime Companion System - Backend
Implements complete companion evolution system from animal to slime
Based on: DOCS/design/SLIME_COMPANION_SYSTEM.md

Features:
- Random starter animals (Level 1-49)
- Tamagotchi-style care system (hunger, thirst, sleep, mood, battle_lust)
- Metamorphosis at Level 50 + critical event
- 8 collectible slime colors (one per region)
- Learning system (copy moves from enemies)
- Rescue mechanic (1x/24h, Hardcore-only)
- Slime-Arena integration
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class CompanionForm(Enum):
    """Companion current form"""
    ANIMAL = "animal"
    SLIME = "slime"


class SlimeColor(Enum):
    """8 slime colors, one per region"""
    BERNSTEIN = "bernstein"  # Amber - Desert
    SMARAGD = "smaragd"      # Emerald - Forest
    AZUR = "azur"            # Azure - Coast
    AMETHYST = "amethyst"    # Amethyst - Highland
    ONYX = "onyx"            # Onyx - Swamp
    PERLE = "perle"          # Pearl - Ice
    RUBIN = "rubin"          # Ruby - Volcano
    OBSIDIAN = "obsidian"    # Obsidian - Endgame


class CombatMode(Enum):
    """Slime combat modes"""
    PRE_FIGHT_BIND = "pre_fight_bind"        # Always with player
    ONE_TIME_SUMMON = "one_time_summon"      # Summoned for 1 battle
    INTERCEPT = "intercept"                  # Auto-rescue at low HP
    MANUAL_CONTROL = "manual_control"        # Player controls slime (Arena only)


@dataclass
class StarterAnimal:
    """Starter animal template"""
    name: str
    type: str  # fire, ice, dark, lightning, nature, earth
    speed: int
    base_hp: int = 50
    base_attack: int = 10
    base_defense: int = 8


@dataclass
class SlimeMove:
    """Move learned by slime"""
    move_id: str
    name: str
    damage: int
    element: str
    mana_cost: int
    learned_from: str  # Enemy that taught this move
    learned_at_timestamp: datetime


@dataclass
class CompanionNeeds:
    """Tamagotchi-style needs"""
    hunger: float = 100.0      # 0-100
    thirst: float = 100.0      # 0-100
    sleep: float = 100.0       # 0-100
    mood: float = 100.0        # 0-100
    battle_lust: float = 50.0  # 0-100

    def update(self, delta_time: float):
        """Update needs over time (delta_time in seconds)"""
        self.hunger = max(0.0, self.hunger - 0.01 * delta_time)
        self.thirst = max(0.0, self.thirst - 0.02 * delta_time)  # Decays faster
        self.sleep = max(0.0, self.sleep - 0.005 * delta_time)
        self.mood = max(0.0, self.mood - 0.003 * delta_time)

    def get_penalties(self) -> Dict[str, float]:
        """Calculate combat penalties based on needs"""
        penalties = {}

        if self.hunger < 30:
            penalties["damage_multiplier"] = 0.80  # -20% damage
            penalties["speed_multiplier"] = 0.85   # -15% speed

        if self.thirst < 20:
            penalties["defense_multiplier"] = 0.70  # -30% defense
            penalties["accuracy_multiplier"] = 0.75  # -25% accuracy

        if self.sleep < 10:
            penalties["error_rate"] = 1.50  # +50% error rate

        if self.mood < 20:
            penalties["obedience_rate"] = 0.50  # 50% chance to ignore commands

        if self.battle_lust > 80:
            penalties["aggression_bonus"] = 1.15  # +15% damage when bloodthirsty

        return penalties


@dataclass
class SlimeCompanionState:
    """Complete state of a slime companion"""
    companion_id: str
    player_id: str

    # Form & Evolution
    current_form: CompanionForm = CompanionForm.ANIMAL
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 100

    # Animal data
    animal: Optional[StarterAnimal] = None

    # Slime data
    slime_unlocked: bool = False
    current_slime_color: Optional[SlimeColor] = None
    collected_colors: List[SlimeColor] = field(default_factory=list)

    # Needs (Tamagotchi)
    needs: CompanionNeeds = field(default_factory=CompanionNeeds)

    # Combat
    hp: int = 50
    max_hp: int = 50
    attack: int = 10
    defense: int = 8
    speed: int = 10
    moveset: List[SlimeMove] = field(default_factory=list)
    max_moves: int = 20

    # Rescue system (Hardcore only)
    rescue_available: bool = True
    rescue_cooldown_until: Optional[datetime] = None
    rescue_used_count_7d: int = 0
    last_rescue_timestamp: Optional[datetime] = None

    # Combat mode
    combat_mode: CombatMode = CombatMode.PRE_FIGHT_BIND
    summon_active: bool = False
    summon_end_time: Optional[datetime] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)


class SlimeCompanionSystem:
    """Main slime companion system controller"""

    # Starter animal templates
    STARTER_ANIMALS = [
        StarterAnimal("Flammen-Hase", "fire", speed=12, base_hp=45, base_attack=12, base_defense=6),
        StarterAnimal("Eis-Fuchs", "ice", speed=10, base_hp=55, base_attack=11, base_defense=9),
        StarterAnimal("Schatten-Spinne", "dark", speed=8, base_hp=50, base_attack=13, base_defense=10),
        StarterAnimal("Blitz-Rabe", "lightning", speed=14, base_hp=40, base_attack=14, base_defense=5),
        StarterAnimal("Wald-Maus", "nature", speed=9, base_hp=60, base_attack=9, base_defense=11),
        StarterAnimal("Kristall-Eichhörnchen", "earth", speed=11, base_hp=52, base_attack=10, base_defense=8)
    ]

    # Region to slime color mapping
    REGION_COLOR_MAP = {
        "Bernstein-Dünen": SlimeColor.BERNSTEIN,
        "Smaragd-Hain": SlimeColor.SMARAGD,
        "Azur-Klippen": SlimeColor.AZUR,
        "Amethyst-Steppe": SlimeColor.AMETHYST,
        "Onyx-Morast": SlimeColor.ONYX,
        "Perl-Gletscher": SlimeColor.PERLE,
        "Rubin-Schlucht": SlimeColor.RUBIN,
        "Obsidian-Nacht": SlimeColor.OBSIDIAN
    }

    # Slime color bonuses
    SLIME_BONUSES = {
        SlimeColor.BERNSTEIN: {"desert_damage": 1.10, "heat_resistance": 0.80},
        SlimeColor.SMARAGD: {"herb_effectiveness": 1.15, "poison_resistance": 0.70},
        SlimeColor.AZUR: {"fishing_success": 1.20, "water_breathing": True},
        SlimeColor.AMETHYST: {"movement_speed": 1.10, "lightning_resistance": 0.75},
        SlimeColor.ONYX: {"poison_damage": 1.15, "disease_immunity": True},
        SlimeColor.PERLE: {"ice_defense": 1.10, "cold_immunity": True},
        SlimeColor.RUBIN: {"fire_magic": 1.15, "fire_immunity": True},
        SlimeColor.OBSIDIAN: {"night_crit": 1.20, "night_vision": True}
    }

    def __init__(self):
        self.companions: Dict[str, SlimeCompanionState] = {}

    def create_companion(self, player_id: str, companion_id: str) -> Dict:
        """
        Create a new companion for a player (random starter animal)
        """
        # Roll random starter animal
        animal = random.choice(self.STARTER_ANIMALS)

        companion = SlimeCompanionState(
            companion_id=companion_id,
            player_id=player_id,
            animal=animal,
            hp=animal.base_hp,
            max_hp=animal.base_hp,
            attack=animal.base_attack,
            defense=animal.base_defense,
            speed=animal.speed
        )

        self.companions[companion_id] = companion

        return {
            "success": True,
            "companion_id": companion_id,
            "animal": {
                "name": animal.name,
                "type": animal.type,
                "stats": {
                    "hp": animal.base_hp,
                    "attack": animal.base_attack,
                    "defense": animal.base_defense,
                    "speed": animal.speed
                }
            },
            "message": f"Du hast einen {animal.name} als Begleiter erhalten!"
        }

    def check_metamorphosis(self, companion_id: str, current_region: str,
                           critical_event: bool = False) -> Dict:
        """
        Check if companion can metamorphose to slime

        Requirements:
        - Level 50
        - Critical event triggered
        - Not already slime
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        # Already slime
        if companion.slime_unlocked:
            return {"success": False, "reason": "already_slime"}

        # Level too low
        if companion.level < 50:
            return {
                "success": False,
                "reason": "level_too_low",
                "current_level": companion.level,
                "required_level": 50
            }

        # No critical event
        if not critical_event:
            return {
                "success": False,
                "reason": "no_critical_event",
                "hint": "Win boss fight, survive near-death, or complete special quest"
            }

        # All conditions met - metamorphose!
        return self._execute_metamorphosis(companion, current_region)

    def _execute_metamorphosis(self, companion: SlimeCompanionState, region: str) -> Dict:
        """
        Execute metamorphosis from animal to slime
        """
        # Determine slime color from region
        slime_color = self.REGION_COLOR_MAP.get(region, SlimeColor.BERNSTEIN)

        # Update companion state
        companion.current_form = CompanionForm.SLIME
        companion.slime_unlocked = True
        companion.current_slime_color = slime_color
        companion.collected_colors.append(slime_color)

        # Stat boost from evolution
        companion.max_hp = int(companion.max_hp * 1.5)
        companion.hp = companion.max_hp
        companion.attack = int(companion.attack * 1.3)
        companion.defense = int(companion.defense * 1.3)
        companion.speed = int(companion.speed * 1.2)

        # Unlock rescue ability
        companion.rescue_available = True

        return {
            "success": True,
            "event": "metamorphosis",
            "form": "slime",
            "color": slime_color.value,
            "region": region,
            "stats": {
                "hp": companion.max_hp,
                "attack": companion.attack,
                "defense": companion.defense,
                "speed": companion.speed
            },
            "collected_colors": [c.value for c in companion.collected_colors],
            "cutscene": "shell_break_animation",
            "message": f"Die Hülle bricht! Dein Begleiter hat sich in einen {slime_color.value.title()}-Slime verwandelt!"
        }

    def feed_companion(self, companion_id: str, food_item: Dict) -> Dict:
        """
        Feed companion to restore hunger
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        hunger_restore = food_item.get("hunger_restore", 20)
        mood_bonus = food_item.get("mood_bonus", 5)

        companion.needs.hunger = min(100.0, companion.needs.hunger + hunger_restore)
        companion.needs.mood = min(100.0, companion.needs.mood + mood_bonus)

        return {
            "success": True,
            "hunger": companion.needs.hunger,
            "mood": companion.needs.mood,
            "message": f"{companion.animal.name if companion.current_form == CompanionForm.ANIMAL else 'Slime'} hat gegessen!"
        }

    def give_water(self, companion_id: str, water_item: Dict) -> Dict:
        """
        Give water to companion
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        thirst_restore = water_item.get("thirst_restore", 30)

        companion.needs.thirst = min(100.0, companion.needs.thirst + thirst_restore)

        return {
            "success": True,
            "thirst": companion.needs.thirst
        }

    def let_sleep(self, companion_id: str, sleep_duration_hours: float) -> Dict:
        """
        Let companion sleep
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        sleep_restore = sleep_duration_hours * 10  # 10% per hour
        companion.needs.sleep = min(100.0, companion.needs.sleep + sleep_restore)
        companion.needs.mood = min(100.0, companion.needs.mood + sleep_restore * 0.5)

        return {
            "success": True,
            "sleep": companion.needs.sleep,
            "mood": companion.needs.mood,
            "message": f"Dein Begleiter hat {sleep_duration_hours} Stunden geschlafen und fühlt sich erfrischt!"
        }

    def attempt_learn_move(self, companion_id: str, enemy_move: Dict) -> Dict:
        """
        Attempt to learn move from defeated enemy
        10-15% base chance
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        # Only slimes can learn moves
        if companion.current_form != CompanionForm.SLIME:
            return {"success": False, "reason": "not_slime_yet"}

        # Roll learn chance (10-15%)
        learn_chance = random.uniform(0.10, 0.15)

        if random.random() < learn_chance:
            # Create move
            move = SlimeMove(
                move_id=f"move_{int(time.time())}_{random.randint(1000, 9999)}",
                name=enemy_move["name"],
                damage=enemy_move.get("damage", 20),
                element=enemy_move.get("element", "neutral"),
                mana_cost=enemy_move.get("mana_cost", 10),
                learned_from=enemy_move.get("enemy_name", "Unknown"),
                learned_at_timestamp=datetime.now()
            )

            # Check if moveset full
            if len(companion.moveset) >= companion.max_moves:
                return {
                    "success": True,
                    "learned": True,
                    "move": move.name,
                    "moveset_full": True,
                    "prompt": "Moveset ist voll! Welchen Move ersetzen?",
                    "current_moves": [m.name for m in companion.moveset]
                }

            companion.moveset.append(move)
            return {
                "success": True,
                "learned": True,
                "move": move.name,
                "learned_from": move.learned_from,
                "moveset_full": False,
                "message": f"Dein Slime hat '{move.name}' von {move.learned_from} gelernt!"
            }

        return {
            "success": True,
            "learned": False
        }

    def replace_move(self, companion_id: str, old_move_id: str, new_move: SlimeMove) -> Dict:
        """
        Replace an old move with a new one
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        # Find and replace move
        for i, move in enumerate(companion.moveset):
            if move.move_id == old_move_id:
                old_move_name = move.name
                companion.moveset[i] = new_move
                return {
                    "success": True,
                    "replaced": old_move_name,
                    "new_move": new_move.name
                }

        return {"success": False, "reason": "move_not_found"}

    def attempt_rescue(self, companion_id: str, hardcore_mode: bool) -> Dict:
        """
        Attempt to rescue player from death (1x/24h, Hardcore only)
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        # Only in hardcore mode
        if not hardcore_mode:
            return {"success": False, "reason": "not_hardcore_mode"}

        # Only slimes can rescue
        if companion.current_form != CompanionForm.SLIME:
            return {"success": False, "reason": "not_slime_yet"}

        # Check if rescue available
        if not companion.rescue_available:
            return {"success": False, "reason": "rescue_not_available"}

        # Check cooldown
        if companion.rescue_cooldown_until and datetime.now() < companion.rescue_cooldown_until:
            remaining = companion.rescue_cooldown_until - datetime.now()
            return {
                "success": False,
                "reason": "cooldown",
                "remaining_seconds": remaining.total_seconds(),
                "remaining_hours": remaining.total_seconds() / 3600
            }

        # Execute rescue!
        companion.rescue_available = False
        companion.rescue_cooldown_until = datetime.now() + timedelta(hours=24)
        companion.last_rescue_timestamp = datetime.now()
        companion.rescue_used_count_7d += 1

        return {
            "success": True,
            "rescued": True,
            "player_hp": 1,  # Player survives with 1 HP
            "cooldown_hours": 24,
            "cooldown_until": companion.rescue_cooldown_until.isoformat(),
            "message": "Dein Slime hat dich vor dem Tod gerettet!",
            "warning": "Rettung nur 1x pro 24 Stunden verfügbar!"
        }

    def update_companion(self, companion_id: str, delta_time: float) -> Dict:
        """
        Update companion state (needs decay, etc.)
        delta_time in seconds
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        # Update needs
        companion.needs.update(delta_time)
        companion.last_update = datetime.now()

        # Get current penalties
        penalties = companion.needs.get_penalties()

        return {
            "success": True,
            "needs": {
                "hunger": companion.needs.hunger,
                "thirst": companion.needs.thirst,
                "sleep": companion.needs.sleep,
                "mood": companion.needs.mood,
                "battle_lust": companion.needs.battle_lust
            },
            "penalties": penalties
        }

    def change_slime_color(self, companion_id: str, new_color: SlimeColor,
                          ritual_complete: bool = False) -> Dict:
        """
        Change slime color (requires ritual or color token)
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return {"success": False, "reason": "companion_not_found"}

        if companion.current_form != CompanionForm.SLIME:
            return {"success": False, "reason": "not_slime"}

        if not ritual_complete:
            return {"success": False, "reason": "ritual_not_complete"}

        # Change color
        old_color = companion.current_slime_color
        companion.current_slime_color = new_color

        # Add to collected colors if new
        if new_color not in companion.collected_colors:
            companion.collected_colors.append(new_color)

        # Check rainbow unlock (all 8 colors)
        rainbow_unlocked = len(companion.collected_colors) >= 8

        return {
            "success": True,
            "old_color": old_color.value if old_color else None,
            "new_color": new_color.value,
            "collected_colors": [c.value for c in companion.collected_colors],
            "total_collected": len(companion.collected_colors),
            "rainbow_unlocked": rainbow_unlocked,
            "message": f"Dein Slime hat die Farbe zu {new_color.value.title()} gewechselt!"
        }

    def get_companion_state(self, companion_id: str) -> Optional[Dict]:
        """
        Get full companion state
        """
        companion = self.companions.get(companion_id)
        if not companion:
            return None

        return {
            "companion_id": companion.companion_id,
            "player_id": companion.player_id,
            "form": companion.current_form.value,
            "level": companion.level,
            "xp": companion.xp,
            "xp_to_next_level": companion.xp_to_next_level,
            "animal": {
                "name": companion.animal.name,
                "type": companion.animal.type,
                "speed": companion.animal.speed
            } if companion.animal else None,
            "slime": {
                "unlocked": companion.slime_unlocked,
                "current_color": companion.current_slime_color.value if companion.current_slime_color else None,
                "collected_colors": [c.value for c in companion.collected_colors],
                "total_collected": len(companion.collected_colors),
                "rainbow_unlocked": len(companion.collected_colors) >= 8,
                "bonuses": self.SLIME_BONUSES.get(companion.current_slime_color, {}) if companion.current_slime_color else {}
            },
            "stats": {
                "hp": companion.hp,
                "max_hp": companion.max_hp,
                "attack": companion.attack,
                "defense": companion.defense,
                "speed": companion.speed
            },
            "needs": {
                "hunger": companion.needs.hunger,
                "thirst": companion.needs.thirst,
                "sleep": companion.needs.sleep,
                "mood": companion.needs.mood,
                "battle_lust": companion.needs.battle_lust,
                "penalties": companion.needs.get_penalties()
            },
            "moveset": [
                {
                    "id": m.move_id,
                    "name": m.name,
                    "damage": m.damage,
                    "element": m.element,
                    "mana_cost": m.mana_cost,
                    "learned_from": m.learned_from
                }
                for m in companion.moveset
            ],
            "rescue": {
                "available": companion.rescue_available,
                "cooldown_until": companion.rescue_cooldown_until.isoformat() if companion.rescue_cooldown_until else None,
                "used_count_7d": companion.rescue_used_count_7d
            },
            "combat_mode": companion.combat_mode.value,
            "created_at": companion.created_at.isoformat(),
            "last_update": companion.last_update.isoformat()
        }
