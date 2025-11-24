# 🎮 NAJIKA WORLD - Game Versionen

**Stand:** 2025-11-24
**Aktuell genutzt:** `najika_world_UNIFIED.html`

---

## 📁 VERFÜGBARE VERSIONEN

### ✅ **najika_world_UNIFIED.html** (HAUPTVERSION - 166 KB)
**Status:** ✅ Produktiv, stabil, vollständig
**Phase:** Phase 1 (Flat Map) + Phase 2 Module verfügbar
**Features:**
- ✅ Open World Map (9.6km × 9.6km)
- ✅ 9 Regionen (3×3 Grid)
- ✅ 8 Städte + Götterfels
- ✅ Schwarze Mühle (12 Räume via index.html)
- ✅ Combat System (MANUAL/ASSIST/AUTO)
- ✅ DataLoader (40 JSON-Dateien)
- ✅ NPCs, Items, Quests, Enemies
- ⚠️ Flat Terrain (Phase 2 Module vorhanden aber nicht aktiv!)

**Start:**
```bash
START_NAJIKA_GAME.bat   # Nur Game
START_NAJIKA_FULL.bat   # Game + Backend
```

**Browser:**
```
http://localhost:5173/najika_world_UNIFIED.html
```

---

### 🚧 **najika_world_PHASE2_WIP.html** (Work In Progress - 21 KB)
**Status:** 🚧 Unvollständig, experimentell
**Phase:** Phase 2 (Terrain Variation)
**Features:**
- ✅ World Manager System integriert
- ✅ Terrain Generator (Perlin Noise)
- ✅ Biome System (Fog, Lighting)
- ✅ Vegetation System (Bäume, Gras)
- ✅ Region Streaming
- ✅ LOD Manager
- ❌ DataLoader fehlt
- ❌ Combat System fehlt
- ❌ Schwarze Mühle fehlt
- ❌ UI unvollständig

**Nicht empfohlen für Produktiv-Nutzung!**

---

### 📦 **Alte Versionen (Backup)**

#### najika_world_PHASE1_TEST.html (165 KB)
- 9 Regionen Test-Version
- Flat Build Mode
- Backup von alter Version

#### najika_world_OLD_v1.html (22 KB)
- Alte Version 1
- Nicht mehr genutzt

#### najika_world_OLD_v3.html (23 KB)
- Alte Version (war "FINAL")
- Nicht mehr genutzt

#### najika_world_OLD_v4.html (27 KB)
- Alte Version (war "complete")
- Nicht mehr genutzt

---

## 🌍 PHASE 1 vs PHASE 2 - Was ist der Unterschied?

### Phase 1 (Aktuell in UNIFIED)
```
✅ Flat Map (alle Regionen auf gleicher Höhe)
✅ Einfache Geometrie (Boxen, Kugeln)
✅ Schnelle Performance
✅ Alle Game-Features funktionieren
✅ Stabil und getestet
```

### Phase 2 (Vorbereitet, nicht aktiv)
```
🏔️ Terrain Variation (Berge, Täler, Dünen)
🌳 Vegetation System (Bäume, Gras instanced)
🏙️ Dynamische Städte (echte Buildings)
🌫️ Biome-Effekte (Nebel, Lighting)
📦 Region Streaming (Performance)
🎨 LOD System (3 Detail-Stufen)

⚠️ Module sind vorhanden in js/world/
⚠️ Aber nicht in UNIFIED integriert!
```

---

## 🛠️ MODULE ÜBERSICHT

### Aktuell geladene Module (UNIFIED.html):
```javascript
// Game-Core
static/js/camera_controller.js
static/js/interior_generator.js

// Systeme
static/js/food_system.js
static/js/inventory_system.js
static/js/npc_system.js
static/js/quest_system.js
static/js/skill_system.js
static/js/crafting_system.js
static/js/special_features.js
static/js/special_locations.js

// Performance & UI
static/js/performance_monitor.js
static/js/save_system.js
static/js/sound_system.js
static/js/tutorial_system.js

// Combat
static/js/realtime_combat.js

// Data
static/js/game_data_loader.js
```

