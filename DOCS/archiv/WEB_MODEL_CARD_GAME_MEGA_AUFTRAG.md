# 🃏 WEB MODEL - CARD GAME MEGA AUFTRAG
**Datum:** 2025-11-18 12:30
**Branch:** `claude/remote-access-setup-011CUt97k27tgaNUMZdyA9DY`
**Auftraggeber:** Kuja
**Status:** 🟡 MEGA AUFTRAG - KOMPLETT NEUES SYSTEM!

---

## 🎯 MISSION: CARD GAME SYSTEME ERSTELLEN

**Ziel:** 2 vollständige Card Game Systeme für Najika World:

### **1. HYBRID CARD GAME (Hauptspiel)**
**Inspiration:** Triple Triad (FF8) + Hearthstone
**Setting:** Fantasy-Western (unsere Welt)
**Wo spielbar:** Normale Welt (Taverne, NPCs, PvP)

### **2. DUNGEON DICE MONSTERS (Modul)**
**Inspiration:** Yu-Gi-Oh! Dungeon Dice Monsters
**Setting:** Angepasst an Najika World
**Wo spielbar:** Extra Modul/Arena

---

## 📋 TEIL 1: HYBRID CARD GAME (Triple Triad + Hearthstone)

### 🎴 **GAME MECHANICS:**

#### **Von Triple Triad (FF8):**
- ✅ **3×3 Grid Board** - Strategisches Platzieren
- ✅ **Directional Values** - Jede Karte hat 4 Werte (Top, Right, Bottom, Left)
- ✅ **Capture Mechanic** - Höhere Werte übernehmen gegnerische Karten
- ✅ **Same/Plus Rule** - Bonus-Mechanic für gleiche Werte
- ✅ **Einfache Regeln** - Easy to learn, hard to master

#### **Von Hearthstone (Blizzard):**
- ✅ **Mana System** - Ressourcen pro Runde (1-10 Mana)
- ✅ **Card Types** - Minions, Spells, Weapons
- ✅ **Card Effects** - Battlecry, Deathrattle, etc.
- ✅ **Hero Powers** - Spezialfähigkeiten
- ✅ **Deck Building** - 30 Karten Deck

#### **Fantasy-Western Twist:**
- ✅ **Fraktionen:**
  - 🔥 Fire Gunslingers (Feuer-Revolverhelden)
  - ❄️ Ice Mages (Eis-Magier)
  - ⚡ Lightning Outlaws (Blitz-Banditen)
  - 🌱 Nature Rangers (Natur-Ranger)
  - 💀 Shadow Necromancers (Schatten-Nekromanten)
  - ✨ Holy Templars (Licht-Templer)

- ✅ **Card Rarities:**
  - Common (Grau)
  - Uncommon (Grün)
  - Rare (Blau)
  - Epic (Lila)
  - Legendary (Orange)

- ✅ **Win Conditions:**
  - **Triple Triad Mode:** Meiste Karten auf Board kontrollieren
  - **Hearthstone Mode:** Gegner-HP auf 0 reduzieren

---

### 🗃️ **DATABASE MODELS:**

#### **Model 1: `backend/models/card_game.py`**

