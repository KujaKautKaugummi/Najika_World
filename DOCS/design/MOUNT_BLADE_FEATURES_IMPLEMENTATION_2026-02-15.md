# MOUNT & BLADE 2 FEATURES FÜR NAJIKA WORLD

**Erstellt:** 2026-02-15
**Zweck:** Konkrete Umsetzung der M&B2-inspirierten Features

---

## ✅ FEATURE 1: COMPANION SKILL-LEARNING SYSTEM

### Konzept:
**Companions lernen Skills von Monstern (genau wie der Spieler!)**

### Implementation:

```yaml
companion_skill_learning:
  learning_sources:
    combat_observation:
      - "Companion sieht Monster-Skill im Kampf"
      - "Chance zu lernen: 5% pro beobachtetem Skill-Einsatz"
      - "Beispiel: Drache nutzt 'Feueratem' → Companion kann es lernen"

    player_teaching:
      - "Spieler kann eigene Skills an Companion lehren"
      - "Kostet: Skill-Buch + Training-Zeit (1 Tag In-Game)"
      - "Erfolgsrate: 80%"

    monster_capturing:
      - "Wenn Monster gefangen wird, kann Companion 1 Skill sofort lernen"
      - "Spieler wählt welchen Skill"

    quest_rewards:
      - "Bestimmte Quests belohnen mit Skill-Büchern"
      - "NPC-Meister können spezielle Skills lehren"

  skill_slots:
    base: 4  # Companion hat 4 Skill-Slots
    unlock_more: "Pro 10 Level +1 Slot (Max 8 Slots bei Level 50)"

  skill_synergies:
    - "Companion mit Feuer + Blitz = lernt Plasma-Skill"
    - "Companion mit Heilung + Schutz = lernt Heiliger Schild"

  examples:
    scenario_1:
      situation: "Spieler kämpft gegen Eis-Drachen mit Companion 'Yuki'"
      observation: "Yuki sieht Drache's 'Eissturm' Skill 10x"
      result: "5% * 10 = 50% Chance → Yuki lernt 'Eissturm I' (schwächere Version)"
      progression: "Yuki muss Skill 50x nutzen → wird zu 'Eissturm II' → 100x → 'Eissturm III'"
```

### UI-Design:
```
┌─────────────────────────────────────────────────┐
│ COMPANION: Yuki (Level 15)                       │
├─────────────────────────────────────────────────┤
│ SKILLS (4/5 Slots):                              │
│ [Eissturm II] [Heilung I] [Schwerthieb] [LEER] │
│                                                  │
│ BEOBACHTETE SKILLS (lernbar):                   │
│ ⚡ Feueratem (Drache) - 35% Lernchance           │
│ 🛡️ Schildstoß (Ritter) - 80% Lernchance         │
│                                                  │
│ [Skills lehren] [Skill-Buch nutzen]              │
└─────────────────────────────────────────────────┘
```

---

## ✅ FEATURE 2: ARENA-SYSTEM (2-TIER)

### Konzept:
**Offizielle Arena + Untergrund-Kämpfe**

### Implementation:

```yaml
arena_system:
  tier_1_official:
    name: "Argentum Arena"
    location: "Argentum Hauptstadt - Kolosseum"
    accessibility: "Öffentlich, Legal"

    rules:
      - "Keine tödlichen Waffen"
      - "Heiler überwachen Kämpfe"
      - "Aufgabe möglich"
      - "Zuschauer erlaubt"

    events:
      weekly_tournament:
        schedule: "Jeden Samstag 18:00 (In-Game Zeit)"
        participants: 16
        format: "Single-Elimination Bracket"
        rewards:
          champion: "5000 Münzen + Titel 'Arena-Champion' + Legendary Waffe"
          runner_up: "2000 Münzen + Epic Waffe"
          semi_finals: "500 Münzen"

      daily_duels:
        open_challenges: "Jederzeit gegen NPCs oder Spieler"
        rewards: "50-200 Münzen pro Sieg"
        ranking: "Elo-System (1000-3000 Rating)"

    betting:
      allowed: true
      min_bet: 10 Münzen
      max_bet: 1000 Münzen
      npc_bettors: "Zuschauer-NPCs wetten auch"

  tier_2_underground:
    name: "Untergrund-Kampfclubs"
    locations:
      - name: "Rattenkeller"
        city: "Argentum - Slums"
        description: "Schmutziger Keller, Fackeln, Blutflecken"

      - name: "Hinterhof der Taverne"
        city: "Schwarze Mühle"
        description: "Nachts nur, geheimes Codewort nötig"

      - name: "Verlassenes Lagerhaus"
        city: "Wüstenstadt Kal'Thara"
        description: "Illegale Gladiatoren-Kämpfe"

    rules:
      - "KEINE Regeln"
      - "Tödliche Waffen erlaubt"
      - "Tod möglich (Permadeath wenn aktiviert)"
      - "Illegale Wetten (höhere Quoten!)"
      - "Stadtgarde kann Razzia machen (10% Chance)"

    accessibility:
      requirement: "Quest-Chain 'Unterwelt' abschließen"
      reputation: "Braucht Ruf bei 'Diebesgilde' (Stufe 3+)"
      codewort: "Täglich wechselndes Passwort von NPC bekommen"

    rewards:
      higher_risk_higher_reward: true
      gold_multiplier: 3x  # 3x mehr Münzen als offizielle Arena
      illegal_items: "Schwarzmarkt-Waffen, Verbotene Zauber"
      reputation_cost: "Ruf bei Stadtgarde sinkt"

    events:
      death_matches:
        frequency: "Jeden Freitag Nacht"
        format: "Bis zum Tod (oder Aufgabe)"
        pot: "Alle Teilnehmer zahlen 1000 Münzen ein → Winner takes all"

      monster_pits:
        description: "Gegen gefangene Monster kämpfen"
        difficulty: "Monster sind stärker als normale Overworld-Spawns"
        rewards: "Monster-Parts für Crafting"

  arena_progression:
    official_titles:
      - rank: "Bronze" (0-1200 Elo)
      - rank: "Silber" (1200-1600 Elo)
      - rank: "Gold" (1600-2000 Elo)
      - rank: "Platin" (2000-2400 Elo)
      - rank: "Champion" (2400+ Elo)

    underground_reputation:
      - rank: "Neuling" (0 Siege)
      - rank: "Kämpfer" (10 Siege)
      - rank: "Veteran" (50 Siege)
      - rank: "Legende" (100 Siege)
      - rank: "Blut-König" (200 Siege + 10 Death-Matches gewonnen)
```

### Graue Moral Integration:
```yaml
moral_choices:
  scenario_1:
    situation: "NPC bittet dich, Kampf zu werfen für Wettbetrug"
    choices:
      - accept:
          reward: "5000 Münzen sofort"
          consequence: "Ruf bei Arena sinkt, Untergrund-Ruf steigt"
      - refuse:
          reward: "Nichts"
          consequence: "Ruf bei Arena steigt, NPC wird Feind"
      - report:
          reward: "2000 Münzen Belohnung von Stadtwache"
          consequence: "Untergrund-Zugang VERLOREN (Quest-Chain Reset nötig)"

  scenario_2:
    situation: "Untergrund-Kampf: Gegner bittet um Gnade"
    choices:
      - kill:
          reward: "Volle Belohnung (3000 Münzen)"
          consequence: "Ruf bei 'Mörder-Fraktion' steigt, andere NPCs fürchten dich"
      - spare:
          reward: "Halbe Belohnung (1500 Münzen)"
          consequence: "NPC wird später Verbündeter, Quest-Geber"
```

---

## ✅ FEATURE 3: NPC/MONSTER REKRUTIERUNG FÜR LEBENSRAUM

### Konzept:
**Trupp-Management NUR im Lebensraum (Housing), NICHT im Hauptspiel**

### Implementation:

```yaml
recruitment_system:
  recruitment_methods:
    quest_rewards:
      - "NPC schließt sich nach Quest an"
      - "Beispiel: Rette Bauern-Familie → Bauer arbeitet auf deiner Farm"

    hiring:
      - "NPCs für Münzen anheuern"
      - "Preise: 100-5000 Münzen je nach Skill"
      - "Beispiel: Schmied (2000 Münzen) → kann Waffen craften"

    favors:
      - "NPC braucht Hilfe → danach arbeitet er für dich"
      - "Beispiel: Heile krankes Kind → Alchemist gibt dir Rabatt + bietet Arbeit an"

    monster_taming:
      - "Monster im Kampf auf <20% HP bringen → Fangen-Chance"
      - "Gefangene Monster können auf Farm/Lebensraum arbeiten"
      - "Beispiel: Slime → gibt tägliche Slime-Drops"
      - "Beispiel: Wolf → bewacht Haus"

    enslavement:
      - "DARK PATH: Feinde versklaven (nur wenn Moral-System erlaubt)"
      - "Konsequenzen: Ruf sinkt massiv, Sklaven rebellieren (50% Chance nach 7 Tagen)"
      - "Vorteil: Kostenlos, aber moralisch verwerflich"

  lebensraum_usage:
    housing_roles:
      farmers:
        - "Bewirtschaften Felder automatisch"
        - "Produzieren Crops täglich"
        - "Skill: Farming-Level (1-100)"

      guards:
        - "Bewachen Haus vor Überfällen (random Event)"
        - "Monster-Guards stärker als NPC-Guards"

      crafters:
        - "Schmied: Craftet Waffen/Rüstung (braucht Mats)"
        - "Alchemist: Stellt Tränke her"
        - "Koch: Macht Food-Buffs"

      companions:
        - "Begleiten Spieler im Kampf (max 1 aktiv)"
        - "Können in Lebensraum trainieren (+XP)"

      servants:
        - "Kümmern sich um Haus (Dekoration, Reparaturen)"
        - "Sammeln Ressourcen (Holz, Stein)"

  mass_battle_system:
    availability: "NUR im Lebensraum"

    scenario:
      - "Spieler baut 'Trainingsplatz' in Lebensraum"
      - "Kann dort NPC-Truppen + Monster aufstellen"
      - "Startet 'Belagerungs-Modus' (optional!)"

    mechanics:
      - "Spieler plant Formation (wie M&B2)"
      - "NPCs kämpfen automatisch basierend auf AI"
      - "Spieler kann in Schlacht eingreifen (spielbar) oder zuschauen"

    use_cases:
      - "Training für NPCs (sie leveln durch Kämpfe)"
      - "Defense-Event: Banditen greifen Hof an"
      - "Optionales PvP: Spieler können Höfe angreifen (wenn aktiviert)"

    wichtig:
      - "NICHT im Hauptspiel (Open-World)!"
      - "Trupp-Steuerung passt nicht zu Action-Combat"
      - "Nur in instanziertem Lebensraum"

  progression:
    lebensraum_levels:
      tier_1:
        name: "Kleine Hütte"
        max_npcs: 3
        max_monsters: 2
        features: "1 Schlafplatz, kleiner Garten"

      tier_2:
        name: "Bauernhof"
        max_npcs: 8
        max_monsters: 5
        features: "Felder, Stall, Werkstatt"
        cost: "10,000 Münzen"

      tier_3:
        name: "Anwesen"
        max_npcs: 20
        max_monsters: 10
        features: "Große Felder, Schmiede, Alchemie-Labor, Trainingsplatz"
        cost: "50,000 Münzen"

      tier_4:
        name: "Festung"
        max_npcs: 50
        max_monsters: 30
        features: "Mauern, Türme, Kaserne, Großer Trainingsplatz"
        cost: "200,000 Münzen"
        unlock: "Quest 'Lord der Lande' abschließen"
```

