/**
 * Combat SFX System
 * Advanced combat sound effects with variations and combos
 * Digimon World battle audio system
 */

// THREE is loaded globally via index.html

class CombatSFXSystem {
    constructor(spatialAudioEngine) {
        this.audioEngine = spatialAudioEngine;
        this.audioContext = spatialAudioEngine.audioContext;
        this.listener = spatialAudioEngine.listener;
        this.audioLoader = new THREE.AudioLoader();

        // Sound library
        this.sounds = new Map();

        // Combo tracking
        this.comboCounts = new Map();
        this.lastHitTime = new Map();
        this.comboResetDelay = 2000; // ms

        // Sound variation tracking
        this.lastPlayedVariations = new Map();

        // Configuration
        this.config = {
            enableCombos: true,
            comboVolumeBoost: 0.15,
            comboPitchIncrease: 0.05,
            maxCombo: 20,
            criticalPitchShift: 0.2,
            randomPitchVariation: 0.1
        };

        this.initializeSoundLibrary();

        console.log('💥 Combat SFX System initialized');
    }

    /**
     * Initialize sound library
     */
    initializeSoundLibrary() {
        // Hit sounds with variations
        this.registerSoundVariations('hit', [
            'hit_punch_1',
            'hit_punch_2',
            'hit_punch_3',
            'hit_punch_4'
        ]);

        this.registerSoundVariations('hit_heavy', [
            'hit_heavy_1',
            'hit_heavy_2',
            'hit_heavy_3'
        ]);

        this.registerSoundVariations('hit_critical', [
            'hit_critical_1',
            'hit_critical_2'
        ]);

        // Slash sounds
        this.registerSoundVariations('slash', [
            'slash_light_1',
            'slash_light_2',
            'slash_light_3'
        ]);

        this.registerSoundVariations('slash_heavy', [
            'slash_heavy_1',
            'slash_heavy_2'
        ]);

        // Block/Parry sounds
        this.registerSoundVariations('block', [
            'block_1',
            'block_2',
            'block_3'
        ]);

        this.registerSoundVariations('parry', [
            'parry_perfect_1',
            'parry_perfect_2'
        ]);

        // Dodge sounds
        this.registerSoundVariations('dodge', [
            'dodge_1',
            'dodge_2'
        ]);

        // Special attack sounds
        this.registerSoundVariations('special', [
            'special_attack_1',
            'special_attack_2',
            'special_attack_3'
        ]);

        // Finisher sounds
        this.registerSoundVariations('finisher', [
            'finisher_brutal',
            'finisher_honorable',
            'finisher_funny'
        ]);

        // UI sounds
        this.registerSoundVariations('ui_combo', [
            'combo_continue',
            'combo_break'
        ]);

        // Pain/damage sounds
        this.registerSoundVariations('pain', [
            'pain_light_1',
            'pain_light_2',
            'pain_heavy_1',
            'pain_heavy_2'
        ]);

        // Weapon sounds
        this.registerSoundVariations('weapon_equip', [
            'weapon_equip_1',
            'weapon_equip_2'
        ]);

        this.registerSoundVariations('weapon_swing', [
            'weapon_swing_1',
            'weapon_swing_2',
            'weapon_swing_3'
        ]);
    }

    /**
     * Register sound variations
     */
    registerSoundVariations(category, soundIds) {
        if (!this.sounds.has(category)) {
            this.sounds.set(category, {
                variations: soundIds,
                lastIndex: -1
            });
        }
    }

    /**
     * Get next variation (avoid repetition)
     */
    getNextVariation(category) {
        const soundData = this.sounds.get(category);
        if (!soundData || soundData.variations.length === 0) {
            return null;
        }

        let index;
        if (soundData.variations.length === 1) {
            index = 0;
        } else {
            // Pick random variation that's different from last
            do {
                index = Math.floor(Math.random() * soundData.variations.length);
            } while (index === soundData.lastIndex && soundData.variations.length > 1);

            soundData.lastIndex = index;
        }

        return soundData.variations[index];
    }

