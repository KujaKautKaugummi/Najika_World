# 🎨 WEB MODEL #1 - TERRAIN-FARBEN & VEGETATION

**Deine Aufgabe:** Biome-spezifische Terrain-Farben + Vegetation implementieren
**Ziel:** Najika World V2 soll nicht mehr grau aussehen, sondern lebendige Biome haben!
**Deadline:** Heute (Teil 1 des 7-Tage-Plans)

---

## ⚠️ WICHTIG - LIES ZUERST!

### Pflichtlektüre (IN DIESER REIHENFOLGE):

1. **`WEB_MODEL_BUGFIX_REPORT.md`** - ALLE Fehler die du NICHT wiederholen darfst!
2. **`CLAUDE_CODE_WEB_LEITFADEN.md`** - Wie du richtig arbeitest
3. **`TEST_SERVER_ERKLAERUNG.md`** - Warum Port 8001, nicht 8000!
4. **`digivice/data/regions.json`** - Die 8 Regionen mit allen Daten
5. **`NAJIKA_WORLD_V2_TODO.md`** - Was insgesamt noch zu tun ist

### Dateien die du ÄNDERN wirst:

```
digivice/najika_world_v2.html     ← Haupt-HTML-Datei
digivice/js/world_generator.js    ← Welt-Generierung (HIER arbeitest du!)
digivice/data/regions.json        ← Nur LESEN, nicht ändern!
```

---

## 📋 DEINE AUFGABE IM DETAIL

### Teil 1: TERRAIN-FARBEN (Biome-spezifisch)

**Aktueller Zustand:**
- Alles ist GRAU/weiß
- Keine Biome-Unterschiede
- Langweilig

**Soll-Zustand:**
- Jede der 8 Regionen hat eigene Farb-Palette
- Terrain reflektiert Biom-Typ (Wald=grün, Eis=weiß, Wüste=gelb, etc.)
- Klare visuelle Unterscheidung zwischen Regionen

---

### DIE 8 REGIONEN & IHRE FARBEN:

**WICHTIG:** Diese Namen sind FINAL! Verwende EXAKT diese Namen!

```javascript
const BIOME_COLORS = {
  "Samtmoos-Tiefwald": {
    // Wald-Biom
    terrain: 0x2d5016,      // Dunkelgrün
    grass: 0x3a6b1f,        // Grasgrün
    accent: 0x4a7c2f,       // Hellgrün (für Highlights)
    description: "Dichter Wald mit moosigen Böden"
  },

  "Reich der Drei": {
    // Eis/Nekromantie-Biom
    terrain: 0xe8f4f8,      // Eisweiß
    snow: 0xffffff,         // Schnee
    ice: 0xb8d8e8,          // Eisblau
    accent: 0x4a5f7f,       // Dunkles Blau (Nekro-Touch)
    description: "Gefrorene Tundra mit nekromantischen Energien"
  },

  "Salzwind-Küste": {
    // Küsten-Biom
    terrain: 0xd4a574,      // Sand
    sand: 0xe8c9a0,         // Heller Sand
    water: 0x2196f3,        // Meerwasser
    accent: 0x64b5f6,       // Hellblau
    description: "Sandstrände und Klippen am Meer"
  },

  "Blitzebene": {
    // Hochebene-Biom
    terrain: 0x8b7355,      // Braune Erde
    grass: 0xa89968,        // Gelbliches Gras
    rock: 0x696969,         // Graue Felsen
    accent: 0xffeb3b,       // Gelb (Blitz!)
    description: "Weite Hochebene mit Gewittern"
  },

  "Grünschlamm-Sumpf": {
    // Sumpf-Biom
    terrain: 0x4a5d3f,      // Dunkelgrün-Braun
    water: 0x5c6e4a,        // Schlamm-Grün
    grass: 0x6b7c5a,        // Sumpfgras
    accent: 0x7d8c6d,       // Moosig
    description: "Sumpfland mit giftigem Nebel"
  },

  "Magmaströme": {
    // Vulkan-Biom
    terrain: 0x2f1f1f,      // Schwarzes Vulkangestein
    lava: 0xff5722,         // Orange Lava
    rock: 0x3f2f2f,         // Dunkles Gestein
    accent: 0xff6f00,       // Feuerorange
    description: "Vulkanische Landschaft mit Lavaflüssen"
  },

  "Heiße Dünen": {
    // Wüsten-Biom
    terrain: 0xd4a960,      // Sandgelb
    sand: 0xe8c88d,         // Heller Sand
    rock: 0xa67c52,         // Sandstein
    accent: 0xffca28,       // Goldgelb
    description: "Endlose Wüste mit Sanddünen"
  },

  "Tiefenhöhlen": {
    // Underground-Biom
    terrain: 0x2f2f2f,      // Dunkles Grau
    rock: 0x4a4a4a,         // Fels
    crystal: 0x9c27b0,      // Lila Kristalle
    accent: 0x6a4a6a,       // Dunkellila
    description: "Unterirdisches Höhlensystem"
  },

  "Götterfels": {
    // Zentrum (gehört zu ALLEN Regionen)
    terrain: 0x8b8b8b,      // Neutrales Grau
    rock: 0xa0a0a0,         // Heller Stein
    accent: 0xffd700,       // Gold (göttlich!)
    description: "Heiliger Berg im Zentrum der Welt"
  }
};
```

