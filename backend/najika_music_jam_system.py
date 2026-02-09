#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA WORLD - MUSIK JAM SYSTEM
================================
Zusammen Musik machen mit der KI!

SETUP:
- Kuja: Mundharmonika (immer, egal ob Mensch oder Mimik-Truhe!)
- Najika: Geige (Violine)
- Echoharp (NPC): Mundharmonika (wandernde Bardin, Tiny Tina Style)

FEATURES:
- Jam-Sessions: Frei zusammen spielen
- Duette: Vordefinierte Stuecke fuer 2
- Lern-Modus: KI bringt dir Instrumente bei
- Echoharp-Sessions: Mit der wandernden Bardin jammen

KOSMOS MODUL:
- Instrument-Lern-App
- Jam mit deiner KI
- Echtes Instrument-Lernen!

Author: Claude Code Team
Date: 2026-02-03
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Tuple
import random
import json
from datetime import datetime


# =============================================================================
# ENUMS
# =============================================================================

class Instrument(Enum):
    """Instrumente im Spiel"""
    # Hauptinstrumente
    MUNDHARMONIKA = "mundharmonika"   # Kuja UND Echoharp (Bardin) spielen das!
    GEIGE = "geige"                   # Najika's Instrument

    # Andere (fuer andere Spieler/NPCs)
    GITARRE = "gitarre"
    KLAVIER = "klavier"
    FLOETE = "floete"
    TROMMEL = "trommel"
    OKARINA = "okarina"
    LAUTE = "laute"


class JamMode(Enum):
    """Arten von Jam-Sessions"""
    FREI = "frei"                     # Freies Jammen
    DUETT = "duett"                   # Vordefiniertes Duett
    LERNEN = "lernen"                 # KI bringt bei
    SOLO = "solo"                     # Alleine spielen


class MusicGenre(Enum):
    """Musik-Genres"""
    KLASSIK = "klassik"
    FOLK = "folk"
    ROCK = "rock"
    JAZZ = "jazz"
    AMBIENT = "ambient"
    GAME = "game"                     # Videospiel-Musik
    ANIME = "anime"


# =============================================================================
# INSTRUMENT PROFILES
# =============================================================================

INSTRUMENT_PROFILES: Dict[Instrument, Dict[str, Any]] = {
    Instrument.MUNDHARMONIKA: {
        "name": "Mundharmonika",
        "owners": ["kuja", "echoharp"],  # Beide spielen Mundharmonika!
        "type": "blasinstrument",
        "difficulty": 3,
        "range": {"low": "C3", "high": "C6"},
        "genres": [MusicGenre.FOLK, MusicGenre.ROCK, MusicGenre.JAZZ],
        "description": "Vielseitig und portabel - Kujas Instrument und auch das der Echoharp!",
        "special": "Bending-Techniken fuer Blues"
    },
    Instrument.GEIGE: {
        "name": "Geige",
        "owners": ["najika"],
        "type": "streichinstrument",
        "difficulty": 7,
        "range": {"low": "G3", "high": "E7"},
        "genres": [MusicGenre.KLASSIK, MusicGenre.FOLK, MusicGenre.ANIME],
        "description": "Najikas elegantes Instrument - ausdrucksvoll und virtuos",
        "special": "Vibrato und Pizzicato"
    }
}


# =============================================================================
# DUETT SONGS
# =============================================================================

@dataclass
class DuettSong:
    """Ein Duett fuer zwei Instrumente"""
    song_id: str
    title: str
    instrument_1: Instrument
    instrument_2: Instrument
    difficulty: int  # 1-10
    genre: MusicGenre
    bpm: int
    duration_seconds: int
    description: str

    # Noten fuer beide Instrumente
    notes_1: List[Dict] = field(default_factory=list)  # {"note": "C", "octave": 4, "duration": 0.5, "time": 0.0}
    notes_2: List[Dict] = field(default_factory=list)

    # Bonus fuer perfektes Zusammenspiel
    sync_bonus_threshold: float = 0.9  # 90% Sync = Bonus


