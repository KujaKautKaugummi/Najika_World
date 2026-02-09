"""
NAJIKA WORLD - Wandernde Bardin & Taten-Bestätigungs-System
============================================================
Inspiriert von: Tiny Tina's Wonderlands

Die wandernde Bardin reist von Stadt zu Stadt und erzählt Geschichten
über Spieler mit hohem Kopfgeld. Mit ihrem speziellen Item können
Spieler ihre Taten BESTÄTIGEN lassen - sie wird zur Zeugin!

WICHTIG:
- Quests NUR in der Wildnis (zwischen Städten)
- In Städten nur Gespräche + Geschichten hören
- Item gibt KEINE Buffs - nur Bestätigung!
- Sie spielt MUNDHARMONIKA beim Erzählen!

Erstellt: 2026-02-01
Autor: OPUS-1 (Backend)
"""

import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# ============================================================
# ENUMS & DATA CLASSES
# ============================================================

class TatKategorie(Enum):
    """Kategorien von Taten die bezeugt werden können"""
    KAMPF = "kampf"              # Gegner besiegt
    BOSS = "boss"                # Boss besiegt
    RETTUNG = "rettung"          # NPC/Spieler gerettet
    ENTDECKUNG = "entdeckung"    # Ort/Geheimnis entdeckt
    QUEST = "quest"              # Quest abgeschlossen
    CRAFTING = "crafting"        # Legendäres Item gecraftet
    HANDEL = "handel"            # Großer Deal abgeschlossen
    CHAOS = "chaos"              # Verrückte Tat (Oregon Trail Event)
    DIEBSTAHL = "diebstahl"      # Erfolgreicher Raub
    DUELL = "duell"              # PvP Sieg


class BardStimmung(Enum):
    """Stimmung der Bardin - beeinflusst Erzählstil"""
    AUFGEREGT = "aufgeregt"      # Dramatisch, laut
    MELANCHOLISCH = "melancholisch"  # Traurig, poetisch
    VERRÜCKT = "verrückt"        # Tiny Tina Mode!
    GEHEIMNISVOLL = "geheimnisvoll"  # Flüsternd, mystisch
    BETRUNKEN = "betrunken"      # Lustig, durcheinander


@dataclass
class BezeugteТat:
    """Eine bezeugte Tat eines Spielers"""
    id: str
    spieler_id: str
    spieler_name: str
    kategorie: TatKategorie
    beschreibung: str
    details: Dict[str, Any]
    ort: str
    region: str
    zeitstempel: datetime
    mundharmonika_melodie: str  # Welche Melodie sie dazu spielt
    erzähl_count: int = 0       # Wie oft wurde es schon erzählt

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "spieler_id": self.spieler_id,
            "spieler_name": self.spieler_name,
            "kategorie": self.kategorie.value,
            "beschreibung": self.beschreibung,
            "details": self.details,
            "ort": self.ort,
            "region": self.region,
            "zeitstempel": self.zeitstempel.isoformat(),
            "mundharmonika_melodie": self.mundharmonika_melodie,
            "erzähl_count": self.erzähl_count
        }


@dataclass
class BardQuest:
    """Quest von der Bardin"""
    id: str
    titel: str
    beschreibung: str
    typ: str  # escort, fetch, crazy
    ziel_region: Optional[str]
    belohnung_item: bool  # Gibt Zeugen-Item
    schwierigkeit: int  # 1-5
    crazy_faktor: int   # 1-10 (Tiny Tina Verrücktheit)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titel": self.titel,
            "beschreibung": self.beschreibung,
            "typ": self.typ,
            "ziel_region": self.ziel_region,
            "belohnung_item": self.belohnung_item,
            "schwierigkeit": self.schwierigkeit,
            "crazy_faktor": self.crazy_faktor
        }


# ============================================================
# DIE BARDIN - NPC KLASSE
# ============================================================

