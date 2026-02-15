# MULTIPLAYER WORLD REGENERATION - FINAL DESIGN 2026-02-15

**Entscheidung:** Hybrid-System mit Smart-Trigger + Fallback

---

## 🎯 FINALE REGEL (VON KUJA BESTÄTIGT)

### PRIORITÄT 1: OPPORTUNISTISCHE REGENERATION
```
WENN alle Spieler in Städten/Besonderen Orten sind
→ Sofort regenerieren (kein Warten nötig!)
```

### PRIORITÄT 2: ERZWUNGENE REGENERATION
```
WENN nicht alle Spieler in Städten sind nach X Zeit
→ Zwangs-Teleport + dann regenerieren
```

---

## 📋 DETAILLIERTES SYSTEM

### TRIGGER-LOGIK:

```python
class WorldRegenerationSystem:
    def __init__(self):
        self.last_regeneration = datetime.now()
        self.regeneration_interval = timedelta(hours=6)  # Oder 12h, 24h
        self.next_forced_regen = self.last_regeneration + self.regeneration_interval

    def update(self):
        """Läuft jede Minute"""

        # CHECK 1: Sind alle Spieler in Städten?
        if self.all_players_in_safe_zones():
            print("✅ Alle Spieler in Städten → Sofort regenerieren!")
            self.regenerate_world()
            return

        # CHECK 2: Ist es Zeit für erzwungene Regeneration?
        if datetime.now() >= self.next_forced_regen:
            print("⏰ Zeit für erzwungene Regeneration!")
            self.force_regeneration()
            return

    def all_players_in_safe_zones(self) -> bool:
        """Prüft ob ALLE Online-Spieler in sicheren Zonen sind"""
        online_players = get_all_online_players()

        for player in online_players:
            if not self.is_in_safe_zone(player):
                return False  # Mindestens 1 Spieler draußen!

        return True  # Alle in sicheren Zonen!

    def is_in_safe_zone(self, player) -> bool:
        """Definiert sichere Zonen"""
        safe_zones = [
            'Schwarze Mühle',
            'Argentum',
            'Kristallstadt',
            'Wüstenstadt',
            'Eisstadt',
            'Kampfarena',           # Arena ist sicher!
            'Götterfels',           # Special Location
            'Spieler-Lebensraum'    # Player Housing
        ]

        # Check: Ist Spieler in einer dieser Zonen?
        return player.current_location in safe_zones

    def force_regeneration(self):
        """Erzwungene Regeneration mit Zwangs-Teleport"""
        # 1. WARNUNG (10 Minuten vorher)
        self.send_global_warning(10)
        time.sleep(300)  # 5min warten

        # 2. WARNUNG (5 Minuten vorher)
        self.send_global_warning(5)
        time.sleep(240)  # 4min warten

        # 3. LETZTE WARNUNG (1 Minute)
        self.send_global_warning(1)
        time.sleep(60)  # 1min warten

        # 4. ZWANGS-TELEPORT
        self.teleport_all_to_cities()

        # 5. REGENERIEREN
        self.regenerate_world()

    def teleport_all_to_cities(self):
        """Teleportiert ALLE Spieler zur nächsten Stadt"""
        online_players = get_all_online_players()

        for player in online_players:
            if self.is_in_safe_zone(player):
                continue  # Schon sicher

            # Finde nächste Stadt
            nearest_city = self.find_nearest_city(player.position)

            # Teleport!
            self.teleport_player(player.id, nearest_city)

            # Notification
            self.send_notification(player.id,
                f"🏠 Du wurdest nach {nearest_city} teleportiert (Welt-Regeneration)")

    def regenerate_world(self):
        """Regeneriert die komplette Open-World"""
        print("🌍 REGENERATING WORLD...")

        # 1. Alle Overworld-Entities löschen
        self.clear_overworld_enemies()
        self.clear_overworld_resources()

        # 2. Neue Welt generieren (prozedural)
        world_generator.regenerate_all_regions()

        # 3. Neue Enemies spawnen
        enemy_spawner.respawn_all()

        # 4. Neue Resources spawnen
        resource_spawner.respawn_all()

        # 5. Timestamps updaten
        self.last_regeneration = datetime.now()
        self.next_forced_regen = self.last_regeneration + self.regeneration_interval

        # 6. Global Notification
        self.send_global_notification("🌍 Die Welt wurde regeneriert! Neue Abenteuer erwarten euch!")

        print(f"✅ Welt regeneriert! Nächste Regeneration: {self.next_forced_regen}")
```

