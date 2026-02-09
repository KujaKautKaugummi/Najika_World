"""
Slime Arena API - Najika World
================================

Backend API für Schleim-Arena System
Basierend auf SCHLEIM_ARENA_DESIGN.md

Features:
- 1v1 Normal Duels
- 1v1 mit Finisher System
- Tournament System (Single-Elimination)
- Fame/Reputation System
- Combat Control Modes (KI, Manual, Cheer)

Author: Claude Code (CLI)
Date: 2026-01-18
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Data file paths
SLIME_ARENA_DATA_DIR = Path("backend/saves/slime_arena")
SLIME_ARENA_DATA_DIR.mkdir(parents=True, exist_ok=True)

DUEL_HISTORY_FILE = SLIME_ARENA_DATA_DIR / "duel_history.json"
TOURNAMENT_FILE = SLIME_ARENA_DATA_DIR / "tournaments.json"
FAME_FILE = SLIME_ARENA_DATA_DIR / "fame_rankings.json"
ACTIVE_DUELS_FILE = SLIME_ARENA_DATA_DIR / "active_duels.json"

# ============================================================================
# FINISHER DATABASE
# ============================================================================

FINISHERS = {
    "inferno_burst": {
        "id": "inferno_burst",
        "name": "Inferno Burst",
        "description": "Standard, spektakulär",
        "icon": "🔥",
        "fame_bonus": 10,
        "animation_duration": 3
    },
    "mega_explosion": {
        "id": "mega_explosion",
        "name": "Mega Explosion",
        "description": "Extra brutal",
        "icon": "💣",
        "fame_bonus": 15,
        "animation_duration": 4
    },
    "flame_stomp": {
        "id": "flame_stomp",
        "name": "Flame Stomp",
        "description": "Demütigend",
        "icon": "👟",
        "fame_bonus": 12,
        "animation_duration": 3
    },
    "mercy": {
        "id": "mercy",
        "name": "Mercy",
        "description": "Gnädig, nur HP-Entzug",
        "icon": "🕊️",
        "fame_bonus": 5,
        "animation_duration": 2
    }
}

# ============================================================================
# FAME SYSTEM
# ============================================================================

FAME_TITLES = [
    {"title": "Anfänger", "min_fame": 0, "max_fame": 99, "icon": "🐣"},
    {"title": "Kämpfer", "min_fame": 100, "max_fame": 499, "icon": "⚔️"},
    {"title": "Veteran", "min_fame": 500, "max_fame": 999, "icon": "🛡️"},
    {"title": "Champion", "min_fame": 1000, "max_fame": 2499, "icon": "👑"},
    {"title": "Legende", "min_fame": 2500, "max_fame": 999999, "icon": "⭐"}
]

def get_fame_title(fame_points: int) -> Dict:
    """Get player title based on fame points"""
    for title_data in FAME_TITLES:
        if title_data["min_fame"] <= fame_points <= title_data["max_fame"]:
            return title_data
    return FAME_TITLES[0]  # Default to Anfänger

# ============================================================================
# DATA PERSISTENCE
# ============================================================================

def load_json_file(filepath: Path, default=None):
    """Load JSON file with error handling"""
    if default is None:
        default = {}

    if not filepath.exists():
        return default

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[SlimeArena] Error loading {filepath}, using default")
        return default

def save_json_file(filepath: Path, data):
    """Save JSON file with error handling"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[SlimeArena] Error saving {filepath}: {e}")
        return False

def load_duel_history():
    """Load duel history"""
    return load_json_file(DUEL_HISTORY_FILE, [])

def save_duel_history(history):
    """Save duel history"""
    return save_json_file(DUEL_HISTORY_FILE, history)

def load_fame_rankings():
    """Load fame rankings"""
    return load_json_file(FAME_FILE, {})

def save_fame_rankings(rankings):
    """Save fame rankings"""
    return save_json_file(FAME_FILE, rankings)

def load_tournaments():
    """Load tournaments"""
    return load_json_file(TOURNAMENT_FILE, {"active": None, "history": []})

def save_tournaments(tournaments):
    """Save tournaments"""
    return save_json_file(TOURNAMENT_FILE, tournaments)

def load_active_duels():
    """Load active duels"""
    return load_json_file(ACTIVE_DUELS_FILE, {})

def save_active_duels(duels):
    """Save active duels"""
    return save_json_file(ACTIVE_DUELS_FILE, duels)

# ============================================================================
# SLIME STATS
# ============================================================================

def get_slime_stats(player_id: int) -> Dict:
    """Get player's slime stats (simplified for now)"""
    # TODO: Integrate with actual slime companion system
    return {
        "name": f"Slime_{player_id}",
        "hp": 100,
        "maxHp": 100,
        "attack": 20,
        "defense": 15,
        "color": "#00ff00",
        "level": 1
    }

