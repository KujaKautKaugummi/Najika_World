/**
 * Spatial Audio Engine
 * 3D positional audio with Web Audio API
 * Digimon World style environmental and combat audio
 */

// THREE is loaded globally via index.html

class SpatialAudioEngine {
    constructor(camera) {
        this.camera = camera;
        this.listener = null;
        this.audioContext = null;
        this.sounds = new Map();
        this.activeSounds = [];
        this.audioLoader = null;

        // Configuration
        this.config = {
            masterVolume: 1.0,
            sfxVolume: 0.8,
            ambientVolume: 0.6,
            musicVolume: 0.7,
            maxDistance: 100,
            rolloffFactor: 1.5,
            distanceModel: 'inverse',
            maxSimultaneousSounds: 32
        };

        // Audio pools for performance
        this.audioPools = new Map();

        this.initialize();

        console.log('🔊 Spatial Audio Engine initialized');
    }

    /**
     * Initialize audio system
     */
    initialize() {
        // Create Audio Listener
        this.listener = new THREE.AudioListener();
        this.camera.add(this.listener);

        // Get AudioContext
        this.audioContext = this.listener.context;

        // Create AudioLoader
        this.audioLoader = new THREE.AudioLoader();

        // Setup audio pools
        this.initializeAudioPools();
    }

    /**
     * Initialize audio pools for common sounds
     */
    initializeAudioPools() {
        // Footstep pool
        this.createAudioPool('footstep', {
            poolSize: 8,
            is3D: true,
            maxDistance: 20,
            volume: 0.3
        });

        // Combat hit pool
        this.createAudioPool('combat_hit', {
            poolSize: 16,
            is3D: true,
            maxDistance: 30,
            volume: 0.6
        });

        // Combat slash pool
        this.createAudioPool('combat_slash', {
            poolSize: 12,
            is3D: true,
            maxDistance: 25,
            volume: 0.5
        });

        // Magic cast pool
        this.createAudioPool('magic_cast', {
            poolSize: 10,
            is3D: true,
            maxDistance: 40,
            volume: 0.7
        });

        // Ambient environmental pool
        this.createAudioPool('ambient', {
            poolSize: 6,
            is3D: true,
            maxDistance: 50,
            volume: 0.4,
            loop: true
        });

        // UI sound pool
        this.createAudioPool('ui', {
            poolSize: 4,
            is3D: false,
            volume: 0.5
        });
    }

    /**
     * Create an audio pool
     */
    createAudioPool(poolName, config) {
        const pool = {
            config: config,
            sounds: [],
            currentIndex: 0
        };

        // Pre-create audio objects
        for (let i = 0; i < config.poolSize; i++) {
            let audio;

            if (config.is3D) {
                audio = new THREE.PositionalAudio(this.listener);
                audio.setMaxDistance(config.maxDistance || this.config.maxDistance);
                audio.setRefDistance(1);
                audio.setRolloffFactor(this.config.rolloffFactor);
                audio.setDistanceModel(this.config.distanceModel);
            } else {
                audio = new THREE.Audio(this.listener);
            }

            audio.setVolume(config.volume || 0.5);
            audio.setLoop(config.loop || false);

            pool.sounds.push(audio);
        }

        this.audioPools.set(poolName, pool);
    }

    /**
     * Load audio file
     */
    async loadAudio(name, url) {
        return new Promise((resolve, reject) => {
            this.audioLoader.load(
                url,
                (buffer) => {
                    this.sounds.set(name, buffer);
                    console.log(`✅ Audio loaded: ${name}`);
                    resolve(buffer);
                },
                (progress) => {
                    // Progress callback
                },
                (error) => {
                    console.error(`❌ Failed to load audio: ${name}`, error);
                    reject(error);
                }
            );
        });
    }

    /**
     * Load multiple audio files
     */
    async loadAudioBatch(audioDefinitions) {
        const promises = audioDefinitions.map(def =>
            this.loadAudio(def.name, def.url)
        );

        return Promise.all(promises);
    }

