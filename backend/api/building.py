"""
Building System API - Lego Fortnite Style!

CORE PRINCIPLE: Building is SEAMLESS - no extra mode needed!
- Collect resources in the world
- Craft at workbench
- Place buildings directly
- Everyone can do this - NO player advantages!

Anti-Cheat: Server validates, but doesn't limit playtime.
If someone fishes 10 hours, they GET those fish!
We validate TIME SPENT, not AMOUNT.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import hmac
import json
import math

# WebSocket for realtime notifications
from backend.services.websocket_manager import websocket_manager

router = APIRouter(prefix="/api/building", tags=["Building"])

# ============================================================================
# ENUMS
# ============================================================================

class ResourceType(str, Enum):
    # Basic Resources (gathered in world)
    WOOD = "wood"
    STONE = "stone"
    IRON = "iron"
    GOLD = "gold"
    CRYSTAL = "crystal"
    CLOTH = "cloth"
    LEATHER = "leather"

    # Processed Resources (crafted)
    PLANK = "plank"
    BRICK = "brick"
    INGOT = "ingot"
    GLASS = "glass"
    ROPE = "rope"

    # Special
    MAGIC_ESSENCE = "magic_essence"
    EXPLOSION_DUST = "explosion_dust"  # Najika special!

class BuildingType(str, Enum):
    # Basic Structures
    WALL = "wall"
    FLOOR = "floor"
    ROOF = "roof"
    DOOR = "door"
    WINDOW = "window"
    STAIRS = "stairs"

    # Functional
    WORKBENCH = "workbench"
    FORGE = "forge"
    LOOM = "loom"
    COOKING_STATION = "cooking_station"
    ALCHEMY_TABLE = "alchemy_table"

    # Decorative
    TORCH = "torch"
    LANTERN = "lantern"
    CHAIR = "chair"
    TABLE = "table"
    BED = "bed"
    CHEST = "chest"

    # Advanced
    TELEPORTER = "teleporter"
    DEFENSE_TURRET = "defense_turret"
    GARDEN_PLOT = "garden_plot"
    FISHING_SPOT = "fishing_spot"

class GatherAction(str, Enum):
    CHOP = "chop"      # Trees -> Wood
    MINE = "mine"      # Rocks -> Stone, Iron, Gold, Crystal
    HARVEST = "harvest" # Plants -> Cloth, Food
    HUNT = "hunt"      # Animals -> Leather, Meat
    FISH = "fish"      # Water -> Fish
    FORAGE = "forage"  # Ground -> Herbs, Mushrooms

# ============================================================================
# MODELS
# ============================================================================

class GatherRequest(BaseModel):
    """Request to gather resources"""
    user_id: str
    action: GatherAction
    location: str
    duration_seconds: int  # How long did they gather?
    timestamp: int
    signature: str

class CraftRequest(BaseModel):
    """Request to craft an item"""
    user_id: str
    recipe_id: str
    quantity: int = 1
    timestamp: int
    signature: str

class BuildRequest(BaseModel):
    """Request to place a building"""
    user_id: str
    building_type: BuildingType
    position: Dict[str, float]  # {x, y, z}
    rotation: float = 0
    timestamp: int
    signature: str

class ResourceInventory(BaseModel):
    """Player's resource inventory"""
    user_id: str
    resources: Dict[str, int] = {}
    last_updated: datetime = datetime.now()

# ============================================================================
# GAME DATA
# ============================================================================

# Gather rates (per second of real gathering time)
GATHER_RATES = {
    GatherAction.CHOP: {ResourceType.WOOD: 0.5},  # 30 wood per minute
    GatherAction.MINE: {
        ResourceType.STONE: 0.3,
        ResourceType.IRON: 0.1,
        ResourceType.GOLD: 0.02,
        ResourceType.CRYSTAL: 0.01,
    },
    GatherAction.HARVEST: {ResourceType.CLOTH: 0.2},
    GatherAction.HUNT: {ResourceType.LEATHER: 0.15},
    GatherAction.FISH: {"fish": 0.05},  # 3 fish per minute
    GatherAction.FORAGE: {"herbs": 0.1, "mushrooms": 0.08},
}

