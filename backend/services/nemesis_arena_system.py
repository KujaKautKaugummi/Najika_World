"""
Najika Nemesis Arena System
Shadow of Mordor meets Digimon World nemesis/hierarchy system

Monsters remember encounters, build grudges, and climb hierarchy to become Arena King.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Set
import random
from datetime import datetime
import json


class RulerRank(Enum):
    """Arena hierarchy ranks (Shadow of Mordor style)"""
    NOBODY = "Niemand"
    FIGHTER = "Kämpfer"
    GLADIATOR = "Gladiator"
    CHAMPION = "Champion"
    REGION_LORD = "Gebietsherrscher"
    ARENA_KING = "ARENA-KÖNIG"


class MonsterType(Enum):
    """Monster species types"""
    SLIME = "Slime"
    BEAST = "Bestie"
    DRAGON = "Drache"
    UNDEAD = "Untot"
    DEMON = "Dämon"
    ELEMENTAL = "Elementar"
    MACHINE = "Maschine"
    PLANT = "Pflanze"


class PersonalityTrait(Enum):
    """Monster personality traits that develop through combat"""
    COWARD = "Feigling"
    BRAVE = "Mutig"
    VENGEFUL = "Rachsüchtig"
    HONORABLE = "Ehrenvoll"
    SADISTIC = "Sadistisch"
    CUNNING = "Gerissen"
    BERSERKER = "Berserker"
    TACTICAL = "Taktisch"


@dataclass
class BattleMemory:
    """A memory of a specific battle"""
    timestamp: datetime
    opponent_name: str
    opponent_id: int
    result: str  # "won", "lost", "fled", "saved"
    how_it_happened: str
    damage_taken: int
    damage_dealt: int
    special_events: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "opponent_name": self.opponent_name,
            "opponent_id": self.opponent_id,
            "result": self.result,
            "how_it_happened": self.how_it_happened,
            "damage_taken": self.damage_taken,
            "damage_dealt": self.damage_dealt,
            "special_events": self.special_events
        }


@dataclass
class NemesisMonster:
    """
    A nemesis monster with personality, memories, and hierarchy position

    Shadow of Mordor style: Monsters remember you, hold grudges, and climb ranks
    """
    id: int
    name: str
    title: str
    monster_type: MonsterType
    rank: RulerRank = RulerRank.NOBODY

    # Stats
    level: int = 1
    max_health: int = 100
    current_health: int = 100
    attack: int = 10
    defense: int = 5

    # Memory system
    kills: int = 0
    deaths: int = 0
    encounters_with_player: int = 0
    battles: List[BattleMemory] = field(default_factory=list)
    grudges: List[str] = field(default_factory=list)  # "You killed my brother!"
    memories: Dict[str, List[str]] = field(default_factory=dict)  # player_id → memories

    # Personality
    personality_traits: Set[PersonalityTrait] = field(default_factory=set)
    special_moves: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)

    # Hierarchy
    region_controlled: Optional[str] = None
    subordinates: List[int] = field(default_factory=list)  # Monster IDs
    boss_id: Optional[int] = None
    rival_ids: List[int] = field(default_factory=list)

    # Appearance
    has_scars: bool = False
    scar_descriptions: List[str] = field(default_factory=list)
    appearance_modifiers: List[str] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert to dictionary for API response"""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "monster_type": self.monster_type.value,
            "rank": self.rank.value,
            "level": self.level,
            "max_health": self.max_health,
            "current_health": self.current_health,
            "attack": self.attack,
            "defense": self.defense,
            "kills": self.kills,
            "deaths": self.deaths,
            "encounters_with_player": self.encounters_with_player,
            "grudges": self.grudges,
            "personality_traits": [trait.value for trait in self.personality_traits],
            "special_moves": self.special_moves,
            "weaknesses": self.weaknesses,
            "strengths": self.strengths,
            "region_controlled": self.region_controlled,
            "has_scars": self.has_scars,
            "scar_descriptions": self.scar_descriptions,
            "appearance_modifiers": self.appearance_modifiers,
            "last_seen": self.last_seen.isoformat()
        }


