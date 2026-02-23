/**
 * Music System
 * Dynamic music with transitions, layers, and battle themes
 * Digimon World style adaptive music
 */

// THREE is loaded globally via index.html

class MusicSystem {
    constructor(listener) {
        this.listener = listener;
        this.audioContext = listener.context;
        this.audioLoader = new THREE.AudioLoader();

        // Music tracks
        this.tracks = new Map();
        this.playlists = new Map();

        // Playback state
        this.currentTrack = null;
        this.currentAudio = null;
        this.nextTrack = null;
        this.isTransitioning = false;

        // Configuration
        this.config = {
            masterVolume: 0.7,
            fadeInDuration: 2.0,
            fadeOutDuration: 1.5,
            crossfadeDuration: 3.0,
            battleFadeInDuration: 0.5,
            enableDynamicLayers: true
        };

        // Music layers (for dynamic combat music)
        this.layers = {
            base: null,       // Ambient/exploration layer
            tension: null,    // Building tension layer
            combat: null,     // Full combat layer
            boss: null        // Epic boss battle layer
        };

        this.currentLayer = 'base';
        this.layerVolumes = {
            base: 1.0,
            tension: 0.0,
            combat: 0.0,
            boss: 0.0
        };

        this.initializePlaylists();

        console.log('🎵 Music System initialized');
    }

    /**
     * Initialize default playlists
     */
    initializePlaylists() {
        // Exploration playlist
        this.createPlaylist('exploration', [
            'exploration_1',
            'exploration_2',
            'exploration_3',
            'exploration_4'
        ], { shuffle: true, loop: true });

        // Battle playlist
        this.createPlaylist('battle', [
            'battle_normal_1',
            'battle_normal_2',
            'battle_normal_3'
        ], { shuffle: false, loop: true });

        // Boss battle playlist
        this.createPlaylist('boss', [
            'boss_battle_1',
            'boss_battle_2',
            'boss_battle_epic'
        ], { shuffle: false, loop: false });

        // Town/Safe area playlist
        this.createPlaylist('town', [
            'town_peaceful',
            'town_day',
            'town_night'
        ], { shuffle: false, loop: true });

        // Evolution playlist
        this.createPlaylist('evolution', [
            'evolution_theme'
        ], { shuffle: false, loop: false });

        // Victory playlist
        this.createPlaylist('victory', [
            'victory_fanfare'
        ], { shuffle: false, loop: false });
    }

    /**
     * Create a playlist
     */
    createPlaylist(name, trackIds, options = {}) {
        this.playlists.set(name, {
            tracks: trackIds,
            currentIndex: 0,
            shuffle: options.shuffle || false,
            loop: options.loop || false,
            shuffledTracks: options.shuffle ? this.shuffleArray([...trackIds]) : trackIds
        });
    }

    /**
     * Load music track
     */
    async loadTrack(trackId, url, metadata = {}) {
        return new Promise((resolve, reject) => {
            this.audioLoader.load(
                url,
                (buffer) => {
                    this.tracks.set(trackId, {
                        buffer: buffer,
                        metadata: {
                            title: metadata.title || trackId,
                            duration: buffer.duration,
                            bpm: metadata.bpm || 120,
                            mood: metadata.mood || 'neutral',
                            intensity: metadata.intensity || 5
                        }
                    });
                    console.log(`✅ Music track loaded: ${trackId}`);
                    resolve(buffer);
                },
                (progress) => {
                    // Progress callback
                },
                (error) => {
                    console.error(`❌ Failed to load music: ${trackId}`, error);
                    reject(error);
                }
            );
        });
    }

    /**
     * Load multiple tracks
     */
    async loadTracks(trackDefinitions) {
        const promises = trackDefinitions.map(def =>
            this.loadTrack(def.id, def.url, def.metadata)
        );

        return Promise.all(promises);
    }

