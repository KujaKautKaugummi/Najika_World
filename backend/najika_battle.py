"""
NAJIKA ENHANCED BATTLE SYSTEM
Full RPG Combat System für Dungeon-Kämpfe
"""

import random
import time
from typing import Dict, List, Optional

# ===== ENEMY DATABASE =====

ENEMY_DB = {
    # COMMON ENEMIES
    "rat": {
        "name": "Dungeon-Ratte",
        "hp": 20,
        "atk": 3,
        "def": 1,
        "gold": 5,
        "xp": 8,
        "loot_table": [
            {"item": "rat_tail", "chance": 0.3},
            {"item": "health_potion_small", "chance": 0.15}
        ]
    },
    "slime": {
        "name": "Schleim",
        "hp": 25,
        "atk": 4,
        "def": 2,
        "gold": 8,
        "xp": 12,
        "loot_table": [
            {"item": "slime_core", "chance": 0.25},
            {"item": "health_potion_small", "chance": 0.2}
        ]
    },
    "skeleton": {
        "name": "Skelett-Krieger",
        "hp": 35,
        "atk": 6,
        "def": 3,
        "gold": 12,
        "xp": 18,
        "loot_table": [
            {"item": "bone_shard", "chance": 0.4},
            {"item": "health_potion_medium", "chance": 0.15}
        ]
    },

    # ELITE ENEMIES
    "goblin_warrior": {
        "name": "Goblin-Krieger",
        "hp": 50,
        "atk": 8,
        "def": 4,
        "gold": 25,
        "xp": 35,
        "loot_table": [
            {"item": "goblin_blade", "chance": 0.2},
            {"item": "health_potion_medium", "chance": 0.25}
        ]
    },
    "dark_mage": {
        "name": "Dunkler Magier",
        "hp": 40,
        "atk": 12,
        "def": 2,
        "gold": 30,
        "xp": 40,
        "loot_table": [
            {"item": "dark_essence", "chance": 0.3},
            {"item": "mana_crystal", "chance": 0.2}
        ]
    },

    # BOSS ENEMIES
    "rat_king": {
        "name": "RATTEN-KOENIG",
        "hp": 150,
        "atk": 12,
        "def": 5,
        "gold": 100,
        "xp": 200,
        "loot_table": [
            {"item": "rat_king_crown", "chance": 1.0},
            {"item": "health_potion_large", "chance": 0.5}
        ],
        "boss": True,
        "special_abilities": ["summon_rats", "poison_cloud"]
    },
    "dungeon_lord": {
        "name": "DUNGEON-LORD",
        "hp": 300,
        "atk": 18,
        "def": 8,
        "gold": 500,
        "xp": 1000,
        "loot_table": [
            {"item": "dungeon_key", "chance": 1.0},
            {"item": "legendary_weapon", "chance": 0.3}
        ],
        "boss": True,
        "special_abilities": ["shadow_strike", "regenerate", "summon_minions"]
    }
}

# ===== ITEMS DATABASE =====

