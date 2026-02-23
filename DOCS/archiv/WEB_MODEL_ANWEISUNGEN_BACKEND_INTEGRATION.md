# 🎯 ANWEISUNGEN FÜR WEB MODEL - BACKEND INTEGRATION

**Erstellt:** 2025-11-17
**Für:** Web Model (Online Claude Code Instanz)
**Branch:** `claude/remote-access-setup-011CUt97k27tgaNUMZdyA9DY`
**Ziel:** Finale Backend-Struktur für UE5 Integration

---

## 📋 KONTEXT

Du hast **EXZELLENTE** Arbeit geleistet! +44,960 Zeilen Code, alle fehlenden Features implementiert!

**ABER:** Jetzt müssen wir das Backend **UE5-kompatibel** machen, weil:
- Das Spiel wird in **Unreal Engine 5** gebaut (nicht Browser!)
- Backend muss **REST API** für UE5 C++ HTTP Client bereitstellen
- Keine Browser-spezifischen Features (WebSocket ist OK, aber optional)

---

## 🎯 DEINE AUFGABEN (1-5)

### ❗ AUFGABE 1: Backend Consolidation (FastAPI als Master)

**Problem:**
- Aktuell: **Flask Blueprints** in `api/slime.py`, `api/pvp.py`, etc.
- Aber: `main.py` nutzt **FastAPI**
- **Flask und FastAPI können NICHT gleichzeitig laufen!**

**LÖSUNG:**

**1.1 Konvertiere ALLE Flask-Blueprints zu FastAPI Routern**

Beispiel für `backend/api/slime.py`:

**❌ VORHER (Flask):**
```python
from flask import Blueprint, request, jsonify

slime_bp = Blueprint('slime', __name__, url_prefix='/api/slime')

@slime_bp.route('/create', methods=['POST'])
def create_companion():
    data = request.get_json()
    # ...
```

**✅ NACHHER (FastAPI):**
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/slime", tags=["slime"])

class CreateCompanionRequest(BaseModel):
    owner_player_id: int
    name: str
    starting_region: str

@router.post("/create")
async def create_companion(request: CreateCompanionRequest):
    # ...
```

**1.2 Update `backend/main.py`**

```python
from fastapi import FastAPI
from backend.api import slime, pvp, oregon_events, arena, region_boss, magic_schools, instrument, world

app = FastAPI(title="Najika Backend API", version="4.0.0")

# Include ALL routers
app.include_router(slime.router)
app.include_router(pvp.router)
app.include_router(oregon_events.router)
app.include_router(arena.router)
app.include_router(region_boss.router)
app.include_router(magic_schools.router)
app.include_router(instrument.router)
app.include_router(world.router)
```

**1.3 Remove Flask Dependencies**

- Delete: `from flask import ...` (überall!)
- Update: `requirements.txt` (remove `flask`, keep `fastapi`, `uvicorn`)

**DEADLINE:** 2 Tage

---

### ❗ AUFGABE 2: Database Strategy (SQLite Local, PostgreSQL Production)

**Entscheidung:**
- **Lokal (Development):** SQLite (`najika.db`)
- **Production (Docker):** PostgreSQL

**LÖSUNG:**

**2.1 Update `backend/config.py`**

```python
class Settings(BaseSettings):
    # Database (Auto-detect)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./najika.db"  # Default: SQLite
    )

    # PostgreSQL for Production
    # Set via ENV: DATABASE_URL=postgresql://user:pass@db:5432/najika

    @property
    def is_production(self) -> bool:
        return "postgresql" in self.DATABASE_URL
```

**2.2 Alembic Migrations Setup**

Du hast schon `backend/alembic/` - SEHR GUT!

**Aber:** Erstelle initiale Migration für ALLE Models:

```bash
# In backend/
alembic revision --autogenerate -m "Initial schema - all models"
alembic upgrade head
```

**2.3 Models konsolidieren**

Checke ob ALLE Models in `backend/models/` sind:
- ✅ `user.py`, `character.py`, `inventory.py`, `training.py` (schon da)
- ❌ **Fehlend:** Slime, PvP, Oregon Events, Arena, Region Boss, Magic Schools, Instrument

**Erstelle:**
```python
# backend/models/slime.py
from sqlalchemy import Column, Integer, String, Boolean, Float, JSON, DateTime, ForeignKey
from backend.database import Base

