#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA MASTER TRAINING LAUNCHER v2.0
=====================================
ZEITBASIERTES Training (nicht mehr Intervall-basiert!)

SCHEDULE:
- Code Training:  TAEGLICH ab 08:00 Uhr (~45 Min)
- LoRA Training:  SONNTAG ab 08:00 Uhr (~2h, blockiert GPU!)
- Failsafe Check: Stuendlich (wenn Launcher laeuft)

Wird via Windows Task Scheduler stuendlich aufgerufen.
Prueft ob die richtige Uhrzeit/Tag ist und startet dann.
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta

try:
    import pytz
    BERLIN_TZ = pytz.timezone('Europe/Berlin')
except ImportError:
    # Fallback ohne pytz
    BERLIN_TZ = None

# Fix encoding (Windows)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# Directories
NAJIKA_DIR = Path('C:/Najika_World')
BACKEND_DIR = NAJIKA_DIR / 'backend'
TRAINING_DIR = NAJIKA_DIR / 'training'
LOG_FILE = TRAINING_DIR / 'master_launcher.log'
STATE_FILE = TRAINING_DIR / 'launcher_state.json'

# ===== SCHEDULE KONFIGURATION =====
DAILY_TRAINING_HOUR = 8       # Code-Training startet ab 08:00
LORA_TRAINING_DAY = 6         # Sonntag (0=Montag, 6=Sonntag)
LORA_TRAINING_HOUR = 8        # LoRA startet ab 08:00 Sonntag


# ===== LOGGING =====

