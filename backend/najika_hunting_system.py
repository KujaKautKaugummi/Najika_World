"""
NAJIKA HUNTING & HARVESTING SYSTEM
===================================
Inspiriert von:
- Red Dead Redemption 2 (Jagd-Qualität, Häuten, Trophäen)
- Monster Hunter (Carving, Materialien pro Körperteil)
- Digimon World (Monster SIND die Tiere der Welt)

WICHTIG:
- Es gibt KEINE getrennten "Tiere" und "Monster"!
- Monster = die Fauna dieser Fantasy-Welt
- Ein "Bär" bei uns ist ein MONSTER-Bär, kein normales Tier
- ALLES ist jagdbar: Monster, Slimes, NPCs (ja, auch Menschen!)
- Element-Immunität gilt (Eis-Slime kann nicht eingefroren werden)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import random


# =============================================================================
# ENUMS
# =============================================================================
class CreatureSize(Enum):
    """Größe beeinflusst welche Waffe optimal ist"""
    TINY = "tiny"           # Vögel, Ratten, Mini-Slimes
    SMALL = "small"         # Hasen, Füchse, Baby-Slimes
    MEDIUM = "medium"       # Wölfe, Hirsche, normale Slimes
    LARGE = "large"         # Bären, Elche, Champion-Slimes
    MASSIVE = "massive"     # Bosse, Riesen-Slimes, Drachen


class WeaponType(Enum):
    """Waffentyp für Jagd"""
    BOW = "bow"             # Leise, gut für alle Größen
    CROSSBOW = "crossbow"   # Stark, gut für Medium+
    RIFLE = "rifle"         # Laut, gut für Large+
    SHOTGUN = "shotgun"     # Zerstört kleine Tiere!
    PISTOL = "pistol"       # OK für Small/Medium
    MELEE = "melee"         # Beschädigt Materialien
    MAGIC = "magic"         # Element-abhängig


class HarvestQuality(Enum):
    """Qualität der Ernte (RDR2 Style)"""
    RUINED = 0      # Komplett zerstört (0%)
    POOR = 1        # Arm (25%)
    GOOD = 2        # Normal (75%)
    PERFECT = 3     # Perfekt (100% + Bonus)


class BodyPart(Enum):
    """Körperteile zum Zerlegen"""
    HEAD = "head"
    TORSO = "torso"
    LIMBS = "limbs"
    TAIL = "tail"
    CORE = "core"           # Für Slimes
    SPECIAL_ORGAN = "special"


# =============================================================================
# WAFFEN-EFFEKTIVITÄT (RDR2 Style)
# =============================================================================
# Welche Waffe für welche Größe?
# Returns: (quality_modifier, noise_level)
WEAPON_EFFECTIVENESS = {
    WeaponType.BOW: {
        CreatureSize.TINY: (1.0, 0.1),      # Perfekt, leise
        CreatureSize.SMALL: (1.0, 0.1),     # Perfekt, leise
        CreatureSize.MEDIUM: (0.9, 0.1),    # Gut, leise
        CreatureSize.LARGE: (0.7, 0.1),     # OK, leise
        CreatureSize.MASSIVE: (0.4, 0.1),   # Schwach, leise
    },
    WeaponType.CROSSBOW: {
        CreatureSize.TINY: (0.7, 0.2),      # Übertrieben
        CreatureSize.SMALL: (0.9, 0.2),     # Gut
        CreatureSize.MEDIUM: (1.0, 0.2),    # Perfekt
        CreatureSize.LARGE: (1.0, 0.2),     # Perfekt
        CreatureSize.MASSIVE: (0.7, 0.2),   # OK
    },
    WeaponType.RIFLE: {
        CreatureSize.TINY: (0.0, 1.0),      # ZERSTÖRT + LAUT
        CreatureSize.SMALL: (0.5, 1.0),     # Beschädigt + LAUT
        CreatureSize.MEDIUM: (0.8, 1.0),    # Gut + LAUT
        CreatureSize.LARGE: (1.0, 1.0),     # Perfekt + LAUT
        CreatureSize.MASSIVE: (1.0, 1.0),   # Perfekt + LAUT
    },
    WeaponType.SHOTGUN: {
        CreatureSize.TINY: (0.0, 1.0),      # KOMPLETT ZERSTÖRT
        CreatureSize.SMALL: (0.0, 1.0),     # KOMPLETT ZERSTÖRT
        CreatureSize.MEDIUM: (0.5, 1.0),    # Beschädigt
        CreatureSize.LARGE: (0.7, 1.0),     # OK
        CreatureSize.MASSIVE: (0.8, 1.0),   # Gut
    },
    WeaponType.PISTOL: {
        CreatureSize.TINY: (0.3, 0.7),      # Beschädigt
        CreatureSize.SMALL: (0.8, 0.7),     # Gut
        CreatureSize.MEDIUM: (0.9, 0.7),    # Gut
        CreatureSize.LARGE: (0.6, 0.7),     # Schwach
        CreatureSize.MASSIVE: (0.3, 0.7),   # Sehr schwach
    },
    WeaponType.MELEE: {
        CreatureSize.TINY: (0.5, 0.3),      # Beschädigt
        CreatureSize.SMALL: (0.6, 0.3),     # Beschädigt
        CreatureSize.MEDIUM: (0.5, 0.3),    # Beschädigt
        CreatureSize.LARGE: (0.4, 0.3),     # Sehr beschädigt
        CreatureSize.MASSIVE: (0.3, 0.3),   # Kaum Material
    },
    WeaponType.MAGIC: {
        CreatureSize.TINY: (0.8, 0.5),      # Gut (verbrennt etwas)
        CreatureSize.SMALL: (0.8, 0.5),     # Gut
        CreatureSize.MEDIUM: (0.8, 0.5),    # Gut
        CreatureSize.LARGE: (0.8, 0.5),     # Gut
        CreatureSize.MASSIVE: (0.9, 0.5),   # Sehr gut für Bosse
    },
}


# =============================================================================
# KÖRPERTEIL-EFFEKTE (Treffer-Zone)
# =============================================================================
HIT_ZONE_MULTIPLIER = {
    BodyPart.HEAD: {
        "damage_mult": 2.0,         # Doppelter Schaden
        "quality_mult": 1.5,        # 50% bessere Qualität (sauberer Kill)
        "instant_kill_chance": 0.8, # 80% Instant-Kill bei kleinen Tieren
    },
    BodyPart.TORSO: {
        "damage_mult": 1.0,
        "quality_mult": 1.0,
        "instant_kill_chance": 0.0,
    },
    BodyPart.LIMBS: {
        "damage_mult": 0.5,
        "quality_mult": 0.8,        # Beschädigt Gliedmaßen-Materialien
        "instant_kill_chance": 0.0,
    },
    BodyPart.TAIL: {
        "damage_mult": 0.3,
        "quality_mult": 0.5,        # Schwanz beschädigt
        "instant_kill_chance": 0.0,
    },
    BodyPart.CORE: {  # Slime-spezifisch
        "damage_mult": 3.0,         # Kritisch!
        "quality_mult": 1.2,        # Kern intakt = bessere Essenz
        "instant_kill_chance": 0.9,
    },
    BodyPart.SPECIAL_ORGAN: {
        "damage_mult": 1.5,
        "quality_mult": 0.5,        # Organ beschädigt wenn getroffen!
        "instant_kill_chance": 0.3,
    },
}


# =============================================================================
# KREATUREN-DEFINITIONEN
# =============================================================================
@dataclass
class HarvestMaterial:
    """Ein Material das geerntet werden kann"""
    id: str
    name: str
    base_amount: int
    rarity: float  # 0.0 - 1.0 (1.0 = immer, 0.1 = 10% Chance)
    body_part: BodyPart
    value: int  # Basiswert in Gold


@dataclass
class CreatureDefinition:
    """Definition einer jagdbaren Kreatur"""
    id: str
    name: str
    size: CreatureSize
    base_hp: int
    materials: List[HarvestMaterial]
    is_slime: bool = False
    element: Optional[str] = None
    trophy_name: Optional[str] = None  # Für perfekte Kills
    immune_to: List[str] = field(default_factory=list)  # Element-Immunitäten
    is_passive: bool = False  # Greift nicht von selbst an
    is_humanoid: bool = False  # Mensch/Goblin = Reputation-Verlust beim Töten!


# =============================================================================
# KREATUREN-DATENBANK
# =============================================================================
CREATURES = {
    # ===== NORMALE TIERE =====
    "rabbit": CreatureDefinition(
        id="rabbit", name="Hase", size=CreatureSize.SMALL, base_hp=20,
        materials=[
            HarvestMaterial("rabbit_meat", "Hasenfleisch", 2, 1.0, BodyPart.TORSO, 5),
            HarvestMaterial("rabbit_pelt", "Hasenfell", 1, 0.9, BodyPart.TORSO, 8),
            HarvestMaterial("rabbit_foot", "Hasenpfote", 1, 0.3, BodyPart.LIMBS, 25),  # Glücksbringer!
        ],
        trophy_name="Perfektes Hasenfell"
    ),

    "deer": CreatureDefinition(
        id="deer", name="Hirsch", size=CreatureSize.MEDIUM, base_hp=80,
        materials=[
            HarvestMaterial("venison", "Wildfleisch", 4, 1.0, BodyPart.TORSO, 12),
            HarvestMaterial("deer_pelt", "Hirschfell", 1, 0.95, BodyPart.TORSO, 20),
            HarvestMaterial("deer_antler", "Hirschgeweih", 2, 0.8, BodyPart.HEAD, 35),
            HarvestMaterial("sinew", "Sehnen", 2, 0.7, BodyPart.LIMBS, 8),
        ],
        trophy_name="Prächtiges Geweih"
    ),

    "wolf": CreatureDefinition(
        id="wolf", name="Wolf", size=CreatureSize.MEDIUM, base_hp=100,
        materials=[
            HarvestMaterial("wolf_meat", "Wolfsfleisch", 3, 1.0, BodyPart.TORSO, 8),
            HarvestMaterial("wolf_pelt", "Wolfsfell", 1, 0.9, BodyPart.TORSO, 30),
            HarvestMaterial("wolf_fang", "Wolfszahn", 2, 0.6, BodyPart.HEAD, 15),
            HarvestMaterial("wolf_claw", "Wolfskralle", 4, 0.5, BodyPart.LIMBS, 10),
        ],
        trophy_name="Alpha-Wolfsfell"
    ),

    "bear": CreatureDefinition(
        id="bear", name="Bär", size=CreatureSize.LARGE, base_hp=300,
        materials=[
            HarvestMaterial("bear_meat", "Bärenfleisch", 8, 1.0, BodyPart.TORSO, 15),
            HarvestMaterial("bear_pelt", "Bärenfell", 1, 0.95, BodyPart.TORSO, 80),
            HarvestMaterial("bear_fat", "Bärenfett", 3, 0.8, BodyPart.TORSO, 20),
            HarvestMaterial("bear_claw", "Bärenkralle", 4, 0.7, BodyPart.LIMBS, 25),
            HarvestMaterial("bear_heart", "Bärenherz", 1, 0.3, BodyPart.SPECIAL_ORGAN, 100),
        ],
        trophy_name="Legendäres Bärenfell"
    ),

    # ===== SLIMES =====
    "moos_slime": CreatureDefinition(
        id="moos_slime", name="Moos-Schleim", size=CreatureSize.SMALL, base_hp=40,
        is_slime=True, element="nature",
        materials=[
            HarvestMaterial("slime_gel", "Schleim-Gel", 3, 1.0, BodyPart.TORSO, 5),
            HarvestMaterial("moos_essence", "Moos-Essenz", 1, 0.8, BodyPart.CORE, 15),
            HarvestMaterial("nature_crystal", "Natur-Kristall", 1, 0.2, BodyPart.CORE, 50),
        ],
        trophy_name="Leuchtender Moos-Kern"
    ),

    "magma_slime": CreatureDefinition(
        id="magma_slime", name="Magma-Schleim", size=CreatureSize.MEDIUM, base_hp=80,
        is_slime=True, element="fire",
        immune_to=["fire", "burn"],  # Kann NICHT verbrennen!
        materials=[
            HarvestMaterial("slime_gel", "Schleim-Gel", 4, 1.0, BodyPart.TORSO, 5),
            HarvestMaterial("magma_essence", "Magma-Essenz", 1, 0.8, BodyPart.CORE, 25),
            HarvestMaterial("fire_crystal", "Feuer-Kristall", 1, 0.3, BodyPart.CORE, 75),
            HarvestMaterial("volcanic_rock", "Vulkangestein", 2, 0.6, BodyPart.TORSO, 10),
        ],
        trophy_name="Glühender Magma-Kern"
    ),

    "frost_slime": CreatureDefinition(
        id="frost_slime", name="Frost-Schleim", size=CreatureSize.MEDIUM, base_hp=70,
        is_slime=True, element="ice",
        immune_to=["ice", "freeze"],  # Kann NICHT eingefroren werden!
        materials=[
            HarvestMaterial("slime_gel", "Schleim-Gel", 4, 1.0, BodyPart.TORSO, 5),
            HarvestMaterial("frost_essence", "Frost-Essenz", 1, 0.8, BodyPart.CORE, 25),
            HarvestMaterial("ice_crystal", "Eis-Kristall", 1, 0.3, BodyPart.CORE, 75),
            HarvestMaterial("permafrost", "Permafrost", 2, 0.5, BodyPart.TORSO, 12),
        ],
        trophy_name="Ewiger Eis-Kern"
    ),

    "crystal_slime": CreatureDefinition(
        id="crystal_slime", name="Kristall-Schleim", size=CreatureSize.MEDIUM, base_hp=120,
        is_slime=True, element="light",
        materials=[
            HarvestMaterial("slime_gel", "Schleim-Gel", 3, 1.0, BodyPart.TORSO, 5),
            HarvestMaterial("crystal_essence", "Kristall-Essenz", 1, 0.8, BodyPart.CORE, 40),
            HarvestMaterial("prisma_shard", "Prisma-Splitter", 3, 0.6, BodyPart.TORSO, 30),
            HarvestMaterial("rainbow_crystal", "Regenbogen-Kristall", 1, 0.1, BodyPart.CORE, 200),
        ],
        trophy_name="Perfekter Prisma-Kern"
    ),

    "goetter_slime": CreatureDefinition(
        id="goetter_slime", name="Götter-Schleim", size=CreatureSize.LARGE, base_hp=500,
        is_slime=True, element="holy",
        materials=[
            HarvestMaterial("divine_gel", "Göttliches Gel", 5, 1.0, BodyPart.TORSO, 50),
            HarvestMaterial("divine_essence", "Göttliche Essenz", 1, 0.9, BodyPart.CORE, 150),
            HarvestMaterial("holy_crystal", "Heiliger Kristall", 1, 0.5, BodyPart.CORE, 300),
            HarvestMaterial("god_tear", "Götterträne", 1, 0.05, BodyPart.SPECIAL_ORGAN, 1000),
        ],
        trophy_name="Götterkern"
    ),

    # ===== MONSTER =====
    # ===== HUMANOIDE (JA, AUCH ZERLEGBAR!) =====
    "bandit": CreatureDefinition(
        id="bandit", name="Bandit", size=CreatureSize.MEDIUM, base_hp=100,
        is_humanoid=True, is_passive=False,
        materials=[
            HarvestMaterial("bandit_gear", "Banditen-Ausrüstung", 1, 0.8, BodyPart.TORSO, 15),
            HarvestMaterial("dirty_gold", "Schmutziges Gold", 5, 0.5, BodyPart.TORSO, 1),
            HarvestMaterial("human_leather", "Menschenleder", 1, 0.6, BodyPart.TORSO, 25),
            HarvestMaterial("human_bone", "Knochen", 3, 0.7, BodyPart.LIMBS, 5),
        ],
        trophy_name="Banditen-Kopfgeld"  # Kopfgeld statt Trophäe - kein Rep-Verlust!
    ),

    "wandering_merchant": CreatureDefinition(
        id="wandering_merchant", name="Wandernder Händler", size=CreatureSize.MEDIUM, base_hp=60,
        is_humanoid=True, is_passive=True,  # PASSIV = Rep-Verlust beim Töten!
        materials=[
            HarvestMaterial("merchant_goods", "Handelswaren", 3, 0.9, BodyPart.TORSO, 30),
            HarvestMaterial("gold_pouch", "Goldbeutel", 1, 0.8, BodyPart.TORSO, 50),
            HarvestMaterial("human_leather", "Menschenleder", 1, 0.6, BodyPart.TORSO, 25),
            HarvestMaterial("human_bone", "Knochen", 2, 0.5, BodyPart.LIMBS, 5),
        ],
        trophy_name=None  # REPUTATION VERLUST bei allen Fraktionen!
    ),

    "friendly_goblin": CreatureDefinition(
        id="friendly_goblin", name="Friedlicher Goblin", size=CreatureSize.SMALL, base_hp=40,
        is_humanoid=True, is_passive=True,  # PASSIV = moralisch fragwürdig!
        materials=[
            HarvestMaterial("goblin_trinket", "Goblin-Tand", 2, 0.9, BodyPart.TORSO, 8),
            HarvestMaterial("goblin_ear", "Goblin-Ohr", 2, 0.8, BodyPart.HEAD, 12),
            HarvestMaterial("goblin_hide", "Goblin-Haut", 1, 0.7, BodyPart.TORSO, 15),
            HarvestMaterial("small_bone", "Kleine Knochen", 3, 0.6, BodyPart.LIMBS, 3),
        ],
        trophy_name=None
    ),

    "sand_wurm": CreatureDefinition(
        id="sand_wurm", name="Sandwurm", size=CreatureSize.MASSIVE, base_hp=800,
        materials=[
            HarvestMaterial("wurm_meat", "Wurmfleisch", 15, 1.0, BodyPart.TORSO, 20),
            HarvestMaterial("wurm_hide", "Wurmhaut", 3, 0.9, BodyPart.TORSO, 60),
            HarvestMaterial("wurm_tooth", "Wurmzahn", 8, 0.7, BodyPart.HEAD, 40),
            HarvestMaterial("sand_gland", "Sand-Drüse", 1, 0.4, BodyPart.SPECIAL_ORGAN, 150),
            HarvestMaterial("wurm_pearl", "Wurmperle", 1, 0.1, BodyPart.CORE, 500),
        ],
        trophy_name="Legendärer Wurmschädel"
    ),
}


# =============================================================================
# HARVEST SYSTEM
# =============================================================================
@dataclass
class HarvestResult:
    """Ergebnis einer Ernte"""
    creature_name: str
    quality: HarvestQuality
    materials: Dict[str, int]  # material_id -> amount
    trophy: Optional[str]
    total_value: int
    message: str


class HuntingSystem:
    """Verwaltet Jagd und Ernte"""

    def __init__(self):
        self.hunting_skill = 1  # Wird vom Spieler-Skill übernommen

    def calculate_kill_quality(
        self,
        creature_id: str,
        weapon: WeaponType,
        hit_zone: BodyPart,
        was_one_hit: bool,
        player_skill: int = 50
    ) -> HarvestQuality:
        """
        Berechnet die Qualität des Kills (RDR2 Style)

        Faktoren:
        - Waffe vs Kreatur-Größe
        - Treffer-Zone (Kopf = besser)
        - Ein-Treffer-Kill = Bonus
        - Spieler-Skill
        """
        if creature_id not in CREATURES:
            return HarvestQuality.POOR

        creature = CREATURES[creature_id]

        # Basis: Waffen-Effektivität
        weapon_data = WEAPON_EFFECTIVENESS.get(weapon, {})
        size_data = weapon_data.get(creature.size, (0.5, 0.5))
        weapon_quality = size_data[0]

        # Wenn Waffe komplett ungeeignet
        if weapon_quality == 0.0:
            return HarvestQuality.RUINED

        # Treffer-Zone Bonus
        zone_data = HIT_ZONE_MULTIPLIER.get(hit_zone, {})
        zone_quality = zone_data.get("quality_mult", 1.0)

        # Ein-Treffer-Kill Bonus
        one_hit_bonus = 1.2 if was_one_hit else 1.0

        # Skill-Bonus (0-100 Skill = 0.5x - 1.5x)
        skill_mult = 0.5 + (player_skill / 100)

        # Finale Qualität berechnen
        final_quality = weapon_quality * zone_quality * one_hit_bonus * skill_mult

        # In Qualitätsstufe umwandeln
        if final_quality >= 1.3:
            return HarvestQuality.PERFECT
        elif final_quality >= 0.9:
            return HarvestQuality.GOOD
        elif final_quality >= 0.4:
            return HarvestQuality.POOR
        else:
            return HarvestQuality.RUINED

    def harvest_creature(
        self,
        creature_id: str,
        quality: HarvestQuality,
        player_skill: int = 50
    ) -> HarvestResult:
        """
        Erntet Materialien von einer Kreatur

        Returns:
            HarvestResult mit allen Materialien
        """
        if creature_id not in CREATURES:
            return HarvestResult(
                creature_name="Unbekannt",
                quality=HarvestQuality.RUINED,
                materials={},
                trophy=None,
                total_value=0,
                message="Kreatur nicht gefunden!"
            )

        creature = CREATURES[creature_id]
        harvested = {}
        total_value = 0

        # Qualitäts-Multiplikatoren
        quality_mult = {
            HarvestQuality.RUINED: 0.0,
            HarvestQuality.POOR: 0.25,
            HarvestQuality.GOOD: 0.75,
            HarvestQuality.PERFECT: 1.0,
        }

        mult = quality_mult[quality]

        # Skill-Bonus für Materialien
        skill_bonus = 1.0 + (player_skill / 200)  # Max +50% bei Skill 100

        # Materialien ernten
        for mat in creature.materials:
            # Rarity-Check
            if random.random() > mat.rarity:
                continue

            # Menge berechnen
            base_amount = mat.base_amount
            final_amount = int(base_amount * mult * skill_bonus)

            # Mindestens 1 wenn nicht RUINED
            if quality != HarvestQuality.RUINED and final_amount == 0:
                final_amount = 1 if random.random() < 0.5 else 0

            if final_amount > 0:
                harvested[mat.id] = final_amount
                total_value += mat.value * final_amount

        # Trophäe nur bei PERFECT
        trophy = None
        if quality == HarvestQuality.PERFECT and creature.trophy_name:
            trophy = creature.trophy_name
            total_value += 100  # Trophäen-Bonus

        # Nachricht generieren
        messages = {
            HarvestQuality.RUINED: f"Die {creature.name} ist komplett zerstört. Keine brauchbaren Materialien.",
            HarvestQuality.POOR: f"Du hast die {creature.name} unsauber erlegt. Wenig Materialien gerettet.",
            HarvestQuality.GOOD: f"Guter Kill! Du erntest brauchbare Materialien von der {creature.name}.",
            HarvestQuality.PERFECT: f"PERFEKTER KILL! Du erhältst alle Materialien + {trophy}!",
        }

        return HarvestResult(
            creature_name=creature.name,
            quality=quality,
            materials=harvested,
            trophy=trophy,
            total_value=total_value,
            message=messages[quality]
        )

    def get_recommended_weapon(self, creature_id: str) -> List[Tuple[WeaponType, str]]:
        """Empfiehlt die beste Waffe für eine Kreatur"""
        if creature_id not in CREATURES:
            return []

        creature = CREATURES[creature_id]
        recommendations = []

        for weapon, size_data in WEAPON_EFFECTIVENESS.items():
            if creature.size in size_data:
                quality, noise = size_data[creature.size]
                if quality >= 0.9:
                    noise_str = "leise" if noise < 0.3 else "mittel" if noise < 0.7 else "LAUT"
                    recommendations.append((weapon, f"Perfekt ({noise_str})"))
                elif quality >= 0.7:
                    recommendations.append((weapon, "Gut"))

        return recommendations


# =============================================================================
# STYLE GUIDE NOTIZEN
# =============================================================================
"""
FANTASY WESTERN STYLE MIX:

VISUALS (Borderlands + Anime):
- Cel-Shading Effekt
- Übertriebene Animationen beim Häuten
- Anime-Style Reactions ("PERFEKT!" mit Sparkles)

GAMEPLAY (RDR2 + Palworld):
- Waffe matters (nicht alles mit Shotgun!)
- Kopfschüsse = sauberer Kill
- Slimes haben KERN statt Kopf
- Jedes Monster = Ressourcen

TONE (1883 + Konosuba):
- Ernstes Survival...
- ...aber Najika kommentiert alles lustig
- "EXPLOSION hätte den Hasen KOMPLETT vernichtet, Mr.K!"

SOUND:
- RDR2 Style "Häuten" Animation
- Satisfying Loot-Sounds
- Najika Voice Lines beim Ernten
"""


# =============================================================================
# TEST
# =============================================================================
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    print("=" * 70)
    print("NAJIKA HUNTING & HARVESTING SYSTEM - TEST")
    print("RDR2 + Palworld + Monster Hunter Style!")
    print("=" * 70)

    hunting = HuntingSystem()

    # Test 1: Hase mit Bogen (perfekt)
    print("\n--- TEST 1: Hase + Bogen (Kopfschuss, 1-Hit) ---")
    quality = hunting.calculate_kill_quality(
        "rabbit", WeaponType.BOW, BodyPart.HEAD,
        was_one_hit=True, player_skill=75
    )
    print(f"Qualität: {quality.name}")
    result = hunting.harvest_creature("rabbit", quality, player_skill=75)
    print(f"  {result.message}")
    print(f"  Materialien: {result.materials}")
    print(f"  Trophäe: {result.trophy}")
    print(f"  Wert: {result.total_value} Gold")

    # Test 2: Hase mit Shotgun (zerstört)
    print("\n--- TEST 2: Hase + Shotgun (ZERSTÖRT!) ---")
    quality = hunting.calculate_kill_quality(
        "rabbit", WeaponType.SHOTGUN, BodyPart.TORSO,
        was_one_hit=True, player_skill=75
    )
    print(f"Qualität: {quality.name}")
    result = hunting.harvest_creature("rabbit", quality, player_skill=75)
    print(f"  {result.message}")

    # Test 3: Magma-Slime mit Magie
    print("\n--- TEST 3: Magma-Slime + Magie (Kern-Treffer) ---")
    quality = hunting.calculate_kill_quality(
        "magma_slime", WeaponType.MAGIC, BodyPart.CORE,
        was_one_hit=True, player_skill=60
    )
    print(f"Qualität: {quality.name}")
    result = hunting.harvest_creature("magma_slime", quality, player_skill=60)
    print(f"  {result.message}")
    print(f"  Materialien: {result.materials}")
    print(f"  Wert: {result.total_value} Gold")

    # Test 4: Empfohlene Waffen
    print("\n--- TEST 4: Empfohlene Waffen ---")
    print("Für Hirsch:")
    for weapon, rating in hunting.get_recommended_weapon("deer"):
        print(f"  - {weapon.value}: {rating}")

    print("\nFür Götter-Schleim:")
    for weapon, rating in hunting.get_recommended_weapon("goetter_slime"):
        print(f"  - {weapon.value}: {rating}")

    print("\n" + "=" * 70)
    print("EXPLOSION!!! Jedes Monster = Ressourcen!")
    print("=" * 70)
