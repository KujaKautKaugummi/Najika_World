# 📚 PFLICHTLEKTÜRE FÜR ONLINE-MODELL

**Zweck:** Diese Dokumente geben dem Online-Modell den kompletten Kontext über Najika World.

**Stand:** 26. November 2025 (Nach Phase 2 Aktivierung)

---

## 🔴 KRITISCH - ZUERST LESEN! (10 Minuten)

### 1. Projekt-Status & Übersicht
```
/STATUS_NAJIKA_WORLD_GAME.md
```
**Warum:** Aktuellster Status von ALLEM. Zeigt was funktioniert, was kaputt ist, was fehlt.

**Enthält:**
- ✅ Fertige Features (Open World, Combat, Schwarze Mühle, etc.)
- ⚠️ Bekannte Bugs (mit Fixes vom 26. Nov 2025)
- 📋 Nächste Schritte
- 📁 Wichtige Dateien & Zeilen-Nummern

**Lesezeit:** 5 Minuten

---

### 2. Vollständige Projekt-Struktur
```
/VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md
```
**Warum:** Zeigt die komplette Architektur, alle Systeme, alle Dateien.

**Enthält:**
- Ordnerstruktur (Frontend/Backend/Data)
- Alle Game-Systeme (Combat, Inventory, Food, etc.)
- Phase 1 vs Phase 2 Unterschiede
- Integration-Details

**Lesezeit:** 5 Minuten

---

## 🟡 WICHTIG - REGELN & CONTEXT (10 Minuten)

### 3. Entwicklungs-Regeln
```
/CLAUDE_CODE_WEB_LEITFADEN.md
```
**Warum:** Die "10 Gebote" für saubere Entwicklung in diesem Projekt.

**Enthält:**
- Nie Dateien ohne Lesen ändern
- Keine Duplikate erstellen
- Versionierung beachten (Three.js r128!)
- Port-Nummern (8000 nicht 5173!)

**Lesezeit:** 3 Minuten

---

### 4. Fehler-Report vom vorherigen Modell
```
/WEB_MODEL_BUGFIX_REPORT.md
```
**Warum:** Vermeide die 8 häufigsten Fehler, die das letzte Modell gemacht hat!

**Enthält:**
- 8 konkrete Fehler mit Lösungen
- Was NICHT zu tun ist
- Best Practices

**Lesezeit:** 3 Minuten

---

### 5. Aktueller Auftrag (falls relevant)
```
/WEB_MODEL_2_MAP_REBUILD_AUFTRAG.md
```
**Warum:** Zeigt den ursprünglichen Plan für Phase 2.

**Enthält:**
- Phase 1 vs Phase 2 Specs
- Map-Größe (9.6km x 9.6km)
- Region-Layout (3x3 Grid)
- Erfolgs-Kriterien

**Lesezeit:** 4 Minuten

---

## 🟢 OPTIONAL - BEI BEDARF (15-30 Minuten)

### 6. Datei-Liste für neue KI
```
/WICHTIGE_DATEIEN_FÜR_NEUE_KI.md
```
**Warum:** Quick-Reference welche Datei bei welchem Problem.

**Enthält:**
- Schnellsuche (Keyword → Datei)
- Lesereihenfolge-Empfehlung
- Problem → Solution Mapping

**Lesezeit:** 3 Minuten

---

### 7. Game Systems Übersicht
```
/GAME_SYSTEMS_COMPLETE_OVERVIEW.md
```
**Warum:** Detaillierte Beschreibung aller Game-Systeme.

**Enthält:**
- Combat System (1200+ Zeilen!)
- Inventory System
- Food System
- Fishing, Garden, Crafting
- Quest System

**Lesezeit:** 10 Minuten

---

### 8. Entwicklungs-Ordner Details
```
/ENTWICKLUNG_ORDNER_COMPLETE.md
```
**Warum:** Übersicht über den /entwicklung/ Ordner (Phase 2 Code).

**Enthält:**
- Phase 2 Module (8 Dateien)
- Terrain Generator
- Biome System
- Vegetation System
- World Manager

**Lesezeit:** 5 Minuten

---

## 🔵 CODE - NUR BEI SPEZIFISCHEN AUFGABEN

### 9. Haupt-Game-Datei (GROSS!)
```
/digivice/index.html (4500+ Zeilen!)
/digivice/najika_world_UNIFIED.html (identisch mit index.html)
```
**Warum:** Das komplette Game in einer Datei.

**Wichtig:**
- **USE_PHASE_2 = true** (seit 26. Nov 2025)
- Inline Scene Setup (bootWhenReady DEAKTIVIERT!)
- Region Marker bei Zeile 1813-1825
- Schwarze Mühle Logic ab Zeile 1256

**Lesezeit:** 30+ Minuten (NICHT komplett lesen, nur bei Bedarf!)

---

### 10. JavaScript Module (je nach Aufgabe)

**3D Scene Management:**
```
/digivice/js/3d_scene.js
```
- **WICHTIG:** bootWhenReady() ist auskommentiert (Zeile 2577)!
- Wird von UNIFIED verwendet für Building Interiors

**Combat System:**
```
/digivice/static/js/realtime_combat.js (1229 Zeilen)
```
- 3 Modi: MANUAL/ASSIST/AUTO
- Dual-Wielding, Element-Weaves
- Enemy Spawning

