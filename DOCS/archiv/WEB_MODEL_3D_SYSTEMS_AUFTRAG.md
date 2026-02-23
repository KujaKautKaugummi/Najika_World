# 🎮 WEB MODEL AUFTRAG: 3D-Systeme für UI-Module

**Erstellt:** 2025-11-23
**Priorität:** HOCH
**Für:** Neues Claude Code Web Model
**Geschätzte Dauer:** 3-5 Tage autonome Arbeit

---

## 📋 PROJEKT-KONTEXT

### **Aktuelle Situation:**

Najika World hat aktuell **8 Game-Systeme**, die als **Button-basierte UI-Module** implementiert sind:

```
AKTUELL (Button-UI):
1. 🎲 Dice Monsters       → Button öffnet Modal
2. 🏰 Region Boss         → Button öffnet Modal
3. 🎵 Instruments         → Button öffnet Modal (GERADE FERTIG!)
4. 🌍 World Info          → Button öffnet Modal
5. 🏠 Housing             → Button öffnet Modal
6. 🃏 Triple Triad        → Button öffnet Modal (GUT SO!)
7. 🐌 Slime Companion     → Button öffnet Modal (GUT SO!)
8. 🚂 Oregon Events       → Button öffnet Modal (GUT SO!)
```

### **Problem:**

Einige dieser Systeme **SOLLTEN 3D sein**, nicht nur Button-basiert, um die Immersion zu verbessern:

```
🟢 GUT ALS BUTTON:
✅ Triple Triad         → Kartenspiel braucht Modal
✅ Slime Companion      → Pet-UI ist OK als Modal
✅ Oregon Events        → Text-Events sind OK als Modal

🟡 KÖNNTE 3D SEIN:
❓ Dice Monsters        → 3D-Würfel würden besser passen
❓ Region Boss          → Map-Marker in Open World besser?
❓ Instruments          → 3D-Animation (Najika spielt)?
❓ World Info           → HUD statt Button?
❓ Housing              → Hybrid (Modal + 3D-Platzierung)?
```

---

## 🎯 DEINE AUFGABE (WEB MODEL)

Du sollst **5 Systeme von Button-UI zu 3D-Integration umbauen**:

### **PHASE 1: Dice Monsters → 3D-Würfel** (Tag 1-2)
### **PHASE 2: Region Boss → Map-Marker** (Tag 2-3)
### **PHASE 3: Instruments → 3D-Animation** (Tag 3-4)
### **PHASE 4: World Info → HUD-System** (Tag 4)
### **PHASE 5: Housing → Hybrid-System** (Tag 5)

---

## ⚠️ WICHTIGE REGELN (LIES ZUERST!)

### **✅ DU DARFST:**

```
✅ Kein Token-Limit - Schreibe komplette Files!
✅ Autonom arbeiten - Frage nicht nach Erlaubnis!
✅ Neue 3D-Systeme schreiben (1000+ Zeilen OK!)
✅ Vorhandene UI-Module ERWEITERN (nicht löschen!)
✅ Neue Three.js Meshes/Geometries erstellen
✅ Neue Event-Listener hinzufügen
✅ Neue CSS/HTML für 3D-Overlays schreiben
✅ Committe nach jedem Milestone
✅ Schreibe tägliche Progress Reports
```

### **❌ DU DARFST NICHT:**

```
❌ NIEMALS funktionierende Systeme kaputt machen!
❌ NIEMALS vorhandenen Backend-Code ändern (nur lesen!)
❌ NIEMALS UE5 Editor öffnen (macht lokales Model)
❌ NIEMALS kompilieren (macht lokales Model)
❌ NIEMALS die vorhandenen Button-UIs LÖSCHEN (nur ergänzen!)
❌ NIEMALS raten oder erfinden - nutze vorhandene Design-Specs!
```

### **📚 PFLICHTLEKTÜRE VOR START:**

Du **MUSST** diese Dateien lesen bevor du anfängst:

1. `C:\Najika_World\NEU_WEB_MODEL_PROJEKT_KOMPLETT.md`
   → Komplette Projekt-Übersicht (850+ Zeilen)

2. `C:\Najika_World\WEB_MODEL_START_INSTRUCTIONS.md`
   → Web Model Verhaltensregeln (89 Zeilen)

3. `C:\Najika_World\info material\web model 1 komplet .txt`
   → Komplette Session vom ersten Web Model (2.1 MB!)
   → Zeigt wie ein Web Model arbeiten sollte

4. `C:\Najika_World\digivice\js\3d_scene.js`
   → Main Engine (2500+ Zeilen) - VERSTEHE DEN CODE!

5. `C:\Najika_World\digivice\js\instrument_player.js`
   → Frisch implementiertes Instrument-System (570+ Zeilen)
   → GUTES BEISPIEL für Modal-UI!

6. `C:\Najika_World\digivice\index.html`
   → Haupt-UI (2400+ Zeilen) - VERSTEHE DIE STRUKTUR!

---

## 🔨 PHASE 1: DICE MONSTERS → 3D-WÜRFEL

### **📊 Aktueller Status:**

**Vorhanden:**
- `digivice/js/ddm.js` - Dungeon Dice Monsters Logik
- `digivice/js/ui/dice_monsters_ui.js` - Button-UI
- `backend/api/dice_monsters.py` - Backend API

**Problem:**
- Würfel werden als 2D-Grid dargestellt
- Keine 3D-Visualisierung

### **🎯 Ziel:**

