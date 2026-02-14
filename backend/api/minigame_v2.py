"""
Minigame Router V2 - Nutzt Shared State
Rhythm, Garten, Reflex, Kochen und andere Minigames.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time
import sys
import os
import logging

logger = logging.getLogger("najika.api.minigame_v2")

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from backend.shared_state import STATE

router = APIRouter(prefix="/api/v2/minigame", tags=["Minigame V2"])


# ============================================================================
# MODELS
# ============================================================================

class MinigameStartRequest(BaseModel):
    game_type: str  # rhythm, garden, reflex, cooking, fishing, alchemy
    difficulty: str = "normal"  # easy, normal, hard


class MinigameScoreRequest(BaseModel):
    game_type: str
    score: int
    perfect: bool = False
    combo: int = 0
    time_ms: Optional[int] = None


class MinigameResult(BaseModel):
    success: bool
    score: int
    xp_gained: int
    gold_gained: int
    happiness_gained: int
    perfect_bonus: bool
    message: str


# ============================================================================
# MINIGAME CONFIG
# ============================================================================

MINIGAME_CONFIG = {
    "rhythm": {
        "name": "Rhythmus-Spiel",
        "description": "Triff die Noten im Takt!",
        "xp_per_point": 0.15,
        "gold_per_point": 0.08,
        "happiness_bonus": 10,
        "perfect_multiplier": 2.0,
    },
    "garden": {
        "name": "Garten-Pflege",
        "description": "Pflanze und pflege Krauter.",
        "xp_per_point": 0.1,
        "gold_per_point": 0.12,
        "happiness_bonus": 8,
        "perfect_multiplier": 1.5,
    },
    "reflex": {
        "name": "Reflex-Training",
        "description": "Reagiere so schnell wie moeglich!",
        "xp_per_point": 0.2,
        "gold_per_point": 0.05,
        "happiness_bonus": 5,
        "perfect_multiplier": 2.5,
    },
    "cooking": {
        "name": "Kochen",
        "description": "Koche ein Gericht fuer Najika!",
        "xp_per_point": 0.12,
        "gold_per_point": 0.1,
        "happiness_bonus": 15,  # Najika liebt Essen!
        "perfect_multiplier": 1.8,
    },
    "fishing": {
        "name": "Angeln",
        "description": "Fange Fische an der Salzwind-Kueste!",
        "xp_per_point": 0.1,
        "gold_per_point": 0.15,
        "happiness_bonus": 7,
        "perfect_multiplier": 1.5,
    },
    "alchemy": {
        "name": "Alchemie",
        "description": "Mische Zutaten zum richtigen Trank!",
        "xp_per_point": 0.18,
        "gold_per_point": 0.12,
        "happiness_bonus": 6,
        "perfect_multiplier": 2.0,
    },
}

# Highscores (in-memory)
_highscores: Dict[str, dict] = {}


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/games")
async def list_minigames():
    """Alle verfuegbaren Minigames"""
    games = []
    for gid, config in MINIGAME_CONFIG.items():
        hs = _highscores.get(gid, {})
        games.append({
            "id": gid,
            "name": config["name"],
            "description": config["description"],
            "highscore": hs.get("score", 0),
            "plays": hs.get("plays", 0),
        })
    return {"games": games, "count": len(games)}


@router.post("/start")
async def start_minigame(request: MinigameStartRequest):
    """Minigame starten"""
    if request.game_type not in MINIGAME_CONFIG:
        raise HTTPException(400, f"Unbekanntes Spiel: {request.game_type}")

    config = MINIGAME_CONFIG[request.game_type]

    # Energy-Check: Braucht mindestens 10 Energy
    if STATE["najika"]["energy"] < 10:
        raise HTTPException(400, "Nicht genug Energie! Ruh dich zuerst aus.")

    return {
        "success": True,
        "game_type": request.game_type,
        "name": config["name"],
        "difficulty": request.difficulty,
        "started_at": time.time(),
    }


@router.post("/score", response_model=MinigameResult)
async def submit_score(request: MinigameScoreRequest):
    """Score einreichen und Rewards berechnen"""
    if request.game_type not in MINIGAME_CONFIG:
        raise HTTPException(400, f"Unbekanntes Spiel: {request.game_type}")

    config = MINIGAME_CONFIG[request.game_type]

    # Rewards berechnen
    base_xp = int(request.score * config["xp_per_point"])
    base_gold = int(request.score * config["gold_per_point"])
    happiness = config["happiness_bonus"]

    # Combo Bonus
    if request.combo > 10:
        base_xp = int(base_xp * 1.3)
        base_gold = int(base_gold * 1.2)

    # Perfect Bonus
    if request.perfect:
        base_xp = int(base_xp * config["perfect_multiplier"])
        base_gold = int(base_gold * config["perfect_multiplier"])
        happiness = int(happiness * 1.5)

    # State updaten
    STATE["user"]["xp"] += base_xp
    STATE["user"]["points"] += base_gold
    STATE["najika"]["happiness"] = min(100, STATE["najika"]["happiness"] + happiness)
    STATE["najika"]["energy"] = max(0, STATE["najika"]["energy"] - 5)

    # Highscore tracken
    if request.game_type not in _highscores:
        _highscores[request.game_type] = {"score": 0, "plays": 0}
    hs = _highscores[request.game_type]
    hs["plays"] += 1
    new_record = request.score > hs["score"]
    if new_record:
        hs["score"] = request.score

    # Message
    if request.perfect:
        message = "PERFEKT! Najika ist begeistert!"
    elif request.score > 500:
        message = "Grossartig gespielt!"
    elif request.score > 200:
        message = "Gut gemacht!"
    else:
        message = "Weiter ueben!"

    if new_record:
        message += " NEUER HIGHSCORE!"

    return MinigameResult(
        success=True,
        score=request.score,
        xp_gained=base_xp,
        gold_gained=base_gold,
        happiness_gained=happiness,
        perfect_bonus=request.perfect,
        message=message,
    )


@router.get("/highscores")
async def get_highscores():
    """Alle Highscores"""
    result = {}
    for gid, config in MINIGAME_CONFIG.items():
        hs = _highscores.get(gid, {"score": 0, "plays": 0})
        result[gid] = {
            "name": config["name"],
            "highscore": hs.get("score", 0),
            "plays": hs.get("plays", 0),
        }
    return {"highscores": result}


@router.get("/highscores/{game_type}")
async def get_game_highscore(game_type: str):
    """Highscore fuer ein Spiel"""
    if game_type not in MINIGAME_CONFIG:
        raise HTTPException(404, f"Spiel nicht gefunden: {game_type}")

    hs = _highscores.get(game_type, {"score": 0, "plays": 0})
    return {
        "game_type": game_type,
        "name": MINIGAME_CONFIG[game_type]["name"],
        "highscore": hs.get("score", 0),
        "plays": hs.get("plays", 0),
    }
