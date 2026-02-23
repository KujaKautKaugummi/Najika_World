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

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from backend.database import get_db
from backend.models.pvp_battle import PvPBattle, PvPStats
from backend.utils import handle_errors

# Create FastAPI Router
router = APIRouter(prefix="/api/pvp", tags=["pvp"])


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
# HELPER FUNCTIONS
# ============================================================================

def get_or_create_pvp_stats(db: Session, player_id: int) -> PvPStats:
    """Get or create PvP stats for a player"""
    stats = db.query(PvPStats).filter(PvPStats.player_id == player_id).first()
    if not stats:
        stats = PvPStats(player_id=player_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/battle/start")
@handle_errors()
async def start_battle(request: StartBattleRequest, db: Session = Depends(get_db)):
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
        # Validate mode
        valid_modes = ["hardcore", "normal", "softy"]
        if request.mode not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Modus: {request.mode}",
                    "valid_modes": valid_modes
                }
            )

        # Check if same player
        if request.attacker_id == request.defender_id:
            raise HTTPException(
                status_code=400,
                detail={"success": False, "message": "Du kannst nicht gegen dich selbst kämpfen!"}
            )

        # Get or create stats for both players
        attacker_stats = get_or_create_pvp_stats(db, request.attacker_id)
        defender_stats = get_or_create_pvp_stats(db, request.defender_id)

        # Check cooldown (if defender has mercy cooldown active)
        if defender_stats.pvp_cooldown_until and defender_stats.pvp_cooldown_until > datetime.utcnow():
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": f"Defender hat PvP Cooldown bis {defender_stats.pvp_cooldown_until.isoformat()}"
                }
            )

        # Create battle
        max_id = db.query(PvPBattle).count()
        new_battle_id = max_id + 1

        battle = PvPBattle(
            battle_id=new_battle_id,
            attacker_id=request.attacker_id,
            defender_id=request.defender_id,
            mode=request.mode,
            status="active",
            started_at=datetime.utcnow()
        )

        db.add(battle)
        db.commit()
        db.refresh(battle)

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "message": f"PvP Battle gestartet! Modus: {request.mode}",
            "mode": request.mode
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/battle/end")
@handle_errors()
async def end_battle(request: EndBattleRequest, db: Session = Depends(get_db)):
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
        # Get battle
        battle = db.query(PvPBattle).filter(PvPBattle.battle_id == request.battle_id).first()

        if not battle:
            raise HTTPException(status_code=404, detail="Battle nicht gefunden")

        if battle.status != "active":
            raise HTTPException(status_code=400, detail=f"Battle ist bereits {battle.status}")

        # Validate winner
        if request.winner_id not in [battle.attacker_id, battle.defender_id]:
            raise HTTPException(status_code=400, detail="Winner muss Attacker oder Defender sein")

        loser_id = battle.defender_id if request.winner_id == battle.attacker_id else battle.attacker_id

        # Update battle
        battle.winner_id = request.winner_id
        battle.battle_duration = request.battle_duration
        battle.ended_at = datetime.utcnow()
        battle.status = "completed"

        # Update player stats
        winner_stats = get_or_create_pvp_stats(db, request.winner_id)
        loser_stats = get_or_create_pvp_stats(db, loser_id)

        winner_stats.total_battles += 1
        winner_stats.total_wins += 1
        winner_stats.last_battle = datetime.utcnow()
        winner_stats.kill_streak += 1
        winner_stats.best_kill_streak = max(winner_stats.best_kill_streak, winner_stats.kill_streak)

        loser_stats.total_battles += 1
        loser_stats.total_losses += 1
        loser_stats.last_battle = datetime.utcnow()
        loser_stats.kill_streak = 0

        # Mode-specific stats
        if battle.mode == "hardcore":
            winner_stats.hardcore_wins += 1
            loser_stats.hardcore_losses += 1
            battle.mercy_offered = True  # Hardcore always offers mercy
        elif battle.mode == "normal":
            winner_stats.normal_wins += 1
            loser_stats.normal_losses += 1
        elif battle.mode == "softy":
            winner_stats.softy_wins += 1
            loser_stats.softy_losses += 1
            # Rating changes (ELO-style)
            rating_change = 25
            winner_stats.rating += rating_change
            loser_stats.rating -= rating_change
            battle.rating_change_attacker = rating_change if request.winner_id == battle.attacker_id else -rating_change
            battle.rating_change_defender = rating_change if request.winner_id == battle.defender_id else -rating_change

        db.commit()
        db.refresh(battle)

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "winner_id": request.winner_id,
            "loser_id": loser_id,
            "mode": battle.mode,
            "duration": battle.battle_duration,
            "mercy_offered": battle.mercy_offered if battle.mode == "hardcore" else False,
            "message": f"Battle beendet! Winner: Player {request.winner_id}"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mercy/decide")
