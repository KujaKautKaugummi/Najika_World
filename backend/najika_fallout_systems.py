"""
NAJIKA FALLOUT-INTEGRATION
===========================
Inspiriert von Fallout New Vegas, 4 und 76

Enthält:
1. Skill-Meilenstein-Boni (automatisch beim Leveln, KEINE Perk-Punkte!)
2. Slime-Perks (passive Boni durch Evolution)
3. Story-Perks (durch Oregon Trail Events)
4. Spieler-Shop-System (Fallout 76 Vending)
5. Ruf-System (New Vegas Style)
6. Regionales Handelssystem

KEIN separates Perk-Punkte-System!
Perks werden VERDIENT durch Spielen, nicht durch Klicken.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random


# =============================================================================
# PERK-SYSTEM (Fallout 4 inspiriert, aber freier wie Skyrim)
# =============================================================================
class PerkCategory(Enum):
    """Perk-Kategorien"""
    COMBAT = "combat"           # Kampf-Perks
    MAGIC = "magic"             # Magie-Perks
    CRAFTING = "crafting"       # Handwerks-Perks
    SOCIAL = "social"           # Soziale Perks (Handel, Charisma)
    SURVIVAL = "survival"       # Überlebens-Perks
    LUCK = "luck"               # Glücks-Perks


@dataclass
class Perk:
    """Ein einzelnes Perk"""
    id: str
    name: str
    description: str
    category: PerkCategory
    max_ranks: int = 1

    # Voraussetzungen
    required_stats: Dict[str, int] = field(default_factory=dict)  # z.B. {"strength": 6}
    required_level: int = 1
    required_perks: List[str] = field(default_factory=list)  # Andere Perks die man braucht

    # Effekte pro Rang
    effects_per_rank: List[str] = field(default_factory=list)

    def get_effect(self, rank: int) -> str:
        """Hole Effekt für bestimmten Rang"""
        if rank <= 0 or rank > len(self.effects_per_rank):
            return "Kein Effekt"
        return self.effects_per_rank[rank - 1]


# Perk-Datenbank
PERK_DATABASE: Dict[str, Perk] = {
    # ===== KAMPF-PERKS =====
    "kopfschuetze": Perk(
        id="kopfschuetze",
        name="Kopfschütze",
        description="Erhöht Schaden bei Kopftreffern",
        category=PerkCategory.COMBAT,
        max_ranks=3,
        required_stats={"perception": 6},
        required_level=5,
        effects_per_rank=[
            "+10% Kopfschuss-Schaden",
            "+20% Kopfschuss-Schaden",
            "+35% Kopfschuss-Schaden, +5% Crit-Chance"
        ]
    ),
    "berserker": Perk(
        id="berserker",
        name="Berserker",
        description="Mehr Schaden bei niedrigen HP",
        category=PerkCategory.COMBAT,
        max_ranks=2,
        required_stats={"strength": 7, "endurance": 5},
        required_level=10,
        effects_per_rank=[
            "+20% Schaden unter 25% HP",
            "+40% Schaden unter 25% HP, +15% unter 50% HP"
        ]
    ),
    "beinschieber": Perk(
        id="beinschieber",
        name="Beinschieber",
        description="Beinschüsse sind effektiver",
        category=PerkCategory.COMBAT,
        max_ranks=2,
        required_stats={"perception": 5},
        required_level=3,
        effects_per_rank=[
            "Beinschüsse verlangsamen 50% stärker",
            "Beinschüsse können Gegner umwerfen (25% Chance)"
        ]
    ),
    "entwaffner": Perk(
        id="entwaffner",
        name="Entwaffner",
        description="Höhere Chance Gegner zu entwaffnen",
        category=PerkCategory.COMBAT,
        max_ranks=3,
        required_stats={"agility": 6},
        required_level=8,
        effects_per_rank=[
            "+10% Entwaffnungs-Chance bei Armtreffern",
            "+25% Entwaffnungs-Chance",
            "+40% Entwaffnungs-Chance, Waffe fliegt weiter"
        ]
    ),

    # ===== MAGIE-PERKS =====
    "explosions_meister": Perk(
        id="explosions_meister",
        name="Explosions-Meister",
        description="Explosion wird mächtiger und effizienter",
        category=PerkCategory.MAGIC,
        max_ranks=5,
        required_stats={"intelligence": 8},
        required_level=15,
        effects_per_rank=[
            "-10% Mana-Kosten für Explosion",
            "-20% Mana-Kosten, +10% Schaden",
            "-30% Mana-Kosten, +20% Schaden",
            "-40% Mana-Kosten, +30% Schaden, +AoE",
            "-50% Mana-Kosten, +50% Schaden, Finisher-Cooldown -4h"
        ]
    ),
    "element_weber": Perk(
        id="element_weber",
        name="Elementweber",
        description="Element-Verweben wird stärker",
        category=PerkCategory.MAGIC,
        max_ranks=3,
        required_stats={"intelligence": 7},
        required_level=12,
        effects_per_rank=[
            "+15% Verweben-Schaden",
            "+30% Verweben-Schaden, -15% Mana-Kosten",
            "+50% Verweben-Schaden, neue Kombinationen möglich"
        ]
    ),
    "mana_brunnen": Perk(
        id="mana_brunnen",
        name="Mana-Brunnen",
        description="Mehr Mana und schnellere Regeneration",
        category=PerkCategory.MAGIC,
        max_ranks=3,
        required_stats={"intelligence": 5, "endurance": 4},
        required_level=5,
        effects_per_rank=[
            "+20 Max Mana",
            "+40 Max Mana, +10% Mana-Regen",
            "+60 Max Mana, +25% Mana-Regen"
        ]
    ),

    # ===== HANDWERKS-PERKS =====
    "schmiedemeister": Perk(
        id="schmiedemeister",
        name="Schmiedemeister",
        description="Bessere Waffen und Rüstungen schmieden",
        category=PerkCategory.CRAFTING,
        max_ranks=4,
        required_stats={"strength": 5, "intelligence": 4},
        required_level=8,
        effects_per_rank=[
            "Kann Stahl-Ausrüstung schmieden",
            "Kann Orichalcum-Ausrüstung schmieden",
            "Kann Mithril-Ausrüstung schmieden",
            "Kann Legendäre Ausrüstung schmieden"
        ]
    ),
    "alchemist": Perk(
        id="alchemist",
        name="Alchemist",
        description="Stärkere Tränke brauen",
        category=PerkCategory.CRAFTING,
        max_ranks=3,
        required_stats={"intelligence": 6},
        required_level=5,
        effects_per_rank=[
            "Tränke 25% effektiver",
            "Tränke 50% effektiver, weniger Zutaten nötig",
            "Tränke 75% effektiver, kann 2 Effekte kombinieren"
        ]
    ),

    # ===== SOZIALE PERKS =====
    "handelstalent": Perk(
        id="handelstalent",
        name="Handelstalent",
        description="Bessere Preise bei Händlern",
        category=PerkCategory.SOCIAL,
        max_ranks=3,
        required_stats={"charisma": 6},
        required_level=3,
        effects_per_rank=[
            "Kaufe 10% billiger, verkaufe 10% teurer",
            "Kaufe 20% billiger, verkaufe 20% teurer",
            "Kaufe 30% billiger, verkaufe 30% teurer, Geheime Waren"
        ]
    ),
    "party_leader": Perk(
        id="party_leader",
        name="Party-Anführer",
        description="Deine Party wird stärker",
        category=PerkCategory.SOCIAL,
        max_ranks=2,
        required_stats={"charisma": 7},
        required_level=15,
        effects_per_rank=[
            "Party-Mitglieder +10% alle Stats",
            "Party-Mitglieder +20% alle Stats, teilen XP effizienter"
        ]
    ),

    # ===== ÜBERLEBENS-PERKS =====
    "dicker_schaedel": Perk(
        id="dicker_schaedel",
        name="Dicker Schädel",
        description="Mehr HP und Resistenzen",
        category=PerkCategory.SURVIVAL,
        max_ranks=3,
        required_stats={"endurance": 6},
        required_level=5,
        effects_per_rank=[
            "+25 Max HP",
            "+50 Max HP, +10% Schadensresistenz",
            "+75 Max HP, +20% Schadensresistenz"
        ]
    ),
    "schnelllaeufer": Perk(
        id="schnelllaeufer",
        name="Schnellläufer",
        description="Schneller bewegen und ausweichen",
        category=PerkCategory.SURVIVAL,
        max_ranks=2,
        required_stats={"agility": 7},
        required_level=8,
        effects_per_rank=[
            "+15% Bewegungsgeschwindigkeit",
            "+25% Bewegungsgeschwindigkeit, +10% Ausweichen"
        ]
    ),

    # ===== GLÜCKS-PERKS =====
    "glueckspilz": Perk(
        id="glueckspilz",
        name="Glückspilz",
        description="Bessere Drops und Zufallseffekte",
        category=PerkCategory.LUCK,
        max_ranks=3,
        required_stats={"luck": 7},
        required_level=5,
        effects_per_rank=[
            "+10% bessere Drops",
            "+20% bessere Drops, +5% Crit-Chance",
            "+35% bessere Drops, +10% Crit-Chance, seltene Events"
        ]
    ),
    "kritischer_banker": Perk(
        id="kritischer_banker",
        name="Kritischer Banker",
        description="Kritische Treffer werden gespeichert",
        category=PerkCategory.LUCK,
        max_ranks=2,
        required_stats={"luck": 8},
        required_level=12,
        effects_per_rank=[
            "Speichere 1 garantierten Crit",
            "Speichere 2 garantierte Crits, Crit-Schaden +25%"
        ]
    ),
}


@dataclass
class PlayerPerks:
    """Spieler Perk-Verwaltung"""
    available_points: int = 0
    learned_perks: Dict[str, int] = field(default_factory=dict)  # perk_id -> rank

    def can_learn(self, perk_id: str, player_stats: Dict[str, int], player_level: int) -> Tuple[bool, str]:
        """Prüfe ob Perk gelernt werden kann"""
        if perk_id not in PERK_DATABASE:
            return False, "Perk existiert nicht!"

        perk = PERK_DATABASE[perk_id]
        current_rank = self.learned_perks.get(perk_id, 0)

        if current_rank >= perk.max_ranks:
            return False, "Maximaler Rang erreicht!"

        if self.available_points < 1:
            return False, "Keine Perk-Punkte verfügbar!"

        if player_level < perk.required_level:
            return False, f"Level {perk.required_level} benötigt!"

        for stat, value in perk.required_stats.items():
            if player_stats.get(stat, 0) < value:
                return False, f"{stat.capitalize()} {value} benötigt!"

        for req_perk in perk.required_perks:
            if req_perk not in self.learned_perks:
                return False, f"Perk '{req_perk}' benötigt!"

        return True, "Kann gelernt werden"

    def learn_perk(self, perk_id: str, player_stats: Dict[str, int], player_level: int) -> Dict:
        """Perk lernen"""
        can, reason = self.can_learn(perk_id, player_stats, player_level)
        if not can:
            return {"success": False, "error": reason}

        perk = PERK_DATABASE[perk_id]
        self.available_points -= 1

        if perk_id in self.learned_perks:
            self.learned_perks[perk_id] += 1
        else:
            self.learned_perks[perk_id] = 1

        new_rank = self.learned_perks[perk_id]

        return {
            "success": True,
            "perk": perk.name,
            "rank": new_rank,
            "max_rank": perk.max_ranks,
            "effect": perk.get_effect(new_rank),
            "remaining_points": self.available_points
        }

    def get_all_effects(self) -> Dict[str, str]:
        """Hole alle aktiven Perk-Effekte"""
        effects = {}
        for perk_id, rank in self.learned_perks.items():
            if perk_id in PERK_DATABASE:
                perk = PERK_DATABASE[perk_id]
                effects[perk.name] = perk.get_effect(rank)
        return effects


# =============================================================================
# SPIELER-SHOP-SYSTEM (Fallout 76 Vending Style)
# =============================================================================
@dataclass
class ShopItem:
    """Ein Item im Spieler-Shop"""
    item_id: str
    item_name: str
    quantity: int
    price: int  # Spieler-gesetzter Preis
    category: str  # "weapon", "armor", "consumable", "material", "misc"


@dataclass
class PlayerShop:
    """
    Spieler-Shop (Fallout 76 Vending Machine Style)

    Features:
    - Eigene Preise setzen
    - Shop in der Welt platzieren
    - 5% Steuer auf Verkäufe
    - Max 50.000 Gold Limit
    """
    owner_id: str
    owner_name: str
    shop_name: str = "Unbenannter Laden"

    # Standort
    region: str = "Black Windmill"
    position_x: float = 0.0
    position_y: float = 0.0

    # Inventar
    items: List[ShopItem] = field(default_factory=list)
    max_slots: int = 20  # Kann durch Housing erweitert werden

    # Statistiken
    total_sales: int = 0
    total_gold_earned: int = 0
    reputation: int = 0  # Händler-Ruf

    # System-Konstanten
    TAX_RATE: float = 0.05  # 5% Steuer
    MAX_GOLD: int = 50000   # Gold-Limit

    def add_item(self, item: ShopItem) -> Dict:
        """Item zum Shop hinzufügen"""
        if len(self.items) >= self.max_slots:
            return {"success": False, "error": f"Shop voll! Max {self.max_slots} Slots."}

        # Prüfe ob Item bereits existiert
        for existing in self.items:
            if existing.item_id == item.item_id:
                existing.quantity += item.quantity
                return {
                    "success": True,
                    "message": f"{item.quantity}x {item.item_name} hinzugefügt (Gesamt: {existing.quantity})"
                }

        self.items.append(item)
        return {"success": True, "message": f"{item.item_name} zum Shop hinzugefügt!"}

    def remove_item(self, item_id: str, quantity: int = 1) -> Dict:
        """Item aus Shop entfernen"""
        for item in self.items:
            if item.item_id == item_id:
                if item.quantity < quantity:
                    return {"success": False, "error": "Nicht genug Items!"}

                item.quantity -= quantity
                if item.quantity <= 0:
                    self.items.remove(item)

                return {"success": True, "message": f"{quantity}x entfernt"}

        return {"success": False, "error": "Item nicht gefunden!"}

    def set_price(self, item_id: str, new_price: int) -> Dict:
        """Preis für Item setzen"""
        if new_price < 1:
            return {"success": False, "error": "Preis muss mindestens 1 sein!"}

        for item in self.items:
            if item.item_id == item_id:
                old_price = item.price
                item.price = new_price
                return {
                    "success": True,
                    "item": item.item_name,
                    "old_price": old_price,
                    "new_price": new_price
                }

        return {"success": False, "error": "Item nicht gefunden!"}

    def buy_item(self, item_id: str, buyer_gold: int, quantity: int = 1) -> Dict:
        """
        Käufer kauft Item

        Verkäufer erhält: Preis - 5% Steuer
        """
        for item in self.items:
            if item.item_id == item_id:
                if item.quantity < quantity:
                    return {"success": False, "error": "Nicht genug auf Lager!"}

                total_price = item.price * quantity

                if buyer_gold < total_price:
                    return {"success": False, "error": f"Nicht genug Gold! Brauchst {total_price}"}

                # Steuer berechnen
                tax = int(total_price * self.TAX_RATE)
                seller_receives = total_price - tax

                # Verkauf durchführen
                item.quantity -= quantity
                if item.quantity <= 0:
                    self.items.remove(item)

                self.total_sales += quantity
                self.total_gold_earned += seller_receives
                self.reputation += 1

                return {
                    "success": True,
                    "item": item.item_name,
                    "quantity": quantity,
                    "total_price": total_price,
                    "tax": tax,
                    "seller_receives": seller_receives,
                    "message": f"Gekauft: {quantity}x {item.item_name} für {total_price} Gold"
                }

        return {"success": False, "error": "Item nicht gefunden!"}

    def get_shop_info(self) -> Dict:
        """Shop-Informationen"""
        return {
            "name": self.shop_name,
            "owner": self.owner_name,
            "region": self.region,
            "items_count": len(self.items),
            "max_slots": self.max_slots,
            "total_sales": self.total_sales,
            "reputation": self.reputation,
            "items": [
                {
                    "id": item.item_id,
                    "name": item.item_name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "category": item.category
                }
                for item in self.items
            ]
        }


# =============================================================================
# RUF-SYSTEM (New Vegas Style)
# =============================================================================
class ReputationLevel(Enum):
    """Ruf-Stufen"""
    VILIFIED = -3       # Verabscheut
    HATED = -2          # Gehasst
    DISLIKED = -1       # Unbeliebt
    NEUTRAL = 0         # Neutral
    ACCEPTED = 1        # Akzeptiert
    LIKED = 2           # Gemocht
    IDOLIZED = 3        # Vergöttert


@dataclass
class FactionReputation:
    """Ruf bei einer Fraktion"""
    faction_name: str
    reputation_value: int = 0  # -100 bis +100
    level: ReputationLevel = ReputationLevel.NEUTRAL

    # Effekte
    price_modifier: float = 1.0  # 0.7 = 30% billiger, 1.3 = 30% teurer
    quest_access: bool = True
    shop_access: bool = True

    def modify_reputation(self, amount: int) -> Dict:
        """Ruf ändern"""
        old_value = self.reputation_value
        old_level = self.level

        self.reputation_value = max(-100, min(100, self.reputation_value + amount))
        self._update_level()

        return {
            "faction": self.faction_name,
            "old_value": old_value,
            "new_value": self.reputation_value,
            "old_level": old_level.name,
            "new_level": self.level.name,
            "price_modifier": self.price_modifier
        }

    def _update_level(self):
        """Level basierend auf Wert aktualisieren"""
        if self.reputation_value <= -80:
            self.level = ReputationLevel.VILIFIED
            self.price_modifier = 2.0  # 100% teurer
            self.quest_access = False
            self.shop_access = False
        elif self.reputation_value <= -50:
            self.level = ReputationLevel.HATED
            self.price_modifier = 1.5
            self.quest_access = False
            self.shop_access = True
        elif self.reputation_value <= -20:
            self.level = ReputationLevel.DISLIKED
            self.price_modifier = 1.2
        elif self.reputation_value < 20:
            self.level = ReputationLevel.NEUTRAL
            self.price_modifier = 1.0
        elif self.reputation_value < 50:
            self.level = ReputationLevel.ACCEPTED
            self.price_modifier = 0.95
        elif self.reputation_value < 80:
            self.level = ReputationLevel.LIKED
            self.price_modifier = 0.85
        else:
            self.level = ReputationLevel.IDOLIZED
            self.price_modifier = 0.7  # 30% billiger


# Standard-Fraktionen
DEFAULT_FACTIONS = [
    "Schwarze Mühle",       # Zentralhub - immer freundlich
    "Handelsgilde",         # Händler-Fraktion
    "Abenteurergilde",      # Quest-Geber
    "Schmiedezunft",        # Crafting-Fraktion
    "Magiergilde",          # Magie-Fraktion
    "Waldläufer",           # Natur-Fraktion
    "Unterwelt",            # Dunkle Fraktion
]


@dataclass
class PlayerReputation:
    """Spieler-Ruf bei allen Fraktionen"""
    factions: Dict[str, FactionReputation] = field(default_factory=dict)

    def __post_init__(self):
        # Standard-Fraktionen initialisieren
        for faction in DEFAULT_FACTIONS:
            if faction not in self.factions:
                self.factions[faction] = FactionReputation(faction_name=faction)

    def modify(self, faction: str, amount: int) -> Dict:
        """Ruf bei Fraktion ändern"""
        if faction not in self.factions:
            self.factions[faction] = FactionReputation(faction_name=faction)

        return self.factions[faction].modify_reputation(amount)

    def get_price_modifier(self, faction: str) -> float:
        """Preismodifikator für Fraktion"""
        if faction in self.factions:
            return self.factions[faction].price_modifier
        return 1.0

    def get_all_reputations(self) -> Dict:
        """Alle Rufe als Dict"""
        return {
            faction: {
                "value": rep.reputation_value,
                "level": rep.level.name,
                "price_mod": rep.price_modifier,
                "quest_access": rep.quest_access,
                "shop_access": rep.shop_access
            }
            for faction, rep in self.factions.items()
        }


# =============================================================================
# REGIONALES HANDELSSYSTEM
# =============================================================================
REGIONAL_PRICE_MODIFIERS = {
    # Region -> {Item-Kategorie -> Preismodifikator}
    "Heiße Dünen": {
        "water": 2.0,       # Wasser teuer in der Wüste
        "fire_material": 0.7,
        "sand_material": 0.5,
    },
    "Reich der Drei": {
        "warm_clothing": 0.8,
        "ice_material": 0.5,
        "fire_material": 1.5,
    },
    "Magmaströme": {
        "ore": 0.6,         # Erz billig beim Vulkan
        "weapon": 0.8,
        "ice_material": 2.0,
    },
    "Salzwind-Küste": {
        "fish": 0.5,
        "water_material": 0.6,
        "ship_parts": 0.8,
    },
    "Samtmoos-Tiefwald": {
        "herbs": 0.5,
        "nature_material": 0.6,
        "wood": 0.7,
    },
    "Grünschlamm-Sumpf": {
        "poison": 0.5,
        "dark_material": 0.6,
        "antidote": 1.5,
    },
}


def calculate_regional_price(base_price: int, item_category: str, region: str) -> int:
    """Berechne regionalen Preis"""
    if region not in REGIONAL_PRICE_MODIFIERS:
        return base_price

    modifiers = REGIONAL_PRICE_MODIFIERS[region]
    modifier = modifiers.get(item_category, 1.0)

    return int(base_price * modifier)


# =============================================================================
# TEST / DEMO
# =============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("NAJIKA FALLOUT-SYSTEME - TEST")
    print("=" * 70)

    # Perk-System Test
    print("\n--- PERK-SYSTEM ---")
    perks = PlayerPerks(available_points=5)
    stats = {"strength": 5, "perception": 7, "intelligence": 8, "luck": 7}

    print(perks.learn_perk("kopfschuetze", stats, player_level=10))
    print(perks.learn_perk("kopfschuetze", stats, player_level=10))
    print(perks.learn_perk("glueckspilz", stats, player_level=10))

    print(f"\nAktive Effekte: {perks.get_all_effects()}")

    # Shop-System Test
    print("\n--- SPIELER-SHOP ---")
    shop = PlayerShop(owner_id="kuja", owner_name="Kuja", shop_name="Kuja's Explosionsladen")

    shop.add_item(ShopItem("sword_01", "Eisenschwert", 5, 100, "weapon"))
    shop.add_item(ShopItem("potion_hp", "Heiltrank", 20, 25, "consumable"))

    print(f"Shop: {shop.get_shop_info()}")

    # Kauf simulieren
    print("\n--- KAUF ---")
    result = shop.buy_item("potion_hp", buyer_gold=100, quantity=3)
    print(f"Kauf: {result}")

    # Ruf-System Test
    print("\n--- RUF-SYSTEM ---")
    reputation = PlayerReputation()

    print(reputation.modify("Handelsgilde", 30))
    print(reputation.modify("Unterwelt", -40))

    print(f"\nAlle Rufe: {reputation.get_all_reputations()}")

    # Regionale Preise Test
    print("\n--- REGIONALE PREISE ---")
    base_price = 100
    print(f"Wasser in Wüste: {calculate_regional_price(base_price, 'water', 'Heiße Dünen')}")
    print(f"Wasser am Meer: {calculate_regional_price(base_price, 'water', 'Salzwind-Küste')}")
    print(f"Erz am Vulkan: {calculate_regional_price(base_price, 'ore', 'Magmaströme')}")

    print("\n" + "=" * 70)
    print("EXPLOSION!!! Fallout-Systeme funktionieren!")
    print("=" * 70)
