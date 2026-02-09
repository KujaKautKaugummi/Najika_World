"""
🏛️ NAJIKA WORLD - NEMESIS ARENA SYSTEM
Shadow of Mordor meets Digimon World Arena
Version: 1.0
"""

import json
import random
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# ============================================
# CORE NEMESIS SYSTEM
# ============================================

class MonsterType(Enum):
    GOBLIN = "Goblin"
    SLIME = "Slime"
    ORC = "Ork"
    DEMON = "Dämon"
    DRAGON = "Drache"
    SHADOW = "Schatten"
    ELEMENTAL = "Elementar"
    UNDEAD = "Untot"

class RulerRank(Enum):
    NOBODY = "Niemand"
    FIGHTER = "Kämpfer"
    GLADIATOR = "Gladiator"
    CHAMPION = "Champion"
    REGION_LORD = "Gebietsherrscher"
    ARENA_KING = "ARENA-KÖNIG"

@dataclass
class NemesisMonster:
    """Monster die sich an Spieler erinnern und aufsteigen können"""
    
    # Identität
    id: str
    name: str
    title: str = "der Namenlose"
    type: MonsterType = MonsterType.GOBLIN
    level: int = 1
    
    # Kampf-Stats
    hp: int = 100
    max_hp: int = 100
    attack: int = 10
    defense: int = 5
    speed: int = 10
    
    # Nemesis-System
    kills: int = 0
    deaths: int = 0
    rank: RulerRank = RulerRank.NOBODY
    grudges: List[str] = field(default_factory=list)  # Spieler die es hasst
    killed_by: List[str] = field(default_factory=list)  # Wer es getötet hat
    
    # Persönlichkeit
    personality_traits: List[str] = field(default_factory=list)
    battle_scars: List[str] = field(default_factory=list)
    special_moves: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    
    # Erinnerungen
    memories: Dict[str, List[str]] = field(default_factory=dict)
    last_encounter: Optional[float] = None
    
    def __post_init__(self):
        """Generiere einzigartige Persönlichkeit"""
        if not self.personality_traits:
            self._generate_personality()
        if not self.special_moves:
            self._generate_moves()
    
    def _generate_personality(self):
        """Generiere zufällige Persönlichkeits-Traits"""
        traits_pool = [
            "Brutal", "Hinterhältig", "Feige", "Mutig", "Verrückt",
            "Rachsüchtig", "Gnadenlos", "Clever", "Berserker", "Sadistisch",
            "Paranoid", "Arrogant", "Vorsichtig", "Blutrünstig", "Ehrenhaft"
        ]
        self.personality_traits = random.sample(traits_pool, min(3, len(traits_pool)))
    
    def _generate_moves(self):
        """Generiere Spezial-Moves basierend auf Typ"""
        move_pools = {
            MonsterType.GOBLIN: ["Giftklinge", "Hinterhalt", "Goblin-Schwarm"],
            MonsterType.SLIME: ["Säure-Spucken", "Teilung", "Absorption"],
            MonsterType.ORC: ["Kriegsschrei", "Berserker-Wut", "Schädelspalter"],
            MonsterType.DEMON: ["Höllenfeuer", "Seelenbrand", "Dunkelheit"],
            MonsterType.DRAGON: ["Feueratem", "Drachenschuppen", "Flügelschlag"],
            MonsterType.SHADOW: ["Schattengriff", "Unsichtbarkeit", "Lebensraub"],
            MonsterType.ELEMENTAL: ["Element-Explosion", "Form-Wechsel", "Energie-Schild"],
            MonsterType.UNDEAD: ["Verwesung", "Untoten-Erweckung", "Seuchenatem"]
        }
        
        pool = move_pools.get(self.type, ["Basis-Angriff"])
        self.special_moves = random.sample(pool, min(2, len(pool)))
    
    def after_killing_player(self, player_name: str):
        """Monster hat Spieler getötet - Level up!"""
        self.kills += 1
        self.level += 1
        
        # Stats erhöhen
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 3
        self.speed += 2
        
        # Neue Narbe/Trophäe
        scar = f"Trophäe von {player_name}"
        if scar not in self.battle_scars:
            self.battle_scars.append(scar)
        
        # Persönlichkeit entwickelt sich
        if self.kills >= 3 and "Berühmt" not in self.personality_traits:
            self.personality_traits.append("Berühmt")
        if self.kills >= 5 and "Legendär" not in self.personality_traits:
            self.personality_traits.append("Legendär")
        
        # Rang-Aufstieg
        self._update_rank()
        
        # Erinnerung speichern
        if player_name not in self.memories:
            self.memories[player_name] = []
        self.memories[player_name].append(f"Getötet am {time.strftime('%Y-%m-%d %H:%M')}")
        
        # Neuer Titel
        self._update_title(player_name)
    
    def after_being_killed(self, player_name: str):
        """Monster wurde getötet"""
        self.deaths += 1
        
        # Grudge entwickeln (kommt stärker zurück!)
        if player_name not in self.grudges:
            self.grudges.append(player_name)
        if player_name not in self.killed_by:
            self.killed_by.append(player_name)
        
        # Neue Schwäche
        weakness = f"Angst vor {player_name}'s Technik"
        if weakness not in self.weaknesses:
            self.weaknesses.append(weakness)
    
    def resurrect_with_grudge(self):
        """Monster kommt zurück - STÄRKER und WÜTENDER!"""
        self.hp = self.max_hp
        
        # Power-Up durch Wut
        self.attack += 10
        self.defense += 5
        self.max_hp += 30
        
        # Neue Narbe
        self.battle_scars.append("Wiederbelebt durch pure Wut")
        
        # Rache-Persönlichkeit
        if "Rachsüchtig" not in self.personality_traits:
            self.personality_traits.append("Rachsüchtig")
        
        return self
    
    def _update_rank(self):
        """Aktualisiere Rang basierend auf Kills"""
        if self.kills >= 50:
            self.rank = RulerRank.ARENA_KING
        elif self.kills >= 25:
            self.rank = RulerRank.REGION_LORD
        elif self.kills >= 10:
            self.rank = RulerRank.CHAMPION
        elif self.kills >= 5:
            self.rank = RulerRank.GLADIATOR
        elif self.kills >= 1:
            self.rank = RulerRank.FIGHTER
    
    def _update_title(self, last_victim: str):
        """Generiere neuen Titel basierend auf Taten"""
        if self.kills >= 10:
            self.title = f"der Schlächter von {last_victim}"
        elif self.kills >= 5:
            self.title = "der Unbezwingbare"
        elif self.kills >= 3:
            self.title = "der Gladiator"
        elif self.kills >= 1:
            self.title = f"{last_victim}'s Fluch"
    
    def generate_taunt(self, player_name: str) -> str:
        """Generiere personalisierte Beleidigung"""
        if player_name in self.grudges:
            return f"Du schon wieder, {player_name}?! Diesmal werde ich dich ZERSTÖREN!"
        elif player_name in self.memories:
            return f"Ich erinnere mich an dich, {player_name}... Zeit für Runde {len(self.memories[player_name]) + 1}!"
        elif self.kills > 10:
            return f"Ein weiteres Opfer für {self.name} {self.title}!"
        else:
            return f"Frischfleisch! Komm her, {player_name}!"
    
    def to_dict(self) -> Dict:
        """Konvertiere zu Dictionary für Speicherung"""
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'type': self.type.value,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'kills': self.kills,
            'deaths': self.deaths,
            'rank': self.rank.value,
            'grudges': self.grudges,
            'killed_by': self.killed_by,
            'personality_traits': self.personality_traits,
            'battle_scars': self.battle_scars,
            'special_moves': self.special_moves,
            'weaknesses': self.weaknesses,
            'memories': self.memories,
            'last_encounter': self.last_encounter
        }


