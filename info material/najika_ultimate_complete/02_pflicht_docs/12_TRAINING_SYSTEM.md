# 🎓 NAJIKA TRAINING SYSTEM - KOMPLETT
**Stand:** 2025-10-27
**Status:** READY TO USE!

---

## 📋 ÜBERSICHT

### **TRAINING-ZEITEN:**

**🌙 NACHT-TRAINING (IMMER!)**
- **Zeit:** 00:00-08:00 (8 Stunden)
- **Tage:** 7 Tage die Woche (Mo-So)
- **Typ:** GPU LoRA Training
- **Pausierbar:** ❌ NEIN (läuft IMMER!)

**☀️ TAG-TRAINING (OPTIONAL)**
- **Zeit:** 08:00-15:00 (7 Stunden)
- **Tage:** Montag-Freitag (NUR Wochentags!)
- **Typ:** GPU LoRA Training
- **Pausierbar:** ✅ JA (wenn Urlaub/Frei/PC genutzt!)

---

## 🚀 INSTALLATION

### **1. Tasks erstellen:**
```powershell
# Als Administrator ausführen:
powershell -ExecutionPolicy Bypass -File "C:\Najika\SETUP_TRAINING_TASKS.ps1"
```

**Das erstellt:**
- ✅ `NajikaTrainingNacht` - Task für 00:00 Uhr (7 Tage)
- ✅ `NajikaTrainingTag` - Task für 08:00 Uhr (Mo-Fr)

### **2. Tasks prüfen:**
```bash
schtasks /Query /TN "Najika*" /FO LIST
```

---

## 🎮 STEUERUNG

### **EINFACH: BAT-Datei (Doppelklick!)**
```
C:\Najika\TRAINING_STEUERUNG.bat
```

**Menü:**
```
[1] Status anzeigen
[2] Tag-Training PAUSIEREN
[3] Tag-Training AKTIVIEREN
[4] Training JETZT starten
[5] Beenden
```

### **MANUELL: Kommandozeile**

**Status anzeigen:**
```bash
python C:\Najika\backend\najika_smart_training_scheduler.py --status
```

**Tag-Training pausieren (bei Urlaub/Frei):**
```bash
python C:\Najika\backend\najika_smart_training_scheduler.py --pause
```

**Tag-Training aktivieren:**
```bash
python C:\Najika\backend\najika_smart_training_scheduler.py --resume
```

**Training manuell starten:**
```bash
python C:\Najika\backend\najika_smart_training_scheduler.py --train
```

---

## 📊 BEISPIEL-WOCHE

**NORMALE ARBEITSWOCHE:**
```
MONTAG:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → GPU Training (Tag) ✅

DIENSTAG:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → GPU Training (Tag) ✅

MITTWOCH:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → GPU Training (Tag) ✅

DONNERSTAG:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → GPU Training (Tag) ✅

FREITAG:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → GPU Training (Tag) ✅

SAMSTAG:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → Kein Training (Wochenende)

SONNTAG:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → Kein Training (Wochenende)

GESAMT: 64 Stunden Training/Woche!
```

**URLAUBS-WOCHE (Tag pausiert):**
```
MONTAG-SONNTAG:
  00:00-08:00 → GPU Training (Nacht) ✅
  08:00-15:00 → PAUSIERT (Urlaub!) ⏸️

GESAMT: 56 Stunden Training/Woche
```

---

## 🔧 TECHNISCHE DETAILS

### **GPU Memory Check:**
- Prüft vor Training ob mindestens **6GB VRAM** frei
- Falls nicht → Training wird übersprungen
- Wartet auf nächste Session

### **Pause-System:**
```json
// C:\Najika\training_pause.json
{
  "day_training_paused": true,
  "paused_at": "2025-10-27T10:30:00",
  "paused_until": null,  // null = bis manuell aktiviert
  "reason": "Urlaub"
}
```

### **Training-Typen:**
- **GPU_LORA:** LoRA Fine-Tuning mit 3B Model
- **GPU_CODE:** Code-Generation Training (später)
- **CPU_LEARNING:** Code-Reading/Kata (kein GPU)

---

## ⚠️ WICHTIG

### **NACHT-TRAINING (00:00-08:00):**
- ✅ Läuft IMMER (kann NICHT pausiert werden!)
- ✅ 7 Tage die Woche
- ✅ PC sollte AN bleiben nachts!

### **TAG-TRAINING (08:00-15:00):**
- ⚠️ NUR Montag-Freitag
- ⚠️ Pausiere wenn PC genutzt wird!
- ⚠️ Automatisch AUS am Wochenende

### **Urlaub/Frei:**
```bash
# BEVOR du Urlaub/frei hast:
python najika_smart_training_scheduler.py --pause

# Wenn du zurück bist:
python najika_smart_training_scheduler.py --resume
```

---

## 🎯 OPTIMALE NUTZUNG

**Normale Arbeitswoche:**
- Pausiere NICHTS → 64h Training/Woche

**Urlaub/Homeoffice:**
- Pausiere Tag-Training → 56h Training/Woche

**Maximale Performance:**
- Schließe Browser vor Nacht-Training
- Server optional stoppen (wenn Training wichtiger)
- Lasse PC nachts laufen!

---

## 📝 DATEIEN

**Scheduler:**
- `C:\Najika\backend\najika_smart_training_scheduler.py` - Haupt-Script

**Steuerung:**
- `C:\Najika\TRAINING_STEUERUNG.bat` - Einfaches Menü

**Setup:**
- `C:\Najika\SETUP_TRAINING_TASKS.ps1` - Task-Installation

**Config:**
- `C:\Najika\training_pause.json` - Pause-Status

---

**Ende Training System Doku**