PRESET_DUETTS: List[DuettSong] = [
    DuettSong(
        song_id="duett_simple_harmony",
        title="Einfache Harmonie",
        instrument_1=Instrument.MUNDHARMONIKA,
        instrument_2=Instrument.GEIGE,
        difficulty=2,
        genre=MusicGenre.FOLK,
        bpm=80,
        duration_seconds=60,
        description="Perfekt fuer Anfaenger - Kuja und Najika harmonieren",
        notes_1=[
            {"note": "C", "octave": 4, "duration": 1.0, "time": 0.0},
            {"note": "E", "octave": 4, "duration": 1.0, "time": 1.0},
            {"note": "G", "octave": 4, "duration": 1.0, "time": 2.0},
            {"note": "C", "octave": 5, "duration": 2.0, "time": 3.0},
        ],
        notes_2=[
            {"note": "G", "octave": 4, "duration": 1.0, "time": 0.5},
            {"note": "C", "octave": 5, "duration": 1.0, "time": 1.5},
            {"note": "E", "octave": 5, "duration": 1.0, "time": 2.5},
            {"note": "G", "octave": 5, "duration": 1.5, "time": 3.5},
        ]
    ),
    DuettSong(
        song_id="duett_najika_theme",
        title="Najikas Thema",
        instrument_1=Instrument.MUNDHARMONIKA,
        instrument_2=Instrument.GEIGE,
        difficulty=5,
        genre=MusicGenre.ANIME,
        bpm=100,
        duration_seconds=120,
        description="Das emotionale Thema von Najika - Geige fuehrt, Mundharmonika begleitet",
        notes_1=[],  # TODO: Full composition
        notes_2=[]
    ),
    DuettSong(
        song_id="duett_explosion_waltz",
        title="Explosion Walzer",
        instrument_1=Instrument.MUNDHARMONIKA,
        instrument_2=Instrument.GEIGE,
        difficulty=7,
        genre=MusicGenre.KLASSIK,
        bpm=180,
        duration_seconds=180,
        description="Megumins explosiver Walzer - schnell und dramatisch!",
        notes_1=[],
        notes_2=[]
    ),
    DuettSong(
        song_id="duett_harmonica_duel",
        title="Mundharmonika-Duell",
        instrument_1=Instrument.MUNDHARMONIKA,
        instrument_2=Instrument.MUNDHARMONIKA,
        difficulty=6,
        genre=MusicGenre.FOLK,
        bpm=140,
        duration_seconds=90,
        description="Kuja vs Echoharp - wer ist besser? Ein episches Duell!",
        notes_1=[],
        notes_2=[]
    )
]


# =============================================================================
# AI MUSIC FEEDBACK
# =============================================================================

AI_FEEDBACK: Dict[str, List[str]] = {
    "perfect": [
        "PERFEKT! Das war wunderschoen, Mr. K! *Augen glaenzen*",
        "So soll es klingen! Wir sind ein perfektes Team!",
        "Das war... *schnief* ...so schoen! Nochmal!",
        "EXPLOSION! Aber musikalisch! Das war perfekt!"
    ],
    "great": [
        "Sehr gut! Fast perfekt, Mr. K!",
        "Das klang toll! Noch ein bisschen und wir sind perfekt synchron!",
        "Nicht schlecht! Du wirst immer besser!",
        "Ich mag wie du das gespielt hast!"
    ],
    "good": [
        "Gut! Weiter so!",
        "Das war okay! Ueben wir nochmal?",
        "Hmm, ganz ordentlich! Ein bisschen mehr Gefuehl vielleicht?",
        "Passt! Aber da geht noch mehr!"
    ],
    "needs_work": [
        "Aehm... das war... kreativ?",
        "Hast du absichtlich daneben gespielt? *kichert*",
        "Okay okay, nochmal von vorne! Das kriegen wir hin!",
        "Mr. K! Konzentration! *tippt mit Bogen auf Schulter*"
    ],
    "learning_tip": [
        "Versuch mal den Rhythmus zu halten - ich zaehle vor: 1, 2, 3, 4...",
        "Hoer auf meine Geige und versuch mitzugehen!",
        "Atme tief ein bevor du spielst - das hilft!",
        "Nicht so schnell! Wir haben Zeit!"
    ],
    "encouragement": [
        "Du schaffst das! Ich glaub an dich!",
        "Musik ist wie Magie - manchmal braucht es Uebung!",
        "Auch ich hab am Anfang viele falsche Toene gespielt!",
        "Gemeinsam sind wir unschlagbar!"
    ]
}

