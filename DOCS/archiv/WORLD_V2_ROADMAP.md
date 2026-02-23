# 🗺️ NAJIKA WORLD V2 - ROADMAP

**Stand:** 9. November 2025, 21:45 Uhr
**Aktueller Status:** ~80% Core-Funktionalität fertig

---

## ✅ WAS FUNKTIONIERT (FERTIG)

### Core-Systeme (100%)
```yaml
✅ World Manager: Lädt und orchestriert alle Systeme
✅ Region Streaming: Lädt/Entlädt Regionen dynamisch
✅ Terrain Generator: Erstellt Terrain-Geometrie für 9 Regionen
✅ Biome System: Definiert Farben und Eigenschaften
✅ Vegetation System: 27 Templates für Bäume/Pflanzen/etc.
✅ City Builder: Baut 5 Städte mit Gebäuden
✅ LOD Manager: Vorhanden (noch nicht aktiviert)
✅ Asset Discovery: Findet 71 Assets (KayKit)
✅ Asset Loader: Lädt Assets (noch Placeholder)
```

### Controls & Navigation (100%)
```yaml
✅ WASD-Steuerung: W/A/S/D + Shift Sprint
✅ Camera Controller: Orbit-Modus, Maus-Steuerung
✅ Teleport-System: 9 Regionen + 5 Städte teleportierbar
✅ Character: Grüne Kapsel bewegt sich korrekt
✅ Terrain-Höhe: Character spawnt über Terrain
✅ Collision: Map-Grenzen (9600x9600)
```

### Data & Config (100%)
```yaml
✅ regions.json: 9 Regionen definiert
✅ biomes.json: 9 Biome mit Farben/Eigenschaften
✅ cities.json: 5 Städte definiert
✅ Alle JSON-Dateien laden korrekt
```

---

## 🔴 WAS AKTUELL KAPUTT IST (MUSS GEFIXT WERDEN!)

### Kritische Bugs
```yaml
❌ Terrain-Farben: Wüste/Küste zeigen Weiß statt Farben
   → Web-Modell muss fixen (Prio 1)

❌ Vulkan-Terrain: Zeigt Wellen statt flach
   → Cache-Problem, muss geprüft werden

❌ Eis-Teleport: Button funktioniert nicht
   → Region-Name stimmt nicht überein
```

---

## 🟡 WAS FEHLT (WICHTIGE FEATURES)

### 1. Vegetation Sichtbar (WICHTIG!)
```yaml
Status: System läuft, aber Placeholder-Grafik

Problem:
  - Bäume = Grüne Kugeln + Braune Zylinder
  - Büsche = Kleine Kugeln
  - Keine echten 3D-Modelle

Was zu tun:
  ✅ Einfach (für jetzt):
     - Bessere Placeholder mit Farben
     - Verschiedene Formen (Kegel für Tannen, etc.)

  ⏳ Später (für Release):
     - KayKit 3D-Modelle laden (.glb)
     - GLTFLoader implementieren
     - Texturen anwenden

Dateien:
  - vegetation_system.js (createTreeTemplate, etc.)
  - Asset-Ordner: /static/assets/kaykit/

Priorität: MITTEL (System funktioniert, nur Optik)
```

### 2. Städte Sichtbar (WICHTIG!)
```yaml
Status: System läuft, aber Placeholder-Boxen

Problem:
  - Gebäude = Bunte Boxen (Placeholder)
  - Keine echten Häuser/Türme

Was zu tun:
  ✅ Einfach (für jetzt):
     - Bessere Placeholder
     - Häuser = Große Box + Dach (Pyramide)
     - Türme = Hohe schmale Box
     - Mauern = Lange flache Box

  ⏳ Später (für Release):
     - KayKit Medieval Assets laden
     - Verschiedene Gebäude-Typen
     - Stadt-Layouts verbessern

Dateien:
  - city_builder.js (createBuilding)

Priorität: MITTEL (System funktioniert, nur Optik)
```

### 3. Wasser-Rendering (WICHTIG!)
```yaml
Status: NICHT implementiert

Problem:
  - Küste hat kein Wasser (Ozean fehlt)
  - Seen fehlen in Wald/Sumpf
  - Flüsse fehlen

Was zu tun:
  1. Wasser-Plane erstellen (THREE.PlaneGeometry)
  2. Wasser-Material (transparent, blau, reflektiv)
  3. Wasser-Position bei Küste (westliche Grenze)
  4. Optional: Wellen-Animation (Shader)
  5. Optional: Reflexionen (Cubemap)

Code-Snippet:
  const waterGeometry = new THREE.PlaneGeometry(2400, 2400);
  const waterMaterial = new THREE.MeshStandardMaterial({
    color: 0x1e90ff,
    transparent: true,
    opacity: 0.7,
    roughness: 0.1,
    metalness: 0.8
  });
  const water = new THREE.Mesh(waterGeometry, waterMaterial);
  water.rotation.x = -Math.PI / 2;
  water.position.y = -2;  // Unter Terrain

Dateien:
  - region_streaming.js (loadRegionFeatures)
  - biomes.json (waterPresence, hasOcean flags)

Priorität: HOCH (für Küste essential!)
```