# ============================================
# ARENA MANAGEMENT SYSTEM
# ============================================

class ArenaManager:
    """Verwaltet die Arena und alle Nemesis-Monster"""
    
    def __init__(self):
        self.monsters: Dict[str, NemesisMonster] = {}
        self.hierarchy: Dict[str, List[str]] = {
            'arena_king': None,
            'region_lords': {},  # region_name: monster_id
            'champions': [],
            'gladiators': [],
            'fighters': []
        }
        self.regions = [
            "Bernstein-Dünen", "Smaragd-Hain", "Azur-Klippen",
            "Amethyst-Steppe", "Onyx-Morast", "Perl-Gletscher",
            "Rubin-Schlucht", "Obsidian-Nacht"
        ]
        self.active_battles: Dict[str, Dict] = {}
        
        # Generiere initiale Monster-Population
        self._populate_arena()
    
    def _populate_arena(self):
        """Erstelle initiale Monster-Population"""
        monster_names = [
            "Grok", "Snarl", "Krug", "Thok", "Grim", "Zog", "Morg", "Brak",
            "Ugluk", "Shagrat", "Gorbag", "Lugdush", "Mauhur", "Grishnakh",
            "Bolg", "Azog", "Gothmog", "Guritz", "Lagduf", "Muzgash"
        ]
        
        for i in range(20):
            name = random.choice(monster_names)
            title = random.choice(["der Grausame", "der Blutige", "der Wilde", "der Starke"])
            monster_type = random.choice(list(MonsterType))
            
            monster_id = f"monster_{i}_{int(time.time())}"
            monster = NemesisMonster(
                id=monster_id,
                name=f"{name}",
                title=title,
                type=monster_type,
                level=random.randint(1, 5)
            )
            
            self.monsters[monster_id] = monster
    
    def get_arena_challenger(self, player_level: int) -> Optional[NemesisMonster]:
        """Finde passenden Gegner für Spieler"""
        # Priorität 1: Monster mit Grudge gegen Spieler
        # Priorität 2: Monster auf ähnlichem Level
        # Priorität 3: Zufälliges Monster
        
        eligible = []
        for monster in self.monsters.values():
            level_diff = abs(monster.level - player_level)
            if level_diff <= 5:  # Max 5 Level Unterschied
                eligible.append(monster)
        
        if eligible:
            return random.choice(eligible)
        return None
    
    def process_battle_result(self, 
                            monster_id: str, 
                            player_name: str, 
                            player_won: bool,
                            battle_data: Dict) -> Dict:
        """Verarbeite Kampf-Ergebnis und aktualisiere Nemesis-System"""
        
        if monster_id not in self.monsters:
            return {'error': 'Monster nicht gefunden'}
        
        monster = self.monsters[monster_id]
        result = {
            'monster_reaction': None,
            'rank_change': False,
            'new_ruler': None,
            'loot': None,
            'nemesis_event': None
        }
        
        if player_won:
            # Spieler hat gewonnen
            monster.after_being_killed(player_name)
            
            # Loot basierend auf Monster-Rang
            result['loot'] = self._generate_loot(monster)
            
            # 30% Chance dass Monster zurückkommt
            if random.random() < 0.3:
                monster.resurrect_with_grudge()
                result['nemesis_event'] = {
                    'type': 'resurrection',
                    'message': f"{monster.name} schwört Rache und wird wiederbelebt!",
                    'monster_buff': '+10 ATK, +30 HP'
                }
            
        else:
            # Monster hat gewonnen
            monster.after_killing_player(player_name)
            
            # Check für Rang-Aufstieg
            old_rank = monster.rank
            if monster.rank != old_rank:
                result['rank_change'] = True
                result['nemesis_event'] = {
                    'type': 'promotion',
                    'message': f"{monster.name} steigt auf zu: {monster.rank.value}!",
                    'old_rank': old_rank.value,
                    'new_rank': monster.rank.value
                }
                
                # Check für Gebietsherrschaft
                if monster.rank == RulerRank.REGION_LORD:
                    region = self._assign_region(monster)
                    if region:
                        result['new_ruler'] = {
                            'region': region,
                            'monster': monster.name,
                            'effects': self._get_region_effects(monster.type)
                        }
        
        # Monster-Reaktion
        result['monster_reaction'] = monster.generate_taunt(player_name)
        
        # Update letzte Begegnung
        monster.last_encounter = time.time()
        
        return result
    
    def _generate_loot(self, monster: NemesisMonster) -> Dict:
        """Generiere Loot basierend auf Monster-Rang"""
        loot = {
            'gold': monster.level * 10,
            'xp': monster.level * 15,
            'items': []
        }
        
        # Bessere Items von höheren Rängen
        if monster.rank == RulerRank.ARENA_KING:
            loot['items'].append({'name': 'Königskrone', 'rarity': 'Legendary'})
            loot['gold'] *= 10
        elif monster.rank == RulerRank.REGION_LORD:
            loot['items'].append({'name': 'Herrschermantel', 'rarity': 'Epic'})
            loot['gold'] *= 5
        elif monster.rank == RulerRank.CHAMPION:
            loot['items'].append({'name': 'Champion-Gürtel', 'rarity': 'Rare'})
            loot['gold'] *= 3
        
        # Chance auf Monster-spezifische Items
        if random.random() < 0.3:
            loot['items'].append({
                'name': f"{monster.name}'s {random.choice(['Schwert', 'Schild', 'Helm'])}",
                'rarity': 'Unique',
                'stats': {'attack': monster.attack // 2}
            })
        
        return loot
    
    def _assign_region(self, monster: NemesisMonster) -> Optional[str]:
        """Weise Monster eine Region zu"""
        # Finde freie Region
        for region in self.regions:
            if region not in self.hierarchy['region_lords']:
                self.hierarchy['region_lords'][region] = monster.id
                return region
        
        # Oder ersetze schwächeren Herrscher
        weakest_region = None
        weakest_level = 999
        
        for region, ruler_id in self.hierarchy['region_lords'].items():
            ruler = self.monsters.get(ruler_id)
            if ruler and ruler.level < weakest_level:
                weakest_level = ruler.level
                weakest_region = region
        
        if weakest_region and monster.level > weakest_level:
            # Entthrone schwächeren Herrscher
            old_ruler_id = self.hierarchy['region_lords'][weakest_region]
            if old_ruler_id in self.monsters:
                self.monsters[old_ruler_id].rank = RulerRank.CHAMPION
            
            self.hierarchy['region_lords'][weakest_region] = monster.id
            return weakest_region
        
        return None
    
    def _get_region_effects(self, monster_type: MonsterType) -> Dict:
        """Bestimme Regions-Effekte basierend auf Herrscher-Typ"""
        effects = {
            MonsterType.GOBLIN: {
                'spawn_rate': 1.5,
                'aggression': 2.0,
                'special': 'Goblin-Händler erscheinen',
                'description': 'Die Region wird von Goblins überrannt!'
            },
            MonsterType.SLIME: {
                'spawn_rate': 0.8,
                'aggression': 0.5,
                'special': 'Heilquellen erscheinen',
                'description': 'Die Region wird friedlicher und grüner.'
            },
            MonsterType.DEMON: {
                'spawn_rate': 1.2,
                'aggression': 3.0,
                'special': 'Permanente Dunkelheit',
                'description': 'Die Region brennt in Höllenfeuer!'
            },
            MonsterType.DRAGON: {
                'spawn_rate': 0.9,
                'aggression': 1.5,
                'special': 'Seltene Schätze',
                'description': 'Der Drache hortet Schätze in der Region.'
            },
            MonsterType.UNDEAD: {
                'spawn_rate': 2.0,
                'aggression': 1.8,
                'special': 'Untote erwachen nachts',
                'description': 'Die Toten erheben sich aus ihren Gräbern!'
            }
        }
        
        return effects.get(monster_type, {
            'spawn_rate': 1.0,
            'aggression': 1.0,
            'special': 'Keine besonderen Effekte',
            'description': 'Standard-Herrschaft'
        })
    
    def get_hierarchy_display(self) -> str:
        """Zeige aktuelle Arena-Hierarchie"""
        display = "🏛️ ARENA HIERARCHIE\n"
        display += "=" * 40 + "\n\n"
        
        # Arena König
        if self.hierarchy['arena_king']:
            king = self.monsters.get(self.hierarchy['arena_king'])
            if king:
                display += f"👑 ARENA-KÖNIG: {king.name} {king.title}\n"
                display += f"   Kills: {king.kills} | Level: {king.level}\n\n"
        else:
            display += "👑 ARENA-KÖNIG: [VAKANT]\n\n"
        
        # Gebietsherrscher
        display += "🏰 GEBIETSHERRSCHER:\n"
        for region, ruler_id in self.hierarchy['region_lords'].items():
            if ruler_id:
                ruler = self.monsters.get(ruler_id)
                if ruler:
                    display += f"  {region}: {ruler.name} (Lvl {ruler.level})\n"
            else:
                display += f"  {region}: [Frei]\n"
        
        display += "\n"
        
        # Top Champions
        champions = sorted(
            [m for m in self.monsters.values() if m.rank == RulerRank.CHAMPION],
            key=lambda x: x.kills,
            reverse=True
        )[:5]
        
        if champions:
            display += "⚔️ TOP CHAMPIONS:\n"
            for i, champ in enumerate(champions, 1):
                display += f"  {i}. {champ.name} - {champ.kills} Kills\n"
        
        return display
    
    def get_monster_profile(self, monster_id: str) -> Dict:
        """Hole detailliertes Monster-Profil"""
        if monster_id not in self.monsters:
            return None
        
        monster = self.monsters[monster_id]
        
        return {
            'basic': {
                'name': f"{monster.name} {monster.title}",
                'type': monster.type.value,
                'level': monster.level,
                'rank': monster.rank.value
            },
            'stats': {
                'hp': f"{monster.hp}/{monster.max_hp}",
                'attack': monster.attack,
                'defense': monster.defense,
                'speed': monster.speed
            },
            'record': {
                'kills': monster.kills,
                'deaths': monster.deaths,
                'grudges': len(monster.grudges),
                'nemesis_of': monster.grudges
            },
            'personality': {
                'traits': monster.personality_traits,
                'scars': monster.battle_scars,
                'moves': monster.special_moves,
                'weaknesses': monster.weaknesses
            }
        }
    
    def simulate_monster_battles(self) -> List[Dict]:
        """Simuliere Kämpfe zwischen Monstern (für Dynamik)"""
        events = []
        
        # 20% Chance für Monster vs Monster
        if random.random() < 0.2:
            fighters = random.sample(list(self.monsters.values()), min(2, len(self.monsters)))
            if len(fighters) == 2:
                m1, m2 = fighters
                
                # Simplee Kampf-Simulation
                m1_power = m1.attack + m1.level * 2 + random.randint(0, 20)
                m2_power = m2.attack + m2.level * 2 + random.randint(0, 20)
                
                if m1_power > m2_power:
                    winner, loser = m1, m2
                else:
                    winner, loser = m2, m1
                
                # Update Stats
                winner.kills += 1
                winner.level += 1
                loser.deaths += 1
                
                events.append({
                    'type': 'monster_duel',
                    'winner': winner.name,
                    'loser': loser.name,
                    'location': random.choice(self.regions),
                    'message': f"{winner.name} besiegt {loser.name} im Kampf!"
                })
        
        return events
    
    def save_state(self, filepath: str):
        """Speichere Arena-Zustand"""
        state = {
            'monsters': {mid: m.to_dict() for mid, m in self.monsters.items()},
            'hierarchy': self.hierarchy,
            'timestamp': time.time()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def load_state(self, filepath: str):
        """Lade Arena-Zustand"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # Rekonstruiere Monster
            self.monsters = {}
            for mid, mdata in state['monsters'].items():
                monster = NemesisMonster(
                    id=mdata['id'],
                    name=mdata['name'],
                    title=mdata['title'],
                    type=MonsterType(mdata['type']),
                    level=mdata['level']
                )
                # Restore all attributes
                for key, value in mdata.items():
                    if hasattr(monster, key):
                        setattr(monster, key, value)
                
                self.monsters[mid] = monster
            
            self.hierarchy = state['hierarchy']
            
            return True
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
            return False


# ============================================
# DIGIVICE INTEGRATION MODULE
# ============================================

class DigiviceArenaModule:
    """Integration des Arena-Systems ins Digivice"""
    
    def __init__(self, arena_manager: ArenaManager):
        self.arena = arena_manager
        self.current_battle = None
        self.player_stats = {
            'name': 'Kuja',
            'level': 1,
            'wins': 0,
            'losses': 0,
            'titles': [],
            'nemesis_list': []
        }
    
    def register_api_endpoints(self, server):
        """Registriere API-Endpoints für das Frontend"""
        
        # Arena Status
        server.add_endpoint('/api/arena/status', self.get_arena_status, ['GET'])
        
        # Monster Liste
        server.add_endpoint('/api/arena/monsters', self.get_monster_list, ['GET'])
        
        # Kampf starten
        server.add_endpoint('/api/arena/challenge', self.start_challenge, ['POST'])
        
        # Kampf-Aktion
        server.add_endpoint('/api/arena/battle/action', self.battle_action, ['POST'])
        
        # Hierarchie
        server.add_endpoint('/api/arena/hierarchy', self.get_hierarchy, ['GET'])
        
        # Monster-Profil
        server.add_endpoint('/api/arena/monster/<id>', self.get_monster_profile, ['GET'])
    
    def get_arena_status(self) -> Dict:
        """Arena-Status für Frontend"""
        return {
            'open': True,
            'total_monsters': len(self.arena.monsters),
            'player_rank': self._calculate_player_rank(),
            'current_king': self.arena.hierarchy.get('arena_king'),
            'events': self.arena.simulate_monster_battles()
        }
    
    def get_monster_list(self) -> List[Dict]:
        """Liste aller Monster für Frontend"""
        monsters = []
        for monster in self.arena.monsters.values():
            monsters.append({
                'id': monster.id,
                'name': f"{monster.name} {monster.title}",
                'level': monster.level,
                'rank': monster.rank.value,
                'type': monster.type.value,
                'kills': monster.kills,
                'has_grudge': self.player_stats['name'] in monster.grudges
            })
        
        return sorted(monsters, key=lambda x: x['kills'], reverse=True)
    
    def start_challenge(self, data: Dict) -> Dict:
        """Starte Arena-Kampf"""
        monster_id = data.get('monster_id')
        
        if monster_id:
            # Spezifisches Monster herausfordern
            monster = self.arena.monsters.get(monster_id)
        else:
            # Zufälliges Monster basierend auf Level
            monster = self.arena.get_arena_challenger(self.player_stats['level'])
        
        if not monster:
            return {'error': 'Kein Gegner verfügbar'}
        
        # Check für Grudge
        has_grudge = self.player_stats['name'] in monster.grudges
        
        self.current_battle = {
            'monster': monster,
            'turn': 0,
            'player_hp': 100,
            'monster_hp': monster.hp,
            'log': [],
            'stakes': data.get('stakes', 'ranking')  # ranking, items, title
        }
        
        # Erste Nachricht
        intro = monster.generate_taunt(self.player_stats['name'])
        if has_grudge:
            intro = f"🔥 RACHE-KAMPF! 🔥\n{intro}"
        
        return {
            'battle_started': True,
            'monster': self.arena.get_monster_profile(monster.id),
            'intro_message': intro,
            'has_grudge': has_grudge,
            'special_rules': self._get_battle_rules(monster)
        }
    
    def battle_action(self, data: Dict) -> Dict:
        """Führe Kampf-Aktion aus"""
        if not self.current_battle:
            return {'error': 'Kein aktiver Kampf'}
        
        action = data.get('action')  # attack, skill, dodge, parry
        
        # Spieler-Aktion
        player_damage = self._calculate_damage(action, self.current_battle['monster'])
        self.current_battle['monster_hp'] -= player_damage
        
        # Monster-Reaktion
        monster_action = self._ai_choose_action(self.current_battle['monster'])
        monster_damage = self._calculate_monster_damage(monster_action)
        self.current_battle['player_hp'] -= monster_damage
        
        # Log
        self.current_battle['log'].append({
            'turn': self.current_battle['turn'],
            'player_action': action,
            'player_damage': player_damage,
            'monster_action': monster_action,
            'monster_damage': monster_damage
        })
        
        # Check für Kampf-Ende
        if self.current_battle['monster_hp'] <= 0:
            # Spieler gewinnt
            result = self.arena.process_battle_result(
                self.current_battle['monster'].id,
                self.player_stats['name'],
                player_won=True,
                battle_data=self.current_battle
            )
            
            self.player_stats['wins'] += 1
            
            return {
                'battle_over': True,
                'winner': 'player',
                'result': result,
                'rewards': result.get('loot')
            }
        
        elif self.current_battle['player_hp'] <= 0:
            # Monster gewinnt
            result = self.arena.process_battle_result(
                self.current_battle['monster'].id,
                self.player_stats['name'],
                player_won=False,
                battle_data=self.current_battle
            )
            
            self.player_stats['losses'] += 1
            
            # Monster in Nemesis-Liste
            if self.current_battle['monster'].id not in self.player_stats['nemesis_list']:
                self.player_stats['nemesis_list'].append(self.current_battle['monster'].id)
            
            return {
                'battle_over': True,
                'winner': 'monster',
                'result': result,
                'consequences': self._get_death_consequences()
            }
        
        self.current_battle['turn'] += 1
        
        return {
            'battle_continues': True,
            'player_hp': self.current_battle['player_hp'],
            'monster_hp': self.current_battle['monster_hp'],
            'last_exchange': self.current_battle['log'][-1]
        }
    
    def get_hierarchy(self) -> str:
        """Hole Hierarchie-Anzeige"""
        return self.arena.get_hierarchy_display()
    
    def get_monster_profile(self, monster_id: str) -> Dict:
        """Hole Monster-Profil"""
        return self.arena.get_monster_profile(monster_id)
    
    def _calculate_damage(self, action: str, monster: NemesisMonster) -> int:
        """Berechne Schaden basierend auf Skill > Gear"""
        base_damage = 10
        
        # Skill-Multiplikatoren (WICHTIGER als Gear!)
        skill_multipliers = {
            'perfect_dodge_counter': 3.0,
            'combo_5hit': 2.5,
            'parry_riposte': 2.0,
            'charged_attack': 1.8,
            'normal_attack': 1.0
        }
        
        multiplier = skill_multipliers.get(action, 1.0)
        
        # Check für Monster-Schwächen
        if any(w in monster.weaknesses for w in ['Angst vor Combos', 'Schwach gegen Timing']):
            multiplier *= 1.5
        
        # Zufälligkeit (Glück)
        luck = random.uniform(0.8, 1.2)
        
        return int(base_damage * multiplier * luck)
    
    def _calculate_monster_damage(self, action: str) -> int:
        """Berechne Monster-Schaden"""
        monster = self.current_battle['monster']
        base_damage = monster.attack
        
        # Spezial-Moves
        if action in monster.special_moves:
            base_damage *= 1.5
        
        # Wut-Bonus (wenn Grudge)
        if self.player_stats['name'] in monster.grudges:
            base_damage *= 1.3
        
        return int(base_damage * random.uniform(0.8, 1.2))
    
    def _ai_choose_action(self, monster: NemesisMonster) -> str:
        """KI wählt Aktion basierend auf Persönlichkeit"""
        
        # Persönlichkeits-basierte Entscheidung
        if "Berserker" in monster.personality_traits:
            # Immer angreifen
            return random.choice(monster.special_moves + ["attack"])
        
        elif "Vorsichtig" in monster.personality_traits:
            # Defensiver
            if self.current_battle['monster_hp'] < monster.max_hp * 0.3:
                return "defend"
            return "attack"
        
        elif "Hinterhältig" in monster.personality_traits:
            # Trickreich
            if random.random() < 0.3:
                return "feint"
            return random.choice(monster.special_moves)
        
        # Standard
        return random.choice(["attack"] + monster.special_moves)
    
    def _get_battle_rules(self, monster: NemesisMonster) -> List[str]:
        """Spezielle Kampf-Regeln basierend auf Monster"""
        rules = []
        
        if monster.rank == RulerRank.ARENA_KING:
            rules.append("👑 Königskampf: Keine Heilung erlaubt!")
        
        if self.player_stats['name'] in monster.grudges:
            rules.append("🔥 Rache-Kampf: Monster hat +30% Schaden!")
        
        if len(monster.battle_scars) > 3:
            rules.append("🗡️ Kampf-Veteran: Monster kennt deine Moves!")
        
        return rules
    
    def _get_death_consequences(self) -> Dict:
        """Konsequenzen bei Niederlage"""
        consequences = {
            'reputation_loss': -10,
            'gold_loss': self.player_stats.get('gold', 0) // 10
        }
        
        # Bei Stakes = "items"
        if self.current_battle.get('stakes') == 'items':
            consequences['item_loss'] = "1 zufälliges Item verloren"
        
        # Bei Stakes = "title"
        if self.current_battle.get('stakes') == 'title':
            consequences['title_loss'] = "Titel verloren"
        
        return consequences
    
    def _calculate_player_rank(self) -> str:
        """Berechne Spieler-Rang"""
        wins = self.player_stats['wins']
        
        if wins >= 100:
            return "Legendärer Gladiator"
        elif wins >= 50:
            return "Arena-Meister"
        elif wins >= 25:
            return "Champion"
        elif wins >= 10:
            return "Gladiator"
        elif wins >= 5:
            return "Kämpfer"
        else:
            return "Neuling"


# ============================================
# BEISPIEL INTEGRATION
# ============================================

if __name__ == "__main__":
    # Erstelle Arena
    arena = ArenaManager()
    
    # Erstelle Digivice-Modul
    digivice = DigiviceArenaModule(arena)
    
    # Zeige Hierarchie
    print(arena.get_hierarchy_display())
    
    # Simuliere Kampf
    print("\n🎮 KAMPF-SIMULATION")
    print("-" * 40)
    
    # Finde Gegner
    monster = arena.get_arena_challenger(player_level=5)
    if monster:
        print(f"Gegner: {monster.name} {monster.title}")
        print(f"Level: {monster.level} | Rang: {monster.rank.value}")
        print(f"Persönlichkeit: {', '.join(monster.personality_traits)}")
        print(f"\nTaunt: {monster.generate_taunt('Kuja')}")
        
        # Simuliere Spieler-Sieg
        result = arena.process_battle_result(
            monster.id,
            'Kuja',
            player_won=True,
            battle_data={}
        )
        
        print(f"\n📊 KAMPF-ERGEBNIS:")
        print(f"Loot: {result['loot']}")
        if result.get('nemesis_event'):
            print(f"Event: {result['nemesis_event']['message']}")
    
    # Speichere Zustand
    arena.save_state('arena_state.json')
    print("\n💾 Arena-Zustand gespeichert!")
    
    # Monster-Events
    events = arena.simulate_monster_battles()
    if events:
        print("\n🎭 MONSTER-EVENTS:")
        for event in events:
            print(f"- {event['message']}")
