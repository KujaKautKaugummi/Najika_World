// 🌱 NAJIKA GARDEN SYSTEM (Stardew Valley + Harvest Moon Style)
(function() {
    const GARDEN_CONFIG = {
        // 9 Beete im Garten (3x3 Grid)
        plots: [
            { id: 1, position: [550, 0, 550], size: 20 },
            { id: 2, position: [600, 0, 550], size: 20 },
            { id: 3, position: [650, 0, 550], size: 20 },
            { id: 4, position: [550, 0, 600], size: 20 },
            { id: 5, position: [600, 0, 600], size: 20 },
            { id: 6, position: [650, 0, 600], size: 20 },
            { id: 7, position: [550, 0, 650], size: 20 },
            { id: 8, position: [600, 0, 650], size: 20 },
            { id: 9, position: [650, 0, 650], size: 20 }
        ],

        // Pflanzen mit 5 Wachstumsstufen
        plants: {
            karotte: {
                name: 'Karotte',
                stages: 5,
                growTime: 60,  // seconds per stage
                harvestYield: 3,
                sellPrice: 15,
                uses: ['kochen', 'verkaufen', 'heilen']
            },
            tomate: {
                name: 'Tomate',
                stages: 5,
                growTime: 80,
                harvestYield: 4,
                sellPrice: 20,
                uses: ['kochen', 'verkaufen']
            },
            weizen: {
                name: 'Weizen',
                stages: 5,
                growTime: 50,
                harvestYield: 5,
                sellPrice: 10,
                uses: ['kochen', 'crafting']
            },
            heilkraut: {
                name: 'Heilkraut',
                stages: 5,
                growTime: 120,
                harvestYield: 2,
                sellPrice: 50,
                uses: ['heilen', 'crafting']
            },
            magische_blume: {
                name: 'Magische Blume',
                stages: 5,
                growTime: 180,
                harvestYield: 1,
                sellPrice: 100,
                uses: ['magie', 'crafting', 'verkaufen']
            }
        },

        // Saatgut-Shop
        seeds: {
            karotte_samen: { plant: 'karotte', cost: 5 },
            tomaten_samen: { plant: 'tomate', cost: 10 },
            weizen_samen: { plant: 'weizen', cost: 3 },
            heilkraut_samen: { plant: 'heilkraut', cost: 30 },
            magische_blumen_samen: { plant: 'magische_blume', cost: 75 }
        },

        // Gießen-System
        wateringCan: {
            capacity: 10,
            current: 10,
            refillTime: 2  // seconds
        }
    };

    // State
    const plotStates = {};  // { plotId: { plant, stage, plantedTime, watered, ready } }
    const inventory = {
        seeds: {},
        harvested: {},
        gold: 100  // Startgold
    };
    let gardenUI = null;
    let selectedPlot = null;
    let wateringCan = { ...GARDEN_CONFIG.wateringCan };

    // === INIT ===

    function init() {
        // Initialize all plots as empty
        GARDEN_CONFIG.plots.forEach(plot => {
            plotStates[plot.id] = {
                plant: null,
                stage: 0,
                plantedTime: 0,
                watered: false,
                ready: false
            };
        });

        // Startgeld und Start-Samen
        inventory.gold = 100;
        inventory.seeds = {
            'karotte_samen': 5,
            'weizen_samen': 10
        };

        createGardenUI();
        console.log('🌱 Garden System initialized');
    }

    // === PLOT MANAGEMENT ===

    function getNearestPlot(playerPosition) {
        let nearest = null;
        let minDist = Infinity;

        for (const plot of GARDEN_CONFIG.plots) {
            const dist = Math.sqrt(
                Math.pow(playerPosition.x - plot.position[0], 2) +
                Math.pow(playerPosition.z - plot.position[2], 2)
            );
            if (dist < plot.size && dist < minDist) {
                minDist = dist;
                nearest = plot;
            }
        }

        return nearest;
    }

    function plantSeed(plotId, seedType) {
        if (!plotStates[plotId]) return false;
        if (plotStates[plotId].plant) {
            if (typeof notify === 'function') {
                notify('⚠️ Beet ist bereits bepflanzt!', 'warning');
            }
            return false;
        }

        const seed = GARDEN_CONFIG.seeds[seedType];
        if (!seed) return false;

        if (!inventory.seeds[seedType] || inventory.seeds[seedType] <= 0) {
            if (typeof notify === 'function') {
                notify('⚠️ Keine Samen vorhanden!', 'warning');
            }
            return false;
        }

        // Plant seed
        inventory.seeds[seedType]--;
        plotStates[plotId] = {
            plant: seed.plant,
            stage: 0,
            plantedTime: Date.now(),
            watered: true,  // Frisch gepflanzt = gegossen
            ready: false
        };

        console.log(`🌱 Gepflanzt: ${GARDEN_CONFIG.plants[seed.plant].name} auf Beet ${plotId}`);

        if (typeof notify === 'function') {
            notify(`🌱 ${GARDEN_CONFIG.plants[seed.plant].name} gepflanzt!`, 'success');
        }

        return true;
    }

    function waterPlot(plotId) {
        if (!plotStates[plotId] || !plotStates[plotId].plant) {
            if (typeof notify === 'function') {
                notify('⚠️ Beet ist leer!', 'warning');
            }
            return false;
        }

        if (wateringCan.current <= 0) {
            if (typeof notify === 'function') {
                notify('⚠️ Gießkanne leer!', 'warning');
            }
            return false;
        }

        if (plotStates[plotId].watered) {
            if (typeof notify === 'function') {
                notify('✓ Bereits gegossen!', 'info');
            }
            return false;
        }

        wateringCan.current--;
        plotStates[plotId].watered = true;

        console.log(`💧 Gegossen: Beet ${plotId}`);

        if (typeof notify === 'function') {
            notify(`💧 Gegossen!`, 'success');
        }

        return true;
    }

    function harvestPlot(plotId) {
        const plot = plotStates[plotId];
        if (!plot || !plot.plant || !plot.ready) {
            if (typeof notify === 'function') {
                notify('⚠️ Nichts zu ernten!', 'warning');
            }
            return false;
        }

        const plantConfig = GARDEN_CONFIG.plants[plot.plant];
        const harvestedItem = plot.plant;
        const amount = plantConfig.harvestYield;

        // Add to inventory
        inventory.harvested[harvestedItem] = (inventory.harvested[harvestedItem] || 0) + amount;

        console.log(`✅ Geerntet: ${amount}x ${plantConfig.name}`);

        if (typeof notify === 'function') {
            notify(`✅ ${amount}x ${plantConfig.name} geerntet!`, 'success');
        }

        // Reset plot
        plotStates[plotId] = {
            plant: null,
            stage: 0,
            plantedTime: 0,
            watered: false,
            ready: false
        };

        return true;
    }

    // === UPDATE LOOP ===

    function updateGarden(delta) {
        const now = Date.now();

        // Update all plots
        for (const plotId in plotStates) {
            const plot = plotStates[plotId];
            if (!plot.plant) continue;

            const plantConfig = GARDEN_CONFIG.plants[plot.plant];
            const growTimeMs = plantConfig.growTime * 1000;

            // Check if needs watering
            const timeSinceWatered = now - plot.plantedTime;
            const dayLength = growTimeMs * plantConfig.stages;  // Gesamtwachstumszeit
            const dayProgress = timeSinceWatered / dayLength;

            // Every "day" (stage) needs watering
            const currentDay = Math.floor(dayProgress * plantConfig.stages);
            if (currentDay > plot.stage && !plot.watered) {
                // Pflanze wächst nicht weiter ohne Wasser
                continue;
            }

            // Calculate stage
            const elapsedTime = now - plot.plantedTime;
            const newStage = Math.min(
                plantConfig.stages,
                Math.floor(elapsedTime / growTimeMs)
            );

            if (newStage > plot.stage) {
                plot.stage = newStage;
                plot.watered = false;  // Needs watering again

                console.log(`🌱 Beet ${plotId}: Stufe ${plot.stage}/${plantConfig.stages}`);
            }

            // Check if ready for harvest
            if (plot.stage >= plantConfig.stages) {
                plot.ready = true;
            }
        }

        // Refill watering can slowly
        if (wateringCan.current < wateringCan.capacity) {
            wateringCan.current = Math.min(
                wateringCan.capacity,
                wateringCan.current + (delta / GARDEN_CONFIG.wateringCan.refillTime)
            );
        }
    }

    // === SHOP ===

    function buySeed(seedType) {
        const seed = GARDEN_CONFIG.seeds[seedType];
        if (!seed) return false;

        if (inventory.gold < seed.cost) {
            if (typeof notify === 'function') {
                notify('⚠️ Nicht genug Gold!', 'warning');
            }
            return false;
        }

        inventory.gold -= seed.cost;
        inventory.seeds[seedType] = (inventory.seeds[seedType] || 0) + 1;

        console.log(`✅ Gekauft: ${seedType} für ${seed.cost}G`);

        if (typeof notify === 'function') {
            const plantConfig = GARDEN_CONFIG.plants[seed.plant];
            notify(`✅ ${plantConfig.name} Samen gekauft!`, 'success');
        }

        // Update shop UI
        updateShopUI();
        updateGardenUI();

        return true;
    }

    function sellHarvest(itemType, amount = 1) {
        const plantConfig = GARDEN_CONFIG.plants[itemType];
        if (!plantConfig) return false;

        if (!inventory.harvested[itemType] || inventory.harvested[itemType] < amount) {
            if (typeof notify === 'function') {
                notify('⚠️ Nicht genug Items!', 'warning');
            }
            return false;
        }

        inventory.harvested[itemType] -= amount;
        const totalValue = plantConfig.sellPrice * amount;
        inventory.gold += totalValue;

        console.log(`💰 Verkauft: ${amount}x ${plantConfig.name} für ${totalValue}G`);

        if (typeof notify === 'function') {
            notify(`💰 +${totalValue}G`, 'success');
        }

        return true;
    }

    // === UI ===

    function createGardenUI() {
        gardenUI = document.createElement('div');
        gardenUI.id = 'garden-ui';
        gardenUI.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.8);
            border: 3px solid #50c878;
            border-radius: 15px;
            padding: 15px;
            color: white;
            font-family: monospace;
            font-size: 12px;
            display: none;
            z-index: 1000;
            max-width: 300px;
        `;

        gardenUI.innerHTML = `
            <h3 style="display: flex; justify-content: space-between; align-items: center; cursor: pointer; margin: 0 0 10px 0; font-size: 16px;" id="garden-header">
                <span>🌱 Garten</span>
                <button id="garden-toggle" style="background: none; border: none; color: #50c878; font-size: 1.2rem; cursor: pointer; padding: 0; margin: 0;">▼</button>
            </h3>
            <div id="garden-content">
                <div id="garden-plot-info" style="margin-bottom: 10px;">
                    Kein Beet ausgewählt
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Inventar:</strong>
                    <div id="garden-inventory" style="margin-top: 5px; font-size: 11px;"></div>
                </div>
                <div>
                    <strong>💧 Gießkanne:</strong>
                    <div style="background: #333; height: 10px; border-radius: 5px; overflow: hidden; margin-top: 3px;">
                        <div id="water-bar" style="background: #4a90e2; height: 100%; width: 100%;"></div>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 11px; color: #aaa;">
                    E: Pflanzen/Ernten | R: Gießen
                </div>
            </div>
        `;

        document.body.appendChild(gardenUI);

        // Toggle collapse handler
        const header = gardenUI.querySelector('#garden-header');
        const toggle = gardenUI.querySelector('#garden-toggle');
        if (header && toggle) {
            const toggleGarden = () => {
                const content = gardenUI.querySelector('#garden-content');
                if (content.style.display === 'none') {
                    content.style.display = 'block';
                    toggle.textContent = '▼';
                } else {
                    content.style.display = 'none';
                    toggle.textContent = '▶';
                }
            };
            header.addEventListener('click', toggleGarden);
            toggle.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleGarden();
            });
        }

        // Create Shop UI
        createShopUI();
    }

    let shopUI = null;

    function createShopUI() {
        shopUI = document.createElement('div');
        shopUI.id = 'garden-shop-ui';
        shopUI.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.95);
            border: 3px solid #50c878;
            border-radius: 15px;
            padding: 20px;
            color: white;
            font-family: monospace;
            font-size: 13px;
            display: none;
            z-index: 2000;
            min-width: 400px;
            max-height: 80vh;
            overflow-y: auto;
        `;

        shopUI.innerHTML = `
            <div style="text-align: center; font-size: 18px; margin-bottom: 15px; font-weight: bold;">
                🏪 SAMEN-SHOP
            </div>
            <div style="margin-bottom: 15px; text-align: center; font-size: 14px;">
                💰 Gold: <span id="shop-gold">100</span>G
            </div>
            <div id="shop-items" style="margin-bottom: 15px;">
                <!-- Will be populated dynamically -->
            </div>
            <div style="text-align: center; margin-top: 15px;">
                <button id="shop-close-btn" style="
                    padding: 10px 25px;
                    background: #ff6b9d;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 14px;
                    cursor: pointer;
                    font-weight: bold;
                ">Schließen (ESC)</button>
            </div>
        `;

        document.body.appendChild(shopUI);

        // Close button handler
        const closeBtn = shopUI.querySelector('#shop-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', hideShopUI);
        }

        // ESC key handler
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Escape' && shopUI && shopUI.style.display === 'block') {
                hideShopUI();
            }
        });

        updateShopUI();
    }

    function showShopUI() {
        if (!shopUI) return;
        shopUI.style.display = 'block';
        updateShopUI();
    }

    function hideShopUI() {
        if (!shopUI) return;
        shopUI.style.display = 'none';
    }

    function updateShopUI() {
        if (!shopUI) return;

        // Update gold
        const goldEl = shopUI.querySelector('#shop-gold');
        if (goldEl) {
            goldEl.textContent = Math.floor(inventory.gold);
        }

        // Update shop items
        const itemsEl = shopUI.querySelector('#shop-items');
        if (itemsEl) {
            let html = '';
            for (const [seedType, seedConfig] of Object.entries(GARDEN_CONFIG.seeds)) {
                const plantConfig = GARDEN_CONFIG.plants[seedConfig.plant];
                const canAfford = inventory.gold >= seedConfig.cost;

                html += `
                    <div style="
                        background: rgba(255,255,255,0.1);
                        padding: 12px;
                        margin-bottom: 10px;
                        border-radius: 8px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        border: 2px solid ${canAfford ? '#50c878' : '#666'};
                    ">
                        <div>
                            <div style="font-weight: bold; font-size: 14px;">🌱 ${plantConfig.name} Samen</div>
                            <div style="font-size: 11px; color: #aaa; margin-top: 3px;">
                                Wächst in ${plantConfig.growTime}s/Stufe | ${plantConfig.harvestYield}x Ertrag
                            </div>
                            <div style="font-size: 11px; color: #aaa;">
                                Verwendung: ${plantConfig.uses.join(', ')}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 16px; font-weight: bold; color: #ffd700; margin-bottom: 5px;">
                                ${seedConfig.cost}G
                            </div>
                            <button
                                onclick="window.GardenSystem.buySeed('${seedType}')"
                                style="
                                    padding: 8px 15px;
                                    background: ${canAfford ? '#50c878' : '#666'};
                                    color: white;
                                    border: none;
                                    border-radius: 6px;
                                    font-family: monospace;
                                    font-size: 12px;
                                    cursor: ${canAfford ? 'pointer' : 'not-allowed'};
                                    font-weight: bold;
                                "
                                ${canAfford ? '' : 'disabled'}
                            >Kaufen</button>
                        </div>
                    </div>
                `;
            }
            itemsEl.innerHTML = html;
        }
    }

    function showGardenUI() {
        if (!gardenUI) return;
        gardenUI.style.display = 'block';
        updateGardenUI();
    }

    function hideGardenUI() {
        if (!gardenUI) return;
        gardenUI.style.display = 'none';
    }

    function updateGardenUI() {
        if (!gardenUI) return;

        // Update plot info
        const plotInfo = gardenUI.querySelector('#garden-plot-info');
        if (plotInfo && selectedPlot) {
            const state = plotStates[selectedPlot.id];
            if (state && state.plant) {
                const plantConfig = GARDEN_CONFIG.plants[state.plant];
                const stageText = state.ready ? '✅ ERNTEREIF' : `Stufe ${state.stage}/${plantConfig.stages}`;
                const wateredText = state.watered ? '💧' : '🚫';
                plotInfo.innerHTML = `
                    <strong>Beet ${selectedPlot.id}:</strong><br>
                    ${plantConfig.name} - ${stageText}<br>
                    Wasser: ${wateredText}
                `;
            } else {
                plotInfo.innerHTML = `
                    <strong>Beet ${selectedPlot.id}:</strong><br>
                    Leer (Drücke E zum Pflanzen)
                `;
            }
        }

        // Update inventory
        const invEl = gardenUI.querySelector('#garden-inventory');
        if (invEl) {
            let html = `💰 Gold: ${Math.floor(inventory.gold)}G<br>`;
            html += '<strong>Samen:</strong><br>';
            for (const [seed, count] of Object.entries(inventory.seeds)) {
                if (count > 0) {
                    html += `${seed}: ${count}<br>`;
                }
            }
            html += '<strong>Geerntet:</strong><br>';
            for (const [item, count] of Object.entries(inventory.harvested)) {
                if (count > 0) {
                    const plantConfig = GARDEN_CONFIG.plants[item];
                    html += `${plantConfig.name}: ${count}<br>`;
                }
            }
            invEl.innerHTML = html;
        }

        // Update water bar
        const waterBar = gardenUI.querySelector('#water-bar');
        if (waterBar) {
            const percent = (wateringCan.current / wateringCan.capacity) * 100;
            waterBar.style.width = `${percent}%`;
        }
    }

    // === KEYBOARD ===

    function setupKeyboardHandler() {
        document.addEventListener('keydown', (e) => {
            // T: Open Shop (global - immer verfügbar)
            if (e.code === 'KeyT') {
                if (shopUI && shopUI.style.display === 'block') {
                    hideShopUI();
                } else {
                    showShopUI();
                }
                return;
            }

            // NUR wenn im Garten (selectedPlot gesetzt)
            if (!selectedPlot) return;

            // E: Plant/Harvest - NUR im Garten!
            if (e.code === 'KeyE') {
                // NICHT im Gebäude! (currentInterior wird in 3d_scene.js gesetzt)
                if (window.currentInterior) {
                    return; // Im Gebäude = keine Garten-Aktionen!
                }
                // Check if near building (Building hat Priorität!)
                const buildingPrompt = document.getElementById('building-prompt-ui');
                if (buildingPrompt && buildingPrompt.style.display === 'block') {
                    return; // Building hat Priorität!
                }
                const state = plotStates[selectedPlot.id];
                if (state && state.plant && state.ready) {
                    harvestPlot(selectedPlot.id);
                    updateGardenUI();
                } else if (!state || !state.plant) {
                    // Open seed selection (for now, plant first available seed)
                    for (const seedType in inventory.seeds) {
                        if (inventory.seeds[seedType] > 0) {
                            plantSeed(selectedPlot.id, seedType);
                            updateGardenUI();
                            break;
                        }
                    }
                }
            }

            // R: Water
            if (e.code === 'KeyR') {
                waterPlot(selectedPlot.id);
                updateGardenUI();
            }
        });
    }

    // === EXPORT ===

    window.GardenSystem = {
        init,
        updateGarden,
        getNearestPlot,
        plantSeed,
        waterPlot,
        harvestPlot,
        buySeed,
        sellHarvest,
        showGardenUI,
        hideGardenUI,
        updateGardenUI,
        showShopUI,
        hideShopUI,
        updateShopUI,
        setSelectedPlot(plot) { selectedPlot = plot; },
        getInventory() { return { ...inventory }; },
        getPlotStates() { return { ...plotStates }; }
    };

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            init();
            setupKeyboardHandler();
        });
    } else {
        init();
        setupKeyboardHandler();
    }

    console.log('🌱 Garden System loaded!');
})();
