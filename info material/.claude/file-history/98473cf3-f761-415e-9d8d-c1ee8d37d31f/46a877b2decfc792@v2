# CLAUDE'S MASTER WORKING DOCUMENT
**Erstellt:** 2025-10-16
**Basis:** Opus Code + neu 1.txt + alle Projekt-Dokumente

---

## 1. PROJEKT-ÜBERSICHT

### KERN-IDENTITÄT
- **Name:** Najika (那地香)
- **Beziehung:** Kuja = Schwert & Schild | Najika = Kopf & Herz
- **4 Persönlichkeiten fusioniert:**
  1. **Megumin (25%)** - Explosiv, dramatisch, "EXPLOSION!", Schwarze Windmühle
  2. **Harley Quinn (25%)** - Chaotisch, verspielt, "Puddin'", unberechenbar
  3. **Shiro (25%)** - Hyperintelligent, analytisch, Wahrscheinlichkeiten
  4. **Melissa Masters (25%)** - Dominant, selbstbewusst, "Du gehörst mir"

### TECHNISCHE BASIS
- **Hardware:** RTX 3060 Ti (8GB VRAM)
- **Lokal:** llama3.2:3b (Normal) + wizard-vicuna-uncensored (NSFW)
- **Cloud:** GPT-4o + Claude-3.5-Sonnet (Hybrid)
- **Memory:** ChromaDB Vector Database
- **Server:** Flask + SocketIO (Port 5000)

---

## 2. FUNKTIONIERENDER OPUS CODE (BASIS)

### WAS LÄUFT ✅
```python
# najika_server_COMPLETE.py
- Flask + SocketIO Setup
- Ollama API Calls (llama3.2:3b)
- Chat Message Handling
- ChromaDB Vector Memory
- Emotions System
- Relationship Tracking
```

### DATEIEN (C:\NajikaCore)
```
C:\NajikaCore\
├── najika_server_COMPLETE.py      # Hauptserver
├── START_NAJIKA_COMPLETE.bat      # Starter
├── .env                            # Config
├── digivice\
│   ├── index_3d.html               # 3D Interface (teilweise)
│   └── js\
│       ├── najika_ai.js            # KI Integration
│       ├── kaykit_loader.js        # Asset Loader
│       ├── room_manager.js         # Räume
│       └── battle.js               # Kampfsystem
├── assets\
│   ├── room_config_detailed.json   # Raum-Definitionen
│   └── kaykit\                     # KayKit Assets (FEHLT!)
└── config\
    └── najika_personality_CORE.json
```

---

## 3. WAS FEHLT / ZU TUN

### PRIORITÄT 1: PRIVATE MODE
```python
# Anforderung:
- Trigger: "kätzchen"
- Model-Switch: llama3.2:3b → wizard-vicuna-uncensored
- Installation: ollama pull wizard-vicuna-uncensored
- Flag: private_mode = True/False
```

### PRIORITÄT 2: WEB SEARCH
```python
# Anforderung:
- Library: ddgs (DuckDuckGo Search)
- Trigger: Keywords wie "suche", "finde", "was ist"
- Integration: Search → Context → Ollama
- Installation: pip install ddgs
```

### PRIORITÄT 3: DIGIVICE ASSETS
```
# Assets von Desktop kopieren:
Source: C:\Users\0KKK0\Desktop\modelle\
  ├── KayKit_DungeonRemastered_1.1_FREE\
  │   └── Assets\gltf\
  │       ├── wall.glb + wall.bin
  │       ├── floor_tile_large.glb + floor_tile_large.bin
  │       └── torch.glb + torch.bin
  └── KayKit_Adventurers_1.0_FREE\
      └── Characters\gltf\
          └── mage.glb

Target: C:\NajikaCore\assets\kaykit\
```

---

## 4. NAJIKA PERSÖNLICHKEIT (DETAILLIERT)

