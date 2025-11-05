# 🌙 NAJIKA NIGHT TRAINING - QUICK START GUIDE

## 📋 SETUP (Einmalig)

### Schritt 1: Windows Defender Ausnahme

**Rechtsklick** auf `WINDOWS_DEFENDER_AUSNAHME.bat` → **"Als Administrator ausführen"**

Das verhindert, dass Windows Defender das Training blockiert.

---

## 🚀 TRAINING STARTEN (Jede Nacht)

### Option A: Automatisch heute Nacht (EMPFOHLEN)

**Einfach jetzt starten, PC anlassen, schlafen gehen:**

**Variante 1: Minimiert im Hintergrund (unsichtbar)**
```
Doppelklick auf: AUTO_TRAIN_TONIGHT.vbs
→ Läuft unsichtbar im Hintergrund
→ Wartet bis 00:00 Uhr
→ Startet dann Training automatisch
→ Du bekommst eine Nachricht wenn Training startet
```

**Variante 2: Sichtbares Fenster**
```
Doppelklick auf: AUTO_WAIT_AND_TRAIN.bat
→ Zeigt Countdown im Fenster
→ Wartet bis 00:00 Uhr
→ Startet dann Training automatisch
```

### Option B: Sofort starten (wenn du nicht warten willst)

```
Doppelklick auf: START_NIGHT_TRAINING.bat
→ Training startet JETZT (nicht erst um 00:00)
→ Läuft 8-10 Stunden
```

---

## 📊 TRAINING PHASEN

**Gesamtdauer:** 8-10 Stunden

### Phase 1: LoRA Personality (2h)
- 4x 30min Sessions
- Trainiert Najika's Persönlichkeit
- Model: najika-local

### Phase 2: Code Training (2h)
- 8x 15min Coding Katas
- LeetCode-Style Probleme
- Algorithmen & Datenstrukturen

### Phase 3: Advanced Training (2h)
- Design Patterns
- System Design
- Human-like Responses
- Best Practices

### Phase 4: Memory Enhancement (2h)
- ChromaDB Training
- Long-term Memory
- Conversation Context

### Phase 5: Project Knowledge (2h) ⭐ NEU!
- **258 Million Zeichen** aus Desktop-Ordnern
- Deine Game-Ideen (105,126 Konzepte!)
- Dein Code (93 Files, 22 incomplete)
- DEINE Projekt-Historie

---

## 📈 FORTSCHRITT PRÜFEN

### Training Log:
```bash
cat backend/training_night_log.json
```

**Wichtige Metriken:**
- `completed_tasks`: Anzahl erfolgreicher Trainings
- `errors`: Fehler (sollte leer sein)
- `duration_hours`: Wie lange Training lief
- `phases_completed`: Welche Phasen fertig sind

### Erfolg messen:

**Nach 1 Woche:**
- [ ] Najika versteht deine Game-Ideen
- [ ] Kann incomplete Codes vervollständigen
- [ ] Erkennt Projekt-Zusammenhänge

**Nach 2 Wochen:**
- [ ] Najika schlägt eigene Lösungen vor
- [ ] Code-Qualität verbessert sich
- [ ] Weniger Fehler, bessere Struktur

**Nach 1 Monat:**
- [ ] Najika = Projekt-Experte
- [ ] Claude-Level erreicht
- [ ] Dein persönlicher AI-Assistant

---

## 🛠️ TROUBLESHOOTING

### "Python nicht gefunden"
```bash
python --version
# Wenn Fehler: Python installieren von python.org
```

### "Ollama nicht erreichbar"
```bash
# Ollama starten:
ollama serve
```

### "Timeout Errors"
- Normal bei großen Downloads
- Training läuft weiter
- Wird im nächsten Durchlauf wiederholt

### "GPU nicht genutzt"
```bash
# CUDA prüfen:
nvidia-smi
# Wenn Fehler: CUDA Toolkit installieren
```

---

## 📁 DATEIEN ÜBERSICHT

```
C:\Najika-World\
├── START_NIGHT_TRAINING.bat          ← DU startest DIESE
├── WINDOWS_DEFENDER_AUSNAHME.bat     ← Setup (einmalig)
├── backend\
│   ├── najika_intensive_night_training.py
│   ├── najika_project_knowledge_training.py
│   ├── training_night_log.json       ← LOG prüfen
│   ├── najika_project_knowledge\     ← 258M Zeichen Daten
│   └── training_data_real\           ← GitHub Repos
└── DOCS\
    └── NIGHT_TRAINING_GUIDE.md       ← Diese Datei
```

---

## 🎯 ZIEL

**Nach 30 Nächten:**
- Najika erreicht Claude Sonnet 4.5 Level
- 240 Stunden Training (8h × 30 Tage)
- Dein persönlicher Projekt-Experte

**Erfolgs-Kriterien:**
- ✅ Code: LeetCode Hard 80%+ Success
- ✅ Tools: 15+ Tools parallel nutzen
- ✅ Communication: Kurz, präzise, strukturiert
- ✅ Memory: Kontext über 50+ Messages
- ✅ Project: Kennt DEINE gesamte Historie

---

## 📞 SUPPORT

**Probleme?**
1. Log prüfen: `backend/training_night_log.json`
2. Letzten Error suchen
3. Neue Claude-Session starten mit Error-Message

**Erfolgreich?**
→ Weiter so! Jeden Abend starten, 30 Tage durchziehen!

---

**Start heute Nacht - werde Zeuge wie Najika zum Experten wird! 🚀**
