# 🏙️ WEB MODEL #2 - STÄDTE & LIGHTING

**Deine Aufgabe:** 5 Städte bauen + Beleuchtung verbessern
**Ziel:** Städte sind sichtbar, Welt sieht professionell ausgeleuchtet aus!
**Deadline:** Heute (Teil 1 des 7-Tage-Plans)

---

## ⚠️ WICHTIG - LIES ZUERST!

### Pflichtlektüre (IN DIESER REIHENFOLGE):

1. **`WEB_MODEL_BUGFIX_REPORT.md`** - ALLE Fehler die du NICHT wiederholen darfst!
2. **`CLAUDE_CODE_WEB_LEITFADEN.md`** - Wie du richtig arbeitest
3. **`TEST_SERVER_ERKLAERUNG.md`** - Warum Port 8001, nicht 8000!
4. **`digivice/data/regions.json`** - Die 8 Regionen + Städte-Daten
5. **`NAJIKA_WORLD_V2_TODO.md`** - Was insgesamt noch zu tun ist

### Dateien die du ÄNDERN wirst:

```
digivice/najika_world_v2.html     ← Haupt-HTML-Datei (Lighting hier)
digivice/js/world_generator.js    ← Stadt-Platzierung hier
digivice/data/regions.json        ← Nur LESEN, nicht ändern!
```

---

## 📋 DEINE AUFGABE IM DETAIL

### Teil 1: STÄDTE BAUEN

**Aktueller Zustand:**
- Städte sind in `regions.json` definiert
- Aber NICHT in der 3D-Welt platziert
- Keine sichtbaren Gebäude

**Soll-Zustand:**
- 5 Haupt-Städte sind sichtbar
- Gebäude platziert (3D-Modelle)
- Stadt-Grenzen erkennbar

---

## 🏙️ DIE 5 STÄDTE (aus regions.json)

### Stadt-Daten aus `regions.json`:

```javascript
// Diese Daten sind BEREITS in regions.json!
// Du musst sie nur AUSLESEN und PLATZIEREN!

const CITIES_TO_BUILD = [
  {
    name: "Samtmoos-Stadt",
    region: "Samtmoos-Tiefwald",
    position: {x: -3600, z: -3600},  // NW Quadrant
    size: "medium",
    description: "Waldstadt mit Baumhäusern",
    buildings: 15,
    population: 500
  },

  {
    name: "Götterfels-Hauptstadt",
    region: "Götterfels",
    position: {x: 0, z: 0},  // Zentrum!
    size: "large",
    description: "Größte Stadt, Hauptstadt der Welt",
    buildings: 30,
    population: 2000,
    isCapital: true
  },

  {
    name: "Nekro-Stadt",
    region: "Reich der Drei",
    position: {x: 3600, z: -3600},  // NE Quadrant
    size: "small",
    description: "Gefrorene Stadt mit Eistürmen",
    buildings: 10,
    population: 200
  },

  {
    name: "Küstenstadt",
    region: "Salzwind-Küste",
    position: {x: -3600, z: 3600},  // SW Quadrant
    size: "medium",
    description: "Hafen-Stadt am Meer",
    buildings: 18,
    population: 800
  },

  {
    name: "Blitz-Stadt",
    region: "Blitzebene",
    position: {x: 3600, z: 3600},  // SE Quadrant
    size: "medium",
    description: "Hochebenen-Stadt mit Blitz-Türmen",
    buildings: 12,
    population: 600
  }
];
```

---

## 🏗️ GEBÄUDE-TYPEN

### Verfügbare 3D-Modelle:

**Check welche Modelle vorhanden sind:**
```bash
# Liste alle Gebäude-Modelle:
dir C:\Najika_World\digivice\assets\models\3d_models\building*.glb
dir C:\Najika_World\digivice\assets\models\3d_models\house*.glb
dir C:\Najika_World\digivice\assets\models\3d_models\tower*.glb
```

**Wahrscheinlich vorhanden:**
```
assets/models/3d_models/building_generic.glb
assets/models/3d_models/house.glb
assets/models/3d_models/tower.glb
```

**Falls NICHT vorhanden:**
Verwende Placeholder (Würfel/Quader):

```javascript
function createPlaceholderBuilding(size = 'medium') {
  const sizes = {
    small: {w: 3, h: 5, d: 3},
    medium: {w: 5, h: 8, d: 5},
    large: {w: 8, h: 12, d: 8}
  };

  const s = sizes[size];

  const geometry = new THREE.BoxGeometry(s.w, s.h, s.d);
  const material = new THREE.MeshStandardMaterial({
    color: 0x8b7355,
    roughness: 0.7,
    metalness: 0.3
  });

  const building = new THREE.Mesh(geometry, material);
  building.position.y = s.h / 2;  // Auf Boden stellen
  building.castShadow = true;
  building.receiveShadow = true;

  return building;
}
```

