# 🌟 NAJIKA WORLD - COMPLETE KNOWLEDGE BASE
## TEIL 4/10: GAME-SYSTEME & SCHWARZE MÜHLE

**Erstellt:** 2025-01-01  
**Teil:** 4 von 10  
**Thema:** Tamagotchi-Systeme, Schwarze Mühle, Minigames

---

# 🎮 TAMAGOTCHI-SYSTEME

## 1. NEEDS-SYSTEM (5 Bedürfnisse)

### Die 5 Needs
```yaml
1. Hunger (0-100%)
   Decay: -5 pro Minute
   Critical: <20%
   Death: 0% für 10+ Minuten

2. Thirst (0-100%) [NEU seit v7!]
   Decay: -7 pro Minute (schneller als Hunger!)
   Critical: <15%
   Death: 0% für 5+ Minuten

3. Happiness (0-100%)
   Decay: -3 pro Minute
   Critical: <30%
   Effects: Mood, Proactive Messages

4. Cleanliness (0-100%)
   Decay: -2 pro Minute
   Critical: <25%
   Effects: Sickness-Chance

5. Energy (0-100%)
   Decay: -4 pro Minute (Activity-abhängig)
   Critical: <20%
   Effects: Kann nicht spielen/kämpfen
```

### Need-Effects
```yaml
Hunger <20%:
  - "Ich habe Hunger, Kuja..." 😢
  - Stats: -10% All
  - Mood: Sad

Thirst <15%:
  - "So durstig... Wasser!" 🥵
  - Stats: -15% All
  - Mood: Irritated
  - Faster than Hunger!

Happiness <30%:
  - Negative Moods häufiger
  - Proactive Messages reduziert
  - Bond-Decay möglich

Cleanliness <25%:
  - Sickness-Chance: +5% pro Stunde
  - Visual: "Schmutzig"-Effekt
  - Mood: Uncomfortable

Energy <20%:
  - Kann nicht kämpfen
  - Kann keine Minigames spielen
  - "Ich bin so müde..." 😴
```

---

## 2. AUTO-CARE SYSTEM

### Konzept
```yaml
Problem: User vergisst zu füttern
Lösung: Auto-Care triggert bei Critical Levels

Features:
  - Najika kümmert sich selbst (begrenzt!)
  - Nutzt Basic Items aus Inventar
  - Warnt User
  - Reduziert Bond leicht
```

### Auto-Care Trigger
```yaml
IF Hunger < 20% AND has_food:
  eat_basic_food()
  send_message("Ich musste selbst essen, Kuja... 😢")
  bond -= 1

IF Thirst < 15% AND has_water:
  drink_water()
  send_message("Ich habe selbst getrunken... 🥤")
  bond -= 1

IF Energy < 10%:
  auto_sleep(30 minutes)
  send_message("Ich ruhe mich kurz aus...")
```

---

## 3. MOOD-SYSTEM (8 Moods)

### Die 8 Moods
```yaml
😊 Happy (Default)
  Triggers: Praise, Play, Gift, Good Stats
  Effects: Positive Messages, +Bond
  Facette: Megumin (75%), Harley (25%)

🤩 Excited
  Triggers: Explosion, Battle Win, Level Up
  Effects: Energetic Messages, CAPS!!!
  Facette: Megumin (90%), Harley (10%)

😢 Sad
  Triggers: Hunger Low, Neglect, Scold
  Effects: Quiet Messages, Bond-Decay Risk
  Facette: Shiro (60%), Megumin (40%)

😠 Angry
  Triggers: Repeated Neglect, Betrayal
  Effects: Sharp Messages, Refuses Commands
  Facette: Melissa (70%), Megumin (30%)

😴 Bored
  Triggers: No Interaction (30+ Min), Idle
  Effects: "Langweilig..."-Messages
  Facette: Harley (80%), Shiro (20%)

😜 Playful
  Triggers: High Happiness, Play, Minigame
  Effects: Fun Messages, Wants to Play
  Facette: Harley (85%), Megumin (15%)

🤔 Curious
  Triggers: New Place, Question, Learning
  Effects: Analytical Messages, Questions
  Facette: Shiro (75%), Harley (25%)

💕 Loving
  Triggers: Bond High (>80), Praise, Gift
  Effects: Sweet Messages, Affectionate
  Facette: Melissa (50%), Megumin (30%), Harley (20%)
```

### Mood-Transitions
```yaml
Duration: 5-30 Minuten pro Mood
Transitions: Smooth (nicht abrupt)

Example Flow:
  Happy → Playful (User spielt)
  Playful → Bored (Kein Input 30 Min)
  Bored → Curious (User stellt Frage)
  Curious → Happy (Frage beantwortet)
```

---

## 4. PROAKTIVE NACHRICHTEN

