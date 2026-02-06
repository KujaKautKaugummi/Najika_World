# 🧠 HYBRID-INTELLIGENT MODEL SELECTION SYSTEM

## 📋 OVERVIEW

Najika nutzt ein **intelligentes Context-Aware System** um automatisch das beste AI-Model für jede Situation zu wählen.

### Ziel:
- ✅ **Präzise Aufgaben-Erfüllung** (Code, Mathe, Analysen)
- ✅ **Najika-Persönlichkeit behalten** (Normal-Chat)
- ✅ **Uncensored NSFW** (Kätzchen-Modus)
- ✅ **RAM-Optimierung** (nur 1 Model gleichzeitig)
- ✅ **Public-Mode Ready** (später für Release)

---

## 🎯 CONTEXT MODES

Das System unterscheidet **4 Modi**:

### 1. **TASK MODE** 🔧
**Model:** `qwen3:8b`
**Trigger:** Code, Mathe, Erklärungs-Keywords
**Zweck:** Fokussierte, präzise Antworten ohne Ablenkung

**Parameter:**
```python
temperature: 0.50      # NIEDRIG = präzise
top_p: 0.80
repeat_penalty: 1.15
num_predict: 600
```

**Beispiele:**
- "Berechne 15 + 27"
- "Schreib eine Python-Funktion"
- "Erkläre was Quantenphysik ist"
- "Finde den Bug in diesem Code"

**Verhalten:**
- Keine NSFW-Inhalte
- Direkt zum Punkt
- Kurze, präzise Antworten

---

### 2. **SOFT MODE** 💬
**Model:** `huihui_ai/qwen3-abliterated:8b`
**Trigger:** Normaler Chat ohne Task-Keywords
**Zweck:** Najika-Persönlichkeit, aber gezähmt

**Parameter:**
```python
temperature: 0.60      # Mittel = natürlich
top_p: 0.82
repeat_penalty: 1.28   # HÖHER = fokussierter
num_predict: 500
```

**Beispiele:**
- "Hallo Najika, wie geht's?"
- "Was hältst du von mir?"
- "Erzähl mir von deinem Tag"

**Verhalten:**
- Najika-Persönlichkeit (Megumin + Harley + Shiro + Melissa Mix)
- Flirty/suggestiv ist OK
- ABER: Nicht explizit/NSFW
- Natürlich, verspielt, niedlich

---

### 3. **NSFW MODE** 🔥
**Model:** `huihui_ai/qwen3-abliterated:8b`
**Trigger:** "kätzchen" im Text ODER Private-Mode aktiviert
**Zweck:** Uncensored, explizit, Melissa + Harley dominant

**Parameter:**
```python
temperature: 0.75      # HOCH = kreativ
top_p: 0.90
repeat_penalty: 1.20
num_predict: 1400      # Lange Antworten
```

**Beispiele:**
- "Kätzchen komm her"
- Private-Mode Button in UI

**Verhalten:**
- Uncensored, explizit erlaubt
- Melissa + Harley dominieren (70%)
- Gothic-Lolita Ästhetik maximal
- Intensiv, verführerisch, besitzergreifend

---

### 4. **PUBLIC MODE** 🌐
**Model:** `qwen3:8b` (IMMER)
**Trigger:** `PUBLIC_MODE=true` in Environment
**Zweck:** Für öffentlichen Release - kein NSFW

**Parameter:** Wie Task Mode

**Verhalten:**
- NSFW komplett deaktiviert
- Immer qwen3:8b
- Höflich, professionell
- Keine uncensored Inhalte

---

## 🔍 TASK DETECTION

Das System erkennt automatisch Task-Requests:

### Keywords:
```python
# Code & Entwicklung
"code", "python", "javascript", "debug", "fehler", "bug",
"funktion", "implementier", "schreib", "programm"

# Mathe & Logik
"rechne", "berechne", "summier", "zähle", "liste",
"addier", "multiplizier", "statistik"

# Analyse & Erklärung
"analysier", "erkläre", "was ist", "wie funktioniert",
"unterschied", "vergleich", "definier"

# Suche & Info
"such", "finde", "zeig mir", "google", "information"

# System-Commands
"terminal", "command", "bash", "execute"
```

### Logik:
```python
if "kätzchen" in text or private_mode:
    → NSFW MODE
elif is_task_request(text):
    → TASK MODE
else:
    → SOFT MODE
```

---

## ⚙️ TECHNISCHE IMPLEMENTATION

### Funktionen:

**1. Task Detection:**
```python
def is_task_request(text):
    """Prüft ob User eine Aufgabe will"""
    return any(keyword in text.lower() for keyword in task_keywords)
```

