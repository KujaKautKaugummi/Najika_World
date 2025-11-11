/**
 * NAJIKA WORLD - REALTIME COMBAT SYSTEM
 * ======================================
 *
 * Basierend auf NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md
 *
 * COMBAT MODES:
 * - MANUAL: Volle Kontrolle (Skyrim + Soulframe + Dark Souls Movement)
 * - ASSIST: Najika kämpft, Spieler feuert an (Digimon World Style)
 * - AUTO: Najika kämpft alleine, Spieler kann anfeuern
 *
 * CONTROLS (MANUAL):
 * - Q = Linke Hand Leicht
 * - Shift+Q = Linke Hand Schwer
 * - E = Rechte Hand Leicht
 * - Shift+E = Rechte Hand Schwer
 * - SPACE = Beide Hände Leicht
 * - Shift+SPACE = Beide Hände Schwer
 * - Q+E = Dual-Strike / Element-Weave
 * - C = Dodge/Roll
 * - X = Block (halten)
 * - V = Parry (Timing!)
 *
 * CONTROLS (ASSIST/AUTO):
 * - 1 = "Los!" (+10% DMG, 3s)
 * - 2 = "Defend!" (+20% DEF, 3s)
 * - 3 = "Combo!" (Special)
 * - 4 = "Finisher!" (Ultimate bei Cheer=100)
 */

class RealtimeCombat {
    constructor(scene, THREE, foodSystem = null) {
        this.scene = scene;
        this.THREE = THREE;
        this.foodSystem = foodSystem; // Food System Integration

        // Combat State
        this.combatActive = false;
        this.combatMode = 'MANUAL'; // MANUAL, ASSIST, AUTO

        // Backend Integration
        this.backendURL = 'http://localhost:8000';
        this.battleID = null;

        // Player Stats
        this.playerHealth = 100;
        this.playerMaxHealth = 100;
        this.playerMana = 100;
        this.playerMaxMana = 100;
        this.playerStamina = 100;
        this.playerMaxStamina = 100;

        // Cheer System (ASSIST/AUTO Mode)
        this.cheerMeter = 0; // 0-100
        this.najikaState = 'idle'; // idle, attacking, dodging, preparing
        this.lastNajikaActionTime = 0;

        // Dual-Wielding State
        this.leftHandWeapon = null; // { type: 'sword', element: 'fire', damage: 15 }
        this.rightHandWeapon = null;
        this.leftHandCooldown = 0;
        this.rightHandCooldown = 0;
        this.bothHandsCooldown = 0;

        // Defense State
        this.isBlocking = false;
        this.isDodging = false;
        this.parryWindow = false;
        this.lastDodgeTime = 0;

        // Enemies
        this.enemies = [];
        this.currentTarget = null;

        // Input State
        this.keys = {
            q: false,
            e: false,
            shift: false,
            space: false,
            c: false,
            x: false,
            v: false,
            '1': false,
            '2': false,
            '3': false,
            '4': false
        };

        // Combo Tracking
        this.comboCount = 0;
        this.lastAttackTime = 0;
        this.comboWindow = 1000; // 1 second

        // Visual Feedback
        this.damageNumbers = [];

        // Bind keyboard events
        this.bindControls();
    }

    // ===== BACKEND INTEGRATION =====

    async startBattleWithBackend(enemyTypes) {
        try {
            const response = await fetch(`${this.backendURL}/api/battle/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    enemy_types: enemyTypes,
                    combat_mode: this.combatMode === 'MANUAL' ? 'action' : 'cheer'
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.battleID = data.battle_id;
            this.combatActive = true;

            console.log('✅ Backend Battle gestartet:', data);
            return data;
        } catch (error) {
            console.warn('⚠️ Backend nicht erreichbar, nutze Offline-Mode:', error);
            // Fallback: Local Combat ohne Backend
            this.combatActive = true;
            this.battleID = `local_${Date.now()}`;
            return { success: true, offline: true };
        }
    }

    async sendAttackToBackend(attackType, targetID, comboData = null) {
        if (!this.battleID) return null;

        try {
            const response = await fetch(`${this.backendURL}/api/battle/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'attack',
                    attack_type: attackType,
                    target_id: targetID,
                    combo_data: comboData
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            return data;
        } catch (error) {
            console.warn('⚠️ Backend Attack fehlgeschlagen:', error);
            return null;
        }
    }

    async updateCheerMeter(change) {
        if (!this.battleID) return;

        try {
            const response = await fetch(`${this.backendURL}/api/battle/cheer`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ change })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.cheerMeter = data.cheer_meter;
        } catch (error) {
            console.warn('⚠️ Cheer Update fehlgeschlagen:', error);
        }
    }

