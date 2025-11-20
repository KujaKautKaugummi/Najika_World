#!/usr/bin/env python3
"""
NAJIKA GAME ACTIONS - Autonome Spielaktionen
Najika kann selbstständig in der Spielwelt agieren!

Features:
- Autonomes Crafting basierend auf Bedürfnissen
- Autonomes Gärtnern (Farming)
- Autonomes Kochen
- Autonomes Erkunden (Teleport zu Locations)
- Resource Gathering
- Smart Actions basierend auf Hunger/Energy/Mood
"""

import time
import random
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

# ═════════════════════════════════════════════════════════════════
# GAME ACTION DEFINITIONEN
# ═════════════════════════════════════════════════════════════════

# Locations/Teleport Ziele
LOCATIONS = {
    "home": {
        "name": "Schwarze Windmühle (Zuhause)",
        "description": "Mein gemütliches Zuhause mit Kuja 💜",
        "activities": ["cooking", "crafting", "sleeping", "reading"],
        "safe": True
    },
    "farm": {
        "name": "Najika's Garten",
        "description": "Hier pflanze ich Gemüse und Früchte! 🌱",
        "activities": ["farming", "fishing", "gathering"],
        "safe": True
    },
    "forest": {
        "name": "Mystischer Wald",
        "description": "Voller Ressourcen und Geheimnisse! 🌲",
        "activities": ["gathering", "exploring", "hunting"],
        "safe": False
    },
    "dungeon": {
        "name": "Dungeon im Keller",
        "description": "Gefährlich aber spannend! 🗝️",
        "activities": ["exploring", "combat", "treasure_hunting"],
        "safe": False
    },
    "village": {
        "name": "Dorf",
        "description": "Hier kann ich einkaufen und Leute treffen! 🏘️",
        "activities": ["shopping", "quests", "socializing"],
        "safe": True
    },
    "training_ground": {
        "name": "Trainingsplatz",
        "description": "Hier werde ich stärker! 💪",
        "activities": ["training", "combat", "meditation"],
        "safe": True
    }
}

# Cooking Recipes
COOKING_RECIPES = {
    "simple_meal": {
        "name": "Einfaches Essen",
        "materials": [{"id": "wheat", "count": 2}],
        "hunger_restore": 30,
        "energy_cost": 5,
        "cooking_time": 300,  # 5 Min
        "mood_bonus": 5,
        "description": "Schnell gemacht, sättigt okay"
    },
    "hearty_meal": {
        "name": "Herzhaftes Essen",
        "materials": [
            {"id": "wheat", "count": 2},
            {"id": "potato", "count": 3},
            {"id": "carrot", "count": 2}
        ],
        "hunger_restore": 60,
        "energy_cost": 10,
        "cooking_time": 600,  # 10 Min
        "mood_bonus": 15,
        "description": "Lecker und sättigend! 😋"
    },
    "gourmet_meal": {
        "name": "Gourmet Essen",
        "materials": [
            {"id": "corn", "count": 2},
            {"id": "tomato", "count": 3},
            {"id": "lettuce", "count": 2},
            {"id": "fish", "count": 1}
        ],
        "hunger_restore": 100,
        "energy_cost": 15,
        "cooking_time": 900,  # 15 Min
        "mood_bonus": 30,
        "description": "Meisterwerk! Für Kuja gekocht! 💜✨"
    },
    "snack": {
        "name": "Snack",
        "materials": [{"id": "strawberry", "count": 3}],
        "hunger_restore": 15,
        "energy_cost": 2,
        "cooking_time": 60,  # 1 Min
        "mood_bonus": 5,
        "description": "Kleiner Hunger-Killer"
    },
    "energy_drink": {
        "name": "Energy Drink",
        "materials": [
            {"id": "strawberry", "count": 5},
            {"id": "water", "count": 1}
        ],
        "hunger_restore": 10,
        "energy_restore": 40,
        "energy_cost": 5,
        "cooking_time": 180,  # 3 Min
        "mood_bonus": 10,
        "description": "Gibt Energie zurück! ⚡"
    }
}

