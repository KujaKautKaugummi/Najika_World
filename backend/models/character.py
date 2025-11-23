"""
Character Model
Database model for game characters (Digimon/Creatures)
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Character(Base):
    """Character/Digimon model"""

    __tablename__ = "characters"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Ownership
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Info
    name = Column(String(100), nullable=False)
    species = Column(String(100), nullable=False)  # e.g., "Jellysquish", "Agumon"
    nickname = Column(String(100), nullable=True)

    # Stats
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    health = Column(Float, default=100.0)
    max_health = Column(Float, default=100.0)
    mana = Column(Float, default=100.0)
    max_mana = Column(Float, default=100.0)
    stamina = Column(Float, default=100.0)
    max_stamina = Column(Float, default=100.0)

    # Combat Stats
    attack = Column(Float, default=10.0)
    defense = Column(Float, default=10.0)
    speed = Column(Float, default=10.0)
    magic = Column(Float, default=10.0)

    # Status
    hunger = Column(Float, default=100.0)  # 0-100
    happiness = Column(Float, default=100.0)  # 0-100
    energy = Column(Float, default=100.0)  # 0-100

    # Position
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)
    position_z = Column(Float, default=0.0)

    # Inventory Reference
    inventory_data = Column(JSON, default=dict)  # Stores items as JSON

    # Skills/Abilities
    skills = Column(JSON, default=list)  # List of skill IDs

    # Buffs/Debuffs
    active_buffs = Column(JSON, default=list)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="characters")
    inventory = relationship("InventoryItem", back_populates="character", cascade="all, delete-orphan")
    equipment = relationship("Equipment", back_populates="character", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}', species='{self.species}', level={self.level})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "species": self.species,
            "nickname": self.nickname,
            "level": self.level,
            "xp": self.xp,
            "stats": {
                "health": self.health,
                "max_health": self.max_health,
                "mana": self.mana,
                "max_mana": self.max_mana,
                "stamina": self.stamina,
                "max_stamina": self.max_stamina,
                "attack": self.attack,
                "defense": self.defense,
                "speed": self.speed,
                "magic": self.magic,
            },
            "status": {
                "hunger": self.hunger,
                "happiness": self.happiness,
                "energy": self.energy,
            },
            "position": {
                "x": self.position_x,
                "y": self.position_y,
                "z": self.position_z,
            },
            "skills": self.skills,
            "active_buffs": self.active_buffs,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_active": self.last_active.isoformat() if self.last_active else None,
        }