# ============================================================================
# API ENDPOINTS
# ============================================================================

def api_start_duel(player_id: int, mode: str = "normal", opponent_id: Optional[int] = None,
                   is_vs_npc: bool = False, npc_name: Optional[str] = None) -> Dict:
    """
    POST /api/slime-arena/start-duel
    Start a new slime duel

    Modes: 'normal', 'finisher', 'tournament'
    """
    # Generate duel ID
    duel_id = f"duel_{int(datetime.now().timestamp() * 1000)}"

    # Get slime stats
    player_slime = get_slime_stats(player_id)

    # Setup opponent
    if is_vs_npc or opponent_id is None:
        opponent_slime = {
            "name": npc_name or "Wilder Schleim",
            "hp": random.randint(70, 90),
            "maxHp": random.randint(70, 90),
            "attack": random.randint(15, 22),
            "defense": random.randint(10, 18),
            "color": f"#{random.randint(0, 0xFFFFFF):06x}",
            "level": 1,
            "is_npc": True
        }
    else:
        opponent_slime = get_slime_stats(opponent_id)

    # Create duel state
    duel_state = {
        "duel_id": duel_id,
        "mode": mode,
        "player_id": player_id,
        "opponent_id": opponent_id,
        "is_vs_npc": is_vs_npc,
        "player_slime": player_slime,
        "opponent_slime": opponent_slime,
        "current_round": 1,
        "player_buffs": {},
        "opponent_buffs": {},
        "combat_log": [],
        "started_at": datetime.now().isoformat(),
        "status": "active"
    }

    # Save to active duels
    active_duels = load_active_duels()
    active_duels[duel_id] = duel_state
    save_active_duels(active_duels)

    return {
        "success": True,
        "duel_id": duel_id,
        "duel_state": duel_state
    }

def api_duel_action(duel_id: str, action_type: str, action_data: Dict) -> Dict:
    """
    POST /api/slime-arena/action
    Perform combat action

    action_type: 'attack', 'defend', 'special', 'cheer', 'auto'
    """
    active_duels = load_active_duels()

    if duel_id not in active_duels:
        return {"success": False, "error": "Duel not found"}

    duel = active_duels[duel_id]

    # Process player action
    result = process_combat_action(duel, action_type, action_data, is_player=True)

    # Enemy turn (if player didn't end the fight)
    if duel["opponent_slime"]["hp"] > 0:
        enemy_action = get_enemy_action(duel)
        enemy_result = process_combat_action(duel, enemy_action["type"], enemy_action["data"], is_player=False)
        result["enemy_action"] = enemy_result

    # Update round
    duel["current_round"] += 1

    # Check for battle end
    if duel["player_slime"]["hp"] <= 0 or duel["opponent_slime"]["hp"] <= 0:
        duel["status"] = "ended"
        winner_id = duel["player_id"] if duel["opponent_slime"]["hp"] <= 0 else (duel["opponent_id"] if not duel["is_vs_npc"] else None)
        result["battle_ended"] = True
        result["winner_id"] = winner_id
        result["show_finisher"] = duel["mode"] in ["finisher", "tournament"]

    # Update duel buffs durations
    update_buff_durations(duel)

    # Save updated duel
    active_duels[duel_id] = duel
    save_active_duels(active_duels)

    return {
        "success": True,
        "result": result,
        "duel_state": duel
    }

