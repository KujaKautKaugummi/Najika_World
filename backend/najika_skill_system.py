"""
NAJIKA SKILL SYSTEM
===================
Komplettes Skill-System mit 10 Basis-Skills + Erweiterungsmöglichkeiten.
Integriert mit Equipment Combat, Temperatur-System und Monster-Attributen.

Skills haben:
- Mana-Kosten
- Cooldowns
- Element-Typen (für Resistenzen/Schwächen)
- Skalierung mit Stats (INT, STR, DEX)
- Visuelle Effekte
- Sound-IDs für Frontend

Erstellt: 2025-12-11
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Callable
import random
import math
import time

# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class Element(Enum):
    """Elementar-Typen für Skills und Monster"""
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    EARTH = "earth"
    WIND = "wind"
    WATER = "water"
    DARK = "dark"
    LIGHT = "light"
    PHYSICAL = "physical"
    HEALING = "healing"

class SkillType(Enum):
    """Skill-Kategorien"""
    ATTACK = "attack"        # Direkter Schaden
    MAGIC = "magic"          # Magischer Schaden
    HEAL = "heal"            # Heilung
    BUFF = "buff"            # Positive Effekte auf sich selbst/Verbündete
    DEBUFF = "debuff"        # Negative Effekte auf Gegner
    SUMMON = "summon"        # Beschwörungen
    UTILITY = "utility"      # Sonstige (Teleport, etc.)

class TargetType(Enum):
    """Ziel-Typen für Skills"""
    SELF = "self"
    SINGLE_ENEMY = "single_enemy"
    ALL_ENEMIES = "all_enemies"
    SINGLE_ALLY = "single_ally"
    ALL_ALLIES = "all_allies"
    AOE_GROUND = "aoe_ground"  # Fläche auf dem Boden

# Element-Stärken und Schwächen
ELEMENT_EFFECTIVENESS = {
    Element.FIRE: {Element.ICE: 1.5, Element.WATER: 0.5, Element.WIND: 1.2},
    Element.ICE: {Element.FIRE: 0.5, Element.WIND: 1.5, Element.EARTH: 1.2},
    Element.LIGHTNING: {Element.WATER: 2.0, Element.EARTH: 0.5, Element.WIND: 1.2},
    Element.EARTH: {Element.LIGHTNING: 1.5, Element.WIND: 0.5, Element.WATER: 1.2},
    Element.WIND: {Element.EARTH: 1.5, Element.ICE: 0.5, Element.FIRE: 1.2},
    Element.WATER: {Element.FIRE: 1.5, Element.LIGHTNING: 0.5, Element.EARTH: 1.2},
    Element.DARK: {Element.LIGHT: 1.5, Element.DARK: 0.5},
    Element.LIGHT: {Element.DARK: 1.5, Element.LIGHT: 0.5},
}

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class SkillEffect:
    """Effekt der durch einen Skill ausgelöst wird"""
    effect_type: str  # "damage", "heal", "dot", "hot", "buff", "debuff"
    value: float
    duration: float = 0  # In Sekunden, 0 = instant
    tick_interval: float = 1.0  # Für DoT/HoT
    stat_scaling: Dict[str, float] = field(default_factory=dict)  # z.B. {"INT": 0.5}

@dataclass
class Skill:
    """Einzelner Skill"""
    id: str
    name: str
    name_de: str
    description: str
    description_de: str
    skill_type: SkillType
    element: Element
    target_type: TargetType

    # Kosten & Cooldown
    mana_cost: int
    cooldown: float  # Sekunden
    stamina_cost: int = 0
    cast_time: float = 0  # Sekunden (0 = instant)

    # Effekte
    effects: List[SkillEffect] = field(default_factory=list)

    # Visuelles
    animation: str = "default"
    particle_effect: str = ""
    sound_id: str = ""
    icon: str = "⚔️"
    color: str = "#ffffff"

    # Anforderungen
    required_level: int = 1
    required_weapon: Optional[str] = None  # None = keine Anforderung

    # AOE
    aoe_radius: float = 0  # 0 = kein AOE

    # Spezial-Flags
    can_crit: bool = True
    ignores_defense: bool = False
    heals_on_hit: float = 0  # Leech-Prozent

@dataclass
class ActiveEffect:
    """Aktiver Buff/Debuff/DoT/HoT auf einer Entität"""
    skill_id: str
    effect_type: str
    value: float
    remaining_duration: float
    tick_interval: float
    last_tick: float
    source_id: str  # Wer hat den Effekt verursacht

@dataclass
class SkillInstance:
    """Gecooldownter Skill einer Entität"""
    skill: Skill
    current_cooldown: float = 0
    charges: int = 1
    max_charges: int = 1

# ============================================================
# SKILL DATABASE - 10 BASIS SKILLS
# ============================================================

SKILL_DATABASE: Dict[str, Skill] = {
    # ========== OFFENSIVE MAGIC ==========
    "fireball": Skill(
        id="fireball",
        name="Fireball",
        name_de="Feuerball",
        description="Hurl a blazing fireball at your enemy",
        description_de="Schleudere einen brennenden Feuerball auf deinen Feind",
        skill_type=SkillType.MAGIC,
        element=Element.FIRE,
        target_type=TargetType.SINGLE_ENEMY,
        mana_cost=25,
        cooldown=3.0,
        cast_time=0.8,
        effects=[
            SkillEffect("damage", 45, stat_scaling={"INT": 0.8}),
            SkillEffect("dot", 5, duration=4.0, tick_interval=1.0)  # Brennen
        ],
        animation="cast_fire",
        particle_effect="fire_explosion",
        sound_id="sfx_fireball",
        icon="🔥",
        color="#ff4400",
        aoe_radius=1.5,  # Kleiner Splash
    ),

    "ice_shard": Skill(
        id="ice_shard",
        name="Ice Shard",
        name_de="Eissplitter",
        description="Launch razor-sharp ice crystals that slow enemies",
        description_de="Schieße rasiermesserscharfe Eiskristalle die Feinde verlangsamen",
        skill_type=SkillType.MAGIC,
        element=Element.ICE,
        target_type=TargetType.SINGLE_ENEMY,
        mana_cost=20,
        cooldown=2.5,
        cast_time=0.5,
        effects=[
            SkillEffect("damage", 35, stat_scaling={"INT": 0.6}),
            SkillEffect("debuff", -0.3, duration=3.0)  # 30% Slow
        ],
        animation="cast_ice",
        particle_effect="ice_shatter",
        sound_id="sfx_ice",
        icon="❄️",
        color="#00ccff",
    ),

    "lightning_bolt": Skill(
        id="lightning_bolt",
        name="Lightning Bolt",
        name_de="Blitzschlag",
        description="Strike your foe with devastating lightning",
        description_de="Triff deinen Feind mit verheerendem Blitz",
        skill_type=SkillType.MAGIC,
        element=Element.LIGHTNING,
        target_type=TargetType.SINGLE_ENEMY,
        mana_cost=35,
        cooldown=5.0,
        cast_time=1.2,
        effects=[
            SkillEffect("damage", 80, stat_scaling={"INT": 1.2}),
            SkillEffect("debuff", 0, duration=1.0)  # 1s Stun
        ],
        animation="cast_lightning",
        particle_effect="lightning_strike",
        sound_id="sfx_thunder",
        icon="⚡",
        color="#ffff00",
        can_crit=True,
    ),

    "shadow_strike": Skill(
        id="shadow_strike",
        name="Shadow Strike",
        name_de="Schattenstoß",
        description="A quick dark-infused attack from the shadows",
        description_de="Ein schneller dunkel-durchdrungener Angriff aus den Schatten",
        skill_type=SkillType.ATTACK,
        element=Element.DARK,
        target_type=TargetType.SINGLE_ENEMY,
        mana_cost=15,
        stamina_cost=20,
        cooldown=4.0,
        cast_time=0,  # Instant
        effects=[
            SkillEffect("damage", 55, stat_scaling={"DEX": 0.9, "STR": 0.3}),
        ],
        animation="dash_attack",
        particle_effect="shadow_trail",
        sound_id="sfx_slash",
        icon="🌑",
        color="#4a0080",
        required_weapon="dagger",
        heals_on_hit=0.1,  # 10% Lifesteal
    ),

    "holy_smite": Skill(
        id="holy_smite",
        name="Holy Smite",
        name_de="Heiliger Zorn",
        description="Call down divine light to smite unholy creatures",
        description_de="Rufe göttliches Licht herbei um unheilige Kreaturen zu vernichten",
        skill_type=SkillType.MAGIC,
        element=Element.LIGHT,
        target_type=TargetType.AOE_GROUND,
        mana_cost=40,
        cooldown=8.0,
        cast_time=1.5,
        effects=[
            SkillEffect("damage", 60, stat_scaling={"INT": 1.0}),
        ],
        animation="cast_holy",
        particle_effect="light_pillar",
        sound_id="sfx_holy",
        icon="✨",
        color="#ffffaa",
        aoe_radius=3.0,
    ),

    # ========== HEALING ==========
    "heal": Skill(
        id="heal",
        name="Heal",
        name_de="Heilung",
        description="Restore health to yourself or an ally",
        description_de="Stelle Gesundheit bei dir oder einem Verbündeten wieder her",
        skill_type=SkillType.HEAL,
        element=Element.HEALING,
        target_type=TargetType.SINGLE_ALLY,
        mana_cost=30,
        cooldown=6.0,
        cast_time=1.0,
        effects=[
            SkillEffect("heal", 50, stat_scaling={"INT": 0.7}),
        ],
        animation="cast_heal",
        particle_effect="healing_glow",
        sound_id="sfx_heal",
        icon="💚",
        color="#00ff88",
        can_crit=False,
    ),

    "regeneration": Skill(
        id="regeneration",
        name="Regeneration",
        name_de="Regeneration",
        description="Grant continuous healing over time",
        description_de="Gewähre kontinuierliche Heilung über Zeit",
        skill_type=SkillType.HEAL,
        element=Element.HEALING,
        target_type=TargetType.SINGLE_ALLY,
        mana_cost=25,
        cooldown=12.0,
        cast_time=0.5,
        effects=[
            SkillEffect("hot", 10, duration=10.0, tick_interval=2.0, stat_scaling={"INT": 0.3}),
        ],
        animation="cast_buff",
        particle_effect="healing_sparkles",
        sound_id="sfx_buff",
        icon="💖",
        color="#ff88cc",
        can_crit=False,
    ),

    # ========== BUFFS ==========
    "battle_cry": Skill(
        id="battle_cry",
        name="Battle Cry",
        name_de="Kampfschrei",
        description="Boost attack power for a short duration",
        description_de="Erhöhe die Angriffskraft für kurze Zeit",
        skill_type=SkillType.BUFF,
        element=Element.PHYSICAL,
        target_type=TargetType.SELF,
        mana_cost=20,
        stamina_cost=15,
        cooldown=20.0,
        cast_time=0.3,
        effects=[
            SkillEffect("buff", 0.25, duration=15.0),  # +25% ATK
        ],
        animation="roar",
        particle_effect="power_aura",
        sound_id="sfx_roar",
        icon="💪",
        color="#ff8800",
        can_crit=False,
    ),

    "ice_armor": Skill(
        id="ice_armor",
        name="Ice Armor",
        name_de="Eispanzer",
        description="Surround yourself with protective ice",
        description_de="Umgib dich mit schützendem Eis",
        skill_type=SkillType.BUFF,
        element=Element.ICE,
        target_type=TargetType.SELF,
        mana_cost=35,
        cooldown=30.0,
        cast_time=1.0,
        effects=[
            SkillEffect("buff", 0.30, duration=20.0),  # +30% DEF
            SkillEffect("buff", 0.50, duration=20.0),  # +50% Ice Resist
        ],
        animation="cast_ice",
        particle_effect="ice_shield",
        sound_id="sfx_ice_armor",
        icon="🛡️",
        color="#aaeeff",
        can_crit=False,
    ),

    # ========== UTILITY ==========
    "wind_dash": Skill(
        id="wind_dash",
        name="Wind Dash",
        name_de="Windstoß",
        description="Dash forward at high speed, evading attacks",
        description_de="Stürme vorwärts mit hoher Geschwindigkeit und weiche Angriffen aus",
        skill_type=SkillType.UTILITY,
        element=Element.WIND,
        target_type=TargetType.SELF,
        mana_cost=15,
        stamina_cost=25,
        cooldown=8.0,
        cast_time=0,
        effects=[
            SkillEffect("buff", 1.0, duration=0.5),  # 0.5s Invincibility
        ],
        animation="dash",
        particle_effect="wind_trail",
        sound_id="sfx_whoosh",
        icon="💨",
        color="#aaffaa",
        can_crit=False,
    ),
}

# ============================================================
# SKILL SYSTEM CLASS
# ============================================================

class SkillSystem:
    """Hauptklasse für das Skill-System"""

    def __init__(self):
        self.skills = SKILL_DATABASE.copy()
        self.entity_skills: Dict[str, Dict[str, SkillInstance]] = {}  # entity_id -> skill_id -> instance
        self.active_effects: Dict[str, List[ActiveEffect]] = {}  # entity_id -> effects

    def register_entity(self, entity_id: str, skill_ids: List[str] = None):
        """Registriere eine Entität mit Skills"""
        self.entity_skills[entity_id] = {}
        self.active_effects[entity_id] = []

        if skill_ids:
            for skill_id in skill_ids:
                if skill_id in self.skills:
                    self.learn_skill(entity_id, skill_id)

    def learn_skill(self, entity_id: str, skill_id: str) -> bool:
        """Lerne einen neuen Skill"""
        if entity_id not in self.entity_skills:
            self.register_entity(entity_id)

        if skill_id not in self.skills:
            return False

        self.entity_skills[entity_id][skill_id] = SkillInstance(
            skill=self.skills[skill_id],
            current_cooldown=0,
            charges=1,
            max_charges=1
        )
        return True

    def can_use_skill(self, entity_id: str, skill_id: str,
                      current_mana: int, current_stamina: int,
                      entity_level: int = 1, equipped_weapon: str = None) -> tuple[bool, str]:
        """Prüfe ob ein Skill verwendet werden kann"""
        if entity_id not in self.entity_skills:
            return False, "Entity nicht registriert"

        if skill_id not in self.entity_skills[entity_id]:
            return False, "Skill nicht gelernt"

        instance = self.entity_skills[entity_id][skill_id]
        skill = instance.skill

        if instance.current_cooldown > 0:
            return False, f"Cooldown: {instance.current_cooldown:.1f}s"

        if current_mana < skill.mana_cost:
            return False, f"Nicht genug Mana ({current_mana}/{skill.mana_cost})"

        if current_stamina < skill.stamina_cost:
            return False, f"Nicht genug Stamina ({current_stamina}/{skill.stamina_cost})"

        if entity_level < skill.required_level:
            return False, f"Level zu niedrig ({entity_level}/{skill.required_level})"

        if skill.required_weapon and equipped_weapon != skill.required_weapon:
            return False, f"Benötigt Waffe: {skill.required_weapon}"

        return True, "OK"

    def use_skill(self, entity_id: str, skill_id: str,
                  caster_stats: Dict[str, int],
                  target_ids: List[str] = None,
                  target_element: Element = None) -> Dict:
        """
        Verwende einen Skill und berechne die Effekte.

        Returns dict mit:
        - success: bool
        - effects: List der angewandten Effekte
        - mana_cost: int
        - stamina_cost: int
        - cooldown: float
        - animation: str
        - particle_effect: str
        - sound_id: str
        """
        if entity_id not in self.entity_skills:
            return {"success": False, "error": "Entity nicht registriert"}

        if skill_id not in self.entity_skills[entity_id]:
            return {"success": False, "error": "Skill nicht gelernt"}

        instance = self.entity_skills[entity_id][skill_id]
        skill = instance.skill

        # Setze Cooldown
        instance.current_cooldown = skill.cooldown

        # Berechne Effekte
        results = []
        for effect in skill.effects:
            value = effect.value

            # Stat Scaling
            for stat, scaling in effect.stat_scaling.items():
                if stat in caster_stats:
                    value += caster_stats[stat] * scaling

            # Element Effectiveness
            if target_element and skill.element in ELEMENT_EFFECTIVENESS:
                effectiveness = ELEMENT_EFFECTIVENESS[skill.element].get(target_element, 1.0)
                value *= effectiveness

            # Crit Check
            crit = False
            if skill.can_crit:
                crit_chance = caster_stats.get("CRIT", 5) / 100
                if random.random() < crit_chance:
                    crit = True
                    value *= 1.5 + (caster_stats.get("CRIT_DMG", 50) / 100)

            results.append({
                "type": effect.effect_type,
                "value": round(value, 1),
                "duration": effect.duration,
                "tick_interval": effect.tick_interval,
                "crit": crit,
            })

            # Füge DoT/HoT/Buff/Debuff zu aktiven Effekten hinzu
            if effect.duration > 0 and target_ids:
                for target_id in target_ids:
                    if target_id not in self.active_effects:
                        self.active_effects[target_id] = []

                    self.active_effects[target_id].append(ActiveEffect(
                        skill_id=skill_id,
                        effect_type=effect.effect_type,
                        value=value,
                        remaining_duration=effect.duration,
                        tick_interval=effect.tick_interval,
                        last_tick=time.time(),
                        source_id=entity_id
                    ))

        return {
            "success": True,
            "skill_name": skill.name_de,
            "effects": results,
            "mana_cost": skill.mana_cost,
            "stamina_cost": skill.stamina_cost,
            "cooldown": skill.cooldown,
            "cast_time": skill.cast_time,
            "animation": skill.animation,
            "particle_effect": skill.particle_effect,
            "sound_id": skill.sound_id,
            "icon": skill.icon,
            "color": skill.color,
            "aoe_radius": skill.aoe_radius,
            "heals_on_hit": skill.heals_on_hit,
        }

    def update_cooldowns(self, entity_id: str, delta_time: float):
        """Update Cooldowns für eine Entität"""
        if entity_id not in self.entity_skills:
            return

        for skill_id, instance in self.entity_skills[entity_id].items():
            if instance.current_cooldown > 0:
                instance.current_cooldown = max(0, instance.current_cooldown - delta_time)

    def update_effects(self, entity_id: str, delta_time: float) -> List[Dict]:
        """
        Update aktive Effekte und gebe Tick-Ergebnisse zurück.
        Returns Liste von {type, value} für jeden Tick.
        """
        if entity_id not in self.active_effects:
            return []

        results = []
        current_time = time.time()
        remaining_effects = []

        for effect in self.active_effects[entity_id]:
            # Reduziere Duration
            effect.remaining_duration -= delta_time

            # Check für Tick
            if current_time - effect.last_tick >= effect.tick_interval:
                effect.last_tick = current_time
                results.append({
                    "type": effect.effect_type,
                    "value": effect.value,
                    "source": effect.source_id,
                })

            # Behalte wenn noch aktiv
            if effect.remaining_duration > 0:
                remaining_effects.append(effect)

        self.active_effects[entity_id] = remaining_effects
        return results

    def get_entity_skills(self, entity_id: str) -> List[Dict]:
        """Hole alle Skills einer Entität als Liste"""
        if entity_id not in self.entity_skills:
            return []

        skills = []
        for skill_id, instance in self.entity_skills[entity_id].items():
            skill = instance.skill
            skills.append({
                "id": skill.id,
                "name": skill.name,
                "name_de": skill.name_de,
                "description_de": skill.description_de,
                "icon": skill.icon,
                "color": skill.color,
                "mana_cost": skill.mana_cost,
                "stamina_cost": skill.stamina_cost,
                "cooldown": skill.cooldown,
                "current_cooldown": instance.current_cooldown,
                "element": skill.element.value,
                "type": skill.skill_type.value,
            })
        return skills

    def get_active_effects_summary(self, entity_id: str) -> List[Dict]:
        """Hole Zusammenfassung aktiver Effekte"""
        if entity_id not in self.active_effects:
            return []

        return [{
            "skill_id": e.skill_id,
            "type": e.effect_type,
            "remaining": round(e.remaining_duration, 1),
        } for e in self.active_effects[entity_id]]

# ============================================================
# SKILL PRESET LOADOUTS
# ============================================================

PRESET_LOADOUTS = {
    "mage": ["fireball", "ice_shard", "lightning_bolt", "heal"],
    "warrior": ["battle_cry", "shadow_strike", "wind_dash", "regeneration"],
    "paladin": ["holy_smite", "heal", "battle_cry", "ice_armor"],
    "rogue": ["shadow_strike", "wind_dash", "ice_shard", "regeneration"],
    "balanced": ["fireball", "heal", "battle_cry", "wind_dash"],
}

# ============================================================
# API ENDPOINTS (für Integration mit Flask/FastAPI)
# ============================================================

# Globale Instanz
skill_system = SkillSystem()

def get_all_skills() -> List[Dict]:
    """Hole alle verfügbaren Skills"""
    return [{
        "id": s.id,
        "name": s.name,
        "name_de": s.name_de,
        "description_de": s.description_de,
        "icon": s.icon,
        "color": s.color,
        "element": s.element.value,
        "type": s.skill_type.value,
        "mana_cost": s.mana_cost,
        "stamina_cost": s.stamina_cost,
        "cooldown": s.cooldown,
        "required_level": s.required_level,
    } for s in SKILL_DATABASE.values()]

def get_skill_info(skill_id: str) -> Optional[Dict]:
    """Hole detaillierte Info zu einem Skill"""
    if skill_id not in SKILL_DATABASE:
        return None

    s = SKILL_DATABASE[skill_id]
    return {
        "id": s.id,
        "name": s.name,
        "name_de": s.name_de,
        "description": s.description,
        "description_de": s.description_de,
        "icon": s.icon,
        "color": s.color,
        "element": s.element.value,
        "type": s.skill_type.value,
        "target_type": s.target_type.value,
        "mana_cost": s.mana_cost,
        "stamina_cost": s.stamina_cost,
        "cooldown": s.cooldown,
        "cast_time": s.cast_time,
        "required_level": s.required_level,
        "required_weapon": s.required_weapon,
        "aoe_radius": s.aoe_radius,
        "effects": [{
            "type": e.effect_type,
            "value": e.value,
            "duration": e.duration,
            "scaling": e.stat_scaling,
        } for e in s.effects],
    }

def get_presets() -> Dict[str, List[str]]:
    """Hole vorgefertigte Skill-Loadouts"""
    return PRESET_LOADOUTS

# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    print("=== NAJIKA SKILL SYSTEM TEST ===\n")

    # Erstelle System
    system = SkillSystem()

    # Registriere Spieler mit Mage-Loadout
    system.register_entity("player1", PRESET_LOADOUTS["mage"])

    # Zeige Skills
    print("Spieler-Skills:")
    for skill in system.get_entity_skills("player1"):
        print(f"  {skill['icon']} {skill['name_de']} - {skill['mana_cost']} MP, {skill['cooldown']}s CD")

    print("\n--- Verwende Fireball ---")
    result = system.use_skill(
        "player1",
        "fireball",
        caster_stats={"INT": 50, "CRIT": 15, "CRIT_DMG": 75},
        target_ids=["enemy1"],
        target_element=Element.ICE  # 1.5x Schaden!
    )

    if result["success"]:
        print(f"✅ {result['skill_name']} verwendet!")
        print(f"   Mana: -{result['mana_cost']}")
        print(f"   Cooldown: {result['cooldown']}s")
        for eff in result["effects"]:
            crit_str = " 💥CRIT!" if eff.get("crit") else ""
            print(f"   → {eff['type']}: {eff['value']}{crit_str}")

    print("\n--- Verwende Heal ---")
    result = system.use_skill(
        "player1",
        "heal",
        caster_stats={"INT": 50},
        target_ids=["player1"]
    )

    if result["success"]:
        print(f"✅ {result['skill_name']} verwendet!")
        for eff in result["effects"]:
            print(f"   → +{eff['value']} HP")

    print("\n--- Alle Skills im Spiel ---")
    for skill in get_all_skills():
        print(f"{skill['icon']} {skill['name_de']:20} [{skill['element']:10}] {skill['mana_cost']:3} MP")

    print("\n✅ Skill System Test erfolgreich!")
