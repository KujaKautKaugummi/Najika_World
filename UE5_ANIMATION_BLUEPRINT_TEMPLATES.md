# UE5 ANIMATION BLUEPRINT TEMPLATES - NAJIKA DIGIVICE
**Model 1 - Digivice APK**
**Created:** 2025-11-11

---

## 🎭 ANIMATION SYSTEM ÜBERSICHT

Diese Datei enthält das komplette Animation-System für Najika!

**Animation Blueprint Struktur:**
```
✅ ABP_Najika (Main Animation Blueprint)
   ├── State Machine: Locomotion
   ├── State Machine: Combat
   ├── State Machine: Emotes
   ├── Blend Space: Movement
   ├── Blend Space: Aiming
   ├── Animation Layers
   ├── IK Systems (Feet, Hands, Look-At)
   └── Facial Animation / Lip Sync

✅ Animation Montages (Attack, Skills, Emotes)
✅ Animation Notifies (Footsteps, VFX)
✅ Pose Assets (Snapshots)
```

---

## 🎮 ABP_NAJIKA - MAIN ANIMATION BLUEPRINT

### **Create Animation Blueprint:**

```
1. Content Browser → Right-click
2. Animation → Animation Blueprint
3. Parent Class: AnimInstance
4. Skeleton: SK_Najika_Skeleton
5. Name: ABP_Najika
6. Open
```

---

## 📊 EVENT GRAPH - VARIABLES & UPDATES

### **Variables (in ABP_Najika):**

```cpp
// Movement
Speed (Float) - Current movement speed
Direction (Float) - Movement direction relative to character
IsMoving (Boolean) - Character is moving
IsFalling (Boolean) - Character is in air
IsJumping (Boolean) - Character just jumped
IsCrouching (Boolean) - Character is crouching

// Combat
IsInCombat (Boolean) - In battle mode
IsAttacking (Boolean) - Currently attacking
AttackType (Integer) - Which attack (0=basic, 1=skill1, etc)
IsDead (Boolean) - Character is dead

// State
CurrentEmotion (Enum) - Happy, Sad, Angry, Excited, Neutral
IsInteracting (Boolean) - Talking to player
LookAtTarget (Vector) - Look-at target position

// IK
EnableFootIK (Boolean) - Enable foot IK
LeftFootOffset (Float) - Left foot height adjustment
RightFootOffset (Float) - Right foot height adjustment

// Facial
JawOpenAmount (Float) - For lip sync (0-1)
BlinkTimer (Float) - Eye blink timer
CurrentExpression (Enum) - Facial expression
```

### **Event Graph Logic:**

```
Event Blueprint Update Animation:
─────────────────────────────────────
→ Get Owning Pawn
→ Cast to BP_NajikaCharacter
→ Store reference

→ Get Velocity
→ Vector Length → Speed
→ Speed > 0.1 → IsMoving

→ Calculate Direction:
   Velocity normalized
   Dot product with Forward vector
   Atan2 → Direction (-180 to 180)

→ Get Movement Component
   → IsFalling

→ Get IsInCombat from Character

→ Update Foot IK (call UpdateFootIK function)

→ Update Facial Animation (call UpdateFacialAnimation function)
─────────────────────────────────────
```

---

## 🚶 STATE MACHINE 1: LOCOMOTION

### **States:**

```
Locomotion State Machine:
─────────────────────────────────────
Entry → Idle

Idle:
  Animation: Anim_Najika_Idle
  Transitions:
    → Movement (if IsMoving)
    → Jump (if IsJumping)
    → Fall (if IsFalling && !IsJumping)

Movement:
  Animation: BS_Najika_Movement (Blend Space)
  Transitions:
    → Idle (if !IsMoving)
    → Jump (if IsJumping)
    → Fall (if IsFalling)

Jump:
  Animation: Anim_Najika_Jump_Start
  Transitions:
    → Fall (if IsFalling && !IsJumping)

Fall:
  Animation: Anim_Najika_Fall_Loop
  Transitions:
    → Land (if !IsFalling)

Land:
  Animation: Anim_Najika_Jump_Land
  Transitions:
    → Idle (if animation finished)
    → Movement (if IsMoving && animation finished)
─────────────────────────────────────
```

