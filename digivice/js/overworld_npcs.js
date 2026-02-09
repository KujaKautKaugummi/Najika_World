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

        // GameEvent emittieren
        if (window.GameEvents) {
            window.GameEvents.emit('npcTalked', { npcId: npc.id, npcName: npc.name, npcType: npc.type });
        }

        // Dialog-System öffnen
        if (window.npcDialogueSystem && npc.dialogue && npc.dialogue.length > 0) {
            window.npcDialogueSystem.openDialogue(npc.id, npc);
        } else if (window.npcSystem && typeof window.npcSystem.interact === 'function') {
            window.npcSystem.interact(npc);
        } else {
            // Fallback: Simpler Alert-Dialog
            showSimpleDialogue(npc);
        }

        hideInteractionPrompt();

        // Nach 1s wieder interagierbar
        setTimeout(() => { npc.isInteracting = false; }, 1000);

        return true;
    }

    function showSimpleDialogue(npc) {
        const text = npc.dialogue?.[0]?.text || `${npc.name}: Hallo, Reisender!`;

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
            <div style="color:#FFD700; font-size:18px; font-weight:bold; margin-bottom:10px;">
                ${npc.name}
            </div>
            <div style="font-size:15px; margin-bottom:15px; line-height:1.5;">
                ${text}
            </div>
            <div style="text-align:center;">
                ${optionsHTML}
            </div>
        `;
        overlay.style.display = 'block';
    }

    function handleDialogOption(npcId, action) {
        const overlay = document.getElementById('simple-npc-dialog');
        if (overlay) overlay.style.display = 'none';

        const npc = state.spawnedNPCs.find(n => n.id === npcId);
        if (!npc) return;

        switch(action) {
            case 'open_shop':
                if (window.npcDialogueSystem) {
                    window.npcDialogueSystem.openShop(npcId, npc);
                } else {
                    console.log(`🛒 Shop öffnen für ${npc.name} (${npc.shopType})`);
                }
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
    // PUBLIC API
    // ==========================================

    return {
        init,
        interactWithNearestNPC,
        handleDialogOption,
        getNPCs: () => state.spawnedNPCs,
        getNearestNPC: () => state.nearestInteractableNPC
    };

})();

window.OverworldNPCs = OverworldNPCs;
console.log('🧑 Overworld NPCs System loaded!');
