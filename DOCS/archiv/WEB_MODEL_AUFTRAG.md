# 🤖 WEB MODEL - AUFTRAG
**Datum:** 2025-11-18 10:30
**Branch:** `claude/remote-access-setup-011CUt97k27tgaNUMZdyA9DY`
**Auftraggeber:** Kuja (via Local Claude)
**Status:** 🟡 AUFTRAG ERTEILT - WARTE AUF START

---

## 🎯 HAUPTAUFGABE

**Ziel:** Mache die FastAPI Backend-Migration **funktionsfähig** und **UE5-ready**.

Du hast bereits **80% der Code-Arbeit** gemacht (Flask→FastAPI, Models, Services). Jetzt musst du die **fehlenden 20% Setup + Integration** erledigen, damit:

1. ✅ Server startet ohne Errors
2. ✅ Database funktioniert (Persistence!)
3. ✅ Endpoints schreiben in Database (nicht in-memory!)
4. ✅ UE5 Mobile Game kann Backend nutzen

---

## 📋 DEINE TODO-LISTE (Priorität)

### 🔴 PHASE 1: KRITISCHE FIXES (45 Minuten)

**Status:** ⏳ MUSS SOFORT GEMACHT WERDEN

#### Task 1.1: Dependencies installieren
```bash
cd C:/Najika_World
pip install sqlalchemy alembic pydantic-settings python-jose bcrypt python-multipart
```

**Warum:** NICHTS funktioniert ohne diese Packages!
**Test:** `python -c "from backend.config import settings; print('✅ Config works')"`
**Zeit:** 5 Minuten

---

#### Task 1.2: database.py Model Imports fixen
**File:** `backend/database.py`
**Zeile:** 49

**VORHER:**
```python
def init_db() -> None:
    from backend.models import user, character, inventory, training
    Base.metadata.create_all(bind=engine)
```

**NACHHER:**
```python
def init_db() -> None:
    # Import ALL models so they are registered with Base
    from backend.models import (
        user, character, inventory, training,
        slime_companion, pvp_battle, arena_monster, magic_progress
    )
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")
```

**Warum:** Sonst werden 4 Tabellen NICHT erstellt!
**Test:** `python -c "from backend.database import init_db; init_db()"`
**Zeit:** 5 Minuten

---

#### Task 1.3: .env File erstellen
**File:** `.env` (NEU, im Root: `C:/Najika_World/.env`)

**Inhalt:**
```env
# Database
DATABASE_URL=sqlite:///./najika_world.db

# Security (WICHTIG: Ändere diese Keys!)
SECRET_KEY=najika-super-secret-key-change-this-in-production-minimum-32-characters
JWT_SECRET=najika-jwt-secret-key-change-this-in-production-minimum-32-characters

# App Settings
DEBUG=True
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# CORS (UE5 Mobile Game Zugriff)
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","*"]
```

**Warum:** config.py braucht diese Werte!
**Test:** `python -c "from backend.config import settings; print(f'Secret: {settings.SECRET_KEY[:10]}...')"`
**Zeit:** 5 Minuten

---

#### Task 1.4: Alembic Migrations erstellen
```bash
cd C:/Najika_World/backend

# Erste Migration erstellen (Alembic scannt Models automatisch)
alembic revision --autogenerate -m "Initial schema - all models"

# Migration anwenden (erstellt najika_world.db + Tabellen)
alembic upgrade head

# Check
ls alembic/versions/  # Sollte .py File enthalten
ls najika_world.db     # Sollte existieren
```

**Warum:** Database Schema muss existieren!
**Test:** `python -c "from backend.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"`
**Zeit:** 10 Minuten

---

#### Task 1.5: Server testen
```bash
cd C:/Najika_World
uvicorn backend.main:app --reload
```

