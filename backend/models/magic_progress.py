"""
Magic School Progress Model
Database model for Magic Schools System (Skyrim-style learning by doing)
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class MagicSchoolProgress(Base):
    """Magic School Progress (Skyrim-style)"""

    __tablename__ = "magic_school_progress"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Player
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # School
    school = Column(String(20), nullable=False)  # feuer, eis, blitz, wasser, erde, wind, licht, dunkelheit, explosion

    # Progress
    level = Column(Integer, default=1)
    xp = Column(Float, default=0.0)
    xp_required = Column(Float, default=100.0)

    # Unlocked Content
    unlocked_spells = Column(JSON, default=list)  # List of spell IDs

    # Stats
    total_casts = Column(Integer, default=0)
    total_damage = Column(Float, default=0.0)
    perfect_casts = Column(Integer, default=0)

    # Weaving (Combo Magic)
    can_weave = Column(Boolean, default=False)  # Level 20+ required
    weave_combinations_unlocked = Column(JSON, default=list)  # List of school pair strings

    # Timestamps
    first_cast = Column(DateTime, default=datetime.utcnow)
    last_cast = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="magic_progress")

    def __repr__(self):
        return f"<MagicSchoolProgress(player_id={self.player_id}, school='{self.school}', level={self.level})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "player_id": self.player_id,
            "school": self.school,
            "level": self.level,
            "xp": self.xp,
            "xp_required": self.xp_required,
            "progress_percentage": (self.xp / self.xp_required * 100) if self.xp_required > 0 else 0.0,
            "unlocked_spells": self.unlocked_spells,
            "stats": {
                "total_casts": self.total_casts,
                "total_damage": self.total_damage,
                "perfect_casts": self.perfect_casts,
                "accuracy": (self.perfect_casts / self.total_casts * 100) if self.total_casts > 0 else 0.0,
            },
            "weaving": {
                "unlocked": self.can_weave,
                "combinations": self.weave_combinations_unlocked,
            },
            "first_cast": self.first_cast.isoformat() if self.first_cast else None,
            "last_cast": self.last_cast.isoformat() if self.last_cast else None,
        }


class RegionBoss(Base):
    """Region Boss (Gebietsherrscher)"""

    __tablename__ = "region_bosses"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Region
    region = Column(String(50), unique=True, nullable=False, index=True)

    # Current Boss
    boss_player_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    boss_name = Column(String(100), nullable=True)

    # Control Data
    conquest_path = Column(String(20), nullable=True)  # "krieg", "handel", "diplomatie", "quest_line"
    control_started = Column(DateTime, nullable=True)
    tax_rate = Column(Float, default=5.0)  # 5-10%

    # Challenge Data
    active_challenge_id = Column(Integer, nullable=True)
    challenge_count = Column(Integer, default=0)

    # Timestamps
    last_conquest = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    boss_player = relationship("User", back_populates="controlled_regions")

    def __repr__(self):
        return f"<RegionBoss(region='{self.region}', boss_player_id={self.boss_player_id})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "region": self.region,
            "boss_player_id": self.boss_player_id,
            "boss_name": self.boss_name,
            "conquest_path": self.conquest_path,
            "control_started": self.control_started.isoformat() if self.control_started else None,
            "tax_rate": self.tax_rate,
            "active_challenge_id": self.active_challenge_id,
            "challenge_count": self.challenge_count,
        }


class Challenge(Base):
    """Region Boss Challenge"""

    __tablename__ = "challenges"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, unique=True, index=True)

    # Challenge Data
    challenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    region = Column(String(50), nullable=False)
    challenge_type = Column(String(20), nullable=False)  # "krieg", "handel", "diplomatie", "quest_line"

    # Status
    status = Column(String(20), default="pending")  # "pending", "active", "completed", "cancelled"
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Stakes
    stakes = Column(JSON, default=dict)
    conditions = Column(JSON, default=dict)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    challenger = relationship("User", foreign_keys=[challenger_id], backref="challenges_created")
    winner = relationship("User", foreign_keys=[winner_id], backref="challenges_won")

    def __repr__(self):
        return f"<Challenge(id={self.challenge_id}, region='{self.region}', type='{self.challenge_type}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "challenge_id": self.challenge_id,
            "challenger_id": self.challenger_id,
            "region": self.region,
            "challenge_type": self.challenge_type,
            "status": self.status,
            "winner_id": self.winner_id,
            "stakes": self.stakes,
            "conditions": self.conditions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "accepted_at": self.accepted_at.isoformat() if self.accepted_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
