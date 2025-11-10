# 🗺️ NAJIKA WORLD - COMPLETE ROADMAP
## Für Claude Code Web-Modelle (Unlimited)

**WICHTIG:**
- Erst **Modell 1** komplett aufbrauchen → Dann **Modell 2** als Reserve
- **GROßE SCHRITTE:** Viel vorbereiten, Code prüfen, dann in großem Rutsch einfügen
- Nicht Task-für-Task, sondern komplette Features auf einmal

---

## 📑 INHALTSVERZEICHNIS

1. [✅ Aktueller Status](#-aktueller-status-stand-najika_world_9regions_testhtml)
2. [🚀 Next Steps - Was jetzt zu tun ist](#-next-steps---was-jetzt-zu-tun-ist)
3. [🎯 Phase A1-A20: Test-Map Features](#-phase-a1-kamera-system-komplett)
4. [🤖 Phase B: Najika KI Integration](#-phase-b-najika-ki-integration)
5. [📝 Zusammenfassung für Web-Modelle](#-zusammenfassung-für-web-modelle)
6. [🔧 Entwicklungs-Richtlinien](#-entwicklungs-richtlinien)

---

## ✅ AKTUELLER STATUS (Stand: najika_world_9regions_test.html)

**WAS IST FERTIG:**
- ✅ 9 Regionen (3x3 Grid, flat build mode) - Ice, Highland, Desert, Swamp, Mountain, Coast, Caves, Forest, Volcano
- ✅ Najika Character (Bohne) mit WASD Movement
- ✅ Auto-adjust character height (Berg ist höher als andere Regionen)
- ✅ Kamera-Controller mit Orbit-Modus
- ✅ UI mit Position, Region, FPS, Asset-Count
- ✅ Minimap (Canvas, 200x200px oben rechts)
- ✅ Region-Marker und Text-Labels für 4 Test-Regionen
- ✅ Grid-Helper (200x200, 40 Divisions)
- ✅ Asset-Loading für 4 Test-Regionen (Oasis, Dungeon, Medieval, Nature)
- ✅ Teleportation zu verschiedenen Positionen
- ✅ Lighting (Ambient + Directional mit Shadows)
- ✅ Shadow-System funktioniert

**WAS FEHLT:**
- ❌ Third-Person Camera (folgt Najika automatisch)
- ❌ Assets für alle 9 Regionen (aktuell nur 4 Regionen)
- ❌ Dungeon-System (E-Taste zum Betreten)
- ❌ Schwarze Mühle (Najika's Home)
- ❌ Stadt-System (8 Städte)
- ❌ Digivice-Module vollständig
- ❌ Najika KI Integration

---

## 📋 STRATEGIE: 2-PHASEN-ANSATZ

### Phase A: TEST-MAP FERTIG
Alle Mechaniken auf Test-Map testen bis rund läuft.
**OHNE Najika KI!**

### Phase B: NAJIKA INTEGRATION
Erst wenn Map stabil → dann KI Najika + Living System drauf.

---

## 🚀 NEXT STEPS - WAS JETZT ZU TUN IST

**PRIORITÄT 1 (SOFORT):**
1. **Phase A1:** Third-Person Camera implementieren (Kamera folgt Najika automatisch)
2. **Assets:** Alle 9 Regionen mit Assets füllen (aktuell nur 4 fertig)
3. **Minimap:** Vollständige Minimap mit allen 9 Regionen + Najika-Position live

**PRIORITÄT 2 (DANACH):**
4. **Phase A3:** Dungeon-System (8 Dungeons, E-Taste zum Betreten)
5. **Phase A4:** Schwarze Mühle auf Berg-Gipfel
6. **Phase A5-A8:** Stadt-System (8 Städte mit Icons, Eintritt, Innenbereich)

**PRIORITÄT 3 (SPÄTER):**
7. **Phase A9-A14:** Digivice-Module (Map, Inventory, Stats, Quests, Crafting, Settings)
8. **Phase A15:** Visuelle Polish (Partikel, Effekte, bessere Modelle)
9. **Phase A16:** Testing & Bugfixes

**PHASE B (GANZ ZUM SCHLUSS):**
10. Najika KI Integration + Living System

---

## 🎯 PHASE A1: KAMERA-SYSTEM KOMPLETT

**STATUS:** ⚠️ TEILWEISE FERTIG (Orbit-Modus funktioniert, Third-Person fehlt noch)

**Was noch zu tun ist:**
Komplettes Third-Person Camera System aus `najika_world_v2.html` übernehmen.

**Vorbereitung:**
1. Lies `static/js/camera_controller.js` vollständig
2. Check wie in v2 Kamera an Character gebunden ist
3. Verstehe Third-Person Camera Logic

**Implementierung (1 großer Commit):**
- ✅ Orbit-Modus funktioniert bereits
- ❌ Third-Person Modus: Kamera folgt Najika automatisch
- ❌ Smooth movement beim Laufen
- ❌ Kamera-Kollision (nicht durch Boden/Berg)
- ✅ Mausrad-Zoom (bereits implementiert)
- ❌ Touch-Controls (Pinch-Zoom, Drag für Mobile)
- ❌ Umschalten zwischen Orbit und Third-Person

**Commit:** "Feature: Third-Person Camera - follows Najika"

---

## 🎯 PHASE A2: MINIMAP & REGION-LABELS

**STATUS:** ⚠️ TEILWEISE FERTIG (Minimap existiert, aber noch nicht vollständig)

**Was ist fertig:**
- ✅ Minimap Canvas (200x200px, oben rechts)
- ✅ Region-Namen als floating Labels (für 4 Test-Regionen)
- ✅ Aktuelle Region im UI ("Gebiet: Mountain")
- ✅ Grid-Lines zwischen Regionen (GridHelper)

**Was fehlt noch:**
- ❌ Minimap zeigt alle 9 Regionen (3x3 Grid)
- ❌ Najika als Dot auf Minimap (live update)
- ❌ Farb-Kodierung der Regionen auf Minimap
- ❌ Minimap anklickbar für Teleportation (optional)

**Implementierung (1 Commit):**
- Minimap vollständig implementieren mit allen 9 Regionen
- Najika-Position live auf Minimap
- Farben entsprechend der Regionen

**Commit:** "Feature: Complete Minimap with 9 Regions + Live Position"

---

## 🎯 PHASE A3: DUNGEON-SYSTEM KOMPLETT

**Was:**
8 Dungeons auf Map (1 pro Region außer Berg).

**Vorbereitung:**
1. Finde Dungeon-Assets in najika_world.html
2. Check Dungeon-Loading Logic
3. Exit-Portal - wie funktioniert es?

**Implementierung (1 großer Commit):**
- 8 Dungeons platzieren
- Dungeon-Eingänge (Glowing Portal)
- E-Taste → Innenraum laden
- Exit-Portal im Dungeon
- Dungeon-Assets: Wände, Boden, Fackeln

**Wichtig:** Robust - keine Bugs beim Betreten/Verlassen.

**Commit:** "Feature: Dungeon System - 8 Dungeons"

---

## 🎯 PHASE A4: SCHWARZE MÜHLE (GÖTTERFELS)

**Was:**
Najika's Home auf Berg-Gipfel.

**Vorbereitung:**
1. Check regions.json → Götterfels
2. Mühlen-Design (Windmühle? Schwarz)
3. Innenraum: Bed, Crafting, Storage

**Implementierung (1 großer Commit):**
- Mühlen-Modell auf Gipfel (X=0, Z=0, Y=15)
- E-Taste → betreten
- Innenraum (Safe Zone)
- Möbel: Bed, Crafting Table, Chest
- Fluss vom Berg (visuell - blaue Linie)
- Exit zurück zur Map

**Commit:** "Feature: Schwarze Mühle - Home"

---

## 🏙️ PHASE A5: STADT-ICONS & POSITIONEN

**Was:**
Städte auf Map sichtbar (noch nicht betreten).

**Vorbereitung:**
1. Lies `entwicklung/data/cities.json`
2. Welche Region = welche Stadt?
3. Icon-Design (Tower? Flagge?)

**Implementierung (1 großer Commit):**
- Stadt-Positionen aus cities.json laden
- 8 Stadt-Icons platzieren
- Icon-Design: Glowing Beacon oder Häuser-Cluster
- Stadt-Name als Label
- Entfernung zur nächsten Stadt im UI

**Städte:**
1. Wüstenstadt (Wüste)
2. Hafenstadt (Küste)
3. Waldstadt (Wald)
4. Vulkanstadt (Vulkan)
5. Eisstadt (Eis)
6. Hochebenenstadt (Hochebene)
7. Sumpfstadt (Sumpf)
8. Höhlenstadt (Höhlen)

**Commit:** "Feature: City Icons - 8 cities"

---

## 🏙️ PHASE A6: STADT-EINTRITT SYSTEM

**Was:**
Mit E-Taste Stadt betreten.

**Vorbereitung:**
1. Check wie Dungeon-Eintritt funktioniert
2. Loading Screen Design
3. Wie Stadt-Szene laden?

**Implementierung (1 großer Commit):**
- Nähe-Check: < 10m → Icon leuchtet
- E-Taste zeigt "Drücke E zum Betreten"
- Loading Screen "Betrete [Stadt]..."
- Stadt-Innenbereich laden (eigene Szene)
- Transition smooth

**Commit:** "Feature: City Entry System"

---

## 🏙️ PHASE A7: STADT-INNENBEREICH (TEMPLATE)

**Was:**
Standard-Stadt-Layout (für alle 8 Städte).

**Vorbereitung:**
1. Stadt-Größe? (z.B. 200x200)
2. Straßen-Layout (Grid oder organisch?)
3. Gebäude-Positionen festlegen

**Implementierung (1 großer Commit):**
- Stadt-Layout: Straßen + Plätze
- 10-15 Gebäude pro Stadt (Primitives OK)
- Gebäude OHNE E betreten (durchlaufen)
- NPCs (statisch - einfach Kapseln)
- Exit-Portal zurück zur Map
- Template für alle 8 Städte kopierbar

**Commit:** "Feature: City Interior Template"

---

## 🏙️ PHASE A8: GEBÄUDE-TYPEN & FUNKTIONEN

**Was:**
Verschiedene Gebäude mit Funktionen.

**Vorbereitung:**
1. Gebäude-Typen definieren
2. Innenräume - wie komplex?
3. NPCs - Interaktion?

**Implementierung (1-2 große Commits):**

**Standard-Gebäude (alle Städte):**
- Wohnhäuser (3-5 Stück) - nur visuell
- Shop (Händler-NPC inside)
- Taverne (Essen kaufen)
- Werkstatt (Crafting)
- Rathaus (Quest-Giver NPC)

**Spezial-Gebäude pro Region:**
- Wüste: Oase, Karawanserei
- Küste: Hafen, Leuchtturm
- Wald: Jäger-Hütte
- Vulkan: Schmiede, Lava-Grube
- Eis: Iglu-Cluster
- Hochebene: Observatorium
- Sumpf: Stelzen-Häuser
- Höhlen: Kristall-Mine

**Commit 1:** "Feature: Standard Buildings"
**Commit 2:** "Feature: Special Buildings per Region"

---

## 🖥️ PHASE A9: DIGIVICE - MAP MODUL

**Was:**
Vollbild-Karte in Digivice.

**Vorbereitung:**
1. Check Digivice UI-Struktur
2. Wie Map rendern? (Canvas? Three.js?)
3. Marker-System

**Implementierung (1 großer Commit):**
- Map-Button in Digivice → Fullscreen Map
- 9 Regionen dargestellt (3x3 Grid)
- Najika-Position live (Dot)
- Stadt-Marker anklickbar (Teleport später)
- Dungeon-Marker
- Zoom In/Out
- Wegpunkt setzen (Kompass in 3D-Welt)

**Commit:** "Feature: Digivice Map Module"

---

## 🖥️ PHASE A10: DIGIVICE - INVENTORY

**Was:**
Rucksack-System.

**Vorbereitung:**
1. Item-Datenstruktur definieren
2. Wo Items speichern? (localStorage?)
3. Item-Icons wo her?

**Implementierung (1 großer Commit):**
- Inventory-Button → öffnet Rucksack
- 20 Item-Slots (Grid)
- Items anzeigen (Icon + Name + Anzahl)
- Item-Details bei Click
- Item benutzen (z.B. Essen → Hunger +10)
- Item wegwerfen
- Item-Gewicht/Limit (optional)

**Commit:** "Feature: Inventory System"

---

## 🖥️ PHASE A11: DIGIVICE - CHARACTER STATS

**Was:**
Charakter-Status anzeigen.

**Vorbereitung:**
1. Stats-System definieren (HP, Stamina, etc.)
2. Wo speichern?
3. Level-Up Mechanik?

**Implementierung (1 großer Commit):**
- Stats-Button → Character Sheet
- Level anzeigen
- XP-Bar (bis nächstes Level)
- Stats: HP, Stamina, Strength, Defense
- Equipment Slots (Waffe, Rüstung, Accessoire)
- Skills/Abilities Liste

**Commit:** "Feature: Character Stats Module"

---

## 🖥️ PHASE A12: DIGIVICE - QUESTS

**Was:**
Quest-Log System.

**Vorbereitung:**
1. Quest-Datenstruktur
2. Quest-Fortschritt tracken wie?
3. Quest-Giver NPCs

**Implementierung (1 großer Commit):**
- Quests-Button → Quest-Log
- Aktive Quests (max 5)
- Quest-Beschreibung
- Quest-Ziele (z.B. "3/10 Items")
- Quest abschließen → Belohnung
- Quest-Giver NPCs in Städten

**Commit:** "Feature: Quest System"

---

## 🖥️ PHASE A13: DIGIVICE - CRAFTING

**Was:**
Crafting-System.

**Vorbereitung:**
1. Rezepte definieren (JSON?)
2. Crafting-Stations wo?
3. Item-Kombinationen

**Implementierung (1 großer Commit):**
- Crafting-Button → Rezept-Liste
- Rezepte anzeigen (benötigte Items)
- Craft-Button (wenn Items vorhanden)
- Item wird erstellt → Inventory
- Crafting-Station-Check (z.B. in Mühle)

**Commit:** "Feature: Crafting System"

---

## 🖥️ PHASE A14: DIGIVICE - SETTINGS

**Was:**
Einstellungen.

**Implementierung (1 Commit):**
- Settings-Button → Einstellungen
- Graphics Quality (Low/Med/High)
- Sound Volume (Master, Music, SFX)
- Controls (WASD, Gamepad)
- Language (DE/EN)
- Save/Load Game

**Commit:** "Feature: Settings Module"

---

## 🎨 PHASE A15: VISUELLE POLISH

**Was:**
Map schöner machen.

**Implementierung (1-2 Commits):**
- Tag/Nacht-Zyklus (optional)
- Schatten optimieren
- Partikel: Rauch (Vulkan), Schnee (Eis), Nebel (Sumpf)
- Wasser-Animation (Küste, Fluss)
- Bessere 3D-Modelle (wo nötig)
- Texturen statt Farben

**Commit 1:** "Polish: Visual Effects"
**Commit 2:** "Polish: Better Models & Textures"

---

## 🧪 PHASE A16: TESTING & BUGFIXES

**Was:**
Alles testen und fixen.

**Testing:**
1. Performance: FPS > 30?
2. Alle Features funktionieren?
3. Mobile: Touch-Controls OK?
4. Keine Console-Errors?

**Bugfixes:**
- Najika fällt nicht durch Boden
- Kamera clippt nicht durch Wände
- UI überlappen sich nicht
- Stadt/Dungeon-Transitions smooth

**Commits:** "Fix: [Bug beschreibung]"

---

## 🤖 PHASE B: NAJIKA KI INTEGRATION

**NUR wenn Phase A komplett fertig!**

### B1: Living System Backend Check
- Auto-Care läuft?
- Mood-System funktioniert?
- Anger-System aktiv?

### B2: Digivice ↔ Backend Sync
- Tamagotchi-Werte vom Backend holen
- Änderungen an Backend senden
- WebSocket für Real-Time (optional)

### B3: KI-Antworten
- Najika antwortet auf Fragen
- Kontext-Awareness (weiß wo sie ist)
- Emotionale Antworten (Mood/Anger)

### B4: Training System
- Training-Session starten
- Trainings-Daten sammeln
- Fortschritt anzeigen

**Commits:** "Feature: Najika AI - [Teil]"

---

## 📊 PRIORITÄTEN

### JETZT (Phase A1-A5)
Basis fertig - Map funktioniert, Kamera OK, Städte/Dungeons sichtbar.

### DANACH (A6-A14)
Stadt-Interiors, Digivice-Module.

### POLISH (A15-A16)
Visuell verbessern, Bugs fixen.

### SPÄTER (Phase B)
Najika KI drauf.

---

## 🎯 ERFOLGS-KRITERIEN Phase A

**Phase A ist fertig wenn:**
- Najika läuft flüssig durch 9 Regionen
- Alle 8 Städte betreten und erkunden
- Dungeons funktionieren
- Digivice zeigt alle Module (außer Handy)
- FPS > 30
- Keine kritischen Bugs
- **BEREIT für Najika KI Integration**

---

## 🔧 ENTWICKLUNGS-RICHTLINIEN

### Commit-Messages Format
```
Feature: [Großes Feature]
Fix: [Bug]
Polish: [Visuell]
Test: [Was getestet]
```

### Vor jedem großen Commit
1. Alle betroffenen Files checken
2. Code durchdenken
3. Testen: WASD, Buttons, Console-Errors
4. Dann erst committen

### Code-Qualität
- Kommentare in Deutsch
- Klare Funktions-Namen
- Error-Handling immer
- Keine console.log in Production

---

**Viel Erfolg, Claude Web-Modelle! 🚀**

**Start mit PHASE A1: Third-Person Camera!**

---

## 📝 ZUSAMMENFASSUNG FÜR WEB-MODELLE

### Was ist die Basis?
- **Datei:** `digivice/najika_world_9regions_test.html`
- **Stand:** 9 Regionen funktionieren, Najika läuft mit WASD, Orbit-Kamera, Assets für 4 Regionen
- **Ziel:** Komplette Test-Map mit allen Features (OHNE Najika KI)

### Wie arbeiten?
1. **VOR jedem großen Feature:** Alle betroffenen Files lesen und verstehen
2. **GROSSE COMMITS:** Nicht häppchenweise, sondern komplette Features auf einmal
3. **TESTEN:** Nach jedem Feature: WASD testen, Console checken, FPS prüfen
4. **COMMIT:** Erst wenn alles funktioniert → dann committen

### Was ist wichtig?
- **Code-Qualität:** Kommentare in Deutsch, klare Funktionsnamen, Error-Handling
- **Performance:** FPS > 30 ist Pflicht
- **Mobile:** Touch-Controls müssen funktionieren
- **Keine Bugs:** Najika darf nicht durch Boden fallen, Kamera nicht clippen

### Wo sind die wichtigen Files?
- **Hauptdatei:** `digivice/najika_world_9regions_test.html`
- **Kamera:** `digivice/static/js/camera_controller.js`
- **Regionen:** `entwicklung/data/regions.json`
- **Städte:** `entwicklung/data/cities.json`
- **Biomes:** `entwicklung/data/biomes.json`
- **Assets:** `digivice/static/assets/` (kaykit, jellysquish)

### Welche Assets sind verfügbar?
- **KayKit:** Dungeon, Medieval, Nature - bereits in Test-Map verwendet
- **Jellysquish:** Oasis - bereits in Test-Map verwendet
- **Weitere:** In `digivice/static/assets/KayKit Mini-Game Variety Pack 1.2/Models/gltf/`

### Quick-Start für neues Web-Modell:
1. Lies diese Roadmap komplett durch
2. Öffne `najika_world_9regions_test.html` und verstehe den aktuellen Stand
3. Wähle PHASE A1 oder A2 (beides Priorität 1)
4. Lies alle relevanten Files durch
5. Plane das Feature komplett durch
6. Implementiere alles in 1-2 großen Commits
7. Teste gründlich
8. Commit mit Message: "Feature: [Feature-Name]"

---



## ⚔️ PHASE A17: KAMPF-SYSTEM

**Was:**
Turn-Based Combat (später fürs Handy-Spiel).

**Vorbereitung:**
1. Kampf-Mechanik definieren (Turn-Based? Action?)
2. Enemy-Stats System
3. Skill-System

**Implementierung (2-3 große Commits):**

**Commit 1: Combat UI**
- Kampf-Screen (Overlay oder eigene Szene?)
- HP-Bars (Najika + Enemy)
- Skill-Buttons (4-6 Skills)
- Turn-Indicator ("Dein Zug" / "Gegner-Zug")
- Damage-Numbers Animation

**Commit 2: Combat Logic**
- Turn-System (Abwechselnd angreifen)
- Damage-Berechnung (Attack - Defense)
- Skills mit verschiedenen Effekten (Heal, AoE, Buff)
- Critical Hits (Chance-based)
- Victory/Defeat Screen

**Commit 3: Enemy System**
- Enemies spawnen in Regionen (außer Berg)
- Enemy-Types pro Biom (aus biomes.json)
- Kampf starten bei Kollision
- Loot nach Kampf (Items, XP, Gold)

**Commits:**
- "Feature: Combat UI"
- "Feature: Combat Logic - Turn-Based"
- "Feature: Enemy System + Loot"

---

## 🎲 PHASE A18: EVENT-SYSTEM (OREGON TRAIL STYLE)

**Was:**
Random Events beim Reisen (wie Oregon Trail + Konosuba).

**Vorbereitung:**
1. Event-Typen definieren (Encounter, Choice, Disaster)
2. Event-Pool pro Region
3. Event-Trigger (Zeit? Distanz?)

**Implementierung (2 große Commits):**

**Commit 1: Event Engine**
- Event-Trigger System (z.B. alle 100m ein Event)
- Event-Screen (Overlay mit Text + Choices)
- Event-Datenstruktur (JSON)
- Event-Konsequenzen (HP-, Item+, etc.)

**Commit 2: Event-Content**
- 50+ Events schreiben:
  * Encounters: Banditen, Händler, NPCs
  * Choices: Helfen oder Ignorieren? 
  * Disasters: Sturm, Monster-Angriff
  * Funny: Konosuba-Style (Explosion Magic, Kazuma's Luck)
- Events pro Region unterschiedlich
- Event-Belohnungen/Strafen

**Commits:**
- "Feature: Event System Engine"
- "Content: 50+ Random Events"

---

## 🎮 PHASE A19: GAMEPLAY-MECHANIKEN

**Was:**
Alle weiteren Mechaniken fürs Handy-Spiel testen.

**Implementierung (jeweils 1 Commit pro Mechanik):**

### A19.1: Resource-Management
- Hunger/Thirst System (sinkt über Zeit)
- Essen konsumieren (aus Inventory)
- Game Over bei Hunger = 0

**Commit:** "Feature: Resource Management - Hunger/Thirst"

### A19.2: Resting System
- Bed in Mühle oder Taverne
- Schlafen → HP+, Time+
- Can't sleep wenn Enemies nearby

**Commit:** "Feature: Rest System"

### A19.3: Weather System
- Wetter pro Region (aus biomes.json)
- Wetter-Effekte: Regen (Sicht↓), Sturm (Damage)
- Wetter beeinflusst Events

**Commit:** "Feature: Weather System"

### A19.4: Time System
- Ingame-Zeit (Tag/Nacht)
- Zeitfortschritt beim Reisen
- Nacht = mehr Enemies

**Commit:** "Feature: Time System - Day/Night"

### A19.5: Party System (optional)
- Begleiter rekrutieren (NPCs)
- Party-Members in Kampf
- Party-Inventory geteilt

**Commit:** "Feature: Party System"

### A19.6: Reputation System
- Reputation pro Stadt
- Gute Taten → Rep+
- Bessere Preise bei hoher Rep

**Commit:** "Feature: Reputation per City"

---

## 📱 PHASE A20: MOBILE OPTIMIERUNG

**Was:**
Alles für Mobile-Play vorbereiten.

**Implementierung (1-2 Commits):**
- Touch-Controls optimieren
- UI-Elemente größer (für Finger)
- Performance-Optimierung (FPS auf Mobile)
- Portrait/Landscape Modes
- Virtual Joystick (optional)

**Commits:**
- "Mobile: Touch Controls + UI"
- "Mobile: Performance Optimization"

---

## 🎯 ERFOLGS-KRITERIEN KOMPLETT

**Test-Map ist 100% fertig wenn:**
- ✅ Alle Phasen A1-A20 abgeschlossen
- ✅ Map funktioniert flüssig (FPS > 30)
- ✅ Kampf-System funktioniert (Turn-Based)
- ✅ Events spawnen und funktionieren
- ✅ Alle Gameplay-Mechaniken laufen
- ✅ Mobile: Touch-Controls OK
- ✅ Keine kritischen Bugs
- ✅ **BEREIT für Handy-Spiel-Integration**

Dann erst → **PHASE B: Najika KI + Handy-Spiel Build**

---

**LOS GEHT'S! Start mit PHASE A1! 🚀**

---

## 🎯 QUICK REFERENCE - DIE WICHTIGSTEN INFOS

### Datei-Struktur:
```
digivice/
├── najika_world_9regions_test.html  ← HAUPTDATEI (aktuell)
├── najika_world_v2.html             ← Reference für Kamera-System
├── index.html                       ← Digivice UI (Tamagotchi etc.)
└── static/
    ├── js/
    │   ├── camera_controller.js     ← Kamera-Logik
    │   └── ...
    └── assets/
        ├── kaykit/                   ← 3D-Assets (Dungeon, Medieval, Nature)
        └── jellysquish/              ← 3D-Assets (Oasis)

entwicklung/data/
├── regions.json                     ← 9 Regionen-Definitionen
├── cities.json                      ← 8 Städte-Definitionen
└── biomes.json                      ← Biome-Eigenschaften
```

### Die 9 Regionen (3x3 Grid):
```
[Ice]     [Highland] [Desert]
[Swamp]   [Mountain] [Coast]
[Caves]   [Forest]   [Volcano]
```
- **Größe:** je 66.66 x 66.66 Einheiten
- **Berg (Mountain):** Y=5 (höher als andere)
- **Alle anderen:** Y=0 (flat)

### Najika Character:
- **Modell:** Bohne (Zylinder + 2 Halbkugeln)
- **Farbe:** Grün (#4CAF50)
- **Steuerung:** WASD + Shift (Sprint)
- **Position:** Startet in Mitte (Mountain-Region)
- **Höhe:** 3.5 Einheiten (passt sich automatisch an Region an)

### Assets Loading:
- **Aktuell:** 4 Regionen haben Assets (Oasis, Dungeon, Medieval, Nature)
- **Fehlt noch:** 5 Regionen brauchen Assets (Ice, Highland, Desert, Swamp, Coast, Caves, Forest, Volcano)
- **Format:** GLTF/GLB
- **Loader:** THREE.GLTFLoader

### Performance-Ziele:
- **FPS:** > 30 (Pflicht)
- **Shadow Quality:** 4096x4096 (bereits implementiert)
- **Fog:** Ja (100-300 Einheiten)
- **Anti-Aliasing:** Ja

### Testing-Checklist nach jedem Feature:
- [ ] WASD Movement funktioniert
- [ ] Kamera folgt Najika (wenn Third-Person)
- [ ] Keine Console-Errors (F12)
- [ ] FPS stabil > 30
- [ ] Najika fällt nicht durch Boden
- [ ] Assets laden korrekt
- [ ] UI zeigt korrekte Werte

### Commit-Message Format:
```
Feature: [Was wurde hinzugefügt]
Fix: [Was wurde gefixt]
Polish: [Visuell verbessert]
Test: [Was getestet]
```

---

**🎮 BEREIT FÜR ACTION? START MIT PHASE A1 ODER A2! 🚀**

