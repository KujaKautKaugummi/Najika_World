"""
Seed 8-Regionen World Map + Fast Travel Points
9600x9600 Grid World
"""

from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.world_map import Region, FastTravelPoint, DayNightCycle
from datetime import datetime


def seed_8_regions(db: Session):
    """
    Seed 8 Regions around Götterfels
    """
    regions_data = [
        # REGION 1: Heiße Dünen (Desert - South-East)
        {
            "name": "Heiße Dünen",
            "region_code": "heisse_duenen",
            "position_x": 6000,
            "position_y": 6000,
            "width": 3600,
            "height": 3600,
            "biome_type": "desert",
            "slime_color": "dusty_gold",
            "climate": "hot_dry",
            "terrain_config": {
                "elevation_range": [0, 50],
                "sand_dune_height": 20,
                "rock_formations": True,
                "oasis_count": 3
            },
            "features": ["oasis", "sand_dunes", "ancient_ruins", "mirage_spots"],
            "dangers": ["sandstorms", "scorpions", "desert_bandits", "heat_exhaustion"],
            "resources": {
                "minerals": ["copper", "gold", "gemstones"],
                "plants": ["cactus", "aloe_vera", "desert_flower"],
                "enemies": ["sand_slime", "scorpion", "mummy", "bandit"]
            }
        },

        # REGION 2: Samtmoos-Tiefwald (Forest - North)
        {
            "name": "Samtmoos-Tiefwald",
            "region_code": "samtmoos_tiefwald",
            "position_x": 3000,
            "position_y": 0,
            "width": 3000,
            "height": 2400,
            "biome_type": "forest",
            "slime_color": "moss_green",
            "climate": "humid_warm",
            "terrain_config": {
                "elevation_range": [20, 80],
                "tree_density": 0.8,
                "underbrush_density": 0.6,
                "mushroom_spots": True
            },
            "features": ["ancient_trees", "fairy_circles", "hidden_groves", "moss_caves"],
            "dangers": ["wild_beasts", "poisonous_plants", "forest_spirits", "quicksand"],
            "resources": {
                "minerals": ["iron", "moonstone"],
                "plants": ["healing_herbs", "magic_mushrooms", "rare_flowers"],
                "enemies": ["forest_slime", "wolf", "bear", "dryad"]
            }
        },

        # REGION 3: Kristall-Tundra (Ice - North-West)
        {
            "name": "Kristall-Tundra",
            "region_code": "kristall_tundra",
            "position_x": 0,
            "position_y": 2400,
            "width": 3000,
            "height": 3300,
            "biome_type": "tundra",
            "slime_color": "ice_blue",
            "climate": "frozen_harsh",
            "terrain_config": {
                "elevation_range": [0, 30],
                "ice_crystal_formations": True,
                "snowdrift_height": 10,
                "glacier_count": 2
            },
            "features": ["ice_crystals", "frozen_lakes", "aurora_borealis", "ice_caves"],
            "dangers": ["blizzards", "ice_monsters", "avalanches", "frostbite"],
            "resources": {
                "minerals": ["ice_crystal", "sapphire", "mithril"],
                "plants": ["frost_flower", "ice_moss"],
                "enemies": ["ice_slime", "yeti", "frost_dragon", "ice_golem"]
            }
        },

        # REGION 4: Lava-Schlucht (Volcanic - West)
        {
            "name": "Lava-Schlucht",
            "region_code": "lava_schlucht",
            "position_x": 0,
            "position_y": 5700,
            "width": 3300,
            "height": 3900,
            "biome_type": "volcanic",
            "slime_color": "magma_red",
            "climate": "extreme_heat",
            "terrain_config": {
                "elevation_range": [-50, 100],
                "lava_rivers": True,
                "volcanic_vents": 5,
                "obsidian_formations": True
            },
            "features": ["lava_rivers", "obsidian_spires", "volcanic_vents", "ash_clouds"],
            "dangers": ["lava_flows", "volcanic_eruptions", "fire_demons", "toxic_gas"],
            "resources": {
                "minerals": ["obsidian", "ruby", "sulfur", "volcanic_glass"],
                "plants": ["fire_flower", "lava_moss"],
                "enemies": ["fire_slime", "fire_elemental", "lava_golem", "phoenix"]
            }
        },

        # REGION 5: Himmelshöhen (Sky Islands - North-East)
        {
            "name": "Himmelshöhen",
            "region_code": "himmelshoehen",
            "position_x": 6000,
            "position_y": 0,
            "width": 3600,
            "height": 2400,
            "biome_type": "sky_islands",
            "slime_color": "cloud_white",
            "climate": "windy_cool",
            "terrain_config": {
                "elevation_range": [200, 400],
                "floating_islands": True,
                "cloud_bridges": True,
                "wind_currents": True
            },
            "features": ["floating_islands", "cloud_bridges", "wind_temples", "sky_gardens"],
            "dangers": ["strong_winds", "flying_monsters", "lightning_storms", "falling"],
            "resources": {
                "minerals": ["sky_crystal", "wind_stone", "silver"],
                "plants": ["sky_flower", "cloud_berry"],
                "enemies": ["cloud_slime", "griffin", "wind_elemental", "sky_dragon"]
            }
        },

        # REGION 6: Donner-Steppe (Thunder Plains - East)
        {
            "name": "Donner-Steppe",
            "region_code": "donner_steppe",
            "position_x": 6000,
            "position_y": 2400,
            "width": 3600,
            "height": 3600,
            "biome_type": "plains",
            "slime_color": "electric_yellow",
            "climate": "stormy_temperate",
            "terrain_config": {
                "elevation_range": [10, 40],
                "grass_density": 0.9,
                "lightning_towers": True,
                "storm_frequency": 0.7
            },
            "features": ["lightning_towers", "thunder_stones", "storm_vortexes", "electric_fields"],
            "dangers": ["lightning_storms", "electric_monsters", "tornadoes", "static_discharge"],
            "resources": {
                "minerals": ["thunder_stone", "electrum", "topaz"],
                "plants": ["storm_grass", "lightning_flower"],
                "enemies": ["thunder_slime", "storm_elemental", "lightning_beast", "raiju"]
            }
        },

        # REGION 7: Schatten-Moor (Swamp - South-West)
        {
            "name": "Schatten-Moor",
            "region_code": "schatten_moor",
            "position_x": 3300,
            "position_y": 6300,
            "width": 2700,
            "height": 3300,
            "biome_type": "swamp",
            "slime_color": "shadow_purple",
            "climate": "damp_foggy",
            "terrain_config": {
                "elevation_range": [-10, 20],
                "water_coverage": 0.4,
                "fog_density": 0.8,
                "dead_trees": True
            },
            "features": ["murky_waters", "dead_trees", "will-o'-wisps", "shadow_pools"],
            "dangers": ["poisonous_fog", "swamp_monsters", "quicksand", "diseases"],
            "resources": {
                "minerals": ["shadow_crystal", "onyx", "dark_pearl"],
                "plants": ["shadow_mushroom", "swamp_root", "ghost_flower"],
                "enemies": ["shadow_slime", "swamp_horror", "wraith", "bog_monster"]
            }
        },

        # REGION 8: Korallen-Küste (Coastal - South)
        {
            "name": "Korallen-Küste",
            "region_code": "korallen_kueste",
            "position_x": 3300,
            "position_y": 9600,
            "width": 2700,
            "height": 0,  # Edge of map
            "biome_type": "coastal",
            "slime_color": "aqua_blue",
            "climate": "tropical_humid",
            "terrain_config": {
                "elevation_range": [0, 50],
                "beach_width": 100,
                "coral_reefs": True,
                "tide_system": True
            },
            "features": ["coral_reefs", "tropical_beaches", "sea_caves", "shipwrecks"],
            "dangers": ["sea_monsters", "pirates", "tsunamis", "sharks"],
            "resources": {
                "minerals": ["coral", "pearl", "sea_crystal"],
                "plants": ["kelp", "sea_flower", "tropical_fruit"],
                "enemies": ["water_slime", "shark", "kraken", "pirate"]
            }
        }
    ]

    created_regions = []
    for region_data in regions_data:
        # Check if exists
        existing = db.query(Region).filter(
            Region.region_code == region_data["region_code"]
        ).first()

        if not existing:
            region = Region(**region_data)
            db.add(region)
            created_regions.append(region)

    db.commit()
    print(f"✅ Seeded {len(created_regions)} regions (8 total)!")
    return created_regions


