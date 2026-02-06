#!/usr/bin/env python3
"""
NAJIKA THOUGHT ORGANIZER - TERMINAL UI
Intelligente Gedanken-Organisation mit Baustein-System
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Versuche curses zu importieren (für Terminal UI)
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    print("[WARNING] curses nicht verfügbar - nutze einfache CLI Version")
    CURSES_AVAILABLE = False

# Najika Integration
try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ===== KONFIGURATION =====

DATA_DIR = Path("C:/Najika_World/thought_organizer")
DATA_DIR.mkdir(exist_ok=True)

BAUSTEIN_DB = DATA_DIR / "bausteine.json"
KERN_FILE = DATA_DIR / "KERN.json"
EXPORT_MD = DATA_DIR / "KONZEPT_AKTUELL.md"
EXPORT_JSON = DATA_DIR / "KONZEPT_AKTUELL.json"

# ===== BAUSTEIN-KLASSE =====

class Baustein:
    """Repräsentiert einen Gedanken-Baustein"""

    def __init__(self, thema, inhalt, quelle="Manuell", status="OPTIONAL", baustein_id=None):
        self.id = baustein_id or self._generate_id()
        self.thema = thema
        self.inhalt = inhalt
        self.quelle = quelle
        self.status = status  # KERN oder OPTIONAL
        self.timestamp = datetime.now().isoformat()

    def _generate_id(self):
        """Generiert eindeutige ID"""
        return f"BS_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    def to_dict(self):
        """Konvertiert zu Dictionary"""
        return {
            'id': self.id,
            'thema': self.thema,
            'inhalt': self.inhalt,
            'quelle': self.quelle,
            'status': self.status,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data):
        """Erstellt Baustein aus Dictionary"""
        return Baustein(
            thema=data['thema'],
            inhalt=data['inhalt'],
            quelle=data.get('quelle', 'Manuell'),
            status=data.get('status', 'OPTIONAL'),
            baustein_id=data.get('id')
        )

# ===== BAUSTEIN-MANAGER =====

class BausteinManager:
    """Verwaltet alle Bausteine"""

    def __init__(self):
        self.bausteine = []
        self.kategorien = {}  # {Thema: [Baustein, ...]}
        self.load()

    def load(self):
        """Lädt Bausteine aus Datei"""
        if BAUSTEIN_DB.exists():
            with open(BAUSTEIN_DB, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.bausteine = [Baustein.from_dict(b) for b in data]
                self._update_kategorien()

    def save(self):
        """Speichert Bausteine"""
        with open(BAUSTEIN_DB, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in self.bausteine], f, indent=2, ensure_ascii=False)

    def _update_kategorien(self):
        """Aktualisiert Kategorie-Index"""
        self.kategorien = {}
        for baustein in self.bausteine:
            if baustein.thema not in self.kategorien:
                self.kategorien[baustein.thema] = []
            self.kategorien[baustein.thema].append(baustein)

    def add_baustein(self, baustein):
        """Fügt Baustein hinzu"""
        self.bausteine.append(baustein)
        self._update_kategorien()
        self.save()

    def remove_baustein(self, baustein_id):
        """Entfernt Baustein"""
        self.bausteine = [b for b in self.bausteine if b.id != baustein_id]
        self._update_kategorien()
        self.save()

    def update_baustein(self, baustein_id, **updates):
        """Aktualisiert Baustein"""
        for baustein in self.bausteine:
            if baustein.id == baustein_id:
                for key, value in updates.items():
                    setattr(baustein, key, value)
                break
        self._update_kategorien()
        self.save()

    def merge_bausteine(self, id1, id2):
        """Fusioniert zwei Bausteine"""
        b1 = next((b for b in self.bausteine if b.id == id1), None)
        b2 = next((b for b in self.bausteine if b.id == id2), None)

        if not b1 or not b2:
            return False

        # Kombiniere Inhalte
        b1.inhalt = f"{b1.inhalt}\n\n---\n\n{b2.inhalt}"
        b1.quelle = f"{b1.quelle} + {b2.quelle}"

        # Entferne b2
        self.remove_baustein(id2)
        self.save()
        return True

    def set_kern(self, baustein_id):
        """Markiert Baustein als KERN"""
        self.update_baustein(baustein_id, status='KERN')

    def set_optional(self, baustein_id):
        """Markiert Baustein als OPTIONAL"""
        self.update_baustein(baustein_id, status='OPTIONAL')

    def export_markdown(self):
        """Exportiert als Markdown"""
        lines = []
        lines.append("# NAJIKA KONZEPT - BAUSTEIN-ÜBERSICHT")
        lines.append(f"**Stand:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Nach Kategorien gruppiert
        for thema in sorted(self.kategorien.keys()):
            lines.append(f"## {thema.upper()}")
            lines.append("")

            kern_bausteine = [b for b in self.kategorien[thema] if b.status == 'KERN']
            optional_bausteine = [b for b in self.kategorien[thema] if b.status == 'OPTIONAL']

            # KERN zuerst
            if kern_bausteine:
                lines.append("### ● KERN (fest)")
                lines.append("")
                for baustein in kern_bausteine:
                    lines.append(f"**Quelle:** {baustein.quelle}")
                    lines.append("")
                    lines.append(baustein.inhalt)
                    lines.append("")
                    lines.append("---")
                    lines.append("")

            # OPTIONAL danach
            if optional_bausteine:
                lines.append("### ○ OPTIONAL")
                lines.append("")
                for baustein in optional_bausteine:
                    lines.append(f"**Quelle:** {baustein.quelle}")
                    lines.append("")
                    lines.append(baustein.inhalt)
                    lines.append("")
                    lines.append("---")
                    lines.append("")

        EXPORT_MD.write_text('\n'.join(lines), encoding='utf-8')
        return EXPORT_MD

    def export_json(self):
        """Exportiert als JSON (für Najika/KIs)"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'kategorien': {}
        }

        for thema, bausteine in self.kategorien.items():
            data['kategorien'][thema] = {
                'kern': [b.to_dict() for b in bausteine if b.status == 'KERN'],
                'optional': [b.to_dict() for b in bausteine if b.status == 'OPTIONAL']
            }

        EXPORT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return EXPORT_JSON

