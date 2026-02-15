"""
Najika World - Game Server
FastAPI Server für Card Games, Dice Monsters & andere Game Systems
Port: 8001

Separate vom Main Server (najika_server.py auf Port 8000)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
import datetime
import sqlite3

# Add parent directory to path so we can import backend
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import database and routers
from backend.database import init_db, engine, Base
from backend.api import card_game, dice_monsters

# Database path for direct SQLite access
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "najika_game.db")

# Create FastAPI app
app = FastAPI(
    title="Najika World - Game Server",
    description="Card Games, Dice Monsters & Game Systems API",
    version="1.0.0"
)

# CORS Configuration (allow frontend on port 8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("[STARTUP] Najika World - Game Server Starting...")
    print("[DB] Initializing Database...")

    try:
        # Initialize database (create tables)
        init_db()
        print("[OK] Database initialized successfully!")
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        raise

    print("[READY] Game Server Ready!")
    print("[URL] Server running on: http://localhost:8001")
    print("[DOCS] API Docs: http://localhost:8001/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("[SHUTDOWN] Game Server Shutting Down...")


# ============================================================================
# ROUTERS
# ============================================================================

# Card Game Routes
app.include_router(card_game.router)
app.include_router(card_game.decks_router)
app.include_router(card_game.matches_router)
app.include_router(card_game.rankings_router)

# Dice Monsters Routes
app.include_router(dice_monsters.router)
app.include_router(dice_monsters.duel_router)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Najika World - Game Server",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "card_games": "/api/cards",
            "dice_monsters": "/api/dice-monsters",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "systems": {
            "card_games": "online",
            "dice_monsters": "online"
        }
    }


# ============================================================================
# CARD GAME APIs
# ============================================================================

@app.get("/api/cards")
async def get_cards(player_id: int = 1, limit: int = 100):
    """Get player's card collection"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Get player's cards
        c.execute('''
            SELECT c.*, pcc.copies_owned
            FROM cards c
            INNER JOIN player_card_collections pcc ON c.id = pcc.card_id
            WHERE pcc.player_id = ?
            LIMIT ?
        ''', (player_id, limit))

        cards = []
        for row in c.fetchall():
            cards.append({
                "id": row["id"],
                "name": row["name"],
                "type": row["card_type"],
                "faction": row["faction"],
                "rarity": row["rarity"],
                "triad_values": {
                    "top": row["top_value"],
                    "right": row["right_value"],
                    "bottom": row["bottom_value"],
                    "left": row["left_value"]
                },
                "hearthstone_stats": {
                    "mana": row["mana_cost"],
                    "attack": row["attack"],
                    "health": row["health"],
                    "durability": row["durability"]
                },
                "effect": {
                    "type": row["effect_type"],
                    "description": row["effect_description"],
                    "script": row["effect_script"]
                },
                "image_url": row["image_url"],
                "description": row["description"],
                "unlock_level": row["unlock_level"],
                "copies_owned": row["copies_owned"]
            })

        conn.close()
        return {"cards": cards, "count": len(cards)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/matches/create")
async def create_match(request: Request):
    """Create a new Triple Triad match"""
    try:
        data = await request.json()
        player_id = data.get("player_id", 1)
        game_mode = data.get("game_mode", "triad")
        is_ranked = data.get("is_ranked", False)

        # Create simple match
        match = {
            "id": int(datetime.datetime.now().timestamp()),
            "player_id": player_id,
            "game_mode": game_mode,
            "is_ranked": is_ranked,
            "board": [[None for _ in range(3)] for _ in range(3)],
            "current_turn": "player",
            "player_score": 5,
            "opponent_score": 5,
            "status": "active"
        }

        return {"match": match, "success": True}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "detail": str(exc)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)}
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("[GAME SERVER] NAJIKA WORLD - GAME SERVER")
    print("=" * 60)
    print()

    uvicorn.run(
        "game_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
