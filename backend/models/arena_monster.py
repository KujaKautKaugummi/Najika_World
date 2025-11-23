"""
Arena Monster Model
Database model for Nemesis Arena System (Shadow of Mordor style)
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class ArenaMonster(Base):
    """Arena Monster (Nemesis System)"""

    __tablename__ = "arena_monsters"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    monster_id = Column(Integer, unique=True, index=True)

    # Basic Info
    name = Column(String(100), nullable=False)
    monster_type = Column(String(50), nullable=False)  # "goblin", "orc", "troll", etc.
    rank = Column(String(20), default="NOBODY")  # NOBODY, SOLDIER, CAPTAIN, LORD, ARENA_KING

    # Stats
    level = Column(Integer, default=1)
    current_health = Column(Float, default=100.0)
    max_health = Column(Float, default=100.0)
    attack = Column(Float, default=10.0)
    defense = Column(Float, default=10.0)

    # Traits
    traits = Column(JSON, default=list)  # List of trait strings
    weaknesses = Column(JSON, default=list)
    strengths = Column(JSON, default=list)

    # Nemesis System
    memories = Column(JSON, default=dict)  # Player ID -> memory string
    grudges = Column(JSON, default=list)  # List of grudge dicts
    encounters_with_player = Column(Integer, default=0)

    # Position
    region_controlled = Column(String(50), nullable=True)
    position = Column(JSON, default=dict)  # {x, y, z}

    # Combat History
    total_battles = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    players_killed = Column(Integer, default=0)
    times_killed = Column(Integer, default=0)

    # Status
    is_alive = Column(Boolean, default=True)
    is_injured = Column(Boolean, default=False)
    injury_recovery_time = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_battle = Column(DateTime, nullable=True)
    last_promotion = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ArenaMonster(id={self.monster_id}, name='{self.name}', rank='{self.rank}', level={self.level})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "monster_id": self.monster_id,
            "name": self.name,
            "monster_type": self.monster_type,
            "rank": self.rank,
            "level": self.level,
            "health": {
                "current": self.current_health,
                "max": self.max_health,
            },
            "stats": {
                "attack": self.attack,
                "defense": self.defense,
            },
            "traits": self.traits,
            "weaknesses": self.weaknesses,
            "strengths": self.strengths,
            "nemesis": {
                "memories": self.memories,
                "grudges": self.grudges,
                "encounters": self.encounters_with_player,
            },
            "region_controlled": self.region_controlled,
            "position": self.position,
            "combat_history": {
                "battles": self.total_battles,
                "wins": self.total_wins,
                "losses": self.total_losses,
                "players_killed": self.players_killed,
                "times_killed": self.times_killed,
            },
            "status": {
                "alive": self.is_alive,
                "injured": self.is_injured,
                "recovery_time": self.injury_recovery_time.isoformat() if self.injury_recovery_time else None,
            },
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_battle": self.last_battle.isoformat() if self.last_battle else None,
        }


class Finisher(Base):
    """Mortal Kombat Style Finisher"""

    __tablename__ = "finishers"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    finisher_id = Column(Integer, unique=True, index=True)

    # Creator
    user_id = Column(Integer, nullable=False)
    character_level = Column(Integer, default=1)

    # Finisher Data
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # HONORABLE_DEATH, FUNNY_DEATH, etc.
    ingredients = Column(JSON, default=list)  # Player keywords
    description = Column(String(500), nullable=False)

    # Animation Data
    animation_style = Column(String(50), nullable=False)
    brutality_level = Column(Integer, default=5)  # 1-10
    humor_level = Column(Integer, default=5)  # 1-10

    # Stats
    use_count = Column(Integer, default=0)
    likes = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Finisher(id={self.finisher_id}, name='{self.name}', category='{self.category}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "finisher_id": self.finisher_id,
            "user_id": self.user_id,
            "name": self.name,
            "category": self.category,
            "ingredients": self.ingredients,
            "description": self.description,
            "animation_style": self.animation_style,
            "brutality_level": self.brutality_level,
            "humor_level": self.humor_level,
            "stats": {
                "use_count": self.use_count,
                "likes": self.likes,
            },
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
