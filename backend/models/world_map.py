"""
World Map System Models
9600x9600 Grid World with 8 Regions + Götterfels Center
"""

from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Region(Base):
    """
    8 Regions around Götterfels
    Persistent world (not procedurally generated!)
    """
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)

    # Region Info
    name = Column(String(100), nullable=False)  # "Heiße Dünen", "Samtmoos-Tiefwald"
    region_code = Column(String(50), unique=True)  # "heisse_duenen", "samtmoos_tiefwald"

    # Position in 9600x9600 World Grid
    position_x = Column(Integer)  # Start X
    position_y = Column(Integer)  # Start Y
    width = Column(Integer)  # Region width
    height = Column(Integer)  # Region height

    # Biome & Environment
    biome_type = Column(String(50))  # "desert", "forest", "mountain", etc.
    slime_color = Column(String(50))  # "dusty_gold", "moss_green"
    climate = Column(String(50))  # "hot_dry", "humid_warm", "cold_snowy"

    # Terrain Generation Data (for 3D rendering)
    terrain_config = Column(JSON)  # {"elevation_range": [0, 100], "vegetation_density": 0.7}

    # Features
    features = Column(JSON)  # ["oasis", "sand_dunes", "ancient_ruins"]
    dangers = Column(JSON)  # ["sandstorms", "scorpions", "bandits"]

    # Resources
    resources = Column(JSON)  # {"minerals": ["copper", "iron"], "plants": ["cactus", "aloe"]}

    # Relationships
    fast_travel_points = relationship("FastTravelPoint", back_populates="region", cascade="all, delete-orphan")
    player_positions = relationship("PlayerPosition", back_populates="region", cascade="all, delete-orphan")


class FastTravelPoint(Base):
    """
    Fast travel locations within regions
    """
    __tablename__ = "fast_travel_points"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey('regions.id'))

    # Travel Point Info
    name = Column(String(100))  # "Desert Oasis", "Forest Shrine"
    point_type = Column(String(50))  # "shrine", "waypoint", "town", "landmark"

    # Position
    position_x = Column(Float)
    position_y = Column(Float)
    position_z = Column(Float, default=0.0)

    # Unlock Requirements
    is_locked = Column(Boolean, default=True)
    unlock_requirement = Column(String(200))  # "Defeat Region Boss", "Find Hidden Key"

    # Icon & Description
    icon = Column(String(50))  # "🏜️", "🌲", "⛰️"
    description = Column(String(500))

    # Relationships
    region = relationship("Region", back_populates="fast_travel_points")


class PlayerPosition(Base):
    """
    Player's current position in the world
    Persistent tracking for Lebensraum world
    """
    __tablename__ = "player_positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    # Current Location
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=True)

    # 3D Position in World Grid
    world_x = Column(Float)  # 0-9600
    world_y = Column(Float)  # 0-9600
    world_z = Column(Float, default=0.0)  # Elevation

    # Rotation
    rotation_y = Column(Float, default=0.0)  # Facing direction

    # Current State
    is_in_house = Column(Boolean, default=False)
    is_in_dungeon = Column(Boolean, default=False)
    current_room = Column(String(50), nullable=True)  # "living_room", "kitchen", etc.

    # Last Updated
    last_moved_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    region = relationship("Region", back_populates="player_positions")


class RegionBoundary(Base):
    """
    Boundaries between regions
    For smooth transitions
    """
    __tablename__ = "region_boundaries"

    id = Column(Integer, primary_key=True, index=True)

    # Boundary Info
    region_a_id = Column(Integer, ForeignKey('regions.id'))
    region_b_id = Column(Integer, ForeignKey('regions.id'))

    # Boundary Line (simplified as 2 points)
    start_x = Column(Float)
    start_y = Column(Float)
    end_x = Column(Float)
    end_y = Column(Float)

    # Transition Type
    transition_type = Column(String(50))  # "smooth", "cliff", "river", "wall"

    # Visual Blending
    blend_distance = Column(Float, default=100.0)  # Pixels for terrain blending


class WorldWeather(Base):
    """
    Weather system per region
    Changes dynamically
    """
    __tablename__ = "world_weather"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey('regions.id'))

    # Current Weather
    weather_type = Column(String(50))  # "clear", "rain", "storm", "sandstorm", "snow"
    intensity = Column(Float, default=0.5)  # 0.0 - 1.0

    # Temperature & Conditions
    temperature = Column(Float)  # -20°C to 50°C
    wind_speed = Column(Float, default=0.0)  # 0-100 km/h
    wind_direction = Column(Float, default=0.0)  # 0-360 degrees

    # Duration
    started_at = Column(DateTime, default=datetime.utcnow)
    duration_minutes = Column(Integer, default=60)

    # Visual Effects
    visibility = Column(Float, default=1.0)  # 0.0 (fog) to 1.0 (clear)
    particle_effects = Column(JSON)  # {"rain": true, "lightning": false}


class DayNightCycle(Base):
    """
    Global day/night cycle
    Synchronized across all regions
    """
    __tablename__ = "day_night_cycle"

    id = Column(Integer, primary_key=True, index=True)

    # Time
    current_hour = Column(Float)  # 0.0 - 24.0
    current_day = Column(Integer, default=1)  # Day counter

    # Cycle Speed
    time_scale = Column(Float, default=1.0)  # 1.0 = real-time, 60.0 = 1 hour/min

    # Sun/Moon Position
    sun_angle = Column(Float)  # 0-360 degrees
    moon_phase = Column(Float)  # 0.0 (new moon) to 1.0 (full moon)

    # Lighting
    ambient_light = Column(Float)  # 0.0 (night) to 1.0 (day)
    sun_intensity = Column(Float)  # 0.0 - 1.0

    # Last Updated
    updated_at = Column(DateTime, default=datetime.utcnow)
