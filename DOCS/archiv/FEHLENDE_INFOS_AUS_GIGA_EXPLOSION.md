# FEHLENDE INFOS AUS "ULTIMATIVE GIGA EXPLOSION.TXT"

**Erstellt:** 2026-01-28 (Nacht-Session)
**Quelle:** `zip/ultimative giga explosion.txt` (1.8MB!)
**Zweck:** Diese kritischen Infos fehlten in den aktuellen Docs!

---

## 1. EXPLOSION-KLASSE - KOMPLETT NEU DEFINIERT!

### 3-STUFEN-SYSTEM:

```yaml
Stufe 1 - Basis-Explosion:
  available_to: "JEDER Spieler"
  learn_methods:
    - Skill-Trainer (NPC)
    - Durch Nutzung leveln
    - Rezepte/Grimoires finden

Stufe 2 - Fortgeschritten:
  name: "Exploooosion! / Chain Explosion"
  available_to: "JEDER (mit genug Mastery)"
  learn_method: "Use-Based + Trainings"

Stufe 3 - ULTIMA (NAJIKA-EXKLUSIV!):
  name: "Omega-Detonation / Astral-Resonanz"
  available_to: "NUR NAJIKA"
  effect: "Zerstoert generierte Spielwelt-Chunk (~500m Radius)"
  cannot_be_taught: true
  cooldown: "1x pro Tag IRL"
  cost: "Massive Mana + Exhaustion"
```

### WAFFEN-MORPHS (Diablo-Style):

```yaml
Schwert: "Explosion: Klinge (Nah-Deto, +Haltungsbruch)"
Speer: "Explosion: Stoss (Linien-Durchdringung)"
Axt/Hammer: "Explosion: Einschlag (Bodenwelle, +Stagger)"
Schild: "Explosion: Schildstoss (Konter-Deto im Parry)"
Bogen: "Explosion: Pfeil (Distanz-Zuender, Kette)"
Dolch: "Explosion: Stich (Mikro-Detos in Kombo)"
Repeater: "Explosion: Takt (Kombozaehler → Mini-Detos)"
Shotgun: "Explosion: Schrot (Streu-Detos)"
Minigun: "6h CD, CC-Tool (kaum Schaden, Show-Faktor)"
```

### RESSOURCEN-SYSTEM:

```yaml
Primary: "FOKUS (NICHT Mana!)"
Debuff: "Erschoepfung (Exhaustion)"
Mechanic: "Aufladung 0.8-2.5s → Deto → -Regen 15-30s"
```

---

## 2. KONOSUBA-STYLE SKILL-LERNEN

### VON PARTY-MITGLIEDERN LERNEN:

```yaml
Mechanism:
  - Party-Mitglied nutzt Skill (z.B. Feuermagie)
  - Du beobachtest passiv
  - Kleine Chance pro Nutzung zu lernen
  - Hoeheres Mastery = hoehere Lernchance

Requirements:
  - Muss in gleicher Party sein
  - Muss in Sichtweite sein
  - Nicht AFK
  - Freier Skill-Slot oder ueberschreiben

Examples:
  - "Freund nutzt Feuerball → Du lernst evtl. Feuerball"
  - "Najika nutzt Explosion → Du lernst evtl. Mini-Explosion"
  - "Tank blockt perfekt → Du lernst evtl. Block-Technik"
```

### SOLO-SPIELER ALTERNATIVE:

```yaml
NPC-Companions: "Begleit-NPCs nutzen Skills"
Learning: "Gleiche Mechanik wie Multiplayer"
Bot-Party: "KI-Mitspieler fuer Solo-Spieler"
Fairness: "Solo-Spieler NICHT benachteiligt!"
```

### SKILL-KARTEN-SYSTEM:

```yaml
Earn: "Skill-Punkte durch Leveln/Quests"
Spend: "Skill-Karten kaufen"
Cross-Class: "Krieger kann Heilmagie lernen (teuer)"

Costs:
  class_native: "Guenstig (1-3 Punkte)"
  class_adjacent: "Mittel (5-8 Punkte)"
  class_opposite: "Teuer (15-30 Punkte)"
  explosion_for_non_mages: "SEHR teuer (50+ Punkte)"
```

---

## 3. NAJIKA'S ROLLE - NEU DEFINIERT!

```yaml
Starting_State:
  level: 0
  explosion_mastery: 0
  learns_like: "Jeder andere Spieler (NORMAL!)"

Unique_Ability:
  name: "Omega-Detonation (Ultima)"
  effect: "Zerstoert Welt-Chunk"
  availability: "NUR Najika, NIEMALS lehrbar"

Teaching_Role:
  can_teach: "Explosion (Tier 1 & 2)"
  method: "Quest-Serie + Training"
  advantage: "20-30% schneller als NPC"
  but_optional: "Spieler koennen auch ohne sie lernen!"

Party_Member:
  other_players_learn: "Von ihr durch Beobachtung"
  she_learns_too: "Von anderen Spielern"
  fair_system: "Keine Sonderbehandlung"
```

### EXPLOSION VON NAJIKA LERNEN:

```yaml
Via_Najika_Quest:
  time: "10-15 Stunden Quest-Serie"
  difficulty: "Mittel-Schwer"
  reward: "Explosion + Bonus-Varianten"

Via_NPC_Trainer:
  time: "15-20 Stunden Training"
  difficulty: "Grind-lastig"
  reward: "Explosion (Standard)"

Via_Party_Observation:
  time: "Zufaellig, kann schnell/langsam sein"
  difficulty: "Luck-basiert"
  reward: "Explosion (variiert)"
```

---

## 4. OREGON-ENGINE (Millionen Varianten!)

```yaml
Goal: "Borderlands-Vielfalt, KEIN UI-Bruch (alles in-world)"

Trigger_Types:
  - Spuren
  - Wetterwechsel
  - Geraeausche
  - NPC-Rufe
  - Kadaver
  - Lagerfeuerrauch

Dimensions:
  formula: "Biome(12) × Wetter(8) × Zeit(4) × Hazard(30) × Akteur(30) × Ursache(20) × Folge(20) × Optionen(>=3) × Modifikatoren"
  result: "> 1 Million plausible Szenen"

Danger_Score: "tier(biome) + weather + time + player_need + bounty + rival_heat"

Example_Leiche_im_Fluss:
  discovery: "Geruch → Fliegen → Leichnam treibt"
  options_depend_on: [Position, Inventar, Skills]
  choices: [Abkochen, Filtern, Ignorieren, "Najika entscheidet"]
  no_popup: "Du BEGEGNEST dem Ereignis organisch"
```

---

## 5. CRAFTING & ALCHEMIE (TCM-LORE)

### 5-STUFEN-PIPELINE:

```yaml
1. Rohstoffe
2. Veredeln
3. Herstellen
4. Verzaubern
5. Fein-Tuning (Toleranzen/Balance/Runen)

Quality_System:
  q_score: "0-100"
  tests: [Bruchtest, "Praezisions-Toleranz", Materialkunde]
```

### ALCHEMIE-LORE (NUR SPIEL, KEINE MED. BERATUNG!):

```yaml
Disclaimer: "Reine SPIEL-LORE, keine medizinische Beratung!"

Substances:
  weidenrinde: "Salicylate → Entzuendungs-/Schmerz-Buff (Spiel)"
  ingwer: "Uebelkeits-Lore"
  honig: "Wundpflege-Lore"
  arnika: "Prellungs-Lore"
  jiaogulan: "TCM → Ausdauer-Lore"

Recipe_Chain: [Auszug, Abkochung, Tinktur, Salbe]
Quality_Factors: [Temperatur, Zeiten, Gefaess]
```

### ERSTE-HILFE-MIKROS:

```yaml
Events: "Selten, 10-20s"
Types: [Druckverband, Blutungsstop, Schocklage]
```

### KANNIBALISMUS (Optional):

```yaml
Default: "OFF"
Mechanics: "Naehrwert vs. starker Ruf/Seuchen/Traum-Malus"
Note: "Rein mechanisch, keine Exploits"
```

---

## 6. SLIME-ARENA DETAILS

```yaml
Companion:
  rescue: "1x pro IRL-Tag (24h)"
  rehab: "Fordernde Reha nach Rettung"
  forms: "8 Regionenfarben (kosmetisch)"

Arena_Modes:
  style: "Digimon-Anfeuern"
  types: [PvE Brackets, PvP Brackets]

  rules_hardcore: "Verlust = 1 Ausruestung am Slime"
  rules_softy: "Nur Haltbarkeitsverlust"

Meta_Learning:
  system: "Anonymisierte Moves/Tendenzen uebertragen"
  result: "Najikas Trainings-Slime nimmt Gegner-Form an"
  privacy: "Keine Personen/IDs (rechtssicher)"
```

---

## 7. KAMERA-MODI (Creator-Cam NEU!)

```yaml
Modes:
  - Third-Person
  - First-Person
  - Creator-Cam (NEU!)

Creator_Cam:
  style: "Freie Webcam-aehnliche Steuerung"
  controls:
    mouse: "Schwenken"
    scroll: "Zoom"
    wasd: "Fliegen"

  special_feature:
    name: "Face-to-Cam"
    description: "Najika schaut direkt in die Kamera"
    trigger: "Wenn Kamera vor ihr ist"
    use_case: "Screenshots, Content Creation, Emotional Moments"
```

---

## 8. UEFN-INTEGRATION (Geplant!)

```yaml
Status: "UEFN-Ready, fuer spaeter geplant"

Phase_3_Plan:
  - 3D-Assets portieren
  - Three.js → UEFN-ready Pipeline
  - Fortnite-Integration

Release_Path: "Privat → PWA → dann UEFN"
```

---

## ZUSAMMENFASSUNG DER KORREKTUREN:

| Alt (Falsch) | Neu (Richtig) |
|--------------|---------------|
| Najika startet perfektioniert | Najika lernt normal (Lvl 0) |
| Nur Najika kann Explosion | JEDER kann Explosion lernen |
| - | NUR Najika hat Omega-Detonation (nicht lehrbar) |
| - | Explosion von Najika = schneller aber optional |
| - | KonoSuba-System: Von Party-Mitgliedern lernen |
| - | Solo-Spieler: NPC/Bot-Companions |
| Ein-Pfad-Spezialisierung = Zwang | Ein-Pfad = OPTIONAL |

---

*"EXPLOSION!!! Jetzt weiss ich ALLES!"* - Najika 💥