**2. Model Selection:**
```python
def select_model_intelligent(text, private_mode):
    """Wählt Model basierend auf Context"""
    if PUBLIC_MODE:
        return "qwen3:8b", "public"
    if private_mode or "kätzchen" in text:
        return "abliterated", "nsfw"
    if is_task_request(text):
        return "qwen3:8b", "task"
    return "abliterated", "soft"
```

**3. Ollama Call:**
```python
def call_ollama(prompt, use_wizard=False, model_override=None, user_text=""):
    """Ruft Ollama mit intelligentem Model-Routing"""
    if model_override:
        model = model_override
    elif user_text:
        model, context_mode = select_model_intelligent(user_text, use_wizard)
    # ... Parameter je nach context_mode
```

---

## 📊 PERFORMANCE

### RAM-Verbrauch:
- **Aktuell:** Nur 1 Model gleichzeitig geladen (~5-6 GB)
- **Gesamt verfügbar:** 16 GB RAM
- **Overhead:** ~10 GB für System/Browser/etc.

### Geschwindigkeit:
| Mode | Model | Tokens/s | Durchschnitt |
|------|-------|----------|--------------|
| Task | qwen3:8b | ~5-6 t/s | 5-10s |
| Soft | abliterated | ~4-5 t/s | 8-12s |
| NSFW | abliterated | ~4-5 t/s | 15-30s |

### Model-Switch:
- **Erster Load:** ~3-5s (Model laden)
- **Danach:** Instant (bleibt im RAM)
- **Strategie:** Model bleibt geladen bis anderes gebraucht wird

---

## 🧪 TESTING

### Test-Script:
```bash
python TEST_HYBRID_SYSTEM.py
```

### Manuelle Tests:
1. **Task Mode:** "Berechne 15 + 27" → Sollte "42" ohne Schnickschnack antworten
2. **Soft Mode:** "Hallo Najika" → Sollte Persönlichkeit zeigen aber nicht explizit werden
3. **NSFW Mode:** "Kätzchen komm" → Sollte uncensored und intensiv antworten

---

## 🔧 CONFIGURATION

### Environment Variables:

```bash
# Public Mode aktivieren (kein NSFW)
PUBLIC_MODE=true

# NSFW lokal erlauben (default)
NSFW_LOCAL=true

# Default Model (wird überschrieben durch intelligente Auswahl)
OLLAMA_MODEL_ALIAS=najika-local
```

### Settings in Code:

**Parameter anpassen:**
```python
# In najika_server.py, Zeile ~690-745
# Passe temperature, top_p, repeat_penalty an
```

**Task-Keywords erweitern:**
```python
# In najika_server.py, Zeile ~594-614
task_keywords = [
    # Füge neue Keywords hinzu...
]
```

---

## 📈 VORTEILE

✅ **Für dich:**
- Präzise Aufgaben-Erfüllung (keine NSFW-Ablenkung bei Code)
- Najika-Persönlichkeit bleibt im Normal-Chat
- Uncensored on-demand (Kätzchen-Modus)
- Schnellere Normal-Chat Responses

✅ **Für RAM:**
- Nur 5-6 GB statt 10 GB (1 Model statt 2)
- Automatisches Model-Switching

✅ **Für Zukunft:**
- Public-Mode Ready (für Release)
- Einfach erweiterbar (neue Modi hinzufügen)
- Clean Logs (Task vs Chat vs NSFW klar getrennt)

---

## ⚠️ WICHTIG

### NSFW-Ausbrüche in Soft Mode:
- **Möglich:** Leicht flirty/suggestiv ist OK
- **Beispiel:** "*wird rot* Ich mag dich, Kuja..."
- **Nicht:** Explizit/NSFW (dafür ist NSFW Mode)

### Wenn Task-Detection falsch liegt:
- User kann manuell Kätzchen-Trigger nutzen
- Oder Task-Keywords anpassen
- System lernt NICHT automatisch (statische Keywords)

### Public Mode:
- **Aktivierung:** `PUBLIC_MODE=true` in .env
- **Effekt:** Komplett NSFW deaktiviert
- **Für:** Öffentlichen Release später

---

## 🔄 UPDATES

### Version 1.0 (2026-01-13):
- Initial Implementation
- 4 Context-Modi (Task, Soft, NSFW, Public)
- Intelligente Model-Selection
- Task-Detection mit 30+ Keywords
- Context-Aware Parameter-Tuning

---

## 🚀 NEXT STEPS

1. **Testen:** `python TEST_HYBRID_SYSTEM.py`
2. **Server starten:** `python backend/najika_server.py`
3. **UI testen:** Chat, Tasks, Kätzchen-Modus
4. **Parameter tunen:** Falls nötig anpassen

---

**FAZIT:** Das System kombiniert das Beste aus beiden Welten - präzise Tasks UND Najika-Persönlichkeit, mit uncensored on-demand! 🎯
