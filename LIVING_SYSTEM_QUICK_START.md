# 🎮 LIVING SYSTEM - QUICK START

**Status:** Fertig implementiert!
**Datum:** 9. November 2025

---

## ✅ WAS IST FERTIG?

### Backend (Python):
- ✅ **najika_living_system.py** - Komplettes Living System
  - Hunger/Energy/Mood Game-Stats
  - Selbstfürsorge (20% → 50%)
  - Anger-System
  - 5 Unfall-Typen
  - Player-Actions (Feed, Bed)
  - Control-Mode (AI vs Player)

- ✅ **najika_living_api.py** - REST API
  - 9 Endpoints
  - State-Persistence (JSON File)
  - CORS enabled

---

## 🚀 STARTEN

### Backend Server starten:

```bash
cd backend
python najika_living_api.py
```

**Server läuft auf:** http://localhost:5001

---

## 📡 API ENDPOINTS

### 1. **GET /api/living/status**
Holt aktuellen Status

```bash
curl http://localhost:5001/api/living/status
```

**Response:**
```json
{
  "status": "ok",
  "state": {
    "hunger": 85.5,
    "energy": 92.0,
    "mood_game": 78.3,
    "anger_level": 12.5,
    "control_mode": "ai",
    "player_online": false
  }
}
```

---

### 2. **POST /api/living/feed**
Spieler füttert Najika

```bash
curl -X POST http://localhost:5001/api/living/feed \
  -H "Content-Type: application/json" \
  -d '{"food_value": 30}'
```

**Response:**
```json
{
  "status": "ok",
  "result": {
    "action": "player_feeds",
    "hunger_before": 45.0,
    "hunger_after": 75.0,
    "anger_level": 8.0,
    "najika_says": "Danke! Das schmeckt super! 😋"
  }
}
```

---

### 3. **POST /api/living/sleep**
Najika ins Bett legen

```bash
curl -X POST http://localhost:5001/api/living/sleep
```

**Response:**
```json
{
  "result": {
    "action": "player_bed",
    "energy_before": 35.0,
    "energy_after": 100.0,
    "najika_says": "Danke... so kuschelig... 😴💤"
  }
}
```

---

### 4. **POST /api/living/control**
Control-Mode setzen

```bash
curl -X POST http://localhost:5001/api/living/control \
  -H "Content-Type: application/json" \
  -d '{"mode": "player", "online": true}'
```

---

### 5. **GET /api/living/greeting**
Begrüßung holen (abhängig von Anger & Abwesenheit)

```bash
curl http://localhost:5001/api/living/greeting
```

**Response:**
```json
{
  "greeting": "Hey! Schon zurück? 😊",
  "anger_level": 5.0,
  "hours_offline": 2.3
}
```

---

### 6. **POST /api/living/update**
Living System Force-Update

```bash
curl -X POST http://localhost:5001/api/living/update
```

---

### 7. **GET /api/living/stats**
Statistiken holen

```bash
curl http://localhost:5001/api/living/stats
```

---

### 8. **GET /api/living/state/export**
Kompletten State exportieren

```bash
curl http://localhost:5001/api/living/state/export > state_backup.json
```

---

### 9. **POST /api/living/state/import**
State importieren

```bash
curl -X POST http://localhost:5001/api/living/state/import \
  -H "Content-Type: application/json" \
  -d @state_backup.json
```

---

## 💾 STATE-PERSISTENCE

State wird automatisch gespeichert in:
```
backend/saves/najika_living_state.json
```

---

## 🎮 USAGE BEISPIELE

### JavaScript (Frontend):

```javascript
// Status holen
async function getNajikaStatus() {
  const res = await fetch('http://localhost:5001/api/living/status');
  const data = await res.json();
  console.log('Hunger:', data.state.hunger);
  console.log('Anger:', data.state.anger_level);
}

// Najika füttern
async function feedNajika() {
  const res = await fetch('http://localhost:5001/api/living/feed', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({food_value: 30})
  });
  const data = await res.json();
  alert(data.result.najika_says);  // "Danke! Das schmeckt super! 😋"
}

// Player-Modus aktivieren (wenn User spielt)
async function startPlaying() {
  await fetch('http://localhost:5001/api/living/control', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({mode: 'player', online: true})
  });
}

// AI-Modus aktivieren (wenn User offline)
async function stopPlaying() {
  await fetch('http://localhost:5001/api/living/control', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({mode: 'ai', online: false})
  });
}
```

---

### Python (Testing):

```python
import requests

# Status holen
r = requests.get('http://localhost:5001/api/living/status')
state = r.json()['state']
print(f"Hunger: {state['hunger']}%")
print(f"Anger: {state['anger_level']}%")

# Najika füttern
r = requests.post('http://localhost:5001/api/living/feed',
                  json={'food_value': 50})
print(r.json()['result']['najika_says'])

# Ins Bett legen
r = requests.post('http://localhost:5001/api/living/sleep')
print(r.json()['result']['najika_says'])
```

---

## 🔧 INTEGRATION IN WEB/MOBILE

### Web (V2):