    // ===== CONTROLS =====

    bindControls() {
        window.addEventListener('keydown', (e) => {
            const key = e.key.toLowerCase();
            if (key in this.keys) this.keys[key] = true;

            // Combat-spezifische Actions (nur wenn Combat aktiv)
            if (!this.combatActive) return;

            if (this.combatMode === 'MANUAL') {
                this.handleManualControls(e);
            } else {
                this.handleAssistControls(e);
            }
        });

        window.addEventListener('keyup', (e) => {
            const key = e.key.toLowerCase();
            if (key in this.keys) this.keys[key] = false;

            // Block loslassen
            if (key === 'x') {
                this.isBlocking = false;
            }
        });
    }

    handleManualControls(e) {
        const key = e.key.toLowerCase();

        // ELEMENT-WEAVE: Q+E gleichzeitig (beide keys müssen gedrückt sein)
        if ((key === 'q' || key === 'e') && this.keys.q && this.keys.e) {
            this.elementWeave();
            return; // Verhindere normale Angriffe
        }

        // LEFT HAND ATTACKS (Q)
        if (key === 'q' && !e.shiftKey) {
            this.leftHandLightAttack();
        } else if (key === 'q' && e.shiftKey) {
            this.leftHandHeavyAttack();
        }

        // RIGHT HAND ATTACKS (E)
        if (key === 'e' && !e.shiftKey) {
            this.rightHandLightAttack();
        } else if (key === 'e' && e.shiftKey) {
            this.rightHandHeavyAttack();
        }

        // BOTH HANDS ATTACKS (SPACE)
        if (key === ' ' && !e.shiftKey) {
            this.bothHandsLightAttack();
        } else if (key === ' ' && e.shiftKey) {
            this.bothHandsHeavyAttack();
        }

        // DODGE/ROLL (C)
        if (key === 'c') {
            this.dodge();
        }

        // BLOCK (X) - handled in keydown/keyup
        if (key === 'x') {
            this.isBlocking = true;
        }

        // PARRY (V)
        if (key === 'v') {
            this.parry();
        }
    }

    // ===== ELEMENT-WEAVES =====

    elementWeave() {
        // Cooldown check
        if (this.bothHandsCooldown > 0) return;
        if (this.playerMana < 30) return; // Mana Cost

        const leftElement = this.leftHandWeapon ? this.leftHandWeapon.element : null;
        const rightElement = this.rightHandWeapon ? this.rightHandWeapon.element : null;

        // Beide Waffen müssen Elemente haben
        if (!leftElement || !rightElement) {
            console.log('⚠️ Beide Waffen brauchen Elemente für Weaves!');
            return;
        }

        // Element-Combo bestimmen
        const comboKey = [leftElement, rightElement].sort().join('+');
        const weaves = {
            'fire+ice': { name: 'Thermoschock', damage: 80, color: 0xff00ff },
            'fire+water': { name: 'Dampfexplosion', damage: 70, color: 0xff8888 },
            'fire+earth': { name: 'Lava-Schuss', damage: 75, color: 0xff4400 },
            'fire+wind': { name: 'Flammensturm', damage: 85, color: 0xff6600 },
            'ice+water': { name: 'Eissturm', damage: 75, color: 0x00ffff },
            'lightning+water': { name: 'Elektroschock', damage: 90, color: 0xffff00 },
            'light+darkness': { name: 'Schatten-Licht', damage: 100, color: 0x888888 }
        };

        const weave = weaves[comboKey];

        if (!weave) {
            console.log(`⚠️ Keine Weave-Combo für ${leftElement} + ${rightElement}`);
            return;
        }

        // Execute Weave
        const damage = this.calculateDamage('both', 'heavy') * 1.5; // +50% Bonus
        this.executeAttack(damage, 'element_weave');

        // Visual Feedback
        console.log(`💫 ELEMENT-WEAVE: ${weave.name}! ${damage} Schaden!`);

        // Costs & Cooldowns
        this.playerMana -= 30;
        this.bothHandsCooldown = 3000; // 3s cooldown

        // Combo update
        this.updateCombo();
    }

    handleAssistControls(e) {
        const key = e.key;

        // Digimon World Anfeuern (Timing-basiert!)
        const timing = this.calculateCheerTiming();

        if (key === '1') {
            this.cheer('Los!', timing);
        } else if (key === '2') {
            this.cheer('Defend!', timing);
        } else if (key === '3') {
            this.cheer('Combo!', timing);
        } else if (key === '4') {
            this.cheer('Finisher!', timing);
        }
    }

    // ===== MANUAL MODE ATTACKS =====

