# 🎮 NAJIKA WORLD - STATUS & ÜBERSICHT
**Stand:** 25. November 2025
**Version:** Game Content Integration (9.6km Open World + Schwarze Mühle)

---

## 📊 AKTUELLER STATUS

### ✅ FERTIG & FUNKTIONIERT

#### 🗺️ **Open World System (9.6km x 9.6km)**
- **Map-Größe:** 9600 x 9600 units = 9.6km x 9.6km
- **Vergleich:** ~3x größer als Fortnite Battle Royale (92.16 km² vs 30 km²)
- **9 Regionen** in 3x3 Grid, je 3200m x 3200m:
  - Ice (Nordwest: -3200, 3200)
  - Highland (Nord: 0, 3200)
  - Desert (Nordost: 3200, 3200)
  - Swamp (West: -3200, 0)
  - Mountain/Götterfels (Zentrum: 0, 0) ⭐ **Schwarze Mühle hier**
  - Coast (Ost: 3200, 0)
  - Caves (Südwest: -3200, -3200)
  - Forest (Süd: 0, -3200)
  - Volcano (Südost: 3200, -3200)
- **Movement Bounds:** ±4800 (korrekt!)
- **Minimap:** Korrekt skaliert für 9.6km
- **Region Marker:** Alle 9 sichtbar mit Labels

#### 🏰 **Schwarze Mühle (4 Etagen)**
- **Erdgeschoss:** Wohnzimmer, Küche, Badezimmer
- **Obergeschoss:** Schlafzimmer
- **Turm:** Terminal (für Digivice-Module)
- **Keller:** Studieren & Crafting
- **Möbel/Geräte (Placeholder):**
  - Küche: Herd (rot), Kühlschrank (weiß)
  - Bad: Dusche (blau)
  - Wohnzimmer: Sofa (grün)
- **Raum-Features:**
  - Boden, 4 Wände, Decke
  - Dunkler Fog/Background im Interior
  - Bewegung innerhalb des Raums möglich

#### 🎮 **Steuerung & UI**
- **E-Taste:** Gebäude betreten (nur in Nähe, 150m Radius)
- **Q-Taste:** Gebäude verlassen (funktioniert überall im Interior)
- **E-Prompt:** Zeigt "Schwarze Windmühle betreten" nur draußen
- **Q-Prompt:** Roter Button "Gebäude verlassen" nur drinnen
- **Stockwerk-Wechsel UI:** Funktioniert in der Mühle
- **WASD:** Bewegung (6-9 m/s)
- **Shift:** Sprint
- **Tab:** Combat Mode Toggle

#### 🚀 **Teleport-System**
- **Teleport-Buttons für alle 9 Regionen** (Ice, Highland, Desert, etc.)
- **Mühlen-Teleport Button:** 🏠 Schwarze Mühle (lila)
  - Teleportiert DIREKT ins Interior (wie Soulframe!)
  - Funktioniert von überall
- Verlässt automatisch Interior beim Teleport zu Regionen

#### ⚔️ **Combat System (REALTIME - 1200+ Zeilen Code!)**
- **3 Kampf-Modi:**
  - **MANUAL:** Volle Kontrolle (Skyrim + Soulframe + Dark Souls Movement)
    - **Dual-Wielding:** Jede Hand einzeln steuerbar (Q/E)
    - **6 Angriffsarten:** Leicht/Schwer pro Hand + Beide Hände
    - **Element-Weaves:** Q+E gleichzeitig = 7 Elementar-Kombos
    - **Combo-Chain:** Schnelle Angriffe = +10% Damage pro Hit
    - **Defense:** Dodge/Roll (C), Block (X), Parry (V - Timing!)
    - **WICHTIG:** Angriffe sind aufeinanderfolgend, NICHT simultan!
    - **NUR** Element-Weave erlaubt simultane Dual-Attacks!
  - **ASSIST:** Najika kämpft, Spieler feuert an (Digimon World Style)
    - "Los!" (+10% DMG, 3s)
    - "Defend!" (+20% DEF, 3s)
    - "Combo!" (Special)
    - "Finisher!" (Ultimate bei Cheer=100)
  - **AUTO:** Najika kämpft alleine, Spieler kann anfeuern
- **Enemy System:**
  - Enemy Spawning in allen 9 Regionen (3-5 pro Region)
  - 14 Enemy-Typen mit KayKit Models
  - Aggro-System (15m Radius)
  - AI Movement & Counter-Attacks
