# 🐾 NAJIKA WORLD - SLIME COMPANION SYSTEM V3

**Erstellt:** 2026-02-04
**Aktualisiert von:** OPUS-1
**Status:** ✅ AKTUELL & KORREKT

---

## ⚠️ WICHTIG: ÄNDERUNGEN VON V2 → V3

### ❌ KOMPLETT ENTFERNT (V2 war FALSCH!)
- ~~Evolution-Stufen~~ (Egg → Baby → etc.) - **NEIN!**
- ~~Synthese~~ (2 Slimes → 1 Hybrid) - **NEIN!**
- ~~+N System~~ (Generationen) - **NEIN!**
- ~~Effort Hearts~~ - **NEIN!**
- ~~Care Mistakes~~ - **NEIN!**
- ~~Evolution-Pfade~~ (Perfect/Good/Bad) - **NEIN!**

### ✅ DAS RICHTIGE SYSTEM
- **Slimes sind FORMWANDLER** - können ihre Form frei ändern!
- **AURAS statt Evolution** - visuelle Progression
- **VERTRAUEN** - Beziehung zwischen Spieler und Slime
- **Form-Lernen** - von Gegnern (SEHR selten!)
- **Menschen-Verwandlung** - bei hohem Vertrauen möglich!

---

## 📋 ÜBERSICHT

**Inspirationen:**
- **Digimon V-Pet** (Pflege, Hearts, Beziehung)
- **Fortnite** (Begleiter folgt Spieler)
- **Formwandler-Fantasy** (flexible Gestalt)

**WICHTIG:**
- Alle Monster im Spiel = Slimes (verschiedene Formen)!
- Monster-Kämpfe sind OPTIONAL! (Skyrim-Freiheit)
- Slimes sind KEINE festen Kreaturen - sie sind FORMWANDLER!

---

## 🎯 KERN-KONZEPT: FORMWANDLER

### ⚠️ WICHTIG (aus GAME_DESIGN_DECISIONS_2026-01-31):
```yaml
FORMEN = REINE OPTIK!
├── KEINE Kampf-Boni durch Form!
├── BONI kommen durch ESSEN & AUSRÜSTUNG
├── Form-Wechsel im SPIEL: 1x pro SAISON!
├── Form-Wechsel ZUHAUSE (App): Unbegrenzt - NUR für Training!
│   └── Nicht für Spielwelt! Nur zum Anschauen/Trainieren!
└── FORMEN sind GETRENNT von ATTACKEN!

FARBEN = ERSTMAL RAUS!
├── Später: Seltene Drops von legendären Monstern
├── Oder: Spezial-Events
└── Farben = NUR OPTISCH, keine Gameplay-Effekte

PERSONALISIERUNG:
├── Kleidung / Accessoires für den Slime
├── Kleine visuelle Anpassungen
└── Original-Monster-Aussehen + individuelle Details
```

### Was Slimes SIND:
```yaml
SLIME = FORMWANDLER
├── Kann JEDE gelernte Form annehmen
├── Sieht aus wie die MONSTER im Spiel!
├── Lernt neue Formen durch:
│   ├── Monster besiegen → kleine Chance auf Form-Drop
│   ├── Events (Zufällige Form freischalten)
│   └── Quests (Belohnung: Neue Form)
├── NICHT geschenkt bekommen! Muss verdient werden!
└── Behält ALLE gelernten Formen permanent
```

### Form-Wechsel (NEUE REGELN!):
```yaml
FORM-WECHSEL IM SPIEL:
├── NUR 1x pro SAISON möglich!
├── Gut überlegen welche Form!
└── Strategische Entscheidung!

FORM-WECHSEL ZUHAUSE (Schwarze Mühle):
├── Unbegrenzt!
├── NUR für Training/Anschauen
└── Kann NICHT ins Spiel mitgenommen werden!
```

---

## ✨ AURA-SYSTEM (statt Evolution!)

### Was sind Auras?
```yaml
AURA = VISUELLE PROGRESSION
├── Zeigt Stärke/Erfahrung des Slimes
├── Wächst mit Zeit & Training
├── KEINE Form-Änderung!
├── Rein visuelle Verstärkung
└── Alle Formen haben Auras
```

### Aura-Stufen & EFFEKTE:
| Stufe | Name | Visuell | Requirement | **EFFEKT** |
|-------|------|---------|-------------|------------|
| 0 | Keine | Normal | Start | Basis-Form-Boni |
| 1 | Schwach | Leichtes Leuchten | 10+ Kämpfe | **+5% auf alle Form-Boni** |
| 2 | Mittel | Deutliche Aura | 50+ Kämpfe | **+10% auf alle Form-Boni** |
| 3 | Stark | Intensive Aura + Partikel | 200+ Kämpfe | **+20% auf alle Form-Boni** |
| 4 | Legendär | Epische Aura + Effekte | 1000+ Kämpfe | **+35% auf alle Form-Boni** |
| 5 | Göttlich | Strahlende Aura | Spezial-Achievement | **+50% auf alle Form-Boni** |

