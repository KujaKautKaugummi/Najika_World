"""
NAJIKA PERK-SYSTEM V2
=====================
KEINE Perk-Punkte! Perks werden VERDIENT durch Spielen.

3 Quellen für Perks:
1. SKILL-MEILENSTEINE - Automatisch bei Level 10/25/50/75/100
2. SLIME-PERKS - Passive Boni durch Slime-Evolution
3. STORY-PERKS - Durch Oregon Trail Events (mit Konsequenzen!)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime


# =============================================================================
# 1. SKILL-MEILENSTEIN-BONI (automatisch beim Leveln)
# =============================================================================
@dataclass
class SkillMilestone:
    """Ein Meilenstein-Bonus der automatisch freigeschaltet wird"""
    level: int
    name: str
    description: str
    effect: Dict  # {"stat": "fire_damage", "modifier": 0.1} = +10%


# Meilensteine pro Skill-Linie
SKILL_MILESTONES = {
    # ===== FEUER-MAGIE =====
    "fire": [
        SkillMilestone(10, "Flammenresistenz", "Weniger Feuerschaden",
                       {"stat": "fire_resistance", "modifier": 0.1}),
        SkillMilestone(25, "Heißer Stahl", "Feuer-Waffen-Kombos stärker",
                       {"stat": "fire_weapon_combo", "modifier": 0.15}),
        SkillMilestone(50, "Phönix-Funken", "5% Chance bei Tod aufzustehen",
                       {"stat": "phoenix_chance", "modifier": 0.05}),
        SkillMilestone(75, "Inferno-Meister", "Feuer-Verweben stärker",
                       {"stat": "fire_weave", "modifier": 0.3}),
        SkillMilestone(100, "Avatar des Feuers", "Feuer-Aura schadet Gegnern",
                       {"stat": "fire_aura", "modifier": 5}),  # 5 DPS
    ],

    # ===== EIS-MAGIE =====
    "ice": [
        SkillMilestone(10, "Kälteresistenz", "Weniger Eisschaden",
                       {"stat": "ice_resistance", "modifier": 0.1}),
        SkillMilestone(25, "Frostbiss", "Eis-Attacken verlangsamen stärker",
                       {"stat": "ice_slow", "modifier": 0.2}),
        SkillMilestone(50, "Eiserner Wille", "Immun gegen Freeze",
                       {"stat": "freeze_immunity", "modifier": 1}),
        SkillMilestone(75, "Gletschermeister", "Eis-Verweben stärker",
                       {"stat": "ice_weave", "modifier": 0.3}),
        SkillMilestone(100, "Herz aus Eis", "Gegner in Nähe werden langsamer",
                       {"stat": "ice_aura", "modifier": 0.15}),
    ],

    # ===== BLITZ-MAGIE =====
    "lightning": [
        SkillMilestone(10, "Statische Ladung", "Weniger Blitzschaden",
                       {"stat": "lightning_resistance", "modifier": 0.1}),
        SkillMilestone(25, "Kettenblitz", "Blitz springt auf 1 extra Ziel",
                       {"stat": "chain_targets", "modifier": 1}),
        SkillMilestone(50, "Blitzreflexe", "+10% Ausweichen",
                       {"stat": "dodge", "modifier": 0.1}),
        SkillMilestone(75, "Donnergott", "Blitz-Stun dauert länger",
                       {"stat": "stun_duration", "modifier": 0.5}),
        SkillMilestone(100, "Lebender Blitz", "Chance Schaden zu ignorieren",
                       {"stat": "phase_chance", "modifier": 0.1}),
    ],

    # ===== EXPLOSION (1-Skill-Weg) =====
    "explosion": [
        SkillMilestone(10, "Stabiler Kern", "-10% Mana-Kosten",
                       {"stat": "explosion_mana_cost", "modifier": -0.1}),
        SkillMilestone(25, "Kettenreaktion", "15% Chance auf Mini-Explosion",
                       {"stat": "chain_explosion", "modifier": 0.15}),
        SkillMilestone(50, "EXPLOSION!", "Erste Morph-Wahl",
                       {"stat": "morph_unlock", "modifier": 1}),
        SkillMilestone(75, "Mega-Detonation", "+50% AoE-Radius",
                       {"stat": "aoe_radius", "modifier": 0.5}),
        SkillMilestone(100, "Explosions-Legende", "Finisher -6h Cooldown",
                       {"stat": "finisher_cooldown", "modifier": -6}),
    ],

    # ===== SCHWERT =====
    "sword": [
        SkillMilestone(10, "Schneller Hieb", "Sprint-Attacke +20% Schaden",
                       {"stat": "sprint_attack", "modifier": 0.2}),
        SkillMilestone(25, "Parade-Meister", "Perfekter Block = Stagger",
                       {"stat": "perfect_block_stagger", "modifier": 1}),
        SkillMilestone(50, "Kreuzschnitt", "Neue Kombo freigeschaltet",
                       {"stat": "combo_unlock", "modifier": 1}),
        SkillMilestone(75, "Klingentänzer", "Ausweichen während Angriff",
                       {"stat": "attack_dodge", "modifier": 1}),
        SkillMilestone(100, "Schwertmeister", "+25% Crit-Chance mit Schwert",
                       {"stat": "sword_crit", "modifier": 0.25}),
    ],

    # ===== BOGEN =====
    "bow": [
        SkillMilestone(10, "Ruhige Hand", "Weniger Spread",
                       {"stat": "accuracy", "modifier": 0.1}),
        SkillMilestone(25, "Schnellschuss", "Schneller nachladen",
                       {"stat": "reload_speed", "modifier": 0.2}),
        SkillMilestone(50, "Adlerauge", "Zoom beim Zielen",
                       {"stat": "zoom", "modifier": 1}),
        SkillMilestone(75, "Tödlicher Schuss", "+30% Headshot-Schaden",
                       {"stat": "headshot_damage", "modifier": 0.3}),
        SkillMilestone(100, "Legendärer Schütze", "Pfeile durchdringen",
                       {"stat": "pierce", "modifier": 1}),
    ],

    # ===== PRÄZISION (Körperteil-Targeting) =====
    "precision": [
        SkillMilestone(10, "Scharfes Auge", "+5% Trefferchance",
                       {"stat": "hit_chance", "modifier": 0.05}),
        SkillMilestone(25, "Anatom", "Analyse zeigt mehr Infos",
                       {"stat": "analysis_bonus", "modifier": 1}),
        SkillMilestone(50, "Präziser Schlag", "Arm/Bein-Effekte +25%",
                       {"stat": "limb_effect", "modifier": 0.25}),
        SkillMilestone(75, "Chirurg", "Kopfschüsse +20% extra Schaden",
                       {"stat": "headshot_bonus", "modifier": 0.2}),
        SkillMilestone(100, "Meister-Scharfschütze", "Kein Miss unter 50% Chance",
                       {"stat": "guaranteed_hit_threshold", "modifier": 50}),
    ],

    # ===== SCHMIEDEN =====
    "smithing": [
        SkillMilestone(10, "Lehrling", "Stahl-Ausrüstung",
                       {"stat": "craft_steel", "modifier": 1}),
        SkillMilestone(25, "Geselle", "Orichalcum-Ausrüstung",
                       {"stat": "craft_orichalcum", "modifier": 1}),
        SkillMilestone(50, "Meister", "Mithril-Ausrüstung",
                       {"stat": "craft_mithril", "modifier": 1}),
        SkillMilestone(75, "Großmeister", "Legendäre Ausrüstung",
                       {"stat": "craft_legendary", "modifier": 1}),
        SkillMilestone(100, "Göttlicher Schmied", "Epische Ausrüstung + Boni",
                       {"stat": "craft_epic", "modifier": 1}),
    ],

    # ===== ALCHEMIE =====
    "alchemy": [
        SkillMilestone(10, "Kräuterkenner", "Mehr Kräuter finden",
                       {"stat": "herb_find", "modifier": 0.2}),
        SkillMilestone(25, "Braumeister", "Tränke +25% Effekt",
                       {"stat": "potion_effect", "modifier": 0.25}),
        SkillMilestone(50, "Giftmischer", "Gifte dauern länger",
                       {"stat": "poison_duration", "modifier": 0.5}),
        SkillMilestone(75, "Alchemist", "2 Effekte kombinieren",
                       {"stat": "dual_effect", "modifier": 1}),
        SkillMilestone(100, "Großer Alchemist", "Perfekte Qualität immer",
                       {"stat": "perfect_quality", "modifier": 1}),
    ],
}


def get_unlocked_milestones(skill_name: str, skill_level: int) -> List[SkillMilestone]:
    """Hole alle freigeschalteten Meilensteine für einen Skill"""
    if skill_name not in SKILL_MILESTONES:
        return []

    return [m for m in SKILL_MILESTONES[skill_name] if m.level <= skill_level]


# =============================================================================
# 2. SLIME-PERKS (passive Boni durch Evolution)
# =============================================================================
class SlimeEvolution(Enum):
    """Slime-Evolutionsstufen"""
    EGG = 0
    BABY = 1
    KIND = 2
    REIF = 3
    CHAMPION = 4
    ULTIMATIV = 5


@dataclass
class SlimePerk:
    """Ein Perk den ein Slime seinem Besitzer gibt"""
    evolution_required: SlimeEvolution
    name: str
    description: str
    effect: Dict


# Slime-Perks pro Slime-Typ
SLIME_PERKS = {
    # ===== MOOS-SCHLEIM (Samtmoos-Tiefwald) =====
    "moos": [
        SlimePerk(SlimeEvolution.BABY, "Naturfreund", "+5% Kräuter finden",
                  {"stat": "herb_find", "modifier": 0.05}),
        SlimePerk(SlimeEvolution.KIND, "Waldläufer", "Kein Verirren im Wald",
                  {"stat": "forest_navigation", "modifier": 1}),
        SlimePerk(SlimeEvolution.REIF, "Gift-Resistenz", "-20% Giftschaden",
                  {"stat": "poison_resistance", "modifier": 0.2}),
        SlimePerk(SlimeEvolution.CHAMPION, "Regeneration", "+10% HP-Regen",
                  {"stat": "hp_regen", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Eins mit Natur", "Tiere greifen nicht an",
                  {"stat": "animal_peace", "modifier": 1}),
    ],

    # ===== MAGMA-SCHLEIM (Magmaströme) =====
    "magma": [
        SlimePerk(SlimeEvolution.BABY, "Wärme", "Kein Kälteschaden durch Wetter",
                  {"stat": "cold_weather_immunity", "modifier": 1}),
        SlimePerk(SlimeEvolution.KIND, "Feuerschutz", "-15% Feuerschaden",
                  {"stat": "fire_resistance", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.REIF, "Schmelzpanzer", "+10% Rüstung",
                  {"stat": "armor", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.CHAMPION, "Lava-Blut", "Angreifer nehmen 5 Schaden",
                  {"stat": "thorns", "modifier": 5}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Vulkan-Herz", "Explosion +20%",
                  {"stat": "explosion_damage", "modifier": 0.2}),
    ],

    # ===== FROST-SCHLEIM (Reich der Drei) =====
    "frost": [
        SlimePerk(SlimeEvolution.BABY, "Kühle", "Kein Hitzeschaden durch Wetter",
                  {"stat": "heat_weather_immunity", "modifier": 1}),
        SlimePerk(SlimeEvolution.KIND, "Eisschild", "-15% Eisschaden",
                  {"stat": "ice_resistance", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.REIF, "Gefrorener Kern", "+10% Eis-Schaden",
                  {"stat": "ice_damage", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.CHAMPION, "Frostbiss", "Angriffe verlangsamen",
                  {"stat": "attack_slow", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Eiskönig", "Freeze-Chance bei Crit",
                  {"stat": "crit_freeze", "modifier": 0.15}),
    ],

    # ===== BLITZ-SCHLEIM (Blitzebene) =====
    "blitz": [
        SlimePerk(SlimeEvolution.BABY, "Statisch", "Kleine Elektro-Resistenz",
                  {"stat": "lightning_resistance", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.KIND, "Schnell", "+5% Bewegung",
                  {"stat": "movement_speed", "modifier": 0.05}),
        SlimePerk(SlimeEvolution.REIF, "Blitzschnell", "+10% Angriffstempo",
                  {"stat": "attack_speed", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.CHAMPION, "Donnerherz", "Blitz-Schaden +15%",
                  {"stat": "lightning_damage", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Lebender Blitz", "Teleport-Dash",
                  {"stat": "lightning_dash", "modifier": 1}),
    ],

    # ===== KRISTALL-SCHLEIM (Tiefenhöhlen) =====
    "kristall": [
        SlimePerk(SlimeEvolution.BABY, "Glitzern", "+10% Gold finden",
                  {"stat": "gold_find", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.KIND, "Edelstein-Spürer", "Seltene Erze markiert",
                  {"stat": "ore_detection", "modifier": 1}),
        SlimePerk(SlimeEvolution.REIF, "Harter Kern", "+15% Stagger-Resist",
                  {"stat": "stagger_resistance", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.CHAMPION, "Prisma", "Licht-Magie +15%",
                  {"stat": "light_damage", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Diamant-Seele", "1x Tod überleben/Tag",
                  {"stat": "death_save", "modifier": 1}),
    ],

    # ===== GIFT-SCHLEIM (Grünschlamm-Sumpf) =====
    "gift": [
        SlimePerk(SlimeEvolution.BABY, "Giftresistent", "+10% Gift-Resist",
                  {"stat": "poison_resistance", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.KIND, "Toxisch", "Angriffe vergiften leicht",
                  {"stat": "poison_on_hit", "modifier": 0.05}),
        SlimePerk(SlimeEvolution.REIF, "Säure", "+15% Gift-Schaden",
                  {"stat": "poison_damage", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.CHAMPION, "Miasma", "Gift-Aura um dich",
                  {"stat": "poison_aura", "modifier": 3}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Giftmeister", "Immun gegen Gift",
                  {"stat": "poison_immunity", "modifier": 1}),
    ],

    # ===== SAND-SCHLEIM (Heiße Dünen) =====
    "sand": [
        SlimePerk(SlimeEvolution.BABY, "Wüstenblut", "Weniger Durst",
                  {"stat": "thirst_reduction", "modifier": 0.2}),
        SlimePerk(SlimeEvolution.KIND, "Sandläufer", "Kein Slow auf Sand",
                  {"stat": "sand_immunity", "modifier": 1}),
        SlimePerk(SlimeEvolution.REIF, "Tarnung", "+15% Stealth in Wüste",
                  {"stat": "desert_stealth", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.CHAMPION, "Sandsturm", "Blind-Chance bei Angriff",
                  {"stat": "blind_on_hit", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Herr der Dünen", "Sandwurm-Reiten",
                  {"stat": "sandworm_mount", "modifier": 1}),
    ],

    # ===== GÖTTER-SCHLEIM (Götterfels - SELTEN!) =====
    "goetter": [
        SlimePerk(SlimeEvolution.BABY, "Göttlich", "+5% alle Stats",
                  {"stat": "all_stats", "modifier": 0.05}),
        SlimePerk(SlimeEvolution.KIND, "Segen", "+10% XP",
                  {"stat": "xp_bonus", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.REIF, "Heilig", "+15% vs Dämonen/Untote",
                  {"stat": "holy_damage", "modifier": 0.15}),
        SlimePerk(SlimeEvolution.CHAMPION, "Avatar", "Alle Resistenzen +10%",
                  {"stat": "all_resistance", "modifier": 0.1}),
        SlimePerk(SlimeEvolution.ULTIMATIV, "Götterkind", "Zweite Chance immer",
                  {"stat": "immortal_once", "modifier": 1}),
    ],
}


def get_slime_perks(slime_type: str, evolution: SlimeEvolution) -> List[SlimePerk]:
    """Hole alle Perks die ein Slime bei seiner Evolution gibt"""
    if slime_type not in SLIME_PERKS:
        return []

    return [p for p in SLIME_PERKS[slime_type] if p.evolution_required.value <= evolution.value]


# =============================================================================
# 3. STORY-PERKS (durch Oregon Trail Events)
# =============================================================================
@dataclass
class StoryPerk:
    """Ein permanenter Perk durch eine Entscheidung"""
    id: str
    name: str
    description: str
    effects: List[Dict]  # Mehrere Effekte möglich
    reputation_changes: Dict[str, int] = field(default_factory=dict)  # Fraktion -> Änderung
    is_negative: bool = False  # Kann auch negative Konsequenzen haben


# Story-Perks die durch Events freigeschaltet werden
STORY_PERKS = {
    # ===== KANNIBALISMUS-EVENT =====
    "survival_instinct": StoryPerk(
        id="survival_instinct",
        name="Überlebensinstinkt",
        description="Du hast getan was nötig war um zu überleben",
        effects=[
            {"stat": "hunger_rate", "modifier": -0.2},  # 20% weniger Hunger
            {"stat": "sanity_cost", "modifier": 0.1},   # Aber Sanity leidet
        ],
        reputation_changes={"Alle": -30},
        is_negative=False
    ),
    "honorable_soul": StoryPerk(
        id="honorable_soul",
        name="Ehrenhafte Seele",
        description="Du hast deine Ehre behalten",
        effects=[
            {"stat": "reputation_gain", "modifier": 0.1},  # 10% mehr Ruf
        ],
        reputation_changes={"Alle": +10}
    ),

    # ===== KRANKER HÄNDLER =====
    "healer_reputation": StoryPerk(
        id="healer_reputation",
        name="Heiler-Ruf",
        description="Du hast einen Händler gerettet",
        effects=[
            {"stat": "shop_discount", "modifier": 0.1},  # 10% Rabatt bei ihm
        ],
        reputation_changes={"Handelsgilde": +20}
    ),
    "ruthless": StoryPerk(
        id="ruthless",
        name="Skrupellos",
        description="Du hast einen Sterbenden bestohlen",
        effects=[
            {"stat": "steal_chance", "modifier": 0.15},  # 15% besseres Stehlen
        ],
        reputation_changes={"Alle": -20},
        is_negative=True
    ),

    # ===== VERFLUCHTER ALTAR =====
    "dark_pact": StoryPerk(
        id="dark_pact",
        name="Dunkler Pakt",
        description="Du hast einen Pakt mit der Dunkelheit geschlossen",
        effects=[
            {"stat": "dark_damage", "modifier": 0.25},   # +25% Dunkel-Magie
            {"stat": "light_damage", "modifier": -0.25}, # -25% Licht-Magie!
        ],
        reputation_changes={"Magiergilde": -20, "Unterwelt": +30},
        is_negative=False  # Trade-off, nicht rein negativ
    ),
    "lightbringer": StoryPerk(
        id="lightbringer",
        name="Lichtbringer",
        description="Du hast die Dunkelheit zerstört",
        effects=[
            {"stat": "light_damage", "modifier": 0.25},  # +25% Licht-Magie
            {"stat": "dark_damage", "modifier": -0.25},  # -25% Dunkel-Magie!
        ],
        reputation_changes={"Magiergilde": +20, "Unterwelt": -30}
    ),
    "neutralist": StoryPerk(
        id="neutralist",
        name="Neutralist",
        description="Du hast dich nicht eingemischt",
        effects=[
            {"stat": "all_magic", "modifier": 0.1},  # +10% alle Magie
        ],
        reputation_changes={}  # Keine Änderungen
    ),

    # ===== WOLF-RUDEL =====
    "wolf_friend": StoryPerk(
        id="wolf_friend",
        name="Wolfsfreund",
        description="Du hast ein Wolfsrudel gerettet",
        effects=[
            {"stat": "animal_damage", "modifier": -0.2},  # Tiere machen -20% Schaden
            {"stat": "wolf_summon", "modifier": 1},       # Kann Wolf rufen
        ],
        reputation_changes={"Waldläufer": +25}
    ),
    "wolf_slayer": StoryPerk(
        id="wolf_slayer",
        name="Wolfstöter",
        description="Du hast das Rudel ausgelöscht",
        effects=[
            {"stat": "animal_damage", "modifier": 0.2},  # +20% Schaden vs Tiere
        ],
        reputation_changes={"Waldläufer": -40}
    ),

    # ===== DORFBRAND =====
    "hero_of_the_people": StoryPerk(
        id="hero_of_the_people",
        name="Held des Volkes",
        description="Du hast ein Dorf vor dem Feuer gerettet",
        effects=[
            {"stat": "reputation_gain", "modifier": 0.2},  # 20% mehr Ruf generell
        ],
        reputation_changes={"Alle": +15}
    ),
    "looter": StoryPerk(
        id="looter",
        name="Plünderer",
        description="Du hast das brennende Dorf geplündert",
        effects=[
            {"stat": "loot_find", "modifier": 0.25},  # 25% mehr Loot
        ],
        reputation_changes={"Alle": -25},
        is_negative=True
    ),
}


@dataclass
class PlayerStoryPerks:
    """Spieler's Story-Perks aus Oregon Trail Events"""
    unlocked_perks: List[str] = field(default_factory=list)  # Perk-IDs

    def unlock_perk(self, perk_id: str) -> Dict:
        """Story-Perk freischalten"""
        if perk_id not in STORY_PERKS:
            return {"success": False, "error": "Perk existiert nicht"}

        if perk_id in self.unlocked_perks:
            return {"success": False, "error": "Bereits freigeschaltet"}

        perk = STORY_PERKS[perk_id]
        self.unlocked_perks.append(perk_id)

        return {
            "success": True,
            "perk": perk.name,
            "description": perk.description,
            "effects": perk.effects,
            "reputation_changes": perk.reputation_changes,
            "message": f"Story-Perk freigeschaltet: {perk.name}!"
        }

    def get_all_effects(self) -> Dict[str, float]:
        """Summiere alle Effekte der Story-Perks"""
        effects = {}

        for perk_id in self.unlocked_perks:
            if perk_id in STORY_PERKS:
                perk = STORY_PERKS[perk_id]
                for effect in perk.effects:
                    stat = effect["stat"]
                    mod = effect["modifier"]
                    effects[stat] = effects.get(stat, 0) + mod

        return effects

    def has_perk(self, perk_id: str) -> bool:
        return perk_id in self.unlocked_perks


