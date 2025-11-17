"""
PvP API - Najika World
======================

REST API für PvP System

Endpoints:
- POST /api/pvp/battle/start - Start PvP Battle
- POST /api/pvp/battle/end - End PvP Battle
- POST /api/pvp/mercy/decide - Mercy Decision
- POST /api/pvp/normal/item-loss - Select random item loss (Normal PvP)
- GET /api/pvp/rankings/<mode> - Get rankings
- GET /api/pvp/stats/<player_id> - Get player stats
- GET /api/pvp/can-pvp - Check if can start PvP
- GET /api/pvp/state/export - Export state
- POST /api/pvp/state/import - Import state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import json

from backend.services.pvp_system import PvPSystem, PvPMode

# Create Blueprint
pvp_bp = Blueprint('pvp', __name__, url_prefix='/api/pvp')

# Global PvP System Instance
pvp_system = PvPSystem()


@pvp_bp.route('/battle/start', methods=['POST'])
def start_battle():
    """
    Start PvP Battle

    Body:
    {
        "attacker_id": 1,
        "defender_id": 2,
        "mode": "hardcore"  // "hardcore", "normal", "softy"
    }
    """
    try:
        data = request.get_json()

        attacker_id = data.get('attacker_id')
        defender_id = data.get('defender_id')
        mode_str = data.get('mode', 'normal')

        if not attacker_id or not defender_id:
            return jsonify({
                "error": "attacker_id und defender_id erforderlich"
            }), 400

        # Parse mode
        try:
            mode = PvPMode(mode_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültiger Modus: {mode_str}",
                "valid_modes": ["hardcore", "normal", "softy"]
            }), 400

        # Start battle
        success, battle_id, message = pvp_system.start_pvp_battle(
            attacker_id, defender_id, mode
        )

        if not success:
            return jsonify({
                "success": False,
                "message": message
            }), 400

        return jsonify({
            "success": True,
            "battle_id": battle_id,
            "message": message,
            "mode": mode.value
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/battle/end', methods=['POST'])
def end_battle():
    """
    End PvP Battle

    Body:
    {
        "battle_id": 1,
        "winner_id": 1,
        "battle_duration": 120.5
    }
    """
    try:
        data = request.get_json()

        battle_id = data.get('battle_id')
        winner_id = data.get('winner_id')
        battle_duration = data.get('battle_duration', 0.0)

        if not battle_id or not winner_id:
            return jsonify({
                "error": "battle_id und winner_id erforderlich"
            }), 400

        result = pvp_system.end_pvp_battle(battle_id, winner_id, battle_duration)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/mercy/decide', methods=['POST'])
def mercy_decision():
    """
    Process Mercy Decision (Hardcore PvP only)

    Body:
    {
        "battle_id": 1,
        "player_id": 2,
        "accept_mercy": true,
        "player_inventory": [
            {"name": "Schwert", "rarity": "epic"},
            {"name": "Trank", "rarity": "common"}
        ]
    }
    """
    try:
        data = request.get_json()

        battle_id = data.get('battle_id')
        player_id = data.get('player_id')
        accept_mercy = data.get('accept_mercy')
        player_inventory = data.get('player_inventory', [])

        if battle_id is None or player_id is None or accept_mercy is None:
            return jsonify({
                "error": "battle_id, player_id, accept_mercy erforderlich"
            }), 400

        result = pvp_system.process_mercy_decision(
            battle_id, player_id, accept_mercy, player_inventory
        )

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/normal/item-loss', methods=['POST'])
def normal_item_loss():
    """
    Select Random Item Loss (Normal PvP only)

    Body:
    {
        "battle_id": 1,
        "player_inventory": [
            {"name": "Schwert", "rarity": "common"}
        ]
    }
    """
    try:
        data = request.get_json()

        battle_id = data.get('battle_id')
        player_inventory = data.get('player_inventory', [])

        if not battle_id:
            return jsonify({
                "error": "battle_id erforderlich"
            }), 400

        result = pvp_system.select_random_item_loss(battle_id, player_inventory)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/rankings/<mode>', methods=['GET'])
def get_rankings(mode: str):
    """
    Get Rankings for PvP Mode

    Path: /api/pvp/rankings/hardcore
    Path: /api/pvp/rankings/normal
    Path: /api/pvp/rankings/softy
    """
    try:
        # Parse mode
        try:
            pvp_mode = PvPMode(mode)
        except ValueError:
            return jsonify({
                "error": f"Ungültiger Modus: {mode}",
                "valid_modes": ["hardcore", "normal", "softy"]
            }), 400

        rankings = pvp_system.get_pvp_rankings(pvp_mode)

        return jsonify({
            "mode": mode,
            "rankings": rankings,
            "total_players": len(rankings)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/stats/<int:player_id>', methods=['GET'])
def get_player_stats(player_id: int):
    """
    Get Player PvP Stats

    Path: /api/pvp/stats/1
    """
    try:
        stats = pvp_system.get_player_pvp_stats(player_id)
        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/can-pvp', methods=['GET'])
def check_can_pvp():
    """
    Check if PvP can be initiated

    Query Params:
        attacker_id: int
        defender_id: int
        mode: str (hardcore/normal/softy)

    Example: /api/pvp/can-pvp?attacker_id=1&defender_id=2&mode=hardcore
    """
    try:
        attacker_id = request.args.get('attacker_id', type=int)
        defender_id = request.args.get('defender_id', type=int)
        mode_str = request.args.get('mode', 'normal')

        if not attacker_id or not defender_id:
            return jsonify({
                "error": "attacker_id und defender_id erforderlich"
            }), 400

        # Parse mode
        try:
            mode = PvPMode(mode_str)
        except ValueError:
            return jsonify({
                "error": f"Ungültiger Modus: {mode_str}",
                "valid_modes": ["hardcore", "normal", "softy"]
            }), 400

        can_start, reason = pvp_system.can_initiate_pvp(attacker_id, defender_id, mode)

        return jsonify({
            "can_start": can_start,
            "reason": reason,
            "attacker_id": attacker_id,
            "defender_id": defender_id,
            "mode": mode.value
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/state/export', methods=['GET'])
def export_state():
    """
    Export complete PvP state

    Returns:
        JSON with all battles, player stats, etc.
    """
    try:
        state = pvp_system.export_state()
        return jsonify(state)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pvp_bp.route('/state/import', methods=['POST'])
def import_state():
    """
    Import PvP state

    Body: Complete state object (from export)
    """
    try:
        state = request.get_json()

        if not state:
            return jsonify({
                "error": "State-Daten erforderlich"
            }), 400

        pvp_system.import_state(state)

        return jsonify({
            "success": True,
            "message": "PvP State importiert",
            "battles": len(pvp_system.battles),
            "players": len(pvp_system.player_stats)
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

    app.register_blueprint(pvp_bp)

    print("=" * 60)
    print("PvP API Server")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  POST   /api/pvp/battle/start")
    print("  POST   /api/pvp/battle/end")
    print("  POST   /api/pvp/mercy/decide")
    print("  POST   /api/pvp/normal/item-loss")
    print("  GET    /api/pvp/rankings/<mode>")
    print("  GET    /api/pvp/stats/<player_id>")
    print("  GET    /api/pvp/can-pvp")
    print("  GET    /api/pvp/state/export")
    print("  POST   /api/pvp/state/import")
    print()
    print("Server läuft auf: http://localhost:5002")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5002, debug=True)
