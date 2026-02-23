# BROWSER BETA - FERTIGSTELLUNGS-CHECKLIST 2026-02-15

**Erstellt von:** SONNET (Claude Sonnet 4.5)
**Zweck:** Was fehlt noch für die Browser Beta?
**Status:** 🟡 In Arbeit

---

## 📊 AKTUELLER STATUS

### ✅ Was FUNKTIONIERT (2026-02-15):

**Backend:**
- ✅ FastAPI auf Port 8001 läuft
- ✅ WebSocket-Verbindung funktioniert
- ✅ 135/350 Endpoints haben Error-Handling (38%)
- ✅ Performance-Monitoring aktiv
- ✅ World Data Loading (regions.json, biomes.json, cities.json)
- ✅ Chat-System V2
- ✅ Battle-System V2
- ✅ Quest-System V2
- ✅ Slime-System V3
- ✅ Housing-System
- ✅ Farming-System

**Frontend (OPUS Phase 2 - FERTIG!):**
- ✅ Quest Tracker V2 (Journal, Chains, Notifications)
- ✅ World Map 3D Viewer (Three.js, 8 Regionen, Fog of War)
- ✅ Skill Tree UI (Diablo-Style, Canvas, 6 Schulen)
- ✅ Housing UI V2 (Möbel-Katalog, Upgrade-System)
- ✅ Combat UI Polish (Damage Numbers, Combos, Screen Shake)
- ✅ NPC Dialogue UI (Visual Novel Style, Branching)
- ✅ Inventory UI V2 (Paperdoll, Drag&Drop, Tooltips)
- ✅ Crafting Minigame (Timing-Bar, Qualitäts-System)

**Game-Systeme:**
- ✅ 9.6km x 9.6km Open World (Battle Royale Scale)
- ✅ 9 Regionen + 5 Major Cities
- ✅ 40+ Enemy-Typen, 9 Bosse
- ✅ 230+ Items (Waffen, Rüstungen, Consumables)
- ✅ 10 Magic-Schools
- ✅ Learning-by-Doing Skill-System
- ✅ Arena-System (PvE Wellen)
- ✅ Overworld-Enemies mit Spawn-System

---

## ❌ WAS FEHLT FÜR BETA?

### 🔴 P0 - KRITISCH (BETA-BLOCKER):

#### 1. **GRUNDLEGENDE SPIELBARKEIT**

**Player-Movement & Controls:**
- ⬜ Spieler-Steuerung testen (WASD + Maus)
- ⬜ Kamera-Controls (Orbit, Zoom)
- ⬜ Collision-Detection funktioniert?
- ⬜ Teleporter zwischen Regionen funktionieren?

**Combat-System:**
- ⬜ Basis-Combat funktioniert? (Schwert, Magie)
- ⬜ Target-Lock-On System?
- ⬜ Skill-Cooldowns werden angezeigt?
- ⬜ Enemy-AI reagiert auf Spieler?

**UI-Integration:**
- ⬜ Alle UI-Panels öffnen/schließen ohne Fehler?
- ⬜ ESC-Menü funktioniert?
- ⬜ Hotkeys funktionieren? (I für Inventory, M für Map, etc.)

#### 2. **KRITISCHE BUGS CHECKEN**

**Console-Errors:**
- ⬜ Keine 404-Fehler beim Laden?
- ⬜ Keine JavaScript-Errors beim Spielstart?
- ⬜ WebSocket bleibt verbunden?

**Performance:**
- ⬜ FPS > 30 auf modernen PCs?
- ⬜ Kein Memory-Leak nach 10 Minuten spielen?
- ⬜ Keine Freeze beim Region-Wechsel?

#### 3. **TUTORIAL/INTRO**

- ❌ **FEHLT KOMPLETT!**
- ⬜ Spieler braucht Tutorial für Steuerung
- ⬜ Intro-Quest ("Willkommen in Schwarze Mühle")?
- ⬜ UI-Tour (zeigt wichtige Buttons)?

**Vorschlag:**
```
TUTORIAL-QUEST: "Najika's Erste Schritte"
1. Bewegung (WASD)
2. Kamera (Maus)
3. Angriff (Linksklick)
4. Skill nutzen (1-4 Tasten)
5. Inventory öffnen (I)
6. Quest-Log öffnen (J)
7. Map öffnen (M)
8. Ersten Gegner besiegen (Slime)
```