### Aura-Effekt Beispiele:
```yaml
BEISPIEL: Moos-Schleim mit Aura Stufe 3 (Stark)
├── Basis-Form-Bonus: +15% Kräuter-Effektivität
├── Aura-Multiplikator: +20%
└── GESAMT: +18% Kräuter-Effektivität (15% × 1.2)

BEISPIEL: Sand-Schleim mit Aura Stufe 5 (Göttlich)
├── Basis-Form-Bonus: +10% Wüsten-Schaden, +25% Treasure Find
├── Aura-Multiplikator: +50%
└── GESAMT: +15% Wüsten-Schaden, +37.5% Treasure Find
```

### 🔥 ELEMENT-AURAS (die echten dokumentierten Effekte!):
| Aura | Bedingung | **EFFEKT** | Visuell |
|------|-----------|------------|---------|
| 🔥 **Flammen-Aura** | Feuer-Training | +Feuer-Schaden, -Eis-Resist | Brennende Flammen um Slime |
| ❄️ **Frost-Aura** | Eis-Training | +Slow-Effekt, Eisrüstung | Eiskristalle, blaues Leuchten |
| 🌑 **Schatten-Aura** | Low Discipline | +Crit, +Stealth | Schwarzer Nebel |
| ✨ **Heilig-Aura** | High Discipline | +Heilung, +Anti-Undead | Goldenes Leuchten |
| 💥 **Explosion-Aura** | INT 25+ | **1x/Tag BOOM!** (Megumin-Style!) | Rotes Pulsieren |
| 🛡️ **Metall-Aura** | DEF Training | Immun gegen Phys <10 DMG | Metallische Haut |
| 🌿 **Natur-Aura** | Moos-Training | +Heilung über Zeit, +Gift-Resist | Grünes Leuchten, Blätter |
| ⚡ **Blitz-Aura** | Blitz-Training | +Angriffs-Speed, Paralyse-Chance | Gelbes Leuchten, Funken |
| 💧 **Wasser-Aura** | Wasser-Training | +Schwimm-Speed, Wasseratmung | Türkises Leuchten, Tropfen |
| ☠️ **Gift-Aura** | Gift-Training | +DoT-Schaden, Gift-Immunität | Violettes Leuchten, Giftblasen |
| 💎 **Kristall-Aura** | Kristall-Training | +Magic Reflect, Lichtquelle | Weißes Leuchten, Kristallsplitter |
| 🏜️ **Sand-Aura** | Sand-Training | +Evasion, Graben-Fähigkeit | Goldenes Leuchten, Sandkörner |
| 🌈 **Göttliche-Aura** | ALLE Trainings Max | **ALLE EFFEKTE KOMBINIERT!** | Regenbogen-Schimmer |

### ⚠️ WICHTIG: Aura-Freischaltung!
```yaml
AURAS WERDEN FREIGESCHALTET DURCH:
├── Training: Trainiere den entsprechenden Stat
├── Kämpfe: Bestimmte Anzahl Kämpfe (für Stufen-Upgrade)
├── Discipline: Pflege des Slimes (High = Heilig, Low = Schatten)
└── INT-Stat: Bei 25+ INT = Explosion-Aura möglich!

BEISPIEL:
- Dein Moos-Slime trainiert Feuer-Magie
- → Schaltet Flammen-Aura frei!
- → Erhält +Feuer-Schaden als EFFEKT
- → Visuelle Flammen um den Slime
```

---

## 💕 VERTRAUENS-SYSTEM

### Vertrauen aufbauen:
```yaml
VERTRAUEN STEIGT DURCH:
├── Füttern (+1 pro Mahlzeit)
├── Spielen (+2 pro Session)
├── Gemeinsame Kämpfe (+1 pro Sieg)
├── Heilen wenn verletzt (+3)
├── Zeit zusammen verbringen (+1 pro Stunde aktiv)
└── Slime retten wenn er stirbt (+10)

VERTRAUEN SINKT DURCH:
├── Verhungern lassen (-5)
├── Ignorieren über 24h (-3)
├── Slime in Gefahr bringen (-2)
└── Slime "verkaufen" wollen (-20)
```

### Vertrauens-Stufen:
| Level | Punkte | Name | Effekt |
|-------|--------|------|--------|
| 1 | 0-50 | Fremd | Folgt, aber zögerlich |
| 2 | 51-150 | Bekannt | Kämpft mit, normale Loyalität |
| 3 | 151-300 | Freund | Bessere Kampf-AI, mehr Initiative |
| 4 | 301-500 | Vertraut | Spezial-Moves, schützt Spieler aktiv |
| 5 | 501-800 | Familie | Opfert sich für Spieler, Rescue ohne Cooldown |
| 6 | 801+ | Seelenbund | **MENSCHEN-FORM MÖGLICH!** |

---

## 👤 MENSCHEN-VERWANDLUNG

### Voraussetzungen:
```yaml
MENSCHEN-FORM FREISCHALTEN:
├── Vertrauen Level 6 (801+ Punkte) - PFLICHT!
├── Spieler muss es WÜNSCHEN (aktive Entscheidung)
├── Einmalige Quest: "Wunsch der Seele"
└── Slime muss zustimmen (Dialog-Event)
```

