"""
NAJIKA SAFE-ZONE SYSTEM
=======================

Definiert Zonen-Logik fuer Permadeath, PvP und Safe-Zones.

Design-Grundsatz (aus NEUE_GAMEPLAY_IDEEN_2026-02-21 + COMBAT_SYSTEM_KOMPLETT_V3):
  - Staedte und Doerfer = SICHER (kein PvP, kein Permadeath)
  - Schwarze Muehle    = 100% Safe (immer)
  - Wildnis/Dungeons   = Permadeath moeglich
  - Ranger-System      = organischer PvP-Content mit Konsequenzen
  - Duell-System       = consensuales PvP ueberall

Erstellt: 2026-02-22
"""

from enum import Enum
from typing import Optional
import time


# ===========================================================================
# ZONE TYPEN
# ===========================================================================

class ZoneType(Enum):
    """Alle moeglichen Zonen-Typen in Najika World."""
    # 100% Sicher - niemals Kampf moeglich
    ABSOLUTE_SAFE = "absolute_safe"       # Schwarze Muehle, Tutorial
    # Sicher - kein PvP, kein Permadeath, aber NPC-Angriffe moeglich (z.B. Guard)
    SAFE_ZONE = "safe_zone"               # Alle Staedte und Doerfer
    # Trainingsgelaende - PvP nur mit Zustimmung, kein Permadeath
    TRAINING_GROUND = "training_ground"   # Trainingsgelaende, Slime-Arena
    # Arena - spezielles PvP ohne Permadeath (ausser Hardcore-Modus)
    ARENA = "arena"                       # Slime-Arena, Spieler-Arena
    # Offene Welt - PvP nur auf Anfrage (Duell), aber Permadeath bei Mobs
    OVERWORLD = "overworld"               # Alle 8 Regionen Aussenbereich
    # Dungeon - Permadeath aktiv, kein PvP (ausser Dungeon-PvP Modus)
    DUNGEON = "dungeon"                   # Alle Dungeons
    # Wildnis - Permadeath aktiv, kein unfreiwilliges PvP
    WILDERNESS = "wilderness"             # Tiefer Wald, Wueste etc.
    # PvP-Zone - markiert fuer freiwilliges PvP, Permadeath aktiv
    PVP_ZONE = "pvp_zone"                 # Designated PvP areas


# ===========================================================================
# ZONEN-DATENBANK  (alle bekannten Orte mit Zone-Typ)
# ===========================================================================

