/**
 * NAJIKA WORLD - SLIME COMPANION SYSTEM V2
 * =========================================
 * Kombiniert: DQM (Synthese) + Digimon V-Pet (Pflege) + Fortnite (Begleiter)
 *
 * WICHTIG: Alle Monster im Spiel = Slimes (verschiedene Formen)
 * Monster-Kämpfe sind OPTIONAL! (Skyrim-Freiheit)
 *
 * Features:
 * - 9 Basis-Typen + 10 Hybrids = 19 Slime-Formen
 * - 6 Evolution-Stufen (Zeit + Training + Pflege)
 * - 4 Evolution-Pfade (PERFECT/GOOD/NORMAL/BAD)
 * - V-Pet Pflege (Hunger/Strength Hearts)
 * - DQM Synthese (2→1, +N System)
 * - Rescue System (Hardcore: 1x pro 24h)
 * - Skill Copy (10-15% von Gegnern)
 * - Passive Boni (für Nicht-Kämpfer!)
 *
 * Backend API Endpoints:
 * - POST /api/slime/status
 * - POST /api/slime/create
 * - POST /api/slime/feed
 * - POST /api/slime/train
 * - POST /api/slime/play
 * - POST /api/slime/evolve
 * - POST /api/slime/synthesize
 */

// =============================================================================
// CONSTANTS & CONFIG
// =============================================================================

const SLIME_CONFIG = {
    API_BASE: window.API_BASE_URL || 'http://localhost:8000',

    // Evolution Stufen (6 Stufen)
    STAGES: {
        1: { name: 'EGG', icon: '🥚', time: 0 },
        2: { name: 'BABY', icon: '👶', time: 3600 }, // 1h
        3: { name: 'KIND', icon: '🧒', time: 86400 }, // 24h
        4: { name: 'REIF', icon: '🧑', time: 259200 }, // 3 Tage
        5: { name: 'CHAMPION', icon: '👑', time: 604800 }, // 7 Tage
        6: { name: 'ULTIMATIV', icon: '⭐', time: 1209600 }, // 14 Tage
    },

    // Evolution Pfade
    PATHS: {
        PERFECT: { name: 'Perfect', color: '#FFD700' },
        GOOD: { name: 'Good', color: '#4CAF50' },
        NORMAL: { name: 'Normal', color: '#2196F3' },
        BAD: { name: 'Bad', color: '#9E9E9E' }
    },

    // 9 Basis Slime-Typen
    TYPES: {
        moos_schleim: {
            name: 'Moos-Schleim',
            color: '#4CAF50',
            icon: '🌿',
            region: 'Samtmoos-Tiefwald',
            element: 'Nature'
        },
        frost_schleim: {
            name: 'Frost-Schleim',
            color: '#81D4FA',
            icon: '❄️',
            region: 'Reich der Drei',
            element: 'Ice'
        },
        wasser_schleim: {
            name: 'Wasser-Schleim',
            color: '#2196F3',
            icon: '💧',
            region: 'Salzwind-Küste',
            element: 'Water'
        },
        blitz_schleim: {
            name: 'Blitz-Schleim',
            color: '#9C27B0',
            icon: '⚡',
            region: 'Blitzebene',
            element: 'Lightning'
        },
        gift_schleim: {
            name: 'Gift-Schleim',
            color: '#1B5E20',
            icon: '☠️',
            region: 'Grünschlamm-Sumpf',
            element: 'Poison'
        },
        magma_schleim: {
            name: 'Magma-Schleim',
            color: '#FF5722',
            icon: '🔥',
            region: 'Magmaströme',
            element: 'Fire'
        },
        sand_schleim: {
            name: 'Sand-Schleim',
            color: '#FFD54F',
            icon: '🏜️',
            region: 'Heiße Dünen',
            element: 'Earth'
        },
        kristall_schleim: {
            name: 'Kristall-Schleim',
            color: '#E0E0E0',
            icon: '💎',
            region: 'Tiefenhöhlen',
            element: 'Crystal'
        },
        goetter_schleim: {
            name: 'Götter-Schleim',
            color: 'rainbow',
            icon: '🌈',
            region: 'Götterfels',
            element: 'Divine'
        }
    },

    // 10 Hybrid-Typen (aus Synthese)
    HYBRIDS: {
        sumpf_schleim: { name: 'Sumpf-Schleim', color: '#5D4037', icon: '🌊' },
        dampf_schleim: { name: 'Dampf-Schleim', color: '#B0BEC5', icon: '💨' },
        glas_schleim: { name: 'Glas-Schleim', color: '#FFF176', icon: '✨' },
        toxin_kristall: { name: 'Toxin-Kristall', color: '#7B1FA2', icon: '☢️' },
        pilz_schleim: { name: 'Pilz-Schleim', color: '#795548', icon: '🍄' },
        juwelen_schleim: { name: 'Juwelen-Schleim', color: '#E91E63', icon: '💍' },
        eisberg_schleim: { name: 'Eisberg-Schleim', color: '#4FC3F7', icon: '🧊' },
        sturm_schleim: { name: 'Sturm-Schleim', color: '#5C6BC0', icon: '⛈️' },
        obsidian_schleim: { name: 'Obsidian-Schleim', color: '#212121', icon: '🖤' },
        winter_gruen: { name: 'Winter-Grün', color: '#00897B', icon: '🌲' }
    },

    // V-Pet Timings
    HUNGER_DECAY: 1800000, // 30 Min = 1 Herz verloren
    RESCUE_COOLDOWN: 86400000, // 24 Stunden

    // Update Interval
    UPDATE_INTERVAL: 5000 // 5 Sekunden
};