def process_combat_action(duel: Dict, action_type: str, action_data: Dict, is_player: bool) -> Dict:
    """Process a single combat action"""
    attacker_key = "player_slime" if is_player else "opponent_slime"
    defender_key = "opponent_slime" if is_player else "player_slime"
    buffs_key = "player_buffs" if is_player else "opponent_buffs"

    attacker = duel[attacker_key]
    defender = duel[defender_key]
    buffs = duel[buffs_key]

    result = {
        "action": action_type,
        "attacker": attacker["name"],
        "defender": defender["name"],
        "damage": 0,
        "message": ""
    }

    if action_type == "attack":
        # Calculate damage
        base_damage = attacker["attack"]

        # Apply buffs
        if "attack" in buffs and buffs["attack"] > 0:
            base_damage *= 1.10  # +10% from cheer

        # Random variance (80-120%)
        damage = int(base_damage * random.uniform(0.8, 1.2))

        # Apply defense
        if "defend" in buffs and buffs["defend"] > 0:
            damage = int(damage * 0.5)  # 50% reduction if defending

        # Apply damage
        defender["hp"] = max(0, defender["hp"] - damage)

        result["damage"] = damage
        result["message"] = f"{attacker['name']} greift an! {damage} Schaden!"

    elif action_type == "defend":
        # Set defending flag
        buffs["defend"] = 1
        result["message"] = f"{attacker['name']} verteidigt!"

    elif action_type == "special":
        # Special attack (1.5x damage)
        damage = int(attacker["attack"] * 1.5 * random.uniform(0.8, 1.2))
        defender["hp"] = max(0, defender["hp"] - damage)

        result["damage"] = damage
        result["message"] = f"{attacker['name']} verwendet Spezial-Attacke! {damage} Schaden!"

    elif action_type == "cheer":
        # Apply cheer buff
        cheer_type = action_data.get("cheer_type", "attack")
        buffs[cheer_type] = 3  # Lasts 3 rounds

        cheer_messages = {
            "attack": f"💪 'Los!' - {attacker['name']}'s Angriff erhöht!",
            "defend": f"🛡️ 'Defend!' - {attacker['name']}'s Verteidigung erhöht!",
            "combo": f"💥 'Combo!' - {attacker['name']} bereitet Combo vor!",
            "focus": f"🎯 'Focus!' - {attacker['name']}'s Genauigkeit erhöht!"
        }

        result["message"] = cheer_messages.get(cheer_type, f"{attacker['name']} wird angefeuert!")

        # Cheer mode also attacks
        damage = int(attacker["attack"] * random.uniform(0.8, 1.2))
        defender["hp"] = max(0, defender["hp"] - damage)
        result["damage"] = damage
        result["message"] += f" Angriff: {damage} Schaden!"

    # Add to combat log
    duel["combat_log"].append(result["message"])

    return result

def update_buff_durations(duel: Dict):
    """Decrease buff durations"""
    for buffs_key in ["player_buffs", "opponent_buffs"]:
        buffs = duel[buffs_key]
        for buff in list(buffs.keys()):
            buffs[buff] -= 1
            if buffs[buff] <= 0:
                del buffs[buff]

def get_enemy_action(duel: Dict) -> Dict:
    """Get enemy AI action"""
    # Simple AI: Random action
    actions = ["attack", "defend", "special"]
    action = random.choice(actions)

    return {
        "type": action,
        "data": {}
    }

def api_execute_finisher(duel_id: str, finisher_id: str, winner_id: int) -> Dict:
    """
    POST /api/slime-arena/finisher
    Execute finishing move
    """
    active_duels = load_active_duels()

    if duel_id not in active_duels:
        return {"success": False, "error": "Duel not found"}

    duel = active_duels[duel_id]

    if finisher_id not in FINISHERS:
        return {"success": False, "error": "Invalid finisher"}

    finisher = FINISHERS[finisher_id]

    # Record finisher
    duel["finisher_used"] = finisher_id
    duel["finisher_data"] = finisher

    # Calculate rewards
    rewards = calculate_duel_rewards(duel, winner_id, finisher)

    # Update fame
    if winner_id:
        update_fame(winner_id, rewards["fame_gained"])

    # Save to history
    save_duel_to_history(duel, winner_id, rewards)

    # Remove from active duels
    del active_duels[duel_id]
    save_active_duels(active_duels)

    return {
        "success": True,
        "finisher": finisher,
        "rewards": rewards,
        "animation_duration": finisher["animation_duration"]
    }

def calculate_duel_rewards(duel: Dict, winner_id: int, finisher: Optional[Dict] = None) -> Dict:
    """Calculate duel rewards"""
    mode = duel["mode"]

    # Base rewards by mode
    if mode == "normal":
        gold = random.randint(100, 500)
        xp = random.randint(50, 150)
        fame = 0
    elif mode == "finisher":
        gold = random.randint(200, 1000)
        xp = random.randint(100, 300)
        fame = 10

        # Bonus for finisher
        if finisher:
            fame += finisher["fame_bonus"]
    elif mode == "tournament":
        gold = random.randint(500, 2000)
        xp = random.randint(200, 500)
        fame = 25
    else:
        gold = 0
        xp = 0
        fame = 0

    return {
        "gold": gold,
        "xp": xp,
        "fame_gained": fame
    }

def update_fame(player_id: int, fame_gained: int):
    """Update player fame"""
    rankings = load_fame_rankings()

    player_key = str(player_id)
    if player_key not in rankings:
        rankings[player_key] = {
            "player_id": player_id,
            "fame": 0,
            "wins": 0,
            "losses": 0,
            "finishers_used": 0
        }

    rankings[player_key]["fame"] += fame_gained

    save_fame_rankings(rankings)

