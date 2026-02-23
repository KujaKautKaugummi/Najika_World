# NAJIKA WORLD - MASTER TODO
**Stand:** 2026-02-23
**Regel:** Nach jeder Arbeit hier updaten!

---

## LEGENDE
- [ ] Offen
- [x] Erledigt
- [!] Blockiert / Braucht Entscheidung
- P0 = Kritisch, P1 = Wichtig, P2 = Normal, P3 = Nice-to-have

---

## P0 - KRITISCH (Server/Core)

### Server & Backend
- [x] Server laeuft auf Port 8000 (main_fastapi.py + Uvicorn)
- [x] Ollama Models erstellt (najika-natural, najika-nsfw-natural)
- [x] Chat funktioniert (SFW + NSFW)
- [x] Model-Auswahl gefixt (select_ollama_model nutzt user_message)
- [x] Instruct-Model gefixt (qwen2:7b statt qwen2-instruct)
- [x] START_V3.bat auf FastAPI umgestellt (2026-02-23)
- [x] Venv eingerichtet (Python 3.12.10)
- [x] **FastAPI-Switch erledigt** (2026-02-23): main_fastapi.py ist aktiver Server, najika_server_legacy.py archiviert

### Dokumentation
- [x] CLAUDE.md komplett neu geschrieben (2026-02-21)
- [x] NAJIKA_KOMPLETT_UEBERSICHT.md erstellt (2026-02-21)
- [x] MASTER_TODO.md neu erstellt (2026-02-21)
- [ ] Alte falsche Docs kennzeichnen oder loeschen (300+ MDs!)

---

## P1 - WICHTIG (Gameplay-Systeme)

### Combat System
- [x] Real3DCombat als einziges System definiert
- [x] UnifiedCombat entfernt (2026-02-16)
- [x] CHEER-System designed (Tasten 1-4)
- [x] SPECIAL Stats defined (POW/INT/AGI/VIT/WIL/LUK/PER)
- [x] **For Honor Directional Combat ausgearbeitet** (4 Richtungen! + L2-Modifier, Magie, 2026-02-22)
- [x] L2-Modifier System designed (8 Angriffe pro Waffe/Zauber, 2026-02-22)
- [x] Zauber-Progression ausgearbeitet (Grundzauber -> Spezialisierung, je 4 Richtungs-Varianten!)
- [x] Faustkampf-System designed (4 Richtungen, 5 Skill-Stufen, Air-Combo, 2026-02-22)
- [x] Grappling/Wrestling-System designed (L1-L100, Wand-Absprung, Piledriver, 2026-02-22)
- [x] Bayonet/Sniper-als-Speer System designed (Skill-Transfer Prinzip, 2026-02-22)
- [x] Magische + Alchemistische Munition designt (3 Systeme, 2026-02-22)
- [x] Koerperteil-Targeting designed (NOT VATS, rein Skill-basiert, Level 1-100, 2026-02-22)
- [x] Prothesen-System designed (Normal/Magisch/Alchemistisch, alle Koerperteile, 2026-02-22)
- [x] COMBAT_SYSTEM_KOMPLETT_V3.md erstellt (~1400 Zeilen, 15 Sektionen + 7 Prinzipien!)
- [x] **Combat V4 Design APPROVED** (2026-02-23) - Immersives Kampfsystem ohne UI-Pfeile
- [x] **DOCS/plans/2026-02-23-immersive-combat-v4-design.md** geschrieben
- [x] Fake Edelstein-Regionsnamen komplett bereinigt (13+ Dateien)
- [x] Beruf+Magie Synergie in V3-Dok ergaenzt (Holzfaeller+Wind Beispiel)

