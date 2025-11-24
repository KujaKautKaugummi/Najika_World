# 🗺️ WEB MODEL 2 - MAP REBUILD AUFTRAG

## 🎯 ZIEL
Erstelle **najika_world_UNIFIED.html** - Eine zusammenhängende 9.6km x 9.6km Open World Map mit Combat-System und allen JSON-Daten.

---

## 📐 TECHNISCHE SPECS

### Map-Größe (Fortnite Battle Royale Scale)
```
Total World: 9600m x 9600m (9.6km)
Per Region: 3200m x 3200m (3.2km)
3x3 Grid Layout (9 Regionen)

Fortnite BR zum Vergleich: 5.5km x 5.5km
→ Najika World ist 1.75x größer!
```

### Region-Layout (3x3 Grid)
```
┌─────────────┬─────────────┬─────────────┐
│ Reich der   │ Blitzebene  │ Heiße       │
│ Drei (Ice)  │ (Highland)  │ Dünen       │
│ x:-3200     │ x:0         │ x:3200      │
│ z:3200      │ z:3200      │ z:3200      │
├─────────────┼─────────────┼─────────────┤
│ Grünschlamm │ Götterfels  │ Salzwind-   │
│ (Swamp)     │ (Mountain)  │ Küste       │
│ x:-3200     │ x:0         │ x:3200      │
│ z:0         │ z:0         │ z:0         │
├─────────────┼─────────────┼─────────────┤
│ Tiefen-     │ Samtmoos-   │ Magma-      │
│ höhlen      │ Tiefwald    │ ströme      │
│ (Caves)     │ (Forest)    │ (Volcano)   │
│ x:-3200     │ x:0         │ x:3200      │
│ z:-3200     │ z:-3200     │ z:-3200     │
└─────────────┴─────────────┴─────────────┘
```

---

## 📋 PHASE 1: FLAT PROTOTYPE (Priorität: HOCH)

### Aufgabe 1.1: Base Map erstellen
```javascript
// WICHTIG: Größe = 3200m pro Region (nicht 133m!)
const REGION_SIZE = 3200;  // 3.2km
const WORLD_SIZE = 9600;   // 9.6km

const regions = [
    // Row 1 (North): z = 3200
    {
        name: 'reich_der_drei',
        displayName: 'Reich der Drei',
        biome: 'ice',
        color: 0xf0f8ff,  // Alice Blue
        x: -3200, z: 3200, y: 0
    },
    {
        name: 'blitzebene',
        displayName: 'Blitzebene',
        biome: 'highland',
        color: 0x8b7355,  // Burlywood4
        x: 0, z: 3200, y: 0
    },
    {
        name: 'heisse_duenen',
        displayName: 'Heiße Dünen',
        biome: 'desert',
        color: 0xe8d4a0,  // Sand
        x: 3200, z: 3200, y: 0
    },

    // Row 2 (Center): z = 0
    {
        name: 'gruenschlamm',
        displayName: 'Grünschlamm',
        biome: 'swamp',
        color: 0x556b2f,  // Dark Olive Green
        x: -3200, z: 0, y: 0
    },
    {
        name: 'goetterfels',
        displayName: 'Götterfels',
        biome: 'mountain',
        color: 0x808080,  // Gray
        x: 0, z: 0, y: 50  // HÖHER (Berg!)
    },
    {
        name: 'salzwind_kueste',
        displayName: 'Salzwind-Küste',
        biome: 'coast',
        color: 0xc2b280,  // Sand/Beach
        x: 3200, z: 0, y: 0
    },

    // Row 3 (South): z = -3200
    {
        name: 'tiefenhoehlen',
        displayName: 'Tiefenhöhlen',
        biome: 'caves',
        color: 0x2f2f2f,  // Dark Gray
        x: -3200, z: -3200, y: 0
    },
    {
        name: 'samtmoos_tiefwald',
        displayName: 'Samtmoos-Tiefwald',
        biome: 'forest',
        color: 0x2d5016,  // Dark Forest Green
        x: 0, z: -3200, y: 0
    },
    {
        name: 'magmastroeme',
        displayName: 'Magmaströme',
        biome: 'volcano',
        color: 0x8b4513,  // Saddle Brown
        x: 3200, z: -3200, y: 0
    }
];

// Regionen generieren
regions.forEach(region => {
    const geometry = new THREE.PlaneGeometry(
        REGION_SIZE,  // 3200m width
        REGION_SIZE,  // 3200m depth
        50,           // 50 segments (für Details)
        50
    );

    const material = new THREE.MeshStandardMaterial({
        color: region.color,
        roughness: 0.9,
        metalness: 0.1,
        side: THREE.DoubleSide
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.rotation.x = -Math.PI / 2;  // Flat liegen
    mesh.position.set(region.x, region.y, region.z);
    mesh.receiveShadow = true;
    mesh.castShadow = true;
    mesh.name = `region_${region.name}`;
    mesh.userData = { regionData: region };

    scene.add(mesh);
});
```

