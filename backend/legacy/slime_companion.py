#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA WORLD - Slime Companion API Endpoints
============================================
REST API fuer das Slime Companion System

Erstellt: 2026-01-28
"""

from flask import Blueprint, jsonify, request
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from najika_slime_system import (
    get_slime_system, SlimeType, EvolutionStage,
    PASSIVE_BONUSES, REGION_TO_SLIME, SLIME_COLORS
)
from najika_slime_evolution import get_evolution_system
from najika_slime_synthesis import get_synthesis_system, register_synthesis_routes


# =============================================================================
# BLUEPRINT
# =============================================================================

slime_bp = Blueprint('slime', __name__, url_prefix='/api/slime')


# =============================================================================
# HELPER
# =============================================================================

def json_response(data, status=200):
    """Standard JSON Response"""
    response = jsonify(data)
    response.status_code = status
    return response


def error_response(message, status=400):
    """Error Response"""
    return json_response({"success": False, "error": message}, status)


# =============================================================================
# STATUS ENDPOINTS
# =============================================================================

@slime_bp.route('/status', methods=['GET'])
def get_status():
    """
    Gibt Status des aktiven Slimes zurueck

    GET /api/slime/status

    Returns:
        {
            "success": true,
            "slime": { ... } oder null,
            "has_slime": true/false
        }
    """
    system = get_slime_system()
    active = system.get_active_slime()

    return json_response({
        "success": True,
        "slime": active,
        "has_slime": active is not None
    })


@slime_bp.route('/status/<slime_id>', methods=['GET'])
def get_slime_status(slime_id):
    """
    Gibt Status eines bestimmten Slimes zurueck

    GET /api/slime/status/<slime_id>
    """
    system = get_slime_system()
    slime = system.get_slime(slime_id)

    if not slime:
        return error_response("Slime nicht gefunden", 404)

    return json_response({
        "success": True,
        "slime": slime
    })


@slime_bp.route('/all', methods=['GET'])
def get_all_slimes():
    """
    Gibt alle Slimes zurueck

    GET /api/slime/all

    Returns:
        {
            "success": true,
            "slimes": [ ... ],
            "count": 5,
            "active_id": "uuid"
        }
    """
    system = get_slime_system()
    slimes = system.get_all_slimes()

    return json_response({
        "success": True,
        "slimes": slimes,
        "count": len(slimes),
        "active_id": system.active_slime_id
    })


# =============================================================================
# CREATION ENDPOINTS
# =============================================================================

@slime_bp.route('/create', methods=['POST'])
def create_slime():
    """
    Erstellt neues Schleim-Ei

    POST /api/slime/create
    Body: {
        "type": "moos_schleim",
        "name": "Moosy"  (optional)
    }

    Returns:
        {
            "success": true,
            "slime": { ... }
        }
    """
    data = request.get_json() or {}

    slime_type_str = data.get("type", "moos_schleim")
    name = data.get("name")

    # Validiere Typ
    try:
        slime_type = SlimeType(slime_type_str)
    except ValueError:
        return error_response(f"Ungueltiger Slime-Typ: {slime_type_str}")

    system = get_slime_system()
    slime = system.create_egg(slime_type, name)

    # Automatisch als aktiv setzen wenn erster Slime
    if len(system.slimes) == 1:
        system.set_active_slime(slime.id)

    return json_response({
        "success": True,
        "message": f"Neues {slime_type.name} Ei erstellt!",
        "slime": slime.to_dict()
    })


@slime_bp.route('/create/region', methods=['POST'])
def create_from_region():
    """
    Erstellt Slime basierend auf Region

    POST /api/slime/create/region
    Body: {
        "region_id": "samtmoos_tiefwald",
        "name": "Moosy"  (optional)
    }
    """
    data = request.get_json() or {}
    region_id = data.get("region_id")
    name = data.get("name")

    if not region_id:
        return error_response("region_id erforderlich")

    system = get_slime_system()
    slime = system.create_from_region(region_id, name)

    if not slime:
        return error_response(f"Unbekannte Region: {region_id}")

    # Automatisch als aktiv setzen wenn erster Slime
    if len(system.slimes) == 1:
        system.set_active_slime(slime.id)

    return json_response({
        "success": True,
        "message": f"Slime aus {region_id} erstellt!",
        "slime": slime.to_dict()
    })


# =============================================================================
# CARE ENDPOINTS (V-Pet Style)
# =============================================================================

@slime_bp.route('/feed', methods=['POST'])
def feed_slime():
    """
    Fuettert den aktiven Slime

    POST /api/slime/feed
    Body: {
        "slime_id": "uuid"  (optional, sonst aktiver Slime)
    }
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    result = system.feed(slime_id)
    return json_response(result)


@slime_bp.route('/train', methods=['POST'])
def train_slime():
    """
    Trainiert den aktiven Slime

    POST /api/slime/train
    Body: {
        "slime_id": "uuid"  (optional)
    }
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    result = system.train(slime_id)
    return json_response(result)


@slime_bp.route('/play', methods=['POST'])
def play_with_slime():
    """
    Spielt mit dem aktiven Slime

    POST /api/slime/play
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    result = system.play(slime_id)
    return json_response(result)


@slime_bp.route('/sleep', methods=['POST'])
def sleep_slime():
    """
    Slime schlafen legen oder aufwecken

    POST /api/slime/sleep
    Body: {
        "slime_id": "uuid",
        "wake": false  (true zum aufwecken)
    }
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    wake = data.get("wake", False)

    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    result = system.sleep(slime_id, wake)
    return json_response(result)


@slime_bp.route('/heal', methods=['POST'])
def heal_slime():
    """
    Heilt Verletzungen des Slimes

    POST /api/slime/heal
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    result = system.heal(slime_id)
    return json_response(result)