---

### Teil 2: VEGETATION

**Vegetation-Typen pro Biom:**

```javascript
const VEGETATION = {
  "Samtmoos-Tiefwald": {
    trees: {
      density: 0.15,      // 15% der Fläche
      models: [
        "assets/models/3d_models/tree_oak.glb",
        "assets/models/3d_models/tree_pine.glb"
      ],
      scale: [2, 4],      // Zufällig zwischen 2x und 4x
      rotation: "random"
    },
    bushes: {
      density: 0.08,      // 8% der Fläche
      models: ["assets/models/3d_models/bush.glb"],
      scale: [0.5, 1.5]
    },
    grass: {
      density: 0.30,      // 30% Gras
      color: 0x3a6b1f
    }
  },

  "Reich der Drei": {
    trees: {
      density: 0.03,      // Wenige Bäume (Eis!)
      models: ["assets/models/3d_models/tree_dead.glb"],
      scale: [1.5, 3],
      tint: 0xcccccc      // Grau/weiß getönt
    },
    rocks: {
      density: 0.12,
      models: ["assets/models/3d_models/rock_ice.glb"],
      scale: [1, 3]
    },
    snow: {
      density: 0.40,      // Viel Schnee!
      color: 0xffffff
    }
  },

  "Salzwind-Küste": {
    trees: {
      density: 0.05,
      models: ["assets/models/3d_models/palm.glb"],
      scale: [2, 5]
    },
    rocks: {
      density: 0.10,
      models: ["assets/models/3d_models/rock.glb"],
      scale: [1, 2.5]
    },
    grass: {
      density: 0.15,
      color: 0xa89968     // Stranggras
    }
  },

  "Blitzebene": {
    trees: {
      density: 0.02,      // Sehr wenige Bäume (Ebene!)
      models: ["assets/models/3d_models/tree_oak.glb"],
      scale: [2, 3]
    },
    rocks: {
      density: 0.08,
      models: ["assets/models/3d_models/rock.glb"],
      scale: [1.5, 3]
    },
    grass: {
      density: 0.25,
      color: 0xa89968
    }
  },

  "Grünschlamm-Sumpf": {
    trees: {
      density: 0.10,
      models: ["assets/models/3d_models/tree_dead.glb"],
      scale: [2, 4],
      tint: 0x4a5d3f      // Grünlich
    },
    bushes: {
      density: 0.15,
      models: ["assets/models/3d_models/bush.glb"],
      scale: [0.8, 2],
      tint: 0x5c6e4a
    },
    grass: {
      density: 0.20,
      color: 0x6b7c5a
    }
  },

  "Magmaströme": {
    trees: {
      density: 0.01,      // Fast keine Bäume (Vulkan!)
      models: ["assets/models/3d_models/tree_dead.glb"],
      scale: [1, 2],
      tint: 0x2f1f1f      // Verbrannt schwarz
    },
    rocks: {
      density: 0.20,      // Viele Felsen!
      models: ["assets/models/3d_models/rock.glb"],
      scale: [1, 4],
      tint: 0x3f2f2f
    },
    lava: {
      density: 0.05,      // Lava-Pools (später)
      color: 0xff5722
    }
  },

  "Heiße Dünen": {
    trees: {
      density: 0.005,     // Kaum Bäume (Wüste!)
      models: ["assets/models/3d_models/palm.glb"],
      scale: [2, 4]
    },
    rocks: {
      density: 0.08,
      models: ["assets/models/3d_models/rock.glb"],
      scale: [1, 3],
      tint: 0xa67c52      // Sandstein
    },
    cacti: {
      density: 0.03,
      models: ["assets/models/3d_models/cactus.glb"],  // Falls vorhanden
      scale: [1, 2.5]
    }
  },

  "Tiefenhöhlen": {
    trees: null,          // Keine Bäume (Underground!)
    rocks: {
      density: 0.25,      // Viele Felsen!
      models: ["assets/models/3d_models/rock.glb"],
      scale: [1, 5],
      tint: 0x2f2f2f
    },
    crystals: {
      density: 0.05,
      models: ["assets/models/3d_models/crystal.glb"],  // Falls vorhanden
      scale: [0.5, 2],
      tint: 0x9c27b0      // Lila
    }
  },

  "Götterfels": {
    trees: {
      density: 0.08,
      models: ["assets/models/3d_models/tree_oak.glb"],
      scale: [2, 4]
    },
    rocks: {
      density: 0.15,
      models: ["assets/models/3d_models/rock.glb"],
      scale: [1.5, 4],
      tint: 0xa0a0a0      // Heller Stein
    },
    grass: {
      density: 0.20,
      color: 0x7c9b6f
    }
  }
};
```

