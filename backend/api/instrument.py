"""
Instrument Playing API - Najika World
======================================

REST API für Spielbares Instrument System (FastAPI)

Endpoints:
- POST /api/instrument/play-note - Play single note
- POST /api/instrument/play-song - Play complete song
- POST /api/instrument/switch - Switch instrument
- GET /api/instrument/<type> - Get instrument info
- GET /api/instrument/songs - Get all songs
- GET /api/instrument/songs/<song_id> - Get specific song
- GET /api/instrument/progress - Get player progress
- GET /api/instrument/state/export - Export state

Educational purpose: Learn real instruments while playing!

NO STAMINA COSTS - Completely unlimited like Zelda Ocarina of Time!

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.services.instrument_system import (
    InstrumentPlayingSystem, InstrumentType, Note, NoteQuality
)

# Create FastAPI Router
router = APIRouter(prefix="/api/instrument", tags=["instrument"])

# Global System Instance
instrument_system = InstrumentPlayingSystem()


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class PlayNoteRequest(BaseModel):
    instrument: Optional[str] = None
    note: str
    octave: int = Field(4, ge=1, le=8)
    duration: float = Field(0.5, gt=0)
    velocity: float = Field(0.8, ge=0.0, le=1.0)
    quality: str = "good"


class PlaySongRequest(BaseModel):
    song_id: str
    note_accuracies: List[float] = []


class SwitchInstrumentRequest(BaseModel):
    instrument: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/play-note")
async def play_note(request: PlayNoteRequest):
    """
    Play Single Note

    Body:
    {
        "instrument": "mundharmonika",  // optional, uses current
        "note": "C",
        "octave": 4,
        "duration": 0.5,  // seconds
        "velocity": 0.8,  // 0.0-1.0
        "quality": "good"  // perfect, great, good, ok, poor, miss
    }

    Returns:
        note_data: {
            note: str,
            frequency: float,
            xp_gained: float,
            level: int,
            level_up: bool,
            quality: str
        }
    """
    try:
        # Parse instrument (optional)
        instrument = None
        if request.instrument:
            try:
                instrument = InstrumentType(request.instrument)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": f"Ungültiges Instrument: {request.instrument}",
                        "valid_instruments": [i.value for i in InstrumentType]
                    }
                )
        else:
            instrument = instrument_system.current_instrument

        # Parse note
        try:
            note = Note(request.note.upper())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültige Note: {request.note}",
                    "valid_notes": [n.value for n in Note]
                }
            )

        # Parse quality
        try:
            quality = NoteQuality(request.quality)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültige Quality: {request.quality}",
                    "valid_qualities": [q.value for q in NoteQuality]
                }
            )

        # Play note!
        result = instrument_system.play_note(
            instrument,
            note,
            request.octave,
            request.duration,
            request.velocity,
            quality
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/play-song")
async def play_song(request: PlaySongRequest):
    """
    Play Complete Song

    Body:
    {
        "song_id": "happy_birthday",
        "note_accuracies": [85.5, 92.0, 78.3, ...]  // accuracy % für jede Note
    }

    Returns:
        song_result: {
            song_name: str,
            notes_count: int,
            perfect_notes: int,
            total_score: float,
            accuracy: float,
            rank: str,  // S, A, B, C, D
            xp_gained: float,
            level: int,
            level_up: bool
        }
    """
    try:
        # Play song!
        result = instrument_system.play_song(
            request.song_id,
            request.note_accuracies
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/switch")
async def switch_instrument(request: SwitchInstrumentRequest):
    """
    Switch Instrument

    Body:
    {
        "instrument": "gitarre"
    }

    Returns:
        {
            success: bool,
            previous: str,
            current: str,
            message: str
        }
    """
    try:
        try:
            instrument = InstrumentType(request.instrument)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiges Instrument: {request.instrument}",
                    "valid_instruments": [i.value for i in InstrumentType]
                }
            )

        result = instrument_system.switch_instrument(instrument)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{instrument_type}")
async def get_instrument_info(instrument_type: str):
    """
    Get Instrument Info

    Path: /api/instrument/mundharmonika

    Returns:
        {
            type: str,
            name: str,
            difficulty: str,
            range_low: str,
            range_high: str,
            description: str
        }
    """
    try:
        try:
            instrument = InstrumentType(instrument_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiges Instrument: {instrument_type}",
                    "valid_instruments": [i.value for i in InstrumentType]
                }
            )

        info = instrument_system.get_instrument_info(instrument)

        return info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs")
async def get_all_songs(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty")
):
    """
    Get All Songs

    Query Params:
        category: str (optional) - tutorial, zelda, popular, etc.
        difficulty: str (optional) - easy, medium, hard

    Returns:
        {
            songs: [
                {
                    id: str,
                    name: str,
                    category: str,
                    difficulty: str,
                    notes_count: int,
                    duration: float
                }
            ],
            count: int
        }
    """
    try:
        songs = instrument_system.get_all_songs(category, difficulty)

        return {
            "songs": songs,
            "count": len(songs)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs/{song_id}")
async def get_song(song_id: str):
    """
    Get Specific Song

    Path: /api/instrument/songs/happy_birthday

    Returns:
        {
            id: str,
            name: str,
            category: str,
            difficulty: str,
            notes: [
                {
                    note: str,
                    octave: int,
                    duration: float,
                    velocity: float
                }
            ],
            tutorial_text: str
        }
    """
    try:
        song = instrument_system.get_song(song_id)

        if not song:
            raise HTTPException(
                status_code=404,
                detail=f"Song nicht gefunden: {song_id}"
            )

        return song

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progress")
async def get_progress():
    """
    Get Player Progress

    Returns:
        {
            current_instrument: str,
            level: int,
            total_xp: float,
            perfect_notes: int,
            total_notes: int,
            accuracy: float,
            play_time: float,
            songs_completed: int
        }
    """
    try:
        progress = instrument_system.get_progress()

        return progress

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
async def export_state():
    """
    Export State

    Returns:
        JSON with complete instrument state
    """
    try:
        state = instrument_system.export_state()
        return state

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
