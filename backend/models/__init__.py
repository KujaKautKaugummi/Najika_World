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
from backend.models.magic_progress import MagicSchoolProgress
from backend.models.instrument_progress import InstrumentProgress, PlayedNote, LearnedSong
from backend.models.oregon_trail import OregonTrailJourney, OregonTrailEvent
from backend.models.region_boss import BossSpawn, BossSpawnDefeat
from backend.models.magic_progress import RegionBoss, Challenge
from backend.models.world_state import WorldState, PlayerWorldState
from backend.models.voice_call import VoiceCall, VoiceMessage
from backend.models.multiplayer_session import MultiplayerSession, SessionParticipant
from backend.models.voice_settings import VoiceSettings

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
    # New PHASE 3 Models
    "InstrumentProgress",
    "PlayedNote",
    "LearnedSong",
    "OregonTrailJourney",
    "OregonTrailEvent",
    "BossSpawn",
    "BossSpawnDefeat",
    "RegionBoss",
    "Challenge",
    "WorldState",
    "PlayerWorldState",
    "VoiceCall",
    "VoiceMessage",
    "MultiplayerSession",
    "SessionParticipant",
    "VoiceSettings",
]
