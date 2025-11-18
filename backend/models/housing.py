"""
Housing & Farming Models - Najika World
Schwarze Mühle Living Quarters System
"""

from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class PlayerHouse(Base):
    """Player's house in Schwarze Mühle"""
    __tablename__ = "player_houses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Location
    region = Column(String(50), default="schwarze_muehle")  # schwarze_muehle, heisse_duenen, etc.
    house_type = Column(String(50), default="mühle_room")  # Room type

    # House State
    furniture = Column(JSON, default=list)  # [{"type": "bed", "position": {"x": 5, "y": 3, "z": 0}, "rotation": 0}, ...]
    decorations = Column(JSON, default=list)  # Wall decorations, paintings, etc.

    # Upgrades
    level = Column(Integer, default=1)
    max_furniture = Column(Integer, default=20)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="player_house")
    farm_plots = relationship("FarmPlot", back_populates="house", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "region": self.region,
            "house_type": self.house_type,
            "furniture": self.furniture or [],
            "decorations": self.decorations or [],
            "level": self.level,
            "max_furniture": self.max_furniture,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class FarmPlot(Base):
    """Farm plot with crops"""
    __tablename__ = "farm_plots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    house_id = Column(Integer, ForeignKey('player_houses.id'), nullable=False)

    # Position
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    position_z = Column(Float, default=0.0)

    # Crop
    crop_type = Column(String(50), nullable=True)  # "wheat", "carrot", "fire_flower", null if empty
    planted_at = Column(DateTime, nullable=True)
    growth_stage = Column(Integer, default=0)  # 0-4 (4 = ready)
    ready_to_harvest = Column(Boolean, default=False)

    # Growth time in seconds (varies by crop)
    growth_time = Column(Integer, default=300)  # 5 minutes default

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="farm_plots")
    house = relationship("PlayerHouse", back_populates="farm_plots")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "house_id": self.house_id,
            "position": {
                "x": self.position_x,
                "y": self.position_y,
                "z": self.position_z
            },
            "crop_type": self.crop_type,
            "planted_at": self.planted_at.isoformat() if self.planted_at else None,
            "growth_stage": self.growth_stage,
            "ready_to_harvest": self.ready_to_harvest,
            "growth_time": self.growth_time,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class FishingSpot(Base):
    """Fishing spots in world regions"""
    __tablename__ = "fishing_spots"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(50), nullable=False)

    # Position
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    position_z = Column(Float, default=0.0)

    # Fish available
    fish_pool = Column(JSON, default=list)  # ["carp", "salmon", "lava_fish"]
    rarity_weights = Column(JSON, default=dict)  # {"common": 0.7, "rare": 0.25, "legendary": 0.05}

    # Spot properties
    spot_type = Column(String(50), default="pond")  # pond, river, ocean, lava
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "region": self.region,
            "position": {
                "x": self.position_x,
                "y": self.position_y,
                "z": self.position_z
            },
            "fish_pool": self.fish_pool or [],
            "rarity_weights": self.rarity_weights or {},
            "spot_type": self.spot_type,
            "is_active": self.is_active
        }
