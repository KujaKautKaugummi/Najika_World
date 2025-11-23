# 🚀 World Map System - Quick Start Guide

## ⚡ Schnellstart in 3 Schritten

### 1. Demo Testen

```bash
# Öffne die Demo-Seite im Browser:
cd /home/user/Najika_World/digivice
# Öffne: world_map_demo.html
```

### 2. Keyboard Shortcuts

| Taste | Funktion |
|-------|----------|
| **M** | Öffne/Schließe Full Map |
| **N** | Toggle Minimap |
| **P** | Focus auf Spieler |
| **ESC** | Schließe Map |

### 3. Integration ins Spiel

Füge in deine HTML-Datei ein (nach THREE.js):

```html
<!-- World Map System -->
<script src="js/world_map_api.js"></script>
<script src="js/world_map_3d_renderer.js"></script>
<script src="js/ui/minimap.js"></script>
<script src="js/ui/world_map_full_ui.js"></script>
<script src="js/world_map_integration.js"></script>
```

**Das war's!** Das System ist jetzt aktiv.

---

## 🎮 Verwendung

### Programmatisch öffnen

```javascript
// Full Map öffnen
window.worldMapIntegration.openFullMap();

// Minimap togglen
window.worldMapIntegration.toggleMinimap();

// Auf Region fokussieren
window.worldMapIntegration.focusOnRegion('heisse_duenen');
```

### Position aktualisieren

```javascript
// Spieler-Position aktualisieren
window.worldMapAPI.savePlayerPosition(
    x,      // World X
    z,      // World Z
    y,      // World Y
    rotation // Rotation in Radians
);
```

### Region entdecken

```javascript
// Automatisch beim Betreten:
window.worldMapAPI.discoverRegion('samtmoos_tiefwald');
```

---

## 📍 Wichtige Weltpositionen

| Location | X | Z | Region |
|----------|---|---|--------|
| **Götterfels (Center)** | 4800 | 4800 | Zentrum |
| **Handelsfestung** | 8400 | 8200 | Heiße Dünen |
| **Dampf-Hain** | 4800 | 1500 | Samtmoos-Tiefwald |
| **Salzige Bucht** | 1500 | 4800 | Salzwind-Küste |
| **Runenheim** | 8400 | 4800 | Blitzebene |
| **Funken-Siedlung** | 4800 | 8200 | Magmaströme |

---

## 🎯 Features Checkliste

### ✅ Implementiert

- [x] 3D World Visualization mit THREE.js
- [x] 8 Biome mit korrekten Farben
- [x] Götterfels als zentraler Berg (500 Höhe)
- [x] Minimap in Bildschirmecke
- [x] Full Map UI (Taste M)
- [x] Player Position Tracking
- [x] Fast Travel System
- [x] Region Discovery
- [x] Fog of War
- [x] Cities als 3D-Marker
- [x] Zoom/Pan/Rotate
- [x] Search Funktion
- [x] Filters (Cities, POI, Biomes)
- [x] Keyboard Shortcuts
- [x] Demo Page

---

## 🔧 Konfiguration

### Minimap Position ändern

```javascript
// In world_map_integration.js, Zeile ~18:
this.config = {
    minimapEnabled: true,
    minimapPosition: 'top-right', // ← Hier ändern
    // Optionen: 'top-left', 'top-right', 'bottom-left', 'bottom-right'
    minimapSize: 200,
    minimapZoom: 20
};
```

### Fog of War deaktivieren

```javascript
// Im Browser Console:
window.worldMapFullUI.renderer3D.toggleFogOfWar(false);
```

### Alle Regionen aufdecken (Debug)

```javascript
// Im Browser Console:
Object.keys(window.worldMapAPI.getRegions().regions).forEach(id => {
    window.worldMapAPI.discoverRegion(id);
});
```

---

## 🐛 Troubleshooting

### Map öffnet nicht

```javascript
// Console Check:
console.log(window.worldMapFullUI); // Sollte nicht undefined sein
console.log(window.worldMapIntegration); // Sollte nicht undefined sein

// Manuell öffnen:
window.worldMapFullUI.open();
```

