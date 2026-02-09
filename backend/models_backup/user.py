"""
User Model - Minimal for Card Game Testing
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class User(Base):
    """Minimal User model for card game system"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships for Card Game
    card_collection = relationship("PlayerCardCollection", back_populates="player")
    card_decks = relationship("PlayerDeck", back_populates="player")
    card_game_ranking = relationship("CardGameRanking", back_populates="player", uselist=False)

    # Relationships for Dice Monsters
    dice_collection = relationship("PlayerDiceCollection", back_populates="player")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
