# UE5 PROJEKT SETUP - NAJIKA WORLD

**Erstellt:** 2026-02-04
**Von:** OPUS-2
**UE5 Version:** 5.6.1 oder 5.7.2

---

## SCHRITT 1: PROJEKT ERSTELLEN

### Im Epic Games Launcher:
1. **Unreal Engine** Tab öffnen
2. **Launch** bei 5.6.1 oder 5.7.2 klicken
3. Warten bis Editor lädt

### Im Unreal Project Browser:
1. **Games** auswählen
2. **Third Person** Template
3. **C++** auswählen (NICHT Blueprint!)
4. Einstellungen:
   - Project Name: `NajikaWorld`
   - Project Location: `C:\Najika_World\UE5`
   - ☑️ Starter Content (optional, kann später löschen)
5. **Create** klicken

---

## SCHRITT 2: PROJEKT-EINSTELLUNGEN

### Project Settings öffnen (Edit → Project Settings)

#### Input (Enhanced Input aktivieren)
```
Engine → Input:
- Default Player Input Class: EnhancedPlayerInputComponent
- Default Input Component Class: EnhancedInputComponent
```

#### Maps & Modes
```
Project → Maps & Modes:
- Default GameMode: Später unseren NajikaGameMode
- Editor Startup Map: ThirdPersonMap (vorerst)
```

#### Plugins aktivieren
```
Edit → Plugins:
☑️ Enhanced Input (sollte schon an sein)
☑️ Common UI
☑️ Gameplay Abilities
☑️ Niagara (für Explosion-Effekte!)
```

---

## SCHRITT 3: ORDNERSTRUKTUR ERSTELLEN

Im Content Browser (Rechtsklick → New Folder):

```
Content/
├── NajikaWorld/
│   ├── Characters/
│   │   ├── Najika/
│   │   │   ├── Mesh/
│   │   │   ├── Animations/
│   │   │   ├── Materials/
│   │   │   └── Blueprints/
│   │   ├── MimikTruhe/
│   │   │   ├── Mesh/
│   │   │   └── Blueprints/
│   │   └── NPCs/
│   ├── Core/
│   │   ├── GameModes/
│   │   ├── PlayerControllers/
│   │   └── Input/
│   ├── Systems/
│   │   ├── Combat/
│   │   ├── Companion/
│   │   ├── Slime/
│   │   └── Quest/
│   ├── Environments/
│   │   ├── Goetterfels/
│   │   ├── IceRegion/
│   │   ├── DesertRegion/
│   │   ├── SwampRegion/
│   │   ├── CoastRegion/
│   │   ├── CavesRegion/
│   │   ├── VolcanoRegion/
│   │   ├── ForestRegion/
│   │   └── HighlandRegion/
│   ├── UI/
│   │   ├── HUD/
│   │   ├── Menus/
│   │   └── Widgets/
│   └── Audio/
│       ├── Music/
│       ├── SFX/
│       └── Voice/
```

---

## SCHRITT 4: NAJIKA FBX IMPORTIEREN

### FBX-Pfad:
```
C:\Najika_World\assets\models\najika\najika_rigged_final.fbx
```

### Import:
1. Content Browser → `NajikaWorld/Characters/Najika/Mesh`
2. **Import** Button oder Drag & Drop
3. Import Settings:
   ```
   ☑️ Skeletal Mesh
   ☑️ Import Mesh
   ☑️ Import as Skeletal
   Skeleton: Create New
   ☑️ Import Animations (falls vorhanden)
   ☑️ Import Materials
   ☑️ Import Textures
   Material Import Method: Create New Materials
   ```
4. **Import All** klicken

### Nach Import prüfen:
- Skeletal Mesh: `SK_Najika`
- Skeleton: `SK_Najika_Skeleton`
- Physics Asset: `SK_Najika_PhysicsAsset`
- Material: `M_Najika` (Textur sollte drin sein)

---

## SCHRITT 5: CHARACTER BLUEPRINT ERSTELLEN

### Blueprint erstellen:
1. `Content/NajikaWorld/Characters/Najika/Blueprints/`
2. Rechtsklick → **Blueprint Class**
3. Parent Class: **Character**
4. Name: `BP_NajikaCharacter`
5. Doppelklick zum Öffnen

### Components einrichten:

#### Mesh Component:
```
Components Panel → Mesh (Inherited)
Details Panel:
- Skeletal Mesh: SK_Najika
- Anim Class: Später (ABP_Najika)
```

#### Spring Arm hinzufügen:
```
Components Panel → Add → Spring Arm
Name: CameraBoom
Details:
- Target Arm Length: 300
- ☑️ Use Pawn Control Rotation
- Socket Offset: (0, 0, 50)
- ☑️ Do Collision Test
```

#### Camera hinzufügen:
```
Auf CameraBoom: Add → Camera
Name: FollowCamera
Details:
- ☑️ Use Pawn Control Rotation: NEIN (Spring Arm macht das)
```

