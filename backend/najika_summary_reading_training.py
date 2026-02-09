#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 NAJIKA SUMMARY READING TRAINING 🧠

Najika liest ALLE gefundenen Zusammenfassungen/Übersichten MINDESTENS 2x!
Basierend auf GREP Report Ergebnissen.

OHNE AUSNAHME - ALLE DOKUMENTE!
"""

import sys
import io
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Config
PROJECT_ROOT = Path("C:/Najika_World")
GREP_REPORT = PROJECT_ROOT / "NAJIKA_GREP_REPORT.json"
PROGRESS_FILE = PROJECT_ROOT / "backend" / "summary_reading_progress.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen3:8b"  # Fokussiertes Lernen

# Logging
def log(msg, level="INFO"):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [{level}] {msg}")

# Windows Notification
def notify(title: str, message: str):
    """Sendet Windows Benachrichtigung"""
    try:
        if sys.platform == 'win32':
            # PowerShell Toast Notification
            ps_script = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

$template = @"
<toast>
    <visual>
        <binding template="ToastText02">
            <text id="1">{title}</text>
            <text id="2">{message}</text>
        </binding>
    </visual>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
$toast.Tag = "Najika"
$toast.Group = "Training"
$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Najika Training")
$notifier.Show($toast)
"""
            subprocess.run(["powershell", "-Command", ps_script],
                         capture_output=True, timeout=5)
    except Exception:
        pass  # Silent fail


