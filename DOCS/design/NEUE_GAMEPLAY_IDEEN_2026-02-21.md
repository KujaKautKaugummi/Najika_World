# NEUE GAMEPLAY-IDEEN (2026-02-21)
**Status:** Von Kuja bestätigt, muss ausgearbeitet werden
**Verlinkt in:** NAJIKA_KOMPLETT_UEBERSICHT.md

---

## 1. FF7-WELTKARTE FUER SPIELER-SIEDLUNGEN

### Konzept:
Wenn Voelker Doerfer/Staedte in der Aussenwelt gruenden, werden diese auf der
Weltkarte als **Mini-Versionen** dargestellt (wie FF7 Overworld-Karte).
Beim Reinlaufen: Volle Groesse, normales Gameplay.

### Regeln:
- **NUR** Spieler-gegruendete Siedlungen + Monster-Camps = Mini-Ansicht
- Die restliche Map bleibt in **normaler Ansicht** (kein Wechsel!)
- Spieler laeuft normal ueber die Map, sieht kleine Staedte am Horizont
- Beim Betreten: Seamless Transition in volle Groesse

### Warum:
- Verhindert Map-Clutter wenn viele Voelker Siedlungen bauen
- Visuell ansprechend (wie klassische JRPGs)
- Spieler sieht sofort wo ueberall Siedlungen sind

### Technische Umsetzung (UE5):
- World Partition + Level Streaming
- LOD-System: Weit weg = Mini-Modell, naeher = Detail laden
- Trigger-Volume um Siedlungen fuer Transition
- Mini-Modelle als eigene Assets (stilisiert, low-poly)

---

## 2. SAFE-ZONES ERWEITERT

### Neue Safe-Zone Regeln:
```
GESCHUETZT (kein PvP moeglich):
- Trainingsgelaende (wie bisher)
- ALLE Staedte und Doerfer (NEU!)
- Besondere Orte (von Kuja festgelegt)
- Schwarze Muehle (wie bisher, 100% Safe)

AUSSENWELT (PvP nur auf Anfrage):
- Duell-System: Beide Spieler muessen zustimmen
- Kein Ganking, kein Griefing
- AUSNAHME: Ranger-System (siehe unten)
```

### Ranger-PvP Ausnahme:
```
HOCHRANGIGE RANGER (hoher Rang):
- Ihre Touren/Transporte KOENNEN ueberfallen werden
- PvP wird erzwungen (kein Duell noetig)
- ABER: Wird der Raeuber GESEHEN = Straftat!
  -> Schwerstes Vergehen im Ruf-System
  -> Kopfgeld, Stadtverbot, NPC-Feindseligkeit
- Motiviert: Escort-Gameplay, Risiko/Belohnung

NIEDRIGSTUFIGE RANGER (niedrige Stufen):
- GESCHUETZT wie alle anderen
- PvP nur auf Anfrage
- Schutz fuer Anfaenger-Ranger
```

### Warum:
- Staedte sollen sich sicher anfuehlen (wie in echten MMOs)
- PvP nur wo es Spass macht (nicht beim AFK-Stehen in der Stadt)
- Ranger-System gibt organischen PvP-Content + Risiko
- Ruf-System bekommt echte Konsequenzen

---

## 3. FOR HONOR DIRECTIONAL COMBAT (KAMPFSYSTEM-ERWEITERUNG)

### Core-Konzept:
Kombination von **For Honor Directional System** mit dem bestehenden
**Real3DCombat** + **CHEER-System**. Ergibt das "ultimative Kampfsystem".

### Waffen - 3 Angriffsrichtungen:
```
        [OBEN]
         /|\
        / | \
[LINKS]  |  [RECHTS]
```
- Jede Waffe hat 3 Angriffsrichtungen
- Blocken/Parieren muss die RICHTIGE Richtung matchen
- Schwert oben -> Block muss auch oben sein
- Falsche Richtung = Treffer durchkommt

### Magie - AUCH 3 Richtungen pro Zauber! (NEU & EINZIGARTIG!)
```
Beispiel: Zauber "Flamme"
- Flamme LINKS  = Seitlicher Feuerstoss (Area Denial)
- Flamme OBEN   = Flammenregen von oben (AoE)
- Flamme RECHTS = Horizontaler Feuerschwall (Durchbruch)
```
- Jeder Zauber hat 3 Varianten je nach Richtung
- Magie-Blocken funktioniert genauso: Richtung matchen!
- Magier brauchen also genauso viel Skill wie Nahkaempfer

