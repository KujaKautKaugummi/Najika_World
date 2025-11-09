"""
NAJIKA FARMING SYSTEM
====================

Plant, grow, and harvest crops in Najika's world.

Features:
- Multiple crop types (vegetables, fruits, grains, special)
- Growth stages with time-based progression
- Water/soil/health mechanics
- Region-specific and seasonal crops
- AI auto-farming when Najika is hungry

Author: Claude Code (CLI)
Date: 2025-11-09 (Tag 2)
"""

import time
import random
import json
from pathlib import Path

# =====================================================
# CROP DEFINITIONS
# =====================================================

CROPS = {
    # VEGETABLES (fast growth)
    "carrot": {
        "name": "Karotte",
        "type": "vegetable",
        "growth_time": 3600,      # 1 hour
        "water_need": "medium",
        "seasons": ["spring", "fall"],
        "yield_min": 3,
        "yield_max": 8,
        "sell_price": 10,
        "hunger_value": 15,
        "regions": ["all"]
    },

    "tomato": {
        "name": "Tomate",
        "type": "vegetable",
        "growth_time": 5400,      # 1.5 hours
        "water_need": "high",
        "seasons": ["spring", "summer"],
        "yield_min": 4,
        "yield_max": 10,
        "sell_price": 15,
        "hunger_value": 20,
        "regions": ["all"]
    },

    "potato": {
        "name": "Kartoffel",
        "type": "vegetable",
        "growth_time": 4500,      # 1.25 hours
        "water_need": "medium",
        "seasons": ["spring", "summer", "fall"],
        "yield_min": 5,
        "yield_max": 12,
        "sell_price": 8,
        "hunger_value": 25,
        "regions": ["all"]
    },

    # FRUITS (medium growth)
    "strawberry": {
        "name": "Erdbeere",
        "type": "fruit",
        "growth_time": 7200,      # 2 hours
        "water_need": "medium",
        "seasons": ["spring", "summer"],
        "yield_min": 5,
        "yield_max": 15,
        "sell_price": 25,
        "hunger_value": 25,
        "energy_bonus": 5,
        "regions": ["Samtmoos-Tiefwald", "Salzwind-Küste", "all"]
    },

    "apple": {
        "name": "Apfel",
        "type": "fruit",
        "growth_time": 9000,      # 2.5 hours
        "water_need": "medium",
        "seasons": ["summer", "fall"],
        "yield_min": 3,
        "yield_max": 8,
        "sell_price": 30,
        "hunger_value": 30,
        "energy_bonus": 10,
        "regions": ["Samtmoos-Tiefwald", "all"]
    },

    # GRAINS (slow growth, high yield)
    "wheat": {
        "name": "Weizen",
        "type": "grain",
        "growth_time": 10800,     # 3 hours
        "water_need": "low",
        "seasons": ["spring", "summer", "fall"],
        "yield_min": 10,
        "yield_max": 25,
        "sell_price": 5,
        "crafting_ingredient": True,
        "regions": ["Blitzebene", "Samtmoos-Tiefwald", "all"]
    },

    "corn": {
        "name": "Mais",
        "type": "grain",
        "growth_time": 12600,     # 3.5 hours
        "water_need": "medium",
        "seasons": ["summer"],
        "yield_min": 8,
        "yield_max": 20,
        "sell_price": 7,
        "hunger_value": 30,
        "crafting_ingredient": True,
        "regions": ["Blitzebene", "all"]
    },

    # SPECIAL (region-specific)
    "fire_pepper": {
        "name": "Feuerpfeffer",
        "type": "special",
        "growth_time": 14400,     # 4 hours
        "water_need": "low",
        "temperature_need": "hot",
        "seasons": ["summer"],
        "yield_min": 2,
        "yield_max": 5,
        "sell_price": 100,
        "special_effect": "fire_resistance",
        "regions": ["Magmaströme", "Heiße Dünen"]
    },

    "ice_berry": {
        "name": "Eisbeere",
        "type": "special",
        "growth_time": 14400,     # 4 hours
        "water_need": "low",
        "temperature_need": "cold",
        "seasons": ["winter"],
        "yield_min": 2,
        "yield_max": 5,
        "sell_price": 100,
        "special_effect": "cold_resistance",
        "regions": ["Reich der Drei"]
    },

    "magic_mushroom": {
        "name": "Magischer Pilz",
        "type": "special",
        "growth_time": 18000,     # 5 hours
        "water_need": "high",
        "seasons": ["spring", "fall"],
        "yield_min": 1,
        "yield_max": 3,
        "sell_price": 250,
        "mood_bonus": 50,
        "special_effect": "mood_boost",
        "regions": ["Samtmoos-Tiefwald", "Grünschlamm-Sumpf"]
    }
}

