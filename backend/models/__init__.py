"""
Najika Backend Models
SQLAlchemy ORM models for database tables
"""

from backend.models.user import User
from backend.models.character import Character
from backend.models.inventory import InventoryItem, Equipment
from backend.models.training import TrainingJob, TrainingProgress
from backend.models.slime_companion import SlimeCompanion
from backend.models.pvp_battle import PvPBattle, PvPStats
from backend.models.arena_monster import ArenaMonster, Finisher
from backend.models.magic_progress import MagicSchoolProgress, RegionBoss, Challenge

__all__ = [
    "User",
    "Character",
    "InventoryItem",
    "Equipment",
    "TrainingJob",
    "TrainingProgress",
    "SlimeCompanion",
    "PvPBattle",
    "PvPStats",
    "ArenaMonster",
    "Finisher",
    "MagicSchoolProgress",
    "RegionBoss",
    "Challenge",
]
