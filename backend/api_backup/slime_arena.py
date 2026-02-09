"""
Slime Arena API - Najika World
===============================

REST API für Slime Arena Combat System (FastAPI)
Location: Handelsfeste (Heiße Dünen) - "Zur Schlammigen Münze"

Features:
- 3 Game Modes: 1v1 Normal, 1v1 mit Finisher, Tournament
- 3 Combat Modes: Auto, Manual, Cheer
- Fame/Reputation System
- Tournament Bracket System

Endpoints:
- POST /api/slime-arena/start-duel - Start new duel
- POST /api/slime-arena/action - Execute combat action
- POST /api/slime-arena/end-duel - End duel and record results
- POST /api/slime-arena/finisher - Execute finisher move
- GET /api/slime-arena/leaderboard - Get fame leaderboard
- GET /api/slime-arena/fame/{player_id} - Get player fame stats
- POST /api/slime-arena/tournament/register - Register for tournament
- GET /api/slime-arena/tournament/{tournament_id} - Get tournament info
- GET /api/slime-arena/tournament/active - Get active/upcoming tournaments
- POST /api/slime-arena/tournament/advance - Advance tournament round

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2026-01-20
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

from backend.database import get_db
from backend.models.slime_arena import SlimeDuel, SlimeTournament, SlimeFame

# Create FastAPI Routers
router = APIRouter(prefix="/api/slime-arena", tags=["slime_arena"])


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class StartDuelRequest(BaseModel):
    player_id: str
    player_slime_name: str
    player_slime_type: str
    opponent_type: str = "npc"  # 'npc' or 'player'
    opponent_id: Optional[str] = None
    opponent_slime_name: Optional[str] = None
    opponent_slime_type: Optional[str] = None
    game_mode: str = "normal"  # 'normal', 'finisher', 'tournament'
    combat_mode: str = "manual"  # 'auto', 'manual', 'cheer'
    tournament_id: Optional[int] = None
    tournament_round: Optional[int] = None


class CombatActionRequest(BaseModel):
    duel_id: int
    action_type: str  # 'attack', 'defend', 'special', 'cheer'
    action_data: Optional[Dict] = None  # Additional action data


class EndDuelRequest(BaseModel):
    duel_id: int
    winner: str  # 'player' or 'opponent'
    player_hp_end: int
    opponent_hp_end: int
    rounds_total: int
    action_log: Optional[List[Dict]] = None
    finisher_used: Optional[str] = None
    finisher_success: bool = False


class FinisherRequest(BaseModel):
    duel_id: int
    finisher_name: str
    target: str = "opponent"


class TournamentRegisterRequest(BaseModel):
    player_id: str
    player_slime_name: str
    player_slime_type: str
    tournament_id: int


class TournamentAdvanceRequest(BaseModel):
    tournament_id: int
    duel_results: List[Dict]  # Results from completed round


# ============================================================================
# COMBAT LOGIC HELPERS
# ============================================================================

def calculate_damage(attacker_type: str, defender_type: str, base_damage: int = 20) -> int:
    """Calculate damage based on slime types"""
    # Type advantages (rock-paper-scissors style)
    advantages = {
        "bubble": ["molten", "fire"],
        "molten": ["crystal", "ice"],
        "crystal": ["shadow", "dark"],
        "shadow": ["bubble", "water"],
        "toxic": ["crystal", "molten"],
        "electric": ["bubble", "water"],
        "ice": ["shadow", "toxic"],
        "fire": ["toxic", "ice"]
    }

    damage = base_damage
    if defender_type in advantages.get(attacker_type, []):
        damage = int(damage * 1.5)  # 50% bonus
    elif attacker_type in advantages.get(defender_type, []):
        damage = int(damage * 0.75)  # 25% penalty

    # Add some randomness
    variance = random.randint(-3, 3)
    return max(1, damage + variance)


def calculate_rewards(game_mode: str, won: bool, rounds: int, finisher_success: bool = False) -> Dict:
    """Calculate gold, XP, and fame rewards"""
    rewards = {"gold": 0, "xp": 0, "fame": 0}

    if not won:
        # Consolation prize
        rewards["gold"] = 50
        rewards["xp"] = 10
        return rewards

    # Base rewards by mode
    if game_mode == "normal":
        rewards["gold"] = random.randint(100, 500)
        rewards["xp"] = random.randint(50, 150)
        rewards["fame"] = 5
    elif game_mode == "finisher":
        rewards["gold"] = random.randint(200, 1000)
        rewards["xp"] = random.randint(100, 300)
        rewards["fame"] = 10
        if finisher_success:
            rewards["fame"] += 5
    elif game_mode == "tournament":
        rewards["gold"] = random.randint(300, 1500)
        rewards["xp"] = random.randint(150, 400)
        rewards["fame"] = 20

    # Bonus for quick victories
    if rounds < 5:
        rewards["gold"] = int(rewards["gold"] * 1.2)
        rewards["fame"] += 2

    return rewards


def generate_npc_opponent() -> Dict:
    """Generate a random NPC opponent"""
    npc_names = [
        "Schleimiger Pete", "Blubber-Bruno", "Kristall-Käthe", "Schatten-Sam",
        "Giftige Greta", "Elektro-Emil", "Eis-Ilse", "Feuer-Franz",
        "Molten Mike", "Bubble Betty", "Dark Dirk", "Aqua Anna"
    ]

    slime_types = ["bubble", "molten", "crystal", "shadow", "toxic", "electric", "ice", "fire"]

    return {
        "name": random.choice(npc_names),
        "slime_type": random.choice(slime_types)
    }


# ============================================================================
# DUEL ENDPOINTS
# ============================================================================

@router.post("/start-duel")
async def start_duel(request: StartDuelRequest, db: Session = Depends(get_db)):
    """Start a new slime duel"""

    # Generate NPC opponent if needed
    if request.opponent_type == "npc" and not request.opponent_slime_name:
        npc = generate_npc_opponent()
        request.opponent_slime_name = npc["name"]
        request.opponent_slime_type = npc["slime_type"]

    # Create duel record
    duel = SlimeDuel(
        player_id=request.player_id,
        player_slime_name=request.player_slime_name,
        player_slime_type=request.player_slime_type,
        opponent_type=request.opponent_type,
        opponent_id=request.opponent_id,
        opponent_slime_name=request.opponent_slime_name,
        opponent_slime_type=request.opponent_slime_type,
        game_mode=request.game_mode,
        combat_mode=request.combat_mode,
        player_hp_start=100,
        opponent_hp_start=100,
        tournament_id=request.tournament_id,
        tournament_round=request.tournament_round,
        action_log=[]
    )

    db.add(duel)
    db.commit()
    db.refresh(duel)

    return {
        "success": True,
        "duel_id": duel.id,
        "duel": duel.to_dict(),
        "message": f"Duell gegen {request.opponent_slime_name} gestartet!"
    }


@router.post("/action")
async def execute_action(request: CombatActionRequest, db: Session = Depends(get_db)):
    """Execute a combat action during a duel"""

    duel = db.query(SlimeDuel).filter(SlimeDuel.id == request.duel_id).first()
    if not duel:
        raise HTTPException(status_code=404, detail="Duell nicht gefunden")

    # Calculate action results
    action_result = {
        "round": duel.rounds_total + 1,
        "action_type": request.action_type,
        "timestamp": datetime.utcnow().isoformat()
    }

    if request.action_type == "attack":
        damage = calculate_damage(
            duel.player_slime_type,
            duel.opponent_slime_type
        )
        action_result["damage"] = damage
        action_result["target"] = "opponent"
        # Note: Actual HP updates happen in end-duel

    elif request.action_type == "defend":
        action_result["defense_bonus"] = 10
        action_result["message"] = "Verteidigung erhöht!"

    elif request.action_type == "special":
        special_damage = calculate_damage(
            duel.player_slime_type,
            duel.opponent_slime_type,
            base_damage=30
        )
        action_result["damage"] = special_damage
        action_result["special_type"] = request.action_data.get("special_type", "default")
        action_result["target"] = "opponent"

    elif request.action_type == "cheer":
        buff_type = request.action_data.get("buff_type", "damage")
        buff_value = 15
        action_result["buff"] = {"type": buff_type, "value": buff_value}
        action_result["message"] = f"+{buff_value}% {buff_type.upper()}!"

    # Append to action log
    if not duel.action_log:
        duel.action_log = []
    duel.action_log.append(action_result)
    duel.rounds_total += 1

    db.commit()
    db.refresh(duel)

    return {
        "success": True,
        "action_result": action_result,
        "round": duel.rounds_total
    }


@router.post("/end-duel")
async def end_duel(request: EndDuelRequest, db: Session = Depends(get_db)):
    """End a duel and record results"""

    duel = db.query(SlimeDuel).filter(SlimeDuel.id == request.duel_id).first()
    if not duel:
        raise HTTPException(status_code=404, detail="Duell nicht gefunden")

    # Update duel results
    duel.winner = request.winner
    duel.player_hp_end = request.player_hp_end
    duel.opponent_hp_end = request.opponent_hp_end
    duel.rounds_total = request.rounds_total
    duel.finisher_used = request.finisher_used
    duel.finisher_success = request.finisher_success
    duel.finished_at = datetime.utcnow()

    if request.action_log:
        duel.action_log = request.action_log

    # Calculate rewards
    won = (request.winner == "player")
    rewards = calculate_rewards(
        duel.game_mode,
        won,
        request.rounds_total,
        request.finisher_success
    )

    duel.gold_earned = rewards["gold"]
    duel.xp_earned = rewards["xp"]
    duel.fame_earned = rewards["fame"]

    db.commit()

    # Update player fame
    fame = db.query(SlimeFame).filter(SlimeFame.player_id == duel.player_id).first()
    if not fame:
        fame = SlimeFame(player_id=duel.player_id)
        db.add(fame)

    fame.update_stats(
        duel_won=won,
        fame_earned=rewards["fame"],
        finisher_used=request.finisher_used is not None,
        finisher_success=request.finisher_success
    )

    fame.total_gold_earned += rewards["gold"]
    fame.total_xp_earned += rewards["xp"]

    db.commit()
    db.refresh(duel)
    db.refresh(fame)

    return {
        "success": True,
        "duel": duel.to_dict(),
        "rewards": rewards,
        "fame": fame.to_dict(),
        "message": "Duell beendet!" if won else "Verloren, aber kämpfe weiter!"
    }


@router.post("/finisher")
async def execute_finisher(request: FinisherRequest, db: Session = Depends(get_db)):
    """Execute a finisher move (only when opponent HP = 0)"""

    duel = db.query(SlimeDuel).filter(SlimeDuel.id == request.duel_id).first()
    if not duel:
        raise HTTPException(status_code=404, detail="Duell nicht gefunden")

    # Finisher mini-game logic (simplified for now)
    success_chance = 0.7  # 70% base success rate

    # Player skill factor (based on fame)
    fame = db.query(SlimeFame).filter(SlimeFame.player_id == duel.player_id).first()
    if fame:
        skill_bonus = min(0.2, fame.finisher_success_rate / 500)  # Up to +20%
        success_chance += skill_bonus

    success = random.random() < success_chance

    # Record finisher attempt
    finisher_result = {
        "finisher_name": request.finisher_name,
        "success": success,
        "bonus_fame": 5 if success else 0,
        "timestamp": datetime.utcnow().isoformat()
    }

    if not duel.action_log:
        duel.action_log = []
    duel.action_log.append({"type": "finisher", **finisher_result})

    duel.finisher_used = request.finisher_name
    duel.finisher_success = success

    db.commit()

    return {
        "success": True,
        "finisher_result": finisher_result,
        "message": "SPEKTAKULÄRER FINISHER!" if success else "Finisher fehlgeschlagen..."
    }


# ============================================================================
# FAME / LEADERBOARD ENDPOINTS
# ============================================================================

@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = Query(100, le=500),
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get fame leaderboard"""

    query = db.query(SlimeFame).order_by(desc(SlimeFame.fame_points))

    if region:
        # TODO: Filter by region if needed
        pass

    leaderboard = query.limit(limit).all()

    # Update rankings
    for rank, fame_entry in enumerate(leaderboard, start=1):
        fame_entry.global_rank = rank

    db.commit()

    return {
        "success": True,
        "leaderboard": [entry.to_dict() for entry in leaderboard],
        "total_entries": len(leaderboard)
    }


