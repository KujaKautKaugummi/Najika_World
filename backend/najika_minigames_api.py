"""
NAJIKA MINIGAMES API - Card Game + Dice Monsters
=================================================

Integrierte APIs für:
- Triple Triad Card Game (Hearthstone-Style)
- Dungeon Dice Monsters (Yu-Gi-Oh DDM)

JSON-basiert (kein SQLAlchemy) für Kompatibilität mit SimpleHTTPRequestHandler

Copyright: Najika World
Author: Claude Code
Date: 2025-12-17
"""

import os
import json
import time
import random
from pathlib import Path

# ===== DATA PATHS =====
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "digivice" / "data"
MINIGAMES_DATA = DATA_DIR / "minigames"

# Ensure directories exist
MINIGAMES_DATA.mkdir(parents=True, exist_ok=True)

# ===== CARD GAME DATA =====

# 52 Triple Triad Cards (Fantasy Western Theme)
CARDS_DATABASE = {
    # Fire Gunslingers (Red)
    1: {"id": 1, "name": "Wüsten-Revolverheld", "faction": "fire_gunslingers", "rarity": "common",
        "stats": {"top": 3, "right": 5, "bottom": 2, "left": 4}, "element": "fire"},
    2: {"id": 2, "name": "Flammen-Scharfschütze", "faction": "fire_gunslingers", "rarity": "uncommon",
        "stats": {"top": 4, "right": 6, "bottom": 3, "left": 4}, "element": "fire"},
    3: {"id": 3, "name": "Dynamit-Desperado", "faction": "fire_gunslingers", "rarity": "rare",
        "stats": {"top": 5, "right": 7, "bottom": 4, "left": 3}, "element": "fire"},
    4: {"id": 4, "name": "Inferno-Marshal", "faction": "fire_gunslingers", "rarity": "epic",
        "stats": {"top": 6, "right": 8, "bottom": 5, "left": 6}, "element": "fire"},
    5: {"id": 5, "name": "Phönix-Outlaw", "faction": "fire_gunslingers", "rarity": "legendary",
        "stats": {"top": 8, "right": 9, "bottom": 7, "left": 8}, "element": "fire", "special": "resurrect"},

    # Ice Mages (Blue)
    6: {"id": 6, "name": "Frost-Lehrling", "faction": "ice_mages", "rarity": "common",
        "stats": {"top": 4, "right": 3, "bottom": 5, "left": 2}, "element": "ice"},
    7: {"id": 7, "name": "Blizzard-Hexer", "faction": "ice_mages", "rarity": "uncommon",
        "stats": {"top": 5, "right": 4, "bottom": 6, "left": 3}, "element": "ice"},
    8: {"id": 8, "name": "Eisberg-Beschwörer", "faction": "ice_mages", "rarity": "rare",
        "stats": {"top": 6, "right": 5, "bottom": 7, "left": 4}, "element": "ice"},
    9: {"id": 9, "name": "Gletscher-Erzmagier", "faction": "ice_mages", "rarity": "epic",
        "stats": {"top": 7, "right": 6, "bottom": 8, "left": 5}, "element": "ice"},
    10: {"id": 10, "name": "Eis-Lich König", "faction": "ice_mages", "rarity": "legendary",
         "stats": {"top": 9, "right": 8, "bottom": 9, "left": 7}, "element": "ice", "special": "freeze"},

    # Earth Warriors (Brown)
    11: {"id": 11, "name": "Minenarbeiter", "faction": "earth_warriors", "rarity": "common",
         "stats": {"top": 5, "right": 2, "bottom": 4, "left": 3}, "element": "earth"},
    12: {"id": 12, "name": "Steingolem", "faction": "earth_warriors", "rarity": "uncommon",
         "stats": {"top": 6, "right": 3, "bottom": 5, "left": 4}, "element": "earth"},
    13: {"id": 13, "name": "Kristall-Wächter", "faction": "earth_warriors", "rarity": "rare",
         "stats": {"top": 7, "right": 4, "bottom": 6, "left": 5}, "element": "earth"},
    14: {"id": 14, "name": "Titan der Tiefe", "faction": "earth_warriors", "rarity": "epic",
         "stats": {"top": 8, "right": 5, "bottom": 7, "left": 6}, "element": "earth"},
    15: {"id": 15, "name": "Götterfels-Avatar", "faction": "earth_warriors", "rarity": "legendary",
         "stats": {"top": 9, "right": 7, "bottom": 8, "left": 9}, "element": "earth", "special": "wall"},

    # Wind Rangers (Green)
    16: {"id": 16, "name": "Präriejäger", "faction": "wind_rangers", "rarity": "common",
         "stats": {"top": 2, "right": 4, "bottom": 3, "left": 5}, "element": "wind"},
    17: {"id": 17, "name": "Sturmreiter", "faction": "wind_rangers", "rarity": "uncommon",
         "stats": {"top": 3, "right": 5, "bottom": 4, "left": 6}, "element": "wind"},
    18: {"id": 18, "name": "Tornado-Schütze", "faction": "wind_rangers", "rarity": "rare",
         "stats": {"top": 4, "right": 6, "bottom": 5, "left": 7}, "element": "wind"},
    19: {"id": 19, "name": "Blitz-Krieger", "faction": "wind_rangers", "rarity": "epic",
         "stats": {"top": 5, "right": 7, "bottom": 6, "left": 8}, "element": "wind"},
    20: {"id": 20, "name": "Sturmgott des Westens", "faction": "wind_rangers", "rarity": "legendary",
         "stats": {"top": 7, "right": 9, "bottom": 8, "left": 9}, "element": "wind", "special": "swap"},

    # Shadow Outlaws (Purple)
    21: {"id": 21, "name": "Taschendieb", "faction": "shadow_outlaws", "rarity": "common",
         "stats": {"top": 3, "right": 3, "bottom": 4, "left": 4}, "element": "shadow"},
    22: {"id": 22, "name": "Giftmischer", "faction": "shadow_outlaws", "rarity": "uncommon",
         "stats": {"top": 4, "right": 4, "bottom": 5, "left": 5}, "element": "shadow"},
    23: {"id": 23, "name": "Schatten-Assassine", "faction": "shadow_outlaws", "rarity": "rare",
         "stats": {"top": 5, "right": 5, "bottom": 6, "left": 6}, "element": "shadow"},
    24: {"id": 24, "name": "Nekromanten-Anführer", "faction": "shadow_outlaws", "rarity": "epic",
         "stats": {"top": 6, "right": 6, "bottom": 7, "left": 7}, "element": "shadow"},
    25: {"id": 25, "name": "Schattenfürst", "faction": "shadow_outlaws", "rarity": "legendary",
         "stats": {"top": 8, "right": 8, "bottom": 8, "left": 8}, "element": "shadow", "special": "flip"},

    # Light Paladins (Gold)
    26: {"id": 26, "name": "Akolyt", "faction": "light_paladins", "rarity": "common",
         "stats": {"top": 4, "right": 4, "bottom": 2, "left": 4}, "element": "light"},
    27: {"id": 27, "name": "Tempelritter", "faction": "light_paladins", "rarity": "uncommon",
         "stats": {"top": 5, "right": 5, "bottom": 3, "left": 5}, "element": "light"},
    28: {"id": 28, "name": "Heiler des Lichts", "faction": "light_paladins", "rarity": "rare",
         "stats": {"top": 6, "right": 6, "bottom": 4, "left": 6}, "element": "light"},
    29: {"id": 29, "name": "Erz-Paladin", "faction": "light_paladins", "rarity": "epic",
         "stats": {"top": 7, "right": 7, "bottom": 5, "left": 7}, "element": "light"},
    30: {"id": 30, "name": "Lichtkönig", "faction": "light_paladins", "rarity": "legendary",
         "stats": {"top": 9, "right": 9, "bottom": 6, "left": 9}, "element": "light", "special": "heal"},

    # Neutral (Western Creatures)
    31: {"id": 31, "name": "Präriehund", "faction": "neutral", "rarity": "common",
         "stats": {"top": 2, "right": 2, "bottom": 3, "left": 3}, "element": None},
    32: {"id": 32, "name": "Klapperschlange", "faction": "neutral", "rarity": "common",
         "stats": {"top": 3, "right": 2, "bottom": 2, "left": 4}, "element": None},
    33: {"id": 33, "name": "Wilder Mustang", "faction": "neutral", "rarity": "uncommon",
         "stats": {"top": 4, "right": 5, "bottom": 3, "left": 4}, "element": None},
    34: {"id": 34, "name": "Kaktus-Golem", "faction": "neutral", "rarity": "uncommon",
         "stats": {"top": 5, "right": 3, "bottom": 5, "left": 3}, "element": None},
    35: {"id": 35, "name": "Geisterbahn-Geist", "faction": "neutral", "rarity": "rare",
         "stats": {"top": 5, "right": 6, "bottom": 5, "left": 5}, "element": None},
    36: {"id": 36, "name": "Wüsten-Sphinx", "faction": "neutral", "rarity": "epic",
         "stats": {"top": 7, "right": 6, "bottom": 6, "left": 7}, "element": None},

    # Special: Najika World Exclusive
    37: {"id": 37, "name": "Najika (Explosions-Magier)", "faction": "special", "rarity": "legendary",
         "stats": {"top": 10, "right": 1, "bottom": 1, "left": 1}, "element": "explosion",
         "special": "explosion", "description": "EXPLOSION! Zerstört alle angrenzenden Karten"},
    38: {"id": 38, "name": "Najika (Slime-Form)", "faction": "special", "rarity": "legendary",
         "stats": {"top": 5, "right": 5, "bottom": 5, "left": 5}, "element": "slime",
         "special": "copy", "description": "Kopiert die Werte einer angrenzenden Karte"},
    39: {"id": 39, "name": "Götterfels-Wächter", "faction": "special", "rarity": "legendary",
         "stats": {"top": 9, "right": 9, "bottom": 9, "left": 9}, "element": "divine",
         "special": "unflippable", "description": "Kann nicht umgedreht werden"},
    40: {"id": 40, "name": "Schwarze Mühle", "faction": "special", "rarity": "epic",
         "stats": {"top": 6, "right": 6, "bottom": 6, "left": 6}, "element": "shadow",
         "special": "home", "description": "Alle Schatten-Karten +1"},
}

