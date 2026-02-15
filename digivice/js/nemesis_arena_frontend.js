// ============================================
// NAJIKA ARENA NEMESIS SYSTEM - FRONTEND
// Shadow of Mordor meets Digimon World
// ============================================

class NemesisArenaUI {
    constructor() {
        this.apiBase = 'http://localhost:8001';  // Backend API
        this.currentBattle = null;
        this.arenaPanel = null;
        this.hierarchyView = null;
        this.monsterProfile = null;
        this.battleLog = [];
        this.playerStats = {
            level: 1,
            wins: 0,
            losses: 0,
            rank: 'Neuling'
        };

        // Wave Mode State
        this.waveState = null;

        this.init();
    }

    init() {
        // Erstelle Arena-UI-Elemente
        this.createArenaPanel();
        this.createHierarchyView();
        this.loadArenaStatus();

        // Wave Mode initialisieren
        this.initWaveState();

        // Event Listeners
        this.setupEventListeners();

        // Auto-Update alle 30 Sekunden
        setInterval(() => this.updateArenaEvents(), 30000);
    }

    createArenaPanel() {
        const panel = document.createElement('div');
        panel.id = 'arena-panel';
        panel.className = 'arena-nemesis-panel';
        panel.innerHTML = `
            <div class="arena-header">
                <h2>🏛️ NEMESIS ARENA</h2>
                <button id="arena-close" class="close-btn">✖</button>
            </div>

            <div class="arena-tabs">
                <button class="arena-tab active" data-tab="challengers">Herausforderer</button>
                <button class="arena-tab" data-tab="waves">🌊 Wellen</button>
                <button class="arena-tab" data-tab="hierarchy">Hierarchie</button>
                <button class="arena-tab" data-tab="nemesis">Meine Nemesis</button>
                <button class="arena-tab" data-tab="regions">Gebiete</button>
            </div>

            <div class="arena-content">
                <div id="challengers-view" class="tab-content active">
                    <div class="quick-challenge">
                        <h3>⚔️ Schnell-Herausforderung</h3>
                        <button id="quick-battle-btn" class="battle-btn glow-effect">
                            ZUFÄLLIGER GEGNER
                        </button>
                    </div>

                    <div class="monster-list" id="monster-list">
                        <!-- Dynamisch geladen -->
                    </div>
                </div>

                <!-- WELLEN-MODUS TAB -->
                <div id="waves-view" class="tab-content">
                    <div class="wave-mode-container">
                        <h3>🌊 Wellen-Modus</h3>
                        <div class="wave-progress">
                            <div class="wave-info">
                                <span class="current-wave">Welle: <strong id="current-wave-num">0</strong>/15</span>
                                <span class="wave-mode-type" id="wave-mode-label">Training-Modus (kein echter Tod)</span>
                            </div>
                            <div class="wave-progress-bar">
                                <div class="wave-progress-fill" id="wave-progress-fill" style="width: 0%"></div>
                            </div>
                        </div>

                        <div class="wave-description">
                            <p><strong>Training (Wellen 1-15):</strong> Übe ohne Risiko! Bei Niederlage kein echter Verlust.</p>
                            <p><strong>Echter Modus (ab Welle 16):</strong> ⚠️ HARDCORE! Echte Konsequenzen bei Niederlage!</p>
                        </div>

                        <div class="wave-buttons">
                            <button id="start-wave-btn" class="battle-btn glow-effect">
                                🌊 WELLE STARTEN
                            </button>
                            <button id="reset-waves-btn" class="battle-btn secondary" style="background:#444;">
                                🔄 Reset (Training)
                            </button>
                        </div>

                        <div class="wave-rewards">
                            <h4>Belohnungen pro Welle:</h4>
                            <ul>
                                <li>🪙 Gold: 50 × Welle</li>
                                <li>⭐ XP: 20 × Welle</li>
                                <li>🏆 Welle 5: Bronzemedaille</li>
                                <li>🏆 Welle 10: Silbermedaille</li>
                                <li>🏆 Welle 15: GOLDMEDAILLE + Echter Modus freigeschaltet!</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div id="hierarchy-view" class="tab-content">
                    <div class="hierarchy-display">
                        <!-- Dynamisch geladen -->
                    </div>
                </div>

                <div id="nemesis-view" class="tab-content">
                    <h3>🔥 Deine Erzfeinde</h3>
                    <div id="nemesis-list">
                        <!-- Monster die dich getötet haben -->
                    </div>
                </div>

                <div id="regions-view" class="tab-content">
                    <h3>🗺️ Gebietsherrschaft</h3>
                    <div id="regions-grid">
                        <!-- 8 Regionen mit Herrschern -->
                    </div>
                </div>
            </div>

            <div class="arena-footer">
                <div class="player-rank">
                    <span>Rang: <strong id="player-rank">Neuling</strong></span>
                    <span>Siege: <strong id="player-wins">0</strong></span>
                    <span>Niederlagen: <strong id="player-losses">0</strong></span>
                </div>
            </div>
        `;

        document.body.appendChild(panel);
        this.arenaPanel = panel;
    }

    // Öffnet das Arena Panel (für game_systems_ui.js)
    showArenaPanel() {
        if (this.arenaPanel) {
            this.arenaPanel.style.display = 'flex';  // flex wegen flex-direction: column
            this.loadMonsterList();  // Aktualisiere Monster-Liste beim Öffnen
        } else {
            console.error('Arena Panel nicht initialisiert!');
        }
    }

    // Alias für showArenaPanel (alternative Namen)
    open() {
        this.showArenaPanel();
    }

    // Schließt das Arena Panel
    hideArenaPanel() {
        if (this.arenaPanel) {
            this.arenaPanel.style.display = 'none';
        }
    }

    close() {
        this.hideArenaPanel();
    }

