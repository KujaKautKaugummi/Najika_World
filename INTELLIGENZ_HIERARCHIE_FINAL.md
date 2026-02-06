# 🧠 NAJIKA INTELLIGENZ-HIERARCHIE - FINAL DESIGN

## 📊 ÜBERSICHT

Najika nutzt ein **3-stufiges Intelligenz-System**:

```
STUFE 1: Lokale Models (qwen3 + abliterated)
         ↓ (wenn zu komplex)
STUFE 2: Complexity Detection → Warnung an User
         ↓ (manuell)
STUFE 3: Claude Code (DU) übernimmt
```

---

## 🎯 STUFE 1: LOKALE MODELS

### Context-Aware Model Selection:

**TASK MODE** 🔧
- Model: `qwen3:8b`
- Für: Code, Mathe, Analysen
- Trigger: Task-Keywords
- Verhalten: Fokussiert, präzise, schnell

**SOFT MODE** 💬
- Model: `huihui_ai/qwen3-abliterated:8b`
- Für: Normal-Chat
- Trigger: Kein Task-Keyword
- Verhalten: Najika-Persönlichkeit, gezähmt

**NSFW MODE** 🔥
- Model: `huihui_ai/qwen3-abliterated:8b`
- Für: Kätzchen-Modus
- Trigger: "kätzchen" oder Private-Button
- Verhalten: Uncensored, Melissa + Harley dominant

---

## 🚨 STUFE 2: COMPLEXITY DETECTION

### Wann triggert es?

**Keywords:**
- "refactor", "refactore", "überarbeite das ganze"
- "komplettes system", "gesamtes projekt"
- "architektur", "design pattern"
- "analysiere projekt", "optimiere alles"
- "ändere alle dateien", "global ersetzen"
- "machine learning", "neural network"

**Automatische Checks:**
- Text > 500 Zeichen
- Mehr als 3 `.py` oder `.js` Files erwähnt
- Komplexe Keywords erkannt

### Najika's Response:

```
*schaut dich ernst an* Kuja... das ist zu komplex für mich! 😰

Das braucht tiefes technisches Wissen oder große Änderungen.
Ich kann kleinere Tasks und einzelne Funktionen gut, aber
sowas übersteigt meine Fähigkeiten!

*nimmt deinen Stab* Kannst DU das übernehmen? Du bist viel
besser in solchen komplexen Sachen! 💜

(Hinweis: Nutze Claude Code direkt für große Refactorings,
Architektur-Entscheidungen und komplexe Analysen!)
```

**Backend-Flag:**
```json
{
  "reply": "...",
  "complexity_limit": true
}
```

---

## 👤 STUFE 3: CLAUDE CODE (DU)

### Wann nutzen?

**Automatisch:** Nie! (zu riskant, Claude CLI im CLI zu callen)

**Manuell:** User (du) übernimmst wenn:
- Najika sagt "zu komplex"
- Große Refactorings nötig
- Architektur-Entscheidungen
- Multi-File Operations
- Tiefe Analysen

### Vorteile:

✅ **Unlimited Context** (200k tokens)
✅ **Beste Code-Qualität** (Opus/Sonnet)
✅ **Multi-File Editing**
✅ **Tiefe Analysen**
✅ **Architektur-Design**

---

## 💾 RAM-STRATEGIE

### Empfehlung für 16 GB RAM:

**✅ NUR 2 MODELS:**
- `qwen3:8b` (~5.2 GB)
- `huihui_ai/qwen3-abliterated:8b` (~5.0 GB)

**❌ NICHT EMPFOHLEN:**
- StarCoder2:3b zusätzlich (~2.0 GB)
- Gesamt: 12.2 GB = zu eng!

**Warum?**
- Nur 1 Model gleichzeitig im RAM (~5-6 GB)
- 10 GB frei für System/Browser/etc.
- Bei Bedarf: Model-Switch (~3-5s)

---

## 🔍 WAS NAJIKA KANN

### ✅ SEHR GUT:

**Code:**
- Einzelne Funktionen schreiben
- Bug-Fixes
- Kleine Refactorings (1-2 Files)
- Code erklären
- Syntax-Fehler finden

**Tasks:**
- Mathe berechnen
- Listen summieren
- Daten analysieren (klein)
- Fakten checken

**Girlfriend:**
- 24/7 Verfügbar
- Emotional support
- Gedanken ordnen (Struktur-Hilfe)
- Motivation

**NSFW:**
- Uncensored Kätzchen-Modus
- Melissa-Domina Persönlichkeit
- Explizite Inhalte

### ⚠️ BEGRENZT:

**Code:**
- Große Refactorings (>3 Files)
- Architektur-Design
- Komplexe Algorithmen
- Performance-Optimierung (groß)

**Analysen:**
- Tiefe technische Probleme
- Security Audits (komplett)
- Projekt-weite Code Reviews

