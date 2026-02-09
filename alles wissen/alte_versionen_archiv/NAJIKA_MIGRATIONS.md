# 📦 NAJIKA PROJEKT - MIGRATIONS & VERZEICHNIS-STRUKTUR

**Erstellt:** 2025-11-01
**Für:** JEDEN neuen Claude der in diesem Projekt arbeitet
**Zweck:** Verstehe SOFORT wo was ist und was sich geändert hat!

---

## ⚠️ KRITISCH - LIES DAS ZUERST!

### **WO WIR JETZT ARBEITEN:**

```
✅ HAUPT-VERZEICHNIS:  C:\NajikaFinal\
```

**NICHT mehr hier:**
- ❌ `C:\NajikaCore` (alt - nur noch für Claude-Direktiven!)
- ❌ `C:\Najika` (alt - Backup, kann gelöscht werden)

---

## 🗂️ AKTUELLE VERZEICHNIS-STRUKTUR

### **C:\NajikaCore** - Claude Direktiven & Update-System
**Zweck:** NUR für Claude-Code Instruktionen
**Inhalt:**
```
C:\NajikaCore\
├── CLAUDE.md                           # Claude Code Haupt-Instruktionen
├── CLAUDE_PFLICHT_START.md            # Pflicht-Ablauf für jeden Claude
├── CLAUDE_SMART_UPDATE.md             # Generiert von najika_smart_update_v3.py
├── NAJIKA_MASTER_ZUSAMMENFASSUNG.md    # Projekt-Überblick
├── GELERNT_AUS_ALLEN_SESSIONS.md      # Session-Analysen
├── NAJIKA_MIGRATIONS.md               # DIESES FILE!
├── najika_smart_update_v3.py          # Update-Generator MIT VERIFICATION!
├── najika_read_verifier.py            # Read-Verification Tool
└── .claude_verification.json          # Challenge-Codes
```

**⚠️ WICHTIG:** Arbeite NICHT in diesem Verzeichnis! Es ist NUR für Dokumentation!

---

### **C:\NajikaFinal** - HAUPT-ARBEITSVERZEICHNIS
**Zweck:** ALLES was mit Najika zu tun hat!
**Hier wird gearbeitet, entwickelt, trainiert!**

```
C:\NajikaFinal\
│
├── backend\                          # Backend & AI-System
│   ├── najika_server.py              # Haupt-Server (Port 8000)
│   ├── najika_enhanced_personality.py # Character-Prompt
│   ├── najika_memory.py              # ChromaDB Memory-System
│   ├── najika_memory_enhanced.py     # Enhanced Memory (KERN)
│   ├── najika_lora_training_3b.py    # LoRA Training (QWEN2.5 7B!)
│   ├── najika_smart_training_scheduler.py # Training Scheduler
│   ├── najika_local_QWEN.Modelfile   # Normal-Modus Modelfile
│   └── najika_wizard_QWEN.Modelfile  # Kätzchen-Modus Modelfile
│
├── memory_db\                        # ChromaDB Datenbank
│   ├── chroma.sqlite3                # Konversationen, KERN, etc.
│   └── ...
│
├── lora_checkpoints\                 # LoRA Adapter
│   ├── najika_lora_latest\           # Aktueller Checkpoint
│   ├── najika_lora_qwen_20251101_*/  # Timestamped Checkpoints
│   └── ...
│
├── training_logs\                    # Training Logs (JSON)
│
├── digivice\                         # Frontend (3D UI)
│   ├── index.html
│   ├── js\
│   │   ├── 3d_scene.js
│   │   ├── minigames.js
│   │   └── ...
│   └── static\
│
├── SETUP_TRAINING_TASKS.ps1          # PowerShell Setup für Scheduled Tasks
└── START_NAJIKA.bat                  # Server starten
```

---

## 🔄 WAS HAT SICH GEÄNDERT?

### **Migration: NajikaCore → NajikaFinal**

