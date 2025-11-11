# 🤖 WEB-MODELL TODO: NAJIKA WORLD TESTWELT KOMPLETT SPIELBAR

**Ziel:** Testwelt komplett spielbar machen - ALLE Features implementiert, bevor Mobile-Transfer

**Arbeitsweise:** GROßE BLÖCKE - Vorbereiten, dann große Commits!

---

## 📋 PHASE 1: STÄDTE + E-TASTE ENTRANCE SYSTEM (PRIO 1)

### ✅ Vorbereitung (vor Coding)
- [ ] C:\Najika_World\digivice\data\cities.json komplett lesen (5 Städte, 247 Zeilen)
- [ ] C:\Najika_World\digivice\data\regions.json komplett lesen
- [ ] C:\Najika_World\digivice\index.html - E-Taste System analysieren (enterBuilding Funktion)
- [ ] C:\Najika_World\digivice\js\3d_scene.js - E-Taste Proximity System verstehen
- [ ] C:\Najika_World\digivice\najika_world_9regions_test.html - Schwarze Windmühle Code anschauen (Zeile 619-626)

### 🏗️ Implementierung (große Commits)

#### Block 1.1: E-Taste Proximity System in Test-Map
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] `buildings` Array erstellen (alle 5 Städte aus cities.json)
- [ ] `specialLocations` Array erstellen (3 besondere Orte)
- [ ] `nearBuilding` Variable + Proximity-Detection (Abstand < 5 Einheiten)
- [ ] E-Taste Event Listener (keydown 'e' oder 'E')
- [ ] `enterBuilding()` Funktion mit:
  - Exterior Position speichern
  - Fade-out Animation
  - Interior laden (später)
- [ ] `exitBuilding()` Funktion mit:
  - Zurück zu Exterior Position
  - Fade-in Animation
- [ ] UI Anzeige: "Drücke E zum Betreten: [Stadtname]"

**Test:** E-Taste bei allen 5 Städten + 3 Orten + Schwarze Windmühle = 9 Locations

#### Block 1.2: Stadt-Marker auf Minimap
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Minimap-Canvas erweitern (bereits vorhanden, muss erweitert werden)
- [ ] Stadt-Icons zeichnen (🏛️, 🌲, 🌊, ⛰️, 🌋)
- [ ] Special-Location Icons (❄️, 🧪, 🕳️)
- [ ] Schwarze Windmühle Icon (⚫)
- [ ] Hover-Tooltips mit Stadtnamen

**Test:** Alle 9 Locations auf Minimap sichtbar

#### Block 1.3: Stadt-Positionen platzieren (3D Meshes)
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Stadt-Meshes erstellen (BoxGeometry + Stadt-spezifische Farbe)
- [ ] Positionen aus cities.json verwenden:
  - Handelsfestung: x=8400, z=8200 → Umrechnung ins Grid-System
  - Dampf-Hain: x=4800, z=1500
  - Salzige Bucht: x=1500, z=4800
  - Runenheim: x=8400, z=4800
  - Funken-Siedlung: x=4800, z=8200
- [ ] userData setzen: `buildingName`, `buildingType`, `cityData`
- [ ] Zur Szene hinzufügen

**Test:** Alle 5 Städte sichtbar in korrekten Regionen

---

## 📋 PHASE 2: STADT-INTERIORS (ERSTE VERSION) (PRIO 1)

### ✅ Vorbereitung
- [ ] C:\Najika_World\digivice\data\cities.json - Alle "buildings" Sections lesen
- [ ] Fallout 76 Player-Shop Style recherchieren (Bilder/Videos)
- [ ] Spirited Away Restaurant Style recherchieren

### 🏗️ Implementierung

#### Block 2.1: Interior-Generation System
**Neue Datei:** `C:\Najika_World\digivice\static\js\interior_generator.js`

**WICHTIG:** Städte-Interiors sind GROß - 66.66 x 66.66 Einheiten (wie 1 ganzes Gebiet!)