    leftHandLightAttack() {
        if (this.leftHandCooldown > 0) return;

        const damage = this.calculateDamage('left', 'light');
        this.executeAttack(damage, 'left_light');

        this.leftHandCooldown = 500; // 0.5s cooldown
        this.updateCombo();

        console.log('⚔️ Linke Hand Leicht:', damage);
    }

    leftHandHeavyAttack() {
        if (this.leftHandCooldown > 0) return;
        if (this.playerStamina < 20) return; // Stamina Cost

        const damage = this.calculateDamage('left', 'heavy');
        this.executeAttack(damage, 'left_heavy');

        this.leftHandCooldown = 1200; // 1.2s cooldown
        this.playerStamina -= 20;
        this.updateCombo();

        console.log('💥 Linke Hand Schwer:', damage);
    }

    rightHandLightAttack() {
        if (this.rightHandCooldown > 0) return;

        const damage = this.calculateDamage('right', 'light');
        this.executeAttack(damage, 'right_light');

        this.rightHandCooldown = 500;
        this.updateCombo();

        console.log('⚔️ Rechte Hand Leicht:', damage);
    }

    rightHandHeavyAttack() {
        if (this.rightHandCooldown > 0) return;
        if (this.playerStamina < 20) return;

        const damage = this.calculateDamage('right', 'heavy');
        this.executeAttack(damage, 'right_heavy');

        this.rightHandCooldown = 1200;
        this.playerStamina -= 20;
        this.updateCombo();

        console.log('💥 Rechte Hand Schwer:', damage);
    }

    bothHandsLightAttack() {
        if (this.bothHandsCooldown > 0) return;

        const damage = this.calculateDamage('both', 'light');
        this.executeAttack(damage, 'both_light');

        this.bothHandsCooldown = 800;
        this.updateCombo();

        console.log('⚔️⚔️ Beide Hände Leicht:', damage);
    }

    bothHandsHeavyAttack() {
        if (this.bothHandsCooldown > 0) return;
        if (this.playerStamina < 40) return;

        const damage = this.calculateDamage('both', 'heavy');
        this.executeAttack(damage, 'both_heavy');

        this.bothHandsCooldown = 2000;
        this.playerStamina -= 40;
        this.updateCombo();

        console.log('💥💥 Beide Hände Schwer:', damage);
    }

    // ===== DAMAGE CALCULATION =====

    calculateDamage(hand, type) {
        let baseDamage = 0;

        // Base Damage
        if (hand === 'left' && this.leftHandWeapon) {
            baseDamage = type === 'light' ? this.leftHandWeapon.damage : this.leftHandWeapon.damage * 2.5;
        } else if (hand === 'right' && this.rightHandWeapon) {
            baseDamage = type === 'light' ? this.rightHandWeapon.damage : this.rightHandWeapon.damage * 2.5;
        } else if (hand === 'both') {
            const leftDmg = this.leftHandWeapon ? this.leftHandWeapon.damage : 10;
            const rightDmg = this.rightHandWeapon ? this.rightHandWeapon.damage : 10;
            baseDamage = type === 'light' ? (leftDmg + rightDmg) * 1.5 : (leftDmg + rightDmg) * 3;
        } else {
            baseDamage = type === 'light' ? 10 : 25; // Faustkampf
        }

        // Combo Bonus
        const comboBonus = 1 + (this.comboCount * 0.1); // +10% pro Combo
        baseDamage *= comboBonus;

        // Cheer Bonus (ASSIST/AUTO Mode)
        if (this.combatMode !== 'MANUAL') {
            const cheerBonus = 1 + (this.cheerMeter / 100 * 0.25); // Max +25% bei Cheer=100
            baseDamage *= cheerBonus;
        }

        // FOOD BUFFS (Phase 4!)
        if (this.foodSystem) {
            const buffSummary = this.foodSystem.getBuffSummary();
            if (buffSummary.damage > 0) {
                baseDamage *= (1 + buffSummary.damage / 100);
            }
        }

        // Random Variance
        baseDamage *= (0.9 + Math.random() * 0.2); // 90-110%

        // Crit Chance (Food Buffs)
        if (this.foodSystem) {
            const buffed = this.foodSystem.calculateBuffedStats({ critChance: 0 });
            if (buffed.critChance > 0 && Math.random() * 100 < buffed.critChance) {
                baseDamage *= 2; // CRITICAL HIT!
                console.log('💥 CRITICAL HIT! x2 Damage!');
            }
        }

        return Math.floor(baseDamage);
    }