```
VORHER:                    NACHHER:
┌─────────────┐           ┌─────────────┐
│ [Roll Dice] │    →      │  🎲 🎲 🎲  │ (echte 3D-Würfel)
│  Grid: □□□  │           │   rolling   │ (Three.js Animation)
└─────────────┘           └─────────────┘
```

### **📝 Implementation Plan:**

#### **Schritt 1.1: Neue Datei erstellen** (200-300 Zeilen)

**Pfad:** `digivice/js/3d_dice_system.js`

**Features:**
```javascript
class DiceSystem3D {
  constructor(scene) {
    this.scene = scene;
    this.activeDice = [];
    this.dicePhysics = null;  // Optional: Cannon.js Physics
  }

  /**
   * Erstelle 3D-Würfel
   * @param {number} count - Anzahl Würfel
   * @param {Vector3} position - Spawn Position
   * @returns {Array<Mesh>} Gewürfelte Würfel
   */
  rollDice(count, position) {
    // 1. Erstelle Three.js BoxGeometry für jeden Würfel
    // 2. Texturen für Würfelseiten (1-6 Punkte)
    // 3. Rotation Animation (Random Spin)
    // 4. Landen auf zufälliger Zahl
    // 5. Return Ergebnisse [4, 2, 6, ...]
  }

  /**
   * Entferne Würfel nach Animation
   */
  clearDice() {
    // Dispose Geometries & Materials
    // Remove from scene
  }

  /**
   * Update (call every frame)
   */
  update(deltaTime) {
    // Animate rolling dice
  }
}
```

**Texturen:**
- Erstelle Canvas-basierte Würfelseiten (1-6 Punkte)
- Oder nutze vorhandene KayKit Textures

#### **Schritt 1.2: Integration in 3d_scene.js** (50 Zeilen)

**Wo:** Nach Zeile 49 (nach `let enemySystem;`)

```javascript
import DiceSystem3D from './3d_dice_system.js';

// After line 49
let diceSystem3D;

// In init() function, after enemySystem init
diceSystem3D = new DiceSystem3D(scene);
```

**In animate() loop:**
```javascript
if (diceSystem3D) diceSystem3D.update(deltaTime);
```

#### **Schritt 1.3: Erweitere dice_monsters_ui.js** (100 Zeilen)

**Wo:** In der `rollDice()` Funktion

**VORHER:**
```javascript
rollDice() {
  // Zeige Grid mit Zahlen
  this.updateGrid([4, 2, 6]);
}
```

**NACHHER:**
```javascript
rollDice() {
  // 1. Triggere 3D-Würfel Animation
  if (window.diceSystem3D) {
    const results = window.diceSystem3D.rollDice(3, playerPosition);

    // 2. Warte auf Animation Ende (2 Sekunden)
    setTimeout(() => {
      this.updateGrid(results);  // Zeige Ergebnis
    }, 2000);
  } else {
    // Fallback: Alte 2D-Methode
    this.updateGrid([4, 2, 6]);
  }
}
```

#### **Schritt 1.4: Testing** (1 Stunde)

1. Öffne `digivice/index.html`
2. Klicke "🎲 Dice Monsters"
3. Teste Roll-Funktion
4. Prüfe:
   - ✅ Würfel spawnen korrekt
   - ✅ Animation läuft smooth (60 FPS)
   - ✅ Ergebnisse stimmen
   - ✅ Würfel verschwinden nach Nutzung

#### **Schritt 1.5: Commit**

```bash
git add digivice/js/3d_dice_system.js
git add digivice/js/3d_scene.js
git add digivice/js/ui/dice_monsters_ui.js
git commit -m "✨ ADD: 3D-Würfel System für Dice Monsters

- Neue Datei: 3d_dice_system.js (300 Zeilen)
- Integration in 3d_scene.js
- Erweitert dice_monsters_ui.js mit 3D-Trigger
- Canvas-basierte Würfelseiten-Texturen
- Rotation Animation mit easing
- Auto-clear nach 2 Sekunden

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 🔨 PHASE 2: REGION BOSS → MAP-MARKER

### **📊 Aktueller Status:**

**Vorhanden:**
- `digivice/js/ui/region_boss_ui.js` - Button-UI
- `backend/api/arena.py` - Nemesis Arena Backend
- `digivice/js/world/world_manager.js` - Open World System

**Problem:**
- Boss-System ist nur über Button erreichbar
- Keine Verbindung zur Open World

### **🎯 Ziel:**

```
VORHER:                       NACHHER:
Digivice UI:                  Open World Map:
┌─────────────┐
│ [Boss Arena]│       →       🗺️ Open World
└─────────────┘                  ├─ 🔴 Boss 1 (Götterfels)
                                 ├─ 🔴 Boss 2 (Crimson Desert)
                                 └─ 🔴 Boss 3 (Azure Coast)

User läuft in Open World zu Boss-Marker → E-Taste → Arena startet
```

### **📝 Implementation Plan:**

#### **Schritt 2.1: Boss-Spawn-Positionen definieren** (50 Zeilen)

**Datei:** `digivice/data/boss_spawns.json` (NEU)

```json
{
  "bosses": [
    {
      "id": "boss_goetterfels",
      "name": "Schattenritter",
      "region": "goetterfels",
      "position": { "x": 4900, "y": 0, "z": 4750 },
      "level": 10,
      "markerColor": "#ff0000",
      "arenaType": "nemesis_tier_1"
    },
    {
      "id": "boss_crimson_desert",
      "name": "Wüstentitan",
      "region": "crimson_desert",
      "position": { "x": 1200, "y": 0, "z": 1200 },
      "level": 25,
      "markerColor": "#ff4400",
      "arenaType": "nemesis_tier_2"
    }
    // ... 7 weitere Bosse (einer pro Region)
  ]
}
```

#### **Schritt 2.2: Boss-Marker System** (300 Zeilen)

**Datei:** `digivice/js/world/boss_marker_system.js` (NEU)

```javascript
class BossMarkerSystem {
  constructor(scene, worldManager) {
    this.scene = scene;
    this.worldManager = worldManager;
    this.markers = [];
    this.activeMarkers = new Map();
  }