---

## 🎮 BEISPIEL-SZENARIEN

### SZENARIO 1: Friedliche Regeneration ✅
```
Zeit: 10:00 Uhr
Spieler: 5 Online
  - Spieler A: Schwarze Mühle (Stadt)
  - Spieler B: Argentum (Stadt)
  - Spieler C: Kampfarena
  - Spieler D: Lebensraum (Housing)
  - Spieler E: Kristallstadt (Stadt)

→ ALLE in sicheren Zonen!
→ System: "✅ Alle Spieler sicher → Regeneriere JETZT!"
→ Welt regeneriert um 10:00 (ohne Warnung, da alle sicher)
```

### SZENARIO 2: Erzwungene Regeneration ⚠️
```
Zeit: 14:50 Uhr (10min vor Deadline 15:00)
Spieler: 3 Online
  - Spieler A: Argentum (Stadt) ✅
  - Spieler B: Flüsterwald (Overworld) ❌
  - Spieler C: Sumpf (Overworld) ❌

→ NICHT alle in sicheren Zonen!
→ System: "⚠️ WARNUNG: Welt regeneriert in 10 Minuten!"

Zeit: 14:55 Uhr (5min vor Deadline)
  - Spieler A: Argentum (Stadt) ✅
  - Spieler B: IMMER NOCH im Wald! ❌
  - Spieler C: Hat sich nach Wüstenstadt teleportiert ✅

→ System: "⚠️ LETZTE WARNUNG: 5 Minuten! Auto-Teleport!"

Zeit: 14:59 Uhr (1min vor Deadline)
  - Spieler B: IMMER NOCH im Wald (AFK?) ❌

→ System: "⚠️ 1 MINUTE! ACHTUNG!"

Zeit: 15:00 Uhr (Deadline erreicht)
→ System teleportiert Spieler B automatisch nach Schwarze Mühle
→ Welt wird regeneriert
→ Alle Spieler erhalten Notification: "🌍 Welt regeneriert!"
```

### SZENARIO 3: Spieler kehrt rechtzeitig zurück ✅
```
Zeit: 14:50 Uhr (10min vor Deadline)
Spieler A: Vulkan (Overworld)

→ Warnung: "⚠️ Welt regeneriert in 10 Minuten! Kehre zurück!"
→ Spieler A läuft zur nächsten Stadt (8 Minuten Laufweg)

Zeit: 14:58 Uhr
→ Spieler A erreicht Argentum
→ Alle Spieler sind jetzt in Städten!
→ System: "✅ Alle Spieler sicher → Regeneriere JETZT!"
→ Welt regeneriert um 14:58 (2min VOR Deadline)
```

---

## ⏰ REGENERATIONS-ZEITPLAN (VORSCHLAG)

### OPTION A: 4x pro Tag (alle 6 Stunden)
```
Regenerations-Windows:
- 00:00 Uhr (Mitternacht)
- 06:00 Uhr (Morgen)
- 12:00 Uhr (Mittag)
- 18:00 Uhr (Abend)

Vorteile:
✅ Häufig frische Welt
✅ Spieler gewöhnen sich an feste Zeiten

Nachteile:
⚠️ Evtl. zu häufig (nervt Spieler?)
```

