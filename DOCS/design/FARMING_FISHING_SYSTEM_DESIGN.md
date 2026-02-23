# 🌾 FARMING & FISHING SYSTEM - COMPLETE DESIGN

**Datum:** 9. November 2025 (Tag 2)
**Autor:** Claude Code (CLI)
**Status:** In Entwicklung

---

## 🎯 ÜBERBLICK

### Was ist das?

Zwei zusammenhängende Systeme die Najika's Welt lebendiger machen:

1. **Farming System:** Pflanzen anbauen, pflegen, ernten
2. **Fishing System:** Fische fangen an verschiedenen Spots

### Wo wird es genutzt?

- ✅ **Najika's Lebensraum (V2):** Kleine Farm (max 20 Felder)
- ✅ **Großes Mobile Game:** Große Farmen, kommerzielle Fischerei
- ✅ **Social Hub:** Gemeinsam fischen

---

## 🌾 FARMING SYSTEM

### 1. CROP TYPES (Pflanzen-Typen)

```python
CROPS = {
    # GEMÜSE (kurze Wachstumszeit)
    "carrot": {
        "name": "Karotte",
        "type": "vegetable",
        "growth_time": 3600,      # 1 Stunde (real-time)
        "water_need": "medium",    # low/medium/high
        "seasons": ["spring", "fall"],
        "yield_min": 3,
        "yield_max": 8,
        "sell_price": 10,
        "hunger_value": 15,
        "regions": ["all"]         # In allen Regionen anbaubar
    },

    "tomato": {
        "name": "Tomate",
        "type": "vegetable",
        "growth_time": 5400,      # 1.5 Stunden
        "water_need": "high",
        "seasons": ["spring", "summer"],
        "yield_min": 4,
        "yield_max": 10,
        "sell_price": 15,
        "hunger_value": 20,
        "regions": ["all"]
    },

    # FRÜCHTE (mittlere Wachstumszeit)
    "strawberry": {
        "name": "Erdbeere",
        "type": "fruit",
        "growth_time": 7200,      # 2 Stunden
        "water_need": "medium",
        "seasons": ["spring", "summer"],
        "yield_min": 5,
        "yield_max": 15,
        "sell_price": 25,
        "hunger_value": 25,
        "energy_bonus": 5,
        "regions": ["Samtmoos-Tiefwald", "Salzwind-Küste"]
    },

    # GETREIDE (lange Wachstumszeit, hoher Ertrag)
    "wheat": {
        "name": "Weizen",
        "type": "grain",
        "growth_time": 10800,     # 3 Stunden
        "water_need": "low",
        "seasons": ["spring", "summer", "fall"],
        "yield_min": 10,
        "yield_max": 25,
        "sell_price": 5,           # Niedriger Einzelpreis
        "crafting_ingredient": True,  # Für Brot etc.
        "regions": ["Blitzebene", "Samtmoos-Tiefwald"]
    },

    # SPEZIAL-PFLANZEN (region-spezifisch)
    "fire_pepper": {
        "name": "Feuerpfeffer",
        "type": "special",
        "growth_time": 14400,     # 4 Stunden
        "water_need": "low",
        "temperature_need": "hot",
        "seasons": ["summer"],
        "yield_min": 2,
        "yield_max": 5,
        "sell_price": 100,
        "special_effect": "fire_resistance",
        "regions": ["Magmaströme", "Heiße Dünen"]  # Nur heiße Regionen!
    },

    "ice_berry": {
        "name": "Eisbeere",
        "type": "special",
        "growth_time": 14400,
        "water_need": "low",
        "temperature_need": "cold",
        "seasons": ["winter"],
        "yield_min": 2,
        "yield_max": 5,
        "sell_price": 100,
        "special_effect": "cold_resistance",
        "regions": ["Reich der Drei"]  # Nur Eis-Region!
    }
}
```

### 2. GROWTH STAGES (Wachstumsphasen)

Jede Pflanze durchläuft 4 Phasen:

```python
GROWTH_STAGES = {
    "planted": {
        "duration_percent": 0,      # 0% der Gesamtzeit
        "visual": "soil_with_seed",
        "description": "Gerade eingepflanzt"
    },
    "sprouting": {
        "duration_percent": 25,     # Nach 25% der Zeit
        "visual": "small_sprout",
        "description": "Keimt gerade"
    },
    "growing": {
        "duration_percent": 60,     # Nach 60% der Zeit
        "visual": "medium_plant",
        "description": "Wächst kräftig"
    },
    "harvestable": {
        "duration_percent": 100,    # Nach 100% der Zeit
        "visual": "full_grown",
        "description": "Bereit zur Ernte!",
        "harvestable": True
    }
}
```

### 3. FIELD STATE (Feld-Status)

```python
FIELD_STATE = {
    "field_id": "farm_field_001",
    "position": {"x": 100, "z": 200},
    "owner": "najika_ai",              # "najika_ai" oder "player"

    # Aktueller Zustand
    "crop_type": "tomato",             # Welche Pflanze?
    "planted_at": 1699545600,          # Unix-Timestamp
    "current_stage": "growing",
    "progress_percent": 75.5,          # 0-100%

    # Pflege-Status
    "water_level": 45.0,               # 0-100%
    "soil_quality": 80.0,              # 0-100%
    "health": 90.0,                    # 0-100% (Krankheit/Schädlinge)

    # Umwelt
    "last_watered": 1699548000,
    "weather_affected": False,
    "fertilized": False,

    # Ernte
    "ready_to_harvest": False,
    "estimated_yield": 6,              # Voraussichtlicher Ertrag
    "actual_yield": None               # Nach Ernte gefüllt
}
```

### 4. FARMING MECHANICS

#### A) Pflanzen (Planting)

```python
def plant_crop(field, crop_type, planter="player"):
    """Pflanze einen Samen"""

    # Check ob Feld leer
    if field["crop_type"] is not None:
        return {"success": False, "error": "Feld ist bereits bepflanzt"}

    # Check ob Jahreszeit passt
    crop = CROPS[crop_type]
    current_season = get_current_season()
    if current_season not in crop["seasons"]:
        return {"success": False, "error": f"{crop['name']} kann nicht im {current_season} angepflanzt werden"}

    # Check ob Region passt (für Spezial-Pflanzen)
    if "regions" in crop and crop["regions"] != ["all"]:
        field_region = get_region_from_position(field["position"])
        if field_region not in crop["regions"]:
            return {"success": False, "error": f"{crop['name']} wächst nicht in {field_region}"}

    # Pflanze!
    field["crop_type"] = crop_type
    field["planted_at"] = time.time()
    field["current_stage"] = "planted"
    field["progress_percent"] = 0
    field["owner"] = planter
    field["water_level"] = 100.0  # Frisch gepflanzt = gut gewässert

    return {
        "success": True,
        "message": f"{crop['name']} gepflanzt!",
        "harvest_time": time.time() + crop["growth_time"]
    }
```

#### B) Wachstum (Growth)

```python
def update_crop_growth(field):
    """Update Wachstum über Zeit"""

    if field["crop_type"] is None:
        return  # Leeres Feld

    crop = CROPS[field["crop_type"]]
    elapsed = time.time() - field["planted_at"]

    # Basis-Fortschritt
    base_progress = (elapsed / crop["growth_time"]) * 100

    # Modifikatoren
    water_modifier = field["water_level"] / 100.0  # 0.0 - 1.0
    soil_modifier = field["soil_quality"] / 100.0
    health_modifier = field["health"] / 100.0

    # Finale Wachstumsrate
    growth_rate = (water_modifier + soil_modifier + health_modifier) / 3.0

    # Wasser sinkt über Zeit
    hours_since_water = (time.time() - field["last_watered"]) / 3600.0
    field["water_level"] -= hours_since_water * 15.0  # -15% pro Stunde
    field["water_level"] = max(0, field["water_level"])

    # Bei zu wenig Wasser: Gesundheit sinkt
    if field["water_level"] < 20:
        field["health"] -= hours_since_water * 5.0
        field["health"] = max(0, field["health"])

    # Progress berechnen
    field["progress_percent"] = min(100, base_progress * growth_rate)

    # Stage bestimmen
    if field["progress_percent"] >= 100:
        field["current_stage"] = "harvestable"
        field["ready_to_harvest"] = True
    elif field["progress_percent"] >= 60:
        field["current_stage"] = "growing"
    elif field["progress_percent"] >= 25:
        field["current_stage"] = "sprouting"

    # Ertrag schätzen (basierend auf Pflege-Qualität)
    care_quality = (water_modifier + soil_modifier + health_modifier) / 3.0
    field["estimated_yield"] = int(
        crop["yield_min"] + (crop["yield_max"] - crop["yield_min"]) * care_quality
    )

    return field
```