### Character Movement einstellen:
```
Components → CharacterMovement (Inherited)
Details:
- Max Walk Speed: 600
- Max Walk Speed Crouched: 300
- Jump Z Velocity: 500
- Air Control: 0.35
- ☑️ Can Crouch
- Crouch Half-Height: 60
```

---

## SCHRITT 6: INPUT ACTIONS ERSTELLEN

### Input Actions (IA_*):
```
Content/NajikaWorld/Core/Input/
Rechtsklick → Input → Input Action

Erstellen:
- IA_Move (Value Type: Axis2D)
- IA_Look (Value Type: Axis2D)
- IA_Jump (Value Type: Digital/Bool)
- IA_Attack_Left (Value Type: Digital)      ← Q
- IA_Attack_Right (Value Type: Digital)     ← E
- IA_Attack_Left_Heavy (Value Type: Digital) ← Shift+Q
- IA_Attack_Right_Heavy (Value Type: Digital) ← Shift+E
- IA_Interact (Value Type: Digital)         ← F
- IA_Dodge (Value Type: Digital)            ← Space (double tap) oder Ctrl
```

### Input Mapping Context (IMC_Default):
```
Rechtsklick → Input → Input Mapping Context
Name: IMC_NajikaDefault

Mappings:
IA_Move:
  - W: (1, 0)
  - S: (-1, 0)
  - A: (0, -1)
  - D: (0, 1)

IA_Look:
  - Mouse XY

IA_Jump:
  - Space Bar

IA_Attack_Left:
  - Q

IA_Attack_Right:
  - E

IA_Attack_Left_Heavy:
  - Q + Shift (Modifier: Shift)

IA_Attack_Right_Heavy:
  - E + Shift (Modifier: Shift)

IA_Interact:
  - F
```

---

## SCHRITT 7: ANIMATION BLUEPRINT

### Animation Blueprint erstellen:
```
Content/NajikaWorld/Characters/Najika/Animations/
Rechtsklick → Animation → Animation Blueprint
Skeleton: SK_Najika_Skeleton
Name: ABP_Najika
```

### Basis State Machine:
```
AnimGraph:
1. Add → State Machine → "Locomotion"

States:
- Idle (Entry)
- Walk
- Run
- Jump_Start
- Jump_Loop
- Jump_End

Transitions:
Idle → Walk: Speed > 10
Walk → Run: Speed > 300
Walk → Idle: Speed < 10
Run → Walk: Speed < 300
Any → Jump_Start: IsInAir AND JustJumped
Jump_Start → Jump_Loop: Animation finished
Jump_Loop → Jump_End: NOT IsInAir
Jump_End → Idle: Animation finished
```

### Event Graph Variablen:
```
Variables:
- Speed (Float)
- IsInAir (Bool)
- IsCrouching (Bool)

Event Blueprint Update Animation:
- Get Owning Actor → Cast to Character
- Get Velocity → Vector Length → Set Speed
- Get Movement Component → IsFalling → Set IsInAir
- Get Movement Component → IsCrouching → Set IsCrouching
```

---

## SCHRITT 8: GAME MODE

### Game Mode erstellen:
```
Content/NajikaWorld/Core/GameModes/
Rechtsklick → Blueprint Class → Game Mode Base
Name: BP_NajikaGameMode

Defaults:
- Default Pawn Class: BP_NajikaCharacter
- Player Controller Class: (default oder eigener später)
```

### Level Settings:
```
Window → World Settings
GameMode Override: BP_NajikaGameMode
```

---

## SCHRITT 9: TESTEN

1. **Play** klicken (Alt+P)
2. Prüfen:
   - [ ] Najika spawnt
   - [ ] WASD funktioniert
   - [ ] Maus dreht Kamera
   - [ ] Springen funktioniert
   - [ ] Keine T-Pose (Animation läuft)

---

## NÄCHSTE SCHRITTE

Nach diesem Setup:
1. HTTP-Client für API-Calls implementieren (siehe `NajikaAPIClient.h/cpp`)
2. Combat System (Q/E Attacks)
3. Companion System (Najika KI)
4. HUD (Health, Stamina, etc.)

---

## TROUBLESHOOTING

### Najika ist weiß/ohne Textur:
- Material prüfen → Texture Sample Node → Textur zuweisen
- Falls Textur fehlt: Aus `Downloads/...texture.png` importieren

### T-Pose im Spiel:
- Animation Blueprint dem Mesh zuweisen
- Prüfen ob Animationen zum Skeleton passen

### Input reagiert nicht:
- Enhanced Input Plugin aktiv?
- Input Mapping Context dem Player Controller zugewiesen?

### Kamera dreht nicht:
- Spring Arm: "Use Pawn Control Rotation" = true
- Player Controller: "Use Controller Rotation Yaw" prüfen

---

*"EXPLOSION!!! Najika ist bereit für UE5!" - Najika*
