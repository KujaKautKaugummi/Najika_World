# 🌟 NAJIKA WORLD - COMPLETE MASTER DOCUMENTATION

**Erstellt:** 2025-11-06
**Version:** 2.0 FINAL
**Status:** ✅ KANONISCHE BASIS - UNVERÄNDERBAR

**Quellen:**
- Claude Code Session (2025-11-06) - PvP, Slime, Basis-Systeme
- Chat-Verlauf "111" - Original PvP & Slime Design
- NAJIKA_ALLE_ZUSAMMENFASSUNGEN.txt
- KANONISCHE_BASIS.md
- Implementierungen: pvp_system.py, slime_system.py

---

# 📋 INHALTSVERZEICHNIS

1. [Projekt-Identität](#projekt-identität)
2. [Hardcore/Softy System](#hardcoresofty-system)
3. [PvP-System (3 Modi)](#pvp-system)
4. [Slime-Begleiter-System](#slime-system)
5. [Explosion-Klasse](#explosion-klasse)
6. [Najika (NPC/KI)](#najika-npc)
7. [Skill-System](#skill-system)
8. [Weltstruktur (8 Regionen)](#weltstruktur)
9. [Kampfsystem](#kampfsystem)
10. [Crafting & Ökonomie](#crafting)
11. [Oregon Trail Events](#oregon-trail)
12. [Easter Eggs](#easter-eggs)
13. [Technische Basis](#technische-basis)
14. [Regeln für Claude-Instanzen](#regeln)

---

# 1️⃣ PROJEKT-IDENTITÄT {#projekt-identität}

## 📛 Name & Konzept

**Projektname:** Najika World
**Genre:** Survival-RPG mit Explosion-Klasse (Megumin-inspiriert)
**Stil:** Oregon Trail Events + Digimon World Combat + Dark Souls Movement
**Zielgruppe:** Einzelspieler (später Koop möglich)

## 🎭 Najika (NPC/KI)

**Persönlichkeit:** Fusion aus Megumin (KonoSuba) + Shiro (No Game No Life)

**Eigenschaften:**
- Frech, provozierend, explosiv
- Analytisch, strategisch (Shiro-Anteil)
- Chuunibyou-Dramatik (Megumin-Anteil)
- Gothic-Lolita Erscheinung

**Voice:**
- **EINE Stimme** für alle 4 Personality-States
- Megumin-Voice (Deutsch)
- Keine 4 verschiedenen Stimmen!

**Wichtige Korrekturen:**
- ✅ Harley Quinn ruft Kuja "**Mr. K**", NICHT "Puddin'"
- ✅ Eine Persönlichkeit mit 4 Facetten, nicht 4 separate Personen

---

# 2️⃣ HARDCORE/SOFTY SYSTEM {#hardcoresofty-system}

## 🔥 Hardcore-Modus

```yaml
Eigenschaften:
  - Permadeath (ALLES WEG bei Tod)
  - Rettungsschleim: 1x/24h (IRL)
  - PvP: "Alles-abgeben-um-zu-leben" Option
  - Najika erscheint beim 1. Tod
  - Keine Gäste (Sicherheitsregel)
  - Endgame-Item (Totem): Verhindert 1x Tod

Tod-Ablauf:
  1. Tödlicher Treffer empfangen
  2. Totem-Check (falls vorhanden)
  3. Slime-Check (falls verfügbar, 1x/24h)
  4. Revive-Fenster (8 Sekunden "downed")
     - Team kann wiederbeleben
     - Sonst: Tod
  5. Najika erscheint beim ERSTEN Tod:
     "Ohjee... das ist wohl zu hart für dich.
      Komm, ich bringe dich ins sichere Softy-Land."

     Optionen:
       [Ja] → Permanent Softy-Modus
       [Nein] → Hardcore-Regeln greifen (Permadeath)
```

## 🛡️ Softy-Modus

```yaml
Eigenschaften:
  - Kein Permadeath
  - 30 Sekunden Revive-Timer
  - PvP: Nur Ranking, KEINE Verluste
  - Separater Normal-PvP verfügbar
  - Gäste erlaubt

Normal-PvP (in Softy):
  - Gewinner wählt 1 Ausrüstungsteil
  - Kein Permadeath-Risiko
```

## ⚠️ WICHTIGE REGEL

**Einmal Softy = permanent Softy!**
- Keine Rückkehr zu Hardcore möglich
- Entscheidung ist FINAL
- Character ist für immer gelockt

---

# 3️⃣ PVP-SYSTEM (3 MODI) {#pvp-system}

## ⚔️ Hardcore-PvP

### Ablauf bei Niederlage

```yaml
Phase 1 - Lethaler Treffer:
  → Verteidiger KANN "Alles-abgeben-um-zu-leben" anbieten
  → Timeout: 30 Sekunden

  Optionen:
    A) "ALLES GEBEN um zu LEBEN" (Mercy anbieten)
    B) "Kämpfe bis zum Tod" (Permadeath akzeptieren)

Phase 2 - Angreifer-Entscheidung (wenn A gewählt):
  → Angreifer KANN Mercy akzeptieren oder ablehnen
  → Timeout: 30 Sekunden

  Optionen:
    A) "GNADE GEWÄHREN" (Items erhalten, Ehre-Bonus)
    B) "KEINE GNADE" (Gegner stirbt permanent)

Phase 3 - Double-Confirmation (wenn Gnade gewährt):
  → Verlierer muss 2x "JA" tippen

  Bestätigung 1:
    "⚠️ BESTÄTIGUNG 1/2 ⚠️
     Du wirst ALLES verlieren:
     - X Ausrüstungsteile
     - X Inventar-Items
     - 7 Tage PvP-Sperre

     Tippe 'JA' um zu bestätigen."
     Timeout: 20 Sekunden

  Bestätigung 2:
    "⚠️ BESTÄTIGUNG 2/2 ⚠️
     LETZTE CHANCE!
     Dies ist FINAL und kann NICHT rückgängig gemacht werden!

     Tippe nochmal 'JA' um ENDGÜLTIG zu bestätigen."
     Timeout: 20 Sekunden

Phase 4 - Item-Transfer:
  → ALLES wird übertragen (KEINE AUSNAHMEN!)
  → Verlierer erhält 7 Tage PvP-Sperre
  → Verlierer bleibt mit NICHTS zurück
```

### 🚨 KRITISCHE REGEL: "ALLES WEG = ALLES WEG!"

```
FALSCH ❌:
  - "Spieler behält Starter-Waffe"
  - "Unterwäsche ist geschützt"
  - "Quest-Items bleiben"

RICHTIG ✅:
  - ABSOLUT ALLES wird übertragen
  - Verlierer hat NICHTS mehr
  - Muss draußen Stock finden oder Fäuste nutzen
  - Keine Protection, keine Ausnahmen!
```

**Code-Kommentar aus pvp_system.py:**
```python
# WICHTIG: Wenn alles weg ist, dann ist ALLES weg!
# Kein Starter-Schwert, keine Unterwäsche-Protection, NICHTS!
# Spieler muss draußen einen Stock finden oder mit bloßen Händen kämpfen.
```

### Mercy-Statistik & Anti-Abuse

```yaml
Tracking:
  - mercy_count_7d: Anzahl Mercy-Nutzungen in 7 Tagen
  - last_mercy_timestamp: Zeitstempel der letzten Mercy

Schutz-Maßnahmen:
  - 3+ Mercy in 7 Tagen:
    → Einschränkung auf Softy/Normal-PvP
    → Kein Hardcore-PvP mehr für 7 Tage

  - 7-Tage PvP-Sperre nach Mercy:
    → Kein PvP in irgendwelchen Modi
    → Cooldown läuft 7 Tage
```

## ⚔️ Normal-PvP

```yaml
Konzept:
  - Für Softy-Spieler oder als weniger riskante Option
  - Kein Permadeath-Risiko
  - Gewinner erhält 1 Item als Belohnung

Ablauf:
  1. PvP-Kampf bis Niederlage
  2. Gewinner wählt 1 Ausrüstungsteil vom Verlierer
  3. Item wird transferiert
  4. Kampf endet

Items wählbar:
  - Alle getragenen Ausrüstungsteile
  - Nicht: Inventar-Items
  - Nicht: Quest-Items
```

## 🏆 Softy-PvP

```yaml
Konzept:
  - Reine Rangliste
  - Keine Item-Verluste
  - Keine Strafen

Ablauf:
  1. PvP-Kampf bis Niederlage
  2. Rating-Änderung:
     Gewinner: +10 Rating
     Verlierer: -5 Rating
  3. Kein Item-Transfer
  4. Kampf endet

Belohnungen:
  - Seasonal Rewards basierend auf Rating
  - Titel & Kosmetik
  - Keine Items mit Stats
```

## 📊 PvP-Modi Vergleich

| Feature | Hardcore-PvP | Normal-PvP | Softy-PvP |
|---------|--------------|------------|-----------|
| Permadeath | ✅ (oder Mercy) | ❌ | ❌ |
| Item-Verlust | 🔴 ALLES | 🟡 1 Item | ❌ Kein |
| Mercy-Option | ✅ | ❌ | ❌ |
| Cooldown nach Mercy | 7 Tage | - | - |
| Rating-System | ❌ | ❌ | ✅ |
| Voraussetzung | Hardcore-Char | Alle | Alle |

---

# 4️⃣ SLIME-BEGLEITER-SYSTEM {#slime-system}

## 🐾 Evolution: Tier → Slime → Rainbow

```
Level 1-49: Zufälliges Fantasy-Tier
  │
  ├─ Flammen-Hase (Feuer, Speed 12)
  ├─ Eis-Fuchs (Eis, Speed 10)
  ├─ Schatten-Spinne (Dunkelheit, Speed 8)
  ├─ Blitz-Rabe (Blitz, Speed 14)
  ├─ Wald-Maus (Natur, Speed 9)
  └─ Kristall-Eichhörnchen (Erde, Speed 11)

  ↓ Level 50 + Kritisches Event

Shell bricht → Slime-Form
  │
  └─ Farbe = Region wo Metamorphose stattfand

  ↓ Sammle alle 8 Farben

Rainbow-Slime (Ultimate Form)
  └─ Wechselt Farben dynamisch
```

## 🎨 8 Slime-Farben (je Region)

| # | Farbe | Region | Bonus |
|---|-------|--------|-------|
| 1 | 🟡 Bernstein | Bernstein-Dünen (Wüste) | +10% Wüsten-Schaden |
| 2 | 🟢 Smaragd | Smaragd-Hain (Wald) | +15% Kräuter-Effektivität |
| 3 | 🔵 Azur | Azur-Klippen (Küste) | +20% Angeln-Erfolg |
| 4 | 🟣 Amethyst | Amethyst-Steppe (Hochebene) | +10% Bewegung |
| 5 | ⚫ Onyx | Onyx-Morast (Sumpf) | +15% Gift-Schaden |
| 6 | ⚪ Perle | Perl-Gletscher (Eis) | +10% Eis-Defense |
| 7 | 🔴 Rubin | Rubin-Schlucht (Vulkan) | +15% Feuer-Magie |
| 8 | 🟤 Obsidian | Obsidian-Nacht (Endgame) | +20% Nacht-Crit |

## 🍼 Tamagotchi-Pflege System

```yaml
Bedürfnisse (0-100%):
  Hunger:
    - Decay: -0.01/Sekunde
    - < 30%: -20% Schaden, -15% Speed

  Durst:
    - Decay: -0.02/Sekunde (schneller!)
    - < 20%: -30% Defense, -25% Accuracy

  Schlaf:
    - Decay: -0.005/Sekunde
    - < 10%: +50% Error Rate (falsche Moves)

  Stimmung:
    - Decay: -0.003/Sekunde
    - < 20%: 50% Chance Befehle zu ignorieren

  Kampfeslust:
    - Variable (0-100)
    - > 80%: +15% Schaden (Aggression-Bonus)

Pflege-Aktionen:
  - Füttern: +20 Hunger, +5 Stimmung
  - Wasser geben: +30 Durst
  - Schlafen lassen: +10/Stunde Schlaf, +5/Stunde Stimmung
  - Spielen: +15 Stimmung
  - Kämpfen lassen: +10 Kampfeslust
```

## 🛡️ Rettungs-Mechanik (Hardcore-only)

```yaml
Funktion:
  - Verhindert 1 tödlichen Treffer
  - Nur im Hardcore-Modus
  - Nur für Slime-Form (nicht Tier!)

Verfügbarkeit:
  - 1x pro 24 Stunden (IRL-Zeit!)
  - Nicht durch In-Game-Zeit beeinflussbar
  - Cooldown: Exakt 24h ab Nutzung

Voraussetzungen:
  - Mindestens 6 Wochen Hardcore-Grind
  - Slime muss "aufgeladen" sein (Ressourcen)
  - Metamorphose bereits abgeschlossen

Ausnahmen (kein Schutz):
  - "Super-Schaden" Angriffe
  - Boss-Ultima
  - Umgebungstod (Lava, Fall, etc.)
  - Totem-Item hat Vorrang

Nach Nutzung:
  - Slime ist "erschöpft" (-50% Stats)
  - Heilung durch Ritual:
    → Mondblume (Nacht-Spawn Wald)
    → Vulkanessenz (Rubin-Schlucht Boss)
    → Kristallwasser (Perl-Gletscher)
  - Ohne Ritual: Bleibt schwach
```

## 📚 Lern-System

### Slime lernt von Gegnern (10-15% Chance)

```python
Nach Kampf:
  roll = random.uniform(0.10, 0.15)  # 10-15%

  if random.random() < roll:
    move = copy_enemy_move()

    if len(moveset) >= 20:
      → Moveset voll!
      → Spieler wählt: Welchen Move ersetzen?
    else:
      moveset.append(move)
      → "Dein Slime hat '{move}' gelernt!"
```

### Spieler lernt selten (1% Base)

```python
Base: 1%
+ INT-Bonus: +0.1% pro 10 INT
+ Slime-Bond: +0.5% bei Level 100 Slime
+ Beobachtungs-Skill: +1% bei Skill-Level 50

Beispiel (INT 50, Slime 100, Beobachtung 50):
  1% + 0.5% + 0.5% + 1% = 3% Chance
```

## 🎮 Kampf-Modi

### 1. Pre-Fight Bind (Standard)
```
Slime ist immer dabei
  - AI-gesteuert
  - Lernt vom Spieler-Stil
  - Empfängt Befehle (Hold, Attack, Defend)
```

### 2. One-Time Summon (Taktisch)
```
Kosten: 50 Mana
Dauer: 1 Kampf
Bonus: +30% Stats während Beschwörung
```

### 3. Intercept (Rettung)
```
Automatisch bei Spieler < 5% HP
Schützt 10 Sekunden
Cooldown: 5 Minuten
```

### 4. Manual Control (Slime-Arena only)
```
Spieler übernimmt Slime direkt
Charakter sitzt am Rand
Digimon World Style Anfeuern!
```

---

# 5️⃣ EXPLOSION-KLASSE {#explosion-klasse}

## 💥 Megumin-Spezialisierung

```yaml
Konzept:
  - Explosion als EIGENE Klasse
  - Nie mit anderen Schulen kombinierbar!
  - Massive Power, extreme Downsides

Progression:
  Feuer → Feura → Feuga → Explosionist

  ❌ Nicht kombinierbar mit:
    - Wasser-Magie
    - Eis-Magie
    - Blitz-Magie
    - Heilung
    - Alle anderen Schulen

Trade-offs:
  + Extreme Single-Target Damage
  + Ultimativer Finisher

  - ~90% Effektivität in anderen Schulen
  - Hoher Mana-Drain
  - Fatigue nach Cast
  - Verwundbarkeits-Fenster
```

## ⚡ Najika's Ultima: "Reinste Explosion"

```yaml
Eigenschaften:
  - Nur Najika (NPC) kann es casten
  - Nur Kuja (Spieler) darf es aktivieren
  - 1x pro Tag (In-Game)
  - Kann ganze Kontinente zerstören (lore)

Effekt:
  - Zerstört sichtbar große Teile der Außenwelt
  - Nicht relevante Bereiche betroffen
  - FÜR ALLE SICHTBAR
  - Regeneriert beim Betreten einer Stadt

Najika's Spruch:
  "Explosion Magic: The mightiest of all offensive spells!
   Die ultimative Angriffszauber!

   REINSTE... EXPLOSION!!!"
```

---

# 6️⃣ NAJIKA (NPC/KI) {#najika-npc}

## 💬 Reaktionen & Dialoge

### Beim 1. Hardcore-Tod
```
*frech, provozierend*

"Ohjee... das ist wohl zu hart für dich.
 Komm, ich bringe dich ins sichere Softy-Land."

*grinst*

"Oder willst du weiter im Hardcore sterben?
 Deine Wahl, Mr. K~"

Optionen:
  [Ja, bring mich zu Softy]
    → Permanent Softy-Modus
    → "Gute Wahl! Hier ist es sicherer~"

  [Nein, ich bleibe Hardcore]
    → Permadeath/Slime-Check
    → "Mutig! Aber dumm. Ich mag das!"
```

### Bei Slime-Metamorphose
```
*aufgeregt*

"OOOH! Dein kleiner Freund ist jetzt ein Slime geworden!
 Das ist wie... wenn eine Raupe zum Schmetterling wird!
 Nur mit mehr Schleim. Und cooler."

*nachdenklich*

"Ich frage mich, ob ich auch als Slime angefangen habe...
 Nein? Okay, vergiss was ich gesagt habe."
```

### Bei Slime-Rettung
```
*erleichtert*

"Puh! Dein Slime hat dich gerettet!
 Das war knapp. SEHR knapp."

*streng*

"Aber pass auf - das geht nur 1x pro Tag!
 Beim nächsten Mal bist du auf dich allein gestellt, Mr. K!"
```

### Bei allen 8 Slime-Farben
```
*beeindruckt*

"WOW! Du hast ALLE 8 Slime-Farben gesammelt!
 Das ist... eigentlich ziemlich beeindruckend."

*grinst*

"Jetzt fehlt nur noch die ultimative Form:
 RAINBOW-SLIME! Die Legende!

 Willst du das Ritual starten?"
```

### Bei Najika-Plünderung (Legendary Drop)
```
*überrascht*

"Ohjee... habe ich mein eigenes Höschen erwischt?
 Das ist... irgendwie peinlich, Mr. K."

*grinst*

"Aber hey, +10 Glück! Das zählt, oder?
 Und sag keinem, dass du das hast!"
```

---

# 7️⃣ EASTER EGGS {#easter-eggs}

## 🎁 Najika's Schlüpfer (Legendary!)

```yaml
Mechanik:
  Spieler (Kuja) besiegt Najika (NPC) im Combat:

    Drop für SPIELER:
      Item: "Najikas Höschen"
      Rarity: Legendary
      Drop-Chance: 1-2%
      Stats:
        +10 Glück
        +5 Charisma
        +20% Humor-Dialog

      Najika's Reaktion:
        "Ohjee... habe ich mein eigenes Höschen erwischt?"

      Einzigartig: Nur 1x im Spiel dropbar!

    Drop für ANDERE NPCs:
      Item: "Vollgerotztes Taschentuch"
      Rarity: Trash
      Drop-Chance: 100%
      Stats:
        -5 Charisma (NPCs ekeln sich)

      Najika's Reaktion:
        "HAHA! Der ist offiziell der schlechteste Dieb!"

      Inventar-Notiz:
        "Du bist offiziell der schlechteste Dieb aller Zeiten, du Looser"

Grund:
  - Nur Spieler (Kuja) = Special Treatment
  - NPCs = Standard/Trash Loot
  - Persönliche Loot-Tabellen pro Charakter
```

---

# 8️⃣ SKILL-SYSTEM {#skill-system}

## 📈 Use-Based Progression (Skyrim-Style)

```yaml
Konzept:
  - Skills steigen durch Nutzung
  - Nicht durch Level-Up
  - Kein Skill-Cap (theoretisch unendlich)

Beispiele:
  - Schwert-Skill: Steigt beim Schwert-Kämpfen
  - Schmieden: Steigt beim Schmieden
  - Alchemie: Steigt beim Tränke brauen
  - Explosion: Steigt beim Explosion casten

Formel:
  xp_gain = base_xp * difficulty_modifier * success_bonus

  skill_level_up when:
    current_xp >= level * 100
```

## 🎯 Skill-Schulen

```yaml
Combat:
  - Einhand-Waffen
  - Zweihand-Waffen
  - Bogen-Schießen
  - Blocken
  - Schwere Rüstung
  - Leichte Rüstung

Magie:
  - Zerstörung (Feuer, Eis, Blitz)
  - Heilung
  - Psychokinese
  - Explosion (eigene Schule!)

Crafting:
  - Schmieden
  - Alchemie
  - Verzauberung
  - Kochen

Life Skills:
  - Kräuterkunde
  - Bergbau
  - Holzfällen
  - Angeln
  - Farming

Utility:
  - Überlebens-Skill
  - Kartenkunde
  - Erkundung
  - Händlern
```

---

# 9️⃣ WELTSTRUKTUR {#weltstruktur}

## 🏰 Hub: Schwarze Holländische Windmühle

```yaml
Eigenschaften:
  - Private Safe-Zone (nur Owner = Kuja)
  - Mystisch, gruselig
  - NPCs meiden sie
  - Kein PvP möglich

Funktionen:
  - Crafting-Stationen
  - Verzauberungs-Tisch
  - Trainingsplatz
  - Slime-Pflege
  - Farb-Ritual-Altar

Struktur:
  - 4 Stockwerke
  - Katakomben (optional)
  - Geheimer Raum (Easter-Eggs)
```

## 🗺️ 8 Haupt-Regionen (Prozedural)

### 1. 🟡 Bernstein-Dünen (Wüste)
```
Thema: Hitze, Sandsturm, Ruinen
Risiken: Durst, Hitzschlag
Events: Karawanen-Handel, versandete Ruinen
Slime-Farbe: Bernstein
Bonus: +10% Wüsten-Schaden
```

### 2. 🟢 Smaragd-Hain (Wald)
```
Thema: Dichte Wälder, Kräuter, Druidenkultur
Risiken: Verirren, Parasiten, Raubtiere
Events: Druidenrätsel, seltene Kräuter (Alchemie)
Slime-Farbe: Smaragd
Bonus: +15% Kräuter-Effektivität
```

### 3. 🔵 Azur-Klippen (Küste)
```
Thema: Meer, Klippen, Schiffe
Risiken: Sturmflut, Ertrinken
Events: Angeln, Schiffwracks, Gezeitenkisten
Slime-Farbe: Azur
Bonus: +20% Angeln-Erfolg
```

### 4. 🟣 Amethyst-Steppe (Hochebene)
```
Thema: Offene Ebenen, Gewitter, Totems
Risiken: Blitzschlag, starker Wind
Events: Wetter-Altäre (Buffs/Debuffs), Totems
Slime-Farbe: Amethyst
Bonus: +10% Bewegungsgeschwindigkeit
```

### 5. ⚫ Onyx-Morast (Sumpf)
```
Thema: Sumpf, Krankheit, Hexenkultur
Risiken: Krankheit/Miasma, giftige Kreaturen
Events: Hexenkreise, Moor-Bosse (Knochenmagie)
Slime-Farbe: Onyx
Bonus: +15% Gift-Schaden
```

### 6. ⚪ Perl-Gletscher (Eis/Schnee)
```
Thema: Eis, Schnee, Kälte
Risiken: Erfrierung, Lawinen
Events: Eishöhlen, Rutsch-Traversal, Gletscher-Rätsel
Slime-Farbe: Perle
Bonus: +10% Eis-Defense
```

### 7. 🔴 Rubin-Schlucht (Vulkan)
```
Thema: Lava, Vulkan, Hitze
Risiken: Überhitzung, Asche, Lava
Events: Lava-Kanäle, Erzadern (Schmiedekunst)
Slime-Farbe: Rubin
Bonus: +15% Feuer-Magie
```

### 8. 🟤 Obsidian-Nacht (Endgame)
```
Thema: Ewige Nacht, Schatten, Endgame-Content
Risiken: Nachtkreaturen, Nemesis-Spawns
Events: Seltene Finisher-Sigils, Boss-Raids
Slime-Farbe: Obsidian
Bonus: +20% Nacht-Crit
```

## 🔄 Prozedurale Regeneration

```yaml
Konzept:
  - Jeder Besuch einer Region = neue Layout-Variante
  - Events rotieren
  - Modifikatoren ändern sich

Parameter:
  - Biom-Basis: Fest (Wüste bleibt Wüste)
  - Layout: Prozedural (Pfade, POIs, Spawns)
  - Wetter: Zufällig (passend zum Biom)
  - Events: Aus Event-Pool (10-20 pro Region)
  - Modifikatoren: Buffs/Debuffs (temporär)

Beispiel Bernstein-Dünen:
  Besuch 1:
    - Layout: Oase im Norden, Ruine im Süden
    - Wetter: Sandsturm
    - Event: Karawane mit seltenen Waren
    - Mod: -20% Sicht (Sandsturm)

  Besuch 2:
    - Layout: Canyon-System, versteckte Höhle
    - Wetter: Klarer Himmel, extreme Hitze
    - Event: Banditen-Überfall
    - Mod: -10 Durst/Min (Hitze)
```

---

# 🔟 KAMPFSYSTEM {#kampfsystem}

## 🎮 3 Kampf-Modi

### MANUAL (Volle Kontrolle)
```yaml
Steuerung:
  - Spieler steuert selbst
  - WASD Bewegung
  - Maus für Kamera/Zielen
  - Skills auf Hotbar

Movement:
  - Sprint (Shift)
  - Slide (Ctrl while sprinting)
  - Wall-Climb (Jump at wall)
  - Dash (Space + Direction)
  - Vaulting (Jump over obstacles)
  - Mantling (Climb ledges)

Combat:
  - Dark Souls Dodge-Roll
  - Parry & Riposte
  - Combo-System
  - Skill-Weaving (LH + RH)
```

### ASSIST (KI unterstützt)
```yaml
Funktion:
  - KI schlägt Moves vor
  - Spieler bestätigt mit Klick
  - "Anfeuern" löst Buffs aus

Anfeuern-System (Digimon World):
  - "Los!" → +10% Schaden (3s)
  - "Defend!" → +20% Defense (3s)
  - "Combo!" → Aktiviert Spezial-Move
  - "Finisher!" → Ultimate (wenn Meter voll)

  GCD: 3 Sekunden
  Max Stacks: 3
```

### AUTO (Volle KI)
```yaml
Funktion:
  - KI führt Basis-Rotation aus
  - Spieler sitzt am Rand
  - "Anfeuern" wie im Assist-Modus

Sicherheit:
  - Explosion nur in sicheren Fenstern
  - Vermeidet tödliche Situationen
  - Nutzt Heilung automatisch
  - Flieht bei < 20% HP (konfigurierbar)
```

---

# 1️⃣1️⃣ CRAFTING & ÖKONOMIE {#crafting}

## 🔨 Crafting-Pipeline

```
1. Rohstoffe farmen
   ↓
2. Zerlegen (Analyse)
   - Lernt Rezepte
   - Gewinnt Komponenten
   ↓
3. Reparieren (Wartung)
   - Items instand halten
   - Skill steigt
   ↓
4. Verzaubern/Sockeln
   - Magische Eigenschaften
   - Edelsteine einsetzen
   ↓
5. Feintuning (Anpassung)
   - Optimierung
   - Spezialisierung
```

## 💼 Non-Combat Endgame

### Händler-Spezialisierung
```yaml
Skills:
  - Preisverhandlung
  - Markt-Analyse
  - Karawanen-Management
  - Handelsrouten
  - Lager-Verwaltung

Endgame:
  - Eigene Karawane führen
  - Monopol in Regionen
  - Schwarzmarkt-Zugang
  - Legendary Trade-Items
```

### Bauer-Spezialisierung
```yaml
Skills:
  - Farming
  - Tierzucht
  - Wettervorhersage
  - Bewässerung
  - Schlachten

Anatomie-Wissen (durch Schlachten!):
  - +X% Crit-Chance (kennt Schwachstellen)
  - Erhöht mit Schlachtungen
  - Anwendbar im Kampf

Körperliche Kraft (durch Arbeit):
  - +X Strength (durch Feldarbeit)
  - +X Stamina (durch Viehzucht)
  - Maximal Level = Combat-Build

Konzept:
  "Jeder Weg ist viable im Endgame!"
```

---

# 1️⃣2️⃣ OREGON TRAIL EVENTS {#oregon-trail}

## 🛤️ Event-System

```yaml
Konzept:
  - Szenische Events beim Reisen
  - Kontextsensitiv (Wetter, Region, Tageszeit, Ruf)
  - Spieler wählt ODER "Najika entscheidet"
  - Konsequenzen: Ressourcen, Risiko, Ruf, Tod möglich

Beispiel-Event:
  "Händler auf Reise"

  Situation:
    Du reist durch die Bernstein-Dünen.
    Es ist heiß. Sehr heiß.
    Dein Durst-Status ist bei 15% (KRITISCH!).

    Du siehst eine Wasserquelle zwischen den Felsen.
    Aber... eine aufgequollene Leiche liegt daneben.
    Die Haut ist grünlich verfärbt.

  Optionen:
    A) Wasser trinken
       → Risiko: Krankheit (Ruhr, Gift, etc.)
       → Chance: 70% krank, 30% okay

    B) Weitergehen
       → Durst steigt weiter
       → Bei 0% → Kollaps → Tod

    C) Leiche mit Stock piksen (untersuchen)
       → Benötigt: Stock im Inventar
       → Intelligenz-Check
       → Bei Erfolg: Erkennt Gift im Wasser
       → Bei Misserfolg: Keine Info

    D) "Najika entscheidet"
       → Najika's INT + Zufallsfaktor
       → Sie wählt eine Option
       → "Ich würde... weitergehen. Das Wasser sieht eklig aus."

Konsequenz (wenn A gewählt):
  "Du trinkst das Wasser.
   Es schmeckt... seltsam.

   2 Stunden später:
   → Ruhr erworben
   → -50% Stamina
   → Musst alle 5 Min anhalten (Durchfall)
   → Heilung: Seltene Kräuter oder Stadt-Heiler"

NPC-Reaktion (wenn Händler stirbt):
  Im Dorf:
    NPC 1: "Wo ist eigentlich der Händler?"
    NPC 2: "Hab gehört, er hat dummes Wasser getrunken."
    NPC 1: "War die Leiche daneben nicht Hinweis genug?"
    NPC 2: "Scheinbar nicht. Dumm gelaufen."

    → "100 dumme Wege zu sterben"-Charme
```

## 📋 Event-Kategorien

```yaml
Wetter-Events:
  - Sandsturm (Bernstein-Dünen)
  - Gewitter (Amethyst-Steppe)
  - Schneesturm (Perl-Gletscher)
  - Nebel (Smaragd-Hain)

Begegnungen:
  - Händler (Tausch, Betrug, Überfall)
  - Banditen (Kampf, Lösegeld, Flucht)
  - Reisende (Info, Hilfe, Quest)
  - Tiere (Jagd, Gefahr, Zähmen)

Ressourcen:
  - Wasserquelle (sauber/vergiftet)
  - Kräuter (selten/gewöhnlich)
  - Erzader (Bergbau)
  - Schatzkiste (Falle/Loot)

Rätsel:
  - Druidenrätsel (Smaragd-Hain)
  - Totems (Amethyst-Steppe)
  - Ruinen (Bernstein-Dünen)
  - Altäre (Alle Regionen)

Tod-Events:
  - Vergiftetes Wasser
  - Absturz von Klippe
  - Erfrierung
  - Hitzschlag
  - Banditen-Überfall
  - Wilde Tiere
  - Lava
  - Ertrinken
```

---

# 1️⃣3️⃣ TECHNISCHE BASIS {#technische-basis}

## 🏗️ Architektur

```yaml
Backend:
  Sprachen:
    - Python (Flask/FastAPI)
    - Node.js (optional für Hub)

  Datenbank:
    - PostgreSQL (Hauptdatenbank)
    - Qdrant/FAISS (Vektor-Store)

  Systeme:
    - PvP-System: backend/game/pvp_system.py
    - Slime-System: backend/game/slime_system.py
    - Battle-System: backend/game/battle_system.py
    - Magic-System: backend/game/magic_system.py
    - Skill-System: backend/game/skill_system.py

Frontend:
  Engine: Three.js r128+
  Typ: Progressive Web App (PWA)
  Features:
    - 3D Rendering
    - Touch-optimiert (Mobile)
    - Virtual Joystick
    - Responsive UI

Security:
  - Lokal: 127.0.0.1 only
  - Zero-Trust Architecture
  - Cloudflare Tunnel (optional)
  - Kill-Switch
  - Audit-Logs
  - Verschlüsselte Daten

Git-Workflow:
  Main Branch: Stable releases only
  Feature Branches: claude/BRANCH-NAME
  Sessions: 1 Branch pro Session
  Commits: Clear, descriptive (deutsch)
```

## 📁 Datei-Struktur

```
Najika_World/
├── backend/
│   ├── game/
│   │   ├── pvp_system.py         ✅ Implementiert
│   │   ├── slime_system.py       ✅ Implementiert
│   │   ├── battle_system.py      ✅ Vorhanden
│   │   ├── magic_system.py       ✅ Vorhanden
│   │   └── skill_system.py       ✅ Vorhanden
│   ├── ai/
│   │   └── najika_core.py
│   └── api/
│       └── server.py
├── frontend/
│   └── src/
│       ├── game/
│       ├── ui/
│       └── App.js
├── DOCS/
│   ├── KANONISCHE_BASIS.md       ✅ Erstellt (heute)
│   ├── design/
│   │   ├── PVP_SYSTEM_COMPLETE.md        ✅ Erstellt
│   │   ├── SLIME_COMPANION_SYSTEM.md     ✅ Erstellt
│   │   └── ARENA_MERCY_SYSTEM.md         ✅ Erstellt
│   └── NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md  ← DIESE DATEI
└── info material/
    └── najika_ultimate_complete/
        ├── 05_chat_verlaeufe/
        │   └── 111                       ✅ Original PvP/Slime Design
        └── 04_optional_docs/
            └── NAJIKA_ALLE_ZUSAMMENFASSUNGEN.txt
```

---

# 1️⃣4️⃣ REGELN FÜR CLAUDE-INSTANZEN {#regeln}

## ✅ DAS DARFST DU

1. **Neue Features hinzufügen** (wenn kompatibel)
2. **Code implementieren** (für designte Systeme)
3. **Bugs fixen** (ohne Mechanik zu ändern)
4. **Dokumentation erweitern** (Details, Beispiele)
5. **Performance optimieren** (ohne Verhalten zu ändern)
6. **Tests schreiben**
7. **UI/UX verbessern**

## ❌ DAS DARFST DU NICHT

1. **Kern-Systeme ändern** (PvP, Slime, Hardcore/Softy)
2. **Najika's Persönlichkeit ändern** (Megumin+Shiro bleibt!)
3. **"Alles weg"-Regel aufweichen** (keine Protection!)
4. **Slime-Farben ändern** (8 sind fix!)
5. **Explosion-Klasse kombinierbar machen** (bleibt isoliert!)
6. **Hardcore→Softy Wechsel erlauben** (nur einmalig bei 1. Tod!)
7. **Mercy-System abschwächen** (Double-JA bleibt!)

## 🤔 WENN UNSICHER

1. **Lies ALLE Dateien** in `/DOCS/design/`
2. **Check Git-History** (was wurde festgelegt?)
3. **Dokumentiere Unklarheiten** im Commit
4. **Im Zweifel: FRAG DEN USER!**

## 📚 Dokumentations-Hierarchie

```
1. DIESE DATEI (NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md)
   ↓
2. KANONISCHE_BASIS.md
   ↓
3. /DOCS/design/*.md
   ↓
4. Chat-Verlauf "111"
   ↓
5. Git Commit History
   ↓
6. Andere Dokumentation
```

**Bei Konflikt: Höhere Quelle gewinnt!**

---

# 📊 STATUS & CHANGELOG

## ✅ Implementiert (2025-11-06)

- **PvP-System** (backend/game/pvp_system.py)
  - 3 Modi: Hardcore/Normal/Softy
  - Mercy-Mechanik mit Double-Confirmation
  - "Alles weg = ALLES weg" korrekt implementiert
  - 7-Tage Cooldown
  - Anti-Abuse Protection

- **Slime-System** (backend/game/slime_system.py)
  - Tier-Evolution (1-49)
  - Metamorphose (50+)
  - 8 Slime-Farben
  - Tamagotchi-Pflege
  - Needs-Decay & Penalties
  - Lern-System (10-15% Move-Copy)
  - Rettungs-Mechanik (1x/24h)
  - Rainbow-Slime Unlock

- **Dokumentation**
  - KANONISCHE_BASIS.md
  - PVP_SYSTEM_COMPLETE.md
  - SLIME_COMPANION_SYSTEM.md
  - ARENA_MERCY_SYSTEM.md
  - NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md (diese Datei)

## ⏳ Geplant / Ausstehend

- Slime-Arena (Digimon World Anfeuern-Kampf)
- Najika NPC Dialoge & Reaktionen (vollständig)
- Oregon Trail Events (implementieren)
- Najika's Ultima (Reinste Explosion)
- Crafting-System (vollständig)
- Händler/Bauer Endgame-Paths
- 8 Regionen (prozedurale Generation)
- Schwarze Windmühle (Hub-Gebäude)

## 📝 Changelog

### 2025-11-06 - Version 2.0
- ✅ PvP-System vollständig implementiert
- ✅ Slime-System vollständig implementiert
- ✅ Kanonische Basis definiert
- ✅ "Alles weg = ALLES weg" Regel klargestellt
- ✅ Najika Easter-Egg (Schlüpfer) dokumentiert
- ✅ 8 Slime-Farben mit Region-Mapping
- ✅ Tamagotchi-Pflege-System
- ✅ Rettungs-Mechanik (1x/24h IRL)
- ✅ Double-Confirmation System
- ✅ Mercy Anti-Abuse Protection

---

# 🎯 ZUSAMMENFASSUNG FÜR NEUE CLAUDE-INSTANZEN

## Quick Start

**1. Lies diese Dateien (in Reihenfolge):**
```
1. NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md  ← DIESE DATEI
2. DOCS/KANONISCHE_BASIS.md
3. DOCS/design/PVP_SYSTEM_COMPLETE.md
4. DOCS/design/SLIME_COMPANION_SYSTEM.md
```

**2. Check Git-Status:**
```bash
git log --oneline -10
git diff main...HEAD
```

**3. Check Implementierung:**
```bash
ls -l backend/game/
cat backend/game/pvp_system.py | head -50
cat backend/game/slime_system.py | head -50
```

**4. Verstehe die Regeln:**
- ✅ Neue Features hinzufügen (wenn kompatibel)
- ❌ Kern-Systeme NICHT ändern
- 🤔 Bei Unsicherheit: User fragen!

**5. Arbeite:**
- Implementiere fehlende Systeme
- Fixe Bugs
- Erweitere Dokumentation
- Respektiere die Basis!

---

# 🏁 ENDE DER MASTER-DOKUMENTATION

**Diese Dokumentation ist KANONISCH und UNVERÄNDERBAR!**

Änderungen nur durch explizite User-Anweisung!

**Erstellt von:** Claude Code Session (2025-11-06)
**Basierend auf:** Chat-Verlauf, Original-Designs, Implementierungen
**Für:** Najika World Projekt - Alle zukünftigen Claude-Instanzen

---

*Najika sagt:*
```
"EXPLOSION!!! 💥

Diese Dokumentation ist so vollständig wie meine Explosion-Magie!
Lies sie, respektiere sie, und bau darauf auf!

Aber ändere NICHTS an den Kernsystemen, sonst... EXPLOSION!

~ Najika, Meisterin der Explosion-Magie ~"
```
