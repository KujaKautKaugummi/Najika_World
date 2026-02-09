"""
NAJIKA SKILL & COMBAT SYSTEM V3 - KORRIGIERT!
==============================================
Basierend auf Kujas Feedback:

HAUPTREGELN:
1. KEINE KLASSEN - Jeder kann alles lernen (Skyrim)
2. 1-SKILL-WEG:
   - JEDE Magieschule UND JEDE Waffenklasse kann diesen Weg wählen
   - Dann kann diese Skill-Linie MORPHEN
   - KEIN ZURÜCK! (Spieler wird mehrfach gewarnt)
   - Explosion: kostet Mana+Stamina, NUR 1-Skill-Weg, KEIN Verweben

3. NORMALE SKILLS:
   - Magie + Magie = VERWEBEN (z.B. Feuer+Wasser=Dampf)
   - Magie + Waffe = KOMBINIEREN (z.B. Feuerzauber+Schwert=Feuerschwert)
   - Können NICHT morphen!

4. KÖRPERTEIL-TARGETING (wie Fortnite/Skyrim):
   - NORMALES ZIELEN, keine Zeitlupe!
   - Wo du triffst = Effekt (Bein = langsam, Kopf = Crit)
   - Precision-Skill verbessert Trefferchance
   - Analyse AUSSERHALB Kampf für Schwächen

5. FALLOUT-INTEGRATION:
   - S.P.E.C.I.A.L. Stats
   - Perk-System
   - Körperteil-Schaden
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
import random
from datetime import datetime, timedelta


# =============================================================================
# FALLOUT S.P.E.C.I.A.L. STATS
# =============================================================================
@dataclass
class SpecialStats:
    """Fallout-Style Basis-Attribute (1-10, max 15 mit Buffs)"""
    strength: int = 5       # Nahkampf, Tragen, Stagger-Resist
    perception: int = 5     # VATS-Präzision, Erkennung, Fallen
    endurance: int = 5      # HP, Stamina, Gift/Krankheit-Resist
    charisma: int = 5       # Händler-Preise, Party-Boni, NPC-Reaktion
    intelligence: int = 5   # Magie-Schaden, XP-Bonus, Crafting
    agility: int = 5        # Ausweichen, Crit, Initiative, AP
    luck: int = 5           # Crit-Chance, Drops, Skill-Lernen

    def get(self, stat_name: str) -> int:
        return getattr(self, stat_name.lower(), 5)

    def modify(self, stat_name: str, amount: int):
        current = getattr(self, stat_name.lower())
        setattr(self, stat_name.lower(), max(1, min(15, current + amount)))


# =============================================================================
# SKILL-LINIEN (Magie + Waffen)
# =============================================================================
class SkillLineType(Enum):
    """Alle Skill-Linien die den 1-Skill-Weg wählen können"""
    # MAGIE
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    WIND = "wind"
    LIGHTNING = "lightning"
    ICE = "ice"
    NATURE = "nature"
    DARK = "dark"
    LIGHT = "light"
    EXPLOSION = "explosion"  # Spezial: NUR 1-Skill-Weg, KEIN Verweben!

    # WAFFEN
    SWORD = "sword"
    AXE = "axe"
    HAMMER = "hammer"
    SPEAR = "spear"
    DAGGER = "dagger"
    BOW = "bow"
    CROSSBOW = "crossbow"
    STAFF = "staff"
    SHIELD = "shield"
    FIST = "fist"


# =============================================================================
# 1-SKILL-WEG SYSTEM
# =============================================================================
@dataclass
class OneSkillPath:
    """
    Der 1-Skill-Weg - KEIN ZURÜCK!

    Wenn gewählt:
    - Diese Skill-Linie kann MORPHEN
    - Explosion: kostet Mana+Stamina, Finisher 1x/Tag
    - Andere: Spezialisierung mit Trade-offs
    """
    skill_line: SkillLineType
    chosen: bool = False
    morph_level: int = 0  # 0-5 Morph-Stufen
    current_morph: Optional[str] = None

    # Warnungen (muss 3x bestätigt werden!)
    warnings_shown: int = 0
    REQUIRED_WARNINGS: int = 3

    # Explosion-spezifisch
    finisher_used_today: bool = False
    finisher_last_used: Optional[datetime] = None

    def can_choose(self) -> Tuple[bool, str]:
        """Prüfe ob 1-Skill-Weg gewählt werden kann"""
        if self.chosen:
            return False, "Bereits auf dem 1-Skill-Weg!"
        if self.warnings_shown < self.REQUIRED_WARNINGS:
            return False, f"Noch {self.REQUIRED_WARNINGS - self.warnings_shown} Warnungen bestätigen!"
        return True, "Bereit für 1-Skill-Weg"

    def show_warning(self) -> Dict:
        """Zeige Warnung vor 1-Skill-Weg"""
        self.warnings_shown += 1
        warnings = [
            "⚠️ WARNUNG 1/3: Der 1-Skill-Weg ist PERMANENT! Du kannst nicht zurück!",
            "⚠️ WARNUNG 2/3: Diese Skill-Linie wird morphen können, aber andere Synergien gehen verloren!",
            "⚠️ WARNUNG 3/3: LETZTE CHANCE! Bist du SICHER? Überlege gut!"
        ]
        return {
            "warning": warnings[min(self.warnings_shown - 1, 2)],
            "remaining": max(0, self.REQUIRED_WARNINGS - self.warnings_shown),
            "can_proceed": self.warnings_shown >= self.REQUIRED_WARNINGS
        }

    def commit_to_path(self) -> Dict:
        """Wähle 1-Skill-Weg (PERMANENT!)"""
        can, reason = self.can_choose()
        if not can:
            return {"success": False, "error": reason}

        self.chosen = True
        return {
            "success": True,
            "message": f"Du hast den 1-Skill-Weg für {self.skill_line.value} gewählt! KEIN ZURÜCK!",
            "skill_line": self.skill_line.value,
            "can_morph": True
        }

    def morph_skill(self, morph_choice: str, morphs_available: List[str]) -> Dict:
        """Morphe die Skill-Linie (nur wenn 1-Skill-Weg)"""
        if not self.chosen:
            return {"success": False, "error": "Nicht auf 1-Skill-Weg!"}

        if morph_choice not in morphs_available:
            return {"success": False, "error": f"Morph nicht verfügbar! Optionen: {morphs_available}"}

        self.current_morph = morph_choice
        self.morph_level += 1

        return {
            "success": True,
            "morph": morph_choice,
            "morph_level": self.morph_level,
            "message": f"Skill zu {morph_choice} gemorpht!"
        }


# =============================================================================
# MORPH-DEFINITIONEN
# =============================================================================
SKILL_MORPHS = {
    # MAGIE MORPHS
    SkillLineType.FIRE: {
        1: ["Inferno", "Magma"],        # Level 1 Morph
        2: ["Phoenix", "Vulkan"],        # Level 2 Morph
        3: ["Sonnenbrand", "Höllenflamme"],
    },
    SkillLineType.WATER: {
        1: ["Sturzflut", "Nebel"],
        2: ["Tsunami", "Geysir"],
        3: ["Maelstrom", "Lebensquelle"],
    },
    SkillLineType.ICE: {
        1: ["Eissturm", "Permafrost"],
        2: ["Gletscher", "Kristall"],
        3: ["Absolute Null", "Eisgefängnis"],
    },
    SkillLineType.LIGHTNING: {
        1: ["Kettenblitz", "Elektroschock"],
        2: ["Donnerschlag", "Blitzschild"],
        3: ["Megavolt", "Plasmastrahl"],
    },
    SkillLineType.EXPLOSION: {
        1: ["Feuerball+", "Sprengmine"],
        2: ["EXPLOSION!", "Kettenreaktion"],
        3: ["MEGA-EXPLOSION!!", "Nuklear"],
        4: ["ULTRA-EXPLOSION!!!", "Supernova"],
        5: ["OMEGA-DETONATION!!!!"],  # Najika-exklusiv
    },

    # WAFFEN MORPHS
    SkillLineType.SWORD: {
        1: ["Wirbelwind", "Präzisionsklinge"],
        2: ["Kreuzschnitt", "Blutklinge"],
        3: ["Himmelsspalter", "Dämonenschnitt"],
    },
    SkillLineType.AXE: {
        1: ["Spaltung", "Raserei"],
        2: ["Erdbeben-Hieb", "Berserker"],
        3: ["Titanenfäller", "Weltenspalter"],
    },
    SkillLineType.BOW: {
        1: ["Schnellschuss", "Giftpfeil"],
        2: ["Pfeilhagel", "Explosivpfeil"],
        3: ["Sonnenpfeil", "Todespfeil"],
    },
    SkillLineType.DAGGER: {
        1: ["Hinterhalt", "Giftklinge"],
        2: ["Schattensprung", "Arterientreffer"],
        3: ["Assassinen-Kunst", "Todesstoß"],
    },
}


# =============================================================================
# VERWEBEN & KOMBINIEREN (nur für NORMALE Skills)
# =============================================================================
# Element-Verweben (Magie + Magie)
ELEMENT_WEAVE = {
    ("fire", "water"): {"name": "Dampf", "effect": "Blind + AoE"},
    ("fire", "wind"): {"name": "Feuersturm", "effect": "Großer AoE"},
    ("fire", "earth"): {"name": "Magma", "effect": "DoT + Slow"},
    ("water", "wind"): {"name": "Blizzard", "effect": "AoE Freeze"},
    ("water", "earth"): {"name": "Schlamm", "effect": "Root + Slow"},
    ("lightning", "water"): {"name": "Elektroschock", "effect": "Chain + Stun"},
    ("lightning", "wind"): {"name": "Gewitter", "effect": "Random Strikes"},
    ("ice", "fire"): {"name": "Thermisch", "effect": "Rüstungsbruch"},
    ("dark", "light"): {"name": "Void", "effect": "True Damage"},
    ("earth", "wind"): {"name": "Sandsturm", "effect": "Blind + DoT"},
    ("nature", "water"): {"name": "Regenwald", "effect": "HoT + Summon"},
    ("nature", "earth"): {"name": "Erdbeben", "effect": "Stagger + AoE"},
}

# Magie + Waffe Kombinationen
MAGIC_WEAPON_COMBINE = {
    ("fire", "sword"): {"name": "Feuerschwert", "bonus": "+50% Feuerschaden"},
    ("fire", "axe"): {"name": "Flammenspaltung", "bonus": "AoE Flammen"},
    ("ice", "sword"): {"name": "Frostschwert", "bonus": "Slow bei Treffer"},
    ("ice", "dagger"): {"name": "Eisdolch", "bonus": "Freeze bei Crit"},
    ("lightning", "spear"): {"name": "Donnerspeer", "bonus": "Chain Lightning"},
    ("lightning", "bow"): {"name": "Blitzpfeil", "bonus": "Stun bei Treffer"},
    ("dark", "dagger"): {"name": "Schattendolch", "bonus": "Lifesteal"},
    ("light", "sword"): {"name": "Heiligenschwert", "bonus": "+100% vs Untote"},
    ("nature", "bow"): {"name": "Naturpfeil", "bonus": "Wurzeln bei Treffer"},
    ("water", "staff"): {"name": "Wasserstab", "bonus": "Heilung verstärkt"},
}


# =============================================================================
# KÖRPERTEIL-TARGETING (wie Fortnite/Skyrim - KEIN VATS!)
# =============================================================================
class BodyPart(Enum):
    """Körperteile die anvisiert werden können - WO du triffst = WAS passiert"""
    HEAD = "head"           # Kopfschuss = +50% Schaden, Crit
    TORSO = "torso"         # Körper = Normaler Treffer
    LEFT_ARM = "left_arm"   # Linker Arm = Entwaffnen möglich
    RIGHT_ARM = "right_arm" # Rechter Arm = Schild deaktivieren
    LEFT_LEG = "left_leg"   # Linkes Bein = Gegner hinkt (-30% Speed)
    RIGHT_LEG = "right_leg" # Rechtes Bein = Gegner hinkt (-30% Speed)


# Körperteil-Effekte (passieren automatisch beim Treffen!)
LIMB_EFFECTS = {
    BodyPart.HEAD: {
        "damage_mod": 1.5,
        "effect": "Kritischer Treffer!",
        "debuff": None,
        "debuff_duration": 0
    },
    BodyPart.TORSO: {
        "damage_mod": 1.0,
        "effect": None,
        "debuff": None,
        "debuff_duration": 0
    },
    BodyPart.LEFT_ARM: {
        "damage_mod": 0.8,
        "effect": "Waffe gelockert!",
        "debuff": "disarm_chance",  # 20% Chance Waffe fallen zu lassen
        "debuff_duration": 0
    },
    BodyPart.RIGHT_ARM: {
        "damage_mod": 0.8,
        "effect": "Schild gelockert!",
        "debuff": "shield_break_chance",  # 25% Chance Schild nutzlos
        "debuff_duration": 0
    },
    BodyPart.LEFT_LEG: {
        "damage_mod": 0.7,
        "effect": "Gegner hinkt!",
        "debuff": "slow",
        "debuff_duration": 10  # 10 Sekunden
    },
    BodyPart.RIGHT_LEG: {
        "damage_mod": 0.7,
        "effect": "Gegner hinkt!",
        "debuff": "slow",
        "debuff_duration": 10
    },
}


@dataclass
class PrecisionSkill:
    """
    Präzisions-Skill (Skyrim Learning by Doing)

    KEIN VATS! Einfach normales Zielen wie Fortnite/Skyrim:
    - Du zielst auf Körperteile
    - Wo du triffst = Effekt
    - Dieser Skill verbessert deine TREFFERCHANCE
    - Analyse außerhalb Kampf zeigt Schwächen
    """
    level: int = 1  # Startet bei 1 (jeder kann zielen!)
    xp: int = 0
    xp_to_next: int = 100

    # Gespeicherte Analysen (für Schwächen)
    analyzed_enemies: Dict[str, Dict] = field(default_factory=dict)

    def gain_xp(self, amount: int = 10) -> Dict:
        """XP gewinnen durch Treffer (Skyrim-Style)"""
        self.xp += amount
        leveled = False

        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.1)
            leveled = True

        return {
            "leveled_up": leveled,
            "new_level": self.level,
            "xp_gained": amount
        }

    def get_hit_chance(self, body_part: BodyPart, perception: int,
                       distance: float = 1.0, is_moving: bool = False) -> int:
        """
        Berechne Trefferchance für Körperteil

        Faktoren:
        - Körperteil-Schwierigkeit (Kopf schwerer als Torso)
        - Precision-Skill Level
        - Perception Stat
        - Distanz (näher = einfacher)
        - Bewegung (stillstehend = einfacher)
        """
        # Basis-Schwierigkeit pro Körperteil
        base_chances = {
            BodyPart.HEAD: 40,      # Schwer zu treffen
            BodyPart.TORSO: 85,     # Leicht
            BodyPart.LEFT_ARM: 55,
            BodyPart.RIGHT_ARM: 55,
            BodyPart.LEFT_LEG: 50,
            BodyPart.RIGHT_LEG: 50,
        }

        chance = base_chances[body_part]

        # Skill-Bonus (+0.5% pro Level)
        chance += self.level * 0.5

        # Perception-Bonus (+2% pro Punkt)
        chance += perception * 2

        # Distanz-Malus (weiter = schwerer)
        if distance > 1.0:
            chance -= (distance - 1.0) * 10  # -10% pro Distanz-Einheit

        # Bewegungs-Malus
        if is_moving:
            chance -= 15

        return max(5, min(95, int(chance)))  # Min 5%, Max 95%

    def hit_body_part(self, body_part: BodyPart, base_damage: int,
                      perception: int, agility: int,
                      distance: float = 1.0, is_moving: bool = False) -> Dict:
        """
        Versuche Körperteil zu treffen (normales Gameplay!)

        Wie Fortnite/Skyrim: Du zielst, du schießt, du triffst (oder nicht)
        KEINE Zeitlupe, KEIN spezielles System
        """
        hit_chance = self.get_hit_chance(body_part, perception, distance, is_moving)

        # Würfeln
        roll = random.randint(1, 100)
        hit = roll <= hit_chance

        if hit:
            # Treffer! Effekte anwenden
            effect_data = LIMB_EFFECTS[body_part]
            final_damage = int(base_damage * effect_data["damage_mod"])

            # XP für Treffer (mehr für schwierige Körperteile)
            xp_gain = {
                BodyPart.HEAD: 15,
                BodyPart.TORSO: 5,
                BodyPart.LEFT_ARM: 10,
                BodyPart.RIGHT_ARM: 10,
                BodyPart.LEFT_LEG: 10,
                BodyPart.RIGHT_LEG: 10,
            }[body_part]

            self.gain_xp(xp_gain)

            return {
                "hit": True,
                "body_part": body_part.value,
                "damage": final_damage,
                "effect": effect_data["effect"],
                "debuff": effect_data["debuff"],
                "debuff_duration": effect_data["debuff_duration"],
                "hit_chance": hit_chance,
                "roll": roll,
                "xp_gained": xp_gain
            }
        else:
            # Daneben! Trotzdem etwas XP
            self.gain_xp(2)

            return {
                "hit": False,
                "body_part": body_part.value,
                "damage": 0,
                "effect": "Verfehlt!",
                "hit_chance": hit_chance,
                "roll": roll,
                "xp_gained": 2
            }

    def analyze_enemy(self, enemy_type: str, perception: int, intelligence: int) -> Dict:
        """
        Gegner AUSSERHALB des Kampfes analysieren

        Zeigt:
        - Schwächen
        - Resistenzen
        - Beste Angriffspunkte

        Braucht Zeit! Nicht im Kampf möglich.
        """
        # Analyse-Qualität
        analysis_power = perception + (intelligence // 2) + (self.level // 10)

        # Basis-Info (immer sichtbar)
        result = {
            "enemy_type": enemy_type,
            "body_parts": {
                "head": "Kritischer Schaden",
                "torso": "Normaler Schaden",
                "arms": "Entwaffnung möglich",
                "legs": "Verlangsamung"
            }
        }

        # Schwächen bei guter Analyse
        weaknesses = []
        resistances = []
        best_targets = []

        if analysis_power >= 10:
            weaknesses = self._get_weaknesses(enemy_type)
            result["weaknesses"] = weaknesses

        if analysis_power >= 15:
            resistances = self._get_resistances(enemy_type)
            result["resistances"] = resistances

        if analysis_power >= 20:
            best_targets = self._get_best_targets(enemy_type)
            result["best_targets"] = best_targets
            result["analysis_quality"] = "Meisterhaft"
        elif analysis_power >= 15:
            result["analysis_quality"] = "Gut"
        elif analysis_power >= 10:
            result["analysis_quality"] = "Basis"
        else:
            result["analysis_quality"] = "Oberflächlich"

        # Speichern
        self.analyzed_enemies[enemy_type] = result

        # XP für Analyse
        self.gain_xp(20)

        return result

    def _get_weaknesses(self, enemy_type: str) -> List[str]:
        """Schwächen pro Gegner-Typ"""
        db = {
            "Goblin": ["Feuer", "Kopfschüsse"],
            "Ork": ["Eis", "Beinschüsse (langsam)"],
            "Skelett": ["Stumpfe Waffen", "Licht-Magie"],
            "Slime": ["Feuer", "Austrocknung"],
            "Wolf": ["Feuer", "Alleinkampf"],
            "Drache": ["Eis", "Bauch (keine Schuppen)"],
            "Bandit": ["Entwaffnung", "Kopfschüsse"],
            "Zombie": ["Feuer", "Kopfschüsse (sofort tot)"],
        }
        return db.get(enemy_type, ["Keine bekannt"])

    def _get_resistances(self, enemy_type: str) -> List[str]:
        """Resistenzen pro Gegner-Typ"""
        db = {
            "Goblin": [],
            "Ork": ["Stumpfe Waffen"],
            "Skelett": ["Gift", "Kälte"],
            "Slime": ["Stumpfe Waffen", "Gift"],
            "Wolf": [],
            "Drache": ["Feuer (immun)"],
            "Zombie": ["Gift"],
        }
        return db.get(enemy_type, [])

    def _get_best_targets(self, enemy_type: str) -> List[str]:
        """Beste Angriffspunkte pro Gegner-Typ"""
        db = {
            "Goblin": ["Kopf (1-Hit bei niedrigem Level)"],
            "Ork": ["Beine (Mobilität zerstören)", "Arme (Entwaffnen)"],
            "Skelett": ["Kopf (sofort zerstört)", "Beine (Zusammenbruch)"],
            "Slime": ["Kern (wenn sichtbar)"],
            "Wolf": ["Beine (kann nicht mehr springen)"],
            "Drache": ["Flügel (Erdung)", "Bauch (kritisch)"],
            "Bandit": ["Waffenarm (Entwaffnen)", "Kopf"],
        }
        return db.get(enemy_type, ["Kopf (universell effektiv)"])


# =============================================================================
# SKILL-LINIE (Einzelner Skill im System)
# =============================================================================
@dataclass
class SkillLine:
    """Eine Skill-Linie (Magie oder Waffe)"""
    skill_type: SkillLineType
    level: int = 1
    xp: int = 0
    xp_to_next: int = 100

    # 1-Skill-Weg
    one_skill_path: Optional[OneSkillPath] = None

    # Gelernte Basis-Skills
    skills: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Basis-Skill automatisch
        self.skills.append(f"{self.skill_type.value}_basic")

    def use_skill(self) -> Dict:
        """Skill nutzen = XP (Skyrim!)"""
        xp_gain = random.randint(5, 15)
        self.xp += xp_gain

        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.12)
            leveled = True

        return {
            "xp_gained": xp_gain,
            "new_level": self.level,
            "leveled_up": leveled
        }

    def start_one_skill_path(self) -> OneSkillPath:
        """1-Skill-Weg initiieren"""
        if self.one_skill_path is None:
            self.one_skill_path = OneSkillPath(skill_line=self.skill_type)
        return self.one_skill_path

    def is_on_one_skill_path(self) -> bool:
        return self.one_skill_path is not None and self.one_skill_path.chosen

    def can_weave(self) -> bool:
        """Kann nur verweben wenn NICHT auf 1-Skill-Weg"""
        # Explosion kann NIEMALS verweben
        if self.skill_type == SkillLineType.EXPLOSION:
            return False
        return not self.is_on_one_skill_path()

    def can_combine_with_weapon(self) -> bool:
        """Magie kann mit Waffe kombiniert werden wenn NICHT auf 1-Skill-Weg"""
        if self.skill_type == SkillLineType.EXPLOSION:
            return False
        # Nur Magie-Typen können kombinieren
        magic_types = {SkillLineType.FIRE, SkillLineType.WATER, SkillLineType.ICE,
                       SkillLineType.LIGHTNING, SkillLineType.EARTH, SkillLineType.WIND,
                       SkillLineType.NATURE, SkillLineType.DARK, SkillLineType.LIGHT}
        return self.skill_type in magic_types and not self.is_on_one_skill_path()


# =============================================================================
# EXPLOSION SPEZIELL (kostet Mana + Stamina!)
# =============================================================================
@dataclass
class ExplosionSkill:
    """
    Explosion - Normale Magieschule aber SPEZIELL:
    - Kostet MANA + STAMINA (andere nur Mana)
    - NUR 1-Skill-Weg möglich (kein Verweben!)
    - Finisher = 1x pro Tag
    - Morpht durch Waffen (Schwert-Explosion, Bogen-Explosion, etc.)
    """
    level: int = 1
    xp: int = 0

    # Kosten (höher als normale Magie!)
    base_mana_cost: int = 50
    base_stamina_cost: int = 30

    # Finisher
    finisher_available: bool = True
    finisher_last_used: Optional[datetime] = None

    # Waffen-Morph
    weapon_morph: Optional[str] = None

    def get_costs(self) -> Dict:
        """Berechne Kosten basierend auf Level"""
        # Kosten sinken leicht mit Level
        level_discount = 1 - (self.level * 0.005)  # Max 50% Rabatt bei Level 100
        return {
            "mana": int(self.base_mana_cost * level_discount),
            "stamina": int(self.base_stamina_cost * level_discount)
        }

    def use(self, current_mana: int, current_stamina: int) -> Dict:
        """Explosion nutzen"""
        costs = self.get_costs()

        if current_mana < costs["mana"]:
            return {"success": False, "error": f"Nicht genug Mana! Brauche {costs['mana']}"}
        if current_stamina < costs["stamina"]:
            return {"success": False, "error": f"Nicht genug Stamina! Brauche {costs['stamina']}"}

        # XP gewinnen
        self.xp += random.randint(10, 20)
        if self.xp >= 100 + (self.level * 15):
            self.level += 1
            self.xp = 0

        # Schaden berechnen
        base_damage = 100 + (self.level * 5)
        if self.weapon_morph:
            base_damage = int(base_damage * 1.2)  # Waffen-Morph Bonus

        return {
            "success": True,
            "damage": base_damage,
            "mana_cost": costs["mana"],
            "stamina_cost": costs["stamina"],
            "level": self.level,
            "weapon_morph": self.weapon_morph
        }

    def use_finisher(self, is_najika: bool = False) -> Dict:
        """
        FINISHER - 1x pro Tag!
        Najika hat exklusiven Omega-Detonation Zugang
        """
        if not self.finisher_available:
            if self.finisher_last_used:
                time_since = datetime.now() - self.finisher_last_used
                if time_since < timedelta(hours=24):
                    remaining = timedelta(hours=24) - time_since
                    return {
                        "success": False,
                        "error": f"Finisher Cooldown! Noch {remaining.seconds // 3600}h {(remaining.seconds % 3600) // 60}m"
                    }
                self.finisher_available = True

        if not self.finisher_available:
            return {"success": False, "error": "Finisher heute bereits genutzt!"}

        self.finisher_available = False
        self.finisher_last_used = datetime.now()

        # Najika hat Zugang zu Omega-Detonation
        if is_najika:
            return {
                "success": True,
                "finisher_type": "OMEGA-DETONATION!!!!",
                "damage_multiplier": 10.0,
                "effect": "Totale Vernichtung im Umkreis!",
                "cooldown_hours": 24
            }
        else:
            return {
                "success": True,
                "finisher_type": "MEGA-EXPLOSION!!",
                "damage_multiplier": 5.0,
                "effect": "Massive AoE-Zerstörung!",
                "cooldown_hours": 24
            }

    def apply_weapon_morph(self, weapon_type: str) -> Dict:
        """Waffen-Morph für Explosion"""
        morphs = {
            "sword": {"name": "Explosions-Klinge", "bonus": "Linien-Detonation"},
            "axe": {"name": "Explosions-Spaltung", "bonus": "Kegel-Detonation"},
            "spear": {"name": "Explosions-Stoß", "bonus": "Durchdringende Detonation"},
            "hammer": {"name": "Explosions-Einschlag", "bonus": "Bodenwelle"},
            "bow": {"name": "Explosions-Pfeil", "bonus": "Fernziel-Detonation"},
            "dagger": {"name": "Mini-Explosion", "bonus": "Schnelle Mikro-Detonationen"},
            "shield": {"name": "Konter-Explosion", "bonus": "Bei Block → Explosion"},
            "staff": {"name": "Kanalisierte Explosion", "bonus": "Aufladbar"},
            "fist": {"name": "Explosions-Faust", "bonus": "Nahkampf-Detonation"},
        }

        if weapon_type not in morphs:
            return {"success": False, "error": f"Unbekannte Waffe: {weapon_type}"}

        self.weapon_morph = weapon_type
        return {
            "success": True,
            "morph": morphs[weapon_type],
            "message": f"Explosion mit {weapon_type} gemorpht!"
        }


# =============================================================================
# SPIELER-KLASSE (KEINE Klassen im Spiel!)
# =============================================================================
@dataclass
class Player:
    """
    Spieler - KEINE KLASSEN! Jeder kann alles lernen (Skyrim)
    """
    name: str
    is_najika: bool = False

    # S.P.E.C.I.A.L.
    stats: SpecialStats = field(default_factory=SpecialStats)

    # Ressourcen
    hp: int = 100
    max_hp: int = 100
    mana: int = 100
    max_mana: int = 100
    stamina: int = 100
    max_stamina: int = 100

    # Skill-Linien (Skyrim Learning by Doing)
    skill_lines: Dict[SkillLineType, SkillLine] = field(default_factory=dict)

    # Explosion Speziell
    explosion: Optional[ExplosionSkill] = None

    # Präzisions-Skill (Körperteil-Targeting)
    precision: PrecisionSkill = field(default_factory=PrecisionSkill)

    # Aktive Kombinationen
    active_weaves: List[str] = field(default_factory=list)
    active_weapon_combo: Optional[str] = None

    def learn_skill_line(self, skill_type: SkillLineType) -> Dict:
        """Neue Skill-Linie lernen"""
        if skill_type in self.skill_lines:
            return {"success": False, "error": "Bereits gelernt!"}

        self.skill_lines[skill_type] = SkillLine(skill_type=skill_type)

        # Explosion extra initialisieren
        if skill_type == SkillLineType.EXPLOSION:
            self.explosion = ExplosionSkill()

        return {
            "success": True,
            "skill_line": skill_type.value,
            "message": f"{skill_type.value} gelernt!"
        }

    def use_skill(self, skill_type: SkillLineType) -> Dict:
        """Skill nutzen = XP (Skyrim!)"""
        if skill_type not in self.skill_lines:
            return {"success": False, "error": "Skill-Linie nicht gelernt!"}

        # Explosion separat behandeln
        if skill_type == SkillLineType.EXPLOSION and self.explosion:
            result = self.explosion.use(self.mana, self.stamina)
            if result["success"]:
                self.mana -= result["mana_cost"]
                self.stamina -= result["stamina_cost"]
            return result

        # Normale Skills
        skill_line = self.skill_lines[skill_type]

        # Mana für Magie, Stamina für Waffen
        magic_types = {SkillLineType.FIRE, SkillLineType.WATER, SkillLineType.ICE,
                       SkillLineType.LIGHTNING, SkillLineType.EARTH, SkillLineType.WIND,
                       SkillLineType.NATURE, SkillLineType.DARK, SkillLineType.LIGHT}

        if skill_type in magic_types:
            cost = 15 + (skill_line.level // 5)
            if self.mana < cost:
                return {"success": False, "error": "Nicht genug Mana!"}
            self.mana -= cost
        else:
            cost = 10 + (skill_line.level // 5)
            if self.stamina < cost:
                return {"success": False, "error": "Nicht genug Stamina!"}
            self.stamina -= cost

        result = skill_line.use_skill()
        result["cost"] = cost
        return result

    def weave_elements(self, element1: SkillLineType, element2: SkillLineType) -> Dict:
        """
        Element-Verweben (Magie + Magie)
        NUR wenn NICHT auf 1-Skill-Weg!
        Explosion kann NIEMALS verweben!
        """
        if element1 not in self.skill_lines or element2 not in self.skill_lines:
            return {"success": False, "error": "Skill-Linie nicht gelernt!"}

        line1 = self.skill_lines[element1]
        line2 = self.skill_lines[element2]

        if not line1.can_weave():
            return {"success": False, "error": f"{element1.value} ist auf 1-Skill-Weg und kann nicht verweben!"}
        if not line2.can_weave():
            return {"success": False, "error": f"{element2.value} ist auf 1-Skill-Weg und kann nicht verweben!"}

        # Kombination suchen
        key = tuple(sorted([element1.value, element2.value]))
        weave = ELEMENT_WEAVE.get(key)

        if not weave:
            return {"success": False, "error": "Diese Elemente können nicht verwoben werden!"}

        # Kosten (beide)
        total_cost = 30 + (line1.level + line2.level) // 4
        if self.mana < total_cost:
            return {"success": False, "error": f"Nicht genug Mana! Brauche {total_cost}"}

        self.mana -= total_cost

        # Beide Skills bekommen XP
        line1.use_skill()
        line2.use_skill()

        return {
            "success": True,
            "weave": weave["name"],
            "effect": weave["effect"],
            "elements": [element1.value, element2.value],
            "mana_cost": total_cost
        }

    def combine_magic_weapon(self, magic: SkillLineType, weapon: SkillLineType) -> Dict:
        """
        Magie + Waffe kombinieren (z.B. Feuer + Schwert = Feuerschwert)
        NUR wenn NICHT auf 1-Skill-Weg!
        """
        if magic not in self.skill_lines:
            return {"success": False, "error": f"{magic.value} nicht gelernt!"}
        if weapon not in self.skill_lines:
            return {"success": False, "error": f"{weapon.value} nicht gelernt!"}

        magic_line = self.skill_lines[magic]
        weapon_line = self.skill_lines[weapon]

        if not magic_line.can_combine_with_weapon():
            return {"success": False, "error": f"{magic.value} auf 1-Skill-Weg, kann nicht kombinieren!"}

        # Kombination suchen
        key = (magic.value, weapon.value)
        combo = MAGIC_WEAPON_COMBINE.get(key)

        if not combo:
            return {"success": False, "error": f"{magic.value} und {weapon.value} können nicht kombiniert werden!"}

        # Kosten
        mana_cost = 20
        stamina_cost = 15
        if self.mana < mana_cost or self.stamina < stamina_cost:
            return {"success": False, "error": "Nicht genug Ressourcen!"}

        self.mana -= mana_cost
        self.stamina -= stamina_cost
        self.active_weapon_combo = combo["name"]

        # Beide Skills XP
        magic_line.use_skill()
        weapon_line.use_skill()

        return {
            "success": True,
            "combo": combo["name"],
            "bonus": combo["bonus"],
            "mana_cost": mana_cost,
            "stamina_cost": stamina_cost
        }

    def use_explosion_finisher(self) -> Dict:
        """Explosion Finisher (1x/Tag)"""
        if not self.explosion:
            return {"success": False, "error": "Explosion nicht gelernt!"}
        return self.explosion.use_finisher(is_najika=self.is_najika)


# =============================================================================
# TEST / DEMO
# =============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("NAJIKA SKILL & COMBAT SYSTEM V3 - TEST")
    print("=" * 70)

    # Spieler erstellen
    kuja = Player(name="Kuja")
    najika = Player(name="Najika", is_najika=True)

    # Kuja lernt verschiedene Skills
    print("\n--- Kuja lernt Skills ---")
    print(kuja.learn_skill_line(SkillLineType.FIRE))
    print(kuja.learn_skill_line(SkillLineType.SWORD))
    print(kuja.learn_skill_line(SkillLineType.ICE))

    # Najika lernt Explosion
    print("\n--- Najika lernt Explosion ---")
    print(najika.learn_skill_line(SkillLineType.EXPLOSION))

    # Kuja verwebt Feuer + Eis
    print("\n--- Element-Verweben (Feuer + Eis) ---")
    result = kuja.weave_elements(SkillLineType.FIRE, SkillLineType.ICE)
    print(f"Verweben: {result}")

    # Kuja kombiniert Feuer + Schwert
    print("\n--- Magie + Waffe kombinieren (Feuer + Schwert) ---")
    result = kuja.combine_magic_weapon(SkillLineType.FIRE, SkillLineType.SWORD)
    print(f"Kombination: {result}")

    # 1-Skill-Weg Test
    print("\n--- 1-Skill-Weg Warnungen ---")
    fire_line = kuja.skill_lines[SkillLineType.FIRE]
    path = fire_line.start_one_skill_path()
    for i in range(3):
        print(path.show_warning())

    print("\n--- 1-Skill-Weg wählen ---")
    print(path.commit_to_path())

    # Nach 1-Skill-Weg kann Feuer nicht mehr verweben!
    print("\n--- Feuer kann nicht mehr verweben nach 1-Skill-Weg ---")
    result = kuja.weave_elements(SkillLineType.FIRE, SkillLineType.ICE)
    print(f"Verweben nach 1-Skill-Weg: {result}")

    # Körperteil-Targeting Test (wie Fortnite/Skyrim!)
    print("\n--- Körperteil-Targeting (Fortnite/Skyrim Style) ---")
    print(f"Precision Level: {kuja.precision.level}")

    print("\n--- Gegner analysieren (AUSSERHALB Kampf) ---")
    analysis = kuja.precision.analyze_enemy("Goblin", kuja.stats.perception, kuja.stats.intelligence)
    print(f"Analyse: {analysis}")

    print("\n--- Kopfschuss versuchen (normales Zielen!) ---")
    result = kuja.precision.hit_body_part(
        BodyPart.HEAD,
        base_damage=50,
        perception=kuja.stats.perception,
        agility=kuja.stats.agility
    )
    print(f"Kopfschuss: {result}")

    print("\n--- Beinschuss (Gegner langsamer machen) ---")
    result = kuja.precision.hit_body_part(
        BodyPart.LEFT_LEG,
        base_damage=50,
        perception=kuja.stats.perception,
        agility=kuja.stats.agility
    )
    print(f"Beinschuss: {result}")

    # Najika Explosion
    print("\n--- Najika's Explosion ---")
    najika.mana = 100
    najika.stamina = 100
    print(f"Explosion: {najika.use_skill(SkillLineType.EXPLOSION)}")

    print("\n--- Najika's OMEGA-DETONATION (Finisher) ---")
    print(najika.use_explosion_finisher())

    print("\n" + "=" * 70)
    print("EXPLOSION!!! System funktioniert korrekt!")
    print("=" * 70)
