"""
Dice Monsters API - Najika World
=================================

REST API für Dungeon Dice Monsters System (FastAPI) (DATABASE)
Yu-Gi-Oh DDM Inspired Mechanics
Fantasy-Western Setting

Endpoints:
- GET /api/dice - Get all dice monsters (static pool)
- GET /api/dice/{dice_id} - Get specific dice monster
- POST /api/dice/add-to-collection - Add dice to player collection
- GET /api/dice/collection/{player_id} - Get player's dice collection

- POST /api/dice-duel/start - Start new dice duel
- POST /api/dice-duel/end - End duel and record results
- GET /api/dice-duel/history/{player_id} - Get duel history
- GET /api/dice-duel/{match_id} - Get specific duel

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database import get_db
from backend.models.dice_monsters import (
    DiceMonster, PlayerDiceCollection, DiceDuelMatch
)

# Create FastAPI Routers
router = APIRouter(prefix="/api/dice", tags=["dice_monsters"])
duel_router = APIRouter(prefix="/api/dice-duel", tags=["dice_duels"])


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class AddDiceToCollectionRequest(BaseModel):
    player_id: int
    dice_monster_id: int
    is_golden: bool = False


class StartDuelRequest(BaseModel):
    player1_id: int
    player2_id: Optional[int] = None
    is_ranked: bool = False
    is_vs_npc: bool = False
    npc_name: Optional[str] = None
    player1_dice_pool: List[int]  # List of 12 dice_monster IDs
    player2_dice_pool: Optional[List[int]] = None


class EndDuelRequest(BaseModel):
    match_id: int
    winner_id: Optional[int] = None
    player1_final_hp: int
    player2_final_hp: int
    turns_played: int
    duration_seconds: int
    final_board: Optional[Dict] = None
    total_dice_rolled: int = 0
    total_monsters_summoned: int = 0
    total_damage_dealt: int = 0
    gold_earned: int = 0
    xp_earned: int = 0
    dice_won: Optional[List[int]] = None


# ============================================================================
# DICE MONSTERS ENDPOINTS
# ============================================================================

@router.get("")
async def get_all_dice_monsters(
    element: Optional[str] = Query(None, description="Filter by element"),
    rarity: Optional[str] = Query(None, description="Filter by rarity"),
    monster_type: Optional[str] = Query(None, description="Filter by type"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get All Dice Monsters (DATABASE)

    Query Params:
        element: str (optional) - fire, water, earth, wind, light, dark
        rarity: str (optional) - common, uncommon, rare, epic, legendary
        monster_type: str (optional) - beast, dragon, warrior, mage, undead
        limit: int (default 100)

    Example: /api/dice?element=fire&rarity=legendary
    """
    try:
        query = db.query(DiceMonster)

        if element:
            query = query.filter(DiceMonster.element == element)
        if rarity:
            query = query.filter(DiceMonster.rarity == rarity)
        if monster_type:
            query = query.filter(DiceMonster.monster_type == monster_type)

        dice_monsters = query.limit(limit).all()

        return {
            "dice_monsters": [dice.to_dict() for dice in dice_monsters],
            "count": len(dice_monsters)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dice_id}")
async def get_dice_monster(dice_id: int, db: Session = Depends(get_db)):
    """
    Get Specific Dice Monster (DATABASE)

    Path: /api/dice/5
    """
    try:
        dice = db.query(DiceMonster).filter(DiceMonster.id == dice_id).first()

        if not dice:
            raise HTTPException(status_code=404, detail=f"Dice Monster {dice_id} not found")

        return dice.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-to-collection")
async def add_dice_to_collection(request: AddDiceToCollectionRequest, db: Session = Depends(get_db)):
    """
    Add Dice Monster to Player Collection (DATABASE)

    Body:
    {
        "player_id": 1,
        "dice_monster_id": 5,
        "is_golden": false
    }
    """
    try:
        # Check if dice monster exists
        dice = db.query(DiceMonster).filter(DiceMonster.id == request.dice_monster_id).first()
        if not dice:
            raise HTTPException(status_code=404, detail=f"Dice Monster {request.dice_monster_id} not found")

        # Check if player already owns this dice
        existing = db.query(PlayerDiceCollection).filter(
            PlayerDiceCollection.player_id == request.player_id,
            PlayerDiceCollection.dice_monster_id == request.dice_monster_id,
            PlayerDiceCollection.is_golden == request.is_golden
        ).first()

        if existing:
            # Increment copies
            existing.copies_owned += 1
            db.commit()
            db.refresh(existing)
            return {
                "success": True,
                "message": f"Added another copy of {dice.name}",
                "collection_entry": existing.to_dict()
            }
        else:
            # Create new entry
            collection_entry = PlayerDiceCollection(
                player_id=request.player_id,
                dice_monster_id=request.dice_monster_id,
                is_golden=request.is_golden,
                copies_owned=1
            )
            db.add(collection_entry)
            db.commit()
            db.refresh(collection_entry)

            return {
                "success": True,
                "message": f"Added {dice.name} to collection!",
                "collection_entry": collection_entry.to_dict()
            }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collection/{player_id}")