  async loadBossData() {
    // Lade boss_spawns.json
    const response = await fetch('/digivice/data/boss_spawns.json');
    this.bossData = await response.json();
  }

  /**
   * Spawne Boss-Marker in der Welt
   */
  spawnMarkers() {
    this.bossData.bosses.forEach(boss => {
      // 1. Erstelle 3D-Marker (Glowing Sphere + Particle Effect)
      const markerMesh = this.createMarker(boss);

      // 2. Position setzen
      markerMesh.position.set(boss.position.x, boss.position.y + 5, boss.position.z);

      // 3. User Data setzen
      markerMesh.userData.bossData = boss;
      markerMesh.userData.interactable = true;
      markerMesh.userData.interactText = `[E] ${boss.name} herausfordern`;

      // 4. Zur Scene hinzufügen
      this.scene.add(markerMesh);
      this.activeMarkers.set(boss.id, markerMesh);
    });
  }

  /**
   * Erstelle einzelnen Boss-Marker
   */
  createMarker(bossData) {
    // 1. Glowing Sphere
    const geometry = new THREE.SphereGeometry(2, 16, 16);
    const material = new THREE.MeshStandardMaterial({
      color: bossData.markerColor,
      emissive: bossData.markerColor,
      emissiveIntensity: 0.5
    });
    const sphere = new THREE.Mesh(geometry, material);

    // 2. Particle System (optional)
    // ...

    // 3. Name Label (3D Text)
    const label = this.createLabel(bossData.name);
    sphere.add(label);

    return sphere;
  }

  /**
   * Check proximity & show E-Prompt
   */
  update(playerPosition) {
    this.activeMarkers.forEach((marker, bossId) => {
      const distance = playerPosition.distanceTo(marker.position);

      if (distance < 5) {
        // Zeige E-Prompt
        this.showInteractPrompt(marker.userData.bossData);
      }
    });

    // Animate markers (bob up/down, rotate)
    this.animateMarkers();
  }

  /**
   * User drückt E auf Boss-Marker
   */
  interactWithBoss(bossId) {
    const boss = this.bossData.bosses.find(b => b.id === bossId);

    // 1. Lade Arena
    // 2. Teleportiere User in Arena
    // 3. Starte Boss-Fight
    console.log(`Starting boss fight: ${boss.name}`);

    // Trigger RegionBossUI mit Arena-Typ
    if (window.regionBossUI) {
      window.regionBossUI.startBossFight(boss.arenaType);
    }
  }
}
```

#### **Schritt 2.3: Integration in world_manager.js** (50 Zeilen)

**Wo:** Nach Zeile 40 (nach LODManager init)

```javascript
import BossMarkerSystem from './boss_marker_system.js';

// After line 40
this.bossMarkerSystem = new BossMarkerSystem(scene, this);
```

**In initialize() Funktion:**
```javascript
// After line 100
await this.bossMarkerSystem.loadBossData();
this.bossMarkerSystem.spawnMarkers();
```

**In update() Funktion:**
```javascript
// After line 189
this.bossMarkerSystem.update(this.playerPosition);
```

#### **Schritt 2.4: E-Taste Interaction Handler** (50 Zeilen)

**Datei:** `digivice/js/3d_scene.js`

**Wo:** In der `handleKeyDown()` Funktion (Zeile 1627+)

**Erweitere E-Taste Handler:**

```javascript
// VORHER (nur Buildings):
if (e.key === 'e') {
  checkBuildingProximity();
}

// NACHHER (Buildings + Boss Markers):
if (e.key === 'e') {
  // 1. Check Buildings
  const building = checkBuildingProximity();

  // 2. Check Boss Markers
  if (!building && worldManager?.bossMarkerSystem) {
    const nearbyBoss = worldManager.bossMarkerSystem.getNearbyBoss(playerPosition);
    if (nearbyBoss) {
      worldManager.bossMarkerSystem.interactWithBoss(nearbyBoss.id);
      return;
    }
  }
}
```

#### **Schritt 2.5: UI-Button als Alternative behalten** (30 Zeilen)

**Wichtig:** Button-UI **NICHT löschen**, nur ergänzen!

**Datei:** `digivice/js/ui/region_boss_ui.js`

**Am Anfang der Datei einfügen:**

```javascript
// Hinweis: Dieses UI kann auch über Boss-Marker in Open World getriggert werden!
// Button-Zugriff bleibt als Backup/Alternative erhalten.
```

#### **Schritt 2.6: Testing** (1 Stunde)

1. Starte Open World
2. Teleportiere zu Götterfels: `worldManager.teleportToRegion('goetterfels')`
3. Laufe zum Boss-Marker (sollte sichtbar sein)
4. Prüfe:
   - ✅ Marker leuchtet
   - ✅ E-Prompt erscheint bei Nähe
   - ✅ E-Taste startet Boss-Fight
   - ✅ Arena lädt korrekt

#### **Schritt 2.7: Commit**

```bash
git add digivice/data/boss_spawns.json
git add digivice/js/world/boss_marker_system.js
git add digivice/js/world/world_manager.js
git add digivice/js/3d_scene.js
git commit -m "🏰 ADD: 3D Boss-Marker System in Open World

