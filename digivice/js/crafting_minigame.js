/**
 * Crafting Minigame - Najika World
 * ==================================
 * Timing-basiertes Crafting Minigame:
 * - Schmiede-Rhythmus: Triff die Timing-Zone!
 * - 3 Phasen: Erhitzen, Haemmern, Abkuehlen
 * - Qualitaets-System (Normal, Gut, Perfekt)
 * - Schwierigkeitsgrad skaliert mit Rezept-Raritaet
 * - Combo-Bonus fuer mehrere perfekte Treffer
 * - Visuelles Feedback: Canvas-Animationen
 * - Rezeptbuch Integration
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // CRAFTING RECIPES
    // ==========================================

    const RECIPES = {
        // Waffen
        iron_sword: {
            name: 'Eisenschwert', icon: '\u2694', rarity: 'common',
            materials: [{ id: 'iron_ore', name: 'Eisenerz', count: 3, icon: '\u26CF' }],
            difficulty: 1, phases: 3, result: { type: 'weapon', damage: 12 }
        },
        steel_sword: {
            name: 'Stahlschwert', icon: '\u2694', rarity: 'uncommon',
            materials: [
                { id: 'iron_ore', name: 'Eisenerz', count: 5, icon: '\u26CF' },
                { id: 'coal', name: 'Kohle', count: 2, icon: '\u26AB' }
            ],
            difficulty: 2, phases: 4, result: { type: 'weapon', damage: 22 }
        },
        fire_sword: {
            name: 'Flammenschwert', icon: '\uD83D\uDD25', rarity: 'rare',
            materials: [
                { id: 'iron_ore', name: 'Eisenerz', count: 5, icon: '\u26CF' },
                { id: 'fire_essence', name: 'Feuer-Essenz', count: 2, icon: '\uD83D\uDD25' },
                { id: 'crystal_shard', name: 'Kristallsplitter', count: 1, icon: '\uD83D\uDC8E' }
            ],
            difficulty: 3, phases: 5, result: { type: 'weapon', damage: 28, fireDmg: 15 }
        },
        // Ruestungen
        leather_armor: {
            name: 'Lederruestung', icon: '\uD83E\uDDE5', rarity: 'common',
            materials: [{ id: 'leather', name: 'Leder', count: 4, icon: '\uD83E\uDE76' }],
            difficulty: 1, phases: 3, result: { type: 'armor', defense: 8 }
        },
        knight_armor: {
            name: 'Ritterruestung', icon: '\uD83D\uDEE1', rarity: 'uncommon',
            materials: [
                { id: 'iron_ore', name: 'Eisenerz', count: 8, icon: '\u26CF' },
                { id: 'leather', name: 'Leder', count: 3, icon: '\uD83E\uDE76' }
            ],
            difficulty: 2, phases: 4, result: { type: 'armor', defense: 22 }
        },
        // Traenke
        hp_potion: {
            name: 'Heiltrank', icon: '\u2764', rarity: 'common',
            materials: [
                { id: 'herb_red', name: 'Rotes Kraut', count: 2, icon: '\uD83C\uDF3F' },
                { id: 'water', name: 'Reines Wasser', count: 1, icon: '\uD83D\uDCA7' }
            ],
            difficulty: 1, phases: 2, result: { type: 'consumable', heal: 50 }
        },
        mp_potion: {
            name: 'Manatrank', icon: '\uD83D\uDCA7', rarity: 'common',
            materials: [
                { id: 'herb_blue', name: 'Blaues Kraut', count: 2, icon: '\uD83C\uDF3F' },
                { id: 'crystal_shard', name: 'Kristallsplitter', count: 1, icon: '\uD83D\uDC8E' }
            ],
            difficulty: 1, phases: 2, result: { type: 'consumable', mana: 30 }
        },
        crystal_staff: {
            name: 'Kristallstab', icon: '\uD83D\uDD2E', rarity: 'epic',
            materials: [
                { id: 'crystal_shard', name: 'Kristallsplitter', count: 5, icon: '\uD83D\uDC8E' },
                { id: 'magic_wood', name: 'Magisches Holz', count: 2, icon: '\uD83C\uDF33' },
                { id: 'star_dust', name: 'Sternenstaub', count: 1, icon: '\u2728' }
            ],
            difficulty: 4, phases: 6, result: { type: 'weapon', magicDmg: 45, mana: 20 }
        }
    };

    const PHASE_TYPES = {
        heat:   { name: 'Erhitzen',   icon: '\uD83D\uDD25', color: '#FF4444', instruction: 'Halte die Temperatur in der Zone!' },
        hammer: { name: 'Haemmern',   icon: '\uD83D\uDD28', color: '#FF9800', instruction: 'Druecke SPACE im richtigen Moment!' },
        cool:   { name: 'Abkuehlen',  icon: '\u2744',       color: '#4A90D9', instruction: 'Warte auf den perfekten Moment!' },
        mix:    { name: 'Mischen',    icon: '\uD83E\uDDEA', color: '#4CAF50', instruction: 'Triff die Mischzone genau!' },
        polish: { name: 'Polieren',   icon: '\u2728',       color: '#FFD700', instruction: 'Rhythmisch druecken fuer Glanz!' },
        enchant:{ name: 'Verzaubern', icon: '\uD83D\uDD2E', color: '#9C27B0', instruction: 'Triff alle magischen Punkte!' }
    };

    const QUALITY_THRESHOLDS = {
        perfect: { min: 0.85, name: 'Perfekt!',  color: '#FFD700', multiplier: 1.5 },
        good:    { min: 0.60, name: 'Gut',        color: '#4CAF50', multiplier: 1.2 },
        normal:  { min: 0.30, name: 'Normal',     color: 'rgba(255,255,255,0.5)', multiplier: 1.0 },
        fail:    { min: 0.00, name: 'Misslungen',  color: '#FF4444', multiplier: 0.5 }
    };

    // ==========================================
    // MINIGAME STATE
    // ==========================================

    let gameState = {
        isOpen: false,
        isPlaying: false,
        container: null,
        canvas: null,
        ctx: null,
        // Current recipe
        currentRecipe: null,
        currentPhase: 0,
        phases: [],
        // Timing bar
        barPosition: 0,       // 0-1 position on the bar
        barSpeed: 0.008,      // speed per frame
        barDirection: 1,       // 1 or -1
        targetZone: { start: 0.4, end: 0.6 }, // green zone
        // Results
        phaseResults: [],      // quality per phase
        comboCount: 0,
        totalScore: 0,
        // Animation
        animationId: null,
        particles: [],
        hammerAngle: 0,
        glowIntensity: 0
    };

    // ==========================================
    // RECIPE BOOK UI
    // ==========================================

    function openCraftingUI() {
        if (gameState.isOpen) { closeCraftingUI(); return; }
        gameState.isOpen = true;

        const container = document.createElement('div');
        container.id = 'crafting-minigame';
        container.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.97);z-index:9500;
            display:flex;align-items:center;justify-content:center;
            font-family:'Courier New',monospace;
        `;
        gameState.container = container;

        // If not playing, show recipe selection
        if (!gameState.isPlaying) {
            container.innerHTML = buildRecipeSelection();
        }

        // Close
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '\u2715 ESC';
        closeBtn.style.cssText = `
            position:absolute;top:16px;right:20px;background:rgba(244,67,54,0.15);
            border:1px solid rgba(244,67,54,0.3);color:#F44336;
            padding:6px 14px;border-radius:4px;cursor:pointer;
            font-family:inherit;font-size:10px;z-index:10;
        `;
        closeBtn.onclick = closeCraftingUI;
        container.appendChild(closeBtn);

        document.body.appendChild(container);

        gameState._escHandler = (e) => {
            if (e.key === 'Escape') closeCraftingUI();
        };
        document.addEventListener('keydown', gameState._escHandler);
    }

    function closeCraftingUI() {
        gameState.isOpen = false;
        gameState.isPlaying = false;
        if (gameState.animationId) cancelAnimationFrame(gameState.animationId);
        if (gameState._spaceHandler) document.removeEventListener('keydown', gameState._spaceHandler);
        if (gameState._escHandler) document.removeEventListener('keydown', gameState._escHandler);

        const container = document.getElementById('crafting-minigame');
        if (container) container.remove();
    }

    function buildRecipeSelection() {
        const rarityColors = {
            common: 'rgba(255,255,255,0.5)', uncommon: '#4CAF50',
            rare: '#2196F3', epic: '#9C27B0', legendary: '#FFD700'
        };

        return `
            <div style="max-width:700px;width:90%;">
                <div style="text-align:center;margin-bottom:24px;">
                    <div style="font-size:16px;color:#FF9800;font-weight:bold;">
                        \uD83D\uDD28 Schmiede & Crafting
                    </div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px;">
                        Waehle ein Rezept zum Craften
                    </div>
                </div>

                <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;">
                    ${Object.entries(RECIPES).map(([key, recipe]) => {
                        const rColor = rarityColors[recipe.rarity] || 'rgba(255,255,255,0.5)';
                        const difficulty = '\u2605'.repeat(recipe.difficulty) +
                                          '\u2606'.repeat(5 - recipe.difficulty);

                        return `
                            <div onclick="window.CraftingMinigame.start('${key}')"
                                style="background:rgba(255,255,255,0.02);
                                border:1px solid rgba(255,255,255,0.06);
                                border-radius:8px;padding:14px;cursor:pointer;
                                transition:all 0.15s;"
                                onmouseover="this.style.background='rgba(255,255,255,0.04)';this.style.borderColor='${rColor}44'"
                                onmouseout="this.style.background='rgba(255,255,255,0.02)';this.style.borderColor='rgba(255,255,255,0.06)'">

                                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                    <span style="font-size:24px;">${recipe.icon}</span>
                                    <div>
                                        <div style="font-size:11px;color:${rColor};font-weight:bold;">
                                            ${recipe.name}</div>
                                        <div style="font-size:8px;color:rgba(255,255,255,0.3);">
                                            ${recipe.rarity.toUpperCase()}</div>
                                    </div>
                                </div>

                                <div style="font-size:9px;color:rgba(255,152,0,0.6);margin-bottom:6px;">
                                    ${difficulty}
                                </div>

                                <div style="font-size:8px;color:rgba(255,255,255,0.3);margin-bottom:6px;">
                                    Materialien:
                                </div>
                                ${recipe.materials.map(m => `
                                    <div style="font-size:9px;color:rgba(255,255,255,0.5);
                                        padding:1px 0;">
                                        ${m.icon} ${m.name} x${m.count}
                                    </div>
                                `).join('')}

                                <div style="margin-top:8px;font-size:9px;color:rgba(255,255,255,0.3);">
                                    ${recipe.phases} Phasen
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }

    // ==========================================
    // MINIGAME CORE
    // ==========================================

    function startCrafting(recipeKey) {
        const recipe = RECIPES[recipeKey];
        if (!recipe) return;

        gameState.isPlaying = true;
        gameState.currentRecipe = recipe;
        gameState.currentPhase = 0;
        gameState.phaseResults = [];
        gameState.comboCount = 0;
        gameState.totalScore = 0;

        // Generate phases
        const phaseTypes = ['heat', 'hammer', 'cool', 'mix', 'polish', 'enchant'];
        gameState.phases = [];
        for (let i = 0; i < recipe.phases; i++) {
            const type = i === 0 ? 'heat' :
                        i === recipe.phases - 1 ? 'cool' :
                        phaseTypes[1 + (i % (phaseTypes.length - 2))];
            gameState.phases.push(type);
        }

        setupPhase(0);
    }

    function setupPhase(phaseIdx) {
        gameState.currentPhase = phaseIdx;
        const phaseType = gameState.phases[phaseIdx];
        const phase = PHASE_TYPES[phaseType];
        const difficulty = gameState.currentRecipe.difficulty;

        // Timing bar settings
        gameState.barPosition = 0;
        gameState.barDirection = 1;
        gameState.barSpeed = 0.006 + difficulty * 0.003; // faster with difficulty

        // Target zone (smaller with difficulty)
        const zoneSize = 0.25 - difficulty * 0.035;
        const zoneCenter = 0.3 + Math.random() * 0.4;
        gameState.targetZone = {
            start: Math.max(0.05, zoneCenter - zoneSize / 2),
            end: Math.min(0.95, zoneCenter + zoneSize / 2)
        };

        gameState.particles = [];
        gameState.hammerAngle = 0;
        gameState.glowIntensity = 0;

        // Create canvas
        const container = gameState.container;
        container.innerHTML = '';

        const canvas = document.createElement('canvas');
        canvas.width = 600;
        canvas.height = 400;
        canvas.style.cssText = 'border-radius:12px;';
        container.appendChild(canvas);

        gameState.canvas = canvas;
        gameState.ctx = canvas.getContext('2d');

        // UI overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
            pointer-events:none;width:600px;text-align:center;
        `;
        overlay.innerHTML = `
            <div style="font-size:10px;color:rgba(255,255,255,0.3);margin-bottom:-180px;">
                Phase ${phaseIdx + 1}/${gameState.phases.length}
            </div>
        `;
        container.appendChild(overlay);

        // Close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '\u2715 ESC';
        closeBtn.style.cssText = `
            position:absolute;top:16px;right:20px;background:rgba(244,67,54,0.15);
            border:1px solid rgba(244,67,54,0.3);color:#F44336;
            padding:6px 14px;border-radius:4px;cursor:pointer;
            font-family:'Courier New',monospace;font-size:10px;z-index:10;
        `;
        closeBtn.onclick = closeCraftingUI;
        container.appendChild(closeBtn);

        // Space handler
        if (gameState._spaceHandler) document.removeEventListener('keydown', gameState._spaceHandler);
        gameState._spaceHandler = (e) => {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                hitTiming();
            }
        };
        document.addEventListener('keydown', gameState._spaceHandler);

        // Also click
        canvas.onclick = () => hitTiming();

        // Start animation
        if (gameState.animationId) cancelAnimationFrame(gameState.animationId);
        animate();
    }

    // ==========================================
    // ANIMATION LOOP
    // ==========================================

    function animate() {
        if (!gameState.isPlaying) return;

        const { canvas, ctx } = gameState;
        if (!canvas || !ctx) return;

        gameState.animationId = requestAnimationFrame(animate);

        const w = canvas.width;
        const h = canvas.height;
        const phaseType = gameState.phases[gameState.currentPhase];
        const phase = PHASE_TYPES[phaseType];

        // Move bar
        gameState.barPosition += gameState.barSpeed * gameState.barDirection;
        if (gameState.barPosition >= 1) { gameState.barPosition = 1; gameState.barDirection = -1; }
        if (gameState.barPosition <= 0) { gameState.barPosition = 0; gameState.barDirection = 1; }

        // Clear
        ctx.fillStyle = '#0a0a18';
        ctx.fillRect(0, 0, w, h);

        // Background glow
        const bgGrad = ctx.createRadialGradient(w/2, h/2, 0, w/2, h/2, 200);
        bgGrad.addColorStop(0, phase.color + '15');
        bgGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, w, h);

        // Phase header
        ctx.font = 'bold 18px monospace';
        ctx.fillStyle = phase.color;
        ctx.textAlign = 'center';
        ctx.fillText(`${phase.icon} ${phase.name}`, w/2, 40);

        ctx.font = '11px monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.5)';
        ctx.fillText(phase.instruction, w/2, 60);

        // Recipe name
        ctx.font = '10px monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        ctx.fillText(`${gameState.currentRecipe.icon} ${gameState.currentRecipe.name}`, w/2, 80);

        // Phase progress
        ctx.fillStyle = 'rgba(255,255,255,0.1)';
        for (let i = 0; i < gameState.phases.length; i++) {
            const px = w/2 - (gameState.phases.length * 15) / 2 + i * 15;
            ctx.beginPath();
            ctx.arc(px + 7, 95, 4, 0, Math.PI * 2);
            if (i < gameState.currentPhase) {
                ctx.fillStyle = '#4CAF50';
            } else if (i === gameState.currentPhase) {
                ctx.fillStyle = phase.color;
            } else {
                ctx.fillStyle = 'rgba(255,255,255,0.1)';
            }
            ctx.fill();
        }

        // ---- TIMING BAR ----
        const barY = 200;
        const barH = 40;
        const barX = 60;
        const barW = w - 120;

        // Bar background
        ctx.fillStyle = 'rgba(255,255,255,0.05)';
        ctx.fillRect(barX, barY, barW, barH);
        ctx.strokeStyle = 'rgba(255,255,255,0.1)';
        ctx.strokeRect(barX, barY, barW, barH);

        // Target zone
        const zoneX = barX + gameState.targetZone.start * barW;
        const zoneW = (gameState.targetZone.end - gameState.targetZone.start) * barW;

        // Perfect zone (center 40%)
        const perfectStart = gameState.targetZone.start + (gameState.targetZone.end - gameState.targetZone.start) * 0.3;
        const perfectEnd = gameState.targetZone.start + (gameState.targetZone.end - gameState.targetZone.start) * 0.7;
        const perfectX = barX + perfectStart * barW;
        const perfectW = (perfectEnd - perfectStart) * barW;

        // Draw zones
        ctx.fillStyle = phase.color + '33';
        ctx.fillRect(zoneX, barY, zoneW, barH);
        ctx.fillStyle = phase.color + '66';
        ctx.fillRect(perfectX, barY, perfectW, barH);

        // Zone labels
        ctx.font = '8px monospace';
        ctx.fillStyle = phase.color + '88';
        ctx.textAlign = 'center';
        ctx.fillText('GUT', zoneX + zoneW / 2, barY - 4);
        ctx.fillStyle = '#FFD700';
        ctx.fillText('PERFEKT', perfectX + perfectW / 2, barY + barH + 12);

        // Moving cursor
        const cursorX = barX + gameState.barPosition * barW;
        ctx.fillStyle = 'white';
        ctx.fillRect(cursorX - 2, barY - 4, 4, barH + 8);
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        ctx.fillRect(cursorX - 1, barY - 8, 2, barH + 16);

        // Combo display
        if (gameState.comboCount > 0) {
            ctx.font = 'bold 16px monospace';
            ctx.fillStyle = gameState.comboCount >= 3 ? '#FFD700' : '#4CAF50';
            ctx.textAlign = 'right';
            ctx.fillText(`${gameState.comboCount}x COMBO`, w - 30, 40);
        }

        // Score
        ctx.font = '10px monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.4)';
        ctx.textAlign = 'left';
        ctx.fillText(`Score: ${gameState.totalScore}`, 30, 40);

        // Phase results (small icons)
        gameState.phaseResults.forEach((result, i) => {
            ctx.font = '12px monospace';
            ctx.fillStyle = result.color;
            ctx.textAlign = 'left';
            ctx.fillText(result.name === 'Perfekt!' ? '\u2605' : result.name === 'Gut' ? '\u25CB' : '\u2717',
                30 + i * 18, 60);
        });

        // Instruction
        ctx.font = 'bold 14px monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.6)';
        ctx.textAlign = 'center';
        ctx.fillText('SPACE / CLICK zum Treffen!', w/2, h - 30);

        // Particles
        gameState.particles = gameState.particles.filter(p => p.life > 0);
        gameState.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.1;
            p.life -= 2;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.life / 100;
            ctx.fill();
            ctx.globalAlpha = 1;
        });
    }

    // ==========================================
    // HIT TIMING
    // ==========================================

    function hitTiming() {
        if (!gameState.isPlaying) return;

        const pos = gameState.barPosition;
        const zone = gameState.targetZone;

        // Calculate quality
        let quality;
        const perfectStart = zone.start + (zone.end - zone.start) * 0.3;
        const perfectEnd = zone.start + (zone.end - zone.start) * 0.7;

        if (pos >= perfectStart && pos <= perfectEnd) {
            quality = QUALITY_THRESHOLDS.perfect;
            gameState.comboCount++;
        } else if (pos >= zone.start && pos <= zone.end) {
            quality = QUALITY_THRESHOLDS.good;
            gameState.comboCount++;
        } else if (pos >= zone.start - 0.1 && pos <= zone.end + 0.1) {
            quality = QUALITY_THRESHOLDS.normal;
            gameState.comboCount = 0;
        } else {
            quality = QUALITY_THRESHOLDS.fail;
            gameState.comboCount = 0;
        }

        // Score
        const comboMult = 1 + gameState.comboCount * 0.1;
        const phaseScore = Math.round(100 * quality.multiplier * comboMult);
        gameState.totalScore += phaseScore;

        gameState.phaseResults.push(quality);

        // Spawn particles
        const cx = 60 + pos * (gameState.canvas.width - 120);
        for (let i = 0; i < 12; i++) {
            gameState.particles.push({
                x: cx, y: 200,
                vx: (Math.random() - 0.5) * 6,
                vy: -Math.random() * 4 - 2,
                size: 2 + Math.random() * 3,
                color: quality.color,
                life: 60 + Math.random() * 40
            });
        }

        // Show quality text
        showQualityFlash(quality);

        // Next phase or finish
        setTimeout(() => {
            if (gameState.currentPhase + 1 < gameState.phases.length) {
                setupPhase(gameState.currentPhase + 1);
            } else {
                finishCrafting();
            }
        }, 800);

        // Stop animation temporarily
        gameState.barSpeed = 0;
    }

    function showQualityFlash(quality) {
        const flash = document.createElement('div');
        flash.style.cssText = `
            position:absolute;top:40%;left:50%;transform:translate(-50%,-50%) scale(0.5);
            font-family:'Courier New',monospace;font-size:28px;font-weight:bold;
            color:${quality.color};text-shadow:0 0 20px ${quality.color};
            z-index:11000;pointer-events:none;opacity:0;
            transition:all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        `;
        flash.textContent = quality.name;
        gameState.container.appendChild(flash);

        requestAnimationFrame(() => {
            flash.style.opacity = '1';
            flash.style.transform = 'translate(-50%,-50%) scale(1)';
        });

        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translate(-50%,-50%) scale(1.3)';
            setTimeout(() => flash.remove(), 300);
        }, 600);
    }

    // ==========================================
    // FINISH CRAFTING
    // ==========================================

    function finishCrafting() {
        gameState.isPlaying = false;
        if (gameState.animationId) cancelAnimationFrame(gameState.animationId);
        if (gameState._spaceHandler) document.removeEventListener('keydown', gameState._spaceHandler);

        // Calculate overall quality
        const perfectCount = gameState.phaseResults.filter(r => r === QUALITY_THRESHOLDS.perfect).length;
        const goodCount = gameState.phaseResults.filter(r => r === QUALITY_THRESHOLDS.good).length;
        const failCount = gameState.phaseResults.filter(r => r === QUALITY_THRESHOLDS.fail).length;
        const totalPhases = gameState.phases.length;

        let overallQuality;
        if (failCount > totalPhases / 2) {
            overallQuality = 'fail';
        } else if (perfectCount === totalPhases) {
            overallQuality = 'masterwork';
        } else if (perfectCount >= totalPhases / 2) {
            overallQuality = 'superior';
        } else if (failCount === 0) {
            overallQuality = 'good';
        } else {
            overallQuality = 'normal';
        }

        const qualityLabels = {
            fail: { name: 'Misslungen', color: '#FF4444', icon: '\u2717', bonus: -50 },
            normal: { name: 'Normal', color: 'rgba(255,255,255,0.5)', icon: '\u25CB', bonus: 0 },
            good: { name: 'Gut', color: '#4CAF50', icon: '\u2713', bonus: 10 },
            superior: { name: 'Ueberragend', color: '#2196F3', icon: '\u2605', bonus: 25 },
            masterwork: { name: 'MEISTERWERK!', color: '#FFD700', icon: '\uD83C\uDFC6', bonus: 50 }
        };

        const result = qualityLabels[overallQuality];
        const recipe = gameState.currentRecipe;

        // Show result screen
        gameState.container.innerHTML = `
            <div style="text-align:center;max-width:400px;">
                <div style="font-size:48px;margin-bottom:12px;
                    ${result.color === '#FFD700' ? 'animation:glow 1.5s infinite alternate;' : ''}">
                    ${result.icon}
                </div>
                <div style="font-size:20px;color:${result.color};font-weight:bold;margin-bottom:6px;">
                    ${result.name}
                </div>
                <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:20px;">
                    ${recipe.icon} ${recipe.name}
                </div>

                <!-- Phase Results -->
                <div style="display:flex;justify-content:center;gap:6px;margin-bottom:20px;">
                    ${gameState.phaseResults.map((r, i) => `
                        <div style="width:30px;height:30px;border-radius:50%;
                            background:${r.color}22;border:2px solid ${r.color};
                            display:flex;align-items:center;justify-content:center;
                            font-size:10px;color:${r.color};">
                            ${r === QUALITY_THRESHOLDS.perfect ? '\u2605' :
                              r === QUALITY_THRESHOLDS.good ? '\u2713' :
                              r === QUALITY_THRESHOLDS.normal ? '\u25CB' : '\u2717'}
                        </div>
                    `).join('')}
                </div>

                <!-- Stats -->
                <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:14px;
                    margin-bottom:20px;text-align:left;">
                    <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;">
                        <span style="color:rgba(255,255,255,0.4);">Score</span>
                        <span style="color:white;font-weight:bold;">${gameState.totalScore}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;">
                        <span style="color:rgba(255,255,255,0.4);">Max Combo</span>
                        <span style="color:#FF9800;">${Math.max(...gameState.phaseResults.map((_, i) => {
                            let c = 0; for (let j = 0; j <= i; j++) {
                                if (gameState.phaseResults[j] !== QUALITY_THRESHOLDS.fail) c++; else c = 0;
                            } return c;
                        }))}x</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;">
                        <span style="color:rgba(255,255,255,0.4);">Stat-Bonus</span>
                        <span style="color:${result.color};">+${result.bonus}%</span>
                    </div>
                </div>

                <div style="display:flex;gap:10px;justify-content:center;">
                    <button onclick="window.CraftingMinigame.start('${Object.keys(RECIPES).find(k => RECIPES[k] === recipe)}')"
                        style="padding:10px 20px;font-size:11px;font-family:inherit;
                        background:rgba(255,152,0,0.15);border:1px solid rgba(255,152,0,0.3);
                        color:#FF9800;border-radius:6px;cursor:pointer;">
                        \uD83D\uDD04 Nochmal
                    </button>
                    <button onclick="window.CraftingMinigame.showRecipes()"
                        style="padding:10px 20px;font-size:11px;font-family:inherit;
                        background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.2);
                        color:#4CAF50;border-radius:6px;cursor:pointer;">
                        \uD83D\uDCDA Rezepte
                    </button>
                    <button onclick="window.CraftingMinigame.close()"
                        style="padding:10px 20px;font-size:11px;font-family:inherit;
                        background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                        color:rgba(255,255,255,0.5);border-radius:6px;cursor:pointer;">
                        Schliessen
                    </button>
                </div>
            </div>
        `;

        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '\u2715 ESC';
        closeBtn.style.cssText = `
            position:absolute;top:16px;right:20px;background:rgba(244,67,54,0.15);
            border:1px solid rgba(244,67,54,0.3);color:#F44336;
            padding:6px 14px;border-radius:4px;cursor:pointer;
            font-family:inherit;font-size:10px;z-index:10;
        `;
        closeBtn.onclick = closeCraftingUI;
        gameState.container.appendChild(closeBtn);

        // Notification
        if (overallQuality !== 'fail' && window.QuestTrackerV2) {
            window.QuestTrackerV2.showNotification(
                'ITEM GECRAFTET',
                `${recipe.icon} ${recipe.name} (${result.name})`,
                result.color
            );
        }

        // Add to inventory
        if (overallQuality !== 'fail' && window.InventoryV2) {
            window.InventoryV2.addItem({
                id: recipe.name.toLowerCase().replace(/\s/g, '_') + '_' + Date.now(),
                name: recipe.name + (overallQuality === 'masterwork' ? ' [M]' : ''),
                type: recipe.result.type,
                rarity: overallQuality === 'masterwork' ? 'legendary' :
                       overallQuality === 'superior' ? 'epic' : recipe.rarity,
                icon: recipe.icon,
                stats: { ...recipe.result },
                value: Math.round(100 * (1 + result.bonus / 100)),
                weight: 2
            });
        }
    }

    // ==========================================
    // CSS
    // ==========================================

    const style = document.createElement('style');
    style.textContent = `
        @keyframes glow {
            from { text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700; }
            to { text-shadow: 0 0 40px #FFD700, 0 0 80px #FFD700; }
        }
    `;
    document.head.appendChild(style);

    // ==========================================
    // EXPORT
    // ==========================================

    window.CraftingMinigame = {
        RECIPES,
        open: openCraftingUI,
        close: closeCraftingUI,
        start: (recipeKey) => {
            if (!gameState.isOpen) openCraftingUI();
            startCrafting(recipeKey);
        },
        showRecipes: () => {
            if (gameState.container) {
                gameState.isPlaying = false;
                gameState.container.innerHTML = buildRecipeSelection();
                // Re-add close button
                const closeBtn = document.createElement('button');
                closeBtn.textContent = '\u2715 ESC';
                closeBtn.style.cssText = `
                    position:absolute;top:16px;right:20px;background:rgba(244,67,54,0.15);
                    border:1px solid rgba(244,67,54,0.3);color:#F44336;
                    padding:6px 14px;border-radius:4px;cursor:pointer;
                    font-family:inherit;font-size:10px;z-index:10;
                `;
                closeBtn.onclick = closeCraftingUI;
                gameState.container.appendChild(closeBtn);
            }
        },
        addRecipe: (key, recipe) => { RECIPES[key] = recipe; },
        isOpen: () => gameState.isOpen
    };

    console.log(`[OK] Crafting Minigame geladen: ${Object.keys(RECIPES).length} Rezepte, Timing-basiert`);

})();
