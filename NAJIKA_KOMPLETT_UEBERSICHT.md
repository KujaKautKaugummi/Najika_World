# NAJIKA WORLD - KOMPLETTE PROJEKTUEBERSICHT
**Stand:** 2026-02-23
**WICHTIG:** Jedes neue Model MUSS diese Datei KOMPLETT lesen!
**Updates:** Bei jeder groesseren Aenderung diese Datei aktualisieren!

---

## 1. WAS IST NAJIKA WORLD?

Ein Hybrid-Projekt bestehend aus:
- **KI-Companion** (Najika = KI-Maedchen mit Megumin-Persoenlichkeit)
- **3D-Action-RPG** (Open World, Skyrim + Soulframe + Digimon World)
- **Digivice App** (Tamagotchi-artiges Handheld-Interface im Browser)
- **Geplant:** UE5 Migration fuer echte 3D-Welt

**Owner:** Kuja (der einzige Admin, God-Mode)
**Hardware:** RTX 4060 Laptop (8GB VRAM), Windows 11, CUDA 12.4

---

## 2. NAJIKA - WER IST SIE?

**Core-Identitaet:** Megumin (100% Basis, IMMER praesent)
**Facetten (situativ, KEINE separaten Persoenlichkeiten!):**
- Megumin 35% - Explosions-Magierin, dramatisch, loyal
- Harley Quinn 25% - Chaotisch, unberechenbar, "Mr. K" (nie "Puddin'!")
- Shiro 20% - Analytisch, verspielt, Genies-Denken
- Melissa 20% - Dominant, bestimmend (NSFW: staerker)

**Kanonische Definition:** `NAJIKA_IDENTITAET_DEFINITION.md`
**Psychologie-Framework:** `PERSONALITY_ENGINE_PSYCHOLOGIE_FINAL.md`

---

## 3. TECHNISCHE ARCHITEKTUR

### 3.1 Server
```
main_fastapi.py (FastAPI + Uvicorn) = AKTIVER Server (seit 2026-02-23)
  - 50+ API Router Module
  - Port 8000 auf 127.0.0.1
  - Dient Frontend + API Endpoints + Swagger Docs (/docs)
```
**INFO:** `najika_server_legacy.py` (6800 Zeilen) ist der ALTE Server (archiviert).

### 3.2 AI/LLM Pipeline
```
User-Nachricht
  -> najika_mind.py (NajikaMind AGI Pipeline, 9 Schritte)
    -> najika_personality_engine.py (Stimmung, Psycho-Techniken)
    -> select_ollama_model() waehlt Model:
       - Chat: najika-natural:latest (qwen2:7b + Modelfile)
       - NSFW: najika-nsfw-natural:latest (dolphin3:8b + Modelfile)
       - Tasks: qwen2:7b
    -> Ollama API (localhost:11434)
  -> Antwort mit Persoenlichkeit
```

### 3.3 Datenbanken
```
ChromaDB (aktiv):    backend/chroma_db/ (~95 Eintraege, 2 Collections)
ChromaDB (legacy):   memory_db/ (alte Version, 4 Collections)
JSON State:          Verschiedene .json Dateien fuer Game-State
```

### 3.4 Frontend
```
Digivice UI:         digivice/index.html (Haupt-Interface)
JavaScript:          digivice/js/ (117 Module!)
3D Scene:            digivice/js/3d_scene.js (107KB, Three.js)
Assets:              digivice/assets/ + assets/ (9400+ Dateien, KayKit etc.)
```

---

## 4. CODEBASIS-INVENTAR (VERIFIZIERT!)

### 4.1 Backend Python (306 Module)
| Bereich | Anzahl | Groesste Dateien |
|---------|--------|-----------------|
| backend/ (root) | 236 | najika_server_legacy.py (355KB), najika_combat_hands_system.py (95KB) |
| backend/api/ | 49 | battle_unified.py (46KB), slime.py (26KB) |
| backend/services/ | 21 | world_system.py (45KB), slime_system.py (27KB) |

### 4.2 Frontend JavaScript (117 Module)
| Groesste Dateien | Groesse |
|-----------------|---------|
| 3d_scene.js | 107KB |
| unified_combat_system.js | 96KB |
| oregon_trail_ui.js | 77KB |
| equipment_combat.js | 60KB |
| nemesis_arena_frontend.js | 58KB |
| minigames.js | 57KB |