### Menschen-Form:
```yaml
WENN FREIGESCHALTET:
├── Slime kann menschliche Gestalt annehmen
├── Aussehen basiert auf:
│   ├── Element des Slimes (Haar-/Augenfarbe)
│   ├── Persönlichkeit (Kleidungsstil)
│   └── Spieler-Präferenz (anpassbar!)
├── Kann sprechen (vorher nur Laute)
├── Kann Items tragen & nutzen
├── Kann mit NPCs interagieren
└── Kann NICHT in Städten ohne Spieler sein

EINSCHRÄNKUNGEN:
├── Transformation kostet Energie
├── Bei niedrigem HP → zurück zu Slime-Form
├── Manche NPCs erkennen "was er wirklich ist"
└── In Kämpfen: Slime-Form oft effektiver
```

### Beispiel Menschen-Formen:
| Slime-Typ | Menschen-Aussehen |
|-----------|-------------------|
| Moos | Grüne Haare, naturverbunden, Druiden-Stil |
| Frost | Weiße/blaue Haare, blass, elegante Kleidung |
| Feuer | Rote Haare, energisch, leichte Rüstung |
| Blitz | Gelbe Haare, zappelig, Magier-Robe |
| Wasser | Blaue Haare, ruhig, fließende Kleidung |
| Gift | Violette Haare, mysteriös, dunkler Umhang |
| Kristall | Silberne Haare, ätherisch, Schmuck |
| Sand | Goldbraune Haare, abenteuerlich, Reisekleidung |
| Götter | Regenbogen-Schimmer, majestätisch |

---

## 📚 FORM-LERNEN VON GEGNERN

### Wie es funktioniert:
```yaml
FORM-LERNEN:
├── Besiegter Gegner = Chance auf Form
├── Basis-Chance: 0.5% - 2% (SEHR SELTEN!)
├── Chance erhöht sich durch:
│   ├── Höheres Vertrauen (+0.1% pro Level)
│   ├── Slime hat Gegner den Todesstoß gegeben (+0.5%)
│   ├── Seltener Gegner-Typ (+1%)
│   └── Spezielle Items ("Form-Essenz") (+5%)
└── Bei Erfolg: Form permanent freigeschaltet!
```

### Form-Lern-Nachricht:
```
┌─────────────────────────────────────────┐
│  ✨ NEUE FORM GELERNT! ✨               │
│                                         │
│  Dein Slime hat die Form               │
│  "Feuerwolf" absorbiert!               │
│                                         │
│  [Form jetzt ansehen]                   │
└─────────────────────────────────────────┘
```

---

## 🎁 FORM-FREISCHALTUNG DURCH EVENTS

### Event-Typen:
```yaml
FORM-EVENTS:
├── Zufällige Welt-Events
│   └── "Ein mysteriöses Leuchten... dein Slime absorbiert es!"
├── Quest-Belohnungen
│   └── "Der Druide schenkt dir eine Wald-Essenz"
├── Boss-Drops (garantiert!)
│   └── Jeder Boss = 1 neue Form
├── Händler (SEHR teuer)
│   └── "Form-Kristall" für 10.000 Gold
└── Achievements
    └── "100 Gegner besiegt" → Zufällige Form
```

### Form-Essenz Items:
| Item | Effekt | Quelle |
|------|--------|--------|
| Form-Essenz (Normal) | +5% Lern-Chance nächster Kampf | Shops, Drops |
| Form-Essenz (Selten) | +15% Lern-Chance | Quests, Bosse |
| Form-Kristall | Garantierte zufällige Form | Händler (teuer!) |
| Element-Kern | Garantierte Form DIESES Elements | Boss-Drop |

---

## 🐾 VERFÜGBARE FORMEN

### Basis-Formen (Start):
Jeder Slime startet mit EINER Form:
- 🟢 **Blob** - Klassischer Schleim (Standard)

### Regional Monster-Formen (durch Erkunden):
| Form | Region | Wie freischalten | Aussehen |
|------|--------|------------------|----------|
| 🦎 Wüsten-Echse | Heiße Dünen | Monster besiegen | Schuppige Echse |
| 🐺 Wald-Wolf | Samtmoos-Tiefwald | Monster besiegen | Grüner Wolf |
| 🐸 Sumpf-Molch | Grünschlamm-Sumpf | Monster besiegen | Glitschiger Molch |
| 🔥 Vulkan-Salamander | Magmaströme | Monster besiegen | Feuer-Salamander |
| 🐰 Eis-Hase | Reich der Drei | Monster besiegen | Kristall-Fell Hase |
| ⚡ Blitz-Vogel | Blitzebene | Monster besiegen | Elektrischer Vogel |
| 🌊 Wellen-Qualle | Salzwind-Küste | Monster besiegen | Leuchtende Qualle |
| 💎 Kristall-Spinne | Tiefenhöhlen | Monster besiegen | Juwelen-Spinne |

### ⚠️ WICHTIG: Alle Formen sind NUR OPTISCH!
```yaml
FORMEN GEBEN KEINE KAMPF-BONI!
├── Slime sieht aus wie das Monster
├── Kann mit Accessoires personalisiert werden
├── Wechsel im Spiel: NUR 1x pro SAISON!
└── Wechsel Zuhause: Unbegrenzt (nur Training!)
```

