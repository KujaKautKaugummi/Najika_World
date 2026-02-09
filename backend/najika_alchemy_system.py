"""
NAJIKA ALCHEMY-SYSTEM
======================

Skyrim + Witcher + Atelier Style Alchemie!

Features:
- Zutaten sammeln (mit Slime-Utility-Bonus!)
- Rezepte entdecken durch Experimentieren
- Tränke, Gifte, Bomben, Öle herstellen
- Qualitätsstufen basierend auf Skill + Zutaten
- Slime-Spezialisierung "Crafting" gibt Boni

"Mische, braue, EXPLODIERE!" - Najika

Author: Claude Code (OPUS-1)
Date: 2026-02-02
"""

import time
import json
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# ============================================================
# ENUMS & KONSTANTEN
# ============================================================

class ZutatKategorie(Enum):
    """Kategorien von Alchemie-Zutaten"""
    KRAEUTER = "kraeuter"        # Pflanzen, Blumen, Blätter
    PILZE = "pilze"              # Alle Pilzarten
    MINERALIEN = "mineralien"    # Erze, Kristalle, Salze
    MONSTER = "monster"          # Monster-Drops
    SLIME = "slime"              # Slime-Essenzen (speziell!)
    TIERISCH = "tierisch"        # Tierische Produkte
    ELEMENTAR = "elementar"      # Elementare Essenzen
    SELTEN = "selten"            # Seltene/Legendäre Zutaten

class ProduktTyp(Enum):
    """Typen von Alchemie-Produkten"""
    TRANK = "trank"              # Heilung, Buffs
    GIFT = "gift"                # Schaden über Zeit
    BOMBE = "bombe"              # AoE-Schaden (EXPLOSION!)
    OEL = "oel"                  # Waffen-Beschichtung
    ELIXIER = "elixier"          # Permanente/Langzeit-Effekte
    ESSENZ = "essenz"            # Crafting-Material
    PARFUEM = "parfuem"          # Social/Charisma Boni

class Qualitaet(Enum):
    """Qualitätsstufen"""
    MISERABEL = 1    # 50% Effektivität
    SCHWACH = 2      # 75% Effektivität
    NORMAL = 3       # 100% Effektivität
    GUT = 4          # 125% Effektivität
    EXZELLENT = 5    # 150% Effektivität
    MEISTERWERK = 6  # 200% Effektivität + Bonus-Effekt

class EffektTyp(Enum):
    """Effekt-Typen"""
    # Positive Effekte
    HEILUNG = "heilung"
    MANA_REGEN = "mana_regen"
    STAMINA_REGEN = "stamina_regen"
    STAERKE_BUFF = "staerke_buff"
    VERTEIDIGUNG_BUFF = "verteidigung_buff"
    GESCHWINDIGKEIT_BUFF = "geschwindigkeit_buff"
    RESISTENZ = "resistenz"
    UNSICHTBARKEIT = "unsichtbarkeit"
    NACHTSICHT = "nachtsicht"
    WASSERATMUNG = "wasseratmung"

    # Negative Effekte (für Gifte)
    SCHADEN = "schaden"
    VERLANGSAMUNG = "verlangsamung"
    SCHWAECHE = "schwaeche"
    VERWIRRUNG = "verwirrung"
    LAHMUNG = "lahmung"

    # Spezial
    EXPLOSION = "explosion"  # NAJIKA APPROVED!
    FEUER = "feuer"
    EIS = "eis"
    BLITZ = "blitz"
    GIFT_DOT = "gift_dot"

# Qualitäts-Multiplikatoren
QUALITAET_MULTI = {
    Qualitaet.MISERABEL: 0.5,
    Qualitaet.SCHWACH: 0.75,
    Qualitaet.NORMAL: 1.0,
    Qualitaet.GUT: 1.25,
    Qualitaet.EXZELLENT: 1.5,
    Qualitaet.MEISTERWERK: 2.0,
}

# Skill-Level Schwellen
SKILL_SCHWELLEN = {
    "anfaenger": 0,
    "lehrling": 15,
    "geselle": 30,
    "experte": 50,
    "meister": 75,
    "grossmeister": 100,
}

# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class Zutat:
    """Eine Alchemie-Zutat"""
    zutat_id: str
    name: str
    kategorie: str

    # Effekte (werden beim Kombinieren kombiniert)
    primaer_effekt: str      # Haupt-Effekt
    sekundaer_effekt: Optional[str] = None

    # Eigenschaften
    potenz: int = 10         # Stärke des Effekts
    toxizitaet: int = 0      # Giftigkeit (zu viel = schlecht)
    seltenheit: int = 1      # 1-5 (häufig bis legendär)

    # Fundorte
    regionen: List[str] = field(default_factory=list)

    # Wert
    basis_preis: int = 10

    def to_dict(self) -> dict:
        return {
            "zutat_id": self.zutat_id,
            "name": self.name,
            "kategorie": self.kategorie,
            "primaer_effekt": self.primaer_effekt,
            "sekundaer_effekt": self.sekundaer_effekt,
            "potenz": self.potenz,
            "toxizitaet": self.toxizitaet,
            "seltenheit": self.seltenheit,
            "regionen": self.regionen,
            "basis_preis": self.basis_preis
        }

