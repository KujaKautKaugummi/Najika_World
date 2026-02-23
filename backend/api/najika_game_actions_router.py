"""
Najika Game Actions Router
Exposes najika_game_actions.py functionality via FastAPI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import sys
import os

# Import the game actions module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from najika_game_actions import (
    LOCATIONS, COOKING_RECIPES, AUTONOMOUS_CRAFTING_RECIPES,
    EXPLORING_ACTIONS, FARMING_ACTIONS,
    GAME_ACTION_STATE,
    decide_next_action, complete_action,
    choose_cooking_recipe, choose_crafting_recipe,
    choose_exploring_action, choose_farming_action,
    check_action_completion,
    export_game_action_state
)
from backend.utils import handle_errors

router = APIRouter(prefix="/najika", tags=["Najika Game Actions"])


class TeleportRequest(BaseModel):
    location_id: str


class RecipeRequest(BaseModel):
    recipe_id: str


class ActionRequest(BaseModel):
    action_id: str
    params: Optional[Dict[str, Any]] = None


@router.get("/status")
@handle_errors()
async def get_najika_status():
    """Get Najika's complete status (location, hunger, energy, mood, activity)"""
    return export_game_action_state()


@router.get("/current-activity")
@handle_errors()
async def get_najika_activity():
    """Get what Najika is currently doing"""
    activity = GAME_ACTION_STATE.get("current_activity")
    if activity:
        return {
            "success": True,
            "activity": activity,
            "started_at": GAME_ACTION_STATE.get("activity_started_at"),
            "progress": check_action_completion()
        }
    return {"success": True, "activity": None, "message": "Najika is idle"}


@router.post("/suggest-action")
@handle_errors()
async def suggest_next_action():
    """Suggest next action based on current state"""
    # Analyze current state and suggest actions
    hunger = GAME_ACTION_STATE.get("hunger", 100)
    energy = GAME_ACTION_STATE.get("energy", 100)
    mood = GAME_ACTION_STATE.get("mood", 70)

    suggestions = []

    if hunger < 30:
        suggestions.append({"type": "cooking", "reason": "Najika is hungry", "priority": "high"})
    if energy < 20:
        suggestions.append({"type": "sleep", "reason": "Najika is tired", "priority": "critical"})
    if mood < 40:
        suggestions.append({"type": "explore", "reason": "Najika is bored", "priority": "medium"})
    if mood > 70:
        suggestions.append({"type": "crafting", "reason": "Najika is happy and wants to create", "priority": "low"})

    return {"success": True, "suggestions": suggestions, "state": export_game_action_state()}


@router.post("/auto-decide-action")
@handle_errors()
async def auto_decide_action():
    """Najika autonomously decides her next action!"""
    result = decide_next_action()
    return result


@router.get("/locations")
@handle_errors()
async def get_locations():
    """Get all available locations"""
    return {"success": True, "locations": list(LOCATIONS.values())}


@router.post("/teleport")
@handle_errors()
async def teleport_to_location(request: TeleportRequest):
    """Teleport Najika to a location"""
    if request.location_id not in LOCATIONS:
        raise HTTPException(status_code=404, detail=f"Location '{request.location_id}' not found")

    location = LOCATIONS[request.location_id]
    GAME_ACTION_STATE["current_location"] = request.location_id

    return {
        "success": True,
        "message": f"Najika teleported to {location['name']}!",
        "location": location,
        "new_state": export_game_action_state()
    }


@router.get("/recipes")
@handle_errors()
async def get_recipes():
    """Get all available recipes (cooking & crafting)"""
    all_recipes = {
        "cooking": list(COOKING_RECIPES.values()),
        "crafting": list(AUTONOMOUS_CRAFTING_RECIPES.values())
    }
    return {"success": True, "recipes": all_recipes}


@router.get("/actions")
@handle_errors()
async def get_actions():
    """Get all available actions"""
    all_actions = {
        "exploring": list(EXPLORING_ACTIONS.values()),
        "farming": list(FARMING_ACTIONS.values())
    }
    return {"success": True, "actions": all_actions}


@router.post("/cook")
@handle_errors()
async def cook_recipe(request: RecipeRequest):
    """Cook a recipe"""
    result = choose_cooking_recipe(request.recipe_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Cooking failed"))
    return result


@router.post("/craft")
@handle_errors()
async def craft_recipe(request: RecipeRequest):
    """Craft an item"""
    result = choose_crafting_recipe(request.recipe_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Crafting failed"))
    return result


@router.post("/explore")
@handle_errors()
async def explore_action(request: ActionRequest):
    """Start an exploring action"""
    result = choose_exploring_action(request.action_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Exploring failed"))
    return result


@router.post("/farm")
@handle_errors()
async def farm_action(request: ActionRequest):
    """Start a farming action"""
    result = choose_farming_action(request.action_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Farming failed"))
    return result


@router.post("/complete-action")
@handle_errors()
async def complete_current_action():
    """Complete the current activity"""
    result = complete_action()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Completion failed"))
    return result


@router.get("/dashboard")
@handle_errors()
async def get_dashboard():
    """Get complete Najika dashboard (status + recipes + locations + actions)"""
    return {
        "success": True,
        "status": export_game_action_state(),
        "current_activity": GAME_ACTION_STATE.get("current_activity"),
        "locations": list(LOCATIONS.values()),
        "cooking_recipes": list(COOKING_RECIPES.values()),
        "crafting_recipes": list(AUTONOMOUS_CRAFTING_RECIPES.values()),
        "exploring_actions": list(EXPLORING_ACTIONS.values()),
        "farming_actions": list(FARMING_ACTIONS.values())
    }


@router.get("/health")
@handle_errors()
async def health_check():
    """Health check for Game Actions system"""
    return {
        "success": True,
        "system": "Najika Game Actions",
        "status": "operational",
        "state_initialized": GAME_ACTION_STATE is not None,
        "locations_count": len(LOCATIONS),
        "recipes_count": len(COOKING_RECIPES) + len(AUTONOMOUS_CRAFTING_RECIPES),
        "actions_count": len(EXPLORING_ACTIONS) + len(FARMING_ACTIONS)
    }