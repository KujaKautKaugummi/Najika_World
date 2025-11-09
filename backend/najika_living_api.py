#!/usr/bin/env python3
"""
NAJIKA LIVING SYSTEM - REST API

Endpoints für das Living System (Hunger/Energy/Mood/Anger/Unfälle)
Integration mit najika_server.py

Author: Claude Code
Date: 2025-11-09
"""

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import time
import json
from pathlib import Path

# Import Living System
from najika_living_system import (
    LIVING_STATE,
    update_living_system,
    player_feeds_najika,
    player_puts_najika_to_bed,
    set_control_mode,
    get_greeting_message,
    export_living_state,
    import_living_state
)

# Blueprint für Integration in najika_server.py
living_api = Blueprint('living_api', __name__, url_prefix='/api/living')

# ===== STATE MANAGEMENT =====

# In-Memory State (wird später in DB/File gespeichert)
current_living_state = LIVING_STATE.copy()

# State-File Pfad
STATE_FILE = Path(__file__).parent / "saves" / "najika_living_state.json"

def load_state():
    """Lädt State aus File"""
    global current_living_state
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                data = f.read()
                current_living_state = import_living_state(data)
                print(f"[OK] Living State geladen aus {STATE_FILE}")
        except Exception as e:
            print(f"[WARNING] Fehler beim Laden: {e}")
            current_living_state = LIVING_STATE.copy()
    else:
        print("[INFO] Kein State-File gefunden, starte mit Default-State")
        current_living_state = LIVING_STATE.copy()

def save_state():
    """Speichert State in File"""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            f.write(export_living_state(current_living_state))
        return True
    except Exception as e:
        print(f"[WARNING] Fehler beim Speichern: {e}")
        return False

# ===== API ENDPOINTS =====

@living_api.route('/status', methods=['GET'])
def get_status():
    """
    Holt aktuellen Living State

    GET /api/living/status

    Returns:
    {
        "hunger": 85.5,
        "energy": 92.0,
        "mood_game": 78.3,
        "anger_level": 12.5,
        "control_mode": "ai",
        "player_online": false,
        "last_accident": null,
        "accidents_today": 0,
        ...
    }
    """
    # Update State bevor Return
    results = update_living_system(current_living_state)

    # Save nach Update
    save_state()

    response = {
        "status": "ok",
        "timestamp": time.time(),
        "state": {
            "hunger": current_living_state["hunger"],
            "energy": current_living_state["energy"],
            "mood_game": current_living_state["mood_game"],
            "anger_level": current_living_state["anger_level"],
            "control_mode": current_living_state["control_mode"],
            "player_online": current_living_state["player_online"],
            "last_accident": current_living_state["last_accident"],
            "accidents_today": current_living_state["accidents_today"],
            "current_mood": current_living_state["current_mood"],
            "relationship_stage": current_living_state["relationship_stage"],
            "emotional_bond": current_living_state["emotional_bond"]
        },
        "update_results": results
    }

    return jsonify(response)

@living_api.route('/update', methods=['POST'])
def force_update():
    """
    Forciert Living System Update

    POST /api/living/update

    Returns:
    {
        "needs_updated": true,
        "auto_care_actions": [...],
        "accidents": [...],
        "warnings": [...]
    }
    """
    results = update_living_system(current_living_state)
    save_state()

    return jsonify({
        "status": "ok",
        "results": results,
        "state": {
            "hunger": current_living_state["hunger"],
            "energy": current_living_state["energy"],
            "anger_level": current_living_state["anger_level"]
        }
    })

@living_api.route('/feed', methods=['POST'])
def feed_najika():
    """
    Spieler füttert Najika

    POST /api/living/feed
    Body: {
        "food_value": 30  // Optional (default: 30)
    }

    Returns:
    {
        "action": "player_feeds",
        "hunger_before": 45.0,
        "hunger_after": 75.0,
        "anger_level": 8.0,
        "najika_says": "Danke! Das schmeckt super! 😋"
    }
    """
    data = request.get_json() or {}
    food_value = data.get("food_value", 30)

    result = player_feeds_najika(current_living_state, food_value)
    save_state()

    return jsonify({
        "status": "ok",
        "result": result,
        "state": {
            "hunger": current_living_state["hunger"],
            "anger_level": current_living_state["anger_level"]
        }
    })

@living_api.route('/sleep', methods=['POST'])
def put_to_bed():
    """
    Spieler legt Najika ins Bett

    POST /api/living/sleep

    Returns:
    {
        "action": "player_bed",
        "energy_before": 35.0,
        "energy_after": 100.0,
        "anger_level": 5.0,
        "najika_says": "Danke... so kuschelig... 😴💤"
    }
    """
    result = player_puts_najika_to_bed(current_living_state)
    save_state()

    return jsonify({
        "status": "ok",
        "result": result,
        "state": {
            "energy": current_living_state["energy"],
            "anger_level": current_living_state["anger_level"]
        }
    })