---

## 🔧 IMPLEMENTATION - SCHRITT FÜR SCHRITT

### Schritt 1: Öffne `world_generator.js`

**Pfad:** `C:\Najika_World\digivice\js\world_generator.js`

Finde die Funktion die das Terrain generiert. Wahrscheinlich heißt sie:
- `generateTerrain()`
- `createWorld()`
- `buildRegion()`
- Oder ähnlich

---

### Schritt 2: Farben-System implementieren

**Füge oben in der Datei hinzu:**

```javascript
// === BIOME FARBEN ===
const BIOME_COLORS = {
  "Samtmoos-Tiefwald": {
    terrain: 0x2d5016,
    grass: 0x3a6b1f,
    accent: 0x4a7c2f
  },
  "Reich der Drei": {
    terrain: 0xe8f4f8,
    snow: 0xffffff,
    ice: 0xb8d8e8,
    accent: 0x4a5f7f
  },
  "Salzwind-Küste": {
    terrain: 0xd4a574,
    sand: 0xe8c9a0,
    water: 0x2196f3,
    accent: 0x64b5f6
  },
  "Blitzebene": {
    terrain: 0x8b7355,
    grass: 0xa89968,
    rock: 0x696969,
    accent: 0xffeb3b
  },
  "Grünschlamm-Sumpf": {
    terrain: 0x4a5d3f,
    water: 0x5c6e4a,
    grass: 0x6b7c5a,
    accent: 0x7d8c6d
  },
  "Magmaströme": {
    terrain: 0x2f1f1f,
    lava: 0xff5722,
    rock: 0x3f2f2f,
    accent: 0xff6f00
  },
  "Heiße Dünen": {
    terrain: 0xd4a960,
    sand: 0xe8c88d,
    rock: 0xa67c52,
    accent: 0xffca28
  },
  "Tiefenhöhlen": {
    terrain: 0x2f2f2f,
    rock: 0x4a4a4a,
    crystal: 0x9c27b0,
    accent: 0x6a4a6a
  },
  "Götterfels": {
    terrain: 0x8b8b8b,
    rock: 0xa0a0a0,
    accent: 0xffd700
  }
};
```

---

### Schritt 3: Terrain-Farbe basierend auf Region setzen

**Finde die Stelle wo das Terrain-Material erstellt wird.**

Wahrscheinlich so etwas wie:
```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0x808080  // ← HIER ist das Problem! Alles grau!
});
```

**ÄNDERE zu:**

