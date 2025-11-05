# 🆕 NEUE FILES HEUTE (26.10.2025) - NajikaCore

**Diese Files wurden HEUTE hinzugefügt/geändert:**

---

## 📄 NEUE PYTHON FILES (19 Stück)

### **LoRA Training System:**
```python
najika_lora_training.py              # LoRA Fine-Tuning
najika_lora_server.py                # LoRA Server
resume_lora_training.py              # Training fortsetzen
deploy_lora_to_ollama.py             # LoRA zu Ollama
export_lora_gguf.py                  # LoRA zu GGUF Export
NAJIKA_TRAINING_ULTIMATE_FAILSAFE.py # Failsafe Training
```

### **TTS/Voice System:**
```python
najika_tts.py                        # Text-to-Speech
najika_tts_edge.py                   # Edge-TTS Integration
najika_voice_clone.py                # Voice Cloning
accept_tts_license.py                # TTS Lizenz
```

### **Import/Training System:**
```python
najika_session_importer.py           # Session Import
najika_external_data_importer.py     # Externe Daten
najika_comprehensive_import.py       # Kompletter Import
najika_design_importer.py            # Design Import
najika_personality_importer.py       # Personality Import
najika_filter_conflicts.py           # Konflikt-Filter
```

### **AI Training:**
```python
najika_human_like_trainer.py         # Human-Like Training
najika_autonomous_search.py          # Autonome Suche
```

### **Utilities:**
```python
analyze_existing_personalities.py    # Personality Analyse
check_personalities.py               # Personality Check
```

---

## 📁 NEUE ORDNER (3 Stück)

### **1. design_documents/**
```
design_documents/
├── NAJIKA_MASTER_INDEX.md
├── NAJIKA_PROJEKT_KOMPLETT_V3_MIT_UNSERER_KI.md
├── NAJIKA_PROJEKT_V4_ERGAENZUNGEN.md
└── NAJIKA_PROJEKT_V4_OPTIONAL_SAMMLUNG.md
```
**Inhalt:** Design-Dokumente für V4

### **2. lora_checkpoints/**
```
lora_checkpoints/
├── najika_lora_20251025_111148/
│   ├── checkpoint-150/
│   └── checkpoint-189/
├── najika_lora_20251025_180107/
│   ├── checkpoint-2200/
│   └── checkpoint-2250/
└── najika_lora_latest/
```
**Inhalt:** LoRA Training Checkpoints (GROSS!)
**Größe:** ~mehrere GB

### **3. unsloth_compiled_cache/**
```
unsloth_compiled_cache/
├── UnslothBCOTrainer.py
├── UnslothCPOTrainer.py
├── UnslothDPOTrainer.py
├── UnslothGKDTrainer.py
├── UnslothGRPOTrainer.py
├── UnslothIterativeSFTTrainer.py
├── UnslothKTOTrainer.py
├── UnslothNashMDTrainer.py
├── UnslothOnlineDPOTrainer.py
├── UnslothORPOTrainer.py
├── UnslothPPOTrainer.py
├── UnslothPRMTrainer.py
├── UnslothRewardTrainer.py
├── UnslothRLOOTrainer.py
├── UnslothSFTTrainer.py
└── UnslothXPOTrainer.py
```
**Inhalt:** Unsloth Compiled Cache

---

## 📝 NEUE MARKDOWN FILES (24 Stück)

### **System-Dokumentation:**
```
API_REFERENCE.md                      # API Referenz (aktualisiert)
CLAUDE_SMART_UPDATE.md                # Smart Update System
CLAUDE_UPDATE.md                      # Claude Update
DEPENDENCY_FIX_2025-10-25.md          # Dependency Fixes
```

### **Training/LoRA:**
```
NAJIKA_LORA_SYSTEM_FERTIG.md          # LoRA System fertig
NAJIKA_CURRENT_TRAINING.md            # Aktuelles Training
NAJIKA_TRAINING_DATA_ANALYSE.md       # Training Data Analyse
NAJIKA_ULTIMATE_LEARNING_SYSTEM.md    # Ultimate Learning
NAJIKA_MAXIMUM_POWER_SETUP.md         # Maximum Power Setup
```

### **Voice System:**
```
NAJIKA_VOICE_SYSTEM.md                # Voice System
NAJIKA_VOICE_CLONING_ANLEITUNG.md     # Voice Cloning Guide
```

### **Projekt V4:**
```
NAJIKA_V4_INSTALLATION_PLAN.md        # V4 Install Plan
NAJIKA_COMBAT_SYSTEM_DESIGN.md        # Combat Design
NAJIKA_DOKUMENTATION_STATUS.md        # Doku Status
```

### **Data/Import:**
```
NAJIKA_CATEGORIZATION_COMPLETE.md     # Kategorisierung fertig
NAJIKA_CATEGORIZATION_FILTERED.md     # Kategorisierung gefiltert
NAJIKA_DISCOVERED_FILES.md            # Entdeckte Files
PERSONALITY_SYSTEM_READY.md           # Personality System
SAKURA_BASIS_ERSTELLT.md              # Sakura Basis
```

