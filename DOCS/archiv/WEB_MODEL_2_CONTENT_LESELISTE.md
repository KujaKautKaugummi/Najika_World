# 📝 WEB MODEL 2 - GAME CONTENT CREATION
## LESELISTE & AUFGABEN (24h Sprint)

**Deine Rolle:** Game Content Designer (NPCs, Items, Quests, Dialogues)
**Ziel:** Fehlende Game Data erstellen - Najika World mit Leben füllen!

---

## 📚 PFLICHTLEKTÜRE (IN DIESER REIHENFOLGE!)

### 1️⃣ PROJEKT-ÜBERSICHT (START HIER!)
```
C:\Najika_World\NEU_WEB_MODEL_PROJEKT_KOMPLETT.md
```
**Warum:** Kompletter Projekt-Überblick, verstehe das Gesamtbild
**Dauer:** 20 min

### 2️⃣ NAJIKA PERSÖNLICHKEIT (SEHR WICHTIG!)
```
C:\Najika_World\alles wissen\zip\najika_personality_CORE.json
C:\Najika_World\alles wissen\zip\najika_personality_PUBLIC.json
```
**Warum:** Du schreibst Dialogues für Najika! 4 Persönlichkeiten kennen:
- Megumin (dramatisch, "EXPLOSION!")
- Harley Quinn (chaotisch, "Puddin'!")
- Shiro (analytisch, Wahrscheinlichkeiten)
- Melissa Masters (dominant, besitzergreifend)
**Dauer:** 20 min

### 3️⃣ WORLD DATA (SEHR WICHTIG!)
```
C:\Najika_World\digivice\data\regions.json
C:\Najika_World\digivice\data\cities.json
C:\Najika_World\digivice\data\biomes.json
```
**Warum:** 9 Regionen, 5 Städte - hier leben deine NPCs!
**Dauer:** 15 min

### 4️⃣ OREGON TRAIL × KONOSUBA EVENTS
```
C:\Najika_World\alles wissen\Najika finale\07_KONOSUBA_OREGON_EVENTS.md
```
**Warum:** 30 Event-Definitionen mit Najika-Reaktionen, Chaos-Mechanik
**Dauer:** 30 min (wichtig für Dialogue-Stil!)

### 5️⃣ COMBAT & SKILL SYSTEM
```
C:\Najika_World\alles wissen\Najika finale\05_COMBAT_SYSTEM.md
C:\Najika_World\alles wissen\Najika finale\08_1_SKILL_WEG_SYSTEM.md
```
**Warum:** Verstehe Combat (für Waffen/Items) und Skill-Weaving (für Spells)
**Dauer:** 25 min

### 6️⃣ GAME SYSTEMS OVERVIEW
```
C:\Najika_World\alles wissen\Najika finale\03_FEATURES_STATUS.md
C:\Najika_World\alles wissen\Najika finale\06_MASTER_ZUSAMMENFASSUNG.md
```
**Warum:** Welche Game-Systeme gibt es? (Slime, Arena, Cards, etc.)
**Dauer:** 20 min

---

## 🎯 DEINE AUFGABEN (24h Sprint)

### **STUNDE 0-4: NPCs ERSTELLEN (30+ Charaktere)**

**Aufgabe:** Für jede Stadt NPCs erstellen

#### **Handelsfestung (Heiße Dünen) - Western Hub:**
- 3 Händler (Waffen, Rüstung, Items)
- 2 Food Vendors (BBQ Ribs, Steak, Champion-Keule!)
- 1 Arena Master (PvP Arena)
- 2 Questgeber (Haupt + Side Quests)
- 1 Blacksmith (Weapon Upgrades)
- 1 Stable Master (Mounts/Slimes)

#### **Dampf-Hain (Samtmoos-Tiefwald) - Japanese Mystical:**
- 2 Onsen Attendants (Healing Buffs)
- 1 Restaurant Owner (Spirited Away Style, Baozi!)
- 3 Druids (Nature Magic Trainers)
- 2 Questgeber

