# 🌍 Najika World - Integration Guide

## Übersicht

Das neue 8-Regionen-World-System ist modular aufgebaut und kann einfach in den bestehenden Digivice-Code integriert werden.

## Modul-Struktur

```
entwicklung/world/
├── terrain_generator.js     # Terrain-Generierung mit Perlin Noise
├── biome_system.js          # Biome-Visuals (Fog, Lighting, Materials)
├── vegetation_system.js     # Vegetation-Placement
├── city_builder.js          # Stadt-Konstruktion
├── region_streaming.js      # Regionen-Streaming (Performance)
├── lod_manager.js           # Level of Detail Management
└── world_manager.js         # 🌟 Hauptorchestrator (USE THIS!)
```

## Schnellstart: WorldManager verwenden

### 1. Import

```javascript
import WorldManager from '/entwicklung/world/world_manager.js';
```

### 2. Initialisierung

```javascript
// In deiner 3d_scene.js oder main.js
const worldManager = new WorldManager(scene, camera);

// Initialisiere die Welt (async!)
await worldManager.initialize({
  dataPath: '/entwicklung/data/',  // Path zu regions.json, biomes.json, cities.json
  enableLOD: true,                  // LOD aktivieren (empfohlen)
  enableStreaming: true,            // Region-Streaming aktivieren (empfohlen)
  enableVegetationBatching: true    // Vegetation-Instancing (Performance)
});
```

### 3. Update Loop

```javascript
// In deinem Animation-Loop
function animate() {
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();

  // Update World-System
  worldManager.update(deltaTime);

  // Update Player Position (für Streaming)
  worldManager.setPlayerPosition(player.position);

  renderer.render(scene, camera);
}
```

---

## API Reference

### Initialisierung

```javascript
await worldManager.initialize(options)
```

**Options:**
- `dataPath` (string): Pfad zu JSON-Daten (default: `/entwicklung/data/`)
- `enableLOD` (boolean): LOD aktivieren (default: true)
- `enableStreaming` (boolean): Region-Streaming aktivieren (default: true)
- `enableVegetationBatching` (boolean): Vegetation-Instancing (default: true)

---

### Spieler-Position

```javascript
// Position setzen (für Streaming)
worldManager.setPlayerPosition(new THREE.Vector3(x, y, z));

// Aktuelle Region abfragen
const region = worldManager.getCurrentRegion();
console.log(region.name);  // z.B. "Samtmoos-Tiefwald"

// Nahe Regionen finden
const nearby = worldManager.getNearbyRegions(5000);  // Radius in Units
```

---

### Teleportation

```javascript
// Teleport zu Position
worldManager.teleportTo(new THREE.Vector3(4800, 0, 4800));  // Götterfels

// Teleport zu Stadt (by name)
worldManager.teleportToCity("Handelsfestung");
worldManager.teleportToCity("Dampf-Hain");
worldManager.teleportToCity("Salzige Bucht");
worldManager.teleportToCity("Runenheim");
worldManager.teleportToCity("Funken-Siedlung");

// Teleport zu Region (by name or ID)
worldManager.teleportToRegion("Samtmoos-Tiefwald");
worldManager.teleportToRegion("heisse_duenen");
```

---

### Terrain-Interaktion

```javascript
// Höhe an Position abfragen
const height = worldManager.getHeightAt(x, z);

// Vegetation in der Nähe finden
const vegetation = worldManager.getVegetationNear(position, radius);

// Vegetation entfernen (Harvesting)
const removed = worldManager.removeVegetationAt(position, 2);
console.log(`Removed ${removed} vegetation items`);

// Vegetation spawnen (Replanting)
worldManager.spawnVegetationAt('tree', position);
```

---

### Performance-Einstellungen

```javascript
// Streaming aktivieren/deaktivieren
worldManager.setStreaming(true);  // Nur nahe Regionen laden
worldManager.setStreaming(false); // Alle Regionen laden (laggy!)

// Streaming-Radius ändern
worldManager.setStreamingRadius(2);  // 2 Regionen = empfohlen
worldManager.setStreamingRadius(3);  // 3 Regionen = mehr laden

// LOD aktivieren/deaktivieren
worldManager.setLOD(true);  // Empfohlen für Performance
```

---

### Debug & Stats

```javascript
// Statistiken anzeigen
worldManager.logStats();

// Städte auflisten
worldManager.listCities();

// Regionen auflisten
worldManager.listRegions();

// LOD visualisieren (Farb-Coding)
worldManager.debugLOD(true);  // Grün=High, Gelb=Medium, Orange=Low

// Geladene Regionen anzeigen
worldManager.debugRegions();

// Stats als Object
const stats = worldManager.getStats();
console.log(stats);
```

---

## Integration in bestehenden Code

### Beispiel: Integration in `digivice/js/3d_scene.js`

```javascript
// Alte Konstanten anpassen
const OPEN_WORLD_SIZE = 9600;  // Vorher: 2400
const WORLD_CENTER = { x: 4800, z: 4800 };

// WorldManager initialisieren
import WorldManager from '/entwicklung/world/world_manager.js';

let worldManager;

async function initWorld() {
  worldManager = new WorldManager(scene, camera);

  const success = await worldManager.initialize({
    dataPath: '/entwicklung/data/',
    enableLOD: true,
    enableStreaming: true
  });

  if (success) {
    console.log('✅ Najika World loaded!');

    // Starte bei Götterfels
    worldManager.teleportTo(new THREE.Vector3(4800, 50, 4800));
  }
}

// In animation loop
function animate() {
  requestAnimationFrame(animate);

  // Update World
  if (worldManager && worldManager.initialized) {
    worldManager.update(clock.getDelta());
    worldManager.setPlayerPosition(camera.position);
  }

  // Deine bestehenden Updates...
  controls.update();

  renderer.render(scene, camera);
}

// Initialisieren
initWorld();
```

