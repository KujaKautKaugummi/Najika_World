"""
World API - Najika World
=========================

REST API für World System (Biomes, Weather, Day/Night, Cities, Wilderness)

Endpoints:
- GET /api/world/info - Get map info
- GET /api/world/biomes - Get all biomes
- GET /api/world/biome/<biome> - Get specific biome
- GET /api/world/weather/<biome> - Get weather for biome
- POST /api/world/weather/<biome>/update - Force weather update
- GET /api/world/time - Get current time
- POST /api/world/time/set - Set game time
- POST /api/world/time/update - Update time (delta)
- GET /api/world/cities - Get all cities
- GET /api/world/city/<city_id> - Get specific city
- POST /api/world/city/enter - Check if can enter city
- GET /api/world/wilderness/<biome> - Generate/get wilderness
- GET /api/world/state/export - Export complete state

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from flask import Blueprint, request, jsonify

from backend.services.world_system import WorldSystem, Biome

# Create Blueprint
world_bp = Blueprint('world', __name__, url_prefix='/api/world')

# Global System Instance
world_system = WorldSystem()


@world_bp.route('/info', methods=['GET'])
def get_map_info():
    """
    Get Map Info

    Returns:
        {
            size_meters: int,
            size_km2: float,
            goetterfels_height: int,
            wilderness_percentage: float,
            total_biomes: int,
            total_cities: int
        }
    """
    try:
        return jsonify({
            "size_meters": world_system.MAP_SIZE,
            "size_km2": world_system.total_area_km2,
            "goetterfels_height": world_system.GOETTERFELS_HEIGHT,
            "wilderness_percentage": world_system.wilderness_percentage,
            "total_biomes": len(world_system.biomes),
            "total_cities": len(world_system.cities)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/biomes', methods=['GET'])
def get_all_biomes():
    """
    Get All Biomes

    Returns:
        {
            biomes: {
                biome_id: {
                    name: str,
                    description: str,
                    slime_color: str,
                    temperature_range: str,
                    hazardous: bool,
                    vegetation_density: float,
                    possible_weather: [str],
                    resources: [str]
                }
            }
        }
    """
    try:
        biomes_data = {}

        for biome, config in world_system.biomes.items():
            biomes_data[biome.value] = {
                "name": config.name,
                "description": config.description,
                "slime_color": config.slime_color,
                "temperature_range": f"{config.temperature_min}°C - {config.temperature_max}°C",
                "hazardous": config.hazardous,
                "vegetation_density": config.vegetation_density,
                "terrain_roughness": config.terrain_roughness,
                "water_presence": config.water_presence,
                "has_ocean": config.has_ocean,
                "lava_flows": config.lava_flows,
                "possible_weather": [w.value for w in config.possible_weather],
                "resources": config.resources,
                "enemy_types": config.enemy_types
            }

        return jsonify({"biomes": biomes_data, "count": len(biomes_data)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/biome/<biome_id>', methods=['GET'])
def get_biome(biome_id: str):
    """
    Get Specific Biome

    Path: /api/world/biome/samtmoos_tiefwald
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            return jsonify({
                "error": f"Ungültiges Biome: {biome_id}",
                "valid_biomes": [b.value for b in Biome]
            }), 400

        config = world_system.biomes[biome]

        return jsonify({
            "id": biome.value,
            "name": config.name,
            "description": config.description,
            "slime_color": config.slime_color,
            "temperature_range": f"{config.temperature_min}°C - {config.temperature_max}°C",
            "hazardous": config.hazardous,
            "vegetation_density": config.vegetation_density,
            "terrain_roughness": config.terrain_roughness,
            "water_presence": config.water_presence,
            "has_ocean": config.has_ocean,
            "lava_flows": config.lava_flows,
            "possible_weather": [w.value for w in config.possible_weather],
            "resources": config.resources,
            "enemy_types": config.enemy_types,
            "colors": {
                "ground": config.ground_color,
                "ambient": config.ambient_color,
                "fog": config.fog_color
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/weather/<biome_id>', methods=['GET'])
def get_weather(biome_id: str):
    """
    Get Weather for Biome

    Path: /api/world/weather/samtmoos_tiefwald
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            return jsonify({
                "error": f"Ungültiges Biome: {biome_id}",
                "valid_biomes": [b.value for b in Biome]
            }), 400

        weather = world_system.get_weather(biome)

        return jsonify({
            "biome": biome.value,
            "weather": {
                "type": weather.type.value,
                "intensity": weather.intensity,
                "temperature": weather.temperature,
                "wind_speed": weather.wind_speed,
                "visibility": weather.visibility,
                "modifiers": {
                    "movement": weather.movement_modifier,
                    "accuracy": weather.accuracy_modifier,
                    "damage": weather.damage_modifier
                },
                "started_at": weather.started_at.isoformat(),
                "duration_minutes": weather.duration_minutes
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/weather/<biome_id>/update', methods=['POST'])
def update_weather(biome_id: str):
    """
    Force Weather Update for Biome

    Path: /api/world/weather/samtmoos_tiefwald/update
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            return jsonify({
                "error": f"Ungültiges Biome: {biome_id}",
                "valid_biomes": [b.value for b in Biome]
            }), 400

        changed = world_system.update_weather(biome)

        new_weather = world_system.get_weather(biome)

        return jsonify({
            "biome": biome.value,
            "changed": changed,
            "new_weather": {
                "type": new_weather.type.value,
                "intensity": new_weather.intensity,
                "temperature": new_weather.temperature
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/time', methods=['GET'])
def get_time():
    """
    Get Current Game Time

    Returns:
        {
            current_time: str,
            time_of_day: str,
            is_night: bool,
            light_level: float,
            sun_altitude: float,
            sun_azimuth: float,
            moon_phase: float,
            time_scale: float
        }
    """
    try:
        time_info = world_system.get_time_info()
        return jsonify(time_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/time/set', methods=['POST'])
def set_time():
    """
    Set Game Time

    Body:
    {
        "hour": 14,
        "minute": 30
    }
    """
    try:
        data = request.get_json()

        hour = data.get('hour')
        minute = data.get('minute', 0)

        if hour is None:
            return jsonify({"error": "hour erforderlich"}), 400

        if not (0 <= hour < 24):
            return jsonify({"error": "hour muss zwischen 0 und 23 liegen"}), 400

        if not (0 <= minute < 60):
            return jsonify({"error": "minute muss zwischen 0 und 59 liegen"}), 400

        world_system.set_time(hour, minute)

        return jsonify({
            "success": True,
            "time": world_system.get_time_info()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/time/update', methods=['POST'])
def update_time():
    """
    Update Game Time (Delta)

    Body:
    {
        "delta_seconds": 60.0
    }

    Used by game loop to advance time
    """
    try:
        data = request.get_json()

        delta_seconds = data.get('delta_seconds', 0.0)

        if delta_seconds <= 0:
            return jsonify({"error": "delta_seconds muss > 0 sein"}), 400

        world_system.update_time(delta_seconds)

        return jsonify({
            "success": True,
            "time": world_system.get_time_info()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/cities', methods=['GET'])
def get_all_cities():
    """
    Get All Cities

    Returns:
        {
            cities: {
                city_id: {
                    name: str,
                    type: str,
                    biome: str,
                    position: [x, y, z],
                    population: int,
                    wealth_level: int,
                    services: {},
                    guard_level: int,
                    pvp_enabled: bool,
                    min_reputation: int
                }
            }
        }
    """
    try:
        cities = world_system.get_all_cities()
        return jsonify({"cities": cities, "count": len(cities)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/city/<city_id>', methods=['GET'])
def get_city(city_id: str):
    """
    Get Specific City

    Path: /api/world/city/handelsfestung
    """
    try:
        city = world_system.get_city(city_id)

        if not city:
            return jsonify({
                "error": f"Stadt nicht gefunden: {city_id}",
                "available_cities": list(world_system.cities.keys())
            }), 404

        return jsonify({
            "id": city.id,
            "name": city.name,
            "type": city.type.value,
            "biome": city.biome.value,
            "position": city.position,
            "population": city.population,
            "wealth_level": city.wealth_level,
            "services": {
                "smithy": city.has_smithy,
                "alchemy": city.has_alchemy,
                "inn": city.has_inn,
                "temple": city.has_temple,
                "market": city.has_market,
                "crafting_stations": city.has_crafting_stations
            },
            "guard_level": city.guard_level,
            "pvp_enabled": city.pvp_enabled,
            "npc_count": city.npc_count,
            "min_reputation": city.min_reputation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/city/enter', methods=['POST'])
def check_city_entry():
    """
    Check if Player Can Enter City

    Body:
    {
        "city_id": "handelsfestung",
        "player_reputation": 50
    }
    """
    try:
        data = request.get_json()

        city_id = data.get('city_id')
        player_reputation = data.get('player_reputation', 0)

        if not city_id:
            return jsonify({"error": "city_id erforderlich"}), 400

        can_enter, message = world_system.can_enter_city(city_id, player_reputation)

        return jsonify({
            "city_id": city_id,
            "can_enter": can_enter,
            "message": message,
            "player_reputation": player_reputation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/wilderness/<biome_id>', methods=['GET'])
def get_wilderness(biome_id: str):
    """
    Generate/Get Wilderness Area

    Query Params:
        player_id: int (required)

    Path: /api/world/wilderness/samtmoos_tiefwald?player_id=1
    """
    try:
        # Parse biome
        try:
            biome = Biome(biome_id)
        except ValueError:
            return jsonify({
                "error": f"Ungültiges Biome: {biome_id}",
                "valid_biomes": [b.value for b in Biome]
            }), 400

        player_id = request.args.get('player_id', type=int)
        if not player_id:
            return jsonify({"error": "player_id erforderlich"}), 400

        wilderness = world_system.get_wilderness(biome, player_id)

        return jsonify({
            "biome": wilderness.biome.value,
            "seed": wilderness.seed,
            "layout_variant": wilderness.layout_variant,
            "poi_count": wilderness.poi_count,
            "pois": wilderness.pois,
            "active_events": wilderness.active_events,
            "modifiers": wilderness.modifiers,
            "enemy_density": wilderness.enemy_density,
            "resource_density": wilderness.resource_density,
            "created_at": wilderness.created_at.isoformat(),
            "expires_at": wilderness.expires_at.isoformat() if wilderness.expires_at else None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@world_bp.route('/state/export', methods=['GET'])
def export_state():
    """
    Export Complete World State

    Returns:
        JSON with map info, biomes, weather, time, cities
    """
    try:
        state = world_system.export_state()
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

    app.register_blueprint(world_bp)

    print("=" * 60)
    print("World API Server")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  GET    /api/world/info")
    print("  GET    /api/world/biomes")
    print("  GET    /api/world/biome/<biome>")
    print("  GET    /api/world/weather/<biome>")
    print("  POST   /api/world/weather/<biome>/update")
    print("  GET    /api/world/time")
    print("  POST   /api/world/time/set")
    print("  POST   /api/world/time/update")
    print("  GET    /api/world/cities")
    print("  GET    /api/world/city/<city_id>")
    print("  POST   /api/world/city/enter")
    print("  GET    /api/world/wilderness/<biome>")
    print("  GET    /api/world/state/export")
    print()
    print("Server läuft auf: http://localhost:5007")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5007, debug=True)
