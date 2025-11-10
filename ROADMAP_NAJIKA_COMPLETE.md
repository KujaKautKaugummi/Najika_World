# 🗺️ NAJIKA WORLD - 9 REGIONS TEST MAP ROADMAP
## Für Claude Code Web-Modelle (Unlimited)

**LETZTE AKTUALISIERUNG:** 2025-11-10 (Basierend auf echtem Code-Stand)

---

## 🎯 WAS IST DIE TEST-MAP?

**User-Klarstellung:**
> "es müssen wirklich alle funktionen bei digivice bei najika drin sein zum schluss"
> "wenn das alles fertig und getestet ist übertragen wir das auf das große handyspiel"

**Die Test-Map ist:**
- ✅ **KOMPLETTE TEST-UMGEBUNG** für alle Features
- ✅ **Alle** Digivice-Funktionen müssen hier getestet werden
- ✅ **Alle** Najika KI Funktionen müssen hier getestet werden
- ✅ **DANN** wird alles auf das große Handyspiel übertragen

**Workflow:**
```
Feature auf Test-Map entwickeln → Testen → Wenn fertig → Auf Handyspiel übertragen
```

---

## ✅ AKTUELLER STAND (najika_world_9regions_test.html)

**URL:** http://localhost:8000/digivice/najika_world_9regions_test.html

**WAS FUNKTIONIERT (100%):**

### Basis-Systeme:
- ✅ **9 Regionen (3x3 Grid)** - Alle Farben korrekt!
  - Ice (weiß), Highland (braun), Desert (gelb)
  - Swamp (grün), Mountain (grau, Y=5 höher), Coast (hellbraun)
  - Caves (dunkelgrau), Forest (dunkelgrün), Volcano (braun)
- ✅ **WASD Movement** - Richtungen korrekt (W=vor, S=zurück, A/D=links/rechts, Shift=Sprint)
- ✅ **Najika Character (Bohne)** - Grüner Zylinder mit Kopf/Füßen
- ✅ **Auto-Height Adjustment** - Character passt sich Berg-Höhe an
- ✅ **Camera Controller** - Orbit-Modus funktioniert
- ✅ **Map Bounds** - Character bleibt auf Map (-100 bis 100)

### Asset-System:
- ✅ **4 Regionen mit Assets:**
  - 🏜️ Oasis (16 Assets): Palmen, Kakteen, Häuser, Töpfe
  - 🏰 Dungeon (15 Assets): Truhen, Fackeln, Banner, Wände
  - 🏛️ Medieval (9 Assets): Gebäude, Fässer, Eimer
  - 🌲 Nature (12 Assets): Bäume, Felsen, Büsche
- ✅ **GLTFLoader** - Lädt .gltf und .glb Dateien
- ✅ **Loading Screen** - Mit Progressbar (zeigt X/52 Assets)
- ✅ **Shadows** - Alle Models casten/empfangen Schatten

### UI-Elemente:
- ✅ **Status-UI** (oben links): Kamera-Modus, Position, Gebiet, Assets, FPS
- ✅ **Teleport-Buttons** (unten): 5 Buttons (Oasis, Dungeon, Medieval, Nature, Center)
- ✅ **Region-Marker** - 4 farbige Säulen mit Text-Labels
- ✅ **Grid Helper** - 200x200 Grid mit 40 Divisions
- ✅ **Minimap Canvas** - 200x200px (oben rechts, noch leer)

### Technisches:
- ✅ **Three.js r128** - Via CDN
- ✅ **Scene** - Himmelblau, Fog, Lighting
- ✅ **Shadows** - 4096x4096 Shadow Map
- ✅ **Responsive** - Window Resize funktioniert

---

## ❌ WAS FEHLT (ToDo für Web-Modelle)

### PRIORITÄT 1 - Assets & Basis-Features:

1. **Assets für 5 fehlende Regionen:**
   - ❌ Ice Region (keine Assets)
   - ❌ Highland Region (keine Assets)
   - ❌ Desert Region (nur Farbe, keine Assets)
   - ❌ Swamp Region (keine Assets)
   - ❌ Caves Region (keine Assets)
   - ❌ Volcano Region (keine Assets)
   - ❌ Coast Region (keine Assets)