### OPTION B: 2x pro Tag (alle 12 Stunden)
```
Regenerations-Windows:
- 06:00 Uhr (Morgen)
- 18:00 Uhr (Abend)

Vorteile:
✅ Nicht zu häufig
✅ Gute Zeitpunkte (vor Peak-Hours)

Nachteile:
⚠️ Welt kann 12h alt werden
```

### OPTION C: 1x pro Tag (alle 24 Stunden)
```
Regenerations-Window:
- 04:00 Uhr (Nachts, wenig Spieler)

Vorteile:
✅ Minimal invasiv
✅ Nachts wenig Spieler → oft automatic

Nachteile:
⚠️ Welt kann 24h alt werden
⚠️ Weniger Abwechslung
```

**EMPFEHLUNG: OPTION B (2x pro Tag, 6:00 + 18:00)**

---

## 🔧 BACKEND IMPLEMENTATION

### 1. Database Schema
```sql
-- Tracking der Regenerations-Events
CREATE TABLE world_regenerations (
    id SERIAL PRIMARY KEY,
    regenerated_at TIMESTAMP NOT NULL,
    trigger_type VARCHAR(20) NOT NULL,  -- 'automatic' oder 'forced'
    players_teleported INT DEFAULT 0,
    duration_seconds INT
);

-- Player Location Tracking
CREATE TABLE player_locations (
    player_id INT PRIMARY KEY,
    current_location VARCHAR(100) NOT NULL,
    position_x FLOAT,
    position_y FLOAT,
    position_z FLOAT,
    last_updated TIMESTAMP NOT NULL,
    is_in_safe_zone BOOLEAN DEFAULT false
);
```

### 2. API Endpoints
```python
# backend/api/world_regeneration.py

@router.get("/api/world/regeneration/status")
async def get_regeneration_status():
    """Gibt aktuellen Regenerations-Status zurück"""
    return {
        "last_regeneration": system.last_regeneration.isoformat(),
        "next_regeneration": system.next_forced_regen.isoformat(),
        "all_players_safe": system.all_players_in_safe_zones(),
        "online_players": len(get_all_online_players()),
        "players_in_overworld": system.count_players_in_overworld()
    }

@router.post("/api/world/regeneration/trigger")
@require_admin
async def trigger_regeneration_manual():
    """Admin kann manuell Regeneration triggern"""
    system.force_regeneration()
    return {"success": True, "message": "Regeneration gestartet"}

@router.post("/api/player/location/update")
async def update_player_location(data: LocationUpdate):
    """Spieler sendet Position-Update"""
    player_id = data.player_id
    location = data.location
    position = data.position

    # Update DB
    db.update_player_location(
        player_id=player_id,
        location=location,
        position=position,
        is_in_safe_zone=system.is_in_safe_zone_name(location)
    )

    # Check: Sind jetzt alle Spieler in Städten?
    if system.all_players_in_safe_zones():
        # Trigger opportunistic regeneration!
        system.regenerate_world()

    return {"success": True}
```

### 3. Background Task (FastAPI)
```python
# backend/main_fastapi.py

from fastapi import BackgroundTasks
import asyncio

async def world_regeneration_loop():
    """Background Task: Läuft permanent"""
    while True:
        try:
            # Update System (prüft Regenerations-Bedingungen)
            world_regen_system.update()

            # Warte 60 Sekunden
            await asyncio.sleep(60)

        except Exception as e:
            print(f"❌ World Regen Loop Error: {e}")
            await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    # Starte Background-Loop
    asyncio.create_task(world_regeneration_loop())
    print("🌍 World Regeneration System gestartet!")
```

---

## 🎨 FRONTEND UI

