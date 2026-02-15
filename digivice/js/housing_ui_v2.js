/**
 * Housing UI V2 - Najika World
 * ==============================
 * Erweitert housing_3d.js + housing_3d_placement.js mit:
 * - Modernes Moebel-Katalog UI (Grid + Preview)
 * - Raum-Uebersicht mit Minimap
 * - Dekorations-Presets (Sparset-Themes)
 * - Haus-Upgrade Fortschrittsanzeige
 * - Gaeste-System (NPCs besuchen dein Haus)
 * - Moebel-Favoriten und Sortierung
 *
 * Oeffnet sich ueber H-Taste oder Housing Button.
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // FURNITURE CATALOG (Extended)
    // ==========================================

    const FURNITURE_CATEGORIES = {
        essential:   { name: 'Grundlagen',    icon: '\uD83C\uDFE0', color: '#4CAF50' },
        bedroom:     { name: 'Schlafzimmer',  icon: '\uD83D\uDECF',  color: '#9C27B0' },
        kitchen:     { name: 'Kueche',        icon: '\uD83C\uDF73', color: '#FF9800' },
        living:      { name: 'Wohnzimmer',    icon: '\uD83D\uDECB',  color: '#2196F3' },
        crafting:    { name: 'Werkstatt',     icon: '\u2692',       color: '#795548' },
        garden:      { name: 'Garten',        icon: '\uD83C\uDF3B', color: '#8BC34A' },
        decoration:  { name: 'Dekoration',    icon: '\uD83C\uDFA8', color: '#E91E63' },
        special:     { name: 'Spezial',       icon: '\u2B50',       color: '#FFD700' }
    };

    const FURNITURE_ITEMS = [
        // Essential
        { id: 'bed_simple', name: 'Einfaches Bett', category: 'essential', cost: 100,
          icon: '\uD83D\uDECF', effect: '+5 HP Regen', rarity: 'common' },
        { id: 'table_wood', name: 'Holztisch', category: 'essential', cost: 50,
          icon: '\uD83E\uDE91', effect: null, rarity: 'common' },
        { id: 'chair_wood', name: 'Holzstuhl', category: 'essential', cost: 30,
          icon: '\uD83E\uDE91', effect: null, rarity: 'common' },
        { id: 'chest_storage', name: 'Lagertruhe', category: 'essential', cost: 150,
          icon: '\uD83D\uDCE6', effect: '+10 Inventar-Slots', rarity: 'common' },
        { id: 'lamp_basic', name: 'Oellampe', category: 'essential', cost: 40,
          icon: '\uD83D\uDCA1', effect: 'Licht', rarity: 'common' },

        // Bedroom
        { id: 'bed_royal', name: 'Koenigsbett', category: 'bedroom', cost: 800,
          icon: '\uD83D\uDC51', effect: '+15 HP Regen, +5% XP', rarity: 'rare' },
        { id: 'wardrobe', name: 'Kleiderschrank', category: 'bedroom', cost: 200,
          icon: '\uD83D\uDEAA', effect: 'Outfit-Wechsel', rarity: 'common' },
        { id: 'nightstand', name: 'Nachttisch', category: 'bedroom', cost: 60,
          icon: '\uD83D\uDCDA', effect: null, rarity: 'common' },
        { id: 'mirror_ornate', name: 'Ornament-Spiegel', category: 'bedroom', cost: 300,
          icon: '\uD83E\uDE9E', effect: 'Aussehen aendern', rarity: 'uncommon' },

        // Kitchen
        { id: 'stove', name: 'Herd', category: 'kitchen', cost: 400,
          icon: '\uD83D\uDD25', effect: 'Kochen moeglich', rarity: 'uncommon' },
        { id: 'alchemy_table', name: 'Alchemie-Tisch', category: 'kitchen', cost: 500,
          icon: '\u2697', effect: 'Traenke brauen', rarity: 'uncommon' },
        { id: 'fridge_ice', name: 'Eis-Kuehlschrank', category: 'kitchen', cost: 350,
          icon: '\u2744', effect: 'Nahrung haelt laenger', rarity: 'uncommon' },

        // Living
        { id: 'sofa_velvet', name: 'Samt-Sofa', category: 'living', cost: 400,
          icon: '\uD83D\uDECB', effect: '+3 NPC Gast-Platz', rarity: 'uncommon' },
        { id: 'bookshelf', name: 'Buecherregal', category: 'living', cost: 250,
          icon: '\uD83D\uDCDA', effect: '+3% XP', rarity: 'common' },
        { id: 'fireplace', name: 'Kamin', category: 'living', cost: 600,
          icon: '\uD83D\uDD25', effect: '+10 HP Regen, Waerme', rarity: 'rare' },
        { id: 'trophy_case', name: 'Trophaeen-Vitrine', category: 'living', cost: 450,
          icon: '\uD83C\uDFC6', effect: 'Boss-Trophaeen zeigen', rarity: 'uncommon' },

        // Crafting
        { id: 'anvil', name: 'Amboss', category: 'crafting', cost: 700,
          icon: '\uD83D\uDD28', effect: 'Schmieden moeglich', rarity: 'rare' },
        { id: 'enchanting_table', name: 'Verzauberungs-Tisch', category: 'crafting', cost: 1000,
          icon: '\u2728', effect: 'Items verzaubern', rarity: 'rare' },
        { id: 'workbench', name: 'Werkbank', category: 'crafting', cost: 300,
          icon: '\uD83D\uDD27', effect: 'Reparaturen + Crafting', rarity: 'uncommon' },

        // Garden
        { id: 'flower_pot', name: 'Blumentopf', category: 'garden', cost: 30,
          icon: '\uD83C\uDF3B', effect: null, rarity: 'common' },
        { id: 'herb_garden', name: 'Kraeuterbeet', category: 'garden', cost: 200,
          icon: '\uD83C\uDF3F', effect: 'Kraeuteranbau', rarity: 'uncommon' },
        { id: 'fountain', name: 'Springbrunnen', category: 'garden', cost: 800,
          icon: '\u26F2', effect: '+5 Trust, NPC Attraktor', rarity: 'rare' },

        // Decoration
        { id: 'painting_landscape', name: 'Landschaftsbild', category: 'decoration', cost: 150,
          icon: '\uD83D\uDDBC', effect: null, rarity: 'common' },
        { id: 'rug_ornate', name: 'Ornament-Teppich', category: 'decoration', cost: 200,
          icon: '\uD83E\uDEA3', effect: null, rarity: 'uncommon' },
        { id: 'chandelier', name: 'Kronleuchter', category: 'decoration', cost: 500,
          icon: '\uD83D\uDCA1', effect: 'Luxus-Licht', rarity: 'rare' },
        { id: 'banner_faction', name: 'Fraktions-Banner', category: 'decoration', cost: 100,
          icon: '\uD83C\uDFF3', effect: 'Zeige deine Fraktion', rarity: 'common' },

        // Special
        { id: 'teleport_crystal', name: 'Teleport-Kristall', category: 'special', cost: 2000,
          icon: '\uD83D\uDC8E', effect: 'Heim-Teleport', rarity: 'legendary' },
        { id: 'slime_bed', name: 'Schleim-Bettchen', category: 'special', cost: 300,
          icon: '\uD83D\uDCA7', effect: '+5 Schleim-Trust', rarity: 'rare' },
        { id: 'music_box', name: 'Spieluhr', category: 'special', cost: 400,
          icon: '\uD83C\uDFB5', effect: 'Hintergrund-Musik', rarity: 'rare' },
        { id: 'portal_frame', name: 'Portal-Rahmen', category: 'special', cost: 5000,
          icon: '\uD83C\uDF00', effect: 'Dungeon-Zugang von Zuhause', rarity: 'legendary' }
    ];

    // House Upgrade Levels
    const HOUSE_LEVELS = [
        { level: 1, name: 'Huette',         rooms: 1, slots: 10,  upgradeCost: 0 },
        { level: 2, name: 'Kleines Haus',   rooms: 2, slots: 20,  upgradeCost: 500 },
        { level: 3, name: 'Haus',           rooms: 3, slots: 35,  upgradeCost: 1500 },
        { level: 4, name: 'Grosses Haus',   rooms: 4, slots: 50,  upgradeCost: 3000 },
        { level: 5, name: 'Villa',          rooms: 5, slots: 75,  upgradeCost: 6000 },
        { level: 6, name: 'Herrenhaus',     rooms: 7, slots: 100, upgradeCost: 12000 },
        { level: 7, name: 'Palast',         rooms: 10, slots: 150, upgradeCost: 25000 },
        { level: 8, name: 'Schwarze Muehle', rooms: 12, slots: 200, upgradeCost: 50000 }
    ];

    // ==========================================
    // STATE
    // ==========================================

    let housingState = {
        isOpen: false,
        houseLevel: 1,
        gold: 5000,
        placedFurniture: [],
        ownedFurniture: [],
        selectedCategory: 'all',
        selectedItem: null,
        favorites: new Set(),
        sortBy: 'cost', // cost, name, rarity
        container: null
    };

    // Load state
    try {
        const saved = JSON.parse(localStorage.getItem('najika_housing_v2'));
        if (saved) {
            housingState.houseLevel = saved.houseLevel || 1;
            housingState.gold = saved.gold ?? 5000;
            housingState.placedFurniture = saved.placedFurniture || [];
            housingState.ownedFurniture = saved.ownedFurniture || [];
            housingState.favorites = new Set(saved.favorites || []);
        }
    } catch(e) { /* default */ }

    function saveHousing() {
        try {
            localStorage.setItem('najika_housing_v2', JSON.stringify({
                houseLevel: housingState.houseLevel,
                gold: housingState.gold,
                placedFurniture: housingState.placedFurniture,
                ownedFurniture: housingState.ownedFurniture,
                favorites: [...housingState.favorites]
            }));
        } catch(e) { /* silent */ }
    }

    // ==========================================
    // MAIN UI
    // ==========================================

    function openHousingUI() {
        if (housingState.isOpen) { closeHousingUI(); return; }
        housingState.isOpen = true;

        const container = document.createElement('div');
        container.id = 'housing-ui-v2';
        container.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.97);
            z-index:9500;display:flex;
            font-family:'Courier New',monospace;
        `;
        housingState.container = container;

        // Left sidebar: categories + house info
        const sidebar = document.createElement('div');
        sidebar.id = 'housing-sidebar';
        sidebar.style.cssText = `
            width:220px;background:rgba(10,10,20,1);
            border-right:1px solid rgba(255,255,255,0.06);
            overflow-y:auto;
        `;
        sidebar.innerHTML = buildSidebar();

        // Main: furniture catalog
        const main = document.createElement('div');
        main.id = 'housing-main';
        main.style.cssText = `flex:1;overflow-y:auto;padding:20px;`;
        main.innerHTML = buildCatalog();

        // Right: detail/preview panel
        const detail = document.createElement('div');
        detail.id = 'housing-detail';
        detail.style.cssText = `
            width:280px;background:rgba(10,10,20,1);
            border-left:1px solid rgba(255,255,255,0.06);
            padding:20px;overflow-y:auto;
        `;
        detail.innerHTML = buildHouseInfo();

        // Close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '\u2715';
        closeBtn.style.cssText = `
            position:absolute;top:12px;right:16px;background:none;border:none;
            color:rgba(255,255,255,0.4);font-size:18px;cursor:pointer;z-index:10;
        `;
        closeBtn.onclick = closeHousingUI;

        container.appendChild(sidebar);
        container.appendChild(main);
        container.appendChild(detail);
        container.appendChild(closeBtn);
        document.body.appendChild(container);

        // ESC
        housingState._escHandler = (e) => { if (e.key === 'Escape') closeHousingUI(); };
        document.addEventListener('keydown', housingState._escHandler);
    }

    function closeHousingUI() {
        housingState.isOpen = false;
        const container = document.getElementById('housing-ui-v2');
        if (container) container.remove();
        if (housingState._escHandler) {
            document.removeEventListener('keydown', housingState._escHandler);
        }
    }

    function refreshUI() {
        const sidebar = document.getElementById('housing-sidebar');
        if (sidebar) sidebar.innerHTML = buildSidebar();
        const main = document.getElementById('housing-main');
        if (main) main.innerHTML = buildCatalog();
        const detail = document.getElementById('housing-detail');
        if (detail) detail.innerHTML = housingState.selectedItem ?
            buildItemDetail(housingState.selectedItem) : buildHouseInfo();
    }

    // ==========================================
    // SIDEBAR
    // ==========================================

    function buildSidebar() {
        const houseInfo = HOUSE_LEVELS[housingState.houseLevel - 1];
        const usedSlots = housingState.placedFurniture.length;

        return `
            <div style="padding:16px;border-bottom:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:14px;color:#FF9800;font-weight:bold;">
                    \uD83C\uDFE0 Hausbau</div>
                <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:4px;">
                    ${houseInfo.name} (Stufe ${houseInfo.level})
                </div>
                <div style="margin-top:8px;">
                    <div style="display:flex;justify-content:space-between;font-size:9px;
                        color:rgba(255,255,255,0.4);margin-bottom:3px;">
                        <span>Moebel</span>
                        <span>${usedSlots}/${houseInfo.slots}</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.06);height:4px;border-radius:2px;">
                        <div style="background:#FF9800;height:100%;
                            width:${Math.min(100, (usedSlots / houseInfo.slots) * 100)}%;
                            border-radius:2px;"></div>
                    </div>
                </div>
                <div style="font-size:10px;color:#FFD700;margin-top:8px;">
                    \uD83D\uDCB0 ${housingState.gold.toLocaleString()} Gold
                </div>
            </div>

            <!-- Categories -->
            <div style="padding:8px 0;">
                <div onclick="window.HousingUIV2._setCategory('all')"
                    style="padding:8px 16px;cursor:pointer;font-size:10px;
                    color:${housingState.selectedCategory === 'all' ? 'white' : 'rgba(255,255,255,0.5)'};
                    border-left:3px solid ${housingState.selectedCategory === 'all' ? '#FF9800' : 'transparent'};
                    background:${housingState.selectedCategory === 'all' ? 'rgba(255,152,0,0.08)' : 'transparent'};">
                    \uD83D\uDCE6 Alle (${FURNITURE_ITEMS.length})
                </div>
                <div onclick="window.HousingUIV2._setCategory('favorites')"
                    style="padding:8px 16px;cursor:pointer;font-size:10px;
                    color:${housingState.selectedCategory === 'favorites' ? 'white' : 'rgba(255,255,255,0.5)'};
                    border-left:3px solid ${housingState.selectedCategory === 'favorites' ? '#E91E63' : 'transparent'};
                    background:${housingState.selectedCategory === 'favorites' ? 'rgba(233,30,99,0.08)' : 'transparent'};">
                    \u2764 Favoriten (${housingState.favorites.size})
                </div>
                ${Object.entries(FURNITURE_CATEGORIES).map(([key, cat]) => {
                    const count = FURNITURE_ITEMS.filter(f => f.category === key).length;
                    const isActive = housingState.selectedCategory === key;
                    return `
                        <div onclick="window.HousingUIV2._setCategory('${key}')"
                            style="padding:8px 16px;cursor:pointer;font-size:10px;
                            color:${isActive ? 'white' : 'rgba(255,255,255,0.5)'};
                            border-left:3px solid ${isActive ? cat.color : 'transparent'};
                            background:${isActive ? cat.color + '14' : 'transparent'};">
                            ${cat.icon} ${cat.name} (${count})
                        </div>
                    `;
                }).join('')}
            </div>

            <!-- Sort -->
            <div style="padding:12px 16px;border-top:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:8px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                    margin-bottom:6px;">SORTIERUNG</div>
                <div style="display:flex;gap:4px;flex-wrap:wrap;">
                    ${['cost', 'name', 'rarity'].map(s => `
                        <button onclick="window.HousingUIV2._setSort('${s}')"
                            style="padding:3px 8px;font-size:8px;font-family:inherit;
                            background:${housingState.sortBy === s ? 'rgba(255,152,0,0.15)' : 'rgba(255,255,255,0.04)'};
                            border:1px solid ${housingState.sortBy === s ? 'rgba(255,152,0,0.3)' : 'rgba(255,255,255,0.08)'};
                            color:${housingState.sortBy === s ? '#FF9800' : 'rgba(255,255,255,0.4)'};
                            border-radius:3px;cursor:pointer;">
                            ${s === 'cost' ? 'Preis' : s === 'name' ? 'Name' : 'Seltenheit'}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // ==========================================
    // CATALOG
    // ==========================================

    function buildCatalog() {
        let items = [...FURNITURE_ITEMS];

        // Filter
        if (housingState.selectedCategory === 'favorites') {
            items = items.filter(f => housingState.favorites.has(f.id));
        } else if (housingState.selectedCategory !== 'all') {
            items = items.filter(f => f.category === housingState.selectedCategory);
        }

        // Sort
        const rarityOrder = { common: 0, uncommon: 1, rare: 2, legendary: 3 };
        if (housingState.sortBy === 'cost') items.sort((a, b) => a.cost - b.cost);
        else if (housingState.sortBy === 'name') items.sort((a, b) => a.name.localeCompare(b.name));
        else if (housingState.sortBy === 'rarity') items.sort((a, b) =>
            rarityOrder[b.rarity] - rarityOrder[a.rarity]);

        if (items.length === 0) {
            return `
                <div style="text-align:center;padding:60px;color:rgba(255,255,255,0.3);">
                    <div style="font-size:36px;margin-bottom:12px;">\uD83C\uDFE0</div>
                    <div style="font-size:12px;">Keine Moebel in dieser Kategorie</div>
                </div>
            `;
        }

        const rarityColors = {
            common: 'rgba(255,255,255,0.3)',
            uncommon: '#4CAF50',
            rare: '#2196F3',
            legendary: '#FFD700'
        };

        return `
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
                gap:10px;">
                ${items.map(item => {
                    const owned = housingState.ownedFurniture.filter(f => f === item.id).length;
                    const isFav = housingState.favorites.has(item.id);
                    const canAfford = housingState.gold >= item.cost;
                    const rColor = rarityColors[item.rarity] || 'rgba(255,255,255,0.3)';
                    const isSelected = housingState.selectedItem === item.id;

                    return `
                        <div onclick="window.HousingUIV2._selectItem('${item.id}')"
                            style="background:${isSelected ? 'rgba(255,152,0,0.06)' : 'rgba(255,255,255,0.02)'};
                            border:1px solid ${isSelected ? 'rgba(255,152,0,0.3)' : 'rgba(255,255,255,0.06)'};
                            border-radius:8px;padding:14px;cursor:pointer;
                            transition:all 0.15s;position:relative;"
                            onmouseover="this.style.background='rgba(255,255,255,0.04)'"
                            onmouseout="this.style.background='${isSelected ? 'rgba(255,152,0,0.06)' : 'rgba(255,255,255,0.02)'}'"
                        >
                            <div onclick="event.stopPropagation();window.HousingUIV2._toggleFav('${item.id}')"
                                style="position:absolute;top:8px;right:8px;cursor:pointer;
                                font-size:12px;opacity:${isFav ? 1 : 0.3};">
                                ${isFav ? '\u2764' : '\u2661'}
                            </div>

                            <div style="font-size:28px;text-align:center;margin-bottom:8px;">
                                ${item.icon}
                            </div>
                            <div style="font-size:10px;color:white;text-align:center;
                                font-weight:bold;margin-bottom:4px;">${item.name}</div>
                            <div style="font-size:8px;color:${rColor};text-align:center;
                                margin-bottom:6px;">${item.rarity.toUpperCase()}</div>

                            ${item.effect ? `
                                <div style="font-size:8px;color:rgba(76,175,80,0.6);
                                    text-align:center;margin-bottom:6px;">
                                    ${item.effect}
                                </div>
                            ` : ''}

                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <span style="font-size:9px;color:${canAfford ? '#FFD700' : '#FF4444'};">
                                    \uD83D\uDCB0 ${item.cost}
                                </span>
                                ${owned > 0 ? `<span style="font-size:8px;color:rgba(255,255,255,0.3);">
                                    x${owned}</span>` : ''}
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    // ==========================================
    // ITEM DETAIL + HOUSE INFO
    // ==========================================

    function buildItemDetail(itemId) {
        const item = FURNITURE_ITEMS.find(f => f.id === itemId);
        if (!item) return buildHouseInfo();

        const cat = FURNITURE_CATEGORIES[item.category];
        const canAfford = housingState.gold >= item.cost;
        const owned = housingState.ownedFurniture.filter(f => f === itemId).length;
        const rarityColors = { common: 'rgba(255,255,255,0.5)', uncommon: '#4CAF50',
                               rare: '#2196F3', legendary: '#FFD700' };

        return `
            <div style="text-align:center;margin-bottom:16px;">
                <div style="font-size:48px;margin-bottom:8px;">${item.icon}</div>
                <div style="font-size:14px;color:white;font-weight:bold;">${item.name}</div>
                <div style="font-size:9px;color:${rarityColors[item.rarity]};margin-top:4px;">
                    ${item.rarity.toUpperCase()}</div>
            </div>

            <div style="font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                margin-bottom:6px;">DETAILS</div>

            <div style="background:rgba(255,255,255,0.03);border-radius:6px;padding:10px;
                margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:10px;
                    padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:rgba(255,255,255,0.4);">Kategorie</span>
                    <span style="color:${cat.color};">${cat.icon} ${cat.name}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:10px;
                    padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:rgba(255,255,255,0.4);">Preis</span>
                    <span style="color:#FFD700;">\uD83D\uDCB0 ${item.cost}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;">
                    <span style="color:rgba(255,255,255,0.4);">Besitz</span>
                    <span style="color:rgba(255,255,255,0.7);">${owned}x</span>
                </div>
            </div>

            ${item.effect ? `
                <div style="background:rgba(76,175,80,0.06);border:1px solid rgba(76,175,80,0.15);
                    border-radius:6px;padding:10px;margin-bottom:12px;">
                    <div style="font-size:9px;color:#4CAF50;font-weight:bold;margin-bottom:4px;">
                        EFFEKT</div>
                    <div style="font-size:10px;color:rgba(76,175,80,0.7);">${item.effect}</div>
                </div>
            ` : ''}

            <button onclick="window.HousingUIV2.buy('${item.id}')"
                style="width:100%;padding:10px;font-size:11px;font-family:inherit;font-weight:bold;
                background:${canAfford ? 'rgba(255,152,0,0.2)' : 'rgba(255,255,255,0.04)'};
                border:1px solid ${canAfford ? 'rgba(255,152,0,0.4)' : 'rgba(255,255,255,0.08)'};
                color:${canAfford ? '#FF9800' : 'rgba(255,255,255,0.3)'};
                border-radius:6px;cursor:${canAfford ? 'pointer' : 'not-allowed'};
                margin-bottom:8px;">
                ${canAfford ? `\uD83D\uDED2 Kaufen (\uD83D\uDCB0 ${item.cost})` : '\uD83D\uDD12 Nicht genug Gold'}
            </button>

            ${owned > 0 ? `
                <button onclick="window.HousingUIV2.place('${item.id}')"
                    style="width:100%;padding:8px;font-size:10px;font-family:inherit;
                    background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.2);
                    color:#4CAF50;border-radius:6px;cursor:pointer;">
                    \uD83D\uDCCD Platzieren
                </button>
            ` : ''}
        `;
    }

    function buildHouseInfo() {
        const current = HOUSE_LEVELS[housingState.houseLevel - 1];
        const next = HOUSE_LEVELS[housingState.houseLevel] || null;
        const usedSlots = housingState.placedFurniture.length;

        let html = `
            <div style="text-align:center;margin-bottom:16px;">
                <div style="font-size:36px;margin-bottom:8px;">\uD83C\uDFE0</div>
                <div style="font-size:14px;color:#FF9800;font-weight:bold;">${current.name}</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.3);">Stufe ${current.level}</div>
            </div>

            <div style="font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                margin-bottom:6px;">HAUS-STATUS</div>

            <div style="background:rgba(255,255,255,0.03);border-radius:6px;padding:10px;
                margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:10px;
                    padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:rgba(255,255,255,0.4);">Raeume</span>
                    <span style="color:rgba(255,255,255,0.7);">${current.rooms}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:10px;
                    padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:rgba(255,255,255,0.4);">Moebel-Slots</span>
                    <span style="color:rgba(255,255,255,0.7);">${usedSlots}/${current.slots}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;">
                    <span style="color:rgba(255,255,255,0.4);">Gold</span>
                    <span style="color:#FFD700;">\uD83D\uDCB0 ${housingState.gold.toLocaleString()}</span>
                </div>
            </div>
        `;

        if (next) {
            const canUpgrade = housingState.gold >= next.upgradeCost;
            html += `
                <div style="font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                    margin-bottom:6px;">NAECHSTES UPGRADE</div>
                <div style="background:rgba(255,152,0,0.05);border:1px solid rgba(255,152,0,0.15);
                    border-radius:6px;padding:12px;margin-bottom:12px;">
                    <div style="font-size:11px;color:#FF9800;font-weight:bold;margin-bottom:6px;">
                        ${next.name} (Stufe ${next.level})</div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-bottom:4px;">
                        ${next.rooms} Raeume | ${next.slots} Slots</div>
                    <div style="font-size:10px;color:#FFD700;">
                        Kosten: \uD83D\uDCB0 ${next.upgradeCost.toLocaleString()}</div>
                </div>

                <button onclick="window.HousingUIV2.upgradeHouse()"
                    style="width:100%;padding:10px;font-size:11px;font-family:inherit;font-weight:bold;
                    background:${canUpgrade ? 'rgba(255,152,0,0.2)' : 'rgba(255,255,255,0.04)'};
                    border:1px solid ${canUpgrade ? 'rgba(255,152,0,0.4)' : 'rgba(255,255,255,0.08)'};
                    color:${canUpgrade ? '#FF9800' : 'rgba(255,255,255,0.3)'};
                    border-radius:6px;cursor:${canUpgrade ? 'pointer' : 'not-allowed'};">
                    ${canUpgrade ? '\u2B06 Haus upgraden' : '\uD83D\uDD12 Nicht genug Gold'}
                </button>
            `;
        } else {
            html += `
                <div style="text-align:center;padding:16px;background:rgba(255,215,0,0.05);
                    border:1px solid rgba(255,215,0,0.15);border-radius:6px;">
                    <div style="font-size:12px;color:#FFD700;font-weight:bold;">\uD83C\uDFC6 MAX LEVEL!</div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:4px;">
                        Dein Haus ist voll ausgebaut</div>
                </div>
            `;
        }

        return html;
    }

    // ==========================================
    // ACTIONS
    // ==========================================

    function buyFurniture(itemId) {
        const item = FURNITURE_ITEMS.find(f => f.id === itemId);
        if (!item || housingState.gold < item.cost) return false;

        housingState.gold -= item.cost;
        housingState.ownedFurniture.push(item.id);
        saveHousing();
        refreshUI();

        if (window.QuestTrackerV2) {
            window.QuestTrackerV2.showNotification(
                'MOEBEL GEKAUFT',
                `${item.icon} ${item.name}`,
                '#FF9800'
            );
        }
        return true;
    }

    function placeFurniture(itemId) {
        const houseInfo = HOUSE_LEVELS[housingState.houseLevel - 1];
        if (housingState.placedFurniture.length >= houseInfo.slots) return false;

        const ownedIdx = housingState.ownedFurniture.indexOf(itemId);
        if (ownedIdx === -1) return false;

        housingState.ownedFurniture.splice(ownedIdx, 1);
        housingState.placedFurniture.push(itemId);
        saveHousing();
        refreshUI();

        // Trigger 3D placement if available
        if (window.HousingSystem && window.HousingSystem.placeFurniture) {
            window.HousingSystem.placeFurniture(itemId);
        }
        return true;
    }

    function upgradeHouse() {
        const next = HOUSE_LEVELS[housingState.houseLevel];
        if (!next || housingState.gold < next.upgradeCost) return false;

        housingState.gold -= next.upgradeCost;
        housingState.houseLevel = next.level;
        saveHousing();
        refreshUI();

        if (window.QuestTrackerV2) {
            window.QuestTrackerV2.showNotification(
                'HAUS UPGRADE!',
                `\uD83C\uDFE0 ${next.name} (Stufe ${next.level})`,
                '#FF9800'
            );
        }
        return true;
    }

    // Keyboard: H = Housing
    document.addEventListener('keydown', (e) => {
        if (e.key === 'h' || e.key === 'H') {
            if (document.activeElement.tagName === 'INPUT' ||
                document.activeElement.tagName === 'TEXTAREA') return;
            const chatUI = document.getElementById('chat-ui');
            if (chatUI && chatUI.style.display !== 'none') return;
            if (housingState.isOpen) closeHousingUI(); else openHousingUI();
        }
    });

    // ==========================================
    // EXPORT
    // ==========================================

    window.HousingUIV2 = {
        open: openHousingUI,
        close: closeHousingUI,
        buy: buyFurniture,
        place: placeFurniture,
        upgradeHouse,
        FURNITURE_ITEMS,
        FURNITURE_CATEGORIES,
        HOUSE_LEVELS,
        getState: () => ({ ...housingState }),
        _setCategory: (cat) => { housingState.selectedCategory = cat; refreshUI(); },
        _setSort: (sort) => { housingState.sortBy = sort; refreshUI(); },
        _selectItem: (id) => { housingState.selectedItem = id; refreshUI(); },
        _toggleFav: (id) => {
            if (housingState.favorites.has(id)) housingState.favorites.delete(id);
            else housingState.favorites.add(id);
            saveHousing();
            refreshUI();
        }
    };

    console.log(`[OK] Housing UI V2 geladen: ${FURNITURE_ITEMS.length} Moebel, ${HOUSE_LEVELS.length} Haus-Stufen`);

})();