#### **Salzige Bucht (Salzwind-Küste) - Pirate Coastal:**
- 1 Harbor Master (Ship Travel)
- 2 Fish Market Vendors (Salzfisch!)
- 1 Lighthouse Keeper (Secret Quest)
- 2 Pirate NPCs (Shady Traders)
- 2 Questgeber

#### **Runenheim (Blitzebene) - Magic Highland:**
- 3 Magic Trainers (Rune Magic, Lightning)
- 1 Rune Altar Keeper (Enchanting)
- 1 Totem Carver (Special Items)
- 2 Questgeber

#### **Funken-Siedlung (Magmaströme) - Volcanic Industrial:**
- 1 Master Blacksmith (Best Weapons/Armor)
- 3 Forge Workers (Crafting Materials)
- 1 Lava Boat Captain (Transportation)
- 2 Questgeber

#### **Special NPCs (Region-spezifisch):**
- Grünschlamm-Sumpf: 2 Witches (Alchemy, Hidden Location)
- Reich der Drei: 1 Ice Lich (Boss NPC, nicht friendly!)
- Tiefenhöhlen: 3 Goblin Traders (Underground Settlements)

**Format:**
```json
{
  "id": "npc_blacksmith_ragnar",
  "name": "Ragnar der Schmied",
  "title": "Meister-Schmied der Lava",
  "race": "Dwarf",
  "location": {
    "region": "magmastroeme",
    "city": "funken_siedlung",
    "position": {"x": 4800, "z": 8100}
  },
  "personality": "gruff_but_kind",
  "voice_style": "deep_raspy",
  "dialogue": {
    "greeting": "Hammer und Amboss! Was willst du?",
    "shop_intro": "Beste Waffen im ganzen Reich! Geschmiedet in echter Lava!",
    "quest_available": "Hm... vielleicht kannst du mir helfen.",
    "quest_complete": "Gut gemacht! Nimm das als Belohnung.",
    "goodbye": "Pass auf deine Klinge auf!"
  },
  "najika_reaction": {
    "first_meet": "EXPLOSION! Der riecht nach FEUER und STAHL! *kicher* Genau mein Typ!",
    "shop_visit": "Puddin', kauf mir die BESTE Waffe! Wahrscheinlichkeit dass ich sie brauche: 99,7%!",
    "quest_accept": "Ohhh, ein Auftrag vom Meister höchstpersönlich! DU gehörst mir bei diesem Quest!"
  },
  "shop_inventory": [
    "legendary_lava_sword",
    "volcanic_armor_set",
    "fire_resistance_potion"
  ],
  "services": ["weapon_upgrade", "armor_repair", "legendary_crafting"],
  "quests": ["quest_volcanic_ore", "quest_lava_beast_heart"]
}
```

**Output:** `npcs_database.json` (30+ NPCs)

---

### **STUNDE 4-8: ITEMS & LOOT (100+ Items)**

**Aufgabe:** Komplette Item-Datenbank erstellen

#### **Kategorien:**

**1. WAFFEN (30 Stück):**
- Schwerter (10): Common → Legendary
- Stäbe (10): Für Magic Classes
- Bögen (5): Range Weapons
- Dual-Wield (5): Linke/Rechte Hand

**Beispiel:**
```json
{
  "id": "weapon_lava_greatsword",
  "name": "Lavastrom-Großschwert",
  "type": "greatsword",
  "rarity": "legendary",
  "level_req": 15,
  "stats": {
    "damage": 120,
    "fire_damage": 50,
    "attack_speed": 0.8,
    "stamina_cost": 25
  },
  "special_ability": {
    "name": "Lava Eruption",
    "effect": "AOE Fire Damage",
    "cooldown": 30
  },
  "lore": "Geschmiedet in den Tiefen der Magmaströme von Meister Ragnar.",
  "najika_comment": "EXPLOSION! Diese Klinge... sie BRENNT wie meine Magie!"
}
```