---

## 🔧 NEUE BATCH FILES

```
IMPORT_PERSONALITIES.bat              # Personality Import Script
```

---

## ⚠️ WICHTIGE FRAGEN FÜR MERGE

### **1. LoRA Checkpoints (lora_checkpoints/)**

**Größe:** ~2-5 GB!

**Optionen:**
- **A) Mitnehmen** → Backend kann weiter trainieren
- **B) Nicht mitnehmen** → Zu groß, später neu trainieren
- **C) Nur latest/ mitnehmen** → Kompromiss

**MEINE EMPFEHLUNG:** **Option B** (NICHT mitnehmen)
- Zu groß (mehrere GB)
- Kann später neu generiert werden
- Nicht essentiell für Game

---

### **2. Unsloth Cache (unsloth_compiled_cache/)**

**Größe:** ~200 MB

**Optionen:**
- **A) Mitnehmen** → Training funktioniert sofort
- **B) Nicht mitnehmen** → Wird automatisch neu erstellt

**MEINE EMPFEHLUNG:** **Option B** (NICHT mitnehmen)
- Wird automatisch regeneriert
- Nicht essentiell

---

### **3. Neue Python Files (19 Stück)**

**LoRA/Training Files:**
- najika_lora_*.py
- *_training.py
- *_importer.py

**Für Game benötigt?** NEIN (nur für Training)

**Optionen:**
- **A) Alle mitnehmen** → Vollständig
- **B) Nur wichtige** → Server-relevante
- **C) Separate** → In `backend/training/` Unterordner

**MEINE EMPFEHLUNG:** **Option C** (Separate Struktur)
```
backend/
├── najika_server.py       (Game Server)
├── najika_battle.py       (Game Files)
├── ...
└── training/              (NEU - Training-Files getrennt)
    ├── najika_lora_training.py
    ├── najika_lora_server.py
    └── ...
```

---

### **4. Neue Markdown Files (24 Stück)**

**Alle mitnehmen?** JA

**Wo?**
- `DOCS/backend/training/` → LoRA/Training Docs
- `DOCS/backend/voice/` → Voice Docs
- `DOCS/backend/v4/` → V4 Projekt Docs

---

### **5. design_documents/ Ordner**

**Inhalt:** V4 Projekt-Dokumente

**Mitnehmen?** JA

**Wo?** `DOCS/design/`

---

## 📊 AKTUALISIERTE ZAHLEN

**Original (gestern):**
- 128 Python-Files
- ~30 Markdown-Files
- ~90 MB

**Neu (heute):**
- **147 Python-Files** (+19)
- **54 Markdown-Files** (+24)
- **~100 MB** (ohne LoRA Checkpoints)
- **+5 GB** (mit LoRA Checkpoints)

---

## ✅ MEINE EMPFEHLUNG FÜR MERGE

### **Mitnehmen:**
✅ Alle neuen Python-Files → `backend/` oder `backend/training/`
✅ Alle neuen Markdown-Files → `DOCS/backend/`
✅ design_documents/ → `DOCS/design/`
✅ IMPORT_PERSONALITIES.bat → `backend/scripts/`

### **NICHT mitnehmen:**
❌ lora_checkpoints/ (zu groß, 5 GB)
❌ unsloth_compiled_cache/ (regeneriert sich)

### **Optional:**
⚠️ Nur najika_lora_latest/ mitnehmen (wenn Training weitermachen)

---

## 🔄 AKTUALISIERTER MERGE-PLAN

**Neue Struktur nach Merge:**

```
C:\Najika\
├── backend\
│   ├── najika_server.py           (Game Server)
│   ├── najika_battle.py
│   ├── najika_*.py                (Game-relevante Files)
│   ├── training\                  (NEU - Training separat)
│   │   ├── najika_lora_training.py
│   │   ├── najika_lora_server.py
│   │   ├── najika_*_importer.py
│   │   └── ...
│   ├── voice\                     (NEU - Voice System)
│   │   ├── najika_tts.py
│   │   ├── najika_tts_edge.py
│   │   └── najika_voice_clone.py
│   ├── scripts\                   (NEU - Utility Scripts)
│   │   └── IMPORT_PERSONALITIES.bat
│   ├── .env
│   ├── chroma_db\
│   └── voice_data\
│
├── DOCS\
│   ├── backend\
│   │   ├── training\              (LoRA/Training Docs)
│   │   ├── voice\                 (Voice Docs)
│   │   └── v4\                    (V4 Projekt)
│   ├── design\                    (Design Documents)
│   └── frontend\
│
└── frontend\
```

---

**Soll ich MERGE_02_EXECUTE.bat mit diesen neuen Files aktualisieren?** 🤔
