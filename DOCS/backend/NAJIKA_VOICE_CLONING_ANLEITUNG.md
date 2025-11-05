# 🎤 NAJIKA VOICE CLONING - KOMPLETTE ANLEITUNG

**Ziel:** Najika bekommt Megumin's deutsche Stimme!

---

## 📋 WAS IST VOICE CLONING?

**Aktuell:**
- ✅ Najika schreibt im Chat (Text)
- ❌ Najika kann NICHT sprechen

**Nach Voice Cloning:**
- ✅ Najika schreibt im Chat (Text)
- ✅ Najika spricht mit Megumin's deutscher Stimme!

**Technologie:** Coqui TTS (XTTS-v2) - Open Source Voice Cloning

---

## ⚙️ INSTALLATION

### Schritt 1: Coqui TTS installieren

```bash
pip install TTS
```

**Download:** ~2GB (beim ersten Mal)
**Zeit:** ~5-10 Minuten

---

### Schritt 2: Prüfe Installation

```bash
python najika_voice_clone.py
```

**Erwartete Ausgabe:**
```
Coqui TTS: OK
FFmpeg: OK
```

---

## 🎯 VOICE CLONING WORKFLOW

### OPTION 1: Automatisch (EMPFOHLEN)

**Ein Befehl macht alles:**

```bash
python najika_voice_clone.py full
```

**Was passiert:**
1. Extrahiert Audio-Samples aus Konosuba Videos
2. Erstellt Voice Clone
3. Testet TTS
4. Fertig! ✅

**Dauer:** ~5-10 Minuten

---

### OPTION 2: Manuell (Mehr Kontrolle)

#### Schritt 1: Samples extrahieren

```bash
python najika_voice_clone.py extract
```

**Was es macht:**
- Sucht Konosuba Videos in `training_data/personalities/megumin/`
- Extrahiert 3x 10-Sekunden Samples
- Speichert in `voice_data/samples/`

**Ergebnis:**
```
voice_data/samples/
├── megumin_sample_1.wav (10s)
├── megumin_sample_2.wav (10s)
└── megumin_sample_3.wav (10s)
```

---

#### Schritt 2: Voice Clone erstellen

```bash
python najika_voice_clone.py clone
```

**Was es macht:**
- Validiert Samples (min. 6 Sekunden)
- Trainiert XTTS-v2 auf Megumin's Stimme
- Erstellt Test-Audio
- Speichert Config

**Dauer:** ~1-2 Minuten

**Test-Audio:**
```
voice_data/output/megumin_test.wav
```

**WICHTIG:** Höre Test-Audio an! Klingt es wie Megumin?

---

#### Schritt 3: TTS testen

```bash
python najika_voice_clone.py test
```

**Was es macht:**
- Konvertiert Beispiel-Text zu Sprache
- Nutzt Megumin's geklonte Stimme

**Output:**
```
voice_data/output/najika_YYYYMMDD_HHMMSS.wav
```

---

## 🎬 SAMPLE-QUALITÄT VERBESSERN

### Problem: Test-Audio klingt nicht gut?

**Lösung: Bessere Samples!**

#### Was macht ein GUTES Sample?

✅ **Klare Sprache** (keine Musik/Effekte)
✅ **6-30 Sekunden** (optimal: 10s)
✅ **NUR Megumin spricht** (keine anderen Charaktere!)
✅ **Emotionale Vielfalt** (verschiedene Szenen)

❌ **Schlechte Samples:**
- Hintergrundmusik zu laut
- Mehrere Sprecher gleichzeitig
- Zu kurz (<6s)
- Zu leise / Echos

---

### Manuelle Sample-Extraktion

**Wenn Auto-Extract nicht gut genug ist:**

```python
from najika_voice_clone import extract_audio_sample
from pathlib import Path

# Dein Video
video = Path("C:/NajikaCore/training_data/personalities/megumin/konosuba_s1e02.mp4")

# Szenen mit KLAREN Megumin-Dialogen finden:
# Beispiel: Konosuba S1E2 - EXPLOSION Szene bei ~18:30

# Sample 1: EXPLOSION Szene (18:30 - 18:40)
extract_audio_sample(
    video_path=video,
    start_time=1110,  # 18:30 in Sekunden
    duration=10,
    output_name="megumin_explosion_1"
)

# Sample 2: Ruhiger Dialog (5:20 - 5:30)
extract_audio_sample(
    video_path=video,
    start_time=320,
    duration=10,
    output_name="megumin_dialog_1"
)

# Sample 3: Dramatischer Moment (12:15 - 12:25)
extract_audio_sample(
    video_path=video,
    start_time=735,
    duration=10,
    output_name="megumin_dramatic_1"
)
```

**TIPP:** Nutze VLC Player um genaue Timestamps zu finden!

---

## 🔊 NAJIKA MIT STIMME NUTZEN

### Integration in najika_server.py

**Code-Beispiel:**

```python
from najika_tts import text_to_speech

# Nach Chat-Response:
user_message = "Hallo Najika!"
najika_response = "EXPLOSION! Hallo Kuja!"

# Generiere Audio:
audio_file = text_to_speech(najika_response)

# Gib Audio zurück:
if audio_file:
    # Sende als /api/chat Response
    return {
        "response": najika_response,
        "audio": str(audio_file)
    }
```