ITEM_DB = {
    # CONSUMABLES
    "health_potion_small": {
        "name": "Kleiner Heiltrank",
        "type": "consumable",
        "effect": "heal",
        "value": 30,
        "description": "Stellt 30 HP wieder her"
    },
    "health_potion_medium": {
        "name": "Mittlerer Heiltrank",
        "type": "consumable",
        "effect": "heal",
        "value": 60,
        "description": "Stellt 60 HP wieder her"
    },
    "health_potion_large": {
        "name": "Grosser Heiltrank",
        "type": "consumable",
        "effect": "heal",
        "value": 100,
        "description": "Stellt 100 HP wieder her"
    },
    "strength_buff": {
        "name": "Staerke-Elixier",
        "type": "consumable",
        "effect": "buff_atk",
        "value": 5,
        "duration": 3,
        "description": "+5 ATK fuer 3 Runden"
    },
    "defense_buff": {
        "name": "Verteidigungs-Elixier",
        "type": "consumable",
        "effect": "buff_def",
        "value": 3,
        "duration": 3,
        "description": "+3 DEF fuer 3 Runden"
    },

    # MATERIALS
    "rat_tail": {"name": "Rattenschwanz", "type": "material"},
    "slime_core": {"name": "Schleim-Kern", "type": "material"},
    "bone_shard": {"name": "Knochensplitter", "type": "material"},
    "dark_essence": {"name": "Dunkle Essenz", "type": "material"},
    "mana_crystal": {"name": "Mana-Kristall", "type": "material"},

    # SPECIAL
    "rat_king_crown": {"name": "Krone des Ratten-Koenigs", "type": "special"},
    "dungeon_key": {"name": "Dungeon-Schluessel", "type": "special"},

    # ===== EQUIPMENT (Digimon Story Style!) =====
    # WEAPONS
    "wooden_sword": {
        "name": "Holzschwert",
        "type": "weapon",
        "slot": "weapon",
        "atk_bonus": 3,
        "description": "Einfaches Holzschwert"
    },
    "iron_sword": {
        "name": "Eisenschwert",
        "type": "weapon",
        "slot": "weapon",
        "atk_bonus": 8,
        "description": "Solides Eisenschwert"
    },
    "goblin_blade": {
        "name": "Goblin-Klinge",
        "type": "weapon",
        "slot": "weapon",
        "atk_bonus": 12,
        "description": "Scharfe Goblin-Waffe"
    },
    "legendary_weapon": {
        "name": "Legendaere Waffe",
        "type": "weapon",
        "slot": "weapon",
        "atk_bonus": 25,
        "description": "Maechtige legendaere Waffe"
    },

    # ARMOR
    "leather_vest": {
        "name": "Lederweste",
        "type": "armor",
        "slot": "armor",
        "def_bonus": 2,
        "description": "Leichte Lederruestung"
    },
    "iron_armor": {
        "name": "Eisenruestung",
        "type": "armor",
        "slot": "armor",
        "def_bonus": 5,
        "description": "Schwere Eisenruestung"
    },
    "dragon_scale": {
        "name": "Drachenschuppen",
        "type": "armor",
        "slot": "armor",
        "def_bonus": 10,
        "description": "Undurchdringliche Drachenschuppen"
    },

    # ACCESSORIES
    "power_ring": {
        "name": "Kraftring",
        "type": "accessory",
        "slot": "accessory",
        "atk_bonus": 5,
        "description": "Ring der Staerke verleiht"
    },
    "defense_charm": {
        "name": "Schutzamulett",
        "type": "accessory",
        "slot": "accessory",
        "def_bonus": 5,
        "description": "Amulett das schuetzt"
    },
    "hp_boost": {
        "name": "HP-Boost",
        "type": "accessory",
        "slot": "accessory",
        "hp_bonus": 30,
        "description": "Erhoecht max HP um 30"
    },
    "mp_boost": {
        "name": "MP-Boost",
        "type": "accessory",
        "slot": "accessory",
        "mp_bonus": 20,
        "description": "Erhoecht max MP um 20"
    }
}

# ===== SKILL DATABASE =====