---

## 🔧 IMPLEMENTATION - SCHRITT FÜR SCHRITT

### Schritt 1: Städte aus regions.json laden

**In `world_generator.js`:**

```javascript
async function loadCities() {
  // Lade regions.json
  const response = await fetch('/data/regions.json');
  const data = await response.json();

  const cities = [];

  // Durchsuche alle Regionen nach Städten
  for (const region of data.regions) {
    if (region.cities && region.cities.length > 0) {
      for (const city of region.cities) {
        cities.push({
          ...city,
          regionName: region.name,
          regionBiome: region.biome
        });
      }
    }
  }

  console.log(`${cities.length} Städte gefunden`);
  return cities;
}
```

---

### Schritt 2: Stadt-Platzierungs-Funktion

```javascript
async function buildCity(cityData, scene) {
  console.log(`Baue Stadt: ${cityData.name}`);

  const {position, buildings, size, regionBiome} = cityData;

  // Stadt-Gruppe (alle Gebäude)
  const cityGroup = new THREE.Group();
  cityGroup.name = cityData.name;

  // Stadt-Zentrum
  const centerX = position.x;
  const centerZ = position.z;
  const centerY = getTerrainHeightAt(centerX, centerZ);

  // Stadtgröße in Metern
  const cityRadius = {
    small: 50,
    medium: 100,
    large: 150
  }[size] || 100;

  // === GEBÄUDE PLATZIEREN ===
  const buildingCount = buildings || 10;

  for (let i = 0; i < buildingCount; i++) {
    // Zufällige Position innerhalb Stadt-Radius
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * cityRadius;

    const x = centerX + Math.cos(angle) * distance;
    const z = centerZ + Math.sin(angle) * distance;
    const y = getTerrainHeightAt(x, z);

    // Gebäude erstellen
    const building = await createBuilding(cityData, i);

    building.position.set(x, y, z);

    // Zufällige Rotation
    building.rotation.y = Math.random() * Math.PI * 2;

    cityGroup.add(building);
  }

  // === STADT-MARKER (für Navigation) ===
  const marker = createCityMarker(cityData);
  marker.position.set(centerX, centerY + 20, centerZ);
  cityGroup.add(marker);

  cityGroup.position.set(0, 0, 0);
  scene.add(cityGroup);

  console.log(`✓ Stadt "${cityData.name}" gebaut (${buildingCount} Gebäude)`);
}

async function createBuilding(cityData, index) {
  // Versuche 3D-Modell zu laden
  const loader = new THREE.GLTFLoader();

  // Modell-Pfade (probiere verschiedene aus)
  const modelPaths = [
    'assets/models/3d_models/building_generic.glb',
    'assets/models/3d_models/house.glb',
    'assets/models/3d_models/tower.glb'
  ];

  // Zufälliges Modell
  const modelPath = modelPaths[index % modelPaths.length];

  try {
    const gltf = await new Promise((resolve, reject) => {
      loader.load(
        modelPath,
        resolve,
        undefined,
        reject
      );
    });

    const building = gltf.scene;

    // Skalierung
    const scale = 1 + Math.random() * 0.5;  // 1.0x - 1.5x
    building.scale.set(scale, scale, scale);

    // Schatten
    building.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
    });

    return building;

  } catch (error) {
    // Fallback: Placeholder
    console.warn(`Modell nicht gefunden: ${modelPath}, verwende Placeholder`);
    return createPlaceholderBuilding('medium');
  }
}

function createCityMarker(cityData) {
  // Text-Sprite für Stadt-Namen
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 128;

  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 48px Arial';
  ctx.textAlign = 'center';
  ctx.fillText(cityData.name, 256, 64);

  const texture = new THREE.CanvasTexture(canvas);

  const spriteMaterial = new THREE.SpriteMaterial({
    map: texture,
    transparent: true
  });

  const sprite = new THREE.Sprite(spriteMaterial);
  sprite.scale.set(20, 5, 1);

  return sprite;
}
```

---

### Schritt 3: Integration in Welt-Generierung

**In der Haupt-Generierungs-Funktion:**