class SlimeCompanion(Base):
    __tablename__ = "slime_companions"

    id = Column(Integer, primary_key=True)
    owner_player_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    is_slime = Column(Boolean, default=False)
    fantasy_tier = Column(String, nullable=True)
    slime_color = Column(String, nullable=True)
    learned_moves = Column(JSON, default=[])
    tamagotchi_stats = Column(JSON, default={})
    colors_collected = Column(JSON, default=[])
    last_rescue_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

Gleiches für:
- `backend/models/pvp.py` (PvP Battles, Rankings)
- `backend/models/arena.py` (Nemesis Arena, Finishers)
- `backend/models/boss.py` (Region Bosses)
- `backend/models/magic.py` (Magic Schools Progress)

**DEADLINE:** 3 Tage

---

### ❗ AUFGABE 3: Flask/FastAPI Migration Checklist

**DIESE Files müssen zu FastAPI konvertiert werden:**

1. ✅ `backend/api/slime.py` (471 Zeilen Flask → FastAPI)
2. ✅ `backend/api/pvp.py` (369 Zeilen Flask → FastAPI)
3. ✅ `backend/api/oregon_events.py` (196 Zeilen Flask → FastAPI)
4. ✅ `backend/api/arena.py` (485 Zeilen Flask → FastAPI)
5. ✅ `backend/api/region_boss.py` (462 Zeilen Flask → FastAPI)
6. ✅ `backend/api/magic_schools.py` (256 Zeilen Flask → FastAPI)
7. ✅ `backend/api/instrument.py` (405 Zeilen Flask → FastAPI)
8. ✅ `backend/api/world.py` (529 Zeilen Flask → FastAPI)
9. ✅ `backend/api/multiplayer.py` (179 Zeilen Flask → FastAPI)

**Migration Pattern:**

```python
# Flask → FastAPI Conversion Cheat Sheet

# 1. Imports
- from flask import Blueprint, request, jsonify
+ from fastapi import APIRouter, HTTPException
+ from pydantic import BaseModel

# 2. Blueprint → Router
- slime_bp = Blueprint('slime', __name__, url_prefix='/api/slime')
+ router = APIRouter(prefix="/api/slime", tags=["slime"])

# 3. Routes
- @slime_bp.route('/create', methods=['POST'])
+ @router.post("/create")

# 4. Request Data
- data = request.get_json()
+ async def create(request: CreateRequest):

# 5. Responses
- return jsonify({"success": True}), 200
+ return {"success": True}  # FastAPI auto-converts

# 6. Errors
- return jsonify({"error": "Not found"}), 404
+ raise HTTPException(status_code=404, detail="Not found")
```

**DEADLINE:** 5 Tage (alle 9 Files)

---

### ❗ AUFGABE 4: TOR Integration - Browser Modul

**Kontext:**
- TOR ist für **Browser Modul** (Najika surft im Darknet)
- Auch für **Terminal Modul**
- **NICHT** für API Zugriff (das wäre zu langsam)

**LÖSUNG:**

**4.1 TOR Service als separates Modul**

```python
# backend/services/tor_browser.py (NEU!)

from backend.security.tor_integration import TORService

class TORBrowserService:
    """TOR Browser für Najika's Browser Modul"""

    def __init__(self):
        self.tor = TORService()
        self.is_active = False

    def start_tor_session(self):
        """Start TOR für Browsing"""
        self.tor.start()
        self.is_active = True
        return {
            "status": "connected",
            "circuit": self.tor.get_current_circuit(),
            "ip": self.tor.get_exit_ip()
        }

    def fetch_url(self, url: str, use_tor: bool = True):
        """Fetch URL (mit oder ohne TOR)"""
        if use_tor and not self.is_active:
            self.start_tor_session()

        if use_tor:
            return self.tor.fetch_via_tor(url)
        else:
            return requests.get(url)

    def search_darknet(self, query: str):
        """Darknet Suche (Ahmia, etc.)"""
        # Ahmia = Darknet Search Engine
        search_url = f"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={query}"
        return self.fetch_url(search_url, use_tor=True)
```