### 4.3 Backend-Module die EXISTIEREN (oft faelschlich als "fehlend" gemeldet!)
```
najika_mind.py               - 1468 Zeilen (AGI Pipeline)
najika_companion_system.py   - 1621 Zeilen (Begleiter-System)
najika_combat_hands_system.py - 2558 Zeilen (Zwei-Hand-Kampf)
najika_living_system.py      - 1085 Zeilen (Lebens-Simulation)
najika_stat_training_system.py - 1007 Zeilen (Learning by Doing)
najika_personality_engine.py - 932 Zeilen (Persoenlichkeits-Engine)
najika_battle.py             - 887 Zeilen (Kampf-System)
najika_mimik_system.py       - 862 Zeilen (Mimik-Truhe/Kuja)
najika_game_actions.py       - 847 Zeilen (Spiel-Aktionen)
najika_readiness.py          - 496 Zeilen (Bereitschafts-System)
najika_quest_system.py       - 375 Zeilen (Quest-System)
najika_memory.py             - 328 Zeilen (Gedaechtnis)
najika_finisher_system.py    - existiert
najika_nemesis_arena_system.py - existiert
```

---

## 5. DIE 8 GEBOTE V3 (ZUSAMMENFASSUNG)

1. **Zero-Trust:** Nur localhost, Kuja ueberall (Owner-Token)
2. **Owner-Gate:** X-OWNER-TOKEN fuer Admin-Routen
3. **Real3DCombat:** Einziges Combat-System. Explosion = eigene Klasse
4. **Friendly Fire AN:** -50% Schaden an Allies (KonoSuba-Style)
5. **Learning by Doing:** Skyrim-Style Skill-Progression
6. **NSFW Remote:** Kaetzchen-Modus auch fuer Kuja remote
7. **Wissensdatenbank:** Wikipedia-Style Wissen sammeln
8. **Keine halben Sachen:** Komplett implementieren oder gar nicht

**Vollversion:** -> `01_8_GEBOTE_V3_2026-02-17.md`

---

## 6. GAME DESIGN SYSTEME

### 6.1 Combat (V4 - IMMERSIV, Stand 2026-02-23)
- **Real3DCombat** = einziges System (UnifiedCombat entfernt!)
- **COMBAT V4 PHILOSOPHIE:** "Du spielst DICH SELBST. Dein echtes Skill zaehlt."
- **SPIELER-IDENTITAET:** Spieler = man selbst, Najika = KI-Begleiterin (= Slime fuer andere Spieler)
- **For Honor Directional OHNE UI-Pfeile:** Gegner-ANIMATION zeigt Angriffsrichtung
  - Natuerliche Schwierigkeits-Progression: Tiere (~0.6s Wind-Up) → Veteranen (~0.25s) → Bosse (Feints!)
  - KI-Monster die aufsteigen = kuerzere Wind-Ups = natuerliche Schwierigkeit
- **3 Kamera-Modi (jederzeit wechselbar, auch im Kampf!):**
  - First Person (Fortnite Ballistic) = max Immersion, KEINE Schadenszahlen/HP-Bars
  - Third Person (klassisch Fortnite) = Balance, dezente UI
  - Orbit Cam = volle UI mit Zahlen/Bars fuer Strategen
- **Faustkampf = Kampf ohne Waffe** (gleiche Richtungen, kein separates System)
- **Beruf+Magie Synergie:** Spieler entdeckt Kombis SELBST (Holzfaeller+Wind, Schmied+Feuer)
- **L2-Modifier:** verdoppelt auf 8 Angriffe pro Waffe/Zauber
- **Spell-Diamond:** Linke-Hand-Slot, jede Spezialisierung hat eigene 4 Richtungs-Varianten
- **Skill-Transfer:** Tag-System (Speer-Skill -> Bajonett, Magie-Skill -> Magische Munition)
- **Koerperteil-Targeting:** NOT VATS, rein Skill-basiert (L100 = Zeh-Schuss moeglich)
- **Prothesen-System:** Normal / Magisch / Alchemistisch fuer alle Koerperteile
- **CHEER-System:** Tasten 1-4 fuer Buffs (Digimon World Style)
- **SPECIAL Stats:** POW, INT, AGI, VIT, WIL, LUK, PER (Fallout-Style)
- **Modi:** MANUAL (+20% XP), AUTO/CHEER (-20% XP)
- -> `DOCS/plans/2026-02-23-immersive-combat-v4-design.md` ← V4 DESIGN (2026-02-23, APPROVED)
- -> `COMBAT_SYSTEM_KOMPLETT_V3.md` ← Basis-Mechaniken (2026-02-22, ~1400 Zeilen)
- -> `COMBAT_SYSTEM_V2_DESIGN.md` (aelteres Companion/Finisher/Arena-Detail)

