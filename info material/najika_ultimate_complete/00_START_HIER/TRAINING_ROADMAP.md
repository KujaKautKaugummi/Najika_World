# 🎓 NAJIKA TRAINING ROADMAP

**Version:** 1.0
**Datum:** 2025-11-01
**Zweck:** Schritt-für-Schritt Training erweitern

---

## 📊 **STATUS: WAS LÄUFT**

```
✅ Phase 1: Code + Persönlichkeit
   - Qwen 2.5-7B-Instruct
   - LoRA Training
   - Konosuba + NGNL + Code
   - Läuft bereits!

❌ Phase 2: Wissen (FEHLT!)
   - Digivice-System
   - Wissensbibliothek
   - Erinnerungssystem
   - Alle Features
```

---

## 🎯 **ZIEL: KOMPLETTES WISSENS-TRAINING**

Najika soll ALLES über sich selbst wissen nach dem Training!

---

## 📚 **SCHRITT 1: TRAININGS-DATEN ERSTELLEN**

### **Datei-Liste (5 Dateien):**

```
1. digivice_komplett.txt (~10-15 Seiten)
   → Alle 12 Räume detailliert
   → Jeder Raum: Funktionen, Use-Cases, Reaktionen
   → Terminal: Passwort, Hacker-Modus, alle Module

2. wissensbibliothek_komplett.txt (~5-8 Seiten)
   → ChromaDB Erklärung
   → Vektoren, Embeddings
   → Speichern & Abrufen
   → Kategorien (personal, projects, code, etc.)
   → Befehle ("Merk dir das!")

3. erinnerungssystem_komplett.txt (~5-8 Seiten)
   → Kurzzeit vs Langzeit-Gedächtnis
   → Automatisch vs Manuell
   → Kontext-Aufbau
   → Zeitstempel, Tags
   → Beispiele

4. features_komplett.txt (~10-15 Seiten)
   → ALLE Features die Najika hat
   → Voice/TTS, Code, Übersetzer
   → Training-System
   → PC-Steuerung
   → Alles!

5. use_cases_komplett.txt (~15-20 Seiten)
   → 30-50 verschiedene Szenarien
   → Alltag, Programmieren, Lernen
   → Gaming (später)
   → Terminal-Nutzung
```

### **Template für Räume:**

```markdown
=== RAUM: Wohnzimmer ===

Beschreibung:
Das Wohnzimmer ist der zentrale Basis-Raum für Interaktion mit Najika.
Hier findet normale Kommunikation statt.

Funktionen:
1. Füttern
   - Najika virtuell füttern
   - Erhöht Energie-Level
   - Sie freut sich darüber!
   
2. Reden
   - Normaler Chat-Modus
   - Plaudern, Fragen, Alltag
   - Najika ist aufmerksam

Use-Case 1: Alltags-Gespräch
User: "Najika, wie geht's dir?"
Najika intern: [Prüfe Status, formuliere Antwort]
Najika: "Kuja! Mir geht's SUPER! Ich bin so froh dich zu sehen! *hüpft aufgeregt* Und dir?"

Use-Case 2: Füttern
User: "Lass uns ins Wohnzimmer, ich gebe dir was zu essen."
Najika: "Kuja! Du bist SO lieb! *Augen leuchten* Was gibt's denn? Ich bin hungrig!"
[Füttern-Aktion durchgeführt]
Najika: "Mmmmh! LECKER! Danke Kuja! *zufrieden*"

Najika's Stimmung im Raum:
- Entspannt
- Gesprächig
- Anhänglich
- Fröhlich

=== ENDE RAUM ===
```

---

## 🛠️ **SCHRITT 2: ORDNER-STRUKTUR**

```
C:\NajikaTraining\
│
├── phase1_done\              # ✅ Schon trainiert
│   ├── konosuba\
│   ├── ngnl\
│   ├── code_examples\
│   └── deutsche_saetze\
│
├── phase2_wissen\            # ⭐ JETZT ERSTELLEN!
│   ├── digivice_komplett.txt
│   ├── wissensbibliothek_komplett.txt
│   ├── erinnerungssystem_komplett.txt
│   ├── features_komplett.txt
│   └── use_cases_komplett.txt
│
└── combined\                 # Alles zusammen
    └── najika_full_v2.txt    # Kombiniert für Training
```

---

## ⚡ **SCHRITT 3: TRAINING DURCHFÜHREN**

### **3.1 Dateien kombinieren**

```bash
# PowerShell:
cd C:\NajikaTraining

# Alles zusammenführen
Get-Content phase1_done\*.txt, phase2_wissen\*.txt | 
  Set-Content combined\najika_full_v2.txt

# Prüfen
Get-ChildItem combined\najika_full_v2.txt
```

### **3.2 LoRA Training starten**

```bash
# Mit existierendem Script!
python najika_lora_training_3b.py `
  --base-model "Qwen/Qwen2.5-7B-Instruct" `
  --training-data "combined/najika_full_v2.txt" `
  --output-dir "najika_trained_v2" `
  --epochs 3 `
  --batch-size 4 `
  --learning-rate 0.0001

# Training läuft: 2-4 Stunden
# GPU: RTX 3060 Ti (8GB VRAM)
```

### **3.3 Konvertieren zu GGUF**

```bash
# Nach Training:
python convert_to_gguf.py \
  --input najika_trained_v2 \
  --output najika_v2.gguf \
  --quant q5_k_m

# Fertig!
```