    executeAttack(damage, attackType) {
        if (!this.currentTarget) return;

        // Apply damage to enemy
        this.currentTarget.health -= damage;

        // Visual Feedback
        this.showDamageNumber(damage, this.currentTarget.position);

        // Send to Backend
        if (this.battleID) {
            this.sendAttackToBackend(attackType, this.currentTarget.id, {
                active: true,
                damage: damage,
                combo_count: this.comboCount
            });
        }

        // Check if enemy died
        if (this.currentTarget.health <= 0) {
            this.killEnemy(this.currentTarget);
        } else {
            // Enemy counter-attack
            this.enemyCounterAttack(this.currentTarget);
        }
    }

    // ===== DEFENSE =====

    dodge() {
        const now = Date.now();
        if (now - this.lastDodgeTime < 1000) return; // 1s cooldown
        if (this.playerStamina < 15) return;

        this.isDodging = true;
        this.playerStamina -= 15;
        this.lastDodgeTime = now;

        console.log('🌀 Dodge/Roll!');

        // Dodge lasts 300ms (i-frames)
        setTimeout(() => {
            this.isDodging = false;
        }, 300);
    }

    parry() {
        if (this.playerStamina < 10) return;

        this.parryWindow = true;
        this.playerStamina -= 10;

        console.log('🛡️ Parry!');

        // Parry window: 200ms
        setTimeout(() => {
            this.parryWindow = false;
        }, 200);
    }

    // ===== ASSIST/AUTO MODE - DIGIMON WORLD CHEERING =====

    calculateCheerTiming() {
        const now = Date.now();
        const timeSinceAction = now - this.lastNajikaActionTime;

        // Perfect: 0-200ms
        if (timeSinceAction <= 200) return 'perfect';

        // Good: 200-500ms
        if (timeSinceAction <= 500) return 'good';

        // Bad: >500ms
        return 'bad';
    }

    cheer(command, timing) {
        console.log(`📣 Cheer: ${command} (${timing})`);

        let cheerChange = 0;
        let statBonus = 0;

        // Timing Evaluation
        if (timing === 'perfect') {
            cheerChange = 20;
            statBonus = 0.20; // +20%
            console.log('✨ PERFECT TIMING! +20% Stats!');
        } else if (timing === 'good') {
            cheerChange = 10;
            statBonus = 0.10; // +10%
            console.log('👍 Good Timing! +10% Stats!');
        } else {
            cheerChange = -5;
            statBonus = 0;
            console.log('😤 Bad Timing! Najika ist genervt!');
        }

        // Update Cheer Meter
        this.cheerMeter = Math.max(0, Math.min(100, this.cheerMeter + cheerChange));
        this.updateCheerMeter(cheerChange);

        // Apply Buffs (3 Sekunden)
        if (statBonus > 0) {
            this.applyCheerBuff(command, statBonus);
        }

        // Special: Finisher bei Cheer=100
        if (command === 'Finisher!' && this.cheerMeter >= 100) {
            this.executeFinisher();
        }
    }

    applyCheerBuff(command, bonus) {
        // Buffs für 3 Sekunden
        const duration = 3000;

        if (command === 'Los!') {
            // +10-20% Damage
            console.log(`⚔️ Damage Buff: +${(bonus * 100)}% für 3s`);
            // TODO: Apply damage multiplier
        } else if (command === 'Defend!') {
            // +20-40% Defense
            console.log(`🛡️ Defense Buff: +${(bonus * 100)}% für 3s`);
            // TODO: Apply defense multiplier
        } else if (command === 'Combo!') {
            // Trigger Special Move
            console.log('💫 Special Move aktiviert!');
            // TODO: Execute special combo
        }

        // Remove buff after duration
        setTimeout(() => {
            console.log('⏱️ Buff abgelaufen');
        }, duration);
    }

