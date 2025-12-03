# Integration Guide - Optional Game Systems

## Quick Start (5 Minuten)

### Option A: Hybrid Server (Empfohlen)

```bash
# 1. Backend APIs kopieren
cp optional_systems/backend_apis/*.py backend/api/
cp optional_systems/database_models/*.py backend/models/

# 2. Database Models registrieren
# In backend/database.py oder backend/models/__init__.py:
from backend.models.card_game import Card, PlayerCardCollection, PlayerDeck
from backend.models.dice_monsters import DiceMonster, PlayerDiceCollection

# 3. Server auf FastAPI umstellen
# Siehe FASTAPI_MIGRATION.md

# 4. Seed-Daten laden
cd backend
python seed_card_games.py
```

---

## Detaillierte Schritte

### Schritt 1: Backend APIs kopieren

```bash
cd /path/to/Najika_World

# Kopiere FastAPI Routers
cp optional_systems/backend_apis/card_game.py backend/api/
cp optional_systems/backend_apis/dice_monsters.py backend/api/

# Kopiere Database Models
cp optional_systems/database_models/card_game.py backend/models/
cp optional_systems/database_models/dice_monsters.py backend/models/

# Kopiere Seed Scripts
cp optional_systems/seed_data/seed_card_games.py backend/
cp optional_systems/seed_data/seed_100_cards.py backend/
```

---

### Schritt 2: Dependencies installieren

```bash
pip install fastapi uvicorn sqlalchemy alembic
```

**Oder aus requirements.txt:**
```bash
pip install -r backend/requirements.txt
```

---

### Schritt 3: Server anpassen

**Option 3A: Neuer FastAPI Server (game_server.py)**

Erstelle `backend/game_server.py`:

```python
"""
Najika World - Game Server
FastAPI Server für Card Game und Dice Monsters
Port: 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import Game Routers
from backend.api.card_game import router as card_router
from backend.api.card_game import matches_router, decks_router, rankings_router
from backend.api.dice_monsters import router as dice_router
from backend.api.dice_monsters import duel_router

# Initialize FastAPI
app = FastAPI(
    title="Najika World Game API",
    description="Card Game & Dice Monsters System",
    version="1.0.0"
)

# CORS (allow frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(card_router)
app.include_router(matches_router)
app.include_router(decks_router)
app.include_router(rankings_router)
app.include_router(dice_router)
app.include_router(duel_router)

@app.get("/")
def root():
    return {
        "message": "Najika World Game API",
        "endpoints": {
            "cards": "/api/cards",
            "matches": "/api/matches",
            "decks": "/api/decks",
            "rankings": "/api/rankings",
            "dice": "/api/dice",
            "dice_duel": "/api/dice-duel"
        },
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("🎮 Starting Najika World Game Server on port 8001...")
    print("📚 API Docs: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Starten:**
```bash
python backend/game_server.py
```

**Frontend anpassen:**
```javascript
// In card_game_ui.js (Zeile 13-16)
this.apiBase = {
    cards: 'http://localhost:8001/api/cards',
    matches: 'http://localhost:8001/api/matches',
    decks: 'http://localhost:8001/api/decks',
    rankings: 'http://localhost:8001/api/rankings'
};

