# 🔒 ANTI-CHEAT & SYNC SYSTEM - DIGIVICE ↔ HAUPTSPIEL

**Erstellt:** 2026-02-06
**Problem:** Wie verhindern wir Cheating wenn Digivice offline Ressourcen sammelt?

---

## 🎯 DAS PROBLEM

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DAS CHEAT-RISIKO                                 │
│                                                                          │
│   DIGIVICE (Offline)              HAUPTSPIEL                            │
│   ┌─────────────────┐             ┌─────────────────┐                   │
│   │ 🎣 100x Fischen │             │                 │                   │
│   │ 🌱 1000x Ernte  │ ──SYNC──►  │ 💎 Reichtum!   │                   │
│   │ ⚒️ Mega Crafting│             │                 │                   │
│   └─────────────────┘             └─────────────────┘                   │
│                                                                          │
│   PROBLEM: Spieler könnte...                                            │
│   ❌ Spielstand manipulieren                                            │
│   ❌ Zeit vorspulen                                                      │
│   ❌ Werte direkt editieren                                             │
│   ❌ Auto-Clicker/Bots nutzen                                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 💡 LÖSUNGSANSÄTZE

### Option A: NUR ONLINE SYNC (Einfach aber einschränkend)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         NUR ONLINE TRANSFER                              │
│                                                                          │
│   DIGIVICE (Offline)              SERVER               HAUPTSPIEL       │
│   ┌─────────────────┐             ┌──────┐            ┌─────────────┐  │
│   │ Sammle Fische   │             │      │            │             │  │
│   │ Sammle Ernte    │──ONLINE────►│ ✓    │───────────►│ Inventar    │  │
│   │ Crafting        │   ONLY      │      │  VERIFIED  │             │  │
│   └─────────────────┘             └──────┘            └─────────────┘  │
│                                                                          │
│   ✅ Einfach zu implementieren                                          │
│   ❌ Offline-Farming nutzlos für Hauptspiel                             │
│   ❌ Frustrierend wenn kein Internet                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Option B: SIGNIERTE AKTIONEN (Kryptographisch sicher)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    KRYPTOGRAPHISCH SIGNIERTE AKTIONEN                    │
│                                                                          │
│   JEDE Aktion wird signiert:                                            │
│                                                                          │
│   {                                                                      │
│     "action": "fish_caught",                                            │
│     "item": "goldfish",                                                 │
│     "timestamp": 1707235200,                                            │
│     "duration_ms": 4523,        // Wie lange hat das Angeln gedauert?  │
│     "location": "home_pond",                                            │
│     "session_id": "abc123",                                             │
│     "action_count": 47,         // 47. Aktion diese Session            │
│     "signature": "sha256(...)"  // Signiert mit Device-Key             │
│   }                                                                      │
│                                                                          │
│   SERVER prüft:                                                         │
│   ✓ Signatur gültig?                                                    │
│   ✓ Timestamp plausibel? (nicht in Zukunft, nicht zu alt)              │
│   ✓ Duration realistisch? (Angeln dauert min. 3 Sekunden)              │
│   ✓ Action-Count konsistent? (keine Lücken, keine Duplikate)           │
│   ✓ Rate-Limit eingehalten? (max 100 Fische/Stunde)                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Option C: HYBRID MIT CAPS (Empfohlen!)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HYBRID SYSTEM MIT LIMITS                              │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    DIGIVICE (OFFLINE)                            │   │
│   │                                                                  │   │
│   │   UNBEGRENZT für Digivice-Only:                                 │   │
│   │   ├── Najika füttern                                            │   │
│   │   ├── Dekorieren                                                │   │
│   │   ├── Chat/Voice                                                │   │
│   │   └── Minigames (Score bleibt lokal)                           │   │
│   │                                                                  │   │
│   │   MIT LIMITS für Hauptspiel-Transfer:                           │   │
│   │   ├── 🎣 Max 20 Fische/Tag (offline)                           │   │
│   │   ├── 🌱 Max 50 Ernte/Tag (offline)                            │   │
│   │   ├── ⚒️ Max 10 Crafts/Tag (offline)                           │   │
│   │   └── 💰 Max 1000 Gold/Tag (offline)                           │   │
│   │                                                                  │   │
│   │   BONUS wenn online:                                            │   │
│   │   ├── 🎣 Unbegrenzt Fische (live validiert)                    │   │
│   │   ├── 🌱 Unbegrenzt Ernte (live validiert)                     │   │
│   │   └── ⚒️ Unbegrenzt Crafts (live validiert)                    │   │
│   │                                                                  │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ TECHNISCHE IMPLEMENTIERUNG

