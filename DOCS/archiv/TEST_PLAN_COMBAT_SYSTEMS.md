# 🎮 COMBAT SYSTEMS - TEST PLAN
**Datum:** 2026-02-17
**Status:** UnifiedCombat entfernt, Real3DCombat als einziges System

---

## ✅ ABGESCHLOSSEN

### 1. **UnifiedCombat komplett entfernt**
- ❌ Alle `window.UnifiedCombat` Referenzen gelöscht
- ✅ Nemesis Arena → Real3DCombat
- ✅ Slime Arena → Real3DCombat (AUTO/CHEER)
- ✅ Overworld → Real3DCombat

### 2. **CHEER-System erweitert**
- ✅ Funktioniert in allen Modi (MANUAL/AUTO/CHEER)
- ✅ Tasten 1-4 für Buffs
- ✅ Perfekt für Slime-Begleiter

### 3. **SPECIAL Stats integriert**
- ✅ POW, INT, AGI, VIT, WIL, LUK, PER
- ✅ Damage-Berechnung angepasst
- ✅ Hit Chance, Crit Chance implementiert

### 4. **Touch-Controls integriert**
- ✅ Direkte Events zu Real3DCombat
- ✅ touchAttack, touchDodge, touchBlock, touchParry

### 5. **Alle Scripts geladen**
- ✅ 17 UI-Systeme hinzugefügt
- ✅ Overworld-Systeme hinzugefügt
- ✅ Arena-Systeme hinzugefügt
- ✅ Slime-Systeme hinzugefügt

---

## 🧪 TEST-CHECKLISTE

### **A. OVERWORLD COMBAT**

#### Test 1: Enemy Encounter
- [ ] **In Browser öffnen:** `http://localhost:8001/najika_world_UNIFIED.html`
- [ ] **Warten bis Welt lädt** (3D-Scene initialisiert)
- [ ] **Auf Gegner zulaufen**
- [ ] **ERWARTUNG:** Gegner spawnt, aggro, Combat startet
- [ ] **PRÜFEN:** Real3DCombat HUD erscheint
- [ ] **PRÜFEN:** Gegner-Mesh bleibt sichtbar (kein Verschwinden!)
- [ ] **PRÜFEN:** Q/E Angriffe funktionieren
- [ ] **PRÜFEN:** Space für Dodge funktioniert

#### Test 2: CHEER-System
- [ ] **Im Combat:** M-Taste drücken
- [ ] **ERWARTUNG:** Modus wechselt MANUAL → AUTO → CHEER
- [ ] **Im CHEER-Modus:** Taste 1 drücken
- [ ] **ERWARTUNG:** "💪 GIB IHM! - Angriff +10%!" Notification
- [ ] **PRÜFEN:** Tasten 2, 3, 4 auch
- [ ] **Im MANUAL-Modus:** Taste 1 drücken
- [ ] **ERWARTUNG:** Funktioniert auch! (für Slime-Begleiter)

#### Test 3: SPECIAL Stats
- [ ] **Console öffnen:** `F12` → Console
- [ ] **Eingeben:** `window.Real3DCombat.getPlayerStats()`
- [ ] **PRÜFEN:** HP = 100 + (VIT * 15) = 175
- [ ] **PRÜFEN:** Mana = 100 + (INT * 10) = 150
- [ ] **Im Combat:** Mehrmals angreifen
- [ ] **PRÜFEN:** Gelegentlich "MISS" (PER = 5 → 10% Miss-Chance)
- [ ] **PRÜFEN:** Gelegentlich Crits (LUK = 5 → 10% Crit-Chance)

---

### **B. ARENA SYSTEMS**

#### Test 4: Nemesis Arena - Wave Mode
- [ ] **Zur Arena teleportieren**
- [ ] **Console:** `window.Scene3D.changeRoom('Kampfarena')`
- [ ] **ERWARTUNG:** Charakter teleportiert zu [-2000, 0, -2000]
- [ ] **PRÜFEN:** Position ändert sich
- [ ] **Wave Battle starten** (UI-Button oder API)
- [ ] **ERWARTUNG:** Real3DCombat startet
- [ ] **PRÜFEN:** Gegner spawnen in Arena
- [ ] **PRÜFEN:** Combat funktioniert
- [ ] **Nach Victory:** Zurück zum Arena-Panel

#### Test 5: Slime Arena - CHEER Mode
- [ ] **Slime Arena öffnen** (UI-Button)
- [ ] **Battle starten**
- [ ] **ERWARTUNG:** Real3DCombat startet
- [ ] **ERWARTUNG:** Auto-Modus = CHEER
- [ ] **PRÜFEN:** KI kämpft automatisch
- [ ] **PRÜFEN:** Tasten 1-4 für Anfeuern funktionieren
- [ ] **Console:** `window.Real3DCombat.getMode()`
- [ ] **ERWARTUNG:** Returns 'CHEER'

---

### **C. TOUCH CONTROLS (Mobile/Tablet)**

#### Test 6: Touch Combat
- [ ] **Browser DevTools:** F12 → Toggle Device Toolbar
- [ ] **Device:** iPad/iPhone simulieren
- [ ] **Overworld Combat starten**
- [ ] **PRÜFEN:** Virtual Joystick erscheint (links unten)
- [ ] **PRÜFEN:** Attack-Buttons erscheinen (rechts unten)
- [ ] **Touch:** Linker Attack-Button
- [ ] **ERWARTUNG:** Linke Hand greift an (Q)
- [ ] **Touch:** Rechter Attack-Button
- [ ] **ERWARTUNG:** Rechte Hand greift an (E)
- [ ] **Swipe:** Nach hinten wischen
- [ ] **ERWARTUNG:** Dodge (Space)

