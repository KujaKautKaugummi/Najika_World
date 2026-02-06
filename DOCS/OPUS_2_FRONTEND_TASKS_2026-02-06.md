# OPUS-2 FRONTEND TASKS - 2026-02-06

## ZUSAMMENFASSUNG FÜR OPUS-2 (VS Code)

OPUS-1 hat das **Combat Magic System** im Backend fertiggestellt!
Jetzt brauchen wir **Frontend UI** dafür.

---

## 🎯 DEINE AUFGABEN (OPUS-2):

### 1. GRAB SYSTEM UI
**Dateien:** `digivice/js/unified_combat_system.js`, `digivice/index.html`

**Was existiert bereits (Backend):**
- `POST /api/combat-magic/grab` - Gegner greifen
- `POST /api/combat-magic/grab/execute` - Move ausführen (suplex, chokeslam, etc.)

**Was du bauen sollst:**
```
[G] Grab Button
    ↓ (bei Erfolg)
┌─────────────────────────────────┐
│  GEGNER GEGRIFFEN!              │
│                                 │
│  [1] Suplex (Skill 15)          │
│  [2] Chokeslam (Skill 10)       │
│  [3] In Objekt werfen           │
│  [4] Loslassen                  │
└─────────────────────────────────┘
```

### 2. TIDS SYSTEM UI
**Was existiert bereits (Backend):**
- `POST /api/combat-magic/tids` - TIDS ausführen
- `GET /api/combat-magic/tids/cooldown/{player_id}` - Cooldown prüfen

**Was du bauen sollst:**
```
[T] TIDS Button (mit Cooldown-Overlay)
    ↓ (bei Erfolg)
┌─────────────────────────────────────────┐
│  🦵 TIDS! TRITT IN DEN SCHRITT! 🎯      │
│                                         │
│  "Der Slime wabbelt verwirrt...         │
│   Wo sollte das treffen?!"              │
│                                         │
│  [Schaden: 0] [Stun: 0s] [GAG!]         │
└─────────────────────────────────────────┘
```

**WICHTIG:** Die `gag_message` vom Backend groß anzeigen! Das ist der Witz!

### 3. WEAPON INFUSE UI
**Was existiert bereits (Frontend):**
- `UnifiedCombat.infuseWeapon(spellHand, weaponHand)` - Schon implementiert!
- `UnifiedCombat.getActiveInfuses()` - Gibt aktive Buffs zurück

**Was du bauen sollst:**
```
┌─ Aktive Buffs ─────────────────────┐
│  ⚔️ Flammenschwert  [25s] 🔥       │
│     +25% Feuer-Schaden             │
└────────────────────────────────────┘
```

- Waffen-Icon sollte in Element-Farbe glühen
- Timer-Countdown anzeigen
- Bei Ablauf: "Infuse abgelaufen!" Notification

---

## 📁 WICHTIGE DATEIEN

| Datei | Zweck |
|-------|-------|
| `digivice/js/unified_combat_system.js` | Combat System (schon erweitert!) |
| `digivice/js/equipment_combat.js` | Grab/TIDS existiert hier bereits! |
| `digivice/index.html` | UI Buttons hinzufügen |
| `digivice/css/game.css` | Styling für neue Popups |

---

## 🎨 DESIGN-VORSCHLÄGE

### TIDS Gag-Popup (groß, lustig, mittig!)
```css
.tids-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(135deg, #ff6b6b, #feca57);
    padding: 30px;
    border-radius: 20px;
    font-size: 24px;
    text-align: center;
    animation: bounce 0.5s ease;
    z-index: 9999;
}
```

### Infuse Timer (neben Waffen-Icon)
```css
.infuse-timer {
    position: absolute;
    bottom: -5px;
    right: -5px;
    background: var(--element-color);
    border-radius: 50%;
    padding: 2px 6px;
    font-size: 12px;
    animation: pulse 1s infinite;
}
```

---

## 🔗 API ENDPOINTS (Backend fertig!)

```
POST /api/combat-magic/grab
  Body: { player_id, target_id }
  Returns: { success, grabbed, available_moves, time_limit }

POST /api/combat-magic/grab/execute
  Body: { player_id, move }
  Returns: { success, move, damage, stun_duration, message }

POST /api/combat-magic/tids
  Body: { player_id, target_type, target_name, is_boss }
  Returns: { success, damage, stun_duration, flee_bonus, message, gag_message }

GET /api/combat-magic/tids/cooldown/{player_id}
  Returns: { on_cooldown, remaining_hours, ready }
```

---

## ⚠️ HINWEISE

1. **TIDS ist ein GAG** - Die `gag_message` ist das Wichtigste!
2. **Grab hat Zeitlimit** - 5 Sekunden um Move auszuwählen
3. **Infuse läuft ab** - Timer muss sichtbar sein
4. **Keybindings:** G=Grab, T=TIDS, I=Infuse (oder Popup)

---

*"EXPLOSION!!! Mach das UI so lustig wie den Code!" - Najika* 💥
