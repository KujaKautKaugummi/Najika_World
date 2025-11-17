"""
PvP System - Najika World
==========================

3 PvP Modi mit Fair-Play-Philosophie:
- Hardcore PvP: Permadeath ODER "Alles-abgeben-um-zu-leben" (Mercy)
- Normal PvP: Verlierer gibt 1 Item ab
- Softy PvP: Nur Ranking, keine Verluste

KRITISCHE REGEL: "ALLES WEG = ALLES WEG!" (Keine Ausnahmen!)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
import json
import random


class PvPMode(Enum):
    """3 PvP Modi"""
    HARDCORE = "hardcore"  # Permadeath OR Mercy
    NORMAL = "normal"      # 1 Item Loss
    SOFTY = "softy"        # Ranking only


class MercyStatus(Enum):
    """Status der Mercy-Entscheidung"""
    NOT_OFFERED = "not_offered"
    OFFERED = "offered"
    FIRST_CONFIRMATION = "first_ja"
    SECOND_CONFIRMATION = "second_ja"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class PvPBattle:
    """Einzelner PvP-Kampf"""
    battle_id: int
    attacker_id: int
    defender_id: int
    mode: PvPMode
    timestamp: datetime
    winner_id: Optional[int] = None
    loser_id: Optional[int] = None
    mercy_offered: bool = False
    mercy_accepted: bool = False
    items_lost: List[Dict] = field(default_factory=list)
    permanent_death: bool = False
    battle_duration: float = 0.0  # in seconds


@dataclass
class PlayerPvPStats:
    """PvP-Statistiken eines Spielers"""
    player_id: int

    # Stats per Mode
    hardcore_wins: int = 0
    hardcore_losses: int = 0
    hardcore_deaths: int = 0

    normal_wins: int = 0
    normal_losses: int = 0

    softy_wins: int = 0
    softy_losses: int = 0

    # Mercy Stats
    mercy_given_count: int = 0  # Wie oft hat Spieler Mercy GEGEBEN
    mercy_received_count: int = 0  # Wie oft hat Spieler Mercy ERHALTEN
    mercy_received_history: List[datetime] = field(default_factory=list)

    # Cooldowns
    pvp_cooldown_until: Optional[datetime] = None
    last_mercy_received: Optional[datetime] = None

    # Rankings
    hardcore_rank: int = 0
    normal_rank: int = 0
    softy_rank: int = 0

    # Total Stats
    total_items_lost: int = 0
    total_items_won: int = 0


class PvPSystem:
    """
    PvP System Manager

    Verwaltet alle PvP-Modi, Mercy-System, Anti-Abuse
    """

    def __init__(self):
        self.battles: Dict[int, PvPBattle] = {}
        self.player_stats: Dict[int, PlayerPvPStats] = {}
        self.next_battle_id = 1

        # Anti-Abuse Limits
        self.MAX_MERCY_PER_WEEK = 3
        self.MERCY_COOLDOWN_DAYS = 7
        self.MERCY_RESET_PERIOD_DAYS = 7


    def can_initiate_pvp(
        self,
        attacker_id: int,
        defender_id: int,
        mode: PvPMode
    ) -> Tuple[bool, str]:
        """
        Prüft ob PvP gestartet werden kann

        Returns:
            (can_start, reason)
        """
        # Prüfe Attacker Stats
        attacker_stats = self._get_player_stats(attacker_id)

        # Prüfe PvP Cooldown (nach Mercy)
        if attacker_stats.pvp_cooldown_until:
            if datetime.now() < attacker_stats.pvp_cooldown_until:
                remaining = (attacker_stats.pvp_cooldown_until - datetime.now()).days
                return False, f"PvP Cooldown: Noch {remaining} Tage"

        # Prüfe Defender Stats
        defender_stats = self._get_player_stats(defender_id)

        # Prüfe Defender Cooldown
        if defender_stats.pvp_cooldown_until:
            if datetime.now() < defender_stats.pvp_cooldown_until:
                return False, "Verteidiger hat PvP Cooldown"

        # Hardcore-spezifische Checks
        if mode == PvPMode.HARDCORE:
            # Prüfe ob Defender bereits tot ist (sollte nicht möglich sein)
            if defender_stats.hardcore_deaths > 0:
                return False, "Verteidiger ist bereits permanent tot"

        return True, "PvP kann gestartet werden"


    def start_pvp_battle(
        self,
        attacker_id: int,
        defender_id: int,
        mode: PvPMode
    ) -> Tuple[bool, Optional[int], str]:
        """
        Startet einen PvP-Kampf

        Returns:
            (success, battle_id, message)
        """
        can_start, reason = self.can_initiate_pvp(attacker_id, defender_id, mode)

        if not can_start:
            return False, None, reason

        # Erstelle Battle
        battle = PvPBattle(
            battle_id=self.next_battle_id,
            attacker_id=attacker_id,
            defender_id=defender_id,
            mode=mode,
            timestamp=datetime.now()
        )

        self.battles[self.next_battle_id] = battle
        self.next_battle_id += 1

        return True, battle.battle_id, f"PvP {mode.value} gestartet!"


    def end_pvp_battle(
        self,
        battle_id: int,
        winner_id: int,
        battle_duration: float
    ) -> Dict:
        """
        Beendet einen PvP-Kampf und verarbeitet Konsequenzen

        Returns:
            Result-Dict mit allen Konsequenzen
        """
        if battle_id not in self.battles:
            return {"error": "Battle nicht gefunden"}

        battle = self.battles[battle_id]
        battle.winner_id = winner_id
        battle.loser_id = (
            battle.defender_id if winner_id == battle.attacker_id
            else battle.attacker_id
        )
        battle.battle_duration = battle_duration

        # Verarbeite basierend auf Modus
        if battle.mode == PvPMode.HARDCORE:
            return self._process_hardcore_result(battle)
        elif battle.mode == PvPMode.NORMAL:
            return self._process_normal_result(battle)
        elif battle.mode == PvPMode.SOFTY:
            return self._process_softy_result(battle)


    def _process_hardcore_result(self, battle: PvPBattle) -> Dict:
        """
        Verarbeitet Hardcore PvP Ergebnis

        Gibt Mercy-Option an Verlierer
        """
        winner_stats = self._get_player_stats(battle.winner_id)
        loser_stats = self._get_player_stats(battle.loser_id)

        # Update Winner Stats
        winner_stats.hardcore_wins += 1

        # Update Loser Stats (vorläufig)
        loser_stats.hardcore_losses += 1

        # Prüfe Mercy-Verfügbarkeit
        can_receive_mercy, mercy_reason = self._can_receive_mercy(battle.loser_id)

        result = {
            "battle_id": battle.battle_id,
            "mode": "hardcore",
            "winner_id": battle.winner_id,
            "loser_id": battle.loser_id,
            "mercy_available": can_receive_mercy,
            "mercy_reason": mercy_reason,
            "status": "awaiting_mercy_decision"
        }

        # Markiere Mercy als angeboten
        if can_receive_mercy:
            battle.mercy_offered = True
        else:
            # Kein Mercy möglich = Permadeath
            battle.permanent_death = True
            loser_stats.hardcore_deaths += 1
            result["status"] = "permanent_death"
            result["message"] = "PERMADEATH! Hardcore-Charakter ist tot."

        return result


    def _can_receive_mercy(self, player_id: int) -> Tuple[bool, str]:
        """
        Prüft ob Spieler Mercy erhalten kann

        Anti-Abuse: Max 3x Mercy in 7 Tagen
        """
        stats = self._get_player_stats(player_id)

        # Prüfe ob in letzten 7 Tagen
        cutoff_date = datetime.now() - timedelta(days=self.MERCY_RESET_PERIOD_DAYS)

        # Zähle Mercy in letzten 7 Tagen
        recent_mercy = [
            date for date in stats.mercy_received_history
            if date > cutoff_date
        ]

        if len(recent_mercy) >= self.MAX_MERCY_PER_WEEK:
            return False, f"Mercy-Limit erreicht ({self.MAX_MERCY_PER_WEEK}x pro {self.MERCY_RESET_PERIOD_DAYS} Tage)"

        return True, f"Mercy verfügbar ({len(recent_mercy)}/{self.MAX_MERCY_PER_WEEK} benutzt)"


    def process_mercy_decision(
        self,
        battle_id: int,
        player_id: int,
        accept_mercy: bool,
        player_inventory: List[Dict]
    ) -> Dict:
        """
        Verarbeitet Mercy-Entscheidung

        Args:
            battle_id: Battle ID
            player_id: Verlierer ID (zur Sicherheit)
            accept_mercy: True = Mercy akzeptieren, False = Permadeath wählen
            player_inventory: Komplettes Inventory des Verlierers

        Returns:
            Result mit Konsequenzen
        """
        if battle_id not in self.battles:
            return {"error": "Battle nicht gefunden"}

        battle = self.battles[battle_id]

        if battle.loser_id != player_id:
            return {"error": "Nur der Verlierer kann Mercy-Entscheidung treffen"}

        if not battle.mercy_offered:
            return {"error": "Mercy wurde nicht angeboten"}

        loser_stats = self._get_player_stats(battle.loser_id)
        winner_stats = self._get_player_stats(battle.winner_id)

        if accept_mercy:
            # MERCY AKZEPTIERT: "ALLES WEG = ALLES WEG!"
            battle.mercy_accepted = True
            battle.items_lost = player_inventory.copy()  # ALLES!

            # Update Stats
            loser_stats.mercy_received_count += 1
            loser_stats.mercy_received_history.append(datetime.now())
            loser_stats.last_mercy_received = datetime.now()
            loser_stats.total_items_lost += len(player_inventory)

            # 7 TAGE PVP COOLDOWN
            loser_stats.pvp_cooldown_until = datetime.now() + timedelta(
                days=self.MERCY_COOLDOWN_DAYS
            )

            # Winner Stats
            winner_stats.mercy_given_count += 1
            winner_stats.total_items_won += len(player_inventory)

            return {
                "battle_id": battle_id,
                "status": "mercy_accepted",
                "message": "ALLES WEG! Aber du lebst.",
                "items_lost": battle.items_lost,
                "items_count": len(battle.items_lost),
                "pvp_cooldown_days": self.MERCY_COOLDOWN_DAYS,
                "pvp_cooldown_until": loser_stats.pvp_cooldown_until.isoformat(),
                "mercy_count": loser_stats.mercy_received_count,
                "mercy_limit": self.MAX_MERCY_PER_WEEK
            }

        else:
            # MERCY ABGELEHNT: PERMADEATH
            battle.permanent_death = True
            loser_stats.hardcore_deaths += 1

            return {
                "battle_id": battle_id,
                "status": "permanent_death",
                "message": "Du hast dich für den ehrenvollen Tod entschieden.",
                "character_deleted": True
            }


    def _process_normal_result(self, battle: PvPBattle) -> Dict:
        """
        Verarbeitet Normal PvP Ergebnis

        Verlierer gibt 1 zufälliges Item ab
        """
        winner_stats = self._get_player_stats(battle.winner_id)
        loser_stats = self._get_player_stats(battle.loser_id)

        # Update Stats
        winner_stats.normal_wins += 1
        loser_stats.normal_losses += 1

        return {
            "battle_id": battle.battle_id,
            "mode": "normal",
            "winner_id": battle.winner_id,
            "loser_id": battle.loser_id,
            "status": "completed",
            "consequence": "loser_gives_1_random_item",
            "message": "Verlierer gibt 1 zufälliges Item ab"
        }


    def select_random_item_loss(
        self,
        battle_id: int,
        player_inventory: List[Dict]
    ) -> Dict:
        """
        Wählt 1 zufälliges Item aus für Normal PvP Verlust

        Args:
            battle_id: Battle ID
            player_inventory: Inventory des Verlierers

        Returns:
            Selected item + updated stats
        """
        if battle_id not in self.battles:
            return {"error": "Battle nicht gefunden"}

        battle = self.battles[battle_id]

        if not player_inventory:
            return {
                "battle_id": battle_id,
                "item_lost": None,
                "message": "Verlierer hat kein Inventory"
            }

        # Wähle zufälliges Item
        lost_item = random.choice(player_inventory)
        battle.items_lost = [lost_item]

        # Update Stats
        loser_stats = self._get_player_stats(battle.loser_id)
        winner_stats = self._get_player_stats(battle.winner_id)

        loser_stats.total_items_lost += 1
        winner_stats.total_items_won += 1

        return {
            "battle_id": battle_id,
            "item_lost": lost_item,
            "message": f"Item verloren: {lost_item.get('name', 'Unknown')}"
        }


    def _process_softy_result(self, battle: PvPBattle) -> Dict:
        """
        Verarbeitet Softy PvP Ergebnis

        Nur Ranking, keine Verluste
        """
        winner_stats = self._get_player_stats(battle.winner_id)
        loser_stats = self._get_player_stats(battle.loser_id)

        # Update Stats
        winner_stats.softy_wins += 1
        loser_stats.softy_losses += 1

        return {
            "battle_id": battle.battle_id,
            "mode": "softy",
            "winner_id": battle.winner_id,
            "loser_id": battle.loser_id,
            "status": "completed",
            "consequence": "ranking_only",
            "message": "Nur Ranking verändert, keine Items verloren"
        }


    def get_pvp_rankings(self, mode: PvPMode) -> List[Dict]:
        """
        Holt Rankings für einen PvP-Modus

        Returns:
            Sortierte Liste von Spielern nach Wins
        """
        rankings = []

        for player_id, stats in self.player_stats.items():
            if mode == PvPMode.HARDCORE:
                wins = stats.hardcore_wins
                losses = stats.hardcore_losses
                rank = stats.hardcore_rank
            elif mode == PvPMode.NORMAL:
                wins = stats.normal_wins
                losses = stats.normal_losses
                rank = stats.normal_rank
            elif mode == PvPMode.SOFTY:
                wins = stats.softy_wins
                losses = stats.softy_losses
                rank = stats.softy_rank

            win_rate = (wins / (wins + losses)) if (wins + losses) > 0 else 0.0

            rankings.append({
                "player_id": player_id,
                "rank": rank,
                "wins": wins,
                "losses": losses,
                "win_rate": win_rate
            })

        # Sortiere nach Wins (absteigend)
        rankings.sort(key=lambda x: x["wins"], reverse=True)

        # Update Ranks
        for i, entry in enumerate(rankings):
            entry["rank"] = i + 1
            player_id = entry["player_id"]

            if mode == PvPMode.HARDCORE:
                self.player_stats[player_id].hardcore_rank = i + 1
            elif mode == PvPMode.NORMAL:
                self.player_stats[player_id].normal_rank = i + 1
            elif mode == PvPMode.SOFTY:
                self.player_stats[player_id].softy_rank = i + 1

        return rankings


    def get_player_pvp_stats(self, player_id: int) -> Dict:
        """Holt PvP-Stats eines Spielers"""
        stats = self._get_player_stats(player_id)

        return {
            "player_id": player_id,
            "hardcore": {
                "wins": stats.hardcore_wins,
                "losses": stats.hardcore_losses,
                "deaths": stats.hardcore_deaths,
                "rank": stats.hardcore_rank
            },
            "normal": {
                "wins": stats.normal_wins,
                "losses": stats.normal_losses,
                "rank": stats.normal_rank
            },
            "softy": {
                "wins": stats.softy_wins,
                "losses": stats.softy_losses,
                "rank": stats.softy_rank
            },
            "mercy": {
                "given": stats.mercy_given_count,
                "received": stats.mercy_received_count,
                "can_receive": self._can_receive_mercy(player_id)[0]
            },
            "cooldowns": {
                "pvp_cooldown_until": (
                    stats.pvp_cooldown_until.isoformat()
                    if stats.pvp_cooldown_until else None
                ),
                "has_cooldown": (
                    stats.pvp_cooldown_until > datetime.now()
                    if stats.pvp_cooldown_until else False
                )
            },
            "items": {
                "total_lost": stats.total_items_lost,
                "total_won": stats.total_items_won
            }
        }


    def _get_player_stats(self, player_id: int) -> PlayerPvPStats:
        """Holt oder erstellt Stats für einen Spieler"""
        if player_id not in self.player_stats:
            self.player_stats[player_id] = PlayerPvPStats(player_id=player_id)
        return self.player_stats[player_id]


    def export_state(self) -> Dict:
        """Exportiert kompletten PvP-State"""
        return {
            "battles": {
                battle_id: {
                    "battle_id": battle.battle_id,
                    "attacker_id": battle.attacker_id,
                    "defender_id": battle.defender_id,
                    "mode": battle.mode.value,
                    "timestamp": battle.timestamp.isoformat(),
                    "winner_id": battle.winner_id,
                    "loser_id": battle.loser_id,
                    "mercy_offered": battle.mercy_offered,
                    "mercy_accepted": battle.mercy_accepted,
                    "items_lost": battle.items_lost,
                    "permanent_death": battle.permanent_death,
                    "battle_duration": battle.battle_duration
                }
                for battle_id, battle in self.battles.items()
            },
            "player_stats": {
                player_id: {
                    "player_id": stats.player_id,
                    "hardcore_wins": stats.hardcore_wins,
                    "hardcore_losses": stats.hardcore_losses,
                    "hardcore_deaths": stats.hardcore_deaths,
                    "normal_wins": stats.normal_wins,
                    "normal_losses": stats.normal_losses,
                    "softy_wins": stats.softy_wins,
                    "softy_losses": stats.softy_losses,
                    "mercy_given_count": stats.mercy_given_count,
                    "mercy_received_count": stats.mercy_received_count,
                    "mercy_received_history": [
                        date.isoformat() for date in stats.mercy_received_history
                    ],
                    "pvp_cooldown_until": (
                        stats.pvp_cooldown_until.isoformat()
                        if stats.pvp_cooldown_until else None
                    ),
                    "last_mercy_received": (
                        stats.last_mercy_received.isoformat()
                        if stats.last_mercy_received else None
                    ),
                    "hardcore_rank": stats.hardcore_rank,
                    "normal_rank": stats.normal_rank,
                    "softy_rank": stats.softy_rank,
                    "total_items_lost": stats.total_items_lost,
                    "total_items_won": stats.total_items_won
                }
                for player_id, stats in self.player_stats.items()
            },
            "next_battle_id": self.next_battle_id
        }


    def import_state(self, state: Dict):
        """Importiert PvP-State"""
        # Import Battles
        self.battles = {}
        for battle_id_str, battle_data in state.get("battles", {}).items():
            battle_id = int(battle_id_str)
            self.battles[battle_id] = PvPBattle(
                battle_id=battle_data["battle_id"],
                attacker_id=battle_data["attacker_id"],
                defender_id=battle_data["defender_id"],
                mode=PvPMode(battle_data["mode"]),
                timestamp=datetime.fromisoformat(battle_data["timestamp"]),
                winner_id=battle_data.get("winner_id"),
                loser_id=battle_data.get("loser_id"),
                mercy_offered=battle_data.get("mercy_offered", False),
                mercy_accepted=battle_data.get("mercy_accepted", False),
                items_lost=battle_data.get("items_lost", []),
                permanent_death=battle_data.get("permanent_death", False),
                battle_duration=battle_data.get("battle_duration", 0.0)
            )

        # Import Player Stats
        self.player_stats = {}
        for player_id_str, stats_data in state.get("player_stats", {}).items():
            player_id = int(player_id_str)
            self.player_stats[player_id] = PlayerPvPStats(
                player_id=stats_data["player_id"],
                hardcore_wins=stats_data.get("hardcore_wins", 0),
                hardcore_losses=stats_data.get("hardcore_losses", 0),
                hardcore_deaths=stats_data.get("hardcore_deaths", 0),
                normal_wins=stats_data.get("normal_wins", 0),
                normal_losses=stats_data.get("normal_losses", 0),
                softy_wins=stats_data.get("softy_wins", 0),
                softy_losses=stats_data.get("softy_losses", 0),
                mercy_given_count=stats_data.get("mercy_given_count", 0),
                mercy_received_count=stats_data.get("mercy_received_count", 0),
                mercy_received_history=[
                    datetime.fromisoformat(date_str)
                    for date_str in stats_data.get("mercy_received_history", [])
                ],
                pvp_cooldown_until=(
                    datetime.fromisoformat(stats_data["pvp_cooldown_until"])
                    if stats_data.get("pvp_cooldown_until") else None
                ),
                last_mercy_received=(
                    datetime.fromisoformat(stats_data["last_mercy_received"])
                    if stats_data.get("last_mercy_received") else None
                ),
                hardcore_rank=stats_data.get("hardcore_rank", 0),
                normal_rank=stats_data.get("normal_rank", 0),
                softy_rank=stats_data.get("softy_rank", 0),
                total_items_lost=stats_data.get("total_items_lost", 0),
                total_items_won=stats_data.get("total_items_won", 0)
            )

        self.next_battle_id = state.get("next_battle_id", 1)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== PvP System Test ===\n")

    pvp = PvPSystem()

    # Test 1: Start Hardcore PvP
    print("1. Start Hardcore PvP (Player 1 vs Player 2)")
    success, battle_id, msg = pvp.start_pvp_battle(1, 2, PvPMode.HARDCORE)
    print(f"   → {msg} (Battle ID: {battle_id})\n")

    # Test 2: Player 2 verliert
    print("2. Player 2 verliert")
    result = pvp.end_pvp_battle(battle_id, winner_id=1, battle_duration=120.5)
    print(f"   → Mercy verfügbar: {result['mercy_available']}")
    print(f"   → {result['mercy_reason']}\n")

    # Test 3: Player 2 akzeptiert Mercy
    print("3. Player 2 akzeptiert Mercy (ALLES WEG!)")
    player_2_inventory = [
        {"name": "Schwert des Lichts", "rarity": "legendary"},
        {"name": "Heilungs-Trank", "rarity": "common"},
        {"name": "Rüstung der Titanen", "rarity": "epic"}
    ]
    mercy_result = pvp.process_mercy_decision(battle_id, 2, True, player_2_inventory)
    print(f"   → {mercy_result['message']}")
    print(f"   → Items verloren: {mercy_result['items_count']}")
    print(f"   → PvP Cooldown: {mercy_result['pvp_cooldown_days']} Tage")
    print(f"   → Mercy Count: {mercy_result['mercy_count']}/{mercy_result['mercy_limit']}\n")

    # Test 4: Player 2 versucht nochmal PvP (sollte Cooldown haben)
    print("4. Player 2 versucht nochmal PvP (Cooldown aktiv)")
    can_pvp, reason = pvp.can_initiate_pvp(2, 3, PvPMode.HARDCORE)
    print(f"   → Kann PvP starten: {can_pvp}")
    print(f"   → Grund: {reason}\n")

    # Test 5: Normal PvP
    print("5. Normal PvP (Player 3 vs Player 4)")
    success, battle_id_2, msg = pvp.start_pvp_battle(3, 4, PvPMode.NORMAL)
    print(f"   → {msg}")
    result = pvp.end_pvp_battle(battle_id_2, winner_id=3, battle_duration=85.0)
    print(f"   → {result['consequence']}")

    player_4_inventory = [{"name": "Bronze-Schwert", "rarity": "common"}]
    item_loss = pvp.select_random_item_loss(battle_id_2, player_4_inventory)
    print(f"   → {item_loss['message']}\n")

    # Test 6: Softy PvP
    print("6. Softy PvP (Player 5 vs Player 6)")
    success, battle_id_3, msg = pvp.start_pvp_battle(5, 6, PvPMode.SOFTY)
    print(f"   → {msg}")
    result = pvp.end_pvp_battle(battle_id_3, winner_id=5, battle_duration=45.0)
    print(f"   → {result['message']}\n")

    # Test 7: Rankings
    print("7. Hardcore Rankings")
    rankings = pvp.get_pvp_rankings(PvPMode.HARDCORE)
    for entry in rankings[:5]:
        print(f"   #{entry['rank']}: Player {entry['player_id']} - "
              f"{entry['wins']} Wins, {entry['losses']} Losses "
              f"({entry['win_rate']*100:.1f}% Win Rate)")
    print()

    # Test 8: Player Stats
    print("8. Player 2 Stats (nach Mercy)")
    stats = pvp.get_player_pvp_stats(2)
    print(f"   Hardcore: {stats['hardcore']['wins']}W / {stats['hardcore']['losses']}L")
    print(f"   Mercy: {stats['mercy']['received']} empfangen, {stats['mercy']['given']} gegeben")
    print(f"   Cooldown aktiv: {stats['cooldowns']['has_cooldown']}")
    print(f"   Items verloren: {stats['items']['total_lost']}")

    print("\n=== PvP System Test Complete ===")
    print(f"Fair Play Philosophie: 'ALLES WEG = ALLES WEG!' ✅")