ZONE_DATABASE: dict[str, dict] = {
    # ----------------------------------------------------------------
    # ABSOLUTE SAFE ZONES
    # ----------------------------------------------------------------
    "schwarze_muehle": {
        "display_name": "Die Schwarze Muehle",
        "zone_type": ZoneType.ABSOLUTE_SAFE,
        "description": "Das soziale Herzstueck der Welt. Immer 100% sicher.",
        "pvp_allowed": False,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
    },
    "tutorial_area": {
        "display_name": "Startgebiet",
        "zone_type": ZoneType.ABSOLUTE_SAFE,
        "description": "Neue Spieler-Schutzbereich.",
        "pvp_allowed": False,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
    },

    # ----------------------------------------------------------------
    # STAEDTE UND DOERFER  (alle SAFE_ZONE)
    # Echte Namen aus cities.json - 5 Staedte (3 Regionen haben keine!)
    # ----------------------------------------------------------------
    "handelsfestung": {
        "display_name": "Handelsfestung",
        "zone_type": ZoneType.SAFE_ZONE,
        "region": "heisse_duenen",
        "description": "Hauptstadt in den Heissen Duenen. Trading Hub, PvP-Arena, Player-Shops.",
        "pvp_allowed": False,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
        "is_capital": True,
    },
    "dampf_hain": {
        "display_name": "Dampf-Hain",
        "zone_type": ZoneType.SAFE_ZONE,
        "region": "samtmoos_tiefwald",
        "description": "Mystischer Onsen-Ort im Samtmoos-Tiefwald. Heisse Quellen, Druiden-Zirkel.",
        "pvp_allowed": False,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
    },
    "salzige_bucht": {
        "display_name": "Salzige Bucht",
        "zone_type": ZoneType.SAFE_ZONE,
        "region": "salzwind_kueste",
        "description": "Hafenstadt an der Salzwind-Kueste. Fischmarkt, Leuchtturm, Piraten-Flair.",
        "pvp_allowed": False,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
    },
    "runenheim": {
        "display_name": "Runenheim",
        "zone_type": ZoneType.SAFE_ZONE,
        "region": "blitzebene",
        "description": "Magie-Akademie in der Blitzebene. Runen-Altar, Skill-Trainer.",
        "pvp_allowed": False,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
    },
    "funken_siedlung": {
        "display_name": "Funken-Siedlung",
        "zone_type": ZoneType.SAFE_ZONE,
        "region": "magmastroeme",
        "description": "Vulkan-Schmiede in den Magmastroemen. Meister-Schmied, Lava-Docks.",
        "pvp_allowed": False,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
    },
    # HINWEIS: 3 Regionen haben KEINE Stadt:
    # - reich_der_drei:     Nur Untote und Nekromanten
    # - gruenschlamm_sumpf: Nur Hexen-Territory (Funkelnest = versteckte Schatzhoehle)
    # - tiefenhoehlen:      Mehrere Goblin-Siedlungen, keine Hauptstadt

    # ----------------------------------------------------------------
    # TRAININGSGELAENDE
    # ----------------------------------------------------------------
    "trainingsgelaende_zentral": {
        "display_name": "Zentrales Trainingsgelaende",
        "zone_type": ZoneType.TRAINING_GROUND,
        "pvp_allowed": False,        # Nur mit Zustimmung beider (Duell)
        "permadeath_active": False,
        "ranger_pvp_exception": False,
        "sparring_allowed": True,    # Sparring/Duell moeglich aber optional
    },

    # ----------------------------------------------------------------
    # ARENEN
    # ----------------------------------------------------------------
    "slime_arena": {
        "display_name": "Slime-Arena",
        "zone_type": ZoneType.ARENA,
        "pvp_allowed": True,         # In Arena = freiwillig
        "permadeath_active": False,  # Ausser Hardcore-Modus!
        "ranger_pvp_exception": False,
        "hardcore_mode_available": True,
    },
    "spieler_arena": {
        "display_name": "Spieler-Arena",
        "zone_type": ZoneType.ARENA,
        "pvp_allowed": True,
        "permadeath_active": False,
        "ranger_pvp_exception": False,
        "hardcore_mode_available": True,
    },

    # ----------------------------------------------------------------
    # OVERWORLD (alle 8 Regionen)
    # Echte Namen aus regions.json!
    # Der Goetterfels liegt ZENTRAL in ALLEN 8 Regionen (wie Mount Everest)
    # ----------------------------------------------------------------
    "samtmoos_tiefwald": {
        "display_name": "Samtmoos-Tiefwald (Wald)",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "forest",
        "city": "dampf_hain",
        "pvp_allowed": False,        # Nur via Duell!
        "permadeath_active": True,   # Mob-Kaempfe = echtes Risiko
        "ranger_pvp_exception": True,
    },
    "reich_der_drei": {
        "display_name": "Reich der Drei - Kaelte Frost Eis",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "ice",
        "city": None,                # Nur Untote und Nekromanten!
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": True,
    },
    "salzwind_kueste": {
        "display_name": "Salzwind-Kueste",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "coast",
        "city": "salzige_bucht",
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": True,
    },
    "blitzebene": {
        "display_name": "Blitzebene (Hochland)",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "highland",
        "city": "runenheim",
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": True,
    },
    "gruenschlamm_sumpf": {
        "display_name": "Gruenschlamm-Sumpf",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "swamp",
        "city": None,                # Nur Hexen-Territory!
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": True,
    },
    "magmastroeme": {
        "display_name": "Magmastroeme (Vulkan)",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "volcano",
        "city": "funken_siedlung",
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": True,
    },
    "heisse_duenen": {
        "display_name": "Heisse Duenen (Wueste)",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "desert",
        "city": "handelsfestung",    # HAUPTSTADT!
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": True,
    },
    "tiefenhoehlen": {
        "display_name": "Tiefenhoehlen",
        "zone_type": ZoneType.OVERWORLD,
        "biome": "caves",
        "city": None,                # Goblin-Siedlungen, keine Hauptstadt
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": True,
        "underground": True,
    },

    # ----------------------------------------------------------------
    # GOETTERFELS - Zentraler Berg, wie Mount Everest
    # KEIN Dungeon! KEIN eigenes Biom! Liegt physisch in ALLEN 8 Regionen.
    # Je nach Region unterschiedlich hoch/zugaenglich.
    # Manche Seiten so steil/hoch dass man nicht raufkommt.
    # ----------------------------------------------------------------
    "goetterfels": {
        "display_name": "Goetterfels (Zentral-Berg)",
        "zone_type": ZoneType.OVERWORLD,  # Berg = Overworld, KEIN Dungeon!
        "biome": "mountain",
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": False,
        "indestructible": True,
        "note": (
            "Wie Mount Everest - liegt ZENTRAL in allen 8 Regionen. "
            "Verschiedene Zugaenge je nach Region, manche Seiten unbesteigbar. "
            "Schwarze Muehle liegt am/auf dem Goetterfels."
        ),
    },
    # NUR die Innenbereiche des Goetterfels sind Dungeon-artig:
    "goetterfels_schmelzwelt": {
        "display_name": "Goetterfels - Schmelzwelt (Inneres)",
        "zone_type": ZoneType.DUNGEON,
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": False,
        "note": "Lava-Welt im Inneren des Berges. Endgame-Bosse, bestes Loot.",
    },
    "goetterfels_turm": {
        "display_name": "Goetterfels - Turm der 100 Pruefungen",
        "zone_type": ZoneType.DUNGEON,
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": False,
        "note": "Erst verfuegbar NACHDEM Najika den Goetterfels gesprengt hat!",
    },

    # ----------------------------------------------------------------
    # DUNGEONS
    # ----------------------------------------------------------------
    "dungeon_katakomben": {
        "display_name": "Katakomben",
        "zone_type": ZoneType.DUNGEON,
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": False,
    },
    "dungeon_kristallhoehle": {
        "display_name": "Kristallhoehle",
        "zone_type": ZoneType.DUNGEON,
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": False,
    },
    "dungeon_verfluchte_ruinen": {
        "display_name": "Verfluchte Ruinen",
        "zone_type": ZoneType.DUNGEON,
        "pvp_allowed": False,
        "permadeath_active": True,
        "ranger_pvp_exception": False,
    },
}


