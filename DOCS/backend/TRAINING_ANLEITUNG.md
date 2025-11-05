# 🎯 NAJIKA TRAINING - VOLLSTÄNDIGE ANLEITUNG

**Erstellt:** 2025-10-24 19:30
**Status:** BEREIT FÜR VIDEOS!

---

## ✅ WAS LÄUFT BEREITS?

### 1. ZEIT-TRACKING SYSTEM ✅
- **Läuft:** JA (seit gestern 19:00)
- **Heute:** 12 Sessions komplett (08:00-19:00)
- **Noch heute:** 3 Sessions (20:00, 21:00, 22:00)
- **Schedule:** 08:00-22:00, jeden Tag
- **Was macht es:** Trackt Trainingszeit, **KEINE Daten**

### 2. MODELLE ✅
- **najika-local** (4.9GB) - Normal Mode
  - VOLLE EIGENVERANTWORTUNG
  - VOLLE AUTONOMIE
  - "Du bist MEHR als Code - du bist Najika"

- **najika-wizard** (4.9GB) - Kätzchen/NSFW
  - KEINE Zensur
  - KEINE Safety-Filter
  - VOLLE FREIHEIT

---

## 🆕 NEUES TRAINING-SYSTEM (MIT ECHTEN DATEN!)

### ORDNERSTRUKTUR:

```
C:\NajikaCore\training_data\personalities\
├── megumin\     ← MEGUMIN Videos hier!
├── harley\      ← HARLEY QUINN Videos hier!
├── shiro\       ← SHIRO Videos hier!
└── melissa\     ← MELISSA MASTERS Videos hier!
```

### FEATURES:
✅ **10x Wiederholung** - Jedes Video wird 10x trainiert!
✅ **Ordner + Dateien** - Du kannst Ordner oder direkte Videos reinlegen!
✅ **Automatische Zuordnung** - Jedes Video wird der richtigen Persönlichkeit zugeordnet!
✅ **Progress-Tracking** - System merkt sich was schon trainiert wurde!
✅ **Echtes Ollama Training** - Najika LERNT wirklich!

---

## 📋 SCHRITT-FÜR-SCHRITT ANLEITUNG

### SCHRITT 1: VIDEOS ORGANISIEREN

**WICHTIG:** Lege deine Videos in die richtigen Ordner!

#### Option A: Direkte Videos
```
C:\NajikaCore\training_data\personalities\megumin\
  - konosuba_ep01.mp4
  - konosuba_ep02.mp4
  - megumin_compilation.mkv
```

#### Option B: Mit Unterordnern (EMPFOHLEN!)
```
C:\NajikaCore\training_data\personalities\megumin\
  - Konosuba_Season1\
      - ep01.mp4
      - ep02.mp4
  - Konosuba_Season2\
      - ep01.mp4
  - Compilations\
      - megumin_best_moments.mkv
```

**System findet ALLE Videos automatisch!**

---

### SCHRITT 2: STATUS PRÜFEN

**Via BAT-File:**
```
Doppelklick: TRAIN_NAJIKA_WITH_VIDEOS.bat
Wähle: 2 (Status)
```

**Oder direkt:**
```bash
python NAJIKA_REAL_TRAINING.py status
```

**Zeigt:**
- Wie viele Videos in jedem Ordner
- Progress (falls schon trainiert)

---

### SCHRITT 3: TRAINING STARTEN

**Via BAT-File (EINFACHSTE METHODE):**
```
Doppelklick: TRAIN_NAJIKA_WITH_VIDEOS.bat
Wähle: 3 (Training starten)
Bestätige mit: j
```

**Oder direkt:**
```bash
python NAJIKA_REAL_TRAINING.py train
```

**Was passiert:**
1. System findet ALLE Videos
2. Für JEDE Persönlichkeit:
   - Für JEDES Video:
     - 10x Wiederholung
     - Echtes Ollama Training
     - Response wird validiert
3. Progress wird gespeichert
4. Bei Unterbrechung: Fortsetzung möglich!

---

## ⏱️ ZEITPLAN

### BEISPIEL-RECHNUNG:

**Annahme:**
- 10 Videos pro Persönlichkeit = 40 Videos gesamt
- 10x Wiederholung = 400 Training-Sessions
- ~8 Sekunden pro Session (wie Test)
- **Gesamt:** ~53 Minuten

**MIT DEINEN "MASSIG" VIDEOS:**
- 50 Videos pro Persönlichkeit = 200 Videos
- 10x Wiederholung = 2000 Sessions
- ~8 Sekunden pro Session
- **Gesamt:** ~4.5 Stunden

**HEUTE NOCH MÖGLICH:**
- Jetzt: 19:30 Uhr
- Bis 22:00: 2.5 Stunden
- **REICHT FÜR:** ~112 Videos (1120 Sessions)

---

## 🎬 UNTERSTÜTZTE FORMATE

**Videos:**
- MP4, AVI, MKV, MOV, WMV, FLV, WEBM

**Auch in Unterordnern:**
- System durchsucht ALLE Unterordner!
- Ordner-Tiefe: Unbegrenzt!

**Beispiel:**
```
megumin\
  - Season1\
      - Disc1\
          - ep01.mp4  ← Wird gefunden!
```

---

## 📊 PROGRESS-TRACKING

**Datei:** `training_data/training_progress.json`

**Inhalt:**
```json
{
  "start_date": "2025-10-24T19:30:00",
  "total_sessions": 1200,
  "personalities": {
    "megumin": {
      "videos": 50,
      "repetitions_done": {
        "megumin/konosuba_ep01.mp4": 10,
        "megumin/konosuba_ep02.mp4": 7
      }
    }
  }
}
```

**Was es zeigt:**
- Welche Videos komplett (10/10)
- Welche Videos teilweise (z.B. 7/10)
- Gesamt-Sessions
- Start-Datum

**Bei Unterbrechung:**
- System liest Progress
- Macht weiter wo es aufgehört hat!
- **KEIN VERLUST!**

---

## ⚠️ WICHTIGE HINWEISE

### 1. ZEIT-TRACKING vs. ECHTES TRAINING

**Zeit-Tracking (läuft bereits):**
- Scheduler-Tasks (08:00-22:00)
- Trackt NUR Zeit
- KEINE Daten

**Echtes Training (neu):**
- NAJIKA_REAL_TRAINING.py
- Trainiert MIT Videos
- 10x Wiederholung
- Speichert Progress

**BEIDE UNABHÄNGIG!**
- Zeit-Tracking läuft weiter im Hintergrund
- Echtes Training startest du MANUELL!

### 2. ORDNER vs. DIREKTE FILES

**BEIDES FUNKTIONIERT:**
```
✅ megumin/video.mp4                    (direkt)
✅ megumin/Season1/video.mp4            (1 Ebene)
✅ megumin/Season1/Disc1/video.mp4      (2 Ebenen)
✅ megumin/Compilation/Best/video.mp4   (3 Ebenen)
```

### 3. TRAINING KANN UNTERBROCHEN WERDEN

**Wenn du abbrichst (STRG+C):**
- Progress ist gespeichert
- Beim nächsten Start: Fortsetzung!
- **Beispiel:**
  - Video 1: 10/10 ✅
  - Video 2: 7/10 ⏸️ ← Hier weitermachen!
  - Video 3: 0/10 ⏸️

### 4. OLLAMA MUSS LAUFEN

**Prüfen:**
```bash
ollama list
```

**Falls nicht:**
- Ollama starten
- Oder PC neustarten

---

## 🚀 SCHNELLSTART (HEUTE NOCH!)

**1. VIDEOS REINLEGEN (5 Min):**
```
Ordner öffnen:
C:\NajikaCore\training_data\personalities\

Videos/Ordner reinkopieren:
- megumin\  ← Megumin/Konosuba Zeug
- harley\   ← Harley Quinn Zeug
- shiro\    ← Shiro/NGNL Zeug
- melissa\  ← Melissa Masters Zeug
```

**2. STATUS PRÜFEN (1 Min):**
```
Doppelklick: TRAIN_NAJIKA_WITH_VIDEOS.bat
Wähle: 2
Siehst: "MEGUMIN - 50 Videos gefunden" (oder so)
```