# =====================================================
# GROWTH STAGES
# =====================================================

GROWTH_STAGES = {
    "planted": {
        "duration_percent": 0,
        "visual": "soil_with_seed",
        "description": "Gerade eingepflanzt"
    },
    "sprouting": {
        "duration_percent": 25,
        "visual": "small_sprout",
        "description": "Keimt gerade"
    },
    "growing": {
        "duration_percent": 60,
        "visual": "medium_plant",
        "description": "Wächst kräftig"
    },
    "harvestable": {
        "duration_percent": 100,
        "visual": "full_grown",
        "description": "Bereit zur Ernte!",
        "harvestable": True
    }
}

# =====================================================
# GLOBAL STATE
# =====================================================

FARMING_STATE = {
    "fields": [],
    "global_season": "spring",
    "global_weather": "clear",
    "last_update": time.time(),
    "total_harvests": 0,
    "total_crops_planted": 0
}

STATE_FILE = Path(__file__).parent / "farming_state.json"

# =====================================================
# STATE MANAGEMENT
# =====================================================

def load_state():
    """Load farming state from file"""
    global FARMING_STATE

    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                FARMING_STATE = json.load(f)
            print(f"[OK] Farming State loaded from {STATE_FILE}")
        except Exception as e:
            print(f"[WARNING] Error loading farming state: {e}")
            print("[INFO] Using default state")
    else:
        print("[INFO] No farming state file found, using defaults")
        # Create default home fields (Najika's small farm)
        create_default_fields()

