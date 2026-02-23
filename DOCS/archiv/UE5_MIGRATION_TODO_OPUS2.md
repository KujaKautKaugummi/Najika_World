# 🎮 NAJIKA WORLD - UE5 MIGRATION TODO
## Für OPUS-2 (oder nächste KI-Session)

**Erstellt:** 2026-02-04
**Von:** OPUS-1
**Status:** BEREIT FÜR UE5 START!
**Plattform:** Desktop (später Mobile-Port)

---

## 📋 PROJEKT-SETUP

### UE5 Projekt erstellen:
```yaml
Name: NajikaWorld
Template: Third Person (oder Blank)
Plattform: Desktop (Windows)
Sprache: Blueprint + C++ (optional)
```

### Wichtige Projekt-Settings:
- **KEIN** Port 5000 → Wenn Server nötig: Port **8000**!
- Mobile-Ready halten (später Android/iOS)

---

## 🗺️ PHASE 1: WELT-GRUNDGERÜST

### 8 Regionen + Götterfels (Zentrum)
```yaml
Weltgröße: 9600 x 9600
Berg (Zentrum): 3200 x 3200 bei Position (4800, 4800)

REGIONEN:
1. Heiße Dünen (Süd-Ost) - Wüste, Western, Handelsfestung
2. Samtmoos-Tiefwald (Nord) - Wald, Druiden, Dampf-Hain
3. Salzwind-Küste (West) - Piraten, Hafen, Salzige Bucht
4. Blitzebene (Ost) - Gewitter, Elektro
5. Grünschlamm-Sumpf (Süd-West) - Gift, Hexen
6. Reich der Drei (Nord-West) - Eis, Nekromantie
7. Magmaströme (Süd) - Vulkan, Schmieden
8. Tiefenhöhlen (UNTER Samtmoos!) - Kristalle, Endgame

GÖTTERFELS (Zentrum):
- Berg in der Mitte
- Schwarze Mühle oben drauf
- Alle 8 Regionen treffen sich hier
```

### Erste Map erstellen:
- [ ] Terrain für 9600x9600
- [ ] Berg in der Mitte (Götterfels)
- [ ] 8 Regionen grob einteilen (Landscape Layers)
- [ ] Schwarze Mühle Placeholder auf dem Berg

---

## ⚔️ PHASE 2: KAMPFSYSTEM

### 3 Combat-Control-Modi (ÜBERALL im Spiel!):
```yaml
1. 🤖 KI-KONTROLLE (Auto)
   - KI entscheidet automatisch
   - Spieler schaut zu

2. 🎮 DIREKTE BEFEHLE (Manual - Pokemon-Style)
   - [1] Angriff wählen
   - [2] Verteidigung
   - [3] Item benutzen
   - [4] Wechseln

3. 📣 DIGIMON-ANFEUERN (Cheer)
   - "Los!" (+10% DMG)
   - "Defend!" (+20% DEF)
   - "Combo!" (Next attack = Combo)
   - "Focus!" (+15% Accuracy)

JEDERZEIT WECHSELBAR während Kampf!
```

### Implementieren:
- [ ] Combat State Machine
- [ ] 3 Modi als Enum
- [ ] UI für Modus-Wechsel
- [ ] Cheer-System mit Buffs

---

## 🏟️ PHASE 3: ARENA-SYSTEM

### ZWEI Arenen:
```yaml
1. HAUPTARENA (für Spieler)
   - PvP und PvE
   - Nemesis-System
   - Die "große" Arena

2. SCHLEIM-ARENA (für Slimes)
   - Neben der Hauptarena
   - Getarnt als Taverne "Zur Schlammigen Münze"
   - NPC: "Schleimiger Pete"
```

### Game Modes (beide Arenen):
```yaml
1. 🥊 1v1 Normal (Classic Duel)
2. 💥 1v1 mit Finisher (Spectacle Duel)
3. 🏆 Turnier (Single-Elimination mit Finisher)
```