```javascript
function getTerrainMaterial(regionName) {
  const biomeColors = BIOME_COLORS[regionName];

  if (!biomeColors) {
    console.warn(`Unbekannte Region: ${regionName}, verwende Default`);
    return new THREE.MeshStandardMaterial({
      color: 0x808080
    });
  }

  return new THREE.MeshStandardMaterial({
    color: biomeColors.terrain,
    roughness: 0.8,
    metalness: 0.2
  });
}

// Verwendung:
const material = getTerrainMaterial(currentRegion.name);
```

---

### Schritt 4: Vegetation platzieren

**Erstelle neue Funktion:**

```javascript
function placeVegetation(region, scene) {
  const regionName = region.name;
  const vegetation = VEGETATION[regionName];

  if (!vegetation) {
    console.log(`Keine Vegetation für ${regionName}`);
    return;
  }

  // Region Bounds
  const bounds = getRegionBounds(region);

  // === BÄUME ===
  if (vegetation.trees && vegetation.trees.density > 0) {
    placeTreesInRegion(vegetation.trees, bounds, scene);
  }

  // === BÜSCHE ===
  if (vegetation.bushes && vegetation.bushes.density > 0) {
    placeBushesInRegion(vegetation.bushes, bounds, scene);
  }

  // === FELSEN ===
  if (vegetation.rocks && vegetation.rocks.density > 0) {
    placeRocksInRegion(vegetation.rocks, bounds, scene);
  }

  // === GRAS (Instanced Mesh für Performance) ===
  if (vegetation.grass && vegetation.grass.density > 0) {
    placeGrassInRegion(vegetation.grass, bounds, scene);
  }
}

function placeTreesInRegion(treeConfig, bounds, scene) {
  const {density, models, scale, rotation, tint} = treeConfig;

  // Berechne wie viele Bäume
  const area = (bounds.maxX - bounds.minX) * (bounds.maxZ - bounds.minZ);
  const treeCount = Math.floor(area * density);

  console.log(`Platziere ${treeCount} Bäume in Region`);

  // GLTFLoader (muss global verfügbar sein)
  const loader = new THREE.GLTFLoader();

  for (let i = 0; i < treeCount; i++) {
    // Zufällige Position innerhalb Bounds
    const x = bounds.minX + Math.random() * (bounds.maxX - bounds.minX);
    const z = bounds.minZ + Math.random() * (bounds.maxZ - bounds.minZ);

    // Höhe am Terrain (wichtig!)
    const y = getTerrainHeightAt(x, z);

    // Zufälliges Modell
    const modelPath = models[Math.floor(Math.random() * models.length)];

    // Lade Modell
    loader.load(modelPath, (gltf) => {
      const tree = gltf.scene;

      tree.position.set(x, y, z);

      // Zufällige Skalierung
      const s = scale[0] + Math.random() * (scale[1] - scale[0]);
      tree.scale.set(s, s, s);

      // Zufällige Rotation (wenn gewünscht)
      if (rotation === "random") {
        tree.rotation.y = Math.random() * Math.PI * 2;
      }

      // Tint (wenn vorhanden)
      if (tint) {
        tree.traverse((child) => {
          if (child.isMesh) {
            child.material = child.material.clone();
            child.material.color.setHex(tint);
          }
        });
      }

      scene.add(tree);
    });
  }
}

function getRegionBounds(region) {
  // Hole Bounds aus Region-Daten
  // Diese Funktion musst du basierend auf deinem bestehenden Code anpassen!

  // Beispiel (ANPASSEN!):
  return {
    minX: region.position.x - region.size / 2,
    maxX: region.position.x + region.size / 2,
    minZ: region.position.z - region.size / 2,
    maxZ: region.position.z + region.size / 2
  };
}

function getTerrainHeightAt(x, z) {
  // Hole Terrain-Höhe an Position (x, z)
  // Diese Funktion musst du basierend auf deinem bestehenden Code anpassen!

  // Beispiel (ANPASSEN!):
  // Raycasting nach unten
  const raycaster = new THREE.Raycaster();
  raycaster.set(
    new THREE.Vector3(x, 100, z),  // Von oben
    new THREE.Vector3(0, -1, 0)    // Nach unten
  );

  const intersects = raycaster.intersectObjects(scene.children, true);

  if (intersects.length > 0) {
    return intersects[0].point.y;
  }

  return 0;  // Fallback
}
```

---

### Schritt 5: Integration in Welt-Generierung

