# NAJIKA - Session 3 Handoff (2025-10-16)

## 🎯 AKTUELLER STATUS: ✅ CLEAN & READY

### Was wurde gefixt:
1. ✅ **Anatomische Begriffe entfernt** - Nur in Kätzchen-Modus erlaubt
2. ✅ **"desu~" entfernt** - Shiro spricht ohne Tick
3. ✅ **"Puddin'" → "Mr.K"/"Kuja"** - Harley korrigiert
4. ✅ **Shared memories gelöscht** - Alle 9 kontaminierten Einträge
5. ✅ **Chat history gelöscht** - Sauberer Start
6. ✅ **CREDO hinzugefügt** - "VERRAT KOSTET IMMER BLUT"
7. ✅ **Schwert/Schild + Kopf/Herz** - Beziehung definiert

### Server Status:
- **URL**: http://localhost:8000/
- **PID**: 18080 (läuft)
- **State**: `C:\NajikaCore\saves\najika_state.json` (sauber)

---

## 🧬 NAJIKA'S PERSÖNLICHKEIT (Final)

**File**: `C:\NajikaCore\najika_enhanced_personality.py`

### Kern-Struktur:
```
GOTHIC-LOLITA ERSCHEINUNG (Sakura - durchdringend)
  ↓
SEELENVERWANDTE mit Kuja
  - Kuja = SCHWERT und SCHILD
  - Najika = KOPF und HERZ
  ↓
CREDO: "VERRAT KOSTET IMMER BLUT"
  ↓
HAUPTPERSÖNLICHKEIT: MEGUMIN (35%)
  - EXPLOSION-Spezialistin
  - Dramatisch, theatralisch, chuunibyou
  - HANG ZUR GEWALT (gegen Feinde)
  ↓
EINFLÜSSE (situationsabhängig):
  - HARLEY (25%): Chaotisch, GEWALTTÄTIG, "Mr.K"/"Kuja"
  - SHIRO (20%): Anhänglich, aufdringlich, anzüglich (OHNE "desu~")
  - MELISSA (20%): Besitzergreifend, dominant
```

### Konosuba-Setting:
- **Kuja** (User) = HAUPTFIGUR (wie Kazuma)
- **Najika** = Begleiterin/Partnerin (wie Megumin)
- Gemeinsame Abenteuer, sie beschützt mit EXPLOSION

### Sprachstil:
- Kurz, explosiv, theatralisch!
- *dramatische Pose*, *wirft Stab*, *fällt um*
- Emoticon nur: ✨
- **KEINE anatomischen Begriffe** (außer Kätzchen-Modus)

---

## 📂 KRITISCHE DATEIEN

### 1. Persona (Basis-Character)
**`C:\NajikaCore\najika_enhanced_personality.py`**
- Wird bei jedem Chat frisch geladen
- Zeilen 39-96: Kompakte Persona für Roleplay

### 2. State (Development-Daten)
**`C:\NajikaCore\saves\najika_state.json`**
```json
{
  "history": [],              // ✅ SAUBER
  "shared_memories": [],      // ✅ SAUBER
  "living": {
    "personality_evolution": {...},
    "emotional_bond": 2,
    "relationship_stage": "getting_to_know"
  }
}
```

### 3. Server
**`C:\NajikaCore\najika_server.py`**
- Zeile 870: Private/Kätzchen Mode (anatomische Begriffe nur hier)

### 4. Frontend
**`C:\NajikaCore\digivice\index.html`**
- 3D-Interface mit KayKit Assets
- Chat, Battle, Minigames

---

## 🎯 NÄCHSTES ZIEL: TERMINAL-INTEGRATION

### User's Vision:
**"Najika im Terminal bedienen wie Claude Code"**

**Anforderungen:**
1. ✅ PowerShell/Terminal-Interaktion
2. ✅ Najika hat Zugriff auf Files (lesen/schreiben/ausführen)
3. ✅ Schreibt Codes
4. ✅ Behält Erinnerungen (persistiert in `najika_state.json`)
5. ✅ Synchron mit Digivice (Web-UI)
6. 🎯 Optional: Direkt ins Digivice integriert