- Neue Datei: boss_spawns.json (9 Bosse, je 1 pro Region)
- Neue Datei: boss_marker_system.js (300 Zeilen)
- Integration in world_manager.js
- Erweitert E-Taste Handler für Boss-Interaktion
- Glowing Spheres mit Particle Effects
- Button-UI bleibt als Alternative erhalten

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 🔨 PHASE 3: INSTRUMENTS → 3D-ANIMATION

### **📊 Aktueller Status:**

**Vorhanden:**
- `digivice/js/instrument_player.js` - Instrument UI (FRISCH FERTIG! 570+ Zeilen)
- `digivice/index.html` - Button für Instrument
- Web Audio API für Sound

**Problem:**
- Instrument ist nur UI-Modal
- Keine 3D-Darstellung von Najika beim Spielen

### **🎯 Ziel:**

```
VORHER:                       NACHHER:
Button öffnet Modal    →      3D-Scene zeigt Najika mit Instrument
                              + Modal bleibt für Noten-Anzeige
                              + Animation sync mit gespielten Noten
```

**WICHTIG:** Instrument-UI **NICHT ersetzen**, nur **3D-Animation HINZUFÜGEN**!

### **📝 Implementation Plan:**

#### **Schritt 3.1: Najika-Instrument Animation** (200 Zeilen)

**Datei:** `digivice/js/najika_instrument_animator.js` (NEU)

```javascript
class NajikaInstrumentAnimator {
  constructor(scene, character) {
    this.scene = scene;
    this.character = character;  // Skeleton_Mage Model
    this.instrument = null;
    this.isPlaying = false;
  }

  /**
   * Lade Instrument-Model (z.B. Flöte/Harmonica)
   */
  async loadInstrument() {
    // Option 1: GLTF Model laden
    // Option 2: Einfache Geometrie (Box für Harmonica)

    const geometry = new THREE.BoxGeometry(0.3, 0.1, 0.05);
    const material = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    this.instrument = new THREE.Mesh(geometry, material);

    // Verstecken bis Spieler Instrument aktiviert
    this.instrument.visible = false;
    this.scene.add(this.instrument);
  }

  /**
   * Spiele Note (triggert Animation)
   */
  playNote(noteName) {
    if (!this.isPlaying) return;

    // 1. Instrument an Mund positionieren
    this.positionInstrument();

    // 2. Leichte Bewegung (Vibration beim Spielen)
    this.animateNotePlay(noteName);

    // 3. Particle Effect (optional)
    this.spawnNoteParticle(noteName);
  }

  /**
   * Positioniere Instrument vor Najika's Mund
   */
  positionInstrument() {
    if (!this.character) return;

    // Get character head position
    const headBone = this.character.skeleton?.getBoneByName('Head');
    if (headBone) {
      const headPos = new THREE.Vector3();
      headBone.getWorldPosition(headPos);

      this.instrument.position.copy(headPos);
      this.instrument.position.x += 0.2;  // Vor dem Mund
    }
  }

  /**
   * Start Instrument Playing
   */
  startPlaying() {
    this.isPlaying = true;
    this.instrument.visible = true;

    // Animation: Character hebt Instrument zum Mund
    // ...
  }

  /**
   * Stop Instrument Playing
   */
  stopPlaying() {
    this.isPlaying = false;
    this.instrument.visible = false;

    // Animation: Character senkt Instrument
    // ...
  }

  /**
   * Update (call every frame)
   */
  update(deltaTime) {
    if (this.isPlaying) {
      this.positionInstrument();
    }
  }
}
```

#### **Schritt 3.2: Integration in 3d_scene.js** (50 Zeilen)

**Wo:** Nach Character Load (Zeile 300+)

```javascript
import NajikaInstrumentAnimator from './najika_instrument_animator.js';

let najikaInstrumentAnimator;

// After character load (line 300+)
function onCharacterLoaded(gltf) {
  character = gltf.scene;
  // ... existing code ...

  // Init Instrument Animator
  najikaInstrumentAnimator = new NajikaInstrumentAnimator(scene, character);
  najikaInstrumentAnimator.loadInstrument();
}

// In animate() loop
if (najikaInstrumentAnimator) {
  najikaInstrumentAnimator.update(deltaTime);
}
```

#### **Schritt 3.3: Verbinde mit instrument_player.js** (50 Zeilen)

**Datei:** `digivice/js/instrument_player.js`

**WICHTIG:** Code **NICHT ersetzen**, nur **erweitern**!

**In playNote() Funktion (Zeile 120+):**

```javascript
// VORHER:
playNote(key) {
  const note = this.noteMapping[key];
  // ... Web Audio API code ...
}

// NACHHER:
playNote(key) {
  const note = this.noteMapping[key];
  // ... Web Audio API code ...

  // NEU: Triggere 3D-Animation
  if (window.najikaInstrumentAnimator) {
    window.najikaInstrumentAnimator.playNote(note.name);
  }
}
```

**In show() Funktion:**

```javascript
show() {
  // ... existing code ...

  // Starte 3D-Animation
  if (window.najikaInstrumentAnimator) {
    window.najikaInstrumentAnimator.startPlaying();
  }
}
```

**In hide() Funktion:**

```javascript
hide() {
  // ... existing code ...

  // Stoppe 3D-Animation
  if (window.najikaInstrumentAnimator) {
    window.najikaInstrumentAnimator.stopPlaying();
  }
}
```

#### **Schritt 3.4: Testing** (30 Minuten)

1. Öffne Digivice
2. Klicke "🎵 Instruments"
3. Spiele Noten (Q W E R T Y)
4. Prüfe:
   - ✅ Najika zeigt Instrument
   - ✅ Animation sync mit Sound
   - ✅ Instrument verschwindet beim Schließen

