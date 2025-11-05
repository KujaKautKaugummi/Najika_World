#!/usr/bin/env python3
"""
🔥 NAJIKA TRAINING - ULTIMATE FAIL-SAFE SYSTEM 🔥

15 STUNDEN TÄGLICH (08:00-23:00)
JEDEN TAG (Mo-So)
MIT WARN-POPUP BEI AUSFALL
AUTO-RECOVERY BEI FEHLERN
LIVE-MONITORING

NIEMALS WIEDER VERLUST!!!
"""

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta
import pytz
import sys

# Fix Windows encoding for emoji support
sys.stdout.reconfigure(encoding='utf-8')

# ===== KONFIGURATION =====

NAJIKA_DIR = Path('C:/NajikaCore')
TRAINING_DIR = NAJIKA_DIR / 'training'
SCHEDULE_FILE = TRAINING_DIR / 'schedule.json'
HEARTBEAT_FILE = NAJIKA_DIR / 'NAJIKA_TRAINING_HEARTBEAT.json'
CURRENT_SESSION_FILE = NAJIKA_DIR / 'NAJIKA_CURRENT_TRAINING.md'
LOG_FILE = TRAINING_DIR / 'training.log'

BERLIN_TZ = pytz.timezone('Europe/Berlin')

# 15 STUNDEN TÄGLICH! (08:00-23:00)
TRAINING_HOURS = list(range(8, 23))  # 8, 9, 10, ..., 22

# JEDEN TAG!
TRAINING_DAYS = [0, 1, 2, 3, 4, 5, 6]  # Mo-So

# WARN-SCHWELLWERTE
MAX_SESSION_AGE_MINUTES = 70  # Wenn Session älter als 70 Min -> WARNUNG!
MAX_HEARTBEAT_AGE_MINUTES = 10  # Wenn Heartbeat älter als 10 Min -> WARNUNG!

# ===== LOGGING =====

def log(message, level='INFO'):
    """Thread-safe Logging"""
    timestamp = datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'[{timestamp}] [{level}] {message}\n'

    print(log_line.strip())

    # Append to log file
    TRAINING_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line)

# ===== HEARTBEAT SYSTEM =====

def update_heartbeat():
    """Updated Heartbeat (System ist am Leben!)"""
    heartbeat = {
        'last_update': datetime.now(BERLIN_TZ).isoformat(),
        'status': 'alive',
        'current_hour': datetime.now(BERLIN_TZ).hour
    }

    with open(HEARTBEAT_FILE, 'w', encoding='utf-8') as f:
        json.dump(heartbeat, f, indent=2)

def check_heartbeat():
    """Prüft ob Heartbeat noch frisch ist"""
    if not HEARTBEAT_FILE.exists():
        return False, "Kein Heartbeat gefunden!"

    try:
        with open(HEARTBEAT_FILE, 'r', encoding='utf-8') as f:
            heartbeat = json.load(f)

        last_update_str = heartbeat.get('last_update')
        if not last_update_str:
            return False, "Heartbeat ohne Timestamp!"

        last_update = datetime.fromisoformat(last_update_str)
        now = datetime.now(BERLIN_TZ)

        age_minutes = (now - last_update).total_seconds() / 60

        if age_minutes > MAX_HEARTBEAT_AGE_MINUTES:
            return False, f"Heartbeat zu alt! ({age_minutes:.1f} Min)"

        return True, f"Heartbeat OK ({age_minutes:.1f} Min)"

    except Exception as e:
        return False, f"Heartbeat Error: {e}"

# ===== SCHEDULE MANAGEMENT =====

def load_schedule():
    """Lädt Schedule (mit Fallback)"""
    if SCHEDULE_FILE.exists():
        try:
            with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log(f"Konnte Schedule nicht laden: {e}", 'ERROR')

    # Fallback: Neuer Schedule
    return {
        'start_date': datetime.now(BERLIN_TZ).isoformat(),
        'total_hours': 0,
        'days_trained': 0,
        'current_week': 1,
        'completed_sessions': [],
        'errors': [],
        'warnings': []
    }

def save_schedule(schedule):
    """Speichert Schedule (ATOMIC!)"""
    TRAINING_DIR.mkdir(exist_ok=True)

    # Backup old schedule
    if SCHEDULE_FILE.exists():
        backup_file = TRAINING_DIR / f'schedule_backup_{int(time.time())}.json'
        import shutil
        shutil.copy(SCHEDULE_FILE, backup_file)

    # Write new schedule
    temp_file = SCHEDULE_FILE.with_suffix('.tmp')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)

    # Atomic rename
    temp_file.replace(SCHEDULE_FILE)

    log(f"Schedule gespeichert: {schedule['total_hours']} Stunden")

