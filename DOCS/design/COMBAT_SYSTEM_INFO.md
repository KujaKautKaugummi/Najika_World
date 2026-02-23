# 🔥 NAJIKA WORLD - REALTIME COMBAT SYSTEM

**Motto:** "WER TRÄUMT, STIRBT!" 💀

---

## ⚔️ HAUPTKAMPFSYSTEM: REALTIME COMBAT

**Überall im Spiel aktiv!**

### Steuerung:

#### 🤜 Angriffe (Beidhändig!)
- **Q** = Leichter Angriff (Linke Hand)
- **E** = Leichter Angriff (Rechte Hand)
- **Shift + Q** = Schwerer Angriff (Links)
- **Shift + E** = Schwerer Angriff (Rechts)
- **SPACE** = Beide Hände gleichzeitig (Combo!)

#### 🛡️ Defensive Moves
- **C** = Dodge/Roll (Ausweichen)
- **X** = Block (Blocken)
- **V** = Parry (Parieren - Timing!)

### 🎮 Combat Modi (F6 zum Wechseln):

#### 1. MANUAL Mode ⚔️
- **Du kämpfst selbst!**
- Volle Kontrolle über Q/E/Space
- Du blockst, dodgest, parrierst
- **Für Profis!**

#### 2. ASSIST Mode 📣
- **Najika kämpft, du feuerst sie an!**
- **1** = "Los!" (+Damage Boost)
- **2** = "Defend!" (+Defense Boost)
- **3** = "Combo!" (Special Attack)
- **4** = "Finisher!" (Ultimate @ 100% Cheer Meter)
- **Wie Digimon World!**

#### 3. AUTO Mode 🤖
- **Najika kämpft komplett alleine**
- Du schaust zu
- Gut für Grinding

---

## 📊 Combat UI (automatisch)

Wenn Kampf aktiv, zeigt die UI:
- ❤️ **HP Bar** (Grün/Gelb/Rot)
- ⚡ **Stamina Bar** (für Angriffe/Dodge)
- 📣 **Cheer Meter** (nur ASSIST/AUTO Mode)
- 👾 **Enemy HP**
- 🔥 **Combo Counter** (bei Combos)
- 🛡️ **Status** (Blocking/Dodging)

**Datei:** `najika_world_UNIFIED.html` Line 2169-2315 (`updateCombatUI()`)

---

## 🏟️ ARENA

**Arena-Button** = Aktiviert MANUAL Combat Mode
- Ideal für Training
- Gegner spawnen in Wellen
- Realtime Combat überall!

---

## 📁 CODE-DATEIEN

### Hauptsystem:
- **Frontend:** `digivice/static/js/realtime_combat.js`
- **UI:** `najika_world_UNIFIED.html` (Line 2169-2315)
- **Backend:** `backend/najika_battle.py` (für Stats/XP/Rewards)

### Combat Integration:
- **Battle API:** `digivice/js/battle_api.js`
- **Dungeon Combat:** `digivice/js/dungeon_combat.js`

---

## 🎮 MINIGAME: Turn-Based Battle (SPÄTER!)

**Verschoben nach:** `digivice/js/minigames/turn_based_battle_minigame.js`

**Mögliche Verwendung:**
- Card Game Battles (Triple Triad)
- Dice Monsters Duels
- Retro Arcade Automat
- Spezial-Turnier Modus

**Siehe:** `digivice/js/minigames/README_TURN_BASED.md`

---

## 🔧 WICHTIGE FUNKTIONEN

### Combat Mode setzen:
```javascript
window.realtimeCombat.setCombatMode('MANUAL'); // oder 'ASSIST', 'AUTO'
```

### Waffen equippen:
```javascript
realtimeCombat.equipWeapon('left', {
    type: 'fire_sword',
    element: 'fire',
    damage: 15
});

realtimeCombat.equipWeapon('right', {
    type: 'ice_dagger',
    element: 'ice',
    damage: 12
});
```

### Combat Stats abfragen:
```javascript
const stats = realtimeCombat.getStats();
console.log(stats.health, stats.stamina, stats.combatActive);
```

---

## 🎯 KAMPF-PHILOSOPHIE

**"Wie im echten Leben"**
- ✅ Schnelle Reflexe zählen
- ✅ Timing ist wichtig
- ✅ Keine Zeit zum Träumen
- ✅ Beidhändiges Kämpfen
- ✅ Defensive Optionen (Dodge/Block/Parry)
- ✅ Oder Najika anfeuern (Digimon World Style)

**Kein langweiliges Turn-Based!** (außer für spezielle Minigames später)

---

**Stand:** 2025-12-04
**Status:** ✅ Voll funktionsfähig