class NemesisArenaSystem:
    """
    Manages the nemesis arena hierarchy and monster AI

    Features:
    - Monsters remember encounters and build personalities
    - Hierarchy system with 6 ranks
    - Grudge system (Shadow of Mordor style)
    - Dynamic title generation
    - Region control and territory wars
    """

    def __init__(self):
        self.monsters: Dict[int, NemesisMonster] = {}
        self.next_monster_id = 1
        self.arena_king_id: Optional[int] = None
        self.region_lords: Dict[str, int] = {}  # region → monster_id

        # Initialize arena with some monsters
        self._init_arena()

    def _init_arena(self):
        """Initialize arena with starter monsters"""
        regions = ["Wald", "Wüste", "Gebirge", "Sumpf", "Vulkan"]

        for i, region in enumerate(regions):
            monster = self.create_monster(
                monster_type=random.choice(list(MonsterType)),
                rank=RulerRank.FIGHTER,
                region=region
            )

    def create_monster(
        self,
        monster_type: MonsterType,
        rank: RulerRank = RulerRank.NOBODY,
        region: Optional[str] = None,
        level: int = 1
    ) -> NemesisMonster:
        """Create a new nemesis monster"""
        name = self._generate_monster_name(monster_type)
        title = self._generate_title(rank, monster_type)

        monster = NemesisMonster(
            id=self.next_monster_id,
            name=name,
            title=title,
            monster_type=monster_type,
            rank=rank,
            level=level,
            max_health=100 + (level * 20),
            current_health=100 + (level * 20),
            attack=10 + (level * 2),
            defense=5 + level,
            region_controlled=region
        )

        # Generate initial personality
        self._generate_initial_personality(monster)

        self.monsters[monster.id] = monster
        self.next_monster_id += 1

        return monster

    def _generate_monster_name(self, monster_type: MonsterType) -> str:
        """Generate random monster name"""
        prefixes = {
            MonsterType.SLIME: ["Gloop", "Blob", "Goo", "Slurp"],
            MonsterType.BEAST: ["Fang", "Claw", "Howl", "Growl"],
            MonsterType.DRAGON: ["Flame", "Scale", "Wing", "Roar"],
            MonsterType.UNDEAD: ["Bone", "Skull", "Grave", "Ghost"],
            MonsterType.DEMON: ["Dark", "Shadow", "Hell", "Doom"],
            MonsterType.ELEMENTAL: ["Storm", "Blaze", "Frost", "Terra"],
            MonsterType.MACHINE: ["Steel", "Bolt", "Circuit", "Gear"],
            MonsterType.PLANT: ["Thorn", "Root", "Vine", "Petal"]
        }

        suffixes = ["bane", "fist", "jaw", "heart", "eye", "tooth", "claw"]

        prefix = random.choice(prefixes[monster_type])
        suffix = random.choice(suffixes)

        return f"{prefix}-{suffix}"

    def _generate_title(self, rank: RulerRank, monster_type: MonsterType) -> str:
        """Generate title based on rank and type"""
        titles = {
            RulerRank.NOBODY: ["der Schwache", "der Niemand", "der Fußsoldat"],
            RulerRank.FIGHTER: ["der Kämpfer", "der Krieger", "der Streiter"],
            RulerRank.GLADIATOR: ["der Gladiator", "der Veteran", "der Krieger"],
            RulerRank.CHAMPION: ["der Champion", "der Held", "der Sieger"],
            RulerRank.REGION_LORD: ["der Gebietsherr", "der Warlord", "der Herrscher"],
            RulerRank.ARENA_KING: ["DER ARENA-KÖNIG", "DER ABSOLUTE HERRSCHER", "DER IMPERATOR"]
        }

        return random.choice(titles[rank])

    def _generate_initial_personality(self, monster: NemesisMonster):
        """Generate initial personality traits and moves"""
        # Add 1-3 personality traits
        num_traits = random.randint(1, 3)
        traits = random.sample(list(PersonalityTrait), num_traits)
        monster.personality_traits = set(traits)

        # Generate special moves based on type
        monster.special_moves = self._generate_special_moves(monster.monster_type, monster.rank)

        # Generate weaknesses and strengths
        monster.weaknesses = self._generate_weaknesses(monster.monster_type)
        monster.strengths = self._generate_strengths(monster.monster_type)

    def _generate_special_moves(self, monster_type: MonsterType, rank: RulerRank) -> List[str]:
        """Generate special moves based on type and rank"""
        moves = {
            MonsterType.SLIME: ["Acid Splash", "Split Form", "Engulf"],
            MonsterType.BEAST: ["Feral Charge", "Pack Tactics", "Savage Bite"],
            MonsterType.DRAGON: ["Fire Breath", "Wing Buffet", "Tail Sweep"],
            MonsterType.UNDEAD: ["Life Drain", "Necrotic Touch", "Fear Aura"],
            MonsterType.DEMON: ["Hellfire", "Dark Pact", "Soul Rend"],
            MonsterType.ELEMENTAL: ["Elemental Burst", "Phase Shift", "Storm Call"],
            MonsterType.MACHINE: ["Laser Beam", "Overcharge", "Repair Protocol"],
            MonsterType.PLANT: ["Vine Whip", "Poison Spores", "Regenerate"]
        }

        base_moves = moves.get(monster_type, ["Basic Attack"])

        # Higher ranks get more moves
        if rank.value in [RulerRank.CHAMPION.value, RulerRank.REGION_LORD.value, RulerRank.ARENA_KING.value]:
            base_moves.append("Ultimate Attack")

        return random.sample(base_moves, min(3, len(base_moves)))

    def _generate_weaknesses(self, monster_type: MonsterType) -> List[str]:
        """Generate type-based weaknesses"""
        weaknesses = {
            MonsterType.SLIME: ["Fire", "Ice"],
            MonsterType.BEAST: ["Noise", "Traps"],
            MonsterType.DRAGON: ["Dragon-Slayer Weapons"],
            MonsterType.UNDEAD: ["Holy Magic", "Sunlight"],
            MonsterType.DEMON: ["Holy Magic", "Exorcism"],
            MonsterType.ELEMENTAL: ["Opposite Element"],
            MonsterType.MACHINE: ["EMP", "Water"],
            MonsterType.PLANT: ["Fire", "Poison"]
        }
        return weaknesses.get(monster_type, [])

    def _generate_strengths(self, monster_type: MonsterType) -> List[str]:
        """Generate type-based strengths"""
        strengths = {
            MonsterType.SLIME: ["Physical Resistance"],
            MonsterType.BEAST: ["Speed", "Pack Hunting"],
            MonsterType.DRAGON: ["High Defense", "Fire Immunity"],
            MonsterType.UNDEAD: ["Poison Immunity", "Fear Resistance"],
            MonsterType.DEMON: ["Dark Magic", "Intimidation"],
            MonsterType.ELEMENTAL: ["Elemental Immunity"],
            MonsterType.MACHINE: ["Logic", "No Emotions"],
            MonsterType.PLANT: ["Regeneration", "Nature Magic"]
        }
        return strengths.get(monster_type, [])

    def battle(
        self,
        monster_id: int,
        player_id: int,
        player_name: str,
        player_damage: int,
        battle_events: List[str]
    ) -> Dict:
        """
        Execute a battle with a nemesis monster

        Args:
            monster_id: ID of monster to battle
            player_id: Player ID
            player_name: Player name
            player_damage: Damage dealt by player
            battle_events: List of special events (e.g., "Player used fire spell", "Monster fled")

        Returns:
            Battle result dictionary
        """
        monster = self.monsters.get(monster_id)
        if not monster:
            return {"success": False, "error": "Monster not found"}

        # Update encounter count
        monster.encounters_with_player += 1
        monster.last_seen = datetime.now()

        # Apply damage
        actual_damage = max(1, player_damage - monster.defense)
        monster.current_health -= actual_damage

        # Determine result
        if monster.current_health <= 0:
            result = self._handle_monster_death(monster, player_id, player_name, actual_damage, battle_events)
        elif "fled" in [e.lower() for e in battle_events]:
            result = self._handle_monster_fled(monster, player_id, player_name, actual_damage, battle_events)
        else:
            result = self._handle_ongoing_battle(monster, player_id, player_name, actual_damage, battle_events)

        return result

    def _handle_monster_death(
        self,
        monster: NemesisMonster,
        player_id: int,
        player_name: str,
        damage: int,
        events: List[str]
    ) -> Dict:
        """Handle monster death and possible resurrection"""
        monster.deaths += 1

        # Calculate monster damage dealt (based on monster stats)
        monster_damage_dealt = max(1, monster.attack - 2)  # Simple calculation

        # Create battle memory
        memory = BattleMemory(
            timestamp=datetime.now(),
            opponent_name=player_name,
            opponent_id=player_id,
            result="lost",
            how_it_happened=f"Wurde besiegt durch {', '.join(events[:2]) if events else 'starken Angriff'}",
            damage_taken=damage,
            damage_dealt=monster_damage_dealt,
            special_events=events
        )
        monster.battles.append(memory)

        # Add grudge
        grudge = f"Du hast mich getötet mit {events[0] if events else 'brutaler Gewalt'}! Ich werde zurückkommen!"
        monster.grudges.append(grudge)

        # 50% chance to return stronger (Shadow of Mordor style)
        will_return = random.random() < 0.5

        if will_return:
            # Resurrect stronger
            monster.level += 1
            monster.max_health += 20
            monster.current_health = monster.max_health
            monster.attack += 2
            monster.defense += 1

            # Add scar
            monster.has_scars = True
            scar = random.choice([
                "Narbe über dem Auge",
                "Verbrannte Haut",
                "Fehlender Arm (durch Metallprothese ersetzt)",
                "Halb zerstörtes Gesicht",
                "Blutende Wunde"
            ])
            monster.scar_descriptions.append(scar)

            # Add VENGEFUL trait
            monster.personality_traits.add(PersonalityTrait.VENGEFUL)

            return {
                "success": True,
                "result": "monster_died",
                "will_return": True,
                "message": f"🔥 {monster.name} wurde besiegt!\n💀 Aber er wird STÄRKER zurückkehren mit: {scar}",
                "monster": monster.to_dict(),
                "grudge": grudge,
                "xp_gained": monster.level * 100
            }
        else:
            # Permanently dead
            # Another monster may take their place
            return {
                "success": True,
                "result": "monster_killed",
                "will_return": False,
                "message": f"💀 {monster.name} wurde PERMANENT besiegt!",
                "monster": monster.to_dict(),
                "xp_gained": monster.level * 150
            }

    def _handle_monster_fled(
        self,
        monster: NemesisMonster,
        player_id: int,
        player_name: str,
        damage: int,
        events: List[str]
    ) -> Dict:
        """Handle monster fleeing from battle"""
        # Add COWARD trait or remove BRAVE trait
        monster.personality_traits.discard(PersonalityTrait.BRAVE)
        monster.personality_traits.add(PersonalityTrait.COWARD)

        memory = BattleMemory(
            timestamp=datetime.now(),
            opponent_name=player_name,
            opponent_id=player_id,
            result="fled",
            how_it_happened="Geflohen aus Angst",
            damage_taken=damage,
            damage_dealt=0,
            special_events=events
        )
        monster.battles.append(memory)

        return {
            "success": True,
            "result": "monster_fled",
            "message": f"🏃 {monster.name} ist geflohen! Er wird sich an dich erinnern...",
            "monster": monster.to_dict()
        }

    def _handle_ongoing_battle(
        self,
        monster: NemesisMonster,
        player_id: int,
        player_name: str,
        damage: int,
        events: List[str]
    ) -> Dict:
        """Handle ongoing battle"""
        return {
            "success": True,
            "result": "battle_ongoing",
            "monster_health": monster.current_health,
            "monster_max_health": monster.max_health,
            "message": f"⚔️ {monster.name} kämpft weiter! {monster.current_health}/{monster.max_health} HP",
            "monster": monster.to_dict()
        }

    def promote_monster(self, monster_id: int) -> Dict:
        """Promote a monster to the next rank"""
        monster = self.monsters.get(monster_id)
        if not monster:
            return {"success": False, "error": "Monster not found"}

        rank_order = list(RulerRank)
        current_index = rank_order.index(monster.rank)

        if current_index >= len(rank_order) - 1:
            return {"success": False, "error": "Already at max rank"}

        # Promote
        new_rank = rank_order[current_index + 1]
        monster.rank = new_rank
        monster.title = self._generate_title(new_rank, monster.monster_type)

        # Stat boost
        monster.max_health += 50
        monster.current_health = monster.max_health
        monster.attack += 5
        monster.defense += 3
        monster.level += 2

        # If became Arena King
        if new_rank == RulerRank.ARENA_KING:
            self.arena_king_id = monster_id

        return {
            "success": True,
            "monster": monster.to_dict(),
            "message": f"🏆 {monster.name} wurde zum {new_rank.value}!"
        }

    def get_arena_hierarchy(self) -> Dict:
        """Get complete arena hierarchy"""
        hierarchy = {
            "arena_king": None,
            "region_lords": [],
            "champions": [],
            "gladiators": [],
            "fighters": [],
            "nobodies": []
        }

        for monster in self.monsters.values():
            if monster.rank == RulerRank.ARENA_KING:
                hierarchy["arena_king"] = monster.to_dict()
            elif monster.rank == RulerRank.REGION_LORD:
                hierarchy["region_lords"].append(monster.to_dict())
            elif monster.rank == RulerRank.CHAMPION:
                hierarchy["champions"].append(monster.to_dict())
            elif monster.rank == RulerRank.GLADIATOR:
                hierarchy["gladiators"].append(monster.to_dict())
            elif monster.rank == RulerRank.FIGHTER:
                hierarchy["fighters"].append(monster.to_dict())
            else:
                hierarchy["nobodies"].append(monster.to_dict())

        return hierarchy

    def get_monster_intro_speech(self, monster_id: int, player_name: str) -> str:
        """Generate dramatic intro speech (Shadow of Mordor style)"""
        monster = self.monsters.get(monster_id)
        if not monster:
            return ""

        speeches = []

        # First encounter
        if monster.encounters_with_player == 1:
            speeches = [
                f"Ich bin {monster.name}, {monster.title}!",
                f"Bereite dich auf deinen Tod vor, {player_name}!"
            ]
        # Has grudge
        elif monster.grudges:
            speeches = [
                f"DU! {player_name}!",
                random.choice(monster.grudges),
                "JETZT WIRST DU BEZAHLEN!"
            ]
        # Returned from death
        elif monster.deaths > 0:
            speeches = [
                f"Ich bin zurückgekehrt, {player_name}!",
                "Der Tod konnte mich nicht aufhalten!",
                f"Diesmal werde ICH siegen!"
            ]
        else:
            speeches = [
                f"Ah, {player_name}... wir treffen uns wieder.",
                "Bist du bereit zu verlieren?"
            ]

        return "\n".join(speeches)


# Global nemesis arena instance
nemesis_arena = NemesisArenaSystem()
