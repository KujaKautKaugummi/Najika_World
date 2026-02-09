# NAJIKA 3D MODEL SPECIFICATIONS

**Ziel:** 3D-Modell für Skelett-Avatar (Blender + KayKit-kompatibel)

---

## 🎯 ZWEI VERSIONEN

### VERSION 1: KAYKIT-STYLE (SOFORT NUTZBAR)
- **Poly Count:** ~500-1500 Tris (low-poly wie KayKit)
- **Stil:** Stylized, simple, cute
- **Textures:** Simple colors, minimal details
- **Rigging:** Basic humanoid skeleton
- **Format:** GLB (GLTF Binary)
- **Kompatibilität:** Passt ins aktuelle Najika-System

### VERSION 2: BLENDER HIGH-DETAIL (SPÄTER)
- **Poly Count:** ~10,000-50,000 Tris (high-quality)
- **Stil:** Detailed anime, realistic textures
- **Textures:** PBR materials, detailed clothing
- **Rigging:** Full humanoid rig + face bones
- **Format:** FBX, GLB, OBJ
- **Use:** Cinematics, close-ups, final version

---

## 📐 VERSION 1: KAYKIT-STYLE SPECS

### BODY MESH (LOW-POLY)

**Base Body:**
```
Proportions (140cm total):
├── Head: 20cm (14% - chibi proportions)
├── Torso: 40cm (29%)
├── Arms: 35cm each (25%)
├── Legs: 45cm (32%)
└── Total: 140cm
```

**Poly Budget:**
- Head: 150 tris
- Body/Torso: 200 tris
- Arms (both): 150 tris
- Legs (both): 200 tris
- Hands: 100 tris
- **Total Body:** ~800 tris

**Simplified Features:**
- **Face:** Basic planes (no detailed features)
- **Eyes:** Simple spheres with red texture
- **Hair:** Chunky blocks (KayKit style)
- **Clothing:** Part of body mesh (not separate)

### CLOTHING & ACCESSORIES (LOW-POLY)

**Hat:**
- Cone shape: 50 tris
- Brim: 30 tris
- **Total:** 80 tris

**Dress:**
- Integrated into body mesh
- Simple A-line shape
- Flat colors (red/black/white)

**Cape:**
- Simple rectangle: 40 tris
- No physics (static pose or simple sway)

**Staff:**
- Cylinder: 20 tris
- Crystal top: 30 tris
- **Total:** 50 tris

**Eyepatch:**
- Simple plane: 4 tris

**TOTAL MODEL:** ~1000 tris (KayKit-compatible!)

### RIGGING (KAYKIT-STYLE)

**Skeleton Structure:**
```
Root
├── Hips
│   ├── Spine
│   │   ├── Chest
│   │   │   ├── Neck
│   │   │   │   └── Head
│   │   │   ├── LeftShoulder
│   │   │   │   ├── LeftArm
│   │   │   │   │   ├── LeftForearm
│   │   │   │   │   │   └── LeftHand
│   │   │   └── RightShoulder
│   │   │       ├── RightArm
│   │   │       │   ├── RightForearm
│   │   │       │       └── RightHand (+ Staff attach point)
│   ├── LeftUpLeg
│   │   ├── LeftLeg
│   │   │   └── LeftFoot
│   └── RightUpLeg
│       ├── RightLeg
│           └── RightFoot
```

**Bone Count:** 19 bones (Humanoid standard)

**Weight Painting:**
- Simple linear weights
- No complex deformation
- Fast performance

### ANIMATIONS (BASIC SET)

```
1. idle.glb          - Standing still, slight breathing
2. walk.glb          - Simple walk cycle
3. explosion_cast.glb - Dramatic pose, staff raised
4. exhausted.glb     - Collapsed after explosion
5. victory.glb       - Confident pose
```

### TEXTURES (KAYKIT-STYLE)

**Texture Atlas:** 512x512 px (single texture for everything)

**Color Map:**
```
Skin:      #FFE5D9
Hair:      #3D2314
Dress Red: #8B0000
Dress Black: #000000
White Collar: #FFFFFF
Eyes:      #FF0000
Hat:       #8B0000
```