- [ ] `InteriorGenerator` Klasse erstellen
- [ ] `generateCityInterior(cityData)` Funktion:
  - **Interior-Size: 66.66 x 66.66** (wie bei Schwarzer Windmühle, nur größer)
  - Boden-Plane (66.66 x 66.66, Stadt-spezifische Farbe)
  - Stadt-Layout generieren (Straßen, Plätze, Gebäude-Plots)
  - Gebäude platzieren:
    - Handelsfestung: 50 Gebäude (Trading Posts, Player Shops, Arena, Inn, Houses)
    - Dampf-Hain: 30 Gebäude (Onsen x3, Restaurants x5, Druid Huts x8, Houses x14)
    - Salzige Bucht: 35 Gebäude (Harbor Buildings x8, Fish Market, Lighthouse, Ships x5, Houses x20)
    - Runenheim: 20 Gebäude (Magic Academy, Rune Shops x3, Totems x5, Houses x11)
    - Funken-Siedlung: 25 Gebäude (Forges x5, Blacksmith, Lava Docks x2, Fireproof Houses x17)
  - Straßen-Grid (5x5 oder 7x7 Blöcke)
  - NPC-Positionen markieren (später NPCs spawnen)
  - Exit-Portal platzieren (am Rand, zurück zur Außenwelt)
  - Beleuchtung (PointLights bei Gebäuden, Straßenlaternen)

**Test:** Alle 5 Städte haben funktionale Interiors (66.66x66.66 groß)

#### Block 2.2: Interior-Loading in Test-Map
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] `interior_generator.js` via CDN/local einbinden
- [ ] `loadBuildingInterior(cityName)` implementieren:
  - Exterior-Objekte verstecken (visible = false)
  - Interior-Generator aufrufen (66.66x66.66 Stadt-Map)
  - Interior zur Szene hinzufügen
  - Character in Interior positionieren (Zentrum: 0, 0 relativ zum Interior)
  - Kamera in Interior positionieren (Third-Person Mode)
  - Lighting anpassen (Interior-Beleuchtung: AmbientLight + DirectionalLight)
  - Movement-Bounds setzen (66.66 x 66.66)
- [ ] `unloadBuildingInterior()` implementieren:
  - Interior-Objekte entfernen
  - Exterior wieder anzeigen
  - Character zurück zu gespeicherter Exterior Position
  - Kamera zurück zu Exterior Position
  - Movement-Bounds zurücksetzen (200 x 200)

**Test:** Betreten + Verlassen aller 5 Städte funktioniert, Stadt ist GROß (wie 1 Gebiet)

---

## 📋 PHASE 3: KAMPFSYSTEM INTEGRATION (PRIO 1)

### ✅ Vorbereitung
- [ ] C:\Najika_World\digivice\js\dungeon_combat.js komplett lesen
- [ ] C:\Najika_World\digivice\js\battle_core.js komplett lesen
- [ ] Combat-Flow verstehen (Turn-based? Real-time?)
- [ ] Enemy-Spawning Mechanismus verstehen

### 🏗️ Implementierung

#### Block 3.1: Kampfsystem Files einbinden
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] `<script src="/static/js/dungeon_combat.js"></script>` hinzufügen
- [ ] `<script src="/static/js/battle_core.js"></script>` hinzufügen
- [ ] Prüfen ob weitere Dependencies fehlen

#### Block 3.2: Enemy Spawning System
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] `enemies` Array erstellen
- [ ] Enemy-Typen definieren (pro Region unterschiedlich):
  - Ice: Eismenschen, Untote
  - Highland: Runen-Wächter
  - Desert: Sandwürmer, Banditen
  - Swamp: Hexen, Giftmonster
  - Mountain: Bergriesen
  - Coast: Piraten, Seemonster
  - Caves: Goblins
  - Forest: Waldgeister, Druiden (feindlich)
  - Volcano: Feuer-Elementare, Lava-Kreaturen
- [ ] `spawnEnemy(region, type, position)` Funktion
- [ ] Random Spawn-Points generieren (außerhalb von Städten)
- [ ] Enemy-Meshes erstellen (BoxGeometry + Region-Farbe + Größe)
- [ ] Enemy-AI (später): Patrouillieren, Aggro-Range

**Test:** Jede Region hat 5-10 Gegner