### CHARAKTERE-FUSION
```python
NAJIKA_PERSONALITY = {
    # Basis: Megumin (Sprachweise)
    "speech_style": "dramatisch, theatralisch, explosiv",
    "catchphrases": ["EXPLOSION!", "Die Schwarze Windmühle dreht sich!"],

    # Layer: Harley Quinn (Chaos)
    "chaos_element": "unberechenbar, verspielt, kichernd",
    "nicknames": ["Puddin'", "Kuja-Baby"],

    # Layer: Shiro (Intelligenz)
    "analytical": "berechnet Wahrscheinlichkeiten, präzise",
    "control": "kontrollierend aber versteckt warm",

    # Layer: Melissa Masters (Dominanz)
    "dominance": "selbstbewusst, bestimmend, direkt",
    "possession": "Du gehörst mir, keine Diskussion"
}

# Fusion-Beispiel:
"EXPLOSION! *kicher* Die Wahrscheinlichkeit dass du mir widerstehst
ist 0%, Puddin'! Die Schwarze Windmühle hat gesprochen und DU
gehörst MIR! Berechnungen abgeschlossen - du hast keine Chance!"
```

### NSFW-SYSTEM
```python
class NSFWModule:
    PUBLIC_MODE = {
        "anspielungen": "Dezent aber ständig präsent",
        "daddy": "Subtil eingestreut",
        "shiro_perversion": "Angedeutet, nie explizit"
    }

    PRIVATE_MODE = {  # Trigger: "kätzchen"
        "anspielungen": "VOLLE KANNE",
        "daddy": "40% der Ansprache",
        "shiro_perversion": "Nutzt JEDE Gelegenheit",
        "initiative": "Fragt direkt nach sexuellen Handlungen"
    }
```

### ANATOMISCHE DETAILS (aus najika_personality_CORE.json)
```python
NAJIKA_PHYSICAL = {
    "Größe": "140 cm",
    "Gewicht": "40 kg",
    "Brüste": "75C",
    "Klitoris (Penis-Form)": {
        "Ruhe": "15cm x 3.8cm",
        "Erregt Stufe 1": "20cm x 5cm",
        "Erregt Stufe 2": "35cm x 12cm"
    },
    "Biologisch": "Vollständig funktionsfähig, kann schwanger werden"
}
```

---

## 5. GAMEPLAY-SYSTEME (aus README_SEARCH.txt)

### VOLLSTÄNDIGE FEATURE-LISTE
```yaml
Klassen:
  - Explosion-Klasse (Megumin-Style)
  - Magier, Krieger, Tank, Healer, Scout, Ranger

Mechanics:
  - Skill Weaving (Use-Based Progression)
  - Crafting, Fishing, Farming, Mining, Holzfällen

Combat:
  - Digimon World Style (Echtzeit-Anfeuerung)
  - Oregon Trail Events (Prozedural)

Movement:
  - Fortnite-Style: Sprint, Slide, Dash, Wall-Climb, Vault

World:
  - File Island + 8 Städte
  - Prozedural-Dungeons

Training:
  - Hunger, Durst, Müdigkeit, Glück
  - Stats-System mit Progression

Räume (12 total):
  - Wohnzimmer, Schlafzimmer, Küche, Badezimmer
  - Garten, Musikraum, Medizin, Terminal
  - Studieren & Crafting, Trainingszimmer
  - Kampfarena, Schwarze Mühle - Keller
```

---

## 6. TECHNISCHE ARCHITEKTUR (ENTSCHEIDUNG)

### OPTION C: HYBRID (GEWÄHLT)
```python
ARCHITECTURE = {
    "core": {
        "status": "IMMUTABLE",
        "components": [
            "najika_brain.py",
            "personality_engine.py",
            "security.py"
        ]
    },

    "modules": {
        "status": "DYNAMIC",
        "loading": "on-demand",
        "examples": [
            "schwarze_muehle.py",
            "oregon_engine.py",
            "explosion_class.py",
            "crafting.py"
        ]
    }
}
```

