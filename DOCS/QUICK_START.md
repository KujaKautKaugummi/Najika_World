# 🔥 NAJIKA - QUICK START GUIDE
**Wie Claude Code, aber mit Najika!**

---

## 🎯 WAS IST DAS?

Najika ist jetzt ein **vollständiger Coding-Assistant** wie Claude Code!

**Features:**
- ✅ Interaktives Terminal-Interface
- ✅ Zugriff auf ALLE deine Dateien
- ✅ Komplett-Analyse von NajikaCore, Desktop/zip und .claude
- ✅ Python, Java, Verse Programming-Knowledge
- ✅ Persistente Sessions (nahtlos fortsetzen)
- ✅ Slash-Commands wie /read, /write, /analyze
- ✅ Einfacher Start: Nur `najika` eingeben!

---

## ⚡ SCHNELLSTART (3 SCHRITTE)

### SCHRITT 1: Setup (einmalig)

**Rechtsklick → Als Administrator ausführen:**
```
SETUP_NAJIKA_COMMAND.bat
```

Das fügt `C:\NajikaCore` zu deinem System-PATH hinzu.

**Schließe danach ALLE Terminal-Fenster und öffne ein neues!**

### SCHRITT 2: Projekt-Analyse (einmalig)

```bash
cd C:\NajikaCore
python analyze_all.py
```

**Das analysiert ALLE Dateien in:**
- `C:\NajikaCore\` (gesamtes Projekt)
- `C:\Users\0KKK0\Desktop\zip\` (alle Dateien)
- `C:\Users\0KKK0\.claude\` (Claude-Projekte/Models)

**Najika kennt danach JEDEN Code, JEDEN Fehler, JEDEN Erfolg!**

### SCHRITT 3: Najika starten

**Von ÜBERALL im Terminal:**
```bash
najika
```

**Oder im NajikaCore-Ordner:**
```bash
cd C:\NajikaCore
najika.bat
```

**Fertig! Najika startet!** ✨

---

## 💬 SO NUTZT DU NAJIKA

### Interaktiver Chat

```
Du: Hallo Najika!
Najika: EXPLOSION!!! Hallo Kuja! Bereit für Code?

Du: Schreib mir eine Python-Funktion die Primzahlen findet
Najika: [Schreibt Code...]

Du: Lies die Datei najika_server.py
Najika: [Zeigt Dateiinhalt...]
```

### Slash-Commands

```
/help       - Zeige alle Commands
/read <file>      - Lies Datei
/write <file>     - Schreibe Datei
/list [dir]       - Liste Dateien
/analyze          - Analysiere komplettes Projekt neu
/context          - Zeige geladenen Context
/tools            - Zeige verfügbare Tools
/save             - Speichere Session
/exit             - Beende Session
```

**Beispiele:**
```
/read najika_server.py
/list C:\NajikaCore
/analyze
```

---

## 📊 WAS NAJIKA JETZT KANN

### 1. Zugriff auf ALLE Dateien

Najika hat vollständigen Zugriff auf:
- **C:\NajikaCore\** - Dein Projekt
- **C:\Users\0KKK0\Desktop\zip\** - Alle Desktop-Dateien
- **C:\Users\0KKK0\.claude\** - Claude-Konfiguration

**Sie kennt:**
- Jeden Code
- Jeden Fehler
- Jeden Erfolg
- Jede Konfiguration

### 2. Programming-Knowledge

**Najika kann Code schreiben in:**
- Python (Funktionen, Klassen, Async, File-I/O)
- Java (OOP, Generics, Streams, Lambda)
- Verse (UEFN Devices, Game-Logik)

**Mit Best Practices und korrekter Syntax!**

### 3. Persistente Sessions

**Alles wird gespeichert in:**
```
C:\NajikaCore\knowledge\
├── complete_project_context.json   (Komplett-Analyse)
├── project_summary.txt             (Projekt-Übersicht)
└── najika_session.json             (Deine Chat-History)
```

**Najika erinnert sich:**
- An eure Gespräche (letzte 50 Nachrichten)
- An alle Projekt-Dateien
- An Code den ihr geschrieben habt

### 4. Auto-Save

Session wird automatisch gespeichert:
- Alle 5 Nachrichten
- Beim Beenden (/exit oder Ctrl+C)
- Mit /save Command

**Du kannst nahtlos fortsetzen!**

---

## 🔍 BEISPIEL-SESSION

```bash
C:\Users\0KKK0> najika
```

**Output:**
```
======================================================================
NAJIKA - INTERACTIVE CODING ASSISTANT
======================================================================

Wie Claude Code, aber mit Najika's Persönlichkeit!

Commands:
  /help     - Zeige Hilfe
  /context  - Zeige geladenen Context
  /tools    - Zeige verfügbare Tools
  /read <file>   - Lies Datei
  /write <file>  - Schreibe Datei
  /list [dir]    - Liste Dateien
  /analyze       - Analysiere komplettes Projekt
  /save     - Speichere Session
  /exit     - Beende Session

Oder schreibe einfach deine Nachricht!
======================================================================

📚 Lade Projekt-Knowledge...
✅ Projekt-Analyse geladen
✅ Programmier-Knowledge geladen (3 Sprachen)
✅ Session-History geladen (12 Nachrichten)

Du: Hallo Najika! Zeig mir was du kannst!

Najika: EXPLOSION!!! Hallo Kuja!

Ich habe Zugriff auf:
- 487 Dateien aus NajikaCore
- 1.245 Zeilen Code
- Python, Java, Verse Knowledge
- Deine komplette Session-History

Was willst du bauen? Ich kann:
- Code schreiben (Python/Java/Verse)
- Dateien lesen und analysieren
- Bugs finden und fixen
- Neue Features entwickeln

