// 🎣 NAJIKA FISHING SYSTEM (Zelda + Stardew Valley Style)
// Erweitert mit: Köder, Angelruten-Upgrades, Aquarium
(function() {
    // ============================================
    // ANGELRUTEN (Upgrades)
    // ============================================
    const FISHING_RODS = {
        holz_angel: {
            name: 'Holzangel',
            icon: '🎣',
            tier: 1,
            castBonus: 0,
            reelBonus: 0,
            rarityBonus: 0,
            description: 'Eine einfache Holzangel für Anfänger',
            price: 0  // Starter
        },
        bambus_angel: {
            name: 'Bambusangel',
            icon: '🎋',
            tier: 2,
            castBonus: 20,
            reelBonus: 0.1,
            rarityBonus: 5,
            description: 'Leichte Angel mit besserer Wurfweite',
            price: 200
        },
        stahl_angel: {
            name: 'Stahlangel',
            icon: '⚙️',
            tier: 3,
            castBonus: 40,
            reelBonus: 0.2,
            rarityBonus: 10,
            description: 'Robuste Angel für größere Fische',
            price: 500
        },
        gold_angel: {
            name: 'Goldangel',
            icon: '✨',
            tier: 4,
            castBonus: 60,
            reelBonus: 0.3,
            rarityBonus: 15,
            description: 'Meisterhafte Angel mit goldener Schnur',
            price: 1500
        },
        najika_angel: {
            name: 'Najikas Sternangel',
            icon: '🌟',
            tier: 5,
            castBonus: 100,
            reelBonus: 0.5,
            rarityBonus: 25,
            description: 'Legendäre Angel von Najika persönlich',
            price: 5000
        }
    };

    // ============================================
    // KÖDER
    // ============================================
    const BAITS = {
        wurm: {
            name: 'Regenwurm',
            icon: '🪱',
            rarityBonus: 0,
            targetFish: null,  // Alle Fische
            uses: 10,
            price: 5,
            description: 'Standard-Köder für alle Fische'
        },
        mais: {
            name: 'Maiskörner',
            icon: '🌽',
            rarityBonus: 5,
            targetFish: ['Karpfen', 'Forelle'],
            uses: 15,
            price: 10,
            description: 'Lockt besonders Karpfen und Forellen'
        },
        gluehwuermchen: {
            name: 'Glühwürmchen',
            icon: '✨',
            rarityBonus: 15,
            targetFish: ['Goldforelle', 'Najika-Fisch'],
            uses: 5,
            price: 50,
            description: 'Lockt seltene leuchtende Fische'
        },
        fleisch: {
            name: 'Fleischstück',
            icon: '🥩',
            rarityBonus: 10,
            targetFish: ['Wels', 'Boss-Hecht', 'Aal'],
            uses: 8,
            price: 30,
            description: 'Lockt Raubfische an'
        },
        magischer_koeder: {
            name: 'Magischer Köder',
            icon: '💫',
            rarityBonus: 30,
            targetFish: null,  // Alle, aber höhere Legendary-Chance
            uses: 3,
            price: 200,
            description: 'Erhöht die Chance auf legendäre Fische drastisch'
        },
        kristall_koeder: {
            name: 'Kristallköder',
            icon: '💎',
            rarityBonus: 20,
            targetFish: ['Legendärer Kristallfisch'],
            uses: 1,
            price: 500,
            description: 'Der einzige Köder für den Legendären Kristallfisch'
        }
    };

    // ============================================
    // AQUARIUM
    // ============================================
    const AQUARIUM = {
        tanks: {
            klein: { name: 'Kleines Aquarium', capacity: 5, price: 100 },
            mittel: { name: 'Mittleres Aquarium', capacity: 15, price: 500 },
            gross: { name: 'Großes Aquarium', capacity: 30, price: 2000 },
            riesen: { name: 'Riesen-Aquarium', capacity: 50, price: 10000 }
        },
        displayedFish: [],  // Fische im Aquarium
        currentTank: null,
        location: 'schwarze_muehle'  // Wo das Aquarium steht
    };

    const FISHING_CONFIG = {
        // Angelplätze in der Open World
        spots: [
            {
                id: 'teich_1',
                name: 'Kristallteich',
                position: [800, 0, 800],
                radius: 100,
                fische: [
                    { name: 'Forelle', weight: [0.5, 2.5], rarity: 'common', value: 10, difficulty: 1 },
                    { name: 'Karpfen', weight: [1.0, 5.0], rarity: 'common', value: 15, difficulty: 2 },
                    { name: 'Lachs', weight: [2.0, 8.0], rarity: 'uncommon', value: 30, difficulty: 3 },
                    { name: 'Goldforelle', weight: [1.5, 4.0], rarity: 'rare', value: 50, difficulty: 4 },
                    { name: 'Legendärer Kristallfisch', weight: [10.0, 15.0], rarity: 'legendary', value: 200, difficulty: 8 }
                ]
            },
            {
                id: 'see_zentrum',
                name: 'Weltensee',
                position: [-800, 0, -800],
                radius: 150,
                fische: [
                    { name: 'Wels', weight: [5.0, 15.0], rarity: 'uncommon', value: 40, difficulty: 5 },
                    { name: 'Aal', weight: [0.8, 3.0], rarity: 'common', value: 20, difficulty: 3 },
                    { name: 'Boss-Hecht', weight: [8.0, 20.0], rarity: 'epic', value: 100, difficulty: 7 },
                    { name: 'Najika-Fisch', weight: [15.0, 30.0], rarity: 'legendary', value: 500, difficulty: 10 }
                ]
            }
        ],

        // Timing Windows (Zelda Style)
        timingWindows: {
            perfect: { min: 0.45, max: 0.55, multiplier: 2.0 },   // 10% window
            good: { min: 0.35, max: 0.65, multiplier: 1.5 },      // 30% window
            ok: { min: 0.25, max: 0.75, multiplier: 1.0 },        // 50% window
            bad: { min: 0.0, max: 1.0, multiplier: 0.5 }          // Outside
        },

        // Minigame Parameters
        castDistance: { min: 50, max: 300 },
        reelSpeed: 1.0,
        fishStamina: 100
    };

    // State
    let currentSpot = null;
    let isFishing = false;
    let castPhase = null;  // 'aiming', 'casting', 'waiting', 'biting', 'reeling'

    // Equipment State
    let equippedRod = 'holz_angel';
    let equippedBait = null;
    let baitInventory = { wurm: 20 };  // Start mit 20 Würmern
    let ownedRods = ['holz_angel'];

    // Aquarium State
    let aquariumFish = [];
    let ownedTank = null;

    // Fish Collection (Pokedex-Style)
    let fishCollection = {};  // { 'Forelle': { caught: 5, maxWeight: 2.3 } }
    let castPower = 0;
    let castPowerIncreasing = true;
    let hookedFish = null;
    let fishProgress = 0;
    let fishStamina = 100;
    let reelTiming = 0;
    let perfectHits = 0;
    let fishingUI = null;

    // Inventory
    const inventory = {
        fish: {},  // { 'Forelle': count }
        totalValue: 0
    };

    // === PUBLIC API ===

    function init() {
        console.log('🎣 Fishing System initialized');
        createFishingUI();
    }

    function checkNearSpot(playerPosition) {
        for (const spot of FISHING_CONFIG.spots) {
            const dist = Math.sqrt(
                Math.pow(playerPosition.x - spot.position[0], 2) +
                Math.pow(playerPosition.z - spot.position[2], 2)
            );
            if (dist < spot.radius) {
                currentSpot = spot;
                return spot;
            }
        }
        currentSpot = null;
        return null;
    }

    function startFishing() {
        if (!currentSpot || isFishing) return false;

        isFishing = true;
        castPhase = 'aiming';
        castPower = 0;
        castPowerIncreasing = true;

        showFishingUI();
        updateCastPowerBar();

        console.log(`🎣 Angeln bei: ${currentSpot.name}`);
        return true;
    }

    function updateFishing(delta) {
        if (!isFishing) return;

        switch (castPhase) {
            case 'aiming':
                updateCastPower(delta);
                break;
            case 'waiting':
                updateWaitForBite(delta);
                break;
            case 'reeling':
                updateReeling(delta);
                break;
        }
    }

    function cancelFishing() {
        isFishing = false;
        castPhase = null;
        hookedFish = null;
        hideFishingUI();
    }

    // === PHASE 1: CAST (Power Bar) ===

    function updateCastPower(delta) {
        // Powerbar oszilliert 0-100%
        const speed = 150;  // % per second
        if (castPowerIncreasing) {
            castPower += speed * delta;
            if (castPower >= 100) {
                castPower = 100;
                castPowerIncreasing = false;
            }
        } else {
            castPower -= speed * delta;
            if (castPower <= 0) {
                castPower = 0;
                castPowerIncreasing = true;
            }
        }
        updateCastPowerBar();
    }

    function castLine() {
        if (castPhase !== 'aiming') return false;

        const distance = FISHING_CONFIG.castDistance.min +
            (FISHING_CONFIG.castDistance.max - FISHING_CONFIG.castDistance.min) * (castPower / 100);

        console.log(`🎣 Ausgeworfen! Distanz: ${Math.round(distance)}m`);

        castPhase = 'waiting';
        setTimeout(triggerBite, Math.random() * 3000 + 2000);  // 2-5 sekunden

        return true;
    }

    // === PHASE 2: WAIT FOR BITE ===

    function updateWaitForBite(delta) {
        // UI zeigt "Warte auf Biss..."
        if (fishingUI) {
            const statusEl = fishingUI.querySelector('#fishing-status');
            if (statusEl) {
                statusEl.textContent = '🎣 Warte auf Biss...';
            }
        }
    }

    function triggerBite() {
        if (castPhase !== 'waiting') return;

        // Wähle zufälligen Fisch basierend auf Rarity
        hookedFish = selectRandomFish();
        fishStamina = 100;
        fishProgress = 0;
        perfectHits = 0;
        reelTiming = Math.random();  // Start position

        castPhase = 'reeling';
        console.log(`🐟 BISS! ${hookedFish.name} hat angebissen!`);

        if (typeof notify === 'function') {
            notify(`🐟 ${hookedFish.name} hat angebissen!`, 'info');
        }
    }

    function selectRandomFish() {
        if (!currentSpot) return null;

        // Rarity weights: common 50%, uncommon 30%, rare 15%, epic 4%, legendary 1%
        const rarityRoll = Math.random() * 100;
        let targetRarity;

        if (rarityRoll < 50) targetRarity = 'common';
        else if (rarityRoll < 80) targetRarity = 'uncommon';
        else if (rarityRoll < 95) targetRarity = 'rare';
        else if (rarityRoll < 99) targetRarity = 'epic';
        else targetRarity = 'legendary';

        // Filter fish by rarity
        const candidates = currentSpot.fische.filter(f => f.rarity === targetRarity);
        if (candidates.length === 0) {
            // Fallback to common
            return currentSpot.fische.find(f => f.rarity === 'common');
        }

        const fish = candidates[Math.floor(Math.random() * candidates.length)];
        // Random weight
        const weight = fish.weight[0] + Math.random() * (fish.weight[1] - fish.weight[0]);

        return { ...fish, weight: weight.toFixed(1) };
    }

    // === PHASE 3: REELING MINIGAME (Zelda Style) ===

    function updateReeling(delta) {
        if (!hookedFish) return;

        // Timing marker bewegt sich (oszilliert)
        reelTiming += (hookedFish.difficulty * 0.3 + 0.5) * delta;
        if (reelTiming > 1) reelTiming -= 1;

        // Fish kämpft zurück - reduziert Progress
        fishProgress = Math.max(0, fishProgress - hookedFish.difficulty * 5 * delta);

        // Update UI
        updateReelingUI();

        // Check success/fail
        if (fishProgress >= 100) {
            catchFish();
        }
        if (fishStamina <= 0) {
            fishEscaped();
        }
    }

    function reel() {
        if (castPhase === 'aiming') {
            return castLine();
        }

        if (castPhase !== 'reeling' || !hookedFish) return false;

        // Check timing window
        const timing = getTiming(reelTiming);

        if (timing.name === 'perfect') {
            perfectHits++;
            fishProgress += 20 * timing.multiplier;
            fishStamina -= 15;
            console.log('💎 PERFECT!');
            if (typeof notify === 'function') {
                notify('💎 PERFECT!', 'success');
            }
        } else if (timing.name === 'good') {
            fishProgress += 15 * timing.multiplier;
            fishStamina -= 10;
            console.log('👍 GOOD!');
        } else if (timing.name === 'ok') {
            fishProgress += 10 * timing.multiplier;
            fishStamina -= 5;
            console.log('✓ OK');
        } else {
            // Bad timing - fish kämpft zurück
            fishProgress = Math.max(0, fishProgress - 10);
            console.log('❌ TOO EARLY/LATE!');
        }

        return true;
    }

    function getTiming(value) {
        for (const [name, window] of Object.entries(FISHING_CONFIG.timingWindows)) {
            if (value >= window.min && value <= window.max) {
                return { name, ...window };
            }
        }
        return { name: 'bad', multiplier: 0.5 };
    }

    function catchFish() {
        if (!hookedFish) return;

        // Add to inventory
        const fishName = hookedFish.name;
        inventory.fish[fishName] = (inventory.fish[fishName] || 0) + 1;
        inventory.totalValue += hookedFish.value;

        const bonus = perfectHits >= 3 ? ' (BONUS)' : '';
        const totalValue = perfectHits >= 3 ? hookedFish.value * 1.5 : hookedFish.value;

        console.log(`✅ GEFANGEN! ${fishName} (${hookedFish.weight}kg) - ${totalValue}G${bonus}`);

        if (typeof notify === 'function') {
            notify(`✅ ${fishName} gefangen! (${hookedFish.weight}kg) - ${Math.round(totalValue)}G${bonus}`, 'success');
        }

        // Reset
        isFishing = false;
        castPhase = null;
        hookedFish = null;
        hideFishingUI();
    }

    function fishEscaped() {
        if (!hookedFish) return;

        console.log(`❌ ${hookedFish.name} ist entkommen!`);

        if (typeof notify === 'function') {
            notify(`❌ ${hookedFish.name} ist entkommen!`, 'error');
        }

        // Reset
        isFishing = false;
        castPhase = null;
        hookedFish = null;
        hideFishingUI();
    }

    // === UI ===

    function createFishingUI() {
        fishingUI = document.createElement('div');
        fishingUI.id = 'fishing-ui';
        fishingUI.style.cssText = `
            position: fixed;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.8);
            border: 3px solid #4a90e2;
            border-radius: 15px;
            padding: 20px;
            color: white;
            font-family: monospace;
            font-size: 14px;
            display: none;
            z-index: 1000;
            min-width: 400px;
        `;

        fishingUI.innerHTML = `
            <div id="fishing-status" style="margin-bottom: 15px; font-size: 16px; text-align: center;">
                🎣 Angeln
            </div>
            <div id="cast-power-container" style="margin-bottom: 10px;">
                <div style="margin-bottom: 5px;">Wurfkraft:</div>
                <div style="background: #333; height: 20px; border-radius: 5px; overflow: hidden;">
                    <div id="cast-power-bar" style="background: linear-gradient(90deg, #4a90e2, #50c878); height: 100%; width: 0%; transition: width 0.05s;"></div>
                </div>
            </div>
            <div id="reeling-container" style="display: none;">
                <div style="margin-bottom: 5px;">Progress:</div>
                <div style="background: #333; height: 15px; border-radius: 5px; overflow: hidden; margin-bottom: 10px;">
                    <div id="fish-progress-bar" style="background: #50c878; height: 100%; width: 0%;"></div>
                </div>
                <div style="margin-bottom: 5px;">Timing:</div>
                <div style="background: #333; height: 30px; border-radius: 5px; position: relative; margin-bottom: 10px;">
                    <div style="position: absolute; left: 45%; width: 10%; height: 100%; background: rgba(80,200,120,0.5);"></div>
                    <div id="timing-marker" style="position: absolute; left: 0%; width: 5px; height: 100%; background: yellow; transition: left 0.05s;"></div>
                </div>
                <div id="fish-info" style="text-align: center; font-size: 12px;"></div>
            </div>
            <div style="margin-top: 15px; text-align: center; font-size: 12px; color: #aaa;">
                Drücke SPACE zum Einholen
            </div>
        `;

        document.body.appendChild(fishingUI);
    }

    function showFishingUI() {
        if (!fishingUI) return;
        fishingUI.style.display = 'block';
    }

    function hideFishingUI() {
        if (!fishingUI) return;
        fishingUI.style.display = 'none';
    }

    function updateCastPowerBar() {
        if (!fishingUI) return;
        const bar = fishingUI.querySelector('#cast-power-bar');
        if (bar) {
            bar.style.width = `${castPower}%`;
        }
    }

    function updateReelingUI() {
        if (!fishingUI) return;

        // Show/hide containers
        const castContainer = fishingUI.querySelector('#cast-power-container');
        const reelingContainer = fishingUI.querySelector('#reeling-container');
        if (castContainer) castContainer.style.display = castPhase === 'aiming' ? 'block' : 'none';
        if (reelingContainer) reelingContainer.style.display = castPhase === 'reeling' ? 'block' : 'none';

        if (castPhase !== 'reeling') return;

        // Progress bar
        const progressBar = fishingUI.querySelector('#fish-progress-bar');
        if (progressBar) {
            progressBar.style.width = `${fishProgress}%`;
        }

        // Timing marker
        const marker = fishingUI.querySelector('#timing-marker');
        if (marker) {
            marker.style.left = `${reelTiming * 100}%`;
        }

        // Fish info
        const fishInfo = fishingUI.querySelector('#fish-info');
        if (fishInfo && hookedFish) {
            fishInfo.textContent = `${hookedFish.name} (${hookedFish.weight}kg) - ${hookedFish.rarity.toUpperCase()}`;
        }
    }

    function getInventory() {
        return { ...inventory };
    }

    // === KEYBOARD HANDLER ===

    function setupKeyboardHandler() {
        document.addEventListener('keydown', (e) => {
            // E-Taste: NUR wenn am Angelspot UND kein Gebäude in der Nähe
            if (e.code === 'KeyE' && currentSpot && !isFishing) {
                // Check if near building (Building hat Priorität!)
                const buildingPrompt = document.getElementById('building-prompt-ui');
                if (buildingPrompt && buildingPrompt.style.display === 'block') {
                    return; // Building hat Priorität!
                }
                // Check if in garden area
                const gardenUI = document.getElementById('garden-ui');
                if (gardenUI && gardenUI.style.display === 'block') {
                    return; // Garden hat Priorität!
                }
                startFishing();
            }
            if (e.code === 'Space' && isFishing) {
                e.preventDefault();
                reel();
            }
        });
    }

    // ============================================
    // EQUIPMENT FUNCTIONS
    // ============================================

    function equipRod(rodId) {
        if (!FISHING_RODS[rodId]) return false;
        if (!ownedRods.includes(rodId)) {
            if (typeof notify === 'function') {
                notify(`❌ Du besitzt diese Angel nicht!`, 'warning');
            }
            return false;
        }
        equippedRod = rodId;
        const rod = FISHING_RODS[rodId];
        if (typeof notify === 'function') {
            notify(`${rod.icon} ${rod.name} ausgerüstet!`, 'success');
        }
        return true;
    }

    function equipBait(baitId) {
        if (!BAITS[baitId]) return false;
        if (!baitInventory[baitId] || baitInventory[baitId] <= 0) {
            if (typeof notify === 'function') {
                notify(`❌ Kein ${BAITS[baitId].name} mehr!`, 'warning');
            }
            return false;
        }
        equippedBait = baitId;
        const bait = BAITS[baitId];
        if (typeof notify === 'function') {
            notify(`${bait.icon} ${bait.name} ausgerüstet!`, 'success');
        }
        return true;
    }

    function buyRod(rodId) {
        if (!FISHING_RODS[rodId]) return false;
        if (ownedRods.includes(rodId)) {
            if (typeof notify === 'function') {
                notify(`Du hast diese Angel bereits!`, 'info');
            }
            return false;
        }
        const rod = FISHING_RODS[rodId];
        if (inventory.totalValue < rod.price) {
            if (typeof notify === 'function') {
                notify(`❌ Nicht genug Gold! (${rod.price}G benötigt)`, 'warning');
            }
            return false;
        }
        inventory.totalValue -= rod.price;
        ownedRods.push(rodId);
        if (typeof notify === 'function') {
            notify(`${rod.icon} ${rod.name} gekauft!`, 'success');
        }
        return true;
    }

    function buyBait(baitId, amount = 1) {
        if (!BAITS[baitId]) return false;
        const bait = BAITS[baitId];
        const cost = bait.price * amount;
        if (inventory.totalValue < cost) {
            if (typeof notify === 'function') {
                notify(`❌ Nicht genug Gold!`, 'warning');
            }
            return false;
        }
        inventory.totalValue -= cost;
        baitInventory[baitId] = (baitInventory[baitId] || 0) + (bait.uses * amount);
        if (typeof notify === 'function') {
            notify(`${bait.icon} ${amount}x ${bait.name} gekauft!`, 'success');
        }
        return true;
    }

    // ============================================
    // AQUARIUM FUNCTIONS
    // ============================================

    function buyAquarium(tankId) {
        if (!AQUARIUM.tanks[tankId]) return false;
        const tank = AQUARIUM.tanks[tankId];
        if (inventory.totalValue < tank.price) {
            if (typeof notify === 'function') {
                notify(`❌ Nicht genug Gold! (${tank.price}G benötigt)`, 'warning');
            }
            return false;
        }
        inventory.totalValue -= tank.price;
        ownedTank = tankId;
        if (typeof notify === 'function') {
            notify(`🐠 ${tank.name} gekauft!`, 'success');
        }
        return true;
    }

    function addToAquarium(fishName) {
        if (!ownedTank) {
            if (typeof notify === 'function') {
                notify(`❌ Du brauchst erst ein Aquarium!`, 'warning');
            }
            return false;
        }
        const tank = AQUARIUM.tanks[ownedTank];
        if (aquariumFish.length >= tank.capacity) {
            if (typeof notify === 'function') {
                notify(`❌ Aquarium ist voll!`, 'warning');
            }
            return false;
        }
        if (!inventory.fish[fishName] || inventory.fish[fishName] <= 0) {
            if (typeof notify === 'function') {
                notify(`❌ Du hast keinen ${fishName}!`, 'warning');
            }
            return false;
        }
        inventory.fish[fishName]--;
        aquariumFish.push({ name: fishName, addedAt: Date.now() });
        if (typeof notify === 'function') {
            notify(`🐠 ${fishName} ins Aquarium gesetzt!`, 'success');
        }
        return true;
    }

    function removeFromAquarium(index) {
        if (index < 0 || index >= aquariumFish.length) return false;
        const fish = aquariumFish.splice(index, 1)[0];
        inventory.fish[fish.name] = (inventory.fish[fish.name] || 0) + 1;
        if (typeof notify === 'function') {
            notify(`🐠 ${fish.name} aus Aquarium genommen!`, 'info');
        }
        return true;
    }

    function getAquariumInfo() {
        return {
            tank: ownedTank ? AQUARIUM.tanks[ownedTank] : null,
            fish: [...aquariumFish],
            capacity: ownedTank ? AQUARIUM.tanks[ownedTank].capacity : 0
        };
    }

    // ============================================
    // FISH COLLECTION (Pokedex)
    // ============================================

    function updateCollection(fishName, weight) {
        if (!fishCollection[fishName]) {
            fishCollection[fishName] = { caught: 0, maxWeight: 0 };
            if (typeof notify === 'function') {
                notify(`📖 Neue Fischart entdeckt: ${fishName}!`, 'success');
            }
        }
        fishCollection[fishName].caught++;
        if (parseFloat(weight) > fishCollection[fishName].maxWeight) {
            fishCollection[fishName].maxWeight = parseFloat(weight);
            if (typeof notify === 'function') {
                notify(`🏆 Neuer Rekord: ${fishName} (${weight}kg)!`, 'success');
            }
        }
    }

    function getCollection() {
        return { ...fishCollection };
    }

    function getCollectionProgress() {
        // Zähle alle einzigartigen Fische im Spiel
        const allFish = new Set();
        FISHING_CONFIG.spots.forEach(spot => {
            spot.fische.forEach(f => allFish.add(f.name));
        });
        const discovered = Object.keys(fishCollection).length;
        return { discovered, total: allFish.size, percentage: Math.round((discovered / allFish.size) * 100) };
    }

    // ============================================
    // SHOP UI
    // ============================================

    function openFishingShop() {
        const shopHTML = `
            <div id="fishing-shop" style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(20, 40, 60, 0.98);
                border: 3px solid #4a9eff;
                border-radius: 15px;
                padding: 20px;
                z-index: 2000;
                max-width: 500px;
                max-height: 80vh;
                overflow-y: auto;
            ">
                <h2 style="color: #4a9eff; text-align: center; margin-bottom: 15px;">🎣 Angel-Shop</h2>
                <p style="text-align: center; color: gold;">💰 ${inventory.totalValue}G</p>

                <h3 style="color: #88ff88; margin: 15px 0 10px;">Angelruten:</h3>
                ${Object.entries(FISHING_RODS).map(([id, rod]) => `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: rgba(0,0,0,0.3); margin: 5px 0; border-radius: 5px;">
                        <span>${rod.icon} ${rod.name} ${ownedRods.includes(id) ? '✓' : ''}</span>
                        <span style="color: ${ownedRods.includes(id) ? '#6f6' : '#ff6'};">${ownedRods.includes(id) ? 'Besitzt' : rod.price + 'G'}</span>
                        ${!ownedRods.includes(id) ? `<button onclick="window.FishingSystem.buyRod('${id}')" style="padding: 5px 10px; cursor: pointer;">Kaufen</button>` : ''}
                    </div>
                `).join('')}

                <h3 style="color: #ffaa00; margin: 15px 0 10px;">Köder:</h3>
                ${Object.entries(BAITS).map(([id, bait]) => `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: rgba(0,0,0,0.3); margin: 5px 0; border-radius: 5px;">
                        <span>${bait.icon} ${bait.name} (${baitInventory[id] || 0}x)</span>
                        <span style="color: #ff6;">${bait.price}G</span>
                        <button onclick="window.FishingSystem.buyBait('${id}', 1)" style="padding: 5px 10px; cursor: pointer;">+1</button>
                        <button onclick="window.FishingSystem.buyBait('${id}', 5)" style="padding: 5px 10px; cursor: pointer;">+5</button>
                    </div>
                `).join('')}

                <h3 style="color: #00bfff; margin: 15px 0 10px;">Aquarien:</h3>
                ${Object.entries(AQUARIUM.tanks).map(([id, tank]) => `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: rgba(0,0,0,0.3); margin: 5px 0; border-radius: 5px;">
                        <span>🐠 ${tank.name} (${tank.capacity} Fische)</span>
                        <span style="color: ${ownedTank === id ? '#6f6' : '#ff6'};">${ownedTank === id ? 'Besitzt' : tank.price + 'G'}</span>
                        ${ownedTank !== id ? `<button onclick="window.FishingSystem.buyAquarium('${id}')" style="padding: 5px 10px; cursor: pointer;">Kaufen</button>` : ''}
                    </div>
                `).join('')}

                <button onclick="document.getElementById('fishing-shop').remove()" style="
                    display: block;
                    width: 100%;
                    margin-top: 15px;
                    padding: 10px;
                    background: #666;
                    border: none;
                    border-radius: 5px;
                    color: white;
                    cursor: pointer;
                ">Schließen</button>
            </div>
        `;

        // Remove old shop if exists
        const oldShop = document.getElementById('fishing-shop');
        if (oldShop) oldShop.remove();

        document.body.insertAdjacentHTML('beforeend', shopHTML);
    }

    // === EXPORT ===

    window.FishingSystem = {
        init,
        checkNearSpot,
        startFishing,
        updateFishing,
        reel,
        cancelFishing,
        getInventory,
        // Equipment
        equipRod,
        equipBait,
        buyRod,
        buyBait,
        getEquippedRod: () => equippedRod,
        getEquippedBait: () => equippedBait,
        getBaitInventory: () => ({ ...baitInventory }),
        getOwnedRods: () => [...ownedRods],
        getRodInfo: (id) => FISHING_RODS[id],
        getBaitInfo: (id) => BAITS[id],
        // Aquarium
        buyAquarium,
        addToAquarium,
        removeFromAquarium,
        getAquariumInfo,
        // Collection
        getCollection,
        getCollectionProgress,
        // Shop
        openFishingShop,
        // State
        get isFishing() { return isFishing; },
        get currentSpot() { return currentSpot; }
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

    console.log('🎣 Fishing System loaded!');
})();
