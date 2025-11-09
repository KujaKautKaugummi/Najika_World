"""
NAJIKA FISHING SYSTEM
=====================

Catch fish at various spots across Najika's world.

Features:
- Multiple fish types (common to legendary)
- Region-specific fish
- Time-of-day and weather mechanics
- Fishing spots with respawn timers
- Skill-based catch chances
- AI auto-fishing when Najika is hungry

Author: Claude Code (CLI)
Date: 2025-11-09 (Tag 2)
"""

import time
import random
import json
from pathlib import Path

# =====================================================
# FISH TYPE DEFINITIONS
# =====================================================

FISH_TYPES = {
    # COMMON (everywhere)
    "small_fish": {
        "name": "Kleinfisch",
        "rarity": "common",
        "catch_chance": 50.0,
        "regions": ["all"],
        "time_of_day": ["day", "night"],
        "sell_price": 5,
        "hunger_value": 10,
        "size_min": 5,
        "size_max": 15
    },

    "carp": {
        "name": "Karpfen",
        "rarity": "common",
        "catch_chance": 35.0,
        "regions": ["Samtmoos-Tiefwald", "Salzwind-Küste"],
        "time_of_day": ["day"],
        "sell_price": 15,
        "hunger_value": 20,
        "size_min": 20,
        "size_max": 50
    },

    # UNCOMMON
    "salmon": {
        "name": "Lachs",
        "rarity": "uncommon",
        "catch_chance": 20.0,
        "regions": ["Salzwind-Küste"],
        "time_of_day": ["day"],
        "weather": ["rain"],
        "sell_price": 50,
        "hunger_value": 35,
        "energy_bonus": 10,
        "size_min": 40,
        "size_max": 80
    },

    "trout": {
        "name": "Forelle",
        "rarity": "uncommon",
        "catch_chance": 25.0,
        "regions": ["Samtmoos-Tiefwald"],
        "time_of_day": ["day", "dawn", "dusk"],
        "sell_price": 40,
        "hunger_value": 30,
        "size_min": 25,
        "size_max": 60
    },

    # RARE
    "golden_trout": {
        "name": "Goldforelle",
        "rarity": "rare",
        "catch_chance": 5.0,
        "regions": ["Samtmoos-Tiefwald"],
        "time_of_day": ["dawn", "dusk"],
        "weather": ["clear"],
        "sell_price": 200,
        "hunger_value": 50,
        "luck_bonus": 5,
        "size_min": 30,
        "size_max": 60
    },

    "tuna": {
        "name": "Thunfisch",
        "rarity": "rare",
        "catch_chance": 8.0,
        "regions": ["Salzwind-Küste"],
        "time_of_day": ["day"],
        "sell_price": 150,
        "hunger_value": 60,
        "energy_bonus": 20,
        "size_min": 80,
        "size_max": 150
    },

    # LEGENDARY (region-specific)
    "lava_eel": {
        "name": "Lava-Aal",
        "rarity": "legendary",
        "catch_chance": 1.0,
        "regions": ["Magmaströme"],
        "time_of_day": ["night"],
        "weather": ["clear"],
        "special_rod_required": "flame_rod",
        "sell_price": 1000,
        "hunger_value": 100,
        "special_effect": "fire_resistance_permanent",
        "size_min": 100,
        "size_max": 200
    },

    "ice_serpent": {
        "name": "Eisschlange",
        "rarity": "legendary",
        "catch_chance": 1.0,
        "regions": ["Reich der Drei"],
        "time_of_day": ["night"],
        "weather": ["snow"],
        "special_rod_required": "frost_rod",
        "sell_price": 1000,
        "hunger_value": 100,
        "special_effect": "cold_resistance_permanent",
        "size_min": 100,
        "size_max": 200
    },

    "swamp_monster": {
        "name": "Sumpfmonster",
        "rarity": "legendary",
        "catch_chance": 0.5,
        "regions": ["Grünschlamm-Sumpf"],
        "time_of_day": ["night"],
        "weather": ["rain", "storm"],
        "sell_price": 1500,
        "hunger_value": 150,
        "special_effect": "poison_resistance",
        "size_min": 150,
        "size_max": 300
    },

    # TRASH
    "old_boot": {
        "name": "Alter Stiefel",
        "rarity": "trash",
        "catch_chance": 15.0,
        "regions": ["all"],
        "sell_price": 1,
        "recyclable": True,
        "size_min": 20,
        "size_max": 35
    },

    "seaweed": {
        "name": "Algen",
        "rarity": "trash",
        "catch_chance": 10.0,
        "regions": ["all"],
        "sell_price": 2,
        "craftable": True,  # Can be used for cooking
        "size_min": 10,
        "size_max": 50
    }
}

