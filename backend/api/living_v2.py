"""
Living System Router V2 - Nutzt Shared State
Najikas Beduerfnisse, Mood, proaktive Nachrichten, Care-Actions.

Ersetzt die getrennten States in living.py durch shared_state.
"""

from fastapi import APIRouter
from backend.utils import handle_errors
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import json
import time
import sys
import os
import logging

logger = logging.getLogger("najika.api.living_v2")

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from backend.shared_state import STATE, update_najika_stat

# Living System Import (graceful)
LIVING_SYSTEM_AVAILABLE = False
try:
    from najika_living_system import (
        detect_mood, update_mood, should_send_proactive_message,
        get_proactive_message, update_living_state, get_living_state_context,
    )
    LIVING_SYSTEM_AVAILABLE = True
    logger.info("Living System verfuegbar")
except ImportError as e:
    logger.warning(f"Living System nicht verfuegbar: {e}")

router = APIRouter(prefix="/api/v2/living", tags=["Living V2"])
care_router = APIRouter(prefix="/api/v2/care", tags=["Care V2"])


# ============================================================================
# MODELS
# ============================================================================

class MoodUpdate(BaseModel):
    mood: str  # happy, sad, angry, excited, explosive, needy, etc.


class CareAction(BaseModel):
    action: str  # feed, drink, sleep, wash, play, train, heal
    item: Optional[str] = None


class NeedsDecayResponse(BaseModel):
    hunger: int
    thirst: int
    energy: int
    hygiene: int
    happiness: int
    mood: str


# ============================================================================
# NEEDS DECAY (aufgerufen von Game-Loop oder Timer)
# ============================================================================

def _apply_needs_decay():
    """Beduerfnisse sinken ueber Zeit"""
    najika = STATE["najika"]
    now = time.time()
    elapsed = now - najika.get("last_update", now)

    # Alle 5 Minuten echte Zeit = 1 Punkt Verlust
    decay_ticks = int(elapsed / 300)
    if decay_ticks <= 0:
        return

    najika["hunger"] = max(0, najika["hunger"] - decay_ticks * 2)
    najika["thirst"] = max(0, najika["thirst"] - decay_ticks * 3)
    najika["energy"] = max(0, najika["energy"] - decay_ticks * 1)
    najika["hygiene"] = max(0, najika["hygiene"] - decay_ticks * 1)

    # Happiness sinkt wenn Beduerfnisse niedrig
    if najika["hunger"] < 30 or najika["thirst"] < 30 or najika["energy"] < 20:
        najika["happiness"] = max(0, najika["happiness"] - decay_ticks)

    najika["last_update"] = now

    # Living State sync
    if "living" in STATE:
        STATE["living"]["hunger"] = najika["hunger"]
        STATE["living"]["energy"] = najika["energy"]


# ============================================================================
# LIVING ENDPOINTS
# ============================================================================

@router.get("/state")
@handle_errors()
async def get_living_state():
    """Kompletter Living State (Needs + Mood + Activity)"""
    _apply_needs_decay()
    return {
        "najika": {
            "hunger": STATE["najika"]["hunger"],
            "thirst": STATE["najika"]["thirst"],
            "energy": STATE["najika"]["energy"],
            "hygiene": STATE["najika"]["hygiene"],
            "happiness": STATE["najika"]["happiness"],
            "fatigue": STATE["najika"]["fatigue"],
        },
        "living": STATE["living"],
        "private_mode": STATE["private_mode"],
        "bond_strength": STATE["bond_strength"],
    }


@router.get("/needs")
@handle_errors()
async def get_needs():
    """Nur die Beduerfnisse"""
    _apply_needs_decay()
    n = STATE["najika"]
    return {
        "hunger": n["hunger"],
        "thirst": n["thirst"],
        "energy": n["energy"],
        "hygiene": n["hygiene"],
        "happiness": n["happiness"],
    }


@router.post("/mood")
@handle_errors()
async def set_mood(update: MoodUpdate):
    """Mood manuell setzen"""
    STATE["living"]["mood"] = update.mood
    if LIVING_SYSTEM_AVAILABLE:
        try:
            update_mood(update.mood)
        except Exception:
            pass
    return {"success": True, "mood": update.mood}


@router.get("/mood")
@handle_errors()
async def get_mood():
    """Aktuellen Mood abrufen"""
    return {"mood": STATE["living"].get("mood", "happy")}


@router.get("/proactive")
@handle_errors()
async def get_proactive_message():
    """Pruefen ob Najika proaktiv sprechen will"""
    if not LIVING_SYSTEM_AVAILABLE:
        return {"should_send": False, "message": None}

    try:
        should_send = should_send_proactive_message(STATE["living"])
        if should_send:
            msg_data = get_proactive_message(STATE["living"])
            return {
                "should_send": True,
                "message": msg_data.get("message", ""),
                "trigger": msg_data.get("trigger", ""),
            }
    except Exception as e:
        logger.error(f"Proactive check error: {e}")

    return {"should_send": False, "message": None}


@router.post("/decay")
@handle_errors()
async def trigger_needs_decay():
    """Needs Decay manuell triggern"""
    _apply_needs_decay()
    n = STATE["najika"]
    return NeedsDecayResponse(
        hunger=n["hunger"],
        thirst=n["thirst"],
        energy=n["energy"],
        hygiene=n["hygiene"],
        happiness=n["happiness"],
        mood=STATE["living"].get("mood", "happy"),
    )


