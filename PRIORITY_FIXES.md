# 🔧 NAJIKA WORLD - PRIORITÄT FIXES (ACTIONABLE)

## TIER 1: SOFORT BEHEBEN (Today!)

### FIX #1: Backend Decision - WHICH ONE TO USE?

**DECISION NEEDED:**
```bash
OPTION A: Keep FastAPI (/backend/main.py)
  Pros: Modern, modular, already set up
  Cons: Some features missing (Game Actions, Living System)
  
OPTION B: Keep Flask (/backend/api/server.py)
  Pros: Has all features in one file
  Cons: Monolithic, hard to maintain
```

**RECOMMENDED:** Option A (FastAPI) - Modern and maintainable

**ACTION ITEMS:**
```bash
# 1. Remove Flask server (or archive it)
mv /home/user/Najika_World/backend/api/server.py /home/user/Najika_World/backend/api/server.py.ARCHIVED

# 2. Update ALL hardcoded URLs from 5000 to 8000
grep -r "localhost:5000\|127.0.0.1:5000" /home/user/Najika_World/ | grep -v ".git" | grep -v ".ARCHIVED"

# Then update each file:
# - /digivice/static/js/api_client.js: Change baseURL
# - Any other references
```

---

### FIX #2: Integrate Najika Game Actions into FastAPI

**LOCATION:** `/backend/najika_game_actions.py` (29KB)

**ACTION 1: Create new router file:**
```bash
cat > /home/user/Najika_World/backend/api/najika_game_actions_router.py << 'ROUTER_EOF'
"""
Najika Game Actions Router
Exposes najika_game_actions.py functionality via FastAPI
"""

from fastapi import APIRouter, Depends
from typing import Optional, Dict, Any
import sys
import os

# Import the game actions module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from najika_game_actions import (
    LOCATIONS, RECIPES, ACTIONS,
    suggest_action, decide_action, get_status,
    get_current_activity, teleport_location, execute_recipe
)

router = APIRouter(prefix="/najika", tags=["Najika Game Actions"])

@router.get("/status")
async def get_najika_status():
    """Get Najika's complete status (location, hunger, energy, mood, activity)"""
    return get_status()

@router.get("/current-activity")
async def get_najika_activity():
    """Get what Najika is currently doing"""
    return get_current_activity()

@router.post("/suggest-action")
async def suggest_next_action():
    """Suggest next action based on current state"""
    return suggest_action()

@router.post("/auto-decide-action")
async def auto_decide_action():
    """Najika autonomously decides her next action!"""
    return decide_action()

@router.get("/locations")
async def get_locations():
    """Get all available locations"""
    return {"locations": LOCATIONS}

@router.post("/teleport")
async def teleport_to_location(location_id: str):
    """Teleport Najika to a location"""
    return teleport_location(location_id)

@router.get("/recipes")
async def get_recipes():
    """Get all available recipes"""
    return {"recipes": RECIPES}

@router.post("/execute-recipe")
async def execute_recipe_action(recipe_id: str):
    """Execute a recipe"""
    return execute_recipe(recipe_id)
ROUTER_EOF
```

**ACTION 2: Add to main.py:**
```python
# In /backend/main.py, add to imports (line 17):
from backend.api import (
    auth, game, training, voice, admin, arena,
    slime, pvp, oregon_events, region_boss, magic_schools,
    instrument, world, multiplayer, card_game, dice_monsters,
    housing, farming, world_map, najika_compat,
    najika_game_actions_router  # ADD THIS
)

# Then in router includes section (after line 144):
app.include_router(najika_game_actions_router.router)  # Add this
```

**VERIFY:**
```bash
cd /home/user/Najika_World
python3 -c "from backend.api import najika_game_actions_router; print('OK')"
```

---

### FIX #3: Integrate Living System into FastAPI

**LOCATION:** `/backend/najika_living_system.py` (36KB)

**ACTION:** Similar to Game Actions - create wrapper router:

```bash
cat > /home/user/Najika_World/backend/api/living_system_router.py << 'LIVING_EOF'
"""
Najika Living System Router
Exposes living_system.py functionality via FastAPI
"""

from fastapi import APIRouter, WebSocket
from typing import Optional, Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from najika_living_system import (
    NajikaLivingSystem,
    get_emotional_state, update_relationship,
    get_daily_activity, learn_new_behavior
)

router = APIRouter(prefix="/living", tags=["Living System"])

# Initialize living system
living_system = NajikaLivingSystem()

@router.get("/state")
async def get_living_state():
    """Get Najika's complete living state"""
    return living_system.get_state()

@router.get("/emotions")
async def get_emotions():
    """Get emotional state"""
    return get_emotional_state(living_system)

@router.post("/relationship/update")
async def update_rel(interaction: str, sentiment: int):
    """Update relationship based on interaction"""
    return update_relationship(living_system, interaction, sentiment)

@router.get("/daily-activities")
async def get_activities():
    """Get today's planned activities"""
    return get_daily_activity(living_system)

@router.post("/learn")
async def learn_behavior(behavior: str, context: str):
    """Najika learns new behavior"""
    return learn_new_behavior(living_system, behavior, context)

@router.websocket("/ws/interaction")
async def websocket_interaction(websocket: WebSocket):
    """Real-time interaction websocket"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            response = living_system.process_interaction(data)
            await websocket.send_json(response)
    except Exception as e:
        await websocket.close(code=1000)
LIVING_EOF
```

Then add to main.py same as above.

---

### FIX #4: Fix Battle API Endpoint Names

**PROBLEM:** Frontend looks for `/api/battle/*` but backend has `/api/v1/game/combat/*`

**OPTION A: Change Frontend (EASIER)**
```javascript
// In /frontend/src/game/BattleAPI.js, change:

const BACKEND_URL = 'http://localhost:8000';
const API_PREFIX = '/api/v1';  // Add this

// Then update all calls:
- fetch(`${BACKEND_URL}/api/battle/start`)
+ fetch(`${BACKEND_URL}${API_PREFIX}/game/character/create`)

- fetch(`${BACKEND_URL}/api/battle/status`)
+ fetch(`${BACKEND_URL}${API_PREFIX}/game/character`)

- fetch(`${BACKEND_URL}/api/battle/action`)
+ fetch(`${BACKEND_URL}${API_PREFIX}/game/combat/action`)

- fetch(`${BACKEND_URL}/api/battle/skills`)
+ fetch(`${BACKEND_URL}${API_PREFIX}/game/skills`)
```

**OPTION B: Create Battle Router Alias (RECOMMENDED)**
```python
# In /backend/api/battle_alias.py
from fastapi import APIRouter
from backend.api.game import router as game_router

router = APIRouter(prefix="/api/battle", tags=["Battle Alias"])

# Re-expose game endpoints under /api/battle prefix
# This maintains backward compatibility

# In main.py add:
app.include_router(battle_alias.router)
```

---

### FIX #5: Create Clear Start Script

**CREATE:** `/backend/start_server.sh`

```bash
#!/bin/bash
set -e

echo "🚀 NAJIKA WORLD BACKEND STARTUP"
echo "=================================="

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python Version: $PYTHON_VERSION"

# Check dependencies
echo ""
echo "Checking dependencies..."
python3 -c "import fastapi; print('✅ FastAPI installed')" || {
    echo "❌ FastAPI missing. Installing..."
    pip install -r requirements.txt
}

# Create necessary directories
mkdir -p logs saves uploads downloads

# Initialize database
echo ""
echo "Initializing database..."
python3 << 'INIT_DB'
from backend.database import init_db
init_db()
print("✅ Database initialized")
INIT_DB

# Check API imports
echo ""
echo "Verifying API modules..."
python3 << 'VERIFY'
try:
    from backend.api import (
        auth, game, arena, training, voice, admin,
        slime, pvp, oregon_events, region_boss, magic_schools,
        instrument, world, multiplayer, card_game, dice_monsters,
        housing, farming, world_map, najika_compat
    )
    print("✅ All core modules loaded")
except ImportError as e:
    print(f"❌ Module import error: {e}")
    exit(1)
VERIFY

# Start backend
echo ""
echo "🎮 Starting Najika Backend..."
echo "Port: 8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

cd /home/user/Najika_World
exec python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**ALSO CREATE:** `/frontend/start_frontend.sh`

```bash
#!/bin/bash
set -e

echo "🎨 NAJIKA FRONTEND STARTUP"
echo "==========================="

cd /home/user/Najika_World/frontend

# Check dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "🌐 Starting Najika Frontend..."
echo "Port: 3000"
echo ""

REACT_APP_API_URL=http://localhost:8000 \
npm start
```

**ALSO CREATE:** `/start_all.sh`

```bash
#!/bin/bash
# Start both frontend and backend in separate terminals

# Check if backend is needed to start
if [ "$1" != "--frontend-only" ]; then
    echo "Starting Backend..."
    bash /home/user/Najika_World/backend/start_server.sh &
    BACKEND_PID=$!
    sleep 5  # Give backend time to start
fi