#### Block 3.3: Combat Trigger System
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Proximity-Detection: Najika < 3 Einheiten zu Enemy
- [ ] Combat-Start Trigger (automatisch oder mit Taste?)
- [ ] `startCombat(enemy)` Funktion:
  - Game-Loop pausieren
  - Combat-UI anzeigen
  - dungeon_combat.js initialisieren
  - Turn-System starten
- [ ] `endCombat(result)` Funktion:
  - Sieg: Enemy entfernen, Loot droppen, XP geben
  - Niederlage: Najika respawnt an letzter Stadt
  - Game-Loop fortsetzen

**Test:** Combat gegen 5 verschiedene Gegner-Typen

#### Block 3.4: Combat UI
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Combat-Overlay (fullscreen, halbtransparent)
- [ ] HP-Bars (Najika + Enemy)
- [ ] Action-Buttons:
  - Angriff
  - Verteidigung
  - Items nutzen
  - Fliehen
- [ ] Damage-Numbers (floating text)
- [ ] Combat-Log (letzte 5 Aktionen)

**Test:** UI ist übersichtlich und reagiert auf Klicks

---

## 📋 PHASE 4: ESSEN-SYSTEM + BUFFS (PRIO 2)

### ✅ Vorbereitung
- [ ] C:\Najika_World\digivice\data\cities.json - Alle "foodSpeciality" Sections lesen
- [ ] Buff-System Design:
  - Strength, Stamina, Combat Power
  - HP Regen, Water Resistance, Swimming
  - Dauer? Stack? Überschreiben?

### 🏗️ Implementierung

#### Block 4.1: Food-Items System
**Neue Datei:** `C:\Najika_World\digivice\static\js\food_system.js`

- [ ] `FoodItem` Klasse:
  - name, type, price, buffs, duration
  - `consume(player)` Funktion
- [ ] Alle Food-Items aus cities.json laden:
  - Handelsfestung: FLEISCH (Arena-Happen, Champion-Keule, etc.)
  - Dampf-Hain: GEDÄMPFTE BRÖTCHEN (Baozi, Manju, Hefeklöße)
  - Salzige Bucht: SALZFISCH (Dried, Fresh, Stew)
  - Runenheim: ? (noch nicht definiert)
  - Funken-Siedlung: ? (noch nicht definiert)
- [ ] `foodVendors` Array (Position in jeder Stadt)

#### Block 4.2: Buff-System
**Datei:** `C:\Najika_World\digivice\static\js\food_system.js`

- [ ] `BuffManager` Klasse:
  - `activeBuffs` Map
  - `addBuff(type, value, duration)` Funktion
  - `removeBuff(type)` Funktion
  - `updateBuffs(delta)` - Timer-System
  - `getBuffValue(type)` - Aktueller Buff-Wert
- [ ] Buff-UI (oben rechts):
  - Aktive Buffs anzeigen
  - Timer countdown
  - Icons (🍖 = Strength, 🛡️ = Stamina, etc.)

#### Block 4.3: Food-Shop UI
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Food-Vendor Interaktion (E-Taste bei Vendor)
- [ ] Shop-UI Overlay:
  - Food-Items Liste
  - Preis, Buff-Info
  - Kaufen-Button
  - Geld-System (Gold Counter)
- [ ] `buyFood(foodItem)` Funktion:
  - Gold abziehen
  - Item ins Inventar
  - Feedback (Sound, Animation)

**Test:** Food kaufen in allen 5 Städten, Buffs aktiv

---

## 📋 PHASE 5: INVENTAR-SYSTEM (PRIO 2)

### 🏗️ Implementierung

#### Block 5.1: Inventar-Backend
**Neue Datei:** `C:\Najika_World\digivice\static\js\inventory_system.js`

- [ ] `Inventory` Klasse:
  - `items` Array (max 50?)
  - `addItem(item)` Funktion
  - `removeItem(itemId)` Funktion
  - `useItem(itemId)` Funktion
  - `getItemCount(type)` Funktion
- [ ] Item-Typen:
  - Food (aus food_system.js)
  - Waffen (aus Combat-Loot)
  - Rüstung (aus Combat-Loot)
  - Quest-Items
  - Materialien (Crafting, später)

