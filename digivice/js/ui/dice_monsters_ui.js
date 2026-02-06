/**
 * Dice Monsters UI - Najika World
 * =================================
 *
 * Yu-Gi-Oh Dungeon Dice Monsters Style
 * Würfel-basiertes Monster-Kampfsystem
 *
 * OHNE 3D Dice Dependency - verwendet 2D Würfel-Animation
 *
 * Copyright: Najika World
 * Author: Claude Code (CLI)
 * Date: 2026-01-24
 */

class DiceMonstersUI {
    constructor() {
        // FastAPI Server auf Port 8001 (Dice Monsters APIs)
        const FASTAPI_BASE = 'http://127.0.0.1:8001';
        this.apiBase = `${FASTAPI_BASE}/api/dice`;
        this.isOpen = false;
        this.playerDice = [];
        this.opponentDice = [];
        this.currentRoll = null;
        this.gamePhase = 'setup'; // setup, roll, move, battle, end

        // Dice Pool
        this.dicePool = [
            { id: 1, name: 'Krieger-Würfel', type: 'warrior', summonCost: 2, attack: 3, defense: 2, emoji: '⚔️' },
            { id: 2, name: 'Magier-Würfel', type: 'mage', summonCost: 3, attack: 4, defense: 1, emoji: '🧙' },
            { id: 3, name: 'Drachen-Würfel', type: 'dragon', summonCost: 4, attack: 5, defense: 3, emoji: '🐉' },
            { id: 4, name: 'Heiler-Würfel', type: 'healer', summonCost: 2, attack: 1, defense: 2, emoji: '💚' },
            { id: 5, name: 'Assassinen-Würfel', type: 'assassin', summonCost: 3, attack: 4, defense: 1, emoji: '🗡️' },
            { id: 6, name: 'Golem-Würfel', type: 'golem', summonCost: 3, attack: 2, defense: 5, emoji: '🗿' }
        ];

        this.init();
    }

    init() {
        this.createUI();
        this.attachEventListeners();
        console.log('✅ Dice Monsters UI geladen');
    }

