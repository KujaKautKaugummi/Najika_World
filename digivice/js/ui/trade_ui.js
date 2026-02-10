// ============================================================
// TRADE UI - Wirtschaftssimulation & Handel (M&B2 / Kenshi Style)
// Integration mit economy_system.js
// ============================================================
(function() {
    'use strict';

    const CATEGORY_META = {
        nahrung:  { name: 'Nahrung',    icon: '🍖', color: '#f39c12' },
        rohstoff: { name: 'Rohstoffe',  icon: '⛏️', color: '#95a5a6' },
        kraeuter: { name: 'Kräuter',    icon: '🌿', color: '#2ecc71' },
        waffen:   { name: 'Waffen',     icon: '⚔️', color: '#e74c3c' },
        illegal:  { name: 'Schmuggelware', icon: '🚫', color: '#c0392b' },
        luxus:    { name: 'Luxus',      icon: '💎', color: '#9b59b6' },
    };

    const REGION_ICONS = {
        samtmoos: '🍄', reich_der_drei: '🏰', heisse_duenen: '🏜️',
        salzwind: '⚓', magmastroeme: '🌋', gruenschlamm: '🐸',
        blitzebene: '⚡', tiefenhoehlen: '⛏️', goetterfels: '🏔️',
    };

    class TradeUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.activeTab = 'market';
            this.selectedRegion = null;
            this.filterCategory = 'all';
            this.buyQuantity = {};
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;
            this.overlay = document.createElement('div');
            this.overlay.id = 'trade-overlay';
            this.overlay.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 10000; display: flex; flex-direction: column;
                font-family: 'Courier New', monospace; color: #e0e0e0; overflow-y: auto;
            `;
            // Auto-detect current region
            if (!this.selectedRegion) {
                this.selectedRegion = this._detectCurrentRegion();
            }
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
        setRegion(region) { this.selectedRegion = region; this.render(); }
        setFilter(cat) { this.filterCategory = cat; this.render(); }

        _detectCurrentRegion() {
            if (window.Scene3D?.getCurrentBiome) return window.Scene3D.getCurrentBiome();
            if (window.currentBiome) return window.currentBiome;
            return 'reich_der_drei';
        }

        renderTab(id, label) {
            const active = this.activeTab === id;
            return `<button onclick="window.tradeUI.switchTab('${id}')" style="
                padding: 10px 20px; border: 2px solid ${active ? '#f39c12' : '#555'};
                background: ${active ? 'rgba(243,156,18,0.15)' : 'rgba(0,0,0,0.3)'};
                color: ${active ? '#f39c12' : '#aaa'};
                border-radius: 8px 8px 0 0; cursor: pointer; font-family: inherit; font-size: 14px;
                font-weight: ${active ? 'bold' : 'normal'};
            ">${label}</button>`;
        }

        render() {
            const es = window.EconomySystem;
            if (!es) {
                this.overlay.innerHTML = '<div style="padding: 40px; text-align: center; color: #555;">EconomySystem nicht geladen</div>';
                return;
            }

            this.overlay.innerHTML = `
                <div style="max-width: 1000px; margin: 0 auto; padding: 20px; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #f39c12; padding-bottom: 10px;">
                        <div>
                            <h1 style="margin: 0; color: #f39c12; font-size: 24px;">💰 HANDEL & WIRTSCHAFT</h1>
                            <div style="font-size: 11px; color: #888; margin-top: 4px;">
                                ${REGION_ICONS[this.selectedRegion] || '🗺️'} Aktueller Markt: <span style="color: #FFD700;">${es.REGIONAL_MARKETS[this.selectedRegion]?.name || this.selectedRegion}</span>
                            </div>
                        </div>
                        <button onclick="window.tradeUI.close()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">✕ [ESC]</button>
                    </div>

                    <div style="display: flex; gap: 5px; margin-bottom: 15px;">
                        ${this.renderTab('market', '🏪 Markt')}
                        ${this.renderTab('routes', '🗺️ Handelsrouten')}
                        ${this.renderTab('caravans', '🐫 Karawanen')}
                        ${this.renderTab('history', '📜 Handelslog')}
                    </div>

                    <div id="trade-tab-content">
                        ${this.activeTab === 'market' ? this.renderMarketTab(es) : ''}
                        ${this.activeTab === 'routes' ? this.renderRoutesTab(es) : ''}
                        ${this.activeTab === 'caravans' ? this.renderCaravansTab(es) : ''}
                        ${this.activeTab === 'history' ? this.renderHistoryTab(es) : ''}
                    </div>
                </div>
            `;
        }

        renderMarketTab(es) {
            const region = this.selectedRegion;
            const market = es.REGIONAL_MARKETS[region];
            const goods = es.GOODS;

            // Filter
            let filteredGoods = Object.entries(goods);
            if (this.filterCategory !== 'all') {
                filteredGoods = filteredGoods.filter(([, g]) => g.category === this.filterCategory);
            }

            return `
            <div>
                <!-- Region Selector -->
                <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px;">
                    ${Object.entries(es.REGIONAL_MARKETS).map(([id, m]) => `
                        <button onclick="window.tradeUI.setRegion('${id}')" style="
                            padding: 5px 10px; border: 1px solid ${region === id ? '#f39c12' : '#555'};
                            background: ${region === id ? 'rgba(243,156,18,0.15)' : 'rgba(0,0,0,0.3)'};
                            color: ${region === id ? '#f39c12' : '#aaa'};
                            border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 11px;
                        ">${REGION_ICONS[id] || ''} ${m.name.split(' ')[0]}</button>
                    `).join('')}
                </div>

                <!-- Market Info -->
                ${market ? `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                    <div style="background: rgba(46,204,113,0.1); border: 1px solid #2ecc7144; border-radius: 6px; padding: 10px;">
                        <div style="font-size: 11px; color: #2ecc71; font-weight: bold; margin-bottom: 5px;">📦 PRODUZIERT (billig!)</div>
                        <div style="font-size: 12px;">${market.produces.map(g => `${goods[g]?.icon || ''} ${goods[g]?.name || g}`).join(', ')}</div>
                    </div>
                    <div style="background: rgba(231,76,60,0.1); border: 1px solid #e74c3c44; border-radius: 6px; padding: 10px;">
                        <div style="font-size: 11px; color: #e74c3c; font-weight: bold; margin-bottom: 5px;">📈 NACHFRAGE (teuer!)</div>
                        <div style="font-size: 12px;">${market.demands.map(g => `${goods[g]?.icon || ''} ${goods[g]?.name || g}`).join(', ')}</div>
                    </div>
                </div>` : ''}

                <!-- Category Filter -->
                <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 12px;">
                    <button onclick="window.tradeUI.setFilter('all')" style="padding: 4px 10px; border: 1px solid ${this.filterCategory === 'all' ? '#f39c12' : '#555'}; background: ${this.filterCategory === 'all' ? 'rgba(243,156,18,0.15)' : 'rgba(0,0,0,0.3)'}; color: ${this.filterCategory === 'all' ? '#f39c12' : '#aaa'}; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 11px;">Alle</button>
                    ${Object.entries(CATEGORY_META).map(([key, meta]) => `
                        <button onclick="window.tradeUI.setFilter('${key}')" style="padding: 4px 10px; border: 1px solid ${this.filterCategory === key ? meta.color : '#555'}; background: ${this.filterCategory === key ? meta.color + '22' : 'rgba(0,0,0,0.3)'}; color: ${this.filterCategory === key ? meta.color : '#aaa'}; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 11px;">${meta.icon} ${meta.name}</button>
                    `).join('')}
                </div>

                <!-- Goods Table -->
                <div style="background: rgba(0,0,0,0.5); border-radius: 8px; border: 1px solid #333; overflow: hidden;">
                    <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1fr 120px; padding: 8px 12px; background: rgba(243,156,18,0.1); font-size: 11px; font-weight: bold; color: #f39c12; border-bottom: 1px solid #555;">
                        <span>Ware</span><span>Kaufen</span><span>Verkaufen</span><span>Basis</span><span>Vorrat</span><span>Aktion</span>
                    </div>
                    ${filteredGoods.map(([id, good]) => {
                        const buyPrice = es.getPrice(id, region, true);
                        const sellPrice = es.getPrice(id, region, false);
                        const supply = es.getSupplyLevel(region, id);
                        const isProduced = market?.produces?.includes(id);
                        const isDemanded = market?.demands?.includes(id);
                        const supplyColor = supply > 70 ? '#2ecc71' : supply > 40 ? '#f39c12' : supply > 20 ? '#e67e22' : '#e74c3c';
                        const catMeta = CATEGORY_META[good.category] || { color: '#888' };

                        return `
                        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1fr 120px; padding: 8px 12px; border-bottom: 1px solid #222; align-items: center; font-size: 12px; ${!good.legal ? 'background: rgba(192,57,43,0.08);' : ''}">
                            <div>
                                <span style="font-size: 14px;">${good.icon}</span>
                                <span style="color: ${catMeta.color}; margin-left: 4px;">${good.name}</span>
                                ${!good.legal ? '<span style="color: #e74c3c; font-size: 9px; margin-left: 4px;">⚠️ILLEGAL</span>' : ''}
                                ${isProduced ? '<span style="color: #2ecc71; font-size: 9px; margin-left: 4px;">▼</span>' : ''}
                                ${isDemanded ? '<span style="color: #e74c3c; font-size: 9px; margin-left: 4px;">▲</span>' : ''}
                            </div>
                            <span style="color: #e74c3c;">${buyPrice}g</span>
                            <span style="color: #2ecc71;">${sellPrice}g</span>
                            <span style="color: #666;">${good.basePrice}g</span>
                            <div>
                                <div style="background: #1a1a2e; border-radius: 2px; height: 6px; width: 50px; overflow: hidden; display: inline-block; vertical-align: middle;">
                                    <div style="background: ${supplyColor}; height: 100%; width: ${supply}%;"></div>
                                </div>
                                <span style="color: ${supplyColor}; font-size: 10px; margin-left: 2px;">${supply}</span>
                            </div>
                            <div style="display: flex; gap: 3px;">
                                <button onclick="window.tradeUI.executeBuy('${id}')" style="padding: 3px 8px; background: #27ae60; border: none; border-radius: 3px; color: white; cursor: pointer; font-family: inherit; font-size: 10px;">Kaufen</button>
                                <button onclick="window.tradeUI.executeSell('${id}')" style="padding: 3px 8px; background: #2980b9; border: none; border-radius: 3px; color: white; cursor: pointer; font-family: inherit; font-size: 10px;">Verkauf</button>
                            </div>
                        </div>`;
                    }).join('')}
                </div>

                ${market ? `
                <div style="display: flex; gap: 15px; margin-top: 12px; font-size: 11px; color: #888;">
                    <span>Illegale Toleranz: <span style="color: ${market.illegalTolerance > 0.5 ? '#2ecc71' : market.illegalTolerance > 0.2 ? '#f39c12' : '#e74c3c'};">${Math.round(market.illegalTolerance * 100)}%</span></span>
                    <span>▼ = Lokale Produktion (billig)</span>
                    <span>▲ = Nachfrage (teuer)</span>
                </div>` : ''}
            </div>`;
        }

        renderRoutesTab(es) {
            const region = this.selectedRegion;
            const routes = es.findBestTradeRoute(region);

            return `
            <div>
                <h3 style="color: #FFD700; margin-bottom: 10px;">🗺️ BESTE HANDELSROUTEN ab ${REGION_ICONS[region] || ''} ${es.REGIONAL_MARKETS[region]?.name || region}</h3>
                <div style="font-size: 11px; color: #888; margin-bottom: 15px;">Top 10 profitabelste Routen von deinem aktuellen Standort</div>

                <!-- Region Selector -->
                <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px;">
                    ${Object.entries(es.REGIONAL_MARKETS).map(([id, m]) => `
                        <button onclick="window.tradeUI.setRegion('${id}')" style="
                            padding: 4px 8px; border: 1px solid ${region === id ? '#FFD700' : '#555'};
                            background: ${region === id ? 'rgba(255,215,0,0.15)' : 'rgba(0,0,0,0.3)'};
                            color: ${region === id ? '#FFD700' : '#aaa'};
                            border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 11px;
                        ">${REGION_ICONS[id] || ''} ${m.name.split(' ')[0]}</button>
                    `).join('')}
                </div>

                ${routes.length > 0 ? `
                <div style="display: grid; gap: 8px;">
                    ${routes.map((r, i) => `
                    <div style="background: rgba(30,30,50,0.9); border: 1px solid ${r.legal ? '#FFD70033' : '#e74c3c33'}; border-left: 3px solid ${r.legal ? '#FFD700' : '#e74c3c'}; border-radius: 6px; padding: 10px; display: grid; grid-template-columns: auto 1fr auto; gap: 12px; align-items: center;">
                        <div style="text-align: center; min-width: 40px;">
                            <div style="font-size: 10px; color: #888;">#${i + 1}</div>
                            <div style="font-size: 20px;">${r.goodIcon}</div>
                        </div>
                        <div>
                            <div style="font-size: 13px; color: #e0e0e0; font-weight: bold;">
                                ${r.goodName} ${!r.legal ? '<span style="color: #e74c3c; font-size: 10px;">⚠️ ILLEGAL</span>' : ''}
                            </div>
                            <div style="font-size: 11px; color: #888; margin-top: 2px;">
                                ${REGION_ICONS[r.from] || ''} ${es.REGIONAL_MARKETS[r.from]?.name?.split(' ')[0] || r.from}
                                → ${REGION_ICONS[r.to] || ''} ${es.REGIONAL_MARKETS[r.to]?.name?.split(' ')[0] || r.to}
                            </div>
                            <div style="font-size: 11px; margin-top: 4px;">
                                Kaufen: <span style="color: #e74c3c;">${r.buyPrice}g</span> →
                                Verkaufen: <span style="color: #2ecc71;">${r.sellPrice}g</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 18px; color: #2ecc71; font-weight: bold;">+${r.profit}g</div>
                            <div style="font-size: 11px; color: ${r.profitPercent > 100 ? '#FFD700' : r.profitPercent > 50 ? '#2ecc71' : '#f39c12'};">+${r.profitPercent}%</div>
                        </div>
                    </div>`).join('')}
                </div>` : `
                <div style="text-align: center; padding: 30px; color: #555;">
                    Keine profitablen Routen von hier gefunden.
                </div>`}
            </div>`;
        }

        renderCaravansTab(es) {
            const caravans = es.getActiveCaravans();
            const routes = es.TRADE_ROUTES;

            return `
            <div>
                <h3 style="color: #e67e22; margin-bottom: 15px;">🐫 AKTIVE KARAWANEN (${caravans.length})</h3>

                ${caravans.length > 0 ? `
                <div style="display: grid; gap: 10px;">
                    ${caravans.map(c => {
                        const route = c.route;
                        const fromMarket = es.REGIONAL_MARKETS[route.from];
                        const toMarket = es.REGIONAL_MARKETS[route.to];
                        const dangerColor = route.danger > 0.4 ? '#e74c3c' : route.danger > 0.2 ? '#f39c12' : '#2ecc71';

                        return `
                        <div style="background: rgba(30,30,50,0.9); border: 1px solid #e67e2233; border-radius: 8px; padding: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <div style="font-size: 13px;">
                                    ${REGION_ICONS[route.from] || ''} <span style="color: #e0e0e0;">${fromMarket?.name || route.from}</span>
                                    <span style="color: #f39c12;"> → </span>
                                    ${REGION_ICONS[route.to] || ''} <span style="color: #e0e0e0;">${toMarket?.name || route.to}</span>
                                </div>
                                <span style="font-size: 11px; color: #888;">🛡️ ${c.guards} Wachen</span>
                            </div>
                            <div style="background: #1a1a2e; border-radius: 4px; height: 12px; overflow: hidden; margin-bottom: 6px;">
                                <div style="background: linear-gradient(90deg, #e67e22, #f39c12); height: 100%; width: ${Math.min(100, c.progress)}%; transition: width 0.5s;"></div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 11px;">
                                <span style="color: #888;">Waren: ${c.goods.map(g => `${es.GOODS[g.id]?.icon || ''} ${g.quantity}x`).join(', ')}</span>
                                <span>Gefahr: <span style="color: ${dangerColor};">${Math.round(route.danger * 100)}%</span> | ${Math.round(c.progress)}%</span>
                            </div>
                        </div>`;
                    }).join('')}
                </div>` : `
                <div style="text-align: center; padding: 30px; color: #555;">
                    <div style="font-size: 36px; margin-bottom: 10px;">🐫</div>
                    Keine Karawanen unterwegs
                </div>`}

                <h3 style="color: #3498db; margin: 25px 0 10px;">🛤️ HANDELSROUTEN (${routes.length})</h3>
                <div style="display: grid; gap: 6px;">
                    ${routes.map(r => {
                        const dangerColor = r.danger > 0.4 ? '#e74c3c' : r.danger > 0.2 ? '#f39c12' : '#2ecc71';
                        return `
                        <div style="background: rgba(30,30,50,0.6); border: 1px solid #333; border-radius: 6px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                            <div>
                                ${REGION_ICONS[r.from] || ''} ${es.REGIONAL_MARKETS[r.from]?.name?.split(' ')[0] || r.from}
                                <span style="color: #f39c12;"> → </span>
                                ${REGION_ICONS[r.to] || ''} ${es.REGIONAL_MARKETS[r.to]?.name?.split(' ')[0] || r.to}
                            </div>
                            <div style="font-size: 11px;">
                                Waren: ${r.goods.map(g => es.GOODS[g]?.icon || '📦').join(' ')}
                                | Gefahr: <span style="color: ${dangerColor};">${Math.round(r.danger * 100)}%</span>
                            </div>
                        </div>`;
                    }).join('')}
                </div>
            </div>`;
        }

        renderHistoryTab(es) {
            const state = es.getState();
            const history = (state.tradeHistory || []).slice().reverse().slice(0, 30);

            return `
            <div>
                <h3 style="color: #3498db; margin-bottom: 15px;">📜 HANDELSPROTOKOLL (letzte 30)</h3>

                ${history.length > 0 ? `
                <div style="background: rgba(0,0,0,0.5); border-radius: 8px; border: 1px solid #333; overflow: hidden;">
                    <div style="display: grid; grid-template-columns: 80px 1fr 1fr 100px 80px; padding: 8px 12px; background: rgba(52,152,219,0.1); font-size: 11px; font-weight: bold; color: #3498db; border-bottom: 1px solid #555;">
                        <span>Typ</span><span>Ware</span><span>Region</span><span>Preis</span><span>Menge</span>
                    </div>
                    ${history.map(h => {
                        const good = es.GOODS[h.good];
                        const market = es.REGIONAL_MARKETS[h.region];
                        const isBuy = h.type === 'buy';
                        const timeAgo = this._timeAgo(h.timestamp);
                        return `
                        <div style="display: grid; grid-template-columns: 80px 1fr 1fr 100px 80px; padding: 6px 12px; border-bottom: 1px solid #222; font-size: 12px; align-items: center;">
                            <span style="color: ${isBuy ? '#e74c3c' : '#2ecc71'}; font-weight: bold;">${isBuy ? '🛒 KAUF' : '💰 VERKAUF'}</span>
                            <span>${good?.icon || ''} ${good?.name || h.good}</span>
                            <span style="color: #888;">${REGION_ICONS[h.region] || ''} ${market?.name?.split(' ')[0] || h.region}</span>
                            <span style="color: ${isBuy ? '#e74c3c' : '#2ecc71'};">${isBuy ? '-' : '+'}${h.price}g</span>
                            <span style="color: #888;">${h.quantity}x</span>
                        </div>`;
                    }).join('')}
                </div>` : `
                <div style="text-align: center; padding: 30px; color: #555;">
                    Noch keine Trades getätigt
                </div>`}
            </div>`;
        }

        _timeAgo(timestamp) {
            const mins = Math.floor((Date.now() - timestamp) / 60000);
            if (mins < 1) return 'Gerade';
            if (mins < 60) return `${mins}m`;
            const hours = Math.floor(mins / 60);
            if (hours < 24) return `${hours}h`;
            return `${Math.floor(hours / 24)}d`;
        }

        executeBuy(goodId) {
            const es = window.EconomySystem;
            if (!es) return;
            const result = es.buyGood(goodId, this.selectedRegion, 1);
            if (result.success) {
                // Add to player inventory
                this._addToInventory(goodId, 1);
                this._showTradeNotification(`✅ ${result.good} gekauft für ${result.totalCost}g`, '#2ecc71');
                // GameEvent emittieren
                if (window.GameEvents) {
                    window.GameEvents.emit('itemPurchased', { itemId: goodId, price: result.totalCost, region: this.selectedRegion });
                }
            } else {
                this._showTradeNotification(`❌ ${result.reason}${result.caught ? ' Strafe: ' + result.penalty + 'g' : ''}`, '#e74c3c');
                if (result.caught && window.SurvivalSystem?.commitCrime) {
                    window.SurvivalSystem.commitCrime('schmuggel', this.selectedRegion);
                }
            }
            this.render();
        }

        executeSell(goodId) {
            const es = window.EconomySystem;
            if (!es) return;
            // Check if player has the item
            if (!this._hasInInventory(goodId)) {
                this._showTradeNotification(`❌ ${es.GOODS[goodId]?.name || goodId} nicht im Inventar!`, '#e74c3c');
                return;
            }
            const result = es.sellGood(goodId, this.selectedRegion, 1);
            if (result.success) {
                this._removeFromInventory(goodId, 1);
                this._showTradeNotification(`💰 ${result.good} verkauft für ${result.totalEarned}g`, '#2ecc71');
                // GameEvent emittieren
                if (window.GameEvents) {
                    window.GameEvents.emit('itemSold', { itemId: goodId, earned: result.totalEarned, region: this.selectedRegion });
                }
            } else {
                this._showTradeNotification(`❌ ${result.reason}${result.caught ? ' Strafe: ' + result.penalty + 'g' : ''}`, '#e74c3c');
                if (result.caught && window.SurvivalSystem?.commitCrime) {
                    window.SurvivalSystem.commitCrime('schmuggel', this.selectedRegion);
                }
            }
            this.render();
        }

        _addToInventory(goodId, qty) {
            try {
                const inv = JSON.parse(localStorage.getItem('najika_inventory') || '{}');
                inv[goodId] = (inv[goodId] || 0) + qty;
                localStorage.setItem('najika_inventory', JSON.stringify(inv));
            } catch {}
        }

        _removeFromInventory(goodId, qty) {
            try {
                const inv = JSON.parse(localStorage.getItem('najika_inventory') || '{}');
                inv[goodId] = Math.max(0, (inv[goodId] || 0) - qty);
                if (inv[goodId] <= 0) delete inv[goodId];
                localStorage.setItem('najika_inventory', JSON.stringify(inv));
            } catch {}
        }

        _hasInInventory(goodId) {
            try {
                const inv = JSON.parse(localStorage.getItem('najika_inventory') || '{}');
                return (inv[goodId] || 0) > 0;
            } catch { return false; }
        }

        _showTradeNotification(text, color) {
            const el = document.createElement('div');
            el.style.cssText = `
                position: fixed; top: 80px; right: 20px; z-index: 10001;
                background: rgba(0,0,0,0.9); border: 1px solid ${color};
                padding: 10px 18px; border-radius: 8px;
                color: ${color}; font-family: 'Courier New', monospace; font-size: 13px;
                animation: slideInRight 0.3s ease-out;
            `;
            el.textContent = text;
            document.body.appendChild(el);
            setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity 0.5s'; }, 2500);
            setTimeout(() => el.remove(), 3000);
        }
    }

    window.tradeUI = new TradeUI();
    console.log('💰 TradeUI geladen');
})();