#### Block 5.2: Inventar-UI
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Inventar-Taste (I oder TAB)
- [ ] Inventar-Overlay (Grid-Layout):
  - Item-Slots (50 Stück)
  - Item-Icons (Platzhalter: BoxGeometry)
  - Item-Namen + Anzahl
  - Rechtsklick: Nutzen
  - Linksklick: Details anzeigen
- [ ] Item-Details Panel:
  - Name, Beschreibung
  - Stats (bei Waffen/Rüstung)
  - Buffs (bei Food)
  - Buttons: Nutzen, Droppen, Abbrechen

**Test:** Inventar öffnen, Items nutzen, Buffs aktivieren

---

## 📋 PHASE 6: NPC-SYSTEM (PRIO 2)

### 🏗️ Implementierung

#### Block 6.1: NPC-Generator
**Neue Datei:** `C:\Najika_World\digivice\static\js\npc_system.js`

- [ ] `NPC` Klasse:
  - name, type (vendor, quest_giver, trainer, etc.)
  - position, mesh
  - dialogue (Textzeilen)
  - inventory (bei Vendors)
  - quests (bei Quest-Givern)
- [ ] NPC-Typen aus cities.json:
  - Handelsfestung: 20 Händler, Arena-Meister
  - Dampf-Hain: Druiden, Restaurant-Besitzer, Onsen-Meister
  - Salzige Bucht: Fischer, Kapitäne, Leuchtturm-Wächter
  - Runenheim: Magier-Lehrer, Runen-Verkäufer
  - Funken-Siedlung: Meister-Schmied, Forge-Arbeiter

#### Block 6.2: NPC-Spawning in Städten
**Datei:** `C:\Najika_World\digivice\static\js\interior_generator.js`

- [ ] `spawnNPCs(cityData)` Funktion
- [ ] NPCs in Interiors platzieren:
  - Vendors in Shops
  - Quest-Giver in zentralen Plätzen
  - Trainer in Academies/Forges
- [ ] NPC-Meshes (CapsuleGeometry + Stadt-Farbe)
- [ ] NPC-Nameplate (über dem Kopf)

#### Block 6.3: NPC-Interaktion
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Proximity-Detection (Najika < 2 Einheiten zu NPC)
- [ ] UI: "Drücke E zum Sprechen: [NPC Name]"
- [ ] Dialogue-System:
  - Dialogue-Overlay (Textbox unten)
  - NPC Portrait (links)
  - Dialogue-Text (rechts)
  - Antwort-Optionen (Multiple Choice)
  - Weiter-Button / ESC zum Schließen
- [ ] Vendor-Dialogue → Shop-UI öffnen
- [ ] Quest-Giver-Dialogue → Quest annehmen

**Test:** Mit 5 verschiedenen NPC-Typen sprechen

---

## 📋 PHASE 7: QUEST-SYSTEM (PRIO 3)

### 🏗️ Implementierung

#### Block 7.1: Quest-Backend
**Neue Datei:** `C:\Najika_World\digivice\static\js\quest_system.js`

- [ ] `Quest` Klasse:
  - id, name, description
  - type (kill, collect, talk, explore)
  - objectives (Array von Sub-Zielen)
  - rewards (Gold, Items, XP)
  - status (available, active, completed)
- [ ] Quests aus cities.json:
  - Dampf-Hain: "forest_secrets", "nature_magic"
  - Andere Städte: Quests definieren
- [ ] `QuestManager` Klasse:
  - `activeQuests` Array
  - `completedQuests` Array
  - `acceptQuest(questId)` Funktion
  - `updateQuest(questId, progress)` Funktion
  - `completeQuest(questId)` Funktion

#### Block 7.2: Quest-UI
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Quest-Log Taste (Q oder J)
- [ ] Quest-Log Overlay:
  - Aktive Quests Liste (links)
  - Quest-Details (rechts):
    - Name, Beschreibung
    - Objectives (mit Checkboxen)
    - Rewards
    - Abbrechen-Button
