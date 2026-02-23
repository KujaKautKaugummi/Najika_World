/**
 * NAJIKA DEATH SYSTEM - Oregon Trail
 * =====================================
 * ALLES verloren beim Tod. Kompletter Neustart.
 * Items + Gold + Ausruestung + Wagen → Leichenhaufen in der Welt.
 * Sklaven fliehen. Rekrutierte: Loyalty-Check.
 *
 * "Der Tod ist ein staendiger Begleiter in dieser Welt.
 *  Aber deine Habseligkeiten warten an deinem Grab..." - Konosuba-Vibes
 */
(function() {
    'use strict';

    let initialized = false;

    // ==========================================
    // MAIN DEATH HANDLER
    // ==========================================

    function handleOregonTrailDeath(source) {
        console.log('[DEATH] Oregon Trail Tod ausgeloest! Ursache:', source);

        // 1. Capture death position
        const playerPos = window.Scene3D?.characterGroup?.position;
        const deathPosition = playerPos
            ? { x: playerPos.x, y: playerPos.y || 0, z: playerPos.z }
            : { x: 4800, y: 0, z: 4800 };

        const deathRegion = window.RegionStreamingV2?.getCurrentRegion?.()
            || window.BiomeSystem?.getCurrentBiome?.()
            || 'Unbekannt';

        // 2. Collect ALL player possessions
        const inv = window.InventoryV2;
        const allItems = inv?.getItems?.() || [];
        const equipped = inv?.getEquipped?.() || {};
        const gold = inv?.getGold?.() || 0;

        // 3. Active wagon + contents
        const activeWagon = window.WagonSystem?.getActiveWagon?.();
        const wagonItems = activeWagon?.items || [];
        const wagonPosition = activeWagon
            ? { ...activeWagon.position }
            : null;

        // 4. Create corpse pile with ALL possessions
        const totalItems = [...allItems];
        // Add equipped items
        Object.values(equipped).forEach(eq => {
            if (eq) totalItems.push(eq);
        });
        // Add wagon items
        wagonItems.forEach(wi => totalItems.push(wi));

        if (window.WorldItems?.createCorpsePile && totalItems.length > 0) {
            window.WorldItems.createCorpsePile(
                totalItems,
                gold,
                {}, // Equipment already merged into totalItems
                deathPosition,
                deathRegion
            );
        }

        // 5. Wagon wreck (separate from corpse pile)
        if (activeWagon && window.WagonSystem?.abandonAllWagons) {
            window.WagonSystem.abandonAllWagons();
        }

        // 6. Clear player inventory
        if (inv?.clearAll) {
            inv.clearAll();
        }

        // 7. Process creatures
        let creatureReport = { stayed: [], fled: [], escaped: [] };
        if (window.CreatureRecruit?.scatterOnDeath) {
            creatureReport = window.CreatureRecruit.scatterOnDeath();
        }

        // 8. Stop player work
        if (window.WorkerSystem?.playerStopWork) {
            window.WorkerSystem.playerStopWork();
        }

        // 9. Show death screen
        showOregonTrailDeathScreen(source, totalItems, gold, creatureReport, deathRegion);

        // 10. Emit event
        if (window.GameEvents) {
            window.GameEvents.emit('playerDied', {
                source,
                position: deathPosition,
                region: deathRegion,
                itemsLost: totalItems.length,
                goldLost: gold,
                creatureReport,
            });
        }

        console.log(`[DEATH] Verloren: ${totalItems.length} Items, ${gold}G, ${creatureReport.escaped.length} Sklaven geflohen`);
    }

    // ==========================================
    // DEATH SCREEN
    // ==========================================

    function showOregonTrailDeathScreen(source, lostItems, lostGold, creatureReport, region) {
        // Remove existing
        const existing = document.getElementById('death-screen-overlay');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'death-screen-overlay';
        overlay.style.cssText = `
            position:fixed; top:0; left:0; width:100%; height:100%;
            background:rgba(0,0,0,0); z-index:99999;
            display:flex; flex-direction:column; justify-content:center; align-items:center;
            font-family:'Courier New',monospace; color:#e0e0e0;
            transition:background 2s;
        `;

        // Fade in
        requestAnimationFrame(() => {
            overlay.style.background = 'rgba(10,0,0,0.97)';
        });

        // Source names
        const sourceNames = {
            hunger: 'Verhungert',
            thirst: 'Verdurstet',
            combat: 'Im Kampf gefallen',
            volcano: 'Vulkanische Hitze',
            lightning: 'Blitzschlag',
            ambush: 'Hinterhalt im Schlaf',
            disease: 'Krankheit',
            fall: 'Sturz in die Tiefe',
        };
        const causeName = sourceNames[source] || source || 'Unbekannte Ursache';

        // Build creature report HTML
        let creatureHtml = '';
        if (creatureReport.stayed.length > 0) {
            creatureHtml += `<div style="color:#4CAF50;font-size:11px;margin-top:8px;">
                Treu geblieben: ${creatureReport.stayed.join(', ')}</div>`;
        }
        if (creatureReport.fled.length > 0) {
            creatureHtml += `<div style="color:#FF9800;font-size:11px;margin-top:4px;">
                Geflohen: ${creatureReport.fled.join(', ')}</div>`;
        }
        if (creatureReport.escaped.length > 0) {
            creatureHtml += `<div style="color:#F44336;font-size:11px;margin-top:4px;">
                Sklaven entkommen: ${creatureReport.escaped.join(', ')}</div>`;
        }

        // Content (appears with delay)
        const content = document.createElement('div');
        content.style.cssText = `
            text-align:center; opacity:0; transition:opacity 1.5s;
            max-width:500px;
        `;
        content.innerHTML = `
            <div style="font-size:48px; margin-bottom:20px; color:#F44336;">☠️</div>

            <div style="font-size:28px; color:#F44336; font-weight:bold;
                letter-spacing:4px; margin-bottom:8px;">
                DU BIST GESTORBEN
            </div>

            <div style="font-size:16px; color:#FF6B6B; margin-bottom:30px;">
                ${causeName}
            </div>

            <div style="background:rgba(244,67,54,0.1); border:1px solid rgba(244,67,54,0.3);
                border-radius:10px; padding:20px; margin-bottom:20px;">

                <div style="font-size:20px; color:#F44336; font-weight:bold; margin-bottom:15px;
                    letter-spacing:2px;">
                    ALLES VERLOREN
                </div>

                <div style="display:flex; justify-content:center; gap:30px; margin-bottom:15px;">
                    <div>
                        <div style="font-size:24px; color:#FF9800;">${lostItems.length}</div>
                        <div style="font-size:10px; color:#888;">Items</div>
                    </div>
                    <div>
                        <div style="font-size:24px; color:#FFD700;">${lostGold}</div>
                        <div style="font-size:10px; color:#888;">Gold</div>
                    </div>
                </div>

                ${creatureHtml}
            </div>

            <div style="font-size:12px; color:#888; margin-bottom:25px;">
                Deine Habseligkeiten liegen bei
                <span style="color:#FF9800; font-weight:bold;">${region}</span>
            </div>

            <div style="font-size:10px; color:#555; margin-bottom:25px; font-style:italic;">
                "In dieser Welt beginnt jeder Tag als waere es der letzte..."
            </div>
        `;

        // Respawn button (appears after 3s)
        const btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'opacity:0; transition:opacity 1s;';
        btnContainer.innerHTML = `
            <button id="death-respawn-btn" style="
                padding:14px 40px; font-size:14px; font-family:inherit;
                background:rgba(244,67,54,0.2); border:2px solid #F44336;
                color:#F44336; border-radius:8px; cursor:pointer;
                letter-spacing:2px; font-weight:bold;
                transition:all 0.3s;
            " onmouseover="this.style.background='rgba(244,67,54,0.4)'"
               onmouseout="this.style.background='rgba(244,67,54,0.2)'">
                VON VORN BEGINNEN
            </button>
        `;

        content.appendChild(btnContainer);
        overlay.appendChild(content);
        document.body.appendChild(overlay);

        // Animations
        setTimeout(() => { content.style.opacity = '1'; }, 500);
        setTimeout(() => { btnContainer.style.opacity = '1'; }, 3000);

        // Respawn handler
        const respawnBtn = btnContainer.querySelector('#death-respawn-btn');
        respawnBtn.addEventListener('click', () => {
            respawnPlayer();
            overlay.style.opacity = '0';
            overlay.style.transition = 'opacity 1s';
            setTimeout(() => overlay.remove(), 1000);
        });
    }

    // ==========================================
    // RESPAWN
    // ==========================================

    function respawnPlayer() {
        // Reset HP
        if (window.SurvivalSystem) {
            const ss = window.SurvivalSystem;
            if (ss.setState) {
                ss.setState({
                    hp: 50,
                    hunger: 40,
                    thirst: 40,
                    energy: 30,
                });
            } else {
                // Fallback: direct state access
                if (ss.state) {
                    ss.state.hp = 50;
                    ss.state.hunger = 40;
                    ss.state.thirst = 40;
                    ss.state.energy = 30;
                }
            }

            // Clear fatal injuries
            if (ss.clearInjuries) ss.clearInjuries();

            // Mood penalty
            if (ss.addMoodlet) {
                ss.addMoodlet('lost_everything', 'Alles verloren...', -30, 3600000);
            }
        }

        // Teleport to Schwarze Muehle
        if (window.TeleporterSystem?.teleportTo) {
            window.TeleporterSystem.teleportTo('schwarze_muehle');
        } else {
            // Fallback: move character directly
            const charGroup = window.Scene3D?.characterGroup;
            if (charGroup) {
                charGroup.position.set(4800, 0, 4800);
            }
        }

        console.log('[DEATH] Respawn an Schwarze Muehle - komplett nackt');

        if (window.QuestTrackerV2?.showNotification) {
            window.QuestTrackerV2.showNotification(
                'NEUANFANG',
                'Du bist an der Schwarzen Muehle aufgewacht. Ohne alles.',
                '#888'
            );
        }
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        if (initialized) return;
        initialized = true;

        // Override survival system death handler
        const ss = window.SurvivalSystem;
        if (ss && ss.handleDeath) {
            const originalHandleDeath = ss.handleDeath;
            ss.handleDeath = function(source) {
                handleOregonTrailDeath(source);
            };
            console.log('[DEATH] SurvivalSystem.handleDeath ueberschrieben (Oregon Trail)');
        }

        console.log('[OK] DeathSystem geladen (Oregon Trail Modus)');
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.DeathSystem = {
        init,
        handleOregonTrailDeath,
        respawnPlayer,
    };

    console.log('[OK] DeathSystem geladen');
})();
