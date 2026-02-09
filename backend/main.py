"""
Najika Backend - Main Application
FastAPI application entry point with all API routers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from backend.config import settings
from backend.database import init_db

# Import API routers
from backend.api import (
    auth, game, training, voice, admin, arena,
    slime, pvp, oregon_events, region_boss, magic_schools,
    instrument, world, multiplayer, card_game, dice_monsters,
    housing, farming, world_map, najika_compat,
    najika_game_actions_router, chat
)


# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    print("=" * 70)
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 70)

    # Initialize database
    print("Initializing database...")
    init_db()

    print("Backend is ready!")
    print(f"API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    print("=" * 70)

    yield

    # Shutdown
    print("👋 Shutting down Najika Backend...")


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    # Najika Backend API

    Complete backend system for Najika World ecosystem.

    ## Features

    - 🔐 **Authentication** - JWT-based user authentication
    - 🎮 **Game Systems** - Combat, inventory, farming, fishing, quests
    - 🏟️ **Nemesis Arena** - Shadow of Mordor hierarchy + Mortal Kombat finishers
    - 🤖 **AI Training** - LoRA training, session training, code training
    - 🎤 **Voice Chat** - WebSocket voice with Whisper AI transcription
    - ⚙️ **Admin** - User management, system monitoring

    ## Components

    - **UE5 Mobile Game** - Android game with backend integration
    - **Digivice Web Game** - Browser-based 3D game
    - **Training Systems** - AI training and model management
    - **Voice Systems** - Real-time voice chat and TTS

    ---

    **Version:** {version}
    **Environment:** {environment}
    """.format(
        version=settings.APP_VERSION,
        environment="Debug" if settings.DEBUG else "Production"
    ),
    lifespan=lifespan,
)


# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# INCLUDE ROUTERS
# ============================================================================

app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(game.router, prefix=settings.API_PREFIX)
app.include_router(training.router, prefix=settings.API_PREFIX)
app.include_router(voice.router, prefix=settings.API_PREFIX)
app.include_router(admin.router, prefix=settings.API_PREFIX)

# Game Systems (FastAPI converted from Flask)
app.include_router(arena.router)  # Already has /api/arena prefix
app.include_router(slime.router)  # Already has /api/slime prefix
app.include_router(pvp.router)  # Already has /api/pvp prefix
app.include_router(oregon_events.router)  # Already has /api/oregon prefix
app.include_router(region_boss.router)  # Already has /api/region-boss prefix
app.include_router(magic_schools.router)  # Already has /api/magic prefix
app.include_router(instrument.router)  # Already has /api/instrument prefix
app.include_router(world.router)  # Already has /api/world prefix
app.include_router(multiplayer.router)  # Already has /multiplayer prefix

# Card Game Systems
app.include_router(card_game.router)  # Already has /api/cards prefix
app.include_router(card_game.decks_router)  # Already has /api/decks prefix
app.include_router(card_game.matches_router)  # Already has /api/matches prefix
app.include_router(card_game.rankings_router)  # Already has /api/rankings prefix

# Dice Monsters System
app.include_router(dice_monsters.router)  # Already has /api/dice prefix
app.include_router(dice_monsters.duel_router)  # Already has /api/dice-duel prefix

# Housing & Farming System
app.include_router(housing.router)  # Already has /api/housing prefix
app.include_router(farming.router)  # Already has /api/farming prefix

# World Map System (9600x9600 Grid)
app.include_router(world_map.router)  # Already has /api/world-map prefix

# Najika Compatibility Layer (for old digivice frontend)
app.include_router(najika_compat.router)

# Najika Game Actions System (Autonomous Living)
app.include_router(najika_game_actions_router.router)

# Chat System (LM Studio + Personality)
app.include_router(chat.router)  # Already has /api/chat prefix


# ============================================================================
# STATIC FILES - DIGIVICE FRONTEND
# ============================================================================

# Mount KayKit assets from digivice/static/assets
app.mount("/assets", StaticFiles(directory="digivice/static/assets"), name="kaykit_assets")

# Mount digivice static files (must be last to allow HTML fallback)
app.mount("/digivice", StaticFiles(directory="digivice", html=True), name="digivice")


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": settings.API_PREFIX,
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    }


@app.get(f"{settings.API_PREFIX}/info")
def api_info():
    """API information and available endpoints"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": {
            "auth": f"{settings.API_PREFIX}/auth",
            "game": f"{settings.API_PREFIX}/game",
            "arena": f"{settings.API_PREFIX}/game/arena",
            "training": f"{settings.API_PREFIX}/training",
            "voice": f"{settings.API_PREFIX}/voice",
            "admin": f"{settings.API_PREFIX}/admin",
        },
        "websocket": {
            "voice": f"{settings.API_PREFIX}/voice/ws/{{token}}",
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json",
        },
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url),
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
        }
    )


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="debug" if settings.DEBUG else "info",
    )
