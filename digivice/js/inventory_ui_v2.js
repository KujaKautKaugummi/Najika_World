/**
 * Inventory UI V2 - Najika World
 * =================================
 * Diablo/Dark Souls Style Inventar mit:
 * - Equipment Slots (Paperdoll-Layout)
 * - Grid-basiertes Inventar (Drag & Drop)
 * - Item Tooltips mit Stats
 * - Item-Vergleich (ausgeruestet vs. neu)
 * - Rarity-Glow Effekte
 * - Quick-Actions (Benutzen, Ausruesten, Wegwerfen)
 * - Sortierung + Filter
 * - Gold + Gewichtsanzeige
 *
 * I-Taste oder Inventar-Button oeffnet das UI.
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // ITEM TYPES & RARITY
    // ==========================================

    const ITEM_TYPES = {
        weapon:     { name: 'Waffe',       icon: '\u2694',       color: '#FF4444' },
        armor:      { name: 'Ruestung',    icon: '\uD83D\uDEE1',  color: '#4A90D9' },
        helmet:     { name: 'Helm',        icon: '\u26D1',       color: '#4A90D9' },
        boots:      { name: 'Stiefel',     icon: '\uD83D\uDC62', color: '#4A90D9' },
        ring:       { name: 'Ring',        icon: '\uD83D\uDC8D', color: '#9C27B0' },
        amulet:     { name: 'Amulett',     icon: '\uD83D\uDCFF', color: '#9C27B0' },
        consumable: { name: 'Verbrauchbar', icon: '\uD83E\uDDEA', color: '#4CAF50' },
        material:   { name: 'Material',    icon: '\uD83D\uDD27', color: '#795548' },
        quest:      { name: 'Quest-Item',  icon: '\u2B50',       color: '#FFD700' },
        key:        { name: 'Schluessel',  icon: '\uD83D\uDD11', color: '#FFD700' }
    };

    const RARITY = {
        common:    { name: 'Normal',    color: 'rgba(255,255,255,0.6)', glow: 'none', border: 'rgba(255,255,255,0.1)' },
        uncommon:  { name: 'Ungewoehnlich', color: '#4CAF50', glow: '0 0 6px rgba(76,175,80,0.3)', border: 'rgba(76,175,80,0.3)' },
        rare:      { name: 'Selten',    color: '#2196F3', glow: '0 0 8px rgba(33,150,243,0.4)', border: 'rgba(33,150,243,0.4)' },
        epic:      { name: 'Episch',    color: '#9C27B0', glow: '0 0 10px rgba(156,39,176,0.4)', border: 'rgba(156,39,176,0.4)' },
        legendary: { name: 'Legendaer', color: '#FFD700', glow: '0 0 12px rgba(255,215,0,0.5)', border: 'rgba(255,215,0,0.5)' }
    };

    // Equipment Slots
    const EQUIP_SLOTS = {
        helmet:    { name: 'Helm',      accepts: ['helmet'],  icon: '\u26D1',       x: 1, y: 0 },
        amulet:    { name: 'Amulett',   accepts: ['amulet'],  icon: '\uD83D\uDCFF', x: 2, y: 0 },
        weapon:    { name: 'Waffe',     accepts: ['weapon'],  icon: '\u2694',       x: 0, y: 1 },
        armor:     { name: 'Ruestung',  accepts: ['armor'],   icon: '\uD83D\uDEE1',  x: 1, y: 1 },
        offhand:   { name: 'Nebenhand', accepts: ['weapon', 'armor'], icon: '\uD83E\uDEF2', x: 2, y: 1 },
        ring_l:    { name: 'Ring L',    accepts: ['ring'],    icon: '\uD83D\uDC8D', x: 0, y: 2 },
        boots:     { name: 'Stiefel',   accepts: ['boots'],   icon: '\uD83D\uDC62', x: 1, y: 2 },
        ring_r:    { name: 'Ring R',    accepts: ['ring'],    icon: '\uD83D\uDC8D', x: 2, y: 2 }
    };

    // ==========================================
    // SAMPLE ITEMS
    // ==========================================

    const SAMPLE_ITEMS = [
        { id: 'iron_sword', name: 'Eisenschwert', type: 'weapon', rarity: 'common',
          icon: '\u2694', stats: { damage: 12, speed: 1.2 }, value: 50, weight: 3 },
        { id: 'fire_sword', name: 'Flammenschwert', type: 'weapon', rarity: 'rare',
          icon: '\uD83D\uDD25', stats: { damage: 28, speed: 1.0, fireDmg: 15 }, value: 800, weight: 4,
          description: 'Eine Klinge, die in ewigem Feuer brennt.' },
        { id: 'crystal_staff', name: 'Kristallstab', type: 'weapon', rarity: 'epic',
          icon: '\uD83D\uDD2E', stats: { magicDmg: 45, mana: 20 }, value: 2000, weight: 2,
          description: 'Verstaerkt alle Zauber um 25%.' },
        { id: 'leather_armor', name: 'Lederruestung', type: 'armor', rarity: 'common',
          icon: '\uD83E\uDDE5', stats: { defense: 8 }, value: 100, weight: 5 },
        { id: 'knight_armor', name: 'Ritterruestung', type: 'armor', rarity: 'uncommon',
          icon: '\uD83D\uDEE1', stats: { defense: 22, hp: 30 }, value: 500, weight: 12 },
        { id: 'iron_helm', name: 'Eisenhelm', type: 'helmet', rarity: 'common',
          icon: '\u26D1', stats: { defense: 5 }, value: 80, weight: 3 },
        { id: 'speed_boots', name: 'Windstiefel', type: 'boots', rarity: 'uncommon',
          icon: '\uD83D\uDC62', stats: { speed: 0.3, dodge: 5 }, value: 350, weight: 1 },
        { id: 'ruby_ring', name: 'Rubin-Ring', type: 'ring', rarity: 'rare',
          icon: '\uD83D\uDC8D', stats: { fireDmg: 10, hp: 15 }, value: 600, weight: 0.1 },
        { id: 'hp_potion', name: 'Heiltrank', type: 'consumable', rarity: 'common',
          icon: '\u2764', stats: { heal: 50 }, value: 25, weight: 0.5, stackable: true, count: 5 },
        { id: 'mp_potion', name: 'Manatrank', type: 'consumable', rarity: 'common',
          icon: '\uD83D\uDCA7', stats: { mana: 30 }, value: 30, weight: 0.5, stackable: true, count: 3 },
        { id: 'iron_ore', name: 'Eisenerz', type: 'material', rarity: 'common',
          icon: '\u26CF', stats: {}, value: 10, weight: 2, stackable: true, count: 12 },
        { id: 'crystal_shard', name: 'Kristallsplitter', type: 'material', rarity: 'uncommon',
          icon: '\uD83D\uDC8E', stats: {}, value: 50, weight: 0.3, stackable: true, count: 4 },
        { id: 'dungeon_key', name: 'Hoehlen-Schluessel', type: 'key', rarity: 'quest',
          icon: '\uD83D\uDD11', stats: {}, value: 0, weight: 0.1,
          description: 'Oeffnet den Eingang zur Kristallhoehle.' }
    ];

    // ==========================================
    // STATE
    // ==========================================

    let invState = {
        isOpen: false,
        items: [...SAMPLE_ITEMS],
        equipped: {},        // slotKey -> item
        gold: 1500,
        maxWeight: 50,
        selectedItem: null,
        dragItem: null,
        dragFrom: null,      // 'inventory' or slotKey
        filterType: 'all',
        sortBy: 'type',
        container: null
    };

    // Load state
    try {
        const saved = JSON.parse(localStorage.getItem('najika_inventory_v2'));
        if (saved) {
            invState.items = saved.items || SAMPLE_ITEMS;
            invState.equipped = saved.equipped || {};
            invState.gold = saved.gold ?? 1500;
        }
    } catch(e) { /* default */ }

    function saveInventory() {
        try {
            localStorage.setItem('najika_inventory_v2', JSON.stringify({
                items: invState.items,
                equipped: invState.equipped,
                gold: invState.gold
            }));
        } catch(e) { /* silent */ }
    }

    function getCurrentWeight() {
        let weight = invState.items.reduce((sum, item) =>
            sum + (item.weight || 0) * (item.count || 1), 0);
        Object.values(invState.equipped).forEach(item => {
            if (item) weight += item.weight || 0;
        });
        return Math.round(weight * 10) / 10;
    }

    // ==========================================
    // MAIN UI
    // ==========================================

    function openInventory() {
        if (invState.isOpen) { closeInventory(); return; }
        invState.isOpen = true;

        const container = document.createElement('div');
        container.id = 'inventory-ui-v2';
        container.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.97);
            z-index:9500;display:flex;justify-content:center;align-items:center;
            font-family:'Courier New',monospace;
        `;
        invState.container = container;

        const inner = document.createElement('div');
        inner.style.cssText = `
            display:flex;gap:20px;max-width:950px;width:90%;
        `;

        // Left: Equipment (Paperdoll)
        const equipPanel = document.createElement('div');
        equipPanel.id = 'inv-equip-panel';
        equipPanel.style.cssText = `
            width:240px;background:rgba(10,10,25,0.95);
            border:1px solid rgba(255,255,255,0.06);border-radius:10px;
            padding:16px;
        `;
        equipPanel.innerHTML = buildEquipPanel();

        // Center: Item Grid
        const gridPanel = document.createElement('div');
        gridPanel.id = 'inv-grid-panel';
        gridPanel.style.cssText = `
            flex:1;background:rgba(10,10,25,0.95);
            border:1px solid rgba(255,255,255,0.06);border-radius:10px;
            padding:16px;overflow-y:auto;max-height:80vh;
        `;
        gridPanel.innerHTML = buildItemGrid();

        // Right: Item Detail / Tooltip
        const detailPanel = document.createElement('div');
        detailPanel.id = 'inv-detail-panel';
        detailPanel.style.cssText = `
            width:240px;background:rgba(10,10,25,0.95);
            border:1px solid rgba(255,255,255,0.06);border-radius:10px;
            padding:16px;
        `;
        detailPanel.innerHTML = buildDetailPanel();

        inner.appendChild(equipPanel);
        inner.appendChild(gridPanel);
        inner.appendChild(detailPanel);
        container.appendChild(inner);

        // Close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '\u2715 ESC';
        closeBtn.style.cssText = `
            position:absolute;top:16px;right:20px;background:rgba(244,67,54,0.15);
            border:1px solid rgba(244,67,54,0.3);color:#F44336;
            padding:6px 14px;border-radius:4px;cursor:pointer;
            font-family:inherit;font-size:10px;z-index:10;
        `;
        closeBtn.onclick = closeInventory;
        container.appendChild(closeBtn);

        document.body.appendChild(container);

        // ESC
        invState._escHandler = (e) => { if (e.key === 'Escape') closeInventory(); };
        document.addEventListener('keydown', invState._escHandler);
    }

    function closeInventory() {
        invState.isOpen = false;
        invState.selectedItem = null;
        const container = document.getElementById('inventory-ui-v2');
        if (container) container.remove();
        if (invState._escHandler) {
            document.removeEventListener('keydown', invState._escHandler);
        }
    }

    function refreshInventory() {
        const equipPanel = document.getElementById('inv-equip-panel');
        if (equipPanel) equipPanel.innerHTML = buildEquipPanel();
        const gridPanel = document.getElementById('inv-grid-panel');
        if (gridPanel) gridPanel.innerHTML = buildItemGrid();
        const detailPanel = document.getElementById('inv-detail-panel');
        if (detailPanel) detailPanel.innerHTML = buildDetailPanel();
    }

    // ==========================================
    // EQUIPMENT PANEL (Paperdoll)
    // ==========================================

    function buildEquipPanel() {
        const weight = getCurrentWeight();
        const maxW = window.WeightSystem ? window.WeightSystem.getMaxWeight() : invState.maxWeight;
        const weightPercent = Math.min(100, (weight / maxW) * 100);
        const ratio = weight / maxW;
        const weightColor = ratio > 1.5 ? '#F44336' : ratio > 1.0 ? '#FF9800' : ratio > 0.7 ? '#FF9800' : '#4CAF50';

        let html = `
            <div style="text-align:center;margin-bottom:14px;">
                <div style="font-size:12px;color:white;font-weight:bold;">Ausruestung</div>
                <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px;">
                    Ziehe Items auf die Slots
                </div>
            </div>

            <!-- Equipment Grid (3x3) -->
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;
                margin-bottom:16px;">
        `;

        // Layout the slots in 3x3 grid
        for (let y = 0; y < 3; y++) {
            for (let x = 0; x < 3; x++) {
                const slotEntry = Object.entries(EQUIP_SLOTS).find(([_, s]) => s.x === x && s.y === y);
                if (slotEntry) {
                    const [slotKey, slot] = slotEntry;
                    const equipped = invState.equipped[slotKey];
                    const rarity = equipped ? (RARITY[equipped.rarity] || RARITY.common) : null;

                    html += `
                        <div onclick="window.InventoryV2._clickSlot('${slotKey}')"
                            ondragover="event.preventDefault()"
                            ondrop="window.InventoryV2._dropOnSlot('${slotKey}')"
                            style="aspect-ratio:1;border-radius:8px;
                            background:${equipped ? 'rgba(255,255,255,0.04)' : 'rgba(255,255,255,0.02)'};
                            border:1px ${equipped ? 'solid' : 'dashed'} ${equipped ? rarity.border : 'rgba(255,255,255,0.08)'};
                            display:flex;flex-direction:column;align-items:center;justify-content:center;
                            cursor:pointer;position:relative;
                            ${equipped ? 'box-shadow:' + rarity.glow + ';' : ''}"
                            title="${slot.name}">
                            <span style="font-size:${equipped ? '22px' : '16px'};
                                ${equipped ? '' : 'opacity:0.2;'}">${equipped ? equipped.icon : slot.icon}</span>
                            <span style="font-size:7px;color:rgba(255,255,255,${equipped ? '0.5' : '0.2'});
                                margin-top:2px;">${equipped ? equipped.name.substring(0, 10) : slot.name}</span>
                        </div>
                    `;
                } else {
                    html += `<div></div>`;
                }
            }
        }

        html += `</div>`;

        // Stats Summary
        const totalStats = calculateTotalStats();
        html += `
            <div style="font-size:8px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                margin-bottom:6px;">GESAMT-STATS</div>
            <div style="background:rgba(255,255,255,0.02);border-radius:6px;padding:8px;">
        `;
        Object.entries(totalStats).forEach(([stat, value]) => {
            if (value === 0) return;
            html += `
                <div style="display:flex;justify-content:space-between;font-size:9px;padding:2px 0;">
                    <span style="color:rgba(255,255,255,0.4);">${formatStatName(stat)}</span>
                    <span style="color:#4CAF50;font-weight:bold;">+${value}</span>
                </div>
            `;
        });
        html += `</div>`;

        // Weight + Gold
        html += `
            <div style="margin-top:12px;">
                <div style="display:flex;justify-content:space-between;font-size:9px;margin-bottom:3px;">
                    <span style="color:rgba(255,255,255,0.4);">Gewicht</span>
                    <span style="color:${weightColor};">${Math.round(weight*10)/10}/${Math.round(maxW*10)/10}${ratio > 1.0 ? ' ÜBERLADEN' : ''}</span>
                </div>
                <div style="background:rgba(255,255,255,0.06);height:3px;border-radius:2px;">
                    <div style="background:${weightColor};height:100%;width:${weightPercent}%;
                        border-radius:2px;"></div>
                </div>
                <div style="font-size:10px;color:#FFD700;margin-top:8px;text-align:center;">
                    \uD83D\uDCB0 ${invState.gold.toLocaleString()} Gold
                </div>
            </div>
        `;

        return html;
    }

    function calculateTotalStats() {
        const stats = {};
        Object.values(invState.equipped).forEach(item => {
            if (!item || !item.stats) return;
            Object.entries(item.stats).forEach(([key, value]) => {
                stats[key] = (stats[key] || 0) + value;
            });
        });
        return stats;
    }

    function formatStatName(stat) {
        const names = {
            damage: 'Schaden', defense: 'Verteidigung', speed: 'Tempo',
            hp: 'HP', mana: 'Mana', fireDmg: 'Feuer-DMG',
            dodge: 'Ausweichen', magicDmg: 'Magie-DMG', heal: 'Heilung'
        };
        return names[stat] || stat;
    }

    // ==========================================
    // ITEM GRID
    // ==========================================

    function buildItemGrid() {
        let items = [...invState.items];

        // Filter
        if (invState.filterType !== 'all') {
            items = items.filter(i => i.type === invState.filterType);
        }

        // Sort
        if (invState.sortBy === 'type') {
            items.sort((a, b) => a.type.localeCompare(b.type));
        } else if (invState.sortBy === 'rarity') {
            const order = { legendary: 0, epic: 1, rare: 2, uncommon: 3, common: 4 };
            items.sort((a, b) => (order[a.rarity] || 5) - (order[b.rarity] || 5));
        } else if (invState.sortBy === 'value') {
            items.sort((a, b) => b.value - a.value);
        } else if (invState.sortBy === 'name') {
            items.sort((a, b) => a.name.localeCompare(b.name));
        }

        // Filter buttons
        let html = `
            <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:10px;">
                ${['all', 'weapon', 'armor', 'helmet', 'boots', 'ring', 'amulet', 'consumable', 'material'].map(t => {
                    const type = t === 'all' ? { name: 'Alle', icon: '\uD83D\uDCE6' } : ITEM_TYPES[t];
                    const isActive = invState.filterType === t;
                    return `
                        <button onclick="window.InventoryV2._setFilter('${t}')"
                            style="padding:3px 8px;font-size:8px;font-family:inherit;
                            background:${isActive ? 'rgba(255,255,255,0.08)' : 'rgba(255,255,255,0.02)'};
                            border:1px solid ${isActive ? 'rgba(255,255,255,0.2)' : 'rgba(255,255,255,0.06)'};
                            color:${isActive ? 'white' : 'rgba(255,255,255,0.4)'};
                            border-radius:3px;cursor:pointer;">
                            ${type.icon}
                        </button>
                    `;
                }).join('')}

                <span style="flex:1;"></span>

                <!-- Sort -->
                <select onchange="window.InventoryV2._setSort(this.value)"
                    style="padding:3px 6px;font-size:8px;font-family:inherit;
                    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                    color:rgba(255,255,255,0.5);border-radius:3px;">
                    <option value="type" ${invState.sortBy === 'type' ? 'selected' : ''}>Typ</option>
                    <option value="rarity" ${invState.sortBy === 'rarity' ? 'selected' : ''}>Seltenheit</option>
                    <option value="value" ${invState.sortBy === 'value' ? 'selected' : ''}>Wert</option>
                    <option value="name" ${invState.sortBy === 'name' ? 'selected' : ''}>Name</option>
                </select>
            </div>

            <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-bottom:8px;">
                ${items.length} Items | Rechtsklick fuer Aktionen
            </div>
        `;

        if (items.length === 0) {
            html += `
                <div style="text-align:center;padding:40px;color:rgba(255,255,255,0.2);">
                    <div style="font-size:28px;margin-bottom:8px;">\uD83C\uDF92</div>
                    <div style="font-size:11px;">Keine Items</div>
                </div>
            `;
        } else {
            html += `<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(70px,1fr));gap:6px;">`;

            items.forEach((item, idx) => {
                const rarity = RARITY[item.rarity] || RARITY.common;
                const isSelected = invState.selectedItem === item.id;

                html += `
                    <div onclick="window.InventoryV2._selectItem('${item.id}')"
                        oncontextmenu="event.preventDefault();window.InventoryV2._contextMenu(event,'${item.id}')"
                        draggable="true"
                        ondragstart="window.InventoryV2._dragStart('${item.id}','inventory')"
                        style="aspect-ratio:1;border-radius:6px;
                        background:${isSelected ? 'rgba(255,255,255,0.06)' : 'rgba(255,255,255,0.02)'};
                        border:1px solid ${isSelected ? rarity.color : rarity.border};
                        display:flex;flex-direction:column;align-items:center;justify-content:center;
                        cursor:pointer;position:relative;
                        box-shadow:${isSelected ? rarity.glow : 'none'};
                        transition:all 0.15s;"
                        onmouseover="this.style.background='rgba(255,255,255,0.04)'"
                        onmouseout="this.style.background='${isSelected ? 'rgba(255,255,255,0.06)' : 'rgba(255,255,255,0.02)'}'"
                    >
                        <span style="font-size:22px;">${item.icon}</span>
                        <span style="font-size:7px;color:${rarity.color};margin-top:2px;
                            max-width:90%;overflow:hidden;text-overflow:ellipsis;
                            white-space:nowrap;text-align:center;">${item.name}</span>
                        ${item.count > 1 ? `<span style="position:absolute;bottom:2px;right:4px;
                            font-size:8px;color:rgba(255,255,255,0.5);">x${item.count}</span>` : ''}
                    </div>
                `;
            });

            html += `</div>`;
        }

        return html;
    }

    // ==========================================
    // DETAIL PANEL
    // ==========================================

    function buildDetailPanel() {
        if (!invState.selectedItem) {
            return `
                <div style="text-align:center;padding:40px 10px;color:rgba(255,255,255,0.2);">
                    <div style="font-size:28px;margin-bottom:8px;">\uD83D\uDD0D</div>
                    <div style="font-size:10px;">Item auswaehlen<br>fuer Details</div>
                </div>
            `;
        }

        const item = invState.items.find(i => i.id === invState.selectedItem) ||
                     Object.values(invState.equipped).find(i => i && i.id === invState.selectedItem);
        if (!item) return '';

        const rarity = RARITY[item.rarity] || RARITY.common;
        const type = ITEM_TYPES[item.type] || { name: item.type, icon: '', color: 'white' };
        const canEquip = ['weapon', 'armor', 'helmet', 'boots', 'ring', 'amulet'].includes(item.type);
        const canUse = item.type === 'consumable';

        // Check if same type is equipped for comparison
        let comparisonHtml = '';
        if (canEquip) {
            const equippedInSlot = Object.entries(invState.equipped).find(([slotKey, eq]) => {
                if (!eq) return false;
                return EQUIP_SLOTS[slotKey]?.accepts?.includes(item.type);
            });
            if (equippedInSlot) {
                const [, equippedItem] = equippedInSlot;
                comparisonHtml = buildComparison(item, equippedItem);
            }
        }

        return `
            <div style="text-align:center;margin-bottom:12px;">
                <div style="font-size:36px;margin-bottom:6px;
                    ${rarity.glow !== 'none' ? 'text-shadow:' + rarity.glow + ';' : ''}">${item.icon}</div>
                <div style="font-size:13px;color:${rarity.color};font-weight:bold;">${item.name}</div>
                <div style="font-size:8px;color:rgba(255,255,255,0.3);margin-top:2px;">
                    ${rarity.name} ${type.name}</div>
            </div>

            ${item.description ? `
                <div style="font-size:9px;color:rgba(255,255,255,0.5);font-style:italic;
                    text-align:center;margin-bottom:12px;line-height:1.5;">
                    "${item.description}"
                </div>
            ` : ''}

            <!-- Stats -->
            ${Object.keys(item.stats || {}).length > 0 ? `
                <div style="font-size:8px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                    margin-bottom:4px;">STATS</div>
                <div style="background:rgba(255,255,255,0.02);border-radius:6px;padding:8px;
                    margin-bottom:10px;">
                    ${Object.entries(item.stats).map(([stat, value]) => `
                        <div style="display:flex;justify-content:space-between;font-size:9px;padding:2px 0;">
                            <span style="color:rgba(255,255,255,0.4);">${formatStatName(stat)}</span>
                            <span style="color:#4CAF50;">+${value}</span>
                        </div>
                    `).join('')}
                </div>
            ` : ''}

            ${comparisonHtml}

            <!-- Info -->
            <div style="display:flex;justify-content:space-between;font-size:9px;
                padding:4px 0;color:rgba(255,255,255,0.3);">
                <span>Wert</span>
                <span style="color:#FFD700;">\uD83D\uDCB0 ${item.value}</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:9px;
                padding:4px 0;color:rgba(255,255,255,0.3);">
                <span>Gewicht</span>
                <span>${item.weight} kg</span>
            </div>

            <!-- Actions -->
            <div style="display:flex;flex-direction:column;gap:6px;margin-top:12px;">
                ${canEquip ? `
                    <button onclick="window.InventoryV2.equip('${item.id}')"
                        style="padding:8px;font-size:10px;font-family:inherit;
                        background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.3);
                        color:#4CAF50;border-radius:4px;cursor:pointer;">
                        \u2694 Ausruesten
                    </button>
                ` : ''}
                ${canUse ? `
                    <button onclick="window.InventoryV2.use('${item.id}')"
                        style="padding:8px;font-size:10px;font-family:inherit;
                        background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.3);
                        color:#4CAF50;border-radius:4px;cursor:pointer;">
                        \uD83E\uDDEA Benutzen
                    </button>
                ` : ''}
                <button onclick="window.InventoryV2.drop('${item.id}')"
                    style="padding:6px;font-size:9px;font-family:inherit;
                    background:rgba(244,67,54,0.06);border:1px solid rgba(244,67,54,0.15);
                    color:rgba(244,67,54,0.5);border-radius:4px;cursor:pointer;">
                    \uD83D\uDDD1 Wegwerfen
                </button>
            </div>
        `;
    }

    function buildComparison(newItem, equippedItem) {
        if (!equippedItem) return '';

        const allStats = new Set([
            ...Object.keys(newItem.stats || {}),
            ...Object.keys(equippedItem.stats || {})
        ]);

        let html = `
            <div style="font-size:8px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                margin-bottom:4px;">VERGLEICH</div>
            <div style="background:rgba(255,255,255,0.02);border-radius:6px;padding:8px;
                margin-bottom:10px;">
        `;

        allStats.forEach(stat => {
            const newVal = (newItem.stats || {})[stat] || 0;
            const oldVal = (equippedItem.stats || {})[stat] || 0;
            const diff = newVal - oldVal;
            if (diff === 0) return;

            const color = diff > 0 ? '#4CAF50' : '#FF4444';
            html += `
                <div style="display:flex;justify-content:space-between;font-size:9px;padding:2px 0;">
                    <span style="color:rgba(255,255,255,0.4);">${formatStatName(stat)}</span>
                    <span style="color:${color};font-weight:bold;">${diff > 0 ? '+' : ''}${diff}</span>
                </div>
            `;
        });

        html += `</div>`;
        return html;
    }

    // ==========================================
    // ACTIONS
    // ==========================================

    function equipItem(itemId) {
        const itemIdx = invState.items.findIndex(i => i.id === itemId);
        if (itemIdx === -1) return false;

        const item = invState.items[itemIdx];
        const slot = Object.entries(EQUIP_SLOTS).find(([_, s]) => s.accepts.includes(item.type));
        if (!slot) return false;

        const [slotKey] = slot;

        // Swap if something is equipped
        if (invState.equipped[slotKey]) {
            invState.items.push(invState.equipped[slotKey]);
        }

        invState.equipped[slotKey] = item;
        invState.items.splice(itemIdx, 1);
        saveInventory();
        refreshInventory();
        return true;
    }

    function unequipItem(slotKey) {
        if (!invState.equipped[slotKey]) return false;

        invState.items.push(invState.equipped[slotKey]);
        invState.equipped[slotKey] = null;
        saveInventory();
        refreshInventory();
        return true;
    }

    function useItem(itemId) {
        const item = invState.items.find(i => i.id === itemId);
        if (!item || item.type !== 'consumable') return false;

        // Apply effect
        if (item.stats.heal && window.CombatUIPolish) {
            window.CombatUIPolish.onPlayerHeal(item.stats.heal);
        }

        // Reduce count or remove
        if (item.stackable && item.count > 1) {
            item.count--;
        } else {
            invState.items = invState.items.filter(i => i.id !== itemId);
            invState.selectedItem = null;
        }

        saveInventory();
        refreshInventory();

        if (window.QuestTrackerV2) {
            window.QuestTrackerV2.showNotification('ITEM BENUTZT', `${item.icon} ${item.name}`, '#4CAF50');
        }
        return true;
    }

    function dropItem(itemId) {
        const itemIdx = invState.items.findIndex(i => i.id === itemId);
        if (itemIdx === -1) return false;

        const item = invState.items[itemIdx];
        if (item.type === 'quest' || item.type === 'key') return false; // Can't drop quest items

        invState.items.splice(itemIdx, 1);
        invState.selectedItem = null;
        saveInventory();
        refreshInventory();
        return true;
    }

    // ==========================================
    // DRAG & DROP
    // ==========================================

    function dragStart(itemId, from) {
        invState.dragItem = itemId;
        invState.dragFrom = from;
    }

    function dropOnSlot(slotKey) {
        if (!invState.dragItem) return;

        const item = invState.items.find(i => i.id === invState.dragItem);
        if (!item) return;

        const slot = EQUIP_SLOTS[slotKey];
        if (!slot || !slot.accepts.includes(item.type)) return;

        equipItem(invState.dragItem);
        invState.dragItem = null;
        invState.dragFrom = null;
    }

    // Context Menu
    function showContextMenu(event, itemId) {
        const existing = document.getElementById('inv-context-menu');
        if (existing) existing.remove();

        const item = invState.items.find(i => i.id === itemId);
        if (!item) return;

        const menu = document.createElement('div');
        menu.id = 'inv-context-menu';
        menu.style.cssText = `
            position:fixed;left:${event.clientX}px;top:${event.clientY}px;
            background:rgba(10,10,25,0.98);border:1px solid rgba(255,255,255,0.1);
            border-radius:6px;padding:4px 0;z-index:11000;min-width:140px;
            font-family:'Courier New',monospace;
            box-shadow:0 4px 16px rgba(0,0,0,0.6);
        `;

        const canEquip = ['weapon', 'armor', 'helmet', 'boots', 'ring', 'amulet'].includes(item.type);
        const canUse = item.type === 'consumable';
        const canDrop = item.type !== 'quest' && item.type !== 'key';

        let menuHtml = '';
        if (canEquip) menuHtml += `<div onclick="window.InventoryV2.equip('${itemId}');document.getElementById('inv-context-menu').remove()" style="padding:6px 14px;font-size:10px;color:#4CAF50;cursor:pointer;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">\u2694 Ausruesten</div>`;
        if (canUse) menuHtml += `<div onclick="window.InventoryV2.use('${itemId}');document.getElementById('inv-context-menu').remove()" style="padding:6px 14px;font-size:10px;color:#4CAF50;cursor:pointer;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">\uD83E\uDDEA Benutzen</div>`;
        if (canDrop) menuHtml += `<div onclick="window.InventoryV2.drop('${itemId}');document.getElementById('inv-context-menu').remove()" style="padding:6px 14px;font-size:10px;color:#FF4444;cursor:pointer;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">\uD83D\uDDD1 Wegwerfen</div>`;

        menu.innerHTML = menuHtml;
        document.body.appendChild(menu);

        // Close on click outside
        setTimeout(() => {
            const closeHandler = () => {
                menu.remove();
                document.removeEventListener('click', closeHandler);
            };
            document.addEventListener('click', closeHandler);
        }, 10);
    }

    // Keyboard: I = Inventory
    document.addEventListener('keydown', (e) => {
        if (e.key === 'i' || e.key === 'I') {
            if (document.activeElement.tagName === 'INPUT' ||
                document.activeElement.tagName === 'TEXTAREA') return;
            const chatUI = document.getElementById('chat-ui');
            if (chatUI && chatUI.style.display !== 'none') return;
            if (invState.isOpen) closeInventory(); else openInventory();
        }
    });

    // ==========================================
    // EXPORT
    // ==========================================

    window.InventoryV2 = {
        open: openInventory,
        close: closeInventory,
        equip: equipItem,
        unequip: unequipItem,
        use: useItem,
        drop: dropItem,
        addItem: (item) => {
            const itemWeight = (item.weight || 0) * (item.count || 1);
            if (window.WeightSystem && !window.WeightSystem.canPickUp(itemWeight)) {
                console.warn('[INVENTORY] Zu schwer! Kann nicht aufheben:', item.name || item.id);
                if (window.QuestTrackerV2?.showNotification) {
                    window.QuestTrackerV2.showNotification('ZU SCHWER', 'Inventar überladen! Kann nicht aufheben.', '#F44336');
                }
                return false;
            }
            invState.items.push(item);
            saveInventory();
            return true;
        },
        addGold: (amount) => { invState.gold += amount; saveInventory(); },
        getGold: () => invState.gold,
        setGold: (amount) => { invState.gold = amount; saveInventory(); },
        getItems: () => [...invState.items],
        getEquipped: () => ({ ...invState.equipped }),
        getCurrentWeight,
        clearAll: () => {
            invState.items = [];
            invState.equipped = {};
            invState.gold = 0;
            saveInventory();
        },
        ITEM_TYPES,
        RARITY,
        EQUIP_SLOTS,
        // Internal
        _selectItem: (id) => { invState.selectedItem = id; refreshInventory(); },
        _setFilter: (f) => { invState.filterType = f; refreshInventory(); },
        _setSort: (s) => { invState.sortBy = s; refreshInventory(); },
        _clickSlot: (slotKey) => {
            if (invState.equipped[slotKey]) {
                invState.selectedItem = invState.equipped[slotKey].id;
                refreshInventory();
            }
        },
        _dragStart: dragStart,
        _dropOnSlot: dropOnSlot,
        _contextMenu: showContextMenu
    };

    console.log(`[OK] Inventory UI V2 geladen: ${invState.items.length} Items, ${Object.keys(EQUIP_SLOTS).length} Equip-Slots`);

})();
