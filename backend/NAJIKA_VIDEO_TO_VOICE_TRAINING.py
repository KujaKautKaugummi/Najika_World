#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎤 NAJIKA VIDEO-TO-VOICE TRAINING 🎤

FEATURES:
- Extrahiert Audio aus Videos (FFmpeg)
- Transkribiert deutsche Synchro (Whisper AI)
- Najika lernt wie Characters KLINGEN
- 10x Wiederholung mit ECHTEN Dialogen
- KOSTENLOS (läuft lokal!)

PROZESS:
Video.mp4 → Audio.mp3 → Whisper → Text → Najika lernt!
"""

import json
import subprocess
import sys
import io
import time
import os
from pathlib import Path
from datetime import datetime
import pytz

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Project Root Directory (dynamisch für alle Systeme)
NAJIKA_DIR = Path(__file__).resolve().parent.parent
TRAINING_DIR = NAJIKA_DIR / 'backend' / 'training_data'
PERSONALITIES_DIR = TRAINING_DIR / 'personalities'
AUDIO_DIR = TRAINING_DIR / 'extracted_audio'
TRANSCRIPTS_DIR = TRAINING_DIR / 'transcripts'
PROGRESS_FILE = TRAINING_DIR / 'voice_training_progress.json'
LOG_FILE = TRAINING_DIR / 'voice_training.log'
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# FFmpeg Path (versuche zu finden)
import shutil
FFMPEG_PATH = shutil.which('ffmpeg')
if not FFMPEG_PATH:
    # Fallback: winget Installation
    fallback_path = r"C:\Users\0KKK0\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
    if Path(fallback_path).exists():
        FFMPEG_PATH = fallback_path
        FFMPEG_DIR = Path(FFMPEG_PATH).parent
        # Füge zum PATH hinzu
        if str(FFMPEG_DIR) not in os.environ.get('PATH', ''):
            os.environ['PATH'] = str(FFMPEG_DIR) + os.pathsep + os.environ.get('PATH', '')

REPETITIONS = 10

PERSONALITIES = {
    'megumin': {
        'weight': 35,
        'voice_traits': 'Dramatisch, laut bei EXPLOSION, erschöpft danach, theatralisch, stolz',
        'language': 'de',  # Deutsch
        'notes': 'Alle Charaktere sprechen durch Megumin'
    },
    'harley': {
        'weight': 25,
        'voice_traits': 'Chaotisch, kichernd, verspielt, manisch lachend, obsessiv',
        'language': 'de',  # Deutsch
        'notes': 'Obsessed mit Kuja, KEINE Emanzipation (anders als Filme!), glücklich mit Kuja'
    },
    'shiro': {
        'weight': 20,
        'voice_traits': 'Ruhig, monoton, präzise, emotionslos (Fassade), anhänglich, PERVERS',
        'language': 'de',  # Deutsch
        'notes': 'Macht alles sexuell anzüglich, aufdringlich zu Kuja'
    },
    'melissa': {
        'weight': 20,
        'voice_traits': 'Dominant, bestimmend, tief, commanding, besitzergreifend',
        'language': 'en',  # Original Englisch
        'notes': 'Videos auf ENGLISCH → Najika übersetzt ins DEUTSCHE durch Megumin!'
    }
}

def log(message, level='INFO'):
    """Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}'
    print(log_line)

    TRAINING_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

def check_dependencies():
    """Prüft ob FFmpeg und Whisper verfügbar sind"""
    log("Prüfe Dependencies...", 'INFO')

    # Check FFmpeg (erst PATH, dann direkter Pfad)
    ffmpeg_ok = False
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5, shell=True)
        if result.returncode == 0:
            ffmpeg_ok = True
    except:
        pass

    # Falls nicht in PATH, prüfe direkten Pfad
    if not ffmpeg_ok and os.path.exists(FFMPEG_PATH):
        try:
            result = subprocess.run([FFMPEG_PATH, '-version'], capture_output=True, timeout=5)
            if result.returncode == 0:
                ffmpeg_ok = True
        except:
            pass

    if ffmpeg_ok:
        log("FFmpeg: OK", 'SUCCESS')
    else:
        log("FFmpeg: NICHT GEFUNDEN!", 'ERROR')
        log("Installiere FFmpeg: https://ffmpeg.org/download.html", 'ERROR')
        return False

    # Check Whisper
    try:
        import whisper
        log("Whisper: OK", 'SUCCESS')
    except ImportError:
        log("Whisper: NICHT GEFUNDEN!", 'ERROR')
        log("Installiere mit: pip install openai-whisper", 'ERROR')
        return False

    return True