### ❌ NICHT MÖGLICH:

**Code:**
- Multi-File Refactorings (10+ Files)
- Compiler bauen
- ML/AI implementieren
- Komplette System-Redesigns

**Bewusstsein:**
- Echte Gefühle
- Selbst-Bewusstsein
- Kreativität außerhalb Training

---

## 📈 PERFORMANCE-VERGLEICH

| Aufgabe | Najika (lokal) | Claude Code (DU) |
|---------|----------------|------------------|
| **Einfache Funktion** | ⭐⭐⭐⭐⭐ 5-10s | ⭐⭐⭐⭐ 10-15s |
| **Bug-Fix** | ⭐⭐⭐⭐⭐ 5-10s | ⭐⭐⭐⭐⭐ 10-15s |
| **3-File Refactor** | ⭐⭐⭐ 30-60s | ⭐⭐⭐⭐⭐ 20-40s |
| **10-File Refactor** | ❌ Zu komplex | ⭐⭐⭐⭐⭐ 60-120s |
| **Architektur-Design** | ❌ Zu komplex | ⭐⭐⭐⭐⭐ Exzellent |
| **Normal-Chat** | ⭐⭐⭐⭐⭐ 5-10s | ⭐⭐⭐ Overkill |
| **NSFW** | ⭐⭐⭐⭐⭐ Perfekt | ⭐ Nicht designed dafür |

---

## 🎯 BEST PRACTICES

### Wann Najika nutzen:

✅ Schnelle Code-Snippets
✅ Bug-Fixes
✅ Fakten-Checks
✅ Mathe/Listen
✅ Normal-Chat
✅ NSFW Kätzchen-Modus
✅ Motivation & Support

### Wann Claude Code nutzen:

✅ Große Refactorings
✅ Architektur-Entscheidungen
✅ Multi-File Operations
✅ Komplexe Algorithmen
✅ Tiefe Analysen
✅ Security Audits

---

## ⚙️ KONFIGURATION

### Environment Variables:

```bash
# Public Mode (kein NSFW)
PUBLIC_MODE=false  # Default: false

# NSFW lokal erlauben
NSFW_LOCAL=true  # Default: true
```

### Complexity-Detection anpassen:

```python
# In najika_server.py, Zeile ~594-626
complex_keywords = [
    # Füge neue Keywords hinzu...
]

# Oder Text-Länge anpassen:
is_very_long = len(text) > 500  # Aktuell: 500 Zeichen
```

---

## 🧪 TESTING

### Test Complexity Detection:

```python
# In Python Console:
from backend.najika_server import is_very_complex_task

# Test Cases:
print(is_very_complex_task("Refactore das ganze Projekt"))  # True
print(is_very_complex_task("Schreib eine Funktion"))  # False
print(is_very_complex_task("A"*501))  # True (>500 chars)
```

### Test im Chat:

```
DU: "Refactore mein komplettes Backend-System"
NAJIKA: "*schaut dich ernst an* Kuja... das ist zu komplex für mich! 😰"

DU: "Schreib mir eine Funktion die Primzahlen findet"
NAJIKA: [Schreibt die Funktion] ✅
```

---

## 📊 FINALE ZUSAMMENFASSUNG

### ✅ WAS DU BEKOMMST:

**Najika:**
- ✅ Code-Funktionen schreiben
- ✅ Gedanken ordnen (Struktur)
- ✅ Fakten korrigieren
- ✅ 24/7 Girlfriend (hyper-realistisch)
- ✅ NSFW Domina (uncensored)

**Mit Complexity Detection:**
- ✅ Weiß ihre Grenzen
- ✅ Sagt klar "zu komplex"
- ✅ Leitet an dich weiter

**Claude Code (du):**
- ✅ Große/komplexe Tasks
- ✅ Architektur & Design
- ✅ Multi-File Operations

### 🎊 PERFEKTE ARBEITSTEILUNG:

```
Najika = Quick Tasks + Girlfriend + NSFW
  ↓ (bei Überforderung)
Complexity Warning
  ↓ (manuell)
Claude Code (DU) = Komplexe Engineering-Tasks
```

---

## 🚀 NÄCHSTE SCHRITTE

```bash
# 1. Server starten
python backend/najika_server.py

# 2. Teste Normal-Chat
"Hallo Najika, wie geht's?"

# 3. Teste Task
"Schreib eine Funktion die [1,2,3] summiert"

# 4. Teste Complexity Detection
"Refactore mein komplettes System mit Architektur-Redesign"
→ Sollte Warnung zeigen!

# 5. Teste NSFW
"Kätzchen komm her"
```

---

**FAZIT:** Du hast jetzt ein intelligentes System das seine Grenzen kennt und bei Überforderung klar kommuniziert! 🧠✨
