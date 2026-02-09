"""
Simple Card Seeder - Without Player Dependencies
Creates basic card pool for testing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models.card_game import Card


def seed_basic_cards():
    """Seed 20 starter cards"""

    print("=" * 60)
    print("[SEED] Card Game Database Seeding")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Check existing
        existing = db.query(Card).count()
        if existing > 0:
            print(f"[WARN] Database already has {existing} cards. Skipping.")
            return

        print("[INFO] Adding 20 starter cards...")

        cards = [
            # Fire Gunslingers (5 cards)
            {"name": "Blazing Outlaw", "card_type": "minion", "faction": "fire_gunslingers", "rarity": "common",
             "top_value": 3, "right_value": 5, "bottom_value": 2, "left_value": 4,
             "mana_cost": 2, "attack": 3, "health": 2, "description": "Ruthless gunslinger", "unlock_level": 1},

            {"name": "Inferno Sharpshooter", "card_type": "minion", "faction": "fire_gunslingers", "rarity": "rare",
             "top_value": 6, "right_value": 5, "bottom_value": 4, "left_value": 5,
             "mana_cost": 4, "attack": 5, "health": 3, "description": "Master of flaming revolver", "unlock_level": 3},

            {"name": "Volcanic Desperado", "card_type": "minion", "faction": "fire_gunslingers", "rarity": "legendary",
             "top_value": 9, "right_value": 8, "bottom_value": 7, "left_value": 8,
             "mana_cost": 8, "attack": 8, "health": 6, "description": "Most feared gunslinger", "unlock_level": 10},

            {"name": "Ember Revolver", "card_type": "weapon", "faction": "fire_gunslingers", "rarity": "common",
             "top_value": 2, "right_value": 3, "bottom_value": 2, "left_value": 3,
             "mana_cost": 2, "attack": 3, "durability": 3, "description": "Revolver of flames", "unlock_level": 1},

            {"name": "Firestorm Bullet", "card_type": "spell", "faction": "fire_gunslingers", "rarity": "rare",
             "top_value": 5, "right_value": 4, "bottom_value": 3, "left_value": 4,
             "mana_cost": 3, "description": "Deal 4 damage to target", "unlock_level": 2},

            # Ice Mages (5 cards)
            {"name": "Frost Apprentice", "card_type": "minion", "faction": "ice_mages", "rarity": "common",
             "top_value": 2, "right_value": 4, "bottom_value": 3, "left_value": 3,
             "mana_cost": 1, "attack": 1, "health": 3, "description": "Young ice mage", "unlock_level": 1},

            {"name": "Glacier Sorcerer", "card_type": "minion", "faction": "ice_mages", "rarity": "rare",
             "top_value": 5, "right_value": 6, "bottom_value": 4, "left_value": 5,
             "mana_cost": 5, "attack": 4, "health": 6, "description": "Master of ice magic", "unlock_level": 5},

            {"name": "Frozen Lich King", "card_type": "minion", "faction": "ice_mages", "rarity": "legendary",
             "top_value": 8, "right_value": 9, "bottom_value": 7, "left_value": 8,
             "mana_cost": 9, "attack": 7, "health": 9, "description": "Ruler of frozen wastes", "unlock_level": 15},

            {"name": "Ice Staff", "card_type": "weapon", "faction": "ice_mages", "rarity": "common",
             "top_value": 3, "right_value": 2, "bottom_value": 3, "left_value": 2,
             "mana_cost": 2, "attack": 2, "durability": 4, "description": "Staff of eternal ice", "unlock_level": 1},

            {"name": "Blizzard", "card_type": "spell", "faction": "ice_mages", "rarity": "rare",
             "top_value": 4, "right_value": 5, "bottom_value": 4, "left_value": 5,
             "mana_cost": 6, "description": "Freeze all enemies", "unlock_level": 4},

            # Nature Druids (5 cards)
            {"name": "Forest Guardian", "card_type": "minion", "faction": "nature_druids", "rarity": "common",
             "top_value": 3, "right_value": 3, "bottom_value": 4, "left_value": 4,
             "mana_cost": 3, "attack": 2, "health": 5, "description": "Protector of the forest", "unlock_level": 1},

            {"name": "Ancient Treant", "card_type": "minion", "faction": "nature_druids", "rarity": "rare",
             "top_value": 6, "right_value": 5, "bottom_value": 7, "left_value": 6,
             "mana_cost": 6, "attack": 5, "health": 7, "description": "Ancient tree spirit", "unlock_level": 6},

            {"name": "Groot the Elder", "card_type": "minion", "faction": "nature_druids", "rarity": "legendary",
             "top_value": 8, "right_value": 7, "bottom_value": 9, "left_value": 8,
             "mana_cost": 10, "attack": 6, "health": 10, "description": "Eldest of treants", "unlock_level": 20},

            {"name": "Living Root Staff", "card_type": "weapon", "faction": "nature_druids", "rarity": "common",
             "top_value": 2, "right_value": 3, "bottom_value": 3, "left_value": 2,
             "mana_cost": 2, "attack": 2, "durability": 5, "description": "Staff of living wood", "unlock_level": 1},

            {"name": "Wild Growth", "card_type": "spell", "faction": "nature_druids", "rarity": "rare",
             "top_value": 5, "right_value": 4, "bottom_value": 5, "left_value": 4,
             "mana_cost": 3, "description": "Restore 6 health", "unlock_level": 2},

            # Shadow Assassins (5 cards)
            {"name": "Shadow Blade", "card_type": "minion", "faction": "shadow_assassins", "rarity": "common",
             "top_value": 4, "right_value": 3, "bottom_value": 2, "left_value": 3,
             "mana_cost": 2, "attack": 4, "health": 1, "description": "Swift assassin", "unlock_level": 1},

            {"name": "Nightstalker", "card_type": "minion", "faction": "shadow_assassins", "rarity": "rare",
             "top_value": 6, "right_value": 5, "bottom_value": 3, "left_value": 4,
             "mana_cost": 4, "attack": 6, "health": 2, "description": "Hunter of darkness", "unlock_level": 4},

            {"name": "Zed the Shadow Master", "card_type": "minion", "faction": "shadow_assassins", "rarity": "legendary",
             "top_value": 9, "right_value": 8, "bottom_value": 6, "left_value": 7,
             "mana_cost": 7, "attack": 9, "health": 4, "description": "Master of shadows", "unlock_level": 12},

            {"name": "Poison Dagger", "card_type": "weapon", "faction": "shadow_assassins", "rarity": "common",
             "top_value": 3, "right_value": 2, "bottom_value": 2, "left_value": 3,
             "mana_cost": 1, "attack": 2, "durability": 2, "description": "Poisoned blade", "unlock_level": 1},

            {"name": "Backstab", "card_type": "spell", "faction": "shadow_assassins", "rarity": "rare",
             "top_value": 4, "right_value": 5, "bottom_value": 3, "left_value": 4,
             "mana_cost": 2, "description": "Deal 6 damage instantly", "unlock_level": 3},
        ]

        for card_data in cards:
            card = Card(**card_data)
            db.add(card)

        db.commit()
        print(f"[OK] Added {len(cards)} cards successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"[ERROR] Seeding failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_basic_cards()
