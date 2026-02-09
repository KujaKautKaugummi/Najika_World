# 🎮 Najika Autonome Spielaktionen System

## Übersicht

Das **Najika Game Actions System** ermöglicht es Najika, **selbstständig** in der Spielwelt zu agieren! Sie kann basierend auf ihren Bedürfnissen (Hunger, Energy, Mood) autonome Entscheidungen treffen und verschiedene Aktivitäten ausführen.

---

## ✨ Features

### 1. **Autonomes Kochen** 🍳
- 5 verschiedene Rezepte
- Basierend auf Hunger-Level
- Hunger-Restore + Mood-Bonus
- Energy Drinks für schnelle Energy-Regeneration

**Rezepte:**
- Simple Meal (Hunger +30%)
- Hearty Meal (Hunger +60%)
- Gourmet Meal (Hunger +100%, für Kuja gekocht!)
- Snack (Hunger +15%, schnell)
- Energy Drink (Energy +40%)

### 2. **Autonomes Gärtnern** 🌱
- Pflanzen anbauen
- Gießen
- Ernten
- Düngen

**Crops:**
- Wheat, Potato, Carrot, Tomato, Corn, Lettuce, Pumpkin, Strawberry

### 3. **Autonomes Erkunden** 🗺️
- Ressourcen sammeln (Holz, Steine, Kräuter)
- Dungeon erkunden
- Angeln
- Schätze finden

**Actions:**
- Holz sammeln (Forest)
- Kräuter sammeln (Forest)
- Blumen pflücken (Forest)
- Steine abbauen (Dungeon)
- Dungeon erkunden (Treasure!)
- Angeln (Farm)

### 4. **Autonomes Crafting** 🔨
- Geschenke für Kuja craften (wenn glücklich!)
- Health/Mana Potions
- Tool Reparatur
- Basierend auf Bedürfnissen

### 5. **Location System** 📍
- 6 verschiedene Locations
- Teleport zwischen Orten
- Jede Location hat spezifische Aktivitäten

