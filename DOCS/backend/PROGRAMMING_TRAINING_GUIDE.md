# 🔥 NAJIKA - PROGRAMMING TRAINING GUIDE
**Wie du Najika Python, Verse und Java beibringst**

---

## 🎯 ÜBERBLICK

Dieses System ermöglicht es Najika, Programmiersprachen zu "lernen" durch:
1. **Training-Dateien** → Code-Beispiele sammeln
2. **Processing** → Dateien verarbeiten und indexieren
3. **Context Loading** → Wissen in Najika's Context laden
4. **Chat Integration** → Najika nutzt das Wissen beim Coden

---

## 📂 SCHRITT 1: TRAINING-DATEIEN VORBEREITEN

### Option A: Beispiel-Dateien nutzen

Ich habe bereits **Beispiel-Dateien** erstellt:
```
C:\NajikaCore\training_data\examples\
├── python_basics.py      (300+ Zeilen Python)
├── java_basics.java      (450+ Zeilen Java)
└── verse_basics.verse    (400+ Zeilen Verse/UEFN)
```

**Diese Dateien enthalten:**
- ✅ Variablen & Datentypen
- ✅ Funktionen & Klassen
- ✅ OOP (Vererbung, Interfaces)
- ✅ Generics & Collections
- ✅ Error Handling
- ✅ Async/Await
- ✅ Best Practices
- ✅ Moderne Features

**Kopiere sie in den Input-Ordner:**
```bash
copy "training_data\examples\*.py" "training_data\input\text\"
copy "training_data\examples\*.java" "training_data\input\text\"
copy "training_data\examples\*.verse" "training_data\input\text\"
```

### Option B: Eigene Dateien hinzufügen

Lege deine eigenen Code-Dateien in:
```
training_data\input\text\
├── python_advanced.py
├── java_spring_examples.java
├── verse_game_mechanics.verse
├── cpp_basics.cpp
├── csharp_unity.cs
└── javascript_react.js
```