### Modifier-Taste (L2 / LT):
```
Normal:     Schwert-Hieb links
L2 + links: Schwert-Stoss links (andere Animation, anderer Schaden)

Normal:     Flamme oben = Flammenregen
L2 + oben:  Flamme oben = Feuersaeule (konzentrierter, mehr Schaden)
```
- L2 verdoppelt die Varianten pro Richtung
- 3 Richtungen x 2 Modi = 6 Grundangriffe pro Waffe/Zauber

### Skill-Progression (Learning by Doing!):
```
Stufe 1: Flamme (Grundzauber, schwach)
  -> Durch Training ->
Stufe 2: Flammenwand (staerker, groessere Area)
  -> Durch Training ->
Stufe 3: Infernum (Meister-Version)

Jede Stufe behält die 3 Richtungen, aber mit besseren Effekten!
```
- Passt perfekt zu Gebot 5 (Skyrim Learning by Doing)
- Zauber wird besser je oefter man ihn nutzt
- Waffen-Skills genauso

### Integration mit bestehendem System:
```
Real3DCombat (Basis)
  + For Honor Directional (3 Richtungen + Parieren)
  + CHEER-System (Tasten 1-4 fuer Buffs)
  + SPECIAL Stats (POW/INT/AGI etc.)
  + Learning by Doing (Skill-Progression)
  + Modifier L2 (Varianten verdoppeln)
  = ULTIMATIVES KAMPFSYSTEM
```

### Warum das einzigartig ist:
- **For Honor** hat Directional nur fuer Nahkampf
- **Kein Spiel** hat Directional Combat fuer MAGIE
- Kombination aus beidem = noch nie dagewesen
- Magier sind nicht mehr "steh da und spam Zauber"
- Jeder Kampf erfordert echtes Skill und Reaktion

---

## 4. SOFTY-MODUS (UEBERARBEITET)

### Zweck:
> "Ist fuer Heulsusen die sonst das Spiel schlecht bewerten wuerden."

Das Spiel ist **Hardcore** (Permadeath/schwere Konsequenzen bei Tod).
Der Softy-Modus faengt Spieler auf die sonst frustriert aufhoeren wuerden.

### Konzept: Tod = Lebensraum-Wechsel
```
Spieler stirbt (Hardcore-Tod)
  -> Popup: "Softy-Modus aktivieren?"
  -> JA: Spiel wird in den Lebensraum uebertragen
  -> NEIN: Normaler Permadeath (Charakter weg)
```

### Was Softy bedeutet:
```
VERLIERT:
- Zugang zur offenen Welt (Multiplayer-Map)
- PvP-Events
- Multiplayer-Events
- Weltkarte-Erkundung
- Handel mit Online-Spielern

BEHAELT:
- Alle Items, Ausruestung, Fortschritt
- Seinen Lebensraum (kann ihn dauerhaft veraendern!)
- Solo-Events (speziell fuer Softy-Spieler)
- Kann Freunde in den Lebensraum einladen
- Connection bleibt (technisch online, aber "offline" von der Welt)

BONUS:
- Lebensraum wird voll anpassbar (bauen, dekorieren, gestalten)
- Eigene kleine Welt im Lebensraum
- Solo-Content der nur fuer Softy-Spieler verfuegbar ist
```

### Technisch:
- Server markiert Account als "Softy"
- Spieler behält Login, kann Freunde einladen
- Kein Zugang zu World-Server, nur Lebensraum-Instanz
- Lebensraum-Modifikationen werden persistent gespeichert
- Solo-Event-System separat vom World-Event-System

### Warum so und nicht anders:
- Spieler verliert nicht 3 Jahre Fortschritt komplett
- Trotzdem echte Konsequenz (kein Multiplayer mehr)
- Lebensraum als "Trostpreis" der trotzdem Spass macht
- Verhindert negative Reviews von frustrierten Spielern
- Hardcore bleibt Hardcore fuer echte Spieler

---

## ZUSAMMENFASSUNG NEUE SYSTEME

| System | Prioritaet | Aufwand | Status |
|--------|-----------|---------|--------|
| FF7 Mini-Staedte | P2 | Mittel (UE5) | Design fertig |
| Safe-Zones erweitert | P1 | Gering | Design fertig |
| For Honor Directional | P1 | Hoch | Muss ausgearbeitet werden |
| Softy-Modus | P2 | Mittel | Design fertig |