# ===========================================================================
# RANGER-SYSTEM KONFIGURATION
# ===========================================================================

# Rang-Schwelle ab der Ranger-Transporte ueberfallen werden KOENNEN
# (niedrigere Raenge sind vollstaendig geschuetzt)
RANGER_PVP_MIN_RANK = 25  # Rang 1-24 = geschuetzt, Rang 25+ = PvP moeglich

# Bounty wenn man einen Ranger ueberfaellt und GESEHEN wird
RANGER_RAID_BOUNTY = 5000  # Goldmuenzen Kopfgeld
RANGER_RAID_REP_LOSS = -50  # Ruf-Verlust (sehr stark!)


# ===========================================================================
# HAUPT-KLASSE: SafeZoneSystem
# ===========================================================================

class SafeZoneSystem:
    """
    Zentrales Safe-Zone System.
    Wird von CombatSystem, PermadeathSystem und RangerSystem verwendet.
    """

    def __init__(self):
        self.zones = ZONE_DATABASE
        # Aktive Duell-Anfragen: {anfragender_spieler_id: {ziel_spieler_id, timestamp}}
        self._pending_duels: dict[str, dict] = {}
        # Aktive Ranger-Transporte: {ranger_id: {rang, zone_id, start_time}}
        self._active_ranger_transports: dict[str, dict] = {}

    # -------------------------------------------------------------------
    # KERN-ABFRAGEN
    # -------------------------------------------------------------------

    def get_zone(self, zone_id: str) -> Optional[dict]:
        """Gibt Zone-Daten zurueck, oder None wenn unbekannt (behandle als Overworld)."""
        return self.zones.get(zone_id)

    def get_zone_type(self, zone_id: str) -> ZoneType:
        """Gibt Zone-Typ zurueck. Unbekannte Zonen = Overworld."""
        zone = self.zones.get(zone_id)
        if zone:
            return zone["zone_type"]
        return ZoneType.OVERWORLD  # Default: Draussen = riskant

    def is_safe_zone(self, zone_id: str) -> bool:
        """Ist diese Zone eine sichere Zone (kein Permadeath, kein unfreiwilliges PvP)?"""
        zone_type = self.get_zone_type(zone_id)
        return zone_type in (ZoneType.ABSOLUTE_SAFE, ZoneType.SAFE_ZONE)

    def is_permadeath_active(self, zone_id: str, hardcore_mode: bool = False) -> bool:
        """Ist Permadeath in dieser Zone aktiv?"""
        zone = self.zones.get(zone_id)
        if zone is None:
            return True  # Unbekannte Zone = gefaehrlich
        if zone.get("permadeath_active", False):
            return True
        # Arenen im Hardcore-Modus = Permadeath
        if hardcore_mode and zone.get("hardcore_mode_available", False):
            return True
        return False

    # -------------------------------------------------------------------
    # PVP-LOGIK
    # -------------------------------------------------------------------

    def can_attack_player(
        self,
        attacker_id: str,
        target_id: str,
        zone_id: str,
        attacker_ranger_rank: int = 0,
        target_ranger_rank: int = 0,
        is_consented_duel: bool = False
    ) -> tuple[bool, str]:
        """
        Prueft ob ein Spieler einen anderen angreifen kann.

        Returns:
            (erlaubt: bool, grund: str)
        """
        zone_type = self.get_zone_type(zone_id)

        # 1. Absolute Safe Zone = niemals Angriff moeglich
        if zone_type == ZoneType.ABSOLUTE_SAFE:
            return False, "absolute_safe_zone"

        # 2. Safe Zone = nur Duell (beide muessen zugestimmt haben)
        if zone_type == ZoneType.SAFE_ZONE:
            if is_consented_duel:
                return True, "consented_duel_in_safe_zone"
            return False, "safe_zone_no_pvp"

        # 3. Trainingsgelaende = nur Sparring/Duell
        if zone_type == ZoneType.TRAINING_GROUND:
            if is_consented_duel:
                return True, "sparring_match"
            return False, "training_ground_no_forced_pvp"

        # 4. Arena = PvP erlaubt (Arena-Kampf)
        if zone_type == ZoneType.ARENA:
            return True, "arena_fight"

        # 5. Overworld / Dungeon / Wilderness / PvP-Zone
        #    Grundregel: NUR via Duell! AUSNAHME: Ranger-Transport-Raid

        # Konsensbasiertes Duell = immer erlaubt (ausserhalb Safe Zones)
        if is_consented_duel:
            return True, "consented_duel"

        # Ranger-PvP Ausnahme pruefen
        zone_data = self.zones.get(zone_id, {})
        if zone_data.get("ranger_pvp_exception", False):
            if self._is_valid_ranger_raid(target_id, target_ranger_rank):
                return True, "ranger_transport_raid"

        # Kein guelltiger Grund gefunden = KEIN PvP
        return False, "no_pvp_consent"

    def _is_valid_ranger_raid(self, ranger_id: str, ranger_rank: int) -> bool:
        """Ist dieser Ranger ein gueltiges Raid-Ziel?"""
        # Rang muss hoch genug sein
        if ranger_rank < RANGER_PVP_MIN_RANK:
            return False
        # Ranger muss aktiven Transport haben
        if ranger_id not in self._active_ranger_transports:
            return False
        return True

    # -------------------------------------------------------------------
    # DUELL-SYSTEM
    # -------------------------------------------------------------------

    def request_duel(self, challenger_id: str, target_id: str) -> dict:
        """Sendet eine Duell-Anfrage an einen anderen Spieler."""
        duel_key = f"{challenger_id}:{target_id}"
        self._pending_duels[duel_key] = {
            "challenger": challenger_id,
            "target": target_id,
            "timestamp": time.time(),
            "expires_at": time.time() + 30.0  # 30 Sekunden um anzunehmen
        }
        return {
            "status": "duel_requested",
            "challenger": challenger_id,
            "target": target_id,
            "expires_in_seconds": 30
        }

    def accept_duel(self, challenger_id: str, acceptor_id: str) -> dict:
        """Akzeptiert eine Duell-Anfrage -> Kampf kann beginnen."""
        duel_key = f"{challenger_id}:{acceptor_id}"
        duel = self._pending_duels.get(duel_key)

        if not duel:
            return {"status": "error", "reason": "no_pending_duel"}

        if time.time() > duel["expires_at"]:
            del self._pending_duels[duel_key]
            return {"status": "error", "reason": "duel_expired"}

        del self._pending_duels[duel_key]
        return {
            "status": "duel_accepted",
            "challenger": challenger_id,
            "acceptor": acceptor_id,
            "is_consented_duel": True
        }

    def decline_duel(self, challenger_id: str, decliner_id: str) -> dict:
        """Lehnt eine Duell-Anfrage ab."""
        duel_key = f"{challenger_id}:{decliner_id}"
        if duel_key in self._pending_duels:
            del self._pending_duels[duel_key]
        return {"status": "duel_declined", "by": decliner_id}

    def is_duel_consented(self, player1_id: str, player2_id: str) -> bool:
        """Haben beide Spieler einem Duell zugestimmt?"""
        key1 = f"{player1_id}:{player2_id}"
        key2 = f"{player2_id}:{player1_id}"
        # Laufende Duelle werden extern getrackt (vereinfacht)
        return False  # Placeholder - in echtem System: check active_duels Dict

    # -------------------------------------------------------------------
    # RANGER-TRANSPORT SYSTEM
    # -------------------------------------------------------------------

    def start_ranger_transport(self, ranger_id: str, ranger_rank: int, zone_id: str) -> dict:
        """Ranger startet offiziellen Transport -> wird PvP-Ziel fuer Raeuber."""
        if ranger_rank < RANGER_PVP_MIN_RANK:
            return {
                "status": "transport_started",
                "pvp_risk": False,
                "note": f"Rang {ranger_rank} ist geschuetzt (min. Rang {RANGER_PVP_MIN_RANK} fuer Risiko)"
            }

        self._active_ranger_transports[ranger_id] = {
            "rank": ranger_rank,
            "zone_id": zone_id,
            "start_time": time.time()
        }
        return {
            "status": "transport_started",
            "pvp_risk": True,
            "note": f"Rang {ranger_rank} Transport - Ueberfaelle moeglich! Begleiter empfohlen.",
            "ranger_rank": ranger_rank
        }

    def end_ranger_transport(self, ranger_id: str) -> dict:
        """Ranger beendet Transport (sicher angekommen oder Escort-Quest done)."""
        if ranger_id in self._active_ranger_transports:
            del self._active_ranger_transports[ranger_id]
        return {"status": "transport_ended", "ranger_id": ranger_id}

    def report_ranger_raid_sighting(
        self, raider_id: str, witness_ids: list[str]
    ) -> dict:
        """
        Wenn ein Raeuber beim Angriff auf Ranger GESEHEN wird.
        -> Schwerste Straftat im Ruf-System.
        """
        consequences = {
            "raider_id": raider_id,
            "crime": "ranger_transport_raid_witnessed",
            "bounty_added": RANGER_RAID_BOUNTY,
            "reputation_loss": RANGER_RAID_REP_LOSS,
            "city_ban_active": True,
            "npc_hostility_level": "feindlich",
            "wanted_level": "GESUCHT",
            "witnesses": witness_ids,
        }
        return {
            "status": "sighting_reported",
            "consequences": consequences,
            "message": (
                f"Raeuber {raider_id} wurde beim Ranger-Ueberfall gesehen! "
                f"Kopfgeld: {RANGER_RAID_BOUNTY} Gold, "
                f"Ruf: {RANGER_RAID_REP_LOSS}"
            )
        }

    # -------------------------------------------------------------------
    # DISCONNECT-HANDLING
    # -------------------------------------------------------------------

    DISCONNECT_GRACE_PERIOD = 30.0  # Sekunden bis Safe-Logout

    def handle_disconnect(self, player_id: str, zone_id: str) -> dict:
        """
        Spieler disconnectet.
        -> In Safe Zones: sofortiger Safe-Logout
        -> In Gefahren-Zonen: 30 Sek Freeze-Phase, dann Safe-Logout
        """
        if self.is_safe_zone(zone_id):
            return {
                "status": "safe_logout",
                "player_id": player_id,
                "zone_id": zone_id,
                "grace_period": 0,
                "permadeath_risk": False
            }
        else:
            return {
                "status": "disconnect_grace_period",
                "player_id": player_id,
                "zone_id": zone_id,
                "grace_period": self.DISCONNECT_GRACE_PERIOD,
                "permadeath_risk": True,
                "note": (
                    "Gegner eingefroren fuer 30 Sek. "
                    "Nach Ablauf: Safe-Logout, kein Tod, kein Progress-Loss."
                )
            }

    # -------------------------------------------------------------------
    # PERMADEATH-KONSEQUENZEN
    # -------------------------------------------------------------------

    def apply_permadeath(self, player_id: str) -> dict:
        """
        Spieler ist in Permadeath-Zone gestorben.
        Was geht verloren, was bleibt?
        """
        return {
            "player_id": player_id,
            "lost": [
                "character",
                "skills",
                "level",
                "meisterschaft",
                "inventar",
            ],
            "kept": [
                "slime_ki_persoenlichkeit",  # Slime-KI Erinnerungen bleiben!
                "account_achievements",
                "cosmetics",
                "echoharp_lore_progress",    # Story-Fortschritt bleibt
            ],
            "note": (
                "Permadeath ist endgueltig. "
                "Die Slime-KI erinnert sich aber an alles - "
                "der naechste Charakter erbt ihre Geschichte."
            )
        }

    # -------------------------------------------------------------------
    # ZONE-INFO (fuer UI / Minimap)
    # -------------------------------------------------------------------

    def get_zone_ui_info(self, zone_id: str) -> dict:
        """Gibt UI-relevante Zone-Infos zurueck (fuer Minimap-Indikator etc.)."""
        zone = self.zones.get(zone_id)
        zone_type = self.get_zone_type(zone_id)

        if zone_type in (ZoneType.ABSOLUTE_SAFE, ZoneType.SAFE_ZONE):
            indicator = "SICHER"
            color = "green"
        elif zone_type == ZoneType.TRAINING_GROUND:
            indicator = "TRAINING"
            color = "blue"
        elif zone_type == ZoneType.ARENA:
            indicator = "ARENA"
            color = "yellow"
        elif zone_type in (ZoneType.OVERWORLD, ZoneType.WILDERNESS):
            indicator = "GEFAHR"
            color = "orange"
        elif zone_type == ZoneType.DUNGEON:
            indicator = "DUNGEON"
            color = "red"
        else:
            indicator = "PVP"
            color = "red"

        return {
            "zone_id": zone_id,
            "display_name": zone.get("display_name", zone_id) if zone else zone_id,
            "zone_type": zone_type.value,
            "indicator": indicator,
            "indicator_color": color,
            "pvp_risk": zone.get("pvp_allowed", False) if zone else False,
            "permadeath_active": self.is_permadeath_active(zone_id),
            "ranger_pvp_possible": zone.get("ranger_pvp_exception", False) if zone else False,
        }

    def add_zone(self, zone_id: str, zone_data: dict) -> None:
        """
        Neue Zone zur Datenbank hinzufuegen.
        Kann von UE5 / Level-Designer aufgerufen werden wenn neue Orte gebaut werden.
        """
        required_keys = ["display_name", "zone_type", "pvp_allowed", "permadeath_active"]
        for key in required_keys:
            if key not in zone_data:
                raise ValueError(f"Zone-Daten fehlen Key: '{key}'")
        self.zones[zone_id] = zone_data