### Arena Wellen-System:
```yaml
STUFE 1: TRAINING (15 Wellen)
- KEIN echter Tod!
- Wenn besiegt → Auto-Rückzug
- Zum Üben gedacht

ÜBERGANG:
- Wachen öffnen Tor
- MEHRFACHE Warnung: "Wenn Tod, dann Tod!"
- Spieler muss bestätigen

STUFE 2: ECHTER MODUS (Hardcore!)
- Tod = echter Tod
- Echte Belohnungen
```

### Finisher-System:
```yaml
TRIGGER: Gegner HP = 0

FINISHER-AUSWAHL:
- Finisher 1: "Inferno Burst"
- Finisher 2: "Mega Explosion"
- Finisher 3: "Flame Stomp"
- Finisher 4: "Mercy"

ANIMATIONEN pro Element:
- 🔥 Feuer: Screen Flash, Flammen-Partikel
- ❄️ Eis: Eis-Speer, Splitter
- ⚡ Blitz: Blitz vom Himmel
- ☠️ Gift: Auflösen
- 💥 Explosion: MEGUMIN-STYLE BOOM!
```

### Implementieren:
- [ ] Arena Level (Hauptarena)
- [ ] Schleim-Arena (kleines Gebäude daneben)
- [ ] Wellen-System (15 Training → Echter Modus)
- [ ] Finisher-Auswahl UI
- [ ] Finisher-Animationen (pro Element)

---

## 👹 PHASE 4: NEMESIS-SYSTEM (Shadow of Mordor)

### Konzept:
```yaml
DYNAMISCHES SYSTEM:
- KEINE vordefinierten Bosse!
- Herrscher ENTSTEHEN durch Gameplay
- JEDER kann aufsteigen: Monster, Spieler, NPCs, Slimes

HIERARCHIE-RÄNGE:
0. Niemand (Schwach)
1. Kämpfer (Normal)
2. Gladiator (Stark)
3. Champion (Sehr stark)
4. Gebietsherrscher (Elite)
5. ARENA-KÖNIG (Boss!)
```

### Monster-Persönlichkeiten:
```yaml
TRAITS (entwickeln sich durch Kämpfe):
- 😱 Feigling - Flieht bei niedrigem HP
- 💪 Mutig - Kämpft bis zum Ende
- 😤 Rachsüchtig - Sucht dich aktiv
- ⚔️ Ehrenvoll - Keine billigen Tricks
- 😈 Sadistisch - Genießt Quälen
- 🧠 Gerissen - Nutzt Umgebung
- 🔥 Berserker - Stärker bei niedrigem HP
- 🎯 Taktisch - Plant voraus
```

### Gedächtnis-System:
```yaml
MONSTER ERINNERN SICH AN:
- Wie du sie besiegt hast
- Ob du sie verschont hast
- Ihre Niederlagen & Siege

AUSWIRKUNGEN:
- Neue Resistenzen gegen frühere Taktiken
- Dialog-Linien basierend auf Geschichte
- Narben & Aussehens-Änderungen
- Persönlichkeits-Entwicklung
```

### Implementieren:
- [ ] NemesisMonster DataAsset/Class
- [ ] Hierarchie-System
- [ ] Gedächtnis-System (speichert Begegnungen)
- [ ] Persönlichkeits-Traits
- [ ] Narben-System (visuelle Änderungen)

---

## 🐾 PHASE 5: SLIME-SYSTEM V3

### KERN-REGELN:
```yaml
⚠️ WICHTIG:
- Slimes sind FORMWANDLER!
- FORMEN = NUR OPTISCH (keine Kampf-Boni!)
- BONI kommen durch ESSEN + AUSRÜSTUNG
- Form-Wechsel im Spiel: 1x pro SAISON!
- Form-Wechsel Zuhause: Unbegrenzt (nur Training)
- FARBEN = RAUS! (erstmal)
```