# =====================================================
# FISHING SPOT DEFINITIONS
# =====================================================

FISHING_SPOTS = {
    # Najika's home (V2)
    "home_pond": {
        "spot_id": "home_pond",
        "name": "Heim-Teich",
        "position": {"x": -500, "z": -500},
        "region": "Samtmoos-Tiefwald",
        "type": "freshwater",
        "fish_pool": ["small_fish", "carp", "trout", "golden_trout", "old_boot", "seaweed"],
        "quality": 0.7,
        "respawn_time": 1800,      # 30 minutes
        "max_fish": 20,
        "current_fish": 20,
        "last_respawn": time.time(),
        "public": False             # Only Najika
    },

    # Big world - Ocean
    "ocean_shore": {
        "spot_id": "ocean_shore_01",
        "name": "Meeresküste",
        "position": {"x": 3800, "z": 200},
        "region": "Salzwind-Küste",
        "type": "saltwater",
        "fish_pool": ["small_fish", "carp", "salmon", "tuna", "old_boot"],
        "quality": 0.85,
        "respawn_time": 3600,      # 1 hour
        "max_fish": 50,
        "current_fish": 50,
        "last_respawn": time.time(),
        "public": True
    },

    # Big world - Swamp
    "swamp_waters": {
        "spot_id": "swamp_waters_01",
        "name": "Sumpfgewässer",
        "position": {"x": -2800, "z": 2800},
        "region": "Grünschlamm-Sumpf",
        "type": "swamp",
        "fish_pool": ["small_fish", "swamp_monster", "seaweed"],
        "quality": 0.6,
        "respawn_time": 7200,      # 2 hours
        "max_fish": 30,
        "current_fish": 30,
        "last_respawn": time.time(),
        "danger_level": "high",
        "public": True
    },

    # Big world - Lava Lake (EXTREME)
    "lava_lake": {
        "spot_id": "lava_lake_01",
        "name": "Lavasee",
        "position": {"x": 2800, "z": 2800},
        "region": "Magmaströme",
        "type": "lava",
        "fish_pool": ["lava_eel"],
        "quality": 1.0,
        "respawn_time": 86400,     # 24 hours
        "max_fish": 1,
        "current_fish": 1,
        "last_respawn": time.time(),
        "danger_level": "extreme",
        "special_equipment_required": "flame_rod",
        "public": True
    },

    # Big world - Ice Lake
    "frozen_lake": {
        "spot_id": "frozen_lake_01",
        "name": "Gefrorener See",
        "position": {"x": 200, "z": -3800},
        "region": "Reich der Drei",
        "type": "frozen",
        "fish_pool": ["small_fish", "ice_serpent"],
        "quality": 0.9,
        "respawn_time": 86400,     # 24 hours
        "max_fish": 15,
        "current_fish": 15,
        "last_respawn": time.time(),
        "danger_level": "high",
        "special_equipment_required": "frost_rod",
        "public": True
    }
}

# =====================================================
# GLOBAL STATE
# =====================================================

FISHING_STATE = {
    "spots": {},  # Will be filled from FISHING_SPOTS
    "player_stats": {
        "fishing_skill": 1,
        "total_caught": 0,
        "total_attempts": 0,
        "biggest_catch": None,
        "legendary_count": 0
    },
    "global_time_of_day": "day",
    "global_weather": "clear",
    "last_update": time.time()
}

STATE_FILE = Path(__file__).parent / "fishing_state.json"

# =====================================================
# STATE MANAGEMENT
# =====================================================

def load_state():
    """Load fishing state from file"""
    global FISHING_STATE

    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                FISHING_STATE = json.load(f)
            print(f"[OK] Fishing State loaded from {STATE_FILE}")
        except Exception as e:
            print(f"[WARNING] Error loading fishing state: {e}")
            print("[INFO] Using default state")
            initialize_spots()
    else:
        print("[INFO] No fishing state file found, using defaults")
        initialize_spots()

