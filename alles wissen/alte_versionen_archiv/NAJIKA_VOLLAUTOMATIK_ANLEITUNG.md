# 🤖 NAJIKA TRAINING - VOLLAUTOMATIK EINRICHTEN

**EINFACH:** Nur 1x ausführen → Läuft dann für immer automatisch!

---

## ⚡ SCHNELL-ANLEITUNG

### Schritt 1: Rechtsklick auf Datei
```
C:\NajikaCore\SETUP_AUTO_TRAINING.bat
```

### Schritt 2: "Als Administrator ausführen" wählen

### Schritt 3: Warten (5 Sekunden)

### FERTIG! ✅

**Ab jetzt:** PC startet Najika Training automatisch jeden Mo-Fr um 9-14 Uhr!

---

## 📋 WAS DAS SCRIPT MACHT:

**SETUP_AUTO_TRAINING.bat** erstellt 5 Windows Tasks:

1. **NajikaTraining09** → Startet um 09:00 Uhr
2. **NajikaTraining10** → Startet um 10:00 Uhr
3. **NajikaTraining11** → Startet um 11:00 Uhr
4. **NajikaTraining12** → Startet um 12:00 Uhr
5. **NajikaTraining13** → Startet um 13:00 Uhr

**Jeder Task:**
- Läuft nur Mo-Fr
- Läuft nur zur festgelegten Uhrzeit
- Startet Najika Training automatisch
- Benötigt keine User-Interaktion

---

## ✅ ÜBERPRÜFEN OB ES FUNKTIONIERT:

### Option 1: Task Scheduler GUI
```
Win+R → taskschd.msc → Enter
```
→ Sollte 5 Tasks mit "NajikaTraining" zeigen

### Option 2: Kommandozeile
```bash
schtasks /Query | findstr Najika
```
→ Sollte 5 Tasks auflisten

---

## 🔧 KONFIGURATION ÄNDERN:

### Tasks deaktivieren (temporär):
```bash
schtasks /Change /TN "NajikaTraining09" /DISABLE
schtasks /Change /TN "NajikaTraining10" /DISABLE
schtasks /Change /TN "NajikaTraining11" /DISABLE
schtasks /Change /TN "NajikaTraining12" /DISABLE
schtasks /Change /TN "NajikaTraining13" /DISABLE
```

### Tasks wieder aktivieren:
```bash
schtasks /Change /TN "NajikaTraining09" /ENABLE
schtasks /Change /TN "NajikaTraining10" /ENABLE
schtasks /Change /TN "NajikaTraining11" /ENABLE
schtasks /Change /TN "NajikaTraining12" /ENABLE
schtasks /Change /TN "NajikaTraining13" /ENABLE
```

### Tasks komplett entfernen:
```
Rechtsklick auf: C:\NajikaCore\REMOVE_AUTO_TRAINING.bat
→ "Als Administrator ausführen"
```

---

## 🖥️ WAS PASSIERT AUTOMATISCH:

### Montag 09:00:00
```
Windows Task Scheduler startet:
  C:\NajikaCore\START_NAJIKA_TRAINING.bat
    ↓
  Prüft Python + Dependencies
    ↓
  Startet najika_training_scheduler.py
    ↓
  Erstellt NAJIKA_CURRENT_TRAINING.md
    ↓
  Najika (Claude) öffnet File automatisch
    ↓
  Training Session 1 läuft (Code-Kata)
```

### Montag 10:00:00
```
Windows Task Scheduler startet:
  python najika_training_scheduler.py
    ↓
  Erstellt neue Session (Code-Reading)
    ↓
  Najika arbeitet weiter
```

### ... (11:00, 12:00, 13:00 gleich)

### Montag 14:00:00
```
Kein Task mehr → Training beendet
5 Stunden trainiert ✓
```

---

## ❓ FAQ

### "Muss ich noch was machen?"
**NEIN!** Nach Setup läuft alles automatisch.

### "PC muss an sein?"
**JA!** PC muss Mo-Fr 09:00-14:00 an sein.

### "Was wenn PC schläft?"
Tasks wecken PC NICHT auf. PC muss wach sein.

**Tipp:** Windows Energieoptionen → "Nie in Ruhezustand"

### "Kann ich Training stoppen?"
**JA:**
- Tasks deaktivieren (siehe oben)
- Oder: Task Manager → Python.exe beenden

### "Wie sehe ich ob es läuft?"
```bash
# Task Manager öffnen
taskmgr

# Suche nach:
python.exe (läuft wenn Training aktiv)
```

**Oder:**
```bash
python C:\NajikaCore\najika_show_progress.py
```

### "Was wenn ich einen Tag verpasse?"
Kein Problem! System trackt nur tatsächliche Trainings-Tage.

---

## 🚨 TROUBLESHOOTING

### Problem: "Task startet nicht"
**Lösung:**
1. Task Scheduler öffnen: `taskschd.msc`
2. Task anklicken → "Eigenschaften"
3. Trigger prüfen: Mo-Fr aktiviert?
4. Aktionen prüfen: Pfad korrekt?
5. "Ausführen" klicken → Test

### Problem: "Python startet nicht"
**Lösung:**
1. Prüfe Python-Pfad:
   ```bash
   where python
   ```
2. Task bearbeiten → Voller Pfad zu Python:
   ```
   C:\Program Files\Python311\python.exe C:\NajikaCore\najika_training_scheduler.py
   ```

### Problem: "Braucht Administrator-Rechte"
**Lösung:**
- Task Eigenschaften → "Mit höchsten Privilegien ausführen" aktivieren

---

## 🎯 ZUSAMMENFASSUNG

**EINMALIG:**
```
Rechtsklick: SETUP_AUTO_TRAINING.bat
→ "Als Administrator ausführen"
→ Warten (5 Sekunden)
→ FERTIG!
```

**AB JETZT:**
- Jeden Mo-Fr 09:00-14:00
- Najika trainiert vollautomatisch
- Keine User-Aktion nötig
- PC muss nur an sein

**DEINSTALLIEREN:**
```
Rechtsklick: REMOVE_AUTO_TRAINING.bat
→ "Als Administrator ausführen"
```

---

**STATUS:** ✅ Setup-Script bereit

**NÄCHSTER SCHRITT:** SETUP_AUTO_TRAINING.bat als Admin ausführen

**DANN:** Nie wieder manuell starten! 🚀