# =============================================================================
# TEST / DEMO
# =============================================================================
if __name__ == "__main__":
    # Fix Windows console encoding
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    print("=" * 70)
    print("NAJIKA PERK-SYSTEM V2 - TEST")
    print("Perks werden VERDIENT, nicht geklickt!")
    print("=" * 70)

    # 1. Skill-Meilensteine Test
    print("\n--- 1. SKILL-MEILENSTEINE ---")
    print("Feuer Level 30:")
    for m in get_unlocked_milestones("fire", 30):
        print(f"  [OK] {m.name}: {m.description}")

    print("\nFeuer Level 100 (alle):")
    for m in get_unlocked_milestones("fire", 100):
        print(f"  [OK] {m.name}: {m.description}")

    # 2. Slime-Perks Test
    print("\n--- 2. SLIME-PERKS ---")
    print("Magma-Schleim CHAMPION:")
    for p in get_slime_perks("magma", SlimeEvolution.CHAMPION):
        print(f"  [SLIME] {p.name}: {p.description}")

    print("\nKristall-Schleim ULTIMATIV:")
    for p in get_slime_perks("kristall", SlimeEvolution.ULTIMATIV):
        print(f"  [SLIME] {p.name}: {p.description}")

    # 3. Story-Perks Test
    print("\n--- 3. STORY-PERKS ---")
    story = PlayerStoryPerks()

    # Simuliere Oregon Trail Event: Dunkler Altar
    print("Event: Dunkler Altar - Spieler waehlt 'Annehmen'")
    result = story.unlock_perk("dark_pact")
    print(f"  {result['message']}")
    print(f"  Effekte: {result['effects']}")
    print(f"  Ruf-Aenderungen: {result['reputation_changes']}")

    # Später ein anderes Event
    print("\nEvent: Wolfrudel - Spieler rettet sie")
    result = story.unlock_perk("wolf_friend")
    print(f"  {result['message']}")

    print(f"\nAlle Story-Effekte: {story.get_all_effects()}")

    print("\n" + "=" * 70)
    print("EXPLOSION!!! Perks durch ERLEBEN, nicht durch KLICKEN!")
    print("=" * 70)