#### C) Bewässern (Watering)

```python
def water_field(field):
    """Feld bewässern"""

    if field["crop_type"] is None:
        return {"success": False, "error": "Leeres Feld kann nicht bewässert werden"}

    # Wasser auffüllen
    old_level = field["water_level"]
    field["water_level"] = min(100.0, field["water_level"] + 50.0)
    field["last_watered"] = time.time()

    # Gesundheit verbessert sich leicht
    if old_level < 30:
        field["health"] = min(100.0, field["health"] + 10.0)

    return {
        "success": True,
        "message": "Feld bewässert!",
        "water_level": field["water_level"]
    }
```

#### D) Ernten (Harvesting)

```python
def harvest_crop(field):
    """Ernte die Pflanze"""

    if not field["ready_to_harvest"]:
        return {"success": False, "error": "Noch nicht erntereif!"}

    crop = CROPS[field["crop_type"]]

    # Finale Ertrag-Berechnung
    care_quality = (field["water_level"] + field["soil_quality"] + field["health"]) / 300.0
    actual_yield = int(
        crop["yield_min"] + (crop["yield_max"] - crop["yield_min"]) * care_quality
    )

    # Boden-Qualität sinkt nach Ernte
    field["soil_quality"] -= 15.0
    field["soil_quality"] = max(20.0, field["soil_quality"])

    # Items erstellen
    harvested_items = {
        "item_id": field["crop_type"],
        "quantity": actual_yield,
        "quality": "normal" if care_quality > 0.7 else "poor"
    }

    # Feld zurücksetzen
    crop_name = crop["name"]
    field["crop_type"] = None
    field["current_stage"] = None
    field["progress_percent"] = 0
    field["ready_to_harvest"] = False
    field["actual_yield"] = actual_yield

    return {
        "success": True,
        "message": f"{actual_yield}x {crop_name} geerntet!",
        "items": harvested_items,
        "xp_gained": actual_yield * 5
    }
```

---

## 🎣 FISHING SYSTEM

### 1. FISH TYPES (Fisch-Arten)

