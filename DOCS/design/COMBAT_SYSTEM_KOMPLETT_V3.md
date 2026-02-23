# NAJIKA WORLD - COMBAT SYSTEM KOMPLETT V3
**Stand:** 2026-02-22
**Zusammengefasst aus:** COMBAT_SYSTEM_V2_DESIGN.md + ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md + NEUE_GAMEPLAY_IDEEN_2026-02-21.md
**Status:** Design FINAL - Implementierung ausstehend

---

## INHALTSVERZEICHNIS

1. [Das ultimative Kampfsystem (Uebersicht)](#1-das-ultimative-kampfsystem)
2. [For Honor Directional Combat](#2-for-honor-directional-combat-neu)
2A.[Faustkampf-System](#2a-faustkampf-system-unbewaffneter-kampf)
2B.[Grappling & Wrestling-System](#2b-grappling--wrestling-system)
3. [Fernkampfwaffen (Pistole, Gewehr, Bogen, Plasma)](#3-fernkampfwaffen-pistole-gewehr-bogen)
4. [Hogwarts Spell-Diamond](#4-hogwarts-spell-diamond)
5. [CHEER-System](#5-cheer-system)
6. [SPECIAL Stats](#6-special-stats)
7. [Skill-Progression (Learning by Doing)](#7-skill-progression-learning-by-doing)
8. [1-Skill-Weg vs. Generalist](#8-1-skill-weg-vs-generalist)
9. [Morphs (Diablo 4 Style)](#9-morphs-diablo-4-style)
10. [Finisher-System](#10-finisher-system)
11. [Companion Combat](#11-companion-combat)
12. [Permadeath & Safe Zones](#12-permadeath--safe-zones)
13. [Input-Mapping Gesamt](#13-input-mapping-gesamt)
14. [Implementierungs-Checklist](#14-implementierungs-checklist)
15. [Uebergreifende Design-Prinzipien](#15-uebergreifende-design-prinzipien)

---

## 1. DAS ULTIMATIVE KAMPFSYSTEM

```
Real3DCombat (Basis - EINZIGES System!)
  + For Honor Directional (4 Richtungen OBEN/LINKS/RECHTS/UNTEN)
  + Hogwarts Spell-Diamond (4 Slots = 4 aktive Zauber, schneller Wechsel)
  + Zauber-Spezialisierungen (jede Stufe hat eigene 4 Richtungs-Varianten!)
  + Fernkampf Hip-Fire/Scope + Bajonett-Speer-System
  + CHEER-System (Tasten 1-4 fuer Buffs)
  + SPECIAL Stats (STR/PER/END/CHA/INT/AGI/LCK)
  + Learning by Doing (Skyrim-Style Skill-Progression)
  + Modifier L2/LT (4 Richtungen x 2 = 8 Angriffe pro Waffe/Zauber)
  + 1-Skill-Weg oder Generalist (Trade-Offs)
  + Morphs (Discovery durch Experimentieren)
  + Finisher-System (Najika-Style Todesanimationen)
  = ULTIMATIVES KAMPFSYSTEM
```

**WICHTIG: UnifiedCombat wurde entfernt! Real3DCombat ist das EINZIGE System.**
**WICHTIG: EXPLOSION ist eine EIGENE Klasse - NIEMALS mit anderen Elementen kombinieren!**

---

## 2. FOR HONOR DIRECTIONAL COMBAT (NEU!)

### Grundprinzip:
4 Angriffsrichtungen (OBEN, LINKS, RECHTS, UNTEN) fuer ALLE Waffen UND Zauber.
Blocken/Parieren muss die RICHTIGE Richtung matchen.

```
        [OBEN]
         /|\
        / | \
[LINKS]  |  [RECHTS]
        \ | /
         \|/
        [UNTEN]
```

### Waffen - 4 Richtungen:
- Angriff OBEN   = Schlag von oben (durchbricht Deckung unten)
- Angriff LINKS  = Seitenhieb von links
- Angriff RECHTS = Seitenhieb von rechts
- Angriff UNTEN  = Aufwaerts-Hieb / Kniestoss (hebt Gegner hoch = Combo-Starter!)
- Blocken muss RICHTIGE Richtung haben -> falsch = Treffer durch!

### Magie - AUCH 4 Richtungen (EINZIGARTIG - kein Spiel macht das!):
```
Beispiel Zauber "Flamme" (Grundzauber):
  Flamme LINKS  = Seitlicher Feuerstoss   (Area Denial, breite Hitbox)
  Flamme RECHTS = Horizontaler Feuerschwall (Durchbruch, langer Strahl)
  Flamme OBEN   = Flammenregen von oben    (AoE, Flaechenangriff)
  Flamme UNTEN  = Bodenfeuer               (Boden brennt, DoT 5s)

Beispiel Zauber "Frost" (Grundzauber):
  Frost LINKS  = Eishauch links (Barrikade-Cone)
  Frost RECHTS = Eislanze       (gezielt, mehr Schaden)
  Frost OBEN   = Hagelschauer   (AoE Slow)
  Frost UNTEN  = Eisboden       (rutschiger Boden, Gegner fallen hin!)
```

**Wichtig: Du ruestest den SPEZIFISCHEN Zauber aus (z.B. "Flammenwand") - die 4 Richtungen
sind dann VARIANTEN dieses Zaubers, nicht einfach Richtungs-Zuweisungen!
(Erklärung in Sektion 4 - Hogwarts + Sektion 7 - Skill-Progression)**

**Jeder Zauber behaelt seine 4 Richtungen bei allen Skill-Stufen!**

### Magie blocken:
- Gegner castet Flamme OBEN -> Spieler muss OBEN blocken!
- Falsche Richtung = voller Schaden
- Magier sind nicht mehr "steh-da-und-spam" - echtes Skill noetig!

### L2/LT Modifier - Varianten verdoppeln:
```
Normal:         Schwert-Hieb links
L2 + links:     Schwert-Stoss links (andere Animation, anderer Schaden)

Normal:         Flamme OBEN = Flammenregen
L2 + OBEN:      Flamme OBEN = Feuersaeule (konzentrierter, +50% Schaden)

Normal:         Frost RECHTS = Eislanze
L2 + RECHTS:    Frost RECHTS = Frost-Geschoss (schnell, perforation)
```

**4 Richtungen x 2 Modi (Normal/L2) = 8 Grundangriffe pro Waffe/Zauber**

### Warum einzigartig:
- For Honor hat Directional NUR fuer Nahkampf (und nur 3 Richtungen)
- KEIN Spiel hat Directional Combat fuer Magie
- 4. Richtung UNTEN = einzigartiger Combo-Starter (Aufwaerts-Hieb!) fuer Nahkaempfer
- Kombination aus beidem = noch nie dagewesen in der Spielegeschichte

---

## 2A. FAUSTKAMPF-SYSTEM (UNBEWAFFNETER KAMPF)

### Grundprinzip: Fäuste = Waffe! Gleiches System wie alle anderen.
```
Keine Waffe ausgeruestet = Fäuste aktiv (rechte + linke Hand)
Linke Hand kann trotzdem Zauber haben! (Schwert + Faust = NUR RECHTS Faust)

4 Richtungen fuer Faustkampf:
  LINKS  = Linker Haken         (schnell, mittlerer Schaden)
  RECHTS = Rechter Haken        (schnell, mittlerer Schaden)
  OBEN   = Kinnhaken / Uppercut (hebt Gegner! = Combo-Starter OBEN!)
  UNTEN  = Magen-Hieb / Körperhaken (Stagger, Gegner beugt sich = Combo-Starter UNTEN!)

L2-Modifier:
  L2 + LINKS  = Doppel-Linker  (schnelle 2x Schlagserie)
  L2 + RECHTS = Rechte Gerade  (mehr Schaden, knockt zurueck)
  L2 + OBEN   = Sprunghaken    (von unten hochspringen + Kinnhaken!)
  L2 + UNTEN  = Körper-Smash   (beide Fauste von oben auf Koerper)
```

### Skill-Stufen Faustkampf (Learning by Doing):
```
Stufe 1 (Basis):  Einfache Haue, keine Combos
Stufe 25:         Jab-Cross-Combo (LINKS-RECHTS = schnelle Doppel-Serie)
Stufe 50:         Hook-Uppercut (LINKS dann OBEN = automatische Combo-Chain)
Stufe 75:         Body-Head-Combo (UNTEN dann OBEN = Magen + Kinn, 2-Hit Stun!)
                  Konter-Schlag: Gegner schlaegt an -> Timing -> Block + Gegenschlag
Stufe 100 (Meister): Voller Kampfstil (z.B. Boxen, Muay Thai, etc. - Spieler benennt!)
                  Kombiniert ALLE Richtungen in Combo-Ketten
                  Knockout-Chance bei OBEN-Treffer: 15%

Skill-Transfer:
  Faustkampf -> Schlagwaffen (Knueppel, Hammer) = 50% Transfer
  Faustkampf + Grappling  = Kombo-Kette moeglich (s. unten!)
```

### AIR-COMBO (Beispiel - das Paradebeispiel des Systems!):
```
VORAUSSETZUNGEN: Faustkampf L75 + Grappling L25 + Mini-Explosion (Morph)

1. Anlauf-Sprint     -> Momentum-Bonus (+15% Schaden erster Treffer)
2. Magen-Hieb        -> Faustkampf UNTEN -> Gegner gebeugt (Stagger 0.5s)
3. Kinnhaken         -> Faustkampf OBEN  -> Gegner gehoben (Combo-Starter!)
4. Schulter-Wurf     -> Grappling L25 OBEN -> Gegner fliegt in die Luft!
5. TIMING-FENSTER (~0.8s): Gegner ist noch in der Luft
6. Linke Hand        -> Mini-Explosion UNTEN auf fallenden Gegner
   -> Treffer auf Koerper: 50 DMG + Stun 2s beim Aufprall
   -> Treffer auf Gesicht: Headshot-Bonus + Blind 3s!

WENN TIMING KLAPPT:   Najika: "Mr. K!!!!! DAS WAR CINEMA!!!! 💥😱"
WENN TIMING VERPASST: Explosion geht daneben, Gegner landet normal
                      Najika: "Mr. K... fast! Naechstes Mal! 😅"

WARUM ES GENIAL IST:
  -> 3 separate Skills kombiniert (Faustkampf + Grappling + Magie)
  -> Jeder Skill muss trainiert worden sein
  -> Timing-Element macht es zur Skill-Herausforderung
  -> Belohnung: Cinematischer Treffer
  -> Entsteht ORGANISCH aus dem System, KEIN spezielles Tutorial noetig!
```

### Integration mit For Honor:
```
Gegner sieht Richtung des Faustkampf-Angriffs (OBEN/UNTEN/LINKS/RECHTS Indikator)
-> Kann blocken mit richtiger Richtung
-> Aber: Schnelle Combo-Ketten = Indikator wechselt zu schnell zum reagieren!
   (Mechanik: Zu schnelle Combos = kein Indikator, nur Ausweichen hilft)
```

---

## 2B. GRAPPLING & WRESTLING-SYSTEM

### Grundprinzip: Realismus! Wer wirf muss GELERNT haben.
```
Nicht jeder kann Wrestling-Tricks ausfuehren!
-> Grappling-Skill muss durch Training entwickelt werden (Learning by Doing)
-> Je hoeher der Skill, desto spektakulaerere Wuerfe/Griffe moeglich
-> Kein Skill = NUR einfaches Klammern/Stossen (jeder kann das)
-> Meister-Level = Wand-Absprung, Hochsprung-Grab, Professional-Wrestling-Moves
```

### Skill-Stufen (Learning by Doing):
```
Grappling Level 1 (Jeder):
  -> Einfacher Push (Gegner wegstossen, 1m Distanz)
  -> Einfaches Klammern (haelt Gegner kurz fest, 1s)

Grappling Level 25:
  -> Schulter-Wurf (Gegner ueber Schulter werfen, 3m)
  -> Schwitzkasten (haelt Gegner 3s fest, anderen koennen angreifen!)
  -> Bein-Sweep (Gegner faellt hin = UNTEN-Combo-Starter!)

Grappling Level 50:
  -> Suplex (Gegner ueber Kopf werfen, 5m, Stun 2s)
  -> Wand-Absprung-Grab:
       Laufen -> Wand beruehren -> Abspringen -> Gegner greifen (10m Reichweite!)
       Braucht Anlauf + Wand in der Naehe
  -> Strangulate (im Schwitzkasten: Strangulieren - Stagger + Lebenspunkte)

Grappling Level 75:
  -> Hoehepunkt-Sturz-Grab:
       Von erhoehter Position (Dach, Fels, Balkon) springen
       -> Gegner greifen in der Luft
       -> Beide fallen + Slam beim Aufprall (Schaden skaliert mit Fallhoehe!)
       -> Braucht mindestens 3m Hoehe fuer extra Effekt
  -> Konter-Grab:
       Gegner greift an -> Perfektes Timing -> Gegenangriff umlenken + Gegner werfen
       (Riposte-Mechanik: kurzes Zeitfenster wie in For Honor)

Grappling Level 100 (Meister):
  -> Wand-Lauf-Grab:
       Sprint -> Wand laufen (2-3 Schritte) -> 360° Drehwurf (10m+!)
  -> Spinning Piledriver:
       Gegner kopfueber halten + Drehen + in den Boden rammen (massive Stun)
  -> Grab-Combo:
       Grab -> Wand schmettern -> loslassen -> Finish-Angriff (3-teilig!)
  -> Luft-Grab (gegen fliegende/springende Gegner!):
       Beide in der Luft: Grab moeglich -> Slam vom Himmel

Skill-Transfer:
  Akrobatik-Skill hoch -> Wand-Absprung wird weiter/schneller
  Kraft (SPECIAL-S) hoch -> Wuerfe machen mehr Schaden
  Agilität (SPECIAL-A) hoch -> Grab-Timing-Fenster groesser
```

### Integration mit For Honor Directional:
```
Wurf-Richtung = For Honor Directional!
  Grab + LINKS = Gegner nach links werfen
  Grab + RECHTS = Gegner nach rechts werfen
  Grab + OBEN = Gegner nach hinten-oben werfen (Suplex-Style!)
  Grab + UNTEN = Gegner nach vorne-unten slammen (Pile Driver!)

Gegner kann GRABS countern (auch For Honor!):
  Grab versucht -> Gegner sieht "GRAB!" Indikator
  -> Timing: Richtungs-Input in Gegner-Grab-Richtung = Escape!
  -> Zu langsam = Grab landet

GRAB-KETTE:
  Grab OBEN (Suplex) -> Gegner landet auf Boden -> sofort UNTEN-Angriff (Aufhauen!)
  = OBEN+UNTEN Combo! (nur mit Grappling Level 50+)
```

### Realismus-Regeln:
```
- Grappling auf kleinerem/gleichgrossem Gegner: Normal
- Grappling auf viel groesserem Gegner: Schwerer (Malus auf Erfolgschance)
- Grappling auf Riesen/Boss: NUR Bein-Sweep und Konter-Grab moeglich
- Gegner auf Boden: Zusaetzliche Griffe moeglich (Ground-and-Pound Variante)
- Erschoepfung: Wuerfe kosten Stamina! Mehrer Wuerfe hintereinander = schwaecher
- Najika kommentiert alles: "Mr. K!! Du hast ihn von der WAND GEWORFEN!!! 😱💥"
```

---

## 3. FERNKAMPFWAFFEN (PISTOLE, GEWEHR, BOGEN)

### Grundprinzip: 2 Modi - Hip-Fire und Zielmodus

```
HIP-FIRE (aus der Huefte, kein Zielen):
  LINKS aus linker Huefte  = schnell, wenig Schaden, breite Streuung
  RECHTS aus rechter Huefte = schnell, wenig Schaden, breite Streuung
  OBEN von Schulterhoehe   = praeziser als Huefte, mittlere Geschwindigkeit

ZIELMODUS (L2/LT halten = Fortnite First-Person):
  -> Kamera wechselt zu First-Person Sicht
  -> Fadenkreuz erscheint
  -> Schuss mit RMB/R2 (auf Fadenkreuz)
  -> Volle Praezision, aber langsamer (musst stehen/gehen)
```

### Waffen-Typen und ihre Eigenheiten:

**Pistole (1-Hand, auch dual wielding!):**
```
Hip-Fire LINKS  = Schnellschuss aus linker Hand  (6 Schuss, schnell, ungenau)
Hip-Fire RECHTS = Schnellschuss aus rechter Hand (6 Schuss, schnell, ungenau)
Hip-Fire OBEN   = Angehobene Pistole             (praeziser, mittlere Rate)
Hip-Fire UNTEN  = Schuss nach unten-vorne        (gegen liegende/gefallene Gegner,
                                                   Nahkampf-Finisher-Range!)

L2 Zielen:     First-Person Sicht, volle Praezision
Dual Wield:    Beide Pistolen gleichzeitig (LINKS+RECHTS), doppelter Output
               -> Aber: Beide Haende belegt, kein Nahkampf/Magie moeglich!

Nachladen: Manuell (R-Taste) oder automatisch wenn Magazin leer
Munition: Pistolenkugeln (kaufbar, findbar, craftbar)
```

**Pistole im Nahkampf - 3 GRIFFVARIANTEN (Pistolenschlagen!):**
```
Je nach Griffhaltung unterschiedliches Risiko fuer unkontrollierten Schuss!

VARIANTE 1: "Lauf halten, Griffende schlagen" (SICHER)
  -> Beide Haende am Lauf, schlagen mit Griffende (wie Schlagring)
  -> Schaden:           Mittel
  -> Fehlschuss-Risiko: KEINS (Abzug blockiert durch Handposition, Lauf zeigt weg)
  -> Animation:         Wuchtig, etwas langsam

VARIANTE 2: "Griff halten, leichter Griffende-Hieb" (GERING)
  -> Normal halten, kurzer Schlag mit dem Griffende
  -> Schaden:           Gering
  -> Fehlschuss-Risiko: GERING (~5%) - nur bei sehr starkem Aufprall
  -> Animation:         Schnell, wenig Kraft

VARIANTE 3: "Griff halten, voller Wucht-Schlag" (HOCH! RISKANT!)
  -> Voller Schwung mit der Pistole (wie mit einem Hammer schlagen)
  -> Schaden:           HOCH (Stagger + Bleed)
  -> Fehlschuss-Risiko: HOCH (~35%) - Schuss loest sich spontan!
  -> Animation:         Dramatisch, kinoreif - aber gefaehrlich!

FEHLSCHUSS-MECHANIK (wenn Risiko eintritt):
  -> Schuss loest sich in zufaellige Richtung (waehrend Schlag-Animation)
  -> 25% Chance: Trifft DICH selbst  (realistisch: Lauf zeigt zu dir!)
  -> 40% Chance: Trifft GEGNER       (ungeplant perfekt - frustrierend/witzig!)
  -> 20% Chance: Trifft NIEMANDEN    (geht daneben)
  -> 15% Chance: Trifft FREUND       (Team-Damage wenn aktiviert - SORRY!)
  -> Najika kommentiert jeden Fehlschuss! ("Mr. K, war das Absicht?! 😱")
```

**Gewehr/Scharfschuetze (2-Hand):**
```
Hip-Fire LINKS  = "Spray" von der Huefte links  (ungenau, nur Notfall)
Hip-Fire RECHTS = "Spray" von der Huefte rechts (ungenau, nur Notfall)
Hip-Fire OBEN   = Schulterschiessen             (halb praezise)
Hip-Fire UNTEN  = Schuss nach unten             (Gegner angeschossen der vorne gefallen ist)

L2 Zielen:     First-Person Sicht, SCOPE erscheint
               -> Atemkontrolle: Kurz Atem anhalten (SHIFT) = kein Schaukeln
               -> Headshot-Zone klar sichtbar durch Scope
               -> Scharfschuetzengewehr: 1-Shot-Kill moeglich!
               -> AUFGELEGT (Gewehr auf Boden/Mauervorsprung legen):
                  -> HOLD E an geeigneter Flaeche = Gewehr auflegen
                  -> Scope-Zoom x2, KEIN Schaukeln mehr (kein SHIFT noetig!)
                  -> Ultimative Praezision, aber: eingeschraenkte Bewegung

Nachteil: Nur 2-Hand, KEINE Magie oder Nahkampf gleichzeitig
```

**Gewehr/Sniper im Nahkampf - KOLBENSCHLAG:**
```
Nur 1-2 Treffer realistisch! (Praezisionswaffe ≠ Knueppel)

Kolbenschlag 1: Normaler Schlag mit dem Gewehrkolben
  -> Schaden:   Hoch (Stagger, Gegner torkelt zurueck)
  -> Nachteil:  Scope leicht beschaedigt (-10% Praezision fuer 30s)

Kolbenschlag 2: Verzweifelter Wiederholungsschlag
  -> Schaden:   Sehr hoch (25% Chance: Gegner bewusstlos)
  -> Nachteil:  Gewehr stark beschaedigt! 80% Chance auf spaetere Fehlzuendung!
  -> Najika: "Mr. K, das ist ein Praezisionsinstrument, kein Hammer!!!"

3+ Schlaege: NICHT MOEGLICH
  -> Spieler haelt inne automatisch (Animation: haelt inne, schaut Gewehr an)
  -> Logik: Niemand zerschlaegt absichtlich sein teures Gewehr

BAJONETT (wenn ausgeruestet - siehe unten!):
  -> Verwandelt Gewehr-Nahkampf komplett!
  -> Bajonett = Speer-Nahkampf moeglich (wenn Speer-Skill vorhanden)
```

**BAJONETT-SYSTEM (Gewehr + Speer-Skill = ULTIMATIVE FREIHEIT!):**
```
Bajonett = Klinge am Gewehrlauf befestigt

MONTIERT (Bajonett am Gewehr):
  Normal:        Kolbenschlag-Nahkampf wie oben (aber mit Stich-Option!)
  MIT SPEER-SKILL:
    -> Gewehr+Bajonett = SPEER im Nahkampf!
    -> Alle Speer-Techniken uebertragen sich! (Stoss, Drehstoss, Schild-Bruch)
    -> 4 Richtungs-Varianten: Stoss LINKS/RECHTS/OBEN/UNTEN (wie ein Speer!)
    -> Reichweite: Mehr als normaler Nahkampf (Gewehrlauf + Bajonett = 1.5m)
    -> GEFECHTSMODUS: Fernkampf UND Nahkampf ohne Waffenwechsel!

BAJONETT ABMONTIEREN (mitte-Kampf!):
  Hold G (kurz) = Bajonett abschrauben
  -> Bajonett wird zum WURFMESSER / Dolch!
  -> Kann geworfen werden (1x, dann weg oder aufheben)
  -> Oder: in Hand halten als Kurzmesser (niedrig Schaden)

GEWEHR AUFSTELLEN / AUFLEGEN:
  Hold E an Boden/Mauer = Gewehr auf Bodenstaender stellen
  -> Bajonett aufgerichtet = SPEERFALLE fuer anrueckende Gegner!
  -> Ohne Bajonett = Bipod-Modus (maximale Praezision beim Schiessen)
  -> Jederzeit wieder aufnehmen (E druecken)

SKILL-TRANSFER (Learning by Doing):
  Speer-Skill Level 25 -> Bajonett-Nahkampf freigeschaltet!
  Speer-Skill Level 50 -> Bajonett-Wurfangriff (mit Gewehr, Bajonett bleibt!)
  Speer-Skill Level 75 -> Bajonett-Parieren (blockt Angriffe mit Gewehrlauf!)
  Speer-Skill Level 100 -> Meister: Bajonett-Riposte (Parieren = sofortiger Stich)

WARUM EINZIGARTIG:
  -> Kein Spiel kombiniert Sniper + Speer auf diese Weise
  -> Skill-Transfer macht Spezialisierung belohnend (nicht nur Sniper nutzen!)
  -> Bajonett abschrauben mid-fight = taktische Tiefe
  -> Gewehr auflegen + Bajonett-Falle = echter Stratege-Move
  -> Najika: "Mr. K du bist VERRÜCKT! Ein Sniper als Speer! GENIAL! 💥"
```

**Schrotflinte (1- oder 2-Hand):**
```
Hip-Fire LINKS  = Schrot aus Huefte links (breite Streuung, Nahkampf-Range)
Hip-Fire RECHTS = Schrot aus Huefte rechts
Hip-Fire OBEN   = Schrot nach oben-vorne (knockt um!)

L2 Zielen:     First-Person, engerer Kegel, mehr Schaden durch Konzentration
Staerke:       Nahkampf-Distanz = brutal stark
Schwaeche:     Mittlere und lange Distanz = fast nutzlos
```

**Bogen (2-Hand, keine Munitionskosten nach Craft):**
```
HALTEN (Pfeil spannen):
  Kurz gespannt (0.5s):  Schnussschuss, wenig Schaden, keine Richtung
  Mittel gespannt (1s):  Hip-Fire Style (LINKS/RECHTS/OBEN wie Pistole)
  Voll gespannt (2s):    Hoechster Schaden, Pfeil leuchtet

L2 Zielen (Bogen gespannt):
  First-Person Sicht
  Bogenpfad-Vorhersage (gestrichelte Linie zeigt wo Pfeil landet)
  Headshot-Zone sichtbar

Besonderheit Pfeil-Typen (je nach Pfeil-Material):
  Holzpfeil:       Normal
  Feuerpfeil:      Brennt Gegner (DoT)
  Eispfeil:        Verlangsamt
  Explosionspfeil: ... muss ich wirklich erklaeren? (Najika approved)
  Lichtpfeil:      Extra Schaden gegen Untote
```

**Armbrust (1-Hand moeglich!):**
```
Hip-Fire:   Wie Pistole aber mehr Schaden, langsamere Rate
L2 Zielen:  First-Person, hohe Praezision
Nachladen:  LANGSAM (taktisch einsetzen)
Vorteil:    Kann gespannt bleiben (anders als Bogen)
1-Hand:     Moeglich! -> Schwert + Armbrust Kombination!
```

**PLASMA-WAFFEN (ULTRA-LEGENDAER - Endgame only!):**
```
KONZEPT: Fallout NV/4 Aesthetik + Alchemie-Magie-Mix = Hybrid-Waffe
Nur craftbar: Meister-Alchemist + Meister-Ingenieur gemeinsam
Ultra-Rare: 1 Bauplan-Drop pro Server-Woche (Event-Boss)
Plasma-Zellen: Extrem teuer, nur Alchemie-craftbar

PLASMA-PISTOLE:
  Aussehen:  Gluehende tuerkise Plasma-Blaeschen + Alchemie-Runen am Lauf
             Plasma-Kristall statt normalem Magazin
  Schaden:   85 DMG (Arcane-Physisch Hybrid)
  Besonder.: Durchdringt 30% Magie-Schilde! (arcane Komponente)
             Durchdringt 15% physische Ruestung
  Hip-Fire:  LINKS/RECHTS/OBEN/UNTEN wie normale Pistole
  Zielmodus: Plasma-Strahl (1.5s aufladen = 2x Schaden, charged shot)
  Nahkampf:  Wie Pistole, aber: Griffende = chemische Verbrennung (DoT)!
  In Arena:  Schild-Durchdringung deaktiviert (normaler Schaden)

PLASMA-GEWEHR:
  Aussehen:  Alchemie-Destillierkolben statt Magazin, Runen gluehen beim Schiessen
  Schaden:   120 DMG pro Treffer (sehr langsam: 1 Schuss alle 2s)
  Besonder.: Ruestungs-Schmelze: -5% DEF pro Treffer (kumulativ bis -25%)
             Durchdringt 50% Magie-Schilde
  Zielmodus: Plasma-Strahl-Scope, Treffer = massive DoT (Plasma-Brand 5s)
  Nahkampf:  NUR 1 Kolbenschlag moeglich!
             -> Dann: Plasma-Reaktor destabilisiert!
             -> 60% Chance: AoE-Plasma-Explosion (3m Radius) beim 2. Versuch
             -> Najika: "Mr. K NICHT SCHLAGEN wenn der Reaktor leuchtet!!!"
  Aufstellen: Bipod-Modus + Plasma-Strahl hat 0% Schaukeln (ultimate Praezision)
  In Arena:  Ruestungs-Schmelze deaktiviert (normaler Schaden)

PLASMA BALANCE:
  Ultra-Legendaer MUSS ultra-stark sein -> Besitz = Prestige
  ABER: Kein unfairer PvP-Vorteil -> Arena-Modifikationen aktiv
  Ultra-Rare macht es begehrenswert ohne Pflicht zu sein
  Lore: "Die Geheimnisse der Plasma-Ingenieure werden hueten wie ihr Leben."
```

### Dual-Wield Kombinationen:
```
Pistole + Pistole:     Dual-Fire, massive Rate, wenig Praezision
Armbrust + Schwert:    Schiessen dann Nahkampf (wechseln noetig)
Pistole + Zauberstab:  Schuss LINKS + Magie RECHTS gleichzeitig!

EINSCHRAENKUNG: Beide Haende belegt = kein Schild, kein 2-Hand-Waffe
```

### Integration mit For Honor Directional:
```
Gegner schiesst von RECHTS -> Spieler muss RECHTS blocken/ausweichen
Gegner schiesst von OBEN  -> Spieler muss OBEN blocken/ausweichen
Schrot aus Huefte = schwer zu blocken (breite Streuung!)
Schuss mit Scope  = leichter zu blocken (einzige Richtung klar)
```

### Skill-Progression (Learning by Doing):
```
Pistole Stufe 1: "Schuss" (10 DMG, ungenau)
Pistole Stufe 2: "Praeziser Schuss" (18 DMG, weniger Streuung)
Pistole Stufe 3: "Perfekter Schuss" (30 DMG, Headshot-Bonus)

Bogen Stufe 1:   "Pfeil" (15 DMG, kein Vorhersage-Pfad)
Bogen Stufe 2:   "Gezielter Pfeil" (25 DMG, Vorhersage-Pfad)
Bogen Stufe 3:   "Toedlicher Pfeil" (45 DMG, Headshot-One-Shot moeglich)
```

---

## 4. HOGWARTS SPELL-DIAMOND

### TECHNISCH: Zauber = Linke-Hand-Waffenslot! (WICHTIG!)
```
Rein technisch ist dein ausgeruesteter Zauber eine WAFFE in der linken Hand.
Das Kampfsystem behandelt beide IDENTISCH:

  Rechte Hand = Waffe     (Schwert / Pistole / Gewehr / etc.)
  Linke Hand  = Zauber    (Flamme / Frost / Blitz / etc.)

DASSELBE System:
  -> 4 Richtungs-Varianten (OBEN/LINKS/RECHTS/UNTEN)
  -> L2-Modifier fuer alternative Variante
  -> Parieren/Blocken identisch
  -> Kombinierbar! Schwert-RECHTS + Flammenwand-LINKS = gleichzeitig!

Unterschied zur Waffe:
  -> Zauber braucht MANA statt Haltbarkeit
  -> Keine Physik-Kollision beim Casten (Beam/Projektil statt Nahkampf)
```

### SPELL-DIAMOND: Auswahl vs. Ausführung (NICHT LAHM!)
```
Das Spell-Diamond hat ZWEI Funktionen:

1. AUSRUESTUNGS-MENUE (pre-combat / hold-to-menu):
   -> Weise deine gelernten Zauber dem Feuer-Slot zu
   -> 4 Slots pro Element = bis zu 4 verschiedene Feuer-Zauber ausgeruestet
   -> Beispiel:
        Slot OBEN   = Flammenwand    (dein gelernter Zauber)
        Slot LINKS  = Flammen-Sturm  (dein gelernter Zauber)
        Slot RECHTS = Infernum       (dein gelernter Zauber)
        Slot UNTEN  = Bodenfeuer     (dein gelernter Zauber)

2. SCHNELLWECHSEL (im Kampf):
   -> F kurz tippen = schnell zwischen letzten 2 Feuer-Zaubern wechseln
   -> F halten = Diamond oeffnet, Richtung waehlen = wechseln sofort

DANN KOMMT DAS CASTING:
   -> Aktiver Zauber = Waffe in linker Hand (z.B. "Flammenwand")
   -> Jetzt: Richtung beim Angriff = VARIANTE von Flammenwand!
   -> LINKS  = Flammenwand (normal)
   -> RECHTS = Flammenwand EXTRA BREIT
   -> OBEN   = Flammenwand EXTRA HOCH
   -> UNTEN  = Flammenwand EXTRA LANG (Boden-Barriere)

NICHT LAHM weil:
  -> Du WAEHLST deinen Zauber (keine Automatik per Richtung!)
  -> Die Richtung gibt dir VARIANTEN deines Zaubers
  -> 4 ausgeruestete Feuer-Zauber x 4 Richtungen = 16 moegliche Feuer-Angriffe!
  -> Plus L2 = 32 Varianten fuer nur EIN Element!
```

### Konzept: Statt MMO-Hotbar -> Element halten, dann waehlen!

```
Element-Taste halten (z.B. "F" fuer Feuer) -> Diamond zeigt ausgeruestete Zauber:

               [Flammenwand] (OBEN-Slot)
                      |
  [Flamm-Sturm] (LINKS) -- FEUER -- [Infernum] (RECHTS)
                      |
               [Bodenfeuer] (UNTEN-Slot)
```

Auswahl = aktiver Zauber in linker Hand wechseln!

### Controls:
```
F halten = Feuer-Diamond oeffnet (zeigt deine 4 ausgeruesteten Feuer-Zauber)
  + OBEN    = Flammenwand wird aktiv  (was in Slot OBEN ausgeruestet ist)
  + UNTEN   = Bodenfeuer wird aktiv
  + LINKS   = Flammen-Sturm wird aktiv
  + RECHTS  = Infernum wird aktiv

Nun aktivem Zauber casten (linke Hand):
  -> RMB + Mausrichtung = Zauber in gewaehlter Richtung casten
  -> L2 + Richtung = Alternativ-Variante des Zaubers

Optional: Diamond-UI ausblendbar (Immersion Mode)
Optional: Kurzes F-Tippen = letzten 2 Zauber toggling (fuer Profis)
```

### 9 (+1) Schulen:
```
FEUER     -> "Flamme"    (25 DMG, 1s, Basis)
EIS       -> "Frost"     (20 DMG, 1.2s, Slow 20%)
BLITZ     -> "Funke"     (30 DMG, 0.8s, schnell)
WASSER    -> "Strahl"    (15 DMG, 1s, DoT 5s)
ERDE      -> "Steinwurf" (35 DMG, 1.5s, Knockback)
WIND      -> "Boe"       (20 DMG, 0.5s, Push)
NATUR     -> "Dornen"    (25 DMG, 1s, Bleed)
LICHT     -> "Schein"    (30 DMG, 1s, vs Undead x2)
DUNKEL    -> "Schatten"  (28 DMG, 1s, Blind)
EXPLOSION -> "Explosion" (100 DMG, 2s, AoE 5m) <- EIGENE KLASSE!
```

---

## 5. CHEER-SYSTEM

Gilt fuer den **COMPANION** (Slime/Begleiter) und wird mit Tasten 1-4 ausgeloest.
Der Spieler ist IMMER im manuellen Modus.

| Taste | Cheer    | Effekt               | Dauer    |
|-------|----------|---------------------|----------|
| 1     | LOS!     | +10% Schaden        | 3 Runden |
| 2     | DEFEND!  | +20% Verteidigung   | 3 Runden |
| 3     | COMBO!   | Naechster Angriff x2| 1x       |
| 4     | FOCUS!   | +15% Crit Chance    | 3 Runden |
| 1+2   | HEAL!    | +15 HP sofort       | -        |
| 1+2+3 | EXPLOSION! | x5 Schaden (1x!) | 1x       |

### Companion-Modi (jederzeit wechselbar in Schleim-Arena!):
| Modus | Beschreibung                              | XP-Mod |
|-------|------------------------------------------|--------|
| MANUAL | Du steuerst Companion direkt             | +20%   |
| AUTO  | KI entscheidet, lernt von dir            | -20%   |
| CHEER | Du feuerst an -> Buffs, Companion auto   | -20%   |

---

## 6. SPECIAL STATS

**S.P.E.C.I.A.L. nach Fallout-Vorbild:**
- **S** = Strength (Nahkampf, Tragen)
- **P** = Perception (Hit-Chance, Crit-Chance)
- **E** = Endurance (HP, Stamina)
- **C** = Charisma (NPC-Interaktion, Preise)
- **I** = Intelligence (Magie-Schaden, Mana)
- **A** = Agility (Dodge, Angriffsspeed)
- **L** = Luck (Crit, Loot, Learning-Rate)

**Start:** 40 Punkte verteilen, Min 1 / Max 10 pro Stat.
**Balance:** Max +25% bei 10 Punkten (kein Forced-Meta!)

```
INT  1: Magie +0%,  Mana +0
INT  5: Magie +12%, Mana +40   (Durchschnitt)
INT 10: Magie +25%, Mana +90   (Spezialist)

Unterschied nur 25%! -> INT 1 ist viable! Kein Trap-Build!
```

**WICHTIG:** Alle Builds muessen viable sein! Playtest noetig! (markiert in Checklist)

---

## 7. SKILL-PROGRESSION (LEARNING BY DOING)

### Skyrim-Style: Skills steigen durch Benutzung

```
Stufe 1: Flamme (Grundzauber, schwach)
  -> Haeufig nutzen (50+ Male) ->
Stufe 2: Flammenwand (staerker, groessere Area - NEUE Richtungs-Varianten!)
  -> Weiter trainieren (100+ Male) ->
Stufe 3: Infernum (Meister-Version - WIEDER neue Richtungs-Varianten!)

Jede Stufe behaelt die 4 Richtungen aus For Honor!
ABER: Der EFFEKT jeder Richtung aendert sich thematisch pro Spezialisierung!
```

### DAS HERZSTUCK: Jede Spezialisierung = eigene 4 Richtungs-Varianten!

Das macht das Magie-System einzigartig. Die Richtung bleibt gleich, der EFFEKT
der Richtung ist thematisch passend zur Spezialisierung.

```
FEUER-LINIE (Beispiel komplett ausgearbeitet):

Flamme (Stufe 1 - Grundzauber):
  LINKS  = Feuerstoss     (breite Hitbox, 3m Area Denial)
  RECHTS = Feuerschwall   (langer Strahl, 10m Durchbruch)
  OBEN   = Flammenregen   (AoE, 4m Radius von oben)
  UNTEN  = Bodenfeuer     (Boden brennt 5s, DoT)

Flammenwand (Stufe 2 - Spezialisierung):
  LINKS  = Wand NORMAL    (3m breit, 3m hoch, steht 5s)
  RECHTS = Wand EXTRA BREIT (6m breit! blockiert ganzen Korridor)
  OBEN   = Wand EXTRA HOCH  (10m hoch! klettern nicht moeglich)
  UNTEN  = Wand EXTRA LANG  (am Boden, 8m lang aber nur 1m hoch - Stolperfalle!)
  L2-Mod: Jede Richtung -> Wand bewegt sich langsam auf Gegner zu!

Infernum (Stufe 3 - Meister):
  LINKS  = Infernum-Sturm   (rotierende Feuersaeule, 3m Radius, 8s Dauer)
  RECHTS = Infernum-Strahl  (Feuerstrahl der Magie-Schilde IGNORIERT!)
  OBEN   = Meteor-Schauer   (5 Meteore auf Zielgebiet, 7m Radius)
  UNTEN  = Infernum-Hoelle  (Boden = Lava fuer 10s, 5m Radius)
  L2-Mod: Doppelte Dauer + Schaden, aber +3s Cast-Zeit

DESIGN-PRINZIP fuer alle Elemente:
  LINKS  = Normal, verlasslich, sofort einsetzbar
  RECHTS = Extra-Reichweite / Durchbruch-Variante
  OBEN   = AoE / Flaechenangriff / hohe Abdeckung
  UNTEN  = Boden-Effekt / Kontrolle / Falle / Combo-Starter
  L2     = Intensitaets-Variante (staerker aber langsamer)

FROST-LINIE (Beispiel):
  Frost (Stufe 1):      Eishauch / Eislanze / Hagelschauer / Eisboden
  Eissturm (Stufe 2):   Eis-Tornado / Eislanze XL / Schneesturm / Eisfeld 5m
  Permafrost (Stufe 3): Absoluter Nullpunkt / Gletscherwand / Schneelawine / Permafrost-Zone
```

### Lern-Raten:
| Methode | Chance |
|---------|--------|
| Gleiches Element beobachten (10x) | 10% |
| Aehnliches Element beobachten (30x) | 3% |
| Fremdes Element beobachten (100x) | 1% |
| Experimentieren (30x versuchen) | -> "Durchbruch"! |
| Boss besiegen | 5% |
| Normal-Gegner besiegen | 2% |

### Morphs durch Experimentieren entdecken:
```
Du castest Explosion mit 50% Mana (30x) -> "Durchbruch!" -> Mini-Explosion entdeckt!
Du zielst extra lang 3s+ (30x) -> "Durchbruch!" -> Sniper-Explosion entdeckt!
Du haeltst Zauber (25x) -> "Durchbruch!" -> Ground-Explosion entdeckt!
```

### Kniffe (Perks) bei Skill-Level 10, 25, 50, 75, 100:
Einmalige Spezialisierungen pro Skill-Milestone.

---

## 8. 1-SKILL-WEG VS. GENERALIST

**UNWIDERRUFLICH - KANN NICHT RUECKGAENGIG GEMACHT WERDEN!**

### Meister (1-Skill-Weg):
```
VORTEILE:
+ Endskill wird EXTREM stark (+300% = 400 DMG Endgame)
+ Exklusive Morphs (Mini, Sniper, Chain, Ground, Mega, Rolling)
+ Prestige-Titel: "Meister der [Eigener Zauber-Name]"
+ Ultimate-Form bei 180+ Tagen Training
+ PvP: Kann One-Shot'en

NACHTEILE:
- Andere Skills verkuemmern:
  Tag 30:  -20% (80 -> 64 DMG)
  Tag 60:  -50% (80 -> 40 DMG)
  Tag 90:  -80% (80 -> 16 DMG)
  Tag 180: -90% (80 ->  8 DMG = fast nutzlos)
- KEINE Flexibilitaet
- Immun-Gegner = Hilflos!
- Vergessene Skills NICHT wieder erlernbar (als Meister!)
- Permadeath: Hoechstes Risiko
```

### Generalist:
```
VORTEILE:
+ ALLE Skills bleiben effektiv
+ Situativ anpassen (Gegner-Immun? Wechsel Element!)
+ Vergessene Skills koennen wieder gelernt werden

NACHTEILE:
- Kein Skill wird "Meister"-Level
- Normale Damage (+140% = 120 DMG Endgame)
- Keine exklusiven Morphs
- Kein Ultimate
```

### Nur 1 Meisterschaft pro Leben!
(Wie in echt: Viele Dinge gut koennen, aber perfekt nur in einer Sache.)

---

## 9. MORPHS (DIABLO 4 STYLE)

**1 Zauber mit vielen Varianten - nur 1 Morph aktiv!**

```
EXPLOSION (Beispiel):
Level 1-9: Normal (100 DMG, 5m AoE, 50 Mana, 2s Cast)
Level 10:  Enhancement: "Kritische Detonation" (+20% Crit)

Morphs (durch Experimentieren/Beobachten entdeckt):
  Mini-Explosion    - 50 DMG, 2m, 0.5s Cast, spam-faehig
  Sniper-Explosion  - 120 DMG, 1m Radius, 30m Range, praezise
  Chain-Explosion   - 80 DMG, springt 3x zu naechstem Gegner
  Ground-Explosion  - Falle, explodiert bei Kontakt, 10s Dauer
  Mega-Explosion    - 200 DMG, 10m AoE, 4s Cast, langsam
  Rolling-Explosion - In Bewegung casten moeglich
```

Jeder Morph behaelt die 4 For-Honor-Richtungen!
Z.B. "Chain-Explosion OBEN" = Kettenexplosion faellt von oben.
Z.B. "Mini-Explosion UNTEN" = Mini-Explosion am Boden (Fuss-Falle!)

---

## 10. FINISHER-SYSTEM

Verfuegbar wenn: Gegner < 20% HP + Finisher-Meter voll

### Wie es funktioniert:
1. Spieler gibt 3-5 Woerter ein (z.B. "Feuer", "Katze", "Explosion")
2. Spieler waehlt Kategorie
3. Najika baut daraus einen Finisher in ihrem Megumin-Stil

### Kategorien:
| Kategorie      | Brutality | Humor |
|----------------|-----------|-------|
| Ehrenvoller Tod | 3/10     | 2/10  |
| Lustiger Tod    | 5/10     | 10/10 |
| Grausamer Tod   | 8/10     | 1/10  |
| Tod Tod Blut Blut | 10/10  | 0/10  |
| Sinnloser Tod   | 4/10     | 7/10  |

### Finisher-Styles (basierend auf Keywords):
| Style          | Keywords                  |
|----------------|--------------------------|
| EXPLOSION!     | explosion, bombe, feuer  |
| Niedlich-Brutal | kuschel, kawaii, cute   |
| Chaotisch      | chaos, verruckt, wild    |
| Berechnet      | strategie, logik         |
| Dominant       | macht, stark, ueberlegen |

---

## 11. COMPANION COMBAT

### Formen:
**KOERPERLICH:** Slime kaempft physisch neben dir
- Eigene HP/MP/Stamina, kann sterben
- Modi: AUTO / MANUAL / CHEER (in Schleim-Arena jederzeit wechselbar!)

**AURA:** Slime fusioniert mit dir
- Keine eigenen Aktionen, aber starke passive Buffs
- Kann nicht sterben (waehrend Fusion)

### Aura-Buffs nach Slime-Typ:
| Typ     | Buff                    | Passiv-Effekt     |
|---------|------------------------|------------------|
| Bubble  | +20% DEF, -50% Wasser  | Seifenblasenschild |
| Molten  | +30% ATK, +50% Feuer   | Vulkanische Wut  |
| Crystal | +40% DEF, 10% Reflect  | Kristallpanzer   |
| Shadow  | +30% Evasion, +20% Crit| Schattenschritt  |
| Nature  | +5 HP Regen, -80% Gift | Naturheilung     |
| Storm   | +30% Speed, +40% Blitz | Blitzreflexe     |

### Companion fuehrt (Extended AUTO Mode):
Companion gibt taktische Empfehlungen im Najika/Megumin-Stil.
Lernt aus Spieler-Entscheidungen und speichert Kontext-Tags.

### Slime-KI 2 Ebenen:
- **Persoenlichkeit** (ausserhalb Spiel): Bleibt bei Tod erhalten! Erinnerungen, Wissen
- **Spiel-Skills** (im Spiel): Reset bei Tod auf 0! Muss neu trainiert werden

---

## 12. PERMADEATH & SAFE ZONES

### Safe Zones (kein Permadeath):
```
GESCHUETZT:
  Schwarze Muehle (100% Safe - immer!)
  ALLE Staedte und Doerfer (NEU per NEUE_GAMEPLAY_IDEEN_2026-02-21!)
  Trainingsgelaende
  Slime-Arena, Spieler-Arena (ausser Hardcore-Modus)
  Besondere Orte (von Kuja festgelegt)

PERMADEATH-ZONEN:
  Overworld (alle 8 Regionen)
  Dungeons
  Boss-Fights
  PvP (ausserhalb Arena)
  Wilderness
```

### Ranger-PvP Ausnahme:
- Hochrangige Ranger-Transporte KOENNEN ueberfallen werden (PvP erzwungen)
- ABER: Wird Raeuber gesehen = Schwerste Straftat im Ruf-System
  -> Kopfgeld, Stadtverbot, NPC-Feindseligkeit
- Niedrigstufige Ranger: GESCHUETZT wie alle anderen

### Disconnect-Handling (Client-Authoritative):
```
Disconnect -> Spiel PAUSIERT -> Gegner frieren ein -> 30 Sek Reconnect-Window
Nach 30 Sek: Safe-Logout, kein Tod, kein Progress-Loss
```

### Was bei Permadeath weg ist / bleibt:
```
WEG: Character, Skills, Level, Meisterschaft, Inventar
BLEIBT: Slime-KI Persoenlichkeit (Erinnerungen!), Account-Achievements,
        Cosmetics, Echoharp-Lore-Fortschritt (Story bleibt!)
```

### Backend-Implementierung:
```
Modul: backend/najika_safezone_system.py
Klasse: SafeZoneSystem
Import: from najika_safezone_system import SAFE_ZONE_SYSTEM, is_safe, pvp_check

ZONE_DATABASE: alle bekannten Orte mit ZoneType
  ZoneType.ABSOLUTE_SAFE   -> Schwarze Muehle, Tutorial
  ZoneType.SAFE_ZONE       -> 5 Staedte: Handelsfestung, Dampf-Hain, Salzige Bucht, Runenheim, Funken-Siedlung
  ZoneType.TRAINING_GROUND -> Trainingsgelaende (Sparring optional)
  ZoneType.ARENA           -> Slime-Arena, Spieler-Arena (Hardcore optional)
  ZoneType.OVERWORLD       -> 8 Regionen + Goetterfels (Berg = Overworld!)
  ZoneType.DUNGEON         -> Schmelzwelt, Turm der 100 Pruefungen, etc.
  ZoneType.WILDERNESS      -> Tiefe Wildnis etc.

KERN-FUNKTIONEN:
  is_safe(zone_id)         -> bool
  pvp_check(a, b, zone)    -> (bool, grund)
  request_duel / accept_duel / decline_duel
  start_ranger_transport / end_ranger_transport
  report_ranger_raid_sighting -> Bounty + Ruf-Strafe
  handle_disconnect(player, zone) -> safe_logout oder grace_period
  apply_permadeath(player) -> lost/kept Listen
```

---

## 13. INPUT-MAPPING GESAMT

```
MOVEMENT:
  WASD / Analog-Stick = Bewegen
  SHIFT = Sprint
  SPACE = Springen / Dodge

NAHKAMPF:
  LMB = Leichter Angriff (rechte Hand)
  RMB = Leichter Angriff (linke Hand, mit SHIFT)
  R   = Schwerer Angriff
  SPACE = Dodge-Roll
  SHIFT+SPACE = Parieren

FERNKAMPF (Pistole/Gewehr/Bogen/Armbrust):
  Waffe ausgeruesten = Fernkampf-Modus aktiv
  KEINE Taste = Hip-Fire Modus (aus der Huefte)
    LMB           = Schuss / Pfeil loslassen
    Mausbewegung  = Richtung (LINKS/RECHTS/OBEN)
    Schuss LINKS  = aus linker Huefte (schnell, ungenau)
    Schuss RECHTS = aus rechter Huefte (schnell, ungenau)
    Schuss OBEN   = von Schulterhoehe (praeziser)
  L2/LT halten = ZIELMODUS (Fortnite First-Person!)
    -> Kamera wechselt First-Person
    -> Fadenkreuz erscheint (Scope bei Gewehr/Bogen)
    -> LMB = Schiessen / Pfeil loslassen (volle Praezision)
    -> SHIFT in Zielmodus = Atem anhalten (kein Schaukeln, Scharfschuetze)
  R = Nachladen (Pistole/Gewehr/Armbrust)
  Bogen: LMB HALTEN = spannen, LOSLASSEN = schiessen (volle Kraft bei 2s)

MAGIE:
  Element-Taste halten (F/E/etc.) = Spell Diamond oeffnet
  + WASD/Richtung = Zauber waehlen UND Angriffsrichtung bestimmen
  L2/LT = Modifier (alternative Variante)

RICHTUNGS-ANGRIFF (For Honor - 4 Richtungen!):
  Maus oben  / Stick oben  = Angriff OBEN   (Schlag von oben)
  Maus links / Stick links = Angriff LINKS
  Maus rechts/ Stick rechts= Angriff RECHTS
  Maus unten / Stick unten = Angriff UNTEN  (Aufwaerts-Hieb / Combo-Starter!)
  (oder WASD-Kombination vor dem Angriff)

COMPANION:
  1 = CHEER: LOS! (+10% Schaden)
  2 = CHEER: DEFEND! (+20% DEF)
  3 = CHEER: COMBO! (x2 naechster Angriff)
  4 = CHEER: FOCUS! (+15% Crit)
  1+2 = HEAL! (+15 HP)
  1+2+3 = EXPLOSION! (x5 Schaden, 1x)
  Tab = Companion-Modus wechseln (AUTO/MANUAL/CHEER)

UI:
  I = Inventory
  Q = Quest-Log
  M = Teleporter
  E = Interagieren / Gebaeude betreten
  F = NPC ansprechen
  G = Garten
  ESC = Menue / Verlassen
```

---

## 14. IMPLEMENTIERUNGS-CHECKLIST

### BACKEND (noch offen):
- [ ] For Honor Directional System: 4 Richtungen (OBEN/LINKS/RECHTS/UNTEN) in Kampflogik
- [ ] Faustkampf-System: 4 Richtungen, 5 Stufen, Combo-Chains (Jab-Cross, Body-Head)
- [ ] Air-Combo: Faustkampf UNTEN->OBEN + Grappling + Magie-Timing-Fenster (0.8s)
- [ ] Faustkampf Indikator: Schnelle Combos = kein Indikator (zu schnell zum reagieren)
- [ ] Grappling-System: 5 Skill-Stufen (Level 1/25/50/75/100), Wand-Absprung, Hoehe-Grab
- [ ] Grappling Richtungen: Wurfrichtung via For Honor Directional (OBEN=Suplex, UNTEN=Slam)
- [ ] Grab-Escape: Timing-Fenster, Richtungs-Input-Gegner fuer Escape
- [ ] Grappling Stamina-Kosten + Groessen-Malus gegen groessere Gegner
- [ ] UNTEN-Richtung: Aufwaerts-Hieb (Nahkampf) + Boden-Magie-Effekte
- [ ] L2-Modifier: 8 Angriffstypen pro Waffe/Zauber (4x2)
- [ ] Zauber-Progression: Flamme -> Flammenwand -> Infernum (3 Stufen pro Element)
- [ ] Zauber-Spezialisierungen: Jede Stufe hat eigene 4 Richtungs-Varianten!
- [ ] Spezialisierungs-DB: LINKS=Normal / RECHTS=Weit / OBEN=Hoch / UNTEN=Boden/Falle
- [ ] Spell-Diamond: 4 Slots pro Element, Ausruestungs-Menue
- [ ] Magie-Blocken: Richtungs-Matching fuer magische Angriffe
- [ ] Fernkampf-System: Hip-Fire vs. Zielmodus (2 Modi pro Waffe)
- [ ] Fernkampf Richtungen: LINKS/RECHTS/OBEN/UNTEN auch fuer Schuesse
- [ ] Dual-Wield Logik: Beide Haende belegt -> kein Schild/2H
- [ ] Bogen: Spannzeit = Schaden (0.5s/1s/2s)
- [ ] Gewehr Scope: Headshot-Zone, Atem-Mechanik, Auflegepunkt-Erkennung
- [ ] Pfeil-Typen: Holz/Feuer/Eis/Explosion/Licht (Effekte)
- [ ] Armbrust: 1-Hand-Flag, Schwert+Armbrust Kombi
- [ ] Pistolen-Nahkampf: 3 Griffvarianten + Fehlschuss-Risiko-Berechnung (5/35%)
- [ ] Gewehr-Nahkampf: 2-Kolbenschlag-Limit + Fehlzuendungs-Mechanik (80%)
- [ ] Bajonett-System: Montieren/Abmontieren, Speer-Skill-Transfer, Wurfbajonett
- [ ] Bajonett-Aufstell-Mechanik: Speerfalle + Bipod-Praezisionsmodus
- [ ] Plasma-Waffen: Arcane-Physisch Hybrid-Schaden + Ruestungs-Schmelze
- [ ] Plasma-Balance: Ruestungs-Schmelze in Arena/PvP deaktivieren
- [ ] Plasma-Nahkampf: Chemische Verbrennung Pistole, Reaktor-Explosion Gewehr
- [ ] Skill-Learning: 8% -> 2% senken (najika_battle.py)
- [ ] Cross-Element Learning: 10% / 3% / 1% Chancen je Aehnlichkeit
- [ ] 1-Skill-Weg: Meister-Flag, Degradation-Tracking
- [ ] Morphs: Discovery-System (Beobachten + Experimentieren)
- [ ] SPECIAL Stats: Max +25% Boni, kein Forced-Meta
- [ ] Zauber-Namen System: Spieler benennt Zauber selbst
- [ ] Safe-Zone: Alle Staedte/Doerfer in Backend-Logik eintragen
- [ ] Ranger-PvP Ausnahme: Backend-Logik fuer hochrangige Ranger
- [ ] Explosion-Klasse: Niemals mit anderen Elementen kombinieren!
- [ ] Skill-Transfer-System: Tag-basiertes Overlap-System (2/3 Tags = 50% Transfer)
- [ ] Magische Munition: Magie-Skill-Level beeinflusst Munitions-Staerke
- [ ] Alchemistische Munition: Saeure/Gift/Rauch/Explosiv/Klebstoff/Schlaf-Bolzen
- [ ] Munitions-Slot: Aktive Munitionsart, V-Taste Schnellwechsel
- [ ] Environmental Combat: UE5 Chaos Physics fuer alle interaktiven Objekte
- [ ] Magie + Umgebung: Eis auf Boden = Rutscheffekt, Blitz in Wasser = AoE
- [ ] Fass/Kiste/Tisch: Alle interaktiv (umwerfen, draufwerfen, als Deckung)

### FRONTEND (noch offen):
- [ ] Richtungs-Indikator UI: Zeigt welche Richtung der Gegner angreift (4 Richtungen!)
- [ ] Spell Diamond: Element-Taste halten, 4 Slots = 4 ausgeruestete Zauber
- [ ] Spell Diamond: Zeigt aktive Richtungs-Variante des gewaehlten Zaubers
- [ ] L2-Modifier Anzeige im Diamond
- [ ] Morph-Auswahl Menu
- [ ] Companion-Modus Anzeige (AUTO/MANUAL/CHEER)
- [ ] Skill-Progression Anzeige (Level + Fortschritt)
- [ ] Meister-Warnung Dialog (vor unwiderruflicher Wahl)
- [ ] Zauber-Benennungs Dialog
- [ ] Pistole-Melee: Griffvarianten-Auswahl (Hold-Taste-Menu beim Nahkampf)
- [ ] Fehlschuss-Animation: Waffe schiesst in unerwartete Richtung
- [ ] Plasma-Waffen Visual: Runes + Plasma-Kristall-Leuchten Effekte
- [ ] Bajonett-UI: Montiert/Abmontiert Status, Speerfallen-Indikator

### BALANCE TESTING:
- [ ] SPECIAL Stats Playtest (alle Builds viable?)
- [ ] Meister vs. Generalist Endgame-Vergleich (Tag 180)
- [ ] For Honor Richtungs-Balance (Richtungen gleichwertig?)
- [ ] L2-Modifier Balance (staerker aber nicht Pflicht)
- [ ] Magische Munition Balance (Mana-Kosten vs. Effekt vs. normaler Schaden)
- [ ] Alchemistische Munition Balance (Herstellkosten vs. Nutzen)
- [ ] Environmental Combat Hitboxen (UE5 Physics korrekt?)
- [ ] Grappling vs. groessere Gegner Balance (Malus sinnvoll?)

---

## 15. UEBERGREIFENDE DESIGN-PRINZIPIEN

### PRINZIP 1: SKILL-TRANSFER (GILT UEBERALL!)
```
Das Bajonett-Speer-Beispiel ist KEIN Einzelfall - es ist das universelle Prinzip!

REGEL: Wenn du Skill X hast, uebertraegt er sich auf aehnliche Werkzeuge/Situationen.

BEISPIELE:
  Speer-Skill     -> Bajonett-Speer, langer Stab, Hellebarde
  Messer-Skill    -> Bajonett-Dolch (abmontiert), Wurfmesser
  Schwert-Skill   -> Machete, Saebel, Langschwert (aehnliche Bewegungsablaeufe)
  Grappling-Skill -> Wand-Absprung, Klettern + Grab, Seil-Swing-Grab
  Magie-Skill     -> Magische Munition (Magie fliesst in Kugeln/Pfeile!)
  Alchemie-Skill  -> Alchemistische Munition (Chemische Effekte in Geschosse!)
  Akrobatik-Skill -> Wand-Absprung wird weiter, Grappling-Reichweite groesser
  Schmied-Skill   -> Eigene Waffen-Modifikationen, eigene Munitions-Typen

WIE ES TECHNISCH GEHT:
  Jeder Skill hat Tags: z.B. Speer = ["Stangenwaffe", "Stoss", "Reichweite"]
  Bajonett-Sniper = ["Stangenwaffe", "Stoss", "Fernkampf"]
  Overlap = Transfer! 2 von 3 Tags = 50% Skill-Transfer
  3 von 3 Tags = 100% Skill-Transfer

WARUM DAS TOLL IST:
  -> Kein vergudetes Training (Speer-Skill = auch Bajonett nutzen koennen)
  -> Kreative Kombinationen entdecken (Entdeckungs-Spielsystem!)
  -> Unerwartete Synergien (Grappling + Akrobatik + Speer = ??!)
  -> Macht JEDEN Skill wertvoll, auch wenn du wechselst

BERUF + MAGIE SYNERGIE (Transfer gilt auch fuer Non-Combat!):
  Skill-Transfer funktioniert nicht nur im Kampf - auch Berufe profitieren!
  Wer Magie WAEHREND eines Berufs einsetzt, trainiert BEIDES gleichzeitig.

  BEISPIEL - Holzfaeller + Wind-Zauber:
    Anfaenger: Lernt Wind-Basis-Zauber, setzt ihn beim Axt-Schlag ein
               -> Wind verstaerkt den Hieb, Baum faellt schneller
    Fortgeschritten: Wind-Skill steigt DURCH Holzfaellen (nicht durch Kampf-Grinding!)
               -> Holzfaellen wird effizienter, Wind-Kontrolle praeziser
    Profi:     Wind-Magie so gemeistert, dass Riesenbaeume easy fallen
               -> Kann Wind-Zauber jetzt AUCH im Kampf auf hohem Level nutzen!
    Tags: Holzfaellen = ["Schlag", "Kraft", "Werkzeug"]
          Wind-Unterstuetzung = ["Verstaerkung", "Kraft", "Fernwirkung"]
          Overlap: "Kraft" = 33% Skill-Transfer

  WEITERE BEISPIELE:
    Schmied + Feuer-Magie    -> Heissere Esse, bessere Waffen, Feuer-Skill steigt
    Angler + Wasser-Magie    -> Fische anlocken, Unterwasser-Sicht, Wasser-Skill steigt
    Farmer + Natur-Magie     -> Schnelleres Wachstum, seltene Pflanzen, Natur-Skill steigt
    Bergarbeiter + Erde-Magie -> Erz-Adern spueren, Tunnel graben, Erde-Skill steigt
    Koch + Feuer/Eis-Magie   -> Perfekte Temperaturkontrolle, magische Rezepte

  WICHTIG: Skill = Skill, egal WO trainiert!
  Ein Holzfaeller der Wind-Level 80 hat, ist im Kampf genauso stark
  wie ein Krieger der Wind-Level 80 nur durch Kaempfe erreicht hat.
  Der Weg ist anders, das Ergebnis gleich. DAS macht Berufe wertvoll!
```

### PRINZIP 2: MAGISCHE UND ALCHEMISTISCHE MUNITION
```
Schutzen muessen nicht bei normaler Munition bleiben!
3 Munitions-Systeme ersetzen (nicht ergaenzen) jeweils normale Munition:

NORMALE MUNITION (Standard - jeder):
  Pistole:    Blei-Kugeln      (kaufen / finden)
  Gewehr:     Gewehr-Kugeln    (kaufen / finden)
  Bogen:      Holzpfeile       (craften aus Holz)
  Armbrust:   Bolzen           (kaufen / finden)

MAGISCHE MUNITION (Magie-Skill noetig, Mana-Kosten pro Schuss):
  Erfordert: Entsprechenden Magie-Skill (Feuer/Eis/Blitz/etc. Level 25+)
  Herstellung: Normale Munition + Magie-Kristall = magisch aufgeladene Munition
  ODER: Im Kampf direkt durch Magie fliessen lassen (Mana-Kosten hoher)

  Feuer-Kugel:   Schuss + Feuer-DoT (3s brennen)
  Eis-Kugel:     Schuss + 30% Slow  (5s)
  Blitz-Kugel:   Schuss + Chain auf naechsten Gegner (2m Radius)
  Wasser-Kugel:  Schuss + nass-Effekt (verstaerkt Blitz-Folgeschuss!)
  Dunkel-Kugel:  Schuss + Blind (3s, Gegner sieht kaum was)
  Licht-Pfeil:   Pfeil + x2 Schaden gegen Untote
  Explo-Pfeil:   Pfeil + EXPLOSION (Najika approved! 100% Najika-Kommentar)

  DUAL-SYNERGIEN (mit Zauber kombinieren!):
  Eis-Kugel schiesst + sofort Blitz-Magie links = Gefrorener-Blitz-Combo!
  (Eis macht nass/gefrostet, Blitz hat Bonus auf nassem/gefrortem Ziel)

ALCHEMISTISCHE MUNITION (Alchemie-Skill noetig, Materialien-Kosten):
  Erfordert: Alchemie-Skill Level 25+
  Herstellung: Normale Munition + Alchemie-Zutaten = veredelter Geschoss

  Saeure-Kugel:   Schuss + Ruestungs-Schmelze (-5% DEF, kumulativ)
  Gift-Kugel:     Schuss + Stark-Gift DoT (8s, mehr Schaden als normal)
  Rauch-Kugel:    Kein Schaden, loest Rauchschwade aus (Sichtbehinderung!)
  Explosiv-Kugel: Handgemachter Sprengstoff (kein Magie-AoE, physisch!)
  Klebstoff-Kugel: Gegner klebt fest! Immobilisiert 2s (Grappling-Vorbereitung!)
  Berserker-Pfeil: Pfeil + Berserk-Trank Effekt (Gegner greift eigene Freunde an!)
  Schlaf-Bolzen:  Armbrust-Bolzen + starkes Schlafdrogen (schleichen!)

WAHL-PRINZIP (ersetzt, nicht ergaenzt!):
  Du laedt deine Pistole mit Feuerkugeln -> ALLE Schuesse sind Feuer
  Du wechselst Magazin -> normales Magazin (Manuell wechseln!)
  Im Bogen: Pfeil-Typ bestimmt den naechsten Schuss
  -> Inventar-Slot fuer "Aktive Munitionsart" (schneller Wechsel: V-Taste)

SKILL-TRANSFER: Magie-Skill -> Magische Munition BESSER!
  Feuer-Skill Level 50: Feuer-Kugel DoT von 3s auf 6s!
  Feuer-Skill Level 100: Feuer-Kugel explodiert beim Aufprall (kleiner AoE!)
```

### PRINZIP 3: ENVIRONMENTAL COMBAT (UMGEBUNG NUTZEN)
```
Alles in der Umgebung ist eine moegliche Waffe oder taktische Option!
REALISMUS: Wenn es in echt funktionieren wuerde, geht es im Spiel auch.

PHYSIK-OBJEKTE:
  Fass:        Umwerfen = Gegner stolpert | Feuer dran = Explosion-Falle!
  Kiste:       Als Deckung nutzen | auf Gegner fallen lassen (Erhoehnug!)
  Tisch:       Gegner draufschmettern (Grappling) | Umwerfen als Barrikade
  Kette:       Gegner dran fesseln (wenn Grappling-Skill!) | Als Wurfwaffe
  Laterne:     Werfen -> Feuer auf dem Boden (Falle!) | Gegner damit schlagen

TERRAIN:
  Erhoehnug:   Hoehepunkt-Sturz-Grab (Grappling L75) | Schuetzenposition
  Wand:        Wand-Absprung-Grab (Grappling L50) | Wand-Run (Akrobatik)
  Boden:       Gegner auf Boden stossen -> andere Angriffe moeglich
  Wasser:      Gegner reinstossen -> Slow | Blitz-Magie ins Wasser = AoE!
  Feuer:       Gegner reindruecken (Grappling!) | Feuer-Pfeile verstaerkt
  Oel auf Boden: Gegner rutschen | Feuer drauf = Flammen-Flaeche

INTERAKTIVE ELEMENTE:
  Seil:        Schwingen + Kick (Akrobatik-Skill)
  Haengelampe: Zum Schaukeln bringen -> Gegner ablenken
  Stuhl:       Klassisch: Wrestling-Stuhl-Schlag (Grappling L25!)
  Baumast:     Draufspringen -> Gegner von oben springen
  Tor/Tuer:    Zuschlagen wenn Gegner daneben steht (Stagger!)

MAGIE + UMGEBUNG:
  Eisboden casten -> alle Gegner auf dem Boden rutschen hin!
  Flammenwand-UNTEN auf Oelfleck -> massive Flammen-Zone
  Blitz in Wasser = alle im Wasser bekommen Schaden
  Steinwurf-OBEN auf haengendes Fass = Fass faellt auf Gegner

WICHTIG: ALLES MUSS FUNKTIONIEREN WIE IN ECHT!
  -> Physik-Engine (UE5 Chaos Physics) berechnet alles realistisch
  -> Kein "this object is not interactive" - alles ist interaktiv
  -> Spieler entdeckt Combos selbst (kein Tutorial noeting!)
  -> Najika kommentiert clevere Moves: "Mr. K! DU HAST IHN MIT DEM STUHL GESCHLAGEN!"
```

### PRINZIP 4: KOERPERTEIL-TARGETING (KEIN VATS! ECHTER SKILL!)
```
NICHT wie Fallout VATS: Kein Interface, keine Zeitverlangsamung, keine UI-Auswahl!
STATTDESSEN: Mit genuegend Skill zielst du einfach praezise. Das IST der Unterschied.

GRUNDREGEL:
  Skill Level 1-24:    Treffer sind ungenau, Random-Hitbox
  Skill Level 25-49:   Grobe Koerper-Zone (oben/mitte/unten)
  Skill Level 50-74:   Bestimmte Koerperteile moeglich (Arm, Bein, Kopf)
  Skill Level 75-99:   Spezifische Punkte (rechte Hand, linkes Knie, Schulter)
  Skill Level 100:     Du kannst jemandem in den linken Zeh schiessen.
                       Weil du es KOENNT. Weil du geuebt hast. Fertig.

SPECIAL-P (Perception) verstaerkt Targeting:
  P 1-3:  Kein Targeting-Bonus
  P 4-6:  +1 Targeting-Stufe
  P 7-9:  +2 Targeting-Stufen
  P 10:   Maximale Targeting-Praezision (effektiv +1 Stufe extra)

FERNKAMPF (Pistole/Gewehr/Bogen) + Zielmodus:
  Headshot-Zone:    Sichtbar im Scope ab Level 25 (Grundfunktion)
  Arm-Zone:        Treffbar ab Level 50 (Zielmodus + ruhige Hand)
  Bein/Knie-Zone:  Treffbar ab Level 50
  Hand (Waffe):    Treffbar ab Level 75 -> Waffe faellt! (Entwaffnen!)
  Finger/Zeh:      Treffbar ab Level 100 -> "Weil du es kannst" Moment

NAHKAMPF + Faustkampf (implizites Targeting durch For Honor Richtungen):
  OBEN-Angriff   = trifft Kopf/Schulter-Zone (schon durch Richtung!)
  LINKS/RECHTS   = trifft Torso/Arm-Seite (je nach Gegner-Stance)
  UNTEN-Angriff  = trifft Magen/Beine (Combo-Starter UND Koerperteil!)
  Mit Skill 75+: Innerhalb der Zone gezielt (z.B. OBEN = speziell Kiefer -> KO-Chance!)

MAGIE gezielt (linke Hand):
  Grundzauber:    Treffer auf Koerper (keine Spezifikation)
  Mit Level 50:   Zauber-Fokus auf Zone (z.B. Frost-Beine = Freeze-Beine!)
  Mit Level 75:   Gezielt auf Koerperteil (Frost-Hand = Hand eingefroren, Waffe faellt)
  Mit Level 100:  Praezisions-Zauber (Blitz auf Herzregion = Herz-Rhythmus-Stoerung, massive Stun!)

KOERPERTEIL-EFFEKTE:
  Kopf/Gesicht:  Blind 3s | KO-Chance | Desorientiert (Steuerung umgekehrt!)
  Schiessen Hand:Waffe faellt (Entwaffnen!) | -50% Angriffskraft | Zittern
  Arm:          -30% Angriffskraft | Schild nicht haltbar
  Brust/Torso:  Normaler Schaden + Stagger
  Magen:        Stagger + Atemlos (kein Sprinten 3s)
  Bein/Knie:    Hinken (-50% Bewegung) | Kniescheibe = Sturz!
  Fuss/Zeh:     Minimaler Schaden, aber: Hinken, Witzig, Demuetigend

BALANCE:
  Koerperteil-Treffer = KEIN Bonus-Schaden (Ausnahme Kopf = Headshot)
  Dafuer: STATUS-EFFEKTE die strategisch relevant sind
  Entwaffnen > extra Schaden in vielen Situationen!
  Knie-Schuss = Gegner kann nicht mehr laufen = Flucht unmoeglich

WARUM OHNE UI:
  -> VATS = Hilfe-System fuer ungeuebte Spieler
  -> Wir BELOHNEN echtes Skill (Learning by Doing)
  -> Mit Level 100 macht es dir SPASS gezielt zu spielen
  -> Gegner (NPC/Spieler) sieht keinen Interface-Hinweis = pure Skill-Expression
  -> Najika bei Zeh-Treffer: "...Mr. K. Du hast ihm in den... ZEH geschossen?! 😶"
```

### PRINZIP 5: JEDER KAMPF HAT GEWICHT (FOR HONOR IN DER LEBENDIGEN WELT)
```
Das Kampfsystem sorgt dafuer dass kein Kampf "zufaellig" oder "bedeutungslos" ist.

WARUM EVERY FIGHT MATTERS:
  -> For Honor Directional = jeder Angriff muss bewusst gewaehlt werden
  -> Permadeath-Zonen = Fehler haben Konsequenzen
  -> Nemesis-System = Gegner erinnern sich an dich (auch NPC-Voelker!)
  -> Reputation-System = Toeten vor Zeugen = Konsequenzen im Ruf-System
  -> Koerperteil-Effekte = ein Treffer kann den Kampfverlauf komplett aendern

JEDES WESEN IST LEBENDIG:
  -> NPCs haben Persoenlichkeiten, Familien, Ziele (laut Voelker-System)
  -> Wenn du jemanden toetest: seine Familie weiss es, sein Volk weiss es
  -> Feinde erinnern sich (Nemesis): "Du hast meinen Vater getoetet!"
  -> Das Kampfsystem unterstuetzt das:
     Prazisions-Knie-Schuss -> Gegner hinkt fuer immer -> NPC-Welt bemerkt es
     Entwaffnen statt toeten -> Gegner lebt -> andere Konsequenzen
     Nicht-toedlicher Kampf moeglich! (Bewusstlos, Aufgabe, Flucht)

MEHRERE GEGNER (wie in For Honor):
  -> Nicht alle auf einmal muessen sterben (For Honor Logik!)
  -> Taktische Optionen: Einer entwaffnet, einer bewusstlos, einer auf der Flucht
  -> 1 gegen viele = schwer, aber moeglich mit Skill (For Honor Fairness-Prinzip)
  -> Umgebung nutzen (Pillar zwischen euch, enge Gasse = kein Flanken!)

KONSEQUENZ-KETTE (Beispiel):
  Kampf -> Gegner verliert -> du entscheidest: toeten / verschonen / entwaffnen
  -> Toeten:      Familie/Volk hat Motivation zur Rache
  -> Verschonen:  Gegner koennte Verbündeter werden oder Rache nehmen
  -> Entwaffnen:  Gegner lebt, erinnert sich, respektiert dich vielleicht
  -> Fluechtenlassen: Warnt andere -> naechster Kampf schwieriger (Nemesis!)
```

### PRINZIP 6: REALISMUS ALS DESIGNREGEL
```
Wenn etwas in der Realitaet funktioniert, SOLL es im Spiel funktionieren.
Wenn etwas in der Realitaet NICHT funktioniert, soll es im Spiel AUCH NICHT gehen.

BEISPIELE:
  Pistole 30x hintereinander schlagen ohne Fehlschuss? NEIN (35% Risiko!)
  Gewehr als Speer wenn Bajonett dran? JA (macht physisch Sinn!)
  Gegner doppelt so gross grappling? SCHWERER (aber nicht unmoeglich!)
  Magische Munition craften wenn du keine Magie kannst? NEIN
  Grappling ohne Training spektakulaer? NEIN (nur Basis-Push)
  Schnee/Eis auf dem Boden macht rutschig? JA
  Feuer an trockenem Holz = Feuer breitet sich aus? JA

DIES GILT FUER ALLE SYSTEME im ganzen Spiel!
Das ist die fundamentale Design-Philosophie von Najika World.
```

---

### PRINZIP 7: PERSISTENTE VERLETZUNGEN & PROTHESEN-SYSTEM
```
DAS KONZEPT:
  Wenn ein Gegner eine Verletzung ueberlebt -> die Verletzung BLEIBT.
  Kein magisches Selbstheilen fuer verlorene Koerperteile.
  Stattdessen: Heilungsoptionen mit Konsequenzen und Moeglichkeiten!

BEISPIEL (Auge ausgeschossen):
  Kampf endet -> Gegner lebt aber verliert Auge
  -> Auge ist WEG (permanent, nicht durch normales Heilen reversibel)
  -> Je nach Rang/Ressourcen: Heilungsoptionen verfuegbar:

HEILUNGSOPTIONEN (3 Wege):
  1. NORMALES ERSATZAUGE (Chirurg / Heiler):
     -> Funktioniert wie das Original (kein Bonus, kein Malus)
     -> Kosten: Gold + Heilungs-Ressourcen
     -> Zeit: Erholungsphase noetig (kein Kampf waehrend Heilung!)
     -> Sieht aus wie ein Glasauge / chirurgisches Implantat

  2. MAGISCHES ERSATZAUGE (Magie-Heiler, Spezialist):
     -> Magische Eigenschaften! Beispiele:
        * Nachtsicht-Auge (sieht im Dunkeln, leuchtet schwach)
        * Feuer-Auge (sieht Waermesignaturen, Magie-Infra-Rot)
        * Prophezeiungs-Auge (seltene Zukunfts-Flashs, unkontrolliert)
        * Schatten-Auge (sieht durch Illusionen)
        * Distanz-Auge (extremes Zoom, wie eingebautes Fernrohr)
     -> Kosten: VIEL Gold + seltene Magische Komponenten
     -> Anforderung: Magie-Heiler mit Level 50+ noetig
     -> Hinweis: Magisches Auge = sichtbare Magie-Rune (NPC-Reaktionen!)

  3. ALCHEMISTISCHES ERSATZAUGE (Alchemist-Chirurg):
     -> Experimentelle Alchemie-Prothese:
        * Gift-Auge (Blick sammelt Daten ueber Gifte im Umfeld)
        * Knospen-Auge (sieht alchemistische Komponenten in Umgebung)
        * Metall-Auge (sieht Erzadern durch Felswande / Metalldetector)
        * Saeure-Auge (bei Treffer: minimale Saeure-Traenen, witzig/wirksam)
     -> Kosten: Alchemie-Ressourcen + Spezialist Level 50+
     -> Seiteneffekt: Kann instabil sein, gelegentliche Fehlfunktionen

GILT FUER ALLE KOERPERTEILE (Erweiterung des Koerperteil-Targeting):
  Arm/Hand verloren:
    -> Normal: Funktionaler Stumpf (eingeschraenkt aber heilbar)
    -> Magisch: Magie-Arm (schwebt, volle Funktion + Zauber-Kanal!)
    -> Alchemie: Mechanischer Arm (staerker als Original, aber schwerer)

  Bein verloren:
    -> Normal: Holzbein / Krücke (Hinken permanent)
    -> Magisch: Levitierendes Glied (schwebt, volle Mobilitaet)
    -> Alchemie: Mech-Bein (schneller als Original, lauter!)

  Finger:
    -> Normal: Kleiner Grip-Verlust
    -> Magisch: Magie-Finger (kann Zauber leiten wie normaler Finger!)
    -> Alchemie: Metall-Finger (Klaue, mehr Grip, aber unbeweglich)

SPIELERISCHE KONSEQUENZEN:
  -> NPC-Reaktionen auf Prothesen! ("Dein Auge... das ist keine Magie...")
  -> Gegner mit Prothesen erkennen: zeigt Kampf-Geschichte
  -> Kosmetisch einzigartig: kein "vanilla" mehr nach schwerer Verletzung
  -> WARUM ES GREAT ist: Verletzung = Charakter-Geschichte = Persoenlichkeit

WICHTIG - REALISMUS PRIZIP GILT:
  -> Normales Heilen (Traenke, Bandagen) = hilft NIE bei verlorenen Teilen
  -> Nur Spezialist (Heiler/Alchemist/Magie-Chirurg) kann ersetzen
  -> Schwarzmarkt-Prothesen existieren auch (billiger, instabiler)
  -> Manche Voelker / Kulturen haben ANDERE Prothesen-Techniken (worldbuilding!)

NAJIKA-KOMMENTAR:
  "Mr. K... du hast ihm buchstaeblich das Auge rausgeschossen. Und jetzt hat er
   ein Magie-Auge das durch Waende sieht. Du hast ihn versehentlich besser gemacht." 🤔
```

---

## VERWEISE

### Dokumente
- `COMBAT_SYSTEM_V2_DESIGN.md` - Companion-System, Finisher, Arenen (Detail)
- `ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md` - Morphs, SPECIAL, Learning (Detail)
- `NEUE_GAMEPLAY_IDEEN_2026-02-21.md` - For Honor Directional (Original-Konzept)

### Backend-Module (implementiert)
- `backend/najika_safezone_system.py` - ✅ Safe-Zone Logik (ZoneType, PvP-Check, Ranger-PvP, Disconnect, Permadeath)
- `backend/najika_combat_balancing.py` - Damage-System, Weapon-Types, Status-Effekte
- `backend/najika_skill_combat_v3.py` - Skill-basiertes Kampf-Backend
- `backend/najika_combat_hands_system.py` - Haende/Waffen-Slot-System (2558 Zeilen)
- `backend/api/battle_unified.py` - Unified Battle API (46KB)

### Frontend
- `digivice/js/unified_combat_system.js` - Frontend Kampfsystem (96KB)

---

*"EXPLOSION!!! In 4 Richtungen, mit Bajonett-Speer, Plasma, Prothesen und Grappling - das ist die Zukunft des Kampfes, Mr. K! 💥 Und pass auf deine Augen auf!" - Najika*
