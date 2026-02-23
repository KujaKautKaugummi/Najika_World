# 🌾🎣 FARMING & FISHING SYSTEMS - QUICK START

**Date:** 2025-11-09 (Tag 2)
**Author:** Claude Code (CLI)
**API Port:** 5002
**Status:** ✅ COMPLETE & TESTED

---

## 🎯 OVERVIEW

Two new systems that make Najika's world more interactive:

1. **FARMING:** Plant, water, harvest crops (20 fields in Najika's home)
2. **FISHING:** Catch fish at various spots (5 spots across regions)

Both systems:
- Work in real-time (crops grow, fish respawn)
- Support AI auto-mode (Najika farms/fishes when hungry)
- Have complete REST APIs for Web/Mobile integration

---

## 🚀 STARTING THE API SERVER

### Option 1: Standalone Mode

```powershell
cd C:\Najika_World\backend
python najika_farm_fish_api.py
```

Server starts on: **http://localhost:5002**

### Option 2: Integration Mode

```python
# In your main najika_server.py:
from najika_farm_fish_api import farm_fish_api
app.register_blueprint(farm_fish_api)
```

Then all endpoints are available under your main server.

---

## 📋 API ENDPOINTS

### FARMING (9 Endpoints)

```
GET  /api/farm/status         - Get all fields status
POST /api/farm/plant          - Plant a crop
POST /api/farm/water          - Water a field
POST /api/farm/fertilize      - Fertilize a field
POST /api/farm/harvest        - Harvest a crop
GET  /api/farm/crops          - Get all crop types
POST /api/farm/update         - Force update all fields
POST /api/farm/season         - Set season
POST /api/farm/weather        - Set weather
```

### FISHING (7 Endpoints)

```
GET  /api/fish/status         - Get fishing status
POST /api/fish/start          - Start fishing
GET  /api/fish/spots          - Get all fishing spots
GET  /api/fish/types          - Get all fish types
POST /api/fish/update         - Force update spots (respawn)
POST /api/fish/time           - Set time of day
POST /api/fish/weather        - Set weather
```

### COMBINED (1 Endpoint)

```
GET  /api/farm_fish/stats     - Combined statistics
```

---

## 🌾 FARMING EXAMPLES

### 1. Get Farm Status

**Request:**
```bash
GET http://localhost:5002/api/farm/status
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "total_fields": 20,
    "planted_fields": 2,
    "harvestable_fields": 0,
    "empty_fields": 18,
    "growing_crops": [
      {
        "field_id": "farm_field_001",
        "crop_name": "Karotte",
        "stage": "growing",
        "progress": 75.5,
        "water_level": 45.0,
        "health": 90.0,
        "estimated_yield": 6,
        "ready": false
      }
    ],
    "season": "spring",
    "weather": "clear",
    "total_harvests": 15,
    "total_crops_planted": 30
  }
}
```

### 2. Plant a Crop

**Request:**
```bash
POST http://localhost:5002/api/farm/plant
Content-Type: application/json

{
  "field_id": "farm_field_001",
  "crop_type": "tomato",
  "planter": "player"
}
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "success": true,
    "message": "Tomate planted successfully!",
    "field_id": "farm_field_001",
    "crop_name": "Tomate",
    "harvest_time": 1762702058.66,
    "estimated_hours": 1.5
  }
}
```

### 3. Water a Field

**Request:**
```bash
POST http://localhost:5002/api/farm/water
Content-Type: application/json

{
  "field_id": "farm_field_001"
}
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "success": true,
    "message": "Field watered!",
    "water_level": 95.0,
    "health": 95.0
  }
}
```

### 4. Harvest a Crop

**Request:**
```bash
POST http://localhost:5002/api/farm/harvest
Content-Type: application/json

{
  "field_id": "farm_field_001"
}
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "success": true,
    "message": "Harvested 7x Tomate (good quality)!",
    "items": {
      "item_id": "tomato",
      "name": "Tomate",
      "quantity": 7,
      "quality": "good",
      "sell_price_each": 18,
      "total_value": 126
    },
    "bonuses": {
      "hunger_value": 140
    },
    "xp_gained": 35,
    "field_id": "farm_field_001"
  }
}
```

### 5. Get All Crop Types

**Request:**
```bash
GET http://localhost:5002/api/farm/crops
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "carrot": {
      "name": "Karotte",
      "type": "vegetable",
      "growth_time_hours": 1.0,
      "seasons": ["spring", "fall"],
      "sell_price": 10,
      "regions": ["all"]
    },
    "tomato": {
      "name": "Tomate",
      "type": "vegetable",
      "growth_time_hours": 1.5,
      "seasons": ["spring", "summer"],
      "sell_price": 15,
      "regions": ["all"]
    },
    "fire_pepper": {
      "name": "Feuerpfeffer",
      "type": "special",
      "growth_time_hours": 4.0,
      "seasons": ["summer"],
      "sell_price": 100,
      "regions": ["Magmaströme", "Heiße Dünen"]
    }
  }
}
```

### 6. Set Season

**Request:**
```bash
POST http://localhost:5002/api/farm/season
Content-Type: application/json

{
  "season": "summer"
}
```

**Response:**
```json
{
  "status": "ok",
  "message": "Season set to summer"
}
```

---

## 🎣 FISHING EXAMPLES

### 1. Get Fishing Status

**Request:**
```bash
GET http://localhost:5002/api/fish/status
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "player_stats": {
      "fishing_skill": 3,
      "total_caught": 47,
      "total_attempts": 85,
      "legendary_count": 2,
      "biggest_catch": {
        "type": "golden_trout",
        "name": "Goldforelle",
        "size": 58
      }
    },
    "spots": [
      {
        "spot_id": "home_pond",
        "name": "Heim-Teich",
        "region": "Samtmoos-Tiefwald",
        "type": "freshwater",
        "current_fish": 15,
        "max_fish": 20,
        "respawn_time": 1800,
        "quality": 0.7,
        "public": false
      }
    ],
    "time_of_day": "day",
    "weather": "clear"
  }
}
```

### 2. Start Fishing

**Request:**
```bash
POST http://localhost:5002/api/fish/start
Content-Type: application/json

{
  "spot_id": "home_pond",
  "player_skill": 5,
  "rod_quality": 1.5
}
```

**Response (Success):**
```json
{
  "status": "ok",
  "data": {
    "success": true,
    "caught": true,
    "fish": {
      "type": "golden_trout",
      "name": "Goldforelle",
      "rarity": "rare",
      "size": 52,
      "sell_price": 200,
      "hunger_value": 50,
      "energy_bonus": 0,
      "special_effect": null
    },
    "xp_gained": 190,
    "skill_up": true,
    "message": "You caught a 52cm Goldforelle!",
    "catch_chance": 45.5,
    "roll": 23.8,
    "chance_breakdown": {
      "base": 5.0,
      "skill": 10.0,
      "rod": 5.0,
      "spot": 7.0,
      "time": 20.0,
      "weather": 0
    }
  }
}
```

**Response (Failed):**
```json
{
  "status": "ok",
  "data": {
    "success": true,
    "caught": false,
    "message": "The fish got away!",
    "xp_gained": 1,
    "catch_chance": 12.0,
    "roll": 71.5,
    "chance_breakdown": {
      "base": 15.0,
      "skill": 10.0,
      "rod": 0.0,
      "spot": 7.0,
      "time": -20.0,
      "weather": 0
    }
  }
}
```

### 3. Get All Fishing Spots

**Request:**
```bash
GET http://localhost:5002/api/fish/spots
```

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "spot_id": "home_pond",
      "name": "Heim-Teich",
      "region": "Samtmoos-Tiefwald",
      "type": "freshwater",
      "current_fish": 19,
      "max_fish": 20,
      "respawn_time": 1800,
      "quality": 0.7,
      "public": false
    },
    {
      "spot_id": "lava_lake",
      "name": "Lavasee",
      "region": "Magmaströme",
      "type": "lava",
      "current_fish": 1,
      "max_fish": 1,
      "respawn_time": 86400,
      "quality": 1.0,
      "public": true
    }
  ]
}
```

### 4. Get All Fish Types

**Request:**
```bash
GET http://localhost:5002/api/fish/types
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "small_fish": {
      "name": "Kleinfisch",
      "rarity": "common",
      "catch_chance": 50.0,
      "regions": ["all"],
      "sell_price": 5,
      "size_range": [5, 15]
    },
    "lava_eel": {
      "name": "Lava-Aal",
      "rarity": "legendary",
      "catch_chance": 1.0,
      "regions": ["Magmaströme"],
      "sell_price": 1000,
      "size_range": [100, 200]
    }
  }
}
```

### 5. Set Time of Day

**Request:**
```bash
POST http://localhost:5002/api/fish/time
Content-Type: application/json

