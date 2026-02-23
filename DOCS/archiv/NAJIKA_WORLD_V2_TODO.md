# 🌍 NAJIKA WORLD V2 - TODO LISTE

**Stand:** 8. November 2025, 22:45 Uhr
**Status:** Grundsystem funktioniert! Character bewegt sich, Assets laden, World initialisiert.

## ✅ ERLEDIGT (Funktioniert bereits)

### Core-Systeme
- ✅ **World Manager** - 9 Regionen laden (9600x9600 Map)
- ✅ **Asset Discovery** - 71 Assets automatisch gefunden (KayKit, JellySquish)
- ✅ **Character System** - Grüne Kapsel bewegt sich mit WASD
- ✅ **Camera Controller** - Orbit-Modus funktioniert
- ✅ **Region Streaming** - regions.json lädt (200 OK)
- ✅ **Data Loading** - asset_mapping_v2_REAL.json lädt
- ✅ **Terrain Generator** - Boden wird generiert (weiß)
- ✅ **Asset Loader** - Assets werden platziert (braune Steine sichtbar)

### Technische Fixes
- ✅ THREE.js r128 Kompatibilität (CapsuleGeometry durch Group ersetzt)
- ✅ Browser-Exports (window.CameraController)
- ✅ ES6 Module Imports (window.THREE statt 'three')
- ✅ Pfade für Port 8001 Test-Server korrigiert

## 🔧 TODO - MUSS NOCH GEMACHT WERDEN

### 1. Terrain-System verbessern
**Priorität:** HOCH
**Was fehlt:**
- ❌ Biome-spezifische Farben (Götterfels = Grau/Braun, Wald = Grün, Wüste = Gelb)
- ❌ Terrain-Texturen (derzeit nur weiß)
- ❌ Höhenprofile aktivieren (Berge, Täler)
- ❌ Wasser-Rendering (Küste, Seen)

**Datei:** `digivice/js/world/terrain_generator.js`

**Code-Snippet zum Fixen:**
```javascript
// In createTerrainMesh() - Material basierend auf Biome
const biomeColors = {
  'Mountain': 0x8B7355,    // Braun/Grau
  'Forest': 0x228B22,      // Grün
  'Desert': 0xEDC9AF,      // Sand-Gelb
  'Swamp': 0x556B2F,       // Dunkelgrün
  'Coast': 0xF4A460        // Hellbraun
};

const material = new THREE.MeshStandardMaterial({
  color: biomeColors[region.biome] || 0xCCCCCC,
  roughness: 0.8,
  metalness: 0.2
});
```

### 2. Vegetation-System aktivieren
**Priorität:** HOCH
**Was fehlt:**
- ❌ Bäume platzieren (KayKit Nature, Forest)
- ❌ Büsche platzieren
- ❌ Gräser/Blumen
- ❌ Biome-spezifische Vegetation (Palmen in Wüste, etc.)

**Datei:** `digivice/js/world/vegetation_system.js`

**Zu aktivieren in:** `digivice/js/world/region_streaming.js`
```javascript
// In buildRegion() nach terrain.add(terrainMesh):
if (this.vegetationSystem) {
  await this.vegetationSystem.populateRegion(region, terrainMesh);
}
```

### 3. Stadt-System aktivieren
**Priorität:** MITTEL
**Was fehlt:**
- ❌ 5 Städte bauen (Handelsfestung, Dampf-Hain, Salzige Bucht, Runenheim, Funken-Siedlung)
- ❌ Häuser platzieren (KayKit Medieval)
- ❌ Stadt-Layouts definieren

**Datei:** `digivice/js/world/city_builder.js`

**Zu aktivieren in:** `digivice/js/world/region_streaming.js`
```javascript
// Nach Vegetation:
if (this.cityBuilder && region.cities) {
  for (const city of region.cities) {
    await this.cityBuilder.buildCity(city, terrainMesh);
  }
}
```

### 4. LOD-System aktivieren
**Priorität:** NIEDRIG (Performance-Optimierung)
**Was fehlt:**
- ❌ Level-of-Detail für ferne Objekte
- ❌ Asset-Culling (nicht sichtbare Assets deaktivieren)

**Datei:** `digivice/js/world/lod_manager.js`

### 5. UI/UX Verbesserungen
**Priorität:** NIEDRIG
**Was fehlt:**
- ❌ Minimap
- ❌ Region-Namen anzeigen wenn man reinläuft
- ❌ Teleport-Buttons testen (funktionieren sie?)

### 6. Performance-Optimierung
**Priorität:** NIEDRIG
**Was fehlt:**
- ❌ Asset-Batching (mehrere Meshes kombinieren)
- ❌ Texture-Atlas
- ❌ Instancing für gleiche Objekte (Bäume, Steine)

## 📋 REIHENFOLGE DER IMPLEMENTATION

**Empfohlene Reihenfolge:**

1. **Terrain-Farben** (30 Min) - Sofort sichtbarer Effekt!
2. **Vegetation platzieren** (1-2 Stunden) - World sieht viel besser aus
3. **Städte bauen** (2-3 Stunden) - Gameplay-relevante Features
4. **LOD + Performance** (1-2 Stunden) - Wenn es laggt
5. **UI/UX Polish** (30 Min - 1 Stunde)

## 🎯 NÄCHSTER SCHRITT

**START HIER:**
```bash
# 1. Terrain-Farben aktivieren
#    Datei: digivice/js/world/terrain_generator.js
#    Funktion: createTerrainMesh()
#    Ändere: material.color basierend auf region.biome

# 2. Teste sofort:
#    Browser: http://localhost:8001/najika_world_v2.html
#    Hard Refresh (Ctrl+F5)
#    → Boden sollte jetzt farbig sein!
```

## 📊 FORTSCHRITT

**Gesamt-Progress:** ~40% fertig

- Core-Systeme: 100% ✅
- Terrain: 30% 🔧
- Vegetation: 10% 🔧
- Städte: 5% 🔧
- Performance: 0% ⏳
- UI/UX: 20% 🔧

**Geschätzte Zeit bis fertig:** 6-8 Stunden Arbeit