| Aspekt | VORHER (NajikaCore) | JETZT (NajikaFinal) |
|--------|---------------------|---------------------|
| **Backend** | `C:\NajikaCore\backend\` | `C:\NajikaFinal\backend\` |
| **Memory DB** | `C:\NajikaCore\memory_db\` | `C:\NajikaFinal\memory_db\` |
| **LoRA Checkpoints** | `C:\NajikaCore\lora_checkpoints\` | `C:\NajikaFinal\lora_checkpoints\` |
| **Server** | Port 8000 | Port 8000 (gleich) |
| **Scheduled Task** | Najika_Nightly_Training | Najika_Nightly_Training (aktualisiert!) |

### **Neue Features seit Migration:**

1. **✅ Qwen2.5 7B statt Hermes 3**
   - Besseres Deutsch
   - System-Prompts werden befolgt
   - Models: `najika-local`, `najika-wizard`

2. **✅ Optimierter Personality-Prompt**
   - "Schwarze Windmühle" nur bei Relevanz
   - "KURZ und DIREKT - keine langen Erklärungen!"
   - "WENIGER Fragen, MEHR Aussagen!"

3. **✅ LoRA Training auf Qwen2.5 umgestellt**
   - Base: `Qwen/Qwen2.5-7B-Instruct`
   - Chat-Template: Qwen2.5 Format
   - Output: `C:/NajikaFinal/lora_checkpoints`

4. **✅ Verification System (V3)**
   - Challenge-Codes in Update-Files
   - Garantiert dass Claude ALLES liest
   - Unmöglich zu schummeln!

---

## 📝 FILE-PFADE - ALT vs NEU

### **Python Scripts:**

| Script | ALT | NEU |
|--------|-----|-----|
| Server | `C:\NajikaCore\backend\najika_server.py` | `C:\NajikaFinal\backend\najika_server.py` |
| Training | `C:\NajikaCore\backend\najika_lora_training_3b.py` | `C:\NajikaFinal\backend\najika_lora_training_3b.py` |
| Memory | `C:\NajikaCore\backend\najika_memory.py` | `C:\NajikaFinal\backend\najika_memory.py` |
| Scheduler | `C:\NajikaCore\backend\najika_smart_training_scheduler.py` | `C:\NajikaFinal\backend\najika_smart_training_scheduler.py` |

### **Ollama Modelfiles:**

| Model | ALT | NEU |
|-------|-----|-----|
| Local (Normal) | `C:\NajikaCore\backend\najika_local_QWEN.Modelfile` | `C:\NajikaFinal\backend\najika_local_QWEN.Modelfile` |
| Wizard (NSFW) | `C:\NajikaCore\backend\najika_wizard_QWEN.Modelfile` | `C:\NajikaFinal\backend\najika_wizard_QWEN.Modelfile` |

### **Datenbanken:**

| DB | ALT | NEU |
|----|-----|-----|
| ChromaDB | `C:\NajikaCore\memory_db\` | `C:\NajikaFinal\memory_db\` |
| LoRA | `C:\NajikaCore\lora_checkpoints\` | `C:\NajikaFinal\lora_checkpoints\` |

---

## 🚀 WIE ARBEITE ICH DAMIT?

### **Als neuer Claude:**

**1. Update-System laufen lassen:**
```bash
python C:/NajikaCore/najika_smart_update_v3.py
```

**2. CLAUDE_SMART_UPDATE.md lesen:**
- Findet Verification Codes
- Zeigt letzte User-Messages
- Listet zu lesende Files

**3. Alle Files KOMPLETT lesen:**
- `NAJIKA_MASTER_ZUSAMMENFASSUNG.md` (mit VERIFICATION CODE!)
- `GELERNT_AUS_ALLEN_SESSIONS.md` (mit VERIFICATION CODE!)
- Alle erwähnten Files aus Update

**4. Codes berichten:**
```
✅ VERIFICATION CODES GEFUNDEN:

