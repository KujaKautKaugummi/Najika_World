/**
 * NAJIKA QUEST UI SYSTEM
 * ======================
 * Skyrim-Style Quest Log + Tracker
 *
 * Features:
 * - Quest Log Panel (Q-Taste)
 * - Quest Tracker (rechts oben auf Screen)
 * - Quest Details mit Objectives
 * - Start/Complete Quest Funktionen
 * - Najika-Reaktionen
 */

class QuestUI {
    constructor() {
        this.API_BASE = window.BACKEND_URL || 'http://127.0.0.1:8000';

        // Quest Data
        this.activeQuests = [];
        this.availableQuests = [];
        this.stats = { total_quests: 0, active: 0, completed: 0 };

        // UI Elements
        this.questLogPanel = null;
        this.questTracker = null;
        this.selectedQuestId = null;

        // State
        this.isLogOpen = false;
        this.trackedQuestIds = [];  // Max 3 tracked quests

        // Init
        this.createUI();
        this.setupEventListeners();
        this.loadQuests();

        console.log('[QUEST UI] ✅ Initialisiert');
    }

    /**
     * QUEST LOG PANEL erstellen
     */
    createUI() {
        // Quest Log Panel (F overlay)
        this.questLogPanel = document.createElement('div');
        this.questLogPanel.id = 'quest-log-panel';
        this.questLogPanel.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
            z-index: 10000;
            display: none;
            overflow: auto;
        `;
        document.body.appendChild(this.questLogPanel);

        // Quest Tracker (rechts oben)
        this.questTracker = document.createElement('div');
        this.questTracker.id = 'quest-tracker';
        this.questTracker.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            width: 320px;
            max-height: 400px;
            background: rgba(0, 0, 0, 0.85);
            border: 2px solid #4CAF50;
            border-radius: 12px;
            padding: 15px;
            z-index: 500;
            overflow-y: auto;
            font-family: 'Segoe UI', Arial, sans-serif;
        `;
        document.body.appendChild(this.questTracker);

        console.log('[QUEST UI] UI Elemente erstellt');
    }

    /**
     * EVENT LISTENERS
     */
    setupEventListeners() {
        // Q-Taste: Toggle Quest Log
        document.addEventListener('keydown', (e) => {
            if (e.key === 'q' || e.key === 'Q') {
                // Check ob Chat offen ist
                const chatUI = document.getElementById('chat-ui');
                if (chatUI && chatUI.style.display !== 'none') {
                    return;  // Chat hat Vorrang
                }

                this.toggleQuestLog();
            }

            // ESC: Close Quest Log
            if (e.key === 'Escape' && this.isLogOpen) {
                this.closeQuestLog();
            }
        });
    }

    /**
     * QUEST DATEN LADEN
     */
    async loadQuests() {
        try {
            // Parallel laden: Stats, Active, Available
            const [statsRes, activeRes, availableRes] = await Promise.all([
                fetch(`${this.API_BASE}/api/quests/stats`),
                fetch(`${this.API_BASE}/api/quests/active`),
                fetch(`${this.API_BASE}/api/quests/available?level=1`)
            ]);

            if (!statsRes.ok || !activeRes.ok || !availableRes.ok) {
                console.warn('[QUEST UI] ⚠️ Quest System nicht verfügbar');
                return;
            }

            this.stats = await statsRes.json();
            const activeData = await activeRes.json();
            const availableData = await availableRes.json();

            this.activeQuests = activeData.quests || [];
            this.availableQuests = availableData.quests || [];

            // Auto-Track erste 3 aktive Quests
            this.trackedQuestIds = this.activeQuests.slice(0, 3).map(q => q.id);

            this.updateQuestTracker();

            console.log(`[QUEST UI] ✅ ${this.activeQuests.length} aktive, ${this.availableQuests.length} verfügbare Quests`);
        } catch (error) {
            console.error('[QUEST UI] ❌ Fehler beim Laden:', error);
        }
    }

    /**
     * QUEST LOG PANEL öffnen/schließen
     */
    toggleQuestLog() {
        if (this.isLogOpen) {
            this.closeQuestLog();
        } else {
            this.openQuestLog();
        }
    }

    openQuestLog() {
        this.isLogOpen = true;
        this.questLogPanel.style.display = 'block';
        this.renderQuestLog();
    }

    closeQuestLog() {
        this.isLogOpen = false;
        this.questLogPanel.style.display = 'none';
    }

