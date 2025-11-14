"""
Najika Backend Services
Business logic layer for training, game systems, voice, and other services
"""

from backend.services.training_launcher import training_launcher, TrainingLauncher
from backend.services.voice_service import voice_service, VoiceService

__all__ = ["training_launcher", "TrainingLauncher", "voice_service", "VoiceService"]