```python
"""
Card Game Models - Najika World
Hybrid Triple Triad + Hearthstone System
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Card(Base):
    """Card definition (static card pool)"""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(100), nullable=False, unique=True)
    card_type = Column(String(20), nullable=False)  # minion, spell, weapon
    faction = Column(String(50), nullable=False)  # fire_gunslingers, ice_mages, etc.
    rarity = Column(String(20), nullable=False)  # common, uncommon, rare, epic, legendary

    # Triple Triad Stats
    top_value = Column(Integer, default=1)  # 1-10
    right_value = Column(Integer, default=1)
    bottom_value = Column(Integer, default=1)
    left_value = Column(Integer, default=1)

    # Hearthstone Stats
    mana_cost = Column(Integer, default=1)  # 0-10
    attack = Column(Integer, default=1)  # For minions
    health = Column(Integer, default=1)  # For minions
    durability = Column(Integer, default=3)  # For weapons

    # Card Effects
    effect_type = Column(String(50), nullable=True)  # battlecry, deathrattle, taunt, etc.
    effect_description = Column(Text, nullable=True)
    effect_script = Column(JSON, nullable=True)  # Script für Effect Logic

    # Visual
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    # Unlock Requirements
    unlock_level = Column(Integer, default=1)
    unlock_quest_id = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class PlayerCardCollection(Base):
    """Player's owned cards"""
    __tablename__ = "player_card_collections"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)

    # Ownership
    copies_owned = Column(Integer, default=1)  # Can have multiple copies
    is_golden = Column(Boolean, default=False)  # Premium version

    # Stats
    times_played = Column(Integer, default=0)
    times_won_with = Column(Integer, default=0)

    # Timestamps
    acquired_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="card_collection")
    card = relationship("Card")


class PlayerDeck(Base):
    """Player's card decks (30 cards)"""
    __tablename__ = "player_decks"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Deck Info
    deck_name = Column(String(100), nullable=False)
    faction = Column(String(50), nullable=False)  # Primary faction
    is_active = Column(Boolean, default=False)  # Currently selected deck

    # Card List (JSON: {card_id: count})
    cards = Column(JSON, nullable=False)  # {"1": 2, "5": 1, "12": 2, ...} (30 total)

    # Stats
    total_games = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="card_decks")


class CardGameMatch(Base):
    """Card game match history"""
    __tablename__ = "card_game_matches"

    id = Column(Integer, primary_key=True, index=True)

    # Players
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null if vs NPC

    # Match Settings
    game_mode = Column(String(20), nullable=False)  # triad, hearthstone, hybrid
    is_ranked = Column(Boolean, default=False)
    is_vs_npc = Column(Boolean, default=False)
    npc_name = Column(String(100), nullable=True)

    # Decks Used
    player1_deck_id = Column(Integer, ForeignKey("player_decks.id"))
    player2_deck_id = Column(Integer, ForeignKey("player_decks.id"), nullable=True)

    # Result
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    turns_played = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)

    # Final Board State (for Triple Triad mode)
    final_board = Column(JSON, nullable=True)  # 3x3 grid

    # Rewards
    gold_earned = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    cards_won = Column(JSON, nullable=True)  # List of card IDs won

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])


class CardGameRanking(Base):
    """Player rankings for card game"""
    __tablename__ = "card_game_rankings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Rankings
    elo_rating = Column(Integer, default=1000)  # ELO rating
    rank_tier = Column(String(20), default="bronze")  # bronze, silver, gold, platinum, diamond, legend

    # Stats
    ranked_wins = Column(Integer, default=0)
    ranked_losses = Column(Integer, default=0)
    ranked_draws = Column(Integer, default=0)
    win_streak = Column(Integer, default=0)
    best_win_streak = Column(Integer, default=0)

    # Season
    season = Column(Integer, default=1)
    season_high_rank = Column(String(20), default="bronze")

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="card_game_ranking")


# Helper method to add to User model (in models/user.py):
# card_collection = relationship("PlayerCardCollection", back_populates="player")
# card_decks = relationship("PlayerDeck", back_populates="player")
# card_game_ranking = relationship("CardGameRanking", back_populates="player", uselist=False)
```

---

### 🎮 **API ENDPOINTS:**

#### **File: `backend/api/card_game.py`**