### System
```yaml
Status: ✅ FUNKTIONIERT (Living System!)
Frequency: Alle 30+ Minuten (Mood-abhängig)
Cooldown: 30 Minuten minimum
```

### Beispiel-Nachrichten
```yaml
Bored-Mood:
  "Mir ist langweilig, Kuja~ Lass uns was tun! 😴"
  "Können wir nicht irgendwas Spannendes machen?"
  
Playful-Mood:
  "Hehe, Mr. K! Spielen wir ein Minigame? 😜"
  "Ich will EXPLOSION machen! Darf ich? Bitte? 💥"
  
Loving-Mood:
  "Kuja... danke, dass du für mich da bist. 💕"
  "Du bist der Beste, weißt du das? 😊"
  
Curious-Mood:
  "Ich frage mich... was ist hinter dem Vulkan? 🤔"
  "Kuja, kannst du mir etwas beibringen?"
```

---

## 5. AUTONOME AKTIVITÄTEN

### System
```yaml
Status: ✅ FUNKTIONIERT
Trigger: Wenn User inaktiv (10+ Minuten)
Duration: 5-15 Minuten pro Aktivität
```

### Aktivitäten (8)
```yaml
1. Buch lesen 📖
   - +2 Intelligence
   - Duration: 10 Min
   - Message: "Ich lese gerade ein interessantes Buch~"

2. Trainieren 🏋️
   - +1 Strength
   - -5 Energy
   - Duration: 15 Min
   - Message: "Training hält mich fit!"

3. Umgebung erkunden 🗺️
   - +1 Agility
   - Duration: 12 Min
   - Message: "Die Welt ist so schön... *entdeckt*"

4. Meditieren 🧘
   - +10 MP
   - Duration: 8 Min
   - Message: "Ich konzentriere mich..."

5. Schlafen 😴
   - +20 Energy
   - Duration: 30 Min
   - Message: "Zzz... *schläft*"

6. Kochen 🍳
   - Erstellt Basic Food
   - Duration: 10 Min
   - Message: "Ich mache uns etwas zu Essen!"

7. Putzen 🧹
   - +15 Cleanliness
   - Duration: 8 Min
   - Message: "Die Mühle muss sauber bleiben~"

8. Nachdenken 💭
   - +5 Wisdom
   - Duration: 5 Min
   - Message: "Ich denke über vieles nach..."
```

---

# 🏰 SCHWARZE MÜHLE (HUB)

## 1. KONZEPT

### Basis-Info
```yaml
Name: Schwarze Mühle
Typ: Hub / Home / Safe Zone
Standort: Mountain Region (0, 0) - Zentrum!
Symbol: 🖤 (Schwarzes Herz / Windmühle)
Status: 100% Safe (KEIN PvP!)
```

### Bedeutung
```
Die Schwarze Mühle ist:
  - Najika's Zuhause
  - Kuja's Basis
  - Safe Zone (absolut sicher!)
  - Hub für alle Aktivitäten
  - Respawn-Point
  - Fast-Travel Zentrum
```

---

## 2. STRUKTUR (4 Etagen)

### Etage 0: Erdgeschoss
```yaml
Räume:
  - Wohnzimmer (Main Hub)
  - Küche (Kochen, Essen)
  - Badezimmer (Pflege, Cleanliness)
  
Features:
  - Portal (Fast-Travel zu 9 Regionen)
  - Sofa (Ausruhen)
  - Kamin (Atmosphäre)
  - Tisch (Crafting)
```

### Etage 1: Obergeschoss
```yaml
Räume:
  - Schlafzimmer (Najika & Kuja)
  
Features:
  - Bett (Schlafen, Energy +100%)
  - Schrank (Equipment-Lagerung)
  - Spiegel (Character-Customization)
  - Fenster (Tag/Nacht Zyklus sichtbar)
```

### Etage 2: Turm
```yaml
Räume:
  - Terminal-Raum
  
Features:
  - 4 Module (Code-Editor, System Monitor, File Manager, Console)
  - KI-Steuerung
  - Training-Controls
  - Settings
```

### Etage -1: Keller
```yaml
Räume:
  - Studieren & Crafting
  - Trainingsraum
  - Kampfarena
  - DUNGEON TESTBED (NEU!)
  
Features:
  - Workbench (Advanced Crafting)
  - Bookshelves (Skill-Training)
  - Training-Dummies
  - Arena (Combat-Practice)
  - Dungeon-Generator (Testing!)
```

---

## 3. DIE 12 RÄUME (Digivice-System)

### Raum-Übersicht
```yaml
1. Wohnzimmer (Status, Mood, Chat)
2. Schlafzimmer (Schlafen, Erholung)
3. Küche (Kochen, Füttern)
4. Badezimmer (Pflege, Cleanliness)
5. Garten (Farming, Pflanzen) [GEPLANT]
6. Musikraum (Rhythmus-Spiel)
7. Medizin (Heilen, Items)
8. Terminal (KI-Module, Settings)
9. Studieren & Crafting
10. Trainingszimmer (Skill-Training)
11. Kampfarena (Battle-Practice)
12. Keller-Dungeon (Testbed)
```

