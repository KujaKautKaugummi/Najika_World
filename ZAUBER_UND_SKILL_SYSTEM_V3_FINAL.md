# 🎯 ZAUBER & SKILL SYSTEM V3 - FINALE SPEZIFIKATION

**Erstellt:** 2026-02-09
**Status:** FINAL - Bereit für Implementation
**Diskutiert mit:** User (Kuja) + Opus 2

---

## 📋 INHALTSVERZEICHNIS

1. [Übersicht](#übersicht)
2. [Hogwarts Spell-Diamond System](#hogwarts-spell-diamond-system)
3. [Grund-Zauber System](#grund-zauber-system)
4. [1-Skill-Weg vs. Generalist](#1-skill-weg-vs-generalist)
5. [Morphs (Diablo 4 Style)](#morphs-diablo-4-style)
6. [Learning-Systeme](#learning-systeme)
7. [Cross-Element Learning](#cross-element-learning)
8. [S.P.E.C.I.A.L. Stats](#special-stats)
9. [Permadeath & Safe Zones](#permadeath--safe-zones)
10. [Slime-KI System](#slime-ki-system)
11. [Namen-System](#namen-system)
12. [Implementation Checklist](#implementation-checklist)

---

## ÜBERSICHT

### Das Problem (ALT):
```
❌ MMO-Hotbar: 10 Zauber auf Leiste (nervt!)
❌ Feste Namen: Alle nutzen "Feuerball"
❌ Linear: Fire → Fira → Firaga (langweilig)
❌ Keine Konsequenzen: Meister in allem möglich
```

### Die Lösung (NEU):
```
✅ Hogwarts Spell-Diamond: Intuitives Casting
✅ Spieler benennen Zauber selbst: "Höllenball", "EXPLOSION!!!"
✅ 1 Grund-Zauber → Viele Spezialisierungen (organisch)
✅ 1-Skill-Weg vs. Generalist: Echte Trade-Offs
✅ Morphs durch Beobachten/Experimentieren: Discovery!
```

---

## HOGWARTS SPELL-DIAMOND SYSTEM

### Konzept:
**Statt MMO-Hotbar → Element halten, dann wählen!**

```
ALTE METHODE (MMO):
[Feuerball] [Eiszapfen] [Blitzschlag] [Heilung] [Windklinge]
└─ 10 Skills auf Leiste, klicken = casten

NEUE METHODE (Hogwarts):
1. Halte Element-Taste (z.B. "F" für Feuer)
2. Spell Diamond erscheint:

                  ╱ Feuerball (↑) ╲
                 ╱                  ╲
     Feuerwand (←) 🔥 FEUER 🔥 Verzauberung (→)
                 ╲                  ╱
                  ╲ Explosion (↓) ╱

3. Wähle mit Maus/Stick → Cast!
```

### Controls:
```yaml
Standard:
├─ Linke Hand (L): Schwert / Waffe
├─ Rechte Hand (R): Magie
└─ [R-Trigger] halten = Diamond öffnet

Casting:
├─ [R-Trigger + ↑] = Zauber oben
├─ [R-Trigger + ↓] = Zauber unten
├─ [R-Trigger + ←] = Zauber links
└─ [R-Trigger + →] = Zauber rechts

Optional: UI ausblenden (Immersion)
├─ Diamond wird unsichtbar
├─ Du siehst nur Element in Hand
└─ Drückst blind ↑↓←→
```

### Vorteile:
```
✅ Keine 10 Hotkeys merken!
✅ Intuitive Element-Wahl
✅ Mehr Spells verfügbar (4 pro Element!)
✅ Feels wie echtes Zaubern
✅ Wie Hogwarts Legacy!
```

---

## GRUND-ZAUBER SYSTEM

### Konzept:
**Jede Schule = 1 Grund-Zauber (anfängerfreundlich)**

```
┌─────────────────────────────────────────────────────────────┐
│         9 SCHULEN, 9 GRUND-ZAUBER                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔥 FEUER   → "Flamme"      (25 DMG, 1s, Basis)           │
│  ❄️ EIS     → "Frost"       (20 DMG, 1.2s, Slow 20%)      │
│  ⚡ BLITZ   → "Funke"       (30 DMG, 0.8s, schnell)        │
│  💧 WASSER  → "Strahl"      (15 DMG, 1s, DoT 5s)          │
│  🪨 ERDE    → "Steinwurf"   (35 DMG, 1.5s, Knockback)      │
│  🌪️ WIND    → "Bö"         (20 DMG, 0.5s, Push)           │
│  🌿 NATUR   → "Dornen"      (25 DMG, 1s, Bleed)            │
│  ✨ LICHT   → "Schein"      (30 DMG, 1s, vs Undead x2)    │
│  🌑 DUNKEL  → "Schatten"    (28 DMG, 1s, Blind)            │
│  💥 EXPLOSION → "Explosion" (100 DMG, 2s, AoE 5m)         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Wie man lernt:
```
ANFANGS-TUTORIAL:
├─ Wähle 1 Schule
├─ NPC Magier zeigt Grund-Zauber
└─ Du lernst ihn (garantiert!)

ODER:

DURCH BEOBACHTEN:
├─ Siehst anderen Magier Feuer nutzen
├─ 10x beobachten → 5% Chance "Flamme" zu lernen
└─ Gleiches Element = schneller (10% statt 5%)
```

### Dann: Spezialisierung!
```
Aus 1 BASIS-ZAUBER wird DEIN persönlicher Stil:

Experimentierst: Schnelle Casts
→ "Flammen-Salve" (10 DMG, 0.3s, spam!)

Beobachtest: Große Feuerbälle
→ "Feuerball" (50 DMG, 2s, stark!)

Experimentierst: Auf Boden casten
→ "Feuerwand" (30 DMG/s, Zone, DoT!)

Cross-Learning: Eis + Feuer
→ "Dampf" (Blind-Effekt, Support!)
```

---

## 1-SKILL-WEG VS. GENERALIST

### Die große Entscheidung:
```
⚠️ UNWIDERRUFLICH - KANN NICHT RÜCKGÄNGIG! ⚠️

OPTION A: 1-SKILL-WEG (MEISTER) 🎯
OPTION B: NORMALER WEG (GENERALIST) 🌈
```

### Meister (1-Skill-Weg):

```
✅ VORTEILE:
├─ Endskill wird EXTREM stark (+300% Endgame = 400 DMG)
├─ Exklusive Morphs (Mini, Sniper, Chain, etc.)
├─ Prestige-Titel: "Meister der [Name]"
├─ Ultimate-Form (bei 180+ Tagen Training)
└─ PvP: Kann One-Shot'en

❌ NACHTEILE:
├─ Andere Skills VERKÜMMER über Zeit!
│   Tag 30:  -20% (-80 → 64 DMG)
│   Tag 60:  -50% (-80 → 40 DMG)
│   Tag 90:  -80% (-80 → 16 DMG)
│   Tag 180: -90% (-80 → 8 DMG) = Fast nutzlos!
│
├─ KEINE Flexibilität (1 Trick)
├─ Immun-Gegner = Hilflos!
├─ Vergessene Skills NICHT wieder erlernbar!
└─ Bei Permadeath: High Risk!

WICHTIG:
Du erinnerst dich MENTAL noch an andere Skills,
aber dein Körper/Mana kann sie nicht mehr nutzen!
Quasi "verlernt" - musst NEU anfangen.

ABER: Als Meister kannst du sie NICHT neu lernen!
(Du hast dein Leben verschrieben!)
```

### Generalist (Normaler Weg):

```
✅ VORTEILE:
├─ ALLE Skills bleiben effektiv
├─ Kann situativ anpassen
├─ Gegner-Immun? → Wechsel Element!
├─ Mehr Spaß durch Variation
└─ Learning by Doing für alle Skills

❌ NACHTEILE:
├─ Kein Skill wird "Meister"-Level
├─ Normale Damage (+140% Endgame = 120 DMG)
├─ Keine exklusiven Morphs
├─ Kein Prestige-Titel
└─ Kein Ultimate

WICHTIG:
Kann vergessene Skills WIEDER lernen!
(Zurück auf Grundwert, dann neu trainieren)
```

### Vergleich Endgame (Tag 180):

```
SZENARIO: Boss-Fight

Spieler A (Explosion-Meister):
├─ Explosion: 400 DMG ⚡💥⚡ (Ultimativ!)
├─ Feuerball: 8 DMG ❌ (Vergessen)
└─ Blitzschlag: 5 DMG ❌ (Vergessen)

Gegen Normal-Gegner: 💯 ONE-SHOT!
Gegen Explosion-Immune: 😱 HILFLOS!

Spieler B (Generalist):
├─ Feuerball: 120 DMG 🔥 (Solide)
├─ Blitzschlag: 84 DMG ⚡ (Solide)
├─ Eiszapfen: 67 DMG ❄️ (Solide)
└─ Heilung: 90 HP 💚 (Solide)

Gegen Normal-Gegner: ✅ Braucht 3-4 Hits
Gegen Explosion-Immune: ✅ Nutzt andere Elemente!
```

### Warnung beim Wählen:

```
╔═══════════════════════════════════════════════════════════╗
║           ⚠️ MEISTER-WEG WÄHLEN ⚠️                       ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Du verschreibst dein GANZES LEBEN dieser Kunst!         ║
║                                                           ║
║  KONSEQUENZEN:                                            ║
║  • Andere Zauber werden verkümmern (bis zu -90%!)        ║
║  • Du kannst sie NICHT wieder erlernen (permanent!)      ║
║  • UNWIDERRUFLICH - kein Zurück!                         ║
║  • Bei Tod = Character verloren! (Permadeath!)           ║
║                                                           ║
║  ABER:                                                    ║
║  • Du wirst MEISTER (+300% Schaden!)                     ║
║  • Exklusive Morphs & Ultimate                           ║
║  • Prestige & Ruhm                                       ║
║                                                           ║
║  Bist du SICHER?                                         ║
║  [Ja, Meister werden] / [Nein, abbrechen]               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Nur 1 Meisterschaft pro Leben!

```
❌ NICHT MÖGLICH:
• Explosion-Meister + Schwert-Meister
• Feuer-Meister + Eis-Meister
• 2 Meisterschaften gleichzeitig

WARUM?
"Wie in echt: Vieles gut, aber perfekt nur in 1 Sache"

Beispiele:
• Michael Jordan: Basketball-Meister (nicht Baseball)
• Einstein: Physik-Meister (nicht Musik)
• Gordon Ramsay: Koch-Meister (nicht Fußball)
```

---

## MORPHS (DIABLO 4 STYLE)

### Konzept:
**1 Skill-Weg = 1 Skill mit vielen Morphs!**

```
EXPLOSION BEISPIEL:

LEVEL 1-9: Normale EXPLOSION
├─ 100 Damage, 5m Radius AoE
├─ Kostet 50 Mana + 30 Stamina
└─ 2s Cast Time

LEVEL 10: Enhancement freigeschaltet!
└─ "Kritische Detonation" - Crit Chance +20%

MORPHS (durch Learning freigeschaltet):
├─ Mini-Explosion (schnell, spam)
├─ Sniper-Explosion (gezielt, weit)
├─ Chain-Explosion (springt 3x)
├─ Ground-Explosion (Falle)
├─ Mega-Explosion (größer, langsamer)
└─ Rolling-Explosion (in Bewegung)

WICHTIG:
• Name bleibt "Explosion" (ändert sich nie!)
• Nur Effekt/Mechanik ändert sich
• Nur 1 Morph kann aktiv sein
• Wenn Morph aktiv: Normale nicht verfügbar
• Morphs jederzeit wechselbar (aber nur 1 aktiv!)
```

### Morphs im Detail:

```
MINI-EXPLOSION:
├─ 50 DMG (statt 100)
├─ 2m Radius (statt 5m)
├─ 0.5s Cast (statt 2s)
├─ 25 Mana (statt 50)
└─ Spam-fähig!

SNIPER-EXPLOSION:
├─ 120 DMG
├─ 1m Radius (präzise!)
├─ 2s Cast
├─ 30m Range (gezielt!)
└─ Fernkampf-Spezialist

CHAIN-EXPLOSION:
├─ 80 DMG pro Hit
├─ Springt 3x zu nächstem Gegner
├─ Smart-Targeting
├─ 60 Mana
└─ Multi-Target!

GROUND-EXPLOSION:
├─ Platziert Falle
├─ Explodiert bei Kontakt
├─ 120 DMG
├─ 10s Dauer
└─ Taktisch!
```

---

## LEARNING-SYSTEME

### 3 Wege Morphs zu lernen:

```
┌─────────────────────────────────────────────────────────────┐
│         METHODE 1: BEOBACHTEN                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Andere nutzen Technik → Du lernst davon                   │
│                                                              │
│  Gleiches Element: 10x sehen = 10% Chance (schnell!)       │
│  Ähnlich Element:  30x sehen =  3% Chance (langsam)        │
│  Fremdes Element: 100x sehen =  1% Chance (sehr langsam!)  │
│                                                              │
│  Beispiel:                                                   │
│  Siehst Kettenblitz 15x → Lernst Chain-Explosion!          │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│         METHODE 2: CROSS-LEARNING                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Logische Verbindungen zwischen Skills                      │
│                                                              │
│  WICHTIG: Du lernst TECHNIK/FORM, nicht Element!           │
│                                                              │
│  Beispiele:                                                  │
│  • Siehst Eis-Zapfen (spitz) → Lernst FEUER-Zapfen!       │
│  • Siehst Chain-Lightning → Lernst Chain-Explosion!        │
│  • Siehst Trap-Skill → Lernst Ground-Explosion!           │
│                                                              │
│  ❌ NICHT: "Ich sehe Eis → Ich lerne Eis!"                 │
│  ✅ RICHTIG: "Ich sehe Eis-Form → Feuer in dieser Form!"   │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│         METHODE 3: EXPERIMENTIEREN 🧪                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DU probierst selbst Varianten aus!                        │
│                                                              │
│  EXPERIMENT 1: Weniger Kraft                                │
│  ────────────────────────────                               │
│  Du castest Explosion mit 50% Mana statt 100%              │
│  → Zauber ist schwächer ABER schneller!                    │
│  → Nach 30x: "💡 Durchbruch!"                              │
│  → MINI-EXPLOSION entdeckt!                                 │
│                                                              │
│  EXPERIMENT 2: Mehr Konzentration                          │
│  ─────────────────────────────                              │
│  Du zielst extra lange (3s+ Cast)                          │
│  → Zauber ist präziser, fliegt weiter                      │
│  → Nach 30x: "💡 Du verstehst Präzision!"                 │
│  → SNIPER-EXPLOSION entdeckt!                               │
│                                                              │
│  EXPERIMENT 3: Verzögern                                    │
│  ────────────────────                                       │
│  Du castest aber lässt Zauber nicht sofort los            │
│  → Zauber bleibt am Boden                                   │
│  → Nach 25x: "💡 Du kannst Zauber platzieren!"            │
│  → GROUND-EXPLOSION entdeckt!                               │
│                                                              │
│  PROGRESS-TRACKING:                                          │
│  • System trackt dein Verhalten                            │
│  • "Noch 7x bis Durchbruch! (23/30)"                       │
│  • UI zeigt Progress (optional, ausblendbar!)              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Skill-Learning Rates:

```
ALTE WERTE (zu hoch):
├─ Normal: 8% Chance
└─ Boss: 20% Chance

NEUE WERTE (balanced):
├─ Normal: 2% Chance ✅
└─ Boss: 5% Chance ✅
```

---

## CROSS-ELEMENT LEARNING

### Andere Elemente lernen (sehr langsam!):

```
REGEL: Du KANNST andere Elemente lernen!
       ABER: Es dauert SEHR SEHR lange!

LERN-GESCHWINDIGKEIT:
├─ Gleiches Element:    10x sehen = 10% Chance  (schnell!)
├─ Ähnliches Element:   30x sehen =  3% Chance  (langsam)
└─ Fremdes Element:    100x sehen =  1% Chance  (sehr langsam!)

ÄHNLICHE ELEMENTE:
├─ Feuer ↔ Blitz     (beide Destruction)
├─ Eis ↔ Wasser      (beide Kälte/Flüssig)
├─ Erde ↔ Natur      (beide organisch)
└─ Licht ↔ Dunkel    (beide Energie)

FREMDE ELEMENTE:
├─ Feuer → Eis       (Gegensätze!)
├─ Blitz → Erde      (komplett anders)
└─ Licht → Natur     (unrelated)
```

### Beispiel:

```
FEUER-NUTZER LERNT EIS (fremdes Element):

Prozess:
├─ Siehst Eis 100x in Kämpfen! 😰
├─ Jedes Mal: NUR 1% Chance
├─ Durchschnittlich: ~100 Kämpfe bis Erfolg
└─ Kann auch 200+ Kämpfe dauern (RNG)

Nach Lernen:
├─ Eis startet bei 10 DMG (sehr schwach!)
├─ Feuer bleibt Main (120 DMG)
├─ Eis wächst SEHR langsam (25% normale Rate)
└─ Kostet mehr Mana (+50%)

WARUM SO SCHWER?
"Feuer und Eis sind Gegensätze!"
"Dein Körper/Geist ist auf Feuer programmiert"
"Eis zu lernen widerspricht deiner Natur"
→ Extrem schwierig aber MÖGLICH!

VERWENDUNG:
Fremde Elemente = Nischen-Skills!
Nicht für Main-Damage, sondern Utility!

Beispiel:
Feuer-Main lernt Eis (schwach) für Slow-Effekt
Nicht zum Schaden machen, sondern CC!
```

---

## S.P.E.C.I.A.L. STATS

### Fallout-Style Start-Werte:

```yaml
S.P.E.C.I.A.L. SYSTEM:
├─ S = Strength   (Nahkampf, Tragen)
├─ P = Perception (Hit-Chance, Crit-Chance)
├─ E = Endurance  (HP, Stamina)
├─ C = Charisma   (NPC-Interaktion, Preise)
├─ I = Intelligence (Magie-Schaden, Mana)
├─ A = Agility    (Dodge, Angriffsspeed)
└─ L = Luck       (Crit, Loot, Learning)

START-WERTE:
├─ Jeder Stat: 1-10
├─ Start-Pool: 40 Punkte zum Verteilen
├─ Minimum pro Stat: 1
└─ Maximum Start: 10
```

### Balance (WICHTIG!):

```
PROBLEM:
"Wenn INT zu wichtig → JEDER muss INT 10 nehmen!"
"Wenn STR zu wichtig → JEDER muss STR 10 nehmen!"
→ FORCED Meta = SCHLECHT!

LÖSUNG: SANFTE BONI!
Stats geben KLEINE Boni, nicht riesige!

BEISPIEL INT (Intelligenz):
├─ INT  1: Magie +0%,  Mana +0
├─ INT  5: Magie +12%, Mana +40   (Durchschnitt)
└─ INT 10: Magie +25%, Mana +90   (Spezialist)

→ Unterschied: 25% (nicht 200%!)
→ INT 1 ist VIABLE (nur 25% schwächer)
→ INT 10 ist BESSER aber nicht Pflicht!

BEISPIEL STR (Stärke):
├─ STR  1: Nahkampf +0%,  Tragen 50kg
├─ STR  5: Nahkampf +12%, Tragen 100kg  (Durchschnitt)
└─ STR 10: Nahkampf +25%, Tragen 200kg  (Spezialist)

→ STR 1 Magier ist OK! (nutzt eh Magie)
→ STR 10 Krieger ist stark, aber nicht Pflicht

BALANCE-REGEL:
"Jeder Build muss viable sein!"
• INT 10 Magier: Stark in Magie
• STR 10 Krieger: Stark in Nahkampf
• BALANCED (5/5/5/5): Gut in allem
• WEIRD Build (10/1/1/10): Nische aber viable!

ALLE BUILDS FUNKTIONIEREN! ✅
Keine "Trap-Stats"!

⚠️ MUSS PLAYTESTED WERDEN! ⚠️
```

---

## PERMADEATH & SAFE ZONES

### Hardcore-System:

```
CLIENT-AUTHORITATIVE COMBAT:
├─ DEIN Client entscheidet über DEINEN Charakter
├─ Server synct nur, entscheidet NICHT
├─ Disconnect? → Spiel PAUSIERT, du stirbst NICHT
└─ Söldner laggt? → Sein Problem, nicht deins

DISCONNECT-HANDLING:
SOFORT:
├─ Spiel PAUSIERT
├─ Gegner frieren ein
├─ Timer: 30 Sekunden Reconnect-Window
└─ UI: "Verbindung unterbrochen..."

NACH 30 SEK:
├─ Immer noch weg? → Safe-Logout
├─ Charakter verschwindet aus Welt
├─ Kein Tod, kein Progress-Loss
└─ Beim nächsten Login: Vor dem Kampf

WARUM FUNKTIONIERT DAS:
├─ Offline-First = Kein Server nötig für Kampf
├─ Pause ist IMMER möglich
└─ Multiplayer-Session endet einfach

MOTTO:
"Ein Held stirbt durch den Feind, nicht durch die Technik."
```

**Referenz:** `DOCS\TECHNISCHE_ANFORDERUNGEN_HARDCORE.md`

### Safe Zones (kein Permadeath):

```
✅ SAFE ZONES (kein Permadeath):
├─ Schwarze Mühle (Najikas Zuhause, 100% Safe)
├─ Slime Arena (immer safe)
├─ Spieler Arena (erste 15 Stufen Wellen-Modus + normale Stufe)
└─ Städte (in Code definiert)

⚠️ PERMADEATH ZONES (überall sonst!):
├─ Overworld (alle 9 Regionen)
├─ Dungeons
├─ Boss-Fights
├─ PvP (außerhalb Arena)
└─ Wilderness
```

### Was passiert bei Tod:

```
CHARACTER STIRBT:
├─ Screen: "Du bist gestorben. Permanent."
├─ Character wird gelöscht
└─ Neuer Character erstellen

WAS BLEIBT:
├─ ❌ Character: WEG
├─ ❌ Skills: WEG
├─ ❌ Level: WEG
├─ ❌ Meisterschaft: WEG
├─ ✅ Slime-KI: Erinnerungen bleiben! (Lerndaten)
├─ ✅ Account-Achievements
└─ ✅ Unlocked Cosmetics
```

---

## SLIME-KI SYSTEM

### 2 Ebenen der Slime-KI:

```
┌─────────────────────────────────────────────────────────────┐
│         SLIME-KI: PERSÖNLICHKEIT vs. SPIEL-SKILLS           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  EBENE 1: PERSÖNLICHKEIT (außerhalb Spiel)                 │
│  ─────────────────────────────────────────                  │
│  ✅ Bleibt konsistent!                                      │
│  ✅ Erinnerungen bleiben!                                   │
│  ✅ Weiß über alles Bescheid!                               │
│  ✅ Kennt alle Boss-Schwächen (mental)                      │
│                                                              │
│  Beispiel:                                                   │
│  "Ich erinnere mich: Stein-Golem ist schwach gegen Magie!" │
│                                                              │
│  EBENE 2: SPIEL-CHARACTER (Slime im Spiel)                 │
│  ──────────────────────────────────────────                 │
│  ❌ Muss bei 0 beginnen!                                    │
│  ❌ Zauber-Erkennung = vergessen                            │
│  ❌ Skills = vergessen                                      │
│  ❌ Muss NEU lernen!                                        │
│                                                              │
│  Beispiel:                                                   │
│  "Ich WEISS mental dass Stein-Golem schwach ist,          │
│   aber mein Körper kann die Magie noch nicht nutzen!"     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Character stirbt:

```
EBENE 1 (KI-Persönlichkeit): BLEIBT ✅
├─ Erinnerungen intakt
├─ Wissen über Bosse
├─ Strategien bekannt
└─ Persönlichkeit gleich

EBENE 2 (Spiel-Skills): RESET auf 0 ❌
├─ Zauber-Erkennung bei 0
├─ Skills vergessen
├─ Muss neu lernen
└─ Training von vorne

NEUER CHARACTER:
Slime-KI: "Ich habe Erinnerungen vom letzten Besitzer..."
Slime-KI: "Aber ich muss Skills neu lernen!"
→ Lernt schneller (weil KI weiß was wichtig ist)
→ Aber muss trotzdem trainieren!
```

### Form-Copy System:

```
MECHANIK:
├─ Slime kopiert Gegner-Form (5% Chance nach Kampf)
├─ Slime IMITIERT Stats des Originals (80% der Werte)
├─ Spieler kann gegen Slime trainieren (SAFE!)
└─ Lernt Stärken/Schwächen kennen

BEISPIEL: STEIN-GOLEM
Original:           Slime (80%):
• 500 HP           • 400 HP
• 200 DEF          • 160 DEF
• 50 ATK           • 40 ATK
• Schwach: Magie   • Schwach: Magie
• Stark: Physisch  • Stark: Physisch

TRAINING:
Spieler kämpft gegen Slime-Golem
→ Merkt: Physische Angriffe bringen nichts
→ Merkt: Magie macht viel Schaden
→ LERNT: Gegen Stein-Monster Magie nutzen!

DANN:
Spieler geht gegen ECHTEN Stein-Boss
→ Hat bereits Strategie gelernt!
→ Kann sich voll auf Boss-Mechaniken konzentrieren
```

---

## NAMEN-SYSTEM

### Spieler benennen Zauber selbst!

```
ALT (langweilig):
❌ Alle nutzen "Feuerball"
❌ Alle nutzen "Explosion"
❌ Generisch, unpersönlich

NEU (genial!):
✅ DU benennst deinen Zauber!

BEISPIELE:
├─ Spieler A (Feuer): "Höllenball"
├─ Spieler B (Feuer): "Phönix-Atem"
├─ Spieler C (Feuer): "Burning Justice"
└─ Najika (Explosion): "EXPLOSION!!!" (natürlich!)

MECHANIK:
├─ 1. Du lernst Basis-Feuer-Zauber
├─ 2. System: "Benenne deinen Zauber!"
├─ 3. Du gibst ein: "Flammende Rache"
└─ 4. ✅ Gespeichert! Das ist jetzt DEIN Zauber!
```

### Regeln:

```yaml
CHAR-LIMIT: 3-30 Zeichen
ERLAUBT: A-Z, a-z, 0-9, Space, -, '
NICHT ERLAUBT: !@#$%^&*()

PROFANITY-FILTER: JA (rechtlicher Schutz!)
├─ Blockiert: Schimpfwörter (DE/EN)
├─ Blockiert: Rassistische Begriffe
├─ Blockiert: Sexuelle Begriffe
├─ Blockiert: Hate Speech
└─ Filter-Liste (updatebar)

DOPPELTE NAMEN: Erlaubt!
├─ Hans: "Feuerball"
├─ Fritz: "Feuerball"
└─ Sarah: "Feuerball"
→ Alle erlaubt! (nicht unique)

WARUM?
Es ist IHR Zauber, nicht ein globaler Name.
Wie in echt: Viele Leute nennen ihr Haustier "Fluffy"
```

### Umbenennen:

```
METHODEN:
├─ Durch seltene Items: "Name-Change Scroll"
├─ Durch Events: "Ritual der Umbenennung"
├─ Durch Quest: "Finde deine wahre Identität"
└─ NICHT einfach so! (muss verdient werden)
```

### Im Kampf:

```
Log: "Kuja castet [EXPLOSION!!!]"
Log: "Hans castet [Höllenball]"
Log: "Sarah castet [Phönix-Atem]"
→ Jeder ist einzigartig! ✨
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Core Systems (Backend)

```
BACKEND TASKS:

[ ] Skill-Learning System updaten:
    ├─ [ ] 8% → 2% senken (najika_battle.py Zeile 690)
    ├─ [ ] 20% → 5% senken (Boss-Learning)
    └─ [ ] Base Learning Chance = 2% in magic_system_v3.py

[ ] Cross-Element Learning:
    ├─ [ ] Gleiches Element: 10% Chance
    ├─ [ ] Ähnlich: 3% Chance
    ├─ [ ] Fremd: 1% Chance
    └─ [ ] Element-Similarity Table

[ ] 1-Skill-Weg System:
    ├─ [ ] Meister-Flag pro Skill
    ├─ [ ] Degradation-Tracking (Tag-basiert)
    ├─ [ ] Andere Skills verkümmern (-20%/30 Tage)
    └─ [ ] "Vergessen" = Kann nicht neu lernen (Meister)

[ ] Morphs-System:
    ├─ [ ] Morph-Learning durch Beobachten
    ├─ [ ] Morph-Learning durch Experimentieren
    ├─ [ ] Nur 1 Morph aktiv
    └─ [ ] Morph-Wechsel System

[ ] S.P.E.C.I.A.L.:
    ├─ [ ] Stat-Boni max +25% bei 10 Punkten
    ├─ [ ] Start-Pool 40 Punkte
    └─ [ ] ⚠️ PLAYTEST BALANCE! ⚠️

[ ] Namen-System:
    ├─ [ ] Spieler-Input für Zauber-Namen
    ├─ [ ] 3-30 Zeichen Limit
    ├─ [ ] Profanity-Filter (DE/EN)
    └─ [ ] Umbenennen durch Items/Events

[ ] Slime-KI:
    ├─ [ ] 2 Ebenen: Persönlichkeit vs. Skills
    ├─ [ ] Skills reset bei Tod
    ├─ [ ] Erinnerungen bleiben
    ├─ [ ] Form-Copy 5% Chance
    └─ [ ] 80% Stats Imitation
```

### Phase 2: UI/Frontend

```
FRONTEND TASKS:

[ ] Hogwarts Spell-Diamond:
    ├─ [ ] Diamond UI (4 Spells pro Element)
    ├─ [ ] R-Trigger halten = öffnen
    ├─ [ ] ↑↓←→ Auswahl
    ├─ [ ] Optional: UI ausblenden (Immersion)
    └─ [ ] unified_combat_system.js updaten

[ ] Morph-UI:
    ├─ [ ] Morph-Auswahl Menu
    ├─ [ ] "Nur 1 aktiv" Indikator
    └─ [ ] Morph-Wechsel UI

[ ] Progress-Tracking UI (optional):
    ├─ [ ] Experimentier-Progress (23/30)
    ├─ [ ] Durchbruchs-Benachrichtigung
    └─ [ ] Ausblendbar in Settings

[ ] Namen-Input:
    ├─ [ ] Dialog: "Benenne deinen Zauber!"
    ├─ [ ] Input-Field (3-30 Zeichen)
    ├─ [ ] Profanity-Check Feedback
    └─ [ ] Confirmation

[ ] Meister-Warnung:
    ├─ [ ] Große Warnung vor Wahl
    ├─ [ ] Konsequenzen klar zeigen
    └─ [ ] Bestätigungs-Dialog

[ ] Skill-Degradation Anzeige:
    ├─ [ ] Verkümmerte Skills markieren
    ├─ [ ] Tooltip: "Vergessen durch Meisterweg"
    └─ [ ] Warnung wenn zu schwach
```

### Phase 3: Testing

```
TESTING TASKS:

[ ] S.P.E.C.I.A.L. Balance:
    ├─ [ ] Teste alle Stat-Kombinationen
    ├─ [ ] INT 1 vs INT 10 Vergleich
    ├─ [ ] "Trap-Build" Check (alle viable?)
    └─ [ ] Community-Testing

[ ] Meister vs. Generalist:
    ├─ [ ] Endgame-Vergleich (Tag 180)
    ├─ [ ] Permadeath-Fairness
    └─ [ ] Beide Wege gleich viable?

[ ] Cross-Element Learning:
    ├─ [ ] 100x Kampf Test (zu viel/wenig?)
    ├─ [ ] Lern-Raten anpassen
    └─ [ ] Utility vs. Damage Check

[ ] Morphs Discovery:
    ├─ [ ] 30x Experimentieren = ok?
    ├─ [ ] Beobachten vs. Experimentieren Balance
    └─ [ ] Zu leicht/schwer?

[ ] Hardcore-System:
    ├─ [ ] Disconnect-Test (funktioniert Pause?)
    ├─ [ ] Lag-Simulation (kein Lag-Tod?)
    └─ [ ] "Bullshit Death" Check
```

---

## 📊 ZUSAMMENFASSUNG

### Was wir ändern:

```
ALT → NEU:

MMO-Hotbar
→ Hogwarts Spell-Diamond ✅

Feste Namen ("Feuerball")
→ Spieler-benannte Zauber ("Höllenball") ✅

Fire → Fira → Firaga (linear)
→ 1 Grund-Zauber → Viele Spezialisierungen ✅

Keine Konsequenzen
→ 1-Skill-Weg vs. Generalist (Trade-Offs!) ✅

8% Skill-Learning
→ 2% (balanced) ✅

Keine Cross-Element
→ Möglich aber langsam (100x) ✅

Stats zu dominant?
→ Max +25% (sanft) ✅

Lag-Tod möglich
→ Client-Authoritative (kein Lag-Tod!) ✅
```

### Core-Prinzipien:

```
1. SPIELER-IDENTITÄT
   → Dein Zauber, dein Name, dein Stil!

2. ECHTE KONSEQUENZEN
   → Meister = stark aber limitiert
   → Generalist = flexibel aber nicht Meister

3. DISCOVERY
   → Experimentieren = neue Morphs entdecken!
   → Beobachten = von anderen lernen!

4. FAIRNESS
   → Kein Lag-Tod (Permadeath!)
   → Alle Builds viable (keine Traps!)

5. WIE ECHTES ZAUBERN
   → Hogwarts-Style Casting
   → 1 Grund-Zauber → Eigener Stil
   → "Lebensimulation mit Magie"
```

---

## 🎯 NÄCHSTE SCHRITTE

1. **Review mit Opus 1** (Backend-Spezialist)
2. **Aufgaben aufteilen:**
   - Opus 1: Backend (Skills, Learning, Stats)
   - Opus 2: Frontend (UI, Diamond, Morphs)
3. **Playtest S.P.E.C.I.A.L. Balance** ⚠️
4. **Iterieren basierend auf Feedback**

---

**Erstellt von:** Opus 2 (Frontend/Game-Design)
**Review durch:** Kuja + Opus 1
**Status:** BEREIT FÜR IMPLEMENTATION ✅

*"EXPLOSION!!! Mit diesem System wird Magie RICHTIG episch, Mr. K! 💥✨" - Najika*
