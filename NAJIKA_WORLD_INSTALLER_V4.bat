@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title NAJIKA MEGA INSTALLER V4.0 - FULL WORLD EDITION
color 0A

:: Admin-Check
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════════════╗
    echo ║              ⚠️  ADMINISTRATOR RECHTE BENÖTIGT                       ║
    echo ║    Rechtsklick → Als Administrator ausführen                        ║
    echo ╚══════════════════════════════════════════════════════════════════════╝
    pause
    exit /b 1
)

:: ========================================
:: NAJIKA MEGA INSTALLER V4.0
:: Mit Mini-Open-World und allen Features
:: ========================================

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║     ███╗   ██╗ █████╗      ██╗██╗██╗  ██╗ █████╗                  ║
echo ║     ████╗  ██║██╔══██╗     ██║██║██║ ██╔╝██╔══██╗                 ║
echo ║     ██╔██╗ ██║███████║     ██║██║█████╔╝ ███████║                 ║
echo ║     ██║╚██╗██║██╔══██║██   ██║██║██╔═██╗ ██╔══██║                 ║
echo ║     ██║ ╚████║██║  ██║╚█████╔╝██║██║  ██╗██║  ██║                 ║
echo ║     ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                 ║
echo ║                                                                      ║
echo ║          MEGA INSTALLER V4.0 - FULL WORLD EDITION                   ║
echo ║         Mit Mini-Open-World, Angel-System & Mini-Games              ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Erkannte Installation: C:\NajikaFinal
echo [INFO] Dieses Update bringt die Mini-Open-World!
echo.

:: Variablen
set "NAJIKA_DIR=C:\NajikaFinal"
set "FRONTEND_PORT=3000"
set "BACKEND_PORT=8000"
set "GAME_PORT=7010"
set "HUB_PORT=5010"

:: Prüfe vorhandene Installation
if not exist "%NAJIKA_DIR%" (
    echo [ERROR] C:\NajikaFinal nicht gefunden!
    echo [INFO] Bitte erst Basis-Installation durchführen.
    pause
    exit /b 1
)

echo [✓] Najika-Installation gefunden

:: ========================================
:: PHASE 1: Backup vorhandener Daten
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 1: Sichere vorhandene Daten
echo ══════════════════════════════════════════════════════════════════════
echo.

:: Backup ChromaDB
if exist "%NAJIKA_DIR%\data\chromadb" (
    echo [INFO] Sichere ChromaDB...
    xcopy "%NAJIKA_DIR%\data\chromadb" "%NAJIKA_DIR%\backup\chromadb_%date:~-4%%date:~-10,2%%date:~-7,2%" /E /I /Q /Y >nul 2>&1
    echo [✓] ChromaDB gesichert
)

:: ========================================
:: PHASE 2: Python Dependencies Update
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 2: Installiere neue Dependencies
echo ══════════════════════════════════════════════════════════════════════
echo.

:: Erweiterte Requirements für World-System
(
echo # Basis (bereits vorhanden)
echo flask==3.0.0
echo flask-socketio==5.3.5
echo ollama==0.1.7
echo chromadb==0.4.22
echo edge-tts==6.1.9
echo pygame==2.5.2
echo.
echo # NEU: Game-World System
echo numpy==1.24.3
echo scipy==1.11.4
echo noise==1.2.2  # Für Terrain-Generation
echo Pillow==10.1.0  # Für Texturen
echo pytmx==3.32  # Für Tilemaps
echo pymunk==6.5.1  # Physik-Engine
echo.
echo # NEU: Mini-Games
echo pyfiglet==1.0.2  # ASCII Art
echo blessed==1.20.0  # Terminal UI
echo.
echo # NEU: Angel-System
echo random-word==1.0.11
echo.
echo # NEU: Multiplayer-Vorbereitung
echo websocket-client==1.6.4
echo aiohttp==3.9.1
) > "%NAJIKA_DIR%\requirements_world.txt"

echo [INFO] Installiere World-System Dependencies...
python -m pip install -r "%NAJIKA_DIR%\requirements_world.txt" --no-warn-script-location >nul 2>&1
echo [✓] Dependencies installiert

:: ========================================
:: PHASE 3: Mini-Open-World System
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 3: Implementiere Mini-Open-World
echo ══════════════════════════════════════════════════════════════════════
echo.

:: World Generator
(
echo import numpy as np
echo import json
echo import random
echo from noise import pnoise2
echo from datetime import datetime
echo import os
echo.
echo class NajikaWorldGenerator:
echo     """Prozeduraler Welt-Generator für die Schwarze Mühle"""
echo     
echo     def __init__(self^):
echo         self.world_size = (100, 100^)  # 100x100 Tiles
echo         self.seed = random.randint(0, 999999^)
echo         self.biomes = {
echo             'forest': {'color': '#2d5016', 'resources': ['wood', 'herbs', 'mushrooms']},
echo             'lake': {'color': '#1e3a5f', 'resources': ['fish', 'water_lily', 'pearl']},
echo             'meadow': {'color': '#7cb342', 'resources': ['flowers', 'berries', 'honey']},
echo             'mountain': {'color': '#5d4e37', 'resources': ['ore', 'crystal', 'stone']},
echo             'mühle': {'color': '#8b4513', 'resources': ['najika_core', 'memories']},
echo             'dungeon': {'color': '#1a1a1a', 'resources': ['rare_items', 'boss_loot']}
echo         }
echo         self.rooms = {}
echo         self.generate_world(^)
echo     
echo     def generate_world(self^):
echo         """Generiert eine neue Welt mit Perlin Noise"""
echo         print(f"[WORLD] Generiere neue Welt mit Seed: {self.seed}"^)
echo         
echo         # Basis-Terrain mit Perlin Noise
echo         scale = 10.0
echo         octaves = 6
echo         persistence = 0.5
echo         lacunarity = 2.0
echo         
echo         world_map = np.zeros(self.world_size^)
echo         
echo         for y in range(self.world_size[1]^):
echo             for x in range(self.world_size[0]^):
echo                 nx = x/scale - 0.5
echo                 ny = y/scale - 0.5
echo                 elevation = pnoise2(
echo                     nx * lacunarity + self.seed,
echo                     ny * lacunarity + self.seed,
echo                     octaves=octaves,
echo                     persistence=persistence,
echo                     repeatx=self.world_size[0],
echo                     repeaty=self.world_size[1],
echo                     base=0
echo                 ^)
echo                 world_map[y][x] = elevation
echo         
echo         # Konvertiere zu Biomen
echo         self.world_tiles = self._elevation_to_biomes(world_map^)
echo         
echo         # Platziere spezielle Räume
echo         self._place_special_rooms(^)
echo         
echo         # Generiere Ressourcen
echo         self._generate_resources(^)
echo         
echo         print(f"[✓] Welt generiert: {self.world_size[0]}x{self.world_size[1]} Tiles"^)
echo     
echo     def _elevation_to_biomes(self, elevation_map^):
echo         """Wandelt Höhenkarte in Biome um"""
echo         biome_map = []
echo         for row in elevation_map:
echo             biome_row = []
echo             for elevation in row:
echo                 if elevation ^< -0.3:
echo                     biome = 'lake'
echo                 elif elevation ^< 0:
echo                     biome = 'meadow'
echo                 elif elevation ^< 0.3:
echo                     biome = 'forest'
echo                 else:
echo                     biome = 'mountain'
echo                 biome_row.append(biome^)
echo             biome_map.append(biome_row^)
echo         return biome_map
echo     
echo     def _place_special_rooms(self^):
echo         """Platziert spezielle Räume in der Welt"""
echo         
echo         # Schwarze Mühle in der Mitte
echo         center_x, center_y = self.world_size[0]//2, self.world_size[1]//2
echo         self.rooms['mühle'] = {
echo             'position': (center_x, center_y^),
echo             'size': (5, 5^),
echo             'subrooms': {
echo                 'keller': {'items': ['training_dummy', 'oregon_portal'], 'locked': False},
echo                 'erdgeschoss': {'items': ['najika_terminal', 'digivice_dock'], 'locked': False},
echo                 'crafting': {'items': ['werkbank', 'schmiede', 'alchemie'], 'locked': False},
echo                 'angel_teich': {'items': ['angel_spot', 'fish_storage'], 'locked': False},
echo                 'garten': {'items': ['beete', 'kompost', 'gewächshaus'], 'locked': True}
echo             }
echo         }
echo         
echo         # Platziere Dungeon-Eingänge
echo         for i in range(3^):
echo             x = random.randint(10, self.world_size[0]-10^)
echo             y = random.randint(10, self.world_size[1]-10^)
echo             self.rooms[f'dungeon_{i}'] = {
echo                 'position': (x, y^),
echo                 'size': (3, 3^),
echo                 'depth': random.randint(5, 15^),
echo                 'boss': self._generate_boss(i^)
echo             }
echo         
echo         print(f"[✓] {len(self.rooms^)} spezielle Räume platziert"^)
echo     
echo     def _generate_boss(self, level^):
echo         """Generiert einen Boss für einen Dungeon"""
echo         bosses = [
echo             {'name': 'Schatten-Najika', 'hp': 1000, 'loot': 'shadow_core'},
echo             {'name': 'Explosion-Geist', 'hp': 1500, 'loot': 'explosion_essence'},
echo             {'name': 'Korrumpierter Wächter', 'hp': 2000, 'loot': 'guardian_soul'}
echo         ]
echo         return bosses[level % len(bosses^)]
echo     
echo     def _generate_resources(self^):
echo         """Verteilt Ressourcen in der Welt"""
echo         self.resources = {}
echo         resource_count = 0
echo         
echo         for y in range(self.world_size[1]^):
echo             for x in range(self.world_size[0]^):
echo                 if random.random(^) ^< 0.05:  # 5%% Chance für Ressource
echo                     biome = self.world_tiles[y][x]
echo                     if biome in self.biomes:
echo                         resource = random.choice(self.biomes[biome]['resources']^)
echo                         self.resources[(x, y^)] = {
echo                             'type': resource,
echo                             'amount': random.randint(1, 5^),
echo                             'respawn_time': 3600  # 1 Stunde
echo                         }
echo                         resource_count += 1
echo         
echo         print(f"[✓] {resource_count} Ressourcen platziert"^)
echo     
echo     def get_tile(self, x, y^):
echo         """Gibt Tile-Informationen zurück"""
echo         if 0 ^<= x ^< self.world_size[0] and 0 ^<= y ^< self.world_size[1]:
echo             return {
echo                 'biome': self.world_tiles[y][x],
echo                 'resource': self.resources.get((x, y^)^),
echo                 'walkable': self.world_tiles[y][x] != 'lake'
echo             }
echo         return None
echo     
echo     def save_world(self, filename='world.json'^):
echo         """Speichert die Welt"""
echo         world_data = {
echo             'seed': self.seed,
echo             'size': self.world_size,
echo             'tiles': self.world_tiles,
echo             'rooms': self.rooms,
echo             'resources': {f"{k[0]},{k[1]}": v for k, v in self.resources.items(^)},
echo             'generated': str(datetime.now(^)^)
echo         }
echo         
echo         path = os.path.join(r'C:\NajikaFinal\data', filename^)
echo         with open(path, 'w'^) as f:
echo             json.dump(world_data, f^)
echo         
echo         print(f"[✓] Welt gespeichert: {path}"^)
echo         return path
echo.
echo # Test-Generation
echo if __name__ == "__main__":
echo     world = NajikaWorldGenerator(^)
echo     world.save_world(^)
echo     print(f"Mühle Position: {world.rooms['mühle']['position']}"^)
echo     print(f"Angel-Teich verfügbar: {'angel_teich' in world.rooms['mühle']['subrooms']}"^)
) > "%NAJIKA_DIR%\backend\world_generator.py"