### Naechste Schritte:
1. **For Honor Combat** genau ausarbeiten (Animations, Input-Mapping, Balance)
2. **Safe-Zone Logik** in bestehenden Code integrieren
3. **FF7 Mini-Staedte** als UE5 Feature planen
4. **Softy-Modus** Server-Logik entwerfen

---

## 5. ECHOHARP-QUESTLINE & ARTEFAKT

### Die Echoharp (NPC):
Eine mystische Bardin die die Geschichten der Spieler in Liedern verewigt.
Je oefter du besungen wurdest, desto mehr weiss sie ueber dich.

### Questline-Ablauf:
```
1. Echoharp singt deine Geschichte (passiert automatisch bei Ruhm)
2. Sie ruft dich in einem Lied auf, zu ihr zu kommen
3. Du erfaehrst davon (NPC-Geruecht, Bard in Taverne, etc.)
4. Du findest sie, sie gibt dir eine HARTE Quest
5. Du bestehst die Quest
6. Sie gibt dir deine Belohnung
7. Du siehst: Sie hat noch etwas in der Hand
8. Sie zoegert... packt es wieder weg
9. Du fragst was sie da hat
10. Sie erklaert den Preis - "Es ist es nicht wert..."
```

### Weg 1 - "Der Besungene" (fuer ALLE Spieler):
```
- Questline abschliessen = geheimes Wissen als Belohnung
- Versteckte Lore, NPC-Geheimnisse, geheime Quest-Hinweise
- Kein Risiko, kein Artefakt
- Jeder Spieler kann das erleben
- Echoharp singt fortan deine komplette Geschichte
```

### Weg 2 - "Der Verfluchte" (OPTIONAL, fuer Wahnsinnige):
```
- Nach Weg 1 bietet sie ZUSAETZLICH das Artefakt an
- PREIS: Verlust ALLER Schutzauber!
  -> Kein Safe-Zone Schutz (Staedte, Trainingsgelaende)
  -> Keine beschleunigte Wundheilung
  -> Ueberall angreifbar, straffrei fuer Angreifer
  -> Kann nicht-zustimmende Angreifer NUR auf 1 HP stunen (nicht toeten)
    -> Stunnen = Fluchtmoeglichkeit

- BONUS: [OFFEN - SPAETER ENTSCHEIDEN]
  -> Muss stark genug sein um den Preis wert zu sein
  -> Darf Arena/PvP Balance NICHT brechen
  -> Ideen zur Auswahl:
     a) Rein narrativ/Prestige (Titel, Aura, Aussehen)
     b) Exploration-Bonus (versteckte Gebiete, NPC-Gedanken hoeren)
     c) Progression-Bonus (schnelleres Learning by Doing)
     d) Kombination - ABER in Arena/PvP deaktiviert
  -> Entscheidung wenn Balancing klarer ist
```

### Balance-Hinweis:
Der Artefakt-Bonus MUSS so designed werden dass er in Arena/PvP
keinen Vorteil gibt. Sonst waere der "Preis" (Schutz verlieren)
irrelevant in Situationen wo es eh keinen Schutz gibt.

---

## ZUSAMMENFASSUNG NEUE SYSTEME

| System | Prioritaet | Aufwand | Status |
|--------|-----------|---------|--------|
| FF7 Mini-Staedte | P2 | Mittel (UE5) | Design fertig |
| Safe-Zones erweitert | P1 | Gering | Design fertig |
| For Honor Directional | P1 | Hoch | Muss ausgearbeitet werden |
| Softy-Modus | P2 | Mittel | Design fertig |
| Echoharp-Questline | P2 | Mittel | Questline fertig, Artefakt-Bonus OFFEN |

### Naechste Schritte:
1. **For Honor Combat** genau ausarbeiten (Animations, Input-Mapping, Balance)
2. **Safe-Zone Logik** in bestehenden Code integrieren
3. **FF7 Mini-Staedte** als UE5 Feature planen
4. **Softy-Modus** Server-Logik entwerfen
5. **Echoharp Artefakt-Bonus** festlegen wenn Balancing klarer ist

---

**Ende - Neue Gameplay-Ideen 2026-02-21**
