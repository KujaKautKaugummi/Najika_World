"""
World System - Najika World
============================

Manages Biomes, Weather, Day/Night Cycle, Cities, and Procedural Wilderness.

Map Structure:
- 6.76 km² (Battle Royale size)
- Götterfels: Center mountain (500m high)
- 8 Regions: Around Götterfels
- Cities: FIXED positions (E key to enter)
- Wilderness: PROCEDURAL (changes each visit)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple
import random
import math


# ============================================================================
# ENUMS
# ============================================================================

class Biome(Enum):
    """8 Main Regions + Center Mountain"""
    # Center
    GOETTERFELS = "goetterfels"

    # 8 Regions (um Götterfels herum)
    SAMTMOOS_TIEFWALD = "samtmoos_tiefwald"        # Wald (Forest)
    REICH_DER_DREI = "reich_der_drei"              # Eisregion (Ice)
    WINDPFAD_HOCHEBENE = "windpfad_hochebene"      # Hochebene (Highland)
    LICHTUNG_DES_ANFANGS = "lichtung_des_anfangs"  # Startgebiet (Meadow)
    KRISTALLSUMPF = "kristallsumpf"                # Sumpf (Swamp)
    SCHATTENBERGE = "schattenberge"                # Berge (Mountains)
    FEUERLAND = "feuerland"                        # Vulkan (Volcano)
    STURMKÜSTE = "sturmkueste"                     # Küste (Coast)


class WeatherType(Enum):
    """Weather Types"""
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    HEAVY_RAIN = "heavy_rain"
    SNOW = "snow"
    BLIZZARD = "blizzard"
    FOG = "fog"
    SANDSTORM = "sandstorm"
    THUNDERSTORM = "thunderstorm"
    ASH_RAIN = "ash_rain"  # Vulkan


class TimeOfDay(Enum):
    """Time of Day"""
    DAWN = "dawn"          # 05:00 - 06:59
    MORNING = "morning"    # 07:00 - 11:59
    NOON = "noon"          # 12:00 - 13:59
    AFTERNOON = "afternoon"  # 14:00 - 17:59
    DUSK = "dusk"          # 18:00 - 19:59
    NIGHT = "night"        # 20:00 - 04:59


class CityType(Enum):
    """City Types"""
    TRADING_HUB = "trading_hub"      # Handelszentrum
    CRAFTING_TOWN = "crafting_town"  # Handwerker-Stadt
    MILITARY_FORT = "military_fort"  # Militärfestung
    TEMPLE_CITY = "temple_city"      # Tempel-Stadt
    FISHING_VILLAGE = "fishing_village"  # Fischerdorf
    MINING_OUTPOST = "mining_outpost"    # Bergbau-Außenposten
    MAGICAL_ACADEMY = "magical_academy"  # Magieakademie
    FARMLAND = "farmland"            # Bauernland


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class BiomeConfig:
    """Biome Configuration"""
    id: Biome
    name: str
    description: str

    # Colors (Hex)
    ground_color: str
    ambient_color: str
    fog_color: str

    # Environment
    vegetation_density: float  # 0.0 - 1.0
    terrain_roughness: float   # 0.0 - 1.0
    water_presence: bool
    has_ocean: bool
    lava_flows: bool

    # Weather (possible weather types)
    possible_weather: List[WeatherType]

    # Risks
    hazardous: bool
    temperature_min: int  # °C
    temperature_max: int  # °C

    # Enemies (spawn types)
    enemy_types: List[str] = field(default_factory=list)

    # Resources
    resources: List[str] = field(default_factory=list)

    # Slime Color (for metamorphosis)
    slime_color: Optional[str] = None


@dataclass
class Weather:
    """Current Weather State"""
    type: WeatherType
    intensity: float  # 0.0 - 1.0
    temperature: int  # °C
    wind_speed: float  # m/s
    visibility: float  # 0.0 - 1.0 (1.0 = clear, 0.0 = zero visibility)

    # Gameplay Effects
    movement_modifier: float = 1.0   # Speed multiplier
    accuracy_modifier: float = 1.0   # Ranged attack accuracy
    damage_modifier: float = 1.0     # Elemental damage modifier

    # Duration
    started_at: datetime = field(default_factory=datetime.now)
    duration_minutes: int = 30


@dataclass
class DayNightCycle:
    """Day/Night Cycle"""
    current_time: datetime
    time_scale: float = 1.0  # 1.0 = real-time, 24.0 = 1h IRL = 1 day in-game

    # Sun position (for lighting)
    sun_altitude: float = 45.0  # degrees
    sun_azimuth: float = 180.0  # degrees

    # Moon phase (0.0 - 1.0, where 0.0 = new moon, 0.5 = full moon)
    moon_phase: float = 0.5

    def get_time_of_day(self) -> TimeOfDay:
        """Get current time of day"""
        hour = self.current_time.hour

        if 5 <= hour < 7:
            return TimeOfDay.DAWN
        elif 7 <= hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= hour < 14:
            return TimeOfDay.NOON
        elif 14 <= hour < 18:
            return TimeOfDay.AFTERNOON
        elif 18 <= hour < 20:
            return TimeOfDay.DUSK
        else:
            return TimeOfDay.NIGHT

    def is_night(self) -> bool:
        """Check if it's night"""
        return self.get_time_of_day() == TimeOfDay.NIGHT

    def get_light_level(self) -> float:
        """Get light level (0.0 - 1.0)"""
        time_of_day = self.get_time_of_day()

        light_levels = {
            TimeOfDay.DAWN: 0.4,
            TimeOfDay.MORNING: 0.9,
            TimeOfDay.NOON: 1.0,
            TimeOfDay.AFTERNOON: 0.9,
            TimeOfDay.DUSK: 0.4,
            TimeOfDay.NIGHT: 0.1
        }

        base_light = light_levels[time_of_day]

        # Moon phase affects night light
        if self.is_night():
            moon_bonus = self.moon_phase * 0.2
            return min(1.0, base_light + moon_bonus)

        return base_light