2. **Minimap vervollständigen:**
   - ❌ Canvas existiert, aber ist leer
   - ❌ 9 Regionen auf Minimap zeichnen
   - ❌ Najika-Position live anzeigen (grüner Punkt)
   - ❌ Farb-Kodierung der Regionen

3. **Alle 9 Regionen mit Teleport-Buttons:**
   - ✅ 4 Buttons existieren (Oasis, Dungeon, Medieval, Nature)
   - ❌ 5 Buttons fehlen (Ice, Highland, Desert, Swamp, Caves, Volcano, Coast, Mountain)

4. **Region-Marker für alle 9:**
   - ✅ 4 Marker existieren
   - ❌ 5 Marker fehlen

### PRIORITÄT 2 - Kamera & Movement:

5. **Third-Person Camera:**
   - ✅ Camera Controller existiert
   - ❌ Third-Person Modus aktivieren (Kamera folgt Najika)
   - ❌ Smooth Follow implementieren
   - ❌ Camera Modi wechseln funktioniert (Button existiert, aber nur Orbit aktiv)

6. **Character Improvements:**
   - ❌ Besseres Character-Model (aktuell simple Bohne)
   - ❌ Walk/Run Animation
   - ❌ Rotation beim Movement

### PRIORITÄT 3 - Digivice Integration:

7. **Digivice-Module einbinden:**
   - ✅ Existiert in `digivice/index.html`
   - ❌ Integration in Test-Map
   - ❌ Terminal-Module (4 Stück bereits fertig)
   - ❌ Najika Tamagotchi Stats anzeigen
   - ❌ Battle-System UI

8. **Backend-Verbindung:**
   - ✅ Backend läuft (najika_server.py Port 8000)
   - ❌ WebSocket-Verbindung zur Test-Map
   - ❌ Najika Status live updates

### PRIORITÄT 4 - Kampfsystem:

9. **Combat Integration:**
   - ✅ Existiert in separaten Files (`dungeon_combat.js`, `battle_core.js`)
   - ❌ Integration in Test-Map
   - ❌ Enemy Spawns in Regionen
   - ❌ Battle UI
   - ❌ E-Taste für Dungeon-Eintritt

10. **Enemy System:**
    - ✅ 10+ Enemy-Types definiert
    - ❌ Spawning-System aktiv
    - ❌ Kollisions-Detection
    - ❌ Loot-System

### PRIORITÄT 5 - Stadt-System & Besondere Orte:

11. **5 Städte + 3 Besondere Orte (E-Taste System):**
    - ✅ `cities.json` existiert mit allen Definitionen
    - ✅ E-Taste System existiert in `index.html` (Referenz: `3d_scene.js` Zeile 506-526)
    - ❌ **5 Städte auf Map platzieren:**
      1. Handelsfestung (Desert/Heiße Dünen) - PvP Arena, Player Shops
      2. Dampf-Hain (Forest/Samtmoos) - Onsen, Restaurants
      3. Salzige Bucht (Coast/Küste) - Hafen, Leuchtturm
      4. Runenheim (Highland/Blitzebene) - Magie-Akademie
      5. Funken-Siedlung (Volcano/Magmaströme) - Schmieden
    - ❌ **3 Besondere Orte auf Map platzieren:**
      1. Reich der Drei (Ice) - Untote & Nekromanten
      2. Funkelnest (Swamp) - Versteckte Schatzhöhle, Hexen
      3. Tiefenhöhlen (Caves) - Goblin-Siedlungen
    - ❌ **E-Taste Proximity-System:**
      - Spieler läuft mit WASD zu Stadt/Ort
      - Bei Nähe: "E - [Name] betreten" Prompt
      - E drücken → Lädt Interior
      - Exit-Taste → Zurück zur Map
    - ❌ **Stadt-Interiors erstellen:**
      - Gebäude, NPCs, Shops (Basis-Version)
      - Basierend auf `cities.json` Features

