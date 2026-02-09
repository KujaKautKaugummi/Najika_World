// 🎬 CHARACTER ANIMATION SYSTEM
// Lädt und verwaltet Character Animationen aus KayKit AnimatedCharacter Pack
// Animations: Idle, Walk, Run, Attack(1h), AttackCombo, AttackSpinning, HeavyAttack,
//             Block, Roll, DashFront/Back/Left/Right, Jump, Hop, Defeat, Cheer, Dance, Wave, etc.

window.CharacterAnimations = {
    mixer: null,
    animations: {},
    currentAction: null,
    currentName: '',
    characterModel: null,
    isLocked: false,        // Animation-Lock (z.B. während Attack)
    lockTimer: null,

    // KayKit Animation-Name-Mapping (lowercase clip name → game action)
    NAME_MAP: {
        'idle': 'idle',
        'walk': 'walk',
        'run': 'run',
        'jump': 'jump',
        'hop': 'hop',
        'roll': 'roll',
        'block': 'block',
        'cheer': 'cheer',
        'dance': 'dance',
        'wave': 'wave',
        'defeat': 'defeat',
        'climb': 'climbing',
        'climbing': 'climbing',
        'interact': 'interact',
        'pickup': 'pickup',
        'throw': 'throw',
        'layingdownidle': 'layingdownidle',
        // Attack variants
        'attack(1h)': 'attack',
        'attack': 'attack',
        'attackcombo': 'attackcombo',
        'attackspinning': 'attackspinning',
        'heavyattack': 'heavyattack',
        // Shoot/Cast variants
        'shoot(1h)': 'cast',
        'shoot(2h)': 'cast2h',
        'shoot(2h)bow': 'shootbow',
        'shooting(1h)': 'casting',
        'shooting(2h)': 'casting2h',
        // Dash variants
        'dashfront': 'dashfront',
        'dashback': 'dashback',
        'dashleft': 'dashleft',
        'dashright': 'dashright'
    },

    init: function(characterGroup, gltf) {
        this.characterModel = characterGroup;
        this.mixer = new THREE.AnimationMixer(characterGroup);
        this.animations = {};
        this.currentAction = null;
        this.currentName = '';
        this.isLocked = false;

        if (gltf.animations && gltf.animations.length > 0) {
            console.log(`🎬 Gefunden: ${gltf.animations.length} Animationen`);

            gltf.animations.forEach(clip => {
                // Originalen Clip-Namen als Key (lowercase, ohne Leerzeichen)
                const rawName = clip.name.toLowerCase().replace(/\s+/g, '');
                this.animations[rawName] = this.mixer.clipAction(clip);

                // Mapped Name auch registrieren
                const mapped = this.NAME_MAP[rawName];
                if (mapped && mapped !== rawName) {
                    this.animations[mapped] = this.mixer.clipAction(clip);
                }

                console.log(`  🎬 ${clip.name} → ${rawName}${mapped ? ' (→' + mapped + ')' : ''}`);
            });

            // Starte Idle als Default
            if (this.animations['idle']) {
                this.playAnimation('idle');
            }
        } else {
            console.warn('⚠️ Keine Animationen in GLTF gefunden!');
        }
    },

    playAnimation: function(name, loop = true, fadeTime = 0.2) {
        if (!this.mixer) return;
        name = name.toLowerCase();

        // Wenn Animation-Lock aktiv, nur unlock-fähige Animationen erlauben
        if (this.isLocked && name !== 'defeat') return;

        const action = this.animations[name];
        if (!action) return;

        // Gleiche Animation nicht neu starten
        if (this.currentName === name && this.currentAction?.isRunning()) return;

        // Fade aus aktueller Animation
        if (this.currentAction && this.currentAction !== action) {
            this.currentAction.fadeOut(fadeTime);
        }

        // Fade in neue Animation
        action.reset();
        action.fadeIn(fadeTime);
        action.setLoop(loop ? THREE.LoopRepeat : THREE.LoopOnce);
        if (!loop) action.clampWhenFinished = true;
        action.play();

        this.currentAction = action;
        this.currentName = name;
    },

    // Einmalige Animation abspielen, dann zurück zu vorheriger
    playOnce: function(name, duration, returnTo) {
        if (!this.mixer || this.isLocked) return;
        name = name.toLowerCase();
        returnTo = (returnTo || 'idle').toLowerCase();

        const action = this.animations[name];
        if (!action) return;

        // Lock setzen
        this.isLocked = true;
        if (this.lockTimer) clearTimeout(this.lockTimer);

        // Animation abspielen
        if (this.currentAction && this.currentAction !== action) {
            this.currentAction.fadeOut(0.1);
        }

        action.reset();
        action.fadeIn(0.1);
        action.setLoop(THREE.LoopOnce);
        action.clampWhenFinished = true;
        action.play();

        this.currentAction = action;
        this.currentName = name;

        // Nach Duration zurück zur Return-Animation
        const ms = (duration || 0.6) * 1000;
        this.lockTimer = setTimeout(() => {
            this.isLocked = false;
            this.playAnimation(returnTo, true, 0.15);
        }, ms);
    },

    update: function(delta) {
        if (this.mixer) {
            this.mixer.update(delta);
        }
    },

    // ==========================================
    // COMBAT ANIMATION HELPERS
    // ==========================================

    playAttack: function(type) {
        const anim = type === 'heavy' ? 'heavyattack' :
                     type === 'combo' ? 'attackcombo' :
                     type === 'spin'  ? 'attackspinning' : 'attack';
        this.playOnce(anim, type === 'heavy' ? 0.8 : 0.5);
    },

    playDodge: function(direction) {
        const anim = direction === 'back' ? 'dashback' :
                     direction === 'left' ? 'dashleft' :
                     direction === 'right' ? 'dashright' : 'roll';
        this.playOnce(anim, 0.5);
    },

    playBlock: function() {
        this.playOnce('block', 0.4);
    },

    playCast: function() {
        this.playOnce('cast', 0.7);
    },

    playHit: function() {
        // Kurzer Rückstoß - kein Lock, nur schnelle Animation
        if (this.isLocked) return;
        const action = this.animations['hop'];
        if (!action) return;
        if (this.currentAction) this.currentAction.fadeOut(0.05);
        action.reset();
        action.fadeIn(0.05);
        action.setLoop(THREE.LoopOnce);
        action.clampWhenFinished = true;
        action.play();
        this.currentAction = action;
        this.currentName = 'hop';
        setTimeout(() => {
            if (this.currentName === 'hop') {
                this.playAnimation('idle', true, 0.1);
            }
        }, 300);
    },

    playDefeat: function() {
        this.isLocked = false; // Override lock
        this.playAnimation('defeat', false, 0.3);
        this.isLocked = true;  // Lock nach defeat
    },

    playCheer: function() {
        this.playOnce('cheer', 1.5);
    },

    // Bewegungs-State-Helper
    getAnimationForState: function(isMoving, isRunning, isJumping, isDucking, isAttacking, isBlocking) {
        if (isAttacking) return 'attack';
        if (isBlocking) return 'block';
        if (isJumping) return 'jump';
        if (isRunning) return 'run';
        if (isMoving) return 'walk';
        return 'idle';
    },

    // Bewege-Animation basierend auf Movement-State
    updateMovement: function(hasInput, isSprinting, isSliding) {
        if (this.isLocked) return;

        let target;
        if (isSliding) {
            target = 'dashfront';
        } else if (hasInput && isSprinting) {
            target = 'run';
        } else if (hasInput) {
            target = 'walk';
        } else {
            target = 'idle';
        }

        if (this.currentName !== target) {
            this.playAnimation(target);
        }
    },

    listAnimations: function() {
        return Object.keys(this.animations);
    },

    isReady: function() {
        return this.mixer !== null && Object.keys(this.animations).length > 0;
    }
};

console.log('🎬 Character Animation System loaded!');
