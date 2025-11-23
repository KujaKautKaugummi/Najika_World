"""
Voice Call Models - Najika World
Database models for voice call system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class VoiceCall(Base):
    """Voice call sessions"""
    __tablename__ = "voice_calls"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Call Status
    active = Column(Boolean, default=True)
    ended = Column(Boolean, default=False)

    # Call Details
    call_type = Column(String(50), default="najika")  # najika, player-to-player, group
    target_id = Column(Integer, nullable=True)  # Target player ID (if p2p)

    # Audio Stats
    duration_seconds = Column(Integer, default=0)
    audio_quality = Column(String(20), default="good")  # poor, good, excellent

    # Transcription Stats
    messages_sent = Column(Integer, default=0)
    messages_received = Column(Integer, default=0)
    words_spoken = Column(Integer, default=0)

    # Cost
    cost_credits = Column(Integer, default=0)  # If voice calls cost credits

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    player = relationship("User", back_populates="voice_calls")
    messages = relationship("VoiceMessage", back_populates="call", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "active": self.active,
            "ended": self.ended,
            "call_type": self.call_type,
            "target_id": self.target_id,
            "duration_seconds": self.duration_seconds,
            "audio_quality": self.audio_quality,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "words_spoken": self.words_spoken,
            "cost_credits": self.cost_credits,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
        }


class VoiceMessage(Base):
    """Transcribed voice messages"""
    __tablename__ = "voice_messages"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("voice_calls.id"), nullable=False)

    # Message Details
    sender = Column(String(50), nullable=False)  # "player", "najika", "other_player"
    sender_id = Column(Integer, nullable=True)  # Player ID if player message

    # Audio
    audio_duration = Column(Float, default=0.0)  # seconds
    audio_file_path = Column(String(500), nullable=True)  # Path to audio file

    # Transcription (Whisper STT)
    transcription = Column(Text, nullable=False)
    confidence = Column(Float, default=0.0)  # 0.0-1.0
    language = Column(String(10), default="de")  # de, en, ja, etc.

    # AI Response (if Najika)
    ai_response = Column(Text, nullable=True)
    ai_response_audio = Column(String(500), nullable=True)  # Path to TTS audio

    # Sentiment
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative
    emotion = Column(String(50), nullable=True)  # happy, sad, angry, etc.

    # Timestamp
    sent_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    call = relationship("VoiceCall", back_populates="messages")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "call_id": self.call_id,
            "sender": self.sender,
            "sender_id": self.sender_id,
            "audio_duration": self.audio_duration,
            "audio_file_path": self.audio_file_path,
            "transcription": self.transcription,
            "confidence": self.confidence,
            "language": self.language,
            "ai_response": self.ai_response,
            "ai_response_audio": self.ai_response_audio,
            "sentiment": self.sentiment,
            "emotion": self.emotion,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
        }