**Inventory System:**
```
/digivice/static/js/inventory_system.js
```
- **FIX vom 26. Nov:** Food-Items hinzugefügt (baozi, arena_happen, salted_fish, champion_keule)

**Phase 2 World System:**
```
/digivice/js/world/world_manager.js
/digivice/js/world/terrain_generator.js
/digivice/js/world/biome_system.js
/digivice/js/world/vegetation_system.js
/digivice/js/world/city_builder.js
/digivice/js/world/region_streaming_v2.js
/digivice/js/world/lod_manager.js
/digivice/js/world/asset_loader.js
```
- Alle 8 Module sind funktional
- Seit 26. Nov 2025 AKTIV (USE_PHASE_2 = true)

---

## 📊 DATEN-DATEIEN (nur bei Content-Arbeit)

### Game Content JSON
```
/digivice/data/regions.json (9 Regionen)
/digivice/data/biomes.json
/digivice/data/cities.json (5 Städte + 3 Special Locations)
/digivice/data/game_content_region_*.json (6 Dateien)
```

### Asset Config
```
/digivice/static/assets/room_config_detailed.json (12 Räume)
```

---

## 🎯 EMPFOHLENE LESEREIHENFOLGE

**Für SCHNELLES Verständnis (20 Minuten):**
1. STATUS_NAJIKA_WORLD_GAME.md (5 min)
2. CLAUDE_CODE_WEB_LEITFADEN.md (3 min)
3. WEB_MODEL_BUGFIX_REPORT.md (3 min)
4. VOLLSTÄNDIGE_PROJEKT_ÜBERSICHT.md (5 min)
5. WICHTIGE_DATEIEN_FÜR_NEUE_KI.md (3 min)

**Für TIEFES Verständnis (60+ Minuten):**
1. Alle oben + GAME_SYSTEMS_COMPLETE_OVERVIEW.md (10 min)
2. WEB_MODEL_2_MAP_REBUILD_AUFTRAG.md (4 min)
3. ENTWICKLUNG_ORDNER_COMPLETE.md (5 min)
4. Relevante Code-Dateien je nach Aufgabe (30+ min)

---

## 🚨 KRITISCHE WARNUNGEN

### NIEMALS ÄNDERN (ohne guten Grund):
- `bootWhenReady()` in 3d_scene.js MUSS auskommentiert bleiben!
- `worldSize = 9600` in index.html
- `regionSize = 3200` in index.html
- Movement Bounds: `±4800`
- Port 8000 für Backend (nicht 5173!)

### VORSICHT BEI:
- Three.js Version ist **r128** (keine neueren Features!)
- NPC System verwendet CylinderGeometry (nicht CapsuleGeometry!)
- Terminal Button zeigt jetzt Alert (nicht window.open!)

### NEUE ÄNDERUNGEN (26. Nov 2025):
1. ✅ Terminal Button gefixt
2. ✅ Inventory System: 4 Food-Items hinzugefügt
3. ✅ Region Marker: Positionen skaliert (±3200)
4. ✅ Phase 2 AKTIVIERT (USE_PHASE_2 = true)

---

## 💡 SCHNELLSUCHE

| Problem | Dokument | Zeile/Section |
|---------|----------|---------------|
| Game lädt nicht | WEB_MODEL_BUGFIX_REPORT.md | Error 1-3 |
| Schwarze Mühle Bug | STATUS_NAJIKA_WORLD_GAME.md | Section "Schwarze Mühle" |
| Map falsche Größe | index.html | Zeile 683, 2423 |
| Combat funktioniert nicht | realtime_combat.js | - |
| NPCs spawnen nicht | npc_system.js | Zeile 45 (CylinderGeometry!) |
| Phase 2 Probleme | ENTWICKLUNG_ORDNER_COMPLETE.md | Phase 2 Section |
| Inventory Error | inventory_system.js | FIX vom 26. Nov |
| Terminal Button | index.html | Zeile 2776-2780 |
| Region Marker | index.html | Zeile 1813-1825 |

---

## 📞 HILFE

**Wenn stuck:**
1. Lies STATUS_NAJIKA_WORLD_GAME.md Section "Probleme & Fixes"
2. Check Browser Console für Errors
3. Lies WEB_MODEL_BUGFIX_REPORT.md - vielleicht gleicher Fehler?
4. Vergleiche mit Backup-Files (*.backup_*)

---

## ✅ CHECKLISTE FÜR ONLINE-MODELL

Bevor du Code änderst:
- [ ] STATUS_NAJIKA_WORLD_GAME.md gelesen?
- [ ] CLAUDE_CODE_WEB_LEITFADEN.md gelesen?
- [ ] WEB_MODEL_BUGFIX_REPORT.md gelesen?
- [ ] Relevante Code-Datei(en) gelesen?
- [ ] Phase 2 ist AKTIV - beachtet?
- [ ] Three.js r128 Limitierungen beachtet?
- [ ] Port 8000 (nicht 5173) beachtet?

---

**Viel Erfolg!** 🚀

_Erstellt von Claude (Sonnet 4.5) am 26. November 2025_
_Nach Phase 2 Aktivierung und 3 kritischen Bugfixes_