    /**
     * Play 3D positional sound
     */
    play3DSound(soundName, position, options = {}) {
        const buffer = this.sounds.get(soundName);
        if (!buffer) {
            console.warn(`Sound not loaded: ${soundName}`);
            return null;
        }

        // Get audio from pool if specified
        const poolName = options.pool || 'combat_hit';
        const pool = this.audioPools.get(poolName);

        if (!pool) {
            console.warn(`Audio pool not found: ${poolName}`);
            return null;
        }

        // Get next available sound from pool
        const audio = pool.sounds[pool.currentIndex];
        pool.currentIndex = (pool.currentIndex + 1) % pool.sounds.length;

        // Stop if already playing
        if (audio.isPlaying) {
            audio.stop();
        }

        // Set buffer and play
        audio.setBuffer(buffer);

        // Apply options
        if (options.volume !== undefined) {
            audio.setVolume(options.volume);
        }

        if (options.playbackRate !== undefined) {
            audio.setPlaybackRate(options.playbackRate);
        }

        if (options.loop !== undefined) {
            audio.setLoop(options.loop);
        }

        // Position the audio
        if (audio instanceof THREE.PositionalAudio && position) {
            // If position is a THREE.Object3D, attach to it
            if (position.isObject3D) {
                position.add(audio);
            } else {
                // Otherwise create a temporary object at that position
                const soundObject = new THREE.Object3D();
                soundObject.position.copy(position);
                this.camera.parent.add(soundObject);
                soundObject.add(audio);

                // Remove after playing
                audio.onEnded = () => {
                    soundObject.remove(audio);
                    this.camera.parent.remove(soundObject);
                };
            }
        }

        audio.play();

        // Track active sound
        this.activeSounds.push({
            audio: audio,
            name: soundName,
            startTime: this.audioContext.currentTime
        });

        return audio;
    }

    /**
     * Play 2D sound (UI, music)
     */
    play2DSound(soundName, options = {}) {
        const buffer = this.sounds.get(soundName);
        if (!buffer) {
            console.warn(`Sound not loaded: ${soundName}`);
            return null;
        }

        const pool = this.audioPools.get('ui');
        if (!pool) return null;

        const audio = pool.sounds[pool.currentIndex];
        pool.currentIndex = (pool.currentIndex + 1) % pool.sounds.length;

        if (audio.isPlaying) {
            audio.stop();
        }

        audio.setBuffer(buffer);
        audio.setVolume(options.volume || pool.config.volume);
        audio.setLoop(options.loop || false);

        if (options.playbackRate !== undefined) {
            audio.setPlaybackRate(options.playbackRate);
        }

        audio.play();

        this.activeSounds.push({
            audio: audio,
            name: soundName,
            startTime: this.audioContext.currentTime
        });

        return audio;
    }

    /**
     * Play footstep sound
     */
    playFootstep(position, terrainType = 'grass') {
        const soundMap = {
            'grass': 'footstep_grass',
            'dirt': 'footstep_dirt',
            'stone': 'footstep_stone',
            'water': 'footstep_water',
            'sand': 'footstep_sand',
            'snow': 'footstep_snow'
        };

        const soundName = soundMap[terrainType] || 'footstep_grass';

        return this.play3DSound(soundName, position, {
            pool: 'footstep',
            volume: 0.2 + Math.random() * 0.1,
            playbackRate: 0.9 + Math.random() * 0.2
        });
    }

    /**
     * Play combat hit sound
     */
    playCombatHit(position, hitType = 'normal') {
        const soundMap = {
            'normal': 'combat_hit_normal',
            'critical': 'combat_hit_critical',
            'heavy': 'combat_hit_heavy',
            'light': 'combat_hit_light'
        };

        const soundName = soundMap[hitType] || 'combat_hit_normal';

        return this.play3DSound(soundName, position, {
            pool: 'combat_hit',
            volume: 0.6,
            playbackRate: 0.95 + Math.random() * 0.1
        });
    }

    /**
     * Play combat slash sound
     */
    playCombatSlash(position, slashType = 'sword') {
        const soundMap = {
            'sword': 'combat_slash_sword',
            'claw': 'combat_slash_claw',
            'heavy': 'combat_slash_heavy',
            'fast': 'combat_slash_fast'
        };

        const soundName = soundMap[slashType] || 'combat_slash_sword';

        return this.play3DSound(soundName, position, {
            pool: 'combat_slash',
            volume: 0.5,
            playbackRate: 0.9 + Math.random() * 0.2
        });
    }