---

### Bestehende Systeme kompatibel halten

**Garden System:**
```javascript
// Garten-Position bleibt kompatibel (kann überall platziert werden)
const gardenPosition = new THREE.Vector3(4900, worldManager.getHeightAt(4900, 4900), 4900);
```

**Fishing System:**
```javascript
// Fischen nur in Wasser-Biomes (Coast, Swamp, Forest mit Wasser)
const currentRegion = worldManager.getCurrentRegion();
if (currentRegion && currentRegion.waterPresence) {
  // Fischen erlaubt
} else {
  console.log('Kein Wasser in der Nähe!');
}
```

**Crafting System:**
```javascript
// Crafting überall möglich, aber Städte haben spezielle Forges
const currentRegion = worldManager.getCurrentRegion();
if (currentRegion.city && currentRegion.city.name === 'Funken-Siedlung') {
  // Meister-Schmiede verfügbar (bessere Items)
}
```

---

## Performance-Tipps

### Empfohlene Einstellungen

```javascript
// Für beste Performance:
await worldManager.initialize({
  enableLOD: true,              // ✅ WICHTIG
  enableStreaming: true,         // ✅ WICHTIG
  enableVegetationBatching: true // ✅ WICHTIG
});

worldManager.setStreamingRadius(2);  // Nicht höher als 2-3!
```

### Was wird geladen?

**Mit Streaming (Radius 2):**
- Aktuelle Region + 2 benachbarte = ~3-5 Regionen
- Performance: ✅ Gut (60 FPS möglich)

**Ohne Streaming:**
- ALLE 9 Regionen gleichzeitig
- Performance: ⚠️ Laggy (<30 FPS)

---

## Tastenkürzel (Development)

Füge diese zu deinem Dev-Mode hinzu:

```javascript
// In deinem Keyboard-Handler
window.addEventListener('keydown', (e) => {
  if (e.key === 'F1') worldManager.logStats();
  if (e.key === 'F2') worldManager.listCities();
  if (e.key === 'F3') worldManager.debugLOD(true);

  // Schnell-Teleport (Numpad)
  if (e.key === '1') worldManager.teleportToCity('Handelsfestung');
  if (e.key === '2') worldManager.teleportToCity('Dampf-Hain');
  if (e.key === '3') worldManager.teleportToCity('Salzige Bucht');
  if (e.key === '4') worldManager.teleportToCity('Runenheim');
  if (e.key === '5') worldManager.teleportToCity('Funken-Siedlung');
  if (e.key === '0') worldManager.teleportTo(new THREE.Vector3(4800, 50, 4800)); // Götterfels
});
```

---

## Nächste Schritte

### Phase 1: Core Testing (JETZT)
1. ✅ Alle Module erstellt
2. ⏳ Integration in `3d_scene.js`
3. ⏳ Test: Terrain lädt korrekt
4. ⏳ Test: Biome-Visuals funktionieren
5. ⏳ Test: Städte werden platziert

### Phase 2: Asset Replacement
1. KayKit-Assets downloaden (siehe `ASSET_PACKS_LISTE.md`)
2. Asset-Loader implementieren
3. Placeholder-Geometries ersetzen
4. Texturen anwenden

### Phase 3: System-Integration
1. Housing-System implementieren (siehe `HOUSING_SYSTEM_DESIGN.md`)
2. Farming-System in Regionen integrieren
3. Fishing-System an Wasser-Regionen binden
4. PvP-Arena (Handelsfestung) implementieren

---

## Troubleshooting

### Problem: "Failed to load world data"
- ✅ Prüfe `dataPath` in `initialize()`
- ✅ Stelle sicher dass `regions.json`, `biomes.json`, `cities.json` existieren
- ✅ Prüfe Browser-Console auf CORS-Fehler

### Problem: Performance ist schlecht
- ✅ Aktiviere `enableLOD: true`
- ✅ Aktiviere `enableStreaming: true`
- ✅ Reduziere `streamingRadius` auf 2
- ✅ Reduziere Shadow-Quality

### Problem: Keine Vegetation sichtbar
- ✅ Prüfe ob Region geladen ist: `worldManager.debugRegions()`
- ✅ Prüfe Vegetation-Stats: `worldManager.logStats()`
- ✅ Teleport näher zu Region-Center

### Problem: Städte nicht sichtbar
- ✅ Prüfe `cities.json` - korrekte Positionen?
- ✅ Teleport direkt zur Stadt: `worldManager.teleportToCity('Handelsfestung')`
- ✅ Prüfe ob Stadt in geladener Region liegt

---

## Beispiel: Vollständige Integration

Siehe: `/entwicklung/INTEGRATION_EXAMPLE.js` für komplettes Code-Beispiel!

---

## Support

Bei Fragen oder Problemen:
1. Prüfe Browser-Console auf Fehler
2. Nutze `worldManager.logStats()` für Debug-Info
3. Nutze `worldManager.debugRegions()` um geladene Regionen zu sehen

---

**Stand: 2025-11-07**
**Version: 1.0.0**
**Status: ✅ Entwicklung abgeschlossen, Integration ausstehend**
