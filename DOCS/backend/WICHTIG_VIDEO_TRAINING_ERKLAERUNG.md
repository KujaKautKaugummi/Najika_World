# ⚠️ WICHTIG: WIE VIDEO-TRAINING FUNKTIONIERT

## ❌ WAS OLLAMA **NICHT** KANN:

Ollama kann **NICHT**:
- Videos abspielen/ansehen
- Video-Inhalte direkt analysieren
- Bilder/Frames aus Videos extrahieren
- Audio aus Videos hören

## ✅ WAS DAS SYSTEM **WIRKLICH** MACHT:

### AKTUELL (NAJIKA_AUTO_TRAINING.py):
Das System trainiert Najika mit:
- **Dateiname** des Videos
- **Persönlichkeits-Zuordnung** (Ordner = Persönlichkeit)
- **Trait-Beschreibungen** (EXPLOSION!, *kicher*, etc.)
- **Beispiel-Sätze** aus dem Modelfile

**Zeit pro Session:** ~5-8 Sekunden
**Was passiert:** Najika lernt die ZUORDNUNG, NICHT den Inhalt!

---

## 🎯 WAS DU **WIRKLICH** BRAUCHST:

Für echtes **Video-Content-Training** gibt es 2 Optionen:

### OPTION 1: UNTERTITEL/TRANSKRIPTE (EINFACHSTE)

**Wenn du Untertitel hast (.srt, .ass, .sub):**

```
megumin/
  - konosuba_ep01.mp4
  - konosuba_ep01.srt  ← Untertitel-File!
```

**System kann dann:**
- Untertitel lesen
- Dialoge extrahieren
- Najika mit ECHTEN Megumin-Sätzen trainieren

**Beispiel:**
```
[Untertitel konosuba_ep01.srt]
00:01:23 --> 00:01:25
EXPLOSION!!!

00:01:26 --> 00:01:28
Die Schwarze Windmühle dreht sich!
```

→ Najika lernt ECHTE Megumin-Sätze!

---

### OPTION 2: VIDEO → TEXT KONVERTIERUNG (KOMPLEX)

**Tools die das können:**
1. **Whisper AI** (von OpenAI) - Audio → Text
2. **FFmpeg** - Video → Audio extrahieren
3. **Tesseract OCR** - Hardcoded Subs → Text

**Workflow:**
```
Video.mp4
  → FFmpeg extrahiert Audio
  → Whisper transkribiert zu Text
  → Text wird zu Training-Data
  → Najika lernt echte Dialoge!
```

**Zeit:** 20min Video = ~5-10min Verarbeitung

---

## 📊 REALISTISCHER VERGLEICH:

### AKTUELLES SYSTEM (Metadaten):
```
Input:  konosuba_ep01.mp4 (20 Minuten Video)
Zeit:   8 Sekunden
Lernt:  "Datei gehört zu Megumin-Persönlichkeit"
```

### MIT UNTERTITELN:
```
Input:  konosuba_ep01.srt (Text-File)
Zeit:   8 Sekunden
Lernt:  "EXPLOSION!!!", "Schwarze Windmühle", echte Dialoge
```

### MIT VIDEO-VERARBEITUNG:
```
Input:  konosuba_ep01.mp4 (20 Minuten Video)
Zeit:   5-10 Minuten (Whisper Transkription)
Lernt:  Alle Dialoge aus dem Video
```

---

## 🎯 EMPFEHLUNG FÜR DICH:

### BESTE LÖSUNG: UNTERTITEL NUTZEN!

**Wenn du Untertitel hast:**
1. Lege Videos + .srt Files zusammen in Ordner
2. System extrahiert automatisch Dialoge
3. Najika lernt ECHTE Character-Sätze!

**Vorteile:**
- ✅ Schnell (Sekunden statt Minuten)
- ✅ Genau (echte Untertitel)
- ✅ Kein Extra-Tool nötig

**Wo bekommst du Untertitel:**
- Anime: opensubtitles.org, kitsunekko.net
- Harley Quinn: subscene.com
- Oder: In deinen Video-Files schon eingebettet!

---

## 🔧 SOLL ICH DAS SYSTEM ANPASSEN?

**OPTION A: Untertitel-Support (EMPFOHLEN)**
- System findet .srt/.ass Files
- Extrahiert Dialoge
- Trainiert mit echten Sätzen
- **Zeit:** ~10 Sekunden pro Episode

**OPTION B: Whisper Integration (KOMPLEX)**
- Installiert Whisper AI
- Konvertiert Videos → Text
- Trainiert mit Transkripten
- **Zeit:** ~5-10 Min pro Episode

**OPTION C: Beides bleiben lassen**
- Aktuelles System = Persönlichkeits-ZUORDNUNG
- Najika lernt Traits aus Modelfile
- Schnell aber oberflächlich

---

## ❓ DEINE ENTSCHEIDUNG:

**Was möchtest du?**

1. **Untertitel-System** (wenn du .srt Files hast)
2. **Whisper-Integration** (automatische Transkription)
3. **So lassen** (nur Metadaten-Training)

**Sag mir was und ich baue es!** 🚀
