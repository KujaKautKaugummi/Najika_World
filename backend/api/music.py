"""
Najika Music Mode API - Fortnite Festival Style!

Features:
- Rhythm Game Mechanics (NUR ZUM SPASS!)
- Instrumente (Ocarina, Echoharp, Taiko, Explosion Horn)
- Songs und Melodien
- Multiplayer Jam Sessions

WICHTIG: Musik gibt KEINE Gameplay-Buffs!
Musik ist nur für Spaß, Atmosphäre und Immersion!
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import random

# WebSocket for multiplayer sync
from backend.services.websocket_manager import websocket_manager
from backend.utils import handle_errors

router = APIRouter(prefix="/api/music", tags=["Music"])

# ============================================================================
# ENUMS
# ============================================================================

class InstrumentType(str, Enum):
    OCARINA = "ocarina"
    ECHOHARP = "echoharp"
    TAIKO = "taiko"
    EXPLOSION_HORN = "explosion_horn"

class NoteRating(str, Enum):
    PERFECT = "perfect"
    GREAT = "great"
    GOOD = "good"
    MISS = "miss"

# ============================================================================
# GAME DATA - KEINE BUFFS! Nur Spaß!
# ============================================================================

INSTRUMENTS = {
    InstrumentType.OCARINA: {
        "name": "Magical Ocarina",
        "description": "A mystical instrument with a beautiful, haunting sound",
        "songs": ["song_of_healing", "song_of_soaring", "lullaby", "sarias_song"],
        "unlock_level": 1,
        "sound_type": "wind",
    },
    InstrumentType.ECHOHARP: {
        "name": "Bard's Echoharp",
        "description": "A stringed instrument that echoes through the land",
        "songs": ["adventure_theme", "peaceful_melody", "campfire_song"],
        "unlock_level": 5,
        "sound_type": "strings",
    },
    InstrumentType.TAIKO: {
        "name": "War Taiko",
        "description": "Ancient drums with powerful beats",
        "songs": ["war_drums", "festival_beat", "thunder_rhythm"],
        "unlock_level": 10,
        "sound_type": "percussion",
    },
    InstrumentType.EXPLOSION_HORN: {
        "name": "Megumin's Explosion Horn",
        "description": "EXPLOSION!!! A dramatic fanfare horn! (Just for fun!)",
        "songs": ["explosion_anthem"],
        "unlock_level": 15,
        "sound_type": "brass",
    },
}

# Songs - KEINE BUFFS, nur Musik!
SONGS = {
    # Ocarina Songs
    "song_of_healing": {
        "name": "Song of Healing",
        "instrument": InstrumentType.OCARINA,
        "duration_seconds": 30,
        "bpm": 80,
        "difficulty": 1,
        "notes": 24,
        "mood": "peaceful",
        "description": "A calming melody that soothes the soul",
    },
    "song_of_soaring": {
        "name": "Song of Soaring",
        "instrument": InstrumentType.OCARINA,
        "duration_seconds": 15,
        "bpm": 120,
        "difficulty": 2,
        "notes": 18,
        "mood": "uplifting",
        "description": "A joyful tune that makes you feel like flying",
    },
    "lullaby": {
        "name": "Najika's Lullaby",
        "instrument": InstrumentType.OCARINA,
        "duration_seconds": 45,
        "bpm": 60,
        "difficulty": 1,
        "notes": 27,
        "mood": "sleepy",
        "description": "A gentle lullaby for peaceful evenings",
    },
    "sarias_song": {
        "name": "Forest Melody",
        "instrument": InstrumentType.OCARINA,
        "duration_seconds": 20,
        "bpm": 100,
        "difficulty": 2,
        "notes": 20,
        "mood": "playful",
        "description": "A cheerful tune that echoes through the forest",
    },

    # Echoharp Songs
    "adventure_theme": {
        "name": "Adventure Theme",
        "instrument": InstrumentType.ECHOHARP,
        "duration_seconds": 40,
        "bpm": 140,
        "difficulty": 3,
        "notes": 56,
        "mood": "epic",
        "description": "An inspiring melody for brave adventurers",
    },
    "peaceful_melody": {
        "name": "Peaceful Melody",
        "instrument": InstrumentType.ECHOHARP,
        "duration_seconds": 35,
        "bpm": 90,
        "difficulty": 2,
        "notes": 32,
        "mood": "relaxed",
        "description": "A gentle song perfect for a sunny afternoon",
    },
    "campfire_song": {
        "name": "Campfire Song",
        "instrument": InstrumentType.ECHOHARP,
        "duration_seconds": 50,
        "bpm": 100,
        "difficulty": 2,
        "notes": 50,
        "mood": "cozy",
        "description": "Gather 'round the campfire for this classic tune",
    },

    # Taiko Songs
    "war_drums": {
        "name": "War Drums",
        "instrument": InstrumentType.TAIKO,
        "duration_seconds": 30,
        "bpm": 160,
        "difficulty": 4,
        "notes": 48,
        "mood": "intense",
        "description": "Thundering drums that shake the earth",
    },
    "festival_beat": {
        "name": "Festival Beat",
        "instrument": InstrumentType.TAIKO,
        "duration_seconds": 45,
        "bpm": 140,
        "difficulty": 3,
        "notes": 63,
        "mood": "festive",
        "description": "A joyful rhythm for celebrations",
    },
    "thunder_rhythm": {
        "name": "Thunder Rhythm",
        "instrument": InstrumentType.TAIKO,
        "duration_seconds": 25,
        "bpm": 180,
        "difficulty": 5,
        "notes": 45,
        "mood": "powerful",
        "description": "A challenging rhythm like rolling thunder",
    },

    # Explosion Horn - Just for fun, no actual explosion!
    "explosion_anthem": {
        "name": "EXPLOSION ANTHEM!!!",
        "instrument": InstrumentType.EXPLOSION_HORN,
        "duration_seconds": 10,
        "bpm": 180,
        "difficulty": 5,
        "notes": 18,
        "mood": "DRAMATIC",
        "description": "A dramatic fanfare! EXPLOSION!!! (Just for fun!)",
    },
}

# Rating thresholds (timing window in ms)
RATING_WINDOWS = {
    NoteRating.PERFECT: 50,   # ±50ms
    NoteRating.GREAT: 100,    # ±100ms
    NoteRating.GOOD: 150,     # ±150ms
    # MISS: > 150ms
}

# ============================================================================
# IN-MEMORY STORAGE
# ============================================================================

# Active sessions: user_id -> session data
active_sessions: Dict[str, Dict[str, Any]] = {}

# Player high scores: user_id -> {song_id: best_score}
high_scores: Dict[str, Dict[str, int]] = {}

# Jam sessions: jam_id -> {users, song, sync_data}
jam_sessions: Dict[str, Dict[str, Any]] = {}

# ============================================================================
# MODELS
# ============================================================================

class StartSongRequest(BaseModel):
    user_id: str
    song_id: str
    instrument: InstrumentType

class NoteHitRequest(BaseModel):
    user_id: str
    note_index: int
    timing_offset_ms: int  # How many ms off from perfect

class SongCompleteRequest(BaseModel):
    user_id: str

class JoinJamRequest(BaseModel):
    user_id: str
    jam_id: Optional[str] = None  # None = create new
    song_id: str

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_rating(timing_offset_ms: int) -> NoteRating:
    """Get rating based on timing offset"""
    offset = abs(timing_offset_ms)
    if offset <= RATING_WINDOWS[NoteRating.PERFECT]:
        return NoteRating.PERFECT
    elif offset <= RATING_WINDOWS[NoteRating.GREAT]:
        return NoteRating.GREAT
    elif offset <= RATING_WINDOWS[NoteRating.GOOD]:
        return NoteRating.GOOD
    else:
        return NoteRating.MISS

def generate_note_pattern(song_id: str) -> List[Dict[str, Any]]:
    """Generate note pattern for a song"""
    song = SONGS[song_id]
    notes = []
    duration_ms = song["duration_seconds"] * 1000
    note_count = song["notes"]
    bpm = song["bpm"]

    # Calculate base interval
    beat_interval = 60000 / bpm  # ms per beat

    # Generate notes with some variation
    current_time = 1000  # Start 1 second in
    for i in range(note_count):
        # Add some rhythmic variation
        variation = random.uniform(-beat_interval * 0.1, beat_interval * 0.1)
        notes.append({
            "index": i,
            "time_ms": int(current_time),
            "lane": random.randint(1, 4),  # 4 lanes
        })
        current_time += beat_interval + variation

        # Ensure we don't exceed duration
        if current_time > duration_ms - 500:
            break

    return notes

def get_performance_rank(score_percent: float) -> str:
    """Get a fun rank based on performance - no gameplay effect!"""
    if score_percent >= 100:
        return "⭐ PERFECT! ⭐"
    elif score_percent >= 95:
        return "S - Amazing!"
    elif score_percent >= 90:
        return "A - Great!"
    elif score_percent >= 80:
        return "B - Good!"
    elif score_percent >= 70:
        return "C - Nice!"
    elif score_percent >= 60:
        return "D - Keep practicing!"
    else:
        return "F - Try again!"

# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/instruments")
@handle_errors()
async def get_instruments():
    """Get all available instruments"""
    return {
        "instruments": [
            {
                "id": inst.value,
                **INSTRUMENTS[inst]
            }
            for inst in InstrumentType
        ],
        "note": "Musik ist nur zum Spaß - keine Gameplay-Buffs!"
    }

@router.get("/songs")
@handle_errors()
async def get_songs(instrument: Optional[InstrumentType] = None):
    """Get available songs, optionally filtered by instrument"""
    songs = []
    for song_id, song_data in SONGS.items():
        if instrument and song_data["instrument"] != instrument:
            continue
        songs.append({
            "id": song_id,
            **song_data
        })
    return {
        "songs": songs,
        "count": len(songs),
        "note": "Spiel Songs zum Spaß - keine Buffs, nur gute Vibes!"
    }

@router.get("/song/{song_id}")
@handle_errors()
async def get_song(song_id: str):
    """Get specific song details"""
    if song_id not in SONGS:
        raise HTTPException(status_code=404, detail=f"Song '{song_id}' not found")
    return {
        "id": song_id,
        **SONGS[song_id]
    }

@router.post("/start-song")
@handle_errors()
async def start_song(request: StartSongRequest):
    """
    Start playing a song.
    Returns the note pattern for the rhythm game.
    """
    if request.song_id not in SONGS:
        raise HTTPException(status_code=404, detail=f"Song '{request.song_id}' not found")

    song = SONGS[request.song_id]

    # Check instrument matches
    if song["instrument"] != request.instrument:
        raise HTTPException(
            status_code=400,
            detail=f"Song requires {song['instrument'].value}, not {request.instrument.value}"
        )

    # Generate note pattern
    notes = generate_note_pattern(request.song_id)

    # Create session
    session = {
        "song_id": request.song_id,
        "instrument": request.instrument,
        "notes": notes,
        "started_at": datetime.now().isoformat(),
        "hits": [],
        "combo": 0,
        "max_combo": 0,
        "score": 0,
    }
    active_sessions[request.user_id] = session

    return {
        "success": True,
        "song": {
            "id": request.song_id,
            "name": song["name"],
            "duration_seconds": song["duration_seconds"],
            "bpm": song["bpm"],
            "difficulty": song["difficulty"],
            "mood": song["mood"],
        },
        "notes": notes,
        "message": f"🎵 Playing {song['name']}! Have fun!"
    }

@router.post("/note-hit")
@handle_errors()
async def note_hit(request: NoteHitRequest):
    """
    Register a note hit during gameplay.
    """
    if request.user_id not in active_sessions:
        raise HTTPException(status_code=400, detail="No active session")

    session = active_sessions[request.user_id]

    # Get rating
    rating = get_rating(request.timing_offset_ms)

    # Update combo
    if rating == NoteRating.MISS:
        session["combo"] = 0
    else:
        session["combo"] += 1
        if session["combo"] > session["max_combo"]:
            session["max_combo"] = session["combo"]

    # Calculate score for this note (just for fun!)
    score_values = {
        NoteRating.PERFECT: 100,
        NoteRating.GREAT: 75,
        NoteRating.GOOD: 50,
        NoteRating.MISS: 0,
    }
    note_score = score_values[rating]
    session["score"] += note_score

    # Record hit
    session["hits"].append({
        "note_index": request.note_index,
        "rating": rating.value,
        "timing_offset": request.timing_offset_ms,
        "score": note_score,
        "combo": session["combo"],
    })

    return {
        "rating": rating.value,
        "score": note_score,
        "combo": session["combo"],
        "total_score": session["score"],
    }

@router.post("/song-complete")
@handle_errors()
async def song_complete(request: SongCompleteRequest, background_tasks: BackgroundTasks):
    """
    Complete a song and see your results!
    NO BUFFS - just fun performance stats!
    """
    if request.user_id not in active_sessions:
        raise HTTPException(status_code=400, detail="No active session")

    session = active_sessions[request.user_id]
    song = SONGS[session["song_id"]]

    # Calculate final score
    total_notes = len(session["notes"])
    hits = len([h for h in session["hits"] if h["rating"] != "miss"])
    perfects = len([h for h in session["hits"] if h["rating"] == "perfect"])
    greats = len([h for h in session["hits"] if h["rating"] == "great"])
    goods = len([h for h in session["hits"] if h["rating"] == "good"])
    misses = total_notes - hits

    # Score percentage
    max_possible = total_notes * 100
    score_percent = (session["score"] / max_possible) * 100 if max_possible > 0 else 0

    # Get fun rank (no gameplay effect!)
    rank = get_performance_rank(score_percent)

    # Check for new high score
    is_new_high_score = False
    if request.user_id not in high_scores:
        high_scores[request.user_id] = {}

    current_best = high_scores[request.user_id].get(session["song_id"], 0)
    if session["score"] > current_best:
        high_scores[request.user_id][session["song_id"]] = session["score"]
        is_new_high_score = True

    # Create result - NO BUFFS!
    result = {
        "success": True,
        "song": song["name"],
        "score": session["score"],
        "score_percent": round(score_percent, 1),
        "max_combo": session["max_combo"],
        "rank": rank,
        "is_new_high_score": is_new_high_score,
        "ratings": {
            "perfect": perfects,
            "great": greats,
            "good": goods,
            "miss": misses,
        },
        "message": f"🎵 {rank} - Thanks for playing!"
    }

    # Special message for Explosion Anthem
    if session["song_id"] == "explosion_anthem":
        result["message"] = f"🎺 EXPLOSION!!! {rank} - Megumin would be proud! 💥"

    # Cleanup session
    del active_sessions[request.user_id]

    # WebSocket notification (for other players to see)
    background_tasks.add_task(
        websocket_manager.broadcast_to_channel,
        'lebensraum',
        {
            'type': 'music_performance',
            'user_id': request.user_id,
            'song': song["name"],
            'score_percent': round(score_percent, 1),
            'rank': rank,
            'mood': song["mood"],
        }
    )

    return result

@router.get("/high-scores/{user_id}")
@handle_errors()
async def get_high_scores(user_id: str):
    """Get player's high scores"""
    scores = high_scores.get(user_id, {})
    return {
        "user_id": user_id,
        "high_scores": [
            {
                "song_id": song_id,
                "song_name": SONGS[song_id]["name"] if song_id in SONGS else "Unknown",
                "score": score,
            }
            for song_id, score in scores.items()
        ],
        "total_songs_played": len(scores),
    }