@dataclass
class Rezept:
    """Ein Alchemie-Rezept"""
    rezept_id: str
    name: str
    produkt_typ: str

    # Zutaten (zutat_id -> menge)
    zutaten: Dict[str, int]

    # Ergebnis
    effekte: List[dict]  # [{"typ": "heilung", "wert": 50, "dauer": 0}, ...]
    basis_qualitaet: int = 3  # Qualitaet.NORMAL

    # Anforderungen
    min_skill: int = 0
    entdeckt: bool = False  # Muss erst entdeckt werden!

    # Crafting
    craft_zeit: float = 5.0  # Sekunden
    basis_menge: int = 1     # Wie viele pro Craft

    # Beschreibung
    beschreibung: str = ""

    def to_dict(self) -> dict:
        return {
            "rezept_id": self.rezept_id,
            "name": self.name,
            "produkt_typ": self.produkt_typ,
            "zutaten": self.zutaten,
            "effekte": self.effekte,
            "basis_qualitaet": self.basis_qualitaet,
            "min_skill": self.min_skill,
            "entdeckt": self.entdeckt,
            "craft_zeit": self.craft_zeit,
            "basis_menge": self.basis_menge,
            "beschreibung": self.beschreibung
        }

@dataclass
class AlchemieProdukt:
    """Ein hergestelltes Alchemie-Produkt"""
    produkt_id: str
    rezept_id: str
    name: str
    produkt_typ: str

    # Qualität & Effekte
    qualitaet: int
    effekte: List[dict]

    # Stack
    menge: int = 1
    max_stack: int = 99

    # Herstellung
    hergestellt_von: str = ""
    hergestellt_am: float = 0

    def to_dict(self) -> dict:
        return {
            "produkt_id": self.produkt_id,
            "rezept_id": self.rezept_id,
            "name": self.name,
            "produkt_typ": self.produkt_typ,
            "qualitaet": self.qualitaet,
            "qualitaet_name": Qualitaet(self.qualitaet).name,
            "effekte": self.effekte,
            "menge": self.menge,
            "hergestellt_von": self.hergestellt_von,
            "hergestellt_am": self.hergestellt_am
        }

@dataclass
class SpielerAlchemie:
    """Alchemie-Fortschritt eines Spielers"""
    spieler_id: str

    # Skill
    skill_level: int = 1
    skill_exp: int = 0
    skill_exp_next: int = 100

    # Entdeckte Rezepte
    entdeckte_rezepte: List[str] = field(default_factory=list)

    # Statistiken
    produkte_hergestellt: int = 0
    experimente_durchgefuehrt: int = 0
    meisterwerke_erstellt: int = 0
    explosionen_verursacht: int = 0  # EXPLOSION counter!

    # Inventar (zutat_id -> menge)
    zutaten_inventar: Dict[str, int] = field(default_factory=dict)

    # Hergestellte Produkte
    produkte: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "spieler_id": self.spieler_id,
            "skill_level": self.skill_level,
            "skill_exp": self.skill_exp,
            "skill_exp_next": self.skill_exp_next,
            "skill_rang": self._get_skill_rang(),
            "entdeckte_rezepte": self.entdeckte_rezepte,
            "produkte_hergestellt": self.produkte_hergestellt,
            "experimente_durchgefuehrt": self.experimente_durchgefuehrt,
            "meisterwerke_erstellt": self.meisterwerke_erstellt,
            "explosionen_verursacht": self.explosionen_verursacht,
            "zutaten_count": len(self.zutaten_inventar),
            "produkte_count": len(self.produkte)
        }

    def _get_skill_rang(self) -> str:
        for rang, schwelle in sorted(SKILL_SCHWELLEN.items(), key=lambda x: -x[1]):
            if self.skill_level >= schwelle:
                return rang
        return "anfaenger"

# ============================================================
# ZUTATEN-DATENBANK
# ============================================================

