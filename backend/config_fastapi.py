"""
Najika Backend Configuration
Centralized configuration management with environment variables
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App Info
    APP_NAME: str = "Najika World API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = True

    # Security
    SECRET_KEY: str = "changeme_generate_secure_secret_key_minimum_32_characters"
    JWT_SECRET: str = "changeme_generate_secure_jwt_secret_minimum_32_characters"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24  # 24 hours
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "*"]

    # Database
    DATABASE_URL: str = "sqlite:///./najika_world.db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO: bool = False

    # Redis (Caching & Sessions)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour

    # Celery (Background Tasks)
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # API Settings
    API_PREFIX: str = "/api/v1"
    RATE_LIMIT_PER_MINUTE: int = 60
    MAX_REQUEST_SIZE: int = 10 * 1024 * 1024  # 10MB

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".mp3", ".wav", ".mp4"]

    # Training Settings
    TRAINING_DATA_DIR: str = "./training_data"
    MODEL_OUTPUT_DIR: str = "./models"
    LORA_OUTPUT_DIR: str = "./lora_models"
    TRAINING_BATCH_SIZE: int = 4
    TRAINING_MAX_LENGTH: int = 2048

    # Voice Settings
    VOICE_DATA_DIR: str = "./voice_data"
    TTS_ENGINE: str = "coqui"  # coqui, edge
    WHISPER_MODEL: str = "base"
    TTS_CACHE_DIR: str = "./tts_cache"

    # AI & Memory
    CHROMA_DB_PATH: str = "./chromadb"
    MEMORY_COLLECTION: str = "najika_memories"
    MAX_MEMORY_RESULTS: int = 10

    # Game Settings
    SAVE_DIR: str = "./saves"
    MAX_SAVE_SLOTS: int = 10
    BATTLE_TIMEOUT_SECONDS: int = 300
    FARM_GROWTH_MULTIPLIER: float = 1.0
    FISHING_SPAWN_RATE: float = 0.3

    # Feature Flags
    ENABLE_REGISTRATION: bool = True
    ENABLE_VOICE_CHAT: bool = True
    ENABLE_TRAINING: bool = True
    ENABLE_TOR: bool = False
    ENABLE_WEBSOCKETS: bool = True

    # Monitoring
    ENABLE_METRICS: bool = True
    ENABLE_LOGGING: bool = True
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/najika.log"

    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Paths
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()


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


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        settings.UPLOAD_DIR,
        settings.TRAINING_DATA_DIR,
        settings.MODEL_OUTPUT_DIR,
        settings.LORA_OUTPUT_DIR,
        settings.VOICE_DATA_DIR,
        settings.TTS_CACHE_DIR,
        settings.CHROMA_DB_PATH,
        settings.SAVE_DIR,
        os.path.dirname(settings.LOG_FILE),
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    return len(directories)


if __name__ == "__main__":
    # Test configuration
    print("=== Najika World Configuration ===")
    print(f"App: {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Database: {settings.DATABASE_URL}")
    print(f"API Prefix: {settings.API_PREFIX}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")

    dirs_created = create_directories()
    print(f"\n✅ Created {dirs_created} necessary directories")
    print("✅ Configuration loaded successfully!")
