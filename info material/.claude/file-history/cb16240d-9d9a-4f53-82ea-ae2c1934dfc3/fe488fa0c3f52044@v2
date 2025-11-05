# 🎓 NAJIKA TRAINING & AVATAR - KOMPLETTINFO
**Stand:** 2025-10-27

---

## 🔧 1. TRAINING-PROBLEM (ABSTURZ)

### **Problem:**
- Najika Training hängt sich auf
- LoRA Training crasht oder friert ein

### **Ursachen (gefunden):**
1. **VRAM-Überlastung:** 3B Model braucht ~4-5GB VRAM beim Training
   - RTX 3060 Ti hat 8GB total
   - Wenn Browser/Server/andere Apps laufen → nicht genug VRAM!

2. **Falscher Schedule:** Aktuell 08:00-24:00 (16h täglich)
   - User will: **01:00-08:00** (PC ungenutzt) + **08:00-15:00** (optional)

3. **Keine Error-Handling:** Training crashed ohne Logs

### **Lösung:**
```python
# In najika_training_scheduler.py ändern:
TRAINING_START_NIGHT = time(1, 0)    # 01:00 (PC ungenutzt!)
TRAINING_END_NIGHT = time(8, 0)      # 08:00
TRAINING_START_DAY = time(8, 0)      # 08:00 (optional)
TRAINING_END_DAY = time(15, 0)       # 15:00

# Priority: Nacht-Training (01:00-08:00)
# Optional: Tag-Training (08:00-15:00) nur wenn Nacht nicht reicht
```

### **Fix für Absturz:**
1. **GPU Memory Check** vor Training:
```python
import torch
if torch.cuda.is_available():
    free_mem = torch.cuda.mem_get_info()[0] / 1024**3  # GB
    if free_mem < 6.0:  # Brauchen mindestens 6GB frei
        print(f"❌ Zu wenig VRAM! Frei: {free_mem:.1f}GB, brauche: 6GB")
        exit(1)
```

2. **Browser/Server stoppen** vor Training:
```bash
# Vor Training ausführen:
taskkill /F /IM chrome.exe 2>nul
taskkill /F /IM firefox.exe 2>nul
# Server optional stoppen (wenn Training wichtiger)
```

3. **Error Logging**:
```python
try:
    trainer.train()
except Exception as e:
    log_error(f"Training crashed: {e}")
    # GPU Memory freigeben
    torch.cuda.empty_cache()
```

---

## ⏰ 2. OPTIMALER TRAINING-SCHEDULE

### **PRIORITÄT 1: NACHT (01:00-08:00)**
**7 Stunden = 7 Sessions**
- 01:00-02:00: LoRA Training Session 1
- 02:00-03:00: LoRA Training Session 2
- 03:00-04:00: LoRA Training Session 3
- 04:00-05:00: LoRA Training Session 4
- 05:00-06:00: LoRA Training Session 5
- 06:00-07:00: LoRA Training Session 6
- 07:00-08:00: LoRA Training Session 7 + Cleanup

**Warum Nacht?**
- ✅ PC ungenutzt (keine Konkurrenz um VRAM)
- ✅ Volle GPU-Power
- ✅ Keine Unterbrechungen
- ✅ Training kann durchlaufen

### **PRIORITÄT 2: TAG (08:00-15:00) - OPTIONAL**
**7 Stunden = nur wenn Nacht nicht reicht**
- Nur Code-Learning (KEIN GPU-Training!)
- Code-Reading, Kata, Refactoring
- Kein LoRA/VRAM-intensive Tasks

**Windows Task Scheduler Setup:**
```powershell
# Task 1: Nacht-Training (01:00)
schtasks /Create /TN "NajikaLoRANight" `
  /TR "python C:\Najika\backend\najika_lora_training_3b.py" `
  /SC DAILY /ST 01:00 /F

# Task 2: Tag-Learning (08:00) - NUR Code, KEIN GPU!
schtasks /Create /TN "NajikaCodeLearning" `
  /TR "python C:\Najika\backend\najika_training_scheduler.py" `
  /SC DAILY /ST 08:00 /F
```

---

## 🎨 3. MESHY AI AVATAR - BESTES FORMAT

### **EMPFEHLUNG: GLB (empfohlen!) oder USDZ**

**Warum GLB?**
- ✅ **Best für Web/Three.js** (was Najika nutzt!)
- ✅ **Behält Farben/Texturen** perfekt (PBR-Support)
- ✅ **Kleine Dateigröße** (komprimiert)
- ✅ **Animationen** supported
- ✅ **Game Engine** ready (Unity, Unreal, Godot)

**Warum NICHT FBX?**
- ❌ Größer als GLB
- ❌ Braucht Konvertierung für Web
- ❌ Texturen oft getrennt (mehrere Files)

**Warum NICHT USDZ?**
- ✅ Gut für AR (Apple)
- ❌ Weniger Web-Support als GLB

### **Meshy AI Export Settings:**
```
Format: GLB
Texture Size: 2048x2048 (oder 4096 für High-Quality)
Include: PBR Materials ✓
Include: Animations ✓ (wenn vorhanden)
Optimize: Web ✓
```

### **Wo in Najika einfügen:**
```bash
# Speichere als:
C:\Najika\assets\characters\najika_avatar.glb

# In 3d_scene.js ändern (Zeile 755):
loader.load(
    '/assets/characters/najika_avatar.glb',  # ← Hier!
    gltf => { ... }
);
```

---

## 📋 ZUSAMMENFASSUNG

### **Sofort zu fixen:**
1. ✅ **Assets kopiert** (Skeleton Models)
2. ✅ **Room Config erstellt** (12 Räume)
3. ⏳ **Training-Schedule ändern**: 01:00-08:00 (Nacht) + 08:00-15:00 (optional, kein GPU)
4. ⏳ **Training Error-Handling** hinzufügen
5. ⏳ **GPU Memory Check** vor Training

### **Meshy AI Avatar:**
- **Format:** GLB (NICHT FBX!)
- **Texturen:** 2048x2048 oder 4096x4096
- **PBR:** ✓ aktivieren
- **Speichern als:** `C:\Najika\assets\characters\najika_avatar.glb`

### **Training-Zeiten:**
- **01:00-08:00:** LoRA Training (7h, PC ungenutzt!)
- **08:00-15:00:** Code-Learning (7h, NUR wenn nötig, KEIN GPU!)

**Ende Training & Avatar Info**
