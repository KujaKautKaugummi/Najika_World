"""
Farming & Fishing System API
Endpoints for crop farming and fishing mechanics
"""

from fastapi import APIRouter, Depends, HTTPException
from backend.utils import handle_errors
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from backend.database import get_db
from backend.models.housing import FarmPlot, FishingSpot
from backend.models.user import User

router = APIRouter(prefix="/api/farming", tags=["Farming"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class PlantCropRequest(BaseModel):
    """Request to plant a crop"""
    player_id: int
    plot_index: int
    crop_type: str


class HarvestCropRequest(BaseModel):
    """Request to harvest a crop"""
    player_id: int
    plot_id: int


class FarmPlotResponse(BaseModel):
    """Farm plot information"""
    id: int
    owner_id: int
    plot_index: int
    crop_type: Optional[str] = None
    growth_stage: int
    ready_to_harvest: bool
    planted_at: Optional[str] = None
    watered_at: Optional[str] = None

    class Config:
        from_attributes = True


class FishingCastRequest(BaseModel):
    """Request to cast fishing line"""
    player_id: int
    fishing_spot_id: int


# ============================================================================
# FARM PLOT ENDPOINTS
# ============================================================================

@router.get("/plots/{player_id}", response_model=List[FarmPlotResponse])
@handle_errors()
async def get_player_farm_plots(player_id: int, db: Session = Depends(get_db)):
    """
    Get all farm plots for a player

    Returns list of farm plots with crop status
    """
    # Check if player exists
    player = db.query(User).filter(User.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get or create farm plots (4 plots per player)
    plots = db.query(FarmPlot).filter(FarmPlot.owner_id == player_id).all()

    if not plots:
        # Create 4 default farm plots
        for i in range(4):
            plot = FarmPlot(
                owner_id=player_id,
                plot_index=i,
                crop_type=None,
                growth_stage=0,
                ready_to_harvest=False
            )
            db.add(plot)

        db.commit()
        plots = db.query(FarmPlot).filter(FarmPlot.owner_id == player_id).all()

    return [
        FarmPlotResponse(
            id=plot.id,
            owner_id=plot.owner_id,
            plot_index=plot.plot_index,
            crop_type=plot.crop_type,
            growth_stage=plot.growth_stage,
            ready_to_harvest=plot.ready_to_harvest,
            planted_at=plot.planted_at.isoformat() if plot.planted_at else None,
            watered_at=plot.watered_at.isoformat() if plot.watered_at else None
        )
        for plot in plots
    ]


@router.post("/plant")
@handle_errors()
async def plant_crop(request: PlantCropRequest, db: Session = Depends(get_db)):
    """
    Plant a crop in a farm plot

    Starts crop growth cycle
    """
    # Get plot
    plot = db.query(FarmPlot).filter(
        FarmPlot.owner_id == request.player_id,
        FarmPlot.plot_index == request.plot_index
    ).first()

    if not plot:
        raise HTTPException(status_code=404, detail="Farm plot not found")

    # Check if plot is empty
    if plot.crop_type is not None:
        raise HTTPException(status_code=400, detail="Plot already has a crop")

    # Validate crop type
    valid_crops = ["wheat", "corn", "tomato", "potato", "carrot", "lettuce", "pumpkin", "strawberry"]
    if request.crop_type not in valid_crops:
        raise HTTPException(status_code=400, detail=f"Invalid crop type. Valid: {valid_crops}")

    # Plant crop
    plot.crop_type = request.crop_type
    plot.growth_stage = 0
    plot.ready_to_harvest = False
    plot.planted_at = datetime.utcnow()

    db.commit()
    db.refresh(plot)

    return {
        "success": True,
        "message": f"Planted {request.crop_type}",
        "plot_id": plot.id,
        "crop_type": plot.crop_type,
        "growth_stage": plot.growth_stage
    }


@router.post("/water/{plot_id}")
@handle_errors()
async def water_crop(plot_id: int, db: Session = Depends(get_db)):
    """
    Water a crop to increase growth

    Advances growth stage by 1 (max 4)
    """
    plot = db.query(FarmPlot).filter(FarmPlot.id == plot_id).first()

    if not plot:
        raise HTTPException(status_code=404, detail="Farm plot not found")

    if plot.crop_type is None:
        raise HTTPException(status_code=400, detail="No crop planted")

    if plot.ready_to_harvest:
        raise HTTPException(status_code=400, detail="Crop already ready to harvest")

    # Water crop
    plot.growth_stage = min(plot.growth_stage + 1, 4)
    plot.watered_at = datetime.utcnow()

    # Check if ready to harvest (stage 4)
    if plot.growth_stage >= 4:
        plot.ready_to_harvest = True

    db.commit()
    db.refresh(plot)

    return {
        "success": True,
        "message": f"Watered {plot.crop_type}",
        "growth_stage": plot.growth_stage,
        "ready_to_harvest": plot.ready_to_harvest
    }


@router.post("/harvest")
@handle_errors()
async def harvest_crop(request: HarvestCropRequest, db: Session = Depends(get_db)):
    """
    Harvest a fully grown crop

    Resets plot and returns crop rewards
    """
    plot = db.query(FarmPlot).filter(FarmPlot.id == request.plot_id).first()

    if not plot:
        raise HTTPException(status_code=404, detail="Farm plot not found")

    if plot.owner_id != request.player_id:
        raise HTTPException(status_code=403, detail="Not your farm plot")

    if not plot.ready_to_harvest:
        raise HTTPException(status_code=400, detail="Crop not ready to harvest")

    # Harvest rewards
    crop_yields = {
        "wheat": {"quantity": 5, "gold": 20},
        "corn": {"quantity": 4, "gold": 30},
        "tomato": {"quantity": 6, "gold": 25},
        "potato": {"quantity": 8, "gold": 15},
        "carrot": {"quantity": 7, "gold": 18},
        "lettuce": {"quantity": 5, "gold": 22},
        "pumpkin": {"quantity": 2, "gold": 50},
        "strawberry": {"quantity": 10, "gold": 35},
    }

    harvested_crop = plot.crop_type
    rewards = crop_yields.get(harvested_crop, {"quantity": 1, "gold": 10})

    # Reset plot
    plot.crop_type = None
    plot.growth_stage = 0
    plot.ready_to_harvest = False
    plot.planted_at = None
    plot.watered_at = None

    db.commit()

    return {
        "success": True,
        "message": f"Harvested {harvested_crop}!",
        "crop": harvested_crop,
        "quantity": rewards["quantity"],
        "gold_earned": rewards["gold"]
    }


# ============================================================================
# FISHING ENDPOINTS
# ============================================================================

@router.get("/fishing/spots")
@handle_errors()
async def get_fishing_spots(db: Session = Depends(get_db)):
    """
    Get all fishing spots in the world

    Returns list of fishing locations
    """
    spots = db.query(FishingSpot).all()

    if not spots:
        # Create default fishing spots
        default_spots = [
            {"location_name": "Peaceful Lake", "region_id": 1, "fish_pool": ["bass", "trout", "carp"]},
            {"location_name": "Mountain Stream", "region_id": 2, "fish_pool": ["salmon", "pike"]},
            {"location_name": "Ocean Pier", "region_id": 3, "fish_pool": ["tuna", "swordfish", "mackerel"]},
            {"location_name": "Desert Oasis", "region_id": 4, "fish_pool": ["catfish", "tilapia"]},
        ]

        for spot_data in default_spots:
            spot = FishingSpot(**spot_data)
            db.add(spot)

        db.commit()
        spots = db.query(FishingSpot).all()

    return {
        "fishing_spots": [
            {
                "id": spot.id,
                "location_name": spot.location_name,
                "region_id": spot.region_id,
                "fish_pool": spot.fish_pool,
                "rare_fish_chance": spot.rare_fish_chance
            }
            for spot in spots
        ]
    }


@router.post("/fishing/cast")
@handle_errors()
async def cast_fishing_line(request: FishingCastRequest, db: Session = Depends(get_db)):
    """
    Cast fishing line and attempt to catch a fish

    Returns random fish based on location
    """
    spot = db.query(FishingSpot).filter(FishingSpot.id == request.fishing_spot_id).first()

    if not spot:
        raise HTTPException(status_code=404, detail="Fishing spot not found")

    # Simulate fishing
    import random

    fish_pool = spot.fish_pool or ["fish"]
    caught_fish = random.choice(fish_pool)

    # Rare fish chance
    is_rare = random.random() < spot.rare_fish_chance
    if is_rare:
        caught_fish = f"Rare {caught_fish.title()}"

    # Size and quality
    size = random.choice(["Small", "Medium", "Large", "Huge"])
    quality = random.choice(["Common", "Uncommon", "Rare", "Legendary"])

    # Calculate gold value
    base_value = 10
    size_multiplier = {"Small": 1.0, "Medium": 1.5, "Large": 2.0, "Huge": 3.0}
    quality_multiplier = {"Common": 1.0, "Uncommon": 1.5, "Rare": 2.5, "Legendary": 5.0}

    gold_value = int(base_value * size_multiplier[size] * quality_multiplier[quality])

    if is_rare:
        gold_value *= 2

    return {
        "success": True,
        "message": f"Caught a {size} {caught_fish}!",
        "fish": caught_fish,
        "size": size,
        "quality": quality,
        "is_rare": is_rare,
        "gold_value": gold_value,
        "location": spot.location_name
    }


@router.get("/crops/catalog")
@handle_errors()
async def get_crop_catalog():
    """
    Get catalog of available crops

    Returns list of crops that can be planted
    """
    crops = [
        {"type": "wheat", "name": "Wheat", "growth_time_hours": 2, "sell_price": 20},
        {"type": "corn", "name": "Corn", "growth_time_hours": 3, "sell_price": 30},
        {"type": "tomato", "name": "Tomato", "growth_time_hours": 2.5, "sell_price": 25},
        {"type": "potato", "name": "Potato", "growth_time_hours": 1.5, "sell_price": 15},
        {"type": "carrot", "name": "Carrot", "growth_time_hours": 2, "sell_price": 18},
        {"type": "lettuce", "name": "Lettuce", "growth_time_hours": 1, "sell_price": 22},
        {"type": "pumpkin", "name": "Pumpkin", "growth_time_hours": 6, "sell_price": 50},
        {"type": "strawberry", "name": "Strawberry", "growth_time_hours": 4, "sell_price": 35},
    ]

    return {
        "crops": crops,
        "total_crops": len(crops)
    }
