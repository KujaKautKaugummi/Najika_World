"""
Voice Settings Models - Najika World
Database models for user voice settings
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base


class VoiceSettings(Base):
    """User voice settings"""
    __tablename__ = "voice_settings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # TTS Settings
    tts_voice = Column(String(50), default="megumin")
    tts_speed = Column(Float, default=1.0)
    tts_pitch = Column(Float, default=1.0)
    tts_volume = Column(Float, default=1.0)

    # STT Settings
    stt_language = Column(String(10), default="de")
    stt_auto_detect = Column(Boolean, default=True)

    # Preferences
    voice_enabled = Column(Boolean, default=True)
    auto_play_response = Column(Boolean, default=True)

    # Relationships
    player = relationship("User", back_populates="voice_settings")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "tts_voice": self.tts_voice,
            "tts_speed": self.tts_speed,
            "tts_pitch": self.tts_pitch,
            "tts_volume": self.tts_volume,
            "stt_language": self.stt_language,
            "stt_auto_detect": self.stt_auto_detect,
            "voice_enabled": self.voice_enabled,
            "auto_play_response": self.auto_play_response,
        }
