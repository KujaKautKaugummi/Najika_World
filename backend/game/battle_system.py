"""
Najika Battle System - Backend
Handles combat logic, enemy AI, and battle state
"""

import random
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Enemy:
    """Enemy entity"""
    id: str
    name: str
    level: int
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    loot_table: List[str] = field(default_factory=list)
    state: str = "idle"  # idle, attacking, dodging, stunned, dead
    ai_pattern: str = "aggressive"  # aggressive, defensive, balanced


@dataclass
class BattleState:
    """Current battle state"""
    active: bool = False
    enemies: List[Enemy] = field(default_factory=list)
    wave: int = 0
    turn: int = 0
    player_hp: int = 100
    player_max_hp: int = 100
    combat_mode: str = "action"  # action or cheer
    cheer_meter: int = 0  # 0-100 (cheer mode only)
    najika_state: str = "idle"  # For cheer timing
    last_action_time: float = 0.0


class BattleSystem:
    """Main battle system controller"""

    def __init__(self):
        self.state = BattleState()
        self.enemy_templates = self._load_enemy_templates()

    def _load_enemy_templates(self) -> Dict[str, Dict]:
        """Load enemy templates"""
        return {
            "rat": {
                "name": "Giant Rat",
                "level": 1,
                "hp": 30,
                "attack": 5,
                "defense": 2,
                "speed": 8,
                "loot": ["rat_tail", "small_coin"],
                "ai": "aggressive"
            },
            "skeleton": {
                "name": "Skeleton Warrior",
                "level": 3,
                "hp": 60,
                "attack": 12,
                "defense": 8,
                "speed": 6,
                "loot": ["bone", "rusty_sword", "medium_coin"],
                "ai": "balanced"
            },
            "slime": {
                "name": "Blue Slime",
                "level": 2,
                "hp": 45,
                "attack": 8,
                "defense": 15,
                "speed": 4,
                "loot": ["slime_gel", "small_coin"],
                "ai": "defensive"
            },
            "ghost": {
                "name": "Shadow Ghost",
                "level": 5,
                "hp": 50,
                "attack": 18,
                "defense": 5,
                "speed": 12,
                "loot": ["ectoplasm", "cursed_gem", "large_coin"],
                "ai": "aggressive"
            },
            "boss_rat_king": {
                "name": "Rat King",
                "level": 10,
                "hp": 200,
                "attack": 25,
                "defense": 12,
                "speed": 10,
                "loot": ["rat_crown", "gold_coin", "rare_item"],
                "ai": "balanced"
            }
        }

    def start_battle(self, enemy_types: List[str], combat_mode: str = "action") -> Dict:
        """Start a new battle"""
        self.state.active = True
        self.state.wave += 1
        self.state.turn = 0
        self.state.combat_mode = combat_mode
        self.state.enemies = []

        # Spawn enemies
        for i, enemy_type in enumerate(enemy_types):
            template = self.enemy_templates.get(enemy_type)
            if template:
                enemy = Enemy(
                    id=f"{enemy_type}_{i}",
                    name=template["name"],
                    level=template["level"],
                    hp=template["hp"],
                    max_hp=template["hp"],
                    attack=template["attack"],
                    defense=template["defense"],
                    speed=template["speed"],
                    loot_table=template["loot"],
                    ai_pattern=template["ai"]
                )
                self.state.enemies.append(enemy)

        return {
            "success": True,
            "battle_id": f"battle_{int(time.time())}",
            "wave": self.state.wave,
            "enemies": [self._enemy_to_dict(e) for e in self.state.enemies],
            "combat_mode": combat_mode
        }

    def player_attack(self, attack_type: str, target_id: str, combo_data: Optional[Dict] = None) -> Dict:
        """Process player attack"""
        enemy = self._get_enemy_by_id(target_id)
        if not enemy:
            return {"success": False, "reason": "invalid_target"}

        if enemy.state == "dead":
            return {"success": False, "reason": "target_dead"}

        # Calculate damage
        base_damage = {
            "light": 10,
            "heavy": 25,
            "combo_triple_strike": 50,
            "combo_smash": 80,
            "combo_riposte": 120,
            "combo_counter": 60
        }.get(attack_type, 10)

        # Apply combo bonus if present
        if combo_data and combo_data.get("active"):
            base_damage = combo_data.get("damage", base_damage)

        # Apply cheer bonus (cheer mode only)
        if self.state.combat_mode == "cheer":
            cheer_bonus = self.state.cheer_meter / 100 * 0.25  # Max +25% at 100 cheer
            base_damage = int(base_damage * (1 + cheer_bonus))

        # Random variance
        damage = int(base_damage * random.uniform(0.9, 1.1))

        # Apply defense
        damage = max(1, damage - enemy.defense)

        # Deal damage
        enemy.hp = max(0, enemy.hp - damage)

        # Check death
        if enemy.hp <= 0:
            enemy.state = "dead"
            loot = self._roll_loot(enemy)

            # Check battle end
            if all(e.state == "dead" for e in self.state.enemies):
                return self._end_battle(victory=True, damage=damage, loot=loot)

        return {
            "success": True,
            "damage": damage,
            "target": self._enemy_to_dict(enemy),
            "battle_state": self.get_state()
        }

    def enemy_turn(self) -> Dict:
        """Process enemy attacks (autonomous in cheer mode, or after player action)"""
        results = []

        for enemy in self.state.enemies:
            if enemy.state == "dead":
                continue

            # AI decision based on pattern
            action = self._enemy_ai_decision(enemy)

            if action == "attack":
                # Update Najika state (for cheer timing)
                if self.state.combat_mode == "cheer":
                    self.state.najika_state = "dodging"

                # Calculate damage
                damage = int(enemy.attack * random.uniform(0.8, 1.2))
                self.state.player_hp = max(0, self.state.player_hp - damage)

                results.append({
                    "enemy_id": enemy.id,
                    "action": "attack",
                    "damage": damage,
                    "player_hp": self.state.player_hp
                })

                # Check player death
                if self.state.player_hp <= 0:
                    return self._end_battle(victory=False)

            elif action == "defend":
                enemy.state = "blocking"
                results.append({
                    "enemy_id": enemy.id,
                    "action": "defend"
                })

        self.state.turn += 1
        return {
            "success": True,
            "turn": self.state.turn,
            "enemy_actions": results,
            "battle_state": self.get_state()
        }

    def _enemy_ai_decision(self, enemy: Enemy) -> str:
        """AI decision making"""
        hp_percent = enemy.hp / enemy.max_hp

        if enemy.ai_pattern == "aggressive":
            return "attack" if random.random() > 0.2 else "defend"

        elif enemy.ai_pattern == "defensive":
            if hp_percent < 0.3:
                return "defend" if random.random() > 0.3 else "attack"
            return "attack" if random.random() > 0.4 else "defend"

        else:  # balanced
            if hp_percent < 0.5:
                return "defend" if random.random() > 0.5 else "attack"
            return "attack" if random.random() > 0.3 else "defend"

    def update_cheer_meter(self, change: int) -> Dict:
        """Update cheer meter (cheer mode only)"""
        if self.state.combat_mode != "cheer":
            return {"success": False, "reason": "not_in_cheer_mode"}

        self.state.cheer_meter = max(0, min(100, self.state.cheer_meter + change))

        return {
            "success": True,
            "cheer_meter": self.state.cheer_meter,
            "special_ready": self.state.cheer_meter >= 100
        }

    def update_najika_state(self, new_state: str) -> Dict:
        """Update Najika's combat state (for cheer timing)"""
        self.state.najika_state = new_state
        self.state.last_action_time = time.time()

        return {
            "success": True,
            "najika_state": new_state,
            "timestamp": self.state.last_action_time
        }

    def use_special_finisher(self) -> Dict:
        """Use special finisher (cheer meter at 100)"""
        if self.state.cheer_meter < 100:
            return {"success": False, "reason": "cheer_meter_not_full"}

        # Reset cheer meter
        self.state.cheer_meter = 0

        # Massive damage to all enemies
        damage = 300
        results = []

        for enemy in self.state.enemies:
            if enemy.state == "dead":
                continue

            enemy.hp = max(0, enemy.hp - damage)
            if enemy.hp <= 0:
                enemy.state = "dead"

            results.append({
                "enemy_id": enemy.id,
                "damage": damage,
                "hp": enemy.hp,
                "dead": enemy.state == "dead"
            })

        # Check battle end
        if all(e.state == "dead" for e in self.state.enemies):
            return self._end_battle(victory=True, special_used=True)

        return {
            "success": True,
            "type": "special_finisher",
            "damage": damage,
            "results": results,
            "cheer_meter": 0,
            "battle_state": self.get_state()
        }

    def _roll_loot(self, enemy: Enemy) -> List[str]:
        """Roll for loot drops"""
        loot = []
        for item in enemy.loot_table:
            if random.random() > 0.5:  # 50% drop rate
                loot.append(item)
        return loot

    def _end_battle(self, victory: bool, damage: int = 0, loot: List[str] = None, special_used: bool = False) -> Dict:
        """End the battle"""
        self.state.active = False

        # Collect all loot
        all_loot = loot or []
        if victory:
            for enemy in self.state.enemies:
                if enemy.state == "dead":
                    all_loot.extend(self._roll_loot(enemy))

        return {
            "success": True,
            "battle_end": True,
            "victory": victory,
            "wave": self.state.wave,
            "turns": self.state.turn,
            "loot": all_loot,
            "special_used": special_used,
            "player_hp": self.state.player_hp
        }

    def _get_enemy_by_id(self, enemy_id: str) -> Optional[Enemy]:
        """Get enemy by ID"""
        for enemy in self.state.enemies:
            if enemy.id == enemy_id:
                return enemy
        return None

    def _enemy_to_dict(self, enemy: Enemy) -> Dict:
        """Convert enemy to dict"""
        return {
            "id": enemy.id,
            "name": enemy.name,
            "level": enemy.level,
            "hp": enemy.hp,
            "max_hp": enemy.max_hp,
            "attack": enemy.attack,
            "defense": enemy.defense,
            "speed": enemy.speed,
            "state": enemy.state
        }

    def get_state(self) -> Dict:
        """Get current battle state"""
        return {
            "active": self.state.active,
            "wave": self.state.wave,
            "turn": self.state.turn,
            "combat_mode": self.state.combat_mode,
            "cheer_meter": self.state.cheer_meter,
            "najika_state": self.state.najika_state,
            "player_hp": self.state.player_hp,
            "player_max_hp": self.state.player_max_hp,
            "enemies": [self._enemy_to_dict(e) for e in self.state.enemies],
            "enemies_alive": sum(1 for e in self.state.enemies if e.state != "dead")
        }

    def reset(self):
        """Reset battle system"""
        self.state = BattleState()