SKILL_DB = {
    "attack": {
        "name": "Normaler Angriff",
        "damage": 10,
        "cost": 0,
        "description": "Standard-Angriff",
        "learnable": False  # Grundskill, kann nicht gelernt werden
    },
    "heavy_attack": {
        "name": "Schwerer Schlag",
        "damage": 20,
        "cost": 10,
        "cooldown": 2,
        "description": "Maechtiger Angriff mit 2x Schaden",
        "learnable": True
    },
    "fire_blast": {
        "name": "Feuerball",
        "damage": 25,
        "cost": 15,
        "aoe": True,
        "cooldown": 3,
        "description": "AOE Feuer-Angriff trifft alle Gegner",
        "learnable": True
    },
    "heal": {
        "name": "Heilung",
        "heal": 40,
        "cost": 20,
        "cooldown": 3,
        "description": "Heilt 40 HP",
        "learnable": True
    },
    "defend": {
        "name": "Verteidigung",
        "defense_multiplier": 2.0,
        "cost": 0,
        "description": "Reduziert eingehenden Schaden um 50%",
        "learnable": False
    },
    "critical_strike": {
        "name": "Kritischer Schlag",
        "damage": 30,
        "crit_chance": 0.5,
        "cost": 15,
        "cooldown": 2,
        "description": "50% Chance auf kritischen Treffer (3x Schaden)",
        "learnable": True
    },
    # ENEMY-EXCLUSIVE SKILLS (Learnable from enemies!)
    "poison_bite": {
        "name": "Giftbiss",
        "damage": 8,
        "cost": 5,
        "dot_damage": 3,
        "dot_turns": 3,
        "description": "Vergiftet Gegner - 3 DMG pro Runde fuer 3 Runden",
        "learnable": True,
        "learn_from": ["rat", "slime"]
    },
    "bone_throw": {
        "name": "Knochen-Wurf",
        "damage": 15,
        "cost": 8,
        "description": "Wirft Knochen auf Gegner",
        "learnable": True,
        "learn_from": ["skeleton"]
    },
    "dark_bolt": {
        "name": "Dunkler Blitz",
        "damage": 20,
        "cost": 12,
        "description": "Schiesst dunkle Energie",
        "learnable": True,
        "learn_from": ["dark_mage"]
    },
    "summon_rats": {
        "name": "Ratten-Beschwörung",
        "cost": 15,
        "cooldown": 5,
        "description": "Beschwört 2 Ratten als Verbuendete (Boss-Skill)",
        "learnable": True,
        "learn_from": ["rat_king"]
    },
    "shadow_strike": {
        "name": "Schatten-Schlag",
        "damage": 35,
        "cost": 20,
        "cooldown": 3,
        "description": "Maechtige Dunkelheit (Boss-Skill)",
        "learnable": True,
        "learn_from": ["dungeon_lord"]
    }
}