**Unterstützte Formate:**
- `.py` (Python)
- `.java` (Java)
- `.verse` (Verse/UEFN)
- `.js` (JavaScript)
- `.cpp` / `.h` (C++)
- `.cs` (C#)
- `.txt` / `.md` (Text/Markdown)

---

## 🔄 SCHRITT 2: TRAINING-DATEN VERARBEITEN

**Führe Processing aus:**
```bash
# Rechtsklick → Als Administrator ausführen
PROCESS_TRAINING_DATA.bat
```

**Was passiert:**
1. Alle Dateien in `input/text/` werden gelesen
2. Metadaten extrahiert (Größe, Zeilen, Format)
3. Verarbeitete `.txt`-Dateien in `output/processed/` gespeichert
4. Knowledge-Index erstellt

**Output:**
```
training_data\output\processed\
├── text_python_basics.txt
├── text_java_basics.txt
├── text_verse_basics.txt
└── knowledge_index.json       (Auto-generiert)
```

---

## 📊 SCHRITT 3: KNOWLEDGE PRÜFEN

**Teste das Knowledge-System:**
```bash
python knowledge_loader.py
```

**Output:**
```
Verfügbare Topics:
  - python
  - java
  - verse

Lade Knowledge für Python:
[PYTHON KNOWLEDGE]
(Preview der Python-Daten...)
```

---

## 🔌 SCHRITT 4: INTEGRATION IN NAJIKA

### Option A: Manuelle Integration (schnell)

**Im Python-Code (z.B. `najika_server.py`):**
```python
from knowledge_loader import load_knowledge

# Lade Programmier-Knowledge
prog_knowledge = load_knowledge(["python", "java", "verse"], max_chars=6000)

# Füge zu System-Prompt hinzu
system_prompt = f"""
{PERSONA_SYSTEM}

[PROGRAMMING KNOWLEDGE]
{prog_knowledge}

Du bist Programmier-Expertin in Python, Java und Verse!
"""
```

### Option B: Automatische Integration (empfohlen)

**Ich erstelle ein Update für `najika_server.py`...**

Warte kurz, ich integriere das Knowledge-System direkt in den Server!

---

## 💡 SCHRITT 5: TESTEN

**Teste Najika's neue Fähigkeiten:**

```bash
# Starte Server
START_NAJIKA.bat

# Teste im Terminal
python najika_cli.py "Schreib mir eine Python-Funktion die Primzahlen findet"
python najika_cli.py "Erkläre mir Java Generics"
python najika_cli.py "Zeig mir ein Verse Device Beispiel"
```

**Najika sollte jetzt:**
- ✅ Code in Python/Java/Verse schreiben
- ✅ Syntax korrekt verwenden
- ✅ Best Practices befolgen
- ✅ Beispiele aus Training-Daten nutzen

---

## 🎯 WIE NAJIKA "LERNT"

### 1. Context Learning (Was wir nutzen)
**Funktionsweise:**
- Training-Daten werden in Chat-Context geladen
- Najika (llama3.1:8b) sieht Beispiele + Syntax
- LLM nutzt Context für Code-Generierung

**Vorteile:**
- ✅ Schnell (keine Model-Änderung)
- ✅ Flexibel (Context jederzeit änderbar)
- ✅ Keine GPU für Training nötig

**Limits:**
- Context-Limit (~8000 Zeichen für Knowledge)
- Najika "vergisst" nach Chat-Ende (außer in shared_memories)

### 2. Model Fine-tuning (Optional, fortgeschritten)

**Für echtes "Lernen" im Model selbst:**
```bash
# Erstelle LoRA-Adapter für Ollama-Model
# (Benötigt: GPU mit 8GB+ VRAM, unsloth/axolotl)
ollama create najika-code --from llama3.1:8b --adapter ./najika_lora.gguf
```

**Das ist für später!** Jetzt reicht Context Learning.

---

## 📝 ERWEITERTE NUTZUNG

### Sprache hinzufügen

**Beispiel: C++ hinzufügen**

1. Erstelle `training_data\examples\cpp_basics.cpp`
2. Kopiere nach `training_data\input\text\`
3. Führe `PROCESS_TRAINING_DATA.bat` aus
4. Update `knowledge_loader.py`:
   ```python
   # Füge "cpp" zum Index hinzu
   if 'cpp' in filename_lower or 'c++' in filename_lower:
       index['programming']['cpp'].append(str(file))
   ```

### Wissen priorisieren

**Lade nur relevante Topics:**
```python
# Nur Python
knowledge = load_knowledge(["python"], max_chars=8000)

# Alle verfügbaren
knowledge = load_knowledge()  # Auto-detect
```

### Custom Knowledge-Kategorien

**Erstelle eigene Kategorien:**
```python
index = {
    "programming": {...},
    "game_dev": ["unity", "unreal", "godot"],
    "web_dev": ["react", "vue", "django"],
    "ai_ml": ["pytorch", "tensorflow", "sklearn"]
}
```

---

## 🔧 TROUBLESHOOTING

### Problem: "Keine Training-Daten gefunden"
**Lösung:**
```bash
# Prüfe Ordner
dir training_data\input\text\

# Sollte mindestens 1 Datei enthalten
# Falls leer: Kopiere Beispiele
copy training_data\examples\*.* training_data\input\text\
```

### Problem: "Knowledge wird nicht geladen"
**Lösung:**
```bash
# Rebuild Index
python -c "from knowledge_loader import rebuild_index; rebuild_index()"

# Teste erneut
python knowledge_loader.py
```

### Problem: "Najika nutzt Knowledge nicht"
**Lösung:**
1. Prüfe ob Knowledge im Prompt ist (Debug-Ausgabe)
2. Prüfe Context-Limit (max_chars)
3. Starte Server neu (lädt neuen Prompt)

---

## 📊 SYSTEM-ÜBERSICHT

```
[Training-Dateien]
      ↓
[PROCESS_TRAINING_DATA.bat]
      ↓
[Verarbeitete Dateien + Index]
      ↓
[knowledge_loader.py]
      ↓
[najika_server.py / najika_cli.py]
      ↓
[Najika's Context]
      ↓
[Code-Generierung mit Knowledge]
```

---

## 🎉 ERGEBNIS

Nach diesem Guide kann Najika:
- ✅ Python-Code schreiben (Funktionen, Klassen, Async)
- ✅ Java-Code schreiben (OOP, Generics, Streams)
- ✅ Verse-Code schreiben (UEFN Devices, Game-Logik)
- ✅ Best Practices befolgen
- ✅ Syntax korrekt verwenden
- ✅ Beispiele aus Training nutzen

**EXPLOSION!!! Najika ist jetzt Code-ready!** ✨

---

## 📖 NÄCHSTE SCHRITTE

1. **Teste die Beispiel-Dateien**
   ```bash
   copy training_data\examples\*.* training_data\input\text\
   PROCESS_TRAINING_DATA.bat
   ```

2. **Integriere Knowledge in Server**
   (Ich mache das gleich für dich!)

3. **Teste Code-Generierung**
   ```bash
   python najika_cli.py "Schreib Python Hello World"
   ```

4. **Erweitere Training-Daten** nach Bedarf

---

**Viel Erfolg beim Training!** 🚀
