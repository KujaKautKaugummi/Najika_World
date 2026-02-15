# MULTIPLAYER WORLD REGENERATION - DESIGN 2026-02-15

**Problem:** Wie verhindern wir dass die Welt neu generiert wird während Spieler in der Open-World sind?

---

## 🎯 DEINE IDEE (Ausgangspunkt)

> "Alle Spieler müssen in einer Stadt oder besonderen Ort sein, damit Welt regeneriert werden kann."

**Problem:** Was wenn Spieler ewig campen um Regeneration zu blocken?

---

## 💡 MEINE LÖSUNGS-VORSCHLÄGE

### ✅ OPTION 1: SERVER-GESTEUERTE REGENERATIONS-FENSTER (EMPFOHLEN!)

**Konzept:**
- Server legt **feste Regenerations-Zeiten** fest (z.B. alle 6 Stunden)
- 10 Minuten vorher: **Warnung an ALLE Spieler**
- 5 Minuten vorher: **Teleport-Countdown** erscheint
- 0 Minuten: **Zwangs-Teleport** in nächste Stadt + Welt regeneriert

**Vorteile:**
- ✅ Keine Camping-Probleme (Zwangs-Teleport!)
- ✅ Fair für alle Spieler (feste Zeiten)
- ✅ Server hat Kontrolle

**Implementation:**
```yaml
regeneration_schedule:
  interval: 6 Stunden (4x pro Tag)
  times: "00:00, 06:00, 12:00, 18:00 (Server-Zeit)"

  warnings:
    - time: -10 Minuten
      message: "⚠️ WELT REGENERIERT IN 10 MINUTEN! Kehre zu einer Stadt zurück!"
      action: "Großes UI-Banner + Sound"

    - time: -5 Minuten
      message: "⚠️ WELT REGENERIERT IN 5 MINUTEN! Auto-Teleport in 5min!"
      action: "Countdown-Timer im UI"

    - time: -1 Minute
      message: "⚠️ WELT REGENERIERT IN 1 MINUTE! LETZTER AUFRUF!"
      action: "Screen-Flash + lauter Sound"

    - time: 0
      message: "🌍 WELT WIRD REGENERIERT..."
      action: |
        1. Alle Spieler → Zwangs-Teleport zur nächsten Stadt
        2. Welt regenerieren (Prozedural)
        3. Spieler können wieder raus

  exceptions:
    - "Spieler im Combat → Combat wird beendet (keine Belohnung)"
    - "Spieler in Dungeon → Dungeon-Progress gespeichert, später fortsetzbar"
```

**Beispiel UI-Warnung:**
```
┌───────────────────────────────────────────────┐
│  ⚠️  WELT-REGENERATION IN 5 MINUTEN!  ⚠️     │
├───────────────────────────────────────────────┤
│                                               │
│  Die Open-World wird in 5 Minuten neu        │
│  generiert. Kehre zu einer Stadt zurück       │
│  oder werde automatisch teleportiert!         │
│                                               │
│         ⏱️ Verbleibende Zeit: 04:37          │
│                                               │
│  [Jetzt teleportieren] [Weiter spielen]      │
└───────────────────────────────────────────────┘
```

---

### ✅ OPTION 2: DYNAMISCHE REGENERATION (REGIONEN-BASIERT)

**Konzept:**
- Welt wird NICHT komplett regeneriert
- Nur **Regionen regenerieren** die **LEER** sind (keine Spieler)
- Jede Region hat eigenen Regenerations-Timer

**Vorteile:**
- ✅ Keine Zwangs-Teleports nötig
- ✅ Spieler können endlos in 1 Region bleiben
- ✅ Andere Regionen regenerieren trotzdem

**Implementation:**
```yaml
region_regeneration:
  trigger: "Region ist leer (keine Spieler) für X Minuten"
  cooldown: 30 Minuten

  regions:
    fluesterswald:
      last_player_left: "2026-02-15 10:00"
      regeneration_eligible: "2026-02-15 10:30"
      status: "LEER → Kann regenerieren"

    kristallberge:
      last_player_left: null
      players_inside: 3
      status: "BEWOHNT → Keine Regeneration"

    sumpf_myrkr:
      last_player_left: "2026-02-15 09:00"
      regeneration_eligible: "2026-02-15 09:30"
      status: "REGENERIERT um 09:30"

  rules:
    - "Spieler betritt Region → Regenerations-Timer stoppt"
    - "Spieler verlässt Region → Timer startet (30min)"
    - "Nach 30min → Region regeneriert NUR wenn immer noch leer"
```