### Aufgabe 1.2: Combat-System übernehmen
Kopiere das **komplette Combat-System** aus `najika_world_9regions_test.html`:
- Realtime Combat Class
- Enemy Spawning
- Weapon System
- Combat Modes (MANUAL/ASSIST/AUTO)
- HP/Stamina/Cheer Bars

**WICHTIG:** Skaliere Enemy-Spawn-Positionen auf neue Größe:
```javascript
// ALT (9regions_test):
const spawnX = region.x + Math.random() * 100 - 50;

// NEU (UNIFIED):
const spawnX = region.x + Math.random() * 3000 - 1500;  // 3000m statt 100m!
```

### Aufgabe 1.3: JSON-Daten laden
Erstelle JSON-Loader für die 36 Dateien in `/data/`:

```javascript
class DataLoader {
    constructor() {
        this.npcs = {};
        this.items = {};
        this.quests = {};
        this.enemies = {};
    }

    async loadAll() {
        const regions = [
            'reich_der_drei',
            'blitzebene',
            'heisse_duenen',
            'gruenschlamm',
            'goetterfels',
            'salzwind_kueste',
            'tiefenhoehlen',
            'samtmoos_tiefwald',
            'magmastroeme'
        ];

        for (const region of regions) {
            // NPCs laden
            const npcsResponse = await fetch(`/data/npcs_${region}.json`);
            this.npcs[region] = await npcsResponse.json();

            // Items laden
            const itemsResponse = await fetch(`/data/items_${region}.json`);
            this.items[region] = await itemsResponse.json();

            // Quests laden
            const questsResponse = await fetch(`/data/quests_${region}.json`);
            this.quests[region] = await questsResponse.json();

            // Enemies laden
            const enemiesResponse = await fetch(`/data/enemies_${region}.json`);
            this.enemies[region] = await enemiesResponse.json();
        }

        console.log('✅ All JSON data loaded:', {
            npcs: Object.values(this.npcs).flat().length,
            items: Object.values(this.items).flat().length,
            quests: Object.values(this.quests).flat().length,
            enemies: Object.values(this.enemies).flat().length
        });
    }

    // Enemies für Region spawnen
    spawnEnemiesForRegion(regionName) {
        const enemyData = this.enemies[regionName];
        if (!enemyData) return;

        enemyData.forEach(enemyDef => {
            // Spawn-Logic hier (aus Combat-System)
            const enemy = realtimeCombat.spawnEnemy({
                name: enemyDef.name,
                type: enemyDef.type,
                health: enemyDef.stats.health,
                damage: enemyDef.stats.damage,
                speed: enemyDef.stats.speed,
                level: enemyDef.level,
                drops: enemyDef.drops,
                regionName: regionName
            });
        });
    }
}
```

### Aufgabe 1.4: Kamera & Bewegung anpassen
```javascript
// Kamera-Geschwindigkeit für größere Map
const MOVE_SPEED = 80;  // Schneller (war 20 in 9regions_test)
const SPRINT_MULTIPLIER = 2.5;  // Sprint = 200 units/s

// Camera-Bounds für große Map
const WORLD_BOUNDS = {
    minX: -4800,  // -3200 - 1600 (Puffer)
    maxX: 4800,   // 3200 + 1600
    minZ: -4800,
    maxZ: 4800
};
```

---

## 📋 PHASE 2: TERRAIN VARIATION (Priorität: MITTEL)

### Aufgabe 2.1: Höhenprofile pro Biome
Füge **nach** Phase 1 Höhenvariation hinzu:

```javascript
// Götterfels (Mountain) - HÖCHSTER PUNKT
function applyMountainTerrain(geometry, regionData) {
    const vertices = geometry.attributes.position.array;
    const centerX = 0;
    const centerZ = 0;

    for (let i = 0; i < vertices.length; i += 3) {
        const x = vertices[i];
        const z = vertices[i + 1];

        // Distanz vom Center
        const distFromCenter = Math.sqrt(x * x + z * z);
        const maxDist = REGION_SIZE / 2;

        // Berg in der Mitte, sanft abfallend zu Edges
        const heightFactor = 1 - (distFromCenter / maxDist);
        const baseHeight = Math.max(0, heightFactor * 150);  // 150m Peak

        // Perlin Noise für Organik
        const noise = perlin2D(x * 0.001, z * 0.001) * 20;

        vertices[i + 2] = baseHeight + noise;  // Y-Koordinate setzen
    }

    geometry.attributes.position.needsUpdate = true;
    geometry.computeVertexNormals();
}

// Heiße Dünen (Desert) - SANFTE WELLEN
function applyDesertTerrain(geometry, regionData) {
    const vertices = geometry.attributes.position.array;

    for (let i = 0; i < vertices.length; i += 3) {
        const x = vertices[i];
        const z = vertices[i + 1];

        // Layered Perlin für Dünen
        const noise1 = perlin2D(x * 0.0008, z * 0.0008) * 15;
        const noise2 = perlin2D(x * 0.002, z * 0.002) * 5;

        vertices[i + 2] = noise1 + noise2;
    }

    geometry.attributes.position.needsUpdate = true;
    geometry.computeVertexNormals();
}

// WICHTIG: Edge-Blending zwischen Regionen!
// Vertices an Grenzen müssen SMOOTH sein, nicht abrupt!
```

