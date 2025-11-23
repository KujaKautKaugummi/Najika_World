# UE5 Animation Specifications for Najika Digivice

**Project:** Najika Digivice UE5 Migration
**Target Platform:** Windows (Development) → Android (Xiaomi 11T Pro)
**Animation Style:** Anime/Stylized
**Date:** 2025-11-13

---

## Table of Contents

1. [Animation Overview](#animation-overview)
2. [Animation Blueprint](#animation-blueprint)
3. [Animation State Machines](#animation-state-machines)
4. [Animation Assets](#animation-assets)
5. [Animation Notifies](#animation-notifies)
6. [Blendspaces](#blendspaces)
7. [IK Systems](#ik-systems)
8. [Mobile Optimization](#mobile-optimization)

---

## Animation Overview

### Animation System Architecture

```
ANajikaCharacter
    └─ USkeletalMeshComponent (SK_Najika)
        └─ ABP_Najika (Animation Blueprint)
            ├─ ASM_Locomotion (State Machine)
            ├─ ASM_Combat (State Machine)
            ├─ ASM_Care (State Machine)
            └─ IK_Feet (Foot IK)
```

### Animation Count

**Total Animations:** 18 core animations + 12 combat animations = 30 total

**Animation Sources:**
- KayKit AnimatedCharacter Pack (base animations)
- Mixamo (combat animations)
- Custom animations (care actions - eat, drink, sleep)

---

## Animation Blueprint

### ABP_Najika

**Parent Class:** UAnimInstance

**Purpose:** Main animation blueprint for Najika character.

**Variables:**

#### Movement Variables
- **Speed** (Float) - Current movement speed (0-600)
- **Direction** (Float) - Movement direction (-180 to 180)
- **IsInAir** (Boolean) - Is character jumping/falling
- **IsCrouching** (Boolean) - Is character crouching

#### Combat Variables
- **IsInCombat** (Boolean) - Is in battle mode
- **AttackIndex** (Integer) - Current attack in combo (0-2)
- **IsBlocking** (Boolean) - Is blocking/parrying
- **IsDodging** (Boolean) - Is dodge rolling

#### Care Variables
- **IsEating** (Boolean) - Is playing eat animation
- **IsDrinking** (Boolean) - Is playing drink animation
- **IsSleeping** (Boolean) - Is playing sleep animation
- **IsTraining** (Boolean) - Is playing training animation

#### Emotional Variables
- **CurrentMood** (String) - Current mood (happy, sad, angry, etc.)
- **MoodIntensity** (Float, 0-100) - Intensity of current mood

**Event Graph:**

```cpp
// Update variables from Character
void UpdateAnimationProperties(float DeltaTime)
{
    ANajikaCharacter* Character = Cast<ANajikaCharacter>(TryGetPawnOwner());
    if (!Character) return;

    // Movement
    Speed = Character->GetVelocity().Size();
    Direction = CalculateDirection(Character->GetVelocity(), Character->GetActorRotation());
    IsInAir = Character->GetCharacterMovement()->IsFalling();

    // Combat
    IsInCombat = Character->bIsInCombat;
    IsDodging = Character->bIsDodgeRolling;

    // Care
    IsEating = Character->bIsEating;
    IsDrinking = Character->bIsDrinking;
    IsSleeping = Character->bIsSleeping;
}
```

---

## Animation State Machines

### ASM_Locomotion (Locomotion State Machine)

**Purpose:** Handles movement animations (idle, walk, run, jump).

**States:**

#### Idle
- **Animation:** A_Najika_Idle
- **Transitions:**
  - To Walk: Speed > 10
  - To Jump: IsInAir == True

#### Walk
- **Animation:** BS_Najika_Walk (Blendspace1D, 0-300 speed)
- **Transitions:**
  - To Idle: Speed <= 10
  - To Run: Speed > 300
  - To Jump: IsInAir == True

#### Run
- **Animation:** BS_Najika_Run (Blendspace1D, 300-600 speed)
- **Transitions:**
  - To Walk: Speed <= 300
  - To Jump: IsInAir == True

#### Jump
- **Animation:** A_Najika_Jump (Jump Start → Jump Loop → Jump Land)
- **Transitions:**
  - To Idle: IsInAir == False AND Speed <= 10
  - To Walk: IsInAir == False AND Speed > 10

**Transition Rules:**
- Blend Time: 0.2 seconds (smooth transitions)
- Interrupt: Allowed for Jump state

---

### ASM_Combat (Combat State Machine)

**Purpose:** Handles combat animations (attack, block, dodge).

**States:**

#### Combat_Idle
- **Animation:** A_Najika_CombatIdle (Combat stance)
- **Transitions:**
  - To Attack_1: AttackIndex == 1
  - To Block: IsBlocking == True
  - To Dodge: IsDodging == True

#### Attack_1
- **Animation:** A_Najika_Attack_1 (Light attack)
- **Duration:** 0.5 seconds
- **Transitions:**
  - To Attack_2: AttackIndex == 2 (during attack window)
  - To Combat_Idle: Animation finished

#### Attack_2
- **Animation:** A_Najika_Attack_2 (Medium attack)
- **Duration:** 0.6 seconds
- **Transitions:**
  - To Attack_3: AttackIndex == 3 (during attack window)
  - To Combat_Idle: Animation finished

#### Attack_3
- **Animation:** A_Najika_Attack_3 (Heavy attack, finisher)
- **Duration:** 0.8 seconds
- **Transitions:**
  - To Combat_Idle: Animation finished

#### Block
- **Animation:** A_Najika_Block (Block pose)
- **Transitions:**
  - To Combat_Idle: IsBlocking == False

#### Dodge
- **Animation:** A_Najika_Dodge (Dodge roll)
- **Duration:** 0.5 seconds
- **Transitions:**
  - To Combat_Idle: Animation finished

**Attack Combo System:**
- Attack window: 0.3 seconds after attack starts
- Reset combo if no input within 1 second
- AnimNotify triggers at damage frame (see Animation Notifies)

---

### ASM_Care (Care State Machine)

**Purpose:** Handles care-related animations (eat, drink, sleep, train).

**States:**

#### Care_Idle
- **Animation:** A_Najika_Idle
- **Transitions:**
  - To Eat: IsEating == True
  - To Drink: IsDrinking == True
  - To Sleep: IsSleeping == True
  - To Train: IsTraining == True

#### Eat
- **Animation:** A_Najika_Eat (Eating animation, 2 seconds)
- **Transitions:**
  - To Care_Idle: Animation finished

#### Drink
- **Animation:** A_Najika_Drink (Drinking animation, 1.5 seconds)
- **Transitions:**
  - To Care_Idle: Animation finished

#### Sleep
- **Animation:** A_Najika_Sleep_Loop (Looping sleep animation)
- **Transitions:**
  - To WakeUp: IsSleeping == False

#### WakeUp
- **Animation:** A_Najika_WakeUp (Wake up animation, 1 second)
- **Transitions:**
  - To Care_Idle: Animation finished

#### Train
- **Animation:** A_Najika_Train (Training animation, looping)
- **Transitions:**
  - To Care_Idle: IsTraining == False

---

## Animation Assets

### Core Animations (18 total)

**Locomotion (6):**
1. **A_Najika_Idle** - Idle standing animation (looping)
   - Duration: 2 seconds
   - Source: KayKit AnimatedCharacter
   - Notes: Breathing, slight sway

2. **A_Najika_Walk** - Walking animation (looping)
   - Duration: 1 second (cycle)
   - Source: KayKit AnimatedCharacter
   - Speed: 150 units/second

3. **A_Najika_Run** - Running animation (looping)
   - Duration: 0.8 seconds (cycle)
   - Source: KayKit AnimatedCharacter
   - Speed: 450 units/second

4. **A_Najika_Jump_Start** - Jump start (rising)
   - Duration: 0.2 seconds
   - Source: KayKit AnimatedCharacter

5. **A_Najika_Jump_Loop** - Jump loop (in air)
   - Duration: Looping
   - Source: KayKit AnimatedCharacter

6. **A_Najika_Jump_Land** - Jump land
   - Duration: 0.3 seconds
   - Source: KayKit AnimatedCharacter

**Care Actions (6):**
7. **A_Najika_Eat** - Eating animation
   - Duration: 2 seconds
   - Source: Custom (or Mixamo "Eating")
   - AnimNotify: FeedComplete (at 1.5s)

8. **A_Najika_Drink** - Drinking animation
   - Duration: 1.5 seconds
   - Source: Custom (or Mixamo "Drinking")
   - AnimNotify: DrinkComplete (at 1.0s)

9. **A_Najika_Sleep_Start** - Lie down animation
   - Duration: 1 second
   - Source: Custom

10. **A_Najika_Sleep_Loop** - Sleeping animation (looping)
    - Duration: 3 seconds (cycle)
    - Source: Custom
    - Notes: Breathing, slight movements

11. **A_Najika_WakeUp** - Wake up animation
    - Duration: 1.5 seconds
    - Source: Custom

12. **A_Najika_Train** - Training animation (looping)
    - Duration: 2 seconds (cycle)
    - Source: Mixamo "Punching" or custom
    - AnimNotify: TrainTick (every cycle)

**Social (6):**
13. **A_Najika_Sit** - Sitting animation
    - Duration: Looping
    - Source: KayKit AnimatedCharacter

14. **A_Najika_Wave** - Waving animation
    - Duration: 1.5 seconds
    - Source: Mixamo "Waving"

15. **A_Najika_Laugh** - Laughing animation
    - Duration: 2 seconds
    - Source: Custom (hand-animated)

16. **A_Najika_Cry** - Crying animation
    - Duration: 3 seconds
    - Source: Custom

17. **A_Najika_Dance** - Dancing animation (looping)
    - Duration: 4 seconds (cycle)
    - Source: Mixamo "Hip Hop Dancing"

18. **A_Najika_Think** - Thinking pose
    - Duration: 2 seconds
    - Source: Mixamo "Thinking"

---

### Combat Animations (12 total)

**Attacks (6):**
1. **A_Najika_Attack_1** - Light attack (left hand)
   - Duration: 0.5 seconds
   - Source: Mixamo "Punching"
   - AnimNotify: DealDamage (at 0.25s)

2. **A_Najika_Attack_2** - Light attack (right hand)
   - Duration: 0.5 seconds
   - Source: Mixamo "Punching"
   - AnimNotify: DealDamage (at 0.25s)

3. **A_Najika_Attack_3** - Heavy attack (both hands)
   - Duration: 0.8 seconds
   - Source: Mixamo "Heavy Attack"
   - AnimNotify: DealDamage (at 0.4s)

4. **A_Najika_Skill_Magic** - Magic attack animation
   - Duration: 1.2 seconds
   - Source: Mixamo "Spellcasting"
   - AnimNotify: SpawnProjectile (at 0.6s)

5. **A_Najika_Skill_AoE** - AoE skill animation
   - Duration: 1.5 seconds
   - Source: Mixamo "Ground Slam"
   - AnimNotify: TriggerAoE (at 1.0s)

6. **A_Najika_Ultimate** - Ultimate skill animation
   - Duration: 3 seconds
   - Source: Custom (epic pose + effects)
   - AnimNotify: UltimateStart (at 0.5s), UltimateDamage (at 2.0s)

**Defense (3):**
7. **A_Najika_Block** - Block pose
   - Duration: Looping (held)
   - Source: Mixamo "Blocking"

8. **A_Najika_Parry** - Parry animation
   - Duration: 0.4 seconds
   - Source: Mixamo "Parry"
   - AnimNotify: ParryWindow (at 0.1s-0.2s)

9. **A_Najika_Dodge** - Dodge roll
   - Duration: 0.5 seconds
   - Source: Mixamo "Roll"
   - AnimNotify: IFrameStart (at 0.0s), IFrameEnd (at 0.3s)

**Reactions (3):**
10. **A_Najika_Hit** - Hit reaction (light)
    - Duration: 0.3 seconds
    - Source: Mixamo "Hit Reaction"

11. **A_Najika_Stagger** - Stagger (heavy hit)
    - Duration: 0.6 seconds
    - Source: Mixamo "Stagger"

12. **A_Najika_Death** - Death animation
    - Duration: 2 seconds
    - Source: Mixamo "Death"

---

## Animation Notifies

### Purpose
Animation Notifies trigger gameplay events at specific frames during animations.

### Custom Notifies

#### AN_DealDamage
- **Used in:** Attack animations
- **Frame:** Damage frame (when weapon hits)
- **C++ Implementation:**
```cpp
void UAN_DealDamage::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
    ANajikaCharacter* Character = Cast<ANajikaCharacter>(MeshComp->GetOwner());
    if (Character)
    {
        Character->DealDamageToTarget();
    }
}
```

#### AN_FeedComplete
- **Used in:** A_Najika_Eat
- **Frame:** When food is consumed
- **Implementation:** Triggers backend API call (POST /api/najika/feed)

#### AN_DrinkComplete
- **Used in:** A_Najika_Drink
- **Frame:** When drink is consumed
- **Implementation:** Triggers backend API call (POST /api/najika/drink)

#### AN_TrainTick
- **Used in:** A_Najika_Train
- **Frame:** Every training cycle
- **Implementation:** Increments training progress, triggers backend sync

#### AN_Footstep
- **Used in:** Walk, Run animations
- **Frame:** When foot hits ground
- **Implementation:** Plays footstep sound, spawns dust particle

#### AN_IFrameStart / AN_IFrameEnd
- **Used in:** A_Najika_Dodge
- **Frame:** Start and end of invincibility frames
- **Implementation:** Sets Character->bIsInvincible flag

#### AN_ParryWindow
- **Used in:** A_Najika_Parry
- **Frame:** Parry active window
- **Implementation:** Sets Character->bCanParry flag

---

## Blendspaces

### BS_Najika_Walk (Blendspace1D)

**Axis:** Speed (0-300)

**Animations:**
- 0: A_Najika_Idle
- 150: A_Najika_Walk
- 300: Transition to Run

**Usage:** Smooth blending between idle and walk based on speed

---

### BS_Najika_Run (Blendspace1D)

**Axis:** Speed (300-600)

**Animations:**
- 300: A_Najika_Walk (fast)
- 450: A_Najika_Run (normal)
- 600: A_Najika_Run (fast variant, increased playback rate)

**Usage:** Smooth blending for run speed variations

---

### BS_Najika_Directional (Blendspace2D)

**Axis X:** Direction (-180 to 180)
**Axis Y:** Speed (0-600)

**Animations:**
- (0, 0): A_Najika_Idle
- (0, 300): A_Najika_Walk_Forward
- (90, 300): A_Najika_Walk_Right
- (-90, 300): A_Najika_Walk_Left
- (180, 300): A_Najika_Walk_Backward

**Usage:** 8-directional movement (optional, for complex movement)

---

## IK Systems

### Foot IK (IK_Feet)

**Purpose:** Adjust foot placement on uneven terrain.

**Implementation:**

1. **Two-Bone IK** nodes for left and right feet
2. **Trace downward** from foot to find ground
3. **Adjust foot offset** based on hit location
4. **Rotate foot** to match ground normal

**C++ Helper Functions:**
```cpp
// In ANajikaCharacter
FVector GetFootIKOffset(FName FootBoneName)
{
    FVector FootLocation = GetMesh()->GetSocketLocation(FootBoneName);
    FVector TraceStart = FootLocation + FVector(0, 0, 50);
    FVector TraceEnd = FootLocation - FVector(0, 0, 100);

    FHitResult Hit;
    if (GetWorld()->LineTraceSingleByChannel(Hit, TraceStart, TraceEnd, ECC_Visibility))
    {
        float Offset = (Hit.Location.Z - FootLocation.Z);
        return FVector(0, 0, Offset);
    }

    return FVector::ZeroVector;
}
```

**Bones:**
- LeftFoot
- RightFoot

**Settings:**
- IK Alpha: 1.0 (when grounded), 0.0 (when jumping)
- Max offset: 20 units

---

### Hand IK (Optional, for interactions)

**Purpose:** Align hands with interactive objects (doors, items).

**Implementation:**
- **Target:** IK target actor (spawned at interaction point)
- **Two-Bone IK** for left/right hand
- **Enabled only** during interaction animations

---

## Mobile Optimization

### Performance Guidelines

**Target:** 60 FPS on Xiaomi 11T Pro

**Animation LODs:**
- LOD 0 (Close): Full animation, all bones
- LOD 1 (Medium): Simplified animation, reduced bone updates
- LOD 2 (Far): Minimal animation (root motion only)

**Optimization Settings:**
- **Max LOD Level:** 2
- **Skeletal Mesh LOD Bias:** 0 (PC), 1 (Mobile)
- **Animation Update Rate:** Optimize (update less frequently when far)

**Animation Compression:**
- **Compression Scheme:** Automatic Compression
- **Translation Compression Format:** Float96NoW (precision)
- **Rotation Compression Format:** QuatFloat96NoW
- **Scale Compression Format:** None (if no scale keys)

**Bone Count Reduction:**
- Full skeleton: 60 bones (PC)
- Mobile skeleton: 40 bones (remove fingers, toes, extra facial bones)

**Disable on Mobile:**
- Cloth simulation
- Physics assets (except for ragdoll)
- Complex IK (foot IK optional, hand IK disabled)

---

## Implementation Checklist

### Phase 1: Animation Blueprint Setup
- [ ] Create ABP_Najika
- [ ] Set up Event Graph (UpdateAnimationProperties)
- [ ] Create animation variables

### Phase 2: State Machines
- [ ] Create ASM_Locomotion
  - [ ] Idle state
  - [ ] Walk state
  - [ ] Run state
  - [ ] Jump states
- [ ] Create ASM_Combat
  - [ ] Combat_Idle state
  - [ ] Attack states (1, 2, 3)
  - [ ] Block state
  - [ ] Dodge state
- [ ] Create ASM_Care
  - [ ] Eat state
  - [ ] Drink state
  - [ ] Sleep states
  - [ ] Train state

### Phase 3: Animation Import
- [ ] Import animations from KayKit
- [ ] Import animations from Mixamo
- [ ] Retarget animations to SK_Najika skeleton
- [ ] Create custom animations (sleep, eat, drink)

### Phase 4: Blendspaces
- [ ] Create BS_Najika_Walk
- [ ] Create BS_Najika_Run
- [ ] (Optional) Create BS_Najika_Directional

### Phase 5: Animation Notifies
- [ ] Create AN_DealDamage
- [ ] Create AN_FeedComplete
- [ ] Create AN_DrinkComplete
- [ ] Create AN_TrainTick
- [ ] Create AN_Footstep
- [ ] Create AN_IFrameStart/End
- [ ] Create AN_ParryWindow

### Phase 6: IK Systems
- [ ] Implement Foot IK (GetFootIKOffset function)
- [ ] Add Two-Bone IK nodes to ABP_Najika
- [ ] Test on uneven terrain

### Phase 7: Mobile Optimization
- [ ] Create animation LODs
- [ ] Compress animations
- [ ] Create mobile skeleton (reduced bones)
- [ ] Profile on Android

---

## Notes

- All animation assets use forward slash paths: `TEXT("AnimSequence'/Game/Animations/A_Najika_Idle.A_Najika_Idle'")`
- Animation Blueprint class: `TEXT("AnimBlueprint'/Game/Animations/ABP_Najika.ABP_Najika_C'")`
- Use Animation Montages for one-shot animations (attacks, skills)
- Consider using Animation Composite for complex sequences
- Root motion enabled for attacks, disabled for locomotion

---

**END OF ANIMATION_SPECS.md**