### UI-Konzept (Lebensraum-Management):
```
┌──────────────────────────────────────────────────────┐
│ LEBENSRAUM: Kuja's Hof (Tier 2 - Bauernhof)          │
├──────────────────────────────────────────────────────┤
│ NPCs (5/8):                                          │
│ ⚒️ Schmied Hans (Skill: 45) - [Crafting Waffen]     │
│ 🌾 Bauer Riku (Skill: 60) - [Bewirtschaftet Feld 1] │
│ 🛡️ Wache Sofia (Level 20) - [Patrouille Eingang]   │
│ 🧪 Alchemistin Yuki (Skill: 55) - [Tränke herstellen]│
│ 👨‍🍳 Koch Marco (Skill: 40) - [Food-Buffs machen]    │
│                                                       │
│ Monster (3/5):                                        │
│ 🐺 Wolf 'Fenrir' (Level 15) - [Wache Hinterhof]     │
│ 🟦 Slime 'Goo' (Level 5) - [Produziert Slime-Gel]   │
│ 🦎 Baby-Drache 'Ember' (Level 10) - [Training]      │
│                                                       │
│ [NPCs verwalten] [Monster zuweisen] [Trainingsplatz]│
└──────────────────────────────────────────────────────┘
```

---

## ✅ FEATURE 5: FRAKTIONS-RUF MIT GRAUER MORAL

### Konzept:
**Ruf-System mit moralischen Konsequenzen**

```yaml
faction_reputation_system:
  factions:
    argentum_guard:
      description: "Stadtwache von Argentum"

      reputation_levels:
        hated: -1000 to -500
          effects:
            - "Wachen greifen bei Sichtkontakt an"
            - "Einreise verboten"
            - "Kopfgeld: 5000 Münzen"

        unfriendly: -499 to -100
          effects:
            - "Höhere Preise bei Vendors (+50%)"
            - "Keine Quests verfügbar"
            - "Wachen beobachten dich"

        neutral: -99 to 99
          effects: "Standard-Preise, basis Quests"

        friendly: 100 to 499
          effects:
            - "Rabatt bei Vendors (-10%)"
            - "Mehr Quests verfügbar"
            - "Wachen helfen im Kampf"

        honored: 500 to 999
          effects:
            - "Rabatt (-25%)"
            - "Exklusive Quests"
            - "Zugang zu Wachen-Trainingsplatz"

        exalted: 1000+
          effects:
            - "Ehren-Titel: 'Held von Argentum'"
            - "Freier Zugang zu allen Bereichen"
            - "Kostenloser Teleport (ausnahme!)"
            - "Legendary Quest-Chain freischalten"

      reputation_gains:
        - "Banditen töten: +10 Ruf"
        - "Quest für Hauptmann: +50 Ruf"
        - "Verbrecher verhaften: +25 Ruf"

      reputation_losses:
        - "Verbrechen begehen: -100 Ruf"
        - "Wache angreifen: -500 Ruf"
        - "Bei Untergrund-Arena erwischt: -200 Ruf"

    thieves_guild:
      description: "Diebesgilde (Untergrund)"

      conflict_with: "argentum_guard"  # Gegensätzliche Fraktionen!

      reputation_levels:
        # Ähnlich wie oben, aber Vorteile sind:
        exalted:
          effects:
            - "Titel: 'Meisterdieb'"
            - "Zugang zu Schwarzmarkt"
            - "Kann Untergrund-Arena betreten"
            - "Fence kauft gestohlene Items"

      reputation_gains:
        - "Erfolgreich stehlen: +15 Ruf"
        - "Untergrund-Arena gewinnen: +20 Ruf"
        - "Quest für Gildenmeister: +100 Ruf"

      reputation_losses:
        - "Mit Stadtwache kooperieren: -200 Ruf"
        - "Gildenmitglied verraten: -1000 Ruf (sofort Hated)"

    mages_guild:
      description: "Magier-Akademie"

      reputation_levels:
        exalted:
          effects:
            - "Titel: 'Erzmagier'"
            - "Zugang zu Verbotener Bibliothek"
            - "Legendary Zauber-Bücher kaufbar"
            - "Kann andere Spieler in Magie trainieren"

      reputation_gains:
        - "Zauber erforschen: +10 Ruf"
        - "Magisches Artefakt finden: +50 Ruf"
        - "Prüfung bestehen: +100 Ruf"

  gray_morality_examples:
    scenario_1:
      situation: "Dieb stiehlt Brot für hungrige Familie"
      choices:
        - option: "Dieb verhaften"
          argentum_guard: +50
          thieves_guild: -50
          personal_morality: "Lawful"

        - option: "Wegsehen"
          argentum_guard: 0
          thieves_guild: +25
          personal_morality: "Neutral"

        - option: "Dieb helfen + Bäcker bezahlen"
          argentum_guard: 0
          thieves_guild: 0
          personal_morality: "Good"
          cost: 50 Münzen

    scenario_2:
      situation: "Korrupter Wachen-Hauptmann verlangt Bestechung"
      choices:
        - option: "Bezahlen (100 Münzen)"
          argentum_guard: +25 (kurzfristig)
          result: "Hauptmann wird später zum Feind (Quest-Chain)"

        - option: "Ablehnen"
          argentum_guard: -50 (kurzfristig)
          result: "Hauptmann wird später verhaftet (du bekommst Belohnung)"

        - option: "An höhere Instanz melden"
          argentum_guard: +100 (langfristig)
          result: "Hauptmann entlassen, neuer NPC erscheint"

  reputation_conflict_system:
    opposing_factions:
      - [argentum_guard, thieves_guild]
      - [mages_guild, witch_coven]
      - [light_church, demon_cult]

    rules:
      - "Wenn Ruf bei Fraktion A steigt, sinkt Ruf bei gegnerischer Fraktion B (50% des Gewinns)"
      - "Beispiel: +100 Ruf bei Stadtwache → -50 Ruf bei Diebesgilde"
      - "Spieler muss sich entscheiden: Beide Seiten spielen = schwer!"
```

