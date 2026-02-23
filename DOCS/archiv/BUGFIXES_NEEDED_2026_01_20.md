# 🐛 BUGFIXES BENÖTIGT - 2026-01-20

**Status:** Analyse komplett, bereit zum Fix
**Quelle:** Browser Console Logs

---

## 🔴 KRITISCHE FEHLER

### 1. LM Studio Chat API Error (400 Bad Request)

**Fehler:**
```
Fehler: 400 Client Error: Bad Request for url: http://localhost:1234/v1/chat/completions
```

**Problem:**
- LM Studio erwartet bestimmtes Request-Format
- Backend sendet falsches Format

**Mögliche Ursachen:**
- Model-Name falsch
- Request-Body fehlt required fields
- API-Version mismatch

**Zu prüfen:**
- `backend/najika_server.py` - LM Studio API call Format
- Ist `dolphin-2.9.2-qwen2-7b` richtig geladen in LM Studio?
- Request body structure

**Fix:**
```python
# backend/najika_server.py
# Prüfen ob Request format korrekt ist:
{
    "model": "dolphin-2.9.2-qwen2-7b",  # Muss EXAKT match
    "messages": [...],
    "temperature": 0.8,
    "max_tokens": 2000
}
```

---

### 2. Tadel API Error (JSON Parse)

**Fehler:**
```
[Najika] Tadel error: SyntaxError: JSON.parse: unexpected character at line 1 column 1
```

**Problem:**
- Backend sendet kein JSON zurück
- Oder HTML Error-Seite

**Zu prüfen:**
- Existiert `/api/tadel` endpoint?
- Sendet Backend JSON zurück?

**Fix:**
- Backend API für Tadel implementieren
- Oder Frontend anpassen (bereits existierenden Endpoint nutzen)

---

## ⚠️ UI FEHLER (Buttons ohne Funktion)

### 3. Card Game UI - `.open()` fehlt

**Fehler:**
```
Uncaught TypeError: window.cardGameUI.open is not a function
```

**Problem:**
- `CardGameUI` Klasse hat keine `.open()` Methode
- Wird aber von Button aufgerufen

**File:** `digivice/js/ui/card_game_ui.js:919`

**Fix:**
```javascript
// In CardGameUI Klasse hinzufügen:
open() {
    this.container.classList.remove('hidden');
}
```

---

### 4. Dice Monsters - `DiceMonsters` nicht definiert

**Fehler:**
```
Uncaught ReferenceError: DiceMonsters is not defined
```

**Problem:**
- Funktion `openDungeonDice()` referenziert `DiceMonsters` global
- Aber nur `DiceMonstersUI` existiert

**File:** `digivice/js/ui/dice_monsters_ui.js:1251`

**Fix:**
```javascript
// VORHER:
function openDungeonDice() {
    DiceMonsters.open();  // ❌ DiceMonsters existiert nicht
}

// NACHHER:
function openDungeonDice() {
    if (window.diceMonstersUI) {
        window.diceMonstersUI.open();  // ✅ Richtige Instanz
    }
}
```

---

### 5. Housing UI - `.open()` fehlt

**Fehler:**
```
Uncaught TypeError: window.housingUI.open is not a function
```

**Problem:**
- `HousingUI` Klasse hat keine `.open()` Methode

**File:** `digivice/js/ui/housing_ui.js`

**Fix:**
```javascript
// In HousingUI Klasse hinzufügen:
open() {
    this.container.classList.remove('hidden');
}
```

---

## 📋 FIX-PRIORITÄTEN

### PRIO 1 - KRITISCH (Chat blockiert):
1. ✅ LM Studio 400 Error fixen
   - Backend Request-Format prüfen
   - Model-Name verifizieren

### PRIO 2 - WICHTIG (UI Features):
2. Card Game UI `.open()` hinzufügen
3. Dice Monsters `.open()` fixen
4. Housing UI `.open()` hinzufügen
5. Tadel API implementieren

---

## 🔍 DETAILLIERTE ANALYSE

### LM Studio API Request Format

**LM Studio erwartet (OpenAI-kompatibel):**
```python
{
    "model": "exakter-model-name",  # MUSS EXAKT MATCH!
    "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
    ],
    "temperature": 0.8,
    "max_tokens": 2000,
    "stream": false  # Optional
}
```

**Häufige Fehler:**
- Model-Name falsch geschrieben
- `messages` Array fehlt
- `role` field fehlt
- Model nicht geladen in LM Studio

---

## ✅ WAS BEREITS FUNKTIONIERT

Laut Console Logs funktioniert:
- ✅ World Loading (alle Assets)
- ✅ Combat System
- ✅ Dungeon System
- ✅ Inventory System
- ✅ Quest System
- ✅ Auto-Save
- ✅ Najika Backend Status API (`/api/najika/status`)
- ✅ Lob API (`/api/lob`)

**Problem:** Nur neue Chat-Requests und UI-Buttons!

---

## 🛠️ FIXES OHNE BLIND ZU SCHIEßEN

### Methode 1: Backend Logging aktivieren

**Erst mal schauen was Backend sendet:**
```python
# backend/najika_server.py
# Bei LM Studio call:
print("🔍 LM Studio Request:", request_data)
print("🔍 LM Studio Response:", response.text)
```

### Methode 2: UI Methoden vorsichtig hinzufügen

**NUR die `.open()` Methoden ergänzen:**
```javascript
// In jeder UI-Klasse die fehlt:
open() {
    if (this.container) {
        this.container.classList.remove('hidden');
    }
}

close() {
    if (this.container) {
        this.container.classList.add('hidden');
    }
}
```

### Methode 3: Browser Cache leeren

**Problem könnte auch Cache sein:**
```
1. STRG + SHIFT + DEL
2. Cache leeren
3. Seite neu laden
```

---

## 📝 NÄCHSTE SCHRITTE

**Reihenfolge:**
1. Browser Cache leeren (schnellster Fix)
2. LM Studio Model-Name prüfen
3. Backend Request-Format debuggen
4. UI `.open()` Methoden hinzufügen
5. Tadel API implementieren (falls gewünscht)

---

**Erstellt:** 2026-01-20
**Status:** Bereit zum vorsichtigen Fix
**WICHTIG:** NICHT blind Code ändern - erst Ursache finden!