# ===== NAJIKA FILTER =====

def najika_filter_text(text, filename="input"):
    """Najika filtert Text und erstellt Bausteine"""

    if not OLLAMA_AVAILABLE:
        # Fallback: Einfache Zeilenweise Extraktion
        return simple_filter(text, filename)

    # Chunking wenn zu groß
    if len(text) > 40000:
        chunks = [text[i:i+40000] for i in range(0, len(text), 40000)]
        all_bausteine = []

        for i, chunk in enumerate(chunks, 1):
            print(f"  Najika filtert Chunk {i}/{len(chunks)}...")
            bausteine = ask_najika_to_organize(chunk, filename, chunk_num=i)
            all_bausteine.extend(bausteine)

        return all_bausteine
    else:
        return ask_najika_to_organize(text, filename)

def ask_najika_to_organize(text, filename, chunk_num=None):
    """Fragt Najika (Ollama) Text zu organisieren"""

    chunk_info = f" (Teil {chunk_num})" if chunk_num else ""

    prompt = f"""Du bist Najika! Deine Aufgabe: Organisiere diesen Text in THEMATISCHE BAUSTEINE!

TEXT-QUELLE: {filename}{chunk_info}

ANLEITUNG:
1. Erkenne ALLE verschiedenen Themen im Text (auch wenn nur 1 Zeile!)
2. Gruppiere Text-Fragmente nach Thema
3. NICHTS weglassen - ALLES kategorisieren!
4. Wenn Widersprüche: Beide als separate Bausteine

FORMAT (JSON):
[
  {{
    "thema": "KI Persönlichkeit",
    "inhalt": "Najika ist Megumin...",
    "zeilen": "1-50, 200-250"
  }},
  {{
    "thema": "Gameplay-Mechanik",
    "inhalt": "Turn-based combat...",
    "zeilen": "51-100"
  }}
]

TEXT:
---
{text[:35000]}
---

DEINE BAUSTEINE (nur JSON, keine Erklärung):"""

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "najika-local",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 3000
                }
            },
            timeout=180
        )

        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")

            # Extrahiere JSON
            try:
                # Finde JSON Array
                start = response_text.find('[')
                end = response_text.rfind(']') + 1

                if start != -1 and end > start:
                    json_str = response_text[start:end]
                    bausteine_data = json.loads(json_str)

                    # Konvertiere zu Baustein-Objekten
                    bausteine = []
                    for data in bausteine_data:
                        quelle = f"{filename} (Zeilen: {data.get('zeilen', '?')})"
                        baustein = Baustein(
                            thema=data.get('thema', 'Unbekannt'),
                            inhalt=data.get('inhalt', ''),
                            quelle=quelle,
                            status='OPTIONAL'
                        )
                        bausteine.append(baustein)

                    return bausteine
                else:
                    print("    [WARNING] Kein JSON Array gefunden - nutze Fallback")
                    return simple_filter(text, filename)

            except json.JSONDecodeError as e:
                print(f"    [WARNING] JSON Parse Error: {e} - nutze Fallback")
                return simple_filter(text, filename)
        else:
            return simple_filter(text, filename)

    except Exception as e:
        print(f"    [ERROR] Ollama Anfrage: {e}")
        return simple_filter(text, filename)

def simple_filter(text, filename):
    """Einfacher Fallback-Filter"""
    # Teile in Absätze
    absaetze = text.split('\n\n')

    bausteine = []
    for i, absatz in enumerate(absaetze, 1):
        if len(absatz.strip()) > 50:  # Mindestens 50 Zeichen
            baustein = Baustein(
                thema="Allgemein",
                inhalt=absatz.strip(),
                quelle=f"{filename} (Absatz {i})",
                status='OPTIONAL'
            )
            bausteine.append(baustein)

    return bausteine

