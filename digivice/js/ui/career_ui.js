// ============================================================
// CAREER UI - 24 Berufspfade mit Level/XP (M&B2 / Konosuba)
// Integration mit career_system.js
// ============================================================
(function() {
    'use strict';

    const CATEGORY_ICONS = {
        kampf: '⚔️', handwerk: '🔨', natur: '🌿', handel: '💰', sozial: '🎭', wissen: '📚'
    };

    class CareerUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.filterCategory = 'all';
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;
            this.overlay = document.createElement('div');
            this.overlay.id = 'career-overlay';
            this.overlay.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 10000; display: flex; flex-direction: column;
                font-family: 'Courier New', monospace; color: #e0e0e0; overflow-y: auto;
            `;
            this.render();
            document.body.appendChild(this.overlay);
            this._keyHandler = (e) => { if (e.key === 'Escape') this.close(); };
            document.addEventListener('keydown', this._keyHandler);
        }

        close() {
            if (!this.isOpen) return;
            this.isOpen = false;
            if (this.overlay) { this.overlay.remove(); this.overlay = null; }
            document.removeEventListener('keydown', this._keyHandler);
        }

        toggle() { this.isOpen ? this.close() : this.open(); }

        setFilter(cat) { this.filterCategory = cat; this.render(); }

        joinCareer(id) {
            const cs = window.CareerSystem;
            if (cs?.joinCareer) {
                cs.joinCareer(id);
                this.render();
            }
        }

        render() {
            const cs = window.CareerSystem;
            if (!cs) {
                this.overlay.innerHTML = '<div style="padding: 40px; text-align: center; color: #555;">CareerSystem nicht geladen</div>';
                return;
            }

            const allCareers = cs.getAllCareers?.() || [];
            const activeCareers = cs.getActiveCareers?.() || [];
            const categories = cs.CAREER_CATEGORIES || {};

            let careers = allCareers;
            if (this.filterCategory !== 'all') {
                careers = careers.filter(c => c.category === this.filterCategory);
            }

            // Sort: active first, then by level descending
            careers.sort((a, b) => {
                if (a.isActive !== b.isActive) return b.isActive ? 1 : -1;
                return (b.data?.level || 0) - (a.data?.level || 0);
            });

            this.overlay.innerHTML = `
                <div style="max-width: 950px; margin: 0 auto; padding: 20px; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #f39c12; padding-bottom: 10px;">
                        <div>
                            <h1 style="margin: 0; color: #f39c12; font-size: 24px;">🏛️ BERUFE & GILDEN</h1>
                            <div style="font-size: 12px; color: #888; margin-top: 4px;">
                                Aktive Berufe: <span style="color: #FFD700;">${activeCareers.length}</span> | Learning by Doing!
                            </div>
                        </div>
                        <button onclick="window.careerUI.close()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">✕ [ESC]</button>
                    </div>

                    <!-- Category Filter -->
                    <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px;">
                        <button onclick="window.careerUI.setFilter('all')" style="padding: 5px 12px; border: 1px solid ${this.filterCategory === 'all' ? '#f39c12' : '#555'}; background: ${this.filterCategory === 'all' ? 'rgba(243,156,18,0.15)' : 'rgba(0,0,0,0.3)'}; color: ${this.filterCategory === 'all' ? '#f39c12' : '#aaa'}; border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 12px;">Alle</button>
                        ${Object.entries(categories).map(([key, label]) => `
                            <button onclick="window.careerUI.setFilter('${key}')" style="padding: 5px 12px; border: 1px solid ${this.filterCategory === key ? '#f39c12' : '#555'}; background: ${this.filterCategory === key ? 'rgba(243,156,18,0.15)' : 'rgba(0,0,0,0.3)'}; color: ${this.filterCategory === key ? '#f39c12' : '#aaa'}; border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 11px;">${CATEGORY_ICONS[key] || ''} ${label || key}</button>
                        `).join('')}
                    </div>

                    <!-- Career Grid -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px;">
                        ${careers.map(c => this.renderCareerCard(c, cs)).join('')}
                    </div>
                </div>
            `;
        }

        renderCareerCard(career, cs) {
            const data = career.data || { level: 0, xp: 0, completedTasks: 0 };
            const isActive = career.isActive;
            const level = data.level || 0;
            const xp = data.xp || 0;
            const nextXP = cs.xpForLevel?.(level + 1) || 100;
            const xpPercent = nextXP > 0 ? Math.floor((xp / nextXP) * 100) : 0;
            const effectiveness = cs.calcEffectiveness?.(level) || 1;

            const levelColor = level >= 40 ? '#FFD700' : level >= 25 ? '#9b59b6' : level >= 10 ? '#3498db' : level >= 5 ? '#2ecc71' : '#aaa';

            return `
            <div style="background: rgba(30,30,50,0.9); border: 1px solid ${isActive ? career.color || '#f39c12' : '#333'}; border-radius: 8px; padding: 12px; ${isActive ? 'border-left: 3px solid ' + (career.color || '#f39c12') + ';' : ''}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                    <div>
                        <span style="font-size: 18px;">${career.icon || '🏛️'}</span>
                        <span style="color: ${career.color || '#ccc'}; font-size: 14px; font-weight: bold; margin-left: 4px;">${career.name}</span>
                    </div>
                    ${isActive ? `<span style="font-size: 10px; padding: 2px 6px; background: rgba(46,204,113,0.2); color: #2ecc71; border-radius: 3px; border: 1px solid #2ecc7144;">AKTIV</span>` : ''}
                </div>

                <div style="font-size: 11px; color: #888; margin-bottom: 8px;">${career.description || ''}</div>

                ${level > 0 ? `
                <div style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 3px;">
                        <span style="color: ${levelColor}; font-weight: bold;">Level ${level}</span>
                        <span style="color: #888;">${xp}/${nextXP} XP</span>
                    </div>
                    <div style="background: #1a1a2e; border-radius: 3px; height: 8px; overflow: hidden;">
                        <div style="background: ${career.color || '#f39c12'}; height: 100%; width: ${xpPercent}%;"></div>
                    </div>
                    <div style="font-size: 10px; color: #666; margin-top: 3px;">
                        Effektivität: ${(effectiveness * 100).toFixed(0)}% | Tasks: ${data.completedTasks || 0}
                    </div>
                </div>` : ''}

                ${career.levelEffects ? `
                <div style="font-size: 10px; color: #888; margin-bottom: 8px;">
                    ${Object.entries(career.levelEffects).slice(0, 3).map(([lvl, desc]) => `
                        <div style="color: ${level >= parseInt(lvl) ? '#2ecc71' : '#555'};">${level >= parseInt(lvl) ? '✅' : '🔒'} Lv${lvl}: ${desc}</div>
                    `).join('')}
                </div>` : ''}

                ${!isActive ? `
                <button onclick="window.careerUI.joinCareer('${career.id}')" style="width: 100%; padding: 8px; background: linear-gradient(135deg, #f39c12, #e67e22); border: none; border-radius: 5px; color: white; cursor: pointer; font-family: inherit; font-size: 12px; font-weight: bold;">Beruf beitreten</button>
                ` : ''}
            </div>`;
        }
    }

    window.careerUI = new CareerUI();
    console.log('🏛️ CareerUI geladen');
})();
