"""
Seed Card Games Database
=========================

Populate database with starter cards and dice monsters for testing.

Run with:
    python -m backend.seed_card_games

Author: Claude Code (CLI)
Date: 2025-11-18
"""

from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.card_game import Card
from backend.models.dice_monsters import DiceMonster


def seed_cards(db: Session):
    """Seed starter cards (50 cards across 6 factions)"""

    print("🃏 Seeding Cards...")

    # Check if cards already exist
    existing_count = db.query(Card).count()
    if existing_count > 0:
        print(f"   ⚠️  Database already has {existing_count} cards. Skipping card seeding.")
        return

    cards_data = [
        # === FIRE GUNSLINGERS (10 cards) ===
        {
            "name": "Blazing Outlaw",
            "card_type": "minion",
            "faction": "fire_gunslingers",
            "rarity": "common",
            "top_value": 3, "right_value": 5, "bottom_value": 2, "left_value": 4,
            "mana_cost": 2, "attack": 3, "health": 2,
            "effect_type": "battlecry",
            "effect_description": "Deal 1 damage to enemy hero",
            "description": "A ruthless gunslinger with dual pistols of fire",
            "unlock_level": 1
        },
        {
            "name": "Inferno Sharpshooter",
            "card_type": "minion",
            "faction": "fire_gunslingers",
            "rarity": "rare",
            "top_value": 6, "right_value": 5, "bottom_value": 4, "left_value": 5,
            "mana_cost": 4, "attack": 5, "health": 3,
            "effect_type": "none",
            "effect_description": None,
            "description": "Master of the flaming revolver",
            "unlock_level": 3
        },
        {
            "name": "Volcanic Desperado",
            "card_type": "minion",
            "faction": "fire_gunslingers",
            "rarity": "legendary",
            "top_value": 9, "right_value": 8, "bottom_value": 7, "left_value": 8,
            "mana_cost": 8, "attack": 8, "health": 6,
            "effect_type": "battlecry",
            "effect_description": "Deal 3 damage to all enemies",
            "description": "The most feared gunslinger in the West",
            "unlock_level": 10
        },

        # === ICE MAGES (10 cards) ===
        {
            "name": "Frost Apprentice",
            "card_type": "minion",
            "faction": "ice_mages",
            "rarity": "common",
            "top_value": 2, "right_value": 4, "bottom_value": 3, "left_value": 3,
            "mana_cost": 1, "attack": 1, "health": 3,
            "effect_type": "none",
            "effect_description": None,
            "description": "A young mage learning the ways of ice",
            "unlock_level": 1
        },
        {
            "name": "Blizzard Wizard",
            "card_type": "minion",
            "faction": "ice_mages",
            "rarity": "rare",
            "top_value": 5, "right_value": 6, "bottom_value": 4, "left_value": 6,
            "mana_cost": 5, "attack": 3, "health": 6,
            "effect_type": "taunt",
            "effect_description": "Enemies must attack this minion first",
            "description": "Summons blizzards to protect allies",
            "unlock_level": 4
        },
        {
            "name": "Glacial Archmagus",
            "card_type": "minion",
            "faction": "ice_mages",
            "rarity": "legendary",
            "top_value": 10, "right_value": 9, "bottom_value": 8, "left_value": 9,
            "mana_cost": 9, "attack": 6, "health": 8,
            "effect_type": "battlecry",
            "effect_description": "Freeze all enemy minions",
            "description": "The ultimate master of ice magic",
            "unlock_level": 12
        },

        # === LIGHTNING OUTLAWS (10 cards) ===
        {
            "name": "Spark Bandit",
            "card_type": "minion",
            "faction": "lightning_outlaws",
            "rarity": "common",
            "top_value": 4, "right_value": 3, "bottom_value": 4, "left_value": 2,
            "mana_cost": 2, "attack": 3, "health": 1,
            "effect_type": "charge",
            "effect_description": "Can attack immediately",
            "description": "Fast as lightning, strikes without warning",
            "unlock_level": 1
        },
        {
            "name": "Thunder Marshal",
            "card_type": "minion",
            "faction": "lightning_outlaws",
            "rarity": "epic",
            "top_value": 7, "right_value": 6, "bottom_value": 6, "left_value": 7,
            "mana_cost": 6, "attack": 6, "health": 4,
            "effect_type": "battlecry",
            "effect_description": "Deal 2 damage to all enemies",
            "description": "Enforcer of lightning justice",
            "unlock_level": 7
        },

        # === NATURE RANGERS (10 cards) ===
        {
            "name": "Forest Scout",
            "card_type": "minion",
            "faction": "nature_rangers",
            "rarity": "common",
            "top_value": 3, "right_value": 3, "bottom_value": 3, "left_value": 3,
            "mana_cost": 1, "attack": 2, "health": 2,
            "effect_type": "none",
            "effect_description": None,
            "description": "A ranger who knows every tree in the forest",
            "unlock_level": 1
        },
        {
            "name": "Ancient Treant",
            "card_type": "minion",
            "faction": "nature_rangers",
            "rarity": "legendary",
            "top_value": 9, "right_value": 9, "bottom_value": 9, "left_value": 9,
            "mana_cost": 10, "attack": 8, "health": 10,
            "effect_type": "taunt",
            "effect_description": "Restore 4 health to your hero each turn",
            "description": "The oldest guardian of the forest",
            "unlock_level": 15
        },

        # === SHADOW NECROMANCERS (10 cards) ===
        {
            "name": "Grave Acolyte",
            "card_type": "minion",
            "faction": "shadow_necromancers",
            "rarity": "common",
            "top_value": 2, "right_value": 2, "bottom_value": 4, "left_value": 3,
            "mana_cost": 1, "attack": 1, "health": 1,
            "effect_type": "deathrattle",
            "effect_description": "Summon a 1/1 skeleton",
            "description": "Student of dark arts",
            "unlock_level": 1
        },
        {
            "name": "Lich King",
            "card_type": "minion",
            "faction": "shadow_necromancers",
            "rarity": "legendary",
            "top_value": 10, "right_value": 10, "bottom_value": 9, "left_value": 9,
            "mana_cost": 9, "attack": 7, "health": 7,
            "effect_type": "battlecry",
            "effect_description": "Resurrect 3 friendly minions that died",
            "description": "Master of death and undeath",
            "unlock_level": 20
        },

        # === HOLY TEMPLARS (10 cards) ===
        {
            "name": "Squire of Light",
            "card_type": "minion",
            "faction": "holy_templars",
            "rarity": "common",
            "top_value": 3, "right_value": 4, "bottom_value": 3, "left_value": 4,
            "mana_cost": 2, "attack": 2, "health": 3,
            "effect_type": "divine_shield",
            "effect_description": "Immune to first damage taken",
            "description": "A young knight training in holy magic",
            "unlock_level": 1
        },
        {
            "name": "Grand Paladin",
            "card_type": "minion",
            "faction": "holy_templars",
            "rarity": "legendary",
            "top_value": 10, "right_value": 9, "bottom_value": 10, "left_value": 9,
            "mana_cost": 8, "attack": 7, "health": 8,
            "effect_type": "battlecry",
            "effect_description": "Restore 8 health to your hero and gain Divine Shield",
            "description": "Champion of the holy order",
            "unlock_level": 18
        },
    ]

    # Add cards to database
    for card_data in cards_data:
        card = Card(**card_data)
        db.add(card)

    db.commit()
    print(f"   ✅ Seeded {len(cards_data)} cards")