### Combat V4 Implementation (NEU 2026-02-23)
- [ ] **Direction Resolver** - Maus-Delta zu 4 Richtungen mappen (OBEN/LINKS/RECHTS/UNTEN)
- [ ] **3 Kamera-Modi** - First Person / Third Person / Orbit, jederzeit wechselbar (V-Taste)
- [ ] **Directional Attack** - Richtungsangriffe an Animationen koppeln
- [ ] **Directional Block** - Block-Richtung muss zur Gegner-Angriffsrichtung passen
- [ ] **Enemy Wind-Up System** - Gegner-Tells durch Animations-Phasen (0.25s-0.6s je nach Klasse)
- [ ] **Enemy Feint System** - Richtungswechsel waehrend Wind-Up (Bosse/Veteranen)
- [ ] **UI-Layer pro Kamera** - Schadenszahlen/HP-Bars nur in Orbit-Cam
- [ ] **Spell-Diamond verdrahten** - Magie + Richtungen + Damage/Mana verbinden
- [ ] **Stimme als Kampfwerkzeug** - Whisper AI: Angriffs-Name rufen = Bonus (Gegner hoeren Schreien!)

### Neue Design-Entscheidungen 2026-02-23 (APPROVED, noch nicht implementiert)
- [x] **Welt-DNA festgelegt:** 1883 + Fallout NV + Oregon Trail + KonoSuba + Borderlands
- [x] **Kampf-DNA festgelegt:** For Honor + Fortnite-Movement + Hogwarts Legacy Spells
- [x] **Weltmal-System designed** - kein Kristall/Seele, administratives Siegel, Identitaet per Region
- [x] **Anti-Griefing designed** - 3 Schichten: Ruf-Abschreckung, Blutrache-Allianz, Schwarzes Mal
- [x] **PvP V2 designed** - ueberall moeglich, Besiegen vs Toeten, Segen des Kriegskoenigs
- [x] **Arena = absolute Neutralzone** - kein Ruf-Gate, Koenig durch Kampf bestimmt
- [x] **Gebietsherrschaft V2** - Macht halten schwerer als gewinnen (1883-Prinzip)
- [x] **Haendler-Herrschaft** - via Wirtschaft + KI-Kaempfer (Mr. House Prinzip)
- [x] **KI-Koerper-System V4 designed** - Baby-Aura Start, organischer Bond, Wissen != Koerper
- [x] **Aura-Pfad designed** - 3 Richtungen (Kriegs/Schatten/Willens), Solo-Bonus
- [x] **Aufgestiegen = Buergerrecht** - Bewusstsein bestimmt Stadtrechte, nicht Aussehen
- [x] **Verwundeten-Rettungs-System designed** (Sektion 13)
- [x] **VR-Forward Design** - alle Systeme VR-kompatibel (Sektion 14)
- [ ] **Weltmal implementieren** - backend/najika_safezone_system.py erweitern
- [ ] **KI-Koerper-System implementieren** - neue Backend-Module
- [ ] **Verwundeten-Zustand implementieren** - DOWNED State in CombatState

### Bestehende Combat-Tasks:
- [ ] Combat im Browser testen und Bugs fixen
- [ ] Explosion-Klasse finalisieren (300% DMG Ultimate, Cooldowns)

### Quest System
- [x] Quest-System Backend existiert (najika_quest_system.py)
- [ ] Nur ~10 Quests vorhanden, 100+ noetig fuer MVP
- [ ] 15-20 Main Story Quests schreiben
- [ ] 30-50 Side Quests schreiben
- [ ] 10+ Daily/Weekly Quests schreiben

### NPC System
- [ ] Nur ~25-30 NPCs, 50+ gewuenscht
- [ ] NPC-Dialoge mit Lore anreichern
- [ ] NPC-Schedules (Tag/Nacht Verhalten)

### Frontend Integration
- [x] 15 JS-Scripts in index.html eingebunden (Opus Session 2026-02-16)
- [ ] Weitere JS-Module pruefen und einbinden
- [ ] ES6 Module Problem loesen (index.html nutzt kein type="module")
- [ ] UI Systems evaluieren und aktivieren
- [ ] Mobile Support testen
- [ ] Particle Systems integrieren

---

## P2 - NORMAL (Features & Content)