# ============================================================================
# JAM SESSION (Multiplayer) - Just for fun together!
# ============================================================================

@router.post("/jam/join")
@handle_errors()
async def join_jam(request: JoinJamRequest, background_tasks: BackgroundTasks):
    """
    Join or create a multiplayer jam session.
    Play music together - just for fun!
    """
    if request.song_id not in SONGS:
        raise HTTPException(status_code=404, detail=f"Song '{request.song_id}' not found")

    song = SONGS[request.song_id]

    if request.jam_id and request.jam_id in jam_sessions:
        # Join existing jam
        jam = jam_sessions[request.jam_id]
        if jam["song_id"] != request.song_id:
            return {
                "success": False,
                "message": f"Jam is playing a different song: {SONGS[jam['song_id']]['name']}"
            }
        if request.user_id not in jam["users"]:
            jam["users"].append(request.user_id)
    else:
        # Create new jam
        jam_id = f"jam_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        jam_sessions[jam_id] = {
            "jam_id": jam_id,
            "song_id": request.song_id,
            "users": [request.user_id],
            "started": False,
            "created_at": datetime.now().isoformat(),
        }
        request.jam_id = jam_id

    # Notify other players
    background_tasks.add_task(
        websocket_manager.broadcast_to_channel,
        'lebensraum',
        {
            'type': 'jam_player_joined',
            'jam_id': request.jam_id,
            'user_id': request.user_id,
            'song': song["name"],
            'player_count': len(jam_sessions[request.jam_id]["users"]),
        }
    )

    return {
        "success": True,
        "jam_id": request.jam_id,
        "song": song["name"],
        "players": jam_sessions[request.jam_id]["users"],
        "message": f"🎵 Joined jam session! Let's play together!"
    }

