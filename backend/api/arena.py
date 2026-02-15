"""
Arena API Router
Handles Nemesis Arena System and Mortal Kombat-style Finishers
"""

from fastapi import APIRouter, Depends, HTTPException, status
from backend.utils import handle_errors
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.database import get_db
from backend.models.user import User
from backend.api.auth import get_current_user
from backend.services.nemesis_arena_system import nemesis_arena, RulerRank, MonsterType
from backend.services.finisher_system import finisher_generator, FinisherStyle

router = APIRouter(prefix="/game/arena", tags=["Arena"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ChallengeRequest(BaseModel):
    monster_id: int


class BattleActionRequest(BaseModel):
    monster_id: int
    action: str
    damage: int
    events: List[str] = []


class CreateFinisherRequest(BaseModel):
    """Request to create Mortal Kombat style finisher"""
    category: str  # "Ehrenvoller Tod", "Lustiger Tod", "Grausamer Tod", "Tod Tod Blut Blut", "Sinnloser Tod"
    ingredients: List[str]  # Player keywords/stichwörter
    defeated_monster_id: int


class MonsterCreateRequest(BaseModel):
    monster_type: str
    rank: str = "NOBODY"
    region: Optional[str] = None
    level: int = 1


# ============================================================================
# ARENA ENDPOINTS
# ============================================================================

@router.get("/hierarchy")
@handle_errors()
async def get_arena_hierarchy(
    current_user: User = Depends(get_current_user)
):
    """
    Get complete arena hierarchy

    Returns all monsters organized by rank (Shadow of Mordor style)
    """
    hierarchy = nemesis_arena.get_arena_hierarchy()

    return {
        "success": True,
        "hierarchy": hierarchy,
        "total_monsters": len(nemesis_arena.monsters)
    }


@router.get("/challengers")
@handle_errors()
async def get_available_challengers(
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Get available monsters to challenge"""
    # Get monsters that can be challenged
    challengers = []

    for monster in nemesis_arena.monsters.values():
        if monster.current_health > 0:
            challengers.append(monster.to_dict())

    # Sort by rank and level
    challengers.sort(key=lambda m: (m['rank'], m['level']), reverse=True)

    return {
        "success": True,
        "challengers": challengers[:limit]
    }


@router.get("/my-nemesis")
@handle_errors()
async def get_my_nemesis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get monsters that have grudges against the player

    Returns monsters that remember the player and want revenge
    """
    my_nemesis = []

    for monster in nemesis_arena.monsters.values():
        # Check if monster has memories of this user
        if str(current_user.id) in monster.memories or len(monster.grudges) > 0:
            my_nemesis.append(monster.to_dict())

    # Sort by encounters
    my_nemesis.sort(key=lambda m: m['encounters_with_player'], reverse=True)

    return {
        "success": True,
        "nemesis": my_nemesis
    }


@router.get("/regions")
@handle_errors()
async def get_arena_regions(
    current_user: User = Depends(get_current_user)
):
    """Get all arena regions and their controllers"""
    regions = {}

    for monster in nemesis_arena.monsters.values():
        if monster.region_controlled:
            regions[monster.region_controlled] = monster.to_dict()

    return {
        "success": True,
        "regions": regions
    }


@router.get("/monster/{monster_id}")
@handle_errors()
async def get_monster_details(
    monster_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get detailed information about a specific monster"""
    monster = nemesis_arena.monsters.get(monster_id)

    if not monster:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monster not found"
        )

    return {
        "success": True,
        "monster": monster.to_dict()
    }


@router.post("/challenge")
@handle_errors()
async def challenge_monster(
    request: ChallengeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Challenge a monster to battle

    Shows dramatic intro speech (Shadow of Mordor style)
    """
    monster = nemesis_arena.monsters.get(request.monster_id)

    if not monster:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monster not found"
        )

    # Generate intro speech
    intro_speech = nemesis_arena.get_monster_intro_speech(
        request.monster_id,
        current_user.username
    )

    return {
        "success": True,
        "monster": monster.to_dict(),
        "intro_speech": intro_speech,
        "message": f"Kampf gegen {monster.name} beginnt!"
    }


@router.post("/battle")
@handle_errors()
async def execute_battle_action(
    request: BattleActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Execute a battle action against a monster

    This updates the monster's health and tracks the battle
    """
    result = nemesis_arena.battle(
        monster_id=request.monster_id,
        player_id=current_user.id,
        player_name=current_user.username,
        player_damage=request.damage,
        battle_events=request.events
    )

    return result


@router.post("/promote/{monster_id}")
@handle_errors()
async def promote_monster(
    monster_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Promote a monster to the next rank

    Admin/debug endpoint
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only"
        )

    result = nemesis_arena.promote_monster(monster_id)
    return result


@router.post("/monster/create")
@handle_errors()
async def create_monster(
    request: MonsterCreateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new monster in the arena

    Admin/debug endpoint
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only"
        )

    try:
        # Convert string enums
        monster_type = MonsterType[request.monster_type.upper()]
        rank = RulerRank[request.rank.upper()]

        monster = nemesis_arena.create_monster(
            monster_type=monster_type,
            rank=rank,
            region=request.region,
            level=request.level
        )

        return {
            "success": True,
            "monster": monster.to_dict(),
            "message": f"Monster {monster.name} erstellt!"
        }
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid enum value: {e}"
        )


# ============================================================================
# MORTAL KOMBAT STYLE FINISHER ENDPOINTS
# ============================================================================

@router.post("/finisher/create")
@handle_errors()
async def create_finisher(
    request: CreateFinisherRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a custom Mortal Kombat-style finisher

    This is triggered AFTER defeating an arena monster.
    Player CHOOSES brutality category, then provides keywords/ingredients.

    ## Brutality Categories:
    1. **Ehrenvoller Tod** - Clean, respectful finish
    2. **Lustiger Tod** - Comical, absurd finish
    3. **Grausamer Tod** - Dark, sadistic finish
    4. **Tod Tod Blut Blut** - EXTREME brutality
    5. **Sinnloser Tod** - Anti-climactic, meaningless

    Different from FinisherQTE (button mashing during combat).
    This is the "FINISH HIM!" moment.
    """
    # Parse category
    from backend.services.finisher_system import BrutalityCategory

    try:
        # Map string to enum
        category_map = {
            "Ehrenvoller Tod": BrutalityCategory.HONORABLE_DEATH,
            "Lustiger Tod": BrutalityCategory.FUNNY_DEATH,
            "Grausamer Tod": BrutalityCategory.CRUEL_DEATH,
            "Tod Tod Blut Blut": BrutalityCategory.BLOOD_BATH,
            "Sinnloser Tod": BrutalityCategory.POINTLESS_DEATH
        }

        category = category_map.get(request.category)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid category. Choose from: {list(category_map.keys())}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category: {e}"
        )

    # Get character level for power calculation
    from backend.models.character import Character
    character = db.query(Character).filter(Character.user_id == current_user.id).first()
    level = character.level if character else 1

    # Create finisher with category
    finisher = finisher_generator.create_custom_finisher(
        category=category,
        ingredients=request.ingredients,
        character_level=level,
        user_id=current_user.id
    )

    # Get defeated monster info
    monster = nemesis_arena.monsters.get(request.defeated_monster_id)
    monster_name = monster.name if monster else "Enemy"

    return {
        "success": True,
        "finisher": finisher.to_dict(),
        "message": f"🔥 FINISH HIM! {finisher.name} gegen {monster_name}!",
        "animation_ready": True,
        "category_selected": category.value
    }


@router.get("/finisher/categories")
@handle_errors()
async def get_brutality_categories(
    current_user: User = Depends(get_current_user)
):
    """
    Get available brutality categories for finisher creation

    Player must choose a category FIRST, then provide keywords
    """
    from backend.services.finisher_system import BrutalityCategory

    categories = [
        {
            "id": "HONORABLE_DEATH",
            "name": "Ehrenvoller Tod",
            "description": "Sauberer, respektvoller Finish",
            "brutality": 3,
            "humor": 2,
            "icon": "⚔️"
        },
        {
            "id": "FUNNY_DEATH",
            "name": "Lustiger Tod",
            "description": "Komisch, absurd, witzig",
            "brutality": 5,
            "humor": 10,
            "icon": "🎭"
        },
        {
            "id": "CRUEL_DEATH",
            "name": "Grausamer Tod",
            "description": "Dunkel, sadistisch, brutal",
            "brutality": 8,
            "humor": 1,
            "icon": "☠️"
        },
        {
            "id": "BLOOD_BATH",
            "name": "Tod Tod Blut Blut",
            "description": "EXTREME BRUTALITÄT! BLUT ÜBERALL!",
            "brutality": 10,
            "humor": 0,
            "icon": "💀💀💀"
        },
        {
            "id": "POINTLESS_DEATH",
            "name": "Sinnloser Tod",
            "description": "Anti-klimatisch, bedeutungslos, absurd",
            "brutality": 4,
            "humor": 7,
            "icon": "🤷"
        }
    ]

    return {
        "success": True,
        "categories": categories,
        "instruction": "Wähle zuerst eine Kategorie, dann gib Stichwörter ein!"
    }


@router.get("/finisher/random-ingredients")
@handle_errors()
async def get_random_finisher_ingredients(
    current_user: User = Depends(get_current_user)
):
    """Get random ingredient suggestions for finisher creation"""
    ingredients = finisher_generator.get_random_finisher_ingredients()

    return {
        "success": True,
        "ingredients": ingredients,
        "tip": "Kombiniere diese Zutaten für einen einzigartigen Finisher!"
    }


@router.get("/finisher/history")
@handle_errors()
async def get_finisher_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Get recent finishers created by players"""
    finishers = finisher_generator.list_all_finishers(limit=limit)

    return {
        "success": True,
        "finishers": [f.to_dict() for f in finishers],
        "total": len(finisher_generator.finisher_database)
    }


@router.get("/finisher/{finisher_id}")
@handle_errors()
async def get_finisher_details(
    finisher_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get detailed animation data for a finisher"""
    finisher = finisher_generator.get_finisher_by_id(finisher_id)

    if not finisher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finisher not found"
        )

    return {
        "success": True,
        "finisher": finisher.to_dict(),
        "can_replay": True
    }


# ============================================================================
# STATS AND LEADERBOARDS
# ============================================================================

@router.get("/stats")
@handle_errors()
async def get_arena_stats(
    current_user: User = Depends(get_current_user)
):
    """Get arena statistics"""
    total_monsters = len(nemesis_arena.monsters)

    rank_distribution = {}
    for monster in nemesis_arena.monsters.values():
        rank_name = monster.rank.value
        rank_distribution[rank_name] = rank_distribution.get(rank_name, 0) + 1

    return {
        "success": True,
        "stats": {
            "total_monsters": total_monsters,
            "arena_king_id": nemesis_arena.arena_king_id,
            "rank_distribution": rank_distribution,
            "total_finishers_created": len(finisher_generator.finisher_database),
            "regions_controlled": len(nemesis_arena.region_lords)
        }
    }