# Crafting Recipes für autonomes Craften
AUTONOMOUS_CRAFTING_RECIPES = {
    "gift_for_kuja": {
        "name": "Geschenk für Kuja 💜",
        "materials": [
            {"id": "wood", "count": 3},
            {"id": "flower", "count": 5}
        ],
        "craft_time": 600,  # 10 Min
        "energy_cost": 10,
        "mood_bonus": 20,
        "description": "Ein besonderes Geschenk für Kuja! 💜✨",
        "trigger_condition": "mood > 70 and energy > 50"
    },
    "health_potion": {
        "name": "Health Potion",
        "materials": [
            {"id": "herb", "count": 3},
            {"id": "water", "count": 1}
        ],
        "craft_time": 300,  # 5 Min
        "energy_cost": 5,
        "description": "Heilt HP",
        "trigger_condition": "health < 50"
    },
    "mana_potion": {
        "name": "Mana Potion",
        "materials": [
            {"id": "herb", "count": 2},
            {"id": "flower", "count": 2}
        ],
        "craft_time": 300,  # 5 Min
        "energy_cost": 5,
        "description": "Stellt Mana wieder her",
        "trigger_condition": "mana < 50"
    },
    "tool_repair": {
        "name": "Werkzeug Reparatur",
        "materials": [
            {"id": "wood", "count": 2},
            {"id": "stone", "count": 3}
        ],
        "craft_time": 400,  # 7 Min
        "energy_cost": 8,
        "description": "Repariert kaputte Tools",
        "trigger_condition": "tools_broken"
    }
}

# Farming Actions
FARMING_ACTIONS = {
    "plant_crops": {
        "name": "Pflanzen anbauen",
        "duration": 300,  # 5 Min
        "energy_cost": 10,
        "crops": ["wheat", "potato", "carrot", "tomato"],
        "description": "Ich pflanze Gemüse im Garten! 🌱"
    },
    "water_crops": {
        "name": "Pflanzen gießen",
        "duration": 180,  # 3 Min
        "energy_cost": 5,
        "description": "Ich gieße meine Pflanzen! 💧"
    },
    "harvest_crops": {
        "name": "Ernten",
        "duration": 240,  # 4 Min
        "energy_cost": 8,
        "description": "Ernte-Zeit! Ich bin so stolz! 😊✨"
    },
    "fertilize": {
        "name": "Düngen",
        "duration": 200,  # 3.3 Min
        "energy_cost": 6,
        "description": "Damit die Pflanzen schneller wachsen! 🌿"
    }
}

# Exploring/Gathering Actions
EXPLORING_ACTIONS = {
    "gather_wood": {
        "name": "Holz sammeln",
        "location": "forest",
        "duration": 600,  # 10 Min
        "energy_cost": 15,
        "resources": [{"id": "wood", "min": 3, "max": 8}],
        "description": "Ich sammle Holz im Wald! 🪵"
    },
    "gather_herbs": {
        "name": "Kräuter sammeln",
        "location": "forest",
        "duration": 400,  # 7 Min
        "energy_cost": 10,
        "resources": [{"id": "herb", "min": 2, "max": 6}],
        "description": "Heilkräuter für Tränke! 🌿"
    },
    "gather_flowers": {
        "name": "Blumen pflücken",
        "location": "forest",
        "duration": 300,  # 5 Min
        "energy_cost": 5,
        "resources": [{"id": "flower", "min": 5, "max": 12}],
        "description": "Blumen für Kuja! 💐"
    },
    "mine_stone": {
        "name": "Steine abbauen",
        "location": "dungeon",
        "duration": 800,  # 13 Min
        "energy_cost": 20,
        "resources": [
            {"id": "stone", "min": 5, "max": 10},
            {"id": "ore", "min": 1, "max": 3}
        ],
        "description": "Ich baue Steine ab! 💎⛏️"
    },
    "explore_dungeon": {
        "name": "Dungeon erkunden",
        "location": "dungeon",
        "duration": 1200,  # 20 Min
        "energy_cost": 25,
        "resources": [
            {"id": "treasure", "min": 1, "max": 2},
            {"id": "gold", "min": 50, "max": 150}
        ],
        "description": "Schatzsuche! *aufgeregt* ✨🗝️"
    },
    "fishing": {
        "name": "Angeln",
        "location": "farm",
        "duration": 500,  # 8 Min
        "energy_cost": 8,
        "resources": [{"id": "fish", "min": 1, "max": 4}],
        "description": "Ich angle am See! 🎣"
    }
}

