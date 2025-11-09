"""
NAJIKA FARMING & FISHING API
============================

REST API for Farming and Fishing systems.

Endpoints:
    FARMING:
    - GET  /api/farm/status         - Get all fields status
    - POST /api/farm/plant          - Plant a crop
    - POST /api/farm/water          - Water a field
    - POST /api/farm/fertilize      - Fertilize a field
    - POST /api/farm/harvest        - Harvest a crop
    - GET  /api/farm/crops          - Get all crop types
    - POST /api/farm/update         - Force update all fields
    - POST /api/farm/season         - Set season
    - POST /api/farm/weather        - Set weather

    FISHING:
    - GET  /api/fish/status         - Get fishing status
    - POST /api/fish/start          - Start fishing
    - GET  /api/fish/spots          - Get all fishing spots
    - GET  /api/fish/types          - Get all fish types
    - POST /api/fish/update         - Force update spots (respawn)
    - POST /api/fish/time           - Set time of day
    - POST /api/fish/weather        - Set weather

    COMBINED:
    - GET  /api/farm_fish/stats     - Combined statistics

Author: Claude Code (CLI)
Date: 2025-11-09 (Tag 2)
"""

from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS

# Import farming and fishing systems
import najika_farming_system as farming
import najika_fishing_system as fishing

# Create Blueprint
farm_fish_api = Blueprint('farm_fish_api', __name__, url_prefix='/api')

# =====================================================
# FARMING ENDPOINTS
# =====================================================

