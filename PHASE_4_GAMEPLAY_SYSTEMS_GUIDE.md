# PHASE 4: GAMEPLAY SYSTEMS - COMPLETE GUIDE
**Model 1 - Digivice APK**
**Datum:** 2025-11-11
**Phase:** 4 - Gameplay Systems (Woche 6-7)
**Dauer:** 2 Wochen

---

## 🎯 PHASE 4 ÜBERSICHT

### **Was wird gebaut:**
```
✅ Tamagotchi System (Digimon World-Style!)
✅ Battle System (Turn-based)
✅ Minigames (Rhythm, Reflex, Garden)
✅ Fishing System (Zelda OoT-Style)
✅ Scanner System (Optional)
```

---

## 💖 TODO 4.1: TAMAGOTCHI SYSTEM

### **Najika Needs System:**

Die Najika hat **5 Bedürfnisse** die über Zeit sinken (Digimon World!):

```
1. Hunger     🍖 (0-100) - Sinkt alle 30 Min um 10
2. Thirst     💧 (0-100) - Sinkt alle 20 Min um 10
3. Energy     ⚡ (0-100) - Sinkt alle 40 Min um 10
4. Hygiene    🚿 (0-100) - Sinkt alle 60 Min um 5
5. Happiness  😊 (0-100) - Sinkt alle 15 Min um 5
```

### **Care Actions:**

```
Feed:     POST /api/najika/feed     → +30 Hunger
Drink:    POST /api/najika/drink    → +30 Energy
Wash:     POST /api/najika/wash     → +50 Hygiene
Sleep:    POST /api/najika/sleep    → +50 Energy
Train:    POST /api/najika/train    → +10 Strength, -20 Energy
Praise:   POST /api/najika/praise   → +20 Happiness
Scold:    POST /api/najika/scold    → -10 Happiness, +5 Discipline
```

### **Implementation:**

#### **1. Create WBP_TamagotchiCare Widget:**

```
Canvas Panel
├── Image_Background (Dark overlay 80% opacity)
├── Image_Najika (Character Portrait - Large!)
│   Animation: Idle loop
│
├── Vertical Box (Status Bars)
│   ├── Horizontal Box (Hunger)
│   │   ├── Image_Icon_Hunger (🍖)
│   │   ├── ProgressBar_Hunger (Red → Yellow → Green)
│   │   └── Text_Hunger ("85/100")
│   │
│   ├── Horizontal Box (Energy)
│   │   ├── Image_Icon_Energy (⚡)
│   │   ├── ProgressBar_Energy (Yellow)
│   │   └── Text_Energy ("70/100")
│   │
│   ├── ... (Thirst, Hygiene, Happiness)
│
├── Grid Panel (Care Buttons 3x2)
│   ├── Button_Feed
│   │   ├── Image_Icon (🍖)
│   │   └── Text ("Feed")
│   │
│   ├── Button_Drink (💧 "Drink")
│   ├── Button_Wash (🚿 "Wash")
│   ├── Button_Sleep (😴 "Sleep")
│   ├── Button_Train (💪 "Train")
│   └── Button_Praise (👍 "Praise")
│
├── Border (Message Bubble)
│   └── Text_Message ("Thank you Mr.K! 💜")
│       Animation: Fade in/out
│
└── Button_Close (Top-right X)
```

#### **2. Widget Logic:**

```
Event Construct:
→ Get Game Instance
→ Cast to BP_NajikaGameInstance
→ Get APIClient
→ LoadNajikaStatus()

LoadNajikaStatus:
→ APIClient->GetNajikaStatus()
→ OnStatusReceived:
   * UpdateProgressBars(Hunger, Energy, Happiness)
   * CheckLowValues() → Show warnings

OnButton_Feed_Clicked:
→ APIClient->FeedNajika()
→ OnFeedResponse(Message):
   * ShowMessage(Message)
   * PlayAnimation("Eating")
   * SpawnParticle("Food_Hearts")
   * Wait 1s
   * LoadNajikaStatus() → Update bars

OnButton_Praise_Clicked:
→ APIClient->SendChatMessage("Good girl Najika!")
→ POST /api/najika/praise
→ OnPraiseResponse:
   * ShowMessage("Thank you! 💜")
   * PlayAnimation("Happy")
   * SpawnParticle("Love_Hearts")
   * Increase Happiness bar

CheckLowValues:
→ If Hunger < 30: Flash red, show warning icon
→ If Energy < 20: Play tired animation
→ If Happiness < 30: Play sad animation
→ If any < 10: Show CRITICAL notification
```

