"""
Najika Backend Services
Business logic layer for training, game systems, voice, and other services
"""

try:
    from services.training_launcher import training_launcher, TrainingLauncher
except ImportError:
    training_launcher = None; TrainingLauncher = None

try:
    from services.voice_service import voice_service, VoiceService
except ImportError:
    voice_service = None; VoiceService = None

try:
    from services.avatar_service import avatar_service, AvatarService
except ImportError:
    avatar_service = None; AvatarService = None

try:
    from services.finisher_system import finisher_generator, NajikaFinisherGenerator
except ImportError:
    finisher_generator = None; NajikaFinisherGenerator = None

try:
    from services.nemesis_arena_system import nemesis_arena, NemesisArenaSystem
except ImportError:
    nemesis_arena = None; NemesisArenaSystem = None

__all__ = [
    "training_launcher", "TrainingLauncher",
    "voice_service", "VoiceService",
    "avatar_service", "AvatarService",
    "finisher_generator", "NajikaFinisherGenerator",
    "nemesis_arena", "NemesisArenaSystem"
]
