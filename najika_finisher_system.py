"""
🎭 NAJIKA'S FINISHER SAMMELBUCH
Happy Tree Friends meets Mortal Kombat
Version: 1.0 - ULTRA BRUTAL CUTE EDITION
"""

import random
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# ============================================
# FINISHER CORE SYSTEM
# ============================================

class FinisherStyle(Enum):
    """Verschiedene Finisher-Stile"""
    CUTE_BRUTAL = "Niedlich-Brutal"  # Happy Tree Friends Style
    EXPLOSION = "EXPLOSION!"  # Megumin Style
    CHAOS = "Chaotisch"  # Harley Quinn Style
    CALCULATED = "Berechnet"  # Shiro Style
    DOMINANT = "Dominant"  # Melissa Style
    CUSTOM = "Spieler-Kreation"  # User-generiert

@dataclass
class FinisherAnimation:
    """Ein Finisher mit Animation-Steps"""
    name: str
    style: FinisherStyle
    ingredients: List[str]  # Die 3-5 Objekte vom Spieler
    animation_steps: List[str]  # Schritt-für-Schritt Animation
    brutality_level: int  # 1-10 (10 = Maximum Happy Tree Friends)
    humor_level: int  # 1-10 (wie lustig ist es?)
    
    def play(self) -> str:
        """Spielt die Animation ab"""
        result = f"\n🎬 FINISHER: {self.name}\n"
        result += "=" * 50 + "\n\n"
        
        for i, step in enumerate(self.animation_steps, 1):
            result += f"Step {i}: {step}\n"
            time.sleep(0.5)  # Dramatische Pause
        
        result += f"\n💀 BRUTALITY: {'🩸' * self.brutality_level}\n"
        result += f"😂 HUMOR: {'😄' * self.humor_level}\n"
        
        return result