// In dice_monsters_ui.js (Zeile 13-16)
this.apiBase = {
    dice: 'http://localhost:8001/api/dice',
    duel: 'http://localhost:8001/api/dice-duel'
};
```

---

**Option 3B: Hybrid Server (FastAPI + Static Files)**

Erstelle `backend/hybrid_server.py`:

```python
"""
Najika World - Hybrid Server
FastAPI + Static File Serving
Port: 8000
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os

# Import ALL routers
from backend.api.card_game import router as card_router
from backend.api.card_game import matches_router, decks_router, rankings_router
from backend.api.dice_monsters import router as dice_router
from backend.api.dice_monsters import duel_router

# Your existing najika_server.py endpoints would go here too
# from backend.api.slime import router as slime_router
# from backend.api.pvp import router as pvp_router
# etc...

app = FastAPI(title="Najika World Complete API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register game routers
app.include_router(card_router)
app.include_router(matches_router)
app.include_router(decks_router)
app.include_router(rankings_router)
app.include_router(dice_router)
app.include_router(duel_router)

# Static files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/digivice", StaticFiles(directory=os.path.join(PROJECT_ROOT, "digivice")), name="digivice")
app.mount("/assets", StaticFiles(directory=os.path.join(PROJECT_ROOT, "digivice", "static", "assets")), name="assets")
app.mount("/config", StaticFiles(directory=os.path.join(PROJECT_ROOT, "digivice", "config")), name="config")

@app.get("/")
def root():
    return FileResponse(os.path.join(PROJECT_ROOT, "digivice", "index.html"))

if __name__ == "__main__":
    print("🌍 Starting Najika World Hybrid Server on port 8000...")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🎮 Frontend: http://localhost:8000/")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Starten:**
```bash
python backend/hybrid_server.py
```

---

### Schritt 4: Database initialisieren

**4.1 Database erstellen:**

```python
# backend/init_game_db.py
from sqlalchemy import create_engine
from backend.database import Base, engine
from backend.models.card_game import Card, PlayerCardCollection, PlayerDeck, CardGameMatch, CardGameRanking
from backend.models.dice_monsters import DiceMonster, PlayerDiceCollection, DiceDuel

print("Creating game database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created!")
```

```bash
python backend/init_game_db.py
```

**4.2 Seed-Daten laden:**

```bash
# 100 Karten erstellen
python backend/seed_card_games.py

# Oder mit Custom-Generator
python backend/seed_100_cards.py
```

---

### Schritt 5: Testen

**5.1 Server starten:**
```bash
# Option A: Game Server (Port 8001)
python backend/game_server.py

# Option B: Hybrid Server (Port 8000)
python backend/hybrid_server.py
```

**5.2 API Docs öffnen:**
```
http://localhost:8001/docs  (Option A)
http://localhost:8000/docs  (Option B)
```

**5.3 Test Requests:**

```bash
# Alle Karten abrufen
curl http://localhost:8001/api/cards

# Spieler Collection
curl http://localhost:8001/api/cards/collection/1

# Alle Würfel-Monster
curl http://localhost:8001/api/dice

# Health Check
curl http://localhost:8001/health
```

**5.4 Frontend testen:**

1. Öffne `http://localhost:8000`
2. Drücke `Tab` → Game Systems Menu
3. Klicke "Card Game" oder "Dice Monsters"
4. UI sollte öffnen und API-Calls machen

**Erwartete Console Logs:**
```
[Card Game] Fetching cards from API...
[Card Game] Loaded 100 cards
[Card Game] Loaded player collection: 0 cards
```

---

## Troubleshooting

### Problem: "404 Not Found" bei API Calls

**Lösung:** Server läuft nicht oder falscher Port

```bash
# Check if server is running
curl http://localhost:8001/health

# Check logs
python backend/game_server.py
# Should see: "🎮 Starting Najika World Game Server on port 8001..."
```

---

### Problem: "CORS Error" im Browser

**Lösung:** CORS Middleware fehlt

In `backend/game_server.py` oder `hybrid_server.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Frontend Port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Problem: "Table doesn't exist"

**Lösung:** Database nicht initialisiert

```bash
python backend/init_game_db.py
python backend/seed_card_games.py
```

---

### Problem: "Module not found: backend.api.card_game"

**Lösung:** APIs nicht kopiert

```bash
ls backend/api/card_game.py
ls backend/api/dice_monsters.py

# Wenn nicht vorhanden:
cp optional_systems/backend_apis/*.py backend/api/
```

---

## Verzeichnisstruktur nach Integration

```
Najika_World/
├── backend/
│   ├── api/
│   │   ├── card_game.py ✅ NEU
│   │   ├── dice_monsters.py ✅ NEU
│   │   └── ... (andere APIs)
│   ├── models/
│   │   ├── card_game.py ✅ NEU
│   │   ├── dice_monsters.py ✅ NEU
│   │   └── ... (andere Models)
│   ├── game_server.py ✅ NEU (Option A)
│   ├── hybrid_server.py ✅ NEU (Option B)
│   ├── seed_card_games.py ✅ NEU
│   └── najika_server.py (Original)
├── digivice/
│   ├── js/
│   │   ├── ui/
│   │   │   ├── card_game_ui.js ✅ Bereits vorhanden
│   │   │   ├── dice_monsters_ui.js ✅ Bereits vorhanden
│   │   │   └── game_systems_ui.js ✅ Bereits vorhanden
│   │   ├── 3d_dice_system.js ✅ Bereits vorhanden
│   │   ├── dungeon_generator.js ✅ Bereits vorhanden
│   │   ├── dungeon_enemies.js ✅ Bereits vorhanden
│   │   └── dungeon_combat.js ✅ Bereits vorhanden
│   └── index.html ✅ Bereits vorhanden (Scripts geladen)
└── optional_systems/ (kann nach Integration gelöscht werden)
```

---

## Start Scripts

**Für Game Server (Option A):**

Erstelle `START_GAME_SERVER.bat`:
```batch
@echo off
title Najika World - Game Server (Port 8001)
cd /d "%~dp0"
cd backend
python game_server.py
pause
```

**Für Hybrid Server (Option B):**

Erstelle `START_HYBRID_SERVER.bat`:
```batch
@echo off
title Najika World - Hybrid Server (Port 8000)
cd /d "%~dp0"
cd backend
python hybrid_server.py
pause
```

---

## Done!

Nach erfolgreicher Integration:
- ✅ Card Game funktioniert mit Datenpersistenz
- ✅ Dice Monsters funktioniert mit Datenpersistenz
- ✅ Dungeon System funktioniert (wie vorher)
- ✅ 3D Dice System funktioniert (wie vorher)
- ✅ Game Systems Menu öffnet alle UIs

**Frontend muss NICHT geändert werden** (außer API URLs wenn separate Server)!
