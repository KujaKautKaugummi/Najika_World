"""
Region Boss API - Najika World
===============================

REST API für Gebietsherrscher System

Endpoints:
- POST /api/region-boss/challenge/create - Create challenge
- POST /api/region-boss/challenge/accept - Accept challenge
- POST /api/region-boss/challenge/complete - Complete challenge
- POST /api/region-boss/conquest/progress - Add conquest progress
- POST /api/region-boss/tax/set - Set tax rate
- POST /api/region-boss/broadcast - Broadcast message
- GET /api/region-boss/region/<region> - Get region info
- GET /api/region-boss/ultimate - Get ultimate ruler info
- GET /api/region-boss/can-challenge - Check if can challenge
- GET /api/region-boss/state/export - Export state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from flask import Blueprint, request, jsonify

from backend.services.region_boss_system import (
    RegionBossSystem, Region, ConquestPath
)

# Create Blueprint
region_boss_bp = Blueprint('region_boss', __name__, url_prefix='/api/region-boss')

# Global System Instance
boss_system = RegionBossSystem()


@region_boss_bp.route('/challenge/create', methods=['POST'])
def create_challenge():
    """
    Create Challenge

    Body:
    {
        "challenger_id": 1,
        "region": "samtmoos_tiefwald",
        "challenge_type": "krieg",  // krieg, handel, diplomatie, quest_line
        "stakes": {},
        "conditions": {}
    }
    """
    try:
        data = request.get_json()

        challenger_id = data.get('challenger_id')
        region_str = data.get('region')
        challenge_type_str = data.get('challenge_type', 'krieg')

        if not challenger_id or not region_str:
            return jsonify({
                "error": "challenger_id und region erforderlich"
            }), 400

        # Parse region
        try:
            region = Region(region_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültige Region: {region_str}",
                "valid_regions": [r.value for r in Region]
            }), 400

        # Parse challenge type
        try:
            challenge_type = ConquestPath(challenge_type_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültiger Challenge-Typ: {challenge_type_str}",
                "valid_types": [c.value for c in ConquestPath]
            }), 400

        success, challenge_id, message = boss_system.create_challenge(
            challenger_id, region, challenge_type,
            stakes=data.get('stakes'),
            conditions=data.get('conditions')
        )

        if not success:
            return jsonify({
                "success": False,
                "message": message
            }), 400

        return jsonify({
            "success": True,
            "challenge_id": challenge_id,
            "message": message,
            "region": region.value,
            "type": challenge_type.value
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/challenge/accept', methods=['POST'])
def accept_challenge():
    """
    Accept Challenge

    Body:
    {
        "challenge_id": 1,
        "boss_player_id": 2
    }
    """
    try:
        data = request.get_json()

        challenge_id = data.get('challenge_id')
        boss_player_id = data.get('boss_player_id')

        if not challenge_id or not boss_player_id:
            return jsonify({
                "error": "challenge_id und boss_player_id erforderlich"
            }), 400

        success, message = boss_system.accept_challenge(challenge_id, boss_player_id)

        if not success:
            return jsonify({
                "success": False,
                "message": message
            }), 400

        return jsonify({
            "success": True,
            "message": message,
            "challenge_id": challenge_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/challenge/complete', methods=['POST'])
def complete_challenge():
    """
    Complete Challenge

    Body:
    {
        "challenge_id": 1,
        "winner_id": 2
    }
    """
    try:
        data = request.get_json()

        challenge_id = data.get('challenge_id')
        winner_id = data.get('winner_id')

        if not challenge_id or not winner_id:
            return jsonify({
                "error": "challenge_id und winner_id erforderlich"
            }), 400

        result = boss_system.complete_challenge(challenge_id, winner_id)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/conquest/progress', methods=['POST'])
def add_conquest_progress():
    """
    Add Conquest Progress (Handel/Diplomatie/Quest)

    Body:
    {
        "player_id": 1,
        "region": "samtmoos_tiefwald",
        "path": "handel",
        "progress": 25.0
    }
    """
    try:
        data = request.get_json()

        player_id = data.get('player_id')
        region_str = data.get('region')
        path_str = data.get('path')
        progress = data.get('progress', 0.0)

        if not all([player_id, region_str, path_str]):
            return jsonify({
                "error": "player_id, region, path erforderlich"
            }), 400

        # Parse region
        try:
            region = Region(region_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültige Region: {region_str}",
                "valid_regions": [r.value for r in Region]
            }), 400

        # Parse path
        try:
            path = ConquestPath(path_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültiger Pfad: {path_str}",
                "valid_paths": [c.value for c in ConquestPath]
            }), 400

        result = boss_system.add_conquest_progress(player_id, region, path, progress)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/tax/set', methods=['POST'])
def set_tax_rate():
    """
    Set Tax Rate (Boss only, 5-10%)

    Body:
    {
        "boss_player_id": 1,
        "region": "samtmoos_tiefwald",
        "tax_rate": 7.5
    }
    """
    try:
        data = request.get_json()

        boss_player_id = data.get('boss_player_id')
        region_str = data.get('region')
        tax_rate = data.get('tax_rate')

        if not all([boss_player_id, region_str, tax_rate is not None]):
            return jsonify({
                "error": "boss_player_id, region, tax_rate erforderlich"
            }), 400

        # Parse region
        try:
            region = Region(region_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültige Region: {region_str}"
            }), 400

        success, message = boss_system.set_tax_rate(boss_player_id, region, tax_rate)

        if not success:
            return jsonify({
                "success": False,
                "message": message
            }), 400

        return jsonify({
            "success": True,
            "message": message,
            "region": region.value,
            "tax_rate": tax_rate
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/broadcast', methods=['POST'])
def broadcast_message():
    """
    Broadcast Message (Boss only)

    Body:
    {
        "boss_player_id": 1,
        "region": "samtmoos_tiefwald",
        "message": "Willkommen!"
    }
    """
    try:
        data = request.get_json()

        boss_player_id = data.get('boss_player_id')
        region_str = data.get('region')
        message = data.get('message')

        if not all([boss_player_id, region_str, message]):
            return jsonify({
                "error": "boss_player_id, region, message erforderlich"
            }), 400

        # Parse region
        try:
            region = Region(region_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültige Region: {region_str}"
            }), 400

        success, broadcast = boss_system.broadcast_message(
            boss_player_id, region, message
        )

        if not success:
            return jsonify({
                "success": False,
                "message": broadcast
            }), 400

        return jsonify({
            "success": True,
            "broadcast": broadcast,
            "region": region.value
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/region/<region>', methods=['GET'])
def get_region_info(region: str):
    """
    Get Region Info

    Path: /api/region-boss/region/samtmoos_tiefwald
    """
    try:
        # Parse region
        try:
            region_enum = Region(region)
        except ValueError:
            return jsonify({
                "error": f"Ungültige Region: {region}",
                "valid_regions": [r.value for r in Region]
            }), 400

        info = boss_system.get_region_info(region_enum)

        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/ultimate', methods=['GET'])
def get_ultimate_ruler():
    """
    Get Ultimate Ruler Info

    Path: /api/region-boss/ultimate
    """
    try:
        info = boss_system.get_ultimate_ruler_info()
        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/can-challenge', methods=['GET'])
def check_can_challenge():
    """
    Check if can challenge

    Query Params:
        challenger_id: int
        region: str

    Example: /api/region-boss/can-challenge?challenger_id=1&region=samtmoos_tiefwald
    """
    try:
        challenger_id = request.args.get('challenger_id', type=int)
        region_str = request.args.get('region')

        if not challenger_id or not region_str:
            return jsonify({
                "error": "challenger_id und region erforderlich"
            }), 400

        # Parse region
        try:
            region = Region(region_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültige Region: {region_str}"
            }), 400

        can_challenge, reason = boss_system.can_challenge_boss(challenger_id, region)

        return jsonify({
            "can_challenge": can_challenge,
            "reason": reason,
            "challenger_id": challenger_id,
            "region": region.value
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@region_boss_bp.route('/state/export', methods=['GET'])
def export_state():
    """
    Export State

    Returns:
        JSON with all region bosses, ultimate ruler
    """
    try:
        state = boss_system.export_state()
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

    app.register_blueprint(region_boss_bp)

    print("=" * 60)
    print("Region Boss API Server")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  POST   /api/region-boss/challenge/create")
    print("  POST   /api/region-boss/challenge/accept")
    print("  POST   /api/region-boss/challenge/complete")
    print("  POST   /api/region-boss/conquest/progress")
    print("  POST   /api/region-boss/tax/set")
    print("  POST   /api/region-boss/broadcast")
    print("  GET    /api/region-boss/region/<region>")
    print("  GET    /api/region-boss/ultimate")
    print("  GET    /api/region-boss/can-challenge")
    print("  GET    /api/region-boss/state/export")
    print()
    print("Server läuft auf: http://localhost:5004")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5004, debug=True)
