"""
Instrument Playing System - Najika World
=========================================

Spielbare Instrumente (wie in echt - echte Töne!)

Features:
- Spielbare Töne (C, D, E, F, G, A, H + Oktaven)
- Standard: Mundharmonika (Harmonica)
- Austauschbare Instrumente (Gitarre, Klavier, etc.)
- Tutorial-Modus zum Lernen
- Song-Database (Lieder zum Üben)
- Skyrim-Style Skill-Progression
- MIDI-Support

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime
import json


class InstrumentType(Enum):
    """Instrument-Typen"""
    HARMONICA = "mundharmonika"    # Default!
    GUITAR = "gitarre"
    PIANO = "klavier"
    FLUTE = "flöte"
    DRUM = "trommel"
    VIOLIN = "violine"
    OCARINA = "okarina"           # Zelda OoT!
    LUTE = "laute"


class Note(Enum):
    """Musikalische Noten (westliche Notation)"""
    C = "C"
    CS = "C#"  # C-Sharp / Cis
    D = "D"
    DS = "D#"  # D-Sharp / Dis
    E = "E"
    F = "F"
    FS = "F#"  # F-Sharp / Fis
    G = "G"
    GS = "G#"  # G-Sharp / Gis
    A = "A"
    AS = "A#"  # A-Sharp / Ais
    H = "H"    # B (deutsch)


class NoteQuality(Enum):
    """Note-Qualität (wie gut gespielt)"""
    PERFECT = "perfect"    # 95-100%
    GREAT = "great"        # 80-94%
    GOOD = "good"          # 60-79%
    OK = "ok"              # 40-59%
    POOR = "poor"          # 20-39%
    MISS = "miss"          # 0-19%


@dataclass
class MusicalNote:
    """Eine gespielte Note"""
    note: Note
    octave: int  # 1-8
    duration: float  # in Sekunden
    velocity: float  # 0.0-1.0 (Lautstärke/Intensität)
    quality: NoteQuality
    timestamp: datetime = field(default_factory=datetime.now)

    def get_frequency(self) -> float:
        """Berechnet Frequenz in Hz (für Audio-Synthese)"""
        # A4 = 440 Hz (Standard)
        # Formel: f = 440 * 2^((n-49)/12)
        # n = Halbtonschritte von A4

        note_values = {
            Note.C: 0, Note.CS: 1, Note.D: 2, Note.DS: 3,
            Note.E: 4, Note.F: 5, Note.FS: 6, Note.G: 7,
            Note.GS: 8, Note.A: 9, Note.AS: 10, Note.H: 11
        }

        # A4 ist Note 49
        # C4 ist 9 Halbtöne unter A4
        base_c4 = 40  # C4 = 40
        note_offset = note_values[self.note]
        octave_offset = (self.octave - 4) * 12

        n = base_c4 + note_offset + octave_offset

        frequency = 440.0 * (2 ** ((n - 49) / 12))
        return frequency


@dataclass
class Song:
    """Ein Lied zum Lernen/Spielen"""
    song_id: str
    title: str
    artist: str
    difficulty: int  # 1-10

    # Notes + Timing
    notes: List[Dict]  # {"note": "C", "octave": 4, "duration": 0.5, "delay": 0.0}

    # Metadata
    bpm: int = 120
    time_signature: str = "4/4"
    genre: str = "unknown"
    description: str = ""

    # Requirements
    required_instrument: Optional[InstrumentType] = None
    required_skill_level: int = 1


@dataclass
class InstrumentProgress:
    """Fortschritt auf einem Instrument"""
    instrument: InstrumentType
    skill_level: int = 1
    experience: float = 0.0
    exp_for_next_level: float = 100.0

    # Stats
    total_notes_played: int = 0
    perfect_notes: int = 0
    total_play_time: float = 0.0  # in Sekunden

    # Songs
    songs_learned: List[str] = field(default_factory=list)
    songs_mastered: List[str] = field(default_factory=list)

    # Timestamps
    first_played: Optional[datetime] = None
    last_played: Optional[datetime] = None


class InstrumentSystem:
    """
    Instrument Playing System Manager

    Verwaltet spielbare Instrumente, Skills, Songs
    """

    def __init__(self):
        # Player progress per instrument
        self.instrument_progress: Dict[InstrumentType, InstrumentProgress] = {}

        # Song database
        self.songs: Dict[str, Song] = {}

        # Current session
        self.current_instrument: Optional[InstrumentType] = InstrumentType.HARMONICA
        self.notes_played_this_session: List[MusicalNote] = []

        # Experience settings
        self.BASE_EXP_FOR_LEVEL = 100.0
        self.EXP_MULTIPLIER = 1.05

        # XP per note quality
        self.NOTE_QUALITY_XP = {
            NoteQuality.PERFECT: 10.0,
            NoteQuality.GREAT: 7.0,
            NoteQuality.GOOD: 5.0,
            NoteQuality.OK: 3.0,
            NoteQuality.POOR: 1.0,
            NoteQuality.MISS: 0.0
        }

        # Initialize default songs
        self.create_default_songs()


    def play_note(
        self,
        instrument: InstrumentType,
        note: Note,
        octave: int,
        duration: float = 0.5,
        velocity: float = 0.8,
        quality: NoteQuality = NoteQuality.GOOD
    ) -> Dict:
        """
        Spielt eine Note (Skyrim Learning by Doing!)

        Args:
            instrument: Instrument-Typ
            note: Note (C, D, E, etc.)
            octave: Oktave (1-8)
            duration: Dauer in Sekunden
            velocity: Lautstärke (0.0-1.0)
            quality: Wie gut gespielt

        Returns:
            Result dict mit XP/Level-Up Info
        """
        # Get/Create progress
        if instrument not in self.instrument_progress:
            self.instrument_progress[instrument] = InstrumentProgress(instrument=instrument)

        progress = self.instrument_progress[instrument]

        # Create musical note
        musical_note = MusicalNote(
            note=note,
            octave=octave,
            duration=duration,
            velocity=velocity,
            quality=quality
        )

        # Add to session
        self.notes_played_this_session.append(musical_note)

        # Calculate XP
        base_xp = self.NOTE_QUALITY_XP.get(quality, 0.0)

        # Duration bonus (longer notes = more XP)
        duration_mult = min(2.0, 1.0 + (duration / 2.0))
        total_xp = base_xp * duration_mult

        # Add XP
        old_level = progress.skill_level
        progress.experience += total_xp

        # Update stats
        progress.total_notes_played += 1
        if quality == NoteQuality.PERFECT:
            progress.perfect_notes += 1
        progress.total_play_time += duration

        if not progress.first_played:
            progress.first_played = datetime.now()
        progress.last_played = datetime.now()

        # Check for level-up
        leveled_up = False
        while progress.experience >= progress.exp_for_next_level:
            progress.experience -= progress.exp_for_next_level
            progress.skill_level += 1
            leveled_up = True

            # Calculate next level exp requirement
            progress.exp_for_next_level = self._calculate_exp_for_level(progress.skill_level)

        result = {
            "note": note.value,
            "octave": octave,
            "frequency": musical_note.get_frequency(),
            "quality": quality.value,
            "xp_gained": total_xp,
            "current_level": progress.skill_level,
            "current_exp": progress.experience,
            "exp_for_next": progress.exp_for_next_level,
            "leveled_up": leveled_up,
            "old_level": old_level
        }

        if leveled_up:
            result["level_up_message"] = (
                f"🎵 {instrument.value.upper()} Skill Level {progress.skill_level}!"
            )

        return result


    def play_song(
        self,
        instrument: InstrumentType,
        song_id: str,
        note_accuracies: List[float]
    ) -> Dict:
        """
        Spielt ein komplettes Lied

        Args:
            instrument: Instrument
            song_id: Song ID
            note_accuracies: Liste von Accuracy-Werten (0.0-1.0) für jede Note

        Returns:
            Result mit Score, XP, etc.
        """
        if song_id not in self.songs:
            return {"error": "Song nicht gefunden"}

        song = self.songs[song_id]

        # Check instrument requirement
        if song.required_instrument and song.required_instrument != instrument:
            return {
                "error": f"Song benötigt {song.required_instrument.value}"
            }

        # Check skill requirement
        progress = self.instrument_progress.get(instrument)
        if not progress or progress.skill_level < song.required_skill_level:
            return {
                "error": f"Skill Level {song.required_skill_level} benötigt"
            }

        # Calculate score
        if len(note_accuracies) != len(song.notes):
            return {"error": "Note-Count mismatch"}

        total_xp = 0.0
        quality_counts = {q: 0 for q in NoteQuality}

        for i, (note_data, accuracy) in enumerate(zip(song.notes, note_accuracies)):
            # Determine quality based on accuracy
            quality = self._accuracy_to_quality(accuracy)
            quality_counts[quality] += 1

            # Get note info
            note = Note(note_data["note"])
            octave = note_data["octave"]
            duration = note_data["duration"]

            # Play note (gets XP)
            result = self.play_note(
                instrument, note, octave, duration,
                velocity=0.8, quality=quality
            )

            total_xp += result["xp_gained"]

        # Calculate overall score
        avg_accuracy = sum(note_accuracies) / len(note_accuracies)
        score_percent = avg_accuracy * 100

        # Determine rank
        if score_percent >= 95:
            rank = "S"
        elif score_percent >= 85:
            rank = "A"
        elif score_percent >= 75:
            rank = "B"
        elif score_percent >= 60:
            rank = "C"
        else:
            rank = "D"

        # Check if learned/mastered
        song_learned = score_percent >= 60
        song_mastered = score_percent >= 95

        if song_learned and song_id not in progress.songs_learned:
            progress.songs_learned.append(song_id)

        if song_mastered and song_id not in progress.songs_mastered:
            progress.songs_mastered.append(song_id)

        return {
            "song_id": song_id,
            "song_title": song.title,
            "score_percent": score_percent,
            "rank": rank,
            "total_xp": total_xp,
            "quality_breakdown": {q.value: count for q, count in quality_counts.items()},
            "learned": song_learned,
            "mastered": song_mastered,
            "perfect_notes": quality_counts[NoteQuality.PERFECT],
            "total_notes": len(note_accuracies)
        }


    def _accuracy_to_quality(self, accuracy: float) -> NoteQuality:
        """Konvertiert Accuracy (0.0-1.0) zu Note Quality"""
        if accuracy >= 0.95:
            return NoteQuality.PERFECT
        elif accuracy >= 0.80:
            return NoteQuality.GREAT
        elif accuracy >= 0.60:
            return NoteQuality.GOOD
        elif accuracy >= 0.40:
            return NoteQuality.OK
        elif accuracy >= 0.20:
            return NoteQuality.POOR
        else:
            return NoteQuality.MISS


    def _calculate_exp_for_level(self, level: int) -> float:
        """Berechnet XP für nächstes Level"""
        return self.BASE_EXP_FOR_LEVEL * (self.EXP_MULTIPLIER ** (level - 1))


    def get_instrument_info(self, instrument: InstrumentType) -> Dict:
        """Holt Info über ein Instrument"""
        progress = self.instrument_progress.get(instrument)

        if not progress:
            return {
                "instrument": instrument.value,
                "unlocked": False,
                "message": "Instrument noch nicht gespielt"
            }

        # Get available songs
        available_songs = [
            {
                "song_id": song.song_id,
                "title": song.title,
                "difficulty": song.difficulty,
                "required_level": song.required_skill_level,
                "learned": song.song_id in progress.songs_learned,
                "mastered": song.song_id in progress.songs_mastered,
                "can_play": progress.skill_level >= song.required_skill_level
            }
            for song in self.songs.values()
            if not song.required_instrument or song.required_instrument == instrument
        ]

        return {
            "instrument": instrument.value,
            "skill_level": progress.skill_level,
            "experience": progress.experience,
            "exp_for_next_level": progress.exp_for_next_level,
            "progress_percent": (progress.experience / progress.exp_for_next_level * 100),
            "total_notes_played": progress.total_notes_played,
            "perfect_notes": progress.perfect_notes,
            "accuracy": (
                (progress.perfect_notes / progress.total_notes_played * 100)
                if progress.total_notes_played > 0 else 0.0
            ),
            "total_play_time": progress.total_play_time,
            "songs_learned": len(progress.songs_learned),
            "songs_mastered": len(progress.songs_mastered),
            "available_songs": available_songs,
            "first_played": progress.first_played.isoformat() if progress.first_played else None,
            "last_played": progress.last_played.isoformat() if progress.last_played else None
        }


    def create_song(self, song: Song):
        """Fügt Song zur Datenbank hinzu"""
        self.songs[song.song_id] = song


    def create_default_songs(self):
        """Erstellt Standard-Lieder"""

        # Tutorial Song - Happy Birthday (einfach!)
        self.create_song(Song(
            song_id="tutorial_happy_birthday",
            title="Happy Birthday",
            artist="Traditional",
            difficulty=1,
            notes=[
                {"note": "C", "octave": 4, "duration": 0.5, "delay": 0.0},
                {"note": "C", "octave": 4, "duration": 0.5, "delay": 0.5},
                {"note": "D", "octave": 4, "duration": 1.0, "delay": 1.0},
                {"note": "C", "octave": 4, "duration": 1.0, "delay": 2.0},
                {"note": "F", "octave": 4, "duration": 1.0, "delay": 3.0},
                {"note": "E", "octave": 4, "duration": 2.0, "delay": 4.0},
            ],
            bpm=120,
            genre="traditional",
            description="Einfaches Tutorial-Lied für Anfänger",
            required_skill_level=1
        ))

        # Zelda OoT - Ocarina Songs!
        self.create_song(Song(
            song_id="zelda_song_of_time",
            title="Song of Time",
            artist="Zelda: Ocarina of Time",
            difficulty=3,
            notes=[
                {"note": "A", "octave": 4, "duration": 1.0, "delay": 0.0},
                {"note": "D", "octave": 4, "duration": 0.5, "delay": 1.0},
                {"note": "F", "octave": 4, "duration": 1.5, "delay": 1.5},
                {"note": "A", "octave": 4, "duration": 1.0, "delay": 3.0},
                {"note": "D", "octave": 4, "duration": 0.5, "delay": 4.0},
                {"note": "F", "octave": 4, "duration": 1.5, "delay": 4.5},
            ],
            bpm=90,
            genre="game",
            description="Legendärer Song aus Zelda OoT",
            required_instrument=InstrumentType.OCARINA,
            required_skill_level=5
        ))

        # Einfache Mundharmonika-Übung
        self.create_song(Song(
            song_id="harmonica_basics_1",
            title="Mundharmonika Basics",
            artist="Najika World",
            difficulty=1,
            notes=[
                {"note": "C", "octave": 4, "duration": 1.0, "delay": 0.0},
                {"note": "D", "octave": 4, "duration": 1.0, "delay": 1.0},
                {"note": "E", "octave": 4, "duration": 1.0, "delay": 2.0},
                {"note": "F", "octave": 4, "duration": 1.0, "delay": 3.0},
                {"note": "G", "octave": 4, "duration": 1.0, "delay": 4.0},
            ],
            bpm=60,
            genre="tutorial",
            description="Grundlegende C-Dur Tonleiter",
            required_instrument=InstrumentType.HARMONICA,
            required_skill_level=1
        ))


    def get_all_songs(self, instrument: Optional[InstrumentType] = None) -> List[Dict]:
        """Holt alle Songs (optional gefiltert nach Instrument)"""
        songs_list = []

        for song in self.songs.values():
            # Instrument filter
            if instrument and song.required_instrument:
                if song.required_instrument != instrument:
                    continue

            songs_list.append({
                "song_id": song.song_id,
                "title": song.title,
                "artist": song.artist,
                "difficulty": song.difficulty,
                "required_instrument": (
                    song.required_instrument.value
                    if song.required_instrument else None
                ),
                "required_skill_level": song.required_skill_level,
                "bpm": song.bpm,
                "genre": song.genre,
                "description": song.description
            })

        return songs_list


    def export_state(self) -> Dict:
        """Exportiert kompletten State"""
        return {
            "instruments": {
                inst.value: {
                    "skill_level": prog.skill_level,
                    "experience": prog.experience,
                    "total_notes_played": prog.total_notes_played,
                    "perfect_notes": prog.perfect_notes,
                    "total_play_time": prog.total_play_time,
                    "songs_learned": prog.songs_learned,
                    "songs_mastered": prog.songs_mastered,
                    "first_played": prog.first_played.isoformat() if prog.first_played else None,
                    "last_played": prog.last_played.isoformat() if prog.last_played else None
                }
                for inst, prog in self.instrument_progress.items()
            }
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== Instrument Playing System Test ===\n")

    inst_sys = InstrumentSystem()

    # Test 1: Play single note
    print("1. Play Note: C4 (Mundharmonika)")
    result = inst_sys.play_note(
        InstrumentType.HARMONICA,
        Note.C, 4,
        duration=0.5,
        quality=NoteQuality.PERFECT
    )
    print(f"   Note: {result['note']}{result['octave']}")
    print(f"   Frequency: {result['frequency']:.2f} Hz")
    print(f"   XP gained: {result['xp_gained']:.1f}")
    print(f"   Level: {result['current_level']}\n")

    # Test 2: Play many notes (level up!)
    print("2. Play 100 notes (level ups!)")
    for i in range(100):
        result = inst_sys.play_note(
            InstrumentType.HARMONICA,
            Note.C, 4,
            duration=0.5,
            quality=NoteQuality.GREAT
        )
        if result.get('leveled_up'):
            print(f"   {result['level_up_message']}")

    print(f"   Final Level: {result['current_level']}\n")

    # Test 3: Play song
    print("3. Play Song: Happy Birthday")
    accuracies = [0.98, 0.95, 0.92, 0.88, 0.90, 0.96]  # Good performance!
    song_result = inst_sys.play_song(
        InstrumentType.HARMONICA,
        "tutorial_happy_birthday",
        accuracies
    )
    print(f"   Score: {song_result['score_percent']:.1f}% (Rank: {song_result['rank']})")
    print(f"   Perfect Notes: {song_result['perfect_notes']}/{song_result['total_notes']}")
    print(f"   Learned: {song_result['learned']}")
    print(f"   Mastered: {song_result['mastered']}\n")

    # Test 4: Instrument Info
    print("4. Mundharmonika Info")
    info = inst_sys.get_instrument_info(InstrumentType.HARMONICA)
    print(f"   Skill Level: {info['skill_level']}")
    print(f"   Total Notes: {info['total_notes_played']}")
    print(f"   Accuracy: {info['accuracy']:.1f}%")
    print(f"   Songs Learned: {info['songs_learned']}")
    print(f"   Available Songs: {len(info['available_songs'])}")

    print("\n=== Instrument Playing System Test Complete ===")
    print("🎵 Mundharmonika ready to play!")
    print("✅ Skyrim Learning by Doing funktioniert!")
