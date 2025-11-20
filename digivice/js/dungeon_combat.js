/**
 * DUNGEON COMBAT SYSTEM
 * Verbindet Dungeon-Generator + Enemy-System + Player-Combat
 */

(function() {
    'use strict';

    let currentDungeon = null;
    let playerHealth = 100;
    let playerMaxHealth = 100;
    let playerDamage = 15;
    let combatActive = false;
    let lastHitNotification = 0; // Throttle hit notifications
    // Auto-attack removed - manual only via SPACE

    // CommandSystem Integration
    let commandSystem = null;
    if (typeof CommandSystem !== 'undefined') {
        commandSystem = new CommandSystem();
        console.log('✅ CommandSystem initialized for combat');
    } else {
        console.warn('⚠️ CommandSystem not available');
    }

    /**
     * Startet Dungeon mit Gegnern
     */
    function startDungeonCombat(level = 1, scene, roomName = null) {
        if (!window.DungeonGenerator || !window.DungeonEnemies) {
            console.error('❌ DungeonGenerator or DungeonEnemies not loaded!');
            return null;
        }

        // Auto-detect dungeon room if not specified
        if (!roomName && window.currentRoom) {
            roomName = window.currentRoom;
        }

        // Support all dungeon types
        const validDungeons = [
            'Kampfarena',
            'Dungeon des Schattens',
            'Dungeon der Explosion',
            'Dungeon des Chaos'
        ];

        // Default to first dungeon if not valid
        if (!roomName || !validDungeons.includes(roomName)) {
            roomName = 'Dungeon des Schattens';
        }

        console.log(`🏰 Starting Dungeon Combat in "${roomName}" - Level ${level}`);

        // Clear old enemies
        if (window.DungeonEnemies) {
            DungeonEnemies.clearAllEnemies();
        }

        // Generate new dungeon for the specific room
        const dungeonConfig = DungeonGenerator.regenerateDungeon(roomName, level);
        if (!dungeonConfig || !dungeonConfig.dungeon) {
            console.error('❌ Failed to generate dungeon config');
            return null;
        }

        currentDungeon = dungeonConfig.dungeon;
        currentDungeon.level = level;

        // Spawn enemies
        DungeonEnemies.spawnEnemies(currentDungeon, scene);

        // Reset player health
        playerHealth = playerMaxHealth;
        combatActive = true;

        // Update UI
        updateCombatUI();

        // Setup event listeners
        setupCombatEvents();

        console.log(`✅ Dungeon Combat started! ${currentDungeon.enemies.length} enemies spawned`);
        return currentDungeon;
    }

    /**
     * Player attacks nearest enemy
     */
    function playerAttack(playerPosition) {
        if (!combatActive || !playerPosition) return;

        const enemy = DungeonEnemies.damageNearestEnemy(playerPosition, playerDamage, 5);

        if (enemy) {
            console.log(`⚔️ Player hit ${enemy.data.name}!`);

            // Visual feedback - throttled to max 1 per 8 seconds
            const now = Date.now();
            if (typeof notify === 'function' && now - lastHitNotification > 8000) {
                notify(`⚔️ Hit! -${playerDamage} HP`, 'success');
                lastHitNotification = now;
            }

            // Check if all enemies dead -> WIN
            checkVictoryCondition();
        }
        // Removed "No enemy in range" spam notification

        updateCombatUI();
    }

    /**
     * Auto-Attack toggle
     */
    // Auto-attack function removed - manual combat only

    /**
     * Enemy attacks player (called from enemy system)
     */
    window.onEnemyAttack = function(damage, enemyPosition) {
        if (!combatActive) return;

        playerHealth = Math.max(0, playerHealth - damage);
        console.log(`💥 Player took ${damage} damage! HP: ${playerHealth}/${playerMaxHealth}`);

        if (typeof notify === 'function') {
            notify(`💥 Took ${damage} damage!`, 'error');
        }

        updateCombatUI();

        if (playerHealth <= 0) {
            gameOver();
        }
    };

    /**
     * Enemy killed (called from enemy system)
     */
    window.onEnemyKilled = async function(xp, loot, position) {
        console.log(`💀 Enemy defeated! +${xp} XP, Loot:`, loot);

        if (typeof notify === 'function') {
            notify(`+${xp} XP | Loot: ${loot.join(', ')}`, 'success');
        }

        // Add XP to player - Connect to backend
        try {
            const response = await fetch(`${API_URL}/api/game/add-xp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ xp: xp })
            });

            if (response.ok) {
                const data = await response.json();
                console.log('✅ XP added to backend:', data);

                // Check for level up
                if (data.leveledUp) {
                    if (typeof notify === 'function') {
                        notify(`🎉 LEVEL UP! Now Level ${data.newLevel}!`, 'success');
                    }
                }
            }
        } catch (error) {
            console.warn('⚠️ Failed to sync XP to backend:', error);
        }

        // Spawn loot items in 3D scene
        if (loot && loot.length > 0 && position) {
            window.spawnLootItems(loot, position);
        }

        // Update UI
        updateCombatUI();

        // Check victory
        checkVictoryCondition();
    };

    /**
     * Check if all enemies dead
     */
    function checkVictoryCondition() {
        const livingEnemies = DungeonEnemies.getLivingEnemies();

        if (livingEnemies.length === 0 && combatActive) {
            victory();
        }
    }

    /**
     * Victory!
     */
    function victory() {
        combatActive = false;
        // Auto-attack removed

        // Remove combat UI
        const healthDisplay = document.getElementById('player-health-display');
        if (healthDisplay) {
            healthDisplay.remove();
        }

        console.log('🎉 VICTORY! Dungeon cleared!');

        if (typeof notify === 'function') {
            notify(`🎉 VICTORY! Level ${currentDungeon.level} cleared!`, 'success');
        }

        // Show victory UI
        showVictoryScreen();
    }

    /**
     * Game Over
     */
    function gameOver() {
        combatActive = false;
        // Auto-attack removed

        // Remove combat UI
        const healthDisplay = document.getElementById('player-health-display');
        if (healthDisplay) {
            healthDisplay.remove();
        }

        console.log('💀 GAME OVER');

        if (typeof notify === 'function') {
            notify('💀 DEFEATED! Dungeon failed...', 'error');
        }

        // Clear enemies
        DungeonEnemies.clearAllEnemies();

        // Show game over UI
        showGameOverScreen();
    }

    /**
     * Update Combat UI
     */
    function updateCombatUI() {
        // Update health bar in header
        const healthPercent = Math.floor((playerHealth / playerMaxHealth) * 100);

        // Find or create health display (under chat input)
        let healthDisplay = document.getElementById('player-health-display');
        if (!healthDisplay) {
            healthDisplay = document.createElement('div');
            healthDisplay.id = 'player-health-display';
            healthDisplay.style.cssText = `
                position: fixed;
                bottom: 70px;
                left: 0;
                right: 0;
                background: rgba(0,0,0,0.9);
                padding: 8px 20px;
                color: white;
                font-family: monospace;
                z-index: 900;
                border-top: 2px solid #667eea;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.9rem;
            `;
            document.body.appendChild(healthDisplay);
        }

        // Color based on health
        let healthColor;
        if (healthPercent > 60) healthColor = '#00ff00';
        else if (healthPercent > 30) healthColor = '#ffff00';
        else healthColor = '#ff0000';

        const enemyCount = DungeonEnemies.getLivingEnemies().length;

        // CommandSystem Buttons
        let commandButtons = '';
        if (commandSystem) {
            const commands = commandSystem.getAvailableCommands();

            // Get happiness/discipline directly from DOM (Najika Status display)
            const happinessEl = document.getElementById('najikaHappiness');
            const disciplineEl = document.getElementById('najikaDiscipline');
            const happiness = happinessEl ? parseInt(happinessEl.textContent) : 50;
            const discipline = disciplineEl ? parseInt(disciplineEl.textContent) : 50;

            commandButtons = `
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span style="color: #ffcc00;">😊${happiness}</span>
                    <span style="color: #cc88ff;">💪${discipline}</span>
                    ${commands.commands.map(cmd => `
                        <button class="cmd-btn" data-key="${cmd.key}" style="background: #667eea; color: white; border: none; padding: 6px 14px; cursor: pointer; border-radius: 4px; font-weight: bold; font-size: 0.85rem;">
                            ${cmd.icon} ${cmd.label}
                        </button>
                    `).join('')}
                    <button id="praise-btn" style="background: #00ff00; color: black; border: none; padding: 4px 10px; cursor: pointer; border-radius: 4px; font-size: 0.8rem;">👍</button>
                    <button id="scold-btn" style="background: #ff0000; color: white; border: none; padding: 4px 10px; cursor: pointer; border-radius: 4px; font-size: 0.8rem;">👎</button>
                    <button id="exit-combat-btn" style="background: #ff8800; color: white; border: none; padding: 4px 10px; cursor: pointer; border-radius: 4px; font-size: 0.8rem; font-weight: bold;">🚪 Beenden</button>
                </div>
            `;
        }

        healthDisplay.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                <div style="display: flex; gap: 15px;">
                    <span style="font-weight: bold;">⚔️ COMBAT</span>
                    <span style="color: ${healthColor};">HP: ${playerHealth}/${playerMaxHealth}</span>
                    <span style="color: #ff8888;">Enemies: ${enemyCount}</span>
                    <span style="color: #88ff88;">Lv ${currentDungeon?.level || 1}</span>
                </div>
                ${commandButtons}
            </div>
        `;

        // Attach button listeners
        if (commandSystem) {
            // Command Buttons (1-4)
            document.querySelectorAll('.cmd-btn').forEach(btn => {
                btn.onclick = () => {
                    const key = btn.dataset.key;
                    const result = commandSystem.executeCommand(key, 'idle');

                    if (result.success) {
                        // Execute actual attack via battle API
                        if (window.Scene3D?.character?.position) {
                            playerAttack(window.Scene3D.character.position);
                        }

                        if (typeof notify === 'function' && result.timing) {
                            notify(`${result.timing.message || 'Command executed'}`,
                                   result.timing.quality === 'perfect' ? 'success' : 'info');
                        }
                    } else {
                        if (typeof notify === 'function') {
                            notify(result.message, 'error');
                        }
                    }

                    updateCombatUI();
                };
            });

            // Praise/Scold
            const praiseBtn = document.getElementById('praise-btn');
            const scoldBtn = document.getElementById('scold-btn');

            if (praiseBtn) {
                praiseBtn.onclick = async () => {
                    const result = await commandSystem.praise('after_good_move');
                    if (typeof notify === 'function') {
                        notify(`💚 ${result.message}`, 'success');
                    }

                    // Update Najika Status HUD (happiness/discipline in DOM)
                    if (typeof updateNajikaHUD === 'function' && result.happiness !== undefined) {
                        updateNajikaHUD({
                            happiness: result.happiness,
                            discipline: result.discipline
                        });
                    }

                    updateCombatUI();
                };
            }

            if (scoldBtn) {
                scoldBtn.onclick = async () => {
                    const result = await commandSystem.scold('after_mistake');
                    if (typeof notify === 'function') {
                        notify(`💢 ${result.message}`, 'error');
                    }

                    // Update Najika Status HUD (happiness/discipline in DOM)
                    if (typeof updateNajikaHUD === 'function' && result.happiness !== undefined) {
                        updateNajikaHUD({
                            happiness: result.happiness,
                            discipline: result.discipline
                        });
                    }

                    updateCombatUI();
                };
            }

            // Exit Combat Button
            const exitCombatBtn = document.getElementById('exit-combat-btn');
            if (exitCombatBtn) {
                exitCombatBtn.onclick = () => {
                    if (confirm('Kampf wirklich beenden?')) {
                        exitDungeon();
                        if (typeof notify === 'function') {
                            notify('🚪 Kampf beendet', 'info');
                        }
                    }
                };
            }
        }
    }

    /**
     * Show victory screen
     */
    function showVictoryScreen() {
        const victoryDiv = document.createElement('div');
        victoryDiv.style.cssText = `
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.5s;
        `;

        victoryDiv.innerHTML = `
            <div style="
                background: linear-gradient(135deg, #667eea, #764ba2);
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                color: white;
                max-width: 500px;
            ">
                <h1 style="font-size: 3rem; margin: 0 0 20px 0;">🎉 VICTORY! 🎉</h1>
                <p style="font-size: 1.5rem; margin: 10px 0;">Dungeon Level ${currentDungeon.level} Cleared!</p>
                <p style="font-size: 1rem; margin: 20px 0; opacity: 0.9;">
                    Health Remaining: ${playerHealth}/${playerMaxHealth}
                </p>
                <button id="nextLevelBtn" style="
                    padding: 15px 30px;
                    font-size: 1.2rem;
                    background: #00ff00;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    margin: 10px;
                    font-weight: bold;
                ">Next Level ➡️</button>
                <button id="exitDungeonBtn" style="
                    padding: 15px 30px;
                    font-size: 1.2rem;
                    background: #ff4444;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    margin: 10px;
                    color: white;
                    font-weight: bold;
                ">Exit Dungeon</button>
            </div>
        `;

        document.body.appendChild(victoryDiv);

        // Event listeners
        document.getElementById('nextLevelBtn').onclick = () => {
            document.body.removeChild(victoryDiv);
            const nextLevel = (currentDungeon?.level || 1) + 1;
            startDungeonCombat(nextLevel, window.Scene3D?.scene);
        };

        document.getElementById('exitDungeonBtn').onclick = () => {
            document.body.removeChild(victoryDiv);
            exitDungeon();
        };
    }

    /**
     * Exit dungeon (clean up)
     */
    function exitDungeon() {
        combatActive = false;
        currentDungeon = null;  // Reset combat state!

        DungeonEnemies.clearAllEnemies();

        const healthDisplay = document.getElementById('player-health-display');
        if (healthDisplay) {
            healthDisplay.remove();
        }

        console.log('🚪 Exited dungeon');
    }

    /**
     * Setup combat event listeners
     */
    function setupCombatEvents() {
        // Keyboard: Space = Attack (nur wenn kein Input aktiv ist)
        const attackHandler = (e) => {
            // Ignore wenn Input/Textarea fokussiert ist
            const activeElement = document.activeElement;
            if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
                return;
            }

            if (e.code === 'Space' && combatActive) {
                e.preventDefault();
                if (window.Scene3D && Scene3D.characterGroup) {
                    const playerPos = Scene3D.characterGroup.position.clone();
                    playerAttack(playerPos);
                }
            }
        };

        document.addEventListener('keydown', attackHandler);

        // Store handlers for cleanup
        window._dungeonCombatHandlers = { attackHandler };
    }

    /**
     * Update combat (call every frame)
     */
    function updateCombat() {
        if (!combatActive) return;

        // Get player position
        if (window.Scene3D && Scene3D.characterGroup) {
            const playerPos = Scene3D.characterGroup.position.clone();

            // Update all enemies
            DungeonEnemies.updateEnemies(playerPos);
        }
    }

    // Public API
    window.DungeonCombat = {
        startDungeonCombat,
        playerAttack,
        updateCombat,
        exitDungeon,
        isActive: () => combatActive,
        getPlayerHealth: () => playerHealth,
        healPlayer: (amount) => {
            playerHealth = Math.min(playerMaxHealth, playerHealth + amount);
            updateCombatUI();
        }
    };

    /**
     * Show Victory Screen UI
     */
    function showVictoryScreen() {
        const overlay = document.createElement('div');
        overlay.id = 'victory-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            animation: fadeIn 0.5s;
        `;

        overlay.innerHTML = `
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; text-align: center; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.5);">
                <h1 style="color: #ffd700; font-size: 3rem; margin: 0 0 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🎉 VICTORY! 🎉</h1>
                <p style="color: white; font-size: 1.5rem; margin: 10px 0;">Dungeon Level ${currentDungeon?.level || 1} Cleared!</p>
                <p style="color: #ffeb3b; font-size: 1.2rem; margin: 20px 0;">Enemies Defeated: ${currentDungeon?.enemyCount || 0}</p>
                <div style="margin: 30px 0;">
                    <button id="continue-btn" style="background: #4caf50; color: white; border: none; padding: 15px 40px; font-size: 1.2rem; border-radius: 10px; cursor: pointer; margin-right: 10px; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                        ✨ Continue
                    </button>
                    <button id="retry-btn" style="background: #ff9800; color: white; border: none; padding: 15px 40px; font-size: 1.2rem; border-radius: 10px; cursor: pointer; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                        🔄 Next Level
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        document.getElementById('continue-btn').onclick = () => {
            overlay.remove();
            exitDungeon();
        };

        document.getElementById('retry-btn').onclick = () => {
            overlay.remove();
            const nextLevel = (currentDungeon?.level || 1) + 1;
            startDungeonCombat(nextLevel, window.Scene3D?.scene);
        };
    }

    /**
     * Show Game Over Screen UI
     */
    function showGameOverScreen() {
        const overlay = document.createElement('div');
        overlay.id = 'gameover-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            animation: fadeIn 0.5s;
        `;

        overlay.innerHTML = `
            <div style="background: linear-gradient(135deg, #c31432 0%, #240b36 100%); padding: 40px; border-radius: 20px; text-align: center; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7);">
                <h1 style="color: #ff4444; font-size: 3rem; margin: 0 0 20px 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.8);">💀 DEFEATED 💀</h1>
                <p style="color: white; font-size: 1.5rem; margin: 10px 0;">Dungeon Level ${currentDungeon?.level || 1}</p>
                <p style="color: #ffcccc; font-size: 1.1rem; margin: 20px 0;">You have fallen in battle...</p>
                <div style="margin: 30px 0;">
                    <button id="retry-gameover-btn" style="background: #f44336; color: white; border: none; padding: 15px 40px; font-size: 1.2rem; border-radius: 10px; cursor: pointer; margin-right: 10px; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                        🔄 Try Again
                    </button>
                    <button id="exit-gameover-btn" style="background: #666; color: white; border: none; padding: 15px 40px; font-size: 1.2rem; border-radius: 10px; cursor: pointer; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                        🚪 Exit
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        document.getElementById('retry-gameover-btn').onclick = () => {
            overlay.remove();
            startDungeonCombat(currentDungeon?.level || 1, window.Scene3D?.scene);
        };

        document.getElementById('exit-gameover-btn').onclick = () => {
            overlay.remove();
            exitDungeon();
        };
    }

    /**
     * Spawn loot items in 3D scene
     */
    window.spawnLootItems = function(loot, position) {
        if (!window.Scene3D || !window.Scene3D.scene) {
            console.warn('⚠️ Scene3D not available for loot spawning');
            return;
        }

        const scene = window.Scene3D.scene;

        loot.forEach((item, index) => {
            // Create glowing cube for loot
            const geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
            const material = new THREE.MeshStandardMaterial({
                color: getLootColor(item),
                emissive: getLootColor(item),
                emissiveIntensity: 0.5,
                metalness: 0.8,
                roughness: 0.2
            });

            const lootMesh = new THREE.Mesh(geometry, material);

            // Offset each item slightly
            const offset = index * 0.7;
            lootMesh.position.set(
                position.x + Math.cos(index * 1.5) * offset,
                position.y + 0.5,
                position.z + Math.sin(index * 1.5) * offset
            );

            lootMesh.userData.lootItem = item;
            lootMesh.userData.type = 'loot';

            // Add floating animation
            lootMesh.userData.floatOffset = index * Math.PI / 3;
            lootMesh.userData.animate = (time) => {
                lootMesh.position.y = position.y + 0.5 + Math.sin(time * 0.002 + lootMesh.userData.floatOffset) * 0.2;
                lootMesh.rotation.y += 0.02;
            };

            scene.add(lootMesh);

            // Add glowing beam effect
            const beamGeometry = new THREE.CylinderGeometry(0.1, 0.3, 5, 8);
            const beamMaterial = new THREE.MeshBasicMaterial({
                color: getLootColor(item),
                transparent: true,
                opacity: 0.3
            });
            const beam = new THREE.Mesh(beamGeometry, beamMaterial);
            beam.position.copy(lootMesh.position);
            beam.position.y += 2.5;
            scene.add(beam);

            console.log(`✨ Spawned loot: ${item} at`, position);
        });
    };

    /**
     * Get color for loot rarity
     */
    function getLootColor(itemName) {
        const lower = itemName.toLowerCase();
        if (lower.includes('legendary') || lower.includes('epic')) return 0xffd700;
        if (lower.includes('rare')) return 0x9b59b6;
        if (lower.includes('uncommon')) return 0x3498db;
        return 0x95a5a6; // Common
    }

    console.log('⚔️ Dungeon Combat System initialized');
    console.log('Controls: SPACE = Attack');
})();
