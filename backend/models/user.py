"""
User Model
Database model for user accounts and authentication
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class User(Base):
    """User account model"""

    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Authentication
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)

    # Profile
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)

    # Permissions
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    characters = relationship("Character", back_populates="user", cascade="all, delete-orphan")
    training_jobs = relationship("TrainingJob", back_populates="user", cascade="all, delete-orphan")
    slime_companions = relationship("SlimeCompanion", back_populates="owner", cascade="all, delete-orphan")
    pvp_stats = relationship("PvPStats", back_populates="player", uselist=False, cascade="all, delete-orphan")
    magic_progress = relationship("MagicSchoolProgress", back_populates="player", cascade="all, delete-orphan")

    # Instrument System
    instrument_progress = relationship("InstrumentProgress", back_populates="player", uselist=False, cascade="all, delete-orphan")

    # Oregon Trail
    oregon_journeys = relationship("OregonTrailJourney", back_populates="player", cascade="all, delete-orphan")

    # Boss Spawns
    boss_spawn_defeats = relationship("BossSpawnDefeat", back_populates="player", cascade="all, delete-orphan")

    # World State
    world_state = relationship("PlayerWorldState", back_populates="player", uselist=False, cascade="all, delete-orphan")

    # Voice System
    voice_calls = relationship("VoiceCall", back_populates="player", cascade="all, delete-orphan")
    voice_settings = relationship("VoiceSettings", back_populates="player", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

    def to_dict(self):
        """Convert to dictionary (excluding password)"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