class WanderndeBardin:
    """
    DIE ECHOHARP, KLANG DER WAHRHEIT
    ================================

    WICHTIG: "Echoharp" ist KEIN Name - es ist eine BEZEICHNUNG!
    Sie hat ihren echten Namen aufgegeben (Ritual des Alten Volkes).

    Die Letzte ihres Ordens - der Chronisten aus den Wüsten-Pyramiden.
    Wandert seit Ewigkeiten und sammelt Wahrheit.
    Spielt verrückt um nicht aufzufallen.

    - Wildnis: Quests & Zeugen-Item
    - Städte: Geschichten erzählen
    - Kampfturm: BOSS-FIGHT - Wahres Selbst enthüllt!

    Siehe: DOCS/ECHOHARP_LORE_KOMPLETT.md für volle Lore!
    """

    # Die Bezeichnung (KEIN Name!)
    BEZEICHNUNG = "Echoharp"
    VOLLER_TITEL = "Echoharp, Klang der Wahrheit"

    # Für NPCs die über sie reden
    ANREDEN = [
        "Die Echoharp",
        "Echoharp",
        "Der Klang der Wahrheit",
        "Die Wandernde",
        "Die Chronistin",  # Nur wer Pyramiden kennt
    ]

    # Mundharmonika Melodien für verschiedene Tat-Kategorien
    MELODIEN = {
        TatKategorie.KAMPF: "Stahlklang-Blues",
        TatKategorie.BOSS: "Titanensturz-Hymne",
        TatKategorie.RETTUNG: "Heldenlicht-Ballade",
        TatKategorie.ENTDECKUNG: "Nebelwanderer-Weise",
        TatKategorie.QUEST: "Pfadsucher-Melodie",
        TatKategorie.CRAFTING: "Ambosstanz",
        TatKategorie.HANDEL: "Goldklirren-Walzer",
        TatKategorie.CHAOS: "Wahnsinnstornado",  # Für Oregon Trail Events!
        TatKategorie.DIEBSTAHL: "Schattenflüstern",
        TatKategorie.DUELL: "Rivalenfeuer",
    }

    def __init__(self):
        self.bezeichnung = self.BEZEICHNUNG
        self.voller_titel = self.VOLLER_TITEL
        self.aktuelle_region: Optional[str] = None
        self.aktueller_ort: str = "unterwegs"  # "unterwegs" oder Stadtname
        self.stimmung: BardStimmung = BardStimmung.AUFGEREGT
        self.bekannte_geschichten: List[BezeugteТat] = []
        self.aktive_beobachtung: Dict[str, dict] = {}  # spieler_id -> pending witness

    def ist_in_wildnis(self) -> bool:
        """Prüft ob Bardin gerade in der Wildnis ist (für Quests)"""
        return self.aktueller_ort == "unterwegs"

    def bewege_zu(self, ziel: str, region: str):
        """Bewegt Bardin zu neuem Ort"""
        self.aktueller_ort = ziel
        self.aktuelle_region = region
        # Stimmung wechselt zufällig beim Reisen
        self.stimmung = random.choice(list(BardStimmung))

    def get_begrüßung(self) -> str:
        """Generiert Begrüßung basierend auf Stimmung"""
        begrüßungen = {
            BardStimmung.AUFGEREGT: [
                f"HEY DU DA! *spielt wilden Akkord* Ich bin die {self.bezeichnung}! Klang der Wahrheit! Willst du Geschichten hören oder MACHEN?!",
                f"OHOHO! Ein Abenteurer! *Mundharmonika kreischt* Ich RIECHE Potential! Die {self.bezeichnung} vergisst NIE ein Gesicht!",
            ],
            BardStimmung.MELANCHOLISCH: [
                f"*seufzt und spielt traurige Melodie* Ah... noch ein Wanderer auf dem Pfad des Schicksals... Ich habe so viele kommen und gehen sehen...",
                f"Die Straßen sind lang und die Geschichten... *spielt leise* ...noch länger. Ich trage sie alle. Alle...",
            ],
            BardStimmung.VERRÜCKT: [
                f"BWAHAHAHA! *spielt chaotische Töne* Du siehst aus wie jemand der DINGE TUT! Verrückte Dinge! ICH MAG VERRÜCKTE DINGE!",
                f"*hüpft herum und spielt* Hast du schonmal einen Drachen mit einer KÄSEREIBE bekämpft?! NEIN?! Langweilig! Aber die {self.bezeichnung} kann dich BERÜHMT machen!",
            ],
            BardStimmung.GEHEIMNISVOLL: [
                f"*flüstert und spielt leise* Die Winde tragen Geschichten... und ich trage sie weiter... seit so langer Zeit...",
                f"Psst... *mysteriöse Melodie* Ich weiß Dinge. Dinge über DICH. Dinge über... nein, vergiss das. Willst du eine Quest?",
            ],
            BardStimmung.BETRUNKEN: [
                f"*schwankt und spielt schief* Heeey du! *hicks* Ich bin... wer bin ich nochmal? Die... die Echoharp! Ja! Klang der... der Dinge! *hicks*",
                f"PROSIT! *spielt fröhlich aber falsch* Du siehst aus wie ein HELD! Oder ein Schurke! Ich hab BEIDES gesehen! Öfter als du denkst... *kichert*",
            ],
        }
        return random.choice(begrüßungen.get(self.stimmung, begrüßungen[BardStimmung.AUFGEREGT]))