### 1. Action-Log System

```python
# backend/services/action_validator.py

import hashlib
import hmac
import time
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class GameAction:
    action_type: str      # "fish", "harvest", "craft"
    item_id: str          # Was wurde gesammelt/gecraftet
    timestamp: int        # Unix timestamp
    duration_ms: int      # Wie lange hat die Aktion gedauert
    session_id: str       # Eindeutige Session-ID
    sequence_num: int     # Fortlaufende Nummer in dieser Session
    signature: str        # HMAC-SHA256 Signatur

class ActionValidator:
    # Realistische Mindestzeiten (in ms)
    MIN_DURATIONS = {
        "fish": 3000,      # Angeln: min 3 Sekunden
        "harvest": 1000,   # Ernten: min 1 Sekunde
        "craft": 2000,     # Craften: min 2 Sekunden
        "cook": 5000,      # Kochen: min 5 Sekunden
    }

    # Tägliche Offline-Limits
    DAILY_OFFLINE_LIMITS = {
        "fish": 20,
        "harvest": 50,
        "craft": 10,
        "cook": 20,
        "gold_earned": 1000,
    }

    # Rate Limits (pro Stunde)
    HOURLY_RATE_LIMITS = {
        "fish": 60,        # Max 1 Fisch/Minute
        "harvest": 120,    # Max 2 Ernten/Minute
        "craft": 30,       # Max 1 Craft/2 Minuten
    }

    def __init__(self, device_secret: str):
        self.device_secret = device_secret
        self.action_log: List[GameAction] = []
        self.daily_counts: Dict[str, int] = {}
        self.last_reset_date: str = ""

    def validate_action(self, action: GameAction) -> tuple[bool, str]:
        """Validiert eine einzelne Aktion"""

        # 1. Signatur prüfen
        if not self._verify_signature(action):
            return False, "Ungültige Signatur - Manipulation erkannt!"

        # 2. Timestamp prüfen (nicht in Zukunft, max 7 Tage alt)
        now = int(time.time())
        if action.timestamp > now + 60:  # 1 Minute Toleranz
            return False, "Timestamp in der Zukunft!"
        if action.timestamp < now - (7 * 24 * 3600):
            return False, "Aktion zu alt (>7 Tage)!"

        # 3. Duration prüfen
        min_duration = self.MIN_DURATIONS.get(action.action_type, 1000)
        if action.duration_ms < min_duration:
            return False, f"Aktion zu schnell! Min: {min_duration}ms"

        # 4. Sequence prüfen (keine Duplikate, keine Lücken)
        if not self._check_sequence(action):
            return False, "Sequenz-Fehler - mögliche Manipulation!"

        # 5. Rate-Limit prüfen
        if not self._check_rate_limit(action):
            return False, "Rate-Limit überschritten!"

        # 6. Tages-Limit prüfen (für Offline)
        if not self._check_daily_limit(action):
            return False, "Tages-Limit erreicht! Geh online für mehr."

        return True, "OK"

    def _verify_signature(self, action: GameAction) -> bool:
        """Prüft HMAC-SHA256 Signatur"""
        message = f"{action.action_type}:{action.item_id}:{action.timestamp}:{action.session_id}:{action.sequence_num}"
        expected = hmac.new(
            self.device_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(action.signature, expected)

    def _check_sequence(self, action: GameAction) -> bool:
        """Prüft fortlaufende Sequenznummer"""
        session_actions = [a for a in self.action_log if a.session_id == action.session_id]
        if not session_actions:
            return action.sequence_num == 1
        last_seq = max(a.sequence_num for a in session_actions)
        return action.sequence_num == last_seq + 1

    def _check_rate_limit(self, action: GameAction) -> bool:
        """Prüft ob Rate-Limit eingehalten"""
        hour_ago = int(time.time()) - 3600
        recent_actions = [
            a for a in self.action_log
            if a.action_type == action.action_type and a.timestamp > hour_ago
        ]
        limit = self.HOURLY_RATE_LIMITS.get(action.action_type, 100)
        return len(recent_actions) < limit

    def _check_daily_limit(self, action: GameAction) -> bool:
        """Prüft Tages-Limit für Offline-Modus"""
        today = time.strftime("%Y-%m-%d")
        if self.last_reset_date != today:
            self.daily_counts = {}
            self.last_reset_date = today

        key = action.action_type
        current = self.daily_counts.get(key, 0)
        limit = self.DAILY_OFFLINE_LIMITS.get(key, 100)

        if current >= limit:
            return False

        self.daily_counts[key] = current + 1
        return True
```