// =============================================================================
// SLIME COMPANION CLASS
// =============================================================================

class SlimeCompanion {
    constructor() {
        // Basic Info
        this.id = null;
        this.name = 'Schleim';
        this.slimeType = 'moos_schleim';
        this.stage = 1; // 1-6
        this.level = 1;
        this.plusValue = 0; // DQM +N System

        // V-Pet Hearts (Max 4)
        this.hungerHearts = 4;
        this.strengthHearts = 4;

        // Care & Training
        this.careMistakes = 0;
        this.effortHearts = 0;
        this.trainingCount = 0;

        // Battle Stats (OPTIONAL!)
        this.battles = 0;
        this.wins = 0;

        // Timestamps
        this.birthTime = Date.now();
        this.lastFed = Date.now();
        this.lastTrained = Date.now();
        this.lastPlayed = Date.now();
        this.evolutionTime = Date.now() + SLIME_CONFIG.STAGES[2].time * 1000;

        // Skills
        this.skills = ['tackle']; // Basis-Skill
        this.inheritedFrom = [];

        // State
        this.isSleeping = false;
        this.injuries = 0;
        this.isAlive = true;

        // Rescue System (WICHTIG!)
        this.rescueCharges = 1;
        this.lastRescueUsed = null;

        // Position (follows player)
        this.position = { x: 0, y: 0, z: 0 };

        // UI State
        this.uiVisible = true;

        console.log('🐾 Slime Companion System V2 initialized');
    }

    // =========================================================================
    // API CALLS
    // =========================================================================