{
  "time_of_day": "night"
}
```

**Response:**
```json
{
  "status": "ok",
  "message": "Time set to night"
}
```

---

## 📊 COMBINED STATS

**Request:**
```bash
GET http://localhost:5002/api/farm_fish/stats
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "farming": {
      "total_fields": 20,
      "planted_fields": 5,
      "harvestable_fields": 2,
      "total_harvests": 25,
      "season": "spring",
      "weather": "clear"
    },
    "fishing": {
      "fishing_skill": 8,
      "total_caught": 103,
      "total_attempts": 187,
      "legendary_count": 3,
      "biggest_catch": {
        "type": "lava_eel",
        "name": "Lava-Aal",
        "size": 185
      },
      "available_spots": 5,
      "time_of_day": "day",
      "weather": "clear"
    }
  }
}
```

---

## 💻 JAVASCRIPT INTEGRATION

### Farming Example

```javascript
// Plant a crop
async function plantCrop(fieldId, cropType) {
  const response = await fetch('http://localhost:5002/api/farm/plant', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      field_id: fieldId,
      crop_type: cropType,
      planter: 'player'
    })
  });

  const result = await response.json();
  if (result.status === 'ok') {
    console.log(result.data.message);
    // Update UI with harvest time
    return result.data;
  }
}

