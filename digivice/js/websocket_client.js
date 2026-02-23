/**
 * WebSocket Client
 * Real-time communication for Najika World
 */

const API_BASE_URL = (window.NajikaConfig && window.NajikaConfig.API_BASE_URL) || 'http://localhost:8000';

class WebSocketClient {
    constructor() {
        this.ws = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000; // ms
        this.reconnectTimer = null;
        this.pingInterval = null;
        this.authToken = localStorage.getItem('auth_token');

        // Event handlers
        this.eventHandlers = new Map();

        // Subscribed channels
        this.subscribedChannels = new Set();

        // Connection state
        this.connectionState = 'disconnected'; // disconnected, connecting, connected, reconnecting

        console.log('🔌 WebSocket Client initialized');
    }

    /**
     * Connect to WebSocket server
     */
    connect() {
        if (this.connected || this.connectionState === 'connecting') {
            console.warn('Already connected or connecting');
            return;
        }

        if (!this.authToken) {
            console.error('No auth token found');
            this.emit('error', { message: 'Not authenticated' });
            return;
        }

        this.connectionState = 'connecting';

        // Create WebSocket connection
        const wsUrl = API_BASE_URL.replace('http', 'ws') + `/ws/connect?token=${this.authToken}`;

        try {
            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => this.onOpen();
            this.ws.onmessage = (event) => this.onMessage(event);
            this.ws.onerror = (error) => this.onError(error);
            this.ws.onclose = (event) => this.onClose(event);

            console.log('🔌 Connecting to WebSocket...');
        } catch (error) {
            console.error('Failed to create WebSocket:', error);
            this.connectionState = 'disconnected';
            this.scheduleReconnect();
        }
    }

    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }

        if (this.pingInterval) {
            clearInterval(this.pingInterval);
            this.pingInterval = null;
        }

        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }

        this.connected = false;
        this.connectionState = 'disconnected';
        this.subscribedChannels.clear();

        console.log('🔌 WebSocket disconnected');
    }

    /**
     * WebSocket opened
     */
    onOpen() {
        console.log('✅ WebSocket connected');

        this.connected = true;
        this.connectionState = 'connected';
        this.reconnectAttempts = 0;

        // Start ping interval
        this.startPing();

        // Emit connected event
        this.emit('connected', {});

        // Re-subscribe to channels
        this.subscribedChannels.forEach(channel => {
            this.send({
                type: 'subscribe',
                channel: channel
            });
        });
    }

    /**
     * WebSocket message received
     */
    onMessage(event) {
        try {
            const message = JSON.parse(event.data);

            // Emit type-specific event
            if (message.type) {
                this.emit(message.type, message);
            }

            // Emit generic message event
            this.emit('message', message);

        } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
        }
    }

    /**
     * WebSocket error
     */
    onError(error) {
        console.error('❌ WebSocket error:', error);
        this.emit('error', error);
    }

    /**
     * WebSocket closed
     */
    onClose(event) {
        console.log(`🔌 WebSocket closed (code: ${event.code}, reason: ${event.reason})`);

        this.connected = false;
        this.connectionState = 'disconnected';

        if (this.pingInterval) {
            clearInterval(this.pingInterval);
            this.pingInterval = null;
        }

        this.emit('disconnected', {
            code: event.code,
            reason: event.reason
        });

        // Attempt to reconnect (unless closed intentionally)
        if (event.code !== 1000) {
            this.scheduleReconnect();
        }
    }

    /**
     * Schedule reconnection attempt
     */
    scheduleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnect attempts reached');
            this.emit('reconnect_failed', {});
            return;
        }

        this.reconnectAttempts++;
        this.connectionState = 'reconnecting';

        const delay = this.reconnectDelay * this.reconnectAttempts;

        console.log(`🔄 Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

        this.emit('reconnecting', {
            attempt: this.reconnectAttempts,
            delay: delay
        });

        this.reconnectTimer = setTimeout(() => {
            this.connect();
        }, delay);
    }

    /**
     * Start ping interval
     */
    startPing() {
        this.pingInterval = setInterval(() => {
            if (this.connected) {
                this.send({
                    type: 'ping',
                    timestamp: Date.now()
                });
            }
        }, 30000); // Ping every 30 seconds
    }

    /**
     * Send message to server
     */
    send(message) {
        if (!this.connected || !this.ws) {
            console.warn('Cannot send: not connected');
            return false;
        }

        try {
            this.ws.send(JSON.stringify(message));
            return true;
        } catch (error) {
            console.error('Failed to send message:', error);
            return false;
        }
    }

    /**
     * Subscribe to channel
     */
    subscribe(channel) {
        this.subscribedChannels.add(channel);

        if (this.connected) {
            this.send({
                type: 'subscribe',
                channel: channel
            });
        }

        console.log(`📡 Subscribed to channel: ${channel}`);
    }

    /**
     * Unsubscribe from channel
     */
    unsubscribe(channel) {
        this.subscribedChannels.delete(channel);

        if (this.connected) {
            this.send({
                type: 'unsubscribe',
                channel: channel
            });
        }

        console.log(`📡 Unsubscribed from channel: ${channel}`);
    }

    /**
     * Spectate battle
     */
    spectateBattle(battleId) {
        this.send({
            type: 'spectate_battle',
            battle_id: battleId
        });

        console.log(`👁️ Spectating battle: ${battleId}`);
    }

    /**
     * Stop spectating battle
     */
    stopSpectating(battleId) {
        this.send({
            type: 'stop_spectating',
            battle_id: battleId
        });

        console.log(`👁️ Stopped spectating battle: ${battleId}`);
    }

    /**
     * Update presence
     */
    updatePresence(presence) {
        this.send({
            type: 'update_presence',
            presence: presence
        });
    }

    /**
     * Register event handler
     */
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }

        this.eventHandlers.get(event).push(handler);

        return () => this.off(event, handler);
    }

    /**
     * Unregister event handler
     */
    off(event, handler) {
        if (!this.eventHandlers.has(event)) {
            return;
        }

        const handlers = this.eventHandlers.get(event);
        const index = handlers.indexOf(handler);

        if (index !== -1) {
            handlers.splice(index, 1);
        }
    }

    /**
     * Emit event
     */
    emit(event, data) {
        if (!this.eventHandlers.has(event)) {
            return;
        }

        const handlers = this.eventHandlers.get(event);

        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (error) {
                console.error(`Error in ${event} handler:`, error);
            }
        });
    }

    /**
     * Get connection state
     */
    getState() {
        return {
            connected: this.connected,
            connectionState: this.connectionState,
            subscribedChannels: Array.from(this.subscribedChannels),
            reconnectAttempts: this.reconnectAttempts
        };
    }
}

/**
 * Global WebSocket client instance
 */
const websocketClient = new WebSocketClient();

/**
 * WebSocket Notification System
 */
class NotificationSystem {
    constructor(wsClient) {
        this.wsClient = wsClient;
        this.notifications = [];
        this.maxNotifications = 50;
        this.notificationHandlers = [];

        this.init();

        console.log('🔔 Notification System initialized');
    }

    /**
     * Initialize notification handlers
     */
    init() {
        // Listen for notifications
        this.wsClient.on('notification', (data) => {
            this.addNotification(data);
        });

        // Listen for user joined
        this.wsClient.on('user_joined', (data) => {
            this.addNotification({
                notification_type: 'info',
                title: 'User Joined',
                message: `${data.username} has joined the game`,
                data: data
            });
        });

        // Listen for user left
        this.wsClient.on('user_left', (data) => {
            this.addNotification({
                notification_type: 'info',
                title: 'User Left',
                message: `${data.username} has left the game`,
                data: data
            });
        });

        // Listen for battle start
        this.wsClient.on('battle_start', (data) => {
            this.addNotification({
                notification_type: 'battle',
                title: 'Battle Started',
                message: `A new battle has begun!`,
                data: data
            });
        });

        // Listen for evolution
        this.wsClient.on('evolution', (data) => {
            this.addNotification({
                notification_type: 'evolution',
                title: 'Evolution!',
                message: `${data.username}'s Digimon evolved!`,
                data: data
            });
        });

        // Listen for finisher
        this.wsClient.on('finisher', (data) => {
            this.addNotification({
                notification_type: 'finisher',
                title: 'Finisher!',
                message: `${data.username} performed a finisher!`,
                data: data
            });
        });
    }

    /**
     * Add notification
     */
    addNotification(notification) {
        const notif = {
            id: Date.now(),
            timestamp: new Date(),
            ...notification
        };

        this.notifications.unshift(notif);

        // Limit notifications
        if (this.notifications.length > this.maxNotifications) {
            this.notifications = this.notifications.slice(0, this.maxNotifications);
        }

        // Trigger handlers
        this.notificationHandlers.forEach(handler => {
            try {
                handler(notif);
            } catch (error) {
                console.error('Error in notification handler:', error);
            }
        });

        // Show browser notification if permitted
        this.showBrowserNotification(notif);

        console.log('🔔 Notification:', notif);
    }

    /**
     * Show browser notification
     */
    showBrowserNotification(notification) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(notification.title, {
                body: notification.message,
                icon: '/assets/images/icon.png',
                tag: notification.notification_type
            });
        }
    }

    /**
     * Request notification permission
     */
    async requestPermission() {
        if ('Notification' in window) {
            const permission = await Notification.requestPermission();
            return permission === 'granted';
        }
        return false;
    }

    /**
     * Register notification handler
     */
    onNotification(handler) {
        this.notificationHandlers.push(handler);

        return () => {
            const index = this.notificationHandlers.indexOf(handler);
            if (index !== -1) {
                this.notificationHandlers.splice(index, 1);
            }
        };
    }

    /**
     * Get all notifications
     */
    getNotifications() {
        return this.notifications;
    }

    /**
     * Clear notifications
     */
    clearNotifications() {
        this.notifications = [];
    }

    /**
     * Mark notification as read
     */
    markAsRead(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
            notification.read = true;
        }
    }
}

// Create global notification system
const notificationSystem = new NotificationSystem(websocketClient);

// Make globally available
window.websocketClient = websocketClient;
window.notificationSystem = notificationSystem;

// Auto-connect if authenticated
if (localStorage.getItem('auth_token')) {
    websocketClient.connect();
}
