"""
Region Boss System (Gebietsherrscher) - Najika World
=====================================================

8 Regionen = 8 Bosse = 8 Digivice

Features:
- Boss-Rechte (Steuern, Modifikatoren, Raum, Titel, Broadcasts)
- Boss-Pflichten (Challenges, Aktivität, Events)
- Challenge-System (1x/Woche pro Boss, 24h Cooldown)
- 4 Eroberungs-Wege (Krieg, Handel, Diplomatie, Quest-Line)
- Ultimate Herrscher (alle 8 + Götterfels)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
import json
import asyncio


class Region(Enum):
    """8 Regionen"""
    SAMTMOOS_TIEFWALD = "samtmoos_tiefwald"      # Wald
    REICH_DER_DREI = "reich_der_drei"            # Eis/Nekromantie
    SALZWIND_KUESTE = "salzwind_kueste"          # Küste
    BLITZEBENE = "blitzebene"                    # Hochebene
    GRUENSCHLAMM_SUMPF = "gruenschlamm_sumpf"    # Sumpf
    MAGMASTROEME = "magmastroeme"                # Vulkan
    HEISSE_DUENEN = "heisse_duenen"              # Wüste
    TIEFENHOEHLEN = "tiefenhoehlen"              # Underground


class ConquestPath(Enum):
    """4 Eroberungs-Wege"""
    WAR = "krieg"           # Krieg (PvP)
    TRADE = "handel"        # Handel (Wirtschaft)
    DIPLOMACY = "diplomatie"  # Diplomatie (Politik)
    QUEST = "quest_line"    # Quest-Line (PvE)


class ChallengeStatus(Enum):
    """Challenge-Status"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class BossRights:
    """Boss-Rechte"""
    # Steuern
    trade_tax_percentage: float = 5.0  # 5-10% auf alle Transaktionen

    # Modifikatoren
    can_set_spawn_rates: bool = True
    can_start_events: bool = True
    can_set_weather: bool = True
    can_set_region_buffs: bool = True

    # Exklusiv
    has_boss_room: bool = True
    has_boss_title: bool = True
    can_broadcast: bool = True

    # Regions-spezifische Boni
    region_bonus_active: bool = True


@dataclass
class BossDuties:
    """Boss-Pflichten"""
    # Challenges
    min_challenges_per_week: int = 3
    challenges_this_week: int = 0

    # Aktivität
    min_hours_per_week: float = 10.0
    hours_this_week: float = 0.0

    # Events
    min_events_per_month: int = 2
    events_this_month: int = 0

    # Community
    community_score: float = 0.0  # 0-100


@dataclass
class Challenge:
    """Challenge gegen Boss"""
    challenge_id: int
    challenger_id: int
    boss_id: int
    region: Region

    status: ChallengeStatus = ChallengeStatus.PENDING
    challenge_type: ConquestPath = ConquestPath.WAR

    created_at: datetime = field(default_factory=datetime.now)
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    winner_id: Optional[int] = None

    # Challenge Details
    stakes: Dict = field(default_factory=dict)
    conditions: Dict = field(default_factory=dict)


@dataclass
class RegionBoss:
    """Region Boss"""
    boss_id: int
    player_id: int
    region: Region

    # Status
    became_boss_at: datetime = field(default_factory=datetime.now)
    total_reign_days: int = 0
    times_dethroned: int = 0

    # Eroberungs-Weg
    conquest_path: ConquestPath = ConquestPath.WAR
    conquest_progress: float = 0.0  # 0-100%

    # Rechte & Pflichten
    rights: BossRights = field(default_factory=BossRights)
    duties: BossDuties = field(default_factory=BossDuties)

    # Challenges
    challenges_received: List[int] = field(default_factory=list)
    challenges_won: int = 0
    challenges_lost: int = 0

    # Activity
    last_active: datetime = field(default_factory=datetime.now)
    is_absent: bool = False
    absent_since: Optional[datetime] = None

    # Reputation
    reputation: float = 50.0  # 0-100

    # Revenue
    total_tax_collected: float = 0.0


@dataclass
class UltimateRuler:
    """Ultimate Herrscher (alle 8 + Götterfels)"""
    player_id: int
    regions_controlled: List[Region] = field(default_factory=list)

    became_ultimate_at: Optional[datetime] = None
    is_ultimate: bool = False

    # Ultimate Powers
    can_world_events: bool = False
    can_global_modifiers: bool = False
    can_use_najikas_explosion: bool = False
    can_set_world_rules: bool = False

    total_ultimate_days: int = 0