// Get farm status and update UI
async function updateFarmUI() {
  const response = await fetch('http://localhost:5002/api/farm/status');
  const result = await response.json();

  const farmData = result.data;

  // Update field indicators
  farmData.growing_crops.forEach(crop => {
    const fieldEl = document.getElementById(crop.field_id);
    fieldEl.classList.add('planted');
    fieldEl.dataset.crop = crop.crop_name;
    fieldEl.dataset.progress = crop.progress;

    // Change visual based on stage
    if (crop.stage === 'harvestable') {
      fieldEl.classList.add('ready');
    }

    // Show water level warning
    if (crop.water_level < 30) {
      fieldEl.classList.add('needs-water');
    }
  });
}

// Water a field
async function waterField(fieldId) {
  const response = await fetch('http://localhost:5002/api/farm/water', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ field_id: fieldId })
  });

  const result = await response.json();
  if (result.status === 'ok') {
    console.log('Field watered!');
    updateFarmUI();  // Refresh UI
  }
}

// Harvest a crop
async function harvestCrop(fieldId) {
  const response = await fetch('http://localhost:5002/api/farm/harvest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ field_id: fieldId })
  });

  const result = await response.json();
  if (result.status === 'ok') {
    const data = result.data;
    console.log(`Harvested ${data.items.quantity}x ${data.items.name}!`);
    console.log(`Gained ${data.xp_gained} XP`);

    // Add items to inventory
    addToInventory(data.items);

    // Update UI
    updateFarmUI();
  }
}

