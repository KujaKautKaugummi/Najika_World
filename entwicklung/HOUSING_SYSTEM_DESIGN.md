# 🏗️ NAJIKA HOUSING SYSTEM - Fortnite Creative Inspired

**Erstellt:** 2025-11-07
**Inspiration:** Fortnite Creative, UEFN, Animal Crossing, Minecraft
**Status:** Design Phase
**Ziel:** Ultimatives Housing System auf dem Digivice

---

## 🎯 VISION

**"Baue dein eigenes Haus auf dem Digivice - komplett frei, wie in Fortnite Creative!"**

- **Vollständige Freiheit:** Platziere Wände, Böden, Dächer wo du willst
- **Grid-Based:** LEGO-Style Snap-to-Grid System
- **Massive Prop-Bibliothek:** Tausende von Möbeln, Deko, Materialien
- **Speichern/Laden:** Deine Builds bleiben gespeichert
- **Später in UEFN:** Direkte Integration ins Handyspiel

---

## 📦 CORE FEATURES

### 1. BUILD MODE (Fortnite Creative Style)

```yaml
Aktivierung:
  - Taste: B (Build Mode)
  - UI: Build-Menü öffnet sich
  - Kamera: Third-Person → Free-Cam (optional)

Features:
  - Grid Snapping (aktivierbar/deaktivierbar)
  - Rotation: 90° Steps (R-Taste)
  - Elevation: Y-Axis (Q/E Tasten)
  - Copy/Paste: Ctrl+C / Ctrl+V
  - Delete: X oder Delete
  - Undo/Redo: Ctrl+Z / Ctrl+Y
```

### 2. GRID SYSTEM (LEGO-Style)

```yaml
Grid-Größen:
  - Small: 0.5m x 0.5m (Kleine Deko)
  - Medium: 1m x 1m (Standard Möbel)
  - Large: 2m x 2m (Wände, Große Möbel)

Snapping:
  - Auto-Snap: Props snappen automatisch zu Grid
  - Free-Placement: Halte Shift für freies Platzieren
  - Surface-Snap: Props snappen zu Oberflächen (Wände, Böden)

Collision:
  - Props können NICHT überlappen (optional deaktivierbar)
  - Rote Outline bei ungültiger Platzierung
```

### 3. PROP KATEGORIEN (wie Fortnite)

```yaml
1. STRUCTURE (Basis-Bau):
   - Walls (Wände)
   - Floors (Böden)
   - Roofs (Dächer)
   - Stairs (Treppen)
   - Doors (Türen)
   - Windows (Fenster)

2. FURNITURE (Möbel):
   - Beds (Betten)
   - Tables (Tische)
   - Chairs (Stühle)
   - Shelves (Regale)
   - Cabinets (Schränke)
   - Sofas

3. DECORATION (Deko):
   - Paintings (Gemälde)
   - Plants (Pflanzen)
   - Rugs (Teppiche)
   - Lamps (Lampen)
   - Vases (Vasen)
   - Books

4. FUNCTIONAL (Funktional):
   - Crafting Stations
   - Storage Chests
   - Cooking Stoves
   - Beds (Sleep-Funktion)
   - Garden Plots

5. LIGHTING (Beleuchtung):
   - Torches
   - Lamps
   - Chandeliers
   - Candles
   - Colored Lights

6. SPECIAL (Spezial):
   - Najika Statues
   - Magic Items
   - Quest Items
   - Trophies
   - Easter Eggs
```

### 4. MATERIAL SYSTEM

```yaml
Konzept:
  - Props haben Material-Varianten
  - Wie Fortnite: Wood/Brick/Metal

Materials:
  - Wood (Holz)
  - Stone (Stein)
  - Metal (Metall)
  - Glass (Glas)
  - Fabric (Stoff)
  - Magic (Magisch - glows!)

Example:
  Wall_Wood → Wall_Stone → Wall_Metal
  (Gleiche Form, andere Textur)
```

### 5. UI DESIGN (Fortnite-inspiriert)

