"""
Database Models Package - Najika World
"""

from backend.models.user import User

from backend.models.card_game import (
    Card,
    PlayerCardCollection,
    PlayerDeck,
    CardGameMatch,
    CardGameRanking
)

from backend.models.dice_monsters import (
    DiceMonster,
    PlayerDiceCollection,
    DiceDuelMatch
)

from backend.models.slime_arena import (
    SlimeDuel,
    SlimeTournament,
    SlimeFame
)

__all__ = [
    # Card Game Models
    "Card",
    "PlayerCardCollection",
    "PlayerDeck",
    "CardGameMatch",
    "CardGameRanking",
    # Dice Monsters Models
    "DiceMonster",
    "PlayerDiceCollection",
    "DiceDuelMatch",
    # Slime Arena Models
    "SlimeDuel",
    "SlimeTournament",
    "SlimeFame",
]
