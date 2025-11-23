"""
Card Game Models - Najika World
Triple Triad Card Game with Hearthstone-style Stone Visuals
Fantasy-Western Setting
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Card(Base):
    """Card definition (static card pool)"""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(100), nullable=False, unique=True)
    card_type = Column(String(20), nullable=False)  # minion, spell, weapon
    faction = Column(String(50), nullable=False)  # fire_gunslingers, ice_mages, etc.
    rarity = Column(String(20), nullable=False)  # common, uncommon, rare, epic, legendary

    # Triple Triad Stats
    top_value = Column(Integer, default=1)  # 1-10
    right_value = Column(Integer, default=1)
    bottom_value = Column(Integer, default=1)
    left_value = Column(Integer, default=1)

    # Hearthstone Stats
    mana_cost = Column(Integer, default=1)  # 0-10
    attack = Column(Integer, default=1)  # For minions
    health = Column(Integer, default=1)  # For minions
    durability = Column(Integer, default=3)  # For weapons

    # Card Effects
    effect_type = Column(String(50), nullable=True)  # battlecry, deathrattle, taunt, etc.
    effect_description = Column(Text, nullable=True)
    effect_script = Column(JSON, nullable=True)  # Script for effect logic

    # Visual
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    # Unlock Requirements
    unlock_level = Column(Integer, default=1)
    unlock_quest_id = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.card_type,
            "faction": self.faction,
            "rarity": self.rarity,
            "triad_values": {
                "top": self.top_value,
                "right": self.right_value,
                "bottom": self.bottom_value,
                "left": self.left_value
            },
            "hearthstone_stats": {
                "mana": self.mana_cost,
                "attack": self.attack,
                "health": self.health,
                "durability": self.durability
            },
            "effect": {
                "type": self.effect_type,
                "description": self.effect_description,
                "script": self.effect_script
            },
            "image_url": self.image_url,
            "description": self.description,
            "unlock_level": self.unlock_level
        }


class PlayerCardCollection(Base):
    """Player's owned cards"""
    __tablename__ = "player_card_collections"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)

    # Ownership
    copies_owned = Column(Integer, default=1)  # Can have multiple copies
    is_golden = Column(Boolean, default=False)  # Premium version

    # Stats
    times_played = Column(Integer, default=0)
    times_won_with = Column(Integer, default=0)

    # Timestamps
    acquired_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="card_collection")
    card = relationship("Card")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "card_id": self.card_id,
            "copies_owned": self.copies_owned,
            "is_golden": self.is_golden,
            "times_played": self.times_played,
            "times_won_with": self.times_won_with,
            "acquired_at": self.acquired_at.isoformat() if self.acquired_at else None
        }


class PlayerDeck(Base):
    """Player's card decks (30 cards)"""
    __tablename__ = "player_decks"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Deck Info
    deck_name = Column(String(100), nullable=False)
    faction = Column(String(50), nullable=False)  # Primary faction
    is_active = Column(Boolean, default=False)  # Currently selected deck

    # Card List (JSON: {card_id: count})
    cards = Column(JSON, nullable=False)  # {"1": 2, "5": 1, "12": 2, ...} (30 total)

    # Stats
    total_games = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="card_decks")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "deck_name": self.deck_name,
            "faction": self.faction,
            "is_active": self.is_active,
            "cards": self.cards or {},
            "total_games": self.total_games,
            "total_wins": self.total_wins,
            "win_rate": self.win_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class CardGameMatch(Base):
    """Card game match history"""
    __tablename__ = "card_game_matches"

    id = Column(Integer, primary_key=True, index=True)

    # Players
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null if vs NPC

    # Match Settings
    game_mode = Column(String(20), nullable=False)  # Only 'triad' supported
    is_ranked = Column(Boolean, default=False)
    is_vs_npc = Column(Boolean, default=False)
    npc_name = Column(String(100), nullable=True)

    # Decks Used
    player1_deck_id = Column(Integer, ForeignKey("player_decks.id"))
    player2_deck_id = Column(Integer, ForeignKey("player_decks.id"), nullable=True)

    # Result
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    turns_played = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)

    # Final Board State (for Triple Triad mode)
    final_board = Column(JSON, nullable=True)  # 3x3 grid

    # Rewards
    gold_earned = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    cards_won = Column(JSON, nullable=True)  # List of card IDs won

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "game_mode": self.game_mode,
            "is_ranked": self.is_ranked,
            "is_vs_npc": self.is_vs_npc,
            "npc_name": self.npc_name,
            "winner_id": self.winner_id,
            "turns_played": self.turns_played,
            "duration_seconds": self.duration_seconds,
            "final_board": self.final_board,
            "gold_earned": self.gold_earned,
            "xp_earned": self.xp_earned,
            "cards_won": self.cards_won or [],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None
        }


class CardGameRanking(Base):
    """Player rankings for card game"""
    __tablename__ = "card_game_rankings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Rankings
    elo_rating = Column(Integer, default=1000)  # ELO rating
    rank_tier = Column(String(20), default="bronze")  # bronze, silver, gold, platinum, diamond, legend

    # Stats
    ranked_wins = Column(Integer, default=0)
    ranked_losses = Column(Integer, default=0)
    ranked_draws = Column(Integer, default=0)
    win_streak = Column(Integer, default=0)
    best_win_streak = Column(Integer, default=0)

    # Season
    season = Column(Integer, default=1)
    season_high_rank = Column(String(20), default="bronze")

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="card_game_ranking")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "elo_rating": self.elo_rating,
            "rank_tier": self.rank_tier,
            "ranked_wins": self.ranked_wins,
            "ranked_losses": self.ranked_losses,
            "ranked_draws": self.ranked_draws,
            "win_streak": self.win_streak,
            "best_win_streak": self.best_win_streak,
            "season": self.season,
            "season_high_rank": self.season_high_rank,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
