"""
State Management Router (V2)
Zentraler State-Endpoint fuer alle Clients.

Nutzt backend.shared_state als Single Source of Truth.
Ersetzt die verstreuten State-Abfragen aus najika_server.py.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from backend.utils import handle_errors
import time

import sys
import os
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from backend.shared_state import STATE, ROOMS, get_state, update_najika_stat

router = APIRouter(prefix="/api/state", tags=["State V2"])


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class NajikaState(BaseModel):
    hunger: int = 100
    thirst: int = 100
    energy: int = 100
    hygiene: int = 100
    happiness: int = 100
    mana: int = 100
    max_mana: int = 100
    strength: int = 10
    intelligence: int = 10
    dexterity: int = 10
    charisma: int = 10
    care_mistakes: int = 0
    fatigue: int = 0
    weight: int = 50
    discipline: int = 0
    level: int = 1
    xp: int = 0
    evolution_stage: str = "base"
    equipment: Dict[str, Optional[str]] = {}


class UserState(BaseModel):
    level: int = 1
    xp: int = 0
    points: int = 0
    inventory: List[Any] = []
    achievements: List[Any] = []


class GameStateResponse(BaseModel):
    najika: Dict[str, Any]
    user: Dict[str, Any]
    battle: Dict[str, Any]
    living: Dict[str, Any]
    private_mode: bool
    behavior_mode: str
    bond_strength: int
    total_interactions: int


class StateUpdateRequest(BaseModel):
    updates: Dict[str, Any]


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/", response_model=GameStateResponse)
@handle_errors()
async def get_game_state():
    """Gesamten Game-State abrufen (ohne sse_clients)"""
    return GameStateResponse(
        najika=STATE["najika"],
        user=STATE["user"],
        battle=STATE["battle"],
        living=STATE["living"],
        private_mode=STATE["private_mode"],
        behavior_mode=STATE["behavior_mode"],
        bond_strength=STATE["bond_strength"],
        total_interactions=STATE["total_interactions"],
    )


@router.get("/najika")
@handle_errors()
async def get_najika_state():
    """Nur Najikas State (Needs, Stats, Equipment)"""
    return STATE["najika"]


@router.post("/najika/update")
@handle_errors()
async def update_najika_state(request: StateUpdateRequest):
    """
    Najika-Stats updaten.

    Beispiel: {"updates": {"hunger": 80, "energy": 50}}
    """
    allowed_keys = set(STATE["najika"].keys()) - {"equipment", "last_fed", "last_trained", "last_sleep", "last_update"}
    updated = {}

    for key, value in request.updates.items():
        if key in allowed_keys:
            update_najika_stat(key, value)
            updated[key] = value

    if not updated:
        raise HTTPException(400, "Keine gueltigen Keys angegeben")

    return {"success": True, "updated": updated, "najika": STATE["najika"]}


@router.get("/user")
@handle_errors()
async def get_user_state():
    """Spieler-State (Level, XP, Inventory)"""
    return STATE["user"]


@router.post("/user/update")
@handle_errors()
async def update_user_state(request: StateUpdateRequest):
    """Spieler-Stats updaten"""
    allowed_keys = {"level", "xp", "points"}
    updated = {}

    for key, value in request.updates.items():
        if key in allowed_keys and key in STATE["user"]:
            STATE["user"][key] = value
            updated[key] = value

    if not updated:
        raise HTTPException(400, "Keine gueltigen Keys angegeben")

    return {"success": True, "updated": updated, "user": STATE["user"]}


@router.get("/battle")
@handle_errors()
async def get_battle_state():
    """Battle-State"""
    return STATE["battle"]


@router.get("/living")
@handle_errors()
async def get_living_state():
    """Living System State (Mood, Needs, Activity)"""
    return STATE["living"]


@router.get("/rooms")
@handle_errors()
async def get_rooms():
    """Alle verfuegbaren Raeume"""
    return {"rooms": ROOMS}


@router.post("/private-mode/toggle")
@handle_errors()
async def toggle_private_mode():
    """Kaetzchen-Modus ein/aus"""
    STATE["private_mode"] = not STATE["private_mode"]
    return {
        "success": True,
        "private_mode": STATE["private_mode"],
    }


@router.get("/private-mode")
@handle_errors()
async def get_private_mode():
    """Kaetzchen-Modus Status"""
    return {"private_mode": STATE["private_mode"]}


@router.post("/behavior-mode")
@handle_errors()
async def set_behavior_mode(mode: str = "standard"):
    """
    Verhaltens-Modus setzen.

    Modi: standard, explosion, chaos, analyse, kontrolle, private
    """
    valid_modes = {"standard", "explosion", "chaos", "analyse", "kontrolle", "private"}
    if mode not in valid_modes:
        raise HTTPException(400, f"Ungueltiger Modus. Erlaubt: {valid_modes}")

    STATE["behavior_mode"] = mode
    return {"success": True, "behavior_mode": mode}


@router.get("/health")
@handle_errors()
async def state_health():
    """Health-Check mit System-Infos"""
    from backend.shared_state import (
        NAJIKA_MEMORY, NAJIKA_SEARCH,
        PERSONALITY_ENGINE_ENABLED, NAJIKA_MIND_ENABLED,
        TTS_ENABLED, SLIME_SYSTEM_ENABLED
    )

    return {
        "status": "healthy",
        "state_keys": list(STATE.keys()),
        "total_interactions": STATE["total_interactions"],
        "bond_strength": STATE["bond_strength"],
        "private_mode": STATE["private_mode"],
        "systems": {
            "memory": NAJIKA_MEMORY is not None,
            "search": NAJIKA_SEARCH is not None,
            "personality_engine": PERSONALITY_ENGINE_ENABLED,
            "mind": NAJIKA_MIND_ENABLED,
            "tts": TTS_ENABLED,
            "slime": SLIME_SYSTEM_ENABLED,
        }
    }