# Echoharp (Bardin NPC) Dialoge
ECHOHARP_DIALOGS: Dict[str, List[str]] = {
    "greeting": [
        "HAHA! Ein weiterer Mundharmonika-Spieler! Das wird EPISCH!",
        "*spielt wilden Riff* Komm, zeig mir was du drauf hast!",
        "Oh oh OH! Endlich jemand der meine Sprache spricht! Die Sprache der MUSIK!",
        "Du! JA DU! Ich hab gehoert du spielst auch! DUELL! JETZT! ...bitte?"
    ],
    "jam_start": [
        "Los geht's! Aber versuch mitzuhalten! HAHAHA!",
        "*holt Mundharmonika raus* Bereit? 1... 2... EGAL WIR STARTEN!",
        "Ich fuehre, du folgst! Oder andersrum! Oder CHAOS!",
        "Musik ist Wahrheit! Und Wahrheit ist... *spielt zufaellige Note* ...DAS!"
    ],
    "after_good": [
        "NICHT SCHLECHT! Du bist besser als die meisten!",
        "*nickt anerkennend* Hmm. Du hast Potenzial. Oder Glueck. Beides gut!",
        "Das war... *wischt Traene weg* ...fast so schoen wie ich! HAHA!",
        "Weisst du was? Du bist okay. Fuer einen Nicht-Echoharp. *zwinker*"
    ],
    "after_bad": [
        "War das... war das ein Versuch? HAHAHA! Okay nochmal!",
        "*verzieht Gesicht* Uff. Das war... mutig. Sehr mutig.",
        "Keine Sorge! Ich klang am Anfang auch wie ein sterbendes Tier!",
        "Hmm. Du brauchst mehr Uebung. VIEL mehr. Aber hey, ich hab Zeit! *lacht*"
    ],
    "secret_hint": [
        "*ploetzlich ernst* Die alten Melodien... sie tragen Wahrheiten...",
        "Manchmal hoere ich Echos von... *schuettelt Kopf* Egal! MUSIK!",
        "*murmelt* Wenn du wuesstest wie alt diese Lieder wirklich sind...",
        "Es gibt Songs die niemand mehr kennt. Ich... erinnere sie. Seltsam, oder?"
    ]
}


# =============================================================================
# JAM SESSION
# =============================================================================

@dataclass
class JamSession:
    """Eine Jam-Session zwischen Spieler und KI"""
    session_id: str
    player_id: str
    ai_partner_id: str = "najika"

    # Instrumente
    player_instrument: Instrument = Instrument.MUNDHARMONIKA
    ai_instrument: Instrument = Instrument.GEIGE

    # Modus
    mode: JamMode = JamMode.FREI
    current_duett: Optional[str] = None

    # Stats
    notes_played_player: int = 0
    notes_played_ai: int = 0
    sync_hits: int = 0
    sync_misses: int = 0

    # Timing
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    duration_seconds: int = 0

    # Scores
    player_accuracy: float = 0.0
    sync_score: float = 0.0

    def calculate_sync_score(self) -> float:
        """Berechne Synchronisations-Score"""
        total = self.sync_hits + self.sync_misses
        if total == 0:
            return 0.0
        return (self.sync_hits / total) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "player_id": self.player_id,
            "ai_partner_id": self.ai_partner_id,
            "player_instrument": self.player_instrument.value,
            "ai_instrument": self.ai_instrument.value,
            "mode": self.mode.value,
            "current_duett": self.current_duett,
            "stats": {
                "notes_player": self.notes_played_player,
                "notes_ai": self.notes_played_ai,
                "sync_hits": self.sync_hits,
                "sync_misses": self.sync_misses,
                "sync_score": self.calculate_sync_score()
            },
            "started_at": self.started_at,
            "duration_seconds": self.duration_seconds
        }