def seed_fast_travel_points(db: Session):
    """
    Seed Fast Travel Points for all regions
    """
    regions = db.query(Region).all()

    travel_points_data = {
        "heisse_duenen": [
            {
                "name": "Oasis Shrine",
                "point_type": "shrine",
                "position_x": 7500.0,
                "position_y": 7500.0,
                "position_z": 0.0,
                "is_locked": False,
                "unlock_requirement": "None",
                "icon": "🏜️",
                "description": "A peaceful oasis in the desert with a healing shrine."
            },
            {
                "name": "Ancient Pyramid",
                "point_type": "landmark",
                "position_x": 8000.0,
                "position_y": 8000.0,
                "position_z": 50.0,
                "is_locked": True,
                "unlock_requirement": "Defeat Desert Guardian",
                "icon": "🔺",
                "description": "An ancient pyramid filled with treasures and traps."
            }
        ],
        "samtmoos_tiefwald": [
            {
                "name": "Forest Shrine",
                "point_type": "shrine",
                "position_x": 4500.0,
                "position_y": 1200.0,
                "position_z": 30.0,
                "is_locked": False,
                "unlock_requirement": "None",
                "icon": "🌲",
                "description": "A moss-covered shrine deep in the forest."
            }
        ],
        "kristall_tundra": [
            {
                "name": "Ice Crystal Waypoint",
                "point_type": "waypoint",
                "position_x": 1500.0,
                "position_y": 4000.0,
                "position_z": 10.0,
                "is_locked": False,
                "unlock_requirement": "None",
                "icon": "❄️",
                "description": "A waypoint marked by glowing ice crystals."
            }
        ],
        "lava_schlucht": [
            {
                "name": "Obsidian Forge",
                "point_type": "town",
                "position_x": 1650.0,
                "position_y": 7500.0,
                "position_z": 20.0,
                "is_locked": False,
                "unlock_requirement": "None",
                "icon": "🔥",
                "description": "A blacksmith town built on obsidian platforms."
            }
        ],
        "himmelshoehen": [
            {
                "name": "Sky Temple",
                "point_type": "shrine",
                "position_x": 7800.0,
                "position_y": 1200.0,
                "position_z": 300.0,
                "is_locked": True,
                "unlock_requirement": "Complete Wind Trial",
                "icon": "☁️",
                "description": "A temple floating high in the clouds."
            }
        ],
        "donner_steppe": [
            {
                "name": "Lightning Tower",
                "point_type": "landmark",
                "position_x": 7800.0,
                "position_y": 4500.0,
                "position_z": 25.0,
                "is_locked": False,
                "unlock_requirement": "None",
                "icon": "⚡",
                "description": "A massive tower that attracts lightning strikes."
            }
        ],
        "schatten_moor": [
            {
                "name": "Shadow Pool",
                "point_type": "waypoint",
                "position_x": 4650.0,
                "position_y": 7950.0,
                "position_z": 0.0,
                "is_locked": False,
                "unlock_requirement": "None",
                "icon": "🌑",
                "description": "A mysterious pool that reflects the stars."
            }
        ],
        "korallen_kueste": [
            {
                "name": "Harbor Town",
                "point_type": "town",
                "position_x": 4650.0,
                "position_y": 9300.0,
                "position_z": 5.0,
                "is_locked": False,
                "unlock_requirement": "None",
                "icon": "⚓",
                "description": "A bustling harbor town with ships and traders."
            }
        ]
    }

    created_points = []
    for region in regions:
        points_for_region = travel_points_data.get(region.region_code, [])

        for point_data in points_for_region:
            # Check if exists
            existing = db.query(FastTravelPoint).filter(
                FastTravelPoint.region_id == region.id,
                FastTravelPoint.name == point_data["name"]
            ).first()

            if not existing:
                point = FastTravelPoint(
                    region_id=region.id,
                    **point_data
                )
                db.add(point)
                created_points.append(point)

    db.commit()
    print(f"✅ Seeded {len(created_points)} fast travel points!")


def seed_day_night_cycle(db: Session):
    """
    Initialize global day/night cycle
    """
    existing = db.query(DayNightCycle).first()

    if not existing:
        cycle = DayNightCycle(
            current_hour=12.0,  # Start at noon
            current_day=1,
            time_scale=60.0,  # 1 real minute = 1 game hour
            sun_angle=180.0,
            moon_phase=0.5,
            ambient_light=1.0,
            sun_intensity=1.0,
            updated_at=datetime.utcnow()
        )
        db.add(cycle)
        db.commit()
        print("✅ Seeded day/night cycle!")


def main():
    """Run all world map seeds"""
    db = SessionLocal()

    try:
        print("\n🌍 Seeding 8-Regionen World Map...")
        print("=" * 70)

        seed_8_regions(db)
        seed_fast_travel_points(db)
        seed_day_night_cycle(db)

        print("=" * 70)
        print("✅ World Map Seeding Complete!")
        print("\n📊 Summary:")
        print(f"   - 8 Regions (9600x9600 Grid)")
        print(f"   - {db.query(FastTravelPoint).count()} Fast Travel Points")
        print(f"   - Day/Night Cycle Initialized")
        print("=" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    main()