# ===== INPUT-HANDLER =====

def read_pdf(file_path):
    """Liest PDF"""
    if not PDF_AVAILABLE:
        return None

    try:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
        return text
    except:
        return None

def read_file(file_path):
    """Liest beliebige Text-Datei"""
    file_path = Path(file_path)

    if file_path.suffix.lower() == '.pdf':
        return read_pdf(file_path)
    elif file_path.suffix.lower() == '.json':
        # JSON direkt importieren als Bausteine
        return None  # Spezial-Behandlung
    else:
        # TXT, MD, etc.
        try:
            return file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            return None

# ===== SIMPLE CLI (Fallback wenn curses nicht verfügbar) =====

def simple_cli():
    """Einfache CLI ohne curses"""
    print("="*80)
    print("NAJIKA THOUGHT ORGANIZER - SIMPLE CLI")
    print("="*80)
    print()

    manager = BausteinManager()

    while True:
        print("\n" + "="*80)
        print("MENÜ:")
        print("  1 - Text eingeben & filtern")
        print("  2 - Datei importieren")
        print("  3 - Bausteine anzeigen")
        print("  4 - Baustein bearbeiten")
        print("  5 - Exportieren (MD + JSON)")
        print("  6 - Beenden")
        print("="*80)

        choice = input("\nWahl: ").strip()

        if choice == '1':
            print("\nGib deinen Text ein (leere Zeile + ENTER zum Beenden):")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)

            text = '\n'.join(lines)
            print("\nNajika filtert...")
            bausteine = najika_filter_text(text, "Direkte Eingabe")

            for baustein in bausteine:
                manager.add_baustein(baustein)

            print(f"\n✓ {len(bausteine)} Bausteine erstellt!")

        elif choice == '2':
            file_path = input("\nDateipfad: ").strip()

            if not Path(file_path).exists():
                print("[ERROR] Datei nicht gefunden!")
                continue

            print("\nLese Datei...")
            content = read_file(file_path)

            if content:
                print("Najika filtert...")
                bausteine = najika_filter_text(content, Path(file_path).name)

                for baustein in bausteine:
                    manager.add_baustein(baustein)

                print(f"\n✓ {len(bausteine)} Bausteine erstellt!")
            else:
                print("[ERROR] Datei konnte nicht gelesen werden!")

        elif choice == '3':
            print("\n" + "="*80)
            print("BAUSTEINE:")
            print("="*80 + "\n")

            if not manager.kategorien:
                print("Keine Bausteine vorhanden!")
            else:
                for thema, bausteine in manager.kategorien.items():
                    print(f"## {thema}")
                    print("-"*80)

                    for baustein in bausteine:
                        marker = "●" if baustein.status == "KERN" else "○"
                        print(f"\n{marker} {baustein.status} | {baustein.quelle}")
                        print(f"   ID: {baustein.id}")
                        print(f"   {baustein.inhalt[:200]}...")

                    print()

        elif choice == '4':
            baustein_id = input("\nBaustein-ID: ").strip()

            # Finde Baustein
            baustein = next((b for b in manager.bausteine if b.id == baustein_id), None)

            if not baustein:
                print("[ERROR] Baustein nicht gefunden!")
                continue

            print(f"\nAktuell: {baustein.status}")
            print(f"Thema: {baustein.thema}")
            print(f"Inhalt: {baustein.inhalt[:200]}...")
            print()
            print("Optionen:")
            print("  1 - Zu KERN machen")
            print("  2 - Zu OPTIONAL machen")
            print("  3 - Löschen")
            print("  4 - Abbrechen")

            sub_choice = input("\nWahl: ").strip()

            if sub_choice == '1':
                manager.set_kern(baustein_id)
                print("✓ Als KERN markiert!")
            elif sub_choice == '2':
                manager.set_optional(baustein_id)
                print("✓ Als OPTIONAL markiert!")
            elif sub_choice == '3':
                manager.remove_baustein(baustein_id)
                print("✓ Gelöscht!")

        elif choice == '5':
            md_file = manager.export_markdown()
            json_file = manager.export_json()
            print(f"\n✓ Exportiert:")
            print(f"  MD:   {md_file}")
            print(f"  JSON: {json_file}")

        elif choice == '6':
            print("\nBis bald! ✨")
            break

# ===== MAIN =====

def main():
    if not CURSES_AVAILABLE:
        print("[INFO] Curses nicht verfügbar - nutze Simple CLI")
        simple_cli()
    else:
        # TODO: Terminal UI mit curses (später)
        print("[INFO] Terminal UI noch nicht implementiert - nutze Simple CLI")
        simple_cli()

if __name__ == "__main__":
    main()
