/**
 * Nemesis Arena UI
 * Shadow of Mordor style hierarchy and nemesis display
 */

export class NemesisArenaUI {
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.currentTab = 'hierarchy';
        this.selectedMonster = null;
        this.arenaPanel = null;
        this.updateInterval = null;
    }

    /**
     * Initialize arena UI
     */
    init() {
        this.createArenaPanel();
        this.loadHierarchy();

        // Auto-refresh every 10 seconds
        this.updateInterval = setInterval(() => {
            this.refreshCurrentView();
        }, 10000);

        console.log('🏟️ Nemesis Arena UI initialized');
    }

    /**
     * Create the arena panel HTML
     */
    createArenaPanel() {
        // Remove existing panel if any
        const existing = document.getElementById('nemesis-arena-panel');
        if (existing) {
            existing.remove();
        }

        // Create panel
        const panel = document.createElement('div');
        panel.id = 'nemesis-arena-panel';
        panel.className = 'nemesis-arena-panel';
        panel.innerHTML = `
            <div class="arena-header">
                <h2>⚔️ Nemesis Arena ⚔️</h2>
                <button class="close-btn" onclick="this.closest('.nemesis-arena-panel').style.display='none'">✖</button>
            </div>

            <div class="arena-tabs">
                <button class="arena-tab active" data-tab="hierarchy">Hierarchie</button>
                <button class="arena-tab" data-tab="challengers">Herausforderer</button>
                <button class="arena-tab" data-tab="nemesis">Meine Nemesis</button>
                <button class="arena-tab" data-tab="regions">Gebiete</button>
            </div>

            <div class="arena-content">
                <div id="hierarchy-view" class="arena-view active"></div>
                <div id="challengers-view" class="arena-view"></div>
                <div id="nemesis-view" class="arena-view"></div>
                <div id="regions-view" class="arena-view"></div>
            </div>

            <div class="arena-footer">
                <button id="refresh-btn" class="btn-primary">🔄 Aktualisieren</button>
                <button id="challenge-btn" class="btn-danger" disabled>⚔️ Herausfordern</button>
            </div>
        `;

        document.body.appendChild(panel);
        this.arenaPanel = panel;

        // Add event listeners
        this.addEventListeners();

        // Add CSS if not already added
        this.addArenaStyles();
    }

    /**
     * Add event listeners
     */
    addEventListeners() {
        // Tab switching
        const tabs = this.arenaPanel.querySelectorAll('.arena-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Refresh button
        const refreshBtn = this.arenaPanel.querySelector('#refresh-btn');
        refreshBtn.addEventListener('click', () => {
            this.refreshCurrentView();
        });

        // Challenge button
        const challengeBtn = this.arenaPanel.querySelector('#challenge-btn');
        challengeBtn.addEventListener('click', () => {
            if (this.selectedMonster) {
                this.challengeMonster(this.selectedMonster);
            }
        });
    }

    /**
     * Switch between tabs
     */
    switchTab(tabName) {
        // Update tab buttons
        const tabs = this.arenaPanel.querySelectorAll('.arena-tab');
        tabs.forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Update views
        const views = this.arenaPanel.querySelectorAll('.arena-view');
        views.forEach(view => {
            view.classList.remove('active');
        });

        const activeView = this.arenaPanel.querySelector(`#${tabName}-view`);
        if (activeView) {
            activeView.classList.add('active');
        }

        this.currentTab = tabName;

        // Load content for tab
        this.loadTabContent(tabName);
    }

    /**
     * Load content for specific tab
     */
    async loadTabContent(tabName) {
        switch (tabName) {
            case 'hierarchy':
                await this.loadHierarchy();
                break;
            case 'challengers':
                await this.loadChallengers();
                break;
            case 'nemesis':
                await this.loadMyNemesis();
                break;
            case 'regions':
                await this.loadRegions();
                break;
        }
    }

    /**
     * Load arena hierarchy
     */
    async loadHierarchy() {
        const view = this.arenaPanel.querySelector('#hierarchy-view');
        view.innerHTML = '<div class="loading">⏳ Lade Hierarchie...</div>';

        try {
            const response = await this.apiClient.get('/api/game/arena/hierarchy');
            const hierarchy = response.data;

            view.innerHTML = this.renderHierarchy(hierarchy);
        } catch (error) {
            console.error('Failed to load hierarchy:', error);
            view.innerHTML = '<div class="error">❌ Fehler beim Laden der Hierarchie</div>';
        }
    }

    /**
     * Render hierarchy HTML
     */
    renderHierarchy(hierarchy) {
        let html = '<div class="hierarchy-pyramid">';

        // Arena King (Top)
        if (hierarchy.arena_king) {
            html += `
                <div class="rank-tier king-tier">
                    <h3>👑 ARENA-KÖNIG 👑</h3>
                    ${this.renderMonsterCard(hierarchy.arena_king, 'king')}
                </div>
            `;
        } else {
            html += `
                <div class="rank-tier king-tier">
                    <h3>👑 ARENA-KÖNIG 👑</h3>
                    <div class="empty-throne">Thron ist leer...</div>
                </div>
            `;
        }

        // Region Lords
        html += `
            <div class="rank-tier lord-tier">
                <h3>🏰 Gebietsherrscher (${hierarchy.region_lords.length})</h3>
                <div class="monster-grid">
                    ${hierarchy.region_lords.map(m => this.renderMonsterCard(m, 'lord')).join('')}
                </div>
            </div>
        `;

        // Champions
        html += `
            <div class="rank-tier champion-tier">
                <h3>⭐ Champions (${hierarchy.champions.length})</h3>
                <div class="monster-grid">
                    ${hierarchy.champions.map(m => this.renderMonsterCard(m, 'champion')).join('')}
                </div>
            </div>
        `;

        // Gladiators
        html += `
            <div class="rank-tier gladiator-tier">
                <h3>⚔️ Gladiatoren (${hierarchy.gladiators.length})</h3>
                <div class="monster-grid">
                    ${hierarchy.gladiators.slice(0, 10).map(m => this.renderMonsterCard(m, 'gladiator')).join('')}
                    ${hierarchy.gladiators.length > 10 ? `<div class="more-info">...und ${hierarchy.gladiators.length - 10} weitere</div>` : ''}
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    /**
     * Render a monster card
     */
    renderMonsterCard(monster, tier) {
        const healthPercent = (monster.current_health / monster.max_health) * 100;
        const scarsHTML = monster.has_scars ?
            `<div class="scars">⚠️ Narben: ${monster.scar_descriptions.join(', ')}</div>` : '';

        return `
            <div class="monster-card ${tier}-card" data-monster-id="${monster.id}">
                <div class="monster-header">
                    <div class="monster-name">${monster.name}</div>
                    <div class="monster-title">${monster.title}</div>
                </div>

                <div class="monster-info">
                    <div class="monster-type">${this.getTypeIcon(monster.monster_type)} ${monster.monster_type}</div>
                    <div class="monster-level">Level ${monster.level}</div>
                </div>

                <div class="monster-health">
                    <div class="health-bar">
                        <div class="health-fill" style="width: ${healthPercent}%"></div>
                    </div>
                    <div class="health-text">${monster.current_health} / ${monster.max_health} HP</div>
                </div>

                <div class="monster-stats">
                    <span>⚔️ ${monster.attack}</span>
                    <span>🛡️ ${monster.defense}</span>
                    <span>💀 ${monster.kills} Kills</span>
                </div>

                ${scarsHTML}

                <div class="monster-traits">
                    ${monster.personality_traits.map(t => `<span class="trait-badge">${t}</span>`).join('')}
                </div>

                ${monster.grudges.length > 0 ? `
                    <div class="grudges">
                        <strong>💢 Grudges:</strong>
                        <ul>
                            ${monster.grudges.slice(0, 2).map(g => `<li>${g}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                <div class="monster-actions">
                    <button class="btn-sm btn-info" onclick="window.arenaUI.viewMonsterDetails(${monster.id})">👁️ Details</button>
                    <button class="btn-sm btn-danger" onclick="window.arenaUI.challengeMonster(${monster.id})">⚔️ Herausfordern</button>
                </div>
            </div>
        `;
    }

    /**
     * Get icon for monster type
     */
    getTypeIcon(type) {
        const icons = {
            'Slime': '💧',
            'Bestie': '🐺',
            'Drache': '🐉',
            'Untot': '💀',
            'Dämon': '👿',
            'Elementar': '⚡',
            'Maschine': '🤖',
            'Pflanze': '🌿'
        };
        return icons[type] || '❓';
    }

    /**
     * Load challengers list
     */
    async loadChallengers() {
        const view = this.arenaPanel.querySelector('#challengers-view');
        view.innerHTML = '<div class="loading">⏳ Lade Herausforderer...</div>';

        try {
            const response = await this.apiClient.get('/api/game/arena/challengers');
            const challengers = response.data;

            let html = '<div class="challengers-list"><h3>Verfügbare Herausforderer</h3>';

            challengers.forEach(monster => {
                html += this.renderMonsterCard(monster, 'challenger');
            });

            html += '</div>';
            view.innerHTML = html;
        } catch (error) {
            console.error('Failed to load challengers:', error);
            view.innerHTML = '<div class="error">❌ Fehler beim Laden</div>';
        }
    }

    /**
     * Load player's personal nemeses
     */
    async loadMyNemesis() {
        const view = this.arenaPanel.querySelector('#nemesis-view');
        view.innerHTML = '<div class="loading">⏳ Lade deine Nemesis...</div>';

        try {
            const response = await this.apiClient.get('/api/game/arena/my-nemesis');
            const nemeses = response.data;

            if (nemeses.length === 0) {
                view.innerHTML = '<div class="info">ℹ️ Du hast noch keine Nemesis. Kämpfe um welche zu bekommen!</div>';
                return;
            }

            let html = '<div class="nemesis-list"><h3>💢 Deine Nemesis 💢</h3>';
            html += '<p>Diese Monster haben einen persönlichen Groll gegen dich...</p>';

            nemeses.forEach(monster => {
                html += this.renderNemesisCard(monster);
            });

            html += '</div>';
            view.innerHTML = html;
        } catch (error) {
            console.error('Failed to load nemesis:', error);
            view.innerHTML = '<div class="error">❌ Fehler beim Laden</div>';
        }
    }

    /**
     * Render nemesis card with extra grudge info
     */
    renderNemesisCard(monster) {
        return `
            <div class="nemesis-card">
                ${this.renderMonsterCard(monster, 'nemesis')}

                <div class="nemesis-history">
                    <h4>📜 Geschichte</h4>
                    <ul>
                        <li>Begegnungen: ${monster.encounters_with_player}</li>
                        <li>Deine Siege: ${monster.deaths}</li>
                        <li>Seine Siege: ${monster.kills}</li>
                    </ul>

                    ${monster.grudges.length > 0 ? `
                        <div class="grudge-speech">
                            <strong>"${monster.grudges[monster.grudges.length - 1]}"</strong>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    /**
     * Load regions map
     */
    async loadRegions() {
        const view = this.arenaPanel.querySelector('#regions-view');
        view.innerHTML = '<div class="loading">⏳ Lade Gebiete...</div>';

        try {
            const response = await this.apiClient.get('/api/game/arena/regions');
            const regions = response.data;

            let html = '<div class="regions-map"><h3>🗺️ Arena Gebiete 🗺️</h3>';

            Object.entries(regions).forEach(([regionName, controller]) => {
                html += this.renderRegionCard(regionName, controller);
            });

            html += '</div>';
            view.innerHTML = html;
        } catch (error) {
            console.error('Failed to load regions:', error);
            view.innerHTML = '<div class="error">❌ Fehler beim Laden</div>';
        }
    }

    /**
     * Render region card
     */
    renderRegionCard(regionName, controller) {
        return `
            <div class="region-card">
                <h4>🏰 ${regionName}</h4>
                ${controller ? `
                    <div class="region-controller">
                        <strong>Herrscher:</strong> ${controller.name}
                        <div class="controller-info">
                            Level ${controller.level} ${controller.monster_type}
                        </div>
                    </div>
                    <button class="btn-sm btn-danger" onclick="window.arenaUI.challengeRegion('${regionName}', ${controller.id})">
                        ⚔️ Gebiet erobern
                    </button>
                ` : `
                    <div class="region-empty">Kein Herrscher</div>
                    <button class="btn-sm btn-primary" onclick="window.arenaUI.claimRegion('${regionName}')">
                        🏰 Gebiet beanspruchen
                    </button>
                `}
            </div>
        `;
    }

    /**
     * Challenge a monster to battle
     */
    async challengeMonster(monsterId) {
        try {
            console.log(`⚔️ Challenging monster ${monsterId}...`);

            const response = await this.apiClient.post('/api/game/arena/challenge', {
                monster_id: monsterId
            });

            const result = response.data;

            // Show intro speech
            if (result.intro_speech) {
                this.showIntroSpeech(result.intro_speech, result.monster);
            }

            // Start battle
            // This would integrate with your existing combat system
            console.log('Battle started with:', result.monster);

            // Trigger battle event
            window.dispatchEvent(new CustomEvent('arena-battle-start', {
                detail: { monster: result.monster }
            }));

        } catch (error) {
            console.error('Failed to challenge monster:', error);
            alert('❌ Fehler beim Herausfordern des Monsters');
        }
    }

    /**
     * Show monster intro speech (Shadow of Mordor style)
     */
    showIntroSpeech(speech, monster) {
        const overlay = document.createElement('div');
        overlay.className = 'intro-speech-overlay';
        overlay.innerHTML = `
            <div class="intro-speech-box">
                <div class="monster-portrait">
                    <div class="monster-icon">${this.getTypeIcon(monster.monster_type)}</div>
                    <div class="monster-name">${monster.name}</div>
                    <div class="monster-title">${monster.title}</div>
                </div>

                <div class="speech-text">
                    ${speech.split('\n').map(line => `<p>${line}</p>`).join('')}
                </div>

                <button class="btn-danger" onclick="this.closest('.intro-speech-overlay').remove()">
                    ⚔️ KAMPF BEGINNEN!
                </button>
            </div>
        `;

        document.body.appendChild(overlay);

        // Remove after 10 seconds if not clicked
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
            }
        }, 10000);
    }

    /**
     * View detailed monster info
     */
    async viewMonsterDetails(monsterId) {
        try {
            const response = await this.apiClient.get(`/api/game/arena/monster/${monsterId}`);
            const monster = response.data;

            this.showMonsterDetailsModal(monster);
        } catch (error) {
            console.error('Failed to load monster details:', error);
        }
    }

    /**
     * Show monster details modal
     */
    showMonsterDetailsModal(monster) {
        const modal = document.createElement('div');
        modal.className = 'monster-details-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${monster.name} ${this.getTypeIcon(monster.monster_type)}</h2>
                    <button class="close-btn" onclick="this.closest('.monster-details-modal').remove()">✖</button>
                </div>

                <div class="modal-body">
                    <div class="detail-section">
                        <h3>📊 Stats</h3>
                        <ul>
                            <li>Rank: ${monster.rank}</li>
                            <li>Level: ${monster.level}</li>
                            <li>HP: ${monster.current_health} / ${monster.max_health}</li>
                            <li>Attack: ${monster.attack}</li>
                            <li>Defense: ${monster.defense}</li>
                        </ul>
                    </div>

                    <div class="detail-section">
                        <h3>🎭 Persönlichkeit</h3>
                        <div class="traits">
                            ${monster.personality_traits.map(t => `<span class="trait-badge">${t}</span>`).join('')}
                        </div>
                    </div>

                    <div class="detail-section">
                        <h3>⚔️ Spezialangriffe</h3>
                        <ul>
                            ${monster.special_moves.map(m => `<li>${m}</li>`).join('')}
                        </ul>
                    </div>

                    <div class="detail-section">
                        <h3>💪 Stärken & Schwächen</h3>
                        <div class="strengths">
                            <strong>Stärken:</strong> ${monster.strengths.join(', ') || 'Keine'}
                        </div>
                        <div class="weaknesses">
                            <strong>Schwächen:</strong> ${monster.weaknesses.join(', ') || 'Keine'}
                        </div>
                    </div>

                    ${monster.grudges.length > 0 ? `
                        <div class="detail-section">
                            <h3>💢 Grudges</h3>
                            <ul>
                                ${monster.grudges.map(g => `<li>"${g}"</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>

                <div class="modal-footer">
                    <button class="btn-danger" onclick="window.arenaUI.challengeMonster(${monster.id}); this.closest('.monster-details-modal').remove();">
                        ⚔️ Herausfordern
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    /**
     * Refresh current view
     */
    refreshCurrentView() {
        this.loadTabContent(this.currentTab);
    }

    /**
     * Show/hide arena panel
     */
    toggle() {
        if (this.arenaPanel) {
            this.arenaPanel.style.display =
                this.arenaPanel.style.display === 'none' ? 'block' : 'none';
        }
    }

    /**
     * Clean up
     */
    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        if (this.arenaPanel) {
            this.arenaPanel.remove();
        }
    }

    /**
     * Add arena styles to page
     */
    addArenaStyles() {
        if (document.getElementById('nemesis-arena-styles')) {
            return;
        }

        const style = document.createElement('style');
        style.id = 'nemesis-arena-styles';
        style.textContent = `
            .nemesis-arena-panel {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 90%;
                max-width: 1200px;
                max-height: 90vh;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 3px solid #e94560;
                border-radius: 15px;
                box-shadow: 0 10px 50px rgba(233, 69, 96, 0.5);
                z-index: 1000;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }

            .arena-header {
                background: linear-gradient(135deg, #e94560 0%, #c72c4d 100%);
                padding: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .arena-header h2 {
                margin: 0;
                color: white;
                font-size: 24px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }

            .close-btn {
                background: rgba(0,0,0,0.3);
                border: none;
                color: white;
                font-size: 20px;
                padding: 5px 10px;
                cursor: pointer;
                border-radius: 5px;
            }

            .arena-tabs {
                display: flex;
                background: #0f3460;
                padding: 0;
                border-bottom: 2px solid #e94560;
            }

            .arena-tab {
                flex: 1;
                padding: 15px;
                background: transparent;
                border: none;
                color: #ccc;
                cursor: pointer;
                transition: all 0.3s;
                border-bottom: 3px solid transparent;
            }

            .arena-tab:hover {
                background: rgba(233, 69, 96, 0.1);
                color: white;
            }

            .arena-tab.active {
                background: rgba(233, 69, 96, 0.2);
                color: white;
                border-bottom-color: #e94560;
            }

            .arena-content {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }

            .arena-view {
                display: none;
            }

            .arena-view.active {
                display: block;
            }

            .hierarchy-pyramid {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }

            .rank-tier {
                background: rgba(255,255,255,0.05);
                border-radius: 10px;
                padding: 20px;
                border-left: 5px solid;
            }

            .king-tier { border-left-color: #ffd700; }
            .lord-tier { border-left-color: #e94560; }
            .champion-tier { border-left-color: #ff6b9d; }
            .gladiator-tier { border-left-color: #4ecdc4; }

            .rank-tier h3 {
                margin: 0 0 15px 0;
                color: white;
                text-align: center;
            }

            .monster-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 15px;
            }

            .monster-card {
                background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
                border: 2px solid #e94560;
                border-radius: 10px;
                padding: 15px;
                transition: transform 0.3s, box-shadow 0.3s;
            }

            .monster-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(233, 69, 96, 0.5);
            }

            .king-card {
                border-color: #ffd700;
                box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
            }

            .lord-card { border-color: #e94560; }
            .champion-card { border-color: #ff6b9d; }
            .gladiator-card { border-color: #4ecdc4; }

            .monster-header {
                margin-bottom: 10px;
            }

            .monster-name {
                font-size: 18px;
                font-weight: bold;
                color: white;
            }

            .monster-title {
                font-size: 14px;
                color: #aaa;
                font-style: italic;
            }

            .monster-info {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                color: #ccc;
            }

            .monster-health {
                margin: 10px 0;
            }

            .health-bar {
                height: 8px;
                background: #333;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 5px;
            }

            .health-fill {
                height: 100%;
                background: linear-gradient(90deg, #e94560 0%, #ff6b9d 100%);
                transition: width 0.3s;
            }

            .health-text {
                font-size: 12px;
                color: #ccc;
                text-align: center;
            }

            .monster-stats {
                display: flex;
                justify-content: space-around;
                margin: 10px 0;
                padding: 10px 0;
                border-top: 1px solid rgba(255,255,255,0.1);
                border-bottom: 1px solid rgba(255,255,255,0.1);
                color: white;
            }

            .monster-traits {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin: 10px 0;
            }

            .trait-badge {
                background: rgba(233, 69, 96, 0.3);
                color: white;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 11px;
            }

            .scars {
                background: rgba(255, 0, 0, 0.2);
                padding: 8px;
                border-radius: 5px;
                margin: 10px 0;
                color: #ffaaaa;
                font-size: 12px;
            }

            .grudges {
                background: rgba(255, 69, 0, 0.2);
                padding: 8px;
                border-radius: 5px;
                margin: 10px 0;
                color: #ffccaa;
                font-size: 12px;
            }

            .grudges ul {
                margin: 5px 0 0 20px;
                padding: 0;
            }

            .monster-actions {
                display: flex;
                gap: 5px;
                margin-top: 10px;
            }

            .btn-sm {
                flex: 1;
                padding: 8px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.3s;
            }

            .btn-info {
                background: #4ecdc4;
                color: white;
            }

            .btn-danger {
                background: #e94560;
                color: white;
            }

            .btn-primary {
                background: #0f3460;
                color: white;
            }

            .btn-sm:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }

            .arena-footer {
                background: #0f3460;
                padding: 15px 20px;
                display: flex;
                gap: 10px;
                border-top: 2px solid #e94560;
            }

            .arena-footer button {
                flex: 1;
                padding: 12px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.3s;
            }

            .loading, .error, .info {
                text-align: center;
                padding: 40px;
                font-size: 18px;
                color: white;
            }

            .empty-throne {
                text-align: center;
                padding: 40px;
                font-size: 20px;
                color: #888;
                font-style: italic;
            }

            .intro-speech-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.9);
                z-index: 2000;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .intro-speech-box {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 5px solid #e94560;
                border-radius: 15px;
                padding: 40px;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 0 50px rgba(233, 69, 96, 0.8);
            }

            .monster-portrait {
                margin-bottom: 30px;
            }

            .monster-icon {
                font-size: 80px;
                margin-bottom: 10px;
            }

            .speech-text {
                color: white;
                font-size: 18px;
                line-height: 1.6;
                margin: 20px 0;
            }

            .speech-text p {
                margin: 10px 0;
            }
        `;

        document.head.appendChild(style);
    }
}

// Make globally available
window.NemesisArenaUI = NemesisArenaUI;