### Aufgabe 2.2: Perlin Noise Implementierung
Nutze diese Funktion (bereits in 9regions_test.html vorhanden):

```javascript
// Simple Perlin-like noise
function perlin2D(x, z) {
    return (Math.sin(x * 0.1) + Math.sin(z * 0.1)) * 0.5;
}
```

Oder bessere Implementierung mit simplex-noise.js:
```html
<script src="https://cdn.jsdelivr.net/npm/simplex-noise@4.0.1/dist/simplex-noise.min.js"></script>
```

---

## 📋 DELIVERABLES

### Datei: `najika_world_UNIFIED.html`
**Größe:** ~30-40KB (größer als 9regions_test wegen JSON-Loading)

**Features:**
- ✅ 9.6km x 9.6km Map (3x3 Grid)
- ✅ Combat-System funktionsfähig
- ✅ JSON-Daten geladen (~90 NPCs, ~200 Items, ~80 Quests, ~45 Enemies)
- ✅ Enemies spawnen in richtigen Regionen
- ✅ Phase 1: Flat terrain
- ✅ Phase 2: Höhenvariation (optional, aber empfohlen)
- ✅ Minimap skaliert auf 9.6km
- ✅ Teleport-System zu allen 9 Regionen

### Testing-Checklist:
```
[ ] Map lädt ohne Fehler
[ ] Alle 9 Regionen sichtbar
[ ] Character spawnt in Götterfels (Center)
[ ] WASD-Bewegung funktioniert (schnell genug für große Map!)
[ ] Enemies spawnen aus JSON-Daten
[ ] Combat funktioniert (MANUAL/ASSIST/AUTO)
[ ] JSON-Daten korrekt geladen (Console-Log prüfen)
[ ] Teleport zu allen Regionen funktioniert
[ ] Performance > 30 FPS
```

---

## 🚫 WAS DU NICHT TUN SOLLST

❌ **NICHT** World Manager JS-Module verwenden (zu komplex)
❌ **NICHT** TerrainGenerator.js nutzen (macht Zick-Zack)
❌ **NICHT** neue Combat-Logik erfinden (nutze 9regions_test)
❌ **NICHT** Region-Positionen aus regions.json nehmen (sind verstreut!)
❌ **NICHT** Assets/3D-Models laden (erstmal nur farbige Planes)

---

## ✅ WAS DU TUN SOLLST

✅ **NUTZE** najika_world_9regions_test.html als Code-Basis
✅ **SKALIERE** auf 3200m x 3200m pro Region (24x größer!)
✅ **LADE** die 36 JSON-Dateien aus `/data/`
✅ **INTEGRIERE** Combat-System 1:1 (nur Spawn-Positionen skalieren)
✅ **HALTE** es einfach und performant (eine HTML-Datei)
✅ **TESTE** gründlich mit Console-Logs

---

## 📊 ERFOLGS-KRITERIEN

1. **Map-Größe korrekt:** 9600m x 9600m (mit `console.log` bestätigen)
2. **Regionen zusammenhängend:** Keine Lücken zwischen Regionen
3. **Combat funktioniert:** Enemies spawnen und angreifen
4. **JSON-Daten geladen:** ~90 NPCs, ~200 Items, ~80 Quests, ~45 Enemies
5. **Performance gut:** Mindestens 30 FPS

---

## 🎯 ZEITPLAN

**Phase 1 (Flat Prototype):** 2-3 Stunden
- Map-Größe anpassen
- Combat-System übernehmen
- JSON-Loader schreiben
- Testing

**Phase 2 (Terrain Variation):** 2-3 Stunden
- Höhenprofile implementieren
- Edge-Blending zwischen Regionen
- Testing + Performance-Optimierung

**Total:** 4-6 Stunden

---

## 📁 BENÖTIGTE DATEIEN

**Input:**
- `C:/Najika_World/digivice/najika_world_9regions_test.html` (Code-Basis)
- `C:/Najika_World/digivice/data/*.json` (36 Dateien - NPCs, Items, Quests, Enemies)

**Output:**
- `C:/Najika_World/digivice/najika_world_UNIFIED.html` (Neue Version)

---

## 🤖 FRAGEN?

Falls etwas unklar ist:
1. Schau in `najika_world_9regions_test.html` (funktionierendes Beispiel)
2. Nutze die JSON-Struktur aus `/data/enemies_goetterfels.json` als Referenz
3. Teste schrittweise (erst Map, dann Combat, dann JSON)

Viel Erfolg! 🚀
