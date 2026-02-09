// ============================================================
// COMPANION 3D - Najika folgt dem Spieler als 3D-Begleiterin
// Kuja = AnimatedCharacter (Spieler), Najika = AnimatedCharacter mit Pink-Tint
// ============================================================
(function() {
    'use strict';

    // Najika companion config
    const COMPANION_CONFIG = {
        // KayKit AnimatedCharacter (gleich wie Spieler, aber mit Pink-Tint)
        modelPath: 'static/assets/KayKit Character Animations 1.2/Animations/gltf/KayKit_AnimatedCharacter_v1.2.glb',
        scale: 0.7,              // Etwas kleiner als Kuja
        followDistance: 3.5,     // Abstand zum Spieler
        followSpeed: 5.0,       // Geschwindigkeit
        catchUpSpeed: 9.0,      // Aufhol-Geschwindigkeit wenn zu weit weg
        maxDistance: 15,         // Teleport wenn weiter als das
        offsetAngle: -0.6,      // Leicht links-hinter dem Spieler
        bobSpeed: 2.5,          // Auf-und-ab-Wippen (nur für Fallback)
        bobHeight: 0.05,        // Minimales Wippen (Skeletal-Animation übernimmt)
        tintColor: 0xE91E63,    // Pink/Rosa Tint für Najika
        nameColor: '#E91E63',
    };

    let companionGroup = null;
    let companionModel = null;
    let companionReady = false;
    let companionLabel = null;
    let companionMixer = null;      // Eigener AnimationMixer
    let companionAnimations = {};   // Animation-Actions
    let companionCurrentAnim = '';
    let bobPhase = 0;
    let idleTimer = 0;
    let isIdle = true;
    let isMoving = false;
    let lastPlayerPos = new THREE.Vector3();
    let baseY = 0;

    // Helper: Get player reference (from index.html)
    function getPlayer() {
        return window.gameCharacter || null;
    }

    // Helper: Get scene reference
    function getScene() {
        return window.scene || window.Scene3D?.scene || null;
    }

    function init() {
        const checkScene = setInterval(() => {
            if (getPlayer() && getScene()) {
                clearInterval(checkScene);
                loadCompanion();
            }
        }, 500);
    }

    function loadCompanion() {
        if (!THREE.GLTFLoader) {
            console.warn('🐾 Companion3D: GLTFLoader fehlt');
            createFallbackCompanion();
            return;
        }

        const loader = new THREE.GLTFLoader();
        loader.load(
            COMPANION_CONFIG.modelPath,
            gltf => {
                companionGroup = new THREE.Group();
                companionModel = gltf.scene;

                companionModel.scale.setScalar(COMPANION_CONFIG.scale);
                companionModel.traverse(node => {
                    if (node.isMesh) {
                        node.castShadow = true;
                        node.receiveShadow = true;
                        // Najika-Tint (Pink)
                        if (node.material) {
                            const mat = node.material.clone();
                            mat.color.lerp(new THREE.Color(COMPANION_CONFIG.tintColor), 0.45);
                            mat.emissive = new THREE.Color(0x2e0a1a);
                            mat.emissiveIntensity = 0.2;
                            node.material = mat;
                        }
                    }
                });

                // Ground adjustment
                const box = new THREE.Box3().setFromObject(companionModel);
                companionModel.position.y -= box.min.y;

                companionGroup.add(companionModel);

                // Floating name label
                companionLabel = createNameLabel('Najika');
                companionLabel.position.y = box.max.y - box.min.y + 0.8;
                companionGroup.add(companionLabel);

                // Aura glow (pink)
                const auraGeo = new THREE.RingGeometry(0.6, 0.9, 16);
                const auraMat = new THREE.MeshBasicMaterial({
                    color: COMPANION_CONFIG.tintColor,
                    transparent: true,
                    opacity: 0.3,
                    side: THREE.DoubleSide,
                });
                const aura = new THREE.Mesh(auraGeo, auraMat);
                aura.rotation.x = -Math.PI / 2;
                aura.position.y = 0.05;
                aura.name = 'najika_aura';
                companionGroup.add(aura);

                // ANIMATIONS initialisieren!
                if (gltf.animations && gltf.animations.length > 0) {
                    companionMixer = new THREE.AnimationMixer(companionModel);
                    gltf.animations.forEach(clip => {
                        const name = clip.name.toLowerCase().replace(/\s+/g, '');
                        companionAnimations[name] = companionMixer.clipAction(clip);
                    });
                    // Idle als Default
                    playCompanionAnim('idle');
                    console.log(`🎬 Najika: ${gltf.animations.length} Animationen geladen`);
                }

                // Initial position: neben dem Spieler
                const player = getPlayer();
                if (player) {
                    companionGroup.position.copy(player.position);
                    companionGroup.position.x += COMPANION_CONFIG.followDistance;
                    lastPlayerPos.copy(player.position);
                    baseY = player.position.y;
                }

                const scene = getScene();
                if (scene) {
                    scene.add(companionGroup);
                }
                companionReady = true;
                console.log('🎀 Najika Companion geladen (Animated + Pink-Tint)');
            },
            undefined,
            error => {
                console.warn('🐾 Companion3D: Model-Fehler, nutze Fallback', error);
                createFallbackCompanion();
            }
        );
    }

    // Companion-eigene Animation abspielen
    function playCompanionAnim(name, loop = true, fadeTime = 0.2) {
        if (!companionMixer) return;
        name = name.toLowerCase();

        // Name-Mapping (gleich wie CharacterAnimations)
        const MAP = {
            'attack': 'attack(1h)', 'cast': 'shoot(1h)',
            'dodge': 'roll', 'block': 'block'
        };
        const mapped = MAP[name] || name;

        const action = companionAnimations[mapped] || companionAnimations[name];
        if (!action) return;
        if (companionCurrentAnim === name) return;

        // Fade transition
        Object.values(companionAnimations).forEach(a => {
            if (a.isRunning()) a.fadeOut(fadeTime);
        });

        action.reset();
        action.fadeIn(fadeTime);
        action.setLoop(loop ? THREE.LoopRepeat : THREE.LoopOnce);
        if (!loop) action.clampWhenFinished = true;
        action.play();

        companionCurrentAnim = name;
    }

    function createFallbackCompanion() {
        companionGroup = new THREE.Group();

        const bodyGeo = new THREE.CylinderGeometry(0.4, 0.35, 1.8, 8);
        const bodyMat = new THREE.MeshStandardMaterial({ color: COMPANION_CONFIG.tintColor });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.position.y = 1.0;
        body.castShadow = true;
        companionGroup.add(body);

        const headGeo = new THREE.SphereGeometry(0.35, 8, 8);
        const headMat = new THREE.MeshStandardMaterial({ color: 0xFFCDD2 });
        const head = new THREE.Mesh(headGeo, headMat);
        head.position.y = 2.1;
        head.castShadow = true;
        companionGroup.add(head);

        const hatGeo = new THREE.ConeGeometry(0.4, 0.7, 6);
        const hatMat = new THREE.MeshStandardMaterial({ color: 0x4A148C });
        const hat = new THREE.Mesh(hatGeo, hatMat);
        hat.position.y = 2.7;
        hat.castShadow = true;
        companionGroup.add(hat);

        companionLabel = createNameLabel('Najika');
        companionLabel.position.y = 3.3;
        companionGroup.add(companionLabel);

        const auraGeo = new THREE.RingGeometry(0.5, 0.8, 16);
        const auraMat = new THREE.MeshBasicMaterial({
            color: COMPANION_CONFIG.tintColor,
            transparent: true,
            opacity: 0.3,
            side: THREE.DoubleSide,
        });
        const aura = new THREE.Mesh(auraGeo, auraMat);
        aura.rotation.x = -Math.PI / 2;
        aura.position.y = 0.05;
        aura.name = 'najika_aura';
        companionGroup.add(aura);

        const player = getPlayer();
        if (player) {
            companionGroup.position.copy(player.position);
            companionGroup.position.x += COMPANION_CONFIG.followDistance;
            lastPlayerPos.copy(player.position);
            baseY = player.position.y;
        }

        const scene = getScene();
        if (scene) {
            scene.add(companionGroup);
        }
        companionReady = true;
        console.log('🎀 Najika Companion (Fallback) geladen');
    }

    function createNameLabel(text) {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');

        ctx.clearRect(0, 0, 256, 64);

        ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
        ctx.roundRect(28, 8, 200, 48, 10);
        ctx.fill();

        ctx.fillStyle = COMPANION_CONFIG.nameColor;
        ctx.font = 'bold 28px Courier New';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, 128, 32);

        ctx.fillStyle = '#E91E63';
        ctx.font = '20px serif';
        ctx.fillText('\u{1F380}', 50, 32);
        ctx.fillText('\u{1F495}', 206, 32);

        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;

        const spriteMat = new THREE.SpriteMaterial({
            map: texture,
            transparent: true,
            depthWrite: false,
        });
        const sprite = new THREE.Sprite(spriteMat);
        sprite.scale.set(2.5, 0.6, 1);
        return sprite;
    }

    function update(delta) {
        if (!companionReady || !companionGroup) return;
        const player = getPlayer();
        if (!player) return;

        const playerPos = player.position;
        const compPos = companionGroup.position;

        // Match player's ground height
        baseY = playerPos.y;

        // AnimationMixer updaten
        if (companionMixer) {
            companionMixer.update(delta);
        }

        // Distance to player (horizontal)
        const dx = playerPos.x - compPos.x;
        const dz = playerPos.z - compPos.z;
        const dist = Math.sqrt(dx * dx + dz * dz);

        // Teleport if too far
        if (dist > COMPANION_CONFIG.maxDistance) {
            const angle = Math.atan2(dx, dz) + COMPANION_CONFIG.offsetAngle;
            compPos.x = playerPos.x - Math.sin(angle) * COMPANION_CONFIG.followDistance;
            compPos.z = playerPos.z - Math.cos(angle) * COMPANION_CONFIG.followDistance;
            compPos.y = baseY;
            return;
        }

        // Check if player moved
        const playerMoved = lastPlayerPos.distanceTo(playerPos) > 0.05;
        lastPlayerPos.copy(playerPos);

        if (playerMoved) {
            isIdle = false;
            idleTimer = 0;
        } else {
            idleTimer += delta;
            if (idleTimer > 1.5) isIdle = true;
        }

        // Target position: behind-left of player
        const playerHeading = player.rotation.y;
        const targetAngle = playerHeading + COMPANION_CONFIG.offsetAngle;
        const targetX = playerPos.x - Math.sin(targetAngle) * COMPANION_CONFIG.followDistance;
        const targetZ = playerPos.z - Math.cos(targetAngle) * COMPANION_CONFIG.followDistance;

        const toDist = Math.sqrt(
            Math.pow(targetX - compPos.x, 2) +
            Math.pow(targetZ - compPos.z, 2)
        );

        // Move towards target + Animation
        const wasMoving = isMoving;
        if (toDist > 0.3) {
            const speed = toDist > 6 ? COMPANION_CONFIG.catchUpSpeed : COMPANION_CONFIG.followSpeed;
            const moveStep = Math.min(speed * delta, toDist);
            const moveAngle = Math.atan2(targetX - compPos.x, targetZ - compPos.z);

            compPos.x += Math.sin(moveAngle) * moveStep;
            compPos.z += Math.cos(moveAngle) * moveStep;

            // Face movement direction
            companionGroup.rotation.y = moveAngle;
            isMoving = true;

            // Animation: Run wenn schnell, Walk wenn langsam
            if (companionMixer) {
                const animName = toDist > 6 ? 'run' : 'walk';
                if (companionCurrentAnim !== animName) {
                    playCompanionAnim(animName);
                }
            }
        } else {
            isMoving = false;
            if (!isIdle) {
                companionGroup.rotation.y += (playerHeading - companionGroup.rotation.y) * 3 * delta;
            }

            // Animation: Idle
            if (companionMixer && wasMoving && !isMoving) {
                playCompanionAnim('idle');
            }
        }

        // Idle: Look at player
        if (isIdle && dist > 1) {
            const lookAngle = Math.atan2(dx, dz);
            companionGroup.rotation.y += (lookAngle - companionGroup.rotation.y) * 2 * delta;
        }

        // Ground height (minimales bob nur ohne skeletal animation)
        if (!companionMixer) {
            bobPhase += delta * COMPANION_CONFIG.bobSpeed;
            const bobOffset = Math.sin(bobPhase) * COMPANION_CONFIG.bobHeight;
            compPos.y = baseY + bobOffset;
        } else {
            compPos.y = baseY;
        }

        // Aura pulse
        const aura = companionGroup.getObjectByName('najika_aura');
        if (aura) {
            bobPhase += delta * COMPANION_CONFIG.bobSpeed;
            aura.material.opacity = 0.15 + Math.sin(bobPhase * 1.5) * 0.15;
            aura.rotation.z += delta * 0.5;
        }

        // Name label always faces camera
        if (companionLabel) {
            companionLabel.material.opacity = dist < 20 ? 1 : Math.max(0, 1 - (dist - 20) / 10);
        }
    }

    // Hook into animation loop
    function hookIntoLoop() {
        let lastTime = 0;

        setInterval(() => {
            const now = performance.now();
            const delta = Math.min((now - lastTime) / 1000, 0.1);
            lastTime = now;
            update(delta);
        }, 1000 / 60);
    }

    // Start
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => { init(); hookIntoLoop(); });
    } else {
        init();
        hookIntoLoop();
    }

    window.Companion3D = {
        getCompanion: () => companionGroup,
        isReady: () => companionReady,
        teleportToPlayer() {
            const player = getPlayer();
            if (player && companionGroup) {
                companionGroup.position.copy(player.position);
                companionGroup.position.x += COMPANION_CONFIG.followDistance;
            }
        },
        setVisible(v) {
            if (companionGroup) companionGroup.visible = v;
        },
        playAnimation(name) {
            playCompanionAnim(name);
        },
        // Combat-Animationen für Najika
        playAttack() { playCompanionAnim('attack', false); },
        playCast() { playCompanionAnim('cast', false); },
    };

    console.log('🎀 Companion3D System geladen');
})();
