"""
World API - Najika World
=========================

REST API für World System (Biomes, Weather, Day/Night, Cities, Wilderness) (FastAPI)

Endpoints:
- GET /api/world/info - Get map info
- GET /api/world/biomes - Get all biomes
- GET /api/world/biome/<biome> - Get specific biome
- GET /api/world/weather/<biome> - Get weather for biome
- POST /api/world/weather/<biome>/update - Force weather update
- GET /api/world/time - Get current time (DATABASE)
- POST /api/world/time/set - Set game time (DATABASE)
- POST /api/world/time/update - Update time (delta) (DATABASE)
- GET /api/world/cities - Get all cities
- GET /api/world/city/<city_id> - Get specific city
- POST /api/world/city/enter - Check if can enter city
- GET /api/world/wilderness/<biome> - Generate/get wilderness
- GET /api/world/state/export - Export complete state (DATABASE)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import get_db
from backend.models.world_state import WorldState, PlayerWorldState
from backend.services.world_system import WorldSystem, Biome

# Create FastAPI Router
router = APIRouter(prefix="/api/world", tags=["world"])

# Global System Instance (for static config: biomes, cities, weather)
world_system = WorldSystem()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_or_create_world_state(db: Session) -> WorldState:
    """Get or create singleton WorldState"""
    world_state = db.query(WorldState).first()
    if not world_state:
        world_state = WorldState(
            id=1,
            world_time=0,
            world_day=1,
            world_season="spring",
            current_weather="clear"
        )
        db.add(world_state)
        db.commit()
        db.refresh(world_state)
    return world_state


def get_or_create_player_world_state(db: Session, player_id: int) -> PlayerWorldState:
    """Get or create PlayerWorldState for player"""
    player_state = db.query(PlayerWorldState).filter(
        PlayerWorldState.player_id == player_id
    ).first()

    if not player_state:
        player_state = PlayerWorldState(
            player_id=player_id,
            current_region="samtmoos_tiefwald",
            position_x=0.0,
            position_y=0.0,
            position_z=0.0
        )
        db.add(player_state)
        db.commit()
        db.refresh(player_state)

    return player_state


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class SetTimeRequest(BaseModel):
    hour: int = Field(..., ge=0, lt=24)
    minute: int = Field(0, ge=0, lt=60)


class UpdateTimeRequest(BaseModel):
    delta_seconds: float = Field(..., gt=0)


class CheckCityEntryRequest(BaseModel):
    city_id: str
    player_reputation: int = 0


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/info")
async def get_map_info():
    """
    Get Map Info

    Returns:
        {
            size_meters: int,
            size_km2: float,
            goetterfels_height: int,
            wilderness_percentage: float,
            total_biomes: int,
            total_cities: int
        }
    """
    try:
        return {
            "size_meters": world_system.MAP_SIZE,
            "size_km2": world_system.total_area_km2,
            "goetterfels_height": world_system.GOETTERFELS_HEIGHT,
            "wilderness_percentage": world_system.wilderness_percentage,
            "total_biomes": len(world_system.biomes),
            "total_cities": len(world_system.cities)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/biomes")
async def get_all_biomes():
    """
    Get All Biomes

    Returns:
        {
            biomes: {
                biome_id: {
                    name: str,
                    description: str,
                    slime_color: str,
                    temperature_range: str,
                    hazardous: bool,
                    vegetation_density: float,
                    possible_weather: [str],
                    resources: [str]
                }
            }
        }
    """
    try:
        biomes_data = {}

        for biome, config in world_system.biomes.items():
            biomes_data[biome.value] = {
                "name": config.name,
                "description": config.description,
                "slime_color": config.slime_color,
                "temperature_range": f"{config.temperature_min}°C - {config.temperature_max}°C",
                "hazardous": config.hazardous,
                "vegetation_density": config.vegetation_density,
                "terrain_roughness": config.terrain_roughness,
                "water_presence": config.water_presence,
                "has_ocean": config.has_ocean,
                "lava_flows": config.lava_flows,
                "possible_weather": [w.value for w in config.possible_weather],
                "resources": config.resources,
                "enemy_types": config.enemy_types
            }

        return {"biomes": biomes_data, "count": len(biomes_data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/biome/{biome_id}")
async def get_biome(biome_id: str):
    """
    Get Specific Biome

    Path: /api/world/biome/samtmoos_tiefwald
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiges Biome: {biome_id}",
                    "valid_biomes": [b.value for b in Biome]
                }
            )

        config = world_system.biomes[biome]

        return {
            "id": biome.value,
            "name": config.name,
            "description": config.description,
            "slime_color": config.slime_color,
            "temperature_range": f"{config.temperature_min}°C - {config.temperature_max}°C",
            "hazardous": config.hazardous,
            "vegetation_density": config.vegetation_density,
            "terrain_roughness": config.terrain_roughness,
            "water_presence": config.water_presence,
            "has_ocean": config.has_ocean,
            "lava_flows": config.lava_flows,
            "possible_weather": [w.value for w in config.possible_weather],
            "resources": config.resources,
            "enemy_types": config.enemy_types,
            "colors": {
                "ground": config.ground_color,
                "ambient": config.ambient_color,
                "fog": config.fog_color
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weather/{biome_id}")
async def get_weather(biome_id: str):
    """
    Get Weather for Biome

    Path: /api/world/weather/samtmoos_tiefwald
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiges Biome: {biome_id}",
                    "valid_biomes": [b.value for b in Biome]
                }
            )

        weather = world_system.get_weather(biome)

        return {
            "biome": biome.value,
            "weather": {
                "type": weather.type.value,
                "intensity": weather.intensity,
                "temperature": weather.temperature,
                "wind_speed": weather.wind_speed,
                "visibility": weather.visibility,
                "modifiers": {
                    "movement": weather.movement_modifier,
                    "accuracy": weather.accuracy_modifier,
                    "damage": weather.damage_modifier
                },
                "started_at": weather.started_at.isoformat(),
                "duration_minutes": weather.duration_minutes
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/weather/{biome_id}/update")
async def update_weather(biome_id: str):
    """
    Force Weather Update for Biome

    Path: /api/world/weather/samtmoos_tiefwald/update
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiges Biome: {biome_id}",
                    "valid_biomes": [b.value for b in Biome]
                }
            )

        changed = world_system.update_weather(biome)

        new_weather = world_system.get_weather(biome)

        return {
            "biome": biome.value,
            "changed": changed,
            "new_weather": {
                "type": new_weather.type.value,
                "intensity": new_weather.intensity,
                "temperature": new_weather.temperature
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/time")
async def get_time(db: Session = Depends(get_db)):
    """
    Get Current Game Time (DATABASE)

    Returns:
        {
            world_time: int,
            world_day: int,
            world_season: str,
            current_time: str,
            time_of_day: str,
            is_night: bool
        }
    """
    try:
        world_state = get_or_create_world_state(db)

        # Calculate time from world_time (seconds since start)
        hours = (world_state.world_time // 3600) % 24
        minutes = (world_state.world_time // 60) % 60

        # Determine time of day
        if 6 <= hours < 12:
            time_of_day = "morning"
        elif 12 <= hours < 18:
            time_of_day = "afternoon"
        elif 18 <= hours < 22:
            time_of_day = "evening"
        else:
            time_of_day = "night"

        is_night = hours < 6 or hours >= 22

        return {
            "world_time": world_state.world_time,
            "world_day": world_state.world_day,
            "world_season": world_state.world_season,
            "current_time": f"{hours:02d}:{minutes:02d}",
            "time_of_day": time_of_day,
            "is_night": is_night
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/time/set")
async def set_time(request: SetTimeRequest, db: Session = Depends(get_db)):
    """
    Set Game Time (DATABASE)

    Body:
    {
        "hour": 14,
        "minute": 30
    }
    """
    try:
        world_state = get_or_create_world_state(db)

        # Set time as seconds since start of day
        new_time = (request.hour * 3600) + (request.minute * 60)
        world_state.world_time = new_time

        db.commit()
        db.refresh(world_state)

        hours = request.hour
        minutes = request.minute

        return {
            "success": True,
            "time": {
                "world_time": world_state.world_time,
                "world_day": world_state.world_day,
                "current_time": f"{hours:02d}:{minutes:02d}"
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/time/update")
async def update_time(request: UpdateTimeRequest, db: Session = Depends(get_db)):
    """
    Update Game Time (Delta) (DATABASE)

    Body:
    {
        "delta_seconds": 60.0
    }

    Used by game loop to advance time
    """
    try:
        world_state = get_or_create_world_state(db)

        # Update time
        world_state.world_time += int(request.delta_seconds)

        # Check if day changed (86400 seconds = 1 day)
        if world_state.world_time >= 86400:
            days_passed = world_state.world_time // 86400
            world_state.world_day += days_passed
            world_state.world_time = world_state.world_time % 86400

        world_state.last_update = datetime.utcnow()

        db.commit()
        db.refresh(world_state)

        hours = (world_state.world_time // 3600) % 24
        minutes = (world_state.world_time // 60) % 60

        return {
            "success": True,
            "time": {
                "world_time": world_state.world_time,
                "world_day": world_state.world_day,
                "current_time": f"{hours:02d}:{minutes:02d}"
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cities")
async def get_all_cities():
    """
    Get All Cities

    Returns:
        {
            cities: {
                city_id: {
                    name: str,
                    type: str,
                    biome: str,
                    position: [x, y, z],
                    population: int,
                    wealth_level: int,
                    services: {},
                    guard_level: int,
                    pvp_enabled: bool,
                    min_reputation: int
                }
            }
        }
    """
    try:
        cities = world_system.get_all_cities()
        return {"cities": cities, "count": len(cities)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/city/{city_id}")
async def get_city(city_id: str):
    """
    Get Specific City

    Path: /api/world/city/handelsfestung
    """
    try:
        city = world_system.get_city(city_id)

        if not city:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": f"Stadt nicht gefunden: {city_id}",
                    "available_cities": list(world_system.cities.keys())
                }
            )

        return {
            "id": city.id,
            "name": city.name,
            "type": city.type.value,
            "biome": city.biome.value,
            "position": city.position,
            "population": city.population,
            "wealth_level": city.wealth_level,
            "services": {
                "smithy": city.has_smithy,
                "alchemy": city.has_alchemy,
                "inn": city.has_inn,
                "temple": city.has_temple,
                "market": city.has_market,
                "crafting_stations": city.has_crafting_stations
            },
            "guard_level": city.guard_level,
            "pvp_enabled": city.pvp_enabled,
            "npc_count": city.npc_count,
            "min_reputation": city.min_reputation
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/city/enter")
async def check_city_entry(request: CheckCityEntryRequest):
    """
    Check if Player Can Enter City

    Body:
    {
        "city_id": "handelsfestung",
        "player_reputation": 50
    }
    """
    try:
        can_enter, message = world_system.can_enter_city(
            request.city_id,
            request.player_reputation
        )

        return {
            "city_id": request.city_id,
            "can_enter": can_enter,
            "message": message,
            "player_reputation": request.player_reputation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/wilderness/{biome_id}")
async def get_wilderness(
    biome_id: str,
    player_id: int = Query(..., description="Player ID")
):
    """
    Generate/Get Wilderness Area

    Query Params:
        player_id: int (required)

    Path: /api/world/wilderness/samtmoos_tiefwald?player_id=1
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiges Biome: {biome_id}",
                    "valid_biomes": [b.value for b in Biome]
                }
            )

        wilderness = world_system.get_wilderness(biome, player_id)

        return {
            "biome": wilderness.biome.value,
            "seed": wilderness.seed,
            "layout_variant": wilderness.layout_variant,
            "poi_count": wilderness.poi_count,
            "pois": wilderness.pois,
            "active_events": wilderness.active_events,
            "modifiers": wilderness.modifiers,
            "enemy_density": wilderness.enemy_density,
            "resource_density": wilderness.resource_density,
            "created_at": wilderness.created_at.isoformat(),
            "expires_at": wilderness.expires_at.isoformat() if wilderness.expires_at else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
async def export_state(db: Session = Depends(get_db)):
    """
    Export Complete World State (DATABASE)

    Returns:
        JSON with map info, biomes, weather, time, cities, world state
    """
    try:
        # Get world state from database
        world_state = get_or_create_world_state(db)

        # Get all player world states
        player_states = db.query(PlayerWorldState).all()

        # Get static world system state
        system_state = world_system.export_state()

        # Combine with database state
        state = {
            **system_state,
            "database_state": {
                "world_time": world_state.world_time,
                "world_day": world_state.world_day,
                "world_season": world_state.world_season,
                "current_weather": world_state.current_weather,
                "active_events": world_state.active_events or [],
                "maintenance_mode": world_state.maintenance_mode,
                "player_count": len(player_states)
            }
        }

        return state

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
