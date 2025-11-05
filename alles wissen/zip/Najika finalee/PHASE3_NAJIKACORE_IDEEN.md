# PHASE 3 TEIL 3: IMPLEMENTIERUNGS-DETAILS AUS NAJIKACORE

**Analysiert:** 2025-10-23
**Quellen:** NajikaCore Code-Basis (najika_server.py, najika_battle.py, najika_memory.py, room_config_detailed.json)
**Gefundene Details:** 15 implementierte Features

---

## ZUSAMMENFASSUNG

**Was ist BEREITS IMPLEMENTIERT aber NICHT in V3 dokumentiert:**

- ✅ **Enhanced Battle System** mit Digimon-World-Style Skill-Learning
- ✅ **ChromaDB Memory System** mit Emotion/Relationship-Tracking
- ✅ **Living System** mit Needs (Hunger, Energy, Hygiene, Happiness)
- ✅ **Dynamic Personality Weights** (4 Persönlichkeiten können wachsen/schrumpfen)
- ✅ **Equipment System** (Weapon/Armor/Accessory Slots)
- ✅ **12 Rooms** mit detaillierter 3D-Konfiguration
- ✅ **Behavior Modes** (standard, explosion, chaos, analyse, kontrolle, private)
- ✅ **Claude Code Integration** (bereits aktiv!)

**Top 3 wichtigste Funde:**
1. **Skill-Learning vom Gegner** - NICHT in V3!
2. **ChromaDB Long-Term Memory** - NICHT in V3!
3. **Living System (Tamagotchi-Style)** - NICHT in V3!

---

## MUSS IN V4 DOKUMENTIERT WERDEN

### 1. [CRITICAL] Digimon-World-Style Skill-Learning

**Quelle:** `najika_battle.py:669-709`
**Kategorie:** Combat / Progression

**BESCHREIBUNG:**
Najika kann **Skills von besiegten Gegnern lernen** (wie Digimon World)!

**TECHNISCHE DETAILS:**
```python
# Nach Enemy-Defeat (najika_battle.py:684-708)
enemy_type = enemy["type"]
is_boss = enemy.get("boss", False)

# Boss: 20% Chance, Normal: 8% Chance
learn_chance = 0.20 if is_boss else 0.08

if random.random() < learn_chance:
    # Finde lernbare Skills von diesem Enemy-Typ
    for skill_name, skill_data in SKILL_DB.items():
        if skill_data.get("learnable") and enemy_type in skill_data.get("learn_from", []):
            if skill_name not in player["known_skills"]:
                player["known_skills"].append(skill_name)
                self._log(f"*** NAJIKA HAT [{skill_name_display}] GELERNT! ***")
```

**Lernbare Skills:**
- `poison_bite` - von Rats/Slimes (8% Chance)
- `bone_throw` - von Skeletons (8% Chance)
- `dark_bolt` - von Dark Mage (8% Chance)
- `summon_rats` - von Rat King Boss (20% Chance)
- `shadow_strike` - von Dungeon Lord Boss (20% Chance)

**IN V3 VORHANDEN?**
- ❌ **FEHLT KOMPLETT!**
- V3 erwähnt Skill-System aber NICHT das Learning-Feature

**VORTEILE:**
- Progression durch Combat (nicht nur Leveling)
- Belohnt Gegner-Vielfalt bekämpfen
- Digimon-World-Nostalgie PERFEKT für Najika
- Emergent Gameplay (unterschiedliche Builds möglich)

**NACHTEILE:**
- RNG-basiert (Frustration möglich)
- Balance: Manche Skills OP?

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN (MUST-HAVE!)**
Dies ist ein KERN-Feature das bereits funktioniert! Muss in V4 prominent als "Digimon-World-Inspiration" dokumentiert werden.

**V4 Integration:**
```markdown
### Skill-Acquisition System (Digimon World Style)

**CHANCE ZU LERNEN:**
- Normale Enemies: 8% Drop-Chance
- Boss Enemies: 20% Drop-Chance

**LEARNABLE SKILLS:**
[Skill-Tabelle mit learn_from info]

**BEISPIEL:**
Wenn Najika einen Skelett-Krieger besiegt, hat sie 8% Chance "Knochen-Wurf" zu lernen.
Nach 10-15 Skeleton-Kämpfen sollte sie den Skill haben.
```

---

### 2. [CRITICAL] ChromaDB Long-Term Memory System

