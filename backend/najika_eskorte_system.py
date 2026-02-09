"""
NAJIKA ESKORTE/SÖLDNER SYSTEM
=============================

"Die Besungenen" - Spieler die von der Echoharp besungen wurden
können andere als Eskorte begleiten.

WICHTIG:
- Söldner = ESKORTE, nicht Kampf-Partner!
- Sie schützen auf dem WEG (auch gegen harte Gegner)
- Sie kämpfen NICHT in Bossen/Dungeons mit!
- 2 Stufen: AI-Abbild (billig) vs Echter Spieler (teuer)
- Rettung: NUR echte Spieler, NUR Legendär-Rang

Author: Claude Code (OPUS-1)
Date: 2026-02-01
"""

import time
import random
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path

# ============================================================
# ENUMS & KONSTANTEN
# ============================================================

class BesungenerRang(Enum):
    """Ränge der Besungenen"""
    UNBEKANNT = "unbekannt"      # < 3 Taten
    BEKANNT = "bekannt"          # 3+ Taten, noch kein Söldner
    BESUNGEN = "besungen"        # 10+ Taten, kann eskortieren
    LEGENDAER = "legendär"       # 50+ Taten, kann retten

class EskorteTyp(Enum):
    """Art der Eskorte"""
    AI_ABBILD = "ai_abbild"      # Billiger, immer verfügbar
    ECHTER_SPIELER = "echter_spieler"  # Teurer, muss online sein

class EskorteStatus(Enum):
    """Status einer aktiven Eskorte"""
    WARTEND = "wartend"          # Wartet auf Spieler
    UNTERWEGS = "unterwegs"      # Begleitet gerade
    AM_ZIEL = "am_ziel"          # Angekommen, wartet
    ZURUECK = "zurueck"          # Auf Rückweg
    BEENDET = "beendet"          # Mission abgeschlossen
    GESCHEITERT = "gescheitert"  # Söldner oder Spieler tot

# Kosten in Gold
KOSTEN = {
    # AI-Abbild Eskorte
    (EskorteTyp.AI_ABBILD, BesungenerRang.BESUNGEN, "hin"): 300,
    (EskorteTyp.AI_ABBILD, BesungenerRang.BESUNGEN, "hin_zurueck"): 500,
    (EskorteTyp.AI_ABBILD, BesungenerRang.LEGENDAER, "hin"): 600,
    (EskorteTyp.AI_ABBILD, BesungenerRang.LEGENDAER, "hin_zurueck"): 1000,

    # Echter Spieler Eskorte
    (EskorteTyp.ECHTER_SPIELER, BesungenerRang.BESUNGEN, "hin"): 800,
    (EskorteTyp.ECHTER_SPIELER, BesungenerRang.BESUNGEN, "hin_zurueck"): 1200,
    (EskorteTyp.ECHTER_SPIELER, BesungenerRang.LEGENDAER, "hin"): 1500,
    (EskorteTyp.ECHTER_SPIELER, BesungenerRang.LEGENDAER, "hin_zurueck"): 2500,

    # Rettung (NUR echter Spieler, NUR Legendär)
    "rettung": 5000,
}

# Rang-Anforderungen
RANG_ANFORDERUNGEN = {
    BesungenerRang.BEKANNT: {"taten": 3, "kampf_taten": 1},
    BesungenerRang.BESUNGEN: {"taten": 10, "kategorien": 3, "bosse": 1},
    BesungenerRang.LEGENDAER: {"taten": 50, "bosse": 5},
}

# ============================================================
# SPIELER-ABBILD (für AI-Eskorte)
# ============================================================