# ===========================================================================
# GLOBALE INSTANZ (Singleton-Pattern fuer Import)
# ===========================================================================

SAFE_ZONE_SYSTEM = SafeZoneSystem()


# ===========================================================================
# CONVENIENCE-FUNKTIONEN (fuer direkten Import)
# ===========================================================================

def is_safe(zone_id: str) -> bool:
    """Schnellcheck: Ist diese Zone sicher?"""
    return SAFE_ZONE_SYSTEM.is_safe_zone(zone_id)

def pvp_check(
    attacker_id: str,
    target_id: str,
    zone_id: str,
    attacker_ranger_rank: int = 0,
    target_ranger_rank: int = 0,
    is_consented_duel: bool = False
) -> tuple[bool, str]:
    """Schnellcheck: Kann Spieler X Spieler Y in dieser Zone angreifen?"""
    return SAFE_ZONE_SYSTEM.can_attack_player(
        attacker_id, target_id, zone_id,
        attacker_ranger_rank, target_ranger_rank,
        is_consented_duel
    )

def get_zone_info(zone_id: str) -> dict:
    """Zone-Info fuer UI."""
    return SAFE_ZONE_SYSTEM.get_zone_ui_info(zone_id)


# ===========================================================================
# QUICK-TEST
# ===========================================================================

