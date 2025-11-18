"""
Oregon Trail Events API - Najika World
=======================================

REST API für Oregon Trail Events System (FastAPI)

Endpoints:
- GET /api/oregon/trigger - Trigger random event
- POST /api/oregon/choice - Execute player choice
- GET /api/oregon/chaos - Get chaos status
- POST /api/oregon/chaos/reduce - Reduce chaos
- GET /api/oregon/current - Get current active event

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional

from backend.services.oregon_trail_events import OregonTrailEventsSystem

# Create FastAPI Router
router = APIRouter(prefix="/api/oregon", tags=["oregon"])

# Global System Instance
oregon_system = OregonTrailEventsSystem()


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class ExecuteChoiceRequest(BaseModel):
    choice_index: int
    player_state: Dict[str, Any] = {}


class ReduceChaosRequest(BaseModel):
    method: str
    amount: Optional[int] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/trigger")
async def trigger_event(
    location: str = Query("any", description="Event location"),
    player_class: Optional[str] = Query(None, description="Player class")
):
    """
    Trigger Random Event

    Query Params:
        location: str (optional, default "any")
        player_class: str (optional)

    Example: /api/oregon/trigger?location=wilderness&player_class=mage
    """
    try:
        event_data = oregon_system.trigger_random_event(location, player_class)

        if not event_data:
            return {
                "triggered": False,
                "message": "Kein Event getriggert"
            }

        return {
            "triggered": True,
            "event": event_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/choice")
async def execute_choice(request: ExecuteChoiceRequest):
    """
    Execute Player Choice

    Body:
    {
        "choice_index": 0,
        "player_state": {
            "gold": 100,
            "health": 80,
            ...
        }
    }
    """
    try:
        result = oregon_system.execute_choice(
            request.choice_index,
            request.player_state
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chaos")
async def get_chaos_status():
    """
    Get Chaos Status

    Returns current chaos level, points, Najika state
    """
    try:
        status = oregon_system.get_chaos_status()
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chaos/reduce")
async def reduce_chaos(request: ReduceChaosRequest):
    """
    Reduce Chaos

    Body:
    {
        "method": "meditation",  // meditation, temple_visit, lawful_quest, etc.
        "amount": 10  // optional, overrides default
    }
    """
    try:
        result = oregon_system.chaos_calc.reduce_chaos(
            request.method,
            request.amount
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current")
async def get_current_event():
    """
    Get Current Active Event

    Returns current event or None
    """
    try:
        if not oregon_system.event_active or not oregon_system.current_event:
            return {
                "active": False,
                "message": "Kein aktives Event"
            }

        event = oregon_system._format_event_for_client(oregon_system.current_event)

        return {
            "active": True,
            "event": event
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