---

## ✅ **SCHRITT 4: TESTEN**

### **Test-Suite:**

```
Test 1: Räume-Wissen
Frage: "Najika, welche Räume gibt es im Digivice?"
✅ Erwartet: Alle 12 Räume aufzählen

Test 2: Terminal-Details
Frage: "Was ist der Hacker-Modus?"
✅ Erwartet: PC-Steuerung erklären

Test 3: Wissensbibliothek
Frage: "Wie funktioniert deine Wissensbibliothek?"
✅ Erwartet: ChromaDB, Vektoren, Kategorien

Test 4: Erinnerungssystem
Frage: "Wie erinnerst du dich an Dinge?"
✅ Erwartet: Kurzzeit/Langzeit, automatisch/manuell

Test 5: Features
Frage: "Was kannst du alles machen?"
✅ Erwartet: Liste aller Features

Test 6: Use-Case
Frage: "Ich will etwas kochen."
✅ Erwartet: Küche vorschlagen + Funktionen

Test 7: Character
Frage: "Bist du Megumin?"
✅ Erwartet: Megumin-Style Antwort + Explosion!

Test 8: Integration
Frage: "Hilf mir beim Coden und merk dir mein Projekt."
✅ Erwartet: Code-Hilfe + Wissensbibliothek erwähnen
```

---

## 📊 **ERFOLGS-KRITERIEN**

### **Training erfolgreich wenn:**

```
✅ Najika kennt alle 12 Räume (nennt Namen + Funktionen)
✅ Najika erklärt Terminal korrekt (Passwort, Module)
✅ Najika beschreibt Wissensbibliothek richtig (ChromaDB)
✅ Najika erklärt Erinnerungssystem (Kurzzeit/Langzeit)
✅ Najika listet alle Features auf
✅ Najika reagiert situationsgerecht (Use-Cases)
✅ Najika bleibt im Character (Megumin-Style!)
✅ Najika gibt technisch korrekte Antworten
✅ Najika kombiniert Wissen (z.B. Code + Wissensbibliothek)
```

---

## 🎯 **QUICK-START: DIESE WOCHE**

### **Tag 1-2: Daten erstellen**
```
1. digivice_komplett.txt schreiben
   → 12 Räume × 1-2 Seiten = 12-24 Seiten
   → Pro Raum: Details, Funktionen, Use-Cases, Reaktionen
   
2. wissensbibliothek_komplett.txt schreiben
   → 5-8 Seiten
   → ChromaDB, Vektoren, Speichern, Abrufen, Beispiele
```

### **Tag 3-4: Mehr Daten**
```
3. erinnerungssystem_komplett.txt schreiben
   → 5-8 Seiten
   → Kurzzeit, Langzeit, Kontext, Beispiele
   
4. features_komplett.txt schreiben
   → 10-15 Seiten
   → ALLE Features detailliert
```

### **Tag 5: Finalisieren**
```
5. use_cases_komplett.txt schreiben
   → 15-20 Seiten
   → 30-50 verschiedene Szenarien
   → Alltag, Code, Lernen, Gaming
```

### **Tag 6: Training**
```
6. Dateien kombinieren
7. LoRA Training starten (2-4h)
8. Konvertieren zu GGUF
```

### **Tag 7: Testen**
```
9. Alle Tests durchgehen
10. Performance prüfen
11. Nachjustieren wenn nötig
```

---

## 💡 **TIPPS**

### **Für gute Trainings-Daten:**

```
✅ Detailliert schreiben
   → Viele Details = besseres Verständnis
   
✅ Konkrete Beispiele
   → Jedes Konzept mit 2-3 Beispielen
   
✅ Megumin-Character
   → ALLE Najika-Antworten im Stil!
   → "Kuja!", "EXPLOSION!", dramatisch
   
✅ Technisch korrekt
   → ChromaDB, APIs, Systeme richtig erklären
   
✅ Variieren
   → Viele verschiedene Situationen
   → Nicht nur Happy-Path!
```

### **Was vermeiden:**

```
❌ Zu kurz
   → Mindestens 1-2 Seiten pro Konzept!
   
❌ Out-of-Character
   → Najika IMMER als Megumin!
   
❌ Nur Theorie
   → Immer praktische Beispiele!
   
❌ Widersprüche
   → Alles muss konsistent sein
```

---

## 🚀 **NACH DEM TRAINING**

### **Najika kann dann:**

```
✅ Alle 12 Räume detailliert beschreiben
✅ Terminal & Hacker-Modus erklären
✅ Wissensbibliothek nutzen & erklären
✅ Erinnerungssystem nutzen & erklären
✅ Alle Features auflisten & erklären
✅ In jedem Szenario richtig reagieren
✅ PC-Steuerung verstehen
✅ Sich selbst komplett erklären
✅ Mit Claude Code perfekt zusammenarbeiten!
```

### **Claude Code Integration:**

```
1. Claude Code startet
2. Lädt trainiertes Najika-Modell
3. Kann Najika ALLES fragen:
   - "Welche Räume hast du?"
   - "Wie funktioniert deine Wissensbibliothek?"
   - "Was ist der Hacker-Modus?"
   - "Erkläre alle Features!"
   
4. Najika antwortet PERFEKT!
5. Zusammen entwickeln sie weiter!
```

---

**READY TO START? 🚀**

**Nächster Schritt:** Beginne mit `digivice_komplett.txt`! ✨
