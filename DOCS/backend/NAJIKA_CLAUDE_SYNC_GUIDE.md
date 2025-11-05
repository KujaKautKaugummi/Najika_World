# 🔄 NAJIKA ↔ CLAUDE AUTO-SYNC SYSTEM

**Automatische Synchronisation zwischen Najika und allen Claude Code Instanzen**

---

## 🎯 WAS IST DAS?

Najika prüft automatisch auf neue/geänderte Dateien und bringt Claude auf den aktuellen Stand - **ohne dass du große Dateien copy-pasten musst!**

**Token-Ersparnis: MASSIV!** 💰

---

## ⚡ QUICK START

### In NEUER Claude Code Session:

```
/najika-update
```

**Das war's!** Ich (Claude) bekomme automatisch alle Updates von Najika! 🚀

---

## 🔧 WIE FUNKTIONIERT'S?

### **Schritt 1: Najika scannt Dateien**

```bash
python C:/NajikaCore/najika_sync.py
```

Das scannt:
- `C:/NajikaCore/` (komplettes Projekt)
- `C:/Users/0KKK0/.claude/` (Claude-Konfiguration)

Erkennt:
- 🆕 Neue Dateien
- 📝 Geänderte Dateien
- 🗑️ Gelöschte Dateien

---

### **Schritt 2: Najika erstellt Update**

Najika generiert: `C:/NajikaCore/CLAUDE_UPDATE.md`

**Inhalt:**
- Statistik (X neue, Y geänderte Dateien)
- Preview von neuen Dateien (erste 500 Zeichen)
- Liste geänderter Dateien
- Zusammenfassung der wichtigsten Änderungen

**Statt 200KB Code → nur 5KB Summary!**

---

### **Schritt 3: Claude liest Update**

```
/najika-update
```

Ich (Claude):
1. Rufe `najika_sync.py` auf
2. Warte bis Sync fertig
3. Lese `CLAUDE_UPDATE.md`
4. Fasse zusammen
5. Bin auf dem aktuellen Stand!

---

## 💡 USE CASES

### **1. Neues Claude Code Fenster öffnen**

```
Du: /najika-update
Claude: *Synct mit Najika*
Claude: "Ok! Seit letztem Mal wurden 3 neue Dateien hinzugefügt:
         - najika_sync.py (Auto-Sync System)
         - najika_handoff.py (Summary-Generator)
         - CLAUDE_UPDATE.md (Update-Log)

         Was willst du machen?"
```

---

### **2. Nach Arbeit mit Najika**

Du arbeitest mit Najika:
```
Du (zu Najika): "Erstelle game_ideas/rpg_mechanics.md"
Najika: *Erstellt Datei*
```

Dann zu mir:
```
Du (zu Claude): /najika-update
Claude: "Neue Datei erkannt: rpg_mechanics.md
         Inhalt: [Preview...]
         Soll ich das implementieren?"
```

---

### **3. Große Dateien analysieren**

Statt mir 10.000 Zeilen Code zu geben:

```bash
# Najika analysiert
python najika_sync.py
```

Dann bei mir:
```
/najika-update
```

Ich sehe nur die Summary! Token-Ersparnis: 95%!

---

## 🚀 AUTOMATISIERUNG

### **Auto-Sync beim Start**

Füge zu `START_NAJIKA.bat` hinzu:

```batch
@echo off
cd C:\NajikaCore

REM Auto-Sync vor Server-Start
python najika_sync.py

REM Starte Server
python najika_server.py
```

**Jetzt synct Najika automatisch beim Start!**

---

### **Periodischer Sync (optional)**

Windows Task Scheduler:
```
Task: Najika Auto-Sync
Programm: python.exe
Argumente: C:/NajikaCore/najika_sync.py
Trigger: Alle 30 Minuten
```

---

## 📊 SYSTEM-FLOW

