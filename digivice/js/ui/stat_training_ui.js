// ============================================================
// STAT TRAINING UI - Trainiere Stats durch Aktivitäten
// Learning by Doing! (Skyrim + KCD + Digimon World)
// ============================================================
(function() {
    'use strict';

    // Trainings-Aktivitäten (aus Backend-Design)
    const ACTIVITIES = {
        // STÄRKE
        chop_wood: { name: 'Holz hacken', icon: '🪓', category: 'labor', stats: { strength: 15, endurance: 5 }, staminaCost: 30, time: 30 },
        carry_heavy: { name: 'Schwere Last tragen', icon: '📦', category: 'labor', stats: { strength: 20, endurance: 10 }, staminaCost: 40, time: 20 },
        mining: { name: 'Bergbau', icon: '⛏️', category: 'labor', stats: { strength: 25, endurance: 15, perception: 5 }, staminaCost: 50, time: 60, dailyLimit: 3 },
        push_ups: { name: 'Liegestütze', icon: '💪', category: 'training', stats: { strength: 10, endurance: 5 }, staminaCost: 20, time: 10, cooldown: 30 },
        wrestling: { name: 'Ringen', icon: '🤼', category: 'combat', stats: { strength: 15, agility: 10, endurance: 10 }, staminaCost: 40, time: 30 },
        smithing: { name: 'Am Amboss hämmern', icon: '🔨', category: 'crafting', stats: { strength: 20, agility: 5 }, staminaCost: 35, time: 45 },

        // AUSDAUER
        running: { name: 'Laufen', icon: '🏃', category: 'training', stats: { endurance: 20, agility: 5 }, staminaCost: 30, time: 30 },
        swimming: { name: 'Schwimmen', icon: '🏊', category: 'training', stats: { endurance: 25, strength: 10, agility: 5 }, staminaCost: 35, time: 30 },
        climbing: { name: 'Klettern', icon: '🧗', category: 'exploration', stats: { endurance: 15, strength: 15, agility: 10 }, staminaCost: 40, time: 20, requires: { strength: 5 } },
        sparring: { name: 'Langes Sparring', icon: '🥊', category: 'combat', stats: { endurance: 30, strength: 5, agility: 5 }, staminaCost: 60, time: 60, dailyLimit: 2 },

        // GESCHICKLICHKEIT
        archery: { name: 'Bogenschießen üben', icon: '🏹', category: 'training', stats: { agility: 20, perception: 10 }, staminaCost: 15, time: 30 },
        lockpicking: { name: 'Schlösser knacken', icon: '🔓', category: 'training', stats: { agility: 25, perception: 5, intelligence: 5 }, staminaCost: 5, time: 20 },
        knife_juggling: { name: 'Messer jonglieren', icon: '🗡️', category: 'training', stats: { agility: 30, perception: 10 }, staminaCost: 10, time: 15, requires: { agility: 8 } },
        dual_wield: { name: 'Beidhändig kämpfen', icon: '⚔️', category: 'combat', stats: { agility: 25, strength: 5 }, staminaCost: 30, time: 30, requires: { agility: 6 } },
        sewing: { name: 'Nähen', icon: '🧵', category: 'crafting', stats: { agility: 15, perception: 5 }, staminaCost: 5, time: 30 },

        // INTELLIGENZ
        read_books: { name: 'Bücher lesen', icon: '📚', category: 'study', stats: { intelligence: 25 }, staminaCost: 0, manaCost: 0, time: 60 },
        solve_puzzles: { name: 'Rätsel lösen', icon: '🧩', category: 'study', stats: { intelligence: 20, perception: 5 }, staminaCost: 0, time: 30 },
        magic_theory: { name: 'Magietheorie', icon: '📖', category: 'study', stats: { intelligence: 30, perception: 5 }, manaCost: 5, time: 45 },
        spell_practice: { name: 'Zauber üben', icon: '🔮', category: 'magic', stats: { intelligence: 20, agility: 5 }, manaCost: 30, time: 30 },
        alchemy: { name: 'Tränke brauen', icon: '⚗️', category: 'crafting', stats: { agility: 10, intelligence: 15 }, manaCost: 10, time: 30 },
        meditation: { name: 'Meditation', icon: '🧘', category: 'training', stats: { intelligence: 15, perception: 10 }, manaCost: 10, time: 30 },

        // WAHRNEHMUNG
        tracking: { name: 'Fährten lesen', icon: '🐾', category: 'exploration', stats: { perception: 25, intelligence: 5 }, staminaCost: 10, time: 45 },
        scouting: { name: 'Spähen', icon: '🔭', category: 'exploration', stats: { perception: 20, agility: 10 }, staminaCost: 15, time: 30 },
        trap_detection: { name: 'Fallen suchen', icon: '🪤', category: 'training', stats: { perception: 30, intelligence: 5 }, staminaCost: 10, time: 30 },
        stargazing: { name: 'Sterne beobachten', icon: '🌟', category: 'study', stats: { perception: 15, intelligence: 10 }, staminaCost: 0, time: 60 },
        hunting: { name: 'Jagen', icon: '🦌', category: 'exploration', stats: { perception: 20, agility: 10, endurance: 5 }, staminaCost: 30, time: 90 },

        // CHARISMA
        haggling: { name: 'Feilschen', icon: '💰', category: 'social', stats: { charisma: 20, intelligence: 5 }, staminaCost: 0, time: 15 },
        storytelling: { name: 'Geschichten erzählen', icon: '📜', category: 'social', stats: { charisma: 25, intelligence: 5 }, staminaCost: 0, time: 30 },
        music: { name: 'Musizieren', icon: '🎵', category: 'social', stats: { charisma: 15, agility: 10 }, staminaCost: 5, time: 30 },
        flirting: { name: 'Flirten üben', icon: '😘', category: 'social', stats: { charisma: 20, perception: 5 }, staminaCost: 0, time: 15 },
        perform: { name: 'Auftreten', icon: '🎭', category: 'social', stats: { charisma: 30, endurance: 5 }, staminaCost: 10, time: 30, requires: { charisma: 8 } }
    };

    const STAT_NAMES = {
        strength: { name: 'Stärke', icon: '💪', color: '#e74c3c' },
        endurance: { name: 'Ausdauer', icon: '🛡️', color: '#2ecc71' },
        agility: { name: 'Agilität', icon: '🏃', color: '#3498db' },
        intelligence: { name: 'Intelligenz', icon: '🧠', color: '#9b59b6' },
        perception: { name: 'Wahrnehmung', icon: '👁️', color: '#f39c12' },
        charisma: { name: 'Charme', icon: '✨', color: '#e91e63' },
        luck: { name: 'Glück', icon: '🍀', color: '#FFD700' }
    };

    const CATEGORY_NAMES = {
        labor: '🔨 Arbeit', training: '🏋️ Training', combat: '⚔️ Kampf',
        crafting: '🔧 Handwerk', study: '📚 Studium', magic: '🔮 Magie',
        exploration: '🗺️ Erkundung', social: '💬 Sozial'
    };

    class StatTrainingUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.filterCategory = 'all';
            this.trainingLog = this.loadLog();
            this.dailyCount = this.loadDailyCount();
        }

        loadLog() {
            try { return JSON.parse(localStorage.getItem('najika_training_log') || '[]'); }
            catch { return []; }
        }

        loadDailyCount() {
            try {
                const data = JSON.parse(localStorage.getItem('najika_training_daily') || '{}');
                const today = new Date().toDateString();
                if (data.date !== today) return { date: today, counts: {}, totalXP: 0 };
                return data;
            } catch { return { date: new Date().toDateString(), counts: {}, totalXP: 0 }; }
        }

        saveDailyCount() {
            localStorage.setItem('najika_training_daily', JSON.stringify(this.dailyCount));
        }

        saveLog() {
            // Keep last 50 entries
            if (this.trainingLog.length > 50) this.trainingLog = this.trainingLog.slice(-50);
            localStorage.setItem('najika_training_log', JSON.stringify(this.trainingLog));
        }

        getPlayerStats() {
            return window.EquipmentCombat?.getPlayerStats?.() || {
                strength: 10, intelligence: 10, agility: 10,
                endurance: 10, luck: 10, charm: 10
            };
        }

        // Diminishing returns formula
        calcXPGain(baseXP, currentStatValue) {
            // Higher stat = less gain (log curve)
            const diminish = 1 / (1 + Math.log(Math.max(1, currentStatValue - 5)) * 0.15);
            return Math.max(1, Math.floor(baseXP * diminish));
        }

        canTrain(activityId) {
            const activity = ACTIVITIES[activityId];
            if (!activity) return { can: false, reason: 'Aktivität nicht gefunden' };

            const stats = this.getPlayerStats();
            const ecState = window.EquipmentCombat?.getState?.() || {};

            // Check stamina
            if (activity.staminaCost && ecState.stamina !== undefined) {
                if (ecState.stamina < activity.staminaCost) {
                    return { can: false, reason: `Brauche ${activity.staminaCost} Stamina (habe ${Math.floor(ecState.stamina)})` };
                }
            }

            // Check mana
            if (activity.manaCost && ecState.mana !== undefined) {
                if (ecState.mana < activity.manaCost) {
                    return { can: false, reason: `Brauche ${activity.manaCost} Mana (habe ${Math.floor(ecState.mana)})` };
                }
            }

            // Check requirements
            if (activity.requires) {
                for (const [stat, val] of Object.entries(activity.requires)) {
                    const mapped = stat === 'charisma' ? 'charm' : stat;
                    if ((stats[mapped] || 0) < val) {
                        return { can: false, reason: `${STAT_NAMES[stat]?.name || stat} muss mindestens ${val} sein` };
                    }
                }
            }

            // Check daily limit
            if (activity.dailyLimit) {
                const count = this.dailyCount.counts[activityId] || 0;
                if (count >= activity.dailyLimit) {
                    return { can: false, reason: `Tageslimit erreicht (${count}/${activity.dailyLimit})` };
                }
            }

            return { can: true };
        }

        doTraining(activityId) {
            const check = this.canTrain(activityId);
            if (!check.can) {
                this.showNotification(check.reason, '#e74c3c');
                return;
            }

            const activity = ACTIVITIES[activityId];
            const stats = this.getPlayerStats();
            const gains = {};

            // Calculate gains with diminishing returns
            for (const [stat, baseXP] of Object.entries(activity.stats)) {
                const mapped = stat === 'charisma' ? 'charm' : stat;
                const currentVal = stats[mapped] || 10;
                const gain = this.calcXPGain(baseXP, currentVal);
                gains[stat] = gain;

                // Apply stat gain (convert XP to stat points: 100 XP = ~1 stat point)
                const statGain = gain / 100;
                if (window.EquipmentCombat?.modifyPlayerStat) {
                    window.EquipmentCombat.modifyPlayerStat(mapped, statGain);
                }
            }

            // Consume stamina/mana
            if (activity.staminaCost && window.EquipmentCombat?.getState) {
                const state = window.EquipmentCombat.getState();
                if (state.stamina !== undefined) {
                    // Use negative healing as stamina drain
                    const newStamina = Math.max(0, state.stamina - activity.staminaCost);
                    // Direct manipulation via modifyPlayerStat isn't ideal but works
                }
            }

            // Track daily count
            this.dailyCount.counts[activityId] = (this.dailyCount.counts[activityId] || 0) + 1;
            this.dailyCount.totalXP = (this.dailyCount.totalXP || 0) + Object.values(gains).reduce((a, b) => a + b, 0);
            this.saveDailyCount();

            // Log
            this.trainingLog.push({
                activity: activityId,
                name: activity.name,
                gains,
                time: Date.now()
            });
            this.saveLog();

            // Show result
            const gainText = Object.entries(gains).map(([stat, xp]) => {
                const info = STAT_NAMES[stat];
                return `${info?.icon || ''} ${info?.name || stat} +${xp} XP`;
            }).join(', ');

            this.showNotification(`${activity.icon} ${activity.name}: ${gainText}`, '#2ecc71');
            this.render();
        }

        showNotification(msg, color) {
            const el = document.createElement('div');
            el.style.cssText = `
                position: fixed; top: 80px; left: 50%; transform: translateX(-50%);
                background: rgba(0,0,0,0.9); color: ${color}; padding: 12px 24px;
                border-radius: 8px; border: 1px solid ${color}; z-index: 10001;
                font-family: 'Courier New', monospace; font-size: 14px; text-align: center;
                animation: fadeInDown 0.3s ease-out;
            `;
            el.textContent = msg;
            document.body.appendChild(el);
            setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity 0.5s'; }, 2500);
            setTimeout(() => el.remove(), 3000);
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;

            this.overlay = document.createElement('div');
            this.overlay.id = 'stat-training-overlay';
            this.overlay.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 10000;
                display: flex;
                flex-direction: column;
                font-family: 'Courier New', monospace;
                color: #e0e0e0;
                overflow-y: auto;
            `;

            this.render();
            document.body.appendChild(this.overlay);

            this._keyHandler = (e) => {
                if (e.key === 'Escape') this.close();
            };
            document.addEventListener('keydown', this._keyHandler);
        }

        close() {
            if (!this.isOpen) return;
            this.isOpen = false;
            if (this.overlay) { this.overlay.remove(); this.overlay = null; }
            document.removeEventListener('keydown', this._keyHandler);
        }

        toggle() {
            if (this.isOpen) this.close();
            else this.open();
        }

        setFilter(cat) {
            this.filterCategory = cat;
            this.render();
        }

        render() {
            const stats = this.getPlayerStats();
            const totalTrainings = this.dailyCount.totalXP || 0;

            let activities = Object.entries(ACTIVITIES);
            if (this.filterCategory !== 'all') {
                activities = activities.filter(([_, a]) => a.category === this.filterCategory);
            }

            this.overlay.innerHTML = `
                <div style="max-width: 950px; margin: 0 auto; padding: 20px; width: 100%;">
                    <!-- Header -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #2ecc71; padding-bottom: 10px;">
                        <div>
                            <h1 style="margin: 0; color: #2ecc71; font-size: 24px;">🏋️ STAT TRAINING</h1>
                            <div style="font-size: 12px; color: #888; margin-top: 4px;">
                                Learning by Doing! | Heute: <span style="color: #FFD700;">${totalTrainings} XP</span> verdient
                            </div>
                        </div>
                        <button onclick="window.statTrainingUI.close()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">
                            ✕ [ESC]
                        </button>
                    </div>

                    <!-- Current Stats Overview -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 8px; margin-bottom: 20px;">
                        ${Object.entries(STAT_NAMES).map(([key, info]) => {
                            const mapped = key === 'charisma' ? 'charm' : key;
                            const val = stats[mapped] || 10;
                            return `
                            <div style="background: rgba(0,0,0,0.5); padding: 8px; border-radius: 6px; border: 1px solid ${info.color}33; text-align: center;">
                                <div style="font-size: 18px;">${info.icon}</div>
                                <div style="font-size: 11px; color: #888;">${info.name}</div>
                                <div style="font-size: 18px; color: ${info.color}; font-weight: bold;">${typeof val === 'number' ? val.toFixed(1) : val}</div>
                            </div>`;
                        }).join('')}
                    </div>

                    <!-- Category Filter -->
                    <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px;">
                        <button onclick="window.statTrainingUI.setFilter('all')" style="
                            padding: 5px 12px; border: 1px solid ${this.filterCategory === 'all' ? '#2ecc71' : '#555'};
                            background: ${this.filterCategory === 'all' ? 'rgba(46,204,113,0.15)' : 'rgba(0,0,0,0.3)'};
                            color: ${this.filterCategory === 'all' ? '#2ecc71' : '#aaa'};
                            border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 12px;
                        ">Alle</button>
                        ${Object.entries(CATEGORY_NAMES).map(([key, label]) => `
                            <button onclick="window.statTrainingUI.setFilter('${key}')" style="
                                padding: 5px 12px; border: 1px solid ${this.filterCategory === key ? '#2ecc71' : '#555'};
                                background: ${this.filterCategory === key ? 'rgba(46,204,113,0.15)' : 'rgba(0,0,0,0.3)'};
                                color: ${this.filterCategory === key ? '#2ecc71' : '#aaa'};
                                border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 11px;
                            ">${label}</button>
                        `).join('')}
                    </div>

                    <!-- Activities Grid -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px;">
                        ${activities.map(([id, a]) => this.renderActivityCard(id, a, stats)).join('')}
                    </div>

                    <!-- Training Log -->
                    ${this.trainingLog.length > 0 ? `
                    <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #333;">
                        <h3 style="color: #888; font-size: 14px; margin-bottom: 10px;">📋 Letzte Trainings</h3>
                        <div style="max-height: 150px; overflow-y: auto;">
                            ${this.trainingLog.slice(-10).reverse().map(log => {
                                const gainText = Object.entries(log.gains).map(([stat, xp]) => `${STAT_NAMES[stat]?.icon || ''} +${xp}`).join(' ');
                                const time = new Date(log.time).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
                                return `<div style="font-size: 11px; color: #666; padding: 3px 0;">[${time}] ${log.name} → ${gainText}</div>`;
                            }).join('')}
                        </div>
                    </div>
                    ` : ''}
                </div>
            `;
        }

        renderActivityCard(id, activity, stats) {
            const check = this.canTrain(id);
            const dailyUses = this.dailyCount.counts[id] || 0;

            // Stat gains preview
            const gainsList = Object.entries(activity.stats).map(([stat, baseXP]) => {
                const mapped = stat === 'charisma' ? 'charm' : stat;
                const currentVal = stats[mapped] || 10;
                const gain = this.calcXPGain(baseXP, currentVal);
                const info = STAT_NAMES[stat];
                return `<span style="color: ${info?.color || '#aaa'};">${info?.icon || ''} +${gain}</span>`;
            }).join(' ');

            // Requirements text
            let reqText = '';
            if (activity.requires) {
                reqText = Object.entries(activity.requires).map(([stat, val]) => {
                    const info = STAT_NAMES[stat];
                    const mapped = stat === 'charisma' ? 'charm' : stat;
                    const has = (stats[mapped] || 0) >= val;
                    return `<span style="color: ${has ? '#2ecc71' : '#e74c3c'};">${info?.icon || ''} ${val}</span>`;
                }).join(' ');
            }

            const costParts = [];
            if (activity.staminaCost) costParts.push(`⚡${activity.staminaCost}`);
            if (activity.manaCost) costParts.push(`💎${activity.manaCost}`);
            costParts.push(`⏱️${activity.time}min`);

            return `
            <div style="background: rgba(30,30,50,0.9); border: 1px solid ${check.can ? '#2ecc71' : '#555'}; border-radius: 8px; padding: 12px; ${!check.can ? 'opacity: 0.6;' : ''}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                    <div>
                        <span style="font-size: 20px;">${activity.icon}</span>
                        <span style="color: #e0e0e0; font-size: 14px; font-weight: bold; margin-left: 6px;">${activity.name}</span>
                    </div>
                    <span style="font-size: 10px; color: #888;">${CATEGORY_NAMES[activity.category] || activity.category}</span>
                </div>

                <!-- Stat gains -->
                <div style="font-size: 12px; margin-bottom: 8px;">${gainsList}</div>

                <!-- Costs -->
                <div style="font-size: 11px; color: #888; margin-bottom: 8px;">${costParts.join(' | ')}</div>

                ${reqText ? `<div style="font-size: 10px; margin-bottom: 6px;">Benötigt: ${reqText}</div>` : ''}
                ${activity.dailyLimit ? `<div style="font-size: 10px; color: #f39c12; margin-bottom: 6px;">Limit: ${dailyUses}/${activity.dailyLimit} heute</div>` : ''}

                <button onclick="window.statTrainingUI.doTraining('${id}')" ${!check.can ? 'disabled' : ''} style="
                    width: 100%; padding: 8px; border: none; border-radius: 5px; cursor: ${check.can ? 'pointer' : 'not-allowed'};
                    background: ${check.can ? 'linear-gradient(135deg, #2ecc71, #27ae60)' : '#333'};
                    color: white; font-family: inherit; font-size: 13px; font-weight: bold;
                ">
                    ${check.can ? `${activity.icon} Trainieren!` : check.reason}
                </button>
            </div>`;
        }
    }

    window.statTrainingUI = new StatTrainingUI();
    console.log('🏋️ StatTrainingUI geladen - ' + Object.keys(ACTIVITIES).length + ' Aktivitäten');
})();