### 4. Lava-Rendering (WICHTIG!)
```yaml
Status: NICHT implementiert

Problem:
  - Vulkan hat keine Lava-Flüsse
  - Lava-Material fehlt

Was zu tun:
  1. Lava-Material erstellen (emissive, orange/rot)
  2. Lava-Flüsse als Planes platzieren
  3. Optional: Glüh-Effekt (emissiveIntensity)
  4. Optional: Fließ-Animation

Code-Snippet:
  const lavaMaterial = new THREE.MeshStandardMaterial({
    color: 0xff4500,
    emissive: 0xff4500,
    emissiveIntensity: 2.0,
    roughness: 0.3
  });

Dateien:
  - region_streaming.js (loadRegionFeatures)
  - biomes.json (lavaFlows flag)

Priorität: MITTEL (Nice-to-have für Vulkan)
```

### 5. Fog/Nebel-System (MITTEL)
```yaml
Status: NICHT implementiert

Problem:
  - Alle Regionen sehen gleich klar aus
  - Keine Atmosphäre

Was zu tun:
  1. THREE.Fog für jedes Biome aktivieren
  2. Fog-Farbe aus biomes.json laden (colors.fog)
  3. Fog-Distanz basierend auf Biome

Code-Snippet:
  scene.fog = new THREE.Fog(
    biome.colors.fog,  // Farbe
    1000,              // Near (wo Fog startet)
    3000               // Far (wo Fog max ist)
  );

Dateien:
  - biome_system.js (applyBiomeEnvironment)
  - biomes.json (colors.fog bereits definiert!)

Priorität: NIEDRIG (Optik-Verbesserung)
```

### 6. Tag/Nacht-Zyklus (NIEDRIG)
```yaml
Status: NICHT implementiert

Problem:
  - Immer Tag
  - Keine dynamischen Schatten
  - Keine Beleuchtungs-Änderungen

Was zu tun:
  1. Zeit-System (0-24 Stunden Loop)
  2. Sonne rotiert um Welt
  3. Licht-Intensität ändert sich
  4. Himmel-Farbe ändert sich
  5. Optional: Mond/Sterne bei Nacht

Dateien:
  - world_manager.js (neue Funktion: updateDayNightCycle)

Priorität: NIEDRIG (Nice-to-have, nicht essential)
```

---

## 🟢 WAS VERBESSERT WERDEN KANN (POLISH)

### 1. Lighting-System Verbessern
```yaml
Aktuell:
  - 1x AmbientLight (0.4)
  - 1x DirectionalLight (0.6)
  - Sehr basic

Verbesserungen:
  - HemisphereLight für Himmel/Boden
  - Mehr Schatten-Details
  - Biome-spezifisches Licht (Wüste heller, Höhlen dunkler)
  - Dynamische Schatten für Character

Priorität: NIEDRIG
```

### 2. UI/UX Verbesserungen
```yaml
Was fehlt:
  ❌ Minimap (zeigt Regionen)
  ❌ Region-Namen beim Betreten (Toast/Notification)
  ❌ Compass (N/O/S/W)
  ❌ Quest-Marker (später)
  ❌ Health/Stamina Bars (später)

Was zu tun:
  1. Canvas-Overlay für Minimap (2D)
  2. Event-System für Region-Wechsel
  3. Toast-Notifications (CSS + JS)

Priorität: NIEDRIG (erstmal Gameplay funktionsfähig)
```

### 3. Performance-Optimierung
```yaml
Was fehlt:
  ❌ LOD aktivieren (Level-of-Detail)
  ❌ Instancing für gleiche Objekte (Bäume)
  ❌ Frustum Culling (nicht sichtbare Objekte deaktivieren)
  ❌ Vegetation-Batching

Was zu tun:
  1. LOD Manager aktivieren (lod_manager.js vorhanden!)
  2. THREE.InstancedMesh für Bäume nutzen
  3. Frustum Culling für Vegetation

Priorität: NIEDRIG (aktuell läuft es noch)
Wird wichtig: Wenn mehr Assets geladen werden
```

### 4. Sound/Music (SPÄTER)
```yaml
Was fehlt:
  ❌ Ambient-Sounds (Wind, Vögel, Wasser)
  ❌ Footstep-Sounds
  ❌ Music-Tracks pro Region
  ❌ Combat-Sounds (später)

Priorität: SEHR NIEDRIG (viel später)
```

---

## 🎯 EMPFOHLENE REIHENFOLGE