ZUTATEN_DB: Dict[str, Zutat] = {
    # --- KRÄUTER ---
    "heilkraut": Zutat(
        zutat_id="heilkraut",
        name="Heilkraut",
        kategorie=ZutatKategorie.KRAEUTER.value,
        primaer_effekt=EffektTyp.HEILUNG.value,
        potenz=15,
        seltenheit=1,
        regionen=["samtmoos_tiefwald", "gruenschlamm_sumpf"],
        basis_preis=5
    ),
    "feuerlilie": Zutat(
        zutat_id="feuerlilie",
        name="Feuerlilie",
        kategorie=ZutatKategorie.KRAEUTER.value,
        primaer_effekt=EffektTyp.FEUER.value,
        sekundaer_effekt=EffektTyp.RESISTENZ.value,
        potenz=25,
        seltenheit=2,
        regionen=["magmastroeme", "heisse_duenen"],
        basis_preis=20
    ),
    "mondblume": Zutat(
        zutat_id="mondblume",
        name="Mondblume",
        kategorie=ZutatKategorie.KRAEUTER.value,
        primaer_effekt=EffektTyp.MANA_REGEN.value,
        sekundaer_effekt=EffektTyp.NACHTSICHT.value,
        potenz=20,
        seltenheit=3,
        regionen=["tiefenhoehlen"],
        basis_preis=35
    ),
    "eiswurz": Zutat(
        zutat_id="eiswurz",
        name="Eiswurz",
        kategorie=ZutatKategorie.KRAEUTER.value,
        primaer_effekt=EffektTyp.EIS.value,
        sekundaer_effekt=EffektTyp.VERLANGSAMUNG.value,
        potenz=20,
        seltenheit=2,
        regionen=["reich_der_drei"],
        basis_preis=25
    ),
    "blitzdistel": Zutat(
        zutat_id="blitzdistel",
        name="Blitzdistel",
        kategorie=ZutatKategorie.KRAEUTER.value,
        primaer_effekt=EffektTyp.BLITZ.value,
        sekundaer_effekt=EffektTyp.GESCHWINDIGKEIT_BUFF.value,
        potenz=25,
        seltenheit=3,
        regionen=["blitzebene"],
        basis_preis=40
    ),

    # --- PILZE ---
    "heilpilz": Zutat(
        zutat_id="heilpilz",
        name="Heilpilz",
        kategorie=ZutatKategorie.PILZE.value,
        primaer_effekt=EffektTyp.HEILUNG.value,
        potenz=25,
        seltenheit=1,
        regionen=["samtmoos_tiefwald", "gruenschlamm_sumpf"],
        basis_preis=8
    ),
    "giftpilz": Zutat(
        zutat_id="giftpilz",
        name="Giftpilz",
        kategorie=ZutatKategorie.PILZE.value,
        primaer_effekt=EffektTyp.GIFT_DOT.value,
        toxizitaet=30,
        potenz=35,
        seltenheit=2,
        regionen=["gruenschlamm_sumpf"],
        basis_preis=15
    ),
    "leuchtpilz": Zutat(
        zutat_id="leuchtpilz",
        name="Leuchtpilz",
        kategorie=ZutatKategorie.PILZE.value,
        primaer_effekt=EffektTyp.NACHTSICHT.value,
        potenz=30,
        seltenheit=2,
        regionen=["tiefenhoehlen"],
        basis_preis=20
    ),

    # --- MINERALIEN ---
    "salz": Zutat(
        zutat_id="salz",
        name="Salz",
        kategorie=ZutatKategorie.MINERALIEN.value,
        primaer_effekt=EffektTyp.RESISTENZ.value,
        potenz=10,
        seltenheit=1,
        regionen=["salzwind_kueste", "heisse_duenen"],
        basis_preis=3
    ),
    "schwefel": Zutat(
        zutat_id="schwefel",
        name="Schwefel",
        kategorie=ZutatKategorie.MINERALIEN.value,
        primaer_effekt=EffektTyp.EXPLOSION.value,
        toxizitaet=20,
        potenz=50,
        seltenheit=2,
        regionen=["magmastroeme"],
        basis_preis=30
    ),
    "mondstein_staub": Zutat(
        zutat_id="mondstein_staub",
        name="Mondstein-Staub",
        kategorie=ZutatKategorie.MINERALIEN.value,
        primaer_effekt=EffektTyp.MANA_REGEN.value,
        sekundaer_effekt=EffektTyp.UNSICHTBARKEIT.value,
        potenz=40,
        seltenheit=4,
        regionen=["goetterfels"],
        basis_preis=100
    ),

    # --- SLIME ESSENZEN (Speziell!) ---
    "moos_essenz": Zutat(
        zutat_id="moos_essenz",
        name="Moos-Schleim-Essenz",
        kategorie=ZutatKategorie.SLIME.value,
        primaer_effekt=EffektTyp.HEILUNG.value,
        sekundaer_effekt=EffektTyp.STAMINA_REGEN.value,
        potenz=30,
        seltenheit=2,
        regionen=["samtmoos_tiefwald"],
        basis_preis=50
    ),
    "frost_essenz": Zutat(
        zutat_id="frost_essenz",
        name="Frost-Schleim-Essenz",
        kategorie=ZutatKategorie.SLIME.value,
        primaer_effekt=EffektTyp.EIS.value,
        sekundaer_effekt=EffektTyp.RESISTENZ.value,
        potenz=35,
        seltenheit=2,
        regionen=["reich_der_drei"],
        basis_preis=55
    ),
    "magma_essenz": Zutat(
        zutat_id="magma_essenz",
        name="Magma-Schleim-Essenz",
        kategorie=ZutatKategorie.SLIME.value,
        primaer_effekt=EffektTyp.FEUER.value,
        sekundaer_effekt=EffektTyp.EXPLOSION.value,
        potenz=45,
        seltenheit=3,
        regionen=["magmastroeme"],
        basis_preis=80
    ),
    "blitz_essenz": Zutat(
        zutat_id="blitz_essenz",
        name="Blitz-Schleim-Essenz",
        kategorie=ZutatKategorie.SLIME.value,
        primaer_effekt=EffektTyp.BLITZ.value,
        sekundaer_effekt=EffektTyp.GESCHWINDIGKEIT_BUFF.value,
        potenz=40,
        seltenheit=3,
        regionen=["blitzebene"],
        basis_preis=75
    ),
    "goetter_essenz": Zutat(
        zutat_id="goetter_essenz",
        name="Götter-Schleim-Essenz",
        kategorie=ZutatKategorie.SLIME.value,
        primaer_effekt=EffektTyp.HEILUNG.value,
        sekundaer_effekt=EffektTyp.MANA_REGEN.value,
        potenz=60,
        seltenheit=5,
        regionen=["goetterfels"],
        basis_preis=500
    ),

    # --- MONSTER-DROPS ---
    "wolfszahn": Zutat(
        zutat_id="wolfszahn",
        name="Wolfszahn",
        kategorie=ZutatKategorie.MONSTER.value,
        primaer_effekt=EffektTyp.STAERKE_BUFF.value,
        potenz=20,
        seltenheit=2,
        regionen=["samtmoos_tiefwald", "reich_der_drei"],
        basis_preis=25
    ),
    "drachenblut": Zutat(
        zutat_id="drachenblut",
        name="Drachenblut",
        kategorie=ZutatKategorie.MONSTER.value,
        primaer_effekt=EffektTyp.FEUER.value,
        sekundaer_effekt=EffektTyp.RESISTENZ.value,
        potenz=60,
        seltenheit=5,
        regionen=["magmastroeme"],
        basis_preis=300
    ),

    # --- ELEMENTAR ---
    "feuer_essenz": Zutat(
        zutat_id="feuer_essenz",
        name="Reine Feuer-Essenz",
        kategorie=ZutatKategorie.ELEMENTAR.value,
        primaer_effekt=EffektTyp.FEUER.value,
        potenz=50,
        seltenheit=4,
        regionen=["magmastroeme"],
        basis_preis=150
    ),
    "wasser_essenz": Zutat(
        zutat_id="wasser_essenz",
        name="Reine Wasser-Essenz",
        kategorie=ZutatKategorie.ELEMENTAR.value,
        primaer_effekt=EffektTyp.WASSERATMUNG.value,
        sekundaer_effekt=EffektTyp.HEILUNG.value,
        potenz=45,
        seltenheit=4,
        regionen=["salzwind_kueste"],
        basis_preis=140
    ),
}

