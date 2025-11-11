/**
 * NAJIKA WORLD - SPEZIAL-FEATURES
 * =================================
 *
 * Spezial-Features für besondere Orte:
 * - Arena (Handelsfestung) - PvP Modi
 * - Player Shops (Handelsfestung) - Fallout 76 Style
 * - Onsen (Dampf-Hain) - Healing Zones
 * - Leuchtturm (Salzige Bucht) - Klettbar mit Aussicht
 */

class SpecialFeatures {
    constructor(scene, THREE, inventorySystem = null, foodSystem = null) {
        this.scene = scene;
        this.THREE = THREE;
        this.inventorySystem = inventorySystem;
        this.foodSystem = foodSystem;

        // Onsen State
        this.inOnsen = false;
        this.currentOnsenBonus = 0;
        this.onsenHealInterval = null;

        // Leuchtturm State
        this.isClimbing = false;
        this.lighthouseHeight = 0;
        this.lighthouseMaxHeight = 30;

        // Arena State
        this.inArena = false;
        this.arenaMode = null; // 'hardcore', 'normal', 'softy'

        console.log('✨ Spezial-Features System initialisiert');
    }

    // ===== ARENA SYSTEM (Handelsfestung) =====

    showArenaModeSelection() {
        const modes = {
            hardcore: {
                name: 'Hardcore Mode',
                description: 'Items können permanent verloren gehen! Höchstes Risiko, höchste Belohnungen.',
                icon: '💀',
                color: '#ff0000'
            },
            normal: {
                name: 'Normal Mode',
                description: 'Normale Arena-Regeln. Moderates Risiko, gute Belohnungen.',
                icon: '⚔️',
                color: '#ffaa00'
            },
            softy: {
                name: 'Softy Mode',
                description: 'Kein Item-Loss, perfekt zum Üben. Niedrige Belohnungen.',
                icon: '🛡️',
                color: '#00ff00'
            }
        };

        let html = '<div style="text-align: center;"><h3 style="color: #FFD700;">🏟️ ARENA MODUS WÄHLEN</h3></div>';

        for (const [key, mode] of Object.entries(modes)) {
            html += `
                <button onclick="window.selectArenaMode('${key}')" style="
                    display: block;
                    width: 100%;
                    padding: 20px;
                    margin: 15px 0;
                    background: rgba(${key === 'hardcore' ? '255,0,0' : key === 'normal' ? '255,170,0' : '0,255,0'}, 0.2);
                    border: 3px solid ${mode.color};
                    border-radius: 10px;
                    color: white;
                    cursor: pointer;
                    font-family: 'Courier New', monospace;
                    font-size: 16px;
                    text-align: left;
                    transition: all 0.2s;
                "
                onmouseenter="this.style.transform='scale(1.05)'; this.style.boxShadow='0 0 20px ${mode.color}';"
                onmouseleave="this.style.transform='scale(1)'; this.style.boxShadow='none';">
                    <div style="font-size: 24px; margin-bottom: 10px;">${mode.icon} ${mode.name}</div>
                    <div style="font-size: 14px; color: #aaa;">${mode.description}</div>
                </button>
            `;
        }

        return html;
    }

    selectArenaMode(mode) {
        this.arenaMode = mode;
        console.log(`🏟️ Arena Modus gewählt: ${mode}`);

        const modeNames = {
            hardcore: 'Hardcore',
            normal: 'Normal',
            softy: 'Softy'
        };

        alert(`Arena Modus: ${modeNames[mode]}\n\nDas Arena-System wird in einer späteren Phase mit Multiplayer vollständig implementiert.\n\nBereit für den Kampf! ⚔️`);
    }

    // ===== ONSEN SYSTEM (Dampf-Hain - Healing Zones) =====

    checkOnsenProximity(playerPosition, buildings) {
        if (!buildings) return false;

        // Suche Onsen-Gebäude
        for (const building of buildings) {
            if (building.userData.buildingType === 'onsen') {
                const distance = this.getDistanceToBuilding(playerPosition, building.position);

                // Im Onsen? (< 10 Einheiten)
                if (distance < 10) {
                    if (!this.inOnsen) {
                        this.enterOnsen();
                    }
                    return true;
                }
            }
        }

        // Nicht mehr im Onsen
        if (this.inOnsen) {
            this.leaveOnsen();
        }

        return false;
    }

