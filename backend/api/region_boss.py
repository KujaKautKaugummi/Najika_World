"""
Region Boss API - Najika World
===============================

REST API für Gebietsherrscher System (FastAPI)

Endpoints:
- POST /api/region-boss/challenge/create - Create challenge
- POST /api/region-boss/challenge/accept - Accept challenge
- POST /api/region-boss/challenge/complete - Complete challenge
- POST /api/region-boss/conquest/progress - Add conquest progress
- POST /api/region-boss/tax/set - Set tax rate
- POST /api/region-boss/broadcast - Broadcast message
- GET /api/region-boss/region/<region> - Get region info
- GET /api/region-boss/ultimate - Get ultimate ruler info
- GET /api/region-boss/can-challenge - Check if can challenge
- GET /api/region-boss/state/export - Export state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional

from backend.services.region_boss_system import (
    RegionBossSystem, Region, ConquestPath
)

# Create FastAPI Router
router = APIRouter(prefix="/api/region-boss", tags=["region_boss"])

# Global System Instance
boss_system = RegionBossSystem()


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class CreateChallengeRequest(BaseModel):
    challenger_id: int
    region: str
    challenge_type: str = "krieg"
    stakes: Optional[Dict[str, Any]] = None
    conditions: Optional[Dict[str, Any]] = None


class AcceptChallengeRequest(BaseModel):
    challenge_id: int
    boss_player_id: int


class CompleteChallengeRequest(BaseModel):
    challenge_id: int
    winner_id: int


class AddConquestProgressRequest(BaseModel):
    player_id: int
    region: str
    path: str
    progress: float = 0.0


class SetTaxRateRequest(BaseModel):
    boss_player_id: int
    region: str
    tax_rate: float


class BroadcastMessageRequest(BaseModel):
    boss_player_id: int
    region: str
    message: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/challenge/create")
async def create_challenge(request: CreateChallengeRequest):
    """
    Create Challenge

    Body:
    {
        "challenger_id": 1,
        "region": "samtmoos_tiefwald",
        "challenge_type": "krieg",  // krieg, handel, diplomatie, quest_line
        "stakes": {},
        "conditions": {}
    }
    """
    try:
        # Parse region
        try:
            region = Region(request.region)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültige Region: {request.region}",
                    "valid_regions": [r.value for r in Region]
                }
            )

        # Parse challenge type
        try:
            challenge_type = ConquestPath(request.challenge_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Challenge-Typ: {request.challenge_type}",
                    "valid_types": [c.value for c in ConquestPath]
                }
            )

        success, challenge_id, message = boss_system.create_challenge(
            request.challenger_id,
            region,
            challenge_type,
            stakes=request.stakes,
            conditions=request.conditions
        )

        if not success:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": message
                }
            )

        return {
            "success": True,
            "challenge_id": challenge_id,
            "message": message,
            "region": region.value,
            "type": challenge_type.value
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/challenge/accept")
async def accept_challenge(request: AcceptChallengeRequest):
    """
    Accept Challenge

    Body:
    {
        "challenge_id": 1,
        "boss_player_id": 2
    }
    """
    try:
        success, message = boss_system.accept_challenge(
            request.challenge_id,
            request.boss_player_id
        )

        if not success:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": message
                }
            )

        return {
            "success": True,
            "message": message,
            "challenge_id": request.challenge_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/challenge/complete")
async def complete_challenge(request: CompleteChallengeRequest):
    """
    Complete Challenge

    Body:
    {
        "challenge_id": 1,
        "winner_id": 2
    }
    """
    try:
        result = boss_system.complete_challenge(
            request.challenge_id,
            request.winner_id
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conquest/progress")
async def add_conquest_progress(request: AddConquestProgressRequest):
    """
    Add Conquest Progress (Handel/Diplomatie/Quest)

    Body:
    {
        "player_id": 1,
        "region": "samtmoos_tiefwald",
        "path": "handel",
        "progress": 25.0
    }
    """
    try:
        # Parse region
        try:
            region = Region(request.region)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültige Region: {request.region}",
                    "valid_regions": [r.value for r in Region]
                }
            )

        # Parse path
        try:
            path = ConquestPath(request.path)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Pfad: {request.path}",
                    "valid_paths": [c.value for c in ConquestPath]
                }
            )

        result = boss_system.add_conquest_progress(
            request.player_id,
            region,
            path,
            request.progress
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tax/set")
async def set_tax_rate(request: SetTaxRateRequest):
    """
    Set Tax Rate (Boss only, 5-10%)

    Body:
    {
        "boss_player_id": 1,
        "region": "samtmoos_tiefwald",
        "tax_rate": 7.5
    }
    """
    try:
        # Parse region
        try:
            region = Region(request.region)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={"error": f"Ungültige Region: {request.region}"}
            )

        success, message = boss_system.set_tax_rate(
            request.boss_player_id,
            region,
            request.tax_rate
        )

        if not success:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": message
                }
            )

        return {
            "success": True,
            "message": message,
            "region": region.value,
            "tax_rate": request.tax_rate
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/broadcast")
async def broadcast_message(request: BroadcastMessageRequest):
    """
    Broadcast Message (Boss only)

    Body:
    {
        "boss_player_id": 1,
        "region": "samtmoos_tiefwald",
        "message": "Willkommen!"
    }
    """
    try:
        # Parse region
        try:
            region = Region(request.region)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={"error": f"Ungültige Region: {request.region}"}
            )

        success, broadcast = boss_system.broadcast_message(
            request.boss_player_id,
            region,
            request.message
        )

        if not success:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": broadcast
                }
            )

        return {
            "success": True,
            "broadcast": broadcast,
            "region": region.value
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/region/{region}")
async def get_region_info(region: str):
    """
    Get Region Info

    Path: /api/region-boss/region/samtmoos_tiefwald
    """
    try:
        # Parse region
        try:
            region_enum = Region(region)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültige Region: {region}",
                    "valid_regions": [r.value for r in Region]
                }
            )

        info = boss_system.get_region_info(region_enum)

        return info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ultimate")
async def get_ultimate_ruler():
    """
    Get Ultimate Ruler Info

    Path: /api/region-boss/ultimate
    """
    try:
        info = boss_system.get_ultimate_ruler_info()
        return info

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/can-challenge")
async def check_can_challenge(
    challenger_id: int = Query(..., description="Challenger player ID"),
    region: str = Query(..., description="Region to challenge")
):
    """
    Check if can challenge

    Query Params:
        challenger_id: int
        region: str

    Example: /api/region-boss/can-challenge?challenger_id=1&region=samtmoos_tiefwald
    """
    try:
        # Parse region
        try:
            region_enum = Region(region)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={"error": f"Ungültige Region: {region}"}
            )

        can_challenge, reason = boss_system.can_challenge_boss(challenger_id, region_enum)

        return {
            "can_challenge": can_challenge,
            "reason": reason,
            "challenger_id": challenger_id,
            "region": region_enum.value
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
async def export_state():
    """
    Export State

    Returns:
        JSON with all region bosses, ultimate ruler
    """
    try:
        state = boss_system.export_state()
        return state

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
