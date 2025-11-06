"""
Najika PvP System - Backend
Implements 3-mode PvP system with mercy mechanics
Based on: DOCS/design/PVP_SYSTEM_COMPLETE.md

Modes:
- Hardcore-PvP: Death or "give all to live" with double confirmation
- Normal-PvP: Winner takes 1 equipment piece
- Softy-PvP: Ranking only, no losses
"""

import time
import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class PvPMode(Enum):
    """PvP battle modes"""
    HARDCORE = "hardcore"
    NORMAL = "normal"
    SOFTY = "softy"


class MercyDecision(Enum):
    """Mercy system decisions"""
    OFFER = "offer"
    DIE = "die"
    ACCEPT = "accept"
    REJECT = "reject"


@dataclass
class PlayerPvPState:
    """Player state in PvP battle"""
    player_id: str
    name: str
    hp: int
    max_hp: int
    level: int
    equipment: Dict[str, str] = field(default_factory=dict)  # slot -> item_id
    inventory: List[str] = field(default_factory=list)  # item_ids
    is_alive: bool = True
    has_slime_rescue: bool = False
    has_totem: bool = False
    hardcore_mode: bool = False
    pvp_cooldown_until: Optional[datetime] = None
    mercy_count_7d: int = 0
    last_mercy_timestamp: Optional[datetime] = None


@dataclass
class PvPBattle:
    """PvP battle state"""
    battle_id: str
    mode: PvPMode
    player1: PlayerPvPState
    player2: PlayerPvPState
    current_turn: int = 0
    battle_active: bool = True
    winner_id: Optional[str] = None
    loser_id: Optional[str] = None
    mercy_offered: bool = False
    mercy_response: Optional[MercyDecision] = None
    created_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    waiting_for_confirmation: bool = False
    confirmation_step: int = 0  # 0=none, 1=first JA, 2=second JA