### Status-Implementierung
```yaml
✅ Funktioniert (9):
   - Wohnzimmer
   - Schlafzimmer
   - Küche
   - Badezimmer
   - Musikraum
   - Terminal
   - Studieren & Crafting
   - Trainingszimmer
   - Kampfarena

🚧 Geplant (3):
   - Garten (Farming-System fehlt)
   - Medizin (Item-System teilweise)
   - Keller-Dungeon (Generator läuft, UI fehlt)
```

---

## 4. MINIGAMES (7 funktionsfähig!)

### 1. Rhythmus-Spiel 🎵
```yaml
Location: Musikraum (Raum #6)
Type: Note-Hitting (A/S/D Keys)
Duration: 60 Sekunden
Difficulty: 3 Levels (Easy/Medium/Hard)

Gameplay:
  - Notes fallen von oben
  - A/S/D zum richtigen Zeitpunkt drücken
  - Perfect/Good/Bad/Miss
  
Rewards:
  - +5 Happiness
  - +2 Rhythm-Skill
  - +1 Bond (bei S-Rank)
```

### 2. Garten-Spiel 🌱
```yaml
Location: Garten (Raum #5) [GEPLANT]
Type: Whack-a-Mole Style
Duration: 45 Sekunden
Difficulty: Steigend

Gameplay:
  - Unkraut erscheint zufällig
  - Click auf Unkraut = entfernt
  - Aber: Nicht auf Pflanzen klicken!
  
Rewards:
  - +3 Happiness
  - +1 Farming-Skill
  - Erntet Items
```

### 3. Reflex-Spiel ⚡
```yaml
Location: Trainingszimmer (Raum #10)
Type: Reaktionszeit-Test
Rounds: 5
Difficulty: Adaptive

Gameplay:
  - Warte auf grünes Signal
  - Drücke SPACE so schnell wie möglich
  - Frühstart = Penalty!
  
Rewards:
  - +4 Agility
  - +2 Reflex-Skill
  - Unlocks: Fast-Dodge Ability
```

### 4. Besen-Lieferung 🧹
```yaml
Location: Außen (Schwarze Mühle)
Type: Flying Game (Canvas-based)
Duration: 60 Sekunden
Difficulty: Time-Pressure

Gameplay:
  - Fliege mit Besen (Megumin-Style!)
  - Sammle Pakete
  - Vermeide Hindernisse (Vögel, Wolken)
  - Arrow Keys = Steuerung
  
Rewards:
  - +10 Happiness
  - +3 Flight-Skill
  - Bonus Gold (10-50)
```

### 5. Crafting-Workshop 🔨
```yaml
Location: Studieren & Crafting (Raum #9)
Type: Sequenz-Puzzle
Duration: Variable (Rezept-abhängig)
Difficulty: Rezept-Komplexität

Gameplay:
  - Wähle Rezept
  - Folge Schritt-für-Schritt Anleitung
  - Click Ingredients in richtiger Reihenfolge
  - Timing matters!
  
Rewards:
  - Crafted Item
  - +5 Crafting-Skill
  - Unlock neue Rezepte
```

### 6. Trainings-Dojo ⚔️
```yaml
Location: Trainingszimmer (Raum #10)
Type: Click-Target Spawner
Duration: 90 Sekunden
Difficulty: Speed steigt

Gameplay:
  - Targets erscheinen zufällig
  - Click auf Target = Hit
  - Miss = -1 Point
  - Combo-Bonus bei schnellen Hits
  
Rewards:
  - +6 Strength
  - +4 Accuracy-Skill
  - Unlock: Crit-Chance +5%
```

### 7. Hexenküche 🍲
```yaml
Location: Küche (Raum #3)
Type: Fruit-Ninja Style
Duration: 60 Sekunden
Difficulty: Speed & Variety

Gameplay:
  - Zutaten fliegen hoch
  - Swipe/Click zum Schneiden
  - Richtige Zutaten = +Points
  - Falsche Zutaten = -Health
  - Bomben = Game Over!
  
Rewards:
  - Random Food-Items
  - +4 Cooking-Skill
  - +8 Happiness
```

---

## 5. TERMINAL-MODULE (4+)