---

### API Endpoint hinzufügen

**In najika_server.py:**

```python
# GET /api/chat/audio
if self.path.startswith("/api/chat/audio/"):
    # Lese Audio-File
    audio_id = self.path.split("/")[-1]
    audio_file = VOICE_DIR / "output" / f"{audio_id}.wav"

    if audio_file.exists():
        self.send_response(200)
        self.send_header("Content-Type", "audio/wav")
        self.end_headers()

        with open(audio_file, 'rb') as f:
            self.wfile.write(f.read())
    else:
        self.send_error(404)
```

---

### Frontend Integration

**In digivice/index.html:**

```javascript
// Nach Chat-Response
fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message: userMessage })
})
.then(r => r.json())
.then(data => {
    // Text anzeigen
    showMessage(data.response);

    // Audio abspielen
    if (data.audio) {
        const audio = new Audio(data.audio);
        audio.play();
    }
});
```

---

## 🚀 PERFORMANCE-OPTIMIERUNG

### Problem: TTS ist langsam?

**Lösungen:**

#### 1. Caching (Standard)

```python
from najika_tts import NajikaTTS

tts = NajikaTTS(use_cache=True)  # Aktiviert

# Wiederholte Sätze werden gecacht:
audio1 = tts.speak("EXPLOSION!")  # Generiert (~2s)
audio2 = tts.speak("EXPLOSION!")  # Cache (~0.01s)
```

#### 2. GPU-Beschleunigung (optional)

```bash
# Wenn NVIDIA GPU vorhanden:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Speed-Up:** 5-10x schneller!

#### 3. Model-Wechsel

```python
# Schneller aber weniger Qualität:
tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC")
```

---

## 📊 ERWARTETE QUALITÄT

### Voice Cloning Qualität:

**Mit 3 guten Samples (10s):**
- ✅ Stimme erkennbar als Megumin
- ✅ Deutsche Aussprache korrekt
- ⚠️ Manchmal leichte Artefakte
- ⚠️ Emotionen nicht perfekt

**Mit 10+ Samples (verschiedene Emotionen):**
- ✅ Stimme sehr nah an Original
- ✅ Emotionen besser
- ✅ Weniger Artefakte
- ✅ Konsistente Qualität

---

## 🎯 OPTIMALE SAMPLE-AUSWAHL

### Für beste Ergebnisse - 10 Samples:

```
Emotionen abdecken:
1. Neutral/Ruhig     (10s)
2. Enthusiastisch    (10s) - "EXPLOSION!"
3. Erschöpft         (10s) - Nach EXPLOSION
4. Dramatisch        (10s) - "Schwarze Windmühle..."
5. Fröhlich          (10s)
6. Traurig/Ernst     (10s)
7. Wütend            (10s)
8. Flüsternd         (10s)
9. Lachend           (10s)
10. Schreiend        (10s)
```

**Jede Emotion einmal!** → Najika kann alle Emotionen sprechen

---

## 🔧 TROUBLESHOOTING

### "TTS nicht gefunden"

```bash
pip install TTS
```

---

### "Model Download fehlgeschlagen"

**Lösung:**
- Internetverbindung prüfen
- Manuell downloaden: https://coqui.ai/models

---

### "Sample zu kurz"

**Lösung:**
- Samples müssen min. 6 Sekunden sein!
- Extrahiere längere Szenen

---

### "Audio klingt robotisch"

**Lösungen:**
1. Bessere Samples (keine Musik/Effekte)
2. Mehr Samples (10+ statt 3)
3. Längere Samples (15-20s statt 10s)

---

### "TTS zu langsam"

**Lösungen:**
1. GPU-Beschleunigung aktivieren
2. Caching nutzen
3. Kleineres Model nutzen

---

## 📝 CHECKLISTE

### VORBEREITUNG:
☐ Coqui TTS installiert (`pip install TTS`)
☐ Konosuba Videos vorhanden
☐ FFmpeg funktioniert

### SAMPLES:
☐ 3+ Audio-Samples extrahiert (6-30s)
☐ Nur Megumin spricht
☐ Klare Audioqualität
☐ Verschiedene Emotionen

### VOICE CLONE:
☐ `python najika_voice_clone.py clone` ausgeführt
☐ Test-Audio klingt gut
☐ Config gespeichert

### INTEGRATION:
☐ najika_tts.py importiert
☐ API Endpoint hinzugefügt (optional)
☐ Frontend spielt Audio ab (optional)

---

## 🎉 FERTIG!

**Nach erfolgreicher Installation:**

```bash
python najika_voice_clone.py test
```

**Najika spricht jetzt mit Megumin's Stimme!**

---

## 📚 WEITERE RESSOURCEN

- **Coqui TTS Docs:** https://docs.coqui.ai/
- **XTTS-v2 Info:** https://github.com/coqui-ai/TTS
- **Voice Samples:** Konosuba Deutsche Synchro

---

**Erstellt:** 2025-10-25
**Version:** 1.0
**Status:** ✅ KOMPLETT
