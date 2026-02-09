// ============================================================
// SURVIVAL HUD - Hunger/Durst/Energie + Gefahren-Anzeige
// Integration mit survival_system.js
// ============================================================
(function() {
    'use strict';

    class SurvivalHUD {
        constructor() {
            this.panel = null;
            this.detailOverlay = null;
            this.isDetailOpen = false;
            this.updateInterval = null;
            this.init();
        }

        init() {
            this.createMiniHUD();
            this.updateInterval = setInterval(() => this.updateMiniHUD(), 3000);
        }

        createMiniHUD() {
            this.panel = document.createElement('div');
            this.panel.id = 'survival-hud';
            this.panel.style.cssText = `
                position: fixed; top: 55px; right: 10px;
                background: rgba(0, 0, 0, 0.85); padding: 8px 12px;
                border-radius: 8px; border: 1px solid #555;
                font-family: 'Courier New', monospace; font-size: 11px;
                color: #ccc; z-index: 500; cursor: pointer;
                min-width: 140px;
            `;
            this.panel.onclick = () => this.toggleDetail();
            document.body.appendChild(this.panel);
            this.updateMiniHUD();
        }

        getData() {
            const ss = window.SurvivalSystem;
            if (!ss) return null;
            const needs = ss.getNeeds?.() || { hunger: 50, thirst: 50, energy: 50, hp: 100, maxHp: 100 };
            const mood = ss.getCurrentMood?.() || 50;
            const injuries = ss.getInjuries?.() || [];
            const diseases = ss.getDiseases?.() || [];
            const bounties = ss.getBounties?.() || {};
            const isWanted = ss.isWanted?.() || false;
            const moodlets = ss.getMoodlets?.() || [];
            return { needs, mood, injuries, diseases, bounties, isWanted, moodlets };
        }

        barColor(val) {
            if (val > 70) return '#2ecc71';
            if (val > 40) return '#f39c12';
            if (val > 20) return '#e67e22';
            return '#e74c3c';
        }

        miniBar(label, val, icon) {
            const color = this.barColor(val);
            const critical = val <= 20;
            return `
            <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 3px; ${critical ? 'animation: pulse 1s infinite;' : ''}">
                <span style="width: 16px;">${icon}</span>
                <div style="flex: 1; background: #1a1a2e; border-radius: 3px; height: 8px; overflow: hidden;">
                    <div style="background: ${color}; height: 100%; width: ${Math.max(0, Math.min(100, val))}%; transition: width 0.5s;"></div>
                </div>
                <span style="width: 28px; text-align: right; color: ${color}; font-size: 10px;">${Math.floor(val)}</span>
            </div>`;
        }

        updateMiniHUD() {
            const data = this.getData();
            if (!data) {
                this.panel.innerHTML = '<span style="color: #555;">⏳ Survival...</span>';
                return;
            }

            const { needs, mood, injuries, diseases, isWanted } = data;

            let alerts = '';
            if (isWanted) alerts += '<span style="color: #e74c3c;">🚨 GESUCHT</span> ';
            if (injuries.length > 0) alerts += `<span style="color: #e67e22;">🩹${injuries.length}</span> `;
            if (diseases.length > 0) alerts += `<span style="color: #9b59b6;">🤒${diseases.length}</span> `;

            const moodIcon = mood > 80 ? '😄' : mood > 60 ? '😊' : mood > 40 ? '😐' : mood > 20 ? '😞' : '😡';

            this.panel.innerHTML = `
                <div style="font-size: 10px; color: #888; margin-bottom: 4px; display: flex; justify-content: space-between;">
                    <span>SURVIVAL</span>
                    <span>${moodIcon} ${Math.floor(mood)}</span>
                </div>
                ${this.miniBar('Hunger', needs.hunger, '🍖')}
                ${this.miniBar('Durst', needs.thirst, '💧')}
                ${this.miniBar('Energie', needs.energy, '⚡')}
                ${alerts ? `<div style="font-size: 10px; margin-top: 3px;">${alerts}</div>` : ''}
            `;
        }

        toggleDetail() {
            if (this.isDetailOpen) this.closeDetail();
            else this.openDetail();
        }

        openDetail() {
            if (this.isDetailOpen) return;
            this.isDetailOpen = true;

            this.detailOverlay = document.createElement('div');
            this.detailOverlay.id = 'survival-detail-overlay';
            this.detailOverlay.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 10000;
                display: flex;
                flex-direction: column;
                font-family: 'Courier New', monospace;
                color: #e0e0e0;
                overflow-y: auto;
            `;

            this.renderDetail();
            document.body.appendChild(this.detailOverlay);

            this._keyHandler = (e) => { if (e.key === 'Escape') this.closeDetail(); };
            document.addEventListener('keydown', this._keyHandler);
        }

        closeDetail() {
            if (!this.isDetailOpen) return;
            this.isDetailOpen = false;
            if (this.detailOverlay) { this.detailOverlay.remove(); this.detailOverlay = null; }
            document.removeEventListener('keydown', this._keyHandler);
        }

        renderDetail() {
            const data = this.getData();
            if (!data) return;
            const { needs, mood, injuries, diseases, bounties, isWanted, moodlets } = data;
            const ss = window.SurvivalSystem;

            const moodIcon = mood > 80 ? '😄' : mood > 60 ? '😊' : mood > 40 ? '😐' : mood > 20 ? '😞' : '😡';

            this.detailOverlay.innerHTML = `
                <div style="max-width: 800px; margin: 0 auto; padding: 20px; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #e67e22; padding-bottom: 10px;">
                        <h1 style="margin: 0; color: #e67e22; font-size: 24px;">🏕️ SURVIVAL STATUS</h1>
                        <button onclick="window.survivalHUD.closeDetail()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">✕ [ESC]</button>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <!-- Linke Spalte: Bedürfnisse -->
                        <div>
                            <h3 style="color: #2ecc71; margin-bottom: 10px;">🍖 BEDÜRFNISSE</h3>
                            <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                                ${this.detailBar('Hunger', needs.hunger, '🍖', '#f39c12')}
                                ${this.detailBar('Durst', needs.thirst, '💧', '#3498db')}
                                ${this.detailBar('Energie', needs.energy, '⚡', '#f1c40f')}
                                ${this.detailBar('HP', (needs.hp / needs.maxHp) * 100, '❤️', '#e74c3c', `${needs.hp}/${needs.maxHp}`)}
                            </div>

                            <h3 style="color: #9b59b6; margin: 20px 0 10px;">${moodIcon} STIMMUNG: ${Math.floor(mood)}/100</h3>
                            <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                                <div style="background: #1a1a2e; border-radius: 4px; height: 20px; overflow: hidden; margin-bottom: 10px;">
                                    <div style="background: ${mood > 60 ? '#2ecc71' : mood > 30 ? '#f39c12' : '#e74c3c'}; height: 100%; width: ${mood}%;"></div>
                                </div>
                                ${moodlets.length > 0 ? moodlets.map(m => `
                                    <div style="display: flex; justify-content: space-between; font-size: 12px; padding: 3px 0; border-bottom: 1px solid #222;">
                                        <span>${m.icon || ''} ${m.name}</span>
                                        <span style="color: ${m.value > 0 ? '#2ecc71' : '#e74c3c'};">${m.value > 0 ? '+' : ''}${m.value}</span>
                                    </div>
                                `).join('') : '<div style="color: #555; font-size: 12px;">Keine aktiven Moodlets</div>'}
                                ${mood < 10 ? '<div style="color: #e74c3c; font-size: 12px; margin-top: 8px; font-weight: bold;">⚠️ MENTAL BREAK droht!</div>' : ''}
                                ${mood > 90 ? '<div style="color: #2ecc71; font-size: 12px; margin-top: 8px; font-weight: bold;">✨ INSPIRATION aktiv!</div>' : ''}
                            </div>
                        </div>

                        <!-- Rechte Spalte: Gesundheit & Gesetz -->
                        <div>
                            <h3 style="color: #e74c3c; margin-bottom: 10px;">🩹 VERLETZUNGEN (${injuries.length})</h3>
                            <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333; max-height: 150px; overflow-y: auto;">
                                ${injuries.length > 0 ? injuries.map(i => {
                                    const sevColors = { light: '#f39c12', medium: '#e67e22', heavy: '#e74c3c', critical: '#c0392b' };
                                    return `
                                    <div style="display: flex; justify-content: space-between; font-size: 12px; padding: 4px 0; border-bottom: 1px solid #222;">
                                        <span>${i.name}</span>
                                        <span style="color: ${sevColors[i.severity] || '#aaa'};">${i.severity}</span>
                                    </div>`;
                                }).join('') : '<div style="color: #555; font-size: 12px;">Keine Verletzungen</div>'}
                            </div>

                            <h3 style="color: #9b59b6; margin: 20px 0 10px;">🤒 KRANKHEITEN (${diseases.length})</h3>
                            <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                                ${diseases.length > 0 ? diseases.map(d => `
                                    <div style="font-size: 12px; padding: 4px 0; border-bottom: 1px solid #222;">
                                        <div>${d.name}</div>
                                        <div style="font-size: 10px; color: #888;">${d.effects ? Object.entries(d.effects).map(([k,v]) => `${k}: ${v}`).join(', ') : ''}</div>
                                    </div>
                                `).join('') : '<div style="color: #555; font-size: 12px;">Keine Krankheiten</div>'}
                            </div>

                            <h3 style="color: ${isWanted ? '#e74c3c' : '#2ecc71'}; margin: 20px 0 10px;">⚖️ GESETZ</h3>
                            <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid ${isWanted ? '#e74c3c' : '#333'};">
                                ${isWanted ? '<div style="color: #e74c3c; font-weight: bold; margin-bottom: 8px;">🚨 GESUCHT!</div>' : ''}
                                ${Object.keys(bounties).length > 0 ? Object.entries(bounties).map(([region, amount]) => `
                                    <div style="display: flex; justify-content: space-between; font-size: 12px; padding: 3px 0;">
                                        <span>${region}</span>
                                        <span style="color: #e74c3c;">${amount} Gold Kopfgeld</span>
                                    </div>
                                `).join('') : '<div style="color: #2ecc71; font-size: 12px;">Keine Kopfgelder - sauber!</div>'}
                            </div>
                        </div>
                    </div>

                    <!-- Quick Actions -->
                    <div style="margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap;">
                        <button onclick="window.SurvivalSystem?.eat?.({name:'Brot',hunger:20}); window.survivalHUD.renderDetail();" style="padding: 8px 16px; background: #f39c12; border: none; border-radius: 5px; color: white; cursor: pointer; font-family: inherit;">🍖 Essen</button>
                        <button onclick="window.SurvivalSystem?.drink?.({name:'Wasser',thirst:25}); window.survivalHUD.renderDetail();" style="padding: 8px 16px; background: #3498db; border: none; border-radius: 5px; color: white; cursor: pointer; font-family: inherit;">💧 Trinken</button>
                        <button onclick="window.SurvivalSystem?.sleep?.(4,{location:'tent_hidden'}); window.survivalHUD.renderDetail();" style="padding: 8px 16px; background: #2c3e50; border: none; border-radius: 5px; color: white; cursor: pointer; font-family: inherit;">😴 Schlafen (4h)</button>
                    </div>
                </div>
            `;
        }

        detailBar(label, val, icon, color, customText) {
            return `
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 3px;">
                    <span>${icon} ${label}</span>
                    <span style="color: ${this.barColor(val)};">${customText || Math.floor(val) + '%'}</span>
                </div>
                <div style="background: #1a1a2e; border-radius: 4px; height: 14px; overflow: hidden;">
                    <div style="background: ${color}; height: 100%; width: ${Math.max(0, Math.min(100, val))}%; transition: width 0.3s;"></div>
                </div>
            </div>`;
        }
    }

    window.survivalHUD = new SurvivalHUD();
    console.log('🏕️ SurvivalHUD geladen');
})();