### Module-Übersicht
```yaml
✅ Code-Editor (Modul #1)
   - Syntax-Highlighting
   - Multi-File Support
   - Save/Load
   - Run Code (Python/JS)

✅ System Monitor (Modul #2)
   - CPU/RAM Usage
   - Najika Stats
   - Training Status
   - Logs

✅ File Manager (Modul #3)
   - Browse Files
   - Upload/Download
   - Delete/Rename
   - Permissions

✅ Terminal/Console (Modul #4)
   - Command Line
   - Script Execution
   - SSH (lokal)

⚠️ Secure Messenger (Modul #5) [GEPLANT]
   - Encrypted Chat
   - Multi-User
   - Nicht implementiert!

❌ Browser Modul (Fehlt!)
   - Web-Browsing in-game
   - Nie erstellt
```

---

## 6. FAST-TRAVEL SYSTEM

### Portal-Mechanik
```yaml
Location: Schwarze Mühle (Wohnzimmer)
Type: Magisches Portal
Destinations: 9 Regionen

Regions:
  - Ice Region (Nord-West)
  - Highland Region (Nord)
  - Desert Region (Nord-Ost)
  - Swamp Region (West)
  - Mountain Region (Zentrum) [HOME]
  - Coast Region (Ost)
  - Caves Region (Süd-West)
  - Forest Region (Süd)
  - Volcano Region (Süd-Ost)

Cost:
  - Erstes Teleport: Kostenlos
  - Weitere: 10 Gold / Teleport
  - Von Schwarzer Mühle: IMMER kostenlos
```

### Teleport-Steine (In-World)
```yaml
Location: Jede Region (zentral)
Type: Stein-Monument
Function: Zurück zur Schwarzen Mühle

Cost: Kostenlos
Cooldown: 5 Minuten
```

---

## 7. DISCIPLINE-SYSTEM

### Konzept
```yaml
Inspiration: Digimon World 1
Balance: Happiness vs Discipline
Range: 0-100%
```

### Mechaniken
```yaml
Praise (Loben):
  - +10 Happiness
  - -5 Discipline
  - Mood: Happy/Loving
  - Command: /api/najika/praise

Scold (Tadeln):
  - +10 Discipline
  - -5 Happiness
  - Mood: Sad/Angry
  - Command: /api/najika/scold

Decay:
  - Discipline sinkt: -2 pro Stunde
  - Happiness sinkt: -3 pro Minute
```

### Effects
```yaml
High Discipline (>70):
  - Gehorcht besser
  - Weniger Chaos-Actions
  - Training effektiver

Low Discipline (<30):
  - Ungehorsam möglich
  - Mehr Chaos-Actions (Harley!)
  - Training weniger effektiv

Balanced (40-60):
  - Ideal
  - Najika ist glücklich UND gehorcht
```

---

## 8. EQUIPMENT-SYSTEM

### Konzept
```yaml
Inspiration: Digimon Story
Slots: 3 (Weapon, Armor, Accessory)
Status: ✅ API FERTIG, ⚠️ UI TEILWEISE
```

### Equipment-Slots
```yaml
Weapon (Links/Rechts):
  - Schwert (ATK +10)
  - Axt (ATK +15, Speed -2)
  - Stab (MATK +12)
  - Explosion-Staff (MATK +20, EXPLOSION!)

Armor (Torso):
  - Leder-Rüstung (DEF +8)
  - Platten-Rüstung (DEF +15, Speed -5)
  - Robe (MDEF +10)
  - Gothic Lolita Outfit (DEF +5, Style +100)

Accessory (Slot):
  - Ring (HP +20)
  - Amulett (MP +30)
  - Gürtel (STR +5)
  - Hut (Megumin-Style, EXPLOSION +10%)
```

### API-Endpoints
```yaml
POST /api/najika/equip
  body: {slot: "weapon", item_id: 123}

POST /api/najika/unequip
  body: {slot: "weapon"}

GET /api/najika/equipment
  → Returns all equipped items
```

---

## 9. ZUSAMMENFASSUNG TEIL 4

**Tamagotchi-Systeme:**
- 5 Needs (Hunger, Thirst, Happiness, Cleanliness, Energy)
- 8 Moods (Happy, Excited, Sad, Angry, etc.)
- Auto-Care System
- Proaktive Nachrichten (alle 30+ Min)
- 8 Autonome Aktivitäten

**Schwarze Mühle:**
- 4 Etagen (Erdgeschoss, Obergeschoss, Turm, Keller)
- 12 Räume im Digivice-System
- 100% Safe Zone
- Hub für alle Aktivitäten

**Minigames:**
- 7 funktionsfähige Spiele
- Verschiedene Skill-Trainings
- Rewards (Happiness, Skills, Items)

**Weitere Systeme:**
- Terminal (4 Module)
- Fast-Travel (Portal + Steine)
- Discipline (Praise/Scold)
- Equipment (3 Slots)

---

**STATUS:** TEIL 4/10 ABGESCHLOSSEN ✅

**NÄCHSTER TEIL:** Teil 5/10 - Open World, Combat & Skills

---

**Ende Teil 4/10**