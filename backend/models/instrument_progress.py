"""
Instrument Progress Models - Najika World
Database models for instrument playing system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class InstrumentProgress(Base):
    """Player progress per instrument"""
    __tablename__ = "instrument_progress"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Current Instrument
    current_instrument = Column(String(50), default="mundharmonika")  # InstrumentType

    # Skill Levels per Instrument (JSON: {instrument_name: level})
    instrument_skills = Column(JSON, default={})  # {"mundharmonika": 5, "gitarre": 12, ...}

    # Experience per Instrument (JSON: {instrument_name: xp})
    instrument_experience = Column(JSON, default={})  # {"mundharmonika": 1500, ...}

    # Learned Songs (List of song IDs)
    learned_songs = Column(JSON, default=[])  # [1, 5, 7, 12]

    # Statistics
    total_notes_played = Column(Integer, default=0)
    perfect_notes = Column(Integer, default=0)
    great_notes = Column(Integer, default=0)
    good_notes = Column(Integer, default=0)

    # Play Session
    session_start = Column(DateTime, nullable=True)
    last_played = Column(DateTime, default=datetime.utcnow)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="instrument_progress")
    played_notes = relationship("PlayedNote", back_populates="progress", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "current_instrument": self.current_instrument,
            "instrument_skills": self.instrument_skills or {},
            "instrument_experience": self.instrument_experience or {},
            "learned_songs": self.learned_songs or [],
            "total_notes_played": self.total_notes_played,
            "perfect_notes": self.perfect_notes,
            "great_notes": self.great_notes,
            "good_notes": self.good_notes,
            "session_start": self.session_start.isoformat() if self.session_start else None,
            "last_played": self.last_played.isoformat() if self.last_played else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class PlayedNote(Base):
    """Log of played notes (for statistics)"""
    __tablename__ = "played_notes"

    id = Column(Integer, primary_key=True, index=True)
    progress_id = Column(Integer, ForeignKey("instrument_progress.id"), nullable=False)

    # Note Details
    instrument = Column(String(50), nullable=False)  # InstrumentType
    note = Column(String(3), nullable=False)  # C, D#, E, etc.
    octave = Column(Integer, nullable=False)  # 1-8
    duration = Column(Float, default=0.5)  # seconds
    velocity = Column(Float, default=0.8)  # 0.0-1.0

    # Quality
    quality = Column(String(20), nullable=False)  # perfect, great, good, ok, poor, miss
    accuracy = Column(Float, default=0.0)  # 0.0-1.0

    # Timestamp
    played_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    progress = relationship("InstrumentProgress", back_populates="played_notes")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "progress_id": self.progress_id,
            "instrument": self.instrument,
            "note": self.note,
            "octave": self.octave,
            "duration": self.duration,
            "velocity": self.velocity,
            "quality": self.quality,
            "accuracy": self.accuracy,
            "played_at": self.played_at.isoformat() if self.played_at else None,
        }


class LearnedSong(Base):
    """Songs learned by player"""
    __tablename__ = "learned_songs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Song Info
    song_id = Column(String(100), nullable=False)  # "zelda_song_of_time"
    song_name = Column(String(200), nullable=False)
    difficulty = Column(Integer, default=1)  # 1-5

    # Progress
    times_played = Column(Integer, default=0)
    best_score = Column(Float, default=0.0)  # 0.0-1.0 (percentage)
    completed = Column(Boolean, default=False)

    # Timestamps
    learned_at = Column(DateTime, default=datetime.utcnow)
    last_played = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("User")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "song_id": self.song_id,
            "song_name": self.song_name,
            "difficulty": self.difficulty,
            "times_played": self.times_played,
            "best_score": self.best_score,
            "completed": self.completed,
            "learned_at": self.learned_at.isoformat() if self.learned_at else None,
            "last_played": self.last_played.isoformat() if self.last_played else None,
        }
