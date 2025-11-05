// 🎬 CHARACTER ANIMATION SYSTEM
// Lädt und verwaltet Character Animationen aus KayKit AnimatedCharacter Pack

window.CharacterAnimations = {
    mixer: null,
    animations: {},
    currentAction: null,
    characterModel: null,

    init: function(characterGroup, gltf) {
        this.characterModel = characterGroup;
        this.mixer = new THREE.AnimationMixer(characterGroup);

        // Extrahiere alle Animations-Clips
        if (gltf.animations && gltf.animations.length > 0) {
            console.log(`🎬 Gefunden: ${gltf.animations.length} Animationen`);

            gltf.animations.forEach(clip => {
                const name = clip.name.toLowerCase();
                this.animations[name] = this.mixer.clipAction(clip);
                console.log(`  - ${clip.name}`);
            });

            // Starte Idle als Default
            this.playAnimation('idle');
        } else {
            console.warn('⚠️ Keine Animationen in GLTF gefunden!');
        }
    },

    playAnimation: function(name, loop = true, fadeTime = 0.2) {
        name = name.toLowerCase();

        if (!this.animations[name]) {
            console.warn(`Animation "${name}" nicht gefunden!`);
            return;
        }

        const newAction = this.animations[name];

        // Fade aus aktueller Animation
        if (this.currentAction && this.currentAction !== newAction) {
            this.currentAction.fadeOut(fadeTime);
        }

        // Fade in neue Animation
        newAction.reset();
        newAction.fadeIn(fadeTime);
        newAction.setLoop(loop ? THREE.LoopRepeat : THREE.LoopOnce);
        newAction.play();

        this.currentAction = newAction;
    },

    update: function(delta) {
        if (this.mixer) {
            this.mixer.update(delta);
        }
    },

    // Hilfsfunktion: Welche Animation sollte gespielt werden?
    getAnimationForState: function(isMoving, isRunning, isJumping, isDucking, isAttacking, isBlocking) {
        if (isAttacking) return 'attack';
        if (isBlocking) return 'block';
        if (isDucking) return 'duck';
        if (isJumping) return 'jump';
        if (isRunning) return 'run';
        if (isMoving) return 'walk';
        return 'idle';
    },

    // Liste verfügbarer Animationen
    listAnimations: function() {
        return Object.keys(this.animations);
    }
};

console.log('🎬 Character Animation System loaded!');
