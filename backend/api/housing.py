"""
Housing System API
Endpoints for player houses, furniture placement, and decorations
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.database import get_db
from backend.models.housing import PlayerHouse
from backend.models.user import User

router = APIRouter(prefix="/api/housing", tags=["Housing"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class FurnitureItem(BaseModel):
    """Single furniture item"""
    type: str
    position: dict  # {x, y, z}
    rotation: float
    scale: Optional[float] = 1.0


class PlaceFurnitureRequest(BaseModel):
    """Request to place furniture"""
    player_id: int
    furniture: FurnitureItem


class RemoveFurnitureRequest(BaseModel):
    """Request to remove furniture"""
    player_id: int
    furniture_index: int


class UpgradeHouseRequest(BaseModel):
    """Request to upgrade house"""
    player_id: int


class HouseResponse(BaseModel):
    """House information response"""
    id: int
    player_id: int
    furniture: List[dict]
    decorations: List[dict]
    level: int
    max_furniture: int
    upgraded_at: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/house/{player_id}", response_model=HouseResponse)
async def get_player_house(player_id: int, db: Session = Depends(get_db)):
    """
    Get player's house information

    Returns house data including furniture layout and decorations
    """
    # Check if player exists
    player = db.query(User).filter(User.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get or create house
    house = db.query(PlayerHouse).filter(PlayerHouse.owner_id == player_id).first()

    if not house:
        # Create default house
        house = PlayerHouse(
            owner_id=player_id,
            furniture=[],
            decorations=[],
            level=1,
            max_furniture=20
        )
        db.add(house)
        db.commit()
        db.refresh(house)

    return HouseResponse(
        id=house.id,
        player_id=house.owner_id,
        furniture=house.furniture or [],
        decorations=house.decorations or [],
        level=house.level,
        max_furniture=house.max_furniture,
        upgraded_at=house.upgraded_at.isoformat() if house.upgraded_at else None
    )


@router.post("/furniture/place")
async def place_furniture(request: PlaceFurnitureRequest, db: Session = Depends(get_db)):
    """
    Place furniture in player's house

    Adds a new furniture item to the house layout
    """
    house = db.query(PlayerHouse).filter(PlayerHouse.owner_id == request.player_id).first()

    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    # Check furniture limit
    current_furniture = house.furniture or []
    if len(current_furniture) >= house.max_furniture:
        raise HTTPException(
            status_code=400,
            detail=f"Furniture limit reached ({house.max_furniture})"
        )

    # Add furniture
    furniture_data = {
        "type": request.furniture.type,
        "position": request.furniture.position,
        "rotation": request.furniture.rotation,
        "scale": request.furniture.scale
    }

    current_furniture.append(furniture_data)
    house.furniture = current_furniture

    db.commit()
    db.refresh(house)

    return {
        "success": True,
        "message": f"Placed {request.furniture.type}",
        "furniture_count": len(house.furniture)
    }


@router.post("/furniture/remove")
async def remove_furniture(request: RemoveFurnitureRequest, db: Session = Depends(get_db)):
    """
    Remove furniture from player's house

    Removes furniture item at specified index
    """
    house = db.query(PlayerHouse).filter(PlayerHouse.owner_id == request.player_id).first()

    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    current_furniture = house.furniture or []

    if request.furniture_index < 0 or request.furniture_index >= len(current_furniture):
        raise HTTPException(status_code=400, detail="Invalid furniture index")

    # Remove furniture
    removed_item = current_furniture.pop(request.furniture_index)
    house.furniture = current_furniture

    db.commit()

    return {
        "success": True,
        "message": f"Removed {removed_item.get('type', 'furniture')}",
        "furniture_count": len(house.furniture)
    }


@router.put("/upgrade")
async def upgrade_house(request: UpgradeHouseRequest, db: Session = Depends(get_db)):
    """
    Upgrade player's house level

    Increases house level and max furniture capacity
    """
    house = db.query(PlayerHouse).filter(PlayerHouse.owner_id == request.player_id).first()

    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    # Check max level (10)
    if house.level >= 10:
        raise HTTPException(status_code=400, detail="House already at max level")

    # Upgrade
    house.level += 1
    house.max_furniture = 20 + (house.level * 5)  # 25, 30, 35, ..., 70

    from datetime import datetime
    house.upgraded_at = datetime.utcnow()

    db.commit()
    db.refresh(house)

    return {
        "success": True,
        "message": f"House upgraded to level {house.level}",
        "level": house.level,
        "max_furniture": house.max_furniture
    }


@router.get("/furniture/catalog")
async def get_furniture_catalog():
    """
    Get catalog of available furniture types

    Returns list of furniture that can be placed in houses
    """
    catalog = [
        {"type": "bed", "name": "Bed", "category": "bedroom", "cost": 100},
        {"type": "table", "name": "Table", "category": "dining", "cost": 50},
        {"type": "chair", "name": "Chair", "category": "dining", "cost": 25},
        {"type": "sofa", "name": "Sofa", "category": "living", "cost": 200},
        {"type": "bookshelf", "name": "Bookshelf", "category": "study", "cost": 150},
        {"type": "desk", "name": "Desk", "category": "study", "cost": 100},
        {"type": "wardrobe", "name": "Wardrobe", "category": "bedroom", "cost": 180},
        {"type": "lamp", "name": "Lamp", "category": "lighting", "cost": 40},
        {"type": "rug", "name": "Rug", "category": "decoration", "cost": 60},
        {"type": "plant", "name": "Potted Plant", "category": "decoration", "cost": 30},
        {"type": "painting", "name": "Painting", "category": "decoration", "cost": 120},
        {"type": "tv", "name": "Television", "category": "entertainment", "cost": 300},
        {"type": "fireplace", "name": "Fireplace", "category": "living", "cost": 500},
        {"type": "kitchen_counter", "name": "Kitchen Counter", "category": "kitchen", "cost": 250},
        {"type": "refrigerator", "name": "Refrigerator", "category": "kitchen", "cost": 400},
    ]

    return {
        "catalog": catalog,
        "total_items": len(catalog)
    }