#### **Schritt 3.5: Commit**

```bash
git add digivice/js/najika_instrument_animator.js
git add digivice/js/3d_scene.js
git add digivice/js/instrument_player.js
git commit -m "🎵 ADD: 3D-Animation für Instrument System

- Neue Datei: najika_instrument_animator.js (200 Zeilen)
- Integration in 3d_scene.js
- Erweitert instrument_player.js mit Animation-Trigger
- Najika hebt Instrument beim Spielen
- Sync mit Web Audio API
- UI-Modal bleibt unverändert (nur ergänzt)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 🔨 PHASE 4: WORLD INFO → HUD-SYSTEM

### **📊 Aktueller Status:**

**Vorhanden:**
- `digivice/js/ui/world_map_ui.js` - Button-UI für World Info
- `digivice/js/world/world_manager.js` - World System

**Problem:**
- World Info nur über Button
- User muss Modal öffnen um Region zu sehen

### **🎯 Ziel:**

```
VORHER:                       NACHHER:
Button → Modal         →      HUD (oben rechts):
                              ┌─────────────────┐
                              │ 📍 Götterfels   │
                              │ Lv. 10 Region   │
                              │ Temp: 20°C      │
                              │ 🌞 12:30 Uhr    │
                              └─────────────────┘
```

### **📝 Implementation Plan:**

#### **Schritt 4.1: HUD System** (300 Zeilen)

**Datei:** `digivice/js/world/world_hud.js` (NEU)

```javascript
class WorldHUD {
  constructor(worldManager) {
    this.worldManager = worldManager;
    this.hudElement = null;
    this.updateInterval = null;
  }

  /**
   * Erstelle HUD HTML
   */
  createHUD() {
    this.hudElement = document.createElement('div');
    this.hudElement.id = 'world-hud';
    this.hudElement.innerHTML = `
      <div class="hud-section">
        <div class="hud-icon">📍</div>
        <div class="hud-text">
          <div id="hud-region">Loading...</div>
          <div id="hud-region-level">Lv. --</div>
        </div>
      </div>
      <div class="hud-section">
        <div class="hud-icon">🌡️</div>
        <div class="hud-text">
          <div id="hud-weather">--°C</div>
        </div>
      </div>
      <div class="hud-section">
        <div class="hud-icon">🌞</div>
        <div class="hud-text">
          <div id="hud-time">--:--</div>
        </div>
      </div>
      <div class="hud-section">
        <div class="hud-icon">📊</div>
        <div class="hud-text">
          <div id="hud-coords">X: -- Z: --</div>
        </div>
      </div>
    `;

    document.body.appendChild(this.hudElement);
  }

