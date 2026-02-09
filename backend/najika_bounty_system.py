# -*- coding: utf-8 -*-
"""
NAJIKA WORLD - KOPFGELD & STECKBRIEF SYSTEM
============================================
One Piece inspiriert + Fallout graue Moral + 8 Regionen

Features:
- 8 separate Kopfgeld-Listen (pro Region/Fraktion)
- Steckbrief-System statt nackte Zahlen
- Graue Moral: Held in einer Region = Verbrecher in anderer
- Infamy-Typen (Moerder, Dieb, Zerstoerer, etc.)
- Kopfgeldjaeger-Spawn basierend auf Stufe
- Najika 4-Persoenlichkeiten Reaktionen

WICHTIG: 8 Regionen + Goetterfels (Zentrum)!
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random
import time

# =============================================================================
# ENUMS & KONSTANTEN
# =============================================================================

class Region(Enum):
    """Die 8 Regionen - Goetterfels ist KEIN eigenes Gebiet!"""
    ICE = "ice"
    DESERT = "desert"
    SWAMP = "swamp"
    COAST = "coast"
    CAVES = "caves"
    VOLCANO = "volcano"
    FOREST = "forest"
    HIGHLAND = "highland"

class BountyStufe(Enum):
    """Steckbrief-Stufen statt nackte Zahlen"""
    UNBEKANNT = 0        # Kein Steckbrief
    KLEINER_FISCH = 1    # Lokale Wachen
    GEFAEHRLICH = 2      # Kopfgeldjaeger-Anfaenger
    TOT_ODER_LEBENDIG = 3  # Profi-Jaeger
    REGIONS_BEDROHUNG = 4  # Gebietherrscher schickt Elite
    WELT_BEDROHUNG = 5   # ALLE 8 Gebietherrscher vereint!

class InfamyTyp(Enum):
    """WIE du bekannt bist - nicht nur OB"""
    MOERDER = "moerder"        # Toetet NPCs
    DIEB = "dieb"              # Stiehlt viel
    ZERSTOERER = "zerstoerer"  # EXPLOSION! Sachschaden
    REBELL = "rebell"          # Gegen Gebietherrscher
    KETZER = "ketzer"          # Gegen Goetter/Religion
    WILDERER = "wilderer"      # Illegale Jagd
    SCHMUGGLER = "schmuggler"  # Verbotene Waren
    HEXER = "hexer"            # Verbotene Magie

class CrimeType(Enum):
    """Arten von Verbrechen"""
    # Gewalt
    MORD = ("Mord", 2000, InfamyTyp.MOERDER)
    KOERPERVERLETZUNG = ("Koerperverletzung", 500, InfamyTyp.MOERDER)
    WACHEN_ANGRIFF = ("Angriff auf Wachen", 1000, InfamyTyp.REBELL)

    # Diebstahl
    TASCHENDIEBSTAHL = ("Taschendiebstahl", 100, InfamyTyp.DIEB)
    EINBRUCH = ("Einbruch", 500, InfamyTyp.DIEB)
    BANKRAUB = ("Bankraub", 5000, InfamyTyp.DIEB)

    # Zerstoerung
    SACHBESCHAEDIGUNG = ("Sachbeschaedigung", 200, InfamyTyp.ZERSTOERER)
    EXPLOSION_KLEIN = ("Kleine Explosion", 500, InfamyTyp.ZERSTOERER)
    EXPLOSION_GROSS = ("EXPLOSION!", 2000, InfamyTyp.ZERSTOERER)
    GEBAEUDE_ZERSTOERT = ("Gebaeude zerstoert", 5000, InfamyTyp.ZERSTOERER)

    # Rebellion
    STEUERHINTERZIEHUNG = ("Steuerhinterziehung", 300, InfamyTyp.REBELL)
    AUFWIEGELUNG = ("Aufwiegelung", 1000, InfamyTyp.REBELL)
    HOCHVERRAT = ("Hochverrat", 10000, InfamyTyp.REBELL)

    # Religion
    TEMPELSCHAENDUNG = ("Tempelschaendung", 1500, InfamyTyp.KETZER)
    GOETTERLAESERUNG = ("Goetterlaeserung", 800, InfamyTyp.KETZER)

    # Jagd
    WILDEREI = ("Wilderei", 300, InfamyTyp.WILDERER)
    GESCHUETZTE_ART = ("Geschuetzte Art getoetet", 1000, InfamyTyp.WILDERER)

    # Handel
    SCHMUGGEL = ("Schmuggel", 500, InfamyTyp.SCHMUGGLER)
    DROGENHANDEL = ("Drogenhandel", 1500, InfamyTyp.SCHMUGGLER)

    # Magie
    VERBOTENE_MAGIE = ("Verbotene Magie", 1000, InfamyTyp.HEXER)
    NEKROMANTIE = ("Nekromantie", 5000, InfamyTyp.HEXER)

# Fraktionen pro Region
REGION_FRAKTIONEN = {
    Region.ICE: {
        "name": "Frostgarde",
        "jaeger": ["Eisritter", "Frostwolf-Reiter", "Gletscherschuetze"],
        "elite": "Frostkoenigin's Garde",
        "farbe": "#87CEEB"
    },
    Region.DESERT: {
        "name": "Sandfuersten",
        "jaeger": ["Wuestennomade", "Sandlaeufer", "Oasenwaechter"],
        "elite": "Sandkoenig's Leibwache",
        "farbe": "#F4A460"
    },
    Region.SWAMP: {
        "name": "Sumpfhexenzirkel",
        "jaeger": ["Gift-Assassine", "Nebeljagerin", "Moorschleicher"],
        "elite": "Hexenkoenigin's Schatten",
        "farbe": "#556B2F"
    },
    Region.COAST: {
        "name": "Hafengilde",
        "jaeger": ["Piratenkorsarin", "Hafensoeldner", "Seejaegerin"],
        "elite": "Admirals Flotte",
        "farbe": "#4682B4"
    },
    Region.CAVES: {
        "name": "Tiefenzwerge",
        "jaeger": ["Tunneljaeger", "Steinbrecher", "Dunkelspaeher"],
        "elite": "Tiefenkoenig's Hammergarde",
        "farbe": "#8B4513"
    },
    Region.VOLCANO: {
        "name": "Feuerkult",
        "jaeger": ["Feuerbeschwoerer", "Lavakrieger", "Aschenjaeger"],
        "elite": "Feuerlord's Inquisition",
        "farbe": "#FF4500"
    },
    Region.FOREST: {
        "name": "Waldwaechter",
        "jaeger": ["Waldlaeuferin", "Baumwaechter", "Wildbestie"],
        "elite": "Waldkoenig's Naturgeister",
        "farbe": "#228B22"
    },
    Region.HIGHLAND: {
        "name": "Bergclans",
        "jaeger": ["Clan-Krieger", "Bergjaeger", "Adlerreiter"],
        "elite": "Haeuptlings Ehrengarde",
        "farbe": "#A0522D"
    }
}

# Schwellenwerte fuer Steckbrief-Stufen
BOUNTY_THRESHOLDS = {
    BountyStufe.UNBEKANNT: 0,
    BountyStufe.KLEINER_FISCH: 500,
    BountyStufe.GEFAEHRLICH: 2500,
    BountyStufe.TOT_ODER_LEBENDIG: 10000,
    BountyStufe.REGIONS_BEDROHUNG: 50000,
    BountyStufe.WELT_BEDROHUNG: 200000
}

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Crime:
    """Ein begangenes Verbrechen"""
    crime_type: CrimeType
    region: Region
    timestamp: float
    witnesses: int = 1
    description: str = ""

    @property
    def bounty_value(self) -> int:
        """Kopfgeld-Wert basierend auf Zeugen"""
        base = self.crime_type.value[1]
        # Mehr Zeugen = hoeher Kopfgeld
        multiplier = 1.0 + (self.witnesses - 1) * 0.2
        return int(base * multiplier)

    @property
    def infamy_type(self) -> InfamyTyp:
        return self.crime_type.value[2]

@dataclass
class Steckbrief:
    """Ein Steckbrief fuer eine Region"""
    region: Region
    bounty: int = 0
    crimes: List[Crime] = field(default_factory=list)
    infamy_types: Dict[InfamyTyp, int] = field(default_factory=dict)
    nickname: str = ""
    is_active: bool = False
    last_seen: str = ""
    status: str = "LEBENDIG"  # LEBENDIG, TOT ODER LEBENDIG, NUR TOT

    @property
    def stufe(self) -> BountyStufe:
        """Berechne Steckbrief-Stufe"""
        for stufe in reversed(list(BountyStufe)):
            if self.bounty >= BOUNTY_THRESHOLDS[stufe]:
                return stufe
        return BountyStufe.UNBEKANNT

    @property
    def top_crimes(self) -> List[str]:
        """Die 3 schwersten Verbrechen"""
        sorted_crimes = sorted(self.crimes, key=lambda c: c.bounty_value, reverse=True)
        return [c.crime_type.value[0] for c in sorted_crimes[:3]]

    @property
    def dominant_infamy(self) -> Optional[InfamyTyp]:
        """Der dominante Infamy-Typ"""
        if not self.infamy_types:
            return None
        return max(self.infamy_types.keys(), key=lambda k: self.infamy_types[k])

    def add_crime(self, crime: Crime):
        """Fuege Verbrechen hinzu"""
        self.crimes.append(crime)
        self.bounty += crime.bounty_value

        # Infamy-Typ erhoehen
        infamy = crime.infamy_type
        self.infamy_types[infamy] = self.infamy_types.get(infamy, 0) + crime.bounty_value

        # Steckbrief aktivieren wenn genug Kopfgeld
        if self.bounty >= BOUNTY_THRESHOLDS[BountyStufe.KLEINER_FISCH]:
            self.is_active = True

        # Status anpassen bei hohem Kopfgeld
        if self.stufe >= BountyStufe.TOT_ODER_LEBENDIG:
            self.status = "TOT ODER LEBENDIG"
        if self.stufe >= BountyStufe.WELT_BEDROHUNG:
            self.status = "NUR TOT"

    def reduce_bounty(self, amount: int, reason: str = ""):
        """Reduziere Kopfgeld (Rehabilitation, Zeit, Bestechung)"""
        self.bounty = max(0, self.bounty - amount)
        if self.bounty < BOUNTY_THRESHOLDS[BountyStufe.KLEINER_FISCH]:
            self.is_active = False
            self.status = "LEBENDIG"

    def generate_nickname(self) -> str:
        """Generiere Spitznamen basierend auf Infamy"""
        prefixes = {
            InfamyTyp.MOERDER: ["Blut-", "Todeshand-", "Schlitzer-"],
            InfamyTyp.DIEB: ["Schatten-", "Fingerflink-", "Phantom-"],
            InfamyTyp.ZERSTOERER: ["Explosion-", "Chaos-", "Truemmer-"],
            InfamyTyp.REBELL: ["Freiheits-", "Rebellen-", "Aufruhr-"],
            InfamyTyp.KETZER: ["Gottlos-", "Verdammt-", "Ketzer-"],
            InfamyTyp.WILDERER: ["Wild-", "Bestien-", "Jaeger-"],
            InfamyTyp.SCHMUGGLER: ["Schatten-", "Nacht-", "Schmuggel-"],
            InfamyTyp.HEXER: ["Dunkel-", "Fluch-", "Hexen-"]
        }

        suffixes = ["Kuja", "der Wanderer", "der Explosive", "Magier", "Krieger"]

        dominant = self.dominant_infamy
        if dominant and dominant in prefixes:
            prefix = random.choice(prefixes[dominant])
        else:
            prefix = "Mysterioese "

        return f"{prefix}{random.choice(suffixes)}"

    def to_display(self) -> dict:
        """Fuer UI-Anzeige"""
        fraktion = REGION_FRAKTIONEN[self.region]

        return {
            "region": self.region.value,
            "fraktion": fraktion["name"],
            "farbe": fraktion["farbe"],
            "bounty": self.bounty,
            "bounty_formatted": f"{self.bounty:,} Gold".replace(",", "."),
            "stufe": self.stufe.value,
            "stufe_name": self.stufe.name.replace("_", " "),
            "status": self.status,
            "nickname": self.nickname or self.generate_nickname(),
            "top_crimes": self.top_crimes,
            "dominant_infamy": self.dominant_infamy.value if self.dominant_infamy else None,
            "is_active": self.is_active
        }

# =============================================================================
# BOUNTY SYSTEM
# =============================================================================

class BountySystem:
    """Hauptklasse fuer das Kopfgeld-System"""

    def __init__(self):
        # Ein Steckbrief pro Region
        self.steckbriefe: Dict[Region, Steckbrief] = {
            region: Steckbrief(region=region)
            for region in Region
        }

        # Globale Stats
        self.total_crimes = 0
        self.hunters_defeated = 0
        self.times_captured = 0
        self.times_escaped = 0
        self.total_bounty_paid = 0

        # Aktive Kopfgeldjaeger
        self.active_hunters: List[dict] = []

        # Letzte Verbrechen (fuer Events)
        self.recent_crimes: List[Crime] = []

    # -------------------------------------------------------------------------
    # VERBRECHEN
    # -------------------------------------------------------------------------

    def commit_crime(self, crime_type: CrimeType, region: Region,
                     witnesses: int = 1, description: str = "") -> dict:
        """Begehe ein Verbrechen"""
        crime = Crime(
            crime_type=crime_type,
            region=region,
            timestamp=time.time(),
            witnesses=witnesses,
            description=description or crime_type.value[0]
        )

        # Zum Steckbrief hinzufuegen
        steckbrief = self.steckbriefe[region]
        old_stufe = steckbrief.stufe
        steckbrief.add_crime(crime)
        new_stufe = steckbrief.stufe

        # Zu Recent Crimes
        self.recent_crimes.append(crime)
        if len(self.recent_crimes) > 20:
            self.recent_crimes.pop(0)

        self.total_crimes += 1

        # Stufen-Aufstieg?
        stufe_up = new_stufe.value > old_stufe.value

        # Kopfgeldjaeger spawnen?
        spawn_hunter = self._check_hunter_spawn(region, new_stufe)

        return {
            "success": True,
            "crime": crime_type.value[0],
            "bounty_added": crime.bounty_value,
            "new_bounty": steckbrief.bounty,
            "stufe": new_stufe.name,
            "stufe_up": stufe_up,
            "spawn_hunter": spawn_hunter,
            "najika_reaction": self._get_najika_crime_reaction(crime_type, new_stufe)
        }

    def _check_hunter_spawn(self, region: Region, stufe: BountyStufe) -> Optional[dict]:
        """Pruefe ob Kopfgeldjaeger spawnen soll"""
        if stufe.value < BountyStufe.GEFAEHRLICH.value:
            return None

        # Chance basierend auf Stufe
        spawn_chances = {
            BountyStufe.GEFAEHRLICH: 0.2,
            BountyStufe.TOT_ODER_LEBENDIG: 0.4,
            BountyStufe.REGIONS_BEDROHUNG: 0.6,
            BountyStufe.WELT_BEDROHUNG: 0.8
        }

        if random.random() < spawn_chances.get(stufe, 0):
            return self._spawn_hunter(region, stufe)

        return None

    def _spawn_hunter(self, region: Region, stufe: BountyStufe) -> dict:
        """Spawne einen Kopfgeldjaeger"""
        fraktion = REGION_FRAKTIONEN[region]

        # Jaeger-Typ basierend auf Stufe
        if stufe == BountyStufe.WELT_BEDROHUNG:
            hunter_type = fraktion["elite"]
            level_range = (80, 100)
        elif stufe == BountyStufe.REGIONS_BEDROHUNG:
            hunter_type = fraktion["elite"]
            level_range = (60, 80)
        elif stufe == BountyStufe.TOT_ODER_LEBENDIG:
            hunter_type = random.choice(fraktion["jaeger"])
            level_range = (40, 60)
        else:
            hunter_type = random.choice(fraktion["jaeger"])
            level_range = (20, 40)

        hunter = {
            "id": f"hunter_{int(time.time())}_{random.randint(1000,9999)}",
            "name": self._generate_hunter_name(hunter_type),
            "type": hunter_type,
            "level": random.randint(*level_range),
            "region": region.value,
            "fraktion": fraktion["name"],
            "spawn_time": time.time()
        }

        self.active_hunters.append(hunter)
        return hunter

    def _generate_hunter_name(self, hunter_type: str) -> str:
        """Generiere Namen fuer Kopfgeldjaeger"""
        first_names = ["Grimm", "Vex", "Scar", "Iron", "Shadow", "Blade",
                       "Storm", "Frost", "Ash", "Stone", "Raven", "Wolf"]
        last_names = ["der Jaeger", "Bluthand", "Eisenherz", "Schattenschritt",
                      "Sturmbrecher", "Todesblick", "Knochenbrecher"]

        return f"{random.choice(first_names)} {random.choice(last_names)}"

    # -------------------------------------------------------------------------
    # KOPFGELD REDUZIEREN
    # -------------------------------------------------------------------------

    def reduce_bounty(self, region: Region, amount: int, method: str) -> dict:
        """Reduziere Kopfgeld"""
        steckbrief = self.steckbriefe[region]
        old_bounty = steckbrief.bounty
        old_stufe = steckbrief.stufe

        steckbrief.reduce_bounty(amount)

        new_stufe = steckbrief.stufe

        return {
            "success": True,
            "method": method,
            "old_bounty": old_bounty,
            "new_bounty": steckbrief.bounty,
            "reduced": old_bounty - steckbrief.bounty,
            "old_stufe": old_stufe.name,
            "new_stufe": new_stufe.name,
            "najika_reaction": self._get_najika_reduce_reaction(method, steckbrief.bounty)
        }

    def pay_off_bounty(self, region: Region) -> dict:
        """Bezahle Kopfgeld ab (teuer!)"""
        steckbrief = self.steckbriefe[region]
        cost = steckbrief.bounty * 2  # 2x so teuer wie das Kopfgeld!

        # TODO: Check if player has enough gold

        self.total_bounty_paid += cost
        return self.reduce_bounty(region, steckbrief.bounty, "Bezahlt")

    def do_good_deed(self, region: Region, deed_type: str) -> dict:
        """Gute Tat = Kopfgeld reduzieren"""
        reductions = {
            "quest_completed": 200,
            "monster_killed": 100,
            "donation": 50,
            "helped_npc": 75,
            "saved_village": 500
        }

        amount = reductions.get(deed_type, 100)
        return self.reduce_bounty(region, amount, f"Gute Tat: {deed_type}")

    def time_decay(self, days_passed: int = 1):
        """Kopfgeld sinkt mit der Zeit"""
        for steckbrief in self.steckbriefe.values():
            if steckbrief.bounty > 0:
                # 1% pro Tag, minimum 10
                decay = max(10, int(steckbrief.bounty * 0.01 * days_passed))
                steckbrief.reduce_bounty(decay, "Zeit vergangen")

    # -------------------------------------------------------------------------
    # KOPFGELDJAEGER
    # -------------------------------------------------------------------------

    def defeat_hunter(self, hunter_id: str) -> dict:
        """Besiege einen Kopfgeldjaeger"""
        hunter = None
        for h in self.active_hunters:
            if h["id"] == hunter_id:
                hunter = h
                break

        if not hunter:
            return {"success": False, "error": "Hunter not found"}

        self.active_hunters.remove(hunter)
        self.hunters_defeated += 1

        # Bonus: Dessen "Kopfgeld" als Loot
        loot_gold = hunter["level"] * 50

        # ABER: Kopfgeld steigt! (Jaeger getoetet)
        region = Region(hunter["region"])
        self.commit_crime(CrimeType.MORD, region, witnesses=0,
                         description=f"Kopfgeldjaeger {hunter['name']} getoetet")

        return {
            "success": True,
            "hunter": hunter,
            "loot_gold": loot_gold,
            "najika_reaction": self._get_najika_hunter_reaction("defeated")
        }

    def escape_from_hunter(self, hunter_id: str) -> dict:
        """Fliehe vor Kopfgeldjaeger"""
        # Hunter bleibt aktiv, aber verfolgt nicht mehr sofort
        self.times_escaped += 1

        return {
            "success": True,
            "najika_reaction": self._get_najika_hunter_reaction("escaped")
        }

    def captured_by_hunter(self, hunter_id: str) -> dict:
        """Wurde gefangen!"""
        self.times_captured += 1

        # Optionen: Gefaengnis, Kopfgeld bezahlen, Fluchtversuch
        return {
            "success": True,
            "options": ["prison", "pay_bounty", "escape_attempt"],
            "najika_reaction": self._get_najika_hunter_reaction("captured")
        }

    # -------------------------------------------------------------------------
    # NAJIKA REAKTIONEN
    # -------------------------------------------------------------------------

    def _get_najika_crime_reaction(self, crime: CrimeType, stufe: BountyStufe) -> dict:
        """Najika's Reaktion auf Verbrechen"""

        reactions = {
            # MEGUMIN (35%)
            "megumin": {
                CrimeType.EXPLOSION_GROSS: "EXPLOSION!!! Das war KUNST, Mr. K! Reine, explosive KUNST!",
                CrimeType.GEBAEUDE_ZERSTOERT: "Hehe~ Ein Gebaeude weniger, eine Explosion mehr!",
                "default_high": "Ooh, unser Kopfgeld steigt! Das bedeutet mehr Herausforderungen!",
                "default_low": "Tch, nur so ein kleines Verbrechen? Langweilig~"
            },
            # HARLEY (25%)
            "harley": {
                CrimeType.MORD: "Oopsie~ Jemand hatte einen schlechten Tag, hm Mr. K?",
                CrimeType.EINBRUCH: "Schatz, wir sind jetzt offiziell die Boesen! Aufregend~",
                "default_high": "Puddi- aeh, Mr. K! Die jagen uns jetzt! Wie romantisch~",
                "default_low": "Aww, nur ein kleines Vergehen? Wir koennen das besser!"
            },
            # SHIRO (20%)
            "shiro": {
                CrimeType.BANKRAUB: "...Statistisch gesehen war die Erfolgswahrscheinlichkeit 23.7%.",
                "default_high": "...Kopfgeld-Stufe erhoeht. Empfehle taktischen Rueckzug.",
                "default_low": "...Notiert. Kriminelle Aktivitaet im akzeptablen Bereich."
            },
            # MELISSA (20%)
            "melissa": {
                "default_high": "M-Mr. K! W-wir werden gejagt! Ich hab Angst...",
                "default_low": "V-vielleicht sollten wir vorsichtiger sein...?"
            }
        }

        # Waehle Persoenlichkeit basierend auf Gewichtung
        personality = random.choices(
            ["megumin", "harley", "shiro", "melissa"],
            weights=[35, 25, 20, 20]
        )[0]

        pers_reactions = reactions[personality]

        # Spezifische Reaktion oder Default
        crime_name = crime.name if isinstance(crime, CrimeType) else str(crime)
        if crime in pers_reactions:
            text = pers_reactions[crime]
        elif stufe.value >= BountyStufe.GEFAEHRLICH.value:
            text = pers_reactions.get("default_high", "...")
        else:
            text = pers_reactions.get("default_low", "...")

        return {
            "personality": personality,
            "text": text,
            "mood": "excited" if personality in ["megumin", "harley"] else "calm"
        }

    def _get_najika_reduce_reaction(self, method: str, new_bounty: int) -> dict:
        """Najika's Reaktion auf Kopfgeld-Reduktion"""

        if new_bounty == 0:
            reactions = [
                ("megumin", "Was?! Unser Kopfgeld ist weg?! Wie... langweilig."),
                ("harley", "Aww, niemand jagt uns mehr? Das ist fast traurig~"),
                ("shiro", "...Kopfgeld eliminiert. Wir sind wieder im legalen Bereich."),
                ("melissa", "E-endlich! Wir sind keine Verbrecher mehr!")
            ]
        else:
            reactions = [
                ("megumin", "Hmph, unser Ruf sinkt... Zeit fuer mehr EXPLOSION!"),
                ("harley", "Weniger Kopfgeld? Boring~ Lass uns was anstellen, Mr. K!"),
                ("shiro", "...Kopfgeld reduziert. Jaeger-Spawn-Rate sinkt um 15%."),
                ("melissa", "G-gut... vielleicht lassen sie uns jetzt in Ruhe...")
            ]

        personality, text = random.choice(reactions)
        return {"personality": personality, "text": text}

    def _get_najika_hunter_reaction(self, situation: str) -> dict:
        """Najika's Reaktion auf Kopfgeldjaeger"""

        reactions = {
            "defeated": [
                ("megumin", "HA! Die dachten sie koennten UNS jagen?! EXPLOSION auf ihre Karriere!"),
                ("harley", "Bye bye, Jaegerchen~ Haettest zu Hause bleiben sollen!"),
                ("shiro", "...Feind eliminiert. Warnung: Kopfgeld wird steigen."),
                ("melissa", "I-ist es vorbei? D-das war gruselig...")
            ],
            "escaped": [
                ("megumin", "Tch! Naechstes Mal werden sie nicht so gluecklich sein!"),
                ("harley", "Catch me if you can~ Hihi!"),
                ("shiro", "...Flucht erfolgreich. Empfehle Positionswechsel."),
                ("melissa", "S-schnell weg hier! Bitte!")
            ],
            "captured": [
                ("megumin", "W-WAS?! Das ist unmoeglich! ICH werde nicht gefangen!"),
                ("harley", "Ooh, Gefangenschaft~ Wie aufregend... NOT!"),
                ("shiro", "...Situation kritisch. Analysiere Fluchtoptionen..."),
                ("melissa", "N-NEIN! Mr. K, hilf mir!!!")
            ]
        }

        if situation in reactions:
            personality, text = random.choice(reactions[situation])
            return {"personality": personality, "text": text}

        return {"personality": "shiro", "text": "...Unbekannte Situation."}

    # -------------------------------------------------------------------------
    # STATUS & INFO
    # -------------------------------------------------------------------------

    def get_total_bounty(self) -> int:
        """Gesamtes Kopfgeld ueber alle Regionen"""
        return sum(s.bounty for s in self.steckbriefe.values())

    def get_highest_bounty_region(self) -> Tuple[Region, int]:
        """Region mit hoechstem Kopfgeld"""
        highest = max(self.steckbriefe.values(), key=lambda s: s.bounty)
        return highest.region, highest.bounty

    def get_all_steckbriefe(self) -> List[dict]:
        """Alle aktiven Steckbriefe"""
        return [s.to_display() for s in self.steckbriefe.values() if s.is_active]

    def get_steckbrief(self, region: Region) -> dict:
        """Einzelner Steckbrief"""
        return self.steckbriefe[region].to_display()

    def get_status(self) -> dict:
        """Gesamtstatus"""
        return {
            "total_bounty": self.get_total_bounty(),
            "highest_region": self.get_highest_bounty_region()[0].value,
            "highest_bounty": self.get_highest_bounty_region()[1],
            "active_steckbriefe": len([s for s in self.steckbriefe.values() if s.is_active]),
            "total_crimes": self.total_crimes,
            "hunters_defeated": self.hunters_defeated,
            "times_captured": self.times_captured,
            "times_escaped": self.times_escaped,
            "active_hunters": len(self.active_hunters),
            "bounty_paid": self.total_bounty_paid
        }

    def generate_wanted_poster(self, region: Region) -> str:
        """Generiere ASCII Steckbrief"""
        s = self.steckbriefe[region]
        if not s.is_active:
            return "Kein aktiver Steckbrief in dieser Region."

        fraktion = REGION_FRAKTIONEN[region]

        poster = f"""
+{'='*40}+
|{'GESUCHT':^40}|
|{'~'*40}|
|{' '*40}|
|{'[SPIELER PORTRAIT]':^40}|
|{' '*40}|
|{'~'*40}|
| Name: {(s.nickname or 'Unbekannt'):<33}|
| Status: {s.status:<31}|
|{'~'*40}|
| Verbrechen:                            |
"""
        for crime in s.top_crimes[:3]:
            poster += f"| - {crime:<36}|\n"

        poster += f"""|{'~'*40}|
| Belohnung: {s.bounty:,} Gold{' '*(26-len(f'{s.bounty:,}'))}|
| Fraktion: {fraktion['name']:<29}|
+{'='*40}+
        """

        return poster