# ═════════════════════════════════════════════════════════════════
# GAME ACTION STATE
# ═════════════════════════════════════════════════════════════════

GAME_ACTION_STATE = {
    "current_action": None,  # Aktuelle Aktion
    "action_started": 0,  # Timestamp
    "action_data": {},  # Zusätzliche Daten
    "current_location": "home",  # Aktuelle Location
    "completed_actions": [],  # Historie
    "inventory": {},  # Gesammelte Ressourcen
    "last_action_time": 0,
    "action_cooldown": 60,  # Min 60 Sek zwischen Actions
}

# ═════════════════════════════════════════════════════════════════
# DECISION MAKING - Was soll Najika tun?
# ═════════════════════════════════════════════════════════════════

def decide_next_action(living_state: Dict, player_state: Dict) -> Optional[Dict]:
    """
    Entscheidet welche Aktion Najika als nächstes ausführen soll
    basierend auf ihren aktuellen Bedürfnissen

    Priority:
    1. Kritische Bedürfnisse (Hunger < 30, Energy < 20)
    2. Mood-basierte Actions
    3. Zeit-basierte Actions (Tag/Nacht)
    4. Random Exploration/Fun
    """

    hunger = living_state.get("hunger", 100)
    energy = living_state.get("energy", 100)
    mood = living_state.get("mood_game", 100)
    current_mood = living_state.get("current_mood", "neutral")
    hour = datetime.now().hour

    # Check if already doing something
    if GAME_ACTION_STATE["current_action"]:
        return None

    # Cooldown check
    if time.time() - GAME_ACTION_STATE["last_action_time"] < GAME_ACTION_STATE["action_cooldown"]:
        return None

    # === KRITISCHE BEDÜRFNISSE ===

    # Hunger kritisch? → Kochen!
    if hunger < 30:
        return {
            "type": "cooking",
            "reason": "hunger_critical",
            "priority": "high",
            "details": choose_cooking_recipe(hunger, energy)
        }

    # Energy kritisch? → Schlafen!
    if energy < 20:
        return {
            "type": "sleeping",
            "reason": "energy_critical",
            "priority": "high",
            "details": {
                "duration": 1800,  # 30 Min
                "energy_restore": 50
            }
        }

    # === MOOD-BASIERTE ACTIONS ===

    # Bored? → Erkunden oder Minigames
    if current_mood == "bored" or mood < 40:
        activities = [
            {"type": "exploring", "details": choose_exploring_action()},
            {"type": "farming", "details": random.choice(list(FARMING_ACTIONS.values()))},
            {"type": "dungeon", "details": EXPLORING_ACTIONS["explore_dungeon"]}
        ]
        return random.choice(activities)

    # Happy? → Geschenk für Kuja craften!
    if current_mood == "happy" or mood > 70:
        if energy > 50 and has_materials("gift_for_kuja"):
            return {
                "type": "crafting",
                "reason": "feeling_happy",
                "priority": "medium",
                "details": AUTONOMOUS_CRAFTING_RECIPES["gift_for_kuja"]
            }

    # === ZEIT-BASIERTE ACTIONS ===

    # Nacht (22-6 Uhr) → Schlafen oder Studieren
    if 22 <= hour or hour < 6:
        if energy < 70:
            return {
                "type": "sleeping",
                "reason": "nighttime",
                "priority": "medium",
                "details": {"duration": 3600, "energy_restore": 80}
            }
        else:
            return {
                "type": "studying",
                "reason": "nighttime_peaceful",
                "priority": "low",
                "details": {
                    "duration": 1200,
                    "skill": "intelligence",
                    "description": "Ich lese über Explosions-Magie! 📚✨"
                }
            }

    # Tag (6-12 Uhr) → Gärtnern
    if 6 <= hour < 12 and energy > 40:
        return {
            "type": "farming",
            "reason": "morning_routine",
            "priority": "medium",
            "details": choose_farming_action()
        }

    # Nachmittag (12-18 Uhr) → Erkunden oder Training
    if 12 <= hour < 18 and energy > 50:
        if random.random() < 0.6:
            return {
                "type": "exploring",
                "reason": "afternoon_adventure",
                "priority": "medium",
                "details": choose_exploring_action()
            }
        else:
            return {
                "type": "training",
                "reason": "afternoon_training",
                "priority": "medium",
                "details": {
                    "duration": 900,
                    "energy_cost": 20,
                    "description": "Training für mehr Power! 💪✨"
                }
            }

    # Abend (18-22 Uhr) → Kochen oder Crafting
    if 18 <= hour < 22 and energy > 30:
        if hunger < 60:
            return {
                "type": "cooking",
                "reason": "evening_dinner",
                "priority": "medium",
                "details": choose_cooking_recipe(hunger, energy)
            }
        else:
            return {
                "type": "crafting",
                "reason": "evening_hobby",
                "priority": "low",
                "details": choose_crafting_recipe(living_state, player_state)
            }

    # === DEFAULT: Random Activity ===
    default_activities = [
        {"type": "farming", "details": choose_farming_action()},
        {"type": "exploring", "details": choose_exploring_action()},
        {"type": "crafting", "details": choose_crafting_recipe(living_state, player_state)},
        {"type": "cooking", "details": choose_cooking_recipe(hunger, energy)}
    ]

    return random.choice(default_activities)