  /**
   * Erstelle HUD CSS
   */
  createStyles() {
    const style = document.createElement('style');
    style.textContent = `
      #world-hud {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        min-width: 200px;
        z-index: 1000;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
      }

      .hud-section {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
      }

      .hud-section:last-child {
        margin-bottom: 0;
      }

      .hud-icon {
        font-size: 20px;
        margin-right: 10px;
      }

      .hud-text {
        flex: 1;
      }

      .hud-text div {
        line-height: 1.4;
      }

      #hud-region {
        font-weight: bold;
        font-size: 16px;
      }

      #hud-region-level {
        font-size: 12px;
        color: #aaa;
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * Update HUD Data
   */
  update() {
    if (!this.worldManager || !this.worldManager.initialized) return;

    // 1. Current Region
    const currentRegion = this.worldManager.getCurrentRegion();
    if (currentRegion) {
      document.getElementById('hud-region').textContent = currentRegion.name;
      document.getElementById('hud-region-level').textContent = `Lv. ${currentRegion.level} Region`;
    }

    // 2. Weather (dummy for now)
    const temp = Math.floor(Math.random() * 30 + 10);
    document.getElementById('hud-weather').textContent = `${temp}°C`;

    // 3. Time (from day/night cycle)
    const time = this.getGameTime();
    document.getElementById('hud-time').textContent = time;

    // 4. Coordinates
    const pos = this.worldManager.playerPosition;
    document.getElementById('hud-coords').textContent =
      `X: ${Math.floor(pos.x)} Z: ${Math.floor(pos.z)}`;
  }

  /**
   * Get Game Time (from day/night cycle)
   */
  getGameTime() {
    // Check if dayNightCycle exists
    if (window.dayNightCycle) {
      const hours = Math.floor(window.dayNightCycle.timeOfDay * 24);
      const minutes = Math.floor((window.dayNightCycle.timeOfDay * 24 % 1) * 60);
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
    }
    return '--:--';
  }

  /**
   * Initialize HUD
   */
  init() {
    this.createStyles();
    this.createHUD();

    // Update every second
    this.updateInterval = setInterval(() => this.update(), 1000);

    // Initial update
    this.update();
  }

  /**
   * Toggle HUD visibility
   */
  toggle() {
    if (this.hudElement) {
      this.hudElement.style.display =
        this.hudElement.style.display === 'none' ? 'block' : 'none';
    }
  }

  /**
   * Dispose HUD
   */
  dispose() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
    if (this.hudElement) {
      this.hudElement.remove();
    }
  }
}

export default WorldHUD;
```

#### **Schritt 4.2: Integration in world_manager.js** (30 Zeilen)

**Wo:** Nach Zeile 41

```javascript
import WorldHUD from './world_hud.js';

// After line 41
this.worldHUD = null;
```

**In initialize() Funktion (nach Zeile 115):**

```javascript
// Init HUD
this.worldHUD = new WorldHUD(this);
this.worldHUD.init();
```

#### **Schritt 4.3: Toggle-Hotkey (H-Taste)** (20 Zeilen)

**Datei:** `digivice/js/3d_scene.js`

**In handleKeyDown() Funktion:**

```javascript
// H-Taste = Toggle HUD
if (e.key === 'h') {
  if (worldManager?.worldHUD) {
    worldManager.worldHUD.toggle();
  }
}
```

#### **Schritt 4.4: Button bleibt als Alternative** (10 Zeilen)

**Datei:** `digivice/index.html`

**Button-Text ändern:**

```html
<!-- VORHER -->
<button onclick="window.worldMapUI?.show()">🌍 World Info</button>

<!-- NACHHER -->
<button onclick="window.worldMapUI?.show()">🌍 World Map (Full)</button>
```

**Hinweis:** HUD zeigt Quick-Info, Button öffnet Full-Map mit Details.

#### **Schritt 4.5: Testing** (20 Minuten)

1. Starte Open World
2. HUD sollte automatisch oben rechts erscheinen
3. Prüfe:
   - ✅ Region-Name aktualisiert sich
   - ✅ Zeit läuft
   - ✅ Koordinaten ändern sich beim Laufen
   - ✅ H-Taste togglet HUD

#### **Schritt 4.6: Commit**

```bash
git add digivice/js/world/world_hud.js
git add digivice/js/world/world_manager.js
git add digivice/js/3d_scene.js
git add digivice/index.html
git commit -m "🌍 ADD: HUD-System für World Info (oben rechts)

- Neue Datei: world_hud.js (300 Zeilen)
- Integration in world_manager.js
- Auto-Update jede Sekunde
- Zeigt: Region, Level, Temp, Zeit, Koordinaten
- H-Taste togglet HUD
- Button bleibt als Full-Map-Alternative

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 🔨 PHASE 5: HOUSING → HYBRID-SYSTEM

### **📊 Aktueller Status:**

**Vorhanden:**
- `digivice/js/ui/housing_ui.js` - Button-UI
- `backend/api/housing.py` - Backend für Housing

**Problem:**
- Möbel nur in Modal-UI platzierbar
- Keine 3D-Preview in der Welt

### **🎯 Ziel:**

```
VORHER:                       NACHHER:
Button → Modal         →      Modal (Möbel auswählen)
→ Setze Möbel                    ↓
                              3D-Preview in Welt
                                 ↓
                              [E] Platzieren / [ESC] Abbrechen
```

**Hybrid:** UI für Auswahl, 3D für Platzierung.

### **📝 Implementation Plan:**

#### **Schritt 5.1: 3D-Möbel-Placement System** (400 Zeilen)

**Datei:** `digivice/js/housing_3d_placement.js` (NEU)

```javascript
class Housing3DPlacement {
  constructor(scene, camera) {
    this.scene = scene;
    this.camera = camera;
    this.isPlacementMode = false;
    this.previewMesh = null;
    this.selectedFurniture = null;
    this.placedFurniture = [];
  }

  /**
   * Start Placement Mode
   * @param {Object} furnitureData - Möbel-Daten aus UI
   */
  startPlacement(furnitureData) {
    this.isPlacementMode = true;
    this.selectedFurniture = furnitureData;

    // 1. Erstelle Preview-Mesh
    this.createPreviewMesh(furnitureData);

    // 2. Zeige Placement-Hinweise
    this.showPlacementHints();

    console.log(`Placement Mode: ${furnitureData.name}`);
  }

  /**
   * Erstelle Preview-Mesh (transparentes Möbel)
   */
  createPreviewMesh(furnitureData) {
    // Lade Möbel-Model oder erstelle Placeholder
    let geometry, material;

    switch(furnitureData.type) {
      case 'bed':
        geometry = new THREE.BoxGeometry(2, 0.5, 3);
        break;
      case 'table':
        geometry = new THREE.BoxGeometry(1.5, 0.8, 1.5);
        break;
      case 'chair':
        geometry = new THREE.BoxGeometry(0.5, 1, 0.5);
        break;
      default:
        geometry = new THREE.BoxGeometry(1, 1, 1);
    }

    material = new THREE.MeshStandardMaterial({
      color: 0x00ff00,
      transparent: true,
      opacity: 0.5,
      wireframe: false
    });

    this.previewMesh = new THREE.Mesh(geometry, material);
    this.previewMesh.userData.isPreview = true;
    this.scene.add(this.previewMesh);
  }

  /**
   * Update Preview Position (folgt Mauszeiger/Kamera)
   */
  update(playerPosition, playerRotation) {
    if (!this.isPlacementMode || !this.previewMesh) return;

    // Position vor dem Spieler (2 Meter)
    const offset = new THREE.Vector3(0, 0, -2);
    offset.applyQuaternion(playerRotation);

    this.previewMesh.position.copy(playerPosition);
    this.previewMesh.position.add(offset);
    this.previewMesh.position.y = 0.5;  // Auf Boden

    // Check Collision (optional)
    const canPlace = this.checkValidPlacement();

    // Farbe ändern basierend auf Validity
    this.previewMesh.material.color.setHex(canPlace ? 0x00ff00 : 0xff0000);
  }

  /**
   * Prüfe ob Platzierung gültig ist
   */
  checkValidPlacement() {
    if (!this.previewMesh) return false;

    // 1. Nicht zu nah an anderen Möbeln
    for (const furniture of this.placedFurniture) {
      const distance = this.previewMesh.position.distanceTo(furniture.position);
      if (distance < 1) return false;  // Mindestabstand 1m
    }

    // 2. Nicht außerhalb der Map
    const pos = this.previewMesh.position;
    if (pos.x < 0 || pos.x > 9600 || pos.z < 0 || pos.z > 9600) {
      return false;
    }

    return true;
  }

  /**
   * Platziere Möbel (E-Taste)
   */
  placeFurniture() {
    if (!this.canPlace()) return false;

    // 1. Konvertiere Preview zu echtem Möbel
    const realMaterial = new THREE.MeshStandardMaterial({
      color: 0x8b4513,
      transparent: false
    });

    const furniture = new THREE.Mesh(
      this.previewMesh.geometry.clone(),
      realMaterial
    );

    furniture.position.copy(this.previewMesh.position);
    furniture.rotation.copy(this.previewMesh.rotation);
    furniture.userData.furnitureData = this.selectedFurniture;

    this.scene.add(furniture);
    this.placedFurniture.push(furniture);

    // 2. Backend speichern
    this.saveFurnitureToBackend(furniture);

    // 3. Cleanup
    this.cancelPlacement();

    console.log(`Furniture placed: ${this.selectedFurniture.name}`);
    return true;
  }

  /**
   * Speichere Möbel in Backend
   */
  async saveFurnitureToBackend(furniture) {
    const data = {
      type: furniture.userData.furnitureData.type,
      position: {
        x: furniture.position.x,
        y: furniture.position.y,
        z: furniture.position.z
      },
      rotation: furniture.rotation.y
    };

    try {
      const response = await fetch('http://localhost:8000/api/housing/place', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        console.log('Furniture saved to backend');
      }
    } catch (error) {
      console.error('Failed to save furniture:', error);
    }
  }

  /**
   * Abbrechen (ESC-Taste)
   */
  cancelPlacement() {
    if (this.previewMesh) {
      this.scene.remove(this.previewMesh);
      this.previewMesh.geometry.dispose();
      this.previewMesh.material.dispose();
      this.previewMesh = null;
    }

    this.isPlacementMode = false;
    this.selectedFurniture = null;
    this.hidePlacementHints();
  }

  /**
   * Zeige Placement-Hinweise
   */
  showPlacementHints() {
    const hints = document.createElement('div');
    hints.id = 'placement-hints';
    hints.innerHTML = `
      <div style="position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%);
                  background: rgba(0,0,0,0.8); color: white; padding: 20px;
                  border-radius: 10px; text-align: center;">
        <div><strong>Möbel platzieren:</strong></div>
        <div style="margin-top: 10px;">
          [E] Platzieren | [R] Rotieren | [ESC] Abbrechen
        </div>
      </div>
    `;
    document.body.appendChild(hints);
  }

  /**
   * Verstecke Placement-Hinweise
   */
  hidePlacementHints() {
    const hints = document.getElementById('placement-hints');
    if (hints) hints.remove();
  }

  /**
   * Rotiere Preview (R-Taste)
   */
  rotateFurniture() {
    if (this.previewMesh) {
      this.previewMesh.rotation.y += Math.PI / 4;  // 45 Grad
    }
  }

  /**
   * Lade gespeicherte Möbel
   */
  async loadPlacedFurniture() {
    try {
      const response = await fetch('http://localhost:8000/api/housing/list');
      const data = await response.json();

      data.furniture.forEach(item => {
        // Erstelle Mesh aus gespeicherten Daten
        // ...
      });
    } catch (error) {
      console.error('Failed to load furniture:', error);
    }
  }
}

export default Housing3DPlacement;
```

#### **Schritt 5.2: Integration in 3d_scene.js** (50 Zeilen)

```javascript
import Housing3DPlacement from './housing_3d_placement.js';

let housing3DPlacement;

// After scene init
housing3DPlacement = new Housing3DPlacement(scene, camera);
housing3DPlacement.loadPlacedFurniture();

// In animate() loop
if (housing3DPlacement?.isPlacementMode) {
  housing3DPlacement.update(playerPosition, playerRotation);
}

// In handleKeyDown()
if (e.key === 'e' && housing3DPlacement?.isPlacementMode) {
  housing3DPlacement.placeFurniture();
  return;
}

if (e.key === 'r' && housing3DPlacement?.isPlacementMode) {
  housing3DPlacement.rotateFurniture();
  return;
}

if (e.key === 'Escape' && housing3DPlacement?.isPlacementMode) {
  housing3DPlacement.cancelPlacement();
  return;
}
```

#### **Schritt 5.3: Erweitere housing_ui.js** (50 Zeilen)

**WICHTIG:** Code **NICHT ersetzen**, nur **erweitern**!

**Datei:** `digivice/js/ui/housing_ui.js`

**In der Funktion wo Möbel ausgewählt wird:**

```javascript
// VORHER:
selectFurniture(furniture) {
  console.log('Selected:', furniture.name);
  // Zeige Details
}

// NACHHER:
selectFurniture(furniture) {
  console.log('Selected:', furniture.name);

  // Schließe UI
  this.hide();

  // Starte 3D-Placement
  if (window.housing3DPlacement) {
    window.housing3DPlacement.startPlacement(furniture);
  }
}
```

#### **Schritt 5.4: Testing** (30 Minuten)

1. Öffne Digivice
2. Klicke "🏠 Housing"
3. Wähle Möbel (z.B. "Bett")
4. Prüfe:
   - ✅ UI schließt sich
   - ✅ 3D-Preview erscheint vor Spieler
   - ✅ E-Taste platziert Möbel
   - ✅ R-Taste rotiert Preview
   - ✅ ESC bricht ab

#### **Schritt 5.5: Commit**

```bash
git add digivice/js/housing_3d_placement.js
git add digivice/js/3d_scene.js
git add digivice/js/ui/housing_ui.js
git commit -m "🏠 ADD: 3D-Möbel-Placement System (Hybrid)

- Neue Datei: housing_3d_placement.js (400 Zeilen)
- Integration in 3d_scene.js
- Erweitert housing_ui.js mit 3D-Trigger
- Transparente Preview-Meshes
- Collision Detection
- E = Platzieren, R = Rotieren, ESC = Abbrechen
- Backend-Sync für Persistenz

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## ✅ CHECKLIST FÜR WEB MODEL

### **Vor Start:**

- [ ] `NEU_WEB_MODEL_PROJEKT_KOMPLETT.md` gelesen (850 Zeilen)
- [ ] `WEB_MODEL_START_INSTRUCTIONS.md` gelesen (89 Zeilen)
- [ ] `digivice/js/3d_scene.js` gelesen & verstanden (2500+ Zeilen)
- [ ] `digivice/js/instrument_player.js` als Referenz gelesen (570 Zeilen)
- [ ] `digivice/index.html` Struktur verstanden (2400+ Zeilen)

### **Phase 1 (Dice Monsters):**

- [ ] `3d_dice_system.js` erstellt (200-300 Zeilen)
- [ ] Integration in `3d_scene.js` (50 Zeilen)
- [ ] Erweitert `dice_monsters_ui.js` (100 Zeilen)
- [ ] Testing abgeschlossen (Würfel rollen smooth)
- [ ] Git Commit mit richtigem Format

### **Phase 2 (Boss Markers):**

- [ ] `boss_spawns.json` erstellt (9 Bosse)
- [ ] `boss_marker_system.js` erstellt (300 Zeilen)
- [ ] Integration in `world_manager.js` (50 Zeilen)
- [ ] E-Taste Handler erweitert (50 Zeilen)
- [ ] Testing abgeschlossen (Marker sichtbar, E-Taste funktioniert)
- [ ] Git Commit

### **Phase 3 (Instruments 3D):**

- [ ] `najika_instrument_animator.js` erstellt (200 Zeilen)
- [ ] Integration in `3d_scene.js` (50 Zeilen)
- [ ] Erweitert `instrument_player.js` (50 Zeilen)
- [ ] Testing abgeschlossen (Animation sync mit Sound)
- [ ] Git Commit

### **Phase 4 (World HUD):**

- [ ] `world_hud.js` erstellt (300 Zeilen)
- [ ] Integration in `world_manager.js` (30 Zeilen)
- [ ] H-Taste Toggle implementiert (20 Zeilen)
- [ ] Testing abgeschlossen (HUD aktualisiert sich)
- [ ] Git Commit

### **Phase 5 (Housing 3D):**

- [ ] `housing_3d_placement.js` erstellt (400 Zeilen)
- [ ] Integration in `3d_scene.js` (50 Zeilen)
- [ ] Erweitert `housing_ui.js` (50 Zeilen)
- [ ] Testing abgeschlossen (Platzierung funktioniert)
- [ ] Git Commit

### **Final:**

- [ ] Alle 5 Phasen abgeschlossen
- [ ] Alle Tests erfolgreich
- [ ] Keine Errors in Browser Console
- [ ] Final Report geschrieben
- [ ] Push to GitHub

---

## 📊 ERWARTETES ERGEBNIS

### **Nach Completion:**

```
NEUE DATEIEN (ca. 1600+ Zeilen):
├─ digivice/js/3d_dice_system.js                (300 Zeilen)
├─ digivice/js/world/boss_marker_system.js      (300 Zeilen)
├─ digivice/js/najika_instrument_animator.js    (200 Zeilen)
├─ digivice/js/world/world_hud.js               (300 Zeilen)
├─ digivice/js/housing_3d_placement.js          (400 Zeilen)
└─ digivice/data/boss_spawns.json               (100 Zeilen)

ERWEITERTE DATEIEN (ca. 400 Zeilen):
├─ digivice/js/3d_scene.js                      (+200 Zeilen)
├─ digivice/js/world/world_manager.js           (+80 Zeilen)
├─ digivice/js/ui/dice_monsters_ui.js           (+100 Zeilen)
├─ digivice/js/instrument_player.js             (+50 Zeilen)
└─ digivice/js/ui/housing_ui.js                 (+50 Zeilen)

GESAMT: ~2000 Zeilen neuer/erweiterter Code
```

### **Features:**

✅ 3D-Würfel beim Dice Monsters
✅ Boss-Marker in Open World (9 Bosse)
✅ Najika spielt Instrument (3D-Animation)
✅ World Info HUD (oben rechts)
✅ Möbel 3D-Platzierung (Hybrid-System)

### **User Experience:**

```
VORHER:
- Alles nur Button-UI
- Keine 3D-Interaktion
- Wenig Immersion

NACHHER:
- 5 Systeme in 3D integriert
- Buttons bleiben als Alternative
- Hohe Immersion
- Smooth Gameplay
```

---

## 🚀 JETZT STARTEN!

**Los geht's, Web Model!**

**Timeline:** 3-5 Tage autonome Arbeit
**Regeln:** Kein Token-Limit, autonom arbeiten, committe täglich

**🤖 STOPPE NICHT BIS ALLE 5 PHASEN FERTIG SIND! 🤖**

---

**ENDE DER ANWEISUNG**

**Erstellt:** 2025-11-23
**Version:** 1.0
**Für:** Neues Claude Code Web Model
**Priorität:** HOCH