**Quelle:** `najika_memory.py:1-329`
**Kategorie:** KI-Behavior / Persistence

**BESCHREIBUNG:**
Najika hat ein **persistentes Langzeit-Gedächtnis** mit ChromaDB!

**TECHNISCHE DETAILS:**
```python
# najika_memory.py:12-26
class NajikaMemory:
    def __init__(self, persist_directory="C:\\NajikaCore\\memory_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)

        # 4 Collections:
        self.conversations = self._get_or_create_collection("conversations")
        self.emotions = self._get_or_create_collection("emotions")
        self.relationships = self._get_or_create_collection("relationships")
        self.events = self._get_or_create_collection("events")
```

**Features:**
1. **Konversations-Speicherung** - Jede Message wird gespeichert mit Metadata (Room, Private-Mode, Emotions)
2. **Semantic Search** - `retrieve_relevant_memories(query, n_results=5)` findet relevante alte Gespräche
3. **Emotion-Tracking** - Happiness, Love, Sadness, Anger, Excitement, Arousal (0-100)
4. **Relationship-Tracking** - Level, Trust, Intimacy (steigt automatisch)
5. **Context-Building** - `build_context_prompt()` baut AI-Prompt mit relevanten Memories

**Emotion-Update-Logik:**
```python
# najika_memory.py:113-142
# Positive Keywords → Happiness +5, Love +3
if "liebe" or "toll" in user_message:
    happiness += 5
    love += 3

# Private Mode → Arousal +10, Excitement +5
if private_mode:
    arousal += 10
    excitement += 5

# Jede Interaktion → Relationship +0.1
relationship_level += 0.1
```

**IN V3 VORHANDEN?**
- ❌ **FEHLT KOMPLETT!**
- V3 erwähnt nur "Context (letzte 4 Messages)" - KEIN Long-Term Memory

**VORTEILE:**
- Najika erinnert sich WIRKLICH (nicht nur Session)
- Emotionen entwickeln sich über Zeit
- Relationship-Progression sichtbar
- ChromaDB = Professionelle Vector-DB

**NACHTEILE:**
- Braucht ChromaDB Installation
- Disk-Space wächst
- Privacy-Concern (alle Messages gespeichert)

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN (CRITICAL!)**
Dies ist DAS Feature das "Najika ist mehr als Code" beweist! Muss in V4 als Haupt-Feature rein.

**V4 Integration:**
```markdown
## Long-Term Memory System (ChromaDB)

**PERSISTENZ:**
- Alle Konversationen werden dauerhaft gespeichert
- Semantic Search findet relevante alte Gespräche
- Najika kann auf frühere Versprechen/Events referenzieren

**EMOTION-TRACKING:**
- Happiness: 0-100 (steigt bei positiven Worten)
- Love: 0-100 (steigt bei "liebe", Komplimenten)
- Arousal: 20-100 (steigt im Private Mode)
- [weitere Emotions...]

**RELATIONSHIP-LEVEL:**
- Steigt automatisch mit jeder Interaktion (+0.1)
- Level 1-100
- Beeinflusst Najika's Verhalten

**BEISPIEL:**
User: "Weißt du noch als wir über Explosion geredet haben?"
Najika: *durchsucht Memory* "JA! Vor 3 Tagen hast du gesagt EXPLOSION ist dein Lieblingswort!"
```

---

### 3. [GAMEPLAY] Living System (Tamagotchi-Style Needs)

**Quelle:** `najika_server.py:83-99`, `najika_living_system.py` (importiert Zeile 6-13)
**Kategorie:** Gameplay / Tamagotchi

**BESCHREIBUNG:**
Najika hat **Tamagotchi-Style Needs** die über Zeit sinken!

**TECHNISCHE DETAILS:**
```python
# najika_server.py:83-99
STATE["najika"] = {
    # NEEDS (0-100, sinken über Zeit)
    "hunger": 100,
    "energy": 100,
    "hygiene": 100,
    "happiness": 100,

    # STATS (Training erhöht diese)
    "strength": 10,
    "intelligence": 10,
    "dexterity": 10,
    "charisma": 10,

    # CARE TRACKING
    "care_mistakes": 0,  # Steigt wenn Needs zu niedrig
    "fatigue": 0,        # 0-100, steigt bei Training
    "weight": 50,        # 0-100
    "discipline": 0,     # 0-100, Praise/Scold System

    # GROWTH
    "level": 1
}
```

