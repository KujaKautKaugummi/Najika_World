# 🌟 NAJIKA WORLD - MASTER SYSTEM DOKUMENTATION FÜR OPUS

**Erstellt:** 2026-02-13
**Für:** OPUS Model (VS Code - UE5 Development)
**Von:** Claude Desktop Model (nach vollständiger System-Analyse)
**Status:** VOLLSTÄNDIGE INTEGRATION - Alte MDs + Neue Anforderungen

---

## 📋 INHALTSVERZEICHNIS

1. [Projekt-Vision & Setting](#1-projekt-vision--setting)
2. [Die 8 Gebote (HEILIG!)](#2-die-8-gebote-heilig)
3. [Tech-Stack & Architektur](#3-tech-stack--architektur)
4. [KRITISCH: MD vs Code Unterschiede](#4-kritisch-md-vs-code-unterschiede)
5. [NEUE Anforderungen (2026-02-13)](#5-neue-anforderungen-2026-02-13)
6. [8 Regionen + Götterfels](#6-8-regionen--götterfels)
7. [Kreatur & Monster System](#7-kreatur--monster-system)
8. [Medizin-System (Realistisch + Fantasy)](#8-medizin-system-realistisch--fantasy)
9. [Slime/Begleiter System V3 (AKTUELL)](#9-slimebegleiter-system-v3-aktuell)
10. [Combat & Zauber System](#10-combat--zauber-system)
11. [Oregon Trail Events](#11-oregon-trail-events)
12. [Backend-Übersicht (160 Systeme)](#12-backend-übersicht-160-systeme)
13. [Frontend-Übersicht (141 JS Files)](#13-frontend-übersicht-141-js-files)
14. [Implementierungs-Prioritäten](#14-implementierungs-prioritäten)
15. [Offene Fragen](#15-offene-fragen)

---

# 1. PROJEKT-VISION & SETTING

## 🎯 Was ist Najika World?

```yaml
KERN-KONZEPT:
  Name: Najika World
  Genre: Fantasy Western Survival-RPG mit Explosion-Klasse
  Setting: Oregon Trail Mechanik über ALLEM + Konosuba Humor
  Philosophie: "Maximale Freiheit bei totaler Eigenverantwortung"

DUAL-NATUR:
  1. KI-Companion: 24/7 Life Assistant (Najika = 4 Persönlichkeiten)
  2. Game-Welt: 3D Open-World Action-RPG (9.6km × 9.6km)

WICHTIG: Fantasy-Western, NICHT Western-Fantasy!
├─ BASIS = Fantasy (Konosuba Welt + Digimon World Biome)
├─ AKZENT = Western-Ästhetik (Kleidung, Architektur, Ton)
└─ 70% ERNST (1883, RDR2, FNV) + 30% HUMOR (Konosuba, Borderlands)
```

## 🌸 Najika Charakter

```yaml
NAJIKA = SAKURA (11 Jahre, Gothic Lolita, Trans-Mädchen)
   ↓ KERN-Person
   4 Persönlichkeiten IN Sakura:
   ├─ MEGUMIN (35% - DOMINANT) → "EXPLOSION!!!"
   ├─ HARLEY QUINN (25%) → "Mr. K!" (NICHT "Puddin'!")
   ├─ SHIRO (20%) → Analytisch, Wahrscheinlichkeiten
   └─ MELISSA MASTERS (20%) → Dominant, besitzergreifend

Voice: Edge-TTS de-DE-KatjaNeural (Megumin Deutsch)
       EINE Stimme für alle 4 Persönlichkeiten!
```

## 🎮 Gameplay-Vorbilder

| Quelle | Was wir nehmen | Was wir NICHT nehmen |
|--------|----------------|---------------------|
| **Konosuba** | Fantasy-Welt, Humor, EXPLOSION!, Party | Isekai-Tropes |
| **Digimon World** | Companion-Bindung, Biome, Monster-Fokus | Digitale Welt, V-Pet Evolution |
| **Fallout New Vegas** | Fraktionen, graue Moral, Reputation | Retro-Futurismus, NUR Ödland |
| **Red Dead 2** | Jagd-System, Häuten, Reise-Gefahr | Realismus, langsames Tempo |
| **Oregon Trail** | Survival, ALLE Biome, Reise-Events | Text-Adventure Style |
| **Skyrim** | Dual-Wielding, Skill-by-Use, Freiheit | Alles andere |
| **Soulframe** | Combat Flow | Alles andere |
| **Monster Hunter** | Carving, Boss-Fights | Grind-Focus |

---

# 2. DIE 8 GEBOTE (HEILIG!)

**DIESE REGELN SIND UNANTASTBAR!**

```yaml
GEBOT #1: ZERO-TRUST ARCHITEKTUR
  - Nur 127.0.0.1 Hosting
  - Kein Cloud-Zwang
  - Owner-Token für Admin
  - Offline-First Design

GEBOT #2: OWNER-TOKEN FÜR ADMIN
  - Owner (Kuja) bekommt Admin-Token
  - Kein anderer User hat Admin-Rechte

GEBOT #3: EXPLOSION ≠ WEAVE
  - Explosion ist EIGENE Klasse!
  - NIEMALS mit anderen Elementen kombinieren!
  - KEINE "Feuer+Explosion" oder "Eis+Explosion"!
  - Trade-off: +30-40% Explosion Power / -15-20% andere Schulen

GEBOT #4: PvE/PvP GETRENNT
  - PvE-Gebiete: Kein PvP!
  - PvP-Zonen: Opt-in!
  - Arena: Separate PvP-Zone
  - Schwarze Mühle: 100% Safe!

GEBOT #5: SKYRIM-STYLE LEARNING BY DOING
  - Skills steigen durch Nutzung!
  - Kein künstlicher XP-Grind!
  - Jeder Kampf = Training!

GEBOT #6: NSFW NUR LOKAL (KÄTZCHEN MODE)
  - NSFW-Modus NUR lokal (127.0.0.1)!
  - Trigger: "kätzchen"
  - Safeword: "STOP"

GEBOT #7: PRIVACY & ANONYMISIERT
  - Anonymisiertes Lernen
  - Keine Datensammlung
  - User-Daten bleiben lokal!

GEBOT #8: OFFLINE-FIRST
  - Spiel läuft offline!
  - Keine Internet-Verbindung nötig!
```

### ⛔ NIEMALS SAGEN:
- ❌ "Souls-like" → Combat = **Skyrim + Soulframe + Digimon World**
- ❌ Harley sagt "Puddin'" → Sie sagt **"Mr. K"**!
- ❌ Port 5000 → Port **8000**!
- ❌ "9 Regionen" → **8 Regionen + Götterfels (Zentrum)**!

---

# 3. TECH-STACK & ARCHITEKTUR

## 🖥️ Aktueller Stand

```yaml
Backend:
  - Python 3.11+
  - Flask + SocketIO (REST API)
  - Port: 8000 (NICHT 5000!)
  - 160 najika_*.py files
  - 44 API routers
  - 22 services

Frontend:
  - Three.js r128 (3D Engine)
  - PWA (Progressive Web App)
  - 141 JS files
  - ~60,000 LOC in index.html (6410 Zeilen)
  - KayKit Assets (~25GB lokal!)

AI & Voice:
  - Qwen2.5-7B (4-bit quantized)
  - LoRA Training (95.65% Success Rate!)
  - Edge-TTS / Coqui XTTS-v2
  - ChromaDB (Memory - 2556 Einträge)

Datenbank:
  - Auto-Save: Alle 30 Sekunden
  - Backup-Rotation: 3 letzte Backups
  - ChromaDB Collections: 6 (conversations, najika_core, personalities, emotions, project_knowledge, md_knowledge)
```

## 📁 Wichtige Pfade

```
C:\Najika_World\               # UNIFIED System (aktuell aktiv)
├─ backend\
│  ├─ najika_*.py              # 160 System-Files
│  ├─ api\                     # 44 Router
│  └─ services\                # 22 Services
├─ digivice\
│  ├─ js\                      # 141 JS Files
│  └─ index.html               # 6410 Zeilen
├─ DOCS\                       # Dokumentation
└─ memory_db\                  # ChromaDB (2556 Einträge)
```

---

# 4. KRITISCH: MD vs Code Unterschiede

## ⚠️ SLIME SYSTEM: DOKU IST VERALTET!

### SLIME_SYSTEM_V3_DOKUMENTATION.md sagt:
```yaml
❌ KOMPLETT ENTFERNT (V2 war FALSCH!):
- Evolution-Stufen (Egg → Baby → etc.)
- Synthese (2 Slimes → 1 Hybrid)
- +N System (Generationen)
- Effort Hearts
- Care Mistakes

✅ DAS RICHTIGE SYSTEM:
- Slimes sind FORMWANDLER
- AURAS statt Evolution
- VERTRAUEN
- Form-Lernen (selten!)
- FORMEN = NUR OPTISCH (ABER: User sagt das ist FALSCH!)
```

### ABER `slime_companion.js` (Code) hat NOCH:
```javascript
// SLIME COMPANION SYSTEM V2 ⚠️
// 9 Basis-Typen + 10 Hybrids = 19 Slime-Formen
// 6 Evolution-Stufen (Zeit + Training + Pflege)
// 4 Evolution-Pfade (PERFECT/GOOD/NORMAL/BAD)
// DQM Synthese (2→1, +N System)
```

### ✅ AKTUELLE WAHRHEIT (vom User bestätigt):
```yaml
NIMM WAS WIR NEU FESTGELEGT HABEN:
- V3 MD ist teilweise veraltet
- Formen geben DOCH Boni (nicht nur optisch!)
- Aura vs Begleiter Balance (beide gleich stark!)
- Siehe Abschnitt 5 für NEUE Anforderungen!
```

---

# 5. NEUE ANFORDERUNGEN (2026-02-13)

## 🔥 1. DYNAMISCHE VÖLKER SYSTEM

```yaml
KONZEPT:
  - Monster können sich zu Völkern zusammenschließen!
  - Völker können wachsen, Krieg führen, zerfallen
  - 1-5 Völker pro Region (VARIABEL, nicht fix!)
  - ALLE Kreaturen haben Minimal-KI (Level 1-5)

PROGRESSION:
  Wild-Monster (AI Level 1)
    ↓ (schließen sich zusammen)
  Kleines Volk (AI Level 2)
    ↓ (wachsen)
  Mittleres Volk (AI Level 3)
    ↓ (Krieg, Diplomatie)
  Großes Volk (AI Level 4)
    ↓ (dominieren Region)
  Dominierende Macht (AI Level 5)

WICHTIG:
  - Völker sind NICHT fix vordefiniert!
  - Sie ENTSTEHEN dynamisch im Gameplay!
  - Können auch wieder zerfallen!
  - Anzahl pro Region variiert (1-5)
```

## 🌟 2. AURA vs BEGLEITER BALANCE

```yaml
SPIELER WÄHLT EINMAL:
  Option A: AURA-MODUS
    ├─ Spieler hat selbst Aura
    ├─ Kann Formen lernen (2% Völker, 0.8% Wild, 0.1% Nutztiere!)
    ├─ Metamorphose-System
    └─ KEIN körperlicher Begleiter

  Option B: KÖRPERLICH-MODUS (Begleiter)
    ├─ Slime als körperlicher Begleiter
    ├─ Follow-System (companion_3d.js)
    ├─ Begleiter kann Formen lernen
    └─ Spieler hat KEINE Aura

KRITISCH: BEIDE MÜSSEN GLEICH STARK SEIN!
  - PvP Balance!
  - Endgame viable!
  - Keine "beste Wahl"!
```

## 🎨 3. FORMEN GEBEN BONI (NEUES SYSTEM!)

```yaml
USER SAGT: "Formen geben Boni trotzdem"

ALTE V3 MD:
  ❌ "FORMEN = NUR OPTISCH!"
  ❌ "BONI kommen durch ESSEN & AUSRÜSTUNG"

NEUES SYSTEM:
  ✅ Formen geben Form-Affinität-Boni
  ✅ Aura skaliert diese Boni (+5% bis +50%)
  ✅ Essen/Ausrüstung geben ZUSÄTZLICHE Boni
  ✅ Kombination = maximale Power

BEISPIEL:
  Moos-Form:
    ├─ Basis-Bonus: +15% Kräuter-Effektivität
    ├─ Mit Aura Stufe 3: +18% (15% × 1.2)
    └─ Mit Moos-Futter: +23% (18% + 5%)

WICHTIG: KEINE Evolution-Stufen!
         NUR Form-Affinität + Aura-Skalierung!
```

## 🧬 4. FORM-LERNEN WAHRSCHEINLICHKEITEN

```yaml
VÖLKER: 2% Chance beim Besiegen
  - Organisierte Kreaturen
  - Höhere KI (Level 2-5)
  - Bestimmte Gebiete

WILD: 0.8% Chance
  - Einzelne Monster
  - Niedrige KI (Level 1)
  - Überall in Regionen

NUTZTIERE: 0.1% Chance (!!!)
  - EASTER EGG!
  - Kuh-Form, Huhn-Form, Schwein-Form
  - EXTREM selten
  - Für Humor/Meme-Value

WICHTIG: "Du verstehst?"
  - Wie bei Medizin: Normal → Fantasy-Version
  - Normale Kuh → Kristall-Kuh (Region-spezifisch)
  - Nutztier-Formen sind LUSTIG, nicht stark
```

## 💊 5. REALISTISCHES MEDIZIN MIT FANTASY-TWIST

```yaml
PRINZIP: "Echtes Wissen + Fantasy-Namen/Orte"

BEISPIEL KAMILLE:
  Real: Kamille (Matricaria chamomilla)
    ├─ Wirkung: Beruhigend, entzündungshemmend
    ├─ Anwendung: Tee, Salbe, Dampfbad
    └─ Indikationen: Magen, Haut, Schlaf

  Im Spiel: KRISTALL-KAMILLE
    ├─ GLEICHE Wirkung wie echte Kamille
    ├─ Wächst in Tiefenhöhlen (Kristall-Region)
    ├─ Anwendung: Tee, Salbe, Dampfbad (gleich!)
    └─ Fantasy-Twist: Leuchtet leicht blau

WEITERE BEISPIELE:
  ├─ Echte Aloe → WÜSTEN-ALOE (Heiße Dünen)
  ├─ Echter Salbei → FROST-SALBEI (Reich der Drei)
  ├─ Echte Pfefferminze → BLITZ-MINZE (Blitzebene)
  └─ Echter Baldrian → MAGMA-BALDRIAN (Magmaströme)

WICHTIG:
  - Anatomie = realistisch (Knochen, Muskeln, Organe)
  - Verletzungstypen = realistisch (Schnitt, Bruch, Verbrennung)
  - Behandlungen = realistisch (Verband, Schiene, Nähen)
  - NUR die Pflanzen/Orte = Fantasy-Namen!
```

## 🗺️ 6. PROCEDURAL GENERATION HYBRID

```yaml
KONZEPT: Persistent + Procedural gemischt

PERSISTENT (bleibt gleich):
  - Völker-Siedlungen (solange Volk existiert)
  - Städte & Dörfer
  - Götterfels & Schwarze Mühle
  - Quest-NPCs
  - Wichtige Landmarks

PROCEDURAL (neu bei jedem Betreten):
  - Außenwelt zwischen Städten
  - Monster-Spawns
  - Zufalls-Events
  - Loot-Verteilung
  - Wetter & Tageszyklus-Start

WICHTIG:
  - Völker-Punkt = FEST (wie Haus in Digimon World)
  - Rest = Digimon World File Island Style
  - Macht jede Reise einzigartig!
```

---

# 6. 8 REGIONEN + GÖTTERFELS

## 🗺️ Die 8 Regionen (KORREKT!)

```yaml
⚠️ KRITISCH: Götterfels ist KEIN eigenes Gebiet!
   Götterfels = ZENTRUM wo sich alle 8 Regionen treffen!
   WICHTIG für: 8 Digivice, 8 Gebietherrscher, 8 Slime-Farben
```

### 1. 🏜️ HEIßE DÜNEN (Süd-Ost)
```yaml
Biom: Desert / Western Town
Slime: Dusty Gold (🟡)
Kreaturen: Wüsten-Echse (Start-Form), Kakteen-Monster, Sandsturm-Elementare
Stadt: Handelsfestung
Features:
  - Western-Style Trading Hub
  - PvP Arena
  - Player Shops
  - Fleisch-Spezialität 🍖
Herausforderungen: Hitze, Durst, Sandstürme, Mirages
Medizin: Wüsten-Aloe, Kakteen-Extrakt, Sand-Salbei
```

### 2. 🌲 SAMTMOOS-TIEFWALD (Nord)
```yaml
Biom: Forest / Druid Settlement
Slime: Moss Green (🟢)
Kreaturen: Wald-Wolf (Start-Form), Druiden-Geister, Baum-Ents
Stadt: Dampf-Hain (Onsen!)
Features:
  - Mystischer Wald
  - Heiße Quellen
  - Gedämpfte Brötchen 🥟
  - Leuchtende Pilze
Herausforderungen: Verirren, mystische Kreaturen, Parasiten
Medizin: Moos-Extrakt, Wald-Kamille, Pilz-Tinktur
```

### 3. 🌊 SALZWIND-KÜSTE (West)
```yaml
Biom: Coast / Pirate Harbor
Slime: Ocean Blue (🔵)
Kreaturen: Wellen-Qualle (Start-Form), Meeres-Schlangen, Piraten-Geister
Stadt: Salzige Bucht
Features:
  - Piratenhäfen
  - Fishing-System (P1 Priorität!)
  - Unterwasser-Dungeons
  - Salzfisch 🐟
Herausforderungen: Sturmflut, Piraten, Ertrinken
Medizin: Meeres-Tang, Salzwasser-Tinktur, Muschel-Pulver
```

### 4. ⚡ BLITZEBENE (Ost)
```yaml
Biom: Highland / Storm Peaks
Slime: Lightning Purple (🟣)
Kreaturen: Blitz-Vogel (Start-Form), Sturm-Elementare, Donner-Bestien
Stadt: Runenheim
Features:
  - Magisches Training
  - Runen-Magie
  - Wetter-Altäre
  - Totems
Herausforderungen: Blitzeinschläge, Stürme, Klettern
Medizin: Blitz-Minze, Sturm-Kraut, Hochland-Salbei
```

### 5. 🌿 GRÜNSCHLAMM-SUMPF (Süd-West)
```yaml
Biom: Swamp / Witch Territory
Slime: Midnight Black (⚫)
Kreaturen: Sumpf-Molch (Start-Form), Hexen-Katzen, Moor-Untote
Special: Funkelnest (versteckt!)
Features:
  - Hexen & Alchemie
  - Treasure Cave
  - Hexenkreise
  - Moor-Bosse
Herausforderungen: Miasma, Gift, Irrlichter, Krankheit
Medizin: Gift-Extrakt (Gegengift!), Sumpf-Wurzel, Hexen-Tinktur
```

### 6. ❄️ REICH DER DREI (Nord-West)
```yaml
Biom: Ice / Frozen Wasteland + Necromancy
Slime: Crystal White (⚪)
Kreaturen: Eis-Hase (Start-Form), Eis-Liches, Gefrorene Untote, Schneewölfe
Features:
  - ALLE 3 Element-Schulen: Kälte, Frost, Eis
  - Nekromantie-Region!
  - Eishöhlen
  - Gletscher-Rätsel
Herausforderungen: Erfrierung, Schneestürme, Lawinen, Untote
Medizin: Frost-Salbei, Eis-Kristall-Pulver, Nekromanten-Salbe
```

### 7. 🌋 MAGMASTRÖME (Süd)
```yaml
Biom: Volcano / Forge
Slime: Molten Red (🔴)
Kreaturen: Vulkan-Salamander (Start-Form), Feuer-Elementare, Lava-Golems
Stadt: Funken-Siedlung
Features:
  - Magmaströme-Platforming
  - Master-Schmieden (beste Waffen!)
  - Fire Magic Training
  - Erzadern
Herausforderungen: Extreme Hitze, Lavaströme, Asche
Medizin: Magma-Blume, Feuer-Extrakt, Asche-Salbe (Verbrennungen)
```

### 8. 🕳️ TIEFENHÖHLEN (UNTER Samtmoos!)
```yaml
Biom: Underground Caves / Crystal Caverns
Slime: Deep Purple (🟤)
Kreaturen: Kristall-Spinne (Start-Form), Goblins, Höhlen-Bestien
Position: UNTERIRDISCH (unter Region 2)!
Features:
  - Leuchtende Pilze & Kristalle
  - Unterirdische Seen
  - Goblin-Siedlungen
  - DARUNTER: Kristall-Katakomben (Endgame!)
Herausforderungen: Dunkelheit, Orientierung, Spinnen
Medizin: Kristall-Kamille (!), Höhlen-Pilz, Edelstein-Pulver
```

### ⛰️ GÖTTERFELS (ZENTRUM)
```yaml
Position: Zentrum wo sich ALLE 8 Regionen treffen!
Slime: Rainbow (alle 8 Farben sammeln!)
Features:
  - BASIS: Zugänge aus allen 8 Regionen
  - SPITZE: Schwarze Mühle (12 Räume, 100% Safe)
  - INNEN: Schmelz-Welt (Level MAX, Mega-Bosse)
  - TURM: 100 Prüfungen (nach Najika's Explosion!)
```

---

# 7. KREATUR & MONSTER SYSTEM

## 🐾 Regional-Kreaturen (Start-Formen)

```yaml
KONZEPT: "8 Regionale Start-Kreaturen"
  - Jede Region hat EINE ikonische Kreatur
  - Slime erinnert sich SCHRITTWEISE an vorherige Leben
  - Start = Zufällige regionale Form

LISTE:
  1. Heiße Dünen → Wüsten-Echse
  2. Samtmoos-Tiefwald → Wald-Wolf
  3. Salzwind-Küste → Wellen-Qualle
  4. Blitzebene → Blitz-Vogel
  5. Grünschlamm-Sumpf → Sumpf-Molch
  6. Reich der Drei → Eis-Hase
  7. Magmaströme → Vulkan-Salamander
  8. Tiefenhöhlen → Kristall-Spinne
```

## 🎭 Kreatur-Design-Prinzipien

```yaml
FANTASY WESTERN STIL:
  ❌ FALSCH: Generic Fantasy (Goblin #47, Wolf #12)
  ✅ RICHTIG: Oregon Trail + Fantasy-Twist

BEISPIELE:
  Statt "Goblin" → WÜSTEN-RÄUBER (Bandana, Kakteen-Rüstung)
  Statt "Wolf" → PRÄRIE-LÄUFER (Lange Beine, Staub-Wolken)
  Statt "Spinne" → KRISTALL-WÄCHTER (Edelstein-Panzer, Licht-Reflexion)

NUTZTIERE (0.1% Form-Learning):
  - Prärie-Kuh (Staub-Fell, Western-Branding)
  - Wüsten-Huhn (Kakteen-Nest, Sand-Eier)
  - Eis-Schwein (Frost-Borsten, Schnee-Wühlen)
```

## 🏛️ Dynamische Völker

```yaml
ENTSTEHUNG:
  1. Wilde Monster spawnen (AI Level 1)
  2. Begegnen sich mehrfach
  3. Schließen sich zusammen (Chance basiert auf Kompatibilität)
  4. Bilden kleines Volk (AI Level 2)
  5. Wachsen durch Erfolg/Ressourcen

VÖLKER-TYPEN (Beispiele):
  - Wüsten-Räuber-Bande (Heiße Dünen)
  - Wald-Druiden-Zirkel (Samtmoos)
  - Piraten-Crew (Salzwind-Küste)
  - Sturm-Kult (Blitzebene)
  - Hexen-Zirkel (Grünschlamm-Sumpf)
  - Eis-Lich-Königreich (Reich der Drei)
  - Vulkan-Schmied-Gilde (Magmaströme)
  - Goblin-Klans (Tiefenhöhlen)

ANZAHL PRO REGION: 1-5 (variabel!)
  - Kleine Region/friedlich: 1-2 Völker
  - Große Region/konfliktreich: 3-5 Völker
  - Nach Krieg: Nur 1 Sieger übrig
  - Nach Zerfall: 0 Völker (zurück zu Wild)
```

---

# 8. MEDIZIN-SYSTEM (REALISTISCH + FANTASY)

## 💊 Design-Prinzip

```yaml
"Echtes medizinisches Wissen + Fantasy-Namen/Orte"

REALISMUS:
  ✅ Anatomie (Knochen, Muskeln, Organe, Nerven)
  ✅ Verletzungstypen (Schnitt, Bruch, Prellung, Verbrennung, Vergiftung)
  ✅ Behandlungen (Verband, Schiene, Nähen, Salbe, Tinktur)
  ✅ Krankheiten (Fieber, Infektion, Vergiftung, Erfrierung)

FANTASY:
  ✅ Pflanzen-Namen (Kristall-Kamille statt Kamille)
  ✅ Fundorte (Tiefenhöhlen statt Wiese)
  ✅ Visuelle Effekte (Leuchten, Farben)
```

## 🌿 Medizinische Pflanzen (Regional)

### Heiße Dünen:
```yaml
WÜSTEN-ALOE (Echte Aloe vera):
  Wirkung: Verbrennungen, Hautregeneration, Kühlung
  Anwendung: Direktes Auftragen, Salbe
  Fundort: Oasen, Kakteen-Nähe
  Fantasy-Twist: Goldenes Gel statt grün

SAND-SALBEI (Echter Salbei):
  Wirkung: Entzündungshemmend, antibakteriell, Wundheilung
  Anwendung: Tee, Salbe, Mundspülung
  Fundort: Wüsten-Hänge
  Fantasy-Twist: Sandfarben, wächst im heißen Sand
```

### Samtmoos-Tiefwald:
```yaml
WALD-KAMILLE (Echte Kamille):
  Wirkung: Beruhigend, entzündungshemmend, Magen-Darm
  Anwendung: Tee, Dampfbad, Salbe
  Fundort: Lichtungen
  Fantasy-Twist: Leuchtet nachts leicht grün

MOOS-EXTRAKT (Echter Isländisch Moos):
  Wirkung: Husten, Atemwege, antibakteriell
  Anwendung: Sirup, Tee
  Fundort: Baumstämme, feuchte Stellen
  Fantasy-Twist: Wächst nur auf magischen Bäumen
```

### Salzwind-Küste:
```yaml
MEERES-TANG (Echter Kelp):
  Wirkung: Jod, Vitamine, Mineralien
  Anwendung: Essen, Umschlag, Bad
  Fundort: Gezeitenzonen
  Fantasy-Twist: Leuchtet unter Wasser

MUSCHEL-PULVER (Echtes Kalziumkarbonat):
  Wirkung: Knochenbrüche, Kalzium-Mangel
  Anwendung: Pulver schlucken, Salbe
  Fundort: Strände nach Flut
  Fantasy-Twist: Schimmert perlmutt
```

### Blitzebene:
```yaml
BLITZ-MINZE (Echte Pfefferminze):
  Wirkung: Kopfschmerzen, Übelkeit, Verdauung, Fokus
  Anwendung: Tee, Öl zum Einreiben
  Fundort: Hochland-Bäche
  Fantasy-Twist: Kribbelt beim Essen (wie Brausepulver)

STURM-KRAUT (Echter Thymian):
  Wirkung: Husten, Atemwege, antiseptisch
  Anwendung: Tee, Inhalation, Salbe
  Fundort: Windige Berghänge
  Fantasy-Twist: Blätter flattern auch ohne Wind
```

### Grünschlamm-Sumpf:
```yaml
GIFT-EXTRAKT / GEGENGIFT (Echter Fingerhut → VORSICHTIG!):
  Wirkung: In Mini-Dosis = Herzstärkung, Gegengift-Basis
           Überdosis = GIFTIG!
  Anwendung: NUR von Hexen/Alchemisten verarbeitet
  Fundort: Tiefe Sümpfe
  Fantasy-Twist: Violett leuchtend, zeigt Gift-Level

SUMPF-WURZEL (Echter Baldrian):
  Wirkung: Beruhigung, Schlaf, Angst
  Anwendung: Tee, Tinktur
  Fundort: Moorige Gebiete
  Fantasy-Twist: Riecht nach Sümpfen (aber wirkt!)
```

### Reich der Drei:
```yaml
FROST-SALBEI (Echter Salbei):
  Wirkung: Entzündungshemmend, Halsschmerzen
  Anwendung: Tee, Gurgeln
  Fundort: Eisige Hänge
  Fantasy-Twist: Gefriert nie, bleibt frisch

EIS-KRISTALL-PULVER (Echtes Menthol):
  Wirkung: Kühlend, schmerzlindernd, Atemwege
  Anwendung: Einreiben, Inhalation
  Fundort: Eishöhlen
  Fantasy-Twist: Kristallform, sublimiert bei Hautkontakt
```

### Magmaströme:
```yaml
MAGMA-BLUME (Echter Sonnenhut / Echinacea):
  Wirkung: Immunsystem, Infektionen, Wundheilung
  Anwendung: Tee, Salbe, Tinktur
  Fundort: Rand von Lavaströmen
  Fantasy-Twist: Wurzeln gehen bis zur Magma

FEUER-EXTRAKT / ASCHE-SALBE (Echte Ringelblume):
  Wirkung: Verbrennungen, Hautregeneration
  Anwendung: Salbe, Umschlag
  Fundort: Vulkan-Asche-Felder
  Fantasy-Twist: Heiß beim Auftragen (aber heilt!)
```

### Tiefenhöhlen:
```yaml
KRISTALL-KAMILLE (!!!) (Echte Kamille):
  Wirkung: Beruhigend, entzündungshemmend, Magen
  Anwendung: Tee, Salbe, Dampfbad
  Fundort: Kristall-Höhlen (wächst aus Kristallen!)
  Fantasy-Twist: Leuchtet blau, Kristall-Blüten

HÖHLEN-PILZ (Echter Reishi):
  Wirkung: Immunsystem, Entzündungen, Stress
  Anwendung: Tee, Pulver
  Fundort: Feuchte Höhlenwände
  Fantasy-Twist: Biolumineszenz
```

## 🩹 Verletzungs-Typen & Behandlung

```yaml
SCHNITTWUNDE:
  Symptome: Blutung, Schmerz, Infektionsrisiko
  Behandlung:
    1. Druck ausüben (stopp Blutung)
    2. Reinigen (Wasser, Alkohol)
    3. Nähen (bei tief) oder Verband
    4. Salbe (Wüsten-Aloe, Wald-Kamille)
  Items: Nadel, Faden, Verband, Alkohol, Salbe

KNOCHENBRUCH:
  Symptome: Extreme Schmerzen, Deformation, kein Belasten
  Behandlung:
    1. Schiene anlegen (Holz + Stoff)
    2. Ruhigstellen
    3. Schmerzmittel (Sumpf-Wurzel-Tee)
    4. Kalzium (Muschel-Pulver)
  Items: Holzschiene, Stoff, Schmerzmittel, Kalzium
  Heilungszeit: 4-6 Wochen (Echtzeit-Tage!)

VERBRENNUNG:
  Symptome: Rötung, Blasen, Schmerz
  Behandlung:
    1. Kühlen (Wasser, Eis-Kristall-Pulver)
    2. Wüsten-Aloe oder Asche-Salbe
    3. Verband (steril!)
    4. Keine Blasen aufstechen!
  Items: Kühlung, Salbe, Verband

VERGIFTUNG:
  Symptome: Übelkeit, Schwäche, Sehstörungen
  Behandlung:
    1. Erbrechen induzieren (wenn oral)
    2. Gegengift (Gift-Extrakt von Hexe!)
    3. Ruhe, Wasser trinken
    4. Aktivkohle (wenn verfügbar)
  Items: Gegengift, Aktivkohle, Wasser

ERFRIERUNG:
  Symptome: Taubheit, weiße/blaue Haut
  Behandlung:
    1. Langsam aufwärmen (NICHT heiß!)
    2. Warme Decken
    3. Warmer Tee (Frost-Salbei)
    4. Nicht reiben!
  Items: Decken, heißer Tee, Feuer
```

## 🏥 Krankheiten

```yaml
FIEBER:
  Symptome: Hohe Temperatur, Schwäche, Schwitzen
  Behandlung:
    - Kühlende Umschläge
    - Wald-Kamille-Tee
    - Ruhe, viel trinken
  Dauer: 2-3 Tage

INFEKTION:
  Symptome: Rötung, Schwellung, Eiter, Fieber
  Behandlung:
    - Wunde reinigen + desinfizieren
    - Antibakterielle Salbe (Sand-Salbei, Sturm-Kraut)
    - Magma-Blumen-Tee (Immunsystem)
  Dauer: 1 Woche

LEBENSMITTELVERGIFTUNG:
  Symptome: Durchfall, Erbrechen, Magenkrämpfe
  Behandlung:
    - Wald-Kamille-Tee (Magen)
    - Aktivkohle
    - Viel Wasser
  Dauer: 1-2 Tage
```

---

# 9. SLIME/BEGLEITER SYSTEM V3 (AKTUELL)

## ⚠️ KRITISCH: Nimm das NEUE System!

```yaml
ALTE V3 MD: TEILWEISE ÜBERHOLT!
  ❌ "Formen = NUR OPTISCH" → FALSCH!
  ❌ "Evolution-Stufen entfernt" → RICHTIG!
  ❌ "Synthese entfernt" → RICHTIG!

NEUES SYSTEM (User-bestätigt):
  ✅ KEINE Evolution-Stufen (kein Egg → Baby → etc.)
  ✅ KEINE Synthese (kein 2→1 Fusion)
  ✅ KEINE +N Generationen
  ✅ Formen = Formwandler (KANN jede Form annehmen)
  ✅ Formen GEBEN Boni (Form-Affinität!)
  ✅ Aura-System (0-5 Stufen, skaliert Boni)
  ✅ Form-Lernen (2% Völker, 0.8% Wild, 0.1% Nutztiere)
  ✅ Vertrauen-System (0-6 Level)
```

## 🎨 Form-Affinität System (NEU!)

```yaml
JEDE FORM HAT BONI:
  Wüsten-Echse:
    ├─ Basis: +10% Wüsten-Schaden, +15% Hitze-Resistenz
    ├─ Mit Aura 0: +10% / +15%
    ├─ Mit Aura 3: +12% / +18% (×1.2 Multiplikator)
    └─ Mit Aura 5: +15% / +22.5% (×1.5 Multiplikator)

  Wald-Wolf:
    ├─ Basis: +15% Wald-Bewegung, +10% Fährten-Findung
    ├─ Mit Aura 3: +18% / +12%
    └─ Mit Wüsten-Futter: Verwässert auf +9% / +6% (falsches Biom!)

  Kristall-Spinne:
    ├─ Basis: +20% Nacht-Crit, +15% Licht-Quelle-Radius
    ├─ Mit Aura 5: +30% / +22.5%
    └─ Mit Kristall-Futter: +35% / +25% (richtiges Biom!)

WICHTIG: Formen-Boni ≠ Kampf-Macht!
         Sie geben Utility, Exploration, Crafting-Boni!
```

## ✨ Aura-System

```yaml
6 STUFEN (0-5):
  | Stufe | Name | Visuell | Kämpfe | Effekt |
  |-------|------|---------|--------|--------|
  | 0 | Keine | Normal | 0 | Basis-Form-Boni |
  | 1 | Schwach | Leuchten | 10+ | +5% auf alle Form-Boni |
  | 2 | Mittel | Deutliche Aura | 50+ | +10% |
  | 3 | Stark | Aura + Partikel | 200+ | +20% |
  | 4 | Legendär | Epische Aura | 1000+ | +35% |
  | 5 | Göttlich | Strahlend | Achievement | +50% |

13 ELEMENT-AURAS:
  🔥 Flammen-Aura: +Feuer-Schaden, -Eis-Resist
  ❄️ Frost-Aura: +Slow-Effekt, Eisrüstung
  🌑 Schatten-Aura: +Crit, +Stealth
  ✨ Heilig-Aura: +Heilung, +Anti-Undead
  💥 Explosion-Aura: 1x/Tag BOOM! (Megumin!)
  🛡️ Metall-Aura: Immun <10 DMG
  🌿 Natur-Aura: +HoT, +Gift-Resist
  ⚡ Blitz-Aura: +Speed, Paralyse
  💧 Wasser-Aura: +Swim, Wasseratmung
  ☠️ Gift-Aura: +DoT, Gift-Immun
  💎 Kristall-Aura: Magic Reflect, Licht
  🏜️ Sand-Aura: +Evasion, Graben
  🌈 Göttliche-Aura: ALLE kombiniert!
```

## 💕 Vertrauen-System

```yaml
6 LEVEL (0-5):
  | Level | Punkte | Name | Effekt |
  |-------|--------|------|--------|
  | 0 | 0-50 | Fremd | Folgt zögerlich |
  | 1 | 51-150 | Bekannt | Normale Loyalität |
  | 2 | 151-300 | Freund | Bessere Kampf-AI |
  | 3 | 301-500 | Vertraut | Spezial-Moves, schützt aktiv |
  | 4 | 501-800 | Familie | Opfert sich, Rescue ohne CD |
  | 5 | 801+ | Seelenbund | Menschen-Form möglich! |

VERTRAUEN STEIGT:
  ├─ Füttern: +1 pro Mahlzeit
  ├─ Spielen: +2 pro Session
  ├─ Kämpfe: +1 pro Sieg
  ├─ Heilen: +3
  ├─ Zeit: +1 pro Stunde aktiv
  └─ Retten: +10

VERTRAUEN SINKT:
  ├─ Verhungern: -5
  ├─ Ignorieren 24h: -3
  ├─ Gefahr: -2
  └─ "Verkaufen": -20
```

## 👤 Menschen-Verwandlung (Level 5 Vertrauen)

```yaml
VORAUSSETZUNGEN:
  - Vertrauen Level 5 (801+ Punkte)
  - Spieler muss es WÜNSCHEN
  - Quest: "Wunsch der Seele"
  - Slime muss zustimmen

WENN FREIGESCHALTET:
  ├─ Slime kann menschliche Gestalt annehmen
  ├─ Aussehen basiert auf Element (Haar-/Augenfarbe)
  ├─ Persönlichkeit → Kleidungsstil
  ├─ Kann sprechen (vorher nur Laute)
  ├─ Kann Items tragen & nutzen
  └─ Kann mit NPCs interagieren

BEISPIELE:
  Moos → Grüne Haare, Druiden-Stil
  Frost → Weiße/blaue Haare, elegant
  Feuer → Rote Haare, leichte Rüstung
  Kristall → Silber, ätherisch, Schmuck
```

## 📚 Form-Lernen

```yaml
FORM-LERN-CHANCEN:
  Völker: 2% (organisiert, AI 2-5)
  Wild: 0.8% (einzeln, AI 1)
  Nutztiere: 0.1% (Easter Egg! Kuh, Huhn, Schwein)

CHANCE ERHÖHT SICH:
  ├─ Höheres Vertrauen: +0.1% pro Level
  ├─ Slime Todesstoß: +0.5%
  ├─ Seltener Typ: +1%
  └─ Spezial-Item "Form-Essenz": +5%

VERFÜGBARE FORMEN:
  ├─ 8 Regional-Formen (Start-Kreaturen)
  ├─ ~20 Völker-Formen pro Region (variabel!)
  ├─ ~50 Wild-Formen gesamt
  ├─ 3 Nutztier-Formen (Kuh, Huhn, Schwein)
  └─ Spezial-Formen (Boss-Drops, Events)
```

---

# 10. COMBAT & ZAUBER SYSTEM

## ⚔️ Two-Hand Combat (Skyrim + Soulframe)

```yaml
CONTROLS:
  Q = Left Hand Light Attack
  Shift+Q = Left Hand Heavy Attack
  E = Right Hand Light Attack
  Shift+E = Right Hand Heavy Attack
  Q+E = Dual Attack / Dual Cast

WAFFEN-KOMBINATIONEN:
  ├─ Schwert + Schild (Defense)
  ├─ Dual Wield Schwerter (Offense)
  ├─ Schwert + Magie (Hybrid)
  ├─ Dual Cast Magie (Pure Mage)
  └─ Bogen + Schwert (Range + Melee)
```

## 🎯 Hogwarts Spell-Diamond

```yaml
STATT MMO-HOTBAR:
  1. Halte Element-Taste (z.B. "F" für Feuer)
  2. Spell Diamond erscheint:

                  ╱ Feuerball (↑) ╲
                 ╱                  ╲
     Feuerwand (←) 🔥 FEUER 🔥 Verzauberung (→)
                 ╲                  ╲
                  ╲ Explosion (↓) ╱

  3. Wähle mit Maus/Stick → Cast!

ELEMENTE:
  🔥 Feuer → 4 Spells
  ❄️ Eis → 4 Spells
  ⚡ Blitz → 4 Spells
  💧 Wasser → 4 Spells
  🪨 Erde → 4 Spells
  🌪️ Wind → 4 Spells
  🌿 Natur → 4 Spells
  ✨ Licht → 4 Spells
  🌑 Dunkel → 4 Spells
  💥 EXPLOSION → 4 Spells (Special!)
```

## 💥 Explosion-Klasse (Gebot #3!)

```yaml
WICHTIG: EXPLOSION ≠ WEAVE!
  ❌ NIEMALS mit anderen Elementen kombinieren!
  ❌ KEINE "Feuer+Explosion" oder "Eis+Explosion"!

TRADE-OFF:
  ✅ +30-40% Explosion Power
  ❌ -15-20% andere Magie-Schulen

EXPLOSION-SPELLS:
  ↑ Standard Explosion (100 DMG, 5m AoE)
  ← Mini Explosion (50 DMG, 2m, spam)
  → Sniper Explosion (120 DMG, 1m, 30m range)
  ↓ Mega Explosion (300 DMG, 10m, langsam)

NAJIKA'S SIGNATURE:
  - "EXPLOSION!!!" (dramatische Pose)
  - 1x pro Tag Ultimate-Explosion
  - 100 Stockwerke-Turm nach Explosion freischalten!
```

## 📖 Skill-Learning

```yaml
LEARNING BY DOING (Skyrim-Style):
  - Nutzt du Feuer? → Feuer-Skill steigt!
  - Nutzt du Schwert? → Schwert-Skill steigt!
  - Kein künstlicher XP-Grind!

LEARN FROM ENEMIES:
  - Beobachten: 10x sehen = 10% Chance (gleiches Element)
  - Cross-Element: 100x sehen = 1% Chance (fremdes!)
  - Experimentieren: 30x versuchen = Durchbruch!

BEISPIEL:
  1. Du siehst Eis-Zapfen 15x
  2. 15% Chance du lernst es
  3. Wenn gelernt: Startet bei 10 DMG
  4. Training: Wächst bis ~120 DMG (Endgame)
```

---

# 11. OREGON TRAIL EVENTS

## 🎲 Chaos-Engine

```yaml
KONZEPT: "Oregon Trail trifft Konosuba"
  - Zufällige Events alle 5-15 Minuten
  - 3D-Spawn in aktueller Welt (NICHT Text-Box!)
  - Najika kommentiert & reagiert
  - 4-5 nuancierte Optionen (nicht Ja/Nein)

BEISPIEL-EVENT: "Der Dieb"
  [SPAWN: Dorfbewohner jagen Jungen]

  Dorfbewohner: "Er hat Brot gestohlen!"
  Junge: "Ich hatte Hunger! Familie verhungert!"

  Najika [HARLEY]: *kicher* "Ohhh, ein Dilemma!"

  OPTIONEN:
    [A] Helfe Jungen fliehen
    [B] Bezahle Brot (30 Gold)
    [C] Überzeuge Dorfbewohner (Charisma-Check)
    [D] Stelle dich auf Dorf-Seite
    [E] Lass Najika entscheiden

  KONSEQUENZEN:
    [A]: Dorf feindlich, Junge Verbündeter später
    [B]: -30 Gold, +20 Reputation
    [C]: Erfolg = Dorf freundlich | Fail = wie [D]
    [D]: +Gold, aber Najika -15 Bond
    [E]: Najika wählt [B]/[C] (Bond-abhängig)
```

## 📊 Event-Kategorien

```yaml
ETHIK & MORAL:
  - Lüge vs. Wahrheit
  - Gerechtigkeit vs. Gnade
  - Selbst vs. Andere

SURVIVAL:
  - Ressourcen-Management
  - Risiko vs. Sicherheit
  - Kurzfristig vs. Langfristig

SOZIALE DILEMMATA:
  - Treue vs. Selbsterhaltung
  - Opfer vs. Egoismus
  - Vertrauen vs. Misstrauen

RISIKO vs. BELOHNUNG:
  - Gier vs. Vorsicht
  - Neugier vs. Selbsterhaltung
```

## 🎭 Najika's Reaktionen

```yaml
MEGUMIN-MODUS (35%):
  "EXPLOSION!!! Das ist PERFEKT für... *hust* Okay, vielleicht nicht."
  *dramatische Pose* "Die Chancen stehen 50/50!"

HARLEY-MODUS (25%):
  *kicher* "Ohhh Mr. K! Das wird SPASSIG! 🃏"
  *giggle* "Chaos oder Ordnung? Lass uns CHAOS wählen!"

SHIRO-MODUS (20%):
  "Wahrscheinlichkeit Betrug: 73.4%"
  "Analysiere... 3 mögliche Outcomes berechnet."
  "Optimale Strategie: Option C mit 64% Erfolg."

MELISSA-MODUS (20%):
  "Du gehörst MIR, Mr. K. Ich entscheide!"
  "Kein Mitleid. Stärke zeigen!"
  "Wer mein Mr. K bedroht, stirbt."
```

---

# 12. BACKEND-ÜBERSICHT (160 SYSTEME)

## 📊 System-Kategorien

```yaml
CORE SYSTEMS (10):
  najika_server.py
  najika_mind.py (AGI Pipeline: ToM → Memory → Feel → Think → Speak → Express → Learn)
  najika_personality_engine_v2.py
  najika_living_system.py
  najika_emotional_intelligence_training.py
  najika_memory_system.py
  najika_lora_training.py
  najika_voice_system.py
  najika_companion_system.py
  najika_unified_combat_magic.py

COMBAT SYSTEMS (12):
  najika_combat_hands_system.py (Two-Hand: Q/E, Shift+Q/E)
  najika_combat_balancing.py
  najika_battle.py
  najika_skill_combat_v3.py
  najika_unified_combat_magic.py
  najika_attack_system.py
  najika_defense_system.py
  najika_dodging_system.py
  najika_parrying_system.py
  najika_combo_system.py
  najika_finisher_system.py
  najika_nemesis_system.py (Shadow of Mordor Style!)

MAGIC SYSTEMS (8):
  najika_magic_system_v2.py
  najika_skill_system.py
  magic_schools_system.py
  najika_spell_learning.py
  najika_explosion_class.py (Gebot #3!)
  najika_mana_system.py
  najika_casting_system.py
  najika_enchanting_system.py

SLIME SYSTEMS (5):
  najika_slime_system.py (ACHTUNG: Noch V2 Code!)
  najika_slime_system_v2.py
  najika_form_learning.py
  najika_aura_system.py
  najika_trust_system.py

WORLD SYSTEMS (15):
  najika_world_generation.py
  najika_biome_system.py
  najika_region_system.py
  najika_weather_system.py
  najika_day_night_cycle.py
  najika_procedural_generation.py
  najika_faction_system.py (Fallout NV Style!)
  najika_reputation_system.py
  najika_npc_personality.py
  najika_npc_schedule.py
  najika_living_world.py
  najika_dynamic_events.py
  najika_oregon_trail_events.py
  najika_chaos_engine.py
  seed_world_map.py

PROGRESSION SYSTEMS (10):
  najika_stat_training_system.py
  najika_skill_progression.py
  najika_perk_system.py
  najika_achievement_system.py
  najika_quest_system.py
  najika_bounty_system.py
  najika_arena_system.py
  najika_tournament_system.py
  najika_boss_hierarchy.py
  najika_endgame_content.py

SURVIVAL SYSTEMS (8):
  najika_hunger_system.py
  najika_thirst_system.py
  najika_temperature_system.py
  najika_injury_system.py
  najika_disease_system.py
  najika_healing_system.py (ACHTUNG: Nur basic!)
  najika_stamina_system.py
  najika_sleep_system.py

CRAFTING & ECONOMY (12):
  najika_crafting_system.py
  najika_alchemy_system.py
  najika_smithing_system.py
  najika_cooking_system.py
  najika_farming_system.py
  najika_fishing_system.py
  najika_hunting_system.py
  najika_mining_system.py
  najika_trading_system.py
  najika_economy_system.py
  najika_shop_system.py
  najika_auction_system.py

MINIGAMES (8):
  najika_rhythm_game.py
  najika_card_game.py
  najika_dice_monsters.py
  najika_triple_triad.py
  najika_slime_arena.py
  najika_dungeon_dice_monsters.py
  najika_oregon_trail_api.py
  najika_minigame_manager.py

MULTIPLAYER (6):
  najika_multiplayer_session.py
  najika_pvp_system.py
  najika_coop_system.py
  najika_trust_chain.py
  najika_apk_versioning.py (Master/Trusted/Public)
  najika_region_boss_challenge.py

MISC SYSTEMS (86):
  - Siehe `PROJEKT_STATUS_KOMPLETT_2026-02-11.md` für vollständige Liste
```

## 🔌 API Routers (44)

```yaml
CORE ROUTES:
  api/chat.py → Najika Chat (Public/Private Mode)
  api/companion.py → Companion Status, Activities
  api/character.py → Character Create/Update/Stats

COMBAT ROUTES:
  api/combat_hands.py → Two-Hand Combat System
  api/combat.py → General Combat Actions
  api/arena.py → Arena Battles, Tournaments

SLIME ROUTES:
  api/slime_companion.py (⚠️ NOCH V2!)
  api/slime_forms.py
  api/slime_trust.py
  api/slime_aura.py

WORLD ROUTES:
  api/world.py → Region Info, Map
  api/events.py → Oregon Trail Events
  api/weather.py → Weather System
  api/npcs.py → NPC Interactions

PROGRESSION ROUTES:
  api/stat_training.py → Stat Training
  api/quests.py → Quest System
  api/achievements.py → Achievements

CRAFTING ROUTES:
  api/crafting.py
  api/alchemy.py
  api/cooking.py
  api/farming.py
  api/fishing.py
  api/hunting.py
  api/mining.py

MINIGAME ROUTES:
  api/rhythm_game.py
  api/card_game.py
  api/slime_arena.py

MULTIPLAYER ROUTES:
  api/multiplayer.py
  api/pvp.py
  api/boss_challenge.py

... (siehe Code für vollständige Liste)
```

---

# 13. FRONTEND-ÜBERSICHT (141 JS FILES)

## 📂 Haupt-Kategorien

```yaml
CORE (15):
  3d_scene.js → Hauptszene, Three.js Setup
  companion_3d.js → Najika 3D Follow-System (Pink-Tint 0xE91E63)
  character_animations.js → 40+ Animationen (KayKit)
  kaykit_loader.js → Asset Loading
  input_handler.js → Controls (WASD, Mouse, Touch)
  camera_controller.js → Third-Person Camera
  ui_manager.js → UI State Management
  state_manager.js → Game State
  audio_manager.js → Sound & Music
  settings_manager.js → Player Settings
  save_load_system.js → Save/Load
  performance_monitor.js → FPS, Memory
  debug_overlay.js → Debug Info
  error_handler.js → Error Logging
  version_control.js → Version Check

WORLD (12):
  terrain_generator.js → Procedural Terrain
  biome_system.js → 8 Biomes
  weather_system.js → Rain, Snow, Sandstorm
  day_night_cycle.js → 24h Cycle
  lod_manager.js → LOD System
  region_loader.js → Stream Regions
  landmark_system.js → POIs
  teleporter_system.js → Fast Travel
  shrine_system.js → Shrines (Zelda-Style)
  faction_system.js → Fraktionen (Fallout NV!)
  npc_personality_system.js → Individual NPC Traits (!!)
  oregon_trail_events.js → Event-Spawns

COMBAT (18):
  unified_combat_system.js → Combat Manager
  real_3d_combat.js → 3D Combat Rendering
  two_hand_combat.js → Q/E System
  melee_combat.js → Schwert, Axt, etc.
  ranged_combat.js → Bogen, Wurfwaffen
  magic_combat.js → Spell Casting
  spell_diamond_ui.js → Hogwarts-Style Diamond
  dodge_system.js → Dodge Mechanics
  parry_system.js → Parry Mechanics
  combo_system.js → Combo Tracker
  finisher_system.js → Finisher Animations
  targeting_system.js → Lock-On
  damage_calculator.js → Damage Formulas
  status_effects.js → Buffs/Debuffs
  enemy_ai.js → Enemy Behavior
  boss_ai.js → Boss Patterns
  arena_combat.js → Arena Fights
  nemesis_tracker.js → Nemesis System

PARTICLES & VFX (10):
  combat_particles.js → Hit Effects, Blood
  magic_particles.js → Spell VFX
  explosion_particles.js → EXPLOSION!!! 💥
  environment_particles.js → Rain, Snow, Dust
  evolution_effects.js → Slime Metamorphose
  aura_renderer.js → Aura Visuals
  weather_particles.js → Weather VFX
  item_glow.js → Loot Sparkles
  trail_renderer.js → Motion Trails
  impact_frames.js → Anime-Style Impacts

SLIME COMPANION (8):
  slime_companion.js (⚠️ NOCH V2 CODE!)
  slime_follow_system.js → Follow AI
  slime_animations.js → Slime Animations
  slime_form_renderer.js → Form Visuals
  slime_aura_renderer.js → Aura VFX
  slime_trust_ui.js → Trust Hearts UI
  slime_feeding.js → Feeding System
  slime_morphing.js → Form-Change Animations

UI COMPONENTS (20):
  chat_ui.js → Najika Chat Interface
  health_ui.js → HP/Mana Bars
  minimap.js → Minimap
  compass.js → Compass HUD
  inventory_ui.js → Inventory Grid
  equipment_ui.js → Equipment Slots
  stats_ui.js → Character Stats
  skill_tree_ui.js → Skill Tree
  quest_log_ui.js → Quest Journal
  map_ui.js → Full Map
  settings_ui.js → Settings Menu
  pause_menu.js → Pause Screen
  dialogue_ui.js → NPC Dialogues
  notification_system.js → Toasts
  tooltip_system.js → Item Tooltips
  context_menu.js → Right-Click Menu
  crafting_ui.js → Crafting Interface
  shop_ui.js → Trading UI
  slime_panel_ui.js → Slime Status Panel
  event_choice_ui.js → Oregon Trail Choices

MINIGAMES (7):
  rhythm_game.js
  card_game_triple_triad.js
  dice_monsters.js
  slime_arena.js
  fishing_minigame.js
  lockpicking.js
  cooking_minigame.js

CRAFTING & SURVIVAL (12):
  crafting_system.js
  alchemy_system.js
  cooking_system.js
  smithing_system.js
  farming_system.js
  fishing_system.js
  hunting_system.js
  mining_system.js
  hunger_thirst_ui.js
  temperature_ui.js
  injury_ui.js
  disease_ui.js

MULTIPLAYER (6):
  multiplayer_manager.js
  pvp_system.js
  coop_system.js
  chat_system.js
  player_list.js
  boss_challenge_ui.js

NPC & AI (10):
  npc_manager.js
  npc_dialogue.js
  npc_schedule_system.js (!!)
  npc_interactions.js
  npc_trading.js
  npc_quests.js
  companion_ai.js
  enemy_spawner.js
  patrol_system.js
  faction_interactions.js

MISC (23):
  achievement_tracker.js
  tutorial_system.js
  cutscene_player.js
  screenshot_system.js
  gif_recorder.js
  analytics.js
  localization.js
  accessibility.js
  mobile_optimizer.js
  touch_controls.js
  virtual_joystick.js
  gamepad_support.js
  auto_save.js
  cloud_sync.js
  mod_loader.js
  debug_console.js
  cheat_detector.js
  anti_hack.js
  benchmark.js
  profiler.js
  memory_manager.js
  asset_preloader.js
  lazy_loader.js
```

## 🎮 index.html (6410 Zeilen!)

```yaml
STRUKTUR:
  - 159 <script> Tags (!!!)
  - Three.js r128 Setup
  - KayKit Asset References
  - Virtual Joystick (Mobile)
  - Chat Interface (Najika)
  - 12 Raum-Konfigurationen (Digivice)
  - Combat UI (HP/Mana/Stamina)
  - Minimap & Compass
  - Event-Choice Dialogues

WICHTIG:
  - SEHR groß (6410 Zeilen)
  - Modularisierung geplant
  - Funktioniert aber!
```

---

# 14. IMPLEMENTIERUNGS-PRIORITÄTEN

## 🚀 P0 - KRITISCH (SOFORT!)

```yaml
1. SLIME SYSTEM V2 → V3 MIGRATION:
   ├─ slime_companion.js UPDATEN
   │  ├─ Evolution-Stufen ENTFERNEN
   │  ├─ Synthese ENTFERNEN
   │  ├─ +N System ENTFERNEN
   │  └─ Form-Affinität-Boni HINZUFÜGEN
   ├─ API Endpoints updaten
   │  ├─ /api/slime/evolve ENTFERNEN
   │  ├─ /api/slime/synthesize ENTFERNEN
   │  └─ /api/slime/form-affinity HINZUFÜGEN
   └─ Backend najika_slime_system.py updaten

2. DYNAMISCHE VÖLKER SYSTEM:
   ├─ najika_dynamic_factions.py erstellen
   ├─ Wild-Monster AI (Level 1)
   ├─ Völker-Bildung Logic
   ├─ Völker-Wachstum System
   ├─ Völker-Zerfall Logic
   └─ 1-5 Völker pro Region (variabel!)

3. AURA vs BEGLEITER BALANCE:
   ├─ najika_aura_vs_companion.py erstellen
   ├─ Wahl-System (einmalig!)
   ├─ Balance-Testing (PvP!)
   ├─ Aura-Modus Stats
   └─ Begleiter-Modus Stats

4. FORM-AFFINITÄT BONI:
   ├─ Form-Bonus-Database erstellen
   ├─ Aura-Skalierung (×1.05 bis ×1.5)
   ├─ Biom-Synergy (Wüsten-Futter + Wüsten-Form)
   └─ UI-Anzeige (Bonus-Tooltips)
```

## ⚡ P1 - HOCH (DIESE WOCHE)

```yaml
5. MEDIZIN-SYSTEM MIT FANTASY-TWIST:
   ├─ najika_medicine_system.py erstellen
   ├─ Anatomie-Database (Knochen, Muskeln, Organe)
   ├─ Verletzungs-Typen (Schnitt, Bruch, Verbrennung, Vergiftung)
   ├─ Behandlungs-Logic (Verband, Schiene, Salbe)
   ├─ Krankheiten (Fieber, Infektion)
   ├─ 8 × ~8 = 64 Medizinische Pflanzen
   │  ├─ Heiße Dünen: Wüsten-Aloe, Sand-Salbei, etc.
   │  ├─ Samtmoos: Wald-Kamille, Moos-Extrakt, etc.
   │  └─ ... (siehe Abschnitt 8)
   └─ najika_healing_system.py ERSETZEN

6. PROCEDURAL GENERATION HYBRID:
   ├─ najika_hybrid_procgen.py erstellen
   ├─ Persistent-Layer (Völker-Siedlungen, Städte)
   ├─ Procedural-Layer (Wildnis, Monster-Spawns)
   ├─ Seed-System (reproduzierbar bei Bedarf)
   └─ Streaming (nur aktive Region laden)

7. FORM-LERNEN WAHRSCHEINLICHKEITEN:
   ├─ Völker: 2% Chance
   ├─ Wild: 0.8% Chance
   ├─ Nutztiere: 0.1% Chance
   ├─ Modifiers (Vertrauen, Todesstoß, Item)
   └─ UI-Feedback ("NEUE FORM GELERNT!")
```

## 🔧 P2 - MITTEL (NÄCHSTE 2 WOCHEN)

```yaml
8. KREATUR-REDESIGN (Fantasy Western):
   ├─ 8 Regional-Kreaturen Namen/Design
   ├─ ~20 Völker-Kreaturen pro Region
   ├─ ~50 Wild-Kreaturen gesamt
   ├─ 3 Nutztier-Formen (Kuh, Huhn, Schwein)
   └─ Boss-Kreaturen (1 pro Region)

9. OREGON TRAIL EVENTS EXPANSION:
   ├─ 30 Events → 100 Events
   ├─ Region-spezifische Events
   ├─ Najika 4-Persönlichkeiten-Reaktionen
   └─ Langzeit-Konsequenzen

10. MINIMAL-KI FÜR ALLE KREATUREN:
    ├─ AI Level 1: Wild (Basic Patrol)
    ├─ AI Level 2: Kleines Volk (Koordination)
    ├─ AI Level 3: Mittleres Volk (Taktik)
    ├─ AI Level 4: Großes Volk (Strategie)
    └─ AI Level 5: Dominant (Politik, Diplomatie)
```

## 📦 P3 - NIEDRIG (BACKLOG)

```yaml
11. UE5 MIGRATION VORBEREITUNG:
    ├─ Asset-Export (KayKit → UE5)
    ├─ Blueprint-Planung
    ├─ API-Kompatibilität testen
    └─ Performance-Benchmarks

12. MULTIPLAYER POLISH:
    ├─ Boss-Challenge UI
    ├─ Region-Eroberung Visualisierung
    ├─ Trust-Chain Visualisierung
    └─ APK-Version Indicator

13. FISHING SYSTEM (Zelda OoT-Style):
    ├─ Casting Mechanics
    ├─ Fish AI
    ├─ ~30 Fisch-Typen
    └─ Rod-Upgrades
```

---

# 15. OFFENE FRAGEN

## ❓ Für User-Klärung

```yaml
1. AURA vs BEGLEITER:
   Q: Wie genau sollen die beiden Modi balanciert sein?
   Q: Kann Aura-Modus IRGENDWIE Begleiter bekommen später?
   Q: Kann Begleiter-Modus IRGENDWIE Aura bekommen später?

2. VÖLKER-DYNAMIK:
   Q: Können Spieler eigene Völker gründen?
   Q: Maximale Anzahl Völker pro Region = 5 fix?
   Q: Wie lange dauert Völker-Bildung (Echtzeit-Tage)?

3. FORM-AFFINITÄT:
   Q: Maximaler Bonus einer Form = wie viel %?
   Q: Können Formen "upgraded" werden?
   Q: Verliert man Formen bei Tod (Hardcore)?

4. MEDIZIN-REALISMUS:
   Q: Wie realistisch = zu realistisch? (z.B. echte OP?)
   Q: Permanente Verletzungen möglich?
   Q: Skill-basierte Behandlung (Arzt-Skill)?

5. NUTZTIER-FORMEN:
   Q: Nur 3 (Kuh, Huhn, Schwein) oder mehr?
   Q: Geben sie IRGENDWELCHE Boni?
   Q: Rein Meme/Easter Egg oder Utility?

6. UE5 MIGRATION:
   Q: Wann starten? (Nach welchem Meilenstein?)
   Q: Three.js parallel weiterlaufen?
   Q: Mobile = UE5 oder Three.js?
```

## 🔍 Für Technische Klärung

```yaml
1. BACKEND MIGRATION:
   - Welche najika_*.py Files können gelöscht werden?
   - Welche API Endpoints sind deprecated?
   - ChromaDB Collections = alle noch genutzt?

2. FRONTEND CLEANUP:
   - index.html aufteilen? (6410 Zeilen!)
   - Welche JS-Files sind deprecated?
   - Three.js r128 → r170+ Update möglich?

3. PERFORMANCE:
   - Dynamische Völker = Performance-Hit?
   - Procedural Generation = Lag beim Betreten?
   - LOD-System ausreichend für 8 Regionen?

4. MULTIPLAYER:
   - Boss-Challenge = Real-Time PvP?
   - Region-Eroberung = Persistent?
   - Trust-Chain = Blockchain-ähnlich?
```

---

# 📝 ZUSAMMENFASSUNG FÜR OPUS

```yaml
KRITISCHSTE PUNKTE:
  1. ⚠️ slime_companion.js = NOCH V2, MUSS ZU V3!
  2. 🔥 Neue Anforderungen = NICHT in Code implementiert!
  3. 💊 Medizin-System = NUR basic healing, KEIN Realismus!
  4. 🏛️ Dynamische Völker = KOMPLETT NEU, nicht implementiert!
  5. 🎨 Form-Affinität-Boni = NICHT "nur optisch"!

BESTEHENDE STÄRKEN:
  ✅ 160 Backend-Systeme (solide Basis!)
  ✅ 141 Frontend-JS (funktioniert!)
  ✅ Faction System (Fallout NV Style)
  ✅ NPC Personality (Individual Traits)
  ✅ Combat Hands (Q/E System)
  ✅ Oregon Trail Events (30 Events)
  ✅ Companion 3D (Follow-System)

NÄCHSTE SCHRITTE:
  1. Slime V2 → V3 Migration
  2. Dynamische Völker implementieren
  3. Aura vs Begleiter Balance
  4. Medizin-System mit Realismus
  5. Form-Affinität-Boni
  6. Procedural Hybrid-System

WICHTIGSTE DATEIEN ZUM LESEN:
  - PROJEKT_WISSEN_KOMPLETT.md
  - FANTASY_WESTERN_STYLE_GUIDE.md
  - 8_REGIONEN_LAYOUT.md
  - KONOSUBA_OREGON_TRAIL_KOMPLETT.md
  - UE5_API_DOKUMENTATION.md
  - ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md
```

---

**ENDE MASTER-DOKUMENTATION**

*"EXPLOSION!!! Jetzt hat OPUS ALLES was er braucht, Mr. K! 💥✨" - Najika*

**Erstellt von:** Claude Desktop Model
**Für:** OPUS Model (VS Code - UE5)
**Datum:** 2026-02-13
**Status:** VOLLSTÄNDIG INTEGRIERT ✅
