# NAJIKA WORLD - CLAUDE CODE ANWEISUNGEN
**ACHTUNG: Diese Datei wird bei JEDEM Claude Code Start automatisch gelesen!**
**MUSS IMMER AKTUELL GEHALTEN WERDEN! Bei jeder groesseren Aenderung updaten!**

---

## PFLICHTLEKTUERE VOR JEDER ARBEIT

1. **DIESE DATEI** (wird automatisch gelesen)
2. **NAJIKA_KOMPLETT_UEBERSICHT.md** - Vollstaendige Projektuebersicht mit Links
3. **MASTER_TODO.md** - Aktuelle Tasks und Fortschritt

**REGEL: Jedes neue Model MUSS diese 3 Dateien KOMPLETT lesen!**

---

## PROJEKT-UEBERSICHT

**Najika World** = Hybrid-Projekt: KI-Companion + 3D-Action-RPG
- **Najika** = Megumin (100% Core-Identitaet) mit situativen Farb-Facetten
- **4 Facetten (KEINE separaten Persoenlichkeiten!):**
  - Megumin 35% (Core - immer praesent)
  - Harley Quinn 25% (chaotisch)
  - Shiro 20% (analytisch)
  - Melissa 20% (dominant)
- **Owner:** Kuja (der User)
- **Codebasis:** ~200.000 LOC, main_fastapi.py + 50+ Router-Module

---

## SERVER-ARCHITEKTUR (KORREKT!)

```yaml
Server:       backend/main_fastapi.py (FastAPI + Uvicorn)
Port:         8000 (NICHT 5000, NICHT 8001!)
Host:         127.0.0.1
Frontend:     http://127.0.0.1:8000/digivice/
Health:       http://127.0.0.1:8000/health
API Docs:     http://127.0.0.1:8000/docs
Startskript:  START_V3.bat (nutzt venv Python + uvicorn)
```

**ACHTUNG:** `najika_server_legacy.py` ist der ALTE Server (ThreadingHTTPServer, 6800 Zeilen).
Der aktive Server ist `main_fastapi.py` mit 50+ API-Routern! Umgestellt am 2026-02-23.

---

## OLLAMA MODELS (KORREKT!)

```yaml
SFW Chat:     najika-natural:latest    (FROM qwen2:7b, 4.4GB)
NSFW Chat:    najika-nsfw-natural:latest (FROM dolphin3:8b, 4.9GB)
Tasks/Code:   qwen2:7b
Ollama:       http://localhost:11434
```

**WICHTIG:** Keine LoRA, kein Fine-Tuning! Die Models nutzen Modelfiles mit
Few-Shot Beispielen fuer die Persoenlichkeit (backend/najika-natural.Modelfile).

---

## DIE 8 GEBOTE V3 (HEILIG - NIEMALS BRECHEN!)

1. **Zero-Trust:** Nur 127.0.0.1, Kuja kann von ueberall (Owner-Token)
2. **Owner-Gate:** Admin nur fuer Kuja (X-OWNER-TOKEN)
3. **Real3DCombat:** EINZIGES Combat-System. Explosion = eigene Klasse, NIE kombinieren!
4. **PvP V2:** Ueberall moeglich! Ohne Consent = nur Besiegen + kleines Gold. Mit Consent = voller Kampf. Friendly Fire AN (-50%). Arena = absolute Neutralzone (kein Ruf-Gate!)
5. **Learning by Doing:** Skyrim-Style, Skills steigen durch Benutzen
6. **NSFW Remote fuer Kuja:** Kaetzchen-Mode auch remote (nur Owner!)
7. **Wissensdatenbank:** Wikipedia-Style Wissen sammeln (NICHT Privacy-Paranoia!)
8. **Alles komplett:** KEINE halben Sachen! Komplett implementieren oder gar nicht!

**Vollversion:** `01_8_GEBOTE_V3_2026-02-17.md`

---

