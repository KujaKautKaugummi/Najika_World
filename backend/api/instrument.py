"""
Instrument Playing API - Najika World
======================================

REST API für Spielbares Instrument System

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

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from flask import Blueprint, request, jsonify

from backend.services.instrument_system import (
    InstrumentPlayingSystem, InstrumentType, Note, NoteQuality
)

# Create Blueprint
instrument_bp = Blueprint('instrument', __name__, url_prefix='/api/instrument')

# Global System Instance
instrument_system = InstrumentPlayingSystem()


@instrument_bp.route('/play-note', methods=['POST'])
def play_note():
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
        data = request.get_json()

        # Parse instrument (optional)
        instrument = None
        if data.get('instrument'):
            try:
                instrument = InstrumentType(data['instrument'])
            except ValueError:
                return jsonify({
                    "error": f"Ungültiges Instrument: {data['instrument']}",
                    "valid_instruments": [i.value for i in InstrumentType]
                }), 400
        else:
            instrument = instrument_system.current_instrument

        # Parse note
        note_str = data.get('note')
        if not note_str:
            return jsonify({"error": "note erforderlich"}), 400

        try:
            note = Note(note_str.upper())
        except ValueError:
            return jsonify({
                "error": f"Ungültige Note: {note_str}",
                "valid_notes": [n.value for n in Note]
            }), 400

        # Parse octave
        octave = data.get('octave', 4)
        if not (1 <= octave <= 8):
            return jsonify({
                "error": "octave muss zwischen 1 und 8 liegen"
            }), 400

        # Parse duration
        duration = data.get('duration', 0.5)
        if duration <= 0:
            return jsonify({"error": "duration muss > 0 sein"}), 400

        # Parse velocity
        velocity = data.get('velocity', 0.8)
        if not (0.0 <= velocity <= 1.0):
            return jsonify({
                "error": "velocity muss zwischen 0.0 und 1.0 liegen"
            }), 400

        # Parse quality
        quality = NoteQuality.GOOD
        if data.get('quality'):
            try:
                quality = NoteQuality(data['quality'])
            except ValueError:
                return jsonify({
                    "error": f"Ungültige Quality: {data['quality']}",
                    "valid_qualities": [q.value for q in NoteQuality]
                }), 400

        # Play note!
        result = instrument_system.play_note(
            instrument, note, octave, duration, velocity, quality
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@instrument_bp.route('/play-song', methods=['POST'])
def play_song():
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
        data = request.get_json()

        song_id = data.get('song_id')
        if not song_id:
            return jsonify({"error": "song_id erforderlich"}), 400

        note_accuracies = data.get('note_accuracies', [])
        if not isinstance(note_accuracies, list):
            return jsonify({
                "error": "note_accuracies muss eine Liste sein"
            }), 400

        # Play song!
        result = instrument_system.play_song(song_id, note_accuracies)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@instrument_bp.route('/switch', methods=['POST'])
def switch_instrument():
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
        data = request.get_json()

        instrument_str = data.get('instrument')
        if not instrument_str:
            return jsonify({"error": "instrument erforderlich"}), 400

        try:
            instrument = InstrumentType(instrument_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültiges Instrument: {instrument_str}",
                "valid_instruments": [i.value for i in InstrumentType]
            }), 400

        result = instrument_system.switch_instrument(instrument)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@instrument_bp.route('/<instrument_type>', methods=['GET'])
def get_instrument_info(instrument_type: str):
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
            return jsonify({
                "error": f"Ungültiges Instrument: {instrument_type}",
                "valid_instruments": [i.value for i in InstrumentType]
            }), 400

        info = instrument_system.get_instrument_info(instrument)

        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@instrument_bp.route('/songs', methods=['GET'])
def get_all_songs():
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
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')

        songs = instrument_system.get_all_songs(category, difficulty)

        return jsonify({
            "songs": songs,
            "count": len(songs)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@instrument_bp.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id: str):
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
            return jsonify({
                "error": f"Song nicht gefunden: {song_id}"
            }), 404

        return jsonify(song)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@instrument_bp.route('/progress', methods=['GET'])
def get_progress():
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

        return jsonify(progress)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@instrument_bp.route('/state/export', methods=['GET'])
def export_state():
    """
    Export State

    Returns:
        JSON with complete instrument state
    """
    try:
        state = instrument_system.export_state()
        return jsonify(state)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# STANDALONE SERVER (für Testing)
# ============================================================================

if __name__ == '__main__':
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(instrument_bp)

    print("=" * 60)
    print("Instrument Playing API Server")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  POST   /api/instrument/play-note")
    print("  POST   /api/instrument/play-song")
    print("  POST   /api/instrument/switch")
    print("  GET    /api/instrument/<type>")
    print("  GET    /api/instrument/songs")
    print("  GET    /api/instrument/songs/<song_id>")
    print("  GET    /api/instrument/progress")
    print("  GET    /api/instrument/state/export")
    print()
    print("Server läuft auf: http://localhost:5006")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5006, debug=True)