### Verfügbare Phase 2 Module (js/world/):
```javascript
// Phase 2 System (nicht aktiv!)
js/world/world_manager.js        // Hauptorchestrator
js/world/terrain_generator.js    // Perlin Noise Terrain
js/world/biome_system.js          // Fog, Lighting
js/world/vegetation_system.js     // Bäume, Gras
js/world/city_builder.js          // Stadt-Konstruktion
js/world/region_streaming.js      // Performance Streaming
js/world/lod_manager.js           // Level of Detail
js/world/asset_loader.js          // Asset Management
js/world/asset_discovery.js       // Asset Discovery
```

---

## 🚀 PHASE 2 AKTIVIEREN

### Option 1: In UNIFIED.html integrieren (Empfohlen)
```javascript
// Am Anfang von <script> hinzufügen:
import WorldManager from 'js/world/world_manager.js';

// Nach Scene-Setup:
const worldManager = new WorldManager(scene, camera);
await worldManager.initialize({
  dataPath: '/data/',
  enableLOD: true,
  enableStreaming: true
});

// In Animation-Loop:
worldManager.update(deltaTime);
worldManager.setPlayerPosition(camera.position);
```

### Option 2: PHASE2_WIP.html fertigstellen
- Alle Features aus UNIFIED kopieren
- DataLoader hinzufügen
- Combat System hinzufügen
- UI vervollständigen

---

## 📊 DATEN-STRUKTUR

### digivice/data/ (40 JSON-Dateien)
```
Meta-Daten:
├── regions.json           # 9 Regionen
├── cities.json            # Städte
├── biomes.json            # Biome
└── asset_mapping_v2_REAL.json  # Assets

Game-Content (9× für Städte):
├── npcs_*.json            # NPCs pro Stadt
├── items_*.json           # Items pro Stadt
├── quests_*.json          # Quests pro Stadt
└── enemies_*.json         # Enemies pro Region
```

---

## 🎯 CONTROLS

### Movement:
- **WASD** - Bewegung (6-9 m/s)
- **Shift** - Sprint
- **E** - Interact (Mühle/Städte betreten)

### Combat:
- **Tab** - Combat Mode umschalten (MANUAL/ASSIST/AUTO)
- **Q** - Attack 1
- **E** - Attack 2
- **Space** - Attack 3
- **C** - Attack 4
- **X** - Attack 5
- **V** - Attack 6

### Dev-Mode (wenn aktiviert):
- **F1** - Stats anzeigen
- **F2** - FPS Counter
- **F3** - Performance Monitor

---

## 🐛 BEKANNTE PROBLEME

### UNIFIED.html (Phase 1):
- ✅ Alle kritischen Bugs gefixt!
- ✅ Skalierung korrekt (9.6km)
- ✅ Character Size korrekt (1.35m)
- ✅ Movement Speed korrekt (6-9 m/s)
- ✅ Schwarze Mühle sichtbar und betretbar
- ✅ Alle Städte an richtigen Positionen
- ✅ DataLoader funktioniert

### PHASE2_WIP.html:
- ❌ Unvollständig (viele Features fehlen)
- ⚠️ Nur für Tests!

---

## 📖 WEITERE DOKUMENTATION

- `../entwicklung/INTEGRATION_GUIDE.md` - Wie Phase 2 integrieren
- `../entwicklung/INTEGRATION_EXAMPLE.js` - Code-Beispiel
- `../entwicklung/TECHNICAL_IMPLEMENTATION.md` - Tech Details
- `../VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md` - Gesamt-Übersicht
- `../PROBLEME_GEFUNDEN.md` - Gefundene Bugs

---

## 🎮 EMPFEHLUNG

**Für Spielen:**
- ✅ Nutze `najika_world_UNIFIED.html`
- ✅ Starte mit `START_NAJIKA_GAME.bat` oder `START_NAJIKA_FULL.bat`

**Für Entwicklung (Phase 2):**
- ⚠️ Siehe `../entwicklung/INTEGRATION_GUIDE.md`
- ⚠️ Module sind vorbereitet in `js/world/`
- ⚠️ Integration in UNIFIED empfohlen

---

**Version:** 1.0.0
**Last Update:** 2025-11-24
**Status:** Phase 1 Stable, Phase 2 Ready to Integrate