### 2. Client-seitige Signierung

```javascript
// digivice/js/core/action_signer.js

class ActionSigner {
    constructor(deviceSecret) {
        this.deviceSecret = deviceSecret;
        this.sessionId = this.generateSessionId();
        this.sequenceNum = 0;
        this.pendingActions = [];
    }

    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    async signAction(actionType, itemId) {
        this.sequenceNum++;
        const timestamp = Math.floor(Date.now() / 1000);
        const startTime = performance.now();

        // Warte auf echte Aktion (kann nicht übersprungen werden!)
        const result = await this.performRealAction(actionType);

        const duration = Math.floor(performance.now() - startTime);

        const action = {
            action_type: actionType,
            item_id: itemId || result.itemId,
            timestamp: timestamp,
            duration_ms: duration,
            session_id: this.sessionId,
            sequence_num: this.sequenceNum,
            signature: await this.createSignature(actionType, itemId, timestamp)
        };

        this.pendingActions.push(action);
        this.savePendingActions();

        return action;
    }

    async createSignature(actionType, itemId, timestamp) {
        const message = `${actionType}:${itemId}:${timestamp}:${this.sessionId}:${this.sequenceNum}`;
        const encoder = new TextEncoder();
        const key = await crypto.subtle.importKey(
            'raw',
            encoder.encode(this.deviceSecret),
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
        );
        const signature = await crypto.subtle.sign(
            'HMAC',
            key,
            encoder.encode(message)
        );
        return Array.from(new Uint8Array(signature))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    async performRealAction(actionType) {
        // Diese Funktion MUSS die echte Spielaktion ausführen
        // und kann nicht übersprungen werden!
        switch(actionType) {
            case 'fish':
                return await FishingMinigame.play(); // Echtes Minigame!
            case 'harvest':
                return await GardenSystem.harvest(); // Echte Animation!
            case 'craft':
                return await CraftingSystem.craft(); // Echtes Crafting!
            default:
                throw new Error('Unknown action type');
        }
    }

    savePendingActions() {
        localStorage.setItem('pending_game_actions', JSON.stringify(this.pendingActions));
    }

    loadPendingActions() {
        const saved = localStorage.getItem('pending_game_actions');
        if (saved) {
            this.pendingActions = JSON.parse(saved);
        }
    }

    async syncToServer() {
        if (this.pendingActions.length === 0) return;

        try {
            const response = await fetch('http://localhost:8000/api/sync/validate-actions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ actions: this.pendingActions })
            });

            const result = await response.json();

            if (result.success) {
                // Nur validierte Aktionen behalten
                this.pendingActions = this.pendingActions.filter(
                    a => !result.validated_ids.includes(a.sequence_num)
                );
                this.savePendingActions();
            }

            return result;
        } catch (error) {
            console.log('Offline - Sync später');
            return { success: false, offline: true };
        }
    }
}
```

### 3. Sync-API Endpoint