    /**
     * Play hit sound with combo tracking
     */
    playHit(position, attackerId, options = {}) {
        const hitType = options.heavy ? 'hit_heavy' : 'hit';
        const soundId = this.getNextVariation(hitType);

        if (!soundId) {
            console.warn(`No sound variation for: ${hitType}`);
            return;
        }

        // Track combo
        const combo = this.updateCombo(attackerId);

        // Calculate volume and pitch based on combo
        let volume = options.volume || 0.6;
        let pitch = 1.0;

        if (this.config.enableCombos && combo > 1) {
            volume += Math.min(this.config.comboVolumeBoost * combo, 0.4);
            pitch += Math.min(this.config.comboPitchIncrease * combo, 0.3);
        }

        // Random pitch variation
        pitch += (Math.random() - 0.5) * this.config.randomPitchVariation;

        // Play sound
        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: Math.min(volume, 1.0),
            playbackRate: pitch
        });

        // Play combo UI sound
        if (combo >= 3 && combo % 5 === 0) {
            this.playComboSound(combo);
        }

        return combo;
    }

    /**
     * Play critical hit sound
     */
    playCritical(position, attackerId, options = {}) {
        const soundId = this.getNextVariation('hit_critical');

        if (!soundId) return;

        // Reset combo on critical
        this.resetCombo(attackerId);

        // Play with enhanced effects
        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: options.volume || 0.9,
            playbackRate: 1.0 + this.config.criticalPitchShift
        });

        // Play special UI sound
        this.playComboSound(999); // Special combo sound
    }

    /**
     * Play slash sound
     */
    playSlash(position, options = {}) {
        const slashType = options.heavy ? 'slash_heavy' : 'slash';
        const soundId = this.getNextVariation(slashType);

        if (!soundId) return;

        let pitch = 1.0 + (Math.random() - 0.5) * this.config.randomPitchVariation;

        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_slash',
            volume: options.volume || 0.5,
            playbackRate: pitch
        });
    }

    /**
     * Play block sound
     */
    playBlock(position, options = {}) {
        const soundId = this.getNextVariation('block');

        if (!soundId) return;

        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: options.volume || 0.6,
            playbackRate: 0.9 + Math.random() * 0.2
        });
    }

    /**
     * Play perfect parry sound
     */
    playParry(position, options = {}) {
        const soundId = this.getNextVariation('parry');

        if (!soundId) return;

        // Parry has special high-pitched metallic sound
        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: options.volume || 0.8,
            playbackRate: 1.2
        });
    }

    /**
     * Play dodge sound
     */
    playDodge(position, options = {}) {
        const soundId = this.getNextVariation('dodge');

        if (!soundId) return;

        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: options.volume || 0.4,
            playbackRate: 1.0 + Math.random() * 0.2
        });
    }

    /**
     * Play special attack sound
     */
    playSpecialAttack(position, options = {}) {
        const soundId = this.getNextVariation('special');

        if (!soundId) return;

        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: options.volume || 0.8,
            playbackRate: options.playbackRate || 1.0
        });
    }

    /**
     * Play finisher sound
     */
    playFinisher(position, category, options = {}) {
        // Map brutality categories to sound types
        const categoryMap = {
            'HONORABLE_DEATH': 'finisher_honorable',
            'FUNNY_DEATH': 'finisher_funny',
            'CRUEL_DEATH': 'finisher_brutal',
            'BLOOD_BATH': 'finisher_brutal',
            'POINTLESS_DEATH': 'finisher_funny'
        };

        const soundId = categoryMap[category] || 'finisher_brutal';

        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: options.volume || 1.0,
            playbackRate: options.playbackRate || 1.0
        });
    }

    /**
     * Play pain/damage sound
     */
    playPain(position, options = {}) {
        const painType = options.heavy ? 'pain_heavy_1' : 'pain_light_1';

        this.audioEngine.play3DSound(painType, position, {
            pool: 'combat_hit',
            volume: options.volume || 0.5,
            playbackRate: 0.9 + Math.random() * 0.2
        });
    }

    /**
     * Play weapon equip sound
     */
    playWeaponEquip(position, options = {}) {
        const soundId = this.getNextVariation('weapon_equip');

        if (!soundId) return;

        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_hit',
            volume: options.volume || 0.4,
            playbackRate: 1.0
        });
    }

    /**
     * Play weapon swing sound
     */
    playWeaponSwing(position, options = {}) {
        const soundId = this.getNextVariation('weapon_swing');

        if (!soundId) return;

        this.audioEngine.play3DSound(soundId, position, {
            pool: 'combat_slash',
            volume: options.volume || 0.3,
            playbackRate: 0.9 + Math.random() * 0.3
        });
    }

    /**
     * Update combo counter
     */
    updateCombo(attackerId) {
        const now = Date.now();
        const lastHit = this.lastHitTime.get(attackerId) || 0;

        // Check if combo should reset
        if (now - lastHit > this.comboResetDelay) {
            this.comboCounts.set(attackerId, 1);
        } else {
            const currentCombo = this.comboCounts.get(attackerId) || 0;
            this.comboCounts.set(attackerId, Math.min(currentCombo + 1, this.config.maxCombo));
        }

        this.lastHitTime.set(attackerId, now);

        return this.comboCounts.get(attackerId);
    }

    /**
     * Get current combo
     */
    getCombo(attackerId) {
        const now = Date.now();
        const lastHit = this.lastHitTime.get(attackerId) || 0;

        if (now - lastHit > this.comboResetDelay) {
            return 0;
        }

        return this.comboCounts.get(attackerId) || 0;
    }

    /**
     * Reset combo
     */
    resetCombo(attackerId) {
        this.comboCounts.set(attackerId, 0);
        this.lastHitTime.delete(attackerId);
    }

    /**
     * Play combo UI sound
     */
    playComboSound(combo) {
        const soundId = combo === 999 ? 'combo_break' : 'combo_continue';

        this.audioEngine.play2DSound(soundId, {
            volume: 0.7,
            playbackRate: 1.0 + Math.min(combo * 0.02, 0.4)
        });
    }

    /**
     * Play attack sequence (combo chain)
     */
    playAttackSequence(positions, attackerId, options = {}) {
        const delay = options.delay || 200; // ms between attacks

        positions.forEach((position, index) => {
            setTimeout(() => {
                if (index === positions.length - 1 && options.finisher) {
                    // Final hit
                    this.playCritical(position, attackerId, options);
                } else {
                    this.playHit(position, attackerId, {
                        ...options,
                        heavy: index % 3 === 2 // Every 3rd hit is heavy
                    });
                }
            }, delay * index);
        });
    }

    /**
     * Play shield impact sequence
     */
    playShieldImpact(position, impactStrength = 1.0) {
        // Initial block sound
        this.playBlock(position, { volume: 0.6 * impactStrength });

        // Metallic reverb impacts
        for (let i = 1; i <= 3; i++) {
            setTimeout(() => {
                this.audioEngine.play3DSound('block_1', position, {
                    pool: 'combat_hit',
                    volume: 0.3 * impactStrength * (1 - i * 0.2),
                    playbackRate: 1.0 + i * 0.1
                });
            }, i * 100);
        }
    }

    /**
     * Play dual finisher sequence (two characters)
     */
    playDualFinisher(position1, position2, category, options = {}) {
        // First character
        this.playFinisher(position1, category, options);

        // Second character (slightly delayed)
        setTimeout(() => {
            this.playFinisher(position2, category, {
                ...options,
                playbackRate: (options.playbackRate || 1.0) * 1.05
            });
        }, 150);

        // Final combined impact
        setTimeout(() => {
            const midPoint = new THREE.Vector3()
                .addVectors(position1, position2)
                .multiplyScalar(0.5);

            this.playCritical(midPoint, 'dual_finisher', {
                volume: 1.0
            });
        }, 800);
    }

    /**
     * Play battle start sound
     */
    playBattleStart() {
        this.audioEngine.play2DSound('battle_start', {
            volume: 0.8,
            playbackRate: 1.0
        });
    }

    /**
     * Play battle end sound
     */
    playBattleEnd(victory = true) {
        const soundId = victory ? 'battle_victory' : 'battle_defeat';

        this.audioEngine.play2DSound(soundId, {
            volume: 0.8,
            playbackRate: 1.0
        });
    }

    /**
     * Get statistics
     */
    getStats() {
        const comboStats = {};

        this.comboCounts.forEach((combo, attackerId) => {
            comboStats[attackerId] = {
                combo: combo,
                timeSinceLastHit: Date.now() - (this.lastHitTime.get(attackerId) || 0)
            };
        });

        return {
            soundCategories: this.sounds.size,
            activeCombos: comboStats,
            maxCombo: this.config.maxCombo,
            enableCombos: this.config.enableCombos
        };
    }

    /**
     * Dispose
     */
    dispose() {
        this.sounds.clear();
        this.comboCounts.clear();
        this.lastHitTime.clear();
        this.lastPlayedVariations.clear();
    }
}