    /**
     * QUEST LOG PANEL rendern
     */
    renderQuestLog() {
        const html = `
            <div style="max-width: 1200px; margin: 50px auto; padding: 30px;">
                <!-- Header -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                    <h1 style="color: #4CAF50; font-size: 36px; margin: 0;">
                        📜 Quest Log
                    </h1>
                    <button onclick="window.questUI.closeQuestLog()" style="
                        background: #f44336;
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 8px;
                        font-size: 16px;
                        cursor: pointer;
                        font-weight: bold;
                    ">✕ Close (ESC)</button>
                </div>

                <!-- Stats -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px;">
                    ${this.renderStatCard('📊 Total', this.stats.total_quests, '#2196F3')}
                    ${this.renderStatCard('🔥 Active', this.stats.active, '#FF9800')}
                    ${this.renderStatCard('✅ Completed', this.stats.completed, '#4CAF50')}
                    ${this.renderStatCard('📈 Rate', Math.round(this.stats.completion_rate || 0) + '%', '#9C27B0')}
                </div>

                <!-- Tabs -->
                <div style="display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #333;">
                    <button onclick="window.questUI.switchTab('active')"
                            id="tab-active"
                            class="quest-tab quest-tab-active"
                            style="padding: 12px 24px; background: #4CAF50; color: white; border: none; border-radius: 8px 8px 0 0; cursor: pointer; font-size: 16px; font-weight: bold;">
                        🔥 Active (${this.activeQuests.length})
                    </button>
                    <button onclick="window.questUI.switchTab('available')"
                            id="tab-available"
                            class="quest-tab"
                            style="padding: 12px 24px; background: #333; color: white; border: none; border-radius: 8px 8px 0 0; cursor: pointer; font-size: 16px;">
                        📋 Available (${this.availableQuests.length})
                    </button>
                </div>

                <!-- Quest List -->
                <div id="quest-list-container">
                    ${this.renderQuestList(this.activeQuests, 'active')}
                </div>
            </div>
        `;

        this.questLogPanel.innerHTML = html;
    }

    renderStatCard(label, value, color) {
        return `
            <div style="
                background: ${color};
                color: white;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            ">
                <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">${label}</div>
                <div style="font-size: 32px; font-weight: bold;">${value}</div>
            </div>
        `;
    }

    renderQuestList(quests, type) {
        if (quests.length === 0) {
            return `
                <div style="text-align: center; padding: 60px; color: #666;">
                    <div style="font-size: 48px; margin-bottom: 20px;">📭</div>
                    <div style="font-size: 20px;">No ${type} quests</div>
                </div>
            `;
        }

        return quests.map(quest => this.renderQuestCard(quest, type)).join('');
    }

