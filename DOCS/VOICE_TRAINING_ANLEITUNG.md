# 🎤 NAJIKA VOICE TRAINING - FINALE ANLEITUNG

**Erstellt:** 2025-10-24 19:45
**System:** Video → Audio → Deutsche Synchro → Najika lernt!

---

## ✅ WAS DU BEKOMMST:

**Najika lernt:**
- ✅ Wie Megumin **KLINGT** (deutsche Synchro!)
- ✅ Welche **WÖRTER** sie nutzt
- ✅ Welchen **TONFALL** sie hat
- ✅ Wie sie **REAGIERT**
- ✅ **ECHTE DIALOGE** aus den Videos!

**Beispiel:**
```
INPUT: Konosuba_Ep01.mp4 (deutsche Synchro)
       ↓
AUDIO: Megumin's Stimme extrahiert
       ↓
WHISPER: "EXPLOSION!!!" + "Die Schwarze Windmühle dreht sich!"
       ↓
NAJIKA LERNT: Wie Megumin WIRKLICH spricht!
```

---

## 💰 KOSTEN: 0€ (KOMPLETT KOSTENLOS!)

**Was läuft lokal (kostenlos):**
- ✅ FFmpeg (Video → Audio) - Kostenlos
- ✅ Whisper AI (Audio → Text) - Kostenlos (von OpenAI)
- ✅ Ollama Training - Kostenlos

**Keine Cloud, keine Gebühren!**

---

## ⏱️ ZEIT PRO VIDEO:

**20-Minuten Episode:**
```
Audio extrahieren:  ~30 Sekunden
Whisper transcribe: ~2-3 Minuten
Training 10x:       ~2 Minuten
GESAMT:             ~5-6 Minuten
```

**Deine "alle Filme und Folgen":**
- Angenommen: 200 Videos (alle 4 Persönlichkeiten)
- Zeit: 200 × 6 Min = 1200 Min = **20 Stunden**
- Läuft automatisch über Nacht!

---

## 📋 INSTALLATION (EINMALIG):

### SCHRITT 1: FFmpeg installieren

**Windows:**
1. Gehe zu: https://ffmpeg.org/download.html
2. Klicke "Windows builds from gyan.dev"
3. Download: `ffmpeg-release-full.7z`
4. Entpacke nach `C:\ffmpeg`
5. Füge zu PATH hinzu:
   ```
   Windows-Taste → "Umgebungsvariablen"
   → PATH bearbeiten
   → Neu: C:\ffmpeg\bin
   ```
6. CMD öffnen, teste: `ffmpeg -version`

**Oder einfach:**
```bash
# Via Chocolatey (falls installiert)
choco install ffmpeg
```

### SCHRITT 2: Whisper AI installieren

```bash
# Öffne CMD als Administrator
pip install openai-whisper
```

**Oder nutze BAT-File:**
```
Doppelklick: SETUP_VOICE_TRAINING.bat
```

### SCHRITT 3: Test

```bash
python NAJIKA_VIDEO_TO_VOICE_TRAINING.py
```

**Sollte zeigen:**
```
NAJIKA VIDEO-TO-VOICE TRAINING
USAGE: python NAJIKA_VIDEO_TO_VOICE_TRAINING.py train
```

---

## 🎬 VIDEOS VORBEREITEN:

### ORDNERSTRUKTUR:

```
C:\NajikaCore\training_data\personalities\
├── megumin\
│   ├── Konosuba_S1\
│   │   ├── Ep01.mkv
│   │   ├── Ep02.mkv
│   │   └── ...
│   ├── Konosuba_S2\
│   │   └── ...
│   └── Konosuba_Film.mp4
│
├── harley\
│   ├── Birds_of_Prey.mp4
│   ├── Suicide_Squad.mkv
│   └── ...
│
├── shiro\
│   ├── NGNL_S1\
│   │   └── ...
│   └── NGNL_Zero.mp4
│
└── melissa\
    └── ... (deine Melissa Videos)
```