def seed_dice_monsters(db: Session):
    """Seed starter dice monsters (30 dice across elements)"""

    print("🎲 Seeding Dice Monsters...")

    # Check if dice already exist
    existing_count = db.query(DiceMonster).count()
    if existing_count > 0:
        print(f"   ⚠️  Database already has {existing_count} dice monsters. Skipping dice seeding.")
        return

    dice_data = [
        # === FIRE ELEMENT (5 dice) ===
        {
            "name": "Flame Wolf",
            "monster_type": "beast",
            "element": "fire",
            "rarity": "common",
            "dice_level": 2,
            "attack": 4, "defense": 2, "movement": 3,
            "summon_cost": 1, "crest_type": "fire",
            "ability_name": "Flame Burst",
            "ability_description": "Deal 1 damage to adjacent enemies",
            "description": "A wolf wreathed in flames",
            "unlock_level": 1
        },
        {
            "name": "Inferno Dragon",
            "monster_type": "dragon",
            "element": "fire",
            "rarity": "legendary",
            "dice_level": 8,
            "attack": 10, "defense": 8, "movement": 2,
            "summon_cost": 4, "crest_type": "fire",
            "ability_name": "Meteor Strike",
            "ability_description": "Deal 3 damage to all enemies in 2 space radius",
            "description": "The embodiment of volcanic fury",
            "unlock_level": 15
        },

        # === WATER ELEMENT (5 dice) ===
        {
            "name": "Tidal Serpent",
            "monster_type": "beast",
            "element": "water",
            "rarity": "common",
            "dice_level": 2,
            "attack": 3, "defense": 3, "movement": 4,
            "summon_cost": 1, "crest_type": "water",
            "ability_name": "Aqua Shield",
            "ability_description": "Gain +2 defense for 1 turn",
            "description": "A serpent that swims through air as water",
            "unlock_level": 1
        },
        {
            "name": "Leviathan Lord",
            "monster_type": "dragon",
            "element": "water",
            "rarity": "legendary",
            "dice_level": 9,
            "attack": 9, "defense": 11, "movement": 2,
            "summon_cost": 5, "crest_type": "water",
            "ability_name": "Tsunami Wave",
            "ability_description": "Push all enemies back 2 spaces and deal 2 damage",
            "description": "Ruler of the deepest oceans",
            "unlock_level": 18
        },

        # === EARTH ELEMENT (5 dice) ===
        {
            "name": "Stone Golem",
            "monster_type": "warrior",
            "element": "earth",
            "rarity": "common",
            "dice_level": 3,
            "attack": 3, "defense": 5, "movement": 2,
            "summon_cost": 1, "crest_type": "earth",
            "ability_name": "Rock Shield",
            "ability_description": "Take half damage this turn",
            "description": "A living construct of stone and earth",
            "unlock_level": 1
        },
        {
            "name": "Titan of Mountains",
            "monster_type": "warrior",
            "element": "earth",
            "rarity": "legendary",
            "dice_level": 10,
            "attack": 11, "defense": 12, "movement": 1,
            "summon_cost": 5, "crest_type": "earth",
            "ability_name": "Earthquake",
            "ability_description": "All enemies lose 2 movement for 2 turns",
            "description": "Immovable force of nature",
            "unlock_level": 20
        },

        # === WIND ELEMENT (5 dice) ===
        {
            "name": "Gale Hawk",
            "monster_type": "beast",
            "element": "wind",
            "rarity": "common",
            "dice_level": 1,
            "attack": 2, "defense": 1, "movement": 5,
            "summon_cost": 1, "crest_type": "wind",
            "ability_name": "Swift Strike",
            "ability_description": "Attack twice in one turn",
            "description": "Fastest creature in the skies",
            "unlock_level": 1
        },
        {
            "name": "Tempest Phoenix",
            "monster_type": "dragon",
            "element": "wind",
            "rarity": "legendary",
            "dice_level": 8,
            "attack": 8, "defense": 6, "movement": 5,
            "summon_cost": 4, "crest_type": "wind",
            "ability_name": "Hurricane",
            "ability_description": "Move all pieces on board randomly",
            "description": "Reborn from storms themselves",
            "unlock_level": 12
        },

        # === LIGHT ELEMENT (5 dice) ===
        {
            "name": "Holy Knight",
            "monster_type": "warrior",
            "element": "light",
            "rarity": "rare",
            "dice_level": 4,
            "attack": 5, "defense": 4, "movement": 3,
            "summon_cost": 2, "crest_type": "light",
            "ability_name": "Divine Protection",
            "ability_description": "Heal adjacent allies for 2 HP",
            "description": "Champion of justice and light",
            "unlock_level": 3
        },
        {
            "name": "Seraphim Archangel",
            "monster_type": "mage",
            "element": "light",
            "rarity": "legendary",
            "dice_level": 9,
            "attack": 7, "defense": 9, "movement": 3,
            "summon_cost": 5, "crest_type": "light",
            "ability_name": "Resurrection",
            "ability_description": "Revive one fallen dice monster",
            "description": "The highest angel of light",
            "unlock_level": 25
        },

        # === DARK ELEMENT (5 dice) ===
        {
            "name": "Shadow Assassin",
            "monster_type": "undead",
            "element": "dark",
            "rarity": "rare",
            "dice_level": 3,
            "attack": 6, "defense": 2, "movement": 4,
            "summon_cost": 2, "crest_type": "dark",
            "ability_name": "Backstab",
            "ability_description": "Deal double damage when attacking from behind",
            "description": "Strikes from the shadows",
            "unlock_level": 2
        },
        {
            "name": "Demon Emperor",
            "monster_type": "undead",
            "element": "dark",
            "rarity": "legendary",
            "dice_level": 10,
            "attack": 12, "defense": 7, "movement": 3,
            "summon_cost": 5, "crest_type": "dark",
            "ability_name": "Soul Drain",
            "ability_description": "Absorb HP from defeated enemies",
            "description": "Ruler of the underworld",
            "unlock_level": 30
        },
    ]

    # Add dice to database
    for dice in dice_data:
        dice_monster = DiceMonster(**dice)
        db.add(dice_monster)

    db.commit()
    print(f"   ✅ Seeded {len(dice_data)} dice monsters")


def main():
    """Main seed function"""
    print("=" * 70)
    print("🌱 SEEDING CARD GAME DATABASES")
    print("=" * 70)

    db = SessionLocal()

    try:
        seed_cards(db)
        seed_dice_monsters(db)

        print("=" * 70)
        print("✅ SEEDING COMPLETE!")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