**2. RÜSTUNG (25 Sets = 100 Teile):**
- Je Set: Helm, Chest, Legs, Boots
- Styles: Leather, Chainmail, Plate, Mage Robes

**3. CONSUMABLES (50 Stück):**
- HP Potions (Small, Medium, Large, Max)
- Mana Potions
- Food Buffs (BBQ Ribs, Champion-Keule, Baozi, Salzfisch)
- Temporary Buffs (Strength, Speed, Magic Power)

**4. CRAFTING MATERIALS (30 Stück):**
- Ores (Iron, Gold, Volcanic Ore)
- Herbs (Forest Moss, Lava Flower)
- Monster Drops (Scales, Claws, Horns)

**Output:** `items_database.json`

---

### **STUNDE 8-12: QUESTS (50+ Quests)**

**Aufgabe:** Quest-Datenbank mit Najika-Kommentaren

#### **Quest-Typen:**

**HAUPTSTORY (10-15 Quests):**
```json
{
  "id": "quest_main_001",
  "title": "Die Schwarze Windmühle erwacht",
  "type": "main_story",
  "chapter": 1,
  "level_req": 1,
  "giver": {
    "npc_id": "npc_elder_goetterfels",
    "location": "goetterfels"
  },
  "description": "Der Elder der Schwarzen Mühle bittet dich um Hilfe. Seltsame Energien erwachen im Berg.",
  "objectives": [
    {
      "type": "talk_to_npc",
      "target": "npc_elder_goetterfels",
      "description": "Sprich mit dem Elder"
    },
    {
      "type": "explore_location",
      "target": "schwarze_muehle_keller",
      "description": "Erkunde den Keller der Schwarzen Mühle"
    },
    {
      "type": "defeat_enemies",
      "target": "shadow_creatures",
      "count": 5,
      "description": "Besiege 5 Schattenkreaturen"
    }
  ],
  "najika_dialogue": {
    "quest_start": "EXPLOSION! Endlich ein ECHTES Abenteuer, Puddin'! Die Wahrscheinlichkeit dass wir sterben beträgt nur 34,7%! *kicher*",
    "objective_1_complete": "Gut zugehört! Jetzt lass uns den Keller erkunden!",
    "objective_2_complete": "WOAH! Schau dir diese Dunkelheit an! *dramatische Pose* Die Schwarze Windmühle zeigt ihre Zähne!",
    "objective_3_complete": "YESSS! Schattenkreaturen = AUSGELÖSCHT! Du gehörst mir, und DU bist STARK!",
    "quest_complete": "Das war erst der Anfang, Mr.K... Die Mühle hat Geheimnisse. Viele Geheimnisse."
  },
  "rewards": {
    "xp": 500,
    "gold": 100,
    "items": ["starter_sword", "hp_potion_medium"],
    "unlock": "schwarze_muehle_upper_floors"
  },
  "next_quest": "quest_main_002"
}
```

**SIDE QUESTS (30 Stück, je 3-5 pro Region):**
- Handelsfestung: Arena Challenges, Merchant Problems
- Dampf-Hain: Druid Rituals, Onsen Mystery
- Salzige Bucht: Pirate Treasure, Fishing Challenges
- etc.

**DAILY QUESTS (10 Stück, wiederholbar):**
- Kill X Enemies
- Gather X Materials
- Catch X Fish
- Complete X Dungeons

**Output:** `quests_database.json`

---

### **STUNDE 12-16: DIALOGUES & NAJIKA REACTIONS**

**Aufgabe:** Erweitere NPCs und Quests mit Dialogues

**Für jeden NPC:**
- Greeting (3 Varianten)
- Shop Talk (wenn Händler)
- Quest Talk (wenn Questgeber)
- Random Banter (5 Sätze)
- Goodbye (2 Varianten)

