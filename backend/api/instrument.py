"""
Instrument Playing API - Najika World
======================================

REST API für Spielbares Instrument System (FastAPI) (DATABASE)

Endpoints:
- POST /api/instrument/play-note - Play single note (DATABASE)
- POST /api/instrument/play-song - Play complete song (DATABASE)
- POST /api/instrument/switch - Switch instrument (DATABASE)
- GET /api/instrument/<type> - Get instrument info (static)
- GET /api/instrument/songs - Get all songs (static)
- GET /api/instrument/songs/<song_id> - Get specific song (static)
- GET /api/instrument/progress - Get player progress (DATABASE)
- GET /api/instrument/state/export - Export state (DATABASE)

Educational purpose: Learn real instruments while playing!

NO STAMINA COSTS - Completely unlimited like Zelda Ocarina of Time!

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from backend.database import get_db
from backend.models.instrument_progress import InstrumentProgress, PlayedNote, LearnedSong
from backend.services.instrument_system import (
    InstrumentSystem, InstrumentType, Note, NoteQuality
)
from backend.utils import handle_errors

# Create FastAPI Router
router = APIRouter(prefix="/api/instrument", tags=["instrument"])

# Global System Instance (for static config: songs, instrument data)
instrument_system = InstrumentSystem()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_or_create_progress(db: Session, player_id: int) -> InstrumentProgress:
    """Get or create instrument progress for player"""
    progress = db.query(InstrumentProgress).filter(
        InstrumentProgress.player_id == player_id
    ).first()

    if not progress:
        progress = InstrumentProgress(
            player_id=player_id,
            current_instrument="mundharmonika",
            instrument_skills={},
            instrument_experience={},
            learned_songs=[],
            total_notes_played=0,
            perfect_notes=0,
            great_notes=0,
            good_notes=0
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return progress


def calculate_xp_for_note(quality: str) -> int:
    """Calculate XP based on note quality"""
    xp_map = {
        "perfect": 10,
        "great": 7,
        "good": 5,
        "ok": 3,
        "poor": 1,
        "miss": 0
    }
    return xp_map.get(quality.lower(), 5)


def calculate_level_from_xp(xp: int) -> int:
    """Calculate level from XP (exponential)"""
    # Level 1 = 0 XP, Level 2 = 100 XP, Level 3 = 220 XP, etc.
    level = 1
    xp_required = 0
    while xp >= xp_required:
        level += 1
        xp_required += int(100 * (1.2 ** (level - 2)))
    return max(1, level - 1)


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class PlayNoteRequest(BaseModel):
    player_id: int
    instrument: Optional[str] = None
    note: str
    octave: int = Field(4, ge=1, le=8)
    duration: float = Field(0.5, gt=0)
    velocity: float = Field(0.8, ge=0.0, le=1.0)
    quality: str = "good"


class PlaySongRequest(BaseModel):
    player_id: int
    song_id: str
    note_accuracies: List[float] = []


class SwitchInstrumentRequest(BaseModel):
    player_id: int
    instrument: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/play-note")
@handle_errors()
async def play_note(request: PlayNoteRequest, db: Session = Depends(get_db)):
    """
    Play Single Note (DATABASE)

    Body:
    {
        "player_id": 1,
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
            xp_gained: int,
            level: int,
            level_up: bool,
            quality: str
        }
    """
    try:
        progress = get_or_create_progress(db, request.player_id)

        # Parse instrument
        instrument_name = request.instrument or progress.current_instrument

        try:
            instrument = InstrumentType(instrument_name)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Ungültiges Instrument: {instrument_name}",
                    "valid_instruments": [i.value for i in InstrumentType]
                }
            )

        # Calculate XP
        xp_gained = calculate_xp_for_note(request.quality)

        # Get current stats
        skills = progress.instrument_skills or {}
        experience = progress.instrument_experience or {}

        current_xp = experience.get(instrument_name, 0)
        old_level = calculate_level_from_xp(current_xp)

        # Add XP
        new_xp = current_xp + xp_gained
        experience[instrument_name] = new_xp
        new_level = calculate_level_from_xp(new_xp)

        # Update skill level
        skills[instrument_name] = new_level

        # Update progress
        progress.instrument_skills = skills
        progress.instrument_experience = experience
        progress.total_notes_played += 1

        # Update quality counters
        if request.quality.lower() == "perfect":
            progress.perfect_notes += 1
        elif request.quality.lower() == "great":
            progress.great_notes += 1
        elif request.quality.lower() == "good":
            progress.good_notes += 1

        progress.last_played = datetime.utcnow()

        # Log played note
        played_note = PlayedNote(
            progress_id=progress.id,
            instrument=instrument_name,
            note=request.note,
            octave=request.octave,
            duration=request.duration,
            velocity=request.velocity,
            quality=request.quality,
            accuracy=sum(request.note_accuracies) / len(request.note_accuracies) if hasattr(request, 'note_accuracies') and request.note_accuracies else 0.8,
            played_at=datetime.utcnow()
        )

        db.add(played_note)
        db.commit()
        db.refresh(progress)

        # Calculate frequency (for audio playback)
        note_frequencies = {
            "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
            "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
            "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88
        }
        base_freq = note_frequencies.get(request.note.upper(), 440.0)
        octave_multiplier = 2 ** (request.octave - 4)
        frequency = base_freq * octave_multiplier

        return {
            "success": True,
            "note": request.note,
            "octave": request.octave,
            "frequency": frequency,
            "xp_gained": xp_gained,
            "level": new_level,
            "level_up": new_level > old_level,
            "quality": request.quality,
            "total_notes_played": progress.total_notes_played
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/play-song")
@handle_errors()
async def play_song(request: PlaySongRequest, db: Session = Depends(get_db)):
    """
    Play Complete Song (DATABASE)

    Body:
    {
        "player_id": 1,
        "song_id": "zelda_song_of_time",
        "note_accuracies": [0.95, 0.88, 0.92, ...]
    }

    Returns:
        song_data: {
            song_id: str,
            score: float,
            xp_gained: int,
            completed: bool,
            learned: bool
        }
    """
    try:
        progress = get_or_create_progress(db, request.player_id)

        # Check if song exists (using static system)
        song_data = instrument_system.get_song(request.song_id)
        if not song_data:
            raise HTTPException(status_code=404, detail=f"Song nicht gefunden: {request.song_id}")

        # Calculate score
        if request.note_accuracies:
            avg_accuracy = sum(request.note_accuracies) / len(request.note_accuracies)
        else:
            avg_accuracy = 0.7

        score = avg_accuracy * 100  # 0-100

        # Calculate XP based on song difficulty and score
        difficulty = song_data.get("difficulty", 1)
        xp_gained = int(difficulty * 50 * avg_accuracy)

        # Update instrument XP
        instrument_name = progress.current_instrument
        experience = progress.instrument_experience or {}
        current_xp = experience.get(instrument_name, 0)
        old_level = calculate_level_from_xp(current_xp)

        new_xp = current_xp + xp_gained
        experience[instrument_name] = new_xp
        new_level = calculate_level_from_xp(new_xp)

        # Update skills
        skills = progress.instrument_skills or {}
        skills[instrument_name] = new_level

        progress.instrument_skills = skills
        progress.instrument_experience = experience
        progress.last_played = datetime.utcnow()

        # Check if song completed (score >= 70%)
        completed = score >= 70.0

        # Check if already learned
        learned_songs_list = progress.learned_songs or []
        already_learned = request.song_id in learned_songs_list
        newly_learned = completed and not already_learned

        if newly_learned:
            learned_songs_list.append(request.song_id)
            progress.learned_songs = learned_songs_list

            # Create LearnedSong entry
            learned_song = LearnedSong(
                player_id=request.player_id,
                song_id=request.song_id,
                song_name=song_data.get("name", request.song_id),
                difficulty=difficulty,
                times_played=1,
                best_score=score,
                completed=True,
                learned_at=datetime.utcnow(),
                last_played=datetime.utcnow()
            )
            db.add(learned_song)
        else:
            # Update existing learned song
            learned_song = db.query(LearnedSong).filter(
                LearnedSong.player_id == request.player_id,
                LearnedSong.song_id == request.song_id
            ).first()

            if learned_song:
                learned_song.times_played += 1
                learned_song.best_score = max(learned_song.best_score, score)
                learned_song.completed = learned_song.completed or completed
                learned_song.last_played = datetime.utcnow()

        db.commit()
        db.refresh(progress)

        return {
            "success": True,
            "song_id": request.song_id,
            "score": round(score, 2),
            "xp_gained": xp_gained,
            "level": new_level,
            "level_up": new_level > old_level,
            "completed": completed,
            "learned": newly_learned or already_learned
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/switch")
@handle_errors()
async def switch_instrument(request: SwitchInstrumentRequest, db: Session = Depends(get_db)):
    """
    Switch Instrument (DATABASE)

    Body:
    {
        "player_id": 1,
        "instrument": "gitarre"
    }
    """
    try:
        progress = get_or_create_progress(db, request.player_id)

        # Validate instrument
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

        old_instrument = progress.current_instrument
        progress.current_instrument = request.instrument

        db.commit()
        db.refresh(progress)

        return {
            "success": True,
            "old_instrument": old_instrument,
            "new_instrument": request.instrument,
            "message": f"Gewechselt von {old_instrument} zu {request.instrument}"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs")
@handle_errors()
async def get_songs_alias():
    """
    Get All Songs - alias (Frontend: game_systems_ui.js InstrumentUI.loadSongs)

    Path: /api/instrument/songs
    """
    try:
        songs = instrument_system.get_all_songs()
        return {"songs": songs, "count": len(songs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs/all")
@handle_errors()
async def get_all_songs():
    """
    Get All Songs (static)

    Path: /api/instrument/songs/all
    """
    try:
        songs = instrument_system.get_all_songs()
        return {"songs": songs, "count": len(songs)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs/{song_id}")
@handle_errors()
async def get_song(song_id: str):
    """
    Get Specific Song (static)

    Path: /api/instrument/songs/zelda_song_of_time
    """
    try:
        song = instrument_system.get_song(song_id)

        if not song:
            raise HTTPException(status_code=404, detail=f"Song nicht gefunden: {song_id}")

        return song

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progress")
@handle_errors()
async def get_progress_default(player_id: int = Query(1), db: Session = Depends(get_db)):
    """
    Get Player Progress - default (Frontend: game_systems_ui.js InstrumentUI.loadProgress)

    Path: /api/instrument/progress?player_id=1
    """
    return await get_progress(player_id, db)


@router.get("/progress/{player_id}")
@handle_errors()
async def get_progress(player_id: int, db: Session = Depends(get_db)):
    """
    Get Player Progress (DATABASE)

    Path: /api/instrument/progress/1
    """
    try:
        progress = get_or_create_progress(db, player_id)

        # Get learned songs
        learned_songs = db.query(LearnedSong).filter(
            LearnedSong.player_id == player_id
        ).all()

        return {
            "player_id": player_id,
            "progress": progress.to_dict(),
            "learned_songs": [song.to_dict() for song in learned_songs],
            "learned_songs_count": len(learned_songs)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export/{player_id}")
@handle_errors()
async def export_state(player_id: int, db: Session = Depends(get_db)):
    """
    Export Complete State (DATABASE)

    Path: /api/instrument/state/export/1
    """
    try:
        progress = get_or_create_progress(db, player_id)

        # Get played notes (last 100)
        played_notes = db.query(PlayedNote).filter(
            PlayedNote.progress_id == progress.id
        ).order_by(
            PlayedNote.played_at.desc()
        ).limit(100).all()

        # Get learned songs
        learned_songs = db.query(LearnedSong).filter(
            LearnedSong.player_id == player_id
        ).all()

        return {
            "player_id": player_id,
            "progress": progress.to_dict(),
            "played_notes": [note.to_dict() for note in played_notes],
            "learned_songs": [song.to_dict() for song in learned_songs],
            "stats": {
                "total_notes": progress.total_notes_played,
                "perfect_notes": progress.perfect_notes,
                "great_notes": progress.great_notes,
                "good_notes": progress.good_notes,
                "learned_songs_count": len(learned_songs)
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# CATCH-ALL: Must be LAST to not intercept /songs, /progress, etc.
@router.get("/{instrument_type}")
@handle_errors()
async def get_instrument_info(instrument_type: str):
    """
    Get Instrument Info (static)

    Path: /api/instrument/mundharmonika
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