    /**
     * Play a specific track
     */
    playTrack(trackId, options = {}) {
        const track = this.tracks.get(trackId);
        if (!track) {
            console.warn(`Music track not loaded: ${trackId}`);
            return null;
        }

        // Stop current track if playing
        if (this.currentAudio && this.currentAudio.isPlaying) {
            if (options.crossfade) {
                return this.crossfadeToTrack(trackId, options);
            } else {
                this.fadeOut(this.currentAudio, this.config.fadeOutDuration);
            }
        }

        // Create new audio
        const audio = new THREE.Audio(this.listener);
        audio.setBuffer(track.buffer);
        audio.setVolume(0);
        audio.setLoop(options.loop !== undefined ? options.loop : true);

        audio.play();

        // Fade in
        this.fadeIn(audio, this.config.masterVolume, options.fadeInDuration || this.config.fadeInDuration);

        this.currentTrack = trackId;
        this.currentAudio = audio;

        // Handle track end
        if (!audio.loop) {
            audio.onEnded = () => {
                this.onTrackEnded();
            };
        }

        console.log(`🎵 Now playing: ${track.metadata.title}`);

        return audio;
    }

    /**
     * Play playlist
     */
    playPlaylist(playlistName, options = {}) {
        const playlist = this.playlists.get(playlistName);
        if (!playlist) {
            console.warn(`Playlist not found: ${playlistName}`);
            return;
        }

        // Reset playlist if needed
        if (options.restart) {
            playlist.currentIndex = 0;
            if (playlist.shuffle) {
                playlist.shuffledTracks = this.shuffleArray([...playlist.tracks]);
            }
        }

        // Get next track
        const trackList = playlist.shuffle ? playlist.shuffledTracks : playlist.tracks;
        const trackId = trackList[playlist.currentIndex];

        // Play the track
        this.playTrack(trackId, {
            loop: false,
            crossfade: options.crossfade || false,
            fadeInDuration: options.fadeInDuration
        });

        // Store current playlist
        this.currentPlaylist = playlistName;
    }

    /**
     * Crossfade to new track
     */
    crossfadeToTrack(trackId, options = {}) {
        const track = this.tracks.get(trackId);
        if (!track) return null;

        const oldAudio = this.currentAudio;
        const duration = options.crossfadeDuration || this.config.crossfadeDuration;

        // Create new audio
        const newAudio = new THREE.Audio(this.listener);
        newAudio.setBuffer(track.buffer);
        newAudio.setVolume(0);
        newAudio.setLoop(options.loop !== undefined ? options.loop : true);

        newAudio.play();

        this.isTransitioning = true;

        // Crossfade
        if (oldAudio && oldAudio.isPlaying) {
            this.fadeOut(oldAudio, duration);
        }

        this.fadeIn(newAudio, this.config.masterVolume, duration);

        setTimeout(() => {
            this.isTransitioning = false;
        }, duration * 1000);

        this.currentTrack = trackId;
        this.currentAudio = newAudio;

        return newAudio;
    }

    /**
     * Switch to battle music
     */
    enterBattle(isBoss = false) {
        const playlistName = isBoss ? 'boss' : 'battle';

        this.playPlaylist(playlistName, {
            crossfade: true,
            crossfadeDuration: this.config.battleFadeInDuration,
            restart: true
        });

        console.log(`⚔️ Battle music started: ${isBoss ? 'Boss' : 'Normal'}`);
    }

    /**
     * Return to exploration music
     */
    exitBattle() {
        this.playPlaylist('exploration', {
            crossfade: true,
            crossfadeDuration: this.config.fadeInDuration
        });

        console.log(`🌿 Exploration music resumed`);
    }

    /**
     * Play evolution theme
     */
    playEvolution() {
        this.playPlaylist('evolution', {
            crossfade: false,
            fadeInDuration: 0.5,
            restart: true
        });
    }

    /**
     * Play victory fanfare
     */
    playVictory() {
        this.playPlaylist('victory', {
            crossfade: false,
            fadeInDuration: 0.3,
            restart: true
        });
    }

