#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Najika Training Tasks Manager
Listet und verwaltet Windows Scheduled Tasks
"""

import subprocess
import sys
import re

def run_cmd(cmd):
    """Führt Windows CMD Befehl aus und gibt Output zurück"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='cp850'  # Windows console encoding
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def list_najika_tasks():
    """Liste alle Najika-Tasks"""
    print("\n" + "="*60)
    print(" NAJIKA SCHEDULED TASKS")
    print("="*60 + "\n")

    # Hole alle Tasks
    code, out, err = run_cmd('schtasks /Query /FO LIST')

    if code != 0:
        print(f"❌ Fehler beim Abrufen der Tasks: {err}")
        return []

    # Parse Output für Najika-Tasks
    tasks = []
    current_task = {}

    for line in out.split('\n'):
        line = line.strip()

        if line.startswith('Taskname:'):
            if current_task:
                tasks.append(current_task)
            current_task = {'name': line.split(':', 1)[1].strip()}
        elif line.startswith('Status:'):
            current_task['status'] = line.split(':', 1)[1].strip()
        elif line.startswith('Nächste Ausführungszeit:'):
            current_task['next_run'] = line.split(':', 1)[1].strip()

    if current_task:
        tasks.append(current_task)

    # Filter für Najika
    najika_tasks = [t for t in tasks if 'Najika' in t.get('name', '')]

    if najika_tasks:
        print(f"✅ {len(najika_tasks)} Najika-Tasks gefunden:\n")

        for i, task in enumerate(najika_tasks, 1):
            name = task.get('name', '').split('\\')[-1]  # Nur Taskname ohne Pfad
            status = task.get('status', 'Unknown')
            next_run = task.get('next_run', 'Unknown')

            print(f"  {i}. {name}")
            print(f"     Status: {status}")
            print(f"     Nächster Lauf: {next_run}")
            print()
    else:
        print("✅ Keine Najika-Tasks gefunden!")

    return najika_tasks

def delete_all_najika_tasks():
    """Lösche alle Najika-Tasks"""
    print("\n" + "="*60)
    print(" LÖSCHE ALLE NAJIKA TASKS")
    print("="*60 + "\n")

    tasks = list_najika_tasks()

    if not tasks:
        print("Nichts zu löschen!")
        return

    print(f"⚠️  ACHTUNG: {len(tasks)} Tasks werden gelöscht!\n")

    confirm = input("Fortfahren? (J/N): ").strip().upper()

    if confirm != 'J':
        print("❌ Abgebrochen.")
        return

    print("\nLösche Tasks...\n")

    deleted = 0
    for task in tasks:
        task_name = task.get('name', '')

        if not task_name:
            continue

        code, out, err = run_cmd(f'schtasks /Delete /TN "{task_name}" /F')

        if code == 0:
            print(f"  ✓ Gelöscht: {task_name.split('\\')[-1]}")
            deleted += 1
        else:
            print(f"  ✗ Fehler bei: {task_name.split('\\')[-1]}")

    print(f"\n✅ {deleted} Tasks gelöscht!")

def create_training_tasks():
    """Erstelle die 2 richtigen Training-Tasks"""
    print("\n" + "="*60)
    print(" ERSTELLE TRAINING TASKS")
    print("="*60 + "\n")

    # Task 1: NACHT (00:00, täglich, 8h limit)
    print("Erstelle NajikaTrainingNacht...")

    cmd1 = '''schtasks /Create /TN "NajikaTrainingNacht" /TR "python C:\\Najika\\backend\\najika_smart_training_scheduler.py --train" /SC DAILY /ST 00:00 /F'''

    code, out, err = run_cmd(cmd1)

    if code == 0:
        print("  ✓ NajikaTrainingNacht erstellt (00:00, täglich)")
    else:
        print(f"  ✗ Fehler: {err}")

    # Task 2: TAG (08:00, Mo-Fr, 7h limit)
    print("Erstelle NajikaTrainingTag...")

    # Windows schtasks unterstützt /MO mit WEEKLY nicht direkt
    # Wir müssen PowerShell verwenden für komplexere Schedules
    ps_cmd = '''powershell -Command "$action = New-ScheduledTaskAction -Execute 'python' -Argument 'C:\\Najika\\backend\\najika_smart_training_scheduler.py --train' -WorkingDirectory 'C:\\Najika\\backend'; $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 08:00; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 7); Register-ScheduledTask -TaskName 'NajikaTrainingTag' -Action $action -Trigger $trigger -Settings $settings -Force"'''

    code, out, err = run_cmd(ps_cmd)

    if code == 0:
        print("  ✓ NajikaTrainingTag erstellt (08:00, Mo-Fr)")
    else:
        print(f"  ✗ Fehler: {err}")

    print("\n✅ Tasks erstellt!")

def main():
    """Main Menu"""
    while True:
        print("\n" + "="*60)
        print(" NAJIKA TASK MANAGER")
        print("="*60)
        print("\n1. Tasks auflisten")
        print("2. ALLE Najika-Tasks löschen")
        print("3. Richtige Training-Tasks erstellen")
        print("4. KOMPLETT-CLEANUP (löschen + neu erstellen)")
        print("5. Beenden\n")

        choice = input("Wahl: ").strip()

        if choice == '1':
            list_najika_tasks()
        elif choice == '2':
            delete_all_najika_tasks()
        elif choice == '3':
            create_training_tasks()
        elif choice == '4':
            delete_all_najika_tasks()
            create_training_tasks()
            print("\n✅ CLEANUP ABGESCHLOSSEN!")
            list_najika_tasks()
        elif choice == '5':
            print("\n👋 Tschüss!")
            break
        else:
            print("\n❌ Ungültige Wahl!")

        input("\nEnter drücken...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Abgebrochen!")
        sys.exit(0)
