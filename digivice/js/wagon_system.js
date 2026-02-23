/**
 * NAJIKA WAGON SYSTEM
 * ====================
 * Wagen als 3D-Entities die dem Spieler folgen.
 * Gezogen von Kreaturen/Sklaven (KEINE Pferde).
 *
 * Typen: Handkarren (Spieler zieht), Kleinwagen (1 Kreatur), Planwagen (2+)
 * Follow-Verhalten wie Companion (companion_3d.js pattern).
 *
 * Wagen beschaffen: Bauen, Kaufen, Mieten, Stehlen (Kopfgeld!).
 * Wagen sind lootbar nach Tod (Oregon Trail).
 */
(function() {
    'use strict';

    const STORAGE_KEY = 'najika_wagons';

    // ==========================================
    // WAGON TYPES
    // ==========================================

    const WAGON_TYPES = {
        handkarren: {
            name: 'Handkarren',
            capacity: 30,
            durability: 100,
            speedModifier: 0.85,
            pullRequirement: 0,
            modelScale: 0.8,
            price: 200,
            buildMaterials: { holz: 5, seil: 2 },
            rentPerDay: 15,
            color: 0x8B6914,
            size: { x: 0.8, y: 0.6, z: 1.2 },
            description: 'Kleiner Handkarren. Du ziehst ihn selbst.',
        },
        kleinwagen: {
            name: 'Kleinwagen',
            capacity: 80,
            durability: 200,
            speedModifier: 0.95,
            pullRequirement: 1,
            modelScale: 1.2,
            price: 800,
            buildMaterials: { holz: 15, erz: 3, seil: 5 },
            rentPerDay: 40,
            color: 0x654321,
            size: { x: 1.4, y: 0.8, z: 2.0 },
            description: 'Einspanner. Braucht eine Kreatur zum Ziehen.',
        },
        planwagen: {
            name: 'Planwagen',
            capacity: 200,
            durability: 350,
            speedModifier: 1.0,
            pullRequirement: 2,
            modelScale: 1.8,
            price: 2500,
            buildMaterials: { holz: 30, erz: 8, stoff: 10, seil: 8 },
            rentPerDay: 100,
            color: 0xD2B48C,
            size: { x: 2.0, y: 1.2, z: 3.0 },
            description: 'Grosser Planwagen mit Stoffdach. Braucht 2+ Kreaturen.',
        },
    };

    // ==========================================
    // STATE
    // ==========================================

    let wagons = [];
    let activeWagonId = null;
    let wagonMeshes = new Map(); // id -> THREE.Group
    let initialized = false;
    let lastUpdateTime = 0;

    // Follow parameters (from companion_3d.js pattern)
    const FOLLOW_DISTANCE = 5.0;
    const FOLLOW_SPEED = 4.0;
    const CATCH_UP_SPEED = 7.0;
    const MAX_DISTANCE = 20;
    const ROTATION_SPEED = 4.0;

    // ==========================================
    // PERSISTENCE
    // ==========================================

    function save() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                wagons: wagons.map(w => ({
                    ...w,
                    // Don't save 3D mesh references
                })),
                activeWagonId,
            }));
        } catch (e) {}
    }

    function load() {
        try {
            const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
            if (data) {
                wagons = data.wagons || [];
                activeWagonId = data.activeWagonId || null;
            }
        } catch (e) {
            wagons = [];
            activeWagonId = null;
        }
    }

    // ==========================================
    // WAGON CRUD
    // ==========================================

    function generateId() {
        return 'wagon_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6);
    }

    function createWagon(type, method) {
        const wType = WAGON_TYPES[type];
        if (!wType) return { success: false, error: 'Unbekannter Wagentyp: ' + type };

        // Method: buy, build, rent, steal
        method = method || 'buy';

        if (method === 'buy') {
            const gold = window.InventoryV2?.getGold?.() || 0;
            if (gold < wType.price) {
                return { success: false, error: `Nicht genug Gold! Brauche ${wType.price}G, habe ${gold}G` };
            }
            if (window.InventoryV2?.addGold) {
                window.InventoryV2.addGold(-wType.price);
            }
        } else if (method === 'build') {
            // Check materials
            const inv = window.InventoryV2;
            if (!inv) return { success: false, error: 'Kein Inventar-System' };
            const items = inv.getItems ? inv.getItems() : [];
            for (const [matId, amount] of Object.entries(wType.buildMaterials)) {
                const have = items.filter(i => i.id === matId).reduce((sum, i) => sum + (i.count || 1), 0);
                if (have < amount) {
                    return { success: false, error: `Fehlt: ${amount - have}x ${matId}` };
                }
            }
            // Remove materials (simplified: just log it, real removal needs item-by-item)
            console.log(`[WAGON] Materialien verbraucht für ${wType.name}`);
        } else if (method === 'steal') {
            // Add bounty!
            if (window.player) {
                window.player.bounty = (window.player.bounty || 0) + Math.floor(wType.price * 0.5);
                console.log(`[WAGON] GESTOHLEN! Kopfgeld: +${Math.floor(wType.price * 0.5)}G`);
            }
        }

        const playerPos = window.Scene3D?.characterGroup?.position;
        const pos = playerPos
            ? { x: playerPos.x - 3, y: playerPos.y || 0, z: playerPos.z - 3 }
            : { x: 0, y: 0, z: 0 };

        const wagon = {
            id: generateId(),
            type,
            items: [],
            currentWeight: 0,
            durability: wType.durability,
            maxDurability: wType.durability,
            pullers: [],
            driver: null,
            ownerId: 'player',
            position: pos,
            region: window.RegionStreamingV2?.getCurrentRegion?.() || 'unbekannt',
            isActive: false,
            isAbandoned: false,
            method,
            isRented: method === 'rent',
            rentDaysLeft: method === 'rent' ? 3 : 0,
        };

        wagons.push(wagon);
        save();

        if (window.QuestTrackerV2?.showNotification) {
            window.QuestTrackerV2.showNotification(
                'WAGEN ERHALTEN',
                `${wType.name} (${method === 'buy' ? 'gekauft' : method === 'build' ? 'gebaut' : method === 'steal' ? 'GESTOHLEN!' : 'gemietet'})`,
                method === 'steal' ? '#F44336' : '#4CAF50'
            );
        }

        console.log(`[WAGON] ${wType.name} erstellt via ${method}`);
        return { success: true, wagon };
    }

    function activateWagon(wagonId) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return { success: false, error: 'Wagen nicht gefunden' };
        if (wagon.isAbandoned) return { success: false, error: 'Wagen ist aufgegeben' };

        const wType = WAGON_TYPES[wagon.type];
        if (!wType) return { success: false, error: 'Unbekannter Typ' };

        // Check pull requirements
        if (wType.pullRequirement > 0 && wagon.pullers.length < wType.pullRequirement) {
            return {
                success: false,
                error: `Braucht ${wType.pullRequirement} Zugtier(e), hat ${wagon.pullers.length}!`
            };
        }

        // Deactivate current
        if (activeWagonId) {
            deactivateWagon(activeWagonId);
        }

        wagon.isActive = true;
        activeWagonId = wagonId;

        // Spawn 3D mesh
        spawnWagonMesh(wagon);

        save();
        console.log(`[WAGON] ${wType.name} aktiviert`);
        return { success: true };
    }

    function deactivateWagon(wagonId) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return;

        wagon.isActive = false;

        // Save position
        const mesh = wagonMeshes.get(wagonId);
        if (mesh) {
            wagon.position = { x: mesh.position.x, y: mesh.position.y, z: mesh.position.z };
        }

        // Remove mesh
        removeWagonMesh(wagonId);

        if (activeWagonId === wagonId) activeWagonId = null;
        save();
    }

    function abandonWagon(wagonId) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return;

        deactivateWagon(wagonId);
        wagon.isAbandoned = true;

        // Create wreck in world
        if (window.WorldItems?.createWagonWreck) {
            window.WorldItems.createWagonWreck(wagon, wagon.position, wagon.region);
        }

        // Remove from our list
        wagons = wagons.filter(w => w.id !== wagonId);
        save();
    }

    // ==========================================
    // CARGO
    // ==========================================

    function addToWagon(wagonId, item) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return { success: false, error: 'Wagen nicht gefunden' };

        const wType = WAGON_TYPES[wagon.type];
        const itemWeight = (item.weight || 0) * (item.count || 1);

        if (wagon.currentWeight + itemWeight > wType.capacity) {
            return { success: false, error: `Wagen zu voll! ${wagon.currentWeight}/${wType.capacity}kg` };
        }

        wagon.items.push(item);
        wagon.currentWeight += itemWeight;
        save();
        return { success: true };
    }

    function removeFromWagon(wagonId, itemIndex) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon || itemIndex < 0 || itemIndex >= wagon.items.length) {
            return { success: false, error: 'Ungueltig' };
        }

        const item = wagon.items[itemIndex];
        const itemWeight = (item.weight || 0) * (item.count || 1);

        // Weight check for player inventory
        if (window.WeightSystem && !window.WeightSystem.canPickUp(itemWeight)) {
            return { success: false, error: 'Spieler zu schwer beladen!' };
        }

        wagon.items.splice(itemIndex, 1);
        wagon.currentWeight = Math.max(0, wagon.currentWeight - itemWeight);

        // Add to player inventory
        if (window.InventoryV2?.addItem) {
            window.InventoryV2.addItem(item);
        }

        save();
        return { success: true, item };
    }

    // ==========================================
    // PULLERS & DRIVER
    // ==========================================

    function assignPuller(wagonId, creatureId) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return { success: false, error: 'Wagen nicht gefunden' };

        // Check creature is available
        const ct = window.CreatureTaming;
        if (ct?.isAvailableForPulling && !ct.isAvailableForPulling(creatureId)) {
            return { success: false, error: 'Kreatur nicht verfuegbar (gerade gemountet oder kein Lasttier)' };
        }

        if (wagon.pullers.includes(creatureId)) {
            return { success: false, error: 'Kreatur zieht bereits diesen Wagen' };
        }

        wagon.pullers.push(creatureId);
        save();
        return { success: true };
    }

    function removePuller(wagonId, creatureId) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return;

        wagon.pullers = wagon.pullers.filter(id => id !== creatureId);
        save();
    }

    function assignDriver(wagonId, recruitId) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return { success: false, error: 'Wagen nicht gefunden' };

        wagon.driver = recruitId;
        save();
        return { success: true };
    }

    function isPlayerPulling() {
        if (!activeWagonId) return false;
        const wagon = wagons.find(w => w.id === activeWagonId);
        if (!wagon || !wagon.isActive) return false;

        const wType = WAGON_TYPES[wagon.type];
        // Player pulls if: pullRequirement is 0 (handkarren) OR no creatures assigned
        return wType.pullRequirement === 0 || wagon.pullers.length === 0;
    }

    function getActiveWagon() {
        if (!activeWagonId) return null;
        return wagons.find(w => w.id === activeWagonId) || null;
    }

    // ==========================================
    // 3D MESH
    // ==========================================

    function spawnWagonMesh(wagon) {
        if (typeof THREE === 'undefined') return;

        const wType = WAGON_TYPES[wagon.type];
        if (!wType) return;

        const group = new THREE.Group();
        group.userData.wagonId = wagon.id;

        // Body
        const bodyGeo = new THREE.BoxGeometry(wType.size.x, wType.size.y, wType.size.z);
        const bodyMat = new THREE.MeshStandardMaterial({
            color: wType.color, roughness: 0.8, metalness: 0.1
        });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.position.y = wType.size.y / 2 + 0.3; // Above wheels
        group.add(body);

        // Wheels (4 for larger, 2 for handkarren)
        const wheelCount = wagon.type === 'handkarren' ? 2 : 4;
        const wheelGeo = new THREE.CylinderGeometry(0.25, 0.25, 0.08, 12);
        const wheelMat = new THREE.MeshStandardMaterial({ color: 0x3E2723 });

        const wheelPositions = wagon.type === 'handkarren'
            ? [[-wType.size.x/2 - 0.1, 0.25, 0], [wType.size.x/2 + 0.1, 0.25, 0]]
            : [
                [-wType.size.x/2 - 0.1, 0.25, -wType.size.z/3],
                [wType.size.x/2 + 0.1, 0.25, -wType.size.z/3],
                [-wType.size.x/2 - 0.1, 0.25, wType.size.z/3],
                [wType.size.x/2 + 0.1, 0.25, wType.size.z/3],
            ];

        wheelPositions.forEach(([x, y, z]) => {
            const wheel = new THREE.Mesh(wheelGeo, wheelMat);
            wheel.position.set(x, y, z);
            wheel.rotation.z = Math.PI / 2;
            group.add(wheel);
        });

        // Canvas top for planwagen
        if (wagon.type === 'planwagen') {
            const topGeo = new THREE.BoxGeometry(wType.size.x * 1.1, 0.05, wType.size.z * 0.9);
            const topMat = new THREE.MeshStandardMaterial({ color: 0xF5F5DC, roughness: 0.9 });
            const top = new THREE.Mesh(topGeo, topMat);
            top.position.y = wType.size.y + 0.6;
            group.add(top);

            // Support arcs
            for (let i = -1; i <= 1; i++) {
                const arcGeo = new THREE.TorusGeometry(0.5, 0.02, 4, 8, Math.PI);
                const arcMat = new THREE.MeshStandardMaterial({ color: 0x8B6914 });
                const arc = new THREE.Mesh(arcGeo, arcMat);
                arc.position.set(0, wType.size.y * 0.5 + 0.3, i * wType.size.z * 0.3);
                arc.rotation.y = Math.PI / 2;
                group.add(arc);
            }
        }

        // Handle for handkarren
        if (wagon.type === 'handkarren') {
            const handleGeo = new THREE.CylinderGeometry(0.03, 0.03, 1.2, 4);
            const handleMat = new THREE.MeshStandardMaterial({ color: 0x8B6914 });
            const handle = new THREE.Mesh(handleGeo, handleMat);
            handle.rotation.x = Math.PI / 4;
            handle.position.set(0, 0.6, -wType.size.z / 2 - 0.4);
            group.add(handle);
        }

        // Set initial position
        const groundY = window.getGroundHeight
            ? window.getGroundHeight(wagon.position.x, wagon.position.z)
            : (wagon.position.y || 0);
        group.position.set(wagon.position.x, groundY, wagon.position.z);

        const scene = window.Scene3D?.scene;
        if (scene) {
            scene.add(group);
            wagonMeshes.set(wagon.id, group);
        }
    }

    function removeWagonMesh(wagonId) {
        const mesh = wagonMeshes.get(wagonId);
        if (!mesh) return;

        mesh.traverse(child => {
            if (child.geometry) child.geometry.dispose();
            if (child.material) child.material.dispose();
        });

        const scene = window.Scene3D?.scene;
        if (scene) scene.remove(mesh);
        wagonMeshes.delete(wagonId);
    }

    // ==========================================
    // FOLLOW LOGIC (from companion_3d.js)
    // ==========================================

    function updateFollow(delta) {
        if (!activeWagonId) return;

        const wagon = wagons.find(w => w.id === activeWagonId);
        if (!wagon || !wagon.isActive) return;

        const mesh = wagonMeshes.get(activeWagonId);
        if (!mesh) return;

        const playerPos = window.Scene3D?.characterGroup?.position;
        const playerHeading = window.Scene3D?.characterGroup?.rotation?.y ?? 0;
        if (!playerPos) return;

        // Target position: behind player
        const targetX = playerPos.x + Math.sin(playerHeading + Math.PI) * FOLLOW_DISTANCE;
        const targetZ = playerPos.z + Math.cos(playerHeading + Math.PI) * FOLLOW_DISTANCE;

        const dx = targetX - mesh.position.x;
        const dz = targetZ - mesh.position.z;
        const dist = Math.sqrt(dx * dx + dz * dz);

        if (dist > MAX_DISTANCE) {
            // Teleport
            mesh.position.x = targetX;
            mesh.position.z = targetZ;
        } else if (dist > 0.5) {
            // Move toward target
            const speed = dist > FOLLOW_DISTANCE * 1.5 ? CATCH_UP_SPEED : FOLLOW_SPEED;
            const step = Math.min(speed * delta, dist);
            mesh.position.x += (dx / dist) * step;
            mesh.position.z += (dz / dist) * step;

            // Rotate to face movement direction
            const targetRot = Math.atan2(dx, dz);
            let rotDiff = targetRot - mesh.rotation.y;
            while (rotDiff > Math.PI) rotDiff -= Math.PI * 2;
            while (rotDiff < -Math.PI) rotDiff += Math.PI * 2;
            mesh.rotation.y += rotDiff * ROTATION_SPEED * delta;
        }

        // Ground height
        const groundY = window.getGroundHeight
            ? window.getGroundHeight(mesh.position.x, mesh.position.z)
            : 0;
        mesh.position.y = groundY;

        // Save position
        wagon.position = { x: mesh.position.x, y: mesh.position.y, z: mesh.position.z };
    }

    // ==========================================
    // DURABILITY & DAMAGE
    // ==========================================

    function damageWagon(wagonId, amount) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return;

        wagon.durability = Math.max(0, wagon.durability - amount);

        if (wagon.durability <= 0) {
            console.log(`[WAGON] ${WAGON_TYPES[wagon.type]?.name} zerstoert!`);
            abandonWagon(wagonId);

            if (window.QuestTrackerV2?.showNotification) {
                window.QuestTrackerV2.showNotification('WAGEN ZERSTOERT', 'Dein Wagen ist kaputt gegangen!', '#F44336');
            }
        }

        save();
    }

    function repairWagon(wagonId, amount) {
        const wagon = wagons.find(w => w.id === wagonId);
        if (!wagon) return;

        wagon.durability = Math.min(wagon.maxDurability, wagon.durability + (amount || 50));
        save();
    }

    // ==========================================
    // UPDATE LOOP
    // ==========================================

    let animFrameId = null;

    function startUpdateLoop() {
        let lastTime = performance.now();

        function loop(now) {
            const delta = (now - lastTime) / 1000;
            lastTime = now;

            if (delta < 0.5) { // Skip huge deltas
                updateFollow(delta);
            }

            animFrameId = requestAnimationFrame(loop);
        }

        animFrameId = requestAnimationFrame(loop);
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        if (initialized) return;
        initialized = true;

        load();

        // Respawn active wagon mesh
        if (activeWagonId) {
            const wagon = wagons.find(w => w.id === activeWagonId);
            if (wagon && wagon.isActive) {
                // Delay to ensure 3D scene is ready
                setTimeout(() => spawnWagonMesh(wagon), 2000);
            }
        }

        startUpdateLoop();
        console.log(`[OK] WagonSystem geladen: ${wagons.length} Wagen`);
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.WagonSystem = {
        init,
        WAGON_TYPES,
        createWagon,
        activateWagon,
        deactivateWagon,
        abandonWagon,
        addToWagon,
        removeFromWagon,
        assignPuller,
        removePuller,
        assignDriver,
        isPlayerPulling,
        getActiveWagon,
        getWagons: () => [...wagons],
        getWagonById: (id) => wagons.find(w => w.id === id),
        damageWagon,
        repairWagon,
        abandonAllWagons: () => {
            wagons.forEach(w => {
                if (w.isActive) deactivateWagon(w.id);
                w.isAbandoned = true;
                if (window.WorldItems?.createWagonWreck) {
                    window.WorldItems.createWagonWreck(w, w.position, w.region);
                }
            });
            wagons = [];
            activeWagonId = null;
            save();
        },
    };

    console.log('[OK] WagonSystem geladen');
})();