# ============================================================
# ZEUGEN-ITEM SYSTEM
# ============================================================

class ZeugenItem:
    """
    Das Zeugen-Item - Bestätigt Taten durch die Bardin

    KEINE Buffs! Nur Bestätigung dass DU es warst!
    """

    ITEM_NAME = "Echokristall der Wahrheit"
    ITEM_BESCHREIBUNG = """Ein schimmernder Kristall, der Taten aufzeichnet.

    VORHER aktivieren: Die nächste besondere Tat wird bezeugt.
    NACHHER aktivieren: Die letzte besondere Tat wird bezeugt.

    Die wandernde Bardin wird davon singen - und ALLE werden wissen,
    dass DU es warst. Keine Gerüchte. Keine Zweifel. WAHRHEIT."""

    def __init__(self, besitzer_id: str, besitzer_name: str):
        self.besitzer_id = besitzer_id
        self.besitzer_name = besitzer_name
        self.aufladungen: int = 1  # Startet mit 1, Quest gibt neue
        self.aktiv_vorher: bool = False  # Wartet auf nächste Tat
        self.letzte_tat: Optional[dict] = None  # Für nachher-Aktivierung

    def aktiviere_vorher(self) -> dict:
        """Aktiviert Item für NÄCHSTE Tat"""
        if self.aufladungen <= 0:
            return {
                "erfolg": False,
                "nachricht": "Der Kristall ist leer. Finde die Bardin für neue Aufladungen!"
            }

        self.aktiv_vorher = True
        return {
            "erfolg": True,
            "nachricht": "Der Kristall glüht... Deine NÄCHSTE besondere Tat wird bezeugt werden!"
        }

    def aktiviere_nachher(self) -> dict:
        """Aktiviert Item für LETZTE Tat"""
        if self.aufladungen <= 0:
            return {
                "erfolg": False,
                "nachricht": "Der Kristall ist leer. Finde die Bardin für neue Aufladungen!"
            }

        if not self.letzte_tat:
            return {
                "erfolg": False,
                "nachricht": "Es gibt keine kürzliche Tat zum Bezeugen!"
            }

        self.aufladungen -= 1
        tat = self.letzte_tat
        self.letzte_tat = None

        return {
            "erfolg": True,
            "nachricht": f"Der Kristall leuchtet auf! Deine Tat wird bezeugt: {tat['beschreibung']}",
            "tat": tat
        }

    def registriere_tat(self, kategorie: TatKategorie, beschreibung: str,
                        details: dict, ort: str, region: str) -> Optional[dict]:
        """
        Registriert eine Tat - wird bezeugt wenn Item aktiv war

        Returns: BezeugteТat dict wenn bezeugt, sonst None
        """
        tat_data = {
            "kategorie": kategorie.value,
            "beschreibung": beschreibung,
            "details": details,
            "ort": ort,
            "region": region,
            "zeitstempel": datetime.now().isoformat()
        }

        # Speichere als letzte Tat für nachher-Aktivierung
        self.letzte_tat = tat_data

        # Wenn vorher aktiviert war, bezeugen!
        if self.aktiv_vorher:
            self.aktiv_vorher = False
            self.aufladungen -= 1
            return {
                "bezeugt": True,
                "tat": tat_data,
                "nachricht": f"Der Kristall BLITZT! Die Bardin wird davon singen: {beschreibung}"
            }

        return None  # Nicht bezeugt

    def aufladen(self, anzahl: int = 1):
        """Lädt Item auf (durch Quest-Belohnung)"""
        self.aufladungen += anzahl

    def to_dict(self) -> dict:
        return {
            "name": self.ITEM_NAME,
            "beschreibung": self.ITEM_BESCHREIBUNG,
            "besitzer_id": self.besitzer_id,
            "besitzer_name": self.besitzer_name,
            "aufladungen": self.aufladungen,
            "aktiv_vorher": self.aktiv_vorher,
            "hat_letzte_tat": self.letzte_tat is not None
        }


# ============================================================
# QUEST GENERATOR
# ============================================================