**Erwartetes Output:**
```
======================================================================
🚀 Starting Najika World API v2.0.0
======================================================================
📊 Initializing database...
✅ Database initialized successfully
✅ Backend is ready!
📖 API Docs: http://0.0.0.0:8000/docs
📖 ReDoc: http://0.0.0.0:8000/redoc
======================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Test:**
1. Browser: `http://localhost:8000/docs` (Swagger UI)
2. Teste `/health` Endpoint
3. Teste `/api/v1/info` Endpoint

**Warum:** Sicherstellen dass Server läuft!
**Zeit:** 10 Minuten

---

### 🟡 PHASE 2: DATABASE INTEGRATION (2-3 Stunden)

**Status:** ⏳ NACH PHASE 1

**Problem:** Alle 16 API Endpoints nutzen noch **in-memory Services** statt Database!

**Beispiel (backend/api/slime.py):**

**VORHER (in-memory):**
```python
from backend.services.slime_system import SlimeSystem

slime_system = SlimeSystem()  # ❌ In-memory dict!

@router.post("/create")
async def create_companion(request: CreateCompanionRequest):
    companion = slime_system.create_companion(...)  # ❌ Geht verloren bei Restart!
    return companion
```

**NACHHER (database):**
```python
from backend.database import get_db
from backend.models.slime_companion import SlimeCompanion
from sqlalchemy.orm import Session
from fastapi import Depends

@router.post("/create")
async def create_companion(
    request: CreateCompanionRequest,
    db: Session = Depends(get_db)
):
    # ✅ Erstelle Model direkt
    companion = SlimeCompanion(
        owner_player_id=request.owner_player_id,
        name=request.name,
        level=1,
        experience=0,
        # ... alle Fields aus Model
    )

    # ✅ Speichere in Database
    db.add(companion)
    db.commit()
    db.refresh(companion)  # Lädt ID zurück

    return {
        "success": True,
        "companion_id": companion.id,
        "name": companion.name,
        "message": f"{companion.name} wurde erstellt!"
    }
```

**Betroffene Files (ALLE 16 API Files):**
1. `backend/api/slime.py` - 12 Endpoints
2. `backend/api/pvp.py` - ~8 Endpoints
3. `backend/api/oregon_events.py` - ~6 Endpoints
4. `backend/api/region_boss.py` - ~5 Endpoints
5. `backend/api/magic_schools.py` - ~8 Endpoints
6. `backend/api/instrument.py` - ~6 Endpoints
7. `backend/api/world.py` - ~10 Endpoints
8. `backend/api/multiplayer.py` - ~8 Endpoints
9. `backend/api/auth.py` - ~5 Endpoints
10. `backend/api/game.py` - ~15 Endpoints
11. `backend/api/training.py` - ~8 Endpoints
12. `backend/api/voice.py` - ~6 Endpoints
13. `backend/api/admin.py` - ~8 Endpoints
14. `backend/api/arena.py` - ~10 Endpoints

**Pattern für jeden Endpoint:**
```python
# 1. Imports hinzufügen
from backend.database import get_db
from backend.models.xxx import XXXModel
from sqlalchemy.orm import Session
from fastapi import Depends

# 2. Entferne in-memory Service
# VORHER: service = XXXService()
# NACHHER: Kein globaler Service mehr!

# 3. Jeder Endpoint bekommt db Parameter
@router.post("/endpoint")
async def endpoint_name(
    request: RequestModel,
    db: Session = Depends(get_db)  # ✅ Dependency Injection
):
    # 4. CRUD Operations statt Service Calls

    # CREATE
    obj = Model(**request.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    # READ
    obj = db.query(Model).filter(Model.id == id).first()
    if not obj:
        raise HTTPException(404, "Not found")

    # UPDATE
    obj.field = new_value
    db.commit()
    db.refresh(obj)

    # DELETE
    db.delete(obj)
    db.commit()

    return {"success": True, "data": obj}
```