    executeFinisher() {
        console.log('💥💥💥 ULTIMATE FINISHER! 💥💥💥');

        // Reset Cheer Meter
        this.cheerMeter = 0;

        // Massive AOE Damage
        const damage = 300;
        this.enemies.forEach(enemy => {
            if (enemy.health > 0) {
                enemy.health = Math.max(0, enemy.health - damage);
                this.showDamageNumber(damage, enemy.position);

                if (enemy.health <= 0) {
                    this.killEnemy(enemy);
                }
            }
        });

        // Send to Backend
        if (this.battleID) {
            fetch(`${this.backendURL}/api/battle/special`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
        }
    }

    // ===== COMBO SYSTEM =====

    updateCombo() {
        const now = Date.now();

        if (now - this.lastAttackTime < this.comboWindow) {
            this.comboCount++;
        } else {
            this.comboCount = 1;
        }

        this.lastAttackTime = now;
        console.log(`🔥 Combo x${this.comboCount}`);
    }

    // ===== ENEMY AI =====

    enemyCounterAttack(enemy) {
        // Ignore if blocking/dodging/parrying
        if (this.isBlocking) {
            console.log('🛡️ Blocked!');
            return;
        }

        if (this.isDodging) {
            console.log('🌀 Dodged!');
            return;
        }

        if (this.parryWindow) {
            console.log('⚔️ PARRIED! Riposte!');
            // Riposte: Double damage back
            enemy.health -= enemy.damage * 2;
            return;
        }

        // Take damage
        const damage = Math.floor(enemy.damage * (0.8 + Math.random() * 0.4));
        this.playerHealth -= damage;

        console.log(`💔 Took ${damage} damage!`);

        // Check death
        if (this.playerHealth <= 0) {
            this.gameOver();
        }
    }

    killEnemy(enemy) {
        enemy.alive = false;
        enemy.mesh.visible = false;

        console.log(`☠️ ${enemy.name} besiegt!`);

        // Check if all enemies dead
        if (this.enemies.every(e => !e.alive)) {
            this.victory();
        }
    }

    // ===== VISUAL FEEDBACK =====

    showDamageNumber(damage, position) {
        // Create floating damage number (Sprite-based)
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 128;

        // Draw damage text
        context.font = 'Bold 60px Arial';
        context.fillStyle = damage > 50 ? '#ff0000' : '#ffaa00';
        context.textAlign = 'center';
        context.fillText(`-${damage}`, 128, 80);

        // Create sprite
        const texture = new this.THREE.CanvasTexture(canvas);
        const material = new this.THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new this.THREE.Sprite(material);

        sprite.position.copy(position);
        sprite.position.y += 2;
        sprite.scale.set(4, 2, 1);

        this.scene.add(sprite);

        // Animate upwards and fade out
        const startY = sprite.position.y;
        const startTime = Date.now();
        const duration = 1500; // 1.5 seconds

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = elapsed / duration;

            if (progress < 1) {
                sprite.position.y = startY + progress * 3; // Float up 3 units
                sprite.material.opacity = 1 - progress; // Fade out
                requestAnimationFrame(animate);
            } else {
                this.scene.remove(sprite);
                sprite.material.dispose();
                texture.dispose();
            }
        };

        animate();
    }

    // ===== ENEMY SPAWNING =====

    spawnEnemiesInAllRegions(regions) {
        console.log('🐉 Spawne Enemies in allen 9 Regionen...');

        // Enemy Types pro Region (basierend auf Master-Doku)
        const regionEnemyTypes = {
            ice: ['ice_undead', 'ice_elemental'],
            highland: ['highland_guardian'],
            desert: ['desert_bandit', 'desert_sandworm'],
            swamp: ['swamp_witch', 'swamp_monster'],
            mountain: ['mountain_giant'],
            coast: ['coast_pirate', 'coast_seamonster'],
            caves: ['caves_goblin'],
            forest: ['forest_druid', 'forest_spirit'],
            volcano: ['volcano_elemental', 'volcano_lavamonster']
        };

        const enemyDatabase = {
            // ICE
            ice_undead: { name: 'Eis-Untoter', hp: 40, damage: 8, speed: 1.0, color: 0x00ffff },
            ice_elemental: { name: 'Eis-Elemental', hp: 50, damage: 10, speed: 0.8, color: 0xaaffff },

            // HIGHLAND
            highland_guardian: { name: 'Hochland-Wächter', hp: 60, damage: 12, speed: 0.9, color: 0x8b7355 },

            // DESERT
            desert_bandit: { name: 'Wüsten-Bandit', hp: 45, damage: 10, speed: 1.2, color: 0xe8d4a0 },
            desert_sandworm: { name: 'Sandwurm', hp: 80, damage: 15, speed: 0.5, color: 0xc4a000 },

            // SWAMP
            swamp_witch: { name: 'Sumpf-Hexe', hp: 55, damage: 14, speed: 0.7, color: 0x556b2f },
            swamp_monster: { name: 'Giftmonster', hp: 70, damage: 12, speed: 0.6, color: 0x3d5c1f },

            // MOUNTAIN
            mountain_giant: { name: 'Bergriese', hp: 100, damage: 20, speed: 0.4, color: 0x808080 },

            // COAST
            coast_pirate: { name: 'Pirat', hp: 50, damage: 11, speed: 1.1, color: 0xc2b280 },
            coast_seamonster: { name: 'Seemonster', hp: 90, damage: 18, speed: 0.8, color: 0x0066cc },

            // CAVES
            caves_goblin: { name: 'Höhlen-Goblin', hp: 35, damage: 7, speed: 1.3, color: 0x2f2f2f },

            // FOREST
            forest_druid: { name: 'Feindlicher Druide', hp: 65, damage: 13, speed: 0.8, color: 0x2d5016 },
            forest_spirit: { name: 'Waldgeist', hp: 45, damage: 9, speed: 1.0, color: 0x4CAF50 },

            // VOLCANO
            volcano_elemental: { name: 'Feuer-Elemental', hp: 85, damage: 22, speed: 0.7, color: 0xff4500 },
            volcano_lavamonster: { name: 'Lava-Kreatur', hp: 95, damage: 25, speed: 0.5, color: 0x8b0000 }
        };

        regions.forEach(region => {
            const enemyTypes = regionEnemyTypes[region.name];
            if (!enemyTypes) return;

            // Spawn 3-5 Enemies pro Region
            const enemyCount = 3 + Math.floor(Math.random() * 3);

            for (let i = 0; i < enemyCount; i++) {
                // Random Enemy Type für diese Region
                const randomType = enemyTypes[Math.floor(Math.random() * enemyTypes.length)];
                const enemyData = enemyDatabase[randomType];

                if (!enemyData) continue;

                // Random Position innerhalb der Region
                const offsetX = (Math.random() - 0.5) * 100;
                const offsetZ = (Math.random() - 0.5) * 100;

                this.spawnEnemy(
                    randomType,
                    region.x + offsetX,
                    region.y + 2,
                    region.z + offsetZ,
                    enemyData
                );
            }
        });

        console.log(`✅ ${this.enemies.length} Enemies gespawnt!`);
    }

