"""
Seed 100 Starter Cards for Triple Triad
60 Common, 25 Rare, 12 Epic, 3 Legendary
"""

from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.card_game import Card


STARTER_CARDS = [
    # ========================================================================
    # COMMON CARDS (60) - Balanced stats 3-6
    # ========================================================================

    # FIRE FACTION (10 Common)
    {"name": "Fire Imp", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 4, "left_value": 2, "faction": "Fire Gunslingers", "mana_cost": 1, "attack": 3, "health": 2, "rarity": "common"},
    {"name": "Ember Sprite", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 3, "left_value": 3, "faction": "Fire Gunslingers", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Flame Wisp", "card_type": "minion", "top_value": 3, "right_value": 5, "bottom_value": 4, "left_value": 2, "faction": "Fire Gunslingers", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Cinder Mage", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 5, "left_value": 3, "faction": "Fire Gunslingers", "mana_cost": 2, "attack": 4, "health": 2, "rarity": "common"},
    {"name": "Scorch Elemental", "card_type": "minion", "top_value": 5, "right_value": 4, "bottom_value": 3, "left_value": 3, "faction": "Fire Gunslingers", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Ash Walker", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 4, "left_value": 4, "faction": "Fire Gunslingers", "mana_cost": 2, "attack": 2, "health": 4, "rarity": "common"},
    {"name": "Lava Hound", "card_type": "minion", "top_value": 4, "right_value": 5, "bottom_value": 3, "left_value": 3, "faction": "Fire Gunslingers", "mana_cost": 2, "attack": 4, "health": 3, "rarity": "common"},
    {"name": "Spark Scout", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 3, "left_value": 4, "faction": "Fire Gunslingers", "mana_cost": 1, "attack": 2, "health": 3, "rarity": "common"},
    {"name": "Pyroclast", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 4, "left_value": 3, "faction": "Fire Gunslingers", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Inferno Bat", "card_type": "minion", "top_value": 3, "right_value": 3, "bottom_value": 5, "left_value": 4, "faction": "Fire Gunslingers", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},

    # ICE FACTION (10 Common)
    {"name": "Frost Imp", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 5, "left_value": 3, "faction": "Ice Mages", "mana_cost": 1, "attack": 2, "health": 3, "rarity": "common"},
    {"name": "Icicle Sprite", "card_type": "minion", "top_value": 3, "right_value": 5, "bottom_value": 3, "left_value": 4, "faction": "Ice Mages", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Snow Wisp", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 4, "left_value": 3, "faction": "Ice Mages", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Blizzard Mage", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 3, "left_value": 4, "faction": "Ice Mages", "mana_cost": 2, "attack": 3, "health": 4, "rarity": "common"},
    {"name": "Glacier Elemental", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 5, "left_value": 3, "faction": "Ice Mages", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Frostbite Wolf", "card_type": "minion", "top_value": 5, "right_value": 4, "bottom_value": 3, "left_value": 3, "faction": "Ice Mages", "mana_cost": 2, "attack": 4, "health": 2, "rarity": "common"},
    {"name": "Crystal Shardling", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 4, "left_value": 4, "faction": "Ice Mages", "mana_cost": 2, "attack": 2, "health": 4, "rarity": "common"},
    {"name": "Permafrost Golem", "card_type": "minion", "top_value": 3, "right_value": 5, "bottom_value": 4, "left_value": 3, "faction": "Ice Mages", "mana_cost": 3, "attack": 2, "health": 5, "rarity": "common"},
    {"name": "Arctic Fox", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 3, "left_value": 5, "faction": "Ice Mages", "mana_cost": 1, "attack": 3, "health": 2, "rarity": "common"},
    {"name": "Winter Owl", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 3, "left_value": 4, "faction": "Ice Mages", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},

    # LIGHTNING FACTION (10 Common)
    {"name": "Shock Imp", "card_type": "minion", "top_value": 5, "right_value": 4, "bottom_value": 3, "left_value": 3, "faction": "Lightning Outlaws", "mana_cost": 1, "attack": 3, "health": 2, "rarity": "common"},
    {"name": "Thunder Sprite", "card_type": "minion", "top_value": 4, "right_value": 5, "bottom_value": 3, "left_value": 3, "faction": "Lightning Outlaws", "mana_cost": 2, "attack": 4, "health": 2, "rarity": "common"},
    {"name": "Volt Wisp", "card_type": "minion", "top_value": 3, "right_value": 3, "bottom_value": 5, "left_value": 4, "faction": "Lightning Outlaws", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Storm Mage", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 4, "left_value": 3, "faction": "Lightning Outlaws", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Static Elemental", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 3, "left_value": 4, "faction": "Lightning Outlaws", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Bolt Hound", "card_type": "minion", "top_value": 3, "right_value": 5, "bottom_value": 4, "left_value": 3, "faction": "Lightning Outlaws", "mana_cost": 2, "attack": 4, "health": 3, "rarity": "common"},
    {"name": "Spark Beetle", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 4, "left_value": 4, "faction": "Lightning Outlaws", "mana_cost": 1, "attack": 2, "health": 3, "rarity": "common"},
    {"name": "Thunder Hawk", "card_type": "minion", "top_value": 5, "right_value": 4, "bottom_value": 3, "left_value": 3, "faction": "Lightning Outlaws", "mana_cost": 2, "attack": 3, "health": 2, "rarity": "common"},
    {"name": "Plasma Bat", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 5, "left_value": 3, "faction": "Lightning Outlaws", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Charge Spider", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 3, "left_value": 5, "faction": "Lightning Outlaws", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},

    # NATURE FACTION (10 Common)
    {"name": "Vine Imp", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 5, "left_value": 3, "faction": "Nature Rangers", "mana_cost": 1, "attack": 2, "health": 3, "rarity": "common"},
    {"name": "Leaf Sprite", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 4, "left_value": 4, "faction": "Nature Rangers", "mana_cost": 2, "attack": 2, "health": 4, "rarity": "common"},
    {"name": "Forest Wisp", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 3, "left_value": 4, "faction": "Nature Rangers", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Grove Mage", "card_type": "minion", "top_value": 3, "right_value": 5, "bottom_value": 4, "left_value": 3, "faction": "Nature Rangers", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Root Elemental", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 5, "left_value": 3, "faction": "Nature Rangers", "mana_cost": 3, "attack": 2, "health": 5, "rarity": "common"},
    {"name": "Moss Bear", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 4, "left_value": 4, "faction": "Nature Rangers", "mana_cost": 3, "attack": 3, "health": 4, "rarity": "common"},
    {"name": "Thorn Wolf", "card_type": "minion", "top_value": 5, "right_value": 4, "bottom_value": 3, "left_value": 3, "faction": "Nature Rangers", "mana_cost": 2, "attack": 4, "health": 2, "rarity": "common"},
    {"name": "Seed Sprite", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 3, "left_value": 4, "faction": "Nature Rangers", "mana_cost": 1, "attack": 2, "health": 3, "rarity": "common"},
    {"name": "Blossom Owl", "card_type": "minion", "top_value": 3, "right_value": 3, "bottom_value": 5, "left_value": 4, "faction": "Nature Rangers", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Petal Fairy", "card_type": "minion", "top_value": 4, "right_value": 5, "bottom_value": 3, "left_value": 3, "faction": "Nature Rangers", "mana_cost": 2, "attack": 3, "health": 2, "rarity": "common"},

    # SHADOW FACTION (10 Common)
    {"name": "Shadow Imp", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 4, "left_value": 3, "faction": "Shadow Necromancers", "mana_cost": 1, "attack": 3, "health": 2, "rarity": "common"},
    {"name": "Dusk Sprite", "card_type": "minion", "top_value": 3, "right_value": 5, "bottom_value": 3, "left_value": 4, "faction": "Shadow Necromancers", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Void Wisp", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 5, "left_value": 3, "faction": "Shadow Necromancers", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Gloom Mage", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 4, "left_value": 4, "faction": "Shadow Necromancers", "mana_cost": 2, "attack": 2, "health": 4, "rarity": "common"},
    {"name": "Dark Elemental", "card_type": "minion", "top_value": 5, "right_value": 4, "bottom_value": 3, "left_value": 3, "faction": "Shadow Necromancers", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Shade Hound", "card_type": "minion", "top_value": 4, "right_value": 5, "bottom_value": 3, "left_value": 3, "faction": "Shadow Necromancers", "mana_cost": 2, "attack": 4, "health": 2, "rarity": "common"},
    {"name": "Whisper Bat", "card_type": "minion", "top_value": 3, "right_value": 3, "bottom_value": 5, "left_value": 4, "faction": "Shadow Necromancers", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Umbra Raven", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 4, "left_value": 3, "faction": "Shadow Necromancers", "mana_cost": 2, "attack": 3, "health": 2, "rarity": "common"},
    {"name": "Eclipse Spider", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 3, "left_value": 4, "faction": "Shadow Necromancers", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Nightcrawler", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 4, "left_value": 4, "faction": "Shadow Necromancers", "mana_cost": 2, "attack": 2, "health": 4, "rarity": "common"},

    # HOLY FACTION (10 Common)
    {"name": "Light Imp", "card_type": "minion", "top_value": 4, "right_value": 3, "bottom_value": 4, "left_value": 4, "faction": "Holy Templars", "mana_cost": 2, "attack": 2, "health": 4, "rarity": "common"},
    {"name": "Dawn Sprite", "card_type": "minion", "top_value": 3, "right_value": 5, "bottom_value": 4, "left_value": 3, "faction": "Holy Templars", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Radiance Wisp", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 3, "left_value": 4, "faction": "Holy Templars", "mana_cost": 1, "attack": 2, "health": 2, "rarity": "common"},
    {"name": "Divine Mage", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 4, "left_value": 3, "faction": "Holy Templars", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Holy Elemental", "card_type": "minion", "top_value": 3, "right_value": 4, "bottom_value": 5, "left_value": 3, "faction": "Holy Templars", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Blessed Lion", "card_type": "minion", "top_value": 5, "right_value": 3, "bottom_value": 3, "left_value": 4, "faction": "Holy Templars", "mana_cost": 2, "attack": 3, "health": 3, "rarity": "common"},
    {"name": "Seraph Dove", "card_type": "minion", "top_value": 4, "right_value": 4, "bottom_value": 3, "left_value": 4, "faction": "Holy Templars", "mana_cost": 1, "attack": 2, "health": 3, "rarity": "common"},
    {"name": "Sanctum Guardian", "card_type": "minion", "top_value": 3, "right_value": 3, "bottom_value": 5, "left_value": 4, "faction": "Holy Templars", "mana_cost": 3, "attack": 2, "health": 5, "rarity": "common"},
    {"name": "Purity Angel", "card_type": "minion", "top_value": 4, "right_value": 5, "bottom_value": 3, "left_value": 3, "faction": "Holy Templars", "mana_cost": 2, "attack": 3, "health": 2, "rarity": "common"},
    {"name": "Light Pegasus", "card_type": "minion", "top_value": 5, "right_value": 4, "bottom_value": 4, "left_value": 3, "faction": "Holy Templars", "mana_cost": 3, "attack": 4, "health": 3, "rarity": "common"},

    # ========================================================================
    # RARE CARDS (25) - Stronger stats 6-8
    # ========================================================================

    # Fire Rare (4)
    {"name": "Flame Drake", "card_type": "minion", "top_value": 7, "right_value": 6, "bottom_value": 5, "left_value": 6, "faction": "Fire Gunslingers", "mana_cost": 4, "attack": 6, "health": 5, "rarity": "rare"},
    {"name": "Inferno Knight", "card_type": "minion", "top_value": 6, "right_value": 7, "bottom_value": 6, "left_value": 5, "faction": "Fire Gunslingers", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},
    {"name": "Magma Golem", "card_type": "minion", "top_value": 6, "right_value": 5, "bottom_value": 7, "left_value": 6, "faction": "Fire Gunslingers", "mana_cost": 5, "attack": 5, "health": 7, "rarity": "rare"},
    {"name": "Pyroclasm Titan", "card_type": "minion", "top_value": 7, "right_value": 6, "bottom_value": 6, "left_value": 5, "faction": "Fire Gunslingers", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},

    # Ice Rare (4)
    {"name": "Frost Guardian", "card_type": "minion", "top_value": 6, "right_value": 7, "bottom_value": 6, "left_value": 6, "faction": "Ice Mages", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},
    {"name": "Blizzard Wyrm", "card_type": "minion", "top_value": 7, "right_value": 5, "bottom_value": 6, "left_value": 6, "faction": "Ice Mages", "mana_cost": 4, "attack": 5, "health": 6, "rarity": "rare"},
    {"name": "Glacier Colossus", "card_type": "minion", "top_value": 6, "right_value": 6, "bottom_value": 7, "left_value": 5, "faction": "Ice Mages", "mana_cost": 5, "attack": 5, "health": 7, "rarity": "rare"},
    {"name": "Frost Lich", "card_type": "minion", "top_value": 7, "right_value": 6, "bottom_value": 5, "left_value": 6, "faction": "Ice Mages", "mana_cost": 5, "attack": 6, "health": 5, "rarity": "rare"},

    # Lightning Rare (4)
    {"name": "Storm Dragon", "card_type": "minion", "top_value": 7, "right_value": 6, "bottom_value": 6, "left_value": 5, "faction": "Lightning Outlaws", "mana_cost": 4, "attack": 6, "health": 5, "rarity": "rare"},
    {"name": "Thunder Titan", "card_type": "minion", "top_value": 6, "right_value": 7, "bottom_value": 6, "left_value": 5, "faction": "Lightning Outlaws", "mana_cost": 5, "attack": 7, "health": 5, "rarity": "rare"},
    {"name": "Volt Archon", "card_type": "minion", "top_value": 6, "right_value": 6, "bottom_value": 7, "left_value": 5, "faction": "Lightning Outlaws", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},
    {"name": "Plasma Leviathan", "card_type": "minion", "top_value": 7, "right_value": 5, "bottom_value": 6, "left_value": 6, "faction": "Lightning Outlaws", "mana_cost": 5, "attack": 5, "health": 6, "rarity": "rare"},

    # Nature Rare (4)
    {"name": "Ancient Treant", "card_type": "minion", "top_value": 6, "right_value": 6, "bottom_value": 7, "left_value": 6, "faction": "Nature Rangers", "mana_cost": 6, "attack": 5, "health": 8, "rarity": "rare"},
    {"name": "Forest Dragon", "card_type": "minion", "top_value": 7, "right_value": 6, "bottom_value": 5, "left_value": 6, "faction": "Nature Rangers", "mana_cost": 4, "attack": 6, "health": 5, "rarity": "rare"},
    {"name": "Vine Behemoth", "card_type": "minion", "top_value": 6, "right_value": 7, "bottom_value": 6, "left_value": 5, "faction": "Nature Rangers", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},
    {"name": "Grove Warden", "card_type": "minion", "top_value": 6, "right_value": 5, "bottom_value": 7, "left_value": 6, "faction": "Nature Rangers", "mana_cost": 5, "attack": 5, "health": 7, "rarity": "rare"},

    # Shadow Rare (5)
    {"name": "Shadow Drake", "card_type": "minion", "top_value": 7, "right_value": 6, "bottom_value": 6, "left_value": 5, "faction": "Shadow Necromancers", "mana_cost": 4, "attack": 6, "health": 5, "rarity": "rare"},
    {"name": "Void Reaper", "card_type": "minion", "top_value": 6, "right_value": 7, "bottom_value": 5, "left_value": 6, "faction": "Shadow Necromancers", "mana_cost": 5, "attack": 7, "health": 4, "rarity": "rare"},
    {"name": "Umbra Demon", "card_type": "minion", "top_value": 6, "right_value": 6, "bottom_value": 7, "left_value": 5, "faction": "Shadow Necromancers", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},
    {"name": "Eclipse Lord", "card_type": "minion", "top_value": 7, "right_value": 5, "bottom_value": 6, "left_value": 6, "faction": "Shadow Necromancers", "mana_cost": 5, "attack": 5, "health": 6, "rarity": "rare"},
    {"name": "Nightmare Horror", "card_type": "minion", "top_value": 6, "right_value": 6, "bottom_value": 6, "left_value": 6, "faction": "Shadow Necromancers", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},

    # Holy Rare (4)
    {"name": "Archangel", "card_type": "minion", "top_value": 7, "right_value": 6, "bottom_value": 6, "left_value": 6, "faction": "Holy Templars", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},
    {"name": "Divine Champion", "card_type": "minion", "top_value": 6, "right_value": 7, "bottom_value": 6, "left_value": 5, "faction": "Holy Templars", "mana_cost": 5, "attack": 7, "health": 5, "rarity": "rare"},
    {"name": "Radiant Paladin", "card_type": "minion", "top_value": 6, "right_value": 6, "bottom_value": 7, "left_value": 5, "faction": "Holy Templars", "mana_cost": 5, "attack": 6, "health": 6, "rarity": "rare"},
    {"name": "Holy Sentinel", "card_type": "minion", "top_value": 6, "right_value": 5, "bottom_value": 6, "left_value": 7, "faction": "Holy Templars", "mana_cost": 5, "attack": 5, "health": 7, "rarity": "rare"},

    # ========================================================================
    # EPIC CARDS (12) - Very strong stats 8-9
    # ========================================================================

    # Fire Epic (2)
    {"name": "Ancient Phoenix", "card_type": "minion", "top_value": 9, "right_value": 8, "bottom_value": 7, "left_value": 8, "faction": "Fire Gunslingers", "mana_cost": 7, "attack": 8, "health": 7, "rarity": "epic"},
    {"name": "Inferno Lord", "card_type": "minion", "top_value": 8, "right_value": 9, "bottom_value": 8, "left_value": 7, "faction": "Fire Gunslingers", "mana_cost": 7, "attack": 9, "health": 7, "rarity": "epic"},

    # Ice Epic (2)
    {"name": "Frost Titan", "card_type": "minion", "top_value": 8, "right_value": 8, "bottom_value": 9, "left_value": 7, "faction": "Ice Mages", "mana_cost": 8, "attack": 7, "health": 9, "rarity": "epic"},
    {"name": "Winter's Fury", "card_type": "minion", "top_value": 9, "right_value": 7, "bottom_value": 8, "left_value": 8, "faction": "Ice Mages", "mana_cost": 7, "attack": 7, "health": 8, "rarity": "epic"},

    # Lightning Epic (2)
    {"name": "Thunder God", "card_type": "minion", "top_value": 9, "right_value": 8, "bottom_value": 8, "left_value": 7, "faction": "Lightning Outlaws", "mana_cost": 7, "attack": 9, "health": 7, "rarity": "epic"},
    {"name": "Storm Sovereign", "card_type": "minion", "top_value": 8, "right_value": 9, "bottom_value": 7, "left_value": 8, "faction": "Lightning Outlaws", "mana_cost": 7, "attack": 8, "health": 7, "rarity": "epic"},

    # Nature Epic (2)
    {"name": "World Tree", "card_type": "minion", "top_value": 8, "right_value": 8, "bottom_value": 9, "left_value": 8, "faction": "Nature Rangers", "mana_cost": 9, "attack": 6, "health": 10, "rarity": "epic"},
    {"name": "Gaia's Champion", "card_type": "minion", "top_value": 9, "right_value": 7, "bottom_value": 8, "left_value": 8, "faction": "Nature Rangers", "mana_cost": 7, "attack": 7, "health": 8, "rarity": "epic"},

    # Shadow Epic (2)
    {"name": "Void Emperor", "card_type": "minion", "top_value": 9, "right_value": 8, "bottom_value": 8, "left_value": 7, "faction": "Shadow Necromancers", "mana_cost": 7, "attack": 9, "health": 6, "rarity": "epic"},
    {"name": "Death Incarnate", "card_type": "minion", "top_value": 8, "right_value": 9, "bottom_value": 7, "left_value": 8, "faction": "Shadow Necromancers", "mana_cost": 7, "attack": 8, "health": 7, "rarity": "epic"},

    # Holy Epic (2)
    {"name": "Seraphim", "card_type": "minion", "top_value": 9, "right_value": 8, "bottom_value": 8, "left_value": 8, "faction": "Holy Templars", "mana_cost": 8, "attack": 8, "health": 8, "rarity": "epic"},
    {"name": "Celestial Avatar", "card_type": "minion", "top_value": 8, "right_value": 9, "bottom_value": 8, "left_value": 7, "faction": "Holy Templars", "mana_cost": 7, "attack": 8, "health": 7, "rarity": "epic"},

    # ========================================================================
    # LEGENDARY CARDS (3) - Maximum stats 10
    # ========================================================================

    {"name": "Bahamut Zero", "card_type": "minion", "top_value": 10, "right_value": 10, "bottom_value": 10, "left_value": 10, "faction": "Lightning Outlaws", "mana_cost": 10, "attack": 12, "health": 12, "rarity": "legendary"},
    {"name": "Leviathan Prime", "card_type": "minion", "top_value": 10, "right_value": 9, "bottom_value": 10, "left_value": 9, "faction": "Ice Mages", "mana_cost": 10, "attack": 10, "health": 12, "rarity": "legendary"},
    {"name": "Ragnarok", "card_type": "minion", "top_value": 10, "right_value": 10, "bottom_value": 9, "left_value": 10, "faction": "Fire Gunslingers", "mana_cost": 10, "attack": 12, "health": 10, "rarity": "legendary"},
]


def seed_100_cards(db: Session):
    """Seed 100 starter cards"""
    created_count = 0

    for card_data in STARTER_CARDS:
        # Check if exists
        existing = db.query(Card).filter(Card.name == card_data["name"]).first()

        if not existing:
            card = Card(**card_data)
            db.add(card)
            created_count += 1

    db.commit()
    return created_count


def main():
    """Run card seeding"""
    db = SessionLocal()

    try:
        print("\n🃏 Seeding 100 Starter Cards...")
        print("=" * 70)

        created_count = seed_100_cards(db)

        # Count by rarity
        common_count = db.query(Card).filter(Card.rarity == "common").count()
        rare_count = db.query(Card).filter(Card.rarity == "rare").count()
        epic_count = db.query(Card).filter(Card.rarity == "epic").count()
        legendary_count = db.query(Card).filter(Card.rarity == "legendary").count()

        print(f"✅ Seeded {created_count} new cards!")
        print("=" * 70)
        print("📊 Card Distribution:")
        print(f"   - Common: {common_count} cards")
        print(f"   - Rare: {rare_count} cards")
        print(f"   - Epic: {epic_count} cards")
        print(f"   - Legendary: {legendary_count} cards")
        print(f"   - TOTAL: {common_count + rare_count + epic_count + legendary_count} cards")
        print("=" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    main()