**4.2 API Endpoints für Browser Modul**

```python
# backend/api/browser.py (NEU!)

from fastapi import APIRouter
from backend.services.tor_browser import TORBrowserService

router = APIRouter(prefix="/api/browser", tags=["browser"])
tor_browser = TORBrowserService()

@router.post("/tor/start")
async def start_tor():
    """Start TOR Session"""
    result = tor_browser.start_tor_session()
    return result

@router.post("/tor/stop")
async def stop_tor():
    """Stop TOR Session"""
    tor_browser.tor.stop()
    return {"status": "disconnected"}

@router.get("/fetch")
async def fetch_url(url: str, use_tor: bool = False):
    """Fetch URL (optional via TOR)"""
    content = tor_browser.fetch_url(url, use_tor)
    return {"url": url, "content": content[:1000]}  # First 1000 chars

@router.get("/darknet/search")
async def search_darknet(query: str):
    """Search Darknet (via Ahmia)"""
    results = tor_browser.search_darknet(query)
    return {"query": query, "results": results}
```

**4.3 Frontend Integration (Browser Modul)**

Im UE5 Game:
- Player öffnet "Terminal" oder "Browser" Modul
- UI zeigt TOR Status (Connected/Disconnected)
- Player kann URLs eingeben
- Option: "Use TOR" Checkbox

**WICHTIG:**
- TOR nur für Browser/Terminal Modul
- **NICHT** für normales API (zu langsam!)

**DEADLINE:** 2 Tage

---

### ❗ AUFGABE 5: Multiplayer Backend - Testing Phase

**Kontext:**
- Multiplayer Backend ist ready
- Aber: Launch erst nach **Private Beta** (nur Kuja + Freunde)
- Dann **Offizielle Beta** (ausgewählte Tester)

**LÖSUNG:**

**5.1 Multiplayer Toggle (Feature Flag)**

```python
# backend/config.py

class Settings(BaseSettings):
    # ...
    MULTIPLAYER_ENABLED: bool = os.getenv("MULTIPLAYER_ENABLED", "false").lower() == "true"
    MULTIPLAYER_MAX_PLAYERS: int = int(os.getenv("MULTIPLAYER_MAX_PLAYERS", "8"))
    MULTIPLAYER_MODE: str = os.getenv("MULTIPLAYER_MODE", "private")  # private, beta, public
```

**5.2 Multiplayer Access Control**

```python
# backend/api/multiplayer.py

@router.post("/join")
async def join_multiplayer(user_id: int):
    """Join Multiplayer Session"""

    # Check if multiplayer enabled
    if not settings.MULTIPLAYER_ENABLED:
        raise HTTPException(status_code=403, detail="Multiplayer not available yet")

    # Check access level
    if settings.MULTIPLAYER_MODE == "private":
        # Only whitelisted users
        if user_id not in WHITELIST:
            raise HTTPException(status_code=403, detail="Private beta - invite only")

    # Join logic
    # ...
```

**5.3 Whitelist System**

```python
# backend/multiplayer_whitelist.py (NEU!)

MULTIPLAYER_WHITELIST = {
    "private": [
        1,  # Kuja
        2,  # Friend 1
        3,  # Friend 2
        # ... max 7 friends
    ],
    "beta": [
        # ... wird später erweitert
    ]
}
```

**5.4 Launch Plan**

```python
# Phase 1: Private (nur Kuja + 7 Freunde)
MULTIPLAYER_ENABLED=true
MULTIPLAYER_MODE=private
MULTIPLAYER_MAX_PLAYERS=8

# Phase 2: Beta (50-100 Tester)
MULTIPLAYER_MODE=beta
MULTIPLAYER_MAX_PLAYERS=100

# Phase 3: Public
MULTIPLAYER_MODE=public
MULTIPLAYER_MAX_PLAYERS=1000
```