#### **3. Auto-Care System (Backend):**

Das Backend hat bereits ein Auto-Care System (najika_living_system.py):

```python
# Najika kümmert sich selbst wenn du zu lange weg bist!
if hunger < 20 and time_since_last_feed > 2_hours:
    hunger = min(100, hunger + 50)
    send_notification("Najika hat sich selbst gefüttert!")
```

Im UE5:
```
WebSocket Message Handler:
→ On Message Type "auto_care":
   * ShowNotification("Najika hat sich selbst versorgt!")
   * LoadNajikaStatus() → Update bars
```

---

## ⚔️ TODO 4.2: BATTLE SYSTEM

### **Battle Flow:**

```
1. Encounter Enemy (Random oder Fixed)
2. Transition to Battle Scene
3. Turn-based Combat:
   - Your Turn: Choose Action (Attack/Skill/Item/Run)
   - Enemy Turn: AI chooses action
   - Repeat until Win/Lose
4. Battle End:
   - Win: Rewards (XP, Items, Gold)
   - Lose: Game Over or Retry
5. Return to Exploration
```

### **Implementation:**

#### **1. Create Battle Manager:**

```
Blueprint: BP_BattleManager (Actor)

Variables:
- APIClient (from Game Instance)
- PlayerHP (Int)
- EnemyHP (Int)
- CurrentTurn (Enum: Player/Enemy)
- BattleActive (Boolean)
- AvailableSkills (Array of Skill Structs)
- BattleUI (WBP_BattleUI Reference)

Functions:
- StartBattle(EnemyID):
   → POST /api/battle/start {"enemy_id": EnemyID}
   → OnBattleStarted:
      * Store PlayerHP, EnemyHP
      * Load Skills from backend
      * Show BattleUI
      * Set CurrentTurn = Player
      * Enable UI buttons

- PerformAction(ActionType, TargetID, SkillID):
   → POST /api/battle/action {
        "action": ActionType,  // "attack", "skill", "item", "run"
        "target": TargetID,
        "skill_id": SkillID
     }
   → OnActionResponse:
      * Parse result (damage, effects)
      * Update HP bars
      * Play animations
      * Show damage numbers
      * Switch turn

- CheckBattleEnd:
   → If EnemyHP <= 0:
      * OnBattleWon(Rewards)
      * Show victory screen
      * Give rewards
   → If PlayerHP <= 0:
      * OnBattleLost()
      * Show defeat screen
      * Option to retry or return

- EndBattle:
   → POST /api/battle/end
   → Hide BattleUI
   → Return to exploration
```

#### **2. Create WBP_BattleUI:**

```
Canvas Panel
├── Overlay (Top)
│   ├── HorizontalBox
│   │   ├── WBP_HPBar_Player
│   │   │   ├── Text_Name ("Najika")
│   │   │   ├── ProgressBar_HP (Red)
│   │   │   └── Text_HP ("85/100")
│   │   │
│   │   └── WBP_HPBar_Enemy
│   │       ├── Text_Name ("Goblin")
│   │       ├── ProgressBar_HP (Red)
│   │       └── Text_HP ("50/80")
│
├── Text_TurnIndicator (Center-Top)
│   "Your Turn!" / "Enemy Turn!"
│   Animation: Pulse
│
├── Grid Panel (Skills) 2x2
│   ├── Button_Skill1 (Icon + Name + MP Cost)
│   ├── Button_Skill2
│   ├── Button_Skill3
│   └── Button_Skill4
│
├── HorizontalBox (Actions) Bottom
│   ├── Button_Attack (⚔️)
│   ├── Button_Defend (🛡️)
│   ├── Button_Items (🎒)
│   └── Button_Run (🏃)
│
└── ScrollBox (Battle Log) Bottom-Left
    "You attack Goblin for 25 damage!"
    "Goblin attacks you for 15 damage!"
```