class BardQuestGenerator:
    """Generiert verrückte Quests für die Bardin (Tiny Tina Style!)"""

    ESCORT_QUESTS = [
        {
            "titel": "Die singende Eskorte",
            "beschreibung": "Bring mich nach {ziel}! Aber VORSICHT - ich singe die ganze Zeit und das lockt Monster an!",
            "crazy_faktor": 3
        },
        {
            "titel": "Mundharmonika-Marathon",
            "beschreibung": "Ich muss nach {ziel} - SCHNELL! Meine Mundharmonika hat ein Konzert! Was? Instrumente können keine Konzerte haben? DEINE KANN DAS VIELLEICHT NICHT!",
            "crazy_faktor": 7
        },
        {
            "titel": "Die Flucht vor dem Fan",
            "beschreibung": "Ein SEHR enthusiastischer Fan verfolgt mich seit drei Städten. Bring mich nach {ziel} OHNE dass er uns findet! Er will meine Mundharmonika heiraten. HEIRATEN!",
            "crazy_faktor": 9
        },
    ]

    FETCH_QUESTS = [
        {
            "titel": "Die verlorene Harmonie",
            "beschreibung": "Meine Lieblings-Mundharmonika! Ein Vogel hat sie gestohlen! Er dachte es wäre ein... glänzender... Wurm? ICH WEISS AUCH NICHT! Finde sie!",
            "crazy_faktor": 5
        },
        {
            "titel": "Die legendäre Saite",
            "beschreibung": "Ich brauche eine Saite aus dem Bart eines Zwergen-Königs. Warte - Mundharmonikas haben keine Saiten? DIESE HIER SCHON! Frag nicht!",
            "crazy_faktor": 8
        },
        {
            "titel": "Echo-Sammlung",
            "beschreibung": "Ich brauche das Echo eines Drachen-Rülpsers. Ja wirklich. NEIN ich erkläre nicht warum! Mach einfach!",
            "crazy_faktor": 10
        },
    ]

    CRAZY_QUESTS = [
        {
            "titel": "Der Geschichten-Dieb",
            "beschreibung": "JEMAND STIEHLT MEINE GESCHICHTEN! Buchstäblich! Die Worte verschwinden während ich rede! Finde den Dieb bevor ich nur noch summen kann!",
            "crazy_faktor": 10
        },
        {
            "titel": "Die umgekehrte Melodie",
            "beschreibung": "Ich habe versehentlich eine Melodie RÜCKWÄRTS gespielt und jetzt redet alles in meiner Nähe verkehrt herum! Finde seiW neie jemanden der das umkehren kann!",
            "crazy_faktor": 10
        },
        {
            "titel": "Duett mit einem Geist",
            "beschreibung": "Ein Geist will mit mir ein Duett spielen - aber er WEINT DABEI SO LAUT dass ich nichts höre! Finde heraus warum er weint. Dann können wir endlich JAMMEN!",
            "crazy_faktor": 8
        },
    ]

    @classmethod
    def generiere_quest(cls, typ: str = "random", ziel_region: str = None) -> BardQuest:
        """Generiert eine Quest basierend auf Typ"""

        if typ == "random":
            typ = random.choice(["escort", "fetch", "crazy"])

        if typ == "escort":
            template = random.choice(cls.ESCORT_QUESTS)
            ziel = ziel_region or random.choice([
                "Runenheim", "Funkensiedlung", "Salzige Bucht",
                "Dampfhain", "Götterfels", "Reich der Drei"
            ])
            return BardQuest(
                id=f"bard_quest_{int(time.time())}",
                titel=template["titel"],
                beschreibung=template["beschreibung"].format(ziel=ziel),
                typ="escort",
                ziel_region=ziel,
                belohnung_item=True,
                schwierigkeit=random.randint(2, 4),
                crazy_faktor=template["crazy_faktor"]
            )

        elif typ == "fetch":
            template = random.choice(cls.FETCH_QUESTS)
            return BardQuest(
                id=f"bard_quest_{int(time.time())}",
                titel=template["titel"],
                beschreibung=template["beschreibung"],
                typ="fetch",
                ziel_region=None,
                belohnung_item=True,
                schwierigkeit=random.randint(2, 4),
                crazy_faktor=template["crazy_faktor"]
            )

        else:  # crazy
            template = random.choice(cls.CRAZY_QUESTS)
            return BardQuest(
                id=f"bard_quest_{int(time.time())}",
                titel=template["titel"],
                beschreibung=template["beschreibung"],
                typ="crazy",
                ziel_region=None,
                belohnung_item=True,
                schwierigkeit=random.randint(3, 5),
                crazy_faktor=template["crazy_faktor"]
            )