**DEADLINE:** 1 Tag (nur Feature Flag + Whitelist)

---

## 📊 PRIORITÄTEN

### 🔴 KRITISCH (DIESE WOCHE):
1. **Flask → FastAPI Migration** (Aufgabe 1 + 3)
2. **Database Models erstellen** (Aufgabe 2)

### 🟡 WICHTIG (NÄCHSTE WOCHE):
3. **TOR Browser Modul** (Aufgabe 4)
4. **Multiplayer Toggle** (Aufgabe 5)

---

## ✅ ABNAHME-KRITERIEN

### Aufgabe 1 + 3: Flask → FastAPI
- [ ] Alle 9 API Files konvertiert
- [ ] `main.py` inkludiert alle Router
- [ ] Keine Flask imports mehr
- [ ] Server startet mit `uvicorn backend.main:app`
- [ ] Alle Endpoints funktionieren

### Aufgabe 2: Database
- [ ] SQLite läuft lokal
- [ ] PostgreSQL läuft in Docker
- [ ] Alembic Migrations erstellt
- [ ] Alle Models in `backend/models/`
- [ ] `alembic upgrade head` funktioniert

### Aufgabe 4: TOR
- [ ] `TORBrowserService` implementiert
- [ ] API Endpoints für Browser Modul
- [ ] TOR kann gestartet/gestoppt werden
- [ ] Darknet Search funktioniert

### Aufgabe 5: Multiplayer
- [ ] Feature Flag `MULTIPLAYER_ENABLED`
- [ ] Whitelist System
- [ ] Access Control funktioniert

---

## 🚫 WAS DU NICHT TUN SOLLST

### ❌ NICHT ändern:
- `backend/services/*.py` (Business Logic ist GUT!)
- Particle Systems, Audio Systems (Browser-spezifisch, ok!)
- Analytics, Security Module (behalten!)
- Testing Suite (behalten!)

### ❌ NICHT entfernen:
- Docker-compose, CI/CD (behalten!)
- Documentation (behalten!)

### ❌ NICHT neu implementieren:
- Quest System (kommt später)
- Achievement System (kommt später)
- Crafting System (kommt später)

---

## 📝 REPORTING

**Nach jeder Aufgabe:**

1. **Commit mit klarer Message:**
```bash
git commit -m "TASK 1: Convert Flask to FastAPI - slime.py, pvp.py, oregon_events.py"
```

2. **Update `PROJECT_SUMMARY.md`:**
```markdown
## ✅ Completed (2025-11-18)
- [x] Task 1: Flask → FastAPI Migration (9 files)
- [x] Task 2: Database Models (Slime, PvP, Arena, Boss, Magic)
```

3. **Testing:**
```bash
# Test alle Endpoints
pytest tests/test_backend.py -v

# Test Server Start
uvicorn backend.main:app --reload
```

---

## 🎯 ZIEL

**Am Ende dieser Tasks:**
- ✅ Einheitliches FastAPI Backend
- ✅ SQLite (lokal) + PostgreSQL (production)
- ✅ TOR Browser Modul ready
- ✅ Multiplayer mit Feature Flag
- ✅ UE5-ready REST API

**Dann können wir:**
- UE5 HTTP Client gegen Backend testen
- Private Beta starten (Kuja + Freunde)
- Fehlende Features implementieren (Quest, Achievement, Crafting)

---

## 💬 FRAGEN?

**Bei Unklarheiten:**
- Schreibe in Commit Message: `QUESTION: Wie soll X funktionieren?`
- Erstelle `QUESTIONS.md` im Root
- User wird antworten

**Bei Problemen:**
- `ERROR_LOG.md` erstellen
- Stack Trace inkludieren
- User wird helfen

---

**VIEL ERFOLG! Du schaffst das! 💪**

**- Kuja & Local Claude Code Instance**