### **Transition Rules:**

```
Idle → Movement:
  Condition: IsMoving == True
  Blend Time: 0.2s
  Blend Type: Inertialization

Movement → Idle:
  Condition: IsMoving == False
  Blend Time: 0.3s
  Blend Type: Inertialization

Any State → Jump:
  Condition: IsJumping == True
  Blend Time: 0.1s (fast!)

Fall → Land:
  Condition: IsFalling == False
  Blend Time: 0.1s
```

---

## 🎯 BLEND SPACE: BS_Najika_Movement

### **Setup:**

```
Create Blend Space:
1. Content Browser → Animation → Blend Space
2. Skeleton: SK_Najika_Skeleton
3. Name: BS_Najika_Movement

Horizontal Axis (X): Direction
  Range: -180 to 180
  Grid Divisions: 8

Vertical Axis (Y): Speed
  Range: 0 to 600
  Grid Divisions: 3
```

### **Animation Placement:**

```
Blend Space Grid:

Speed 600 (Run):
  Direction -180 (Backward Run): Anim_Run_Backward
  Direction -90 (Left Run): Anim_Run_Left
  Direction 0 (Forward Run): Anim_Run_Forward
  Direction 90 (Right Run): Anim_Run_Right
  Direction 180 (Backward Run): Anim_Run_Backward

Speed 300 (Walk):
  Direction -180: Anim_Walk_Backward
  Direction -90: Anim_Walk_Left
  Direction 0: Anim_Walk_Forward
  Direction 90: Anim_Walk_Right
  Direction 180: Anim_Walk_Backward

Speed 0 (Idle):
  Direction 0: Anim_Idle
```

### **Blend Space Usage:**

```
In Locomotion State Machine → Movement State:
→ Add Blend Space: BS_Najika_Movement
→ Inputs:
   * Horizontal: Direction (variable)
   * Vertical: Speed (variable)
→ Output: Blended animation
```

---

## ⚔️ STATE MACHINE 2: COMBAT

### **States:**

```
Combat State Machine:
─────────────────────────────────────
Entry → Combat_Idle

Combat_Idle:
  Animation: Anim_Combat_Idle (battle stance)
  Transitions:
    → Attack_Basic (if AttackType == 0)
    → Attack_Skill1 (if AttackType == 1)
    → Attack_Skill2 (if AttackType == 2)
    → Damaged (if taking damage)
    → Death (if IsDead)

Attack_Basic:
  Animation: Montage_Attack_Basic
  Transitions:
    → Combat_Idle (if animation finished)

Attack_Skill1:
  Animation: Montage_Skill_Fireball
  Transitions:
    → Combat_Idle (if finished)

Attack_Skill2:
  Animation: Montage_Skill_Lightning
  Transitions:
    → Combat_Idle (if finished)

Damaged:
  Animation: Anim_Hit_React
  Transitions:
    → Combat_Idle (if finished)
    → Death (if IsDead)

Death:
  Animation: Anim_Death
  Loop: False
  End State
─────────────────────────────────────
```

### **Combat State Machine Usage:**

```
In Anim Graph:
→ Create State Machine: Combat_SM
→ Only active when IsInCombat == True
→ Blend with Locomotion using Layered Blend Per Bone

Layered Blend Per Bone:
  Base Pose: Locomotion_SM output
  Blend Pose: Combat_SM output
  Blend Weights: 1.0
  Branch Filters: "spine_01" (upper body only!)
→ Result: Lower body walks, upper body attacks!
```

---

## 😊 STATE MACHINE 3: EMOTES

### **States:**