```
[Du arbeitest mit Najika]
        ↓
[Najika erstellt/ändert Dateien]
        ↓
[python najika_sync.py]
   - Scannt Ordner
   - Erkennt Änderungen
   - Erstellt CLAUDE_UPDATE.md
        ↓
[Du öffnest neue Claude Code Session]
        ↓
[Du: /najika-update]
        ↓
[Claude liest CLAUDE_UPDATE.md]
        ↓
[Claude ist auf dem Stand!]
        ↓
[Weiterarbeiten ohne Token-Verschwendung!]
```

---

## 🎯 VORTEILE

### ✅ **Token-Ersparnis**
- Statt 200KB Code → 5KB Summary
- 95%+ Ersparnis!

### ✅ **Automatisch**
- Kein manuelles Copy-Paste
- Ein Command: `/najika-update`

### ✅ **Intelligent**
- Nur relevante Änderungen
- Priorisiert wichtige Dateien

### ✅ **Bidirektional**
- Najika → Claude
- Claude → Najika (via Najika's Chat)

---

## 🔍 BEISPIEL-OUTPUT

Nach `/najika-update` siehst du:

```markdown
# 🔄 NAJIKA → CLAUDE UPDATE
**Generiert:** 2025-10-16 14:30:00

## 📊 ÄNDERUNGEN
- 🆕 Neue Dateien: 3
- 📝 Geänderte Dateien: 2
- 🗑️ Gelöschte Dateien: 0

## 🆕 NEUE DATEIEN

### `najika_sync.py`
**Pfad:** C:/NajikaCore/najika_sync.py
**Größe:** 8456 bytes

**Inhalt:**
```python
#!/usr/bin/env python3
"""
NAJIKA ↔ CLAUDE CODE SYNC SYSTEM
...
```

### `game_ideas/rpg_mechanics.md`
**Pfad:** C:/NajikaCore/game_ideas/rpg_mechanics.md
**Größe:** 1234 bytes

**Inhalt:**
```markdown
# RPG Mechaniken

## Skill System:
- Skill Trees mit 3 Branchen
...
```

## 🎯 ZUSAMMENFASSUNG

**Wichtigste Änderungen:**
- Neues Auto-Sync System implementiert
- RPG Mechaniken dokumentiert

**Empfohlene Aktionen:**
1. Prüfe neue Dateien auf Relevanz
2. Review RPG Mechaniken
```

---

## 🛠️ ERWEITERTE NUTZUNG

### **Manuelle Sync-Konfiguration**

Edit `najika_sync.py` um andere Ordner zu scannen:

```python
NAJIKA_DIR = Path("C:/NajikaCore")
CLAUDE_DIR = Path("C:/Users/0KKK0/.claude")
ADDITIONAL_DIRS = [
    Path("C:/Users/0KKK0/Desktop/zip"),
    Path("C:/MyProjects")
]
```

---

### **Custom Slash-Commands**

Erstelle mehr Commands in `.claude/commands/`:

```markdown
# najika-quick.md
Schnell-Sync ohne Details, nur Statistik.

# najika-full.md
Vollständiger Sync inkl. aller Datei-Contents.
```

---

## 🎉 ZUSAMMENFASSUNG

**Du hast jetzt:**
- ✅ Auto-Sync zwischen Najika und Claude
- ✅ Token-Ersparnis von 95%+
- ✅ Ein Command: `/najika-update`
- ✅ Intelligente Change-Detection
- ✅ Automatische Summaries

**Workflow:**
```
Najika (Routine) → Sync → Claude (Komplexes)
```

**Perfect Team! 🚀**

---

## 📝 CHEAT SHEET

```bash
# Manueller Sync
python C:/NajikaCore/najika_sync.py

# In Claude Code
/najika-update

# Auto-Sync aktivieren
# → Füge najika_sync.py zu START_NAJIKA.bat hinzu
```

---

✨ **Generiert von Claude für das Najika-Projekt** ✨