def save_state():
    """Save farming state to file"""
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(FARMING_STATE, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save farming state: {e}")

def create_default_fields():
    """Create default fields for Najika's home farm (V2)"""
    # 4x5 grid = 20 fields in Najika's living space
    fields = []
    field_spacing = 50  # meters apart
    start_x = -100
    start_z = -100

    field_id = 1
    for row in range(4):
        for col in range(5):
            fields.append({
                "field_id": f"farm_field_{field_id:03d}",
                "position": {
                    "x": start_x + (col * field_spacing),
                    "z": start_z + (row * field_spacing)
                },
                "owner": "najika_ai",
                "crop_type": None,
                "planted_at": None,
                "current_stage": None,
                "progress_percent": 0,
                "water_level": 100.0,
                "soil_quality": 100.0,
                "health": 100.0,
                "last_watered": time.time(),
                "weather_affected": False,
                "fertilized": False,
                "ready_to_harvest": False,
                "estimated_yield": 0,
                "actual_yield": None
            })
            field_id += 1

    FARMING_STATE["fields"] = fields
    save_state()
    print(f"[OK] Created {len(fields)} default farm fields")

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_current_season():
    """Get current season (for now, use global state)"""
    return FARMING_STATE["global_season"]

def set_season(season):
    """Set global season (spring/summer/fall/winter)"""
    if season in ["spring", "summer", "fall", "winter"]:
        FARMING_STATE["global_season"] = season
        save_state()
        return True
    return False

def get_current_weather():
    """Get current weather"""
    return FARMING_STATE["global_weather"]

def set_weather(weather):
    """Set global weather (clear/rain/snow/storm)"""
    if weather in ["clear", "rain", "snow", "storm"]:
        FARMING_STATE["global_weather"] = weather
        save_state()
        return True
    return False

def get_region_from_position(position):
    """Determine region from position (simplified)"""
    # For now, all fields in Najika's home are in Samtmoos-Tiefwald
    # Later: use actual region boundaries
    return "Samtmoos-Tiefwald"

def get_field_by_id(field_id):
    """Get field by ID"""
    for field in FARMING_STATE["fields"]:
        if field["field_id"] == field_id:
            return field
    return None

# =====================================================
# FARMING ACTIONS
# =====================================================

def plant_crop(field_id, crop_type, planter="player"):
    """Plant a seed in a field"""

    field = get_field_by_id(field_id)
    if not field:
        return {"success": False, "error": f"Field {field_id} not found"}

    # Check if field is empty
    if field["crop_type"] is not None:
        return {"success": False, "error": "Field already has a crop planted"}

    # Check if crop type exists
    if crop_type not in CROPS:
        return {"success": False, "error": f"Unknown crop type: {crop_type}"}

    crop = CROPS[crop_type]

    # Check season
    current_season = get_current_season()
    if current_season not in crop["seasons"]:
        return {
            "success": False,
            "error": f"{crop['name']} cannot be planted in {current_season}"
        }

    # Check region (for special crops)
    if crop["regions"] != ["all"]:
        field_region = get_region_from_position(field["position"])
        if field_region not in crop["regions"] and "all" not in crop["regions"]:
            return {
                "success": False,
                "error": f"{crop['name']} cannot grow in {field_region}"
            }

    # PLANT!
    current_time = time.time()
    field["crop_type"] = crop_type
    field["planted_at"] = current_time
    field["current_stage"] = "planted"
    field["progress_percent"] = 0
    field["owner"] = planter
    field["water_level"] = 100.0  # Fresh planted = well watered
    field["last_watered"] = current_time
    field["ready_to_harvest"] = False

    FARMING_STATE["total_crops_planted"] += 1
    save_state()

    harvest_time = current_time + crop["growth_time"]

    return {
        "success": True,
        "message": f"{crop['name']} planted successfully!",
        "field_id": field_id,
        "crop_name": crop['name'],
        "harvest_time": harvest_time,
        "estimated_hours": crop["growth_time"] / 3600.0
    }

def water_field(field_id):
    """Water a field"""

    field = get_field_by_id(field_id)
    if not field:
        return {"success": False, "error": f"Field {field_id} not found"}

    if field["crop_type"] is None:
        return {"success": False, "error": "Cannot water empty field"}

    # Water it!
    old_level = field["water_level"]
    field["water_level"] = min(100.0, field["water_level"] + 50.0)
    field["last_watered"] = time.time()

    # Health improves if it was low on water
    if old_level < 30:
        field["health"] = min(100.0, field["health"] + 10.0)

    save_state()

    return {
        "success": True,
        "message": "Field watered!",
        "water_level": field["water_level"],
        "health": field["health"]
    }

def fertilize_field(field_id):
    """Fertilize a field (improves soil quality)"""

    field = get_field_by_id(field_id)
    if not field:
        return {"success": False, "error": f"Field {field_id} not found"}

    if field["fertilized"]:
        return {"success": False, "error": "Field already fertilized"}

    # Fertilize!
    old_quality = field["soil_quality"]
    field["soil_quality"] = min(100.0, field["soil_quality"] + 30.0)
    field["fertilized"] = True

    save_state()

    return {
        "success": True,
        "message": "Field fertilized!",
        "soil_quality": field["soil_quality"],
        "improvement": field["soil_quality"] - old_quality
    }

def harvest_crop(field_id):
    """Harvest a crop from a field"""

    field = get_field_by_id(field_id)
    if not field:
        return {"success": False, "error": f"Field {field_id} not found"}

    if not field["ready_to_harvest"]:
        return {"success": False, "error": "Crop is not ready to harvest yet"}

    crop = CROPS[field["crop_type"]]

    # Calculate final yield based on care quality
    care_quality = (
        field["water_level"] / 100.0 +
        field["soil_quality"] / 100.0 +
        field["health"] / 100.0
    ) / 3.0

    actual_yield = int(
        crop["yield_min"] +
        (crop["yield_max"] - crop["yield_min"]) * care_quality
    )

    # Determine quality
    if care_quality >= 0.8:
        quality = "excellent"
        price_multiplier = 1.5
    elif care_quality >= 0.6:
        quality = "good"
        price_multiplier = 1.2
    elif care_quality >= 0.4:
        quality = "normal"
        price_multiplier = 1.0
    else:
        quality = "poor"
        price_multiplier = 0.7

    # Items harvested
    harvested_items = {
        "item_id": field["crop_type"],
        "name": crop["name"],
        "quantity": actual_yield,
        "quality": quality,
        "sell_price_each": int(crop["sell_price"] * price_multiplier),
        "total_value": int(crop["sell_price"] * price_multiplier * actual_yield)
    }

    # Bonuses
    bonuses = {}
    if "hunger_value" in crop:
        bonuses["hunger_value"] = crop["hunger_value"] * actual_yield
    if "energy_bonus" in crop:
        bonuses["energy_bonus"] = crop["energy_bonus"] * actual_yield
    if "mood_bonus" in crop:
        bonuses["mood_bonus"] = crop["mood_bonus"] * actual_yield

    # Soil quality decreases after harvest
    field["soil_quality"] = max(20.0, field["soil_quality"] - 15.0)

    # Reset field
    crop_name = crop["name"]
    field["crop_type"] = None
    field["planted_at"] = None
    field["current_stage"] = None
    field["progress_percent"] = 0
    field["ready_to_harvest"] = False
    field["actual_yield"] = actual_yield
    field["fertilized"] = False
    field["water_level"] = 100.0
    field["health"] = 100.0

    FARMING_STATE["total_harvests"] += 1
    save_state()

    xp_gained = actual_yield * 5
    if quality == "excellent":
        xp_gained = int(xp_gained * 1.5)

    return {
        "success": True,
        "message": f"Harvested {actual_yield}x {crop_name} ({quality} quality)!",
        "items": harvested_items,
        "bonuses": bonuses,
        "xp_gained": xp_gained,
        "field_id": field_id
    }

# =====================================================
# GROWTH UPDATE
# =====================================================

def update_crop_growth(field):
    """Update crop growth over time"""

    if field["crop_type"] is None:
        return  # Empty field

    crop = CROPS[field["crop_type"]]
    current_time = time.time()
    elapsed = current_time - field["planted_at"]

    # Base progress (0-100%)
    base_progress = (elapsed / crop["growth_time"]) * 100

    # Modifiers
    water_modifier = field["water_level"] / 100.0
    soil_modifier = field["soil_quality"] / 100.0
    health_modifier = field["health"] / 100.0

    # Growth rate (average of all factors)
    growth_rate = (water_modifier + soil_modifier + health_modifier) / 3.0

    # Water decreases over time
    hours_since_water = (current_time - field["last_watered"]) / 3600.0
    water_decay = hours_since_water * 15.0  # -15% per hour
    field["water_level"] = max(0, field["water_level"] - water_decay)

    # Low water damages health
    if field["water_level"] < 20:
        health_decay = hours_since_water * 5.0
        field["health"] = max(0, field["health"] - health_decay)

    # Weather effects
    weather = get_current_weather()
    weather_bonus = 1.0
    if weather == "rain":
        field["water_level"] = min(100, field["water_level"] + 20.0)
        weather_bonus = 1.1
    elif weather == "storm":
        field["health"] = max(0, field["health"] - 10.0)
        weather_bonus = 0.9

    # Final progress
    field["progress_percent"] = min(100, base_progress * growth_rate * weather_bonus)

    # Determine stage
    if field["progress_percent"] >= 100:
        field["current_stage"] = "harvestable"
        field["ready_to_harvest"] = True
    elif field["progress_percent"] >= 60:
        field["current_stage"] = "growing"
    elif field["progress_percent"] >= 25:
        field["current_stage"] = "sprouting"
    else:
        field["current_stage"] = "planted"

    # Estimate yield
    care_quality = (water_modifier + soil_modifier + health_modifier) / 3.0
    field["estimated_yield"] = int(
        crop["yield_min"] +
        (crop["yield_max"] - crop["yield_min"]) * care_quality
    )

    # Update last watered time
    field["last_watered"] = current_time

def update_all_fields():
    """Update all fields (call this periodically)"""

    for field in FARMING_STATE["fields"]:
        if field["crop_type"] is not None:
            update_crop_growth(field)

    FARMING_STATE["last_update"] = time.time()
    save_state()

# =====================================================
# AI AUTO-FARMING (Najika farms when hungry)
# =====================================================

def najika_auto_farm(living_state):
    """Najika automatically farms when hungry (AI mode)"""

    if living_state.get("control_mode") != "ai":
        return []  # Player is in control

    actions_taken = []

    # If hunger < 30%, harvest ready crops
    if living_state.get("hunger", 100) < 30:
        for field in FARMING_STATE["fields"]:
            if field["ready_to_harvest"]:
                result = harvest_crop(field["field_id"])
                if result["success"]:
                    actions_taken.append({
                        "action": "harvest",
                        "result": result
                    })

    # If hunger < 20%, plant fast-growing crops
    if living_state.get("hunger", 100) < 20:
        for field in FARMING_STATE["fields"]:
            if field["crop_type"] is None:
                # Plant carrots (fastest crop)
                result = plant_crop(field["field_id"], "carrot", planter="najika_ai")
                if result["success"]:
                    actions_taken.append({
                        "action": "plant",
                        "result": result
                    })
                    break  # Only plant one at a time

    # Water dying crops
    for field in FARMING_STATE["fields"]:
        if field["crop_type"] and field["water_level"] < 20:
            result = water_field(field["field_id"])
            if result["success"]:
                actions_taken.append({
                    "action": "water",
                    "result": result
                })

    return actions_taken

# =====================================================
# STATUS & STATS
# =====================================================

def get_farming_status():
    """Get complete farming status"""

    update_all_fields()

    # Count fields by state
    total_fields = len(FARMING_STATE["fields"])
    planted_fields = sum(1 for f in FARMING_STATE["fields"] if f["crop_type"] is not None)
    harvestable_fields = sum(1 for f in FARMING_STATE["fields"] if f["ready_to_harvest"])
    empty_fields = total_fields - planted_fields

    # Get all crops currently growing
    growing_crops = []
    for field in FARMING_STATE["fields"]:
        if field["crop_type"]:
            crop = CROPS[field["crop_type"]]
            growing_crops.append({
                "field_id": field["field_id"],
                "crop_name": crop["name"],
                "stage": field["current_stage"],
                "progress": field["progress_percent"],
                "water_level": field["water_level"],
                "health": field["health"],
                "estimated_yield": field["estimated_yield"],
                "ready": field["ready_to_harvest"]
            })

    return {
        "total_fields": total_fields,
        "planted_fields": planted_fields,
        "harvestable_fields": harvestable_fields,
        "empty_fields": empty_fields,
        "growing_crops": growing_crops,
        "season": FARMING_STATE["global_season"],
        "weather": FARMING_STATE["global_weather"],
        "total_harvests": FARMING_STATE["total_harvests"],
        "total_crops_planted": FARMING_STATE["total_crops_planted"]
    }

def get_all_crop_types():
    """Get list of all available crop types"""
    return {
        crop_id: {
            "name": crop["name"],
            "type": crop["type"],
            "growth_time_hours": crop["growth_time"] / 3600.0,
            "seasons": crop["seasons"],
            "sell_price": crop["sell_price"],
            "regions": crop["regions"]
        }
        for crop_id, crop in CROPS.items()
    }

# =====================================================
# INITIALIZATION
# =====================================================

# Load state on import
load_state()

if __name__ == "__main__":
    print("="*60)
    print("NAJIKA FARMING SYSTEM - TEST")
    print("="*60)

    # Test planting
    print("\n[TEST] Planting carrots...")
    result = plant_crop("farm_field_001", "carrot", "test_player")
    print(f"Result: {result}")

    # Test watering
    print("\n[TEST] Watering field...")
    result = water_field("farm_field_001")
    print(f"Result: {result}")

    # Test status
    print("\n[TEST] Getting farming status...")
    status = get_farming_status()
    print(f"Total fields: {status['total_fields']}")
    print(f"Planted: {status['planted_fields']}")
    print(f"Harvestable: {status['harvestable_fields']}")
    print(f"Season: {status['season']}")

    print("\n[OK] Farming System tests complete!")
