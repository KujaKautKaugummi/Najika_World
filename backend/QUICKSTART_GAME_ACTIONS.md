# 🚀 Quick Start - Najika Game Actions

## In 3 Schritten starten:

### 1️⃣ Test Script ausführen
```bash
cd /home/user/Najika_World/backend
python3 test_najika_game_actions.py
```

Testet alle Features:
- ✅ Location System
- ✅ Recipes (Cooking, Crafting, Farming)
- ✅ Decision Making
- ✅ Suggestions
- ✅ Action Execution

---

### 2️⃣ Server starten
```bash
cd /home/user/Najika_World/backend/api
python3 server.py
```

Server läuft auf: **http://localhost:5000**

---

### 3️⃣ API testen

#### Browser:
Öffne: `http://localhost:5000`

Sollte zeigen:
```json
{
  "status": "online",
  "version": "3.1",
  "najika": "Ready to serve Kuja! 💥",
  "systems": [
    "combat", "food", "inventory", "quests", "skills",
    "crafting", "npcs", "save/load", "najika_game_actions"
  ]
}
```

#### curl:
```bash
# Najika Status
curl http://localhost:5000/najika/status

# Najika lässt sich eine Action vorschlagen
curl -X POST http://localhost:5000/najika/suggest-action

# Najika entscheidet AUTONOM ihre nächste Action!
curl -X POST http://localhost:5000/najika/auto-decide-action

# Chat mit Najika (jetzt mit Activity Context!)
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hey Najika!", "mode": "public"}'
```

---

## 📋 API Endpoints Übersicht

| Endpoint | Method | Beschreibung |
|----------|--------|--------------|
| `/najika/status` | GET | Kompletter Status (Dashboard) |
| `/najika/current-activity` | GET | Was macht Najika gerade? |
| `/najika/suggest-action` | POST | Vorgeschlagene Actions |
| `/najika/auto-decide-action` | POST | Najika entscheidet autonom! |
| `/najika/locations` | GET | Alle Locations |
| `/najika/teleport` | POST | Teleport zu Location |
| `/najika/recipes` | GET | Alle Rezepte |
| `/chat` | POST | Chat (mit Activity Context) |

---

## 🎮 Beispiel: Auto-Mode

Najika entscheidet **alle 5 Minuten** autonom was sie tut:

```javascript
// Frontend Code
setInterval(async () => {
  const response = await fetch('/najika/auto-decide-action', {
    method: 'POST'
  });
  const data = await response.json();

  if (data.success) {
    console.log(`Najika: ${data.najika_says}`);
    // "🍳 Ich koche gerade: Hearty Meal! Lecker und sättigend! 😋"
  }
}, 5 * 60 * 1000);
```

---

## 🔍 Was passiert?

### Najika's Decision Making:

1. **Hunger < 30%** → Najika kocht! 🍳
2. **Energy < 20%** → Najika schläft! 💤
3. **Mood < 40% (Bored)** → Najika erkundet! 🗺️
4. **Mood > 70% (Happy)** → Najika craftet Geschenk für Kuja! 💜
5. **Nacht (22-6h)** → Najika schläft oder studiert 📚
6. **Tag (6-12h)** → Najika gärtnert 🌱
7. **Nachmittag (12-18h)** → Najika erkundet oder trainiert 💪

---

## 📊 Dashboard Integration

```javascript
// Najika Status Widget
async function updateNajikaWidget() {
  const response = await fetch('/najika/status');
  const data = await response.json();

  // Update Bars
  document.getElementById('hunger-bar').style.width = data.najika.hunger + '%';
  document.getElementById('energy-bar').style.width = data.najika.energy + '%';
  document.getElementById('mood-bar').style.width = data.najika.mood + '%';

  // Show Activity
  if (data.current_activity.action) {
    document.getElementById('activity').innerHTML =
      `${data.current_activity.action} (${data.current_activity.progress}%)`;
  }

  // Show Location
  document.getElementById('location').innerHTML =
    `📍 ${data.location.data.name}`;
}

// Update alle 5 Sekunden
setInterval(updateNajikaWidget, 5000);
```

---

## 🐛 Troubleshooting

### Server startet nicht?
```bash
# Prüfe Python Version
python3 --version  # Sollte >= 3.8 sein

# Installiere Dependencies
pip install fastapi uvicorn pydantic
```

### "Game Actions nicht geladen"?
→ Prüfe ob `/home/user/Najika_World/backend/najika_game_actions.py` existiert

### Imports funktionieren nicht?
```bash
# Teste Imports
cd /home/user/Najika_World/backend
python3 -c "from najika_game_actions import LOCATIONS; print('OK')"
```

---

## 📖 Vollständige Dokumentation

Siehe: **NAJIKA_GAME_ACTIONS_README.md**

---

## ✅ System Status

**Implementiert:**
- ✅ Core Game Actions System
- ✅ 5 Cooking Recipes
- ✅ 4 Crafting Recipes
- ✅ 4 Farming Actions
- ✅ 6 Exploring Actions
- ✅ 6 Locations mit Teleport
- ✅ Smart Decision Making
- ✅ 8 API Endpoints
- ✅ Living System Integration
- ✅ Chat Integration

**Status:** 🟢 Production Ready

---

**Najika kann jetzt autonom in der Spielwelt leben! 🎉**