def choose_cooking_recipe(hunger: float, energy: float) -> Dict:
    """Wählt das beste Cooking Recipe basierend auf Hunger/Energy"""

    # Hunger sehr niedrig? → Hearty Meal
    if hunger < 40:
        if energy > 30:
            return COOKING_RECIPES["hearty_meal"]
        else:
            return COOKING_RECIPES["simple_meal"]

    # Hunger mittel? → Simple Meal oder Snack
    if hunger < 70:
        return COOKING_RECIPES["simple_meal"]

    # Energy niedrig? → Energy Drink
    if energy < 50:
        return COOKING_RECIPES["energy_drink"]

    # Glücklich und gut versorgt? → Gourmet für Kuja!
    if hunger > 60 and energy > 50:
        return COOKING_RECIPES["gourmet_meal"]

    return COOKING_RECIPES["snack"]


def choose_farming_action() -> Dict:
    """Wählt eine Farming Action"""
    # Zufällig zwischen verschiedenen Farming-Aktivitäten
    actions = list(FARMING_ACTIONS.values())
    return random.choice(actions)


def choose_exploring_action() -> Dict:
    """Wählt eine Exploring Action"""
    # Bevorzuge sichere Actions wenn Energy niedrig
    actions = list(EXPLORING_ACTIONS.values())
    return random.choice(actions)


def choose_crafting_recipe(living_state: Dict, player_state: Dict) -> Dict:
    """Wählt ein Crafting Recipe basierend auf Bedürfnissen"""

    health = player_state.get("health", 100)
    mana = player_state.get("mana", 100)
    mood = living_state.get("mood_game", 100)

    # Health niedrig? → Health Potion
    if health < 50:
        return AUTONOMOUS_CRAFTING_RECIPES["health_potion"]

    # Mana niedrig? → Mana Potion
    if mana < 50:
        return AUTONOMOUS_CRAFTING_RECIPES["mana_potion"]

    # Glücklich? → Geschenk für Kuja
    if mood > 70:
        return AUTONOMOUS_CRAFTING_RECIPES["gift_for_kuja"]

    # Default: Health Potion
    return AUTONOMOUS_CRAFTING_RECIPES["health_potion"]