**Problem:**
- ⚠️ Beliebte Regionen regenerieren NIE (immer Spieler drin)
- ⚠️ Spieler könnten "Farming-Spots" dauerhaft blockieren

**Lösung für Problem:**
- **Max-Staleness-Timer:** Auch bewohnte Regionen regenerieren nach 24h (Zwangs-Kick!)

---

### ✅ OPTION 3: INSTANZIERTE WELTEN (MMO-Style)

**Konzept:**
- Jede Region hat **mehrere Instanzen** (wie WoW Sharding)
- Instanz 1 (alt, seit 6h) → wird geschlossen, neue Spieler gehen in Instanz 2 (neu)
- Spieler in Instanz 1 spielen weiter bis sie verlassen
- Dann automatisch in neueste Instanz

**Vorteile:**
- ✅ KEINE Zwangs-Teleports!
- ✅ Spieler merken Regeneration kaum
- ✅ Keine Camping-Probleme

**Nachteile:**
- ❌ Komplexer (mehrere Welten gleichzeitig)
- ❌ Spieler könnten in verschiedenen Instanzen sein (Anti-Multiplayer!)

**Implementation:**
```yaml
instance_system:
  fluesterswald:
    instances:
      - id: "fluesterswald_1"
        created: "2026-02-15 08:00"
        status: "DEPRECATED (alt)"
        players: 2 (werden nicht rausgeworfen)
        new_joins: false (neue Spieler gehen in #2)

      - id: "fluesterswald_2"
        created: "2026-02-15 14:00"
        status: "ACTIVE (neu)"
        players: 15
        new_joins: true

  rules:
    - "Instanz wird alle 6h neu erstellt"
    - "Alte Instanz wird als DEPRECATED markiert"
    - "Neue Spieler gehen NUR in neueste Instanz"
    - "Spieler in alter Instanz können weiter spielen"
    - "Wenn Spieler Region verlässt → automatisch in neueste Instanz beim Re-Enter"
```

---

## 🎮 MEINE EMPFEHLUNG: HYBRID-SYSTEM

**Kombination aus Option 1 + 2:**

### NORMAL-MODUS (90% der Zeit):
- Regionen regenerieren **dynamisch** (Option 2)
- Nur leere Regionen nach 30min
- Beliebte Regionen bleiben stabil

### GLOBAL-REGENERATION (10% der Zeit):
- Alle 24 Stunden: **Server-weite Regeneration** (Option 1)
- Alle Spieler bekommen 10min Warnung
- Zwangs-Teleport zu Städten
- KOMPLETTE Welt wird neu generiert

### VORTEIL:
- ✅ Meist keine Zwangs-Kicks (dynamische Regeneration)
- ✅ Aber 1x pro Tag: Garantierte Frische (Global-Regeneration)
- ✅ Kein Camping-Problem (Max 24h)

---

## 📋 IMPLEMENTATION (BACKEND)

