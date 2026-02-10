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
    player_id: int = Query(1, description="Player ID")
):
    """
    Get All Spells

    Optional Query Params:
        school: str (filter by school)
        player_id: int (default 1)
    """
    # Static spell definitions (Explosion darf NIEMALS mit anderen kombiniert werden!)
    all_spells = [
        {"spell_id": "feuerball", "name": "Feuerball", "school": "feuer", "tier": "basic", "required_level": 1, "mana_cost": 10, "base_damage": 25, "description": "Ein brennender Ball aus Feuer", "is_ultimate": False, "can_weave": True},
        {"spell_id": "feuersturm", "name": "Feuersturm", "school": "feuer", "tier": "advanced", "required_level": 5, "mana_cost": 30, "base_damage": 60, "description": "Ein gewaltiger Sturm aus Flammen", "is_ultimate": False, "can_weave": True},
        {"spell_id": "eislanze", "name": "Eislanze", "school": "eis", "tier": "basic", "required_level": 1, "mana_cost": 12, "base_damage": 20, "description": "Ein scharfer Speer aus Eis", "is_ultimate": False, "can_weave": True},
        {"spell_id": "blizzard", "name": "Blizzard", "school": "eis", "tier": "advanced", "required_level": 5, "mana_cost": 35, "base_damage": 55, "description": "Ein eisiger Schneesturm", "is_ultimate": False, "can_weave": True},
        {"spell_id": "blitzschlag", "name": "Blitzschlag", "school": "blitz", "tier": "basic", "required_level": 1, "mana_cost": 15, "base_damage": 30, "description": "Ein zuckender Blitz", "is_ultimate": False, "can_weave": True},
        {"spell_id": "donnersturm", "name": "Donnersturm", "school": "blitz", "tier": "advanced", "required_level": 5, "mana_cost": 40, "base_damage": 70, "description": "Ein gewaltiger Donner", "is_ultimate": False, "can_weave": True},
        {"spell_id": "wasserstrahl", "name": "Wasserstrahl", "school": "wasser", "tier": "basic", "required_level": 1, "mana_cost": 8, "base_damage": 15, "description": "Ein Strahl reinen Wassers", "is_ultimate": False, "can_weave": True},
        {"spell_id": "erdstoss", "name": "Erdstoß", "school": "erde", "tier": "basic", "required_level": 1, "mana_cost": 10, "base_damage": 20, "description": "Die Erde bebt", "is_ultimate": False, "can_weave": True},
        {"spell_id": "windsense", "name": "Windsense", "school": "wind", "tier": "basic", "required_level": 1, "mana_cost": 8, "base_damage": 12, "description": "Scharfe Windsicheln", "is_ultimate": False, "can_weave": True},
        {"spell_id": "heiliges_licht", "name": "Heiliges Licht", "school": "licht", "tier": "basic", "required_level": 1, "mana_cost": 15, "base_damage": 18, "description": "Heilendes und schädigendes Licht", "is_ultimate": False, "can_weave": True},
        {"spell_id": "schattenpfeil", "name": "Schattenpfeil", "school": "dunkelheit", "tier": "basic", "required_level": 1, "mana_cost": 12, "base_damage": 22, "description": "Ein Pfeil aus reiner Dunkelheit", "is_ultimate": False, "can_weave": True},
        {"spell_id": "explosion", "name": "EXPLOSION!!!", "school": "explosion", "tier": "ultimate", "required_level": 1, "mana_cost": 100, "base_damage": 999, "description": "EXPLOSION!!! Die ultimative Zerstörung!", "is_ultimate": True, "can_weave": False},
    ]

    spells_list = all_spells
    if school:
        spells_list = [s for s in spells_list if s["school"] == school]

    return {
        "spells": spells_list,
        "total": len(spells_list)
    }


# ============================================================================
# CROSS-ELEMENT LEARNING (Magic/Skill System V3)
# ============================================================================

# Element-Similarity Table
ELEMENT_SIMILARITY = {
    "feuer": {
        "same": ["feuer"],
        "similar": ["blitz", "licht"],  # Energy-based
        "foreign": ["eis", "wasser", "erde", "wind", "dunkelheit", "natur"]
    },
    "eis": {
        "same": ["eis"],
        "similar": ["wasser", "wind"],  # Cold/fluid
        "foreign": ["feuer", "blitz", "erde", "licht", "dunkelheit", "natur"]
    },
    "blitz": {
        "same": ["blitz"],
        "similar": ["feuer", "licht"],  # Energy-based
        "foreign": ["eis", "wasser", "erde", "wind", "dunkelheit", "natur"]
    },
    "wasser": {
        "same": ["wasser"],
        "similar": ["eis", "natur"],  # Nature/fluid
        "foreign": ["feuer", "blitz", "erde", "wind", "licht", "dunkelheit"]
    },
    "erde": {
        "same": ["erde"],
        "similar": ["natur", "wind"],  # Physical/nature
        "foreign": ["feuer", "eis", "blitz", "wasser", "licht", "dunkelheit"]
    },
    "wind": {
        "same": ["wind"],
        "similar": ["eis", "erde"],  # Movement/physical
        "foreign": ["feuer", "blitz", "wasser", "licht", "dunkelheit", "natur"]
    },
    "natur": {
        "same": ["natur"],
        "similar": ["erde", "wasser"],  # Life/growth
        "foreign": ["feuer", "eis", "blitz", "wind", "licht", "dunkelheit"]
    },
    "licht": {
        "same": ["licht"],
        "similar": ["feuer", "blitz"],  # Energy/divine
        "foreign": ["eis", "wasser", "erde", "wind", "natur", "dunkelheit"]
    },
    "dunkelheit": {
        "same": ["dunkelheit"],
        "similar": ["natur"],  # Void/corruption
        "foreign": ["feuer", "eis", "blitz", "wasser", "erde", "wind", "licht"]
    },
    "explosion": {
        "same": ["explosion"],
        "similar": [],  # EXPLOSION kann nicht kombiniert werden!
        "foreign": []
    }
}