- [ ] Quest-Tracker (oben rechts):
  - Aktuell getrackte Quest
  - Objectives + Fortschritt
  - Auto-Update bei Progress

#### Block 7.3: Quest-Progress Tracking
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Quest-Hooks einbauen:
  - Enemy getötet → Kill-Quests updaten
  - Item gesammelt → Collect-Quests updaten
  - NPC gesprochen → Talk-Quests updaten
  - Region betreten → Explore-Quests updaten
- [ ] Quest-Complete Notification (Popup):
  - "Quest abgeschlossen: [Name]"
  - Rewards anzeigen
  - Zum Quest-Geber zurückkehren (oder Auto-Complete)

**Test:** 3 verschiedene Quests (Kill, Collect, Talk) abschließen

---

## 📋 PHASE 8: SPEZIAL-FEATURES (PRIO 3)

### Block 8.1: PvP Arena (Handelsfestung)
**Datei:** `C:\Najika_World\digivice\static\js\interior_generator.js`

- [ ] Arena-Interior generieren (großer Kreis, 100 Capacity)
- [ ] Arena-Modi aus cities.json:
  - Hardcore (permadeath Items)
  - Normal (normale Regeln)
  - Softy (kein Item-Loss)
- [ ] Arena-Entrance (E-Taste)
- [ ] PvP-Toggle (später, wenn Multiplayer)

**Test:** Arena-Interior betreten, Modi-Auswahl

### Block 8.2: Player Shops (Handelsfestung, Fallout 76 Style)
**Datei:** `C:\Najika_World\digivice\static\js\interior_generator.js`

- [ ] 15 Player-Shop Gebäude generieren
- [ ] Shop-Interiors (leer, später Player-Items platzieren)
- [ ] Shop-Ownership System (später, wenn Multiplayer)

**Test:** Alle 15 Shops betreten

### Block 8.3: Onsen (Dampf-Hain, Healing Zones)
**Datei:** `C:\Najika_World\digivice\static\js\interior_generator.js`

- [ ] 3 Onsen-Gebäude generieren
- [ ] Onsen-Interiors (Wasser-Pools, Dampf-Partikel)
- [ ] Healing-Zone:
  - Proximity-Detection (im Pool)
  - HP Regen +10/sec
  - Buff: "Comfort" (+5% alle Stats, 10 Min)
- [ ] Onsen-UI: "Heilung aktiv... HP +10/s"

**Test:** In Onsen gehen, HP regeneriert

### Block 8.4: Leuchtturm (Salzige Bucht, Climbable)
**Datei:** `C:\Najika_World\digivice\static\js\interior_generator.js`

- [ ] Leuchtturm-Interior (Treppe nach oben)
- [ ] Climb-Mechanik:
  - Treppen-Collider
  - Auto-Climb (Character steigt automatisch)
  - Oder: Manual-Climb (Taste gedrückt halten)
- [ ] Leuchtturm-Top:
  - Aussichtsplattform
  - View-Point (Kamera-Effekt: Zoom out, Panorama)

**Test:** Leuchtturm erklimmen, Aussicht genießen

### Block 8.5: Magie-Akademie (Runenheim, Skill Trainer)
**Neue Datei:** `C:\Najika_World\digivice\static\js\skill_system.js`

- [ ] `Skill` Klasse:
  - name, type (rune_magic, lightning_magic)
  - level (1-10)
  - xp, xpRequired
- [ ] Skills aus cities.json:
  - Rune Magic (Runenheim)
  - Lightning Magic (Runenheim)
  - Nature Magic (Dampf-Hain, Quest)
- [ ] Skill-Trainer NPC:
  - Dialogue: Skill lernen
  - Kosten: Gold + Level-Requirement
  - `learnSkill(skillName)` Funktion
- [ ] Skill-UI (Skills Tab im Character-Menu)

**Test:** Skill lernen bei Trainer, Skill-UI anzeigen

### Block 8.6: Schmiede (Funken-Siedlung, Crafting)
**Neue Datei:** `C:\Najika_World\digivice\static\js\crafting_system.js`

- [ ] `Recipe` Klasse:
  - name, type (weapon, armor)
  - materials (Array: {item, count})
  - result (Item)