**Finde die Haupt-Generierungs-Funktion und füge hinzu:**

```javascript
async function generateWorld() {
  // ... Bestehender Code ...

  // Lade Regionen
  const regions = await loadRegions();  // Aus regions.json

  for (const region of regions) {
    // 1. Terrain mit korrekten Farben
    const material = getTerrainMaterial(region.name);
    const terrain = createTerrainMesh(region, material);
    scene.add(terrain);

    // 2. Vegetation platzieren
    placeVegetation(region, scene);

    console.log(`Region "${region.name}" generiert`);
  }
}
```

---

## ⚠️ FEHLER-VERMEIDUNG

### DO's:
- ✅ Verwende EXAKT die Region-Namen aus `regions.json`
- ✅ Teste mit Port 8001 (nicht 8000!)
- ✅ Console-Logs für Debugging
- ✅ Fehlerbehandlung (if (!region) return;)
- ✅ Performance beachten (nicht 10.000 Bäume!)
- ✅ Paths mit `/` (nicht `\`)

### DON'Ts:
- ❌ NICHT `assets` Pfad ändern (bleib bei `assets/models/...`)
- ❌ NICHT neue Region-Namen erfinden
- ❌ NICHT regions.json ändern
- ❌ NICHT zu viele Objekte auf einmal laden (Freeze!)
- ❌ NICHT hardcoded Pfade wie `C:\...`

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

✅ **Samtmoos-Tiefwald:** Dunkelgrün mit vielen Bäumen
✅ **Reich der Drei:** Weiß/Eisblau mit wenigen toten Bäumen
✅ **Salzwind-Küste:** Sandgelb mit Palmen
✅ **Blitzebene:** Braun mit wenigen Bäumen, viel Gras
✅ **Grünschlamm-Sumpf:** Dunkelgrün mit Büschen
✅ **Magmaströme:** Schwarz mit wenigen verbrannten Bäumen
✅ **Heiße Dünen:** Gelb mit Kakteen (falls vorhanden)
✅ **Tiefenhöhlen:** Dunkelgrau mit Felsen
✅ **Götterfels:** Grau mit goldenen Akzenten

---

### 3. Console-Checks:

```javascript
// Öffne Browser-Console (F12)
// Erwarte Logs wie:
// "Platziere 234 Bäume in Region Samtmoos-Tiefwald"
// "Region Salzwind-Küste generiert"
// etc.
```

---

### 4. Performance-Check:

- FPS sollte > 30 bleiben
- Keine Freezes beim Laden
- Wenn laggy: Density reduzieren!

---

## 📤 FERTIG? PUSH INS REPO!

### Wenn alles funktioniert:

```bash
git add digivice/js/world_generator.js
git add digivice/najika_world_v2.html  # Falls geändert
git commit -m "feat: Biome-Farben und Vegetation implementiert

- 8 Regionen haben jetzt biome-spezifische Farben
- Vegetation (Bäume, Büsche, Felsen) platziert
- Performance optimiert mit density controls
- Tested auf Port 8001"

git push
```

**Dann:** Ping Claude Code (CLI) im Chat dass du fertig bist!

---

## ❓ PROBLEME?

### Modelle laden nicht:

**Check:**
1. Pfad korrekt? `assets/models/3d_models/tree_oak.glb`
2. Datei existiert?
3. GLTFLoader importiert? `import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';`

### Performance-Issues:

**Lösung:**
- Reduziere `density` Werte
- Verwende Instanced Meshes für Gras
- LOD-System (später)

### Farben falsch:

**Check:**
- Region-Name richtig geschrieben?
- `BIOME_COLORS[regionName]` findet Region?

---

## 📚 REFERENZEN

- **regions.json:** `C:\Najika_World\digivice\data\regions.json`
- **Assets:** `C:\Najika_World\digivice\assets\models\3d_models\`
- **Fehler-Report:** `C:\Najika_World\WEB_MODEL_BUGFIX_REPORT.md`
- **Leitfaden:** `C:\Najika_World\CLAUDE_CODE_WEB_LEITFADEN.md`

---

**VIEL ERFOLG! Du schaffst das! 🎨🌲**

**Nach Push:** CLI übernimmt Review & Fix falls nötig!