```python
FISH_TYPES = {
    # COMMON (überall)
    "small_fish": {
        "name": "Kleinfisch",
        "rarity": "common",
        "catch_chance": 50.0,      # 50% Basis-Chance
        "regions": ["all"],
        "time_of_day": ["day", "night"],
        "sell_price": 5,
        "hunger_value": 10,
        "size_min": 5,
        "size_max": 15
    },

    "carp": {
        "name": "Karpfen",
        "rarity": "common",
        "catch_chance": 35.0,
        "regions": ["Samtmoos-Tiefwald", "Salzwind-Küste"],
        "time_of_day": ["day"],
        "sell_price": 15,
        "hunger_value": 20,
        "size_min": 20,
        "size_max": 50
    },

    # UNCOMMON
    "salmon": {
        "name": "Lachs",
        "rarity": "uncommon",
        "catch_chance": 20.0,
        "regions": ["Salzwind-Küste"],
        "time_of_day": ["day"],
        "weather": ["rain"],       # Nur bei Regen!
        "sell_price": 50,
        "hunger_value": 35,
        "energy_bonus": 10,
        "size_min": 40,
        "size_max": 80
    },

    # RARE
    "golden_trout": {
        "name": "Goldforelle",
        "rarity": "rare",
        "catch_chance": 5.0,
        "regions": ["Samtmoos-Tiefwald"],
        "time_of_day": ["dawn", "dusk"],  # Nur Morgen/Abenddämmerung
        "sell_price": 200,
        "hunger_value": 50,
        "luck_bonus": 5,
        "size_min": 30,
        "size_max": 60
    },

    # LEGENDARY (region-spezifisch)
    "lava_eel": {
        "name": "Lava-Aal",
        "rarity": "legendary",
        "catch_chance": 1.0,       # Nur 1%!
        "regions": ["Magmaströme"],
        "time_of_day": ["night"],
        "weather": ["clear"],
        "special_rod_required": "flame_rod",
        "sell_price": 1000,
        "hunger_value": 100,
        "special_effect": "fire_resistance_permanent",
        "size_min": 100,
        "size_max": 200
    },

    "ice_serpent": {
        "name": "Eisschlange",
        "rarity": "legendary",
        "catch_chance": 1.0,
        "regions": ["Reich der Drei"],
        "time_of_day": ["night"],
        "weather": ["snow"],
        "special_rod_required": "frost_rod",
        "sell_price": 1000,
        "hunger_value": 100,
        "special_effect": "cold_resistance_permanent",
        "size_min": 100,
        "size_max": 200
    },

    # TRASH (Müll - kann auch gefangen werden)
    "old_boot": {
        "name": "Alter Stiefel",
        "rarity": "trash",
        "catch_chance": 15.0,
        "regions": ["all"],
        "sell_price": 1,
        "recyclable": True
    }
}
```

### 2. FISHING SPOTS

```python
FISHING_SPOTS = {
    # Najika's Lebensraum (V2)
    "home_pond": {
        "spot_id": "home_pond",
        "name": "Heim-Teich",
        "position": {"x": -500, "z": -500},
        "region": "Samtmoos-Tiefwald",
        "type": "freshwater",
        "fish_pool": ["small_fish", "carp", "golden_trout"],  # Welche Fische hier?
        "quality": 0.7,            # 0.0-1.0 (beeinflusst Größe/Qualität)
        "respawn_time": 1800,      # 30 Min bis neue Fische spawnen
        "max_fish": 20,
        "current_fish": 20
    },

    # Große Welt
    "ocean_shore": {
        "spot_id": "ocean_shore_01",
        "name": "Meeresküste",
        "position": {"x": 3800, "z": 200},
        "region": "Salzwind-Küste",
        "type": "saltwater",
        "fish_pool": ["small_fish", "carp", "salmon"],
        "quality": 0.85,
        "respawn_time": 3600,      # 1 Stunde
        "max_fish": 50,
        "current_fish": 50,
        "public": True             # Mehrere Spieler können hier fischen
    },

    "lava_lake": {
        "spot_id": "lava_lake_01",
        "name": "Lavasee",
        "position": {"x": 2800, "z": 2800},
        "region": "Magmaströme",
        "type": "lava",
        "fish_pool": ["lava_eel"],  # Nur Lava-Aal!
        "quality": 1.0,
        "respawn_time": 86400,     # 24 Stunden (sehr selten!)
        "max_fish": 1,
        "current_fish": 1,
        "danger_level": "extreme",
        "special_equipment_required": "flame_rod"
    }
}
```

### 3. FISHING MECHANICS

#### A) Angeln starten (Start Fishing)