# ===== DICE MONSTERS DATABASE =====

DICE_MONSTERS_DATABASE = {
    # Fire Monsters
    1: {"id": 1, "name": "Feuer-Imp", "element": "fire", "rarity": "common", "monster_type": "beast",
        "atk": 10, "def": 10, "hp": 20, "summon_cost": 1, "dice_faces": [1,1,2,2,3,"summon"]},
    2: {"id": 2, "name": "Lava-Hund", "element": "fire", "rarity": "uncommon", "monster_type": "beast",
        "atk": 20, "def": 15, "hp": 30, "summon_cost": 2, "dice_faces": [1,2,2,3,3,"summon"]},
    3: {"id": 3, "name": "Inferno-Drache", "element": "fire", "rarity": "rare", "monster_type": "dragon",
        "atk": 35, "def": 25, "hp": 50, "summon_cost": 3, "dice_faces": [2,2,3,3,4,"summon"]},
    4: {"id": 4, "name": "Phönix", "element": "fire", "rarity": "legendary", "monster_type": "beast",
        "atk": 40, "def": 30, "hp": 60, "summon_cost": 4, "dice_faces": [3,3,4,4,5,"summon"],
        "special": "Wiedergeburt: Kehrt mit 50% HP zurück"},

    # Water Monsters
    5: {"id": 5, "name": "Wasser-Sprite", "element": "water", "rarity": "common", "monster_type": "mage",
        "atk": 8, "def": 12, "hp": 25, "summon_cost": 1, "dice_faces": [1,1,2,2,2,"summon"]},
    6: {"id": 6, "name": "Sumpf-Kreatur", "element": "water", "rarity": "uncommon", "monster_type": "beast",
        "atk": 18, "def": 22, "hp": 35, "summon_cost": 2, "dice_faces": [1,2,2,3,3,"summon"]},
    7: {"id": 7, "name": "Kraken", "element": "water", "rarity": "rare", "monster_type": "beast",
        "atk": 30, "def": 35, "hp": 55, "summon_cost": 3, "dice_faces": [2,3,3,4,4,"summon"]},
    8: {"id": 8, "name": "Leviathan", "element": "water", "rarity": "legendary", "monster_type": "dragon",
        "atk": 45, "def": 40, "hp": 70, "summon_cost": 4, "dice_faces": [3,4,4,5,5,"summon"],
        "special": "Tsunami: Schiebt alle Gegner 2 Felder"},

    # Earth Monsters
    9: {"id": 9, "name": "Erd-Wurm", "element": "earth", "rarity": "common", "monster_type": "beast",
        "atk": 12, "def": 8, "hp": 22, "summon_cost": 1, "dice_faces": [1,1,2,2,3,"summon"]},
    10: {"id": 10, "name": "Stein-Golem", "element": "earth", "rarity": "uncommon", "monster_type": "warrior",
         "atk": 15, "def": 30, "hp": 40, "summon_cost": 2, "dice_faces": [1,2,2,3,4,"summon"]},
    11: {"id": 11, "name": "Kristall-Titan", "element": "earth", "rarity": "rare", "monster_type": "warrior",
         "atk": 28, "def": 40, "hp": 60, "summon_cost": 3, "dice_faces": [2,3,3,4,5,"summon"]},
    12: {"id": 12, "name": "Erdbeben-Behemoth", "element": "earth", "rarity": "legendary", "monster_type": "beast",
         "atk": 50, "def": 50, "hp": 80, "summon_cost": 4, "dice_faces": [3,4,4,5,6,"summon"],
         "special": "Erdbeben: Alle Gegner verlieren 1 Bewegung"},

    # Wind Monsters
    13: {"id": 13, "name": "Wind-Fae", "element": "wind", "rarity": "common", "monster_type": "mage",
         "atk": 10, "def": 8, "hp": 18, "summon_cost": 1, "dice_faces": [1,2,2,2,3,"summon"]},
    14: {"id": 14, "name": "Sturm-Falke", "element": "wind", "rarity": "uncommon", "monster_type": "beast",
         "atk": 22, "def": 12, "hp": 28, "summon_cost": 2, "dice_faces": [2,2,3,3,4,"summon"]},
    15: {"id": 15, "name": "Tornado-Elemental", "element": "wind", "rarity": "rare", "monster_type": "mage",
         "atk": 32, "def": 20, "hp": 45, "summon_cost": 3, "dice_faces": [2,3,4,4,5,"summon"]},
    16: {"id": 16, "name": "Sturmgott", "element": "wind", "rarity": "legendary", "monster_type": "mage",
         "atk": 42, "def": 28, "hp": 55, "summon_cost": 4, "dice_faces": [3,4,5,5,6,"summon"],
         "special": "Blitz: Greift 2x an"},

    # Light Monsters
    17: {"id": 17, "name": "Licht-Wisp", "element": "light", "rarity": "common", "monster_type": "mage",
         "atk": 8, "def": 10, "hp": 20, "summon_cost": 1, "dice_faces": [1,1,2,2,3,"summon"]},
    18: {"id": 18, "name": "Engel-Wächter", "element": "light", "rarity": "uncommon", "monster_type": "warrior",
         "atk": 18, "def": 25, "hp": 35, "summon_cost": 2, "dice_faces": [1,2,3,3,4,"summon"]},
    19: {"id": 19, "name": "Seraph", "element": "light", "rarity": "rare", "monster_type": "mage",
         "atk": 30, "def": 30, "hp": 50, "summon_cost": 3, "dice_faces": [2,3,4,4,5,"summon"]},
    20: {"id": 20, "name": "Erzengel", "element": "light", "rarity": "legendary", "monster_type": "warrior",
         "atk": 38, "def": 42, "hp": 65, "summon_cost": 4, "dice_faces": [3,4,5,5,6,"summon"],
         "special": "Heilung: +20 HP für alle verbündeten Monster"},

    # Dark Monsters
    21: {"id": 21, "name": "Schatten-Sprite", "element": "dark", "rarity": "common", "monster_type": "beast",
         "atk": 12, "def": 6, "hp": 15, "summon_cost": 1, "dice_faces": [1,2,2,3,3,"summon"]},
    22: {"id": 22, "name": "Vampir", "element": "dark", "rarity": "uncommon", "monster_type": "undead",
         "atk": 24, "def": 16, "hp": 32, "summon_cost": 2, "dice_faces": [2,2,3,4,4,"summon"]},
    23: {"id": 23, "name": "Lich", "element": "dark", "rarity": "rare", "monster_type": "undead",
         "atk": 35, "def": 22, "hp": 48, "summon_cost": 3, "dice_faces": [2,3,4,5,5,"summon"]},
    24: {"id": 24, "name": "Dunkler Lord", "element": "dark", "rarity": "legendary", "monster_type": "undead",
         "atk": 48, "def": 35, "hp": 60, "summon_cost": 4, "dice_faces": [3,4,5,6,6,"summon"],
         "special": "Lebensraub: Heilt sich für 50% des Schadens"},

    # Special: Najika Dice
    25: {"id": 25, "name": "Najika-Würfel", "element": "explosion", "rarity": "legendary", "monster_type": "mage",
         "atk": 99, "def": 1, "hp": 30, "summon_cost": 5, "dice_faces": [1,1,1,1,1,"EXPLOSION"],
         "special": "EXPLOSION: Zerstört ALLE Monster auf dem Feld (auch eigene!)"},
}