    renderQuestCard(quest, type) {
        const typeColors = {
            'main_quest': '#FF4444',
            'side_quest': '#4CAF50',
            'legendary_quest': '#FFD700',
            'story_quest': '#9C27B0',
            'exploration_quest': '#2196F3'
        };

        const typeLabels = {
            'main_quest': '🔥 Main Quest',
            'side_quest': '📋 Side Quest',
            'legendary_quest': '⭐ Legendary',
            'story_quest': '📖 Story',
            'exploration_quest': '🗺️ Exploration'
        };

        const color = typeColors[quest.type] || '#666';
        const typeLabel = typeLabels[quest.type] || quest.type;

        // Progress berechnen
        let progressHTML = '';
        if (type === 'active' && quest.objectives) {
            const progress = quest.progress || {};
            const completed = Object.values(progress).filter(v => v === true).length;
            const total = quest.objectives.length;
            const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

            progressHTML = `
                <div style="margin-top: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #aaa; font-size: 14px;">Progress</span>
                        <span style="color: #4CAF50; font-weight: bold;">${completed}/${total} (${percent}%)</span>
                    </div>
                    <div style="background: #222; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: #4CAF50; height: 100%; width: ${percent}%; transition: width 0.3s;"></div>
                    </div>
                </div>
            `;
        }

        // Objectives
        let objectivesHTML = '';
        if (quest.objectives && quest.objectives.length > 0) {
            const progress = quest.progress || {};
            objectivesHTML = `
                <div style="margin-top: 15px; border-top: 1px solid #333; padding-top: 15px;">
                    <div style="color: #aaa; font-size: 14px; margin-bottom: 10px;">Objectives:</div>
                    ${quest.objectives.map((obj, idx) => {
                        const isDone = progress[idx] === true;
                        return `
                            <div style="
                                display: flex;
                                align-items: center;
                                gap: 10px;
                                padding: 8px;
                                background: ${isDone ? 'rgba(76, 175, 80, 0.1)' : 'rgba(255,255,255,0.05)'};
                                border-radius: 6px;
                                margin-bottom: 8px;
                                ${isDone ? 'opacity: 0.6; text-decoration: line-through;' : ''}
                            ">
                                <span style="font-size: 18px;">${isDone ? '✅' : '⬜'}</span>
                                <span style="color: ${isDone ? '#4CAF50' : 'white'}; flex: 1;">${obj.description}</span>
                                ${obj.target_amount > 1 ? `<span style="color: #aaa;">(0/${obj.target_amount})</span>` : ''}
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        }

        // Actions
        let actionsHTML = '';
        if (type === 'available') {
            actionsHTML = `
                <button onclick="window.questUI.startQuest('${quest.id}')" style="
                    width: 100%;
                    margin-top: 15px;
                    padding: 12px;
                    background: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                ">▶️ Start Quest</button>
            `;
        } else if (type === 'active') {
            const isTracked = this.trackedQuestIds.includes(quest.id);
            actionsHTML = `
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button onclick="window.questUI.toggleTrackQuest('${quest.id}')" style="
                        flex: 1;
                        padding: 12px;
                        background: ${isTracked ? '#FF9800' : '#333'};
                        color: white;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">${isTracked ? '📌 Tracked' : '📍 Track'}</button>
                    <button onclick="window.questUI.completeQuest('${quest.id}')" style="
                        flex: 1;
                        padding: 12px;
                        background: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">✅ Complete</button>
                </div>
            `;
        }

        return `
            <div style="
                background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(0,0,0,0.7));
                border-left: 4px solid ${color};
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            ">
                <!-- Header -->
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <div>
                        <div style="color: ${color}; font-size: 12px; font-weight: bold; margin-bottom: 5px;">
                            ${typeLabel}
                        </div>
                        <h3 style="color: white; font-size: 24px; margin: 0;">${quest.name}</h3>
                    </div>
                    <div style="
                        background: rgba(255,255,255,0.1);
                        padding: 8px 12px;
                        border-radius: 6px;
                        font-size: 14px;
                        color: #FFD700;
                        font-weight: bold;
                    ">Level ${quest.level_required || 1}</div>
                </div>

                <!-- Description -->
                <p style="color: #ccc; font-size: 16px; line-height: 1.6; margin: 15px 0;">
                    ${quest.description}
                </p>

                <!-- Region -->
                <div style="display: inline-block; background: rgba(33, 150, 243, 0.2); color: #2196F3; padding: 6px 12px; border-radius: 6px; font-size: 14px; margin-bottom: 10px;">
                    📍 ${quest.region || 'Unknown Region'}
                </div>

                ${progressHTML}
                ${objectivesHTML}

                <!-- Rewards -->
                ${quest.rewards ? `
                    <div style="margin-top: 15px; padding: 15px; background: rgba(255, 215, 0, 0.1); border-radius: 8px; border: 1px solid #FFD700;">
                        <div style="color: #FFD700; font-size: 14px; margin-bottom: 10px;">🎁 Rewards:</div>
                        <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                            ${quest.rewards.gold ? `<span style="color: white;">💰 ${quest.rewards.gold} Gold</span>` : ''}
                            ${quest.rewards.xp ? `<span style="color: white;">⭐ ${quest.rewards.xp} XP</span>` : ''}
                            ${quest.rewards.items ? quest.rewards.items.map(item => `<span style="color: white;">📦 ${item}</span>`).join('') : ''}
                        </div>
                    </div>
                ` : ''}

                ${actionsHTML}
            </div>
        `;
    }

    /**
     * TAB SWITCHING
     */
    switchTab(tab) {
        // Update Tabs
        document.getElementById('tab-active').className = 'quest-tab';
        document.getElementById('tab-available').className = 'quest-tab';
        document.getElementById(`tab-${tab}`).className = 'quest-tab quest-tab-active';

        // Update Tab Styles
        document.getElementById('tab-active').style.background = tab === 'active' ? '#4CAF50' : '#333';
        document.getElementById('tab-available').style.background = tab === 'available' ? '#4CAF50' : '#333';

        // Update Content
        const container = document.getElementById('quest-list-container');
        if (tab === 'active') {
            container.innerHTML = this.renderQuestList(this.activeQuests, 'active');
        } else {
            container.innerHTML = this.renderQuestList(this.availableQuests, 'available');
        }
    }

