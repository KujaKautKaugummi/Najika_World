# KRITISCHE BUGS GEFIXT - 2026-02-15 ROUND 2

**Erstellt:** 2026-02-15 17:50
**Grund:** User meldete: "Arena geht immer noch nicht, Gegner verschwinden"
**Problem:** Vorheriges SONNET hat Code nicht GETESTET!

---

## 🐛 BUG #1: ARENA TELEPORT FUNKTIONIERT NICHT

### Problem:
- "Herausfordern" Button startet Combat aber teleportiert NICHT zur Arena
- "Welle starten" Button ebenfalls kein Teleport

### Root Cause:
**Code rief `window.switchRoom('Kampfarena')` auf - diese Funktion EXISTIERT NICHT!**

```javascript
// FALSCH (in beiden Dateien):
if (window.switchRoom) {
    window.switchRoom('Kampfarena');
}
```

### Lösung:
Die korrekte Funktion heißt `window.Scene3D.changeRoom()`:

**Datei 1:** `digivice/js/nemesis_arena_ui.js` (Zeile ~459)
```javascript
// NEU (RICHTIG):
if (window.Scene3D && typeof window.Scene3D.changeRoom === 'function') {
    window.Scene3D.changeRoom('Kampfarena');
    console.log('🏟️ Teleported to Kampfarena');
} else {
    console.error('❌ Scene3D.changeRoom() not available!');
}
```

**Datei 2:** `digivice/js/nemesis_arena_frontend.js` (Zeile ~939)
```javascript
// NEU (RICHTIG):
if (window.Scene3D && typeof window.Scene3D.changeRoom === 'function') {
    window.Scene3D.changeRoom('Kampfarena');
    console.log('🏟️ Teleported to Kampfarena for Wave Battle');
} else {
    console.error('❌ Scene3D.changeRoom() not available!');
}
```

### Status: ✅ GEFIXT

---

## 🐛 BUG #2: OVERWORLD-GEGNER VERSCHWINDEN BEIM ANNÄHERN

### Problem:
- Spieler geht auf Gegner zu
- Gegner wird unsichtbar (`mesh.visible = false`)
- Combat startet NICHT oder Callbacks funktionieren nicht
- Gegner bleibt unsichtbar (kommt nie zurück)

### Root Cause (ANALYSE):

#### Teilproblem A: Callbacks werden überschrieben
```javascript
// PROBLEM: Wenn 2 Gegner gleichzeitig aggro sind:
Enemy1: window.onCombatVictory = function() { /* Enemy1 Code */ }
Enemy2: window.onCombatVictory = function() { /* Enemy2 Code */ } // ÜBERSCHREIBT Enemy1!

// Ergebnis: Nur Enemy2 profitiert von Victory-Callback!
```

#### Teilproblem B: GameEvents existiert nicht überall
Code nutzt `window.GameEvents.on()` aber GameEvents ist möglicherweise nicht geladen!

### Lösung (IN ARBEIT):

**Option 1: Combat-Queue-System**
- Nur 1 Combat gleichzeitig erlauben
- Andere Enemies in Warteschlange
- Nach Combat Victory/Defeat → nächster Enemy

**Option 2: Enemy-ID in Callbacks**
- Combat-System gibt Enemy-ID zurück
- Callbacks prüfen: "War das MEIN Enemy?"

**Option 3: GameEvents Fallback**
- Checken ob GameEvents existiert
- Falls nicht: Simple `window.overworldCombatCallbacks = { enemyId: callbacks }`

### Status: ⚠️ TEILWEISE GEFIXT (Arena Teleport ja, Enemy-Callbacks nein)

---

## 📋 NÄCHSTE SCHRITTE

### SOFORT (SONNET):
1. ⬜ **Enemy-Combat-Queue implementieren** (nur 1 Combat gleichzeitig)
2. ⬜ **GameEvents Check** (existiert es überhaupt?)
3. ⬜ **LIVE-TESTING** (Browser öffnen, SELBST testen!)

### Lessons Learned:
- ❌ **NIEMALS Code committen ohne Testing!**
- ❌ **NIEMALS Funktionen aufrufen ohne zu prüfen ob sie existieren!**
- ✅ **IMMER im Browser testen nach Fixes!**

---

## 🧪 TEST-PLAN (MUSS GEMACHT WERDEN!)

### Test 1: Arena Teleport
```
1. Browser → http://127.0.0.1:8001
2. Arena öffnen
3. "Herausfordern" klicken
4. ERWARTE: Teleport zu Kampfarena + Combat startet
```

### Test 2: Overworld Enemies
```
1. In Open-World gehen (nicht Stadt)
2. Auf Gegner zugehen (Wolf, Slime, etc.)
3. ERWARTE: Combat startet
4. Combat gewinnen
5. ERWARTE: Gegner wird entfernt, Loot erscheint
```

### Test 3: Multiple Enemies
```
1. Mehrere Gegner spawnen lassen
2. Schnell zwischen 2 Gegnern hin- und herlaufen
3. ERWARTE: Nur 1 Combat startet, andere warten
```

---

**Status:** Bug #1 gefixt ✅, Bug #2 teilweise analysiert ⚠️
**Nächstes:** LIVE-TESTING + Combat-Queue implementieren