- [ ] Recipes aus cities.json:
  - Legendary Weapons (Funken-Siedlung)
  - Legendary Armor (Funken-Siedlung)
- [ ] Crafting-UI (bei Schmied):
  - Recipe-Liste
  - Material-Anforderungen (grün = vorhanden, rot = fehlt)
  - Craften-Button
  - Preview (Item-Stats)
- [ ] `craftItem(recipeId)` Funktion:
  - Materialien abziehen
  - Item erstellen
  - Ins Inventar

**Test:** 1 Waffe + 1 Rüstung craften

---

## 📋 PHASE 9: BESONDERE ORTE (PRIO 3)

### Block 9.1: Reich der Drei (Ice, Undead Territory)
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Keine Stadt, aber Special Location
- [ ] Untote-Spawning (10+ Undead Enemies)
- [ ] Nekromanten-Boss (Elite Enemy)
- [ ] Entrance: Großes Tor (E-Taste)
- [ ] Interior: Dunkle Halle, Eis-Kristalle
- [ ] Loot: Legendary Ice Weapons

**Test:** Betreten, gegen Untote kämpfen, Boss besiegen

### Block 9.2: Funkelnest (Swamp, Hidden Treasure Cave)
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Versteckte Höhle (schwer zu finden, im Sumpf)
- [ ] Entrance: Kleines Loch im Boden (E-Taste)
- [ ] Interior: Höhle mit Schätzen
- [ ] Hexen-Patrouille (Feinde)
- [ ] Treasure Chests (10 Stück):
  - Random Loot (Gold, Items, Rare Materials)
  - 1x Legendary Item garantiert
- [ ] Respawn-Timer (Chests respawnen nach 24h?)

**Test:** Höhle finden, Schätze sammeln

### Block 9.3: Tiefenhöhlen (Caves, Goblin Settlements)
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] Mehrere Goblin-Dörfer (3-5 Siedlungen)
- [ ] Goblin-NPCs (neutral, nicht feindlich)
- [ ] Goblin-Händler (verkaufen rare Materialien)
- [ ] Goblin-Quests:
  - "Bring mir 10 Pilze"
  - "Töte den Höhlen-Boss"
- [ ] Höhlen-Boss (Elite Goblin-King)
- [ ] Loot: Goblin-Waffen (Special Stats)

**Test:** Mit Goblins handeln, Quest annehmen, Boss besiegen

---

## 📋 PHASE 10: POLISH + FINAL TESTING (PRIO 4)

### Block 10.1: Performance-Optimierung
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] LOD (Level of Detail) für Meshes
- [ ] Frustum Culling (nur sichtbare Objekte rendern)
- [ ] Enemy-Pooling (Objekte wiederverwenden)
- [ ] Texture-Compression
- [ ] FPS-Counter (Performance-Monitoring)

### Block 10.2: Sound-System
**Neue Datei:** `C:\Najika_World\digivice\static\js\sound_system.js`

- [ ] Ambient-Sounds (pro Region):
  - Ice: Wind
  - Forest: Vögel
  - Coast: Wellen
  - Volcano: Lava-Blubbern
- [ ] UI-Sounds:
  - Button-Click
  - Door-Open
  - Combat-Hit
  - Level-Up
- [ ] Music (später, wenn vorhanden)

### Block 10.3: Speichersystem
**Datei:** `C:\Najika_World\backend\saves\najika_state.json`

- [ ] Auto-Save (alle 60 Sekunden)
- [ ] Save-Data:
  - Najika Position
  - Inventar
  - Quests (active, completed)
  - Skills
  - Gold
  - Buffs
  - Enemy-States (getötet oder nicht)
- [ ] Load-Data beim Start
- [ ] Save/Load-UI (Speichern, Laden, Löschen)

**Test:** Spiel speichern, neu laden, alles ist da

### Block 10.4: Tutorial-System
**Datei:** `C:\Najika_World\digivice\najika_world_9regions_test.html`

- [ ] First-Time-Launch Detection
- [ ] Tutorial-Popups:
  - "WASD zum Bewegen"
  - "E zum Interagieren"
  - "Tab für Inventar"
  - "Maus für Kamera"
