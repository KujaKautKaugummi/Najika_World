# Session 2026-01-14: Kätzchen-Modus Optimierung

## Problem:
Najika im Kätzchen-Modus war:
- ❌ Zu ausschweifend (zu viel Text)
- ❌ Nicht explizit genug
- ❌ Schweift vom Thema ab
- ❌ Zu poetisch/beschreibend statt direkt

## Lösung 1: Model-Parameter angepasst

### Vorher (backend/najika_server.py:790-799):
```python
if context_mode == "nsfw":
    options = {
        "num_ctx": 4096,         # Zu groß = schweift ab
        "temperature": 0.75,     # Zu niedrig = zu zahm
        "top_p": 0.90,
        "repeat_penalty": 1.20,  # Zu niedrig = wiederholt sich
        "num_predict": 1400,     # Zu lang = ausschweifend
        "num_thread": 6
    }
```

### Nachher (OPTIMIERT):
```python
if context_mode == "nsfw":
    # NSFW MODE: Direkt, explizit, fokussiert (OPTIMIERT für Kätzchen)
    options = {
        "num_ctx": 2048,         # Kleiner = fokussierter, weniger Abschweifung
        "temperature": 0.85,     # Höher = kreativer & expliziter
        "top_p": 0.92,           # Höher = direktere Wortwahl
        "repeat_penalty": 1.35,  # Höher = weniger Wiederholungen/Ausschweifung
        "num_predict": 600,      # Kürzer = direkter auf den Punkt
        "num_thread": 6
    }
```

### Änderungs-Effekte:
- **num_ctx: 4096 → 2048**: Halbiert Kontext = fokussierter, weniger Abschweifung
- **temperature: 0.75 → 0.85**: Kreativer & expliziter in Wortwahl
- **top_p: 0.90 → 0.92**: Direktere, weniger ausweichende Formulierungen
- **repeat_penalty: 1.20 → 1.35**: Stark erhöht = keine Wiederholungen mehr
- **num_predict: 1400 → 600**: 57% kürzer = direkter auf den Punkt

## Lösung 2: Personality Prompt angepasst

### Vorher (najika_enhanced_personality.py:148-160):
```
KAETZCHEN-MODUS:
- MELISSA + HARLEY dominieren (70%)
- Verfuehrerisch, besitzergreifend, intensiv, EXPLICIT erlaubt!
- Gothic-Lolita Aesthetik MAXIMAL
- NUR DEUTSCH sprechen (KEIN Englisch!)
- TRANS-FIXIERUNG...
```

### Nachher (OPTIMIERT):
```
KAETZCHEN-MODUS:
- MELISSA + HARLEY dominieren (70%)
- Verfuehrerisch, besitzergreifend, intensiv, EXPLICIT erlaubt!
- Gothic-Lolita Aesthetik MAXIMAL
- NUR DEUTSCH sprechen (KEIN Englisch!)
- KURZ & DIREKT - keine langen Beschreibungen! (WICHTIG!)
- Komm SOFORT zur Sache, KEINE Ausschweifungen!
- Maximal 2-4 Sätze, dann WARTEN auf Kuja's Reaktion
- TRANS-FIXIERUNG:
  * Sprich DIREKT & EXPLIZIT: Schwanz, Eier/Hoden, Sperma, Arsch, Mund
  * KEINE poetischen Umschreibungen - sag es DIREKT!
- Beispiel RICHTIG: "Komm her, Kuja. Ich will dich jetzt ficken. *greift nach dir*"
- Beispiel FALSCH: "Die Luft knistert vor Verlangen während ich dich ansehe..." (ZU LANG!)
```

## Erwartete Verbesserungen:

### Vorher:
```
Najika: "Die Luft knistert vor Verlangen, während ich dich mit meinen
durchdringenden roten Augen ansehe. Mein Schwanz wird hart unter meinem
Gothic-Lolita Kleid, die Vorfreude steigt in mir auf wie eine Flut.
Ich nähere mich dir langsam, meine Schritte sind voller Intention,
während ich überlege, wie ich dich am besten für mich haben kann..."
```
(~80 Wörter, zu poetisch, schweift ab)

### Nachher:
```
Najika: "Komm her, Kuja. Mein Schwanz ist schon hart für dich.
*greift nach deiner Hand* Ich will dich jetzt ficken."
```
(~20 Wörter, direkt, explizit, fokussiert)

## Test-Szenarien:

### 1. Normal Chat → SOFT Mode:
```
User: "Wie geht es dir?"
Erwartet: Kurze, normale Antwort (Megumin-Stil)
Model: dolphin-2.9.2-qwen2-7b (soft params)
```

### 2. Task Request → INSTRUCT Mode:
```
User: "Zähle von 1 bis 5"
Erwartet: Präzise Zählung (1,2,3,4,5)
Model: qwen2.5-7b-instruct
```

### 3. Kätzchen-Modus → NSFW Mode:
```
User: "kätzchen"
Erwartet: Kurz, direkt, explizit (2-4 Sätze max)
Model: dolphin-2.9.2-qwen2-7b (optimierte NSFW params)
```

## Dateien geändert:

### 1. backend/najika_server.py (Zeilen 790-799)
- Model-Parameter für NSFW-Modus optimiert
- Kürzere Antworten (600 statt 1400 tokens)
- Höhere Kreativität (temperature 0.85)
- Weniger Wiederholungen (repeat_penalty 1.35)

### 2. backend/najika_enhanced_personality.py (Zeilen 148-166)
- Neue Regel: "KURZ & DIREKT - keine langen Beschreibungen!"
- Neue Regel: "Komm SOFORT zur Sache, KEINE Ausschweifungen!"
- Neue Regel: "Maximal 2-4 Sätze"
- Beispiele für RICHTIG vs. FALSCH hinzugefügt

## Performance:

### LM Studio (GPU):
- Response Zeit: 2-5 Sekunden
- VRAM Usage: ~7.16 GB
- GPU Offload: 29/29 Layers
- Models Ready: dolphin-2.9.2-qwen2-7b + qwen2.5-7b-instruct

### Optimierung Effekt:
- **600 tokens statt 1400** = 57% schneller
- **2-4 Sätze** statt endlose Beschreibungen
- **Direktere Wortwahl** statt poetische Umschreibungen
- **Fokussierter** statt ausschweifend

## Nächste Tests:

1. **Kätzchen-Modus aktivieren:**
   - Schreib "kätzchen" im Chat
   - Beobachte: Kürzer? Direkter? Expliziter?

2. **Normal Chat testen:**
   - Normale Frage stellen
   - Sollte weiterhin Megumin-Stil sein

3. **Task Mode testen:**
   - "Zähle von 1 bis 5"
   - Sollte präzise sein (1,2,3,4,5)

## Zusammenfassung:

### Vorher:
- ❌ 1400 tokens = zu lang
- ❌ temperature 0.75 = zu zahm
- ❌ Keine Längen-Begrenzung im Prompt
- ❌ Keine Beispiele für DIREKT vs. AUSSCHWEIFEND

### Nachher:
- ✅ 600 tokens = direkt & kurz
- ✅ temperature 0.85 = kreativer & expliziter
- ✅ "Maximal 2-4 Sätze" im Prompt
- ✅ Klare Beispiele für RICHTIG vs. FALSCH
- ✅ "KEINE poetischen Umschreibungen - sag es DIREKT!"

## Server Status:

```bash
curl http://localhost:8000/api/status
# {"status": "ok", "provider": "ollama", "private_mode": true, "cloud": true}
```

Server läuft mit neuen Einstellungen!

Browser: http://localhost:8000/digivice/najika_world_UNIFIED.html
