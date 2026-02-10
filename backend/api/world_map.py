"""
World Map API
9600x9600 Grid World with 8 Regions
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models.world_map import (
    Region, FastTravelPoint, PlayerPosition,
    RegionBoundary, WorldWeather, DayNightCycle,
    PlayerTravelPointUnlock
)
from backend.models.user import User

router = APIRouter(prefix="/api/world-map", tags=["World Map"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class RegionResponse(BaseModel):
    """Region information"""
    id: int
    name: str
    region_code: str
    position_x: int
    position_y: int
    width: int
    height: int
    biome_type: str
    slime_color: str
    climate: str
    features: List[str]
    dangers: List[str]

    class Config:
        from_attributes = True


class FastTravelRequest(BaseModel):
    """Request to fast travel"""
    player_id: int
    travel_point_id: int


class UpdatePositionRequest(BaseModel):
    """Update player position"""
    player_id: int
    world_x: float
    world_y: float
    world_z: float = 0.0
    rotation_y: float = 0.0


class PlayerPositionResponse(BaseModel):
    """Player position response"""
    user_id: int
    region_id: Optional[int]
    region_name: Optional[str]
    world_x: float
    world_y: float
    world_z: float
    rotation_y: float
    is_in_house: bool
    is_in_dungeon: bool

    class Config:
        from_attributes = True


# ============================================================================
# WORLD MAP ENDPOINTS
# ============================================================================

@router.get("/map")
async def get_world_map(db: Session = Depends(get_db)):
    """
    Get complete 9600x9600 world map layout

    Returns all regions, boundaries, and center mountain
    """
    regions = db.query(Region).all()

    return {
        "world_size": {"width": 9600, "height": 9600},
        "center": {"x": 4800, "y": 4800},
        "center_mountain": {
            "name": "Götterfels",
            "position": {"x": 3300, "y": 3300},
            "size": {"width": 3000, "height": 3000},
            "peak": "Schwarze Mühle (12 Rooms)"
        },
        "regions": [
            {
                "id": r.id,
                "name": r.name,
                "region_code": r.region_code,
                "position": {
                    "x": r.position_x,
                    "y": r.position_y,
                    "width": r.width,
                    "height": r.height
                },
                "biome": r.biome_type,
                "slime_color": r.slime_color,
                "climate": r.climate,
                "features": r.features or [],
                "dangers": r.dangers or []
            }
            for r in regions
        ],
        "total_regions": len(regions)
    }


@router.get("/regions", response_model=List[RegionResponse])
async def get_all_regions(db: Session = Depends(get_db)):
    """
    Get all regions

    Returns list of all 8 regions with details
    """
    regions = db.query(Region).all()
    return regions


@router.get("/regions/{region_id}")
async def get_region_details(region_id: int, db: Session = Depends(get_db)):
    """
    Get detailed region information

    Includes fast travel points, weather, resources
    """
    region = db.query(Region).filter(Region.id == region_id).first()

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    # Get fast travel points
    travel_points = db.query(FastTravelPoint).filter(
        FastTravelPoint.region_id == region_id
    ).all()

    # Get current weather
    weather = db.query(WorldWeather).filter(
        WorldWeather.region_id == region_id
    ).order_by(WorldWeather.started_at.desc()).first()

    return {
        "region": {
            "id": region.id,
            "name": region.name,
            "region_code": region.region_code,
            "biome": region.biome_type,
            "slime_color": region.slime_color,
            "climate": region.climate,
            "position": {
                "x": region.position_x,
                "y": region.position_y,
                "width": region.width,
                "height": region.height
            },
            "features": region.features or [],
            "dangers": region.dangers or [],
            "resources": region.resources or {}
        },
        "fast_travel_points": [
            {
                "id": point.id,
                "name": point.name,
                "type": point.point_type,
                "position": {
                    "x": point.position_x,
                    "y": point.position_y,
                    "z": point.position_z
                },
                "is_locked": point.is_locked,
                "icon": point.icon,
                "description": point.description
            }
            for point in travel_points
        ],
        "weather": {
            "type": weather.weather_type if weather else "clear",
            "intensity": weather.intensity if weather else 0.5,
            "temperature": weather.temperature if weather else 20.0,
            "visibility": weather.visibility if weather else 1.0
        } if weather else None
    }


@router.get("/travel-points")
async def get_all_travel_points(player_id: int, db: Session = Depends(get_db)):
    """
    Get all fast travel points

    Shows locked/unlocked status for player
    """
    travel_points = db.query(FastTravelPoint).all()

    # Get player's unlocked travel points
    player_unlocks = db.query(PlayerTravelPointUnlock).filter(
        PlayerTravelPointUnlock.user_id == player_id
    ).all()

    # Create set of unlocked travel point IDs for quick lookup
    unlocked_ids = {unlock.travel_point_id for unlock in player_unlocks}

    return {
        "travel_points": [
            {
                "id": point.id,
                "name": point.name,
                "region_id": point.region_id,
                "type": point.point_type,
                "position": {
                    "x": point.position_x,
                    "y": point.position_y,
                    "z": point.position_z
                },
                "is_locked": point.is_locked and point.id not in unlocked_ids,
                "is_unlocked_by_player": point.id in unlocked_ids,
                "unlock_requirement": point.unlock_requirement,
                "icon": point.icon,
                "description": point.description
            }
            for point in travel_points
        ]
    }


@router.post("/travel")
async def fast_travel(request: FastTravelRequest, db: Session = Depends(get_db)):
    """
    Fast travel to a travel point

    Updates player position to travel point location
    """
    # Get travel point
    travel_point = db.query(FastTravelPoint).filter(
        FastTravelPoint.id == request.travel_point_id
    ).first()

    if not travel_point:
        raise HTTPException(status_code=404, detail="Travel point not found")

    # Check if player has unlocked this travel point
    player_unlock = db.query(PlayerTravelPointUnlock).filter(
        PlayerTravelPointUnlock.user_id == request.player_id,
        PlayerTravelPointUnlock.travel_point_id == request.travel_point_id
    ).first()

    # Check if locked (both globally and per-player)
    if travel_point.is_locked and not player_unlock:
        raise HTTPException(
            status_code=403,
            detail=f"Travel point locked: {travel_point.unlock_requirement}"
        )

    # Get or create player position
    player_pos = db.query(PlayerPosition).filter(
        PlayerPosition.user_id == request.player_id
    ).first()

    if not player_pos:
        player_pos = PlayerPosition(
            user_id=request.player_id,
            region_id=travel_point.region_id,
            world_x=travel_point.position_x,
            world_y=travel_point.position_y,
            world_z=travel_point.position_z,
            rotation_y=0.0
        )
        db.add(player_pos)
    else:
        player_pos.region_id = travel_point.region_id
        player_pos.world_x = travel_point.position_x
        player_pos.world_y = travel_point.position_y
        player_pos.world_z = travel_point.position_z
        player_pos.is_in_house = False
        player_pos.is_in_dungeon = False
        player_pos.last_moved_at = datetime.utcnow()

    db.commit()
    db.refresh(player_pos)

    # Get region
    region = db.query(Region).filter(Region.id == travel_point.region_id).first()

    return {
        "success": True,
        "message": f"Traveled to {travel_point.name}",
        "travel_point": {
            "name": travel_point.name,
            "type": travel_point.point_type
        },
        "region": {
            "id": region.id,
            "name": region.name,
            "biome": region.biome_type
        },
        "position": {
            "x": player_pos.world_x,
            "y": player_pos.world_y,
            "z": player_pos.world_z
        }
    }


# ============================================================================
# PLAYER POSITION ENDPOINTS
# ============================================================================

@router.get("/position/{player_id}", response_model=PlayerPositionResponse)
async def get_player_position(player_id: int, db: Session = Depends(get_db)):
    """
    Get player's current position in world
    """
    player_pos = db.query(PlayerPosition).filter(
        PlayerPosition.user_id == player_id
    ).first()

    if not player_pos:
        # Create default position (spawn at Schwarze Mühle)
        player_pos = PlayerPosition(
            user_id=player_id,
            region_id=None,  # Center mountain
            world_x=4800.0,  # Center
            world_y=4800.0,
            world_z=100.0,
            rotation_y=0.0,
            is_in_house=True,
            current_room="living_room"
        )
        db.add(player_pos)
        db.commit()
        db.refresh(player_pos)

    # Get region name
    region_name = None
    if player_pos.region_id:
        region = db.query(Region).filter(Region.id == player_pos.region_id).first()
        region_name = region.name if region else None

    return PlayerPositionResponse(
        user_id=player_pos.user_id,
        region_id=player_pos.region_id,
        region_name=region_name,
        world_x=player_pos.world_x,
        world_y=player_pos.world_y,
        world_z=player_pos.world_z,
        rotation_y=player_pos.rotation_y,
        is_in_house=player_pos.is_in_house,
        is_in_dungeon=player_pos.is_in_dungeon
    )


@router.post("/travel-points/{travel_point_id}/unlock")
async def unlock_travel_point(
    travel_point_id: int,
    player_id: int,
    unlock_method: str = "discovery",
    db: Session = Depends(get_db)
):
    """
    Unlock a travel point for a player

    Methods: "discovery", "quest", "purchase", "boss_defeat"
    """
    # Check if travel point exists
    travel_point = db.query(FastTravelPoint).filter(
        FastTravelPoint.id == travel_point_id
    ).first()

    if not travel_point:
        raise HTTPException(status_code=404, detail="Travel point not found")

    # Check if already unlocked
    existing_unlock = db.query(PlayerTravelPointUnlock).filter(
        PlayerTravelPointUnlock.user_id == player_id,
        PlayerTravelPointUnlock.travel_point_id == travel_point_id
    ).first()

    if existing_unlock:
        return {
            "success": False,
            "message": "Travel point already unlocked",
            "unlocked_at": existing_unlock.unlocked_at.isoformat()
        }

    # Create unlock
    unlock = PlayerTravelPointUnlock(
        user_id=player_id,
        travel_point_id=travel_point_id,
        unlock_method=unlock_method
    )

    db.add(unlock)
    db.commit()
    db.refresh(unlock)

    return {
        "success": True,
        "message": f"Travel point '{travel_point.name}' unlocked!",
        "travel_point": {
            "id": travel_point.id,
            "name": travel_point.name,
            "type": travel_point.point_type
        },
        "unlocked_at": unlock.unlocked_at.isoformat(),
        "unlock_method": unlock_method
    }


@router.post("/position/update")
async def update_player_position(
    request: UpdatePositionRequest,
    db: Session = Depends(get_db)
):
    """
    Update player position (for continuous movement)
    """
    player_pos = db.query(PlayerPosition).filter(
        PlayerPosition.user_id == request.player_id
    ).first()

    if not player_pos:
        raise HTTPException(status_code=404, detail="Player position not found")

    # Update position
    player_pos.world_x = request.world_x
    player_pos.world_y = request.world_y
    player_pos.world_z = request.world_z
    player_pos.rotation_y = request.rotation_y
    player_pos.last_moved_at = datetime.utcnow()

    # Check which region player is in
    regions = db.query(Region).all()
    current_region_id = None

    for region in regions:
        if (region.position_x <= request.world_x <= region.position_x + region.width and
            region.position_y <= request.world_y <= region.position_y + region.height):
            current_region_id = region.id
            break

    player_pos.region_id = current_region_id

    db.commit()

    return {
        "success": True,
        "position": {
            "x": player_pos.world_x,
            "y": player_pos.world_y,
            "z": player_pos.world_z
        },
        "region_id": current_region_id
    }


# ============================================================================
# WEATHER & TIME ENDPOINTS
# ============================================================================

@router.get("/time")
async def get_day_night_cycle(db: Session = Depends(get_db)):
    """
    Get current day/night cycle state
    """
    cycle = db.query(DayNightCycle).first()

    if not cycle:
        # Create default cycle
        cycle = DayNightCycle(
            current_hour=12.0,  # Noon
            current_day=1,
            time_scale=60.0,  # 1 hour = 1 minute
            sun_angle=180.0,
            moon_phase=0.5,
            ambient_light=1.0,
            sun_intensity=1.0
        )
        db.add(cycle)
        db.commit()
        db.refresh(cycle)

    return {
        "current_hour": cycle.current_hour,
        "current_day": cycle.current_day,
        "time_scale": cycle.time_scale,
        "is_day": 6.0 <= cycle.current_hour <= 18.0,
        "sun_angle": cycle.sun_angle,
        "moon_phase": cycle.moon_phase,
        "ambient_light": cycle.ambient_light,
        "sun_intensity": cycle.sun_intensity
    }


@router.get("/weather/{region_id}")
async def get_region_weather(region_id: int, db: Session = Depends(get_db)):
    """
    Get current weather for region
    """
    weather = db.query(WorldWeather).filter(
        WorldWeather.region_id == region_id
    ).order_by(WorldWeather.started_at.desc()).first()

    if not weather:
        return {
            "weather_type": "clear",
            "intensity": 0.5,
            "temperature": 20.0,
            "wind_speed": 0.0,
            "visibility": 1.0
        }

    return {
        "weather_type": weather.weather_type,
        "intensity": weather.intensity,
        "temperature": weather.temperature,
        "wind_speed": weather.wind_speed,
        "wind_direction": weather.wind_direction,
        "visibility": weather.visibility,
        "particle_effects": weather.particle_effects or {}
    }


# ============================================================================
# EXPLORATION ENDPOINTS (Frontend: world_map_api.js)
# ============================================================================

@router.get("/explored-regions")
async def get_explored_regions(player_id: int = 1, db: Session = Depends(get_db)):
    """
    Get explored regions for a player (Frontend: WorldMapAPI.loadExploredRegions)
    """
    # Check which regions player has visited via travel point unlocks
    unlocks = db.query(PlayerTravelPointUnlock).filter(
        PlayerTravelPointUnlock.user_id == player_id
    ).all()

    # Get region codes from unlocked travel points
    explored = set(["goetterfels"])  # Starting region always explored
    for unlock in unlocks:
        tp = db.query(FastTravelPoint).filter(FastTravelPoint.id == unlock.travel_point_id).first()
        if tp:
            region = db.query(Region).filter(Region.id == tp.region_id).first()
            if region:
                explored.add(region.region_code)

    return {
        "player_id": player_id,
        "explored_regions": list(explored),
        "count": len(explored)
    }


class DiscoverRegionRequest(BaseModel):
    player_id: int = 1
    region_id: str = ""


@router.post("/discover-region")
async def discover_region(request: DiscoverRegionRequest, db: Session = Depends(get_db)):
    """
    Mark a region as discovered (Frontend: WorldMapAPI.discoverRegion)
    """
    if not request.region_id:
        raise HTTPException(status_code=400, detail="region_id required")

    # Find region by code
    region = db.query(Region).filter(Region.region_code == request.region_id).first()
    if not region:
        # Gracefully return success even if region not in DB yet
        return {
            "success": True,
            "region_id": request.region_id,
            "region_name": request.region_id,
            "message": f"Region {request.region_id} entdeckt!"
        }

    # Auto-unlock the region's first travel point
    first_tp = db.query(FastTravelPoint).filter(
        FastTravelPoint.region_id == region.id
    ).first()

    if first_tp:
        existing = db.query(PlayerTravelPointUnlock).filter(
            PlayerTravelPointUnlock.user_id == request.player_id,
            PlayerTravelPointUnlock.travel_point_id == first_tp.id
        ).first()

        if not existing:
            unlock = PlayerTravelPointUnlock(
                user_id=request.player_id,
                travel_point_id=first_tp.id,
                unlocked_at=datetime.utcnow()
            )
            db.add(unlock)
            db.commit()

    return {
        "success": True,
        "region_id": request.region_id,
        "region_name": region.name,
        "message": f"Region {region.name} entdeckt!"
    }
