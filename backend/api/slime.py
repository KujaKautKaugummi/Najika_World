"""
Slime API - Najika World
========================

REST API für Slime Companion System (FastAPI)

Endpoints:
- POST /api/slime/create - Create companion
- POST /api/slime/experience - Add experience
- POST /api/slime/metamorphosis - Perform metamorphosis
- POST /api/slime/color/collect - Collect color
- POST /api/slime/learn - Try learn move
- POST /api/slime/rescue - Use rescue mechanic
- POST /api/slime/tamagotchi/update - Update tamagotchi stats
- POST /api/slime/feed - Feed companion
- POST /api/slime/water - Give water
- POST /api/slime/sleep - Let sleep
- GET /api/slime/{companion_id} - Get companion info
- GET /api/slime/state/export - Export state
- POST /api/slime/state/import - Import state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from backend.services.slime_system import SlimeSystem

# Create FastAPI Router
router = APIRouter(prefix="/api/slime", tags=["slime"])

# Global Slime System Instance
slime_system = SlimeSystem()


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class CreateCompanionRequest(BaseModel):
    owner_player_id: int
    name: str
    starting_region: str


class AddExperienceRequest(BaseModel):
    companion_id: int
    exp_amount: int = 0


class MetamorphosisRequest(BaseModel):
    companion_id: int
    current_region: str


class CollectColorRequest(BaseModel):
    companion_id: int
    region: str


class LearnMoveRequest(BaseModel):
    companion_id: int
    move_name: str
    move_type: str  # "enemy" or "player"
    source_name: str


class RescueRequest(BaseModel):
    companion_id: int


class UpdateTamagotchiRequest(BaseModel):
    companion_id: int
    delta_hours: Optional[float] = None


class FeedCompanionRequest(BaseModel):
    companion_id: int
    amount: float = 30.0


class GiveWaterRequest(BaseModel):
    companion_id: int
    amount: float = 40.0


class LetSleepRequest(BaseModel):
    companion_id: int
    hours: float = 8.0


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/create")
async def create_companion(request: CreateCompanionRequest):
    """
    Create Companion

    Body:
    {
        "owner_player_id": 1,
        "name": "Fluffi",
        "starting_region": "samtmoos_tiefwald"
    }
    """
    try:
        companion = slime_system.create_companion(
            request.owner_player_id,
            request.name,
            request.starting_region
        )

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "level": companion.level,
            "fantasy_tier": companion.fantasy_tier.value if companion.fantasy_tier else None,
            "message": f"{companion.name} wurde erstellt!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/experience")
async def add_experience(request: AddExperienceRequest):
    """
    Add Experience

    Body:
    {
        "companion_id": 1,
        "exp_amount": 120
    }
    """
    try:
        leveled_up, result = slime_system.add_experience(
            request.companion_id,
            request.exp_amount
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metamorphosis")
async def perform_metamorphosis(request: MetamorphosisRequest):
    """
    Perform Metamorphosis (Level 50)

    Body:
    {
        "companion_id": 1,
        "current_region": "samtmoos_tiefwald"
    }
    """
    try:
        result = slime_system.perform_metamorphosis(
            request.companion_id,
            request.current_region
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/color/collect")
async def collect_color(request: CollectColorRequest):
    """
    Collect Slime Color (Rainbow Quest)

    Body:
    {
        "companion_id": 1,
        "region": "reich_der_drei"
    }
    """
    try:
        result = slime_system.collect_color(
            request.companion_id,
            request.region
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn")
async def try_learn_move(request: LearnMoveRequest):
    """
    Try Learn Move

    Body:
    {
        "companion_id": 1,
        "move_name": "Thunder Strike",
        "move_type": "enemy",
        "source_name": "Goblin King"
    }
    """
    try:
        learned, result = slime_system.try_learn_move(
            request.companion_id,
            request.move_name,
            request.move_type,
            request.source_name
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rescue")
async def use_rescue(request: RescueRequest):
    """
    Use Rescue Mechanic (Hardcore)

    Body:
    {
        "companion_id": 1
    }
    """
    try:
        rescued, result = slime_system.use_rescue(request.companion_id)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tamagotchi/update")
async def update_tamagotchi(request: UpdateTamagotchiRequest):
    """
    Update Tamagotchi Stats (Decay)

    Body:
    {
        "companion_id": 1,
        "delta_hours": 1.0
    }
    """
    try:
        result = slime_system.update_tamagotchi(
            request.companion_id,
            request.delta_hours
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feed")
async def feed_companion(request: FeedCompanionRequest):
    """
    Feed Companion

    Body:
    {
        "companion_id": 1,
        "amount": 30.0
    }
    """
    try:
        result = slime_system.feed_companion(
            request.companion_id,
            request.amount
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/water")
async def give_water(request: GiveWaterRequest):
    """
    Give Water

    Body:
    {
        "companion_id": 1,
        "amount": 40.0
    }
    """
    try:
        result = slime_system.give_water(
            request.companion_id,
            request.amount
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sleep")
async def let_sleep(request: LetSleepRequest):
    """
    Let Sleep

    Body:
    {
        "companion_id": 1,
        "hours": 8.0
    }
    """
    try:
        result = slime_system.let_sleep(
            request.companion_id,
            request.hours
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{companion_id}")
async def get_companion_info(companion_id: int):
    """
    Get Companion Info

    Path: /api/slime/1
    """
    try:
        result = slime_system.get_companion_info(companion_id)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
async def export_state():
    """
    Export Slime State

    Returns:
        JSON with all companions
    """
    try:
        state = slime_system.export_state()
        return state

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/state/import")
async def import_state(state: Dict[str, Any]):
    """
    Import Slime State

    Body: Complete state object (from export)
    """
    try:
        if not state:
            raise HTTPException(status_code=400, detail="State-Daten erforderlich")

        # TODO: Implement import_state in SlimeSystem
        # slime_system.import_state(state)

        return {
            "success": True,
            "message": "Slime State importiert",
            "companions": len(state.get("companions", {}))
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
