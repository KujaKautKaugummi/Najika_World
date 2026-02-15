/**
 * NAJIKA WORLD - GameEvents ↔ WebSocket Bridge
 * ==============================================
 * Verbindet das lokale GameEvents-System mit dem WebSocket-Server
 * fuer Realtime-Events (Battle, Quest, Region, etc.)
 *
 * Funktionsweise:
 * - GameEvents.emit() → WebSocket Server (outgoing)
 * - WebSocket Message → GameEvents.emit() (incoming)
 *
 * Abhaengigkeiten: game_events.js (muss vorher geladen sein)
 */

(function() {
    'use strict';

    // =========================================================================
    // CONFIG
    // =========================================================================

    const WS_CONFIG = {
        // WebSocket URL (gleicher Host wie API, ws:// statt http://)
        url: 'ws://127.0.0.1:8001/ws/connect',
        reconnectDelay: 5000,
        maxReconnects: 0,  // Kein Reconnect - WS-Server existiert nicht
        pingInterval: 30000,
        // Events die an den Server gesendet werden
        outgoingEvents: [
            'combatStarted', 'combatEnded', 'enemyKilled',
            'questCompleted', 'questAccepted',
            'regionEntered', 'levelUp',
            'itemCrafted', 'itemPurchased'
        ],
        // Channels die automatisch abonniert werden
        autoSubscribe: ['global', 'battle']
    };

    // =========================================================================
    // STATE
    // =========================================================================

    let ws = null;
    let connected = false;
    let reconnectAttempts = 0;
    let reconnectTimer = null;
    let pingTimer = null;

    // =========================================================================
    // WEBSOCKET CONNECTION
    // =========================================================================

    function connect() {
        if (connected || (ws && ws.readyState === WebSocket.CONNECTING)) return;

        // Auth-Token aus localStorage (falls vorhanden)
        const token = localStorage.getItem('auth_token') || 'local_player';
        const url = `${WS_CONFIG.url}?token=${token}`;

        try {
            ws = new WebSocket(url);
        } catch (e) {
            console.warn('[WS-Bridge] WebSocket nicht verfuegbar:', e.message);
            scheduleReconnect();
            return;
        }

        ws.onopen = function() {
            console.log('[WS-Bridge] Verbunden mit WebSocket Server');
            connected = true;
            reconnectAttempts = 0;

            // Auto-Subscribe
            WS_CONFIG.autoSubscribe.forEach(function(channel) {
                send({ type: 'subscribe', channel: channel });
            });

            // Ping starten
            startPing();

            // GameEvent emittieren
            if (window.GameEvents) {
                window.GameEvents.emit('wsConnected', { url: WS_CONFIG.url });
            }
        };

        ws.onmessage = function(event) {
            try {
                var msg = JSON.parse(event.data);
                handleIncomingMessage(msg);
            } catch (e) {
                console.warn('[WS-Bridge] Parse-Fehler:', e);
            }
        };

        ws.onerror = function(event) {
            // Leise - WS-Server ist optional, Spiel funktioniert ohne
            console.debug('[WS-Bridge] WebSocket nicht verfuegbar (optional)');
        };

        ws.onclose = function(event) {
            console.log('[WS-Bridge] Verbindung geschlossen (Code: ' + event.code + ')');
            connected = false;
            stopPing();

            if (window.GameEvents) {
                window.GameEvents.emit('wsDisconnected', { code: event.code });
            }

            // Reconnect (ausser bei intentionalem Close)
            if (event.code !== 1000) {
                scheduleReconnect();
            }
        };
    }

    function disconnect() {
        if (reconnectTimer) {
            clearTimeout(reconnectTimer);
            reconnectTimer = null;
        }
        stopPing();
        if (ws) {
            ws.close(1000, 'Client disconnect');
            ws = null;
        }
        connected = false;
    }

    function send(msg) {
        if (!connected || !ws) return false;
        try {
            ws.send(JSON.stringify(msg));
            return true;
        } catch (e) {
            return false;
        }
    }

    function scheduleReconnect() {
        if (reconnectAttempts >= WS_CONFIG.maxReconnects) {
            console.warn('[WS-Bridge] Max Reconnects erreicht');
            return;
        }
        reconnectAttempts++;
        var delay = WS_CONFIG.reconnectDelay * reconnectAttempts;
        console.log('[WS-Bridge] Reconnect in ' + delay + 'ms (Versuch ' + reconnectAttempts + ')');
        reconnectTimer = setTimeout(connect, delay);
    }

    function startPing() {
        stopPing();
        pingTimer = setInterval(function() {
            send({ type: 'ping', timestamp: Date.now() });
        }, WS_CONFIG.pingInterval);
    }

    function stopPing() {
        if (pingTimer) {
            clearInterval(pingTimer);
            pingTimer = null;
        }
    }

    // =========================================================================
    // INCOMING: WebSocket → GameEvents
    // =========================================================================

    function handleIncomingMessage(msg) {
        if (!window.GameEvents) return;

        var type = msg.type;
        if (!type) return;

        // Pong ignorieren
        if (type === 'pong') return;

        // Server-Events als GameEvents emittieren
        switch (type) {
            case 'battle_start':
                window.GameEvents.emit('combatStarted', msg.data || msg);
                break;
            case 'battle_action':
                window.GameEvents.emit('combatAction', msg.data || msg);
                break;
            case 'battle_end':
                window.GameEvents.emit('combatEnded', msg.data || msg);
                break;
            case 'notification':
                window.GameEvents.emit('serverNotification', msg);
                break;
            case 'world_event':
                window.GameEvents.emit('worldEvent', msg.data || msg);
                break;
            case 'user_joined':
                window.GameEvents.emit('playerJoined', msg);
                break;
            case 'user_left':
                window.GameEvents.emit('playerLeft', msg);
                break;
            case 'evolution':
                window.GameEvents.emit('slimeEvolved', msg.data || msg);
                break;
            case 'inventory_update':
                window.GameEvents.emit('inventoryUpdated', msg.data || msg);
                break;
            default:
                // Generisches Event durchreichen
                window.GameEvents.emit('ws:' + type, msg.data || msg);
                break;
        }
    }

    // =========================================================================
    // OUTGOING: GameEvents → WebSocket
    // =========================================================================

    function setupOutgoingBridge() {
        if (!window.GameEvents) {
            console.warn('[WS-Bridge] GameEvents nicht verfuegbar, warte...');
            setTimeout(setupOutgoingBridge, 500);
            return;
        }

        WS_CONFIG.outgoingEvents.forEach(function(eventName) {
            window.GameEvents.on(eventName, function(data) {
                send({
                    type: 'game_event',
                    event: eventName,
                    data: data,
                    timestamp: Date.now()
                });
            });
        });

        console.log('[WS-Bridge] ' + WS_CONFIG.outgoingEvents.length + ' GameEvents → WebSocket verdrahtet');
    }

    // =========================================================================
    // PUBLIC API
    // =========================================================================

    window.GameEventsWSBridge = {
        connect: connect,
        disconnect: disconnect,
        send: send,
        isConnected: function() { return connected; },
        getState: function() {
            return {
                connected: connected,
                reconnectAttempts: reconnectAttempts,
                url: WS_CONFIG.url
            };
        }
    };

    // =========================================================================
    // AUTO-INIT
    // =========================================================================

    // Bridge setup (GameEvents → WS)
    setupOutgoingBridge();

    // Auto-Connect nach kurzer Verzoegerung (Server muss bereit sein)
    setTimeout(function() {
        connect();
    }, 1000);

    console.log('[WS-Bridge] GameEvents ↔ WebSocket Bridge initialisiert');

})();