    createHierarchyView() {
        const hierarchyHTML = `
            <div class="hierarchy-pyramid">
                <div class="rank-level arena-king">
                    <div class="rank-title">👑 ARENA-KÖNIG</div>
                    <div id="current-king" class="rank-holder">
                        [VAKANT]
                    </div>
                </div>

                <div class="rank-level region-lords">
                    <div class="rank-title">🏰 GEBIETSHERRSCHER</div>
                    <div id="region-lords-list" class="rank-holders">
                        <!-- 8 Slots -->
                    </div>
                </div>

                <div class="rank-level champions">
                    <div class="rank-title">⚔️ CHAMPIONS</div>
                    <div id="champions-list" class="rank-holders">
                        <!-- Top 5 -->
                    </div>
                </div>

                <div class="rank-level gladiators">
                    <div class="rank-title">🗡️ GLADIATOREN</div>
                    <div id="gladiators-count" class="rank-count">
                        0 Monster
                    </div>
                </div>
            </div>
        `;

        // Update hierarchy view wenn Tab gewählt
        this.hierarchyView = hierarchyHTML;
    }

    async loadArenaStatus() {
        try {
            const response = await fetch(`${this.apiBase}/api/arena/status`);
            const data = await response.json();

            // Update Player Stats
            document.getElementById('player-rank').textContent = data.player_rank;

            // Load Monster List
            await this.loadMonsterList();

            // Check für Events
            if (data.events && data.events.length > 0) {
                this.displayArenaEvents(data.events);
            }

        } catch (error) {
            console.error('Arena Status konnte nicht geladen werden:', error);
        }
    }

    async loadMonsterList() {
        try {
            const response = await fetch(`${this.apiBase}/api/arena/monsters`);
            const data = await response.json();
            const monsters = data.monsters || [];  // API gibt {success, monsters, count} zurück

            const listElement = document.getElementById('monster-list');
            listElement.innerHTML = '<h3>🎭 Monster in der Arena</h3>';

            monsters.forEach(monster => {
                const monsterCard = this.createMonsterCard(monster);
                listElement.appendChild(monsterCard);
            });

        } catch (error) {
            console.error('Monster-Liste konnte nicht geladen werden (Offline-Modus):', error);
            // Offline-Fallback: Zeige Mock-Monster
            const listElement = document.getElementById('monster-list');
            if (listElement) {
                const mockMonsters = [
                    { id: 'mock_1', name: 'Schattenwolf', rank: 'Gladiator', level: 5, type: 'Bestie', has_grudge: false, stats: { hp: 80, attack: 14, defense: 8 } },
                    { id: 'mock_2', name: 'Frostgolem', rank: 'Champion', level: 8, type: 'Elementar', has_grudge: false, stats: { hp: 120, attack: 18, defense: 15 } },
                    { id: 'mock_3', name: 'Schattenritter', rank: 'Gebietsherrscher', level: 12, type: 'Untot', has_grudge: true, stats: { hp: 150, attack: 22, defense: 12 } }
                ];
                listElement.innerHTML = '<h3>🎭 Arena-Gegner (Offline)</h3>';
                mockMonsters.forEach(monster => {
                    const card = this.createMonsterCard(monster);
                    listElement.appendChild(card);
                });
            }
        }
    }

    createMonsterCard(monster) {
        const card = document.createElement('div');
        card.className = 'monster-card';
        if (monster.has_grudge) {
            card.classList.add('has-grudge');
        }

        // Rang-basierte Farben
        const rankColors = {
            'ARENA-KÖNIG': 'gold',
            'Gebietsherrscher': 'purple',
            'Champion': 'blue',
            'Gladiator': 'green',
            'Kämpfer': 'gray',
            'Niemand': 'darkgray'
        };

        card.innerHTML = `
            <div class="monster-header" style="border-left: 4px solid ${rankColors[monster.rank] || 'gray'}">
                <div class="monster-name">
                    ${monster.name}
                    ${monster.has_grudge ? '<span class="grudge-icon" title="Hat eine Rechnung mit dir offen!">🔥</span>' : ''}
                </div>
                <div class="monster-level">Lvl ${monster.level}</div>
            </div>

            <div class="monster-info">
                <span class="monster-type">${monster.type}</span>
                <span class="monster-rank">${monster.rank}</span>
                <span class="monster-kills">💀 ${monster.kills}</span>
            </div>

            <div class="monster-actions">
                <button class="challenge-btn" data-monster-id="${monster.id}">
                    HERAUSFORDERN
                </button>
                <button class="profile-btn" data-monster-id="${monster.id}">
                    PROFIL
                </button>
            </div>
        `;

        // Event Listeners
        card.querySelector('.challenge-btn').addEventListener('click', (e) => {
            this.startBattle(e.target.dataset.monsterId);
        });

        card.querySelector('.profile-btn').addEventListener('click', (e) => {
            this.showMonsterProfile(e.target.dataset.monsterId);
        });

        return card;
    }