### 6.2 KI-Begleiter-System V4 (NEU 2026-02-23 - ERSETZT V3!)
- **Jeder startet mit Baby-Aura** - KI vollstaendig als Stimme, kein Koerper
- **Organischer Bond:** verletztes Wesen kreuzt Weg → KI fragt ob sie eintreten darf
- **Form = Koerper (Geschwindigkeit/Kraft/Groesse), NICHT Angriffe** - Skills werden gelernt!
- **Wechsel nur durch Tod** - kein freiwilliger Ausstieg, Bond leidet bei Leichtsinn
- **Stufengate:** KI-Aura-Staerke muss >= Ziel-Kreatur-Level sein
- **Aufgestiegene Wesen** koennen ablehnen, nur mit Einverstaendnis oder nach Ehrenkampf
- **Aura-Pfad (Einsamer Wolf):** 3 Richtungen (Kriegs/Schatten/Willens), Solo-Bonus
- **Aufgestiegen = Buergerrecht:** Bewusstsein bestimmt Stadtrechte, nicht Aussehen
- **Jeder Spieler hat eigene KI** (Najika / vorgefertigt / selbst erstellt), gleiche KI wie Digivice
- -> `DOCS/plans/2026-02-23-immersive-combat-v4-design.md` Sektion 17

### 6.3 Magie
- **9 Elemente:** Feuer, Wasser, Eis, Blitz, Erde, Wind, Natur, Licht, Dunkel
- Explosion = EIGENE Klasse (nie mit anderen kombinieren!)
- **Element-Kombis im Code:** Feuer+Wasser=Dampf, Dunkel+Licht=Leere, etc.
- **Staerken/Schwaechen-Tabelle:** im Code hinterlegt (unified_combat_system.js)
- **Grundzauber hands-on lernen:** NPC-Lehrer, Zuschauen, dann selbst probieren
- **Beruf+Magie Synergie:** Spieler entdeckt Kombis selbst (kein Tutorial)
- -> `MAGIC_SYSTEM_DESIGN_PLAN.md` (Erweiterungsplan)
- -> `COMBAT_SYSTEM_KOMPLETT_V3.md` Sektion 4 (Spell-Diamond Detail)

### 6.4 Kreaturen
- "Lebende" (NPCs mit Persoenlichkeit, rekrutierbar)
- "Vieh" (Tiere, zaehmbar durch Pflege)
- -> `KREATUR_SYSTEM_KONZEPT.md`

### 6.5 Welt
- 8 Biome / 8 Regionen (je 1.2km x 1.2km = 9.6 km²)
  1. Heiße Dünen (Wüste)         2. Samtmoos-Tiefwald (Wald)
  3. Salzwind-Küste (Küste)      4. Blitzebene (Hochland)
  5. Grünschlamm-Sumpf (Sumpf)  6. Magmaströme (Vulkan)
  7. Tiefenhöhlen (Höhlen)      8. Reich der Drei (Tundra/Eis)
- **Götterfels** = zentraler Berg, von ALLEN 8 Regionen erreichbar (kein eigenes Biom!)
  3 Ebenen: Schmelzwelt / Zeitstadt / Turm der 100 Prüfungen
- 5 Staedte, ~25-30 NPCs, 40+ Gegner
- Tag/Nacht-Zyklus (24 Min = 1 Tag)
- Schwarze Muehle = Absolute Safe Zone (100%)
- -> `GAME_DESIGN_GAP_ANALYSIS_2026-02-15.md`