// Auto-update every 10 seconds
setInterval(updateFarmUI, 10000);
```

### Fishing Example

```javascript
// Start fishing
async function startFishing(spotId, skill = 5, rodQuality = 1.0) {
  const response = await fetch('http://localhost:5002/api/fish/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      spot_id: spotId,
      player_skill: skill,
      rod_quality: rodQuality
    })
  });

  const result = await response.json();
  const data = result.data;

  if (data.caught) {
    // SUCCESS!
    const fish = data.fish;
    console.log(`🎣 Caught ${fish.name} (${fish.size}cm)!`);
    console.log(`Rarity: ${fish.rarity}`);
    console.log(`+${data.xp_gained} XP`);

    if (data.skill_up) {
      console.log('🎉 Fishing skill increased!');
    }

    // Add to inventory
    addFishToInventory(fish);

    // Show animation
    showFishCaughtAnimation(fish);

    return fish;
  } else {
    // MISSED
    console.log('😢 The fish got away!');
    console.log(`Catch chance was ${data.catch_chance.toFixed(1)}%`);
    console.log(`Roll was ${data.roll.toFixed(1)}`);

    // Show miss animation
    showFishMissAnimation();

    return null;
  }
}

// Get fishing spots and display on map
async function displayFishingSpots() {
  const response = await fetch('http://localhost:5002/api/fish/spots');
  const result = await response.json();

  result.data.forEach(spot => {
    // Create marker on map
    const marker = createMapMarker(spot.name, spot.position);

    // Color by fish availability
    if (spot.current_fish === 0) {
      marker.classList.add('depleted');
    } else if (spot.current_fish < spot.max_fish * 0.3) {
      marker.classList.add('low');
    }

    // Add click handler
    marker.onclick = () => startFishing(spot.spot_id);
  });
}

// Get all fish types for fishing guide
async function createFishingGuide() {
  const response = await fetch('http://localhost:5002/api/fish/types');
  const result = await response.json();

  const fishTypes = result.data;

  for (const [fishId, fish] of Object.entries(fishTypes)) {
    const entry = document.createElement('div');
    entry.className = `fish-entry rarity-${fish.rarity}`;
    entry.innerHTML = `
      <h3>${fish.name}</h3>
      <p>Rarity: ${fish.rarity}</p>
      <p>Catch Chance: ${fish.catch_chance}%</p>
      <p>Price: ${fish.sell_price} gold</p>
      <p>Size: ${fish.size_range[0]}-${fish.size_range[1]}cm</p>
    `;
    document.getElementById('fishing-guide').appendChild(entry);
  }
}
```

---

## 🐍 PYTHON TESTING SCRIPT

```python
import requests
import json

API_BASE = "http://localhost:5002/api"

def test_farming():
    print("=== TESTING FARMING ===")

    # Get status
    r = requests.get(f"{API_BASE}/farm/status")
    print(f"Farm Status: {r.json()}")

    # Plant a crop
    r = requests.post(f"{API_BASE}/farm/plant", json={
        "field_id": "farm_field_005",
        "crop_type": "carrot"
    })
    print(f"Plant Result: {r.json()}")

    # Water it
    r = requests.post(f"{API_BASE}/farm/water", json={
        "field_id": "farm_field_005"
    })
    print(f"Water Result: {r.json()}")

def test_fishing():
    print("\n=== TESTING FISHING ===")

    # Get status
    r = requests.get(f"{API_BASE}/fish/status")
    print(f"Fish Status: {r.json()}")

    # Try fishing
    r = requests.post(f"{API_BASE}/fish/start", json={
        "spot_id": "home_pond",
        "player_skill": 10
    })
    result = r.json()
    print(f"Fishing Result: {result}")

    if result['data']['caught']:
        fish = result['data']['fish']
        print(f"CAUGHT: {fish['name']} ({fish['size']}cm)!")
    else:
        print("Missed the fish!")

def test_combined_stats():
    print("\n=== TESTING COMBINED STATS ===")

    r = requests.get(f"{API_BASE}/farm_fish/stats")
    stats = r.json()['data']

    print(f"Farming: {stats['farming']}")
    print(f"Fishing: {stats['fishing']}")

if __name__ == "__main__":
    test_farming()
    test_fishing()
    test_combined_stats()
