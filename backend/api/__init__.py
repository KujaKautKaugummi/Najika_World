"""
Najika Backend API Routers
"""

from backend.api import auth, game, arena, training, voice, admin
from backend.api import state_v2, chat_v2  # V2 Migration Phase 1
from backend.api import battle_v2, living_v2, quest_v2, minigame_v2  # V2 Phase 2
from backend.api import slime_v3  # V3 Phase 3

__all__ = [
    "auth", "game", "arena", "training", "voice", "admin",
    "state_v2", "chat_v2",
    "battle_v2", "living_v2", "quest_v2", "minigame_v2",
    "slime_v3",
]