@dataclass
class City:
    """City/Settlement"""
    id: str
    name: str
    type: CityType
    biome: Biome

    # Position (FIXED!)
    position: Tuple[float, float, float]  # (x, y, z)

    # Population & Economy
    population: int
    wealth_level: int  # 1-10

    # Services
    has_smithy: bool = False
    has_alchemy: bool = False
    has_inn: bool = False
    has_temple: bool = False
    has_market: bool = False
    has_crafting_stations: bool = False

    # Security
    guard_level: int = 5  # 1-10 (affects crime/safety)
    pvp_enabled: bool = False  # Cities are usually safe zones

    # NPC Count
    npc_count: int = 20

    # Reputation requirement (-100 to 100)
    min_reputation: int = 0  # Required reputation to enter


@dataclass
class WildernessArea:
    """Procedurally Generated Wilderness"""
    biome: Biome
    seed: int  # Procedural seed (changes each visit)

    # Layout
    layout_variant: str  # "canyon", "oasis", "dense_forest", etc.

    # POIs (Points of Interest)
    poi_count: int = 3
    pois: List[Dict] = field(default_factory=list)

    # Events (Oregon Trail style)
    active_events: List[str] = field(default_factory=list)

    # Modifiers
    modifiers: Dict[str, float] = field(default_factory=dict)

    # Spawns
    enemy_density: float = 1.0
    resource_density: float = 1.0

    # Created at
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None  # When this variant expires


# ============================================================================
# WORLD SYSTEM
# ============================================================================