def has_materials(recipe_id: str) -> bool:
    """Prüft ob Materialien vorhanden sind"""
    # Simplified: Immer true für Demo
    # In real implementation: Check GAME_ACTION_STATE["inventory"]
    return True

# ═════════════════════════════════════════════════════════════════
# ACTION EXECUTION
# ═════════════════════════════════════════════════════════════════

def start_action(action: Dict) -> Dict:
    """Startet eine Game Action"""

    action_type = action["type"]
    details = action["details"]

    GAME_ACTION_STATE["current_action"] = action_type
    GAME_ACTION_STATE["action_started"] = time.time()
    GAME_ACTION_STATE["action_data"] = details
    GAME_ACTION_STATE["last_action_time"] = time.time()

    # Message für Chat/UI
    messages = {
        "cooking": f"🍳 Ich koche gerade: {details.get('name', 'Essen')}! {details.get('description', '')}",
        "farming": f"🌱 {details.get('description', 'Ich arbeite im Garten!')}",
        "exploring": f"🗺️ {details.get('description', 'Ich erkunde die Welt!')}",
        "crafting": f"🔨 Ich crafte: {details.get('name', 'etwas')}! {details.get('description', '')}",
        "sleeping": "💤 Ich schlafe gerade... zzz...",
        "training": "💪 Ich trainiere! Werde stärker!",
        "studying": "📚 Ich lese und lerne!",
        "dungeon": "🗝️ Dungeon-Erkundung! Wish me luck! ✨"
    }

    message = messages.get(action_type, "Ich mache gerade was...")

    return {
        "action_started": True,
        "type": action_type,
        "message": message,
        "duration": details.get("duration", 600),
        "energy_cost": details.get("energy_cost", 10),
        "started_at": datetime.now().isoformat()
    }


def check_action_completion() -> Optional[Dict]:
    """Prüft ob aktuelle Action abgeschlossen ist"""

    if not GAME_ACTION_STATE["current_action"]:
        return None

    action_type = GAME_ACTION_STATE["current_action"]
    details = GAME_ACTION_STATE["action_data"]
    started = GAME_ACTION_STATE["action_started"]
    duration = details.get("duration", 600)

    elapsed = time.time() - started

    if elapsed >= duration:
        # Action abgeschlossen!
        result = complete_action(action_type, details)

        # State zurücksetzen
        GAME_ACTION_STATE["current_action"] = None
        GAME_ACTION_STATE["action_data"] = {}

        # Historie
        GAME_ACTION_STATE["completed_actions"].append({
            "type": action_type,
            "completed_at": time.time(),
            "result": result
        })

        return result

    # Noch nicht fertig
    progress = (elapsed / duration) * 100
    return {
        "completed": False,
        "progress": min(100, progress),
        "remaining_seconds": max(0, duration - elapsed)
    }


