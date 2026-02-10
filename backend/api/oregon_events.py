"""
Oregon Trail Events API - Najika World
=======================================

REST API für Oregon Trail Events System (FastAPI)

Endpoints (DATABASE):
- GET /api/oregon/journey/start - Start new journey
- GET /api/oregon/journey/status - Get journey status
- POST /api/oregon/trigger - Trigger random event
- POST /api/oregon/choice - Execute player choice
- POST /api/oregon/progress - Add travel progress
- GET /api/oregon/events - Get event history

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import random

from backend.database import get_db
from backend.models.oregon_trail import OregonTrailJourney, OregonTrailEvent
from backend.services.oregon_trail_events import OregonTrailEventsSystem

# Create FastAPI Router
router = APIRouter(prefix="/api/oregon", tags=["oregon"])

# Global System Instance (for event generation logic)
oregon_system = OregonTrailEventsSystem()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_or_create_journey(db: Session, player_id: int) -> OregonTrailJourney:
    """Get or create active journey for player"""
    # Look for active journey
    journey = db.query(OregonTrailJourney).filter(
        OregonTrailJourney.player_id == player_id,
        OregonTrailJourney.active == True
    ).first()

    if not journey:
        # Create new journey
        journey = OregonTrailJourney(
            player_id=player_id,
            active=True,
            completed=False,
            distance_traveled=0,
            days_elapsed=0,
            current_location="Independence, Missouri",
            party_health=100.0,
            party_morale=100.0,
            party_members=["John", "Mary", "Sarah", "Tom"],
            alive_members=4,
            food=200,
            water=50,
            money=100,
            ammunition=50,
            oxen=2,
            wagon_wheels=2,
            wagon_axles=1,
            wagon_tongues=1
        )
        db.add(journey)
        db.commit()
        db.refresh(journey)

    return journey


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class TriggerEventRequest(BaseModel):
    player_id: int
    location: str = "any"
    player_class: Optional[str] = None


class ExecuteChoiceRequest(BaseModel):
    player_id: int
    event_id: int
    choice_index: int


class AddProgressRequest(BaseModel):
    player_id: int
    distance: int = 10  # miles
    days: int = 1


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/journey/start")
async def start_journey(
    player_id: int = Query(..., description="Player ID"),
    db: Session = Depends(get_db)
):
    """
    Start New Journey (DATABASE)

    Query Params:
        player_id: int

    Example: /api/oregon/journey/start?player_id=1
    """
    try:
        # End any active journeys
        active_journeys = db.query(OregonTrailJourney).filter(
            OregonTrailJourney.player_id == player_id,
            OregonTrailJourney.active == True
        ).all()

        for journey in active_journeys:
            journey.active = False
            journey.ended_at = datetime.utcnow()

        # Create new journey
        journey = OregonTrailJourney(
            player_id=player_id,
            active=True,
            completed=False,
            distance_traveled=0,
            days_elapsed=0,
            current_location="Independence, Missouri"
        )

        db.add(journey)
        db.commit()
        db.refresh(journey)

        return {
            "success": True,
            "journey_id": journey.id,
            "message": "Deine Oregon Trail Reise hat begonnen!",
            "journey": journey.to_dict()
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/journey/status")
async def get_journey_status(
    player_id: int = Query(..., description="Player ID"),
    db: Session = Depends(get_db)
):
    """
    Get Journey Status (DATABASE)

    Query Params:
        player_id: int

    Example: /api/oregon/journey/status?player_id=1
    """
    try:
        journey = get_or_create_journey(db, player_id)

        return {
            "active": journey.active,
            "journey": journey.to_dict()
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/random")
async def get_random_event(player_id: int = Query(1), db: Session = Depends(get_db)):
    """
    Get Random Event (Frontend: game_systems_ui.js OregonEventsUI.show)

    Returns a random Oregon Trail event for display.
    """
    try:
        journey = get_or_create_journey(db, player_id)
        event_data = oregon_system.trigger_random_event("wilderness", "adventurer")
        if not event_data:
            return {
                "title": "Ruhige Reise",
                "text": "Die Straße ist ruhig... zu ruhig.",
                "options": [
                    {"text": "Weiterreisen", "effect": {"distance": 10}},
                    {"text": "Rasten", "effect": {"health": 5}}
                ],
                "najika_reaction": "*schaut sich nervös um* Kuja, hier ist es so still..."
            }
        return event_data
    except Exception as e:
        return {
            "title": "Händler-Karawane",
            "text": "Eine Karawane bietet dir ihre Waren an.",
            "options": [
                {"text": "Kaufen", "effect": {"gold": -10, "items": 1}},
                {"text": "Ablehnen", "effect": {}}
            ],
            "najika_reaction": "*kicher* Die haben glänzende Sachen, Mr. K!"
        }


@router.get("/chaos")
async def get_chaos_event():
    """
    Get Chaos Event (Frontend: game_systems_ui.js OregonEventsUI - chaos check)

    Returns a random chaos event or no event.
    """
    chance = random.random()
    if chance < 0.3:
        return {
            "chaos_event": True,
            "event": {
                "title": "CHAOS!",
                "description": "Ein unerwartetes Chaos-Event!",
                "effect": {"chaos_level": random.randint(1, 5)}
            },
            "najika_reaction": "EXPLOSION!!! *aufgeregt hüpf*"
        }
    return {"chaos_event": False, "message": "Kein Chaos... diesmal."}


@router.post("/trigger")
async def trigger_event(request: TriggerEventRequest, db: Session = Depends(get_db)):
    """
    Trigger Random Event (DATABASE)

    Body:
    {
        "player_id": 1,
        "location": "wilderness",
        "player_class": "mage"
    }
    """
    try:
        journey = get_or_create_journey(db, request.player_id)

        # Use oregon_system to generate event
        event_data = oregon_system.trigger_random_event(
            request.location,
            request.player_class
        )

        if not event_data:
            return {
                "triggered": False,
                "message": "Kein Event getriggert"
            }

        # Log event in database
        event = OregonTrailEvent(
            journey_id=journey.id,
            event_type=event_data.get("type", "random"),
            event_name=event_data.get("title", "Unbekanntes Event"),
            event_description=event_data.get("description", ""),
            choices=event_data.get("choices", []),
            location_at_event=journey.current_location,
            distance_at_event=journey.distance_traveled,
            occurred_at=datetime.utcnow()
        )

        db.add(event)
        journey.total_events += 1
        journey.last_event_at = datetime.utcnow()

        db.commit()
        db.refresh(event)

        return {
            "triggered": True,
            "event_id": event.id,
            "event": event_data
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/choice")
async def execute_choice(request: ExecuteChoiceRequest, db: Session = Depends(get_db)):
    """
    Execute Player Choice (DATABASE)

    Body:
    {
        "player_id": 1,
        "event_id": 5,
        "choice_index": 0
    }
    """
    try:
        journey = get_or_create_journey(db, request.player_id)

        # Find event
        event = db.query(OregonTrailEvent).filter(
            OregonTrailEvent.id == request.event_id
        ).first()

        if not event:
            raise HTTPException(status_code=404, detail="Event nicht gefunden")

        if event.journey_id != journey.id:
            raise HTTPException(status_code=403, detail="Event gehört nicht zu deiner Journey")

        # Validate choice index
        if request.choice_index < 0 or request.choice_index >= len(event.choices or []):
            raise HTTPException(status_code=400, detail="Ungültiger Choice Index")

        choice_text = event.choices[request.choice_index] if event.choices else ""

        # Update event with choice
        event.player_choice = choice_text
        event.success = random.random() > 0.3  # 70% success rate

        # Calculate impact
        impact = {}
        if event.success:
            impact = {"gold": random.randint(-10, 20), "morale": random.randint(5, 15)}
            event.outcome = "Erfolg!"
        else:
            impact = {"health": random.randint(-20, -5), "food": random.randint(-15, -5)}
            event.outcome = "Fehlgeschlagen!"

        event.impact = impact

        # Apply impact to journey
        if "food" in impact:
            journey.food = max(0, journey.food + impact["food"])
        if "health" in impact:
            journey.party_health = max(0, min(100, journey.party_health + impact["health"]))
        if "morale" in impact:
            journey.party_morale = max(0, min(100, journey.party_morale + impact["morale"]))
        if "gold" in impact:
            journey.money = max(0, journey.money + impact["gold"])

        db.commit()
        db.refresh(event)
        db.refresh(journey)

        return {
            "success": True,
            "choice": choice_text,
            "outcome": event.outcome,
            "impact": impact,
            "journey": journey.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/progress")
async def add_progress(request: AddProgressRequest, db: Session = Depends(get_db)):
    """
    Add Travel Progress (DATABASE)

    Body:
    {
        "player_id": 1,
        "distance": 10,
        "days": 1
    }
    """
    try:
        journey = get_or_create_journey(db, request.player_id)

        # Update journey progress
        journey.distance_traveled += request.distance
        journey.days_elapsed += request.days

        # Consume resources
        journey.food -= (journey.alive_members * 2 * request.days)  # 2 lbs per person per day
        journey.water -= (journey.alive_members * 1 * request.days)  # 1 gallon per person per day

        # Check if out of resources
        if journey.food <= 0:
            journey.party_health -= 10
            journey.party_morale -= 15
        if journey.water <= 0:
            journey.party_health -= 20
            journey.party_morale -= 20

        # Check if reached Oregon (2000 miles)
        if journey.distance_traveled >= 2000:
            journey.completed = True
            journey.active = False
            journey.ended_at = datetime.utcnow()

        db.commit()
        db.refresh(journey)

        return {
            "success": True,
            "distance_traveled": journey.distance_traveled,
            "days_elapsed": journey.days_elapsed,
            "completed": journey.completed,
            "journey": journey.to_dict()
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events")
async def get_event_history(
    player_id: int = Query(..., description="Player ID"),
    limit: int = Query(10, ge=1, le=100, description="Max events to return"),
    db: Session = Depends(get_db)
):
    """
    Get Event History (DATABASE)

    Query Params:
        player_id: int
        limit: int (default 10, max 100)

    Example: /api/oregon/events?player_id=1&limit=20
    """
    try:
        journey = get_or_create_journey(db, player_id)

        events = db.query(OregonTrailEvent).filter(
            OregonTrailEvent.journey_id == journey.id
        ).order_by(
            OregonTrailEvent.occurred_at.desc()
        ).limit(limit).all()

        return {
            "journey_id": journey.id,
            "event_count": len(events),
            "events": [event.to_dict() for event in events]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