async def get_player_dice_collection(player_id: int, db: Session = Depends(get_db)):
    """
    Get Player's Dice Collection (DATABASE)

    Path: /api/dice/collection/1
    """
    try:
        collection = db.query(PlayerDiceCollection).filter(
            PlayerDiceCollection.player_id == player_id
        ).all()

        # Join with dice data
        collection_with_dice = []
        for entry in collection:
            dice = db.query(DiceMonster).filter(DiceMonster.id == entry.dice_monster_id).first()
            collection_with_dice.append({
                "collection": entry.to_dict(),
                "dice_monster": dice.to_dict() if dice else None
            })

        return {
            "player_id": player_id,
            "collection": collection_with_dice,
            "total_dice": len(collection_with_dice)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DICE DUEL ENDPOINTS
# ============================================================================

@duel_router.post("/start")
async def start_duel(request: StartDuelRequest, db: Session = Depends(get_db)):
    """
    Start New Dice Duel (DATABASE)

    Body:
    {
        "player1_id": 1,
        "player2_id": 2,
        "is_ranked": true,
        "is_vs_npc": false,
        "player1_dice_pool": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "player2_dice_pool": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    }
    """
    try:
        # Validate dice pool size (12 dice)
        if len(request.player1_dice_pool) != 12:
            raise HTTPException(
                status_code=400,
                detail=f"Player 1 dice pool must have exactly 12 dice (has {len(request.player1_dice_pool)})"
            )

        if not request.is_vs_npc and request.player2_dice_pool:
            if len(request.player2_dice_pool) != 12:
                raise HTTPException(
                    status_code=400,
                    detail=f"Player 2 dice pool must have exactly 12 dice (has {len(request.player2_dice_pool)})"
                )

        # Create duel
        duel = DiceDuelMatch(
            player1_id=request.player1_id,
            player2_id=request.player2_id,
            is_ranked=request.is_ranked,
            is_vs_npc=request.is_vs_npc,
            npc_name=request.npc_name,
            player1_dice_pool=request.player1_dice_pool,
            player2_dice_pool=request.player2_dice_pool or [],
            player1_starting_hp=3000,
            player2_starting_hp=3000,
            player1_final_hp=3000,
            player2_final_hp=3000,
            started_at=datetime.utcnow()
        )

        db.add(duel)
        db.commit()
        db.refresh(duel)

        return {
            "success": True,
            "match_id": duel.id,
            "message": "Dice Duel started!",
            "duel": duel.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@duel_router.post("/end")
async def end_duel(request: EndDuelRequest, db: Session = Depends(get_db)):
    """
    End Dice Duel and Record Results (DATABASE)

    Body:
    {
        "match_id": 5,
        "winner_id": 1,
        "player1_final_hp": 1200,
        "player2_final_hp": 0,
        "turns_played": 18,
        "duration_seconds": 600,
        "final_board": {...},
        "total_dice_rolled": 45,
        "total_monsters_summoned": 12,
        "total_damage_dealt": 4800,
        "gold_earned": 150,
        "xp_earned": 300,
        "dice_won": [25, 26]
    }
    """
    try:
        duel = db.query(DiceDuelMatch).filter(
            DiceDuelMatch.id == request.match_id
        ).first()

        if not duel:
            raise HTTPException(status_code=404, detail=f"Duel {request.match_id} not found")

        # Update duel results
        duel.winner_id = request.winner_id
        duel.player1_final_hp = request.player1_final_hp
        duel.player2_final_hp = request.player2_final_hp
        duel.turns_played = request.turns_played
        duel.duration_seconds = request.duration_seconds
        duel.final_board = request.final_board
        duel.total_dice_rolled = request.total_dice_rolled
        duel.total_monsters_summoned = request.total_monsters_summoned
        duel.total_damage_dealt = request.total_damage_dealt
        duel.gold_earned = request.gold_earned
        duel.xp_earned = request.xp_earned
        duel.dice_won = request.dice_won or []
        duel.ended_at = datetime.utcnow()

        # Update dice collection stats for summoned dice
        for dice_id in duel.player1_dice_pool:
            collection_entry = db.query(PlayerDiceCollection).filter(
                PlayerDiceCollection.player_id == duel.player1_id,
                PlayerDiceCollection.dice_monster_id == dice_id
            ).first()
            if collection_entry:
                collection_entry.times_summoned += 1
                if duel.winner_id == duel.player1_id:
                    collection_entry.times_won_with += 1

        if duel.player2_id and duel.player2_dice_pool:
            for dice_id in duel.player2_dice_pool:
                collection_entry = db.query(PlayerDiceCollection).filter(
                    PlayerDiceCollection.player_id == duel.player2_id,
                    PlayerDiceCollection.dice_monster_id == dice_id
                ).first()
                if collection_entry:
                    collection_entry.times_summoned += 1
                    if duel.winner_id == duel.player2_id:
                        collection_entry.times_won_with += 1

        db.commit()
        db.refresh(duel)

        return {
            "success": True,
            "message": "Duel ended and results recorded!",
            "duel": duel.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@duel_router.get("/history/{player_id}")
async def get_duel_history(
    player_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get Duel History (DATABASE)

    Path: /api/dice-duel/history/1?limit=20
    """
    try:
        duels = db.query(DiceDuelMatch).filter(
            (DiceDuelMatch.player1_id == player_id) | (DiceDuelMatch.player2_id == player_id)
        ).order_by(DiceDuelMatch.started_at.desc()).limit(limit).all()

        return {
            "player_id": player_id,
            "duels": [duel.to_dict() for duel in duels],
            "count": len(duels)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@duel_router.get("/{match_id}")
async def get_duel(match_id: int, db: Session = Depends(get_db)):
    """
    Get Specific Duel (DATABASE)

    Path: /api/dice-duel/5
    """
    try:
        duel = db.query(DiceDuelMatch).filter(DiceDuelMatch.id == match_id).first()

        if not duel:
            raise HTTPException(status_code=404, detail=f"Duel {match_id} not found")

        return duel.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