@dataclass
class SpielerAbbild:
    """
    Snapshot eines Spielers für AI-Eskorte.
    Wird gespeichert wenn Spieler "Besungen" wird.
    """
    spieler_id: str
    name: str
    rang: BesungenerRang

    # Snapshot zum Zeitpunkt der letzten Aktualisierung
    level: int = 1
    stats: Dict = field(default_factory=dict)
    ausruestung: Dict = field(default_factory=dict)
    kampfstil: str = "balanced"  # "aggressiv", "defensiv", "balanced"

    # Verfügbarkeit
    verfuegbar: bool = True
    letzte_aktualisierung: float = 0

    # Echoharp-Lore
    balladen: List[str] = field(default_factory=list)
    bekannte_regionen: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "spieler_id": self.spieler_id,
            "name": self.name,
            "rang": self.rang.value,
            "level": self.level,
            "stats": self.stats,
            "ausruestung": self.ausruestung,
            "kampfstil": self.kampfstil,
            "verfuegbar": self.verfuegbar,
            "letzte_aktualisierung": self.letzte_aktualisierung,
            "balladen": self.balladen,
            "bekannte_regionen": self.bekannte_regionen
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SpielerAbbild':
        return cls(
            spieler_id=data["spieler_id"],
            name=data["name"],
            rang=BesungenerRang(data["rang"]),
            level=data.get("level", 1),
            stats=data.get("stats", {}),
            ausruestung=data.get("ausruestung", {}),
            kampfstil=data.get("kampfstil", "balanced"),
            verfuegbar=data.get("verfuegbar", True),
            letzte_aktualisierung=data.get("letzte_aktualisierung", 0),
            balladen=data.get("balladen", []),
            bekannte_regionen=data.get("bekannte_regionen", [])
        )


# ============================================================
# AKTIVE ESKORTE SESSION
# ============================================================

@dataclass
class EskorteSession:
    """Eine aktive Eskorte-Mission"""
    session_id: str
    auftraggeber_id: str

    # Söldner-Info
    soeldner_id: str
    soeldner_typ: EskorteTyp
    soeldner_rang: BesungenerRang

    # Route
    start_ort: str
    ziel_ort: str
    mit_rueckweg: bool

    # Status
    status: EskorteStatus = EskorteStatus.WARTEND
    gestartet: float = 0
    beendet: float = 0

    # Kosten
    bezahlt: int = 0

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "auftraggeber_id": self.auftraggeber_id,
            "soeldner_id": self.soeldner_id,
            "soeldner_typ": self.soeldner_typ.value,
            "soeldner_rang": self.soeldner_rang.value,
            "start_ort": self.start_ort,
            "ziel_ort": self.ziel_ort,
            "mit_rueckweg": self.mit_rueckweg,
            "status": self.status.value,
            "gestartet": self.gestartet,
            "beendet": self.beendet,
            "bezahlt": self.bezahlt
        }


# ============================================================
# SÖLDNER-GILDE (HAUPT-MANAGER)
# ============================================================