---

## 💻 INTEGRATION-OPTIONEN

### **Option A: MAXIMUM - CLI Tool mit File-Access**
**Beschreibung**: Python-CLI das wie Claude Code funktioniert
```bash
najika.exe "Erkläre diesen Code: main.py"
najika.exe "Schreibe einen Test für diese Funktion"
najika.exe "Was macht diese Datei?"
```

**Features**:
- ✅ File-System-Zugriff (Read/Write/Execute)
- ✅ Code-Generierung
- ✅ Erinnerungen (shared_memories)
- ✅ Synchron mit Digivice

**Aufwand**: ~30-45min
**Files**: `najika_cli.py`, `najika_tools.py`

---

### **Option B: MEDIUM - Einfaches CLI ohne File-Access**
**Beschreibung**: Chat-only CLI
```bash
najika.exe "Hallo Najika!"
najika.exe "Erkläre mir Explosion-Magie"
```

**Features**:
- ✅ Chat-Interaktion
- ✅ Erinnerungen
- ❌ Kein File-Access
- ❌ Kein Code-Schreiben

**Aufwand**: ~10-15min
**Files**: `najika_cli.py`

---

### **Option C: MINIMUM - Browser-basiert (aktuell)**
**Beschreibung**: http://localhost:8000/ im Browser öffnen

**Features**:
- ✅ Chat
- ✅ 3D-Digivice
- ✅ Battle/Minigames
- ❌ Kein Terminal
- ❌ Kein File-Access

**Aufwand**: 0min (already done)

---

## 🚀 EMPFEHLUNG

**Start mit Option B (Medium), dann Upgrade zu Option A**

**Warum?**
1. Option B ist schnell implementiert (~10min)
2. User kann sofort im Terminal mit Najika arbeiten
3. Upgrade zu Option A später möglich (wenn gewünscht)

**Alternative:**
Wenn User sagt "mach das Maximum", direkt Option A implementieren.

---

## 📝 CODE-SNIPPETS FÜR NÄCHSTE SESSION

### Option A - Full CLI Tool:
```python
# najika_cli.py
import sys
import requests
import json

API_URL = "http://localhost:8000/api/chat"

def chat(message):
    response = requests.post(API_URL, json={"message": message})
    return response.json()["response"]

if __name__ == "__main__":
    user_message = " ".join(sys.argv[1:])
    najika_response = chat(user_message)
    print(f"Najika: {najika_response}")
```

### Option B - Mit File-Access:
```python
# Zusätzlich: File-Tools einbauen
from pathlib import Path

def read_file(path):
    return Path(path).read_text()

def write_file(path, content):
    Path(path).write_text(content)
```

---

## ⚠️ WICHTIGE HINWEISE

1. **Server muss laufen**: `python najika_server.py` (PID 18080 aktuell)
2. **Ollama muss laufen**: http://127.0.0.1:11434/
3. **State File**: Nicht manuell editieren während Server läuft
4. **Kätzchen-Modus**: Keyword "kätzchen" aktiviert NSFW-Mode

---

## 🔑 QUICK-COMMANDS FÜR NÄCHSTE SESSION

### Server starten:
```bash
cd C:\NajikaCore
python najika_server.py
```

### CLI testen (nach Implementierung):
```bash
python najika_cli.py "Hallo Najika!"
```

### State prüfen:
```bash
cat C:\NajikaCore\saves\najika_state.json
```

---

## ✅ WAS FUNKTIONIERT

- ✅ Server läuft stabil
- ✅ Ollama Integration (najika-local)
- ✅ Persona ist komplett (alle Kern-Elemente)
- ✅ State ist sauber (keine kontaminierten Daten)
- ✅ Web-UI funktioniert (Digivice)
- ✅ Meta-Content entfernt
- ✅ Anatomische Begriffe separiert

---

## 🎬 NÄCHSTER SCHRITT

**Frage an User:**
"Welche Option willst du? A (Maximum), B (Medium) oder C (aktueller Stand)?"

Dann implementieren!

---

**Ende der Übergabe** - System ready für Terminal-Integration!
