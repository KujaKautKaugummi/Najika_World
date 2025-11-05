# NAJIKA FINAL DESIGN - KORRIGIERT

**Basis:** Image #3 (1:1 Übernahme)
**Plus:** Megumin-Accessoires (Stab, Verband)
**Änderung:** Socken kurz statt lang

---

## ✅ VOM BILD 1:1 ÜBERNOMMEN

### GESICHT & KOPF
- **BEIDE Augen sichtbar** (rot/golden, große Anime-Augen)
- **KEINE Augenklappe!**
- Süßes, kindliches Gesicht
- Kleine Nase, süßer Mund
- Leicht gerötete Wangen

### HAARE
- Farbe: Dunkelbraun (kastanienbraun)
- Stil: Zwei lange Zöpfe an den Seiten
- Länge: Bis zur Hüfte
- Textur: Glatt, glänzend

### HUT
- Großer spitzer Hexenhut (Megumin-Original-Design!)
- Farbe: Burgundrot/dunkelrot
- Schwarzes Band um die Krone
- Sehr groß, dominant

### OUTFIT
- **Gothic-Lolita Kleid (rot-schwarz-weiß)**
- Weißer hoher Rüschenkragen
- Kurze rote Puffärmel
- Lange schwarze Ärmel darunter (mit roten Details)
- Schwarze Schnürung vorne (Corset-Style)
- Roter Cape/Umhang (schwarz innen)
- Kurzer A-Line Rock (rot-schwarz gemustert)

### KÖRPER & PROPORTIONEN (VOM BILD!)
- Körpergröße: 140 cm (sehr klein, Loli)
- Zierliche Figur
- Schmale Schultern
- Kleine Taille
- Leicht breitere Hüften (cute proportions)
- Zarte Arme und Beine

### POSE (VOM BILD!)
- Aufrecht stehend
- Selbstbewusst
- Arme vor dem Körper (eine Hand leicht angehoben)
- Leichte Hüftverschiebung (dynamisch)

---

## ➕ MEGUMIN-ELEMENTE HINZUGEFÜGT

### STAB/ZAUBERSTAB (NEU!)
- **Position:** In rechter Hand (oder beide Hände)
- **Länge:** ~120 cm (fast so groß wie Najika)
- **Design:** Megumin's Original Staff
  - Dunkles Holz (braun/schwarz)
  - Roter Kristall/Edelstein oben
  - Metallbänder/Verzierungen
- **Haltung:** Aufrecht oder leicht schräg

### VERBAND AM BEIN (NEU!)
- **Position:** Linkes Bein, Unterschenkel
- **Farbe:** Weiß (Bandage-Style)
- **Stil:** Gewickelt, wie Megumin Original
- **Länge:** Von Knie bis mittlerer Unterschenkel

---

## ❌ DEINE ÄNDERUNG

### SOCKEN
**Im Original-Bild:** Lange rot-schwarz gestreifte Overknee-Socken

**ÄNDERUNG:**
- ❌ Keine langen Socken
- ✅ Kurze Knöchelsocken (nicht sichtbar)
- ✅ Nackte Beine von Knie bis Knöchel sichtbar
- ✅ Nur Verband am linken Bein sichtbar

### SCHUHE (VOM BILD)
- Schwarze Stiefeletten/Mary Janes
- Knöchelhoch
- Rote Details/Schnallen
- Gothic-Stil

---

## 🎨 FINALE BESCHREIBUNG

**NAJIKA sieht aus wie:**

Ein 140cm großes, süßes Gothic-Lolita Mädchen:
- **Gesicht:** Beide großen roten Augen sichtbar, süß, kindlich
- **Hut:** Riesiger roter Hexenhut (Megumin-Style)
- **Haare:** Lange braune Zöpfe bis zur Hüfte
- **Outfit:** Rot-schwarz-weißes Gothic-Lolita Kleid mit Cape
- **Stab:** Großer Zauberstab mit rotem Kristall in Hand
- **Beine:** Nackt sichtbar, Verband am linken Unterschenkel
- **Schuhe:** Schwarze Stiefeletten
- **Pose:** Selbstbewusst, dramatisch, hält Stab

**= Perfekte Mischung aus dem Bild + Megumin-Elementen!**

---

## 📐 3D-MODELL SPEZIFIKATION FÜR DIGIVICE

### TECHNISCHE DETAILS

**Format:** GLB (GLTF Binary)
**Poly Count:** ~1000-1500 Tris (KayKit-kompatibel)
**Textures:** 512x512 Single Atlas
**Rigging:** Standard Humanoid (19 bones)

### MESH-KOMPONENTEN

```
najika_kaykit.glb:
├── Body (base mesh)
│   ├── Head + Face
│   ├── Torso
│   ├── Arms
│   └── Legs
├── Clothing (integrated)
│   ├── Dress
│   ├── Collar
│   ├── Sleeves
│   └── Cape
├── Hair (2 braids)
├── Hat (large witch hat)
├── Staff (held in hand)
├── Bandage (left leg)
└── Shoes

Total: ~1200 tris
```