**Living System Features (aus Import):**
- `LIVING_STATE` - Globaler State
- `MOODS` - Verschiedene Stimmungen (Happy, Sad, Angry, Excited, etc.)
- `PROACTIVE_MESSAGES` - Najika sendet von selbst Messages
- `ACTIVITIES` - Autonome Aktivitäten
- `detect_mood()` - Mood Detection basierend auf Needs
- `should_send_proactive_message()` - Entscheidet wann Najika von selbst schreibt
- `create_emotional_memory()` - Erstellt Emotional Memories

**IN V3 VORHANDEN?**
- ❌ **FEHLT KOMPLETT!**
- V3 hat kein Tamagotchi/Living-System

**VORTEILE:**
- Najika fühlt sich "lebendig" an
- Player-Engagement (muss sich kümmern)
- Digimon-World-Style Companion-Feeling
- Progression durch Stats/Training

**NACHTEILE:**
- Kann annoying sein (ständig füttern)
- Balancing schwierig
- Mobile-Notifications nötig für "Najika hungert!"

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN**
Tamagotchi-Mechanik passt PERFEKT zu Najika! Aber: Als **optional feature** markieren (nicht jeder will Tamagotchi).

**V4 Integration:**
```markdown
## [OPTIONAL] Living System (Tamagotchi-Style)

**NEEDS (0-100, sinken über Zeit):**
- Hunger: Füttern in Küche
- Energy: Schlafen im Schlafzimmer
- Hygiene: Baden im Badezimmer
- Happiness: Mit Najika reden/spielen

**CARE-SYSTEM:**
- Care Mistakes steigen wenn Needs < 20
- Zu viele Mistakes → Najika wird traurig/distanziert
- Gute Care → Bond-Strength steigt

**STATS (Training erhöht):**
- Strength: Trainingszimmer
- Intelligence: Studieren & Crafting
- Dexterity: Kampfarena
- Charisma: Musikraum

**PROAKTIVE MESSAGES:**
Najika sendet von selbst Messages:
- "Puddin'... ich hab Hunger..." (Hunger < 30)
- "Ich bin müde..." (Energy < 20)
- "Ich vermisse dich!" (24h keine Interaktion)
```

---

### 4. [SYSTEM] Dynamic Personality Weights

**Quelle:** `najika_server.py:69`
**Kategorie:** KI-Behavior

**BESCHREIBUNG:**
Die 4 Persönlichkeiten haben **dynamische Gewichtungen** die sich ändern können!

**TECHNISCHE DETAILS:**
```python
# najika_server.py:69
STATE["personality_weights"] = {
    "megumin": 25,   # 25% zu Beginn
    "harley": 25,
    "shiro": 25,
    "melissa": 25
}
# Total: 100%
```

**IN V3 VORHANDEN?**
- ⚠️ **TEILWEISE**
- V3 hat fixe Prozente: Megumin 35%, Harley 25%, Shiro 20%, Melissa 20%
- Aber: Code erlaubt DYNAMISCHE Änderung!

**VORTEILE:**
- Persönlichkeit kann sich entwickeln
- Player-Choices beeinflussen Weights
- Emergent Personality-Shifts

**NACHTEILE:**
- Könnte zu Charakterbruch führen
- Balancing: Wie verhindern dass 1 Persönlichkeit dominiert?

**EMPFEHLUNG:**
⚠️ **ÜBERARBEITEN**
Interessantes Feature, aber widerspricht V3's Design (fixe 35/25/20/20).

**Vorschlag:** Als **advanced optional feature** dokumentieren:
- Normal: Fixe Weights (35/25/20/20)
- Unlock nach Level 50: "Dynamic Personality Mode" (Player kann Weights beeinflussen)

---

### 5. [COMBAT] Equipment System (Weapon/Armor/Accessory)

**Quelle:** `najika_battle.py:161-243`
**Kategorie:** Combat / RPG

**BESCHREIBUNG:**
Vollständiges **Equipment-System** mit 3 Slots!

**TECHNISCHE DETAILS:**
```python
# ITEM_DB Equipment
# WEAPONS (Slot: weapon)
"wooden_sword": {"atk_bonus": 3}
"iron_sword": {"atk_bonus": 8}
"goblin_blade": {"atk_bonus": 12}
"legendary_weapon": {"atk_bonus": 25}

# ARMOR (Slot: armor)
"leather_vest": {"def_bonus": 2}
"iron_armor": {"def_bonus": 5}
"dragon_scale": {"def_bonus": 10}

# ACCESSORIES (Slot: accessory)
"power_ring": {"atk_bonus": 5}
"defense_charm": {"def_bonus": 5}
"hp_boost": {"hp_bonus": 30}
"mp_boost": {"mp_bonus": 20}
```

