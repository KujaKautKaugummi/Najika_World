// 🎵 INSTRUMENT PLAYER - Digivice Modul (Zelda Ocarina of Time Style)
// ZWEI MODI: 1) Lehrer-Modus (Najika zeigt vor), 2) Freies Spielen

class InstrumentPlayer {
    constructor() {
        this.audioContext = null;
        this.isVisible = false;
        this.currentMode = 'free'; // 'free' or 'teacher'

        // 🎵 3D Animation (if available)
        this.animator = null;

        // Recording
        this.isRecording = false;
        this.recordedNotes = [];
        this.recordingStartTime = 0;

        // Teacher Mode
        this.currentLesson = null;
        this.lessonIndex = 0;

        // Note mapping (Zelda OoT style)
        this.noteMapping = {
            'q': { note: 'C4', freq: 261.63, color: '#3498db', name: 'C' },
            'w': { note: 'D4', freq: 293.66, color: '#2ecc71', name: 'D' },
            'e': { note: 'E4', freq: 329.63, color: '#f39c12', name: 'E' },
            'r': { note: 'F4', freq: 349.23, color: '#e74c3c', name: 'F' },
            't': { note: 'G4', freq: 392.00, color: '#9b59b6', name: 'G' },
            'y': { note: 'A4', freq: 440.00, color: '#1abc9c', name: 'A' }
        };

        // Lektionen (nur für Teacher Mode)
        this.lessons = {
            'zelda_lullaby': {
                name: "Zelda's Lullaby",
                notes: ['e', 'w', 'q', 'e', 'w', 'q'],
                delays: [500, 500, 500, 500, 500, 500],
                description: "Die beruhigende Melodie der königlichen Familie"
            },
            'song_of_time': {
                name: "Song of Time",
                notes: ['t', 'q', 'w', 't', 'q', 'w'],
                delays: [400, 400, 400, 400, 400, 400],
                description: "Kontrolliere die Zeit selbst"
            },
            'saria_song': {
                name: "Saria's Song",
                notes: ['r', 'e', 'w', 'r', 'e', 'w'],
                delays: [350, 350, 350, 350, 350, 350],
                description: "Deine Freundin aus dem Kokiri-Wald"
            },
            'c_major': {
                name: "C-Major Tonleiter",
                notes: ['q', 'w', 'e', 'r', 't', 'y'],
                delays: [300, 300, 300, 300, 300, 300],
                description: "Die Grundlage aller Melodien"
            }
        };

        this.createUI();
        this.initAudio();
    }