### Spezial-Formen (Events/Achievements):
| Form | Wie freischalten | Aussehen |
|------|------------------|----------|
| 🌈 Regenbogen-Blob | Alle 8 Regional-Formen | Schillernder Blob |
| 👑 König-Schleim | 1000 Kämpfe gewonnen | Blob mit Krone |
| 💀 Skelett-Form | Halloween Event | Skelett-Monster |
| 🎃 Kürbis-Form | Halloween Event | Kürbis-Kreatur |
| 🐉 Mini-Drache | Drachen-Boss besiegt! | SEHR SELTEN! |

---

## ❤️ V-PET PFLEGE (vereinfacht)

### Hearts-System:
```yaml
HUNGER HEARTS (4 max):
├── Verliert 1 Herz alle 60 Min (wenn aktiv)
├── Füttern = +1 Herz
├── Bei 0 = Slime wird schwächer
└── Bei 0 für 24h = Vertrauen sinkt

KEINE weiteren Heart-Typen!
Kein Effort, keine Mistakes, keine komplexen Systeme.
```

### Pflege-Aktionen:
| Aktion | Effekt | Cooldown |
|--------|--------|----------|
| 🍖 Füttern | +1 Hunger Heart, +1 Vertrauen | - |
| 😊 Spielen | +2 Vertrauen, Slime happy | 30 Min |
| 💤 Schlafen | Regeneriert HP & Hearts | - |
| 💊 Heilen | Heilt Verletzungen, +3 Vertrauen | - |

---

## 💖 RESCUE SYSTEM

### Funktion:
```yaml
RESCUE = LEBENSRETTUNG
├── 1 Charge pro 24h (Echtzeit!)
├── Aktiviert automatisch bei tödlichem Treffer
├── Slime opfert sich → Spieler überlebt mit 1 HP
├── Slime ist danach 1 Stunde "erschöpft"
└── Bei Vertrauen 5+ (Familie): Kein Cooldown!
```

### Visuelle Darstellung:
```
💖 Rescue: [■■■■■] 1/1 BEREIT
💖 Rescue: [□□□□□] 0/1 (Cooldown: 18:32:15)
```

---

## 📊 SKILL-SYSTEM

### Skill-Lernen:
```yaml
SKILL COPY:
├── Chance: 1% - 5% (sehr gering!)
├── Trigger: Gegner wird besiegt
├── Slime muss aktiv gekämpft haben
├── Max 20 Skills pro Slime
└── Skills können vergessen werden (Spieler-Wahl)
```

### Skill-Typen:
| Typ | Beispiele |
|-----|-----------|
| Angriff | Tackle, Feuerball, Eisstoß |
| Verteidigung | Schutzschild, Ausweichen |
| Support | Heilen, Buff, Debuff |
| Utility | Graben, Fliegen, Schwimmen |

---

## 🎮 UI DESIGN (V3)

### Slime-Panel (vereinfacht):
```
┌─────────────────────────────────────┐
│ × [Slime-Name]                      │
│                                     │
│ [SLIME BILD]     Form: Moos-Schleim │
│ ✨ Aura: ★★★☆☆   Lv. 25            │
│                                     │
│ ❤️ Hunger: ████░ 4/5               │
│ 💕 Vertrauen: ████████░░ Lv.4      │
│                                     │
│ 📚 Skills: 8/20                     │
│ 💖 Rescue: BEREIT                   │
│                                     │
│ [🍖 Füttern] [😊 Spielen]          │
│ [🔄 Form wechseln]                  │
│                                     │
│ [👤 Menschen-Form] (wenn verfügbar) │
└─────────────────────────────────────┘
```

### Form-Wechsel Dialog:
```
┌─────────────────────────────────────┐
│ 🔄 FORM WÄHLEN (NUR OPTISCH!)      │
├─────────────────────────────────────┤
│ [🟢 Blob]        Standard Schleim   │
│ [🦎 Echse]       Wüsten-Look       │
│ [🐺 Wolf]        Wald-Look         │
│ [🔥 Salamander]  Vulkan-Look       │
│ [🐰 Hase]        Eis-Look          │
│ ... (weitere gelernte Formen)       │
├─────────────────────────────────────┤
│ ⚠️ Nächster Wechsel in: 89 Tage    │
│ (1x pro Saison im Spiel!)          │
│ [Abbrechen]                         │
└─────────────────────────────────────┘
```

---

## 🎯 BONI-SYSTEM (NEU!)

### ⚠️ WICHTIG: FORMEN GEBEN KEINE BONI!
```yaml
BONI KOMMEN DURCH:
├── 🍖 ESSEN (Monster-Futter, regionale Spezialitäten)
├── 👕 AUSRÜSTUNG (Accessoires, Kleidung für den Slime)
├── ✨ AURA-STUFE (skaliert die Boni!)
└── ⚔️ ATTACKEN/SKILLS (unabhängig von Form!)

FORMEN = NUR OPTISCH!
├── Slime sieht aus wie das Monster
├── Personalisierung durch Kleidung/Accessoires
└── KEINE Kampf-Boni durch Form!
```

