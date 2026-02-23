/**
 * SLIME ARENA UI SYSTEM
 *
 * Location: Handelsfeste (Heiße Dünen) - Neben der Nemesis Arena
 * Building: "Zur Schlammigen Münze" (schäbige Taverne-Tarnung)
 *
 * Features:
 * - 3 Game Modes: 1v1 Normal, 1v1 mit Finisher, Turnier
 * - 3 Combat Control Modes: KI, Manual, Cheer (jede Runde wechselbar)
 * - Finisher System (nur bei HP = 0)
 * - Tournament Bracket System
 */

class SlimeArenaUI {
    constructor() {
        this.container = null;
        this.currentMode = null; // 'normal', 'finisher', 'tournament'
        this.currentCombatMode = 'manual'; // 'auto', 'manual', 'cheer'
        this.currentBattle = null;
        this.tournamentBracket = null;

        // Combat state
        this.playerSlime = null;
        this.enemySlime = null;
        this.currentRound = 1;
        this.cheerBuffs = {}; // Active cheer buffs

        // API integration - FastAPI Server auf Port 8001
        this.apiBase = 'http://127.0.0.1:8000/api/slime-arena';
        this.currentDuelId = null;
        this.playerId = (typeof getPlayerId === 'function') ? getPlayerId() : 'player_1';

        this.init();
    }

    init() {
        // Create container
        this.container = document.createElement('div');
        this.container.id = 'slime-arena-ui';
        this.container.className = 'slime-arena-container hidden';
        this.container.innerHTML = this.getMainMenuHTML();
        document.body.appendChild(this.container);

        // Event listeners
        this.attachEventListeners();
    }

    getMainMenuHTML() {
        return `
            <div class="slime-arena-main-menu">
                <div class="arena-header">
                    <h1>🍺 Zur Schlammigen Münze</h1>
                    <p class="subtitle">Schleim-Arena</p>
                    <button class="close-btn" data-action="close">✕</button>
                </div>

                <div class="arena-welcome">
                    <div class="npc-dialogue">
                        <img src="/static/assets/npc/schleimiger_pete.png" class="npc-avatar" alt="Schleimiger Pete">
                        <div class="dialogue-box">
                            <strong>Schleimiger Pete:</strong>
                            <p>"Willkommen in der Grube, Fremder. Dein Schleim bereit für'n Kampf?"</p>
                        </div>
                    </div>
                </div>

                <div class="game-mode-selection">
                    <h2>Kampfmodus wählen</h2>

                    <div class="mode-card" data-mode="normal">
                        <div class="mode-icon">🥊</div>
                        <h3>1v1 Normal</h3>
                        <p>Klassisches Duell ohne Schnickschnack</p>
                        <div class="mode-rewards">
                            <span>💰 100-500 Gold</span>
                            <span>⭐ XP</span>
                        </div>
                        <button class="select-mode-btn" data-mode="normal">Auswählen</button>
                    </div>

                    <div class="mode-card" data-mode="finisher">
                        <div class="mode-icon">💥</div>
                        <h3>1v1 mit Finisher</h3>
                        <p>Spektakuläre Finishing Moves!</p>
                        <div class="mode-rewards">
                            <span>💰 200-1000 Gold</span>
                            <span>⭐ 2x XP</span>
                            <span>🏆 Ruhm +10</span>
                        </div>
                        <button class="select-mode-btn" data-mode="finisher">Auswählen</button>
                    </div>

                    <div class="mode-card tournament-card" data-mode="tournament">
                        <div class="mode-icon">🏆</div>
                        <h3>Turnier</h3>
                        <p>Single-Elimination Tournament</p>
                        <div class="tournament-info">
                            <span>👥 8-16 Teilnehmer</span>
                            <span>💀 1 Loss = Finisher K.O.</span>
                            <span>💸 Entry: 500 Gold</span>
                        </div>
                        <div class="tournament-status">
                            <span class="next-tournament">Nächstes Turnier: <strong>in 3 Tagen</strong></span>
                        </div>
                        <button class="select-mode-btn" data-mode="tournament">Einschreiben</button>
                    </div>
                </div>
            </div>
        `;
    }