    /**
     * Dynamic layer system for combat intensity
     */
    setMusicIntensity(intensity) {
        // intensity: 0 = exploration, 1-3 = tension, 4-7 = combat, 8-10 = boss
        let targetLayer = 'base';

        if (intensity >= 8) {
            targetLayer = 'boss';
        } else if (intensity >= 4) {
            targetLayer = 'combat';
        } else if (intensity >= 1) {
            targetLayer = 'tension';
        }

        if (targetLayer !== this.currentLayer) {
            this.transitionToLayer(targetLayer);
        }
    }

    /**
     * Transition between music layers
     */
    transitionToLayer(targetLayer) {
        const duration = 2.0;
        const steps = 60;
        const stepDuration = (duration * 1000) / steps;

        let currentStep = 0;

        const transitionInterval = setInterval(() => {
            currentStep++;
            const progress = currentStep / steps;

            // Fade out all layers
            Object.keys(this.layerVolumes).forEach(layer => {
                if (layer === targetLayer) {
                    this.layerVolumes[layer] = progress;
                } else {
                    this.layerVolumes[layer] = 1 - progress;
                }

                // Apply volume to actual audio if layer exists
                if (this.layers[layer] && this.layers[layer].isPlaying) {
                    this.layers[layer].setVolume(this.layerVolumes[layer] * this.config.masterVolume);
                }
            });

            if (currentStep >= steps) {
                clearInterval(transitionInterval);
                this.currentLayer = targetLayer;
                console.log(`🎵 Music layer transitioned to: ${targetLayer}`);
            }
        }, stepDuration);
    }

    /**
     * Handle track ended
     */
    onTrackEnded() {
        if (this.currentPlaylist) {
            const playlist = this.playlists.get(this.currentPlaylist);

            if (playlist) {
                // Move to next track
                playlist.currentIndex++;

                // Check if playlist should loop
                if (playlist.currentIndex >= playlist.tracks.length) {
                    if (playlist.loop) {
                        playlist.currentIndex = 0;

                        // Re-shuffle if needed
                        if (playlist.shuffle) {
                            playlist.shuffledTracks = this.shuffleArray([...playlist.tracks]);
                        }
                    } else {
                        // Playlist finished
                        console.log(`✅ Playlist finished: ${this.currentPlaylist}`);
                        return;
                    }
                }

                // Play next track
                this.playPlaylist(this.currentPlaylist, { restart: false });
            }
        }
    }

