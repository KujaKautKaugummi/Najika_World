"""
PvP Battle Model
Database model for PvP System (Hardcore, Normal, Softy)
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class PvPBattle(Base):
    """PvP Battle record"""

    __tablename__ = "pvp_battles"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    battle_id = Column(Integer, unique=True, index=True)

    # Players
    attacker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    defender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Mode
    mode = Column(String(20), nullable=False)  # "hardcore", "normal", "softy"

    # Status
    status = Column(String(20), default="active")  # "active", "completed", "mercy", "cancelled"

    # Battle Data
    battle_duration = Column(Float, default=0.0)  # seconds
    damage_dealt_attacker = Column(Float, default=0.0)
    damage_dealt_defender = Column(Float, default=0.0)

    # Mercy Decision (Hardcore only)
    mercy_offered = Column(Boolean, default=False)
    mercy_accepted = Column(Boolean, nullable=True)
    items_lost = Column(JSON, default=list)  # List of item dicts

    # Item Loss (Normal mode)
    item_lost_normal = Column(JSON, nullable=True)  # Single item dict

    # Rating Changes (Softy mode)
    rating_change_attacker = Column(Integer, default=0)
    rating_change_defender = Column(Integer, default=0)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    attacker = relationship("User", foreign_keys=[attacker_id], backref="pvp_battles_as_attacker")
    defender = relationship("User", foreign_keys=[defender_id], backref="pvp_battles_as_defender")
    winner = relationship("User", foreign_keys=[winner_id], backref="pvp_battles_won")

    def __repr__(self):
        return f"<PvPBattle(id={self.battle_id}, mode='{self.mode}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "battle_id": self.battle_id,
            "attacker_id": self.attacker_id,
            "defender_id": self.defender_id,
            "winner_id": self.winner_id,
            "mode": self.mode,
            "status": self.status,
            "battle_duration": self.battle_duration,
            "damage_dealt": {
                "attacker": self.damage_dealt_attacker,
                "defender": self.damage_dealt_defender,
            },
            "mercy": {
                "offered": self.mercy_offered,
                "accepted": self.mercy_accepted,
                "items_lost": self.items_lost,
            },
            "item_lost_normal": self.item_lost_normal,
            "rating_changes": {
                "attacker": self.rating_change_attacker,
                "defender": self.rating_change_defender,
            },
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
        }


class PvPStats(Base):
    """Player PvP Statistics"""

    __tablename__ = "pvp_stats"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Overall Stats
    total_battles = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)

    # Mode-specific Stats
    hardcore_wins = Column(Integer, default=0)
    hardcore_losses = Column(Integer, default=0)
    normal_wins = Column(Integer, default=0)
    normal_losses = Column(Integer, default=0)
    softy_wins = Column(Integer, default=0)
    softy_losses = Column(Integer, default=0)

    # Mercy Stats
    mercy_count_7d = Column(Integer, default=0)  # Last 7 days
    mercy_total = Column(Integer, default=0)
    pvp_cooldown_until = Column(DateTime, nullable=True)

    # Rating (Softy mode)
    rating = Column(Integer, default=1000)

    # Kill Streak
    kill_streak = Column(Integer, default=0)
    best_kill_streak = Column(Integer, default=0)

    # Timestamps
    last_battle = Column(DateTime, nullable=True)
    last_mercy = Column(DateTime, nullable=True)

    # Relationships
    player = relationship("User", back_populates="pvp_stats")

    def __repr__(self):
        return f"<PvPStats(player_id={self.player_id}, wins={self.total_wins}, losses={self.total_losses})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "player_id": self.player_id,
            "total_battles": self.total_battles,
            "total_wins": self.total_wins,
            "total_losses": self.total_losses,
            "win_rate": (self.total_wins / self.total_battles * 100) if self.total_battles > 0 else 0.0,
            "modes": {
                "hardcore": {"wins": self.hardcore_wins, "losses": self.hardcore_losses},
                "normal": {"wins": self.normal_wins, "losses": self.normal_losses},
                "softy": {"wins": self.softy_wins, "losses": self.softy_losses},
            },
            "mercy": {
                "count_7d": self.mercy_count_7d,
                "total": self.mercy_total,
                "cooldown_until": self.pvp_cooldown_until.isoformat() if self.pvp_cooldown_until else None,
            },
            "rating": self.rating,
            "kill_streak": self.kill_streak,
            "best_kill_streak": self.best_kill_streak,
            "last_battle": self.last_battle.isoformat() if self.last_battle else None,
        }