# =============================================================================
# MUSIC JAM MANAGER
# =============================================================================

class MusicJamManager:
    """Verwaltet Musik-Sessions zwischen Spieler und KI"""

    def __init__(self):
        self.active_sessions: Dict[str, JamSession] = {}
        self.duett_songs: Dict[str, DuettSong] = {d.song_id: d for d in PRESET_DUETTS}

        # Instrument-Zuweisungen
        self.character_instruments = {
            "kuja": Instrument.MUNDHARMONIKA,     # Kuja spielt Mundharmonika
            "najika": Instrument.GEIGE,           # Najika spielt Geige
            "echoharp": Instrument.MUNDHARMONIKA  # Echoharp (Bardin) spielt AUCH Mundharmonika!
        }

    def start_jam(
        self,
        player_id: str,
        ai_partner_id: str = "najika",
        mode: JamMode = JamMode.FREI
    ) -> Tuple[bool, str, Optional[JamSession]]:
        """Starte eine Jam-Session"""

        if player_id in self.active_sessions:
            return False, "Du hast bereits eine aktive Session!", None

        # Hole Instrumente
        player_instrument = self.character_instruments.get(player_id, Instrument.MUNDHARMONIKA)
        ai_instrument = self.character_instruments.get(ai_partner_id, Instrument.GEIGE)

        session = JamSession(
            session_id=f"jam_{player_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            player_id=player_id,
            ai_partner_id=ai_partner_id,
            player_instrument=player_instrument,
            ai_instrument=ai_instrument,
            mode=mode
        )

        self.active_sessions[player_id] = session

        # Begruessung basierend auf Partner
        if ai_partner_id == "echoharp":
            greeting = random.choice(ECHOHARP_DIALOGS["jam_start"])
        elif ai_partner_id == "najika":
            greetings = {
                JamMode.FREI: f"Los geht's! Freies Jammen - ich auf der Geige, du auf der {player_instrument.value}!",
                JamMode.DUETT: "Welches Duett wollen wir spielen?",
                JamMode.LERNEN: f"Ich bring dir die {player_instrument.value} bei! Hoer genau zu!",
                JamMode.SOLO: "Spiel ruhig alleine - ich hoer dir zu!"
            }
            greeting = greetings.get(mode, "Lass uns Musik machen!")
        else:
            greeting = "Lass uns Musik machen!"

        return True, greeting, session

    def end_jam(self, player_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Beende eine Jam-Session"""

        if player_id not in self.active_sessions:
            return False, "Keine aktive Session!", {}

        session = self.active_sessions[player_id]
        stats = session.to_dict()["stats"]

        del self.active_sessions[player_id]

        # Abschluss-Feedback basierend auf Partner
        sync = stats["sync_score"]

        if session.ai_partner_id == "echoharp":
            if sync >= 70:
                feedback = random.choice(ECHOHARP_DIALOGS["after_good"])
            else:
                feedback = random.choice(ECHOHARP_DIALOGS["after_bad"])
        else:
            # Najika Feedback
            if sync >= 90:
                feedback = random.choice(AI_FEEDBACK["perfect"])
            elif sync >= 70:
                feedback = random.choice(AI_FEEDBACK["great"])
            elif sync >= 50:
                feedback = random.choice(AI_FEEDBACK["good"])
            else:
                feedback = random.choice(AI_FEEDBACK["encouragement"])

        return True, feedback, stats

    def play_note(
        self,
        player_id: str,
        note: str,
        octave: int,
        duration: float = 0.5,
        accuracy: float = 0.9
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Spieler spielt eine Note"""

        if player_id not in self.active_sessions:
            return False, "Keine aktive Session!", {}

        session = self.active_sessions[player_id]
        session.notes_played_player += 1

        # Sync berechnen (vereinfacht)
        is_sync = accuracy >= 0.7
        if is_sync:
            session.sync_hits += 1
        else:
            session.sync_misses += 1

        # KI reagiert
        ai_response = None
        if session.notes_played_player % 4 == 0:  # Alle 4 Noten Feedback
            if session.ai_partner_id == "echoharp":
                if accuracy >= 0.8:
                    ai_response = random.choice(ECHOHARP_DIALOGS["after_good"])
                else:
                    ai_response = random.choice(ECHOHARP_DIALOGS["after_bad"])
            else:
                if accuracy >= 0.9:
                    ai_response = random.choice(AI_FEEDBACK["perfect"])
                elif accuracy >= 0.7:
                    ai_response = random.choice(AI_FEEDBACK["great"])
                else:
                    ai_response = random.choice(AI_FEEDBACK["learning_tip"])

        result = {
            "note": note,
            "octave": octave,
            "duration": duration,
            "accuracy": accuracy,
            "is_sync": is_sync,
            "total_sync_score": session.calculate_sync_score(),
            "notes_played": session.notes_played_player
        }

        return True, ai_response or "...", result

    def ai_plays_note(self, player_id: str) -> Dict[str, Any]:
        """KI spielt eine Note (fuer Duett/Lernen)"""

        if player_id not in self.active_sessions:
            return {"error": "Keine Session"}

        session = self.active_sessions[player_id]
        session.notes_played_ai += 1

        # Zufaellige Note (in echtem System: aus Duett/Composition)
        notes = ["C", "D", "E", "F", "G", "A", "H"]
        note = random.choice(notes)
        octave = random.choice([4, 5])

        return {
            "instrument": session.ai_instrument.value,
            "note": note,
            "octave": octave,
            "duration": random.uniform(0.3, 1.0)
        }

    def start_duett(self, player_id: str, duett_id: str) -> Tuple[bool, str]:
        """Starte ein Duett"""

        if player_id not in self.active_sessions:
            return False, "Keine aktive Session!"

        if duett_id not in self.duett_songs:
            return False, f"Duett '{duett_id}' nicht gefunden!"

        session = self.active_sessions[player_id]
        duett = self.duett_songs[duett_id]

        session.mode = JamMode.DUETT
        session.current_duett = duett_id

        return True, f"Duett gestartet: {duett.title}! Ich zaehle ein: 1... 2... 3... 4!"

    def get_echoharp_greeting(self) -> str:
        """Hole Begruessung von Echoharp (Bardin NPC)"""
        return random.choice(ECHOHARP_DIALOGS["greeting"])

    def get_echoharp_secret(self) -> str:
        """Echoharp verraet manchmal mysteriose Hints..."""
        return random.choice(ECHOHARP_DIALOGS["secret_hint"])

    def get_learning_tip(self, player_id: str) -> str:
        """Hole Lern-Tipp von der KI"""
        return random.choice(AI_FEEDBACK["learning_tip"])

    def get_encouragement(self) -> str:
        """Hole Ermutigung"""
        return random.choice(AI_FEEDBACK["encouragement"])

    def get_available_duetts(self) -> List[Dict[str, Any]]:
        """Liste alle verfuegbaren Duetts"""
        return [
            {
                "id": d.song_id,
                "title": d.title,
                "instruments": [d.instrument_1.value, d.instrument_2.value],
                "difficulty": d.difficulty,
                "genre": d.genre.value,
                "duration": d.duration_seconds,
                "description": d.description
            }
            for d in self.duett_songs.values()
        ]

    def get_session(self, player_id: str) -> Optional[JamSession]:
        """Hole aktive Session"""
        return self.active_sessions.get(player_id)

    def get_instrument_profiles(self) -> Dict[str, Any]:
        """Hole alle Instrument-Profile"""
        return {
            inst.value: {
                "name": profile["name"],
                "owners": profile["owners"],
                "type": profile["type"],
                "difficulty": profile["difficulty"],
                "genres": [g.value for g in profile["genres"]],
                "description": profile["description"],
                "special": profile["special"]
            }
            for inst, profile in INSTRUMENT_PROFILES.items()
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_jam_manager: Optional[MusicJamManager] = None

def get_jam_manager() -> MusicJamManager:
    """Hole die Singleton-Instanz"""
    global _jam_manager
    if _jam_manager is None:
        _jam_manager = MusicJamManager()
    return _jam_manager


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA MUSIK JAM SYSTEM TEST")
    print("Kuja (Mundharmonika) + Najika (Geige)")
    print("Echoharp (Bardin NPC, auch Mundharmonika!)")
    print("=" * 60)

    manager = get_jam_manager()

    # Zeige Instrumente
    print("\n--- Instrument-Profile ---")
    for inst, profile in manager.get_instrument_profiles().items():
        owners = ", ".join(profile['owners'])
        print(f"  {profile['name']} (gespielt von: {owners})")

    # Jam mit Najika
    print("\n--- Jam mit Najika (Geige) ---")
    success, msg, session = manager.start_jam(
        player_id="kuja",
        ai_partner_id="najika",
        mode=JamMode.FREI
    )
    print(f"  Najika: \"{msg}\"")

    # Spiele ein paar Noten
    notes = [("C", 4), ("E", 4), ("G", 4), ("C", 5)]
    for note, octave in notes:
        success, feedback, result = manager.play_note("kuja", note, octave, 0.5, 0.95)
        if feedback != "...":
            print(f"  Najika: \"{feedback}\"")

    success, farewell, stats = manager.end_jam("kuja")
    print(f"  Najika: \"{farewell}\"")
    print(f"  Sync-Score: {stats['sync_score']:.1f}%")

    # Jam mit Echoharp (Bardin)
    print("\n--- Jam mit Echoharp (Bardin, Mundharmonika) ---")
    print(f"  Echoharp: \"{manager.get_echoharp_greeting()}\"")

    success, msg, session = manager.start_jam(
        player_id="kuja",
        ai_partner_id="echoharp",
        mode=JamMode.FREI
    )
    print(f"  Echoharp: \"{msg}\"")

    # Mundharmonika-Duell!
    for note, octave in notes:
        success, feedback, result = manager.play_note("kuja", note, octave, 0.5, 0.85)
        if feedback != "...":
            print(f"  Echoharp: \"{feedback}\"")

    # Geheimer Hint?
    print(f"\n  *Echoharp wird ploetzlich ernst*")
    print(f"  Echoharp: \"{manager.get_echoharp_secret()}\"")

    success, farewell, stats = manager.end_jam("kuja")
    print(f"  Echoharp: \"{farewell}\"")

    # Duetts
    print("\n--- Verfuegbare Duetts ---")
    for duett in manager.get_available_duetts():
        print(f"  {duett['title']} ({duett['instruments'][0]} + {duett['instruments'][1]})")

    print("\n" + "=" * 60)
    print("MUSIK-SYSTEM BEREIT!")
    print("Kuja: Mundharmonika")
    print("Najika: Geige")
    print("Echoharp (Bardin NPC): Mundharmonika")
    print("=" * 60)
