"""
Oregon Trail Events API - Najika World
=======================================

REST API für Oregon Trail Events System

Endpoints:
- GET /api/oregon/trigger - Trigger random event
- POST /api/oregon/choice - Execute player choice
- GET /api/oregon/chaos - Get chaos status
- POST /api/oregon/chaos/reduce - Reduce chaos
- GET /api/oregon/current - Get current active event

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from flask import Blueprint, request, jsonify

from backend.services.oregon_trail_events import OregonTrailEventsSystem

# Create Blueprint
oregon_bp = Blueprint('oregon', __name__, url_prefix='/api/oregon')

# Global System Instance
oregon_system = OregonTrailEventsSystem()


@oregon_bp.route('/trigger', methods=['GET'])
def trigger_event():
    """
    Trigger Random Event

    Query Params:
        location: str (optional, default "any")
        player_class: str (optional)

    Example: /api/oregon/trigger?location=wilderness&player_class=mage
    """
    try:
        location = request.args.get('location', 'any')
        player_class = request.args.get('player_class')

        event_data = oregon_system.trigger_random_event(location, player_class)

        if not event_data:
            return jsonify({
                "triggered": False,
                "message": "Kein Event getriggert"
            })

        return jsonify({
            "triggered": True,
            "event": event_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@oregon_bp.route('/choice', methods=['POST'])
def execute_choice():
    """
    Execute Player Choice

    Body:
    {
        "choice_index": 0,
        "player_state": {
            "gold": 100,
            "health": 80,
            ...
        }
    }
    """
    try:
        data = request.get_json()

        choice_index = data.get('choice_index')
        player_state = data.get('player_state', {})

        if choice_index is None:
            return jsonify({
                "error": "choice_index erforderlich"
            }), 400

        result = oregon_system.execute_choice(choice_index, player_state)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@oregon_bp.route('/chaos', methods=['GET'])
def get_chaos_status():
    """
    Get Chaos Status

    Returns current chaos level, points, Najika state
    """
    try:
        status = oregon_system.get_chaos_status()
        return jsonify(status)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@oregon_bp.route('/chaos/reduce', methods=['POST'])
def reduce_chaos():
    """
    Reduce Chaos

    Body:
    {
        "method": "meditation",  // meditation, temple_visit, lawful_quest, etc.
        "amount": 10  // optional, overrides default
    }
    """
    try:
        data = request.get_json()

        method = data.get('method')
        amount = data.get('amount')

        if not method:
            return jsonify({
                "error": "method erforderlich"
            }), 400

        result = oregon_system.chaos_calc.reduce_chaos(method, amount)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@oregon_bp.route('/current', methods=['GET'])
def get_current_event():
    """
    Get Current Active Event

    Returns current event or None
    """
    try:
        if not oregon_system.event_active or not oregon_system.current_event:
            return jsonify({
                "active": False,
                "message": "Kein aktives Event"
            })

        event = oregon_system._format_event_for_client(oregon_system.current_event)

        return jsonify({
            "active": True,
            "event": event
        })

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

    app.register_blueprint(oregon_bp)

    print("=" * 60)
    print("Oregon Trail Events API Server")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  GET    /api/oregon/trigger")
    print("  POST   /api/oregon/choice")
    print("  GET    /api/oregon/chaos")
    print("  POST   /api/oregon/chaos/reduce")
    print("  GET    /api/oregon/current")
    print()
    print("Server läuft auf: http://localhost:5005")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5005, debug=True)