class WorldSystem:
    """
    World System - Manages entire game world

    Features:
    - 8 Regions + Götterfels (9 total)
    - Dynamic Weather per Region
    - Day/Night Cycle (accelerated time)
    - Fixed Cities (E key to enter)
    - Procedural Wilderness (changes each visit)
    """

    # Map Size
    MAP_SIZE = 6760  # meters (6.76 km²)
    GOETTERFELS_HEIGHT = 500  # meters

    # Time
    DEFAULT_TIME_SCALE = 24.0  # 1h IRL = 1 day in-game

    # Weather
    WEATHER_CHANGE_INTERVAL = 30  # minutes

    def __init__(self):
        # Biomes
        self.biomes: Dict[Biome, BiomeConfig] = {}
        self._initialize_biomes()

        # Weather (per biome)
        self.current_weather: Dict[Biome, Weather] = {}
        self._initialize_weather()

        # Day/Night Cycle
        self.day_night = DayNightCycle(
            current_time=datetime.now().replace(hour=12, minute=0, second=0),
            time_scale=self.DEFAULT_TIME_SCALE
        )

        # Cities (FIXED positions)
        self.cities: Dict[str, City] = {}
        self._initialize_cities()

        # Wilderness (PROCEDURAL)
        self.wilderness_cache: Dict[str, WildernessArea] = {}

        # Stats
        self.total_area_km2 = 6.76
        self.wilderness_percentage = 0.85  # 85% wilderness, 15% cities/roads

    # ========================================================================
    # INITIALIZATION
    # ========================================================================

    def _initialize_biomes(self):
        """Initialize all biomes"""

        # Götterfels (Center Mountain)
        self.biomes[Biome.GOETTERFELS] = BiomeConfig(
            id=Biome.GOETTERFELS,
            name="Götterfels",
            description="Massive center mountain (500m high)",
            ground_color="#808080",
            ambient_color="#AAAAAA",
            fog_color="#C0C0C0",
            vegetation_density=0.3,
            terrain_roughness=0.95,
            water_presence=False,
            has_ocean=False,
            lava_flows=False,
            possible_weather=[
                WeatherType.CLEAR, WeatherType.CLOUDY,
                WeatherType.FOG, WeatherType.SNOW
            ],
            hazardous=True,
            temperature_min=-10,
            temperature_max=15,
            enemy_types=["mountain_goat", "snow_leopard", "harpy"],
            resources=["iron_ore", "silver_ore", "mountain_herbs"],
            slime_color=None  # No slime color (not one of the 8)
        )

        # 1. Samtmoos-Tiefwald (Forest)
        self.biomes[Biome.SAMTMOOS_TIEFWALD] = BiomeConfig(
            id=Biome.SAMTMOOS_TIEFWALD,
            name="Samtmoos-Tiefwald",
            description="Dense mossy forest",
            ground_color="#2D5016",
            ambient_color="#3A6B1F",
            fog_color="#4A7B2F",
            vegetation_density=0.95,
            terrain_roughness=0.7,
            water_presence=True,
            has_ocean=False,
            lava_flows=False,
            possible_weather=[
                WeatherType.CLEAR, WeatherType.CLOUDY,
                WeatherType.RAIN, WeatherType.FOG
            ],
            hazardous=False,
            temperature_min=10,
            temperature_max=25,
            enemy_types=["wolf", "bear", "forest_spider"],
            resources=["wood", "moss", "mushrooms", "herbs"],
            slime_color="moss_green"
        )

        # 2. Reich der Drei (Ice)
        self.biomes[Biome.REICH_DER_DREI] = BiomeConfig(
            id=Biome.REICH_DER_DREI,
            name="Reich der Drei",
            description="Frozen ice region",
            ground_color="#E0F0FF",
            ambient_color="#C0D8E8",
            fog_color="#A0C0D8",
            vegetation_density=0.1,
            terrain_roughness=0.3,
            water_presence=True,
            has_ocean=False,
            lava_flows=False,
            possible_weather=[
                WeatherType.CLEAR, WeatherType.SNOW,
                WeatherType.BLIZZARD, WeatherType.FOG
            ],
            hazardous=True,
            temperature_min=-30,
            temperature_max=-5,
            enemy_types=["ice_wolf", "frost_giant", "yeti"],
            resources=["ice_crystal", "frozen_herb", "whale_oil"],
            slime_color="crystal_white"
        )

        # 3. Windpfad-Hochebene (Highland)
        self.biomes[Biome.WINDPFAD_HOCHEBENE] = BiomeConfig(
            id=Biome.WINDPFAD_HOCHEBENE,
            name="Windpfad-Hochebene",
            description="Windy highland plains",
            ground_color="#8B7355",
            ambient_color="#A08060",
            fog_color="#B09070",
            vegetation_density=0.4,
            terrain_roughness=0.5,
            water_presence=False,
            has_ocean=False,
            lava_flows=False,
            possible_weather=[
                WeatherType.CLEAR, WeatherType.CLOUDY,
                WeatherType.THUNDERSTORM, WeatherType.FOG
            ],
            hazardous=False,
            temperature_min=5,
            temperature_max=20,
            enemy_types=["lightning_hawk", "plains_runner", "totem_guardian"],
            resources=["highland_grass", "totem_wood", "amber"],
            slime_color="amethyst"
        )

        # 4. Lichtung des Anfangs (Starting Area - Meadow)
        self.biomes[Biome.LICHTUNG_DES_ANFANGS] = BiomeConfig(
            id=Biome.LICHTUNG_DES_ANFANGS,
            name="Lichtung des Anfangs",
            description="Peaceful starting meadow",
            ground_color="#7CBD56",
            ambient_color="#8BCD66",
            fog_color="#9BDD76",
            vegetation_density=0.6,
            terrain_roughness=0.3,
            water_presence=True,
            has_ocean=False,
            lava_flows=False,
            possible_weather=[
                WeatherType.CLEAR, WeatherType.CLOUDY,
                WeatherType.RAIN
            ],
            hazardous=False,
            temperature_min=15,
            temperature_max=25,
            enemy_types=["rabbit", "deer", "slime"],  # Weak enemies
            resources=["flowers", "grass", "berries"],
            slime_color=None  # Starting area, not part of 8 colors
        )

        # 5. Kristallsumpf (Swamp)
        self.biomes[Biome.KRISTALLSUMPF] = BiomeConfig(
            id=Biome.KRISTALLSUMPF,
            name="Kristallsumpf",
            description="Crystal-infused swamp",
            ground_color="#3A5F4F",
            ambient_color="#2A4F3F",
            fog_color="#1A3F2F",
            vegetation_density=0.7,
            terrain_roughness=0.85,
            water_presence=True,
            has_ocean=False,
            lava_flows=False,
            possible_weather=[
                WeatherType.FOG, WeatherType.RAIN,
                WeatherType.HEAVY_RAIN
            ],
            hazardous=True,
            temperature_min=15,
            temperature_max=30,
            enemy_types=["swamp_witch", "bog_horror", "poison_frog"],
            resources=["swamp_herb", "miasma_essence", "crystal_shard"],
            slime_color="onyx"
        )

        # 6. Schattenberge (Mountains)
        self.biomes[Biome.SCHATTENBERGE] = BiomeConfig(
            id=Biome.SCHATTENBERGE,
            name="Schattenberge",
            description="Dark shadow mountains",
            ground_color="#4A4A4A",
            ambient_color="#3A3A3A",
            fog_color="#2A2A2A",
            vegetation_density=0.2,
            terrain_roughness=0.9,
            water_presence=False,
            has_ocean=False,
            lava_flows=False,
            possible_weather=[
                WeatherType.CLOUDY, WeatherType.FOG,
                WeatherType.THUNDERSTORM
            ],
            hazardous=True,
            temperature_min=0,
            temperature_max=15,
            enemy_types=["shadow_beast", "mountain_troll", "dark_elemental"],
            resources=["shadow_ore", "obsidian", "dark_crystal"],
            slime_color="obsidian"
        )

        # 7. Feuerland (Volcano)
        self.biomes[Biome.FEUERLAND] = BiomeConfig(
            id=Biome.FEUERLAND,
            name="Feuerland",
            description="Volcanic fire region",
            ground_color="#8B0000",
            ambient_color="#A01010",
            fog_color="#B02020",
            vegetation_density=0.1,
            terrain_roughness=0.95,
            water_presence=False,
            has_ocean=False,
            lava_flows=True,
            possible_weather=[
                WeatherType.CLEAR, WeatherType.ASH_RAIN,
                WeatherType.FOG
            ],
            hazardous=True,
            temperature_min=30,
            temperature_max=60,
            enemy_types=["fire_elemental", "lava_golem", "salamander"],
            resources=["lava_stone", "fire_crystal", "volcanic_ash"],
            slime_color="rubin"
        )

        # 8. Sturmküste (Coast)
        self.biomes[Biome.STURMKÜSTE] = BiomeConfig(
            id=Biome.STURMKÜSTE,
            name="Sturmküste",
            description="Stormy coastal cliffs",
            ground_color="#5F9EA0",
            ambient_color="#4F8E90",
            fog_color="#3F7E80",
            vegetation_density=0.3,
            terrain_roughness=0.7,
            water_presence=True,
            has_ocean=True,
            lava_flows=False,
            possible_weather=[
                WeatherType.CLEAR, WeatherType.RAIN,
                WeatherType.THUNDERSTORM, WeatherType.FOG
            ],
            hazardous=False,
            temperature_min=10,
            temperature_max=25,
            enemy_types=["sea_serpent", "siren", "crab_giant"],
            resources=["fish", "pearl", "seaweed", "coral"],
            slime_color="azur"
        )

    def _initialize_weather(self):
        """Initialize weather for all biomes"""
        for biome in Biome:
            self.current_weather[biome] = self._generate_weather(biome)

    def _initialize_cities(self):
        """Initialize fixed cities"""

        # 1. Handelsfestung (Trading Hub) - Lichtung des Anfangs
        self.cities["handelsfestung"] = City(
            id="handelsfestung",
            name="Handelsfestung",
            type=CityType.TRADING_HUB,
            biome=Biome.LICHTUNG_DES_ANFANGS,
            position=(100.0, 0.0, 100.0),
            population=5000,
            wealth_level=8,
            has_smithy=True,
            has_alchemy=True,
            has_inn=True,
            has_temple=False,
            has_market=True,
            has_crafting_stations=True,
            guard_level=7,
            pvp_enabled=False,
            npc_count=50,
            min_reputation=0
        )

        # 2. Dampf-Hain (Crafting Town) - Samtmoos-Tiefwald
        self.cities["dampf_hain"] = City(
            id="dampf_hain",
            name="Dampf-Hain",
            type=CityType.CRAFTING_TOWN,
            biome=Biome.SAMTMOOS_TIEFWALD,
            position=(-500.0, 0.0, 300.0),
            population=2000,
            wealth_level=6,
            has_smithy=True,
            has_alchemy=True,
            has_inn=True,
            has_temple=False,
            has_market=False,
            has_crafting_stations=True,
            guard_level=5,
            pvp_enabled=False,
            npc_count=30,
            min_reputation=0
        )

        # 3. Salzige Bucht (Fishing Village) - Sturmküste
        self.cities["salzige_bucht"] = City(
            id="salzige_bucht",
            name="Salzige Bucht",
            type=CityType.FISHING_VILLAGE,
            biome=Biome.STURMKÜSTE,
            position=(800.0, 0.0, -600.0),
            population=1500,
            wealth_level=5,
            has_smithy=False,
            has_alchemy=False,
            has_inn=True,
            has_temple=True,
            has_market=True,
            has_crafting_stations=False,
            guard_level=4,
            pvp_enabled=False,
            npc_count=25,
            min_reputation=0
        )

        # 4. Runenheim (Magical Academy) - Windpfad-Hochebene
        self.cities["runenheim"] = City(
            id="runenheim",
            name="Runenheim",
            type=CityType.MAGICAL_ACADEMY,
            biome=Biome.WINDPFAD_HOCHEBENE,
            position=(400.0, 50.0, 700.0),
            population=3000,
            wealth_level=9,
            has_smithy=False,
            has_alchemy=True,
            has_inn=True,
            has_temple=True,
            has_market=False,
            has_crafting_stations=True,
            guard_level=8,
            pvp_enabled=False,
            npc_count=40,
            min_reputation=10  # Requires positive reputation
        )

        # 5. Funken-Siedlung (Mining Outpost) - Schattenberge
        self.cities["funken_siedlung"] = City(
            id="funken_siedlung",
            name="Funken-Siedlung",
            type=CityType.MINING_OUTPOST,
            biome=Biome.SCHATTENBERGE,
            position=(-700.0, 100.0, -500.0),
            population=800,
            wealth_level=7,
            has_smithy=True,
            has_alchemy=False,
            has_inn=True,
            has_temple=False,
            has_market=False,
            has_crafting_stations=True,
            guard_level=6,
            pvp_enabled=False,
            npc_count=15,
            min_reputation=-10  # Accepts outlaws
        )

    # ========================================================================
    # WEATHER SYSTEM
    # ========================================================================

    def _generate_weather(self, biome: Biome) -> Weather:
        """Generate random weather for a biome"""
        biome_config = self.biomes[biome]

        # Choose random weather type from possible weather
        weather_type = random.choice(biome_config.possible_weather)

        # Intensity
        intensity = random.uniform(0.3, 1.0)

        # Temperature (within biome range)
        temperature = random.randint(
            biome_config.temperature_min,
            biome_config.temperature_max
        )

        # Wind speed
        wind_speed = self._get_wind_speed(weather_type, intensity)

        # Visibility
        visibility = self._get_visibility(weather_type, intensity)

        # Gameplay modifiers
        movement_mod = self._get_movement_modifier(weather_type, intensity)
        accuracy_mod = self._get_accuracy_modifier(weather_type, intensity)
        damage_mod = self._get_damage_modifier(weather_type, biome)

        # Duration
        duration = random.randint(15, 60)  # 15-60 minutes

        return Weather(
            type=weather_type,
            intensity=intensity,
            temperature=temperature,
            wind_speed=wind_speed,
            visibility=visibility,
            movement_modifier=movement_mod,
            accuracy_modifier=accuracy_mod,
            damage_modifier=damage_mod,
            started_at=datetime.now(),
            duration_minutes=duration
        )

    def _get_wind_speed(self, weather: WeatherType, intensity: float) -> float:
        """Calculate wind speed"""
        base_speeds = {
            WeatherType.CLEAR: 2.0,
            WeatherType.CLOUDY: 5.0,
            WeatherType.RAIN: 10.0,
            WeatherType.HEAVY_RAIN: 15.0,
            WeatherType.SNOW: 8.0,
            WeatherType.BLIZZARD: 25.0,
            WeatherType.FOG: 1.0,
            WeatherType.SANDSTORM: 30.0,
            WeatherType.THUNDERSTORM: 20.0,
            WeatherType.ASH_RAIN: 12.0
        }

        return base_speeds.get(weather, 5.0) * intensity

    def _get_visibility(self, weather: WeatherType, intensity: float) -> float:
        """Calculate visibility (0.0 - 1.0)"""
        base_visibility = {
            WeatherType.CLEAR: 1.0,
            WeatherType.CLOUDY: 0.9,
            WeatherType.RAIN: 0.7,
            WeatherType.HEAVY_RAIN: 0.5,
            WeatherType.SNOW: 0.6,
            WeatherType.BLIZZARD: 0.2,
            WeatherType.FOG: 0.3,
            WeatherType.SANDSTORM: 0.1,
            WeatherType.THUNDERSTORM: 0.6,
            WeatherType.ASH_RAIN: 0.4
        }

        base = base_visibility.get(weather, 0.8)
        return max(0.1, base - (intensity * 0.3))

    def _get_movement_modifier(self, weather: WeatherType, intensity: float) -> float:
        """Calculate movement speed modifier"""
        penalties = {
            WeatherType.HEAVY_RAIN: -0.2,
            WeatherType.BLIZZARD: -0.4,
            WeatherType.SANDSTORM: -0.3,
            WeatherType.FOG: -0.1
        }

        penalty = penalties.get(weather, 0.0) * intensity
        return 1.0 + penalty

    def _get_accuracy_modifier(self, weather: WeatherType, intensity: float) -> float:
        """Calculate ranged attack accuracy modifier"""
        penalties = {
            WeatherType.RAIN: -0.1,
            WeatherType.HEAVY_RAIN: -0.25,
            WeatherType.BLIZZARD: -0.4,
            WeatherType.SANDSTORM: -0.5,
            WeatherType.FOG: -0.3,
            WeatherType.THUNDERSTORM: -0.2
        }

        penalty = penalties.get(weather, 0.0) * intensity
        return 1.0 + penalty

    def _get_damage_modifier(self, weather: WeatherType, biome: Biome) -> float:
        """Calculate elemental damage modifier"""
        # Fire magic weaker in rain/snow
        # Ice magic stronger in snow/blizzard
        # Lightning magic stronger in thunderstorm
        # etc.
        return 1.0  # TODO: Implement elemental interactions

    def update_weather(self, biome: Biome):
        """Update weather for a biome (called periodically)"""
        current = self.current_weather[biome]

        # Check if weather expired
        elapsed = datetime.now() - current.started_at
        if elapsed.total_seconds() / 60 >= current.duration_minutes:
            # Generate new weather
            self.current_weather[biome] = self._generate_weather(biome)
            return True

        return False

    def get_weather(self, biome: Biome) -> Weather:
        """Get current weather for a biome"""
        return self.current_weather[biome]

    # ========================================================================
    # DAY/NIGHT CYCLE
    # ========================================================================

    def update_time(self, delta_seconds: float):
        """Update game time (called each frame/tick)"""
        # Accelerated time
        scaled_delta = delta_seconds * self.day_night.time_scale

        self.day_night.current_time += timedelta(seconds=scaled_delta)

        # Update sun position
        self._update_sun_position()

        # Update moon phase (slowly)
        self._update_moon_phase()

    def _update_sun_position(self):
        """Update sun altitude and azimuth based on time"""
        hour = self.day_night.current_time.hour
        minute = self.day_night.current_time.minute

        # Total minutes since midnight
        total_minutes = hour * 60 + minute

        # Sun altitude (peaks at noon)
        # 0° at midnight, 90° at noon
        altitude = math.sin((total_minutes / 1440.0) * 2 * math.pi) * 90.0
        self.day_night.sun_altitude = max(altitude, -20.0)

        # Sun azimuth (rotates 360° in 24h)
        self.day_night.sun_azimuth = (total_minutes / 1440.0) * 360.0

    def _update_moon_phase(self):
        """Update moon phase (cycles every ~30 days)"""
        # TODO: Implement lunar cycle
        pass

    def set_time(self, hour: int, minute: int = 0):
        """Manually set game time"""
        self.day_night.current_time = self.day_night.current_time.replace(
            hour=hour,
            minute=minute,
            second=0
        )
        self._update_sun_position()

    def get_time_info(self) -> Dict:
        """Get current time information"""
        return {
            "current_time": self.day_night.current_time.strftime("%H:%M:%S"),
            "time_of_day": self.day_night.get_time_of_day().value,
            "is_night": self.day_night.is_night(),
            "light_level": self.day_night.get_light_level(),
            "sun_altitude": self.day_night.sun_altitude,
            "sun_azimuth": self.day_night.sun_azimuth,
            "moon_phase": self.day_night.moon_phase,
            "time_scale": self.day_night.time_scale
        }

    # ========================================================================
    # CITIES
    # ========================================================================

    def get_city(self, city_id: str) -> Optional[City]:
        """Get city by ID"""
        return self.cities.get(city_id)

    def get_cities_in_biome(self, biome: Biome) -> List[City]:
        """Get all cities in a biome"""
        return [city for city in self.cities.values() if city.biome == biome]

    def can_enter_city(self, city_id: str, player_reputation: int) -> Tuple[bool, str]:
        """Check if player can enter city"""
        city = self.get_city(city_id)
        if not city:
            return False, f"Stadt nicht gefunden: {city_id}"

        if player_reputation < city.min_reputation:
            return False, f"Reputation zu niedrig! Benötigt: {city.min_reputation}, Du hast: {player_reputation}"

        return True, "Willkommen!"

    def get_all_cities(self) -> Dict:
        """Get all cities info"""
        return {
            city_id: {
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
                "min_reputation": city.min_reputation
            }
            for city_id, city in self.cities.items()
        }

    # ========================================================================
    # PROCEDURAL WILDERNESS
    # ========================================================================

    def generate_wilderness(self, biome: Biome, player_id: int) -> WildernessArea:
        """
        Generate procedural wilderness area

        Changes each visit! (new seed)
        """
        # Generate unique seed based on biome + timestamp + player
        seed = hash(f"{biome.value}_{datetime.now().timestamp()}_{player_id}") % (2**31)
        random.seed(seed)

        # Choose layout variant
        layout_variants = self._get_layout_variants(biome)
        layout = random.choice(layout_variants)

        # Generate POIs
        poi_count = random.randint(2, 5)
        pois = self._generate_pois(biome, poi_count)

        # Modifiers
        modifiers = self._generate_modifiers(biome)

        # Density
        enemy_density = random.uniform(0.7, 1.3)
        resource_density = random.uniform(0.8, 1.2)

        # Expiration (wilderness variant expires after leaving)
        expires_at = datetime.now() + timedelta(hours=1)

        wilderness = WildernessArea(
            biome=biome,
            seed=seed,
            layout_variant=layout,
            poi_count=poi_count,
            pois=pois,
            active_events=[],
            modifiers=modifiers,
            enemy_density=enemy_density,
            resource_density=resource_density,
            created_at=datetime.now(),
            expires_at=expires_at
        )

        # Cache it
        cache_key = f"{biome.value}_{player_id}"
        self.wilderness_cache[cache_key] = wilderness

        random.seed()  # Reset seed

        return wilderness

    def _get_layout_variants(self, biome: Biome) -> List[str]:
        """Get possible layout variants for a biome"""
        layouts = {
            Biome.SAMTMOOS_TIEFWALD: ["dense_forest", "river_valley", "mossy_grove"],
            Biome.REICH_DER_DREI: ["frozen_lake", "ice_caves", "glacier_field"],
            Biome.WINDPFAD_HOCHEBENE: ["open_plains", "totem_field", "canyon"],
            Biome.KRISTALLSUMPF: ["murky_swamp", "crystal_grove", "bog"],
            Biome.SCHATTENBERGE: ["dark_peaks", "shadow_valley", "cave_system"],
            Biome.FEUERLAND: ["lava_field", "volcanic_crater", "ash_plains"],
            Biome.STURMKÜSTE: ["cliff_path", "beach", "shipwreck_cove"]
        }

        return layouts.get(biome, ["generic_wilderness"])

    def _generate_pois(self, biome: Biome, count: int) -> List[Dict]:
        """Generate Points of Interest"""
        poi_types = [
            "abandoned_camp", "treasure_cache", "resource_node",
            "mini_boss_spawn", "lore_stone", "shrine", "vendor_npc"
        ]

        pois = []
        for i in range(count):
            poi = {
                "type": random.choice(poi_types),
                "position": (
                    random.uniform(-1000, 1000),
                    0.0,
                    random.uniform(-1000, 1000)
                ),
                "discovered": False
            }
            pois.append(poi)

        return pois

    def _generate_modifiers(self, biome: Biome) -> Dict[str, float]:
        """Generate temporary modifiers"""
        possible_mods = [
            ("xp_bonus", random.uniform(1.0, 1.3)),
            ("loot_bonus", random.uniform(1.0, 1.5)),
            ("enemy_damage", random.uniform(0.9, 1.2)),
            ("resource_yield", random.uniform(0.8, 1.3))
        ]

        # Randomly select 0-2 modifiers
        mod_count = random.randint(0, 2)
        selected = random.sample(possible_mods, mod_count)

        return {mod: value for mod, value in selected}

    def get_wilderness(self, biome: Biome, player_id: int) -> WildernessArea:
        """Get wilderness area (generates new if not cached)"""
        cache_key = f"{biome.value}_{player_id}"

        # Check cache
        if cache_key in self.wilderness_cache:
            wilderness = self.wilderness_cache[cache_key]

            # Check expiration
            if datetime.now() < wilderness.expires_at:
                return wilderness

        # Generate new
        return self.generate_wilderness(biome, player_id)

    # ========================================================================
    # EXPORT STATE
    # ========================================================================

    def export_state(self) -> Dict:
        """Export complete world state"""
        return {
            "map_info": {
                "size_meters": self.MAP_SIZE,
                "size_km2": self.total_area_km2,
                "goetterfels_height": self.GOETTERFELS_HEIGHT,
                "wilderness_percentage": self.wilderness_percentage
            },
            "biomes": {
                biome.value: {
                    "name": config.name,
                    "description": config.description,
                    "slime_color": config.slime_color,
                    "temperature_range": f"{config.temperature_min}°C - {config.temperature_max}°C",
                    "hazardous": config.hazardous
                }
                for biome, config in self.biomes.items()
            },
            "weather": {
                biome.value: {
                    "type": weather.type.value,
                    "intensity": weather.intensity,
                    "temperature": f"{weather.temperature}°C",
                    "wind_speed": f"{weather.wind_speed} m/s",
                    "visibility": weather.visibility,
                    "modifiers": {
                        "movement": weather.movement_modifier,
                        "accuracy": weather.accuracy_modifier,
                        "damage": weather.damage_modifier
                    }
                }
                for biome, weather in self.current_weather.items()
            },
            "time": self.get_time_info(),
            "cities": self.get_all_cities(),
            "total_cities": len(self.cities)
        }


