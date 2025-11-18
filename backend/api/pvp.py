"""
PvP API - Najika World
======================

REST API für PvP System (FastAPI)

Endpoints:
- POST /api/pvp/battle/start - Start PvP Battle
- POST /api/pvp/battle/end - End PvP Battle
- POST /api/pvp/mercy/decide - Mercy Decision
- POST /api/pvp/normal/item-loss - Select random item loss (Normal PvP)
- GET /api/pvp/rankings/<mode> - Get rankings
- GET /api/pvp/stats/<player_id> - Get player stats
- GET /api/pvp/can-pvp - Check if can start PvP
- GET /api/pvp/state/export - Export state
- POST /api/pvp/state/import - Import state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from backend.services.pvp_system import PvPSystem, PvPMode

# Create FastAPI Router
router = APIRouter(prefix="/api/pvp", tags=["pvp"])

# Global PvP System Instance
pvp_system = PvPSystem()


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class StartBattleRequest(BaseModel):
    attacker_id: int
    defender_id: int
    mode: str = "normal"


class EndBattleRequest(BaseModel):
    battle_id: int
    winner_id: int
    battle_duration: float = 0.0


class ItemData(BaseModel):
    name: str
    rarity: str


class MercyDecisionRequest(BaseModel):
    battle_id: int
    player_id: int
    accept_mercy: bool
    player_inventory: List[ItemData] = []


class NormalItemLossRequest(BaseModel):
    battle_id: int
    player_inventory: List[ItemData] = []


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/battle/start")
async def start_battle(request: StartBattleRequest):
    """
    Start PvP Battle

    Body:
    {
        "attacker_id": 1,
        "defender_id": 2,
        "mode": "hardcore"  // "hardcore", "normal", "softy"
    }
    """
    try:
        # Parse mode
        try:
            mode = PvPMode(request.mode)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Modus: {request.mode}",
                    "valid_modes": ["hardcore", "normal", "softy"]
                }
            )

        # Start battle
        success, battle_id, message = pvp_system.start_pvp_battle(
            request.attacker_id, request.defender_id, mode
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
            "battle_id": battle_id,
            "message": message,
            "mode": mode.value
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/battle/end")
async def end_battle(request: EndBattleRequest):
    """
    End PvP Battle

    Body:
    {
        "battle_id": 1,
        "winner_id": 1,
        "battle_duration": 120.5
    }
    """
    try:
        result = pvp_system.end_pvp_battle(
            request.battle_id,
            request.winner_id,
            request.battle_duration
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mercy/decide")
async def mercy_decision(request: MercyDecisionRequest):
    """
    Process Mercy Decision (Hardcore PvP only)

    Body:
    {
        "battle_id": 1,
        "player_id": 2,
        "accept_mercy": true,
        "player_inventory": [
            {"name": "Schwert", "rarity": "epic"},
            {"name": "Trank", "rarity": "common"}
        ]
    }
    """
    try:
        # Convert Pydantic models to dicts for service layer
        inventory_dicts = [item.dict() for item in request.player_inventory]

        result = pvp_system.process_mercy_decision(
            request.battle_id,
            request.player_id,
            request.accept_mercy,
            inventory_dicts
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/normal/item-loss")
async def normal_item_loss(request: NormalItemLossRequest):
    """
    Select Random Item Loss (Normal PvP only)

    Body:
    {
        "battle_id": 1,
        "player_inventory": [
            {"name": "Schwert", "rarity": "common"}
        ]
    }
    """
    try:
        # Convert Pydantic models to dicts for service layer
        inventory_dicts = [item.dict() for item in request.player_inventory]

        result = pvp_system.select_random_item_loss(
            request.battle_id,
            inventory_dicts
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rankings/{mode}")
async def get_rankings(mode: str):
    """
    Get Rankings for PvP Mode

    Path: /api/pvp/rankings/hardcore
    Path: /api/pvp/rankings/normal
    Path: /api/pvp/rankings/softy
    """
    try:
        # Parse mode
        try:
            pvp_mode = PvPMode(mode)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Modus: {mode}",
                    "valid_modes": ["hardcore", "normal", "softy"]
                }
            )

        rankings = pvp_system.get_pvp_rankings(pvp_mode)

        return {
            "mode": mode,
            "rankings": rankings,
            "total_players": len(rankings)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/{player_id}")
async def get_player_stats(player_id: int):
    """
    Get Player PvP Stats

    Path: /api/pvp/stats/1
    """
    try:
        stats = pvp_system.get_player_pvp_stats(player_id)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/can-pvp")
async def check_can_pvp(
    attacker_id: int = Query(..., description="ID des Angreifers"),
    defender_id: int = Query(..., description="ID des Verteidigers"),
    mode: str = Query("normal", description="PvP Modus (hardcore/normal/softy)")
):
    """
    Check if PvP can be initiated

    Query Params:
        attacker_id: int
        defender_id: int
        mode: str (hardcore/normal/softy)

    Example: /api/pvp/can-pvp?attacker_id=1&defender_id=2&mode=hardcore
    """
    try:
        # Parse mode
        try:
            pvp_mode = PvPMode(mode)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Modus: {mode}",
                    "valid_modes": ["hardcore", "normal", "softy"]
                }
            )

        can_start, reason = pvp_system.can_initiate_pvp(attacker_id, defender_id, pvp_mode)

        return {
            "can_start": can_start,
            "reason": reason,
            "attacker_id": attacker_id,
            "defender_id": defender_id,
            "mode": pvp_mode.value
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
async def export_state():
    """
    Export complete PvP state

    Returns:
        JSON with all battles, player stats, etc.
    """
    try:
        state = pvp_system.export_state()
        return state

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/state/import")
async def import_state(state: Dict[str, Any]):
    """
    Import PvP state

    Body: Complete state object (from export)
    """
    try:
        if not state:
            raise HTTPException(status_code=400, detail="State-Daten erforderlich")

        pvp_system.import_state(state)

        return {
            "success": True,
            "message": "PvP State importiert",
            "battles": len(pvp_system.battles),
            "players": len(pvp_system.player_stats)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