- **Food System Integration:**
  - Buffs (Damage, Crit, Stamina Regen)
  - Champion-Keule (legendäres Food Item!)
- **Backend Integration:**
  - Battle API (Port 8000)
  - Offline-Fallback vorhanden
- **Visual Feedback:**
  - Floating Damage Numbers
  - Enemy Emissive Glow (Aggro)
  - Combo Counter Display

#### 🎨 **Visuelle Features**
- Phase 1 (Flat Terrain) - AKTIV
- Phase 2 (Terrain Variation) - verfügbar, nicht aktiv
- Region-spezifische Farben
- Grid Helper (9600x9600, toggle mit Button)
- Lighting System (Sun, Ambient, Hemisphere)
- Fog System (draußen hell, drinnen dunkel)

#### 🔧 **Backend Integration**
- Server läuft auf Port 8000
- Najika Status API verfügbar
- TTS System (Megumin Voice Clone) aktiviert
- Backend Status wird angezeigt (grün/rot Dot)

#### 🏟️ **Arena & PvP System (GEPLANT)**
- **Handelsfestung Arena** (Heisse Dünen Region)
  - Position: (8400, 8300)
  - Kapazität: 100 Zuschauer
  - **3 PvP-Modi:**
    1. **Hardcore-PvP:** Permadeath oder "Alles-abgeben-um-zu-leben" Mercy-System
    2. **Normal-PvP:** Gewinner erhält 1 Ausrüstungsteil
    3. **Softy-PvP:** Nur Ranking, keine Item-Verluste
- **Arena-Happen:** Legendäres Burger-Item (im Inventory System bereits referenziert)
- **Champion-Keule:** Legendäres Fleisch-Item (two-handed eating!)

#### 🎣 **Fishing System (IMPLEMENTIERT)**
- **2 Angelplätze:** Kristallteich, Weltensee
- **Zelda + Stardew Valley Style**
- **Timing-basiert:** Perfect/Good/Ok/Bad Windows
- **Fische:** 9 Arten (Forelle → Legendärer Najika-Fisch)
- **Minigame:** Cast Power, Reel Timing, Fish Stamina
- **Inventory:** Fische sammeln, verkaufen

#### 🌱 **Garden System (IMPLEMENTIERT)**
- **9 Beete** (3x3 Grid)
- **Stardew Valley + Harvest Moon Style**
- **5 Pflanzen:** Karotte, Tomate, Weizen, Heilkraut, Magische Blume
- **5 Wachstumsstufen** pro Pflanze
- **Gießen-System:** Watering Can (10 Kapazität)
- **Uses:** Kochen, Verkaufen, Heilen, Crafting, Magie
- **Saatgut-Shop:** 5 Samen-Typen

#### 🔨 **Crafting System (IMPLEMENTIERT)**
- **Legendary Weapons:** Fire Blade, Dark Blade, Light Staff
- **Rezepte:** Materials + Gold Requirements
- **Integration:** Schmied-NPCs (Funken-Siedlung)

---

### ⚠️ PROBLEME & FIXES NOTWENDIG

#### 🐛 **Kritische Bugs**
1. **Terminal Button öffnet falsche Seite**
   - Aktuell: `window.open('http://localhost:5173/index.html')`
   - Problem: Öffnet falschen Port/Datei
   - Fix needed: Muss Digivice-Module im Terminal-Raum öffnen

2. **Inventory System Error**
   - `this.items.push is not a function`
   - Zeile: `inventory_system.js:243`
   - Items nicht gefunden: baozi, arena_happen, salted_fish, champion_keule

3. **CORS Error**
   - Port 5000 nicht erreichbar
   - Nicht kritisch (Fallback zu Port 8000 funktioniert)

#### 🔨 **Fehlende Features**
1. **Terminal-Raum Funktionalität**
   - Im Turm (Floor 2) müssen Digivice-Module verfügbar sein:
     - Chat UI (Najika AI)
     - Code Editor
     - File Manager
     - System Monitor
     - Terminal
     - Secure Messenger
   - Aktuell: Nur leerer Raum mit Wänden

2. **Interaktions-System für Möbel**
   - Möbel sind vorhanden aber nicht interaktiv
   - F-Taste System fehlt
   - Benötigt:
     - Proximity Detection für Objekte
     - F-Taste Handler
     - Aktionen: Kochen, Essen, Duschen, Sitzen