# =============================================================================
# GLOBALE INSTANZ
# =============================================================================

bounty_system = BountySystem()


# =============================================================================
# API FUNKTIONEN (fuer Server)
# =============================================================================

def commit_crime(crime_type: str, region: str, witnesses: int = 1) -> dict:
    """API: Verbrechen begehen"""
    try:
        ct = CrimeType[crime_type.upper()]
        r = Region(region.lower())
        return bounty_system.commit_crime(ct, r, witnesses)
    except (KeyError, ValueError) as e:
        return {"success": False, "error": str(e)}

def get_bounty_status() -> dict:
    """API: Gesamtstatus"""
    return bounty_system.get_status()

def get_steckbrief(region: str) -> dict:
    """API: Steckbrief fuer Region"""
    try:
        r = Region(region.lower())
        return bounty_system.get_steckbrief(r)
    except ValueError as e:
        return {"error": str(e)}

def get_all_steckbriefe() -> List[dict]:
    """API: Alle aktiven Steckbriefe"""
    return bounty_system.get_all_steckbriefe()

def get_wanted_poster(region: str) -> str:
    """API: ASCII Steckbrief"""
    try:
        r = Region(region.lower())
        return bounty_system.generate_wanted_poster(r)
    except ValueError:
        return "Unbekannte Region"