# ============================================================
# REZEPT-DATENBANK
# ============================================================

REZEPT_DB: Dict[str, Rezept] = {
    # --- TRÄNKE ---
    "kleiner_heiltrank": Rezept(
        rezept_id="kleiner_heiltrank",
        name="Kleiner Heiltrank",
        produkt_typ=ProduktTyp.TRANK.value,
        zutaten={"heilkraut": 2},
        effekte=[{"typ": EffektTyp.HEILUNG.value, "wert": 50, "dauer": 0}],
        min_skill=0,
        entdeckt=True,  # Starter-Rezept
        beschreibung="Ein einfacher Heiltrank. Jeder Alchemist lernt diesen zuerst."
    ),
    "mittlerer_heiltrank": Rezept(
        rezept_id="mittlerer_heiltrank",
        name="Mittlerer Heiltrank",
        produkt_typ=ProduktTyp.TRANK.value,
        zutaten={"heilkraut": 2, "heilpilz": 1},
        effekte=[{"typ": EffektTyp.HEILUNG.value, "wert": 150, "dauer": 0}],
        min_skill=15,
        beschreibung="Ein stärkerer Heiltrank mit Pilz-Extrakt."
    ),
    "grosser_heiltrank": Rezept(
        rezept_id="grosser_heiltrank",
        name="Großer Heiltrank",
        produkt_typ=ProduktTyp.TRANK.value,
        zutaten={"heilkraut": 3, "heilpilz": 2, "moos_essenz": 1},
        effekte=[{"typ": EffektTyp.HEILUNG.value, "wert": 300, "dauer": 0}],
        min_skill=30,
        beschreibung="Ein mächtiger Heiltrank mit Schleim-Essenz."
    ),
    "mana_trank": Rezept(
        rezept_id="mana_trank",
        name="Mana-Trank",
        produkt_typ=ProduktTyp.TRANK.value,
        zutaten={"mondblume": 2, "salz": 1},
        effekte=[{"typ": EffektTyp.MANA_REGEN.value, "wert": 100, "dauer": 0}],
        min_skill=10,
        beschreibung="Stellt Mana sofort wieder her."
    ),
    "stamina_trank": Rezept(
        rezept_id="stamina_trank",
        name="Ausdauer-Trank",
        produkt_typ=ProduktTyp.TRANK.value,
        zutaten={"heilkraut": 1, "wolfszahn": 1},
        effekte=[{"typ": EffektTyp.STAMINA_REGEN.value, "wert": 100, "dauer": 0}],
        min_skill=10,
        beschreibung="Stellt Ausdauer sofort wieder her."
    ),
    "nachtsicht_trank": Rezept(
        rezept_id="nachtsicht_trank",
        name="Nachtsicht-Trank",
        produkt_typ=ProduktTyp.TRANK.value,
        zutaten={"leuchtpilz": 2, "mondblume": 1},
        effekte=[{"typ": EffektTyp.NACHTSICHT.value, "wert": 1, "dauer": 300}],
        min_skill=20,
        beschreibung="Sehe im Dunkeln für 5 Minuten."
    ),
    "geschwindigkeits_trank": Rezept(
        rezept_id="geschwindigkeits_trank",
        name="Geschwindigkeits-Elixier",
        produkt_typ=ProduktTyp.ELIXIER.value,
        zutaten={"blitzdistel": 2, "blitz_essenz": 1},
        effekte=[{"typ": EffektTyp.GESCHWINDIGKEIT_BUFF.value, "wert": 30, "dauer": 180}],
        min_skill=35,
        beschreibung="+30% Bewegungsgeschwindigkeit für 3 Minuten."
    ),
    "unsichtbarkeits_trank": Rezept(
        rezept_id="unsichtbarkeits_trank",
        name="Trank der Unsichtbarkeit",
        produkt_typ=ProduktTyp.ELIXIER.value,
        zutaten={"mondstein_staub": 2, "mondblume": 2, "wasser_essenz": 1},
        effekte=[{"typ": EffektTyp.UNSICHTBARKEIT.value, "wert": 1, "dauer": 60}],
        min_skill=60,
        beschreibung="Werde für 60 Sekunden unsichtbar!"
    ),

    # --- GIFTE ---
    "schwaches_gift": Rezept(
        rezept_id="schwaches_gift",
        name="Schwaches Gift",
        produkt_typ=ProduktTyp.GIFT.value,
        zutaten={"giftpilz": 2},
        effekte=[{"typ": EffektTyp.GIFT_DOT.value, "wert": 5, "dauer": 10}],
        min_skill=10,
        beschreibung="Vergiftet das Ziel für 10 Sekunden."
    ),
    "starkes_gift": Rezept(
        rezept_id="starkes_gift",
        name="Starkes Gift",
        produkt_typ=ProduktTyp.GIFT.value,
        zutaten={"giftpilz": 3, "wolfszahn": 1},
        effekte=[{"typ": EffektTyp.GIFT_DOT.value, "wert": 15, "dauer": 15}],
        min_skill=25,
        beschreibung="Schweres Gift mit Wolfszahn-Katalysator."
    ),
    "laehmungsgift": Rezept(
        rezept_id="laehmungsgift",
        name="Lähmungsgift",
        produkt_typ=ProduktTyp.GIFT.value,
        zutaten={"giftpilz": 2, "eiswurz": 2},
        effekte=[{"typ": EffektTyp.LAHMUNG.value, "wert": 1, "dauer": 5}],
        min_skill=40,
        beschreibung="Lähmt das Ziel für 5 Sekunden!"
    ),

    # --- BOMBEN (EXPLOSION!!!) ---
    "kleine_bombe": Rezept(
        rezept_id="kleine_bombe",
        name="Kleine Bombe",
        produkt_typ=ProduktTyp.BOMBE.value,
        zutaten={"schwefel": 2, "salz": 1},
        effekte=[{"typ": EffektTyp.EXPLOSION.value, "wert": 50, "radius": 3}],
        min_skill=15,
        beschreibung="Eine kleine Explosion. BOOM!"
    ),
    "feuerbombe": Rezept(
        rezept_id="feuerbombe",
        name="Feuerbombe",
        produkt_typ=ProduktTyp.BOMBE.value,
        zutaten={"schwefel": 2, "feuerlilie": 2, "feuer_essenz": 1},
        effekte=[
            {"typ": EffektTyp.EXPLOSION.value, "wert": 80, "radius": 4},
            {"typ": EffektTyp.FEUER.value, "wert": 20, "dauer": 5}
        ],
        min_skill=35,
        beschreibung="Explosiver Feuerschaden + Brennen!"
    ),
    "blitzbombe": Rezept(
        rezept_id="blitzbombe",
        name="Blitzbombe",
        produkt_typ=ProduktTyp.BOMBE.value,
        zutaten={"schwefel": 2, "blitzdistel": 2, "blitz_essenz": 1},
        effekte=[
            {"typ": EffektTyp.EXPLOSION.value, "wert": 70, "radius": 5},
            {"typ": EffektTyp.BLITZ.value, "wert": 30, "chain": 3}
        ],
        min_skill=40,
        beschreibung="Kettenblitz nach der Explosion!"
    ),
    "mega_explosion": Rezept(
        rezept_id="mega_explosion",
        name="MEGA EXPLOSION",
        produkt_typ=ProduktTyp.BOMBE.value,
        zutaten={"schwefel": 5, "magma_essenz": 2, "feuer_essenz": 2, "drachenblut": 1},
        effekte=[
            {"typ": EffektTyp.EXPLOSION.value, "wert": 500, "radius": 10},
            {"typ": EffektTyp.FEUER.value, "wert": 100, "dauer": 10}
        ],
        min_skill=75,
        craft_zeit=30,
        beschreibung="EXPLOSION!!! Najika's Lieblingsrezept! Massiver AoE-Schaden!"
    ),

    # --- ÖLE ---
    "feueroel": Rezept(
        rezept_id="feueroel",
        name="Feueröl",
        produkt_typ=ProduktTyp.OEL.value,
        zutaten={"feuerlilie": 2, "salz": 1},
        effekte=[{"typ": EffektTyp.FEUER.value, "wert": 20, "hits": 10}],
        min_skill=20,
        beschreibung="Beschichtet Waffe mit Feuer (10 Treffer)."
    ),
    "giftoel": Rezept(
        rezept_id="giftoel",
        name="Giftöl",
        produkt_typ=ProduktTyp.OEL.value,
        zutaten={"giftpilz": 2, "salz": 1},
        effekte=[{"typ": EffektTyp.GIFT_DOT.value, "wert": 5, "hits": 10}],
        min_skill=20,
        beschreibung="Beschichtet Waffe mit Gift (10 Treffer)."
    ),

    # --- GÖTTLICH ---
    "goetter_elixier": Rezept(
        rezept_id="goetter_elixier",
        name="Götter-Elixier",
        produkt_typ=ProduktTyp.ELIXIER.value,
        zutaten={"goetter_essenz": 2, "mondstein_staub": 2, "drachenblut": 1},
        effekte=[
            {"typ": EffektTyp.HEILUNG.value, "wert": 500, "dauer": 0},
            {"typ": EffektTyp.MANA_REGEN.value, "wert": 200, "dauer": 0},
            {"typ": EffektTyp.STAERKE_BUFF.value, "wert": 50, "dauer": 300}
        ],
        min_skill=90,
        craft_zeit=60,
        beschreibung="Das ultimative Elixier. Vollständige Wiederherstellung + Buff!"
    ),
}