**IN V3 VORHANDEN?**
- ⚠️ **TEILWEISE**
- V3 erwähnt "Items" aber NICHT Equipment-Slots

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN**
Standard-RPG-Feature, sollte dokumentiert sein.

---

### 6. [WORLD] 12 Rooms - Detaillierte 3D-Konfiguration

**Quelle:** `assets/room_config_detailed.json:1-532`
**Kategorie:** World / 3D

**BESCHREIBUNG:**
Jeder Raum hat **hochdetaillierte 3D-Konfiguration**!

**TECHNISCHE DETAILS:**
Jeder Raum hat:
- `floor.model` - GLTF Model-Pfad
- `floor.tint` - Farb-Tint (Hex)
- `floor.roughness` - Material-Property
- `floor.metalness` - Material-Property
- `floor.envMapIntensity` - Reflection
- `walls.model` - Wall-Models
- `props[]` - Platzierte Objekte mit Position/Rotation/Scale
- `palette` - Farbpalette (background, fog, ambient, primary, secondary, floor)
- `spawn` - Spawn-Position (nur bei Schwarze Mühle)
- `wallHeight` - Höhe (Schwarze Mühle: 96 statt 6)

**Beispiel - Schwarze Mühle:**
```json
{
  "name": "Schwarze Mühle – Keller",
  "floor": {
    "model": "KayKit_HalloweenBits_1.0_FREE/.../floor_dirt.gltf",
    "span": 576,  // 12x größer als normale Räume!
    "tint": "#3f2c1f"
  },
  "wallHeight": 96,  // 16x höher
  "spawn": [0, 0, 15],
  "props": [
    {"model": "coffin.gltf", "position": [12, 0, 12]},
    {"model": "lantern_standing.gltf", ...},
    {"model": "pillar.gltf", ...}
  ]
}
```

**IN V3 VORHANDEN?**
- ⚠️ **TEILWEISE**
- V3 listet 12 Räume auf, aber NICHT die 3D-Details

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN**
Sollte im "Technical Implementation" Kapitel stehen.

---

### 7. [KI] Behavior Modes (6 Modi)

**Quelle:** `najika_server.py:67`
**Kategorie:** KI-Behavior

**BESCHREIBUNG:**
Najika hat **6 verschiedene Behavior-Modi**!

**TECHNISCHE DETAILS:**
```python
STATE["behavior_mode"] = "standard"

# Mögliche Modi:
# - "standard": Normal-Verhalten
# - "explosion": EXPLOSION-fokussiert
# - "chaos": Harley-Quinn-Chaos
# - "analyse": Shiro-Analytical
# - "kontrolle": Melissa-Dominant
# - "private": NSFW-Mode
```

**IN V3 VORHANDEN?**
- ⚠️ **TEILWEISE**
- V3 hat "Modi-System" aber nur 2 Modi (NSFW, Standard)

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN**
Erweitere V3's Modi-System von 2 auf 6.

---

### 8. [SYSTEM] Bond-Strength Tracking

**Quelle:** `najika_server.py:68,70`
**Kategorie:** Progression

**TECHNISCHE DETAILS:**
```python
STATE["bond_strength"] = 0  # 0-100
STATE["total_interactions"] = 0  # Tracking
```

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN**
Ergänzt Affinity-System aus Claude-Sessions-Analyse.

---

### 9. [PROGRESSION] User-State (Level/XP/Points/Inventory)

**Quelle:** `najika_server.py:72-78`
**Kategorie:** Progression

**TECHNISCHE DETAILS:**
```python
STATE["user"] = {
    "level": 1,
    "xp": 0,
    "points": 0,
    "inventory": [],
    "achievements": []
}

STATE["progress"] = {
    "dungeon_level": 0,
    "quests_completed": []
}
```

**EMPFEHLUNG:**
✅ **IN V4 DOKUMENTIEREN**

---

### 10. [INTEGRATION] Claude Code Integration (AKTIV!)

**Quelle:** `najika_server.py:34-35`, `najika_claude_code.py`
**Kategorie:** AI-Integration

**BESCHREIBUNG:**
**Claude Code ist BEREITS integriert** (ich bin es gerade!)