    createUI() {
        const container = document.createElement('div');
        container.id = 'dice-monsters-container';
        container.className = 'dice-monsters-container hidden';
        container.innerHTML = `
            <div class="dm-panel">
                <div class="dm-header">
                    <h2>🎲 Dice Monsters</h2>
                    <div class="dm-phase" id="dm-phase">Setup Phase</div>
                    <button class="dm-close-btn" id="dm-close-btn">✖</button>
                </div>

                <div class="dm-content">
                    <!-- Spielfeld -->
                    <div class="dm-battlefield">
                        <!-- Gegner Seite -->
                        <div class="dm-opponent-area">
                            <div class="dm-dice-zone opponent" id="opponent-dice-zone">
                                <div class="zone-label">Gegner Würfel</div>
                            </div>
                            <div class="dm-monster-zone opponent" id="opponent-monster-zone">
                                <div class="zone-label">Gegner Monster</div>
                            </div>
                        </div>

                        <!-- Würfel-Arena -->
                        <div class="dm-dice-arena" id="dm-dice-arena">
                            <div class="dice-result" id="dice-result">
                                <span class="dice-face" id="dice-face-1">⚀</span>
                                <span class="dice-face" id="dice-face-2">⚀</span>
                            </div>
                            <button class="roll-btn" id="roll-btn">🎲 WÜRFELN!</button>
                        </div>

                        <!-- Spieler Seite -->
                        <div class="dm-player-area">
                            <div class="dm-monster-zone player" id="player-monster-zone">
                                <div class="zone-label">Deine Monster</div>
                            </div>
                            <div class="dm-dice-zone player" id="player-dice-zone">
                                <div class="zone-label">Deine Würfel</div>
                            </div>
                        </div>
                    </div>

                    <!-- Seitenleiste -->
                    <div class="dm-sidebar">
                        <div class="dm-stats">
                            <div class="stat-box">
                                <span class="stat-label">LP</span>
                                <span class="stat-value" id="player-lp">3</span>
                            </div>
                            <div class="stat-box">
                                <span class="stat-label">Crests</span>
                                <span class="stat-value" id="player-crests">0</span>
                            </div>
                        </div>

                        <div class="dm-dice-pool">
                            <h4>Würfel-Pool</h4>
                            <div class="dice-pool-list" id="dice-pool-list">
                                ${this.dicePool.map(d => `
                                    <div class="dice-item" data-id="${d.id}" onclick="window.diceMonstersUI?.selectDice(${d.id})">
                                        <span class="dice-emoji">${d.emoji}</span>
                                        <span class="dice-name">${d.name}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>

                        <div class="dm-actions">
                            <button class="dm-btn" onclick="DiceMonstersUI.summon()">
                                📦 Beschwören
                            </button>
                            <button class="dm-btn" onclick="DiceMonstersUI.attack()">
                                ⚔️ Angreifen
                            </button>
                            <button class="dm-btn secondary" onclick="DiceMonstersUI.endTurn()">
                                ⏭️ Zug beenden
                            </button>
                        </div>
                    </div>
                </div>

                <div class="dm-log" id="dm-log">
                    <p>🎲 Willkommen bei Dice Monsters! Wähle einen Würfel und würfle!</p>
                </div>
            </div>
        `;

        // Styles
        const styles = document.createElement('style');
        styles.textContent = `
            .dice-monsters-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.9);
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .dice-monsters-container.hidden {
                display: none;
            }
            .dm-panel {
                background: linear-gradient(135deg, #1a0a2e 0%, #0d0d1a 100%);
                border: 2px solid #9932CC;
                border-radius: 15px;
                width: 95%;
                max-width: 1100px;
                max-height: 90vh;
                overflow: hidden;
                box-shadow: 0 10px 50px rgba(153,50,204,0.4);
            }
            .dm-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(90deg, #9932CC, #6B238E);
            }
            .dm-header h2 {
                margin: 0;
                color: white;
            }
            .dm-phase {
                background: rgba(0,0,0,0.3);
                padding: 5px 15px;
                border-radius: 15px;
                color: #FFD700;
            }
            .dm-close-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                font-size: 20px;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                cursor: pointer;
            }
            .dm-content {
                display: grid;
                grid-template-columns: 1fr 250px;
                gap: 15px;
                padding: 15px;
            }
            .dm-battlefield {
                display: flex;
                flex-direction: column;
                gap: 10px;
                background: rgba(0,0,0,0.5);
                border-radius: 10px;
                padding: 15px;
            }
            .dm-opponent-area, .dm-player-area {
                display: flex;
                gap: 10px;
            }
            .dm-dice-zone, .dm-monster-zone {
                flex: 1;
                min-height: 80px;
                background: rgba(153,50,204,0.2);
                border: 2px dashed rgba(153,50,204,0.5);
                border-radius: 8px;
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                padding: 10px;
                position: relative;
            }
            .dm-dice-zone.opponent, .dm-monster-zone.opponent {
                background: rgba(220,20,60,0.2);
                border-color: rgba(220,20,60,0.5);
            }
            .zone-label {
                position: absolute;
                top: -10px;
                left: 10px;
                background: #1a0a2e;
                padding: 2px 8px;
                font-size: 10px;
                color: #aaa;
            }
            .dm-dice-arena {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                background: linear-gradient(135deg, rgba(153,50,204,0.3), rgba(107,35,142,0.3));
                border-radius: 10px;
            }
            .dice-result {
                display: flex;
                gap: 20px;
                margin-bottom: 15px;
            }
            .dice-face {
                font-size: 60px;
                background: white;
                color: #333;
                width: 80px;
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.5);
            }
            .dice-face.rolling {
                animation: rollDice 0.1s infinite;
            }
            @keyframes rollDice {
                0% { transform: rotate(0deg); }
                25% { transform: rotate(90deg); }
                50% { transform: rotate(180deg); }
                75% { transform: rotate(270deg); }
                100% { transform: rotate(360deg); }
            }
            .roll-btn {
                padding: 15px 40px;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                border: none;
                color: #333;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .roll-btn:hover {
                transform: scale(1.1);
            }
            .roll-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .dm-sidebar {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            .dm-stats {
                display: flex;
                gap: 10px;
            }
            .stat-box {
                flex: 1;
                background: rgba(0,0,0,0.5);
                padding: 10px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-label {
                display: block;
                font-size: 12px;
                color: #aaa;
            }
            .stat-value {
                font-size: 24px;
                font-weight: bold;
                color: #FFD700;
            }
            .dm-dice-pool {
                background: rgba(0,0,0,0.5);
                padding: 15px;
                border-radius: 10px;
                flex: 1;
                overflow-y: auto;
            }
            .dm-dice-pool h4 {
                margin: 0 0 10px 0;
                color: #9932CC;
            }
            .dice-pool-list {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }
            .dice-item {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 8px 10px;
                background: rgba(153,50,204,0.2);
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .dice-item:hover {
                background: rgba(153,50,204,0.4);
            }
            .dice-item.selected {
                background: rgba(153,50,204,0.6);
                border: 1px solid #9932CC;
            }
            .dice-emoji {
                font-size: 24px;
            }
            .dice-name {
                font-size: 12px;
                color: #ccc;
            }
            .dm-actions {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .dm-btn {
                padding: 12px;
                background: linear-gradient(135deg, #9932CC, #6B238E);
                border: none;
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
            }
            .dm-btn:hover {
                filter: brightness(1.2);
            }
            .dm-btn.secondary {
                background: linear-gradient(135deg, #555, #333);
            }
            .dm-log {
                background: rgba(0,0,0,0.5);
                padding: 10px 15px;
                max-height: 60px;
                overflow-y: auto;
                font-size: 12px;
                color: #aaa;
            }
            .dm-log p {
                margin: 3px 0;
            }
            .monster-card {
                width: 50px;
                height: 60px;
                background: linear-gradient(135deg, #9932CC, #6B238E);
                border-radius: 5px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            }
            .monster-card .stats {
                font-size: 8px;
                color: white;
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(container);
    }

    attachEventListeners() {
        // Close Button
        document.getElementById('dm-close-btn')?.addEventListener('click', () => this.close());

        // Roll Button
        document.getElementById('roll-btn')?.addEventListener('click', () => this.roll());

        // Escape zum Schließen
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    selectDice(id) {
        this.selectedDice = this.dicePool.find(d => d.id === id);

        document.querySelectorAll('.dice-item').forEach(item => {
            item.classList.remove('selected');
            if (parseInt(item.dataset.id) === id) {
                item.classList.add('selected');
            }
        });

        this.log(`${this.selectedDice.emoji} ${this.selectedDice.name} ausgewählt`);
    }

    async roll() {
        const rollBtn = document.getElementById('roll-btn');
        const dice1 = document.getElementById('dice-face-1');
        const dice2 = document.getElementById('dice-face-2');

        if (!rollBtn || !dice1 || !dice2) return;

        rollBtn.disabled = true;
        dice1.classList.add('rolling');
        dice2.classList.add('rolling');

        // Würfel-Animation
        const faces = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
        let rollCount = 0;
        const rollInterval = setInterval(() => {
            dice1.textContent = faces[Math.floor(Math.random() * 6)];
            dice2.textContent = faces[Math.floor(Math.random() * 6)];
            rollCount++;

            if (rollCount > 20) {
                clearInterval(rollInterval);

                // Finale Werte
                const result1 = Math.floor(Math.random() * 6);
                const result2 = Math.floor(Math.random() * 6);

                dice1.textContent = faces[result1];
                dice2.textContent = faces[result2];
                dice1.classList.remove('rolling');
                dice2.classList.remove('rolling');

                this.currentRoll = { dice1: result1 + 1, dice2: result2 + 1 };
                this.log(`🎲 Gewürfelt: ${result1 + 1} + ${result2 + 1} = ${result1 + result2 + 2}`);

                rollBtn.disabled = false;
                this.processRoll();
            }
        }, 50);
    }

    processRoll() {
        const total = this.currentRoll.dice1 + this.currentRoll.dice2;

        // Crests basierend auf Wurf
        const crests = document.getElementById('player-crests');
        if (crests) {
            const newCrests = parseInt(crests.textContent) + Math.floor(total / 3);
            crests.textContent = newCrests;
        }

        this.setPhase('move');
    }

    setPhase(phase) {
        this.gamePhase = phase;
        const phaseEl = document.getElementById('dm-phase');
        if (phaseEl) {
            const phases = {
                'setup': 'Setup Phase',
                'roll': 'Würfel Phase',
                'move': 'Bewegungs Phase',
                'battle': 'Kampf Phase',
                'end': 'Ende'
            };
            phaseEl.textContent = phases[phase] || phase;
        }
    }

    log(message) {
        const logEl = document.getElementById('dm-log');
        if (logEl) {
            const p = document.createElement('p');
            p.textContent = message;
            logEl.appendChild(p);
            logEl.scrollTop = logEl.scrollHeight;
        }
    }

    open() {
        const container = document.getElementById('dice-monsters-container');
        if (container) {
            container.classList.remove('hidden');
            this.isOpen = true;
            this.setPhase('roll');
        }
    }

    close() {
        const container = document.getElementById('dice-monsters-container');
        if (container) {
            container.classList.add('hidden');
            this.isOpen = false;
        }
    }

    static summon() {
        const ui = window.diceMonstersUI;
        if (!ui?.selectedDice) {
            alert('Wähle zuerst einen Würfel aus!');
            return;
        }

        const zone = document.getElementById('player-monster-zone');
        if (zone) {
            const card = document.createElement('div');
            card.className = 'monster-card';
            card.innerHTML = `
                ${ui.selectedDice.emoji}
                <div class="stats">${ui.selectedDice.attack}/${ui.selectedDice.defense}</div>
            `;
            zone.appendChild(card);
            ui.log(`${ui.selectedDice.emoji} ${ui.selectedDice.name} beschworen!`);
        }
    }

    static attack() {
        const ui = window.diceMonstersUI;
        ui?.log('⚔️ Angriff! (Wähle ein gegnerisches Monster)');
    }

    static endTurn() {
        const ui = window.diceMonstersUI;
        ui?.log('⏭️ Zug beendet');
        ui?.setPhase('roll');
    }
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.diceMonstersUI = new DiceMonstersUI();
    });
} else {
    window.diceMonstersUI = new DiceMonstersUI();
}

window.DiceMonstersUI = DiceMonstersUI;

console.log('✅ Dice Monsters UI geladen');