# ============================================================
# GESCHICHTEN GENERATOR
# ============================================================

class GeschichtenGenerator:
    """Generiert Erzählungen basierend auf bezeugten Taten"""

    KAMPF_TEMPLATES = [
        "Und DANN! *spielt dramatische Melodie* {spieler} zog {waffe} und ZACK! {gegner} wusste nicht wie ihm geschah! {detail}",
        "*wilde Mundharmonika* {spieler} gegen {gegner}! Ein Kampf für die EWIGKEIT! Und wisst ihr was? {spieler} hat {methode}! UNGLAUBLICH!",
        "Ich SAH es mit eigenen Augen! *spielt* {spieler} stand da, {gegner} kam näher... und BOOM! {detail} Einfach so!",
    ]

    BOSS_TEMPLATES = [
        "*epische Hymne* DER GROSSE {boss}! Gefürchtet von allen! Aber nicht von {spieler}! OH NEIN! {detail}",
        "Alle sagten es wäre unmöglich! *dramatische Pause + Akkord* Aber {spieler}?! {spieler} hat {boss} in den STAUB geschickt! {methode}!",
        "*flüstert* Der legendäre {boss}... *LAUT* BESIEGT! VON {spieler}! *spielt triumphale Melodie* {detail}",
    ]

    CHAOS_TEMPLATES = [
        "BWAHAHA! *chaotische Melodie* Das war SO VERRÜCKT! {spieler} hat {tat}! Wer MACHT sowas?! EIN HELD! ODER EIN WAHNSINNIGER! ODER BEIDES!",
        "*kann kaum spielen vor Lachen* Ihr... ihr glaubt mir nicht! {spieler} hat WIRKLICH {tat}! ICH WAR DABEI!",
        "Das ist die BESTE Geschichte die ich je erzählen durfte! *wilde Töne* {spieler}! {tat}! Die Welt wird das NIEMALS vergessen!",
    ]

    @classmethod
    def generiere_geschichte(cls, tat: BezeugteТat, stimmung: BardStimmung) -> str:
        """Generiert eine Geschichte basierend auf Tat und Stimmung"""

        details = tat.details

        if tat.kategorie == TatKategorie.KAMPF:
            template = random.choice(cls.KAMPF_TEMPLATES)
            return template.format(
                spieler=tat.spieler_name,
                waffe=details.get("waffe", "eine Waffe"),
                gegner=details.get("gegner", "den Feind"),
                methode=details.get("methode", "gewonnen"),
                detail=details.get("detail", "Es war episch!")
            )

        elif tat.kategorie == TatKategorie.BOSS:
            template = random.choice(cls.BOSS_TEMPLATES)
            return template.format(
                spieler=tat.spieler_name,
                boss=details.get("boss", "Boss"),
                methode=details.get("methode", "sie besiegt"),
                detail=details.get("detail", "Legendär!")
            )

        elif tat.kategorie == TatKategorie.CHAOS:
            template = random.choice(cls.CHAOS_TEMPLATES)
            return template.format(
                spieler=tat.spieler_name,
                tat=tat.beschreibung
            )

        else:
            # Generische Geschichte
            return f"*spielt {tat.mundharmonika_melodie}* {tat.spieler_name} hat Großes vollbracht! {tat.beschreibung}! Ich war Zeuge!"


# ============================================================
# HAUPT-SYSTEM MANAGER
# ============================================================