**Warum:** Ohne Database gehen ALLE Daten verloren beim Server-Restart!
**Test:** Nach jedem File:
1. Server neu starten
2. Endpoint testen (z.B. POST `/api/slime/create`)
3. Server neu starten
4. GET Endpoint testen (z.B. GET `/api/slime/1`)
5. ✅ Daten sollten noch da sein!

**Zeit:** 2-3 Stunden (16 Files, ~10 Minuten pro File)

---

#### Task 2.1: backend/api/slime.py umschreiben
**Priorität:** 🔴 HOCH (Beispiel-File)
**Endpoints:** 12 Endpoints
**Model:** `backend/models/slime_companion.py`

**Checklist:**
- [ ] Import `get_db`, `SlimeCompanion`, `Session`, `Depends`
- [ ] Entferne `slime_system = SlimeSystem()` global
- [ ] Alle 12 Endpoints umschreiben:
  - [ ] `/create` - db.add()
  - [ ] `/experience` - db.query().filter().first() + db.commit()
  - [ ] `/metamorphosis` - db.query() + update
  - [ ] `/color/collect` - db.query() + update
  - [ ] `/learn` - db.query() + update
  - [ ] `/rescue` - db.query() + update
  - [ ] `/tamagotchi/update` - db.query() + update
  - [ ] `/feed` - db.query() + update
  - [ ] `/water` - db.query() + update
  - [ ] `/sleep` - db.query() + update
  - [ ] `/{companion_id}` GET - db.query().filter()
  - [ ] `/state/export` - db.query().all()
  - [ ] `/state/import` - db.add_all()

**Test:**
```bash
# Start Server
uvicorn backend.main:app --reload

# Test (in anderem Terminal oder Browser)
curl -X POST http://localhost:8000/api/slime/create \
  -H "Content-Type: application/json" \
  -d '{"owner_player_id": 1, "name": "TestSlime", "starting_region": "forest"}'

# Server RESTART!
# STRG+C und uvicorn nochmal starten

# Test ob Daten noch da sind
curl http://localhost:8000/api/slime/1

# ✅ Sollte TestSlime zurückgeben!
```

---

#### Task 2.2 - 2.14: Alle anderen API Files
**Wiederhole für:**
- `backend/api/pvp.py` (Model: `pvp_battle.py`)
- `backend/api/arena.py` (Model: `arena_monster.py`)
- `backend/api/magic_schools.py` (Model: `magic_progress.py`)
- `backend/api/auth.py` (Model: `user.py`)
- `backend/api/game.py` (Models: `character.py`, `inventory.py`)
- `backend/api/training.py` (Model: `training.py`)
- ... etc.

**Immer gleicher Pattern:**
1. Imports hinzufügen
2. Globale Services entfernen
3. `db: Session = Depends(get_db)` zu jedem Endpoint
4. CRUD Operations statt Service Calls
5. Testen mit Server Restart!

---

### 🟢 PHASE 3: OPTIONAL (Nice to have)

**Status:** ⏳ NUR WENN ZEIT ÜBRIG IST

#### Task 3.1: alembic/env.py Model Imports
**File:** `backend/alembic/env.py`

**Prüfe ob vorhanden:**
```python
from backend.models import (
    user, character, inventory, training,
    slime_companion, pvp_battle, arena_monster, magic_progress
)
from backend.database import Base

target_metadata = Base.metadata
```

**Warum:** Alembic muss Models sehen für `--autogenerate`
**Zeit:** 5 Minuten

---

#### Task 3.2: Tests schreiben
**Directory:** `tests/` (NEU erstellen)

**Beispiel:** `tests/test_slime_api.py`
```python
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_slime():
    response = client.post("/api/slime/create", json={
        "owner_player_id": 1,
        "name": "Test Slime",
        "starting_region": "Forest"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Slime"

def test_get_slime():
    # Create
    create_response = client.post("/api/slime/create", json={
        "owner_player_id": 1,
        "name": "Test Slime 2",
        "starting_region": "Forest"
    })
    companion_id = create_response.json()["companion_id"]

    # Get
    get_response = client.get(f"/api/slime/{companion_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Slime 2"
```