**Materials:**
- Unlit shader (like KayKit)
- Flat colors, no gradients
- Simple eye glow effect

### EXPORT SETTINGS

**Format:** GLB (GLTF Binary)

**Settings:**
- Apply Modifiers: Yes
- Selected Objects Only: Yes
- +Y Up: Yes
- Include Animations: Yes
- Compression: Draco (optional)

**File Size Target:** <5 MB

---

## 🎨 VERSION 2: BLENDER HIGH-DETAIL SPECS

### BODY MESH (HIGH-POLY)

**Subdivision Surface Ready:**
- Base mesh: 5,000 tris
- Subdivided (Level 2): 20,000 tris
- Subdivided (Level 3): 80,000 tris (render only)

**Detailed Features:**
- Detailed face (nose, lips, eyebrows)
- Individual fingers (5 per hand)
- Detailed ears
- Anatomically correct body

**Anatomical Details (Trans-Body):**
```
Hidden Layer (under dress):
├── Penis-Klitoris mesh (3 morphs)
│   ├── Resting: 15cm
│   ├── Erect1: 20cm
│   └── Erect2: 35cm
├── Testicles mesh
└── Vagina mesh

Shape Keys:
- Penis_Rest (default)
- Penis_Erect1 (blend 0.5)
- Penis_Erect2 (blend 1.0)
```

### CLOTHING (SEPARATE MESHES)

**Each piece separate for customization:**

1. **Hat:** 200 tris
2. **Eyepatch:** 50 tris
3. **Dress_Top:** 2,000 tris (with folds)
4. **Dress_Skirt:** 3,000 tris (cloth sim ready)
5. **Cape:** 1,500 tris (cloth sim ready)
6. **Collar:** 500 tris (ruffles)
7. **Sleeves:** 800 tris
8. **Boots:** 600 tris each (1,200 total)
9. **Staff:** 500 tris (detailed wood texture)

**Total Clothing:** ~10,000 tris

**Total Character:** ~30,000 tris (game-ready)

### ADVANCED RIGGING

**Full Humanoid Rig + Extras:**
```
Main Skeleton (52 bones):
├── IK Chains for arms/legs
├── Twist bones for natural deformation
├── Hand bones (individual fingers)
├── Facial bones (eyes, jaw, eyebrows)
└── Breast physics bones

Clothing Bones:
├── Cape bones (3 segments, cloth sim)
├── Skirt bones (8 segments, cloth sim)
└── Hair bones (2 segments per braid)

Prop Bones:
└── Staff (attached to RightHand with constraint)
```

**Weight Painting:**
- Automatic weights + manual refinement
- Corrective shape keys for extreme poses
- Breast physics (soft body or bone-based)

### ADVANCED ANIMATIONS

```
Core Set (12 animations):
1. idle_neutral.fbx
2. idle_excited.fbx (bouncing)
3. walk_cycle.fbx
4. run_cycle.fbx
5. explosion_cast_full.fbx (with chant poses)
6. exhausted_collapse.fbx
7. carried_pose.fbx (被抱着)
8. victory_pose.fbx
9. embarrassed.fbx (blush, fidget)
10. angry.fbx (puffed cheeks)
11. sleep.fbx
12. attack_staff_swing.fbx
```

**Facial Animations (Shape Keys):**
```
Face Morphs (20 shape keys):
├── Smile, Frown, Pout
├── Eye_Blink_L, Eye_Blink_R
├── Eye_Wide, Eye_Squint
├── Mouth_Open, Mouth_A, Mouth_O, Mouth_E
├── Eyebrow_Raised_L, Eyebrow_Raised_R
├── Blush (texture swap)
└── Sweat_Drop (texture swap)
```

### TEXTURES (HIGH-DETAIL)

**PBR Texture Set (4K resolution):**

1. **BaseColor:** 4096x4096 px
2. **Normal Map:** 4096x4096 px
3. **Roughness:** 2048x2048 px
4. **Metallic:** 2048x2048 px (mostly 0, except buckles)
5. **Emission:** 2048x2048 px (glowing eyes, magic effects)