```python
"""
Card Game API - Najika World
Hybrid Triple Triad + Hearthstone System
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.card_game import (
    Card, PlayerCardCollection, PlayerDeck,
    CardGameMatch, CardGameRanking
)
from typing import List, Optional
import random

router = APIRouter(prefix="/api/card-game", tags=["card-game"])


# ============================================================================
# REQUEST MODELS
# ============================================================================

class CreateDeckRequest(BaseModel):
    deck_name: str
    faction: str
    cards: dict  # {card_id: count}


class StartMatchRequest(BaseModel):
    game_mode: str  # triad, hearthstone, hybrid
    is_ranked: bool = False
    opponent_id: Optional[int] = None  # Null = vs NPC
    deck_id: int


class PlayCardRequest(BaseModel):
    match_id: int
    card_id: int
    position: Optional[dict] = None  # {x: 0, y: 0} for Triple Triad


# ============================================================================
# CARD COLLECTION ENDPOINTS
# ============================================================================

@router.get("/cards/all")
async def get_all_cards(db: Session = Depends(get_db)):
    """Get all available cards"""
    cards = db.query(Card).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "type": c.card_type,
            "faction": c.faction,
            "rarity": c.rarity,
            "mana": c.mana_cost,
            "attack": c.attack,
            "health": c.health,
            "triad_values": {
                "top": c.top_value,
                "right": c.right_value,
                "bottom": c.bottom_value,
                "left": c.left_value
            },
            "effect": c.effect_description
        }
        for c in cards
    ]


@router.get("/collection/{player_id}")
async def get_player_collection(player_id: int, db: Session = Depends(get_db)):
    """Get player's card collection"""
    collection = db.query(PlayerCardCollection).filter(
        PlayerCardCollection.player_id == player_id
    ).all()

    cards_data = []
    for item in collection:
        card = db.query(Card).filter(Card.id == item.card_id).first()
        if card:
            cards_data.append({
                "card_id": card.id,
                "name": card.name,
                "copies": item.copies_owned,
                "is_golden": item.is_golden,
                "times_played": item.times_played
            })

    return {
        "player_id": player_id,
        "total_cards": len(cards_data),
        "cards": cards_data
    }


@router.post("/collection/add")
async def add_card_to_collection(
    player_id: int,
    card_id: int,
    db: Session = Depends(get_db)
):
    """Add card to player collection"""
    # Check if card exists
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(404, "Card not found")

    # Check if already owned
    existing = db.query(PlayerCardCollection).filter(
        PlayerCardCollection.player_id == player_id,
        PlayerCardCollection.card_id == card_id
    ).first()

    if existing:
        existing.copies_owned += 1
        db.commit()
        return {"message": f"Added another copy of {card.name}", "copies": existing.copies_owned}
    else:
        new_item = PlayerCardCollection(
            player_id=player_id,
            card_id=card_id,
            copies_owned=1
        )
        db.add(new_item)
        db.commit()
        return {"message": f"Added {card.name} to collection", "copies": 1}


# ============================================================================
# DECK ENDPOINTS
# ============================================================================

@router.get("/decks/{player_id}")
async def get_player_decks(player_id: int, db: Session = Depends(get_db)):
    """Get all player decks"""
    decks = db.query(PlayerDeck).filter(PlayerDeck.player_id == player_id).all()
    return [
        {
            "id": d.id,
            "name": d.deck_name,
            "faction": d.faction,
            "is_active": d.is_active,
            "cards": d.cards,
            "wins": d.total_wins,
            "games": d.total_games,
            "win_rate": d.win_rate
        }
        for d in decks
    ]


@router.post("/decks/create")
async def create_deck(
    player_id: int,
    request: CreateDeckRequest,
    db: Session = Depends(get_db)
):
    """Create new deck"""
    # Validate 30 cards
    total_cards = sum(request.cards.values())
    if total_cards != 30:
        raise HTTPException(400, f"Deck must have exactly 30 cards (got {total_cards})")

    # Validate player owns all cards
    for card_id, count in request.cards.items():
        owned = db.query(PlayerCardCollection).filter(
            PlayerCardCollection.player_id == player_id,
            PlayerCardCollection.card_id == int(card_id)
        ).first()

        if not owned or owned.copies_owned < count:
            raise HTTPException(400, f"Not enough copies of card {card_id}")

    # Create deck
    new_deck = PlayerDeck(
        player_id=player_id,
        deck_name=request.deck_name,
        faction=request.faction,
        cards=request.cards
    )
    db.add(new_deck)
    db.commit()
    db.refresh(new_deck)

    return {
        "success": True,
        "deck_id": new_deck.id,
        "message": f"Deck '{request.deck_name}' created"
    }


@router.post("/decks/{deck_id}/set-active")
async def set_active_deck(deck_id: int, player_id: int, db: Session = Depends(get_db)):
    """Set active deck"""
    # Deactivate all decks
    db.query(PlayerDeck).filter(PlayerDeck.player_id == player_id).update({"is_active": False})

    # Activate selected deck
    deck = db.query(PlayerDeck).filter(PlayerDeck.id == deck_id).first()
    if not deck:
        raise HTTPException(404, "Deck not found")

    deck.is_active = True
    db.commit()

    return {"success": True, "active_deck": deck.deck_name}


# ============================================================================
# MATCH ENDPOINTS
# ============================================================================

@router.post("/match/start")
async def start_match(
    player_id: int,
    request: StartMatchRequest,
    db: Session = Depends(get_db)
):
    """Start card game match"""
    # Get deck
    deck = db.query(PlayerDeck).filter(PlayerDeck.id == request.deck_id).first()
    if not deck:
        raise HTTPException(404, "Deck not found")

    # Determine opponent
    is_vs_npc = request.opponent_id is None
    npc_name = None

    if is_vs_npc:
        npcs = ["Gunslinger Jake", "Ice Mage Elsa", "Lightning Outlaw Bolt", "Nature Ranger Green"]
        npc_name = random.choice(npcs)

    # Create match
    new_match = CardGameMatch(
        player1_id=player_id,
        player2_id=request.opponent_id,
        game_mode=request.game_mode,
        is_ranked=request.is_ranked,
        is_vs_npc=is_vs_npc,
        npc_name=npc_name,
        player1_deck_id=request.deck_id
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return {
        "match_id": new_match.id,
        "game_mode": request.game_mode,
        "opponent": npc_name if is_vs_npc else f"Player {request.opponent_id}",
        "message": "Match started!"
    }


@router.get("/match/{match_id}")
async def get_match_state(match_id: int, db: Session = Depends(get_db)):
    """Get current match state"""
    match = db.query(CardGameMatch).filter(CardGameMatch.id == match_id).first()
    if not match:
        raise HTTPException(404, "Match not found")

    return {
        "match_id": match.id,
        "game_mode": match.game_mode,
        "turns": match.turns_played,
        "board": match.final_board,
        "started_at": match.started_at,
        "ended_at": match.ended_at,
        "winner_id": match.winner_id
    }


@router.post("/match/end")
async def end_match(
    match_id: int,
    winner_id: int,
    final_board: dict,
    db: Session = Depends(get_db)
):
    """End match and calculate rewards"""
    match = db.query(CardGameMatch).filter(CardGameMatch.id == match_id).first()
    if not match:
        raise HTTPException(404, "Match not found")

    match.winner_id = winner_id
    match.final_board = final_board
    match.ended_at = datetime.utcnow()

    # Calculate rewards
    gold_reward = 100 if match.is_ranked else 50
    xp_reward = 200 if match.is_ranked else 100

    # Random card reward (10% chance)
    cards_won = []
    if random.random() < 0.1:
        random_card = db.query(Card).order_by(db.func.random()).first()
        if random_card:
            cards_won.append(random_card.id)

    match.gold_earned = gold_reward
    match.xp_earned = xp_reward
    match.cards_won = cards_won

    # Update deck stats
    if match.player1_id == winner_id:
        winning_deck = db.query(PlayerDeck).filter(PlayerDeck.id == match.player1_deck_id).first()
        if winning_deck:
            winning_deck.total_wins += 1
            winning_deck.total_games += 1
            winning_deck.win_rate = winning_deck.total_wins / winning_deck.total_games

    db.commit()

    return {
        "winner_id": winner_id,
        "gold_earned": gold_reward,
        "xp_earned": xp_reward,
        "cards_won": cards_won,
        "message": "Match ended!"
    }


# ============================================================================
# RANKING ENDPOINTS
# ============================================================================

@router.get("/rankings")
async def get_rankings(limit: int = 100, db: Session = Depends(get_db)):
    """Get top players rankings"""
    rankings = db.query(CardGameRanking).order_by(
        CardGameRanking.elo_rating.desc()
    ).limit(limit).all()

    return [
        {
            "rank": idx + 1,
            "player_id": r.player_id,
            "elo": r.elo_rating,
            "tier": r.rank_tier,
            "wins": r.ranked_wins,
            "losses": r.ranked_losses,
            "win_streak": r.win_streak
        }
        for idx, r in enumerate(rankings)
    ]


@router.get("/ranking/{player_id}")
async def get_player_ranking(player_id: int, db: Session = Depends(get_db)):
    """Get player ranking"""
    ranking = db.query(CardGameRanking).filter(
        CardGameRanking.player_id == player_id
    ).first()

    if not ranking:
        # Create new ranking
        ranking = CardGameRanking(player_id=player_id)
        db.add(ranking)
        db.commit()
        db.refresh(ranking)

    return {
        "player_id": player_id,
        "elo": ranking.elo_rating,
        "tier": ranking.rank_tier,
        "wins": ranking.ranked_wins,
        "losses": ranking.ranked_losses,
        "win_rate": ranking.ranked_wins / (ranking.ranked_wins + ranking.ranked_losses) if (ranking.ranked_wins + ranking.ranked_losses) > 0 else 0,
        "win_streak": ranking.win_streak,
        "best_streak": ranking.best_win_streak
    }
```