**Für jedes Quest:**
- Start Dialogue (Najika + NPC)
- Progress Comments (Najika)
- Completion Dialogue (Najika + NPC)

**Najika-Stil beachten:**
- Megumin: Dramatisch, "EXPLOSION!", "Die Schwarze Windmühle..."
- Harley: *kicher*, *giggle*, "Puddin'!", "Mr.K!"
- Shiro: "Wahrscheinlichkeit: X%", analytisch
- Melissa: "Du gehörst mir!", dominant

**Beispiel:**
```json
{
  "npc_id": "npc_fish_vendor_001",
  "dialogues": {
    "greeting": [
      "Frischer Fisch! Direkt vom Meer!",
      "Salziger als das Meer selbst!",
      "Willkommen an meinem Stand!"
    ],
    "najika_reactions": {
      "greeting": [
        "*schnüffel* FISCH! Wahrscheinlichkeit dass ich Hunger habe: 78%!",
        "Puddin', kauf mir Fisch! Ich will ALLES probieren! *kicher*",
        "Salzfisch... interessant. EXPLOSION-mäßig lecker!"
      ]
    }
  }
}
```

**Output:** Erweiterte `npcs_database.json` und `quests_database.json`

---

### **STUNDE 16-20: ENEMY STATS & LOOT TABLES**

**Aufgabe:** Für jede Region Enemies definieren

#### **Pro Region: 3-5 Common, 1-2 Elite, 1 Boss**

**Beispiel:**
```json
{
  "region": "magmastroeme",
  "enemies": {
    "common": [
      {
        "id": "enemy_lava_imp",
        "name": "Lava-Kobold",
        "level": 12,
        "stats": {
          "hp": 300,
          "damage": 25,
          "fire_resistance": 80,
          "water_weakness": 50
        },
        "behavior": "aggressive",
        "loot_table": {
          "gold": [5, 15],
          "items": [
            {"item_id": "volcanic_ore", "chance": 0.3},
            {"item_id": "fire_crystal", "chance": 0.1}
          ]
        },
        "najika_comment_on_kill": "Ha! Lava-Kobold? Mehr wie Lava-LOSER! *kicher*"
      }
    ],
    "elite": [
      {
        "id": "enemy_magma_golem",
        "name": "Magma-Golem",
        "level": 15,
        "stats": {
          "hp": 1500,
          "damage": 60
        },
        "loot_table": {
          "gold": [50, 100],
          "items": [
            {"item_id": "golem_core", "chance": 0.5},
            {"item_id": "legendary_lava_sword", "chance": 0.05}
          ]
        }
      }
    ],
    "boss": {
      "id": "boss_lava_titan",
      "name": "Lava-Titan",
      "level": 20,
      "stats": {
        "hp": 10000,
        "damage": 150
      },
      "special_abilities": [
        "lava_eruption",
        "molten_armor",
        "fire_breath"
      ],
      "loot_table": {
        "gold": [500, 1000],
        "guaranteed_items": ["titan_heart", "legendary_lava_greatsword"],
        "chance_items": [
          {"item_id": "volcanic_armor_set", "chance": 0.3}
        ]
      },
      "najika_dialogue": {
        "boss_encounter": "EXPLOSION! DAS ist ein BOSS! Mr.K, zeig ihm was WIR drauf haben!",
        "boss_50_percent": "Er wird schwächer! Wahrscheinlichkeit unseres Sieges: 67,3%!",
        "boss_defeated": "YESSS! DER LAVA-TITAN FÄLLT! *dramatische Pose* Die Schwarze Windmühle siegt immer!"
      }
    }
  }
}
```

**Output:** `enemies_database.json` (für alle 9 Regionen)

---

### **STUNDE 20-24: SPELL DEFINITIONS & REVIEW**

**Aufgabe:** 8 Magic Schools mit Spell-Weaving System

#### **Skill-Weaving (Final Fantasy Style):**