---

## ❌ FEATURE 4: TELEPORT-SYSTEM (EINGESCHRÄNKT!)

### Konzept:
**Teleport ist TEUER und SELTEN, kein Convenience-Feature**

```yaml
teleport_system:
  philosophy:
    - "Teleport ist für Testing/Debug - NICHT für normales Gameplay!"
    - "Spieler SOLLEN die Welt erkunden"
    - "Procedural Generation macht Reisen interessant"

  ingame_teleport_options:
    mage_teleport_service:
      locations:
        - "Schwarze Mühle → Argentum"
        - "Argentum → Kristallberge"
        - "Argentum → Wüstenstadt"

      cost:
        base: 5000 Münzen (1-Weg!)
        distance_multiplier: "+1000 Münzen pro Region-Entfernung"
        example: "Schwarze Mühle → Wüste = 5000 + 3000 = 8000 Münzen"

      availability:
        requirement: "Quest 'Die Teleporter-Gilde' abschließen (Level 30+ Quest)"
        locations: "Nur in Major Cities (5 Städte)"
        cooldown: "1x pro Tag (In-Game Tag = 2 Stunden Realzeit)"

    teleport_scrolls:
      source: "Legendary Quest-Belohnung oder Boss-Drop (0.1% Chance)"

      types:
        scroll_of_recall:
          effect: "Teleport zurück zur letzten Stadt"
          uses: 1 (verbraucht!)
          value: 10,000 Münzen

        scroll_of_home:
          effect: "Teleport zu deinem Lebensraum"
          uses: 3
          value: 5,000 Münzen
          crafting: "Meister-Alchemist + 50x seltene Mats"

      rarity: "So selten, dass Spieler sie HORTEN und nie nutzen!"

    teleport_beacons:
      description: "Spieler kann Beacon in der Welt platzieren"

      mechanics:
        - "Max 3 Beacons gleichzeitig"
        - "Beacon kostet: 20,000 Münzen + Quest-Item"
        - "Teleport zu Beacon: 2000 Münzen"
        - "Andere Spieler können Beacons NICHT nutzen"

      use_case: "Für Dungeon-Farming oder Boss-Grinding"

      risk: "Beacon kann von Monstern zerstört werden (10% Chance pro Tag)"

  debug_teleport:
    availability: "NUR für Testing (wird in Release deaktiviert)"
    command: "/tp [location]"
    ui: "Cheat-Menu (Strg+Shift+T) - nur in Dev-Mode"

  alternative_travel:
    mounts:
      horse:
        speed: "+50% Bewegung"
        cost: 1000 Münzen

      griffin:
        speed: "+100% Bewegung + Fliegen"
        cost: 50,000 Münzen
        requirement: "Level 40 + Quest"

    fast_travel_unlocks:
      - "Pro Region 1x 'Wegpunkt' freischalten (durch Erkunden)"
      - "Wegpunkt → Wegpunkt Reise: Kostet nur 500 Münzen"
      - "Aber: Muss beide Wegpunkte ERST entdecken!"

  procedural_world_benefits:
    - "Jede Reise = neue Random-Encounters"
    - "Gathering-Nodes spawnen während Reise"
    - "Hidden Events nur durch Reisen findbar"
    - "Reisen ist TEIL des Gameplays, nicht lästig!"
```