---

### 🎨 **FRONTEND UI:**

#### **File: `digivice/js/ui/card_game_ui.js`**

**Features:**
- 3×3 Grid Board (Triple Triad)
- Card Hand Display (Hearthstone)
- Mana Counter
- Deck Viewer
- Collection Manager
- Match History

---

## 📋 TEIL 2: DUNGEON DICE MONSTERS

### 🎲 **GAME MECHANICS:**

#### **Von Yu-Gi-Oh! DDM:**
- ✅ **Dice Monsters** - Würfel mit verschiedenen Monstern
- ✅ **Board Movement** - Tactical grid movement
- ✅ **Dice Rolling** - RNG für Monster Summon
- ✅ **Crest System** - Ressourcen sammeln
- ✅ **Dungeon Master HP** - Zerstöre gegnerischen DM

#### **Najika World Twist:**
- ✅ **Fantasy-Western Monsters** statt Yu-Gi-Oh Monsters
- ✅ **Regions als Boards** - Jede Region = Unique Arena
- ✅ **Würfel-Types:**
  - 🔥 Fire Dice (Revolverheld-Monster)
  - ❄️ Ice Dice (Eis-Magier-Monster)
  - ⚡ Lightning Dice (Blitz-Monster)
  - 🌱 Nature Dice (Natur-Monster)
  - 💀 Shadow Dice (Schatten-Monster)
  - ✨ Light Dice (Licht-Monster)

