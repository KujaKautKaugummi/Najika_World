/**
 * NAJIKA WORLD - ECONOMY & TRADE SIMULATION
 * ==========================================
 * Mount & Blade 2 / Kenshi Style Wirtschaft.
 * Angebot & Nachfrage. Handelsrouten. Schmuggel.
 *
 * - Jede Stadt/Region hat eigene Preise
 * - Preise ändern sich durch Events, Kriege, tote Händler
 * - Spieler kann Handelsrouten ausnutzen (billig kaufen, teuer verkaufen)
 * - Schmuggel: Verbotene Waren = hoher Profit, hohes Risiko
 * - Karawanen reisen zwischen Städten (können überfallen werden!)
 * - Ressourcen-Knappheit durch Wetter/Krieg/Events
 */

(function() {
    'use strict';

    // ==========================================
    // WAREN & BASISPREISE
    // ==========================================

    const GOODS = {
        // NAHRUNG
        brot:          { name: 'Brot',              icon: '🍞', basePrice: 5,    category: 'nahrung',   weight: 0.5, legal: true },
        fleisch:       { name: 'Fleisch',            icon: '🥩', basePrice: 12,   category: 'nahrung',   weight: 1,   legal: true },
        fisch:         { name: 'Fisch',              icon: '🐟', basePrice: 8,    category: 'nahrung',   weight: 0.8, legal: true },
        kraeuterbier:  { name: 'Kräuterbier',        icon: '🍺', basePrice: 15,   category: 'nahrung',   weight: 1,   legal: true },
        buff_mahl:     { name: 'Buff-Festmahl',      icon: '🍖', basePrice: 80,   category: 'nahrung',   weight: 2,   legal: true },

        // ROHSTOFFE
        holz:          { name: 'Holz',               icon: '🪵', basePrice: 8,    category: 'rohstoff',  weight: 3,   legal: true },
        erz:           { name: 'Eisenerz',           icon: '⛏️', basePrice: 15,   category: 'rohstoff',  weight: 4,   legal: true },
        stein:         { name: 'Stein',              icon: '🪨', basePrice: 5,    category: 'rohstoff',  weight: 5,   legal: true },
        leder:         { name: 'Leder',              icon: '🟤', basePrice: 20,   category: 'rohstoff',  weight: 1.5, legal: true },
        root_fiber:    { name: 'Wurzelfaser',        icon: '🌱', basePrice: 10,   category: 'rohstoff',  weight: 0.3, legal: true },

        // KRAUTER & ALCHEMIE
        heilkraut:     { name: 'Heilkraut',          icon: '🌿', basePrice: 18,   category: 'kraeuter',  weight: 0.2, legal: true },
        giftpilz:      { name: 'Giftpilz',           icon: '🍄', basePrice: 25,   category: 'kraeuter',  weight: 0.2, legal: false }, // ILLEGAL in Silberdorn!
        mondblume:     { name: 'Mondblume',           icon: '🌸', basePrice: 40,   category: 'kraeuter',  weight: 0.1, legal: true },
        sumpfessenz:   { name: 'Sumpfessenz',         icon: '🧪', basePrice: 60,   category: 'kraeuter',  weight: 0.3, legal: false },

        // WAFFEN & RÜSTUNGEN
        eisenschwert:  { name: 'Eisenschwert',        icon: '⚔️', basePrice: 100,  category: 'waffen',    weight: 3,   legal: true },
        stahlschild:   { name: 'Stahlschild',         icon: '🛡️', basePrice: 80,   category: 'waffen',    weight: 4,   legal: true },
        magmaklinge:   { name: 'Magmaklinge',         icon: '🔥', basePrice: 500,  category: 'waffen',    weight: 3,   legal: true },

        // SCHMUGGELWARE (HOHER PROFIT, HOHE STRAFE!)
        organprobe:    { name: 'Organprobe',          icon: '🫀', basePrice: 300,  category: 'illegal',   weight: 0.5, legal: false },
        verbotenes_buch: { name: 'Verbotenes Buch',   icon: '📕', basePrice: 200,  category: 'illegal',   weight: 0.5, legal: false },
        schlafgift:    { name: 'Schlafgift',          icon: '💧', basePrice: 150,  category: 'illegal',   weight: 0.2, legal: false },
        gefaelschte_papiere: { name: 'Gefälschte Papiere', icon: '📄', basePrice: 100, category: 'illegal', weight: 0.1, legal: false },

        // LUXUSGÜTER
        gold_barren:   { name: 'Goldbarren',          icon: '🪙', basePrice: 500,  category: 'luxus',     weight: 2,   legal: true },
        edelstein:     { name: 'Edelstein',           icon: '💎', basePrice: 300,  category: 'luxus',     weight: 0.3, legal: true },
        seide:         { name: 'Seide',               icon: '🧵', basePrice: 80,   category: 'luxus',     weight: 0.5, legal: true },
    };

    // ==========================================
    // REGIONALE MÄRKTE (Angebot & Nachfrage)
    // ==========================================

    const REGIONAL_MARKETS = {
        samtmoos: {
            name: 'Samtmoos Markt',
            produces: ['holz', 'heilkraut', 'root_fiber', 'mondblume'],  // Billig hier
            demands:  ['eisenschwert', 'erz', 'fleisch'],                 // Teuer hier
            productionBonus: 0.7,   // Produziertes: 70% vom Basispreis
            demandPenalty: 1.4,     // Nachgefragtes: 140% vom Basispreis
            illegalTolerance: 0.3,  // 30% Chance dass illegale Waren toleriert
        },
        reich_der_drei: {
            name: 'Markt der Drei Häuser',
            produces: ['eisenschwert', 'stahlschild', 'brot', 'seide'],
            demands:  ['erz', 'holz', 'heilkraut', 'leder'],
            productionBonus: 0.6,
            demandPenalty: 1.5,
            illegalTolerance: 0.1,  // Streng!
        },
        heisse_duenen: {
            name: 'Dünenbasar',
            produces: ['edelstein', 'seide', 'giftpilz'],
            demands:  ['holz', 'fisch', 'heilkraut', 'brot'],
            productionBonus: 0.65,
            demandPenalty: 1.6,    // Wasser und Nahrung sind Gold wert!
            illegalTolerance: 0.5,  // Tolerant
        },
        salzwind: {
            name: 'Hafenmarkt Salzwind',
            produces: ['fisch', 'seide', 'gold_barren'],
            demands:  ['holz', 'erz', 'fleisch', 'heilkraut'],
            productionBonus: 0.6,
            demandPenalty: 1.3,
            illegalTolerance: 0.4,
        },
        magmastroeme: {
            name: 'Schmiede-Markt',
            produces: ['magmaklinge', 'eisenschwert', 'stahlschild', 'erz'],
            demands:  ['brot', 'fisch', 'heilkraut', 'holz', 'leder'],
            productionBonus: 0.5,   // Hier sind Waffen billig!
            demandPenalty: 1.8,     // Essen ist hier verdammt teuer
            illegalTolerance: 0.3,
        },
        gruenschlamm: {
            name: 'Sumpfmarkt',
            produces: ['heilkraut', 'giftpilz', 'sumpfessenz', 'mondblume'],
            demands:  ['brot', 'fleisch', 'eisenschwert', 'stein'],
            productionBonus: 0.5,
            demandPenalty: 1.5,
            illegalTolerance: 0.7,   // Hier ist fast alles erlaubt
        },
        blitzebene: {
            name: 'Blitzmarkt',
            produces: ['leder', 'fleisch'],
            demands:  ['holz', 'stein', 'eisenschwert', 'heilkraut'],
            productionBonus: 0.7,
            demandPenalty: 1.4,
            illegalTolerance: 0.3,
        },
        tiefenhoehlen: {
            name: 'Unterirdischer Markt',
            produces: ['erz', 'stein', 'edelstein'],
            demands:  ['brot', 'holz', 'heilkraut', 'leder', 'fisch'],
            productionBonus: 0.5,   // Erze spottbillig
            demandPenalty: 2.0,     // Nahrung extrem teuer
            illegalTolerance: 0.6,
        },
        goetterfels: {
            name: 'Pilger-Markt',
            produces: ['mondblume', 'heilkraut'],
            demands:  ['brot', 'fleisch', 'seide', 'edelstein'],
            productionBonus: 0.8,
            demandPenalty: 1.3,
            illegalTolerance: 0.05, // Fast null Toleranz!
        },
    };

    // ==========================================
    // KARAWANEN (reisen zwischen Regionen!)
    // ==========================================

    const TRADE_ROUTES = [
        { from: 'magmastroeme', to: 'reich_der_drei', goods: ['magmaklinge', 'eisenschwert'], danger: 0.2 },
        { from: 'samtmoos',     to: 'heisse_duenen',  goods: ['holz', 'heilkraut'],           danger: 0.3 },
        { from: 'salzwind',     to: 'tiefenhoehlen',  goods: ['fisch', 'seide'],               danger: 0.4 },
        { from: 'tiefenhoehlen', to: 'magmastroeme',  goods: ['erz', 'edelstein'],             danger: 0.15 },
        { from: 'gruenschlamm', to: 'samtmoos',       goods: ['sumpfessenz', 'giftpilz'],      danger: 0.35 },
        { from: 'reich_der_drei', to: 'salzwind',     goods: ['brot', 'stahlschild'],           danger: 0.25 },
        { from: 'heisse_duenen', to: 'blitzebene',    goods: ['edelstein', 'seide'],            danger: 0.45 },
        { from: 'blitzebene',   to: 'samtmoos',       goods: ['leder', 'fleisch'],              danger: 0.2 },
    ];

    // ==========================================
    // ECONOMY STATE
    // ==========================================

    let economyState = loadEconomyState();

    function loadEconomyState() {
        try {
            return JSON.parse(localStorage.getItem('najika_economy') || 'null') || createFreshEconomyState();
        } catch { return createFreshEconomyState(); }
    }

    function createFreshEconomyState() {
        const state = {
            regionalPrices: {},     // { region: { good: currentPrice } }
            activeCaravans: [],     // Karawanen unterwegs
            supplyLevels: {},       // { region: { good: supplyLevel } } (0-100)
            tradeHistory: [],       // Letzte Trades
            smugglingBounties: [],  // Kopfgelder für Schmuggler
            lastUpdate: Date.now(),
        };

        // Initialisiere regionale Preise und Vorräte
        Object.keys(REGIONAL_MARKETS).forEach(region => {
            state.regionalPrices[region] = {};
            state.supplyLevels[region] = {};

            const market = REGIONAL_MARKETS[region];

            Object.keys(GOODS).forEach(goodId => {
                const good = GOODS[goodId];
                let price = good.basePrice;

                // Lokale Produktion = billiger
                if (market.produces.includes(goodId)) {
                    price = Math.floor(price * market.productionBonus);
                    state.supplyLevels[region][goodId] = 80 + Math.floor(Math.random() * 20);
                }
                // Lokale Nachfrage = teurer
                else if (market.demands.includes(goodId)) {
                    price = Math.floor(price * market.demandPenalty);
                    state.supplyLevels[region][goodId] = 20 + Math.floor(Math.random() * 30);
                }
                // Neutral
                else {
                    state.supplyLevels[region][goodId] = 40 + Math.floor(Math.random() * 30);
                }

                // Kleine Zufallsvariation (±10%)
                price = Math.floor(price * (0.9 + Math.random() * 0.2));
                state.regionalPrices[region][goodId] = Math.max(1, price);
            });
        });

        return state;
    }

    function saveEconomyState() {
        localStorage.setItem('najika_economy', JSON.stringify(economyState));
    }

    // ==========================================
    // PREIS-BERECHNUNG (dynamisch!)
    // ==========================================

    function getPrice(goodId, region, isBuying) {
        const market = REGIONAL_MARKETS[region];
        const good = GOODS[goodId];
        if (!market || !good) return good?.basePrice || 0;

        let price = economyState.regionalPrices[region]?.[goodId] || good.basePrice;

        // Supply-Level beeinflusst Preis
        const supply = economyState.supplyLevels[region]?.[goodId] || 50;
        if (supply < 20) price *= 1.5;        // Knappheit!
        else if (supply < 40) price *= 1.2;   // Wenig
        else if (supply > 80) price *= 0.8;   // Überfluss

        // Fraktions-Reputation Modifier
        if (window.FactionSystem) {
            // Finde Hauptfraktion der Region
            const regionFactions = Object.values(window.FactionSystem.FACTIONS)
                .filter(f => f.region === region);
            if (regionFactions.length > 0) {
                const bestModifier = Math.min(
                    ...regionFactions.map(f => window.FactionSystem.getPriceModifier(f.id))
                );
                if (bestModifier !== Infinity) {
                    price *= bestModifier;
                }
            }
        }

        // WorldEventGenerator Preis-Modifier
        if (window.WorldEventGenerator) {
            const wState = WorldEventGenerator.getWorldState();
            const eco = wState.economyState?.[region];
            if (eco?.priceMultiplier) {
                price *= eco.priceMultiplier;
            }
        }

        // Kaufen = teurer, Verkaufen = billiger (Händlermarge)
        if (isBuying) {
            price *= 1.1;  // +10% beim Kauf
        } else {
            price *= 0.75; // -25% beim Verkauf (Händler will Gewinn)
        }

        return Math.max(1, Math.round(price));
    }

    // ==========================================
    // HANDEL
    // ==========================================

    function buyGood(goodId, region, quantity) {
        const price = getPrice(goodId, region, true) * quantity;
        const good = GOODS[goodId];
        if (!good) return { success: false, reason: 'Unbekannte Ware' };

        // Illegale Ware? Risiko!
        if (!good.legal) {
            const market = REGIONAL_MARKETS[region];
            if (market && Math.random() > market.illegalTolerance) {
                // Erwischt!
                return {
                    success: false,
                    reason: 'ERWISCHT! Illegaler Handel!',
                    caught: true,
                    penalty: Math.floor(price * 0.5),
                };
            }
        }

        // Supply reduzieren
        if (economyState.supplyLevels[region]) {
            economyState.supplyLevels[region][goodId] =
                Math.max(0, (economyState.supplyLevels[region][goodId] || 50) - quantity * 5);
        }

        // Preis steigt leicht nach Kauf (Nachfrage)
        if (economyState.regionalPrices[region]) {
            economyState.regionalPrices[region][goodId] =
                Math.floor((economyState.regionalPrices[region][goodId] || good.basePrice) * 1.02);
        }

        economyState.tradeHistory.push({
            type: 'buy', good: goodId, region, quantity, price,
            timestamp: Date.now(),
        });

        saveEconomyState();

        return { success: true, totalCost: price, good: good.name, quantity };
    }

    function sellGood(goodId, region, quantity) {
        const price = getPrice(goodId, region, false) * quantity;
        const good = GOODS[goodId];
        if (!good) return { success: false, reason: 'Unbekannte Ware' };

        // Illegale Ware?
        if (!good.legal) {
            const market = REGIONAL_MARKETS[region];
            if (market && Math.random() > market.illegalTolerance) {
                return {
                    success: false,
                    reason: 'ERWISCHT beim Verkauf illegaler Waren!',
                    caught: true,
                    penalty: Math.floor(price * 0.5),
                };
            }
            // Schmuggel erfolgreich → Fraktions-Reaktion
            if (window.FactionSystem) {
                window.FactionSystem.performAction('schmuggel', { intensity: 3 });
            }
        }

        // Supply erhöhen
        if (economyState.supplyLevels[region]) {
            economyState.supplyLevels[region][goodId] =
                Math.min(100, (economyState.supplyLevels[region][goodId] || 50) + quantity * 5);
        }

        // Preis sinkt leicht (mehr Angebot)
        if (economyState.regionalPrices[region]) {
            economyState.regionalPrices[region][goodId] =
                Math.floor((economyState.regionalPrices[region][goodId] || good.basePrice) * 0.98);
        }

        economyState.tradeHistory.push({
            type: 'sell', good: goodId, region, quantity, price,
            timestamp: Date.now(),
        });

        saveEconomyState();

        return { success: true, totalEarned: price, good: good.name, quantity };
    }

    // ==========================================
    // BESTE HANDELSROUTEN BERECHNEN
    // ==========================================

    function findBestTradeRoute(startRegion) {
        const routes = [];

        Object.keys(GOODS).forEach(goodId => {
            const buyPrice = getPrice(goodId, startRegion, true);
            if (buyPrice === Infinity) return;

            Object.keys(REGIONAL_MARKETS).forEach(targetRegion => {
                if (targetRegion === startRegion) return;
                const sellPrice = getPrice(goodId, targetRegion, false);
                const profit = sellPrice - buyPrice;
                if (profit > 0) {
                    routes.push({
                        good: goodId,
                        goodName: GOODS[goodId].name,
                        goodIcon: GOODS[goodId].icon,
                        from: startRegion,
                        to: targetRegion,
                        buyPrice,
                        sellPrice,
                        profit,
                        profitPercent: Math.round((profit / buyPrice) * 100),
                        legal: GOODS[goodId].legal,
                    });
                }
            });
        });

        return routes.sort((a, b) => b.profit - a.profit).slice(0, 10);
    }

    // ==========================================
    // KARAWANEN-SIMULATION
    // ==========================================

    function spawnCaravan() {
        const route = TRADE_ROUTES[Math.floor(Math.random() * TRADE_ROUTES.length)];
        const caravan = {
            id: `caravan_${Date.now()}`,
            route,
            progress: 0,    // 0-100
            goods: route.goods.map(g => ({ id: g, quantity: 5 + Math.floor(Math.random() * 10) })),
            guards: 2 + Math.floor(Math.random() * 3),
            alive: true,
            spawnedAt: Date.now(),
        };

        economyState.activeCaravans.push(caravan);
        saveEconomyState();
        return caravan;
    }

    function advanceCaravans() {
        economyState.activeCaravans.forEach(caravan => {
            if (!caravan.alive) return;

            // Fortschritt (10-20% pro Zyklus)
            caravan.progress += 10 + Math.floor(Math.random() * 10);

            // Überfall-Check
            if (Math.random() < caravan.route.danger * 0.1) {
                if (caravan.guards <= 0 || Math.random() < 0.3) {
                    // Karawane zerstört!
                    caravan.alive = false;

                    // Auswirkungen auf Wirtschaft
                    const targetRegion = caravan.route.to;
                    caravan.goods.forEach(g => {
                        if (economyState.supplyLevels[targetRegion]) {
                            economyState.supplyLevels[targetRegion][g.id] =
                                Math.max(0, (economyState.supplyLevels[targetRegion][g.id] || 50) - 10);
                        }
                    });

                    if (typeof notify === 'function') {
                        notify(`💀 Karawane auf dem Weg nach ${targetRegion} überfallen! Preise steigen.`, 'warning');
                    }
                } else {
                    caravan.guards--;
                }
            }

            // Angekommen?
            if (caravan.progress >= 100 && caravan.alive) {
                deliverCaravan(caravan);
            }
        });

        // Abgeschlossene/tote Karawanen entfernen
        economyState.activeCaravans = economyState.activeCaravans.filter(c =>
            c.alive && c.progress < 100
        );

        saveEconomyState();
    }

    function deliverCaravan(caravan) {
        const targetRegion = caravan.route.to;

        // Supply erhöhen in Zielregion
        caravan.goods.forEach(g => {
            if (economyState.supplyLevels[targetRegion]) {
                economyState.supplyLevels[targetRegion][g.id] =
                    Math.min(100, (economyState.supplyLevels[targetRegion][g.id] || 50) + g.quantity * 2);
            }
            // Preise sinken leicht
            if (economyState.regionalPrices[targetRegion]) {
                economyState.regionalPrices[targetRegion][g.id] =
                    Math.floor((economyState.regionalPrices[targetRegion][g.id] || GOODS[g.id]?.basePrice || 10) * 0.95);
            }
        });
    }

    // ==========================================
    // TAGES-UPDATE
    // ==========================================

    function dailyEconomyUpdate() {
        // 1. Preise normalisieren sich langsam
        Object.keys(REGIONAL_MARKETS).forEach(region => {
            const market = REGIONAL_MARKETS[region];
            Object.keys(GOODS).forEach(goodId => {
                const good = GOODS[goodId];
                const currentPrice = economyState.regionalPrices[region]?.[goodId] || good.basePrice;
                let targetPrice = good.basePrice;

                if (market.produces.includes(goodId)) targetPrice *= market.productionBonus;
                else if (market.demands.includes(goodId)) targetPrice *= market.demandPenalty;

                // Langsam zum Zielpreis hin bewegen (5% pro Tag)
                const newPrice = Math.floor(currentPrice + (targetPrice - currentPrice) * 0.05);
                if (economyState.regionalPrices[region]) {
                    economyState.regionalPrices[region][goodId] = Math.max(1, newPrice);
                }
            });

            // Supply regeneriert sich langsam
            Object.keys(GOODS).forEach(goodId => {
                if (economyState.supplyLevels[region]) {
                    const current = economyState.supplyLevels[region][goodId] || 50;
                    const target = market.produces.includes(goodId) ? 80 : 50;
                    economyState.supplyLevels[region][goodId] =
                        Math.floor(current + (target - current) * 0.1);
                }
            });
        });

        // 2. Neue Karawanen spawnen
        if (economyState.activeCaravans.length < 5) {
            if (Math.random() < 0.6) {
                spawnCaravan();
            }
        }

        // 3. Karawanen voranbewegen
        advanceCaravans();

        // 4. Trade History kürzen
        if (economyState.tradeHistory.length > 50) {
            economyState.tradeHistory = economyState.tradeHistory.slice(-50);
        }

        saveEconomyState();
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.EconomySystem = {
        // Daten
        GOODS,
        REGIONAL_MARKETS,
        TRADE_ROUTES,

        // Preise
        getPrice,
        findBestTradeRoute,

        // Handel
        buyGood,
        sellGood,

        // Karawanen
        spawnCaravan,
        advanceCaravans,
        getActiveCaravans: () => economyState.activeCaravans.filter(c => c.alive),

        // Update
        dailyEconomyUpdate,

        // State
        getState: () => ({ ...economyState }),
        getSupplyLevel: (region, good) => economyState.supplyLevels[region]?.[good] || 50,
        saveEconomyState,
    };

    console.log(`💰 Economy System geladen! ${Object.keys(GOODS).length} Waren | ${Object.keys(REGIONAL_MARKETS).length} Märkte`);
    console.log(`🐫 ${TRADE_ROUTES.length} Handelsrouten | ${economyState.activeCaravans.length} aktive Karawanen`);

})();
