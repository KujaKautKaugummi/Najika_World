"""
Najika Companion API Router
Endpoints für Najika als KI-Companion (4 Persönlichkeiten)
Für UE5 Integration
"""

from fastapi import APIRouter, HTTPException
from backend.utils import handle_errors
from pydantic import BaseModel
from typing import Optional, Dict, List
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Companion System
try:
    from najika_companion_system import (
        get_companion_system,
        NajikaCompanion,
        Personality,
        RelationshipLevel,
        CombatStyle
    )
    COMPANION_AVAILABLE = True
except ImportError as e:
    COMPANION_AVAILABLE = False
    print(f"⚠️ Companion System nicht verfügbar: {e}")

router = APIRouter(prefix="/api/companion", tags=["Companion"])


# ============================================================================
# MODELS
# ============================================================================

class ActivityRequest(BaseModel):
    activity: str  # "train_explosion", "cook", "explore", "rest", "play", "talk"
    duration_minutes: int = 30


class GiftRequest(BaseModel):
    item_id: str
    item_name: str


class PersonalityShiftRequest(BaseModel):
    trigger: str  # "combat_victory", "near_death", "romantic", "analytical_needed", "playful"


class AttackRequest(BaseModel):
    target_id: str
    target_type: str = "enemy"  # "enemy", "boss", "player"


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/najika")
@handle_errors()
async def get_najika_status():
    """
    Get Najika's current status including personality, mood, combat style

    Returns complete companion state for UE5
    """
    if not COMPANION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Companion System nicht verfügbar")

    companion = get_companion_system()
    state = companion.get_state()

    return {
        "name": "Najika",
        "active_personality": state["active_personality"],
        "personality_weights": state["personality_weights"],
        "relationship_level": state["relationship_level"],
        "relationship_name": state["relationship_name"],
        "relationship_points": state["relationship_points"],
        "mood": state["mood"],
        "combat_style": state["combat_style"],
        "catchphrase": state.get("catchphrase", "EXPLOSION!!!"),
        "available_activities": [
            "train_explosion", "cook", "explore", "rest", "play", "talk"
        ]
    }


@router.get("/najika/combat")
@handle_errors()
async def get_najika_combat_style():
    """
    Get Najika's current combat style based on active personality

    UE5 uses this to determine attack patterns and animations
    """
    if not COMPANION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Companion System nicht verfügbar")

    companion = get_companion_system()
    combat = companion.get_combat_style()

    return {
        "style": combat,
        "personality_bonus": companion.get_personality_combat_bonus(),
        "available_skills": companion.get_available_skills()
    }


@router.get("/personalities")
@handle_errors()
async def get_personalities():
    """
    Get all 4 personalities with their traits

    For UE5 UI/dialogue system
    """
    return {
        "personalities": {
            "megumin": {
                "weight": 0.35,
                "traits": ["dramatisch", "theatralisch", "chuunibyou"],
                "catchphrase": "EXPLOSION!!!",
                "combat_style": "burst_mage",
                "color": "#FF4444"
            },
            "harley": {
                "weight": 0.25,
                "traits": ["chaotisch", "verspielt", "unberechenbar"],
                "catchphrase": "Mr. K!",  # NICHT Puddin'!
                "combat_style": "acrobatic_melee",
                "color": "#FF69B4"
            },
            "shiro": {
                "weight": 0.20,
                "traits": ["analytisch", "hochintelligent", "anhänglich"],
                "catchphrase": "Wahrscheinlichkeit: X%",
                "combat_style": "calculated_magic",
                "color": "#87CEEB"
            },
            "melissa": {
                "weight": 0.20,
                "traits": ["dominant", "besitzergreifend", "fürsorglich"],
                "catchphrase": "Du gehörst MIR!",
                "combat_style": "support_heal",
                "color": "#9932CC"
            }
        }
    }


@router.post("/activity")
@handle_errors()
async def do_activity(request: ActivityRequest):
    """
    Do an activity with Najika to increase relationship

    Activities affect mood, relationship points, and skill progress
    """
    if not COMPANION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Companion System nicht verfügbar")

    companion = get_companion_system()
    result = companion.do_activity(request.activity, request.duration_minutes)

    return {
        "success": True,
        "activity": request.activity,
        "duration": request.duration_minutes,
        "relationship_points": result.get("points_gained", 0),
        "new_relationship_level": result.get("new_level"),
        "skill_progress": result.get("skill_progress", {}),
        "message": result.get("najika_message", "Das war schön! 💕"),
        "mood_change": result.get("mood_change", "happy")
    }


