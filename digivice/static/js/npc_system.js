/**
 * NAJIKA WORLD - NPC SYSTEM
 * ==========================
 *
 * Komplettes NPC-System mit:
 * - NPC-Typen: Vendors, Quest-Giver, Trainers, Citizens
 * - Dialogue-System
 * - Shop-Integration
 * - Quest-Integration
 * - Proximity-Detection
 */

class NPC {
    constructor(data) {
        this.id = data.id || `npc_${Date.now()}_${Math.random()}`;
        this.name = data.name;
        this.type = data.type; // 'vendor', 'quest_giver', 'trainer', 'citizen'
        this.position = data.position || { x: 0, y: 0, z: 0 };
        this.mesh = null;

        // Dialogue
        this.dialogue = data.dialogue || [];
        this.currentDialogueIndex = 0;

        // Vendor-specific
        this.inventory = data.inventory || []; // Array of item IDs
        this.shopType = data.shopType || null; // 'food', 'weapons', 'armor', 'general'

        // Quest-Giver-specific
        this.quests = data.quests || []; // Array of quest IDs

        // Trainer-specific
        this.skills = data.skills || []; // Array of skills to teach

        // Appearance
        this.color = data.color || 0x8B4513; // Brown default
        this.nameplate = null;

        // State
        this.isInteracting = false;
    }

