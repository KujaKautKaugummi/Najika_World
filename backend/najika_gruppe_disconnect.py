"""
NAJIKA GRUPPEN-DISCONNECT ABSTIMMUNGS-SYSTEM
==============================================

Fairness bei Disconnect in Gruppen-Kämpfen.

WICHTIG:
- Boss-HP skaliert NICHT runter bei Disconnect (kein Exploit!)
- Gruppe kann abstimmen: Weitermachen/Warten/Abbrechen
- Anti-Exploit: Cooldowns + Pattern-Erkennung
- Solo-Disconnect: Pause + Safe-Logout

"Tod = Tod. Aber nicht durch Disconnect."

Author: Claude Code (OPUS-1)
Date: 2026-02-01
"""

import time
import random
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from pathlib import Path

# ============================================================
# ENUMS & KONSTANTEN
# ============================================================

class DisconnectGrund(Enum):
    """Grund für Disconnect (falls bekannt)"""
    UNBEKANNT = "unbekannt"
    INTERNET = "internet"          # Echte Verbindungsprobleme
    ABSTURZ = "absturz"            # Client-Crash
    MANUELL = "manuell"            # Spieler hat beendet
    TIMEOUT = "timeout"            # Keine Antwort
    VERDAECHTIG = "verdaechtig"    # Pattern passt zu Exploit

class AbstimmungsOption(Enum):
    """Optionen bei Gruppen-Disconnect"""
    WEITERKAEMPFEN = "weiterkaempfen"  # Ohne disconnected Spieler
    WARTEN = "warten"                   # Auf Reconnect warten (max 60s)
    ABBRECHEN = "abbrechen"             # Boss resettet, Cooldown

class GruppenStatus(Enum):
    """Status einer Gruppe"""
    NORMAL = "normal"              # Normaler Kampf
    DISCONNECT_PAUSE = "pause"     # 5s Pause nach Disconnect
    ABSTIMMUNG = "abstimmung"      # Abstimmung läuft
    WARTEN_AUF_RECONNECT = "warten"
    KAMPF_OHNE_SPIELER = "ohne_spieler"
    ABGEBROCHEN = "abgebrochen"

# Cooldowns
COOLDOWNS = {
    "abbruch_gruppe": 600,      # 10 Min Cooldown nach Abbruch
    "abbruch_einzeln": 1800,    # 30 Min für den Disconnect-Spieler
    "warten_max": 60,           # Max 60s auf Reconnect warten
    "abstimmung_timeout": 15,   # 15s für Abstimmung
}

# Pattern-Schwellwerte für Exploit-Erkennung
EXPLOIT_SCHWELLEN = {
    "disconnects_pro_stunde": 3,       # Max 3 Disconnects/h bevor verdächtig
    "disconnect_bei_niedrig_hp": 3,    # 3x bei <20% HP = verdächtig
    "disconnect_bei_boss_special": 2,  # 2x bei Boss-Spezial = verdächtig
}

# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class DisconnectEvent:
    """Ein einzelner Disconnect"""
    event_id: str
    spieler_id: str
    zeitpunkt: float
    grund: DisconnectGrund

    # Kampf-Kontext (für Pattern-Erkennung)
    in_kampf: bool = False
    gegner_typ: str = ""          # "trash", "elite", "boss"
    spieler_hp_prozent: float = 100.0
    boss_hp_prozent: float = 100.0
    boss_aktion: str = ""         # z.B. "spezial_angriff"

    # Reconnect
    reconnected: bool = False
    reconnect_zeit: float = 0

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "spieler_id": self.spieler_id,
            "zeitpunkt": self.zeitpunkt,
            "grund": self.grund.value,
            "in_kampf": self.in_kampf,
            "gegner_typ": self.gegner_typ,
            "spieler_hp_prozent": self.spieler_hp_prozent,
            "boss_hp_prozent": self.boss_hp_prozent,
            "boss_aktion": self.boss_aktion,
            "reconnected": self.reconnected,
            "reconnect_zeit": self.reconnect_zeit
        }