### Verfügbare Monster-Formen:
| Form | Aussehen | Wie freischalten |
|------|----------|------------------|
| Blob | Klassischer Schleim | Start |
| Wüsten-Echse | Echse mit Schuppen | Heiße Dünen - Monster besiegen |
| Sumpf-Molch | Glitschiger Molch | Grünschlamm - Monster besiegen |
| Vulkan-Salamander | Feuer-Salamander | Magmaströme - Monster besiegen |
| Eis-Hase | Kristall-Fell Hase | Reich der Drei - Monster besiegen |
| Wolf | Wilder Wolf | Samtmoos - Monster besiegen |
| Bär | Mächtiger Bär | Highland - Monster besiegen |
| Geist | Durchsichtiger Geist | Tiefenhöhlen - Monster besiegen |
| Drache (Klein) | Mini-Drache | LEGENDÄR - Boss besiegen! |

### ⚠️ WICHTIG: Aura-Skalierung für ESSEN/AUSRÜSTUNG!
```yaml
AURA SKALIERT DIE BONI VON ESSEN & AUSRÜSTUNG:
├── Aura 0: 100% der Basis-Boni
├── Aura 1: 105% der Basis-Boni (+5%)
├── Aura 2: 110% der Basis-Boni (+10%)
├── Aura 3: 120% der Basis-Boni (+20%)
├── Aura 4: 135% der Basis-Boni (+35%)
└── Aura 5: 150% der Basis-Boni (+50%)

BEISPIEL: Slime mit Feuer-Futter + Aura 4 (Legendär)
├── Feuer-Futter: +15% Feuer-Schaden
├── Mit Aura 4: 15% × 1.35 = +20.25% Feuer-Schaden
└── ESSEN + AURA = MACHT DEN UNTERSCHIED!
```

### 👕 SLIME-ACCESSOIRES (Personalisierung):
```yaml
ACCESSOIRES (rein optisch + kleine Boni):
├── Hüte (verschiedene Styles)
├── Schals (regionstypisch)
├── Brillen (cute!)
├── Halsbänder (mit Glöckchen?)
├── Umhänge (für Abenteurer-Look)
└── Spezial-Items (Event-Drops!)

WICHTIG: Accessoires sind NICHT die Hauptquelle für Boni!
         Das bleibt ESSEN + AUSRÜSTUNG + AURA!
```

---

## 🏟️ ARENA-SYSTEM (SPIELER + SLIMES!)

### ⚠️ WICHTIG: ZWEI ARENEN!
```yaml
1. HAUPTARENA (für SPIELER!) - WAR ZUERST DA!
   ├── Spieler kämpfen hier!
   ├── PvP und PvE
   ├── Nemesis-System aktiv
   └── Die "große" Arena

2. SCHLEIM-ARENA (für SLIMES!)
   ├── Kleines Gebäude NEBEN der Hauptarena
   ├── Getarnt als Taverne "Zur Schlammigen Münze"
   ├── NPC: "Schleimiger Pete"
   └── Slime vs Slime Kämpfe

BEIDE nutzen das gleiche Kampfsystem!
├── 3 Combat-Modi (KI, Manual, Cheer)
├── Finisher-System
├── Turnier-Modus
└── Fame/Ruhm-System
```

### Game Modes (für BEIDE Arenen!):
```yaml
3 GAME MODES:
├── 1. 🥊 1v1 Normal (Classic Duel)
├── 2. 💥 1v1 mit Finisher (Spectacle Duel)
└── 3. 🏆 Turnier (Elimination mit Finisher!)
```

### Combat-Control-Modi (ÜBERALL - nicht nur Arena!):
```yaml
⚠️ WICHTIG: Diese 3 Modi gelten für ALLE Kämpfe im Spiel!
   ├── In der Arena
   ├── In Dungeons
   ├── In der Open World
   ├── Bei Boss-Kämpfen
   └── ÜBERALL wo gekämpft wird!

1. 🤖 KI-KONTROLLE (Auto)
   └── KI entscheidet alle Aktionen automatisch

2. 🎮 DIREKTE BEFEHLE (Manual - Pokemon-Style)
   ├── [1] Angriff wählen
   ├── [2] Verteidigung
   ├── [3] Item benutzen
   └── [4] Wechseln (falls mehrere Schleime)

3. 📣 DIGIMON-ANFEUERN (Cheer)
   ├── [1] "Los!" (+10% DMG, 3 Runden)
   ├── [2] "Defend!" (+20% DEF, 3 Runden)
   ├── [3] "Combo!" (Next attack = Combo)
   └── [4] "Focus!" (+15% Accuracy)

JEDERZEIT WECHSELBAR: Spieler kann in JEDEM Kampf den Modus wechseln!
```