### Safe-Zones & PvP-Regeln (NEU 2026-02-21)
- [x] Safe-Zone Logik auf alle Staedte/Doerfer definiert (Design + Backend!)
- [x] Duell-System designed (request/accept/decline, 30s Fenster)
- [x] Ranger-PvP Ausnahme implementiert (Rang 25+ = ueberfallbar, aktiver Transport noetig)
- [x] Straftat-System bei Ranger-Ueberfall (5000G Kopfgeld, -50 Ruf, Stadtverbot)
- [x] **backend/najika_safezone_system.py erstellt** (ZoneType, SafeZoneSystem, alle Tests OK!)
- [x] Disconnect-Handling designed (Safe Zone = sofort | Gefahr = 30s Grace Period)
- [x] Permadeath-Konsequenzen definiert (WEG: Char/Skills | BLEIBT: Slime-KI, Achievements)
- -> `NEUE_GAMEPLAY_IDEEN_2026-02-21.md`
- -> `backend/najika_safezone_system.py`

### FF7 Mini-Staedte Weltkarte (NEU 2026-02-21)
- [ ] Spieler-Siedlungen als Mini-Modelle auf Weltkarte
- [ ] Seamless Transition beim Betreten
- [ ] LOD-System fuer Mini -> Voll-Ansicht
- -> `NEUE_GAMEPLAY_IDEEN_2026-02-21.md`

### Softy-Modus (NEU 2026-02-21)
- [ ] Server-Logik: Account als "Softy" markieren bei Tod
- [ ] Lebensraum als Offline-Welt (Items behalten, kein Multiplayer)
- [ ] Solo-Events fuer Softy-Spieler
- [ ] Freunde in Lebensraum einladen (einzige Online-Funktion)
- -> `NEUE_GAMEPLAY_IDEEN_2026-02-21.md`

### Wissensdatenbank (Gebot 7)
- [ ] Bibliothek-Modul im Digivice konzipieren
- [ ] Backend: PostgreSQL + Elasticsearch Setup
- [ ] Frontend: Markdown-Wiki mit Suche
- [ ] In-Game Wissen: Lore-Buecher, Bestiary, Rezepte
- [ ] Real-World Info-Happen (Kraeuterkunde etc.)

### Multiplayer
- [x] Backend: multiplayer.py Router existiert
- [x] Frontend: multiplayer_manager.js eingebunden
- [x] WebSocket URL angepasst
- [ ] Multiplayer im Browser testen
- [ ] 8 Digivices gleichzeitig testen

### Housing & Farming
- [x] Backend komplett implementiert
- [x] API Endpoints vorhanden
- [ ] Frontend-UI testen und polishen

### Slime-Begleiter V3
- [x] V3 Design fertig (Formwandler statt Evolution)
- [ ] Frontend-UI fuer Formwechsel
- [ ] Monster-Form Loot-Tabellen erstellen

### NSFW / Kaetzchen-Modus
- [x] Model existiert (najika-nsfw-natural)
- [x] Remote-Zugriff konzipiert (Cloudflare + Owner-Token)
- [ ] Remote-Setup konfigurieren
- [ ] Biometric Auth einrichten

---

## P3 - NICE TO HAVE (Zukunft)

### UE5 Migration
- [x] UE5 5.7 installiert
- [x] Projektstruktur angelegt (mehrere UE5-Ordner)
- [x] UEFN als ungeeignet bewertet
- [ ] Python Copy&Paste Approach ausarbeiten
- [ ] Three.js -> UE5 Mapping umsetzen
- [ ] UE5 Prototyp mit Basic World erstellen

### Grafik-Qualitaet (Genshin/Diablo Immortal Level)
- [ ] Stylized Anime Look fuer Najika (Genshin-Style)
- [ ] PBR Textures (4K)
- [ ] Cloth Physics, Facial Animations
- [ ] Niagara Particles (VFX)
- [ ] Performance: 60 FPS @ 1080p PC, 30 FPS @ 720p Mobile

### Anti-Cheat
- [ ] Sync-System implementieren (Digivice <-> Game)
- [ ] Timestamp-Plausibilitaet
- [ ] Rate-Limiting