    enterOnsen() {
        this.inOnsen = true;
        console.log('♨️ Onsen betreten! HP Regeneration +10/s aktiv!');

        // Zeige Onsen-UI
        const onsenUI = document.getElementById('onsen-ui');
        if (onsenUI) {
            onsenUI.style.display = 'block';
        }

        // Starte Heilung (alle 1 Sekunde +10 HP)
        if (!this.onsenHealInterval) {
            this.onsenHealInterval = setInterval(() => {
                if (this.inOnsen) {
                    // Heile HP (via Combat System)
                    if (window.realtimeCombat) {
                        window.realtimeCombat.playerHealth = Math.min(
                            window.realtimeCombat.playerHealth + 10,
                            window.realtimeCombat.playerMaxHealth
                        );
                        console.log(`♨️ Onsen Heilung: +10 HP`);
                    }
                }
            }, 1000);
        }
    }

    leaveOnsen() {
        this.inOnsen = false;
        console.log('♨️ Onsen verlassen!');

        // Verstecke Onsen-UI
        const onsenUI = document.getElementById('onsen-ui');
        if (onsenUI) {
            onsenUI.style.display = 'none';
        }

        // Stoppe Heilung
        if (this.onsenHealInterval) {
            clearInterval(this.onsenHealInterval);
            this.onsenHealInterval = null;
        }

        // Gebe "Comfort" Buff (10 Minuten, +5% alle Stats)
        if (this.foodSystem) {
            console.log('✨ Comfort Buff erhalten! (+5% alle Stats, 10 Min)');
            // Füge Comfort-Buff hinzu (simuliert als Food-Buff)
            this.foodSystem.applyBuffs({
                id: 'onsen_comfort',
                name: 'Onsen Comfort',
                effects: {
                    strength: 5,
                    combat_power: 5,
                    speed_bonus: 0.05,
                    comfort: 5
                },
                startTime: Date.now(),
                duration: 600000 // 10 Minuten
            });
        }
    }

    // ===== LEUCHTTURM SYSTEM (Salzige Bucht - Klettbar) =====

    checkLighthouseProximity(playerPosition, buildings) {
        if (!buildings) return null;

        // Suche Leuchtturm
        for (const building of buildings) {
            if (building.userData.buildingType === 'lighthouse') {
                const distance = this.getDistanceToBuilding(playerPosition, building.position);

                // Nahe genug zum Klettern? (< 5 Einheiten)
                if (distance < 5) {
                    return building;
                }
            }
        }

        return null;
    }

    startClimbing(lighthouse) {
        this.isClimbing = true;
        this.lighthouseHeight = 0;

        console.log('🗼 Leuchtturm-Klettern gestartet! Halte SPACE gedrückt!');

        // Zeige Climb-UI
        const climbUI = document.getElementById('lighthouse-climb-ui');
        if (climbUI) {
            climbUI.style.display = 'block';
        }
    }

    updateClimbing(delta, climbing) {
        if (!this.isClimbing) return 0;

        if (climbing) {
            // Klettere nach oben (5 Einheiten/Sekunde)
            this.lighthouseHeight = Math.min(
                this.lighthouseHeight + delta * 5,
                this.lighthouseMaxHeight
            );

            // Oben angekommen?
            if (this.lighthouseHeight >= this.lighthouseMaxHeight) {
                this.reachLighthouseTop();
            }

            // Update UI
            const climbUI = document.getElementById('lighthouse-climb-ui');
            if (climbUI) {
                const percent = Math.floor((this.lighthouseHeight / this.lighthouseMaxHeight) * 100);
                climbUI.innerHTML = `
                    <div style="font-weight: bold; color: #FFD700; margin-bottom: 10px;">
                        🗼 Leuchtturm klettern
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.2); border-radius: 5px; height: 20px; margin-bottom: 10px;">
                        <div style="background: #4CAF50; height: 100%; width: ${percent}%; border-radius: 5px;"></div>
                    </div>
                    <div style="font-size: 12px; color: #aaa;">
                        Höhe: ${this.lighthouseHeight.toFixed(1)}m / ${this.lighthouseMaxHeight}m
                    </div>
                    <div style="font-size: 12px; color: #fff; margin-top: 10px;">
                        Halte SPACE gedrückt zum Klettern
                    </div>
                `;
            }
        } else {
            // Nicht mehr am Klettern - langsam nach unten
            this.lighthouseHeight = Math.max(this.lighthouseHeight - delta * 2, 0);

            if (this.lighthouseHeight <= 0) {
                this.stopClimbing();
            }
        }

        return this.lighthouseHeight;
    }