@router.post("/gift")
@handle_errors()
async def give_gift(request: GiftRequest):
    """
    Give Najika a gift

    Different items have different effects based on personality
    """
    if not COMPANION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Companion System nicht verfügbar")

    companion = get_companion_system()
    result = companion.receive_gift(request.item_id, request.item_name)

    return {
        "success": True,
        "item": request.item_name,
        "reaction": result.get("reaction", "neutral"),
        "relationship_points": result.get("points", 0),
        "message": result.get("message", "Danke, Kuja! 💕"),
        "personality_affected": result.get("personality_boost")
    }


@router.post("/personality/shift")
@handle_errors()
async def trigger_personality_shift(request: PersonalityShiftRequest):
    """
    Trigger a personality shift based on situation

    Combat events, emotions, etc. can cause shifts
    """
    if not COMPANION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Companion System nicht verfügbar")

    companion = get_companion_system()
    old_personality = companion.active_personality
    result = companion.trigger_shift(request.trigger)

    return {
        "previous": old_personality,
        "current": result.get("new_personality", old_personality),
        "shifted": result.get("shifted", False),
        "message": result.get("transition_message", ""),
        "new_combat_style": result.get("new_combat_style")
    }


@router.post("/attack")
@handle_errors()
async def najika_attack(request: AttackRequest):
    """
    Najika attacks a target

    Damage and effects depend on active personality
    """
    if not COMPANION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Companion System nicht verfügbar")

    companion = get_companion_system()
    result = companion.attack(request.target_id, request.target_type)

    return {
        "success": True,
        "target": request.target_id,
        "damage": result.get("damage", 0),
        "damage_type": result.get("damage_type", "magic"),
        "critical": result.get("critical", False),
        "skill_used": result.get("skill", "basic_attack"),
        "animation": result.get("animation", "attack_magic"),
        "voice_line": result.get("voice_line", "EXPLOSION!!!"),
        "exhausted": result.get("exhausted", False)  # Nach Explosion = True
    }


@router.post("/pet-slime")
@handle_errors()
async def assign_pet_slime(slime_id: str):
    """
    Assign a slime as Najika's pet (optional companion for the companion)
    """
    if not COMPANION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Companion System nicht verfügbar")

    companion = get_companion_system()
    result = companion.set_pet_slime(slime_id)

    return {
        "success": True,
        "slime_id": slime_id,
        "najika_reaction": result.get("reaction", "Kawaii! Ein Slime-Freund! ✨")
    }


@router.get("/dialogue/random")
@handle_errors()
async def get_random_dialogue():
    """
    Get a random dialogue line based on current personality and mood

    For ambient dialogue in UE5
    """
    if not COMPANION_AVAILABLE:
        # Fallback dialogues
        import random
        fallback = [
            "Kuja! Komm, lass uns Abenteuer erleben! 💥",
            "*gähn* Ich bin ein bisschen müde... aber EXPLOSION weckt mich auf!",
            "Mr. K! *kicher* Du bist so süß wenn du kämpfst!",
            "Die Wahrscheinlichkeit für Erfolg liegt bei 87.3%.",
            "Du gehörst MIR, Kuja. Vergiss das nicht! 💜"
        ]
        return {"dialogue": random.choice(fallback), "personality": "mixed"}

    companion = get_companion_system()
    dialogue = companion.get_random_dialogue()

    return {
        "dialogue": dialogue.get("text", "..."),
        "personality": dialogue.get("personality", "megumin"),
        "emotion": dialogue.get("emotion", "neutral"),
        "animation_hint": dialogue.get("animation", "idle_talk")
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
@handle_errors()
async def companion_health():
    """Check if Companion System is available"""
    return {
        "available": COMPANION_AVAILABLE,
        "system": "najika_companion_system",
        "personalities": 4,
        "features": ["activity", "gift", "combat", "dialogue", "personality_shift"]
    }