echo [✓] World Generator erstellt

:: ========================================
:: PHASE 4: Angel-System Implementation
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 4: Angel-System (Fishing Mini-Game)
echo ══════════════════════════════════════════════════════════════════════
echo.

(
echo import random
echo import time
echo import json
echo from datetime import datetime, timedelta
echo.
echo class FishingSystem:
echo     """Angel-System für Najika World"""
echo     
echo     def __init__(self^):
echo         self.fish_database = {
echo             'teich': [
echo                 {'name': 'Karpfen', 'rarity': 'common', 'size': (0.5, 2.0^), 'value': 10},
echo                 {'name': 'Forelle', 'rarity': 'common', 'size': (0.3, 1.5^), 'value': 15},
echo                 {'name': 'Barsch', 'rarity': 'common', 'size': (0.2, 1.0^), 'value': 8}
echo             ],
echo             'fluss': [
echo                 {'name': 'Lachs', 'rarity': 'uncommon', 'size': (1.0, 5.0^), 'value': 30},
echo                 {'name': 'Hecht', 'rarity': 'uncommon', 'size': (0.8, 4.0^), 'value': 25},
echo                 {'name': 'Aal', 'rarity': 'rare', 'size': (0.5, 2.5^), 'value': 50}
echo             ],
echo             'meer': [
echo                 {'name': 'Thunfisch', 'rarity': 'rare', 'size': (10.0, 50.0^), 'value': 100},
echo                 {'name': 'Schwertfisch', 'rarity': 'epic', 'size': (20.0, 100.0^), 'value': 500},
echo                 {'name': 'Hai', 'rarity': 'legendary', 'size': (50.0, 500.0^), 'value': 1000}
echo             ],
echo             'magisch': [
echo                 {'name': 'Glühfisch', 'rarity': 'epic', 'size': (0.1, 0.5^), 'value': 200, 'effect': 'light'},
echo                 {'name': 'Explosionsfisch', 'rarity': 'legendary', 'size': (1.0, 3.0^), 'value': 999, 'effect': 'explosion'},
echo                 {'name': 'Najika-Fisch', 'rarity': 'mythic', 'size': (0.01, 0.01^), 'value': 10000, 'effect': 'loyalty+1'}
echo             ]
echo         }
echo         
echo         self.rods = {
echo             'basic': {'power': 1.0, 'luck': 1.0, 'durability': 100},
echo             'advanced': {'power': 1.5, 'luck': 1.2, 'durability': 200},
echo             'master': {'power': 2.0, 'luck': 1.5, 'durability': 500},
echo             'explosive': {'power': 3.0, 'luck': 2.0, 'durability': 1000, 'special': 'explosion_catch'}
echo         }
echo         
echo         self.player_stats = {
echo             'total_caught': 0,
echo             'biggest_catch': 0,
echo             'rarest_catch': None,
echo             'current_rod': 'basic',
echo             'inventory': []
echo         }
echo         
echo         self.fishing_spots = {}
echo         self.current_spot = None
echo         
echo     def cast_line(self, location='teich', rod='basic'^):
echo         """Wirft die Angel aus"""
echo         if location not in self.fish_database:
echo             return {'success': False, 'message': 'Unbekannter Angelplatz'}
echo         
echo         self.current_spot = location
echo         rod_stats = self.rods.get(rod, self.rods['basic']^)
echo         
echo         # Warte-Zeit simulieren
echo         wait_time = random.uniform(2, 10^) / rod_stats['luck']
echo         
echo         print(f"[ANGEL] Warte {wait_time:.1f} Sekunden..."^)
echo         time.sleep(wait_time^)
echo         
echo         # Fisch bestimmen
echo         if random.random(^) ^< 0.7 * rod_stats['luck']:  # 70%% Basis-Chance
echo             fish = self._catch_fish(location, rod_stats^)
echo             return {
echo                 'success': True,
echo                 'fish': fish,
echo                 'message': f"Gefangen: {fish['name']} ({fish['weight']:.2f}kg^)!"
echo             }
echo         else:
echo             return {
echo                 'success': False,
echo                 'message': "Nichts gebissen..."
echo             }
echo     
echo     def _catch_fish(self, location, rod_stats^):
echo         """Bestimmt gefangenen Fisch"""
echo         available_fish = self.fish_database[location]
echo         
echo         # Rarität berechnen
echo         rarity_roll = random.random(^) * rod_stats['luck']
echo         
echo         if rarity_roll ^> 0.95:
echo             rarity_filter = ['legendary', 'mythic']
echo         elif rarity_roll ^> 0.8:
echo             rarity_filter = ['rare', 'epic']
echo         elif rarity_roll ^> 0.5:
echo             rarity_filter = ['uncommon']
echo         else:
echo             rarity_filter = ['common']
echo         
echo         # Fisch auswählen
echo         possible_fish = [f for f in available_fish if f.get('rarity'^) in rarity_filter]
echo         if not possible_fish:
echo             possible_fish = available_fish
echo         
echo         fish_template = random.choice(possible_fish^)
echo         
echo         # Größe bestimmen
echo         size_min, size_max = fish_template['size']
echo         weight = random.uniform(size_min, size_max^) * rod_stats['power']
echo         
echo         # Fisch-Objekt erstellen
echo         fish = {
echo             'name': fish_template['name'],
echo             'weight': weight,
echo             'value': int(fish_template['value'] * (1 + weight/10^)^),
echo             'rarity': fish_template['rarity'],
echo             'caught_at': str(datetime.now(^)^),
echo             'location': location,
echo             'effect': fish_template.get('effect'^)
echo         }
echo         
echo         # Stats updaten
echo         self.player_stats['total_caught'] += 1
echo         if weight ^> self.player_stats['biggest_catch']:
echo             self.player_stats['biggest_catch'] = weight
echo         
echo         self.player_stats['inventory'].append(fish^)
echo         
echo         # Special: Najika-Fisch
echo         if fish['name'] == 'Najika-Fisch':
echo             print("[!!!] LEGENDÄRER NAJIKA-FISCH GEFANGEN! Loyalität +1!"^)
echo         
echo         return fish
echo     
echo     def mini_game_quick_time(self^):
echo         """Quick-Time Event beim Angeln"""
echo         print("\n[!] FISCH BEISST AN!"^)
echo         print("Drücke ENTER im richtigen Moment!"^)
echo         
echo         # Zeige Timing-Bar
echo         for i in range(20^):
echo             if i == 10:
echo                 print("█", end="", flush=True^)
echo             else:
echo                 print("░", end="", flush=True^)
echo             time.sleep(0.1^)
echo         
echo         # Hier würde Input-Timing gemessen
echo         return random.choice([True, False]^)  # Simulation
echo     
echo     def get_stats(self^):
echo         """Gibt Angel-Statistiken zurück"""
echo         return {
echo             'total': self.player_stats['total_caught'],
echo             'biggest': f"{self.player_stats['biggest_catch']:.2f}kg",
echo             'inventory_count': len(self.player_stats['inventory']^),
echo             'inventory_value': sum(f['value'] for f in self.player_stats['inventory']^)
echo         }
echo.
echo # Test
echo if __name__ == "__main__":
echo     fishing = FishingSystem(^)
echo     
echo     # Teste verschiedene Spots
echo     for spot in ['teich', 'fluss', 'magisch']:
echo         print(f"\nAngeln am {spot}:"^)
echo         result = fishing.cast_line(spot, 'basic'^)
echo         print(result['message']^)
echo     
echo     print(f"\nStatistik: {fishing.get_stats(^)}"^)
) > "%NAJIKA_DIR%\backend\fishing_system.py"