@router.get("/jam/{jam_id}")
@handle_errors()
async def get_jam_status(jam_id: str):
    """Get jam session status"""
    if jam_id not in jam_sessions:
        raise HTTPException(status_code=404, detail="Jam session not found")

    jam = jam_sessions[jam_id]
    song = SONGS[jam["song_id"]]

    return {
        "jam_id": jam_id,
        "song": song["name"],
        "mood": song["mood"],
        "players": jam["users"],
        "player_count": len(jam["users"]),
        "started": jam["started"],
    }

@router.post("/jam/{jam_id}/start")
@handle_errors()
async def start_jam(jam_id: str, background_tasks: BackgroundTasks):
    """Start the jam session - play music together!"""
    if jam_id not in jam_sessions:
        raise HTTPException(status_code=404, detail="Jam session not found")

    jam = jam_sessions[jam_id]

    jam["started"] = True
    song = SONGS[jam["song_id"]]
    notes = generate_note_pattern(jam["song_id"])

    # Create sessions for all players
    for user_id in jam["users"]:
        active_sessions[user_id] = {
            "song_id": jam["song_id"],
            "instrument": song["instrument"],
            "notes": notes,
            "jam_id": jam_id,
            "started_at": datetime.now().isoformat(),
            "hits": [],
            "combo": 0,
            "max_combo": 0,
            "score": 0,
        }

    # Notify all players
    background_tasks.add_task(
        websocket_manager.broadcast_to_channel,
        'lebensraum',
        {
            'type': 'jam_started',
            'jam_id': jam_id,
            'song': song["name"],
            'notes': notes,
            'players': jam["users"],
            'mood': song["mood"],
        }
    )

    return {
        "success": True,
        "message": f"🎵 JAM SESSION STARTED! Let's make music together!",
        "notes": notes,
        "players": jam["users"],
        "song": song["name"],
        "mood": song["mood"],
    }

@router.delete("/jam/{jam_id}")
@handle_errors()
async def leave_jam(jam_id: str, user_id: str, background_tasks: BackgroundTasks):
    """Leave a jam session"""
    if jam_id not in jam_sessions:
        raise HTTPException(status_code=404, detail="Jam session not found")

    jam = jam_sessions[jam_id]

    if user_id in jam["users"]:
        jam["users"].remove(user_id)

    # Delete jam if empty
    if len(jam["users"]) == 0:
        del jam_sessions[jam_id]
        return {"success": True, "message": "Jam session ended"}

    # Notify remaining players
    background_tasks.add_task(
        websocket_manager.broadcast_to_channel,
        'lebensraum',
        {
            'type': 'jam_player_left',
            'jam_id': jam_id,
            'user_id': user_id,
            'remaining_players': jam["users"],
        }
    )

    return {
        "success": True,
        "message": "Left jam session",
        "remaining_players": jam["users"],
    }