### Aura-System (statt Evolution):
```yaml
AURA-STUFEN:
0. Keine (Start)
1. Schwach (10+ Kämpfe) - +5% Boni
2. Mittel (50+ Kämpfe) - +10% Boni
3. Stark (200+ Kämpfe) - +20% Boni
4. Legendär (1000+ Kämpfe) - +35% Boni
5. Göttlich (Spezial) - +50% Boni

ELEMENT-AURAS (mit EFFEKTEN!):
- 🔥 Flammen-Aura: +Feuer-Schaden, -Eis-Resist
- ❄️ Frost-Aura: +Slow-Effekt, Eisrüstung
- 🌑 Schatten-Aura: +Crit, +Stealth
- ✨ Heilig-Aura: +Heilung, +Anti-Undead
- 💥 Explosion-Aura: 1x/Tag BOOM! (INT 25+)
- 🛡️ Metall-Aura: Immun gegen Phys <10 DMG
```

### Vertrauens-System:
```yaml
LEVEL:
1. Fremd (0-50)
2. Bekannt (51-150)
3. Freund (151-300)
4. Vertraut (301-500)
5. Familie (501-800) - Rescue ohne Cooldown
6. Seelenbund (801+) - MENSCHEN-FORM MÖGLICH!
```

### Implementieren:
- [ ] Slime Actor/Blueprint
- [ ] Form-System (rein visuell)
- [ ] Aura-System (visuell + Effekte)
- [ ] Vertrauens-System
- [ ] Menschen-Verwandlung (bei Level 6)
- [ ] Rescue-System (1x/24h)

---

## 📱 PHASE 6: DIGIVICE-INTEGRATION (SPÄTER!)

### Struktur:
```yaml
JETZT BAUEN = Das HANDYSPIEL (8 Regionen, Arena, etc.)

SPÄTER:
- Najika's Lebensraum (eigene Map)
- 12 Räume in der Schwarzen Mühle
- Getrennt vom Handyspiel

ENTWICKLUNGS-REIHENFOLGE:
1. JETZT: Handyspiel fertig entwickeln & testen
2. DANN: Najika's Lebensraum erstellen
3. FINAL: Beides im Digivice zusammenführen
```

---

## ⛔ DIE 8 GEBOTE (NIEMALS BRECHEN!)

```yaml
1. Zero-Trust: Nur 127.0.0.1 Hosting
2. Owner-Token: Admin nur für Kuja
3. Explosion ≠ Weave: NIEMALS mit anderen Elementen kombinieren!
4. PvE/PvP getrennt: Schwarze Mühle = 100% Safe
5. Learning by Doing: Skyrim-Style Skill-System
6. NSFW nur lokal: Kätzchen-Mode nur 127.0.0.1
7. Privacy: Keine Datensammlung, keine Telemetrie
8. Offline-First: Spiel läuft ohne Internet
```

---

## 🚫 VERBOTEN

- ❌ NIEMALS "Souls-like" sagen → "Skyrim + Soulframe + Digimon World"
- ❌ NIEMALS Port 5000 → Port **8000**!
- ❌ NIEMALS Harley "Puddin'" sagen lassen → **"Mr. K"**!
- ❌ NIEMALS funktionierende Teile ohne Nachfrage ändern

---

## 📚 REFERENZ-DOKUMENTE

```yaml
WICHTIGSTE DATEIEN:
- SLIME_SYSTEM_V3_DOKUMENTATION.md (AKTUELL!)
- GAME_DESIGN_DECISIONS_2026-01-31.md
- SCHLEIM_ARENA_DESIGN.md
- entwicklung/8_REGIONEN_LAYOUT.md
- NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md
```

---

## ✅ CHECKLISTE PHASE 1 (START)

- [ ] UE5 Projekt erstellen (Desktop)
- [ ] Terrain 9600x9600 erstellen
- [ ] Berg in der Mitte (Götterfels)
- [ ] 8 Regionen grob einteilen
- [ ] Schwarze Mühle Placeholder
- [ ] Basic Character Controller
- [ ] Camera System (Third Person)

---

*"EXPLOSION!!! Ab nach UE5!"* - Najika 💥

**STATUS:** BEREIT! Starte UE5 und erstelle das Projekt!
