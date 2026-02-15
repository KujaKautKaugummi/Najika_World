#!/usr/bin/env python3
"""
NAJIKA WORLD - START ALL SERVERS
================================
Startet beide Backend-Server parallel:
- Flask Server (najika_server.py) auf Port 8000 - Chat, TTS, Living System
- FastAPI Server (main_fastapi.py) auf Port 8001 - Card Game, Dice Monsters, etc.

Beide Server laufen nur auf 127.0.0.1 (Zero-Trust!)
"""

import subprocess
import sys
import os
import time
import signal

# Setze Working Directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BACKEND_DIR)

# Server-Prozesse
processes = []

def cleanup(signum=None, frame=None):
    """Beendet alle Server-Prozesse sauber"""
    print("\n[SHUTDOWN] Beende alle Server...")
    for name, proc in processes:
        if proc and proc.poll() is None:
            print(f"  - Beende {name}...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    print("[SHUTDOWN] Alle Server beendet.")
    sys.exit(0)

# Signal Handler fuer sauberes Beenden
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def main():
    print("=" * 70)
    print("  NAJIKA WORLD - MULTI-SERVER STARTUP")
    print("=" * 70)
    print()

    # 1. Flask Server (Chat, TTS, Living System)
    print("[1/2] Starte Flask Server (Port 8000)...")
    flask_cmd = [sys.executable, "najika_server.py"]
    flask_proc = subprocess.Popen(
        flask_cmd,
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    processes.append(("Flask (8000)", flask_proc))
    time.sleep(2)  # Warte kurz

    if flask_proc.poll() is None:
        print("  [OK] Flask Server gestartet!")
    else:
        print("  [ERROR] Flask Server konnte nicht gestartet werden!")
        cleanup()

    # 2. FastAPI Server (Card Game, Dice Monsters, etc.)
    print("[2/2] Starte FastAPI Server (Port 8001)...")
    # Wichtig: FastAPI muss aus dem PROJECT_ROOT gestartet werden (nicht backend!)
    # weil die Imports "from backend.config" erwarten
    PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
    fastapi_cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main_fastapi:app",
        "--host", "127.0.0.1",
        "--port", "8001",
        "--reload"
    ]
    fastapi_proc = subprocess.Popen(
        fastapi_cmd,
        cwd=PROJECT_ROOT,  # Wichtig: Aus Project Root starten!
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    processes.append(("FastAPI (8001)", fastapi_proc))
    time.sleep(3)  # Warte kurz

    if fastapi_proc.poll() is None:
        print("  [OK] FastAPI Server gestartet!")
    else:
        print("  [ERROR] FastAPI Server konnte nicht gestartet werden!")
        cleanup()

    print()
    print("=" * 70)
    print("  ALLE SERVER LAUFEN!")
    print("=" * 70)
    print()
    print("  Flask Server:   http://127.0.0.1:8001")
    print("    - Chat API, TTS, Living System, Battle")
    print()
    print("  FastAPI Server: http://127.0.0.1:8001")
    print("    - Card Game (/api/cards)")
    print("    - Dice Monsters (/api/dice)")
    print("    - Housing (/api/housing)")
    print("    - Farming (/api/farming)")
    print("    - API Docs: http://127.0.0.1:8001/docs")
    print()
    print("  Digivice:       http://127.0.0.1:8001")
    print()
    print("  Druecke CTRL+C zum Beenden")
    print("=" * 70)
    print()

    # Output beider Server anzeigen
    import select
    import threading

    def read_output(name, proc):
        """Liest Output eines Prozesses"""
        try:
            for line in iter(proc.stdout.readline, ''):
                if line:
                    print(f"[{name}] {line.rstrip()}")
                if proc.poll() is not None:
                    break
        except:
            pass

    # Starte Output-Reader Threads
    flask_thread = threading.Thread(target=read_output, args=("Flask", flask_proc), daemon=True)
    fastapi_thread = threading.Thread(target=read_output, args=("FastAPI", fastapi_proc), daemon=True)

    flask_thread.start()
    fastapi_thread.start()

    # Warte auf Beendigung
    try:
        while True:
            # Pruefe ob ein Server abgestuerzt ist
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"\n[WARNING] {name} ist beendet worden (Code: {proc.returncode})")
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