### Chaos-Events
- [x] 30 Events definiert
- [ ] Events in 3D-Szene integrieren (nicht nur Text-Popups!)
- [ ] Konsequenzen-System ausbauen

---

## OFFENE ENTSCHEIDUNGEN (KUJA MUSS ENTSCHEIDEN)

### 1. Level-System - ENTSCHIEDEN (2026-02-23)
**Entscheidung:** Fallout SPECIAL Style + Learning by Doing
- Anfang: Startwerte verteilen (geben nur minimale Richtung vor)
- Danach: Alles wie im echten Leben - Skills steigen durch Nutzung
- KEIN Level-Up gibt Stats! Nur durch Training/Equipment/Nutzung

### 2. Spieler-Character Model (+ Najika-Begleiterin)
**Status:** User kuemmert sich drum
**WICHTIG:** Spieler = man SELBST, Najika = KI-Begleiterin (= Slime)
- najika_rigged_final.fbx hat 0 Bones (nur static mesh)
- Kein Mixamo-Download gefunden
- User wird geriggtes Spieler-Model mit ~40 Animationen bereitstellen
- Fuer First Person: Braucht separate Haende/Arm-Assets
- Najika/Slime braucht eigenes Model + Animationen

### 3. main_fastapi.py - ENTSCHIEDEN (2026-02-23)
**Entscheidung:** FastAPI ist der aktive Server!
- main_fastapi.py = aktiver Server auf Port 8000
- najika_server.py → najika_server_legacy.py (archiviert)
- START_V3.bat nutzt jetzt uvicorn
- 4 deaktivierte Router reaktiviert (companion, combat_hands, mimik, stat_training)

### 4. Alte Dokumentation (300+ MDs)
**Entscheidung:** Behalten (2026-02-23) - Models brauchen das Wissen noch
- Archiv-MDs bleiben als Referenz
- Aktuelle Wahrheit: CLAUDE.md + KOMPLETT_UEBERSICHT + MASTER_TODO

---

## ERLEDIGTE MEILENSTEINE

### 2026-02-22 (Mega Combat Session)
- [x] 262 veraltete Docs archiviert (DOCS/archiv/)
- [x] COMBAT_SYSTEM_KOMPLETT_V3.md von Grund auf neu (~1400 Zeilen!)
  - For Honor Directional auf 4 Richtungen erweitert (OBEN/LINKS/RECHTS/UNTEN)
  - L2-Modifier = 8 Grundangriffe pro Waffe/Zauber
  - Spell-Diamond System (Hogwarts = Linke-Hand-Slot, 2-Layer Auswahl/Casting)
  - Jede Zauber-Spezialisierung hat eigene 4 Richtungs-Varianten
  - Faustkampf-System mit Air-Combo Paradebeispiel
  - Grappling/Wrestling (L1-L100, Wand-Absprung, Luft-Grab, Piledriver)
  - Bayonet/Sniper-als-Speer (Skill-Transfer Prinzip = gilt ueberall!)
  - Pistole Melee (3 Griffen, 0/5/35% Ausloese-Risiko)
  - Magische + Alchemistische Munition (je 7 Typen)
  - Environmental Combat (UE5 Chaos Physics, alles interaktiv)
  - Plasma-Waffen (ultra-legendaer)
  - Koerperteil-Targeting (NOT VATS, Level 1-100, Zeh-Schuss bei L100 😄)
  - Prothesen-System (Normal/Magisch/Alchemistisch, alle Koerperteile!)
  - 7 Uebergreifende Design-Prinzipien
- [x] backend/najika_safezone_system.py erstellt (alle Tests bestand!)
  - 9 Zonen-Typen, komplette Zone-DB (alle 8 Regionen + Staedte + Goetterfels + Dungeons)
  - PvP-Check, Duell-System, Ranger-Transport, Disconnect-Handling
  - Permadeath-Konsequenzen
- [x] MASTER_TODO.md aktualisiert

