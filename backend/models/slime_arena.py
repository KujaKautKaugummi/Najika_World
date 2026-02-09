"""
Slime Arena Models - Najika World
Combat system for slime companions with tournament support
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class SlimeDuel(Base):
    """Individual slime duel records"""
    __tablename__ = "slime_duels"

    id = Column(Integer, primary_key=True, index=True)

    # Player info
    player_id = Column(String(100), nullable=False, index=True)
    player_slime_name = Column(String(100), nullable=False)
    player_slime_type = Column(String(50), nullable=False)  # bubble, molten, crystal, shadow, etc.

    # Opponent info
    opponent_type = Column(String(20), nullable=False)  # 'npc' or 'player'
    opponent_id = Column(String(100), nullable=True)  # Player ID if PvP
    opponent_slime_name = Column(String(100), nullable=False)
    opponent_slime_type = Column(String(50), nullable=False)

    # Game mode
    game_mode = Column(String(20), nullable=False)  # 'normal', 'finisher', 'tournament'
    combat_mode = Column(String(20), nullable=False)  # 'auto', 'manual', 'cheer'

    # Battle stats
    rounds_total = Column(Integer, default=0)
    player_hp_start = Column(Integer, default=100)
    player_hp_end = Column(Integer, default=0)
    opponent_hp_start = Column(Integer, default=100)
    opponent_hp_end = Column(Integer, default=0)

    # Results
    winner = Column(String(20), nullable=False)  # 'player' or 'opponent'
    finisher_used = Column(String(100), nullable=True)  # Name of finisher move
    finisher_success = Column(Boolean, default=False)

    # Rewards
    gold_earned = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    fame_earned = Column(Integer, default=0)

    # Combat log
    action_log = Column(JSON, nullable=True)  # Detailed turn-by-turn log

    # Tournament reference
    tournament_id = Column(Integer, ForeignKey('slime_tournaments.id'), nullable=True)
    tournament_round = Column(Integer, nullable=True)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    # Relationships
    tournament = relationship("SlimeTournament", back_populates="duels")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player": {
                "id": self.player_id,
                "slime_name": self.player_slime_name,
                "slime_type": self.player_slime_type,
                "hp_start": self.player_hp_start,
                "hp_end": self.player_hp_end
            },
            "opponent": {
                "type": self.opponent_type,
                "id": self.opponent_id,
                "slime_name": self.opponent_slime_name,
                "slime_type": self.opponent_slime_type,
                "hp_start": self.opponent_hp_start,
                "hp_end": self.opponent_hp_end
            },
            "game_mode": self.game_mode,
            "combat_mode": self.combat_mode,
            "rounds_total": self.rounds_total,
            "winner": self.winner,
            "finisher": {
                "used": self.finisher_used,
                "success": self.finisher_success
            },
            "rewards": {
                "gold": self.gold_earned,
                "xp": self.xp_earned,
                "fame": self.fame_earned
            },
            "tournament_id": self.tournament_id,
            "tournament_round": self.tournament_round,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None
        }


class SlimeTournament(Base):
    """Tournament brackets and status"""
    __tablename__ = "slime_tournaments"

    id = Column(Integer, primary_key=True, index=True)

    # Tournament info
    name = Column(String(200), nullable=False)
    status = Column(String(20), nullable=False, default='registration')  # registration, in_progress, completed
    format = Column(String(20), nullable=False, default='single_elimination')
    max_participants = Column(Integer, default=16)
    entry_fee = Column(Integer, default=500)

    # Bracket data
    bracket_data = Column(JSON, nullable=True)  # Complete bracket structure
    current_round = Column(Integer, default=1)

    # Prize pool
    first_place_gold = Column(Integer, default=5000)
    second_place_gold = Column(Integer, default=2000)
    third_place_gold = Column(Integer, default=1000)
    first_place_fame = Column(Integer, default=100)

    # Participants
    participants = Column(JSON, nullable=False)  # List of player IDs and slimes

    # Schedule
    registration_opens = Column(DateTime, nullable=False)
    registration_closes = Column(DateTime, nullable=False)
    tournament_starts = Column(DateTime, nullable=False)
    tournament_ends = Column(DateTime, nullable=True)

    # Winner
    winner_id = Column(String(100), nullable=True)
    winner_slime_name = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    duels = relationship("SlimeDuel", back_populates="tournament")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "format": self.format,
            "max_participants": self.max_participants,
            "entry_fee": self.entry_fee,
            "current_round": self.current_round,
            "bracket_data": self.bracket_data,
            "prizes": {
                "first": {"gold": self.first_place_gold, "fame": self.first_place_fame},
                "second": {"gold": self.second_place_gold},
                "third": {"gold": self.third_place_gold}
            },
            "participants": self.participants,
            "schedule": {
                "registration_opens": self.registration_opens.isoformat() if self.registration_opens else None,
                "registration_closes": self.registration_closes.isoformat() if self.registration_closes else None,
                "tournament_starts": self.tournament_starts.isoformat() if self.tournament_starts else None,
                "tournament_ends": self.tournament_ends.isoformat() if self.tournament_ends else None
            },
            "winner": {
                "player_id": self.winner_id,
                "slime_name": self.winner_slime_name
            } if self.winner_id else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class SlimeFame(Base):
    """Player fame/reputation in slime arena"""
    __tablename__ = "slime_fame"

    id = Column(Integer, primary_key=True, index=True)

    # Player info
    player_id = Column(String(100), nullable=False, unique=True, index=True)

    # Fame stats
    fame_points = Column(Integer, default=0)
    fame_title = Column(String(100), default="Anfänger")  # Anfänger, Kämpfer, Veteran, Champion, Legende

    # Battle statistics
    total_duels = Column(Integer, default=0)
    duels_won = Column(Integer, default=0)
    duels_lost = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)

    # Finisher statistics
    finishers_attempted = Column(Integer, default=0)
    finishers_successful = Column(Integer, default=0)
    finisher_success_rate = Column(Float, default=0.0)

    # Tournament statistics
    tournaments_entered = Column(Integer, default=0)
    tournaments_won = Column(Integer, default=0)
    tournament_best_placement = Column(Integer, nullable=True)

    # Rewards totals
    total_gold_earned = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)

    # Current streak
    current_win_streak = Column(Integer, default=0)
    best_win_streak = Column(Integer, default=0)

    # Rankings
    global_rank = Column(Integer, nullable=True)
    regional_rank = Column(Integer, nullable=True)

    # Unlocks
    unlocked_titles = Column(JSON, default=list)  # List of earned titles
    unlocked_finishers = Column(JSON, default=list)  # List of unlocked finisher moves

    # Timestamps
    first_duel = Column(DateTime, nullable=True)
    last_duel = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "fame": {
                "points": self.fame_points,
                "title": self.fame_title,
                "unlocked_titles": self.unlocked_titles or []
            },
            "statistics": {
                "total_duels": self.total_duels,
                "won": self.duels_won,
                "lost": self.duels_lost,
                "win_rate": round(self.win_rate, 2)
            },
            "finishers": {
                "attempted": self.finishers_attempted,
                "successful": self.finishers_successful,
                "success_rate": round(self.finisher_success_rate, 2),
                "unlocked": self.unlocked_finishers or []
            },
            "tournaments": {
                "entered": self.tournaments_entered,
                "won": self.tournaments_won,
                "best_placement": self.tournament_best_placement
            },
            "streaks": {
                "current": self.current_win_streak,
                "best": self.best_win_streak
            },
            "rankings": {
                "global": self.global_rank,
                "regional": self.regional_rank
            },
            "totals": {
                "gold": self.total_gold_earned,
                "xp": self.total_xp_earned
            },
            "first_duel": self.first_duel.isoformat() if self.first_duel else None,
            "last_duel": self.last_duel.isoformat() if self.last_duel else None
        }

    def calculate_title(self):
        """Calculate title based on fame points"""
        if self.fame_points >= 10000:
            return "Legende"
        elif self.fame_points >= 5000:
            return "Champion"
        elif self.fame_points >= 2000:
            return "Veteran"
        elif self.fame_points >= 500:
            return "Kämpfer"
        else:
            return "Anfänger"

    def update_stats(self, duel_won, fame_earned, finisher_used=False, finisher_success=False):
        """Update statistics after a duel"""
        self.total_duels += 1

        if duel_won:
            self.duels_won += 1
            self.current_win_streak += 1
            if self.current_win_streak > self.best_win_streak:
                self.best_win_streak = self.current_win_streak
        else:
            self.duels_lost += 1
            self.current_win_streak = 0

        self.win_rate = (self.duels_won / self.total_duels) * 100 if self.total_duels > 0 else 0

        if finisher_used:
            self.finishers_attempted += 1
            if finisher_success:
                self.finishers_successful += 1

        self.finisher_success_rate = (self.finishers_successful / self.finishers_attempted) * 100 if self.finishers_attempted > 0 else 0

        self.fame_points += fame_earned
        self.fame_title = self.calculate_title()

        self.last_duel = datetime.utcnow()
        if not self.first_duel:
            self.first_duel = datetime.utcnow()
