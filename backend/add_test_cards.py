# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime

conn = sqlite3.connect('najika_game.db')
c = conn.cursor()

# Triple Triad Test Cards
test_cards = [
    (1, 'Squall', 'character', 'Heroes', 'rare', 10, 4, 10, 2, 0, 0, 0, 0, None, 'Legendary SeeD mercenary', None, 'https://via.placeholder.com/150?text=Squall', 'Main protagonist of FF8', 1, None, datetime.now()),
    (2, 'Zidane', 'character', 'Heroes', 'rare', 9, 6, 2, 9, 0, 0, 0, 0, None, 'Genome thief from FF9', None, 'https://via.placeholder.com/150?text=Zidane', 'Main protagonist of FF9', 1, None, datetime.now()),
    (3, 'Cloud', 'character', 'Heroes', 'rare', 10, 9, 6, 2, 0, 0, 0, 0, None, 'SOLDIER 1st Class', None, 'https://via.placeholder.com/150?text=Cloud', 'Main protagonist of FF7', 1, None, datetime.now()),
    (4, 'Sephiroth', 'character', 'Villains', 'legendary', 10, 10, 8, 1, 0, 0, 0, 0, 'Plus', 'One-Winged Angel', None, 'https://via.placeholder.com/150?text=Sephiroth', 'Main antagonist of FF7', 5, None, datetime.now()),
    (5, 'Ifrit', 'summon', 'Fire', 'rare', 9, 8, 2, 8, 0, 0, 0, 0, 'Elemental', 'Fire summon', None, 'https://via.placeholder.com/150?text=Ifrit', 'Fire-based Eidolon', 1, None, datetime.now()),
    (6, 'Shiva', 'summon', 'Ice', 'rare', 6, 9, 4, 9, 0, 0, 0, 0, 'Elemental', 'Ice summon', None, 'https://via.placeholder.com/150?text=Shiva', 'Ice-based Eidolon', 1, None, datetime.now()),
    (7, 'Bahamut', 'summon', 'Dragon', 'legendary', 10, 10, 8, 5, 0, 0, 0, 0, 'Plus', 'King of Dragons', None, 'https://via.placeholder.com/150?text=Bahamut', 'Ultimate Dragon summon', 10, None, datetime.now()),
    (8, 'Chocobo', 'creature', 'Nature', 'common', 3, 5, 5, 4, 0, 0, 0, 0, None, 'Cute yellow bird', None, 'https://via.placeholder.com/150?text=Chocobo', 'Iconic FF mascot', 1, None, datetime.now()),
    (9, 'Moogle', 'creature', 'Nature', 'common', 4, 4, 5, 3, 0, 0, 0, 0, None, 'Kupo!', None, 'https://via.placeholder.com/150?text=Moogle', 'Fluffy messenger', 1, None, datetime.now()),
    (10, 'Cactuar', 'creature', 'Nature', 'uncommon', 6, 7, 3, 5, 0, 0, 0, 0, None, '1000 Needles!', None, 'https://via.placeholder.com/150?text=Cactuar', 'Speedy cactus', 1, None, datetime.now()),
    (11, 'Tonberry', 'creature', 'Dark', 'uncommon', 3, 6, 8, 4, 0, 0, 0, 0, 'Counter', 'Grudge attack', None, 'https://via.placeholder.com/150?text=Tonberry', 'Slow but deadly', 1, None, datetime.now()),
    (12, 'Odin', 'summon', 'Lightning', 'legendary', 8, 9, 10, 2, 0, 0, 0, 0, 'Same', 'Zantetsuken instant kill', None, 'https://via.placeholder.com/150?text=Odin', 'Norse god summon', 8, None, datetime.now()),
]

print("[INFO] Adding cards to database...")
for card in test_cards:
    c.execute('''INSERT OR REPLACE INTO cards
                 (id, name, card_type, faction, rarity, top_value, right_value, bottom_value, left_value,
                  mana_cost, attack, health, durability, effect_type, effect_description, effect_script,
                  image_url, description, unlock_level, unlock_quest_id, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', card)

print("[INFO] Adding cards to player collection...")
for card_id in range(1, 13):
    c.execute('''INSERT OR REPLACE INTO player_card_collections
                 (player_id, card_id, copies_owned, is_golden, times_played, times_won_with, acquired_at)
                 VALUES (1, ?, 3, 0, 0, 0, ?)''', (card_id, datetime.now()))

conn.commit()
conn.close()
print("[OK] Added 12 Triple Triad test cards!")
print("[OK] Player 1 has all cards (3 copies each)!")