```python
def start_fishing(spot_id, player_skill=1, rod_quality=1.0):
    """Starte Angel-Aktion"""

    spot = FISHING_SPOTS[spot_id]

    # Check ob Fische verfügbar
    if spot["current_fish"] <= 0:
        return {
            "success": False,
            "error": "Keine Fische verfügbar! Komm später wieder."
        }

    # Wähle zufälligen Fisch aus Pool
    fish_type = random.choice(spot["fish_pool"])
    fish = FISH_TYPES[fish_type]

    # Catch-Chance berechnen
    base_chance = fish["catch_chance"]
    skill_bonus = player_skill * 2.0      # +2% pro Skill-Level
    rod_bonus = (rod_quality - 1.0) * 10  # Bessere Angel = höhere Chance
    spot_bonus = spot["quality"] * 10

    # Zeit-Bonus (manche Fische nur zu bestimmten Zeiten)
    current_time = get_time_of_day()  # "day", "night", "dawn", "dusk"
    time_bonus = 20.0 if current_time in fish["time_of_day"] else -20.0

    # Wetter-Bonus
    weather_bonus = 0
    if "weather" in fish:
        current_weather = get_current_weather()
        weather_bonus = 30.0 if current_weather in fish["weather"] else -50.0

    # Finale Chance
    final_chance = base_chance + skill_bonus + rod_bonus + spot_bonus + time_bonus + weather_bonus
    final_chance = max(1.0, min(95.0, final_chance))  # Zwischen 1% und 95%

    # Würfeln!
    success = random.random() * 100 < final_chance

    if success:
        # GEFANGEN!
        spot["current_fish"] -= 1

        # Größe berechnen
        size = random.randint(fish["size_min"], fish["size_max"])
        quality_modifier = spot["quality"] * rod_quality
        size = int(size * (0.8 + quality_modifier * 0.4))  # Größere Fische mit besserer Ausrüstung

        return {
            "success": True,
            "caught": True,
            "fish": {
                "type": fish_type,
                "name": fish["name"],
                "rarity": fish["rarity"],
                "size": size,
                "sell_price": fish["sell_price"],
                "hunger_value": fish.get("hunger_value", 0)
            },
            "xp_gained": int(fish["catch_chance"] * 2),  # Seltene Fische = mehr XP
            "message": f"Du hast einen {size}cm {fish['name']} gefangen!"
        }
    else:
        # NICHT GEFANGEN
        return {
            "success": True,
            "caught": False,
            "message": "Der Fisch ist entkommen!",
            "xp_gained": 1  # Trotzdem 1 XP für Versuch
        }
```

#### B) Fishing Spot Respawn

```python
def update_fishing_spots():
    """Aktualisiere alle Fishing Spots (Fische spawnen nach)"""

    current_time = time.time()

    for spot_id, spot in FISHING_SPOTS.items():
        # Check ob genug Zeit vergangen
        if "last_respawn" not in spot:
            spot["last_respawn"] = current_time
            continue

        elapsed = current_time - spot["last_respawn"]

        if elapsed >= spot["respawn_time"]:
            # Fische spawnen nach!
            old_count = spot["current_fish"]
            spot["current_fish"] = spot["max_fish"]
            spot["last_respawn"] = current_time

            print(f"[INFO] {spot['name']}: {spot['max_fish'] - old_count} neue Fische gespawnt")
```

---

## 🔗 INTEGRATION MIT LIVING SYSTEM

### Najika fischt/farmt selbstständig (AI-Modus)

```python
def najika_auto_farm():
    """Najika kümmert sich selbst um ihre Farm (wenn Hunger < 30%)"""

    if LIVING_STATE["control_mode"] != "ai":
        return  # Spieler kontrolliert

    if LIVING_STATE["hunger"] < 30:
        # Najika erntet fertige Pflanzen
        for field in get_all_fields():
            if field["ready_to_harvest"]:
                result = harvest_crop(field)
                if result["success"]:
                    # Najika isst direkt
                    LIVING_STATE["hunger"] += result["items"]["quantity"] * 5
                    LIVING_STATE["mood_game"] += 5
                    print(f"[AI] Najika hat {result['message']} geerntet und gegessen")

        # Najika pflanzt neue Pflanzen (wenn unter 20% Hunger)
        if LIVING_STATE["hunger"] < 20:
            for field in get_all_fields():
                if field["crop_type"] is None:
                    # Pflanze schnell wachsende Karotten
                    plant_crop(field, "carrot", planter="najika_ai")
                    print("[AI] Najika hat Karotten gepflanzt")

def najika_auto_fish():
    """Najika fischt selbstständig (wenn Hunger < 25% und keine Farm-Ernte)"""

    if LIVING_STATE["control_mode"] != "ai":
        return

    if LIVING_STATE["hunger"] < 25 and LIVING_STATE["energy"] > 20:
        # Najika fischt am Heim-Teich
        result = start_fishing("home_pond", player_skill=LIVING_STATE.get("fishing_skill", 1))

        if result["caught"]:
            # Najika isst den Fisch
            fish = result["fish"]
            LIVING_STATE["hunger"] += fish["hunger_value"]
            LIVING_STATE["energy"] -= 5  # Angeln kostet Energie
            LIVING_STATE["mood_game"] += 10  # Macht gute Laune!
            print(f"[AI] Najika hat {fish['name']} gefangen und gegessen")
        else:
            LIVING_STATE["energy"] -= 3
            LIVING_STATE["anger_level"] += 2  # Frustriert wenn nichts gefangen
```