```javascript
async function generateWorld() {
  // ... Terrain & Vegetation (von Web-Model #1) ...

  // === STÄDTE BAUEN ===
  console.log("=== Baue Städte ===");

  const cities = await loadCities();

  for (const city of cities) {
    await buildCity(city, scene);
  }

  console.log(`✓ ${cities.length} Städte gebaut`);
}
```

---

## 💡 LIGHTING - VERBESSERN

### Schritt 1: Aktuelles Lighting checken

**Öffne `najika_world_v2.html` und finde die Lighting-Setup-Stelle.**

Wahrscheinlich so etwas wie:

```javascript
// Ambient Light
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// Directional Light (Sonne)
const sunLight = new THREE.DirectionalLight(0xffffff, 1.0);
sunLight.position.set(100, 100, 50);
scene.add(sunLight);
```

---

### Schritt 2: VERBESSERE Lighting

**Ersetze mit diesem Setup:**

```javascript
// === LIGHTING SETUP ===

// 1. Ambient Light (Basis-Helligkeit)
const ambientLight = new THREE.AmbientLight(0x404040, 0.3);  // Dunkler für besseren Kontrast
scene.add(ambientLight);

// 2. Hemisphere Light (Himmel + Boden)
const hemisphereLight = new THREE.HemisphereLight(
  0x87ceeb,  // Himmelblau
  0x4a5d3f,  // Bodengrün
  0.4
);
scene.add(hemisphereLight);

// 3. Directional Light (Sonne)
const sunLight = new THREE.DirectionalLight(0xfff8dc, 1.2);  // Warmes Sonnenlicht
sunLight.position.set(1000, 1500, 500);
sunLight.castShadow = true;

// Schatten-Einstellungen
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 5000;
sunLight.shadow.camera.left = -2000;
sunLight.shadow.camera.right = 2000;
sunLight.shadow.camera.top = 2000;
sunLight.shadow.camera.bottom = -2000;
sunLight.shadow.bias = -0.0001;

scene.add(sunLight);

// 4. Point Lights für Städte (optional)
function addCityLights(cityPosition) {
  const cityLight = new THREE.PointLight(0xffaa00, 1.5, 100);
  cityLight.position.set(cityPosition.x, cityPosition.y + 15, cityPosition.z);
  cityLight.castShadow = true;
  scene.add(cityLight);
}

// 5. Renderer Schatten aktivieren
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;  // Weiche Schatten

// 6. Tone Mapping (für bessere Farben)
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

// 7. Fog (optionaler Nebel für Atmosphäre)
scene.fog = new THREE.Fog(0x87ceeb, 1000, 8000);  // Himmelblau-Nebel
```

---

### Schritt 3: Tag/Nacht-Zyklus (OPTIONAL)

**Wenn Zeit ist:**

```javascript
class DayNightCycle {
  constructor(scene, sunLight) {
    this.scene = scene;
    this.sunLight = sunLight;
    this.time = 0;  // 0-24 (Stunden)
    this.speed = 0.01;  // Geschwindigkeit
  }

  update(deltaTime) {
    this.time += deltaTime * this.speed;
    if (this.time >= 24) this.time = 0;

    // Sonnen-Position
    const angle = (this.time / 24) * Math.PI * 2;
    const radius = 1500;

    this.sunLight.position.x = Math.cos(angle) * radius;
    this.sunLight.position.y = Math.sin(angle) * radius;

    // Licht-Intensität
    if (this.time >= 6 && this.time <= 18) {
      // Tag (6:00 - 18:00)
      this.sunLight.intensity = 1.2;
      this.sunLight.color.setHex(0xfff8dc);  // Warmes Licht
      this.scene.fog.color.setHex(0x87ceeb);  // Blauer Himmel
    } else {
      // Nacht (18:00 - 6:00)
      this.sunLight.intensity = 0.2;
      this.sunLight.color.setHex(0x4a5f8f);  // Blaues Mondlicht
      this.scene.fog.color.setHex(0x1a1a2e);  // Dunkler Himmel
    }
  }
}

// Usage:
const dayNight = new DayNightCycle(scene, sunLight);

function animate() {
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();
  dayNight.update(deltaTime);

  renderer.render(scene, camera);
}
```

---

## ⚠️ FEHLER-VERMEIDUNG

### DO's:
- ✅ Schatten aktivieren (`castShadow`, `receiveShadow`)
- ✅ Shadow Map Size vernünftig (2048x2048)
- ✅ Gebäude auf Terrain-Höhe platzieren
- ✅ Stadt-Positionen aus `regions.json` lesen
- ✅ Console-Logs für Debugging