    spawnEnemy(type, x, y, z, data) {
        // Create mesh container (ALWAYS add simple fallback immediately)
        const mesh = new this.THREE.Group();
        mesh.position.set(x, y, z);

        // Simple fallback geometry (ALWAYS present)
        const geometry = new this.THREE.BoxGeometry(2, 3, 2);
        const material = new this.THREE.MeshStandardMaterial({
            color: data.color,
            roughness: 0.7,
            metalness: 0.3
        });
        const fallback = new this.THREE.Mesh(geometry, material);
        fallback.castShadow = true;
        fallback.receiveShadow = true;
        mesh.add(fallback);

        // Try to load KayKit model (async, replace fallback if successful)
        // Map enemy types to actual existing models with full paths
        const characterModels = {
            // Ice Region - Skeleton Models
            'ice_undead': {
                path: 'static/assets/KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_warrior.gltf',
                scale: 2
            },
            'ice_elemental': {
                path: 'static/assets/KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_mage.gltf',
                scale: 2
            },

            // Desert Region - Knight & Barbarian
            'desert_bandit': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_rogue.gltf',
                scale: 2
            },
            'desert_sandworm': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_barbarian.gltf',
                scale: 2.5
            },

            // Swamp Region - Witch & Mage
            'swamp_witch': {
                path: 'static/assets/KayKit Spooktober Seasonal Pack 1.1/Models/Characters/Witch/gltf/character_witch.gltf',
                scale: 2
            },
            'swamp_monster': {
                path: 'static/assets/KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_minion.gltf',
                scale: 2.5
            },

