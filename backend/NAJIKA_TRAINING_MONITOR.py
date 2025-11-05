#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA TRAINING - LIVE MONITOR

Zeigt Echtzeit-Status des Training-Systems
"""
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
import time
from pathlib import Path
from datetime import datetime, timedelta
import pytz

NAJIKA_DIR = Path('C:/NajikaCore')
TRAINING_DIR = NAJIKA_DIR / 'training'
SCHEDULE_FILE = TRAINING_DIR / 'schedule.json'
HEARTBEAT_FILE = NAJIKA_DIR / 'NAJIKA_TRAINING_HEARTBEAT.json'
CURRENT_SESSION_FILE = NAJIKA_DIR / 'NAJIKA_CURRENT_TRAINING.md'
LOG_FILE = TRAINING_DIR / 'training.log'

BERLIN_TZ = pytz.timezone('Europe/Berlin')

def clear_screen():
    """Clears Terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_schedule():
    """Lädt Schedule"""
    if SCHEDULE_FILE.exists():
        try:
            with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None

def check_heartbeat():
    """Prüft Heartbeat"""
    if not HEARTBEAT_FILE.exists():
        return None, "Kein Heartbeat"

    try:
        with open(HEARTBEAT_FILE, 'r', encoding='utf-8') as f:
            heartbeat = json.load(f)

        last_update_str = heartbeat.get('last_update')
        if not last_update_str:
            return None, "Heartbeat ohne Timestamp"

        last_update = datetime.fromisoformat(last_update_str)
        now = datetime.now(BERLIN_TZ)

        age_seconds = (now - last_update).total_seconds()
        age_minutes = age_seconds / 60

        if age_minutes < 10:
            status = "OK"
        elif age_minutes < 30:
            status = "WARNING"
        else:
            status = "CRITICAL"

        return status, f"{age_minutes:.1f} Min"

    except Exception as e:
        return "ERROR", str(e)

def get_last_log_lines(n=10):
    """Holt letzte N Log-Zeilen"""
    if not LOG_FILE.exists():
        return []

    try:
        with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            return lines[-n:]
    except:
        return []

def monitor_loop():
    """Haupt-Monitor-Loop"""

    while True:
        clear_screen()

        print("="*80)
        print("NAJIKA TRAINING - LIVE MONITOR")
        print("="*80)
        print()

        now = datetime.now(BERLIN_TZ)
        print(f"Zeit: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print()

        # ===== HEARTBEAT =====
        print("─"*80)
        print("HEARTBEAT STATUS")
        print("─"*80)

        hb_status, hb_msg = check_heartbeat()

        if hb_status == "OK":
            print(f"[OK] System alive - Letzter Beat vor {hb_msg}")
        elif hb_status == "WARNING":
            print(f"[WARNING] System langsam - Letzter Beat vor {hb_msg}")
        elif hb_status == "CRITICAL":
            print(f"[CRITICAL] System down? - Letzter Beat vor {hb_msg}")
        else:
            print(f"[ERROR] {hb_msg}")

        print()

        # ===== SCHEDULE =====
        print("─"*80)
        print("TRAINING PROGRESS")
        print("─"*80)

        schedule = load_schedule()

        if schedule:
            print(f"Gesamt-Stunden:  {schedule.get('total_hours', 0)}")
            print(f"Trainings-Tage:  {schedule.get('days_trained', 0)}")
            print(f"Aktuelle Woche:  {schedule.get('current_week', 1)}")
            print(f"Startdatum:      {schedule.get('start_date', 'Unbekannt')[:10]}")

            # Heute's Sessions
            today_key = now.strftime('%Y-%m-%d')
            today_sessions = [s for s in schedule.get('completed_sessions', []) if today_key in s]

            print()
            print(f"Heute completed: {len(today_sessions)} / 15")

            if today_sessions:
                print("  Letzte Sessions:")
                for session in today_sessions[-3:]:
                    _, time_block = session.split('_')
                    print(f"    OK {time_block}")

        else:
            print("[WARNING] Kein Schedule gefunden!")
            print("System wurde noch nicht gestartet.")

        print()

        # ===== AKTUELLE SESSION =====
        print("─"*80)
        print("AKTUELLE SESSION")
        print("─"*80)

        if CURRENT_SESSION_FILE.exists():
            age_seconds = time.time() - CURRENT_SESSION_FILE.stat().st_mtime
            age_minutes = age_seconds / 60

            print(f"Session-File:    OK (vor {age_minutes:.0f} Min)")

            # Lese erste Zeilen
            try:
                with open(CURRENT_SESSION_FILE, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:15]
                    for line in lines:
                        if '**Zeit:**' in line or '**Focus:**' in line:
                            print(f"  {line.strip()}")
            except:
                pass
        else:
            print("[WARNING] Kein Session-File gefunden!")

        print()

        # ===== LETZTE LOG-ZEILEN =====
        print("─"*80)
        print("LETZTE LOG-EINTRÄGE")
        print("─"*80)

        log_lines = get_last_log_lines(5)

        if log_lines:
            for line in log_lines:
                # Färbe nach Level
                if '[ERROR]' in line:
                    print(line.strip())
                elif '[WARNING]' in line:
                    print(line.strip())
                else:
                    print(line.strip())
        else:
            print("[INFO] Keine Logs vorhanden")

        print()

        # ===== FOOTER =====
        print("="*80)
        print("Drücke Ctrl+C zum Beenden | Auto-Refresh alle 10 Sekunden")
        print("="*80)

        # Wait
        time.sleep(10)

if __name__ == '__main__':
    try:
        monitor_loop()
    except KeyboardInterrupt:
        print("\n\nMonitor beendet!")