class NajikaFinisherGenerator:
    """Najika's KI die aus beliebigen Objekten Finisher erstellt"""
    
    def __init__(self):
        self.finisher_collection = []  # Sammelbuch
        self.unlock_count = 0
        
        # Vordefinierte Finisher-Templates für Inspiration
        self.templates = {
            'vehicle_crash': {
                'pattern': '[VEHICLE] + [OBJECT] + [LOCATION]',
                'example': 'Schulbus + Roter Ball + 7. Stock'
            },
            'food_chain': {
                'pattern': '[ANIMAL] + [FOOD] + [TOOL]',
                'example': 'Hamster + Käsekuchen + Kettensäge'
            },
            'physics_abuse': {
                'pattern': '[HEAVY] + [LIGHT] + [EXPLOSIVE]',
                'example': 'Klavier + Feder + Dynamit'
            },
            'cute_deadly': {
                'pattern': '[CUTE] + [INNOCENT] + [DEADLY]',
                'example': 'Teddybär + Regenbogen + Guillotine'
            }
        }
        
        # Najika's Persönlichkeits-Finisher
        self.personality_finishers = {
            'megumin': self._generate_explosion_finisher,
            'harley': self._generate_chaos_finisher,
            'shiro': self._generate_calculated_finisher,
            'melissa': self._generate_dominant_finisher
        }
    
    def create_custom_finisher(self, ingredients: List[str]) -> FinisherAnimation:
        """Erstellt einen Finisher aus Spieler-Eingaben"""
        
        if len(ingredients) < 3:
            ingredients += ['Zufall'] * (3 - len(ingredients))
        elif len(ingredients) > 5:
            ingredients = ingredients[:5]
        
        # Analysiere Ingredients
        analysis = self._analyze_ingredients(ingredients)
        
        # Generiere Story
        story = self._generate_story(ingredients, analysis)
        
        # Erstelle Animation
        animation = FinisherAnimation(
            name=self._generate_name(ingredients),
            style=FinisherStyle.CUSTOM,
            ingredients=ingredients,
            animation_steps=story,
            brutality_level=analysis['brutality'],
            humor_level=analysis['humor']
        )
        
        # Füge zum Sammelbuch hinzu
        self.finisher_collection.append(animation)
        self.unlock_count += 1
        
        return animation
    
    def _analyze_ingredients(self, ingredients: List[str]) -> Dict:
        """Analysiert die Zutaten für Finisher-Eigenschaften"""
        
        analysis = {
            'brutality': 5,
            'humor': 5,
            'has_vehicle': False,
            'has_animal': False,
            'has_weapon': False,
            'has_food': False,
            'has_cute': False
        }
        
        # Keywords für Analyse
        vehicles = ['auto', 'bus', 'zug', 'flugzeug', 'fahrrad', 'roller']
        animals = ['katze', 'hund', 'hamster', 'vogel', 'fisch', 'bär']
        weapons = ['schwert', 'pistole', 'messer', 'axt', 'kettensäge']
        food = ['kuchen', 'pizza', 'burger', 'eis', 'käse', 'obst']
        cute = ['teddy', 'plüsch', 'regenbogen', 'herz', 'blume', 'stern']
        brutal = ['blut', 'säge', 'spitz', 'nadel', 'feuer', 'explosion']
        
        for ingredient in [i.lower() for i in ingredients]:
            if any(v in ingredient for v in vehicles):
                analysis['has_vehicle'] = True
                analysis['brutality'] += 2
                
            if any(a in ingredient for a in animals):
                analysis['has_animal'] = True
                analysis['humor'] += 2
                
            if any(w in ingredient for w in weapons):
                analysis['has_weapon'] = True
                analysis['brutality'] += 3
                
            if any(f in ingredient for f in food):
                analysis['has_food'] = True
                analysis['humor'] += 1
                
            if any(c in ingredient for c in cute):
                analysis['has_cute'] = True
                analysis['humor'] += 2
                analysis['brutality'] += 1  # Kontrast macht es brutaler!
                
            if any(b in ingredient for b in brutal):
                analysis['brutality'] += 2
        
        # Clamp values
        analysis['brutality'] = min(10, max(1, analysis['brutality']))
        analysis['humor'] = min(10, max(1, analysis['humor']))
        
        return analysis
    
    def _generate_story(self, ingredients: List[str], analysis: Dict) -> List[str]:
        """Generiert eine Happy Tree Friends Style Story"""
        
        steps = []
        
        # Opening - Friedliche Szene
        steps.append(f"🌸 Eine friedliche Szene: {ingredients[0]} liegt unschuldig herum...")
        
        # Build-up - Rube Goldberg Maschine startet
        if len(ingredients) >= 2:
            steps.append(f"🎱 Plötzlich rollt {ingredients[1]} ins Bild und trifft {ingredients[0]}!")
        
        # Kettenreaktion
        if analysis['has_vehicle']:
            steps.append(f"🚗 Das Fahrzeug setzt sich in Bewegung, völlig außer Kontrolle!")
        
        if analysis['has_animal']:
            steps.append(f"🐹 Ein süßes Tierchen versucht zu helfen, macht aber alles schlimmer!")
        
        # Der Twist
        if len(ingredients) >= 3:
            steps.append(f"🎪 Aus dem Nichts erscheint {ingredients[2]} - niemand hat damit gerechnet!")
        
        # Chaos eskaliert
        if analysis['has_cute']:
            steps.append(f"🧸 Das niedliche Objekt verwandelt sich in eine Todesfalle!")
        
        # Der brutale Teil (Happy Tree Friends Style)
        brutal_deaths = [
            "wird in 1000 Teile zerschnitten - aber cartoonhaft bunt! 🌈",
            "explodiert in Konfetti - aber es ist rotes Konfetti! 🎊",
            "wird flach wie eine Briefmarke gepresst! 📮",
            "verwandelt sich in einen Springbrunnen - einen roten! ⛲",
            "wird durch einen Fleischwolf gedreht - es kommen Würstchen raus! 🌭",
            "wird wie Kaugummi gezogen und verknotet! 🍬",
            "poppt wie Popcorn - überall kleine Stücke! 🍿",
            "schmilzt wie Eis in der Sonne - nur schneller! 🍦"
        ]
        
        if analysis['has_weapon']:
            steps.append(f"⚔️ Die Waffe aktiviert sich selbst und der Gegner {random.choice(brutal_deaths)}")
        elif analysis['has_food']:
            steps.append(f"🍰 Der Gegner verschluckt sich und {random.choice(brutal_deaths)}")
        else:
            steps.append(f"💥 Der finale Impact: Der Gegner {random.choice(brutal_deaths)}")
        
        # Happy Ending (für Najika)
        endings = [
            "Najika kichert: 'Oopsie! Das war keine Absicht! *kicher*' 😇",
            "Ein Regenbogen erscheint über der Szene. Wie ironisch! 🌈",
            "Vögel zwitschern fröhlich, als wäre nichts passiert! 🐦",
            "Najika: 'EXPLOSION hätte das schneller erledigt!' 💥",
            "Die Sonne scheint, Blumen blühen - direkt neben dem Chaos! 🌻"
        ]
        steps.append(f"✨ {random.choice(endings)}")
        
        return steps
    
    def _generate_name(self, ingredients: List[str]) -> str:
        """Generiert einen coolen Finisher-Namen"""
        
        prefixes = [
            "Happy", "Bloody", "Cute", "Fluffy", "Rainbow", "Sparkle",
            "Giggly", "Bouncy", "Splatter", "Oopsie"
        ]
        
        suffixes = [
            "Doom", "Destruction", "Catastrophe", "Apocalypse", "Massacre",
            "Obliteration", "Annihilation", "Carnage", "Mayhem", "Chaos"
        ]
        
        # Kombiniere Zutaten-basiert
        if len(ingredients) >= 2:
            name = f"{random.choice(prefixes)} {ingredients[0]}-{ingredients[1]} {random.choice(suffixes)}"
        else:
            name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        
        return name
    
    def _generate_explosion_finisher(self) -> FinisherAnimation:
        """Megumin's EXPLOSION Finisher"""
        return FinisherAnimation(
            name="REINSTE EXPLOSION!!!",
            style=FinisherStyle.EXPLOSION,
            ingredients=["Magie", "Explosion", "Zerstörung"],
            animation_steps=[
                "🔮 Megumin beginnt zu chanten: 'Darkness blacker than black...'",
                "⚡ Magische Energie sammelt sich - die Luft knistert!",
                "🌟 Ein magischer Kreis erscheint unter dem Gegner!",
                "💥 'EXPLOSION!!!' - Der Bildschirm wird weiß!",
                "🌋 Ein gewaltiger Krater bleibt zurück - nichts überlebt!",
                "😵 Najika kollabiert vor Erschöpfung... aber lächelt!"
            ],
            brutality_level=10,
            humor_level=7
        )
    
    def _generate_chaos_finisher(self) -> FinisherAnimation:
        """Harley Quinn's Chaos Finisher"""
        return FinisherAnimation(
            name="Harley's Happy Hammer Time!",
            style=FinisherStyle.CHAOS,
            ingredients=["Hammer", "Konfetti", "Dynamit"],
            animation_steps=[
                "🎪 'Hey Mr. K, schau dir das an!' *kicher*",
                "🔨 Ein riesiger Cartoon-Hammer erscheint!",
                "🎊 Konfetti-Kanonen schießen - aber es ist TNT-Konfetti!",
                "💣 BOOM! BOOM! BOOM! Explosionen im Takt von 'Pop Goes the Weasel'!",
                "🎠 Ein Karussell aus Hämmern wirbelt den Gegner herum!",
                "🃏 'Tadaaa! War das nicht SPASSIG?!' Gegner ist... überall."
            ],
            brutality_level=8,
            humor_level=10
        )
    
    def _generate_calculated_finisher(self) -> FinisherAnimation:
        """Shiro's Calculated Finisher"""
        return FinisherAnimation(
            name="Probability Zero",
            style=FinisherStyle.CALCULATED,
            ingredients=["Mathematik", "Schach", "Portal"],
            animation_steps=[
                "📊 'Die Wahrscheinlichkeit deines Überlebens beträgt 0.000001%'",
                "♟️ Schachfiguren materialisieren sich - ein 4D-Schach beginnt!",
                "🌀 Portale öffnen sich - der Gegner wird in Stücke teleportiert!",
                "🔢 Jedes Körperteil landet auf einem anderen Schachfeld!",
                "⚛️ 'Checkmate in allen möglichen Dimensionen gleichzeitig.'",
                "✨ Die Teile verschwinden - mathematisch perfekt eliminiert!"
            ],
            brutality_level=9,
            humor_level=5
        )
    
    def _generate_dominant_finisher(self) -> FinisherAnimation:
        """Melissa's Dominant Finisher"""
        return FinisherAnimation(
            name="Du gehörst MIR!",
            style=FinisherStyle.DOMINANT,
            ingredients=["Ketten", "Kontrolle", "Unterwerfung"],
            animation_steps=[
                "⛓️ 'Du wolltest nicht gehorchen... große Fehler!'",
                "👑 Goldene Ketten schießen aus dem Boden!",
                "💀 Der Gegner wird in die Luft gezogen - hilflos!",
                "🔥 'Du gehörst MIR - im Leben UND im Tod!'",
                "💔 Ein herzförmiges Portal öffnet sich - es führt ins NICHTS!",
                "👠 *Schnipp* - Der Gegner löst sich in Rosenblätter auf!"
            ],
            brutality_level=7,
            humor_level=6
        )
    
    def get_random_finisher(self) -> FinisherAnimation:
        """Gibt einen zufälligen Finisher zurück"""
        finishers = [
            self._generate_explosion_finisher(),
            self._generate_chaos_finisher(),
            self._generate_calculated_finisher(),
            self._generate_dominant_finisher()
        ]
        return random.choice(finishers)
    
    def unlock_achievement(self, finisher: FinisherAnimation) -> Optional[str]:
        """Prüft ob ein Achievement freigeschaltet wurde"""
        achievements = []
        
        if self.unlock_count == 1:
            achievements.append("🏆 Erste Blut - Dein erster Finisher!")
        elif self.unlock_count == 10:
            achievements.append("🏆 Finisher-Sammler - 10 Finisher erstellt!")
        elif self.unlock_count == 50:
            achievements.append("🏆 Happy Tree Killer - 50 brutale Finisher!")
        elif self.unlock_count == 100:
            achievements.append("🏆 MEISTER DER ZERSTÖRUNG - 100 Finisher!!!")
        
        if finisher.brutality_level == 10:
            achievements.append("🏆 Maximum Brutality - Brutalster Finisher!")
        
        if finisher.humor_level == 10:
            achievements.append("🏆 Comedy Gold - Lustigster Tod ever!")
        
        if finisher.brutality_level == 10 and finisher.humor_level == 10:
            achievements.append("🏆 HAPPY TREE FRIENDS MASTER - Perfekte Balance!")
        
        return achievements