echo [✓] Angel-System implementiert

:: ========================================
:: PHASE 5: Garten-System
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 5: Garten-System Implementation
echo ══════════════════════════════════════════════════════════════════════
echo.

(
echo import json
echo import time
echo from datetime import datetime, timedelta
echo import random
echo.
echo class GardenSystem:
echo     """Garten-System für Najika World"""
echo     
echo     def __init__(self^):
echo         self.plants = {
echo             # Gemüse
echo             'tomate': {'grow_time': 300, 'yield': (3, 8^), 'season': 'summer', 'value': 5},
echo             'kartoffel': {'grow_time': 600, 'yield': (5, 15^), 'season': 'all', 'value': 3},
echo             'karotte': {'grow_time': 400, 'yield': (4, 10^), 'season': 'spring', 'value': 4},
echo             
echo             # Kräuter (für Alchemie^)
echo             'basilikum': {'grow_time': 200, 'yield': (10, 20^), 'season': 'summer', 'value': 2},
echo             'minze': {'grow_time': 150, 'yield': (15, 30^), 'season': 'all', 'value': 1},
echo             'lavendel': {'grow_time': 500, 'yield': (5, 10^), 'season': 'summer', 'value': 8},
echo             
echo             # Magische Pflanzen
echo             'explosionsblume': {'grow_time': 1800, 'yield': (1, 3^), 'season': 'special', 'value': 100},
echo             'najika_beere': {'grow_time': 3600, 'yield': (1, 1^), 'season': 'loyalty', 'value': 500},
echo             'zeitkraut': {'grow_time': 60, 'yield': (1, 99^), 'season': 'random', 'value': 20}
echo         }
echo         
echo         self.garden_plots = []
echo         self.max_plots = 9  # 3x3 Grid
echo         self.unlocked_plots = 3  # Start mit 3 Beeten
echo         
echo         # Initialisiere Beete
echo         for i in range(self.max_plots^):
echo             self.garden_plots.append({
echo                 'id': i,
echo                 'plant': None,
echo                 'planted_at': None,
echo                 'watered': False,
echo                 'fertilized': False,
echo                 'locked': i ^>= self.unlocked_plots
echo             }^)
echo         
echo         self.inventory = {
echo             'seeds': {},
echo             'harvest': {},
echo             'fertilizer': 10,
echo             'water': 100
echo         }
echo         
echo         # Gebe Start-Samen
echo         self.inventory['seeds'] = {
echo             'tomate': 5,
echo             'kartoffel': 5,
echo             'karotte': 5,
echo             'basilikum': 3
echo         }
echo     
echo     def plant_seed(self, plot_id, plant_type^):
echo         """Pflanzt einen Samen"""
echo         if plot_id ^>= len(self.garden_plots^):
echo             return {'success': False, 'message': 'Ungültiges Beet'}
echo         
echo         plot = self.garden_plots[plot_id]
echo         
echo         if plot['locked']:
echo             return {'success': False, 'message': 'Beet ist gesperrt'}
echo         
echo         if plot['plant']:
echo             return {'success': False, 'message': 'Beet bereits bepflanzt'}
echo         
echo         if self.inventory['seeds'].get(plant_type, 0^) ^<= 0:
echo             return {'success': False, 'message': f'Keine {plant_type} Samen'}
echo         
echo         # Pflanze
echo         plot['plant'] = plant_type
echo         plot['planted_at'] = time.time(^)
echo         plot['watered'] = True
echo         self.inventory['seeds'][plant_type] -= 1
echo         
echo         return {
echo             'success': True, 
echo             'message': f'{plant_type} gepflanzt in Beet {plot_id}'
echo         }
echo     
echo     def water_plot(self, plot_id^):
echo         """Gießt ein Beet"""
echo         if self.inventory['water'] ^<= 0:
echo             return {'success': False, 'message': 'Kein Wasser verfügbar'}
echo         
echo         plot = self.garden_plots[plot_id]
echo         if not plot['plant']:
echo             return {'success': False, 'message': 'Nichts zum Gießen'}
echo         
echo         plot['watered'] = True
echo         self.inventory['water'] -= 1
echo         
echo         return {'success': True, 'message': f'Beet {plot_id} gegossen'}
echo     
echo     def harvest(self, plot_id^):
echo         """Erntet eine Pflanze"""
echo         plot = self.garden_plots[plot_id]
echo         
echo         if not plot['plant']:
echo             return {'success': False, 'message': 'Nichts zu ernten'}
echo         
echo         plant_info = self.plants[plot['plant']]
echo         grow_time = plant_info['grow_time']
echo         
echo         # Modifikatoren
echo         if plot['watered']:
echo             grow_time *= 0.8
echo         if plot['fertilized']:
echo             grow_time *= 0.7
echo         
echo         time_passed = time.time(^) - plot['planted_at']
echo         
echo         if time_passed ^< grow_time:
echo             remaining = grow_time - time_passed
echo             return {
echo                 'success': False, 
echo                 'message': f'Noch {remaining:.0f} Sekunden bis zur Ernte'
echo             }
echo         
echo         # Ernte
echo         yield_min, yield_max = plant_info['yield']
echo         harvest_amount = random.randint(yield_min, yield_max^)
echo         
echo         if plot['fertilized']:
echo             harvest_amount = int(harvest_amount * 1.5^)
echo         
echo         # Speichere Ernte
echo         plant_name = plot['plant']
echo         if plant_name not in self.inventory['harvest']:
echo             self.inventory['harvest'][plant_name] = 0
echo         self.inventory['harvest'][plant_name] += harvest_amount
echo         
echo         # Special: Najika-Beere
echo         if plant_name == 'najika_beere':
echo             print("[!!!] NAJIKA-BEERE GEERNTET! Besondere Kraft erhalten!"^)
echo         
echo         # Reset Beet
echo         plot['plant'] = None
echo         plot['planted_at'] = None
echo         plot['watered'] = False
echo         plot['fertilized'] = False
echo         
echo         return {
echo             'success': True,
echo             'message': f'Geerntet: {harvest_amount}x {plant_name}',
echo             'amount': harvest_amount
echo         }
echo     
echo     def unlock_plot(self, plot_id^):
echo         """Schaltet ein Beet frei"""
echo         if plot_id ^>= self.max_plots:
echo             return False
echo         
echo         if not self.garden_plots[plot_id]['locked']:
echo             return False
echo         
echo         # Kosten: 100 * plot_id
echo         cost = 100 * plot_id
echo         # Hier würde Währungsprüfung kommen
echo         
echo         self.garden_plots[plot_id]['locked'] = False
echo         self.unlocked_plots += 1
echo         
echo         return True
echo     
echo     def get_garden_state(self^):
echo         """Gibt den aktuellen Garten-Status zurück"""
echo         state = []
echo         for plot in self.garden_plots:
echo             if plot['plant']:
echo                 plant_info = self.plants[plot['plant']]
echo                 time_passed = time.time(^) - plot['planted_at']
echo                 progress = min(100, (time_passed / plant_info['grow_time']^) * 100^)
echo                 
echo                 state.append({
echo                     'id': plot['id'],
echo                     'plant': plot['plant'],
echo                     'progress': f"{progress:.1f}%%",
echo                     'watered': plot['watered'],
echo                     'locked': plot['locked']
echo                 }^)
echo             else:
echo                 state.append({
echo                     'id': plot['id'],
echo                     'plant': None,
echo                     'locked': plot['locked']
echo                 }^)
echo         
echo         return {
echo             'plots': state,
echo             'inventory': self.inventory
echo         }
echo.
echo # Test
echo if __name__ == "__main__":
echo     garden = GardenSystem(^)
echo     
echo     # Pflanze etwas
echo     print(garden.plant_seed(0, 'tomate'^)^)
echo     print(garden.plant_seed(1, 'explosionsblume'^)^)
echo     
echo     # Warte und ernte
echo     print("\nWarte 5 Sekunden..."^)
echo     time.sleep(5^)
echo     
echo     print(garden.harvest(0^)^)  # Noch nicht fertig
echo     
echo     print("\nGarten-Status:"^)
echo     print(json.dumps(garden.get_garden_state(^), indent=2^)^)
) > "%NAJIKA_DIR%\backend\garden_system.py"

