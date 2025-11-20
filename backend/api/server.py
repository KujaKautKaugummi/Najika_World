"""
Najika Backend API
Version: 3.0
FastAPI-based backend for Najika AI + Game
Includes: Combat, Food, Inventory, NPCs, Quests, Skills, Crafting, Save/Load
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

app = FastAPI(title="Najika API", version="3.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# IN-MEMORY STORAGE (Session-based, replace with DB later)
# ═══════════════════════════════════════════════════════════════

game_state = {
    "player": {
        "health": 100,
        "maxHealth": 100,
        "mana": 100,
        "maxMana": 100,
        "stamina": 100,
        "maxStamina": 100,
        "gold": 100,
        "level": 1,
        "xp": 0,
        "position": {"x": 0, "y": 0, "z": 0}
    },
    "inventory": {
        "items": [],
        "equipment": {
            "weapon_left": None,
            "weapon_right": None,
            "armor_head": None,
            "armor_chest": None,
            "armor_legs": None,
            "accessory_1": None,
            "accessory_2": None
        }
    },
    "quests": {
        "active": [],
        "completed": []
    },
    "skills": {},
    "buffs": [],
    "npcs": {},
    "combat_history": []
}

# ═══════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════

class ChatMessage(BaseModel):
    message: str
    mode: str = "public"  # public or private

class GameAction(BaseModel):
    action_type: str
    data: dict

# Combat Models
class CombatAction(BaseModel):
    action: str  # "attack_left", "attack_right", "attack_both", "dodge", "block", "parry"
    enemy_id: Optional[str] = None
    hand: Optional[str] = None

class CombatResult(BaseModel):
    success: bool
    damage: int
    player_health: int
    enemy_health: int
    message: str
    loot: Optional[List[Dict]] = None

# Inventory Models
class InventoryItem(BaseModel):
    id: str
    type: str  # "food", "weapon", "armor", "material", "quest"
    name: str
    count: int = 1
    stats: Optional[Dict[str, Any]] = None

class InventoryAction(BaseModel):
    action: str  # "add", "remove", "use", "equip", "unequip"
    item_id: Optional[str] = None
    item_data: Optional[Dict[str, Any]] = None
    slot: Optional[str] = None

# Food Models
class FoodConsume(BaseModel):
    food_id: str
    player_stats: Dict[str, int]

# Quest Models
class QuestUpdate(BaseModel):
    quest_id: str
    objective_index: int
    amount: int = 1

class QuestComplete(BaseModel):
    quest_id: str

# Skill Models
class SkillUse(BaseModel):
    skill_id: str
    target_id: Optional[str] = None

class SkillLevelUp(BaseModel):
    skill_id: str
    xp_gained: int

# Crafting Models
class CraftingAction(BaseModel):
    recipe_id: str
    materials: List[Dict[str, Any]]

# Save/Load Models
class SaveGameData(BaseModel):
    player: Dict[str, Any]
    inventory: Dict[str, Any]
    quests: Dict[str, Any]
    skills: Dict[str, Any]
    timestamp: str

class LoadGameRequest(BaseModel):
    save_id: Optional[str] = "latest"

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "3.0",
        "najika": "Ready to serve Kuja! 💥",
        "systems": [
            "combat", "food", "inventory", "quests", "skills",
            "crafting", "npcs", "save/load"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_backend": "ollama" if os.getenv("USE_OLLAMA") == "true" else "llama.cpp",
        "chromadb": "connected",
        "game_systems": "operational"
    }

@app.post("/chat")
async def chat(message: ChatMessage):
    """
    Main chat endpoint for Najika
    """
    # TODO: Implement AI response logic
    return {
        "response": "Kuja! Ich bin noch nicht vollständig implementiert, aber ich bin hier! 💥",
        "mode": message.mode,
        "emotion": "excited"
    }

# ═══════════════════════════════════════════════════════════════
# GAME STATE ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/game/state")
async def get_game_state():
    """Get complete game state"""
    return game_state

@app.get("/game/player")
async def get_player_state():
    """Get player stats"""
    return game_state["player"]

@app.post("/game/player/update")
async def update_player_state(updates: Dict[str, Any]):
    """Update player stats"""
    for key, value in updates.items():
        if key in game_state["player"]:
            game_state["player"][key] = value
    return {"success": True, "player": game_state["player"]}

# ═══════════════════════════════════════════════════════════════
# COMBAT ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.post("/combat/action")
async def combat_action(action: CombatAction):
    """Execute combat action"""
    import random

    # Simple combat simulation
    damage = 0
    if action.action in ["attack_left", "attack_right"]:
        damage = random.randint(10, 30)
    elif action.action == "attack_both":
        damage = random.randint(25, 50)

    enemy_health = random.randint(50, 150)  # Placeholder
    player_health = game_state["player"]["health"]

    result = {
        "success": True,
        "damage": damage,
        "player_health": player_health,
        "enemy_health": max(0, enemy_health - damage),
        "message": f"Du hast {damage} Schaden verursacht!"
    }

    # Add to combat history
    game_state["combat_history"].append({
        "action": action.action,
        "damage": damage,
        "timestamp": datetime.now().isoformat()
    })

    return result

@app.get("/combat/history")
async def get_combat_history(limit: int = 10):
    """Get recent combat history"""
    return game_state["combat_history"][-limit:]

# ═══════════════════════════════════════════════════════════════
# INVENTORY ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/inventory")
async def get_inventory():
    """Get player inventory"""
    return game_state["inventory"]

@app.post("/inventory/action")
async def inventory_action(action: InventoryAction):
    """Perform inventory action"""
    if action.action == "add":
        game_state["inventory"]["items"].append(action.item_data)
        return {"success": True, "message": "Item hinzugefügt"}

    elif action.action == "remove":
        game_state["inventory"]["items"] = [
            item for item in game_state["inventory"]["items"]
            if item.get("id") != action.item_id
        ]
        return {"success": True, "message": "Item entfernt"}

    elif action.action == "equip":
        game_state["inventory"]["equipment"][action.slot] = action.item_data
        return {"success": True, "message": f"Item equipped in {action.slot}"}

    elif action.action == "unequip":
        game_state["inventory"]["equipment"][action.slot] = None
        return {"success": True, "message": f"Item unequipped from {action.slot}"}

    return {"success": False, "message": "Unknown action"}

@app.get("/inventory/equipment")
async def get_equipment():
    """Get equipped items"""
    return game_state["inventory"]["equipment"]

# ═══════════════════════════════════════════════════════════════
# FOOD/BUFF ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.post("/food/consume")
async def consume_food(food: FoodConsume):
    """Consume food and apply buffs"""
    buff = {
        "id": f"buff_{food.food_id}_{datetime.now().timestamp()}",
        "food_id": food.food_id,
        "start_time": datetime.now().isoformat(),
        "effects": {}
    }

    game_state["buffs"].append(buff)

    # Update player stats
    for stat, value in food.player_stats.items():
        if stat in game_state["player"]:
            game_state["player"][stat] = min(
                game_state["player"][stat] + value,
                game_state["player"].get(f"max{stat.capitalize()}", 100)
            )

    return {
        "success": True,
        "message": f"Food consumed: {food.food_id}",
        "active_buffs": len(game_state["buffs"])
    }

@app.get("/food/buffs")
async def get_active_buffs():
    """Get active buffs"""
    return game_state["buffs"]

# ═══════════════════════════════════════════════════════════════
# QUEST ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/quests")
async def get_quests():
    """Get all quests"""
    return game_state["quests"]

@app.post("/quests/update")
async def update_quest(update: QuestUpdate):
    """Update quest progress"""
    for quest in game_state["quests"]["active"]:
        if quest.get("id") == update.quest_id:
            if "progress" not in quest:
                quest["progress"] = {}
            quest["progress"][update.objective_index] = update.amount

            return {
                "success": True,
                "message": f"Quest {update.quest_id} updated",
                "quest": quest
            }

    return {"success": False, "message": "Quest not found"}

@app.post("/quests/complete")
async def complete_quest(complete: QuestComplete):
    """Complete a quest"""
    quest = None
    for q in game_state["quests"]["active"]:
        if q.get("id") == complete.quest_id:
            quest = q
            break

    if quest:
        game_state["quests"]["active"].remove(quest)
        game_state["quests"]["completed"].append({
            **quest,
            "completed_at": datetime.now().isoformat()
        })

        return {
            "success": True,
            "message": f"Quest {complete.quest_id} abgeschlossen!",
            "rewards": quest.get("rewards", {})
        }

    return {"success": False, "message": "Quest not found"}

@app.post("/quests/start")
async def start_quest(quest_data: Dict[str, Any]):
    """Start a new quest"""
    game_state["quests"]["active"].append({
        **quest_data,
        "started_at": datetime.now().isoformat()
    })
    return {"success": True, "message": "Quest gestartet"}

# ═══════════════════════════════════════════════════════════════
# SKILL ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/skills")
async def get_skills():
    """Get all skills"""
    return game_state["skills"]

@app.post("/skills/use")
async def use_skill(skill: SkillUse):
    """Use a skill"""
    if skill.skill_id in game_state["skills"]:
        skill_data = game_state["skills"][skill.skill_id]

        # Check mana cost
        mana_cost = skill_data.get("mana_cost", 10)
        if game_state["player"]["mana"] >= mana_cost:
            game_state["player"]["mana"] -= mana_cost

            return {
                "success": True,
                "message": f"Skill {skill.skill_id} verwendet!",
                "damage": skill_data.get("power", 50)
            }
        else:
            return {"success": False, "message": "Nicht genug Mana!"}

    return {"success": False, "message": "Skill nicht gefunden"}

@app.post("/skills/levelup")
async def skill_levelup(level: SkillLevelUp):
    """Level up a skill"""
    if level.skill_id in game_state["skills"]:
        skill = game_state["skills"][level.skill_id]
        skill["xp"] = skill.get("xp", 0) + level.xp_gained

        # Level up logic
        xp_required = 100 * (skill.get("level", 1) ** 1.5)
        if skill["xp"] >= xp_required:
            skill["level"] = skill.get("level", 1) + 1
            skill["xp"] = 0
            skill["power"] = skill.get("power", 50) + 5

            return {
                "success": True,
                "message": f"Skill {level.skill_id} Level UP!",
                "new_level": skill["level"]
            }

    return {"success": True, "message": "XP hinzugefügt"}

@app.post("/skills/learn")
async def learn_skill(skill_data: Dict[str, Any]):
    """Learn a new skill"""
    skill_id = skill_data.get("id")
    game_state["skills"][skill_id] = {
        **skill_data,
        "learned_at": datetime.now().isoformat()
    }
    return {"success": True, "message": f"Skill {skill_id} gelernt!"}

# ═══════════════════════════════════════════════════════════════
# CRAFTING ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.post("/crafting/craft")
async def craft_item(craft: CraftingAction):
    """Craft an item"""
    # Define crafting recipes
    recipes = {
        "wooden_sword": {
            "name": "Wooden Sword",
            "type": "weapon",
            "materials": [
                {"id": "wood", "count": 5},
                {"id": "rope", "count": 2}
            ],
            "result": {
                "id": "wooden_sword",
                "name": "Wooden Sword",
                "type": "weapon",
                "stats": {"attack": 10, "durability": 50}
            }
        },
        "health_potion": {
            "name": "Health Potion",
            "type": "consumable",
            "materials": [
                {"id": "herb", "count": 3},
                {"id": "water", "count": 1}
            ],
            "result": {
                "id": "health_potion",
                "name": "Health Potion",
                "type": "food",
                "stats": {"health_restore": 50}
            }
        },
        "leather_armor": {
            "name": "Leather Armor",
            "type": "armor",
            "materials": [
                {"id": "leather", "count": 8},
                {"id": "thread", "count": 4}
            ],
            "result": {
                "id": "leather_armor",
                "name": "Leather Armor",
                "type": "armor",
                "stats": {"defense": 15, "durability": 100}
            }
        }
    }

    # Check if recipe exists
    if craft.recipe_id not in recipes:
        return {
            "success": False,
            "message": f"Rezept {craft.recipe_id} nicht gefunden",
            "error": "unknown_recipe"
        }

    recipe = recipes[craft.recipe_id]

    # Check if player has required materials
    inventory_items = game_state["inventory"]["items"]

    # Count available materials
    material_counts = {}
    for item in inventory_items:
        item_id = item.get("id")
        item_count = item.get("count", 1)
        material_counts[item_id] = material_counts.get(item_id, 0) + item_count

    # Check if all materials are available
    missing_materials = []
    for material in recipe["materials"]:
        mat_id = material["id"]
        mat_count = material["count"]
        available = material_counts.get(mat_id, 0)

        if available < mat_count:
            missing_materials.append({
                "id": mat_id,
                "required": mat_count,
                "available": available,
                "missing": mat_count - available
            })

    if missing_materials:
        return {
            "success": False,
            "message": "Nicht genug Materialien!",
            "missing_materials": missing_materials,
            "error": "insufficient_materials"
        }

    # Remove materials from inventory
    for material in recipe["materials"]:
        mat_id = material["id"]
        mat_count = material["count"]
        remaining = mat_count

        # Remove from inventory
        game_state["inventory"]["items"] = [
            item for item in game_state["inventory"]["items"]
            if not (item.get("id") == mat_id and (remaining := remaining - item.get("count", 1)) >= 0)
        ]

    # Add crafted item to inventory
    crafted_item = {
        **recipe["result"],
        "count": 1,
        "crafted_at": datetime.now().isoformat()
    }
    game_state["inventory"]["items"].append(crafted_item)

    return {
        "success": True,
        "message": f"{recipe['name']} erfolgreich gecraftet!",
        "result": crafted_item,
        "materials_used": recipe["materials"],
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# SAVE/LOAD ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.post("/save")
async def save_game(save_data: SaveGameData):
    """Save game state"""
    save_file = f"backend/saves/save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    os.makedirs("backend/saves", exist_ok=True)

    with open(save_file, 'w') as f:
        json.dump({
            "player": save_data.player,
            "inventory": save_data.inventory,
            "quests": save_data.quests,
            "skills": save_data.skills,
            "timestamp": save_data.timestamp
        }, f, indent=2)

    return {
        "success": True,
        "message": "Spiel gespeichert!",
        "save_file": save_file
    }

@app.post("/load")
async def load_game(load: LoadGameRequest):
    """Load game state"""
    # Find latest save
    save_dir = "backend/saves"
    if os.path.exists(save_dir):
        saves = sorted(os.listdir(save_dir), reverse=True)
        if saves:
            save_file = os.path.join(save_dir, saves[0])
            with open(save_file, 'r') as f:
                loaded_data = json.load(f)

            # Update game state
            game_state["player"].update(loaded_data.get("player", {}))
            game_state["inventory"].update(loaded_data.get("inventory", {}))
            game_state["quests"].update(loaded_data.get("quests", {}))
            game_state["skills"].update(loaded_data.get("skills", {}))

            return {
                "success": True,
                "message": "Spiel geladen!",
                "save_file": save_file
            }

    return {"success": False, "message": "Kein Speicherstand gefunden"}

@app.get("/saves")
async def list_saves():
    """List all save files"""
    save_dir = "backend/saves"
    if os.path.exists(save_dir):
        saves = sorted(os.listdir(save_dir), reverse=True)
        return {"saves": saves}
    return {"saves": []}

# ═══════════════════════════════════════════════════════════════
# NPC ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/npcs")
async def get_npcs():
    """Get all NPCs"""
    return game_state["npcs"]

@app.post("/npcs/interact")
async def interact_npc(npc_data: Dict[str, Any]):
    """Interact with an NPC"""
    npc_id = npc_data.get("npc_id")
    action = npc_data.get("action", "talk")

    return {
        "success": True,
        "message": f"Interacting with NPC {npc_id}",
        "dialogue": "Hallo, Kuja! Wie kann ich dir helfen?",
        "options": ["Shop", "Quest", "Tschüss"]
    }

@app.post("/game/action")
async def game_action(action: GameAction):
    """
    Handle generic game actions
    """
    return {
        "success": True,
        "result": f"Action {action.action_type} processed",
        "data": action.data
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket for real-time communication
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Najika: {data}")
    except:
        pass

# ═══════════════════════════════════════════════════════════════
# RUN SERVER
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = int(os.getenv("BACKEND_PORT", 5000))
    
    print("🌟 Najika Backend starting...")
    print(f"🔗 Listening on {host}:{port}")
    
    uvicorn.run(app, host=host, port=port)