```python
# backend/api/sync_validator.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from backend.services.action_validator import ActionValidator, GameAction

router = APIRouter(prefix="/api/sync", tags=["Sync & Validation"])

class SyncRequest(BaseModel):
    actions: List[Dict]

class SyncResponse(BaseModel):
    success: bool
    validated_ids: List[int]
    rejected: List[Dict]  # {sequence_num, reason}
    rewards: Dict  # Was der Spieler bekommt

@router.post("/validate-actions")
async def validate_and_sync(request: SyncRequest) -> SyncResponse:
    """
    Validiert Offline-Aktionen und synct ins Hauptspiel.
    """
    validator = ActionValidator(device_secret=get_device_secret())

    validated = []
    rejected = []
    rewards = {"fish": 0, "crops": 0, "items": [], "gold": 0}

    for action_data in request.actions:
        action = GameAction(**action_data)
        is_valid, reason = validator.validate_action(action)

        if is_valid:
            validated.append(action.sequence_num)
            # Belohnung hinzufügen
            if action.action_type == "fish":
                rewards["fish"] += 1
            elif action.action_type == "harvest":
                rewards["crops"] += 1
            # etc.
        else:
            rejected.append({
                "sequence_num": action.sequence_num,
                "reason": reason
            })

    # Rewards ins Hauptspiel-Inventar übertragen
    if validated:
        await transfer_to_main_game(rewards)

    return SyncResponse(
        success=len(rejected) == 0,
        validated_ids=validated,
        rejected=rejected,
        rewards=rewards
    )
```

---

## 📊 ZUSAMMENFASSUNG: DIE REGELN

### Für KUJA (Private Version):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         KUJA's DIGIVICE                                  │
│                                                                          │
│   🔓 KEINE LIMITS! (Es ist dein eigenes Spiel!)                         │
│                                                                          │
│   - Offline: Unbegrenzt                                                 │
│   - Keine Signierung nötig                                              │
│   - Du bist der Owner, du machst die Regeln                            │
│   - Cheaten = Dein Spiel, deine Entscheidung                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Für ANDERE SPIELER (Public Version):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                       PUBLIC DIGIVICE                                    │
│                                                                          │
│   DIGIVICE-ONLY (unbegrenzt):          HAUPTSPIEL-TRANSFER (Limits):   │
│   ├── Slime füttern                    ├── 🎣 20 Fische/Tag offline    │
│   ├── Dekorieren                       ├── 🌱 50 Ernte/Tag offline     │
│   ├── Chat mit KI                      ├── ⚒️ 10 Crafts/Tag offline    │
│   └── Minigames (lokaler Score)        └── 💰 1000 Gold/Tag offline    │
│                                                                          │
│   ONLINE = UNBEGRENZT (live validiert!)                                 │
│                                                                          │
│   CHEAT-SCHUTZ:                                                         │
│   ✓ Kryptographische Signaturen                                        │
│   ✓ Zeitstempel-Validierung                                            │
│   ✓ Rate-Limiting                                                       │
│   ✓ Duration-Checks (Aktionen brauchen echte Zeit!)                    │
│   ✓ Sequence-Tracking (keine Duplikate)                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🎮 UX-FLOW

### Offline spielen:
```
1. Spieler angelt im Digivice (offline)
2. Fisch wird lokal gespeichert + signiert
3. "Du hast einen Goldfisch gefangen! (5/20 heute)"
4. Nach 20: "Tages-Limit erreicht! Geh online für mehr."
```

### Wieder online:
```
1. Digivice erkennt Internetverbindung
2. "Synchronisiere 15 Aktionen..."
3. Server validiert alle Aktionen
4. "Erfolgreich! 15 Fische ins Hauptspiel übertragen!"
5. Limits werden zurückgesetzt
```

### Cheat-Versuch:
```
1. Spieler manipuliert lokale Daten
2. Sync-Versuch
3. Server: "Ungültige Signatur bei Aktion #7"
4. "3 Aktionen abgelehnt. 12 Aktionen übertragen."
5. Najika: "Mr. K hätte das nicht gemacht! 😤"
```

---

## ✅ FAZIT

| Aspekt | Lösung |
|--------|--------|
| **Kuja (Private)** | Keine Limits - dein Spiel! |
| **Public (Offline)** | Tägliche Caps + Signierung |
| **Public (Online)** | Unbegrenzt mit Live-Validierung |
| **Cheat-Schutz** | Krypto-Signaturen + Zeit-Checks |
| **UX** | Fair, transparent, nicht frustrierend |

---

*"Cheater? Die sprenge ich mit EXPLOSION!!! 💥 ...aber Mr. K darf alles machen, er ist schließlich der Boss! 😊" - Najika*