### 1. Region-State-Tracking
```python
# backend/systems/world_regeneration.py

class RegionState:
    region_id: str
    players_inside: List[int]  # Player IDs
    last_player_left: datetime
    last_regenerated: datetime
    regeneration_scheduled: bool

class WorldRegenerationSystem:
    def __init__(self):
        self.regions = {}  # region_id → RegionState
        self.global_regen_schedule = "00:00"  # Jeden Tag Mitternacht

    def on_player_enter_region(self, player_id, region_id):
        """Spieler betritt Region → Cancel Regeneration"""
        region = self.regions[region_id]
        region.players_inside.append(player_id)
        region.regeneration_scheduled = False  # Cancel!

    def on_player_leave_region(self, player_id, region_id):
        """Spieler verlässt Region → Start Timer"""
        region = self.regions[region_id]
        region.players_inside.remove(player_id)

        if len(region.players_inside) == 0:
            region.last_player_left = datetime.now()
            # Schedule Regeneration in 30min
            schedule_task(self.regenerate_region, region_id, delay=1800)

    def regenerate_region(self, region_id):
        """Regeneriert Region wenn immer noch leer"""
        region = self.regions[region_id]

        # Check: Immer noch leer?
        if len(region.players_inside) > 0:
            print(f"❌ Region {region_id} nicht leer → Abbruch")
            return

        # Regenerate!
        print(f"🌍 Regenerating region: {region_id}")
        world_generator.regenerate_region(region_id)
        region.last_regenerated = datetime.now()

    def global_regeneration(self):
        """Komplette Welt regenerieren (1x pro Tag)"""
        # 10min Warnung
        self.send_global_warning("⚠️ WELT REGENERIERT IN 10 MINUTEN!")
        sleep(600)  # 10min warten

        # Alle Spieler teleportieren
        for player in get_all_online_players():
            if player.is_in_city():
                continue  # Schon in Stadt
            else:
                nearest_city = find_nearest_city(player.position)
                teleport_player(player.id, nearest_city)

        # Welt regenerieren
        world_generator.regenerate_all_regions()
        print("🌍 Komplette Welt regeneriert!")
```

### 2. Player-Position-Tracking
```python
# backend/api/multiplayer.py

@router.post("/api/multiplayer/position/update")
async def update_player_position(data: PositionUpdate):
    """Spieler sendet Position → Track Region"""
    region_id = get_region_from_position(data.position)

    # Update Region State
    if player.current_region != region_id:
        # Spieler wechselt Region!
        world_regen.on_player_leave_region(player.id, player.current_region)
        world_regen.on_player_enter_region(player.id, region_id)
        player.current_region = region_id

    return {"success": True}
```

### 3. Warning-System (Frontend)
```javascript
// digivice/js/world_regeneration_ui.js

class WorldRegenerationUI {
    showWarning(minutesLeft) {
        const banner = document.createElement('div');
        banner.id = 'regen-warning';
        banner.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255,100,0,0.95);
            border: 3px solid #ff0000;
            padding: 20px;
            border-radius: 10px;
            z-index: 10000;
            font-size: 18px;
            box-shadow: 0 0 20px rgba(255,0,0,0.5);
        `;

        banner.innerHTML = `
            <div style="text-align:center;">
                <h2>⚠️ WELT-REGENERATION IN ${minutesLeft} MINUTEN! ⚠️</h2>
                <p>Kehre zu einer Stadt zurück oder werde automatisch teleportiert!</p>
                <div style="font-size: 32px; margin: 10px 0;" id="countdown-timer">${minutesLeft}:00</div>
                <button onclick="window.RegenerationUI.teleportToCity()"
                        style="padding: 10px 30px; font-size: 16px; cursor: pointer;">
                    🏠 Jetzt Teleportieren
                </button>
            </div>
        `;

        document.body.appendChild(banner);
        this.startCountdown(minutesLeft * 60);
    }

    startCountdown(seconds) {
        const timer = setInterval(() => {
            seconds--;
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            document.getElementById('countdown-timer').textContent =
                `${mins}:${secs.toString().padStart(2, '0')}`;

            if (seconds <= 0) {
                clearInterval(timer);
            }
        }, 1000);
    }
}
```

---

## ❓ OFFENE FRAGEN FÜR DICH

1. **Wie oft soll die Welt regenerieren?**
   - Alle 6 Stunden? Alle 12 Stunden? 1x pro Tag?

2. **Regionen-basiert oder komplett?**
   - HYBRID (meine Empfehlung)?
   - NUR Regionen-basiert (kein Global-Reset)?
   - NUR Global-Reset (feste Zeiten)?

3. **Zwangs-Teleport oder Soft-Warning?**
   - Zwangs-Teleport nach Countdown? (harscher)
   - Nur Warnung, Spieler entscheidet? (weicher, aber Camping-Gefahr)

4. **Was passiert bei Combat während Regeneration?**
   - Combat sofort beenden (keine Belohnung)?
   - Combat zu Ende spielen lassen (Regeneration wartet)?

5. **Dungeon-Progress?**
   - Dungeons resetten auch?
   - Oder Dungeons sind instanziert (unabhängig von Welt-Regen)?

---

**Warte auf deine Entscheidung!** 🎮
