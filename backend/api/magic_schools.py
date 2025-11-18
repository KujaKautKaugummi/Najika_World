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

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from backend.services.magic_schools_system import (
    MagicSchoolSystem, MagicSchool
)

# Create FastAPI Router
router = APIRouter(prefix="/api/magic", tags=["magic"])

# Global System Instance
magic_system = MagicSchoolSystem()

# Initialize default spells
magic_system.create_default_spells()


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class CastSpellRequest(BaseModel):
    spell_id: str
    damage_dealt: float = 0.0


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/cast")
async def cast_spell(request: CastSpellRequest):
    """
    Cast Spell (Skyrim Learning by Doing!)

    Body:
    {
        "spell_id": "fire_novice_1",
        "damage_dealt": 25.0
    }
    """
    try:
        result = magic_system.cast_spell(
            request.spell_id,
            request.damage_dealt
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/school/{school}")
async def get_school_info(school: str):
    """
    Get School Info

    Path: /api/magic/school/feuer
    """
    try:
        # Parse school
        try:
            magic_school = MagicSchool(school)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültige Schule: {school}",
                    "valid_schools": [s.value for s in MagicSchool]
                }
            )

        info = magic_system.get_school_info(magic_school)

        return info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overview")
async def get_overview():
    """
    Get All Schools Overview

    Returns summary for all 9 schools
    """
    try:
        overview = magic_system.get_all_schools_overview()
        return overview

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/can-weave")
async def check_can_weave(
    school1: str = Query(..., description="First magic school"),
    school2: str = Query(..., description="Second magic school")
):
    """
    Check if can weave (combine) 2 schools

    Query Params:
        school1: str
        school2: str

    Example: /api/magic/can-weave?school1=feuer&school2=eis

    WICHTIG: Explosion NIEMALS kombinierbar! (Gebot #3)
    """
    try:
        # Parse schools
        try:
            school1_enum = MagicSchool(school1)
            school2_enum = MagicSchool(school2)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültige Schule: {e}",
                    "valid_schools": [s.value for s in MagicSchool]
                }
            )

        can_weave, reason = magic_system.can_weave(school1_enum, school2_enum)

        return {
            "can_weave": can_weave,
            "reason": reason,
            "school1": school1_enum.value,
            "school2": school2_enum.value
        }

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
async def export_state():
    """
    Export State

    Returns complete state for all schools
    """
    try:
        state = magic_system.export_state()
        return state

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