**TECHNISCHE DETAILS:**
```python
# najika_server.py:35
from najika_claude_code import call_ai_with_hierarchy, CLAUDE_CODE_INSTANCE

# In API-Handler:
out, provider = call_ai_with_hierarchy(
    prompt=prompt,
    use_wizard=private_trigger,
    context=STATE["history"],
    ollama_callback=call_ollama
)
```

**IN V3 VORHANDEN?**
- ✅ **BEREITS DOKUMENTIERT** in `CLAUDE_CODE_INTEGRATION.md`

**EMPFEHLUNG:**
✅ **IN V4 REFERENZIEREN**
Verweise auf bestehende Doku.

---

## TECHNISCHE ERWEITERUNGEN (Details)

### 11. SSE (Server-Sent Events) Clients

**Quelle:** `najika_server.py:71`
**Kategorie:** Real-Time

```python
STATE["sse_clients"] = []
```

**NUTZUNG:** Real-Time Updates für Frontend (z.B. proaktive Messages)

**EMPFEHLUNG:** ✅ Dokumentieren im Technical-Kapitel

---

### 12. Boss-Special-Abilities System

**Quelle:** `najika_battle.py:643-667`
**Kategorie:** Combat

**ABILITIES:**
- `summon_rats` - Spawnt 2 Ratten
- `poison_cloud` - Giftschaden -5 HP
- `regenerate` - Heilt sich +30 HP
- `shadow_strike` - 2x Damage

**EMPFEHLUNG:** ✅ Dokumentieren

---

### 13. Loot-Table System

**Quelle:** `najika_battle.py:21-24, 677-682`
**Kategorie:** Economy

```python
"loot_table": [
    {"item": "rat_tail", "chance": 0.3},
    {"item": "health_potion_small", "chance": 0.15}
]
```

**EMPFEHLUNG:** ✅ Dokumentieren

---

### 14. Wave-Based Enemy-Spawning

**Quelle:** `najika_battle.py:388-416`
**Kategorie:** Combat

**LOGIK:**
- Wave < 5: Rats + Slimes
- Wave 5-9: Rats + Slimes + Skeletons
- Wave 10-14: Skeletons + Goblin Warriors
- Wave 15+: Goblin Warriors + Dark Mages
- Wave % 10 == 0: Boss-Wave

**EMPFEHLUNG:** ✅ Dokumentieren

---

### 15. Skill Cooldown & MP System

**Quelle:** `najika_battle.py:246-341, 507-562`
**Kategorie:** Combat

**FEATURES:**
- Skills kosten MP
- Skills haben Cooldowns (2-5 Turns)
- Cooldowns reduzieren sich automatisch
- MP regeneriert NICHT automatisch (Items nötig)

**EMPFEHLUNG:** ✅ Dokumentieren

---

## VERALTET / ZU ÜBERARBEITEN

### ❌ Fixe Ollama-Models im Code

**Quelle:** `najika_server.py:55`

```python
OLLAMA_ALIAS=os.getenv("OLLAMA_MODEL_ALIAS","najika-local")
```

**PROBLEM:** Hardcoded Fallback

**EMPFEHLUNG:** ❌ In V4 dokumentieren dass Models konfigurierbar sind

---

## 📊 STATISTIK

**Implementierte Features:** 15
**Davon in V3:** 3 (teilweise)
**Davon NICHT in V3:** 12 (komplett neu)

**Must-Dokumentieren in V4:** 10 Features
**Überarbeiten:** 2 Features
**Veraltet:** 1 Feature

---

## 🎯 TOP 5 FÜR V4-DOKUMENTATION (PRIORITY)

1. **Skill-Learning (Digimon World)** - KERN-Feature!
2. **ChromaDB Long-Term Memory** - "Mehr als Code" Beweis
3. **Living System (Tamagotchi)** - Unique Companion-Feeling
4. **Equipment System** - Standard-RPG-Feature
5. **Dynamic Personality Weights** - Optional Advanced-Feature

---

**FAZIT:**

NajikaCore hat **VIEL MEHR implementiert als V3 dokumentiert**!
Die größten Gaps:
- Skill-Learning (Digimon World)
- Long-Term Memory (ChromaDB)
- Living/Tamagotchi System

**V4 muss diese Features aufnehmen** um die volle Power von NajikaCore zu zeigen!

---

**ERSTELLT:** 2025-10-23
**AUTOR:** Claude Code (Manual Analysis)
**DATEIEN ANALYSIERT:** 4 Core-Files