# =============================================================================
# EVOLUTION ENDPOINTS
# =============================================================================

@slime_bp.route('/evolution/check', methods=['GET'])
def check_evolution():
    """
    Prueft ob Evolution moeglich ist

    GET /api/slime/evolution/check?slime_id=uuid
    """
    slime_id = request.args.get("slime_id")
    system = get_slime_system()

    if not slime_id:
        slime_id = system.active_slime_id

    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    evo_system = get_evolution_system()
    result = evo_system.check_evolution_ready(slime_id)

    return json_response({
        "success": True,
        **result
    })


@slime_bp.route('/evolve', methods=['POST'])
def evolve_slime():
    """
    Fuehrt Evolution durch

    POST /api/slime/evolve
    Body: {
        "slime_id": "uuid",
        "path": "perfect"  (optional, sonst bester moeglicher)
    }
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    chosen_path = data.get("path")

    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    evo_system = get_evolution_system()
    result = evo_system.evolve(slime_id, chosen_path)

    return json_response(result)


# =============================================================================
# MANAGEMENT ENDPOINTS
# =============================================================================

@slime_bp.route('/activate', methods=['POST'])
def activate_slime():
    """
    Setzt aktiven Begleiter-Slime

    POST /api/slime/activate
    Body: {
        "slime_id": "uuid"
    }
    """
    data = request.get_json() or {}
    slime_id = data.get("slime_id")

    if not slime_id:
        return error_response("slime_id erforderlich")

    system = get_slime_system()
    if system.set_active_slime(slime_id):
        slime = system.get_slime(slime_id)
        return json_response({
            "success": True,
            "message": f"{slime['name']} ist jetzt dein Begleiter!",
            "slime": slime
        })
    else:
        return error_response("Slime nicht gefunden", 404)


@slime_bp.route('/rename', methods=['POST'])
def rename_slime():
    """
    Benennt Slime um

    POST /api/slime/rename
    Body: {
        "slime_id": "uuid",
        "name": "Neuer Name"
    }
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    new_name = data.get("name")

    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")
    if not new_name:
        return error_response("name erforderlich")

    result = system.rename(slime_id, new_name)
    return json_response(result)


# =============================================================================
# BONUS ENDPOINTS
# =============================================================================

@slime_bp.route('/bonuses', methods=['GET'])
def get_bonuses():
    """
    Gibt aktuelle passive Boni zurueck

    GET /api/slime/bonuses

    Returns:
        {
            "success": true,
            "bonuses": {
                "farming_speed": 0.24,
                "herb_quality": 0.12
            },
            "from_slime": "Moosy"
        }
    """
    system = get_slime_system()
    bonuses = system.get_passive_bonuses()
    active = system.get_active_slime()

    return json_response({
        "success": True,
        "bonuses": bonuses,
        "from_slime": active["name"] if active else None
    })


# =============================================================================
# INFO ENDPOINTS
# =============================================================================

@slime_bp.route('/types', methods=['GET'])
def get_slime_types():
    """
    Gibt alle Slime-Typen zurueck

    GET /api/slime/types
    """
    types = []
    for slime_type in SlimeType:
        bonus = PASSIVE_BONUSES.get(slime_type, {})
        types.append({
            "id": slime_type.value,
            "name": slime_type.name,
            "color": SLIME_COLORS.get(slime_type, "#888888"),
            "passive_bonuses": bonus,
            "description": bonus.get("description", "")
        })

    return json_response({
        "success": True,
        "types": types,
        "count": len(types)
    })


@slime_bp.route('/regions', methods=['GET'])
def get_region_mapping():
    """
    Gibt Region zu Slime-Typ Mapping zurueck

    GET /api/slime/regions
    """
    mapping = {}
    for region, slime_type in REGION_TO_SLIME.items():
        mapping[region] = {
            "slime_type": slime_type.value,
            "slime_name": slime_type.name,
            "color": SLIME_COLORS.get(slime_type, "#888888")
        }

    return json_response({
        "success": True,
        "regions": mapping
    })


# =============================================================================
# BATTLE ENDPOINTS (OPTIONAL!)
# =============================================================================

@slime_bp.route('/battle/record', methods=['POST'])
def record_battle():
    """
    Zeichnet Kampfergebnis auf (NUR wenn Spieler kaempfen WILL!)

    POST /api/slime/battle/record
    Body: {
        "slime_id": "uuid",
        "won": true/false
    }

    WICHTIG: Diese Funktion ist OPTIONAL!
    Monster-Kaempfe sind NICHT ZWINGEND!
    """
    data = request.get_json() or {}
    system = get_slime_system()

    slime_id = data.get("slime_id") or system.active_slime_id
    won = data.get("won", False)

    if not slime_id:
        return error_response("Kein Slime ausgewaehlt")

    result = system.record_battle(slime_id, won)
    return json_response(result)


# =============================================================================
# UPDATE ENDPOINT (Called periodically by server)
# =============================================================================

@slime_bp.route('/update', methods=['POST'])
def update_slimes():
    """
    Periodischer Update fuer alle Slimes
    Sollte alle 5-10 Minuten aufgerufen werden

    POST /api/slime/update

    Returns:
        {
            "success": true,
            "events": [ ... ]
        }
    """
    system = get_slime_system()
    events = system.update()

    return json_response({
        "success": True,
        "events": events,
        "event_count": len(events)
    })


# =============================================================================
# EXPORT
# =============================================================================

def register_slime_routes(app):
    """Registriert Slime Blueprint bei Flask App"""
    # Synthese-Routes hinzufuegen
    register_synthesis_routes(slime_bp)

    app.register_blueprint(slime_bp)
    print("[SlimeAPI] Slime Companion API registriert (inkl. Synthese)")