    /**
     * QUEST ACTIONS
     */
    async startQuest(questId) {
        try {
            const response = await fetch(`${this.API_BASE}/api/quests/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ quest_id: questId })
            });

            if (!response.ok) {
                console.error('[QUEST UI] ❌ Failed to start quest');
                return;
            }

            const result = await response.json();

            if (result.success) {
                console.log('[QUEST UI] ✅ Quest started:', result.quest_name);

                // Reload quests
                await this.loadQuests();
                this.renderQuestLog();

                // Show Najika reaction
                if (result.najika_reaction && window.chatUI) {
                    window.chatUI.addMessage('najika', result.najika_reaction);
                }
            } else {
                console.error('[QUEST UI] ❌', result.error);
            }
        } catch (error) {
            console.error('[QUEST UI] ❌ Error starting quest:', error);
        }
    }

    async completeQuest(questId) {
        try {
            const response = await fetch(`${this.API_BASE}/api/quests/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ quest_id: questId })
            });

            if (!response.ok) {
                console.error('[QUEST UI] ❌ Failed to complete quest');
                return;
            }

            const result = await response.json();

            if (result.success) {
                console.log('[QUEST UI] ✅ Quest completed:', result.quest_name);

                // Reload quests
                await this.loadQuests();
                this.renderQuestLog();

                // Show rewards + Najika reaction
                if (window.chatUI) {
                    const rewardsText = [];
                    if (result.rewards.gold) rewardsText.push(`💰 ${result.rewards.gold} Gold`);
                    if (result.rewards.xp) rewardsText.push(`⭐ ${result.rewards.xp} XP`);

                    window.chatUI.addMessage('system', `✅ Quest Complete! ${rewardsText.join(', ')}`);

                    if (result.najika_reaction) {
                        window.chatUI.addMessage('najika', result.najika_reaction);
                    }
                }
            } else {
                console.error('[QUEST UI] ❌', result.error);
            }
        } catch (error) {
            console.error('[QUEST UI] ❌ Error completing quest:', error);
        }
    }

    toggleTrackQuest(questId) {
        const index = this.trackedQuestIds.indexOf(questId);
        if (index > -1) {
            // Untrack
            this.trackedQuestIds.splice(index, 1);
        } else {
            // Track (max 3)
            if (this.trackedQuestIds.length >= 3) {
                this.trackedQuestIds.shift();  // Remove oldest
            }
            this.trackedQuestIds.push(questId);
        }

        this.updateQuestTracker();
        this.renderQuestLog();  // Update UI
    }

    /**
     * QUEST TRACKER (rechts oben) aktualisieren
     */
    updateQuestTracker() {
        const trackedQuests = this.activeQuests.filter(q => this.trackedQuestIds.includes(q.id));

        if (trackedQuests.length === 0) {
            this.questTracker.innerHTML = `
                <div style="text-align: center; color: #666;">
                    <div style="font-size: 36px; margin-bottom: 10px;">📋</div>
                    <div style="font-size: 14px;">No tracked quests</div>
                    <div style="font-size: 12px; margin-top: 5px;">Press Q to open Quest Log</div>
                </div>
            `;
            return;
        }

        const html = `
            <div style="margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #4CAF50;">
                <h3 style="color: #4CAF50; margin: 0; font-size: 18px;">📋 Tracked Quests</h3>
            </div>
            ${trackedQuests.map(quest => this.renderTrackedQuest(quest)).join('')}
            <div style="text-align: center; margin-top: 15px; padding-top: 10px; border-top: 1px solid #333;">
                <button onclick="window.questUI.openQuestLog()" style="
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 12px;
                ">Open Quest Log (Q)</button>
            </div>
        `;

        this.questTracker.innerHTML = html;
    }

    renderTrackedQuest(quest) {
        const progress = quest.progress || {};
        const completed = Object.values(progress).filter(v => v === true).length;
        const total = quest.objectives ? quest.objectives.length : 0;
        const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

        return `
            <div style="
                background: rgba(255,255,255,0.05);
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 12px;
            ">
                <div style="color: white; font-size: 14px; font-weight: bold; margin-bottom: 8px;">
                    ${quest.name}
                </div>
                <div style="background: #222; height: 6px; border-radius: 3px; overflow: hidden; margin-bottom: 6px;">
                    <div style="background: #4CAF50; height: 100%; width: ${percent}%;"></div>
                </div>
                <div style="color: #aaa; font-size: 12px;">
                    ${completed}/${total} Objectives (${percent}%)
                </div>
            </div>
        `;
    }
}

// Global Instance
window.questUI = null;

// Init nach DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    window.questUI = new QuestUI();
    console.log('[NAJIKA] ✅ Quest UI initialized');
});