# ============================================================
# HAUPT-MANAGER
# ============================================================

class AlchemieSystem:
    """
    Verwaltet das gesamte Alchemie-System.

    Features:
    - Zutaten sammeln/verwalten
    - Rezepte entdecken durch Experimentieren
    - Produkte herstellen mit Qualitätssystem
    - Skill-Progression (Learning by Doing)
    - Slime-Bonus Integration
    """

    def __init__(self):
        # Datenbanken
        self.zutaten = ZUTATEN_DB
        self.rezepte = REZEPT_DB

        # Spieler-Daten
        self.spieler_daten: Dict[str, SpielerAlchemie] = {}

        # State laden
        self._load_state()

    # --- Zutaten ---

    def sammle_zutat(self, spieler_id: str, zutat_id: str, menge: int = 1,
                      slime_bonus: float = 0) -> dict:
        """Fügt Zutat zum Inventar hinzu"""
        if zutat_id not in self.zutaten:
            return {"erfolg": False, "grund": f"Unbekannte Zutat: {zutat_id}"}

        spieler = self._get_oder_erstelle_spieler(spieler_id)
        zutat = self.zutaten[zutat_id]

        # Slime-Bonus anwenden (z.B. +20% Menge)
        if slime_bonus > 0:
            bonus_menge = int(menge * slime_bonus)
            menge += bonus_menge

        # Zum Inventar hinzufügen
        if zutat_id in spieler.zutaten_inventar:
            spieler.zutaten_inventar[zutat_id] += menge
        else:
            spieler.zutaten_inventar[zutat_id] = menge

        self._save_state()

        return {
            "erfolg": True,
            "zutat": zutat.to_dict(),
            "menge": menge,
            "gesamt": spieler.zutaten_inventar[zutat_id],
            "slime_bonus_angewendet": slime_bonus > 0
        }

    def get_zutaten_inventar(self, spieler_id: str) -> dict:
        """Gibt Zutaten-Inventar zurück"""
        spieler = self.spieler_daten.get(spieler_id)
        if not spieler:
            return {"zutaten": [], "count": 0}

        zutaten_liste = []
        for zutat_id, menge in spieler.zutaten_inventar.items():
            if zutat_id in self.zutaten:
                zutat_dict = self.zutaten[zutat_id].to_dict()
                zutat_dict["menge"] = menge
                zutaten_liste.append(zutat_dict)

        return {
            "zutaten": zutaten_liste,
            "count": len(zutaten_liste),
            "gesamt_items": sum(spieler.zutaten_inventar.values())
        }

    # --- Rezepte ---

    def get_bekannte_rezepte(self, spieler_id: str) -> List[dict]:
        """Gibt alle bekannten Rezepte zurück"""
        spieler = self.spieler_daten.get(spieler_id)
        entdeckt = spieler.entdeckte_rezepte if spieler else []

        rezepte = []
        for rezept_id, rezept in self.rezepte.items():
            if rezept.entdeckt or rezept_id in entdeckt:
                rezept_dict = rezept.to_dict()
                rezept_dict["kann_craften"] = self._kann_craften(spieler_id, rezept_id)[0]
                rezepte.append(rezept_dict)

        return rezepte

    def _kann_craften(self, spieler_id: str, rezept_id: str) -> Tuple[bool, str]:
        """Prüft ob Spieler Rezept craften kann"""
        spieler = self.spieler_daten.get(spieler_id)
        if not spieler:
            return False, "Spieler nicht gefunden"

        if rezept_id not in self.rezepte:
            return False, "Rezept nicht gefunden"

        rezept = self.rezepte[rezept_id]

        # Skill-Level prüfen
        if spieler.skill_level < rezept.min_skill:
            return False, f"Benötigt Skill-Level {rezept.min_skill} (du hast {spieler.skill_level})"

        # Rezept entdeckt?
        if not rezept.entdeckt and rezept_id not in spieler.entdeckte_rezepte:
            return False, "Rezept noch nicht entdeckt"

        # Zutaten prüfen
        for zutat_id, menge in rezept.zutaten.items():
            vorhanden = spieler.zutaten_inventar.get(zutat_id, 0)
            if vorhanden < menge:
                return False, f"Nicht genug {zutat_id} ({vorhanden}/{menge})"

        return True, "OK"

    # --- Crafting ---

    def stelle_her(self, spieler_id: str, rezept_id: str,
                    slime_qualitaet_bonus: float = 0) -> dict:
        """Stellt ein Alchemie-Produkt her"""
        kann, grund = self._kann_craften(spieler_id, rezept_id)
        if not kann:
            return {"erfolg": False, "grund": grund}

        spieler = self.spieler_daten[spieler_id]
        rezept = self.rezepte[rezept_id]

        # Zutaten verbrauchen
        for zutat_id, menge in rezept.zutaten.items():
            spieler.zutaten_inventar[zutat_id] -= menge
            if spieler.zutaten_inventar[zutat_id] <= 0:
                del spieler.zutaten_inventar[zutat_id]

        # Qualität berechnen
        qualitaet = self._berechne_qualitaet(spieler, rezept, slime_qualitaet_bonus)

        # Effekte skalieren
        effekte = self._skaliere_effekte(rezept.effekte, qualitaet)

        # Produkt erstellen
        produkt = AlchemieProdukt(
            produkt_id=f"prod_{int(time.time())}_{random.randint(1000, 9999)}",
            rezept_id=rezept_id,
            name=rezept.name,
            produkt_typ=rezept.produkt_typ,
            qualitaet=qualitaet,
            effekte=effekte,
            menge=rezept.basis_menge,
            hergestellt_von=spieler_id,
            hergestellt_am=time.time()
        )

        spieler.produkte.append(produkt.to_dict())
        spieler.produkte_hergestellt += 1

        # EXP geben
        exp_gewinn = 10 + (rezept.min_skill // 5) + (qualitaet * 5)
        self._add_exp(spieler, exp_gewinn)

        # Meisterwerk?
        if qualitaet == Qualitaet.MEISTERWERK.value:
            spieler.meisterwerke_erstellt += 1

        # Explosion?
        if rezept.produkt_typ == ProduktTyp.BOMBE.value:
            spieler.explosionen_verursacht += 1

        self._save_state()

        return {
            "erfolg": True,
            "produkt": produkt.to_dict(),
            "qualitaet_name": Qualitaet(qualitaet).name,
            "exp_gewinn": exp_gewinn,
            "ist_meisterwerk": qualitaet == Qualitaet.MEISTERWERK.value,
            "nachricht": self._get_craft_nachricht(rezept, qualitaet)
        }

    def _berechne_qualitaet(self, spieler: SpielerAlchemie, rezept: Rezept,
                            slime_bonus: float) -> int:
        """Berechnet Qualität basierend auf Skill und Zufall"""
        # Basis-Chance
        skill_diff = spieler.skill_level - rezept.min_skill

        # Würfeln (1-100)
        wurf = random.randint(1, 100)

        # Boni
        wurf += skill_diff * 2  # +2 pro Skill über Minimum
        wurf += int(slime_bonus * 20)  # Slime-Bonus

        # Qualität bestimmen
        if wurf >= 95:
            return Qualitaet.MEISTERWERK.value
        elif wurf >= 80:
            return Qualitaet.EXZELLENT.value
        elif wurf >= 60:
            return Qualitaet.GUT.value
        elif wurf >= 40:
            return Qualitaet.NORMAL.value
        elif wurf >= 20:
            return Qualitaet.SCHWACH.value
        else:
            return Qualitaet.MISERABEL.value

    def _skaliere_effekte(self, basis_effekte: List[dict], qualitaet: int) -> List[dict]:
        """Skaliert Effekte basierend auf Qualität"""
        multi = QUALITAET_MULTI[Qualitaet(qualitaet)]

        skaliert = []
        for effekt in basis_effekte:
            neuer_effekt = effekt.copy()
            if "wert" in neuer_effekt:
                neuer_effekt["wert"] = int(neuer_effekt["wert"] * multi)
            skaliert.append(neuer_effekt)

        return skaliert

    def _get_craft_nachricht(self, rezept: Rezept, qualitaet: int) -> str:
        """Gibt Crafting-Nachricht zurück"""
        q_name = Qualitaet(qualitaet).name

        if rezept.produkt_typ == ProduktTyp.BOMBE.value:
            if qualitaet >= Qualitaet.EXZELLENT.value:
                return f"EXPLOSION!!! Ein {q_name}es {rezept.name}! Das wird EPISCH! 💥"
            else:
                return f"Boom! {rezept.name} ({q_name}) hergestellt!"

        if qualitaet == Qualitaet.MEISTERWERK.value:
            return f"MEISTERWERK! Dein {rezept.name} ist PERFEKT! ✨"
        elif qualitaet >= Qualitaet.GUT.value:
            return f"Gut gemacht! {rezept.name} ({q_name}) hergestellt."
        else:
            return f"{rezept.name} ({q_name}) hergestellt. Naja, Übung macht den Meister..."

    # --- Experimentieren ---

    def experimentiere(self, spieler_id: str, zutat_ids: List[str]) -> dict:
        """
        Experimentiert mit Zutaten um neue Rezepte zu entdecken.
        Kann auch fehlschlagen (mit lustigen Konsequenzen)!
        """
        spieler = self._get_oder_erstelle_spieler(spieler_id)

        # Mindestens 2 Zutaten
        if len(zutat_ids) < 2:
            return {"erfolg": False, "grund": "Mindestens 2 Zutaten zum Experimentieren!"}

        # Zutaten prüfen
        for zutat_id in zutat_ids:
            if zutat_id not in self.zutaten:
                return {"erfolg": False, "grund": f"Unbekannte Zutat: {zutat_id}"}
            if spieler.zutaten_inventar.get(zutat_id, 0) < 1:
                return {"erfolg": False, "grund": f"Keine {zutat_id} vorhanden"}

        # Zutaten verbrauchen
        for zutat_id in zutat_ids:
            spieler.zutaten_inventar[zutat_id] -= 1
            if spieler.zutaten_inventar[zutat_id] <= 0:
                del spieler.zutaten_inventar[zutat_id]

        spieler.experimente_durchgefuehrt += 1

        # Rezept-Match suchen
        zutat_set = set(zutat_ids)
        gefundenes_rezept = None

        for rezept_id, rezept in self.rezepte.items():
            if rezept_id in spieler.entdeckte_rezepte:
                continue  # Schon entdeckt

            rezept_zutaten = set(rezept.zutaten.keys())
            if zutat_set == rezept_zutaten:
                # MATCH!
                gefundenes_rezept = rezept
                spieler.entdeckte_rezepte.append(rezept_id)
                break

        # EXP fürs Experimentieren
        exp_gewinn = 5 + len(zutat_ids) * 2
        if gefundenes_rezept:
            exp_gewinn += 50  # Bonus für Entdeckung!

        self._add_exp(spieler, exp_gewinn)
        self._save_state()

        if gefundenes_rezept:
            return {
                "erfolg": True,
                "entdeckt": True,
                "rezept": gefundenes_rezept.to_dict(),
                "exp_gewinn": exp_gewinn,
                "nachricht": f"ENTDECKUNG! Du hast '{gefundenes_rezept.name}' entdeckt! 🎉"
            }
        else:
            # Fehlschlag - aber lustig!
            fehlschlag = self._generiere_fehlschlag(zutat_ids)
            return {
                "erfolg": True,
                "entdeckt": False,
                "fehlschlag": fehlschlag,
                "exp_gewinn": exp_gewinn,
                "nachricht": fehlschlag["nachricht"]
            }

    def _generiere_fehlschlag(self, zutat_ids: List[str]) -> dict:
        """Generiert lustigen Fehlschlag"""
        fehlschlaege = [
            {
                "typ": "explosion",
                "nachricht": "PUFF! Dein Experiment explodiert in einer Rauchwolke. Hustend wedelst du den Rauch weg.",
                "effekt": None
            },
            {
                "typ": "schleim",
                "nachricht": "Die Mischung verwandelt sich in nutzlosen Schleim. Immerhin riecht er interessant?",
                "effekt": None
            },
            {
                "typ": "stinker",
                "nachricht": "IGITT! Eine übelriechende Substanz entsteht. NPCs in der Nähe verziehen das Gesicht.",
                "effekt": {"typ": "stink", "dauer": 60}
            },
            {
                "typ": "mini_explosion",
                "nachricht": "BUMM! Eine kleine Explosion! Du verlierst 5 HP aber gewinnst eine coole Geschichte.",
                "effekt": {"typ": "damage", "wert": 5}
            },
            {
                "typ": "verfaerbung",
                "nachricht": "Deine Hände sind jetzt blau gefärbt. Das geht in ein paar Stunden wieder weg... hoffentlich.",
                "effekt": {"typ": "cosmetic", "dauer": 3600}
            },
            {
                "typ": "fast",
                "nachricht": "Fast! Du spürst, dass du nah dran warst. Vielleicht eine andere Kombination?",
                "effekt": None
            }
        ]

        return random.choice(fehlschlaege)

    # --- Skill-System ---

    def _add_exp(self, spieler: SpielerAlchemie, exp: int):
        """Fügt EXP hinzu und handled Level-Up"""
        spieler.skill_exp += exp

        while spieler.skill_exp >= spieler.skill_exp_next:
            spieler.skill_exp -= spieler.skill_exp_next
            spieler.skill_level += 1
            spieler.skill_exp_next = int(spieler.skill_exp_next * 1.15)  # +15% pro Level

    # --- Abfragen ---

    def get_spieler_status(self, spieler_id: str) -> dict:
        """Gibt Spieler-Alchemie-Status zurück"""
        spieler = self.spieler_daten.get(spieler_id)
        if not spieler:
            return {
                "hat_daten": False,
                "hinweis": "Noch keine Alchemie-Aktivitäten"
            }

        return {
            "hat_daten": True,
            "status": spieler.to_dict(),
            "zutaten": self.get_zutaten_inventar(spieler_id),
            "rezepte_bekannt": len(spieler.entdeckte_rezepte) + sum(1 for r in self.rezepte.values() if r.entdeckt)
        }

    def get_stats(self) -> dict:
        """Gibt System-Statistiken zurück"""
        return {
            "zutaten_verfuegbar": len(self.zutaten),
            "rezepte_gesamt": len(self.rezepte),
            "spieler_aktiv": len(self.spieler_daten),
            "produkte_hergestellt_gesamt": sum(s.produkte_hergestellt for s in self.spieler_daten.values()),
            "meisterwerke_gesamt": sum(s.meisterwerke_erstellt for s in self.spieler_daten.values()),
            "explosionen_gesamt": sum(s.explosionen_verursacht for s in self.spieler_daten.values())
        }

    # --- Hilfsfunktionen ---

    def _get_oder_erstelle_spieler(self, spieler_id: str) -> SpielerAlchemie:
        """Holt oder erstellt Spieler-Daten"""
        if spieler_id not in self.spieler_daten:
            self.spieler_daten[spieler_id] = SpielerAlchemie(spieler_id=spieler_id)
        return self.spieler_daten[spieler_id]

    def _save_state(self):
        """Speichert State"""
        state = {
            "spieler_daten": {k: v.to_dict() for k, v in self.spieler_daten.items()},
            # Entdeckte Rezepte separat speichern
            "spieler_rezepte": {k: v.entdeckte_rezepte for k, v in self.spieler_daten.items()},
            "spieler_inventare": {k: v.zutaten_inventar for k, v in self.spieler_daten.items()},
            "spieler_produkte": {k: v.produkte for k, v in self.spieler_daten.items()}
        }

        path = Path(__file__).parent / "alchemy_state.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        """Lädt State"""
        path = Path(__file__).parent / "alchemy_state.json"
        if not path.exists():
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)

            for spieler_id, daten in state.get("spieler_daten", {}).items():
                spieler = SpielerAlchemie(
                    spieler_id=spieler_id,
                    skill_level=daten.get("skill_level", 1),
                    skill_exp=daten.get("skill_exp", 0),
                    skill_exp_next=daten.get("skill_exp_next", 100),
                    produkte_hergestellt=daten.get("produkte_hergestellt", 0),
                    experimente_durchgefuehrt=daten.get("experimente_durchgefuehrt", 0),
                    meisterwerke_erstellt=daten.get("meisterwerke_erstellt", 0),
                    explosionen_verursacht=daten.get("explosionen_verursacht", 0)
                )

                # Entdeckte Rezepte
                spieler.entdeckte_rezepte = state.get("spieler_rezepte", {}).get(spieler_id, [])

                # Inventar
                spieler.zutaten_inventar = state.get("spieler_inventare", {}).get(spieler_id, {})

                # Produkte
                spieler.produkte = state.get("spieler_produkte", {}).get(spieler_id, [])

                self.spieler_daten[spieler_id] = spieler

        except Exception as e:
            print(f"[ALCHEMY] Fehler beim Laden: {e}")


# ============================================================
# SINGLETON
# ============================================================

_system: Optional[AlchemieSystem] = None

def get_alchemy_system() -> AlchemieSystem:
    """Gibt Singleton-Instanz zurück"""
    global _system
    if _system is None:
        _system = AlchemieSystem()
    return _system


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("🧪 Alchemy-System Test")
    print("=" * 50)

    system = get_alchemy_system()

    # Test: Zutaten sammeln
    print("\n1. Sammle Zutaten...")
    result = system.sammle_zutat("test_player", "heilkraut", 5)
    print(f"   {result.get('zutat', {}).get('name')}: {result.get('menge')} gesammelt")

    result = system.sammle_zutat("test_player", "heilpilz", 3)
    print(f"   {result.get('zutat', {}).get('name')}: {result.get('menge')} gesammelt")

    # Test: Crafting
    print("\n2. Stelle kleinen Heiltrank her...")
    result = system.stelle_her("test_player", "kleiner_heiltrank")
    print(f"   Erfolg: {result.get('erfolg')}")
    print(f"   Qualität: {result.get('qualitaet_name')}")
    print(f"   Nachricht: {result.get('nachricht')}")

    # Test: Experimentieren
    print("\n3. Experimentiere...")
    system.sammle_zutat("test_player", "schwefel", 2)
    system.sammle_zutat("test_player", "salz", 1)
    result = system.experimentiere("test_player", ["schwefel", "schwefel", "salz"])
    print(f"   Entdeckt: {result.get('entdeckt')}")
    print(f"   Nachricht: {result.get('nachricht')}")

    # Stats
    print("\n4. System Stats:")
    stats = system.get_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")

    print("\n✅ Test abgeschlossen!")
