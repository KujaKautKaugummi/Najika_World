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


class FinisherStyle(Enum):
    """Finisher personality styles"""
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
    style: FinisherStyle
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
        ingredients: List[str],
        character_level: int = 1,
        user_id: Optional[int] = None
    ) -> FinisherAnimation:
        """
        Create a custom finisher from ingredients

        Args:
            ingredients: List of ingredient descriptions
            character_level: Character level (affects power)
            user_id: User ID for tracking

        Returns:
            FinisherAnimation object
        """
        # Analyze ingredients to determine style
        analysis = self._analyze_ingredients(ingredients)
        style = analysis["style"]

        # Generate name
        name = self._generate_name(ingredients, style)

        # Generate animation steps
        animation_steps = self._generate_animation_steps(ingredients, style, analysis)

        # Calculate power
        brutality = min(10, analysis["brutality_score"] + (character_level // 10))
        humor = min(10, analysis["humor_score"])
        damage_multiplier = 1.0 + (brutality * 0.2) + (character_level * 0.05)

        # Duration based on complexity
        duration = 3.0 + (len(animation_steps) * 0.5)

        finisher = FinisherAnimation(
            name=name,
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

    def _analyze_ingredients(self, ingredients: List[str]) -> Dict:
        """Analyze ingredients to determine finisher characteristics"""
        text = " ".join(ingredients).lower()

        # Keyword scoring
        scores = {
            FinisherStyle.EXPLOSION: 0,
            FinisherStyle.CUTE_BRUTAL: 0,
            FinisherStyle.CHAOS: 0,
            FinisherStyle.CALCULATED: 0,
            FinisherStyle.DOMINANT: 0
        }

        # EXPLOSION keywords
        explosion_keywords = ["explosion", "dynamit", "bombe", "feuer", "flamme", "spreng", "blast"]
        scores[FinisherStyle.EXPLOSION] = sum(1 for k in explosion_keywords if k in text)

        # CUTE_BRUTAL keywords
        cute_keywords = ["niedlich", "süß", "kuschel", "plüsch", "kawaii", "cute", "fluffy"]
        scores[FinisherStyle.CUTE_BRUTAL] = sum(1 for k in cute_keywords if k in text)

        # CHAOS keywords
        chaos_keywords = ["chaos", "anarchie", "verrückt", "wahnsinn", "random", "crazy"]
        scores[FinisherStyle.CHAOS] = sum(1 for k in chaos_keywords if k in text)

        # CALCULATED keywords
        calculated_keywords = ["strategie", "plan", "präzis", "berechnung", "mathematik", "logik"]
        scores[FinisherStyle.CALCULATED] = sum(1 for k in calculated_keywords if k in text)

        # DOMINANT keywords
        dominant_keywords = ["macht", "herrsch", "dominant", "stark", "überlegen", "throne"]
        scores[FinisherStyle.DOMINANT] = sum(1 for k in dominant_keywords if k in text)

        # Determine primary style
        style = max(scores, key=scores.get)

        # If no clear winner, use CUTE_BRUTAL (default Happy Tree Friends style)
        if scores[style] == 0:
            style = FinisherStyle.CUTE_BRUTAL

        return {
            "style": style,
            "brutality_score": min(10, len(ingredients) + scores[style]),
            "humor_score": min(10, 5 + random.randint(0, 5)),
            "complexity": len(ingredients)
        }

    def _generate_name(self, ingredients: List[str], style: FinisherStyle) -> str:
        """Generate finisher name based on ingredients and style"""
        templates = self.templates[style]
        prefix = random.choice(templates["prefixes"])

        # Use first ingredient as base
        base = ingredients[0] if ingredients else "Finisher"

        names = {
            FinisherStyle.EXPLOSION: f"{prefix}e {base}-EXPLOSION!!!",
            FinisherStyle.CUTE_BRUTAL: f"{prefix}s {base} des Todes ♥",
            FinisherStyle.CHAOS: f"{prefix}r {base}-Wahnsinn!",
            FinisherStyle.CALCULATED: f"{prefix}r {base}-Strike",
            FinisherStyle.DOMINANT: f"{prefix}r {base}-Judgment"
        }

        return names.get(style, f"{prefix}r {base}-Finisher")

    def _generate_animation_steps(
        self,
        ingredients: List[str],
        style: FinisherStyle,
        analysis: Dict
    ) -> List[Dict[str, str]]:
        """Generate the 4-phase animation sequence"""
        templates = self.templates[style]
        action = random.choice(templates["actions"])
        effect = random.choice(templates["effects"])

        steps = [
            {
                "phase": AnimationStep.SETUP.value,
                "duration": 0.5,
                "camera": "zoom_in",
                "description": f"Bereitet {ingredients[0] if ingredients else 'Angriff'} vor...",
                "visual": "Charge-up effects, screen shake"
            },
            {
                "phase": AnimationStep.BUILDUP.value,
                "duration": 1.0,
                "camera": "dramatic_angle",
                "description": f"Energie sammelt sich, {effect} erscheint!",
                "visual": f"Particle effects: {effect}"
            },
            {
                "phase": AnimationStep.IMPACT.value,
                "duration": 1.5,
                "camera": "impact_zoom",
                "description": f"{action}!",
                "visual": "Screen flash, massive particle explosion, slow-mo"
            },
            {
                "phase": AnimationStep.AFTERMATH.value,
                "duration": 1.0,
                "camera": "wide_shot",
                "description": "Staub legt sich... Ziel besiegt!",
                "visual": "Victory pose, confetti, XP gain"
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
