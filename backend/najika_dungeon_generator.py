"""
NAJIKA WORLD - PROCEDURAL DUNGEON GENERATOR
============================================

Generiert prozedural Dungeons für das Keller-Testbed und später für die Außenwelt.

Algorithmus: BSP (Binary Space Partitioning) + Random Walk Hybrid
Inspiration: Diablo, Binding of Isaac, Enter the Gungeon

WICHTIG: Dies ist das KERNFEATURE für Phase 3!
- Erst im Keller testen (klein, kontrolliert)
- Dann auf Außenwelt skalieren

Author: OPUS-1 (Claude Code Desktop)
Date: 2026-01-31
"""

import random
import json
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import math


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class RoomType(Enum):
    """Raumtypen im Dungeon"""
    ENTRANCE = "entrance"       # Startpunkt
    COMBAT = "combat"           # Kampfraum
    LOOT = "loot"               # Schatzkammer
    TRAP = "trap"               # Fallenraum
    PUZZLE = "puzzle"           # Rätselraum
    BOSS = "boss"               # Bossraum
    REST = "rest"               # Rastplatz (Heilen)
    SHOP = "shop"               # Händler
    SECRET = "secret"           # Geheimraum
    CORRIDOR = "corridor"       # Verbindungsgang
    EXIT = "exit"               # Ausgang


class BiomeType(Enum):
    """Die 8 Regionen - Dungeon übernimmt Biom vom Eingang"""
    ICE = "ice"                 # Reich der Drei
    DESERT = "desert"           # Heiße Dünen
    SWAMP = "swamp"             # Grünschlamm-Sumpf
    COAST = "coast"             # Küstenland
    CAVES = "caves"             # Tiefenhöhlen
    VOLCANO = "volcano"         # Magmaströme
    FOREST = "forest"           # Samtmoos-Tiefwald
    HIGHLAND = "highland"       # Blitzebene


class DungeonDifficulty(Enum):
    """Schwierigkeitsgrade"""
    TUTORIAL = 1    # Keller-Testbed (5-10 Räume)
    EASY = 2        # 10-15 Räume
    NORMAL = 3      # 15-25 Räume
    HARD = 4        # 25-40 Räume
    NIGHTMARE = 5   # 40-60 Räume
    ENDLESS = 99    # Unendlich (Roguelike-Modus)


