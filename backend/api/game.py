"""
Game API Router
Handles game systems: combat, inventory, farming, fishing, quests, skills
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import random
import json
import os

from backend.database import get_db
from backend.models.user import User
from backend.models.character import Character
from backend.models.inventory import InventoryItem, Equipment
from backend.api.auth import get_current_user
from backend.config import get_save_path

router = APIRouter(prefix="/game", tags=["Game"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CharacterCreateRequest(BaseModel):
    name: str
    species: str = "Jellysquish"
    nickname: Optional[str] = None


class CharacterResponse(BaseModel):
    id: int
    name: str
    species: str
    level: int
    stats: Dict[str, float]
    status: Dict[str, float]
    position: Dict[str, float]


class CombatActionRequest(BaseModel):
    action: str  # "attack", "dodge", "block", "parry", "skill"
    enemy_id: Optional[str] = None
    skill_id: Optional[str] = None


class CombatResult(BaseModel):
    success: bool
    damage: int
    player_health: float
    enemy_health: float
    message: str
    loot: Optional[List[Dict]] = None
    xp_gained: int = 0


class InventoryActionRequest(BaseModel):
    action: str  # "add", "remove", "use", "equip", "unequip"
    item_id: str
    quantity: int = 1


class FoodConsumeRequest(BaseModel):
    item_id: str


class QuestStartRequest(BaseModel):
    quest_id: str


class SkillUseRequest(BaseModel):
    skill_id: str
    target_id: Optional[str] = None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_user_character(user: User, db: Session) -> Character:
    """Get user's primary character"""
    character = db.query(Character).filter(Character.user_id == user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No character found. Create a character first."
        )
    return character


def calculate_damage(attacker_attack: float, defender_defense: float) -> int:
    """Calculate combat damage"""
    base_damage = max(1, int(attacker_attack - (defender_defense * 0.5)))
    variance = random.uniform(0.8, 1.2)
    return int(base_damage * variance)


# ============================================================================
# CHARACTER ENDPOINTS
# ============================================================================

