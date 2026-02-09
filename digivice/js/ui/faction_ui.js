// ============================================================
// FACTION UI - 12+ Fraktionen mit Fame/Infamy (Fallout NV Style)
// Integration mit faction_system.js
// ============================================================
(function() {
    'use strict';

    class FactionUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.selectedFaction = null;
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;
            this.overlay = document.createElement('div');
            this.overlay.id = 'faction-overlay';
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

        selectFaction(id) {
            this.selectedFaction = id;
            this.render();
        }

        getRepLevelName(fame) {
            if (fame >= 100) return { name: 'Vergöttert', icon: '👑', color: '#FFD700' };
            if (fame >= 75) return { name: 'Verehrt', icon: '🏆', color: '#9b59b6' };
            if (fame >= 50) return { name: 'Bewundert', icon: '⭐', color: '#3498db' };
            if (fame >= 25) return { name: 'Geschätzt', icon: '😊', color: '#2ecc71' };
            if (fame >= 10) return { name: 'Akzeptiert', icon: '👋', color: '#f39c12' };
            return { name: 'Unbekannt', icon: '❓', color: '#666' };
        }

        getInfamyLevelName(infamy) {
            if (infamy >= 100) return { name: 'NEMESIS', icon: '☠️', color: '#c0392b' };
            if (infamy >= 75) return { name: 'Erzfeind', icon: '💀', color: '#e74c3c' };
            if (infamy >= 50) return { name: 'Feind', icon: '⚔️', color: '#e67e22' };
            if (infamy >= 25) return { name: 'Unerwünscht', icon: '🚫', color: '#f39c12' };
            if (infamy >= 10) return { name: 'Verdächtig', icon: '👀', color: '#888' };
            return { name: 'Neutral', icon: '➖', color: '#555' };
        }

        render() {
            const fs = window.FactionSystem;
            if (!fs) {
                this.overlay.innerHTML = '<div style="padding: 40px; text-align: center; color: #555;">FactionSystem nicht geladen</div>';
                return;
            }

            const factions = fs.FACTIONS || {};
            const allReps = fs.getAllReputations?.() || {};
            const wars = fs.getActiveWars?.() || [];

            this.overlay.innerHTML = `
                <div style="max-width: 950px; margin: 0 auto; padding: 20px; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #9b59b6; padding-bottom: 10px;">
                        <h1 style="margin: 0; color: #9b59b6; font-size: 24px;">⚔️ FRAKTIONEN</h1>
                        <button onclick="window.factionUI.close()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">✕ [ESC]</button>
                    </div>

                    ${wars.length > 0 ? `
                    <div style="background: rgba(231,76,60,0.15); border: 1px solid #e74c3c; border-radius: 8px; padding: 10px; margin-bottom: 15px;">
                        <div style="font-size: 12px; color: #e74c3c; font-weight: bold; margin-bottom: 5px;">⚔️ AKTIVE KRIEGE</div>
                        ${wars.map(w => `<div style="font-size: 11px; color: #e74c3c;">${factions[w.attacker]?.name || w.attacker} vs ${factions[w.defender]?.name || w.defender}</div>`).join('')}
                    </div>` : ''}

                    <div style="display: grid; grid-template-columns: 1fr ${this.selectedFaction ? '1fr' : ''}; gap: 20px;">
                        <!-- Faction List -->
                        <div>
                            <div style="display: grid; grid-template-columns: 1fr; gap: 8px;">
                                ${Object.entries(factions).map(([id, f]) => {
                                    const rep = allReps[id] || { fame: 0, infamy: 0 };
                                    const fameLevel = this.getRepLevelName(rep.fame);
                                    const infamyLevel = this.getInfamyLevelName(rep.infamy);
                                    const selected = this.selectedFaction === id;
                                    return `
                                    <div onclick="window.factionUI.selectFaction('${id}')" style="
                                        background: ${selected ? 'rgba(155,89,182,0.2)' : 'rgba(30,30,50,0.9)'};
                                        border: 1px solid ${selected ? '#9b59b6' : f.color || '#555'};
                                        border-left: 3px solid ${f.color || '#555'};
                                        border-radius: 6px; padding: 10px; cursor: pointer;
                                    ">
                                        <div style="display: flex; justify-content: space-between; align-items: center;">
                                            <span style="font-size: 14px; color: ${f.color || '#ccc'}; font-weight: bold;">${f.icon || ''} ${f.name}</span>
                                            <div style="font-size: 11px;">
                                                <span style="color: ${fameLevel.color};">${fameLevel.icon} ${Math.floor(rep.fame)}</span>
                                                ${rep.infamy > 5 ? `<span style="color: ${infamyLevel.color}; margin-left: 6px;">${infamyLevel.icon} ${Math.floor(rep.infamy)}</span>` : ''}
                                            </div>
                                        </div>
                                        <div style="display: flex; gap: 4px; margin-top: 4px;">
                                            <div style="flex: 1; background: #1a1a2e; border-radius: 2px; height: 4px; overflow: hidden;">
                                                <div style="background: ${fameLevel.color}; height: 100%; width: ${Math.min(100, rep.fame)}%;"></div>
                                            </div>
                                            <div style="flex: 1; background: #1a1a2e; border-radius: 2px; height: 4px; overflow: hidden;">
                                                <div style="background: ${infamyLevel.color}; height: 100%; width: ${Math.min(100, rep.infamy)}%;"></div>
                                            </div>
                                        </div>
                                        <div style="font-size: 10px; color: #666; margin-top: 3px;">${f.region || ''} | ${f.category || ''}</div>
                                    </div>`;
                                }).join('')}
                            </div>
                        </div>

                        ${this.selectedFaction ? this.renderFactionDetail(factions[this.selectedFaction], allReps[this.selectedFaction] || { fame: 0, infamy: 0 }) : ''}
                    </div>
                </div>
            `;
        }

        renderFactionDetail(f, rep) {
            if (!f) return '';
            const fameLevel = this.getRepLevelName(rep.fame);
            const infamyLevel = this.getInfamyLevelName(rep.infamy);

            return `
            <div>
                <div style="background: rgba(30,30,50,0.9); border: 1px solid ${f.color || '#555'}; border-radius: 8px; padding: 15px;">
                    <h2 style="color: ${f.color || '#ccc'}; margin: 0 0 10px;">${f.icon || ''} ${f.name}</h2>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center;">
                            <div style="font-size: 10px; color: #888;">FAME</div>
                            <div style="font-size: 24px; color: ${fameLevel.color};">${fameLevel.icon}</div>
                            <div style="font-size: 13px; color: ${fameLevel.color}; font-weight: bold;">${fameLevel.name}</div>
                            <div style="font-size: 11px; color: #888;">${Math.floor(rep.fame)}/100</div>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center;">
                            <div style="font-size: 10px; color: #888;">INFAMY</div>
                            <div style="font-size: 24px; color: ${infamyLevel.color};">${infamyLevel.icon}</div>
                            <div style="font-size: 13px; color: ${infamyLevel.color}; font-weight: bold;">${infamyLevel.name}</div>
                            <div style="font-size: 11px; color: #888;">${Math.floor(rep.infamy)}/100</div>
                        </div>
                    </div>

                    ${f.lightSide ? `<div style="font-size: 11px; margin-bottom: 5px;"><span style="color: #2ecc71;">✅ Licht:</span> ${f.lightSide}</div>` : ''}
                    ${f.darkSide ? `<div style="font-size: 11px; margin-bottom: 10px;"><span style="color: #e74c3c;">❌ Dunkel:</span> ${f.darkSide}</div>` : ''}

                    ${f.allies?.length ? `<div style="font-size: 11px; margin-bottom: 5px;"><span style="color: #3498db;">Verbündete:</span> ${f.allies.join(', ')}</div>` : ''}
                    ${f.enemies?.length ? `<div style="font-size: 11px; margin-bottom: 5px;"><span style="color: #e74c3c;">Feinde:</span> ${f.enemies.join(', ')}</div>` : ''}
                    ${f.values?.length ? `<div style="font-size: 11px; margin-bottom: 5px;"><span style="color: #FFD700;">Werte:</span> ${f.values.join(', ')}</div>` : ''}
                </div>
            </div>`;
        }
    }

    window.factionUI = new FactionUI();
    console.log('⚔️ FactionUI geladen');
})();