# ===== PLAYER DATA MANAGEMENT =====

def get_player_data_path(player_id):
    """Gibt den Pfad zur Spieler-Datei zurück"""
    return MINIGAMES_DATA / f"player_{player_id}.json"

def load_player_data(player_id):
    """Lädt Spielerdaten oder erstellt Default"""
    path = get_player_data_path(player_id)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Default Player Data
    return {
        "player_id": player_id,
        "created_at": time.time(),
        "card_game": {
            "collection": {},  # card_id: count
            "decks": [],
            "elo": 1000,
            "rank_tier": "bronze",
            "wins": 0,
            "losses": 0,
            "matches_played": 0
        },
        "dice_monsters": {
            "collection": {},  # dice_id: count
            "dice_pool": [],  # Active 12-dice pool
            "wins": 0,
            "losses": 0,
            "duels_played": 0
        },
        "gold": 100,
        "total_xp": 0
    }

def save_player_data(player_id, data):
    """Speichert Spielerdaten"""
    path = get_player_data_path(player_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ===== MATCH HISTORY =====

def get_match_history_path():
    return MINIGAMES_DATA / "match_history.json"

def load_match_history():
    path = get_match_history_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"card_matches": [], "dice_duels": []}

def save_match_history(history):
    path = get_match_history_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