    initAudio() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    createUI() {
        const container = document.createElement('div');
        container.id = 'instrument-player-container';
        container.style.cssText = `
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 600px;
            background: linear-gradient(135deg, #2c3e50, #34495e);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            z-index: 10000;
            color: white;
            font-family: 'Arial', sans-serif;
        `;

        container.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="margin: 0; color: #ecf0f1;">🎵 Instrument Player</h2>
                <button id="instrument-close-btn" style="
                    background: #e74c3c;
                    border: none;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                ">✕</button>
            </div>

            <!-- Mode Toggle -->
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <button id="mode-free" class="mode-btn active" data-mode="free" style="
                    flex: 1;
                    padding: 10px;
                    border: 2px solid #3498db;
                    background: #3498db;
                    color: white;
                    border-radius: 10px;
                    cursor: pointer;
                    font-weight: bold;
                ">🎹 Freies Spielen</button>
                <button id="mode-teacher" class="mode-btn" data-mode="teacher" style="
                    flex: 1;
                    padding: 10px;
                    border: 2px solid #3498db;
                    background: transparent;
                    color: #3498db;
                    border-radius: 10px;
                    cursor: pointer;
                    font-weight: bold;
                ">🎓 Lehrer-Modus</button>
            </div>

            <!-- Free Play Mode -->
            <div id="free-mode-content" style="display: block;">
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="margin: 0 0 10px 0;">Mundharmonika</h3>
                    <div id="harmonica-keys" style="display: flex; gap: 5px; justify-content: center;"></div>
                </div>

                <div style="display: flex; gap: 10px;">
                    <button id="record-btn" style="
                        flex: 1;
                        padding: 10px;
                        background: #e74c3c;
                        border: none;
                        color: white;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">⏺ Record</button>
                    <button id="play-recording-btn" style="
                        flex: 1;
                        padding: 10px;
                        background: #2ecc71;
                        border: none;
                        color: white;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    " disabled>▶ Play</button>
                </div>
            </div>

            <!-- Teacher Mode -->
            <div id="teacher-mode-content" style="display: none;">
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                        <div id="najika-avatar" style="
                            width: 60px;
                            height: 60px;
                            background: linear-gradient(135deg, #e91e63, #9c27b0);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 30px;
                        ">👩</div>
                        <div>
                            <h3 style="margin: 0;">Najika - Musiklehrerin</h3>
                            <p id="najika-speech" style="
                                margin: 5px 0 0 0;
                                font-size: 14px;
                                color: #ecf0f1;
                            ">Wähle eine Lektion zum Üben!</p>
                        </div>
                    </div>
                </div>

                <div id="lessons-list" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                </div>

                <div id="lesson-progress" style="display: none; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span id="lesson-name"></span>
                        <span id="lesson-step">0/0</span>
                    </div>
                    <div id="lesson-notes" style="display: flex; gap: 5px; justify-content: center; margin-bottom: 10px;"></div>
                    <button id="play-lesson-btn" style="
                        width: 100%;
                        padding: 10px;
                        background: #9b59b6;
                        border: none;
                        color: white;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">▶ Najika spielt vor</button>
                </div>
            </div>

            <div style="margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 8px; font-size: 12px; color: #bdc3c7;">
                <strong>Tasten:</strong> Q W E R T Y = C D E F G A
            </div>
        `;

        document.body.appendChild(container);

        this.container = container;
        this.setupEventListeners();
        this.createHarmonicaKeys();
        this.createLessonsList();
    }

    createHarmonicaKeys() {
        const container = document.getElementById('harmonica-keys');

        Object.entries(this.noteMapping).forEach(([key, data]) => {
            const keyElement = document.createElement('div');
            keyElement.className = 'harmonica-key';
            keyElement.dataset.key = key;
            keyElement.style.cssText = `
                width: 80px;
                height: 100px;
                background: linear-gradient(135deg, ${data.color}, ${data.color}dd);
                border-radius: 10px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.1s;
                border: 3px solid rgba(255,255,255,0.3);
            `;

            keyElement.innerHTML = `
                <div style="font-size: 24px; font-weight: bold;">${key.toUpperCase()}</div>
                <div style="font-size: 14px; margin-top: 5px;">${data.name}</div>
            `;

            keyElement.addEventListener('click', () => this.playNote(key));
            container.appendChild(keyElement);
        });
    }

    createLessonsList() {
        const container = document.getElementById('lessons-list');

        Object.entries(this.lessons).forEach(([id, lesson]) => {
            const btn = document.createElement('button');
            btn.style.cssText = `
                padding: 15px;
                background: linear-gradient(135deg, #9b59b6, #8e44ad);
                border: none;
                color: white;
                border-radius: 10px;
                cursor: pointer;
                text-align: left;
            `;
            btn.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 5px;">${lesson.name}</div>
                <div style="font-size: 11px; opacity: 0.8;">${lesson.description}</div>
            `;
            btn.addEventListener('click', () => this.selectLesson(id));
            container.appendChild(btn);
        });
    }