class RegionBossSystem:
    """
    Region Boss System Manager

    Verwaltet alle 8 Regionen-Bosse, Challenges, Eroberung, Ultimate Herrscher
    """

    def __init__(self):
        # 8 Regionen → 8 Bosse (kann None sein wenn vacant)
        self.region_bosses: Dict[Region, Optional[RegionBoss]] = {
            region: None for region in Region
        }

        self.challenges: Dict[int, Challenge] = {}
        self.next_challenge_id = 1

        # Ultimate Herrscher (kann None sein)
        self.ultimate_ruler: Optional[UltimateRuler] = None

        # Challenge Cooldowns
        self.challenge_cooldowns: Dict[Tuple[int, int], datetime] = {}

        # Conquest Progress Tracking
        self.conquest_progress: Dict[int, Dict[Region, Dict[ConquestPath, float]]] = {}

        # Constants
        self.CHALLENGE_COOLDOWN_HOURS = 24
        self.MAX_CHALLENGES_PER_WEEK_PER_BOSS = 1
        self.CONQUEST_THRESHOLD = 100.0  # 100% um Boss zu werden

        # Boss-spezifische Boni pro Region
        self.REGION_BONUSES = {
            Region.SAMTMOOS_TIEFWALD: "+15% Kräuter-Effektivität",
            Region.REICH_DER_DREI: "+10% Eis-Defense",
            Region.SALZWIND_KUESTE: "+20% Fisch-Spawn",
            Region.BLITZEBENE: "+10% Bewegungsgeschwindigkeit",
            Region.GRUENSCHLAMM_SUMPF: "+15% Gift-Schaden",
            Region.MAGMASTROEME: "+15% Feuer-Magie",
            Region.HEISSE_DUENEN: "+10% Handelswaren-Qualität",
            Region.TIEFENHOEHLEN: "+20% Seltene Material-Drops"
        }


    def can_challenge_boss(
        self,
        challenger_id: int,
        region: Region
    ) -> Tuple[bool, str]:
        """
        Prüft ob Challenge möglich ist

        Returns:
            (can_challenge, reason)
        """
        # Check ob Region Boss hat
        boss = self.region_bosses.get(region)
        if not boss:
            return False, "Region hat keinen Boss"

        # Check ob Challenger = Boss
        if boss.player_id == challenger_id:
            return False, "Du bist bereits Boss dieser Region"

        # Check Cooldown
        cooldown_key = (challenger_id, boss.player_id)
        if cooldown_key in self.challenge_cooldowns:
            cooldown_until = self.challenge_cooldowns[cooldown_key]
            if datetime.now() < cooldown_until:
                remaining = (cooldown_until - datetime.now()).total_seconds() / 3600
                return False, f"Cooldown aktiv: {remaining:.1f}h verbleibend"

        # Check wöchentliche Challenge-Limit
        challenges_this_week = self._count_challenges_this_week(challenger_id, boss.boss_id)
        if challenges_this_week >= self.MAX_CHALLENGES_PER_WEEK_PER_BOSS:
            return False, "Challenge-Limit pro Woche erreicht (1x/Woche)"

        return True, "Challenge möglich"


    def create_challenge(
        self,
        challenger_id: int,
        region: Region,
        challenge_type: ConquestPath,
        stakes: Optional[Dict] = None,
        conditions: Optional[Dict] = None
    ) -> Tuple[bool, Optional[int], str]:
        """
        Erstellt eine Challenge

        Returns:
            (success, challenge_id, message)
        """
        can_challenge, reason = self.can_challenge_boss(challenger_id, region)

        if not can_challenge:
            return False, None, reason

        boss = self.region_bosses[region]

        challenge = Challenge(
            challenge_id=self.next_challenge_id,
            challenger_id=challenger_id,
            boss_id=boss.player_id,
            region=region,
            challenge_type=challenge_type,
            stakes=stakes or {},
            conditions=conditions or {}
        )

        self.challenges[self.next_challenge_id] = challenge
        boss.challenges_received.append(self.next_challenge_id)

        challenge_id = self.next_challenge_id
        self.next_challenge_id += 1

        return True, challenge_id, f"Challenge erstellt gegen {region.value} Boss"


    def accept_challenge(
        self,
        challenge_id: int,
        boss_player_id: int
    ) -> Tuple[bool, str]:
        """
        Boss akzeptiert Challenge

        Returns:
            (success, message)
        """
        if challenge_id not in self.challenges:
            return False, "Challenge nicht gefunden"

        challenge = self.challenges[challenge_id]

        if challenge.boss_id != boss_player_id:
            return False, "Nur der Boss kann diese Challenge annehmen"

        if challenge.status != ChallengeStatus.PENDING:
            return False, f"Challenge-Status: {challenge.status.value}"

        challenge.status = ChallengeStatus.ACCEPTED
        challenge.accepted_at = datetime.now()

        return True, "Challenge akzeptiert"


    def complete_challenge(
        self,
        challenge_id: int,
        winner_id: int
    ) -> Dict:
        """
        Beendet Challenge und verarbeitet Ergebnis

        Returns:
            Result dict mit Konsequenzen
        """
        if challenge_id not in self.challenges:
            return {"error": "Challenge nicht gefunden"}

        challenge = self.challenges[challenge_id]

        if challenge.status != ChallengeStatus.ACCEPTED:
            return {"error": f"Challenge nicht aktiv (Status: {challenge.status.value})"}

        challenge.status = ChallengeStatus.COMPLETED
        challenge.completed_at = datetime.now()
        challenge.winner_id = winner_id

        boss = self.region_bosses[challenge.region]

        # Challenger gewinnt!
        if winner_id == challenge.challenger_id:
            # Boss wird gestürzt!
            old_boss_id = boss.player_id
            boss.challenges_lost += 1
            boss.times_dethroned += 1

            # Neuer Boss!
            new_boss = RegionBoss(
                boss_id=len([b for b in self.region_bosses.values() if b]) + 1,
                player_id=challenge.challenger_id,
                region=challenge.region,
                conquest_path=challenge.challenge_type
            )

            self.region_bosses[challenge.region] = new_boss

            # Check für Ultimate Herrscher
            ultimate_check = self._check_ultimate_ruler(challenge.challenger_id)

            result = {
                "challenge_id": challenge_id,
                "winner": "challenger",
                "winner_id": winner_id,
                "old_boss_id": old_boss_id,
                "new_boss_id": winner_id,
                "region": challenge.region.value,
                "message": f"🎉 {challenge.region.value} hat einen neuen Boss!",
                "dethroned": True
            }

            if ultimate_check:
                result["ultimate_ruler"] = True
                result["message"] += "\n👑 ULTIMATE HERRSCHER VON NAJIKA WORLD!"

            return result

        # Boss gewinnt!
        else:
            boss.challenges_won += 1

            # Cooldown setzen
            cooldown_key = (challenge.challenger_id, boss.player_id)
            self.challenge_cooldowns[cooldown_key] = (
                datetime.now() + timedelta(hours=self.CHALLENGE_COOLDOWN_HOURS)
            )

            return {
                "challenge_id": challenge_id,
                "winner": "boss",
                "winner_id": winner_id,
                "region": challenge.region.value,
                "message": f"💪 Boss von {challenge.region.value} hat verteidigt!",
                "dethroned": False,
                "cooldown_hours": self.CHALLENGE_COOLDOWN_HOURS
            }


    def add_conquest_progress(
        self,
        player_id: int,
        region: Region,
        path: ConquestPath,
        progress: float
    ) -> Dict:
        """
        Fügt Eroberungs-Progress hinzu (für Handel/Diplomatie/Quest Wege)

        Returns:
            Progress update dict
        """
        if player_id not in self.conquest_progress:
            self.conquest_progress[player_id] = {}

        if region not in self.conquest_progress[player_id]:
            self.conquest_progress[player_id][region] = {}

        if path not in self.conquest_progress[player_id][region]:
            self.conquest_progress[player_id][region][path] = 0.0

        # Add progress
        self.conquest_progress[player_id][region][path] += progress
        current = self.conquest_progress[player_id][region][path]

        result = {
            "player_id": player_id,
            "region": region.value,
            "path": path.value,
            "progress": current,
            "threshold": self.CONQUEST_THRESHOLD
        }

        # Check ob Threshold erreicht
        if current >= self.CONQUEST_THRESHOLD:
            # Check ob Region bereits Boss hat
            current_boss = self.region_bosses.get(region)

            if current_boss is None:
                # Vacant Region → Spieler wird Boss!
                new_boss = RegionBoss(
                    boss_id=len([b for b in self.region_bosses.values() if b]) + 1,
                    player_id=player_id,
                    region=region,
                    conquest_path=path,
                    conquest_progress=current
                )

                self.region_bosses[region] = new_boss

                result["became_boss"] = True
                result["message"] = f"🎉 Du bist jetzt Boss von {region.value} (via {path.value})!"

                # Check Ultimate
                ultimate_check = self._check_ultimate_ruler(player_id)
                if ultimate_check:
                    result["ultimate_ruler"] = True
                    result["message"] += "\n👑 ULTIMATE HERRSCHER VON NAJIKA WORLD!"

            else:
                result["became_boss"] = False
                result["message"] = f"Region hat bereits Boss. Starte Challenge via Krieg!"

        return result


    def _check_ultimate_ruler(self, player_id: int) -> bool:
        """
        Prüft ob Spieler Ultimate Herrscher ist (alle 8 Regionen)

        Returns:
            True wenn Ultimate Herrscher
        """
        controlled_regions = [
            region for region, boss in self.region_bosses.items()
            if boss and boss.player_id == player_id
        ]

        # Alle 8 Regionen?
        if len(controlled_regions) == 8:
            # Erstelle oder Update Ultimate Herrscher
            if not self.ultimate_ruler or self.ultimate_ruler.player_id != player_id:
                self.ultimate_ruler = UltimateRuler(
                    player_id=player_id,
                    regions_controlled=controlled_regions,
                    became_ultimate_at=datetime.now(),
                    is_ultimate=True,
                    can_world_events=True,
                    can_global_modifiers=True,
                    can_use_najikas_explosion=True,
                    can_set_world_rules=True
                )

            return True

        # Ultimate Herrscher verloren?
        elif self.ultimate_ruler and self.ultimate_ruler.player_id == player_id:
            self.ultimate_ruler.is_ultimate = False
            self.ultimate_ruler.regions_controlled = controlled_regions

        return False


    def set_tax_rate(
        self,
        boss_player_id: int,
        region: Region,
        tax_rate: float
    ) -> Tuple[bool, str]:
        """
        Boss setzt Steuerrate (5-10%)

        Returns:
            (success, message)
        """
        boss = self.region_bosses.get(region)

        if not boss or boss.player_id != boss_player_id:
            return False, "Du bist nicht Boss dieser Region"

        if tax_rate < 5.0 or tax_rate > 10.0:
            return False, "Steuerrate muss zwischen 5% und 10% liegen"

        boss.rights.trade_tax_percentage = tax_rate

        return True, f"Steuerrate auf {tax_rate}% gesetzt"


    async def broadcast_message(
        self,
        boss_player_id: int,
        region: Region,
        message: str
    ) -> Tuple[bool, str]:
        """
        Boss macht Region-weite Ankündigung

        Returns:
            (success, broadcast_message)
        """
        boss = self.region_bosses.get(region)

        if not boss or boss.player_id != boss_player_id:
            return False, "Du bist nicht Boss dieser Region"

        if not boss.rights.can_broadcast:
            return False, "Broadcast-Recht nicht verfügbar"

        broadcast = f"[BOSS von {region.value}]: {message}"

        # Broadcast to all players in the region via WebSocket
        try:
            from backend.services.websocket_manager import websocket_manager

            await websocket_manager.broadcast_to_region(
                region_code=region.value,
                message={
                    'type': 'boss_broadcast',
                    'region': region.value,
                    'boss_player_id': boss_player_id,
                    'message': message,
                    'formatted_message': broadcast,
                    'timestamp': datetime.now().isoformat()
                }
            )
        except Exception as e:
            # Log error but don't fail the broadcast
            print(f"[REGION BOSS] Warning: WebSocket broadcast failed: {e}")

        return True, broadcast


    def get_region_info(self, region: Region) -> Dict:
        """Holt Region-Info inkl. Boss"""
        boss = self.region_bosses.get(region)

        if not boss:
            return {
                "region": region.value,
                "has_boss": False,
                "vacant": True,
                "bonus": self.REGION_BONUSES.get(region, "")
            }

        return {
            "region": region.value,
            "has_boss": True,
            "boss": {
                "player_id": boss.player_id,
                "became_boss_at": boss.became_boss_at.isoformat(),
                "reign_days": boss.total_reign_days,
                "conquest_path": boss.conquest_path.value,
                "tax_rate": boss.rights.trade_tax_percentage,
                "challenges_won": boss.challenges_won,
                "challenges_lost": boss.challenges_lost,
                "reputation": boss.reputation
            },
            "bonus": self.REGION_BONUSES.get(region, "")
        }


    def get_ultimate_ruler_info(self) -> Dict:
        """Holt Ultimate Herrscher Info"""
        if not self.ultimate_ruler or not self.ultimate_ruler.is_ultimate:
            return {
                "has_ultimate_ruler": False,
                "message": "Kein Ultimate Herrscher"
            }

        return {
            "has_ultimate_ruler": True,
            "player_id": self.ultimate_ruler.player_id,
            "title": "Kaiser/Kaiserin von Najika World",
            "regions_controlled": [r.value for r in self.ultimate_ruler.regions_controlled],
            "became_ultimate_at": self.ultimate_ruler.became_ultimate_at.isoformat(),
            "total_days": self.ultimate_ruler.total_ultimate_days,
            "powers": {
                "world_events": self.ultimate_ruler.can_world_events,
                "global_modifiers": self.ultimate_ruler.can_global_modifiers,
                "najikas_explosion": self.ultimate_ruler.can_use_najikas_explosion,
                "world_rules": self.ultimate_ruler.can_set_world_rules
            }
        }


    def _count_challenges_this_week(self, challenger_id: int, boss_id: int) -> int:
        """Zählt Challenges diese Woche"""
        week_ago = datetime.now() - timedelta(days=7)

        count = 0
        for challenge in self.challenges.values():
            if (challenge.challenger_id == challenger_id and
                challenge.boss_id == boss_id and
                challenge.created_at > week_ago):
                count += 1

        return count


    def export_state(self) -> Dict:
        """Exportiert kompletten State"""
        return {
            "region_bosses": {
                region.value: {
                    "boss_id": boss.boss_id,
                    "player_id": boss.player_id,
                    "region": boss.region.value,
                    "became_boss_at": boss.became_boss_at.isoformat(),
                    "total_reign_days": boss.total_reign_days,
                    "conquest_path": boss.conquest_path.value,
                    "challenges_won": boss.challenges_won,
                    "challenges_lost": boss.challenges_lost,
                    "reputation": boss.reputation,
                    "tax_rate": boss.rights.trade_tax_percentage
                } if boss else None
                for region, boss in self.region_bosses.items()
            },
            "ultimate_ruler": {
                "player_id": self.ultimate_ruler.player_id,
                "is_ultimate": self.ultimate_ruler.is_ultimate,
                "regions_controlled": [r.value for r in self.ultimate_ruler.regions_controlled],
                "became_ultimate_at": self.ultimate_ruler.became_ultimate_at.isoformat() if self.ultimate_ruler.became_ultimate_at else None
            } if self.ultimate_ruler else None
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== Region Boss System Test ===\n")

    boss_sys = RegionBossSystem()

    # Test 1: Player 1 erobert Region via Handel
    print("1. Player 1 erobert Samtmoos-Tiefwald via Handel")
    for i in range(5):
        result = boss_sys.add_conquest_progress(
            1, Region.SAMTMOOS_TIEFWALD, ConquestPath.TRADE, 25.0
        )
        print(f"   Progress: {result['progress']}/{result['threshold']}")

    if result.get('became_boss'):
        print(f"   → {result['message']}\n")

    # Test 2: Player 2 challenged Player 1
    print("2. Player 2 challenged Player 1 (Krieg)")
    success, challenge_id, msg = boss_sys.create_challenge(
        2, Region.SAMTMOOS_TIEFWALD, ConquestPath.WAR
    )
    print(f"   → {msg} (Challenge ID: {challenge_id})\n")

    # Test 3: Player 1 akzeptiert
    print("3. Player 1 akzeptiert Challenge")
    success, msg = boss_sys.accept_challenge(challenge_id, 1)
    print(f"   → {msg}\n")

    # Test 4: Player 2 gewinnt!
    print("4. Challenge completed - Player 2 gewinnt!")
    result = boss_sys.complete_challenge(challenge_id, 2)
    print(f"   → {result['message']}")
    print(f"   → Dethroned: {result['dethroned']}\n")

    # Test 5: Player 2 setzt Steuerrate
    print("5. Player 2 setzt Steuerrate")
    success, msg = boss_sys.set_tax_rate(2, Region.SAMTMOOS_TIEFWALD, 7.5)
    print(f"   → {msg}\n")

    # Test 6: Player 2 Broadcast
    print("6. Player 2 macht Broadcast")
    success, broadcast = boss_sys.broadcast_message(
        2, Region.SAMTMOOS_TIEFWALD,
        "Willkommen! Steuern sind jetzt 7.5%!"
    )
    print(f"   → {broadcast}\n")

    # Test 7: Region Info
    print("7. Region Info")
    info = boss_sys.get_region_info(Region.SAMTMOOS_TIEFWALD)
    print(f"   Boss: Player {info['boss']['player_id']}")
    print(f"   Tax Rate: {info['boss']['tax_rate']}%")
    print(f"   Conquest Path: {info['boss']['conquest_path']}")
    print(f"   Bonus: {info['bonus']}")

    print("\n=== Region Boss System Test Complete ===")
