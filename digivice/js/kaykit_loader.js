// KAYKIT ASSET LOADER
(function() {
    const ASSETS_ROOT = 'http://localhost:8001/assets/';
    const loadedModels = {};
    let loader = null;
    let config = null;
    let roomMap = {};

    function init() {
        if (loader) {
            return;
        }
        if (typeof THREE === 'undefined' || typeof THREE.GLTFLoader === 'undefined') {
            setTimeout(init, 500);
            return;
        }

        loader = new THREE.GLTFLoader();
        console.log('✅ KayKit Loader initialized');
        loadRoomConfig();
    }

    async function loadRoomConfig() {
        try {
            const response = await fetch('http://localhost:8001/config/room_config_detailed.json');
            config = await response.json();
            console.log('📦 Room config loaded:', config);
            roomMap = {};

            if (Array.isArray(config.rooms)) {
                config.rooms.forEach(room => {
                    if (room && room.name) {
                        roomMap[room.name] = room;
                    }
                });
            }

            // LAZY LOADING: Nur Character + erster Raum werden sofort geladen
            const defaultRoom = 'Wohnzimmer';
            console.log(`🎯 Lazy Loading: Lade nur ${defaultRoom} beim Start`);

            // Lade Character-Modell (Skeleton_Mage wird separat in 3d_scene.js geladen)
            // Lade nur Assets vom Startroom
            if (roomMap[defaultRoom]) {
                preloadRoomAssets(defaultRoom);
            }

            document.dispatchEvent(new CustomEvent('kaykit:configReady'));
        } catch (error) {
            console.log('ℹ️ No room config found, using defaults');
        }
    }

    function preloadRoomAssets(roomName) {
        const room = roomMap[roomName];
        if (!room) return;

        const assetsToLoad = new Set();

        if (room?.floor?.model) {
            assetsToLoad.add(room.floor.model);
        }
        if (room?.walls?.model) {
            assetsToLoad.add(room.walls.model);
        }
        if (Array.isArray(room?.props)) {
            room.props.forEach(prop => {
                if (prop?.model) {
                    assetsToLoad.add(prop.model);
                }
            });
        }

        console.log(`📦 Loading room "${roomName}": ${assetsToLoad.size} assets`);
        assetsToLoad.forEach(path => preloadAsset(path));
    }

    function preloadAsset(path, alias) {
        if (!loader) {
            return;
        }
        if (!path || path === '__none__') {
            return;
        }

        const fullPath = ASSETS_ROOT + path;
        const key = alias || path;

        loader.load(
            fullPath,
            gltf => {
                loadedModels[key] = gltf.scene;
                console.log(`✅ Loaded ${key}: ${path}`);
                dispatchModelLoaded(key);
            },
            undefined,
            error => {
                console.log(`ℹ️ Could not load ${key}: ${error.message || error}`);
            }
        );
    }

    function dispatchModelLoaded(name) {
        document.dispatchEvent(new CustomEvent('kaykit:modelLoaded', {
            detail: { name }
        }));
    }

    function getModel(name) {
        return loadedModels[name] || null;
    }

    function hasModel(name) {
        return !!loadedModels[name];
    }

    function getConfig() {
        return config;
    }

    function getRoomConfig(name) {
        if (!name || !roomMap[name]) {
            return null;
        }
        try {
            return structuredClone(roomMap[name]);
        } catch (err) {
            return JSON.parse(JSON.stringify(roomMap[name]));
        }
    }

    function loadRoomOnDemand(roomName) {
        if (!roomMap[roomName]) {
            console.log(`⚠️ Room "${roomName}" not found in config`);
            return;
        }

        // Prüfe ob Assets bereits geladen sind
        const room = roomMap[roomName];
        const assetsNeeded = new Set();

        if (room?.floor?.model && !hasModel(room.floor.model)) {
            assetsNeeded.add(room.floor.model);
        }
        if (room?.walls?.model && !hasModel(room.walls.model)) {
            assetsNeeded.add(room.walls.model);
        }
        if (Array.isArray(room?.props)) {
            room.props.forEach(prop => {
                if (prop?.model && !hasModel(prop.model)) {
                    assetsNeeded.add(prop.model);
                }
            });
        }

        if (assetsNeeded.size === 0) {
            console.log(`✅ Room "${roomName}" already loaded`);
            return;
        }

        console.log(`📦 Lazy loading room "${roomName}": ${assetsNeeded.size} new assets`);
        assetsNeeded.forEach(path => preloadAsset(path));
    }

    window.KayKitLoader = {
        init,
        getModel,
        hasModel,
        getConfig,
        getRoomConfig,
        loadRoomOnDemand,
        loadedModels
    };

    if (typeof THREE !== 'undefined') {
        setTimeout(init, 500);
    } else {
        setTimeout(init, 1000);
    }
})();