# ============================================================================
# 1-SKILL-WEG (MEISTER-PATH) System
# ============================================================================

class ActivateMeisterRequest(BaseModel):
    player_id: int
    skill_id: str
    school: str


# ============================================================================
# MORPHS SYSTEM (Diablo 4 Style)
# ============================================================================

class LearnMorphRequest(BaseModel):
    player_id: int
    spell_id: str
    morph_id: str
    method: str  # "observe", "experiment", "cross-learn"


class ActivateMorphRequest(BaseModel):
    player_id: int
    spell_id: str
    morph_id: str  # or "standard" for base version


class ObserveSpellRequest(BaseModel):
    player_id: int
    observed_school: str
    observed_spell: str
    player_school: str  # Current school player is learning


@router.post("/observe")
async def observe_spell(request: ObserveSpellRequest, db: Session = Depends(get_db)):
    """
    Observe spell for cross-element learning

    Learning rates:
    - Same element: 10% chance after 10x observations
    - Similar element: 3% chance after 30x observations
    - Foreign element: 1% chance after 100x observations

    Body:
    {
        "player_id": 1,
        "observed_school": "feuer",
        "observed_spell": "feuerball",
        "player_school": "eis"
    }
    """
    import random

    try:
        # Check if explosion (cannot be learned cross-element)
        if request.observed_school == "explosion":
            return {
                "success": False,
                "message": "EXPLOSION kann nicht durch Beobachtung gelernt werden!",
                "learned": False
            }

        # Determine similarity
        similarity_data = ELEMENT_SIMILARITY.get(request.player_school, {})

        if request.observed_school in similarity_data.get("same", []):
            similarity = "same"
            learn_chance = 0.10  # 10%
            observations_needed = 10
        elif request.observed_school in similarity_data.get("similar", []):
            similarity = "similar"
            learn_chance = 0.03  # 3%
            observations_needed = 30
        else:
            similarity = "foreign"
            learn_chance = 0.01  # 1%
            observations_needed = 100

        # Get or create progress for observed school
        progress = get_or_create_school_progress(db, request.player_id, request.observed_school)

        # Track observations (store in a metadata field or separate table)
        # For now, simple random check
        if random.random() < learn_chance:
            # LEARNED!
            if request.observed_spell not in progress.unlocked_spells:
                progress.unlocked_spells.append(request.observed_spell)
                db.commit()

                return {
                    "success": True,
                    "learned": True,
                    "message": f"🎓 Technik gelernt! {request.observed_spell} (durch Beobachtung)",
                    "similarity": similarity,
                    "learn_chance": learn_chance
                }

        return {
            "success": True,
            "learned": False,
            "message": f"Beobachtet... ({similarity}, {int(learn_chance * 100)}% Chance)",
            "similarity": similarity,
            "learn_chance": learn_chance,
            "observations_needed": observations_needed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/meister/activate")
async def activate_meister(request: ActivateMeisterRequest, db: Session = Depends(get_db)):
    """
    Activate Meister-Weg (1-Skill-Weg)

    UNWIDERRUFLICH!
    - +300% Damage für gewählten Skill
    - Andere Skills verkümmern über Zeit:
      - Tag 30: -20%
      - Tag 90: -80%
      - Tag 180: -90%

    Body:
    {
        "player_id": 1,
        "skill_id": "kleine_explosion",
        "school": "explosion"
    }
    """
    from datetime import datetime

    try:
        progress = get_or_create_school_progress(db, request.player_id, request.school)

        # Check if already Meister
        if hasattr(progress, 'meister_skill') and progress.meister_skill:
            return {
                "success": False,
                "message": f"Du bist bereits Meister in: {progress.meister_skill}",
                "is_meister": True
            }

        # Activate Meister mode (store in DB - you might need to add field to model)
        # For now, store in metadata or create separate table
        progress.meister_skill = request.skill_id
        progress.meister_activated_at = datetime.now()
        progress.meister_damage_bonus = 3.0  # +300%

        db.commit()

        return {
            "success": True,
            "message": f"🎯 Du bist jetzt MEISTER in: {request.skill_id}",
            "is_meister": True,
            "skill_id": request.skill_id,
            "damage_bonus": 3.0,
            "warning": "Andere Skills werden über Zeit verkümmern!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meister/degradation")
async def get_degradation(player_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Get skill degradation status for Meister player

    Returns degradation percentages for all non-Meister skills
    """
    from datetime import datetime

    try:
        # Find Meister school
        all_progress = db.query(MagicSchoolProgress).filter(MagicSchoolProgress.player_id == player_id).all()

        meister_skill = None
        meister_activated_at = None

        for progress in all_progress:
            if hasattr(progress, 'meister_skill') and progress.meister_skill:
                meister_skill = progress.meister_skill
                meister_activated_at = progress.meister_activated_at
                break

        if not meister_skill:
            return {
                "is_meister": False,
                "degraded_skills": []
            }

        # Calculate days since activation
        days_since = (datetime.now() - meister_activated_at).days

        # Calculate degradation
        if days_since >= 180:
            penalty = 0.9
        elif days_since >= 90:
            penalty = 0.8
        elif days_since >= 30:
            penalty = 0.2
        else:
            penalty = 0.0

        # Get all schools except Meister school
        degraded_skills = []
        for progress in all_progress:
            if not hasattr(progress, 'meister_skill') or progress.school != meister_skill:
                degraded_skills.append({
                    "school": progress.school,
                    "penalty": penalty,
                    "penalty_percent": int(penalty * 100),
                    "days_since_meister": days_since
                })

        return {
            "is_meister": True,
            "meister_skill": meister_skill,
            "days_since_activation": days_since,
            "current_penalty": penalty,
            "degraded_skills": degraded_skills
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/morph/learn")
async def learn_morph(request: LearnMorphRequest, db: Session = Depends(get_db)):
    """
    Learn a morph through observation or experimentation

    Methods:
    - observe: Watch others use it (10x = 10% for same element)
    - experiment: Try 30x yourself
    - cross-learn: Learn technique from different element
    """
    import random

    try:
        # Get progress for spell's school
        # (You'd need to determine school from spell_id)
        school = "feuer"  # TODO: Look up from spell database

        progress = get_or_create_school_progress(db, request.player_id, school)

        # Track learned morphs (would need field in DB)
        if not hasattr(progress, 'learned_morphs'):
            progress.learned_morphs = {}

        if request.spell_id not in progress.learned_morphs:
            progress.learned_morphs[request.spell_id] = []

        # Check if already learned
        if request.morph_id in progress.learned_morphs[request.spell_id]:
            return {
                "success": False,
                "message": "Morph bereits gelernt!",
                "learned": False
            }

        # Learn based on method
        if request.method == "experiment":
            # 30x usage = breakthrough
            progress.learned_morphs[request.spell_id].append(request.morph_id)
            db.commit()

            return {
                "success": True,
                "learned": True,
                "message": f"💡 DURCHBRUCH! Morph gelernt: {request.morph_id}",
                "method": "experimentation"
            }

        elif request.method == "observe":
            # Random chance based on similarity
            if random.random() < 0.10:
                progress.learned_morphs[request.spell_id].append(request.morph_id)
                db.commit()

                return {
                    "success": True,
                    "learned": True,
                    "message": f"🎓 Durch Beobachtung gelernt: {request.morph_id}",
                    "method": "observation"
                }

        return {
            "success": True,
            "learned": False,
            "message": "Noch nicht gelernt, weiter üben!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/morph/activate")
async def activate_morph(request: ActivateMorphRequest, db: Session = Depends(get_db)):
    """
    Activate a morph (only 1 can be active per spell)

    Body:
    {
        "player_id": 1,
        "spell_id": "kleine_explosion",
        "morph_id": "mini_explosion"  // or "standard"
    }
    """
    try:
        school = "feuer"  # TODO: Look up from spell_id
        progress = get_or_create_school_progress(db, request.player_id, school)

        # Track active morphs
        if not hasattr(progress, 'active_morphs'):
            progress.active_morphs = {}

        # Activate morph
        progress.active_morphs[request.spell_id] = request.morph_id
        db.commit()

        return {
            "success": True,
            "message": f"🔮 Morph aktiviert: {request.morph_id}",
            "spell_id": request.spell_id,
            "morph_id": request.morph_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schools")
async def list_schools(player_id: int = Query(1), db: Session = Depends(get_db)):
    """
    List All Schools (Frontend: game_systems_ui.js MagicUI.loadSchools)

    Returns schools array with id, name, level, xp for each school.
    """
    all_schools = ["feuer", "eis", "blitz", "wasser", "erde", "wind", "licht", "dunkelheit", "explosion"]
    school_names = {
        "feuer": "Feuer", "eis": "Eis", "blitz": "Blitz", "wasser": "Wasser",
        "erde": "Erde", "wind": "Wind", "licht": "Licht", "dunkelheit": "Dunkelheit",
        "explosion": "EXPLOSION!!!"
    }
    try:
        schools = []
        for school in all_schools:
            progress = get_or_create_school_progress(db, player_id, school)
            schools.append({
                "id": school,
                "name": school_names.get(school, school.title()),
                "level": progress.level,
                "xp": progress.xp,
                "can_weave": progress.can_weave
            })
        return {"schools": schools}
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