### DON'Ts:
- ❌ NICHT zu viele Schatten (Performance!)
- ❌ NICHT Gebäude unter Terrain platzieren
- ❌ NICHT hardcoded Stadt-Positionen
- ❌ NICHT Shadow Map Size > 4096 (zu langsam!)
- ❌ NICHT regions.json ändern

---

## 🧪 TESTING

### 1. Server starten:

```bash
cd C:\Najika_World
.\START_WORLD_V2_TEST.bat
```

**Browser:** http://localhost:8001/najika_world_v2.html

---

### 2. Was du sehen solltest:

✅ **5 Städte sichtbar:**
- Samtmoos-Stadt (NW)
- Götterfels-Hauptstadt (Zentrum)
- Nekro-Stadt (NE)
- Küstenstadt (SW)
- Blitz-Stadt (SE)

✅ **Beleuchtung:**
- Warmes Sonnenlicht
- Weiche Schatten
- Nicht zu dunkel, nicht zu hell
- Nebel in der Ferne (optional)

✅ **Performance:**
- FPS > 30
- Keine Freezes

---

### 3. Console-Checks:

```javascript
// Erwarte Logs:
// "5 Städte gefunden"
// "Baue Stadt: Samtmoos-Stadt"
// "✓ Stadt Samtmoos-Stadt gebaut (15 Gebäude)"
// ...
// "✓ 5 Städte gebaut"
```

---

### 4. Visueller Check:

**Fliege zur Götterfels-Hauptstadt (0, 0):**
- Sollte größte Stadt sein (30 Gebäude)
- Stadt-Marker sichtbar
- Beleuchtung gut

**Check Schatten:**
- Gebäude werfen Schatten
- Schatten sind weich (nicht pixelig)

---

## 📊 PERFORMANCE-OPTIMIERUNG

### Falls FPS zu niedrig:

1. **Schatten reduzieren:**
```javascript
sunLight.shadow.mapSize.width = 1024;  // Statt 2048
sunLight.shadow.mapSize.height = 1024;
```

2. **Weniger Gebäude:**
```javascript
const buildingCount = Math.floor(buildings * 0.7);  // 30% weniger
```

3. **Frustum Culling:**
```javascript
building.frustumCulled = true;  // Nur sichtbare rendern
```

4. **LOD System (später):**
```javascript
const lod = new THREE.LOD();
lod.addLevel(detailedBuilding, 0);
lod.addLevel(simpleBuilding, 100);
lod.addLevel(placeholderBuilding, 500);
```

---

## 📤 FERTIG? PUSH INS REPO!

### Wenn alles funktioniert:

```bash
git add digivice/najika_world_v2.html
git add digivice/js/world_generator.js
git commit -m "feat: 5 Städte gebaut und Lighting verbessert

- 5 Hauptstädte aus regions.json platziert
- Gebäude mit 3D-Modellen oder Placeholders
- Stadt-Marker für Navigation
- Verbessertes Lighting-Setup (Sonne, Schatten, Fog)
- Tag/Nacht-Zyklus (optional implementiert)
- Tested auf Port 8001, Performance OK"

git push
```

**Dann:** Ping Claude Code (CLI) im Chat dass du fertig bist!

---

## ❓ PROBLEME?

### Städte nicht sichtbar:

**Check:**
1. `loadCities()` findet Städte? (Console-Log)
2. Positionen korrekt? (x, z innerhalb Map)
3. Höhe korrekt? (`getTerrainHeightAt` funktioniert?)

### Beleuchtung zu dunkel:

**Lösung:**
```javascript
ambientLight.intensity = 0.5;  // Erhöhen
sunLight.intensity = 1.5;       // Erhöhen
```

### Schatten pixelig:

**Lösung:**
```javascript
sunLight.shadow.mapSize.width = 4096;  // Erhöhen (langsamer!)
sunLight.shadow.bias = -0.00001;       // Anpassen
```

### Performance-Issues:

**Lösung:**
- Schatten deaktivieren: `renderer.shadowMap.enabled = false;`
- Weniger Gebäude
- Einfachere Modelle

---

## 📚 REFERENZEN

- **regions.json:** `C:\Najika_World\digivice\data\regions.json`
- **Assets:** `C:\Najika_World\digivice\assets\models\3d_models\`
- **THREE.js Docs:** https://threejs.org/docs/
- **Fehler-Report:** `C:\Najika_World\WEB_MODEL_BUGFIX_REPORT.md`

---

**VIEL ERFOLG! Du schaffst das! 🏙️💡**

**Nach Push:** CLI übernimmt Review & Fix falls nötig!
