"""
Najika Finisher System
Happy Tree Friends meets Mortal Kombat style finisher generator

Generates brutal yet cute finisher animations based on player-provided ingredients.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
import random
from datetime import datetime


class BrutalityCategory(Enum):
    """Player-selected brutality categories"""
    HONORABLE_DEATH = "Ehrenvoller Tod"      # Clean, respectful finish
    FUNNY_DEATH = "Lustiger Tod"             # Comical, absurd finish
    CRUEL_DEATH = "Grausamer Tod"            # Dark, sadistic finish
    BLOOD_BATH = "Tod Tod Blut Blut"         # EXTREME brutality
    EPIC_DEATH = "Epischer Tod"              # Cinematic, over-the-top


class FinisherStyle(Enum):
    """Finisher personality styles (auto-determined from category + ingredients)"""
    CUTE_BRUTAL = "Niedlich-Brutal"  # Happy Tree Friends Style
    EXPLOSION = "EXPLOSION!"  # Megumin Style
    CHAOS = "Chaotisch"  # Harley Quinn Style
    CALCULATED = "Berechnet"  # Shiro Style
    DOMINANT = "Dominant"  # Albedo/Shadow Style


class AnimationStep(Enum):
    """Animation phases for finisher"""
    SETUP = "Setup"
    BUILDUP = "Buildup"
    IMPACT = "Impact"
    AFTERMATH = "Aftermath"


@dataclass
class FinisherAnimation:
    """A complete finisher animation sequence"""
    name: str
    category: BrutalityCategory  # Player-selected category
    style: FinisherStyle  # Auto-determined style
    animation_steps: List[Dict[str, str]]
    brutality_level: int  # 1-10
    humor_level: int  # 1-10
    damage_multiplier: float  # 1.0 - 3.0
    duration_seconds: float
    ingredients_used: List[str]
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert to dictionary for API response"""
        return {
            "name": self.name,
            "category": self.category.value,
            "style": self.style.value,
            "animation_steps": self.animation_steps,
            "brutality_level": self.brutality_level,
            "humor_level": self.humor_level,
            "damage_multiplier": self.damage_multiplier,
            "duration_seconds": self.duration_seconds,
            "ingredients_used": self.ingredients_used,
            "created_at": self.created_at.isoformat()
        }


