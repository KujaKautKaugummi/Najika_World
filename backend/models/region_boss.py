"""
Region Boss Spawn Models - Najika World
Database models for boss spawn system in regions
(Note: Different from Territory Control "RegionBoss" in magic_progress.py)
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from backend.database import Base


class BossSpawn(Base):
    """Boss monster spawns in regions"""
    __tablename__ = "boss_spawns"

    id = Column(Integer, primary_key=True, index=True)

    # Region Info
    region_name = Column(String(100), nullable=False, index=True)  # "samtmoos_tiefwald", etc.

    # Boss Info
    boss_name = Column(String(200), nullable=False)
    boss_type = Column(String(50), nullable=False)  # "field_boss", "dungeon_boss", "world_boss"
    boss_level = Column(Integer, nullable=False)
    boss_health = Column(Integer, nullable=False)

    # Spawn Status
    active = Column(Boolean, default=True)
    defeated = Column(Boolean, default=False)

    # Spawn Details
    spawn_location = Column(String(200), nullable=False)  # Coordinates or landmark
    spawn_radius = Column(Integer, default=50)  # meters

    # Loot
    guaranteed_drops = Column(JSON, default=[])  # List of item IDs
    rare_drops = Column(JSON, default=[])  # List of item IDs with drop rates
    gold_reward = Column(Integer, default=1000)
    exp_reward = Column(Integer, default=5000)

    # Mechanics
    abilities = Column(JSON, default=[])  # List of boss abilities
    phases = Column(Integer, default=1)  # Boss phases (1-3)
    enrage_timer = Column(Integer, default=600)  # seconds (10 min)

    # Difficulty
    recommended_players = Column(Integer, default=1)  # Solo or group
    recommended_level = Column(Integer, default=50)

    # Respawn
    respawn_time_hours = Column(Integer, default=24)  # hours until respawn
    last_defeated_at = Column(DateTime, nullable=True)
    next_spawn_at = Column(DateTime, nullable=True)

    # Timestamps
    spawned_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    defeats = relationship("BossSpawnDefeat", back_populates="boss", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "region_name": self.region_name,
            "boss_name": self.boss_name,
            "boss_type": self.boss_type,
            "boss_level": self.boss_level,
            "boss_health": self.boss_health,
            "active": self.active,
            "defeated": self.defeated,
            "spawn_location": self.spawn_location,
            "spawn_radius": self.spawn_radius,
            "guaranteed_drops": self.guaranteed_drops or [],
            "rare_drops": self.rare_drops or [],
            "gold_reward": self.gold_reward,
            "exp_reward": self.exp_reward,
            "abilities": self.abilities or [],
            "phases": self.phases,
            "enrage_timer": self.enrage_timer,
            "recommended_players": self.recommended_players,
            "recommended_level": self.recommended_level,
            "respawn_time_hours": self.respawn_time_hours,
            "last_defeated_at": self.last_defeated_at.isoformat() if self.last_defeated_at else None,
            "next_spawn_at": self.next_spawn_at.isoformat() if self.next_spawn_at else None,
            "spawned_at": self.spawned_at.isoformat() if self.spawned_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class BossSpawnDefeat(Base):
    """Log of boss spawn defeats"""
    __tablename__ = "boss_spawn_defeats"

    id = Column(Integer, primary_key=True, index=True)
    boss_id = Column(Integer, ForeignKey("boss_spawns.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Defeat Details
    party_size = Column(Integer, default=1)
    party_members = Column(JSON, default=[])  # List of player IDs

    # Performance
    time_to_kill = Column(Integer, nullable=False)  # seconds
    deaths_during_fight = Column(Integer, default=0)
    damage_dealt = Column(Integer, default=0)
    damage_taken = Column(Integer, default=0)

    # Rewards
    gold_earned = Column(Integer, default=0)
    exp_earned = Column(Integer, default=0)
    items_dropped = Column(JSON, default=[])  # List of item IDs

    # Achievement
    first_kill = Column(Boolean, default=False)  # Server-first?
    flawless = Column(Boolean, default=False)  # No deaths?
    speedrun = Column(Boolean, default=False)  # Under 5 minutes?

    # Timestamp
    defeated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    boss = relationship("BossSpawn", back_populates="defeats")
    player = relationship("User", back_populates="boss_spawn_defeats")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "boss_id": self.boss_id,
            "player_id": self.player_id,
            "party_size": self.party_size,
            "party_members": self.party_members or [],
            "time_to_kill": self.time_to_kill,
            "deaths_during_fight": self.deaths_during_fight,
            "damage_dealt": self.damage_dealt,
            "damage_taken": self.damage_taken,
            "gold_earned": self.gold_earned,
            "exp_earned": self.exp_earned,
            "items_dropped": self.items_dropped or [],
            "first_kill": self.first_kill,
            "flawless": self.flawless,
            "speedrun": self.speedrun,
            "defeated_at": self.defeated_at.isoformat() if self.defeated_at else None,
        }