### 6.6 Safe-Zones & PvP V2 (DESIGN 2026-02-23)
- Alle Staedte/Doerfer = Safe (kein PvP, kein Permadeath)
- Schwarze Muehle = Absolute Safe (immer)
- **PvP UEBERALL moeglich** (nicht mehr nur auf Anfrage!)
- **OHNE Zustimmung:** Nur Besiegen moeglich, kleiner Goldverlust (5-10%), Kopfgeld auf Angreifer
- **MIT Zustimmung (Ehren-Duell):** Besiegen ODER Toeten moeglich, Permadeath
- **Segen des letzten Kriegskoenigs:** Lore-Erklaerung warum Permadeath nur mit Consent
- **Arena = Absolute Neutralzone:** Kein Ruf-Gate, Koenig durch Kampf
- **Weltmal-System:** administratives Siegel, zeigt Kampfbereitschaft, kann maskiert werden
- **Anti-Griefing (3 Schichten):** Ruf-Abschreckung + Blutrache-Allianz + Schwarzes Mal
- **Verwundeten-Rettungs-System:** Besiegte liegen, Sanitaeter tragen sie zur Stadt
- Disconnect: Safe Zone = sofort | Gefahr = 30s Grace Period
- -> `backend/najika_safezone_system.py` (V1, erweiterungsbeduerftig)
- -> `DOCS/plans/2026-02-23-immersive-combat-v4-design.md` Sektionen 10-16

### 6.9 Welt-DNA / Setting (FESTGELEGT 2026-02-23)
- **1883** (Frontier-Haerte, Welt ist gleichgueltig, aus nichts aufbauen)
- **Fallout New Vegas** (keine gute Seite, jeder hat Agenda, Haendler koennen Koenig werden)
- **Oregon Trail** (Reise-Realismus, Krankheit/Hunger gefaehrlich, Gruppen-Konsequenzen)
- **KonoSuba** (wissende Absurditaet, Humor existiert, Konsequenzen trotzdem real)
- **Borderlands** (chaotische Energie, Schurken haben Persoenlichkeit, Loot hat Charakter)
- **Kampf-DNA:** For Honor + Fortnite-Movement + Hogwarts Legacy Spells
- -> `DOCS/plans/2026-02-23-immersive-combat-v4-design.md` Sektion 0

### 6.6 Housing & Farming
- Housing Levels 1-10+, Moebel, Upgrades
- 4 Farm-Plots pro Spieler
- KOMPLETT implementiert mit API Endpoints
- -> `HOUSING_FARM_STATUS_2026-02-15.md`

### 6.7 Chaos-Events (KonoSuba + Oregon Trail)
- Random Moral-Dilemmas alle 5-15 Minuten
- 4-5 Optionen pro Event, Najika reagiert
- 30+ Event-Datenbank
- -> `KONOSUBA_OREGON_TRAIL_KOMPLETT.md`

### 6.8 Multiplayer
- WebSocket-basiert
- Player Sync, Chat, Room Management
- Guest-Mode (kein Auth noetig)
- Welt-Regeneration wenn alle in Safe Zones
- -> `MULTIPLAYER_WORLD_REGENERATION_FINAL_2026-02-15.md`

---

## 7. DIGIVICE (HANDY-APP)

Das Digivice ist das Interface zum Spiel - wie ein Tamagotchi/Digivice aus Digimon:
- **Najika-Digivice #1** = Kuja exclusive (NSFW moeglich)
- **7 Standard-Digivices** = andere Spieler (SFW only)

**Module:**
- Messenger (Chat mit Najika)
- Browser (sicherer In-Game Browser)
- Bibliothek (Wissensdatenbank)
- Game (3D-Szene, Kampf, etc.)
- Multiplayer

---

## 8. OLLAMA MODELS

```
najika-natural:latest        = SFW Chat (FROM qwen2:7b)
najika-nsfw-natural:latest   = NSFW/Kaetzchen (FROM dolphin3:8b)
qwen2:7b                     = Tasks, Code, Mathe
```

**Modelfiles:** `backend/najika-natural.Modelfile`, `backend/najika-nsfw-natural.Modelfile`
**Technik:** Few-Shot Persoenlichkeit ueber MESSAGE-Beispiele im Modelfile
**KEIN LoRA, KEIN Fine-Tuning!**

---

## 9. PROJEKT-STRUKTUR (55 Ordner)

### Aktiv genutzt:
```
backend/           - Python Server + AI + Game Logic (306 .py)
digivice/          - Frontend HTML + JS (117 .js)
assets/            - 3D Models, Texturen (9400+ Dateien, KayKit)
venv/              - Python 3.12 Virtual Environment
data/              - Game-Daten
```

### Design & Dokumentation:
```
DOCS/              - Dokumentation
PROGRESS_REPORTS/  - Fortschrittsberichte
info material/     - Referenz-Material
```