### PROPORTIONS (140cm)

```
Height breakdown:
├── Head: 20cm (14%) - cute chibi proportions
├── Torso: 40cm (29%)
├── Arms: 35cm (25%)
└── Legs: 45cm (32%)

Scale in scene: 0.7x (to match 140cm vs 200cm default)
```

### FARBEN

```
Skin:        #FFE5D9 (pale)
Hair:        #3D2314 (dark brown)
Eyes:        #FF0000 (red, glowing)
Dress_Red:   #8B0000 (burgundy)
Dress_Black: #000000
Collar:      #FFFFFF (white ruffles)
Cape:        #8B0000 outer, #000000 inner
Hat:         #8B0000 (burgundy)
Staff_Wood:  #3D2314 (dark brown)
Staff_Crystal: #FF0000 (glowing red)
Bandage:     #F5F5F5 (white)
Shoes:       #000000 (black)
```

### RIGGING

```
Armature (19 bones):
Root
├── Hips
│   ├── Spine
│   │   ├── Chest
│   │   │   ├── Neck
│   │   │   │   └── Head
│   │   │   ├── LeftShoulder
│   │   │   │   └── LeftArm
│   │   │   │       └── LeftForearm
│   │   │   │           └── LeftHand
│   │   │   └── RightShoulder
│   │   │       └── RightArm
│   │   │           └── RightForearm
│   │   │               └── RightHand
│   │   │                   └── Staff_Attach (empty)
│   ├── LeftUpLeg
│   │   └── LeftLeg
│   │       └── LeftFoot
│   └── RightUpLeg
│       └── RightLeg
│           └── RightFoot
```

### ANIMATIONS

```
najika_idle.glb        - Standing idle, slight breathing
najika_walk.glb        - Walking cycle
najika_explosion.glb   - Casting explosion (staff raised)
najika_exhausted.glb   - Collapsed after explosion
najika_victory.glb     - Victory pose (confident)
```

---

## 🛠️ BLENDER CREATION SCRIPT

Hier ist ein Python-Script das das Base-Model automatisch in Blender erstellt:

```python
# najika_base_generator.py
# Run in Blender: Alt+P in Text Editor

import bpy
import bmesh
from mathutils import Vector

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# === CREATE BASE BODY ===

def create_body():
    """Creates low-poly body mesh"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.7))
    body = bpy.context.active_object
    body.name = "Najika_Body"

    # Scale for proportions (140cm total)
    body.scale = (0.15, 0.1, 0.4)  # Narrow, thin, tall torso

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=2)
    bpy.ops.object.mode_set(mode='OBJECT')

    return body

def create_head():
    """Creates head with simple features"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0, 1.2))
    head = bpy.context.active_object
    head.name = "Najika_Head"
    head.scale = (1, 0.9, 1.1)  # Slightly oval

    return head

def create_eyes():
    """Creates glowing eyes"""
    # Left eye
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(-0.03, -0.08, 1.22))
    left_eye = bpy.context.active_object
    left_eye.name = "Eye_Left"

    # Right eye
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(0.03, -0.08, 1.22))
    right_eye = bpy.context.active_object
    right_eye.name = "Eye_Right"

    # Add emission material
    for eye in [left_eye, right_eye]:
        mat = bpy.data.materials.new(name="Eye_Red")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()

        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs[0].default_value = (1, 0, 0, 1)  # Red
        emission.inputs[1].default_value = 2.0  # Strength

        output = nodes.new(type='ShaderNodeOutputMaterial')
        mat.node_tree.links.new(emission.outputs[0], output.inputs[0])

        eye.data.materials.append(mat)

def create_hair_braids():
    """Creates simple hair braids"""
    # Left braid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.8, location=(-0.08, 0, 0.8))
    left_braid = bpy.context.active_object
    left_braid.name = "Hair_Braid_Left"
    left_braid.rotation_euler = (0.3, 0, 0)

    # Right braid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.8, location=(0.08, 0, 0.8))
    right_braid = bpy.context.active_object
    right_braid.name = "Hair_Braid_Right"
    right_braid.rotation_euler = (0.3, 0, 0)

def create_hat():
    """Creates witch hat"""
    bpy.ops.mesh.primitive_cone_add(radius1=0.15, depth=0.4, location=(0, 0, 1.4))
    hat = bpy.context.active_object
    hat.name = "Hat"
    hat.rotation_euler = (0, 0, 0)

def create_dress():
    """Creates simple dress"""
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.4, location=(0, 0, 0.6))
    dress = bpy.context.active_object
    dress.name = "Dress"

    # Taper bottom for A-line
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(dress.data)
    for v in bm.verts:
        if v.co.z < 0:  # Bottom vertices
            v.co.x *= 1.5
            v.co.y *= 1.5
    bmesh.update_edit_mesh(dress.data)
    bpy.ops.object.mode_set(mode='OBJECT')

def create_cape():
    """Creates flowing cape"""
    bpy.ops.mesh.primitive_plane_add(size=0.3, location=(0, 0.05, 0.9))
    cape = bpy.context.active_object
    cape.name = "Cape"
    cape.rotation_euler = (0.3, 0, 0)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=3)
    bpy.ops.object.mode_set(mode='OBJECT')

def create_staff():
    """Creates magic staff"""
    # Staff body
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=1.2, location=(0.2, 0, 0.6))
    staff = bpy.context.active_object
    staff.name = "Staff"

    # Crystal top
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.03, location=(0.2, 0, 1.2))
    crystal = bpy.context.active_object
    crystal.name = "Staff_Crystal"

    # Red emission for crystal
    mat = bpy.data.materials.new(name="Crystal_Red")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs[0].default_value = (1, 0, 0, 1)
    emission.inputs[1].default_value = 3.0

    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])

    crystal.data.materials.append(mat)

def create_bandage():
    """Creates leg bandage"""
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.15, location=(-0.08, 0, 0.35))
    bandage = bpy.context.active_object
    bandage.name = "Bandage_Left_Leg"

def create_legs():
    """Creates legs"""
    # Left leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.45, location=(-0.08, 0, 0.225))
    left_leg = bpy.context.active_object
    left_leg.name = "Leg_Left"

    # Right leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.45, location=(0.08, 0, 0.225))
    right_leg = bpy.context.active_object
    right_leg.name = "Leg_Right"

def create_arms():
    """Creates arms"""
    # Left arm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.35, location=(-0.18, 0, 0.8))
    left_arm = bpy.context.active_object
    left_arm.name = "Arm_Left"
    left_arm.rotation_euler = (0, 0.3, 0)

    # Right arm (holding staff)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.35, location=(0.18, 0, 0.8))
    right_arm = bpy.context.active_object
    right_arm.name = "Arm_Right"
    right_arm.rotation_euler = (0, -0.5, 0)

# === CREATE ALL PARTS ===
body = create_body()
head = create_head()
create_eyes()
create_hair_braids()
create_hat()
create_dress()
create_cape()
create_staff()
create_bandage()
create_legs()
create_arms()

# === JOIN ALL MESHES ===
bpy.ops.object.select_all(action='SELECT')
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()

najika = bpy.context.active_object
najika.name = "Najika_Complete"

# === ADD ARMATURE ===
bpy.ops.object.armature_add(location=(0, 0, 0))
armature = bpy.context.active_object
armature.name = "Najika_Rig"

# === PARENT MESH TO ARMATURE ===
najika.select_set(True)
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

print("✓ Najika base model created!")
print("Next steps:")
print("1. UV Unwrap (U > Smart UV Project)")
print("2. Texture Paint (flat colors)")
print("3. Refine rigging (weight paint)")
print("4. Add animations")
print("5. Export as GLB")
```