            // Mountain Region - Big Barbarian
            'mountain_giant': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_barbarian.gltf',
                scale: 3
            },

            // Coast Region - Pirate & Knight
            'coast_pirate': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_rogue.gltf',
                scale: 2
            },
            'coast_seamonster': {
                path: 'static/assets/KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_warrior.gltf',
                scale: 2.5
            },

            // Caves Region - Minion
            'caves_goblin': {
                path: 'static/assets/KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_minion.gltf',
                scale: 1.5
            },

            // Forest Region - Mage & Archer
            'forest_druid': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_mage.gltf',
                scale: 2
            },
            'forest_spirit': {
                path: 'static/assets/KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_archer.gltf',
                scale: 2
            },

            // Volcano Region - Barbarian & Warrior
            'volcano_elemental': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_barbarian.gltf',
                scale: 2.5
            },
            'volcano_lavamonster': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf',
                scale: 2.5
            },

            // Highland Region - Knight
            'highland_guardian': {
                path: 'static/assets/KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf',
                scale: 2
            }
        };

        const modelConfig = characterModels[type];
        const modelPath = modelConfig ? modelConfig.path : null;
        const modelScale = modelConfig ? modelConfig.scale : 2;

        // Try async loading (don't block spawning!)
        if (modelPath && typeof THREE !== 'undefined' && THREE.GLTFLoader) {
            const loader = new THREE.GLTFLoader();
            loader.load(
                modelPath,
                (gltf) => {
                    // Remove fallback
                    mesh.remove(fallback);

                    // Add KayKit model
                    const model = gltf.scene;
                    model.scale.set(modelScale, modelScale, modelScale);

                    model.traverse((child) => {
                        if (child.isMesh) {
                            child.castShadow = true;
                            child.receiveShadow = true;

                            // Color tinting for enemy variation
                            if (data.color) {
                                const colorObj = new this.THREE.Color(data.color);
                                child.material = child.material.clone();
                                child.material.color.multiply(colorObj);
                            }
                        }
                    });

                    mesh.add(model);
                    console.log(`✅ Loaded KayKit model for ${type}: ${modelPath}`);
                },
                undefined,
                (error) => {
                    console.warn(`⚠️ KayKit model failed for ${type} (${modelPath}), keeping fallback:`, error);
                }
            );
        } else {
            console.log(`ℹ️ No model configured for ${type}, using fallback geometry`);
        }

        // Enemy Object
        const enemy = {
            id: `${type}_${Date.now()}_${Math.random()}`,
            type: type,
            name: data.name,
            health: data.hp,
            maxHealth: data.hp,
            damage: data.damage,
            speed: data.speed,
            position: mesh.position,
            mesh: mesh,
            alive: true,
            aggro: false
        };

        this.enemies.push(enemy);
        this.scene.add(mesh);
    }

    // ===== UPDATE LOOP =====

    setEnemyEmissive(enemy, color, intensity) {
        // Helper function: enemy.mesh is now a Group, need to traverse children
        if (!enemy || !enemy.mesh) return;

        enemy.mesh.traverse((child) => {
            if (child.isMesh && child.material) {
                if (!child.material.emissive) {
                    child.material.emissive = new this.THREE.Color(0x000000);
                }
                if (color) {
                    child.material.emissive.set(color);
                }
                child.material.emissiveIntensity = intensity;
            }
        });
    }

    update(delta, playerPosition) {
        // Update Cooldowns
        if (this.leftHandCooldown > 0) this.leftHandCooldown -= delta * 1000;
        if (this.rightHandCooldown > 0) this.rightHandCooldown -= delta * 1000;
        if (this.bothHandsCooldown > 0) this.bothHandsCooldown -= delta * 1000;

        // Stamina Regen (Base + Food Buffs)
        let staminaRegen = 10; // Base
        if (this.foodSystem) {
            const buffSummary = this.foodSystem.getBuffSummary();
            staminaRegen += buffSummary.stamina_regen;
        }

        if (this.playerStamina < this.playerMaxStamina) {
            this.playerStamina = Math.min(this.playerMaxStamina, this.playerStamina + delta * staminaRegen);
        }

        // Food System Update (HP/Mana/Stamina Regens)
        if (this.foodSystem) {
            const player = this.foodSystem.updateRegens(delta, {
                health: this.playerHealth,
                maxHealth: this.playerMaxHealth,
                mana: this.playerMana,
                maxMana: this.playerMaxMana,
                stamina: this.playerStamina,
                maxStamina: this.playerMaxStamina
            });

            // Apply updated values
            this.playerHealth = player.health;
            this.playerMana = player.mana;
            this.playerStamina = player.stamina;
        }

        // Najika AI (ASSIST/AUTO Mode only!)
        if ((this.combatMode === 'ASSIST' || this.combatMode === 'AUTO') && this.combatActive) {
            this.updateNajikaAI(delta);
        }

        // Update ALL enemies (AI, Movement)
        if (playerPosition) {
            this.updateEnemies(delta, playerPosition);
        }
    }

    updateNajikaAI(delta) {
        // Najika's AI: Auto-attack in ASSIST/AUTO mode
        if (!this.najikaNextActionTime) {
            this.najikaNextActionTime = Date.now() + 1500; // First action in 1.5s
        }

        const now = Date.now();
        if (now >= this.najikaNextActionTime && this.currentTarget && this.currentTarget.alive) {
            // Najika performs an action!
            this.lastNajikaActionTime = now;

            // Choose random action
            const actions = ['attack_left', 'attack_right', 'attack_both', 'dodge'];
            const randomAction = actions[Math.floor(Math.random() * actions.length)];

            this.najikaState = randomAction === 'dodge' ? 'dodging' : 'attacking';

            // Execute the action
            if (randomAction === 'attack_left') {
                this.leftHandLightAttack();
                console.log('🤖 Najika: Linker Hand Angriff!');
            } else if (randomAction === 'attack_right') {
                this.rightHandLightAttack();
                console.log('🤖 Najika: Rechter Hand Angriff!');
            } else if (randomAction === 'attack_both') {
                if (this.playerStamina >= 30) {
                    this.bothHandsAttack();
                    console.log('🤖 Najika: Beide Hände!');
                } else {
                    // Fallback to single hand
                    this.leftHandLightAttack();
                }
            } else if (randomAction === 'dodge') {
                console.log('🤖 Najika: Dodge!');
            }

            // Schedule next action (1.5-2.5s random)
            this.najikaNextActionTime = now + 1500 + Math.random() * 1000;

            // Back to idle after 0.5s
            setTimeout(() => {
                this.najikaState = 'idle';
            }, 500);
        }
    }

    updateEnemies(delta, playerPosition) {
        // Update ALL living enemies
        for (const enemy of this.enemies) {
            if (!enemy.alive) continue;

            // Calculate distance to player
            const distance = playerPosition.distanceTo(enemy.position);

            // Aggro: Follow player if close
            if (distance < 15) {
                enemy.aggro = true;

                // Move towards player
                const direction = new this.THREE.Vector3();
                direction.subVectors(playerPosition, enemy.position);
                direction.y = 0; // Only move horizontally
                direction.normalize();

                const moveSpeed = enemy.speed * delta;
                enemy.position.x += direction.x * moveSpeed;
                enemy.position.z += direction.z * moveSpeed;

                // Rotate towards player
                const angle = Math.atan2(direction.x, direction.z);
                enemy.mesh.rotation.y = angle;

                // Visual: Glow if aggro
                this.setEnemyEmissive(enemy, 0xff0000, 0.3);

                // Attack if very close (< 3 units) and in combat
                if (distance < 3 && this.combatActive && enemy === this.currentTarget) {
                    // Enemy attacks automatically every 2 seconds
                    if (!enemy.lastAttackTime || Date.now() - enemy.lastAttackTime > 2000) {
                        this.enemyCounterAttack(enemy);
                        enemy.lastAttackTime = Date.now();
                    }
                }
            } else {
                // De-aggro if far away
                enemy.aggro = false;
                this.setEnemyEmissive(enemy, null, 0);
            }
        }
    }

    // ===== PROXIMITY DETECTION =====

    checkEnemyProximity(playerPosition) {
        if (this.combatActive) return null;

        let closestEnemy = null;
        let closestDistance = Infinity;

        for (const enemy of this.enemies) {
            if (!enemy.alive) continue;

            const distance = playerPosition.distanceTo(enemy.position);

            if (distance < 5 && distance < closestDistance) {
                closestEnemy = enemy;
                closestDistance = distance;
            }
        }

        return closestEnemy;
    }

    // ===== COMBAT LIFECYCLE =====

    async startCombat(enemy) {
        this.currentTarget = enemy;
        this.combatActive = true;

        // Start battle with backend
        await this.startBattleWithBackend([enemy.type]);

        console.log(`⚔️ Combat gestartet gegen: ${enemy.name}!`);

        // Visual: Enemy glüht rot
        enemy.aggro = true;
        this.setEnemyEmissive(enemy, 0xff0000, 0.5);
    }

    endCombat() {
        this.combatActive = false;
        this.battleID = null;
        this.cheerMeter = 0;
        this.comboCount = 0;

        console.log('✅ Combat beendet');
    }

    victory() {
        console.log('🎉 VICTORY!');
        this.endCombat();
    }

    gameOver() {
        console.log('💀 GAME OVER');
        this.endCombat();

        // Respawn nach 2s
        setTimeout(() => {
            this.playerHealth = this.playerMaxHealth;
            console.log('♻️ Respawned');
        }, 2000);
    }

    // ===== PUBLIC API =====

    getStats() {
        return {
            combatActive: this.combatActive,
            combatMode: this.combatMode,
            health: this.playerHealth,
            maxHealth: this.playerMaxHealth,
            mana: this.playerMana,
            maxMana: this.playerMaxMana,
            stamina: this.playerStamina,
            maxStamina: this.playerMaxStamina,
            cheerMeter: this.cheerMeter,
            comboCount: this.comboCount,
            isBlocking: this.isBlocking,
            isDodging: this.isDodging
        };
    }

    setCombatMode(mode) {
        if (['MANUAL', 'ASSIST', 'AUTO'].includes(mode)) {
            this.combatMode = mode;
            console.log(`🎮 Combat Mode: ${mode}`);
        }
    }

    equipWeapon(hand, weapon) {
        if (hand === 'left') {
            this.leftHandWeapon = weapon;
        } else if (hand === 'right') {
            this.rightHandWeapon = weapon;
        }
        console.log(`⚔️ ${hand} Hand: ${weapon.type} equipped`);
    }
}

// Export for global use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RealtimeCombat;
}