#### **3. Battle Logic:**

```
OnButton_Attack_Clicked:
→ If CurrentTurn == Player:
   * BattleManager->PerformAction("attack", "enemy_001", null)
   * Disable UI buttons (prevent double-click)
   * Play attack animation
   * Wait for response

OnActionResponse(Result):
→ Parse JSON:
   {
     "ok": true,
     "damage": 25,
     "enemy_hp": 55,
     "player_hp": 85,
     "turn": "enemy"
   }
→ UpdateHPBars(PlayerHP, EnemyHP)
→ ShowDamageNumber(Damage, Position)
→ AddBattleLog("You dealt 25 damage!")
→ If turn == "enemy":
   * Wait 1.5s
   * Enemy performs action (automatic)
→ Else:
   * Enable UI buttons
```

### **Skills System:**

```
Skill Struct:
- ID (String)
- Name (String)
- Description (String)
- Type (Enum: Physical/Magical/Support)
- MPCost (Int)
- Damage (Int)
- Effects (Array of Effect Structs)
- Icon (Texture2D)

Load Skills:
→ GET /api/battle/skills
→ Response:
   {
     "skills": [
       {
         "id": "fireball",
         "name": "Fireball",
         "type": "magical",
         "mp_cost": 15,
         "damage": 40,
         "icon": "/static/icons/fireball.png"
       },
       ...
     ]
   }
→ Create Button for each skill
→ Display icon, name, MP cost
```

---

## 🎮 TODO 4.3: MINIGAMES

### **Minigame 1: Rhythm Game (Digimon World Cheering!)**

```
Gameplay:
- Notes fall from top to bottom
- Press button when note reaches hit zone
- Timing determines score (Perfect/Good/OK/Miss)
- Combo multiplier
- Song duration: 2-3 minutes

Implementation:
1. Create WBP_RhythmGame
2. Spawn Note widgets at beats
3. Move notes down (Lerp)
4. Detect input timing
5. Calculate score
6. Send score to backend: POST /api/minigame/rhythm
```

### **Minigame 2: Reflex Game**

```
Gameplay:
- Targets appear randomly on screen
- Tap target quickly
- Measure reaction time
- Speed increases over time
- High score tracking

Implementation:
1. Create WBP_ReflexGame
2. Spawn targets at random positions
3. On Click: Calculate reaction time
4. Increase spawn speed
5. Game Over after 3 misses
6. Submit score: POST /api/minigame/reflex
```

### **Minigame 3: Garden Game**

```
Gameplay:
- Plant seeds
- Water plants
- Wait for growth (real-time!)
- Harvest crops
- Sell for gold

Implementation:
1. Create BP_Garden (Level)
2. Create BP_Plant (Actor)
3. Plant has Growth stages (Seed → Sprout → Mature)
4. Water action: POST /api/garden/water
5. Growth simulated by backend
6. Harvest: POST /api/garden/harvest
```

---

## 🎣 TODO 4.4: FISHING SYSTEM (Zelda OoT!)

### **Fishing Mechanics:**

```
1. Equip Fishing Rod
2. Cast line (Hold button, release)
3. Wait for fish to bite
4. Button mashing minigame
5. Catch fish or it escapes
6. Caught fish → Inventory
```

### **Implementation:**

#### **1. Create BP_FishingRod:**