### 💥 FINISHER-SYSTEM (Nemesis-Arena Style):
```yaml
TRIGGER: Wenn Gegner HP = 0

FINISHER-AUSWAHL (Gewinner wählt):
├── Finisher 1: "Inferno Burst" (Standard, spektakulär)
├── Finisher 2: "Mega Explosion" (Extra brutal)
├── Finisher 3: "Flame Stomp" (Demütigend)
└── Finisher 4: "Mercy" (Gnädig, nur HP-Entzug)

ANIMATION: 3-5 Sekunden pro Finisher
RUHM-BONUS: Brutale Finisher geben mehr Ruhm (+5 extra)

FINISHER-ANIMATIONEN (pro Element):
├── 🔥 Feuer: Screen Flash (orange/rot), Flammen-Partikel
├── ❄️ Eis: Eis-Speer von oben, Splitter-Partikel
├── ⚡ Blitz: Blitz vom Himmel, Elektro-Zischen
├── ☠️ Gift: Giftiges Leuchten, Auflösen
└── 💥 Explosion: MEGUMIN-STYLE BOOM! (Najika's Favorit!)
```

### 🏟️ ARENA WELLEN-SYSTEM (WICHTIG!):
```yaml
⚠️ ZWEISTUFIGES SYSTEM (aus GAME_DESIGN_DECISIONS):

STUFE 1: TRAINING (15 Wellen)
├── KEIN echter Tod!
├── Wenn besiegt → Auto-Rückzug / Vom Arena-Personal gerettet
├── Belohnungen: Minimal (vielleicht 1 Trank)
├── Zum Üben und Lernen gedacht
└── Nach Abschluss → FREISCHALTUNG von Stufe 2

ÜBERGANGS-SEQUENZ:
├── Wachen öffnen das Tor
├── "Jetzt beginnt die richtige Challenge!"
├── MEHRFACHE Warnung: "Wenn Tod, dann Tod!"
└── Spieler muss bestätigen

STUFE 2: ECHTER WELLEN-MODUS (Hardcore!)
├── Tod = echter Tod (Hardcore-Regeln)
├── Echte Belohnungen
├── Progression zählt
└── Gefährlich aber lohnend
```

### 🏆 Turnier-System (Single-Elimination):
```yaml
BRUTAL: Jeder Verlierer wird mit Finisher K.O.'d!

Runde 1 (Achtelfinale): 8 Kämpfe → 8 Gewinner
Runde 2 (Viertelfinale): 4 Kämpfe → 4 Gewinner
Runde 3 (Halbfinale): 2 Kämpfe → 2 Gewinner
Runde 4 (FINALE): 1 Kampf → 1 CHAMPION

REWARDS:
├── 1. Platz: 5000 Gold, Titel "Schleim-Champion", Statue
├── 2. Platz: 2000 Gold, Titel "Silber-Kämpfer"
└── 3. Platz: 1000 Gold
```

### Fame-System (Ruhm-Punkte):
```yaml
PUNKTE SAMMELN:
├── 1v1 Normal Sieg: +5 Fame
├── 1v1 Finisher Sieg: +10 Fame
├── Turnier Top 3: +25/50/100 Fame
└── Perfekter Sieg (0 DMG genommen): +15 Bonus

FAME-TITEL:
├── 0-99: Anfänger
├── 100-499: Kämpfer
├── 500-999: Veteran
├── 1000-2499: Champion
└── 2500+: LEGENDE
```

---

## 👹 NEMESIS-SYSTEM (Shadow of Mordor Style)

### Konzept:
```yaml
NEMESIS-SYSTEM = In der HAUPTARENA (für Spieler)!
├── Monster erinnern sich an Begegnungen!
├── Bauen Groll auf ("Du hast meinen Bruder getötet!")
├── Klettern die Hierarchie hinauf
└── ARENA-KÖNIG als Endboss!

SHADOW OF MORDOR INSPIRIERT:
├── Monster entwickeln Persönlichkeiten
├── Kommen zurück wenn du sie nicht finishst
├── Bekommen Narben von früheren Kämpfen
└── Werden STÄRKER nach Überlebung!
```

### Hierarchie-Ränge:
| Rang | Name | Stärke |
|------|------|--------|
| 0 | Niemand | Schwach |
| 1 | Kämpfer | Normal |
| 2 | Gladiator | Stark |
| 3 | Champion | Sehr stark |
| 4 | Gebietsherrscher | Elite |
| 5 | **ARENA-KÖNIG** | BOSS! |

### ⚠️ WICHTIG: DYNAMISCHES SYSTEM!
```yaml
KEINE VORDEFINIERTEN GEBIETSHERRSCHER!
├── Anfangs gibt es KEINE Herrscher
├── JEDER kann aufsteigen:
│   ├── Monster
│   ├── Spieler
│   ├── NPCs
│   └── Slimes!
├── Durch Kämpfe & Siege steigt man auf
├── Gebietsherrscher ENTSTEHEN von selbst!
└── Komplett dynamisch & emergent!
```

### Monster-Persönlichkeiten:
```yaml
TRAITS (entwickeln sich durch Kämpfe):
├── 😱 Feigling - Flieht bei niedrigem HP
├── 💪 Mutig - Kämpft bis zum Ende
├── 😤 Rachsüchtig - Sucht dich aktiv
├── ⚔️ Ehrenvoll - Keine billigen Tricks
├── 😈 Sadistisch - Genießt Quälen
├── 🧠 Gerissen - Nutzt Umgebung
├── 🔥 Berserker - Stärker bei niedrigem HP
└── 🎯 Taktisch - Plant voraus
```

