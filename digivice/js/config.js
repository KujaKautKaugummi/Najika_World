/**
 * Najika World - Configuration
 * Central configuration file for API and WebSocket connections
 *
 * AUDIT FIX 2026-02-15: Created to support ES6 module imports
 */

// API Configuration
export const API_BASE_URL = 'http://127.0.0.1:8001';
export const WS_BASE_URL = 'ws://127.0.0.1:8001';

// API Endpoints
export const API_ENDPOINTS = {
    // Auth
    AUTH: `${API_BASE_URL}/api/auth`,

    // Chat
    CHAT: `${API_BASE_URL}/api/chat`,
    CHAT_V2: `${API_BASE_URL}/api/v2/chat`,

    // Battle
    BATTLE: `${API_BASE_URL}/api/v2/battle`,

    // State
    STATE: `${API_BASE_URL}/api/state`,

    // Slime
    SLIME_V3: `${API_BASE_URL}/api/slime-v3`,

    // Quest
    QUEST: `${API_BASE_URL}/api/v2/quest`,

    // Arena
    ARENA: `${API_BASE_URL}/api/arena`,

    // Companion
    COMPANION: `${API_BASE_URL}/api/companion`,

    // Admin
    ADMIN: `${API_BASE_URL}/api/admin`
};

// WebSocket Configuration
export const WS_CONFIG = {
    URL: `${WS_BASE_URL}/ws/connect`,
    RECONNECT_INTERVAL: 5000,  // 5 seconds
    MAX_RECONNECT_ATTEMPTS: 10
};

// Environment
export const ENV = {
    isDevelopment: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
    isProduction: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
};

// Export for non-module usage (backward compatibility)
if (typeof window !== 'undefined') {
    window.NajikaConfig = {
        API_BASE_URL,
        WS_BASE_URL,
        API_ENDPOINTS,
        WS_CONFIG,
        ENV
    };
}
