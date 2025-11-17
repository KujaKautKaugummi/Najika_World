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
        return `${protocol}//${host}/api/v1/multiplayer/ws`;
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
     * Create name label for player
     */
    createNameLabel(username) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 64;

        // Draw text
        context.fillStyle = 'rgba(0, 0, 0, 0.5)';
        context.fillRect(0, 0, canvas.width, canvas.height);

        context.fillStyle = 'white';
        context.font = 'bold 32px Arial';
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(username, canvas.width / 2, canvas.height / 2);

        // Create texture and sprite
        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.scale.set(2, 0.5, 1);

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
        });
    }

    /**
     * Play animation for player
     */
    playPlayerAnimation(player, animationName) {
        // TODO: Implement animation system
        player.currentAnimation = animationName;
    }

    /**
     * Play emote
     */
    playEmote(player, emoteType) {
        // TODO: Implement emote system
        console.log(`${player.username} plays emote: ${emoteType}`);
    }

    /**
     * Play attack animation
     */
    playAttackAnimation(player) {
        // TODO: Implement attack animation
        console.log(`${player.username} attacks!`);
    }

    /**
     * Play interact animation
     */
    playInteractAnimation(player) {
        // TODO: Implement interact animation
        console.log(`${player.username} interacts`);
    }

    /**
     * Show notification
     */
    showNotification(message) {
        // TODO: Implement notification UI
        console.log(`📢 ${message}`);
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