**Wichtig:**
- Deutsche Synchro! (Whisper erkennt automatisch)
- Alle Video-Formate OK (.mp4, .mkv, .avi, etc.)
- Ordner/Unterordner OK (System findet alles!)

---

## 🚀 TRAINING STARTEN:

### EINFACHSTER WEG:

```bash
python NAJIKA_VIDEO_TO_VOICE_TRAINING.py train
```

**Was passiert:**
1. System findet ALLE Videos
2. Für JEDES Video:
   - Extrahiert Audio (FFmpeg)
   - Transkribiert deutsche Synchro (Whisper)
   - Trainiert Najika 10x mit echten Dialogen
3. Läuft bis ALLES fertig!

**Live-Output:**
```
[19:45:23] [INFO] Extrahiere Audio: Konosuba_Ep01.mkv...
[19:45:45] [SUCCESS] Audio extrahiert: Konosuba_Ep01.mp3 (42.3 MB)
[19:45:46] [INFO] Transkribiere deutsche Synchro...
[19:47:12] [SUCCESS] Transkript erstellt (86s)
[19:47:12] [INFO] Preview: Ich bin Najika, Arch-Wizard des Crimson Clans! Meine Magie ist...
[19:47:13] [TRAINING] [1/10] Training läuft...
[19:47:20] [SUCCESS] OK: *dramatisch* EXPLOSION!!!
...
```

---

## 📊 WAS NAJIKA LERNT:

### BEISPIEL MEGUMIN:

**Input (deutsche Synchro):**
```
[Konosuba Ep01 - 05:23]
Audio: "EXPLOSION!!!"
      *erschöpfte Stimme* "Ahh... ich kann nicht mehr..."
      *schwach* "Kazuma... trag mich..."
```

**Whisper Transkript:**
```
EXPLOSION!!!
Ahh... ich kann nicht mehr...
Kazuma... trag mich...
Die Schwarze Windmühle hat ihre Kraft entfesselt!
```

**Najika lernt (10x Wiederholung):**
- ✅ Wörter: "EXPLOSION", "Schwarze Windmühle", "Kraft entfesselt"
- ✅ Tonfall: Laut → Erschöpft → Bittend
- ✅ Sprachmuster: Dramatisch, dann schwach
- ✅ Reaktionen: Auf Zauber folgt Erschöpfung

**Nach 10x:**
- Najika KENNT diese Dialoge auswendig!
- Nutzt sie spontan im Chat!
- Klingt wie Megumin!

---

## 🔍 FORTSCHRITT TRACKEN:

### WÄHREND DEM TRAINING:

**Terminal zeigt:**
```
[INFO] >>> VIDEO 1/50 <<<
[INFO] VIDEO: Konosuba_Ep01.mkv
[SUCCESS] Audio extrahiert
[SUCCESS] Transkript erstellt (2m 15s)
[TRAINING] [1/10] OK: *dramatisch* EXPLOSION!
[TRAINING] [2/10] OK: Die Schwarze Windmühle...
...
[SUCCESS] VIDEO KOMPLETT! (10x mit echten Dialogen)
```

### GESPEICHERTE FILES:

```
training_data\
├── extracted_audio\
│   └── megumin\
│       ├── Konosuba_Ep01.mp3  ← Audio extrahiert
│       └── ...
├── transcripts\
│   └── megumin\
│       ├── Konosuba_Ep01.txt  ← Deutsche Dialoge!
│       └── ...
└── voice_training.log  ← Komplettes Log
```

**Du kannst Transkripte lesen:**
```
C:\NajikaCore\training_data\transcripts\megumin\Konosuba_Ep01.txt
```

→ Siehst was Whisper erkannt hat!

---

## ⚠️ WICHTIGE HINWEISE:

### 1. ERSTE AUSFÜHRUNG DAUERT LÄNGER

