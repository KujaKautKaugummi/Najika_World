"""
NAJIKA CHEATER-HINRICHTUNGS-EVENT SYSTEM
=========================================

Öffentliche Hinrichtungen für bewiesene Cheater in der Arena!

WICHTIG:
- NUR nach 100% Beweis (Logs, Video, etc.)
- IMMER menschliche Review VOR Hinrichtung
- Einspruchsmöglichkeit
- Kein Versehen oder Bug darf bestraft werden

"Wer betrügt, stirbt öffentlich. Wer fair spielt, wird geschützt."

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

class CheatTyp(Enum):
    """Arten von Cheats"""
    DAMAGE_HACK = "damage_hack"        # Überhöhter Schaden
    SPEED_HACK = "speed_hack"          # Zu schnelle Bewegung
    TELEPORT_HACK = "teleport_hack"    # Unerlaubtes Teleportieren
    GODMODE = "godmode"                # Unsterblichkeit
    GOLD_HACK = "gold_hack"            # Gold aus dem Nichts
    ITEM_DUPLICATION = "item_dupe"     # Item-Duplikation
    COOLDOWN_HACK = "cooldown_hack"    # Keine Cooldowns
    WALL_HACK = "wall_hack"            # Durch Wände gehen
    BOT_USAGE = "bot_usage"            # Automatisierte Spieler
    EXPLOIT_ABUSE = "exploit_abuse"    # Bewusster Exploit-Missbrauch

class ReviewStatus(Enum):
    """Status der Überprüfung"""
    PENDING = "pending"              # Wartet auf Review
    UNDER_REVIEW = "under_review"    # Wird geprüft
    CONFIRMED = "confirmed"          # Cheat bestätigt
    REJECTED = "rejected"            # Falschalarm
    APPEALED = "appealed"            # Einspruch eingereicht

class HinrichtungsStatus(Enum):
    """Status der Hinrichtung"""
    SCHEDULED = "scheduled"          # Geplant
    ANNOUNCED = "announced"          # Angekündigt (Spieler können zuschauen)
    IN_PROGRESS = "in_progress"      # Läuft gerade
    COMPLETED = "completed"          # Abgeschlossen
    CANCELLED = "cancelled"          # Abgebrochen (z.B. Einspruch erfolgreich)

# Hinrichtungs-Methoden (für Show-Effekt)
HINRICHTUNGS_METHODEN = [
    {
        "id": "schwert",
        "name": "Schwert des Gerechten",
        "beschreibung": "Der Henker-NPC enthauptet den Betrüger mit einem heiligen Schwert.",
        "dauer_sekunden": 15
    },
    {
        "id": "feuer",
        "name": "Reinigendes Feuer",
        "beschreibung": "Der Betrüger wird in magischem Feuer verbrannt.",
        "dauer_sekunden": 20
    },
    {
        "id": "void",
        "name": "Verschlingung durch die Leere",
        "beschreibung": "Ein Portal zur Leere öffnet sich und verschlingt den Betrüger.",
        "dauer_sekunden": 25
    },
    {
        "id": "blitz",
        "name": "Göttlicher Blitz",
        "beschreibung": "Ein Blitz vom Himmel trifft den Betrüger.",
        "dauer_sekunden": 10
    },
    {
        "id": "slimes",
        "name": "Schleimflut",
        "beschreibung": "Tausende Slimes überrollen den Betrüger.",
        "dauer_sekunden": 30
    }
]

# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class CheatReport:
    """Ein Cheat-Bericht"""
    report_id: str
    spieler_id: str
    spieler_name: str

    # Cheat-Details
    cheat_typ: CheatTyp
    beschreibung: str
    zeitpunkt: float
    beweise: List[dict] = field(default_factory=list)  # Logs, Screenshots, Videos

    # Review
    review_status: ReviewStatus = ReviewStatus.PENDING
    reviewer_id: Optional[str] = None
    review_notizen: str = ""
    review_zeitpunkt: float = 0

    # Einspruch
    einspruch_text: Optional[str] = None
    einspruch_zeitpunkt: float = 0
    einspruch_entscheidung: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "report_id": self.report_id,
            "spieler_id": self.spieler_id,
            "spieler_name": self.spieler_name,
            "cheat_typ": self.cheat_typ.value,
            "beschreibung": self.beschreibung,
            "zeitpunkt": self.zeitpunkt,
            "beweise": self.beweise,
            "review_status": self.review_status.value,
            "reviewer_id": self.reviewer_id,
            "review_notizen": self.review_notizen,
            "review_zeitpunkt": self.review_zeitpunkt,
            "einspruch_text": self.einspruch_text,
            "einspruch_zeitpunkt": self.einspruch_zeitpunkt,
            "einspruch_entscheidung": self.einspruch_entscheidung
        }

@dataclass
class HinrichtungsEvent:
    """Ein geplantes Hinrichtungs-Event"""
    event_id: str
    report_id: str
    spieler_id: str
    spieler_name: str

    # Event-Details
    methode: dict
    geplant_fuer: float  # Unix Timestamp
    arena: str = "Götterfels Arena"

    # Status
    status: HinrichtungsStatus = HinrichtungsStatus.SCHEDULED
    zuschauer_ids: List[str] = field(default_factory=list)

    # Ergebnis
    durchgefuehrt: float = 0
    zuschauer_anzahl: int = 0

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "report_id": self.report_id,
            "spieler_id": self.spieler_id,
            "spieler_name": self.spieler_name,
            "methode": self.methode,
            "geplant_fuer": self.geplant_fuer,
            "arena": self.arena,
            "status": self.status.value,
            "zuschauer_ids": self.zuschauer_ids,
            "zuschauer_anzahl": len(self.zuschauer_ids),
            "durchgefuehrt": self.durchgefuehrt
        }

# ============================================================
# HALL OF SHAME
# ============================================================

@dataclass
class HallOfShameEintrag:
    """Eintrag in der Hall of Shame"""
    spieler_id: str
    spieler_name: str
    cheat_typ: str
    hinrichtungs_datum: float
    hinrichtungs_methode: str
    zuschauer_anzahl: int

    # Ewige Schande
    schand_punkte: int = 100  # Mehr bei schweren Vergehen

    def to_dict(self) -> dict:
        return {
            "spieler_id": self.spieler_id,
            "spieler_name": self.spieler_name,
            "cheat_typ": self.cheat_typ,
            "hinrichtungs_datum": self.hinrichtungs_datum,
            "hinrichtungs_methode": self.hinrichtungs_methode,
            "zuschauer_anzahl": self.zuschauer_anzahl,
            "schand_punkte": self.schand_punkte
        }

# ============================================================
# HAUPT-MANAGER
# ============================================================

class CheaterHinrichtungsSystem:
    """
    Verwaltet Cheat-Reports, Reviews und Hinrichtungs-Events.

    Prozess:
    1. Cheat wird automatisch erkannt (Anomalie-Detektion)
    2. Report wird erstellt und geloggt
    3. Menschlicher Reviewer prüft den Fall
    4. Bei Bestätigung: Hinrichtung wird geplant
    5. Spieler kann Einspruch erheben (vor Hinrichtung)
    6. Hinrichtungs-Event wird angekündigt
    7. Öffentliche Hinrichtung in der Arena
    8. Eintrag in Hall of Shame
    9. Account permanent gebannt
    """

    def __init__(self):
        # Reports
        self.reports: Dict[str, CheatReport] = {}
        self.pending_reports: List[str] = []  # IDs wartender Reports

        # Hinrichtungen
        self.hinrichtungen: Dict[str, HinrichtungsEvent] = {}
        self.geplante_hinrichtungen: List[str] = []  # Anstehende Events

        # Hall of Shame
        self.hall_of_shame: List[HallOfShameEintrag] = []

        # Gebannte Accounts
        self.gebannte_accounts: Dict[str, dict] = {}  # spieler_id -> ban_info

        # Statistiken
        self.stats = {
            "reports_gesamt": 0,
            "hinrichtungen_gesamt": 0,
            "einsprueche_erfolgreich": 0,
            "falschalarme": 0
        }

        # State laden
        self._load_state()

    # --- Anomalie-Erkennung ---

    def pruefe_anomalie(self, spieler_id: str, event_typ: str, daten: dict) -> Optional[dict]:
        """
        Prüft ob ein Spieler-Event verdächtig ist.
        Wird vom Server bei jedem relevanten Event aufgerufen.

        Returns: Anomalie-Info oder None wenn OK
        """
        anomalie = None

        if event_typ == "damage":
            # Damage-Hack prüfen
            damage = daten.get("damage", 0)
            expected_max = daten.get("expected_max", 1000)
            if damage > expected_max * 1.5:  # 50% Toleranz für Crits etc.
                anomalie = {
                    "typ": CheatTyp.DAMAGE_HACK,
                    "beschreibung": f"Schaden {damage} übersteigt Maximum {expected_max} um mehr als 50%",
                    "schwere": "hoch" if damage > expected_max * 3 else "mittel"
                }

        elif event_typ == "position":
            # Teleport/Speed-Hack prüfen
            distanz = daten.get("distanz", 0)
            zeit_delta = daten.get("zeit_delta", 1)
            max_speed = daten.get("max_speed", 10)

            geschwindigkeit = distanz / max(zeit_delta, 0.1)
            if geschwindigkeit > max_speed * 2:
                anomalie = {
                    "typ": CheatTyp.SPEED_HACK if geschwindigkeit < max_speed * 10 else CheatTyp.TELEPORT_HACK,
                    "beschreibung": f"Geschwindigkeit {geschwindigkeit:.1f} übersteigt Maximum {max_speed}",
                    "schwere": "hoch" if geschwindigkeit > max_speed * 5 else "mittel"
                }

        elif event_typ == "gold":
            # Gold-Hack prüfen
            gold_vorher = daten.get("gold_vorher", 0)
            gold_nachher = daten.get("gold_nachher", 0)
            gold_quelle = daten.get("quelle", "unbekannt")

            if gold_nachher - gold_vorher > 100000 and gold_quelle == "unbekannt":
                anomalie = {
                    "typ": CheatTyp.GOLD_HACK,
                    "beschreibung": f"Unerklärlicher Gold-Zuwachs: {gold_nachher - gold_vorher}",
                    "schwere": "kritisch"
                }

        elif event_typ == "hp":
            # Godmode prüfen
            hp = daten.get("hp", 100)
            damage_received = daten.get("damage_received", 0)

            if damage_received > 0 and hp >= daten.get("hp_vorher", 100):
                # Wurde getroffen aber HP gleich oder höher
                anomalie = {
                    "typ": CheatTyp.GODMODE,
                    "beschreibung": f"Spieler erhielt {damage_received} Schaden aber HP unverändert",
                    "schwere": "kritisch"
                }

        elif event_typ == "cooldown":
            # Cooldown-Hack prüfen
            skill_id = daten.get("skill_id")
            letzte_nutzung = daten.get("letzte_nutzung", 0)
            cooldown = daten.get("cooldown", 5)

            zeit_seit_nutzung = time.time() - letzte_nutzung
            if zeit_seit_nutzung < cooldown * 0.5:  # 50% Toleranz
                anomalie = {
                    "typ": CheatTyp.COOLDOWN_HACK,
                    "beschreibung": f"Skill {skill_id} genutzt nach {zeit_seit_nutzung:.1f}s (Cooldown: {cooldown}s)",
                    "schwere": "mittel"
                }

        # Bei Anomalie: Report erstellen
        if anomalie:
            self.erstelle_auto_report(spieler_id, anomalie, daten)

        return anomalie

    # --- Report-System ---

    def erstelle_auto_report(self, spieler_id: str, anomalie: dict, rohdaten: dict) -> str:
        """Erstellt automatischen Report bei Anomalie"""
        report_id = f"auto_{int(time.time())}_{random.randint(1000, 9999)}"

        report = CheatReport(
            report_id=report_id,
            spieler_id=spieler_id,
            spieler_name=rohdaten.get("spieler_name", "Unbekannt"),
            cheat_typ=anomalie["typ"],
            beschreibung=anomalie["beschreibung"],
            zeitpunkt=time.time(),
            beweise=[{
                "typ": "auto_detection",
                "daten": rohdaten,
                "anomalie": {k: v.value if isinstance(v, Enum) else v for k, v in anomalie.items()},
                "zeitstempel": time.time()
            }],
            review_status=ReviewStatus.PENDING
        )

        self.reports[report_id] = report
        self.pending_reports.append(report_id)
        self.stats["reports_gesamt"] += 1
        self._save_state()

        return report_id

    def erstelle_manuellen_report(self, reporter_id: str, verdaechtiger_id: str,
                                   verdaechtiger_name: str, cheat_typ: str,
                                   beschreibung: str, beweise: List[dict]) -> str:
        """Erstellt manuellen Report (von Spielern oder Admins)"""
        report_id = f"manual_{int(time.time())}_{random.randint(1000, 9999)}"

        try:
            cheat_enum = CheatTyp(cheat_typ)
        except ValueError:
            cheat_enum = CheatTyp.EXPLOIT_ABUSE

        report = CheatReport(
            report_id=report_id,
            spieler_id=verdaechtiger_id,
            spieler_name=verdaechtiger_name,
            cheat_typ=cheat_enum,
            beschreibung=beschreibung,
            zeitpunkt=time.time(),
            beweise=beweise,
            review_status=ReviewStatus.PENDING
        )

        self.reports[report_id] = report
        self.pending_reports.append(report_id)
        self.stats["reports_gesamt"] += 1
        self._save_state()

        return report_id

    # --- Review-System ---

    def starte_review(self, report_id: str, reviewer_id: str) -> dict:
        """Reviewer beginnt mit der Prüfung"""
        if report_id not in self.reports:
            return {"erfolg": False, "grund": "Report nicht gefunden"}

        report = self.reports[report_id]

        if report.review_status != ReviewStatus.PENDING:
            return {"erfolg": False, "grund": f"Report ist bereits {report.review_status.value}"}

        report.review_status = ReviewStatus.UNDER_REVIEW
        report.reviewer_id = reviewer_id
        self._save_state()

        return {
            "erfolg": True,
            "report": report.to_dict(),
            "nachricht": "Review gestartet. Bitte alle Beweise sorgfältig prüfen!"
        }

    def beende_review(self, report_id: str, reviewer_id: str,
                      entscheidung: str, notizen: str) -> dict:
        """
        Beendet Review mit Entscheidung.
        entscheidung: "confirmed" oder "rejected"
        """
        if report_id not in self.reports:
            return {"erfolg": False, "grund": "Report nicht gefunden"}

        report = self.reports[report_id]

        if report.review_status != ReviewStatus.UNDER_REVIEW:
            return {"erfolg": False, "grund": "Report ist nicht unter Review"}

        if report.reviewer_id != reviewer_id:
            return {"erfolg": False, "grund": "Nur der zugewiesene Reviewer kann entscheiden"}

        if entscheidung == "confirmed":
            report.review_status = ReviewStatus.CONFIRMED
            report.review_notizen = notizen
            report.review_zeitpunkt = time.time()

            # Hinrichtung planen
            hinrichtung = self._plane_hinrichtung(report)

            self._save_state()

            return {
                "erfolg": True,
                "status": "confirmed",
                "hinrichtung_geplant": hinrichtung.to_dict(),
                "nachricht": f"Cheat bestätigt. Hinrichtung geplant für {hinrichtung.arena}."
            }

        elif entscheidung == "rejected":
            report.review_status = ReviewStatus.REJECTED
            report.review_notizen = notizen
            report.review_zeitpunkt = time.time()
            self.stats["falschalarme"] += 1

            # Aus pending entfernen
            if report_id in self.pending_reports:
                self.pending_reports.remove(report_id)

            self._save_state()

            return {
                "erfolg": True,
                "status": "rejected",
                "nachricht": "Report abgelehnt. Kein Cheat nachweisbar."
            }

        return {"erfolg": False, "grund": "Ungültige Entscheidung"}

    # --- Einspruch-System ---

    def reiche_einspruch_ein(self, report_id: str, spieler_id: str, einspruch_text: str) -> dict:
        """Spieler reicht Einspruch gegen Verurteilung ein"""
        if report_id not in self.reports:
            return {"erfolg": False, "grund": "Report nicht gefunden"}

        report = self.reports[report_id]

        if report.spieler_id != spieler_id:
            return {"erfolg": False, "grund": "Nur der Betroffene kann Einspruch erheben"}

        if report.review_status != ReviewStatus.CONFIRMED:
            return {"erfolg": False, "grund": "Kein bestätigter Report zum Anfechten"}

        if report.einspruch_text:
            return {"erfolg": False, "grund": "Einspruch wurde bereits eingereicht"}

        report.einspruch_text = einspruch_text
        report.einspruch_zeitpunkt = time.time()
        report.review_status = ReviewStatus.APPEALED

        # Hinrichtung pausieren falls geplant
        for event_id, event in self.hinrichtungen.items():
            if event.report_id == report_id and event.status == HinrichtungsStatus.SCHEDULED:
                event.status = HinrichtungsStatus.CANCELLED  # Temporär

        self._save_state()

        return {
            "erfolg": True,
            "nachricht": "Einspruch eingereicht. Ein Senior-Reviewer wird deinen Fall prüfen.",
            "hinweis": "Hinrichtung ist temporär ausgesetzt."
        }

    def entscheide_einspruch(self, report_id: str, reviewer_id: str,
                              angenommen: bool, begruendung: str) -> dict:
        """Senior-Reviewer entscheidet über Einspruch"""
        if report_id not in self.reports:
            return {"erfolg": False, "grund": "Report nicht gefunden"}

        report = self.reports[report_id]

        if report.review_status != ReviewStatus.APPEALED:
            return {"erfolg": False, "grund": "Kein offener Einspruch"}

        if angenommen:
            # Einspruch angenommen - Spieler freigesprochen
            report.review_status = ReviewStatus.REJECTED
            report.einspruch_entscheidung = f"ANGENOMMEN: {begruendung}"
            self.stats["einsprueche_erfolgreich"] += 1

            # Hinrichtung endgültig absagen
            for event_id, event in self.hinrichtungen.items():
                if event.report_id == report_id:
                    event.status = HinrichtungsStatus.CANCELLED

            self._save_state()

            return {
                "erfolg": True,
                "entscheidung": "angenommen",
                "nachricht": f"Einspruch ANGENOMMEN. Spieler {report.spieler_name} ist freigesprochen."
            }
        else:
            # Einspruch abgelehnt - Hinrichtung fortsetzen
            report.review_status = ReviewStatus.CONFIRMED
            report.einspruch_entscheidung = f"ABGELEHNT: {begruendung}"

            # Hinrichtung reaktivieren
            for event_id, event in self.hinrichtungen.items():
                if event.report_id == report_id:
                    event.status = HinrichtungsStatus.SCHEDULED
                    # Neuen Termin setzen (1h in der Zukunft)
                    event.geplant_fuer = time.time() + 3600

            self._save_state()

            return {
                "erfolg": True,
                "entscheidung": "abgelehnt",
                "nachricht": "Einspruch ABGELEHNT. Hinrichtung wird fortgesetzt."
            }

    # --- Hinrichtungs-Event ---

    def _plane_hinrichtung(self, report: CheatReport) -> HinrichtungsEvent:
        """Plant Hinrichtungs-Event"""
        event_id = f"exec_{int(time.time())}_{random.randint(1000, 9999)}"

        # Zufällige Methode wählen
        methode = random.choice(HINRICHTUNGS_METHODEN)

        # Event in 24h (Zeit für Einspruch)
        geplant_fuer = time.time() + 86400

        event = HinrichtungsEvent(
            event_id=event_id,
            report_id=report.report_id,
            spieler_id=report.spieler_id,
            spieler_name=report.spieler_name,
            methode=methode,
            geplant_fuer=geplant_fuer,
            status=HinrichtungsStatus.SCHEDULED
        )

        self.hinrichtungen[event_id] = event
        self.geplante_hinrichtungen.append(event_id)

        return event

    def ankuendige_hinrichtung(self, event_id: str) -> dict:
        """Kündigt Hinrichtung öffentlich an (1h vorher)"""
        if event_id not in self.hinrichtungen:
            return {"erfolg": False, "grund": "Event nicht gefunden"}

        event = self.hinrichtungen[event_id]

        if event.status != HinrichtungsStatus.SCHEDULED:
            return {"erfolg": False, "grund": f"Event Status ist {event.status.value}"}

        event.status = HinrichtungsStatus.ANNOUNCED
        self._save_state()

        return {
            "erfolg": True,
            "event": event.to_dict(),
            "ankuendigung": {
                "titel": f"ÖFFENTLICHE HINRICHTUNG: {event.spieler_name}",
                "text": f"Ein Betrüger wurde gefasst! {event.spieler_name} wird hingerichtet wegen: {self.reports[event.report_id].cheat_typ.value}",
                "ort": event.arena,
                "zeit": event.geplant_fuer,
                "methode": event.methode["name"]
            }
        }

    def melde_zuschauer_an(self, event_id: str, spieler_id: str) -> dict:
        """Spieler meldet sich als Zuschauer an"""
        if event_id not in self.hinrichtungen:
            return {"erfolg": False, "grund": "Event nicht gefunden"}

        event = self.hinrichtungen[event_id]

        if event.status not in [HinrichtungsStatus.ANNOUNCED, HinrichtungsStatus.SCHEDULED]:
            return {"erfolg": False, "grund": "Anmeldung nicht mehr möglich"}

        if spieler_id not in event.zuschauer_ids:
            event.zuschauer_ids.append(spieler_id)
            self._save_state()

        return {
            "erfolg": True,
            "nachricht": f"Du wirst bei der Hinrichtung von {event.spieler_name} dabei sein.",
            "zuschauer_gesamt": len(event.zuschauer_ids)
        }

    def fuehre_hinrichtung_durch(self, event_id: str) -> dict:
        """Führt die Hinrichtung durch"""
        if event_id not in self.hinrichtungen:
            return {"erfolg": False, "grund": "Event nicht gefunden"}

        event = self.hinrichtungen[event_id]

        if event.status == HinrichtungsStatus.CANCELLED:
            return {"erfolg": False, "grund": "Hinrichtung wurde abgesagt"}

        if event.status == HinrichtungsStatus.COMPLETED:
            return {"erfolg": False, "grund": "Hinrichtung bereits durchgeführt"}

        # Hinrichtung durchführen
        event.status = HinrichtungsStatus.IN_PROGRESS
        event.durchgefuehrt = time.time()
        event.zuschauer_anzahl = len(event.zuschauer_ids)

        # Account bannen
        self.gebannte_accounts[event.spieler_id] = {
            "spieler_name": event.spieler_name,
            "grund": self.reports[event.report_id].cheat_typ.value,
            "zeitpunkt": time.time(),
            "hinrichtung_event": event_id
        }

        # Hall of Shame Eintrag
        scham_eintrag = HallOfShameEintrag(
            spieler_id=event.spieler_id,
            spieler_name=event.spieler_name,
            cheat_typ=self.reports[event.report_id].cheat_typ.value,
            hinrichtungs_datum=time.time(),
            hinrichtungs_methode=event.methode["name"],
            zuschauer_anzahl=event.zuschauer_anzahl
        )
        self.hall_of_shame.append(scham_eintrag)

        # Event abschließen
        event.status = HinrichtungsStatus.COMPLETED
        self.stats["hinrichtungen_gesamt"] += 1

        # Aus geplanten entfernen
        if event_id in self.geplante_hinrichtungen:
            self.geplante_hinrichtungen.remove(event_id)

        self._save_state()

        return {
            "erfolg": True,
            "event": event.to_dict(),
            "animation": {
                "methode": event.methode,
                "spieler": event.spieler_name,
                "text": f"{event.spieler_name} wurde durch '{event.methode['name']}' hingerichtet!",
                "zuschauer": event.zuschauer_anzahl
            },
            "hall_of_shame_eintrag": scham_eintrag.to_dict(),
            "account_gebannt": True
        }

    # --- Abfragen ---

    def ist_gebannt(self, spieler_id: str) -> dict:
        """Prüft ob Spieler gebannt ist"""
        if spieler_id in self.gebannte_accounts:
            return {
                "gebannt": True,
                "details": self.gebannte_accounts[spieler_id]
            }
        return {"gebannt": False}

    def get_hall_of_shame(self, limit: int = 50) -> List[dict]:
        """Gibt Hall of Shame zurück"""
        # Nach Schandpunkten sortiert
        sortiert = sorted(self.hall_of_shame, key=lambda x: x.schand_punkte, reverse=True)
        return [e.to_dict() for e in sortiert[:limit]]

    def get_anstehende_hinrichtungen(self) -> List[dict]:
        """Gibt alle anstehenden Hinrichtungen zurück"""
        ergebnis = []
        for event_id in self.geplante_hinrichtungen:
            event = self.hinrichtungen.get(event_id)
            if event and event.status in [HinrichtungsStatus.SCHEDULED, HinrichtungsStatus.ANNOUNCED]:
                ergebnis.append(event.to_dict())
        return ergebnis

    def get_pending_reports(self) -> List[dict]:
        """Gibt alle wartenden Reports zurück (für Reviewer)"""
        return [self.reports[rid].to_dict() for rid in self.pending_reports if rid in self.reports]

    def get_stats(self) -> dict:
        """Gibt System-Statistiken zurück"""
        return {
            **self.stats,
            "reports_wartend": len(self.pending_reports),
            "hinrichtungen_geplant": len(self.geplante_hinrichtungen),
            "accounts_gebannt": len(self.gebannte_accounts),
            "hall_of_shame_eintraege": len(self.hall_of_shame)
        }

    # --- Persistenz ---

    def _save_state(self):
        """Speichert State"""
        state = {
            "reports": {k: v.to_dict() for k, v in self.reports.items()},
            "pending_reports": self.pending_reports,
            "hinrichtungen": {k: v.to_dict() for k, v in self.hinrichtungen.items()},
            "geplante_hinrichtungen": self.geplante_hinrichtungen,
            "hall_of_shame": [e.to_dict() for e in self.hall_of_shame],
            "gebannte_accounts": self.gebannte_accounts,
            "stats": self.stats
        }

        path = Path(__file__).parent / "cheater_state.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        """Lädt State"""
        path = Path(__file__).parent / "cheater_state.json"
        if not path.exists():
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)

            # Reports laden
            for k, v in state.get("reports", {}).items():
                self.reports[k] = CheatReport(
                    report_id=v["report_id"],
                    spieler_id=v["spieler_id"],
                    spieler_name=v["spieler_name"],
                    cheat_typ=CheatTyp(v["cheat_typ"]),
                    beschreibung=v["beschreibung"],
                    zeitpunkt=v["zeitpunkt"],
                    beweise=v.get("beweise", []),
                    review_status=ReviewStatus(v["review_status"]),
                    reviewer_id=v.get("reviewer_id"),
                    review_notizen=v.get("review_notizen", ""),
                    review_zeitpunkt=v.get("review_zeitpunkt", 0),
                    einspruch_text=v.get("einspruch_text"),
                    einspruch_zeitpunkt=v.get("einspruch_zeitpunkt", 0),
                    einspruch_entscheidung=v.get("einspruch_entscheidung")
                )

            self.pending_reports = state.get("pending_reports", [])

            # Hinrichtungen laden
            for k, v in state.get("hinrichtungen", {}).items():
                self.hinrichtungen[k] = HinrichtungsEvent(
                    event_id=v["event_id"],
                    report_id=v["report_id"],
                    spieler_id=v["spieler_id"],
                    spieler_name=v["spieler_name"],
                    methode=v["methode"],
                    geplant_fuer=v["geplant_fuer"],
                    arena=v.get("arena", "Götterfels Arena"),
                    status=HinrichtungsStatus(v["status"]),
                    zuschauer_ids=v.get("zuschauer_ids", []),
                    durchgefuehrt=v.get("durchgefuehrt", 0),
                    zuschauer_anzahl=v.get("zuschauer_anzahl", 0)
                )

            self.geplante_hinrichtungen = state.get("geplante_hinrichtungen", [])

            # Hall of Shame laden
            for e in state.get("hall_of_shame", []):
                self.hall_of_shame.append(HallOfShameEintrag(
                    spieler_id=e["spieler_id"],
                    spieler_name=e["spieler_name"],
                    cheat_typ=e["cheat_typ"],
                    hinrichtungs_datum=e["hinrichtungs_datum"],
                    hinrichtungs_methode=e["hinrichtungs_methode"],
                    zuschauer_anzahl=e["zuschauer_anzahl"],
                    schand_punkte=e.get("schand_punkte", 100)
                ))

            self.gebannte_accounts = state.get("gebannte_accounts", {})
            self.stats = state.get("stats", self.stats)

        except Exception as e:
            print(f"[CHEATER] Fehler beim Laden: {e}")


# ============================================================
# SINGLETON
# ============================================================

_system: Optional[CheaterHinrichtungsSystem] = None

def get_cheater_system() -> CheaterHinrichtungsSystem:
    """Gibt Singleton-Instanz zurück"""
    global _system
    if _system is None:
        _system = CheaterHinrichtungsSystem()
    return _system


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("⚔️ Cheater-Hinrichtungs-System Test")
    print("=" * 50)

    system = get_cheater_system()

    # Test: Anomalie erkennen
    print("\n1. Simuliere Damage-Hack Anomalie...")
    anomalie = system.pruefe_anomalie("cheater123", "damage", {
        "damage": 99999,
        "expected_max": 500,
        "spieler_name": "H4ck3rM4n"
    })
    print(f"   Anomalie erkannt: {anomalie}")

    # Test: Review starten
    print("\n2. Starte Review...")
    if system.pending_reports:
        report_id = system.pending_reports[0]
        result = system.starte_review(report_id, "admin1")
        print(f"   {result.get('nachricht', result.get('grund'))}")

        # Review abschließen
        print("\n3. Bestätige Cheat...")
        result = system.beende_review(report_id, "admin1", "confirmed", "Klarer Damage-Hack")
        print(f"   {result.get('nachricht', result.get('grund'))}")

        # Hinrichtung durchführen
        if system.geplante_hinrichtungen:
            event_id = system.geplante_hinrichtungen[0]
            print(f"\n4. Führe Hinrichtung durch...")
            result = system.fuehre_hinrichtung_durch(event_id)
            if result.get("erfolg"):
                print(f"   {result['animation']['text']}")

    # Stats
    print("\n5. System Stats:")
    stats = system.get_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")

    # Hall of Shame
    print("\n6. Hall of Shame:")
    shame = system.get_hall_of_shame(5)
    for e in shame:
        print(f"   - {e['spieler_name']}: {e['cheat_typ']} ({e['hinrichtungs_methode']})")

    print("\n✅ Test abgeschlossen!")