    async startBattle(monsterId = null) {
        try {
            const data = monsterId ? { monster_id: monsterId } : {};
            data.stakes = 'ranking'; // oder 'items', 'title'

            const response = await fetch(`${this.apiBase}/api/arena/challenge`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const battle = await response.json();

            if (battle.battle_started) {
                this.currentBattle = battle;

                // NUTZE UNIFIED COMBAT SYSTEM wenn verfügbar
                if (window.UnifiedCombat) {
                    // Verstecke Arena Panel während Kampf
                    this.arenaPanel.style.display = 'none';

                    // Starte Combat mit Monster-Daten
                    window.UnifiedCombat.startCombat({
                        type: 'arena',
                        enemy: {
                            name: battle.monster?.basic?.name || 'Arena-Gegner',
                            hp: battle.monster?.stats?.hp || 80,
                            maxHp: battle.monster?.stats?.hp || 80,
                            attack: battle.monster?.stats?.attack || 15,
                            defense: battle.monster?.stats?.defense || 8,
                            speed: battle.monster?.stats?.speed || 1.0,
                            xp: battle.monster?.stats?.xp || 50,
                            loot: battle.monster?.loot || [],
                            traits: battle.monster?.personality?.traits || [],
                            element: battle.monster?.basic?.element || null
                        },
                        location: 'Nemesis Arena',
                        isHardcore: false,
                        waveNumber: 0
                    });

                    // Callback für Arena nach Kampf
                    window.onCombatVictory = (result) => {
                        if (result.type === 'arena') {
                            this.playerStats.wins++;
                            document.getElementById('player-wins').textContent = this.playerStats.wins;
                            this.arenaPanel.style.display = 'flex';
                        }
                    };
                    window.onCombatDefeat = (result) => {
                        if (result.type === 'arena') {
                            this.playerStats.losses++;
                            document.getElementById('player-losses').textContent = this.playerStats.losses;
                            this.arenaPanel.style.display = 'flex';
                        }
                    };
                } else {
                    // Fallback zum alten System
                    this.showBattleScreen(battle);
                }
            }

        } catch (error) {
            console.error('Kampf konnte nicht gestartet werden:', error);
            // Fallback mit Mock-Daten für Offline
            if (window.UnifiedCombat) {
                this.arenaPanel.style.display = 'none';
                window.UnifiedCombat.startCombat({
                    type: 'arena',
                    enemy: {
                        name: 'Arena-Champion',
                        hp: 100,
                        attack: 18,
                        defense: 10,
                        speed: 1.0,
                        xp: 60,
                        loot: ['gold_coin', 'arena_token']
                    },
                    location: 'Nemesis Arena',
                    isHardcore: false
                });

                // Callbacks auch im Offline-Modus setzen
                window.onCombatVictory = (result) => {
                    if (result.type === 'arena') {
                        this.playerStats.wins++;
                        document.getElementById('player-wins').textContent = this.playerStats.wins;
                        this.arenaPanel.style.display = 'flex';
                    }
                };
                window.onCombatDefeat = (result) => {
                    if (result.type === 'arena') {
                        this.playerStats.losses++;
                        document.getElementById('player-losses').textContent = this.playerStats.losses;
                        this.arenaPanel.style.display = 'flex';
                    }
                };
            }
        }
    }

    showBattleScreen(battle) {
        const battleScreen = document.createElement('div');
        battleScreen.id = 'battle-screen';
        battleScreen.className = 'arena-battle-screen';

        // Grudge-Match Special Effects
        if (battle.has_grudge) {
            battleScreen.classList.add('grudge-match');
        }

        battleScreen.innerHTML = `
            <div class="battle-header">
                <h2>⚔️ ARENA-KAMPF ⚔️</h2>
                ${battle.has_grudge ? '<div class="grudge-banner">🔥 RACHE-KAMPF! 🔥</div>' : ''}
            </div>

            <div class="battle-arena">
                <div class="fighter player-side">
                    <div class="fighter-name">KUJA</div>
                    <div class="hp-bar">
                        <div id="player-hp-fill" class="hp-fill" style="width: 100%"></div>
                        <span class="hp-text">100/100</span>
                    </div>
                    <div class="fighter-sprite">
                        <img src="/assets/player.png" alt="Player">
                    </div>
                </div>

                <div class="battle-center">
                    <div class="versus">VS</div>
                    <div id="battle-effects">
                        <!-- Kampf-Effekte hier -->
                    </div>
                </div>

                <div class="fighter monster-side">
                    <div class="fighter-name">${battle.monster.basic.name}</div>
                    <div class="hp-bar">
                        <div id="monster-hp-fill" class="hp-fill enemy" style="width: 100%"></div>
                        <span class="hp-text">${battle.monster.stats.hp}</span>
                    </div>
                    <div class="fighter-sprite">
                        <div class="monster-model">${this.getMonsterEmoji(battle.monster.basic.type)}</div>
                    </div>
                    <div class="monster-traits">
                        ${battle.monster.personality.traits.map(t => `<span class="trait">${t}</span>`).join('')}
                    </div>
                </div>
            </div>

            <div class="battle-log" id="battle-log">
                <div class="log-entry intro">${battle.intro_message}</div>
            </div>

            <div class="battle-controls">
                <div class="action-buttons">
                    <button class="action-btn attack" data-action="attack">
                        ⚔️ ANGRIFF
                    </button>
                    <button class="action-btn skill" data-action="combo_5hit">
                        💥 COMBO
                    </button>
                    <button class="action-btn dodge" data-action="perfect_dodge_counter">
                        🛡️ KONTER
                    </button>
                    <button class="action-btn special" data-action="charged_attack">
                        ⚡ SPECIAL
                    </button>
                </div>

                <button id="flee-btn" class="flee-btn">FLIEHEN</button>
            </div>

            ${battle.special_rules && battle.special_rules.length > 0 ? `
                <div class="special-rules">
                    <h4>⚠️ Spezial-Regeln:</h4>
                    ${battle.special_rules.map(rule => `<div>${rule}</div>`).join('')}
                </div>
            ` : ''}
        `;

        document.body.appendChild(battleScreen);

        // Battle Action Listeners
        battleScreen.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.performBattleAction(e.target.dataset.action);
            });
        });

        // Flee Button
        battleScreen.querySelector('#flee-btn').addEventListener('click', () => {
            this.fleeBattle();
        });
    }

    async performBattleAction(action) {
        if (!this.currentBattle) return;

        try {
            const response = await fetch(`${this.apiBase}/api/arena/battle/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action })
            });

            const result = await response.json();

            // Update Battle Display
            this.updateBattleDisplay(result);

            // Check für Kampf-Ende
            if (result.battle_over) {
                this.handleBattleEnd(result);
            }

        } catch (error) {
            console.error('Kampf-Aktion fehlgeschlagen:', error);
        }
    }

    updateBattleDisplay(result) {
        // Update HP Bars
        if (result.player_hp !== undefined) {
            const playerHpBar = document.getElementById('player-hp-fill');
            playerHpBar.style.width = `${result.player_hp}%`;
            playerHpBar.parentElement.querySelector('.hp-text').textContent = `${result.player_hp}/100`;
        }

        if (result.monster_hp !== undefined) {
            const monsterHpBar = document.getElementById('monster-hp-fill');
            const maxHp = parseInt(this.currentBattle.monster.stats.hp.split('/')[1]);
            const hpPercent = (result.monster_hp / maxHp) * 100;
            monsterHpBar.style.width = `${hpPercent}%`;
            monsterHpBar.parentElement.querySelector('.hp-text').textContent = `${result.monster_hp}/${maxHp}`;
        }

        // Add to Battle Log
        if (result.last_exchange) {
            const log = document.getElementById('battle-log');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `
                <span class="player-action">Du: ${result.last_exchange.player_action} (${result.last_exchange.player_damage} DMG)</span>
                <span class="monster-action">Gegner: ${result.last_exchange.monster_action} (${result.last_exchange.monster_damage} DMG)</span>
            `;
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
        }
    }

    handleBattleEnd(result) {
        const endScreen = document.createElement('div');
        endScreen.className = 'battle-end-screen';

        if (result.winner === 'player') {
            // SIEG!
            endScreen.innerHTML = `
                <div class="victory-screen">
                    <h2>🏆 SIEG! 🏆</h2>

                    ${result.result.nemesis_event ? `
                        <div class="nemesis-event">
                            <h3>⚠️ NEMESIS EVENT!</h3>
                            <p>${result.result.nemesis_event.message}</p>
                        </div>
                    ` : ''}

                    <div class="rewards">
                        <h3>Belohnungen:</h3>
                        <div class="loot">
                            💰 Gold: ${result.rewards.gold}<br>
                            ⭐ XP: ${result.rewards.xp}<br>
                            ${result.rewards.items.map(item =>
                                `<div class="item ${item.rarity}">${item.name}</div>`
                            ).join('')}
                        </div>
                    </div>

                    <button class="continue-btn">WEITER</button>
                </div>
            `;

            // Update Player Stats
            this.playerStats.wins++;

        } else {
            // NIEDERLAGE
            endScreen.innerHTML = `
                <div class="defeat-screen">
                    <h2>💀 NIEDERLAGE 💀</h2>

                    <div class="monster-taunt">
                        "${result.result.monster_reaction}"
                    </div>

                    ${result.result.nemesis_event ? `
                        <div class="nemesis-event">
                            <h3>${result.result.nemesis_event.type === 'promotion' ? '📈 BEFÖRDERUNG!' : '⚠️ EVENT!'}</h3>
                            <p>${result.result.nemesis_event.message}</p>
                        </div>
                    ` : ''}

                    ${result.result.new_ruler ? `
                        <div class="new-ruler">
                            <h3>👑 NEUER HERRSCHER!</h3>
                            <p>${result.result.new_ruler.monster} herrscht nun über ${result.result.new_ruler.region}!</p>
                            <p class="region-effects">${result.result.new_ruler.effects.description}</p>
                        </div>
                    ` : ''}

                    <div class="consequences">
                        <h3>Konsequenzen:</h3>
                        ${Object.entries(result.consequences).map(([key, value]) =>
                            `<div>${key}: ${value}</div>`
                        ).join('')}
                    </div>

                    <button class="revenge-btn">RACHE SCHWÖREN</button>
                    <button class="continue-btn">WEITER</button>
                </div>
            `;

            // Update Player Stats
            this.playerStats.losses++;
        }

        document.getElementById('battle-screen').appendChild(endScreen);

        // Event Listeners
        endScreen.querySelector('.continue-btn').addEventListener('click', () => {
            document.getElementById('battle-screen').remove();
            this.loadArenaStatus(); // Refresh
        });

        const revengeBtn = endScreen.querySelector('.revenge-btn');
        if (revengeBtn) {
            revengeBtn.addEventListener('click', () => {
                // Markiere als Nemesis
                if (typeof notify !== 'undefined') {
                    notify('Du hast Rache geschworen! Dieses Monster wird sich an dich erinnern...', 'warning');
                }
                document.getElementById('battle-screen').remove();
                this.loadArenaStatus();
            });
        }
    }

    async showMonsterProfile(monsterId) {
        try {
            const response = await fetch(`${this.apiBase}/api/arena/monster/${monsterId}`);
            const profile = await response.json();

            const profileModal = document.createElement('div');
            profileModal.className = 'monster-profile-modal';
            profileModal.innerHTML = `
                <div class="profile-content">
                    <button class="close-profile">✖</button>

                    <h2>${profile.basic.name}</h2>
                    <div class="profile-rank">${profile.basic.rank}</div>

                    <div class="profile-stats">
                        <h3>📊 Statistiken</h3>
                        <div class="stat-grid">
                            <div>Level: ${profile.basic.level}</div>
                            <div>Typ: ${profile.basic.type}</div>
                            <div>HP: ${profile.stats.hp}</div>
                            <div>Angriff: ${profile.stats.attack}</div>
                            <div>Verteidigung: ${profile.stats.defense}</div>
                            <div>Geschwindigkeit: ${profile.stats.speed}</div>
                        </div>
                    </div>

                    <div class="profile-record">
                        <h3>🏆 Kampfbilanz</h3>
                        <div>Siege: ${profile.record.kills}</div>
                        <div>Niederlagen: ${profile.record.deaths}</div>
                        ${profile.record.nemesis_of.length > 0 ? `
                            <div class="nemesis-list">
                                Erzfeind von: ${profile.record.nemesis_of.join(', ')}
                            </div>
                        ` : ''}
                    </div>

                    <div class="profile-personality">
                        <h3>🎭 Persönlichkeit</h3>
                        <div class="traits">
                            ${profile.personality.traits.map(t => `<span class="trait">${t}</span>`).join('')}
                        </div>

                        ${profile.personality.scars.length > 0 ? `
                            <h4>Narben & Trophäen:</h4>
                            <ul>
                                ${profile.personality.scars.map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        ` : ''}

                        <h4>Spezial-Moves:</h4>
                        <div class="moves">
                            ${profile.personality.moves.map(m => `<span class="move">${m}</span>`).join('')}
                        </div>

                        ${profile.personality.weaknesses.length > 0 ? `
                            <h4>Schwächen:</h4>
                            <ul class="weaknesses">
                                ${profile.personality.weaknesses.map(w => `<li>${w}</li>`).join('')}
                            </ul>
                        ` : ''}
                    </div>
                </div>
            `;

            document.body.appendChild(profileModal);

            profileModal.querySelector('.close-profile').addEventListener('click', () => {
                profileModal.remove();
            });

        } catch (error) {
            console.error('Monster-Profil konnte nicht geladen werden:', error);
        }
    }

    displayArenaEvents(events) {
        events.forEach(event => {
            if (event.type === 'monster_duel') {
                if (typeof notify !== 'undefined') {
                    notify(`⚔️ Arena-Event: ${event.message}`, 'info');
                }
            }
        });
    }

    updateArenaEvents() {
        // Periodisches Update für Monster vs Monster Kämpfe
        this.loadArenaStatus();
    }

    fleeBattle() {
        if (!this._fleeConfirmPending) {
            this._fleeConfirmPending = true;
            notify('⚠️ Wirklich fliehen? Klicke nochmal zum Bestätigen!', 'warning');
            setTimeout(() => { this._fleeConfirmPending = false; }, 3000);
            return;
        }
        this._fleeConfirmPending = false;
        const battleScreen = document.getElementById('battle-screen');
        if (battleScreen) battleScreen.remove();
        this.playerStats.losses++;
        notify('Du bist aus der Arena geflohen...', 'warning');
    }

    setupEventListeners() {
        // Tab-System
        document.querySelectorAll('.arena-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                // Deaktiviere alle Tabs
                document.querySelectorAll('.arena-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

                // Aktiviere gewählten Tab
                e.target.classList.add('active');
                const tabName = e.target.dataset.tab;
                document.getElementById(`${tabName}-view`).classList.add('active');

                // Lade spezifische Daten wenn nötig
                if (tabName === 'hierarchy') {
                    this.loadHierarchy();
                } else if (tabName === 'regions') {
                    this.loadRegions();
                } else if (tabName === 'nemesis') {
                    this.loadNemesisList();
                } else if (tabName === 'waves') {
                    this.updateWaveUI();
                }
            });
        });

        // Close Button
        document.getElementById('arena-close').addEventListener('click', () => {
            this.arenaPanel.style.display = 'none';
        });

        // Quick Battle
        document.getElementById('quick-battle-btn').addEventListener('click', () => {
            this.startBattle();
        });

        // Wave Mode Buttons
        document.getElementById('start-wave-btn')?.addEventListener('click', () => {
            this.startWaveBattle();
        });

        document.getElementById('reset-waves-btn')?.addEventListener('click', () => {
            this.resetWaves();
        });
    }

    // ========== WAVE MODE SYSTEM ==========

    initWaveState() {
        // Lade gespeicherten Wave-Stand aus localStorage
        const saved = localStorage.getItem('arenaWaveState');
        if (saved) {
            try {
                this.waveState = JSON.parse(saved);
            } catch (e) {
                this.waveState = this.getDefaultWaveState();
            }
        } else {
            this.waveState = this.getDefaultWaveState();
        }
    }

    getDefaultWaveState() {
        return {
            currentWave: 0,
            highestWave: 0,
            hardcoreUnlocked: false,
            inHardcoreMode: false,
            totalWins: 0,
            totalLosses: 0,
            medals: []
        };
    }

    saveWaveState() {
        localStorage.setItem('arenaWaveState', JSON.stringify(this.waveState));
    }

    updateWaveUI() {
        if (!this.waveState) {
            this.initWaveState();
        }

        const waveNum = document.getElementById('current-wave-num');
        const progressFill = document.getElementById('wave-progress-fill');
        const modeLabel = document.getElementById('wave-mode-label');
        const startBtn = document.getElementById('start-wave-btn');

        if (waveNum) {
            waveNum.textContent = this.waveState.currentWave;
        }

        if (progressFill) {
            const progress = Math.min((this.waveState.currentWave / 15) * 100, 100);
            progressFill.style.width = progress + '%';

            // Farbe ändern je nach Fortschritt
            if (this.waveState.currentWave >= 15) {
                progressFill.style.background = 'linear-gradient(90deg, #FFD700, #FFA500)'; // Gold
            } else if (this.waveState.currentWave >= 10) {
                progressFill.style.background = 'linear-gradient(90deg, #C0C0C0, #A0A0A0)'; // Silber
            } else if (this.waveState.currentWave >= 5) {
                progressFill.style.background = 'linear-gradient(90deg, #CD7F32, #8B4513)'; // Bronze
            }
        }

        if (modeLabel) {
            if (this.waveState.inHardcoreMode) {
                modeLabel.textContent = '⚠️ ECHTER MODUS (Hardcore!)';
                modeLabel.style.color = '#ff4444';
            } else if (this.waveState.hardcoreUnlocked) {
                modeLabel.textContent = '✅ Training abgeschlossen! Echter Modus verfügbar!';
                modeLabel.style.color = '#44ff44';
            } else {
                modeLabel.textContent = 'Training-Modus (kein echter Tod)';
                modeLabel.style.color = '#aaaaaa';
            }
        }

        if (startBtn) {
            const nextWave = this.waveState.currentWave + 1;
            if (this.waveState.inHardcoreMode) {
                startBtn.textContent = `⚠️ HARDCORE WELLE ${nextWave} STARTEN`;
                startBtn.style.background = 'linear-gradient(135deg, #ff4444, #cc0000)';
            } else if (nextWave > 15 && !this.waveState.hardcoreUnlocked) {
                startBtn.textContent = '🏆 Training abgeschlossen!';
                startBtn.disabled = true;
            } else {
                startBtn.textContent = `🌊 WELLE ${nextWave} STARTEN`;
                startBtn.style.background = '';
            }
        }
    }

    async startWaveBattle() {
        if (!this.waveState) {
            this.initWaveState();
        }

        const nextWave = this.waveState.currentWave + 1;
        const isHardcore = this.waveState.inHardcoreMode || nextWave > 15;

        // Warnung vor Hardcore
        if (nextWave === 16 && !this.waveState.inHardcoreMode) {
            if (!this._hardcoreConfirmed) {
                this._hardcoreConfirmed = true;
                notify('⚠️ ACHTUNG! Ab Welle 16 = HARDCORE! Niederlagen haben echte Konsequenzen. Nochmal klicken zum Bestätigen!', 'warning');
                setTimeout(() => { this._hardcoreConfirmed = false; }, 5000);
                return;
            }
            this._hardcoreConfirmed = false;
            this.waveState.inHardcoreMode = true;
            this.saveWaveState();
            notify('💀 HARDCORE-MODUS aktiviert!', 'error');
        }

        // Generiere Wellen-Gegner (skaliert mit Welle)
        const waveEnemies = this.generateWaveEnemies(nextWave);

        // NUTZE REAL 3D COMBAT (Tastatur: Q/E/Space)
        if (window.Real3DCombat && window.Real3DCombat.startCombat) {
            this.arenaPanel.style.display = 'none';

            // Teleport player to Arena FIRST!
            if (window.switchRoom) {
                window.switchRoom('Kampfarena');
            } else if (window.DigiviceSystem && window.DigiviceSystem.switchRoom) {
                window.DigiviceSystem.switchRoom('Kampfarena');
            }

            const scene = window.getScene ? window.getScene() : null;
            const arenaCenter = { x: 0, y: 0, z: -10 };

            if (scene) {
                // Setup Callbacks BEFORE starting combat
                const self = this;
                window.onCombatVictory = (result) => {
                    if (result.type === 'real3d') {
                        console.log(`✅ Welle ${nextWave} geschafft!`);
                        self.onWaveBattleEnd(true);
                        self.arenaPanel.style.display = 'flex';
                    }
                };

                window.onCombatDefeat = (result) => {
                    if (result.type === 'real3d') {
                        console.log(`💀 Welle ${nextWave} verloren!`);
                        self.onWaveBattleEnd(false);
                        self.arenaPanel.style.display = 'flex';
                    }
                };

                // Konvertiere Enemy-Namen zu Types die Real3DCombat kennt
                const enemyTypes = waveEnemies.map(e => {
                    // Map zu bekannten Real3DCombat Types
                    const nameToType = {
                        'Skelett-Krieger': 'skeleton_warrior',
                        'Goblin-Räuber': 'goblin',
                        'Wolf': 'wolf',
                        'Ork-Krieger': 'corrupted_knight',
                        'Dunkel-Magier': 'skeleton_mage',
                        'Elite-Ritter': 'corrupted_knight',
                        'Drachen-Welpe': 'barbarian_boss'
                    };
                    return nameToType[e.name] || 'skeleton_warrior';
                });

                window.Real3DCombat.startCombat(enemyTypes, scene, arenaCenter);
                console.log(`⚔️ Welle ${nextWave} Combat gestartet! ${enemyTypes.length} Gegner`);
            } else {
                console.error('Scene nicht verfügbar!');
            }

        } else if (window.UnifiedCombat) {
            // Fallback: Unified Combat
            this.arenaPanel.style.display = 'none';

            window.UnifiedCombat.startCombat({
                type: 'arena',
                enemies: waveEnemies,
                location: `Nemesis Arena - Welle ${nextWave}`,
                isHardcore: isHardcore,
                waveNumber: nextWave
            });

            const self = this;
            window.onCombatVictory = (result) => {
                if (result.type === 'arena') {
                    self.onWaveBattleEnd(true);
                    self.arenaPanel.style.display = 'flex';
                }
            };
            window.onCombatDefeat = (result) => {
                if (result.type === 'arena') {
                    self.onWaveBattleEnd(false);
                    self.arenaPanel.style.display = 'flex';
                }
            };

        } else {
            // Fallback zum alten System
            try {
                const response = await fetch(`${this.apiBase}/api/arena/wave-battle`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ wave: nextWave, hardcore: isHardcore })
                });
                const battle = await response.json();
                if (battle.battle_started || battle.success) {
                    this.currentBattle = battle;
                    this.showBattleScreen(battle);
                }
            } catch (error) {
                console.error('Wave-Kampf Fehler:', error);
            }
        }
    }

    /**
     * Generiert Gegner für eine Welle (skaliert mit Wellen-Nummer)
     */
    generateWaveEnemies(wave) {
        const baseEnemies = [
            { name: 'Skelett-Krieger', hp: 40, attack: 10, defense: 5, speed: 1.0, xp: 15, tier: 1 },
            { name: 'Goblin-Räuber', hp: 30, attack: 12, defense: 3, speed: 1.3, xp: 12, tier: 1 },
            { name: 'Wolf', hp: 35, attack: 8, defense: 4, speed: 1.4, xp: 14, tier: 1 },
            { name: 'Ork-Krieger', hp: 60, attack: 15, defense: 8, speed: 0.8, xp: 25, tier: 2 },
            { name: 'Dunkel-Magier', hp: 45, attack: 20, defense: 3, speed: 0.9, xp: 30, tier: 2 },
            { name: 'Elite-Ritter', hp: 80, attack: 18, defense: 12, speed: 0.7, xp: 40, tier: 3 },
            { name: 'Drachen-Welpe', hp: 100, attack: 25, defense: 10, speed: 1.0, xp: 60, tier: 3 }
        ];

        // Schwierigkeit skaliert mit Welle
        const scaleFactor = 1 + (wave - 1) * 0.15;  // +15% pro Welle
        const enemyCount = Math.min(1 + Math.floor(wave / 3), 4);  // 1-4 Gegner

        // Wähle Gegner basierend auf Welle (höhere Wellen = stärkere Gegner)
        const availableTiers = wave < 5 ? [1] : (wave < 10 ? [1, 2] : [1, 2, 3]);
        const tierEnemies = baseEnemies.filter(e => availableTiers.includes(e.tier));

        const enemies = [];
        for (let i = 0; i < enemyCount; i++) {
            const template = tierEnemies[Math.floor(Math.random() * tierEnemies.length)];
            enemies.push({
                name: template.name,
                hp: Math.floor(template.hp * scaleFactor),
                maxHp: Math.floor(template.hp * scaleFactor),
                attack: Math.floor(template.attack * scaleFactor),
                defense: Math.floor(template.defense * scaleFactor),
                speed: template.speed,
                xp: Math.floor(template.xp * scaleFactor),
                loot: ['gold_coin', 'arena_token']
            });
        }

        // Boss auf Wellen 5, 10, 15
        if (wave === 5 || wave === 10 || wave === 15) {
            const bossScale = wave / 5;
            enemies.push({
                name: wave === 15 ? '👑 Arena-Champion' : (wave === 10 ? '💀 Dunkler Herrscher' : '⚔️ Elite-Wächter'),
                hp: Math.floor(150 * bossScale * scaleFactor),
                maxHp: Math.floor(150 * bossScale * scaleFactor),
                attack: Math.floor(25 * bossScale * scaleFactor),
                defense: Math.floor(15 * bossScale * scaleFactor),
                speed: 0.8,
                xp: Math.floor(100 * bossScale),
                loot: ['rare_gem', 'arena_crown', 'gold_pile'],
                traits: ['Boss', 'Verstärkt']
            });
        }

        return enemies;
    }

    onWaveBattleEnd(won) {
        if (!this.waveState) this.initWaveState();

        if (won) {
            this.waveState.currentWave++;
            this.waveState.totalWins++;

            // Medaillen vergeben
            if (this.waveState.currentWave === 5 && !this.waveState.medals.includes('bronze')) {
                this.waveState.medals.push('bronze');
                notify('🥉 BRONZEMEDAILLE erhalten! Weiter so!', 'success');
            } else if (this.waveState.currentWave === 10 && !this.waveState.medals.includes('silver')) {
                this.waveState.medals.push('silver');
                notify('🥈 SILBERMEDAILLE erhalten! Fantastisch!', 'success');
            } else if (this.waveState.currentWave === 15 && !this.waveState.medals.includes('gold')) {
                this.waveState.medals.push('gold');
                this.waveState.hardcoreUnlocked = true;
                notify('🥇 GOLDMEDAILLE! ECHTER MODUS freigeschaltet!', 'success');
            }

            if (this.waveState.currentWave > this.waveState.highestWave) {
                this.waveState.highestWave = this.waveState.currentWave;
            }
        } else {
            this.waveState.totalLosses++;

            if (this.waveState.inHardcoreMode) {
                // Echte Konsequenzen im Hardcore-Modus
                notify('💀 NIEDERLAGE im Hardcore-Modus! Dein Digimon braucht Erholung...', 'error');
            } else {
                notify('Training-Niederlage! Im Training verlierst du nichts. Versuch es nochmal!', 'warning');
            }
        }

        this.saveWaveState();
        this.updateWaveUI();
    }

    resetWaves() {
        if (this.waveState?.inHardcoreMode) {
            notify('Im Hardcore-Modus kann nicht zurückgesetzt werden!', 'error');
            return;
        }

        if (!this._resetConfirmPending) {
            this._resetConfirmPending = true;
            notify('⚠️ Training zurücksetzen? Medaillen bleiben. Nochmal klicken zum Bestätigen!', 'warning');
            setTimeout(() => { this._resetConfirmPending = false; }, 3000);
            return;
        }
        this._resetConfirmPending = false;
        const medals = this.waveState?.medals || [];
        this.waveState = this.getDefaultWaveState();
        this.waveState.medals = medals;
        this.saveWaveState();
        this.updateWaveUI();
        notify('Training zurückgesetzt! Starte bei Welle 1.', 'info');
    }

    async loadHierarchy() {
        try {
            const response = await fetch(`${this.apiBase}/api/arena/hierarchy`);
            const hierarchy = await response.text();

            document.querySelector('#hierarchy-view .hierarchy-display').innerHTML = `<pre>${hierarchy}</pre>`;

        } catch (error) {
            console.error('Hierarchie konnte nicht geladen werden:', error);
        }
    }

    async loadRegions() {
        // Lade Regions-Daten und zeige Herrscher-Effekte
        const regions = [
            'Samtmoos-Tiefwald', 'Reich der Drei', 'Salzwind-Küste',
            'Blitzebene', 'Grünschlamm-Sumpf', 'Magmaströme',
            'Heiße Dünen', 'Tiefenhöhlen'
        ];

        const grid = document.getElementById('regions-grid');
        grid.innerHTML = '';

        regions.forEach(region => {
            const regionCard = document.createElement('div');
            regionCard.className = 'region-card';
            regionCard.innerHTML = `
                <h4>${region}</h4>
                <div class="ruler-info">
                    <span>Herrscher: </span>
                    <strong>[Wird geladen...]</strong>
                </div>
                <div class="region-effects">
                    <!-- Effekte hier -->
                </div>
            `;
            grid.appendChild(regionCard);
        });
    }

    loadNemesisList() {
        // Zeige Monster die den Spieler getötet haben
        const nemesisList = document.getElementById('nemesis-list');
        nemesisList.innerHTML = '<p>Monster die dich besiegt haben werden hier erscheinen...</p>';

        // Würde aus playerStats.nemesis_list laden
        if (this.playerStats.nemesis_list && this.playerStats.nemesis_list.length > 0) {
            nemesisList.innerHTML = '';
            this.playerStats.nemesis_list.forEach(nemesisId => {
                // Lade Monster-Details und zeige sie
            });
        }
    }

    getMonsterEmoji(type) {
        const emojis = {
            'Goblin': '👺',
            'Slime': '🟢',
            'Ork': '🧟',
            'Dämon': '👹',
            'Drache': '🐲',
            'Schatten': '👤',
            'Elementar': '🔥',
            'Untot': '💀'
        };
        return emojis[type] || '👾';
    }
}

// CSS Styles für Arena
const arenaStyles = `
<style>
.arena-nemesis-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 1200px;
    height: 80vh;
    background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
    border: 3px solid #667eea;
    border-radius: 15px;
    box-shadow: 0 0 50px rgba(102, 126, 234, 0.5);
    z-index: 10000;
    display: none;
    flex-direction: column;
}

.arena-header {
    padding: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 12px 12px 0 0;
}

.arena-tabs {
    display: flex;
    background: rgba(0,0,0,0.3);
    padding: 10px;
    gap: 10px;
}

.arena-tab {
    padding: 10px 20px;
    background: rgba(255,255,255,0.1);
    border: 2px solid transparent;
    color: #a0a0a0;
    cursor: pointer;
    transition: all 0.3s;
}

.arena-tab.active {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-color: #fff;
}

.arena-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

/* WAVE MODE STYLES */
.wave-mode-container {
    padding: 20px;
}

.wave-progress {
    margin: 20px 0;
}

.wave-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.current-wave {
    font-size: 1.5em;
    color: #FFD700;
}

.wave-mode-type {
    font-size: 0.9em;
    padding: 5px 10px;
    background: rgba(255,255,255,0.1);
    border-radius: 5px;
}

.wave-progress-bar {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 20px;
    overflow: hidden;
}

.wave-progress-fill {
    background: linear-gradient(90deg, #667eea, #764ba2);
    height: 100%;
    transition: width 0.5s ease, background 0.5s ease;
}

.wave-description {
    background: rgba(0,0,0,0.3);
    padding: 15px;
    border-radius: 10px;
    margin: 20px 0;
}

.wave-description p {
    margin: 8px 0;
    color: #ccc;
}

.wave-buttons {
    display: flex;
    gap: 10px;
    margin: 20px 0;
}

.wave-buttons .secondary {
    flex: 0 0 auto;
}

.wave-rewards {
    background: rgba(102,126,234,0.1);
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 10px;
    padding: 15px;
}

.wave-rewards h4 {
    color: #FFD700;
    margin: 0 0 10px 0;
}

.wave-rewards ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.wave-rewards li {
    padding: 5px 0;
    color: #aaa;
}

.monster-card {
    background: rgba(255,255,255,0.05);
    border: 2px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    transition: all 0.3s;
}

.monster-card:hover {
    border-color: #667eea;
    box-shadow: 0 0 20px rgba(102,126,234,0.3);
}

.monster-card.has-grudge {
    border-color: #ff4444;
    animation: grudge-pulse 2s infinite;
}

@keyframes grudge-pulse {
    0%, 100% { box-shadow: 0 0 10px rgba(255,68,68,0.5); }
    50% { box-shadow: 0 0 30px rgba(255,68,68,0.8); }
}

.grudge-icon {
    color: #ff4444;
    font-size: 1.2em;
    animation: fire-flicker 1s infinite;
}

@keyframes fire-flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.battle-btn {
    padding: 15px 30px;
    background: linear-gradient(135deg, #ff6b6b, #ff4757);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.2em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
}

.battle-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 30px rgba(255,107,107,0.5);
}

.glow-effect {
    animation: glow 2s infinite;
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(255,107,107,0.5); }
    50% { box-shadow: 0 0 40px rgba(255,107,107,0.8); }
}

/* Battle Screen Styles */
.arena-battle-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #0a0a0a, #1a0000);
    z-index: 11000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.grudge-match {
    background: linear-gradient(135deg, #200000, #400000);
    animation: grudge-bg 3s infinite;
}

@keyframes grudge-bg {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.3); }
}

.battle-arena {
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    max-width: 1200px;
    padding: 40px;
}

.fighter {
    text-align: center;
}

.hp-bar {
    width: 200px;
    height: 25px;
    background: rgba(0,0,0,0.5);
    border: 2px solid #444;
    border-radius: 15px;
    overflow: hidden;
    position: relative;
    margin: 10px auto;
}

.hp-fill {
    height: 100%;
    background: linear-gradient(90deg, #2ecc71, #27ae60);
    transition: width 0.5s ease;
}

.hp-fill.enemy {
    background: linear-gradient(90deg, #e74c3c, #c0392b);
}

.monster-model {
    font-size: 100px;
    animation: monster-idle 2s infinite;
}

@keyframes monster-idle {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.action-btn {
    padding: 15px 25px;
    margin: 5px;
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
}

.action-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 5px 20px rgba(52,152,219,0.5);
}

.action-btn.attack { background: linear-gradient(135deg, #e74c3c, #c0392b); }
.action-btn.skill { background: linear-gradient(135deg, #f39c12, #e67e22); }
.action-btn.dodge { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
.action-btn.special { background: linear-gradient(135deg, #1abc9c, #16a085); }

.battle-log {
    width: 100%;
    max-width: 800px;
    height: 150px;
    background: rgba(0,0,0,0.7);
    border: 2px solid #333;
    border-radius: 10px;
    padding: 15px;
    margin: 20px auto;
    overflow-y: auto;
    color: #fff;
}

.log-entry {
    margin-bottom: 10px;
    padding: 5px;
    border-bottom: 1px solid #333;
}

.log-entry.intro {
    color: #f39c12;
    font-weight: bold;
    font-size: 1.1em;
}

/* Victory/Defeat Screens */
.battle-end-screen {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(135deg, #1a1a2e, #0f0f1e);
    border: 3px solid #667eea;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 0 50px rgba(102,126,234,0.8);
}

.victory-screen h2 {
    color: #f39c12;
    font-size: 3em;
    margin-bottom: 20px;
    animation: victory-pulse 1s infinite;
}

@keyframes victory-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.defeat-screen h2 {
    color: #e74c3c;
    font-size: 3em;
    margin-bottom: 20px;
}

.monster-taunt {
    font-style: italic;
    color: #ff6b6b;
    font-size: 1.2em;
    margin: 20px;
    padding: 15px;
    background: rgba(255,0,0,0.1);
    border-left: 4px solid #ff4444;
}

.nemesis-event {
    background: rgba(255,193,7,0.2);
    border: 2px solid #ffc107;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

.new-ruler {
    background: rgba(156,39,176,0.2);
    border: 2px solid #9c27b0;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

.region-effects {
    color: #f39c12;
    font-style: italic;
    margin-top: 10px;
}

.revenge-btn {
    padding: 15px 30px;
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
    margin: 10px;
    animation: revenge-pulse 2s infinite;
}

@keyframes revenge-pulse {
    0%, 100% { box-shadow: 0 0 10px rgba(231,76,60,0.5); }
    50% { box-shadow: 0 0 30px rgba(231,76,60,0.8); }
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 1.5em;
    cursor: pointer;
}

.continue-btn {
    padding: 15px 30px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
    margin: 10px;
}

.monster-profile-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    z-index: 12000;
    display: flex;
    justify-content: center;
    align-items: center;
}

.profile-content {
    background: linear-gradient(135deg, #1a1a2e, #0f0f1e);
    border: 3px solid #667eea;
    border-radius: 15px;
    padding: 30px;
    max-width: 600px;
    color: white;
    position: relative;
}

.close-profile {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    color: white;
    font-size: 1.5em;
    cursor: pointer;
}

.trait, .move {
    display: inline-block;
    padding: 5px 10px;
    margin: 3px;
    background: rgba(102,126,234,0.3);
    border-radius: 5px;
    font-size: 0.9em;
}
</style>
`;

// Füge Styles zum Document hinzu
document.head.insertAdjacentHTML('beforeend', arenaStyles);

// Initialize Arena System wenn DOM bereit
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.NemesisArena = new NemesisArenaUI();
    });
} else {
    window.NemesisArena = new NemesisArenaUI();
}

console.log('✅ Nemesis Arena System geladen!');