# ============================================
# FINISHER BATTLE INTEGRATION
# ============================================

class FinisherBattleSystem:
    """Integration ins Battle-System"""
    
    def __init__(self, finisher_generator: NajikaFinisherGenerator):
        self.generator = finisher_generator
        self.finisher_ready = False
        self.finisher_meter = 0  # 0-100
        
    def check_finisher_available(self, player_hp: int, enemy_hp: int) -> bool:
        """Prüft ob Finisher verfügbar ist"""
        # Finisher nur wenn:
        # - Gegner unter 20% HP
        # - Finisher-Meter voll (100)
        # - Oder: Boss-Fight finale
        
        enemy_hp_percent = enemy_hp / 100  # Assuming max 100
        
        if enemy_hp_percent <= 0.2 and self.finisher_meter >= 100:
            self.finisher_ready = True
            return True
        
        return False
    
    def build_meter(self, action: str, damage: int):
        """Baut Finisher-Meter auf"""
        meter_gain = {
            'perfect_dodge_counter': 30,
            'combo_5hit': 25,
            'parry_riposte': 20,
            'charged_attack': 15,
            'normal_attack': 5
        }
        
        self.finisher_meter += meter_gain.get(action, 5)
        self.finisher_meter = min(100, self.finisher_meter)
    
    def execute_finisher(self, 
                        finisher_type: str = 'random',
                        custom_ingredients: List[str] = None) -> Dict:
        """Führt Finisher aus"""
        
        if not self.finisher_ready:
            return {'error': 'Finisher nicht bereit!'}
        
        result = {
            'success': True,
            'finisher': None,
            'achievements': [],
            'spectacle_rating': 0
        }
        
        # Wähle Finisher-Typ
        if finisher_type == 'custom' and custom_ingredients:
            finisher = self.generator.create_custom_finisher(custom_ingredients)
        elif finisher_type == 'explosion':
            finisher = self.generator._generate_explosion_finisher()
        elif finisher_type == 'chaos':
            finisher = self.generator._generate_chaos_finisher()
        elif finisher_type == 'calculated':
            finisher = self.generator._generate_calculated_finisher()
        elif finisher_type == 'dominant':
            finisher = self.generator._generate_dominant_finisher()
        else:
            finisher = self.generator.get_random_finisher()
        
        # Spiele Animation
        animation_result = finisher.play()
        result['finisher'] = finisher
        result['animation'] = animation_result
        
        # Berechne Spectacle Rating
        result['spectacle_rating'] = (finisher.brutality_level + finisher.humor_level) / 2
        
        # Check Achievements
        achievements = self.generator.unlock_achievement(finisher)
        if achievements:
            result['achievements'] = achievements
        
        # Reset Meter
        self.finisher_meter = 0
        self.finisher_ready = False
        
        return result