    reachLighthouseTop() {
        console.log('🗼 Leuchtturm-Spitze erreicht! Genieße die Aussicht!');

        alert('🗼 LEUCHTTURM-SPITZE ERREICHT!\n\nDu hast einen atemberaubenden Blick über das gesamte Meer!\n\n✨ Achievement freigeschaltet: "Höhenpunkt"');

        // Give reward
        if (this.inventorySystem) {
            this.inventorySystem.addGold(100);
            console.log('💰 +100 Gold für das Erklimmen des Leuchtturms!');
        }
    }

    stopClimbing() {
        this.isClimbing = false;
        this.lighthouseHeight = 0;

        // Verstecke Climb-UI
        const climbUI = document.getElementById('lighthouse-climb-ui');
        if (climbUI) {
            climbUI.style.display = 'none';
        }

        console.log('🗼 Leuchtturm-Klettern beendet');
    }

    // ===== PLAYER SHOPS (Handelsfestung) =====

    // Player Shops sind bereits als Gebäude vorhanden
    // Interiors und Ownership-System werden später mit Multiplayer implementiert

    checkPlayerShopProximity(playerPosition, buildings) {
        if (!buildings) return null;

        for (const building of buildings) {
            if (building.userData.buildingType === 'player_shop') {
                const distance = this.getDistanceToBuilding(playerPosition, building.position);

                if (distance < 3) {
                    return building;
                }
            }
        }

        return null;
    }

    showPlayerShopInfo(shop) {
        const shopName = shop.userData.buildingName || 'Player Shop';

        console.log(`🛒 ${shopName}: Noch kein Besitzer`);

        // Placeholder für Multiplayer
        return `
            <div style="text-align: center;">
                <h3 style="color: #FFD700;">🛒 ${shopName}</h3>
                <p style="color: #aaa; margin: 20px 0;">
                    Dieser Shop ist noch leer.<br><br>
                    Im Multiplayer-Modus kannst du hier deinen<br>
                    eigenen Shop eröffnen und Items verkaufen!
                </p>
                <p style="color: #4CAF50; font-size: 14px;">
                    (Fallout 76 Style - Coming Soon!)
                </p>
            </div>
        `;
    }

    // ===== HELPER FUNCTIONS =====

    getDistanceToBuilding(playerPos, buildingPos) {
        const dx = playerPos.x - buildingPos.x;
        const dz = playerPos.z - buildingPos.z;
        return Math.sqrt(dx * dx + dz * dz);
    }

    // ===== UPDATE =====

    update(delta, playerPosition, buildings) {
        // Check Onsen Healing
        this.checkOnsenProximity(playerPosition, buildings);

        // Update Climbing
        // (wird von außen mit climbing-Parameter gesteuert)
    }

    // ===== CREATE UI ELEMENTS =====

    createOnsenUI() {
        const ui = document.createElement('div');
        ui.id = 'onsen-ui';
        ui.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 150, 255, 0.9);
            border: 3px solid #4682b4;
            border-radius: 15px;
            padding: 30px;
            color: white;
            font-family: 'Courier New', monospace;
            text-align: center;
            z-index: 600;
            display: none;
            font-size: 18px;
        `;
        ui.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 15px;">♨️</div>
            <div style="font-weight: bold; font-size: 24px; margin-bottom: 10px;">ONSEN HEILUNG AKTIV</div>
            <div style="font-size: 16px; color: #aaffff;">HP Regeneration: +10/s</div>
            <div style="font-size: 14px; color: #aaffff; margin-top: 10px;">Entspanne dich im heißen Wasser...</div>
        `;
        document.body.appendChild(ui);
        return ui;
    }

    createLighthouseClimbUI() {
        const ui = document.createElement('div');
        ui.id = 'lighthouse-climb-ui';
        ui.style.cssText = `
            position: fixed;
            bottom: 150px;
            left: 50%;
            transform: translateX(-50%);
            width: 400px;
            background: rgba(0, 0, 0, 0.9);
            border: 3px solid #3498db;
            border-radius: 15px;
            padding: 20px;
            color: white;
            font-family: 'Courier New', monospace;
            text-align: center;
            z-index: 600;
            display: none;
        `;
        document.body.appendChild(ui);
        return ui;
    }

    createArenaUI() {
        const ui = document.createElement('div');
        ui.id = 'arena-ui';
        ui.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 600px;
            background: rgba(0, 0, 0, 0.95);
            border: 3px solid #FFD700;
            border-radius: 15px;
            padding: 30px;
            color: white;
            font-family: 'Courier New', monospace;
            z-index: 1000;
            display: none;
        `;
        document.body.appendChild(ui);
        return ui;
    }
}

// Export für globale Nutzung
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SpecialFeatures;
}