**Texture Maps Needed:**
```
Body:
- najika_body_basecolor.png
- najika_body_normal.png
- najika_body_roughness.png

Face:
- najika_face_basecolor.png
- najika_face_normal.png (skin detail)
- najika_face_emission.png (eye glow)

Clothing:
- najika_dress_basecolor.png (fabric patterns)
- najika_dress_normal.png (fabric wrinkles)
- najika_dress_roughness.png

Hair:
- najika_hair_basecolor.png
- najika_hair_alpha.png (hair transparency)

Accessories:
- najika_accessories_basecolor.png (hat, staff, eyepatch)
```

**Material Setup (Shader Nodes):**
```
Principled BSDF:
├── Base Color: BaseColor texture
├── Roughness: Roughness texture
├── Normal: Normal Map node
├── Emission: Emission texture (eyes)
└── Alpha: Alpha texture (hair transparency)
```

### CLOTH SIMULATION

**Physics-Ready Meshes:**

**Cape:**
- Vertex Groups: Pinned (shoulders), Free (rest)
- Settings: Medium weight, high stiffness
- Wind force field for dramatic flow

**Skirt:**
- Vertex Groups: Pinned (waist), Free (hem)
- Settings: Light weight, low stiffness
- Collision with legs

**Hair (Braids):**
- Vertex Groups: Pinned (head), Free (tips)
- Settings: Light weight, medium stiffness
- Swaying motion

### ADVANCED FEATURES

**Subsurface Scattering (Skin):**
```
Skin Shader:
├── Subsurface Scattering: 0.1
├── Subsurface Radius: (1.0, 0.5, 0.3) RGB
└── Subsurface Color: Slight red tint
```

**Hair Shader:**
```
Hair BSDF:
├── Anisotropic reflection
├── Multiple color tones (brown highlights)
└── Transparency for strand tips
```

**Eye Shader:**
```
Eye Material:
├── Cornea (glossy, refractive)
├── Iris (red texture, detailed)
├── Pupil (black, depth)
└── Emission (slight glow)
```

**Magic Effects:**
```
Staff Crystal:
├── Emission: Red glow
├── Transparency: Glass-like
└── Volume Scatter (optional)

Explosion VFX:
├── Particle system (fire/smoke)
├── Emission shader (orange/red)
└── Dynamic paint (ground scorch)
```

---

## 📦 EXPORT FORMATS

### FOR GAME (Real-time):
```
najika_kaykit.glb        - KayKit version (~1000 tris)
najika_game_lod0.glb     - High-detail (~30,000 tris)
najika_game_lod1.glb     - Medium (~15,000 tris)
najika_game_lod2.glb     - Low (~5,000 tris)
```

### FOR BLENDER (Editing):
```
najika_master.blend      - Full Blender file
najika_rig.blend         - Rigged character only
najika_animations.blend  - Animation library
```

### FOR OTHER TOOLS:
```
najika_highpoly.fbx      - For Unity/Unreal
najika_lowpoly.obj       - For general 3D tools
najika_textures/         - Folder with all PNGs
```

---

## 🎮 INTEGRATION INTO NAJIKA SYSTEM

### CURRENT SYSTEM (KayKit Assets):

**Location:** `C:\NajikaCore\assets\kaykit\`

**Add Najika:**
```
assets/
├── kaykit/
│   ├── characters/
│   │   ├── najika_kaykit.glb          ← NEW!
│   │   ├── najika_idle.glb            ← NEW!
│   │   ├── najika_walk.glb            ← NEW!
│   │   └── najika_explosion_cast.glb  ← NEW!
```

**Update 3D Scene:**
```javascript
// In digivice/js/3d_scene.js

function loadNajikaCharacter() {
    const loader = new GLTFLoader();

    loader.load('/assets/kaykit/characters/najika_kaykit.glb', (gltf) => {
        const najika = gltf.scene;
        najika.scale.set(0.7, 0.7, 0.7); // Scale for 140cm
        najika.position.set(0, 0, 0);

        scene.add(najika);

        // Load animations
        const mixer = new THREE.AnimationMixer(najika);
        gltf.animations.forEach((clip) => {
            mixer.clipAction(clip).play();
        });
    });
}
```

---

## 🛠️ BLENDER WORKFLOW

### STEP 1: BASE MESH (KayKit Version)

```
1. Create base body:
   - Cube → Subdivide → Shape into chibi body
   - Keep poly count ~800 tris

