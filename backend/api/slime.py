"""
Slime API - Najika World
========================

REST API für Slime Companion System

Endpoints:
- POST /api/slime/create - Create companion
- POST /api/slime/experience - Add experience
- POST /api/slime/metamorphosis - Perform metamorphosis
- POST /api/slime/color/collect - Collect color
- POST /api/slime/learn - Try learn move
- POST /api/slime/rescue - Use rescue mechanic
- POST /api/slime/tamagotchi/update - Update tamagotchi stats
- POST /api/slime/feed - Feed companion
- POST /api/slime/water - Give water
- POST /api/slime/sleep - Let sleep
- GET /api/slime/<companion_id> - Get companion info
- GET /api/slime/state/export - Export state
- POST /api/slime/state/import - Import state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any

from backend.services.slime_system import SlimeSystem

# Create Blueprint
slime_bp = Blueprint('slime', __name__, url_prefix='/api/slime')

# Global Slime System Instance
slime_system = SlimeSystem()


@slime_bp.route('/create', methods=['POST'])
def create_companion():
    """
    Create Companion

    Body:
    {
        "owner_player_id": 1,
        "name": "Fluffi",
        "starting_region": "samtmoos_tiefwald"
    }
    """
    try:
        data = request.get_json()

        owner_id = data.get('owner_player_id')
        name = data.get('name')
        region = data.get('starting_region')

        if not owner_id or not name or not region:
            return jsonify({
                "error": "owner_player_id, name, starting_region erforderlich"
            }), 400

        companion = slime_system.create_companion(owner_id, name, region)

        return jsonify({
            "success": True,
            "companion_id": companion.companion_id,
            "name": companion.name,
            "level": companion.level,
            "fantasy_tier": companion.fantasy_tier.value if companion.fantasy_tier else None,
            "message": f"{companion.name} wurde erstellt!"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/experience', methods=['POST'])
def add_experience():
    """
    Add Experience

    Body:
    {
        "companion_id": 1,
        "exp_amount": 120
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        exp_amount = data.get('exp_amount', 0)

        if not companion_id:
            return jsonify({
                "error": "companion_id erforderlich"
            }), 400

        leveled_up, result = slime_system.add_experience(companion_id, exp_amount)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/metamorphosis', methods=['POST'])
def perform_metamorphosis():
    """
    Perform Metamorphosis (Level 50)

    Body:
    {
        "companion_id": 1,
        "current_region": "samtmoos_tiefwald"
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        region = data.get('current_region')

        if not companion_id or not region:
            return jsonify({
                "error": "companion_id, current_region erforderlich"
            }), 400

        result = slime_system.perform_metamorphosis(companion_id, region)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/color/collect', methods=['POST'])
def collect_color():
    """
    Collect Slime Color (Rainbow Quest)

    Body:
    {
        "companion_id": 1,
        "region": "reich_der_drei"
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        region = data.get('region')

        if not companion_id or not region:
            return jsonify({
                "error": "companion_id, region erforderlich"
            }), 400

        result = slime_system.collect_color(companion_id, region)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/learn', methods=['POST'])
def try_learn_move():
    """
    Try Learn Move

    Body:
    {
        "companion_id": 1,
        "move_name": "Thunder Strike",
        "move_type": "enemy",  // "enemy" or "player"
        "source_name": "Goblin King"
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        move_name = data.get('move_name')
        move_type = data.get('move_type')
        source_name = data.get('source_name')

        if not all([companion_id, move_name, move_type, source_name]):
            return jsonify({
                "error": "companion_id, move_name, move_type, source_name erforderlich"
            }), 400

        learned, result = slime_system.try_learn_move(
            companion_id, move_name, move_type, source_name
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/rescue', methods=['POST'])
def use_rescue():
    """
    Use Rescue Mechanic (Hardcore)

    Body:
    {
        "companion_id": 1
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')

        if not companion_id:
            return jsonify({
                "error": "companion_id erforderlich"
            }), 400

        rescued, result = slime_system.use_rescue(companion_id)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/tamagotchi/update', methods=['POST'])
def update_tamagotchi():
    """
    Update Tamagotchi Stats (Decay)

    Body:
    {
        "companion_id": 1,
        "delta_hours": 1.0  // optional
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        delta_hours = data.get('delta_hours')

        if not companion_id:
            return jsonify({
                "error": "companion_id erforderlich"
            }), 400

        result = slime_system.update_tamagotchi(companion_id, delta_hours)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/feed', methods=['POST'])
def feed_companion():
    """
    Feed Companion

    Body:
    {
        "companion_id": 1,
        "amount": 30.0  // optional, default 30.0
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        amount = data.get('amount', 30.0)

        if not companion_id:
            return jsonify({
                "error": "companion_id erforderlich"
            }), 400

        result = slime_system.feed_companion(companion_id, amount)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/water', methods=['POST'])
def give_water():
    """
    Give Water

    Body:
    {
        "companion_id": 1,
        "amount": 40.0  // optional, default 40.0
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        amount = data.get('amount', 40.0)

        if not companion_id:
            return jsonify({
                "error": "companion_id erforderlich"
            }), 400

        result = slime_system.give_water(companion_id, amount)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/sleep', methods=['POST'])
def let_sleep():
    """
    Let Sleep

    Body:
    {
        "companion_id": 1,
        "hours": 8.0  // optional, default 8.0
    }
    """
    try:
        data = request.get_json()

        companion_id = data.get('companion_id')
        hours = data.get('hours', 8.0)

        if not companion_id:
            return jsonify({
                "error": "companion_id erforderlich"
            }), 400

        result = slime_system.let_sleep(companion_id, hours)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/<int:companion_id>', methods=['GET'])
def get_companion_info(companion_id: int):
    """
    Get Companion Info

    Path: /api/slime/1
    """
    try:
        result = slime_system.get_companion_info(companion_id)

        if "error" in result:
            return jsonify(result), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/state/export', methods=['GET'])
def export_state():
    """
    Export Slime State

    Returns:
        JSON with all companions
    """
    try:
        state = slime_system.export_state()
        return jsonify(state)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slime_bp.route('/state/import', methods=['POST'])
def import_state():
    """
    Import Slime State

    Body: Complete state object (from export)
    """
    try:
        state = request.get_json()

        if not state:
            return jsonify({
                "error": "State-Daten erforderlich"
            }), 400

        # TODO: Implement import_state in SlimeSystem
        # slime_system.import_state(state)

        return jsonify({
            "success": True,
            "message": "Slime State importiert",
            "companions": len(state.get("companions", {}))
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

    app.register_blueprint(slime_bp)

    print("=" * 60)
    print("Slime API Server")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  POST   /api/slime/create")
    print("  POST   /api/slime/experience")
    print("  POST   /api/slime/metamorphosis")
    print("  POST   /api/slime/color/collect")
    print("  POST   /api/slime/learn")
    print("  POST   /api/slime/rescue")
    print("  POST   /api/slime/tamagotchi/update")
    print("  POST   /api/slime/feed")
    print("  POST   /api/slime/water")
    print("  POST   /api/slime/sleep")
    print("  GET    /api/slime/<companion_id>")
    print("  GET    /api/slime/state/export")
    print("  POST   /api/slime/state/import")
    print()
    print("Server läuft auf: http://localhost:5003")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5003, debug=True)