```
Components:
- Skeletal Mesh (Rod)
- Cable Component (Fishing Line)
- Sphere Collision (Bobber)

Variables:
- IsCasting (Boolean)
- CastPower (Float 0-1)
- FishOnLine (Boolean)
- CurrentFish (Fish Struct)

Functions:
- StartCharge:
   → Holding button
   → CastPower increases (0 → 1)
   → Play charge animation

- Cast:
   → Release button
   → Calculate cast distance (CastPower * MaxDistance)
   → Spawn Bobber at location
   → Start waiting for fish

- OnFishBite:
   → Random chance every 5s
   → Fish type depends on location
   → Play bite animation
   → Start button mash minigame

- CatchFish:
   → If button mashed fast enough
   → Add fish to inventory
   → POST /api/fishing/catch
   → Show caught fish UI

- FishEscaped:
   → If too slow
   → Fish swims away
   → Sad animation
```

#### **2. Button Mash Minigame:**

```
WBP_FishingMiniGame:
- ProgressBar (Tension)
- Text ("Mash E!")
- Timer countdown

Logic:
- Tension starts at 50%
- Press E → Tension -10%
- Every 0.5s → Tension +5%
- If Tension >= 100% → Fish escapes
- If Tension <= 0% → Fish caught!
```

### **Fish Database:**

```
Backend: /api/fishing/fish_types
[
  {
    "id": "common_carp",
    "name": "Common Carp",
    "rarity": "common",
    "value": 10,
    "icon": "/static/icons/carp.png"
  },
  {
    "id": "golden_koi",
    "name": "Golden Koi",
    "rarity": "legendary",
    "value": 500,
    "icon": "/static/icons/golden_koi.png"
  }
]
```

---

## 📷 TODO 4.5: SCANNER SYSTEM (Optional)

### **Scanner Feature:**

```
Funktion:
- Öffne Kamera (Android)
- Scanne reale Objekte
- AI erkennt Objekte (YOLO/TensorFlow)
- Najika kommentiert was sie sieht
- Manche Objekte geben Items!

Use Cases:
- Scanne Essen → Get virtual food item
- Scanne Blumen → Najika freut sich
- Scanne Tiere → Dex Entry
```

### **Implementation (Advanced!):**

```
1. Camera Permission (Android):
   - Add to AndroidManifest.xml
   - Request permission at runtime

2. Camera Capture:
   - Use Android Camera2 API (JNI)
   - Or: UE5 Camera Capture Component

3. Image Processing:
   - Send frame to backend: POST /api/scanner/detect
   - Backend runs YOLO model
   - Returns detected objects

4. Najika Response:
   - Based on detected object
   - "Oh, das ist eine Katze! 😊"
   - "Wow, Pizza! Gib mir auch! 🍕"

5. Reward System:
   - Certain objects give items
   - Track scanned objects (Dex)
```

**NOTE:** Scanner ist OPTIONAL für MVP! Kann in Phase 8 hinzugefügt werden.

---

## 📊 SUCCESS CRITERIA

**Phase 4 ist komplett wenn:**

```
✅ Tamagotchi System funktioniert
   - Needs sinken über Zeit
   - Feed/Drink/Wash funktionieren
   - UI updated real-time
   - Auto-Care System zeigt Notifications

✅ Battle System funktioniert
   - Turn-based combat works
   - Skills können verwendet werden
   - HP bars aktualisieren
   - Win/Lose conditions
   - Rewards werden gegeben

✅ Mindestens 2 Minigames funktionieren
   - Rhythm oder Reflex
   - Scores werden gespeichert
   - High Score tracking

✅ Fishing System funktioniert (optional aber cool!)
   - Rod equip
   - Cast mechanics
   - Button mash minigame
   - Fish inventory

✅ Integration mit Backend
   - Alle API calls funktionieren
   - State synchronisiert
   - Performance akzeptabel
```

---

## 🎉 PHASE 4 COMPLETE!

Wenn alle Success Criteria erfüllt sind, ist **Phase 4 abgeschlossen!**

**Nächster Schritt:** Phase 5 - UI/UX Polish

**Geschätzte Dauer Phase 4:** 2 Wochen
**Nach Abschluss:** Create Progress Report + Git Commit + Push

---

**Model 1 - Digivice APK Development**
**Phase:** 4/9 - Gameplay Systems
**Status:** Ready to Execute
**Timeline:** Week 6-7/12
