/**
 * OVERWORLD NPC SYSTEM - Najika World
 * ====================================
 *
 * Spawnt NPCs als 3D-Modelle in der Open World
 * - KayKit Character-Modelle statt Zylinder
 * - Proximity-Detection für Interaction
 * - Integration mit npc_dialogue_system.js
 * - Händler bei Städten, Wanderer auf Straßen
 */

const OverworldNPCs = (function() {
    'use strict';

    const ASSET_BASE = '/static/assets/';
    const MODELS = {
        knight:    'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf',
        barbarian: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_barbarian.gltf',
        mage:      'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_mage.gltf',
        rogue:     'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_rogue.gltf'
    };

    // ==========================================
    // OVERWORLD NPC DEFINITIONEN
    // ==========================================

    const OVERWORLD_NPCS = [
        // === GÖTTERFELS (Schwarze Mühle - Safe Zone) ===
        {
            id: 'goetterfels_haendler', name: 'Reisender Händler Tomoe',
            type: 'vendor', model: MODELS.barbarian, color: 0x8B7355,
            position: { x: 4850, y: 0, z: 4850 }, modelScale: 3.5,
            shopType: 'general',
            dialogue: [{ text: "Willkommen am Götterfels! Ich habe Waren aus allen Regionen!",
                         options: [{ text: "Zeig mir deine Waren", action: 'open_shop' }, { text: "Danke, nein", action: 'close' }] }],
            inventory: ['health_potion', 'bread', 'iron_sword', 'leather_armor', 'torch']
        },
        {
            id: 'goetterfels_schmied', name: 'Wanderschmied Goro',
            type: 'vendor', model: MODELS.knight, color: 0xCD853F,
            position: { x: 4750, y: 0, z: 4900 }, modelScale: 3.5,
            shopType: 'weapons',
            dialogue: [{ text: "Brauchst du eine gute Klinge? Ich bin der beste Schmied weit und breit!",
                         options: [{ text: "Was hast du?", action: 'open_shop' }, { text: "Vielleicht später", action: 'close' }] }],
            inventory: ['steel_sword', 'iron_axe', 'steel_shield', 'chainmail']
        },
        {
            id: 'goetterfels_questgeber', name: 'Abenteurer Hiro',
            type: 'quest_giver', model: MODELS.rogue, color: 0x4682B4,
            position: { x: 4900, y: 0, z: 4750 }, modelScale: 3.5,
            dialogue: [{ text: "Hey! Du siehst aus wie jemand der Abenteuer sucht!",
                         options: [{ text: "Was gibt es zu tun?", action: 'show_quests' }, { text: "Nicht jetzt", action: 'close' }] }],
            quests: ['wolfsjagd', 'sammler', 'erste_schritte', 'erkunder']
        },
        {
            id: 'goetterfels_hexe', name: 'Kräuterhexe Midori',
            type: 'vendor', model: MODELS.mage, color: 0x6B8E23,
            position: { x: 4700, y: 0, z: 4780 }, modelScale: 3.5,
            shopType: 'alchemy',
            dialogue: [{ text: "Kräuter und Tränke... alles was ein Abenteurer braucht!",
                         options: [{ text: "Zeig mir deine Tränke", action: 'open_shop' }, { text: "Nein danke", action: 'close' }] }],
            inventory: ['health_potion', 'mana_potion', 'antidote', 'stamina_potion']
        },

        // === WANDERNDE NPCs (verschiedene Positionen) ===
        {
            id: 'wanderer_krieger', name: 'Söldner Kaze',
            type: 'quest_giver', model: MODELS.knight, color: 0x8B0000,
            position: { x: 3500, y: 0, z: 3500 }, modelScale: 3.5,
            dialogue: [{ text: "Die Wölfe im Samtmoos-Wald werden immer frecher...",
                         options: [{ text: "Kann ich helfen?", action: 'show_quests' }, { text: "Pass auf dich auf", action: 'close' }] }],
            quests: ['wolfsjagd']
        },
        {
            id: 'wanderer_magier', name: 'Wandermagier Kazuki',
            type: 'trainer', model: MODELS.mage, color: 0x9370DB,
            position: { x: 5500, y: 0, z: 3000 }, modelScale: 3.5,
            dialogue: [{ text: "Die Magie der Blitzebene ist besonders stark hier...",
                         options: [{ text: "Kannst du mir etwas beibringen?", action: 'train_magic' }, { text: "Interessant...", action: 'close' }] }],
            skills: ['fireball', 'ice_lance', 'lightning_bolt']
        },
        {
            id: 'wanderer_schatzjaeger', name: 'Schatzsucherin Sakura',
            type: 'quest_giver', model: MODELS.rogue, color: 0xFFD700,
            position: { x: 6000, y: 0, z: 6000 }, modelScale: 3.5,
            dialogue: [{ text: "Ich suche seltene Kristalle in den Tiefenhöhlen! Willst du mir helfen?",
                         options: [{ text: "Klar!", action: 'show_quests' }, { text: "Nein", action: 'close' }] }],
            quests: ['sammler']
        }
    ];

    // ==========================================
    // STATE
    // ==========================================

    const state = {
        spawnedNPCs: [],
        scene: null,
        interactionRange: 15,  // Wie nah muss Spieler für Interaction
        promptRange: 25,       // Ab wann "E drücken" angezeigt wird
        gltfLoader: null,
        modelCache: {}
    };

    // ==========================================
    // INITIALIZATION
    // ==========================================

    function init(scene) {
        state.scene = scene;

        if (window.THREE && THREE.GLTFLoader) {
            state.gltfLoader = new THREE.GLTFLoader();
        }

        console.log('🧑 Overworld NPC System initializing...');

        // Alle Overworld-NPCs spawnen
        OVERWORLD_NPCS.forEach(npcDef => spawnNPC(npcDef));

        // Proximity-Check Loop
        setInterval(checkProximity, 500);

        console.log(`✅ ${state.spawnedNPCs.length} Overworld NPCs gespawnt`);
    }

    // ==========================================
    // SPAWNING
    // ==========================================

    function spawnNPC(npcDef) {
        if (!state.scene || !window.THREE) return;

        const group = new THREE.Group();
        group.position.set(npcDef.position.x, npcDef.position.y, npcDef.position.z);
        group.userData.npcId = npcDef.id;
        group.userData.isNPC = true;
        group.userData.npcData = npcDef;

        // Name-Label
        createNPCLabel(npcDef, group);

        // Typ-Indikator über Label
        createTypeIndicator(npcDef, group);

        state.scene.add(group);

        const npcInstance = {
            ...npcDef,
            mesh: group,
            isInteracting: false
        };

        state.spawnedNPCs.push(npcInstance);

        // Model laden
        if (npcDef.model && state.gltfLoader) {
            loadNPCModel(npcDef, group);
        } else {
            // Fallback
            const fallback = createNPCFallback(npcDef);
            group.add(fallback);
        }
    }

    function loadNPCModel(npcDef, group) {
        const fullPath = ASSET_BASE + npcDef.model;
        const cacheKey = npcDef.model;

        if (state.modelCache[cacheKey]) {
            const clone = state.modelCache[cacheKey].clone();
            applyNPCSettings(clone, npcDef);
            group.add(clone);
        } else {
            state.gltfLoader.load(
                fullPath,
                (gltf) => {
                    state.modelCache[cacheKey] = gltf.scene.clone();
                    const model = gltf.scene;
                    applyNPCSettings(model, npcDef);
                    group.add(model);
                    console.log(`✅ NPC model loaded: ${npcDef.name}`);
                },
                undefined,
                (error) => {
                    console.warn(`⚠️ NPC model failed: ${npcDef.name}`, error.message || error);
                    const fallback = createNPCFallback(npcDef);
                    group.add(fallback);
                }
            );
        }
    }

    function applyNPCSettings(model, npcDef) {
        const scale = npcDef.modelScale || 3.5;
        model.scale.set(scale, scale, scale);

        // Freundliche Farb-Tints
        model.traverse(node => {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
                if (node.material && npcDef.color) {
                    node.material = node.material.clone();
                    node.material.emissive = new THREE.Color(npcDef.color);
                    node.material.emissiveIntensity = 0.15;  // Subtiler als Enemies
                }
            }
        });

        // Füße auf Boden
        const box = new THREE.Box3().setFromObject(model);
        model.position.y = -box.min.y;
    }

    function createNPCFallback(npcDef) {
        const geometry = new THREE.CylinderGeometry(0.8, 0.8, 3, 8);
        const material = new THREE.MeshStandardMaterial({
            color: npcDef.color || 0x8B4513,
            roughness: 0.6
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.y = 1.5;
        mesh.castShadow = true;
        return mesh;
    }

    function createNPCLabel(npcDef, parentGroup) {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 48;
        const ctx = canvas.getContext('2d');

        // Freundlicher grüner Hintergrund (NPCs = freundlich, Enemies = rot)
        const bgColor = npcDef.type === 'vendor' ? 'rgba(0,100,0,0.85)' :
                         npcDef.type === 'quest_giver' ? 'rgba(180,150,0,0.85)' :
                         npcDef.type === 'trainer' ? 'rgba(80,0,160,0.85)' :
                         'rgba(0,80,120,0.85)';
        ctx.fillStyle = bgColor;
        ctx.roundRect(4, 4, 248, 40, 8);
        ctx.fill();

        // Name
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 18px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(npcDef.name, 128, 30);

        const texture = new THREE.CanvasTexture(canvas);
        const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(spriteMat);

        const height = (npcDef.modelScale || 3.5) * 1.5 + 3;
        sprite.position.set(0, height, 0);
        sprite.scale.set(6, 1.5, 1);

        parentGroup.add(sprite);
    }

    function createTypeIndicator(npcDef, parentGroup) {
        // Icon über dem NPC (💰 für Vendor, ❗ für Quest, 📚 für Trainer)
        const canvas = document.createElement('canvas');
        canvas.width = 64;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');

        ctx.font = '40px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        const icon = npcDef.type === 'vendor' ? '💰' :
                     npcDef.type === 'quest_giver' ? '❗' :
                     npcDef.type === 'trainer' ? '📚' : '💬';
        ctx.fillText(icon, 32, 32);

        const texture = new THREE.CanvasTexture(canvas);
        const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(spriteMat);

        const height = (npcDef.modelScale || 3.5) * 1.5 + 5;
        sprite.position.set(0, height, 0);
        sprite.scale.set(2, 2, 1);

        // Schwebe-Animation
        const baseY = height;
        let phase = Math.random() * Math.PI * 2;
        const animate = () => {
            phase += 0.03;
            sprite.position.y = baseY + Math.sin(phase) * 0.3;
            requestAnimationFrame(animate);
        };
        animate();

        parentGroup.add(sprite);
    }

    // ==========================================
    // PROXIMITY & INTERACTION
    // ==========================================

    let interactionPrompt = null;

    function checkProximity() {
        const playerPos = getPlayerPosition();
        if (!playerPos) return;

        let closestNPC = null;
        let closestDist = Infinity;

        state.spawnedNPCs.forEach(npc => {
            const dx = playerPos.x - npc.position.x;
            const dz = playerPos.z - npc.position.z;
            const dist = Math.sqrt(dx * dx + dz * dz);

            if (dist < closestDist) {
                closestDist = dist;
                closestNPC = npc;
            }
        });

        // Show/Hide "E drücken" prompt
        if (closestNPC && closestDist < state.promptRange) {
            showInteractionPrompt(closestNPC, closestDist < state.interactionRange);
        } else {
            hideInteractionPrompt();
        }
    }

    function showInteractionPrompt(npc, canInteract) {
        if (!interactionPrompt) {
            interactionPrompt = document.createElement('div');
            interactionPrompt.id = 'npc-interaction-prompt';
            interactionPrompt.style.cssText = `
                position: fixed; bottom: 120px; left: 50%; transform: translateX(-50%);
                background: rgba(0,0,0,0.85); color: #fff; padding: 10px 25px;
                border-radius: 10px; font-size: 16px; font-family: Arial;
                z-index: 1000; pointer-events: none; transition: opacity 0.3s;
                border: 2px solid #FFD700;
            `;
            document.body.appendChild(interactionPrompt);
        }

        const icon = npc.type === 'vendor' ? '💰' : npc.type === 'quest_giver' ? '❗' : npc.type === 'trainer' ? '📚' : '💬';
        interactionPrompt.innerHTML = canInteract
            ? `${icon} <b>[E]</b> ${npc.name} ansprechen`
            : `${icon} ${npc.name} (näher kommen)`;
        interactionPrompt.style.opacity = '1';
        interactionPrompt.style.borderColor = canInteract ? '#00ff00' : '#FFD700';

        // Aktiven NPC merken für E-Taste
        state.nearestInteractableNPC = canInteract ? npc : null;
    }

    function hideInteractionPrompt() {
        if (interactionPrompt) {
            interactionPrompt.style.opacity = '0';
        }
        state.nearestInteractableNPC = null;
    }

    function interactWithNearestNPC() {
        const npc = state.nearestInteractableNPC;
        if (!npc || npc.isInteracting) return false;

        console.log(`💬 Interacting with NPC: ${npc.name}`);
        npc.isInteracting = true;

        // Fraktions-basierte NPC-Reaktion
        let npcFaction = npc.faction || null;
        let npcAttitude = 'neutral';
        if (window.FactionSystem && npcFaction) {
            const reaction = FactionSystem.getNPCReaction(npcFaction);
            npcAttitude = reaction.attitude;
            if (reaction.willAttack) {
                showNotification(`⚔️ ${npc.name}: "${reaction.dialogue}"`, 'error');
                npc.isInteracting = false;

                // Kampf gegen feindlichen NPC starten
                startHostileNPCCombat(npc);
                return false;
            }
        }

        // GameEvent emittieren (mit Faction-Info)
        if (window.GameEvents) {
            window.GameEvents.emit('npcTalked', { npcId: npc.id, npcName: npc.name, npcType: npc.type, npcFaction });
        }

        // NPC-Typ spezifische Aktionen
        if (npc.type === 'arena' || npc.type === 'pvp_arena_master') {
            if (window.NemesisArena) {
                window.NemesisArena.showArenaPanel ? window.NemesisArena.showArenaPanel() : (window.NemesisArena.open ? window.NemesisArena.open() : console.warn('NemesisArena hat keine show/open Methode'));
            } else if (window.openNemesisArena) {
                window.openNemesisArena();
            } else {
                showSimpleDialogue(npc);
            }
        } else if (npc.type === 'vendor' || npc.type === 'shop' || npc.type === 'merchant') {
            openShopUI(npc);
        } else if (npc.type === 'inn' || npc.type === 'inn_keeper' || npc.type === 'restaurant') {
            openInnUI(npc);
        } else if (npc.type === 'forge' || npc.type === 'blacksmith') {
            openForgeUI(npc);
        } else if (window.npcDialogueSystem && window.npcDialogueSystem.startDialogue) {
            // Versuche Dialog-Baum System
            const npcId = npc.id || npc.name;
            if (!window.npcDialogueSystem.startDialogue(npcId, npc)) {
                // Fallback wenn NPC nicht im Dialog-System registriert
                showSimpleDialogue(npc);
            }
        } else {
            showSimpleDialogue(npc);
        }

        hideInteractionPrompt();

        // Nach 1s wieder interagierbar
        setTimeout(() => { npc.isInteracting = false; }, 1000);

        return true;
    }

    function showSimpleDialogue(npc) {
        // Priority: Schedule dialogue override > Personality greeting > Default dialogue
        let text;
        const scheduleOverride = window.NPCScheduleSystem?.getNPCDialogueOverride?.(npc.id);
        const personalityGreeting = window.NPCPersonalitySystem?.getGreeting?.(npc.id);

        if (scheduleOverride) {
            text = scheduleOverride;
        } else if (personalityGreeting) {
            text = personalityGreeting;
        } else {
            text = npc.dialogue?.[0]?.text || `${npc.name}: Hallo, Reisender!`;
        }

        // Show relationship label if available
        const relLabel = window.NPCPersonalitySystem?.getRelationshipLabel?.(npc.id) || '';

        // Einfaches Dialog-Overlay
        let overlay = document.getElementById('simple-npc-dialog');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'simple-npc-dialog';
            overlay.style.cssText = `
                position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.9); color: #fff; padding: 30px;
                border-radius: 15px; z-index: 2000; max-width: 400px;
                border: 2px solid #FFD700; font-family: Arial;
            `;
            document.body.appendChild(overlay);
        }

        const options = npc.dialogue?.[0]?.options || [{ text: "OK", action: 'close' }];
        const optionsHTML = options.map(opt =>
            `<button onclick="OverworldNPCs.handleDialogOption('${npc.id}', '${opt.action}')"
                style="background:#4a4a8a; color:#fff; border:none; padding:10px 20px;
                       border-radius:8px; margin:5px; cursor:pointer; font-size:14px;">
                ${opt.text}
            </button>`
        ).join('');

        overlay.innerHTML = `
            <div style="color:#FFD700; font-size:18px; font-weight:bold; margin-bottom:5px;">
                ${npc.name}
            </div>
            ${relLabel ? `<div style="font-size:12px; color:#aaa; margin-bottom:10px;">${relLabel}</div>` : ''}
            <div style="font-size:15px; margin-bottom:15px; line-height:1.5;">
                ${text}
            </div>
            <div style="text-align:center;">
                ${optionsHTML}
            </div>
        `;
        overlay.style.display = 'block';
    }

    // ==========================================
    // SHOP UI - Handel mit Economy-System
    // ==========================================

    function openShopUI(npc) {
        // Check if NPC is willing to sell (personality check)
        if (window.NPCPersonalitySystem && !NPCPersonalitySystem.willNPCSell(npc.id)) {
            if (typeof notify === 'function') {
                notify(`${npc.name} weigert sich, mit dir zu handeln!`, 'error');
            }
            return;
        }

        let overlay = document.getElementById('shop-ui-overlay');
        if (overlay) overlay.remove();

        overlay = document.createElement('div');
        overlay.id = 'shop-ui-overlay';
        overlay.style.cssText = `
            position:fixed; top:0; left:0; width:100%; height:100%;
            background:rgba(0,0,0,0.85); z-index:15000;
            display:flex; align-items:center; justify-content:center;
        `;

        const panel = document.createElement('div');
        panel.style.cssText = `
            background:linear-gradient(135deg,#1a1a2e,#1e3a2e);
            border:3px solid #FFD700; border-radius:15px;
            padding:25px; max-width:600px; width:90%; max-height:80vh;
            overflow-y:auto; color:#fff;
            font-family:'Segoe UI',Arial,sans-serif;
        `;

        const shopName = npc.name || 'Händler';
        const shopType = npc.shopType || 'general';
        const inventory = npc.inventory || ['health_potion', 'bread', 'iron_sword'];

        // Preis-Berechnung via EconomySystem
        const region = getCurrentRegion();
        const priceModifier = getPriceModifierForNPC(npc);

        let itemsHTML = '';
        inventory.forEach(itemId => {
            const ecoGood = window.EconomySystem?.GOODS?.[itemId];
            let name = itemId.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
            let icon = '📦';
            let price = 50;

            if (ecoGood) {
                name = ecoGood.name;
                icon = ecoGood.icon;
                price = window.EconomySystem.getPrice(itemId, region, true);
            }
            price = Math.round(price * priceModifier);

            itemsHTML += `
                <div style="display:flex;justify-content:space-between;align-items:center;
                    background:rgba(255,255,255,0.05);border:1px solid rgba(255,215,0,0.2);
                    border-radius:8px;padding:12px;margin-bottom:8px;cursor:pointer;
                    transition:border-color 0.2s;"
                    onmouseover="this.style.borderColor='#FFD700'"
                    onmouseout="this.style.borderColor='rgba(255,215,0,0.2)'">
                    <div>
                        <span style="font-size:20px;margin-right:8px;">${icon}</span>
                        <strong>${name}</strong>
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="color:#FFD700;font-weight:bold;font-size:16px;">${price}g</span>
                        <button onclick="OverworldNPCs._buyItem('${itemId}','${npc.id}',${price})" style="
                            background:#4CAF50;color:#fff;border:none;
                            padding:8px 15px;border-radius:5px;cursor:pointer;font-size:13px;">
                            Kaufen
                        </button>
                    </div>
                </div>`;
        });

        panel.innerHTML = `
            <h2 style="color:#FFD700;margin:0 0 5px;text-align:center">🏪 ${shopName}</h2>
            <p style="color:#888;text-align:center;margin:0 0 15px;font-size:12px;">${shopType.toUpperCase()} | ${region}</p>
            ${priceModifier !== 1.0 ? `<p style="color:${priceModifier < 1 ? '#2ecc71' : '#e74c3c'};text-align:center;font-size:12px;margin:0 0 15px;">
                Preismodifikator: ${Math.round(priceModifier * 100)}% (Reputation)
            </p>` : ''}
            <div>${itemsHTML}</div>
            <button onclick="document.getElementById('shop-ui-overlay').remove()" style="
                width:100%;margin-top:15px;background:#555;color:#fff;border:none;
                padding:12px;border-radius:10px;cursor:pointer;font-size:14px;">
                Verlassen
            </button>
        `;

        overlay.appendChild(panel);
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
        document.body.appendChild(overlay);
    }

    function handleBuyItem(itemId, npcId, price) {
        const region = getCurrentRegion();
        let result = null;

        if (window.EconomySystem) {
            result = EconomySystem.buyGood(itemId, region, 1);
        } else {
            result = { success: true, totalCost: price };
        }

        if (result.success) {
            showNotification(`🛒 ${itemId.replace(/_/g,' ')} gekauft! (-${result.totalCost || price}g)`, 'success');
            if (window.GameEvents) {
                GameEvents.emit('itemPurchased', { itemId, price: result.totalCost || price, npcId, region });
            }
        } else if (result.caught) {
            showNotification(`🚨 ${result.reason}`, 'error');
        } else {
            showNotification(`❌ ${result.reason || 'Kauf fehlgeschlagen'}`, 'error');
        }

        const overlay = document.getElementById('shop-ui-overlay');
        if (overlay) overlay.remove();
    }

    function getCurrentRegion() {
        if (window.WorldEventGenerator?.getCurrentBiome) {
            return WorldEventGenerator.getCurrentBiome();
        }
        return 'goetterfels';
    }

    function getPriceModifierForNPC(npc) {
        let modifier = 1.0;
        // Faction reputation modifier
        if (window.FactionSystem && npc.faction) {
            const factionMod = FactionSystem.getPriceModifier(npc.faction);
            if (factionMod !== Infinity) modifier = factionMod;
        }
        // Personality/relationship discount (-0.25 to +0.20)
        if (window.NPCPersonalitySystem) {
            const personalityDiscount = NPCPersonalitySystem.getShopDiscount(npc.id);
            if (personalityDiscount) modifier += personalityDiscount;
        }
        return Math.max(0.5, modifier); // Min 50% price
    }

    // ==========================================
    // INN UI - Schlafen, Essen, Heilen
    // ==========================================

    function openInnUI(npc) {
        let overlay = document.getElementById('inn-ui-overlay');
        if (overlay) overlay.remove();

        overlay = document.createElement('div');
        overlay.id = 'inn-ui-overlay';
        overlay.style.cssText = `
            position:fixed; top:0; left:0; width:100%; height:100%;
            background:rgba(0,0,0,0.8); z-index:15000;
            display:flex; align-items:center; justify-content:center;
        `;

        const panel = document.createElement('div');
        panel.style.cssText = `
            background:linear-gradient(135deg,#1a1a2e,#2d1b3d);
            border:3px solid #e67e22; border-radius:15px;
            padding:25px; max-width:450px; width:90%; color:#fff;
            font-family:'Segoe UI',Arial,sans-serif;
        `;

        const innName = npc.name || 'Gasthaus';
        panel.innerHTML = `
            <h2 style="color:#e67e22;margin:0 0 20px;text-align:center">🍺 ${innName}</h2>
            <p style="color:#ccc;text-align:center;margin-bottom:20px">"Willkommen, Reisender! Was darf es sein?"</p>

            <div style="display:grid;gap:10px;">
                <button onclick="OverworldNPCs._innAction('sleep','${npc.id}')" style="
                    background:linear-gradient(135deg,#2c3e50,#3498db);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    🛏️ <strong>Schlafen</strong> - Voll heilen, Energie + Stamina auffüllen
                    <br><small style="color:#aaa">Kostet 50 Gold</small>
                </button>
                <button onclick="OverworldNPCs._innAction('eat','${npc.id}')" style="
                    background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    🍖 <strong>Essen</strong> - Hunger stillen, +30% HP Regen
                    <br><small style="color:#aaa">Kostet 20 Gold</small>
                </button>
                <button onclick="OverworldNPCs._innAction('drink','${npc.id}')" style="
                    background:linear-gradient(135deg,#8e44ad,#9b59b6);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    🍺 <strong>Trinken</strong> - Durst stillen, +10% Mana Regen
                    <br><small style="color:#aaa">Kostet 10 Gold</small>
                </button>
                <button onclick="document.getElementById('inn-ui-overlay').remove()" style="
                    background:#555;color:#fff;border:none;padding:12px;border-radius:10px;
                    cursor:pointer;font-size:14px;margin-top:5px;">
                    Verlassen
                </button>
            </div>
        `;

        overlay.appendChild(panel);
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
        document.body.appendChild(overlay);
    }

    function handleInnAction(action, npcId) {
        const overlay = document.getElementById('inn-ui-overlay');

        if (action === 'sleep') {
            // Voll heilen via Survival System
            if (window.SurvivalSystem) {
                window.SurvivalSystem.setNeed('energy', 100);
                window.SurvivalSystem.setNeed('hunger', 80);
                window.SurvivalSystem.setNeed('thirst', 80);
            }
            if (window.GameEvents) window.GameEvents.emit('playerRested', { type: 'inn', quality: 'full' });
            showNotification('🛏️ Ausgeruht! Voll geheilt!', 'success');
        } else if (action === 'eat') {
            if (window.SurvivalSystem) window.SurvivalSystem.setNeed('hunger', 100);
            if (window.GameEvents) window.GameEvents.emit('playerAte', { type: 'inn_meal' });
            showNotification('🍖 Satt! +30% HP Regen!', 'success');
        } else if (action === 'drink') {
            if (window.SurvivalSystem) window.SurvivalSystem.setNeed('thirst', 100);
            if (window.GameEvents) window.GameEvents.emit('playerDrank', { type: 'inn_drink' });
            showNotification('🍺 Erfrischt! +10% Mana Regen!', 'success');
        }

        if (overlay) overlay.remove();
    }

    // ==========================================
    // FORGE UI - Waffen upgraden, reparieren
    // ==========================================

    function openForgeUI(npc) {
        let overlay = document.getElementById('forge-ui-overlay');
        if (overlay) overlay.remove();

        overlay = document.createElement('div');
        overlay.id = 'forge-ui-overlay';
        overlay.style.cssText = `
            position:fixed; top:0; left:0; width:100%; height:100%;
            background:rgba(0,0,0,0.8); z-index:15000;
            display:flex; align-items:center; justify-content:center;
        `;

        const panel = document.createElement('div');
        panel.style.cssText = `
            background:linear-gradient(135deg,#1a1a2e,#3d1b1b);
            border:3px solid #e74c3c; border-radius:15px;
            padding:25px; max-width:450px; width:90%; color:#fff;
            font-family:'Segoe UI',Arial,sans-serif;
        `;

        const forgeName = npc.name || 'Schmiede';
        panel.innerHTML = `
            <h2 style="color:#e74c3c;margin:0 0 20px;text-align:center">🔨 ${forgeName}</h2>
            <p style="color:#ccc;text-align:center;margin-bottom:20px">"Feuer und Stahl, das ist meine Sprache!"</p>

            <div style="display:grid;gap:10px;">
                <button onclick="OverworldNPCs._forgeAction('upgrade','${npc.id}')" style="
                    background:linear-gradient(135deg,#c0392b,#e74c3c);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    ⬆️ <strong>Waffe verbessern</strong> - +10% Schaden
                    <br><small style="color:#ffaaaa">Kostet 100 Gold + 5 Eisenbarren</small>
                </button>
                <button onclick="OverworldNPCs._forgeAction('repair','${npc.id}')" style="
                    background:linear-gradient(135deg,#d35400,#e67e22);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    🔧 <strong>Reparieren</strong> - Haltbarkeit wiederherstellen
                    <br><small style="color:#ffddaa">Kostet 30 Gold</small>
                </button>
                <button onclick="OverworldNPCs._forgeAction('infuse','${npc.id}')" style="
                    background:linear-gradient(135deg,#2980b9,#3498db);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    🔮 <strong>Element-Infusion</strong> - Dauerhaftes Element auf Waffe
                    <br><small style="color:#aaddff">Kostet 200 Gold + Elementar-Essenz</small>
                </button>
                <button onclick="document.getElementById('forge-ui-overlay').remove()" style="
                    background:#555;color:#fff;border:none;padding:12px;border-radius:10px;
                    cursor:pointer;font-size:14px;margin-top:5px;">
                    Verlassen
                </button>
            </div>
        `;

        overlay.appendChild(panel);
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
        document.body.appendChild(overlay);
    }

    function handleForgeAction(action, npcId) {
        const overlay = document.getElementById('forge-ui-overlay');

        if (action === 'upgrade') {
            if (window.GameEvents) window.GameEvents.emit('weaponUpgraded', { npcId });
            showNotification('⬆️ Waffe verbessert! +10% Schaden!', 'success');
        } else if (action === 'repair') {
            if (window.GameEvents) window.GameEvents.emit('weaponRepaired', { npcId });
            showNotification('🔧 Waffe repariert!', 'success');
        } else if (action === 'infuse') {
            if (window.GameEvents) window.GameEvents.emit('weaponInfused', { npcId });
            showNotification('🔮 Element-Infusion aufgebracht!', 'success');
        }

        if (overlay) overlay.remove();
    }

    function showNotification(text, type) {
        const notif = document.createElement('div');
        notif.style.cssText = `
            position:fixed; top:80px; right:20px; z-index:20000;
            background:${type === 'success' ? 'rgba(0,150,0,0.95)' : 'rgba(150,0,0,0.95)'};
            color:#fff; padding:15px 25px; border-radius:10px;
            border:2px solid ${type === 'success' ? '#00ff00' : '#ff4444'};
            font-family:Arial; font-size:15px; font-weight:bold;
            box-shadow:0 5px 20px rgba(0,0,0,0.5);
        `;
        notif.textContent = text;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 3000);
    }

    function handleDialogOption(npcId, action) {
        const overlay = document.getElementById('simple-npc-dialog');
        if (overlay) overlay.style.display = 'none';

        const npc = state.spawnedNPCs.find(n => n.id === npcId);
        if (!npc) return;

        switch(action) {
            case 'open_shop':
                // Immer das neue integrierte Shop-UI verwenden (mit Economy-Preisen)
                openShopUI(npc);
                break;
            case 'show_quests':
                if (window.questManager) {
                    (npc.quests || []).forEach(qId => {
                        const quest = window.questManager.quests[qId];
                        if (quest && quest.status === 'available') {
                            window.questManager.acceptQuest(qId);
                            console.log(`📜 Quest angenommen: ${quest.name}`);
                        }
                    });
                }
                break;
            case 'train_magic':
            case 'train_smithing':
                console.log(`📚 Training bei ${npc.name}: ${(npc.skills || []).join(', ')}`);
                break;
            case 'close':
            default:
                break;
        }
    }

    // ==========================================
    // UTILITY
    // ==========================================

    function getPlayerPosition() {
        if (window.character && window.character.position) {
            return { x: window.character.position.x, y: window.character.position.y, z: window.character.position.z };
        }
        if (window.playerPosition) return window.playerPosition;
        return { x: 4800, y: 0, z: 4800 };
    }

    // ==========================================
    // KEYBOARD HOOK (E = Interact)
    // ==========================================

    document.addEventListener('keydown', (e) => {
        if (e.key === 'e' || e.key === 'E') {
            if (state.nearestInteractableNPC) {
                e.preventDefault();
                interactWithNearestNPC();
            }
        }
    });

    // ==========================================
    // HOSTILE NPC COMBAT
    // ==========================================

    function startHostileNPCCombat(npc) {
        // Build enemy data from NPC
        const npcLevel = npc.level || 5;
        const npcHp = npc.hp || (100 + npcLevel * 20);
        const enemyData = {
            id: npc.id,
            name: npc.name,
            level: npcLevel,
            hp: npcHp,
            maxHp: npcHp,
            type: npc.model || npc.id,
            faction: npc.faction || null
        };

        // Emit combatStarted
        if (window.GameEvents) {
            window.GameEvents.emit('combatStarted', {
                type: 'npc_hostile',
                npcId: npc.id,
                npcFaction: npc.faction,
                enemies: [enemyData]
            });
        }

        // Real3DCombat ist das einzige Kampfsystem
        if (window.Real3DCombat && window.Real3DCombat.startCombat) {
            const scene = window.Scene3D?.scene || state.scene;
            const pos = npc.mesh ? npc.mesh.position : { x: 0, y: 0, z: -10 };
            window.Real3DCombat.startCombat([enemyData], scene, pos);
        } else {
            console.error('Real3DCombat nicht geladen!');
        }

        // Temporarily hide NPC during combat
        if (npc.mesh) npc.mesh.visible = false;

        // Restore NPC after combat ends (win or lose)
        const restoreNPC = () => {
            setTimeout(() => {
                if (npc.mesh) npc.mesh.visible = true;
                npc.isInteracting = false;
            }, 3000);
        };

        if (window.GameEvents) {
            window.GameEvents.once('combatEnded', restoreNPC);
        } else {
            setTimeout(restoreNPC, 10000);
        }
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    return {
        init,
        interactWithNearestNPC,
        handleDialogOption,
        _innAction: handleInnAction,
        _forgeAction: handleForgeAction,
        _buyItem: handleBuyItem,
        openInnUI,
        openForgeUI,
        openShopUI,
        getNPCs: () => state.spawnedNPCs,
        getNearestNPC: () => state.nearestInteractableNPC
    };

})();

window.OverworldNPCs = OverworldNPCs;
console.log('🧑 Overworld NPCs System loaded!');