class BardWitnessSystem:
    """
    Haupt-Manager für das Bardin & Zeugen-System

    Verwaltet:
    - Die wandernde Bardin (Position, Quests, Geschichten)
    - Spieler Zeugen-Items
    - Bezeugte Taten (global für alle Spieler)
    """

    def __init__(self):
        self.bardin = WanderndeBardin()  # Echoharp, Klang der Wahrheit
        self.spieler_items: Dict[str, ZeugenItem] = {}
        self.bezeugte_taten: List[BezeugteТat] = []
        self.globale_geschichten: List[dict] = []  # Was in Tavernen erzählt wird

    # --- Bardin Management ---

    def get_bardin_status(self) -> dict:
        """Gibt aktuellen Status der Echoharp zurück"""
        return {
            "bezeichnung": self.bardin.bezeichnung,
            "voller_titel": self.bardin.voller_titel,
            "ort": self.bardin.aktueller_ort,
            "region": self.bardin.aktuelle_region,
            "stimmung": self.bardin.stimmung.value,
            "ist_in_wildnis": self.bardin.ist_in_wildnis(),
            "bekannte_geschichten": len(self.bardin.bekannte_geschichten),
            "begrüßung": self.bardin.get_begrüßung()
        }

    def bewege_bardin(self, ziel: str, region: str):
        """Bewegt Bardin zu neuem Ort"""
        self.bardin.bewege_zu(ziel, region)
        return self.get_bardin_status()

    # --- Quest System ---

    def get_quest(self, spieler_id: str) -> dict:
        """
        Gibt Quest von Bardin - NUR wenn in Wildnis!
        """
        if not self.bardin.ist_in_wildnis():
            return {
                "erfolg": False,
                "nachricht": f"*{self.bardin.name} winkt ab* Quests? HIER? In der Stadt? Nee nee, triff mich draußen in der Wildnis! Da passieren die ECHTEN Abenteuer!",
                "grund": "bardin_in_stadt"
            }

        quest = BardQuestGenerator.generiere_quest()
        return {
            "erfolg": True,
            "quest": quest.to_dict(),
            "nachricht": f"*{self.bardin.name} grinst verrückt* OHOHO! Du willst eine Aufgabe?! {quest.beschreibung}"
        }

    def quest_abschließen(self, spieler_id: str, spieler_name: str, quest_id: str) -> dict:
        """Quest abschließen und Zeugen-Item erhalten"""

        # Item erstellen oder aufladen
        if spieler_id not in self.spieler_items:
            self.spieler_items[spieler_id] = ZeugenItem(spieler_id, spieler_name)
            nachricht = f"*{self.bardin.name} überreicht einen schimmernden Kristall* DA! Der {ZeugenItem.ITEM_NAME}! Damit werden deine Taten zur WAHRHEIT!"
        else:
            self.spieler_items[spieler_id].aufladen(1)
            nachricht = f"*{self.bardin.name} berührt deinen Kristall* Eine neue Aufladung! Geh raus und tu DINGE!"

        return {
            "erfolg": True,
            "item": self.spieler_items[spieler_id].to_dict(),
            "nachricht": nachricht
        }

    # --- Zeugen-Item System ---

    def aktiviere_item_vorher(self, spieler_id: str) -> dict:
        """Aktiviert Zeugen-Item für nächste Tat"""
        if spieler_id not in self.spieler_items:
            return {
                "erfolg": False,
                "nachricht": "Du hast keinen Echokristall! Finde die wandernde Bardin in der Wildnis!"
            }
        return self.spieler_items[spieler_id].aktiviere_vorher()

    def aktiviere_item_nachher(self, spieler_id: str) -> dict:
        """Aktiviert Zeugen-Item für letzte Tat"""
        if spieler_id not in self.spieler_items:
            return {
                "erfolg": False,
                "nachricht": "Du hast keinen Echokristall! Finde die wandernde Bardin in der Wildnis!"
            }

        result = self.spieler_items[spieler_id].aktiviere_nachher()

        if result["erfolg"] and "tat" in result:
            # Tat zur globalen Liste hinzufügen
            self._tat_bezeugen(spieler_id, result["tat"])

        return result

    def registriere_tat(self, spieler_id: str, kategorie: str,
                        beschreibung: str, details: dict,
                        ort: str, region: str) -> dict:
        """
        Registriert eine Tat eines Spielers

        Wird automatisch bezeugt wenn Item aktiv war!
        """
        if spieler_id not in self.spieler_items:
            # Spieler hat kein Item - Tat wird nicht bezeugt
            return {
                "bezeugt": False,
                "nachricht": "Deine Tat bleibt ein Gerücht... ohne Zeugen weiß niemand ob DU es wirklich warst."
            }

        try:
            kat = TatKategorie(kategorie)
        except ValueError:
            kat = TatKategorie.CHAOS  # Default

        result = self.spieler_items[spieler_id].registriere_tat(
            kategorie=kat,
            beschreibung=beschreibung,
            details=details,
            ort=ort,
            region=region
        )

        if result and result.get("bezeugt"):
            self._tat_bezeugen(spieler_id, result["tat"])
            return result

        return {
            "bezeugt": False,
            "nachricht": "Tat registriert. Aktiviere deinen Kristall NACHHER um sie zu bezeugen!"
        }

    def _tat_bezeugen(self, spieler_id: str, tat_data: dict):
        """Interne Methode: Fügt bezeugte Tat zur globalen Liste hinzu"""

        spieler_name = self.spieler_items[spieler_id].besitzer_name
        kategorie = TatKategorie(tat_data["kategorie"])

        bezeugte_tat = BezeugteТat(
            id=f"tat_{int(time.time())}_{spieler_id[:8]}",
            spieler_id=spieler_id,
            spieler_name=spieler_name,
            kategorie=kategorie,
            beschreibung=tat_data["beschreibung"],
            details=tat_data["details"],
            ort=tat_data["ort"],
            region=tat_data["region"],
            zeitstempel=datetime.now(),
            mundharmonika_melodie=WanderndeBardin.MELODIEN.get(kategorie, "Unbekannte Weise")
        )

        self.bezeugte_taten.append(bezeugte_tat)
        self.bardin.bekannte_geschichten.append(bezeugte_tat)

        # Geschichte generieren für Tavernen
        geschichte = GeschichtenGenerator.generiere_geschichte(bezeugte_tat, self.bardin.stimmung)
        self.globale_geschichten.append({
            "tat_id": bezeugte_tat.id,
            "spieler": spieler_name,
            "text": geschichte,
            "zeitstempel": datetime.now().isoformat()
        })

    # --- Geschichten Abruf ---

    def get_geschichten_für_taverne(self, region: str = None, limit: int = 5) -> List[dict]:
        """Gibt Geschichten zurück die in Tavernen erzählt werden"""
        geschichten = self.globale_geschichten

        if region:
            # Filter nach Region
            geschichten = [g for g in geschichten
                          if any(t.region == region for t in self.bezeugte_taten
                                if t.id == g["tat_id"])]

        # Neueste zuerst
        geschichten = sorted(geschichten,
                           key=lambda x: x["zeitstempel"],
                           reverse=True)[:limit]

        return geschichten

    def get_spieler_taten(self, spieler_id: str) -> List[dict]:
        """Gibt alle bezeugten Taten eines Spielers zurück"""
        return [t.to_dict() for t in self.bezeugte_taten
                if t.spieler_id == spieler_id]

    def get_top_kopfgeld_geschichten(self, limit: int = 10) -> List[dict]:
        """
        Gibt Geschichten über Spieler mit höchstem Kopfgeld zurück
        TODO: Integration mit Kopfgeld-System
        """
        # Erstmal alle Geschichten, später mit Kopfgeld-System verknüpfen
        return self.globale_geschichten[:limit]