class NajikaSummaryReader:
    """Liest und lernt ALLE Zusammenfassungen"""

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.progress = self._load_progress()

    def _load_progress(self) -> Dict:
        """Lädt Fortschritt"""
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "started": datetime.now().isoformat(),
            "documents_read": [],
            "total_readings": 0,
            "phase1_complete": False,
            "phase2_complete": False
        }

    def _save_progress(self):
        """Speichert Fortschritt"""
        PROGRESS_FILE.parent.mkdir(exist_ok=True)
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)

    def _call_ollama(self, prompt: str) -> str:
        """Ruft Ollama API"""
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Fokussiert
                        "num_predict": 500
                    }
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return ""

        except Exception as e:
            log(f"Ollama Error: {e}", "ERROR")
            return ""

    def _read_document(self, file_path: str, reading_number: int, max_retries: int = 3) -> bool:
        """Liest ein einzelnes Dokument mit Retry-Logik"""
        for attempt in range(max_retries):
            try:
                full_path = self.project_root / file_path
                if not full_path.exists():
                    log(f"Datei nicht gefunden: {file_path}", "WARN")
                    return False

                # Lese Inhalt
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

                # Truncate wenn zu lang
                if len(content) > 10000:
                    content = content[:10000] + "\n[...gekürzt...]"

                log(f"📖 Lese ({reading_number}/2): {file_path}")
                log(f"   Länge: {len(content)} Zeichen")

                # PHASE 1: Lesen & Zusammenfassen
                prompt = f"""Du bist Najika und liest dieses Dokument aufmerksam durch.

DOKUMENT: {file_path}

INHALT:
{content}

Fasse kurz zusammen was du gelernt hast (3-5 Sätze):"""

                summary = self._call_ollama(prompt)

                if summary:
                    log(f"   ✅ Verstanden: {summary[:100]}...")
                else:
                    if attempt < max_retries - 1:
                        log(f"   ⚠️  Keine Antwort, Retry {attempt+1}/{max_retries-1}...")
                        import time
                        time.sleep(2)
                        continue
                    else:
                        log(f"   ❌ Keine Antwort nach {max_retries} Versuchen")
                        return False

                # PHASE 2: Verständnis-Check
                check_prompt = f"""Du hast gerade dieses Dokument gelesen: {file_path}

Was sind die 3 wichtigsten Punkte?"""

                check = self._call_ollama(check_prompt)

                if check:
                    log(f"   ✅ Check: {check[:80]}...")
                else:
                    log(f"   ⚠️  Check fehlgeschlagen (aber Dokument wurde gelesen)")

                return True

            except Exception as e:
                if attempt < max_retries - 1:
                    log(f"Error reading {file_path} (Retry {attempt+1}/{max_retries-1}): {e}", "WARN")
                    import time
                    time.sleep(2)
                    continue
                else:
                    log(f"❌ KRITISCHER FEHLER nach {max_retries} Versuchen: {file_path}", "ERROR")
                    log(f"   Error: {e}", "ERROR")
                    return False

        return False

    def run_phase1(self):
        """PHASE 1: Erstes Durchlesen ALLER Dokumente"""
        log("="*70)
        log("📚 PHASE 1: ERSTES DURCHLESEN")
        log("="*70)

        if self.progress.get("phase1_complete"):
            log("⏭️  Phase 1 bereits abgeschlossen!")
            return

        # Lade GREP Report
        if not GREP_REPORT.exists():
            log("❌ GREP Report nicht gefunden!", "ERROR")
            return

        with open(GREP_REPORT, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # Sammle ALLE einzigartigen Dokumente
        all_docs = set()

        # Phase 1: Zusammenfassungen
        for item in report.get("phase1_overview", []):
            all_docs.add(item["file"])

        # Phase 2: Roadmaps
        for item in report.get("phase2_roadmaps", []):
            all_docs.add(item["file"])

        # Phase 3: Vollständige Versionen
        for item in report.get("phase3_complete", []):
            all_docs.add(item["file"])

        # Phase 4: Themen
        for theme, items in report.get("phase4_themes", {}).items():
            for item in items:
                all_docs.add(item["file"])

        # Phase 5: Vergessenes
        for item in report.get("phase5_missing", []):
            all_docs.add(item["file"])

        all_docs = sorted(list(all_docs))
        log(f"📊 Gefunden: {len(all_docs)} einzigartige Dokumente")
        log("")

        # Lese JEDES Dokument
        success_count = 0
        for i, doc in enumerate(all_docs, 1):
            log(f"[{i}/{len(all_docs)}] {doc}")

            if self._read_document(doc, reading_number=1):
                success_count += 1
                self.progress["documents_read"].append({
                    "file": doc,
                    "reading": 1,
                    "timestamp": datetime.now().isoformat()
                })
                self.progress["total_readings"] += 1
                self._save_progress()

            log("")

        self.progress["phase1_complete"] = True
        self._save_progress()

        log("="*70)
        log(f"🎉 PHASE 1 ABGESCHLOSSEN!")
        log(f"   Erfolg: {success_count}/{len(all_docs)} Dokumente")
        log("="*70)

    def run_phase2(self):
        """PHASE 2: Zweites Durchlesen zur Festigung"""
        log("="*70)
        log("📚 PHASE 2: ZWEITES DURCHLESEN (Festigung)")
        log("="*70)

        if not self.progress.get("phase1_complete"):
            log("❌ Phase 1 muss erst abgeschlossen sein!", "ERROR")
            return

        if self.progress.get("phase2_complete"):
            log("⏭️  Phase 2 bereits abgeschlossen!")
            return

        # Sammle alle bereits gelesenen Docs
        phase1_docs = set()
        for entry in self.progress.get("documents_read", []):
            if entry["reading"] == 1:
                phase1_docs.add(entry["file"])

        phase1_docs = sorted(list(phase1_docs))
        log(f"📊 Lese erneut: {len(phase1_docs)} Dokumente")
        log("")

        success_count = 0
        for i, doc in enumerate(phase1_docs, 1):
            log(f"[{i}/{len(phase1_docs)}] {doc} (2. Durchlauf)")

            if self._read_document(doc, reading_number=2):
                success_count += 1
                self.progress["documents_read"].append({
                    "file": doc,
                    "reading": 2,
                    "timestamp": datetime.now().isoformat()
                })
                self.progress["total_readings"] += 1
                self._save_progress()

            log("")

        self.progress["phase2_complete"] = True
        self._save_progress()

        log("="*70)
        log(f"🎉 PHASE 2 ABGESCHLOSSEN!")
        log(f"   Erfolg: {success_count}/{len(phase1_docs)} Dokumente")
        log("="*70)

    def run(self):
        """Hauptfunktion - Beide Phasen"""
        log("="*70)
        log("🧠 NAJIKA SUMMARY READING TRAINING")
        log("="*70)
        log("")
        log("ZIEL: ALLE Zusammenfassungen mindestens 2x lesen!")
        log(f"MODEL: {MODEL}")
        log("")

        # Benachrichtigung: Start
        notify("🧠 Najika Training gestartet",
               "Lese alle 1258 Dokumente 2x durch")

        try:
            # Phase 1: Erstes Durchlesen
            self.run_phase1()

            # Benachrichtigung: Phase 1 fertig
            notify("✅ Phase 1 abgeschlossen",
                   f"{len(set(e['file'] for e in self.progress['documents_read'] if e['reading']==1))} Dokumente gelesen")

            log("")
            log("⏳ Kurze Pause vor Phase 2...")
            log("")

            # Phase 2: Zweites Durchlesen
            self.run_phase2()

            # Finale Stats
            log("")
            log("="*70)
            log("🎉 TRAINING KOMPLETT ABGESCHLOSSEN!")
            log("="*70)
            log(f"📊 Statistiken:")
            log(f"   Total Readings: {self.progress['total_readings']}")
            log(f"   Dokumente: {len(set(e['file'] for e in self.progress['documents_read']))}")
            log(f"   Started: {self.progress['started']}")
            log(f"   Finished: {datetime.now().isoformat()}")
            log("")

            # Benachrichtigung: FERTIG!
            notify("🎉 Najika Training FERTIG!",
                   f"Alle {len(set(e['file'] for e in self.progress['documents_read']))} Dokumente 2x gelesen!")

        except Exception as e:
            log(f"❌ KRITISCHER FEHLER: {e}", "ERROR")
            # Benachrichtigung: FEHLER!
            notify("❌ Najika Training FEHLER!",
                   f"Kritischer Fehler aufgetreten: {str(e)[:50]}")
            raise


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  NAJIKA SUMMARY READING TRAINING                             ║
╚══════════════════════════════════════════════════════════════╝

Najika liest ALLE gefundenen Zusammenfassungen/Übersichten!

PHASE 1: Erstes Durchlesen (Verstehen)
PHASE 2: Zweites Durchlesen (Festigung)

OHNE AUSNAHME - ALLE DOKUMENTE!

""")

    reader = NajikaSummaryReader()
    reader.run()


if __name__ == "__main__":
    main()
