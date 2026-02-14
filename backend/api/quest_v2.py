"""
Quest System Router V2 - Nutzt Shared State
Quests generieren, annehmen, Fortschritt tracken, abschliessen.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import random
import time
import sys
import os
import logging

logger = logging.getLogger("najika.api.quest_v2")

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from backend.shared_state import STATE

# Quest System Import (graceful)
QUEST_SYSTEM_AVAILABLE = False
_quest_system = None

try:
    from najika_quest_system import get_quest_system
    _quest_system = get_quest_system()
    QUEST_SYSTEM_AVAILABLE = True
    logger.info("Quest System geladen")
except ImportError as e:
    logger.warning(f"Quest System nicht verfuegbar: {e}")

router = APIRouter(prefix="/api/v2/quest", tags=["Quest V2"])


# ============================================================================
# MODELS
# ============================================================================

class QuestStartRequest(BaseModel):
    quest_id: str


class QuestUpdateRequest(BaseModel):
    quest_id: str
    objective_id: str
    progress: int = 1


# ============================================================================
# IN-MEMORY QUEST STATE (falls kein Backend-System)
# ============================================================================

_quest_state = {
    "available": [],
    "active": [],
    "completed": [],
    "stats": {"total_completed": 0, "total_xp_earned": 0, "total_gold_earned": 0},
}

# Vorgefertigte Quest-Templates
_QUEST_TEMPLATES = [
    {
        "id": "hunt_wolves",
        "title": "Wolfjagd",
        "description": "Besiege 5 Woelfe im Samtmoos-Tiefwald.",
        "objectives": [{"id": "kill_wolves", "description": "Woelfe besiegen", "target": 5, "current": 0}],
        "rewards": {"xp": 100, "gold": 50},
        "min_level": 1,
        "region": "samtmoos_tiefwald",
    },
    {
        "id": "gather_herbs",
        "title": "Kraeutersammlung",
        "description": "Sammle 10 Heilkraeuter im Gruenschlamm-Sumpf.",
        "objectives": [{"id": "collect_herbs", "description": "Heilkraeuter sammeln", "target": 10, "current": 0}],
        "rewards": {"xp": 75, "gold": 30},
        "min_level": 1,
        "region": "gruenschlamm_sumpf",
    },
    {
        "id": "arena_champion",
        "title": "Arena-Champion",
        "description": "Gewinne 3 Kaempfe in der Arena.",
        "objectives": [{"id": "win_battles", "description": "Arena-Kaempfe gewinnen", "target": 3, "current": 0}],
        "rewards": {"xp": 200, "gold": 100},
        "min_level": 3,
        "region": "kampfarena",
    },
    {
        "id": "explore_caves",
        "title": "Tiefenforschung",
        "description": "Erkunde 3 Bereiche der Tiefenhoehlen.",
        "objectives": [{"id": "explore", "description": "Hoehlen-Bereiche erkunden", "target": 3, "current": 0}],
        "rewards": {"xp": 150, "gold": 75},
        "min_level": 5,
        "region": "tiefenhoehlen",
    },
    {
        "id": "deliver_mail",
        "title": "Postman-Auftrag",
        "description": "Liefere 3 Pakete fuer den Postman-Orden ab.",
        "objectives": [{"id": "deliver", "description": "Pakete abliefern", "target": 3, "current": 0}],
        "rewards": {"xp": 80, "gold": 60},
        "min_level": 1,
        "region": "*",
    },
    {
        "id": "craft_potion",
        "title": "Alchemie-Lehrling",
        "description": "Braue deinen ersten Heiltrank.",
        "objectives": [{"id": "craft", "description": "Heiltrank brauen", "target": 1, "current": 0}],
        "rewards": {"xp": 50, "gold": 20},
        "min_level": 1,
        "region": "gruenschlamm_sumpf",
    },
    {
        "id": "desert_survival",
        "title": "Wuestenueberlebender",
        "description": "Ueberlebe 5 Tage in den Heissen Duenen ohne zu sterben.",
        "objectives": [{"id": "survive", "description": "Tage ueberleben", "target": 5, "current": 0}],
        "rewards": {"xp": 250, "gold": 120},
        "min_level": 5,
        "region": "heisse_duenen",
    },
    {
        "id": "befriend_faction",
        "title": "Diplomatie",
        "description": "Erreiche 'Geschaetzt' Ruf bei einer Fraktion.",
        "objectives": [{"id": "reputation", "description": "Geschaetzt-Status erreichen", "target": 1, "current": 0}],
        "rewards": {"xp": 300, "gold": 150},
        "min_level": 3,
        "region": "*",
    },
]

def _init_quests():
    """Initialisiert verfuegbare Quests"""
    if _quest_state["available"]:
        return
    player_level = STATE["user"].get("level", 1)
    completed_ids = {q["id"] for q in _quest_state["completed"]}
    active_ids = {q["id"] for q in _quest_state["active"]}

    for qt in _QUEST_TEMPLATES:
        if qt["id"] not in completed_ids and qt["id"] not in active_ids:
            if qt["min_level"] <= player_level:
                _quest_state["available"].append(dict(qt))


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/available")
async def get_available_quests():
    """Verfuegbare Quests (basierend auf Spieler-Level)"""
    if QUEST_SYSTEM_AVAILABLE and _quest_system:
        try:
            return _quest_system.get_available_quests(player_level=STATE["user"]["level"])
        except Exception:
            pass

    _init_quests()
    return {"quests": _quest_state["available"], "count": len(_quest_state["available"])}


@router.get("/active")
async def get_active_quests():
    """Aktive Quests"""
    if QUEST_SYSTEM_AVAILABLE and _quest_system:
        try:
            return _quest_system.get_active_quests()
        except Exception:
            pass

    return {"quests": _quest_state["active"], "count": len(_quest_state["active"])}


@router.post("/start")
async def start_quest(request: QuestStartRequest):
    """Quest starten"""
    if QUEST_SYSTEM_AVAILABLE and _quest_system:
        try:
            return _quest_system.start_quest(request.quest_id)
        except Exception:
            pass

    _init_quests()

    quest = None
    for i, q in enumerate(_quest_state["available"]):
        if q["id"] == request.quest_id:
            quest = _quest_state["available"].pop(i)
            break

    if not quest:
        raise HTTPException(404, f"Quest '{request.quest_id}' nicht gefunden oder nicht verfuegbar")

    quest["started_at"] = time.time()
    quest["status"] = "active"
    _quest_state["active"].append(quest)

    return {"success": True, "quest": quest}


@router.post("/update")
async def update_quest_progress(request: QuestUpdateRequest):
    """Quest-Fortschritt updaten"""
    if QUEST_SYSTEM_AVAILABLE and _quest_system:
        try:
            return _quest_system.update_progress(
                quest_id=request.quest_id,
                objective_id=request.objective_id,
                progress=request.progress,
            )
        except Exception:
            pass

    quest = None
    for q in _quest_state["active"]:
        if q["id"] == request.quest_id:
            quest = q
            break

    if not quest:
        raise HTTPException(404, f"Quest '{request.quest_id}' ist nicht aktiv")

    for obj in quest.get("objectives", []):
        if obj["id"] == request.objective_id:
            obj["current"] = min(obj["target"], obj["current"] + request.progress)
            break

    # Check ob alle Objectives erfuellt
    all_complete = all(
        obj["current"] >= obj["target"]
        for obj in quest.get("objectives", [])
    )

    return {
        "success": True,
        "quest": quest,
        "all_objectives_complete": all_complete,
    }


@router.post("/complete/{quest_id}")
async def complete_quest(quest_id: str):
    """Quest abschliessen und Rewards erhalten"""
    if QUEST_SYSTEM_AVAILABLE and _quest_system:
        try:
            result = _quest_system.complete_quest(quest_id)
            STATE["user"]["xp"] += result.get("rewards", {}).get("xp", 0)
            STATE["user"]["points"] += result.get("rewards", {}).get("gold", 0)
            return result
        except Exception:
            pass

    quest = None
    for i, q in enumerate(_quest_state["active"]):
        if q["id"] == quest_id:
            quest = _quest_state["active"].pop(i)
            break

    if not quest:
        raise HTTPException(404, f"Quest '{quest_id}' ist nicht aktiv")

    # Objectives pruefen
    all_complete = all(
        obj["current"] >= obj["target"]
        for obj in quest.get("objectives", [])
    )
    if not all_complete:
        _quest_state["active"].append(quest)
        raise HTTPException(400, "Nicht alle Objectives erfuellt!")

    # Rewards anwenden
    rewards = quest.get("rewards", {})
    xp_reward = rewards.get("xp", 0)
    gold_reward = rewards.get("gold", 0)

    STATE["user"]["xp"] += xp_reward
    STATE["user"]["points"] += gold_reward
    STATE["najika"]["xp"] += xp_reward

    quest["completed_at"] = time.time()
    quest["status"] = "completed"
    _quest_state["completed"].append(quest)
    STATE["progress"]["quests_completed"].append(quest_id)

    _quest_state["stats"]["total_completed"] += 1
    _quest_state["stats"]["total_xp_earned"] += xp_reward
    _quest_state["stats"]["total_gold_earned"] += gold_reward

    return {
        "success": True,
        "quest": quest,
        "rewards": {"xp": xp_reward, "gold": gold_reward},
    }


@router.get("/stats")
async def quest_stats():
    """Quest-Statistiken"""
    return {
        "stats": _quest_state["stats"],
        "active_count": len(_quest_state["active"]),
        "completed_count": len(_quest_state["completed"]),
        "available_count": len(_quest_state["available"]),
    }