# ===== CARD GAME API FUNCTIONS =====

def api_get_all_cards(faction=None, rarity=None):
    """GET /api/cards - Alle Karten"""
    cards = list(CARDS_DATABASE.values())
    if faction:
        cards = [c for c in cards if c.get("faction") == faction]
    if rarity:
        cards = [c for c in cards if c.get("rarity") == rarity]
    return {"cards": cards, "count": len(cards)}

def api_get_card(card_id):
    """GET /api/cards/{card_id}"""
    card = CARDS_DATABASE.get(card_id)
    if not card:
        return {"error": f"Card {card_id} not found"}
    return card

def api_add_card_to_collection(player_id, card_id, is_golden=False):
    """POST /api/cards/add-to-collection"""
    if card_id not in CARDS_DATABASE:
        return {"error": f"Card {card_id} not found"}

    data = load_player_data(player_id)
    collection = data["card_game"]["collection"]

    key = f"{card_id}_golden" if is_golden else str(card_id)
    collection[key] = collection.get(key, 0) + 1

    save_player_data(player_id, data)
    card = CARDS_DATABASE[card_id]
    return {
        "success": True,
        "message": f"Added {card['name']} to collection!",
        "new_count": collection[key]
    }

def api_get_player_collection(player_id):
    """GET /api/cards/collection/{player_id}"""
    data = load_player_data(player_id)
    collection = data["card_game"]["collection"]

    cards_with_data = []
    for key, count in collection.items():
        is_golden = "_golden" in key
        card_id = int(key.replace("_golden", ""))
        card = CARDS_DATABASE.get(card_id)
        if card:
            cards_with_data.append({
                "card": card,
                "count": count,
                "is_golden": is_golden
            })

    return {
        "player_id": player_id,
        "collection": cards_with_data,
        "total_cards": sum(collection.values())
    }