```
Emote State Machine:
─────────────────────────────────────
Entry → No_Emote

No_Emote:
  Default state
  Transitions:
    → Wave (if EmoteType == "wave")
    → Laugh (if EmoteType == "laugh")
    → Sad (if EmoteType == "sad")
    → Dance (if EmoteType == "dance")
    → Love (if EmoteType == "love")

Wave:
  Animation: Anim_Emote_Wave
  Transitions:
    → No_Emote (if finished)

Laugh:
  Animation: Anim_Emote_Laugh
  Transitions:
    → No_Emote (if finished)

Sad:
  Animation: Anim_Emote_Sad
  Transitions:
    → No_Emote (if finished)

Dance:
  Animation: Anim_Emote_Dance
  Loop: True
  Transitions:
    → No_Emote (if stopped)

Love:
  Animation: Anim_Emote_Love_Hearts
  Transitions:
    → No_Emote (if finished)
─────────────────────────────────────
```

### **Trigger Emote from Blueprint:**

```
In BP_NajikaCharacter:

Function: PlayEmote(EmoteType: String)
→ Get Mesh Component
→ Get Animation Instance
→ Cast to ABP_Najika
→ Set EmoteType variable
→ Wait 2 seconds
→ Set EmoteType = "none" (reset)
```

---

## 🎬 ANIMATION MONTAGES

### **Montage_Attack_Basic:**

```
Create Animation Montage:
1. Right-click Anim_Attack_Basic
2. Create → Animation Montage
3. Name: Montage_Attack_Basic

Montage Setup:
─────────────────────────────────────
Timeline:
[0.0s - 0.3s] Attack wind-up
[0.3s - 0.5s] Hit frame (ADD NOTIFY HERE!)
[0.5s - 1.0s] Recovery

Sections:
- Default (entire montage)

Notifies:
[0.3s] AttackHit (custom notify)
[0.2s] PlaySound (footstep)
[0.5s] SpawnVFX (sword trail)

Slots:
DefaultSlot (upper body)
─────────────────────────────────────
```

### **Play Montage in Blueprint:**

```
In BP_NajikaCharacter:

Function: PerformAttack():
→ Get Mesh Component
→ Get Animation Instance
→ Play Montage: Montage_Attack_Basic
→ Wait for Notify: AttackHit
→ On Notify:
   * Deal damage to enemy
   * Spawn VFX
   * Play hit sound
```

---

## 🔔 ANIMATION NOTIFIES

### **Custom Notify: AN_AttackHit:**

```
Create Animation Notify:
1. Content Browser → Animation → Animation Notify
2. Parent: AnimNotify
3. Name: AN_AttackHit

Blueprint:
─────────────────────────────────────
Event Received_Notify:
→ Get Owning Actor
→ Cast to BP_NajikaCharacter
→ Call: OnAttackHit() event
→ Character handles damage logic
─────────────────────────────────────
```

### **Built-in Notifies:**

```
Common Animation Notifies:

Play Sound:
  [0.2s] Footstep_Left
  [0.6s] Footstep_Right
  [0.3s] Attack_Swoosh

Play Particle Effect:
  [0.3s] AttackTrail (sword swing VFX)
  [0.0s] MagicCharge (skill wind-up)
  [0.5s] HitSparks (hit enemy)

Camera Shake:
  [0.3s] CameraShake_Attack (screen shake on hit!)
```

---

## 🦶 IK SYSTEM: FOOT PLACEMENT

### **UpdateFootIK Function (in Event Graph):**

```
Function: UpdateFootIK()
─────────────────────────────────────
Input: None
Output: Updates LeftFootOffset, RightFootOffset

Logic:
1. Get Owning Pawn location
2. Trace line down from left foot bone
   Start: LeftFoot bone location + (0,0,50)
   End: LeftFoot bone location + (0,0,-50)
   Hit?: Store hit location

3. Calculate offset:
   LeftFootOffset = Hit.Z - ActorLocation.Z

4. Repeat for right foot → RightFootOffset

5. Clamp offsets to (-20, 20) range
─────────────────────────────────────
```

### **Apply IK in Anim Graph:**