@router.post("/character/create", response_model=CharacterResponse)
def create_character(
    request: CharacterCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new character for the user"""

    # Check if user already has a character
    existing = db.query(Character).filter(Character.user_id == current_user.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a character"
        )

    # Create new character
    character = Character(
        user_id=current_user.id,
        name=request.name,
        species=request.species,
        nickname=request.nickname,
    )

    db.add(character)
    db.commit()
    db.refresh(character)

    # Create equipment for character
    equipment = Equipment(character_id=character.id)
    db.add(equipment)
    db.commit()

    return CharacterResponse(
        id=character.id,
        name=character.name,
        species=character.species,
        level=character.level,
        stats=character.to_dict()["stats"],
        status=character.to_dict()["status"],
        position=character.to_dict()["position"],
    )


@router.get("/character", response_model=CharacterResponse)
def get_character(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's character"""
    character = get_user_character(current_user, db)

    return CharacterResponse(
        id=character.id,
        name=character.name,
        species=character.species,
        level=character.level,
        stats=character.to_dict()["stats"],
        status=character.to_dict()["status"],
        position=character.to_dict()["position"],
    )


@router.post("/character/update")
def update_character(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update character stats/position"""
    character = get_user_character(current_user, db)

    # Update allowed fields
    if "position_x" in data:
        character.position_x = data["position_x"]
    if "position_y" in data:
        character.position_y = data["position_y"]
    if "position_z" in data:
        character.position_z = data["position_z"]
    if "health" in data:
        character.health = min(data["health"], character.max_health)
    if "hunger" in data:
        character.hunger = max(0, min(100, data["hunger"]))
    if "happiness" in data:
        character.happiness = max(0, min(100, data["happiness"]))

    db.commit()

    return {"success": True, "message": "Character updated"}


# ============================================================================
# COMBAT ENDPOINTS
# ============================================================================

@router.post("/combat/action", response_model=CombatResult)
def combat_action(
    request: CombatActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a combat action"""
    character = get_user_character(current_user, db)

    # Simplified combat (integrate with najika_battle.py later)
    enemy_health = 50.0
    damage = calculate_damage(character.attack, 10.0)

    enemy_health -= damage
    player_damage = 0

    if random.random() < 0.5:  # Enemy counter-attack
        player_damage = calculate_damage(10.0, character.defense)
        character.health -= player_damage
        db.commit()

    # Check victory
    loot = None
    xp_gained = 0
    if enemy_health <= 0:
        xp_gained = 20
        character.xp += xp_gained
        loot = [{"item": "health_potion_small", "quantity": 1}]
        db.commit()

    return CombatResult(
        success=True,
        damage=damage,
        player_health=character.health,
        enemy_health=max(0, enemy_health),
        message=f"Dealt {damage} damage! Took {player_damage} damage.",
        loot=loot,
        xp_gained=xp_gained,
    )


@router.get("/combat/history")
def get_combat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get combat history (placeholder)"""
    return {"history": []}


# ============================================================================
# INVENTORY ENDPOINTS
# ============================================================================

@router.get("/inventory")
def get_inventory(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get character's inventory"""
    character = get_user_character(current_user, db)
    items = db.query(InventoryItem).filter(InventoryItem.character_id == character.id).all()

    return {"items": [item.to_dict() for item in items]}


@router.post("/inventory/action")
def inventory_action(
    request: InventoryActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform inventory action (add, remove, use, equip)"""
    character = get_user_character(current_user, db)

    if request.action == "add":
        # Add item to inventory
        existing_item = db.query(InventoryItem).filter(
            InventoryItem.character_id == character.id,
            InventoryItem.item_id == request.item_id,
            InventoryItem.is_stackable == True
        ).first()

        if existing_item:
            existing_item.quantity += request.quantity
        else:
            new_item = InventoryItem(
                character_id=character.id,
                item_id=request.item_id,
                name=request.item_id.replace("_", " ").title(),
                item_type="misc",
                quantity=request.quantity,
            )
            db.add(new_item)

        db.commit()
        return {"success": True, "message": f"Added {request.quantity}x {request.item_id}"}

    elif request.action == "remove":
        # Remove item
        item = db.query(InventoryItem).filter(
            InventoryItem.character_id == character.id,
            InventoryItem.item_id == request.item_id
        ).first()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if item.quantity > request.quantity:
            item.quantity -= request.quantity
        else:
            db.delete(item)

        db.commit()
        return {"success": True, "message": f"Removed {request.quantity}x {request.item_id}"}

    return {"success": False, "message": "Unknown action"}


@router.get("/inventory/equipment")
def get_equipment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get character's equipment"""
    character = get_user_character(current_user, db)
    equipment = db.query(Equipment).filter(Equipment.character_id == character.id).first()

    if not equipment:
        return {"equipment": {}}

    return {"equipment": equipment.to_dict()}


# ============================================================================
# FOOD/FARMING ENDPOINTS
# ============================================================================

@router.post("/food/consume")
def consume_food(
    request: FoodConsumeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Consume food item"""
    character = get_user_character(current_user, db)

    # Find food item in inventory
    food_item = db.query(InventoryItem).filter(
        InventoryItem.character_id == character.id,
        InventoryItem.item_id == request.item_id,
        InventoryItem.item_type == "food"
    ).first()

    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    # Apply food effects
    hunger_restored = 20
    health_restored = 10

    character.hunger = min(100, character.hunger + hunger_restored)
    character.health = min(character.max_health, character.health + health_restored)

    # Remove one food item
    if food_item.quantity > 1:
        food_item.quantity -= 1
    else:
        db.delete(food_item)

    db.commit()

    return {
        "success": True,
        "message": f"Consumed {food_item.name}",
        "hunger_restored": hunger_restored,
        "health_restored": health_restored,
    }


# ============================================================================
# QUEST ENDPOINTS
# ============================================================================

@router.get("/quests")
def get_quests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get available and active quests (placeholder)"""
    return {"active": [], "available": [], "completed": []}


@router.post("/quests/start")
def start_quest(
    request: QuestStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a quest (placeholder)"""
    return {"success": True, "quest_id": request.quest_id}


# ============================================================================
# SKILL ENDPOINTS
# ============================================================================

@router.get("/skills")
def get_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get character's skills"""
    character = get_user_character(current_user, db)
    return {"skills": character.skills}


@router.post("/skills/use")
def use_skill(
    request: SkillUseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Use a skill (placeholder)"""
    character = get_user_character(current_user, db)

    if request.skill_id not in character.skills:
        raise HTTPException(status_code=404, detail="Skill not learned")

    return {"success": True, "message": f"Used skill {request.skill_id}"}


# ============================================================================
# SAVE/LOAD ENDPOINTS
# ============================================================================

@router.post("/save")
def save_game(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save game state to file"""
    character = get_user_character(current_user, db)

    save_data = {
        "user_id": current_user.id,
        "character": character.to_dict(),
        "saved_at": datetime.utcnow().isoformat(),
    }

    save_file = get_save_path(f"save_{current_user.id}.json")
    os.makedirs(os.path.dirname(save_file), exist_ok=True)

    with open(save_file, "w") as f:
        json.dump(save_data, f, indent=2)

    return {"success": True, "message": "Game saved successfully"}


@router.post("/load")
def load_game(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Load game state from file (placeholder)"""
    save_file = get_save_path(f"save_{current_user.id}.json")

    if not os.path.exists(save_file):
        raise HTTPException(status_code=404, detail="No save file found")

    with open(save_file, "r") as f:
        save_data = json.load(f)

    return {"success": True, "data": save_data}
