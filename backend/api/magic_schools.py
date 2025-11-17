"""
Magic Schools API - Najika World
=================================

REST API für 9 Magieschulen System

Endpoints:
- POST /api/magic/cast - Cast spell (Skyrim Learning!)
- GET /api/magic/school/<school> - Get school info
- GET /api/magic/overview - Get all schools overview
- GET /api/magic/can-weave - Check if can weave
- GET /api/magic/spells - Get all spells
- GET /api/magic/state/export - Export state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from flask import Blueprint, request, jsonify

from backend.services.magic_schools_system import (
    MagicSchoolSystem, MagicSchool
)

# Create Blueprint
magic_bp = Blueprint('magic', __name__, url_prefix='/api/magic')

# Global System Instance
magic_system = MagicSchoolSystem()

# Initialize default spells
magic_system.create_default_spells()


@magic_bp.route('/cast', methods=['POST'])
def cast_spell():
    """
    Cast Spell (Skyrim Learning by Doing!)

    Body:
    {
        "spell_id": "fire_novice_1",
        "damage_dealt": 25.0
    }
    """
    try:
        data = request.get_json()

        spell_id = data.get('spell_id')
        damage_dealt = data.get('damage_dealt', 0.0)

        if not spell_id:
            return jsonify({
                "error": "spell_id erforderlich"
            }), 400

        result = magic_system.cast_spell(spell_id, damage_dealt)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@magic_bp.route('/school/<school>', methods=['GET'])
def get_school_info(school: str):
    """
    Get School Info

    Path: /api/magic/school/feuer
    """
    try:
        # Parse school
        try:
            magic_school = MagicSchool(school)
        except ValueError:
            return jsonify({
                "error": f"Ungültige Schule: {school}",
                "valid_schools": [s.value for s in MagicSchool]
            }), 400

        info = magic_system.get_school_info(magic_school)

        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@magic_bp.route('/overview', methods=['GET'])
def get_overview():
    """
    Get All Schools Overview

    Returns summary for all 9 schools
    """
    try:
        overview = magic_system.get_all_schools_overview()
        return jsonify(overview)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@magic_bp.route('/can-weave', methods=['GET'])
def check_can_weave():
    """
    Check if can weave (combine) 2 schools

    Query Params:
        school1: str
        school2: str

    Example: /api/magic/can-weave?school1=feuer&school2=eis

    WICHTIG: Explosion NIEMALS kombinierbar! (Gebot #3)
    """
    try:
        school1_str = request.args.get('school1')
        school2_str = request.args.get('school2')

        if not school1_str or not school2_str:
            return jsonify({
                "error": "school1 und school2 erforderlich"
            }), 400

        # Parse schools
        try:
            school1 = MagicSchool(school1_str)
            school2 = MagicSchool(school2_str)
        except ValueError as e:
            return jsonify({
                "error": f"Ungültige Schule: {e}",
                "valid_schools": [s.value for s in MagicSchool]
            }), 400

        can_weave, reason = magic_system.can_weave(school1, school2)

        return jsonify({
            "can_weave": can_weave,
            "reason": reason,
            "school1": school1.value,
            "school2": school2.value
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@magic_bp.route('/spells', methods=['GET'])
def get_all_spells():
    """
    Get All Spells

    Optional Query Params:
        school: str (filter by school)
        unlocked_only: bool (only show unlocked)
    """
    try:
        school_filter = request.args.get('school')
        unlocked_only = request.args.get('unlocked_only', 'false').lower() == 'true'

        spells_list = []

        for spell_id, spell in magic_system.spells.items():
            # School filter
            if school_filter and spell.school.value != school_filter:
                continue

            # Unlocked filter
            if unlocked_only:
                progress = magic_system.school_progress[spell.school]
                if spell_id not in progress.unlocked_spells:
                    continue

            spells_list.append({
                "spell_id": spell.spell_id,
                "name": spell.name,
                "school": spell.school.value,
                "tier": spell.tier.value,
                "required_level": spell.required_level,
                "mana_cost": spell.mana_cost,
                "base_damage": spell.base_damage,
                "description": spell.description,
                "is_ultimate": spell.is_ultimate,
                "can_weave": spell.can_weave
            })

        return jsonify({
            "spells": spells_list,
            "total": len(spells_list)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@magic_bp.route('/state/export', methods=['GET'])
def export_state():
    """
    Export State

    Returns complete state for all schools
    """
    try:
        state = magic_system.export_state()
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

    app.register_blueprint(magic_bp)

    print("=" * 60)
    print("Magic Schools API Server")
    print("=" * 60)
    print()
    print("9 Magieschulen (Skyrim Learning by Doing):")
    print("  1. Feuer")
    print("  2. Eis")
    print("  3. Blitz")
    print("  4. Wasser")
    print("  5. Erde")
    print("  6. Wind")
    print("  7. Licht")
    print("  8. Dunkelheit")
    print("  9. Explosion (NIEMALS kombinierbar!)")
    print()
    print("Endpoints:")
    print("  POST   /api/magic/cast")
    print("  GET    /api/magic/school/<school>")
    print("  GET    /api/magic/overview")
    print("  GET    /api/magic/can-weave")
    print("  GET    /api/magic/spells")
    print("  GET    /api/magic/state/export")
    print()
    print("Server läuft auf: http://localhost:5006")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5006, debug=True)