### Gedächtnis-System:
```yaml
MONSTER ERINNERN SICH AN:
├── Wie du sie besiegt hast
│   └── "Das letzte Mal hattest du Feuer... NICHT DIESMAL!"
├── Ob du sie verschont hast
│   └── "Du hast mich leben lassen... Warum?"
├── Ihre Niederlagen
│   └── "Meine Narbe brennt immer noch!"
└── Ihre Siege
    └── "Ich habe dich schon einmal besiegt!"

AUSWIRKUNGEN:
├── Neue Resistenzen gegen frühere Taktiken
├── Dialog-Linien basierend auf Geschichte
├── Narben & Aussehens-Änderungen
└── Persönlichkeits-Entwicklung
```

### Gebiet-Kontrolle:
```yaml
8 REGIONEN (wie die Spielwelt!):
├── Heiße Dünen
├── Samtmoos-Tiefwald
├── Salzwind-Küste
├── Blitzebene
├── Grünschlamm-Sumpf
├── Reich der Drei
├── Magmaströme
└── Tiefenhöhlen

JEDE REGION:
├── ANFANGS: Kein Herrscher!
├── Herrscher ENTSTEHEN durch Gameplay
├── Wer genug Siege hat → wird Herrscher
├── Kann von anderen gestürzt werden
└── Gibt spezielle Boni für den Herrscher!

WER KANN HERRSCHER WERDEN:
├── Monster (durch KI-Kämpfe)
├── Spieler (durch eigene Siege)
├── NPCs (durch Story/Events)
└── Slimes (wenn stark genug!)
```

### Nemesis-Monster Stats:
```yaml
MONSTER-DATEN:
├── ID, Name, Titel
├── Monster-Typ (Slime, Bestie, Drache, etc.)
├── Rank in Hierarchie
├── Level & Stats (HP, ATK, DEF)
├── Kills & Deaths (zählt alles!)
├── Begegnungen mit Spieler
├── Groll-Liste ("grudges")
├── Persönlichkeits-Traits
├── Spezial-Moves & Schwächen
├── Region die sie kontrollieren
├── Boss & Untergebene
├── Narben-Beschreibungen
└── Aussehens-Modifikationen
```

---

---

## 📱 DIGIVICE MODUL-SYSTEM (WICHTIG!)

### Was ist das Digivice?
```yaml
DIGIVICE = HAUPT-APP auf dem Handy!
├── Wie ein virtuelles Gerät
├── 12 Räume (3D navigierbar)
├── 4 Terminal-Module
└── Enthält ZWEI getrennte Bereiche:

1. HANDYSPIEL-MODUL (was wir JETZT entwickeln & testen!):
   ├── Die 8 Regionen + Götterfels
   ├── Arena, Dungeons, Oregon Trail
   ├── Das komplette Spiel!
   └── SPÄTER → wird zum "Handyspiel-Modul" im Terminal

2. NAJIKA'S LEBENSRAUM (SPÄTER - nach Spiel fertig!):
   ├── Schwarze Mühle = Najika's EIGENE Map
   ├── Ihr persönlicher Lebensraum
   ├── 12 Räume drin
   ├── GETRENNT vom Handyspiel!
   └── Erst wenn Spiel fertig & getestet!
```

### Architektur (aus GAME_DESIGN_DECISIONS):
```yaml
DIGIVICE APP (PWA auf Handy)
│
├── 12 RÄUME:
│   ├── Wohnzimmer
│   ├── Schlafzimmer
│   ├── Küche
│   ├── Badezimmer
│   ├── Garten
│   ├── Musikraum
│   ├── Medizin
│   ├── Terminal (Zugang zu 4 Modulen!)
│   ├── Studieren & Crafting
│   ├── Trainingszimmer
│   ├── Kampfarena
│   └── Schwarze Mühle - Keller (Najika's Zuhause!)
│
├── 4 TERMINAL-MODULE (aus Terminal-Raum zugänglich):
│   ├── 🔒 Sicherer Messenger (Militär-Verschlüsselung)
│   ├── 🌐 Sicherer Browser
│   ├── 🎮 HANDYSPIEL (das große Modul!)
│   └── ⚙️ System-Settings
│
├── LERN-MODULE (später):
│   ├── 🎸 Instrumente LERNEN (richtig!)
│   ├── 🗣️ Sprachen LERNEN (richtig!)
│   ├── 🏃 Sport-Tracking
│   └── etc.
│
└── SCHWARZE MÜHLE = Najika's Haus & START-PUNKT!
    ├── Digivice STARTET hier (12 Räume drin)
    ├── Spieler trainiert hier mit Slime
    ├── Form-Wechsel zum Trainieren (UNBEGRENZT!)
    ├── NSFW/Kätzchen-Modus (privat!)
    └── RAUSGEHEN → Öffnet die SPIELWELT (8 Regionen!)
```