    getCombatScreenHTML() {
        const playerSlime = this.playerSlime || { name: 'Dein Schleim', hp: 100, maxHp: 100, color: '#00ff00' };
        const enemySlime = this.enemySlime || { name: 'Gegner Schleim', hp: 100, maxHp: 100, color: '#ff0000' };

        return `
            <div class="slime-arena-combat">
                <div class="combat-header">
                    <div class="round-counter">Runde ${this.currentRound}</div>
                    <div class="combat-mode-indicator">
                        <span>Modus: <strong>${this.getCombatModeName()}</strong></span>
                    </div>
                    <button class="flee-btn" data-action="flee">Fliehen</button>
                </div>

                <div class="battle-field">
                    <!-- Enemy Slime (Top) -->
                    <div class="slime-display enemy">
                        <div class="slime-info">
                            <div class="slime-name">${enemySlime.name}</div>
                            <div class="hp-bar-container">
                                <div class="hp-bar" style="width: ${(enemySlime.hp / enemySlime.maxHp) * 100}%"></div>
                            </div>
                            <div class="hp-text">${enemySlime.hp}/${enemySlime.maxHp} HP</div>
                        </div>
                        <div class="slime-sprite enemy-sprite" style="background-color: ${enemySlime.color}">
                            <div class="slime-face">( ͡° ͜ʖ ͡°)</div>
                        </div>
                        <div class="status-effects" id="enemy-status"></div>
                    </div>

                    <!-- VS Indicator -->
                    <div class="vs-indicator">VS</div>

                    <!-- Player Slime (Bottom) -->
                    <div class="slime-display player">
                        <div class="slime-sprite player-sprite" style="background-color: ${playerSlime.color}">
                            <div class="slime-face">(◕‿◕)</div>
                        </div>
                        <div class="slime-info">
                            <div class="slime-name">${playerSlime.name}</div>
                            <div class="hp-bar-container">
                                <div class="hp-bar player-hp" style="width: ${(playerSlime.hp / playerSlime.maxHp) * 100}%"></div>
                            </div>
                            <div class="hp-text">${playerSlime.hp}/${playerSlime.maxHp} HP</div>
                        </div>
                        <div class="status-effects" id="player-status"></div>
                    </div>
                </div>

                <div class="combat-controls">
                    ${this.getCombatControlsHTML()}
                </div>

                <div class="battle-log">
                    <div class="log-header">Kampfprotokoll</div>
                    <div class="log-content" id="battle-log-content">
                        <div class="log-entry">Kampf beginnt!</div>
                    </div>
                </div>
            </div>
        `;
    }

    getCombatControlsHTML() {
        const mode = this.currentCombatMode;

        // Mode switching always available
        const modeSwitcher = `
            <div class="mode-switcher">
                <button class="mode-switch-btn ${mode === 'auto' ? 'active' : ''}"
                        data-switch-mode="auto" title="KI-Kontrolle">
                    🤖 KI
                </button>
                <button class="mode-switch-btn ${mode === 'manual' ? 'active' : ''}"
                        data-switch-mode="manual" title="Direkte Befehle">
                    🎮 Manual
                </button>
                <button class="mode-switch-btn ${mode === 'cheer' ? 'active' : ''}"
                        data-switch-mode="cheer" title="Anfeuern">
                    📣 Cheer
                </button>
            </div>
        `;

        let controls = '';

        switch (mode) {
            case 'auto':
                controls = `
                    <div class="auto-mode-controls">
                        <p class="mode-description">🤖 KI steuert deinen Schleim automatisch</p>
                        <button class="action-btn auto-action" data-action="auto-turn">
                            KI-Zug ausführen
                        </button>
                    </div>
                `;
                break;

            case 'manual':
                controls = `
                    <div class="manual-mode-controls">
                        <p class="mode-description">🎮 Wähle deine Aktion</p>
                        <div class="action-grid">
                            <button class="action-btn attack-btn" data-action="attack">
                                ⚔️ Angreifen
                            </button>
                            <button class="action-btn defend-btn" data-action="defend">
                                🛡️ Verteidigen
                            </button>
                            <button class="action-btn item-btn" data-action="item">
                                🎒 Item
                            </button>
                            <button class="action-btn special-btn" data-action="special">
                                ✨ Spezial
                            </button>
                        </div>
                    </div>
                `;
                break;

            case 'cheer':
                controls = `
                    <div class="cheer-mode-controls">
                        <p class="mode-description">📣 Feuere deinen Schleim an! (Buffs halten 3 Runden)</p>
                        <div class="cheer-grid">
                            <button class="cheer-btn" data-cheer="attack"
                                    ${this.cheerBuffs.attack ? 'disabled' : ''}>
                                <span class="cheer-icon">💪</span>
                                <span class="cheer-text">Los!</span>
                                <span class="cheer-effect">+10% DMG</span>
                            </button>
                            <button class="cheer-btn" data-cheer="defend"
                                    ${this.cheerBuffs.defend ? 'disabled' : ''}>
                                <span class="cheer-icon">🛡️</span>
                                <span class="cheer-text">Defend!</span>
                                <span class="cheer-effect">+20% DEF</span>
                            </button>
                            <button class="cheer-btn" data-cheer="combo"
                                    ${this.cheerBuffs.combo ? 'disabled' : ''}>
                                <span class="cheer-icon">💥</span>
                                <span class="cheer-text">Combo!</span>
                                <span class="cheer-effect">Next = Combo</span>
                            </button>
                            <button class="cheer-btn" data-cheer="focus"
                                    ${this.cheerBuffs.focus ? 'disabled' : ''}>
                                <span class="cheer-icon">🎯</span>
                                <span class="cheer-text">Focus!</span>
                                <span class="cheer-effect">+15% ACC</span>
                            </button>
                        </div>
                        <div class="active-buffs">
                            ${this.getActiveBuffsHTML()}
                        </div>
                    </div>
                `;
                break;
        }

        return modeSwitcher + controls;
    }

