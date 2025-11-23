"""
World State Models - Najika World
Database models for world state system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class WorldState(Base):
    """Global world state (singleton)"""
    __tablename__ = "world_state"

    id = Column(Integer, primary_key=True, index=True)

    # Time & Weather
    world_time = Column(Integer, default=0)  # seconds since start
    world_day = Column(Integer, default=1)
    world_season = Column(String(20), default="spring")  # spring, summer, autumn, winter
    current_weather = Column(String(50), default="clear")

    # Global Events
    active_events = Column(JSON, default=[])  # List of active world events
    event_flags = Column(JSON, default={})  # Dict of event completion flags

    # World Bosses
    world_boss_spawned = Column(Boolean, default=False)
    world_boss_name = Column(String(200), nullable=True)
    world_boss_location = Column(String(200), nullable=True)

    # Economy
    global_gold_pool = Column(Integer, default=0)
    inflation_rate = Column(Float, default=1.0)

    # Server Status
    server_version = Column(String(50), default="2.0.0")
    maintenance_mode = Column(Boolean, default=False)

    # Timestamps
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "world_time": self.world_time,
            "world_day": self.world_day,
            "world_season": self.world_season,
            "current_weather": self.current_weather,
            "active_events": self.active_events or [],
            "event_flags": self.event_flags or {},
            "world_boss_spawned": self.world_boss_spawned,
            "world_boss_name": self.world_boss_name,
            "world_boss_location": self.world_boss_location,
            "global_gold_pool": self.global_gold_pool,
            "inflation_rate": self.inflation_rate,
            "server_version": self.server_version,
            "maintenance_mode": self.maintenance_mode,
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PlayerWorldState(Base):
    """Player-specific world state"""
    __tablename__ = "player_world_state"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Position
    current_region = Column(String(100), default="samtmoos_tiefwald")
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)
    position_z = Column(Float, default=0.0)

    # Discovered Regions
    discovered_regions = Column(JSON, default=[])  # List of region names
    unlocked_teleports = Column(JSON, default=[])  # List of teleport points

    # Quest Flags
    completed_quests = Column(JSON, default=[])  # List of quest IDs
    active_quests = Column(JSON, default=[])  # List of quest IDs
    quest_progress = Column(JSON, default={})  # Dict of quest progress

    # Collectibles
    found_treasures = Column(JSON, default=[])  # List of treasure IDs
    collected_artifacts = Column(JSON, default=[])  # List of artifact IDs

    # Reputation
    faction_reputation = Column(JSON, default={})  # Dict of faction reps

    # Timestamps
    last_position_update = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="world_state")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "current_region": self.current_region,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "position_z": self.position_z,
            "discovered_regions": self.discovered_regions or [],
            "unlocked_teleports": self.unlocked_teleports or [],
            "completed_quests": self.completed_quests or [],
            "active_quests": self.active_quests or [],
            "quest_progress": self.quest_progress or {},
            "found_treasures": self.found_treasures or [],
            "collected_artifacts": self.collected_artifacts or [],
            "faction_reputation": self.faction_reputation or {},
            "last_position_update": self.last_position_update.isoformat() if self.last_position_update else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