3. **Füttern/Trinken UI Buttons**
   - Im alten System vorhanden
   - Fehlen im neuen System
   - Sollten im Food System integriert sein

#### 📦 **Fehlende Assets**
- Barrel, Floor Tile 1/2, Gravestone 2, Lava Rock
- Nicht kritisch, aber loggt Fehler

#### 🎨 **Visuelle Verbesserungen Notwendig**
1. **Möbel sind Placeholder-Würfel**
   - Sollten durch richtige GLTF Modelle ersetzt werden
   - KayKit Assets verfügbar in `/static/assets/`

2. **Region Marker zu groß**
   - Positions sind noch von alter Map (±200 statt ±4800)
   - Siehe Zeile 1737-1748 in index.html

3. **City Buildings nicht platziert**
   - 5 Städte definiert in `cityLocations` (Zeile 2048-2138)
   - 3 Special Locations definiert
   - Werden geladen aber Positionen müssen überprüft werden

---

## 📁 WICHTIGE DATEIEN

### Frontend (Haupt-Game)
- **`C:\Najika_World\digivice\index.html`** - UNIFIED System (Port 8000)
  - 4500+ Zeilen
  - Enthält komplettes Game System inline
  - Phase 1 (Flat) & Phase 2 (Terrain) Toggle

### JavaScript Module (wichtigste)
- **`js/3d_scene.js`** - 3D Scene Management (DEAKTIVIERT für UNIFIED!)
  - `bootWhenReady()` auskommentiert (Zeile 2577)
  - Exports: Building Interior Funktionen für UNIFIED

- **`static/js/realtime_combat.js`** - ⚔️ **COMBAT SYSTEM (1229 Zeilen!)**
  - 3 Kampf-Modi (MANUAL/ASSIST/AUTO)
  - Dual-Wielding System (Linke/Rechte Hand separat)
  - Element-Weaves (7 Combos: Fire+Ice, Lightning+Water, etc.)
  - Defense System (Dodge, Block, Parry)
  - Cheer System (Digimon World Style)
  - Enemy Spawning für alle 9 Regionen (14 Enemy-Typen)
  - Food Buff Integration
  - Backend Battle API Integration
  - Visual Feedback (Damage Numbers, Emissive Glow)

- **`js/world/world_manager.js`** - Phase 2 World System
  - Terrain, Biome, Vegetation, LOD
  - Noch nicht integriert

- **`static/js/npc_system.js`** - NPC System
  - FIX ANGEWANDT: CapsuleGeometry → CylinderGeometry (r128 kompatibel)

- **`static/js/inventory_system.js`** - Inventory (HAT BUGS!)
  - Zeile 243: `this.items.push` Error

- **`static/js/food_system.js`** - Food & Buff System
  - Champion-Keule, Baozi, Arena-Happen, Salzfisch
  - Buff-System (Damage, Crit, Stamina Regen)
  - Hunger/Satiety System

- **`static/js/crafting_system.js`** - Crafting System
  - Legendary Weapons (Fire Blade, Dark Blade, Light Staff)
  - Material-Anforderungen
  - Gold-Requirements
  - Integration mit Schmied-NPCs

- **`static/js/quest_system.js`** - Quest System
  - 4 Quest-Typen (Kill, Collect, Talk, Explore)
  - Quest-Tracking UI
  - Progress-Tracking
  - Rewards (Gold, Items, XP)

- **`static/js/skill_system.js`** - Skill System (Use-Based Progression)
- **`static/js/save_system.js`** - Save/Load System
- **`static/js/camera_controller.js`** - Kamera (Orbit/Third/First Person)
- **`static/js/sound_system.js`** - Sound & Music System
- **`static/js/special_features.js`** - Special Features
- **`static/js/tutorial_system.js`** - Tutorial System
- **`static/js/world_mode_manager.js`** - World Mode Manager

- **`js/fishing.js`** - 🎣 Fishing System (Zelda + Stardew Valley)
  - 2 Angelplätze, 9 Fisch-Arten
  - Timing-basiertes Minigame

- **`js/garden.js`** - 🌱 Garden System (Stardew Valley + Harvest Moon)
  - 9 Beete (3x3 Grid), 5 Pflanzen
  - Gießen-System, Wachstumsstufen