// Placeholder SFX definitions
const COMBAT_SFX = {
    // Hit sounds
    hit_punch_1: '/assets/audio/sfx/combat/hit_punch_1.mp3',
    hit_punch_2: '/assets/audio/sfx/combat/hit_punch_2.mp3',
    hit_punch_3: '/assets/audio/sfx/combat/hit_punch_3.mp3',
    hit_punch_4: '/assets/audio/sfx/combat/hit_punch_4.mp3',
    hit_heavy_1: '/assets/audio/sfx/combat/hit_heavy_1.mp3',
    hit_heavy_2: '/assets/audio/sfx/combat/hit_heavy_2.mp3',
    hit_heavy_3: '/assets/audio/sfx/combat/hit_heavy_3.mp3',
    hit_critical_1: '/assets/audio/sfx/combat/hit_critical_1.mp3',
    hit_critical_2: '/assets/audio/sfx/combat/hit_critical_2.mp3',

    // Slash sounds
    slash_light_1: '/assets/audio/sfx/combat/slash_light_1.mp3',
    slash_light_2: '/assets/audio/sfx/combat/slash_light_2.mp3',
    slash_light_3: '/assets/audio/sfx/combat/slash_light_3.mp3',
    slash_heavy_1: '/assets/audio/sfx/combat/slash_heavy_1.mp3',
    slash_heavy_2: '/assets/audio/sfx/combat/slash_heavy_2.mp3',

    // Block/Parry
    block_1: '/assets/audio/sfx/combat/block_1.mp3',
    block_2: '/assets/audio/sfx/combat/block_2.mp3',
    block_3: '/assets/audio/sfx/combat/block_3.mp3',
    parry_perfect_1: '/assets/audio/sfx/combat/parry_perfect_1.mp3',
    parry_perfect_2: '/assets/audio/sfx/combat/parry_perfect_2.mp3',

    // Dodge
    dodge_1: '/assets/audio/sfx/combat/dodge_1.mp3',
    dodge_2: '/assets/audio/sfx/combat/dodge_2.mp3',

    // Special attacks
    special_attack_1: '/assets/audio/sfx/combat/special_attack_1.mp3',
    special_attack_2: '/assets/audio/sfx/combat/special_attack_2.mp3',
    special_attack_3: '/assets/audio/sfx/combat/special_attack_3.mp3',

    // Finishers
    finisher_brutal: '/assets/audio/sfx/combat/finisher_brutal.mp3',
    finisher_honorable: '/assets/audio/sfx/combat/finisher_honorable.mp3',
    finisher_funny: '/assets/audio/sfx/combat/finisher_funny.mp3',

    // UI/Combo
    combo_continue: '/assets/audio/sfx/ui/combo_continue.mp3',
    combo_break: '/assets/audio/sfx/ui/combo_break.mp3',

    // Pain
    pain_light_1: '/assets/audio/sfx/combat/pain_light_1.mp3',
    pain_light_2: '/assets/audio/sfx/combat/pain_light_2.mp3',
    pain_heavy_1: '/assets/audio/sfx/combat/pain_heavy_1.mp3',
    pain_heavy_2: '/assets/audio/sfx/combat/pain_heavy_2.mp3',

    // Weapon
    weapon_equip_1: '/assets/audio/sfx/combat/weapon_equip_1.mp3',
    weapon_equip_2: '/assets/audio/sfx/combat/weapon_equip_2.mp3',
    weapon_swing_1: '/assets/audio/sfx/combat/weapon_swing_1.mp3',
    weapon_swing_2: '/assets/audio/sfx/combat/weapon_swing_2.mp3',
    weapon_swing_3: '/assets/audio/sfx/combat/weapon_swing_3.mp3',

    // Battle
    battle_start: '/assets/audio/sfx/combat/battle_start.mp3',
    battle_victory: '/assets/audio/sfx/combat/battle_victory.mp3',
    battle_defeat: '/assets/audio/sfx/combat/battle_defeat.mp3'
};

// Make globally available
window.CombatSFXSystem = CombatSFXSystem;
window.COMBAT_SFX = COMBAT_SFX;
