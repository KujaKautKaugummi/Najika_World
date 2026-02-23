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

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.database import get_db
from backend.models.slime_companion import SlimeCompanion
from backend.utils import handle_errors

# Create FastAPI Router
router = APIRouter(prefix="/api/slime", tags=["slime"])


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
@handle_errors()
async def create_companion(request: CreateCompanionRequest, db: Session = Depends(get_db)):
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
        # Generate unique companion_id
        max_id = db.query(SlimeCompanion).count()
        new_companion_id = max_id + 1

        # Create new companion
        companion = SlimeCompanion(
            companion_id=new_companion_id,
            owner_player_id=request.owner_player_id,
            name=request.name,
            level=1,
            xp=0,
            xp_required=100,
            fantasy_tier="tier",
            metamorphosed=False,
            metamorphosis_region=request.starting_region,
            collected_colors=[],
            hunger=100.0,
            thirst=100.0,
            schlaf=100.0,
            stimmung=100.0,
            kampfeslust=0.0,
            moves=[],
            max_moves=20,
            is_hardcore=False,
            rescue_available=True,
            health=100.0,
            max_health=100.0,
            attack=10.0,
            defense=10.0,
            total_battles=0,
            total_wins=0,
            created_at=datetime.utcnow(),
            last_fed=datetime.utcnow(),
            last_watered=datetime.utcnow(),
            last_slept=datetime.utcnow(),
            last_update=datetime.utcnow()
        )

        db.add(companion)
        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "level": companion.level,
            "fantasy_tier": companion.fantasy_tier,
            "message": f"{companion.name} wurde erstellt!"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/experience")