    /**
     * Play magic cast sound
     */
    playMagicCast(position, element = 'fire') {
        const soundMap = {
            'fire': 'magic_fire',
            'ice': 'magic_ice',
            'lightning': 'magic_lightning',
            'earth': 'magic_earth',
            'wind': 'magic_wind',
            'water': 'magic_water',
            'light': 'magic_light',
            'dark': 'magic_dark'
        };

        const soundName = soundMap[element] || 'magic_fire';

        return this.play3DSound(soundName, position, {
            pool: 'magic_cast',
            volume: 0.7,
            playbackRate: 1.0
        });
    }

    /**
     * Play ambient loop
     */
    playAmbient(position, ambientType = 'forest') {
        const soundMap = {
            'forest': 'ambient_forest',
            'cave': 'ambient_cave',
            'water': 'ambient_water',
            'wind': 'ambient_wind',
            'fire': 'ambient_fire',
            'city': 'ambient_city'
        };

        const soundName = soundMap[ambientType] || 'ambient_forest';

        return this.play3DSound(soundName, position, {
            pool: 'ambient',
            volume: 0.3,
            loop: true
        });
    }

    /**
     * Stop all sounds of a specific type
     */
    stopSoundsByPool(poolName) {
        const pool = this.audioPools.get(poolName);
        if (!pool) return;

        pool.sounds.forEach(audio => {
            if (audio.isPlaying) {
                audio.stop();
            }
        });
    }

    /**
     * Stop all sounds
     */
    stopAllSounds() {
        this.audioPools.forEach((pool) => {
            pool.sounds.forEach(audio => {
                if (audio.isPlaying) {
                    audio.stop();
                }
            });
        });

        this.activeSounds = [];
    }

    /**
     * Fade out all sounds
     */
    fadeOutAll(duration = 1.0) {
        this.audioPools.forEach((pool) => {
            pool.sounds.forEach(audio => {
                if (audio.isPlaying) {
                    this.fadeOut(audio, duration);
                }
            });
        });
    }

    /**
     * Fade out a specific sound
     */
    fadeOut(audio, duration = 1.0) {
        if (!audio || !audio.isPlaying) return;

        const currentVolume = audio.getVolume();
        const steps = 60;
        const stepDuration = (duration * 1000) / steps;
        const volumeStep = currentVolume / steps;

        let currentStep = 0;

        const fadeInterval = setInterval(() => {
            currentStep++;
            const newVolume = currentVolume - (volumeStep * currentStep);

            if (currentStep >= steps || newVolume <= 0) {
                audio.stop();
                clearInterval(fadeInterval);
            } else {
                audio.setVolume(newVolume);
            }
        }, stepDuration);
    }

    /**
     * Fade in a sound
     */
    fadeIn(audio, targetVolume = 1.0, duration = 1.0) {
        if (!audio || !audio.isPlaying) return;

        audio.setVolume(0);

        const steps = 60;
        const stepDuration = (duration * 1000) / steps;
        const volumeStep = targetVolume / steps;

        let currentStep = 0;

        const fadeInterval = setInterval(() => {
            currentStep++;
            const newVolume = volumeStep * currentStep;

            if (currentStep >= steps) {
                audio.setVolume(targetVolume);
                clearInterval(fadeInterval);
            } else {
                audio.setVolume(newVolume);
            }
        }, stepDuration);
    }

    /**
     * Set master volume
     */
    setMasterVolume(volume) {
        this.config.masterVolume = Math.max(0, Math.min(1, volume));
        this.listener.setMasterVolume(this.config.masterVolume);
    }

    /**
     * Set volume for specific pool
     */
    setPoolVolume(poolName, volume) {
        const pool = this.audioPools.get(poolName);
        if (!pool) return;

        pool.config.volume = Math.max(0, Math.min(1, volume));

        pool.sounds.forEach(audio => {
            if (!audio.isPlaying) {
                audio.setVolume(pool.config.volume);
            }
        });
    }

