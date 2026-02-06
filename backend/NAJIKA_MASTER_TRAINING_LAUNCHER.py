#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥🔥🔥 NAJIKA MASTER TRAINING LAUNCHER 🔥🔥🔥

BOMBENFEST - NIEMALS STOP!

STARTET:
1. LoRA-Training (alle 7 Tage)
2. Coding-Training (täglich)
3. Failsafe-Monitor (stündlich)
4. Auto-Recovery bei Fehlern

LÄUFT EWIG - KEIN AUSFALL MEHR!
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta
import pytz

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

# Directories
NAJIKA_DIR = Path('C:/Najika_World')
BACKEND_DIR = NAJIKA_DIR / 'backend'
CORE_DIR = Path('C:/Najika_World')
TRAINING_DIR = CORE_DIR / 'training'
LOG_FILE = TRAINING_DIR / 'master_launcher.log'
STATE_FILE = TRAINING_DIR / 'launcher_state.json'

BERLIN_TZ = pytz.timezone('Europe/Berlin')

# ===== LOGGING =====

def log(message, level='INFO'):
    """Thread-safe Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}'

    print(log_line)

    TRAINING_DIR.mkdir(exist_ok=True, parents=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

# ===== STATE MANAGEMENT =====

def load_state():
    """Lädt launcher state"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log(f"State load error: {e}", 'ERROR')

    # Default state
    return {
        'last_lora_training': None,
        'last_coding_training': None,
        'last_failsafe_check': None,
        'total_runs': 0,
        'errors': [],
        'created': datetime.now(BERLIN_TZ).isoformat()
    }

def save_state(state):
    """Speichert launcher state"""
    TRAINING_DIR.mkdir(exist_ok=True, parents=True)

    state['last_update'] = datetime.now(BERLIN_TZ).isoformat()

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

# ===== TRAINING FUNCTIONS =====

def should_run_lora_training(state):
    """Prüft ob LoRA-Training fällig ist (alle 7 Tage)"""
    if not state.get('last_lora_training'):
        return True, "Erstes LoRA-Training"

    try:
        last_run = datetime.fromisoformat(state['last_lora_training'])
        now = datetime.now(BERLIN_TZ)
        days_since = (now - last_run).days

        if days_since >= 7:
            return True, f"Letztes Training vor {days_since} Tagen"
        else:
            return False, f"Nächstes Training in {7 - days_since} Tagen"
    except Exception as e:
        log(f"LoRA-Check Error: {e}", 'ERROR')
        return False, str(e)

def run_lora_training():
    """Startet LoRA-Training"""
    log("="*80)
    log("🔥 STARTE LORA-TRAINING 🔥")
    log("="*80)

    script_path = BACKEND_DIR / 'najika_lora_training.py'

    if not script_path.exists():
        log(f"LoRA-Script nicht gefunden: {script_path}", 'ERROR')
        return False

    try:
        log("Starte LoRA-Training-Prozess...")

        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=7200,  # 2 Stunden Timeout
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0:
            log("LoRA-Training ERFOLGREICH!", 'INFO')
            log(f"Output: {result.stdout[:500]}", 'INFO')
            return True
        else:
            log(f"LoRA-Training FEHLER! Code: {result.returncode}", 'ERROR')
            log(f"stderr: {result.stderr[:500]}", 'ERROR')
            return False

    except subprocess.TimeoutExpired:
        log("LoRA-Training TIMEOUT nach 2 Stunden!", 'ERROR')
        return False
    except Exception as e:
        log(f"LoRA-Training Exception: {e}", 'ERROR')
        return False

def should_run_coding_training(state):
    """Prüft ob Coding-Training fällig ist (täglich)"""
    if not state.get('last_coding_training'):
        return True, "Erstes Coding-Training"

    try:
        last_run = datetime.fromisoformat(state['last_coding_training'])
        now = datetime.now(BERLIN_TZ)
        hours_since = (now - last_run).total_seconds() / 3600

        if hours_since >= 24:
            return True, f"Letztes Training vor {hours_since:.1f} Stunden"
        else:
            return False, f"Nächstes Training in {24 - hours_since:.1f} Stunden"
    except Exception as e:
        log(f"Coding-Check Error: {e}", 'ERROR')
        return False, str(e)

def run_coding_training():
    """Startet Coding-Training (generiert Doku)"""
    log("="*80)
    log("💻 STARTE CODING-TRAINING 💻")
    log("="*80)

    script_path = BACKEND_DIR / 'najika_create_coding_training.py'

    if not script_path.exists():
        log(f"Coding-Script nicht gefunden: {script_path}", 'ERROR')
        return False

    try:
        log("Generiere Coding-Training-Dokumentation...")

        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300,  # 5 Minuten Timeout
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0:
            log("Coding-Training ERFOLGREICH!", 'INFO')
            return True
        else:
            log(f"Coding-Training FEHLER! Code: {result.returncode}", 'ERROR')
            log(f"stderr: {result.stderr[:500]}", 'ERROR')
            return False

    except subprocess.TimeoutExpired:
        log("Coding-Training TIMEOUT nach 5 Minuten!", 'ERROR')
        return False
    except Exception as e:
        log(f"Coding-Training Exception: {e}", 'ERROR')
        return False

