/**
 * World Map 3D Viewer - Najika World
 * ====================================
 * Interaktive 3D-Weltkarte mit:
 * - Three.js Terrain-Rendering (Hex-Grid)
 * - 8 Regionen mit einzigartigen Farben + Markern
 * - Fog of War (unentdeckte Gebiete)
 * - Quest-Marker, NPC-Marker, Teleporter
 * - Kamera: Pan, Zoom, Rotate
 * - Region-Info Popup bei Hover/Click
 * - Minimap-Mode (klein) + Fullscreen-Mode
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // REGION DATABASE
    // ==========================================

    const REGIONS = {
        heisse_duenen: {
            name: 'Heisse Duenen',
            icon: '\uD83C\uDFDC',
            color: 0xD4A574,
            accent: '#D4A574',
            position: { x: 3, z: -2 },
            size: 2.5,
            height: 0.3,
            description: 'Endlose Sandduenen unter sengender Sonne',
            biome: 'desert',
            level: '5-15',
            features: ['Oasen', 'Sandwuermer', 'Ruinen']
        },
        samtmoos_tiefwald: {
            name: 'Samtmoos Tiefwald',
            icon: '\uD83C\uDF32',
            color: 0x2D5A27,
            accent: '#2D5A27',
            position: { x: -2, z: -1 },
            size: 3,
            height: 0.6,
            description: 'Uralter Wald mit moosbewachsenen Riesen',
            biome: 'forest',
            level: '1-10',
            features: ['Waldgeister', 'Heilkraeuter', 'Wolfsrudel']
        },
        salzwind_kueste: {
            name: 'Salzwind Kueste',
            icon: '\uD83C\uDF0A',
            color: 0x4A90D9,
            accent: '#4A90D9',
            position: { x: 4, z: 2 },
            size: 2.8,
            height: 0.1,
            description: 'Stuermische Kueste mit verborgenen Grotten',
            biome: 'coast',
            level: '8-18',
            features: ['Piraten', 'Seeungeheuer', 'Leuchtturm']
        },
        blitzebene: {
            name: 'Blitzebene',
            icon: '\u26A1',
            color: 0xB8860B,
            accent: '#B8860B',
            position: { x: 0, z: -3.5 },
            size: 2.5,
            height: 0.2,
            description: 'Flache Steppe unter ewigem Gewitterhimmel',
            biome: 'plains',
            level: '10-20',
            features: ['Blitztuerme', 'Nomaden', 'Elementare']
        },
        gruenschlamm_sumpf: {
            name: 'Gruenschlamm Sumpf',
            icon: '\uD83E\uDEB9',
            color: 0x4A6741,
            accent: '#4A6741',
            position: { x: -3.5, z: 2 },
            size: 2.2,
            height: -0.1,
            description: 'Giftiger Sumpf voller Alchemie-Zutaten',
            biome: 'swamp',
            level: '12-22',
            features: ['Giftpilze', 'Hexenhuetten', 'Schleimhoehlen']
        },
        reich_der_drei: {
            name: 'Reich der Drei',
            icon: '\u2744',
            color: 0xADD8E6,
            accent: '#ADD8E6',
            position: { x: -1, z: -4.5 },
            size: 2.8,
            height: 0.8,
            description: 'Eisiges Koenigreich der drei Fuersten',
            biome: 'ice',
            level: '18-28',
            features: ['Eispalast', 'Frostdrachen', 'Kristallminen']
        },
        magmastroeme: {
            name: 'Magmastroeme',
            icon: '\uD83C\uDF0B',
            color: 0xCC3300,
            accent: '#CC3300',
            position: { x: 2, z: 4 },
            size: 2,
            height: 0.5,
            description: 'Vulkanisches Gebiet mit fliessender Lava',
            biome: 'volcano',
            level: '20-30',
            features: ['Schmieden', 'Feuerelementare', 'Obsidianhort']
        },
        tiefenhoehlen: {
            name: 'Tiefenhoehlen',
            icon: '\uD83D\uDC8E',
            color: 0x6A0DAD,
            accent: '#6A0DAD',
            position: { x: 0, z: 3 },
            size: 2,
            height: -0.3,
            description: 'Kristallbesetzte Hoehlen tief unter der Erde',
            biome: 'cave',
            level: '25-35',
            features: ['Kristallspinnen', 'Prismenhoehle', 'Unterweltsee']
        }
    };

    const GOETTERFELS = {
        name: 'Goetterfels',
        icon: '\uD83C\uDFD4',
        color: 0xFFD700,
        accent: '#FFD700',
        position: { x: 0, z: 0 },
        size: 1.5,
        height: 1.5,
        description: 'Zentrum der Welt - Sitz der Goetter',
        biome: 'divine',
        level: '35+',
        features: ['Goettertempel', 'Endgame-Dungeon', 'Najika Ursprung']
    };

    // ==========================================
    // MAP STATE
    // ==========================================

    let mapState = {
        isOpen: false,
        isFullscreen: false,
        discoveredRegions: new Set(['samtmoos_tiefwald']), // Start-Region
        questMarkers: [],
        npcMarkers: [],
        playerPosition: { x: -2, z: -1 }, // Start in Samtmoos
        selectedRegion: null,
        scene: null,
        camera: null,
        renderer: null,
        controls: null,
        regionMeshes: {},
        markerMeshes: [],
        animationId: null,
        container: null
    };

    // Load discovered regions
    try {
        const saved = JSON.parse(localStorage.getItem('najika_discovered_regions'));
        if (saved) mapState.discoveredRegions = new Set(saved);
    } catch(e) { /* default */ }

    function saveDiscoveredRegions() {
        try {
            localStorage.setItem('najika_discovered_regions',
                JSON.stringify([...mapState.discoveredRegions]));
        } catch(e) { /* silent */ }
    }

    // ==========================================
    // THREE.JS MAP SETUP
    // ==========================================

    function createMap(container) {
        if (typeof THREE === 'undefined') {
            console.warn('[WORLD MAP] THREE.js nicht geladen');
            return false;
        }

        const width = container.clientWidth;
        const height = container.clientHeight;

        // Scene
        mapState.scene = new THREE.Scene();
        mapState.scene.background = new THREE.Color(0x0a0a1a);
        mapState.scene.fog = new THREE.FogExp2(0x0a0a1a, 0.04);

        // Camera (isometric-ish)
        mapState.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
        mapState.camera.position.set(0, 12, 8);
        mapState.camera.lookAt(0, 0, 0);

        // Renderer
        mapState.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        mapState.renderer.setSize(width, height);
        mapState.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(mapState.renderer.domElement);

        // Lights
        const ambientLight = new THREE.AmbientLight(0x404060, 0.6);
        mapState.scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(5, 10, 5);
        mapState.scene.add(dirLight);

        // Grid Floor
        const gridHelper = new THREE.GridHelper(20, 40, 0x111133, 0x111122);
        gridHelper.position.y = -0.05;
        mapState.scene.add(gridHelper);

        // Build Regions
        buildRegions();

        // Build Goetterfels (center)
        buildGoetterfels();

        // Player Marker
        buildPlayerMarker();

        // Connection Lines between regions
        buildConnectionLines();

        // Mouse interaction
        setupMapInteraction(container);

        return true;
    }

    function buildRegions() {
        Object.entries(REGIONS).forEach(([key, region]) => {
            const isDiscovered = mapState.discoveredRegions.has(key);

            // Region terrain (rounded hexagonal prism)
            const geometry = new THREE.CylinderGeometry(
                region.size * 0.5,
                region.size * 0.55,
                Math.max(0.1, region.height + 0.3),
                6  // hexagonal
            );

            const material = new THREE.MeshPhongMaterial({
                color: isDiscovered ? region.color : 0x222244,
                transparent: true,
                opacity: isDiscovered ? 0.85 : 0.3,
                flatShading: true
            });

            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(region.position.x, region.height * 0.5, region.position.z);
            mesh.userData = { regionKey: key, type: 'region' };

            mapState.scene.add(mesh);
            mapState.regionMeshes[key] = mesh;

            // Region Label (sprite)
            if (isDiscovered) {
                const canvas = document.createElement('canvas');
                canvas.width = 256;
                canvas.height = 64;
                const ctx = canvas.getContext('2d');
                ctx.fillStyle = 'rgba(0,0,0,0.6)';
                ctx.fillRect(0, 0, 256, 64);
                ctx.font = 'bold 20px monospace';
                ctx.fillStyle = 'white';
                ctx.textAlign = 'center';
                ctx.fillText(region.name, 128, 38);

                const texture = new THREE.CanvasTexture(canvas);
                const spriteMaterial = new THREE.SpriteMaterial({ map: texture, transparent: true });
                const sprite = new THREE.Sprite(spriteMaterial);
                sprite.position.set(region.position.x, region.height + 1.2, region.position.z);
                sprite.scale.set(2.5, 0.6, 1);
                mapState.scene.add(sprite);
            }

            // Biome particles
            if (isDiscovered) {
                addBiomeParticles(region);
            }
        });
    }

    function buildGoetterfels() {
        // Central golden peak
        const geometry = new THREE.ConeGeometry(0.8, 2, 8);
        const material = new THREE.MeshPhongMaterial({
            color: 0xFFD700,
            emissive: 0x332200,
            flatShading: true
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(0, 1, 0);
        mesh.userData = { regionKey: 'goetterfels', type: 'region' };
        mapState.scene.add(mesh);

        // Glow ring
        const ringGeometry = new THREE.TorusGeometry(1.2, 0.05, 8, 32);
        const ringMaterial = new THREE.MeshBasicMaterial({ color: 0xFFD700, transparent: true, opacity: 0.4 });
        const ring = new THREE.Mesh(ringGeometry, ringMaterial);
        ring.position.set(0, 0.5, 0);
        ring.rotation.x = Math.PI / 2;
        mapState.scene.add(ring);

        // Label
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');
        ctx.font = 'bold 22px monospace';
        ctx.fillStyle = '#FFD700';
        ctx.textAlign = 'center';
        ctx.fillText('Goetterfels', 128, 40);
        const texture = new THREE.CanvasTexture(canvas);
        const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(spriteMat);
        sprite.position.set(0, 2.8, 0);
        sprite.scale.set(2.5, 0.6, 1);
        mapState.scene.add(sprite);
    }

    function buildPlayerMarker() {
        const geometry = new THREE.ConeGeometry(0.15, 0.4, 4);
        const material = new THREE.MeshBasicMaterial({ color: 0x00FF00 });
        const marker = new THREE.Mesh(geometry, material);
        marker.position.set(mapState.playerPosition.x, 1.5, mapState.playerPosition.z);
        marker.rotation.x = Math.PI; // point down
        marker.userData = { type: 'player' };
        mapState.scene.add(marker);
        mapState.playerMarker = marker;
    }

    function buildConnectionLines() {
        const connections = [
            ['samtmoos_tiefwald', 'goetterfels'],
            ['heisse_duenen', 'goetterfels'],
            ['salzwind_kueste', 'goetterfels'],
            ['blitzebene', 'goetterfels'],
            ['gruenschlamm_sumpf', 'goetterfels'],
            ['reich_der_drei', 'goetterfels'],
            ['magmastroeme', 'goetterfels'],
            ['tiefenhoehlen', 'goetterfels'],
            ['samtmoos_tiefwald', 'gruenschlamm_sumpf'],
            ['heisse_duenen', 'blitzebene'],
            ['salzwind_kueste', 'magmastroeme'],
            ['reich_der_drei', 'blitzebene']
        ];

        const lineMaterial = new THREE.LineBasicMaterial({
            color: 0x333355,
            transparent: true,
            opacity: 0.3
        });

        connections.forEach(([from, to]) => {
            const fromPos = from === 'goetterfels' ?
                { x: 0, z: 0 } :
                REGIONS[from]?.position || { x: 0, z: 0 };
            const toPos = to === 'goetterfels' ?
                { x: 0, z: 0 } :
                REGIONS[to]?.position || { x: 0, z: 0 };

            const points = [
                new THREE.Vector3(fromPos.x, 0.05, fromPos.z),
                new THREE.Vector3(toPos.x, 0.05, toPos.z)
            ];
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const line = new THREE.Line(geometry, lineMaterial);
            mapState.scene.add(line);
        });
    }

    function addBiomeParticles(region) {
        const particleCount = 20;
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        const color = new THREE.Color(region.color);

        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            const radius = Math.random() * region.size * 0.4;
            positions[i * 3] = region.position.x + Math.cos(angle) * radius;
            positions[i * 3 + 1] = region.height + 0.3 + Math.random() * 0.5;
            positions[i * 3 + 2] = region.position.z + Math.sin(angle) * radius;

            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.08,
            vertexColors: true,
            transparent: true,
            opacity: 0.6
        });

        const particles = new THREE.Points(geometry, material);
        particles.userData = { type: 'particles', regionKey: region };
        mapState.scene.add(particles);
    }

    // ==========================================
    // MAP INTERACTION
    // ==========================================

    function setupMapInteraction(container) {
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        // Camera controls (simple orbit)
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let cameraAngle = 0;
        let cameraHeight = 12;
        let cameraDistance = 8;
        let cameraTarget = new THREE.Vector3(0, 0, 0);

        function updateCamera() {
            mapState.camera.position.x = cameraTarget.x + Math.sin(cameraAngle) * cameraDistance;
            mapState.camera.position.z = cameraTarget.z + Math.cos(cameraAngle) * cameraDistance;
            mapState.camera.position.y = cameraHeight;
            mapState.camera.lookAt(cameraTarget);
        }

        container.addEventListener('mousedown', (e) => {
            isDragging = true;
            dragStart = { x: e.clientX, y: e.clientY };
        });

        container.addEventListener('mousemove', (e) => {
            if (isDragging) {
                const dx = e.clientX - dragStart.x;
                const dy = e.clientY - dragStart.y;
                if (e.buttons === 1) { // Left: rotate
                    cameraAngle += dx * 0.005;
                    cameraHeight = Math.max(4, Math.min(20, cameraHeight - dy * 0.02));
                } else if (e.buttons === 2) { // Right: pan
                    const right = new THREE.Vector3();
                    mapState.camera.getWorldDirection(right);
                    right.cross(mapState.camera.up).normalize();
                    cameraTarget.add(right.multiplyScalar(-dx * 0.02));
                    cameraTarget.z += dy * 0.02;
                }
                dragStart = { x: e.clientX, y: e.clientY };
                updateCamera();
            }

            // Hover detection
            const rect = container.getBoundingClientRect();
            mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, mapState.camera);
            const meshes = Object.values(mapState.regionMeshes);
            const intersects = raycaster.intersectObjects(meshes);

            // Reset all highlights
            meshes.forEach(m => { m.material.emissive && m.material.emissive.setHex(0x000000); });

            if (intersects.length > 0) {
                const obj = intersects[0].object;
                if (obj.material.emissive) {
                    obj.material.emissive.setHex(0x222222);
                }
                container.style.cursor = 'pointer';
            } else {
                container.style.cursor = isDragging ? 'grabbing' : 'grab';
            }
        });

        container.addEventListener('mouseup', () => { isDragging = false; });

        // Click: select region
        container.addEventListener('click', (e) => {
            const rect = container.getBoundingClientRect();
            mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, mapState.camera);
            const meshes = Object.values(mapState.regionMeshes);
            const intersects = raycaster.intersectObjects(meshes);

            if (intersects.length > 0) {
                const regionKey = intersects[0].object.userData.regionKey;
                selectRegion(regionKey);
            } else {
                hideRegionInfo();
            }
        });

        // Zoom
        container.addEventListener('wheel', (e) => {
            e.preventDefault();
            cameraDistance = Math.max(3, Math.min(18, cameraDistance + e.deltaY * 0.01));
            updateCamera();
        });

        // Prevent context menu
        container.addEventListener('contextmenu', (e) => e.preventDefault());

        updateCamera();
    }

    // ==========================================
    // REGION INFO PANEL
    // ==========================================

    function selectRegion(regionKey) {
        const region = regionKey === 'goetterfels' ? GOETTERFELS : REGIONS[regionKey];
        if (!region) return;

        mapState.selectedRegion = regionKey;
        const isDiscovered = regionKey === 'goetterfels' || mapState.discoveredRegions.has(regionKey);

        const existing = document.getElementById('map-region-info');
        if (existing) existing.remove();

        const panel = document.createElement('div');
        panel.id = 'map-region-info';
        panel.style.cssText = `
            position:absolute; bottom:20px; left:20px;
            background:linear-gradient(135deg, rgba(10,10,30,0.95), rgba(5,5,15,0.98));
            border:2px solid ${isDiscovered ? region.accent : 'rgba(255,255,255,0.1)'};
            border-radius:12px; padding:18px; color:white;
            font-family:'Courier New',monospace;
            min-width:280px; max-width:350px;
            box-shadow:0 8px 32px rgba(0,0,0,0.8);
        `;

        if (!isDiscovered) {
            panel.innerHTML = `
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                    <span style="font-size:28px;">\u2753</span>
                    <div>
                        <div style="font-size:14px;font-weight:bold;color:rgba(255,255,255,0.4);">
                            Unentdeckte Region</div>
                        <div style="font-size:10px;color:rgba(255,255,255,0.2);">
                            Erkunde die Welt um diese Region freizuschalten!</div>
                    </div>
                </div>
            `;
        } else {
            panel.innerHTML = `
                <button onclick="document.getElementById('map-region-info').remove()"
                    style="position:absolute;top:6px;right:10px;background:none;border:none;
                    color:rgba(255,255,255,0.4);font-size:14px;cursor:pointer;">x</button>

                <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                    <span style="font-size:28px;">${region.icon}</span>
                    <div>
                        <div style="font-size:14px;font-weight:bold;">${region.name}</div>
                        <div style="font-size:10px;color:rgba(255,255,255,0.4);">
                            Level ${region.level} | ${region.biome}
                        </div>
                    </div>
                </div>

                <div style="font-size:10px;color:rgba(255,255,255,0.6);line-height:1.5;
                    margin-bottom:12px;">
                    ${region.description}
                </div>

                <div style="font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:1px;
                    margin-bottom:6px;">BESONDERHEITEN</div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;">
                    ${region.features.map(f => `
                        <span style="font-size:9px;padding:3px 8px;
                            background:rgba(255,255,255,0.05);
                            border:1px solid rgba(255,255,255,0.1);
                            border-radius:4px;color:rgba(255,255,255,0.6);">${f}</span>
                    `).join('')}
                </div>

                <button onclick="window.WorldMap3D.travelTo('${regionKey}')"
                    style="width:100%;padding:8px;font-size:10px;font-family:inherit;
                    background:rgba(76,175,80,0.15);border:1px solid rgba(76,175,80,0.3);
                    color:#4CAF50;border-radius:6px;cursor:pointer;">
                    \uD83D\uDEB6 Hierhin reisen
                </button>
            `;
        }

        const container = document.getElementById('world-map-container');
        if (container) container.appendChild(panel);
    }

    function hideRegionInfo() {
        const el = document.getElementById('map-region-info');
        if (el) el.remove();
        mapState.selectedRegion = null;
    }

    // ==========================================
    // MAP UI (Container + Controls)
    // ==========================================

    function openMap(fullscreen) {
        if (mapState.isOpen) {
            closeMap();
            return;
        }

        mapState.isOpen = true;
        mapState.isFullscreen = fullscreen !== false;

        const container = document.createElement('div');
        container.id = 'world-map-container';
        container.style.cssText = mapState.isFullscreen ? `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.98);z-index:9500;
        ` : `
            position:fixed;bottom:80px;right:20px;
            width:400px;height:300px;
            background:rgba(0,0,0,0.95);z-index:600;
            border:2px solid rgba(76,175,80,0.3);border-radius:12px;
            overflow:hidden;
        `;

        // Controls overlay
        const controls = document.createElement('div');
        controls.style.cssText = `
            position:absolute;top:10px;left:10px;z-index:10;
            display:flex;gap:8px;
        `;
        controls.innerHTML = `
            <button onclick="window.WorldMap3D.close()"
                style="padding:6px 12px;font-size:10px;font-family:'Courier New',monospace;
                background:rgba(244,67,54,0.2);border:1px solid rgba(244,67,54,0.3);
                color:#F44336;border-radius:4px;cursor:pointer;">ESC</button>
            <button onclick="window.WorldMap3D.toggleFullscreen()"
                style="padding:6px 12px;font-size:10px;font-family:'Courier New',monospace;
                background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.2);
                color:#4CAF50;border-radius:4px;cursor:pointer;">
                ${mapState.isFullscreen ? 'Mini' : 'Fullscreen'}</button>
        `;
        container.appendChild(controls);

        // Legend
        if (mapState.isFullscreen) {
            const legend = document.createElement('div');
            legend.style.cssText = `
                position:absolute;top:10px;right:10px;z-index:10;
                background:rgba(10,10,30,0.9);border:1px solid rgba(255,255,255,0.1);
                border-radius:8px;padding:10px 14px;
                font-family:'Courier New',monospace;
            `;
            legend.innerHTML = `
                <div style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:1px;
                    margin-bottom:8px;">LEGENDE</div>
                ${Object.entries(REGIONS).map(([key, r]) => `
                    <div style="font-size:10px;display:flex;align-items:center;gap:6px;
                        padding:2px 0;color:${mapState.discoveredRegions.has(key) ?
                        'rgba(255,255,255,0.7)' : 'rgba(255,255,255,0.2)'};">
                        <span style="width:8px;height:8px;border-radius:2px;
                            background:${mapState.discoveredRegions.has(key) ? r.accent : '#333'};
                            display:inline-block;"></span>
                        ${r.icon} ${r.name}
                    </div>
                `).join('')}
                <div style="font-size:10px;display:flex;align-items:center;gap:6px;
                    padding:2px 0;color:#FFD700;margin-top:4px;">
                    <span style="width:8px;height:8px;border-radius:2px;
                        background:#FFD700;display:inline-block;"></span>
                    \uD83C\uDFD4 Goetterfels
                </div>
            `;
            container.appendChild(legend);
        }

        document.body.appendChild(container);
        mapState.container = container;

        // Initialize Three.js
        if (!createMap(container)) {
            // Fallback: 2D canvas map
            render2DFallback(container);
        }

        // Start render loop
        animateMap();

        // ESC handler
        mapState._escHandler = (e) => {
            if (e.key === 'Escape') closeMap();
        };
        document.addEventListener('keydown', mapState._escHandler);
    }

    function closeMap() {
        mapState.isOpen = false;
        if (mapState.animationId) {
            cancelAnimationFrame(mapState.animationId);
            mapState.animationId = null;
        }
        if (mapState.renderer) {
            mapState.renderer.dispose();
            mapState.renderer = null;
        }
        mapState.scene = null;
        mapState.camera = null;
        mapState.regionMeshes = {};

        const container = document.getElementById('world-map-container');
        if (container) container.remove();

        if (mapState._escHandler) {
            document.removeEventListener('keydown', mapState._escHandler);
        }
    }

    function toggleFullscreen() {
        const wasFullscreen = mapState.isFullscreen;
        closeMap();
        openMap(!wasFullscreen);
    }

    // ==========================================
    // ANIMATION LOOP
    // ==========================================

    let mapTime = 0;

    function animateMap() {
        if (!mapState.isOpen || !mapState.renderer) return;

        mapState.animationId = requestAnimationFrame(animateMap);
        mapTime += 0.016;

        // Animate player marker (bob)
        if (mapState.playerMarker) {
            mapState.playerMarker.position.y = 1.5 + Math.sin(mapTime * 3) * 0.15;
        }

        // Animate particles
        if (mapState.scene) {
            mapState.scene.children.forEach(child => {
                if (child.userData && child.userData.type === 'particles') {
                    const pos = child.geometry.attributes.position;
                    for (let i = 0; i < pos.count; i++) {
                        pos.array[i * 3 + 1] += Math.sin(mapTime * 2 + i) * 0.002;
                    }
                    pos.needsUpdate = true;
                }
            });
        }

        mapState.renderer.render(mapState.scene, mapState.camera);
    }

    // ==========================================
    // 2D FALLBACK (if THREE.js not available)
    // ==========================================

    function render2DFallback(container) {
        const canvas = document.createElement('canvas');
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        canvas.style.cssText = 'width:100%;height:100%;';
        container.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        const cx = w / 2;
        const cy = h / 2;
        const scale = Math.min(w, h) / 14;

        // Background
        ctx.fillStyle = '#0a0a1a';
        ctx.fillRect(0, 0, w, h);

        // Grid
        ctx.strokeStyle = 'rgba(255,255,255,0.03)';
        for (let x = 0; x < w; x += 30) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
        for (let y = 0; y < h; y += 30) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }

        // Connection lines
        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
        ctx.lineWidth = 1;
        Object.values(REGIONS).forEach(r => {
            ctx.beginPath();
            ctx.moveTo(cx + r.position.x * scale, cy + r.position.z * scale);
            ctx.lineTo(cx, cy);
            ctx.stroke();
        });

        // Goetterfels
        ctx.beginPath();
        ctx.arc(cx, cy, 12, 0, Math.PI * 2);
        ctx.fillStyle = '#FFD700';
        ctx.fill();
        ctx.font = 'bold 10px monospace';
        ctx.fillStyle = '#FFD700';
        ctx.textAlign = 'center';
        ctx.fillText('Goetterfels', cx, cy - 18);

        // Regions
        Object.entries(REGIONS).forEach(([key, r]) => {
            const rx = cx + r.position.x * scale;
            const ry = cy + r.position.z * scale;
            const isDiscovered = mapState.discoveredRegions.has(key);

            ctx.beginPath();
            ctx.arc(rx, ry, r.size * scale * 0.2, 0, Math.PI * 2);
            ctx.fillStyle = isDiscovered ? r.accent : 'rgba(255,255,255,0.1)';
            ctx.globalAlpha = isDiscovered ? 0.8 : 0.3;
            ctx.fill();
            ctx.globalAlpha = 1;

            if (isDiscovered) {
                ctx.font = '10px monospace';
                ctx.fillStyle = 'white';
                ctx.fillText(r.name, rx, ry - r.size * scale * 0.2 - 6);
                ctx.font = '16px serif';
                ctx.fillText(r.icon, rx, ry + 5);
            }
        });

        // Player
        const px = cx + mapState.playerPosition.x * scale;
        const py = cy + mapState.playerPosition.z * scale;
        ctx.beginPath();
        ctx.arc(px, py, 5, 0, Math.PI * 2);
        ctx.fillStyle = '#00FF00';
        ctx.fill();

        // Click handler for 2D
        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = (e.clientX - rect.left) * (canvas.width / rect.width);
            const my = (e.clientY - rect.top) * (canvas.height / rect.height);

            Object.entries(REGIONS).forEach(([key, r]) => {
                const rx = cx + r.position.x * scale;
                const ry = cy + r.position.z * scale;
                const dist = Math.sqrt((mx - rx) ** 2 + (my - ry) ** 2);
                if (dist < r.size * scale * 0.25) {
                    selectRegion(key);
                }
            });
        });
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    function discoverRegion(regionKey) {
        if (!REGIONS[regionKey]) return false;
        if (mapState.discoveredRegions.has(regionKey)) return false;

        mapState.discoveredRegions.add(regionKey);
        saveDiscoveredRegions();

        if (window.QuestTrackerV2) {
            window.QuestTrackerV2.showNotification(
                'REGION ENTDECKT',
                `${REGIONS[regionKey].icon} ${REGIONS[regionKey].name}`,
                REGIONS[regionKey].accent
            );
        }

        return true;
    }

    function travelTo(regionKey) {
        const region = REGIONS[regionKey] || (regionKey === 'goetterfels' ? GOETTERFELS : null);
        if (!region) return;

        mapState.playerPosition = { ...region.position };

        if (window.GameEvents) {
            window.GameEvents.emit('player:travel', { region: regionKey });
        }

        closeMap();
    }

    function setPlayerPosition(x, z) {
        mapState.playerPosition = { x, z };
    }

    // Keyboard: M = Map
    document.addEventListener('keydown', (e) => {
        if (e.key === 'm' || e.key === 'M') {
            const chatUI = document.getElementById('chat-ui');
            if (chatUI && chatUI.style.display !== 'none') return;
            if (mapState.isOpen) {
                closeMap();
            } else {
                openMap(true);
            }
        }
    });

    // ==========================================
    // EXPORT
    // ==========================================

    window.WorldMap3D = {
        REGIONS,
        GOETTERFELS,
        open: openMap,
        close: closeMap,
        toggleFullscreen,
        discoverRegion,
        travelTo,
        setPlayerPosition,
        getDiscoveredRegions: () => [...mapState.discoveredRegions],
        isOpen: () => mapState.isOpen
    };

    console.log(`[OK] World Map 3D geladen: ${Object.keys(REGIONS).length} Regionen + Goetterfels`);

})();