---

## ✅ FEATURE 10: HOUSING UPGRADE-SYSTEM

### Status:
**Sollte bereits implementiert sein - VERIFIKATION nötig!**

```yaml
housing_verification:
  check_files:
    - "digivice/data/housing.json"
    - "backend/api/housing.py"

  expected_features:
    upgrades:
      - "Haus-Größe upgraden (Small → Medium → Large)"
      - "Räume hinzufügen (Küche, Schmiede, Alchemie-Labor)"
      - "Lager-Kapazität erhöhen"

    npc_servants:
      - "Koch einstellen"
      - "Butler/Maid einstellen"
      - "Gärtner für Farm"

    farm_upgrades:
      - "Mehr Felder freischalten"
      - "Tiergehege bauen"
      - "Bewässerungs-System (automatische Ernte)"

    decorations:
      - "Möbel platzieren"
      - "Trophäen (Boss-Drops) ausstellen"
      - "Pflanzen/Garten gestalten"

  if_missing:
    priority: "P1 - Wichtig für Endgame"
    assign_to: "OPUS (Frontend + Game Design)"
```

---

## 📋 IMPLEMENTATION ROADMAP

### Phase 1 - MVP (P0):
1. ✅ **Companion Skill-Learning** (Backend: SONNET, Frontend: OPUS)
   - Datenstruktur: `backend/systems/companion_skills.py`
   - UI: `digivice/js/companion_management.js`
   - Estimated: 2-3 Tage

2. ✅ **Arena 2-Tier System** (Backend: SONNET, Design: OPUS)
   - Offizielle Arena erweitern: `backend/api/arena.py`
   - Untergrund-System: `backend/api/underground_arena.py`
   - Locations + NPCs: OPUS
   - Estimated: 3-4 Tage

3. ✅ **Teleport-Restrictions** (Backend: SONNET)
   - Mage-Service: `backend/api/teleport.py`
   - Kosten-System implementieren
   - Debug-Mode Trennung
   - Estimated: 1 Tag

### Phase 2 - Beta (P1):
4. ✅ **NPC/Monster Recruitment** (Backend: SONNET, UI: OPUS)
   - Rekrutierungs-System: `backend/systems/recruitment.py`
   - Lebensraum-Management: `backend/api/lebensraum.py`
   - UI für Trupp-Verwaltung: OPUS
   - Estimated: 5-7 Tage

5. ✅ **Fraktions-Ruf mit grauer Moral** (Backend: SONNET, Quests: OPUS)
   - Ruf-System: `backend/systems/faction_reputation.py`
   - Quest-Consequences: OPUS schreibt Quests
   - Estimated: 3-4 Tage

### Phase 3 - Post-Launch (P2):
6. ✅ **Mass-Battle System (Lebensraum)** (Komplex - OPUS Lead)
   - Trupp-AI: `backend/systems/troop_ai.py`
   - Schlacht-UI: Three.js Integration
   - Estimated: 7-10 Tage

---

## 🎯 TASK-ASSIGNMENT

### SONNET (Backend, Systeme):
- [ ] Companion Skill-Learning Backend
- [ ] Arena-Erweiterung (Underground-API)
- [ ] Teleport-Cost-System
- [ ] Recruitment-System Backend
- [ ] Faction-Reputation Backend

### OPUS (Frontend, Content, Design):
- [ ] Companion UI + Skill-Display
- [ ] Arena-Locations + NPCs erstellen (Underground)
- [ ] Recruitment-UI (Lebensraum-Management)
- [ ] Quest-Writing für Fraktionen (graue Moral)
- [ ] Housing-System verifizieren + erweitern

---

**Bereit für Implementation!** 🚀
Welches Feature soll als erstes angegangen werden?