echo "Starting Frontend..."
bash /home/user/Najika_World/frontend/start_frontend.sh &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers started!"
echo "Backend:  http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop..."

wait
```

---

## TIER 2: TODAY - Integration Lücken Schließen

### FIX #6: Fix Environment Configuration

**CREATE:** `/frontend/.env.example`

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_PREFIX=/api/v1
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_DEBUG=true
REACT_APP_VERSION=1.0.0
```

**UPDATE:** `/backend/.env`

```env
# Remove from .env and keep only in .env.example:
SECRET_KEY=<GENERATE THIS: python3 -c "import secrets; print(secrets.token_urlsafe(32))">
JWT_SECRET=<GENERATE THIS: python3 -c "import secrets; print(secrets.token_urlsafe(32))">

# Use proper values
DATABASE_URL=sqlite:///./najika_world.db
DEBUG=True
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","*"]
API_PREFIX=/api/v1
```

---

### FIX #7: Create Docker Compose

**CREATE:** `/docker-compose.yml`

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: sqlite:///./najika_world.db
      DEBUG: "True"
    volumes:
      - ./backend:/app/backend
      - ./logs:/app/logs
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
      REACT_APP_API_PREFIX: /api/v1
    depends_on:
      - backend
    command: npm start
```

**CREATE:** `/backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### FIX #8: Fix Logging Configuration

**UPDATE:** `/backend/main.py` - Add after imports:

```python
import logging
import logging.handlers

# Configure logging
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # File handler
    fh = logging.handlers.RotatingFileHandler(
        f"{log_dir}/najika.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Console handler
    ch = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Logger
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# Call in lifespan startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=" * 70)
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 70)
    
    logger = setup_logging()  # ADD THIS
    logger.info(f"Starting {settings.APP_NAME}")
    
    # ... rest of startup code
```

---

### FIX #9: API Consistency

**CREATE:** `/backend/API_ENDPOINTS.md`

Document all endpoints in one place:

```markdown
# Najika World API Endpoints

## Base URL
`http://localhost:8000/api/v1`

## Auth
- POST `/auth/register` - Register user
- POST `/auth/login` - Login user
- POST `/auth/logout` - Logout
- GET `/auth/profile` - Get user profile

## Game
- POST `/game/character/create` - Create character
- GET `/game/character` - Get character
- POST `/game/combat/action` - Execute combat action
- GET `/game/inventory` - Get inventory
- POST `/game/inventory/action` - Modify inventory
- GET `/game/skills` - Get skills
- POST `/game/skills/use` - Use skill
- GET `/game/quests` - Get quests
- POST `/game/quests/start` - Start quest

## Najika Game Actions (Living AI)
- GET `/najika/status` - Najika's full status
- GET `/najika/current-activity` - What is she doing?
- POST `/najika/suggest-action` - Suggest action
- POST `/najika/auto-decide-action` - Auto decide
- GET `/najika/locations` - All locations
- POST `/najika/teleport` - Teleport location
- GET `/najika/recipes` - All recipes
- POST `/najika/execute-recipe` - Execute recipe

[... more endpoints ...]
```

---

## Verification Commands

```bash
# After fixes applied, test everything:

# 1. Test Backend Startup
python3 /home/user/Najika_World/backend/main.py &
sleep 3
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Should show Swagger UI

# 2. Test Frontend Config
cd /home/user/Najika_World/frontend
cat .env | grep REACT_APP_API_URL

# 3. Test API Endpoints
curl http://localhost:8000/api/v1/game  # Should work
curl http://localhost:8000/api/battle/start  # Should fail (unless you created alias)

# 4. Check Logging
tail -f logs/najika.log

# 5. Check Database
ls -la najika_world.db
```

---

## Summary of Changes

| Fix # | File | Action | Impact |
|-------|------|--------|--------|
| 1 | various | Remove Flask backend | ✅ Single backend |
| 2 | `api/najika_game_actions_router.py` | Create + integrate | ✅ Game Actions available |
| 3 | `api/living_system_router.py` | Create + integrate | ✅ Living System available |
| 4 | `BattleAPI.js` OR `api/battle_alias.py` | Fix endpoints | ✅ Battle works |
| 5 | `*.sh` | Create start scripts | ✅ Easy startup |
| 6 | `.env*` files | Fix config | ✅ Proper environment |
| 7 | `docker-compose.yml` | Create | ✅ Docker ready |
| 8 | `main.py` | Add logging setup | ✅ Debugging possible |
| 9 | `API_ENDPOINTS.md` | Document | ✅ Clear API reference |