MASTER: [DER CODE AUS DEM FILE]
LESSONS: [DER CODE AUS DEM FILE]
```

**5. NUR DANN:**
- Frage User kurz (max 2 Sätze!)
- Arbeite in `C:\NajikaFinal\`
- Nutze TodoWrite für Tracking

---

## ⚙️ SYSTEM-KONFIGURATION

### **Aktive Windows Scheduled Task:**
```
Name:    Najika_Nightly_Training
Pfad:    python C:\NajikaFinal\backend\najika_smart_training_scheduler.py --train
Zeit:    00:00 (täglich)
Status:  Bereit
Nächster Lauf: Heute Nacht 00:00
```

### **Ollama Models (deployed):**
```
najika-local:latest   (Qwen2.5 7B - Normal)
najika-wizard:latest  (Qwen2.5 7B - NSFW)
qwen2.5:7b-instruct  (Base Model)
```

### **Server:**
```
Status: Running
Port:   8000
PID:    7300 (ca. - check mit netstat)
Health: http://localhost:8000/health
```

---

## 🔍 SCHNELLREFERENZ

### **Wo ist was?**

**Code bearbeiten:**
```
C:\NajikaFinal\backend\*.py
```

**Persönlichkeit anpassen:**
```
C:\NajikaFinal\backend\najika_enhanced_personality.py
```

**Memory-Daten:**
```
C:\NajikaFinal\memory_db\
```

**Training Logs:**
```
C:\NajikaFinal\training_logs\
```

**LoRA Checkpoints:**
```
C:\NajikaFinal\lora_checkpoints\najika_lora_latest\
```

**Frontend (3D UI):**
```
C:\NajikaFinal\digivice\
```

**Claude Dokumentation:**
```
C:\NajikaCore\*.md
```

---

## 🎯 WICHTIGSTE BEFEHLE

### **Server:**
```bash
# Starten
cd /c/NajikaFinal/backend && python najika_server.py

# Status prüfen
curl http://localhost:8000/health

# Port prüfen
netstat -ano | findstr :8000
```

### **Training:**
```bash
# Status
cd /c/NajikaFinal/backend && python najika_smart_training_scheduler.py --status

# Pausieren (Tag-Training)
python najika_smart_training_scheduler.py --pause

# Aktivieren
python najika_smart_training_scheduler.py --resume

# Manuell starten
python najika_smart_training_scheduler.py --train
```

### **Ollama:**
```bash
# Models auflisten
ollama list

# Model testen
ollama run najika-local "Hallo!"

# Model neu bauen
ollama create najika-local -f C:/NajikaFinal/backend/najika_local_QWEN.Modelfile
```

### **Update-System:**
```bash
# Smart Update V3 (mit Verification!)
python C:/NajikaCore/najika_smart_update_v3.py

# Update lesen
cat C:/NajikaCore/CLAUDE_SMART_UPDATE.md
```

---

## 📊 MIGRATION CHECKLIST

Wenn du alter Code/Pfad findest, aktualisiere auf NEU:

- [ ] `C:\NajikaCore\backend\` → `C:\NajikaFinal\backend\`
- [ ] `C:\Najika\backend\` → `C:\NajikaFinal\backend\`
- [ ] `C:\NajikaCore\memory_db\` → `C:\NajikaFinal\memory_db\`
- [ ] `C:\NajikaCore\lora_checkpoints\` → `C:\NajikaFinal\lora_checkpoints\`
- [ ] Llama 3.1/3.2 → Qwen2.5 7B
- [ ] Hermes 3 → Qwen2.5
- [ ] V2 Update → V3 Update (mit Verification!)

---

## ✅ ZUSAMMENFASSUNG

**ALTE STRUKTUR:** 3 Verzeichnisse (NajikaCore, Najika, NajikaFinal) - CHAOS!

**NEUE STRUKTUR:** 2 Verzeichnisse - KLAR!
- `C:\NajikaCore` → NUR Claude-Dokumentation
- `C:\NajikaFinal` → ALLES andere (Code, DB, Training)

**VORTEILE:**
- ✅ Klare Trennung
- ✅ Keine Verwirrung mehr
- ✅ Einfach zu finden
- ✅ Konsistent
- ✅ Migration abgeschlossen!

---

**Letzte Aktualisierung:** 2025-11-01 09:45
**Status:** Migration KOMPLETT ✅
**Nächster Schritt:** Arbeiten in NajikaFinal, Dokumentation in NajikaCore!