### THREE.js nicht geladen

```html
<!-- Stelle sicher, dass THREE.js VOR den Map Scripts geladen wird: -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
```

### Minimap wird nicht angezeigt

```javascript
// Console Check:
console.log(window.minimap); // Sollte Minimap-Instanz sein

// Manuell erstellen:
window.minimap = new Minimap({
    position: 'top-right',
    size: 200
});
```

### Position wird nicht aktualisiert

```javascript
// Manuell setzen:
window.worldMapAPI.savePlayerPosition(4800, 4800, 0, 0);

// Check API Status:
console.log(window.worldMapAPI.getPlayerPosition());
```

---

## 📊 Console Commands (Debug)

```javascript
// Position anzeigen
window.worldMapAPI.getPlayerPosition();

// Alle Regionen anzeigen
window.worldMapAPI.getRegions();

// Erkundete Regionen anzeigen
window.worldMapAPI.getExploredRegions();

// Cities anzeigen
window.worldMapAPI.getCities();

// Travel Points anzeigen
window.worldMapAPI.getTravelPoints();

// Zu Region teleportieren
window.worldMapIntegration.focusOnRegion('goetterfels');

// Minimap neu erstellen
window.minimap.dispose();
window.minimap = new Minimap({ position: 'bottom-right', size: 250 });
```

---

## 🎨 Customization

### Minimap Größe ändern

```javascript
const minimap = new Minimap({
    size: 250,        // Größer (Default: 200)
    zoom: 15,         // Näher ran (Default: 20)
    position: 'bottom-left'
});
```

### Biome-Farben anpassen

Edit: `/home/user/Najika_World/digivice/data/biomes.json`

```json
"desert": {
    "colors": {
        "ground": "#e8d4a0",  // ← Ändere Farbe hier
        "ambient": "#ffa500",
        "fog": "#ffd700"
    }
}
```

### Region Bounds ändern

Edit: `/home/user/Najika_World/digivice/data/regions.json`

```json
"heisse_duenen": {
    "bounds": {
        "minX": 7200,   // ← Ändere Grenzen hier
        "maxX": 9600,
        "minZ": 7200,
        "maxZ": 9600
    }
}
```

---

## 🚀 Performance Tips

1. **Fog of War aktiviert lassen** - Rendert nur erkundete Regionen in Full Detail
2. **Minimap Update Interval erhöhen** - Weniger Updates = bessere Performance
3. **3D Detail reduzieren** - Weniger Segmente in Terrain Geometry
4. **Position Save throtteln** - Default ist 5 Sekunden, kann erhöht werden

```javascript
// In world_map_api.js:
this.positionUpdateInterval = 10000; // 10 Sekunden statt 5
```

---

## 📱 Mobile Support

Das System funktioniert auf Mobile, aber mit eingeschränkter Performance:

- Touch-Gesten für Zoom/Pan in Full Map
- Kleinere Minimap empfohlen (150px)
- Reduzierte 3D-Details

```javascript
// Mobile Config:
const minimap = new Minimap({
    size: 150,           // Kleiner
    zoom: 30,            // Weiter raus
    updateInterval: 200  // Weniger frequent
});
```

---

## ✅ Checklist für Production

- [ ] THREE.js korrekt eingebunden
- [ ] Alle JSON Dateien vorhanden (regions, biomes, cities)
- [ ] Backend API Endpoints implementiert (optional, funktioniert auch ohne)
- [ ] Position Tracking aktiviert
- [ ] Fog of War konfiguriert
- [ ] Keyboard Shortcuts dokumentiert
- [ ] Performance getestet
- [ ] Mobile Kompatibilität geprüft

---

## 🎉 Fertig!

Das World Map System ist jetzt vollständig einsatzbereit!

**Teste es:**
1. Öffne `world_map_demo.html`
2. Drücke **M** für Full Map
3. Drücke **N** für Minimap
4. Erkunde die Welt!

**Viel Spaß!** 🗺️✨