class NajikaFinisherGenerator:
    """
    Generates custom finisher animations based on ingredients

    Example ingredients:
    - "Dynamit" → EXPLOSION style
    - "Kuscheliges Plüschtier" → CUTE_BRUTAL style
    - "Mathematische Gleichung" → CALCULATED style
    - "Chaos und Anarchie" → CHAOS style
    """

    def __init__(self):
        self.finisher_database = []
        self._init_templates()

    def _init_templates(self):
        """Initialize finisher templates for each style"""
        self.templates = {
            FinisherStyle.CUTE_BRUTAL: {
                "prefixes": ["Niedliches", "Kuscheliges", "Süßes", "Flauschiges"],
                "actions": [
                    "zerquetscht mit unerwarteter Gewalt",
                    "sprengt süß lächelnd in die Luft",
                    "zerstört mit niedlicher Eleganz",
                    "vernichtet mit kawaii Power"
                ],
                "effects": ["Glitzer-Explosion", "Herz-Partikel", "Regenbogen-Spray", "Konfetti-Regen"]
            },
            FinisherStyle.EXPLOSION: {
                "prefixes": ["Explosive", "Magische", "Gewaltige", "MEGA"],
                "actions": [
                    "EXPLODIERT mit maximaler Zerstörungskraft",
                    "entfesselt eine vernichtende Explosion",
                    "sprengt alles in die Stratosphäre",
                    "löst eine Kettenreaktion aus"
                ],
                "effects": ["Mushroom Cloud", "Flammen-Tornado", "Schockwelle", "Krater"]
            },
            FinisherStyle.CHAOS: {
                "prefixes": ["Chaotische", "Wahnsinnige", "Anarchistische", "Verrückte"],
                "actions": [
                    "zerstört mit unberechenbarer Energie",
                    "vernichtet in purem Chaos",
                    "entfesselt totale Anarchie",
                    "erschafft kreatives Chaos"
                ],
                "effects": ["Disco-Lichter", "Glitch-Effekte", "Farb-Chaos", "Reality-Break"]
            },
            FinisherStyle.CALCULATED: {
                "prefixes": ["Präzise", "Berechnete", "Strategische", "Analytische"],
                "actions": [
                    "zerstört mit mathematischer Präzision",
                    "vernichtet nach perfektem Plan",
                    "eliminiert mit 99.99% Effizienz",
                    "dekonstruiert systematisch"
                ],
                "effects": ["Blaupausen-Overlay", "Berechnungs-Formeln", "Scan-Lines", "Data-Stream"]
            },
            FinisherStyle.DOMINANT: {
                "prefixes": ["Überlegene", "Absolute", "Herrschende", "Dominante"],
                "actions": [
                    "unterwirft mit absoluter Macht",
                    "vernichtet mit überlegener Kraft",
                    "demonstriert totale Dominanz",
                    "zerquetscht wie eine Ameise"
                ],
                "effects": ["Dark Aura", "Shadow Wings", "Throne Appearance", "Crown Glow"]
            }
        }

    def create_custom_finisher(
        self,
        category: BrutalityCategory,
        ingredients: List[str],
        character_level: int = 1,
        user_id: Optional[int] = None
    ) -> FinisherAnimation:
        """
        Create a custom finisher from category and ingredients

        Args:
            category: Player-selected brutality category
            ingredients: List of ingredient descriptions (keywords)
            character_level: Character level (affects power)
            user_id: User ID for tracking

        Returns:
            FinisherAnimation object
        """
        # Analyze ingredients to determine style
        analysis = self._analyze_ingredients(ingredients, category)
        style = analysis["style"]

        # Generate name based on category and ingredients
        name = self._generate_name(ingredients, style, category)

        # Generate animation steps
        animation_steps = self._generate_animation_steps(ingredients, style, category, analysis)

        # Calculate power based on category
        brutality = self._calculate_brutality(category, character_level)
        humor = self._calculate_humor(category, analysis)
        damage_multiplier = 1.0 + (brutality * 0.2) + (character_level * 0.05)

        # Duration based on complexity and category
        duration = 3.0 + (len(animation_steps) * 0.5)
        if category == BrutalityCategory.BLOOD_BATH:
            duration += 1.0  # Longer for extreme brutality
        elif category == BrutalityCategory.EPIC_DEATH:
            duration += 1.5  # Cinematic = longer

        finisher = FinisherAnimation(
            name=name,
            category=category,
            style=style,
            animation_steps=animation_steps,
            brutality_level=brutality,
            humor_level=humor,
            damage_multiplier=damage_multiplier,
            duration_seconds=duration,
            ingredients_used=ingredients
        )

        self.finisher_database.append(finisher)
        return finisher

    def _analyze_ingredients(self, ingredients: List[str], category: BrutalityCategory) -> Dict:
        """Analyze ingredients and category to determine finisher characteristics"""
        text = " ".join(ingredients).lower()

        # Keyword scoring for style
        scores = {
            FinisherStyle.EXPLOSION: 0,
            FinisherStyle.CUTE_BRUTAL: 0,
            FinisherStyle.CHAOS: 0,
            FinisherStyle.CALCULATED: 0,
            FinisherStyle.DOMINANT: 0
        }

        # EXPLOSION keywords
        explosion_keywords = ["explosion", "dynamit", "bombe", "feuer", "flamme", "spreng", "blast", "boom"]
        scores[FinisherStyle.EXPLOSION] = sum(1 for k in explosion_keywords if k in text)

        # CUTE_BRUTAL keywords
        cute_keywords = ["niedlich", "süß", "kuschel", "plüsch", "kawaii", "cute", "fluffy", "herz"]
        scores[FinisherStyle.CUTE_BRUTAL] = sum(1 for k in cute_keywords if k in text)

        # CHAOS keywords
        chaos_keywords = ["chaos", "anarchie", "verrückt", "wahnsinn", "random", "crazy", "wild"]
        scores[FinisherStyle.CHAOS] = sum(1 for k in chaos_keywords if k in text)

        # CALCULATED keywords
        calculated_keywords = ["strategie", "plan", "präzis", "berechnung", "mathematik", "logik", "analyse"]
        scores[FinisherStyle.CALCULATED] = sum(1 for k in calculated_keywords if k in text)

        # DOMINANT keywords
        dominant_keywords = ["macht", "herrsch", "dominant", "stark", "überlegen", "throne", "könig"]
        scores[FinisherStyle.DOMINANT] = sum(1 for k in dominant_keywords if k in text)

        # Determine primary style
        style = max(scores, key=scores.get)

        # Category influences style selection
        if scores[style] == 0:
            # No keyword match, choose style based on category
            category_style_map = {
                BrutalityCategory.HONORABLE_DEATH: FinisherStyle.CALCULATED,
                BrutalityCategory.FUNNY_DEATH: FinisherStyle.CUTE_BRUTAL,
                BrutalityCategory.CRUEL_DEATH: FinisherStyle.DOMINANT,
                BrutalityCategory.BLOOD_BATH: FinisherStyle.CHAOS,
                BrutalityCategory.EPIC_DEATH: FinisherStyle.EXPLOSION
            }
            style = category_style_map.get(category, FinisherStyle.CUTE_BRUTAL)

        return {
            "style": style,
            "brutality_score": min(10, len(ingredients) + scores[style]),
            "humor_score": min(10, 5 + random.randint(0, 5)),
            "complexity": len(ingredients)
        }

    def _calculate_brutality(self, category: BrutalityCategory, character_level: int) -> int:
        """Calculate brutality level based on category"""
        base_brutality = {
            BrutalityCategory.HONORABLE_DEATH: 3,   # Clean, respectful
            BrutalityCategory.FUNNY_DEATH: 5,       # Moderate, comical
            BrutalityCategory.CRUEL_DEATH: 8,       # Dark, sadistic
            BrutalityCategory.BLOOD_BATH: 10,       # EXTREME
            BrutalityCategory.EPIC_DEATH: 7         # Spectacular
        }

        brutality = base_brutality.get(category, 5)
        brutality += (character_level // 10)  # Level bonus
        return min(10, brutality)

    def _calculate_humor(self, category: BrutalityCategory, analysis: Dict) -> int:
        """Calculate humor level based on category"""
        base_humor = {
            BrutalityCategory.HONORABLE_DEATH: 2,   # Serious
            BrutalityCategory.FUNNY_DEATH: 10,      # Maximum comedy
            BrutalityCategory.CRUEL_DEATH: 1,       # Dark, no humor
            BrutalityCategory.BLOOD_BATH: 0,        # Pure brutality
            BrutalityCategory.EPIC_DEATH: 5         # Some flair
        }

        humor = base_humor.get(category, 5)
        return min(10, humor)

    def _generate_name(self, ingredients: List[str], style: FinisherStyle, category: BrutalityCategory) -> str:
        """Generate finisher name based on ingredients, style, and category"""
        templates = self.templates[style]
        prefix = random.choice(templates["prefixes"])

        # Use first ingredient as base
        base = ingredients[0] if ingredients else "Tod"

        # Category-specific suffixes
        category_suffixes = {
            BrutalityCategory.HONORABLE_DEATH: "des Ehrbaren Kriegers",
            BrutalityCategory.FUNNY_DEATH: "der Absurdität ☺",
            BrutalityCategory.CRUEL_DEATH: "der Grausamkeit ☠",
            BrutalityCategory.BLOOD_BATH: "DES BLUTBADES 💀💀💀",
            BrutalityCategory.EPIC_DEATH: "der Legende ⚡"
        }

        suffix = category_suffixes.get(category, "")

        names = {
            FinisherStyle.EXPLOSION: f"{prefix}e {base}-EXPLOSION!!! {suffix}",
            FinisherStyle.CUTE_BRUTAL: f"{prefix}s {base} {suffix}",
            FinisherStyle.CHAOS: f"{prefix}r {base}-Wahnsinn {suffix}",
            FinisherStyle.CALCULATED: f"{prefix}r {base}-Strike {suffix}",
            FinisherStyle.DOMINANT: f"{prefix}r {base}-Judgment {suffix}"
        }

        return names.get(style, f"{prefix}r {base}-Finisher {suffix}")

    def _generate_animation_steps(
        self,
        ingredients: List[str],
        style: FinisherStyle,
        category: BrutalityCategory,
        analysis: Dict
    ) -> List[Dict[str, str]]:
        """Generate the 4-phase animation sequence based on category"""
        templates = self.templates[style]
        action = random.choice(templates["actions"])
        effect = random.choice(templates["effects"])

        # Category-specific descriptions
        category_descriptions = {
            BrutalityCategory.HONORABLE_DEATH: {
                "setup": f"Verbeugt sich respektvoll, bereitet {ingredients[0] if ingredients else 'Klinge'} vor",
                "aftermath": "Ehrenvolle Verbeugung. Gegner fällt würdevoll."
            },
            BrutalityCategory.FUNNY_DEATH: {
                "setup": f"*Stolpert* Ooops! Bereitet {ingredients[0] if ingredients else 'Witz'} vor",
                "aftermath": "🎭 Comedy-Trommel! Alle lachen! XP +100"
            },
            BrutalityCategory.CRUEL_DEATH: {
                "setup": f"Böses Grinsen... {ingredients[0] if ingredients else 'Folter'} wird vorbereitet",
                "aftermath": "Blut fließt. Gegner leidet. Sieg durch Grausamkeit."
            },
            BrutalityCategory.BLOOD_BATH: {
                "setup": f"BLUT! BLUT! {ingredients[0] if ingredients else 'ZERSTÖRUNG'} WIRD ENTFESSELT!",
                "aftermath": "💀💀💀 BLUTBAD! Überall nur ROT! EXTREME BRUTALITY!"
            },
            BrutalityCategory.EPIC_DEATH: {
                "setup": f"⚡ Epische Musik! {ingredients[0] if ingredients else 'Ultimativer Angriff'} lädt auf!",
                "aftermath": "🎬 LEGENDARY KILL! Cinematische Slow-Motion Victory!"
            }
        }

        desc = category_descriptions.get(category, {
            "setup": f"Bereitet {ingredients[0] if ingredients else 'Angriff'} vor...",
            "aftermath": "Staub legt sich... Ziel besiegt!"
        })

        steps = [
            {
                "phase": AnimationStep.SETUP.value,
                "duration": 0.5,
                "camera": "zoom_in",
                "description": desc.get("setup", f"Bereitet {ingredients[0]} vor"),
                "visual": "Charge-up effects, screen shake",
                "category_modifier": category.value
            },
            {
                "phase": AnimationStep.BUILDUP.value,
                "duration": 1.0,
                "camera": "dramatic_angle",
                "description": f"Energie sammelt sich, {effect} erscheint!",
                "visual": f"Particle effects: {effect}",
                "category_modifier": category.value
            },
            {
                "phase": AnimationStep.IMPACT.value,
                "duration": 1.5,
                "camera": "impact_zoom",
                "description": f"{action}!",
                "visual": "Screen flash, massive particle explosion, slow-mo",
                "category_modifier": category.value,
                "brutality_level": self._calculate_brutality(category, 1)
            },
            {
                "phase": AnimationStep.AFTERMATH.value,
                "duration": 1.0,
                "camera": "wide_shot",
                "description": desc.get("aftermath", "Ziel besiegt!"),
                "visual": "Victory pose, confetti, XP gain",
                "category_modifier": category.value
            }
        ]

        return steps

    def get_finisher_by_id(self, finisher_id: int) -> Optional[FinisherAnimation]:
        """Get finisher from database by ID"""
        if 0 <= finisher_id < len(self.finisher_database):
            return self.finisher_database[finisher_id]
        return None

    def list_all_finishers(self, limit: int = 50) -> List[FinisherAnimation]:
        """List all created finishers"""
        return self.finisher_database[-limit:]

    def get_random_finisher_ingredients(self) -> List[str]:
        """Get random ingredient suggestions for players"""
        ingredient_pool = [
            "Dynamit",
            "Kuscheliges Plüschtier",
            "Mathematische Gleichung",
            "Chaos-Orb",
            "Herrscherstab",
            "Explosionstrank",
            "Niedlicher Hammer",
            "Berechnungs-Matrix",
            "Anarchie-Flagge",
            "Dominanz-Aura",
            "Glitzer-Bombe",
            "Strategie-Buch",
            "Wahnsinniger Blick",
            "Magische Krone",
            "MEGA-Feuerwerk"
        ]

        return random.sample(ingredient_pool, k=3)


# Global finisher generator instance
finisher_generator = NajikaFinisherGenerator()