- **`js/minigames.js`** - Minigames System
- **`js/oregon.js`** - Oregon Trail Events (NICHT implementiert!)
- **`js/dungeon_generator.js`** - Dungeon Generator
- **`js/dungeon_combat.js`** - Dungeon Combat
- **`js/dungeon_enemies.js`** - Dungeon Enemies
- **`js/battle_core.js`** - Battle Core System
- **`js/battle_api.js`** - Battle API

- **`js/terminal_modules.js`** - 🖥️ **Terminal Module System**
  - Code-Editor, Secure Messenger, System Monitor, File Manager
  - Swipe Gestures, Keyboard Shortcuts (1-4)

- **`js/chat_ui.js`** - Chat UI (Najika AI)
- **`js/code_editor.js`** - Code-Editor Modul
- **`js/file_manager.js`** - File-Manager Modul
- **`js/secure_messenger.js`** - Secure Messenger (E2E encrypted)
- **`js/system_monitor.js`** - System Monitor
- **`js/voice_call.js`** - Voice Call System
- **`js/private_mode.js`** - Private Mode
- **`js/safe_functions.js`** - Safe Functions
- **`js/command_system.js`** - Command System
- **`js/touch_controls.js`** - Touch Controls (Mobile)
- **`js/character_animations.js`** - Character Animations
- **`js/room_connector.js`** - Room Connector (12 Räume)

### Data Files
- **`data/regions.json`** - 9 Regionen Definition
- **`data/biomes.json`** - Biome-Daten
- **`data/cities.json`** - **5 Städte + 3 Special Locations**
  - **Handelsfestung** (Heisse Dünen) - **PvP Arena hier!**
    - 10 Trading Posts, 15 Player Shops (Fallout 76 Style)
    - Arena: 3 PvP-Modi (Hardcore/Normal/Softy)
    - Food: FLEISCH (Arena-Happen Burger, Champion-Keule!)
  - **Dampf-Hain** (Samtmoos Tiefwald) - Onsen & Restaurant
    - Spirited Away Style Steam Kitchen
    - Food: GEDÄMPFTE BRÖTCHEN (Baozi, Manju)
  - **Salzige Bucht** (Salzwind Küste) - Hafen & Fischmarkt
    - Leuchtturm (climbable), 5 Docks, 10 Ships
    - Food: SALZFISCH (getrocknet/frisch)
  - **Runenheim** (Blitzebene) - Magie-Akademie
  - **Funken-Siedlung** (Magmaströme) - Legendary Forge
- **`data/game_content_region_*.json`** - 6 Regionen (NPCs, Items, Quests, Enemies)
- **`static/assets/room_config_detailed.json`** - Raum-Konfiguration (12 Räume)

### Backend
- **`backend/najika_server.py`** - Python Server (Port 8000)
  - Serviert `/digivice/` Ordner
  - TTS System
  - Najika AI API

---

## 🎯 NÄCHSTE SCHRITTE (PRIORISIERT)

### **HIGH PRIORITY (Critical)**
1. ✅ **Debug Logs entfernen** (DONE)
2. ⚠️ **Terminal Button fixen**
   - Entferne oder ändere `openTerminal()` Funktion
3. ⚠️ **Inventory System Bug fixen**
   - Zeile 243 in `inventory_system.js`

### **MEDIUM PRIORITY (Important)**
4. **Terminal-Raum funktional machen**
   - Interaktives System für Digivice-Module
   - Computer/Terminal Objekt im Raum
   - F-Taste öffnet Module

5. **Region Marker Positionen korrigieren**
   - Von ±200 auf ±4800 skalieren
   - Zeile 1737-1748

6. **Cities & Special Locations überprüfen**
   - Positionen auf 9.6km Map anpassen
   - Buildings sichtbar machen

### **LOW PRIORITY (Nice to have)**
7. **Möbel-Interaktionen**
   - F-Taste System
   - Kochen, Essen, Duschen Funktionen

8. **Bessere Möbel Modelle**
   - GLTF statt Würfel

9. **Phase 2 Integration**
   - Terrain Variation System aktivieren
   - Berge, Täler, Vegetation

---

## 🔧 TECHNISCHE DETAILS

