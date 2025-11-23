"""
Najika Backend Services
Business logic layer for training, game systems, voice, and other services
"""

from backend.services.training_launcher import training_launcher, TrainingLauncher
from backend.services.voice_service import voice_service, VoiceService
from backend.services.avatar_service import avatar_service, AvatarService
from backend.services.finisher_system import finisher_generator, NajikaFinisherGenerator
from backend.services.nemesis_arena_system import nemesis_arena, NemesisArenaSystem

__all__ = [
    "training_launcher", "TrainingLauncher",
    "voice_service", "VoiceService",
    "avatar_service", "AvatarService",
    "finisher_generator", "NajikaFinisherGenerator",
    "nemesis_arena", "NemesisArenaSystem"
]
