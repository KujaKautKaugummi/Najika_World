# 🔧 OLLAMA GPU PROBLEM - LÖSUNG

## ❌ PROBLEM IDENTIFIZIERT

### Symptome
- Ollama nutzt CPU statt GPU (`size_vram: 0`)
- Chat-Antworten dauern 180+ Sekunden
- GPU ist zu 100% ausgelastet mit 7484MB / 8192MB VRAM belegt
- Nur **708MB VRAM frei** - zu wenig für 8B Model (~5GB benötigt)

### Root Cause
**Windows Display Driver Model (WDDM)** verhindert effiziente VRAM-Nutzung:
- Desktop-Rendering belegt ~7GB permanent
- Fragmentierter VRAM-Pool
- Ollama kann keinen zusammenhängenden 5GB-Block allozieren
- Fällt auf CPU-Inferenz zurück → extrem langsam

### GPU Status
```
NVIDIA GeForce RTX 3060 Ti
Driver: 581.15
CUDA: 13.0
VRAM: 7484MB / 8192MB belegt (91%)
GPU-Auslastung: 100%
Temperatur: 62°C
```

### Hauptverbraucher
- Windows Desktop Window Manager (DWM.exe)
- Claude Desktop App
- Windows Shell Components
- Xbox Game Bar
- System UI Components

---

## ✅ LÖSUNG 1: TIMEOUT ERHÖHEN (EINFACH)

### Implementierung
Erhöhe Chat-Timeout von 30s auf 300s (5 Minuten):

**backend/najika_server.py:**
```python
# Erhöhe Ollama Timeout
OLLAMA_TIMEOUT = 300  # 5 Minuten statt 30 Sekunden

def call_ollama(model, prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=OLLAMA_TIMEOUT  # ← Hier
    )
```

**TEST_NAJIKA_SYSTEM.py:**
```python
# Erhöhe Test-Timeout
r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=300)  # 5 Min
```

### Vor-/Nachteile
✅ Einfach zu implementieren
✅ Keine Systemänderungen nötig
❌ Chat bleibt langsam (3-5 Minuten pro Antwort)
❌ Keine echte Performance-Verbesserung

---

## ✅ LÖSUNG 2: KLEINERES MODEL (EMPFOHLEN)

### Implementierung
Wechsel zu `starcoder2:3b` (nur 1.7GB) für Chat:

**backend/najika_server.py:**
```python
def get_model_for_message(text, private_mode=False):
    if PUBLIC_MODE:
        return "starcoder2:3b", "public"  # ← Kleineres Model

    # Kätzchen-Modus: Nutze 7B statt 8B
    if private_mode or "kätzchen" in text.lower():
        return "dolphin-mistral:7b", "nsfw"  # ← 4.1GB statt 5.0GB

    # Normaler Chat: Kleineres Model
    return "starcoder2:3b", "normal"  # ← Schnell auf CPU
```

### Model-Vergleich
| Model | Größe | VRAM | CPU-Speed | GPU-Speed | Use Case |
|-------|-------|------|-----------|-----------|----------|
| qwen3:8b | 5.2GB | Nein | 180s+ | 2-5s | Task/Code |
| qwen3-abliterated:8b | 5.0GB | Nein | 180s+ | 2-5s | NSFW |
| dolphin-mistral:7b | 4.1GB | Teilweise | 120s | 2-4s | NSFW Alt |
| starcoder2:3b | 1.7GB | Ja! | 10-20s | 1-2s | Chat/Code |

### Vor-/Nachteile
✅ Schnelle Antworten (10-20s statt 180s)
✅ Passt in VRAM
✅ Gut für Code/Chat
❌ Weniger Wissen als 8B Models
❌ Schlechteres Deutsch

---

## ✅ LÖSUNG 3: WSL2 MIT GPU (KOMPLEX)

### Implementierung
1. Installiere WSL2: `wsl --install`
2. Installiere Ollama in WSL2
3. Aktiviere GPU-Passthrough
4. Starte Ollama in WSL2

### Vorteile
✅ Direkter GPU-Zugriff ohne WDDM
✅ Volle VRAM-Nutzung möglich
✅ 8B Models mit GPU-Speed

### Nachteile
❌ Komplexe Setup-Prozedur
❌ Zusätzliche Wartung
❌ Windows-WSL2-Interop nötig

---

## ✅ LÖSUNG 4: ALTERNATIVE INFERENCE ENGINE

### LM Studio (Empfohlen für Windows)
- Download: https://lmstudio.ai/
- Native Windows-Optimierung
- Bessere VRAM-Verwaltung als Ollama
- GPU-Beschleunigung auch bei wenig VRAM
- API-kompatibel mit Ollama

### Text Generation WebUI
- Mehr Kontrolle über Model-Loading
- Kann Models in Chunks laden
- Exllama2 Backend für bessere Performance

---

## 🎯 EMPFOHLENE LÖSUNG FÜR NAJIKA

### Kurzfristig (Heute)
**Lösung 2: Kleineres Model für Chat**
```python
# backend/najika_server.py
def get_model_for_message(text, private_mode=False):
    # Fast Chat: starcoder2:3b
    if not private_mode and len(text) < 200:
        return "starcoder2:3b", "fast"

    # NSFW: dolphin-mistral:7b
    if private_mode or "kätzchen" in text.lower():
        return "dolphin-mistral:7b", "nsfw"

    # Complex Tasks: qwen3:8b (akzeptiere langsam)
    if any(kw in text.lower() for kw in ["code", "analyse", "erstelle"]):
        return "qwen3:8b", "task"

    # Default: starcoder2:3b
    return "starcoder2:3b", "normal"
```

### Mittelfristig (Diese Woche)
**Teste LM Studio als Ollama-Ersatz**
- Installiere LM Studio
- Lade qwen3:8b in LM Studio
- Ändere Backend auf LM Studio API
- Teste Performance

### Langfristig (Später)
**WSL2 Setup für optimale Performance**
- Ollama in WSL2 mit direktem GPU-Zugriff
- Oder dedizierter Inference-Server

---

## 📝 NÄCHSTE SCHRITTE

1. **Jetzt:** Model-Auswahl in najika_server.py anpassen
2. **Test:** Chat mit starcoder2:3b testen
3. **Validieren:** Performance-Verbesserung messen
4. **Optional:** LM Studio als Alternative testen

---

## 🔍 DEBUG-BEFEHLE

```bash
# Prüfe VRAM-Auslastung
nvidia-smi --query-gpu=memory.used,memory.total --format=csv

# Prüfe Ollama Model Status
curl http://localhost:11434/api/ps | python -m json.tool

# Entlade alle Models
curl -X POST http://localhost:11434/api/generate -d '{"model":"qwen3:8b","keep_alive":0}'

# Teste Model-Performance
time curl -X POST http://localhost:11434/api/generate -d '{"model":"starcoder2:3b","prompt":"Hi","stream":false}'
```

---

**Status:** GPU-Problem identifiziert, Lösungen dokumentiert
**Empfehlung:** Implementiere Lösung 2 (kleineres Model) für sofortige Verbesserung