- [ ] Tutorial-Quest: "Erkunde die erste Stadt"

### Block 10.5: Bug-Fixing + Final Testing
- [ ] Alle Features durchspielen
- [ ] Edge-Cases testen:
  - Teleport während Combat
  - Inventar voll
  - Negative Gold
  - Quest-Abbruch
  - Save/Load während Combat
- [ ] Browser-Kompatibilität (Chrome, Firefox, Safari)
- [ ] Mobile-Kompatibilität (Touch-Controls)

---

## 📋 PHASE 11: MOBILE-TRANSFER (PRIO 5, SPÄTER)

**Erst wenn Testwelt 100% fertig ist!**

- [ ] C:\Najika_World\digivice\index.html - Alle Features übertragen
- [ ] Mobile-Optimierungen
- [ ] Touch-UI anpassen
- [ ] Performance-Anpassungen

---

## ✅ SUCCESS-KRITERIEN (TESTWELT KOMPLETT SPIELBAR)

- [x] 9 Regionen begehbar (DONE)
- [x] WASD Movement (DONE)
- [x] Kamera-Modi (DONE)
- [ ] 5 Städte + E-Taste Entrance
- [ ] 3 Besondere Orte + E-Taste Entrance
- [ ] Schwarze Windmühle + E-Taste Entrance
- [ ] Kampfsystem funktioniert (5+ Kämpfe gewonnen)
- [ ] Essen-System funktioniert (5+ Foods gegessen, Buffs aktiv)
- [ ] Inventar funktioniert (50 Items gesammelt)
- [ ] NPCs funktionieren (5+ Dialoge geführt)
- [ ] Quests funktionieren (3+ Quests abgeschlossen)
- [ ] Special Features funktionieren:
  - PvP Arena betreten
  - Onsen heilt HP
  - Leuchtturm erklommen
  - Skill gelernt
  - Item gecraftet
- [ ] Besondere Orte abgeschlossen:
  - Reich der Drei Boss besiegt
  - Funkelnest Treasure gesammelt
  - Goblin-Quest abgeschlossen
- [ ] Performance: 60 FPS konstant
- [ ] Speichern/Laden funktioniert

---

## 📊 ZEITSCHÄTZUNG (für Web-Modell)

| Phase | Aufwand | Commits |
|-------|---------|---------|
| Phase 1: Städte + E-Taste | 4-6 Stunden | 3 Commits |
| Phase 2: Interiors | 6-8 Stunden | 2 Commits |
| Phase 3: Kampfsystem | 8-10 Stunden | 4 Commits |
| Phase 4: Essen + Buffs | 4-6 Stunden | 2 Commits |
| Phase 5: Inventar | 4-6 Stunden | 2 Commits |
| Phase 6: NPCs | 6-8 Stunden | 3 Commits |
| Phase 7: Quests | 8-10 Stunden | 3 Commits |
| Phase 8: Special Features | 10-12 Stunden | 6 Commits |
| Phase 9: Besondere Orte | 6-8 Stunden | 3 Commits |
| Phase 10: Polish | 6-8 Stunden | 2 Commits |
| **GESAMT** | **62-82 Stunden** | **30 Commits** |

---

## 🎯 PRIORITÄTEN

**PRIO 1 (Must-Have):** Phasen 1-3
**PRIO 2 (Should-Have):** Phasen 4-6
**PRIO 3 (Nice-to-Have):** Phasen 7-9
**PRIO 4 (Polish):** Phase 10
**PRIO 5 (Later):** Phase 11

---

## 📝 ARBEITSWEISE-REMINDER

**VOR JEDEM BLOCK:**
1. Alle genannten Files KOMPLETT lesen
2. Code mental durchgehen
3. Struktur planen
4. Dann: GROßER COMMIT mit allem auf einmal

**KEIN HÄPPCHENWEISE!**
**KEINE HALBFERTIGEN FEATURES!**
**EIN FEATURE = EIN GROßER COMMIT!**

---

**Erstellt:** 2025-11-11
**Für:** Web-Modell (Claude Code Unlimited)
**Projekt:** Najika World - 9 Regions Test Map