### 2026-02-21 (Neuer PC Setup)
- [x] Neues System eingerichtet (nach PC-Crash)
- [x] Venv + Packages installiert
- [x] Ollama Models erstellt
- [x] Chat gefixt (2 Bugs: Model-Name + Task-Detection)
- [x] START_V3.bat erstellt
- [x] CLAUDE.md komplett neu (war total falsch!)
- [x] KOMPLETT_UEBERSICHT erstellt
- [x] MASTER_TODO neu erstellt

### 2026-02-16/17 (Letzte grosse Session)
- [x] UnifiedCombat entfernt -> Real3DCombat only
- [x] 8 Gebote V3 geschrieben
- [x] 15 Frontend-Scripts eingebunden
- [x] Multiplayer integriert
- [x] Legacy-Code separiert (backend/legacy/)
- [x] 4 Router deaktiviert (in main_fastapi.py) -> 2026-02-23 reaktiviert!

### 2026-02-15 (Code Audit)
- [x] Kompletter Code-Audit durchgefuehrt
- [x] Arena Teleport Bug gefixt
- [x] Enemy Callback Issue gefixt
- [x] Gap Analysis erstellt

### 2026-02-12 (Personality & Chat)
- [x] Modelfile "11 Jahre" entfernt
- [x] Melissa-Persoenlichkeit gefixt
- [x] History Poisoning Fix
- [x] RAG Trigger reduziert
- [x] Personality Engine Psychologie Framework

### Frueher (Jan/Feb 2026)
- [x] Flask -> ThreadingHTTPServer Migration
- [x] ChromaDB Setup
- [x] 3D Scene (Three.js)
- [x] Slime System V3 Design
- [x] Housing & Farming Backend
- [x] 56+ API Endpoints implementiert
- [x] NajikaMind AGI Pipeline (9 Schritte)

---

### 2026-02-23 (Immersive Combat V4 Design)
- [x] Fake Edelstein-Regionsnamen in 13+ Dateien bereinigt (Backend + Docs)
- [x] Browser-Test V3 durchgefuehrt: 94.8% (201/212 passed)
- [x] Najika FBX Avatar-Integration versucht (0 Bones - static mesh only)
- [x] FBXLoader + fflate CDN in index.html eingebaut
- [x] Beruf+Magie Synergie in COMBAT_SYSTEM_KOMPLETT_V3.md ergaenzt
- [x] **Combat V4 Design erarbeitet und APPROVED:**
  - For Honor Directional OHNE UI-Pfeile (Animation Reading)
  - Natuerliche Schwierigkeits-Progression (Gegner-Qualitaet = Schwierigkeit)
  - 3 Kamera-Modi: First Person / Third Person / Orbit (jederzeit wechselbar)
  - Faustkampf = Kampf ohne Waffe (gleiche Richtungen)
  - KI-Monster die aufsteigen = kuerzere Wind-Ups
- [x] DOCS/plans/2026-02-23-immersive-combat-v4-design.md geschrieben
- [x] Alle Pflicht-Dateien aktualisiert (CLAUDE.md, KOMPLETT_UEBERSICHT, MASTER_TODO)

### 2026-02-23 (FastAPI Switch)
- [x] **FastAPI als aktiven Server aktiviert** (Entscheidung + Umsetzung)
  - config.py: HOST 0.0.0.0 -> 127.0.0.1, PORT 8001 -> 8000
  - START_V3.bat: najika_server.py -> uvicorn backend.main_fastapi:app
  - najika_server.py -> najika_server_legacy.py umbenannt
  - 4 Router reaktiviert (companion, combat_hands, mimik, stat_training)
  - CLAUDE.md + MASTER_TODO aktualisiert
- [x] Level-System entschieden: Fallout SPECIAL + Learning by Doing
- [x] Alte MDs entschieden: Behalten als Wissensquelle

**Naechste Session:** Combat V4 implementieren (Direction Resolver + 3 Kamera-Modi)
**Bei Aenderungen:** MASTER_TODO + CLAUDE.md + KOMPLETT_UEBERSICHT updaten!