```javascript
// in digivice/js/najika_living.js

class NajikaLiving {
  constructor() {
    this.apiUrl = 'http://localhost:5001/api/living';
    this.updateInterval = 60000;  // 1 Minute
    this.startAutoUpdate();
  }

  startAutoUpdate() {
    setInterval(() => {
      this.update();
    }, this.updateInterval);
  }

  async update() {
    const res = await fetch(`${this.apiUrl}/status`);
    const data = await res.json();

    // Update UI
    this.updateStatsUI(data.state);

    // Check Warnings
    if (data.update_results.warnings.length > 0) {
      this.showWarnings(data.update_results.warnings);
    }

    // Check Unfälle
    if (data.update_results.accidents.length > 0) {
      this.handleAccidents(data.update_results.accidents);
    }
  }

  updateStatsUI(state) {
    document.getElementById('hunger-bar').style.width = state.hunger + '%';
    document.getElementById('energy-bar').style.width = state.energy + '%';
    document.getElementById('anger-bar').style.width = state.anger_level + '%';

    // Anger-Warning
    if (state.anger_level > 50) {
      document.getElementById('anger-warning').style.display = 'block';
    }
  }

  async feedNajika() {
    const res = await fetch(`${this.apiUrl}/feed`, {method: 'POST'});
    const data = await res.json();
    this.showNajikaMessage(data.result.najika_says);
  }

  async putToBed() {
    const res = await fetch(`${this.apiUrl}/sleep`, {method: 'POST'});
    const data = await res.json();
    this.showNajikaMessage(data.result.najika_says);
  }
}

// Init
const living = new NajikaLiving();
```

---

### Mobile (Flutter):

```dart
// In lib/services/living_service.dart

class LivingService {
  final String apiUrl = 'http://localhost:5001/api/living';

  Future<Map<String, dynamic>> getStatus() async {
    final res = await http.get(Uri.parse('$apiUrl/status'));
    return jsonDecode(res.body);
  }

  Future<void> feedNajika() async {
    final res = await http.post(
      Uri.parse('$apiUrl/feed'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'food_value': 30})
    );
    final data = jsonDecode(res.body);
    print(data['result']['najika_says']);
  }

  Future<void> setControlMode(String mode, bool online) async {
    await http.post(
      Uri.parse('$apiUrl/control'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'mode': mode, 'online': online})
    );
  }
}
```

---

## 📊 STATS & BALANCE

### Aktuelle Werte:

| Parameter | Wert |
|-----------|------|
| Hunger Decay | -5% pro Stunde |
| Energy Decay | -3% pro Stunde |
| Auto-Care Threshold | 20% |
| Auto-Care Max | 50% |
| Anger Gain (Auto-Eat) | +10 |
| Anger Gain (Auto-Sleep) | +8 |
| Anger Loss (Player Feed) | -5 |
| Anger Loss (Player Bed) | -15 |
| Max Accidents/Day | 3 |

**Diese Werte können in `najika_living_system.py` angepasst werden!**

---

## 🐛 TESTING

### Test-Script:

```python
#!/usr/bin/env python3
# test_living_system.py

import requests
import time

api = 'http://localhost:5001/api/living'

# 1. Initial Status
print("=== INITIAL STATUS ===")
r = requests.get(f'{api}/status')
state = r.json()['state']
print(f"Hunger: {state['hunger']:.1f}%")
print(f"Energy: {state['energy']:.1f}%")
print(f"Anger: {state['anger_level']:.1f}%")

# 2. Hunger auf 15% reduzieren (simuliere Zeit)
print("\n=== SIMULATE TIME (Hunger → 15%) ===")
r = requests.post(f'{api}/state/import', json={
    'state': {'hunger': 15.0, 'energy': 80.0}
})

# 3. Force Update (Auto-Care sollte aktivieren)
print("\n=== FORCE UPDATE (Auto-Care) ===")
r = requests.post(f'{api}/update')
results = r.json()['results']

if results['auto_care_actions']:
    print("Auto-Care aktiviert!")
    for action in results['auto_care_actions']:
        print(f"  - {action['action']}: {action['najika_says']}")

# 4. Player füttert Najika
print("\n=== PLAYER FEEDS NAJIKA ===")
r = requests.post(f'{api}/feed', json={'food_value': 50})
result = r.json()['result']
print(f"Najika: {result['najika_says']}")
print(f"Hunger: {result['hunger_before']:.1f}% → {result['hunger_after']:.1f}%")
print(f"Anger: {result['anger_level']:.1f}%")

# 5. Greeting
print("\n=== GREETING ===")
r = requests.get(f'{api}/greeting')
data = r.json()
print(f"Najika sagt: {data['greeting']}")
```

**Run:**
```bash
python test_living_system.py
```

---

## ✅ DONE FOR TODAY!

**Tag 1 Backend - FERTIG! 🎉**

### Erstellt:
- ✅ Living System mit Selbstfürsorge
- ✅ REST API (9 Endpoints)
- ✅ State-Persistence
- ✅ Testing-Tools

### Nächste Schritte (für Web-Modelle):
1. **Web #1:** Terrain-Farben + Vegetation implementieren
2. **Web #2:** 5 Städte bauen + Lighting

### Morgen (Tag 2):
- Farming Backend
- Fishing Backend
- Web-Integration

---

**Erstellt:** 2025-11-09
**Autor:** Claude Code (CLI)