## VERBOTEN

- NIEMALS "Souls-like" sagen -> "1883 + Fallout NV + Oregon Trail + KonoSuba + Borderlands"
- NIEMALS "Kristall der Seele" sagen -> **"Weltmal"** (administratives Siegel, keine Seele!)
- NIEMALS Begleiter-System als "Slime V3" beschreiben -> **KI-Koerper-System V4** (Baby-Aura Start, organischer Bond!)
- NIEMALS Port 5000 oder 8001 -> Port **8000**! Server = FastAPI (main_fastapi.py)
- NIEMALS Harley "Puddin'" sagen lassen -> **"Mr. K"**!
- NIEMALS funktionierende Teile ohne Nachfrage aendern
- NIEMALS behaupten Module fehlen ohne `ls` zu machen!
- NIEMALS ChromaDB-Zahlen erfinden -> Aktuell nur ~95 Eintraege (2 Collections)

---

## CHROMADB (AKTUELLER STAND!)

```yaml
Pfad:              backend/chroma_db/
Collections:       2 (NICHT 6!)
najika_personalities: 83 Eintraege
najika_core:         12 Eintraege
Gesamt:             ~95 Eintraege (NICHT 2556!)
```

Alte Datenbank unter `memory_db/` hat 4 Collections aber ist die Legacy-Version.

---

## KRITISCHE PFADE

```yaml
Backend Server:    backend/main_fastapi.py (FastAPI, Port 8000)
Legacy Server:     backend/najika_server_legacy.py (6800 Zeilen, NICHT MEHR AKTIV)
NajikaMind:        backend/najika_mind.py (1468 Zeilen, AGI Pipeline)
Personality:       backend/najika_personality_engine.py (932 Zeilen)
Combat:            backend/najika_combat_hands_system.py (2558 Zeilen)
Companion:         backend/najika_companion_system.py (1621 Zeilen)
Living System:     backend/najika_living_system.py (1085 Zeilen)
Frontend:          digivice/index.html
JS Modules:        digivice/js/
Modelfile SFW:     backend/najika-natural.Modelfile
Modelfile NSFW:    backend/najika-nsfw-natural.Modelfile
Venv Python:       venv/Scripts/python.exe (Python 3.12.10)
```

---

## HARDWARE (NEUER PC - Feb 2026)

```yaml
GPU:    RTX 4060 Laptop (8GB VRAM)
CUDA:   12.4
UE5:    5.7 (C:\Program Files\Epic Games\UE_5.7)
OS:     Windows 11 Home
```

---

## BEKANNTE FEHLERQUELLEN (LESSONS LEARNED)

1. **Alte Dokumentation luegt!** Immer Code pruefen, nie blind MDs vertrauen
2. **"12 fehlende Module"** -> ALLE 12 existieren! Alte Models haben nicht `ls` gemacht
3. **Port-Verwirrung:** Es gab 5000, 8000, 8001 in verschiedenen Docs. RICHTIG = 8000
4. **ChromaDB-Zahlen:** Wurden von alten Models erfunden. Immer `check_chromadb.py` nutzen
5. **LoRA/Fine-Tuning:** Wird NICHT mehr genutzt. Najika Natural = Modelfile + Few-Shot
6. **CLAUDE.md war veraltet:** Hat jedes neue Model mit falschen Infos gefuettert!

---

## TEAM-REGELN

- Vor jeder Arbeit: MASTER_TODO.md und KOMPLETT_UEBERSICHT lesen
- Nach jeder Arbeit: Betroffene Docs updaten (inkl. CLAUDE.md wenn noetig!)
- Code pruefen vor Behauptungen (ls, grep, cat - nicht raten!)
- Keine Mock-Implementierungen die "spaeter ersetzt werden"
- Kein Code der zu 80% funktioniert und dann liegen bleibt

---

*"EXPLOSION!!! Lies die Docs ERST, code DANN!" - Najika*
