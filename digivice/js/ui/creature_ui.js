// ============================================================
// KREATUR UI - Zähmen, Anwerben, Farm-Übersicht
// 2 Kategorien: Kat.1 "Lebende" (Anwerben) + Kat.2 "Vieh" (Zähmen)
// ============================================================
(function() {
    'use strict';

    class CreatureUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.activeTab = 'companion';
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;
            this.overlay = document.createElement('div');
            this.overlay.id = 'creature-overlay';
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
        switchTab(tab) { this.activeTab = tab; this.render(); }

        renderTab(id, label) {
            const active = this.activeTab === id;
            return `<button onclick="window.creatureUI.switchTab('${id}')" style="
                padding: 10px 20px; border: 2px solid ${active ? '#00E676' : '#555'};
                background: ${active ? 'rgba(0,230,118,0.15)' : 'rgba(0,0,0,0.3)'};
                color: ${active ? '#00E676' : '#aaa'};
                border-radius: 8px 8px 0 0; cursor: pointer; font-family: inherit; font-size: 14px;
                font-weight: ${active ? 'bold' : 'normal'};
            ">${label}</button>`;
        }

        render() {
            const cs = window.CompanionSystem;
            const companionData = cs?.getCompanionData?.() || null;
            const state = cs?.getState?.() || {};

            this.overlay.innerHTML = `
                <div style="max-width: 900px; margin: 0 auto; padding: 20px; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #00E676; padding-bottom: 10px;">
                        <h1 style="margin: 0; color: #00E676; font-size: 24px;">🐾 KREATUREN & BEGLEITER</h1>
                        <button onclick="window.creatureUI.close()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">✕ [ESC]</button>
                    </div>

                    <div style="display: flex; gap: 5px; margin-bottom: 20px;">
                        ${this.renderTab('companion', '🐾 Begleiter')}
                        ${this.renderTab('forms', '🔄 Formen')}
                        ${this.renderTab('training', '💪 V-Pet Training')}
                        ${this.renderTab('farm', '🐄 Farm')}
                    </div>

                    <div id="creature-tab-content">
                        ${this.activeTab === 'companion' ? this.renderCompanionTab(companionData, state) : ''}
                        ${this.activeTab === 'forms' ? this.renderFormsTab(cs, state) : ''}
                        ${this.activeTab === 'training' ? this.renderTrainingTab(companionData, state, cs) : ''}
                        ${this.activeTab === 'farm' ? this.renderFarmTab() : ''}
                    </div>
                </div>
            `;
        }

        renderCompanionTab(data, state) {
            if (!data) {
                return `
                <div style="text-align: center; padding: 40px;">
                    <div style="font-size: 48px; margin-bottom: 20px;">🐾</div>
                    <div style="color: #888; font-size: 16px;">Kein Begleiter-System aktiv</div>
                    <div style="color: #555; font-size: 12px; margin-top: 10px;">CompanionSystem nicht geladen</div>
                </div>`;
            }

            const hearts = (n, max, icon, emptyIcon) => {
                let h = '';
                for (let i = 0; i < max; i++) h += i < n ? icon : emptyIcon;
                return h;
            };

            const trustNames = ['Fremd', 'Bekannt', 'Freund', 'Vertraut', 'Seelenverwandt', 'SEELENBUND'];
            const stageNames = ['Ei', 'Baby', 'Kind', 'Reif', 'Champion', 'Ultimativ'];
            const pathColors = { NORMAL: '#aaa', GOOD: '#2ecc71', PERFECT: '#FFD700', BAD: '#e74c3c' };

            return `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3 style="color: #00E676; margin-bottom: 10px;">🎭 MODUS: ${data.mode === 'kuja' ? 'KUJA (Mimik)' : 'STANDARD'}</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        <div style="font-size: 14px; margin-bottom: 10px;">
                            <span style="color: #FFD700;">Charakter:</span> ${data.character?.type || '?'}
                            ${data.character?.form ? ` → <span style="color: #00E676;">${data.character.form}</span>` : ''}
                        </div>
                        <div style="font-size: 14px; margin-bottom: 10px;">
                            <span style="color: #E91E63;">Begleiter:</span> ${data.companion?.name || '?'} (${data.companion?.type || '?'})
                        </div>
                        <div style="font-size: 12px; color: #888;">
                            ${data.training?.description || ''}
                        </div>
                    </div>

                    <h3 style="color: #9b59b6; margin: 20px 0 10px;">📊 EVOLUTION</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span>Stadium: <span style="color: #FFD700;">${stageNames[(data.stage || 1) - 1] || '?'}</span> (${data.stage || 1}/6)</span>
                            <span style="color: ${pathColors[data.path] || '#aaa'};">Pfad: ${data.path || 'NORMAL'}</span>
                        </div>
                        <div style="background: #1a1a2e; border-radius: 4px; height: 12px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #9b59b6, #FFD700); height: 100%; width: ${((data.stage || 1) / 6) * 100}%;"></div>
                        </div>
                    </div>
                </div>

                <div>
                    <h3 style="color: #e74c3c; margin-bottom: 10px;">❤️ V-PET CARE</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        <div style="margin-bottom: 10px;">
                            <span style="color: #f39c12;">Hunger:</span>
                            <span style="font-size: 18px; margin-left: 8px;">${hearts(data.hungerHearts || 0, 4, '❤️', '🖤')}</span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <span style="color: #e74c3c;">Stärke:</span>
                            <span style="font-size: 18px; margin-left: 8px;">${hearts(data.strengthHearts || 0, 4, '💪', '⚫')}</span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <span style="color: #2ecc71;">Effort:</span>
                            <span style="font-size: 18px; margin-left: 8px;">${hearts(Math.min(data.effortHearts || 0, 8), 8, '⭐', '☆')}</span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <span style="color: #3498db;">Vertrauen:</span>
                            <span style="color: #FFD700; font-weight: bold; margin-left: 8px;">${trustNames[(data.trustLevel || 1) - 1] || '?'} (${data.trustLevel || 1}/6)</span>
                        </div>
                    </div>

                    <div style="display: flex; gap: 8px; margin-top: 15px; flex-wrap: wrap;">
                        <button onclick="window.CompanionSystem?.feed?.(); window.creatureUI.render();" style="flex: 1; padding: 10px; background: #f39c12; border: none; border-radius: 5px; color: white; cursor: pointer; font-family: inherit; font-size: 13px;">🍖 Füttern</button>
                        <button onclick="window.CompanionSystem?.play?.(); window.creatureUI.render();" style="flex: 1; padding: 10px; background: #E91E63; border: none; border-radius: 5px; color: white; cursor: pointer; font-family: inherit; font-size: 13px;">🎮 Spielen</button>
                    </div>
                </div>
            </div>`;
        }

        renderFormsTab(cs, state) {
            const forms = cs?.getAvailableForms?.() || [];
            const currentForm = cs?.getCurrentForm?.() || null;
            const isKuja = cs?.isKujaMode?.() || false;

            const allForms = isKuja ? (cs?.MIMIK_FORMS || {}) : (cs?.SLIME_FORMS || {});

            return `
            <div>
                <h3 style="color: #00E676; margin-bottom: 10px;">${isKuja ? '🫠 MIMIK-FORMEN (Kuja wechselt selbst!)' : '🐾 SLIME-FORMEN (Begleiter wechselt!)'}</h3>
                ${currentForm ? `<div style="font-size: 14px; color: #FFD700; margin-bottom: 15px;">Aktuelle Form: ${currentForm.icon || ''} ${currentForm.name}</div>` : ''}

                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px;">
                    ${Object.entries(allForms).map(([id, form]) => {
                        const unlocked = forms.some(f => f.id === id);
                        const isCurrent = currentForm?.id === id;
                        return `
                        <div style="background: ${isCurrent ? 'rgba(0,230,118,0.15)' : 'rgba(30,30,50,0.9)'}; border: 1px solid ${isCurrent ? '#00E676' : unlocked ? '#555' : '#333'}; border-radius: 8px; padding: 12px; ${!unlocked ? 'opacity: 0.5;' : ''}">
                            <div style="font-size: 24px; text-align: center;">${form.icon || '❓'}</div>
                            <div style="text-align: center; font-size: 13px; color: ${unlocked ? '#e0e0e0' : '#555'}; font-weight: bold; margin: 5px 0;">${unlocked ? form.name : '???'}</div>
                            <div style="text-align: center; font-size: 10px; color: ${form.color || '#888'};">${unlocked ? (form.description || '') : 'Nicht freigeschaltet'}</div>
                            ${form.requirement ? `<div style="font-size: 10px; color: #888; text-align: center; margin-top: 5px;">Benötigt: ${Object.entries(form.requirement).map(([k,v]) => `${k}: ${v}`).join(', ')}</div>` : ''}
                            ${unlocked && !isCurrent ? `<button onclick="window.CompanionSystem?.changeForm?.('${id}'); window.creatureUI.render();" style="width: 100%; margin-top: 8px; padding: 6px; background: #00E676; border: none; border-radius: 4px; color: #000; cursor: pointer; font-family: inherit; font-size: 11px; font-weight: bold;">Wechseln</button>` : ''}
                        </div>`;
                    }).join('')}
                </div>
            </div>`;
        }

        renderTrainingTab(data, state, cs) {
            const trainingStats = state.trainingStats || {};
            const trainingTypes = [
                { key: 'kampf_training', name: 'Kampftraining', icon: '⚔️', color: '#e74c3c' },
                { key: 'stealth_training', name: 'Schleichtraining', icon: '🥷', color: '#2c3e50' },
                { key: 'kraft_training', name: 'Krafttraining', icon: '💪', color: '#e67e22' },
                { key: 'geschick_training', name: 'Geschicktraining', icon: '🎯', color: '#3498db' },
                { key: 'wild_training', name: 'Wildnistraining', icon: '🐺', color: '#27ae60' },
                { key: 'magie_training', name: 'Magietraining', icon: '🔮', color: '#9b59b6' }
            ];

            return `
            <div>
                <h3 style="color: #FFD700; margin-bottom: 15px;">💪 TRAINING (Formen freischalten!)</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 10px;">
                    ${trainingTypes.map(t => {
                        const val = trainingStats[t.key] || 0;
                        const percent = Math.min(100, (val / 50) * 100);
                        return `
                        <div style="background: rgba(30,30,50,0.9); border: 1px solid ${t.color}33; border-radius: 8px; padding: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="color: ${t.color}; font-size: 14px;">${t.icon} ${t.name}</span>
                                <span style="color: ${t.color}; font-weight: bold;">${val}</span>
                            </div>
                            <div style="background: #1a1a2e; border-radius: 3px; height: 10px; overflow: hidden;">
                                <div style="background: ${t.color}; height: 100%; width: ${percent}%;"></div>
                            </div>
                            <button onclick="window.CompanionSystem?.train?.('${t.key}'); window.creatureUI.render();" style="width: 100%; margin-top: 8px; padding: 8px; background: ${t.color}; border: none; border-radius: 4px; color: white; cursor: pointer; font-family: inherit; font-size: 12px; font-weight: bold;">${t.icon} Trainieren!</button>
                        </div>`;
                    }).join('')}
                </div>

                <div style="margin-top: 15px; font-size: 11px; color: #888;">
                    <div>Gesamt-Training: <span style="color: #FFD700;">${trainingStats.total_training || 0}</span></div>
                    <div>Training-Count: ${state.trainingCount || 0}</div>
                </div>
            </div>`;
        }
    }

    // Add renderFarmTab method
    CreatureUI.prototype.renderFarmTab = function() {
        const ct = window.CreatureTaming;
        const farmStatus = ct?.getFarmStatus?.() || null;
        const tamedCreatures = ct?.getTamedCreatures?.() || [];
        const farmAnimals = tamedCreatures.filter(c => c.role === 'farm' || c.type === 'livestock');

        if (!farmStatus && farmAnimals.length === 0) {
            return `
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 48px; margin-bottom: 20px;">🐄</div>
                <h3 style="color: #8BC34A;">FARM-TIERE</h3>
                <div style="color: #888; font-size: 14px; margin-top: 10px;">
                    Noch keine Farmtiere gezähmt!
                </div>
                <div style="color: #555; font-size: 12px; margin-top: 15px; max-width: 400px; margin-left: auto; margin-right: auto;">
                    Fange wilde Tiere in der Overworld und weise sie der Farm zu.
                    Farmtiere produzieren Ressourcen wie Milch, Eier oder Wolle.
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 25px; max-width: 500px; margin-left: auto; margin-right: auto;">
                    <div style="background: rgba(139,195,74,0.1); border: 1px solid rgba(139,195,74,0.2); border-radius: 8px; padding: 12px;">
                        <div style="font-size: 24px;">🐔</div>
                        <div style="font-size: 11px; color: #8BC34A; margin-top: 4px;">Huhn</div>
                        <div style="font-size: 9px; color: #888;">Eier</div>
                    </div>
                    <div style="background: rgba(139,195,74,0.1); border: 1px solid rgba(139,195,74,0.2); border-radius: 8px; padding: 12px;">
                        <div style="font-size: 24px;">🐄</div>
                        <div style="font-size: 11px; color: #8BC34A; margin-top: 4px;">Kuh</div>
                        <div style="font-size: 9px; color: #888;">Milch</div>
                    </div>
                    <div style="background: rgba(139,195,74,0.1); border: 1px solid rgba(139,195,74,0.2); border-radius: 8px; padding: 12px;">
                        <div style="font-size: 24px;">🐑</div>
                        <div style="font-size: 11px; color: #8BC34A; margin-top: 4px;">Schaf</div>
                        <div style="font-size: 9px; color: #888;">Wolle</div>
                    </div>
                </div>
            </div>`;
        }

        return `
        <div>
            <h3 style="color: #8BC34A; margin-bottom: 15px;">🐄 FARM-TIERE (${farmAnimals.length})</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 10px;">
                ${farmAnimals.map((animal, idx) => {
                    const icons = { chicken: '🐔', cow: '🐄', sheep: '🐑', pig: '🐷', goat: '🐐', horse: '🐴' };
                    const icon = icons[animal.species] || '🐾';
                    const hungry = (animal.hunger || 0) < 50;
                    const hasProduct = animal.productReady || false;
                    return `
                    <div style="background: rgba(30,30,50,0.9); border: 1px solid ${hasProduct ? '#FFD700' : '#333'}; border-radius: 8px; padding: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 28px;">${icon}</span>
                            <span style="font-size: 12px; color: ${hungry ? '#e74c3c' : '#4CAF50'};">${hungry ? '🍽️ Hungrig!' : '😊 Satt'}</span>
                        </div>
                        <div style="font-size: 13px; color: #e0e0e0; font-weight: bold;">${animal.name || animal.species}</div>
                        <div style="font-size: 10px; color: #888; margin-top: 2px;">Zufriedenheit: ${animal.happiness || 50}%</div>
                        <div style="display: flex; gap: 6px; margin-top: 10px;">
                            <button onclick="window.CreatureTaming?.feedFarmAnimal?.(${idx}); window.creatureUI.render();" style="flex:1; padding: 6px; background: #f39c12; border: none; border-radius: 4px; color: white; cursor: pointer; font-family: inherit; font-size: 11px;">🍖 Füttern</button>
                            <button onclick="window.CreatureTaming?.collectProduct?.(${idx}); window.creatureUI.render();" style="flex:1; padding: 6px; background: ${hasProduct ? '#FFD700' : '#555'}; border: none; border-radius: 4px; color: ${hasProduct ? '#000' : '#888'}; cursor: ${hasProduct ? 'pointer' : 'not-allowed'}; font-family: inherit; font-size: 11px;">${hasProduct ? '📦 Sammeln!' : '⏳ Warten...'}</button>
                        </div>
                    </div>`;
                }).join('')}
            </div>
            ${farmStatus ? `
            <div style="margin-top: 20px; background: rgba(139,195,74,0.08); border: 1px solid rgba(139,195,74,0.2); border-radius: 8px; padding: 15px;">
                <div style="font-size: 12px; color: #8BC34A; font-weight: bold; margin-bottom: 8px;">📊 Farm-Statistiken</div>
                <div style="font-size: 11px; color: #888;">Tiere gesamt: ${farmStatus.totalAnimals || 0}</div>
                <div style="font-size: 11px; color: #888;">Tägliche Produktion: ${farmStatus.dailyOutput || '???'}</div>
            </div>` : ''}
        </div>`;
    };

    window.creatureUI = new CreatureUI();
    console.log('🐾 CreatureUI geladen');
})();