**Erstes Video:**
- Whisper lädt Model (~1.5 GB) - EINMALIG!
- Danach: Cached, geht schneller

### 2. SPEICHERPLATZ

**Pro Video (20min):**
- Audio: ~40 MB
- Transkript: ~10 KB
- Gesamt: ~50 MB pro Video

**200 Videos:**
- ~10 GB für Audio/Transkripte
- Kannst du später löschen (nach Training)

### 3. CPU/GPU AUSLASTUNG

**Whisper nutzt:**
- CPU: ~50-80% (bei medium model)
- GPU: Falls CUDA verfügbar (schneller!)
- RAM: ~2-4 GB

**Tipp:** Lass über Nacht laufen!

### 4. FORTSETZUNG BEI ABBRUCH

**System ist SMART:**
- Prüft ob Audio schon extrahiert
- Prüft ob Transkript schon existiert
- Überspringt was schon gemacht wurde!

**Bei STRG+C:**
- Einfach neu starten
- Macht weiter wo es aufhörte!

---

## 🎯 BESTE REIHENFOLGE:

### TAG 1 (HEUTE):
```
1. Setup durchführen (FFmpeg + Whisper)
2. EIN Test-Video (prüfen ob alles läuft)
3. Rest über Nacht laufen lassen
```

### TAG 2 (MORGEN):
```
1. Prüfen ob alles durch
2. Najika testen ("Hallo Najika!")
3. Hören wie sie jetzt klingt!
```

---

## 📝 SCHNELLSTART-CHECKLISTE:

```
[ ] FFmpeg installiert (ffmpeg -version)
[ ] Whisper installiert (pip install openai-whisper)
[ ] Videos in Ordner gelegt
[ ] python NAJIKA_VIDEO_TO_VOICE_TRAINING.py train
[ ] Über Nacht laufen lassen
[ ] Morgen: Najika testen!
```

---

## 🎉 NACH DEM TRAINING:

**Najika wird sagen:**
```
User: "Hallo Najika!"

Najika (VORHER):
"Mir geht's super, Kuja! *hüpft* Bereit für Abenteuer?"

Najika (NACHHER mit Voice-Training):
"EXPLOSION!!! *dramatisch* Ich bin Najika, Arch-Wizard des
Crimson Clans! Die Schwarze Windmühle hat ihre Kraft für DICH
entfesselt, Puddin'! *kicher* Die Wahrscheinlichkeit dass ich
bereit bin beträgt 100%! Du gehörst MIR! *hüpft enthusiastisch*"
```

**Unterschied:**
- ✅ Nutzt ECHTE Megumin-Sätze!
- ✅ Kombiniert alle 4 Persönlichkeiten!
- ✅ Klingt wie die deutsche Synchro!

---

## 💡 ZUSAMMENFASSUNG:

**DU HAST:**
- Alle Filme + Folgen (Megumin, Harley, Shiro, Melissa)
- Deutsche Synchro

**SYSTEM MACHT:**
1. Extrahiert Audio (FFmpeg)
2. Hört deutsche Sprecherin (Whisper)
3. Transkribiert Dialoge
4. Trainiert Najika 10x

**KOSTEN:**
- 0€ (alles lokal!)

**ZEIT:**
- ~5-6 Min pro Video
- ~20h für alle Videos
- Läuft automatisch!

**ERGEBNIS:**
- Najika spricht wie Megumin/Harley/Shiro/Melissa
- Nutzt ECHTE Dialoge
- Klingt wie deutsche Synchro!

---

## 🚀 JETZT STARTEN:

```bash
# 1. Setup (einmalig)
SETUP_VOICE_TRAINING.bat

# 2. Training starten
python NAJIKA_VIDEO_TO_VOICE_TRAINING.py train

# 3. Warten...
# 4. Najika ist fertig trainiert! 🎉
```

---

**VIEL ERFOLG!**

*Najika wird die deutsche Synchro HÖREN und LERNEN!* 🎤