@handle_errors()
async def mercy_decision(request: MercyDecisionRequest, db: Session = Depends(get_db)):
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
        # Get battle
        battle = db.query(PvPBattle).filter(PvPBattle.battle_id == request.battle_id).first()

        if not battle:
            raise HTTPException(status_code=404, detail="Battle nicht gefunden")

        if battle.mode != "hardcore":
            raise HTTPException(status_code=400, detail="Mercy nur in Hardcore Modus!")

        if not battle.mercy_offered:
            raise HTTPException(status_code=400, detail="Keine Mercy angeboten!")

        # Get player stats
        player_stats = get_or_create_pvp_stats(db, request.player_id)

        if request.accept_mercy:
            # Accept mercy - select 3 items to give up
            inventory_dicts = [item.dict() for item in request.player_inventory]
            num_items_to_lose = min(3, len(inventory_dicts))
            items_lost = random.sample(inventory_dicts, num_items_to_lose) if inventory_dicts else []

            battle.mercy_accepted = True
            battle.items_lost = items_lost
            battle.status = "mercy"

            # Update mercy stats
            player_stats.mercy_count_7d += 1
            player_stats.mercy_total += 1
            player_stats.last_mercy = datetime.utcnow()

            # Check if mercy limit exceeded (3 in 7 days)
            if player_stats.mercy_count_7d >= 3:
                player_stats.pvp_cooldown_until = datetime.utcnow() + timedelta(days=7)
                message = f"Mercy akzeptiert! {num_items_to_lose} Items verloren. WARNUNG: 3 Mercies in 7 Tagen - 7 Tage PvP Cooldown!"
            else:
                message = f"Mercy akzeptiert! {num_items_to_lose} Items verloren. Mercy Count: {player_stats.mercy_count_7d}/3"

            db.commit()
            db.refresh(battle)

            return {
                "success": True,
                "battle_id": battle.battle_id,
                "mercy_accepted": True,
                "items_lost": items_lost,
                "mercy_count_7d": player_stats.mercy_count_7d,
                "pvp_cooldown_active": player_stats.pvp_cooldown_until is not None and player_stats.pvp_cooldown_until > datetime.utcnow(),
                "message": message
            }
        else:
            # Reject mercy - lose all items
            inventory_dicts = [item.dict() for item in request.player_inventory]
            battle.mercy_accepted = False
            battle.items_lost = inventory_dicts
            battle.status = "completed"

            db.commit()
            db.refresh(battle)

            return {
                "success": True,
                "battle_id": battle.battle_id,
                "mercy_accepted": False,
                "items_lost": inventory_dicts,
                "message": f"Mercy abgelehnt! ALLE Items verloren ({len(inventory_dicts)} Items)!"
            }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/normal/item-loss")
@handle_errors()
async def normal_item_loss(request: NormalItemLossRequest, db: Session = Depends(get_db)):
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
        # Get battle
        battle = db.query(PvPBattle).filter(PvPBattle.battle_id == request.battle_id).first()

        if not battle:
            raise HTTPException(status_code=404, detail="Battle nicht gefunden")

        if battle.mode != "normal":
            raise HTTPException(status_code=400, detail="Random Item Loss nur in Normal Modus!")

        # Select 1 random item
        inventory_dicts = [item.dict() for item in request.player_inventory]
        if not inventory_dicts:
            battle.item_lost_normal = None
            db.commit()
            return {
                "success": True,
                "battle_id": battle.battle_id,
                "item_lost": None,
                "message": "Kein Item verloren (leeres Inventar)"
            }

        lost_item = random.choice(inventory_dicts)
        battle.item_lost_normal = lost_item

        db.commit()
        db.refresh(battle)

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "item_lost": lost_item,
            "message": f"1 zufälliges Item verloren: {lost_item['name']} ({lost_item['rarity']})"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rankings/{mode}")
@handle_errors()
async def get_rankings(mode: str, db: Session = Depends(get_db)):
    """
    Get Rankings for PvP Mode

    Path: /api/pvp/rankings/hardcore
    Path: /api/pvp/rankings/normal
    Path: /api/pvp/rankings/softy
    """
    try:
        # Validate mode
        valid_modes = ["hardcore", "normal", "softy"]
        if mode not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Modus: {mode}",
                    "valid_modes": valid_modes
                }
            )

        # Get all player stats
        all_stats = db.query(PvPStats).all()

        # Build rankings based on mode
        rankings = []
        for stats in all_stats:
            if mode == "hardcore":
                wins = stats.hardcore_wins
                losses = stats.hardcore_losses
            elif mode == "normal":
                wins = stats.normal_wins
                losses = stats.normal_losses
            else:  # softy
                wins = stats.softy_wins
                losses = stats.softy_losses

            total_battles = wins + losses
            if total_battles > 0:
                rankings.append({
                    "player_id": stats.player_id,
                    "wins": wins,
                    "losses": losses,
                    "total_battles": total_battles,
                    "win_rate": round(wins / total_battles * 100, 2),
                    "rating": stats.rating if mode == "softy" else None,
                    "kill_streak": stats.kill_streak
                })

        # Sort by wins (or rating for softy)
        if mode == "softy":
            rankings.sort(key=lambda x: x["rating"], reverse=True)
        else:
            rankings.sort(key=lambda x: x["wins"], reverse=True)

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
@handle_errors()
async def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    """
    Get Player PvP Stats

    Path: /api/pvp/stats/1
    """
    try:
        stats = get_or_create_pvp_stats(db, player_id)
        return stats.to_dict()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/can-pvp")