---

## 📊 DATABASE STRUCTURE

```python
# State-Files (JSON)

# farming_state.json
{
    "fields": [
        {
            "field_id": "farm_field_001",
            "position": {"x": 100, "z": 200},
            "crop_type": "tomato",
            "planted_at": 1699545600,
            "current_stage": "growing",
            "progress_percent": 75.5,
            "water_level": 45.0,
            "soil_quality": 80.0,
            "health": 90.0,
            # ...
        }
    ],
    "global_season": "spring",
    "global_weather": "clear",
    "last_update": 1699548000
}

# fishing_state.json
{
    "spots": {
        "home_pond": {
            "current_fish": 15,
            "last_respawn": 1699548000,
            # ...
        }
    },
    "player_stats": {
        "fishing_skill": 3,
        "total_caught": 47,
        "biggest_catch": {"type": "golden_trout", "size": 58}
    }
}
```

---

## 🎮 API ENDPOINTS (für Tag 2)

```python
# Farming
POST /api/farm/plant          # Pflanze Samen
POST /api/farm/water          # Bewässere Feld
POST /api/farm/harvest        # Ernte Pflanze
GET  /api/farm/status         # Status aller Felder
POST /api/farm/fertilize      # Dünge Feld (optional)

# Fishing
POST /api/fish/start          # Starte Angeln
GET  /api/fish/spots          # Alle verfügbaren Spots
GET  /api/fish/inventory      # Gefangene Fische
POST /api/fish/sell           # Verkaufe Fische

# Combined
GET  /api/farm_fish/stats     # Statistiken
POST /api/farm_fish/update    # Force-Update (für Testing)
```

---

## 🎯 BALANCE

### Farming
- **Schnelle Crops:** 1-2 Stunden (Karotten, Tomaten)
- **Mittlere Crops:** 2-4 Stunden (Früchte, Kräuter)
- **Langsame Crops:** 4-8 Stunden (Getreide, Spezial-Pflanzen)
- **Wasser:** Sinkt 15% pro Stunde → alle 3-4 Stunden gießen
- **Boden-Qualität:** Sinkt 15% pro Ernte → alle 5-6 Ernten düngen

### Fishing
- **Common Fish:** 35-50% Chance
- **Uncommon Fish:** 15-25% Chance
- **Rare Fish:** 3-8% Chance
- **Legendary Fish:** 0.5-2% Chance
- **Respawn:** 30 Min (Teich) bis 24h (Legendary Spots)

---

## 🚀 IMPLEMENTATION PLAN (Tag 2)

### Phase 1: Backend (jetzt)
1. ✅ Design-Dokument erstellen
2. ⏳ `backend/najika_farming_system.py` implementieren
3. ⏳ `backend/najika_fishing_system.py` implementieren
4. ⏳ `backend/najika_farm_fish_api.py` erstellen (API)
5. ⏳ Testing

### Phase 2: Web-Modelle (nachher)
1. **Web-Modell #1:** Farming UI (Felder anzeigen, Interaktion)
2. **Web-Modell #2:** Fishing UI (Fishing Spots, Angel-Minigame)

---

**Erstellt:** 2025-11-09 (Tag 2)
**Status:** Design abgeschlossen, Implementation startet