### Warning UI (10min vor Zwangs-Teleport)
```javascript
// digivice/js/world_regeneration_ui.js

class WorldRegenerationUI {
    showWarning(minutesLeft) {
        // Großes UI-Banner
        const banner = document.createElement('div');
        banner.id = 'world-regen-warning';
        banner.style.cssText = `
            position: fixed;
            top: 0; left: 0; right: 0;
            background: linear-gradient(135deg, #ff6b00, #ff0000);
            color: white;
            padding: 20px;
            text-align: center;
            z-index: 99999;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 4px 20px rgba(255,0,0,0.5);
            animation: pulse 2s infinite;
        `;

        banner.innerHTML = `
            <div>
                ⚠️ WELT-REGENERATION IN ${minutesLeft} MINUTEN! ⚠️
            </div>
            <div style="font-size: 16px; margin-top: 10px;">
                Kehre zu einer Stadt zurück oder werde automatisch teleportiert!
            </div>
            <div id="regen-countdown" style="font-size: 32px; margin: 10px 0;">
                ${minutesLeft}:00
            </div>
            <button onclick="window.WorldRegenUI.quickTeleport()"
                    style="padding: 15px 40px; font-size: 18px; cursor: pointer; background: #fff; color: #ff0000; border: none; border-radius: 5px; font-weight: bold;">
                🏠 JETZT TELEPORTIEREN
            </button>
        `;

        document.body.appendChild(banner);

        // Sound-Warnung
        this.playWarningSound();

        // Countdown starten
        this.startCountdown(minutesLeft * 60);
    }

    startCountdown(seconds) {
        const countdownEl = document.getElementById('regen-countdown');

        const interval = setInterval(() => {
            seconds--;
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;

            if (countdownEl) {
                countdownEl.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
            }

            // Sound bei letzten 10 Sekunden
            if (seconds <= 10 && seconds > 0) {
                this.playTickSound();
            }

            if (seconds <= 0) {
                clearInterval(interval);
                this.showTeleportingScreen();
            }
        }, 1000);
    }

    quickTeleport() {
        // API-Call: Spieler zur nächsten Stadt teleportieren
        fetch('/api/player/teleport/nearest-city', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_id: window.playerId })
        }).then(() => {
            this.showSuccess("✅ Zur Stadt teleportiert!");
            this.hideWarning();
        });
    }

    playWarningSound() {
        const audio = new Audio('/static/sounds/warning.mp3');
        audio.volume = 0.5;
        audio.play();
    }
}

window.WorldRegenUI = new WorldRegenerationUI();
```

### WebSocket für Live-Warnings
```javascript
// digivice/js/websocket_handlers.js

socket.on('world_regeneration_warning', (data) => {
    const { minutes_left } = data;
    window.WorldRegenUI.showWarning(minutes_left);
});

socket.on('world_regeneration_complete', (data) => {
    window.WorldRegenUI.showNotification("🌍 Die Welt wurde regeneriert! Neue Abenteuer warten!");
});

socket.on('forced_teleport', (data) => {
    const { destination } = data;
    window.WorldRegenUI.showTeleportScreen(destination);
    // Scene wird automatisch neu geladen
});
```

---

## ✅ ZUSAMMENFASSUNG

### DAS SYSTEM MACHT:

1. **Jede Minute:** Prüfe ob alle Spieler in Städten sind
   - JA → Sofort regenerieren! ✅
   - NEIN → Warten bis Deadline

2. **Zur Deadline (z.B. 6:00, 18:00):**
   - 10min vorher: Warnung #1
   - 5min vorher: Warnung #2
   - 1min vorher: Letzte Warnung
   - 0min: Zwangs-Teleport + Regeneration

3. **Nach Regeneration:**
   - Neue prozedural generierte Welt
   - Neue Enemies
   - Neue Resources
   - Alle Spieler bekommen Notification

### VORTEILE:
- ✅ Meist friedliche Regeneration (wenn alle in Städten)
- ✅ Garantierte Regeneration (Fallback zu festen Zeiten)
- ✅ Kein Camping-Problem (Zwangs-Teleport)
- ✅ Fair für alle Spieler

---

**Bereit für Implementation?** 🚀