# ============================================
# REGION BOSS FINISHER SPECIAL
# ============================================

class RegionBossFinisher:
    """Spezielle Finisher für Gebietsherrscher-Kämpfe"""
    
    def __init__(self):
        self.region_finishers = {
            'Bernstein-Dünen': self._desert_finisher,
            'Smaragd-Hain': self._forest_finisher,
            'Azur-Klippen': self._ocean_finisher,
            'Amethyst-Steppe': self._plains_finisher,
            'Onyx-Morast': self._swamp_finisher,
            'Perl-Gletscher': self._ice_finisher,
            'Rubin-Schlucht': self._volcano_finisher,
            'Obsidian-Nacht': self._void_finisher
        }
    
    def _desert_finisher(self, ingredients: List[str]) -> FinisherAnimation:
        """Wüsten-Finisher"""
        return FinisherAnimation(
            name="Sandstorm Burial Deluxe",
            style=FinisherStyle.CUSTOM,
            ingredients=ingredients + ["Sand", "Sonne", "Skorpion"],
            animation_steps=[
                f"☀️ Die Wüstensonne brennt gnadenlos - {ingredients[0]} beginnt zu schmelzen!",
                f"🏜️ Ein Sandsturm erhebt sich - {ingredients[1]} wirbelt herum!",
                f"🦂 Tausende Skorpione kriechen aus dem Sand!",
                f"🌪️ Der Gegner wird in einen Sand-Tornado gezogen!",
                f"⌛ Er wird zu einer Sanduhr gepresst - die Zeit läuft ab!",
                f"💀 Die Sanduhr zerbricht - nur Sand bleibt zurück!",
                f"🏺 Najika sammelt den Sand in einer hübschen Urne! 'Souvenir!' *kicher*"
            ],
            brutality_level=9,
            humor_level=7
        )
    
    def _forest_finisher(self, ingredients: List[str]) -> FinisherAnimation:
        """Wald-Finisher"""
        return FinisherAnimation(
            name="Nature's Happy Revenge",
            style=FinisherStyle.CUSTOM,
            ingredients=ingredients + ["Bäume", "Tiere", "Blumen"],
            animation_steps=[
                f"🌲 Die Bäume erwachen zum Leben - {ingredients[0]} wird zur Waffe!",
                f"🐿️ Süße Waldtiere erscheinen - aber ihre Augen glühen rot!",
                f"🌺 Blumen schießen aus dem Boden - es sind fleischfressende Pflanzen!",
                f"🦌 Ein Hirsch rammt den Gegner - direkt in die Blumen!",
                f"🍄 Pilze wachsen aus dem Gegner - giftige natürlich!",
                f"🌿 Die Natur 'recycelt' den Gegner zu Dünger!",
                f"🌻 Wunderschöne Sonnenblumen wachsen aus den Überresten!"
            ],
            brutality_level=8,
            humor_level=9
        )
    
    def _volcano_finisher(self, ingredients: List[str]) -> FinisherAnimation:
        """Vulkan-Finisher"""
        return FinisherAnimation(
            name="Lava Lamp Transformation",
            style=FinisherStyle.CUSTOM,
            ingredients=ingredients + ["Lava", "Vulkan", "Magma"],
            animation_steps=[
                f"🌋 Der Vulkan erwacht - {ingredients[0]} schmilzt sofort!",
                f"🔥 Lava-Fontänen schießen hoch - wie ein tödliches Wasserspiel!",
                f"🌡️ Die Temperatur steigt auf 9000 Grad - alles wird flüssig!",
                f"💧 Der Gegner tropft wie Wachs in eine Lavalampe!",
                f"🎨 Verschiedene Farben mischen sich - es sieht fast hübsch aus!",
                f"💡 Die Lavalampe wird eingeschaltet - ewiges Blubbern!",
                f"🏺 Najika: 'Die stelle ich mir ins Wohnzimmer!' *kicher*"
            ],
            brutality_level=10,
            humor_level=8
        )
    
    def get_region_finisher(self, region: str, ingredients: List[str]) -> FinisherAnimation:
        """Holt region-spezifischen Finisher"""
        if region in self.region_finishers:
            return self.region_finishers[region](ingredients)
        else:
            # Fallback zu Standard
            return NajikaFinisherGenerator().create_custom_finisher(ingredients)