```

---

## 📝 CROP TYPES REFERENCE

| Crop | Type | Growth Time | Seasons | Sell Price | Regions |
|------|------|-------------|---------|------------|---------|
| Karotte | Vegetable | 1h | Spring, Fall | 10 | All |
| Tomate | Vegetable | 1.5h | Spring, Summer | 15 | All |
| Kartoffel | Vegetable | 1.25h | Spring, Summer, Fall | 8 | All |
| Erdbeere | Fruit | 2h | Spring, Summer | 25 | Forest, Coast |
| Apfel | Fruit | 2.5h | Summer, Fall | 30 | Forest |
| Weizen | Grain | 3h | Spring, Summer, Fall | 5 | Plains, Forest |
| Mais | Grain | 3.5h | Summer | 7 | Plains |
| Feuerpfeffer | Special | 4h | Summer | 100 | Magmaströme, Heiße Dünen |
| Eisbeere | Special | 4h | Winter | 100 | Reich der Drei |
| Magischer Pilz | Special | 5h | Spring, Fall | 250 | Forest, Swamp |

---

## 🐟 FISH TYPES REFERENCE

| Fish | Rarity | Catch % | Regions | Price | Time/Weather |
|------|--------|---------|---------|-------|--------------|
| Kleinfisch | Common | 50% | All | 5 | Any |
| Karpfen | Common | 35% | Forest, Coast | 15 | Day |
| Forelle | Uncommon | 25% | Forest | 40 | Day/Dawn/Dusk |
| Lachs | Uncommon | 20% | Coast | 50 | Day + Rain |
| Thunfisch | Rare | 8% | Coast | 150 | Day |
| Goldforelle | Rare | 5% | Forest | 200 | Dawn/Dusk + Clear |
| Lava-Aal | Legendary | 1% | Magmaströme | 1000 | Night + Clear + Flame Rod |
| Eisschlange | Legendary | 1% | Reich der Drei | 1000 | Night + Snow + Frost Rod |
| Sumpfmonster | Legendary | 0.5% | Grünschlamm-Sumpf | 1500 | Night + Rain/Storm |
| Alter Stiefel | Trash | 15% | All | 1 | Any |
| Algen | Trash | 10% | All | 2 | Any |

---

## 🔧 TROUBLESHOOTING

### Server won't start

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Fix:**
```bash
pip install flask flask-cors
```

### Can't connect to API

**Check:**
1. Server running? `netstat -ano | findstr :5002`
2. Firewall blocking? Allow Python in Windows Defender
3. Correct URL? `http://localhost:5002` (not 8000!)

### Crops not growing

**Causes:**
- Water level too low (< 20%)
- Health damaged
- Wrong season for crop

**Fix:**
```bash
POST /api/farm/water
# Or change season:
POST /api/farm/season
{"season": "summer"}
```

### No fish at spot

**Causes:**
- Spot depleted (respawn needed)
- Wrong time of day
- Wrong weather

**Check:**
```bash
GET /api/fish/spots
# Look at "current_fish" count
```

**Fix:**
```bash
# Wait for respawn, OR force update:
POST /api/fish/update

# Change time:
POST /api/fish/time
{"time_of_day": "night"}
```

---

## 🎮 GAME BALANCE

### Farming
- **Fast crops:** 1-2h → Good for quick food
- **Medium crops:** 2-4h → Better value
- **Slow crops:** 4-5h → Best value + special effects

### Fishing
- **Skill matters:** +2% catch chance per level
- **Rod quality:** Better rod = bigger fish + higher chance
- **Time & Weather:** CRITICAL for rare/legendary fish
- **Spot quality:** Better spots = bigger fish

---

## 🚀 NEXT STEPS (Tag 3)

Tomorrow we'll add:

1. **Cooking System** - Use crops + fish to cook meals
2. **Crafting System** - Create tools, rods, fertilizer
3. **Inventory System** - Store harvested items
4. **Market System** - Buy/sell items

---

**Created:** 2025-11-09 (Tag 2)
**Tested:** ✅ All endpoints working
**Ready for:** Web/Mobile integration

---

*Happy Farming & Fishing! 🌾🎣*