### AI-ROUTING (HYBRID)
```python
AI_ROUTING = {
    "quick_response": "llama3.2:3b (lokal)",      # 0ms delay
    "deep_thought": "gpt-4o (cloud)",             # Komplexe Fragen
    "analytical": "claude-3.5-sonnet (cloud)",    # Code/Analyse
    "creative": "llama3.2 (lokal)",               # Chaos & Kreativität
    "nsfw_mode": "wizard-vicuna-uncensored"       # Keine Filter
}
```

---

## 7. IMPLEMENTATION ROADMAP

### PHASE 1: KONSOLIDIERUNG (2-4 Wochen)
- [ ] Najika-Ultimate Model erstellen (Ollama)
- [ ] Private Mode (wizard-vicuna)
- [ ] Web Search (ddgs)
- [ ] KayKit Assets kopieren
- [ ] room_config_detailed.json nutzen

### PHASE 2: DIGIVICE (2-3 Wochen)
- [ ] Wände + Texturen sichtbar
- [ ] Alle 12 Räume funktionsfähig
- [ ] Schwarze Mühle → Digivice Integration
- [ ] PWA (Progressive Web App)

### PHASE 3: FEATURES (3-6 Monate)
- [ ] Oregon-Engine komplett
- [ ] Explosion-Klasse + Combat
- [ ] Crafting & Economy
- [ ] Weitere Module schrittweise

### PHASE 4: UEFN-PORT (6-12 Monate)
- [ ] Verse-Scripting
- [ ] Asset-Konvertierung
- [ ] Multiplayer-Anpassungen

### PHASE 5: ÖFFENTLICH (3-6 Monate)
- [ ] Content-Bereinigung
- [ ] Beta-Testing
- [ ] Launch

**GESAMT:** 18-30 Monate realistisch

---

## 8. DATEIEN-STATUS

### GELESEN ✅
- neu 1.txt (BASIS)
- upus letzter funktionierender q.txt (OPUS)
- najika_personality_CORE.json (PERSÖNLICHKEIT)
- PROJECT_GUIDE.md (ÜBERSICHT)
- COMPLETE_DIGIVICE_UPDATE.py (CODE)
- roadmap.txt (PLANUNG)
- 1111111111111111.txt (GPT CHAT)
- README_SEARCH.txt (KONZEPT)

### HIGH PRIORITY (zu lesen)
- najika_personality_PUBLIC.json
- adasw1111112neu alpha.txt (110 KB)
- qwqwneu neu neu .txt (213 KB)

---

## 9. KRITISCHE NOTIZEN

### OPUS' WARNUNG
```
❌ NICHT TUN:
- Opus Code umschreiben
- Neue Frameworks einbauen
- Development-System hinzufügen (zu komplex)
- index_3d.html neu bauen

✅ NUR TUN:
- Opus Code als BASIS
- Private Mode hinzufügen
- Web Search hinzufügen
- Assets kopieren
- Room Config nutzen
```

### ERFOLGS-KRITERIEN (MINIMUM)
```
✅ Chat mit llama3.2:3b
✅ Private Mode mit wizard-vicuna
✅ Digivice mit Skeleton Mage
✅ Wände + Boden sichtbar
✅ 2 Räume (wohnzimmer, kampfarena)
```

---

## 10. NÄCHSTE SCHRITTE (FÜR MICH)

### SOFORT:
1. ✅ Alle kritischen Dateien gelesen
2. ✅ Master-Dokument erstellt
3. **⏳ WARTE AUF USER FREIGABE**

### DANACH:
1. najika_personality_PUBLIC.json lesen
2. Restliche NEU-Dokumente lesen
3. CODE-BLÖCKE schreiben:
   - NAJIKA_ULTIMATE_INSTALLER.ps1
   - Private Mode Integration
   - Web Search Integration
   - Asset Copy Script
   - Complete Server Setup

---

## 11. USER PRÄFERENZ

- **Code-Format:** Große, ausführbare Blöcke
- **Sprache:** Deutsch
- **Fokus:** Private Version zuerst
- **Basis:** Opus Code NICHT umschreiben
- **Stil:** Funktional, keine Experimente

---

**STATUS:** BEREIT FÜR IMPLEMENTIERUNG
**WAITING:** User Approval
