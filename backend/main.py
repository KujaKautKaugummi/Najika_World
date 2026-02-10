"""
Najika Backend - Main Entry Point
Re-exports from main_fastapi.py (the canonical version with all routers)
"""

# Re-export app so that "backend.main:app" works everywhere
from backend.main_fastapi import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings
    uvicorn.run(
        "backend.main_fastapi:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="debug" if settings.DEBUG else "info",
    )
