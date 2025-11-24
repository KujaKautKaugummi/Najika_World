# 🎮 NAJIKA WORLD - START GUIDE

## Quick Start

### 1. Starte das Game
```bash
START_NAJIKA_GAME.bat
```

**Das startet:**
- Python HTTP Server auf Port 5173
- Öffnet: http://localhost:5173/najika_world_UNIFIED.html

---

## Was funktioniert (OHNE Backend):

### ✅ Open World Features:
- **9.6km × 9.6km Map** (1.75× größer als Fortnite BR!)
- **9 Regionen** mit verschiedenen Biomes
- **Schwarze Mühle** auf dem Berg (Najika's Home)
- **8 Städte/Orte** verteilt auf der Map
- **WASD Bewegung** (6-9 m/s, realistisch!)
- **Combat System** (MANUAL/ASSIST/AUTO Modi)
- **Enemies** spawnen in allen Regionen
- **E-Taste Interaktionen** (Gebäude betreten)

### 🎮 Controls:
- **WASD** - Bewegung
- **Shift** - Sprint
- **E** - Interagieren (Mühle/Städte betreten)
- **Tab** - Combat Mode wechseln
- **Q/E/Space/C/X/V** - Combat (MANUAL Mode)
- **1/2/3/4** - Anfeuern (ASSIST/AUTO Mode)

---

## Was Backend (Port 8000) braucht:

### 🔴 Optional Features (brauchen Backend):
- **Najika AI Chat** (im Digivice/Mühle)
- **Najika Stats Sync** (Hunger, Energy, Happiness)
- **Teleport System** (zwischen Räumen)
- **Voice Call System**
- **Training System**

### Starten (falls gewünscht):
```bash
cd backend
python najika_server.py
```

**Warnung:** Server hat viele Dependencies:
- Ollama (für AI)
- ChromaDB (für Memory)
- Coqui TTS (für Voice)
- Whisper (für STT)

---

## Aktuelle Map-Status:

### ✅ Fertig & Funktioniert:
1. **Regionen:** 9× 3200m × 3200m Gebiete
2. **Schwarze Mühle:**
   - Position: (0, 50, 0) auf Berg
   - Scale: 25× (sichtbar!)
   - Marker: Lila Kugel bei y=300
   - Betreten: 150m Radius
3. **Städte:** 8 Orte mit 120m Interact-Radius
4. **Character:** 1.35m groß, 6-9 m/s Speed
5. **Enemies:** Über ganze Regionen verteilt
6. **Combat:** Realtime mit 3 Modi

### 📋 TODO (Phase 2 - nicht zwingend):
- **Terrain Variation:** Berge, Täler, Dünen (aktuell flat)
- **Perlin Noise:** Organisches Terrain
- **Edge Blending:** Smooth Übergänge zwischen Regionen

---

## Troubleshooting:

### Mühle nicht sichtbar?
1. Prüfe Console (F12): Sollte "✅ Schwarze Windmühle auf Berg-Gipfel platziert!" zeigen
2. Schaue zum Center (0, 0): Lila Marker bei y=300
3. Fliege zur Mitte: Berg sollte bei y=50 sein

### Mühle nicht betretbar?
1. Näher ran: 150m Radius
2. Drücke **E** wenn Prompt erscheint
3. Öffnet neues Fenster: http://localhost:5173/index.html

### Movement zu langsam/schnell?
- Langsam: 0.1 = 6 m/s (Walking)
- Schnell: 0.15 = 9 m/s (Sprint)
- Aktuell korrekt für 9.6km Map!

### Keine Enemies?
1. Prüfe Console: "✅ X Enemies gespawnt!"
2. Enemies spawnen ±1500m um Region-Center
3. Laufe durch Regionen um sie zu finden

### Backend Offline?
- Oben rechts: Roter Punkt = "Backend Offline"
- **Normal!** Game funktioniert ohne Backend
- Nur Chat/Teleport brauchen Backend

---

## Map-Layout (3×3 Grid):

```
┌─────────────┬─────────────┬─────────────┐
│ Reich der   │ Blitzebene  │ Heiße       │
│ Drei (Ice)  │ (Highland)  │ Dünen       │
│ x:-3200     │ x:0         │ x:3200      │
│ z:3200      │ z:3200      │ z:3200      │
├─────────────┼─────────────┼─────────────┤
│ Grünschlamm │ Götterfels  │ Salzwind-   │
│ (Swamp)     │ (Mountain)  │ Küste       │
│ x:-3200     │ ⭐ MÜHLE    │ x:3200      │
│ z:0         │ x:0, z:0    │ z:0         │
├─────────────┼─────────────┼─────────────┤
│ Tiefen-     │ Samtmoos-   │ Magma-      │
│ höhlen      │ Tiefwald    │ ströme      │
│ (Caves)     │ (Forest)    │ (Volcano)   │
│ x:-3200     │ x:0         │ x:3200      │
│ z:-3200     │ z:-3200     │ z:-3200     │
└─────────────┴─────────────┴─────────────┘
```

**Spawn Point:** Götterfels Center (0, 55, 0) auf dem Berg!

---

## Performance:

**Ziel:** 30+ FPS
**Map-Größe:** 9.6km × 9.6km = 92.16 km²
**Enemies:** ~30-45 gleichzeitig (3-5 pro Region)
**Gebäude:** 9 (1 Mühle + 8 Städte)

**Optimierungen:**
- Flat terrain (Phase 1) = Fast
- Terrain Variation (Phase 2) = Langsamer
- Shadow Map: 2048×2048
- Grid: 9600m mit 200 Lines

---

## Vergleich mit anderen Games:

| Game | Map-Größe | Laufzeit (Diagonal) |
|------|-----------|---------------------|
| **Najika World** | 9.6km × 9.6km | ~37 Minuten |
| Fortnite BR | 5.5km × 5.5km | ~20 Minuten |
| Skyrim | 37 km² | ~30 Minuten |
| GTA V | 127 km² | ~60 Minuten |

**Najika World ist 1.75× größer als Fortnite BR!** 🎮

---

## Nächste Schritte (optional):

1. **Teste alles:** Laufen, Combat, Mühle betreten
2. **Phase 2:** Terrain Variation (wenn gewünscht)
3. **Backend:** Starte für Chat/Teleport Features
4. **NPCs laden:** JSON-Dateien in `/data/` (36 Dateien)
5. **Quests aktivieren:** Quest-System einbauen

---

**Viel Spaß in Najika World! 🌍**