---

### 🗃️ **DATABASE MODELS:**

#### **Model 2: `backend/models/dice_monsters.py`**

```python
"""
Dungeon Dice Monsters Models - Najika World
Yu-Gi-Oh! DDM inspired system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class DiceMonster(Base):
    """Dice Monster definition"""
    __tablename__ = "dice_monsters"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(100), nullable=False, unique=True)
    monster_type = Column(String(50), nullable=False)  # fire, ice, lightning, nature, shadow, light
    rarity = Column(String(20), nullable=False)

    # Dice Stats
    dice_level = Column(Integer, default=1)  # 1-4 star
    crest_cost = Column(Integer, default=1)  # Crests needed to summon

    # Monster Stats
    attack = Column(Integer, default=1)
    defense = Column(Integer, default=1)
    movement = Column(Integer, default=1)  # Squares per turn

    # Abilities
    special_ability = Column(String(100), nullable=True)
    ability_description = Column(Text, nullable=True)

    # Visual
    image_url = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class PlayerDiceCollection(Base):
    """Player's dice collection"""
    __tablename__ = "player_dice_collections"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dice_id = Column(Integer, ForeignKey("dice_monsters.id"), nullable=False)

    # Ownership
    dice_owned = Column(Integer, default=1)

    # Stats
    times_used = Column(Integer, default=0)
    wins_with = Column(Integer, default=0)

    # Timestamps
    acquired_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("User")
    dice = relationship("DiceMonster")


class DiceDuelMatch(Base):
    """Dice duel match history"""
    __tablename__ = "dice_duel_matches"

    id = Column(Integer, primary_key=True, index=True)

    # Players
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null if vs NPC

    # Match Settings
    arena_region = Column(String(100), default="samtmoos_tiefwald")
    is_ranked = Column(Boolean, default=False)
    is_vs_npc = Column(Boolean, default=False)
    npc_name = Column(String(100), nullable=True)

    # Result
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    turns_played = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)

    # Final Board State
    final_board = Column(JSON, nullable=True)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
```

---

### 🎮 **API ENDPOINTS:**

#### **File: `backend/api/dice_monsters.py`**

```python
"""
Dice Monsters API - Najika World
Yu-Gi-Oh! DDM inspired system
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.dice_monsters import DiceMonster, PlayerDiceCollection, DiceDuelMatch
import random

router = APIRouter(prefix="/api/dice-monsters", tags=["dice-monsters"])


@router.get("/dice/all")
async def get_all_dice(db: Session = Depends(get_db)):
    """Get all dice monsters"""
    dice = db.query(DiceMonster).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "type": d.monster_type,
            "level": d.dice_level,
            "attack": d.attack,
            "defense": d.defense,
            "movement": d.movement,
            "ability": d.special_ability
        }
        for d in dice
    ]


@router.get("/collection/{player_id}")
async def get_player_dice_collection(player_id: int, db: Session = Depends(get_db)):
    """Get player's dice collection"""
    collection = db.query(PlayerDiceCollection).filter(
        PlayerDiceCollection.player_id == player_id
    ).all()

    return {
        "player_id": player_id,
        "total_dice": len(collection),
        "dice": [
            {
                "dice_id": item.dice_id,
                "owned": item.dice_owned,
                "times_used": item.times_used
            }
            for item in collection
        ]
    }


@router.post("/duel/start")
async def start_dice_duel(
    player_id: int,
    opponent_id: int = None,
    arena_region: str = "samtmoos_tiefwald",
    db: Session = Depends(get_db)
):
    """Start dice duel"""
    is_vs_npc = opponent_id is None
    npc_name = None

    if is_vs_npc:
        npcs = ["Dice Master Alex", "Shadow Roller Emma", "Lightning Duke"]
        npc_name = random.choice(npcs)

    new_match = DiceDuelMatch(
        player1_id=player_id,
        player2_id=opponent_id,
        arena_region=arena_region,
        is_vs_npc=is_vs_npc,
        npc_name=npc_name
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return {
        "match_id": new_match.id,
        "arena": arena_region,
        "opponent": npc_name if is_vs_npc else f"Player {opponent_id}",
        "message": "Dice Duel started!"
    }
```