def should_run_failsafe(state):
    """Prüft ob Failsafe fällig ist (stündlich)"""
    if not state.get('last_failsafe_check'):
        return True, "Erster Failsafe-Check"

    try:
        last_run = datetime.fromisoformat(state['last_failsafe_check'])
        now = datetime.now(BERLIN_TZ)
        minutes_since = (now - last_run).total_seconds() / 60

        if minutes_since >= 60:
            return True, f"Letzter Check vor {minutes_since:.0f} Minuten"
        else:
            return False, f"Nächster Check in {60 - minutes_since:.0f} Minuten"
    except Exception as e:
        log(f"Failsafe-Check Error: {e}", 'ERROR')
        return False, str(e)

def run_failsafe():
    """Startet Failsafe-System"""
    log("="*80)
    log("🛡️ STARTE FAILSAFE-CHECK 🛡️")
    log("="*80)

    script_path = BACKEND_DIR / 'NAJIKA_TRAINING_ULTIMATE_FAILSAFE.py'

    if not script_path.exists():
        log(f"Failsafe-Script nicht gefunden: {script_path}", 'ERROR')
        return False

    try:
        log("Führe Failsafe-Check aus...")

        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300,  # 5 Minuten Timeout
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0:
            log("Failsafe-Check ERFOLGREICH!", 'INFO')
            return True
        else:
            log(f"Failsafe-Check WARNUNG! Code: {result.returncode}", 'WARNING')
            return True  # Warnung, aber kein Fehler

    except subprocess.TimeoutExpired:
        log("Failsafe TIMEOUT nach 5 Minuten!", 'ERROR')
        return False
    except Exception as e:
        log(f"Failsafe Exception: {e}", 'ERROR')
        return False

# ===== MAIN LOOP =====

def main():
    """Main Entry Point"""

    log("="*80)
    log("🔥🔥🔥 NAJIKA MASTER TRAINING LAUNCHER 🔥🔥🔥")
    log("="*80)
    log(f"Zeit: {datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    log("="*80)

    # Load state
    state = load_state()
    state['total_runs'] += 1

    log(f"Run #{state['total_runs']}")

    # 1. LoRA-Training (alle 7 Tage)
    should_lora, lora_msg = should_run_lora_training(state)
    log(f"LoRA-Training: {lora_msg}")

    if should_lora:
        success = run_lora_training()
        if success:
            state['last_lora_training'] = datetime.now(BERLIN_TZ).isoformat()
            log("✅ LoRA-Training abgeschlossen!", 'INFO')
        else:
            state['errors'].append({
                'time': datetime.now(BERLIN_TZ).isoformat(),
                'type': 'lora_training',
                'message': 'LoRA-Training fehlgeschlagen'
            })
            log("❌ LoRA-Training fehlgeschlagen!", 'ERROR')

    # 2. Coding-Training (täglich)
    should_coding, coding_msg = should_run_coding_training(state)
    log(f"Coding-Training: {coding_msg}")

    if should_coding:
        success = run_coding_training()
        if success:
            state['last_coding_training'] = datetime.now(BERLIN_TZ).isoformat()
            log("✅ Coding-Training abgeschlossen!", 'INFO')
        else:
            state['errors'].append({
                'time': datetime.now(BERLIN_TZ).isoformat(),
                'type': 'coding_training',
                'message': 'Coding-Training fehlgeschlagen'
            })
            log("❌ Coding-Training fehlgeschlagen!", 'ERROR')

    # 3. Failsafe (stündlich)
    should_fail, fail_msg = should_run_failsafe(state)
    log(f"Failsafe: {fail_msg}")

    if should_fail:
        success = run_failsafe()
        if success:
            state['last_failsafe_check'] = datetime.now(BERLIN_TZ).isoformat()
            log("✅ Failsafe-Check abgeschlossen!", 'INFO')
        else:
            state['errors'].append({
                'time': datetime.now(BERLIN_TZ).isoformat(),
                'type': 'failsafe',
                'message': 'Failsafe fehlgeschlagen'
            })
            log("❌ Failsafe fehlgeschlagen!", 'ERROR')

    # Trim errors (max 50)
    if len(state.get('errors', [])) > 50:
        state['errors'] = state['errors'][-50:]

    # Save state
    save_state(state)

    log("="*80)
    log("MASTER LAUNCHER FERTIG!")
    log("="*80)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("Launcher abgebrochen (Ctrl+C)", 'WARNING')
        sys.exit(1)
    except Exception as e:
        log(f"KRITISCHER FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
        sys.exit(1)