def complete_action(action_type: str, details: Dict) -> Dict:
    """Führt Completion-Logic aus und gibt Rewards"""

    result = {
        "completed": True,
        "type": action_type,
        "message": "",
        "rewards": {},
        "stat_changes": {}
    }

    if action_type == "cooking":
        result["message"] = f"✨ Fertig gekocht: {details['name']}! Nom nom! 😋"
        result["rewards"] = {
            "hunger_restore": details.get("hunger_restore", 30),
            "energy_restore": details.get("energy_restore", 0),
            "mood_bonus": details.get("mood_bonus", 5)
        }
        result["stat_changes"] = {
            "hunger": details.get("hunger_restore", 30),
            "energy": -details.get("energy_cost", 5),
            "mood_game": details.get("mood_bonus", 5)
        }

    elif action_type == "farming":
        result["message"] = f"✨ {details['name']} abgeschlossen! 🌱"
        result["stat_changes"] = {
            "energy": -details.get("energy_cost", 10),
            "mood_game": 5
        }

    elif action_type == "exploring":
        resources = details.get("resources", [])
        gathered = {}

        for resource in resources:
            amount = random.randint(resource.get("min", 1), resource.get("max", 3))
            resource_id = resource["id"]
            gathered[resource_id] = amount

            # Add to inventory
            if resource_id in GAME_ACTION_STATE["inventory"]:
                GAME_ACTION_STATE["inventory"][resource_id] += amount
            else:
                GAME_ACTION_STATE["inventory"][resource_id] = amount

        result["message"] = f"✨ Erkundung beendet! Gesammelt: {gathered}"
        result["rewards"] = {"resources": gathered}
        result["stat_changes"] = {
            "energy": -details.get("energy_cost", 15),
            "mood_game": 10
        }

    elif action_type == "crafting":
        result["message"] = f"✨ {details['name']} fertig gecraftet! 🔨"
        result["stat_changes"] = {
            "energy": -details.get("energy_cost", 10),
            "mood_game": details.get("mood_bonus", 10)
        }

    elif action_type == "sleeping":
        result["message"] = "💤 Ausgeschlafen! Fühle mich gut! ✨"
        result["stat_changes"] = {
            "energy": details.get("energy_restore", 50),
            "mood_game": 10
        }

    elif action_type == "training":
        result["message"] = "💪 Training abgeschlossen! Ich bin stärker! ✨"
        result["stat_changes"] = {
            "energy": -details.get("energy_cost", 20),
            "strength": 2,
            "mood_game": 5
        }

    elif action_type == "studying":
        result["message"] = "📚 Habe viel gelernt! 🧠✨"
        result["stat_changes"] = {
            "energy": -10,
            "intelligence": 2,
            "mood_game": 8
        }

    return result


def apply_stat_changes(living_state: Dict, player_state: Dict, stat_changes: Dict):
    """Wendet Stat-Changes auf Living/Player State an"""

    for stat, change in stat_changes.items():
        # Living State Stats
        if stat in ["hunger", "energy", "mood_game", "anger_level"]:
            current = living_state.get(stat, 100)
            living_state[stat] = max(0, min(100, current + change))

        # Player State Stats
        elif stat in ["health", "mana", "stamina", "strength", "intelligence"]:
            if stat in player_state:
                current = player_state.get(stat, 100)
                max_stat = player_state.get(f"max{stat.capitalize()}", 100)
                player_state[stat] = max(0, min(max_stat, current + change))

# ═════════════════════════════════════════════════════════════════
# TELEPORT/LOCATION SYSTEM
# ═════════════════════════════════════════════════════════════════

def teleport_to_location(location_id: str) -> Dict:
    """Teleportiert Najika zu einer Location"""

    if location_id not in LOCATIONS:
        return {
            "success": False,
            "message": f"Location {location_id} existiert nicht!"
        }

    location = LOCATIONS[location_id]
    old_location = GAME_ACTION_STATE["current_location"]
    GAME_ACTION_STATE["current_location"] = location_id

    return {
        "success": True,
        "message": f"Teleportiert von {old_location} → {location['name']}!",
        "location": location,
        "activities_available": location["activities"]
    }


def get_current_location() -> Dict:
    """Gibt aktuelle Location zurück"""
    location_id = GAME_ACTION_STATE["current_location"]
    return LOCATIONS.get(location_id, LOCATIONS["home"])

# ═════════════════════════════════════════════════════════════════
# SUGGESTED ACTIONS für UI
# ═════════════════════════════════════════════════════════════════