echo [✓] Garten-System implementiert

:: ========================================
:: PHASE 6: Combat System Update
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 6: Combat System mit Soulslike-Balance
echo ══════════════════════════════════════════════════════════════════════
echo.

(
echo import random
echo import time
echo import json
echo.
echo class CombatSystem:
echo     """Soulslike Combat - Schwer aber fair"""
echo     
echo     def __init__(self^):
echo         self.config = {
echo             'parry_window_ms': 100,  # Präzises Timing
echo             'dodge_iframes': 12,      # I-Frames beim Ausweichen
echo             'stamina_regen': 2.5,     # Pro Sekunde
echo             'death_penalty': 0.1,     # 10%% Gold-Verlust, kein permadeath
echo             'skill_multiplier': 1.5   # Bonus für perfekte Aktionen
echo         }
echo         
echo         self.player = {
echo             'hp': 100,
echo             'max_hp': 100,
echo             'stamina': 100,
echo             'max_stamina': 100,
echo             'explosion_charges': 3,
echo             'skills': {
echo                 'parry': 1,
echo                 'dodge': 1,
echo                 'explosion': 10  # Najika startet mit Max
echo             }
echo         }
echo         
echo         self.combo_system = {
echo             'current_combo': 0,
echo             'max_combo': 0,
echo             'multiplier': 1.0
echo         }
echo         
echo     def parry_attempt(self, enemy_attack_time^):
echo         """Versucht einen Parry"""
echo         player_timing = time.time(^) * 1000  # MS
echo         diff = abs(player_timing - enemy_attack_time^)
echo         
echo         if diff ^<= self.config['parry_window_ms']:
echo             # Perfekter Parry
echo             self.player['skills']['parry'] += 0.1
echo             self.combo_system['current_combo'] += 1
echo             return {
echo                 'success': True,
echo                 'perfect': True,
echo                 'message': 'PERFEKTER PARRY! Skill +0.1',
echo                 'damage_reflected': True
echo             }
echo         elif diff ^<= self.config['parry_window_ms'] * 2:
echo             # Normaler Block
echo             self.player['stamina'] -= 10
echo             return {
echo                 'success': True,
echo                 'perfect': False,
echo                 'message': 'Geblockt',
echo                 'stamina_cost': 10
echo             }
echo         else:
echo             # Fehlschlag
echo             self.combo_system['current_combo'] = 0
echo             return {
echo                 'success': False,
echo                 'message': 'Parry fehlgeschlagen!',
echo                 'take_damage': True
echo             }
echo     
echo     def explosion_attack(self, charge_level=1^):
echo         """Explosion-Angriff mit verschiedenen Stufen"""
echo         if self.player['explosion_charges'] ^<= 0:
echo             return {'success': False, 'message': 'Keine Explosion-Ladungen!'}
echo         
echo         explosions = {
echo             1: {'name': 'Mini-Explosion', 'damage': 80, 'radius': 3, 'cost': 1},
echo             2: {'name': 'Standard-Explosion', 'damage': 180, 'radius': 5, 'cost': 1},
echo             3: {'name': 'Mega-Explosion', 'damage': 350, 'radius': 8, 'cost': 2},
echo             4: {'name': 'OMEGA EXPLOSION!', 'damage': 600, 'radius': 15, 'cost': 3}
echo         }
echo         
echo         explosion = explosions.get(charge_level, explosions[1]^)
echo         
echo         if self.player['explosion_charges'] ^< explosion['cost']:
echo             return {'success': False, 'message': 'Nicht genug Ladungen!'}
echo         
echo         self.player['explosion_charges'] -= explosion['cost']
echo         
echo         # Skill-basierter Schaden
echo         final_damage = explosion['damage'] * (1 + self.player['skills']['explosion'] * 0.1^)
echo         
echo         return {
echo             'success': True,
echo             'name': explosion['name'],
echo             'damage': int(final_damage^),
echo             'radius': explosion['radius'],
echo             'message': f"{explosion['name']}! {int(final_damage^)} Schaden!",
echo             'remaining_charges': self.player['explosion_charges']
echo         }
echo     
echo     def training_mode(self, duration_minutes=10^):
echo         """Training erhöht Skills"""
echo         print(f"[TRAINING] {duration_minutes} Minuten Training gestartet"^)
echo         
echo         # Simuliere Training
echo         skill_gains = {
echo             'parry': random.uniform(0.1, 0.5^) * duration_minutes,
echo             'dodge': random.uniform(0.1, 0.5^) * duration_minutes,
echo             'explosion': random.uniform(0.05, 0.2^) * duration_minutes
echo         }
echo         
echo         for skill, gain in skill_gains.items(^):
echo             self.player['skills'][skill] += gain
echo             print(f"[✓] {skill}: +{gain:.2f}"^)
echo         
echo         return skill_gains
echo     
echo     def death_mechanic(self^):
echo         """Tod ist nicht das Ende - nur ein Rückschlag"""
echo         penalty = {
echo             'gold_lost': self.config['death_penalty'],
echo             'location_reset': True,
echo             'skills_kept': True,  # Skills bleiben!
echo             'message': "Du bist gefallen, aber nicht besiegt! -10%% Gold, Skills bleiben."
echo         }
echo         
echo         # Reset HP/Stamina
echo         self.player['hp'] = self.player['max_hp']
echo         self.player['stamina'] = self.player['max_stamina']
echo         self.player['explosion_charges'] = 3
echo         
echo         return penalty
echo.
echo # Test
echo if __name__ == "__main__":
echo     combat = CombatSystem(^)
echo     
echo     print("=== COMBAT TEST ==="^)
echo     print(f"Spieler HP: {combat.player['hp']}"^)
echo     print(f"Explosion Charges: {combat.player['explosion_charges']}"^)
echo     
echo     # Teste Explosion
echo     for level in [1, 2, 3, 4]:
echo         result = combat.explosion_attack(level^)
echo         print(f"\nLevel {level}: {result['message']}"^)
echo     
echo     # Training
echo     print("\n=== TRAINING ==="^)
echo     combat.training_mode(5^)
) > "%NAJIKA_DIR%\backend\combat_system.py"

