/**
 * Quest Tracker V2 - Najika World
 * ================================
 * Erweitert quest_ui.js mit:
 * - Animierter Quest-Tracker (Witcher 3 Style)
 * - Journal/Codex System (abgeschlossene Quests + Lore)
 * - Quest-Chain Visualisierung
 * - Minimap Quest-Markers
 * - Notification-Toasts bei Quest-Updates
 *
 * Haengt sich an window.questUI an und erweitert es.
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // QUEST JOURNAL (Codex)
    // ==========================================

    const QUEST_CATEGORIES = {
        main:        { label: 'Hauptquest',   icon: '\uD83D\uDD25', color: '#FF4444' },
        side:        { label: 'Nebenquests',  icon: '\uD83D\uDCCB', color: '#4CAF50' },
        legendary:   { label: 'Legendaer',    icon: '\u2B50',       color: '#FFD700' },
        faction:     { label: 'Fraktionen',   icon: '\uD83C\uDFF0', color: '#9C27B0' },
        exploration: { label: 'Erkundung',    icon: '\uD83D\uDDFA',  color: '#2196F3' },
        companion:   { label: 'Gefaehrten',   icon: '\u2764',       color: '#E91E63' },
        daily:       { label: 'Taeglich',     icon: '\uD83D\uDD04', color: '#FF9800' }
    };

    // Quest-Chains: verkettete Quests
    const QUEST_CHAINS = {
        'hauptstory': {
            name: 'Der Goetterfels ruft',
            quests: ['prolog_erwachen', 'reise_nach_samtmoos', 'der_erste_splitter',
                     'die_salzwind_probe', 'blitzebene_ritual', 'vulkan_herz',
                     'kristall_tiefe', 'goetterfels_aufstieg'],
            color: '#FF4444'
        },
        'schleim_band': {
            name: 'Band des Vertrauens',
            quests: ['schleim_finden', 'erste_fuetterung', 'form_entdecken',
                     'aura_erwachen', 'modus_wahl', 'seelenbund'],
            color: '#E91E63'
        },
        'fraktionskrieg': {
            name: 'Krieg der Voelker',
            quests: ['geruechte_hoeren', 'fraktion_waehlen', 'erste_mission',
                     'krieg_vorbereiten', 'entscheidungsschlacht'],
            color: '#9C27B0'
        }
    };

    // ==========================================
    // JOURNAL DATA STORE
    // ==========================================

    class QuestJournal {
        constructor() {
            this.completedQuests = [];
            this.loreEntries = [];
            this.questNotes = {};   // questId -> user notes
            this.discoveredChains = new Set();
            this.currentTab = 'active';
            this.currentCategory = 'all';
            this.searchQuery = '';
            this.load();
        }

        save() {
            try {
                localStorage.setItem('najika_quest_journal', JSON.stringify({
                    completedQuests: this.completedQuests,
                    loreEntries: this.loreEntries,
                    questNotes: this.questNotes,
                    discoveredChains: [...this.discoveredChains]
                }));
            } catch(e) { /* silent */ }
        }

        load() {
            try {
                const data = JSON.parse(localStorage.getItem('najika_quest_journal'));
                if (data) {
                    this.completedQuests = data.completedQuests || [];
                    this.loreEntries = data.loreEntries || [];
                    this.questNotes = data.questNotes || {};
                    this.discoveredChains = new Set(data.discoveredChains || []);
                }
            } catch(e) { /* silent */ }
        }

        addCompleted(quest) {
            if (!this.completedQuests.find(q => q.id === quest.id)) {
                this.completedQuests.push({
                    ...quest,
                    completedAt: Date.now()
                });
                this.save();
            }
        }

        addLoreEntry(entry) {
            if (!this.loreEntries.find(e => e.id === entry.id)) {
                this.loreEntries.push({
                    ...entry,
                    discoveredAt: Date.now()
                });
                this.save();
                showNotification('\uD83D\uDCD6 Neuer Lore-Eintrag', entry.title, '#2196F3');
            }
        }

        setNote(questId, note) {
            this.questNotes[questId] = note;
            this.save();
        }

        getNote(questId) {
            return this.questNotes[questId] || '';
        }
    }

    // ==========================================
    // NOTIFICATION TOASTS
    // ==========================================

    let notificationQueue = [];
    let isShowingNotification = false;

    function showNotification(title, message, color) {
        notificationQueue.push({ title, message, color });
        if (!isShowingNotification) processNotificationQueue();
    }

    function processNotificationQueue() {
        if (notificationQueue.length === 0) {
            isShowingNotification = false;
            return;
        }

        isShowingNotification = true;
        const { title, message, color } = notificationQueue.shift();

        const toast = document.createElement('div');
        toast.style.cssText = `
            position:fixed; top:-80px; right:20px;
            background:linear-gradient(135deg, rgba(10,10,30,0.95), rgba(5,5,15,0.98));
            border:2px solid ${color || '#4CAF50'};
            border-radius:12px; padding:15px 20px;
            color:white; font-family:'Courier New',monospace;
            z-index:12000; min-width:280px; max-width:400px;
            box-shadow:0 8px 32px rgba(0,0,0,0.8);
            transition: top 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        `;
        toast.innerHTML = `
            <div style="font-size:12px;color:${color || '#4CAF50'};font-weight:bold;
                letter-spacing:1px;margin-bottom:4px;">${title}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.8);">${message}</div>
        `;
        document.body.appendChild(toast);

        requestAnimationFrame(() => { toast.style.top = '20px'; });

        setTimeout(() => {
            toast.style.top = '-80px';
            setTimeout(() => {
                toast.remove();
                processNotificationQueue();
            }, 500);
        }, 3000);
    }

    // ==========================================
    // ENHANCED QUEST TRACKER (Witcher-Style)
    // ==========================================

    function createEnhancedTracker() {
        const existing = document.getElementById('quest-tracker-v2');
        if (existing) existing.remove();

        const tracker = document.createElement('div');
        tracker.id = 'quest-tracker-v2';
        tracker.style.cssText = `
            position:fixed; top:20px; right:20px;
            width:300px; max-height:450px;
            background:linear-gradient(180deg, rgba(5,5,15,0.92), rgba(10,10,25,0.88));
            border:1px solid rgba(76,175,80,0.3);
            border-radius:10px; padding:0;
            z-index:550; overflow:hidden;
            font-family:'Courier New',monospace;
            box-shadow:0 4px 24px rgba(0,0,0,0.6);
            backdrop-filter:blur(8px);
        `;
        document.body.appendChild(tracker);
        return tracker;
    }

    function renderEnhancedTracker(questUI) {
        if (!questUI) return;

        const tracker = document.getElementById('quest-tracker-v2') || createEnhancedTracker();
        const tracked = (questUI.activeQuests || []).filter(q =>
            (questUI.trackedQuestIds || []).includes(q.id)
        );

        // Alten Tracker verstecken
        const oldTracker = document.getElementById('quest-tracker');
        if (oldTracker) oldTracker.style.display = 'none';

        if (tracked.length === 0) {
            tracker.innerHTML = `
                <div style="padding:20px;text-align:center;">
                    <div style="font-size:10px;color:rgba(76,175,80,0.5);
                        letter-spacing:2px;margin-bottom:8px;">QUEST TRACKER</div>
                    <div style="color:rgba(255,255,255,0.3);font-size:11px;">
                        Keine Quests verfolgt<br>
                        <span style="font-size:10px;">Druecke Q fuer Quest Log</span>
                    </div>
                </div>
            `;
            return;
        }

        let html = `
            <div style="padding:10px 14px 6px;border-bottom:1px solid rgba(76,175,80,0.2);
                display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:10px;color:rgba(76,175,80,0.6);
                    letter-spacing:2px;font-weight:bold;">QUEST TRACKER</span>
                <span style="font-size:9px;color:rgba(255,255,255,0.3);">${tracked.length}/3</span>
            </div>
            <div style="padding:8px 10px;max-height:380px;overflow-y:auto;">
        `;

        tracked.forEach((quest, idx) => {
            const progress = quest.progress || {};
            const objectives = quest.objectives || [];
            const completed = Object.values(progress).filter(v => v === true).length;
            const total = objectives.length;
            const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

            const typeColors = {
                'main_quest': '#FF4444', 'side_quest': '#4CAF50',
                'legendary_quest': '#FFD700', 'story_quest': '#9C27B0',
                'exploration_quest': '#2196F3'
            };
            const color = typeColors[quest.type] || '#4CAF50';

            html += `
                <div style="padding:8px 10px;margin-bottom:${idx < tracked.length - 1 ? '6' : '0'}px;
                    background:rgba(255,255,255,0.03);border-radius:6px;
                    border-left:3px solid ${color};">
                    <div style="display:flex;justify-content:space-between;align-items:center;
                        margin-bottom:6px;">
                        <span style="font-size:11px;color:white;font-weight:bold;
                            max-width:200px;overflow:hidden;text-overflow:ellipsis;
                            white-space:nowrap;">${quest.name}</span>
                        <span style="font-size:9px;color:${color};">${percent}%</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.08);height:3px;
                        border-radius:2px;overflow:hidden;margin-bottom:6px;">
                        <div style="background:${color};height:100%;width:${percent}%;
                            transition:width 0.6s ease;border-radius:2px;
                            ${percent === 100 ? 'box-shadow:0 0 6px ' + color + ';' : ''}"></div>
                    </div>
            `;

            // Aktuelle Objectives (nur unerledigte, max 2)
            const pendingObjs = objectives.filter((_, i) => !progress[i]);
            pendingObjs.slice(0, 2).forEach(obj => {
                html += `
                    <div style="font-size:9px;color:rgba(255,255,255,0.5);
                        padding:2px 0;display:flex;align-items:center;gap:4px;">
                        <span style="color:rgba(255,255,255,0.2);">\u25CB</span>
                        ${obj.description}
                        ${obj.target_amount > 1 ? `<span style="color:rgba(255,255,255,0.3);">(0/${obj.target_amount})</span>` : ''}
                    </div>
                `;
            });
            if (pendingObjs.length > 2) {
                html += `<div style="font-size:8px;color:rgba(255,255,255,0.3);padding-top:2px;">
                    +${pendingObjs.length - 2} weitere...</div>`;
            }

            html += `</div>`;
        });

        html += `</div>`;
        tracker.innerHTML = html;
    }

    // ==========================================
    // JOURNAL UI (Full-Screen Overlay)
    // ==========================================

    function openJournalUI(questUI, journal) {
        const existing = document.getElementById('quest-journal-overlay');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'quest-journal-overlay';
        overlay.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.97);
            backdrop-filter:blur(12px);
            z-index:10001; display:flex;
            font-family:'Courier New',monospace;
        `;

        // Sidebar
        const sidebar = document.createElement('div');
        sidebar.style.cssText = `
            width:240px; background:rgba(10,10,20,1);
            border-right:1px solid rgba(76,175,80,0.2);
            padding:20px 0; overflow-y:auto;
        `;

        const tabs = [
            { id: 'active',    icon: '\uD83D\uDD25', label: 'Aktiv',       count: (questUI.activeQuests || []).length },
            { id: 'available', icon: '\uD83D\uDCCB', label: 'Verfuegbar',  count: (questUI.availableQuests || []).length },
            { id: 'completed', icon: '\u2705',       label: 'Abgeschlossen', count: journal.completedQuests.length },
            { id: 'chains',    icon: '\uD83D\uDD17', label: 'Quest-Ketten', count: Object.keys(QUEST_CHAINS).length },
            { id: 'lore',      icon: '\uD83D\uDCD6', label: 'Kodex',       count: journal.loreEntries.length }
        ];

        sidebar.innerHTML = `
            <div style="padding:0 16px 16px;border-bottom:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:16px;color:#4CAF50;font-weight:bold;">Quest Journal</div>
                <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:4px;">
                    ${(questUI.activeQuests || []).length} aktiv |
                    ${journal.completedQuests.length} fertig
                </div>
            </div>
            ${tabs.map(t => `
                <div onclick="window.QuestTrackerV2._switchJournalTab('${t.id}')"
                    id="journal-tab-${t.id}"
                    style="padding:10px 16px;cursor:pointer;display:flex;align-items:center;
                    gap:8px;font-size:11px;color:rgba(255,255,255,0.6);
                    border-left:3px solid transparent;
                    transition:all 0.2s;
                    ${journal.currentTab === t.id ? 'color:white;border-left-color:#4CAF50;background:rgba(76,175,80,0.08);' : ''}"
                    onmouseover="this.style.background='rgba(255,255,255,0.04)'"
                    onmouseout="this.style.background='${journal.currentTab === t.id ? 'rgba(76,175,80,0.08)' : 'transparent'}'">
                    <span style="font-size:14px;">${t.icon}</span>
                    <span style="flex:1;">${t.label}</span>
                    <span style="font-size:9px;color:rgba(255,255,255,0.3);
                        background:rgba(255,255,255,0.06);padding:2px 6px;
                        border-radius:8px;">${t.count}</span>
                </div>
            `).join('')}
            <div style="padding:16px;border-top:1px solid rgba(255,255,255,0.06);margin-top:auto;">
                <div style="font-size:9px;color:rgba(255,255,255,0.2);text-align:center;">
                    Q = Schliessen | J = Journal
                </div>
            </div>
        `;

        // Main Content
        const main = document.createElement('div');
        main.id = 'journal-main-content';
        main.style.cssText = `flex:1;overflow-y:auto;padding:24px 30px;`;

        // Close Button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '\u2715';
        closeBtn.style.cssText = `
            position:absolute;top:16px;right:20px;background:none;border:none;
            color:rgba(255,255,255,0.4);font-size:20px;cursor:pointer;z-index:10;
        `;
        closeBtn.onclick = () => overlay.remove();

        overlay.appendChild(sidebar);
        overlay.appendChild(main);
        overlay.appendChild(closeBtn);
        document.body.appendChild(overlay);

        renderJournalContent(journal.currentTab, questUI, journal);
    }

    function renderJournalContent(tab, questUI, journal) {
        const main = document.getElementById('journal-main-content');
        if (!main) return;

        journal.currentTab = tab;

        // Update tab highlights
        ['active','available','completed','chains','lore'].forEach(t => {
            const el = document.getElementById(`journal-tab-${t}`);
            if (el) {
                el.style.color = t === tab ? 'white' : 'rgba(255,255,255,0.6)';
                el.style.borderLeftColor = t === tab ? '#4CAF50' : 'transparent';
                el.style.background = t === tab ? 'rgba(76,175,80,0.08)' : 'transparent';
            }
        });

        switch(tab) {
            case 'active':
                main.innerHTML = renderQuestListV2(questUI.activeQuests || [], 'active', questUI, journal);
                break;
            case 'available':
                main.innerHTML = renderQuestListV2(questUI.availableQuests || [], 'available', questUI, journal);
                break;
            case 'completed':
                main.innerHTML = renderCompletedList(journal);
                break;
            case 'chains':
                main.innerHTML = renderQuestChains(questUI, journal);
                break;
            case 'lore':
                main.innerHTML = renderLoreCodex(journal);
                break;
        }
    }

    // ==========================================
    // QUEST LIST V2
    // ==========================================

    function renderQuestListV2(quests, type, questUI, journal) {
        if (quests.length === 0) {
            return `
                <div style="text-align:center;padding:60px 0;color:rgba(255,255,255,0.3);">
                    <div style="font-size:36px;margin-bottom:12px;">\uD83D\uDCED</div>
                    <div style="font-size:13px;">Keine ${type === 'active' ? 'aktiven' : 'verfuegbaren'} Quests</div>
                </div>
            `;
        }

        let html = `
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div style="font-size:14px;color:white;font-weight:bold;">
                    ${type === 'active' ? '\uD83D\uDD25 Aktive Quests' : '\uD83D\uDCCB Verfuegbare Quests'}
                </div>
                <div style="font-size:10px;color:rgba(255,255,255,0.3);">${quests.length} Quests</div>
            </div>
        `;

        quests.forEach(quest => {
            const progress = quest.progress || {};
            const objectives = quest.objectives || [];
            const completed = Object.values(progress).filter(v => v === true).length;
            const total = objectives.length;
            const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

            const typeColors = {
                'main_quest': '#FF4444', 'side_quest': '#4CAF50',
                'legendary_quest': '#FFD700', 'story_quest': '#9C27B0',
                'exploration_quest': '#2196F3', 'faction_quest': '#9C27B0'
            };
            const color = typeColors[quest.type] || '#4CAF50';

            const isTracked = (questUI.trackedQuestIds || []).includes(quest.id);
            const note = journal.getNote(quest.id);

            html += `
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                    border-left:3px solid ${color};border-radius:8px;padding:16px;margin-bottom:12px;
                    transition:background 0.2s;"
                    onmouseover="this.style.background='rgba(255,255,255,0.04)'"
                    onmouseout="this.style.background='rgba(255,255,255,0.02)'">

                    <div style="display:flex;justify-content:space-between;align-items:start;">
                        <div style="flex:1;">
                            <div style="font-size:9px;color:${color};letter-spacing:1px;
                                font-weight:bold;margin-bottom:4px;">
                                ${(quest.type || 'side_quest').replace(/_/g, ' ').toUpperCase()}
                            </div>
                            <div style="font-size:14px;color:white;font-weight:bold;margin-bottom:6px;">
                                ${quest.name}
                            </div>
                            <div style="font-size:11px;color:rgba(255,255,255,0.5);line-height:1.5;">
                                ${quest.description}
                            </div>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:4px;margin-left:12px;">
                            <span style="font-size:9px;color:rgba(255,215,0,0.6);
                                background:rgba(255,215,0,0.08);padding:3px 8px;
                                border-radius:4px;text-align:center;">Lv.${quest.level_required || 1}</span>
                            ${quest.region ? `<span style="font-size:9px;color:rgba(33,150,243,0.6);
                                background:rgba(33,150,243,0.08);padding:3px 8px;
                                border-radius:4px;text-align:center;">${quest.region}</span>` : ''}
                        </div>
                    </div>
            `;

            // Progress bar (active only)
            if (type === 'active' && total > 0) {
                html += `
                    <div style="margin-top:12px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <span style="font-size:9px;color:rgba(255,255,255,0.4);">Fortschritt</span>
                            <span style="font-size:9px;color:${color};">${completed}/${total} (${percent}%)</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.06);height:4px;border-radius:2px;overflow:hidden;">
                            <div style="background:${color};height:100%;width:${percent}%;
                                transition:width 0.6s ease;border-radius:2px;
                                ${percent === 100 ? 'box-shadow:0 0 8px ' + color + ';' : ''}"></div>
                        </div>
                    </div>
                `;

                // Objectives
                objectives.forEach((obj, idx) => {
                    const done = progress[idx] === true;
                    html += `
                        <div style="font-size:10px;padding:3px 0;display:flex;align-items:center;gap:6px;
                            color:${done ? 'rgba(76,175,80,0.6)' : 'rgba(255,255,255,0.5)'};
                            ${done ? 'text-decoration:line-through;' : ''}">
                            <span>${done ? '\u2713' : '\u25CB'}</span>
                            ${obj.description}
                        </div>
                    `;
                });
            }

            // Rewards
            if (quest.rewards) {
                html += `<div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">`;
                if (quest.rewards.gold) html += `<span style="font-size:9px;color:rgba(255,215,0,0.6);
                    background:rgba(255,215,0,0.06);padding:2px 8px;border-radius:4px;">
                    \uD83D\uDCB0 ${quest.rewards.gold}</span>`;
                if (quest.rewards.xp) html += `<span style="font-size:9px;color:rgba(76,175,80,0.6);
                    background:rgba(76,175,80,0.06);padding:2px 8px;border-radius:4px;">
                    \u2B50 ${quest.rewards.xp} XP</span>`;
                html += `</div>`;
            }

            // Actions
            html += `<div style="margin-top:10px;display:flex;gap:8px;">`;
            if (type === 'active') {
                html += `
                    <button onclick="window.questUI.toggleTrackQuest('${quest.id}');window.QuestTrackerV2.refresh()"
                        style="flex:1;padding:6px;font-size:10px;font-family:inherit;
                        background:${isTracked ? 'rgba(255,152,0,0.15)' : 'rgba(255,255,255,0.04)'};
                        border:1px solid ${isTracked ? 'rgba(255,152,0,0.3)' : 'rgba(255,255,255,0.1)'};
                        color:${isTracked ? '#FF9800' : 'rgba(255,255,255,0.5)'};
                        border-radius:4px;cursor:pointer;">
                        ${isTracked ? '\uD83D\uDCCC Verfolgt' : '\uD83D\uDCCD Verfolgen'}
                    </button>
                    <button onclick="window.questUI.completeQuest('${quest.id}');window.QuestTrackerV2.refresh()"
                        style="flex:1;padding:6px;font-size:10px;font-family:inherit;
                        background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.3);
                        color:#4CAF50;border-radius:4px;cursor:pointer;">
                        \u2705 Abschliessen
                    </button>
                `;
            } else {
                html += `
                    <button onclick="window.questUI.startQuest('${quest.id}');window.QuestTrackerV2.refresh()"
                        style="flex:1;padding:8px;font-size:10px;font-family:inherit;
                        background:rgba(76,175,80,0.15);border:1px solid rgba(76,175,80,0.3);
                        color:#4CAF50;border-radius:4px;cursor:pointer;font-weight:bold;">
                        \u25B6 Quest starten
                    </button>
                `;
            }
            html += `</div></div>`;
        });

        return html;
    }

    // ==========================================
    // COMPLETED QUESTS
    // ==========================================

    function renderCompletedList(journal) {
        if (journal.completedQuests.length === 0) {
            return `
                <div style="text-align:center;padding:60px 0;color:rgba(255,255,255,0.3);">
                    <div style="font-size:36px;margin-bottom:12px;">\uD83D\uDCDA</div>
                    <div style="font-size:13px;">Noch keine Quests abgeschlossen</div>
                </div>
            `;
        }

        let html = `
            <div style="font-size:14px;color:white;font-weight:bold;margin-bottom:20px;">
                \u2705 Abgeschlossene Quests (${journal.completedQuests.length})
            </div>
        `;

        // Sortiert nach completedAt (neueste zuerst)
        const sorted = [...journal.completedQuests].sort((a, b) => b.completedAt - a.completedAt);

        sorted.forEach(quest => {
            const date = new Date(quest.completedAt);
            const dateStr = `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`;

            html += `
                <div style="background:rgba(76,175,80,0.03);border:1px solid rgba(76,175,80,0.1);
                    border-radius:8px;padding:14px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:12px;color:white;">${quest.name}</div>
                            <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px;">
                                ${quest.description || ''}
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:9px;color:rgba(76,175,80,0.5);">\u2713 Erledigt</div>
                            <div style="font-size:8px;color:rgba(255,255,255,0.2);margin-top:2px;">${dateStr}</div>
                        </div>
                    </div>
                </div>
            `;
        });

        return html;
    }

    // ==========================================
    // QUEST CHAINS
    // ==========================================

    function renderQuestChains(questUI, journal) {
        let html = `
            <div style="font-size:14px;color:white;font-weight:bold;margin-bottom:20px;">
                \uD83D\uDD17 Quest-Ketten
            </div>
        `;

        const activeIds = (questUI.activeQuests || []).map(q => q.id);
        const completedIds = journal.completedQuests.map(q => q.id);

        Object.entries(QUEST_CHAINS).forEach(([chainId, chain]) => {
            const chainCompleted = chain.quests.filter(qId => completedIds.includes(qId)).length;
            const chainActive = chain.quests.filter(qId => activeIds.includes(qId)).length;
            const chainPercent = Math.round((chainCompleted / chain.quests.length) * 100);

            html += `
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:18px;margin-bottom:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;
                        margin-bottom:12px;">
                        <div>
                            <div style="font-size:13px;color:${chain.color};font-weight:bold;">
                                ${chain.name}
                            </div>
                            <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px;">
                                ${chainCompleted}/${chain.quests.length} Quests
                                ${chainActive > 0 ? ` | ${chainActive} aktiv` : ''}
                            </div>
                        </div>
                        <div style="font-size:12px;color:${chain.color};font-weight:bold;">
                            ${chainPercent}%
                        </div>
                    </div>

                    <!-- Progress Bar -->
                    <div style="background:rgba(255,255,255,0.06);height:6px;border-radius:3px;
                        overflow:hidden;margin-bottom:14px;">
                        <div style="background:${chain.color};height:100%;width:${chainPercent}%;
                            border-radius:3px;transition:width 0.6s;
                            ${chainPercent === 100 ? 'box-shadow:0 0 10px ' + chain.color + ';' : ''}"></div>
                    </div>

                    <!-- Chain Steps -->
                    <div style="display:flex;align-items:center;gap:0;flex-wrap:wrap;">
                        ${chain.quests.map((qId, idx) => {
                            const isCompleted = completedIds.includes(qId);
                            const isActive = activeIds.includes(qId);
                            const stateColor = isCompleted ? chain.color :
                                              isActive ? '#FF9800' : 'rgba(255,255,255,0.15)';

                            return `
                                <div style="display:flex;align-items:center;">
                                    <div style="width:20px;height:20px;border-radius:50%;
                                        background:${isCompleted ? stateColor : 'transparent'};
                                        border:2px solid ${stateColor};
                                        display:flex;align-items:center;justify-content:center;
                                        font-size:8px;color:${isCompleted ? 'white' : stateColor};
                                        ${isActive ? 'box-shadow:0 0 8px rgba(255,152,0,0.5);animation:pulse 2s infinite;' : ''}">
                                        ${isCompleted ? '\u2713' : idx + 1}
                                    </div>
                                    ${idx < chain.quests.length - 1 ? `
                                        <div style="width:16px;height:2px;
                                            background:${isCompleted ? stateColor : 'rgba(255,255,255,0.08)'};"></div>
                                    ` : ''}
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        });

        return html;
    }

    // ==========================================
    // LORE CODEX
    // ==========================================

    function renderLoreCodex(journal) {
        if (journal.loreEntries.length === 0) {
            return `
                <div style="text-align:center;padding:60px 0;color:rgba(255,255,255,0.3);">
                    <div style="font-size:36px;margin-bottom:12px;">\uD83D\uDCD6</div>
                    <div style="font-size:13px;">Noch keine Lore-Eintraege entdeckt</div>
                    <div style="font-size:10px;margin-top:6px;color:rgba(255,255,255,0.2);">
                        Erkunde die Welt und schliesse Quests ab!</div>
                </div>
            `;
        }

        let html = `
            <div style="font-size:14px;color:white;font-weight:bold;margin-bottom:20px;">
                \uD83D\uDCD6 Kodex (${journal.loreEntries.length} Eintraege)
            </div>
        `;

        journal.loreEntries.forEach(entry => {
            html += `
                <div style="background:rgba(33,150,243,0.03);border:1px solid rgba(33,150,243,0.1);
                    border-radius:8px;padding:16px;margin-bottom:10px;">
                    <div style="font-size:12px;color:#2196F3;font-weight:bold;margin-bottom:6px;">
                        ${entry.title}
                    </div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.6);line-height:1.6;">
                        ${entry.text}
                    </div>
                    ${entry.region ? `<div style="font-size:8px;color:rgba(255,255,255,0.2);
                        margin-top:8px;">\uD83D\uDCCD ${entry.region}</div>` : ''}
                </div>
            `;
        });

        return html;
    }

    // ==========================================
    // QUEST UPDATE NOTIFICATIONS
    // ==========================================

    function onQuestStarted(questName) {
        showNotification('QUEST GESTARTET', questName, '#4CAF50');
    }

    function onQuestCompleted(questName, rewards) {
        showNotification('QUEST ABGESCHLOSSEN', `${questName}${rewards ? ' | ' + rewards : ''}`, '#FFD700');
    }

    function onObjectiveCompleted(objectiveName) {
        showNotification('ZIEL ERREICHT', objectiveName, '#2196F3');
    }

    // ==========================================
    // KEYBOARD & INTEGRATION
    // ==========================================

    const journal = new QuestJournal();

    function initV2() {
        // Keyboard: J = Journal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'j' || e.key === 'J') {
                const chatUI = document.getElementById('chat-ui');
                if (chatUI && chatUI.style.display !== 'none') return;
                const existing = document.getElementById('quest-journal-overlay');
                if (existing) {
                    existing.remove();
                } else if (window.questUI) {
                    openJournalUI(window.questUI, journal);
                }
            }
        });

        // Periodisch Tracker updaten
        setInterval(() => {
            if (window.questUI) {
                renderEnhancedTracker(window.questUI);
            }
        }, 5000);

        // Initial render
        setTimeout(() => {
            if (window.questUI) {
                renderEnhancedTracker(window.questUI);
            }
        }, 2000);

        // Hook into questUI methods
        setTimeout(() => {
            if (window.questUI) {
                const origStart = window.questUI.startQuest.bind(window.questUI);
                window.questUI.startQuest = async function(questId) {
                    await origStart(questId);
                    const quest = (window.questUI.activeQuests || []).find(q => q.id === questId);
                    if (quest) onQuestStarted(quest.name);
                    renderEnhancedTracker(window.questUI);
                };

                const origComplete = window.questUI.completeQuest.bind(window.questUI);
                window.questUI.completeQuest = async function(questId) {
                    const quest = (window.questUI.activeQuests || []).find(q => q.id === questId);
                    await origComplete(questId);
                    if (quest) {
                        journal.addCompleted(quest);
                        onQuestCompleted(quest.name);
                    }
                    renderEnhancedTracker(window.questUI);
                };
            }
        }, 3000);
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.QuestTrackerV2 = {
        journal,
        QUEST_CHAINS,
        QUEST_CATEGORIES,
        showNotification,
        onQuestStarted,
        onQuestCompleted,
        onObjectiveCompleted,
        openJournal: () => window.questUI && openJournalUI(window.questUI, journal),
        refresh: () => window.questUI && renderEnhancedTracker(window.questUI),
        _switchJournalTab: (tab) => window.questUI && renderJournalContent(tab, window.questUI, journal),
        init: initV2
    };

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initV2);
    } else {
        initV2();
    }

    console.log('[OK] Quest Tracker V2 geladen: Journal + Chains + Notifications');

})();