def suggest_actions(living_state: Dict, player_state: Dict) -> List[Dict]:
    """Gibt Liste von vorgeschlagenen Actions für UI zurück"""

    suggestions = []

    hunger = living_state.get("hunger", 100)
    energy = living_state.get("energy", 100)
    mood = living_state.get("mood_game", 100)

    # Hunger niedrig?
    if hunger < 50:
        suggestions.append({
            "type": "cooking",
            "reason": "Najika hat Hunger",
            "icon": "🍳",
            "priority": "high" if hunger < 30 else "medium"
        })

    # Energy niedrig?
    if energy < 40:
        suggestions.append({
            "type": "sleeping",
            "reason": "Najika ist müde",
            "icon": "💤",
            "priority": "high" if energy < 20 else "medium"
        })

    # Mood niedrig?
    if mood < 50:
        suggestions.append({
            "type": "exploring",
            "reason": "Najika ist gelangweilt",
            "icon": "🗺️",
            "priority": "medium"
        })

    # Immer verfügbar
    suggestions.extend([
        {"type": "farming", "reason": "Garten pflegen", "icon": "🌱", "priority": "low"},
        {"type": "crafting", "reason": "Etwas craften", "icon": "🔨", "priority": "low"},
        {"type": "exploring", "reason": "Welt erkunden", "icon": "🗺️", "priority": "low"}
    ])

    return suggestions

# ═════════════════════════════════════════════════════════════════
# MAIN UPDATE FUNCTION
# ═════════════════════════════════════════════════════════════════

def update_game_actions(living_state: Dict, player_state: Dict) -> Dict:
    """
    Haupt-Update Funktion
    Wird regelmäßig aufgerufen um Game Actions zu managen
    """

    result = {
        "action_completed": None,
        "action_started": None,
        "current_action": None,
        "suggestions": []
    }

    # 1. Check ob aktuelle Action fertig ist
    completion = check_action_completion()
    if completion and completion.get("completed"):
        result["action_completed"] = completion

        # Apply stat changes
        if "stat_changes" in completion:
            apply_stat_changes(living_state, player_state, completion["stat_changes"])
    else:
        result["current_action"] = completion

    # 2. Wenn keine Action läuft: Entscheide nächste Action
    if not GAME_ACTION_STATE["current_action"]:
        next_action = decide_next_action(living_state, player_state)

        if next_action:
            started = start_action(next_action)
            result["action_started"] = started

            # Apply immediate energy cost
            energy_cost = started.get("energy_cost", 0)
            if energy_cost > 0:
                living_state["energy"] = max(0, living_state["energy"] - energy_cost)

    # 3. Generiere Suggestions für UI
    result["suggestions"] = suggest_actions(living_state, player_state)

    return result

# ═════════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS
# ═════════════════════════════════════════════════════════════════

def get_game_action_state() -> Dict:
    """Gibt kompletten Game Action State zurück"""
    return {
        **GAME_ACTION_STATE,
        "locations": LOCATIONS,
        "current_location_data": get_current_location()
    }


def export_game_action_state() -> str:
    """Exportiert State als JSON"""
    return json.dumps(GAME_ACTION_STATE, indent=2)


def import_game_action_state(json_string: str) -> Dict:
    """Importiert State aus JSON"""
    try:
        imported = json.loads(json_string)
        GAME_ACTION_STATE.update(imported)
        return GAME_ACTION_STATE
    except:
        return GAME_ACTION_STATE


if __name__ == "__main__":
    print("🎮 Najika Game Actions System geladen!")
    print()
    print("Features:")
    print("  - Autonomes Kochen (5 Rezepte)")
    print("  - Autonomes Farming (4 Actions)")
    print("  - Autonomes Erkunden (6 Actions)")
    print("  - Autonomes Crafting (4 Recipes)")
    print("  - 6 Locations mit Teleport")
    print("  - Smart Decision Making basierend auf Needs")
    print("  - Zeit-basierte Actions (Tag/Nacht)")
    print("  - Resource Gathering & Inventory")
    print()
    print("Integriere dieses Modul in najika_living_system.py und server.py!")