def api_create_deck(player_id, deck_name, faction, cards):
    """POST /api/decks/create"""
    total_cards = sum(cards.values())
    if total_cards != 5:  # Triple Triad uses 5 cards
        return {"error": f"Deck must have exactly 5 cards (has {total_cards})"}

    data = load_player_data(player_id)

    deck_id = len(data["card_game"]["decks"]) + 1
    deck = {
        "id": deck_id,
        "name": deck_name,
        "faction": faction,
        "cards": cards,
        "created_at": time.time(),
        "wins": 0,
        "games": 0
    }

    data["card_game"]["decks"].append(deck)
    save_player_data(player_id, data)

    return {"success": True, "deck": deck}

def api_get_player_decks(player_id):
    """GET /api/decks/{player_id}"""
    data = load_player_data(player_id)
    return {
        "player_id": player_id,
        "decks": data["card_game"]["decks"],
        "count": len(data["card_game"]["decks"])
    }

def api_start_card_match(player1_id, player2_id=None, is_vs_npc=False, npc_name=None):
    """POST /api/matches/start"""
    history = load_match_history()

    match_id = len(history["card_matches"]) + 1
    match = {
        "id": match_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "is_vs_npc": is_vs_npc,
        "npc_name": npc_name,
        "started_at": time.time(),
        "ended_at": None,
        "winner_id": None,
        "turns_played": 0,
        "board_state": [[None]*3 for _ in range(3)]  # 3x3 board
    }

    history["card_matches"].append(match)
    save_match_history(history)

    return {"success": True, "match_id": match_id, "match": match}