### System-Architektur
```
UNIFIED System (index.html Port 8000)
├── Inline 3D Scene (Three.js r128)
├── Phase 1: Flat 9 Regions
├── Phase 2: Terrain System (optional)
├── Building System (Mühle)
│   └── 4 Floors via loadMuehleFloor()
├── Combat System (Realtime)
├── NPC System (Cities)
├── Food/Inventory System
└── Backend Integration (Port 8000)
```

### Wichtige Variablen
- `worldSize = 9600` - Map Größe
- `regionSize = 3200` - Region Größe
- `isInInterior` - Boolean für Interior/Exterior
- `currentMuehleFloor` - Aktuelles Stockwerk (0-3)
- `schwarzeMuehle` - Mühlen-Objekt
- `buildings` - Array aller Gebäude

### Key Functions
- `loadMuehleInterior()` - Lade Mühle Interior
- `unloadBuildingInterior()` - Verlasse Interior
- `teleportToMuehle()` - Teleport zur Mühle
- `teleportTo(region)` - Teleport zu Region
- `checkBuildingProximity()` - E-Taste Proximity

---

## 🚨 BEKANNTE EINSCHRÄNKUNGEN

1. **Three.js r128 Limitierung**
   - CapsuleGeometry nicht verfügbar (≥r147 benötigt)
   - Workaround: CylinderGeometry

2. **Performance**
   - 9.6km Map kann laggy sein ohne LOD
   - Phase 2 LOD System noch nicht aktiv

3. **Asset Loading**
   - Einige KayKit Assets fehlen
   - Error Logs nicht kritisch

4. **Browser Kompatibilität**
   - Getestet: Firefox
   - Chrome/Edge sollten funktionieren
   - Mobile: Noch nicht optimiert

---

## 📚 DOKUMENTATION

### Für neue KI Modelle wichtig:
1. **`VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md`** - Komplette Projektstruktur
2. **`CLAUDE_CODE_WEB_LEITFADEN.md`** - 10 Gebote für Web-Entwicklung
3. **`WEB_MODEL_BUGFIX_REPORT.md`** - 8 Fehler vom vorherigen Modell
4. **Dieser File** (`STATUS_NAJIKA_WORLD_GAME.md`) - Aktueller Status

### Hilfreiche Commits
- `8fc208a` - Phase 2 ist PFLICHT Warnung
- `a8ee198` - Map-Rebuild-Auftrag
- `0d0b5bf` - dataPath korrigiert
- `302efd1` - Game Content für 6 Regionen
- `6389b82` - Game Content für 3 Regionen

---

## 🎮 VERWENDUNG

### Starten
```bash
# Backend starten (Port 8000)
cd C:\Najika_World\backend
python najika_server.py

# Oder mit BAT-File
START_NAJIKA_WORLD.bat
```

### URL
```
http://localhost:8000/digivice/
```

### Steuerung
- **WASD** - Bewegung
- **Shift** - Sprint
- **E** - Gebäude betreten (nur in Nähe)
- **Q** - Gebäude verlassen (überall im Interior)
- **Tab** - Combat Mode wechseln
- **F6** - Camera Mode wechseln
- **Maus** - Kamera drehen

### Teleport-Buttons (oben rechts)
- 🏠 Schwarze Mühle - Direkt ins Interior
- ❄️ Ice, ⛰️ Highland, 🏜️ Desert, etc. - Zu Regionen

---

## 🔄 LETZTE ÄNDERUNGEN (Heute)

### Session Zusammenfassung
1. ✅ Schwarze Mühle Rebuild-Loop gefixt
2. ✅ Map-Größe auf 9.6km korrigiert
3. ✅ Minimap-Skalierung gefixt
4. ✅ Movement Bounds gefixt (±4800)
5. ✅ E-Prompt nur draußen
6. ✅ Q-Prompt für Verlassen hinzugefügt
7. ✅ Region Marker ausblenden im Interior
8. ✅ Teleport-System implementiert
9. ✅ Decke in Räumen hinzugefügt
10. ✅ Möbel-Placeholder erstellt
11. ✅ NPC System r128 kompatibel gemacht
12. ✅ Debug Logs entfernt

### Geänderte Dateien
- `digivice/index.html` (Haupt-File, viele Änderungen)
- `digivice/js/3d_scene.js` (bootWhenReady deaktiviert)
- `digivice/static/js/npc_system.js` (CapsuleGeometry Fix)

---

**Ende der Übersicht** 🎮