    async loadFromBackend() {
        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.slime) {
                    this.fromJSON(data.slime);
                    console.log('✅ Slime loaded from backend');
                }
            }
        } catch (error) {
            console.error('❌ Failed to load slime:', error);
        }
    }

    async createNewSlime(slimeType, name) {
        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    slime_type: slimeType,
                    name: name
                })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.slime) {
                    this.fromJSON(data.slime);
                    console.log('✅ New slime created!');
                    this.showNotification(`🥚 ${name} wurde geboren!`, 5000);
                }
            }
        } catch (error) {
            console.error('❌ Failed to create slime:', error);
        }
    }

    async feed() {
        if (!this.id) return;

        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/feed`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: this.id })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.hungerHearts = data.hunger_hearts;
                    this.showNotification(`🍖 ${this.name} wurde gefüttert!`, 2000);
                } else {
                    this.showNotification(`⚠️ ${data.message}`, 2000);
                }
            }
        } catch (error) {
            console.error('❌ Feed failed:', error);
        }
    }

    async train() {
        if (!this.id) return;

        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/train`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: this.id })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.strengthHearts = data.strength_hearts;
                    this.trainingCount = data.training_count;
                    this.effortHearts = data.effort_hearts;
                    this.showNotification(`💪 ${this.name} hat trainiert!`, 2000);
                } else {
                    this.showNotification(`⚠️ ${data.message}`, 2000);
                }
            }
        } catch (error) {
            console.error('❌ Train failed:', error);
        }
    }

    async play() {
        if (!this.id) return;

        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/play`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: this.id })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.strengthHearts = data.strength_hearts;
                    this.showNotification(`😊 ${this.name} hat gespielt!`, 2000);
                } else {
                    this.showNotification(`⚠️ ${data.message}`, 2000);
                }
            }
        } catch (error) {
            console.error('❌ Play failed:', error);
        }
    }

    async evolve() {
        if (!this.id) return;

        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/evolve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: this.id })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.fromJSON(data.slime);
                    this.showNotification(`✨ EVOLUTION! ${data.message}`, 8000);
                } else {
                    this.showNotification(`⚠️ ${data.message}`, 3000);
                }
            }
        } catch (error) {
            console.error('❌ Evolution failed:', error);
        }
    }

    // =========================================================================
    // RESCUE SYSTEM (WICHTIG!)
    // =========================================================================

    canUseRescue() {
        if (this.rescueCharges <= 0) return false;

        if (this.lastRescueUsed) {
            const timeSince = Date.now() - this.lastRescueUsed;
            if (timeSince < SLIME_CONFIG.RESCUE_COOLDOWN) {
                return false;
            }
        }

        return true;
    }

    useRescue() {
        if (!this.canUseRescue()) {
            console.log('❌ Rescue not available!');
            return false;
        }

        this.rescueCharges--;
        this.lastRescueUsed = Date.now();

        console.log('💖 RESCUE ACTIVATED! You were saved!');
        this.showNotification('💖 RETTUNGSSCHLEIM! Du wurdest vor dem Tod gerettet!', 8000);

        // Trigger rescue effect
        if (window.realtimeCombat) {
            window.realtimeCombat.rescueActivated();
        }

        return true;
    }

    getRescueCooldownRemaining() {
        if (!this.lastRescueUsed) return 0;

        const timeSince = Date.now() - this.lastRescueUsed;
        const remaining = SLIME_CONFIG.RESCUE_COOLDOWN - timeSince;

        return Math.max(0, remaining);
    }

    // =========================================================================
    // SKILL COPY (10-15% Chance)
    // =========================================================================

    tryLearnSkill(enemySkill) {
        if (this.skills.length >= 20) {
            console.log('📚 Moveset full! (20/20)');
            return false;
        }

        // 10-15% chance
        const chance = 0.10 + Math.random() * 0.05;
        if (Math.random() < chance) {
            this.skills.push(enemySkill.name);

            console.log(`📚 ${this.name} learned "${enemySkill.name}"!`);
            this.showNotification(`📚 ${this.name} lernte "${enemySkill.name}"!`, 3000);

            return true;
        }

        return false;
    }

    // =========================================================================
    // GETTERS
    // =========================================================================

    getName() {
        const typeData = this.getTypeData();
        const stageData = SLIME_CONFIG.STAGES[this.stage];

        if (this.plusValue > 0) {
            return `${typeData.icon} ${this.name} +${this.plusValue}`;
        }
        return `${typeData.icon} ${this.name}`;
    }

    getTypeData() {
        return SLIME_CONFIG.TYPES[this.slimeType] ||
               SLIME_CONFIG.HYBRIDS[this.slimeType] ||
               { name: 'Unknown', color: '#888', icon: '❓' };
    }

    getStageData() {
        return SLIME_CONFIG.STAGES[this.stage] || SLIME_CONFIG.STAGES[1];
    }

    canEvolve() {
        return Date.now() >= this.evolutionTime && this.stage < 6 && this.isAlive;
    }

    getAgeHours() {
        return (Date.now() - this.birthTime) / 3600000;
    }

    getWinRate() {
        return this.battles > 0 ? (this.wins / this.battles) : 0;
    }

    // =========================================================================
    // UI
    // =========================================================================

    createUI() {
        let ui = document.getElementById('slime-companion-ui');
        if (!ui) {
            ui = document.createElement('div');
            ui.id = 'slime-companion-ui';
            document.body.appendChild(ui);
        }

        if (!this.uiVisible || !this.id) {
            ui.style.display = 'none';
            return;
        }

        ui.style.display = 'block';

        const typeData = this.getTypeData();
        const stageData = this.getStageData();
        const rescueCooldown = this.getRescueCooldownRemaining();
        const rescueAvailable = this.canUseRescue();
        const rescueTimeStr = rescueCooldown > 0
            ? `${Math.floor(rescueCooldown / 3600000)}h ${Math.floor((rescueCooldown % 3600000) / 60000)}m`
            : 'Bereit!';

        const canEvolve = this.canEvolve();

        ui.innerHTML = `
            <style>
                #slime-companion-ui {
                    position: fixed;
                    bottom: 120px;
                    left: 20px;
                    background: linear-gradient(135deg, rgba(0, 0, 0, 0.95), rgba(30, 30, 30, 0.95));
                    border: 2px solid ${typeData.color};
                    border-radius: 15px;
                    padding: 15px;
                    color: white;
                    font-family: 'Courier New', monospace;
                    z-index: 500;
                    min-width: 250px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
                }

                .slime-header {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 12px;
                    padding-bottom: 10px;
                    border-bottom: 1px solid ${typeData.color}40;
                }

                .slime-icon {
                    font-size: 36px;
                    filter: drop-shadow(0 0 8px ${typeData.color});
                }

                .slime-info {
                    flex: 1;
                }

                .slime-name {
                    font-weight: bold;
                    color: ${typeData.color};
                    font-size: 14px;
                }

                .slime-stage {
                    font-size: 10px;
                    color: #888;
                }

                .slime-hearts {
                    margin-bottom: 8px;
                }

                .heart-row {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 4px;
                }

                .heart-label {
                    font-size: 11px;
                    color: #aaa;
                }

                .hearts {
                    display: flex;
                    gap: 3px;
                }

                .heart {
                    width: 16px;
                    height: 16px;
                    display: inline-block;
                }

                .slime-stats {
                    display: flex;
                    gap: 12px;
                    font-size: 11px;
                    color: #aaa;
                    margin-bottom: 10px;
                    padding: 8px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 8px;
                }

                .slime-rescue {
                    background: ${rescueAvailable ? 'rgba(76, 175, 80, 0.2)' : 'rgba(255, 0, 0, 0.1)'};
                    border: 1px solid ${rescueAvailable ? '#4CAF50' : '#ff4444'};
                    padding: 8px;
                    border-radius: 8px;
                    font-size: 11px;
                    margin-bottom: 10px;
                }

                .rescue-title {
                    color: ${rescueAvailable ? '#4CAF50' : '#ff6666'};
                    font-weight: bold;
                }

                .rescue-cooldown {
                    color: #888;
                    font-size: 10px;
                }

                .slime-buttons {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 6px;
                    margin-top: 10px;
                }

                .slime-btn {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 6px;
                    padding: 8px;
                    color: white;
                    font-size: 11px;
                    cursor: pointer;
                    transition: all 0.2s;
                    font-family: 'Courier New', monospace;
                }

                .slime-btn:hover {
                    background: rgba(255, 255, 255, 0.2);
                    border-color: ${typeData.color};
                }

                .slime-btn:active {
                    transform: scale(0.95);
                }

                .slime-btn.evolve {
                    grid-column: 1 / -1;
                    background: linear-gradient(90deg, #FFD700, #FFA500);
                    border-color: #FFD700;
                    color: #000;
                    font-weight: bold;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0%, 100% { box-shadow: 0 0 10px #FFD700; }
                    50% { box-shadow: 0 0 20px #FFA500; }
                }

                .slime-close {
                    position: absolute;
                    top: 8px;
                    right: 8px;
                    background: rgba(255, 255, 255, 0.1);
                    border: none;
                    color: white;
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 12px;
                }
            </style>

            <button class="slime-close" onclick="window.slimeCompanion.toggleUI()">×</button>

            <div class="slime-header">
                <div class="slime-icon">${stageData.icon}</div>
                <div class="slime-info">
                    <div class="slime-name">${this.getName()}</div>
                    <div class="slime-stage">Lv.${this.level} | ${stageData.name}</div>
                </div>
            </div>

            <div class="slime-hearts">
                <div class="heart-row">
                    <span class="heart-label">❤️ Hunger</span>
                    <div class="hearts">
                        ${'❤️'.repeat(this.hungerHearts)}${'🖤'.repeat(4 - this.hungerHearts)}
                    </div>
                </div>
                <div class="heart-row">
                    <span class="heart-label">💪 Kraft</span>
                    <div class="hearts">
                        ${'💪'.repeat(this.strengthHearts)}${'🤍'.repeat(4 - this.strengthHearts)}
                    </div>
                </div>
            </div>

            <div class="slime-stats">
                <span>⭐ ${this.effortHearts} Effort</span>
                <span>❌ ${this.careMistakes} Mistakes</span>
                <span>📚 ${this.skills.length}/20</span>
            </div>

            <div class="slime-rescue">
                <div class="rescue-title">💖 Rescue: ${this.rescueCharges}/1</div>
                <div class="rescue-cooldown">${rescueTimeStr}</div>
            </div>

            <div class="slime-buttons">
                <button class="slime-btn" onclick="window.slimeCompanion.feed()">🍖 Füttern</button>
                <button class="slime-btn" onclick="window.slimeCompanion.play()">😊 Spielen</button>
                <button class="slime-btn" onclick="window.slimeCompanion.train()">💪 Training</button>
                <button class="slime-btn" onclick="window.slimeCompanion.sleep()">😴 Schlafen</button>
                ${canEvolve ? '<button class="slime-btn evolve" onclick="window.slimeCompanion.evolve()">✨ EVOLUTION!</button>' : ''}
            </div>
        `;
    }

    toggleUI() {
        this.uiVisible = !this.uiVisible;
        this.createUI();
    }

    showNotification(message, duration = 3000) {
        if (window.showNotification) {
            window.showNotification(message, duration);
        } else {
            console.log(message);
        }
    }

    // =========================================================================
    // UPDATE LOOP
    // =========================================================================

    update() {
        // UI aktualisieren
        this.createUI();

        // Hunger-Check (alle 30 Min = 1 Herz)
        if (!this.isSleeping) {
            const timeSinceFed = Date.now() - this.lastFed;
            const heartsToLose = Math.floor(timeSinceFed / SLIME_CONFIG.HUNGER_DECAY);

            if (heartsToLose > 0 && this.hungerHearts > 0) {
                this.hungerHearts = Math.max(0, this.hungerHearts - heartsToLose);
                this.lastFed = Date.now();

                if (this.hungerHearts === 0) {
                    this.careMistakes++;
                    this.showNotification(`❌ Care Mistake! ${this.name} verhungert!`, 5000);
                } else if (this.hungerHearts <= 1) {
                    this.showNotification(`⚠️ ${this.name} ist hungrig!`, 3000);
                }
            }
        }
    }

    // =========================================================================
    // SAVE/LOAD
    // =========================================================================

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            slimeType: this.slimeType,
            stage: this.stage,
            level: this.level,
            plusValue: this.plusValue,
            hungerHearts: this.hungerHearts,
            strengthHearts: this.strengthHearts,
            careMistakes: this.careMistakes,
            effortHearts: this.effortHearts,
            trainingCount: this.trainingCount,
            battles: this.battles,
            wins: this.wins,
            birthTime: this.birthTime,
            lastFed: this.lastFed,
            lastTrained: this.lastTrained,
            lastPlayed: this.lastPlayed,
            evolutionTime: this.evolutionTime,
            skills: this.skills,
            inheritedFrom: this.inheritedFrom,
            isSleeping: this.isSleeping,
            injuries: this.injuries,
            isAlive: this.isAlive,
            rescueCharges: this.rescueCharges,
            lastRescueUsed: this.lastRescueUsed
        };
    }

    fromJSON(data) {
        if (!data) return;

        this.id = data.id || this.id;
        this.name = data.name || this.name;
        this.slimeType = data.slime_type || data.slimeType || this.slimeType;
        this.stage = data.stage || this.stage;
        this.level = data.level || this.level;
        this.plusValue = data.plus_value || data.plusValue || this.plusValue;
        this.hungerHearts = data.hunger_hearts || data.hungerHearts || this.hungerHearts;
        this.strengthHearts = data.strength_hearts || data.strengthHearts || this.strengthHearts;
        this.careMistakes = data.care_mistakes || data.careMistakes || this.careMistakes;
        this.effortHearts = data.effort_hearts || data.effortHearts || this.effortHearts;
        this.trainingCount = data.training_count || data.trainingCount || this.trainingCount;
        this.battles = data.battles || this.battles;
        this.wins = data.wins || this.wins;
        this.birthTime = data.birth_time || data.birthTime || this.birthTime;
        this.lastFed = data.last_fed || data.lastFed || this.lastFed;
        this.lastTrained = data.last_trained || data.lastTrained || this.lastTrained;
        this.lastPlayed = data.last_played || data.lastPlayed || this.lastPlayed;
        this.evolutionTime = data.evolution_time || data.evolutionTime || this.evolutionTime;
        this.skills = data.skills || this.skills;
        this.inheritedFrom = data.inherited_from || data.inheritedFrom || this.inheritedFrom;
        this.isSleeping = data.is_sleeping !== undefined ? data.is_sleeping : this.isSleeping;
        this.injuries = data.injuries || this.injuries;
        this.isAlive = data.is_alive !== undefined ? data.is_alive : this.isAlive;

        // Rescue System
        if (data.rescue_charges !== undefined) {
            this.rescueCharges = data.rescue_charges;
        }
        if (data.last_rescue_used !== undefined) {
            this.lastRescueUsed = data.last_rescue_used;
        }
    }
}

// =============================================================================
// GLOBAL INSTANCE & AUTO-INIT
// =============================================================================

window.slimeCompanion = new SlimeCompanion();

// Auto-load from backend
window.addEventListener('load', () => {
    if (window.slimeCompanion) {
        window.slimeCompanion.loadFromBackend();
    }
});

// Update Loop
setInterval(() => {
    if (window.slimeCompanion) {
        window.slimeCompanion.update();
    }
}, SLIME_CONFIG.UPDATE_INTERVAL);

console.log('✅ Slime Companion System V2 loaded');