@router.get("/stream")
@handle_errors()
async def living_stream():
    """SSE Stream fuer Living State Updates"""
    async def event_generator():
        while True:
            _apply_needs_decay()
            data = json.dumps({
                "hunger": STATE["najika"]["hunger"],
                "thirst": STATE["najika"]["thirst"],
                "energy": STATE["najika"]["energy"],
                "happiness": STATE["najika"]["happiness"],
                "mood": STATE["living"].get("mood", "happy"),
                "private_mode": STATE["private_mode"],
                "bond_strength": STATE["bond_strength"],
            })
            yield f"data: {data}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ============================================================================
# CARE ENDPOINTS
# ============================================================================

def _care_response(action: str, **deltas):
    """Care-Aktion anwenden und State updaten"""
    n = STATE["najika"]
    for key, delta in deltas.items():
        if key in n:
            n[key] = max(0, min(100, n[key] + delta))

    n["last_update"] = time.time()

    # Bond steigt bei Pflege
    STATE["bond_strength"] = min(100, STATE["bond_strength"] + 1)

    # V1-kompatible Felder (ok, msg, najika) + V2 Felder
    msgs = {
        "feed": "Mmh, lecker! Danke!",
        "drink": "Ahh, erfrischend!",
        "sleep": "Gute Nacht... zzz",
        "wash": "Blitzeblank!",
        "play": "Yay, spielen!",
        "train": "Training macht stark!",
        "heal": "Mir geht's besser!",
        "praise": "Danke, Kuja! Das motiviert mich!",
        "scold": "Okay, ich pass besser auf!",
        "touch": "Hehe, das kitzelt!",
    }

    return {
        "success": True,
        "ok": True,
        "action": action,
        "msg": msgs.get(action, "Aktion ausgefuehrt!"),
        "najika": {
            "hunger": n["hunger"],
            "thirst": n["thirst"],
            "energy": n["energy"],
            "hygiene": n["hygiene"],
            "happiness": n["happiness"],
            "discipline": n.get("discipline", 0),
        },
        "hunger": n["hunger"],
        "thirst": n["thirst"],
        "energy": n["energy"],
        "hygiene": n["hygiene"],
        "happiness": n["happiness"],
        "bond_strength": STATE["bond_strength"],
    }


@care_router.post("/feed")
async def feed_najika():
    """Fuettern - Hunger steigt, Happiness steigt"""
    STATE["najika"]["last_fed"] = time.time()
    return _care_response("feed", hunger=20, happiness=5)


@care_router.post("/drink")
async def drink_najika():
    """Trinken - Thirst steigt"""
    return _care_response("drink", thirst=25, energy=5)


@care_router.post("/sleep")
async def sleep_najika():
    """Schlafen - Energy steigt, Fatigue sinkt"""
    STATE["najika"]["last_sleep"] = time.time()
    return _care_response("sleep", energy=40, fatigue=-30, happiness=5)


@care_router.post("/wash")
async def wash_najika():
    """Waschen - Hygiene steigt"""
    return _care_response("wash", hygiene=30, happiness=3)


@care_router.post("/play")
async def play_najika():
    """Spielen - Happiness steigt, Energy sinkt"""
    return _care_response("play", happiness=15, energy=-10)


@care_router.post("/train")
async def train_najika():
    """Training - Stats steigen, Energy/Fatigue aendern"""
    STATE["najika"]["last_trained"] = time.time()
    # Zufaelliger Stat-Boost
    import random
    stat = random.choice(["strength", "intelligence", "dexterity", "charisma"])
    STATE["najika"][stat] = min(100, STATE["najika"][stat] + 1)
    result = _care_response("train", energy=-15, fatigue=10, happiness=3)
    result["stat_boosted"] = stat
    result["new_value"] = STATE["najika"][stat]
    return result


@care_router.post("/heal")
async def heal_najika():
    """Heilen - HP (Hunger als HP-Proxy) steigt"""
    return _care_response("heal", hunger=30, energy=10, happiness=5)


@care_router.post("/praise")
async def praise_najika():
    """Loben - Happiness steigt, Discipline steigt"""
    return _care_response("praise", happiness=10, discipline=5)


@care_router.post("/scold")
async def scold_najika():
    """Tadeln - Discipline steigt, Happiness sinkt"""
    return _care_response("scold", discipline=10, happiness=-5)


@care_router.post("/touch")
async def touch_najika():
    """Beruehren/Streicheln - Happiness steigt, Bond steigt"""
    return _care_response("touch", happiness=8)


@care_router.post("/action")
async def care_action(action: CareAction):
    """Generische Care-Aktion"""
    handlers = {
        "feed": feed_najika,
        "drink": drink_najika,
        "sleep": sleep_najika,
        "wash": wash_najika,
        "play": play_najika,
        "train": train_najika,
        "heal": heal_najika,
        "praise": praise_najika,
        "scold": scold_najika,
        "touch": touch_najika,
    }
    handler = handlers.get(action.action)
    if not handler:
        return {"success": False, "error": f"Unbekannte Aktion: {action.action}"}
    return await handler()