    getActiveBuffsHTML() {
        const buffs = Object.entries(this.cheerBuffs).filter(([_, rounds]) => rounds > 0);
        if (buffs.length === 0) {
            return '<span class="no-buffs">Keine aktiven Buffs</span>';
        }

        return buffs.map(([buff, rounds]) => {
            const icons = {
                attack: '💪',
                defend: '🛡️',
                combo: '💥',
                focus: '🎯'
            };
            return `<span class="active-buff">${icons[buff]} ${buff} (${rounds} Runden)</span>`;
        }).join('');
    }

    getFinisherSelectionHTML() {
        const finishers = [
            {
                id: 'inferno_burst',
                name: 'Inferno Burst',
                description: 'Standard, spektakulär',
                icon: '🔥',
                fame: 10
            },
            {
                id: 'mega_explosion',
                name: 'Mega Explosion',
                description: 'Extra brutal',
                icon: '💣',
                fame: 15
            },
            {
                id: 'flame_stomp',
                name: 'Flame Stomp',
                description: 'Demütigend',
                icon: '👟',
                fame: 12
            },
            {
                id: 'mercy',
                name: 'Mercy',
                description: 'Gnädig, nur HP-Entzug',
                icon: '🕊️',
                fame: 5
            }
        ];

        return `
            <div class="finisher-selection-screen">
                <div class="finisher-header">
                    <h2>🏆 FINISH HIM!</h2>
                    <p>Wähle deinen Finishing Move</p>
                </div>

                <div class="finisher-grid">
                    ${finishers.map(f => `
                        <div class="finisher-card" data-finisher="${f.id}">
                            <div class="finisher-icon">${f.icon}</div>
                            <h3>${f.name}</h3>
                            <p class="finisher-desc">${f.description}</p>
                            <div class="finisher-fame">+${f.fame} Ruhm</div>
                            <button class="select-finisher-btn" data-finisher="${f.id}">
                                Ausführen
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    getTournamentBracketHTML() {
        // Tournament bracket visualization
        return `
            <div class="tournament-bracket-screen">
                <div class="tournament-header">
                    <h2>🏆 Turnier-Bracket</h2>
                    <div class="tournament-round">Runde: ${this.tournamentBracket?.currentRound || 1}/4</div>
                    <button class="close-bracket-btn" data-action="close-bracket">Zurück</button>
                </div>

                <div class="bracket-container">
                    <div class="bracket-round round-1">
                        <h3>Achtelfinale</h3>
                        ${this.getBracketMatchesHTML(1, 8)}
                    </div>

                    <div class="bracket-round round-2">
                        <h3>Viertelfinale</h3>
                        ${this.getBracketMatchesHTML(2, 4)}
                    </div>

                    <div class="bracket-round round-3">
                        <h3>Halbfinale</h3>
                        ${this.getBracketMatchesHTML(3, 2)}
                    </div>

                    <div class="bracket-round round-4">
                        <h3>FINALE</h3>
                        ${this.getBracketMatchesHTML(4, 1)}
                    </div>
                </div>

                <div class="tournament-info-footer">
                    <div class="elimination-warning">
                        ⚠️ Single-Elimination: 1 Niederlage = Du bist RAUS und wirst gefinischt!
                    </div>
                </div>
            </div>
        `;
    }

    getBracketMatchesHTML(round, matchCount) {
        let html = '';
        for (let i = 0; i < matchCount; i++) {
            const match = this.tournamentBracket?.rounds?.[round - 1]?.[i] || { player1: '???', player2: '???', winner: null };
            html += `
                <div class="bracket-match ${match.winner ? 'completed' : 'pending'}">
                    <div class="match-participant ${match.winner === 'player1' ? 'winner' : match.winner === 'player2' ? 'loser' : ''}">
                        ${match.player1}
                    </div>
                    <div class="match-vs">VS</div>
                    <div class="match-participant ${match.winner === 'player2' ? 'winner' : match.winner === 'player1' ? 'loser' : ''}">
                        ${match.player2}
                    </div>
                    ${match.winner ? '<div class="finisher-badge">💀 FINISHED</div>' : ''}
                    ${!match.winner && (match.player1 === 'Du' || match.player2 === 'Du') ? '<button data-action="start-tournament-fight" style="background:#ff4444;color:white;border:none;padding:4px 12px;cursor:pointer;border-radius:4px;margin-top:4px;font-weight:bold;">Kämpfen!</button>' : ''}
                </div>
            `;
        }
        return html;
    }

    getCombatModeName() {
        const names = {
            auto: '🤖 KI-Kontrolle',
            manual: '🎮 Direkte Befehle',
            cheer: '📣 Digimon-Anfeuern'
        };
        return names[this.currentCombatMode] || this.currentCombatMode;
    }

    attachEventListeners() {
        this.container.addEventListener('click', (e) => {
            const target = e.target;

            // Close arena
            if (target.dataset.action === 'close') {
                this.close();
            }

            // Mode selection
            if (target.classList.contains('select-mode-btn')) {
                const mode = target.dataset.mode;
                this.startMode(mode);
            }

            // Combat mode switching
            if (target.dataset.switchMode) {
                this.switchCombatMode(target.dataset.switchMode);
            }

            // Combat actions
            if (target.dataset.action === 'attack') {
                this.executeAttack();
            }
            if (target.dataset.action === 'defend') {
                this.executeDefend();
            }
            if (target.dataset.action === 'item') {
                this.openItemMenu();
            }
            if (target.dataset.action === 'special') {
                this.executeSpecial();
            }
            if (target.dataset.action === 'auto-turn') {
                this.executeAutoTurn();
            }

            // Cheer actions
            if (target.classList.contains('cheer-btn') || target.closest('.cheer-btn')) {
                const btn = target.classList.contains('cheer-btn') ? target : target.closest('.cheer-btn');
                const cheerType = btn.dataset.cheer;
                if (cheerType) {
                    this.executeCheer(cheerType);
                }
            }

            // Finisher selection
            if (target.classList.contains('select-finisher-btn')) {
                const finisher = target.dataset.finisher;
                this.executeFinisher(finisher);
            }

            // Tournament
            if (target.dataset.action === 'close-bracket') {
                this.showMainMenu();
            }
            if (target.dataset.action === 'start-tournament-fight') {
                this.startBattle('finisher');
            }

            // Flee
            if (target.dataset.action === 'flee') {
                this.fleeBattle();
            }
        });
    }

    // === PUBLIC API ===

    open() {
        this.container.classList.remove('hidden');
        this.showMainMenu();
    }

    close() {
        this.container.classList.add('hidden');
    }

    showMainMenu() {
        this.container.innerHTML = this.getMainMenuHTML();
        this.attachEventListeners();
    }

    startMode(mode) {
        this.currentMode = mode;

        if (mode === 'tournament') {
            this.startTournament();
        } else {
            this.startBattle(mode);
        }
    }

    async startBattle(mode) {
        // Initialize battle
        this.currentRound = 1;
        this.cheerBuffs = {};
        this.currentMode = mode;

        // Generiere Slime-Gegner
        const slimeTypes = [
            { name: 'Grüner Schleim', hp: 60, attack: 12, defense: 8, color: '#00ff00', element: 'nature' },
            { name: 'Roter Schleim', hp: 50, attack: 18, defense: 5, color: '#ff0000', element: 'fire' },
            { name: 'Blauer Schleim', hp: 70, attack: 10, defense: 12, color: '#0066ff', element: 'water' },
            { name: 'Goldener Schleim', hp: 80, attack: 15, defense: 10, color: '#ffd700', element: 'light' },
            { name: 'Dunkler Schleim', hp: 55, attack: 20, defense: 6, color: '#330066', element: 'dark' }
        ];

        const enemyTemplate = slimeTypes[Math.floor(Math.random() * slimeTypes.length)];

        // ⚔️ REAL 3D COMBAT - Slime Arena (AUTO/CHEER only!)
        if (!window.Real3DCombat || !window.Real3DCombat.startCombat) {
            console.error('❌ Real3DCombat nicht verfügbar!');
            this.startFallbackBattle(mode, enemyTemplate);
            return;
        }

        this.container.classList.add('hidden');

        // Don't teleport for Slime Arena - stays in current location
        const scene = window.getScene ? window.getScene() : null;
        if (!scene) {
            console.error('❌ Scene nicht verfügbar!');
            this.startFallbackBattle(mode, enemyTemplate);
            return;
        }

        // Map slime element to enemy type
        const elementMap = {
            'nature': 'slime',
            'fire': 'bat',
            'water': 'slime',
            'light': 'slime',
            'dark': 'slime'
        };
        const enemyType = elementMap[enemyTemplate.element] || 'slime';

        const self = this;
        const playerPos = window.getPlayerPosition ? window.getPlayerPosition() : { x: 0, y: 0, z: 0 };

        window.onCombatVictory = (result) => {
            if (result.type === 'real3d') {
                self.container.classList.remove('hidden');
                if (mode === 'finisher') {
                    self.container.innerHTML = self.getFinisherSelectionHTML();
                    self.attachEventListeners();
                } else {
                    self.showBattleResult(true);
                }
            }
        };
        window.onCombatDefeat = (result) => {
            if (result.type === 'real3d') {
                self.container.classList.remove('hidden');
                self.showBattleResult(false);
            }
        };

        window.Real3DCombat.startCombat([enemyType], scene, playerPos);

        // 🎮 Auto-set to CHEER mode for Slime Arena (Digimon World style!)
        setTimeout(() => {
            if (window.Real3DCombat && window.Real3DCombat.setMode) {
                window.Real3DCombat.setMode('CHEER');
            }
        }, 100);

        console.log(`⚔️ Slime Arena: ${enemyTemplate.name} (CHEER-Modus!)`);

    }

    startFallbackBattle(mode, enemyTemplate) {
        // Fallback zum alten internen System
        if (true) {
            // Fallback zum alten internen System
            this.playerSlime = {
                name: 'Dein Schleim',
                hp: 100,
                maxHp: 100,
                color: '#00ff00',
                attack: 20,
                defense: 15
            };

            this.enemySlime = {
                name: enemyTemplate.name,
                hp: enemyTemplate.hp,
                maxHp: enemyTemplate.hp,
                color: enemyTemplate.color,
                attack: enemyTemplate.attack,
                defense: enemyTemplate.defense
            };

            this.container.innerHTML = this.getCombatScreenHTML();
            this.attachEventListeners();

            this.addLogEntry(`Kampf gegen ${this.enemySlime.name} beginnt! ${mode === 'finisher' ? '(Finisher-Modus aktiviert)' : ''}`);
        }
    }

    startTournament() {
        // Initialize tournament bracket
        this.tournamentBracket = {
            currentRound: 1,
            rounds: [
                // Round 1: 8 matches
                [
                    { player1: 'Du', player2: 'NPC 1', winner: null },
                    { player1: 'NPC 2', player2: 'NPC 3', winner: null },
                    { player1: 'NPC 4', player2: 'NPC 5', winner: null },
                    { player1: 'NPC 6', player2: 'NPC 7', winner: null },
                    { player1: 'NPC 8', player2: 'NPC 9', winner: null },
                    { player1: 'NPC 10', player2: 'NPC 11', winner: null },
                    { player1: 'NPC 12', player2: 'NPC 13', winner: null },
                    { player1: 'NPC 14', player2: 'NPC 15', winner: null }
                ],
                // Rounds 2-4 will be filled as tournament progresses
                [], [], []
            ]
        };

        this.container.innerHTML = this.getTournamentBracketHTML();
        this.attachEventListeners();
    }

    switchCombatMode(newMode) {
        this.currentCombatMode = newMode;

        // Update UI
        const controlsContainer = this.container.querySelector('.combat-controls');
        if (controlsContainer) {
            controlsContainer.innerHTML = this.getCombatControlsHTML();
        }

        this.addLogEntry(`Modus gewechselt zu: ${this.getCombatModeName()}`);
    }

    // === COMBAT ACTIONS ===

    executeAttack() {
        let attackMult = 1.0;
        if (this.cheerBuffs && this.cheerBuffs.attack > 0) attackMult *= 1.10;
        if (this.cheerBuffs && this.cheerBuffs.combo > 0) attackMult *= 1.25;
        const damage = Math.floor(this.playerSlime.attack * (0.8 + Math.random() * 0.4) * attackMult);
        this.enemySlime.hp = Math.max(0, this.enemySlime.hp - damage);

        this.addLogEntry(`${this.playerSlime.name} greift an! ${damage} Schaden!`);
        this.updateBattleDisplay();

        if (this.enemySlime.hp === 0) {
            this.handleBattleEnd(true);
        } else {
            this.executeEnemyTurn();
        }
    }

    executeDefend() {
        this.addLogEntry(`${this.playerSlime.name} verteidigt!`);
        // Apply defense buff for next enemy turn
        this.playerSlime.defending = true;
        this.executeEnemyTurn();
    }

    executeSpecial() {
        const damage = Math.floor(this.playerSlime.attack * 1.5);
        this.enemySlime.hp = Math.max(0, this.enemySlime.hp - damage);

        this.addLogEntry(`${this.playerSlime.name} verwendet Spezial-Attacke! ${damage} Schaden!`);
        this.updateBattleDisplay();

        if (this.enemySlime.hp === 0) {
            this.handleBattleEnd(true);
        } else {
            this.executeEnemyTurn();
        }
    }

    executeAutoTurn() {
        // AI picks random action
        const actions = ['attack', 'defend', 'special'];
        const action = actions[Math.floor(Math.random() * actions.length)];

        this.addLogEntry(`KI wählt: ${action}`);

        setTimeout(() => {
            switch (action) {
                case 'attack':
                    this.executeAttack();
                    break;
                case 'defend':
                    this.executeDefend();
                    break;
                case 'special':
                    this.executeSpecial();
                    break;
            }
        }, 500);
    }

    executeCheer(cheerType) {
        // Apply buff for 3 rounds
        this.cheerBuffs[cheerType] = 3;

        const messages = {
            attack: '💪 "Los!" - Angriff erhöht!',
            defend: '🛡️ "Defend!" - Verteidigung erhöht!',
            combo: '💥 "Combo!" - Nächster Angriff wird Combo!',
            focus: '🎯 "Focus!" - Genauigkeit erhöht!'
        };

        this.addLogEntry(messages[cheerType]);

        // Slime fights automatically with buff
        setTimeout(() => {
            this.executeAttack();
        }, 1000);
    }

    executeEnemyTurn() {
        this.currentRound++;

        // Decrease buff durations
        Object.keys(this.cheerBuffs).forEach(buff => {
            this.cheerBuffs[buff]--;
            if (this.cheerBuffs[buff] <= 0) {
                delete this.cheerBuffs[buff];
            }
        });

        setTimeout(() => {
            const damage = Math.floor(this.enemySlime.attack * (0.8 + Math.random() * 0.4));
            const defMult = (this.cheerBuffs && this.cheerBuffs.defend > 0) ? 0.3 : 0.5;
            const actualDamage = this.playerSlime.defending ? Math.floor(damage * defMult) : damage;
            this.playerSlime.defending = false;

            this.playerSlime.hp = Math.max(0, this.playerSlime.hp - actualDamage);

            this.addLogEntry(`${this.enemySlime.name} greift an! ${actualDamage} Schaden!`);
            this.updateBattleDisplay();

            if (this.playerSlime.hp === 0) {
                this.handleBattleEnd(false);
            }
        }, 1000);
    }

    openItemMenu() {
        if (!this.arenaItems) {
            this.arenaItems = [
                { name: 'Heiltrank', heal: 25, count: 2 },
                { name: 'Mana-Trank', heal: 15, count: 1 }
            ];
        }
        const available = this.arenaItems.filter(i => i.count > 0);
        if (available.length === 0) {
            this.addLogEntry('Keine Items mehr!');
            return;
        }
        const item = available[0];
        item.count--;
        const oldHp = this.playerSlime.hp;
        this.playerSlime.hp = Math.min(this.playerSlime.maxHp, this.playerSlime.hp + item.heal);
        const healed = this.playerSlime.hp - oldHp;
        this.addLogEntry(`${item.name} benutzt! +${healed} HP (${item.count} übrig)`);
        this.updateBattleDisplay();
        setTimeout(() => this.executeEnemyTurn(), 800);
    }

    handleBattleEnd(playerWon) {
        if (playerWon && this.currentMode === 'finisher') {
            // Show finisher selection
            this.container.innerHTML = this.getFinisherSelectionHTML();
            this.attachEventListeners();
        } else {
            // Show victory/defeat screen
            this.showBattleResult(playerWon);
        }
    }

    executeFinisher(finisherId) {
        this.addLogEntry(`🎬 Finisher: ${finisherId} wird ausgeführt!`);

        // Play finisher animation
        this.playFinisherAnimation(finisherId);
    }

    /**
     * Play finisher animation mit visuellen Effekten
     */
    playFinisherAnimation(finisherId) {
        // Erstelle Animation Overlay
        const overlay = document.createElement('div');
        overlay.className = 'finisher-animation-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(0,0,0,0.95), rgba(30,0,0,0.95));
            z-index: 20000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.5s ease-out;
        `;

        // Finisher Namen und Kategorie basierend auf ID
        const finisherData = this.getFinisherData(finisherId);

        overlay.innerHTML = `
            <style>
                @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
                @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
                @keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-10px); } 75% { transform: translateX(10px); } }
                @keyframes slideUp { from { opacity: 0; transform: translateY(50px); } to { opacity: 1; transform: translateY(0); } }
            </style>
            <div style="text-align: center;">
                <h1 style="color: #ff4444; font-size: 72px; text-shadow: 0 0 30px #ff0000; margin: 0; animation: pulse 0.5s infinite;">
                    💀 FINISH HIM! 💀
                </h1>
                <h2 style="color: #ffcc00; font-size: 48px; margin: 20px 0; animation: slideUp 0.5s ease-out 0.5s both;">
                    ${finisherData.name}
                </h2>
                <div style="color: #888; font-size: 24px; animation: slideUp 0.5s ease-out 0.7s both;">
                    Kategorie: ${finisherData.category}
                </div>
                <div id="finisher-sequence" style="margin-top: 30px; min-height: 200px;"></div>
                <div style="margin-top: 20px; animation: slideUp 0.5s ease-out 1s both;">
                    <span style="color: #ff6666;">Brutalität: ${'💀'.repeat(finisherData.brutality)}</span>
                    <span style="color: #ffcc66; margin-left: 20px;">Schaden: ${finisherData.damageMultiplier}x</span>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Animiere Sequenz
        const sequence = overlay.querySelector('#finisher-sequence');
        const steps = finisherData.steps;
        let stepIndex = 0;

        const animateStep = () => {
            if (stepIndex < steps.length) {
                const step = steps[stepIndex];
                const stepEl = document.createElement('div');
                stepEl.style.cssText = `
                    color: #fff;
                    font-size: 28px;
                    margin: 10px 0;
                    animation: slideUp 0.3s ease-out, shake 0.2s ease-out 0.3s;
                `;
                stepEl.innerHTML = `${step.emoji} ${step.text}`;
                sequence.appendChild(stepEl);
                stepIndex++;
                setTimeout(animateStep, step.duration || 800);
            } else {
                // Finisher komplett - zeige Ergebnis
                setTimeout(() => {
                    overlay.style.animation = 'fadeOut 1s ease-out';
                    setTimeout(() => {
                        overlay.remove();
                        this.showBattleResult(true);
                    }, 1000);
                }, 1000);
            }
        };

        setTimeout(animateStep, 1000);
    }

    /**
     * Holt Finisher-Daten basierend auf ID
     */
    getFinisherData(finisherId) {
        // Standard Finisher-Daten (kann später von API kommen)
        const finishers = {
            // Aus getFinisherSelectionHTML
            'inferno_burst': {
                name: 'INFERNO BURST!',
                category: 'Feuer',
                brutality: 7,
                damageMultiplier: 2,
                steps: [
                    { emoji: '🔥', text: 'Flammen umhüllen den Gegner...', duration: 700 },
                    { emoji: '🌋', text: 'INFERNO!!!', duration: 500 },
                    { emoji: '💀', text: 'Zu Asche verbrannt!', duration: 600 }
                ]
            },
            'mega_explosion': {
                name: 'MEGA EXPLOSION!!!',
                category: 'Explosiv',
                brutality: 10,
                damageMultiplier: 3,
                steps: [
                    { emoji: '⚡', text: 'Energie konzentriert sich...', duration: 600 },
                    { emoji: '🔥', text: 'CRIMSON EXPLOSION!!!', duration: 500 },
                    { emoji: '💥', text: 'BOOOOOOM!!!', duration: 400 },
                    { emoji: '☠️', text: 'Totale Vernichtung!', duration: 700 }
                ]
            },
            'flame_stomp': {
                name: 'FLAME STOMP',
                category: 'Demütigung',
                brutality: 8,
                damageMultiplier: 2,
                steps: [
                    { emoji: '🔥', text: 'Flammen umhüllen den Fuß...', duration: 600 },
                    { emoji: '👟', text: 'STOMP! STOMP! STOMP!', duration: 500 },
                    { emoji: '😵', text: 'Plattgetreten und verbrannt!', duration: 600 }
                ]
            },
            'mercy': {
                name: 'GNADE',
                category: 'Barmherzig',
                brutality: 1,
                damageMultiplier: 1,
                steps: [
                    { emoji: '🕊️', text: 'Du verschonst deinen Gegner...', duration: 800 },
                    { emoji: '✨', text: 'Ehre bewahrt.', duration: 600 }
                ]
            },
            // Zusätzliche Finisher
            'explosion_supreme': {
                name: 'EXPLOSION SUPREME!',
                category: 'Explosiv',
                brutality: 10,
                damageMultiplier: 3,
                steps: [
                    { emoji: '🔥', text: 'Magische Energie sammelt sich...', duration: 800 },
                    { emoji: '⚡', text: 'CRIMSON EXPLOSION!!!', duration: 600 },
                    { emoji: '💥', text: 'BOOOOM!!!', duration: 400 },
                    { emoji: '☠️', text: 'Totale Vernichtung!', duration: 600 }
                ]
            },
            'chaos_slice': {
                name: 'CHAOS SLICE',
                category: 'Scharf',
                brutality: 8,
                damageMultiplier: 2.5,
                steps: [
                    { emoji: '🗡️', text: 'Die Klinge glüht...', duration: 700 },
                    { emoji: '⚔️', text: 'SLASH! SLASH! SLASH!', duration: 500 },
                    { emoji: '🩸', text: 'In Stücke geschnitten!', duration: 600 }
                ]
            },
            'pudding_doom': {
                name: 'PUDDING OF DOOM',
                category: 'Witzig',
                brutality: 5,
                damageMultiplier: 1.5,
                steps: [
                    { emoji: '🍮', text: 'Ein riesiger Pudding erscheint!', duration: 800 },
                    { emoji: '😱', text: 'Der Gegner ist verwirrt...', duration: 700 },
                    { emoji: '💀', text: 'SPLAT! Tod durch Pudding!', duration: 600 }
                ]
            }
        };

        return finishers[finisherId] || {
            name: finisherId.replace(/_/g, ' ').toUpperCase(),
            category: 'Unbekannt',
            brutality: 5,
            damageMultiplier: 2,
            steps: [
                { emoji: '⚡', text: 'Energie aufgeladen!', duration: 600 },
                { emoji: '💥', text: 'FINISHER!!!', duration: 500 },
                { emoji: '☠️', text: 'K.O.!', duration: 400 }
            ]
        };
    }

    showBattleResult(won) {
        const resultHTML = `
            <div class="battle-result-screen">
                <h2>${won ? '🏆 SIEG!' : '💀 NIEDERLAGE'}</h2>
                <p>${won ? 'Dein Schleim hat gewonnen!' : 'Dein Schleim wurde besiegt!'}</p>

                ${won ? `
                    <div class="rewards">
                        <h3>Belohnungen:</h3>
                        <div class="reward-item">💰 500 Gold</div>
                        <div class="reward-item">⭐ 150 XP</div>
                        ${this.currentMode === 'finisher' ? '<div class="reward-item">🏆 +10 Ruhm</div>' : ''}
                    </div>
                ` : ''}

                <button class="return-btn" onclick="window.slimeArenaUI.showMainMenu()">
                    Zurück zum Menü
                </button>
            </div>
        `;

        this.container.innerHTML = resultHTML;
    }

    fleeBattle() {
        if (this._fleeConfirmPending) {
            this._fleeConfirmPending = false;
            this.addLogEntry('Du bist geflohen!');
            setTimeout(() => {
                this.showMainMenu();
            }, 1000);
            return;
        }
        this._fleeConfirmPending = true;
        if (typeof notify === 'function') notify('⚠️ Nochmal klicken um zu fliehen!', 'warning');
        setTimeout(() => { this._fleeConfirmPending = false; }, 3000);
    }

    updateBattleDisplay() {
        // Update HP bars
        const playerHpBar = this.container.querySelector('.player-hp');
        const enemyHpBar = this.container.querySelector('.slime-display.enemy .hp-bar');

        if (playerHpBar) {
            playerHpBar.style.width = `${(this.playerSlime.hp / this.playerSlime.maxHp) * 100}%`;
        }
        if (enemyHpBar) {
            enemyHpBar.style.width = `${(this.enemySlime.hp / this.enemySlime.maxHp) * 100}%`;
        }

        // Update HP text
        const playerHpText = this.container.querySelector('.slime-display.player .hp-text');
        const enemyHpText = this.container.querySelector('.slime-display.enemy .hp-text');

        if (playerHpText) {
            playerHpText.textContent = `${this.playerSlime.hp}/${this.playerSlime.maxHp} HP`;
        }
        if (enemyHpText) {
            enemyHpText.textContent = `${this.enemySlime.hp}/${this.enemySlime.maxHp} HP`;
        }

        // Update round counter
        const roundCounter = this.container.querySelector('.round-counter');
        if (roundCounter) {
            roundCounter.textContent = `Runde ${this.currentRound}`;
        }

        // Update active buffs display (if in cheer mode)
        if (this.currentCombatMode === 'cheer') {
            const activeBuffsDiv = this.container.querySelector('.active-buffs');
            if (activeBuffsDiv) {
                activeBuffsDiv.innerHTML = this.getActiveBuffsHTML();
            }
        }
    }

    addLogEntry(message) {
        const logContent = this.container.querySelector('#battle-log-content');
        if (logContent) {
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.textContent = message;
            logContent.appendChild(entry);
            logContent.scrollTop = logContent.scrollHeight;
        }
    }
}

// Global instance
window.slimeArenaUI = new SlimeArenaUI();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SlimeArenaUI;
}