def api_end_card_match(match_id, winner_id, turns_played, gold_earned=0, xp_earned=0):
    """POST /api/matches/end"""
    history = load_match_history()

    match = None
    for m in history["card_matches"]:
        if m["id"] == match_id:
            match = m
            break

    if not match:
        return {"error": f"Match {match_id} not found"}

    match["ended_at"] = time.time()
    match["winner_id"] = winner_id
    match["turns_played"] = turns_played
    match["gold_earned"] = gold_earned
    match["xp_earned"] = xp_earned

    # Update player stats
    for pid in [match["player1_id"], match["player2_id"]]:
        if pid:
            pdata = load_player_data(pid)
            pdata["card_game"]["matches_played"] += 1
            if pid == winner_id:
                pdata["card_game"]["wins"] += 1
                pdata["card_game"]["elo"] += 25
            else:
                pdata["card_game"]["losses"] += 1
                pdata["card_game"]["elo"] = max(0, pdata["card_game"]["elo"] - 15)
            pdata["gold"] += gold_earned
            pdata["total_xp"] += xp_earned
            save_player_data(pid, pdata)

    save_match_history(history)
    return {"success": True, "match": match}

def api_get_card_leaderboard(limit=100):
    """GET /api/rankings/leaderboard"""
    # Sammle alle Spieler
    players = []
    for f in MINIGAMES_DATA.glob("player_*.json"):
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            players.append({
                "player_id": data["player_id"],
                "elo": data["card_game"]["elo"],
                "wins": data["card_game"]["wins"],
                "losses": data["card_game"]["losses"],
                "rank_tier": data["card_game"]["rank_tier"]
            })

    # Sortiere nach ELO
    players.sort(key=lambda x: x["elo"], reverse=True)
    return {"leaderboard": players[:limit], "count": len(players[:limit])}

