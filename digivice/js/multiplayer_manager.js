/**
 * Multiplayer Manager
 * Handles real-time multiplayer functionality for Digivice Web Game
 *
 * Features:
 * - WebSocket connection to multiplayer server
 * - Player position/state synchronization
 * - Other players rendering
 * - Chat system
 * - Player list management
 */

class MultiplayerManager {
    constructor(scene, camera, localPlayer) {
        this.scene = scene;
        this.camera = camera;
        this.localPlayer = localPlayer;

        // WebSocket connection
        this.ws = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 2000;

        // Player management
        this.otherPlayers = new Map(); // {playerId: PlayerObject}
        this.localPlayerId = null;
        this.playerColors = [
            0xff0000, 0x00ff00, 0x0000ff, 0xffff00,
            0xff00ff, 0x00ffff, 0xffa500, 0x800080
        ];

        // Synchronization
        this.updateInterval = 100; // Send updates every 100ms
        this.lastUpdateTime = 0;
        this.interpolationBuffer = []; // For smooth movement

        // Chat
        this.chatMessages = [];
        this.maxChatMessages = 50;

        // Server URL
        this.serverUrl = this.getServerUrl();
    }

    /**
     * Get WebSocket server URL
     */
    getServerUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/api/multiplayer/ws`;
    }

    /**
     * Connect to multiplayer server
     */
    async connect(username, token) {
        if (this.connected) {
            console.log('Already connected to multiplayer server');
            return;
        }

        console.log('🌐 Connecting to multiplayer server...');

        try {
            // Connect with token for authentication
            const url = `${this.serverUrl}?token=${token}`;
            this.ws = new WebSocket(url);

            this.ws.onopen = () => this.onConnected(username);
            this.ws.onclose = () => this.onDisconnected();
            this.ws.onerror = (error) => this.onError(error);
            this.ws.onmessage = (event) => this.onMessage(event);

        } catch (error) {
            console.error('Failed to connect to multiplayer server:', error);
            this.attemptReconnect(username, token);
        }
    }

    /**
     * Handle connection established
     */
    onConnected(username) {
        console.log('✅ Connected to multiplayer server');
        this.connected = true;
        this.reconnectAttempts = 0;

        // Send join message
        this.send({
            type: 'join',
            username: username,
            position: this.localPlayer.position,
            character: {
                species: this.localPlayer.species || 'Jellysquish',
                level: this.localPlayer.level || 1,
                color: this.localPlayer.color || 0xff69b4
            }
        });

        // Start update loop
        this.startUpdateLoop();

        // Notify UI
        this.onConnectionStatusChanged(true);
    }

    /**
     * Handle disconnection
     */
    onDisconnected() {
        console.log('❌ Disconnected from multiplayer server');
        this.connected = false;
        this.ws = null;

        // Remove all other players
        this.removeAllPlayers();

        // Notify UI
        this.onConnectionStatusChanged(false);

        // Attempt reconnect
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.attemptReconnect();
        }
    }

    /**
     * Handle WebSocket error
     */
    onError(error) {
        console.error('WebSocket error:', error);
    }

    /**
     * Attempt to reconnect
     */
    attemptReconnect(username, token) {
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * this.reconnectAttempts;

        console.log(`🔄 Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);

        setTimeout(() => {
            if (!this.connected && username) {
                this.connect(username, token);
            }
        }, delay);
    }

    /**
     * Handle incoming message
     */
    onMessage(event) {
        try {
            const message = JSON.parse(event.data);

            switch (message.type) {
                case 'welcome':
                    this.onWelcome(message);
                    break;

                case 'player_joined':
                    this.onPlayerJoined(message);
                    break;

                case 'player_left':
                    this.onPlayerLeft(message);
                    break;

                case 'player_update':
                    this.onPlayerUpdate(message);
                    break;

                case 'player_list':
                    this.onPlayerList(message);
                    break;

                case 'chat_message':
                    this.onChatMessage(message);
                    break;

                case 'action':
                    this.onPlayerAction(message);
                    break;

                default:
                    console.warn('Unknown message type:', message.type);
            }

        } catch (error) {
            console.error('Failed to parse message:', error);
        }
    }

    /**
     * Handle welcome message
     */
    onWelcome(message) {
        this.localPlayerId = message.player_id;
        console.log(`✅ Joined as player ${this.localPlayerId}`);
    }

    /**
     * Handle player list
     */
    onPlayerList(message) {
        console.log(`👥 ${message.players.length} players online`);

        // Add all existing players
        message.players.forEach(player => {
            if (player.id !== this.localPlayerId) {
                this.addPlayer(player);
            }
        });
    }

    /**
     * Handle player joined
     */
    onPlayerJoined(message) {
        if (message.player_id === this.localPlayerId) return;

        console.log(`➕ Player joined: ${message.username}`);
        this.addPlayer(message);

        // Show notification
        this.showNotification(`${message.username} joined the game`);
    }

    /**
     * Handle player left
     */
    onPlayerLeft(message) {
        console.log(`➖ Player left: ${message.username}`);
        this.removePlayer(message.player_id);

        // Show notification
        this.showNotification(`${message.username} left the game`);
    }

    /**
     * Handle player update (position, animation, state)
     */
    onPlayerUpdate(message) {
        const player = this.otherPlayers.get(message.player_id);
        if (!player) return;

        // Update player state
        if (message.position) {
            player.targetPosition = {
                x: message.position.x,
                y: message.position.y,
                z: message.position.z
            };
        }

        if (message.rotation) {
            player.targetRotation = message.rotation.y;
        }

        if (message.animation) {
            this.playPlayerAnimation(player, message.animation);
        }

        if (message.state) {
            player.state = message.state;
        }
    }

    /**
     * Handle chat message
     */
    onChatMessage(message) {
        const chatMsg = {
            player_id: message.player_id,
            username: message.username,
            message: message.message,
            timestamp: Date.now()
        };

        this.chatMessages.push(chatMsg);

        // Keep only last N messages
        if (this.chatMessages.length > this.maxChatMessages) {
            this.chatMessages.shift();
        }

        // Notify UI
        this.onChatMessageReceived(chatMsg);

        console.log(`💬 ${message.username}: ${message.message}`);
    }

    /**
     * Handle player action (emote, attack, etc.)
     */
    onPlayerAction(message) {
        const player = this.otherPlayers.get(message.player_id);
        if (!player) return;

        switch (message.action) {
            case 'emote':
                this.playEmote(player, message.emote_type);
                break;

            case 'attack':
                this.playAttackAnimation(player);
                break;

            case 'interact':
                this.playInteractAnimation(player);
                break;
        }
    }

    /**
     * Add a new player to the scene
     */
    addPlayer(playerData) {
        if (this.otherPlayers.has(playerData.player_id)) {
            console.warn(`Player ${playerData.player_id} already exists`);
            return;
        }

        // Create player object (simple cube for now, replace with actual model)
        const geometry = new THREE.BoxGeometry(1, 2, 1);
        const colorIndex = this.otherPlayers.size % this.playerColors.length;
        const material = new THREE.MeshStandardMaterial({
            color: playerData.character?.color || this.playerColors[colorIndex]
        });

        const playerMesh = new THREE.Mesh(geometry, material);
        playerMesh.castShadow = true;
        playerMesh.receiveShadow = true;

        // Set initial position
        if (playerData.position) {
            playerMesh.position.set(
                playerData.position.x,
                playerData.position.y,
                playerData.position.z
            );
        }

        // Add name label (TODO: Create proper 3D text)
        const nameLabel = this.createNameLabel(playerData.username);
        nameLabel.position.y = 2.5;
        playerMesh.add(nameLabel);

        // Add to scene
        this.scene.add(playerMesh);

        // Store player data
        const player = {
            id: playerData.player_id,
            username: playerData.username,
            mesh: playerMesh,
            nameLabel: nameLabel,
            targetPosition: playerMesh.position.clone(),
            targetRotation: 0,
            character: playerData.character,
            state: playerData.state || 'idle'
        };

        this.otherPlayers.set(playerData.player_id, player);

        console.log(`✅ Added player: ${playerData.username} (${playerData.player_id})`);
    }

    /**
     * Remove a player from the scene
     */
    removePlayer(playerId) {
        const player = this.otherPlayers.get(playerId);
        if (!player) return;

        // Remove from scene
        this.scene.remove(player.mesh);

        // Dispose geometry and material
        player.mesh.geometry.dispose();
        player.mesh.material.dispose();

        // Remove from map
        this.otherPlayers.delete(playerId);

        console.log(`🗑️ Removed player: ${player.username}`);
    }

    /**
     * Remove all players
     */
    removeAllPlayers() {
        this.otherPlayers.forEach((player, playerId) => {
            this.removePlayer(playerId);
        });
    }

    /**
     * Create name label for player (3D Text with TextGeometry)
     */
    createNameLabel(username) {
        // Use sprite-based approach for better performance
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 512;
        canvas.height = 128;

        // Draw background with border
        context.fillStyle = 'rgba(0, 0, 0, 0.7)';
        context.strokeStyle = 'rgba(255, 255, 255, 0.8)';
        context.lineWidth = 3;
        const borderRadius = 10;

        // Rounded rectangle
        context.beginPath();
        context.moveTo(borderRadius, 0);
        context.lineTo(canvas.width - borderRadius, 0);
        context.quadraticCurveTo(canvas.width, 0, canvas.width, borderRadius);
        context.lineTo(canvas.width, canvas.height - borderRadius);
        context.quadraticCurveTo(canvas.width, canvas.height, canvas.width - borderRadius, canvas.height);
        context.lineTo(borderRadius, canvas.height);
        context.quadraticCurveTo(0, canvas.height, 0, canvas.height - borderRadius);
        context.lineTo(0, borderRadius);
        context.quadraticCurveTo(0, 0, borderRadius, 0);
        context.closePath();
        context.fill();
        context.stroke();

        // Draw text with shadow
        context.shadowColor = 'rgba(0, 0, 0, 0.8)';
        context.shadowBlur = 4;
        context.shadowOffsetX = 2;
        context.shadowOffsetY = 2;
        context.fillStyle = '#ffffff';
        context.font = 'bold 48px Arial, sans-serif';
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(username, canvas.width / 2, canvas.height / 2);

        // Create texture and sprite
        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        const spriteMaterial = new THREE.SpriteMaterial({
            map: texture,
            transparent: true,
            depthTest: true,
            depthWrite: false
        });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.scale.set(3, 0.75, 1);
        sprite.renderOrder = 1000; // Always render on top

        return sprite;
    }

    /**
     * Send message to server
     */
    send(data) {
        if (!this.connected || !this.ws) {
            console.warn('Cannot send message: not connected');
            return false;
        }

        try {
            this.ws.send(JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('Failed to send message:', error);
            return false;
        }
    }

    /**
     * Send position update
     */
    sendPositionUpdate() {
        if (!this.localPlayer) return;

        this.send({
            type: 'update',
            position: {
                x: this.localPlayer.position.x,
                y: this.localPlayer.position.y,
                z: this.localPlayer.position.z
            },
            rotation: {
                y: this.localPlayer.rotation.y
            },
            animation: this.localPlayer.currentAnimation || 'idle',
            state: this.localPlayer.state || 'idle'
        });
    }

    /**
     * Send chat message
     */
    sendChatMessage(message) {
        this.send({
            type: 'chat',
            message: message
        });
    }

    /**
     * Send player action
     */
    sendAction(action, data = {}) {
        this.send({
            type: 'action',
            action: action,
            ...data
        });
    }

    /**
     * Start update loop
     */
    startUpdateLoop() {
        setInterval(() => {
            if (this.connected) {
                this.sendPositionUpdate();
            }
        }, this.updateInterval);
    }

    /**
     * Update (call every frame)
     */
    update(deltaTime) {
        if (!this.connected) return;

        const currentTime = Date.now();

        // Interpolate other players' positions
        this.otherPlayers.forEach(player => {
            // Smooth position interpolation
            if (player.targetPosition) {
                player.mesh.position.lerp(player.targetPosition, 0.2);
            }

            // Smooth rotation interpolation
            if (player.targetRotation !== undefined) {
                const currentRotation = player.mesh.rotation.y;
                const diff = player.targetRotation - currentRotation;
                player.mesh.rotation.y += diff * 0.2;
            }

            // Update animations
            this.updatePlayerAnimations(player, currentTime);

            // Always face camera for name label
            if (player.nameLabel) {
                player.nameLabel.lookAt(this.camera.position);
            }
        });
    }

    /**
     * Update player animations based on animation data
     */
    updatePlayerAnimations(player, currentTime) {
        if (!player.animationData) return;

        const { type, startTime } = player.animationData;
        const elapsed = currentTime - startTime;

        switch (type) {
            case 'idle':
                // Gentle bobbing
                const bobAmount = player.animationData.bobAmount;
                const bobSpeed = player.animationData.bobSpeed;
                player.mesh.position.y = Math.sin(elapsed * bobSpeed) * bobAmount;
                break;

            case 'walk':
                // Walking bounce
                const walkBounce = Math.abs(Math.sin(elapsed * player.animationData.bounceSpeed)) * player.animationData.bounceAmount;
                player.mesh.position.y = walkBounce;
                player.mesh.rotation.z = Math.sin(elapsed * player.animationData.rotateSpeed) * 0.05;
                break;

            case 'run':
                // Running bounce (faster)
                const runBounce = Math.abs(Math.sin(elapsed * player.animationData.bounceSpeed)) * player.animationData.bounceAmount;
                player.mesh.position.y = runBounce;
                player.mesh.rotation.z = Math.sin(elapsed * player.animationData.rotateSpeed) * 0.1;
                break;

            case 'jump':
                // Jump arc
                const jumpProgress = Math.min(elapsed / player.animationData.jumpDuration, 1);
                const jumpHeight = Math.sin(jumpProgress * Math.PI) * player.animationData.jumpHeight;
                player.mesh.position.y = jumpHeight;
                if (jumpProgress >= 1) {
                    player.animationData = null; // End animation
                }
                break;

            case 'hurt':
                // Flash red
                const flashProgress = elapsed / player.animationData.flashDuration;
                if (flashProgress < 1) {
                    const flashColor = flashProgress % 0.2 < 0.1 ? 0xff0000 : player.animationData.originalColor;
                    player.mesh.material.color.setHex(flashColor);
                } else {
                    player.mesh.material.color.copy(player.animationData.originalColor);
                    player.animationData = null;
                }
                break;
        }
    }

    /**
     * Play animation for player
     */
    playPlayerAnimation(player, animationName) {
        player.currentAnimation = animationName;

        // Animation states: 'idle', 'walk', 'run', 'jump', 'attack', 'hurt', 'die'
        const animations = {
            idle: () => {
                // Gentle bobbing motion
                player.animationData = {
                    type: 'idle',
                    startTime: Date.now(),
                    bobSpeed: 0.002,
                    bobAmount: 0.05
                };
            },
            walk: () => {
                // Walking animation with bounce
                player.animationData = {
                    type: 'walk',
                    startTime: Date.now(),
                    bounceSpeed: 0.008,
                    bounceAmount: 0.15,
                    rotateSpeed: 0.01
                };
            },
            run: () => {
                // Running animation with faster bounce
                player.animationData = {
                    type: 'run',
                    startTime: Date.now(),
                    bounceSpeed: 0.015,
                    bounceAmount: 0.25,
                    rotateSpeed: 0.02
                };
            },
            jump: () => {
                // Jump animation
                player.animationData = {
                    type: 'jump',
                    startTime: Date.now(),
                    jumpHeight: 2,
                    jumpDuration: 500
                };
            },
            attack: () => {
                this.playAttackAnimation(player);
            },
            hurt: () => {
                // Hurt flash effect
                player.animationData = {
                    type: 'hurt',
                    startTime: Date.now(),
                    flashDuration: 300,
                    originalColor: player.mesh.material.color.clone()
                };
            }
        };

        // Execute animation if exists
        if (animations[animationName]) {
            animations[animationName]();
        }

        // Update animation in game loop
        this.updatePlayerAnimations(player);
    }

    /**
     * Play emote (visual effects above player)
     */
    playEmote(player, emoteType) {
        console.log(`${player.username} plays emote: ${emoteType}`);

        // Emote icons/symbols
        const emotes = {
            wave: '👋',
            laugh: '😂',
            happy: '😊',
            sad: '😢',
            angry: '😠',
            heart: '❤️',
            star: '⭐',
            thumbsup: '👍',
            thumbsdown: '👎',
            question: '❓',
            exclamation: '❗',
            zzz: '💤'
        };

        const emoteSymbol = emotes[emoteType] || '💬';

        // Create emote bubble
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 256;

        // Draw bubble background
        context.fillStyle = 'rgba(255, 255, 255, 0.9)';
        context.strokeStyle = 'rgba(0, 0, 0, 0.6)';
        context.lineWidth = 4;
        context.beginPath();
        context.arc(128, 128, 100, 0, Math.PI * 2);
        context.fill();
        context.stroke();

        // Draw emote symbol
        context.font = 'bold 120px Arial';
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(emoteSymbol, 128, 128);

        // Create sprite
        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({
            map: texture,
            transparent: true,
            depthTest: false
        });
        const emoteBubble = new THREE.Sprite(spriteMaterial);
        emoteBubble.scale.set(1.5, 1.5, 1);
        emoteBubble.position.y = 3.5;
        emoteBubble.renderOrder = 999;

        player.mesh.add(emoteBubble);

        // Animate bubble (float up and fade out)
        const startTime = Date.now();
        const duration = 2000;
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = elapsed / duration;

            if (progress < 1) {
                emoteBubble.position.y = 3.5 + progress * 2;
                emoteBubble.material.opacity = 1 - progress;
                emoteBubble.scale.setScalar(1.5 + progress * 0.5);
                requestAnimationFrame(animate);
            } else {
                player.mesh.remove(emoteBubble);
                emoteBubble.material.dispose();
                texture.dispose();
            }
        };
        animate();
    }

    /**
     * Play attack animation with slash effect
     */
    playAttackAnimation(player) {
        console.log(`${player.username} attacks!`);

        // Attack animation: quick forward lunge
        const originalZ = player.mesh.position.z;
        const startTime = Date.now();
        const duration = 300;

        // Create slash effect
        const slashGeometry = new THREE.PlaneGeometry(2, 2);
        const slashMaterial = new THREE.MeshBasicMaterial({
            color: 0xffff00,
            transparent: true,
            opacity: 0.8,
            side: THREE.DoubleSide,
            blending: THREE.AdditiveBlending
        });
        const slash = new THREE.Mesh(slashGeometry, slashMaterial);
        slash.position.set(0, 1, 1);
        slash.rotation.z = Math.PI / 4;
        player.mesh.add(slash);

        // Animate attack
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = elapsed / duration;

            if (progress < 1) {
                // Lunge forward
                if (progress < 0.3) {
                    player.mesh.position.z = originalZ + Math.sin(progress * Math.PI * 5) * 0.5;
                }

                // Slash rotation and fade
                slash.rotation.z = Math.PI / 4 + progress * Math.PI;
                slash.material.opacity = 0.8 * (1 - progress);
                slash.scale.setScalar(1 + progress * 2);

                requestAnimationFrame(animate);
            } else {
                player.mesh.position.z = originalZ;
                player.mesh.remove(slash);
                slash.geometry.dispose();
                slash.material.dispose();
            }
        };
        animate();

        // Play sound effect (if available)
        if (window.audioManager) {
            window.audioManager.playSound('attack');
        }
    }

    /**
     * Play interact animation (searching/picking up)
     */
    playInteractAnimation(player) {
        console.log(`${player.username} interacts`);

        // Interact animation: bob down and up
        const originalY = player.mesh.position.y;
        const startTime = Date.now();
        const duration = 500;

        // Create sparkle effect
        const sparkles = [];
        for (let i = 0; i < 5; i++) {
            const sparkleGeometry = new THREE.SphereGeometry(0.1, 8, 8);
            const sparkleMaterial = new THREE.MeshBasicMaterial({
                color: 0x00ffff,
                transparent: true,
                opacity: 1
            });
            const sparkle = new THREE.Mesh(sparkleGeometry, sparkleMaterial);
            sparkle.position.set(
                Math.random() * 2 - 1,
                1 + Math.random(),
                Math.random() * 2 - 1
            );
            player.mesh.add(sparkle);
            sparkles.push(sparkle);
        }

        // Animate
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = elapsed / duration;

            if (progress < 1) {
                // Bob down and up
                player.mesh.position.y = originalY + Math.sin(progress * Math.PI) * -0.3;

                // Animate sparkles
                sparkles.forEach((sparkle, index) => {
                    sparkle.position.y += 0.05;
                    sparkle.material.opacity = 1 - progress;
                    sparkle.rotation.x += 0.1;
                    sparkle.rotation.y += 0.1;
                });

                requestAnimationFrame(animate);
            } else {
                player.mesh.position.y = originalY;
                sparkles.forEach(sparkle => {
                    player.mesh.remove(sparkle);
                    sparkle.geometry.dispose();
                    sparkle.material.dispose();
                });
            }
        };
        animate();

        // Play sound effect (if available)
        if (window.audioManager) {
            window.audioManager.playSound('interact');
        }
    }

    /**
     * Show notification (toast-style UI)
     */
    showNotification(message) {
        console.log(`📢 ${message}`);

        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'multiplayer-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            padding: 12px 20px;
            border-radius: 8px;
            border: 2px solid #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            font-weight: bold;
            z-index: 10000;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            animation: slideInRight 0.3s ease-out, slideOutRight 0.3s ease-in 2.7s;
            pointer-events: none;
        `;

        document.body.appendChild(notification);

        // Add animation styles if not already added
        if (!document.getElementById('notification-animations')) {
            const style = document.createElement('style');
            style.id = 'notification-animations';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        // Remove after animation
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    /**
     * Get player count
     */
    getPlayerCount() {
        return this.otherPlayers.size + (this.connected ? 1 : 0);
    }

    /**
     * Get player list
     */
    getPlayerList() {
        const players = [];

        // Add local player
        if (this.connected && this.localPlayerId) {
            players.push({
                id: this.localPlayerId,
                username: this.localPlayer.username || 'You',
                isLocal: true
            });
        }

        // Add other players
        this.otherPlayers.forEach(player => {
            players.push({
                id: player.id,
                username: player.username,
                isLocal: false
            });
        });

        return players;
    }

    /**
     * Disconnect from server
     */
    disconnect() {
        if (!this.connected) return;

        console.log('Disconnecting from multiplayer server...');

        // Send leave message
        this.send({ type: 'leave' });

        // Close WebSocket
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }

        this.connected = false;
        this.removeAllPlayers();

        // Notify UI
        this.onConnectionStatusChanged(false);
    }

    /**
     * Callbacks (to be overridden by UI)
     */
    onConnectionStatusChanged(connected) {
        // Override this in your UI code
    }

    onChatMessageReceived(message) {
        // Override this in your UI code
    }

    /**
     * Cleanup
     */
    dispose() {
        this.disconnect();
        this.removeAllPlayers();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MultiplayerManager;
}