### Phase 1: BUGS FIXEN (JETZT!) 🔴
```yaml
1. Terrain-Farben reparieren (Web-Modell)
2. Vulkan-Terrain glätten (Cache-Problem)
3. Eis-Teleport fixen (Region-Name)

Dauer: 1-2 Stunden
Ziel: Alles funktioniert fehlerfrei!
```

### Phase 2: WASSER & LAVA (DANACH) 🟡
```yaml
1. Wasser-Rendering für Küste implementieren
2. Seen für Wald/Sumpf
3. Lava-Flüsse für Vulkan

Dauer: 2-3 Stunden
Ziel: Regionen sehen viel besser aus!
```

### Phase 3: VEGETATION & STÄDTE VERBESSERN 🟢
```yaml
1. Bessere Placeholder für Bäume (Kegel statt Kugel)
2. Bessere Placeholder für Häuser (Box + Dach)
3. Optional: KayKit 3D-Modelle laden

Dauer: 3-4 Stunden
Ziel: Welt sieht aus wie ein Spiel!
```

### Phase 4: POLISH & PERFORMANCE 🎨
```yaml
1. Fog-System aktivieren
2. Lighting verbessern
3. LOD aktivieren
4. UI verbessern (Minimap, etc.)

Dauer: 4-6 Stunden
Ziel: Release-Quality!
```

### Phase 5: NICE-TO-HAVE ✨
```yaml
1. Tag/Nacht-Zyklus
2. Sound/Music
3. Partikel-Effekte
4. Wetter-System

Dauer: 10+ Stunden
Ziel: AAA-Quality! (aber nicht jetzt)
```

---

## 📊 FORTSCHRITTS-ÜBERSICHT

```
Core-Systeme:     ████████████████████ 100% ✅
Terrain:          ████████████████░░░░  80% (Farben broken)
Vegetation:       ████████████░░░░░░░░  60% (Placeholder)
Städte:           ████████████░░░░░░░░  60% (Placeholder)
Wasser:           ░░░░░░░░░░░░░░░░░░░░   0% (fehlt!)
Lava:             ░░░░░░░░░░░░░░░░░░░░   0% (fehlt!)
Fog:              ░░░░░░░░░░░░░░░░░░░░   0% (fehlt!)
Controls:         ████████████████████ 100% ✅
Teleport:         ███████████████████░  95% (Eis broken)
UI/UX:            ████░░░░░░░░░░░░░░░░  20%
Performance:      ████████░░░░░░░░░░░░  40%
Sound:            ░░░░░░░░░░░░░░░░░░░░   0%

─────────────────────────────────────────────
GESAMT:           ████████████░░░░░░░░  65%
─────────────────────────────────────────────

SPIELBAR:         ✅ JA (mit Bugs)
RELEASE-READY:    ❌ NEIN (Phase 1-3 nötig)
```

---

## 🎮 WAS MINDESTENS FUNKTIONIEREN MUSS (MVP)

### Minimum Viable Product:
```yaml
✅ 9 Regionen mit verschiedenen FARBEN
✅ Alle Teleport-Buttons funktionieren
✅ WASD-Steuerung funktioniert
✅ Character schwebt ÜBER Terrain (nicht unter)
✅ Wasser sichtbar bei Küste
⏳ Lava sichtbar bei Vulkan (nice-to-have)
⏳ Vegetation erkennbar (mind. gute Placeholder)
⏳ Städte erkennbar (mind. gute Placeholder)

Das ist MINIMUM für "testbar"!
```

---

## 💡 IDEEN FÜR SPÄTER (NICHT JETZT!)

```yaml
💡 Wettersystem (Regen, Schnee, Sturm)
💡 Jahreszeiten (Herbst-Farben, Winter-Schnee)
💡 Dynamische Events (NPCs spawnen, Quests)
💡 Combat-System integrieren
💡 Najika als begehbarer NPC
💡 Schwarze Windmühle als 3D-Gebäude
💡 Götterfels als massiver Berg (500m hoch!)
💡 Tiefenhöhlen als Untergrund-System
💡 Crafting-Stations in Städten
💡 Teleport-Animationen (Partikel)
💡 Character-Customization
💡 Multiplayer-Support (viel später!)
```

---

## 📝 ZUSAMMENFASSUNG

**Was JETZT gemacht werden muss:**
1. 🔴 **Terrain-Farben fixen** (Web-Modell, 1h)
2. 🔴 **Vulkan & Eis fixen** (Web-Modell, 30min)
3. 🟡 **Wasser implementieren** (2h)
4. 🟡 **Lava implementieren** (1h)
5. 🟢 **Placeholder verbessern** (2-3h)

**Nach 6-8 Stunden Arbeit:**
→ World V2 ist **RELEASE-READY** für Testing! ✅

**Alles andere:**
→ Kann später kommen (Nice-to-have, nicht essential)

---

**Erstellt:** 2025-11-09, 21:45 Uhr
**Für:** Vollständige Roadmap-Übersicht
**Status:** 65% fertig, MVP bei ~80% möglich
