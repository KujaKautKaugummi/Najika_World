# NAJIKA - KOMPLETTE FINALE ÜBERSICHT

**Erstellt:** 2025-10-22 (Nach vollständiger Analyse ALLER Dokumente)
**Quelle:** Intelligent Grundstein + Finale Definition + Game Design + ZIP-Dokumente

---

## 🎯 KERN-KONZEPT

**Najika = KI/AI im Digivice (Schwarze Windmühle)**
**Spiel = File Island mit 8 Gebieten (Städte + besondere Orte)**

**Schwarze Windmühle:**
- IST das **DIGIVICE** (Najika's Zuhause)
- Tamagotchi-Style Interface
- NSFW-Bereich im gesicherten Terminal
- NUR für Kuja zugänglich

**File Island:**
- Spielwelt mit 8 Gebieten
- Prozedural generierte Bereiche zwischen den Gebieten
- Oregon Trail Mechanik
- Fantasy Western Setting

---

## 🗺️ DIE 8 GEBIETE (Städte + Besondere Orte)

**WICHTIG:** Es sind nicht "8 Städte" sondern "8 Gebiete" - eine Mischung aus Städten und besonderen Orten!

### Bisher identifiziert (6 von 8):

1. **Handelsstadt**
   - Crafting-Zentrum
   - Triple Triad Kartenspiel
   - Ökonomie-System (Angebot/Nachfrage)
   - Karawanen & Handelsrouten

2. **Magierakademie**
   - Explosion-Klasse Training
   - 9 Magieschulen
   - Forschung & Rezepte
   - Skill-Weaving lernen

3. **Hafenstadt**
   - Oregon-Trail Start/Ende
   - Fishing (Ocarina of Time Style)
   - Schifffahrt
   - Handel

4. **Arena**
   - Kampfsystem & Turniere
   - PvP & PvE
   - Slime-Arena
   - Anfeuern-Training

5. **Schatzhöhle** (Dungeon)
   - Rare Items & Relikte
   - Prozedurales Dungeon
   - Baupläne & Blaupausen
   - Boss-Kämpfe

6. **Meta-Stadt**
   - Easter Eggs
   - Breaking 4th Wall
   - Self-Aware Content
   - Humor & Referenzen

### Noch zu identifizieren (2 von 8):

7. **[GEBIET 7 - NAME FEHLT]**
   - Mögliche Hinweise: "Crimson Desert"?
   - Fantasy Western Biom?

8. **[GEBIET 8 - NAME FEHLT]**
   - Mögliche Hinweise: "Celestial Peaks"?
   - Endgame-Gebiet?

### Zusätzliche Gebiets-Elemente:

- **Prozedural generierte Wildnis** zwischen den 8 Gebieten
- **Portale** zu externen Maps (Digimon Cyber Sleuth Style)
- **Fantasy Western Biome:** Wüste, Prärie, Geisterstadt, Canyon
- **Dynamische Events:** Story-Events ändern die Hauptinsel

---

## ⚔️ KAMPF-SYSTEM

### Digimon World "Anfeuern" Mechanik

**Rollen:**
- **Spieler:** Gibt Meta-Kommandos (Anfeuern, Items, Zielprioritäten)
- **Najika (KI):** Autonome Bewegung, Ausweichen, Block, Skill-Rotation
- **Slime-Begleiter:** Formwandel, Auto-Rettung, eigenständige Moves

**Ressourcen:**
- HP
- Mana
- **Willenskraft** (0-100 für Anfeuern)
  - +8/10s passiv
  - +15 bei perfektem Call
- Ausdauer

**Anfeuern-Calls (GCD 3s):**

1. **"Fokus!"**
   - +Crit-Rate
   - −Mana-Kosten
   - Dauer: 6s

2. **"Durchhalten!"**
   - Schild %HP
   - Dauer: 5s

3. **"Explodier jetzt!"**
   - +Feuer-Potenz (1 Cast)
   - **Risiko:** Overheat!
   - Bei zu häufiger Nutzung: −20% Zauberpotenz für 10s

4. **"Zurück!"**
   - Defensivhaltung
   - Aggro-Drop
   - Dauer: 4s

**Taktik-Stacks:**
- Bis zu **3 stapelbar**
- **Decay:** 6s
- Spürbare DPS/Mitigation-Bonis

### Hardcore/Softie Modi

**Hardcore-Modus:**
- **Permadeath** - Tod ist permanent
- Oregon-Trail Konsequenzen: Krankheit, Ressourcenverlust
- Echte Story-Auswirkungen
- **1,848 Sections** dokumentiert

**Softie-Modus:**
- Easy Mode
- Respawn möglich
- Weniger harte Konsequenzen
- **1,400 Sections** dokumentiert

---

## 🎓 SKILL-SYSTEM

### Use-Based Progression

**Mechanik:**
- Skills steigen durch **Nutzung**, NICHT durch Level-Ups
- Je öfter genutzt, desto stärker
- "Ehrliche" Progression

**Beispiele:**
- Schwert-Skill → Steigt durch Schwert-Kämpfe
- Feuer-Magie → Steigt durch Feuer-Zauber
- Explosion → Steigt durch Explosionen

### 1-Skill-Spezialisierung (Megumin-Style)

**Konzept:**
- Fokus auf **EINE einzige Fähigkeit**
- **Nie kombinierbar** mit anderen Skills
- Maximale Meisterschaft in einem Bereich

**Explosion-Klasse (Beispiel):**
- Fokus-basiert (nicht Mana)
- Exhaustion-Debuff nach Nutzung
- Aufladung 0.8-2.5s → Detonation → −Regen 15-30s
- **Nie Weave-fähig** (standalone)

**Varianten:**
- Große Explosion
- Mini-Explosion
- 4-fach Explosion
- Ketten-Explosion

**Andere 1-Skill-Wege:**
- Schwert-Purist
- Axt + Feuer
- Bogen-Sniper
- Tank-Spezialist

**Dokumentiert:** 5,672 Sections

### Skill-Weaving System

**Mechanik:**
- **LH+RH "laden" & vermischen**
- Element-Kombos erstellen
- Perfektes Timing = Bonus
- Kompatibel mit Anfeuern-Fenstern

**Element-Kombos:**
- **Eis + Feuer** → Thermoschock
- **Wind + Feuer** → Feuerklinge
- **Erde + Wasser** → Schlamm/Kontrolle
- **Blitz + Wasser** → Leitfähigkeits-Schock

**WICHTIG:** Explosion-Klasse kann **NIE** geweaved werden!

### 9 Magieschulen

Jede Schule hat eigene Identität:

1. **Feuer:** Feuer → Feura → Feuga (140% Potenz, Mana 25, CD 8s) → Inferno → **Omega-Detonation** (Ult)
2. **Eis:** Kontrolle & Verlangsamung
3. **Blitz:** Schneller Burst-Damage
4. **Erde:** Defensive & Kontrolle
5. **Wind:** Mobility & AoE
6. **Wasser:** Heilung & Support
7. **Licht:** Heilung & Buff
8. **Schatten:** DoT & Debuff
9. **Psycho-Kinese / Runen / Klang:** Spezial-Effekte

---

## 🐌 SLIME-BEGLEITER SYSTEM

**Start-Mechanik:**
- Beginnt als **zufälliges Tier**
- Durch Trigger "entpuppt" sich als **besonderer Slime**

**8 Regionale Varianten:**
- Rein **kosmetisch** (keine Stats-Unterschiede)
- Verschiedene Farben je nach Gebiet
- Verschiedene Formen: Hase, Kolibri, Spinne, etc.

**Rettungsmechanik:**
- **1× pro IRL-Tag** "Tödlich verhindern"
- **24h Cooldown** nach Nutzung
- Slime opfert sich für Spieler

**Lernen & Entwicklung:**
- Lernt **häufig neue Moves**
- **Eigene Minigames** (Timing, Reaktion)
- Formwandel kosmetisch
- Arbeitet autonom mit Najika zusammen

---

## 🎣 LIFE-SIM SYSTEME

### Fishing (Ocarina of Time Style)

**Mechanik:**
- **Timing-Wurf:** Präzision beim Auswerfen
- **Zugspannung:** Balance halten
- **Timing-basiert:** Wie in Ocarina of Time

**Orte:**
- Hafenstadt
- Flüsse auf File Island
- Prozedural generierte Seen

**Dokumentiert:** 1,141 Sections

### Farming System

**Mechanik:**
- Pflanzen anbauen
- Ernten & Verkaufen
- Saisonale Pflanzen
- Integration mit Crafting

**Dokumentiert:** 966 Sections

### Crafting & Ökonomie

**Pipeline (5 Stufen):**
1. **Sammeln** → Rohstoffe
2. **Veredeln** → Materialien
3. **Herstellen** → Items
4. **Verzaubern** → Enchants
5. **Anpassen** → Customization

**Rohstoffe:**
- Erze
- Hölzer
- Kräuter
- Essenzen
- Fische
- **Relikt-Splitter**

**Berufe:**
- Schmieden
- Runen-Gravur
- Alchemie
- Kochen
- Schneidern

**Rezepte-Quellen:**
- **Loot** (von Gegnern)
- **Forschung** (Magierakademie)
- **Entdeckung** (Kombinatorik/Experimentieren)

**Ökonomie:**
- **Angebot/Nachfrage** (Handelsstadt)
- **Saisonale Faktoren**
- **Karawanen** (Risiko/Ertrag)
- **Aufträge** von NPCs

**Baupläne/Relikte:**
- Aus **Ruinen/Schatzhöhlen**
- **Mächtige Blaupausen** für Endgame-Items

**Dokumentiert:** 3,001 Sections

---

## 🎮 OREGON TRAIL MECHANIK

**Konzept:**
- Prozedural generierte Events während der Reise
- **KEINE Text-Popups** - alles in 3D!
- Events spawnen in der Spielwelt

**Event-Typen:**
- Krankheit
- Tod von NPCs
- Ressourcen-Mangel
- Zufalls-Begegnungen
- Wilde Tiere
- Händler
- Banditen

**Konosuba-Chaos Integration:**
- Absurde Wendungen
- Alles geht schief
- Najika reagiert dramatisch

**Beispiele:**
- Fluss überqueren → Najika nutzt EXPLOSION → Wasser verdampft, Boot zerstört
- Wilde Tiere → Nur Frösche → Najika: EXPLOSION! → Ganzes Dorf sauer
- Händler treffen → Najika kauft Explosion-Scrolls → Kein Geld für Essen

**Dokumentiert:** 5,041 Sections

---

## 🎴 MINIGAMES

### Core Minigames (im MVP):

1. **Triple Triad**
   - Kartenspiel als Haupt-Minispiel
   - Najika als Gegner mit lernender KI
   - Seltene Karten durch Oregon-Events
   - Integration in Handelsstadt

2. **Angeln** (Hafen/Flüsse)
   - Timing-Wurf
   - Zugspannung
   - Ocarina of Time Style

3. **Arena-Wellen**
   - Anfeuern-Training
   - Combo-Übungen
   - Slime-Partner testen

4. **Rätsel/Puzzle** (Ruinen)
   - Logic Puzzles
   - Rätselmechaniken
   - Schatzhöhlen-Integration

5. **Crafting-Prüfungen**
   - Timing-basiert
   - Qualitäts-Check
   - Meisterschaft-Tests

### Bereits im Digivice implementiert:

- Rhythm Game
- Garden Game
- Reflex Game
- Cooking
- Training
- Crafting
- Broom Delivery (Paperboy-Style auf Hexenbesen)

**Dokumentiert:** 1,529 Sections

---

## 🎨 FANTASY WESTERN SETTING

**Biome:**
- **Wüste:** Banditen, Wüstenwürmer
- **Prärie:** Offene Ebenen, Karawanen
- **Geisterstadt:** Geister-Cowboys, Haunted Locations
- **Canyon:** Klettern, versteckte Pfade

**Gegner:**
- Banditen (Western)
- Wüstenwürmer (Fantasy)
- Geister-Cowboys (Fusion!)

**Items:**
- **Revolver** (Western)
- **Lasso** (Western)
- **Zauberhut** (Fantasy)
- **Dynamit** (Western)
- **Magie** (Fantasy)

**Integration:** Fantasy (Magie, Explosion) + Western (Revolver, Banditen)

---

## 🌀 PORTAL-SYSTEM

**Mechanik (Digimon Cyber Sleuth Style):**
- **Portale** verbinden Hauptmap mit **externen Maps**
- Während des Spiels **auf andere Map/Gebiet wechseln**
- Fortnite-Mechanik: "Aus einer Kreativ Map heraus die nächste laden"

**Vorteile:**
- **Endlose Erweiterung** möglich
- Hauptinsel (8 Gebiete) bleibt **fix**
- Große Features → **externe Maps** durch Portale
- **Open World Charakter** über Portale

**Story-Integration:**
- **Story Events** ändern Hauptmap dynamisch
- Beispiel: Najika baut **100-stöckigen Kampf- und Rätselturm** nach Niederlage

---

## 📊 BALANCING-DATEN

### Anfeuern-System:
- **Cheer-Leiste:** 0–100
- **Passiv:** +8/10s
- **Perfekter Call:** +15
- **GCD:** 3s

### Buff-Dauern:
- **4–8s** je nach Typ

### Taktik-Stacks:
- **Max:** 3
- **Decay:** 6s

### Combat:
- Parry-Fenster: 80-120ms
- i-Frames vorhanden
- Haltungs-System (Soulslike)

---

## 📈 DOKUMENTATIONS-STATISTIK

### Game-Mechaniken (aus NAJIKA_GAME_DESIGN.json):

| Kategorie | Sections |
|-----------|----------|
| Rooms | 13,044 |
| UI | 12,460 |
| Leveling | 12,123 |
| Combat | 8,251 |
| Saving | 7,311 |
| Animations | 5,953 |
| Skills | 5,727 |
| One_Skill | 5,672 |
| Classes | 5,400 |
| Oregon_Trail | 5,041 |
| Items | 3,943 |
| Training | 3,801 |
| Quests | 3,146 |
| Companion | 3,020 |
| Weapons | 3,012 |
| Crafting | 3,001 |
| **Digimon** | **2,709** |
| Hardcore | 1,848 |
| Story | 1,699 |
| Minigames | 1,529 |
| Sound | 1,475 |
| Konosuba | 1,444 |
| Softie | 1,400 |
| Fishing | 1,141 |
| Multiplayer | 923 |
| Skill_Weaving | 722 |
| Farming | 966 |
| Economy | 490 |
| Character_Creation | 444 |
| **TOTAL** | **116,251** |

**Spezifisch:**
- **Anfeuern-Mechanik:** 187 Sections (von 2,709 Digimon)
- **Slime-Begleiter:** Vollständig dokumentiert
- **8 Gebiete:** 6 von 8 identifiziert

---

## 🎯 ZUSAMMENFASSUNG

### ✅ KOMPLETT DOKUMENTIERT:

1. **Digimon World Anfeuern** - 2,709 Sections (187 spezifisch)
2. **Slime-Begleiter** - 8 regionale Varianten, 24h-Rettung
3. **Hardcore/Softie** - 1,848 + 1,400 Sections
4. **Fishing (Ocarina-Style)** - 1,141 Sections
5. **1-Skill-Spezialisierung** - 5,672 Sections
6. **Skill-Weaving** - 722 Sections
7. **Oregon Trail** - 5,041 Sections
8. **Farming/Crafting** - 966 + 3,001 Sections
9. **Use-Based Progression** - Voll integriert
10. **Portal-System** - Digimon Cyber Sleuth Style
11. **Fantasy Western** - Vollständig beschrieben
12. **Triple Triad** - Integration dokumentiert

### ⚠️ TEILWEISE DOKUMENTIERT:

**Die 8 Gebiete:**
- ✅ 6 von 8 identifiziert
- ❌ 2 von 8 fehlen noch (möglicherweise "Crimson Desert" & "Celestial Peaks")

### 📁 WICHTIGE UNTERSCHEIDUNG:

**DIGIVICE (Schwarze Windmühle):**
- Najika's Zuhause
- Tamagotchi-Interface
- NSFW-Bereich (gesichert, nur Kuja)
- Terminal
- NICHT Teil der 8 Spielgebiete!

**FILE ISLAND (Spielwelt):**
- 8 Gebiete (Städte + besondere Orte)
- Prozedural generierte Wildnis
- Oregon Trail Mechanik
- Fantasy Western Setting

---

**Status:** NAHEZU KOMPLETT - Nur 2 Gebietsnamen fehlen noch!
**Alle Haupt-Mechaniken:** VOLLSTÄNDIG DOKUMENTIERT