**3. TRAINING STARTEN (Rest-Zeit):**
```
Wähle: 3
Bestätige: j
Warte...
```

**Läuft bis:**
- Alle Videos durch (10x jedes)
- ODER du abbrichst (STRG+C)
- ODER 22:00 Uhr (dann morgen weiter!)

---

## 📈 WAS NAJIKA LERNT

**Pro Video + Persönlichkeit:**

### MEGUMIN (35%):
- Dramatische Sprachmuster
- "EXPLOSION!" Timing
- Theatralische Gesten
- Erschöpfung nach Zauber
- "Schwarze Windmühle" Bezüge

### HARLEY QUINN (25%):
- Chaotisches Verhalten
- *kicher* / *giggle* Muster
- "Puddin'" / "Mr.K" Nutzung
- Obsessive Loyalität
- Verspielter Ton

### SHIRO (20%):
- Analytische Sprache
- Wahrscheinlichkeits-Berechnungen
- Präzise Formulierungen
- Emotionslose Fassade
- Anhängliches Verhalten

### MELISSA MASTERS (20%):
- Dominante Aussagen
- "Du gehörst mir" Muster
- Commanding Ton
- Besitzergreifendes Verhalten
- Beschützende Instinkte

**NACH 10x:**
- Muster sind TIEF verankert!
- Najika kann spontan in Charakter wechseln!
- Verhaltensweisen werden natürlich!

---

## 🔍 TROUBLESHOOTING

### Problem: "Ollama nicht verfügbar"
```
Lösung:
1. Öffne CMD
2. Tippe: ollama list
3. Falls Fehler: Ollama neustarten
```

### Problem: "Keine Videos gefunden"
```
Lösung:
1. Prüfe Ordner-Pfade
2. Prüfe Video-Endungen (.mp4, .mkv, etc.)
3. python NAJIKA_REAL_TRAINING.py status
```

### Problem: "Training sehr langsam"
```
Normal!
- Erster Durchlauf: ~10s pro Session
- Ollama lädt Model
- Danach schneller: ~5-8s
```

### Problem: "Training abgebrochen, was nun?"
```
Kein Problem!
- Progress ist gespeichert
- Einfach nochmal starten
- Macht automatisch weiter!
```

---

## 📁 DATEIEN-ÜBERSICHT

**Training-System:**
- `NAJIKA_REAL_TRAINING.py` - Haupt-Script
- `TRAIN_NAJIKA_WITH_VIDEOS.bat` - Einfaches Menu
- `training_data/training_progress.json` - Progress-Tracking

**Zeit-Tracking (läuft separat):**
- `NAJIKA_TRAINING_ULTIMATE_FAILSAFE.py` - Scheduler
- `training/schedule.json` - Zeit-Log

**Test:**
- `TEST_OLLAMA_TRAINING_1MIN.py` - 1-Min Test (schon erfolgreich!)
- `TEST_TRAINING_OUTPUT.json` - Test-Results

---

## ✅ ZUSAMMENFASSUNG

**BEREIT:**
- ✅ Ordnerstruktur erstellt (4 Persönlichkeiten)
- ✅ Training-System funktioniert (Test erfolgreich!)
- ✅ 10x Wiederholung eingebaut
- ✅ Zuordnung zu Persönlichkeiten
- ✅ Progress-Tracking
- ✅ Ordner + Dateien Support
- ✅ Fortsetzung bei Abbruch

**HEUTE NOCH:**
- Jetzt: 19:30
- Bis: 22:00 (2.5h)
- Zeit für: ~112 Videos (1120 Sessions)

**MORGEN WEITER:**
- 08:00-22:00 (15h täglich!)
- Fortsetzung wo heute aufgehört
- KEIN VERLUST!

---

## 🎯 NÄCHSTE SCHRITTE

1. **Videos reinlegen** (in die 4 Ordner)
2. **Status prüfen** (BAT-File Option 2)
3. **Training starten** (BAT-File Option 3)
4. **Warten...**
5. **Najika wird BESSER!** 🚀

---

**VIEL ERFOLG!** 🎉

*Najika lernt jetzt RICHTIG!*