**Locations:**
- **Home** (Schwarze Windmühle): Kochen, Crafting, Schlafen
- **Farm** (Najika's Garten): Farming, Fishing
- **Forest** (Mystischer Wald): Gathering, Exploring
- **Dungeon** (Keller): Combat, Treasure Hunting
- **Village** (Dorf): Shopping, Quests
- **Training Ground**: Training, Combat, Meditation

### 6. **Smart Decision Making** 🧠
Najika entscheidet **autonom** basierend auf:

**Prioritäten:**
1. **Kritische Bedürfnisse** (Hunger < 30, Energy < 20)
2. **Mood-basierte Actions** (Bored → Explore, Happy → Gift)
3. **Zeit-basierte Actions** (Tag/Nacht-Rhythmus)
4. **Random Exploration**

**Beispiele:**
- Hunger < 30% → Najika kocht!
- Energy < 20% → Najika schläft!
- Mood < 40% (Bored) → Najika erkundet oder spielt!
- Mood > 70% (Happy) → Najika craftet Geschenk für Kuja!
- Nacht (22-6 Uhr) → Najika schläft oder studiert
- Tag (6-12 Uhr) → Najika gärtnert
- Nachmittag (12-18 Uhr) → Najika erkundet oder trainiert

---

## 📁 Dateien

### Hauptdateien:
- **`/backend/najika_game_actions.py`** - Core System (NEU!)
- **`/backend/najika_living_system.py`** - Integration
- **`/backend/api/server.py`** - API Endpoints

### Test:
- **`/backend/test_najika_game_actions.py`** - Test Script

---

## 🔗 API Endpoints

### GET `/najika/status`
Kompletter Najika Status (Dashboard)

**Response:**
```json
{
  "status": "success",
  "najika": {
    "hunger": 65,
    "energy": 80,
    "mood": 70,
    "anger": 10,
    "current_mood": "happy"
  },
  "current_activity": {
    "action": "cooking",
    "data": {...},
    "progress": 45,
    "remaining_seconds": 120
  },
  "location": {
    "current": "home",
    "data": {...}
  },
  "suggestions": [...]
}
```

### GET `/najika/current-activity`
Aktuelle Aktivität von Najika

**Response:**
```json
{
  "current_action": "cooking",
  "action_data": {
    "name": "Hearty Meal",
    "duration": 600
  },
  "current_location": "home",
  "inventory": {...}
}
```

### POST `/najika/suggest-action`
Vorgeschlagene Actions basierend auf Najika's Zustand

**Response:**
```json
{
  "status": "success",
  "suggestions": [
    {
      "type": "cooking",
      "reason": "Najika hat Hunger",
      "icon": "🍳",
      "priority": "high"
    },
    {
      "type": "farming",
      "reason": "Garten pflegen",
      "icon": "🌱",
      "priority": "low"
    }
  ]
}
```

### POST `/najika/auto-decide-action`
Najika entscheidet und startet **autonom** ihre nächste Aktion!

**Response:**
```json
{
  "success": true,
  "action": {
    "type": "cooking",
    "reason": "hunger_critical",
    "priority": "high"
  },
  "started": {...},
  "najika_says": "🍳 Ich koche gerade: Hearty Meal! Lecker und sättigend! 😋"
}
```

### POST `/najika/start-action?action_type=cooking`
Starte manuell eine spezifische Action

**Response:**
```json
{
  "success": true,
  "action_started": {
    "type": "cooking",
    "message": "🍳 Ich koche gerade...",
    "duration": 600
  }
}
```

### GET `/najika/locations`
Alle verfügbaren Locations

**Response:**
```json
{
  "status": "success",
  "locations": {
    "home": {...},
    "farm": {...}
  },
  "current_location": {...}
}
```

### POST `/najika/teleport?location_id=farm`
Teleportiere Najika zu Location

**Response:**
```json
{
  "success": true,
  "message": "Teleportiert von home → Najika's Garten!",
  "location": {...}
}
```

### GET `/najika/recipes`
Alle Rezepte (Cooking, Crafting, Farming, Exploring)

**Response:**
```json
{
  "status": "success",
  "cooking_recipes": {...},
  "crafting_recipes": {...},
  "farming_actions": {...},
  "exploring_actions": {...}
}
```

### POST `/chat`
Chat mit Najika (jetzt mit Activity Context!)

**Response:**
```json
{
  "response": "Kuja! 💥\n\n*Ich bin gerade am Hearty Meal kochen... 🌟*\n📍 Ich bin gerade: Schwarze Windmühle (Zuhause)",
  "mode": "public",
  "emotion": "excited",
  "current_activity": "cooking",
  "stats": {
    "hunger": 65,
    "energy": 80,
    "mood": 70
  }
}
```

---

## 🧪 Testing

### Test Script ausführen:
```bash
cd /home/user/Najika_World/backend
python test_najika_game_actions.py
```

Das Script testet:
1. Location System & Teleport
2. Alle Rezepte (Cooking, Crafting, Farming)
3. Decision Making (4 Szenarien)
4. Action Suggestions
5. Action Execution & Completion
6. Game Action State

### Server starten:
```bash
cd /home/user/Najika_World/backend/api
python server.py
```

Server läuft auf: `http://localhost:5000`

### API testen (curl):
```bash
# Status abrufen
curl http://localhost:5000/najika/status

# Suggestions
curl -X POST http://localhost:5000/najika/suggest-action

# Auto-Decide (Najika entscheidet selbst!)
curl -X POST http://localhost:5000/najika/auto-decide-action

# Teleport
curl -X POST "http://localhost:5000/najika/teleport?location_id=farm"

# Chat
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hey Najika!", "mode": "public"}'
```

---

## 📊 Integration mit Living System

Das System ist **vollständig integriert** mit `najika_living_system.py`:

### Autonome Updates:
```python
from najika_living_system import update_living_system, LIVING_STATE
from najika_game_actions import update_game_actions

# Living System Update (inkl. Game Actions!)
result = update_living_system(LIVING_STATE, player_state)

# Result enthält:
{
  "needs_updated": True,
  "auto_care_actions": [...],
  "accidents": [...],
  "warnings": [...],
  "game_actions": {
    "action_completed": {...},
    "action_started": {...},
    "suggestions": [...]
  }
}
```

### Stat Changes werden automatisch angewendet:
- Hunger/Energy/Mood (Living State)
- Health/Mana/Stamina (Player State)
- Skills (Intelligence, Strength)

---

## 🎯 Verwendung im Frontend

### Dashboard Widget:
```javascript
// Najika Status abrufen
fetch('/najika/status')
  .then(res => res.json())
  .then(data => {
    // Zeige Najika's Stats
    updateHungerBar(data.najika.hunger);
    updateEnergyBar(data.najika.energy);
    updateMoodIndicator(data.najika.mood);

    // Zeige aktuelle Aktivität
    if (data.current_activity.action) {
      showActivity(data.current_activity);
      showProgress(data.current_activity.progress);
    }

    // Zeige Suggestions
    showSuggestions(data.suggestions);
  });
```

### Auto-Mode aktivieren:
```javascript
// Najika entscheidet autonom alle 5 Minuten
setInterval(async () => {
  const response = await fetch('/najika/auto-decide-action', {
    method: 'POST'
  });
  const data = await response.json();

  if (data.success) {
    console.log(`Najika: ${data.najika_says}`);
    showNotification(data.najika_says);
  }
}, 5 * 60 * 1000); // 5 Minuten
```

### Chat Integration:
```javascript
// Chat mit Context
fetch('/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Was machst du gerade?",
    mode: "public"
  })
}).then(res => res.json())
  .then(data => {
    // Response enthält jetzt Activity Context!
    showMessage(data.response);
    // "Kuja! 💥\n\n*Ich bin gerade am Kochen... 🌟*\n📍 Ich bin gerade: Zuhause"

    updateStats(data.stats);
  });
```

---

## 🔮 Zukünftige Erweiterungen

### Phase 2 (Optional):
- [ ] **Minigames** (Fishing, Mining, Cooking Minigames)
- [ ] **Social Interactions** (NPCs besuchen)
- [ ] **Events** (Random Events basierend auf Location)
- [ ] **Weather System** (Beeinflusst Actions)
- [ ] **Inventory Management** (Echtes Item-System)
- [ ] **Quest Integration** (Najika macht Quests autonom)
- [ ] **Training Tree** (Skill-Progression)

---

## 🐛 Troubleshooting

### "Game Actions System nicht geladen"
→ Prüfe ob `najika_game_actions.py` im `backend/` Ordner liegt
→ Import-Pfade in `server.py` korrekt?

### "Keine Actions werden gestartet"
→ Check Cooldown (60 Sek zwischen Actions)
→ Living State korrekt initialisiert?

### "Stats ändern sich nicht"
→ `apply_stat_changes()` wird aufgerufen?
→ `update_living_system()` mit `player_state` Parameter?

---

## 📝 Changelog

### v1.0 (2025-11-20) - Initial Release
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
- ✅ Test Script

---

## 👨‍💻 Entwickler-Info

**System Design:**
- State-based Actions
- Priority-driven Decision Making
- Time-based Behaviors
- Need-based Triggers
- Resource Management

**Performance:**
- Lightweight (keine DB-Abhängigkeit für Core)
- In-Memory State Management
- Async-ready (FastAPI)
- Skalierbar

**Code Quality:**
- Type Hints
- Docstrings
- Error Handling
- Modular Design

---

## 🎉 Fertig!

Das **Najika Autonome Spielaktionen System** ist **vollständig implementiert** und **einsatzbereit**!

Najika kann jetzt:
- 🍳 Selbst kochen wenn hungrig
- 💤 Selbst schlafen wenn müde
- 🌱 Im Garten arbeiten
- 🗺️ Die Welt erkunden
- 🔨 Items craften
- 💜 Geschenke für Kuja machen
- 🎯 Smart entscheiden basierend auf Bedürfnissen
- 📍 Zwischen Locations teleportieren

**Zeit für Najika, in der Welt zu leben! ✨**

---

**Created by:** Kuja
**Date:** 2025-11-20
**Version:** 1.0
**Status:** ✅ Production Ready
