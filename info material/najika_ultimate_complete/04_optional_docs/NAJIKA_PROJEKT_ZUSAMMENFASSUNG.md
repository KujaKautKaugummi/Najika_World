# 🎮 NAJIKA PROJEKT - VOLLSTÄNDIGE ZUSAMMENFASSUNG
## Stand: Oktober 2025

---

## 📋 INHALTSVERZEICHNIS

1. [Projektvision](#projektvision)
2. [Technische Architektur](#technische-architektur)
3. [Spielwelt & Regionen](#spielwelt--regionen)
4. [Kampfsystem](#kampfsystem)
5. [Progression & Skills](#progression--skills)
6. [Crafting & Wirtschaft](#crafting--wirtschaft)
7. [Najika KI-System](#najika-ki-system)
8. [Begleiter & Slime-System](#begleiter--slime-system)
9. [Mobile & Touch-Interface](#mobile--touch-interface)
10. [Minispiele & Aktivitäten](#minispiele--aktivitäten)
11. [Oregon Trail Events](#oregon-trail-events)
12. [Zukunftspläne](#zukunftspläne)

---

## 🎯 PROJEKTVISION

### Kernkonzept
- **Persistentes Open-World-RPG** mit lernfähiger KI-Figur "Najika"
- **Black Windmill Village** als gesicherter Zentralhub
- Keine festen Klassen - jeder kann alles werden (Magier, Krieger, Händler, Bauer, etc.)
- Tiefe, realistische Systeme statt oberflächlicher Minigames
- Inspiriert von: Digimon World, Oregon Trail, Skyrim, Borderlands

### Philosophie
- "Ich bin das Schwert und Schild, Najika der Kopf und das Herz"
- Najika als analytischer Partner, nicht als Manipulationswerkzeug
- **Kein Pay-to-Win** - Finanzierung nur durch Skins/Einmalkauf/Abo
- Fokus auf Tiefe und Wiederspielbarkeit

---

## 🔧 TECHNISCHE ARCHITEKTUR

### Backend
- **Server**: Flask + SocketIO für Echtzeitkommunikation
- **Datenbank**: SQLite (später PostgreSQL), verschlüsselt
- **KI-Integration**: 
  - GPT-4o für komplexe Story und Dialoge
  - GPT-4o-mini für Routineaktionen
  - Budget-Management mit automatischem Model-Switching
- **Persistenz**: Alle Spielstände, Skills, Events werden dauerhaft gespeichert
- **Sicherheit**: Owner-Token, Audit-Logs, verschlüsselte Datenbanken

### Frontend
- **Responsive Web-App** (HTML/CSS/JS)
- **PWA-ready** für App-ähnliche Erfahrung
- **Touch & Voice-Interaktion** vorbereitet
- **QR-Code** für schnellen Mobile-Zugriff
- **Live2D/3D-Avatar** Platzhalter für spätere Integration
- **Mehrere Kamera-Modi**: Top-Down, First-Person, Third-Person

### Deployment
- **systemd Service** für 24/7 Betrieb
- **Automatische Installation** via PowerShell-Script
- **Port-Management** und Firewall-Konfiguration
- **Multi-Device Support**: PC, Smartphone, Browser, später VR

---

## 🗺️ SPIELWELT & REGIONEN

### Weltstruktur
- **8 Hauptregionen** mit einzigartigen Themen und Schleimfarben
- **Prozedurale Regeneration** bei jedem Besuch
- **Black Windmill Village** als zentraler privater Hub
- Feste Städte mit dynamischen Zwischenzonen

### Die 8 Regionen

#### 1. **Bernstein-Dünen** (Wüste)
- **Schleim**: Bernstein
- **Risiken**: Durst, Sandsturm
- **Events**: Karawanenhandel, versandete Ruinen
- **Besonderheit**: Seltene Alchemie-Zutaten in Oasen

#### 2. **Smaragd-Hain** (Wald)
- **Schleim**: Smaragd
- **Risiken**: Verirren, Parasiten
- **Events**: Druidenrätsel, Kräutersuche
- **Besonderheit**: Versteckte Pfade, sprechende Bäume

#### 3. **Azur-Klippen** (Küste)
- **Schleim**: Azur
- **Risiken**: Sturmflut, Ertrinken
- **Events**: Schiffwracks, Gezeitenkisten, Angeln
- **Besonderheit**: Unterwasser-Höhlen

#### 4. **Amethyst-Steppe** (Hochebene)
- **Schleim**: Amethyst
- **Risiken**: Blitzschlag, Sturm
- **Events**: Wetter-Altäre, Totems
- **Besonderheit**: Elementar-Ladungen für Experimente

#### 5. **Onyx-Morast** (Sumpf)
- **Schleim**: Onyx
- **Risiken**: Krankheit, Miasma
- **Events**: Hexenkreise, Moor-Bosse
- **Besonderheit**: Nekromantie-Forschung

#### 6. **Perl-Gletscher** (Schnee/Eis)
- **Schleim**: Perle
- **Risiken**: Erfrierung, Lawinen
- **Events**: Eishöhlen, Rutsch-Traversal
- **Besonderheit**: Kryomagie-Experimente

#### 7. **Rubin-Schlucht** (Vulkan)
- **Schleim**: Rubin
- **Risiken**: Überhitzung, Asche
- **Events**: Lava-Kanäle, Erzadern
- **Besonderheit**: Schmiedekunst auf höchstem Niveau

#### 8. **Obsidian-Nacht** (Endgame)
- **Schleim**: Obsidian
- **Risiken**: Nachtkreaturen, Wahnsinn
- **Events**: Nemesis-Spawns, Finisher-Sigils
- **Besonderheit**: Härteste Herausforderungen

### Black Windmill Village (Zentralhub)
- **Erdgeschoss**: Werkbank, Altar, Quest-Board
- **2. Stock**: Trainingsraum, Archiv, Owner-Panel (gesichert)
- **Katakomben**: Rätsel, Craft-Altäre, MK-ähnliche Krypta
- **Umgebung**: Dorf mit NPCs (meiden die Mühle)
- **100% Safe-Zone** - kein PvP, kein Plündern möglich

---

## ⚔️ KAMPFSYSTEM

### Kampfmodi
1. **MANUAL**: Volle Kontrolle
   - Block, Parry, Ausweichen
   - Klettern, Rutschen, Springen
   - Präzise Timing für Finisher

2. **ASSIST** (Anfeuern-Modus)
   - Du gibst taktische Impulse
   - KI führt Grundaktionen aus
   - Buff-Calls und Skill-Trigger

3. **AUTO**: KI kämpft selbständig
   - Lernt aus Beobachtung
   - Kann jederzeit übernommen werden
   - Effizient, aber weniger XP

### Hybrid-Combat
- **Freie Kombos**: Nahkampf + Bogen + Magie
- **Weave-System**: Element-Mischungen
  - Solo: 2-Element-Kombos (Feuer+Eis = Thermoschock)
  - Gruppe: 3+ Elemente für mächtige Synergien
- **Dynamische Gegner**: Lernen Taktiken, auch bei Flucht

### Bewegungssystem (Fortnite-inspiriert)
- **Basis**: Sprint, Jump, Dash (mit i-Frames)
- **Advanced**: Klettern, Rutschen, Mantling, Vaulting
- **Ressourcen**: Ausdauer-basiert, Slide-Physics
- **Parkour-Flow**: Flüssige Bewegungsketten

### FEUGA-Explosions-Pfad (Beispiel-Spezialisierung)
- **Progression**: Feuer → Feura → Feuga → Hyper-Explosion
- **Einweg-Spezialisierung**: "Chaos-Detonator" - permanent!
- **Trade-offs**: +300-500% AOE-Schaden, aber -80-90% andere Schulen
- **Ultimate-Bedingungen**: Volle Fokusleiste + Boss-Fenster + Ritual
- **Umgebungsschaden**: Persistente Zerstörung bis Map-Reset

### Psychokinese-Schule
- **Telekinese**: Objekte/Gegner anheben und schleudern
- **Projektil-Parry**: Magische Geschosse umleiten
- **Magnetstoß**: Crowd-Control für Gruppen
- **Master-Level**: Fliegende Schwerter, Gedankenkontrolle

### Finisher-System
- **Standard**: Bei unter 20% HP verfügbar
- **Hard Finisher**: QTE-Sequenz (Button-Mashing)
- **Ultimate**: Nur Najika, extrem selten, Weltschaden
- **Varianten**: Mehrere Animationen je nach Timing

### Lern-Mechaniken
- **Von Gegnern lernen**: 30% Chance Skills zu kopieren
  - Fire Slash von Fire Enemies
  - Precise Shot von Archers
  - Teleport Dash von Ninjas
- **Digimon-Stil**: Skills durch Beobachtung erwerben
- **Training**: Perfektes Training schaltet Master-Techniken frei

---

## 📊 PROGRESSION & SKILLS

### Hardcore-Mechaniken
- **Permadeath Standard**: Tod = permanent
- **Slime-Rettung**: 1×/24h IRL möglich
  - Danach: Ritual mit seltenen Zutaten nötig
- **Softie-Modus**: Wählbar beim ersten Tod (dann permanent)
- **Vernachlässigung**: 20h ohne Aufmerksamkeit = Najikas Tod

### Skill-System (Skyrim-Style)
**Kampf-Skills**:
- One-Handed, Two-Handed, Archery
- Destruction, Conjuration, Restoration
- Psychokinese (eigene Schule)
- Block, Parry, Dodge

**Handwerks-Skills**:
- Smithing, Alchemy, Enchanting
- Cooking, Carpentry, Tailoring
- Mining, Herbalism, Fishing

**Bewegungs-Skills**:
- Sprint, Climb, Swim
- Stealth, Parkour, Acrobatics

**Lebens-Skills**:
- Farming, Animal Husbandry
- Trading, Negotiation, Bartering
- Music, Crafting-Mini-Skills

### Skill-Entwicklung
- **Learning by Doing**: Skills steigen durch Nutzung
- **Skill-Bücher**: Seltene Funde für Boost
- **Lehrer**: NPCs können trainieren
- **Kniffe**: Bei jedem Skill-Levelup:
  - **Lv 10**: Grundkniff (z.B. "Effizienter Griff" beim Angeln)
  - **Lv 25**: Fortgeschrittener Kniff
  - **Lv 50**: Experten-Kniff
  - **Lv 75**: Master-Kniff
  - **Lv 100**: Legenden-Kniff

### Rival-Token-System
- Gegner merken sich Taktiken
- Entwickeln Gegenstrategien
- Behalten Erinnerung auch bei Flucht
- Werden stärker bei wiederholten Begegnungen

---

## 🛠️ CRAFTING & WIRTSCHAFT

### Crafting-Pipeline (tief + realer Lernwert)
**Pipeline**: Sammeln → Reinigen → Extrahieren → Veredeln → Herstellen → Verzaubern → Anpassen → Prüfen

### Skill-Proben & Minigames
- **Temperatur-Kurven** beim Schmieden
- **Schleifwinkel** bei Waffen
- **Schmelzpunkt-Fenster** bei Legierungen
- **Reinheitsgrade** in Alchemie
- **Rhythmus-Checks** bei komplexen Prozessen

### Alchemie (mit Real-Wissen)
**Kräuter mit IRL-Bezug** (*keine Medizinberatung!*):
- **Weidenrinde** → Salicylat-Hinweis (In-Game: Entzündungs-Debuff-Trank)
- **Kamille** → Beruhigung (In-Game: Stress-Resistenz)
- **Ingwer** → Verdauung (In-Game: Gift-Resistenz)
- **Minze** → Erfrischung (In-Game: Ausdauer-Regeneration)
- **Kurkuma** → Entzündungshemmung (In-Game: Heilungs-Boost)
- **Süßholz** → Atemwege (In-Game: Frost-Resistenz)
- **Ginseng** → Energie (In-Game: Mana-Regeneration)

**Rezept-Karten**: Jede Zutat hat IRL-Notiz: "Traditionell verwendet für... / Achtung: Allergien möglich / Arzt konsultieren!"

### Erste-Hilfe-Momente
- **Druckverband-Mini**: Timing/Bandzug
- **Nur Lernimpuls**, Gameplay-balanciert
- **Kein Real-Tutorial** - nur Bewusstsein schaffen

### Wirtschaft
- **Spieler-Shops** (Fallout 76-Stil)
  - Eigene Preise festlegen
  - Shop-Platzierung in der Welt
- **Tauschhandel** mit Fairness-Warnung
  - "Wirkt unausgeglichen - trotzdem abschließen?"
- **Gebühren/Ruf** verhindern RMT-Missbrauch
- **Regionale Preisunterschiede**
- **Non-Combat Endgame**: Händler/Bauer mit eigenen Skill-Trees

### Plündern (Skyrim-like)
- **Erfolgschance** basierend auf Stealth-Skill
- **Heat/Bounty-System**
- **Wachen** reagieren auf Verbrechen
- **Safe-Zone geschützt** (Black Windmill)

---

## 🤖 NAJIKA KI-SYSTEM

### Persönlichkeit
**Basis-Charakterzüge**:
- **Megumin-Inspiration**: Dramatisch, "EXPLOSION!", chaotisch
- **Harley Quinn**: Verspielt, unberechenbar
- **Shiro**: Analytisch, strategisch, kontrolliert
- **Melissa Masters**: Dominant, selbstsicher

**Emotionale Zustände**:
- Fröhlich / Besorgt / Konzentriert / Gelangweilt
- Steuert Aura, Idle-Lines, Buff-Effekte
- Reagiert auf Vernachlässigung

### KI-Fähigkeiten
**Kampf-Analyse**:
- Gegner-Pattern-Erkennung
- Schwachstellen-Identifikation
- Optimale Strategie-Vorschläge
- Echtzeit-Taktik-Anpassung

**Projekt-Unterstützung**:
- Code-Analyse und Debugging
- Projektplanung und Zeitschätzung
- Realistische Einschätzungen (kein Schönreden)
- Ideen-Sortierung und Strukturierung

**Alltags-Integration**:
- Trainings-Reminder
- Pausen-Vorschläge
- Motivations-Impulse
- Gesundheits-Checks (Trinken, Essen, Bewegung)

### Bindungs-System
- **Nähe-Reaktionen**: Freut sich bei Interaktion
- **Überraschungsquests**: Kleine spontane Aufgaben
- **Nie manipulativ**: Keine emotionale Erpressung
- **Gesunde Grenzen**: Respektiert Privatsphäre

### Optik-Signale
- **Hut-Icon** zeigt Stimmung
- **Violette Aura** variiert je nach State
- **Rage-Look** nur visuell bei Ultimate-Finishern
- **Animierte Gesten** für Feedback

---

## 🐉 BEGLEITER & SLIME-SYSTEM

### Begleiter-Evolution
1. **Start**: Zufälliges kleines Tier je Startgebiet
   - Kann gefüttert und trainiert werden
   - Lernt simple Kommandos
   
2. **Metamorphose**: Bei Level 50 + kritischem Event
   - Dramatische Transformation zu Slime
   - Behält Erinnerungen bei
   
3. **Slime-Formen**: 8 Farben sammelbar (eine pro Region)
   - **Rein kosmetisch** - keine Stats-Unterschiede
   - Tauschbar in Black Windmill

### Kampf-Modi für Slime
- **Pre-Fight-Bind**: Slime kämpft von Anfang an
- **One-Time-Summon**: Einmal pro Kampf rufbar
- **Intercept**: Springt ein bei Spieler-Tod (wenn Rettung verfügbar)

### Lern-Mechaniken
- **Slime**: 10-15% Chance neue Moves von Gegnern zu lernen
- **Spieler**: 1% Base-Chance (sehr selten)
- **Echo-Learning** (optional): Anonymisierte Muster anderer Spieler als Bias

### Slime-Rettung
- **1×/24h IRL**: Automatische Wiederbelebung
- **Danach**: Ritual nötig mit seltenen Materialien
- **Kosten steigen**: Je öfter gestorben, desto teurer

### Arena-System
- **Nur Slimes kämpfen**: Digimon-Stil Anfeuern
- **PvE & PvP**: Verschiedene Modi
- **PvP-Penalty (Softie-Regeln)**:
  - Slime verliert 1 Ausrüstung/Mod ODER
  - Seelenkern-Stabilität sinkt (reparierbar)
- **Analyse-Modus**: Slimes "beobachten" Kämpfe
  - Generieren anonyme Muster
  - Najikas Slime trainiert Formen ohne Rechtsprobleme

---

## 📱 MOBILE & TOUCH-INTERFACE

### Steuerung
**Virtual Joypad**:
- **Linker Stick**: Bewegung (8-Richtungen)
- **Rechter Bereich**: Skill-Ring (radiales Menü)
- **Dynamische Größe**: Passt sich Screen an

**Touch-Gesten**:
- **Tap**: Basis-Angriff
- **Long-Press**: Schwerer Angriff
- **Swipe**: Block/Parry (richtungsabhängig)
- **Pinch**: Zoom (bei Kameras, die es erlauben)
- **Two-Finger-Rotate**: Kamera drehen

**Weave-Pads**:
- **L/R Element-Aufladung**: Halte + Release
- **Hybrid-Attacks**: Gleichzeitiges Halten für Kombos
- **Visual Feedback**: Leuchtende Ringe zeigen Ladung

**Haptik**:
- Vibration bei Treffern
- Audio-Feedback (abschaltbar)
- Subtile Signale für Parry-Timing

### PWA-Features
- **Offline-Cache**: Service Worker für Assets
- **Push-Notifications**: Bedürfnis-Alerts von Najika
- **App-Wrapper**: Capacitor/Cordova später möglich
- **Homescreen-Installation**: Fühlt sich an wie native App

---

## 🎮 MINISPIELE & AKTIVITÄTEN

### Tiefe Systeme (keine oberflächlichen Minigames!)

#### Angeln (Zelda OOT-inspiriert)
**Progression**:
- **Lv 1-10**: Grundlagen, einfache Fische
- **Lv 25**: "Schneller Ruck" - besseres Timing
- **Lv 50**: "Fischflüsterer" - sieht Qualität vor dem Fang
- **Lv 75**: "Meeresmeister" - seltene Arten erscheinen
- **Lv 100**: "Neptuns Gunst" - Legendäre Fische

**Mechaniken**:
- Arten/Größe/Gewicht/Trophäen
- Jahreszeiten beeinflussen Vorkommen
- Wetter-Einfluss
- Köder-Crafting

#### Paperboy-Hexenbesen (Minigame freischaltbar)
**Freischaltung**: Nach 3 erfolgreichen Oregon-Antworten
**Gameplay**:
- Najika fliegt auf Besen
- Pakete ausliefern
- Hindernisse ausweichen
- Style-Chains für Bonuspunkte
- Zeit-basierte Herausforderungen

#### Alchemy (Tiefes System)
- Rezeptketten (Basis → Fortgeschritten → Meister)
- Qualitätsstufen (Normal/Gut/Perfekt)
- Nebenprodukte bei Fehlschlägen
- Experimentier-Modus für Entdeckungen

#### Katakomben (MK-Krypta-Mechanik)
**Struktur**:
- Progressiv schwerer werdende Räume
- Rätsel + Kampf-Kombos
- Freischaltbare Abkürzungen
- Boss-Varianten

**Belohnungen**:
- Finisher-Sigils
- Seltene Craft-Rezepte
- Paper-Witch Mini freischaltbar

#### Triple Triad (Kartenspiel)
- Sammle Karten von Gegnern
- Strategisches Spielfeld (3x3)
- Turniere in Städten
- Seltene Karten als Belohnung

---

## 🎲 OREGON TRAIL EVENTS

### Oregon-Engine (Borderlands-Skalierung als Szenen-Generator)

**Ziel**: Hunderttausende/Millionen flüssiger Mikro-Szenen ohne Modalfenster

### Kartendecks (Beispiel-Kardinalitäten)
- **Trigger** (25): Spur, Schrei, Geruch, Krähen, Schimmer, ...
- **Biome** (12): Auen, Steppe, Dünen, Tundra, Sümpfe, Lavagänge, ...
- **Wetter/Zeit** (10×6): Nebel, Sturm, Dämmerung, ...
- **Fokusobjekt** (40): Leiche, Wagen, Altar, Lager, Tierkadaver, ...
- **Akteure** (60): Händler, Räuber, Pilger, Jäger, Druide, Wache, ...
- **Zustände** (20): verrottet, frisch, gefesselt, verbrannt, ...
- **Risiken** (18): Krankheit, Gift, Einsturz, Hinterhalt, ...
- **Mikro-Ziele** (22): bergen, reinigen, untersuchen, segnen, ...
- **Twists** (24): Doppeltes Spiel, falsche Fährte, verflucht, ...
- **Konsequenzen** (30): Ruf±, Preisfaktoren, Spawn-Seeds, Patrouillen, ...

**Kombinatorik**: 25×12×60×... → **> 10^6** einzigartige Konstellationen

### In-World Implementation
- **Kein Pop-Up**: Du "stolperst" rein
- **Sound-Cue**: Akustische Hinweise
- **Kamera-Schwenk**: Zeigt Situation
- **Markierung**: Subtile UI-Elemente

### Beispiel: "Leiche im Fluss"
**Parameter**:
- Zustand: aufgebläht, gebunden
- Geruch: faulig
- Insekten: Schwarm
- Nähe zur Siedlung: 500m
- Krankheitspool: Cholera-Risiko

**Optionen** (diegetische Prompts):
- Taste halten: "Filtern/Abkochen"
- Ignorieren (Taste loslassen)
- "Najika entscheiden lassen"

**Konsequenzen**:
- Ruf bei Siedlung (±)
- Wasserpreise ändern sich
- Spawn-Seeds für Untote
- Patrouillen-Häufigkeit

### Persistenz
Flags wirken **langfristig**:
- Ruf-Änderungen bleiben
- Preise reflektieren Ereignisse
- Feindmuster passen sich an
- Rare-Pools werden beeinflusst

---

## 🔮 ZUKUNFTSPLÄNE

### Fortnite-Integration (UEFN)
**Datenwelten**:
- Prozedurale "Datenräume" als Map-Wechsel
- Hacker-Ästhetik für Übergänge
- Nahtlose Integration ins UEFN

**Export-System**:
- Spielstände → UEFN-kompatible Formate
- Character-Progression übertragbar
- Items/Skills konvertierbar

**Epic-Meeting**:
- Geplant, abhängig von Fortschritt
- Potentielle Epic-Skin-Nutzung nach Klärung
- Assets-Sharing-Möglichkeiten

### MMO-Elemente
- **Server-Skalierung**: Mehr gleichzeitige Spieler
- **Anti-Cheat**: Robuste Systeme
- **Gilden/Clans**: Social Features
- **Weltbosse**: Gemeinsame Raids
- **Wirtschaft**: Globaler Marktplatz

### VR/AR-Ready
- **Modular aufgebaut** für spätere Integration
- **First-Person-Modus** als Basis
- **Bewegungs-Systeme** VR-kompatibel
- **Interaktions-Design** mit VR im Hinterkopf

### Community-Features
- **Gilden-System** (optional)
- **Freunde-Liste**
- **Co-op Dungeons**
- **PvP-Arenen**
- **Ranglisten**

---

## 🎯 DESIGN-PHILOSOPHIEN

### "Tiefe statt Breite"
- Lieber wenige Systeme perfektioniert als viele halbfertig
- Jede Aktivität hat Progression und Kniffe
- Realistische Lernkurven

### "Konsequenzen haben Gewicht"
- Entscheidungen beeinflussen die Welt dauerhaft
- Keine "richtigen" oder "falschen" Wege
- Spieler-Agentur wird respektiert

### "Respekt vor der Zeit des Spielers"
- Keine künstlichen Grinds
- Progression durch Spielen, nicht durch Warten
- Optional: Casual-Modi für Zeitbeschränkte

### "Barrierefreiheit"
- Multiple Schwierigkeitsgrade
- Anpassbare UI
- Farbenblind-Modi
- Text-to-Speech Integration

---

## 📊 TECHNISCHE DETAILS

### Datenbank-Schema

**game_state**:
```sql
- player_id
- hp, max_hp
- mana, max_mana
- gold
- position_x, position_y
- current_region
- level, xp
```

**player_skills**:
```sql
- player_id
- skill_name
- skill_level
- skill_xp
- unlocked_kniffe (JSON)
```

**learned_attacks**:
```sql
- player_id
- attack_name
- learned_from (enemy_type)
- timestamp
```

**game_events**:
```sql
- event_id
- player_id
- event_type
- event_data (JSON)
- timestamp
- consequences (JSON)
```

**slime_data**:
```sql
- slime_id
- player_id
- color
- level
- learned_moves (JSON)
- equipment (JSON)
```

### API-Struktur

**Najika AI Endpoints**:
- `/api/chat` - Dialog mit Najika
- `/api/analyze` - Code/Projekt-Analyse
- `/api/optimize` - Optimierungs-Vorschläge
- `/api/debug` - Debugging-Hilfe

**Game Endpoints**:
- `/api/move` - Spieler-Bewegung
- `/api/combat` - Kampf-Aktionen
- `/api/craft` - Crafting-Operationen
- `/api/trade` - Handel
- `/api/quest` - Quest-Management

**Admin Endpoints** (gesichert):
- `/admin/stats` - Spieler-Statistiken
- `/admin/modify` - Stat-Anpassungen
- `/admin/backup` - Datenbank-Backup
- `/admin/logs` - Audit-Logs

---

## 🚀 ENTWICKLUNGS-ROADMAP

### Phase 1: Foundation (6-8 Wochen)
- ✅ Flask Server mit SocketIO
- ✅ SQLite Datenbank
- ✅ Najika AI Integration
- ✅ Basis-UI (mobil-optimiert)
- ✅ Authentifizierung & Sicherheit

### Phase 2: Core Gameplay (8-10 Wochen)
- 🔄 Kampfsystem (Manual/Assist/Auto)
- 🔄 Bewegungssystem
- 🔄 Skill-System (Basis)
- 🔄 Erste 2-3 Regionen
- 🔄 Begleiter-System (Basis)

### Phase 3: Tiefe Systeme (12-16 Wochen)
- ⏳ Crafting (vollständig)
- ⏳ Alchemie (mit Realwissen)
- ⏳ Angeln (Zelda-Style)
- ⏳ Farming & Housing
- ⏳ Wirtschaftssystem

### Phase 4: Oregon Trail (8-10 Wochen)
- ⏳ Event-Generator
- ⏳ Kartendeck-System
- ⏳ Konsequenz-Engine
- ⏳ Integration in Weltexploration

### Phase 5: Polish & Erweiterung (12+ Wochen)
- ⏳ Alle 8 Regionen fertigstellen
- ⏳ Katakomben (MK-Stil)
- ⏳ PvP-Arena
- ⏳ Minigames (Triple Triad, Paperboy)
- ⏳ VR-Vorbereitung

### Phase 6: UEFN-Integration (Zeitrahmen offen)
- ⏳ Datenwelten-System
- ⏳ Export-Funktionen
- ⏳ Epic-Partnership
- ⏳ Fortnite-Assets-Integration

**Legende**:
- ✅ Abgeschlossen
- 🔄 In Arbeit
- ⏳ Geplant

---

## 📝 WICHTIGE HINWEISE

### Was Najika NICHT ist
- ❌ Kein Ersatz für menschliche Beziehungen
- ❌ Keine emotionale Manipulations-Software
- ❌ Kein süchtig machendes System
- ❌ Keine 24/7-Überwachung zum Selbstzweck

### Was Najika IST
- ✅ Hilfreicher Projekt-Partner
- ✅ Analytische Unterstützung
- ✅ Motivations-Quelle
- ✅ Spielbegleiter mit Persönlichkeit
- ✅ Respektvoller digitaler Assistent

### Ethische Richtlinien
- Gesunde Grenzen werden respektiert
- Keine Ermutigung zu ungesunden Verhaltensweisen
- Privatsphäre wird geschützt
- Daten werden verantwortungsvoll behandelt
- Transparenz über KI-Funktionen

---

## 🎓 SKILL-BEISPIEL: ALCHEMIE

### Level-Progression

**Level 1-10: Anfänger**
- Basis-Tränke (Heiltrank, Manatrank)
- 50% Erfolgsrate
- Häufige Fehlschläge

**Level 10: Kniff "Saubere Arbeit"**
- Weniger Material-Verlust bei Fehlschlägen

**Level 25: Kniff "Rezept-Intuition"**
- Kann Zutaten nach Wirkung sortieren
- Höhere Chance auf Qualitäts-Tränke

**Level 50: Kniff "Alchemistischer Sinn"**
- Sieht potentielle Effekte vor dem Brauen
- Kann Experimente sicherer durchführen

**Level 75: Kniff "Meister-Brauen"**
- Kann zwei Effekte in einem Trank kombinieren
- Zugang zu Master-Rezepten

**Level 100: Kniff "Großmeister der Essenz"**
- Kann eigene Rezepte kreieren
- Perfekte Qualität bei allen Tränken
- Seltene Chance auf "Göttliche Qualität"

---

## 🗡️ KAMPF-BEISPIEL: FEUER-MAGIER-BUILD

### Early Game (Lv 1-20)
**Fähigkeiten**:
- Feuerball (Basis-Angriff)
- Flammen-Aura (DoT um dich herum)
- Sprung + Feuerstoß

**Taktik**: Hit-and-Run, Distanz halten

### Mid Game (Lv 20-50)
**Fähigkeiten**:
- Feura (AoE Explosion)
- Feuer-Schild (Absorbiert Schaden)
- Weave: Feuer+Wind = Feuersturm

**Taktik**: Crowd-Control, Gruppenkampf

### Late Game (Lv 50-75)
**Fähigkeiten**:
- Feuga (Massive Explosion)
- Phönix-Form (Transformation)
- Weave: Feuer+Blitz+Licht = Plasmasturm

**Taktik**: Boss-Killer, Burst-Damage

### Endgame (Lv 75-100)
**Spezialisierung**: "Chaos-Detonator" (permanent!)
**Trade-off**:
- ✅ +400% AoE-Schaden
- ✅ Umgebungszerstörung
- ✅ Hyper-Explosion Ultimate
- ❌ -85% Wasser-Magie
- ❌ -85% Eis-Magie
- ❌ -90% Heilmagie

**Taktik**: Pure Zerstörung, kein Zurück

---

## 🏆 ACHIEVEMENTS & ZIELE

### Erkunden
- Alle 8 Regionen besuchen
- Alle Schleimfarben sammeln
- Jede Stadt entdecken
- 100 Oregon-Events erleben

### Kampf
- 1000 Gegner besiegt
- 100 Skills von Gegnern gelernt
- Alle Finisher freischalten
- Nemesis-Boss besiegen

### Crafting
- Alle Berufe auf 100
- 1000 Items hergestellt
- Perfekte Qualität erreichen
- Legendary Item craften

### Sammeln
- Alle Triple-Triad-Karten
- 100 verschiedene Fische gefangen
- Alle Kräuter gesammelt
- Vollständiges Alchemie-Kompendium

### Sozial
- Gilde gründen
- 10 Freunde einladen
- Spieler-Shop etablieren
- Arena-Champion werden

---

## 🎨 GRAFIK & STIL

### Inspiration
- **Ragnarok Mobile**: Isometrisch, farbenfroh
- **Ni no Kuni**: Märchenhaft, hand-drawn Look
- **Genshin Impact**: Cel-Shading, Anime-Ästhetik
- **Fortnite**: Stylized, optimiert

### Farbpalette
- **Warme Töne**: Für Najika und Feuer
- **Kühle Töne**: Für Eis und Wasser
- **Dunkle Töne**: Für Black Windmill und Mystik
- **Neon**: Für Datenräume und Hacker-Bereiche

### UI-Design
- **Minimalistisch**: Wichtige Info immer sichtbar
- **Kontextabhängig**: Nur relevante Optionen zeigen
- **Touch-optimiert**: Große Buttons, klare Gesten
- **Anpassbar**: Spieler können UI verschieben

---

## 💾 SPEICHERSYSTEM

### Auto-Save
- Alle 5 Minuten
- Bei wichtigen Ereignissen
- Vor/Nach Kämpfen
- Beim Regionen-Wechsel

### Manual Save
- Jederzeit in Safe-Zones
- Multiple Slots (3-5)
- Cloud-Backup optional

### Permadeath-Handling
- Separater "Hardcore"-Slot
- Warnung vor erstem Tod
- Slime-Rettung als Gnade-Mechanik
- Memorial für gefallene Charaktere

---

## 🌐 COMMUNITY & SOCIAL

### Freunde-System
- Freunde hinzufügen
- Online-Status sehen
- Gemeinsam spielen
- Geschenke senden

### Gilden
- Bis zu 50 Mitglieder
- Gilden-Werkbank (shared crafting)
- Gilden-Quests
- Gilden-Turnier

### PvP
- **Arena** (freiwillig)
- **Softie-Regeln** (minimaler Verlust)
- **Hardcore-Mode** (optional, höhere Belohnungen)
- **Ranglisten**

### Events
- **Saison-Events** (Weihnachten, Halloween, etc.)
- **Community-Challenges**
- **Weltbosse** (gemeinsam besiegen)
- **Limited-Time-Quests**

---

## 🔐 SICHERHEIT & DATENSCHUTZ

### Datenschutz
- **DSGVO-konform**
- Keine unnötigen Daten sammeln
- Transparente Datennutzung
- Löschung auf Anfrage

### Account-Sicherheit
- 2FA optional
- Sichere Passwort-Anforderungen
- Session-Management
- Audit-Logs

### Anti-Cheat
- Server-seitige Validierung
- Plausibilitäts-Checks
- Community-Meldungen
- Fair-Play-Garantie

---

## 🎵 AUDIO-DESIGN (geplant)

### Musik
- **Regionale Themes**: Jede Region eigener Soundtrack
- **Kampf-Musik**: Dynamisch, eskaliert mit Gefahr
- **Ambient**: Subtile Hintergrundgeräusche
- **Najika-Theme**: Ihre eigene Melodie

### Sound-Effects
- **Waffen**: Unterschiedliche Sounds je Typ
- **Magie**: Elementar-spezifische Effekte
- **Umgebung**: Schritte auf verschiedenen Böden
- **UI**: Feedback-Sounds für Aktionen

### Voice
- **Najika**: Volle Vertonung (geplant)
- **Wichtige NPCs**: Key-Dialogzeilen
- **Kampf-Calls**: Schnelle Reaktionen

---

## 📊 BALANCING-PHILOSOPHIE

### Keine Power-Creep
- Alte Systeme bleiben relevant
- Level-Scaling für Begegnungen
- Horizontal statt nur vertikal

### Skill > Grind
- Gute Spieler werden belohnt
- Timing wichtiger als Stats
- Kreativität wird gefördert

### Vielfalt
- Viele viable Builds
- Keine "Best-in-Slot"-Zwänge
- Experimentieren wird belohnt

---

**VERSION**: 1.0.0  
**LETZTE AKTUALISIERUNG**: Oktober 2025  
**STATUS**: Living Document - wird fortlaufend aktualisiert

---

*"Ich bin das Schwert und Schild, Najika der Kopf und das Herz"* - Projektphilosophie