def save_state():
    """Save fishing state to file"""
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(FISHING_STATE, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save fishing state: {e}")

def initialize_spots():
    """Initialize all fishing spots"""
    FISHING_STATE["spots"] = {}
    for spot_id, spot_data in FISHING_SPOTS.items():
        FISHING_STATE["spots"][spot_id] = {
            "current_fish": spot_data["max_fish"],
            "last_respawn": time.time()
        }
    save_state()

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_time_of_day():
    """Get current time of day"""
    # For now, use global state (later: calculate from real time)
    return FISHING_STATE["global_time_of_day"]

def set_time_of_day(time_of_day):
    """Set time of day (day/night/dawn/dusk)"""
    if time_of_day in ["day", "night", "dawn", "dusk"]:
        FISHING_STATE["global_time_of_day"] = time_of_day
        save_state()
        return True
    return False

def get_weather():
    """Get current weather"""
    return FISHING_STATE["global_weather"]

def set_weather(weather):
    """Set weather (clear/rain/snow/storm)"""
    if weather in ["clear", "rain", "snow", "storm"]:
        FISHING_STATE["global_weather"] = weather
        save_state()
        return True
    return False

def get_spot_by_id(spot_id):
    """Get fishing spot by ID"""
    if spot_id in FISHING_SPOTS:
        spot = FISHING_SPOTS[spot_id].copy()
        if spot_id in FISHING_STATE["spots"]:
            spot.update(FISHING_STATE["spots"][spot_id])
        return spot
    return None

# =====================================================
# FISHING MECHANICS
# =====================================================

def start_fishing(spot_id, player_skill=None, rod_quality=1.0, special_rod=None):
    """
    Start fishing at a spot

    Args:
        spot_id: ID of the fishing spot
        player_skill: Player's fishing skill (1-100), uses global if None
        rod_quality: Quality of rod (1.0 = basic, 2.0 = excellent)
        special_rod: Name of special rod (e.g. "flame_rod")

    Returns:
        Dictionary with fishing result
    """

    spot = get_spot_by_id(spot_id)
    if not spot:
        return {"success": False, "error": f"Fishing spot {spot_id} not found"}

    # Check if fish available
    spot_state = FISHING_STATE["spots"].get(spot_id, {})
    current_fish = spot_state.get("current_fish", spot["max_fish"])

    if current_fish <= 0:
        return {
            "success": False,
            "error": "No fish available! Come back later.",
            "next_respawn": spot_state.get("last_respawn", time.time()) + spot["respawn_time"]
        }

    # Check special equipment
    if spot.get("special_equipment_required"):
        if special_rod != spot["special_equipment_required"]:
            return {
                "success": False,
                "error": f"You need {spot['special_equipment_required']} to fish here!"
            }

    # Use global fishing skill if not provided
    if player_skill is None:
        player_skill = FISHING_STATE["player_stats"]["fishing_skill"]

    # Choose random fish from pool (weighted by rarity)
    fish_type = choose_fish_from_pool(spot["fish_pool"])
    fish = FISH_TYPES[fish_type]

    # Calculate catch chance
    chance_result = calculate_catch_chance(
        fish=fish,
        spot=spot,
        player_skill=player_skill,
        rod_quality=rod_quality
    )

    final_chance = chance_result["final_chance"]

    # Roll for success!
    roll = random.random() * 100
    success = roll < final_chance

    # Update stats
    FISHING_STATE["player_stats"]["total_attempts"] += 1

    if success:
        # CAUGHT!
        spot_state["current_fish"] = current_fish - 1
        FISHING_STATE["spots"][spot_id] = spot_state
        FISHING_STATE["player_stats"]["total_caught"] += 1

        # Calculate size
        size = calculate_fish_size(fish, spot["quality"], rod_quality)

        # Update biggest catch
        if FISHING_STATE["player_stats"]["biggest_catch"] is None or \
           size > FISHING_STATE["player_stats"]["biggest_catch"].get("size", 0):
            FISHING_STATE["player_stats"]["biggest_catch"] = {
                "type": fish_type,
                "name": fish["name"],
                "size": size
            }

        # Count legendaries
        if fish["rarity"] == "legendary":
            FISHING_STATE["player_stats"]["legendary_count"] += 1

        # XP gained (rarer fish = more XP)
        rarity_multiplier = {
            "trash": 0.5,
            "common": 1.0,
            "uncommon": 2.0,
            "rare": 5.0,
            "legendary": 20.0
        }
        base_xp = int((100 - fish["catch_chance"]) * 2)
        xp_gained = int(base_xp * rarity_multiplier.get(fish["rarity"], 1.0))

        # Skill up chance (5% per catch)
        if random.random() < 0.05:
            old_skill = FISHING_STATE["player_stats"]["fishing_skill"]
            FISHING_STATE["player_stats"]["fishing_skill"] = min(100, old_skill + 1)
            skill_up = True
        else:
            skill_up = False

        save_state()

        return {
            "success": True,
            "caught": True,
            "fish": {
                "type": fish_type,
                "name": fish["name"],
                "rarity": fish["rarity"],
                "size": size,
                "sell_price": fish["sell_price"],
                "hunger_value": fish.get("hunger_value", 0),
                "energy_bonus": fish.get("energy_bonus", 0),
                "special_effect": fish.get("special_effect")
            },
            "xp_gained": xp_gained,
            "skill_up": skill_up,
            "message": f"You caught a {size}cm {fish['name']}!",
            "catch_chance": final_chance,
            "roll": roll,
            "chance_breakdown": chance_result["breakdown"]
        }
    else:
        # DIDN'T CATCH
        save_state()

        return {
            "success": True,
            "caught": False,
            "message": "The fish got away!",
            "xp_gained": 1,  # Still get 1 XP for trying
            "catch_chance": final_chance,
            "roll": roll,
            "chance_breakdown": chance_result["breakdown"]
        }

def choose_fish_from_pool(fish_pool):
    """Choose a fish from the pool (weighted by rarity)"""

    # Build weighted list
    weighted_fish = []
    for fish_type in fish_pool:
        if fish_type in FISH_TYPES:
            fish = FISH_TYPES[fish_type]
            # Weight is the catch_chance (common fish appear more often)
            weight = int(fish["catch_chance"])
            weighted_fish.extend([fish_type] * weight)

    if not weighted_fish:
        return "small_fish"  # Fallback

    return random.choice(weighted_fish)

def calculate_catch_chance(fish, spot, player_skill, rod_quality):
    """Calculate final catch chance with all modifiers"""

    base_chance = fish["catch_chance"]
    breakdown = {"base": base_chance}

    # Skill bonus (+2% per skill level)
    skill_bonus = player_skill * 2.0
    breakdown["skill"] = skill_bonus

    # Rod quality bonus
    rod_bonus = (rod_quality - 1.0) * 10
    breakdown["rod"] = rod_bonus

    # Spot quality bonus
    spot_bonus = spot["quality"] * 10
    breakdown["spot"] = spot_bonus

    # Time of day bonus
    current_time = get_time_of_day()
    if current_time in fish.get("time_of_day", []):
        time_bonus = 20.0
    else:
        time_bonus = -20.0
    breakdown["time"] = time_bonus

    # Weather bonus
    weather_bonus = 0
    if "weather" in fish:
        current_weather = get_weather()
        if current_weather in fish["weather"]:
            weather_bonus = 30.0
        else:
            weather_bonus = -50.0
    breakdown["weather"] = weather_bonus

    # Calculate final
    final_chance = (
        base_chance +
        skill_bonus +
        rod_bonus +
        spot_bonus +
        time_bonus +
        weather_bonus
    )

    # Clamp between 1% and 95%
    final_chance = max(1.0, min(95.0, final_chance))

    return {
        "final_chance": final_chance,
        "breakdown": breakdown
    }

def calculate_fish_size(fish, spot_quality, rod_quality):
    """Calculate fish size based on quality factors"""

    # Base size range
    size_range = fish["size_max"] - fish["size_min"]
    base_size = random.randint(fish["size_min"], fish["size_max"])

    # Quality modifier (better spot + rod = bigger fish)
    quality_modifier = (spot_quality + (rod_quality - 1.0)) / 2.0
    size_bonus = int(size_range * quality_modifier * 0.4)

    final_size = base_size + size_bonus
    return max(fish["size_min"], min(fish["size_max"], final_size))

# =====================================================
# SPOT RESPAWN
# =====================================================

def update_fishing_spots():
    """Update all fishing spots (fish respawn over time)"""

    current_time = time.time()

    for spot_id, spot_def in FISHING_SPOTS.items():
        if spot_id not in FISHING_STATE["spots"]:
            FISHING_STATE["spots"][spot_id] = {
                "current_fish": spot_def["max_fish"],
                "last_respawn": current_time
            }
            continue

        spot_state = FISHING_STATE["spots"][spot_id]
        elapsed = current_time - spot_state.get("last_respawn", current_time)

        # Check if respawn time reached
        if elapsed >= spot_def["respawn_time"]:
            old_count = spot_state.get("current_fish", 0)
            spot_state["current_fish"] = spot_def["max_fish"]
            spot_state["last_respawn"] = current_time

            new_fish = spot_def["max_fish"] - old_count
            if new_fish > 0:
                print(f"[INFO] {spot_def['name']}: {new_fish} new fish spawned")

    FISHING_STATE["last_update"] = current_time
    save_state()

# =====================================================
# AI AUTO-FISHING (Najika fishes when hungry)
# =====================================================

def najika_auto_fish(living_state):
    """Najika automatically fishes when hungry (AI mode)"""

    if living_state.get("control_mode") != "ai":
        return []

    if living_state.get("hunger", 100) >= 25:
        return []  # Not hungry enough

    if living_state.get("energy", 100) < 20:
        return []  # Too tired

    actions_taken = []

    # Fish at home pond
    result = start_fishing(
        "home_pond",
        player_skill=FISHING_STATE["player_stats"]["fishing_skill"],
        rod_quality=1.0
    )

    if result.get("caught"):
        actions_taken.append({
            "action": "fish_caught",
            "result": result
        })
    else:
        actions_taken.append({
            "action": "fish_missed",
            "result": result
        })

    return actions_taken

# =====================================================
# STATUS & STATS
# =====================================================

def get_fishing_status():
    """Get complete fishing status"""

    update_fishing_spots()

    # Get all spots with current fish counts
    spots_status = []
    for spot_id, spot_def in FISHING_SPOTS.items():
        spot_state = FISHING_STATE["spots"].get(spot_id, {})
        spots_status.append({
            "spot_id": spot_id,
            "name": spot_def["name"],
            "region": spot_def["region"],
            "type": spot_def["type"],
            "current_fish": spot_state.get("current_fish", spot_def["max_fish"]),
            "max_fish": spot_def["max_fish"],
            "respawn_time": spot_def["respawn_time"],
            "last_respawn": spot_state.get("last_respawn", time.time()),
            "quality": spot_def["quality"],
            "public": spot_def.get("public", False)
        })

    return {
        "player_stats": FISHING_STATE["player_stats"],
        "spots": spots_status,
        "time_of_day": FISHING_STATE["global_time_of_day"],
        "weather": FISHING_STATE["global_weather"]
    }

def get_all_fish_types():
    """Get list of all fish types"""
    return {
        fish_id: {
            "name": fish["name"],
            "rarity": fish["rarity"],
            "catch_chance": fish["catch_chance"],
            "regions": fish.get("regions", []),
            "sell_price": fish["sell_price"],
            "size_range": [fish["size_min"], fish["size_max"]]
        }
        for fish_id, fish in FISH_TYPES.items()
    }

# =====================================================
# INITIALIZATION
# =====================================================

# Load state on import
load_state()

if __name__ == "__main__":
    print("="*60)
    print("NAJIKA FISHING SYSTEM - TEST")
    print("="*60)

    # Test fishing
    print("\n[TEST] Fishing at home pond...")
    result = start_fishing("home_pond", player_skill=5, rod_quality=1.0)
    print(f"Success: {result['success']}")
    print(f"Caught: {result.get('caught', False)}")
    if result.get('caught'):
        print(f"Fish: {result['fish']['name']} ({result['fish']['size']}cm)")
        print(f"XP: {result['xp_gained']}")
    else:
        print(f"Message: {result['message']}")

    # Test status
    print("\n[TEST] Getting fishing status...")
    status = get_fishing_status()
    print(f"Fishing Skill: {status['player_stats']['fishing_skill']}")
    print(f"Total Caught: {status['player_stats']['total_caught']}")
    print(f"Available Spots: {len(status['spots'])}")

    print("\n[OK] Fishing System tests complete!")