---

## 🎯 **PRIORITIES:**

### 🔴 **PHASE 1: HYBRID CARD GAME (HAUPTFOKUS)**

1. **Database Models erstellen** (30 min)
   - card_game.py mit allen 5 Models

2. **API Endpoints** (2h)
   - Collection, Decks, Matches, Rankings

3. **Starter Cards erstellen** (30 min)
   - 100 Basic Cards in Database seeden
   - Alle 6 Fraktionen
   - Common bis Legendary

4. **Frontend UI** (3h)
   - Card Game UI (Triple Triad Board + Hearthstone Hand)
   - Collection Viewer
   - Deck Builder

**Zeit:** ~6 Stunden

---

### 🟡 **PHASE 2: DUNGEON DICE MONSTERS (MODUL)**

1. **Database Models** (20 min)
2. **API Endpoints** (1h)
3. **Starter Dice** (20 min)
4. **Frontend UI** (2h)

**Zeit:** ~4 Stunden

---

### 🟢 **PHASE 3: INTEGRATION**

1. **Add to Digivice Menu**
2. **Taverne/NPC Integration**
3. **Arena Module**

**Zeit:** ~1 Stunde

---

## 📦 **DELIVERABLES:**

### ✅ **Backend:**
- [ ] `backend/models/card_game.py` (5 Models, 6 Tables)
- [ ] `backend/models/dice_monsters.py` (3 Models, 3 Tables)
- [ ] `backend/api/card_game.py` (15+ Endpoints)
- [ ] `backend/api/dice_monsters.py` (8+ Endpoints)
- [ ] Migration erstellt & angewendet
- [ ] Starter Cards/Dice in Database

### ✅ **Frontend:**
- [ ] `digivice/js/ui/card_game_ui.js` (Triple Triad + Hearthstone Hybrid)
- [ ] `digivice/js/ui/dice_monsters_ui.js` (DDM Board + Dice Rolling)
- [ ] `digivice/static/css/card_game.css`
- [ ] Menu Integration

### ✅ **Documentation:**
- [ ] `CARD_GAME_COMPLETE_REPORT.md`
- [ ] Game Rules Documentation
- [ ] API Reference

---

## 🚀 **ZUSÄTZLICH: DIGIVICE UI INTEGRATION (aus vorherigem Auftrag)**

**AUCH MACHEN:**
1. ✅ `index.html` updaten (Script Tags, Init, Menu)
2. ✅ `game_systems.css` erstellen
3. ✅ Alle 5 Game Systems UIs aktivieren

**Zeit:** ~1 Stunde

---

## 📊 **TOTAL TIME ESTIMATE:**

```
Digivice UI Integration:  1h
Card Game System:         6h
Dice Monsters System:     4h
Integration:              1h
──────────────────────────────
TOTAL:                    12h
```

---

## 🎯 **ERFOLGSKRITERIEN:**

### Card Game:
- [ ] Kann Deck mit 30 Karten erstellen
- [ ] Kann Match vs NPC starten
- [ ] Triple Triad Board funktioniert
- [ ] Hearthstone Mana System funktioniert
- [ ] Karten haben korrekte Stats
- [ ] Rankings funktionieren

### Dice Monsters:
- [ ] Kann Dice Collection sehen
- [ ] Kann Duel vs NPC starten
- [ ] Board Movement funktioniert
- [ ] Dice Rolling funktioniert

### Digivice:
- [ ] Alle 5 Game Systems UIs laden
- [ ] Menu Buttons funktionieren
- [ ] Keine Console Errors

---

**VIEL ERFOLG!** 🎴🎲

Kuja + Local Claude
2025-11-18 12:30