def log(message, level='INFO'):
    """Thread-safe Logging"""
    now = datetime.now(BERLIN_TZ) if BERLIN_TZ else datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}'

    print(log_line)

    TRAINING_DIR.mkdir(exist_ok=True, parents=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
    except:
        pass


# ===== STATE MANAGEMENT =====

def load_state():
    """Laedt launcher state"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log(f"State load error: {e}", 'ERROR')

    return {
        'last_lora_training': None,
        'last_coding_training': None,
        'last_failsafe_check': None,
        'total_runs': 0,
        'errors': [],
        'created': datetime.now().isoformat()
    }

def save_state(state):
    """Speichert launcher state"""
    TRAINING_DIR.mkdir(exist_ok=True, parents=True)
    state['last_update'] = datetime.now().isoformat()
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


# ===== SCHEDULE CHECKS =====

def should_run_coding_today(state):
    """
    Code-Training: Taeglich ab 08:00, EINMAL pro Tag
    Prueft ob heute schon gelaufen ist.
    """
    now = datetime.now(BERLIN_TZ) if BERLIN_TZ else datetime.now()

    # Nur ab 08:00 starten
    if now.hour < DAILY_TRAINING_HOUR:
        return False, f"Zu frueh ({now.hour}:00 < {DAILY_TRAINING_HOUR}:00)"

    # Pruefe ob heute schon gelaufen
    last = state.get('last_coding_training')
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            # Wenn timezone-naive, mach es aware
            if last_dt.tzinfo is None and BERLIN_TZ:
                last_dt = BERLIN_TZ.localize(last_dt)
            if last_dt.date() == now.date():
                return False, "Heute schon gelaufen"
        except:
            pass

    return True, f"Taeglich 08:00 - jetzt ist {now.hour}:{now.minute:02d}"


def should_run_lora_today(state):
    """
    LoRA Training: NUR SONNTAG ab 08:00, EINMAL pro Woche
    """
    now = datetime.now(BERLIN_TZ) if BERLIN_TZ else datetime.now()

    # Nur Sonntag
    if now.weekday() != LORA_TRAINING_DAY:
        days_until = (LORA_TRAINING_DAY - now.weekday()) % 7
        if days_until == 0:
            days_until = 7
        return False, f"Nicht Sonntag (noch {days_until} Tage)"

    # Nur ab 08:00
    if now.hour < LORA_TRAINING_HOUR:
        return False, f"Sonntag aber zu frueh ({now.hour}:00 < {LORA_TRAINING_HOUR}:00)"

    # Pruefe ob diese Woche schon gelaufen
    last = state.get('last_lora_training')
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if last_dt.tzinfo is None and BERLIN_TZ:
                last_dt = BERLIN_TZ.localize(last_dt)
            days_since = (now - last_dt).days
            if days_since < 6:  # Weniger als 6 Tage seit letztem Run
                return False, f"Diese Woche schon gelaufen (vor {days_since} Tagen)"
        except:
            pass

    return True, f"Sonntag 08:00 - GO!"


def should_run_failsafe(state):
    """Failsafe: Stuendlich"""
    last = state.get('last_failsafe_check')
    if not last:
        return True, "Erster Check"

    try:
        last_dt = datetime.fromisoformat(last)
        now = datetime.now(BERLIN_TZ) if BERLIN_TZ else datetime.now()
        if last_dt.tzinfo is None and BERLIN_TZ:
            last_dt = BERLIN_TZ.localize(last_dt)
        minutes_since = (now - last_dt).total_seconds() / 60
        if minutes_since >= 55:  # 55 Min Buffer
            return True, f"Letzter Check vor {minutes_since:.0f} Min"
        return False, f"Naechster Check in {60 - minutes_since:.0f} Min"
    except:
        return True, "Check-Error, laufe sicherheitshalber"


# ===== TRAINING FUNCTIONS =====

def run_coding_training():
    """Startet Code-Training"""
    log("=" * 60)
    log("CODE-TRAINING START (taeglich 08:00)")
    log("=" * 60)

    # Bevorzuge das echte Code-Training Script
    script_path = BACKEND_DIR / 'najika_code_training_real.py'
    if not script_path.exists():
        script_path = BACKEND_DIR / 'najika_create_coding_training.py'

    if not script_path.exists():
        log(f"Coding-Script nicht gefunden!", 'ERROR')
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=2700,  # 45 Minuten Timeout
            encoding='utf-8',
            errors='replace',
            cwd=str(NAJIKA_DIR)
        )

        if result.returncode == 0:
            log("Code-Training ERFOLGREICH!")
            if result.stdout:
                # Nur letzte 3 Zeilen loggen
                last_lines = result.stdout.strip().split('\n')[-3:]
                for line in last_lines:
                    log(f"  {line}")
            return True
        else:
            log(f"Code-Training FEHLER! Code: {result.returncode}", 'ERROR')
            if result.stderr:
                log(f"  {result.stderr[:300]}", 'ERROR')
            return False

    except subprocess.TimeoutExpired:
        log("Code-Training TIMEOUT nach 45 Min!", 'ERROR')
        return False
    except Exception as e:
        log(f"Code-Training Exception: {e}", 'ERROR')
        return False


def run_lora_training():
    """Startet LoRA Fine-Tuning (Sonntag)"""
    log("=" * 60)
    log("LORA FINE-TUNING START (Sonntag 08:00)")
    log("=" * 60)

    # Pruefe ob Ollama laeuft
    try:
        import urllib.request
        urllib.request.urlopen('http://127.0.0.1:11434/api/tags', timeout=5)
        log("Ollama erreichbar")
    except:
        log("Ollama nicht erreichbar - LoRA-Training uebersprungen!", 'WARNING')
        return False

    # Bevorzuge unsloth training
    script_path = BACKEND_DIR / 'najika_unsloth_training.py'
    if not script_path.exists():
        script_path = BACKEND_DIR / 'najika_lora_training_3b.py'

    if not script_path.exists():
        log(f"LoRA-Script nicht gefunden!", 'ERROR')
        return False

    try:
        log(f"Starte {script_path.name}...")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=10800,  # 3 Stunden Timeout
            encoding='utf-8',
            errors='replace',
            cwd=str(NAJIKA_DIR)
        )

        if result.returncode == 0:
            log("LoRA-Training ERFOLGREICH!")
            return True
        else:
            log(f"LoRA-Training FEHLER! Code: {result.returncode}", 'ERROR')
            if result.stderr:
                log(f"  {result.stderr[:300]}", 'ERROR')
            return False

    except subprocess.TimeoutExpired:
        log("LoRA-Training TIMEOUT nach 3 Stunden!", 'ERROR')
        return False
    except Exception as e:
        log(f"LoRA-Training Exception: {e}", 'ERROR')
        return False


def run_failsafe():
    """Failsafe Health-Check"""
    script_path = BACKEND_DIR / 'NAJIKA_TRAINING_ULTIMATE_FAILSAFE.py'
    if not script_path.exists():
        return True  # Kein Failsafe-Script = OK

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300,
            encoding='utf-8',
            errors='replace',
            cwd=str(NAJIKA_DIR)
        )
        return result.returncode == 0
    except:
        return True  # Fehler im Failsafe ist kein Blocker


# ===== MAIN =====

def main():
    now = datetime.now(BERLIN_TZ) if BERLIN_TZ else datetime.now()

    log("=" * 60)
    log("NAJIKA TRAINING LAUNCHER v2.0")
    log(f"Zeit: {now.strftime('%A %Y-%m-%d %H:%M:%S')}")
    log(f"Schedule: Code taeglich 08:00 | LoRA Sonntag 08:00")
    log("=" * 60)

    state = load_state()
    state['total_runs'] = state.get('total_runs', 0) + 1
    log(f"Run #{state['total_runs']}")

    # 1. LoRA Training (Sonntag 08:00)
    should_lora, lora_msg = should_run_lora_today(state)
    log(f"LoRA: {lora_msg}")

    if should_lora:
        success = run_lora_training()
        if success:
            state['last_lora_training'] = now.isoformat()
            log("LoRA-Training abgeschlossen!")
        else:
            state.setdefault('errors', []).append({
                'time': now.isoformat(),
                'type': 'lora_training',
                'message': 'LoRA-Training fehlgeschlagen'
            })

    # 2. Code Training (taeglich 08:00)
    should_coding, coding_msg = should_run_coding_today(state)
    log(f"Code: {coding_msg}")

    if should_coding:
        success = run_coding_training()
        if success:
            state['last_coding_training'] = now.isoformat()
            log("Code-Training abgeschlossen!")
        else:
            state.setdefault('errors', []).append({
                'time': now.isoformat(),
                'type': 'coding_training',
                'message': 'Code-Training fehlgeschlagen'
            })

    # 3. Failsafe (stuendlich)
    should_fail, fail_msg = should_run_failsafe(state)
    if should_fail:
        run_failsafe()
        state['last_failsafe_check'] = now.isoformat()

    # Trim errors (max 20)
    if len(state.get('errors', [])) > 20:
        state['errors'] = state['errors'][-20:]

    save_state(state)

    log("LAUNCHER FERTIG")
    log("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("Abgebrochen (Ctrl+C)", 'WARNING')
        sys.exit(1)
    except Exception as e:
        log(f"KRITISCHER FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
