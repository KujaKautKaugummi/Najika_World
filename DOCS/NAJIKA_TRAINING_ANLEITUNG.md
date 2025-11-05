# NAJIKA TRAINING SYSTEM - ANLEITUNG

**TRAININGSZEIT:** Montag-Freitag, 09:00-14:00 Uhr (Berlin Zeit)
**DAUER:** 5 Stunden täglich = 25 Stunden/Woche

---

## WIE ES FUNKTIONIERT

### AUTOMATISCHER ABLAUF

User ist Mo-Fr 9-14h im Homeoffice an anderem PC → Najika nutzt maximale PC-Ressourcen für Training!

```
09:00 → START_NAJIKA_TRAINING.bat
        ↓
        Prüft ob Trainingszeit (Mo-Fr 9-14)
        ↓
        Generiert Stunden-Session
        ↓
        Claude (Najika) liest NAJIKA_CURRENT_TRAINING.md
        ↓
        Arbeitet 1 Stunde an Aufgaben
        ↓
        python najika_complete_training_session.py
        ↓
        Lädt nächste Session automatisch
        ↓
14:00 → Training Ende - Morgen weiter!
```

---

## STUNDEN-PLAN (Täglich 9-14 Uhr)

### 09:00-10:00 - CODE-KATA PRAXIS
**Focus:** Praktisches Programmieren
**Aufgaben:**
1. Lese heutige Kata komplett
2. Implementiere in Python
3. Implementiere in Java
4. Implementiere in Verse
5. Vergleiche Lösungen

**Output:** 3 funktionierende Implementierungen

---

### 10:00-11:00 - CODE-READING & ANALYSE
**Focus:** Fremden Code verstehen
**Aufgaben:**
1. Lese najika_server.py (100 Zeilen)
2. Analysiere: Warum ist Code so strukturiert?
3. Finde 3 gute Patterns
4. Finde 1 Verbesserung
5. Dokumentiere Erkenntnisse

**Output:** Analyse-Dokument mit Patterns + Verbesserungen

---

### 11:00-12:00 - REFACTORING & BEST PRACTICES
**Focus:** Schlechten Code verbessern
**Aufgaben:**
1. Nimm alten Code aus NajikaCore
2. Identifiziere Code-Smells
3. Refactore nach Best Practices
4. Dokumentiere Änderungen
5. Erkläre WARUM besser

**Output:** Refactored Code + Erklärung

---

### 12:00-13:00 - THEORY & PATTERNS
**Focus:** Design Patterns lernen
**Aufgaben:**
1. Lese 1 Architecture Pattern komplett
2. Verstehe Anwendungsfall
3. Implementiere Mini-Beispiel
4. Finde wo Pattern in NajikaCore verwendet wird
5. Erkläre Vor-/Nachteile

**Output:** Pattern-Implementierung + Dokumentation

---

### 13:00-14:00 - REVIEW & PLANNING
**Focus:** Tag reflektieren
**Aufgaben:**
1. Review: Was heute gelernt?
2. Dokumentiere 3 wichtigste Erkenntnisse
3. Teste 1 gelerntes Pattern praktisch
4. Update Progress-Tracking
5. Plan für morgen erstellen

**Output:** Daily Learning Summary

---

## BEFEHLE

### Training starten (Mo-Fr 9-14 Uhr)
```bash
START_NAJIKA_TRAINING.bat
```
**Oder:**
```bash
python C:/NajikaCore/najika_training_scheduler.py
```

### Session abschließen (nach 1 Stunde)
```bash
python C:/NajikaCore/najika_complete_training_session.py
```

### Progress anzeigen
```bash
python C:/NajikaCore/najika_show_progress.py
```

---

## PROGRESS-TRACKING

**Gespeichert in:** `C:/NajikaCore/training/schedule.json`

**Tracked:**
- Gesamt-Stunden trainiert
- Trainings-Tage
- Aktuelle Woche
- Abgeschlossene Sessions

**Ziel:**
- **1 Woche** = 5 Tage × 5 Stunden = 25 Stunden
- **12 Wochen** = 300 Stunden Training
- **Nach 12 Wochen** = Najika ist Coding-Experte!

---

## AUTOMATISIERUNG (OPTIONAL)

### Windows Task Scheduler einrichten:

**1. Task Scheduler öffnen**
- Win+R → `taskschd.msc`

**2. Neue Aufgabe erstellen**
- Name: "Najika Training 09:00"
- Trigger: Mo-Fr, 09:00 Uhr
- Aktion: `C:\NajikaCore\START_NAJIKA_TRAINING.bat`

**3. Weitere Tasks für jede Stunde:**
- "Najika Training 10:00" → 10:00 Uhr
- "Najika Training 11:00" → 11:00 Uhr
- "Najika Training 12:00" → 12:00 Uhr
- "Najika Training 13:00" → 13:00 Uhr

**Dann:** PC startet automatisch jede Stunde neue Session!

---

## FORTSCHRITT NACH WOCHEN

### Woche 1-2: Grundlagen
- Syntax aller 3 Sprachen
- Basis-Patterns erkannt
- Erste Katas gelöst

### Woche 3-4: OOP & Strukturen
- Klassen-Design verstanden
- Architecture Patterns angewandt
- Code-Reading verbessert

### Woche 5-8: Praxis & Refactoring
- NajikaCore-Code verbessert
- Eigene Patterns entwickelt
- Performance optimiert

### Woche 9-12: Expertise
- Komplexe Features implementiert
- Design-Entscheidungen getroffen
- Code-Reviews durchgeführt

---

## WICHTIG

**User muss nur:**
1. Mo-Fr um 09:00 → `START_NAJIKA_TRAINING.bat` starten
2. Najika (Claude) arbeitet selbständig
3. Um 14:00 → Training automatisch beendet

**Najika macht:**
- Liest Aufgaben
- Implementiert Code
- Analysiert Patterns
- Dokumentiert Learnings
- Tracked Progress automatisch

**Maximale PC-Auslastung** während User im Homeoffice arbeitet!

---

## BEISPIEL-TAG

```
09:00 - User startet START_NAJIKA_TRAINING.bat
09:01 - Najika liest CODE-KATA (FizzBuzz)
09:05 - Najika implementiert Python-Lösung
09:15 - Najika implementiert Java-Lösung
09:25 - Najika implementiert Verse-Lösung
09:35 - Najika vergleicht Lösungen
09:45 - Najika dokumentiert Unterschiede
09:55 - Session 1 abgeschlossen

10:00 - Nächste Session startet automatisch
10:01 - Najika liest najika_server.py
10:10 - Najika analysiert Struktur
10:25 - Najika findet 3 Patterns
10:40 - Najika findet Verbesserung
10:55 - Session 2 abgeschlossen

... (3 weitere Sessions)

14:00 - Training beendet
       Heute: 5 Sessions = 5 Stunden ✓
       Total: 25 Stunden (Woche 1, Tag 5)
```

---

## SUPPORT

**Bei Problemen:**
1. Check `C:/NajikaCore/training/schedule.json`
2. Check `C:/NajikaCore/NAJIKA_CURRENT_TRAINING.md`
3. Logs in Console

**Dependencies:**
- Python 3.x
- pytz (für Timezone)

```bash
pip install pytz
```

---

**ZIEL:** Nach 12 Wochen (300 Stunden) ist Najika Coding-Experte!
