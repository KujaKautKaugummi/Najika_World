# Three.js → Unreal Engine 5 Mapping Guide
**Najika World - 3D System Migration**

---

## 📋 Inhaltsverzeichnis

1. [Scene Setup](#scene-setup)
2. [Camera System](#camera-system)
3. [Lighting](#lighting)
4. [Geometrie & Meshes](#geometrie--meshes)
5. [Materials & Textures](#materials--textures)
6. [Character Controller](#character-controller)
7. [Combat System](#combat-system)
8. [Physics & Collision](#physics--collision)
9. [Animation System](#animation-system)
10. [Asset Loading](#asset-loading)

---

## SCENE SETUP

### Three.js
```javascript
scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);
scene.fog = new THREE.Fog(0x1a1a2e, 12, 160);
```

### UE5 Blueprint
```
Level Blueprint:
├─ Create Level (World)
├─ Set Background Color: RGB(26, 26, 46)
└─ Add Exponential Height Fog:
    ├─ Fog Density: 0.02
    ├─ Fog Start Distance: 1200 cm (12m)
    └─ Fog Max Distance: 16000 cm (160m)
```

### UE5 C++
```cpp
// In Level Constructor or BeginPlay
AExponentialHeightFog* Fog = GetWorld()->SpawnActor<AExponentialHeightFog>();
if (Fog) {
    Fog->GetComponent()->FogDensity = 0.02f;
    Fog->GetComponent()->StartDistance = 1200.0f;
    Fog->GetComponent()->FogMaxOpacity = 1.0f;
}
```

---

## CAMERA SYSTEM

### Three.js
```javascript
camera = new THREE.PerspectiveCamera(
    60,  // FOV
    aspectRatio,
    0.1,  // Near
    1000  // Far
);
camera.position.set(0, 12, 28);
```

### UE5 Blueprint
```
Camera Component:
├─ Field of View: 60°
├─ Near Clip Plane: 10 cm (0.1m)
├─ Far Clip Plane: 100000 cm (1000m)
└─ Location: X=0, Y=2800, Z=1200
   (Note: UE5 Z = Three.js Y, Y = Three.js Z)
```

### UE5 C++
```cpp
// In Character or Pawn
UCameraComponent* Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
Camera->SetupAttachment(RootComponent);
Camera->FieldOfView = 60.0f;
Camera->SetRelativeLocation(FVector(0.0f, 2800.0f, 1200.0f));
```

### Camera Modes Mapping

| Three.js | UE5 Equivalent | Implementation |
|----------|----------------|----------------|
| **ORBIT** | Spring Arm + Camera | Use `USpringArmComponent` with auto-rotation |
| **THIRD** | Third Person Camera | Spring Arm with fixed offset, no auto-rotate |
| **FIRST** | First Person Camera | Camera directly on character head socket |

---

## LIGHTING

### Three.js
```javascript
// Ambient Light
ambientLight = new THREE.AmbientLight(0xffffff, 0.45);
scene.add(ambientLight);

// Directional Light (Sun)
dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
dirLight.position.set(8, 18, 5);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
scene.add(dirLight);

// Point Lights
pointLight1 = new THREE.PointLight(0xff6b6b, 1.2, 50);
pointLight1.position.set(-10, 5, -10);
scene.add(pointLight1);
```

### UE5 Blueprint
```
Lighting Setup:
├─ Skylight (Ambient):
│   ├─ Intensity: 0.45
│   ├─ Color: RGB(255, 255, 255)
│   └─ Source Type: Captured Scene
│
├─ Directional Light (Sun):
│   ├─ Intensity: 0.9
│   ├─ Location: X=800, Y=500, Z=1800
│   ├─ Rotation: Point towards (0,0,0)
│   ├─ Cast Shadows: TRUE
│   └─ Dynamic Shadow Distance: 20000 cm
│
└─ Point Light 1:
    ├─ Intensity: 1.2
    ├─ Attenuation Radius: 5000 cm (50m)
    ├─ Location: X=-1000, Y=-1000, Z=500
    └─ Color: RGB(255, 107, 107)
```

### UE5 C++
```cpp
// Directional Light (Sun)
ADirectionalLight* Sun = GetWorld()->SpawnActor<ADirectionalLight>();
Sun->SetActorLocation(FVector(800.0f, 500.0f, 1800.0f));
Sun->SetLightColor(FLinearColor::White);
Sun->SetIntensity(0.9f);
Sun->SetCastShadows(true);

// Point Light
APointLight* PointLight = GetWorld()->SpawnActor<APointLight>();
PointLight->SetActorLocation(FVector(-1000.0f, -1000.0f, 500.0f));
PointLight->SetLightColor(FLinearColor(1.0f, 0.42f, 0.42f)); // 0xff6b6b
PointLight->SetIntensity(1.2f);
PointLight->SetAttenuationRadius(5000.0f);
```

---

## GEOMETRIE & MESHES

### Three.js
```javascript
// Simple Box
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0xff6b6b });
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// Group (for complex objects)
const group = new THREE.Group();
group.add(mesh1);
group.add(mesh2);
scene.add(group);
```

### UE5 Blueprint
```
Actor Blueprint:
├─ Add Component: Static Mesh
├─ Set Static Mesh: Cube (Engine Content)
├─ Set Material: M_Basic_Red
└─ Set Scale: X=100, Y=100, Z=100
   (UE5 default scale = 100cm = 1m)
```

### UE5 C++
```cpp
// Static Mesh Component
UStaticMeshComponent* MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
MeshComp->SetupAttachment(RootComponent);

// Load Mesh Asset
static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshAsset(
    TEXT("/Engine/BasicShapes/Cube")
);
if (MeshAsset.Succeeded()) {
    MeshComp->SetStaticMesh(MeshAsset.Object);
}

// Set Scale (Three.js 1 = UE5 100)
MeshComp->SetRelativeScale3D(FVector(1.0f, 1.0f, 1.0f));
```

### Wichtig: Koordinaten-Transformation

| Three.js | UE5 | Faktor |
|----------|-----|--------|
| X | X | 100 cm |
| Y | Z | 100 cm |
| Z | Y | 100 cm |

**Formel:**
```cpp
FVector UE5Position = FVector(
    ThreeJS_X * 100.0f,
    ThreeJS_Z * 100.0f,
    ThreeJS_Y * 100.0f
);
```

---

## MATERIALS & TEXTURES

### Three.js
```javascript
const material = new THREE.MeshStandardMaterial({
    color: 0xff6b6b,
    metalness: 0.2,
    roughness: 0.8,
    transparent: false,
    opacity: 1.0
});
```

### UE5 Material Editor
```
Material Blueprint:
├─ Base Color: RGB(255, 107, 107)
├─ Metallic: 0.2
├─ Roughness: 0.8
├─ Opacity: 1.0
└─ Blend Mode: Opaque
```

### UE5 C++ (Dynamic Material)
```cpp
UMaterialInstanceDynamic* DynMaterial = UMaterialInstanceDynamic::Create(
    BaseMaterial, this
);

// Set Parameters
DynMaterial->SetVectorParameterValue(
    FName("BaseColor"),
    FLinearColor(1.0f, 0.42f, 0.42f) // 0xff6b6b
);
DynMaterial->SetScalarParameterValue(FName("Metallic"), 0.2f);
DynMaterial->SetScalarParameterValue(FName("Roughness"), 0.8f);

// Apply to Mesh
MeshComponent->SetMaterial(0, DynMaterial);
```

---

## CHARACTER CONTROLLER

### Three.js
```javascript
const CHARACTER_SPEED = 7.5;
const CHARACTER_HEIGHT = 3.8;

// Movement (in animate loop)
if (activeKeys.has('w')) {
    const forward = new THREE.Vector3();
    camera.getWorldDirection(forward);
    forward.y = 0;
    forward.normalize();
    characterGroup.position.addScaledVector(forward, CHARACTER_SPEED * deltaTime);
}
```

### UE5 Blueprint (Character Movement Component)
```
Character Blueprint:
├─ Character Movement Component:
│   ├─ Max Walk Speed: 750 cm/s (7.5 m/s)
│   ├─ Capsule Height: 380 cm (3.8m)
│   ├─ Capsule Radius: 42 cm
│   └─ Gravity Scale: 1.0
│
└─ Input:
    ├─ W: Add Movement Input (Forward)
    ├─ S: Add Movement Input (Backward)
    ├─ A: Add Movement Input (Left)
    └─ D: Add Movement Input (Right)
```

### UE5 C++
```cpp
// In Character class
void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) {
    PlayerInputComponent->BindAxis("MoveForward", this, &AMyCharacter::MoveForward);
    PlayerInputComponent->BindAxis("MoveRight", this, &AMyCharacter::MoveRight);
}

void AMyCharacter::MoveForward(float Value) {
    if (Value != 0.0f) {
        // Get forward direction
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0, Rotation.Yaw, 0);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);

        AddMovementInput(Direction, Value);
    }
}
```

---

## COMBAT SYSTEM

### Three.js (Najika Dual-Wield)
```javascript
const COMBAT_SYSTEM = {
    leftHand: { type: 'wand', damage: 25 },
    rightHand: { type: 'sword', damage: 35 },
    stamina: 100,
    maxStamina: 100,

    attackLeft() {
        if (this.stamina < 10) return false;
        this.stamina -= 10;
        return true;
    },

    attackRight() {
        if (this.stamina < 15) return false;
        this.stamina -= 15;
        return true;
    },

    dodge() {
        if (this.stamina < 20) return false;
        this.stamina -= 20;
        this.dodgeRoll.active = true;
        return true;
    }
};
```

### UE5 Blueprint
```
Combat Component:
├─ Variables:
│   ├─ Stamina (Float): 100.0
│   ├─ MaxStamina (Float): 100.0
│   ├─ LeftHandWeapon (Actor Reference)
│   └─ RightHandWeapon (Actor Reference)
│
├─ Functions:
│   ├─ AttackLeft():
│   │   ├─ Check Stamina >= 10
│   │   ├─ Subtract 10
│   │   ├─ Play Animation
│   │   └─ Deal Damage (25)
│   │
│   ├─ AttackRight():
│   │   ├─ Check Stamina >= 15
│   │   ├─ Subtract 15
│   │   ├─ Play Animation
│   │   └─ Deal Damage (35)
│   │
│   └─ Dodge():
│       ├─ Check Stamina >= 20
│       ├─ Subtract 20
│       ├─ Enable IFrames (0.4s)
│       └─ Play Roll Animation
│
└─ Input Events:
    ├─ Left Mouse: AttackLeft
    ├─ Right Mouse: AttackRight
    └─ Space: Dodge
```

### UE5 C++
```cpp
// UCombatComponent.h
UCLASS()
class UCombatComponent : public UActorComponent {
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Stamina = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MaxStamina = 100.0f;

    UFUNCTION(BlueprintCallable)
    bool AttackLeft();

    UFUNCTION(BlueprintCallable)
    bool AttackRight();

    UFUNCTION(BlueprintCallable)
    bool Dodge();

private:
    AActor* LeftHandWeapon;
    AActor* RightHandWeapon;
};

// UCombatComponent.cpp
bool UCombatComponent::AttackLeft() {
    if (Stamina < 10.0f) return false;

    Stamina -= 10.0f;
    // Play animation, deal damage
    return true;
}

bool UCombatComponent::Dodge() {
    if (Stamina < 20.0f) return false;

    Stamina -= 20.0f;
    // Enable IFrames, play animation
    return true;
}
```

---

## PHYSICS & COLLISION

### Three.js (Manual Collision)
```javascript
// Character position clamping
const minX = -currentRoomSpan / 2 + CLAMP_PADDING;
const maxX = currentRoomSpan / 2 - CLAMP_PADDING;
characterGroup.position.x = Math.max(minX, Math.min(maxX, characterGroup.position.x));
characterGroup.position.z = Math.max(minZ, Math.min(maxZ, characterGroup.position.z));
```

### UE5 Blueprint
```
Collision Setup:
├─ Character Capsule:
│   ├─ Collision Preset: "Pawn"
│   ├─ Block: WorldStatic, WorldDynamic
│   └─ Overlap: Trigger
│
├─ Wall Collision:
│   ├─ Collision Preset: "BlockAll"
│   └─ Static Mesh Collision: Simple Collision
│
└─ Volume Trigger (Room Bounds):
    ├─ Collision Preset: "OverlapAllDynamic"
    └─ On Overlap: Clamp Position
```

### UE5 C++
```cpp
// Setup collision in Constructor
GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));
GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);

// Clamp position (in Tick)
FVector Location = GetActorLocation();
Location.X = FMath::Clamp(Location.X, MinX, MaxX);
Location.Y = FMath::Clamp(Location.Y, MinY, MaxY);
SetActorLocation(Location);
```

---

## ANIMATION SYSTEM

### Three.js (GLTFLoader Animations)
```javascript
const loader = new THREE.GLTFLoader();
loader.load('model.glb', (gltf) => {
    const mixer = new THREE.AnimationMixer(gltf.scene);
    const clip = THREE.AnimationClip.findByName(gltf.animations, 'Walk');
    const action = mixer.clipAction(clip);
    action.play();

    // In animate loop
    mixer.update(deltaTime);
});
```

### UE5 Blueprint
```
Animation Blueprint:
├─ State Machine:
│   ├─ Idle State
│   ├─ Walk State
│   ├─ Run State
│   └─ Attack State
│
├─ Blend Spaces:
│   ├─ Locomotion (2D):
│   │   ├─ X: Speed (0-750)
│   │   └─ Y: Direction (-180 to 180)
│   └─ Combat (1D):
│       └─ X: Attack Type (0-3)
│
└─ Transitions:
    ├─ Idle → Walk: Speed > 10
    ├─ Walk → Idle: Speed < 10
    └─ Any → Attack: Attack Input
```

### UE5 C++
```cpp
// Play Animation Montage
UAnimInstance* AnimInstance = GetMesh()->GetAnimInstance();
if (AnimInstance && AttackMontage) {
    AnimInstance->Montage_Play(AttackMontage, 1.0f);
}

// Set Animation Variables
AnimInstance->SetVariableValue(FName("Speed"), GetVelocity().Size());
AnimInstance->SetVariableValue(FName("IsAttacking"), bIsAttacking);
```

---

## ASSET LOADING

### Three.js (GLTFLoader)
```javascript
const loader = new THREE.GLTFLoader();
loader.load(
    'assets/room.glb',
    (gltf) => {
        scene.add(gltf.scene);
    },
    (xhr) => {
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    (error) => {
        console.error('Error loading model:', error);
    }
);
```

### UE5 Blueprint
```
Asset Loading:
├─ Import GLTF/FBX:
│   ├─ File → Import
│   ├─ Select .glb or .fbx
│   └─ Import Settings:
│       ├─ Import Mesh: TRUE
│       ├─ Import Materials: TRUE
│       ├─ Import Textures: TRUE
│       └─ Combine Meshes: FALSE
│
└─ Runtime Loading:
    ├─ Use Async Load Asset
    ├─ Load Static Mesh
    └─ Spawn Actor with Loaded Mesh
```

### UE5 C++ (Async Loading)
```cpp
// In C++
FStreamableManager& Streamable = UAssetManager::GetStreamableManager();
TSoftObjectPtr<UStaticMesh> MeshAsset = TSoftObjectPtr<UStaticMesh>(
    FSoftObjectPath(TEXT("/Game/Assets/room.room"))
);

Streamable.RequestAsyncLoad(
    MeshAsset.ToSoftObjectPath(),
    FStreamableDelegate::CreateLambda([this, MeshAsset]() {
        if (UStaticMesh* LoadedMesh = MeshAsset.Get()) {
            MeshComponent->SetStaticMesh(LoadedMesh);
        }
    })
);
```

---

## WICHTIGE KONVERTIERUNGEN

### Einheiten
| Three.js | UE5 | Faktor |
|----------|-----|--------|
| 1 Unit | 100 cm | × 100 |
| Position | Position × 100 | × 100 |
| Rotation | Rotation | 1:1 (Degrees) |
| Scale | Scale | 1:1 |

### Koordinatensystem
```
Three.js (Right-handed, Y-up):
    Y (up)
    |
    |_____ X (right)
   /
  Z (forward)

UE5 (Left-handed, Z-up):
    Z (up)
    |
    |_____ X (forward)
   /
  Y (right)
```

### Konvertierungs-Funktion
```cpp
// Three.js → UE5
FVector ConvertThreeJSToUE5(float x, float y, float z) {
    return FVector(
        x * 100.0f,  // X → X
        z * 100.0f,  // Z → Y
        y * 100.0f   // Y → Z
    );
}

// UE5 → Three.js
FVector ConvertUE5ToThreeJS(float x, float y, float z) {
    return FVector(
        x / 100.0f,  // X → X
        z / 100.0f,  // Z → Y
        y / 100.0f   // Y → Z
    );
}
```

---

## PERFORMANCE-TIPPS

### Three.js → UE5 Optimierungen

1. **Instancing**
   - Three.js: `THREE.InstancedMesh`
   - UE5: `Instanced Static Mesh Component` oder `Hierarchical Instanced Static Mesh`

2. **Level of Detail (LOD)**
   - Three.js: Manuelles LOD-Switching
   - UE5: Automatic LOD System (Built-in)

3. **Occlusion Culling**
   - Three.js: Frustum Culling
   - UE5: Hardware Occlusion Queries + Software Occlusion

4. **Shadows**
   - Three.js: Shadow Maps (2048x2048)
   - UE5: Cascaded Shadow Maps + Distance Field Shadows

---

## TESTING CHECKLIST (Generisch)

- [ ] Scene Setup (Background, Fog)
- [ ] Camera (FOV, Position, Modes)
- [ ] Lighting (Ambient, Directional, Point)
- [ ] Character Movement (Speed, Height, Collision)
- [ ] Combat System (Attacks, Stamina, Dodge)
- [ ] Animations (Idle, Walk, Attack)
- [ ] Asset Loading (Meshes, Textures)
- [ ] Koordinaten-Konvertierung korrekt
- [ ] Performance acceptable (60+ FPS)

---

## NAJIKA WORLD - PROJEKTSPEZIFISCHES SYSTEM-MAPPING

### Komplette Datei-Inventur: digivice/js/ (141+ Dateien)

Die folgende Tabelle zeigt **jede Three.js-Datei** und ihr UE5-Pendant.

---

### CORE 3D SCENE

| Three.js Datei | Zeilen | UE5 Pendant | UE5 Klasse/System |
|----------------|--------|-------------|-------------------|
| `3d_scene.js` | 5800+ | Level Blueprint + GameMode | `ANajikaGameMode`, `ANajikaPlayerController` |
| `game_input.js` | - | Enhanced Input System | `UInputAction`, `UInputMappingContext` |
| `touch_controls.js` | - | Enhanced Input (Touch) | `UInputTrigger`, Touch Mappings |
| `mobile_controls.js` | - | UMG Widget (Virtual Joystick) | `UVirtualJoystickWidget` |
| `cleanup_manager.js` | - | Garbage Collection (automatisch) | UE5 GC ist automatisch |
| `safe_functions.js` | - | Nicht noetig | UE5 hat native Null-Checks |

**Notizen:**
- `3d_scene.js` ist die Master-Datei. In UE5 wird das auf GameMode + Level Blueprint + PlayerController aufgeteilt
- Enhanced Input System ersetzt alle manuellen Key-Listener
- Three.js `requestAnimationFrame` = UE5 `Tick()` Funktion

---

### COMBAT SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `combat/real_3d_combat.js` | `NajikaCombatComponent` | GAS (Gameplay Ability System) |
| `battle_core.js` | `NajikaBattleManager` | Game Instance Subsystem |
| `equipment_combat.js` | `NajikaEquipmentComponent` | GAS Attribute Set |
| `touch_combat.js` | Enhanced Input (Touch) | Gemeinsam mit `mobile_controls.js` |
| `nemesis_arena_frontend.js` | `NajikaNemesisComponent` | Bereits als C++ vorhanden! |
| `simple_arena.js` | `NajikaArenaComponent` | Bereits als C++ vorhanden! |

**Backend-APIs die UE5 aufruft:**
```
POST /api/battle/start          - Kampf starten
POST /api/battle/action         - Angriff/Verteidigung
POST /api/battle/combo          - Combo-Angriff
GET  /api/battle/status/{id}    - Kampfstatus
POST /api/combat-magic/infuse   - Waffe verzaubern
POST /api/combat-magic/grab     - Wrestling-Griff
POST /api/combat-magic/tids     - TIDS Spezialangriff
```

**Three.js Hitbox (Box3) → UE5:**
```cpp
// Three.js: const box = new THREE.Box3().setFromObject(mesh);
// UE5: Collision Component (Capsule/Box)
UPROPERTY()
UCapsuleComponent* HitboxCapsule;

// Overlap Events statt manueller Box-Intersection
HitboxCapsule->OnComponentBeginOverlap.AddDynamic(this, &ACombat::OnHitboxOverlap);
```

---

### COMPANION / NPC SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `companion_3d.js` | `ANajikaCompanionAI` | AI Controller + Behavior Tree |
| `companion_approval.js` | `UCompanionApprovalComponent` | ActorComponent mit Events |
| `companion_swap_system.js` | Companion Manager | Game Instance Subsystem |
| `slime_companion.js` | `ANajikaSlimeAI` | Bereits als C++ vorhanden! |
| `npc_dialogue_system.js` | Dialogue Plugin | CommonUI + Data Tables |
| `npc_interaction.js` | `UNPCInteractionComponent` | SphereCollision + UI Widget |
| `npc_schedule_system.js` | `UNPCScheduleComponent` | Timeline + Spline Movement |
| `npc_personality_system.js` | `UNPCPersonalityComponent` | Data Asset + Struct |
| `overworld_npcs.js` | NPC Spawner Blueprint | Level Streaming + Data Tables |

**Companion Follow-AI Mapping:**
```
Three.js:                         UE5:
─────────                         ────
followDistance = 3.5               AI MoveTo (Blackboard: FollowDistance = 350cm)
lerp(pos, target, 0.05)           AIController->MoveToLocation() mit AcceptanceRadius
lookAt(player)                     SetFocalPoint(PlayerLocation)
animation.play("walk")            AnimBP State Machine: Idle → Walk
pink tint shader                  Material Instance: BaseColor *= FLinearColor(1, 0.7, 0.8)
name label (THREE.Sprite)         UWidgetComponent (Screenspace, Text)
```

**Backend-APIs fuer NPCs:**
```
GET  /api/companion/status       - Companion-Zustand
POST /api/companion/interact     - Interaktion
GET  /api/living/stats           - Hunger/Energie/Stimmung
POST /api/najika/feed            - Fuettern
POST /api/najika/sleep           - Schlafen lassen
```

---

### WELT / UMGEBUNG

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `world/world_manager.js` | `ANajikaWorldManager` | GameState oder Subsystem |
| `world/terrain_generator.js` | Landscape Tool | Heightmap Import + Procedural |
| `world/biome_system.js` | Landscape Layer Blend | Material Functions + Foliage |
| `world/vegetation_system.js` | Procedural Foliage Spawner | PCG (Procedural Content Gen) |
| `world/weather_system.js` | Niagara + Post Process | Weather Blueprint Actor |
| `world/day_night_cycle.js` | Sky Atmosphere + Sun | `ADirectionalLight` mit Timeline |
| `world/region_streaming.js` | World Partition | Automatisch in UE5! |
| `world/region_streaming_v2.js` | World Partition + Data Layers | HLOD + Streaming |
| `world/lod_manager.js` | Nanite / Auto-LOD | Automatisch in UE5! |
| `world/asset_loader.js` | Async Asset Loading | `FStreamableManager` |
| `world/asset_discovery.js` | Asset Registry | `UAssetManager` |
| `world/city_builder.js` | PCG Graph | Procedural Content Generation |
| `world/boss_marker_system.js` | Map Marker Widget | UMG + World Space Widget |
| `world/world_systems_integration.js` | Game Framework | GameMode verteilt alles |

**Wichtig - UE5 macht vieles automatisch:**
- **Region Streaming** → World Partition (built-in, kein Code noetig!)
- **LOD Management** → Nanite (automatisch fuer Static Meshes)
- **Occlusion Culling** → Hardware Occlusion (automatisch)
- **Terrain** → Landscape System (Editor-Tool, nicht prozedural noetig)

**Day/Night Cycle Mapping:**
```
Three.js:                               UE5:
─────────                               ────
dirLight.position.set(x, y, z)          DirectionalLight->SetActorRotation()
ambientLight.intensity = 0.2            SkyLight->SetIntensity()
scene.fog.color = nightColor            ExponentialHeightFog->SetFogColor()
material.emissive = lampColor           Emissive Material Parameter
1 Echtminute = 10 Game-Minuten          Timeline Blueprint (6s = 1 Game-Stunde)
```

---

### DUNGEON SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `dungeon_generator.js` | PCG Graph | Procedural Content Generation Plugin |
| `dungeon_crawler.js` | Dungeon GameMode | Separater GameMode fuer Dungeons |
| `room_connector.js` | Level Streaming | Sublevel pro Raum, Streaming Volumes |
| `overworld_enemies.js` | Enemy Spawner BP | `AEnemySpawner` mit SpawnVolumes |

**Dungeon-Generator Algorithmus (BSP + RandomWalk, 8 Biomes):**
```
Three.js Dungeon:                       UE5:
─────────────────                       ────
BSP Tree Split                          PCG Graph mit Partition Node
Room = THREE.BoxGeometry                Room = Level Instance (Sublevel)
Corridor = line between rooms           Spline + Instanced Static Mesh
Enemy spawn points                      SpawnVolume + EQS Query
Loot chests = THREE.Group               BP_LootChest Actor (Interaction)
Biome = texture swap                    Level Instance Variant (Material Swap)
```

---

### PARTICLE / VFX SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `particles/combat_particles.js` | Niagara System | NS_CombatEffects |
| `particles/magic_particles.js` | Niagara System | NS_MagicSpells (pro Element) |
| `particles/environment_particles.js` | Niagara System | NS_Weather (Rain/Snow/Dust) |
| `particles/evolution_effects.js` | Niagara System | NS_Evolution (Burst + Glow) |

**Particle Mapping:**
```
Three.js:                               UE5 Niagara:
─────────                               ────────────
THREE.Points + BufferGeometry           Sprite Renderer + Emitter
position.lerp(target, 0.1)             Velocity/Force Module
material.opacity -= 0.01               Alpha Fade over Lifetime
color.lerpColors(start, end, t)         Color over Lifetime Curve
scale *= 0.99                           Size over Lifetime Curve
Math.random() * spread                  Random Distribution Module
```

---

### AUDIO SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `audio/music_system.js` | Sound Manager | `USoundMix` + `USoundClass` |
| `audio/spatial_audio_engine.js` | Attenuation Settings | `USoundAttenuation` (automatisch 3D) |
| `audio/combat_sfx_system.js` | Sound Cues | `USoundCue` mit Random/Switch Nodes |
| `radio_najika.js` | Media Player | `UMediaPlayer` + `UMediaSoundComponent` |

**Spatial Audio ist in UE5 native:**
```
Three.js:                               UE5:
─────────                               ────
THREE.AudioListener (camera)            Listener = PlayerController (automatisch!)
THREE.PositionalAudio(listener)         UAudioComponent mit SoundAttenuation
audio.setRefDistance(10)                 AttenuationSettings.InnerRadius = 1000cm
audio.setRolloffFactor(1)               AttenuationSettings.FalloffDistance
audio.setDistanceModel('linear')        AttenuationSettings.DistanceAlgorithm
```

---

### UI SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `ui/combat_special_ui.js` | UMG Widget | WBP_CombatHUD |
| `ui/character_stats_ui.js` | UMG Widget | WBP_CharacterStats |
| `ui/bestiary_ui.js` | UMG Widget | WBP_Bestiary (ListView) |
| `ui/stat_training_ui.js` | UMG Widget | WBP_StatTraining |
| `ui/skill_tree_ui.js` | UMG Widget | WBP_SkillTree (Custom Canvas) |
| `ui/minimap.js` | UMG Widget | WBP_Minimap (SceneCaptureComponent2D) |
| `ui/world_map_ui.js` | UMG Widget | WBP_WorldMap (Interaktiv) |
| `ui/world_map_full_ui.js` | UMG Widget | WBP_WorldMapFull |
| `ui/housing_ui.js` | UMG Widget | WBP_Housing |
| `ui/pvp_ui.js` | UMG Widget | WBP_PvP |
| `ui/faction_ui.js` | UMG Widget | WBP_Factions |
| `ui/creature_ui.js` | UMG Widget | WBP_CreatureInfo |
| `ui/law_notification.js` | UMG Widget | WBP_Notification (Animated) |
| `ui/affinity_ui.js` | UMG Widget | WBP_NPCAffinity |
| `ui/gildenhaus_ui.js` | UMG Widget | WBP_GuildHouse |
| `quest_ui.js` | UMG Widget | WBP_QuestLog |
| `chaos_event_ui.js` | UMG Widget | WBP_ChaosEvent (Fullscreen) |
| `world_hud.js` | UMG Widget | WBP_WorldHUD (Always Visible) |

**UI Pattern:**
```
Three.js DOM:                            UE5 UMG:
─────────────                            ────────
document.createElement('div')            CreateWidget<UUserWidget>()
element.style.position = 'absolute'      Anchor: Center/TopLeft/etc.
element.innerHTML = '<span>HP</span>'    UTextBlock + UProgressBar
element.addEventListener('click', fn)    OnClicked.AddDynamic()
element.classList.add('active')          PlayAnimation("Activate")
setTimeout(hide, 3000)                   SetTimer → SetVisibility(Hidden)
```

---

### MINIGAMES / SPEZIAL-SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `3d_dice_system.js` | Physics Actor | `APhysicsDice` mit Chaos Physics |
| `fishing.js` | Fishing GameMode | Minigame Blueprint |
| `garden.js` | Farming System | `AFarmPlot` Actor + Timer |
| `creature_taming.js` | Taming Component | `UTamingComponent` |
| `instrument_system.js` | Music System | `UInstrumentComponent` |
| `instrument_player.js` | Music Player UI | UMG + Audio |
| `najika_instrument_animator.js` | AnimMontage | Instrument-spezifische Montages |
| `dungeon_dice_game.js` | Dice Minigame | UMG + Physics Dice |
| `minigames/turn_based_battle_minigame.js` | Turn-Based BP | Separate GameMode |

---

### GAMEPLAY SYSTEME (Kein Three.js, aber JS → UE5)

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `monster_registry.js` | Data Table | `DT_Monsters` (CSV/JSON Import) |
| `game_events.js` | Event Dispatcher | `UGameplayMessageSubsystem` |
| `game_events_ws_bridge.js` | HTTP Module | `FHttpModule` fuer REST Calls |
| `websocket_client.js` | WebSocket Module | `FWebSocketsModule` |
| `multiplayer_manager.js` | Online Subsystem | `UOnlineSubsystem` |
| `economy_system.js` | Economy Component | `UEconomyComponent` |
| `faction_system.js` | Faction Component | `UFactionComponent` + Data Asset |
| `career_system.js` | Career Component | `UCareerComponent` |
| `world_event_generator.js` | World Event Manager | Timer + Random Events |
| `postman_system.js` | Mail System | Data Table + Timer |
| `command_system.js` | Cheat Manager | `UCheatManager` Extension |
| `system_monitor.js` | Stat System | `DECLARE_STATS_GROUP` |
| `najika_logger.js` | UE_LOG | `UE_LOG(LogNajika, Log, TEXT(...))` |

---

### PERFORMANCE SYSTEME

| Three.js Datei | UE5 Pendant | Notizen |
|----------------|-------------|---------|
| `performance/performance_monitor.js` | Stat Commands | `stat fps`, `stat unit` (built-in) |
| `performance/cache_manager.js` | Asset Manager | `UAssetManager` (built-in) |
| `performance/resource_loader.js` | Async Loading | `FStreamableManager` (built-in) |
| `mobile_performance_manager.js` | Scalability | Device Profiles + Scalability Groups |

**UE5 hat die meisten Performance-Features built-in:**
- LOD: Nanite (automatisch)
- Culling: Hardware Occlusion (automatisch)
- Streaming: World Partition (automatisch)
- Memory: Garbage Collection (automatisch)

---

### BUILDING / HOUSING SYSTEME

| Three.js Datei | UE5 Pendant | Implementierung |
|----------------|-------------|-----------------|
| `housing_3d.js` | Housing Blueprint | `ABuildingActor` + Snap System |
| `housing_3d_placement.js` | Placement System | Grid Snap + Preview Ghost |
| `buildings_custom.js` | Building Data | Data Table + Static Meshes |
| `farming_3d.js` | Farm Visualization | Instanced Static Mesh + Timer |

**Placement System Mapping (Lego Fortnite Style):**
```
Three.js:                               UE5:
─────────                               ────
raycaster.intersectObjects(ground)       LineTrace(Start, End, ECC_WorldStatic)
previewMesh.position = hitPoint          PreviewActor->SetActorLocation(HitResult.Location)
snap to grid (Math.round)               SnapToGrid(GridSize=100)
previewMesh.material.color = green/red   PreviewMaterial: Green=valid, Red=blocked
scene.add(buildingMesh)                  SpawnActor<ABuildingActor>(Location)
```

---

### API-INTEGRATION: WIE UE5 MIT DEM BACKEND SPRICHT

**Alle API-Endpoints die UE5 aufruft (Port 8000):**

```
SYSTEM          | ENDPOINT                        | METHODE
────────────────|─────────────────────────────────|────────
Chat            | /api/chat/message               | POST
Voice TTS       | /api/voice-ue5/speak            | POST
Voice STT       | /api/voice-ue5/listen           | POST
Voice Status    | /api/voice-ue5/status            | GET
Memory Query    | /api/memory/query               | POST
Memory Add      | /api/memory/add                 | POST
Memory Recall   | /api/memory/recall/{topic}      | GET
Memory Stats    | /api/memory/stats               | GET
Game Event      | /api/memory/game-event          | POST
Conversation    | /api/memory/conversation        | POST
Battle Start    | /api/battle/start               | POST
Battle Action   | /api/battle/action              | POST
Magic Infuse    | /api/combat-magic/infuse        | POST
Magic Schools   | /api/magic/observe              | POST
Magic Meister   | /api/magic/meister/activate     | POST
Morph Learn     | /api/magic/morph/learn          | POST
Spell Names     | /api/spells/name/create         | POST
Companion       | /api/companion/status           | GET
Slime           | /api/slime/status               | GET
Slime AI        | /api/slime-ai/personality       | GET
Living Stats    | /api/living/stats               | GET
Feed Najika     | /api/najika/feed                | POST
World State     | /api/world/status               | GET
World Map       | /api/world-map/regions          | GET
Housing         | /api/housing/buildings          | GET
Farming         | /api/farming/plots              | GET
Cards           | /api/cards/collection/{id}      | GET
Dice            | /api/dice/roll                  | POST
NPC             | /api/game/npc/{id}              | GET
Auth            | /api/auth/login                 | POST
WebSocket       | /ws/connect?token=...           | WS
```

**UE5 HTTP-Call Pattern (C++):**
```cpp
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"

void ANajikaGameMode::CallBackendAPI(const FString& Endpoint, const FString& Body) {
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(FString::Printf(TEXT("http://127.0.0.1:8000%s"), *Endpoint));
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request->SetContentAsString(Body);
    Request->OnProcessRequestComplete().BindUObject(this, &ANajikaGameMode::OnAPIResponse);
    Request->ProcessRequest();
}
```

**UE5 HTTP-Call Pattern (Blueprint):**
```
VaRest Plugin oder HTTP Blueprint Library:
1. Create HTTP Request
2. Set URL: "http://127.0.0.1:8000/api/..."
3. Set Verb: POST
4. Set Body: JSON String
5. Send Request
6. On Response → Parse JSON → Update Game State
```

---

### PRIORISIERUNG FUER UE5 PORTIERUNG

**Phase 1 - Core (Wochen 1-4):**
| Prio | System | Three.js | UE5 Status |
|------|--------|----------|------------|
| 1 | Character Controller | `3d_scene.js` | BP_NajikaCharacter |
| 2 | Camera System | `3d_scene.js` | Spring Arm + Camera |
| 3 | Combat (Dual-Wield) | `real_3d_combat.js` | GAS + AnimMontages |
| 4 | Companion Follow-AI | `companion_3d.js` | Behavior Tree |
| 5 | Basic UI/HUD | `world_hud.js` + `combat_special_ui.js` | UMG Widgets |

**Phase 2 - Welt (Wochen 5-8):**
| Prio | System | Three.js | UE5 Status |
|------|--------|----------|------------|
| 6 | Terrain + Biomes | `terrain_generator.js` + `biome_system.js` | Landscape + Materials |
| 7 | Day/Night Cycle | `day_night_cycle.js` | Sky Atmosphere BP |
| 8 | Weather | `weather_system.js` | Niagara + Post Process |
| 9 | NPC System | `npc_*.js` (4 Dateien) | AI Controller + BT |
| 10 | Region Streaming | `region_streaming_v2.js` | World Partition (auto!) |

**Phase 3 - Systeme (Wochen 9-14):**
| Prio | System | Three.js | UE5 Status |
|------|--------|----------|------------|
| 11 | Dungeon Generator | `dungeon_generator.js` | PCG Plugin |
| 12 | Housing/Building | `housing_3d*.js` | Snap-Placement BP |
| 13 | Particles/VFX | `particles/*.js` (4 Dateien) | Niagara Systems |
| 14 | Spatial Audio | `spatial_audio_engine.js` | Built-in! |
| 15 | Backend Integration | `websocket_client.js` | HTTP + WS Module |

**Phase 4 - Polish (Wochen 15+):**
| Prio | System | Three.js | UE5 Status |
|------|--------|----------|------------|
| 16 | Minigames | `fishing.js`, `3d_dice_system.js` | Separate GameModes |
| 17 | Instrument System | `instrument_*.js` | AnimMontage + Audio |
| 18 | Monster Registry | `monster_registry.js` | Data Tables |
| 19 | Economy/Factions | `economy_system.js`, `faction_system.js` | Components |
| 20 | Multiplayer | `multiplayer_manager.js` | Online Subsystem |

---

### ALREADY DONE (Bereits als C++ in UE5)

Diese Three.js-Systeme wurden bereits nach C++ portiert:

| System | Three.js | UE5 C++ Datei | Status |
|--------|----------|---------------|--------|
| Combat Component | `real_3d_combat.js` | `Combat/NajikaCombatComponent.h/.cpp` | DONE |
| Slime System | `slime_companion.js` | `Slime/NajikaSlimeComponent.h/.cpp` | DONE |
| Nemesis System | `nemesis_arena_frontend.js` | `Nemesis/NajikaNemesisComponent.h/.cpp` | DONE |
| Arena System | `simple_arena.js` | `Arena/NajikaArenaComponent.h/.cpp` | DONE |

---

## TESTING CHECKLIST (Projektspezifisch)

### Phase 1:
- [ ] Najika Character laeuft in UE5
- [ ] Kamera: Orbit/Third/First Person wechselbar
- [ ] Dual-Wield Combat funktioniert (Links/Rechts)
- [ ] Dodge Roll mit I-Frames
- [ ] Companion Najika folgt dem Spieler
- [ ] HP/Stamina/Mana HUD sichtbar
- [ ] Backend API erreichbar (127.0.0.1:8000)

### Phase 2:
- [ ] Goetterfels Terrain geladen
- [ ] 8 Regionen mit Biom-Materialien
- [ ] Tag/Nacht-Zyklus laeuft
- [ ] Wetter-Effekte (Regen/Schnee)
- [ ] NPCs bewegen sich nach Tagesplan
- [ ] NPC-Dialog funktioniert

### Phase 3:
- [ ] Dungeon generiert sich prozedural
- [ ] Housing: Gebaeude platzieren
- [ ] Magie-Partikel sichtbar
- [ ] 3D Audio positionell korrekt
- [ ] Chat mit Najika via Backend API
- [ ] Voice (TTS/STT) funktioniert

### Phase 4:
- [ ] Angel-Minigame spielbar
- [ ] Wuerfel-System (3D Physics)
- [ ] Instrumente spielbar
- [ ] Alle 50+ API-Endpoints getestet
- [ ] Multiplayer grundlegend

---

## RESSOURCEN

- **Three.js Docs:** https://threejs.org/docs/
- **UE5 Docs:** https://docs.unrealengine.com/5.0/
- **GLTF Import:** https://github.com/KhronosGroup/UnrealEngine (GLTF Plugin)
- **Coordinate Systems:** https://docs.unrealengine.com/5.0/coordinate-space-terminology/
- **GAS (Gameplay Ability System):** https://docs.unrealengine.com/5.0/gameplay-ability-system/
- **PCG (Procedural Content):** https://docs.unrealengine.com/5.0/procedural-content-generation-framework/
- **Niagara VFX:** https://docs.unrealengine.com/5.0/niagara-visual-effects/
- **World Partition:** https://docs.unrealengine.com/5.0/world-partition/

---

**Version:** 2.0
**Erstellt:** 2026-02-09 (V1.0 generisch)
**Erweitert:** 2026-02-11 (V2.0 projektspezifisches Mapping, 141+ Dateien)
**Projekt:** Najika World
**Author:** Claude Code (OPUS-1 + OPUS-2)
