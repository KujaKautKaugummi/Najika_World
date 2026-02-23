/**
 * NAJIKA WORLD ITEMS SYSTEM
 * ==========================
 * Persistente Items in der 3D-Welt.
 * - Gedropte Items (Spieler wirft weg)
 * - Leichenhaufen (Oregon Trail Tod)
 * - Wagen-Wracks (zerstoerte/aufgegebene Wagen)
 *
 * Max 50 World-Items, max 20 sichtbare Meshes.
 * Decay nach 7 Spieltagen.
 */
(function() {
    'use strict';

    const STORAGE_KEY = 'najika_world_items';
    const MAX_WORLD_ITEMS = 50;
    const MAX_VISIBLE_MESHES = 20;
    const RENDER_DISTANCE = 100;
    const INTERACTION_DISTANCE = 3;
    const DECAY_DAYS = 7;

    let worldItems = [];
    let activeMeshes = new Map(); // id -> THREE.Group
    let initialized = false;
    let lootPromptEl = null;
    let nearestLootable = null;

    // ==========================================
    // PERSISTENCE
    // ==========================================

    function save() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(worldItems));
        } catch (e) { /* quota exceeded - remove oldest */
            if (worldItems.length > 10) {
                worldItems = worldItems.slice(-10);
                try { localStorage.setItem(STORAGE_KEY, JSON.stringify(worldItems)); } catch(e2) {}
            }
        }
    }

    function load() {
        try {
            const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
            if (Array.isArray(data)) worldItems = data;
        } catch (e) { worldItems = []; }
    }

    // ==========================================
    // CREATE WORLD ITEMS
    // ==========================================

    function generateId() {
        return 'wi_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6);
    }

    function getPlayerRegion() {
        return window.RegionStreamingV2?.getCurrentRegion?.()
            || window.BiomeSystem?.getCurrentBiome?.()
            || 'unbekannt';
    }

    function dropItems(items, position, region) {
        if (!items || items.length === 0) return null;

        const worldItem = {
            id: generateId(),
            type: 'item',
            items: items,
            gold: 0,
            position: { x: position.x, y: position.y || 0, z: position.z },
            region: region || getPlayerRegion(),
            createdAt: Date.now(),
            decayDays: DECAY_DAYS,
        };

        addWorldItem(worldItem);
        return worldItem;
    }

    function createCorpsePile(items, gold, equipment, position, region) {
        // Merge equipment into items
        const allItems = [...(items || [])];
        if (equipment && typeof equipment === 'object') {
            Object.values(equipment).forEach(eq => {
                if (eq) allItems.push(eq);
            });
        }

        const worldItem = {
            id: generateId(),
            type: 'corpse_pile',
            items: allItems,
            gold: gold || 0,
            position: { x: position.x, y: position.y || 0, z: position.z },
            region: region || getPlayerRegion(),
            createdAt: Date.now(),
            decayDays: DECAY_DAYS,
        };

        addWorldItem(worldItem);
        console.log(`[WORLD ITEMS] Leichenhaufen erstellt: ${allItems.length} Items, ${gold}G bei ${worldItem.region}`);
        return worldItem;
    }

    function createWagonWreck(wagonData, position, region) {
        const worldItem = {
            id: generateId(),
            type: 'wagon_wreck',
            items: wagonData.items || [],
            gold: 0,
            wagonType: wagonData.type || 'handkarren',
            position: { x: position.x, y: position.y || 0, z: position.z },
            region: region || getPlayerRegion(),
            createdAt: Date.now(),
            decayDays: DECAY_DAYS * 2, // Wrecks last longer
        };

        addWorldItem(worldItem);
        console.log(`[WORLD ITEMS] Wagen-Wrack erstellt: ${wagonData.type} bei ${worldItem.region}`);
        return worldItem;
    }

    function addWorldItem(item) {
        worldItems.push(item);

        // Enforce max limit - remove oldest
        while (worldItems.length > MAX_WORLD_ITEMS) {
            const removed = worldItems.shift();
            removeMesh(removed.id);
        }

        save();

        if (window.GameEvents) {
            window.GameEvents.emit('worldItemDropped', { item });
        }
    }

    // ==========================================
    // LOOTING
    // ==========================================

    function lootWorldItem(worldItemId, itemIndex) {
        const wi = worldItems.find(w => w.id === worldItemId);
        if (!wi || !wi.items) return { success: false, error: 'Nicht gefunden' };

        // Loot single item
        if (typeof itemIndex === 'number') {
            if (itemIndex < 0 || itemIndex >= wi.items.length) {
                return { success: false, error: 'Ungültiger Index' };
            }

            const item = wi.items[itemIndex];
            const weight = (item.weight || 0) * (item.count || 1);

            if (window.WeightSystem && !window.WeightSystem.canPickUp(weight)) {
                return { success: false, error: 'Zu schwer!' };
            }

            // Add to inventory
            if (window.InventoryV2?.addItem) {
                const added = window.InventoryV2.addItem(item);
                if (added === false) return { success: false, error: 'Zu schwer!' };
            }

            wi.items.splice(itemIndex, 1);
        } else {
            // Loot all (try each item)
            const taken = [];
            const left = [];

            for (const item of wi.items) {
                const weight = (item.weight || 0) * (item.count || 1);
                if (window.WeightSystem && !window.WeightSystem.canPickUp(weight)) {
                    left.push(item);
                    continue;
                }
                if (window.InventoryV2?.addItem) {
                    const added = window.InventoryV2.addItem(item);
                    if (added === false) { left.push(item); continue; }
                }
                taken.push(item);
            }

            wi.items = left;
        }

        // Take gold
        if (wi.gold > 0) {
            if (window.InventoryV2?.addGold) {
                window.InventoryV2.addGold(wi.gold);
            }
            wi.gold = 0;
        }

        // Remove if empty
        if (wi.items.length === 0 && wi.gold <= 0) {
            removeMesh(wi.id);
            worldItems = worldItems.filter(w => w.id !== wi.id);

            if (window.GameEvents) {
                window.GameEvents.emit('worldItemLooted', { id: wi.id });
            }
        }

        save();
        return { success: true };
    }

    // ==========================================
    // 3D MESHES
    // ==========================================

    function createMeshForItem(wi) {
        if (typeof THREE === 'undefined') return null;

        const group = new THREE.Group();
        group.userData.worldItemId = wi.id;

        let mesh;
        switch (wi.type) {
            case 'corpse_pile': {
                // Skull-like sphere + red glow
                const geo = new THREE.SphereGeometry(0.4, 8, 6);
                const mat = new THREE.MeshStandardMaterial({
                    color: 0x8B4513, emissive: 0xFF0000, emissiveIntensity: 0.3,
                    roughness: 0.8
                });
                mesh = new THREE.Mesh(geo, mat);

                // Cross bones
                const boneGeo = new THREE.CylinderGeometry(0.03, 0.03, 0.6, 4);
                const boneMat = new THREE.MeshStandardMaterial({ color: 0xE0D0B0 });
                const bone1 = new THREE.Mesh(boneGeo, boneMat);
                bone1.rotation.z = Math.PI / 4;
                bone1.position.y = -0.1;
                const bone2 = new THREE.Mesh(boneGeo, boneMat);
                bone2.rotation.z = -Math.PI / 4;
                bone2.position.y = -0.1;
                group.add(bone1, bone2);

                // Light
                const light = new THREE.PointLight(0xFF4444, 0.5, 5);
                light.position.y = 0.5;
                group.add(light);
                break;
            }
            case 'wagon_wreck': {
                // Large broken box
                const geo = new THREE.BoxGeometry(2, 1, 1.5);
                const mat = new THREE.MeshStandardMaterial({
                    color: 0x654321, roughness: 0.9
                });
                mesh = new THREE.Mesh(geo, mat);
                mesh.position.y = 0.5;

                // Broken wheel
                const wheelGeo = new THREE.TorusGeometry(0.35, 0.05, 6, 12);
                const wheelMat = new THREE.MeshStandardMaterial({ color: 0x3E2723 });
                const wheel = new THREE.Mesh(wheelGeo, wheelMat);
                wheel.position.set(0.8, 0.2, 0.8);
                wheel.rotation.x = Math.PI / 6;
                group.add(wheel);
                break;
            }
            default: {
                // Small glowing box
                const geo = new THREE.BoxGeometry(0.3, 0.3, 0.3);
                const mat = new THREE.MeshStandardMaterial({
                    color: 0xFFD700, emissive: 0xFFD700, emissiveIntensity: 0.5,
                    transparent: true, opacity: 0.8
                });
                mesh = new THREE.Mesh(geo, mat);
                mesh.position.y = 0.5;

                // Point light
                const light = new THREE.PointLight(0xFFD700, 0.4, 4);
                light.position.y = 0.7;
                group.add(light);
                break;
            }
        }

        if (mesh) group.add(mesh);

        // Label sprite
        const label = createLabel(wi);
        if (label) {
            label.position.y = wi.type === 'wagon_wreck' ? 2.0 : 1.2;
            group.add(label);
        }

        // Position
        const groundY = window.getGroundHeight
            ? window.getGroundHeight(wi.position.x, wi.position.z)
            : (wi.position.y || 0);
        group.position.set(wi.position.x, groundY, wi.position.z);

        return group;
    }

    function createLabel(wi) {
        if (typeof THREE === 'undefined') return null;

        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = 'rgba(0,0,0,0.6)';
        ctx.fillRect(0, 0, 256, 64);

        ctx.font = 'bold 20px monospace';
        ctx.textAlign = 'center';

        switch (wi.type) {
            case 'corpse_pile':
                ctx.fillStyle = '#FF4444';
                ctx.fillText('LEICHENHAUFEN', 128, 25);
                ctx.font = '14px monospace';
                ctx.fillStyle = '#FFD700';
                ctx.fillText(`${wi.items.length} Items | ${wi.gold}G`, 128, 48);
                break;
            case 'wagon_wreck':
                ctx.fillStyle = '#FF9800';
                ctx.fillText('WAGEN-WRACK', 128, 25);
                ctx.font = '14px monospace';
                ctx.fillStyle = '#aaa';
                ctx.fillText(`${wi.items.length} Items`, 128, 48);
                break;
            default:
                ctx.fillStyle = '#FFD700';
                ctx.fillText('LOOT', 128, 25);
                ctx.font = '14px monospace';
                ctx.fillStyle = '#aaa';
                ctx.fillText(`${wi.items.length} Items`, 128, 48);
        }

        const texture = new THREE.CanvasTexture(canvas);
        const mat = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(mat);
        sprite.scale.set(2, 0.5, 1);
        return sprite;
    }

    function removeMesh(id) {
        const mesh = activeMeshes.get(id);
        if (!mesh) return;

        mesh.traverse(child => {
            if (child.geometry) child.geometry.dispose();
            if (child.material) {
                if (child.material.map) child.material.map.dispose();
                child.material.dispose();
            }
        });

        const scene = window.Scene3D?.scene;
        if (scene) scene.remove(mesh);
        activeMeshes.delete(id);
    }

    // ==========================================
    // LOOT PROMPT UI
    // ==========================================

    function showLootPrompt(wi) {
        if (!lootPromptEl) {
            lootPromptEl = document.createElement('div');
            lootPromptEl.id = 'world-item-loot-prompt';
            lootPromptEl.style.cssText = `
                position:fixed; bottom:120px; left:50%; transform:translateX(-50%);
                background:rgba(0,0,0,0.85); border:1px solid #FFD700;
                padding:10px 20px; border-radius:8px; z-index:8000;
                font-family:'Courier New',monospace; color:#FFD700;
                text-align:center; pointer-events:none;
            `;
            document.body.appendChild(lootPromptEl);
        }

        const typeNames = {
            corpse_pile: 'LEICHENHAUFEN',
            wagon_wreck: 'WAGEN-WRACK',
            item: 'LOOT'
        };

        lootPromptEl.innerHTML = `
            <div style="font-size:14px; font-weight:bold;">${typeNames[wi.type] || 'LOOT'}</div>
            <div style="font-size:11px; color:#aaa; margin-top:4px;">
                ${wi.items.length} Items${wi.gold > 0 ? ` | ${wi.gold}G` : ''}
            </div>
            <div style="font-size:12px; color:#4CAF50; margin-top:6px;">
                [E] Looten
            </div>
        `;
        lootPromptEl.style.display = 'block';
    }

    function hideLootPrompt() {
        if (lootPromptEl) lootPromptEl.style.display = 'none';
        nearestLootable = null;
    }

    // ==========================================
    // LOOT UI (when E pressed)
    // ==========================================

    function openLootUI(wi) {
        const existing = document.getElementById('world-item-loot-ui');
        if (existing) existing.remove();

        const panel = document.createElement('div');
        panel.id = 'world-item-loot-ui';
        panel.style.cssText = `
            position:fixed; top:50%; left:50%; transform:translate(-50%,-50%);
            background:rgba(10,10,20,0.97); border:1px solid #FFD700;
            padding:20px; border-radius:10px; z-index:9000;
            font-family:'Courier New',monospace; color:#e0e0e0;
            min-width:300px; max-width:450px; max-height:70vh; overflow-y:auto;
        `;

        function renderLootItems() {
            const freshWi = worldItems.find(w => w.id === wi.id);
            if (!freshWi || (freshWi.items.length === 0 && freshWi.gold <= 0)) {
                panel.remove();
                return;
            }

            let html = `
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;">
                    <span style="color:#FFD700;font-size:16px;font-weight:bold;">LOOT</span>
                    <button onclick="document.getElementById('world-item-loot-ui').remove()"
                        style="background:#c0392b;border:none;color:white;padding:4px 10px;border-radius:4px;cursor:pointer;font-family:inherit;">X</button>
                </div>
            `;

            if (freshWi.gold > 0) {
                html += `<div onclick="window.WorldItems._lootGold('${freshWi.id}')"
                    style="padding:8px;margin-bottom:4px;background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.3);
                    border-radius:6px;cursor:pointer;display:flex;justify-content:space-between;">
                    <span style="color:#FFD700;">Gold</span>
                    <span style="color:#FFD700;font-weight:bold;">${freshWi.gold}G</span>
                </div>`;
            }

            freshWi.items.forEach((item, idx) => {
                const w = (item.weight || 0) * (item.count || 1);
                const canTake = !window.WeightSystem || window.WeightSystem.canPickUp(w);
                html += `<div onclick="${canTake ? `window.WorldItems._lootOne('${freshWi.id}',${idx})` : ''}"
                    style="padding:8px;margin-bottom:3px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                    border-radius:4px;cursor:${canTake ? 'pointer' : 'not-allowed'};display:flex;justify-content:space-between;
                    opacity:${canTake ? 1 : 0.4};">
                    <span>${item.icon || ''} ${item.name || item.id}${item.count > 1 ? ' x' + item.count : ''}</span>
                    <span style="color:#888;font-size:10px;">${w > 0 ? w.toFixed(1) + 'kg' : ''}</span>
                </div>`;
            });

            const ws = window.WeightSystem?.getStatus?.();
            if (ws) {
                html += `<div style="margin-top:10px;font-size:10px;color:${ws.color};">
                    Gewicht: ${ws.current}/${ws.max} (${ws.label})
                </div>`;
            }

            html += `<button onclick="window.WorldItems._lootAll('${freshWi.id}')"
                style="width:100%;margin-top:10px;padding:8px;background:rgba(76,175,80,0.2);border:1px solid rgba(76,175,80,0.4);
                color:#4CAF50;border-radius:6px;cursor:pointer;font-family:inherit;font-weight:bold;">
                ALLES nehmen
            </button>`;

            panel.innerHTML = html;
        }

        renderLootItems();
        document.body.appendChild(panel);

        // Re-render after each loot action
        window._refreshLootUI = renderLootItems;
    }

    // ==========================================
    // UPDATE LOOP
    // ==========================================

    function update() {
        if (typeof THREE === 'undefined') return;

        const scene = window.Scene3D?.scene;
        const playerPos = window.Scene3D?.characterGroup?.position;
        if (!scene || !playerPos) return;

        // Check decay
        const now = Date.now();
        const dayMs = 86400000; // 24h real time = 1 game day (simplified)
        worldItems = worldItems.filter(wi => {
            const age = (now - wi.createdAt) / dayMs;
            if (age > wi.decayDays) {
                removeMesh(wi.id);
                if (window.GameEvents) {
                    window.GameEvents.emit('worldItemDecayed', { id: wi.id });
                }
                return false;
            }
            return true;
        });

        // Manage meshes: show nearby, hide far
        let visibleCount = 0;
        let closest = null;
        let closestDist = Infinity;

        for (const wi of worldItems) {
            const dx = wi.position.x - playerPos.x;
            const dz = wi.position.z - playerPos.z;
            const dist = Math.sqrt(dx * dx + dz * dz);

            if (dist < RENDER_DISTANCE && visibleCount < MAX_VISIBLE_MESHES) {
                // Show mesh
                if (!activeMeshes.has(wi.id)) {
                    const mesh = createMeshForItem(wi);
                    if (mesh) {
                        scene.add(mesh);
                        activeMeshes.set(wi.id, mesh);
                    }
                }

                // Bounce animation for item type
                const mesh = activeMeshes.get(wi.id);
                if (mesh && wi.type === 'item') {
                    mesh.position.y = (wi.position.y || 0) + 0.2 + Math.sin(now * 0.003) * 0.15;
                }

                visibleCount++;

                // Track closest for interaction
                if (dist < INTERACTION_DISTANCE && dist < closestDist) {
                    closest = wi;
                    closestDist = dist;
                }
            } else {
                // Too far - remove mesh
                if (activeMeshes.has(wi.id)) {
                    removeMesh(wi.id);
                }
            }
        }

        // Interaction prompt
        if (closest) {
            nearestLootable = closest;
            showLootPrompt(closest);
        } else {
            hideLootPrompt();
        }

        save();
    }

    // ==========================================
    // INPUT HANDLER
    // ==========================================

    function handleInput(e) {
        if (e.key === 'e' || e.key === 'E') {
            if (document.activeElement?.tagName === 'INPUT' || document.activeElement?.tagName === 'TEXTAREA') return;
            if (nearestLootable) {
                e.preventDefault();
                openLootUI(nearestLootable);
            }
        }
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        if (initialized) return;
        initialized = true;

        load();
        document.addEventListener('keydown', handleInput);

        // Update every 500ms
        setInterval(update, 500);

        console.log(`[OK] WorldItems geladen: ${worldItems.length} Items in der Welt`);
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.WorldItems = {
        init,
        dropItems,
        createCorpsePile,
        createWagonWreck,
        lootWorldItem,
        getWorldItems: () => [...worldItems],
        getWorldItemById: (id) => worldItems.find(w => w.id === id),
        removeWorldItem: (id) => {
            removeMesh(id);
            worldItems = worldItems.filter(w => w.id !== id);
            save();
        },

        // UI callbacks
        _lootOne: (wiId, idx) => {
            lootWorldItem(wiId, idx);
            if (window._refreshLootUI) window._refreshLootUI();
        },
        _lootAll: (wiId) => {
            lootWorldItem(wiId);
            if (window._refreshLootUI) window._refreshLootUI();
        },
        _lootGold: (wiId) => {
            const wi = worldItems.find(w => w.id === wiId);
            if (wi && wi.gold > 0) {
                if (window.InventoryV2?.addGold) window.InventoryV2.addGold(wi.gold);
                wi.gold = 0;
                save();
            }
            if (window._refreshLootUI) window._refreshLootUI();
        },
    };

    console.log('[OK] WorldItems System geladen');
})();