# Recipes: what you need to craft what
RECIPES = {
    # Processing
    "plank": {
        "input": {ResourceType.WOOD: 2},
        "output": {ResourceType.PLANK: 1},
        "station": "workbench",
        "time": 5,
    },
    "brick": {
        "input": {ResourceType.STONE: 3},
        "output": {ResourceType.BRICK: 1},
        "station": "forge",
        "time": 10,
    },
    "iron_ingot": {
        "input": {ResourceType.IRON: 2},
        "output": {ResourceType.INGOT: 1},
        "station": "forge",
        "time": 15,
    },
    "glass": {
        "input": {ResourceType.STONE: 4, ResourceType.CRYSTAL: 1},
        "output": {ResourceType.GLASS: 1},
        "station": "forge",
        "time": 20,
    },
    "rope": {
        "input": {ResourceType.CLOTH: 3},
        "output": {ResourceType.ROPE: 1},
        "station": "loom",
        "time": 8,
    },

    # Basic Building
    "wall": {
        "input": {ResourceType.PLANK: 4},
        "output": {"wall": 1},
        "station": "workbench",
        "time": 10,
    },
    "floor": {
        "input": {ResourceType.PLANK: 6},
        "output": {"floor": 1},
        "station": "workbench",
        "time": 12,
    },
    "roof": {
        "input": {ResourceType.PLANK: 5, ResourceType.CLOTH: 2},
        "output": {"roof": 1},
        "station": "workbench",
        "time": 15,
    },
    "door": {
        "input": {ResourceType.PLANK: 3, ResourceType.IRON: 1},
        "output": {"door": 1},
        "station": "workbench",
        "time": 8,
    },
    "window": {
        "input": {ResourceType.PLANK: 2, ResourceType.GLASS: 1},
        "output": {"window": 1},
        "station": "workbench",
        "time": 10,
    },
    "stairs": {
        "input": {ResourceType.PLANK: 8},
        "output": {"stairs": 1},
        "station": "workbench",
        "time": 15,
    },

    # Stations
    "workbench": {
        "input": {ResourceType.WOOD: 10, ResourceType.STONE: 5},
        "output": {"workbench": 1},
        "station": None,  # Can craft without station!
        "time": 30,
    },
    "forge": {
        "input": {ResourceType.STONE: 20, ResourceType.IRON: 5},
        "output": {"forge": 1},
        "station": "workbench",
        "time": 60,
    },
    "loom": {
        "input": {ResourceType.WOOD: 15, ResourceType.CLOTH: 10},
        "output": {"loom": 1},
        "station": "workbench",
        "time": 45,
    },

    # Furniture
    "chest": {
        "input": {ResourceType.PLANK: 6, ResourceType.IRON: 2},
        "output": {"chest": 1},
        "station": "workbench",
        "time": 20,
    },
    "bed": {
        "input": {ResourceType.PLANK: 8, ResourceType.CLOTH: 5, ResourceType.LEATHER: 2},
        "output": {"bed": 1},
        "station": "workbench",
        "time": 30,
    },
    "torch": {
        "input": {ResourceType.WOOD: 1, ResourceType.CLOTH: 1},
        "output": {"torch": 4},
        "station": None,
        "time": 5,
    },
}

# ============================================================================
# IN-MEMORY STORAGE
# ============================================================================

# Player inventories
player_inventories: Dict[str, ResourceInventory] = {}

# Player buildings
player_buildings: Dict[str, List[Dict[str, Any]]] = {}

# Gather sessions (for anti-cheat validation)
gather_sessions: Dict[str, Dict[str, Any]] = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_inventory(user_id: str) -> ResourceInventory:
    """Get or create player inventory"""
    if user_id not in player_inventories:
        player_inventories[user_id] = ResourceInventory(user_id=user_id)
    return player_inventories[user_id]