if __name__ == "__main__":
    print("=== NAJIKA SAFE-ZONE SYSTEM TEST ===\n")

    # Test 1: Safe Zone Check
    print("[Test 1] Safe Zone Check:")
    print(f"  Schwarze Muehle sicher? {is_safe('schwarze_muehle')}")       # True
    print(f"  Handelsfestung sicher? {is_safe('handelsfestung')}")         # True
    print(f"  Dampf-Hain sicher? {is_safe('dampf_hain')}")                # True
    print(f"  Heisse Duenen sicher? {is_safe('heisse_duenen')}")           # False (Overworld!)
    print(f"  Goetterfels sicher? {is_safe('goetterfels')}")               # False (Overworld!)

    # Test 2: PvP Check
    print("\n[Test 2] PvP Check:")
    allowed, grund = pvp_check("Spieler_A", "Spieler_B", "schwarze_muehle")
    print(f"  Angriff in Schwarzer Muehle: {allowed} ({grund})")  # False

    allowed, grund = pvp_check("Spieler_A", "Spieler_B", "heisse_duenen")
    print(f"  Angriff in Heisse Duenen (kein Duell): {allowed} ({grund})")  # False

    allowed, grund = pvp_check("Spieler_A", "Spieler_B", "heisse_duenen", is_consented_duel=True)
    print(f"  Duell in Heisse Duenen: {allowed} ({grund})")  # True

    allowed, grund = pvp_check("Raeuber", "Ranger_Hans", "heisse_duenen",
                                target_ranger_rank=30)
    print(f"  Ranger-Raid (ohne aktiven Transport): {allowed} ({grund})")  # False

    # Test 3: Ranger Transport starten
    print("\n[Test 3] Ranger-Transport:")
    result = SAFE_ZONE_SYSTEM.start_ranger_transport("Ranger_Hans", ranger_rank=30, zone_id="heisse_duenen")
    print(f"  Transport gestartet: {result['pvp_risk']} - {result['note']}")

    allowed, grund = pvp_check("Raeuber", "Ranger_Hans", "heisse_duenen",
                                target_ranger_rank=30)
    print(f"  Ranger-Raid (mit aktivem Transport): {allowed} ({grund})")  # True

    # Test 4: Disconnect
    print("\n[Test 4] Disconnect-Handling:")
    result = SAFE_ZONE_SYSTEM.handle_disconnect("Spieler_C", "schwarze_muehle")
    print(f"  Disconnect in Muehle: {result['status']} ({result['permadeath_risk']=})")
    result = SAFE_ZONE_SYSTEM.handle_disconnect("Spieler_C", "gruenschlamm_sumpf")
    print(f"  Disconnect in Gruenschlamm: {result['status']} ({result['grace_period']}s Grace)")

    # Test 5: Zone UI Info
    print("\n[Test 5] Zone UI Info:")
    info = get_zone_info("magmastroeme")
    print(f"  Magmastroeme: [{info['indicator']}] Permadeath={info['permadeath_active']}, PvP={info['pvp_risk']}")
    info = get_zone_info("goetterfels")
    print(f"  Goetterfels: [{info['indicator']}] Permadeath={info['permadeath_active']} (Berg=Overworld!)")
    info = get_zone_info("goetterfels_schmelzwelt")
    print(f"  Schmelzwelt: [{info['indicator']}] Permadeath={info['permadeath_active']} (Inneres=Dungeon)")
    info = get_zone_info("schwarze_muehle")
    print(f"  Schwarze Muehle: [{info['indicator']}] Permadeath={info['permadeath_active']}")
    info = get_zone_info("handelsfestung")
    print(f"  Handelsfestung: [{info['indicator']}] Permadeath={info['permadeath_active']} (Hauptstadt)")

    print("\n=== ALLE TESTS OK ===")