**Fire School:**
```json
{
  "school": "fire",
  "color": "#FF4500",
  "spells": [
    {
      "id": "spell_feuer",
      "name": "Feuer",
      "tier": 1,
      "mana_cost": 10,
      "damage": 30,
      "cast_time": 1.0,
      "description": "Grundlegender Feuerzauber",
      "najika_cast_phrase": "Feuer! *poof*"
    },
    {
      "id": "spell_feura",
      "name": "Feura",
      "tier": 2,
      "mana_cost": 25,
      "damage": 80,
      "cast_time": 1.5,
      "unlock_condition": "Cast Feuer 50 times",
      "najika_cast_phrase": "Feura! Jetzt wird's heiß, Puddin'!"
    },
    {
      "id": "spell_feuraga",
      "name": "Feuraga",
      "tier": 3,
      "mana_cost": 50,
      "damage": 200,
      "cast_time": 2.5,
      "unlock_condition": "Cast Feura 100 times",
      "najika_cast_phrase": "FEURAGA! EXPLOSION!!! *dramatische Pose*"
    }
  ]
}
```

**Alle 8 Schools:** Fire, Ice, Lightning, Earth, Water, Wind, Light, Dark

**Output:** `spells_database.json`

**PLUS: Final Review aller Dateien!**

---

## 📂 WICHTIGE DATEIEN ZUM NACHSCHLAGEN

**Wenn du nicht weiterkommst:**
- `C:\Najika_World\WEB_MODEL_COMPLETE_IMPLEMENTATION_TODO.md` (32KB Guide)
- `C:\Najika_World\backend\api\*.py` (Backend Code für System-Verständnis)
- `C:\Najika_World\alles wissen\Najika finale\NAJIKA_FEATURES_KOMPLETT.md`

---

## 🚨 WICHTIGE REGELN

1. **NICHTS ERFINDEN!** Basiere alles auf regions.json, cities.json, biomes.json
2. **Najika IMMER dabei!** Jedes Quest, jedes NPC-Meeting = Najika kommentiert
3. **4 Persönlichkeiten mischen!** Megumin (Basis) + Harley + Shiro + Melissa
4. **Fantasy-Western Vibe!** Handelsfestung = Wild West, Mix mit Anime/Japanese
5. **Deutsch!** Najika spricht Deutsch (deutsche Megumin-Stimme!)

---

## 💬 AUSTAUSCH MIT WEB MODEL 1

**Alle 4 Stunden kurzer Sync:**
- Welche NPCs/Items hast du erstellt?
- Braucht Web Model 1 spezielle Asset-Infos?
- Gibt es Blocker?

**Übergabe am Ende:**
- Alle JSON Databases → direkt nutzbar im Game
- Web Model 1 kann Asset-Mappings anpassen basierend auf deinen Items

---

## ✅ DELIVERABLES (Ende 24h)

1. ✅ `npcs_database.json` (30+ NPCs mit Dialogues)
2. ✅ `items_database.json` (100+ Items: Weapons, Armor, Consumables)
3. ✅ `quests_database.json` (50+ Quests: Main, Side, Daily)
4. ✅ `enemies_database.json` (Alle Regionen: Enemies + Loot Tables)
5. ✅ `spells_database.json` (8 Magic Schools mit Spell-Weaving)

**Alle Dateien als JSON, speichern in:**
```
C:\Najika_World\game_content\
```

---

## 🎮 VIEL ERFOLG!

Du hast 24h um Najika World mit Leben zu füllen!

**Bei Fragen:** Lies zuerst najika_personality_CORE.json und 07_KONOSUBA_OREGON_EVENTS.md für den richtigen Ton!

**Dein Motto:** "EXPLOSION! Lass uns Content machen, der Najika würdig ist!"

---

**Erstellt:** 2025-11-23
**Für:** Web Model 2 (Content Designer)
**Sprint Dauer:** 24 Stunden