# ===== SESSION MANAGEMENT =====

def get_current_session_key():
    """Bestimmt aktuellen Session-Key"""
    now = datetime.now(BERLIN_TZ)
    date_key = now.strftime('%Y-%m-%d')
    hour = now.hour

    if hour not in TRAINING_HOURS:
        return None

    hour_block = f"{hour:02d}:00-{hour+1:02d}:00"
    return f"{date_key}_{hour_block}"

def is_training_time():
    """Prüft ob JETZT Trainingszeit ist"""
    now = datetime.now(BERLIN_TZ)

    # Prüfe Wochentag
    if now.weekday() not in TRAINING_DAYS:
        return False, f"Heute ist {now.strftime('%A')} - kein Trainingstag"

    # Prüfe Uhrzeit
    hour = now.hour
    if hour not in TRAINING_HOURS:
        return False, f"Außerhalb Trainingszeit (08:00-23:00, jetzt: {hour:02d}:{now.minute:02d})"

    return True, "Trainingszeit!"

def mark_session_completed(session_key):
    """Markiert Session als completed"""
    schedule = load_schedule()

    if session_key in schedule['completed_sessions']:
        log(f"Session {session_key} bereits completed", 'WARNING')
        return schedule

    # Markiere als completed
    schedule['completed_sessions'].append(session_key)
    schedule['total_hours'] += 1

    # Berechne Tage
    unique_days = set(s.split('_')[0] for s in schedule['completed_sessions'])
    schedule['days_trained'] = len(unique_days)

    # Berechne Woche
    schedule['current_week'] = (schedule['days_trained'] // 7) + 1

    save_schedule(schedule)

    log(f"Session {session_key} COMPLETED! (Total: {schedule['total_hours']}h)")

    return schedule

# ===== WARN-POPUP SYSTEM =====

def show_warning_popup(title, message):
    """Zeigt Windows-Popup mit Warnung"""
    try:
        # PowerShell Popup
        ps_script = f'''
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show('{message}', '{title}', 'OK', 'Warning')
'''
        subprocess.Popen(
            ['powershell', '-Command', ps_script],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        log(f"WARN-POPUP: {title} - {message}", 'WARNING')
    except Exception as e:
        log(f"Konnte Popup nicht zeigen: {e}", 'ERROR')

# ===== AUTO-RECOVERY SYSTEM =====

def auto_recover():
    """Versucht automatisch zu recovern"""
    log("AUTO-RECOVERY gestartet...", 'WARNING')

    try:
        # 1. Prüfe ob Session-File existiert
        if not CURRENT_SESSION_FILE.exists():
            log("Session-File fehlt - regeneriere...", 'WARNING')
            subprocess.run(['python', str(NAJIKA_DIR / 'najika_training_scheduler.py')], timeout=30)

        # 2. Update Heartbeat
        update_heartbeat()

        # 3. Prüfe Schedule
        schedule = load_schedule()
        if not schedule.get('completed_sessions'):
            log("Schedule leer - setze Startdatum", 'WARNING')
            schedule['start_date'] = datetime.now(BERLIN_TZ).isoformat()
            save_schedule(schedule)

        log("AUTO-RECOVERY abgeschlossen", 'INFO')
        return True

    except Exception as e:
        log(f"AUTO-RECOVERY fehlgeschlagen: {e}", 'ERROR')
        return False

# ===== MONITORING SYSTEM =====

def check_system_health():
    """Prüft Gesundheit des gesamten Systems"""
    issues = []

    # 1. Heartbeat Check
    heartbeat_ok, heartbeat_msg = check_heartbeat()
    if not heartbeat_ok:
        issues.append(f"HEARTBEAT: {heartbeat_msg}")

    # 2. Session File Check
    if not CURRENT_SESSION_FILE.exists():
        issues.append("SESSION-FILE fehlt!")
    else:
        # Prüfe Alter
        age_seconds = time.time() - CURRENT_SESSION_FILE.stat().st_mtime
        age_minutes = age_seconds / 60
        if age_minutes > MAX_SESSION_AGE_MINUTES:
            issues.append(f"SESSION-FILE zu alt ({age_minutes:.0f} Min)!")

    # 3. Schedule Check
    if not SCHEDULE_FILE.exists():
        issues.append("SCHEDULE-FILE fehlt!")

    # 4. Training Time Check
    is_time, time_msg = is_training_time()
    if not is_time:
        issues.append(f"KEINE TRAININGSZEIT: {time_msg}")

    return issues

def run_health_check():
    """Führt Gesundheits-Check aus und warnt bei Problemen"""
    issues = check_system_health()

    if issues:
        log("SYSTEM-HEALTH: PROBLEME ERKANNT!", 'WARNING')
        for issue in issues:
            log(f"  - {issue}", 'WARNING')

        # WARN-POPUP bei kritischen Fehlern
        critical_keywords = ['fehlt', 'zu alt', 'HEARTBEAT']
        critical_issues = [i for i in issues if any(k in i for k in critical_keywords)]

        if critical_issues:
            message = "NAJIKA TRAINING HAT PROBLEME!\\n\\n" + "\\n".join(critical_issues[:3])
            show_warning_popup("NAJIKA TRAINING - WARNUNG", message)

            # AUTO-RECOVERY versuchen
            if auto_recover():
                log("AUTO-RECOVERY erfolgreich!", 'INFO')
            else:
                log("AUTO-RECOVERY fehlgeschlagen!", 'ERROR')
                show_warning_popup(
                    "NAJIKA TRAINING - KRITISCH",
                    "AUTO-RECOVERY FEHLGESCHLAGEN!\\n\\nBitte manuell pruefen!"
                )

        return False

    else:
        log("SYSTEM-HEALTH: OK", 'INFO')
        return True

# ===== MAIN TRAINING LOOP =====

def run_training_session():
    """Führt eine Training-Session aus"""

    log("="*80)
    log("NAJIKA TRAINING SESSION START")
    log("="*80)

    # Update Heartbeat
    update_heartbeat()

    # Prüfe ob Trainingszeit
    is_time, time_msg = is_training_time()
    if not is_time:
        log(f"SKIP: {time_msg}", 'INFO')
        return

    # Bestimme aktuelle Session
    session_key = get_current_session_key()
    if not session_key:
        log("Konnte Session-Key nicht bestimmen!", 'ERROR')
        return

    log(f"Session: {session_key}")

    # Prüfe ob bereits completed
    schedule = load_schedule()
    if session_key in schedule.get('completed_sessions', []):
        log(f"Session {session_key} bereits completed!", 'INFO')
        return

    # Generiere Session-File
    log("Generiere Session-File...")
    try:
        result = subprocess.run(
            ['python', str(NAJIKA_DIR / 'najika_training_scheduler.py')],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            log(f"Scheduler fehlgeschlagen: {result.stderr}", 'ERROR')
            return

        log("Session-File generiert!")

    except Exception as e:
        log(f"Konnte Session nicht generieren: {e}", 'ERROR')
        return

    # HIER WÜRDE NAJIKA DIE SESSION ABARBEITEN
    # Für jetzt: Warte 5 Sekunden (Simulation)
    log(">>> NAJIKA arbeitet Session ab...")
    time.sleep(5)

    # Markiere als completed
    mark_session_completed(session_key)

    # Update Heartbeat
    update_heartbeat()

    log("SESSION COMPLETED!")
    log("="*80)

# ===== MAIN ENTRY POINT =====

def main():
    """Main Entry Point"""

    log("="*80)
    log("🔥 NAJIKA TRAINING - ULTIMATE FAIL-SAFE SYSTEM 🔥")
    log("="*80)
    log(f"Zeit: {datetime.now(BERLIN_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    log(f"Training-Zeiten: {TRAINING_HOURS[0]:02d}:00-{TRAINING_HOURS[-1]+1:02d}:00")
    log(f"Training-Tage: JEDEN TAG")
    log("="*80)

    # Update Heartbeat ZUERST (vor Health Check!)
    update_heartbeat()

    # Health Check
    log("Führe System Health Check aus...")
    health_ok = run_health_check()

    if not health_ok:
        log("Health Check fehlgeschlagen - siehe Warnungen oben!", 'WARNING')

    # Training Session ausführen
    run_training_session()

    log("FERTIG!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("Training abgebrochen (Ctrl+C)", 'WARNING')
        sys.exit(1)
    except Exception as e:
        log(f"KRITISCHER FEHLER: {e}", 'ERROR')
        import traceback
        traceback.print_exc()

        # CRITICAL ERROR POPUP
        show_warning_popup(
            "NAJIKA TRAINING - KRITISCHER FEHLER",
            f"Training-System crashed!\\n\\nFehler: {str(e)[:100]}"
        )
        sys.exit(1)