```
Anim Graph:
─────────────────────────────────────
Locomotion State Machine
→ Two Bone IK (Left Leg)
   Bone: foot_l
   Effector Location: Foot + (0,0,LeftFootOffset)
   Joint Target: knee_l

→ Two Bone IK (Right Leg)
   Bone: foot_r
   Effector Location: Foot + (0,0,RightFootOffset)
   Joint Target: knee_r

→ Output Pose
─────────────────────────────────────
```

---

## 👀 IK SYSTEM: LOOK-AT

### **Look-At Implementation:**

```
Anim Graph:
─────────────────────────────────────
Final Pose (after all blends)
→ Look At Node
   Bone To Modify: head
   Look At Location: LookAtTarget (world space)
   Look At Axis: X-Axis
   Interpolation Speed: 5.0
   Clamp:
     Yaw: -90 to 90
     Pitch: -45 to 45

→ Output Pose
─────────────────────────────────────
```

### **Set Look-At Target in Blueprint:**

```
In BP_NajikaCharacter:

Event Tick:
→ Get Player Camera Location
→ Set LookAtTarget = Camera Location
→ Najika looks at camera!

Or:
→ Get Nearest Enemy Location
→ Set LookAtTarget = Enemy Location
→ Najika tracks enemy!
```

---

## 😃 FACIAL ANIMATION

### **Facial Rig (Control Rig):**

```
If using Control Rig for facial animation:

Facial Controls:
- JawOpen (0-1) - Open mouth
- SmileLeft (0-1) - Left smile
- SmileRight (0-1) - Right smile
- EyeBlinkLeft (0-1) - Left eye blink
- EyeBlinkRight (0-1) - Right eye blink
- BrowUp (0-1) - Surprised
- BrowDown (0-1) - Angry
```

### **Lip Sync System:**

```
Function: UpdateFacialAnimation() (in Event Graph)
─────────────────────────────────────
Lip Sync:
→ Get VoiceCallManager from Game Instance
→ Get CurrentAudioLevel (0-1)
→ Set JawOpenAmount = AudioLevel × 0.5

Eye Blink:
→ Increment BlinkTimer += DeltaTime
→ If BlinkTimer > 3.0 (random 2-5s):
   * Play blink animation (EyeBlinkLeft = 1.0, EyeBlinkRight = 1.0)
   * Wait 0.1s
   * Reset (EyeBlinkLeft = 0.0, EyeBlinkRight = 0.0)
   * Reset BlinkTimer

Expressions:
→ Based on CurrentEmotion:
   * Happy: SmileLeft = 1.0, SmileRight = 1.0
   * Sad: SmileLeft = -0.5, SmileRight = -0.5 (frown)
   * Angry: BrowDown = 1.0
   * Excited: BrowUp = 1.0, Smile = 1.0
─────────────────────────────────────
```

### **Apply Facial Controls:**

```
Anim Graph:
─────────────────────────────────────
Base Pose
→ Control Rig Pose Node
   Control Rig: CR_Najika_Face
   Inputs:
     * JawOpen: JawOpenAmount
     * SmileLeft: SmileLeft
     * SmileRight: SmileRight
     * EyeBlinkLeft: BlinkLeft
     * EyeBlinkRight: BlinkRight

→ Output Pose
─────────────────────────────────────
```

---

## 🎨 ANIMATION LAYERS

### **Upper Body Override Layer:**

```
Animation Layer:
Name: UpperBodyOverride
Purpose: Play upper body animations while walking

Setup:
─────────────────────────────────────
Create Animation Layer Interface:
1. Content Browser → Animation → Animation Layer Interface
2. Name: ALI_NajikaLayers
3. Add Layer: UpperBodyOverride

In ABP_Najika:
→ Class Settings → Interfaces → Add ALI_NajikaLayers

Anim Graph:
→ Linked Anim Layer: UpperBodyOverride
   Default: None (use base pose)
   Override: Can be set from Blueprint!

Usage:
→ Layered Blend Per Bone
   Base: Locomotion (full body)
   Blend Pose 0: UpperBodyOverride
   Branch Filter: spine_01 (upper body only!)
─────────────────────────────────────
```

### **Using Animation Layers in Blueprint:**