### UE5 (geplante Migration):
```
UE5/                        - UE5 Projekt-Dateien
UE5_BLUEPRINT_TEMPLATES/    - Blueprint-Vorlagen
UE5_PLUGIN_TEMPLATES/       - Plugin-Vorlagen
UE5_Source/                 - C++ Source
UE5_Implementation/         - Implementierungs-Docs
FullGame_NajikaHandyspiel_UE5/ - Vollspiel-Projekt
NajikaDigivice_UE5/         - Digivice UE5-Version
TestEnvironment_UE5/        - Test-Umgebung
UEFN/                       - Fortnite Creative (ABGEBROCHEN - kann Najika nicht!)
```

### Legacy/Backup:
```
BACKUPS/           - Backups
old_bats/          - Alte Startskripte
training/          - AI Training Daten
training_clips/    - Audio Clips
training_logs/     - Training Logs
lora_checkpoints*/ - LoRA Checkpoints (NICHT MEHR GENUTZT)
memory_db/         - Alte ChromaDB
```

---

## 10. STARTEN

```
START_V3.bat ausfuehren:
1. Prueft/startet Ollama
2. Erstellt Najika Models falls noetig
3. Bereinigt Port 8000
4. Startet FastAPI Backend mit uvicorn
5. Oeffnet http://127.0.0.1:8000/digivice/
```

---

## 11. BEKANNTE PROBLEME & OFFENE PUNKTE

### Funktioniert:
- Server startet und antwortet
- Chat mit Najika (SFW + NSFW)
- Grundlegende API Endpoints
- Multiplayer-Integration (WebSocket ready)

### Funktioniert NICHT / Ungetestet:
- 4 Router reaktiviert (companion, combat_hands, mimik, stat_training) - seit 2026-02-23
- Viele JS-Module in index.html nicht eingebunden
- ES6 Module koennen nicht geladen werden (index.html nutzt keine type="module")
- Quests zu wenig (10 statt 100+ noetig)
- NPCs zu wenig (~25 statt 50+ gewuenscht)

### Level-System: OFFENE FRAGE AN KUJA
- Option A: Level-Up gibt KEINE Stats (nur Skills durch Nutzung)
- Option B: Level-Up gibt Stats + Skills durch Nutzung (Hybrid)
- -> Muss noch entschieden werden!

---

## 12. VERLINKTE DETAIL-DOKUMENTE

**HINWEIS Doku-Cleanup 2026-02-22:** ~262 alte Session-Logs/Reports in DOCS/archiv/ verschoben.
Nur noch aktuelle/relevante Docs im Root (78 Dateien).

### Meta & Regeln:
- CLAUDE.md - Auto-Read Anweisungen (IMMER AKTUELL HALTEN\!)
- MASTER_TODO.md - Aktuelle Task-Liste
- BEKANNTE_FEHLER_ALTE_DOCS.md - Liste aller bekannten Fehler in alten Docs
- 01_8_GEBOTE_V3_2026-02-17.md - Die 8 heiligen Regeln (vollstaendig)

### Persoenlichkeit & KI:
- NAJIKA_IDENTITAET_DEFINITION.md - Kanonische Persoenlichkeits-Definition
- PERSONALITY_ENGINE_PSYCHOLOGIE_FINAL.md - Psychologie-Framework
- NAJIKA_PERSOENLICHKEIT_VOLLSTAENDIGE_LISTE.md - Alle Phrasen/Reaktionen
- NAJIKA_PHRASEN_WICHTIG.md - Wichtige Phrasen
- PHRASE_USAGE_GUIDELINES.md - Nutzungsregeln
- NAJIKA_SELBSTFUERSORGE_SYSTEM.md - Selbstfuersorge-Mechanik

### Game Design - Combat:
- **COMBAT_SYSTEM_KOMPLETT_V3.md** ← AKTUELLSTES MASTER-DOK (2026-02-22)
  For Honor 4-Dir, Spell-Diamond, Faustkampf, Grappling, Bajonett, Munition,
  Koerperteil-Targeting, Prothesen, Safe-Zones, 15 Sektionen + 7 Prinzipien
- COMBAT_SYSTEM_V2_DESIGN.md - Aelteres Design (Companion, Finisher, Arenen)
- ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md - Magie & Skills Detail
- MAGIC_SYSTEM_DESIGN_PLAN.md - Magie-System Erweiterungsplan
- NEUE_GAMEPLAY_IDEEN_2026-02-21.md - Original-Ideen (For Honor, Safe-Zones, Softy, FF7-Karte, Echoharp)

