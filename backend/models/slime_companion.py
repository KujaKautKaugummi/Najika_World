"""
Slime Companion Model
Database model for Slime Companion System (Tamagotchi + Monster Rancher)
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class SlimeCompanion(Base):
    """Slime Companion model (Tamagotchi-style)"""

    __tablename__ = "slime_companions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    companion_id = Column(Integer, unique=True, index=True)  # Game-specific ID

    # Ownership
    owner_player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Info
    name = Column(String(100), nullable=False)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    xp_required = Column(Integer, default=100)

    # Fantasy Tier (Tier → Slime → Rainbow)
    fantasy_tier = Column(String(20), nullable=True)  # "tier", "slime", "rainbow"
    metamorphosed = Column(Boolean, default=False)
    metamorphosis_region = Column(String(50), nullable=True)

    # Rainbow Quest (Color Collection)
    collected_colors = Column(JSON, default=list)  # List of color strings

    # Tamagotchi Needs (0-100)
    hunger = Column(Float, default=100.0)
    thirst = Column(Float, default=100.0)
    schlaf = Column(Float, default=100.0)  # Sleep
    stimmung = Column(Float, default=100.0)  # Mood
    kampfeslust = Column(Float, default=0.0)  # Battle lust

    # Moveset (Learning System)
    moves = Column(JSON, default=list)  # List of move dicts
    max_moves = Column(Integer, default=20)

    # Hardcore Mode
    is_hardcore = Column(Boolean, default=False)
    rescue_available = Column(Boolean, default=True)
    rescue_cooldown_until = Column(DateTime, nullable=True)
    last_rescue_time = Column(DateTime, nullable=True)

    # Combat Stats
    health = Column(Float, default=100.0)
    max_health = Column(Float, default=100.0)
    attack = Column(Float, default=10.0)
    defense = Column(Float, default=10.0)

    # Stats
    total_battles = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_fed = Column(DateTime, default=datetime.utcnow)
    last_watered = Column(DateTime, default=datetime.utcnow)
    last_slept = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="slime_companions")

    def __repr__(self):
        return f"<SlimeCompanion(id={self.companion_id}, name='{self.name}', level={self.level}, tier='{self.fantasy_tier}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "companion_id": self.companion_id,
            "owner_player_id": self.owner_player_id,
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "xp_required": self.xp_required,
            "fantasy_tier": self.fantasy_tier,
            "metamorphosed": self.metamorphosed,
            "metamorphosis_region": self.metamorphosis_region,
            "collected_colors": self.collected_colors,
            "needs": {
                "hunger": self.hunger,
                "thirst": self.thirst,
                "schlaf": self.schlaf,
                "stimmung": self.stimmung,
                "kampfeslust": self.kampfeslust,
            },
            "moves": self.moves,
            "max_moves": self.max_moves,
            "is_hardcore": self.is_hardcore,
            "rescue_available": self.rescue_available,
            "rescue_cooldown_until": self.rescue_cooldown_until.isoformat() if self.rescue_cooldown_until else None,
            "stats": {
                "health": self.health,
                "max_health": self.max_health,
                "attack": self.attack,
                "defense": self.defense,
                "total_battles": self.total_battles,
                "total_wins": self.total_wins,
            },
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_update": self.last_update.isoformat() if self.last_update else None,
        }