**Warum:** Qualitätssicherung
**Zeit:** 4-8 Stunden (wenn alle Endpoints getestet werden)

---

#### Task 3.3: Docker Setup
**File:** `docker-compose.yml` (NEU)

**Inhalt:**
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app/backend
      - ./najika_world.db:/app/najika_world.db
    environment:
      - DATABASE_URL=sqlite:///./najika_world.db
      - DEBUG=True
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Warum:** Production Deployment
**Zeit:** 1-2 Stunden

---

## ✅ DEFINITION OF DONE

**PHASE 1 ist DONE wenn:**
- [ ] `pip install` funktioniert ohne Errors
- [ ] `python -c "from backend.config import settings"` funktioniert
- [ ] `najika_world.db` File existiert
- [ ] `alembic/versions/*.py` File existiert
- [ ] Server startet mit `uvicorn backend.main:app --reload`
- [ ] Swagger UI lädt: `http://localhost:8000/docs`
- [ ] `/health` Endpoint gibt 200 zurück
- [ ] Keine Errors im Server Log

**PHASE 2 ist DONE wenn:**
- [ ] ALLE 16 API Files umgeschrieben (in-memory → database)
- [ ] Test: Create Slime → Server Restart → Get Slime → ✅ Daten noch da
- [ ] Test: Create User → Server Restart → Login → ✅ Funktioniert
- [ ] Test: Create Arena Monster → Server Restart → Get Monster → ✅ Daten da
- [ ] Keine Errors im Server Log

**PHASE 3 ist DONE wenn:**
- [ ] `alembic/env.py` importiert alle Models
- [ ] `tests/` Directory existiert mit mindestens 3 Test-Files
- [ ] `pytest` läuft ohne Errors
- [ ] `docker-compose up` startet Backend

---

## 🚨 WICHTIGE HINWEISE

### Was du NICHT tun sollst:
❌ Modelfiles ändern (lasse `backend/models/*.py` WIE SIE SIND!)
❌ Services löschen (lasse `backend/services/*.py` - werden für Business Logic genutzt)
❌ Neue Features hinzufügen (fokussiere auf Setup + Integration!)
❌ Code refactoring (lass Code-Struktur wie sie ist!)

### Was du tun sollst:
✅ Dependencies installieren
✅ Database funktionsfähig machen
✅ Endpoints auf Database umstellen
✅ Testen dass Persistence funktioniert
✅ Server lauffähig machen

---

## 📊 ZEITSCHÄTZUNG

**Phase 1 (KRITISCH):**
- Task 1.1: 5 min
- Task 1.2: 5 min
- Task 1.3: 5 min
- Task 1.4: 10 min
- Task 1.5: 10 min
**TOTAL:** 45 Minuten

**Phase 2 (WICHTIG):**
- Task 2.1: 20 min (Beispiel-File, gründlich)
- Task 2.2-2.14: 10 min × 13 = 130 min
**TOTAL:** 2.5 Stunden

**Phase 3 (OPTIONAL):**
- Task 3.1: 5 min
- Task 3.2: 4-8 Stunden
- Task 3.3: 1-2 Stunden
**TOTAL:** 5-10 Stunden

**GESAMT (ohne Optional):** ~3.5 Stunden

---

## 🎯 ERFOLGSKRITERIEN

### Minimum Success:
✅ Server startet
✅ Database existiert
✅ Swagger UI funktioniert
✅ Health Check gibt 200 zurück

### Good Success:
✅ Minimum +
✅ Alle Endpoints umgeschrieben (database statt in-memory)
✅ Create/Read/Update/Delete funktioniert
✅ Persistence nach Server Restart

### Perfect Success:
✅ Good +
✅ Tests geschrieben (mindestens 3 Files)
✅ alembic/env.py korrekt
✅ Docker Setup vorhanden

---

## 📝 REPORTING