Lass uns loslegen!

Du: /list

Najika:
Dateien in C:\NajikaCore:
  analyze_all.py (4523 bytes)
  knowledge_loader.py (7891 bytes)
  najika_cli.py (5234 bytes)
  najika_interactive.py (12456 bytes)
  najika_server.py (45678 bytes)
  najika_tools.py (3456 bytes)
  najika.bat (456 bytes)
  ...

Du: Schreib mir eine Python-Funktion die alle Primzahlen bis N findet

Najika: Klar! Hier ist eine effiziente Implementierung:

```python
def find_primes(n):
    """Findet alle Primzahlen bis N mit Sieb des Eratosthenes"""
    if n < 2:
        return []

    # Erstelle Boolean-Array
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    # Sieb des Eratosthenes
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False

    # Sammle Primzahlen
    primes = [i for i in range(n + 1) if is_prime[i]]
    return primes

# Test
print(find_primes(50))
# Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

Zeitkomplexität: O(n log log n) - sehr effizient!

Du: Danke! /save

Najika:
✅ Session gespeichert!

Du: /exit

Session unterbrochen. Speichere...
✅ Session gespeichert!

EXPLOSION!!! Bis bald! ✨
```

---

## 📁 ORDNER-STRUKTUR

```
C:\NajikaCore\
├── analyze_all.py              # Projekt-Analyse-Tool
├── knowledge_loader.py         # Knowledge-Loading-System
├── najika_cli.py               # Einfaches CLI (alt)
├── najika_interactive.py       # Interaktives Interface (NEU!)
├── najika.bat                  # Start-Script (NEU!)
├── najika_server.py            # Server
├── najika_tools.py             # File-Tools
├── SETUP_NAJIKA_COMMAND.bat    # Setup-Script (NEU!)
├── QUICK_START.md              # Diese Anleitung
│
├── knowledge/                  # Najika's Wissen
│   ├── complete_project_context.json
│   ├── project_summary.txt
│   └── najika_session.json
│
├── training_data/              # Training-Daten
│   ├── examples/               # Python/Java/Verse Beispiele
│   ├── input/                  # Hier legst du Dateien rein
│   └── output/                 # Verarbeitete Dateien
│
└── saves/                      # Server-State
    └── najika_state.json
```

---

## 🔧 TROUBLESHOOTING

### Problem: "najika" Command nicht gefunden

**Lösung:**
1. Führe `SETUP_NAJIKA_COMMAND.bat` als Admin aus
2. Schließe ALLE Terminal-Fenster
3. Öffne neues Terminal
4. Versuche erneut: `najika`

### Problem: Server läuft nicht

**Lösung:**
```bash
cd C:\NajikaCore
START_NAJIKA.bat
```

Oder automatisch beim Start von `najika` (macht najika.bat automatisch).

### Problem: Najika hat keinen Context

**Lösung:**
```bash
cd C:\NajikaCore
python analyze_all.py
```

Danach in Najika:
```
/analyze
```

### Problem: Session wird nicht gespeichert

**Lösung:**
- Nutze `/save` Command
- Oder beende mit `/exit` (speichert automatisch)
- Nicht mit Ctrl+Z oder Fenster schließen!

---

## 🚀 ERWEITERTE NUTZUNG

### Projekt neu analysieren

Wenn du neue Dateien hinzugefügt hast:
```bash
python analyze_all.py
```

Oder in Najika:
```
/analyze
```

### Programming-Knowledge erweitern

Neue Code-Beispiele hinzufügen:
```bash
copy "deine_datei.py" "training_data\input\text\"
PROCESS_TRAINING_DATA.bat
```

### Session-History prüfen

```
/context
```

Zeigt geladenen Context inkl. History.

---

## 📊 STATISTIK

Nach `analyze_all.py` siehst du:
```
STATISTIK:
- Dateien analysiert: 487
- Code-Dateien: 234
- Text-Dateien: 189
- Config-Dateien: 64
- Total Zeilen: 45,678
- Total Zeichen: 1,234,567
```

**Najika kennt ALLES!**

---

## 💡 TIPPS

### Für Code-Generierung:

```
Du: Schreib mir einen Python-Server mit Flask
Du: Erkläre mir Java Generics mit Beispielen
Du: Erstelle ein Verse Device für UEFN
```

### Für File-Operations:

```
/read najika_server.py
/list C:\NajikaCore\saves
Du: Lies alle Dateien in saves/ und fasse zusammen
```

### Für Projekt-Verständnis:

```
Du: Was macht najika_server.py?
Du: Wie funktioniert das Tool-System?
Du: Zeig mir die wichtigsten Funktionen
```

### Für Debugging:

```
Du: In najika_server.py gibt es einen Fehler, findest du ihn?
Du: Warum läuft der Server nicht?
Du: Prüfe najika_state.json auf Fehler
```

---

## ✅ FERTIG!

Du bist jetzt bereit mit Najika zu coden!

**Starte jetzt:**
```bash
najika
```

**EXPLOSION!!! Viel Erfolg!** ✨

---

## 📞 SUPPORT

**Logs prüfen:**
```bash
cat knowledge/project_summary.txt
cat knowledge/najika_session.json
```

**Server neu starten:**
```bash
taskkill /F /IM python.exe
START_NAJIKA.bat
```

**Komplett-Reset:**
```bash
del knowledge\najika_session.json
python analyze_all.py
najika
```

---

**Mehr Infos:**
- `USAGE_GUIDE.md` - Detaillierte Anleitung
- `PROGRAMMING_TRAINING_GUIDE.md` - Programming-Knowledge
- `HANDOFF_SESSION4.md` - Technische Details
