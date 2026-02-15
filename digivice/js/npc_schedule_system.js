/**
 * NPC TAGESABLAUF / ROUTINE SYSTEM - Najika World
 * ================================================
 *
 * NPCs haben Tagesroutinen wie in Skyrim/Stardew Valley:
 * - Morgens: Aufstehen, zum Arbeitsplatz gehen
 * - Mittags: Pause, Gasthaus, Markt
 * - Abends: Nach Hause, Gasthaus
 * - Nachts: Schlafen (nicht ansprechbar oder nur mürrisch)
 *
 * NPCs bewegen sich auf vordefinierten Waypoints.
 * Wanderer haben eigene Routen zwischen Regionen.
 *
 * Integration: Klinkt sich in OverworldNPCs ein.
 * GameEvents: npcMovedTo, npcActivityChanged, timeOfDayChanged
 */

const NPCScheduleSystem = (function() {
    'use strict';

    // ==========================================
    // TAGESZEIT-SYSTEM
    // ==========================================

    // 1 Echtzeit-Minute = 10 Spielminuten → 1 Tag = 2.4 Stunden Echtzeit
    // Oder: Kürzerer Zyklus für schnelleres Gameplay
    const TIME_CONFIG = {
        REAL_MINUTES_PER_GAME_DAY: 24, // 24 Echtminuten = 1 Spieltag (anpassbar)
        TICKS_PER_SECOND: 1,           // Update-Frequenz
    };

    // Tageszeiten
    const TIME_OF_DAY = {
        DAWN:      5,   // 05:00 - Morgendämmerung
        MORNING:   7,   // 07:00 - Morgen
        MIDDAY:   12,   // 12:00 - Mittag
        AFTERNOON: 14,  // 14:00 - Nachmittag
        EVENING:  18,   // 18:00 - Abend
        NIGHT:    21,   // 21:00 - Nacht
        MIDNIGHT:  0,   // 00:00 - Mitternacht
    };

    // Aktueller Spielzeit-Zustand
    const timeState = {
        gameHour: 8,        // Start um 08:00
        gameMinute: 0,
        dayNumber: 1,
        lastRealTime: Date.now(),
        isPaused: false,
        timeScale: 1.0,    // Speed-Multiplikator
    };

    function getTimeOfDay() {
        const h = timeState.gameHour;
        if (h >= 21 || h < 5)  return 'night';
        if (h >= 5 && h < 7)   return 'dawn';
        if (h >= 7 && h < 12)  return 'morning';
        if (h >= 12 && h < 14) return 'midday';
        if (h >= 14 && h < 18) return 'afternoon';
        if (h >= 18 && h < 21) return 'evening';
        return 'morning';
    }

    function getTimeString() {
        const h = String(timeState.gameHour).padStart(2, '0');
        const m = String(timeState.gameMinute).padStart(2, '0');
        return `${h}:${m}`;
    }

    function updateGameTime() {
        if (timeState.isPaused) return;

        const now = Date.now();
        const deltaReal = (now - timeState.lastRealTime) / 1000; // Sekunden
        timeState.lastRealTime = now;

        // Spielminuten pro Echtzeit-Sekunde
        const gameMinutesPerSecond = (24 * 60) / (TIME_CONFIG.REAL_MINUTES_PER_GAME_DAY * 60);
        const gameMinutesDelta = deltaReal * gameMinutesPerSecond * timeState.timeScale;

        const oldTimeOfDay = getTimeOfDay();

        timeState.gameMinute += gameMinutesDelta;
        while (timeState.gameMinute >= 60) {
            timeState.gameMinute -= 60;
            timeState.gameHour++;
            if (timeState.gameHour >= 24) {
                timeState.gameHour = 0;
                timeState.dayNumber++;
            }
        }

        const newTimeOfDay = getTimeOfDay();
        if (oldTimeOfDay !== newTimeOfDay) {
            onTimeOfDayChanged(oldTimeOfDay, newTimeOfDay);
        }
    }

    let lastTimeOfDay = 'morning';
    function onTimeOfDayChanged(oldTime, newTime) {
        lastTimeOfDay = newTime;
        console.log(`🌅 Tageszeit: ${oldTime} → ${newTime} (${getTimeString()})`);

        if (window.GameEvents) {
            window.GameEvents.emit('timeOfDayChanged', {
                from: oldTime, to: newTime,
                hour: timeState.gameHour, minute: Math.floor(timeState.gameMinute),
                dayNumber: timeState.dayNumber,
            });
        }

        // Alle NPCs updaten
        updateAllNPCSchedules();
    }

    // ==========================================
    // NPC SCHEDULE DEFINITIONEN
    // ==========================================

    // Jeder NPC hat einen Schedule pro Tageszeit
    // position = Zielkoordinaten, activity = Was er tut
    const NPC_SCHEDULES = {
        // === GÖTTERFELS NPCs ===
        'goetterfels_haendler': {
            dawn:      { position: { x: 4820, z: 4820 }, activity: 'sleeping', interactable: false, dialogue_override: '*gähnt* Es ist noch so früh...' },
            morning:   { position: { x: 4850, z: 4850 }, activity: 'working', interactable: true },
            midday:    { position: { x: 4780, z: 4870 }, activity: 'eating', interactable: true, dialogue_override: 'Ah, Mittagspause! Willst du mit mir essen, Reisender?' },
            afternoon: { position: { x: 4850, z: 4850 }, activity: 'working', interactable: true },
            evening:   { position: { x: 4780, z: 4870 }, activity: 'relaxing', interactable: true, dialogue_override: 'Feierabend! Möchtest du trotzdem noch etwas kaufen?' },
            night:     { position: { x: 4820, z: 4820 }, activity: 'sleeping', interactable: false, dialogue_override: '*schnarcht*' },
        },
        'goetterfels_schmied': {
            dawn:      { position: { x: 4750, z: 4880 }, activity: 'waking_up', interactable: false },
            morning:   { position: { x: 4750, z: 4900 }, activity: 'working', interactable: true, dialogue_override: '*hämmert auf Amboss* Oh, ein Kunde!' },
            midday:    { position: { x: 4780, z: 4870 }, activity: 'eating', interactable: true },
            afternoon: { position: { x: 4750, z: 4900 }, activity: 'working', interactable: true },
            evening:   { position: { x: 4780, z: 4870 }, activity: 'drinking', interactable: true, dialogue_override: 'Nach einem harten Tag am Amboss braucht man ein Bier!' },
            night:     { position: { x: 4750, z: 4880 }, activity: 'sleeping', interactable: false },
        },
        'goetterfels_questgeber': {
            dawn:      { position: { x: 4850, z: 4780 }, activity: 'training', interactable: true, dialogue_override: 'Frühes Training! Der frühe Vogel fängt den Wurm!' },
            morning:   { position: { x: 4900, z: 4750 }, activity: 'working', interactable: true },
            midday:    { position: { x: 4780, z: 4870 }, activity: 'eating', interactable: true },
            afternoon: { position: { x: 4950, z: 4700 }, activity: 'patrolling', interactable: true, dialogue_override: 'Ich patrouilliere die Gegend. Hast du etwas Verdächtiges gesehen?' },
            evening:   { position: { x: 4780, z: 4870 }, activity: 'socializing', interactable: true, dialogue_override: 'Hey! Setz dich zu uns ans Feuer und erzähl von deinen Abenteuern!' },
            night:     { position: { x: 4850, z: 4780 }, activity: 'sleeping', interactable: false },
        },
        'goetterfels_hexe': {
            dawn:      { position: { x: 4650, z: 4750 }, activity: 'gathering', interactable: true, dialogue_override: 'Psst! Die besten Kräuter sammelt man im Morgentau!' },
            morning:   { position: { x: 4700, z: 4780 }, activity: 'working', interactable: true },
            midday:    { position: { x: 4700, z: 4780 }, activity: 'brewing', interactable: true, dialogue_override: 'Ich braue gerade einen besonderen Trank... *rührt im Kessel*' },
            afternoon: { position: { x: 4700, z: 4780 }, activity: 'working', interactable: true },
            evening:   { position: { x: 4650, z: 4750 }, activity: 'meditating', interactable: false, dialogue_override: 'Ich meditiere... Bitte nicht stören.' },
            night:     { position: { x: 4650, z: 4750 }, activity: 'stargazing', interactable: true, dialogue_override: 'Die Sterne verraten viel... Komm, ich lese dir dein Schicksal!' },
        },

        // === WANDERNDE NPCs ===
        'wanderer_krieger': {
            dawn:      { position: { x: 3500, z: 3500 }, activity: 'camping', interactable: true },
            morning:   { position: { x: 3800, z: 3800 }, activity: 'traveling', interactable: true, dialogue_override: 'Auf dem Weg nach Götterfels. Willst du mitkommen?' },
            midday:    { position: { x: 4200, z: 4200 }, activity: 'resting', interactable: true },
            afternoon: { position: { x: 4600, z: 4600 }, activity: 'traveling', interactable: true },
            evening:   { position: { x: 4800, z: 4750 }, activity: 'arrived', interactable: true, dialogue_override: 'Endlich Götterfels! Zeit für ein warmes Bett!' },
            night:     { position: { x: 4800, z: 4750 }, activity: 'sleeping', interactable: false },
        },
        'wanderer_magier': {
            dawn:      { position: { x: 5500, z: 3000 }, activity: 'meditating', interactable: false },
            morning:   { position: { x: 5500, z: 3000 }, activity: 'working', interactable: true },
            midday:    { position: { x: 5200, z: 3300 }, activity: 'traveling', interactable: true },
            afternoon: { position: { x: 5000, z: 3800 }, activity: 'researching', interactable: true, dialogue_override: 'Hier ist ein Leyline-Knotenpunkt! Spürst du die Magie?' },
            evening:   { position: { x: 5500, z: 3000 }, activity: 'returning', interactable: true },
            night:     { position: { x: 5500, z: 3000 }, activity: 'stargazing', interactable: true, dialogue_override: 'Die Sterne der Blitzebene sind besonders hell heute Nacht...' },
        },
        'wanderer_schatzjaeger': {
            dawn:      { position: { x: 6000, z: 6000 }, activity: 'preparing', interactable: true, dialogue_override: 'Ich packe meine Ausrüstung! Heute wird der Tag!' },
            morning:   { position: { x: 5800, z: 5800 }, activity: 'exploring', interactable: true },
            midday:    { position: { x: 5500, z: 5500 }, activity: 'digging', interactable: true, dialogue_override: '*gräbt* Ich bin mir SICHER dass hier was ist!' },
            afternoon: { position: { x: 5200, z: 5200 }, activity: 'exploring', interactable: true },
            evening:   { position: { x: 6000, z: 6000 }, activity: 'returning', interactable: true, dialogue_override: 'Naja, heute war nix dabei... Morgen wird besser!' },
            night:     { position: { x: 6000, z: 6000 }, activity: 'sleeping', interactable: false },
        },
    };

    // ==========================================
    // BEWEGUNGS-SYSTEM
    // ==========================================

    const MOVE_SPEED = 3.0;           // Einheiten pro Sekunde
    const ARRIVAL_THRESHOLD = 2.0;    // Ab wann "angekommen"

    // Aktive Bewegungen
    const activeMovements = {};  // npcId → { targetX, targetZ, speed }

    function moveNPCTowards(npc, targetX, targetZ, delta) {
        if (!npc.mesh) return false;

        const currentX = npc.mesh.position.x;
        const currentZ = npc.mesh.position.z;
        const dx = targetX - currentX;
        const dz = targetZ - currentZ;
        const dist = Math.sqrt(dx * dx + dz * dz);

        if (dist < ARRIVAL_THRESHOLD) {
            // Angekommen
            npc.mesh.position.x = targetX;
            npc.mesh.position.z = targetZ;
            npc.position.x = targetX;
            npc.position.z = targetZ;
            return true; // arrived
        }

        // Bewegen
        const moveStep = MOVE_SPEED * delta;
        const ratio = Math.min(moveStep / dist, 1);
        npc.mesh.position.x += dx * ratio;
        npc.mesh.position.z += dz * ratio;

        // NPC-Daten synchron halten
        npc.position.x = npc.mesh.position.x;
        npc.position.z = npc.mesh.position.z;

        // NPC in Bewegungsrichtung drehen
        const angle = Math.atan2(dx, dz);
        npc.mesh.rotation.y = angle;

        return false; // still moving
    }

    // ==========================================
    // SCHEDULE MANAGEMENT
    // ==========================================

    // Aktuelle Activity pro NPC
    const npcActivities = {};  // npcId → { activity, interactable, dialogue_override }

    function updateAllNPCSchedules() {
        const timeOfDay = getTimeOfDay();

        if (!window.OverworldNPCs) return;
        const npcs = window.OverworldNPCs.getNPCs();
        if (!npcs) return;

        npcs.forEach(npc => {
            const schedule = NPC_SCHEDULES[npc.id];
            if (!schedule) return;

            const slot = schedule[timeOfDay];
            if (!slot) return;

            // Activity tracken
            const oldActivity = npcActivities[npc.id]?.activity;
            npcActivities[npc.id] = {
                activity: slot.activity,
                interactable: slot.interactable !== false,
                dialogue_override: slot.dialogue_override || null,
            };

            // Bewegung starten
            if (slot.position) {
                activeMovements[npc.id] = {
                    targetX: slot.position.x,
                    targetZ: slot.position.z,
                    speed: MOVE_SPEED,
                };
            }

            // Activity-Change Event
            if (oldActivity && oldActivity !== slot.activity) {
                if (window.GameEvents) {
                    window.GameEvents.emit('npcActivityChanged', {
                        npcId: npc.id, npcName: npc.name,
                        from: oldActivity, to: slot.activity,
                        timeOfDay,
                    });
                }
            }
        });
    }

    function getNPCActivity(npcId) {
        return npcActivities[npcId] || { activity: 'idle', interactable: true, dialogue_override: null };
    }

    function isNPCInteractable(npcId) {
        const activity = npcActivities[npcId];
        if (!activity) return true; // Default: interactable
        return activity.interactable !== false;
    }

    function getNPCDialogueOverride(npcId) {
        return npcActivities[npcId]?.dialogue_override || null;
    }

    // ==========================================
    // ACTIVITY INDICATORS (Visuelle Hinweise)
    // ==========================================

    const ACTIVITY_ICONS = {
        sleeping:    '💤',
        waking_up:   '🌅',
        working:     '⚒️',
        eating:      '🍖',
        drinking:    '🍺',
        relaxing:    '😌',
        socializing: '🗣️',
        training:    '⚔️',
        gathering:   '🌿',
        brewing:     '🧪',
        meditating:  '🧘',
        stargazing:  '⭐',
        traveling:   '🚶',
        camping:     '⛺',
        resting:     '🪑',
        arrived:     '🏠',
        returning:   '↩️',
        patrolling:  '👁️',
        exploring:   '🗺️',
        digging:     '⛏️',
        preparing:   '🎒',
        researching: '📖',
        idle:        '💬',
    };

    // Activity-Label über NPC anzeigen
    const activitySprites = {};  // npcId → sprite

    function updateActivityIndicator(npc) {
        const activity = npcActivities[npc.id];
        if (!activity) return;

        const icon = ACTIVITY_ICONS[activity.activity] || '💬';

        let sprite = activitySprites[npc.id];
        if (!sprite && npc.mesh && window.THREE) {
            // Activity-Sprite erstellen
            const canvas = document.createElement('canvas');
            canvas.width = 64;
            canvas.height = 64;

            const texture = new THREE.CanvasTexture(canvas);
            const mat = new THREE.SpriteMaterial({ map: texture, transparent: true });
            sprite = new THREE.Sprite(mat);

            const height = (npc.modelScale || 3.5) * 1.5 + 7;
            sprite.position.set(0, height, 0);
            sprite.scale.set(1.5, 1.5, 1);

            npc.mesh.add(sprite);
            activitySprites[npc.id] = sprite;
        }

        if (sprite) {
            // Canvas updaten
            const canvas = sprite.material.map.image;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, 64, 64);

            // Hintergrund
            ctx.fillStyle = activity.interactable ? 'rgba(0,60,0,0.7)' : 'rgba(60,0,0,0.7)';
            ctx.beginPath();
            ctx.arc(32, 32, 28, 0, Math.PI * 2);
            ctx.fill();

            // Icon
            ctx.font = '28px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(icon, 32, 32);

            sprite.material.map.needsUpdate = true;

            // Nicht-interagierbare NPCs etwas transparent machen
            sprite.material.opacity = activity.interactable ? 1.0 : 0.6;
        }
    }

    // ==========================================
    // MAIN UPDATE LOOP
    // ==========================================

    let lastUpdateTime = Date.now();

    function update() {
        const now = Date.now();
        const delta = (now - lastUpdateTime) / 1000;
        lastUpdateTime = now;

        // Spielzeit updaten
        updateGameTime();

        // NPC-Bewegungen updaten
        if (!window.OverworldNPCs) return;
        const npcs = window.OverworldNPCs.getNPCs();
        if (!npcs) return;

        npcs.forEach(npc => {
            const movement = activeMovements[npc.id];
            if (movement) {
                const arrived = moveNPCTowards(npc, movement.targetX, movement.targetZ, delta);
                if (arrived) {
                    delete activeMovements[npc.id];

                    // Arrived Event
                    if (window.GameEvents) {
                        window.GameEvents.emit('npcMovedTo', {
                            npcId: npc.id, npcName: npc.name,
                            x: npc.position.x, z: npc.position.z,
                            activity: npcActivities[npc.id]?.activity,
                        });
                    }
                }
            }

            // Activity-Indicator updaten
            updateActivityIndicator(npc);
        });
    }

    // ==========================================
    // TIME HUD (Uhr oben links)
    // ==========================================

    let timeHud = null;

    function createTimeHud() {
        timeHud = document.createElement('div');
        timeHud.id = 'game-time-hud';
        timeHud.style.cssText = `
            position: fixed; top: 60px; left: 20px;
            background: rgba(0,0,0,0.7); color: #FFD700;
            padding: 6px 14px; border-radius: 8px;
            font-family: 'Courier New', monospace; font-size: 14px;
            z-index: 999; border: 1px solid #444;
            pointer-events: none; user-select: none;
        `;
        document.body.appendChild(timeHud);
    }

    function updateTimeHud() {
        if (!timeHud) return;

        const timeOfDay = getTimeOfDay();
        const timeIcons = {
            dawn: '🌅', morning: '☀️', midday: '🌞',
            afternoon: '⛅', evening: '🌆', night: '🌙',
        };
        const icon = timeIcons[timeOfDay] || '🕐';

        timeHud.innerHTML = `${icon} ${getTimeString()} <span style="color:#888;font-size:11px;">Tag ${timeState.dayNumber}</span>`;
    }

    // ==========================================
    // INTERACTION OVERRIDE
    // ==========================================

    // OverworldNPCs Interaction überschreiben um Schedule zu berücksichtigen
    function patchInteractionSystem() {
        if (!window.OverworldNPCs) {
            setTimeout(patchInteractionSystem, 1000);
            return;
        }

        const originalInteract = window.OverworldNPCs.interactWithNearestNPC;

        // Monkey-patch: Prüfe ob NPC interactable ist
        window.OverworldNPCs.interactWithNearestNPC = function() {
            const npc = window.OverworldNPCs.getNearestNPC();
            if (!npc) return false;

            const activity = getNPCActivity(npc.id);

            if (!activity.interactable) {
                // NPC schläft oder ist beschäftigt
                showBusyMessage(npc, activity);
                return false;
            }

            // Override-Dialogue wenn vorhanden (z.B. "Mittagspause!")
            if (activity.dialogue_override && npc.dialogue && npc.dialogue.length > 0) {
                npc._originalDialogue = npc._originalDialogue || npc.dialogue[0].text;
                npc.dialogue[0].text = activity.dialogue_override;
            }

            return originalInteract.call(window.OverworldNPCs);
        };

        console.log('🕐 NPCSchedule: Interaction-System gepatcht');
    }

    function showBusyMessage(npc, activity) {
        const messages = {
            sleeping: `💤 ${npc.name} schläft tief und fest...`,
            meditating: `🧘 ${npc.name} meditiert. Besser nicht stören.`,
            waking_up: `🌅 ${npc.name} ist gerade erst aufgewacht...`,
        };

        const msg = messages[activity.activity] || `${npc.name} ist gerade beschäftigt.`;

        // Kleine Notification
        const notif = document.createElement('div');
        notif.style.cssText = `
            position: fixed; bottom: 160px; left: 50%; transform: translateX(-50%);
            background: rgba(80,0,0,0.9); color: #ff8888; padding: 10px 20px;
            border-radius: 8px; font-size: 14px; font-family: Arial;
            z-index: 1000; border: 1px solid #ff4444;
            animation: fadeInOut 2.5s ease-in-out forwards;
            pointer-events: none;
        `;
        notif.textContent = msg;

        // CSS Animation einmalig hinzufügen
        if (!document.getElementById('npc-schedule-styles')) {
            const style = document.createElement('style');
            style.id = 'npc-schedule-styles';
            style.textContent = `
                @keyframes fadeInOut {
                    0% { opacity: 0; transform: translateX(-50%) translateY(10px); }
                    15% { opacity: 1; transform: translateX(-50%) translateY(0); }
                    75% { opacity: 1; }
                    100% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 2500);
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        console.log('🕐 NPC Schedule System initializing...');

        createTimeHud();
        patchInteractionSystem();

        // Initial: Alle Schedules setzen
        updateAllNPCSchedules();

        // Main Loop
        setInterval(() => {
            update();
            updateTimeHud();
        }, 1000 / TIME_CONFIG.TICKS_PER_SECOND);

        console.log('✅ NPC Schedule System active!');
        console.log(`   Tageszeit: ${getTimeOfDay()} (${getTimeString()})`);
        console.log(`   ${Object.keys(NPC_SCHEDULES).length} NPCs mit Routinen`);
    }

    // Auto-Init wenn DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => setTimeout(init, 500));
    } else {
        setTimeout(init, 500); // Warten bis OverworldNPCs geladen
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    return {
        init,
        getTimeOfDay,
        getTimeString,
        getGameTime: () => ({ hour: timeState.gameHour, minute: Math.floor(timeState.gameMinute), day: timeState.dayNumber }),
        setTimeScale: (scale) => { timeState.timeScale = Math.max(0, Math.min(10, scale)); },
        pauseTime: () => { timeState.isPaused = true; },
        resumeTime: () => { timeState.isPaused = false; timeState.lastRealTime = Date.now(); },
        setTime: (hour, minute) => {
            timeState.gameHour = hour % 24;
            timeState.gameMinute = minute || 0;
            timeState.lastRealTime = Date.now();
            updateAllNPCSchedules();
        },
        advanceTime: (minutes) => {
            // Advance game time by given minutes
            timeState.gameMinute += minutes;
            while (timeState.gameMinute >= 60) {
                timeState.gameMinute -= 60;
                timeState.gameHour++;
                if (timeState.gameHour >= 24) {
                    timeState.gameHour = 0;
                    timeState.dayNumber++;
                }
            }
            timeState.lastRealTime = Date.now();
            updateAllNPCSchedules();
        },
        getNPCActivity,
        isNPCInteractable,
        getNPCDialogueOverride,
        getSchedules: () => NPC_SCHEDULES,
        addSchedule: (npcId, schedule) => { NPC_SCHEDULES[npcId] = schedule; },
    };
})();

window.NPCScheduleSystem = NPCScheduleSystem;
console.log('🕐 NPC Schedule System loaded!');