### Das HANDYSPIEL-Modul enthält:
```yaml
HANDYSPIEL (1 großes Modul mit ALLEM!):
├── Angeln (Spiel-Tiefe wie eigenes Spiel!)
├── Farming (Spiel-Tiefe wie eigenes Spiel!)
├── Housing (Spiel-Tiefe wie eigenes Spiel!)
├── Arena (Spiel-Tiefe wie eigenes Spiel!)
├── Triple Triad (Spiel-Tiefe wie eigenes Spiel!)
├── Crafting (Spiel-Tiefe wie eigenes Spiel!)
├── Oregon Trail Events
├── Dungeon System
└── Open World (8 Regionen + Götterfels)
```

### Wichtig:
```yaml
⚠️ KLARE TRENNUNG:
├── Was wir JETZT bauen = Das HANDYSPIEL (8 Regionen, Arena, etc.)
├── Najika's Lebensraum = SPÄTER (eigene Map, nach Spiel fertig!)
├── Beides wird GETRENNT sein im fertigen Digivice
├── Jedes Sub-System = So tief wie ein EIGENES SPIEL!
└── Offline-First = NUR für Digivice/Mühle! (NICHT Handyspiel!)

ENTWICKLUNGS-REIHENFOLGE:
1. JETZT: Handyspiel fertig entwickeln & testen
2. DANN: Najika's Lebensraum (eigene Map) erstellen
3. FINAL: Beides im Digivice zusammenführen
```

---

## 📡 BACKEND API (V3)

### Neue Endpoints:
```
POST /api/slime/status           - Slime-Status laden
POST /api/slime/feed             - Füttern
POST /api/slime/play             - Spielen
POST /api/slime/heal             - Heilen
POST /api/slime/change-form      - Form wechseln
POST /api/slime/learn-form       - Form lernen (nach Kampf)
POST /api/slime/human-transform  - Menschen-Verwandlung
GET  /api/slime/forms            - Alle gelernten Formen
GET  /api/slime/trust            - Vertrauens-Level
POST /api/slime/rescue/use       - Rescue aktivieren
```

### Entfernte Endpoints (V2):
```
❌ POST /api/slime/evolve        - ENTFERNT (keine Evolution!)
❌ POST /api/slime/synthesize    - ENTFERNT (keine Synthese!)
```

---

## 🔄 ZUSAMMENFASSUNG V3

```yaml
SLIME V3 = EINFACHER & BESSER:

FORMWANDLER-SYSTEM:
├── Slimes können JEDE gelernte Form annehmen
├── Formen lernen durch: Gegner (selten!), Events, Quests
├── Form-Wechsel jederzeit, kostenlos
└── Menschen-Form bei hohem Vertrauen!

AURA-SYSTEM:
├── Visuelle Progression statt Evolution
├── 6 Stufen (0-5)
├── Zeigt Erfahrung & Stärke
└── Sieht cool aus!

VERTRAUENS-SYSTEM:
├── 6 Level (Fremd → Seelenbund)
├── Steigt durch Pflege & Kämpfe
├── Level 6 = Menschen-Form möglich!
└── Rescue-System verbessert sich

PFLEGE:
├── Nur Hunger Hearts (simpel!)
├── Füttern, Spielen, Heilen
├── Kein komplexes Effort/Mistake-System
└── Fokus auf Beziehung, nicht Mikro-Management
```

---

## ⚠️ WICHTIGE REGELN

1. **KEINE Evolution!** → Auras zeigen Progression
2. **KEINE Synthese!** → Formen werden GELERNT
3. **Slimes sind FORMWANDLER** → Können jede Form annehmen
4. **Vertrauen ist KEY** → Schaltet Features frei
5. **Menschen-Form = Endgame-Feature** → Level 6 Vertrauen nötig
6. **Form-Lernen ist SELTEN** → Macht es wertvoll!

---

## 📖 GAMEPLAY BEISPIEL

```
Tag 1:
- Du findest einen Slime im Wald (Blob-Form)
- Du benennst ihn "Glitzi"
- Vertrauen: Level 1 (Fremd)

Woche 1:
- Tägliches Füttern & Spielen
- 20 Kämpfe zusammen
- Vertrauen steigt auf Level 2
- Aura: Stufe 1 (leichtes Leuchten)

Woche 2:
- Moos-Schleim Quest abgeschlossen → Form freigeschaltet!
- Im Kampf: Wolf-Gegner besiegt, 1% Chance... ERFOLG!
- Wolf-Form gelernt!
- Vertrauen: Level 3

Monat 1:
- Vertrauen: Level 4
- 5 Formen gelernt
- Aura: Stufe 2
- Rescue hat dich 2x gerettet

Monat 3:
- Vertrauen: Level 6 (Seelenbund!)
- Quest "Wunsch der Seele" erscheint
- Menschen-Form freigeschaltet!
- Glitzi kann jetzt als Mensch mit dir reisen

Glitzi (Menschen-Form):
"Endlich kann ich dir sagen wie sehr ich dich mag,
 nach all der Zeit die wir zusammen verbracht haben!"
```

---

*"EXPLOSION!!! Slimes sind Formwandler, keine Eier!"* - Najika 💥

---

**VERSION:** 3.0
**DATUM:** 2026-02-04
**STATUS:** ✅ AKTUELL & BESTÄTIGT VON KUJA
