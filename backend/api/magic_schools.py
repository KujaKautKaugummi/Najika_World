"""
Magic Schools API - Najika World
=================================

REST API für 9 Magieschulen System (FastAPI)

Endpoints:
- POST /api/magic/cast - Cast spell (Skyrim Learning!)
- GET /api/magic/school/<school> - Get school info
- GET /api/magic/overview - Get all schools overview
- GET /api/magic/can-weave - Check if can weave
- GET /api/magic/spells - Get all spells
- GET /api/magic/state/export - Export state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import get_db
from backend.models.magic_progress import MagicSchoolProgress

# Create FastAPI Router
router = APIRouter(prefix="/api/magic", tags=["magic"])


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_or_create_school_progress(db: Session, player_id: int, school: str) -> MagicSchoolProgress:
    """Get or create progress for a magic school"""
    progress = db.query(MagicSchoolProgress).filter(
        MagicSchoolProgress.player_id == player_id,
        MagicSchoolProgress.school == school
    ).first()

    if not progress:
        progress = MagicSchoolProgress(
            player_id=player_id,
            school=school,
            level=1,
            xp=0.0,
            xp_required=100.0,
            unlocked_spells=[],
            can_weave=False
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return progress


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class CastSpellRequest(BaseModel):
    player_id: int
    school: str
    spell_id: str
    damage_dealt: float = 0.0


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/cast")
async def cast_spell(request: CastSpellRequest, db: Session = Depends(get_db)):
    """
    Cast Spell (Skyrim Learning by Doing!)

    Body:
    {
        "player_id": 1,
        "school": "feuer",
        "spell_id": "fire_novice_1",
        "damage_dealt": 25.0
    }
    """
    try:
        # Validate school
        valid_schools = ["feuer", "eis", "blitz", "wasser", "erde", "wind", "licht", "dunkelheit", "explosion"]
        if request.school not in valid_schools:
            raise HTTPException(status_code=400, detail={"error": f"Ungültige Schule: {request.school}", "valid_schools": valid_schools})

        # Get or create progress
        progress = get_or_create_school_progress(db, request.player_id, request.school)

        # Add XP based on damage
        xp_gained = request.damage_dealt
        progress.xp += xp_gained
        progress.total_casts += 1
        progress.total_damage += request.damage_dealt
        progress.last_cast = datetime.utcnow()

        # Perfect cast bonus
        if request.damage_dealt >= 50:
            progress.perfect_casts += 1

        # Level up logic
        leveled_up = False
        while progress.xp >= progress.xp_required:
            progress.xp -= progress.xp_required
            progress.level += 1
            leveled_up = True
            progress.xp_required = 100 * (1.2 ** progress.level)
            if progress.level >= 20:
                progress.can_weave = True

        # Unlock spell
        unlocked = progress.unlocked_spells or []
        if request.spell_id not in unlocked:
            unlocked.append(request.spell_id)
            progress.unlocked_spells = unlocked

        db.commit()
        db.refresh(progress)

        return {
            "success": True,
            "school": request.school,
            "xp_gained": xp_gained,
            "level": progress.level,
            "xp": progress.xp,
            "leveled_up": leveled_up,
            "can_weave": progress.can_weave
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/school/{school}")
async def get_school_info(school: str, player_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Get School Info

    Path: /api/magic/school/feuer?player_id=1
    """
    try:
        valid_schools = ["feuer", "eis", "blitz", "wasser", "erde", "wind", "licht", "dunkelheit", "explosion"]
        if school not in valid_schools:
            raise HTTPException(status_code=400, detail={"error": f"Ungültige Schule: {school}", "valid_schools": valid_schools})

        progress = get_or_create_school_progress(db, player_id, school)
        return progress.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overview")
async def get_overview(player_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Get All Schools Overview

    Query: /api/magic/overview?player_id=1
    """
    try:
        all_schools = ["feuer", "eis", "blitz", "wasser", "erde", "wind", "licht", "dunkelheit", "explosion"]
        overview = []
        for school in all_schools:
            progress = get_or_create_school_progress(db, player_id, school)
            overview.append({"school": school, "level": progress.level, "xp": progress.xp, "can_weave": progress.can_weave})
        return {"player_id": player_id, "schools": overview}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/can-weave")
async def check_can_weave(
    player_id: int = Query(...),
    school1: str = Query(...),
    school2: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Check if can weave (combine) 2 schools

    Example: /api/magic/can-weave?player_id=1&school1=feuer&school2=eis

    WICHTIG: Explosion NIEMALS kombinierbar! (Gebot #3)
    """
    try:
        if school1 == "explosion" or school2 == "explosion":
            return {"can_weave": False, "reason": "Explosion kann NIEMALS kombiniert werden!"}

        if school1 == school2:
            return {"can_weave": False, "reason": "Gleiche Schulen können nicht kombiniert werden"}

        progress1 = get_or_create_school_progress(db, player_id, school1)
        progress2 = get_or_create_school_progress(db, player_id, school2)

        if progress1.can_weave and progress2.can_weave:
            return {"can_weave": True, "reason": "Beide Schulen Level 20+!", "school1": school1, "school2": school2}
        else:
            return {"can_weave": False, "reason": f"Level 20+ required. {school1}: {progress1.level}, {school2}: {progress2.level}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spells")
async def get_all_spells(
    school: Optional[str] = Query(None, description="Filter by school"),
    unlocked_only: bool = Query(False, description="Only show unlocked spells")
):
    """
    Get All Spells

    Optional Query Params:
        school: str (filter by school)
        unlocked_only: bool (only show unlocked)
    """
    try:
        spells_list = []

        for spell_id, spell in magic_system.spells.items():
            # School filter
            if school and spell.school.value != school:
                continue

            # Unlocked filter
            if unlocked_only:
                progress = magic_system.school_progress[spell.school]
                if spell_id not in progress.unlocked_spells:
                    continue

            spells_list.append({
                "spell_id": spell.spell_id,
                "name": spell.name,
                "school": spell.school.value,
                "tier": spell.tier.value,
                "required_level": spell.required_level,
                "mana_cost": spell.mana_cost,
                "base_damage": spell.base_damage,
                "description": spell.description,
                "is_ultimate": spell.is_ultimate,
                "can_weave": spell.can_weave
            })

        return {
            "spells": spells_list,
            "total": len(spells_list)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
async def export_state(player_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Export State

    Returns complete state for all schools for a player
    """
    try:
        all_progress = db.query(MagicSchoolProgress).filter(MagicSchoolProgress.player_id == player_id).all()
        schools_data = {p.school: p.to_dict() for p in all_progress}
        return {"player_id": player_id, "schools": schools_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
