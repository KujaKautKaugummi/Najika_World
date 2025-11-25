# 📁 WICHTIGE DATEIEN FÜR NEUE KI MODELLE

**Zweck:** Diese Liste zeigt dir, welche Dateien du aus dem Repo lesen musst, um das Projekt zu verstehen.

---

## 🔴 PFLICHTLEKTÜRE (ZUERST LESEN!)

### 1. Projekt-Übersicht & Status
```
/STATUS_NAJIKA_WORLD_GAME.md          ⭐ WICHTIGSTE DATEI! Aktueller Status
/VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md    📚 Komplette Projektstruktur
/CLAUDE_CODE_WEB_LEITFADEN.md         📜 10 Gebote für Web-Entwicklung
/WEB_MODEL_BUGFIX_REPORT.md           ⚠️  8 Fehler vom vorherigen Modell
```

**Warum:** Diese 4 Dateien geben dir den kompletten Kontext. Lies sie ALLE bevor du Code änderst!

---

## 🟡 HAUPT-CODE (Frontend)

### HTML (Game Entry Point)
```
/digivice/index.html                   🎮 UNIFIED System - HAUPTDATEI (4500+ Zeilen!)
/digivice/najika_world_UNIFIED.html    📄 Original UNIFIED (Backup/Referenz)
```

**Wichtig:** `index.html` ist das aktuelle Game. `najika_world_UNIFIED.html` ist das Original.

### JavaScript - Core Systems
```
/digivice/js/3d_scene.js              🏗️  3D Scene Manager (bootWhenReady DEAKTIVIERT!)
/digivice/js/buildings_custom.js      🏰 Custom Buildings (Mühle, Arena, etc.)
/digivice/js/kaykit_loader.js         📦 Asset Loader (KayKit Models)
```

**Achtung:** `3d_scene.js` hat `bootWhenReady()` auskommentiert (Zeile 2577)! Das ist WICHTIG.

### JavaScript - Game Systems
```
/digivice/static/js/realtime_combat.js    ⚔️  Combat System (MANUAL/ASSIST/AUTO)
/digivice/static/js/npc_system.js         👤 NPC System (HAT FIX: CylinderGeometry!)
/digivice/static/js/inventory_system.js   🎒 Inventory (⚠️  HAT BUGS!)
/digivice/static/js/food_system.js        🍖 Food/Hunger System
/digivice/static/js/camera_controller.js  📷 Kamera (Orbit/Third/First Person)
```

**Bug-Warnung:** `inventory_system.js` Zeile 243 hat einen `this.items.push` Error!

### JavaScript - World/Phase 2 (nicht aktiv, aber wichtig!)
```
/digivice/js/world/world_manager.js       🌍 World Manager (Phase 2)
/digivice/js/world/terrain_generator.js   ⛰️  Terrain Generation
/digivice/js/world/biome_system.js        🌿 Biome System
/digivice/js/world/vegetation_system.js   🌳 Vegetation
/digivice/js/world/city_builder.js        🏘️  City Builder
/digivice/js/world/region_streaming_v2.js 📡 Region Streaming + LOD
```

**Status:** Phase 2 ist FERTIG aber nicht integriert! Siehe `VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md`.

---

## 🟢 DATA FILES (JSON)

### Game Content
```
/digivice/data/regions.json                    🗺️  9 Regionen Definition
/digivice/data/biomes.json                     🌿 Biome-Daten
/digivice/data/cities.json                     🏘️  5 Städte + 3 Special Locations
/digivice/static/assets/room_config_detailed.json  🏠 12 Räume (Mühle etc.)
```

**Wichtig:** `regions.json` definiert die 9.6km x 9.6km Map!

### Game Content (Full Detail)
```
/digivice/data/game_content_region_*.json      📦 6 Regionen (NPCs, Items, Quests, Enemies)
```
**Info:** Regionen 4-9 haben kompletten Content. Regionen 1-3 auch (andere Dateien).

---

## 🔵 BACKEND

### Python Server
```
/backend/najika_server.py              🐍 Main Server (Port 8000)
/backend/najika_ai_local.py            🤖 Najika AI (Ollama Integration)
```

### Backend-Daten
```
/backend/saves/najika_state.json       💾 Najika State
/backend/*.json                        📊 Training Logs
```

---

## 🟣 STARTER SCRIPTS

```
/START_NAJIKA_WORLD.bat               🚀 Hauptstarter (Port 8000)
/START_NAJIKA_GAME.bat                🎮 Game only (kein Backend)
/START_NAJIKA_PHASE1_FLAT.bat         🌍 Phase 1 (Flat Terrain)
/START_NAJIKA_PHASE2_TERRAIN.bat      ⛰️  Phase 2 (Terrain Variation)
```

**Verwende:** `START_NAJIKA_WORLD.bat` für normales Testen.

---

## 📂 ORDNERSTRUKTUR (Kurzversion)

```
Najika_World/
├── digivice/                    🎮 Frontend (Game)
│   ├── index.html              ⭐ HAUPTDATEI
│   ├── js/                     📜 Game Logic
│   │   ├── 3d_scene.js        🏗️  Scene Manager
│   │   ├── world/             🌍 Phase 2 System
│   │   └── ...
│   ├── static/                 📦 Assets & Systems
│   │   ├── js/                🎮 Game Systems
│   │   └── assets/            🖼️  Models, Textures
│   └── data/                   📊 Game Content (JSON)
├── backend/                     🐍 Python Backend
│   ├── najika_server.py        🚀 Server
│   └── saves/                  💾 Save Files
├── entwicklung/                 🔧 Development (Phase 2)
│   └── world/                  🌍 Phase 2 Code (fertig!)
└── *.md                         📚 Dokumentation
```

