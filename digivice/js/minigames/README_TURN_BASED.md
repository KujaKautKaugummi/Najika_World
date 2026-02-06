# Turn-Based Battle System (MINIGAME MODUS)

**Status:** Für später - Minigame/Card Game Battles

## Zweck
Dieses Turn-Based RPG Battle System wurde **bewusst NICHT** für den Hauptkampf verwendet.

**Hauptkampfsystem = Realtime Combat** (Q/E Angriffe, Anfeuern wie Digimon World)

## Mögliche Verwendung später:
- 📇 **Card Game Battles** (Triple Triad style mit Turn-Based)
- 🎲 **Dice Monsters Duels** (Yu-Gi-Oh DDM style)
- 🎮 **Retro Arcade Automat** in der Spielhalle
- 🏆 **Spezial-Turnier Modus**
- 📚 **Story-Flashback Kämpfe**

## Dateien:
- `turn_based_battle_minigame.js` - Komplettes Turn-Based UI (720 Zeilen)
- Backend: `backend/najika_battle.py` - RPG Battle System
- Backend API: `/api/battle/*` Endpoints in `najika_server.py`

## Aktivierung (später):
```javascript
// In index.html einbinden:
<script src="js/minigames/turn_based_battle_minigame.js"></script>

// Dann aufrufen mit:
window.rpgBattleUI.open();
```

## Features:
- ⚔️ Turn-Based Combat (Spieler → Gegner → Spieler)
- 💫 Skill System mit Cooldowns
- 🎒 Item Usage
- 🛡️ Defense/Block Mechanik
- 🏃 Flee Option
- 📊 Wave System (Gegner-Wellen)
- 💰 Rewards (Gold, XP, Loot)
- 📜 Live Battle Log

---
**Erstellt:** 2025-12-04
**Zweck:** Aufbewahrt für spätere Minigame-Integration