    /**
     * Update audio system (call in animation loop)
     */
    update(deltaTime) {
        // Clean up finished sounds
        this.activeSounds = this.activeSounds.filter(sound => {
            return sound.audio.isPlaying;
        });

        // Enforce max simultaneous sounds
        if (this.activeSounds.length > this.config.maxSimultaneousSounds) {
            // Stop oldest sounds
            const toStop = this.activeSounds.length - this.config.maxSimultaneousSounds;
            for (let i = 0; i < toStop; i++) {
                if (this.activeSounds[i] && this.activeSounds[i].audio) {
                    this.activeSounds[i].audio.stop();
                }
            }
        }
    }

    /**
     * Get active sound count
     */
    getActiveSoundCount() {
        return this.activeSounds.filter(s => s.audio.isPlaying).length;
    }

    /**
     * Get statistics
     */
    getStats() {
        const poolStats = {};

        this.audioPools.forEach((pool, name) => {
            const playingCount = pool.sounds.filter(audio => audio.isPlaying).length;
            poolStats[name] = {
                total: pool.sounds.length,
                playing: playingCount,
                available: pool.sounds.length - playingCount
            };
        });

        return {
            totalActiveSounds: this.getActiveSoundCount(),
            maxSimultaneousSounds: this.config.maxSimultaneousSounds,
            masterVolume: this.config.masterVolume,
            poolStats: poolStats,
            loadedSounds: this.sounds.size
        };
    }

    /**
     * Dispose of audio engine
     */
    dispose() {
        this.stopAllSounds();

        this.audioPools.forEach((pool) => {
            pool.sounds.forEach(audio => {
                audio.disconnect();
            });
        });

        this.audioPools.clear();
        this.sounds.clear();
        this.activeSounds = [];

        if (this.listener) {
            this.camera.remove(this.listener);
        }
    }
}

// Placeholder audio file definitions
// These should be replaced with actual audio files
const AUDIO_ASSETS = {
    // Footsteps
    footstep_grass: '/assets/audio/sfx/footstep_grass.mp3',
    footstep_dirt: '/assets/audio/sfx/footstep_dirt.mp3',
    footstep_stone: '/assets/audio/sfx/footstep_stone.mp3',
    footstep_water: '/assets/audio/sfx/footstep_water.mp3',
    footstep_sand: '/assets/audio/sfx/footstep_sand.mp3',
    footstep_snow: '/assets/audio/sfx/footstep_snow.mp3',

    // Combat hits
    combat_hit_normal: '/assets/audio/sfx/combat_hit_normal.mp3',
    combat_hit_critical: '/assets/audio/sfx/combat_hit_critical.mp3',
    combat_hit_heavy: '/assets/audio/sfx/combat_hit_heavy.mp3',
    combat_hit_light: '/assets/audio/sfx/combat_hit_light.mp3',

    // Combat slashes
    combat_slash_sword: '/assets/audio/sfx/combat_slash_sword.mp3',
    combat_slash_claw: '/assets/audio/sfx/combat_slash_claw.mp3',
    combat_slash_heavy: '/assets/audio/sfx/combat_slash_heavy.mp3',
    combat_slash_fast: '/assets/audio/sfx/combat_slash_fast.mp3',

    // Magic
    magic_fire: '/assets/audio/sfx/magic_fire.mp3',
    magic_ice: '/assets/audio/sfx/magic_ice.mp3',
    magic_lightning: '/assets/audio/sfx/magic_lightning.mp3',
    magic_earth: '/assets/audio/sfx/magic_earth.mp3',
    magic_wind: '/assets/audio/sfx/magic_wind.mp3',
    magic_water: '/assets/audio/sfx/magic_water.mp3',
    magic_light: '/assets/audio/sfx/magic_light.mp3',
    magic_dark: '/assets/audio/sfx/magic_dark.mp3',

    // Ambient
    ambient_forest: '/assets/audio/ambient/forest.mp3',
    ambient_cave: '/assets/audio/ambient/cave.mp3',
    ambient_water: '/assets/audio/ambient/water.mp3',
    ambient_wind: '/assets/audio/ambient/wind.mp3',
    ambient_fire: '/assets/audio/ambient/fire.mp3',
    ambient_city: '/assets/audio/ambient/city.mp3'
};

// Make globally available
window.SpatialAudioEngine = SpatialAudioEngine;
window.AUDIO_ASSETS = AUDIO_ASSETS;