class PvPSystem:
    """Main PvP system controller"""

    def __init__(self):
        self.active_battles: Dict[str, PvPBattle] = {}
        self.player_states: Dict[str, PlayerPvPState] = {}

    def can_player_join_pvp(self, player_id: str, mode: PvPMode) -> Tuple[bool, Optional[str]]:
        """
        Check if player can join PvP in given mode
        Returns: (can_join, reason_if_not)
        """
        player = self.player_states.get(player_id)
        if not player:
            return False, "player_not_found"

        # Check cooldown
        if player.pvp_cooldown_until:
            if datetime.now() < player.pvp_cooldown_until:
                remaining = player.pvp_cooldown_until - datetime.now()
                return False, f"pvp_cooldown_{remaining.total_seconds()}_seconds"

        # Check mercy abuse protection
        if player.mercy_count_7d >= 3:
            # Restricted to low-risk modes
            if mode in [PvPMode.HARDCORE, PvPMode.NORMAL]:
                return False, "mercy_abuse_restriction"

        # Hardcore mode specific checks
        if mode == PvPMode.HARDCORE:
            if not player.hardcore_mode:
                return False, "not_hardcore_player"

        return True, None

    def create_battle(self, player1_id: str, player2_id: str, mode: PvPMode) -> Dict:
        """
        Create a new PvP battle
        """
        # Validate both players can join
        can_join_1, reason_1 = self.can_player_join_pvp(player1_id, mode)
        can_join_2, reason_2 = self.can_player_join_pvp(player2_id, mode)

        if not can_join_1:
            return {"success": False, "reason": f"player1_{reason_1}"}
        if not can_join_2:
            return {"success": False, "reason": f"player2_{reason_2}"}

        # Create battle
        battle_id = str(uuid.uuid4())
        battle = PvPBattle(
            battle_id=battle_id,
            mode=mode,
            player1=self.player_states[player1_id],
            player2=self.player_states[player2_id]
        )

        self.active_battles[battle_id] = battle

        return {
            "success": True,
            "battle_id": battle_id,
            "mode": mode.value,
            "player1": self._player_to_dict(battle.player1),
            "player2": self._player_to_dict(battle.player2)
        }

    def handle_defeat(self, battle_id: str, loser_id: str, winner_id: str) -> Dict:
        """
        Handle player defeat - triggers appropriate mode logic
        """
        battle = self.active_battles.get(battle_id)
        if not battle:
            return {"success": False, "reason": "battle_not_found"}

        if not battle.battle_active:
            return {"success": False, "reason": "battle_already_ended"}

        battle.loser_id = loser_id
        battle.winner_id = winner_id

        # Route to appropriate mode handler
        if battle.mode == PvPMode.HARDCORE:
            return self._handle_defeat_hardcore(battle)
        elif battle.mode == PvPMode.NORMAL:
            return self._handle_defeat_normal(battle)
        else:  # SOFTY
            return self._handle_defeat_softy(battle)

    def _handle_defeat_hardcore(self, battle: PvPBattle) -> Dict:
        """
        Hardcore-PvP Defeat Handler

        Process:
        1. Loser can offer "give all to live"
        2. Winner can accept or reject
        3. Double "JA" confirmation required
        4. Transfer all items OR permadeath
        """
        loser = self._get_player_in_battle(battle, battle.loser_id)
        winner = self._get_player_in_battle(battle, battle.winner_id)

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "mode": "hardcore",
            "phase": "mercy_window",
            "loser_id": loser.player_id,
            "winner_id": winner.player_id,
            "prompt_loser": {
                "type": "mercy_choice",
                "message": "Du stehst am Rande des Todes! Was willst du tun?",
                "options": [
                    {
                        "value": "offer",
                        "label": "ALLES GEBEN um zu LEBEN",
                        "description": "Gib dein gesamtes Inventar ab und überlebe. 7 Tage PvP-Sperre."
                    },
                    {
                        "value": "die",
                        "label": "Kämpfe bis zum Tod",
                        "description": "Permadeath (Slime/Totem-Rettung möglich)"
                    }
                ],
                "timeout": 30
            }
        }

    def process_mercy_offer(self, battle_id: str, loser_decision: str) -> Dict:
        """
        Process loser's mercy decision
        """
        battle = self.active_battles.get(battle_id)
        if not battle:
            return {"success": False, "reason": "battle_not_found"}

        loser = self._get_player_in_battle(battle, battle.loser_id)
        winner = self._get_player_in_battle(battle, battle.winner_id)

        if loser_decision == "die":
            # Loser chose death
            return self._apply_permadeath(battle, loser, winner)

        elif loser_decision == "offer":
            # Loser offers mercy
            battle.mercy_offered = True

            return {
                "success": True,
                "battle_id": battle.battle_id,
                "phase": "mercy_offer_made",
                "prompt_winner": {
                    "type": "mercy_accept",
                    "message": f"{loser.name} bittet um Gnade!",
                    "loser_items": {
                        "equipment": loser.equipment,
                        "inventory": loser.inventory,
                        "total_count": len(loser.equipment) + len(loser.inventory)
                    },
                    "options": [
                        {
                            "value": "accept",
                            "label": "GNADE GEWÄHREN",
                            "description": "Du erhältst alle Items. Ehre-Bonus."
                        },
                        {
                            "value": "reject",
                            "label": "KEINE GNADE",
                            "description": "Gegner stirbt permanent."
                        }
                    ],
                    "timeout": 30
                }
            }

        return {"success": False, "reason": "invalid_decision"}

    def process_mercy_response(self, battle_id: str, winner_decision: str) -> Dict:
        """
        Process winner's response to mercy offer
        """
        battle = self.active_battles.get(battle_id)
        if not battle:
            return {"success": False, "reason": "battle_not_found"}

        if not battle.mercy_offered:
            return {"success": False, "reason": "no_mercy_offered"}

        loser = self._get_player_in_battle(battle, battle.loser_id)
        winner = self._get_player_in_battle(battle, battle.winner_id)

        if winner_decision == "reject":
            # Winner rejects mercy
            battle.mercy_response = MercyDecision.REJECT
            return self._apply_permadeath(battle, loser, winner)

        elif winner_decision == "accept":
            # Winner accepts - trigger double confirmation
            battle.mercy_response = MercyDecision.ACCEPT
            battle.waiting_for_confirmation = True
            battle.confirmation_step = 0

            return {
                "success": True,
                "battle_id": battle.battle_id,
                "phase": "confirmation_1",
                "prompt_loser": {
                    "type": "confirmation",
                    "message": "⚠️ BESTÄTIGUNG 1/2 ⚠️\n\nDu wirst ALLES verlieren:\n" +
                              f"- {len(loser.equipment)} Ausrüstungsteile\n" +
                              f"- {len(loser.inventory)} Inventar-Items\n" +
                              "- 7 Tage PvP-Sperre\n\n" +
                              'Tippe "JA" um zu bestätigen.',
                    "expected_input": "JA",
                    "timeout": 20
                }
            }

        return {"success": False, "reason": "invalid_decision"}

    def process_confirmation(self, battle_id: str, loser_input: str) -> Dict:
        """
        Process double confirmation ("JA" twice)
        """
        battle = self.active_battles.get(battle_id)
        if not battle:
            return {"success": False, "reason": "battle_not_found"}

        if not battle.waiting_for_confirmation:
            return {"success": False, "reason": "not_waiting_for_confirmation"}

        loser = self._get_player_in_battle(battle, battle.loser_id)
        winner = self._get_player_in_battle(battle, battle.winner_id)

        if loser_input != "JA":
            # Wrong input - cancel mercy, apply death
            battle.waiting_for_confirmation = False
            return self._apply_permadeath(battle, loser, winner)

        battle.confirmation_step += 1

        if battle.confirmation_step == 1:
            # First confirmation received, ask for second
            return {
                "success": True,
                "battle_id": battle.battle_id,
                "phase": "confirmation_2",
                "prompt_loser": {
                    "type": "confirmation",
                    "message": "⚠️ BESTÄTIGUNG 2/2 ⚠️\n\n" +
                              "LETZTE CHANCE!\n" +
                              "Dies ist FINAL und kann NICHT rückgängig gemacht werden!\n\n" +
                              'Tippe nochmal "JA" um ENDGÜLTIG zu bestätigen.',
                    "expected_input": "JA",
                    "timeout": 20
                }
            }

        elif battle.confirmation_step == 2:
            # Second confirmation received - execute mercy transfer
            battle.waiting_for_confirmation = False
            return self._execute_mercy_transfer(battle, loser, winner)

        return {"success": False, "reason": "invalid_confirmation_state"}

    def _execute_mercy_transfer(self, battle: PvPBattle, loser: PlayerPvPState,
                                winner: PlayerPvPState) -> Dict:
        """
        Execute the mercy transfer:
        - Transfer ABSOLUTELY ALL items from loser to winner (NO EXCEPTIONS!)
        - Loser is left with NOTHING - must find/craft weapons in the world
        - Apply 7-day PvP cooldown to loser
        - Update mercy statistics
        - End battle

        WICHTIG: Wenn alles weg ist, dann ist ALLES weg!
        Kein Starter-Schwert, keine Unterwäsche-Protection, NICHTS!
        Spieler muss draußen einen Stock finden oder mit bloßen Händen kämpfen.
        """
        # Collect EVERYTHING (no protection, no exceptions)
        transferred_items = {
            "equipment": dict(loser.equipment),
            "inventory": list(loser.inventory)
        }

        # Transfer to winner
        for slot, item_id in loser.equipment.items():
            winner.inventory.append(item_id)

        for item_id in loser.inventory:
            winner.inventory.append(item_id)

        # Clear loser's items - EVERYTHING GONE
        loser.equipment.clear()
        loser.inventory.clear()

        # Apply cooldown
        loser.pvp_cooldown_until = datetime.now() + timedelta(days=7)
        loser.last_mercy_timestamp = datetime.now()
        loser.mercy_count_7d += 1

        # End battle
        battle.battle_active = False
        battle.ended_at = datetime.now()

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "result": "mercy_granted",
            "loser_survived": True,
            "winner_id": winner.player_id,
            "loser_id": loser.player_id,
            "transferred_items": transferred_items,
            "loser_pvp_cooldown_days": 7,
            "loser_pvp_cooldown_until": loser.pvp_cooldown_until.isoformat(),
            "message": {
                "winner": f"Du hast Gnade gewährt! {len(transferred_items['equipment']) + len(transferred_items['inventory'])} Items erhalten.",
                "loser": "Du hast überlebt, aber alles verloren. 7 Tage PvP-Sperre aktiv."
            }
        }

    def _apply_permadeath(self, battle: PvPBattle, loser: PlayerPvPState,
                         winner: PlayerPvPState) -> Dict:
        """
        Apply permadeath to loser (with Slime/Totem rescue check)
        """
        loser.is_alive = False

        # Check for rescue options
        rescue_available = None
        if loser.has_slime_rescue:
            rescue_available = "slime"
        elif loser.has_totem:
            rescue_available = "totem"

        # End battle
        battle.battle_active = False
        battle.ended_at = datetime.now()

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "result": "permadeath",
            "loser_died": True,
            "winner_id": winner.player_id,
            "loser_id": loser.player_id,
            "rescue_available": rescue_available,
            "message": {
                "winner": "Du hast den Kampf gewonnen!",
                "loser": "Du bist gestorben!" + (
                    f" ({rescue_available.upper()}-Rettung verfügbar!)" if rescue_available else ""
                )
            }
        }

    def _handle_defeat_normal(self, battle: PvPBattle) -> Dict:
        """
        Normal-PvP Defeat Handler
        Winner selects 1 equipment piece from loser
        """
        loser = self._get_player_in_battle(battle, battle.loser_id)
        winner = self._get_player_in_battle(battle, battle.winner_id)

        available_items = list(loser.equipment.items())

        if not available_items:
            # Loser has no equipment
            battle.battle_active = False
            return {
                "success": True,
                "battle_id": battle.battle_id,
                "result": "victory_no_loot",
                "winner_id": winner.player_id,
                "loser_id": loser.player_id,
                "message": {
                    "winner": "Sieg! (Gegner hatte keine Ausrüstung)",
                    "loser": "Niederlage! (Keine Items verloren)"
                }
            }

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "phase": "item_selection",
            "prompt_winner": {
                "type": "select_item",
                "message": "Wähle 1 Ausrüstungsteil:",
                "available_items": [
                    {"slot": slot, "item_id": item_id}
                    for slot, item_id in available_items
                ],
                "timeout": 30
            }
        }

    def process_item_selection(self, battle_id: str, selected_slot: str) -> Dict:
        """
        Process winner's item selection (Normal-PvP)
        """
        battle = self.active_battles.get(battle_id)
        if not battle:
            return {"success": False, "reason": "battle_not_found"}

        if battle.mode != PvPMode.NORMAL:
            return {"success": False, "reason": "wrong_mode"}

        loser = self._get_player_in_battle(battle, battle.loser_id)
        winner = self._get_player_in_battle(battle, battle.winner_id)

        # Validate selection
        if selected_slot not in loser.equipment:
            return {"success": False, "reason": "invalid_item"}

        # Transfer item
        item_id = loser.equipment.pop(selected_slot)
        winner.inventory.append(item_id)

        # End battle
        battle.battle_active = False
        battle.ended_at = datetime.now()

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "result": "normal_pvp_victory",
            "winner_id": winner.player_id,
            "loser_id": loser.player_id,
            "transferred_item": {
                "slot": selected_slot,
                "item_id": item_id
            },
            "message": {
                "winner": f"Sieg! {selected_slot} ({item_id}) erhalten!",
                "loser": f"Niederlage! {selected_slot} verloren."
            }
        }

    def _handle_defeat_softy(self, battle: PvPBattle) -> Dict:
        """
        Softy-PvP Defeat Handler
        Ranking only, no losses
        """
        loser = self._get_player_in_battle(battle, battle.loser_id)
        winner = self._get_player_in_battle(battle, battle.winner_id)

        # End battle
        battle.battle_active = False
        battle.ended_at = datetime.now()

        return {
            "success": True,
            "battle_id": battle.battle_id,
            "result": "softy_pvp_victory",
            "winner_id": winner.player_id,
            "loser_id": loser.player_id,
            "ranking_change": {
                "winner": "+10 Rating",
                "loser": "-5 Rating"
            },
            "message": {
                "winner": "Sieg! +10 Rating",
                "loser": "Niederlage! -5 Rating (keine Items verloren)"
            }
        }

    def _get_player_in_battle(self, battle: PvPBattle, player_id: str) -> PlayerPvPState:
        """Get player state from battle"""
        if battle.player1.player_id == player_id:
            return battle.player1
        return battle.player2

    def _player_to_dict(self, player: PlayerPvPState) -> Dict:
        """Convert player state to dict"""
        return {
            "player_id": player.player_id,
            "name": player.name,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "level": player.level,
            "is_alive": player.is_alive,
            "equipment_count": len(player.equipment),
            "inventory_count": len(player.inventory),
            "pvp_cooldown_until": player.pvp_cooldown_until.isoformat() if player.pvp_cooldown_until else None,
            "mercy_count_7d": player.mercy_count_7d
        }

    def get_battle_state(self, battle_id: str) -> Optional[Dict]:
        """Get current battle state"""
        battle = self.active_battles.get(battle_id)
        if not battle:
            return None

        return {
            "battle_id": battle.battle_id,
            "mode": battle.mode.value,
            "active": battle.battle_active,
            "current_turn": battle.current_turn,
            "player1": self._player_to_dict(battle.player1),
            "player2": self._player_to_dict(battle.player2),
            "winner_id": battle.winner_id,
            "loser_id": battle.loser_id,
            "mercy_offered": battle.mercy_offered,
            "waiting_for_confirmation": battle.waiting_for_confirmation,
            "confirmation_step": battle.confirmation_step
        }

    def register_player(self, player_id: str, name: str, level: int,
                       hardcore_mode: bool = False) -> Dict:
        """Register a player for PvP"""
        player = PlayerPvPState(
            player_id=player_id,
            name=name,
            hp=100,
            max_hp=100,
            level=level,
            hardcore_mode=hardcore_mode
        )

        self.player_states[player_id] = player

        return {
            "success": True,
            "player_id": player_id,
            "registered": True
        }
