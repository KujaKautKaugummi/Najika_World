"""
Najika Backend - Main Application
FastAPI application entry point with all API routers
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from backend.config import settings
from backend.database import init_db

# Import API routers
from backend.api import (
    auth, game, training, voice, admin, arena,
    slime, slime_arena, pvp, oregon_events, region_boss, magic_schools,
    instrument, world, multiplayer, card_game, dice_monsters,
    housing, farming, world_map, najika_compat,
    najika_game_actions_router, readiness, combat_magic, battle_unified,
    lebensraum, building, memory, voice_ue5, music, spell_names, special_stats, slime_2layer_ai,
    chat, living, temperature, websocket,  # WebSocket Support hinzugefügt!
    state_v2, chat_v2,  # V2 Core Router (Migration Phase 1)
    battle_v2, living_v2, quest_v2, minigame_v2,  # V2 Game Systems (Phase 2)
    slime_v3,  # Slime V3 Formwandler + Aura (Phase 3)
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

    # ================================================================
    # Initialize Shared Systems (V2 Migration)
    # ================================================================
    import backend.shared_state as shared

    # ChromaDB Memory (Enhanced)
    try:
        from najika_memory_enhanced import NajikaMemoryEnhanced
        shared.NAJIKA_MEMORY = NajikaMemoryEnhanced(
            persist_directory="C:\\Najika_World\\memory_db"
        )
        count = getattr(shared.NAJIKA_MEMORY, 'count', lambda: '?')
        print(f"  ChromaDB Memory loaded")
    except Exception as e:
        print(f"  Memory not available: {e}")

    # Web Search
    try:
        from najika_search import NajikaSearch
        shared.NAJIKA_SEARCH = NajikaSearch()
        print("  Web Search System loaded")
    except Exception as e:
        print(f"  Search not available: {e}")

    # Security (Alcatraz)
    try:
        from najika_security import NajikaSecurity
        shared.NAJIKA_SECURITY = NajikaSecurity()
        print("  Alcatraz Security loaded")
    except Exception as e:
        print(f"  Security not available: {e}")

    # Feature Flags
    try:
        from najika_personality_engine import PERSONALITY_ENGINE
        shared.PERSONALITY_ENGINE_ENABLED = True
        print("  PersonalityEngine v2.0 loaded")
    except ImportError:
        pass

    try:
        from najika_mind import get_mind
        shared.NAJIKA_MIND_ENABLED = True
        print("  NajikaMind AGI loaded")
    except ImportError:
        pass

    print("=" * 70)
    print("Backend is ready!")
    print(f"API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    print("=" * 70)

    yield

    # Shutdown
    print("Shutting down Najika Backend...")


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
app.include_router(arena.router, prefix=settings.API_PREFIX)
app.include_router(training.router, prefix=settings.API_PREFIX)
app.include_router(voice.router, prefix=settings.API_PREFIX)
app.include_router(admin.router, prefix=settings.API_PREFIX)

# Najika Compatibility Layer - MUSS VOR Game Systems (wegen catch-all routes)
app.include_router(najika_compat.router)

# Game Systems (FastAPI converted from Flask)
app.include_router(slime.router)  # Already has /api/slime prefix
app.include_router(slime_arena.router)  # Slime Arena: /api/slime-arena
app.include_router(slime_2layer_ai.router)  # Already has /api/slime-ai prefix
app.include_router(pvp.router)  # Already has /api/pvp prefix
app.include_router(oregon_events.router)  # Already has /api/oregon prefix
app.include_router(region_boss.router)  # Already has /api/region-boss prefix
app.include_router(magic_schools.router)  # Already has /api/magic prefix
app.include_router(spell_names.router)  # Already has /api/spells/name prefix
app.include_router(special_stats.router)  # Already has /api/special prefix
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

# Najika Game Actions System (Autonomous Living)
app.include_router(najika_game_actions_router.router)

# Najika Readiness System (Autonomy Gate)
app.include_router(readiness.router)

# Najika Combat Magic System (Infuse + Combo)
app.include_router(combat_magic.router)  # Already has /api/combat-magic prefix

# Unified Battle System (3 Modi: Auto, Manual, Cheer)
app.include_router(battle_unified.router)  # /api/battle prefix

# Lebensraum System (Digivice 3D World Sync)
app.include_router(lebensraum.router)  # /api/lebensraum prefix

# Building System (Lego Fortnite Style - Seamless Building!)
app.include_router(building.router)  # /api/building prefix

# Memory System (ChromaDB - Najika's permanent memory!)
app.include_router(memory.router)  # /api/memory prefix

# Voice UE5 Adapter (simplified TTS/STT for UE5 Blueprints)
app.include_router(voice_ue5.router)  # /api/voice-ue5 prefix

# Music Mode (Fortnite Festival Style - NUR ZUM SPASS, keine Buffs!)
app.include_router(music.router)  # /api/music prefix

# Chat (Najika Chat mit Ollama - public + kätzchen mode)
app.include_router(chat.router)  # /api/chat prefix

# Living System (Hunger, Energy, Mood - für living_system_ui.js)
app.include_router(living.router)  # /api/living prefix
app.include_router(living.care_router)  # /api/najika/feed, /drink, /sleep, /wash
app.include_router(living.status_router)  # /api/status/stream (SSE für private_mode.js)

# Temperature System (Body + Environment Temp)
app.include_router(temperature.router)  # /api/temperature prefix

# WebSocket System (Real-time communication)
app.include_router(websocket.router)  # /ws/connect - WebSocket Endpoint

# ============================================================================
# V2 CORE ROUTER (Migration Phase 1)
# ============================================================================
app.include_router(state_v2.router)   # /api/state - Zentraler State Management
app.include_router(chat_v2.router)    # /api/v2/chat - Chat V2 mit Shared State

# ============================================================================
# V2 GAME SYSTEMS (Migration Phase 2)
# ============================================================================
app.include_router(battle_v2.router)      # /api/v2/battle - Battle V2
app.include_router(living_v2.router)      # /api/v2/living - Living V2
app.include_router(living_v2.care_router) # /api/v2/care - Care Actions V2
app.include_router(quest_v2.router)       # /api/v2/quest - Quest V2
app.include_router(minigame_v2.router)    # /api/v2/minigame - Minigames V2

# ============================================================================
# SLIME V3 (Migration Phase 3 - Formwandler + Aura)
# ============================================================================
app.include_router(slime_v3.router)       # /api/slime-v3 - Slime Formwandler System


# ============================================================================
# STATIC FILES - DIGIVICE FRONTEND
# ============================================================================

# Get absolute paths for static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIVICE_DIR = os.path.join(BASE_DIR, "digivice")
STATIC_DIR = os.path.join(DIGIVICE_DIR, "static")
ASSETS_DIR = os.path.join(STATIC_DIR, "assets")
JS_DIR = os.path.join(DIGIVICE_DIR, "js")
DATA_DIR = os.path.join(DIGIVICE_DIR, "data")

# Mount /data → digivice/data (World Data JSON files)
app.mount("/data", StaticFiles(directory=DATA_DIR), name="world_data")

# Mount /js → digivice/js (JavaScript files)
app.mount("/js", StaticFiles(directory=JS_DIR), name="js_files")

# Mount /static → digivice/static (CSS, Assets, etc.)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static_files")

# Mount KayKit assets from digivice/static/assets (legacy /assets path)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="kaykit_assets")

# Mount digivice static files (must be last to allow HTML fallback)
app.mount("/digivice", StaticFiles(directory=DIGIVICE_DIR, html=True), name="digivice")


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Serve the Digivice frontend"""
    index_path = os.path.join(DIGIVICE_DIR, "index.html")
    return FileResponse(index_path)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    }


@app.get("/api/performance/stats")
def performance_stats():
    """Performance statistics for all endpoints"""
    from backend.utils import get_performance_stats
    return {
        "endpoints": get_performance_stats(),
        "note": "Use @measure_performance() decorator to track endpoints"
    }


@app.get("/api/performance/slow")
def slow_endpoints(limit: int = 10):
    """Recent slow endpoint calls"""
    from backend.utils import get_slow_endpoints
    return {
        "slow_calls": get_slow_endpoints(limit=limit),
        "limit": limit
    }


@app.get("/api/performance/slowest")
def slowest_endpoints(top_n: int = 10):
    """Top N slowest endpoints by average time"""
    from backend.utils import get_slowest_endpoints
    return {
        "slowest_endpoints": get_slowest_endpoints(top_n=top_n),
        "top_n": top_n
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
        "backend.main_fastapi:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="debug" if settings.DEBUG else "info",
    )