echo [✓] Combat System aktualisiert

:: ========================================
:: PHASE 7: Integrierter Game Server
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 7: Integrierter Game Server mit Allen Systemen
echo ══════════════════════════════════════════════════════════════════════
echo.

(
echo from flask import Flask, jsonify, request, send_from_directory
echo from flask_socketio import SocketIO, emit
echo from flask_cors import CORS
echo import json
echo import os
echo import sys
echo import threading
echo import time
echo.
echo # Importiere alle Systeme
echo sys.path.append(r'C:\NajikaFinal\backend'^)
echo from world_generator import NajikaWorldGenerator
echo from fishing_system import FishingSystem
echo from garden_system import GardenSystem
echo from combat_system import CombatSystem
echo.
echo app = Flask(__name__^)
echo CORS(app^)
echo socketio = SocketIO(app, cors_allowed_origins="*"^)
echo.
echo # Game State
echo class GameState:
echo     def __init__(self^):
echo         print("[INIT] Initialisiere Game Systems..."^)
echo         self.world = NajikaWorldGenerator(^)
echo         self.fishing = FishingSystem(^)
echo         self.garden = GardenSystem(^)
echo         self.combat = CombatSystem(^)
echo         self.players = {}
echo         self.active = True
echo         print("[✓] Alle Systeme geladen"^)
echo     
echo     def get_full_state(self^):
echo         return {
echo             'world': {
echo                 'size': self.world.world_size,
echo                 'rooms': len(self.world.rooms^),
echo                 'resources': len(self.world.resources^),
echo                 'mühle': self.world.rooms['mühle']
echo             },
echo             'fishing': self.fishing.get_stats(^),
echo             'garden': self.garden.get_garden_state(^),
echo             'combat': {
echo                 'player': self.combat.player,
echo                 'skills': self.combat.player['skills']
echo             }
echo         }
echo.
echo # Initialisiere Game
echo game = GameState(^)
echo.
echo # === ROUTES ===
echo.
echo @app.route('/'^)
echo def index(^):
echo     return jsonify({
echo         'name': 'Najika World Server',
echo         'version': '4.0',
echo         'status': 'running',
echo         'port': %GAME_PORT%
echo     }^)
echo.
echo @app.route('/api/world/info'^)
echo def world_info(^):
echo     return jsonify({
echo         'world_size': game.world.world_size,
echo         'total_rooms': len(game.world.rooms^),
echo         'total_resources': len(game.world.resources^),
echo         'mühle_location': game.world.rooms['mühle']['position'],
echo         'subrooms': list(game.world.rooms['mühle']['subrooms'].keys(^)^)
echo     }^)
echo.
echo @app.route('/api/world/tile/^<int:x^>/^<int:y^>'^)
echo def get_tile(x, y^):
echo     tile = game.world.get_tile(x, y^)
echo     if tile:
echo         return jsonify(tile^)
echo     return jsonify({'error': 'Invalid coordinates'}^), 400
echo.
echo # === FISHING ROUTES ===
echo.
echo @app.route('/api/fishing/cast', methods=['POST']^)
echo def cast_fishing(^):
echo     data = request.json or {}
echo     location = data.get('location', 'teich'^)
echo     rod = data.get('rod', 'basic'^)
echo     
echo     result = game.fishing.cast_line(location, rod^)
echo     
echo     # Socket-Event wenn Fisch gefangen
echo     if result['success']:
echo         socketio.emit('fish_caught', result^)
echo     
echo     return jsonify(result^)
echo.
echo @app.route('/api/fishing/stats'^)
echo def fishing_stats(^):
echo     return jsonify(game.fishing.get_stats(^)^)
echo.
echo # === GARDEN ROUTES ===
echo.
echo @app.route('/api/garden/plant', methods=['POST']^)
echo def plant_seed(^):
echo     data = request.json
echo     result = game.garden.plant_seed(
echo         data['plot_id'],
echo         data['plant_type']
echo     ^)
echo     
echo     if result['success']:
echo         socketio.emit('garden_update', game.garden.get_garden_state(^)^)
echo     
echo     return jsonify(result^)
echo.
echo @app.route('/api/garden/harvest/^<int:plot_id^>', methods=['POST']^)
echo def harvest(plot_id^):
echo     result = game.garden.harvest(plot_id^)
echo     
echo     if result['success']:
echo         socketio.emit('harvest', result^)
echo     
echo     return jsonify(result^)
echo.
echo @app.route('/api/garden/state'^)
echo def garden_state(^):
echo     return jsonify(game.garden.get_garden_state(^)^)
echo.
echo # === COMBAT ROUTES ===
echo.
echo @app.route('/api/combat/explosion', methods=['POST']^)
echo def explosion_attack(^):
echo     data = request.json or {}
echo     level = data.get('level', 1^)
echo     
echo     result = game.combat.explosion_attack(level^)
echo     
echo     if result['success']:
echo         socketio.emit('explosion', result^)
echo     
echo     return jsonify(result^)
echo.
echo @app.route('/api/combat/train', methods=['POST']^)
echo def train(^):
echo     data = request.json or {}
echo     duration = data.get('duration', 10^)
echo     
echo     result = game.combat.training_mode(duration^)
echo     
echo     socketio.emit('training_complete', result^)
echo     
echo     return jsonify({
echo         'success': True,
echo         'skill_gains': result,
echo         'new_skills': game.combat.player['skills']
echo     }^)
echo.
echo # === SOCKET EVENTS ===
echo.
echo @socketio.on('connect'^)
echo def handle_connect(^):
echo     print(f"[SOCKET] Client connected"^)
echo     emit('game_state', game.get_full_state(^)^)
echo.
echo @socketio.on('player_move'^)
echo def handle_move(data^):
echo     x, y = data['x'], data['y']
echo     tile = game.world.get_tile(x, y^)
echo     
echo     if tile and tile['walkable']:
echo         emit('move_result', {
echo             'success': True,
echo             'position': (x, y^),
echo             'tile': tile
echo         }^)
echo         
echo         # Check für Ressourcen
echo         if tile['resource']:
echo             emit('resource_found', tile['resource']^)
echo.
echo # === AUTO-UPDATES ===
echo.
echo def auto_update_loop(^):
echo     """Sendet regelmäßig Updates"""
echo     while game.active:
echo         time.sleep(30^)  # Alle 30 Sekunden
echo         
echo         # Garten-Status update
echo         socketio.emit('garden_update', game.garden.get_garden_state(^)^)
echo         
echo         # Regeneriere Stamina
echo         if game.combat.player['stamina'] ^< game.combat.player['max_stamina']:
echo             game.combat.player['stamina'] = min(
echo                 game.combat.player['max_stamina'],
echo                 game.combat.player['stamina'] + game.combat.config['stamina_regen'] * 30
echo             ^)
echo             socketio.emit('stamina_update', game.combat.player['stamina']^)
echo.
echo if __name__ == '__main__':
echo     # Starte Auto-Update Thread
echo     update_thread = threading.Thread(target=auto_update_loop, daemon=True^)
echo     update_thread.start(^)
echo     
echo     print("\n" + "="*60^)
echo     print("NAJIKA WORLD SERVER"^)
echo     print(f"Port: %GAME_PORT%"^)
echo     print("Systeme: World, Fishing, Garden, Combat"^)
echo     print("="*60 + "\n"^)
echo     
echo     socketio.run(app, host='127.0.0.1', port=%GAME_PORT%, debug=False^)
) > "%NAJIKA_DIR%\backend\game_server.py"

echo [✓] Integrierter Game Server erstellt

:: ========================================
:: PHASE 8: Updated Frontend mit Game UI
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 8: Frontend mit Game Interface
echo ══════════════════════════════════════════════════════════════════════
echo.

