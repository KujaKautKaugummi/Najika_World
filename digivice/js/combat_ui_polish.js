/**
 * Combat UI Polish - Najika World
 * ==================================
 * Visuelles Kampf-Feedback System:
 * - Damage Numbers (floating, farbcodiert)
 * - Hit-Flash (Screen Shake + Edge Glow)
 * - Combo Counter mit Multiplier
 * - HP/MP Bars mit Animationen
 * - Skill-Cooldown Radiale Anzeige
 * - Critical Hit Effekte
 * - Status-Effect Icons (Burn, Freeze, Poison, etc.)
 * - Kill-Streak Announcements
 *
 * Arbeitet mit battle_core.js, real_3d_combat.js zusammen.
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // CONFIG
    // ==========================================

    const CONFIG = {
        damageNumberDuration: 1200,
        damageNumberRise: 60,
        screenShakeDuration: 200,
        screenShakeIntensity: 8,
        comboTimeout: 3000,
        maxDamageNumbers: 30,
        hitFlashDuration: 150
    };

    const DAMAGE_COLORS = {
        physical:  '#FFFFFF',
        fire:      '#FF4444',
        ice:       '#88CCFF',
        lightning: '#FFD700',
        poison:    '#44FF44',
        nature:    '#4CAF50',
        holy:      '#FFFFAA',
        dark:      '#9944CC',
        critical:  '#FFD700',
        heal:      '#44FF88',
        miss:      'rgba(255,255,255,0.4)'
    };

    const STATUS_EFFECTS = {
        burn:      { icon: '\uD83D\uDD25', color: '#FF4444', name: 'Verbrennung' },
        freeze:    { icon: '\u2744',       color: '#88CCFF', name: 'Eingefroren' },
        poison:    { icon: '\u2620',       color: '#44FF44', name: 'Vergiftet' },
        stun:      { icon: '\uD83D\uDCAB', color: '#FFD700', name: 'Betaeubt' },
        bleed:     { icon: '\uD83E\uDE78', color: '#CC0000', name: 'Blutung' },
        slow:      { icon: '\uD83D\uDC22', color: '#8888FF', name: 'Verlangsamt' },
        shield:    { icon: '\uD83D\uDEE1',  color: '#4CAF50', name: 'Geschuetzt' },
        regen:     { icon: '\uD83D\uDC9A', color: '#44FF88', name: 'Regeneration' },
        berserk:   { icon: '\uD83D\uDCA2', color: '#FF6600', name: 'Berserker' },
        paralyze:  { icon: '\u26A1',       color: '#FFDD00', name: 'Paralysiert' }
    };

    // ==========================================
    // STATE
    // ==========================================

    let combatState = {
        damageNumbers: [],
        comboCount: 0,
        comboTimer: null,
        maxCombo: 0,
        killStreak: 0,
        screenShaking: false,
        activeEffects: [],    // player status effects
        enemyEffects: [],     // enemy status effects
        playerHP: 100,
        playerMaxHP: 100,
        playerMP: 50,
        playerMaxMP: 50,
        enemyHP: 100,
        enemyMaxHP: 100,
        enemyName: '',
        isInCombat: false,
        cooldowns: {},       // skillId -> { current, max }
        damageNumberId: 0
    };

    // ==========================================
    // DAMAGE NUMBERS
    // ==========================================

    function showDamageNumber(amount, type, x, y, isCrit) {
        if (combatState.damageNumbers.length >= CONFIG.maxDamageNumbers) {
            combatState.damageNumbers.shift();
        }

        const id = ++combatState.damageNumberId;
        const color = isCrit ? DAMAGE_COLORS.critical : (DAMAGE_COLORS[type] || DAMAGE_COLORS.physical);
        const isHeal = type === 'heal';
        const isMiss = type === 'miss';

        // Random X spread
        const spreadX = (Math.random() - 0.5) * 40;

        const el = document.createElement('div');
        el.id = `dmg-${id}`;
        el.style.cssText = `
            position:fixed;
            left:${x + spreadX}px;
            top:${y}px;
            color:${color};
            font-family:'Courier New',monospace;
            font-weight:bold;
            font-size:${isCrit ? '22px' : isMiss ? '12px' : '16px'};
            z-index:11000;
            pointer-events:none;
            text-shadow:0 0 ${isCrit ? '12' : '6'}px ${color},
                         0 2px 4px rgba(0,0,0,0.8);
            transition:transform ${CONFIG.damageNumberDuration}ms ease-out,
                       opacity ${CONFIG.damageNumberDuration}ms ease-in;
            transform:translateY(0) scale(${isCrit ? 1.3 : 1});
            opacity:1;
            ${isCrit ? 'letter-spacing:2px;' : ''}
        `;

        if (isMiss) {
            el.textContent = 'MISS';
        } else if (isHeal) {
            el.textContent = `+${amount}`;
        } else {
            el.textContent = isCrit ? `${amount}!` : `${amount}`;
        }

        document.body.appendChild(el);

        // Animate
        requestAnimationFrame(() => {
            el.style.transform = `translateY(-${CONFIG.damageNumberRise}px) scale(${isCrit ? 0.8 : 0.7})`;
            el.style.opacity = '0';
        });

        setTimeout(() => el.remove(), CONFIG.damageNumberDuration);

        combatState.damageNumbers.push({ id, el });
    }

    // ==========================================
    // SCREEN SHAKE
    // ==========================================

    function screenShake(intensity) {
        if (combatState.screenShaking) return;
        combatState.screenShaking = true;

        const canvas = document.querySelector('canvas');
        const target = canvas || document.body;
        const power = intensity || CONFIG.screenShakeIntensity;
        const duration = CONFIG.screenShakeDuration;
        const startTime = performance.now();

        function shake(time) {
            const elapsed = time - startTime;
            if (elapsed > duration) {
                target.style.transform = '';
                combatState.screenShaking = false;
                return;
            }

            const decay = 1 - elapsed / duration;
            const dx = (Math.random() - 0.5) * power * decay;
            const dy = (Math.random() - 0.5) * power * decay;
            target.style.transform = `translate(${dx}px, ${dy}px)`;

            requestAnimationFrame(shake);
        }

        requestAnimationFrame(shake);
    }

    // ==========================================
    // HIT FLASH (Edge Glow)
    // ==========================================

    function hitFlash(color, isTakingDamage) {
        const existing = document.getElementById('combat-hit-flash');
        if (existing) existing.remove();

        const flash = document.createElement('div');
        flash.id = 'combat-hit-flash';
        flash.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            pointer-events:none;z-index:10999;
            ${isTakingDamage ?
                `background:radial-gradient(ellipse at center,
                    transparent 50%,
                    ${color || 'rgba(255,0,0,0.3)'} 100%);` :
                `box-shadow:inset 0 0 60px ${color || 'rgba(255,68,68,0.4)'};`
            }
            opacity:1;
            transition:opacity ${CONFIG.hitFlashDuration}ms ease-out;
        `;
        document.body.appendChild(flash);

        requestAnimationFrame(() => { flash.style.opacity = '0'; });
        setTimeout(() => flash.remove(), CONFIG.hitFlashDuration);
    }

    // ==========================================
    // COMBO COUNTER
    // ==========================================

    function incrementCombo() {
        combatState.comboCount++;
        if (combatState.comboCount > combatState.maxCombo) {
            combatState.maxCombo = combatState.comboCount;
        }

        // Reset timer
        if (combatState.comboTimer) clearTimeout(combatState.comboTimer);
        combatState.comboTimer = setTimeout(() => {
            combatState.comboCount = 0;
            updateComboDisplay();
        }, CONFIG.comboTimeout);

        updateComboDisplay();
    }

    function updateComboDisplay() {
        let comboEl = document.getElementById('combat-combo');

        if (combatState.comboCount <= 1) {
            if (comboEl) comboEl.remove();
            return;
        }

        if (!comboEl) {
            comboEl = document.createElement('div');
            comboEl.id = 'combat-combo';
            comboEl.style.cssText = `
                position:fixed;right:30px;top:50%;transform:translateY(-50%);
                font-family:'Courier New',monospace;
                z-index:10998;pointer-events:none;
                text-align:right;
            `;
            document.body.appendChild(comboEl);
        }

        const multiplier = 1 + (combatState.comboCount - 1) * 0.1;
        const comboColor = combatState.comboCount >= 20 ? '#FFD700' :
                          combatState.comboCount >= 10 ? '#FF4444' :
                          combatState.comboCount >= 5 ? '#FF9800' : '#4CAF50';

        comboEl.innerHTML = `
            <div style="font-size:36px;color:${comboColor};font-weight:bold;
                text-shadow:0 0 20px ${comboColor};
                animation:comboPulse 0.3s ease-out;">
                ${combatState.comboCount}
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.6);letter-spacing:2px;">
                COMBO
            </div>
            <div style="font-size:10px;color:${comboColor};margin-top:2px;">
                x${multiplier.toFixed(1)}
            </div>
        `;

        // Pulse animation
        comboEl.style.animation = 'none';
        comboEl.offsetHeight; // reflow
        comboEl.style.animation = '';
    }

    // ==========================================
    // HP/MP BARS
    // ==========================================

    function createCombatHUD() {
        const existing = document.getElementById('combat-hud');
        if (existing) existing.remove();

        const hud = document.createElement('div');
        hud.id = 'combat-hud';
        hud.style.cssText = `
            position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
            width:600px;max-width:90vw;
            font-family:'Courier New',monospace;
            z-index:10500;pointer-events:none;
        `;

        hud.innerHTML = `
            <!-- Player Bars -->
            <div style="display:flex;gap:12px;align-items:end;">
                <!-- Player Info -->
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                        <span style="font-size:11px;color:white;font-weight:bold;">Spieler</span>
                        <span id="combat-hp-text" style="font-size:10px;color:#FF4444;">
                            ${combatState.playerHP}/${combatState.playerMaxHP}
                        </span>
                    </div>
                    <!-- HP Bar -->
                    <div style="background:rgba(0,0,0,0.6);height:14px;border-radius:7px;
                        overflow:hidden;border:1px solid rgba(255,68,68,0.3);position:relative;">
                        <div id="combat-hp-bar-bg" style="position:absolute;height:100%;
                            background:rgba(255,68,68,0.2);width:100%;border-radius:7px;
                            transition:width 0.8s ease;"></div>
                        <div id="combat-hp-bar" style="position:absolute;height:100%;
                            background:linear-gradient(90deg,#CC0000,#FF4444);
                            width:${(combatState.playerHP / combatState.playerMaxHP * 100)}%;
                            border-radius:7px;transition:width 0.3s ease;"></div>
                    </div>
                    <!-- MP Bar -->
                    <div style="margin-top:4px;display:flex;justify-content:space-between;">
                        <span style="font-size:9px;color:rgba(68,136,255,0.6);">MP</span>
                        <span id="combat-mp-text" style="font-size:9px;color:#4488FF;">
                            ${combatState.playerMP}/${combatState.playerMaxMP}
                        </span>
                    </div>
                    <div style="background:rgba(0,0,0,0.6);height:8px;border-radius:4px;
                        overflow:hidden;border:1px solid rgba(68,136,255,0.2);">
                        <div id="combat-mp-bar" style="height:100%;
                            background:linear-gradient(90deg,#2244AA,#4488FF);
                            width:${(combatState.playerMP / combatState.playerMaxMP * 100)}%;
                            border-radius:4px;transition:width 0.3s ease;"></div>
                    </div>
                    <!-- Status Effects -->
                    <div id="combat-player-effects" style="display:flex;gap:4px;margin-top:6px;"></div>
                </div>

                <!-- Enemy Info -->
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                        <span id="combat-enemy-name" style="font-size:11px;color:white;font-weight:bold;">
                            ${combatState.enemyName || 'Gegner'}
                        </span>
                        <span id="combat-enemy-hp-text" style="font-size:10px;color:#FF4444;">
                            ${combatState.enemyHP}/${combatState.enemyMaxHP}
                        </span>
                    </div>
                    <div style="background:rgba(0,0,0,0.6);height:14px;border-radius:7px;
                        overflow:hidden;border:1px solid rgba(255,68,68,0.3);position:relative;">
                        <div id="combat-enemy-hp-bg" style="position:absolute;height:100%;
                            background:rgba(255,68,68,0.2);width:100%;border-radius:7px;
                            transition:width 0.8s ease;"></div>
                        <div id="combat-enemy-hp-bar" style="position:absolute;height:100%;
                            background:linear-gradient(90deg,#880000,#CC3333);
                            width:${(combatState.enemyHP / combatState.enemyMaxHP * 100)}%;
                            border-radius:7px;transition:width 0.3s ease;"></div>
                    </div>
                    <div id="combat-enemy-effects" style="display:flex;gap:4px;margin-top:6px;"></div>
                </div>
            </div>
        `;

        document.body.appendChild(hud);
    }

    function updateHPBar(target, current, max) {
        const percent = Math.max(0, Math.min(100, (current / max) * 100));

        if (target === 'player') {
            combatState.playerHP = current;
            combatState.playerMaxHP = max;
            const bar = document.getElementById('combat-hp-bar');
            const bg = document.getElementById('combat-hp-bar-bg');
            const text = document.getElementById('combat-hp-text');
            if (bar) bar.style.width = percent + '%';
            if (bg) setTimeout(() => { bg.style.width = percent + '%'; }, 500);
            if (text) text.textContent = `${Math.round(current)}/${max}`;
        } else {
            combatState.enemyHP = current;
            combatState.enemyMaxHP = max;
            const bar = document.getElementById('combat-enemy-hp-bar');
            const bg = document.getElementById('combat-enemy-hp-bg');
            const text = document.getElementById('combat-enemy-hp-text');
            if (bar) bar.style.width = percent + '%';
            if (bg) setTimeout(() => { bg.style.width = percent + '%'; }, 500);
            if (text) text.textContent = `${Math.round(current)}/${max}`;
        }
    }

    function updateMPBar(current, max) {
        combatState.playerMP = current;
        combatState.playerMaxMP = max;
        const percent = Math.max(0, Math.min(100, (current / max) * 100));
        const bar = document.getElementById('combat-mp-bar');
        const text = document.getElementById('combat-mp-text');
        if (bar) bar.style.width = percent + '%';
        if (text) text.textContent = `${Math.round(current)}/${max}`;
    }

    // ==========================================
    // STATUS EFFECTS
    // ==========================================

    function addStatusEffect(target, effectKey, duration) {
        const effect = STATUS_EFFECTS[effectKey];
        if (!effect) return;

        const effects = target === 'player' ? combatState.activeEffects : combatState.enemyEffects;
        const existing = effects.find(e => e.key === effectKey);
        if (existing) {
            existing.endTime = Date.now() + duration;
            return;
        }

        effects.push({
            key: effectKey,
            endTime: Date.now() + duration,
            ...effect
        });

        renderStatusEffects(target);
    }

    function removeStatusEffect(target, effectKey) {
        const effects = target === 'player' ? combatState.activeEffects : combatState.enemyEffects;
        const idx = effects.findIndex(e => e.key === effectKey);
        if (idx > -1) effects.splice(idx, 1);
        renderStatusEffects(target);
    }

    function renderStatusEffects(target) {
        const containerId = target === 'player' ? 'combat-player-effects' : 'combat-enemy-effects';
        const container = document.getElementById(containerId);
        if (!container) return;

        const effects = target === 'player' ? combatState.activeEffects : combatState.enemyEffects;

        container.innerHTML = effects.map(e => {
            const remaining = Math.max(0, Math.round((e.endTime - Date.now()) / 1000));
            return `
                <div style="background:${e.color}22;border:1px solid ${e.color}44;
                    border-radius:4px;padding:2px 4px;display:flex;align-items:center;gap:3px;"
                    title="${e.name} (${remaining}s)">
                    <span style="font-size:10px;">${e.icon}</span>
                    <span style="font-size:7px;color:${e.color};">${remaining}s</span>
                </div>
            `;
        }).join('');
    }

    // Periodic effect cleanup
    setInterval(() => {
        const now = Date.now();
        combatState.activeEffects = combatState.activeEffects.filter(e => e.endTime > now);
        combatState.enemyEffects = combatState.enemyEffects.filter(e => e.endTime > now);
        if (combatState.isInCombat) {
            renderStatusEffects('player');
            renderStatusEffects('enemy');
        }
    }, 1000);

    // ==========================================
    // SKILL COOLDOWN DISPLAY
    // ==========================================

    function setCooldown(skillId, duration) {
        combatState.cooldowns[skillId] = {
            startTime: Date.now(),
            duration: duration,
            endTime: Date.now() + duration
        };
    }

    function getCooldownRemaining(skillId) {
        const cd = combatState.cooldowns[skillId];
        if (!cd) return 0;
        const remaining = cd.endTime - Date.now();
        return remaining > 0 ? remaining : 0;
    }

    function getCooldownPercent(skillId) {
        const cd = combatState.cooldowns[skillId];
        if (!cd) return 0;
        const remaining = cd.endTime - Date.now();
        if (remaining <= 0) return 0;
        return remaining / cd.duration;
    }

    // ==========================================
    // KILL STREAK ANNOUNCEMENTS
    // ==========================================

    const KILL_STREAK_NAMES = {
        2: { text: 'DOUBLE KILL', color: '#4CAF50' },
        3: { text: 'TRIPLE KILL', color: '#FF9800' },
        5: { text: 'RAMPAGE!', color: '#FF4444' },
        8: { text: 'UNSTOPPABLE!', color: '#9C27B0' },
        10: { text: 'GODLIKE!', color: '#FFD700' },
        15: { text: 'LEGENDARY!', color: '#FFD700' }
    };

    function onEnemyKilled() {
        combatState.killStreak++;
        const streak = KILL_STREAK_NAMES[combatState.killStreak];

        if (streak) {
            showKillStreakAnnouncement(streak.text, streak.color);
        }
    }

    function showKillStreakAnnouncement(text, color) {
        const el = document.createElement('div');
        el.style.cssText = `
            position:fixed;top:30%;left:50%;transform:translate(-50%,-50%) scale(0.5);
            font-family:'Courier New',monospace;font-size:32px;font-weight:bold;
            color:${color};text-shadow:0 0 30px ${color}, 0 0 60px ${color};
            z-index:11001;pointer-events:none;opacity:0;
            letter-spacing:4px;
            transition:all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        `;
        el.textContent = text;
        document.body.appendChild(el);

        requestAnimationFrame(() => {
            el.style.opacity = '1';
            el.style.transform = 'translate(-50%,-50%) scale(1)';
        });

        setTimeout(() => {
            el.style.opacity = '0';
            el.style.transform = 'translate(-50%,-50%) scale(1.5)';
            setTimeout(() => el.remove(), 500);
        }, 2000);
    }

    // ==========================================
    // CRITICAL HIT EFFECT
    // ==========================================

    function criticalHitEffect(x, y) {
        // Star burst
        for (let i = 0; i < 6; i++) {
            const angle = (i / 6) * Math.PI * 2;
            const star = document.createElement('div');
            star.style.cssText = `
                position:fixed;left:${x}px;top:${y}px;
                width:4px;height:4px;background:#FFD700;border-radius:50%;
                z-index:11000;pointer-events:none;
                box-shadow:0 0 8px #FFD700;
                transition:all 0.6s ease-out;
                opacity:1;
            `;
            document.body.appendChild(star);

            requestAnimationFrame(() => {
                star.style.left = (x + Math.cos(angle) * 60) + 'px';
                star.style.top = (y + Math.sin(angle) * 60) + 'px';
                star.style.opacity = '0';
            });

            setTimeout(() => star.remove(), 600);
        }

        // Flash text
        const crit = document.createElement('div');
        crit.style.cssText = `
            position:fixed;left:${x}px;top:${y - 30}px;
            transform:translate(-50%,-50%) scale(0.5);
            font-family:'Courier New',monospace;font-size:14px;font-weight:bold;
            color:#FFD700;text-shadow:0 0 10px #FFD700;
            z-index:11000;pointer-events:none;opacity:0;
            transition:all 0.3s ease-out;
        `;
        crit.textContent = 'CRITICAL!';
        document.body.appendChild(crit);

        requestAnimationFrame(() => {
            crit.style.opacity = '1';
            crit.style.transform = 'translate(-50%,-50%) scale(1)';
        });

        setTimeout(() => {
            crit.style.opacity = '0';
            crit.style.transform = 'translate(-50%,-100%) scale(0.8)';
            setTimeout(() => crit.remove(), 300);
        }, 600);
    }

    // ==========================================
    // COMBAT LIFECYCLE
    // ==========================================

    function startCombat(enemyName, enemyHP) {
        combatState.isInCombat = true;
        combatState.enemyName = enemyName;
        combatState.enemyHP = enemyHP;
        combatState.enemyMaxHP = enemyHP;
        combatState.comboCount = 0;
        combatState.killStreak = 0;
        combatState.activeEffects = [];
        combatState.enemyEffects = [];
        combatState.cooldowns = {};

        createCombatHUD();
    }

    function endCombat() {
        combatState.isInCombat = false;

        const hud = document.getElementById('combat-hud');
        if (hud) {
            hud.style.transition = 'opacity 0.5s';
            hud.style.opacity = '0';
            setTimeout(() => hud.remove(), 500);
        }

        const combo = document.getElementById('combat-combo');
        if (combo) combo.remove();
    }

    // ==========================================
    // CONVENIENCE: onHit
    // ==========================================

    function onPlayerHit(damage, type, isCrit, screenX, screenY) {
        const x = screenX || window.innerWidth * 0.35;
        const y = screenY || window.innerHeight * 0.6;

        showDamageNumber(damage, type || 'physical', x, y, isCrit);
        hitFlash(DAMAGE_COLORS[type] || 'rgba(255,0,0,0.3)', true);
        screenShake(isCrit ? CONFIG.screenShakeIntensity * 1.5 : CONFIG.screenShakeIntensity * 0.5);

        if (isCrit) criticalHitEffect(x, y);

        combatState.playerHP = Math.max(0, combatState.playerHP - damage);
        updateHPBar('player', combatState.playerHP, combatState.playerMaxHP);
    }

    function onEnemyHit(damage, type, isCrit, screenX, screenY) {
        const x = screenX || window.innerWidth * 0.65;
        const y = screenY || window.innerHeight * 0.4;

        showDamageNumber(damage, type || 'physical', x, y, isCrit);
        incrementCombo();

        if (isCrit) {
            criticalHitEffect(x, y);
            screenShake(CONFIG.screenShakeIntensity);
        }

        combatState.enemyHP = Math.max(0, combatState.enemyHP - damage);
        updateHPBar('enemy', combatState.enemyHP, combatState.enemyMaxHP);

        if (combatState.enemyHP <= 0) {
            onEnemyKilled();
        }
    }

    function onPlayerHeal(amount, screenX, screenY) {
        const x = screenX || window.innerWidth * 0.35;
        const y = screenY || window.innerHeight * 0.5;

        showDamageNumber(amount, 'heal', x, y, false);
        hitFlash('rgba(68,255,136,0.2)', false);

        combatState.playerHP = Math.min(combatState.playerMaxHP, combatState.playerHP + amount);
        updateHPBar('player', combatState.playerHP, combatState.playerMaxHP);
    }

    // ==========================================
    // CSS ANIMATIONS
    // ==========================================

    const style = document.createElement('style');
    style.textContent = `
        @keyframes comboPulse {
            0% { transform: translateY(-50%) scale(1.3); }
            100% { transform: translateY(-50%) scale(1); }
        }
    `;
    document.head.appendChild(style);

    // ==========================================
    // EXPORT
    // ==========================================

    window.CombatUIPolish = {
        // Core
        showDamageNumber,
        screenShake,
        hitFlash,
        criticalHitEffect,
        // Combo
        incrementCombo,
        getCombo: () => combatState.comboCount,
        getMaxCombo: () => combatState.maxCombo,
        // Bars
        createCombatHUD,
        updateHPBar,
        updateMPBar,
        // Status Effects
        addStatusEffect,
        removeStatusEffect,
        STATUS_EFFECTS,
        // Cooldowns
        setCooldown,
        getCooldownRemaining,
        getCooldownPercent,
        // Kill Streak
        onEnemyKilled,
        getKillStreak: () => combatState.killStreak,
        // Lifecycle
        startCombat,
        endCombat,
        // Convenience
        onPlayerHit,
        onEnemyHit,
        onPlayerHeal,
        // Config
        CONFIG,
        DAMAGE_COLORS
    };

    console.log('[OK] Combat UI Polish geladen: Damage Numbers, Combos, Hit-Flash, Status Effects');

})();
