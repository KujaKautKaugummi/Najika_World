# NAJIKA CHARACTER - THREE.JS INTEGRATION GUIDE

**Stand:** 2026-02-11
**Three.js Version:** r128
**Model-Pack:** KayKit AnimatedCharacter v1.2

---

## ARCHITEKTUR

```
index.html (159 Scripts)
    |
    +-- companion_3d.js        (Najika 3D Companion - Follow System)
    +-- character_animations.js (Animation Mixer + 40 Animationen)
    +-- kaykit_loader.js       (Asset Loading)
    +-- 3d_scene.js            (Hauptszene + Raum-Builder)
    |
    +-- world/                 (Welt-Rendering)
    |   +-- terrain_generator.js
    |   +-- biome_system.js
    |   +-- weather_system.js
    |   +-- day_night_cycle.js
    |   +-- lod_manager.js
    |
    +-- particles/             (VFX)
    |   +-- combat_particles.js
    |   +-- magic_particles.js
    |   +-- environment_particles.js
    |   +-- evolution_effects.js
    |
    +-- combat/
        +-- real_3d_combat.js  (3D Kampf-Rendering)
```

---

## NAJIKA 3D COMPANION

### Datei: `digivice/js/companion_3d.js`

### Config
```javascript
const COMPANION_CONFIG = {
    modelPath: 'static/assets/KayKit Character Animations 1.2/.../KayKit_AnimatedCharacter_v1.2.glb',
    scale: 0.7,              // Kleiner als Spieler (1.0)
    followDistance: 3.5,     // Abstand zum Spieler
    followSpeed: 5.0,       // Geschwindigkeit
    catchUpSpeed: 9.0,      // Aufhol-Speed wenn zu weit
    maxDistance: 15,         // Teleport-Schwelle
    offsetAngle: -0.6,      // Links-hinter dem Spieler
    tintColor: 0xE91E63,    // Pink/Rosa Tint
    nameColor: '#E91E63',
};
```

### Laden
```javascript
// GLTFLoader laedt KayKit AnimatedCharacter GLB
const loader = new THREE.GLTFLoader();
loader.load(COMPANION_CONFIG.modelPath, gltf => {
    companionModel = gltf.scene;
    companionModel.scale.setScalar(0.7);

    // Pink-Tint fuer Najika
    companionModel.traverse(node => {
        if (node.isMesh && node.material) {
            const mat = node.material.clone();
            mat.color.lerp(new THREE.Color(0xE91E63), 0.45);
            mat.emissive = new THREE.Color(0x2e0a1a);
            node.material = mat;
        }
    });

    // AnimationMixer
    companionMixer = new THREE.AnimationMixer(companionModel);

    scene.add(companionGroup);
});
```

### Follow-System
- Najika folgt dem Spieler (`window.gameCharacter`)
- Abstand: 3.5 Einheiten, leicht links-hinter
- Aufhol-Modus bei > followDistance
- Teleport bei > maxDistance (15)
- Idle-Animation wenn Spieler steht
- Walk/Run-Animation wenn Spieler sich bewegt

### Animation-Trigger vom Backend
```javascript
// Backend sendet Animation-Hooks im Chat-Response:
// { "hooks": [{"type": "ANIMATION", "content": "cheer"}] }

// Frontend empfaengt und spielt ab:
function triggerCompanionAnim(animName) {
    // animName: "cheer", "dance", "wave", "idle", etc.
    playCompanionAnimation(animName);
}
```

---

## ANIMATION SYSTEM

### Datei: `digivice/js/character_animations.js`

### Verfuegbare Animationen (40+)
```
BEWEGUNG:
  idle, walk, run, jump, hop, roll, climb

KAMPF:
  attack, attackcombo, attackspinning, heavyattack, block

MAGIE:
  cast (shoot 1h), cast2h (shoot 2h), shootbow
  casting (shooting 1h), casting2h (shooting 2h)

DASH:
  dashfront, dashback, dashleft, dashright

INTERAKTION:
  interact, pickup, throw, layingdownidle

SOZIAL:
  dance, wave, cheer, defeat
```

### Animation abspielen
```javascript
// CharacterAnimations ist global verfuegbar
window.CharacterAnimations.playAnimation('dance');

// Mit Lock (z.B. waehrend Attack):
window.CharacterAnimations.playAnimation('attack', {
    loop: false,
    lockDuration: 800  // ms
});
```

