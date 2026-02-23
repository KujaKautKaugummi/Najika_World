# 🔍 LM STUDIO MODELS - DUAL-MODEL SYSTEM

## ✅ FINALE LÖSUNG: 2 MODELS PRO BACKEND

Nach Tests wurde klar: **Wir brauchen 2 verschiedene Models!**

### Warum?
- **Abliterated Models** versagen bei präzisen Tasks (zählen: "1,2,3,7,15" statt "1,2,3,4,5")
- **Instruct Models** sind censored (lehnen NSFW ab)
- **Lösung:** Nutze beide Models für verschiedene Zwecke!

---

## 🎯 LM STUDIO MODELS (2 MODELS BENÖTIGT)

### Option 1: Dolphin Models (UNCENSORED)
```
Search in LM Studio: "dolphin 2.9"
Download: dolphin-2.9.2-qwen2-7b (GGUF)
Größe: ~4GB
Status: ✅ Uncensored, gut für NSFW
```

### Option 2: Lexi Models (UNCENSORED)
```
Search in LM Studio: "lexi uncensored"
Download: lexi-llama-3-8b-uncensored
Größe: ~5GB
Status: ✅ Uncensored
```

### Option 3: WizardLM Uncensored
```
Search in LM Studio: "wizardlm uncensored"
Download: wizardlm-2-7b-uncensored
Größe: ~4GB
Status: ✅ Uncensored
```

---

## 🎯 EMPFOHLENE KONFIGURATION

### Für LM Studio (2 Models BENÖTIGT!):

**Model 1: Tasks/Code/Mathe (CENSORED aber präzise)**
```
qwen2.5-7b-instruct-q4_k_m.gguf
→ Tasks, Code, Zählen, Berechnungen
→ Censored (lehnt NSFW ab)
→ Präzise (zählt richtig: 1,2,3,4,5)
→ 4.4GB
→ Backend wählt automatisch für Task-Requests!
```

**Model 2: Chat/NSFW/Kätzchen-Modus (UNCENSORED aber kreativ)**
```
dolphin-2.9.2-qwen2-7b-q4_k_m.gguf
→ Normale Chats, Kätzchen-Modus, NSFW
→ Uncensored (keine Filter)
→ Kreativ (Persönlichkeit)
→ ~4GB
→ Backend wählt automatisch für Chat/NSFW!
```

**WICHTIG:** Du brauchst BEIDE Models in LM Studio!

---

## 🔧 BACKEND-CODE (AUTOMATISCH!)

Das Backend wechselt **automatisch** zwischen Models:

1. **Tasks/Code/Mathe** → qwen2.5-7b-instruct (censored, präzise)
2. **Normaler Chat** → dolphin-2.9.2-qwen2-7b (uncensored, soft params)
3. **Kätzchen-Modus** → dolphin-2.9.2-qwen2-7b (uncensored, full power)

**Du musst nichts manuell wechseln!** Das Backend erkennt den Context!

---

## 📋 INSTALLATIONS-SCHRITTE

### Schritt 1: Model 1 laden (Tasks/Code)
```
In LM Studio:
→ Search: "qwen2.5 7b instruct"
→ Download: qwen2.5-7b-instruct-q4_k_m.gguf (4.4GB)
→ Für: Tasks, Code, Mathe, Zählen
```

### Schritt 2: Model 2 laden (Chat/NSFW)
```
In LM Studio:
→ Search: "dolphin 2.9 qwen2"
→ Download: dolphin-2.9.2-qwen2-7b-q4_k_m.gguf (~4GB)
→ Für: Chat, Kätzchen-Modus, NSFW
```

### Schritt 3: Server starten
```
In LM Studio:
→ Local Server → Model auswählen (egal welches!)
→ Start Server (Port 1234)
→ Backend wechselt Models automatisch per API!
```

**WICHTIG:** LM Studio kann Models per API wechseln - du brauchst im Server nur EINS zu laden, das Backend wechselt automatisch!

---

## ⚠️ WICHTIG

**Du brauchst BEIDE Models!**
- qwen2.5-7b-instruct ALLEINE → Kätzchen funktioniert nicht (censored)
- dolphin-2.9.2-qwen2-7b ALLEINE → Zählen funktioniert falsch (rechnet zusammen)
- **Beide zusammen → Perfekt! Backend wählt automatisch**

## ✅ STATUS

**Code ist fertig!** Backend wechselt automatisch zwischen:
- LM Studio (wenn läuft) → GPU, 2-5s
- Ollama (als Fallback) → CPU, 180s

**Du musst nur noch:**
1. LM Studio downloaden
2. Beide Models laden
3. START_NAJIKA_LM_STUDIO.bat