# ============================================================================
# STANDALONE TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("WORLD SYSTEM - Najika World")
    print("=" * 70)
    print()

    # Initialize
    world = WorldSystem()

    # Map Info
    print(f"Map Size: {world.MAP_SIZE}m ({world.total_area_km2} km²)")
    print(f"Götterfels Height: {world.GOETTERFELS_HEIGHT}m")
    print(f"Total Biomes: {len(world.biomes)}")
    print(f"Total Cities: {len(world.cities)}")
    print()

    # Biomes
    print("Biomes:")
    for biome, config in world.biomes.items():
        print(f"  - {config.name} ({biome.value})")
        if config.slime_color:
            print(f"    Slime Color: {config.slime_color}")
    print()

    # Weather
    print("Current Weather:")
    for biome in [Biome.SAMTMOOS_TIEFWALD, Biome.REICH_DER_DREI, Biome.FEUERLAND]:
        weather = world.get_weather(biome)
        config = world.biomes[biome]
        print(f"  {config.name}: {weather.type.value} ({weather.temperature}°C)")
    print()

    # Time
    time_info = world.get_time_info()
    print(f"Game Time: {time_info['current_time']} ({time_info['time_of_day']})")
    print(f"Light Level: {time_info['light_level']:.1%}")
    print(f"Sun Altitude: {time_info['sun_altitude']:.1f}°")
    print()

    # Cities
    print("Cities:")
    for city_id, city in world.cities.items():
        print(f"  - {city.name} ({city.type.value}) in {city.biome.value}")
    print()

    # Wilderness
    print("Generating Wilderness:")
    wilderness = world.generate_wilderness(Biome.SAMTMOOS_TIEFWALD, player_id=1)
    print(f"  Biome: {wilderness.biome.value}")
    print(f"  Layout: {wilderness.layout_variant}")
    print(f"  POIs: {wilderness.poi_count}")
    print(f"  Modifiers: {wilderness.modifiers}")
    print()

    print("=" * 70)
    print("✅ World System Test Complete!")
    print("=" * 70)