class SoeldnerGilde:
    """
    Verwaltet die Söldner-Gilde und alle Eskorte-Dienste.

    Standorte:
    - Götterfels: Hauptquartier (größte Auswahl)
    - Jede Stadt: Außenstelle
    - Wildnis: Echoharp kann vermitteln
    """

    def __init__(self):
        # Alle registrierten Besungenen (AI-Abbilder)
        self.abbilder: Dict[str, SpielerAbbild] = {}

        # Spieler-Ränge (für echte Spieler)
        self.spieler_raenge: Dict[str, BesungenerRang] = {}
        self.spieler_taten: Dict[str, dict] = {}  # Taten-Tracking

        # Aktive Sessions
        self.aktive_sessions: Dict[str, EskorteSession] = {}

        # Online-Söldner (echte Spieler die verfügbar sind)
        self.online_soeldner: Dict[str, dict] = {}  # spieler_id -> info

        # Statistiken
        self.stats = {
            "eskorten_gesamt": 0,
            "rettungen_gesamt": 0,
            "gold_umgesetzt": 0
        }

        # State laden
        self._load_state()

    # --- Rang-System ---

    def get_spieler_rang(self, spieler_id: str) -> BesungenerRang:
        """Gibt aktuellen Rang eines Spielers zurück"""
        return self.spieler_raenge.get(spieler_id, BesungenerRang.UNBEKANNT)

    def update_spieler_rang(self, spieler_id: str) -> dict:
        """
        Prüft und aktualisiert Spieler-Rang basierend auf Taten.
        Wird vom Echoharp-System aufgerufen nach jeder bezeugten Tat.
        """
        taten = self.spieler_taten.get(spieler_id, {
            "gesamt": 0,
            "kategorien": set(),
            "kampf": 0,
            "bosse": 0
        })

        aktueller_rang = self.get_spieler_rang(spieler_id)
        neuer_rang = aktueller_rang

        # Prüfe Rang-Aufstieg
        if aktueller_rang == BesungenerRang.UNBEKANNT:
            req = RANG_ANFORDERUNGEN[BesungenerRang.BEKANNT]
            if taten["gesamt"] >= req["taten"] and taten["kampf"] >= req["kampf_taten"]:
                neuer_rang = BesungenerRang.BEKANNT

        elif aktueller_rang == BesungenerRang.BEKANNT:
            req = RANG_ANFORDERUNGEN[BesungenerRang.BESUNGEN]
            if (taten["gesamt"] >= req["taten"] and
                len(taten["kategorien"]) >= req["kategorien"] and
                taten["bosse"] >= req["bosse"]):
                neuer_rang = BesungenerRang.BESUNGEN

        elif aktueller_rang == BesungenerRang.BESUNGEN:
            req = RANG_ANFORDERUNGEN[BesungenerRang.LEGENDAER]
            if taten["gesamt"] >= req["taten"] and taten["bosse"] >= req["bosse"]:
                neuer_rang = BesungenerRang.LEGENDAER

        # Rang aktualisieren
        if neuer_rang != aktueller_rang:
            self.spieler_raenge[spieler_id] = neuer_rang
            self._save_state()

            return {
                "aufstieg": True,
                "alter_rang": aktueller_rang.value,
                "neuer_rang": neuer_rang.value,
                "nachricht": self._get_aufstieg_nachricht(neuer_rang)
            }

        return {"aufstieg": False, "rang": aktueller_rang.value}

    def registriere_tat(self, spieler_id: str, kategorie: str, ist_boss: bool = False):
        """Registriert eine bezeugte Tat für Rang-Tracking"""
        if spieler_id not in self.spieler_taten:
            self.spieler_taten[spieler_id] = {
                "gesamt": 0,
                "kategorien": set(),
                "kampf": 0,
                "bosse": 0
            }

        self.spieler_taten[spieler_id]["gesamt"] += 1
        self.spieler_taten[spieler_id]["kategorien"].add(kategorie)

        if kategorie == "kampf":
            self.spieler_taten[spieler_id]["kampf"] += 1

        if ist_boss:
            self.spieler_taten[spieler_id]["bosse"] += 1

        # Prüfe Rang-Aufstieg
        return self.update_spieler_rang(spieler_id)

    def _get_aufstieg_nachricht(self, rang: BesungenerRang) -> str:
        """Generiert Aufstiegs-Nachricht"""
        if rang == BesungenerRang.BEKANNT:
            return "Die Echoharp singt deinen Namen in Tavernen. Du wirst BEKANNT."
        elif rang == BesungenerRang.BESUNGEN:
            return "Die Echoharp hat dich BESUNGEN! Du kannst nun als Eskorte dienen."
        elif rang == BesungenerRang.LEGENDAER:
            return "Du bist LEGENDÄR! Deine Ballade hallt durch alle Lande. Du kannst nun andere RETTEN."
        return ""

    # --- Abbild-System (für AI-Eskorte) ---

    def erstelle_abbild(self, spieler_id: str, spieler_daten: dict) -> dict:
        """
        Erstellt oder aktualisiert AI-Abbild eines Spielers.
        Wird aufgerufen wenn Spieler "Besungen" wird oder Abbild auffrischt.
        """
        rang = self.get_spieler_rang(spieler_id)

        if rang.value not in [BesungenerRang.BESUNGEN.value, BesungenerRang.LEGENDAER.value]:
            return {
                "erfolg": False,
                "grund": f"Rang '{rang.value}' zu niedrig. Mindestens 'besungen' nötig."
            }

        abbild = SpielerAbbild(
            spieler_id=spieler_id,
            name=spieler_daten.get("name", "Unbekannt"),
            rang=rang,
            level=spieler_daten.get("level", 1),
            stats=spieler_daten.get("stats", {}),
            ausruestung=spieler_daten.get("ausruestung", {}),
            kampfstil=spieler_daten.get("kampfstil", "balanced"),
            verfuegbar=True,
            letzte_aktualisierung=time.time(),
            bekannte_regionen=spieler_daten.get("bekannte_regionen", [])
        )

        self.abbilder[spieler_id] = abbild
        self._save_state()

        return {
            "erfolg": True,
            "abbild": abbild.to_dict(),
            "nachricht": "Dein Abbild wurde in der Söldner-Gilde registriert."
        }

    def suche_abbilder(self, region: str = None, min_level: int = 1,
                       rang: BesungenerRang = None) -> List[dict]:
        """Sucht verfügbare AI-Abbilder für Eskorte"""
        ergebnisse = []

        for abbild in self.abbilder.values():
            if not abbild.verfuegbar:
                continue
            if abbild.level < min_level:
                continue
            if rang and abbild.rang != rang:
                continue
            if region and region not in abbild.bekannte_regionen and abbild.bekannte_regionen:
                continue

            ergebnisse.append(abbild.to_dict())

        return ergebnisse

    # --- Online-Söldner (echte Spieler) ---

    def melde_verfuegbar(self, spieler_id: str, spieler_info: dict) -> dict:
        """Echter Spieler meldet sich als Söldner verfügbar"""
        rang = self.get_spieler_rang(spieler_id)

        if rang.value not in [BesungenerRang.BESUNGEN.value, BesungenerRang.LEGENDAER.value]:
            return {
                "erfolg": False,
                "grund": "Du bist noch nicht BESUNGEN. Sammle mehr bezeugte Taten!"
            }

        self.online_soeldner[spieler_id] = {
            "name": spieler_info.get("name", "Söldner"),
            "rang": rang.value,
            "level": spieler_info.get("level", 1),
            "regionen": spieler_info.get("regionen", []),
            "dienste": spieler_info.get("dienste", ["eskorte"]),  # eskorte, rettung
            "seit": time.time()
        }

        return {
            "erfolg": True,
            "nachricht": "Du bist jetzt als Söldner verfügbar. Warte auf Anfragen!"
        }

    def melde_nicht_verfuegbar(self, spieler_id: str) -> dict:
        """Spieler meldet sich ab"""
        if spieler_id in self.online_soeldner:
            del self.online_soeldner[spieler_id]
            return {"erfolg": True}
        return {"erfolg": False, "grund": "Warst nicht angemeldet."}

    def suche_online_soeldner(self, region: str = None,
                               dienst: str = "eskorte") -> List[dict]:
        """Sucht verfügbare echte Spieler"""
        ergebnisse = []

        for spieler_id, info in self.online_soeldner.items():
            if dienst not in info.get("dienste", []):
                continue
            if region and region not in info.get("regionen", []) and info.get("regionen"):
                continue

            ergebnisse.append({
                "spieler_id": spieler_id,
                **info
            })

        return ergebnisse

    # --- Eskorte buchen ---

    def berechne_kosten(self, typ: EskorteTyp, rang: BesungenerRang,
                        mit_rueckweg: bool) -> int:
        """Berechnet Kosten für Eskorte"""
        key = (typ, rang, "hin_zurueck" if mit_rueckweg else "hin")
        return KOSTEN.get(key, 1000)

    def buche_eskorte(self, auftraggeber_id: str, soeldner_id: str,
                      typ: EskorteTyp, start_ort: str, ziel_ort: str,
                      mit_rueckweg: bool, gold_vorhanden: int) -> dict:
        """Bucht eine Eskorte"""

        # Rang des Söldners ermitteln
        if typ == EskorteTyp.AI_ABBILD:
            if soeldner_id not in self.abbilder:
                return {"erfolg": False, "grund": "Abbild nicht gefunden."}
            rang = self.abbilder[soeldner_id].rang
        else:
            if soeldner_id not in self.online_soeldner:
                return {"erfolg": False, "grund": "Söldner nicht online."}
            rang = BesungenerRang(self.online_soeldner[soeldner_id]["rang"])

        # Kosten prüfen
        kosten = self.berechne_kosten(typ, rang, mit_rueckweg)
        if gold_vorhanden < kosten:
            return {
                "erfolg": False,
                "grund": f"Nicht genug Gold. Benötigt: {kosten}, Vorhanden: {gold_vorhanden}"
            }

        # Session erstellen
        session_id = f"eskorte_{int(time.time())}_{random.randint(1000, 9999)}"
        session = EskorteSession(
            session_id=session_id,
            auftraggeber_id=auftraggeber_id,
            soeldner_id=soeldner_id,
            soeldner_typ=typ,
            soeldner_rang=rang,
            start_ort=start_ort,
            ziel_ort=ziel_ort,
            mit_rueckweg=mit_rueckweg,
            status=EskorteStatus.WARTEND,
            gestartet=time.time(),
            bezahlt=kosten
        )

        self.aktive_sessions[session_id] = session
        self.stats["eskorten_gesamt"] += 1
        self.stats["gold_umgesetzt"] += kosten
        self._save_state()

        return {
            "erfolg": True,
            "session_id": session_id,
            "kosten": kosten,
            "typ": typ.value,
            "nachricht": f"Eskorte gebucht! {start_ort} → {ziel_ort}"
        }

    def update_session_status(self, session_id: str, neuer_status: EskorteStatus) -> dict:
        """Aktualisiert Status einer Eskorte-Session"""
        if session_id not in self.aktive_sessions:
            return {"erfolg": False, "grund": "Session nicht gefunden."}

        session = self.aktive_sessions[session_id]
        session.status = neuer_status

        if neuer_status in [EskorteStatus.BEENDET, EskorteStatus.GESCHEITERT]:
            session.beendet = time.time()

        self._save_state()
        return {"erfolg": True, "status": neuer_status.value}

    # --- Rettung (NUR echte Spieler, NUR Legendär) ---

    def buche_rettung(self, auftraggeber_id: str, soeldner_id: str,
                      tod_ort: str, gold_vorhanden: int) -> dict:
        """
        Bucht eine Rettung.
        NUR echte Spieler mit Legendär-Rang können retten!
        """

        # Prüfe ob Söldner online und Legendär
        if soeldner_id not in self.online_soeldner:
            return {"erfolg": False, "grund": "Söldner nicht online."}

        soeldner_info = self.online_soeldner[soeldner_id]
        if soeldner_info["rang"] != BesungenerRang.LEGENDAER.value:
            return {
                "erfolg": False,
                "grund": "Nur LEGENDÄRE Söldner können retten!"
            }

        if "rettung" not in soeldner_info.get("dienste", []):
            return {"erfolg": False, "grund": "Söldner bietet keine Rettung an."}

        # Kosten prüfen
        kosten = KOSTEN["rettung"]
        if gold_vorhanden < kosten:
            return {
                "erfolg": False,
                "grund": f"Nicht genug Gold. Benötigt: {kosten}"
            }

        # Rettung durchführen
        self.stats["rettungen_gesamt"] += 1
        self.stats["gold_umgesetzt"] += kosten
        self._save_state()

        return {
            "erfolg": True,
            "kosten": kosten,
            "soeldner": soeldner_info["name"],
            "nachricht": f"{soeldner_info['name']} eilt zu deiner Rettung!"
        }

    # --- Söldner-Tod ---

    def soeldner_gestorben(self, session_id: str, soeldner_id: str) -> dict:
        """
        Söldner ist während Eskorte gestorben.
        - Kein permanenter Tod für Söldner
        - Debuff: 2h kann nicht dienen
        - 10% Gold-Verlust
        - Auftraggeber: Kein Refund
        """
        if session_id in self.aktive_sessions:
            session = self.aktive_sessions[session_id]
            session.status = EskorteStatus.GESCHEITERT
            session.beendet = time.time()

        # Söldner offline setzen mit Debuff
        if soeldner_id in self.online_soeldner:
            del self.online_soeldner[soeldner_id]

        self._save_state()

        return {
            "session_beendet": True,
            "soeldner_debuff": 7200,  # 2 Stunden in Sekunden
            "gold_verlust_prozent": 10,
            "nachricht": "Der Söldner ist gefallen. Mission gescheitert. Kein Refund."
        }

    # --- Persistenz ---

    def _save_state(self):
        """Speichert State in Datei"""
        state = {
            "abbilder": {k: v.to_dict() for k, v in self.abbilder.items()},
            "spieler_raenge": {k: v.value for k, v in self.spieler_raenge.items()},
            "spieler_taten": {
                k: {**v, "kategorien": list(v.get("kategorien", set()))}
                for k, v in self.spieler_taten.items()
            },
            "stats": self.stats
        }

        path = Path(__file__).parent / "soeldner_state.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        """Lädt State aus Datei"""
        path = Path(__file__).parent / "soeldner_state.json"
        if not path.exists():
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)

            self.abbilder = {
                k: SpielerAbbild.from_dict(v)
                for k, v in state.get("abbilder", {}).items()
            }
            self.spieler_raenge = {
                k: BesungenerRang(v)
                for k, v in state.get("spieler_raenge", {}).items()
            }
            self.spieler_taten = {
                k: {**v, "kategorien": set(v.get("kategorien", []))}
                for k, v in state.get("spieler_taten", {}).items()
            }
            self.stats = state.get("stats", self.stats)

        except Exception as e:
            print(f"[SÖLDNER] Fehler beim Laden: {e}")

    def get_stats(self) -> dict:
        """Gibt Gilde-Statistiken zurück"""
        return {
            **self.stats,
            "abbilder_registriert": len(self.abbilder),
            "soeldner_online": len(self.online_soeldner),
            "aktive_eskorten": len([s for s in self.aktive_sessions.values()
                                    if s.status not in [EskorteStatus.BEENDET,
                                                         EskorteStatus.GESCHEITERT]])
        }


# ============================================================
# SINGLETON INSTANZ
# ============================================================

_gilde: Optional[SoeldnerGilde] = None

def get_soeldner_gilde() -> SoeldnerGilde:
    """Gibt Singleton-Instanz der Söldner-Gilde zurück"""
    global _gilde
    if _gilde is None:
        _gilde = SoeldnerGilde()
    return _gilde


# ============================================================
# API HELPER FUNKTIONEN
# ============================================================

def get_eskorte_preisliste() -> dict:
    """Gibt komplette Preisliste zurück"""
    return {
        "ai_abbild": {
            "besungen": {
                "hin": KOSTEN[(EskorteTyp.AI_ABBILD, BesungenerRang.BESUNGEN, "hin")],
                "hin_zurueck": KOSTEN[(EskorteTyp.AI_ABBILD, BesungenerRang.BESUNGEN, "hin_zurueck")]
            },
            "legendär": {
                "hin": KOSTEN[(EskorteTyp.AI_ABBILD, BesungenerRang.LEGENDAER, "hin")],
                "hin_zurueck": KOSTEN[(EskorteTyp.AI_ABBILD, BesungenerRang.LEGENDAER, "hin_zurueck")]
            }
        },
        "echter_spieler": {
            "besungen": {
                "hin": KOSTEN[(EskorteTyp.ECHTER_SPIELER, BesungenerRang.BESUNGEN, "hin")],
                "hin_zurueck": KOSTEN[(EskorteTyp.ECHTER_SPIELER, BesungenerRang.BESUNGEN, "hin_zurueck")]
            },
            "legendär": {
                "hin": KOSTEN[(EskorteTyp.ECHTER_SPIELER, BesungenerRang.LEGENDAER, "hin")],
                "hin_zurueck": KOSTEN[(EskorteTyp.ECHTER_SPIELER, BesungenerRang.LEGENDAER, "hin_zurueck")]
            }
        },
        "rettung": KOSTEN["rettung"]
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("🛡️ Söldner-Gilde System Test")
    print("=" * 50)

    gilde = get_soeldner_gilde()

    # Test: Taten registrieren
    print("\n1. Registriere Taten für Spieler 'held1'...")
    for i in range(12):
        result = gilde.registriere_tat("held1", "kampf", ist_boss=(i == 10))
        if result.get("aufstieg"):
            print(f"   → {result['nachricht']}")

    # Test: Abbild erstellen
    print("\n2. Erstelle Abbild...")
    result = gilde.erstelle_abbild("held1", {
        "name": "Der Tapfere Held",
        "level": 25,
        "kampfstil": "aggressiv",
        "bekannte_regionen": ["Samtmoos-Tiefwald", "Salzwind-Küste"]
    })
    print(f"   → {result.get('nachricht', result.get('grund'))}")

    # Test: Abbilder suchen
    print("\n3. Suche Abbilder...")
    abbilder = gilde.suche_abbilder()
    print(f"   → {len(abbilder)} Abbild(er) gefunden")

    # Test: Preisliste
    print("\n4. Preisliste:")
    preise = get_eskorte_preisliste()
    print(f"   AI Besungen Hin: {preise['ai_abbild']['besungen']['hin']}g")
    print(f"   Echt Legendär Hin+Zurück: {preise['echter_spieler']['legendär']['hin_zurueck']}g")
    print(f"   Rettung: {preise['rettung']}g")

    # Stats
    print("\n5. Gilde Stats:")
    stats = gilde.get_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")

    print("\n✅ Test abgeschlossen!")