class BattleSystem:
    def __init__(self):
        """Initialisiert das Battle System"""
        self.reset_battle()

    def reset_battle(self):
        """Reset Battle State"""
        self.battle_state = {
            "active": False,
            "player": {
                "hp": 100,
                "max_hp": 100,
                "mp": 50,
                "max_mp": 50,
                "atk": 10,
                "def": 5,
                "buffs": {},  # {buff_name: remaining_turns}
                "cooldowns": {},  # {skill_name: turns_remaining}
                "inventory": [],
                "known_skills": ["attack", "defend"]  # Start-Skills
            },
            "enemies": [],
            "wave": 0,
            "turn": 0,
            "gold_earned": 0,
            "xp_earned": 0,
            "loot": [],
            "skills_learned": [],  # Neu gelernte Skills in diesem Kampf
            "battle_log": []
        }

    def start_battle(self, dungeon_level: int = 1, boss_wave: int = 10):
        """Startet einen neuen Kampf"""
        self.reset_battle()
        self.battle_state["active"] = True
        self.battle_state["wave"] = 1
        self.battle_state["dungeon_level"] = dungeon_level
        self.battle_state["boss_wave"] = boss_wave

        self._spawn_enemies(1)
        self._log("KAMPF GESTARTET! Wave 1 beginnt!")

        return self.get_battle_status()

    def _spawn_enemies(self, wave: int):
        """Spawnt Enemies basierend auf Wave"""
        enemies = []

        # Boss Wave?
        if wave % self.battle_state.get("boss_wave", 10) == 0:
            boss_type = "rat_king" if wave < 20 else "dungeon_lord"
            enemies.append(self._create_enemy(boss_type))
            self._log(f"BOSS ERSCHEINT: {enemies[0]['name']}!")
        else:
            # Normale Wave: Schwierigkeit steigt mit Wave
            enemy_count = min(5, 2 + wave // 3)

            # Enemy-Pool basierend auf Wave
            if wave < 5:
                pool = ["rat", "slime"]
            elif wave < 10:
                pool = ["rat", "slime", "skeleton"]
            elif wave < 15:
                pool = ["skeleton", "goblin_warrior"]
            else:
                pool = ["goblin_warrior", "dark_mage"]

            for _ in range(enemy_count):
                enemy_type = random.choice(pool)
                enemies.append(self._create_enemy(enemy_type))

        self.battle_state["enemies"] = enemies
        self._log(f"Wave {wave}: {len(enemies)} Gegner erscheinen!")

    def _create_enemy(self, enemy_type: str) -> Dict:
        """Erstellt einen Enemy aus der DB"""
        template = ENEMY_DB[enemy_type]
        return {
            "type": enemy_type,
            "name": template["name"],
            "hp": template["hp"],
            "max_hp": template["hp"],
            "atk": template["atk"],
            "def": template["def"],
            "gold": template["gold"],
            "xp": template["xp"],
            "loot_table": template.get("loot_table", []),
            "boss": template.get("boss", False),
            "special_abilities": template.get("special_abilities", [])
        }

    def player_action(self, action: str, target_index: int = 0, **kwargs):
        """
        Führt Spieler-Aktion aus

        Args:
            action: "attack", "skill", "item", "defend", "flee"
            target_index: Index des Ziel-Gegners
            **kwargs: Zusätzliche Parameter (skill_name, item_name, etc.)
        """
        if not self.battle_state["active"]:
            return {"ok": False, "msg": "Kein aktiver Kampf!"}

        result = None

        if action == "attack":
            result = self._player_attack(target_index)
        elif action == "skill":
            skill_name = kwargs.get("skill_name")
            result = self._player_skill(skill_name, target_index)
        elif action == "item":
            item_name = kwargs.get("item_name")
            result = self._player_use_item(item_name)
        elif action == "defend":
            result = self._player_defend()
        elif action == "flee":
            result = self._player_flee()
        else:
            return {"ok": False, "msg": "Ungueltige Aktion!"}

        # Nach Spieler-Aktion: Enemy Turn
        if result.get("ok") and self.battle_state["active"]:
            self._enemy_turn()
            self._update_buffs()
            self._update_cooldowns()
            self.battle_state["turn"] += 1

        # Check Win/Loss
        self._check_battle_end()

        return self.get_battle_status()

    def _player_attack(self, target_index: int):
        """Standard-Angriff"""
        enemies = self.battle_state["enemies"]
        if target_index >= len(enemies):
            return {"ok": False, "msg": "Ungültiges Ziel!"}

        player = self.battle_state["player"]
        enemy = enemies[target_index]

        # Schaden berechnen
        base_damage = player["atk"]
        damage = max(1, base_damage - enemy["def"])

        # Anwenden
        enemy["hp"] -= damage
        self._log(f"Du greifst {enemy['name']} an! -{damage} HP")

        # Gegner tot?
        if enemy["hp"] <= 0:
            self._enemy_defeated(target_index)

        return {"ok": True}

    def _player_skill(self, skill_name: str, target_index: int):
        """Skill-Angriff"""
        if skill_name not in SKILL_DB:
            return {"ok": False, "msg": "Unbekannter Skill!"}

        skill = SKILL_DB[skill_name]
        player = self.battle_state["player"]

        # Check Cooldown
        if skill_name in player["cooldowns"] and player["cooldowns"][skill_name] > 0:
            return {"ok": False, "msg": f"{skill['name']} ist auf Cooldown!"}

        # Check MP Cost
        cost = skill.get("cost", 0)
        if player["mp"] < cost:
            return {"ok": False, "msg": "Nicht genug MP!"}

        player["mp"] -= cost

        # Skill Effekt
        if "damage" in skill:
            if skill.get("aoe"):
                # AOE Skill
                damage = skill["damage"]
                for enemy in self.battle_state["enemies"]:
                    dmg_dealt = max(1, damage - enemy["def"])
                    enemy["hp"] -= dmg_dealt
                self._log(f"Du nutzt {skill['name']}! AOE Schaden!")

                # Tote Gegner entfernen
                self._remove_dead_enemies()
            else:
                # Single Target
                enemies = self.battle_state["enemies"]
                if target_index >= len(enemies):
                    return {"ok": False, "msg": "Ungültiges Ziel!"}

                enemy = enemies[target_index]
                damage = skill["damage"]

                # Crit Check
                if skill.get("crit_chance", 0) > random.random():
                    damage *= 3
                    self._log(f"KRITISCHER TREFFER!")

                dmg_dealt = max(1, damage - enemy["def"])
                enemy["hp"] -= dmg_dealt
                self._log(f"Du nutzt {skill['name']}! -{dmg_dealt} HP")

                if enemy["hp"] <= 0:
                    self._enemy_defeated(target_index)

        elif "heal" in skill:
            # Heal Skill
            heal_amount = skill["heal"]
            old_hp = player["hp"]
            player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
            healed = player["hp"] - old_hp
            self._log(f"Du nutzt {skill['name']}! +{healed} HP")

        # Set Cooldown
        if "cooldown" in skill:
            player["cooldowns"][skill_name] = skill["cooldown"]

        return {"ok": True}

    def _player_use_item(self, item_name: str):
        """Item benutzen"""
        player = self.battle_state["player"]

        if item_name not in player["inventory"]:
            return {"ok": False, "msg": "Item nicht vorhanden!"}

        if item_name not in ITEM_DB:
            return {"ok": False, "msg": "Unbekanntes Item!"}

        item = ITEM_DB[item_name]

        if item.get("effect") == "heal":
            heal_amount = item.get("value", 0)
            old_hp = player["hp"]
            player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
            healed = player["hp"] - old_hp
            self._log(f"Du nutzt {item['name']}! +{healed} HP")

        elif item.get("effect") == "buff_atk":
            player["buffs"]["atk_buff"] = item.get("duration", 3)
            player["atk"] += item.get("value", 0)
            self._log(f"Du nutzt {item['name']}! +{item['value']} ATK")

        elif item.get("effect") == "buff_def":
            player["buffs"]["def_buff"] = item.get("duration", 3)
            player["def"] += item.get("value", 0)
            self._log(f"Du nutzt {item['name']}! +{item['value']} DEF")

        # Entferne Item
        player["inventory"].remove(item_name)

        return {"ok": True}

    def _player_defend(self):
        """Verteidigungshaltung"""
        self.battle_state["player"]["buffs"]["defending"] = 1
        self._log("Du nimmst Verteidigungshaltung ein!")
        return {"ok": True}

    def _player_flee(self):
        """Flucht-Versuch"""
        # 50% Flucht-Chance (bei Bossen niedriger)
        has_boss = any(e.get("boss") for e in self.battle_state["enemies"])
        flee_chance = 0.3 if has_boss else 0.5

        if random.random() < flee_chance:
            self._log("Flucht erfolgreich!")
            self.battle_state["active"] = False
            return {"ok": True, "fled": True}
        else:
            self._log("Flucht fehlgeschlagen!")
            return {"ok": True, "fled": False}

    def _enemy_turn(self):
        """Gegner-Aktion"""
        player = self.battle_state["player"]

        for enemy in self.battle_state["enemies"]:
            if enemy["hp"] <= 0:
                continue

            # Boss Special Abilities
            if enemy.get("boss") and random.random() < 0.3:
                ability = random.choice(enemy["special_abilities"])
                self._enemy_special_ability(enemy, ability)
            else:
                # Normaler Angriff
                damage = enemy["atk"]

                # Verteidigung?
                if "defending" in player["buffs"]:
                    damage = damage // 2

                damage = max(1, damage - player["def"])
                player["hp"] -= damage
                self._log(f"{enemy['name']} greift an! -{damage} HP")

    def _enemy_special_ability(self, enemy: Dict, ability: str):
        """Boss Special Abilities"""
        if ability == "summon_rats":
            # Spawne 2 Ratten
            for _ in range(2):
                self.battle_state["enemies"].append(self._create_enemy("rat"))
            self._log(f"{enemy['name']} beschwört Ratten!")

        elif ability == "poison_cloud":
            # Giftschaden
            self.battle_state["player"]["hp"] -= 5
            self._log(f"{enemy['name']} setzt Giftgas frei! -5 HP")

        elif ability == "regenerate":
            # Heilt sich selbst
            heal = min(30, enemy["max_hp"] - enemy["hp"])
            enemy["hp"] += heal
            self._log(f"{enemy['name']} regeneriert! +{heal} HP")

        elif ability == "shadow_strike":
            # Starker Angriff
            damage = enemy["atk"] * 2
            damage = max(1, damage - self.battle_state["player"]["def"])
            self.battle_state["player"]["hp"] -= damage
            self._log(f"{enemy['name']} nutzt Schatten-Schlag! -{damage} HP")

    def _enemy_defeated(self, enemy_index: int):
        """Enemy wurde besiegt - Loot droppen + Skill Learning (Digimon World Style)"""
        enemy = self.battle_state["enemies"][enemy_index]

        # Gold & XP
        self.battle_state["gold_earned"] += enemy["gold"]
        self.battle_state["xp_earned"] += enemy["xp"]

        # Loot
        for loot_entry in enemy["loot_table"]:
            if random.random() < loot_entry["chance"]:
                self.battle_state["loot"].append(loot_entry["item"])
                item = ITEM_DB[loot_entry["item"]]
                self._log(f"Loot: {item['name']}")

        # ===== SKILL LEARNING (DIGIMON WORLD STYLE) =====
        # Chance Skills vom Gegner zu lernen
        enemy_type = enemy["type"]
        is_boss = enemy.get("boss", False)

        # Boss: 20% Chance, Normal: 8% Chance
        learn_chance = 0.20 if is_boss else 0.08

        if random.random() < learn_chance:
            # Finde lernbare Skills von diesem Enemy-Typ
            learnable_skills = []
            for skill_name, skill_data in SKILL_DB.items():
                if skill_data.get("learnable") and enemy_type in skill_data.get("learn_from", []):
                    # Prüfe ob Skill noch nicht bekannt ist
                    if skill_name not in self.battle_state["player"]["known_skills"]:
                        learnable_skills.append(skill_name)

            # Lerne einen zufälligen Skill
            if learnable_skills:
                learned_skill = random.choice(learnable_skills)
                self.battle_state["player"]["known_skills"].append(learned_skill)
                self.battle_state["skills_learned"].append(learned_skill)

                skill_name_display = SKILL_DB[learned_skill]["name"]
                self._log(f"*** NAJIKA HAT [{skill_name_display}] GELERNT! ***")

        self._log(f"{enemy['name']} wurde besiegt! +{enemy['gold']} Gold, +{enemy['xp']} XP")

        # Entferne Enemy
        self.battle_state["enemies"].pop(enemy_index)

    def _remove_dead_enemies(self):
        """Entfernt alle toten Gegner"""
        alive_enemies = []
        for i, enemy in enumerate(self.battle_state["enemies"]):
            if enemy["hp"] <= 0:
                self._enemy_defeated(i)
            else:
                alive_enemies.append(enemy)
        self.battle_state["enemies"] = alive_enemies

    def _update_buffs(self):
        """Reduziert Buff-Dauer"""
        player = self.battle_state["player"]
        expired_buffs = []

        for buff_name, duration in player["buffs"].items():
            player["buffs"][buff_name] = duration - 1
            if player["buffs"][buff_name] <= 0:
                expired_buffs.append(buff_name)

        for buff in expired_buffs:
            del player["buffs"][buff]
            # Reset Stat-Buffs
            if buff == "atk_buff":
                player["atk"] -= 5  # Hardcoded für jetzt
            elif buff == "def_buff":
                player["def"] -= 3

    def _update_cooldowns(self):
        """Reduziert Skill-Cooldowns"""
        player = self.battle_state["player"]
        for skill_name in list(player["cooldowns"].keys()):
            player["cooldowns"][skill_name] -= 1
            if player["cooldowns"][skill_name] <= 0:
                del player["cooldowns"][skill_name]

    def _check_battle_end(self):
        """Prüft ob Kampf vorbei ist (Win/Loss/Next Wave)"""
        player = self.battle_state["player"]

        # Player tot?
        if player["hp"] <= 0:
            self._log("NIEDERLAGE! Du wurdest besiegt...")
            self.battle_state["active"] = False
            self.battle_state["result"] = "defeat"
            return

        # Alle Gegner tot?
        if len(self.battle_state["enemies"]) == 0:
            wave = self.battle_state["wave"]

            # Nächste Wave spawnen
            self.battle_state["wave"] += 1
            self._spawn_enemies(self.battle_state["wave"])

    def _log(self, message: str):
        """Fügt Message zum Battle-Log hinzu"""
        self.battle_state["battle_log"].append({
            "turn": self.battle_state["turn"],
            "msg": message,
            "timestamp": time.time()
        })

        # Behalte nur letzte 20 Einträge
        if len(self.battle_state["battle_log"]) > 20:
            self.battle_state["battle_log"].pop(0)

    def get_battle_status(self) -> Dict:
        """Gibt aktuellen Battle-Status zurück"""
        return {
            "active": self.battle_state["active"],
            "player": self.battle_state["player"],
            "enemies": [
                {
                    "name": e["name"],
                    "hp": e["hp"],
                    "max_hp": e["max_hp"],
                    "boss": e.get("boss", False)
                }
                for e in self.battle_state["enemies"]
            ],
            "wave": self.battle_state["wave"],
            "turn": self.battle_state["turn"],
            "gold_earned": self.battle_state["gold_earned"],
            "xp_earned": self.battle_state["xp_earned"],
            "loot": self.battle_state["loot"],
            "skills_learned": self.battle_state.get("skills_learned", []),  # Gelernte Skills
            "battle_log": self.battle_state["battle_log"][-5:],  # Nur letzte 5
            "result": self.battle_state.get("result")
        }

    def get_available_skills(self) -> List[Dict]:
        """Gibt verfügbare Skills zurück (nur bekannte Skills!)"""
        player = self.battle_state["player"]
        known_skills = player.get("known_skills", ["attack", "defend"])
        skills = []

        for skill_name in known_skills:
            if skill_name not in SKILL_DB:
                continue

            skill = SKILL_DB[skill_name]
            available = True
            reason = ""

            # Check Cooldown
            if skill_name in player["cooldowns"] and player["cooldowns"][skill_name] > 0:
                available = False
                reason = f"Cooldown: {player['cooldowns'][skill_name]} Runden"

            # Check MP
            cost = skill.get("cost", 0)
            if player["mp"] < cost:
                available = False
                reason = "Nicht genug MP"

            skills.append({
                "name": skill_name,
                "display_name": skill["name"],
                "description": skill["description"],
                "cost": cost,
                "available": available,
                "reason": reason
            })

        return skills


# Global Instance
BATTLE_SYSTEM = BattleSystem()


# Test-Funktion
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA BATTLE SYSTEM TEST")
    print("=" * 60)

    battle = BattleSystem()

    # Starte Kampf
    status = battle.start_battle(dungeon_level=1)
    print(f"\n[WAVE {status['wave']}]")
    print(f"Gegner: {len(status['enemies'])}")
    for i, enemy in enumerate(status["enemies"]):
        print(f"  {i+1}. {enemy['name']} ({enemy['hp']}/{enemy['max_hp']} HP)")

    # Simuliere ein paar Runden
    for turn in range(5):
        print(f"\n[TURN {turn + 1}]")

        # Spieler greift an
        status = battle.player_action("attack", target_index=0)

        print(f"Player HP: {status['player']['hp']}/{status['player']['max_hp']}")
        print(f"Player MP: {status['player']['mp']}/{status['player']['max_mp']}")
        print(f"Gegner: {len(status['enemies'])}")

        # Battle Log
        for log_entry in status["battle_log"]:
            print(f"  LOG: {log_entry['msg']}")

        if not status["active"]:
            print(f"\n[KAMPF BEENDET]")
            print(f"Ergebnis: {status.get('result', 'unknown')}")
            print(f"Gold: {status['gold_earned']}")
            print(f"XP: {status['xp_earned']}")
            print(f"Loot: {status['loot']}")
            break

    print("\n" + "=" * 60)
    print("TEST ABGESCHLOSSEN")
    print("=" * 60)