```yaml
Build-Menü (Linke Seite):
┌─────────────────────┐
│ 🏗️ BUILD MODE       │
├─────────────────────┤
│ [Structure] ▼       │  ← Dropdown
│   ├─ Walls          │
│   ├─ Floors         │
│   └─ Roofs          │
│                     │
│ [Furniture] ▼       │
│   ├─ Beds           │
│   ├─ Tables         │
│   └─ Chairs         │
│                     │
│ [Decoration] ▼      │
├─────────────────────┤
│ 🔍 Search...        │  ← Suche
├─────────────────────┤
│ [Grid: ON]   [R]    │  ← Rotation
│ [Snap: ON]   [X]    │  ← Delete
└─────────────────────┘

Prop-Grid (Rechte Seite):
┌─────────────────────┐
│  Props (36 Slots)   │
├─────────────────────┤
│ [🪑] [🛏️] [🪴] [🕯️] │  ← Icons
│ [📚] [🖼️] [🧺] [🪟] │
│ [🚪] [🪜] [🗄️] [🛋️] │
│ ... (mehr Slots)    │
└─────────────────────┘

Control-Info (Unten):
┌─────────────────────┐
│ B: Exit Build Mode  │
│ R: Rotate (90°)     │
│ Q/E: Elevation      │
│ X: Delete           │
│ Space: Place        │
└─────────────────────┘
```

---

## 🔧 TECHNISCHE IMPLEMENTATION

### Grid Placement System (Three.js)

```javascript
class GridPlacementSystem {
  constructor(scene) {
    this.scene = scene;
    this.gridSize = 1.0; // 1 Meter
    this.currentProp = null;
    this.ghostProp = null; // Preview
    this.snapToGrid = true;
    this.placedProps = [];
  }

  // Snap Position zu Grid
  snapPosition(position) {
    if (!this.snapToGrid) return position;

    return {
      x: Math.round(position.x / this.gridSize) * this.gridSize,
      y: Math.round(position.y / this.gridSize) * this.gridSize,
      z: Math.round(position.z / this.gridSize) * this.gridSize
    };
  }

  // Platziere Prop
  placeProp(propType, position, rotation = 0) {
    const snappedPos = this.snapPosition(position);

    // Check Collision
    if (this.checkCollision(snappedPos, propType)) {
      return { ok: false, msg: "Platz ist belegt!" };
    }

    // Create Prop
    const prop = this.createProp(propType, snappedPos, rotation);
    this.placedProps.push(prop);
    this.scene.add(prop);

    return { ok: true, prop: prop };
  }

  // Check Collision
  checkCollision(position, propType) {
    const bbox = this.getPropBoundingBox(propType);

    for (const placed of this.placedProps) {
      const placedBBox = placed.geometry.boundingBox;
      if (this.boundingBoxesOverlap(bbox, placedBBox)) {
        return true; // Collision!
      }
    }
    return false;
  }

  // Ghost Preview (transparent prop vor placement)
  updateGhostProp(position, rotation) {
    const snappedPos = this.snapPosition(position);

    if (!this.ghostProp) {
      this.ghostProp = this.createGhostProp(this.currentProp);
      this.scene.add(this.ghostProp);
    }

    this.ghostProp.position.set(snappedPos.x, snappedPos.y, snappedPos.z);
    this.ghostProp.rotation.y = rotation;

    // Färbe rot bei Collision
    const hasCollision = this.checkCollision(snappedPos, this.currentProp);
    this.ghostProp.material.color.set(hasCollision ? 0xff0000 : 0x00ff00);
  }
}
```

### Prop-Bibliothek (JSON)

```json
{
  "props": {
    "wall_wood": {
      "id": "wall_wood",
      "category": "structure",
      "name": "Wooden Wall",
      "model": "assets/props/wall_wood.glb",
      "size": [1, 2, 0.1],
      "cost": 10,
      "material": "wood",
      "variants": ["wall_stone", "wall_metal"]
    },
    "bed_simple": {
      "id": "bed_simple",
      "category": "furniture",
      "name": "Simple Bed",
      "model": "assets/props/bed_simple.glb",
      "size": [2, 1, 1],
      "cost": 50,
      "functional": true,
      "action": "sleep"
    },
    "lamp_torch": {
      "id": "lamp_torch",
      "category": "lighting",
      "name": "Torch",
      "model": "assets/props/torch.glb",
      "size": [0.5, 1.5, 0.5],
      "cost": 5,
      "light": {
        "color": 0xffa500,
        "intensity": 0.8,
        "radius": 10
      }
    }
  }
}
```