    setupEventListeners() {
        // Close button
        document.getElementById('instrument-close-btn').addEventListener('click', () => this.hide());

        // Mode toggle
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchMode(btn.dataset.mode));
        });

        // Recording
        document.getElementById('record-btn').addEventListener('click', () => this.toggleRecording());
        document.getElementById('play-recording-btn').addEventListener('click', () => this.playRecording());

        // Keyboard
        document.addEventListener('keydown', (e) => {
            if (!this.isVisible) return;
            const key = e.key.toLowerCase();
            if (this.noteMapping[key]) {
                this.playNote(key);
            }
        });
    }

    switchMode(mode) {
        this.currentMode = mode;

        // Update buttons
        document.querySelectorAll('.mode-btn').forEach(btn => {
            if (btn.dataset.mode === mode) {
                btn.style.background = '#3498db';
                btn.style.color = 'white';
                btn.classList.add('active');
            } else {
                btn.style.background = 'transparent';
                btn.style.color = '#3498db';
                btn.classList.remove('active');
            }
        });

        // Show/hide content
        document.getElementById('free-mode-content').style.display = mode === 'free' ? 'block' : 'none';
        document.getElementById('teacher-mode-content').style.display = mode === 'teacher' ? 'block' : 'none';
    }

    playNote(key) {
        const note = this.noteMapping[key];
        if (!note) return;

        this.initAudio();

        // Visual feedback
        const keyElement = document.querySelector(`.harmonica-key[data-key="${key}"]`);
        if (keyElement) {
            keyElement.style.transform = 'scale(1.1)';
            keyElement.style.boxShadow = `0 0 20px ${note.color}`;
            setTimeout(() => {
                keyElement.style.transform = 'scale(1)';
                keyElement.style.boxShadow = 'none';
            }, 200);
        }

        // 🎵 3D Animation - Play note particles
        if (this.animator) {
            this.animator.playNote(note.note, note.color);
        }

        // Play sound
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.value = note.freq;
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.5);

        // Recording
        if (this.isRecording) {
            this.recordedNotes.push({
                key: key,
                time: Date.now() - this.recordingStartTime
            });
        }
    }

    toggleRecording() {
        const btn = document.getElementById('record-btn');

        if (!this.isRecording) {
            this.isRecording = true;
            this.recordedNotes = [];
            this.recordingStartTime = Date.now();
            btn.textContent = '⏹ Stop';
            btn.style.background = '#95a5a6';
        } else {
            this.isRecording = false;
            btn.textContent = '⏺ Record';
            btn.style.background = '#e74c3c';
            document.getElementById('play-recording-btn').disabled = false;
        }
    }

    async playRecording() {
        if (this.recordedNotes.length === 0) return;

        const btn = document.getElementById('play-recording-btn');
        btn.disabled = true;

        for (const note of this.recordedNotes) {
            await new Promise(resolve => setTimeout(resolve, note.time));
            this.playNote(note.key);
        }

        btn.disabled = false;
    }

    selectLesson(lessonId) {
        this.currentLesson = this.lessons[lessonId];
        this.lessonIndex = 0;

        document.getElementById('lesson-progress').style.display = 'block';
        document.getElementById('lesson-name').textContent = this.currentLesson.name;
        document.getElementById('lesson-step').textContent = `0/${this.currentLesson.notes.length}`;
        document.getElementById('najika-speech').textContent = `Gut! Lass uns "${this.currentLesson.name}" üben!`;

        // Show notes
        const notesContainer = document.getElementById('lesson-notes');
        notesContainer.innerHTML = '';
        this.currentLesson.notes.forEach((key, i) => {
            const note = this.noteMapping[key];
            const div = document.createElement('div');
            div.style.cssText = `
                width: 50px;
                height: 50px;
                background: ${note.color};
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 18px;
                opacity: 0.5;
            `;
            div.textContent = key.toUpperCase();
            div.dataset.index = i;
            notesContainer.appendChild(div);
        });

        document.getElementById('play-lesson-btn').addEventListener('click', () => this.playLesson());
    }

    async playLesson() {
        if (!this.currentLesson) return;

        const btn = document.getElementById('play-lesson-btn');
        btn.disabled = true;
        btn.textContent = '🎵 Najika spielt...';

        document.getElementById('najika-speech').textContent = 'Hör gut zu!';

        const notesElements = document.querySelectorAll('#lesson-notes > div');

        for (let i = 0; i < this.currentLesson.notes.length; i++) {
            const key = this.currentLesson.notes[i];
            const delay = this.currentLesson.delays[i];

            // Highlight note
            notesElements[i].style.opacity = '1';
            notesElements[i].style.transform = 'scale(1.2)';

            this.playNote(key);

            await new Promise(resolve => setTimeout(resolve, delay));

            notesElements[i].style.transform = 'scale(1)';
        }

        // Reset
        setTimeout(() => {
            notesElements.forEach(el => el.style.opacity = '0.5');
            btn.disabled = false;
            btn.textContent = '▶ Najika spielt vor';
            document.getElementById('najika-speech').textContent = 'Jetzt du! Versuche es nachzuspielen!';
        }, 500);
    }

    show() {
        this.isVisible = true;
        this.container.style.display = 'block';
        this.initAudio();

        // 🎵 Start 3D animation
        if (this.animator) {
            this.animator.startPlaying('harmonica');
        }
    }

    hide() {
        this.isVisible = false;
        this.container.style.display = 'none';

        // 🎵 Stop 3D animation
        if (this.animator) {
            this.animator.stopPlaying();
        }
    }

    /**
     * Set 3D animator reference (called from 3d_scene.js)
     * @param {InstrumentAnimator} animator
     */
    setAnimator(animator) {
        this.animator = animator;
        console.log('🎵 Animator connected to InstrumentPlayer');
    }
}

// Initialize
window.instrumentPlayer = new InstrumentPlayer();