    createMesh(THREE, scene) {
        // NPC Body (Capsule-like shape)
        const bodyGeometry = new THREE.CapsuleGeometry(0.5, 1.5, 8, 16);
        const bodyMaterial = new THREE.MeshStandardMaterial({
            color: this.color,
            roughness: 0.7,
            metalness: 0.2
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.castShadow = true;
        body.receiveShadow = true;

        // Position
        body.position.set(this.position.x, this.position.y + 1, this.position.z);

        // Store reference
        this.mesh = body;
        this.mesh.userData.npc = this; // Back-reference

        scene.add(body);

        // Create Nameplate
        this.createNameplate(THREE, scene);

        return body;
    }

    createNameplate(THREE, scene) {
        // Create canvas for text
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 128;
        const context = canvas.getContext('2d');

        // Background
        context.fillStyle = 'rgba(0, 0, 0, 0.7)';
        context.fillRect(0, 0, 512, 128);

        // Name
        context.font = 'Bold 48px Arial';
        context.fillStyle = '#ffffff';
        context.textAlign = 'center';
        context.fillText(this.name, 256, 65);

        // Type indicator
        const typeIcons = {
            vendor: '🛒',
            quest_giver: '❗',
            trainer: '⚔️',
            citizen: '🧑'
        };
        const icon = typeIcons[this.type] || '🧑';
        context.font = 'Bold 40px Arial';
        context.fillText(icon, 256, 110);

        // Create sprite
        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({
            map: texture,
            transparent: true
        });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.scale.set(3, 0.75, 1);
        sprite.position.set(
            this.position.x,
            this.position.y + 3.5,
            this.position.z
        );

        this.nameplate = sprite;
        scene.add(sprite);
    }

    getDistanceToPlayer(playerPosition) {
        if (!this.mesh) return Infinity;

        const npcPos = this.mesh.position;
        const dx = npcPos.x - playerPosition.x;
        const dz = npcPos.z - playerPosition.z;

        return Math.sqrt(dx * dx + dz * dz);
    }

    startInteraction() {
        this.isInteracting = true;
        this.currentDialogueIndex = 0;

        // Highlight NPC (glow effect)
        if (this.mesh) {
            this.mesh.material.emissive = new THREE.Color(0x44ff44);
            this.mesh.material.emissiveIntensity = 0.3;
        }
    }

    endInteraction() {
        this.isInteracting = false;

        // Remove highlight
        if (this.mesh) {
            this.mesh.material.emissive = new THREE.Color(0x000000);
            this.mesh.material.emissiveIntensity = 0;
        }
    }

    getNextDialogue() {
        if (this.dialogue.length === 0) {
            return {
                text: "...",
                options: [{ text: "Tschüss", action: 'close' }]
            };
        }

        const current = this.dialogue[this.currentDialogueIndex];
        this.currentDialogueIndex = (this.currentDialogueIndex + 1) % this.dialogue.length;

        return current;
    }

    update(delta) {
        // Billboard nameplate (always face camera)
        if (this.nameplate && window.camera) {
            this.nameplate.lookAt(window.camera.position);
        }
    }
}

class NPCSystem {
    constructor(scene, THREE) {
        this.scene = scene;
        this.THREE = THREE;
        this.npcs = [];
        this.activeNPC = null; // Currently interacting NPC

        console.log('🧑 NPC-System initialisiert');
    }

    // ===== NPC TEMPLATES =====

    getNPCTemplates() {
        return {
            // ===== HANDELSFESTUNG NPCs =====
            'handelsfestung_arena_master': {
                name: 'Arena-Meister Takeshi',
                type: 'trainer',
                color: 0xff0000,
                dialogue: [
                    {
                        text: "Willkommen in der Arena! Bist du bereit für den Kampf?",
                        options: [
                            { text: "Ja, ich bin bereit!", action: 'start_arena' },
                            { text: "Noch nicht...", action: 'close' }
                        ]
                    },
                    {
                        text: "Die Arena ist der beste Ort um deine Kampffähigkeiten zu testen!",
                        options: [
                            { text: "Verstanden!", action: 'close' }
                        ]
                    }
                ],
                skills: ['heavy_strike', 'shield_bash', 'war_cry']
            },

            'handelsfestung_weapon_vendor': {
                name: 'Waffenhändler Gorou',
                type: 'vendor',
                color: 0x808080,
                shopType: 'weapons',
                dialogue: [
                    {
                        text: "Suchst du eine gute Waffe? Ich habe die besten!",
                        options: [
                            { text: "Zeig mir deine Waren!", action: 'open_shop' },
                            { text: "Vielleicht später", action: 'close' }
                        ]
                    }
                ],
                inventory: ['fire_sword', 'ice_dagger', 'lightning_staff', 'water_bow']
            },

            'handelsfestung_food_vendor': {
                name: 'Imbiss-Besitzer Hiro',
                type: 'vendor',
                color: 0xFFA500,
                shopType: 'food',
                dialogue: [
                    {
                        text: "🍖 Frisches Fleisch! Die besten Burger der Stadt!",
                        options: [
                            { text: "Ich hätte gerne etwas!", action: 'open_shop' },
                            { text: "Nein danke", action: 'close' }
                        ]
                    }
                ],
                inventory: ['champion_keule', 'arena_happen', 'dreh_braten', 'glut_steak', 'rauch_rippchen']
            },

            // ===== DAMPF-HAIN NPCs =====
            'dampf_hain_restaurant_owner': {
                name: 'Restaurant-Besitzerin Mei',
                type: 'vendor',
                color: 0x90EE90,
                shopType: 'food',
                dialogue: [
                    {
                        text: "🥟 Willkommen! Probiere unsere gedämpften Spezialitäten!",
                        options: [
                            { text: "Zeig mir die Speisekarte!", action: 'open_shop' },
                            { text: "Danke, später!", action: 'close' }
                        ]
                    }
                ],
                inventory: ['baozi', 'manju', 'dampfnudel']
            },

            'dampf_hain_druid': {
                name: 'Druide Kaito',
                type: 'quest_giver',
                color: 0x228B22,
                dialogue: [
                    {
                        text: "Der Wald spricht zu mir... Er braucht deine Hilfe.",
                        options: [
                            { text: "Was ist los?", action: 'next' }
                        ]
                    },
                    {
                        text: "Die alten Bäume verlieren ihre Magie. Bringe mir 5 Kristallscherben!",
                        options: [
                            { text: "Ich werde helfen!", action: 'accept_quest' },
                            { text: "Vielleicht später", action: 'close' }
                        ]
                    }
                ],
                quests: ['forest_secrets', 'nature_magic']
            },

            'dampf_hain_onsen_master': {
                name: 'Onsen-Meister Tanaka',
                type: 'citizen',
                color: 0x87CEEB,
                dialogue: [
                    {
                        text: "Ah, willkommen im Onsen! Das heiße Wasser hier heilt Körper und Seele.",
                        options: [
                            { text: "Danke für die Info!", action: 'close' }
                        ]
                    }
                ]
            },

            // ===== SALZIGE BUCHT NPCs =====
            'salzige_bucht_fish_vendor': {
                name: 'Fischer Ryuu',
                type: 'vendor',
                color: 0x00CED1,
                shopType: 'food',
                dialogue: [
                    {
                        text: "🐟 Frischer Fisch vom Meer! Heute besonders gut!",
                        options: [
                            { text: "Was hast du?", action: 'open_shop' },
                            { text: "Nein danke", action: 'close' }
                        ]
                    }
                ],
                inventory: ['salted_fish', 'premium_salted_fish']
            },

            'salzige_bucht_captain': {
                name: 'Kapitän Akira',
                type: 'quest_giver',
                color: 0x4169E1,
                dialogue: [
                    {
                        text: "Arrr! Suchst du Abenteuer auf hoher See?",
                        options: [
                            { text: "Was für Abenteuer?", action: 'next' }
                        ]
                    },
                    {
                        text: "Ich brauche jemanden der meinen Schatz vom Meeresgrund holt!",
                        options: [
                            { text: "Ich bin dabei!", action: 'accept_quest' },
                            { text: "Zu gefährlich...", action: 'close' }
                        ]
                    }
                ],
                quests: ['ocean_treasure']
            },

            'salzige_bucht_lighthouse_keeper': {
                name: 'Leuchtturm-Wächter Sora',
                type: 'citizen',
                color: 0xFFD700,
                dialogue: [
                    {
                        text: "Der Leuchtturm führt alle Schiffe sicher nach Hause.",
                        options: [
                            { text: "Interessant!", action: 'close' }
                        ]
                    }
                ]
            },

            // ===== RUNENHEIM NPCs =====
            'runenheim_mage_teacher': {
                name: 'Magier-Lehrerin Luna',
                type: 'trainer',
                color: 0x9370DB,
                dialogue: [
                    {
                        text: "Willst du die Geheimnisse der Magie lernen?",
                        options: [
                            { text: "Ja, bitte!", action: 'train_magic' },
                            { text: "Noch nicht", action: 'close' }
                        ]
                    }
                ],
                skills: ['fireball', 'ice_lance', 'lightning_bolt']
            },

            'runenheim_rune_vendor': {
                name: 'Runen-Verkäufer Zephyr',
                type: 'vendor',
                color: 0x8A2BE2,
                shopType: 'magic',
                dialogue: [
                    {
                        text: "Mächtige Runen für mächtige Krieger!",
                        options: [
                            { text: "Was hast du?", action: 'open_shop' },
                            { text: "Danke, nein", action: 'close' }
                        ]
                    }
                ],
                inventory: ['rune_of_strength', 'rune_of_wisdom', 'rune_of_speed']
            },

            // ===== FUNKEN-SIEDLUNG NPCs =====
            'funken_siedlung_master_smith': {
                name: 'Meister-Schmied Tetsu',
                type: 'vendor',
                color: 0xFF4500,
                shopType: 'weapons',
                dialogue: [
                    {
                        text: "🔨 Die besten Waffen werden hier geschmiedet!",
                        options: [
                            { text: "Zeig mir dein Handwerk!", action: 'open_shop' },
                            { text: "Später", action: 'close' }
                        ]
                    }
                ],
                inventory: ['steel_sword', 'iron_axe', 'master_blade']
            },

            'funken_siedlung_forge_worker': {
                name: 'Schmied Kenta',
                type: 'trainer',
                color: 0xCD5C5C,
                dialogue: [
                    {
                        text: "Willst du lernen wie man Waffen schmiedet?",
                        options: [
                            { text: "Ja!", action: 'train_smithing' },
                            { text: "Nein danke", action: 'close' }
                        ]
                    }
                ],
                skills: ['smithing', 'repair', 'enchanting']
            }
        };
    }

    // ===== NPC SPAWNING =====

    spawnNPCsForCity(cityId, cityData, interiorBounds) {
        const templates = this.getNPCTemplates();
        const spawned = [];

        // Determine which NPCs to spawn based on city
        let npcTypes = [];

        switch(cityId) {
            case 'handelsfestung':
                npcTypes = [
                    'handelsfestung_arena_master',
                    'handelsfestung_weapon_vendor',
                    'handelsfestung_food_vendor'
                ];
                break;

            case 'dampf_hain':
                npcTypes = [
                    'dampf_hain_restaurant_owner',
                    'dampf_hain_druid',
                    'dampf_hain_onsen_master'
                ];
                break;

            case 'salzige_bucht':
                npcTypes = [
                    'salzige_bucht_fish_vendor',
                    'salzige_bucht_captain',
                    'salzige_bucht_lighthouse_keeper'
                ];
                break;

            case 'runenheim':
                npcTypes = [
                    'runenheim_mage_teacher',
                    'runenheim_rune_vendor'
                ];
                break;

            case 'funken_siedlung':
                npcTypes = [
                    'funken_siedlung_master_smith',
                    'funken_siedlung_forge_worker'
                ];
                break;
        }

        // Spawn NPCs at random positions
        npcTypes.forEach((typeId, index) => {
            const template = templates[typeId];
            if (!template) return;

            // Random position within interior bounds
            const x = (Math.random() - 0.5) * (interiorBounds.width - 20);
            const z = (Math.random() - 0.5) * (interiorBounds.depth - 20);

            const npcData = {
                ...template,
                id: `${cityId}_${typeId}`,
                position: { x, y: 0, z }
            };

            const npc = new NPC(npcData);
            npc.createMesh(this.THREE, this.scene);

            this.npcs.push(npc);
            spawned.push(npc);

            console.log(`🧑 NPC spawned: ${npc.name} at (${x.toFixed(1)}, ${z.toFixed(1)})`);
        });

        return spawned;
    }

    // ===== NPC INTERACTION =====

    getNearestNPC(playerPosition, maxDistance = 3) {
        let nearest = null;
        let minDistance = maxDistance;

        for (const npc of this.npcs) {
            const distance = npc.getDistanceToPlayer(playerPosition);
            if (distance < minDistance) {
                minDistance = distance;
                nearest = npc;
            }
        }

        return nearest;
    }

    startInteraction(npc) {
        if (this.activeNPC) {
            this.endInteraction();
        }

        this.activeNPC = npc;
        npc.startInteraction();

        console.log(`💬 Started talking to: ${npc.name}`);
    }

    endInteraction() {
        if (this.activeNPC) {
            this.activeNPC.endInteraction();
            this.activeNPC = null;
        }
    }

    // ===== UPDATE =====

    update(delta) {
        for (const npc of this.npcs) {
            npc.update(delta);
        }
    }

    // ===== CLEANUP =====

    clearNPCs() {
        for (const npc of this.npcs) {
            if (npc.mesh) {
                this.scene.remove(npc.mesh);
                npc.mesh.geometry.dispose();
                npc.mesh.material.dispose();
            }
            if (npc.nameplate) {
                this.scene.remove(npc.nameplate);
                npc.nameplate.material.map.dispose();
                npc.nameplate.material.dispose();
            }
        }
        this.npcs = [];
        this.activeNPC = null;
        console.log('🧹 All NPCs cleared');
    }
}

// Export for global use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NPC, NPCSystem };
}