@handle_errors()
async def check_can_pvp(
    attacker_id: int = Query(..., description="ID des Angreifers"),
    defender_id: int = Query(..., description="ID des Verteidigers"),
    mode: str = Query("normal", description="PvP Modus (hardcore/normal/softy)"),
    db: Session = Depends(get_db)
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
        # Validate mode
        valid_modes = ["hardcore", "normal", "softy"]
        if mode not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiger Modus: {mode}",
                    "valid_modes": valid_modes
                }
            )

        # Check same player
        if attacker_id == defender_id:
            return {
                "can_start": False,
                "reason": "Du kannst nicht gegen dich selbst kämpfen!",
                "attacker_id": attacker_id,
                "defender_id": defender_id,
                "mode": mode
            }

        # Check defender cooldown
        defender_stats = get_or_create_pvp_stats(db, defender_id)
        if defender_stats.pvp_cooldown_until and defender_stats.pvp_cooldown_until > datetime.utcnow():
            return {
                "can_start": False,
                "reason": f"Defender hat PvP Cooldown bis {defender_stats.pvp_cooldown_until.isoformat()}",
                "attacker_id": attacker_id,
                "defender_id": defender_id,
                "mode": mode
            }

        # Check for active battle
        active_battle = db.query(PvPBattle).filter(
            PvPBattle.status == "active",
            (
                (PvPBattle.attacker_id == attacker_id) |
                (PvPBattle.defender_id == attacker_id) |
                (PvPBattle.attacker_id == defender_id) |
                (PvPBattle.defender_id == defender_id)
            )
        ).first()

        if active_battle:
            return {
                "can_start": False,
                "reason": f"Einer der Spieler ist bereits in Battle #{active_battle.battle_id}",
                "attacker_id": attacker_id,
                "defender_id": defender_id,
                "mode": mode
            }

        return {
            "can_start": True,
            "reason": "PvP kann gestartet werden!",
            "attacker_id": attacker_id,
            "defender_id": defender_id,
            "mode": mode
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
@handle_errors()
async def export_state(db: Session = Depends(get_db)):
    """
    Export complete PvP state

    Returns:
        JSON with all battles, player stats, etc.
    """
    try:
        battles = db.query(PvPBattle).all()
        player_stats = db.query(PvPStats).all()

        battles_data = {}
        for battle in battles:
            battles_data[str(battle.battle_id)] = battle.to_dict()

        stats_data = {}
        for stats in player_stats:
            stats_data[str(stats.player_id)] = stats.to_dict()

        return {
            "battles": battles_data,
            "player_stats": stats_data,
            "total_battles": len(battles_data),
            "total_players": len(stats_data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/state/import")
@handle_errors()
async def import_state(state: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Import PvP state

    Body: Complete state object (from export)
    """
    try:
        if not state:
            raise HTTPException(status_code=400, detail="State-Daten erforderlich")

        imported_battles = 0
        imported_stats = 0

        # Import battles
        battles_data = state.get("battles", {})
        for battle_id, battle_dict in battles_data.items():
            existing = db.query(PvPBattle).filter(PvPBattle.battle_id == int(battle_id)).first()
            if existing:
                for key, value in battle_dict.items():
                    if hasattr(existing, key) and key != "id":
                        setattr(existing, key, value)
            else:
                new_battle = PvPBattle(**battle_dict)
                db.add(new_battle)
            imported_battles += 1

        # Import player stats
        stats_data = state.get("player_stats", {})
        for player_id, stats_dict in stats_data.items():
            existing = db.query(PvPStats).filter(PvPStats.player_id == int(player_id)).first()
            if existing:
                for key, value in stats_dict.items():
                    if hasattr(existing, key) and key != "id":
                        setattr(existing, key, value)
            else:
                new_stats = PvPStats(**stats_dict)
                db.add(new_stats)
            imported_stats += 1

        db.commit()

        return {
            "success": True,
            "message": "PvP State importiert",
            "battles": imported_battles,
            "players": imported_stats
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))