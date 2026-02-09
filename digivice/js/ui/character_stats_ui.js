// ============================================================
// CHARACTER STATS UI - Vollständiges Charakter-Sheet
// Zeigt Stats, Equipment, Skills, 1-Skill-Weg
// ============================================================
(function() {
    'use strict';

    class CharacterStatsUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.activeTab = 'stats';
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;

            this.overlay = document.createElement('div');
            this.overlay.id = 'character-stats-overlay';
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

            // ESC to close
            this._keyHandler = (e) => {
                if (e.key === 'Escape') this.close();
            };
            document.addEventListener('keydown', this._keyHandler);
        }

        close() {
            if (!this.isOpen) return;
            this.isOpen = false;
            if (this.overlay) {
                this.overlay.remove();
                this.overlay = null;
            }
            document.removeEventListener('keydown', this._keyHandler);
        }

        toggle() {
            if (this.isOpen) this.close();
            else this.open();
        }

        getData() {
            const ec = window.EquipmentCombat;
            const state = ec?.getState?.() || {};
            const stats = ec?.getPlayerStats?.() || {};
            const skills = ec?.getSkills?.() || {};
            const oneSkill = ec?.getOneSkillPath?.() || {};
            const weapons = ec?.getWeapons?.() || {};
            const armor = ec?.getArmor?.() || {};
            return { state, stats, skills, oneSkill, weapons, armor };
        }

        render() {
            const { state, stats, skills, oneSkill, weapons, armor } = this.getData();

            this.overlay.innerHTML = `
                <div style="max-width: 900px; margin: 0 auto; padding: 20px; width: 100%;">
                    <!-- Header -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">
                        <h1 style="margin: 0; color: #FFD700; font-size: 24px;">
                            ⚔️ CHARACTER SHEET
                        </h1>
                        <button onclick="window.characterStatsUI.close()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">
                            ✕ Schließen [ESC]
                        </button>
                    </div>

                    <!-- Tab Navigation -->
                    <div style="display: flex; gap: 5px; margin-bottom: 20px;">
                        ${this.renderTab('stats', '📊 Stats')}
                        ${this.renderTab('equipment', '🗡️ Equipment')}
                        ${this.renderTab('skills', '⚡ Skills')}
                    </div>

                    <!-- Tab Content -->
                    <div id="char-tab-content">
                        ${this.activeTab === 'stats' ? this.renderStatsTab(state, stats, oneSkill) : ''}
                        ${this.activeTab === 'equipment' ? this.renderEquipmentTab(state, weapons, armor) : ''}
                        ${this.activeTab === 'skills' ? this.renderSkillsTab(skills, oneSkill) : ''}
                    </div>
                </div>
            `;
        }

        renderTab(id, label) {
            const active = this.activeTab === id;
            return `<button onclick="window.characterStatsUI.switchTab('${id}')" style="
                padding: 10px 20px; border: 2px solid ${active ? '#FFD700' : '#555'};
                background: ${active ? 'rgba(255, 215, 0, 0.15)' : 'rgba(0,0,0,0.3)'};
                color: ${active ? '#FFD700' : '#aaa'};
                border-radius: 8px 8px 0 0; cursor: pointer; font-family: inherit; font-size: 14px;
                font-weight: ${active ? 'bold' : 'normal'};
            ">${label}</button>`;
        }

        switchTab(tab) {
            this.activeTab = tab;
            this.render();
        }

        // ==================== STATS TAB ====================
        renderStatsTab(state, stats, oneSkill) {
            const hpPercent = state.maxHp ? Math.floor((state.hp / state.maxHp) * 100) : 0;
            const staminaPercent = state.maxStamina ? Math.floor((state.stamina / state.maxStamina) * 100) : 0;
            const manaPercent = state.maxMana ? Math.floor((state.mana / state.maxMana) * 100) : 0;

            return `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <!-- Linke Spalte: Vitals -->
                <div>
                    <h3 style="color: #e74c3c; margin-bottom: 10px;">❤️ VITALS</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        ${this.renderBar('HP', state.hp || 0, state.maxHp || 100, '#e74c3c')}
                        ${this.renderBar('Stamina', state.stamina || 0, state.maxStamina || 100, '#2ecc71')}
                        ${this.renderBar('Mana', state.mana || 0, state.maxMana || 50, '#3498db')}
                    </div>

                    <h3 style="color: #9b59b6; margin: 20px 0 10px;">🎭 STATUS</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            ${(state.effects || []).length > 0
                                ? state.effects.map(e => `<span style="background: rgba(155,89,182,0.3); padding: 4px 8px; border-radius: 4px; font-size: 12px;">${e.type}</span>`).join('')
                                : '<span style="color: #666;">Keine Effekte aktiv</span>'
                            }
                        </div>
                        <div style="margin-top: 10px; font-size: 12px; color: #888;">
                            💥 Explosion heute: ${state.explosionUsedToday ? '❌ Verbraucht' : '✅ Verfügbar'}
                        </div>
                    </div>
                </div>

                <!-- Rechte Spalte: Attribute -->
                <div>
                    <h3 style="color: #FFD700; margin-bottom: 10px;">⚡ ATTRIBUTE</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        ${this.renderStat('💪 Stärke', stats.strength || 10, 'Physischer Schaden')}
                        ${this.renderStat('🧠 Intelligenz', stats.intelligence || 10, 'Magie-Schaden')}
                        ${this.renderStat('🏃 Agilität', stats.agility || 10, 'Dodge, Bewegung')}
                        ${this.renderStat('🛡️ Ausdauer', stats.endurance || 10, 'Max Stamina')}
                        ${this.renderStat('🍀 Glück', stats.luck || 10, 'Crits, Drops, Fischen')}
                        ${this.renderStat('✨ Charme', stats.charm || 10, 'NPCs, Preise')}
                    </div>

                    ${oneSkill?.active ? `
                    <h3 style="color: #e74c3c; margin: 20px 0 10px;">🔥 1-SKILL-WEG</h3>
                    <div style="background: rgba(231,76,60,0.15); padding: 15px; border-radius: 8px; border: 1px solid #e74c3c;">
                        <div style="font-size: 18px; color: #e74c3c; font-weight: bold;">
                            ${oneSkill.chosenSkill?.toUpperCase() || '???'}
                        </div>
                        <div style="font-size: 12px; color: #aaa; margin-top: 5px;">
                            +300% in ${oneSkill.chosenSkill}, -90% alle anderen
                        </div>
                        <div style="font-size: 11px; margin-top: 5px; color: ${oneSkill.confirmedPermanent ? '#e74c3c' : '#f39c12'};">
                            ${oneSkill.confirmedPermanent ? '🔒 PERMANENT' : '⏳ Temporär (Quest noch offen)'}
                        </div>
                    </div>
                    ` : ''}
                </div>
            </div>
            `;
        }

        renderBar(label, current, max, color) {
            const percent = max > 0 ? Math.floor((current / max) * 100) : 0;
            return `
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 3px;">
                    <span>${label}</span>
                    <span>${current}/${max}</span>
                </div>
                <div style="background: #1a1a2e; border-radius: 4px; height: 16px; overflow: hidden; border: 1px solid #333;">
                    <div style="background: ${color}; height: 100%; width: ${percent}%; transition: width 0.3s;"></div>
                </div>
            </div>`;
        }

        renderStat(label, value, desc) {
            const barWidth = Math.min(100, (value / 30) * 100);
            const color = value > 15 ? '#2ecc71' : value > 10 ? '#f39c12' : '#e74c3c';
            return `
            <div style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px;">
                    <span>${label}</span>
                    <span style="color: ${color}; font-weight: bold;">${value}</span>
                </div>
                <div style="background: #1a1a2e; border-radius: 3px; height: 6px; overflow: hidden; margin-top: 2px;">
                    <div style="background: ${color}; height: 100%; width: ${barWidth}%;"></div>
                </div>
                <div style="font-size: 10px; color: #666; margin-top: 1px;">${desc}</div>
            </div>`;
        }

        // ==================== EQUIPMENT TAB ====================
        renderEquipmentTab(state, weapons, armor) {
            const slots = [
                { key: 'rightHand', label: '🗡️ Rechte Hand', type: 'weapon' },
                { key: 'leftHand', label: '🛡️ Linke Hand', type: 'weapon' },
                { key: 'head', label: '🎩 Kopf', type: 'armor' },
                { key: 'body', label: '👕 Körper', type: 'armor' },
                { key: 'legs', label: '👖 Beine', type: 'armor' },
            ];

            return `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3 style="color: #3498db; margin-bottom: 10px;">🎒 AUSRÜSTUNG</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        ${slots.map(slot => this.renderEquipSlot(slot, state, weapons, armor)).join('')}
                    </div>
                </div>

                <div>
                    <h3 style="color: #e67e22; margin-bottom: 10px;">📋 WAFFEN-DETAILS</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333; max-height: 400px; overflow-y: auto;">
                        ${this.renderWeaponDetails(state.rightHand, weapons, 'Rechts')}
                        ${this.renderWeaponDetails(state.leftHand, weapons, 'Links')}
                    </div>

                    <h3 style="color: #2ecc71; margin: 20px 0 10px;">🛡️ RÜSTUNGS-DETAILS</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                        ${this.renderArmorSummary(state, armor)}
                    </div>
                </div>
            </div>
            `;
        }

        renderEquipSlot(slot, state, weapons, armor) {
            const itemId = state[slot.key];
            let itemName = 'Leer';
            let itemColor = '#555';

            if (itemId) {
                const db = slot.type === 'weapon' ? weapons : armor;
                const item = db?.[itemId];
                if (item) {
                    itemName = item.name || itemId;
                    const rarityColors = { common: '#aaa', uncommon: '#2ecc71', rare: '#3498db', epic: '#9b59b6', legendary: '#FFD700' };
                    itemColor = rarityColors[item.rarity] || '#aaa';
                } else {
                    itemName = itemId.replace(/_/g, ' ');
                }
            }

            return `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; margin-bottom: 6px; background: rgba(255,255,255,0.03); border-radius: 4px; border-left: 3px solid ${itemColor};">
                <span style="color: #888; font-size: 12px;">${slot.label}</span>
                <span style="color: ${itemColor}; font-size: 13px; font-weight: bold;">${itemName}</span>
            </div>`;
        }

        renderWeaponDetails(weaponId, weapons, hand) {
            if (!weaponId || !weapons?.[weaponId]) {
                return `<div style="color: #555; font-size: 12px; margin-bottom: 10px;">${hand}: Nichts ausgerüstet</div>`;
            }
            const w = weapons[weaponId];
            return `
            <div style="margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #333;">
                <div style="font-size: 14px; font-weight: bold; color: #e67e22;">${hand}: ${w.name}</div>
                <div style="font-size: 11px; color: #888; margin: 4px 0;">${w.type || 'Waffe'} | ${w.element || 'Physisch'}</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 12px; margin-top: 6px;">
                    <span>⚔️ Schaden: <span style="color: #e74c3c;">${w.damage || '?'}</span></span>
                    <span>📏 Reichweite: <span style="color: #3498db;">${w.range || '?'}</span></span>
                    <span>⚡ Speed: <span style="color: #f39c12;">${w.speed || '?'}</span></span>
                    <span>🎯 Crit: <span style="color: #FFD700;">${w.critChance ? (w.critChance * 100).toFixed(0) + '%' : '?'}</span></span>
                </div>
                ${w.special ? `<div style="font-size: 11px; color: #9b59b6; margin-top: 4px;">✨ ${w.special}</div>` : ''}
            </div>`;
        }

        renderArmorSummary(state, armor) {
            let totalDef = 0;
            const armorSlots = ['head', 'body', 'legs'];
            const parts = armorSlots.map(slot => {
                const itemId = state[slot];
                if (!itemId || !armor?.[itemId]) return null;
                const a = armor[itemId];
                totalDef += a.defense || 0;
                return `<div style="font-size: 12px; margin-bottom: 4px;">${a.name}: <span style="color: #2ecc71;">+${a.defense || 0} DEF</span></div>`;
            }).filter(Boolean);

            return `
                ${parts.length > 0 ? parts.join('') : '<div style="color: #555; font-size: 12px;">Keine Rüstung</div>'}
                <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #333; font-size: 14px; font-weight: bold;">
                    🛡️ Gesamt-Verteidigung: <span style="color: #2ecc71;">${totalDef}</span>
                </div>
            `;
        }

        // ==================== SKILLS TAB ====================
        renderSkillsTab(skills, oneSkill) {
            const categories = {
                '⚔️ WAFFEN': ['sword', 'dagger', 'axe', 'hammer', 'spear', 'staff', 'shield', 'fist', 'bow', 'club'],
                '🤠 WESTERN': ['gun', 'rifle', 'shotgun', 'whip', 'lasso'],
                '🥊 KAMPF': ['dodge', 'parry', 'block', 'combo', 'grab', 'throw', 'suplex', 'environment'],
                '🔥 ZERSTÖRUNG': ['fire', 'ice', 'lightning'],
                '✨ MAGIE': ['restoration', 'illusion', 'conjuration', 'alteration', 'necromancy', 'poison', 'water', 'shadow', 'arcane'],
                '💥 EXPLOSION': ['explosion']
            };

            let html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">';

            for (const [catName, skillList] of Object.entries(categories)) {
                html += `
                <div>
                    <h3 style="color: #FFD700; margin-bottom: 10px; font-size: 14px;">${catName}</h3>
                    <div style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 8px; border: 1px solid #333;">
                `;

                for (const skillId of skillList) {
                    const skill = skills[skillId];
                    if (!skill) continue;

                    const xpPercent = skill.xpNeeded > 0 ? Math.floor((skill.xp / skill.xpNeeded) * 100) : 0;
                    const isOneSkill = oneSkill?.active && oneSkill?.chosenSkill === skillId;
                    const nameColor = isOneSkill ? '#e74c3c' : skillId === 'explosion' ? '#ff6600' : '#ccc';
                    const levelColor = skill.level >= 10 ? '#FFD700' : skill.level >= 5 ? '#2ecc71' : '#aaa';

                    html += `
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; padding: 4px; ${isOneSkill ? 'background: rgba(231,76,60,0.1); border-radius: 4px;' : ''}">
                        <span style="color: ${nameColor}; font-size: 12px; width: 90px; text-transform: capitalize;">${skillId}</span>
                        <span style="color: ${levelColor}; font-weight: bold; font-size: 13px; width: 30px; text-align: center;">Lv${skill.level}</span>
                        <div style="flex: 1; background: #1a1a2e; border-radius: 3px; height: 8px; overflow: hidden;">
                            <div style="background: ${skillId === 'explosion' ? '#ff6600' : '#3498db'}; height: 100%; width: ${xpPercent}%;"></div>
                        </div>
                        <span style="color: #666; font-size: 10px; width: 45px; text-align: right;">${skill.xp}/${skill.xpNeeded}</span>
                    </div>`;
                }

                html += `</div></div>`;
            }

            html += '</div>';
            return html;
        }
    }

    // Global instance
    window.characterStatsUI = new CharacterStatsUI();

    console.log('📊 CharacterStatsUI geladen');
})();