@farm_fish_api.route('/farm/status', methods=['GET'])
def farm_status():
    """Get status of all farm fields"""
    try:
        status = farming.get_farming_status()
        return jsonify({
            "status": "ok",
            "data": status
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/plant', methods=['POST'])
def farm_plant():
    """Plant a crop in a field"""
    try:
        data = request.get_json() or {}
        field_id = data.get('field_id')
        crop_type = data.get('crop_type')
        planter = data.get('planter', 'player')

        if not field_id or not crop_type:
            return jsonify({
                "status": "error",
                "error": "Missing field_id or crop_type"
            }), 400

        result = farming.plant_crop(field_id, crop_type, planter)

        if result["success"]:
            return jsonify({
                "status": "ok",
                "data": result
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": result["error"]
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/water', methods=['POST'])
def farm_water():
    """Water a field"""
    try:
        data = request.get_json() or {}
        field_id = data.get('field_id')

        if not field_id:
            return jsonify({
                "status": "error",
                "error": "Missing field_id"
            }), 400

        result = farming.water_field(field_id)

        if result["success"]:
            return jsonify({
                "status": "ok",
                "data": result
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": result["error"]
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/fertilize', methods=['POST'])
def farm_fertilize():
    """Fertilize a field"""
    try:
        data = request.get_json() or {}
        field_id = data.get('field_id')

        if not field_id:
            return jsonify({
                "status": "error",
                "error": "Missing field_id"
            }), 400

        result = farming.fertilize_field(field_id)

        if result["success"]:
            return jsonify({
                "status": "ok",
                "data": result
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": result["error"]
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/harvest', methods=['POST'])
def farm_harvest():
    """Harvest a crop"""
    try:
        data = request.get_json() or {}
        field_id = data.get('field_id')

        if not field_id:
            return jsonify({
                "status": "error",
                "error": "Missing field_id"
            }), 400

        result = farming.harvest_crop(field_id)

        if result["success"]:
            return jsonify({
                "status": "ok",
                "data": result
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": result["error"]
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/crops', methods=['GET'])
def farm_crops():
    """Get all available crop types"""
    try:
        crops = farming.get_all_crop_types()
        return jsonify({
            "status": "ok",
            "data": crops
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/update', methods=['POST'])
def farm_update():
    """Force update all farm fields"""
    try:
        farming.update_all_fields()
        status = farming.get_farming_status()
        return jsonify({
            "status": "ok",
            "message": "Farm updated",
            "data": status
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/season', methods=['POST'])
def farm_season():
    """Set global season"""
    try:
        data = request.get_json() or {}
        season = data.get('season')

        if not season:
            return jsonify({
                "status": "error",
                "error": "Missing season (spring/summer/fall/winter)"
            }), 400

        success = farming.set_season(season)

        if success:
            return jsonify({
                "status": "ok",
                "message": f"Season set to {season}"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": "Invalid season"
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/farm/weather', methods=['POST'])
def farm_weather():
    """Set global weather"""
    try:
        data = request.get_json() or {}
        weather = data.get('weather')

        if not weather:
            return jsonify({
                "status": "error",
                "error": "Missing weather (clear/rain/snow/storm)"
            }), 400

        success = farming.set_weather(weather)

        if success:
            return jsonify({
                "status": "ok",
                "message": f"Weather set to {weather}"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": "Invalid weather"
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# =====================================================
# FISHING ENDPOINTS
# =====================================================

@farm_fish_api.route('/fish/status', methods=['GET'])
def fish_status():
    """Get fishing status"""
    try:
        status = fishing.get_fishing_status()
        return jsonify({
            "status": "ok",
            "data": status
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/fish/start', methods=['POST'])
def fish_start():
    """Start fishing at a spot"""
    try:
        data = request.get_json() or {}
        spot_id = data.get('spot_id')
        player_skill = data.get('player_skill')
        rod_quality = data.get('rod_quality', 1.0)
        special_rod = data.get('special_rod')

        if not spot_id:
            return jsonify({
                "status": "error",
                "error": "Missing spot_id"
            }), 400

        result = fishing.start_fishing(
            spot_id,
            player_skill=player_skill,
            rod_quality=rod_quality,
            special_rod=special_rod
        )

        if result["success"]:
            return jsonify({
                "status": "ok",
                "data": result
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": result["error"]
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/fish/spots', methods=['GET'])
def fish_spots():
    """Get all fishing spots"""
    try:
        status = fishing.get_fishing_status()
        return jsonify({
            "status": "ok",
            "data": status["spots"]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/fish/types', methods=['GET'])
def fish_types():
    """Get all fish types"""
    try:
        types = fishing.get_all_fish_types()
        return jsonify({
            "status": "ok",
            "data": types
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/fish/update', methods=['POST'])
def fish_update():
    """Force update fishing spots (respawn)"""
    try:
        fishing.update_fishing_spots()
        status = fishing.get_fishing_status()
        return jsonify({
            "status": "ok",
            "message": "Fishing spots updated",
            "data": status
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/fish/time', methods=['POST'])
def fish_time():
    """Set time of day"""
    try:
        data = request.get_json() or {}
        time_of_day = data.get('time_of_day')

        if not time_of_day:
            return jsonify({
                "status": "error",
                "error": "Missing time_of_day (day/night/dawn/dusk)"
            }), 400

        success = fishing.set_time_of_day(time_of_day)

        if success:
            return jsonify({
                "status": "ok",
                "message": f"Time set to {time_of_day}"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": "Invalid time_of_day"
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@farm_fish_api.route('/fish/weather', methods=['POST'])
def fish_weather():
    """Set weather"""
    try:
        data = request.get_json() or {}
        weather = data.get('weather')

        if not weather:
            return jsonify({
                "status": "error",
                "error": "Missing weather (clear/rain/snow/storm)"
            }), 400

        success = fishing.set_weather(weather)

        if success:
            return jsonify({
                "status": "ok",
                "message": f"Weather set to {weather}"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": "Invalid weather"
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# =====================================================
# COMBINED STATS
# =====================================================

@farm_fish_api.route('/farm_fish/stats', methods=['GET'])
def combined_stats():
    """Get combined farming and fishing statistics"""
    try:
        farm_status = farming.get_farming_status()
        fish_status = fishing.get_fishing_status()

        stats = {
            "farming": {
                "total_fields": farm_status["total_fields"],
                "planted_fields": farm_status["planted_fields"],
                "harvestable_fields": farm_status["harvestable_fields"],
                "total_harvests": farm_status["total_harvests"],
                "season": farm_status["season"],
                "weather": farm_status["weather"]
            },
            "fishing": {
                "fishing_skill": fish_status["player_stats"]["fishing_skill"],
                "total_caught": fish_status["player_stats"]["total_caught"],
                "total_attempts": fish_status["player_stats"]["total_attempts"],
                "legendary_count": fish_status["player_stats"]["legendary_count"],
                "biggest_catch": fish_status["player_stats"]["biggest_catch"],
                "available_spots": len(fish_status["spots"]),
                "time_of_day": fish_status["time_of_day"],
                "weather": fish_status["weather"]
            }
        }

        return jsonify({
            "status": "ok",
            "data": stats
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# =====================================================
# STANDALONE SERVER (for testing)
# =====================================================

def create_standalone_app():
    """Create standalone Flask app for testing"""
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(farm_fish_api)

    @app.route('/')
    def index():
        return jsonify({
            "service": "Najika Farming & Fishing API",
            "version": "1.0",
            "endpoints": {
                "farming": [
                    "GET  /api/farm/status",
                    "POST /api/farm/plant",
                    "POST /api/farm/water",
                    "POST /api/farm/fertilize",
                    "POST /api/farm/harvest",
                    "GET  /api/farm/crops",
                    "POST /api/farm/update",
                    "POST /api/farm/season",
                    "POST /api/farm/weather"
                ],
                "fishing": [
                    "GET  /api/fish/status",
                    "POST /api/fish/start",
                    "GET  /api/fish/spots",
                    "GET  /api/fish/types",
                    "POST /api/fish/update",
                    "POST /api/fish/time",
                    "POST /api/fish/weather"
                ],
                "combined": [
                    "GET  /api/farm_fish/stats"
                ]
            }
        })

    return app

if __name__ == "__main__":
    print("="*60)
    print("NAJIKA FARMING & FISHING API")
    print("="*60)
    print("Starting server on http://localhost:5002")
    print("Press Ctrl+C to stop")
    print("="*60)

    app = create_standalone_app()
    app.run(host='0.0.0.0', port=5002, debug=True)