# ===== DICE MONSTERS API FUNCTIONS =====

def api_get_all_dice(element=None, rarity=None):
    """GET /api/dice - Alle Dice Monsters"""
    dice = list(DICE_MONSTERS_DATABASE.values())
    if element:
        dice = [d for d in dice if d.get("element") == element]
    if rarity:
        dice = [d for d in dice if d.get("rarity") == rarity]
    return {"dice_monsters": dice, "count": len(dice)}

def api_get_dice(dice_id):
    """GET /api/dice/{dice_id}"""
    dice = DICE_MONSTERS_DATABASE.get(dice_id)
    if not dice:
        return {"error": f"Dice Monster {dice_id} not found"}
    return dice

def api_add_dice_to_collection(player_id, dice_id, is_golden=False):
    """POST /api/dice/add-to-collection"""
    if dice_id not in DICE_MONSTERS_DATABASE:
        return {"error": f"Dice Monster {dice_id} not found"}

    data = load_player_data(player_id)
    collection = data["dice_monsters"]["collection"]

    key = f"{dice_id}_golden" if is_golden else str(dice_id)
    collection[key] = collection.get(key, 0) + 1

    save_player_data(player_id, data)
    dice = DICE_MONSTERS_DATABASE[dice_id]
    return {
        "success": True,
        "message": f"Added {dice['name']} to collection!",
        "new_count": collection[key]
    }

def api_get_dice_collection(player_id):
    """GET /api/dice/collection/{player_id}"""
    data = load_player_data(player_id)
    collection = data["dice_monsters"]["collection"]

    dice_with_data = []
    for key, count in collection.items():
        is_golden = "_golden" in key
        dice_id = int(key.replace("_golden", ""))
        dice = DICE_MONSTERS_DATABASE.get(dice_id)
        if dice:
            dice_with_data.append({
                "dice": dice,
                "count": count,
                "is_golden": is_golden
            })

    return {
        "player_id": player_id,
        "collection": dice_with_data,
        "total_dice": sum(collection.values())
    }

def api_start_dice_duel(player1_id, player2_id=None, is_vs_npc=False, npc_name=None, player1_dice_pool=None):
    """POST /api/dice-duel/start"""
    if not player1_dice_pool or len(player1_dice_pool) != 12:
        return {"error": "Player 1 must have exactly 12 dice in pool"}

    history = load_match_history()

    match_id = len(history["dice_duels"]) + 1
    duel = {
        "id": match_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "is_vs_npc": is_vs_npc,
        "npc_name": npc_name,
        "player1_dice_pool": player1_dice_pool,
        "player2_dice_pool": [],
        "player1_hp": 3000,
        "player2_hp": 3000,
        "started_at": time.time(),
        "ended_at": None,
        "winner_id": None,
        "turns_played": 0,
        "board_state": {}
    }

    history["dice_duels"].append(duel)
    save_match_history(history)

    return {"success": True, "match_id": match_id, "duel": duel}

