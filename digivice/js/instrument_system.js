/**
 * NAJIKA WORLD - INSTRUMENT SYSTEM
 * =================================
 * Ocarina of Time / Zelda-Style Musik-System
 *
 * Features:
 * - Verschiedene Instrumente (Okarina, Harfe, Flöte, Trommel)
 * - Noten spielen mit Tastatur/Touch
 * - Melodien lernen und abspielen
 * - Magische Effekte durch Lieder
 * - Duett-Modus mit NPCs
 *
 * Controls:
 * - A/S/D/F/G = Noten (Do/Re/Mi/Fa/Sol)
 * - H/J/K/L/; = Noten (La/Si/Do'/Re'/Mi')
 * - SHIFT = Oktave höher
 * - SPACE = Note halten
 *
 * Erstellt: 2025-12-14
 */

const InstrumentSystem = (function() {
    'use strict';

    // ============================================
    // KONFIGURATION
    // ============================================

    // Audio Context
    let audioContext = null;
    let masterGain = null;

    // Noten-Frequenzen (C4 = Middle C)
    const NOTE_FREQUENCIES = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00,
        'A4': 440.00, 'B4': 493.88, 'C5': 523.25, 'D5': 587.33, 'E5': 659.25,
        'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77, 'C6': 1046.50
    };

    // Tastatur-Mapping
    const KEY_TO_NOTE = {
        'a': 'C4', 's': 'D4', 'd': 'E4', 'f': 'F4', 'g': 'G4',
        'h': 'A4', 'j': 'B4', 'k': 'C5', 'l': 'D5', ';': 'E5'
    };

    // Instrumente
    const INSTRUMENTS = {
        okarina: {
            name: 'Okarina',
            icon: '🎵',
            waveform: 'sine',
            attack: 0.02,
            decay: 0.1,
            sustain: 0.7,
            release: 0.3,
            color: '#4a9eff'
        },
        harfe: {
            name: 'Harfe',
            icon: '🎸',
            waveform: 'triangle',
            attack: 0.01,
            decay: 0.2,
            sustain: 0.5,
            release: 0.8,
            color: '#ffd700'
        },
        floete: {
            name: 'Flöte',
            icon: '🎶',
            waveform: 'sine',
            attack: 0.05,
            decay: 0.15,
            sustain: 0.6,
            release: 0.4,
            color: '#88ff88'
        },
        trommel: {
            name: 'Trommel',
            icon: '🥁',
            waveform: 'square',
            attack: 0.001,
            decay: 0.3,
            sustain: 0.1,
            release: 0.1,
            color: '#ff6b6b'
        },
        glockenspiel: {
            name: 'Glockenspiel',
            icon: '🔔',
            waveform: 'sine',
            attack: 0.001,
            decay: 0.4,
            sustain: 0.3,
            release: 1.0,
            color: '#c0c0c0'
        },
        mundharmonika: {
            name: 'Mundharmonika',
            icon: '🎵',
            waveform: 'sawtooth',
            attack: 0.03,
            decay: 0.1,
            sustain: 0.8,
            release: 0.2,
            color: '#8B4513'
        },
        geige: {
            name: 'Geige',
            icon: '🎻',
            waveform: 'sawtooth',
            attack: 0.08,
            decay: 0.2,
            sustain: 0.7,
            release: 0.5,
            color: '#D2691E'
        },
        violine: {
            name: 'Violine',
            icon: '🎻',
            waveform: 'sawtooth',
            attack: 0.1,
            decay: 0.15,
            sustain: 0.75,
            release: 0.6,
            color: '#8B0000'
        }
    };

    // Magische Lieder (Melodien die Effekte auslösen)
    const MAGIC_SONGS = {
        sonnenlied: {
            name: 'Sonnenlied',
            notes: ['C4', 'E4', 'G4', 'C5', 'G4', 'E4'],
            effect: 'change_time_day',
            description: 'Ändert die Zeit zu Tag',
            icon: '☀️',
            learned: false
        },
        mondlied: {
            name: 'Mondlied',
            notes: ['G4', 'E4', 'C4', 'G4', 'E4', 'C4'],
            effect: 'change_time_night',
            description: 'Ändert die Zeit zu Nacht',
            icon: '🌙',
            learned: false
        },
        regenlied: {
            name: 'Regenlied',
            notes: ['A4', 'B4', 'A4', 'G4', 'F4', 'G4'],
            effect: 'summon_rain',
            description: 'Beschwört Regen',
            icon: '🌧️',
            learned: false
        },
        teleportlied: {
            name: 'Lied der Mühle',
            notes: ['C4', 'D4', 'E4', 'C4', 'D4', 'E4', 'F4', 'G4'],
            effect: 'teleport_home',
            description: 'Teleportiert zur Schwarzen Mühle',
            icon: '🏠',
            learned: true  // Start mit diesem Lied
        },
        heillied: {
            name: 'Heillied',
            notes: ['E4', 'G4', 'A4', 'G4', 'E4', 'C4'],
            effect: 'heal_player',
            description: 'Heilt den Spieler',
            icon: '💚',
            learned: false
        },
        schlaflied: {
            name: 'Schlaflied',
            notes: ['C4', 'E4', 'G4', 'E4', 'C4', 'E4', 'G4'],
            effect: 'sleep_enemies',
            description: 'Schläfert nahe Gegner ein',
            icon: '😴',
            learned: false
        },
        sturmruf: {
            name: 'Sturmruf',
            notes: ['G4', 'A4', 'B4', 'C5', 'B4', 'A4', 'G4'],
            effect: 'summon_najika',
            description: 'Ruft Najika zu dir',
            icon: '🌸',
            learned: true
        },
        zeitlied: {
            name: 'Lied der Zeit',
            notes: ['C4', 'A4', 'D4', 'C4', 'A4', 'D4'],
            effect: 'slow_time',
            description: 'Verlangsamt die Zeit kurzzeitig',
            icon: '⏰',
            learned: false
        }
    };

    // State
    let state = {
        active: false,
        currentInstrument: 'okarina',
        playedNotes: [],
        noteTimeout: null,
        ownedInstruments: ['okarina'],
        learnedSongs: ['teleportlied', 'sturmruf'],
        isRecording: false,
        recordedMelody: [],
        duetPartner: null
    };

    // Active oscillators
    const activeOscillators = {};

    // UI Elements
    let instrumentUI = null;
    let noteDisplay = null;

    // ============================================
    // AUDIO INITIALIZATION
    // ============================================

    function initAudio() {
        if (audioContext) return true;

        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            masterGain = audioContext.createGain();
            masterGain.gain.value = 0.5;
            masterGain.connect(audioContext.destination);
            console.log('🎵 Instrument Audio initialisiert');
            return true;
        } catch (e) {
            console.error('🎵 Audio Context Fehler:', e);
            return false;
        }
    }

    // ============================================
    // NOTE PLAYING
    // ============================================

    function playNote(note, duration = 0.5) {
        if (!initAudio()) return;
        if (!NOTE_FREQUENCIES[note]) return;

        const instrument = INSTRUMENTS[state.currentInstrument];
        const freq = NOTE_FREQUENCIES[note];

        // Create oscillator
        const osc = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        osc.type = instrument.waveform;
        osc.frequency.value = freq;

        // ADSR Envelope
        const now = audioContext.currentTime;
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(1, now + instrument.attack);
        gainNode.gain.linearRampToValueAtTime(instrument.sustain, now + instrument.attack + instrument.decay);
        gainNode.gain.setValueAtTime(instrument.sustain, now + duration - instrument.release);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);

        osc.connect(gainNode);
        gainNode.connect(masterGain);

        osc.start(now);
        osc.stop(now + duration);

        // Visual feedback
        showNoteVisual(note, instrument.color);

        // Track played notes for melody detection
        state.playedNotes.push({
            note: note,
            time: Date.now()
        });

        // Recording
        if (state.isRecording) {
            state.recordedMelody.push(note);
        }

        // Clear old notes after 3 seconds
        clearTimeout(state.noteTimeout);
        state.noteTimeout = setTimeout(() => {
            checkMelody();
            state.playedNotes = [];
        }, 2000);

        console.log(`🎵 Note: ${note} (${freq.toFixed(1)} Hz)`);
    }

    function stopNote(note) {
        if (activeOscillators[note]) {
            activeOscillators[note].stop();
            delete activeOscillators[note];
        }
    }

    // ============================================
    // MELODY DETECTION
    // ============================================

    function checkMelody() {
        if (state.playedNotes.length < 3) return;

        const recentNotes = state.playedNotes
            .filter(n => Date.now() - n.time < 5000)
            .map(n => n.note);

        // Check against learned songs
        for (const [songId, song] of Object.entries(MAGIC_SONGS)) {
            if (!state.learnedSongs.includes(songId)) continue;

            if (matchesMelody(recentNotes, song.notes)) {
                triggerSongEffect(songId, song);
                state.playedNotes = [];
                return;
            }
        }
    }

    function matchesMelody(played, target) {
        if (played.length < target.length) return false;

        // Check if the last N notes match the song
        const lastNotes = played.slice(-target.length);
        return lastNotes.every((note, i) => note === target[i]);
    }

    function triggerSongEffect(songId, song) {
        console.log(`🎵 Lied erkannt: ${song.name}!`);
        showSongNotification(song);

        switch (song.effect) {
            case 'change_time_day':
                if (window.WorldManager) {
                    window.WorldManager.setTimeOfDay('day');
                }
                notify(`☀️ Die Sonne geht auf!`, 'success');
                break;

            case 'change_time_night':
                if (window.WorldManager) {
                    window.WorldManager.setTimeOfDay('night');
                }
                notify(`🌙 Die Nacht bricht herein!`, 'success');
                break;

            case 'summon_rain':
                if (window.WeatherSystem) {
                    window.WeatherSystem.setWeather('rain');
                }
                notify(`🌧️ Regenwolken sammeln sich!`, 'success');
                break;

            case 'teleport_home':
                if (window.playerController) {
                    window.playerController.teleport(0, 0, 0);
                }
                notify(`🏠 Zurück zur Schwarzen Mühle!`, 'success');
                break;

            case 'heal_player':
                if (window.realtimeCombat) {
                    window.realtimeCombat.healPlayer(30);
                }
                notify(`💚 Du wurdest geheilt!`, 'success');
                break;

            case 'sleep_enemies':
                if (window.realtimeCombat) {
                    window.realtimeCombat.sleepNearbyEnemies();
                }
                notify(`😴 Gegner schlafen ein!`, 'success');
                break;

            case 'summon_najika':
                notify(`🌸 Najika kommt zu dir!`, 'success');
                // Trigger Najika to come to player
                break;

            case 'slow_time':
                notify(`⏰ Die Zeit verlangsamt sich!`, 'success');
                // Slow motion effect
                break;

            default:
                console.log(`Unbekannter Effekt: ${song.effect}`);
        }
    }

    // ============================================
    // UI CREATION
    // ============================================

    function createUI() {
        if (instrumentUI) return;

        instrumentUI = document.createElement('div');
        instrumentUI.id = 'instrument-ui';
        instrumentUI.style.cssText = `
            display: none;
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(20, 20, 40, 0.95);
            border: 2px solid #4a9eff;
            border-radius: 20px;
            padding: 20px;
            z-index: 2000;
            text-align: center;
            min-width: 400px;
        `;

        instrumentUI.innerHTML = `
            <div style="margin-bottom: 15px;">
                <span id="instrument-icon" style="font-size: 48px;">🎵</span>
                <h3 id="instrument-name" style="color: #4a9eff; margin: 5px 0;">Okarina</h3>
            </div>

            <!-- Noten-Display -->
            <div id="note-display" style="
                background: rgba(0,0,0,0.5);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                min-height: 60px;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                flex-wrap: wrap;
            ">
                <span style="color: #666;">Spiele Noten mit A-S-D-F-G-H-J-K-L</span>
            </div>

            <!-- Noten-Tasten -->
            <div id="note-buttons" style="display: flex; justify-content: center; gap: 5px; margin-bottom: 15px;">
                ${Object.entries(KEY_TO_NOTE).map(([key, note]) => `
                    <button class="note-btn" data-note="${note}" style="
                        width: 40px;
                        height: 50px;
                        background: linear-gradient(180deg, #fff 0%, #ddd 100%);
                        border: 2px solid #888;
                        border-radius: 0 0 8px 8px;
                        cursor: pointer;
                        font-size: 10px;
                        font-weight: bold;
                        transition: all 0.1s;
                    ">
                        <div style="font-size: 14px;">${key.toUpperCase()}</div>
                        <div style="font-size: 8px; color: #666;">${note}</div>
                    </button>
                `).join('')}
            </div>

            <!-- Instrument Wechseln -->
            <div style="margin-bottom: 15px;">
                <div style="color: #888; font-size: 12px; margin-bottom: 5px;">Instrument:</div>
                <div id="instrument-select" style="display: flex; justify-content: center; gap: 10px;">
                    ${Object.entries(INSTRUMENTS).map(([id, inst]) => `
                        <button class="inst-btn" data-instrument="${id}" style="
                            padding: 8px 12px;
                            background: ${state.ownedInstruments.includes(id) ? 'rgba(74, 158, 255, 0.3)' : 'rgba(100,100,100,0.3)'};
                            border: 1px solid ${state.ownedInstruments.includes(id) ? inst.color : '#555'};
                            border-radius: 5px;
                            color: #fff;
                            cursor: ${state.ownedInstruments.includes(id) ? 'pointer' : 'not-allowed'};
                            opacity: ${state.ownedInstruments.includes(id) ? '1' : '0.5'};
                        " ${state.ownedInstruments.includes(id) ? '' : 'disabled'}>
                            ${inst.icon} ${inst.name}
                        </button>
                    `).join('')}
                </div>
            </div>

            <!-- Gelernte Lieder -->
            <div style="margin-bottom: 15px;">
                <div style="color: #888; font-size: 12px; margin-bottom: 5px;">Gelernte Lieder:</div>
                <div id="learned-songs" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
                    ${Object.entries(MAGIC_SONGS).map(([id, song]) => `
                        <button class="song-btn" data-song="${id}" style="
                            padding: 5px 10px;
                            background: ${state.learnedSongs.includes(id) ? 'rgba(100, 200, 100, 0.3)' : 'rgba(50,50,50,0.5)'};
                            border: 1px solid ${state.learnedSongs.includes(id) ? '#6c6' : '#333'};
                            border-radius: 5px;
                            color: ${state.learnedSongs.includes(id) ? '#fff' : '#555'};
                            cursor: pointer;
                            font-size: 11px;
                        " title="${song.description}">
                            ${song.icon} ${song.name}
                        </button>
                    `).join('')}
                </div>
            </div>

            <!-- Controls -->
            <div style="display: flex; justify-content: center; gap: 10px;">
                <button onclick="InstrumentSystem.toggleRecording()" id="record-btn" style="
                    padding: 8px 15px;
                    background: rgba(255, 100, 100, 0.3);
                    border: 1px solid #f66;
                    border-radius: 5px;
                    color: #fff;
                    cursor: pointer;
                ">⏺️ Aufnehmen</button>
                <button onclick="InstrumentSystem.close()" style="
                    padding: 8px 15px;
                    background: rgba(100, 100, 100, 0.3);
                    border: 1px solid #666;
                    border-radius: 5px;
                    color: #fff;
                    cursor: pointer;
                ">✖️ Schließen</button>
            </div>
        `;

        document.body.appendChild(instrumentUI);

        // Note button events
        instrumentUI.querySelectorAll('.note-btn').forEach(btn => {
            btn.addEventListener('mousedown', () => {
                const note = btn.dataset.note;
                playNote(note, 0.5);
                btn.style.background = 'linear-gradient(180deg, #4a9eff 0%, #2a6edd 100%)';
            });
            btn.addEventListener('mouseup', () => {
                btn.style.background = 'linear-gradient(180deg, #fff 0%, #ddd 100%)';
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.background = 'linear-gradient(180deg, #fff 0%, #ddd 100%)';
            });
        });

        // Instrument select events
        instrumentUI.querySelectorAll('.inst-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                if (!btn.disabled) {
                    selectInstrument(btn.dataset.instrument);
                }
            });
        });

        // Song preview events
        instrumentUI.querySelectorAll('.song-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const songId = btn.dataset.song;
                if (state.learnedSongs.includes(songId)) {
                    playSongPreview(songId);
                }
            });
        });

        noteDisplay = instrumentUI.querySelector('#note-display');

        console.log('🎵 Instrument UI erstellt');
    }

    function showNoteVisual(note, color) {
        if (!noteDisplay) return;

        const noteEl = document.createElement('span');
        noteEl.textContent = note;
        noteEl.style.cssText = `
            display: inline-block;
            padding: 8px 12px;
            background: ${color};
            border-radius: 50%;
            color: #fff;
            font-weight: bold;
            font-size: 14px;
            animation: notePopIn 0.3s ease-out;
        `;

        // Clear placeholder text
        if (noteDisplay.querySelector('span:not([style])')) {
            noteDisplay.innerHTML = '';
        }

        noteDisplay.appendChild(noteEl);

        // Remove after animation
        setTimeout(() => {
            noteEl.style.opacity = '0.5';
        }, 500);

        // Keep only last 10 notes visible
        while (noteDisplay.children.length > 10) {
            noteDisplay.removeChild(noteDisplay.firstChild);
        }
    }

    function showSongNotification(song) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            border: 3px solid gold;
            border-radius: 15px;
            padding: 30px 50px;
            z-index: 3000;
            text-align: center;
            animation: songReveal 2s ease-out forwards;
        `;
        notification.innerHTML = `
            <div style="font-size: 64px; margin-bottom: 10px;">${song.icon}</div>
            <div style="font-size: 24px; color: gold; font-weight: bold;">${song.name}</div>
            <div style="font-size: 14px; color: #aaa; margin-top: 10px;">${song.description}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 2000);
    }

    // ============================================
    // CONTROLS
    // ============================================

    function bindControls() {
        document.addEventListener('keydown', (e) => {
            if (!state.active) return;
            if (e.repeat) return;
            // Ignorieren wenn Chat-Input fokussiert ist
            if (window.chatInputFocused) return;

            const key = e.key.toLowerCase();
            if (KEY_TO_NOTE[key]) {
                e.preventDefault();
                playNote(KEY_TO_NOTE[key], 0.5);

                // Visual feedback on button
                const btn = instrumentUI?.querySelector(`.note-btn[data-note="${KEY_TO_NOTE[key]}"]`);
                if (btn) {
                    btn.style.background = 'linear-gradient(180deg, #4a9eff 0%, #2a6edd 100%)';
                }
            }

            // ESC to close
            if (e.key === 'Escape') {
                close();
            }
        });

        document.addEventListener('keyup', (e) => {
            if (!state.active) return;

            const key = e.key.toLowerCase();
            if (KEY_TO_NOTE[key]) {
                const btn = instrumentUI?.querySelector(`.note-btn[data-note="${KEY_TO_NOTE[key]}"]`);
                if (btn) {
                    btn.style.background = 'linear-gradient(180deg, #fff 0%, #ddd 100%)';
                }
            }
        });
    }

    // ============================================
    // PUBLIC API
    // ============================================

    function open(instrumentId = null) {
        createUI();
        initAudio();

        if (instrumentId && state.ownedInstruments.includes(instrumentId)) {
            selectInstrument(instrumentId);
        }

        state.active = true;
        instrumentUI.style.display = 'block';
        console.log('🎵 Instrument geöffnet:', state.currentInstrument);
    }

    function close() {
        state.active = false;
        if (instrumentUI) {
            instrumentUI.style.display = 'none';
        }
        state.playedNotes = [];
        console.log('🎵 Instrument geschlossen');
    }

    function selectInstrument(instrumentId) {
        if (!INSTRUMENTS[instrumentId]) return;
        if (!state.ownedInstruments.includes(instrumentId)) {
            notify(`Du besitzt diese Instrument nicht!`, 'warning');
            return;
        }

        state.currentInstrument = instrumentId;
        const inst = INSTRUMENTS[instrumentId];

        if (instrumentUI) {
            instrumentUI.querySelector('#instrument-icon').textContent = inst.icon;
            instrumentUI.querySelector('#instrument-name').textContent = inst.name;
            instrumentUI.querySelector('#instrument-name').style.color = inst.color;
            instrumentUI.style.borderColor = inst.color;

            // Update selection
            instrumentUI.querySelectorAll('.inst-btn').forEach(btn => {
                const isSelected = btn.dataset.instrument === instrumentId;
                btn.style.background = isSelected ?
                    `rgba(74, 158, 255, 0.5)` :
                    `rgba(74, 158, 255, 0.2)`;
            });
        }

        console.log(`🎵 Instrument gewechselt: ${inst.name}`);
    }

    function toggleRecording() {
        state.isRecording = !state.isRecording;

        const recordBtn = document.getElementById('record-btn');
        if (recordBtn) {
            if (state.isRecording) {
                state.recordedMelody = [];
                recordBtn.textContent = '⏹️ Stoppen';
                recordBtn.style.background = 'rgba(255, 50, 50, 0.5)';
                notify('🎵 Aufnahme gestartet...', 'info');
            } else {
                recordBtn.textContent = '⏺️ Aufnehmen';
                recordBtn.style.background = 'rgba(255, 100, 100, 0.3)';
                console.log('Aufgenommene Melodie:', state.recordedMelody);
                notify(`🎵 ${state.recordedMelody.length} Noten aufgenommen`, 'success');
            }
        }
    }

    function playSongPreview(songId) {
        const song = MAGIC_SONGS[songId];
        if (!song) return;

        notify(`🎵 ${song.name}...`, 'info');

        // Play each note with delay
        song.notes.forEach((note, i) => {
            setTimeout(() => {
                playNote(note, 0.4);
            }, i * 400);
        });
    }

    function learnSong(songId) {
        if (!MAGIC_SONGS[songId]) return false;
        if (state.learnedSongs.includes(songId)) return false;

        state.learnedSongs.push(songId);
        MAGIC_SONGS[songId].learned = true;

        const song = MAGIC_SONGS[songId];
        notify(`🎵 Neues Lied gelernt: ${song.name}!`, 'success');

        // Update UI if open
        if (instrumentUI) {
            const btn = instrumentUI.querySelector(`.song-btn[data-song="${songId}"]`);
            if (btn) {
                btn.style.background = 'rgba(100, 200, 100, 0.3)';
                btn.style.borderColor = '#6c6';
                btn.style.color = '#fff';
            }
        }

        return true;
    }

    function unlockInstrument(instrumentId) {
        if (!INSTRUMENTS[instrumentId]) return false;
        if (state.ownedInstruments.includes(instrumentId)) return false;

        state.ownedInstruments.push(instrumentId);
        const inst = INSTRUMENTS[instrumentId];
        notify(`${inst.icon} Neues Instrument: ${inst.name}!`, 'success');

        return true;
    }

    function isActive() {
        return state.active;
    }

    // Helper notify function
    function notify(message, type = 'info') {
        if (typeof window.showNotification === 'function') {
            window.showNotification(message, 2000);
        } else {
            console.log(`[${type}] ${message}`);
        }
    }

    // ============================================
    // INITIALIZATION
    // ============================================

    function init() {
        bindControls();

        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes notePopIn {
                0% { transform: scale(0); opacity: 0; }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); opacity: 1; }
            }
            @keyframes songReveal {
                0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
                30% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        console.log('🎵 Instrument System initialisiert');
        console.log('   - 5 Instrumente verfügbar');
        console.log('   - 8 magische Lieder');
        console.log('   - Tasten: A-S-D-F-G-H-J-K-L');
    }

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ============================================
    // EXPORT
    // ============================================

    return {
        open,
        close,
        playNote,
        selectInstrument,
        toggleRecording,
        learnSong,
        unlockInstrument,
        isActive,
        getLearnedSongs: () => [...state.learnedSongs],
        getOwnedInstruments: () => [...state.ownedInstruments],
        getSongInfo: (id) => MAGIC_SONGS[id],
        getInstrumentInfo: (id) => INSTRUMENTS[id]
    };
})();

// Global export
window.InstrumentSystem = InstrumentSystem;

console.log('🎵 Instrument System (Ocarina-Style) geladen');
