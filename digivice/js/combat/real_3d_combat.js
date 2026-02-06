/**
 * REAL 3D COMBAT SYSTEM - Najika World
 * =====================================
 *
 * ERSETZT den Text-basierten Kampf mit ECHTEN 3D Gegnern!
 *
 * Nutzt:
 * - KayKit 3D Models (Skelette, Adventurers, etc.)
 * - Echte Hitboxen und Kollisionen
 * - Visuelle Angriffs-Animationen
 *
 * MODES:
 * - MANUAL: Q/E für Angriffe, Space für Dodge
 * - AUTO: KI kämpft
 * - CHEER: Anfeuern (Digimon Style)
 */

(function() {
    'use strict';

    // ==========================================
    // COMBAT STATE
    // ==========================================

    let combatActive = false;
    let combatMode = 'MANUAL'; // MANUAL, AUTO, CHEER
    let currentEnemies = [];
    let playerStats = {
        hp: 100,
        maxHp: 100,
        stamina: 100,
        maxStamina: 100,
        mana: 100,
        maxMana: 100
    };

    // Combo System
    let comboCount = 0;
    let lastAttackTime = 0;
    const COMBO_WINDOW = 1500; // 1.5 seconds

    // Cooldowns
    let attackCooldown = 0;
    let dodgeCooldown = 0;
    let skillCooldowns = {};

    // Animation
    let animationFrame = null;
    const clock = new THREE.Clock();

    // ==========================================
    // KAYKIT ENEMY MODELS MAPPING
    // ==========================================

    const KAYKIT_MODELS = {
        // Skeletons
        skeleton_warrior: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_warrior.gltf',
        skeleton_archer: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_archer.gltf',
        skeleton_mage: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_mage.gltf',
        skeleton_minion: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_minion.gltf',

        // Dungeon Pack Characters
        knight: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf',
        barbarian: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_barbarian.gltf',
        mage: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_mage.gltf',
        rogue: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_rogue.gltf',

        // Halloween
        witch: 'KayKit Spooktober Seasonal Pack 1.1/Models/Characters/Witch/gltf/character_witch.gltf',

        // Generic fallback
        default: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf'
    };

    // ==========================================
    // ENEMY TYPES WITH STATS
    // ==========================================

    const ENEMY_TYPES = {
        // === TIER 1: Easy ===
        bat: {
            name: 'Höhlenfledermaus',
            model: 'skeleton_minion',
            hp: 15, damage: 3, speed: 2.0,
            attackRange: 2, xp: 5, tier: 1,
            loot: ['bat_wing']
        },
        slime: {
            name: 'Schleim',
            model: 'default',
            hp: 20, damage: 2, speed: 0.5,
            attackRange: 1.5, xp: 8, tier: 1,
            loot: ['slime_goo'],
            color: 0x00ff00
        },
        skeleton_warrior: {
            name: 'Skelett-Krieger',
            model: 'skeleton_warrior',
            hp: 30, damage: 8, speed: 1.2,
            attackRange: 2.5, xp: 15, tier: 1,
            loot: ['bone', 'sword_rusty']
        },
        skeleton_archer: {
            name: 'Skelett-Bogenschütze',
            model: 'skeleton_archer',
            hp: 20, damage: 10, speed: 1.0,
            attackRange: 10, xp: 18, tier: 1,
            loot: ['bone', 'arrow']
        },

        // === TIER 2: Medium ===
        wolf: {
            name: 'Wolf',
            model: 'skeleton_minion',
            hp: 40, damage: 12, speed: 2.5,
            attackRange: 2, xp: 25, tier: 2,
            loot: ['wolf_pelt', 'wolf_fang'],
            color: 0x888888
        },
        goblin: {
            name: 'Goblin',
            model: 'rogue',
            hp: 35, damage: 10, speed: 1.8,
            attackRange: 2, xp: 22, tier: 2,
            loot: ['gold_coin', 'dagger_crude'],
            color: 0x00aa00
        },
        skeleton_mage: {
            name: 'Skelett-Magier',
            model: 'skeleton_mage',
            hp: 25, damage: 18, speed: 0.8,
            attackRange: 8, xp: 30, tier: 2,
            loot: ['bone', 'magic_crystal']
        },

        // === TIER 3: Hard ===
        corrupted_knight: {
            name: 'Verfluchter Ritter',
            model: 'knight',
            hp: 80, damage: 20, speed: 1.0,
            attackRange: 3, xp: 60, tier: 3,
            loot: ['cursed_sword', 'plate_armor_broken'],
            color: 0x440044
        },
        witch: {
            name: 'Hexe',
            model: 'witch',
            hp: 60, damage: 25, speed: 0.9,
            attackRange: 10, xp: 70, tier: 3,
            loot: ['witch_hat', 'potion_empty', 'spell_scroll']
        },

        // === TIER 4: Boss ===
        barbarian_boss: {
            name: 'Berserker-Untoter',
            model: 'barbarian',
            hp: 200, damage: 35, speed: 0.7,
            attackRange: 3, xp: 150, tier: 4,
            loot: ['great_axe', 'berserker_helm', 'rare_gem'],
            isBoss: true
        }
    };

    // ==========================================
    // BIOME -> ENEMY MAPPING (Fixes null biome bug!)
    // ==========================================

    const BIOME_ENEMIES = {
        // === NAJIKA WORLD BIOME NAMES (from overworld_enemies.js) ===
        'samtmoos': ['wolf', 'skeleton_warrior', 'goblin', 'bat'],
        'reich_der_drei': ['skeleton_warrior', 'skeleton_mage', 'wolf'],
        'heisse_duenen': ['skeleton_archer', 'skeleton_mage', 'goblin'],
        'salzwind': ['slime', 'skeleton_warrior', 'bat'],
        'magmastroeme': ['skeleton_warrior', 'corrupted_knight', 'bat', 'skeleton_mage'],
        'gruenschlamm': ['witch', 'slime', 'skeleton_mage', 'bat'],
        'blitzebene': ['wolf', 'goblin', 'corrupted_knight'],
        'tiefenhoehlen': ['bat', 'goblin', 'skeleton_mage', 'slime'],
        'goetterfels': [], // Safe zone - no enemies!

        // === GENERIC BIOME ALIASES ===
        'forest': ['wolf', 'skeleton_warrior', 'goblin', 'bat'],
        'desert': ['skeleton_archer', 'skeleton_mage', 'goblin'],
        'coast': ['slime', 'skeleton_warrior', 'bat'],
        'swamp': ['witch', 'slime', 'skeleton_mage', 'bat'],
        'ice': ['skeleton_warrior', 'skeleton_mage', 'wolf'],
        'volcano': ['skeleton_warrior', 'corrupted_knight', 'bat'],
        'highland': ['wolf', 'goblin', 'corrupted_knight'],
        'caves': ['bat', 'goblin', 'skeleton_mage', 'slime'],
        'mountain': ['wolf', 'skeleton_archer', 'corrupted_knight'],

        // Fallback for null/undefined biome
        'null': ['skeleton_warrior', 'bat', 'slime'],
        'undefined': ['skeleton_warrior', 'bat', 'slime'],
        'default': ['skeleton_warrior', 'bat', 'slime']
    };

    // ==========================================
    // 3D ENEMY CLASS
    // ==========================================

    class Enemy3D {
        constructor(type, position, level = 1, scene) {
            this.type = type;
            this.data = ENEMY_TYPES[type] || ENEMY_TYPES.skeleton_warrior;
            this.level = level;
            this.scene = scene;

            // Stats scaled by level
            this.maxHp = Math.floor(this.data.hp * (1 + level * 0.25));
            this.hp = this.maxHp;
            this.damage = Math.floor(this.data.damage * (1 + level * 0.15));
            this.speed = this.data.speed;
            this.xp = Math.floor(this.data.xp * (1 + level * 0.4));

            // Position
            this.position = new THREE.Vector3(position.x, position.y || 0, position.z);
            this.rotation = Math.random() * Math.PI * 2;

            // AI State
            this.state = 'idle'; // idle, patrol, chase, attack, hurt, dead
            this.target = null;
            this.attackCooldown = 0;

            // 3D Model
            this.group = null;
            this.model = null;
            this.mixer = null;
            this.healthBar = null;
            this.isLoaded = false;
            this.isDead = false;

            // Hitbox for collision
            this.hitbox = null;
        }

        async load() {
            const modelKey = this.data.model || 'default';
            const modelPath = KAYKIT_MODELS[modelKey] || KAYKIT_MODELS.default;

            try {
                const loader = new THREE.GLTFLoader();
                const gltf = await new Promise((resolve, reject) => {
                    loader.load(
                        `static/assets/${modelPath}`,
                        resolve,
                        undefined,
                        reject
                    );
                });

                this.group = new THREE.Group();
                this.model = gltf.scene.clone();
                this.model.scale.setScalar(1.5);

                // Color tint if specified
                if (this.data.color) {
                    this.model.traverse(child => {
                        if (child.isMesh && child.material) {
                            child.material = child.material.clone();
                            child.material.emissive = new THREE.Color(this.data.color);
                            child.material.emissiveIntensity = 0.3;
                        }
                    });
                }

                this.group.add(this.model);
                this.group.position.copy(this.position);
                this.group.rotation.y = this.rotation;

                // Health bar
                this.createHealthBar();

                // Hitbox (invisible sphere for collision)
                const hitboxGeom = new THREE.SphereGeometry(1.5, 8, 8);
                const hitboxMat = new THREE.MeshBasicMaterial({
                    visible: false,
                    transparent: true,
                    opacity: 0
                });
                this.hitbox = new THREE.Mesh(hitboxGeom, hitboxMat);
                this.hitbox.userData.enemy = this;
                this.group.add(this.hitbox);

                // Animations
                if (gltf.animations && gltf.animations.length > 0) {
                    this.mixer = new THREE.AnimationMixer(this.model);
                    this.animations = {};
                    gltf.animations.forEach(clip => {
                        this.animations[clip.name] = this.mixer.clipAction(clip);
                    });
                }

                this.scene.add(this.group);
                this.isLoaded = true;

                console.log(`✅ 3D Enemy loaded: ${this.data.name} (Lv${this.level})`);
                return true;
            } catch (error) {
                console.error(`❌ Failed to load enemy ${this.type}:`, error);
                // Fallback: Create colored cube
                this.createFallbackModel();
                return false;
            }
        }

        createFallbackModel() {
            this.group = new THREE.Group();

            const geometry = new THREE.BoxGeometry(1, 2, 1);
            const material = new THREE.MeshLambertMaterial({
                color: this.data.color || 0xff0000
            });
            this.model = new THREE.Mesh(geometry, material);
            this.model.position.y = 1;

            this.group.add(this.model);
            this.group.position.copy(this.position);

            this.createHealthBar();

            // Hitbox
            const hitboxGeom = new THREE.SphereGeometry(1.5, 8, 8);
            const hitboxMat = new THREE.MeshBasicMaterial({ visible: false });
            this.hitbox = new THREE.Mesh(hitboxGeom, hitboxMat);
            this.hitbox.userData.enemy = this;
            this.group.add(this.hitbox);

            this.scene.add(this.group);
            this.isLoaded = true;
        }

        createHealthBar() {
            const barWidth = 2;
            const barGeometry = new THREE.PlaneGeometry(barWidth, 0.2);
            const barMaterial = new THREE.MeshBasicMaterial({
                color: 0x00ff00,
                side: THREE.DoubleSide
            });

            this.healthBar = new THREE.Mesh(barGeometry, barMaterial);
            this.healthBar.position.y = 3;
            this.group.add(this.healthBar);
        }

        updateHealthBar() {
            if (!this.healthBar) return;

            const percent = this.hp / this.maxHp;
            this.healthBar.scale.x = Math.max(0, percent);

            if (percent > 0.5) {
                this.healthBar.material.color.setHex(0x00ff00);
            } else if (percent > 0.25) {
                this.healthBar.material.color.setHex(0xffff00);
            } else {
                this.healthBar.material.color.setHex(0xff0000);
            }
        }

        update(delta, playerPosition) {
            if (this.isDead || !this.isLoaded) return;

            this.attackCooldown = Math.max(0, this.attackCooldown - delta);

            if (this.mixer) {
                this.mixer.update(delta);
            }

            // AI
            if (playerPosition) {
                const distance = this.position.distanceTo(playerPosition);

                if (distance < this.data.attackRange) {
                    // Attack!
                    if (this.attackCooldown <= 0) {
                        this.attack(playerPosition);
                        this.attackCooldown = 1 + Math.random() * 0.5;
                    }
                    this.state = 'attack';
                } else if (distance < 15) {
                    // Chase
                    this.state = 'chase';
                    const direction = playerPosition.clone().sub(this.position).normalize();
                    this.position.add(direction.multiplyScalar(this.speed * delta));
                    this.rotation = Math.atan2(direction.x, direction.z);
                } else {
                    this.state = 'idle';
                }
            }

            this.group.position.copy(this.position);
            this.group.rotation.y = this.rotation;

            // Billboard healthbar
            if (this.healthBar && window.Scene3D?.camera) {
                this.healthBar.lookAt(Scene3D.camera.position);
            }
        }

        attack(playerPosition) {
            console.log(`⚔️ ${this.data.name} greift an! -${this.damage} HP`);

            // Damage player
            takeDamage(this.damage, this.data.name);

            // Notify UnifiedCombat if it exists
            if (typeof UnifiedCombat !== 'undefined' && UnifiedCombat.notify) {
                UnifiedCombat.notify(`${this.data.name} greift an! -${this.damage} HP`);
            }
        }

        takeDamage(amount) {
            if (this.isDead) return;

            this.hp -= amount;
            this.updateHealthBar();

            // Visual feedback - flash red
            if (this.model) {
                this.model.traverse(child => {
                    if (child.isMesh && child.material) {
                        const origColor = child.material.emissive?.clone() || new THREE.Color(0);
                        child.material.emissive = new THREE.Color(0xff0000);
                        setTimeout(() => {
                            if (child.material) child.material.emissive = origColor;
                        }, 100);
                    }
                });
            }

            console.log(`💥 ${this.data.name}: -${amount} HP (${this.hp}/${this.maxHp})`);

            if (this.hp <= 0) {
                this.die();
            }
        }

        die() {
            this.isDead = true;
            this.state = 'dead';

            console.log(`💀 ${this.data.name} besiegt! +${this.xp} XP`);

            // Drop loot
            if (this.data.loot) {
                console.log(`💎 Loot: ${this.data.loot.join(', ')}`);
            }

            // Notify systems
            if (typeof UnifiedCombat !== 'undefined' && UnifiedCombat.notify) {
                UnifiedCombat.notify(`💀 ${this.data.name} besiegt! +${this.xp} XP`);
            }

            // Add XP
            addXP(this.xp);

            // Fade out
            if (this.group) {
                const fadeOut = () => {
                    if (!this.group) return;
                    this.group.scale.multiplyScalar(0.9);
                    this.group.position.y -= 0.1;
                    if (this.group.scale.x > 0.1) {
                        requestAnimationFrame(fadeOut);
                    } else {
                        this.dispose();
                    }
                };
                setTimeout(fadeOut, 500);
            }

            // Remove from enemies list
            const index = currentEnemies.indexOf(this);
            if (index > -1) currentEnemies.splice(index, 1);

            // Check victory
            checkVictory();
        }

        dispose() {
            if (this.group && this.scene) {
                this.scene.remove(this.group);
            }
            this.group = null;
            this.model = null;
        }
    }

    // ==========================================
    // PLAYER FUNCTIONS
    // ==========================================

    function takeDamage(amount, source = 'Unknown') {
        playerStats.hp = Math.max(0, playerStats.hp - amount);

        updateCombatHUD();

        // Screen flash
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed; inset: 0;
            background: rgba(255, 0, 0, 0.3);
            pointer-events: none;
            z-index: 9999;
            animation: fadeOut 0.3s forwards;
        `;
        document.body.appendChild(flash);
        setTimeout(() => flash.remove(), 300);

        if (playerStats.hp <= 0) {
            gameOver();
        }
    }

    function heal(amount) {
        playerStats.hp = Math.min(playerStats.maxHp, playerStats.hp + amount);
        updateCombatHUD();
    }

    function addXP(amount) {
        // TODO: Connect to skill system
        console.log(`+${amount} XP`);
    }

    // ==========================================
    // COMBAT FUNCTIONS
    // ==========================================

    function startCombat(enemyList, scene, position) {
        combatActive = true;
        currentEnemies = [];

        enemyList.forEach((enemyType, i) => {
            const offset = {
                x: position.x + (Math.random() - 0.5) * 10,
                y: 0,
                z: position.z + (Math.random() - 0.5) * 10
            };

            const level = 1 + Math.floor(Math.random() * 3);
            const enemy = new Enemy3D(enemyType, offset, level, scene);
            enemy.load();
            currentEnemies.push(enemy);
        });

        createCombatHUD();
        startCombatLoop();

        console.log(`⚔️ Combat started: ${enemyList.length} enemies!`);
    }

    function attackNearestEnemy(damage, range = 5) {
        if (!combatActive) return null;

        const playerPos = getPlayerPosition();
        if (!playerPos) return null;

        let nearest = null;
        let nearestDist = Infinity;

        currentEnemies.forEach(enemy => {
            if (enemy.isDead) return;
            const dist = enemy.position.distanceTo(playerPos);
            if (dist < range && dist < nearestDist) {
                nearest = enemy;
                nearestDist = dist;
            }
        });

        if (nearest) {
            // Combo bonus
            const now = Date.now();
            if (now - lastAttackTime < COMBO_WINDOW) {
                comboCount++;
            } else {
                comboCount = 1;
            }
            lastAttackTime = now;

            const comboDamage = Math.floor(damage * (1 + comboCount * 0.1));
            nearest.takeDamage(comboDamage);

            if (comboCount > 1) {
                console.log(`🔥 ${comboCount}-Hit Combo! ${comboDamage} Schaden!`);
            }

            return nearest;
        }

        return null;
    }

    function getPlayerPosition() {
        if (window.Scene3D?.characterGroup) {
            return Scene3D.characterGroup.position.clone();
        }
        return null;
    }

    function checkVictory() {
        const living = currentEnemies.filter(e => !e.isDead);
        if (living.length === 0 && combatActive) {
            victory();
        }
    }

    function victory() {
        combatActive = false;
        stopCombatLoop();

        console.log('🎉 SIEG!');

        if (typeof notify === 'function') {
            notify('🎉 Alle Gegner besiegt!', 'success');
        }

        removeCombatHUD();
    }

    function gameOver() {
        combatActive = false;
        stopCombatLoop();

        console.log('💀 GAME OVER');

        if (typeof notify === 'function') {
            notify('💀 Du wurdest besiegt!', 'error');
        }

        // Respawn with half HP
        setTimeout(() => {
            playerStats.hp = Math.floor(playerStats.maxHp / 2);
            removeCombatHUD();
        }, 2000);
    }

    // ==========================================
    // COMBAT LOOP
    // ==========================================

    function startCombatLoop() {
        const loop = () => {
            if (!combatActive) return;

            const delta = clock.getDelta();
            const playerPos = getPlayerPosition();

            currentEnemies.forEach(enemy => {
                enemy.update(delta, playerPos);
            });

            updateCombatHUD();

            animationFrame = requestAnimationFrame(loop);
        };

        loop();
    }

    function stopCombatLoop() {
        if (animationFrame) {
            cancelAnimationFrame(animationFrame);
            animationFrame = null;
        }
    }

    // ==========================================
    // COMBAT HUD
    // ==========================================

    function createCombatHUD() {
        let hud = document.getElementById('real-combat-hud');
        if (hud) return;

        hud = document.createElement('div');
        hud.id = 'real-combat-hud';
        hud.style.cssText = `
            position: fixed;
            bottom: 70px;
            left: 0; right: 0;
            background: rgba(0,0,0,0.9);
            padding: 10px 20px;
            color: white;
            font-family: monospace;
            z-index: 900;
            border-top: 2px solid #ff4444;
        `;
        document.body.appendChild(hud);

        updateCombatHUD();
    }

    function updateCombatHUD() {
        const hud = document.getElementById('real-combat-hud');
        if (!hud) return;

        const hpPercent = Math.floor((playerStats.hp / playerStats.maxHp) * 100);
        let hpColor = '#00ff00';
        if (hpPercent < 60) hpColor = '#ffff00';
        if (hpPercent < 30) hpColor = '#ff0000';

        const enemyCount = currentEnemies.filter(e => !e.isDead).length;

        hud.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; gap: 20px;">
                    <span style="font-weight: bold;">⚔️ REAL COMBAT</span>
                    <span style="color: ${hpColor};">HP: ${playerStats.hp}/${playerStats.maxHp}</span>
                    <span style="color: #ff8888;">Gegner: ${enemyCount}</span>
                    ${comboCount > 1 ? `<span style="color: #ffaa00;">🔥 ${comboCount}x Combo!</span>` : ''}
                </div>
                <div style="display: flex; gap: 10px;">
                    <span style="color: #aaa;">Q/E = Angriff | Space = Dodge | M = Modus</span>
                    <button id="exit-real-combat" style="background: #ff4444; color: white; border: none; padding: 5px 10px; cursor: pointer;">Beenden</button>
                </div>
            </div>
        `;

        document.getElementById('exit-real-combat')?.addEventListener('click', () => {
            if (confirm('Kampf beenden?')) {
                endCombat();
            }
        });
    }

    function removeCombatHUD() {
        const hud = document.getElementById('real-combat-hud');
        if (hud) hud.remove();
    }

    function endCombat() {
        combatActive = false;
        stopCombatLoop();

        currentEnemies.forEach(e => e.dispose());
        currentEnemies = [];

        removeCombatHUD();
        console.log('🚪 Combat beendet');
    }

    // ==========================================
    // KEYBOARD CONTROLS
    // ==========================================

    function setupControls() {
        document.addEventListener('keydown', (e) => {
            // Skip if typing
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            if (!combatActive) return;

            const key = e.key.toLowerCase();

            switch(key) {
                case 'q':
                    // Left hand attack
                    attackNearestEnemy(15, 4);
                    break;
                case 'e':
                    // Right hand attack
                    attackNearestEnemy(12, 4);
                    break;
                case ' ':
                    e.preventDefault();
                    // Dodge (TODO: implement i-frames)
                    console.log('Dodge!');
                    break;
                case 'm':
                    // Toggle mode
                    const modes = ['MANUAL', 'AUTO', 'CHEER'];
                    const idx = modes.indexOf(combatMode);
                    combatMode = modes[(idx + 1) % modes.length];
                    console.log(`Combat Mode: ${combatMode}`);
                    break;
            }
        });
    }

    // ==========================================
    // BIOME ENEMY SPAWNER (Fixes null biome!)
    // ==========================================

    function getEnemiesForBiome(biome) {
        const normalizedBiome = (biome || 'default').toLowerCase();
        const enemies = BIOME_ENEMIES[normalizedBiome] || BIOME_ENEMIES.default;
        return enemies;
    }

    function spawnBiomeEnemies(biome, position, scene, count = 3) {
        const enemyTypes = getEnemiesForBiome(biome);
        if (enemyTypes.length === 0) {
            console.log(`⚔️ Safe Zone: ${biome} - keine Gegner`);
            return;
        }

        const toSpawn = [];
        for (let i = 0; i < count; i++) {
            const type = enemyTypes[Math.floor(Math.random() * enemyTypes.length)];
            toSpawn.push(type);
        }

        startCombat(toSpawn, scene, position);
    }

    // ==========================================
    // INIT
    // ==========================================

    setupControls();

    // CSS for fadeOut animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    // ==========================================
    // PUBLIC API
    // ==========================================

    window.Real3DCombat = {
        startCombat,
        endCombat,
        attackNearestEnemy,
        takeDamage,
        heal,

        // Biome system
        getEnemiesForBiome,
        spawnBiomeEnemies,

        // State
        isActive: () => combatActive,
        getMode: () => combatMode,
        setMode: (mode) => { combatMode = mode; },
        getPlayerStats: () => ({ ...playerStats }),
        getEnemies: () => currentEnemies,

        // Enemy types for reference
        ENEMY_TYPES,
        BIOME_ENEMIES
    };

    console.log('✅ Real 3D Combat System loaded!');
    console.log('   🎮 Controls: Q/E = Attack, Space = Dodge, M = Mode');
    console.log('   ⚔️ Echte KayKit 3D Gegner!');

})();