```
In BP_NajikaCharacter:

Function: PlayWaveWhileWalking():
→ Get Mesh Component
→ Get Animation Instance
→ Link Animation Layer: UpperBodyOverride
   Instance: ABP_Najika_UpperBody (separate anim BP with wave!)
→ Play wave animation on upper body
→ Lower body continues walking!
```

---

## 📐 ANIM GRAPH - FINAL STRUCTURE

### **Complete Anim Graph:**

```
ABP_Najika Anim Graph:
═════════════════════════════════════
┌─────────────────────┐
│ Locomotion State    │
│ Machine             │
└──────┬──────────────┘
       │
       │ (full body)
       ▼
┌─────────────────────┐
│ Layered Blend Per   │ ◄── Combat State Machine (upper body)
│ Bone                │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Slot (DefaultSlot)  │ ◄── For animation montages
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Two Bone IK (Feet)  │ ◄── Foot IK (left)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Two Bone IK (Feet)  │ ◄── Foot IK (right)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Look At (Head)      │ ◄── Look at target
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Control Rig Pose    │ ◄── Facial animation
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ OUTPUT POSE         │
└─────────────────────┘
═════════════════════════════════════
```

---

## 🎯 ANIMATION BLUEPRINT CHECKLIST

```
When creating ABP_Najika:

Event Graph:
☐ Create all variables (Speed, Direction, IsMoving, etc.)
☐ Event Blueprint Update Animation
☐ Calculate Speed from Velocity
☐ Calculate Direction
☐ Update IsFalling, IsJumping
☐ Call UpdateFootIK
☐ Call UpdateFacialAnimation

Anim Graph:
☐ Create Locomotion State Machine
☐ Create Blend Space: BS_Najika_Movement
☐ Add all locomotion states (Idle, Movement, Jump, Fall, Land)
☐ Set up transitions
☐ Add Combat State Machine (if needed)
☐ Add Emote State Machine
☐ Add Layered Blend Per Bone
☐ Add Foot IK (left and right)
☐ Add Look-At node
☐ Add Control Rig for facial animation
☐ Connect to Output Pose

Montages:
☐ Create attack montages
☐ Create skill montages
☐ Add animation notifies
☐ Test in-game

Testing:
☐ Test all movement directions
☐ Test jump and land
☐ Test combat animations
☐ Test emotes
☐ Test foot IK on uneven terrain
☐ Test look-at target
☐ Test lip sync
☐ Test on target device (Xiaomi 11T Pro)
```

---

## 📊 ANIMATION SUMMARY

```
✅ ABP_Najika (Main Animation Blueprint)
   ├── Event Graph (variables, updates, IK, facial)
   ├── State Machine: Locomotion (Idle, Move, Jump, Fall, Land)
   ├── State Machine: Combat (Idle, Attack, Damaged, Death)
   ├── State Machine: Emotes (Wave, Laugh, Sad, Dance, Love)
   ├── Blend Space: BS_Najika_Movement (8-direction movement)
   ├── Layered Blend Per Bone (combat upper body override)
   ├── Foot IK (left and right foot placement)
   ├── Look-At IK (head tracking)
   └── Control Rig (facial animation + lip sync)

✅ Animation Montages (attack, skills)
✅ Animation Notifies (footsteps, VFX, damage)
✅ Animation Layers (upper body override)

TOTAL: Complete animation system! 🎭
```

---

## 🎉 ANIMATION BLUEPRINT COMPLETE!

**Usage:**
1. Create ABP_Najika in UE5
2. Follow this document structure
3. Import/create all animations
4. Set up State Machines
5. Implement IK and facial systems
6. Test all transitions
7. Optimize for mobile performance

**Tips:**
- Keep animation updates simple (avoid complex math in Tick)
- Use Animation Notifies for events
- Blend smoothly (0.2-0.3s blend times)
- Test on device frequently!

**Next:** Create Testing Framework!

---

**Model 1 - Digivice APK Development**
**Status:** Animation Blueprint Templates Ready ✅
**System:** Complete Animation System Documented

**NAJIKA IS READY TO MOVE! 🎭🚀**