@dataclass
class Abstimmung:
    """Eine laufende Abstimmung"""
    abstimmung_id: str
    gruppe_id: str
    gestartet: float
    timeout: float

    # Auslöser
    disconnect_spieler_id: str

    # Stimmen
    stimmen: Dict[str, AbstimmungsOption] = field(default_factory=dict)
    teilnehmer: List[str] = field(default_factory=list)

    # Ergebnis
    abgeschlossen: bool = False
    ergebnis: Optional[AbstimmungsOption] = None

    def to_dict(self) -> dict:
        return {
            "abstimmung_id": self.abstimmung_id,
            "gruppe_id": self.gruppe_id,
            "gestartet": self.gestartet,
            "timeout": self.timeout,
            "disconnect_spieler_id": self.disconnect_spieler_id,
            "stimmen": {k: v.value for k, v in self.stimmen.items()},
            "teilnehmer": self.teilnehmer,
            "abgeschlossen": self.abgeschlossen,
            "ergebnis": self.ergebnis.value if self.ergebnis else None
        }

@dataclass
class Gruppe:
    """Eine Spieler-Gruppe"""
    gruppe_id: str
    mitglieder: List[str]
    erstellt: float

    # Kampf-Status
    in_kampf: bool = False
    boss_id: Optional[str] = None
    boss_hp_start: int = 0
    boss_hp_aktuell: int = 0

    # Status
    status: GruppenStatus = GruppenStatus.NORMAL
    aktive_abstimmung: Optional[str] = None

    # Disconnected Spieler
    disconnected: List[str] = field(default_factory=list)

    # Cooldowns
    cooldowns: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "gruppe_id": self.gruppe_id,
            "mitglieder": self.mitglieder,
            "erstellt": self.erstellt,
            "in_kampf": self.in_kampf,
            "boss_id": self.boss_id,
            "boss_hp_start": self.boss_hp_start,
            "boss_hp_aktuell": self.boss_hp_aktuell,
            "status": self.status.value,
            "aktive_abstimmung": self.aktive_abstimmung,
            "disconnected": self.disconnected,
            "cooldowns": self.cooldowns
        }

@dataclass
class SpielerDisconnectProfil:
    """Tracking eines Spielers für Exploit-Erkennung"""
    spieler_id: str

    # Statistiken
    disconnects_gesamt: int = 0
    disconnects_letzte_stunde: int = 0
    letzte_stunde_reset: float = 0

    # Pattern
    disconnects_bei_niedrig_hp: int = 0
    disconnects_bei_boss_special: int = 0
    disconnects_kurz_vor_tod: int = 0

    # Strafen
    aktive_strafe: Optional[str] = None  # "warnung", "cooldown_1h", "cooldown_24h", "gruppe_bann"
    strafe_bis: float = 0
    warnungen: int = 0

    def to_dict(self) -> dict:
        return {
            "spieler_id": self.spieler_id,
            "disconnects_gesamt": self.disconnects_gesamt,
            "disconnects_letzte_stunde": self.disconnects_letzte_stunde,
            "disconnects_bei_niedrig_hp": self.disconnects_bei_niedrig_hp,
            "disconnects_bei_boss_special": self.disconnects_bei_boss_special,
            "aktive_strafe": self.aktive_strafe,
            "strafe_bis": self.strafe_bis,
            "warnungen": self.warnungen
        }

# ============================================================
# HAUPT-MANAGER
# ============================================================

