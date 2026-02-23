/**
 * Gildenhaus UI - Konosuba Style Adventurer's Guild
 * ==================================================
 *
 * Features:
 * - Quest Board (Available, Active, Completed)
 * - Party System (Create, Join, Manage)
 * - Reward Collection
 * - Guild Rank & Reputation
 * - NPC Interactions (Quest Giver, Receptionist)
 *
 * Style: Konosuba Adventurer's Guild
 */

(function() {
    'use strict';

    const API_BASE = window.API_BASE_URL || 'http://localhost:8000';

    // ==================== STATE ====================

    // Load persisted guild data from localStorage
    const saved = (() => {
        try {
            return JSON.parse(localStorage.getItem('najika_guild_state') || '{}');
        } catch { return {}; }
    })();

    const GuildState = {
        playerRank: saved.playerRank || 'Anfänger',
        reputation: saved.reputation || 0,
        completedQuests: saved.completedQuests || 0,
        completedQuestIds: saved.completedQuestIds || [],
        activeQuests: saved.activeQuests || [],
        availableQuests: [],
        party: null,
        isOpen: false
    };

    function saveGuildState() {
        try {
            localStorage.setItem('najika_guild_state', JSON.stringify({
                playerRank: GuildState.playerRank,
                reputation: GuildState.reputation,
                completedQuests: GuildState.completedQuests,
                completedQuestIds: GuildState.completedQuestIds,
                activeQuests: GuildState.activeQuests
            }));
        } catch {}
    }

    // ==================== GUILD RANKS ====================

    const GUILD_RANKS = [
        { name: 'Anfänger', minRep: 0, color: '#8b4513' },
        { name: 'Neuling', minRep: 100, color: '#696969' },
        { name: 'Abenteurer', minRep: 500, color: '#4682b4' },
        { name: 'Veteran', minRep: 1500, color: '#9370db' },
        { name: 'Elite', minRep: 3000, color: '#ffa500' },
        { name: 'Meister', minRep: 5000, color: '#ffd700' },
        { name: 'Legende', minRep: 10000, color: '#ff1493' }
    ];

    // ==================== QUEST TYPES ====================

    const QUEST_TYPES = {
        MONSTER_HUNT: { icon: '🗡️', color: '#dc143c' },
        GATHERING: { icon: '🌿', color: '#228b22' },
        ESCORT: { icon: '👥', color: '#4169e1' },
        DELIVERY: { icon: '📦', color: '#daa520' },
        INVESTIGATION: { icon: '🔍', color: '#9370db' },
        BOSS_RAID: { icon: '💀', color: '#8b0000' }
    };

    // ==================== MOCK DATA ====================

    const MOCK_QUESTS = [
        {
            id: 'quest_1',
            title: 'Kröten-Invasion!',
            description: 'Töte 10 Riesenkröten die die Felder bedrohen.',
            type: 'MONSTER_HUNT',
            rank: 'Anfänger',
            reward: { gold: 150, xp: 100, rep: 10 },
            objectives: [
                { text: 'Töte 10 Riesenkröten', progress: 0, max: 10 }
            ],
            timeLimit: null,
            location: 'Götterfels Felder'
        },
        {
            id: 'quest_2',
            title: 'Kräuter sammeln',
            description: 'Sammle 20 Heilkräuter für die Alchemistin.',
            type: 'GATHERING',
            rank: 'Anfänger',
            reward: { gold: 100, xp: 50, rep: 5 },
            objectives: [
                { text: 'Sammle Heilkräuter', progress: 0, max: 20 }
            ],
            timeLimit: null,
            location: 'Samtmoos-Tiefwald'
        },
        {
            id: 'quest_3',
            title: 'Händler-Eskorte',
            description: 'Eskortiere Händler sicher zur nächsten Stadt.',
            type: 'ESCORT',
            rank: 'Neuling',
            reward: { gold: 300, xp: 200, rep: 20 },
            objectives: [
                { text: 'Bringe Händler sicher ans Ziel', progress: 0, max: 1 }
            ],
            timeLimit: 3600,  // 1 hour
            location: 'Götterfels → Kristall-Stadt'
        },
        {
            id: 'quest_4',
            title: 'Drachen-Bestie!',
            description: 'BOSS-RAID: Töte den Terror-Drachen!',
            type: 'BOSS_RAID',
            rank: 'Elite',
            reward: { gold: 5000, xp: 2000, rep: 200 },
            objectives: [
                { text: 'Besiege Terror-Drachen', progress: 0, max: 1 }
            ],
            timeLimit: null,
            location: 'Magmaströme Gipfel',
            partyRequired: true,
            minPartySize: 3
        }
    ];

    // ==================== UI CREATION ====================

    function createGildenhausUI() {
        const container = document.createElement('div');
        container.id = 'gildenhaus-ui';
        container.className = 'gildenhaus-ui hidden';
        container.innerHTML = `
            <div class="gildenhaus-overlay"></div>
            <div class="gildenhaus-content">
                <!-- Header -->
                <div class="gildenhaus-header">
                    <h2>🏰 Abenteurer-Gilde</h2>
                    <button class="gildenhaus-close" title="Schließen (G)">&times;</button>
                </div>

                <!-- Player Info -->
                <div class="gildenhaus-player-info">
                    <div class="player-rank">
                        <span class="rank-label">Rang:</span>
                        <span class="rank-value">${GuildState.playerRank}</span>
                    </div>
                    <div class="player-reputation">
                        <span class="rep-label">Ruf:</span>
                        <span class="rep-value">${GuildState.reputation}</span>
                        <div class="rep-bar">
                            <div class="rep-fill" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="player-stats">
                        <span>✅ Quests: ${GuildState.completedQuests}</span>
                        <span>📋 Aktiv: ${GuildState.activeQuests.length}</span>
                    </div>
                </div>

                <!-- Tabs -->
                <div class="gildenhaus-tabs">
                    <button class="tab-btn active" data-tab="quests">📋 Quests</button>
                    <button class="tab-btn" data-tab="party">👥 Gruppe</button>
                    <button class="tab-btn" data-tab="rewards">🎁 Belohnungen</button>
                    <button class="tab-btn" data-tab="ranks">⭐ Ränge</button>
                </div>

                <!-- Content Areas -->
                <div class="gildenhaus-body">
                    <!-- Quests Tab -->
                    <div class="tab-content active" data-tab="quests">
                        <div class="quest-filters">
                            <button class="filter-btn active" data-filter="available">Verfügbar</button>
                            <button class="filter-btn" data-filter="active">Aktiv</button>
                            <button class="filter-btn" data-filter="completed">Abgeschlossen</button>
                        </div>
                        <div class="quest-list"></div>
                    </div>

                    <!-- Party Tab -->
                    <div class="tab-content" data-tab="party">
                        <div class="party-section">
                            <h3>Deine Gruppe</h3>
                            <div class="party-info">
                                <p class="no-party">Du bist in keiner Gruppe!</p>
                            </div>
                            <div class="party-actions">
                                <button class="btn-create-party">Gruppe erstellen</button>
                                <button class="btn-find-party">Gruppe suchen</button>
                            </div>
                        </div>
                    </div>

                    <!-- Rewards Tab -->
                    <div class="tab-content" data-tab="rewards">
                        <div class="rewards-section">
                            <h3>Ausstehende Belohnungen</h3>
                            <div class="rewards-list">
                                <p class="no-rewards">Keine Belohnungen verfügbar!</p>
                            </div>
                        </div>
                    </div>

                    <!-- Ranks Tab -->
                    <div class="tab-content" data-tab="ranks">
                        <div class="ranks-section">
                            <h3>Gilden-Ränge</h3>
                            <div class="ranks-list"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(container);

        // Add CSS
        addGildenhausStyles();

        // Setup event listeners
        setupEventListeners(container);

        // Initialize
        updateQuestList('available');
        updateRanksList();

        return container;
    }

    // ==================== EVENT LISTENERS ====================

    function setupEventListeners(container) {
        // Close button
        container.querySelector('.gildenhaus-close').addEventListener('click', closeGildenhaus);
        container.querySelector('.gildenhaus-overlay').addEventListener('click', closeGildenhaus);

        // Tab switching
        container.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => switchTab(btn.dataset.tab));
        });

        // Quest filters
        container.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                updateQuestList(btn.dataset.filter);
            });
        });

        // Party actions
        container.querySelector('.btn-create-party').addEventListener('click', createParty);
        container.querySelector('.btn-find-party').addEventListener('click', findParty);
    }

    // ==================== QUEST SYSTEM ====================

    function updateQuestList(filter) {
        const questList = document.querySelector('.quest-list');
        if (!questList) return;

        let quests = [];
        if (filter === 'available') {
            quests = MOCK_QUESTS.filter(q => !GuildState.activeQuests.includes(q.id));
        } else if (filter === 'active') {
            quests = MOCK_QUESTS.filter(q => GuildState.activeQuests.includes(q.id));
        } else if (filter === 'completed') {
            quests = MOCK_QUESTS.filter(q => GuildState.completedQuestIds.includes(q.id));
        }

        if (quests.length === 0) {
            questList.innerHTML = '<p class="no-quests">Keine Quests verfügbar!</p>';
            return;
        }

        questList.innerHTML = quests.map(quest => `
            <div class="quest-card" data-quest-id="${quest.id}">
                <div class="quest-header">
                    <span class="quest-icon">${QUEST_TYPES[quest.type].icon}</span>
                    <div class="quest-title-section">
                        <h4 class="quest-title">${quest.title}</h4>
                        <span class="quest-rank" style="color: ${getRankColor(quest.rank)}">${quest.rank}</span>
                    </div>
                </div>
                <p class="quest-description">${quest.description}</p>
                <div class="quest-objectives">
                    ${quest.objectives.map(obj => `
                        <div class="objective">
                            <span>${obj.text}</span>
                            <span class="objective-progress">${obj.progress}/${obj.max}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="quest-footer">
                    <div class="quest-rewards">
                        <span title="Gold">💰 ${quest.reward.gold}G</span>
                        <span title="Erfahrung">⭐ ${quest.reward.xp} XP</span>
                        <span title="Ruf">📈 ${quest.reward.rep} Ruf</span>
                    </div>
                    <div class="quest-actions">
                        ${filter === 'available' ?
                            `<button class="btn-accept-quest" data-quest-id="${quest.id}">Annehmen</button>` :
                            `<button class="btn-abandon-quest" data-quest-id="${quest.id}">Abbrechen</button>`
                        }
                    </div>
                </div>
                ${quest.partyRequired ? `
                    <div class="quest-party-required">
                        ⚠️ Gruppe erforderlich (Min. ${quest.minPartySize} Spieler)
                    </div>
                ` : ''}
            </div>
        `).join('');

        // Add event listeners to quest buttons
        questList.querySelectorAll('.btn-accept-quest').forEach(btn => {
            btn.addEventListener('click', () => acceptQuest(btn.dataset.questId));
        });

        questList.querySelectorAll('.btn-abandon-quest').forEach(btn => {
            btn.addEventListener('click', () => abandonQuest(btn.dataset.questId));
        });
    }

    function acceptQuest(questId) {
        const quest = MOCK_QUESTS.find(q => q.id === questId);
        if (!quest) return;

        // Check if party required
        if (quest.partyRequired && !GuildState.party) {
            showNotification('❌ Diese Quest erfordert eine Gruppe!', 'error');
            return;
        }

        // Check rank
        if (!isRankSufficient(GuildState.playerRank, quest.rank)) {
            showNotification(`❌ Du benötigst Rang ${quest.rank}!`, 'error');
            return;
        }

        // Accept quest
        GuildState.activeQuests.push(questId);
        showNotification(`✅ Quest angenommen: ${quest.title}`, 'success');
        updateQuestList('available');

        saveGuildState();
        if (window.GameEvents) {
            window.GameEvents.emit('questAccepted', { questId, factionId: quest.faction || null, title: quest.title });
        }
    }

    function abandonQuest(questId) {
        const quest = MOCK_QUESTS.find(q => q.id === questId);
        if (!quest) return;

        const index = GuildState.activeQuests.indexOf(questId);
        if (index > -1) {
            GuildState.activeQuests.splice(index, 1);
            showNotification(`Quest abgebrochen: ${quest.title}`, 'warning');
            updateQuestList('active');
            saveGuildState();
            if (window.GameEvents) {
                window.GameEvents.emit('questAbandoned', { questId, title: quest.title });
            }
        }
    }

    // ==================== PARTY SYSTEM ====================

    function createParty() {
        showNotification('🎉 Gruppe erstellt! Warte auf Mitglieder...', 'success');
        GuildState.party = {
            id: 'party_' + Date.now(),
            leader: 'Player',
            members: ['Player'],
            maxSize: 4
        };
        updatePartyUI();
    }

    function findParty() {
        showNotification('🔍 Suche nach verfügbaren Gruppen...', 'info');
        // TODO: Implement party finder
    }

    function updatePartyUI() {
        const partyInfo = document.querySelector('.party-info');
        if (!partyInfo) return;

        if (!GuildState.party) {
            partyInfo.innerHTML = '<p class="no-party">Du bist in keiner Gruppe!</p>';
            return;
        }

        partyInfo.innerHTML = `
            <div class="party-details">
                <div class="party-header">
                    <h4>Gruppe: ${GuildState.party.id}</h4>
                    <span class="party-size">${GuildState.party.members.length}/${GuildState.party.maxSize}</span>
                </div>
                <div class="party-members">
                    ${GuildState.party.members.map((member, i) => `
                        <div class="party-member">
                            <span class="member-name">${member}</span>
                            ${i === 0 ? '<span class="leader-badge">👑 Anführer</span>' : ''}
                        </div>
                    `).join('')}
                </div>
                <button class="btn-leave-party">Gruppe verlassen</button>
            </div>
        `;

        // Add leave button listener
        partyInfo.querySelector('.btn-leave-party')?.addEventListener('click', () => {
            GuildState.party = null;
            updatePartyUI();
            showNotification('Du hast die Gruppe verlassen.', 'info');
        });
    }

    // ==================== RANKS SYSTEM ====================

    function updateRanksList() {
        const ranksList = document.querySelector('.ranks-list');
        if (!ranksList) return;

        ranksList.innerHTML = GUILD_RANKS.map(rank => {
            const isUnlocked = GuildState.reputation >= rank.minRep;
            const isCurrent = rank.name === GuildState.playerRank;

            return `
                <div class="rank-card ${isUnlocked ? 'unlocked' : 'locked'} ${isCurrent ? 'current' : ''}">
                    <div class="rank-icon" style="background: ${rank.color}">
                        ${isUnlocked ? '⭐' : '🔒'}
                    </div>
                    <div class="rank-info">
                        <h4 style="color: ${rank.color}">${rank.name}</h4>
                        <p>Benötigt: ${rank.minRep} Ruf</p>
                        ${isCurrent ? '<span class="current-badge">✅ Dein Rang</span>' : ''}
                    </div>
                </div>
            `;
        }).join('');
    }

    function updatePlayerRank() {
        const rank = GUILD_RANKS
            .filter(r => GuildState.reputation >= r.minRep)
            .pop();

        if (rank && rank.name !== GuildState.playerRank) {
            const oldRank = GuildState.playerRank;
            GuildState.playerRank = rank.name;
            showNotification(`🎊 Rang aufgestiegen: ${oldRank} → ${rank.name}!`, 'success');
            updateRanksList();
        }
    }

    // ==================== HELPERS ====================

    function switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.dataset.tab === tabName);
        });

        // Update party UI when switching to party tab
        if (tabName === 'party') {
            updatePartyUI();
        }
    }

    function getRankColor(rankName) {
        const rank = GUILD_RANKS.find(r => r.name === rankName);
        return rank ? rank.color : '#8b4513';
    }

    function isRankSufficient(playerRank, requiredRank) {
        const playerRankIndex = GUILD_RANKS.findIndex(r => r.name === playerRank);
        const requiredRankIndex = GUILD_RANKS.findIndex(r => r.name === requiredRank);
        return playerRankIndex >= requiredRankIndex;
    }

    function showNotification(message, type = 'info') {
        if (typeof notify === 'function') {
            notify(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }

    // ==================== OPEN/CLOSE ====================

    function openGildenhaus() {
        const ui = document.getElementById('gildenhaus-ui');
        if (ui) {
            ui.classList.remove('hidden');
            GuildState.isOpen = true;
        } else {
            createGildenhausUI();
            GuildState.isOpen = true;
        }
    }

    function closeGildenhaus() {
        const ui = document.getElementById('gildenhaus-ui');
        if (ui) {
            ui.classList.add('hidden');
            GuildState.isOpen = false;
        }
    }

    function toggleGildenhaus() {
        if (GuildState.isOpen) {
            closeGildenhaus();
        } else {
            openGildenhaus();
        }
    }

    // ==================== STYLES ====================

    function addGildenhausStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .gildenhaus-ui {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10000;
                font-family: 'Arial', sans-serif;
            }

            .gildenhaus-ui.hidden {
                display: none;
            }

            .gildenhaus-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
            }

            .gildenhaus-content {
                position: relative;
                width: 90%;
                max-width: 1200px;
                height: 80%;
                max-height: 800px;
                margin: 5% auto;
                background: linear-gradient(135deg, #2c1810 0%, #1a0f0a 100%);
                border: 3px solid #d4af37;
                border-radius: 15px;
                box-shadow: 0 0 30px rgba(212, 175, 55, 0.5);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .gildenhaus-header {
                background: linear-gradient(90deg, #8b4513 0%, #654321 100%);
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #d4af37;
            }

            .gildenhaus-header h2 {
                margin: 0;
                color: #ffd700;
                font-size: 24px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            }

            .gildenhaus-close {
                background: #8b0000;
                border: none;
                color: white;
                font-size: 32px;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s;
            }

            .gildenhaus-close:hover {
                background: #ff0000;
                transform: rotate(90deg);
            }

            .gildenhaus-player-info {
                background: rgba(0, 0, 0, 0.3);
                padding: 15px;
                display: flex;
                gap: 20px;
                border-bottom: 1px solid #d4af37;
            }

            .player-rank, .player-reputation {
                display: flex;
                align-items: center;
                gap: 10px;
                color: white;
            }

            .rank-value {
                color: #ffd700;
                font-weight: bold;
                font-size: 18px;
            }

            .rep-bar {
                width: 200px;
                height: 10px;
                background: #333;
                border-radius: 5px;
                overflow: hidden;
            }

            .rep-fill {
                height: 100%;
                background: linear-gradient(90deg, #ffd700, #ff8c00);
                transition: width 0.3s;
            }

            .player-stats {
                margin-left: auto;
                display: flex;
                gap: 15px;
                color: white;
            }

            .gildenhaus-tabs {
                display: flex;
                background: rgba(0, 0, 0, 0.3);
                border-bottom: 2px solid #d4af37;
            }

            .tab-btn {
                flex: 1;
                padding: 15px;
                background: transparent;
                border: none;
                color: #ccc;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s;
                border-right: 1px solid #d4af37;
            }

            .tab-btn:last-child {
                border-right: none;
            }

            .tab-btn.active {
                background: rgba(212, 175, 55, 0.2);
                color: #ffd700;
                font-weight: bold;
            }

            .tab-btn:hover:not(.active) {
                background: rgba(212, 175, 55, 0.1);
                color: white;
            }

            .gildenhaus-body {
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

            .quest-filters {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }

            .filter-btn {
                padding: 10px 20px;
                background: #654321;
                border: 2px solid #d4af37;
                color: white;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .filter-btn.active {
                background: #d4af37;
                color: #1a0f0a;
            }

            .quest-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 20px;
            }

            .quest-card {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #d4af37;
                border-radius: 10px;
                padding: 15px;
                transition: all 0.3s;
            }

            .quest-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
            }

            .quest-header {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 10px;
            }

            .quest-icon {
                font-size: 32px;
            }

            .quest-title {
                margin: 0;
                color: #ffd700;
                font-size: 18px;
            }

            .quest-rank {
                font-size: 12px;
                font-weight: bold;
            }

            .quest-description {
                color: #ccc;
                margin: 10px 0;
                font-size: 14px;
            }

            .quest-objectives {
                margin: 10px 0;
            }

            .objective {
                display: flex;
                justify-content: space-between;
                color: white;
                padding: 5px 0;
                font-size: 14px;
            }

            .objective-progress {
                color: #ffd700;
            }

            .quest-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #d4af37;
            }

            .quest-rewards {
                display: flex;
                gap: 15px;
                color: white;
                font-size: 14px;
            }

            .btn-accept-quest, .btn-abandon-quest {
                padding: 8px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }

            .btn-accept-quest {
                background: #228b22;
                color: white;
            }

            .btn-accept-quest:hover {
                background: #32cd32;
            }

            .btn-abandon-quest {
                background: #8b0000;
                color: white;
            }

            .btn-abandon-quest:hover {
                background: #ff0000;
            }

            .quest-party-required {
                margin-top: 10px;
                padding: 10px;
                background: rgba(255, 165, 0, 0.2);
                border: 1px solid #ffa500;
                border-radius: 5px;
                color: #ffa500;
                font-size: 12px;
                text-align: center;
            }

            .no-quests, .no-party, .no-rewards {
                text-align: center;
                color: #999;
                padding: 40px;
                font-size: 18px;
            }

            .party-section, .rewards-section, .ranks-section {
                color: white;
            }

            .party-section h3, .rewards-section h3, .ranks-section h3 {
                color: #ffd700;
                margin-bottom: 20px;
            }

            .party-actions {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }

            .btn-create-party, .btn-find-party, .btn-leave-party {
                padding: 12px 24px;
                background: #4169e1;
                border: 2px solid #d4af37;
                color: white;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }

            .btn-create-party:hover, .btn-find-party:hover {
                background: #5a7fc4;
            }

            .btn-leave-party {
                background: #8b0000;
            }

            .btn-leave-party:hover {
                background: #ff0000;
            }

            .ranks-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 15px;
            }

            .rank-card {
                display: flex;
                align-items: center;
                gap: 15px;
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid #666;
                border-radius: 10px;
                transition: all 0.3s;
            }

            .rank-card.unlocked {
                border-color: #d4af37;
            }

            .rank-card.current {
                background: rgba(212, 175, 55, 0.2);
                border-color: #ffd700;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
            }

            .rank-icon {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            }

            .rank-info h4 {
                margin: 0 0 5px 0;
                font-size: 18px;
            }

            .rank-info p {
                margin: 0;
                color: #999;
                font-size: 14px;
            }

            .current-badge {
                display: inline-block;
                background: #228b22;
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 12px;
                margin-top: 5px;
            }
        `;
        document.head.appendChild(style);
    }

    // ==================== KEYBOARD SHORTCUT ====================

    document.addEventListener('keydown', (e) => {
        if (e.key === 'g' || e.key === 'G') {
            // Don't open if typing in input field
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            toggleGildenhaus();
        }
    });

    // ==================== PUBLIC API ====================

    window.GildenhausUI = {
        open: openGildenhaus,
        close: closeGildenhaus,
        toggle: toggleGildenhaus,
        getState: () => GuildState,
        addReputation: (amount) => {
            GuildState.reputation += amount;
            updatePlayerRank();
        },
        completeQuest: (questId) => {
            const quest = MOCK_QUESTS.find(q => q.id === questId);
            if (!quest) return;
            if (GuildState.completedQuestIds.includes(questId)) return;

            // Remove from active
            const idx = GuildState.activeQuests.indexOf(questId);
            if (idx > -1) GuildState.activeQuests.splice(idx, 1);

            // Add to completed
            GuildState.completedQuestIds.push(questId);
            GuildState.completedQuests++;
            GuildState.reputation += quest.reward.rep;
            updatePlayerRank();

            // Give rewards
            if (window.player && quest.reward.gold) {
                window.player.gold += quest.reward.gold;
            }
            if (window.addPlayerXP && quest.reward.xp) {
                window.addPlayerXP(quest.reward.xp, 'guild_quest');
            }

            showNotification(`✅ Quest abgeschlossen: ${quest.title} (+${quest.reward.gold}G, +${quest.reward.xp}XP)`, 'success');
            saveGuildState();

            if (window.GameEvents) {
                window.GameEvents.emit('questCompleted', {
                    questId,
                    title: quest.title,
                    reward: quest.reward
                });
            }
        }
    };

})();
