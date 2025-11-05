// 🏰 CUSTOM BUILDING CONSTRUCTION SYSTEM
// Baut ECHTE Gebäude aus THREE.js Primitives

window.CustomBuildings = {
    buildWindmill: function(position, scale, parentGroup) {
        const mill = new THREE.Group();

        // Turm (Zylinder) - Dunkel/Schwarz
        const towerGeo = new THREE.CylinderGeometry(8, 10, 40, 8);
        const towerMat = new THREE.MeshStandardMaterial({
            color: 0x2C2C2C,
            roughness: 0.8
        });
        const tower = new THREE.Mesh(towerGeo, towerMat);
        tower.position.y = 20;
        tower.castShadow = true;
        tower.receiveShadow = true;
        mill.add(tower);

        // Dach (Kegel) - Braun
        const roofGeo = new THREE.ConeGeometry(12, 15, 8);
        const roofMat = new THREE.MeshStandardMaterial({
            color: 0x8B4513,
            roughness: 0.9
        });
        const roof = new THREE.Mesh(roofGeo, roofMat);
        roof.position.y = 47;
        roof.castShadow = true;
        mill.add(roof);

        // Mühlenflügel (4 Flügel)
        const bladeGroup = new THREE.Group();
        for (let i = 0; i < 4; i++) {
            const bladeGeo = new THREE.BoxGeometry(2, 20, 1);
            const bladeMat = new THREE.MeshStandardMaterial({
                color: 0x654321,
                roughness: 0.7
            });
            const blade = new THREE.Mesh(bladeGeo, bladeMat);
            blade.position.y = 10 * Math.sin(i * Math.PI / 2);
            blade.position.x = 10 * Math.cos(i * Math.PI / 2);
            blade.rotation.z = i * Math.PI / 2;
            blade.castShadow = true;
            bladeGroup.add(blade);
        }
        bladeGroup.position.set(0, 30, 10);
        bladeGroup.rotation.y = Math.PI / 4;
        mill.add(bladeGroup);

        // Tür
        const doorGeo = new THREE.BoxGeometry(6, 12, 0.5);
        const doorMat = new THREE.MeshStandardMaterial({
            color: 0x4A2511,
            roughness: 0.9
        });
        const door = new THREE.Mesh(doorGeo, doorMat);
        door.position.set(0, 6, 10);
        door.castShadow = true;
        mill.add(door);

        // Fenster (2 Stück, beleuchtet)
        const windowGeo = new THREE.BoxGeometry(3, 4, 0.3);
        const windowMat = new THREE.MeshStandardMaterial({
            color: 0xFFFFAA,
            emissive: 0x888800,
            emissiveIntensity: 0.3
        });

        const window1 = new THREE.Mesh(windowGeo, windowMat);
        window1.position.set(7, 25, 7);
        window1.rotation.y = -Math.PI / 4;
        mill.add(window1);

        const window2 = new THREE.Mesh(windowGeo, windowMat);
        window2.position.set(-7, 25, 7);
        window2.rotation.y = Math.PI / 4;
        mill.add(window2);

        mill.position.set(position[0], 0, position[2]);
        mill.scale.set(scale, scale, scale);
        mill.userData.buildingName = 'Schwarze Mühle';
        mill.userData.buildingRadius = 80;
        mill.userData.bladeGroup = bladeGroup; // Für spätere Animation

        parentGroup.add(mill);
        console.log('🏰 Schwarze Mühle gebaut!');
        return mill;
    },

    buildHouse: function(position, scale, color, name, radius, parentGroup) {
        const house = new THREE.Group();

        // Basis/Boden
        const baseGeo = new THREE.BoxGeometry(20, 1, 20);
        const baseMat = new THREE.MeshStandardMaterial({ color: 0x8B7355 });
        const base = new THREE.Mesh(baseGeo, baseMat);
        base.position.y = 0.5;
        base.receiveShadow = true;
        house.add(base);

        // Wände
        const wallGeo = new THREE.BoxGeometry(20, 15, 20);
        const wallMat = new THREE.MeshStandardMaterial({
            color: color,
            roughness: 0.8
        });
        const walls = new THREE.Mesh(wallGeo, wallMat);
        walls.position.y = 8.5;
        walls.castShadow = true;
        walls.receiveShadow = true;
        house.add(walls);

        // Dach (Pyramide)
        const roofGeo = new THREE.ConeGeometry(16, 10, 4);
        const roofMat = new THREE.MeshStandardMaterial({
            color: 0x8B4513,
            roughness: 0.9
        });
        const roof = new THREE.Mesh(roofGeo, roofMat);
        roof.position.y = 21;
        roof.rotation.y = Math.PI / 4;
        roof.castShadow = true;
        house.add(roof);

        // Tür
        const doorGeo = new THREE.BoxGeometry(5, 10, 0.3);
        const doorMat = new THREE.MeshStandardMaterial({ color: 0x4A2511 });
        const door = new THREE.Mesh(doorGeo, doorMat);
        door.position.set(0, 6, 10.2);
        door.castShadow = true;
        house.add(door);

        // Fenster (4 Stück)
        const windowGeo = new THREE.BoxGeometry(3, 3, 0.2);
        const windowMat = new THREE.MeshStandardMaterial({
            color: 0xADD8E6,
            emissive: 0x5588AA,
            emissiveIntensity: 0.2
        });
        [[6, 10, 10.2], [-6, 10, 10.2], [10.2, 10, 6], [10.2, 10, -6]].forEach((pos, i) => {
            const win = new THREE.Mesh(windowGeo, windowMat);
            win.position.set(...pos);
            if (i >= 2) win.rotation.y = Math.PI / 2;
            house.add(win);
        });

        house.position.set(position[0], 0, position[2]);
        house.scale.set(scale, scale, scale);
        house.userData.buildingName = name;
        house.userData.buildingRadius = radius;

        parentGroup.add(house);
        console.log(`🏠 ${name} gebaut!`);
        return house;
    },

    buildArena: function(position, scale, parentGroup) {
        const arena = new THREE.Group();

        // Arena-Boden (erhöht)
        const floorGeo = new THREE.CylinderGeometry(30, 30, 2, 16);
        const floorMat = new THREE.MeshStandardMaterial({
            color: 0x8B7355,
            roughness: 0.9
        });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.position.y = 1;
        floor.receiveShadow = true;
        arena.add(floor);

        // Umzäunung (16 Säulen im Kreis)
        for (let i = 0; i < 16; i++) {
            const angle = (i / 16) * Math.PI * 2;
            const pillarGeo = new THREE.BoxGeometry(3, 20, 3);
            const pillarMat = new THREE.MeshStandardMaterial({
                color: 0xCC0000,
                roughness: 0.7
            });
            const pillar = new THREE.Mesh(pillarGeo, pillarMat);
            pillar.position.set(
                Math.cos(angle) * 35,
                10,
                Math.sin(angle) * 35
            );
            pillar.castShadow = true;
            arena.add(pillar);
        }

        // Eingangs-Tor (2 große Säulen)
        const gateGeo = new THREE.BoxGeometry(4, 25, 4);
        const gateMat = new THREE.MeshStandardMaterial({ color: 0x8B0000 });

        const gate1 = new THREE.Mesh(gateGeo, gateMat);
        gate1.position.set(-8, 12.5, 35);
        gate1.castShadow = true;
        arena.add(gate1);

        const gate2 = new THREE.Mesh(gateGeo, gateMat);
        gate2.position.set(8, 12.5, 35);
        gate2.castShadow = true;
        arena.add(gate2);

        // Tor-Überdachung
        const archGeo = new THREE.BoxGeometry(20, 3, 3);
        const archMat = new THREE.MeshStandardMaterial({ color: 0x8B0000 });
        const arch = new THREE.Mesh(archGeo, archMat);
        arch.position.set(0, 25, 35);
        arch.castShadow = true;
        arena.add(arch);

        arena.position.set(position[0], 0, position[2]);
        arena.scale.set(scale, scale, scale);
        arena.userData.buildingName = 'Kampfarena';
        arena.userData.buildingRadius = 50;

        parentGroup.add(arena);
        console.log('⚔️ Kampfarena gebaut!');
        return arena;
    }
};

console.log('🏗️ Custom Buildings System loaded!');