---

## 🎯 WELCHE DATEIEN BEI WELCHEM PROBLEM?

### Problem: **Game lädt nicht / schwarzer Screen**
Lies:
- `/digivice/index.html` (inline scene setup)
- `/digivice/js/3d_scene.js` (check `bootWhenReady()` auskommentiert?)
- `/WEB_MODEL_BUGFIX_REPORT.md` (Error 1-3)

### Problem: **Schwarze Mühle funktioniert nicht**
Lies:
- `/digivice/index.html` (Zeile 1256-1520: `loadMuehleInterior()`)
- `/digivice/static/assets/room_config_detailed.json` (Raum-Definitionen)
- `/STATUS_NAJIKA_WORLD_GAME.md` (Section "Schwarze Mühle")

### Problem: **Map ist falsche Größe**
Lies:
- `/digivice/index.html` (Zeile 677: `regionSize`, Zeile 2405: `worldSize`)
- `/digivice/data/regions.json` (Region Positionen)
- `/STATUS_NAJIKA_WORLD_GAME.md` (Section "Open World System")

### Problem: **Combat funktioniert nicht**
Lies:
- `/digivice/static/js/realtime_combat.js`
- `/digivice/index.html` (Zeile 574-636: Combat Mode Toggle)

### Problem: **NPCs spawnen nicht**
Lies:
- `/digivice/static/js/npc_system.js` (⚠️  Line 45: CylinderGeometry Fix!)
- `/digivice/data/game_content_region_*.json` (NPC-Daten)

### Problem: **Phase 2 integrieren**
Lies:
- `/entwicklung/world/*.js` (alle 8 Dateien!)
- `/VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md` (Section "Phase 2")
- `/digivice/js/world/world_manager.js` (Main Orchestrator)

---

## ⚠️ WICHTIGE WARNUNGEN

### 🔴 NIEMALS ÄNDERN (ohne guten Grund):
- `bootWhenReady()` in `3d_scene.js` MUSS auskommentiert bleiben!
- `worldSize = 9600` in index.html
- `regionSize = 3200` in index.html
- Movement Bounds: `±4800`

### 🟡 VORSICHT BEI:
- `inventory_system.js` - HAT BUGS!
- `npc_system.js` - Verwendet jetzt CylinderGeometry (nicht CapsuleGeometry!)
- Three.js r128 - Keine neueren Features nutzen!

### 🟢 SAFE TO CHANGE:
- UI Text/Styling
- Möbel-Positionen in Räumen
- Region Marker Positionen (Zeile 1737-1748)
- Terminal Button Funktion (sollte gefixt werden!)

---

## 📖 LESEREIHENFOLGE FÜR NEUE KI

**Empfohlene Reihenfolge:**

1. **START:** `/STATUS_NAJIKA_WORLD_GAME.md` (10 Minuten)
   - Gibt dir kompletten Überblick was funktioniert und was nicht

2. **KONTEXT:** `/VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md` (15 Minuten)
   - Verstehe die gesamte Projektstruktur

3. **REGELN:** `/CLAUDE_CODE_WEB_LEITFADEN.md` (5 Minuten)
   - 10 Gebote für saubere Entwicklung

4. **FEHLER:** `/WEB_MODEL_BUGFIX_REPORT.md` (5 Minuten)
   - Vermeide die 8 Fehler vom vorherigen Modell

5. **CODE:** `/digivice/index.html` (30+ Minuten)
   - Verstehe das Haupt-Game System

6. **OPTIONAL:** Lies spezifische JS Files je nach Aufgabe

**Geschätzte Zeit:** 1-2 Stunden für komplettes Verständnis

---

## 🔍 SCHNELLSUCHE

**Suche nach Keyword im Code:**

| Keyword | Datei | Zeile ca. | Beschreibung |
|---------|-------|-----------|--------------|
| `loadMuehleInterior` | index.html | 1256 | Mühle laden |
| `teleportToMuehle` | index.html | 2395 | Teleport zur Mühle |
| `worldSize` | index.html | 2405 | Map-Größe |
| `regionSize` | index.html | 677 | Region-Größe |
| `checkBuildingProximity` | index.html | 954 | E-Taste Proximity |
| `bootWhenReady` | 3d_scene.js | 2577 | ⚠️  AUSKOMMENTIERT! |
| `CylinderGeometry` | npc_system.js | 45 | NPC Body (Fix) |

---

## 💡 TIPPS

1. **Nutze die Browser Console** - Viele Debug-Infos werden dort geloggt
2. **Port 8000 ist wichtig** - Backend läuft dort, nicht 5173!
3. **Hard Reload** - Strg+F5 nach Code-Änderungen
4. **Git Branch** - Wir sind auf `claude/game-content-integration-final`
5. **Backup vorhanden** - `index.html.backup_20251125_174031` falls was schief geht

---

## 🆘 HILFE

**Wenn du stuck bist:**
1. Lies `/STATUS_NAJIKA_WORLD_GAME.md` Section "Probleme & Fixes"
2. Check Browser Console für Errors
3. Vergleiche mit `index.html.backup_*` Files
4. Lies `/WEB_MODEL_BUGFIX_REPORT.md` - vielleicht gleicher Fehler?

---

**Viel Erfolg!** 🚀

_Diese Liste wurde erstellt von Claude (Sonnet 4.5) am 25. November 2025_