def save_duel_to_history(duel: Dict, winner_id: Optional[int], rewards: Dict):
    """Save completed duel to history"""
    history = load_duel_history()

    history_entry = {
        "duel_id": duel["duel_id"],
        "mode": duel["mode"],
        "player_id": duel["player_id"],
        "opponent_id": duel["opponent_id"],
        "is_vs_npc": duel["is_vs_npc"],
        "winner_id": winner_id,
        "rounds": duel["current_round"],
        "finisher_used": duel.get("finisher_used"),
        "rewards": rewards,
        "timestamp": datetime.now().isoformat()
    }

    history.append(history_entry)

    # Keep last 1000 duels
    if len(history) > 1000:
        history = history[-1000:]

    save_duel_history(history)

def api_get_leaderboard(limit: int = 100) -> Dict:
    """
    GET /api/slime-arena/leaderboard
    Get fame rankings leaderboard
    """
    rankings = load_fame_rankings()

    # Convert to list and sort by fame
    leaderboard = sorted(
        rankings.values(),
        key=lambda x: x["fame"],
        reverse=True
    )[:limit]

    # Add titles
    for entry in leaderboard:
        title_data = get_fame_title(entry["fame"])
        entry["title"] = title_data["title"]
        entry["title_icon"] = title_data["icon"]

    return {
        "success": True,
        "leaderboard": leaderboard
    }

def api_get_player_stats(player_id: int) -> Dict:
    """
    GET /api/slime-arena/stats/{player_id}
    Get player arena stats
    """
    rankings = load_fame_rankings()
    history = load_duel_history()

    player_key = str(player_id)

    # Get or create player stats
    if player_key not in rankings:
        player_stats = {
            "player_id": player_id,
            "fame": 0,
            "wins": 0,
            "losses": 0,
            "finishers_used": 0
        }
    else:
        player_stats = rankings[player_key]

    # Calculate stats from history
    player_duels = [d for d in history if d["player_id"] == player_id or d["opponent_id"] == player_id]
    player_stats["total_duels"] = len(player_duels)
    player_stats["wins"] = len([d for d in player_duels if d["winner_id"] == player_id])
    player_stats["losses"] = len([d for d in player_duels if d["winner_id"] != player_id and d["winner_id"] is not None])

    # Get title
    title_data = get_fame_title(player_stats["fame"])
    player_stats["title"] = title_data["title"]
    player_stats["title_icon"] = title_data["icon"]

    return {
        "success": True,
        "stats": player_stats
    }

def api_get_duel_history(player_id: int, limit: int = 20) -> Dict:
    """
    GET /api/slime-arena/history/{player_id}
    Get player's duel history
    """
    history = load_duel_history()

    # Filter for player
    player_history = [
        d for d in history
        if d["player_id"] == player_id or d["opponent_id"] == player_id
    ]

    # Sort by newest first
    player_history.sort(key=lambda x: x["timestamp"], reverse=True)

    # Limit results
    player_history = player_history[:limit]

    return {
        "success": True,
        "history": player_history
    }

# ============================================================================
# TOURNAMENT SYSTEM (TODO: Expand later)
# ============================================================================

def api_register_tournament(player_id: int, entry_fee: int = 500) -> Dict:
    """
    POST /api/slime-arena/tournament/register
    Register for tournament
    """
    tournaments = load_tournaments()

    # Check if tournament is active
    if tournaments["active"] is None:
        return {"success": False, "error": "No active tournament"}

    active_tournament = tournaments["active"]

    # Check if player already registered
    if player_id in active_tournament["participants"]:
        return {"success": False, "error": "Already registered"}

    # Register player
    active_tournament["participants"].append(player_id)

    save_tournaments(tournaments)

    return {
        "success": True,
        "tournament": active_tournament
    }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def api_get_finishers() -> Dict:
    """
    GET /api/slime-arena/finishers
    Get all available finishers
    """
    return {
        "success": True,
        "finishers": list(FINISHERS.values())
    }

def api_get_active_duel(player_id: int) -> Dict:
    """
    GET /api/slime-arena/active/{player_id}
    Get player's active duel if any
    """
    active_duels = load_active_duels()

    # Find player's active duel
    for duel_id, duel in active_duels.items():
        if duel["player_id"] == player_id and duel["status"] == "active":
            return {
                "success": True,
                "has_active_duel": True,
                "duel": duel
            }

    return {
        "success": True,
        "has_active_duel": False
    }

# Export all API functions
__all__ = [
    'api_start_duel',
    'api_duel_action',
    'api_execute_finisher',
    'api_get_leaderboard',
    'api_get_player_stats',
    'api_get_duel_history',
    'api_register_tournament',
    'api_get_finishers',
    'api_get_active_duel',
    'FINISHERS',
    'FAME_TITLES',
    'get_fame_title'
]