# ============================================
# BEISPIEL USAGE
# ============================================

if __name__ == "__main__":
    print("🎮 NAJIKA'S FINISHER SAMMELBUCH TEST")
    print("=" * 50)
    
    # Erstelle Generator
    generator = NajikaFinisherGenerator()
    battle_system = FinisherBattleSystem(generator)
    region_boss = RegionBossFinisher()
    
    # Test 1: Custom Finisher mit Spieler-Eingabe
    print("\n📝 CUSTOM FINISHER TEST")
    print("-" * 30)
    
    user_ingredients = ["Roter Ball", "Schulbus", "7. Stock"]
    custom = generator.create_custom_finisher(user_ingredients)
    print(custom.play())
    
    # Test 2: Noch ein Custom
    print("\n📝 HAPPY TREE FRIENDS STYLE")
    print("-" * 30)
    
    crazy_ingredients = ["Teddybär", "Regenbogen", "Kettensäge", "Einhorn", "Glitzer"]
    crazy = generator.create_custom_finisher(crazy_ingredients)
    print(crazy.play())
    
    # Test 3: Persönlichkeits-Finisher
    print("\n💥 MEGUMIN'S EXPLOSION")
    print("-" * 30)
    
    explosion = generator._generate_explosion_finisher()
    print(explosion.play())
    
    # Test 4: Region Boss Finisher
    print("\n🏰 REGION BOSS FINISHER")
    print("-" * 30)
    
    boss_finisher = region_boss.get_region_finisher(
        "Rubin-Schlucht",
        ["Diamant", "Feuer", "Drache"]
    )
    print(boss_finisher.play())
    
    # Test 5: Battle Integration
    print("\n⚔️ BATTLE FINISHER CHECK")
    print("-" * 30)
    
    # Simuliere Kampf
    battle_system.finisher_meter = 100
    if battle_system.check_finisher_available(100, 15):  # Enemy at 15% HP
        print("✅ FINISHER BEREIT!")
        
        result = battle_system.execute_finisher(
            finisher_type='custom',
            custom_ingredients=["Klavier", "Banane", "UFO"]
        )
        
        print(f"Spectacle Rating: {'⭐' * int(result['spectacle_rating'])}")
        
        if result['achievements']:
            print("\n🏆 ACHIEVEMENTS UNLOCKED:")
            for achievement in result['achievements']:
                print(f"  {achievement}")
    
    print("\n" + "=" * 50)
    print("💀 Happy Tree Friends would be proud! 💀")