12. **Schwarze Windmühle (Najika's Home):**
    - ✅ Existiert komplett in `index.html` (12 Räume, 4 Stockwerke)
    - ✅ E-Taste System funktioniert
    - ❌ Auf Berg-Gipfel (Mountain Region) platzieren
    - ❌ Zugang wie bei Städten (E-Taste)

---

## 🚀 EMPFOHLENE ARBEITS-REIHENFOLGE

### Phase 1: Basis vervollständigen (4-6h)
1. Assets für 5 fehlende Regionen hinzufügen
2. Alle 9 Teleport-Buttons implementieren
3. Alle 9 Region-Marker platzieren
4. Minimap vervollständigen

**Ergebnis:** Alle 9 Regionen komplett navigierbar und sichtbar

### Phase 2: Kamera & Character (2-3h)
5. Third-Person Camera aktivieren
6. Character-Rotation beim Movement
7. Camera Modi-Wechsel testen

**Ergebnis:** Smooth gameplay mit Third-Person Kamera

### Phase 3: Digivice Integration (3-4h)
8. Backend WebSocket-Verbindung
9. Najika Stats UI einbinden
10. Terminal-Module zugänglich machen

**Ergebnis:** Najika KI lebt auf der Map

### Phase 4: Kampfsystem (4-5h)
11. Combat-Files integrieren
12. Enemy Spawns aktivieren
13. Battle UI implementieren
14. E-Taste für Dungeons

**Ergebnis:** Kampf-Mechanik funktioniert

### Phase 5: Stadt-System & Besondere Orte (5-6h)
15. 5 Städte + 3 Besondere Orte auf Map platzieren (Icons/3D-Modelle)
16. E-Taste Proximity-System für alle 8 Locations
17. Stadt-Interiors erstellen (Basis: Gebäude, NPCs)
18. Schwarze Windmühle auf Berg-Gipfel

**Ergebnis:** Komplette Open-World mit 5 Städten + 3 Besonderen Orten + Najika's Home

### Phase 6: Polish & Testing (4-6h)
18. Performance-Optimierung (FPS > 30)
19. Mobile Touch-Controls
20. Visuelle Verbesserungen
21. Bug-Fixes
22. Vollständiges Testing

**Ergebnis:** Release-ready für Übertragung auf Handyspiel

---

## 📁 WICHTIGE DATEIEN

### Haupt-Datei:
```
digivice/najika_world_9regions_test.html    (631 Zeilen - ALLES DRIN!)
```

### Referenz-Dateien:
```
digivice/index.html                         (Digivice UI + 12 Räume)
digivice/static/js/camera_controller.js     (Kamera-System)
```

### Kampfsystem:
```
digivice/js/dungeon_combat.js               (Combat-Logik)
digivice/js/dungeon_enemies.js              (10+ Enemy-Types)
digivice/js/battle_core.js                  (Battle-Engine)
digivice/js/battle_api.js                   (Backend-Integration)
```

### Data-Files:
```
digivice/data/regions.json                  (9 Regionen)
digivice/data/cities.json                   (8 Städte)
digivice/data/biomes.json                   (Biome-Eigenschaften)
```

### Backend:
```
backend/najika_server.py                    (2153 Zeilen - Python Server)
```

### Assets:
```
digivice/static/assets/kaykit/              (Dungeon, Medieval, Nature)
digivice/static/assets/jellysquish/         (Oasis)
```

---

## 📝 ENTWICKLUNGS-RICHTLINIEN

### 1. IMMER die Haupt-Datei lesen:
```bash
# Die Test-Map ist EINE HTML-Datei (631 Zeilen)
# Kein komplexes Modul-System mehr!
Read: digivice/najika_world_9regions_test.html
```

### 2. Assets hinzufügen:
```javascript
// Pattern (siehe Zeilen 387-458):
regionAssets: {
    ice: [
        { path: 'static/assets/...', name: '...', position: [x, 0, z], scale: 1 }
    ]
}
```

### 3. Teleport-Button hinzufügen:
```html
<!-- Pattern (siehe Zeile 169-175): -->
<button onclick="teleportTo('ice')">❄️ Eis</button>
```

### 4. Region-Position in `regionPositions` (Zeile 523):
```javascript
regionPositions: {
    ice: { x: -66.66, z: 66.66 }  // Top-left region
}
```

### 5. E-Taste System implementieren (für Städte/Orte):
```javascript
// Referenz: digivice/js/3d_scene.js (Zeile 506-526)

// 1. Proximity-Detection
let nearBuilding = null;

function checkBuildingProximity() {
    const playerPos = character.position;
    // Check distance zu Stadt/Ort
    const distance = playerPos.distanceTo(building.position);
    if (distance < 10) {  // 10 Einheiten Radius
        nearBuilding = building;
        showPrompt("E - " + building.userData.buildingName + " betreten");
    } else {
        nearBuilding = null;
        hidePrompt();
    }
}

// 2. E-Taste Event
window.addEventListener('keydown', (e) => {
    if (e.key === 'e' || e.key === 'E') {
        if (nearBuilding) {
            enterBuilding(nearBuilding);
        }
    }
});

// 3. Interior laden
function enterBuilding(building) {
    const buildingName = building.userData.buildingName;
    // Speichere Außen-Position
    exteriorPosition = { x: character.position.x, z: character.position.z };
    // Lade Interior (aus cities.json oder room_config_detailed.json)
    loadBuildingInterior(buildingName);
}

// 4. Exit zurück zur Map
function exitBuilding() {
    character.position.set(exteriorPosition.x, 0, exteriorPosition.z);
    // Zeige Außen-Scene wieder
}
```

### 6. Testing nach jeder Änderung:
```bash
1. Browser neu laden (Strg+F5)
2. Console checken (F12)
3. Alle Buttons testen
4. WASD Movement testen
5. E-Taste bei Stadt/Ort testen
6. Interior-Loading testen
7. Exit zurück zur Map testen
8. FPS prüfen (sollte > 30 sein)
```

---

## 🎯 ERFOLGS-KRITERIEN

### MVP (Minimum Viable Product):
- ✅ Alle 9 Regionen mit Assets
- ✅ Alle 9 Teleport-Buttons funktionieren
- ✅ Minimap zeigt alle Regionen + Najika-Position
- ✅ Third-Person Camera folgt Najika
- ✅ FPS > 30

### KOMPLETT (Ready für Handyspiel):
- ✅ MVP erfüllt
- ✅ Digivice komplett integriert
- ✅ Najika KI läuft und reagiert
- ✅ Kampfsystem funktioniert (Enemies spawnen, Battle UI)
- ✅ **5 Städte zugänglich** (E-Taste System)
- ✅ **3 Besondere Orte zugänglich** (E-Taste System)
- ✅ Schwarze Windmühle als Home (Berg-Gipfel)
- ✅ Mobile Touch-Controls
- ✅ Keine kritischen Bugs
- ✅ Performance stabil

---

## 💡 QUICK START FÜR WEB-MODELLE

### 1. Verstehe den Code:
```bash
Read: digivice/najika_world_9regions_test.html
# Komplett durchlesen! Nur 631 Zeilen, ALLES an einem Ort!
```

### 2. Starte Server:
```bash
# Backend muss laufen auf Port 8000
cd C:\Najika_World\backend
python najika_server.py
```

### 3. Öffne Test-Map:
```
http://localhost:8000/digivice/najika_world_9regions_test.html
```

### 4. Verstehe die Struktur:
- **Zeilen 1-136:** CSS & HTML-Struktur
- **Zeilen 184-250:** Scene Setup & 9 Regionen
- **Zeilen 252-290:** Najika Character (Bohne)
- **Zeilen 292-343:** WASD-Steuerung & Height-System
- **Zeilen 345-378:** Region-Marker
- **Zeilen 380-520:** Asset-Loading System
- **Zeilen 522-572:** Teleport & UI-Functions
- **Zeilen 574-625:** Animation Loop

### 5. Beginne mit Phase 1:
Assets für Ice-Region hinzufügen (einfachster Start!)

---

## 🔥 WICHTIG

**Die Test-Map ist SIMPEL gehalten:**
- Eine HTML-Datei (kein Webpack, kein Bundler)
- Three.js via CDN
- Inline JavaScript
- Einfach zu verstehen und zu erweitern

**NICHT verwechseln mit:**
- `najika_world_v2.html` (alte Version mit Modulen)
- `najika_world_FINAL.html` (andere Variante)

**DIE RICHTIGE DATEI:**
- `najika_world_9regions_test.html` ← DIESE!

---

**🎮 BEREIT? START MIT PHASE 1! 🚀**

**Ziel:** Alle 9 Regionen komplett → Dann Digivice → Dann Kampf → Dann Transfer auf Handyspiel!