@living_api.route('/control', methods=['POST'])
def set_control():
    """
    Setzt Control-Mode (AI vs Player)

    POST /api/living/control
    Body: {
        "mode": "player",  // "ai" oder "player"
        "online": true
    }

    Returns:
    {
        "control_mode": "player",
        "player_online": true,
        "message": "Najika wird jetzt von dir gesteuert"
    }
    """
    data = request.get_json()
    mode = data.get("mode", "ai")
    online = data.get("online", False)

    result = set_control_mode(current_living_state, mode, online)
    save_state()

    return jsonify({
        "status": "ok",
        "result": result
    })

@living_api.route('/greeting', methods=['GET'])
def get_greeting():
    """
    Holt Begrüßungs-Nachricht (basierend auf Anger & Abwesenheit)

    GET /api/living/greeting

    Returns:
    {
        "greeting": "Hey! Schon zurück? 😊",
        "anger_level": 5.0,
        "hours_offline": 2.3
    }
    """
    greeting = get_greeting_message(current_living_state)

    last_interaction = current_living_state.get("last_interaction", time.time())
    hours_offline = (time.time() - last_interaction) / 3600.0

    return jsonify({
        "status": "ok",
        "greeting": greeting,
        "anger_level": current_living_state["anger_level"],
        "hours_offline": hours_offline
    })

@living_api.route('/state/export', methods=['GET'])
def export_state():
    """
    Exportiert kompletten State als JSON

    GET /api/living/state/export

    Returns: Full JSON State
    """
    return jsonify({
        "status": "ok",
        "state": current_living_state
    })

@living_api.route('/state/import', methods=['POST'])
def import_state():
    """
    Importiert State aus JSON

    POST /api/living/state/import
    Body: {
        "state": {...}
    }

    Returns:
    {
        "status": "ok",
        "message": "State importiert"
    }
    """
    global current_living_state

    data = request.get_json()
    state_data = data.get("state")

    if not state_data:
        return jsonify({"status": "error", "message": "Kein State bereitgestellt"}), 400

    try:
        # Merge mit Default State
        current_living_state = {**LIVING_STATE, **state_data}
        save_state()

        return jsonify({
            "status": "ok",
            "message": "State erfolgreich importiert"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Fehler beim Import: {str(e)}"
        }), 500

@living_api.route('/stats', methods=['GET'])
def get_stats():
    """
    Holt Statistiken

    GET /api/living/stats

    Returns:
    {
        "total_time_together": 86400,  // Sekunden
        "days_since_meeting": 1,
        "accidents_today": 2,
        "activities_completed": 12,
        "relationship_stage": "friends",
        "emotional_bond": 45.0
    }
    """
    return jsonify({
        "status": "ok",
        "stats": {
            "total_time_together": current_living_state.get("total_time_together", 0),
            "days_since_meeting": current_living_state.get("days_since_meeting", 0),
            "accidents_today": current_living_state.get("accidents_today", 0),
            "activities_completed": len(current_living_state.get("activities_completed", [])),
            "relationship_stage": current_living_state.get("relationship_stage", "getting_to_know"),
            "emotional_bond": current_living_state.get("emotional_bond", 0),
            "personality_evolution": current_living_state.get("personality_evolution", {})
        }
    })

# ===== STANDALONE FLASK APP (für Testing) =====

if __name__ == '__main__':
    # Erstelle Standalone Flask App für Testing
    app = Flask(__name__)
    CORS(app)

    # Register Blueprint
    app.register_blueprint(living_api)

    # Load State
    load_state()

    print("=" * 60)
    print(">>> Najika Living System API")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  GET  /api/living/status       - Aktueller Status")
    print("  POST /api/living/update       - Force Update")
    print("  POST /api/living/feed         - Najika füttern")
    print("  POST /api/living/sleep        - Najika ins Bett")
    print("  POST /api/living/control      - Control-Mode setzen")
    print("  GET  /api/living/greeting     - Begrüßung holen")
    print("  GET  /api/living/state/export - State exportieren")
    print("  POST /api/living/state/import - State importieren")
    print("  GET  /api/living/stats        - Statistiken")
    print()
    print("Current State:")
    print(f"  Hunger: {current_living_state['hunger']:.1f}%")
    print(f"  Energy: {current_living_state['energy']:.1f}%")
    print(f"  Mood: {current_living_state['mood_game']:.1f}%")
    print(f"  Anger: {current_living_state['anger_level']:.1f}%")
    print()
    print("Server läuft auf: http://localhost:5001")
    print("=" * 60)

    # Run Server
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