# ============================================================
# GLOBALE INSTANZ
# ============================================================

# Singleton für Server-weite Nutzung
_bard_system: Optional[BardWitnessSystem] = None

def get_bard_system() -> BardWitnessSystem:
    """Gibt globale Instanz des Bardin-Systems zurück"""
    global _bard_system
    if _bard_system is None:
        _bard_system = BardWitnessSystem()
    return _bard_system


# ============================================================
# API ROUTES (für najika_server.py Integration)
# ============================================================

def register_bard_routes(app):
    """
    Registriert Flask-Routes für das Bardin-System

    Aufrufen in najika_server.py:
    from najika_bard_witness_system import register_bard_routes
    register_bard_routes(app)
    """
    from flask import jsonify, request

    system = get_bard_system()

    @app.route('/api/bard/status', methods=['GET'])
    def bard_status():
        """GET: Status der wandernden Bardin"""
        return jsonify(system.get_bardin_status())

    @app.route('/api/bard/quest', methods=['GET'])
    def bard_quest():
        """GET: Quest von Bardin (nur in Wildnis!)"""
        spieler_id = request.args.get('spieler_id', 'default')
        return jsonify(system.get_quest(spieler_id))

    @app.route('/api/bard/quest/complete', methods=['POST'])
    def bard_quest_complete():
        """POST: Quest abschließen und Item erhalten"""
        data = request.get_json()
        return jsonify(system.quest_abschließen(
            spieler_id=data.get('spieler_id', 'default'),
            spieler_name=data.get('spieler_name', 'Unbekannt'),
            quest_id=data.get('quest_id', '')
        ))

    @app.route('/api/bard/item/status', methods=['GET'])
    def bard_item_status():
        """GET: Status des Spieler-Items"""
        spieler_id = request.args.get('spieler_id', 'default')
        if spieler_id in system.spieler_items:
            return jsonify(system.spieler_items[spieler_id].to_dict())
        return jsonify({"error": "Kein Item", "nachricht": "Du hast keinen Echokristall!"})

    @app.route('/api/bard/item/activate/before', methods=['POST'])
    def bard_activate_before():
        """POST: Item für NÄCHSTE Tat aktivieren"""
        data = request.get_json()
        return jsonify(system.aktiviere_item_vorher(data.get('spieler_id', 'default')))

    @app.route('/api/bard/item/activate/after', methods=['POST'])
    def bard_activate_after():
        """POST: Item für LETZTE Tat aktivieren"""
        data = request.get_json()
        return jsonify(system.aktiviere_item_nachher(data.get('spieler_id', 'default')))

    @app.route('/api/bard/deed/register', methods=['POST'])
    def bard_register_deed():
        """POST: Tat registrieren (wird bezeugt wenn Item aktiv)"""
        data = request.get_json()
        return jsonify(system.registriere_tat(
            spieler_id=data.get('spieler_id', 'default'),
            kategorie=data.get('kategorie', 'chaos'),
            beschreibung=data.get('beschreibung', 'Eine Tat'),
            details=data.get('details', {}),
            ort=data.get('ort', 'Unbekannt'),
            region=data.get('region', 'Unbekannt')
        ))

    @app.route('/api/bard/stories', methods=['GET'])
    def bard_stories():
        """GET: Geschichten für Tavernen"""
        region = request.args.get('region')
        limit = int(request.args.get('limit', 5))
        return jsonify(system.get_geschichten_für_taverne(region, limit))

    @app.route('/api/bard/player/deeds', methods=['GET'])
    def bard_player_deeds():
        """GET: Bezeugte Taten eines Spielers"""
        spieler_id = request.args.get('spieler_id', 'default')
        return jsonify(system.get_spieler_taten(spieler_id))

    print("🎭 Bardin & Zeugen-System: Routes registriert!")
    print("   - GET  /api/bard/status")
    print("   - GET  /api/bard/quest")
    print("   - POST /api/bard/quest/complete")
    print("   - GET  /api/bard/item/status")
    print("   - POST /api/bard/item/activate/before")
    print("   - POST /api/bard/item/activate/after")
    print("   - POST /api/bard/deed/register")
    print("   - GET  /api/bard/stories")
    print("   - GET  /api/bard/player/deeds")


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("🎭 Bardin & Zeugen-System - Test")
    print("=" * 50)

    system = get_bard_system()

    # Test 1: Echoharp Status
    print("\n1. Echoharp Status:")
    status = system.get_bardin_status()
    print(f"   Bezeichnung: {status['bezeichnung']}")
    print(f"   Voller Titel: {status['voller_titel']}")
    print(f"   Ort: {status['ort']}")
    print(f"   Stimmung: {status['stimmung']}")
    print(f"   Begrüßung: {status['begrüßung'][:50]}...")

    # Test 2: Quest holen (sollte klappen - Bardin startet "unterwegs")
    print("\n2. Quest holen:")
    quest = system.get_quest("test_spieler")
    print(f"   Erfolg: {quest['erfolg']}")
    if quest['erfolg']:
        print(f"   Quest: {quest['quest']['titel']}")

    # Test 3: Quest abschließen & Item erhalten
    print("\n3. Quest abschließen:")
    result = system.quest_abschließen("test_spieler", "TestHeld", "quest_123")
    print(f"   Item erhalten: {result['item']['name']}")
    print(f"   Aufladungen: {result['item']['aufladungen']}")

    # Test 4: Item aktivieren & Tat bezeugen
    print("\n4. Item aktivieren (VORHER):")
    result = system.aktiviere_item_vorher("test_spieler")
    print(f"   {result['nachricht']}")

    # Test 5: Tat registrieren (sollte bezeugt werden!)
    print("\n5. Tat registrieren:")
    result = system.registriere_tat(
        spieler_id="test_spieler",
        kategorie="boss",
        beschreibung="Den Feuerlord in einem epischen Kampf besiegt",
        details={
            "boss": "Feuerlord Ignatius",
            "methode": "ihn mit einem Eiskristall-Schwert durchbohrt",
            "detail": "Der Boden schmolz unter seinen Füßen!"
        },
        ort="Vulkan-Gipfel",
        region="Volcano"
    )
    print(f"   Bezeugt: {result.get('bezeugt', False)}")
    if result.get('bezeugt'):
        print(f"   Nachricht: {result['nachricht']}")

    # Test 6: Geschichten abrufen
    print("\n6. Geschichten für Tavernen:")
    geschichten = system.get_geschichten_für_taverne(limit=3)
    for g in geschichten:
        print(f"   - {g['text'][:80]}...")

    print("\n" + "=" * 50)
    print("✅ Test abgeschlossen!")