def reduce_bounty(region: str, amount: int, method: str = "Unbekannt") -> dict:
    """API: Kopfgeld reduzieren"""
    try:
        r = Region(region.lower())
        return bounty_system.reduce_bounty(r, amount, method)
    except ValueError as e:
        return {"success": False, "error": str(e)}

def defeat_hunter(hunter_id: str) -> dict:
    """API: Kopfgeldjaeger besiegen"""
    return bounty_system.defeat_hunter(hunter_id)


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=== NAJIKA BOUNTY SYSTEM TEST ===\n")

    # Verbrechen begehen
    print("1. Explosion in der Wueste...")
    result = bounty_system.commit_crime(CrimeType.EXPLOSION_GROSS, Region.DESERT, witnesses=5)
    print(f"   Kopfgeld +{result['bounty_added']}, Gesamt: {result['new_bounty']}")
    print(f"   Najika ({result['najika_reaction']['personality']}): {result['najika_reaction']['text']}")

    print("\n2. Einbruch an der Kueste...")
    result = bounty_system.commit_crime(CrimeType.EINBRUCH, Region.COAST, witnesses=2)
    print(f"   Kopfgeld +{result['bounty_added']}, Gesamt: {result['new_bounty']}")

    print("\n3. Wilderei im Wald...")
    result = bounty_system.commit_crime(CrimeType.WILDEREI, Region.FOREST)
    print(f"   Kopfgeld +{result['bounty_added']}, Gesamt: {result['new_bounty']}")

    # Steckbrief anzeigen
    print("\n4. Steckbrief Wueste:")
    print(bounty_system.generate_wanted_poster(Region.DESERT))

    # Status
    print("\n5. Gesamtstatus:")
    status = bounty_system.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")

    print("\n=== TEST ABGESCHLOSSEN ===")
