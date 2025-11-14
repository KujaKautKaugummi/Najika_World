"""
Najika Backend Database
SQLAlchemy database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from backend.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI routes to get database session

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables
    Call this on application startup
    """
    # Import all models here to ensure they are registered with Base
    from backend.models import user, character, inventory, training

    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")


def drop_all_tables() -> None:
    """
    Drop all tables (use with caution!)
    Only for development/testing
    """
    if not settings.DEBUG:
        raise Exception("Cannot drop tables in production mode!")

    Base.metadata.drop_all(bind=engine)
    print("⚠️ All tables dropped")


def reset_database() -> None:
    """
    Reset database by dropping and recreating all tables
    Only for development
    """
    if not settings.DEBUG:
        raise Exception("Cannot reset database in production mode!")

    drop_all_tables()
    init_db()
    print("🔄 Database reset complete")
