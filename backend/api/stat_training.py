"""
Najika Stat Training API Router
Learning by Doing System - Stats steigen durch Nutzung
Für UE5 Integration
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Stat Training System
try:
    from najika_stat_training_system import (
        get_stat_training_system,
        Stat,
        TrainingActivity
    )
    STAT_TRAINING_AVAILABLE = True
except ImportError as e:
    STAT_TRAINING_AVAILABLE = False
    print(f"⚠️ Stat Training System nicht verfügbar: {e}")

router = APIRouter(prefix="/api/stat-training", tags=["Stat Training"])


# ============================================================================
# MODELS
# ============================================================================

class TrainingRequest(BaseModel):
    activity: str  # "chop_tree", "run", "read_book", "lockpick", etc.
    duration_seconds: int = 60
    intensity: str = "normal"  # "light", "normal", "intense"


class StatCheckRequest(BaseModel):
    stat: str
    required_value: int


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/stats/{player_id}")
async def get_player_stats(player_id: str):
    """
    Get all stats for a player

    Stats: STR, END, INT, DEX, PER, CHA, LUK
    """
    if not STAT_TRAINING_AVAILABLE:
        # Return default stats
        return {
            "player_id": player_id,
            "stats": {
                "strength": {"value": 10, "xp": 0, "level": 1},
                "endurance": {"value": 10, "xp": 0, "level": 1},
                "intelligence": {"value": 10, "xp": 0, "level": 1},
                "dexterity": {"value": 10, "xp": 0, "level": 1},
                "perception": {"value": 10, "xp": 0, "level": 1},
                "charisma": {"value": 10, "xp": 0, "level": 1},
                "luck": {"value": 5, "xp": 0, "level": 1, "note": "Schwer zu trainieren!"}
            },
            "training_today": {},
            "daily_limit_reached": []
        }

    training = get_stat_training_system()
    return training.get_player_stats(player_id)


@router.get("/activities")
async def get_all_activities():
    """
    Get all training activities and which stats they affect

    Learning by Doing - jede Aktivität trainiert bestimmte Stats
    """
    return {
        "activities": {
            # STÄRKE (STR)
            "chop_tree": {
                "name": "Baum fällen",
                "stats": ["strength"],
                "xp_per_minute": 5,
                "tool_required": "axe"
            },
            "carry_heavy": {
                "name": "Schwere Last tragen",
                "stats": ["strength", "endurance"],
                "xp_per_minute": 3
            },
            "smithing": {
                "name": "Schmieden",
                "stats": ["strength", "dexterity"],
                "xp_per_minute": 4,
                "station_required": "forge"
            },
            "wrestling": {
                "name": "Wrestling/Ringen",
                "stats": ["strength"],
                "xp_per_minute": 6
            },

            # AUSDAUER (END)
            "running": {
                "name": "Laufen/Sprinten",
                "stats": ["endurance"],
                "xp_per_minute": 4
            },
            "swimming": {
                "name": "Schwimmen",
                "stats": ["endurance", "strength"],
                "xp_per_minute": 5
            },
            "climbing": {
                "name": "Bergsteigen",
                "stats": ["endurance", "strength"],
                "xp_per_minute": 6
            },
            "combat": {
                "name": "Kämpfen",
                "stats": ["endurance"],
                "xp_per_minute": 3
            },

            # INTELLIGENZ (INT)
            "read_book": {
                "name": "Buch lesen",
                "stats": ["intelligence"],
                "xp_per_minute": 5
            },
            "solve_puzzle": {
                "name": "Rätsel lösen",
                "stats": ["intelligence"],
                "xp_per_minute": 8
            },
            "research": {
                "name": "Forschen",
                "stats": ["intelligence"],
                "xp_per_minute": 4,
                "station_required": "library"
            },
            "study_magic": {
                "name": "Magie studieren",
                "stats": ["intelligence"],
                "xp_per_minute": 6,
                "unlocks": "new_spells"
            },

            # GESCHICK (DEX)
            "archery": {
                "name": "Bogenschießen",
                "stats": ["dexterity", "perception"],
                "xp_per_minute": 5
            },
            "lockpicking": {
                "name": "Schlösser knacken",
                "stats": ["dexterity"],
                "xp_per_minute": 7
            },
            "pickpocket": {
                "name": "Taschendiebstahl",
                "stats": ["dexterity"],
                "xp_per_minute": 6,
                "risk": "detection"
            },
            "cooking": {
                "name": "Kochen",
                "stats": ["dexterity", "intelligence"],
                "xp_per_minute": 3,
                "station_required": "kitchen"
            },

            # WAHRNEHMUNG (PER)
            "hunting": {
                "name": "Jagen/Spurenlesen",
                "stats": ["perception"],
                "xp_per_minute": 5
            },
            "herb_gathering": {
                "name": "Kräuter sammeln",
                "stats": ["perception", "intelligence"],
                "xp_per_minute": 3
            },
            "trap_detection": {
                "name": "Fallen entdecken",
                "stats": ["perception"],
                "xp_per_minute": 6
            },
            "stargazing": {
                "name": "Sternenkunde",
                "stats": ["perception", "intelligence"],
                "xp_per_minute": 4
            },

            # CHARISMA (CHA)
            "haggling": {
                "name": "Handeln/Feilschen",
                "stats": ["charisma"],
                "xp_per_minute": 5
            },
            "persuading": {
                "name": "Überreden",
                "stats": ["charisma"],
                "xp_per_minute": 6
            },
            "performing": {
                "name": "Auftreten/Musizieren",
                "stats": ["charisma"],
                "xp_per_minute": 4,
                "tool_required": "instrument"
            },
            "leading": {
                "name": "Führen (Gruppe)",
                "stats": ["charisma"],
                "xp_per_minute": 5
            },

            # GLÜCK (LUK) - Schwer zu trainieren!
            "gambling": {
                "name": "Glücksspiel",
                "stats": ["luck"],
                "xp_per_minute": 1,
                "note": "Sehr langsam!"
            },
            "special_event": {
                "name": "Spezial-Event",
                "stats": ["luck"],
                "xp_per_minute": 10,
                "note": "Nur durch besondere Ereignisse"
            },
            "gods_blessing": {
                "name": "Götter-Segen",
                "stats": ["luck"],
                "xp_per_minute": 50,
                "note": "Extrem selten!"
            }
        },
        "daily_limit": {
            "max_training_per_stat": 5,
            "message": "Nach 5x Training pro Tag: 'zu müde'"
        },
        "diminishing_returns": {
            "description": "Wiederholungen werden weniger effektiv",
            "formula": "first: 100%, second: 80%, third: 64%, etc."
        }
    }


@router.get("/scaling")
async def get_weapon_scaling():
    """
    Get weapon scaling grades (Dark Souls Style)

    Higher grade = more bonus damage from stat
    """
    return {
        "grades": {
            "S": {"bonus": 1.4, "description": "Legendär - 140% Bonus"},
            "A": {"bonus": 1.0, "description": "Exzellent - 100% Bonus"},
            "B": {"bonus": 0.75, "description": "Gut - 75% Bonus"},
            "C": {"bonus": 0.5, "description": "Durchschnitt - 50% Bonus"},
            "D": {"bonus": 0.25, "description": "Schwach - 25% Bonus"},
            "E": {"bonus": 0.1, "description": "Minimal - 10% Bonus"},
            "-": {"bonus": 0.0, "description": "Kein Bonus"}
        },
        "example": {
            "weapon": "Langschwert",
            "base_damage": 100,
            "str_scaling": "C",
            "dex_scaling": "C",
            "player_str": 30,
            "player_dex": 25,
            "calculation": "100 + (30 * 0.5) + (25 * 0.5) = 127.5 Schaden"
        }
    }


@router.post("/train")
async def train_stat(player_id: str, request: TrainingRequest):
    """
    Perform a training activity

    Stats improve through doing - Skyrim style!
    """
    if not STAT_TRAINING_AVAILABLE:
        # Simulate training
        xp_gained = request.duration_seconds // 60 * 5
        if request.intensity == "intense":
            xp_gained = int(xp_gained * 1.5)
        elif request.intensity == "light":
            xp_gained = int(xp_gained * 0.5)

        return {
            "success": True,
            "player_id": player_id,
            "activity": request.activity,
            "duration": request.duration_seconds,
            "xp_gained": xp_gained,
            "stats_affected": ["unknown"],
            "message": f"+{xp_gained} XP (Simulation)"
        }

    training = get_stat_training_system()
    result = training.train(player_id, request.activity, request.duration_seconds, request.intensity)

    return {
        "success": result.get("success", False),
        "player_id": player_id,
        "activity": request.activity,
        "duration": request.duration_seconds,
        "xp_gained": result.get("xp_gained", 0),
        "stats_affected": result.get("stats_affected", []),
        "level_ups": result.get("level_ups", []),
        "diminishing_returns": result.get("diminishing_returns", 1.0),
        "daily_limit_reached": result.get("daily_limit_reached", False),
        "message": result.get("message", "Training abgeschlossen!")
    }


@router.post("/check")
async def check_stat_requirement(player_id: str, request: StatCheckRequest):
    """
    Check if player meets a stat requirement

    Returns percentage of requirement met
    """
    if not STAT_TRAINING_AVAILABLE:
        return {
            "player_id": player_id,
            "stat": request.stat,
            "required": request.required_value,
            "current": 10,
            "meets_requirement": 10 >= request.required_value,
            "percentage": min(100, int(10 / request.required_value * 100))
        }

    training = get_stat_training_system()
    result = training.check_requirement(player_id, request.stat, request.required_value)

    return result


@router.get("/milestones/{player_id}")
async def get_milestones(player_id: str):
    """
    Get achieved and upcoming milestones

    Milestones unlock perks at 10, 25, 50, 75, 100
    """
    return {
        "player_id": player_id,
        "milestone_levels": [10, 25, 50, 75, 100],
        "perks_per_milestone": {
            10: "Basic perk unlocked",
            25: "Intermediate perk + efficiency boost",
            50: "Advanced perk + major efficiency boost",
            75: "Expert perk + special ability",
            100: "Master perk + unique ability"
        },
        "example_perks": {
            "strength": {
                10: "Heavy Lifter - +10% carry weight",
                25: "Power Strike - +15% melee damage",
                50: "Titan Grip - Can wield 2H weapons in 1H",
                75: "Unstoppable - Immune to stagger",
                100: "Colossus - +100% melee damage, -50% attack speed"
            },
            "intelligence": {
                10: "Quick Learner - +10% XP gain",
                25: "Mana Well - +25% max mana",
                50: "Spell Mastery - -25% spell cost",
                75: "Dual Mind - Can prepare extra spells",
                100: "Archmage - Spells cost no mana once per battle"
            }
        }
    }


@router.post("/reset-daily/{player_id}")
async def reset_daily_training(player_id: str):
    """
    Reset daily training counters (called at midnight)

    For server-side day change handling
    """
    if not STAT_TRAINING_AVAILABLE:
        return {"success": True, "message": "Daily training reset (simulation)"}

    training = get_stat_training_system()
    result = training.reset_daily(player_id)

    return {
        "success": True,
        "player_id": player_id,
        "message": "Tägliches Training zurückgesetzt!",
        "new_day": True
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def stat_training_health():
    """Check if Stat Training System is available"""
    return {
        "available": STAT_TRAINING_AVAILABLE,
        "system": "najika_stat_training_system",
        "stats": ["strength", "endurance", "intelligence", "dexterity", "perception", "charisma", "luck"],
        "features": ["learning_by_doing", "diminishing_returns", "daily_limits", "milestones", "weapon_scaling"]
    }
