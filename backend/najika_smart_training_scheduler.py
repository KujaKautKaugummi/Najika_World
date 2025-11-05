#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA SMART TRAINING SCHEDULER
Automatisches GPU-Training mit intelligentem Pause-System
"""
import sys
import io
import json
from pathlib import Path
from datetime import datetime, time
import pytz

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NAJIKA_DIR = Path('C:/Najika-World/backend')
CONFIG_FILE = NAJIKA_DIR / 'training_config.json'
PAUSE_FILE = NAJIKA_DIR / 'training_pause.json'

# Berlin Timezone
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# ========================================
# TRAINING SCHEDULE (KONFIGUARIERT!)
# ========================================

# NACHT-TRAINING (IMMER! 7 TAGE DIE WOCHE!)
NIGHT_TRAINING = {
    "enabled": True,
    "start": time(0, 0),   # 00:00 (Mitternacht)
    "end": time(8, 0),     # 08:00
    "days": [0, 1, 2, 3, 4, 5, 6],  # Mo-So (JEDEN TAG!)
    "type": "GPU_LORA",
    "priority": "HIGH"
}

# TAG-TRAINING (NUR MONTAG-FREITAG, 8-15 UHR, PAUSIERBAR!)
DAY_TRAINING = {
    "enabled": True,
    "start": time(8, 0),   # 08:00
    "end": time(15, 0),    # 15:00
    "days": [0, 1, 2, 3, 4],  # Mo-Fr (NUR WOCHENTAGS!)
    "type": "GPU_LORA",
    "priority": "MEDIUM",
    "pausable": True  # ← KANN PAUSIERT WERDEN!
}

def get_berlin_time():
    """Aktuelle Berlin Zeit"""
    return datetime.now(BERLIN_TZ)

def load_pause_status():
    """Lädt Pause-Status"""
    if PAUSE_FILE.exists():
        try:
            with open(PAUSE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass

    return {
        "day_training_paused": False,
        "paused_until": None,
        "reason": None
    }

def save_pause_status(status):
    """Speichert Pause-Status"""
    with open(PAUSE_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2)

def pause_day_training(reason="Urlaub/Frei", until_date=None):
    """Pausiert Tag-Training (8-15 Uhr)

    Args:
        reason: Grund (z.B. "Urlaub", "Frei", "PC genutzt")
        until_date: Bis wann pausiert (None = bis manuell aktiviert)
    """
    status = {
        "day_training_paused": True,
        "paused_at": datetime.now(BERLIN_TZ).isoformat(),
        "paused_until": until_date.isoformat() if until_date else None,
        "reason": reason
    }
    save_pause_status(status)

    print("=" * 60)
    print("⏸️  TAG-TRAINING PAUSIERT!")
    print("=" * 60)
    print(f"Grund: {reason}")
    print(f"Pausiert bis: {until_date if until_date else 'Manuell aktiviert'}")
    print("")
    print("NACHT-TRAINING (00:00-08:00) läuft weiter!")
    print("")
    print("Zum Aktivieren:")
    print("  python najika_smart_training_scheduler.py --resume")
    print("=" * 60)

def resume_day_training():
    """Aktiviert Tag-Training wieder"""
    status = {
        "day_training_paused": False,
        "resumed_at": datetime.now(BERLIN_TZ).isoformat(),
        "paused_until": None,
        "reason": None
    }
    save_pause_status(status)

    print("=" * 60)
    print("▶️  TAG-TRAINING AKTIVIERT!")
    print("=" * 60)
    print("Training läuft wieder:")
    print("  - NACHT: 00:00-08:00 (7 Tage)")
    print("  - TAG: 08:00-15:00 (Mo-Fr)")
    print("=" * 60)

def is_training_time():
    """Prüft ob JETZT Trainingszeit ist"""
    now = get_berlin_time()
    current_time = now.time()
    current_day = now.weekday()

    pause_status = load_pause_status()

    # ========================================
    # 1. NACHT-TRAINING (IMMER!)
    # ========================================
    if (NIGHT_TRAINING["start"] <= current_time < NIGHT_TRAINING["end"] and
        current_day in NIGHT_TRAINING["days"]):
        return True, "NACHT-TRAINING (00:00-08:00)", NIGHT_TRAINING["type"]

    # ========================================
    # 2. TAG-TRAINING (NUR WENN NICHT PAUSIERT!)
    # ========================================
    if (DAY_TRAINING["enabled"] and
        DAY_TRAINING["start"] <= current_time < DAY_TRAINING["end"] and
        current_day in DAY_TRAINING["days"]):

        # Prüfe Pause-Status
        if pause_status.get("day_training_paused", False):
            # Prüfe ob Pause abgelaufen
            paused_until = pause_status.get("paused_until")
            if paused_until:
                paused_until_dt = datetime.fromisoformat(paused_until)
                if now >= paused_until_dt:
                    # Pause abgelaufen → automatisch aktivieren
                    resume_day_training()
                    return True, "TAG-TRAINING (08:00-15:00)", DAY_TRAINING["type"]

            # Pause aktiv
            reason = pause_status.get("reason", "Unbekannt")
            return False, f"TAG-TRAINING PAUSIERT ({reason})", None

        # Nicht pausiert → Training läuft
        return True, "TAG-TRAINING (08:00-15:00)", DAY_TRAINING["type"]

    # Außerhalb aller Trainingszeiten
    return False, "Keine Trainingszeit (außerhalb 00:00-08:00 und 08:00-15:00)", None

def check_gpu_available():
    """Prüft ob GPU verfügbar ist"""
    try:
        import torch
        if not torch.cuda.is_available():
            return False, "Keine CUDA GPU gefunden"

        free_mem = torch.cuda.mem_get_info()[0] / 1024**3  # GB
        if free_mem < 6.0:
            return False, f"Zu wenig VRAM frei ({free_mem:.1f}GB, brauche 6GB)"

        return True, f"GPU OK ({free_mem:.1f}GB frei)"
    except ImportError:
        return False, "PyTorch nicht installiert"

def start_training_session():
    """Startet Training-Session"""
    print("\n" + "=" * 60)
    print("🚀 NAJIKA GPU-TRAINING START")
    print("=" * 60)

    now = get_berlin_time()
    print(f"Zeit: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Wochentag: {now.strftime('%A')}")
    print("")

    # Prüfe Trainingszeit
    is_time, session_type, training_type = is_training_time()
    print(f"Status: {session_type}")

    if not is_time:
        print("\n❌ Keine Trainingszeit - komm später wieder!")
        return False

    # Prüfe GPU
    gpu_ok, gpu_msg = check_gpu_available()
    print(f"GPU: {gpu_msg}")

    if not gpu_ok:
        print("\n❌ GPU nicht verfügbar - Training abgebrochen!")
        return False

    print("\n✅ Alle Checks OK - starte Training...")
    print(f"Training-Typ: {training_type}")
    print(f"Session: {session_type}")
    print("=" * 60)

    # Starte tatsächliches Training
    if training_type == "GPU_LORA":
        return start_lora_training()

    return False

def start_lora_training():
    """Startet LoRA Training"""
    try:
        from najika_lora_training_3b import NajikaLoRATrainer3B

        print("\n📚 Starte LoRA Training (3B Model)...")

        trainer = NajikaLoRATrainer3B()

        # Prüfe ob genug Daten vorhanden
        dataset = trainer.prepare_training_data(min_samples=10)
        if dataset is None:
            print("❌ Zu wenig Training-Daten!")
            return False

        # Training durchführen
        print("\n🎓 Training läuft...")
        success = trainer.train(dataset)

        if success:
            print("\n✅ Training erfolgreich abgeschlossen!")
            return True
        else:
            print("\n❌ Training fehlgeschlagen!")
            return False

    except Exception as e:
        print(f"\n❌ Training-Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_status():
    """Zeigt aktuellen Training-Status"""
    print("\n" + "=" * 60)
    print("📊 NAJIKA TRAINING STATUS")
    print("=" * 60)

    now = get_berlin_time()
    print(f"Zeit: {now.strftime('%Y-%m-%d %H:%M:%S (%A)')}")
    print("")

    # Nacht-Training
    print("🌙 NACHT-TRAINING:")
    print(f"  Zeit: 00:00-08:00 (JEDEN TAG!)")
    print(f"  Status: ✅ AKTIV")
    print(f"  Typ: GPU LoRA Training")
    print("")

    # Tag-Training
    pause_status = load_pause_status()
    print("☀️  TAG-TRAINING:")
    print(f"  Zeit: 08:00-15:00 (Mo-Fr)")

    if pause_status.get("day_training_paused", False):
        reason = pause_status.get("reason", "Unbekannt")
        paused_until = pause_status.get("paused_until")
        print(f"  Status: ⏸️  PAUSIERT")
        print(f"  Grund: {reason}")
        print(f"  Bis: {paused_until if paused_until else 'Manuell aktiviert'}")
        print("")
        print("  Zum Aktivieren:")
        print("    python najika_smart_training_scheduler.py --resume")
    else:
        print(f"  Status: ✅ AKTIV")
        print(f"  Typ: GPU LoRA Training")
        print("")
        print("  Zum Pausieren:")
        print("    python najika_smart_training_scheduler.py --pause")

    print("=" * 60)

    # Aktuelle Session
    is_time, session_type, training_type = is_training_time()
    print(f"\nJETZT: {session_type}")
    print("=" * 60)

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "--pause":
            pause_day_training(reason="Manuell pausiert")

        elif cmd == "--resume":
            resume_day_training()

        elif cmd == "--status":
            print_status()

        elif cmd == "--train":
            start_training_session()

        else:
            print("Unbekannter Befehl!")
            print("")
            print("Verfügbare Befehle:")
            print("  --pause    Pausiert Tag-Training (08:00-15:00)")
            print("  --resume   Aktiviert Tag-Training wieder")
            print("  --status   Zeigt aktuellen Status")
            print("  --train    Startet Training (wenn Zeit)")
    else:
        # Kein Argument → zeige Status
        print_status()