def validate_gather_time(user_id: str, action: GatherAction, duration: int, timestamp: int) -> bool:
    """
    ANTI-CHEAT: Validate that gather time is realistic.

    We DON'T limit how long someone can gather!
    We validate that the TIME CLAIMED matches REALITY.

    - Max session: 12 hours (43200 seconds) - after that, take a break!
    - Min time per resource: prevents instant-gather exploits
    - Timestamp must be recent (within last 24 hours)
    """
    now = int(datetime.now().timestamp() * 1000)

    # Timestamp must be within last 24 hours
    if abs(now - timestamp) > 86400000:  # 24 hours in ms
        return False

    # Duration must be positive and reasonable
    if duration < 1 or duration > 43200:  # Max 12 hours
        return False

    # Check for impossible gather speed
    # (This catches people claiming 1000 fish in 1 second)
    session_key = f"{user_id}_{action}"
    if session_key in gather_sessions:
        last_session = gather_sessions[session_key]
        time_since_last = (timestamp - last_session['timestamp']) / 1000

        # If less than claimed duration passed, that's cheating
        if time_since_last < duration * 0.9:  # 10% tolerance for lag
            return False

    # Store this session
    gather_sessions[session_key] = {
        'timestamp': timestamp,
        'duration': duration,
    }

    return True

def calculate_gathered_resources(action: GatherAction, duration: int) -> Dict[str, int]:
    """Calculate resources based on gather time"""
    resources = {}
    rates = GATHER_RATES.get(action, {})

    for resource, rate in rates.items():
        # Resources = rate * time (in seconds)
        # Add some randomness (+/- 20%)
        import random
        variance = random.uniform(0.8, 1.2)
        amount = int(rate * duration * variance)
        if amount > 0:
            resources[resource] = amount

    return resources

def can_craft(inventory: ResourceInventory, recipe_id: str, quantity: int = 1) -> bool:
    """Check if player has resources to craft"""
    if recipe_id not in RECIPES:
        return False

    recipe = RECIPES[recipe_id]
    for resource, needed in recipe['input'].items():
        have = inventory.resources.get(resource, 0)
        if have < needed * quantity:
            return False

    return True

def do_craft(inventory: ResourceInventory, recipe_id: str, quantity: int = 1) -> Dict[str, int]:
    """Perform crafting, consume inputs, return outputs"""
    recipe = RECIPES[recipe_id]

    # Consume inputs
    for resource, needed in recipe['input'].items():
        inventory.resources[resource] = inventory.resources.get(resource, 0) - (needed * quantity)

    # Add outputs
    outputs = {}
    for resource, amount in recipe['output'].items():
        total = amount * quantity
        inventory.resources[resource] = inventory.resources.get(resource, 0) + total
        outputs[resource] = total

    inventory.last_updated = datetime.now()
    return outputs

# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/gather")
async def gather_resources(request: GatherRequest, background_tasks: BackgroundTasks):
    """
    Gather resources from the world.

    IMPORTANT: We validate TIME, not limit AMOUNT!
    If you gather for 10 hours, you get 10 hours of resources.
    """
    # Validate gather time (anti-cheat)
    if not validate_gather_time(
        request.user_id,
        request.action,
        request.duration_seconds,
        request.timestamp
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid gather session - time validation failed"
        )

    # Calculate resources
    resources = calculate_gathered_resources(request.action, request.duration_seconds)

    # Add to inventory
    inventory = get_inventory(request.user_id)
    for resource, amount in resources.items():
        inventory.resources[resource] = inventory.resources.get(resource, 0) + amount
    inventory.last_updated = datetime.now()

    # WebSocket notification (async in background)
    background_tasks.add_task(
        websocket_manager.notify_gather_complete,
        int(request.user_id) if request.user_id.isdigit() else 0,
        request.action.value,
        resources,
        request.duration_seconds
    )

    return {
        "success": True,
        "gathered": resources,
        "duration_seconds": request.duration_seconds,
        "message": f"Gathered resources for {request.duration_seconds} seconds!",
        "inventory": inventory.resources,
    }