    /**
     * Fade out audio
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
     * Fade in audio
     */
    fadeIn(audio, targetVolume = 1.0, duration = 1.0) {
        if (!audio || !audio.isPlaying) return;

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
     * Pause current music
     */
    pause() {
        if (this.currentAudio && this.currentAudio.isPlaying) {
            this.currentAudio.pause();
        }
    }

    /**
     * Resume music
     */
    resume() {
        if (this.currentAudio && !this.currentAudio.isPlaying) {
            this.currentAudio.play();
        }
    }

    /**
     * Stop all music
     */
    stop() {
        if (this.currentAudio && this.currentAudio.isPlaying) {
            this.currentAudio.stop();
        }

        Object.values(this.layers).forEach(layer => {
            if (layer && layer.isPlaying) {
                layer.stop();
            }
        });

        this.currentTrack = null;
        this.currentPlaylist = null;
    }

    /**
     * Set master volume
     */
    setMasterVolume(volume) {
        this.config.masterVolume = Math.max(0, Math.min(1, volume));

        if (this.currentAudio && this.currentAudio.isPlaying) {
            this.currentAudio.setVolume(this.config.masterVolume);
        }

        Object.values(this.layers).forEach(layer => {
            if (layer && layer.isPlaying) {
                const layerName = Object.keys(this.layers).find(key => this.layers[key] === layer);
                layer.setVolume(this.layerVolumes[layerName] * this.config.masterVolume);
            }
        });
    }

    /**
     * Shuffle array helper
     */
    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    /**
     * Get current track info
     */
    getCurrentTrackInfo() {
        if (!this.currentTrack) return null;

        const track = this.tracks.get(this.currentTrack);
        if (!track) return null;

        return {
            id: this.currentTrack,
            ...track.metadata,
            isPlaying: this.currentAudio ? this.currentAudio.isPlaying : false,
            currentTime: this.currentAudio ? this.audioContext.currentTime : 0
        };
    }

    /**
     * Get statistics
     */
    getStats() {
        return {
            loadedTracks: this.tracks.size,
            playlists: this.playlists.size,
            currentTrack: this.currentTrack,
            currentPlaylist: this.currentPlaylist,
            isPlaying: this.currentAudio ? this.currentAudio.isPlaying : false,
            isTransitioning: this.isTransitioning,
            currentLayer: this.currentLayer,
            masterVolume: this.config.masterVolume
        };
    }

    /**
     * Dispose of music system
     */
    dispose() {
        this.stop();

        this.tracks.clear();
        this.playlists.clear();

        if (this.currentAudio) {
            this.currentAudio.disconnect();
        }

        Object.values(this.layers).forEach(layer => {
            if (layer) {
                layer.disconnect();
            }
        });
    }
}

// Placeholder music track definitions
const MUSIC_TRACKS = {
    // Exploration
    exploration_1: { url: '/assets/audio/music/exploration_1.mp3', metadata: { title: 'Forest Path', bpm: 90, mood: 'peaceful' } },
    exploration_2: { url: '/assets/audio/music/exploration_2.mp3', metadata: { title: 'Mountain Trail', bpm: 95, mood: 'adventurous' } },
    exploration_3: { url: '/assets/audio/music/exploration_3.mp3', metadata: { title: 'Grasslands', bpm: 88, mood: 'calm' } },
    exploration_4: { url: '/assets/audio/music/exploration_4.mp3', metadata: { title: 'Ancient Ruins', bpm: 85, mood: 'mysterious' } },

    // Battle
    battle_normal_1: { url: '/assets/audio/music/battle_normal_1.mp3', metadata: { title: 'Battle Theme', bpm: 140, mood: 'intense', intensity: 7 } },
    battle_normal_2: { url: '/assets/audio/music/battle_normal_2.mp3', metadata: { title: 'Combat', bpm: 145, mood: 'aggressive', intensity: 7 } },
    battle_normal_3: { url: '/assets/audio/music/battle_normal_3.mp3', metadata: { title: 'Fight', bpm: 138, mood: 'energetic', intensity: 6 } },

    // Boss
    boss_battle_1: { url: '/assets/audio/music/boss_battle_1.mp3', metadata: { title: 'Boss Theme', bpm: 150, mood: 'epic', intensity: 9 } },
    boss_battle_2: { url: '/assets/audio/music/boss_battle_2.mp3', metadata: { title: 'Final Battle', bpm: 155, mood: 'dramatic', intensity: 10 } },
    boss_battle_epic: { url: '/assets/audio/music/boss_battle_epic.mp3', metadata: { title: 'Ultimate Showdown', bpm: 160, mood: 'heroic', intensity: 10 } },

    // Town
    town_peaceful: { url: '/assets/audio/music/town_peaceful.mp3', metadata: { title: 'Safe Haven', bpm: 75, mood: 'peaceful' } },
    town_day: { url: '/assets/audio/music/town_day.mp3', metadata: { title: 'Village Day', bpm: 80, mood: 'cheerful' } },
    town_night: { url: '/assets/audio/music/town_night.mp3', metadata: { title: 'Moonlit Town', bpm: 70, mood: 'serene' } },

    // Special
    evolution_theme: { url: '/assets/audio/music/evolution_theme.mp3', metadata: { title: 'Evolution!', bpm: 120, mood: 'triumphant' } },
    victory_fanfare: { url: '/assets/audio/music/victory_fanfare.mp3', metadata: { title: 'Victory!', bpm: 130, mood: 'victorious' } }
};

// Make globally available
window.MusicSystem = MusicSystem;
window.MUSIC_TRACKS = MUSIC_TRACKS;