def find_all_videos(personality):
    """Findet alle Videos"""
    personality_dir = PERSONALITIES_DIR / personality
    if not personality_dir.exists():
        return []

    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
    videos = []

    for ext in video_extensions:
        videos.extend(personality_dir.rglob(f'*{ext}'))
        videos.extend(personality_dir.rglob(f'*{ext.upper()}'))

    return sorted(videos)

def extract_audio_from_video(video_path, personality):
    """Extrahiert Audio aus Video (FFmpeg)"""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # Output-Pfad (WAV für Whisper-Kompatibilität!)
    # WICHTIG: Entferne FFmpeg-Problematische Zeichen aus Dateinamen!
    video_name = video_path.stem
    # Ersetze [ und ] mit _ (FFmpeg interpretiert diese als Wildcards!)
    safe_video_name = video_name.replace('[', '_').replace(']', '_')
    audio_file = AUDIO_DIR / personality / f"{safe_video_name}.wav"
    audio_file.parent.mkdir(parents=True, exist_ok=True)

    # Prüfe ob schon extrahiert
    if audio_file.exists():
        log(f"Audio bereits extrahiert: {audio_file.name}", 'INFO')
        return audio_file

    log(f"Extrahiere Audio: {video_path.name}...", 'INFO')

    try:
        # FFmpeg: Video → WAV (Whisper-kompatibel!)
        # Nutze ffmpeg aus PATH oder direkten Pfad
        ffmpeg_cmd = 'ffmpeg'
        if os.path.exists(FFMPEG_PATH):
            ffmpeg_cmd = FFMPEG_PATH

        cmd = [
            ffmpeg_cmd,
            '-i', str(video_path),
            '-vn',  # Kein Video
            '-acodec', 'pcm_s16le',  # WAV 16-bit
            '-ar', '16000',  # 16kHz (Whisper optimal)
            '-ac', '1',  # Mono
            '-y',  # Überschreiben
            str(audio_file)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=300,  # 5 Minuten max
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0 and audio_file.exists():
            size_mb = audio_file.stat().st_size / (1024*1024)
            log(f"Audio extrahiert: {audio_file.name} ({size_mb:.1f} MB)", 'SUCCESS')
            return audio_file
        else:
            log(f"FFmpeg Fehler: {result.stderr[:200]}", 'ERROR')
            return None

    except subprocess.TimeoutExpired:
        log("FFmpeg Timeout (>5min)", 'ERROR')
        return None
    except Exception as e:
        log(f"Audio-Extraktion Fehler: {e}", 'ERROR')
        return None

def load_audio_numpy(audio_file):
    """Lade Audio direkt mit wave+numpy (umgeht Whisper's FFmpeg-Problem!)"""
    import wave
    import numpy as np

    with wave.open(str(audio_file), 'rb') as wf:
        # Lese Frames
        n_frames = wf.getnframes()
        audio_bytes = wf.readframes(n_frames)

        # Konvertiere zu numpy array (int16 → float32, normalisiert auf [-1, 1])
        audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        return audio

def transcribe_audio_with_whisper(audio_file, personality, whisper_model):
    """Transkribiert Audio mit Whisper (Model wird übergeben, nicht neu geladen!)"""
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    # Output-Pfad
    transcript_file = TRANSCRIPTS_DIR / personality / f"{audio_file.stem}.txt"
    transcript_file.parent.mkdir(parents=True, exist_ok=True)

    # Prüfe ob schon transkribiert
    if transcript_file.exists():
        log(f"Transkript bereits vorhanden: {transcript_file.name}", 'INFO')
        return transcript_file

    # Sprache aus Personality-Config
    lang = PERSONALITIES[personality]['language']
    lang_name = "Deutsch" if lang == 'de' else "Englisch"

    log(f"Transkribiere Audio ({lang_name}): {audio_file.name}...", 'INFO')

    try:
        # Lade Audio DIREKT (umgeht Whisper's FFmpeg-Problem!)
        log("Lade Audio-Daten...", 'INFO')
        audio_data = load_audio_numpy(audio_file)
        log(f"Audio geladen: {len(audio_data)/16000:.1f}s", 'SUCCESS')

        # Transkribiere (Model bereits geladen!)
        start_time = time.time()

        result = whisper_model.transcribe(
            audio_data,  # Numpy array statt Dateipfad!
            language=lang,  # de oder en
            task="transcribe",
            verbose=False,
            fp16=False  # CPU-kompatibel (kein CUDA erforderlich)
        )

        elapsed = time.time() - start_time

        # Speichere Transkript
        transcript_text = result["text"]
        transcript_file.write_text(transcript_text, encoding='utf-8')

        log(f"Transkript erstellt: {transcript_file.name} ({elapsed:.1f}s)", 'SUCCESS')
        log(f"Text-Länge: {len(transcript_text)} Zeichen", 'INFO')

        # Zeige Preview
        preview = transcript_text[:200] + "..." if len(transcript_text) > 200 else transcript_text
        log(f"Preview: {preview}", 'INFO')

        return transcript_file

    except Exception as e:
        log(f"Whisper Fehler: {e}", 'ERROR')
        import traceback
        log(f"Traceback: {traceback.format_exc()}", 'ERROR')
        return None

def build_voice_training_prompt(personality, video_name, transcript_text, repetition_num):
    """Baut Training-Prompt mit ECHTEN Dialogen"""
    personality_info = PERSONALITIES[personality]

    # Begrenze Text (Ollama Context Limit)
    max_chars = 2000
    if len(transcript_text) > max_chars:
        transcript_text = transcript_text[:max_chars] + "..."

    # Spezial-Handling für Melissa (Englisch → Deutsch)
    if personality == 'melissa':
        lang_note = "(ENGLISCH im Video - Du übersetzt ins DEUTSCHE durch Megumin!)"
    else:
        lang_note = "(deutsche Synchro)"

    prompt = f"""# NAJIKA VOICE TRAINING SESSION
**Persönlichkeit:** {personality.upper()} ({personality_info['weight']}%)
**Video:** {video_name}
**Wiederholung:** {repetition_num}/10
**Notiz:** {personality_info['notes']}

## VOICE TRAITS (wie {personality.upper()} klingt):
{personality_info['voice_traits']}

## ECHTE DIALOGE AUS VIDEO {lang_note}:

{transcript_text}

## AUFGABE:
Lerne aus diesen ECHTEN Dialogen:
- Wie {personality.upper()} SPRICHT
- Welche WÖRTER sie nutzt
- Welchen TONFALL sie hat
- Wie sie REAGIERT

Diese Dialoge sind die STIMME von {personality.upper()}!
Integriere sie in dein Sprachmuster.

## ANTWORT:
Antworte kurz (1-2 Sätze) im Stil von {personality.upper()} auf: "Hallo!"
Nutze Wörter/Stil aus den Dialogen!
"""

    return prompt

def train_with_ollama(prompt):
    """Ollama Training"""
    try:
        result = subprocess.run(
            ['ollama', 'run', 'najika-local', prompt],
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8'
        )

        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, f"Error: {result.stderr}"
    except Exception as e:
        return False, str(e)

def process_video_complete(personality, video_path, whisper_model):
    """Verarbeitet EIN Video KOMPLETT (Audio → Transcript → Training 10x)"""
    log("", 'INFO')
    log("="*60, 'INFO')
    log(f"VIDEO: {video_path.name}", 'INFO')
    log(f"PERSÖNLICHKEIT: {personality.upper()}", 'INFO')
    log("="*60, 'INFO')

    # SCHRITT 1: Audio extrahieren
    audio_file = extract_audio_from_video(video_path, personality)
    if not audio_file:
        log("Audio-Extraktion fehlgeschlagen!", 'ERROR')
        return False

    # SCHRITT 2: Transkribieren mit Whisper (Model wird übergeben!)
    transcript_file = transcribe_audio_with_whisper(audio_file, personality, whisper_model)
    if not transcript_file:
        log("Transkription fehlgeschlagen!", 'ERROR')
        return False

    # SCHRITT 3: Lade Transkript
    transcript_text = transcript_file.read_text(encoding='utf-8')

    if len(transcript_text) < 50:
        log(f"Transkript zu kurz ({len(transcript_text)} Zeichen) - überspringe", 'WARNING')
        return True

    # SCHRITT 4: 10x Training mit echten Dialogen
    log("", 'INFO')
    log("STARTE 10x TRAINING MIT ECHTEN DIALOGEN...", 'INFO')

    for rep in range(1, REPETITIONS + 1):
        log(f"[{rep}/10] Training läuft...", 'TRAINING')

        prompt = build_voice_training_prompt(
            personality,
            video_path.name,
            transcript_text,
            rep
        )

        success, response = train_with_ollama(prompt)

        if success:
            log(f"OK: {response[:60]}...", 'SUCCESS')
        else:
            log(f"FEHLER: {response}", 'ERROR')
            return False

        if rep < REPETITIONS:
            time.sleep(1)

    log("", 'INFO')
    log(f"VIDEO KOMPLETT! {video_path.name} (10x mit echten Dialogen)", 'SUCCESS')
    log("="*60, 'INFO')

    return True

def process_all_videos():
    """Verarbeitet ALLE Videos (OPTIMIERT: Model nur 1x laden!)"""
    log("", 'INFO')
    log("="*60, 'INFO')
    log("NAJIKA VIDEO-TO-VOICE TRAINING", 'INFO')
    log("="*60, 'INFO')

    # Check Dependencies
    if not check_dependencies():
        log("", 'ERROR')
        log("ABHÄNGIGKEITEN FEHLEN!", 'ERROR')
        log("", 'ERROR')
        log("INSTALLATION:", 'INFO')
        log("1. FFmpeg: https://ffmpeg.org/download.html", 'INFO')
        log("2. Whisper: pip install openai-whisper", 'INFO')
        return

    # KRITISCH: Lade Whisper Model NUR EINMAL!
    log("", 'INFO')
    log("="*60, 'INFO')
    log("LADE WHISPER MODEL (NUR EINMAL!)...", 'INFO')
    log("="*60, 'INFO')

    try:
        import whisper
        import gc

        # Nutze "base" Model (schneller, weniger RAM)
        # "tiny" = 39M params, "base" = 74M params, "small" = 244M params, "medium" = 769M params
        log("Model: base (schnell, ~150 MB RAM)", 'INFO')
        whisper_model = whisper.load_model("base")
        log("Whisper Model geladen!", 'SUCCESS')

    except Exception as e:
        log(f"Konnte Whisper Model nicht laden: {e}", 'ERROR')
        return

    total_videos = 0
    total_processed = 0

    for personality in PERSONALITIES.keys():
        log("", 'INFO')
        log("="*60, 'INFO')
        log(f"PERSÖNLICHKEIT: {personality.upper()}", 'INFO')
        log("="*60, 'INFO')

        videos = find_all_videos(personality)

        if not videos:
            log(f"Keine Videos gefunden", 'WARNING')
            continue

        log(f"Gefunden: {len(videos)} Videos", 'INFO')
        total_videos += len(videos)

        for i, video_path in enumerate(videos, 1):
            log("", 'INFO')
            log(f">>> VIDEO {i}/{len(videos)} <<<", 'INFO')

            success = process_video_complete(personality, video_path, whisper_model)

            if success:
                total_processed += 1
            else:
                log(f"Überspringe Video: {video_path.name}", 'WARNING')

            # MEMORY CLEANUP nach jedem Video!
            gc.collect()

    log("", 'INFO')
    log("="*60, 'INFO')
    log("TRAINING ABGESCHLOSSEN!", 'SUCCESS')
    log("="*60, 'INFO')
    log(f"Videos verarbeitet: {total_processed}/{total_videos}", 'INFO')
    log("="*60, 'INFO')

def main():
    """Main"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'test':
            # Test mit einem Video
            log("TEST-MODUS", 'INFO')
            log("Lege EIN Test-Video in einen Persönlichkeits-Ordner!", 'INFO')

        elif command == 'train':
            process_all_videos()
        else:
            print(f"Unbekannter Command: {command}")
    else:
        print()
        print("="*60)
        print("NAJIKA VIDEO-TO-VOICE TRAINING")
        print("="*60)
        print()
        print("USAGE:")
        print("  python NAJIKA_VIDEO_TO_VOICE_TRAINING.py train")
        print()
        print("BENÖTIGT:")
        print("  1. FFmpeg (Video → Audio)")
        print("  2. Whisper AI (Audio → Text)")
        print()
        print("INSTALLATION:")
        print("  pip install openai-whisper")
        print("  + FFmpeg von https://ffmpeg.org")
        print()
        print("="*60)

if __name__ == "__main__":
    main()