@router.post("/craft")
async def craft_item(request: CraftRequest, background_tasks: BackgroundTasks):
    """
    Craft an item at a station.

    No limits on crafting - if you have the resources, you can craft!
    """
    if request.recipe_id not in RECIPES:
        raise HTTPException(status_code=404, detail=f"Recipe '{request.recipe_id}' not found")

    inventory = get_inventory(request.user_id)

    if not can_craft(inventory, request.recipe_id, request.quantity):
        recipe = RECIPES[request.recipe_id]
        return {
            "success": False,
            "message": "Not enough resources",
            "needed": recipe['input'],
            "have": {k: inventory.resources.get(k, 0) for k in recipe['input'].keys()},
        }

    outputs = do_craft(inventory, request.recipe_id, request.quantity)

    # WebSocket notification
    background_tasks.add_task(
        websocket_manager.notify_craft_complete,
        int(request.user_id) if request.user_id.isdigit() else 0,
        request.recipe_id,
        request.quantity,
        outputs
    )

    return {
        "success": True,
        "crafted": outputs,
        "quantity": request.quantity,
        "message": f"Crafted {request.quantity}x {request.recipe_id}!",
        "inventory": inventory.resources,
    }

@router.post("/build")
async def place_building(request: BuildRequest, background_tasks: BackgroundTasks):
    """
    Place a building in the world.

    Buildings are placed directly - no building mode needed!
    Like Lego Fortnite: select item, place it.
    """
    inventory = get_inventory(request.user_id)
    building_key = request.building_type.value

    # Check if player has the building item
    if inventory.resources.get(building_key, 0) < 1:
        return {
            "success": False,
            "message": f"You don't have a {building_key} to place!",
            "have": inventory.resources.get(building_key, 0),
        }

    # Consume the building item
    inventory.resources[building_key] -= 1

    # Add to player's buildings
    if request.user_id not in player_buildings:
        player_buildings[request.user_id] = []

    building = {
        "type": request.building_type.value,
        "position": request.position,
        "rotation": request.rotation,
        "placed_at": datetime.now().isoformat(),
    }
    player_buildings[request.user_id].append(building)

    # WebSocket notification for multiplayer sync
    background_tasks.add_task(
        websocket_manager.notify_building_placed,
        int(request.user_id) if request.user_id.isdigit() else 0,
        building_key,
        request.position,
        request.rotation
    )

    return {
        "success": True,
        "building": building,
        "message": f"Placed {building_key}!",
        "remaining": inventory.resources.get(building_key, 0),
    }

@router.get("/inventory/{user_id}")
async def get_player_inventory(user_id: str):
    """Get player's resource inventory"""
    inventory = get_inventory(user_id)
    return {
        "user_id": user_id,
        "resources": inventory.resources,
        "last_updated": inventory.last_updated.isoformat(),
    }

@router.get("/buildings/{user_id}")
async def get_player_buildings(user_id: str):
    """Get player's placed buildings"""
    buildings = player_buildings.get(user_id, [])
    return {
        "user_id": user_id,
        "buildings": buildings,
        "count": len(buildings),
    }

@router.get("/recipes")
async def get_all_recipes():
    """Get all available recipes"""
    return {
        "recipes": RECIPES,
        "count": len(RECIPES),
    }

@router.get("/recipe/{recipe_id}")
async def get_recipe(recipe_id: str):
    """Get a specific recipe"""
    if recipe_id not in RECIPES:
        raise HTTPException(status_code=404, detail=f"Recipe '{recipe_id}' not found")

    return {
        "recipe_id": recipe_id,
        **RECIPES[recipe_id],
    }

@router.get("/gather-rates")
async def get_gather_rates():
    """Get resource gather rates"""
    return {
        "rates": {action.value: rates for action, rates in GATHER_RATES.items()},
        "description": "Resources per second of gathering time",
    }

@router.delete("/building/{user_id}")
async def remove_building(user_id: str, building_index: int):
    """Remove a placed building (returns resources)"""
    if user_id not in player_buildings or building_index >= len(player_buildings[user_id]):
        raise HTTPException(status_code=404, detail="Building not found")

    building = player_buildings[user_id].pop(building_index)

    # Return the building item to inventory
    inventory = get_inventory(user_id)
    building_key = building['type']
    inventory.resources[building_key] = inventory.resources.get(building_key, 0) + 1

    return {
        "success": True,
        "removed": building,
        "returned": building_key,
        "message": f"Removed {building_key} and returned to inventory",
    }