def api_end_dice_duel(match_id, winner_id, player1_hp, player2_hp, turns_played, gold_earned=0, xp_earned=0):
    """POST /api/dice-duel/end"""
    history = load_match_history()

    duel = None
    for d in history["dice_duels"]:
        if d["id"] == match_id:
            duel = d
            break

    if not duel:
        return {"error": f"Duel {match_id} not found"}

    duel["ended_at"] = time.time()
    duel["winner_id"] = winner_id
    duel["player1_hp"] = player1_hp
    duel["player2_hp"] = player2_hp
    duel["turns_played"] = turns_played
    duel["gold_earned"] = gold_earned
    duel["xp_earned"] = xp_earned

    # Update player stats
    for pid in [duel["player1_id"], duel["player2_id"]]:
        if pid:
            pdata = load_player_data(pid)
            pdata["dice_monsters"]["duels_played"] += 1
            if pid == winner_id:
                pdata["dice_monsters"]["wins"] += 1
            else:
                pdata["dice_monsters"]["losses"] += 1
            pdata["gold"] += gold_earned
            pdata["total_xp"] += xp_earned
            save_player_data(pid, pdata)

    save_match_history(history)
    return {"success": True, "duel": duel}

def api_get_duel_history(player_id, limit=20):
    """GET /api/dice-duel/history/{player_id}"""
    history = load_match_history()

    player_duels = [d for d in history["dice_duels"]
                    if d["player1_id"] == player_id or d["player2_id"] == player_id]

    # Sortiere nach Zeit (neueste zuerst)
    player_duels.sort(key=lambda x: x.get("started_at", 0), reverse=True)

    return {
        "player_id": player_id,
        "duels": player_duels[:limit],
        "count": len(player_duels[:limit])
    }

# ===== STARTER PACK =====

def api_give_starter_pack(player_id):
    """Gibt einem neuen Spieler ein Starter Pack"""
    data = load_player_data(player_id)

    # Check ob schon Karten vorhanden
    if data["card_game"]["collection"] or data["dice_monsters"]["collection"]:
        return {"error": "Player already has cards/dice"}

    # 10 zufällige Common/Uncommon Karten
    starter_cards = random.sample([c for c in CARDS_DATABASE.values()
                                   if c["rarity"] in ["common", "uncommon"]], 10)
    for card in starter_cards:
        data["card_game"]["collection"][str(card["id"])] = 1

    # 12 zufällige Common/Uncommon Dice
    starter_dice = random.sample([d for d in DICE_MONSTERS_DATABASE.values()
                                  if d["rarity"] in ["common", "uncommon"]], 12)
    for dice in starter_dice:
        data["dice_monsters"]["collection"][str(dice["id"])] = 1

    # Setze Dice Pool auf die ersten 12
    data["dice_monsters"]["dice_pool"] = [d["id"] for d in starter_dice]

    # Bonus Gold
    data["gold"] += 500

    save_player_data(player_id, data)

    return {
        "success": True,
        "message": "Starter Pack erhalten!",
        "cards_received": [c["name"] for c in starter_cards],
        "dice_received": [d["name"] for d in starter_dice],
        "gold_received": 500
    }

# ===== HELPER: Roll Dice =====

def roll_dice_face(dice_id):
    """Würfelt einen Dice Monster Würfel"""
    dice = DICE_MONSTERS_DATABASE.get(dice_id)
    if not dice:
        return {"error": "Dice not found"}

    face = random.choice(dice["dice_faces"])
    return {
        "dice_id": dice_id,
        "dice_name": dice["name"],
        "result": face,
        "can_summon": face == "summon" or face == "EXPLOSION"
    }


print("✅ Najika Minigames API geladen (Card Game + Dice Monsters)")
