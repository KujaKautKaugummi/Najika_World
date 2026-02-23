"""
Najika Living System API
Handles Najika's basic living state (hunger, energy, mood)
Used by living_system_ui.js + index.html Care-Buttons
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
from backend.utils import handle_errors

router = APIRouter(prefix="/api/living", tags=["Living System"])

# Zweiter Router für /api/najika/* Care-Endpoints (index.html)
care_router = APIRouter(prefix="/api/najika", tags=["Najika Care"])

# SSE Router für /api/status/stream (private_mode.js)
status_router = APIRouter(prefix="/api/status", tags=["Status Stream"])

# In-Memory State (resets on server restart)
_state = {
    "hunger": 80,
    "energy": 70,
    "mood": "happy",
    "mood_value": 75,
    "happiness": 75,
    "anger": 0,
    "current_activity": None,
    "satiation": 80,
    "private_mode": False,
}


# ============================================================================
# /api/living/* - Living System UI Polling
# ============================================================================

@router.get("/state")
@handle_errors()
async def get_living_state():
    """Get Najika's current living state"""
    return _state


@router.get("/proactive")
@handle_errors()
async def get_proactive_message():
    """Check if Najika wants to say something proactively"""
    return {
        "should_send": False,
        "message": None
    }


@router.get("/activity/check")
@handle_errors()
async def check_activity():
    """Check current activity status"""
    return {
        "active": _state["current_activity"] is not None,
        "activity": _state["current_activity"],
        "started_at": None
    }


@router.post("/activity/start")
@handle_errors()
async def start_activity(activity: dict = {"name": "idle"}):
    """Start a new activity for Najika"""
    _state["current_activity"] = activity.get("name", "idle")
    return {"status": "ok", "activity": _state["current_activity"]}


# ============================================================================
# /api/najika/* - Care Buttons (Feed, Drink, Sleep, Wash)
# ============================================================================

def _care_response(action: str, hunger_delta=0, energy_delta=0):
    """Applies care action and returns updated state"""
    _state["hunger"] = min(100, max(0, _state["hunger"] + hunger_delta))
    _state["energy"] = min(100, max(0, _state["energy"] + energy_delta))
    return {
        "status": "ok",
        "action": action,
        "hunger": _state["hunger"],
        "energy": _state["energy"],
        "mood": _state["mood"]
    }


@care_router.post("/feed")
@handle_errors()
async def feed_najika():
    """Feed Najika - increases hunger/satiation"""
    return _care_response("feed", hunger_delta=15)


@care_router.post("/drink")
@handle_errors()
async def drink_najika():
    """Give Najika a drink"""
    return _care_response("drink", hunger_delta=5, energy_delta=5)


@care_router.post("/sleep")
@handle_errors()
async def sleep_najika():
    """Put Najika to sleep - restores energy"""
    return _care_response("sleep", energy_delta=30)


@care_router.post("/wash")
@handle_errors()
async def wash_najika():
    """Najika takes a shower/bath"""
    return _care_response("wash", energy_delta=5)


# ============================================================================
# /api/status/stream - SSE for private_mode.js
# ============================================================================

@status_router.get("/stream")
async def status_stream():
    """Server-Sent Events stream for status updates (private mode etc.)"""
    async def event_generator():
        while True:
            data = json.dumps({
                "private_mode": _state["private_mode"],
                "mood": _state["mood"],
                "energy": _state["energy"]
            })
            yield f"data: {data}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
