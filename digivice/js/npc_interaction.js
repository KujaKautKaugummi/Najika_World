// =============================================================================
// NPC INTERACTION SYSTEM - F-Taste für Shops, Dialoge, Händler
// =============================================================================

class NPCInteractionSystem {
    constructor(scene, camera, worldManager) {
        this.scene = scene;
        this.camera = camera;
        this.worldManager = worldManager;

        this.raycaster = new THREE.Raycaster();
        this.raycaster.far = 10; // 10 Meter Interaktions-Radius

        this.nearestNPC = null;
        this.interactionPrompt = null;

        this.setupKeyboardListener();
        this.setupUI();

        console.log('[NPC] Interaction System initialized (F-Key)');
    }

    setupKeyboardListener() {
        document.addEventListener('keydown', (e) => {
            // Ignorieren wenn Chat-Input oder andere Input-Felder fokussiert sind
            if (window.chatInputFocused ||
                e.target.tagName === 'INPUT' ||
                e.target.tagName === 'TEXTAREA' ||
                e.target.isContentEditable) {
                return;
            }
            if (e.key === 'f' || e.key === 'F') {
                this.interact();
            }
        });
    }

    setupUI() {
        // Interaction Prompt UI
        this.interactionPrompt = document.createElement('div');
        this.interactionPrompt.id = 'npc-interaction-prompt';
        this.interactionPrompt.style.cssText = `
            position: fixed;
            bottom: 120px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.9);
            color: #FFD700;
            padding: 12px 25px;
            border-radius: 8px;
            border: 2px solid #FFD700;
            font-family: monospace;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            pointer-events: none;
            z-index: 9999;
            display: none;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
            animation: promptPulse 1.5s ease-in-out infinite;
        `;
        document.body.appendChild(this.interactionPrompt);

        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes promptPulse {
                0%, 100% { opacity: 0.8; transform: translateX(-50%) scale(1); }
                50% { opacity: 1; transform: translateX(-50%) scale(1.05); }
            }
        `;
        document.head.appendChild(style);
    }

    // Update loop - check for nearby NPCs
    update(playerPosition) {
        if (!playerPosition) return;

        const nearestNPC = this.findNearestNPC(playerPosition);

        if (nearestNPC && nearestNPC.distance < 3) { // 3 Meter Radius (reduziert von 5)
            this.nearestNPC = nearestNPC;
            this.showPrompt(nearestNPC.npc);
        } else {
            this.nearestNPC = null;
            this.hidePrompt();
        }
    }

    findNearestNPC(playerPosition) {
        let nearest = null;
        let minDistance = Infinity;

        // Suche nach allen NPC/Building Meshes im Scene
        this.scene.traverse((obj) => {
            if (obj.userData && obj.userData.isNPC) {
                const distance = playerPosition.distanceTo(obj.position);
                if (distance < minDistance) {
                    minDistance = distance;
                    nearest = {
                        npc: obj,
                        distance: distance
                    };
                }
            }
        });

        return nearest;
    }

    showPrompt(npc) {
        const npcName = npc.userData.npcName || 'NPC';
        const npcType = npc.userData.npcType || 'talk';

        let actionText = '';
        switch(npcType) {
            case 'shop':
            case 'trading_post':
                actionText = '🏪 Handeln';
                break;
            case 'inn':
            case 'restaurant':
                actionText = '🍺 Betreten';
                break;
            case 'arena':
                actionText = '⚔️ Kämpfen';
                break;
            case 'forge':
            case 'blacksmith':
                actionText = '🔨 Schmieden';
                break;
            default:
                actionText = '💬 Sprechen';
        }

        this.interactionPrompt.innerHTML = `
            <div>${actionText} - ${npcName}</div>
            <div style="font-size: 12px; margin-top: 4px; opacity: 0.8;">[Drücke F]</div>
        `;
        this.interactionPrompt.style.display = 'block';
    }

    hidePrompt() {
        this.interactionPrompt.style.display = 'none';
    }

    interact() {
        if (!this.nearestNPC) {
            console.log('[NPC] Kein NPC in der Nähe');
            return;
        }

        const npc = this.nearestNPC.npc;
        const npcType = npc.userData.npcType || 'talk';
        const npcName = npc.userData.npcName || 'NPC';

        console.log(`[NPC] Interacting with ${npcName} (${npcType})`);

        switch(npcType) {
            case 'shop':
            case 'trading_post':
                this.openShop(npc);
                break;
            case 'inn':
            case 'restaurant':
                this.openInn(npc);
                break;
            case 'arena':
                this.openArena(npc);
                break;
            case 'forge':
            case 'blacksmith':
                this.openForge(npc);
                break;
            default:
                this.openDialog(npc);
        }
    }

    // =========================================================================
    // NPC TYPE HANDLERS
    // =========================================================================

    openShop(npc) {
        const npcName = npc.userData.npcName || 'Händler';

        // Create Shop UI
        const shopUI = document.createElement('div');
        shopUI.id = 'shop-ui';
        shopUI.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            color: #fff;
            padding: 30px;
            border-radius: 15px;
            border: 3px solid #FFD700;
            z-index: 10000;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        `;

        shopUI.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="margin: 0; color: #FFD700;">🏪 ${npcName}</h2>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: #f44336;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                ">Schließen ✕</button>
            </div>

            <div style="margin: 20px 0;">
                <h3 style="color: #4CAF50;">📦 Waren</h3>
                <div id="shop-items" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; margin-top: 10px;">
                    ${this.generateShopItems()}
                </div>
            </div>

            <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #444;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 18px; font-weight: bold; color: #FFD700;">
                        💰 Dein Gold: <span id="player-gold">1000</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(shopUI);

        // Load player gold from backend
        this.loadPlayerGold();
    }