#### 4. **SAVE/LOAD SYSTEM**

- ⬜ Spieler-Progress wird gespeichert?
- ⬜ Auto-Save aktiv?
- ⬜ Load-Game beim Neustart funktioniert?

**Backend-Check nötig:**
- Ist `backend/api/state_v2.py` vollständig?
- Werden Position, Stats, Inventory gespeichert?

---

### 🟡 P1 - WICHTIG (sollte in Beta sein):

#### 5. **QUEST-CONTENT**

**Aktuell:** Nur ~10 Quests
**Beta braucht:** Min. 30 Quests

**Notwendig:**
- ⬜ Tutorial-Quest (5 Steps)
- ⬜ Main-Story-Arc (10 Quests)
- ⬜ Pro Region 2-3 Side-Quests (18 Quests)

#### 6. **NPC-DENSITY**

**Aktuell:** ~25-30 NPCs
**Beta braucht:** Min. 50 NPCs

**Verteilung:**
- ⬜ Schwarze Mühle: 15 NPCs (aktuell ~8)
- ⬜ Argentum: 20 NPCs (aktuell ~5)
- ⬜ Andere Cities: je 5 NPCs

#### 7. **BALANCING**

- ⬜ Enemy-HP/Damage balanciert?
- ⬜ Weapon-Damage sinnvoll? (Level 1 Schwert vs Level 50?)
- ⬜ Skill-Mana-Costs nicht zu hoch/niedrig?
- ⬜ Item-Preise festgelegt?

#### 8. **SOUND/MUSIC**

- ⬜ Background-Music für Regionen?
- ⬜ Combat-Sounds (Schwert, Magie)?
- ⬜ UI-Sounds (Click, Open/Close)?
- ⬜ Ambient-Sounds (Wald, Stadt, Wüste)?

---

### 🟢 P2 - NICE TO HAVE (kann nach Beta):

#### 9. **POLISH**

- ⬜ Loading-Screen mit Tipps
- ⬜ Settings-Menu (Grafik, Audio, Keybinds)
- ⬜ Achievements-System
- ⬜ Leaderboards (Arena)

#### 10. **MULTIPLAYER**

- ⬜ Co-Op funktioniert?
- ⬜ PvP-Arena?
- ⬜ Trading zwischen Spielern?

---

## 🧪 TESTING-PLAN FÜR BETA

### Test 1: **Fresh Start** (Neuer Spieler)
```
1. Browser öffnen → http://127.0.0.1:8001
2. Spiel lädt ohne Errors?
3. Tutorial startet automatisch?
4. Nach Tutorial: Spieler hat Basis-Waffe + 1 Skill?
5. Kann frei in Schwarze Mühle rumlaufen?
```

### Test 2: **Combat**
```
1. Ersten Enemy finden (Slime/Wolf)
2. Linksklick → Schwert-Angriff funktioniert?
3. Taste 1 → Magic-Skill funktioniert?
4. Enemy stirbt → Loot erscheint?
5. Loot aufheben → landet in Inventory?
```

### Test 3: **Quest-Flow**
```
1. NPC-Dialog öffnen
2. Quest annehmen
3. Quest-Ziel erreichen (z.B. 5 Slimes töten)
4. Zurück zum NPC
5. Quest abgeben → Belohnung (Gold + XP)?
```

### Test 4: **UI-Funktionalität**
```
1. Inventory öffnen (I) → Items sichtbar?
2. Item equip via Drag&Drop?
3. Map öffnen (M) → Position korrekt?
4. Skill Tree öffnen → Skills unlockbar?
5. Quest-Log (J) → Aktive Quests sichtbar?
```

### Test 5: **Save/Load**
```
1. 5 Minuten spielen (Quest machen, Items sammeln)
2. F5 (Browser-Reload)
3. Spiel lädt → Alles noch da? (Position, Items, Quest-Progress)
```

### Test 6: **Performance**
```
1. 10 Minuten in Open-World rumlaufen
2. FPS-Counter beobachten (sollte > 30 bleiben)
3. Memory-Usage im Task-Manager (sollte nicht steigen)
4. Region wechseln (Wald → Stadt) → Kein Freeze?
```

