"""
Card Game API - Najika World
=============================

REST API für Triple Triad Card Game System (FastAPI) (DATABASE)
Triple Triad gameplay with Hearthstone-style stone visuals
Fantasy-Western Setting

Endpoints:
- GET /api/cards - Get all cards (static pool)
- GET /api/cards/{card_id} - Get specific card
- POST /api/cards/add-to-collection - Add card to player collection
- GET /api/cards/collection/{player_id} - Get player's card collection

- POST /api/decks/create - Create new deck
- GET /api/decks/{player_id} - Get all player decks
- PUT /api/decks/{deck_id} - Update deck
- DELETE /api/decks/{deck_id} - Delete deck
- POST /api/decks/{deck_id}/activate - Set active deck

- POST /api/matches/start - Start new match
- POST /api/matches/end - End match and record results
- GET /api/matches/history/{player_id} - Get match history
- GET /api/matches/{match_id} - Get specific match

- GET /api/rankings/leaderboard - Get top rankings
- GET /api/rankings/{player_id} - Get player ranking
- POST /api/rankings/update - Update ELO after match

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database import get_db
from backend.models.card_game import (
    Card, PlayerCardCollection, PlayerDeck, CardGameMatch, CardGameRanking
)
from backend.utils import handle_errors

# Create FastAPI Router
router = APIRouter(prefix="/api/cards", tags=["card_game"])

# Additional router for matches and rankings
matches_router = APIRouter(prefix="/api/matches", tags=["card_matches"])
rankings_router = APIRouter(prefix="/api/rankings", tags=["card_rankings"])
decks_router = APIRouter(prefix="/api/decks", tags=["card_decks"])


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class AddCardToCollectionRequest(BaseModel):
    player_id: int
    card_id: int
    is_golden: bool = False


class CreateDeckRequest(BaseModel):
    player_id: int
    deck_name: str
    faction: str
    cards: Dict[str, int]  # {"card_id": count} totaling 30


class UpdateDeckRequest(BaseModel):
    deck_name: Optional[str] = None
    cards: Optional[Dict[str, int]] = None


class StartMatchRequest(BaseModel):
    player1_id: int
    player2_id: Optional[int] = None
    game_mode: str = "triad"  # Only Triple Triad supported
    is_ranked: bool = False
    is_vs_npc: bool = False
    npc_name: Optional[str] = None
    player1_deck_id: int
    player2_deck_id: Optional[int] = None


class EndMatchRequest(BaseModel):
    match_id: int
    winner_id: Optional[int] = None
    turns_played: int
    duration_seconds: int
    final_board: Optional[Dict] = None
    gold_earned: int = 0
    xp_earned: int = 0
    cards_won: Optional[List[int]] = None


class UpdateRankingRequest(BaseModel):
    player_id: int
    elo_change: int
    won: bool


# ============================================================================
# CARDS ENDPOINTS
# ============================================================================

@router.get("")
@handle_errors()
async def get_all_cards(
    faction: Optional[str] = Query(None, description="Filter by faction"),
    rarity: Optional[str] = Query(None, description="Filter by rarity"),
    card_type: Optional[str] = Query(None, description="Filter by type"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get All Cards (DATABASE)

    Query Params:
        faction: str (optional) - fire_gunslingers, ice_mages, etc.
        rarity: str (optional) - common, uncommon, rare, epic, legendary
        card_type: str (optional) - minion, spell, weapon
        limit: int (default 100)

    Example: /api/cards?faction=fire_gunslingers&rarity=legendary
    """
    try:
        query = db.query(Card)

        if faction:
            query = query.filter(Card.faction == faction)
        if rarity:
            query = query.filter(Card.rarity == rarity)
        if card_type:
            query = query.filter(Card.card_type == card_type)

        cards = query.limit(limit).all()

        return {
            "cards": [card.to_dict() for card in cards],
            "count": len(cards)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{card_id}")
@handle_errors()
async def get_card(card_id: int, db: Session = Depends(get_db)):
    """
    Get Specific Card (DATABASE)

    Path: /api/cards/5
    """
    try:
        card = db.query(Card).filter(Card.id == card_id).first()

        if not card:
            raise HTTPException(status_code=404, detail=f"Card {card_id} not found")

        return card.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-to-collection")
@handle_errors()
async def add_card_to_collection(request: AddCardToCollectionRequest, db: Session = Depends(get_db)):
    """
    Add Card to Player Collection (DATABASE)

    Body:
    {
        "player_id": 1,
        "card_id": 5,
        "is_golden": false
    }
    """
    try:
        # Check if card exists
        card = db.query(Card).filter(Card.id == request.card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail=f"Card {request.card_id} not found")

        # Check if player already owns this card
        existing = db.query(PlayerCardCollection).filter(
            PlayerCardCollection.player_id == request.player_id,
            PlayerCardCollection.card_id == request.card_id,
            PlayerCardCollection.is_golden == request.is_golden
        ).first()

        if existing:
            # Increment copies
            existing.copies_owned += 1
            db.commit()
            db.refresh(existing)
            return {
                "success": True,
                "message": f"Added another copy of {card.name}",
                "collection_entry": existing.to_dict()
            }
        else:
            # Create new entry
            collection_entry = PlayerCardCollection(
                player_id=request.player_id,
                card_id=request.card_id,
                is_golden=request.is_golden,
                copies_owned=1
            )
            db.add(collection_entry)
            db.commit()
            db.refresh(collection_entry)

            return {
                "success": True,
                "message": f"Added {card.name} to collection!",
                "collection_entry": collection_entry.to_dict()
            }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collection/{player_id}")
@handle_errors()
async def get_player_collection(player_id: int, db: Session = Depends(get_db)):
    """
    Get Player's Card Collection (DATABASE)

    Path: /api/cards/collection/1
    """
    try:
        collection = db.query(PlayerCardCollection).filter(
            PlayerCardCollection.player_id == player_id
        ).all()

        # Join with card data
        collection_with_cards = []
        for entry in collection:
            card = db.query(Card).filter(Card.id == entry.card_id).first()
            collection_with_cards.append({
                "collection": entry.to_dict(),
                "card": card.to_dict() if card else None
            })

        return {
            "player_id": player_id,
            "collection": collection_with_cards,
            "total_cards": len(collection_with_cards)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DECK ENDPOINTS
# ============================================================================

@decks_router.post("/create")
async def create_deck(request: CreateDeckRequest, db: Session = Depends(get_db)):
    """
    Create New Deck (DATABASE)

    Body:
    {
        "player_id": 1,
        "deck_name": "Fire Gunslinger Aggro",
        "faction": "fire_gunslingers",
        "cards": {"1": 2, "3": 2, "5": 1, ...}  // Must total 30 cards
    }
    """
    try:
        # Validate deck has 30 cards
        total_cards = sum(request.cards.values())
        if total_cards != 30:
            raise HTTPException(
                status_code=400,
                detail=f"Deck must have exactly 30 cards (has {total_cards})"
            )

        # Create deck
        deck = PlayerDeck(
            player_id=request.player_id,
            deck_name=request.deck_name,
            faction=request.faction,
            cards=request.cards,
            is_active=False
        )

        db.add(deck)
        db.commit()
        db.refresh(deck)

        return {
            "success": True,
            "message": f"Deck '{request.deck_name}' created!",
            "deck": deck.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@decks_router.get("/{player_id}")
async def get_player_decks(player_id: int, db: Session = Depends(get_db)):
    """
    Get All Player Decks (DATABASE)

    Path: /api/decks/1
    """
    try:
        decks = db.query(PlayerDeck).filter(
            PlayerDeck.player_id == player_id
        ).all()

        return {
            "player_id": player_id,
            "decks": [deck.to_dict() for deck in decks],
            "count": len(decks)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@decks_router.put("/{deck_id}")
async def update_deck(deck_id: int, request: UpdateDeckRequest, db: Session = Depends(get_db)):
    """
    Update Deck (DATABASE)

    Path: /api/decks/5
    Body:
    {
        "deck_name": "New Name",
        "cards": {"1": 2, "3": 2, ...}
    }
    """
    try:
        deck = db.query(PlayerDeck).filter(PlayerDeck.id == deck_id).first()

        if not deck:
            raise HTTPException(status_code=404, detail=f"Deck {deck_id} not found")

        if request.deck_name:
            deck.deck_name = request.deck_name

        if request.cards:
            total_cards = sum(request.cards.values())
            if total_cards != 30:
                raise HTTPException(
                    status_code=400,
                    detail=f"Deck must have exactly 30 cards (has {total_cards})"
                )
            deck.cards = request.cards

        deck.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(deck)

        return {
            "success": True,
            "message": "Deck updated!",
            "deck": deck.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@decks_router.delete("/{deck_id}")
async def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    """
    Delete Deck (DATABASE)

    Path: /api/decks/5
    """
    try:
        deck = db.query(PlayerDeck).filter(PlayerDeck.id == deck_id).first()

        if not deck:
            raise HTTPException(status_code=404, detail=f"Deck {deck_id} not found")

        deck_name = deck.deck_name
        db.delete(deck)
        db.commit()

        return {
            "success": True,
            "message": f"Deck '{deck_name}' deleted"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@decks_router.post("/{deck_id}/activate")
async def activate_deck(deck_id: int, db: Session = Depends(get_db)):
    """
    Set Active Deck (DATABASE)

    Path: /api/decks/5/activate
    """
    try:
        deck = db.query(PlayerDeck).filter(PlayerDeck.id == deck_id).first()

        if not deck:
            raise HTTPException(status_code=404, detail=f"Deck {deck_id} not found")

        # Deactivate all other decks for this player
        db.query(PlayerDeck).filter(
            PlayerDeck.player_id == deck.player_id
        ).update({"is_active": False})

        # Activate this deck
        deck.is_active = True

        db.commit()
        db.refresh(deck)

        return {
            "success": True,
            "message": f"Deck '{deck.deck_name}' is now active",
            "deck": deck.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MATCH ENDPOINTS
# ============================================================================

@matches_router.post("/start")
async def start_match(request: StartMatchRequest, db: Session = Depends(get_db)):
    """
    Start New Match (DATABASE)

    Body:
    {
        "player1_id": 1,
        "player2_id": 2,
        "game_mode": "triad",
        "is_ranked": true,
        "is_vs_npc": false,
        "player1_deck_id": 5,
        "player2_deck_id": 7
    }
    """
    try:
        # Create match
        match = CardGameMatch(
            player1_id=request.player1_id,
            player2_id=request.player2_id,
            game_mode=request.game_mode,
            is_ranked=request.is_ranked,
            is_vs_npc=request.is_vs_npc,
            npc_name=request.npc_name,
            player1_deck_id=request.player1_deck_id,
            player2_deck_id=request.player2_deck_id,
            started_at=datetime.utcnow()
        )

        db.add(match)
        db.commit()
        db.refresh(match)

        return {
            "success": True,
            "match_id": match.id,
            "message": "Match started!",
            "match": match.to_dict()
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.post("/end")
async def end_match(request: EndMatchRequest, db: Session = Depends(get_db)):
    """
    End Match and Record Results (DATABASE)

    Body:
    {
        "match_id": 5,
        "winner_id": 1,
        "turns_played": 15,
        "duration_seconds": 480,
        "final_board": {...},
        "gold_earned": 100,
        "xp_earned": 250,
        "cards_won": [12, 34]
    }
    """
    try:
        match = db.query(CardGameMatch).filter(
            CardGameMatch.id == request.match_id
        ).first()

        if not match:
            raise HTTPException(status_code=404, detail=f"Match {request.match_id} not found")

        # Update match results
        match.winner_id = request.winner_id
        match.turns_played = request.turns_played
        match.duration_seconds = request.duration_seconds
        match.final_board = request.final_board
        match.gold_earned = request.gold_earned
        match.xp_earned = request.xp_earned
        match.cards_won = request.cards_won or []
        match.ended_at = datetime.utcnow()

        # Update deck stats
        if match.player1_deck_id:
            deck1 = db.query(PlayerDeck).filter(PlayerDeck.id == match.player1_deck_id).first()
            if deck1:
                deck1.total_games += 1
                if match.winner_id == match.player1_id:
                    deck1.total_wins += 1
                deck1.win_rate = (deck1.total_wins / deck1.total_games) * 100 if deck1.total_games > 0 else 0

        if match.player2_deck_id:
            deck2 = db.query(PlayerDeck).filter(PlayerDeck.id == match.player2_deck_id).first()
            if deck2:
                deck2.total_games += 1
                if match.winner_id == match.player2_id:
                    deck2.total_wins += 1
                deck2.win_rate = (deck2.total_wins / deck2.total_games) * 100 if deck2.total_games > 0 else 0

        db.commit()
        db.refresh(match)

        return {
            "success": True,
            "message": "Match ended and results recorded!",
            "match": match.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.get("/history/{player_id}")
async def get_match_history(
    player_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get Match History (DATABASE)

    Path: /api/matches/history/1?limit=20
    """
    try:
        matches = db.query(CardGameMatch).filter(
            (CardGameMatch.player1_id == player_id) | (CardGameMatch.player2_id == player_id)
        ).order_by(CardGameMatch.started_at.desc()).limit(limit).all()

        return {
            "player_id": player_id,
            "matches": [match.to_dict() for match in matches],
            "count": len(matches)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.get("/{match_id}")
async def get_match(match_id: int, db: Session = Depends(get_db)):
    """
    Get Specific Match (DATABASE)

    Path: /api/matches/5
    """
    try:
        match = db.query(CardGameMatch).filter(CardGameMatch.id == match_id).first()

        if not match:
            raise HTTPException(status_code=404, detail=f"Match {match_id} not found")

        return match.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RANKING ENDPOINTS
# ============================================================================

@rankings_router.get("/leaderboard")
async def get_leaderboard(
    limit: int = Query(100, ge=1, le=500),
    season: Optional[int] = Query(None, description="Filter by season"),
    db: Session = Depends(get_db)
):
    """
    Get Top Rankings (DATABASE)

    Query Params:
        limit: int (default 100)
        season: int (optional)

    Example: /api/rankings/leaderboard?limit=50&season=1
    """
    try:
        query = db.query(CardGameRanking)

        if season:
            query = query.filter(CardGameRanking.season == season)

        rankings = query.order_by(CardGameRanking.elo_rating.desc()).limit(limit).all()

        return {
            "leaderboard": [ranking.to_dict() for ranking in rankings],
            "count": len(rankings)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@rankings_router.get("/{player_id}")
async def get_player_ranking(player_id: int, db: Session = Depends(get_db)):
    """
    Get Player Ranking (DATABASE)

    Path: /api/rankings/1
    """
    try:
        ranking = db.query(CardGameRanking).filter(
            CardGameRanking.player_id == player_id
        ).first()

        if not ranking:
            # Create default ranking
            ranking = CardGameRanking(
                player_id=player_id,
                elo_rating=1000,
                rank_tier="bronze",
                season=1
            )
            db.add(ranking)
            db.commit()
            db.refresh(ranking)

        return ranking.to_dict()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@rankings_router.post("/update")
async def update_ranking(request: UpdateRankingRequest, db: Session = Depends(get_db)):
    """
    Update ELO After Match (DATABASE)

    Body:
    {
        "player_id": 1,
        "elo_change": 25,
        "won": true
    }
    """
    try:
        ranking = db.query(CardGameRanking).filter(
            CardGameRanking.player_id == request.player_id
        ).first()

        if not ranking:
            ranking = CardGameRanking(
                player_id=request.player_id,
                elo_rating=1000,
                rank_tier="bronze",
                season=1
            )
            db.add(ranking)

        # Update ELO
        ranking.elo_rating += request.elo_change

        # Update stats
        if request.won:
            ranking.ranked_wins += 1
            ranking.win_streak += 1
            if ranking.win_streak > ranking.best_win_streak:
                ranking.best_win_streak = ranking.win_streak
        else:
            ranking.ranked_losses += 1
            ranking.win_streak = 0

        # Update rank tier based on ELO
        if ranking.elo_rating >= 2000:
            ranking.rank_tier = "legend"
        elif ranking.elo_rating >= 1700:
            ranking.rank_tier = "diamond"
        elif ranking.elo_rating >= 1400:
            ranking.rank_tier = "platinum"
        elif ranking.elo_rating >= 1100:
            ranking.rank_tier = "gold"
        elif ranking.elo_rating >= 800:
            ranking.rank_tier = "silver"
        else:
            ranking.rank_tier = "bronze"

        # Update season high
        if ranking.rank_tier not in ["bronze", "silver"]:
            tier_order = ["gold", "platinum", "diamond", "legend"]
            current_high = ranking.season_high_rank or "bronze"
            if ranking.rank_tier in tier_order and (current_high not in tier_order or tier_order.index(ranking.rank_tier) > tier_order.index(current_high)):
                ranking.season_high_rank = ranking.rank_tier

        db.commit()
        db.refresh(ranking)

        return {
            "success": True,
            "message": f"ELO updated: {'+' if request.elo_change >= 0 else ''}{request.elo_change}",
            "ranking": ranking.to_dict()
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))