### Save/Load System

```javascript
class HousingSaveSystem {
  // Save Build
  saveBuild(name) {
    const buildData = {
      name: name,
      timestamp: Date.now(),
      props: this.placedProps.map(prop => ({
        type: prop.userData.type,
        position: prop.position.toArray(),
        rotation: prop.rotation.toArray(),
        scale: prop.scale.toArray(),
        material: prop.userData.material
      }))
    };

    // Save zu LocalStorage
    localStorage.setItem(`najika_build_${name}`, JSON.stringify(buildData));

    // Optional: Save zu Backend
    fetch('/api/housing/save', {
      method: 'POST',
      body: JSON.stringify(buildData)
    });

    return { ok: true, msg: `Build "${name}" gespeichert!` };
  }

  // Load Build
  loadBuild(name) {
    const data = localStorage.getItem(`najika_build_${name}`);
    if (!data) return { ok: false, msg: "Build nicht gefunden!" };

    const buildData = JSON.parse(data);

    // Clear current
    this.clearAllProps();

    // Place all props
    for (const propData of buildData.props) {
      this.placeProp(
        propData.type,
        propData.position,
        propData.rotation[1] // Y-rotation
      );
    }

    return { ok: true, msg: `Build "${name}" geladen!` };
  }
}
```

---

## 🎨 PROP PROGRESSION SYSTEM

### Unlock System (Stardew Valley Style)

```yaml
Concept:
  - Props werden durch Spielfortschritt freigeschaltet
  - Crafting, Quests, Achievements

Unlock-Methods:
  1. Craften:
     - Craft "Wooden Table" → Unlock "Wooden Chair"

  2. Kaufen:
     - Shop in Stadt (Gold)

  3. Finden:
     - Loot in Dungeons

  4. Quests:
     - NPC-Quests belohnen mit Props

  5. Achievements:
     - "Build your first house" → Unlock Decoration Pack

Example Progression:
  Level 1: Basic Wood Props
  Level 10: Stone Props unlocked
  Level 20: Metal Props unlocked
  Level 30: Magic Props unlocked
  Level 50: Legendary Props unlocked
```

---

## 🌟 SPECIAL FEATURES

### 1. THEMES (wie Animal Crossing)

```yaml
Themes:
  - Medieval (KayKit Dungeon)
  - Modern (Minimalist)
  - Japanese (Zen Garden)
  - Gothic (Dark Aesthetic - Najika!)
  - Fantasy (Magic Glow)
  - Sci-Fi (Futuristic)

One-Click Apply:
  - Wähle Theme → Alle Props werden im Theme-Stil platziert
  - Oder: Manuelles Mischen von Themes
```

### 2. ROOMS (vordefinierte Layouts)

```yaml
Pre-Built Rooms:
  - Bedroom (fertig eingerichtet)
  - Kitchen
  - Bathroom
  - Living Room
  - Workshop
  - Training Room

Usage:
  - Wähle "Bedroom Template" → Platziere als Ganzes
  - Dann: Individual Props anpassen
```

### 3. SHARE BUILDS (Community)

```yaml
Concept:
  - Spieler können Builds exportieren (JSON)
  - Upload zu Community-Server
  - Andere Spieler können downloaden

Features:
  - Rating System (⭐⭐⭐⭐⭐)
  - Tags (Gothic, Modern, Cozy, etc.)
  - Search & Filter
  - Featured Builds

Example:
  "Download Najika's Gothic Castle by User123"
  → Click → Load → Enjoy!
```

### 4. UEFN INTEGRATION (später)

```yaml
Ziel:
  - Housing-System wird nach UEFN portiert
  - Gleiche Props, gleiches System
  - Builds vom Digivice → Fortnite übertragbar!

Process:
  1. Digivice: Build erstellen
  2. Export als JSON
  3. UEFN Script: Liest JSON
  4. Props werden in Fortnite platziert
  5. Fertig!
```

