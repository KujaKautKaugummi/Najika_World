"""
Dungeon Dice Monsters Models - Najika World
Yu-Gi-Oh DDM Inspired System
Fantasy-Western Setting
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class DiceMonster(Base):
    """Dice Monster definition (static dice pool)"""
    __tablename__ = "dice_monsters"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(100), nullable=False, unique=True)
    monster_type = Column(String(50), nullable=False)  # beast, dragon, warrior, mage, undead, etc.
    element = Column(String(20), nullable=False)  # fire, water, earth, wind, light, dark
    rarity = Column(String(20), nullable=False)  # common, uncommon, rare, epic, legendary

    # Dice Stats
    dice_level = Column(Integer, default=1)  # 1-10 (determines board space cost)
    attack = Column(Integer, default=1)  # 1-12
    defense = Column(Integer, default=1)  # 1-12
    movement = Column(Integer, default=2)  # 1-5 spaces

    # Crest System (like mana in DDM)
    summon_cost = Column(Integer, default=1)  # Number of crests needed
    crest_type = Column(String(20), nullable=False)  # fire, water, earth, wind, light, dark

    # Special Abilities
    ability_name = Column(String(100), nullable=True)
    ability_description = Column(Text, nullable=True)
    ability_script = Column(JSON, nullable=True)  # Script for ability logic

    # Visual
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    # Unlock Requirements
    unlock_level = Column(Integer, default=1)
    unlock_quest_id = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.monster_type,
            "element": self.element,
            "rarity": self.rarity,
            "dice_level": self.dice_level,
            "stats": {
                "attack": self.attack,
                "defense": self.defense,
                "movement": self.movement
            },
            "summon": {
                "cost": self.summon_cost,
                "crest_type": self.crest_type
            },
            "ability": {
                "name": self.ability_name,
                "description": self.ability_description,
                "script": self.ability_script
            },
            "image_url": self.image_url,
            "description": self.description,
            "unlock_level": self.unlock_level
        }


class PlayerDiceCollection(Base):
    """Player's owned dice monsters"""
    __tablename__ = "player_dice_collections"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dice_monster_id = Column(Integer, ForeignKey("dice_monsters.id"), nullable=False)

    # Ownership
    copies_owned = Column(Integer, default=1)  # Can have multiple copies
    is_golden = Column(Boolean, default=False)  # Premium shiny version

    # Stats
    times_summoned = Column(Integer, default=0)
    times_won_with = Column(Integer, default=0)
    total_damage_dealt = Column(Integer, default=0)

    # Timestamps
    acquired_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="dice_collection")
    dice_monster = relationship("DiceMonster")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "dice_monster_id": self.dice_monster_id,
            "copies_owned": self.copies_owned,
            "is_golden": self.is_golden,
            "times_summoned": self.times_summoned,
            "times_won_with": self.times_won_with,
            "total_damage_dealt": self.total_damage_dealt,
            "acquired_at": self.acquired_at.isoformat() if self.acquired_at else None
        }


class DiceDuelMatch(Base):
    """Dice Duel match history"""
    __tablename__ = "dice_duel_matches"

    id = Column(Integer, primary_key=True, index=True)

    # Players
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null if vs NPC

    # Match Settings
    is_ranked = Column(Boolean, default=False)
    is_vs_npc = Column(Boolean, default=False)
    npc_name = Column(String(100), nullable=True)

    # Dungeon Master HP (each player starts with 3000 LP in DDM)
    player1_starting_hp = Column(Integer, default=3000)
    player2_starting_hp = Column(Integer, default=3000)
    player1_final_hp = Column(Integer, default=0)
    player2_final_hp = Column(Integer, default=0)

    # Dice Pools Used (JSON: list of dice_monster_ids)
    player1_dice_pool = Column(JSON, nullable=False)  # [1, 3, 5, 7, 9, ...] (12 dice)
    player2_dice_pool = Column(JSON, nullable=True)

    # Result
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    turns_played = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)

    # Final Board State
    final_board = Column(JSON, nullable=True)  # Grid with monster positions

    # Match Statistics
    total_dice_rolled = Column(Integer, default=0)
    total_monsters_summoned = Column(Integer, default=0)
    total_damage_dealt = Column(Integer, default=0)

    # Rewards
    gold_earned = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    dice_won = Column(JSON, nullable=True)  # List of dice_monster IDs won

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "is_ranked": self.is_ranked,
            "is_vs_npc": self.is_vs_npc,
            "npc_name": self.npc_name,
            "hp": {
                "player1_start": self.player1_starting_hp,
                "player2_start": self.player2_starting_hp,
                "player1_final": self.player1_final_hp,
                "player2_final": self.player2_final_hp
            },
            "dice_pools": {
                "player1": self.player1_dice_pool or [],
                "player2": self.player2_dice_pool or []
            },
            "winner_id": self.winner_id,
            "turns_played": self.turns_played,
            "duration_seconds": self.duration_seconds,
            "final_board": self.final_board,
            "stats": {
                "total_dice_rolled": self.total_dice_rolled,
                "total_monsters_summoned": self.total_monsters_summoned,
                "total_damage_dealt": self.total_damage_dealt
            },
            "rewards": {
                "gold_earned": self.gold_earned,
                "xp_earned": self.xp_earned,
                "dice_won": self.dice_won or []
            },
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None
        }