2. Add clothing:
   - Extrude dress from body
   - Simple hat cone
   - Flat cape rectangle

3. UV Unwrap:
   - Smart UV Project
   - Pack islands
   - Export UV layout

4. Texture painting:
   - Flat colors in Texture Paint mode
   - No shading/lighting baked

5. Rig:
   - Add Armature (Humanoid)
   - Auto-weight paint
   - Test pose

6. Export:
   - File → Export → GLB
   - Include animations
```

### STEP 2: HIGH-DETAIL MESH (Later)

```
1. Import KayKit base as reference
2. Model high-detail body:
   - Start with Metaball/Sculpt
   - Retopology for clean mesh
   - Subdivision surface modifier

3. Model clothing separately:
   - Each piece own object
   - Real fabric folds (sculpt)
   - Clean topology for deformation

4. UV Unwrap (detailed):
   - Seams at hidden areas
   - Maximum texture space usage
   - Multiple UDIM tiles (optional)

5. Texture painting (PBR):
   - BaseColor in Substance Painter / Blender
   - Normal map from sculpt (bake)
   - Roughness map painted

6. Advanced rigging:
   - Rigify add-on (auto-rig)
   - Custom face bones
   - Physics bones for cloth

7. Animations:
   - Key all 12 core animations
   - Bake physics simulations
   - Export each as separate FBX

8. Final export:
   - Master blend file
   - GLB for web
   - FBX for game engines
```

---

## 📋 CHECKLIST FOR 3D ARTIST

### KAYKIT VERSION (PRIORITY 1):
- [ ] Model base body (800 tris)
- [ ] Model clothing integrated (200 tris)
- [ ] Create simple hat + cape
- [ ] UV unwrap (single 512x512 atlas)
- [ ] Texture paint (flat colors)
- [ ] Rig (19 bones humanoid)
- [ ] Weight paint (automatic)
- [ ] Animate: idle, walk, explosion_cast
- [ ] Export GLB (<5 MB)
- [ ] Test in Najika system

### BLENDER HIGH-DETAIL (PRIORITY 2):
- [ ] Model detailed body (5,000 base tris)
- [ ] Model separate clothing pieces
- [ ] Add anatomical details (hidden layer)
- [ ] UV unwrap (detailed, 4K ready)
- [ ] Create PBR textures (4K resolution)
- [ ] Advanced rig (52 bones + face)
- [ ] Weight paint (manual refinement)
- [ ] Create all 12 animations
- [ ] Add facial shape keys (20 morphs)
- [ ] Setup cloth simulation (cape/skirt)
- [ ] Export all formats (GLB, FBX, OBJ)
- [ ] Create LOD versions (3 levels)

---

## 💾 FILE ORGANIZATION

```
C:\NajikaCore\
├── assets/
│   ├── kaykit/
│   │   └── characters/
│   │       ├── najika_kaykit.glb
│   │       ├── najika_idle.glb
│   │       └── najika_walk.glb
│   └── najika_3d/
│       ├── blender/
│       │   ├── najika_master.blend
│       │   ├── najika_rig.blend
│       │   └── najika_animations.blend
│       ├── exports/
│       │   ├── najika_game_lod0.glb
│       │   ├── najika_game_lod1.glb
│       │   ├── najika_game_lod2.glb
│       │   └── najika_highpoly.fbx
│       └── textures/
│           ├── najika_body_basecolor.png (4K)
│           ├── najika_body_normal.png (4K)
│           ├── najika_dress_basecolor.png (4K)
│           └── ... (all texture files)
```

---

**Ende der 3D Model Specifications**

**NÄCHSTER SCHRITT:**
Willst du dass ich dir ein Blender Python-Script erstelle das automatisch das KayKit-Base-Mesh generiert? Oder brauchst du eine visuelle Anleitung mit Screenshots?
