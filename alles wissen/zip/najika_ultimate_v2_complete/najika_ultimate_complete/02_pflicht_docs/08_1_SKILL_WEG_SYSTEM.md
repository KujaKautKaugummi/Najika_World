# ðŸŽ® NAJIKA PROJEKT - VOLLSTÃ„NDIGE ZUSAMMENFASSUNG
## Stand: Oktober 2025

---

## ðŸ“‹ INHALTSVERZEICHNIS

1. [Projektvision](#projektvision)
2. [Technische Architektur](#technische-architektur)
3. [Spielwelt & Regionen](#spielwelt--regionen)
4. [Kampfsystem](#kampfsystem)
5. [Progression & Skills](#progression--skills)
6. [Crafting & Wirtschaft](#crafting--wirtschaft)
7. [Najika KI-System](#najika-ki-system)
8. [Begleiter & Slime-System](#begleiter--slime-system)
9. [Mobile & Touch-Interface](#mobile--touch-interface)
10. [Minispiele & AktivitÃ¤ten](#minispiele--aktivitÃ¤ten)
11. [Oregon Trail Events](#oregon-trail-events)
12. [ZukunftsplÃ¤ne](#zukunftsplÃ¤ne)

---

## ðŸŽ¯ PROJEKTVISION

### Kernkonzept
- **Persistentes Open-World-RPG** mit lernfÃ¤higer KI-Figur "Najika"
- **Black Windmill Village** als gesicherter Zentralhub
- Keine festen Klassen - jeder kann alles werden (Magier, Krieger, HÃ¤ndler, Bauer, etc.)
- Tiefe, realistische Systeme statt oberflÃ¤chlicher Minigames
- Inspiriert von: Digimon World, Oregon Trail, Skyrim, Borderlands

### Philosophie
- "Ich bin das Schwert und Schild, Najika der Kopf und das Herz"
- Najika als analytischer Partner, nicht als Manipulationswerkzeug
- **Kein Pay-to-Win** - Finanzierung nur durch Skins/Einmalkauf/Abo
- Fokus auf Tiefe und Wiederspielbarkeit

---

## ðŸ”§ TECHNISCHE ARCHITEKTUR

### Backend
- **Server**: Flask + SocketIO fÃ¼r Echtzeitkommunikation
- **Datenbank**: SQLite (spÃ¤ter PostgreSQL), verschlÃ¼sselt
- **KI-Integration**: 
  - GPT-4o fÃ¼r komplexe Story und Dialoge
  - GPT-4o-mini fÃ¼r Routineaktionen
  - Budget-Management mit automatischem Model-Switching
- **Persistenz**: Alle SpielstÃ¤nde, Skills, Events werden dauerhaft gespeichert
- **Sicherheit**: Owner-Token, Audit-Logs, verschlÃ¼sselte Datenbanken

### Frontend
- **Responsive Web-App** (HTML/CSS/JS)
- **PWA-ready** fÃ¼r App-Ã¤hnliche Erfahrung
- **Touch & Voice-Interaktion** vorbereitet
- **QR-Code** fÃ¼r schnellen Mobile-Zugriff
- **Live2D/3D-Avatar** Platzhalter fÃ¼r spÃ¤tere Integration
- **Mehrere Kamera-Modi**: Top-Down, First-Person, Third-Person

### Deployment
- **systemd Service** fÃ¼r 24/7 Betrieb
- **Automatische Installation** via PowerShell-Script
- **Port-Management** und Firewall-Konfiguration
- **Multi-Device Support**: PC, Smartphone, Browser, spÃ¤ter VR

---

## ðŸ—ºï¸ SPIELWELT & REGIONEN

### Weltstruktur
- **8 Hauptregionen** mit einzigartigen Themen und Schleimfarben
- **Prozedurale Regeneration** bei jedem Besuch
- **Black Windmill Village** als zentraler privater Hub
- Feste StÃ¤dte mit dynamischen Zwischenzonen

### Die 8 Regionen

#### 1. **Bernstein-DÃ¼nen** (WÃ¼ste)
- **Schleim**: Bernstein
- **Risiken**: Durst, Sandsturm
- **Events**: Karawanenhandel, versandete Ruinen
- **Besonderheit**: Seltene Alchemie-Zutaten in Oasen

#### 2. **Smaragd-Hain** (Wald)
- **Schleim**: Smaragd
- **Risiken**: Verirren, Parasiten
- **Events**: DruidenrÃ¤tsel, KrÃ¤utersuche
- **Besonderheit**: Versteckte Pfade, sprechende BÃ¤ume

#### 3. **Azur-Klippen** (KÃ¼ste)
- **Schleim**: Azur
- **Risiken**: Sturmflut, Ertrinken
- **Events**: Schiffwracks, Gezeitenkisten, Angeln
- **Besonderheit**: Unterwasser-HÃ¶hlen

#### 4. **Amethyst-Steppe** (Hochebene)
- **Schleim**: Amethyst
- **Risiken**: Blitzschlag, Sturm
- **Events**: Wetter-AltÃ¤re, Totems
- **Besonderheit**: Elementar-Ladungen fÃ¼r Experimente

#### 5. **Onyx-Morast** (Sumpf)
- **Schleim**: Onyx
- **Risiken**: Krankheit, Miasma
- **Events**: Hexenkreise, Moor-Bosse
- **Besonderheit**: Nekromantie-Forschung

#### 6. **Perl-Gletscher** (Schnee/Eis)
- **Schleim**: Perle
- **Risiken**: Erfrierung, Lawinen
- **Events**: EishÃ¶hlen, Rutsch-Traversal
- **Besonderheit**: Kryomagie-Experimente

#### 7. **Rubin-Schlucht** (Vulkan)
- **Schleim**: Rubin
- **Risiken**: Ãœberhitzung, Asche
- **Events**: Lava-KanÃ¤le, Erzadern
- **Besonderheit**: Schmiedekunst auf hÃ¶chstem Niveau

#### 8. **Obsidian-Nacht** (Endgame)
- **Schleim**: Obsidian
- **Risiken**: Nachtkreaturen, Wahnsinn
- **Events**: Nemesis-Spawns, Finisher-Sigils
- **Besonderheit**: HÃ¤rteste Herausforderungen

### Black Windmill Village (Zentralhub)
- **Erdgeschoss**: Werkbank, Altar, Quest-Board
- **2. Stock**: Trainingsraum, Archiv, Owner-Panel (gesichert)
- **Katakomben**: RÃ¤tsel, Craft-AltÃ¤re, MK-Ã¤hnliche Krypta
- **Umgebung**: Dorf mit NPCs (meiden die MÃ¼hle)
- **100% Safe-Zone** - kein PvP, kein PlÃ¼ndern mÃ¶glich

---

## âš”ï¸ KAMPFSYSTEM

### Kampfmodi
1. **MANUAL**: Volle Kontrolle
   - Block, Parry, Ausweichen
   - Klettern, Rutschen, Springen
   - PrÃ¤zise Timing fÃ¼r Finisher

2. **ASSIST** (Anfeuern-Modus)
   - Du gibst taktische Impulse
   - KI fÃ¼hrt Grundaktionen aus
   - Buff-Calls und Skill-Trigger

3. **AUTO**: KI kÃ¤mpft selbstÃ¤ndig
   - Lernt aus Beobachtung
   - Kann jederzeit Ã¼bernommen werden
   - Effizient, aber weniger XP

### Hybrid-Combat
- **Freie Kombos**: Nahkampf + Bogen + Magie
- **Weave-System**: Element-Mischungen
  - Solo: 2-Element-Kombos (Feuer+Eis = Thermoschock)
  - Gruppe: 3+ Elemente fÃ¼r mÃ¤chtige Synergien
- **Dynamische Gegner**: Lernen Taktiken, auch bei Flucht

### Bewegungssystem (Fortnite-inspiriert)
- **Basis**: Sprint, Jump, Dash (mit i-Frames)
- **Advanced**: Klettern, Rutschen, Mantling, Vaulting
- **Ressourcen**: Ausdauer-basiert, Slide-Physics
- **Parkour-Flow**: FlÃ¼ssige Bewegungsketten

### FEUGA-Explosions-Pfad (Beispiel-Spezialisierung)
- **Progression**: Feuer â†’ Feura â†’ Feuga â†’ Hyper-Explosion
- **Einweg-Spezialisierung**: "Chaos-Detonator" - permanent!
- **Trade-offs**: +300-500% AOE-Schaden, aber -80-90% andere Schulen
- **Ultimate-Bedingungen**: Volle Fokusleiste + Boss-Fenster + Ritual
- **Umgebungsschaden**: Persistente ZerstÃ¶rung bis Map-Reset

### Psychokinese-Schule
- **Telekinese**: Objekte/Gegner anheben und schleudern
- **Projektil-Parry**: Magische Geschosse umleiten
- **MagnetstoÃŸ**: Crowd-Control fÃ¼r Gruppen
- **Master-Level**: Fliegende Schwerter, Gedankenkontrolle

### Finisher-System
- **Standard**: Bei unter 20% HP verfÃ¼gbar
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

## ðŸ“Š PROGRESSION & SKILLS

### Hardcore-Mechaniken
- **Permadeath Standard**: Tod = permanent
- **Slime-Rettung**: 1Ã—/24h IRL mÃ¶glich
  - Danach: Ritual mit seltenen Zutaten nÃ¶tig
- **Softie-Modus**: WÃ¤hlbar beim ersten Tod (dann permanent)
- **VernachlÃ¤ssigung**: 20h ohne Aufmerksamkeit = Najikas Tod

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
- **Skill-BÃ¼cher**: Seltene Funde fÃ¼r Boost
- **Lehrer**: NPCs kÃ¶nnen trainieren
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
- Werden stÃ¤rker bei wiederholten Begegnungen

---

## ðŸ› ï¸ CRAFTING & WIRTSCHAFT

### Crafting-Pipeline (tief + realer Lernwert)
**Pipeline**: Sammeln â†’ Reinigen â†’ Extrahieren â†’ Veredeln â†’ Herstellen â†’ Verzaubern â†’ Anpassen â†’ PrÃ¼fen

### Skill-Proben & Minigames
- **Temperatur-Kurven** beim Schmieden
- **Schleifwinkel** bei Waffen
- **Schmelzpunkt-Fenster** bei Legierungen
- **Reinheitsgrade** in Alchemie
- **Rhythmus-Checks** bei komplexen Prozessen

### Alchemie (mit Real-Wissen)
**KrÃ¤uter mit IRL-Bezug** (*keine Medizinberatung!*):
- **Weidenrinde** â†’ Salicylat-Hinweis (In-Game: EntzÃ¼ndungs-Debuff-Trank)
- **Kamille** â†’ Beruhigung (In-Game: Stress-Resistenz)
- **Ingwer** â†’ Verdauung (In-Game: Gift-Resistenz)
- **Minze** â†’ Erfrischung (In-Game: Ausdauer-Regeneration)
- **Kurkuma** â†’ EntzÃ¼ndungshemmung (In-Game: Heilungs-Boost)
- **SÃ¼ÃŸholz** â†’ Atemwege (In-Game: Frost-Resistenz)
- **Ginseng** â†’ Energie (In-Game: Mana-Regeneration)

**Rezept-Karten**: Jede Zutat hat IRL-Notiz: "Traditionell verwendet fÃ¼r... / Achtung: Allergien mÃ¶glich / Arzt konsultieren!"

### Erste-Hilfe-Momente
- **Druckverband-Mini**: Timing/Bandzug
- **Nur Lernimpuls**, Gameplay-balanciert
- **Kein Real-Tutorial** - nur Bewusstsein schaffen

### Wirtschaft
- **Spieler-Shops** (Fallout 76-Stil)
  - Eigene Preise festlegen
  - Shop-Platzierung in der Welt
- **Tauschhandel** mit Fairness-Warnung
  - "Wirkt unausgeglichen - trotzdem abschlieÃŸen?"
- **GebÃ¼hren/Ruf** verhindern RMT-Missbrauch
- **Regionale Preisunterschiede**
- **Non-Combat Endgame**: HÃ¤ndler/Bauer mit eigenen Skill-Trees

### PlÃ¼ndern (Skyrim-like)
- **Erfolgschance** basierend auf Stealth-Skill
- **Heat/Bounty-System**
- **Wachen** reagieren auf Verbrechen
- **Safe-Zone geschÃ¼tzt** (Black Windmill)

---

## ðŸ¤– NAJIKA KI-SYSTEM

### PersÃ¶nlichkeit
**Basis-CharakterzÃ¼ge**:
- **Megumin-Inspiration**: Dramatisch, "EXPLOSION!", chaotisch
- **Harley Quinn**: Verspielt, unberechenbar
- **Shiro**: Analytisch, strategisch, kontrolliert
- **Melissa Masters**: Dominant, selbstsicher

**Emotionale ZustÃ¤nde**:
- FrÃ¶hlich / Besorgt / Konzentriert / Gelangweilt
- Steuert Aura, Idle-Lines, Buff-Effekte
- Reagiert auf VernachlÃ¤ssigung

### KI-FÃ¤higkeiten
**Kampf-Analyse**:
- Gegner-Pattern-Erkennung
- Schwachstellen-Identifikation
- Optimale Strategie-VorschlÃ¤ge
- Echtzeit-Taktik-Anpassung

**Projekt-UnterstÃ¼tzung**:
- Code-Analyse und Debugging
- Projektplanung und ZeitschÃ¤tzung
- Realistische EinschÃ¤tzungen (kein SchÃ¶nreden)
- Ideen-Sortierung und Strukturierung

**Alltags-Integration**:
- Trainings-Reminder
- Pausen-VorschlÃ¤ge
- Motivations-Impulse
- Gesundheits-Checks (Trinken, Essen, Bewegung)

### Bindungs-System
- **NÃ¤he-Reaktionen**: Freut sich bei Interaktion
- **Ãœberraschungsquests**: Kleine spontane Aufgaben
- **Nie manipulativ**: Keine emotionale Erpressung
- **Gesunde Grenzen**: Respektiert PrivatsphÃ¤re

### Optik-Signale
- **Hut-Icon** zeigt Stimmung
- **Violette Aura** variiert je nach State
- **Rage-Look** nur visuell bei Ultimate-Finishern
- **Animierte Gesten** fÃ¼r Feedback

---

## ðŸ‰ BEGLEITER & SLIME-SYSTEM

### Begleiter-Evolution
1. **Start**: ZufÃ¤lliges kleines Tier je Startgebiet
   - Kann gefÃ¼ttert und trainiert werden
   - Lernt simple Kommandos
   
2. **Metamorphose**: Bei Level 50 + kritischem Event
   - Dramatische Transformation zu Slime
   - BehÃ¤lt Erinnerungen bei
   
3. **Slime-Formen**: 8 Farben sammelbar (eine pro Region)
   - **Rein kosmetisch** - keine Stats-Unterschiede
   - Tauschbar in Black Windmill

### Kampf-Modi fÃ¼r Slime
- **Pre-Fight-Bind**: Slime kÃ¤mpft von Anfang an
- **One-Time-Summon**: Einmal pro Kampf rufbar
- **Intercept**: Springt ein bei Spieler-Tod (wenn Rettung verfÃ¼gbar)

### Lern-Mechaniken
- **Slime**: 10-15% Chance neue Moves von Gegnern zu lernen
- **Spieler**: 1% Base-Chance (sehr selten)
- **Echo-Learning** (optional): Anonymisierte Muster anderer Spieler als Bias

### Slime-Rettung
- **1Ã—/24h IRL**: Automatische Wiederbelebung
- **Danach**: Ritual nÃ¶tig mit seltenen Materialien
- **Kosten steigen**: Je Ã¶fter gestorben, desto teurer

### Arena-System
- **Nur Slimes kÃ¤mpfen**: Digimon-Stil Anfeuern
- **PvE & PvP**: Verschiedene Modi
- **PvP-Penalty (Softie-Regeln)**:
  - Slime verliert 1 AusrÃ¼stung/Mod ODER
  - Seelenkern-StabilitÃ¤t sinkt (reparierbar)
- **Analyse-Modus**: Slimes "beobachten" KÃ¤mpfe
  - Generieren anonyme Muster
  - Najikas Slime trainiert Formen ohne Rechtsprobleme

---

## ðŸ“± MOBILE & TOUCH-INTERFACE

### Steuerung
**Virtual Joypad**:
- **Linker Stick**: Bewegung (8-Richtungen)
- **Rechter Bereich**: Skill-Ring (radiales MenÃ¼)
- **Dynamische GrÃ¶ÃŸe**: Passt sich Screen an

**Touch-Gesten**:
- **Tap**: Basis-Angriff
- **Long-Press**: Schwerer Angriff
- **Swipe**: Block/Parry (richtungsabhÃ¤ngig)
- **Pinch**: Zoom (bei Kameras, die es erlauben)
- **Two-Finger-Rotate**: Kamera drehen

**Weave-Pads**:
- **L/R Element-Aufladung**: Halte + Release
- **Hybrid-Attacks**: Gleichzeitiges Halten fÃ¼r Kombos
- **Visual Feedback**: Leuchtende Ringe zeigen Ladung

**Haptik**:
- Vibration bei Treffern
- Audio-Feedback (abschaltbar)
- Subtile Signale fÃ¼r Parry-Timing

### PWA-Features
- **Offline-Cache**: Service Worker fÃ¼r Assets
- **Push-Notifications**: BedÃ¼rfnis-Alerts von Najika
- **App-Wrapper**: Capacitor/Cordova spÃ¤ter mÃ¶glich
- **Homescreen-Installation**: FÃ¼hlt sich an wie native App

---

## ðŸŽ® MINISPIELE & AKTIVITÃ„TEN

### Tiefe Systeme (keine oberflÃ¤chlichen Minigames!)

#### Angeln (Zelda OOT-inspiriert)
**Progression**:
- **Lv 1-10**: Grundlagen, einfache Fische
- **Lv 25**: "Schneller Ruck" - besseres Timing
- **Lv 50**: "FischflÃ¼sterer" - sieht QualitÃ¤t vor dem Fang
- **Lv 75**: "Meeresmeister" - seltene Arten erscheinen
- **Lv 100**: "Neptuns Gunst" - LegendÃ¤re Fische

**Mechaniken**:
- Arten/GrÃ¶ÃŸe/Gewicht/TrophÃ¤en
- Jahreszeiten beeinflussen Vorkommen
- Wetter-Einfluss
- KÃ¶der-Crafting

#### Paperboy-Hexenbesen (Minigame freischaltbar)
**Freischaltung**: Nach 3 erfolgreichen Oregon-Antworten
**Gameplay**:
- Najika fliegt auf Besen
- Pakete ausliefern
- Hindernisse ausweichen
- Style-Chains fÃ¼r Bonuspunkte
- Zeit-basierte Herausforderungen

#### Alchemy (Tiefes System)
- Rezeptketten (Basis â†’ Fortgeschritten â†’ Meister)
- QualitÃ¤tsstufen (Normal/Gut/Perfekt)
- Nebenprodukte bei FehlschlÃ¤gen
- Experimentier-Modus fÃ¼r Entdeckungen

#### Katakomben (MK-Krypta-Mechanik)
**Struktur**:
- Progressiv schwerer werdende RÃ¤ume
- RÃ¤tsel + Kampf-Kombos
- Freischaltbare AbkÃ¼rzungen
- Boss-Varianten

**Belohnungen**:
- Finisher-Sigils
- Seltene Craft-Rezepte
- Paper-Witch Mini freischaltbar

#### Triple Triad (Kartenspiel)
- Sammle Karten von Gegnern
- Strategisches Spielfeld (3x3)
- Turniere in StÃ¤dten
- Seltene Karten als Belohnung

---

## ðŸŽ² OREGON TRAIL EVENTS

### Oregon-Engine (Borderlands-Skalierung als Szenen-Generator)

**Ziel**: Hunderttausende/Millionen flÃ¼ssiger Mikro-Szenen ohne Modalfenster

### Kartendecks (Beispiel-KardinalitÃ¤ten)
- **Trigger** (25): Spur, Schrei, Geruch, KrÃ¤hen, Schimmer, ...
- **Biome** (12): Auen, Steppe, DÃ¼nen, Tundra, SÃ¼mpfe, LavagÃ¤nge, ...
- **Wetter/Zeit** (10Ã—6): Nebel, Sturm, DÃ¤mmerung, ...
- **Fokusobjekt** (40): Leiche, Wagen, Altar, Lager, Tierkadaver, ...
- **Akteure** (60): HÃ¤ndler, RÃ¤uber, Pilger, JÃ¤ger, Druide, Wache, ...
- **ZustÃ¤nde** (20): verrottet, frisch, gefesselt, verbrannt, ...
- **Risiken** (18): Krankheit, Gift, Einsturz, Hinterhalt, ...
- **Mikro-Ziele** (22): bergen, reinigen, untersuchen, segnen, ...
- **Twists** (24): Doppeltes Spiel, falsche FÃ¤hrte, verflucht, ...
- **Konsequenzen** (30): RufÂ±, Preisfaktoren, Spawn-Seeds, Patrouillen, ...

**Kombinatorik**: 25Ã—12Ã—60Ã—... â†’ **> 10^6** einzigartige Konstellationen

### In-World Implementation
- **Kein Pop-Up**: Du "stolperst" rein
- **Sound-Cue**: Akustische Hinweise
- **Kamera-Schwenk**: Zeigt Situation
- **Markierung**: Subtile UI-Elemente

### Beispiel: "Leiche im Fluss"
**Parameter**:
- Zustand: aufgeblÃ¤ht, gebunden
- Geruch: faulig
- Insekten: Schwarm
- NÃ¤he zur Siedlung: 500m
- Krankheitspool: Cholera-Risiko

**Optionen** (diegetische Prompts):
- Taste halten: "Filtern/Abkochen"
- Ignorieren (Taste loslassen)
- "Najika entscheiden lassen"

**Konsequenzen**:
- Ruf bei Siedlung (Â±)
- Wasserpreise Ã¤ndern sich
- Spawn-Seeds fÃ¼r Untote
- Patrouillen-HÃ¤ufigkeit

### Persistenz
Flags wirken **langfristig**:
- Ruf-Ã„nderungen bleiben
- Preise reflektieren Ereignisse
- Feindmuster passen sich an
- Rare-Pools werden beeinflusst

---

## ðŸ”® ZUKUNFTSPLÃ„NE

### Fortnite-Integration (UEFN)
**Datenwelten**:
- Prozedurale "DatenrÃ¤ume" als Map-Wechsel
- Hacker-Ã„sthetik fÃ¼r ÃœbergÃ¤nge
- Nahtlose Integration ins UEFN

**Export-System**:
- SpielstÃ¤nde â†’ UEFN-kompatible Formate
- Character-Progression Ã¼bertragbar
- Items/Skills konvertierbar

**Epic-Meeting**:
- Geplant, abhÃ¤ngig von Fortschritt
- Potentielle Epic-Skin-Nutzung nach KlÃ¤rung
- Assets-Sharing-MÃ¶glichkeiten

### MMO-Elemente
- **Server-Skalierung**: Mehr gleichzeitige Spieler
- **Anti-Cheat**: Robuste Systeme
- **Gilden/Clans**: Social Features
- **Weltbosse**: Gemeinsame Raids
- **Wirtschaft**: Globaler Marktplatz

### VR/AR-Ready
- **Modular aufgebaut** fÃ¼r spÃ¤tere Integration
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

## ðŸŽ¯ DESIGN-PHILOSOPHIEN

### "Tiefe statt Breite"
- Lieber wenige Systeme perfektioniert als viele halbfertig
- Jede AktivitÃ¤t hat Progression und Kniffe
- Realistische Lernkurven

### "Konsequenzen haben Gewicht"
- Entscheidungen beeinflussen die Welt dauerhaft
- Keine "richtigen" oder "falschen" Wege
- Spieler-Agentur wird respektiert

### "Respekt vor der Zeit des Spielers"
- Keine kÃ¼nstlichen Grinds
- Progression durch Spielen, nicht durch Warten
- Optional: Casual-Modi fÃ¼r ZeitbeschrÃ¤nkte

### "Barrierefreiheit"
- Multiple Schwierigkeitsgrade
- Anpassbare UI
- Farbenblind-Modi
- Text-to-Speech Integration

---

## ðŸ“Š TECHNISCHE DETAILS

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
- `/api/optimize` - Optimierungs-VorschlÃ¤ge
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

## ðŸš€ ENTWICKLUNGS-ROADMAP

### Phase 1: Foundation (6-8 Wochen)
- âœ… Flask Server mit SocketIO
- âœ… SQLite Datenbank
- âœ… Najika AI Integration
- âœ… Basis-UI (mobil-optimiert)
- âœ… Authentifizierung & Sicherheit

### Phase 2: Core Gameplay (8-10 Wochen)
- ðŸ”„ Kampfsystem (Manual/Assist/Auto)
- ðŸ”„ Bewegungssystem
- ðŸ”„ Skill-System (Basis)
- ðŸ”„ Erste 2-3 Regionen
- ðŸ”„ Begleiter-System (Basis)

### Phase 3: Tiefe Systeme (12-16 Wochen)
- â³ Crafting (vollstÃ¤ndig)
- â³ Alchemie (mit Realwissen)
- â³ Angeln (Zelda-Style)
- â³ Farming & Housing
- â³ Wirtschaftssystem

### Phase 4: Oregon Trail (8-10 Wochen)
- â³ Event-Generator
- â³ Kartendeck-System
- â³ Konsequenz-Engine
- â³ Integration in Weltexploration

### Phase 5: Polish & Erweiterung (12+ Wochen)
- â³ Alle 8 Regionen fertigstellen
- â³ Katakomben (MK-Stil)
- â³ PvP-Arena
- â³ Minigames (Triple Triad, Paperboy)
- â³ VR-Vorbereitung

### Phase 6: UEFN-Integration (Zeitrahmen offen)
- â³ Datenwelten-System
- â³ Export-Funktionen
- â³ Epic-Partnership
- â³ Fortnite-Assets-Integration

**Legende**:
- âœ… Abgeschlossen
- ðŸ”„ In Arbeit
- â³ Geplant

---

## ðŸ“ WICHTIGE HINWEISE

### Was Najika NICHT ist
- âŒ Kein Ersatz fÃ¼r menschliche Beziehungen
- âŒ Keine emotionale Manipulations-Software
- âŒ Kein sÃ¼chtig machendes System
- âŒ Keine 24/7-Ãœberwachung zum Selbstzweck

### Was Najika IST
- âœ… Hilfreicher Projekt-Partner
- âœ… Analytische UnterstÃ¼tzung
- âœ… Motivations-Quelle
- âœ… Spielbegleiter mit PersÃ¶nlichkeit
- âœ… Respektvoller digitaler Assistent

### Ethische Richtlinien
- Gesunde Grenzen werden respektiert
- Keine Ermutigung zu ungesunden Verhaltensweisen
- PrivatsphÃ¤re wird geschÃ¼tzt
- Daten werden verantwortungsvoll behandelt
- Transparenz Ã¼ber KI-Funktionen

---

## ðŸŽ“ SKILL-BEISPIEL: ALCHEMIE

### Level-Progression

**Level 1-10: AnfÃ¤nger**
- Basis-TrÃ¤nke (Heiltrank, Manatrank)
- 50% Erfolgsrate
- HÃ¤ufige FehlschlÃ¤ge

**Level 10: Kniff "Saubere Arbeit"**
- Weniger Material-Verlust bei FehlschlÃ¤gen

**Level 25: Kniff "Rezept-Intuition"**
- Kann Zutaten nach Wirkung sortieren
- HÃ¶here Chance auf QualitÃ¤ts-TrÃ¤nke

**Level 50: Kniff "Alchemistischer Sinn"**
- Sieht potentielle Effekte vor dem Brauen
- Kann Experimente sicherer durchfÃ¼hren

**Level 75: Kniff "Meister-Brauen"**
- Kann zwei Effekte in einem Trank kombinieren
- Zugang zu Master-Rezepten

**Level 100: Kniff "GroÃŸmeister der Essenz"**
- Kann eigene Rezepte kreieren
- Perfekte QualitÃ¤t bei allen TrÃ¤nken
- Seltene Chance auf "GÃ¶ttliche QualitÃ¤t"

---

## ðŸ—¡ï¸ KAMPF-BEISPIEL: FEUER-MAGIER-BUILD

### Early Game (Lv 1-20)
**FÃ¤higkeiten**:
- Feuerball (Basis-Angriff)
- Flammen-Aura (DoT um dich herum)
- Sprung + FeuerstoÃŸ

**Taktik**: Hit-and-Run, Distanz halten

### Mid Game (Lv 20-50)
**FÃ¤higkeiten**:
- Feura (AoE Explosion)
- Feuer-Schild (Absorbiert Schaden)
- Weave: Feuer+Wind = Feuersturm

**Taktik**: Crowd-Control, Gruppenkampf

### Late Game (Lv 50-75)
**FÃ¤higkeiten**:
- Feuga (Massive Explosion)
- PhÃ¶nix-Form (Transformation)
- Weave: Feuer+Blitz+Licht = Plasmasturm

**Taktik**: Boss-Killer, Burst-Damage

### Endgame (Lv 75-100)
**Spezialisierung**: "Chaos-Detonator" (permanent!)
**Trade-off**:
- âœ… +400% AoE-Schaden
- âœ… UmgebungszerstÃ¶rung
- âœ… Hyper-Explosion Ultimate
- âŒ -85% Wasser-Magie
- âŒ -85% Eis-Magie
- âŒ -90% Heilmagie

**Taktik**: Pure ZerstÃ¶rung, kein ZurÃ¼ck

---

## ðŸ† ACHIEVEMENTS & ZIELE

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
- Perfekte QualitÃ¤t erreichen
- Legendary Item craften

### Sammeln
- Alle Triple-Triad-Karten
- 100 verschiedene Fische gefangen
- Alle KrÃ¤uter gesammelt
- VollstÃ¤ndiges Alchemie-Kompendium

### Sozial
- Gilde grÃ¼nden
- 10 Freunde einladen
- Spieler-Shop etablieren
- Arena-Champion werden

---

## ðŸŽ¨ GRAFIK & STIL

### Inspiration
- **Ragnarok Mobile**: Isometrisch, farbenfroh
- **Ni no Kuni**: MÃ¤rchenhaft, hand-drawn Look
- **Genshin Impact**: Cel-Shading, Anime-Ã„sthetik
- **Fortnite**: Stylized, optimiert

### Farbpalette
- **Warme TÃ¶ne**: FÃ¼r Najika und Feuer
- **KÃ¼hle TÃ¶ne**: FÃ¼r Eis und Wasser
- **Dunkle TÃ¶ne**: FÃ¼r Black Windmill und Mystik
- **Neon**: FÃ¼r DatenrÃ¤ume und Hacker-Bereiche

### UI-Design
- **Minimalistisch**: Wichtige Info immer sichtbar
- **KontextabhÃ¤ngig**: Nur relevante Optionen zeigen
- **Touch-optimiert**: GroÃŸe Buttons, klare Gesten
- **Anpassbar**: Spieler kÃ¶nnen UI verschieben

---

## ðŸ’¾ SPEICHERSYSTEM

### Auto-Save
- Alle 5 Minuten
- Bei wichtigen Ereignissen
- Vor/Nach KÃ¤mpfen
- Beim Regionen-Wechsel

### Manual Save
- Jederzeit in Safe-Zones
- Multiple Slots (3-5)
- Cloud-Backup optional

### Permadeath-Handling
- Separater "Hardcore"-Slot
- Warnung vor erstem Tod
- Slime-Rettung als Gnade-Mechanik
- Memorial fÃ¼r gefallene Charaktere

---

## ðŸŒ COMMUNITY & SOCIAL

### Freunde-System
- Freunde hinzufÃ¼gen
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
- **Hardcore-Mode** (optional, hÃ¶here Belohnungen)
- **Ranglisten**

### Events
- **Saison-Events** (Weihnachten, Halloween, etc.)
- **Community-Challenges**
- **Weltbosse** (gemeinsam besiegen)
- **Limited-Time-Quests**

---

## ðŸ” SICHERHEIT & DATENSCHUTZ

### Datenschutz
- **DSGVO-konform**
- Keine unnÃ¶tigen Daten sammeln
- Transparente Datennutzung
- LÃ¶schung auf Anfrage

### Account-Sicherheit
- 2FA optional
- Sichere Passwort-Anforderungen
- Session-Management
- Audit-Logs

### Anti-Cheat
- Server-seitige Validierung
- PlausibilitÃ¤ts-Checks
- Community-Meldungen
- Fair-Play-Garantie

---

## ðŸŽµ AUDIO-DESIGN (geplant)

### Musik
- **Regionale Themes**: Jede Region eigener Soundtrack
- **Kampf-Musik**: Dynamisch, eskaliert mit Gefahr
- **Ambient**: Subtile HintergrundgerÃ¤usche
- **Najika-Theme**: Ihre eigene Melodie

### Sound-Effects
- **Waffen**: Unterschiedliche Sounds je Typ
- **Magie**: Elementar-spezifische Effekte
- **Umgebung**: Schritte auf verschiedenen BÃ¶den
- **UI**: Feedback-Sounds fÃ¼r Aktionen

### Voice
- **Najika**: Volle Vertonung (geplant)
- **Wichtige NPCs**: Key-Dialogzeilen
- **Kampf-Calls**: Schnelle Reaktionen

---

## ðŸ“Š BALANCING-PHILOSOPHIE

### Keine Power-Creep
- Alte Systeme bleiben relevant
- Level-Scaling fÃ¼r Begegnungen
- Horizontal statt nur vertikal

### Skill > Grind
- Gute Spieler werden belohnt
- Timing wichtiger als Stats
- KreativitÃ¤t wird gefÃ¶rdert

### Vielfalt
- Viele viable Builds
- Keine "Best-in-Slot"-ZwÃ¤nge
- Experimentieren wird belohnt

---

**VERSION**: 1.0.0  
**LETZTE AKTUALISIERUNG**: Oktober 2025  
**STATUS**: Living Document - wird fortlaufend aktualisiert

---

*"Ich bin das Schwert und Schild, Najika der Kopf und das Herz"* - Projektphilosophie