**Nach PHASE 1:**
Erstelle Report: `WEB_MODEL_PHASE1_COMPLETE.md` mit:
- [ ] Was wurde gemacht
- [ ] Welche Commands wurden ausgeführt
- [ ] Screenshots von Server Start + Swagger UI
- [ ] Liste aller Tests die du gemacht hast

**Nach PHASE 2:**
Erstelle Report: `WEB_MODEL_PHASE2_COMPLETE.md` mit:
- [ ] Welche Files wurden umgeschrieben
- [ ] Beispiel Code-Änderungen (VORHER/NACHHER)
- [ ] Test-Ergebnisse (mit Server Restart!)
- [ ] Liste aller funktionierenden Endpoints

**Nach PHASE 3 (optional):**
Erstelle Report: `WEB_MODEL_PHASE3_COMPLETE.md` mit:
- [ ] Test Coverage Report
- [ ] Docker Setup Instructions
- [ ] alembic/env.py Code

---

## 🆘 WENN DU BLOCKIERT BIST

**Problem:** Import Errors
**Lösung:** `pip install -r backend/requirements.txt` nochmal ausführen

**Problem:** Alembic findet Models nicht
**Lösung:** Prüfe `alembic/env.py` - importiert es `from backend.models import ...`?

**Problem:** Database Errors
**Lösung:** Lösche `najika_world.db` und `alembic upgrade head` nochmal

**Problem:** Server startet nicht
**Lösung:** Check `.env` File - existiert es? Sind SECRET_KEY und JWT_SECRET gesetzt?

**Problem:** Endpoints returnen 500
**Lösung:** Check Server Log - welches Model fehlt? Importiere es in `database.py`

---

## 📚 REFERENZEN

**SQLAlchemy CRUD Cheatsheet:**
```python
# CREATE
obj = Model(field1=value1, field2=value2)
db.add(obj)
db.commit()
db.refresh(obj)  # Lädt ID zurück

# READ (single)
obj = db.query(Model).filter(Model.id == id).first()
if not obj:
    raise HTTPException(404, "Not found")

# READ (multiple)
objs = db.query(Model).filter(Model.owner_id == owner_id).all()

# UPDATE
obj = db.query(Model).filter(Model.id == id).first()
obj.field = new_value
db.commit()
db.refresh(obj)

# DELETE
obj = db.query(Model).filter(Model.id == id).first()
db.delete(obj)
db.commit()

# COMPLEX QUERY
from sqlalchemy import and_, or_

objs = db.query(Model).filter(
    and_(
        Model.level >= 5,
        Model.region == "forest"
    )
).order_by(Model.created_at.desc()).limit(10).all()
```

**FastAPI Dependency Injection:**
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import get_db

@router.post("/endpoint")
async def endpoint(
    request: RequestModel,
    db: Session = Depends(get_db)  # ✅ Automatisch injected
):
    # db ist jetzt verfügbar!
    pass
```

**Alembic Commands:**
```bash
# Migration erstellen (autogenerate)
alembic revision --autogenerate -m "Description"

# Migration anwenden (upgrade)
alembic upgrade head

# Migration rückgängig (downgrade)
alembic downgrade -1

# Aktuellen Status zeigen
alembic current

# History zeigen
alembic history
```

---

## 🎯 FINAL NOTE

**Du hast bereits 80% geschafft!** 🎉

Die Code-Struktur ist **perfekt**:
- ✅ Flask komplett entfernt
- ✅ FastAPI Pattern korrekt
- ✅ Models definiert
- ✅ Services geschrieben
- ✅ Router aufgesetzt

Jetzt brauchen wir nur noch:
- ✅ Setup (Dependencies, Migrations, .env)
- ✅ Integration (Endpoints → Database)

**Das schaffst du!** 💪

Wenn du Fragen hast → schreib sie in die Phase Reports!
Wenn du blockiert bist → dokumentiere das Problem genau!

---

**VIEL ERFOLG!** 🚀

Kuja + Local Claude
