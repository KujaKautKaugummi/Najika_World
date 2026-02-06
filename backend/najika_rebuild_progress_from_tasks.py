#!/usr/bin/env python3
"""
REBUILD TRAINING PROGRESS FROM WINDOWS TASK SCHEDULER
Rekonstruiert verlorene Training-Sessions aus Task Scheduler History
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import re

NAJIKA_DIR = Path('C:/Najika_World')
TRAINING_DIR = NAJIKA_DIR / 'training'
SCHEDULE_FILE = TRAINING_DIR / 'schedule.json'

def get_task_history(task_name):
    """Holt History eines Tasks aus Task Scheduler"""
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             f'Get-ScheduledTaskInfo -TaskName "{task_name}" | Select-Object LastRunTime, LastTaskResult'],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.strip()

        # Parse Output
        lines = output.split('\n')
        last_run = None
        last_result = None

        for line in lines:
            if 'LastRunTime' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    time_str = parts[1].strip()
                    try:
                        last_run = datetime.strptime(time_str, '%d.%m.%Y %H:%M:%S')
                    except:
                        pass
            elif 'LastTaskResult' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    last_result = parts[1].strip()

        return last_run, last_result
    except Exception as e:
        print(f"[ERROR] Konnte History für {task_name} nicht holen: {e}")
        return None, None

def rebuild_progress():
    """Rekonstruiert Progress aus allen Tasks"""

    print('='*80)
    print('NAJIKA TRAINING - PROGRESS REBUILD')
    print('='*80)
    print()

    # Alle Training Tasks
    tasks = [
        'NajikaTraining09',
        'NajikaTraining10',
        'NajikaTraining11',
        'NajikaTraining12',
        'NajikaTraining13',
        'NajikaTraining16h'
    ]

    print('[INFO] Analysiere Task Scheduler History...')
    print()

    completed_sessions = []

    for task in tasks:
        print(f'[CHECK] {task}...')
        last_run, last_result = get_task_history(task)

        if last_run:
            print(f'  -> Letzte Ausfuehrung: {last_run.strftime("%Y-%m-%d %H:%M:%S")}')
            print(f'  -> Ergebnis: {last_result}')

            # Bestimme Stunden-Block aus Task-Name
            if '09' in task:
                hour_block = '09:00-10:00'
            elif '10' in task:
                hour_block = '10:00-11:00'
            elif '11' in task:
                hour_block = '11:00-12:00'
            elif '12' in task:
                hour_block = '12:00-13:00'
            elif '13' in task:
                hour_block = '13:00-14:00'
            elif '16h' in task:
                hour_block = '20:00-21:00'
            else:
                continue

            # Erstelle Session-Key
            date_key = last_run.strftime('%Y-%m-%d')
            session_key = f"{date_key}_{hour_block}"

            if session_key not in completed_sessions:
                completed_sessions.append(session_key)
        else:
            print(f'  -> Keine History gefunden')

        print()

    # Sortiere Sessions
    completed_sessions.sort()

    # Berechne Stats
    total_hours = len(completed_sessions)
    unique_days = set(s.split('_')[0] for s in completed_sessions)
    days_trained = len(unique_days)
    current_week = (days_trained // 5) + 1 if days_trained > 0 else 1

    # Erstelle Schedule
    schedule = {
        'start_date': completed_sessions[0].split('_')[0] if completed_sessions else datetime.now().isoformat(),
        'total_hours': total_hours,
        'days_trained': days_trained,
        'current_week': current_week,
        'completed_sessions': completed_sessions,
        'rebuilt_from_tasks': True,
        'rebuild_date': datetime.now().isoformat()
    }

    # Speichern
    TRAINING_DIR.mkdir(exist_ok=True)
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)

    print('='*80)
    print('REBUILD ABGESCHLOSSEN!')
    print('='*80)
    print()
    print(f'OK Gefundene Sessions: {total_hours}')
    print(f'OK Trainings-Tage: {days_trained}')
    print(f'OK Aktuelle Woche: {current_week}')
    print()
    print(f'Sessions pro Tag: {total_hours / days_trained if days_trained > 0 else 0:.1f}')
    print()
    print(f'Gespeichert: {SCHEDULE_FILE}')
    print()

    # Zeige letzte 5 Sessions
    if completed_sessions:
        print('Letzte Sessions:')
        for session in completed_sessions[-5:]:
            date, time_block = session.split('_')
            print(f'  OK {date} {time_block}')

    print()
    return schedule

if __name__ == '__main__':
    try:
        rebuild_progress()
    except Exception as e:
        print(f'[ERROR] Rebuild fehlgeschlagen: {e}')
        import traceback
        traceback.print_exc()