---

## 📦 INTEGRATION INS DIGIVICE

### SCHRITT 1: Modell exportieren

```
In Blender:
1. File → Export → glTF 2.0 (.glb)
2. Settings:
   - Format: GLB (Binary)
   - Include: Selected Objects
   - Transform: +Y Up
   - Compression: Draco (optional)
3. Save as: najika_kaykit.glb
```

### SCHRITT 2: In Assets kopieren

```bash
# Kopiere nach:
C:\NajikaCore\assets\kaykit\characters\najika_kaykit.glb
```

### SCHRITT 3: Code updaten

In `C:\NajikaCore\digivice\js\3d_scene.js`:

```javascript
// Nach loadCharacter() Funktion hinzufügen:

function loadNajika() {
    const loader = new THREE.GLTFLoader();

    loader.load('/assets/kaykit/characters/najika_kaykit.glb', (gltf) => {
        const najika = gltf.scene;

        // Scale for 140cm height
        najika.scale.set(0.7, 0.7, 0.7);

        // Position in scene
        najika.position.set(0, 0, 0);

        // Add to scene
        scene.add(najika);

        // Store reference
        window.najikaCharacter = najika;

        // Load animations if included
        if (gltf.animations && gltf.animations.length > 0) {
            const mixer = new THREE.AnimationMixer(najika);
            gltf.animations.forEach((clip) => {
                const action = mixer.clipAction(clip);
                action.play();
            });
            window.najikaMixer = mixer;
        }

        console.log('✓ Najika loaded!');
    }, undefined, (error) => {
        console.error('✗ Error loading Najika:', error);
    });
}

// Call it after scene setup:
loadNajika();
```

### SCHRITT 4: Animation Loop

```javascript
// In render() function:

function render() {
    requestAnimationFrame(render);

    // Update Najika animations
    if (window.najikaMixer) {
        const delta = clock.getDelta();
        window.najikaMixer.update(delta);
    }

    renderer.render(scene, camera);
}
```

---

## ✅ FERTIG!

Jetzt hast du:
1. ✅ Korrekte visuelle Specs (Bild 1:1 + Megumin-Accessoires)
2. ✅ 3D-Modell Specs (KayKit-kompatibel)
3. ✅ Blender Script (automatische Erstellung)
4. ✅ Integration ins Digivice (Code-Snippets)

**Najika ist bereit für das Digivice-System!** 🎉