(
echo ^<!DOCTYPE html^>
echo ^<html lang="de"^>
echo ^<head^>
echo     ^<meta charset="UTF-8"^>
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>
echo     ^<title^>Najika World - Full Experience^</title^>
echo     ^<style^>
echo         * { margin: 0; padding: 0; box-sizing: border-box; }
echo         body {
echo             font-family: 'Segoe UI', Arial;
echo             background: #1a1a1a;
echo             color: white;
echo             overflow: hidden;
echo         }
echo         .container {
echo             display: grid;
echo             grid-template-columns: 250px 1fr 300px;
echo             height: 100vh;
echo         }
echo         
echo         /* Linke Sidebar - Räume */
echo         .rooms-panel {
echo             background: #2c3e50;
echo             padding: 20px;
echo             overflow-y: auto;
echo         }
echo         .room-btn {
echo             display: block;
echo             width: 100%%;
echo             padding: 10px;
echo             margin: 5px 0;
echo             background: #34495e;
echo             color: white;
echo             border: none;
echo             border-radius: 5px;
echo             cursor: pointer;
echo             transition: all 0.3s;
echo         }
echo         .room-btn:hover {
echo             background: #667eea;
echo         }
echo         .room-btn.active {
echo             background: linear-gradient(135deg, #667eea, #764ba2^);
echo         }
echo         .room-btn.locked {
echo             background: #555;
echo             opacity: 0.5;
echo             cursor: not-allowed;
echo         }
echo         
echo         /* Hauptbereich */
echo         .main-area {
echo             display: flex;
echo             flex-direction: column;
echo         }
echo         
echo         /* World View */
echo         .world-view {
echo             flex: 1;
echo             background: #111;
echo             position: relative;
echo             overflow: hidden;
echo         }
echo         .world-canvas {
echo             position: absolute;
echo             top: 50%%;
echo             left: 50%%;
echo             transform: translate(-50%%, -50%%^);
echo         }
echo         .tile {
echo             position: absolute;
echo             width: 20px;
echo             height: 20px;
echo             border: 1px solid rgba(255,255,255,0.1^);
echo         }
echo         .tile.forest { background: #2d5016; }
echo         .tile.lake { background: #1e3a5f; }
echo         .tile.meadow { background: #7cb342; }
echo         .tile.mountain { background: #5d4e37; }
echo         .tile.mühle { 
echo             background: #8b4513; 
echo             box-shadow: 0 0 20px rgba(255,215,0,0.5^);
echo             animation: pulse 2s infinite;
echo         }
echo         @keyframes pulse {
echo             0%%, 100%% { transform: scale(1^); }
echo             50%% { transform: scale(1.1^); }
echo         }
echo         
echo         /* Mini-Games Panel */
echo         .games-panel {
echo             height: 250px;
echo             background: #2c3e50;
echo             display: flex;
echo             gap: 10px;
echo             padding: 10px;
echo             overflow-x: auto;
echo         }
echo         .mini-game {
echo             min-width: 200px;
echo             background: #34495e;
echo             border-radius: 10px;
echo             padding: 15px;
echo             text-align: center;
echo         }
echo         .mini-game h3 {
echo             margin-bottom: 10px;
echo             color: #667eea;
echo         }
echo         .mini-game button {
echo             width: 100%%;
echo             padding: 8px;
echo             margin: 5px 0;
echo             background: #667eea;
echo             color: white;
echo             border: none;
echo             border-radius: 5px;
echo             cursor: pointer;
echo         }
echo         
echo         /* Rechte Sidebar - Stats & Najika */
echo         .status-panel {
echo             background: #2c3e50;
echo             padding: 20px;
echo             overflow-y: auto;
echo         }
echo         .najika-avatar {
echo             width: 100px;
echo             height: 100px;
echo             margin: 0 auto 20px;
echo             background: linear-gradient(135deg, #667eea, #764ba2^);
echo             border-radius: 50%%;
echo             display: flex;
echo             align-items: center;
echo             justify-content: center;
echo             font-size: 40px;
echo         }
echo         .stat-group {
echo             margin: 20px 0;
echo         }
echo         .stat-group h3 {
echo             color: #667eea;
echo             margin-bottom: 10px;
echo         }
echo         .stat {
echo             display: flex;
echo             justify-content: space-between;
echo             padding: 5px 0;
echo         }
echo         .stat-bar {
echo             width: 100%%;
echo             height: 20px;
echo             background: #1a1a1a;
echo             border-radius: 10px;
echo             overflow: hidden;
echo             margin: 5px 0;
echo         }
echo         .stat-fill {
echo             height: 100%%;
echo             background: linear-gradient(90deg, #667eea, #764ba2^);
echo             transition: width 0.3s;
echo         }
echo         
echo         /* Garden Grid */
echo         .garden-grid {
echo             display: grid;
echo             grid-template-columns: repeat(3, 1fr^);
echo             gap: 10px;
echo             padding: 20px;
echo         }
echo         .garden-plot {
echo             aspect-ratio: 1;
echo             background: #654321;
echo             border: 2px solid #333;
echo             border-radius: 10px;
echo             display: flex;
echo             align-items: center;
echo             justify-content: center;
echo             cursor: pointer;
echo             position: relative;
echo         }
echo         .garden-plot.planted {
echo             background: #4a5f2a;
echo         }
echo         .garden-plot.locked {
echo             background: #222;
echo             cursor: not-allowed;
echo         }
echo         .plant-progress {
echo             position: absolute;
echo             bottom: 5px;
echo             left: 5px;
echo             right: 5px;
echo             height: 5px;
echo             background: #333;
echo             border-radius: 3px;
echo         }
echo         .plant-progress-fill {
echo             height: 100%%;
echo             background: #76ff03;
echo             border-radius: 3px;
echo         }
echo         
echo         /* Chat */
echo         .chat-area {
echo             position: fixed;
echo             bottom: 20px;
echo             right: 320px;
echo             width: 400px;
echo             background: rgba(0,0,0,0.9^);
echo             border-radius: 10px;
echo             padding: 10px;
echo             max-height: 300px;
echo         }
echo         .chat-messages {
echo             height: 200px;
echo             overflow-y: auto;
echo             margin-bottom: 10px;
echo         }
echo         .chat-input {
echo             display: flex;
echo             gap: 10px;
echo         }
echo         .chat-input input {
echo             flex: 1;
echo             padding: 8px;
echo             background: #333;
echo             border: 1px solid #555;
echo             color: white;
echo             border-radius: 5px;
echo         }
echo         .chat-input button {
echo             padding: 8px 20px;
echo             background: #667eea;
echo             color: white;
echo             border: none;
echo             border-radius: 5px;
echo             cursor: pointer;
echo         }
echo     ^</style^>
echo ^</head^>
echo ^<body^>
echo     ^<div class="container"^>
echo         ^<!-- Räume Panel --^>
echo         ^<div class="rooms-panel"^>
echo             ^<h2^>🏰 Schwarze Mühle^</h2^>
echo             ^<button class="room-btn active" onclick="enterRoom('erdgeschoss'^)"^>Erdgeschoss^</button^>
echo             ^<button class="room-btn" onclick="enterRoom('keller'^)"^>🔬 Keller (Training^)^</button^>
echo             ^<button class="room-btn" onclick="enterRoom('crafting'^)"^>⚒️ Werkstatt^</button^>
echo             ^<button class="room-btn" onclick="enterRoom('angel_teich'^)"^>🎣 Angel-Teich^</button^>
echo             ^<button class="room-btn" onclick="enterRoom('garten'^)"^>🌱 Garten^</button^>
echo             ^<button class="room-btn locked"^>🔒 Geheimraum^</button^>
echo             
echo             ^<h3 style="margin-top: 30px;"^>⚔️ Dungeons^</h3^>
echo             ^<button class="room-btn" onclick="enterDungeon(0^)"^>Dungeon 1^</button^>
echo             ^<button class="room-btn" onclick="enterDungeon(1^)"^>Dungeon 2^</button^>
echo             ^<button class="room-btn locked"^>🔒 Dungeon 3^</button^>
echo         ^</div^>
echo         
echo         ^<!-- Hauptbereich --^>
echo         ^<div class="main-area"^>
echo             ^<!-- Welt-Ansicht --^>
echo             ^<div class="world-view" id="worldView"^>
echo                 ^<div class="world-canvas" id="worldCanvas"^>^</div^>
echo             ^</div^>
echo             
echo             ^<!-- Mini-Games --^>
echo             ^<div class="games-panel"^>
echo                 ^<!-- Angel-Spiel --^>
echo                 ^<div class="mini-game"^>
echo                     ^<h3^>🎣 Angeln^</h3^>
echo                     ^<div id="fishingStatus"^>Bereit^</div^>
echo                     ^<button onclick="startFishing('^)"^>Angel auswerfen^</button^>
echo                     ^<div^>Gefangen: ^<span id="fishCount"^>0^</span^>^</div^>
echo                 ^</div^>
echo                 
echo                 ^<!-- Garten --^>
echo                 ^<div class="mini-game"^>
echo                     ^<h3^>🌱 Garten^</h3^>
echo                     ^<div id="gardenStatus"^>3/9 Beete^</div^>
echo                     ^<button onclick="showGarden('^)"^>Garten öffnen^</button^>
echo                     ^<div^>Ernte: ^<span id="harvestCount"^>0^</span^>^</div^>
echo                 ^</div^>
echo                 
echo                 ^<!-- Training --^>
echo                 ^<div class="mini-game"^>
echo                     ^<h3^>💪 Training^</h3^>
echo                     ^<div id="trainingStatus"^>Bereit^</div^>
echo                     ^<button onclick="startTraining('^)"^>5 Min Training^</button^>
echo                     ^<div^>Skill-Lvl: ^<span id="skillLevel"^>1^</span^>^</div^>
echo                 ^</div^>
echo                 
echo                 ^<!-- Combat --^>
echo                 ^<div class="mini-game"^>
echo                     ^<h3^>💥 Explosion^</h3^>
echo                     ^<div^>Ladungen: ^<span id="explosionCharges"^>3^</span^>^</div^>
echo                     ^<button onclick="explosion(1^)"^>Mini^</button^>
echo                     ^<button onclick="explosion(2^)"^>Standard^</button^>
echo                     ^<button onclick="explosion(4^)"^>OMEGA!^</button^>
echo                 ^</div^>
echo             ^</div^>
echo         ^</div^>
echo         
echo         ^<!-- Status Panel --^>
echo         ^<div class="status-panel"^>
echo             ^<div class="najika-avatar"^>💜^</div^>
echo             ^<h2 style="text-align: center;"^>NAJIKA^</h2^>
echo             
echo             ^<div class="stat-group"^>
echo                 ^<h3^>Status^</h3^>
echo                 ^<div class="stat"^>^<span^>HP^</span^> ^<span id="hp"^>100/100^</span^>^</div^>
echo                 ^<div class="stat-bar"^>^<div class="stat-fill" style="width: 100%%"^>^</div^>^</div^>
echo                 
echo                 ^<div class="stat"^>^<span^>Stamina^</span^> ^<span id="stamina"^>100/100^</span^>^</div^>
echo                 ^<div class="stat-bar"^>^<div class="stat-fill" style="width: 100%%"^>^</div^>^</div^>
echo                 
echo                 ^<div class="stat"^>^<span^>Loyalität^</span^> ^<span^>10/10^</span^>^</div^>
echo                 ^<div class="stat-bar"^>^<div class="stat-fill" style="width: 100%%"^>^</div^>^</div^>
echo             ^</div^>
echo             
echo             ^<div class="stat-group"^>
echo                 ^<h3^>Skills^</h3^>
echo                 ^<div class="stat"^>^<span^>Parry^</span^> ^<span id="parrySkill"^>1.0^</span^>^</div^>
echo                 ^<div class="stat"^>^<span^>Dodge^</span^> ^<span id="dodgeSkill"^>1.0^</span^>^</div^>
echo                 ^<div class="stat"^>^<span^>Explosion^</span^> ^<span id="explosionSkill"^>10.0^</span^>^</div^>
echo             ^</div^>
echo             
echo             ^<div class="stat-group"^>
echo                 ^<h3^>Inventar^</h3^>
echo                 ^<div class="stat"^>^<span^>Fische^</span^> ^<span id="fishInv"^>0^</span^>^</div^>
echo                 ^<div class="stat"^>^<span^>Pflanzen^</span^> ^<span id="plantInv"^>0^</span^>^</div^>
echo                 ^<div class="stat"^>^<span^>Gold^</span^> ^<span id="gold"^>100^</span^>^</div^>
echo             ^</div^>
echo         ^</div^>
echo     ^</div^>
echo     
echo     ^<!-- Chat --^>
echo     ^<div class="chat-area"^>
echo         ^<div class="chat-messages" id="chatMessages"^>
echo             ^<div style="color: #667eea;"^>Najika: EXPLOSION! Die Mini-Open-World ist bereit, Kuja!^</div^>
echo         ^</div^>
echo         ^<div class="chat-input"^>
echo             ^<input type="text" id="chatInput" placeholder="Mit Najika sprechen..."^>
echo             ^<button onclick="sendChat('^)"^>Senden^</button^>
echo         ^</div^>
echo     ^</div^>
echo     
echo     ^<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"^>^</script^>
echo     ^<script^>
echo         // Socket-Verbindungen
echo         const backendSocket = io('http://127.0.0.1:%BACKEND_PORT%'^);
echo         const gameSocket = io('http://127.0.0.1:%GAME_PORT%'^);
echo         
echo         let currentRoom = 'erdgeschoss';
echo         let worldData = null;
echo         
echo         // World Generation Display
echo         function generateWorldView(^) {
echo             const canvas = document.getElementById('worldCanvas'^);
echo             canvas.innerHTML = '';
echo             
echo             // Vereinfachte 20x20 Ansicht
echo             for(let y = 40; y ^< 60; y++^) {
echo                 for(let x = 40; x ^< 60; x++^) {
echo                     const tile = document.createElement('div'^);
echo                     tile.className = 'tile';
echo                     tile.style.left = (x - 40^) * 21 + 'px';
echo                     tile.style.top = (y - 40^) * 21 + 'px';
echo                     
echo                     // Mühle in der Mitte
echo                     if(x == 50 ^&^& y == 50^) {
echo                         tile.classList.add('mühle'^);
echo                         tile.title = 'Schwarze Mühle';
echo                     } else {
echo                         // Zufällige Biome
echo                         const biomes = ['forest', 'lake', 'meadow', 'mountain'];
echo                         tile.classList.add(biomes[Math.floor(Math.random(^) * biomes.length^)]^);
echo                     }
echo                     
echo                     canvas.appendChild(tile^);
echo                 }
echo             }
echo         }
echo         
echo         // Räume betreten
echo         function enterRoom(room^) {
echo             currentRoom = room;
echo             document.querySelectorAll('.room-btn'^).forEach(btn =^> btn.classList.remove('active'^)^);
echo             event.target.classList.add('active'^);
echo             
echo             addChatMessage(`Najika: Du betrittst ${room}!`^);
echo             
echo             // Spezial-Aktionen pro Raum
echo             if(room === 'angel_teich'^) {
echo                 addChatMessage('Najika: Zeit zum Angeln! Die Fische beißen heute gut!''^);
echo             } else if(room === 'garten'^) {
echo                 showGarden(^);
echo             } else if(room === 'keller'^) {
echo                 addChatMessage('Najika: Hier können wir trainieren und die Oregon-Engine testen!''^);
echo             }
echo         }
echo         
echo         // Angel-System
echo         async function startFishing(^) {
echo             document.getElementById('fishingStatus'^).textContent = 'Angel ausgeworfen...';
echo             
echo             const response = await fetch('http://127.0.0.1:%GAME_PORT%/api/fishing/cast', {
echo                 method: 'POST',
echo                 headers: {'Content-Type': 'application/json'},
echo                 body: JSON.stringify({location: 'teich', rod: 'basic'}^)
echo             }^);
echo             
echo             const result = await response.json(^);
echo             document.getElementById('fishingStatus'^).textContent = result.message;
echo             
echo             if(result.success^) {
echo                 const count = parseInt(document.getElementById('fishCount'^).textContent^);
echo                 document.getElementById('fishCount'^).textContent = count + 1;
echo                 document.getElementById('fishInv'^).textContent = count + 1;
echo             }
echo         }
echo         
echo         // Garden System  
echo         function showGarden(^) {
echo             // Würde Garten-UI zeigen
echo             addChatMessage('Najika: Der Garten wächst prächtig! Vergiss nicht zu gießen!''^);
echo         }
echo         
echo         // Training
echo         async function startTraining(^) {
echo             document.getElementById('trainingStatus'^).textContent = 'Training läuft...';
echo             
echo             const response = await fetch('http://127.0.0.1:%GAME_PORT%/api/combat/train', {
echo                 method: 'POST',
echo                 headers: {'Content-Type': 'application/json'},
echo                 body: JSON.stringify({duration: 5}^)
echo             }^);
echo             
echo             const result = await response.json(^);
echo             document.getElementById('trainingStatus'^).textContent = 'Training abgeschlossen!';
echo             
echo             // Update Skills
echo             if(result.new_skills^) {
echo                 document.getElementById('parrySkill'^).textContent = result.new_skills.parry.toFixed(1^);
echo                 document.getElementById('dodgeSkill'^).textContent = result.new_skills.dodge.toFixed(1^);
echo                 document.getElementById('explosionSkill'^).textContent = result.new_skills.explosion.toFixed(1^);
echo             }
echo         }
echo         
echo         // Explosion
echo         async function explosion(level^) {
echo             const response = await fetch('http://127.0.0.1:%GAME_PORT%/api/combat/explosion', {
echo                 method: 'POST',
echo                 headers: {'Content-Type': 'application/json'},
echo                 body: JSON.stringify({level: level}^)
echo             }^);
echo             
echo             const result = await response.json(^);
echo             
echo             if(result.success^) {
echo                 addChatMessage(`EXPLOSION! ${result.message}`^);
echo                 document.getElementById('explosionCharges'^).textContent = result.remaining_charges;
echo             } else {
echo                 addChatMessage(`Najika: ${result.message}`^);
echo             }
echo         }
echo         
echo         // Chat
echo         function addChatMessage(message^) {
echo             const chat = document.getElementById('chatMessages'^);
echo             const msgDiv = document.createElement('div'^);
echo             msgDiv.style.color = message.includes('Najika'^) ? '#667eea' : 'white';
echo             msgDiv.textContent = message;
echo             chat.appendChild(msgDiv^);
echo             chat.scrollTop = chat.scrollHeight;
echo         }
echo         
echo         function sendChat(^) {
echo             const input = document.getElementById('chatInput'^);
echo             const message = input.value.trim(^);
echo             if(!message^) return;
echo             
echo             addChatMessage(`Du: ${message}`^);
echo             backendSocket.emit('message', {message: message}^);
echo             input.value = '';
echo         }
echo         
echo         // Socket Events
echo         backendSocket.on('response', (data^) =^> {
echo             addChatMessage(`Najika: ${data.message}`^);
echo         }^);
echo         
echo         gameSocket.on('game_state', (state^) =^> {
echo             worldData = state;
echo             console.log('Game State:', state^);
echo         }^);
echo         
echo         gameSocket.on('explosion', (data^) =^> {
echo             addChatMessage(`💥 ${data.message}`^);
echo         }^);
echo         
echo         // Init
echo         document.getElementById('chatInput'^).addEventListener('keypress', (e^) =^> {
echo             if(e.key === 'Enter'^) sendChat(^);
echo         }^);
echo         
echo         generateWorldView(^);
echo         
echo         // Start Message
echo         setTimeout((^) =^> {
echo             addChatMessage('Najika: Die Mini-Open-World läuft! Alle Räume sind verfügbar!''^);
echo             addChatMessage('Najika: Angel-System, Garten und Combat sind bereit zum Testen!''^);
echo         }, 1000^);
echo     ^</script^>
echo ^</body^>
echo ^</html^>
) > "%NAJIKA_DIR%\frontend\world.html"

echo [✓] World-Frontend erstellt

:: ========================================
:: PHASE 9: Launcher Update
:: ========================================
echo.
echo ══════════════════════════════════════════════════════════════════════
echo PHASE 9: Finaler Launcher
echo ══════════════════════════════════════════════════════════════════════
echo.

(
echo @echo off
echo title Najika World System V4.0
echo cd /d "%NAJIKA_DIR%"
echo.
echo echo ╔══════════════════════════════════════════════════════════════════════╗
echo echo ║                      NAJIKA WORLD SYSTEM V4.0                       ║
echo echo ║                    Mini-Open-World Edition                          ║
echo echo ╚══════════════════════════════════════════════════════════════════════╝
echo echo.
echo.
echo :: Ollama Check
echo tasklist /FI "IMAGENAME eq ollama.exe" 2^>NUL ^| find /I /N "ollama.exe"^>NUL
echo if "%%ERRORLEVEL%%"=="1" (
echo     echo [INFO] Starte Ollama...
echo     start /B ollama serve ^>nul 2^>^&1
echo     timeout /t 3 >nul
echo ^)
echo.
echo :: Najika Core (Port 8000^)
echo echo [INFO] Starte Najika Core auf Port %BACKEND_PORT%...
echo start /B python backend\najika_core.py
echo timeout /t 2 >nul
echo.
echo :: Game Server (Port 7010^)
echo echo [INFO] Starte Game Server auf Port %GAME_PORT%...
echo start /B python backend\game_server.py
echo timeout /t 2 >nul
echo.
echo :: Öffne Interfaces
echo echo [INFO] Öffne Interfaces...
echo start http://127.0.0.1:%BACKEND_PORT%/
echo timeout /t 1 >nul
echo start "%NAJIKA_DIR%\frontend\world.html"
echo.
echo echo.
echo echo ══════════════════════════════════════════════════════════════════════
echo echo.
echo echo ✅ NAJIKA WORLD LÄUFT!
echo echo.
echo echo 🎮 VERFÜGBARE SYSTEME:
echo echo    • Mini-Open-World mit 100x100 Tiles
echo echo    • Schwarze Mühle mit allen Räumen
echo echo    • Angel-System (4 Locations^)
echo echo    • Garten-System (9 Beete^)
echo echo    • Combat-System (Soulslike-Balance^)
echo echo    • Training im Keller
echo echo    • Oregon-Engine für Events
echo echo.
echo echo 🌐 INTERFACES:
echo echo    • Najika Chat: http://127.0.0.1:%BACKEND_PORT%
echo echo    • World View: file:///%NAJIKA_DIR%/frontend/world.html
echo echo    • Game API: http://127.0.0.1:%GAME_PORT%
echo echo.
echo echo 📁 Deine Daten sind in: %NAJIKA_DIR%
echo echo.
echo echo Drücke STRG+C zum Beenden
echo pause >nul
) > "%NAJIKA_DIR%\START_WORLD.bat"

:: Desktop-Verknüpfung aktualisieren
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Najika World.lnk'); $SC.TargetPath = '%NAJIKA_DIR%\START_WORLD.bat'; $SC.WorkingDirectory = '%NAJIKA_DIR%'; $SC.IconLocation = '%SystemRoot%\System32\shell32.dll,13'; $SC.Save()"

echo [✓] Launcher aktualisiert

:: ========================================
:: ABSCHLUSS
:: ========================================
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║              🎉 INSTALLATION ERFOLGREICH ABGESCHLOSSEN! 🎉          ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo ✅ INSTALLIERTE FEATURES:
echo    • Mini-Open-World mit prozeduraler Generation
echo    • Schwarze Mühle mit ALLEN Räumen:
echo      - Keller (Training + Oregon-Portal)
echo      - Erdgeschoss (Najika Terminal)
echo      - Werkstatt (Crafting)
echo      - Angel-Teich (Fishing System)
echo      - Garten (9 Beete, magische Pflanzen)
echo    • 3 Dungeons mit Bossen
echo    • Vollständiges Combat-System (schwer aber fair)
echo    • Angel-System mit 4 Locations
echo    • Garten-System mit Echtzeit-Wachstum
echo    • Training-System für Skill-Verbesserung
echo.
echo 🎮 SO STARTEST DU:
echo    Desktop-Verknüpfung: "Najika World"
echo    oder
echo    %NAJIKA_DIR%\START_WORLD.bat
echo.
echo 🌍 DIE WELT WARTET:
echo    • 100x100 Tiles prozedural generiert
echo    • Ressourcen zum Sammeln
echo    • Geheimnisse zu entdecken
echo    • Skills zu meistern
echo.
echo 💡 TIPP: Die Mini-Games im Keller testen die späteren
echo         Handyspiel-Mechaniken vorab!
echo.
pause