@router.get("/fame/{player_id}")
async def get_player_fame(player_id: str, db: Session = Depends(get_db)):
    """Get player fame statistics"""

    fame = db.query(SlimeFame).filter(SlimeFame.player_id == player_id).first()

    if not fame:
        # Create new fame entry
        fame = SlimeFame(player_id=player_id)
        db.add(fame)
        db.commit()
        db.refresh(fame)

    return {
        "success": True,
        "fame": fame.to_dict()
    }


# ============================================================================
# TOURNAMENT ENDPOINTS
# ============================================================================

@router.post("/tournament/register")
async def register_tournament(request: TournamentRegisterRequest, db: Session = Depends(get_db)):
    """Register player for a tournament"""

    tournament = db.query(SlimeTournament).filter(SlimeTournament.id == request.tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Turnier nicht gefunden")

    if tournament.status != "registration":
        raise HTTPException(status_code=400, detail="Registrierung geschlossen")

    participants = tournament.participants or []

    # Check if already registered
    if any(p["player_id"] == request.player_id for p in participants):
        raise HTTPException(status_code=400, detail="Bereits registriert")

    # Check capacity
    if len(participants) >= tournament.max_participants:
        raise HTTPException(status_code=400, detail="Turnier voll")

    # Add participant
    participants.append({
        "player_id": request.player_id,
        "slime_name": request.player_slime_name,
        "slime_type": request.player_slime_type
    })

    tournament.participants = participants
    tournament.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(tournament)

    return {
        "success": True,
        "tournament": tournament.to_dict(),
        "message": f"Registriert! {len(participants)}/{tournament.max_participants} Teilnehmer"
    }


@router.get("/tournament/{tournament_id}")
async def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """Get tournament information"""

    tournament = db.query(SlimeTournament).filter(SlimeTournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Turnier nicht gefunden")

    return {
        "success": True,
        "tournament": tournament.to_dict()
    }


@router.get("/tournament/active")
async def get_active_tournaments(db: Session = Depends(get_db)):
    """Get active and upcoming tournaments"""

    now = datetime.utcnow()
    tournaments = db.query(SlimeTournament).filter(
        (SlimeTournament.status.in_(["registration", "in_progress"])) |
        (SlimeTournament.registration_opens > now)
    ).all()

    return {
        "success": True,
        "tournaments": [t.to_dict() for t in tournaments],
        "total": len(tournaments)
    }


@router.post("/tournament/advance")
async def advance_tournament(request: TournamentAdvanceRequest, db: Session = Depends(get_db)):
    """Advance tournament to next round (admin endpoint)"""

    tournament = db.query(SlimeTournament).filter(SlimeTournament.id == request.tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Turnier nicht gefunden")

    # TODO: Implement bracket advancement logic
    # This would update bracket_data, current_round, etc.

    tournament.current_round += 1
    tournament.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(tournament)

    return {
        "success": True,
        "tournament": tournament.to_dict(),
        "message": f"Turnier zu Runde {tournament.current_round} fortgeschritten"
    }


# Export router
__all__ = ["router"]
