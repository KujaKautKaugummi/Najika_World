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
    constructor(scene, THREE) {
        this.scene = scene;
        this.THREE = THREE;

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

        // Random Variance
        baseDamage *= (0.9 + Math.random() * 0.2); // 90-110%

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
        // TODO: Create 3D Text floating upwards
        console.log(`-${damage} HP`);
    }

    // ===== UPDATE LOOP =====

    update(delta) {
        if (!this.combatActive) return;

        // Update Cooldowns
        if (this.leftHandCooldown > 0) this.leftHandCooldown -= delta * 1000;
        if (this.rightHandCooldown > 0) this.rightHandCooldown -= delta * 1000;
        if (this.bothHandsCooldown > 0) this.bothHandsCooldown -= delta * 1000;

        // Stamina Regen
        if (this.playerStamina < this.playerMaxStamina) {
            this.playerStamina = Math.min(this.playerMaxStamina, this.playerStamina + delta * 10);
        }

        // Update Enemies (AI)
        this.updateEnemies(delta);
    }

    updateEnemies(delta) {
        // TODO: Enemy AI behavior
    }

    // ===== COMBAT LIFECYCLE =====

    async startCombat(enemies) {
        this.enemies = enemies;
        this.currentTarget = enemies[0];

        // Start battle with backend
        const enemyTypes = enemies.map(e => e.type);
        await this.startBattleWithBackend(enemyTypes);

        console.log('⚔️ Combat gestartet!');
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