### Mood -> Animation Mapping (Backend)
```python
# backend/najika_server.py oder api/chat.py
mood_animations = {
    "happy": "cheer",
    "excited": "cheer",
    "sad": "wave",
    "angry": "idle",
    "explosive": "cheer",
    "sleepy": "idle",
    "needy": "wave",
    "dominant": "idle",
    "playful": "dance",
    "possessive": "idle",
    "sweet": "cheer",
    "horny": "dance",
    "pouty": "wave",
    "jealous": "idle",
    "loving": "cheer",
}
```

---

## SZENE + RENDERING

### Globale Referenzen
```javascript
// Szene
window.scene          // THREE.Scene
window.Scene3D?.scene // Alternative Referenz

// Kamera
window.camera         // THREE.PerspectiveCamera

// Spieler
window.gameCharacter  // Player Group (KayKit Model)

// Companion (Najika)
// Nicht direkt global, aber via companion_3d.js IIFE
```

### Render-Loop
```javascript
// In index.html oder 3d_scene.js
function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();

    // Spieler-Animationen
    if (CharacterAnimations.mixer) {
        CharacterAnimations.mixer.update(delta);
    }

    // Companion-Animationen
    if (companionMixer) {
        companionMixer.update(delta);
    }

    renderer.render(scene, camera);
}
```

---

## BEKANNTE EINSCHRAENKUNGEN

1. **CapsuleGeometry fehlt** in Three.js r128 (erst ab r143)
   - Workaround: CylinderGeometry oder Sphere fuer Collider

2. **KayKit = Platzhalter** - Das finale Najika-Model (Gothic Lolita) existiert noch nicht
   - Aktuell: Generic KayKit Character mit Pink-Tint
   - Ziel: Custom Najika Skeletal Mesh

3. **Keine Blend-Trees** - Animationen sind diskret (kein Uebergang Walk->Run)
   - THREE.AnimationMixer.crossFadeTo() verfuegbar aber nicht implementiert

4. **Performance** bei vielen NPCs
   - LOD-System vorhanden (`world/lod_manager.js`)
   - Instancing nicht genutzt

---

## SCHRITT-FUER-SCHRITT: Najika Custom Model einbinden

### 1. Model erstellen
- Format: GLB (mit Skeletal Animations)
- Skeleton: Humanoid (kompatibel mit KayKit-Animationen)
- Groesse: ~1m in Blender (Scale 0.7 im Code)
- Style: Gothic Lolita, 11 Jahre, kurze Haare

### 2. Model exportieren
```
Blender -> Export as glTF 2.0 (.glb)
- Include: Mesh + Armature + Animations
- Format: GLB (Binary)
- Speichern: digivice/static/assets/najika/najika_character.glb
```

### 3. companion_3d.js anpassen
```javascript
// Aendere modelPath:
const COMPANION_CONFIG = {
    modelPath: 'static/assets/najika/najika_character.glb',
    scale: 0.7,
    // ... rest bleibt gleich
    tintColor: null,  // Kein Tint noetig bei Custom Model
};
```

### 4. Animationen pruefen
```javascript
// Nach dem Laden loggen welche Animationen vorhanden sind:
gltf.animations.forEach(clip => {
    console.log(`Animation: ${clip.name} (${clip.duration}s)`);
});
// Fehlende Animationen -> character_animations.js NAME_MAP anpassen
```

### 5. Testen
```
http://127.0.0.1:8000/
- Najika sollte neben dem Spieler stehen
- Idle-Animation laeuft
- Chat senden -> Animation-Hook triggert
```

---

## API INTEGRATION

### Chat -> Animation Flow
```
1. User sendet Chat an /api/chat
2. Backend verarbeitet mit NajikaMind
3. NajikaMind bestimmt mood (happy/sad/angry/...)
4. mood -> Animation Mapping
5. Response enthaelt hooks: [{type:"ANIMATION", content:"cheer"}]
6. Frontend empfaengt Response
7. companion_3d.js spielt Animation ab
```

### Beispiel-Response
```json
{
    "response": "*springt auf* KUJA! EXPLOSION!!!",
    "mood": "explosive",
    "personality": "megumin",
    "intent": "observe",
    "hooks": [
        {"type": "ANIMATION", "trigger": "explosive", "content": "Anim_Najika_Happy"}
    ]
}
```

---

*Generiert am 2026-02-11 von Claude Opus*