class GruppenDisconnectSystem:
    """
    Verwaltet Disconnect-Handling in Gruppen.

    Ablauf bei Disconnect:
    1. Sofortige Pause (5 Sekunden)
    2. Alle sehen: "[Name] hat Verbindung verloren"
    3. Abstimmung (15 Sekunden): Weiterkämpfen/Warten/Abbrechen
    4. Je nach Wahl: Kampf fortsetzen oder abbrechen
    """

    def __init__(self):
        # Gruppen
        self.gruppen: Dict[str, Gruppe] = {}

        # Disconnect-Events
        self.disconnect_events: List[DisconnectEvent] = []

        # Abstimmungen
        self.abstimmungen: Dict[str, Abstimmung] = {}

        # Spieler-Profile (für Pattern-Erkennung)
        self.spieler_profile: Dict[str, SpielerDisconnectProfil] = {}

        # Statistiken
        self.stats = {
            "disconnects_gesamt": 0,
            "abstimmungen_gesamt": 0,
            "weitergekampft": 0,
            "gewartet_reconnect": 0,
            "abgebrochen": 0,
            "exploits_erkannt": 0
        }

        # State laden
        self._load_state()

    # --- Gruppen-Verwaltung ---

    def erstelle_gruppe(self, gruppe_id: str, mitglieder: List[str]) -> dict:
        """Erstellt eine neue Gruppe"""
        gruppe = Gruppe(
            gruppe_id=gruppe_id,
            mitglieder=mitglieder,
            erstellt=time.time()
        )
        self.gruppen[gruppe_id] = gruppe
        self._save_state()

        return {
            "erfolg": True,
            "gruppe": gruppe.to_dict()
        }

    def starte_boss_kampf(self, gruppe_id: str, boss_id: str, boss_hp: int) -> dict:
        """Markiert Gruppe als in Boss-Kampf"""
        if gruppe_id not in self.gruppen:
            return {"erfolg": False, "grund": "Gruppe nicht gefunden"}

        gruppe = self.gruppen[gruppe_id]
        gruppe.in_kampf = True
        gruppe.boss_id = boss_id
        gruppe.boss_hp_start = boss_hp
        gruppe.boss_hp_aktuell = boss_hp
        gruppe.status = GruppenStatus.NORMAL

        self._save_state()
        return {"erfolg": True}

    def beende_kampf(self, gruppe_id: str, gewonnen: bool) -> dict:
        """Beendet einen Kampf"""
        if gruppe_id not in self.gruppen:
            return {"erfolg": False, "grund": "Gruppe nicht gefunden"}

        gruppe = self.gruppen[gruppe_id]
        gruppe.in_kampf = False
        gruppe.boss_id = None
        gruppe.status = GruppenStatus.NORMAL
        gruppe.disconnected = []

        self._save_state()
        return {
            "erfolg": True,
            "gewonnen": gewonnen
        }

    # --- Disconnect Handling ---

    def handle_disconnect(self, spieler_id: str, gruppe_id: Optional[str],
                          kampf_kontext: dict) -> dict:
        """
        Verarbeitet einen Disconnect.

        kampf_kontext: {
            "in_kampf": bool,
            "gegner_typ": str,
            "spieler_hp_prozent": float,
            "boss_hp_prozent": float,
            "boss_aktion": str
        }
        """
        # Spieler-Profil aktualisieren
        profil = self._get_oder_erstelle_profil(spieler_id)
        self._update_profil(profil, kampf_kontext)

        # Disconnect-Event erstellen
        event = DisconnectEvent(
            event_id=f"dc_{int(time.time())}_{random.randint(1000, 9999)}",
            spieler_id=spieler_id,
            zeitpunkt=time.time(),
            grund=self._ermittle_grund(profil, kampf_kontext),
            in_kampf=kampf_kontext.get("in_kampf", False),
            gegner_typ=kampf_kontext.get("gegner_typ", ""),
            spieler_hp_prozent=kampf_kontext.get("spieler_hp_prozent", 100),
            boss_hp_prozent=kampf_kontext.get("boss_hp_prozent", 100),
            boss_aktion=kampf_kontext.get("boss_aktion", "")
        )
        self.disconnect_events.append(event)
        self.stats["disconnects_gesamt"] += 1

        # Exploit-Check
        exploit_warnung = self._pruefe_exploit(profil, event)
        if exploit_warnung:
            self.stats["exploits_erkannt"] += 1

        # Solo oder Gruppe?
        if not gruppe_id or gruppe_id not in self.gruppen:
            # Solo-Disconnect
            return self._handle_solo_disconnect(spieler_id, event, exploit_warnung)

        # Gruppen-Disconnect
        return self._handle_gruppe_disconnect(spieler_id, gruppe_id, event, exploit_warnung)

    def _handle_solo_disconnect(self, spieler_id: str, event: DisconnectEvent,
                                 exploit_warnung: Optional[dict]) -> dict:
        """Behandelt Solo-Disconnect"""
        return {
            "typ": "solo",
            "aktion": "pause",
            "nachricht": f"Verbindung unterbrochen. Spiel pausiert.",
            "reconnect_window": 30,  # 30 Sekunden zum Reconnect
            "event_id": event.event_id,
            "exploit_warnung": exploit_warnung,
            "hinweis": "Kein Tod durch Disconnect! Kampf ist pausiert."
        }

    def _handle_gruppe_disconnect(self, spieler_id: str, gruppe_id: str,
                                    event: DisconnectEvent,
                                    exploit_warnung: Optional[dict]) -> dict:
        """Behandelt Gruppen-Disconnect"""
        gruppe = self.gruppen[gruppe_id]

        # Spieler als disconnected markieren
        if spieler_id not in gruppe.disconnected:
            gruppe.disconnected.append(spieler_id)

        # Gruppe in Pause setzen
        gruppe.status = GruppenStatus.DISCONNECT_PAUSE

        # Abstimmung starten (nach 5s Pause)
        abstimmung = self._starte_abstimmung(gruppe, spieler_id)

        self._save_state()

        return {
            "typ": "gruppe",
            "aktion": "abstimmung",
            "nachricht": f"[{spieler_id}] hat Verbindung verloren!",
            "pause_dauer": 5,
            "abstimmung": abstimmung.to_dict(),
            "optionen": {
                "weiterkaempfen": "Kampf ohne Spieler fortsetzen (Boss-HP bleibt gleich!)",
                "warten": f"Auf Reconnect warten (max {COOLDOWNS['warten_max']}s)",
                "abbrechen": f"Abbrechen (Gruppe: {COOLDOWNS['abbruch_gruppe']//60}min Cooldown)"
            },
            "event_id": event.event_id,
            "exploit_warnung": exploit_warnung
        }

    def _starte_abstimmung(self, gruppe: Gruppe, disconnect_spieler_id: str) -> Abstimmung:
        """Startet Abstimmung in Gruppe"""
        abstimmung_id = f"vote_{int(time.time())}_{random.randint(1000, 9999)}"

        # Teilnehmer = alle außer disconnected
        teilnehmer = [m for m in gruppe.mitglieder if m not in gruppe.disconnected]

        abstimmung = Abstimmung(
            abstimmung_id=abstimmung_id,
            gruppe_id=gruppe.gruppe_id,
            gestartet=time.time(),
            timeout=time.time() + COOLDOWNS["abstimmung_timeout"],
            disconnect_spieler_id=disconnect_spieler_id,
            teilnehmer=teilnehmer
        )

        self.abstimmungen[abstimmung_id] = abstimmung
        gruppe.aktive_abstimmung = abstimmung_id
        gruppe.status = GruppenStatus.ABSTIMMUNG
        self.stats["abstimmungen_gesamt"] += 1

        return abstimmung

    # --- Abstimmung ---

    def stimme_ab(self, abstimmung_id: str, spieler_id: str, wahl: str) -> dict:
        """Spieler gibt Stimme ab"""
        if abstimmung_id not in self.abstimmungen:
            return {"erfolg": False, "grund": "Abstimmung nicht gefunden"}

        abstimmung = self.abstimmungen[abstimmung_id]

        if abstimmung.abgeschlossen:
            return {"erfolg": False, "grund": "Abstimmung bereits beendet"}

        if spieler_id not in abstimmung.teilnehmer:
            return {"erfolg": False, "grund": "Du bist kein Teilnehmer dieser Abstimmung"}

        if time.time() > abstimmung.timeout:
            # Timeout - automatisch entscheiden
            return self._beende_abstimmung_timeout(abstimmung)

        try:
            option = AbstimmungsOption(wahl)
        except ValueError:
            return {"erfolg": False, "grund": f"Ungültige Option: {wahl}"}

        abstimmung.stimmen[spieler_id] = option
        self._save_state()

        # Alle abgestimmt?
        if len(abstimmung.stimmen) >= len(abstimmung.teilnehmer):
            return self._werte_abstimmung_aus(abstimmung)

        return {
            "erfolg": True,
            "stimme_gezaehlt": True,
            "stimmen_abgegeben": len(abstimmung.stimmen),
            "stimmen_noetig": len(abstimmung.teilnehmer),
            "verbleibende_zeit": abstimmung.timeout - time.time()
        }

    def _werte_abstimmung_aus(self, abstimmung: Abstimmung) -> dict:
        """Wertet Abstimmung aus"""
        # Stimmen zählen
        zaehlung = {
            AbstimmungsOption.WEITERKAEMPFEN: 0,
            AbstimmungsOption.WARTEN: 0,
            AbstimmungsOption.ABBRECHEN: 0
        }

        for stimme in abstimmung.stimmen.values():
            zaehlung[stimme] += 1

        # Gewinner ermitteln (Mehrheit)
        gewinner = max(zaehlung, key=zaehlung.get)

        abstimmung.abgeschlossen = True
        abstimmung.ergebnis = gewinner
        self._save_state()

        # Aktion ausführen
        return self._fuehre_abstimmungsergebnis_aus(abstimmung, gewinner, zaehlung)

    def _beende_abstimmung_timeout(self, abstimmung: Abstimmung) -> dict:
        """Beendet Abstimmung bei Timeout"""
        # Bei Timeout: Standard ist WARTEN (fairste Option)
        abstimmung.abgeschlossen = True
        abstimmung.ergebnis = AbstimmungsOption.WARTEN
        self._save_state()

        return {
            "erfolg": True,
            "timeout": True,
            "ergebnis": "warten",
            "nachricht": "Abstimmung timeout - es wird auf Reconnect gewartet."
        }

    def _fuehre_abstimmungsergebnis_aus(self, abstimmung: Abstimmung,
                                         gewinner: AbstimmungsOption,
                                         zaehlung: dict) -> dict:
        """Führt Ergebnis der Abstimmung aus"""
        gruppe = self.gruppen.get(abstimmung.gruppe_id)
        if not gruppe:
            return {"erfolg": False, "grund": "Gruppe nicht mehr gefunden"}

        if gewinner == AbstimmungsOption.WEITERKAEMPFEN:
            return self._aktion_weiterkaempfen(gruppe, abstimmung, zaehlung)

        elif gewinner == AbstimmungsOption.WARTEN:
            return self._aktion_warten(gruppe, abstimmung, zaehlung)

        elif gewinner == AbstimmungsOption.ABBRECHEN:
            return self._aktion_abbrechen(gruppe, abstimmung, zaehlung)

    def _aktion_weiterkaempfen(self, gruppe: Gruppe, abstimmung: Abstimmung,
                                zaehlung: dict) -> dict:
        """Kampf ohne disconnected Spieler fortsetzen"""
        gruppe.status = GruppenStatus.KAMPF_OHNE_SPIELER
        gruppe.aktive_abstimmung = None
        self.stats["weitergekampft"] += 1
        self._save_state()

        return {
            "erfolg": True,
            "ergebnis": "weiterkaempfen",
            "stimmen": {k.value: v for k, v in zaehlung.items()},
            "nachricht": "Kampf wird ohne Spieler fortgesetzt!",
            "hinweis": "Boss-HP bleibt UNVERÄNDERT - kein Free-Pass!",
            "disconnected_spieler": {
                "id": abstimmung.disconnect_spieler_id,
                "status": "geist",  # Untargetbar, kann später rejoinen
                "kann_rejoinen": True
            }
        }

    def _aktion_warten(self, gruppe: Gruppe, abstimmung: Abstimmung,
                        zaehlung: dict) -> dict:
        """Auf Reconnect warten"""
        gruppe.status = GruppenStatus.WARTEN_AUF_RECONNECT
        gruppe.aktive_abstimmung = None
        self.stats["gewartet_reconnect"] += 1
        self._save_state()

        return {
            "erfolg": True,
            "ergebnis": "warten",
            "stimmen": {k.value: v for k, v in zaehlung.items()},
            "nachricht": f"Warten auf Reconnect (max {COOLDOWNS['warten_max']}s)",
            "warten_bis": time.time() + COOLDOWNS["warten_max"],
            "boss_pausiert": True,
            "hinweis": "Jeder kann jederzeit Abstimmung für Weitermachen/Abbrechen starten"
        }

    def _aktion_abbrechen(self, gruppe: Gruppe, abstimmung: Abstimmung,
                           zaehlung: dict) -> dict:
        """Kampf abbrechen"""
        gruppe.status = GruppenStatus.ABGEBROCHEN
        gruppe.aktive_abstimmung = None
        gruppe.in_kampf = False

        # Cooldowns setzen
        jetzt = time.time()
        for mitglied in gruppe.mitglieder:
            gruppe.cooldowns[mitglied] = jetzt + COOLDOWNS["abbruch_gruppe"]

        # Disconnect-Spieler bekommt längeren Cooldown
        disconnect_spieler = abstimmung.disconnect_spieler_id
        if disconnect_spieler:
            gruppe.cooldowns[disconnect_spieler] = jetzt + COOLDOWNS["abbruch_einzeln"]

        self.stats["abgebrochen"] += 1
        self._save_state()

        return {
            "erfolg": True,
            "ergebnis": "abbrechen",
            "stimmen": {k.value: v for k, v in zaehlung.items()},
            "nachricht": "Kampf abgebrochen. Boss wird zurückgesetzt.",
            "cooldowns": {
                "gruppe": COOLDOWNS["abbruch_gruppe"],
                "disconnect_spieler": COOLDOWNS["abbruch_einzeln"]
            },
            "hinweis": "Exploit-Schutz: Absichtlicher Disconnect = längerer Cooldown!"
        }

    # --- Reconnect ---

    def handle_reconnect(self, spieler_id: str, gruppe_id: Optional[str]) -> dict:
        """Verarbeitet Reconnect eines Spielers"""
        # Event aktualisieren
        for event in reversed(self.disconnect_events):
            if event.spieler_id == spieler_id and not event.reconnected:
                event.reconnected = True
                event.reconnect_zeit = time.time() - event.zeitpunkt
                break

        if not gruppe_id or gruppe_id not in self.gruppen:
            return {
                "erfolg": True,
                "typ": "solo",
                "nachricht": "Willkommen zurück! Spiel wird fortgesetzt."
            }

        gruppe = self.gruppen[gruppe_id]

        # Aus disconnected entfernen
        if spieler_id in gruppe.disconnected:
            gruppe.disconnected.remove(spieler_id)

        # Gruppe-Status aktualisieren
        if gruppe.status == GruppenStatus.WARTEN_AUF_RECONNECT:
            if len(gruppe.disconnected) == 0:
                gruppe.status = GruppenStatus.NORMAL

        self._save_state()

        return {
            "erfolg": True,
            "typ": "gruppe",
            "nachricht": "Willkommen zurück! Du bist wieder im Kampf.",
            "gruppe_status": gruppe.status.value,
            "hp_strafe": 20,  # 20% weniger HP als Reconnect-Strafe
            "hinweis": "Du startest mit reduziertem HP als Reconnect-Strafe."
        }

    # --- Pattern-Erkennung & Exploit-Schutz ---

    def _get_oder_erstelle_profil(self, spieler_id: str) -> SpielerDisconnectProfil:
        """Holt oder erstellt Spieler-Profil"""
        if spieler_id not in self.spieler_profile:
            self.spieler_profile[spieler_id] = SpielerDisconnectProfil(spieler_id=spieler_id)
        return self.spieler_profile[spieler_id]

    def _update_profil(self, profil: SpielerDisconnectProfil, kontext: dict):
        """Aktualisiert Spieler-Profil mit Disconnect-Daten"""
        jetzt = time.time()

        # Reset stündliche Zählung wenn nötig
        if jetzt - profil.letzte_stunde_reset > 3600:
            profil.disconnects_letzte_stunde = 0
            profil.letzte_stunde_reset = jetzt

        profil.disconnects_gesamt += 1
        profil.disconnects_letzte_stunde += 1

        # Pattern tracken
        if kontext.get("spieler_hp_prozent", 100) < 20:
            profil.disconnects_bei_niedrig_hp += 1

        if kontext.get("boss_aktion") in ["spezial_angriff", "ultimate", "aoe"]:
            profil.disconnects_bei_boss_special += 1

    def _ermittle_grund(self, profil: SpielerDisconnectProfil, kontext: dict) -> DisconnectGrund:
        """Ermittelt wahrscheinlichen Disconnect-Grund"""
        # Verdächtig wenn Pattern passt
        if (profil.disconnects_bei_niedrig_hp >= EXPLOIT_SCHWELLEN["disconnect_bei_niedrig_hp"] or
            profil.disconnects_bei_boss_special >= EXPLOIT_SCHWELLEN["disconnect_bei_boss_special"]):
            return DisconnectGrund.VERDAECHTIG

        # Ansonsten unbekannt (wir geben Benefit of Doubt)
        return DisconnectGrund.UNBEKANNT

    def _pruefe_exploit(self, profil: SpielerDisconnectProfil,
                         event: DisconnectEvent) -> Optional[dict]:
        """Prüft auf Exploit-Missbrauch"""
        warnungen = []

        # Zu viele Disconnects pro Stunde?
        if profil.disconnects_letzte_stunde > EXPLOIT_SCHWELLEN["disconnects_pro_stunde"]:
            warnungen.append(f"Zu viele Disconnects ({profil.disconnects_letzte_stunde}/h)")

        # Pattern: Immer bei niedrigem HP?
        if profil.disconnects_bei_niedrig_hp >= EXPLOIT_SCHWELLEN["disconnect_bei_niedrig_hp"]:
            warnungen.append(f"Pattern erkannt: Disconnect bei niedrigem HP ({profil.disconnects_bei_niedrig_hp}x)")

        # Pattern: Immer bei Boss-Spezial?
        if profil.disconnects_bei_boss_special >= EXPLOIT_SCHWELLEN["disconnect_bei_boss_special"]:
            warnungen.append(f"Pattern erkannt: Disconnect bei Boss-Spezial ({profil.disconnects_bei_boss_special}x)")

        if not warnungen:
            return None

        # Strafe verhängen
        profil.warnungen += 1

        if profil.warnungen == 1:
            profil.aktive_strafe = "warnung"
            stufe = "Stufe 1: Warnung"
        elif profil.warnungen == 2:
            profil.aktive_strafe = "cooldown_1h"
            profil.strafe_bis = time.time() + 3600
            stufe = "Stufe 2: 1h Cooldown"
        elif profil.warnungen == 3:
            profil.aktive_strafe = "cooldown_24h"
            profil.strafe_bis = time.time() + 86400
            stufe = "Stufe 3: 24h Cooldown"
        else:
            profil.aktive_strafe = "gruppe_bann"
            profil.strafe_bis = time.time() + 604800  # 7 Tage
            stufe = "Stufe 4: 7 Tage Gruppen-Bann"

        self._save_state()

        return {
            "erkannt": True,
            "warnungen": warnungen,
            "strafe": stufe,
            "profil_warnungen": profil.warnungen,
            "nachricht": "Verdächtiges Disconnect-Pattern erkannt! Wiederholter Missbrauch führt zu Strafen."
        }

    def hat_cooldown(self, spieler_id: str, gruppe_id: Optional[str] = None) -> dict:
        """Prüft ob Spieler Cooldown hat"""
        profil = self.spieler_profile.get(spieler_id)

        # Strafe aktiv?
        if profil and profil.strafe_bis > time.time():
            return {
                "hat_cooldown": True,
                "grund": profil.aktive_strafe,
                "bis": profil.strafe_bis,
                "verbleibend": profil.strafe_bis - time.time()
            }

        # Gruppen-Cooldown?
        if gruppe_id and gruppe_id in self.gruppen:
            gruppe = self.gruppen[gruppe_id]
            cooldown_bis = gruppe.cooldowns.get(spieler_id, 0)
            if cooldown_bis > time.time():
                return {
                    "hat_cooldown": True,
                    "grund": "gruppen_abbruch",
                    "bis": cooldown_bis,
                    "verbleibend": cooldown_bis - time.time()
                }

        return {"hat_cooldown": False}

    # --- Statistiken ---

    def get_stats(self) -> dict:
        """Gibt System-Statistiken zurück"""
        return {
            **self.stats,
            "gruppen_aktiv": len([g for g in self.gruppen.values() if g.in_kampf]),
            "abstimmungen_aktiv": len([a for a in self.abstimmungen.values() if not a.abgeschlossen]),
            "spieler_mit_warnungen": len([p for p in self.spieler_profile.values() if p.warnungen > 0])
        }

    def get_spieler_statistik(self, spieler_id: str) -> dict:
        """Gibt Spieler-Statistik zurück"""
        profil = self.spieler_profile.get(spieler_id)
        if not profil:
            return {"disconnects_gesamt": 0, "warnungen": 0}
        return profil.to_dict()

    # --- Persistenz ---

    def _save_state(self):
        """Speichert State"""
        state = {
            "gruppen": {k: v.to_dict() for k, v in self.gruppen.items()},
            "abstimmungen": {k: v.to_dict() for k, v in self.abstimmungen.items()},
            "spieler_profile": {k: v.to_dict() for k, v in self.spieler_profile.items()},
            "stats": self.stats,
            "disconnect_events": [e.to_dict() for e in self.disconnect_events[-1000:]]  # Letzte 1000
        }

        path = Path(__file__).parent / "gruppe_disconnect_state.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        """Lädt State"""
        path = Path(__file__).parent / "gruppe_disconnect_state.json"
        if not path.exists():
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)

            # Gruppen laden
            for k, v in state.get("gruppen", {}).items():
                self.gruppen[k] = Gruppe(
                    gruppe_id=v["gruppe_id"],
                    mitglieder=v["mitglieder"],
                    erstellt=v["erstellt"],
                    in_kampf=v.get("in_kampf", False),
                    boss_id=v.get("boss_id"),
                    boss_hp_start=v.get("boss_hp_start", 0),
                    boss_hp_aktuell=v.get("boss_hp_aktuell", 0),
                    status=GruppenStatus(v.get("status", "normal")),
                    disconnected=v.get("disconnected", []),
                    cooldowns=v.get("cooldowns", {})
                )

            # Profile laden
            for k, v in state.get("spieler_profile", {}).items():
                self.spieler_profile[k] = SpielerDisconnectProfil(
                    spieler_id=v["spieler_id"],
                    disconnects_gesamt=v.get("disconnects_gesamt", 0),
                    disconnects_letzte_stunde=v.get("disconnects_letzte_stunde", 0),
                    disconnects_bei_niedrig_hp=v.get("disconnects_bei_niedrig_hp", 0),
                    disconnects_bei_boss_special=v.get("disconnects_bei_boss_special", 0),
                    aktive_strafe=v.get("aktive_strafe"),
                    strafe_bis=v.get("strafe_bis", 0),
                    warnungen=v.get("warnungen", 0)
                )

            self.stats = state.get("stats", self.stats)

        except Exception as e:
            print(f"[DISCONNECT] Fehler beim Laden: {e}")


# ============================================================
# SINGLETON
# ============================================================

_system: Optional[GruppenDisconnectSystem] = None

def get_disconnect_system() -> GruppenDisconnectSystem:
    """Gibt Singleton-Instanz zurück"""
    global _system
    if _system is None:
        _system = GruppenDisconnectSystem()
    return _system


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("🔌 Gruppen-Disconnect System Test")
    print("=" * 50)

    system = get_disconnect_system()

    # Test: Gruppe erstellen
    print("\n1. Erstelle Gruppe...")
    result = system.erstelle_gruppe("gruppe1", ["tank", "healer", "dps1", "dps2"])
    print(f"   Gruppe erstellt: {result['erfolg']}")

    # Test: Boss-Kampf starten
    print("\n2. Starte Boss-Kampf...")
    result = system.starte_boss_kampf("gruppe1", "boss_dragon", 100000)
    print(f"   Kampf gestartet: {result['erfolg']}")

    # Test: Tank disconnected
    print("\n3. Tank disconnected während Boss-Kampf...")
    result = system.handle_disconnect("tank", "gruppe1", {
        "in_kampf": True,
        "gegner_typ": "boss",
        "spieler_hp_prozent": 45,
        "boss_hp_prozent": 60,
        "boss_aktion": "normaler_angriff"
    })
    print(f"   Typ: {result['typ']}")
    print(f"   Aktion: {result['aktion']}")
    print(f"   Nachricht: {result['nachricht']}")

    # Test: Abstimmung
    if "abstimmung" in result:
        abstimmung_id = result["abstimmung"]["abstimmung_id"]
        print(f"\n4. Abstimmung läuft: {abstimmung_id}")

        # Healer stimmt für Warten
        result = system.stimme_ab(abstimmung_id, "healer", "warten")
        print(f"   Healer stimmt: warten - {result.get('erfolg')}")

        # DPS1 stimmt für Weiterkämpfen
        result = system.stimme_ab(abstimmung_id, "dps1", "weiterkaempfen")
        print(f"   DPS1 stimmt: weiterkaempfen - {result.get('erfolg')}")

        # DPS2 stimmt für Warten
        result = system.stimme_ab(abstimmung_id, "dps2", "warten")
        print(f"   DPS2 stimmt: warten")
        print(f"   Ergebnis: {result.get('ergebnis')}")

    # Stats
    print("\n5. System Stats:")
    stats = system.get_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")

    print("\n✅ Test abgeschlossen!")