---

## 📝 NOTWENDIGE FIXES/ADDITIONS

### SOFORT (SONNET kann machen):

1. ⬜ **Save/Load System testen**
   - Backend-Endpoint `/api/state/save` + `/api/state/load` prüfen
   - Auto-Save alle 60 Sekunden aktivieren?

2. ⬜ **Tutorial-Quest implementieren** (Backend)
   - Quest-Daten in `backend/api/quest_v2.py` hinzufügen
   - 5-Step Tutorial-Chain

3. ⬜ **Error-Handling vervollständigen**
   - Restliche 215 Endpoints mit @handle_errors() sichern
   - Priorität: Movement, Combat, UI-Endpoints

4. ⬜ **Performance-Check**
   - `/api/performance/slowest` aufrufen
   - Endpoints > 500ms optimieren

### BALD (OPUS sollte machen):

5. ⬜ **20 neue Quests schreiben**
   - Tutorial: 1 Quest (5 Steps)
   - Main Story: 10 Quests
   - Side Quests: 9 Quests (pro Region 1-2)

6. ⬜ **30 neue NPCs erstellen**
   - Schwarze Mühle: +7 NPCs (Vendor, Guards, Citizens)
   - Argentum: +15 NPCs
   - Andere Cities: +8 NPCs

7. ⬜ **Item-Balancing**
   - Alle Waffen/Rüstungen Stats setzen
   - Vendor-Preise definieren
   - Drop-Rates für Enemies

8. ⬜ **Sound/Music Integration**
   - Background-Music für 9 Regionen
   - Combat-Sounds
   - UI-Feedback-Sounds

---

## 🎯 BETA-KRITERIEN (Definition of Done)

### MINIMUM (MVP Beta):
- ✅ Spieler kann rumlaufen ohne Errors
- ⬜ Combat funktioniert (Schwert + 1 Magic-Skill)
- ⬜ Mind. 1 Quest spielbar (Tutorial)
- ⬜ Mind. 1 NPC gibt Quest
- ⬜ Save/Load funktioniert
- ⬜ Keine Console-Errors
- ⬜ FPS > 30

### VOLLSTÄNDIGE BETA:
- ⬜ Tutorial-Quest komplett
- ⬜ 30 Quests spielbar
- ⬜ 50+ NPCs in der Welt
- ⬜ 9 Regionen erkundbar
- ⬜ Combat balanciert
- ⬜ Sound/Music vorhanden
- ⬜ Settings-Menu
- ⬜ Auto-Save

---

## 🚀 NÄCHSTE SCHRITTE (PRIORISIERT)

### SONNET macht (1-2 Tage):
1. ⬜ **Live-Testing** - Browser öffnen, 30 Minuten spielen, Bugs notieren
2. ⬜ **Save/Load System prüfen** - Funktioniert es?
3. ⬜ **Tutorial-Quest Backend** - 5-Step Quest anlegen
4. ⬜ **Error-Handling vervollständigen** - P2 Endpoints (215 übrig)
5. ⬜ **Performance-Audit** - Slow Endpoints fixen

### OPUS macht (2-3 Tage):
1. ⬜ **Tutorial-Quest Content** - Dialog schreiben, Steps definieren
2. ⬜ **20 neue Quests** - Story + Side-Quests
3. ⬜ **30 neue NPCs** - Namen, Dialoge, Positionen
4. ⬜ **Item-Balancing** - Stats, Preise, Drop-Rates
5. ⬜ **Sound-Integration** - Music + SFX einbinden

---

## ❓ OFFENE FRAGEN

1. **Was ist der Beta-Release-Termin?**
   - Wenn wir wissen wann, können wir priorisieren!

2. **Welche Features MÜSSEN in Beta sein?**
   - Tutorial? Main-Story? Oder reicht "rumlaufen und erkunden"?

3. **Wie viel Content ist genug für Beta?**
   - 10 Quests? 30 Quests? 50 Quests?

4. **Multiplayer in Beta oder später?**
   - Co-Op System existiert, aber muss getestet werden

5. **Sound/Music Priorität?**
   - Können wir ohne Music in Beta gehen?
   - Oder ist Sound kritisch für Experience?

---

**Bereit für Live-Testing oder soll ich spezifische Features prüfen?**