---

### **D. SCRIPT-LOADING**

#### Test 7: Console Errors
- [ ] **F12 → Console**
- [ ] **Page Refresh:** Strg+F5
- [ ] **PRÜFEN:** Keine 404-Errors für .js Dateien
- [ ] **PRÜFEN:** Keine "Uncaught ReferenceError"
- [ ] **PRÜFEN:** "✅ Real3DCombat ready!" in Console
- [ ] **PRÜFEN:** "✅ EquipmentCombat loaded!" in Console
- [ ] **PRÜFEN:** "✅ Overworld Enemies System ready!" in Console

#### Test 8: System Availability
- [ ] **Console:** `window.Real3DCombat`
- [ ] **ERWARTUNG:** Object mit Funktionen
- [ ] **Console:** `window.EquipmentCombat`
- [ ] **ERWARTUNG:** Object mit WEAPONS
- [ ] **Console:** `window.OverworldEnemies`
- [ ] **ERWARTUNG:** Object
- [ ] **Console:** `window.UnifiedCombat`
- [ ] **ERWARTUNG:** `undefined` (entfernt!)

---

### **E. EDGE CASES**

#### Test 9: Multiple Enemies
- [ ] **3+ Gegner spawnen**
- [ ] **PRÜFEN:** Alle Gegner sichtbar
- [ ] **Angreifen:** Q
- [ ] **ERWARTUNG:** Nearest enemy wird getroffen
- [ ] **Gegner töten**
- [ ] **PRÜFEN:** Loot-Notification
- [ ] **PRÜFEN:** XP-Gain

#### Test 10: Combat-Modus Wechsel während Combat
- [ ] **Im Combat:** M drücken (MANUAL → AUTO)
- [ ] **ERWARTUNG:** KI übernimmt
- [ ] **Wieder M drücken:** AUTO → CHEER
- [ ] **ERWARTUNG:** KI kämpft, Tasten 1-4 funktionieren
- [ ] **Wieder M drücken:** CHEER → MANUAL
- [ ] **ERWARTUNG:** Spieler-Kontrolle zurück

#### Test 11: Arena-Teleport Bug Fix
- [ ] **Overworld Position notieren**
- [ ] **Arena-Wave starten**
- [ ] **PRÜFEN:** Charakter bewegt sich zur Arena
- [ ] **PRÜFEN:** Gegner spawnen in Arena (nicht Overworld)
- [ ] **Nach Combat:**
- [ ] **PRÜFEN:** Zurück zur Arena (nicht Random-Position)

#### Test 12: Enemy Despawn Bug Fix
- [ ] **Overworld:** Gegner spawnen lassen
- [ ] **Langsam auf Gegner zulaufen**
- [ ] **PRÜFEN:** Gegner bleibt sichtbar (verschwindet NICHT!)
- [ ] **Aggro auslösen**
- [ ] **PRÜFEN:** Combat startet
- [ ] **PRÜFEN:** Gegner-Mesh wird versteckt NACH Combat-Load

---

## 🐛 BEKANNTE PROBLEME

### Bereits Gefixt:
- ✅ **Arena-Teleport:** Scene3D.changeRoom teleportiert jetzt korrekt
- ✅ **Gegner verschwinden:** Warten auf combatEnemiesLoaded Event
- ✅ **UnifiedCombat Fallbacks:** Alle entfernt

### Zu Testen:
- ⚠️ **Slime-Begleiter AI:** Kämpft der Slime parallel zum Spieler?
- ⚠️ **CHEER in MANUAL:** Funktioniert parallel kämpfen + anfeuern?
- ⚠️ **Touch-Controls Kompatibilität:** Alle Devices OK?

---

## 📊 CRITICAL PATHS

**Diese Pfade MÜSSEN funktionieren:**

1. **Overworld → Combat → Victory → Loot**
   - Gegner spawnt → Aggro → Real3DCombat → Q/E/Space → Enemy stirbt → Loot + XP

2. **Arena Wave → Multiple Enemies → Victory**
   - Teleport → Wave startet → Real3DCombat → Mehrere Gegner → Alle töten → Wave Victory

3. **Slime Arena → AUTO/CHEER → Victory**
   - Slime Battle → Auto-CHEER → KI kämpft → Anfeuern (1-4) → Victory

4. **Mobile Touch → Combat → Victory**
   - Touch-UI erscheint → Virtual Buttons → Combat → Victory

---

## 🎯 SUCCESS CRITERIA

✅ **Alle Tests bestanden**
✅ **Keine Console-Errors**
✅ **UnifiedCombat komplett entfernt**
✅ **Real3DCombat als einziges System**
✅ **CHEER funktioniert in allen Modi**
✅ **Touch-Controls funktionieren**
✅ **Keine Gegner-Bugs**

---

## 📝 NOTES

**Model-Wechsel Empfehlung:**
- Für einfache Bug-Fixes → **Sonnet** (schneller, günstiger)
- Für komplexe System-Änderungen → **Opus** (aktuell)
- Aktuell: **Opus 4.6** (wegen Combat-System-Umbau)

**User-Feedback:**
- "Waffen-Balance noch nicht 100% stimmig" → Playtesting nötig
- Slime Arena: Nur AUTO/CHEER, kein MANUAL
- Mobile muss funktionieren (wie andere Games)