@handle_errors()
async def add_experience(request: AddExperienceRequest, db: Session = Depends(get_db)):
    """
    Add Experience

    Body:
    {
        "companion_id": 1,
        "exp_amount": 120
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        # Add XP
        companion.xp += request.exp_amount
        leveled_up = False
        levels_gained = 0

        # Check for level ups
        while companion.xp >= companion.xp_required:
            companion.xp -= companion.xp_required
            companion.level += 1
            levels_gained += 1
            leveled_up = True

            # Increase XP requirement (exponential growth)
            companion.xp_required = int(100 * (1.1 ** companion.level))

            # Increase stats on level up
            companion.max_health += 5
            companion.health = companion.max_health
            companion.attack += 2
            companion.defense += 2

        companion.last_update = datetime.utcnow()
        db.commit()
        db.refresh(companion)

        result = {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "xp_added": request.exp_amount,
            "current_xp": companion.xp,
            "xp_required": companion.xp_required,
            "level": companion.level,
            "leveled_up": leveled_up,
            "levels_gained": levels_gained
        }

        if leveled_up:
            result["message"] = f"{companion.name} ist jetzt Level {companion.level}!"

        return result

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metamorphosis")
@handle_errors()
async def perform_metamorphosis(request: MetamorphosisRequest, db: Session = Depends(get_db)):
    """
    Perform Metamorphosis (Level 50)

    Body:
    {
        "companion_id": 1,
        "current_region": "samtmoos_tiefwald"
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        if companion.level < 50:
            raise HTTPException(
                status_code=400,
                detail=f"Level 50 erforderlich! Aktuelles Level: {companion.level}"
            )

        if companion.metamorphosed:
            raise HTTPException(
                status_code=400,
                detail="Metamorphose bereits durchgeführt!"
            )

        # Perform metamorphosis
        companion.metamorphosed = True
        companion.metamorphosis_region = request.current_region
        companion.fantasy_tier = "slime"

        # Boost stats significantly
        companion.max_health *= 2
        companion.health = companion.max_health
        companion.attack *= 1.5
        companion.defense *= 1.5
        companion.max_moves = 30  # More move slots

        companion.last_update = datetime.utcnow()
        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "fantasy_tier": companion.fantasy_tier,
            "metamorphosis_region": companion.metamorphosis_region,
            "message": f"{companion.name} hat die Metamorphose vollzogen und ist jetzt ein Slime!"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/color/collect")
@handle_errors()
async def collect_color(request: CollectColorRequest, db: Session = Depends(get_db)):
    """
    Collect Slime Color (Rainbow Quest)

    Body:
    {
        "companion_id": 1,
        "region": "reich_der_drei"
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        if companion.fantasy_tier != "slime":
            raise HTTPException(
                status_code=400,
                detail="Nur Slimes können Farben sammeln! Metamorphose erforderlich."
            )

        # Region to color mapping
        region_colors = {
            "samtmoos_tiefwald": "green",
            "reich_der_drei": "blue",
            "kristall_gebirge": "purple",
            "wueste_der_echos": "yellow",
            "feuer_vulkan": "red",
            "ozeanus": "cyan",
            "aether_himmel": "white"
        }

        color = region_colors.get(request.region)
        if not color:
            raise HTTPException(
                status_code=400,
                detail=f"Unbekannte Region: {request.region}"
            )

        if color in companion.collected_colors:
            return {
                "success": False,
                "companion_id": companion.companion_id,
                "name": companion.name,
                "color": color,
                "message": f"Farbe {color} bereits gesammelt!"
            }

        # Add color
        collected = companion.collected_colors or []
        collected.append(color)
        companion.collected_colors = collected

        # Check if rainbow complete
        all_colors = ["red", "yellow", "green", "blue", "purple", "cyan", "white"]
        if set(collected) == set(all_colors):
            companion.fantasy_tier = "rainbow"
            companion.max_health *= 1.5
            companion.health = companion.max_health
            companion.attack *= 1.3
            companion.defense *= 1.3
            message = f"{companion.name} hat alle Farben gesammelt und ist jetzt ein RAINBOW SLIME!"
        else:
            message = f"{companion.name} hat die Farbe {color} gesammelt! ({len(collected)}/7)"

        companion.last_update = datetime.utcnow()
        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "color": color,
            "collected_colors": companion.collected_colors,
            "fantasy_tier": companion.fantasy_tier,
            "message": message
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn")
@handle_errors()
async def try_learn_move(request: LearnMoveRequest, db: Session = Depends(get_db)):
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
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        # Check if move list is full
        current_moves = companion.moves or []
        if len(current_moves) >= companion.max_moves:
            return {
                "success": False,
                "learned": False,
                "companion_id": companion.companion_id,
                "name": companion.name,
                "move_name": request.move_name,
                "message": f"Moveset voll! ({len(current_moves)}/{companion.max_moves})"
            }

        # Check if move already learned
        for move in current_moves:
            if move.get("name") == request.move_name:
                return {
                    "success": False,
                    "learned": False,
                    "companion_id": companion.companion_id,
                    "name": companion.name,
                    "move_name": request.move_name,
                    "message": f"{request.move_name} bereits gelernt!"
                }

        # Learn new move (10% chance)
        import random
        learned = random.random() < 0.10

        if learned:
            move_dict = {
                "name": request.move_name,
                "type": request.move_type,
                "source": request.source_name,
                "learned_at": datetime.utcnow().isoformat()
            }
            current_moves.append(move_dict)
            companion.moves = current_moves
            companion.last_update = datetime.utcnow()
            db.commit()
            db.refresh(companion)

            return {
                "success": True,
                "learned": True,
                "companion_id": companion.companion_id,
                "name": companion.name,
                "move_name": request.move_name,
                "moves_count": len(current_moves),
                "message": f"{companion.name} hat {request.move_name} gelernt!"
            }
        else:
            return {
                "success": True,
                "learned": False,
                "companion_id": companion.companion_id,
                "name": companion.name,
                "move_name": request.move_name,
                "message": f"{companion.name} konnte {request.move_name} nicht lernen (10% Chance)"
            }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rescue")
@handle_errors()
async def use_rescue(request: RescueRequest, db: Session = Depends(get_db)):
    """
    Use Rescue Mechanic (Hardcore)

    Body:
    {
        "companion_id": 1
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        if not companion.is_hardcore:
            raise HTTPException(
                status_code=400,
                detail="Rescue nur im Hardcore-Modus verfügbar!"
            )

        if not companion.rescue_available:
            raise HTTPException(
                status_code=400,
                detail="Rescue nicht verfügbar! Cooldown aktiv."
            )

        # Check if rescue is needed (health < 20%)
        if companion.health > (companion.max_health * 0.2):
            return {
                "success": False,
                "rescued": False,
                "companion_id": companion.companion_id,
                "name": companion.name,
                "message": "Rescue nicht nötig! Health über 20%."
            }

        # Perform rescue
        companion.health = companion.max_health
        companion.rescue_available = False
        companion.last_rescue_time = datetime.utcnow()
        companion.rescue_cooldown_until = datetime.utcnow() + timedelta(hours=24)
        companion.last_update = datetime.utcnow()

        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "rescued": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "health": companion.health,
            "cooldown_until": companion.rescue_cooldown_until.isoformat(),
            "message": f"{companion.name} wurde gerettet! 24h Cooldown aktiv."
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tamagotchi/update")
@handle_errors()
async def update_tamagotchi(request: UpdateTamagotchiRequest, db: Session = Depends(get_db)):
    """
    Update Tamagotchi Stats (Decay)

    Body:
    {
        "companion_id": 1,
        "delta_hours": 1.0
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        # Calculate time delta
        if request.delta_hours is not None:
            hours = request.delta_hours
        else:
            # Calculate from last_update
            time_diff = datetime.utcnow() - companion.last_update
            hours = time_diff.total_seconds() / 3600

        # Decay rates per hour
        hunger_decay = 5.0 * hours
        thirst_decay = 8.0 * hours
        sleep_decay = 4.0 * hours

        # Apply decay
        companion.hunger = max(0.0, companion.hunger - hunger_decay)
        companion.thirst = max(0.0, companion.thirst - thirst_decay)
        companion.schlaf = max(0.0, companion.schlaf - sleep_decay)

        # Update mood based on needs
        needs = [companion.hunger, companion.thirst, companion.schlaf]
        avg_needs = sum(needs) / len(needs)
        if avg_needs < 30:
            companion.stimmung = max(0.0, companion.stimmung - 10.0)
        elif avg_needs > 70:
            companion.stimmung = min(100.0, companion.stimmung + 5.0)

        # Update kampfeslust (battle lust increases with low mood)
        if companion.stimmung < 50:
            companion.kampfeslust = min(100.0, companion.kampfeslust + 10.0)
        else:
            companion.kampfeslust = max(0.0, companion.kampfeslust - 5.0)

        companion.last_update = datetime.utcnow()
        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "hours_passed": round(hours, 2),
            "needs": {
                "hunger": companion.hunger,
                "thirst": companion.thirst,
                "schlaf": companion.schlaf,
                "stimmung": companion.stimmung,
                "kampfeslust": companion.kampfeslust,
            },
            "message": f"Tamagotchi Stats aktualisiert ({round(hours, 2)}h vergangen)"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feed")
@handle_errors()
async def feed_companion(request: FeedCompanionRequest, db: Session = Depends(get_db)):
    """
    Feed Companion

    Body:
    {
        "companion_id": 1,
        "amount": 30.0
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        # Increase hunger (max 100)
        companion.hunger = min(100.0, companion.hunger + request.amount)
        companion.last_fed = datetime.utcnow()
        companion.last_update = datetime.utcnow()

        # Improve mood if hunger was low
        if companion.hunger < 30:
            companion.stimmung = min(100.0, companion.stimmung + 10.0)

        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "hunger": companion.hunger,
            "stimmung": companion.stimmung,
            "message": f"{companion.name} wurde gefüttert!"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/water")
@handle_errors()
async def give_water(request: GiveWaterRequest, db: Session = Depends(get_db)):
    """
    Give Water

    Body:
    {
        "companion_id": 1,
        "amount": 40.0
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        # Increase thirst (max 100)
        companion.thirst = min(100.0, companion.thirst + request.amount)
        companion.last_watered = datetime.utcnow()
        companion.last_update = datetime.utcnow()

        # Improve mood if thirst was low
        if companion.thirst < 30:
            companion.stimmung = min(100.0, companion.stimmung + 10.0)

        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "thirst": companion.thirst,
            "stimmung": companion.stimmung,
            "message": f"{companion.name} hat Wasser bekommen!"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sleep")
@handle_errors()
async def let_sleep(request: LetSleepRequest, db: Session = Depends(get_db)):
    """
    Let Sleep

    Body:
    {
        "companion_id": 1,
        "hours": 8.0
    }
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == request.companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        # Restore sleep based on hours (10 per hour)
        sleep_restored = request.hours * 10.0
        companion.schlaf = min(100.0, companion.schlaf + sleep_restored)
        companion.last_slept = datetime.utcnow()
        companion.last_update = datetime.utcnow()

        # Improve mood with good sleep
        if sleep_restored >= 50:
            companion.stimmung = min(100.0, companion.stimmung + 15.0)

        db.commit()
        db.refresh(companion)

        return {
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "schlaf": companion.schlaf,
            "stimmung": companion.stimmung,
            "hours_slept": request.hours,
            "message": f"{companion.name} hat {request.hours} Stunden geschlafen!"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{companion_id}")
@handle_errors()
async def get_companion_info(companion_id: int, db: Session = Depends(get_db)):
    """
    Get Companion Info

    Path: /api/slime/1
    """
    try:
        companion = db.query(SlimeCompanion).filter(
            SlimeCompanion.companion_id == companion_id
        ).first()

        if not companion:
            raise HTTPException(status_code=404, detail="Companion nicht gefunden")

        return companion.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
@handle_errors()
async def export_state(db: Session = Depends(get_db)):
    """
    Export Slime State

    Returns:
        JSON with all companions
    """
    try:
        companions = db.query(SlimeCompanion).all()

        companions_data = {}
        for companion in companions:
            companions_data[str(companion.companion_id)] = companion.to_dict()

        return {
            "companions": companions_data,
            "count": len(companions_data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/state/import")
@handle_errors()
async def import_state(state: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Import Slime State

    Body: Complete state object (from export)
    """
    try:
        if not state or "companions" not in state:
            raise HTTPException(status_code=400, detail="Ungültige State-Daten")

        companions_data = state.get("companions", {})
        imported_count = 0

        for companion_id, companion_dict in companions_data.items():
            # Check if companion already exists
            existing = db.query(SlimeCompanion).filter(
                SlimeCompanion.companion_id == int(companion_id)
            ).first()

            if existing:
                # Update existing
                for key, value in companion_dict.items():
                    if hasattr(existing, key) and key != "id":
                        setattr(existing, key, value)
            else:
                # Create new
                new_companion = SlimeCompanion(**companion_dict)
                db.add(new_companion)

            imported_count += 1

        db.commit()

        return {
            "success": True,
            "message": "Slime State importiert",
            "companions": imported_count
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