---

## 📊 UMFANG (MVP → Full)

### MVP (Minimum Viable Product)

```yaml
Benötigt für ersten Release:
  ✅ Grid Placement System
  ✅ 50 Basic Props (Wände, Böden, Möbel)
  ✅ Build Mode UI
  ✅ Save/Load System
  ✅ 3 Material-Varianten (Wood/Stone/Metal)

Features:
  - Platziere Props
  - Rotiere Props
  - Delete Props
  - Speichere Build
  - Lade Build
```

### FULL VERSION

```yaml
Ziel für vollständiges System:
  ✅ 500+ Props (massive Bibliothek)
  ✅ 10+ Themes
  ✅ Room Templates
  ✅ Unlock Progression
  ✅ Share Community Builds
  ✅ UEFN Integration

Features:
  - Alles vom MVP
  - + Copy/Paste
  - + Undo/Redo
  - + Multi-Select
  - + Terrain Editing
  - + Custom Textures
  - + Lighting System
```

---

## 🔗 INTEGRATION MIT ANDEREN SYSTEMEN

### 1. Mit Farming System

```yaml
Props:
  - Garden Plot (platzierbar)
  - Watering Can Stand
  - Scarecrow
  - Greenhouse (größeres Gebäude)

Features:
  - Platziere Garden Plots überall
  - Pflanzen wachsen wie im Farming System
  - Automatisierung durch Props (Sprinkler)
```

### 2. Mit Fishing System

```yaml
Props:
  - Fishing Dock (baue eigenen Angelplatz)
  - Fish Tank (Display gefangene Fische)
  - Aquarium (decorativ)

Features:
  - Angelplätze custom platzieren
  - Fische als Deko ausstellen
```

### 3. Mit Crafting System

```yaml
Props:
  - Crafting Tables (verschiedene Typen)
  - Furnace (Schmelzen)
  - Alchemy Lab
  - Enchanting Table

Features:
  - Crafting-Stationen bauen
  - Upgrade-System (bessere Rezepte mit besseren Tischen)
```

---

## 🎯 DEVELOPMENT ROADMAP

### Phase 1: Core System (2 Wochen)
```yaml
- [ ] Grid Placement implementieren
- [ ] Basic Prop Loading (10 Props)
- [ ] Build Mode UI (einfach)
- [ ] Place/Rotate/Delete
- [ ] Save/Load (LocalStorage)
```

### Phase 2: Prop Library (2 Wochen)
```yaml
- [ ] 50 Props modellieren/importieren
- [ ] Material-System
- [ ] Kategorien-UI
- [ ] Search-Funktion
```

### Phase 3: Advanced Features (2 Wochen)
```yaml
- [ ] Copy/Paste
- [ ] Undo/Redo
- [ ] Collision Detection
- [ ] Ghost Preview
- [ ] Themes
```

### Phase 4: Integration (1 Woche)
```yaml
- [ ] Farming Integration
- [ ] Fishing Integration
- [ ] Crafting Integration
- [ ] Backend API
```

### Phase 5: Community Features (optional)
```yaml
- [ ] Share System
- [ ] Rating System
- [ ] Community-Server
- [ ] Featured Builds
```

---

## 📝 NOTES & IDEAS

- **Performance:** LOD System für weit entfernte Props (wie UEFN)
- **Mobile:** Touch-Controls für Build Mode (wichtig!)
- **VR:** Später VR-Support? (Hand-tracking für Platzierung)
- **AI:** Najika kann Build-Tipps geben ("Das sieht gemütlich aus!")
- **Seasons:** Saisonale Props (Weihnachten, Halloween, etc.)

---

**Status:** Design Complete ✅
**Next Step:** Implementation in `/entwicklung/housing_system/`
**Inspiration:** Fortnite Creative, UEFN, Animal Crossing, Stardew Valley

---

*"Najika sagt: 'Bau dein eigenes Zuhause, Mr. K! Aber nicht zu viel Explosion-Deko, okay?'"* 💥🏠