# Raumgewichtungen nach Schwierigkeit
ROOM_WEIGHTS = {
    DungeonDifficulty.TUTORIAL: {
        RoomType.COMBAT: 40,
        RoomType.LOOT: 25,
        RoomType.REST: 20,
        RoomType.TRAP: 10,
        RoomType.PUZZLE: 5,
    },
    DungeonDifficulty.EASY: {
        RoomType.COMBAT: 45,
        RoomType.LOOT: 20,
        RoomType.REST: 15,
        RoomType.TRAP: 12,
        RoomType.PUZZLE: 8,
    },
    DungeonDifficulty.NORMAL: {
        RoomType.COMBAT: 50,
        RoomType.LOOT: 15,
        RoomType.REST: 10,
        RoomType.TRAP: 15,
        RoomType.PUZZLE: 10,
    },
    DungeonDifficulty.HARD: {
        RoomType.COMBAT: 55,
        RoomType.LOOT: 10,
        RoomType.REST: 5,
        RoomType.TRAP: 20,
        RoomType.PUZZLE: 10,
    },
    DungeonDifficulty.NIGHTMARE: {
        RoomType.COMBAT: 60,
        RoomType.LOOT: 8,
        RoomType.REST: 2,
        RoomType.TRAP: 20,
        RoomType.PUZZLE: 10,
    },
}


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Point:
    """2D Punkt"""
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance_to(self, other: 'Point') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass
class Room:
    """Einzelner Raum im Dungeon"""
    id: int
    room_type: RoomType
    position: Point
    width: int
    height: int
    connections: List[int] = field(default_factory=list)
    cleared: bool = False
    discovered: bool = False
    enemies: List[Dict] = field(default_factory=list)
    loot: List[Dict] = field(default_factory=list)
    traps: List[Dict] = field(default_factory=list)
    special_feature: Optional[str] = None

    @property
    def center(self) -> Point:
        return Point(
            self.position.x + self.width // 2,
            self.position.y + self.height // 2
        )

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Returns (x1, y1, x2, y2)"""
        return (
            self.position.x,
            self.position.y,
            self.position.x + self.width,
            self.position.y + self.height
        )

    def overlaps(self, other: 'Room', padding: int = 1) -> bool:
        """Prüft ob zwei Räume überlappen (mit Padding)"""
        x1, y1, x2, y2 = self.bounds
        ox1, oy1, ox2, oy2 = other.bounds

        return not (
            x2 + padding < ox1 or
            ox2 + padding < x1 or
            y2 + padding < oy1 or
            oy2 + padding < y1
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.room_type.value,
            "position": {"x": self.position.x, "y": self.position.y},
            "width": self.width,
            "height": self.height,
            "connections": self.connections,
            "cleared": self.cleared,
            "discovered": self.discovered,
            "enemies": self.enemies,
            "loot": self.loot,
            "traps": self.traps,
            "special_feature": self.special_feature
        }


@dataclass
class Corridor:
    """Verbindungsgang zwischen Räumen"""
    start: Point
    end: Point
    width: int = 2

    def to_dict(self) -> Dict:
        return {
            "start": {"x": self.start.x, "y": self.start.y},
            "end": {"x": self.end.x, "y": self.end.y},
            "width": self.width
        }


@dataclass
class Dungeon:
    """Kompletter Dungeon"""
    seed: int
    biome: BiomeType
    difficulty: DungeonDifficulty
    floor: int
    rooms: List[Room] = field(default_factory=list)
    corridors: List[Corridor] = field(default_factory=list)
    entrance_id: int = 0
    boss_id: int = -1
    exit_id: int = -1

    def to_dict(self) -> Dict:
        return {
            "seed": self.seed,
            "biome": self.biome.value,
            "difficulty": self.difficulty.value,
            "floor": self.floor,
            "rooms": [r.to_dict() for r in self.rooms],
            "corridors": [c.to_dict() for c in self.corridors],
            "entrance_id": self.entrance_id,
            "boss_id": self.boss_id,
            "exit_id": self.exit_id,
            "total_rooms": len(self.rooms),
            "total_corridors": len(self.corridors)
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ============================================================================
# DUNGEON GENERATOR
# ============================================================================

class DungeonGenerator:
    """
    Procedural Dungeon Generator

    Algorithmus:
    1. BSP (Binary Space Partitioning) für Grundstruktur
    2. Random Walk für organische Verbindungen
    3. Room Placement mit Kollisionserkennung
    4. Corridor Generation (L-shaped oder direct)
    5. Room Type Assignment basierend auf Position/Distanz
    6. Enemy/Loot/Trap Spawning basierend auf Biom
    """

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed or random.randint(0, 2**32 - 1)
        self.rng = random.Random(self.seed)

    def generate(
        self,
        biome: BiomeType = BiomeType.CAVES,
        difficulty: DungeonDifficulty = DungeonDifficulty.TUTORIAL,
        floor: int = 1,
        min_rooms: Optional[int] = None,
        max_rooms: Optional[int] = None
    ) -> Dungeon:
        """
        Generiert einen kompletten Dungeon

        Args:
            biome: Das Biom (bestimmt Textur, Monster, Loot)
            difficulty: Schwierigkeit (bestimmt Raumanzahl, Monster-Stärke)
            floor: Aktuelles Stockwerk (für Multi-Floor Dungeons)
            min_rooms: Mindestanzahl Räume (optional)
            max_rooms: Maximalanzahl Räume (optional)

        Returns:
            Dungeon: Fertiger Dungeon
        """
        # Raumanzahl basierend auf Difficulty
        if min_rooms is None or max_rooms is None:
            room_ranges = {
                DungeonDifficulty.TUTORIAL: (5, 10),
                DungeonDifficulty.EASY: (10, 15),
                DungeonDifficulty.NORMAL: (15, 25),
                DungeonDifficulty.HARD: (25, 40),
                DungeonDifficulty.NIGHTMARE: (40, 60),
                DungeonDifficulty.ENDLESS: (50, 100),
            }
            min_rooms, max_rooms = room_ranges.get(difficulty, (10, 20))

        target_rooms = self.rng.randint(min_rooms, max_rooms)

        # Dungeon erstellen
        dungeon = Dungeon(
            seed=self.seed,
            biome=biome,
            difficulty=difficulty,
            floor=floor
        )

        # Räume generieren
        self._generate_rooms(dungeon, target_rooms)

        # Korridore generieren
        self._generate_corridors(dungeon)

        # Raumtypen zuweisen
        self._assign_room_types(dungeon)

        # Inhalt generieren (Gegner, Loot, Fallen)
        self._populate_rooms(dungeon)

        return dungeon

    def _generate_rooms(self, dungeon: Dungeon, target_rooms: int):
        """Generiert Räume mit BSP + Random Walk Hybrid"""

        # Konstanten
        MIN_ROOM_SIZE = 4
        MAX_ROOM_SIZE = 12
        MAP_SIZE = 100  # Maximale Map-Größe

        # Erster Raum (Eingang) in der Mitte
        entrance = Room(
            id=0,
            room_type=RoomType.ENTRANCE,
            position=Point(MAP_SIZE // 2, MAP_SIZE // 2),
            width=self.rng.randint(6, 8),
            height=self.rng.randint(6, 8)
        )
        dungeon.rooms.append(entrance)
        dungeon.entrance_id = 0

        # Weitere Räume generieren
        attempts = 0
        max_attempts = target_rooms * 50  # Maximal 50 Versuche pro Raum

        while len(dungeon.rooms) < target_rooms and attempts < max_attempts:
            attempts += 1

            # Zufälligen existierenden Raum als Ausgangspunkt wählen
            parent_room = self.rng.choice(dungeon.rooms)

            # Neue Raumgröße
            new_width = self.rng.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
            new_height = self.rng.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)

            # Richtung vom Parent-Raum (N/S/E/W)
            direction = self.rng.choice(["north", "south", "east", "west"])

            # Position basierend auf Richtung
            offset = self.rng.randint(3, 8)  # Abstand zwischen Räumen

            if direction == "north":
                new_x = parent_room.center.x - new_width // 2 + self.rng.randint(-3, 3)
                new_y = parent_room.position.y - new_height - offset
            elif direction == "south":
                new_x = parent_room.center.x - new_width // 2 + self.rng.randint(-3, 3)
                new_y = parent_room.position.y + parent_room.height + offset
            elif direction == "east":
                new_x = parent_room.position.x + parent_room.width + offset
                new_y = parent_room.center.y - new_height // 2 + self.rng.randint(-3, 3)
            else:  # west
                new_x = parent_room.position.x - new_width - offset
                new_y = parent_room.center.y - new_height // 2 + self.rng.randint(-3, 3)

            # Bounds check
            if new_x < 0 or new_y < 0 or new_x + new_width > MAP_SIZE or new_y + new_height > MAP_SIZE:
                continue

            # Neuen Raum erstellen
            new_room = Room(
                id=len(dungeon.rooms),
                room_type=RoomType.COMBAT,  # Wird später zugewiesen
                position=Point(int(new_x), int(new_y)),
                width=new_width,
                height=new_height
            )

            # Kollisionsprüfung
            overlaps = False
            for existing_room in dungeon.rooms:
                if new_room.overlaps(existing_room, padding=2):
                    overlaps = True
                    break

            if not overlaps:
                # Verbindung zum Parent-Raum
                new_room.connections.append(parent_room.id)
                parent_room.connections.append(new_room.id)
                dungeon.rooms.append(new_room)

        # Zusätzliche Verbindungen für Loops (macht Dungeon interessanter)
        self._add_extra_connections(dungeon)

    def _add_extra_connections(self, dungeon: Dungeon):
        """Fügt zusätzliche Verbindungen für alternative Wege hinzu"""
        for room in dungeon.rooms:
            # Finde nahe Räume die noch nicht verbunden sind
            for other in dungeon.rooms:
                if other.id == room.id:
                    continue
                if other.id in room.connections:
                    continue

                distance = room.center.distance_to(other.center)

                # Chance für extra Verbindung wenn nah genug
                if distance < 20 and self.rng.random() < 0.2:
                    room.connections.append(other.id)
                    other.connections.append(room.id)

    def _generate_corridors(self, dungeon: Dungeon):
        """Generiert Korridore zwischen verbundenen Räumen"""
        processed_pairs: Set[Tuple[int, int]] = set()

        for room in dungeon.rooms:
            for connected_id in room.connections:
                # Vermeidung von Duplikaten
                pair = tuple(sorted([room.id, connected_id]))
                if pair in processed_pairs:
                    continue
                processed_pairs.add(pair)

                connected_room = dungeon.rooms[connected_id]

                # L-förmiger Korridor
                start = room.center
                end = connected_room.center

                # 50% Chance für horizontale oder vertikale erste Hälfte
                if self.rng.random() < 0.5:
                    # Erst horizontal, dann vertikal
                    mid = Point(end.x, start.y)
                    dungeon.corridors.append(Corridor(start, mid))
                    dungeon.corridors.append(Corridor(mid, end))
                else:
                    # Erst vertikal, dann horizontal
                    mid = Point(start.x, end.y)
                    dungeon.corridors.append(Corridor(start, mid))
                    dungeon.corridors.append(Corridor(mid, end))

    def _assign_room_types(self, dungeon: Dungeon):
        """Weist Raumtypen basierend auf Position und Distanz zu"""
        if len(dungeon.rooms) < 2:
            return

        entrance = dungeon.rooms[dungeon.entrance_id]

        # Finde den am weitesten entfernten Raum für Boss
        max_distance = 0
        boss_room = None

        for room in dungeon.rooms:
            if room.id == dungeon.entrance_id:
                continue

            distance = room.center.distance_to(entrance.center)
            if distance > max_distance:
                max_distance = distance
                boss_room = room

        if boss_room:
            boss_room.room_type = RoomType.BOSS
            dungeon.boss_id = boss_room.id

            # Exit neben Boss oder als separater Raum
            if len(boss_room.connections) > 1:
                # Nutze existierende Verbindung als Exit-Raum
                for conn_id in boss_room.connections:
                    if conn_id != dungeon.entrance_id:
                        exit_room = dungeon.rooms[conn_id]
                        if exit_room.room_type != RoomType.BOSS:
                            exit_room.room_type = RoomType.EXIT
                            dungeon.exit_id = exit_room.id
                            break

        # Restliche Räume zufällig zuweisen
        weights = ROOM_WEIGHTS.get(dungeon.difficulty, ROOM_WEIGHTS[DungeonDifficulty.NORMAL])
        room_types = list(weights.keys())
        room_weights = list(weights.values())

        for room in dungeon.rooms:
            if room.room_type in [RoomType.ENTRANCE, RoomType.BOSS, RoomType.EXIT]:
                continue

            # Gewichtete Zufallsauswahl
            room.room_type = self.rng.choices(room_types, weights=room_weights)[0]

        # Garantiere mindestens einen Shop und Rest-Raum bei längeren Dungeons
        if len(dungeon.rooms) >= 15:
            self._ensure_room_type(dungeon, RoomType.SHOP)
        if len(dungeon.rooms) >= 10:
            self._ensure_room_type(dungeon, RoomType.REST)

        # Secret Room (10% Chance pro Dungeon)
        if self.rng.random() < 0.1:
            self._ensure_room_type(dungeon, RoomType.SECRET)

    def _ensure_room_type(self, dungeon: Dungeon, room_type: RoomType):
        """Stellt sicher dass mindestens ein Raum des Typs existiert"""
        for room in dungeon.rooms:
            if room.room_type == room_type:
                return  # Bereits vorhanden

        # Konvertiere zufälligen COMBAT Raum
        combat_rooms = [r for r in dungeon.rooms if r.room_type == RoomType.COMBAT]
        if combat_rooms:
            room = self.rng.choice(combat_rooms)
            room.room_type = room_type

    def _populate_rooms(self, dungeon: Dungeon):
        """Füllt Räume mit Gegnern, Loot und Fallen"""

        # Biom-spezifische Monster
        biome_enemies = {
            BiomeType.ICE: ["frost_slime", "ice_golem", "snow_wolf", "frozen_skeleton"],
            BiomeType.DESERT: ["sand_slime", "mummy", "scorpion", "dust_devil"],
            BiomeType.SWAMP: ["poison_slime", "frog_monster", "swamp_zombie", "toxic_plant"],
            BiomeType.COAST: ["water_slime", "crab_monster", "sea_serpent", "drowned_one"],
            BiomeType.CAVES: ["crystal_slime", "cave_spider", "bat_swarm", "rock_golem"],
            BiomeType.VOLCANO: ["magma_slime", "fire_elemental", "ash_demon", "lava_serpent"],
            BiomeType.FOREST: ["moss_slime", "treant", "wild_boar", "forest_spirit"],
            BiomeType.HIGHLAND: ["storm_slime", "thunder_hawk", "mountain_troll", "wind_elemental"],
        }

        # Biom-spezifischer Loot
        biome_loot = {
            BiomeType.ICE: ["frost_crystal", "ice_shard", "frozen_heart", "cold_essence"],
            BiomeType.DESERT: ["golden_scarab", "sand_ruby", "ancient_coin", "sun_fragment"],
            BiomeType.SWAMP: ["swamp_moss", "poison_gland", "murky_pearl", "decay_essence"],
            BiomeType.COAST: ["sea_pearl", "coral_fragment", "nautical_map", "water_essence"],
            BiomeType.CAVES: ["raw_crystal", "cave_mushroom", "ancient_fossil", "earth_essence"],
            BiomeType.VOLCANO: ["fire_opal", "volcanic_glass", "ash_remnant", "fire_essence"],
            BiomeType.FOREST: ["rare_herb", "fairy_dust", "ancient_bark", "nature_essence"],
            BiomeType.HIGHLAND: ["storm_crystal", "lightning_shard", "cloud_fragment", "wind_essence"],
        }

        enemies = biome_enemies.get(dungeon.biome, ["generic_slime", "skeleton"])
        loot_items = biome_loot.get(dungeon.biome, ["gold_coin", "potion"])

        difficulty_multiplier = dungeon.difficulty.value

        for room in dungeon.rooms:
            if room.room_type == RoomType.COMBAT:
                # Gegner spawnen
                enemy_count = self.rng.randint(1, 2 + difficulty_multiplier)
                for _ in range(enemy_count):
                    enemy = {
                        "type": self.rng.choice(enemies),
                        "level": dungeon.floor * difficulty_multiplier + self.rng.randint(-1, 2),
                        "position": {
                            "x": self.rng.randint(1, room.width - 2),
                            "y": self.rng.randint(1, room.height - 2)
                        }
                    }
                    room.enemies.append(enemy)

                # Kleiner Loot-Chance
                if self.rng.random() < 0.3:
                    room.loot.append({
                        "type": self.rng.choice(loot_items),
                        "quantity": self.rng.randint(1, 3)
                    })

            elif room.room_type == RoomType.LOOT:
                # Mehr Loot, weniger/keine Gegner
                loot_count = self.rng.randint(2, 4)
                for _ in range(loot_count):
                    room.loot.append({
                        "type": self.rng.choice(loot_items),
                        "quantity": self.rng.randint(1, 5)
                    })

                # Chance auf seltenes Item
                if self.rng.random() < 0.2:
                    room.loot.append({
                        "type": f"rare_{self.rng.choice(loot_items)}",
                        "quantity": 1
                    })

            elif room.room_type == RoomType.TRAP:
                # Fallen und einige Gegner
                trap_count = self.rng.randint(2, 4)
                trap_types = ["spike_trap", "poison_dart", "falling_rocks", "flame_jet", "freezing_floor"]

                for _ in range(trap_count):
                    room.traps.append({
                        "type": self.rng.choice(trap_types),
                        "damage": 10 * difficulty_multiplier,
                        "position": {
                            "x": self.rng.randint(1, room.width - 2),
                            "y": self.rng.randint(1, room.height - 2)
                        }
                    })

                # Belohnung für Überleben
                room.loot.append({
                    "type": self.rng.choice(loot_items),
                    "quantity": self.rng.randint(2, 4)
                })

            elif room.room_type == RoomType.BOSS:
                # Boss-Gegner
                boss_enemies = {
                    BiomeType.ICE: "frost_titan",
                    BiomeType.DESERT: "pharaoh_king",
                    BiomeType.SWAMP: "swamp_hydra",
                    BiomeType.COAST: "kraken_spawn",
                    BiomeType.CAVES: "crystal_guardian",
                    BiomeType.VOLCANO: "magma_lord",
                    BiomeType.FOREST: "ancient_treant",
                    BiomeType.HIGHLAND: "storm_giant",
                }

                room.enemies.append({
                    "type": boss_enemies.get(dungeon.biome, "dungeon_boss"),
                    "level": dungeon.floor * difficulty_multiplier * 2,
                    "is_boss": True,
                    "position": {"x": room.width // 2, "y": room.height // 2}
                })

                # Add some minions
                for _ in range(difficulty_multiplier):
                    room.enemies.append({
                        "type": self.rng.choice(enemies),
                        "level": dungeon.floor * difficulty_multiplier,
                        "position": {
                            "x": self.rng.randint(1, room.width - 2),
                            "y": self.rng.randint(1, room.height - 2)
                        }
                    })

                # Boss loot
                room.loot.append({
                    "type": f"boss_key_{dungeon.biome.value}",
                    "quantity": 1
                })
                room.loot.append({
                    "type": f"legendary_{self.rng.choice(loot_items)}",
                    "quantity": 1
                })

            elif room.room_type == RoomType.SHOP:
                room.special_feature = "shop"
                room.loot = []  # Shop hat Inventar, kein freies Loot

            elif room.room_type == RoomType.REST:
                room.special_feature = "campfire"
                # Kleine Chance auf Loot
                if self.rng.random() < 0.3:
                    room.loot.append({
                        "type": "healing_potion",
                        "quantity": 1
                    })

            elif room.room_type == RoomType.SECRET:
                room.special_feature = "hidden"
                room.discovered = False
                # Guter Loot in geheimen Räumen
                for _ in range(self.rng.randint(3, 5)):
                    room.loot.append({
                        "type": f"rare_{self.rng.choice(loot_items)}",
                        "quantity": self.rng.randint(1, 3)
                    })


# ============================================================================
# API FUNCTIONS
# ============================================================================

def generate_dungeon(
    seed: Optional[int] = None,
    biome: str = "caves",
    difficulty: int = 1,
    floor: int = 1
) -> Dict:
    """
    API-Funktion zum Generieren eines Dungeons

    Args:
        seed: Random Seed (optional, für Reproduzierbarkeit)
        biome: Biom-Name (siehe BiomeType)
        difficulty: 1-5 (oder 99 für Endless)
        floor: Stockwerk (1+)

    Returns:
        Dict: Dungeon als Dictionary
    """
    try:
        biome_type = BiomeType(biome)
    except ValueError:
        biome_type = BiomeType.CAVES

    try:
        diff_type = DungeonDifficulty(difficulty)
    except ValueError:
        diff_type = DungeonDifficulty.TUTORIAL

    generator = DungeonGenerator(seed)
    dungeon = generator.generate(
        biome=biome_type,
        difficulty=diff_type,
        floor=floor
    )

    return dungeon.to_dict()


def generate_keller_testbed(seed: Optional[int] = None) -> Dict:
    """
    Generiert einen kleinen Dungeon für das Keller-Testbed

    Returns:
        Dict: Kleiner Tutorial-Dungeon (5-10 Räume)
    """
    return generate_dungeon(
        seed=seed,
        biome="caves",  # Keller = Höhlen-Biom
        difficulty=1,   # Tutorial
        floor=1
    )


# ============================================================================
# MAIN (Testing)
# ============================================================================

if __name__ == "__main__":
    # Windows Encoding Fix
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 60)
    print("NAJIKA WORLD - PROCEDURAL DUNGEON GENERATOR")
    print("=" * 60)

    # Test: Keller-Testbed
    print("\n[BOX] Generating Keller Testbed Dungeon...")
    testbed = generate_keller_testbed(seed=12345)

    print(f"\n[DICE] Seed: {testbed['seed']}")
    print(f"[TREE] Biome: {testbed['biome']}")
    print(f"[SWORD] Difficulty: {testbed['difficulty']}")
    print(f"[HOUSE] Total Rooms: {testbed['total_rooms']}")
    print(f"[DOOR] Corridors: {testbed['total_corridors']}")

    print("\n[CHART] Room Types:")
    room_counts = {}
    for room in testbed['rooms']:
        rt = room['type']
        room_counts[rt] = room_counts.get(rt, 0) + 1
    for rt, count in sorted(room_counts.items()):
        print(f"  - {rt}: {count}")

    print("\n[MONSTER] Sample Enemies (first combat room):")
    for room in testbed['rooms']:
        if room['type'] == 'combat' and room['enemies']:
            for enemy in room['enemies'][:3]:
                print(f"  - {enemy['type']} (Lvl {enemy['level']})")
            break

    # Test verschiedene Biome
    print("\n" + "=" * 60)
    print("Testing all 8 Biomes...")
    print("=" * 60)

    for biome in BiomeType:
        dungeon = generate_dungeon(biome=biome.value, difficulty=3)
        boss = None
        for room in dungeon['rooms']:
            for enemy in room['enemies']:
                if enemy.get('is_boss'):
                    boss = enemy['type']
                    break
        print(f"  {biome.value.upper():10} - Rooms: {dungeon['total_rooms']:2}, Boss: {boss or 'N/A'}")

    print("\n[OK] Dungeon Generator ready!")
    print("EXPLOSION!!! - Najika")
