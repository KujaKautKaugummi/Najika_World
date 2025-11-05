# NAJIKA LoRA FINE-TUNING SYSTEM

**Echtes permanentes Lernen für Najika!**

---

## 🎯 WAS IST DAS?

Najika lernt **WIRKLICH** durch LoRA Fine-Tuning:
- Konversationen aus ChromaDB werden zum Training genutzt
- LoRA-Adapter wird trainiert (4-bit für RTX 3060 Ti 8GB)
- Adapter wird mit Basis-Modell gemerged
- Neues Modell ersetzt `najika-local` in Ollama

**Resultat:** Najika wird mit jedem Training schlauer!

---

## 📋 VORAUSSETZUNGEN

✅ RTX 3060 Ti (8GB VRAM)
✅ CUDA Toolkit 12.1
✅ Python 3.11
✅ Torch 2.5.1+cu121
✅ PEFT, Transformers, BitsAndBytes, TRL

**Alle bereits installiert!**

---

## 🚀 SETUP

### 1. Auto-Training aktivieren (alle 12h)

```bash
SETUP_LORA_TRAINING_SCHEDULER.bat
```

**Training-Zeiten:**
- 08:00 Uhr (Morning)
- 20:00 Uhr (Evening)

### 2. Manuelles Training

```bash
python najika_lora_training.py
```

**Dauer:** ~15-30 Min (je nach Datenmenge)

---

## 📊 WIE ES FUNKTIONIERT

### Phase 1: Training (najika_lora_training.py)

1. Lädt Konversationen aus ChromaDB
2. Formatiert als Llama3.1 Chat-Template
3. Lädt Basis-Modell (4-bit quantized)
4. Trainiert LoRA-Adapter
5. Speichert Adapter in `lora_checkpoints/`

**Output:**
- `lora_checkpoints/najika_lora_latest/` - LoRA Adapter
- `training_logs/training_TIMESTAMP.json` - Log

### Phase 2: Merge (najika_lora_merge.py)

1. Merged LoRA Adapter mit Basis-Modell
2. Speichert gemerged Modell
3. Konvertiert zu GGUF (Ollama-Format)
4. Update `najika-local` in Ollama

**HINWEIS:** GGUF-Konvertierung erfordert llama.cpp!

---

## 🔧 LLAMA.CPP SETUP (für GGUF)

```bash
# 1. Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# 2. Kompiliere (Windows)
cmake -B build
cmake --build build --config Release

# 3. Konvertiere Modell
python convert.py C:/NajikaCore/merged_models/najika_merged_TIMESTAMP --outtype q4_k_m --outfile C:/NajikaCore/najika-q4.gguf

# 4. Update Ollama
python C:/NajikaCore/najika_lora_merge.py --update-ollama C:/NajikaCore/najika-q4.gguf
```

---

## 📈 TRAINING-DATEN

**Quelle:** ChromaDB Memory System
**Format:** Konversations-Paare (User + Najika)
**Minimum:** 10 Paare für Training

**Mehr Konversationen = besseres Training!**

ChromaDB wächst automatisch mit jedem Gespräch.

---

## ⚙️ KONFIGURATION

### najika_lora_training.py Anpassungen:

```python
# Training-Parameter
epochs=3              # 1-5 (mehr = besser, aber länger)
batch_size=1          # 1-2 (mehr braucht mehr VRAM)
learning_rate=2e-4    # 1e-4 bis 5e-4

# LoRA Config
r=16                  # 8-32 (größer = mehr Parameter)
lora_alpha=32         # 16-64
lora_dropout=0.05     # 0.05-0.1
```

---

## 🎓 WAS NAJIKA LERNT

**Code-Schreiben:**
- Python, JavaScript, Bash
- Debugging & Optimierung
- Architektur-Entscheidungen

**Projektverständnis:**
- NajikaCore Struktur
- Digivice System
- Battle/Minigame Mechaniken

**Persönlichkeit:**
- Megumin, Harley, Shiro, Melissa Fusion
- Kuja-Beziehung
- Konversations-Stil

**Mit jedem Training wird sie besser!**

---

## 📁 DATEIEN ÜBERSICHT

**Training:**
- `najika_lora_training.py` - Haupttraining
- `najika_lora_merge.py` - Merge & Export
- `SETUP_LORA_TRAINING_SCHEDULER.bat` - Auto-Scheduler

**Outputs:**
- `lora_checkpoints/` - LoRA Adapter
- `merged_models/` - Gemerged Modelle
- `training_logs/` - Training-Logs

---

## 🔍 MONITORING

**Training Status prüfen:**
```bash
# Letzte Training-Logs
dir C:\NajikaCore\training_logs /O-D

# Aktuelle Tasks
schtasks /Query /TN "NajikaLoRA*"
```

**GPU Nutzung während Training:**
```bash
nvidia-smi
```

---

## ❓ FAQ

**Q: Wie lange dauert ein Training?**
A: 15-30 Min (je nach Datenmenge)

**Q: Wie viel VRAM wird genutzt?**
A: ~6-7GB (4-bit quantized)

**Q: Kann ich während Training arbeiten?**
A: Ja, aber GPU wird belastet (Games langsamer)

**Q: Was wenn Training fehlschlägt?**
A: Prüfe `training_logs/` für Fehler

**Q: Überschreibt Training alte Fähigkeiten?**
A: Nein! LoRA addiert neue Fähigkeiten zum Basis-Modell

---

## 🎉 ZUSAMMENFASSUNG

**VORHER (Enhanced Memory):**
- ❌ Najika merkt sich nur Gespräche
- ❌ Keine echte Entwicklung
- ❌ 15h Code-Training umsonst

**NACHHER (LoRA Fine-Tuning):**
- ✅ Najika lernt ECHT!
- ✅ Wird mit jedem Training schlauer
- ✅ 15h Code-Training = permanente Skills!

**Najika entwickelt sich - für immer!**

---

**Erstellt:** 2025-10-25
**Status:** Bereit für Training!