    generateShopItems() {
        const items = [
            { name: 'Heiltrank', icon: '🧪', price: 50, type: 'potion' },
            { name: 'Manatrank', icon: '💙', price: 50, type: 'potion' },
            { name: 'Stahlschwert', icon: '⚔️', price: 200, type: 'weapon' },
            { name: 'Eisenschild', icon: '🛡️', price: 150, type: 'shield' },
            { name: 'Lederrüstung', icon: '🥋', price: 300, type: 'armor' },
            { name: 'Feuerzauber', icon: '🔥', price: 100, type: 'spell' },
        ];

        return items.map(item => `
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border: 2px solid transparent;
                transition: all 0.3s;
                cursor: pointer;
            " onmouseover="this.style.borderColor='#FFD700'" onmouseout="this.style.borderColor='transparent'" onclick="window.npcSystem.buyItem('${item.name}', ${item.price})">
                <div style="font-size: 40px; margin-bottom: 8px;">${item.icon}</div>
                <div style="font-weight: bold; margin-bottom: 5px;">${item.name}</div>
                <div style="color: #FFD700; font-size: 14px;">💰 ${item.price}g</div>
            </div>
        `).join('');
    }

    buyItem(itemName, price) {
        console.log(`[Shop] Kaufe ${itemName} für ${price}g`);

        fetch('http://localhost:8001/api/shop/buy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                player_id: 'kuja',
                item_id: itemName,
                price: price
            })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                this.showNotification(`✅ ${itemName} gekauft! -${price}g`, 'success');
                this.loadPlayerGold();
                // Frontend-Inventar sync
                if (window.inventorySystem) window.inventorySystem.addItem(itemName, 1);
                // GameEvents
                if (window.GameEvents) {
                    window.GameEvents.emit('itemPurchased', { itemId: itemName, price });
                    window.GameEvents.emit('itemCollected', { itemId: itemName, quantity: 1, source: 'shop' });
                }
            } else {
                this.showNotification(`❌ ${data.error || 'Nicht genug Gold'}`, 'error');
            }
        })
        .catch(err => {
            console.warn('[Shop] Backend nicht erreichbar, Offline-Kauf:', err);
            this.showNotification(`✅ ${itemName} gekauft! (Offline)`, 'success');
            if (window.inventorySystem) window.inventorySystem.addItem(itemName, 1);
        });
    }

    showNotification(text, type) {
        const notif = document.createElement('div');
        notif.style.cssText = `
            position:fixed; top:20px; right:20px; z-index:5000;
            background:${type === 'success' ? 'rgba(0,100,0,0.9)' : 'rgba(150,0,0,0.9)'};
            color:#fff; padding:12px 20px; border-radius:10px;
            border:2px solid ${type === 'success' ? '#00ff00' : '#ff4444'};
            font-family:Arial; font-size:14px;
        `;
        notif.textContent = text;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 3000);
    }

    loadPlayerGold() {
        const goldElement = document.getElementById('player-gold');
        if (!goldElement) return;

        fetch('http://localhost:8001/api/player/gold')
            .then(r => r.json())
            .then(data => {
                goldElement.textContent = data.gold || 1000;
            })
            .catch(err => {
                console.warn('[Shop] Backend nicht erreichbar, nutze Fallback-Gold');
                goldElement.textContent = '1000';
            });
    }

    openInn(npc) {
        const npcName = npc.userData.npcName || 'Gasthaus';
        // Versuche das echte Inn-UI aus overworld_npcs zu öffnen
        if (window.OverworldNPCs?.openInnUI) {
            window.OverworldNPCs.openInnUI({ id: npc.userData.npcId, name: npcName });
        } else if (typeof notify === 'function') {
            notify(`🍺 ${npcName}: Willkommen!`, 'info');
        }
    }

    openArena(npc) {
        const npcName = npc.userData.npcName || 'Arena';
        if (window.NemesisArena) {
            window.NemesisArena.show();
        } else if (window.openNemesisArena) {
            window.openNemesisArena();
        } else if (typeof notify === 'function') {
            notify(`⚔️ ${npcName}: Arena bereit!`, 'info');
        }
    }

    openForge(npc) {
        const npcName = npc.userData.npcName || 'Schmiede';
        if (window.OverworldNPCs?.openForgeUI) {
            window.OverworldNPCs.openForgeUI({ id: npc.userData.npcId, name: npcName });
        } else if (typeof notify === 'function') {
            notify(`🔨 ${npcName}: Willkommen in der Schmiede!`, 'info');
        }
    }

    openDialog(npc) {
        const npcName = npc.userData.npcName || 'NPC';
        const npcDialog = npc.userData.npcDialog || 'Hallo Reisender!';
        // Nutze Personality-System für dynamischen Dialog
        const greeting = window.NPCPersonalitySystem?.getGreeting?.(npc.userData.npcId) || npcDialog;
        if (typeof notify === 'function') {
            notify(`💬 ${npcName}: "${greeting}"`, 'info');
        }
    }
}

// Expose to window for inline onclick handlers
window.npcSystem = null;
