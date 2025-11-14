"""
Najika Backend Configuration
Centralized configuration management with environment variables
"""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App Info
    APP_NAME: str = "Najika API"
    APP_VERSION: str = "4.0"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./najika.db")

    # CORS
    CORS_ORIGINS: list = ["*"]  # Configure in production

    # API Settings
    API_PREFIX: str = "/api"
    RATE_LIMIT_PER_MINUTE: int = 60

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # Training Settings
    TRAINING_DATA_DIR: str = os.getenv("TRAINING_DATA_DIR", "./training_data")
    MODEL_OUTPUT_DIR: str = os.getenv("MODEL_OUTPUT_DIR", "./models")

    # Voice Settings
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")
    TTS_ENGINE: str = os.getenv("TTS_ENGINE", "edge")  # edge or coqui
    VOICE_DATA_DIR: str = "./voice_data"

    # Game Settings
    SAVE_DIR: str = "./saves"
    MAX_SAVE_SLOTS: int = 10

    # ChromaDB
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")

    # Paths
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Helper functions
def get_database_url() -> str:
    """Get database URL with proper formatting"""
    return settings.DATABASE_URL


def get_training_data_path(filename: str = "") -> str:
    """Get full path to training data file"""
    return os.path.join(settings.TRAINING_DATA_DIR, filename)


def get_model_output_path(filename: str = "") -> str:
    """Get full path to model output"""
    return os.path.join(settings.MODEL_OUTPUT_DIR, filename)


def get_save_path(filename: str = "") -> str:
    """Get full path to save file"""
    return os.path.join(settings.SAVE_DIR, filename)


def get_voice_data_path(filename: str = "") -> str:
    """Get full path to voice data file"""
    return os.path.join(settings.VOICE_DATA_DIR, filename)
