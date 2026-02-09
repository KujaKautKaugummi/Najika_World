"""
Multiplayer Session Models - Najika World
Database models for multiplayer system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class MultiplayerSession(Base):
    """Multiplayer game sessions"""
    __tablename__ = "multiplayer_sessions"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Session Info
    session_name = Column(String(200), nullable=False)
    session_code = Column(String(20), unique=True, nullable=False)  # Join code

    # Status
    active = Column(Boolean, default=True)
    started = Column(Boolean, default=False)
    ended = Column(Boolean, default=False)

    # Settings
    max_players = Column(Integer, default=4)
    current_players = Column(Integer, default=1)
    is_public = Column(Boolean, default=False)
    password_protected = Column(Boolean, default=False)
    password_hash = Column(String(200), nullable=True)

    # Game Mode
    game_mode = Column(String(50), default="coop")  # coop, pvp, raid, dungeon
    difficulty = Column(String(20), default="normal")  # easy, normal, hard, hardcore

    # Region
    current_region = Column(String(100), nullable=True)
    current_activity = Column(String(100), nullable=True)  # "boss_fight", "dungeon", etc.

    # Progress
    objectives_completed = Column(Integer, default=0)
    total_objectives = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, default=datetime.utcnow)

    # Relationships
    host = relationship("User")
    participants = relationship("SessionParticipant", back_populates="session", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "host_id": self.host_id,
            "session_name": self.session_name,
            "session_code": self.session_code,
            "active": self.active,
            "started": self.started,
            "ended": self.ended,
            "max_players": self.max_players,
            "current_players": self.current_players,
            "is_public": self.is_public,
            "password_protected": self.password_protected,
            "game_mode": self.game_mode,
            "difficulty": self.difficulty,
            "current_region": self.current_region,
            "current_activity": self.current_activity,
            "objectives_completed": self.objectives_completed,
            "total_objectives": self.total_objectives,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
        }


class SessionParticipant(Base):
    """Participants in multiplayer sessions"""
    __tablename__ = "session_participants"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("multiplayer_sessions.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Status
    connected = Column(Boolean, default=True)
    ready = Column(Boolean, default=False)

    # Role
    role = Column(String(50), default="member")  # host, member, spectator

    # Stats (session-specific)
    damage_dealt = Column(Integer, default=0)
    healing_done = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    kills = Column(Integer, default=0)

    # Connection
    connection_quality = Column(String(20), default="good")  # poor, good, excellent
    latency_ms = Column(Integer, default=0)

    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow)
    left_at = Column(DateTime, nullable=True)

    # Relationships
    session = relationship("MultiplayerSession", back_populates="participants")
    player = relationship("User")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "player_id": self.player_id,
            "connected": self.connected,
            "ready": self.ready,
            "role": self.role,
            "damage_dealt": self.damage_dealt,
            "healing_done": self.healing_done,
            "deaths": self.deaths,
            "kills": self.kills,
            "connection_quality": self.connection_quality,
            "latency_ms": self.latency_ms,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "left_at": self.left_at.isoformat() if self.left_at else None,
        }