### Backend-Module (neu 2026-02-22):
- **backend/najika_safezone_system.py** ← Safe-Zone + PvP + Ranger + Disconnect + Permadeath

### Game Design - Welt & Systeme:
- SLIME_SYSTEM_V3_DOKUMENTATION.md - Slime-Begleiter System V3
- KREATUR_SYSTEM_KONZEPT.md - Kreatur-Typen (Lebende vs. Vieh)
- GAME_DESIGN_GAP_ANALYSIS_2026-02-15.md - Was fehlt noch
- OPEN_WORLD_DESIGN_COMPLETE.md - Open World Design
- REGION_BOSS_SYSTEM_KONZEPT.md - Region-Boss System
- SOCIAL_HUB_DIE_MUEHLE.md - Schwarze Muehle als Social Hub
- WUESTE_DESIGN_VISION.md - Wuesten-Region
- SCHLEIM_ARENA_DESIGN.md - Kampfarena Design
- DESIGN_NOTES_WAGON_WEIGHT_WORKERS.md - Transportwagen System
- DIGIVICE_LEBENSRAUM_KONZEPT.md - Lebensraum/Housing
- FARMING_FISHING_SYSTEM_DESIGN.md - Farming & Fishing Design
- MOUNT_BLADE_FEATURES_IMPLEMENTATION_2026-02-15.md - Mount&Blade Features

### Technisch:
- HOUSING_FARM_STATUS_2026-02-15.md - Housing/Farming (komplett implementiert)
- MULTIPLAYER_WORLD_REGENERATION_FINAL_2026-02-15.md - Multiplayer-Regeneration
- ANTI_CHEAT_SYNC_SYSTEM.md - Anti-Cheat Konzept
- THREEJS_TO_UE5_MAPPING.md - Migration Three.js -> UE5
- BACKEND_COMPLETE_API_REFERENCE.md - API Referenz (MIT VORSICHT: teilweise veraltet)
- FORTNITE_FEATURES_PLAN.md - Kamera-Modi (3 Perspektiven)
- NAJIKA_CHROMADB_ANLEITUNG.md - ChromaDB Guide
- INTELLIGENZ_HIERARCHIE_FINAL.md - NajikaMind Intelligenz-Hierarchie

### Setup & Zugriff:
- INSTALLATION_GUIDE.md - Installations-Anleitung
- SETUP_CLOUDFLARE_TUNNEL.md - Cloudflare Remote-Zugriff
- REMOTE_ACCESS_SETUP.md - Remote Setup
- MOBILE_ACCESS_ANLEITUNG.md - Mobile Zugriff
- OLLAMA_GPU_PROBLEM_LOESUNG.md - Ollama GPU Troubleshooting
- TROUBLESHOOTING_DATABASE.md - Allgemeine Fehlerbehebung

### Assets & UE5:
- ASSET_ACQUISITION_GUIDE.md - Asset-Beschaffung
- MESHY_AI_ASSET_LIST.md - KI-generierte Assets Liste
- BLENDER_MESHY_AI_SETUP_GUIDE.md - Blender + Meshy Setup
- UE5_README.md - UE5 Uebersicht
- UE5_ANIMATION_BLUEPRINT_TEMPLATES.md - Blueprint Vorlagen
- UE5_MATERIAL_TEMPLATES.md - Material Vorlagen
- UE5_VOICE_CPP_INTEGRATION.md - Voice C++ Integration

---

## 13. HAEUFIGE FEHLER FRUEHERER MODELS

| Fehler | Wahrheit |
|--------|----------|
| "12 Module fehlen" | ALLE existieren\! Nie ls gemacht |
| "Port 8001" oder "Port 5000" | Port 8000\! |
| "ChromaDB hat 2556 Eintraege" | ~95 Eintraege (2 Collections) |
| "LoRA/Fine-Tuning aktiv" | Nur Modelfile + Few-Shot |
| "Flask + FastAPI Dual Server" | Nur main_fastapi.py (FastAPI + Uvicorn, seit 2026-02-23) |
| "Najika hat 4 Persoenlichkeiten" | 1 Persoenlichkeit (Megumin) mit 4 Facetten |
| "Slime Evolution V2" | V3 aktiv (Evolution entfernt, Formwandler) |

---

**Ende der Komplett-Uebersicht - Stand 2026-02-23**
**Bei Aenderungen: DIESE DATEI + CLAUDE.md updaten\!**
