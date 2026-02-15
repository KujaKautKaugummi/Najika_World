/**
 * Skill Tree UI - Najika World
 * ==============================
 * Visueller Skill-Baum (Diablo/PoE Style) mit:
 * - Canvas-basierter Baum-Rendering
 * - 6 Magie-Schulen als Aeste
 * - Node-States: locked, available, learned, mastered
 * - Zoom + Pan auf dem Canvas
 * - Skill-Detail-Panel bei Click
 * - Skillpunkt-Vergabe
 * - Verbindungslinien mit Glow-Effekt
 *
 * Oeffnet sich ueber die skill_ui.js (T-Taste) oder direkt.
 * Ergaenzt skill_ui.js - ersetzt es nicht.
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // SKILL TREE DATA
    // ==========================================

    const SCHOOLS = {
        runen: {
            name: 'Runen-Magie',
            icon: '\uD83D\uDCDC',
            color: '#4A90D9',
            glow: 'rgba(74,144,217,0.4)',
            angle: 0, // position on the wheel
            skills: [
                { id: 'rune_bolt', name: 'Runen-Blitz', tier: 1, cost: 1, icon: '\uD83D\uDD35',
                  desc: 'Einfacher Runen-Projektil-Angriff', requires: [] },
                { id: 'rune_shield', name: 'Runen-Schild', tier: 1, cost: 1, icon: '\uD83D\uDEE1',
                  desc: 'Temporaerer Schutzschild aus Runen', requires: [] },
                { id: 'rune_trap', name: 'Runen-Falle', tier: 2, cost: 2, icon: '\uD83D\uDD37',
                  desc: 'Platziert eine explodierbare Rune', requires: ['rune_bolt'] },
                { id: 'rune_chain', name: 'Runen-Kette', tier: 2, cost: 2, icon: '\uD83D\uDD17',
                  desc: 'Kettenreaktion zwischen gesetzten Runen', requires: ['rune_trap'] },
                { id: 'rune_storm', name: 'Runen-Sturm', tier: 3, cost: 3, icon: '\uD83C\uDF00',
                  desc: 'Runen-Hagel ueber grosses Gebiet', requires: ['rune_chain', 'rune_shield'] },
                { id: 'rune_master', name: 'Runen-Meister', tier: 4, cost: 5, icon: '\u2728',
                  desc: 'Alle Runen-Kosten -50%, Cooldown -30%', requires: ['rune_storm'],
                  oneWay: true }
            ]
        },
        blitz: {
            name: 'Blitz-Magie',
            icon: '\u26A1',
            color: '#FFD700',
            glow: 'rgba(255,215,0,0.4)',
            angle: 60,
            skills: [
                { id: 'spark', name: 'Funke', tier: 1, cost: 1, icon: '\u26A1',
                  desc: 'Schneller Blitz-Angriff', requires: [] },
                { id: 'chain_lightning', name: 'Kettenblitz', tier: 1, cost: 1, icon: '\u26A1',
                  desc: 'Blitz springt zu Nachbar-Feinden', requires: [] },
                { id: 'thunder_clap', name: 'Donnerschlag', tier: 2, cost: 2, icon: '\uD83D\uDCA5',
                  desc: 'AoE Blitz um den Spieler', requires: ['spark'] },
                { id: 'lightning_dash', name: 'Blitz-Dash', tier: 2, cost: 2, icon: '\uD83D\uDCA8',
                  desc: 'Teleport als Blitz zum Ziel', requires: ['chain_lightning'] },
                { id: 'mjolnir', name: 'Mjolnir', tier: 3, cost: 3, icon: '\uD83D\uDD28',
                  desc: 'Beschwort einen Blitz-Hammer', requires: ['thunder_clap', 'lightning_dash'] },
                { id: 'storm_lord', name: 'Sturmherr', tier: 4, cost: 5, icon: '\uD83C\uDF29',
                  desc: 'Permanenter Blitz-Schild + AoE Damage', requires: ['mjolnir'],
                  oneWay: true }
            ]
        },
        natur: {
            name: 'Natur-Magie',
            icon: '\uD83C\uDF3F',
            color: '#4CAF50',
            glow: 'rgba(76,175,80,0.4)',
            angle: 120,
            skills: [
                { id: 'heal', name: 'Heilung', tier: 1, cost: 1, icon: '\uD83D\uDC9A',
                  desc: 'Heilt HP ueber Zeit', requires: [] },
                { id: 'vine_whip', name: 'Rankenpeitsche', tier: 1, cost: 1, icon: '\uD83C\uDF3F',
                  desc: 'Rankenangriff mit Slow-Effekt', requires: [] },
                { id: 'bark_skin', name: 'Rindenhaut', tier: 2, cost: 2, icon: '\uD83C\uDF33',
                  desc: '+30% Ruestung fuer 30 Sekunden', requires: ['heal'] },
                { id: 'entangle', name: 'Verstricken', tier: 2, cost: 2, icon: '\uD83E\uDEB4',
                  desc: 'Wurzeln halten Feinde fest', requires: ['vine_whip'] },
                { id: 'treant_summon', name: 'Baumwesen', tier: 3, cost: 3, icon: '\uD83C\uDF32',
                  desc: 'Beschwort einen Baum-Verteidiger', requires: ['bark_skin', 'entangle'] },
                { id: 'gaia_wrath', name: 'Gaias Zorn', tier: 4, cost: 5, icon: '\uD83C\uDF0D',
                  desc: 'Erdbeben + Dornen-Explosion im Radius', requires: ['treant_summon'],
                  oneWay: true }
            ]
        },
        feuer: {
            name: 'Feuer-Magie',
            icon: '\uD83D\uDD25',
            color: '#FF4444',
            glow: 'rgba(255,68,68,0.4)',
            angle: 180,
            skills: [
                { id: 'fireball', name: 'Feuerball', tier: 1, cost: 1, icon: '\uD83D\uDD25',
                  desc: 'Klassischer Feuerball-Angriff', requires: [] },
                { id: 'flame_wall', name: 'Flammenwand', tier: 1, cost: 1, icon: '\uD83D\uDD25',
                  desc: 'Wand aus Feuer blockt Feinde', requires: [] },
                { id: 'meteor_shower', name: 'Meteorregen', tier: 2, cost: 2, icon: '\u2604',
                  desc: 'Meteore fallen vom Himmel', requires: ['fireball'] },
                { id: 'inferno', name: 'Inferno', tier: 2, cost: 2, icon: '\uD83D\uDD25',
                  desc: 'Dauerfeuer in Kegelform', requires: ['flame_wall'] },
                { id: 'phoenix', name: 'Phönix', tier: 3, cost: 3, icon: '\uD83E\uDD85',
                  desc: 'Wiederbelebung bei Tod (1x pro Kampf)', requires: ['meteor_shower', 'inferno'] },
                { id: 'explosion_master', name: 'EXPLOSION!', tier: 4, cost: 5, icon: '\uD83D\uDCA5',
                  desc: 'Megumin-Style! Mega-Explosion, danach erschoepft', requires: ['phoenix'],
                  oneWay: true }
            ]
        },
        eis: {
            name: 'Frost-Magie',
            icon: '\u2744',
            color: '#ADD8E6',
            glow: 'rgba(173,216,230,0.4)',
            angle: 240,
            skills: [
                { id: 'ice_shard', name: 'Eissplitter', tier: 1, cost: 1, icon: '\u2744',
                  desc: 'Schneller Eis-Projektil', requires: [] },
                { id: 'frost_nova', name: 'Frost-Nova', tier: 1, cost: 1, icon: '\u2744',
                  desc: 'AoE Freeze um den Spieler', requires: [] },
                { id: 'blizzard', name: 'Blizzard', tier: 2, cost: 2, icon: '\uD83C\uDF28',
                  desc: 'Schneesturm verlangsamt alle', requires: ['ice_shard'] },
                { id: 'ice_armor', name: 'Eis-Ruestung', tier: 2, cost: 2, icon: '\uD83E\uDDE5',
                  desc: 'Eis-Schild absorbiert Schaden', requires: ['frost_nova'] },
                { id: 'absolute_zero', name: 'Absoluter Null', tier: 3, cost: 3, icon: '\uD83D\uDCA0',
                  desc: 'Friert alles im Radius ein', requires: ['blizzard', 'ice_armor'] },
                { id: 'frost_emperor', name: 'Frostkaiser', tier: 4, cost: 5, icon: '\uD83D\uDC51',
                  desc: 'Permanenter Frost-Aura + Eis-Elementar', requires: ['absolute_zero'],
                  oneWay: true }
            ]
        },
        schmiede: {
            name: 'Schmiedekunst',
            icon: '\uD83D\uDD28',
            color: '#FF9800',
            glow: 'rgba(255,152,0,0.4)',
            angle: 300,
            skills: [
                { id: 'repair', name: 'Reparieren', tier: 1, cost: 1, icon: '\uD83D\uDD27',
                  desc: 'Waffen/Ruestungen reparieren', requires: [] },
                { id: 'sharpen', name: 'Schaerfen', tier: 1, cost: 1, icon: '\u2694',
                  desc: '+15% Waffen-Schaden fuer 5 min', requires: [] },
                { id: 'enchant_weapon', name: 'Waffenverzauberung', tier: 2, cost: 2, icon: '\u2728',
                  desc: 'Element auf Waffe infusen', requires: ['sharpen'] },
                { id: 'armor_craft', name: 'Ruestungsschmied', tier: 2, cost: 2, icon: '\uD83D\uDEE1',
                  desc: 'Bessere Ruestungen herstellen', requires: ['repair'] },
                { id: 'legendary_forge', name: 'Legendaere Schmiede', tier: 3, cost: 3, icon: '\uD83D\uDD25',
                  desc: 'Chance auf legendaere Items', requires: ['enchant_weapon', 'armor_craft'] },
                { id: 'divine_smith', name: 'Goetterschmied', tier: 4, cost: 5, icon: '\u2B50',
                  desc: 'Kann goettliche Waffen schmieden', requires: ['legendary_forge'],
                  oneWay: true }
            ]
        }
    };

    // ==========================================
    // STATE
    // ==========================================

    let treeState = {
        isOpen: false,
        canvas: null,
        ctx: null,
        container: null,
        // Camera
        offsetX: 0,
        offsetY: 0,
        zoom: 1,
        isDragging: false,
        dragStart: { x: 0, y: 0 },
        // Player
        skillPoints: 10,
        learnedSkills: new Set(),
        selectedSkill: null,
        selectedSchool: null,
        // Node positions (calculated)
        nodePositions: {}
    };

    // Load state
    try {
        const saved = JSON.parse(localStorage.getItem('najika_skill_tree'));
        if (saved) {
            treeState.learnedSkills = new Set(saved.learnedSkills || []);
            treeState.skillPoints = saved.skillPoints ?? 10;
        }
    } catch(e) { /* default */ }

    function saveState() {
        try {
            localStorage.setItem('najika_skill_tree', JSON.stringify({
                learnedSkills: [...treeState.learnedSkills],
                skillPoints: treeState.skillPoints
            }));
        } catch(e) { /* silent */ }
    }

    // ==========================================
    // LAYOUT CALCULATION
    // ==========================================

    const NODE_RADIUS = 24;
    const TIER_SPACING = 100;
    const BRANCH_SPREAD = 80;
    const CENTER_X = 0;
    const CENTER_Y = 0;

    function calculateNodePositions() {
        treeState.nodePositions = {};

        Object.entries(SCHOOLS).forEach(([schoolKey, school]) => {
            const angleRad = (school.angle - 90) * Math.PI / 180;
            const dirX = Math.cos(angleRad);
            const dirY = Math.sin(angleRad);

            // Perpendicular for branching
            const perpX = -dirY;
            const perpY = dirX;

            school.skills.forEach((skill, idx) => {
                const tierDist = skill.tier * TIER_SPACING + 60;
                // Spread within tier
                const sametier = school.skills.filter(s => s.tier === skill.tier);
                const tierIdx = sameTimer(samerier, skill);
                const tierCount = samerier.length;
                const spread = (tierIdx - (tierCount - 1) / 2) * BRANCH_SPREAD;

                treeState.nodePositions[skill.id] = {
                    x: CENTER_X + dirX * tierDist + perpX * spread,
                    y: CENTER_Y + dirY * tierDist + perpY * spread,
                    school: schoolKey,
                    skill: skill
                };
            });
        });
    }

    // Helper: find index of skill among same-tier skills
    function sameTimer(arr, skill) {
        const sameTier = arr.filter(s => s.tier === skill.tier);
        return sameTier.indexOf(skill);
    }

    function samerier(school, skill) {
        return school.filter(s => s.tier === skill.tier);
    }

    // Simplified positioning
    function getNodePosition(schoolKey, skill) {
        const school = SCHOOLS[schoolKey];
        const angleRad = (school.angle - 90) * Math.PI / 180;
        const dirX = Math.cos(angleRad);
        const dirY = Math.sin(angleRad);
        const perpX = -dirY;
        const perpY = dirX;

        const tierDist = skill.tier * TIER_SPACING + 60;
        const sameT = school.skills.filter(s => s.tier === skill.tier);
        const idx = sameT.indexOf(skill);
        const spread = (idx - (sameT.length - 1) / 2) * BRANCH_SPREAD;

        return {
            x: CENTER_X + dirX * tierDist + perpX * spread,
            y: CENTER_Y + dirY * tierDist + perpY * spread
        };
    }

    // ==========================================
    // CANVAS RENDERING
    // ==========================================

    function render() {
        const { canvas, ctx } = treeState;
        if (!canvas || !ctx) return;

        const w = canvas.width;
        const h = canvas.height;
        const cx = w / 2 + treeState.offsetX;
        const cy = h / 2 + treeState.offsetY;
        const zoom = treeState.zoom;

        // Clear
        ctx.fillStyle = '#080810';
        ctx.fillRect(0, 0, w, h);

        // Background radial pattern
        const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 400 * zoom);
        grad.addColorStop(0, 'rgba(40,40,60,0.3)');
        grad.addColorStop(1, 'rgba(8,8,16,0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        // Draw center node
        ctx.beginPath();
        ctx.arc(cx, cy, 30 * zoom, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,215,0,0.15)';
        ctx.fill();
        ctx.strokeStyle = '#FFD700';
        ctx.lineWidth = 2 * zoom;
        ctx.stroke();

        ctx.font = `${14 * zoom}px monospace`;
        ctx.fillStyle = '#FFD700';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('NAJIKA', cx, cy - 6 * zoom);
        ctx.font = `${8 * zoom}px monospace`;
        ctx.fillText('Skill Tree', cx, cy + 8 * zoom);

        // Draw each school
        Object.entries(SCHOOLS).forEach(([schoolKey, school]) => {
            // School label on the outer edge
            const angleRad = (school.angle - 90) * Math.PI / 180;
            const labelDist = (4.5 * TIER_SPACING + 80) * zoom;
            const lx = cx + Math.cos(angleRad) * labelDist;
            const ly = cy + Math.sin(angleRad) * labelDist;

            ctx.font = `bold ${11 * zoom}px monospace`;
            ctx.fillStyle = school.color;
            ctx.textAlign = 'center';
            ctx.fillText(`${school.icon} ${school.name}`, lx, ly);

            // Draw connections first (below nodes)
            school.skills.forEach(skill => {
                const pos = getNodePosition(schoolKey, skill);
                const sx = cx + pos.x * zoom;
                const sy = cy + pos.y * zoom;

                // Connection from center to tier 1
                if (skill.tier === 1) {
                    drawConnection(ctx, cx, cy, sx, sy, school.color, zoom,
                        treeState.learnedSkills.has(skill.id));
                }

                // Connections to requirements
                skill.requires.forEach(reqId => {
                    const reqSkill = school.skills.find(s => s.id === reqId);
                    if (reqSkill) {
                        const rpos = getNodePosition(schoolKey, reqSkill);
                        const rx = cx + rpos.x * zoom;
                        const ry = cy + rpos.y * zoom;
                        const bothLearned = treeState.learnedSkills.has(skill.id) &&
                                           treeState.learnedSkills.has(reqId);
                        drawConnection(ctx, rx, ry, sx, sy, school.color, zoom, bothLearned);
                    }
                });
            });

            // Draw nodes
            school.skills.forEach(skill => {
                const pos = getNodePosition(schoolKey, skill);
                const sx = cx + pos.x * zoom;
                const sy = cy + pos.y * zoom;

                const state = getSkillState(schoolKey, skill);
                drawSkillNode(ctx, sx, sy, skill, state, school, zoom);
            });
        });

        // Draw UI overlay (skill points)
        drawUIOverlay(ctx, w, h);
    }

    function drawConnection(ctx, x1, y1, x2, y2, color, zoom, isActive) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);

        if (isActive) {
            ctx.strokeStyle = color;
            ctx.lineWidth = 2.5 * zoom;
            ctx.globalAlpha = 0.8;
        } else {
            ctx.strokeStyle = 'rgba(255,255,255,0.08)';
            ctx.lineWidth = 1.5 * zoom;
            ctx.globalAlpha = 0.5;
        }
        ctx.stroke();
        ctx.globalAlpha = 1;

        // Glow for active
        if (isActive) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = color;
            ctx.lineWidth = 6 * zoom;
            ctx.globalAlpha = 0.1;
            ctx.stroke();
            ctx.globalAlpha = 1;
        }
    }

    function drawSkillNode(ctx, x, y, skill, state, school, zoom) {
        const r = NODE_RADIUS * zoom;
        const isSelected = treeState.selectedSkill === skill.id;

        // Glow for available/learned
        if (state === 'learned' || state === 'mastered') {
            ctx.beginPath();
            ctx.arc(x, y, r + 8 * zoom, 0, Math.PI * 2);
            ctx.fillStyle = school.glow;
            ctx.globalAlpha = 0.3;
            ctx.fill();
            ctx.globalAlpha = 1;
        }

        // Node circle
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);

        switch(state) {
            case 'locked':
                ctx.fillStyle = 'rgba(20,20,30,0.9)';
                ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                break;
            case 'available':
                ctx.fillStyle = 'rgba(30,30,50,0.9)';
                ctx.strokeStyle = school.color;
                break;
            case 'learned':
                ctx.fillStyle = `${school.color}33`;
                ctx.strokeStyle = school.color;
                break;
            case 'mastered':
                ctx.fillStyle = `${school.color}55`;
                ctx.strokeStyle = '#FFD700';
                break;
        }

        ctx.lineWidth = (isSelected ? 3 : 2) * zoom;
        ctx.fill();
        ctx.stroke();

        // Selection ring
        if (isSelected) {
            ctx.beginPath();
            ctx.arc(x, y, r + 4 * zoom, 0, Math.PI * 2);
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 1 * zoom;
            ctx.setLineDash([4 * zoom, 4 * zoom]);
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // Icon
        ctx.font = `${16 * zoom}px serif`;
        ctx.fillStyle = state === 'locked' ? 'rgba(255,255,255,0.2)' : 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(skill.icon, x, y - 2 * zoom);

        // Name (small, below)
        ctx.font = `${7 * zoom}px monospace`;
        ctx.fillStyle = state === 'locked' ? 'rgba(255,255,255,0.15)' :
                        state === 'learned' || state === 'mastered' ? school.color : 'rgba(255,255,255,0.5)';
        ctx.fillText(skill.name, x, y + r + 10 * zoom);

        // Cost badge (top-right)
        if (state !== 'learned' && state !== 'mastered') {
            const bx = x + r * 0.65;
            const by = y - r * 0.65;
            ctx.beginPath();
            ctx.arc(bx, by, 8 * zoom, 0, Math.PI * 2);
            ctx.fillStyle = state === 'available' && treeState.skillPoints >= skill.cost ?
                'rgba(76,175,80,0.8)' : 'rgba(80,80,80,0.8)';
            ctx.fill();
            ctx.font = `bold ${7 * zoom}px monospace`;
            ctx.fillStyle = 'white';
            ctx.fillText(skill.cost, bx, by + 1);
        }

        // One-way warning
        if (skill.oneWay) {
            ctx.font = `${6 * zoom}px monospace`;
            ctx.fillStyle = '#FF4444';
            ctx.fillText('1-WEG', x, y + r + 20 * zoom);
        }
    }

    function drawUIOverlay(ctx, w, h) {
        // Skill Points display
        ctx.fillStyle = 'rgba(10,10,30,0.9)';
        ctx.fillRect(w / 2 - 80, 10, 160, 36);
        ctx.strokeStyle = 'rgba(76,175,80,0.3)';
        ctx.lineWidth = 1;
        ctx.strokeRect(w / 2 - 80, 10, 160, 36);

        ctx.font = 'bold 11px monospace';
        ctx.fillStyle = treeState.skillPoints > 0 ? '#4CAF50' : 'rgba(255,255,255,0.4)';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`\u2B50 ${treeState.skillPoints} Skillpunkte`, w / 2, 28);

        // Legend (bottom-left)
        const legend = [
            { color: 'rgba(255,255,255,0.1)', label: 'Gesperrt' },
            { color: '#4A90D9', label: 'Verfuegbar' },
            { color: '#4CAF50', label: 'Gelernt' },
            { color: '#FFD700', label: 'Gemeistert' }
        ];
        legend.forEach((item, i) => {
            const ly = h - 80 + i * 16;
            ctx.beginPath();
            ctx.arc(20, ly, 5, 0, Math.PI * 2);
            ctx.fillStyle = item.color;
            ctx.fill();
            ctx.font = '9px monospace';
            ctx.fillStyle = 'rgba(255,255,255,0.5)';
            ctx.textAlign = 'left';
            ctx.fillText(item.label, 32, ly + 3);
        });

        // Controls hint (bottom-right)
        ctx.font = '9px monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.textAlign = 'right';
        ctx.fillText('Maus: Ziehen | Scroll: Zoom | Click: Waehlen', w - 16, h - 16);
    }

    // ==========================================
    // SKILL STATE LOGIC
    // ==========================================

    function getSkillState(schoolKey, skill) {
        if (treeState.learnedSkills.has(skill.id)) {
            return skill.oneWay ? 'mastered' : 'learned';
        }

        // Check requirements
        const allReqsMet = skill.requires.every(reqId => treeState.learnedSkills.has(reqId));
        if (!allReqsMet && skill.requires.length > 0) return 'locked';

        // Tier 1 skills are always available
        if (skill.tier === 1) return 'available';

        return allReqsMet ? 'available' : 'locked';
    }

    function learnSkill(schoolKey, skill) {
        if (treeState.learnedSkills.has(skill.id)) return false;

        const state = getSkillState(schoolKey, skill);
        if (state !== 'available') return false;
        if (treeState.skillPoints < skill.cost) return false;

        treeState.skillPoints -= skill.cost;
        treeState.learnedSkills.add(skill.id);
        saveState();

        // Notify
        if (window.QuestTrackerV2) {
            window.QuestTrackerV2.showNotification(
                'SKILL GELERNT',
                `${skill.icon} ${skill.name}`,
                SCHOOLS[schoolKey].color
            );
        }

        return true;
    }

    // ==========================================
    // INTERACTION
    // ==========================================

    function setupInteraction(canvas) {
        // Pan
        canvas.addEventListener('mousedown', (e) => {
            if (e.button === 0) {
                treeState.isDragging = true;
                treeState.dragStart = { x: e.clientX, y: e.clientY };
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (treeState.isDragging) {
                treeState.offsetX += e.clientX - treeState.dragStart.x;
                treeState.offsetY += e.clientY - treeState.dragStart.y;
                treeState.dragStart = { x: e.clientX, y: e.clientY };
                render();
            }
        });

        canvas.addEventListener('mouseup', () => { treeState.isDragging = false; });

        // Zoom
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const oldZoom = treeState.zoom;
            treeState.zoom = Math.max(0.4, Math.min(2.5, treeState.zoom - e.deltaY * 0.001));
            // Adjust offset to zoom toward mouse
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left - canvas.width / 2;
            const my = e.clientY - rect.top - canvas.height / 2;
            treeState.offsetX += mx * (1 - treeState.zoom / oldZoom);
            treeState.offsetY += my * (1 - treeState.zoom / oldZoom);
            render();
        });

        // Click: select node
        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;
            const cx = canvas.width / 2 + treeState.offsetX;
            const cy = canvas.height / 2 + treeState.offsetY;
            const zoom = treeState.zoom;

            let clicked = null;

            Object.entries(SCHOOLS).forEach(([schoolKey, school]) => {
                school.skills.forEach(skill => {
                    const pos = getNodePosition(schoolKey, skill);
                    const sx = cx + pos.x * zoom;
                    const sy = cy + pos.y * zoom;
                    const dist = Math.sqrt((mx - sx) ** 2 + (my - sy) ** 2);
                    if (dist < NODE_RADIUS * zoom) {
                        clicked = { schoolKey, skill };
                    }
                });
            });

            if (clicked) {
                treeState.selectedSkill = clicked.skill.id;
                treeState.selectedSchool = clicked.schoolKey;
                showSkillDetail(clicked.schoolKey, clicked.skill);
            } else {
                treeState.selectedSkill = null;
                treeState.selectedSchool = null;
                hideSkillDetail();
            }
            render();
        });
    }

    // ==========================================
    // SKILL DETAIL PANEL
    // ==========================================

    function showSkillDetail(schoolKey, skill) {
        const existing = document.getElementById('skill-detail-panel');
        if (existing) existing.remove();

        const school = SCHOOLS[schoolKey];
        const state = getSkillState(schoolKey, skill);
        const canLearn = state === 'available' && treeState.skillPoints >= skill.cost;

        const panel = document.createElement('div');
        panel.id = 'skill-detail-panel';
        panel.style.cssText = `
            position:absolute;bottom:20px;right:20px;
            background:linear-gradient(135deg, rgba(10,10,30,0.95), rgba(5,5,15,0.98));
            border:2px solid ${school.color};
            border-radius:12px;padding:18px;color:white;
            font-family:'Courier New',monospace;
            width:280px;
            box-shadow:0 8px 32px rgba(0,0,0,0.8);
        `;

        panel.innerHTML = `
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                <span style="font-size:28px;">${skill.icon}</span>
                <div>
                    <div style="font-size:13px;font-weight:bold;">${skill.name}</div>
                    <div style="font-size:9px;color:${school.color};">${school.name} | Tier ${skill.tier}</div>
                </div>
            </div>

            <div style="font-size:10px;color:rgba(255,255,255,0.6);line-height:1.5;
                margin-bottom:12px;">${skill.desc}</div>

            <div style="display:flex;gap:8px;margin-bottom:12px;">
                <span style="font-size:9px;padding:3px 8px;background:rgba(255,255,255,0.06);
                    border-radius:4px;color:rgba(255,255,255,0.5);">Kosten: ${skill.cost} SP</span>
                ${skill.oneWay ? `<span style="font-size:9px;padding:3px 8px;
                    background:rgba(255,68,68,0.1);border:1px solid rgba(255,68,68,0.3);
                    border-radius:4px;color:#FF4444;">1-WEG SKILL</span>` : ''}
            </div>

            ${skill.requires.length > 0 ? `
                <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-bottom:4px;">
                    Voraussetzungen:</div>
                <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:12px;">
                    ${skill.requires.map(reqId => {
                        const reqSkill = school.skills.find(s => s.id === reqId);
                        const hasReq = treeState.learnedSkills.has(reqId);
                        return `<span style="font-size:9px;padding:2px 6px;
                            background:${hasReq ? 'rgba(76,175,80,0.1)' : 'rgba(255,68,68,0.1)'};
                            border:1px solid ${hasReq ? 'rgba(76,175,80,0.3)' : 'rgba(255,68,68,0.3)'};
                            border-radius:3px;color:${hasReq ? '#4CAF50' : '#FF4444'};">
                            ${hasReq ? '\u2713' : '\u2717'} ${reqSkill ? reqSkill.name : reqId}
                        </span>`;
                    }).join('')}
                </div>
            ` : ''}

            <div style="font-size:10px;padding:6px 10px;border-radius:4px;text-align:center;
                background:${state === 'learned' || state === 'mastered' ?
                    'rgba(76,175,80,0.1)' : 'rgba(255,255,255,0.03)'};
                color:${state === 'learned' || state === 'mastered' ? '#4CAF50' : 'rgba(255,255,255,0.3)'};
                border:1px solid ${state === 'learned' || state === 'mastered' ?
                    'rgba(76,175,80,0.3)' : 'rgba(255,255,255,0.06)'};
                margin-bottom:8px;">
                ${state === 'learned' ? '\u2713 Gelernt' :
                  state === 'mastered' ? '\u2B50 Gemeistert' :
                  state === 'locked' ? '\uD83D\uDD12 Gesperrt' :
                  `Verfuegbar (${skill.cost} SP)`}
            </div>

            ${canLearn ? `
                <button onclick="window.SkillTreeUI.learn('${schoolKey}','${skill.id}')"
                    style="width:100%;padding:8px;font-size:11px;font-family:inherit;
                    background:rgba(76,175,80,0.2);border:1px solid rgba(76,175,80,0.4);
                    color:#4CAF50;border-radius:6px;cursor:pointer;font-weight:bold;">
                    \u2B50 Skill lernen (${skill.cost} SP)
                </button>
            ` : ''}

            ${skill.oneWay && canLearn ? `
                <div style="font-size:8px;color:#FF4444;text-align:center;margin-top:6px;">
                    \u26A0 1-Weg: Kann nicht rueckgaengig gemacht werden!</div>
            ` : ''}
        `;

        const container = document.getElementById('skill-tree-container');
        if (container) container.appendChild(panel);
    }

    function hideSkillDetail() {
        const el = document.getElementById('skill-detail-panel');
        if (el) el.remove();
    }

    // ==========================================
    // OPEN / CLOSE
    // ==========================================

    function openTree() {
        if (treeState.isOpen) { closeTree(); return; }
        treeState.isOpen = true;

        const container = document.createElement('div');
        container.id = 'skill-tree-container';
        container.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.98);z-index:9500;
        `;

        // Canvas
        const canvas = document.createElement('canvas');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        canvas.style.cssText = 'width:100%;height:100%;display:block;';
        container.appendChild(canvas);

        treeState.canvas = canvas;
        treeState.ctx = canvas.getContext('2d');
        treeState.container = container;
        treeState.offsetX = 0;
        treeState.offsetY = 0;
        treeState.zoom = 1;

        // Controls
        const controls = document.createElement('div');
        controls.style.cssText = `
            position:absolute;top:10px;left:10px;z-index:10;display:flex;gap:8px;
        `;
        controls.innerHTML = `
            <button onclick="window.SkillTreeUI.close()"
                style="padding:6px 14px;font-size:10px;font-family:'Courier New',monospace;
                background:rgba(244,67,54,0.2);border:1px solid rgba(244,67,54,0.3);
                color:#F44336;border-radius:4px;cursor:pointer;">ESC Schliessen</button>
            <button onclick="window.SkillTreeUI.resetView()"
                style="padding:6px 14px;font-size:10px;font-family:'Courier New',monospace;
                background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.2);
                color:#4CAF50;border-radius:4px;cursor:pointer;">Zentrieren</button>
        `;
        container.appendChild(controls);

        document.body.appendChild(container);

        setupInteraction(canvas);
        render();

        // ESC handler
        treeState._escHandler = (e) => {
            if (e.key === 'Escape') closeTree();
        };
        document.addEventListener('keydown', treeState._escHandler);
    }

    function closeTree() {
        treeState.isOpen = false;
        treeState.selectedSkill = null;
        treeState.canvas = null;
        treeState.ctx = null;

        const container = document.getElementById('skill-tree-container');
        if (container) container.remove();

        if (treeState._escHandler) {
            document.removeEventListener('keydown', treeState._escHandler);
        }
    }

    // Keyboard: T = Skill Tree
    document.addEventListener('keydown', (e) => {
        if (e.key === 't' || e.key === 'T') {
            if (document.activeElement.tagName === 'INPUT' ||
                document.activeElement.tagName === 'TEXTAREA') return;
            const chatUI = document.getElementById('chat-ui');
            if (chatUI && chatUI.style.display !== 'none') return;

            if (treeState.isOpen) {
                closeTree();
            } else {
                openTree();
            }
        }
    });

    // ==========================================
    // EXPORT
    // ==========================================

    window.SkillTreeUI = {
        SCHOOLS,
        open: openTree,
        close: closeTree,
        resetView: () => {
            treeState.offsetX = 0;
            treeState.offsetY = 0;
            treeState.zoom = 1;
            render();
        },
        learn: (schoolKey, skillId) => {
            const school = SCHOOLS[schoolKey];
            if (!school) return;
            const skill = school.skills.find(s => s.id === skillId);
            if (!skill) return;
            if (learnSkill(schoolKey, skill)) {
                showSkillDetail(schoolKey, skill);
                render();
            }
        },
        getLearnedSkills: () => [...treeState.learnedSkills],
        getSkillPoints: () => treeState.skillPoints,
        addSkillPoints: (n) => { treeState.skillPoints += n; saveState(); },
        isOpen: () => treeState.isOpen
    };

    console.log(`[OK] Skill Tree UI geladen: ${Object.keys(SCHOOLS).length} Schulen, ${
        Object.values(SCHOOLS).reduce((sum, s) => sum + s.skills.length, 0)} Skills`);

})();
