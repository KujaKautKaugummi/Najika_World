/**
 * NAJIKA WORKER SYSTEM
 * =====================
 * Job-Automation fuer rekrutierte/versklavte Kreaturen.
 *
 * - Jobs produzieren Ressourcen ueber Zeit
 * - Arbeiter muessen gefuettert + bezahlt werden
 * - Expeditionen: Arbeiter auf Sammel-Mission schicken
 * - Schicht-System: Mehrere Kreaturen teilen sich einen Job
 * - Spieler kann selbst arbeiten = spart Geld + Career-XP (Learning by Doing!)
 *
 * Job-Definitionen sind beliebig erweiterbar.
 */
(function() {
    'use strict';

    const STORAGE_KEY = 'najika_workers';

    // ==========================================
    // JOB DEFINITIONS (erweiterbar!)
    // ==========================================

    const JOB_DEFINITIONS = {
        holzfaeller: {
            name: 'Holzfaeller',
            icon: '🪓',
            produces: { id: 'holz', name: 'Holz', amount: 2, weight: 3 },
            cycleTime: 300000,   // 5 min
            feedCost: { id: 'brot', amount: 1 },
            payCost: 5,
            skill: 'holzfaeller',
            playerXP: 15,
            description: 'Faellt Baeume und sammelt Holz.',
        },
        bergmann: {
            name: 'Bergmann',
            icon: '⛏️',
            produces: { id: 'erz', name: 'Erz', amount: 1, weight: 4 },
            cycleTime: 360000,   // 6 min
            feedCost: { id: 'brot', amount: 1 },
            payCost: 8,
            skill: 'bergmann',
            playerXP: 20,
            description: 'Baut Erz und Mineralien ab.',
        },
        sammler: {
            name: 'Sammler',
            icon: '🌿',
            produces: { id: 'heilkraut', name: 'Heilkraut', amount: 3, weight: 0.2 },
            cycleTime: 240000,   // 4 min
            feedCost: { id: 'brot', amount: 1 },
            payCost: 3,
            skill: 'sammler',
            playerXP: 10,
            description: 'Sammelt Kraeuter, Beeren und Pilze.',
        },
        jaeger: {
            name: 'Jaeger',
            icon: '🏹',
            produces: { id: 'fleisch', name: 'Fleisch', amount: 1, weight: 2 },
            cycleTime: 360000,
            feedCost: { id: 'brot', amount: 1 },
            payCost: 7,
            skill: 'jaeger',
            playerXP: 18,
            description: 'Jagt Wild und bringt Fleisch und Leder.',
        },
        fischer: {
            name: 'Fischer',
            icon: '🎣',
            produces: { id: 'fisch', name: 'Fisch', amount: 2, weight: 1.5 },
            cycleTime: 300000,
            feedCost: { id: 'brot', amount: 1 },
            payCost: 4,
            skill: 'fischer',
            playerXP: 12,
            description: 'Angelt Fische an Gewaessern.',
        },
        wache: {
            name: 'Wache',
            icon: '🛡️',
            produces: null,
            effect: 'area_guard',
            cycleTime: 600000,   // 10 min
            feedCost: { id: 'brot', amount: 1 },
            payCost: 10,
            skill: 'soeldner',
            playerXP: 8,
            description: 'Bewacht ein Gebiet. Verhindert Diebstahl, warnt vor Feinden.',
        },
        kutscher: {
            name: 'Kutscher',
            icon: '🐂',
            produces: null,
            effect: 'wagon_driver',
            cycleTime: 0,
            feedCost: { id: 'brot', amount: 1 },
            payCost: 6,
            skill: null,
            playerXP: 5,
            description: 'Fuehrt einen Wagen. Automatisches Follow ohne Speed-Penalty.',
        },
        schmied: {
            name: 'Schmied',
            icon: '🔨',
            produces: null,
            effect: 'repair_items',
            cycleTime: 480000,   // 8 min
            feedCost: { id: 'brot', amount: 2 },
            payCost: 12,
            skill: 'schmied',
            playerXP: 25,
            description: 'Repariert Ausruestung und schmiedet einfache Waffen.',
        },
        haendler: {
            name: 'Haendler',
            icon: '💰',
            produces: null,
            effect: 'passive_income',
            cycleTime: 600000,
            feedCost: { id: 'brot', amount: 1 },
            payCost: 0,  // Earns money instead
            earnAmount: 15,
            skill: 'haendler',
            playerXP: 10,
            description: 'Handelt mit Waren und verdient passiv Gold.',
        },
    };

    // ==========================================
    // STATE
    // ==========================================

    let assignments = [];
    let initialized = false;

    // ==========================================
    // PERSISTENCE
    // ==========================================

    function save() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(assignments));
        } catch (e) {}
    }

    function load() {
        try {
            const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
            if (Array.isArray(data)) assignments = data;
        } catch (e) { assignments = []; }
    }

    // ==========================================
    // ASSIGNMENT MANAGEMENT
    // ==========================================

    function generateId() {
        return 'wa_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6);
    }

    function assignWorker(creatureId, jobKey) {
        const job = JOB_DEFINITIONS[jobKey];
        if (!job) return { success: false, error: `Unbekannter Job: ${jobKey}` };

        // Check not already assigned
        if (assignments.find(a => a.creatureId === creatureId)) {
            return { success: false, error: 'Kreatur hat bereits einen Job!' };
        }

        // Determine creature type
        let creatureType = 'recruited';
        let creatureName = creatureId;

        const recruit = window.CreatureRecruit?.getRecruitedCreatures?.()?.find(r => r.id === creatureId);
        if (recruit) {
            creatureName = recruit.name;
            creatureType = 'recruited';
        } else {
            const slave = window.CreatureRecruit?.getEnslavedCreatures?.()?.find(s => s.id === creatureId);
            if (slave) {
                creatureName = slave.name;
                creatureType = 'enslaved';
            }
        }

        const assignment = {
            id: generateId(),
            creatureId,
            creatureName,
            creatureType,
            job: jobKey,
            assignedAt: Date.now(),
            lastCycleAt: Date.now(),
            pendingOutput: [],
            shiftSlot: 0,
            isOnExpedition: false,
            expeditionReturn: null,
            expeditionRewards: [],
        };

        assignments.push(assignment);

        // Also assign in creature_recruit
        if (window.CreatureRecruit?.assignJob) {
            window.CreatureRecruit.assignJob(creatureId, jobKey);
        }

        save();
        console.log(`[WORKER] ${creatureName} → ${job.name}`);
        return { success: true, assignment };
    }

    function removeWorker(assignmentId) {
        assignments = assignments.filter(a => a.id !== assignmentId);
        save();
    }

    function collectOutput(assignmentId) {
        const assignment = assignments.find(a => a.id === assignmentId);
        if (!assignment || assignment.pendingOutput.length === 0) {
            return { success: false, error: 'Nichts zum Abholen' };
        }

        const collected = [];
        const leftover = [];

        for (const item of assignment.pendingOutput) {
            const weight = (item.weight || 0) * (item.count || 1);
            if (window.WeightSystem && !window.WeightSystem.canPickUp(weight)) {
                leftover.push(item);
                continue;
            }
            if (window.InventoryV2?.addItem) {
                const added = window.InventoryV2.addItem(item);
                if (added === false) { leftover.push(item); continue; }
            }
            collected.push(item);
        }

        assignment.pendingOutput = leftover;
        save();

        return { success: true, collected, remaining: leftover.length };
    }

    // ==========================================
    // EXPEDITIONS
    // ==========================================

    function sendOnExpedition(assignmentId, config) {
        const assignment = assignments.find(a => a.id === assignmentId);
        if (!assignment) return { success: false, error: 'Nicht gefunden' };
        if (assignment.isOnExpedition) return { success: false, error: 'Bereits auf Expedition!' };

        const duration = config.duration || 600000; // 10 min default
        const risk = config.risk || 0.1;

        assignment.isOnExpedition = true;
        assignment.expeditionReturn = Date.now() + duration;
        assignment.expeditionConfig = {
            targetResource: config.targetResource || 'holz',
            quantity: config.quantity || 5,
            risk,
            duration,
        };

        save();
        console.log(`[WORKER] ${assignment.creatureName} auf Expedition: ${config.targetResource} x${config.quantity}`);
        return { success: true };
    }

    // ==========================================
    // UPDATE LOOP (5s interval)
    // ==========================================

    function update() {
        const now = Date.now();

        for (const assignment of assignments) {
            const job = JOB_DEFINITIONS[assignment.job];
            if (!job) continue;

            // Check expedition return
            if (assignment.isOnExpedition) {
                if (now >= assignment.expeditionReturn) {
                    processExpeditionReturn(assignment);
                }
                continue;
            }

            // Check cycle completion
            if (job.cycleTime > 0 && (now - assignment.lastCycleAt) >= job.cycleTime) {
                processCycle(assignment, job);
                assignment.lastCycleAt = now;
            }
        }

        save();
    }

    function processCycle(assignment, job) {
        // Pay cost
        if (assignment.creatureType === 'recruited' && job.payCost > 0) {
            const gold = window.InventoryV2?.getGold?.() || 0;
            if (gold >= job.payCost) {
                window.InventoryV2.addGold(-job.payCost);
            } else {
                // Can't pay - loyalty drops
                const recruit = window.CreatureRecruit?.getRecruitedCreatures?.()?.find(r => r.id === assignment.creatureId);
                if (recruit) {
                    recruit.loyalty = Math.max(0, (recruit.loyalty || 50) - 5);
                    console.warn(`[WORKER] ${assignment.creatureName} nicht bezahlt! Loyalitaet sinkt.`);
                }
                return; // Don't produce if not paid
            }
        }

        // Produce output
        if (job.produces) {
            const amount = job.produces.amount;
            // Career bonus
            let bonusMult = 1.0;
            const cs = window.CareerSystem;
            if (cs?.getCareerLevel && job.skill) {
                const level = cs.getCareerLevel(job.skill);
                if (level >= 10) bonusMult = 3.0;
                else if (level >= 5) bonusMult = 2.0;
                else if (level >= 2) bonusMult = 1.5;
            }

            const finalAmount = Math.ceil(amount * bonusMult);

            assignment.pendingOutput.push({
                id: job.produces.id,
                name: job.produces.name || job.produces.id,
                weight: job.produces.weight || 0,
                count: finalAmount,
                icon: job.icon,
            });
        }

        // Special effects
        if (job.effect === 'passive_income' && job.earnAmount) {
            if (window.InventoryV2?.addGold) {
                window.InventoryV2.addGold(job.earnAmount);
            }
        }
    }

    function processExpeditionReturn(assignment) {
        assignment.isOnExpedition = false;
        assignment.expeditionReturn = null;

        const config = assignment.expeditionConfig;
        if (!config) return;

        // Risk check
        if (Math.random() < config.risk) {
            console.log(`[WORKER] ${assignment.creatureName} Expedition FEHLGESCHLAGEN!`);
            if (window.QuestTrackerV2?.showNotification) {
                window.QuestTrackerV2.showNotification(
                    'EXPEDITION FEHLGESCHLAGEN',
                    `${assignment.creatureName} kehrt mit leeren Haenden zurueck!`,
                    '#F44336'
                );
            }
            return;
        }

        // Success!
        const job = JOB_DEFINITIONS[assignment.job];
        assignment.pendingOutput.push({
            id: config.targetResource,
            name: config.targetResource,
            weight: job?.produces?.weight || 1,
            count: config.quantity,
            icon: job?.icon || '📦',
        });

        console.log(`[WORKER] ${assignment.creatureName} Expedition ERFOLGREICH: ${config.quantity}x ${config.targetResource}`);
        if (window.QuestTrackerV2?.showNotification) {
            window.QuestTrackerV2.showNotification(
                'EXPEDITION ERFOLGREICH',
                `${assignment.creatureName}: ${config.quantity}x ${config.targetResource}!`,
                '#4CAF50'
            );
        }

        assignment.expeditionConfig = null;
    }

    // ==========================================
    // PLAYER DOES THE WORK (Learning by Doing!)
    // ==========================================

    let playerWorkTimer = null;
    let playerCurrentJob = null;

    function playerStartWork(jobKey) {
        const job = JOB_DEFINITIONS[jobKey];
        if (!job) return { success: false, error: 'Unbekannter Job' };
        if (playerCurrentJob) return { success: false, error: 'Bereits am Arbeiten!' };

        playerCurrentJob = jobKey;

        if (window.QuestTrackerV2?.showNotification) {
            window.QuestTrackerV2.showNotification(
                'ARBEIT BEGONNEN',
                `${job.icon} ${job.name} - Du arbeitest jetzt selbst!`,
                '#2196F3'
            );
        }

        playerWorkTimer = setInterval(() => {
            // Produce
            if (job.produces) {
                const item = {
                    id: job.produces.id,
                    name: job.produces.name || job.produces.id,
                    weight: job.produces.weight || 0,
                    count: job.produces.amount,
                    icon: job.icon,
                };

                if (window.WeightSystem && !window.WeightSystem.canPickUp(item.weight * item.count)) {
                    playerStopWork();
                    if (window.QuestTrackerV2?.showNotification) {
                        window.QuestTrackerV2.showNotification('ZU SCHWER', 'Inventar voll! Arbeit beendet.', '#FF9800');
                    }
                    return;
                }

                if (window.InventoryV2?.addItem) {
                    window.InventoryV2.addItem(item);
                }
            }

            // Career XP (Learning by Doing - Konosuba style!)
            if (job.skill && job.playerXP && window.CareerSystem?.addXP) {
                window.CareerSystem.addXP(job.skill, job.playerXP);
            }

            // Special effect
            if (job.effect === 'passive_income' && job.earnAmount) {
                if (window.InventoryV2?.addGold) {
                    window.InventoryV2.addGold(job.earnAmount);
                }
            }

            console.log(`[WORKER] Spieler ${job.name}: +${job.produces?.amount || 0}x ${job.produces?.id || 'Effekt'}`);

        }, job.cycleTime || 300000);

        return { success: true, job: job.name };
    }

    function playerStopWork() {
        if (playerWorkTimer) {
            clearInterval(playerWorkTimer);
            playerWorkTimer = null;
        }
        const stoppedJob = playerCurrentJob;
        playerCurrentJob = null;

        if (stoppedJob) {
            const job = JOB_DEFINITIONS[stoppedJob];
            if (window.QuestTrackerV2?.showNotification) {
                window.QuestTrackerV2.showNotification('ARBEIT BEENDET', `${job?.icon || ''} ${job?.name || stoppedJob}`, '#888');
            }
        }

        return { stopped: stoppedJob };
    }

    // ==========================================
    // STATUS
    // ==========================================

    function getWorkerStatus() {
        return assignments.map(a => {
            const job = JOB_DEFINITIONS[a.job];
            const now = Date.now();
            const cycleProgress = job?.cycleTime > 0
                ? Math.min(1, (now - a.lastCycleAt) / job.cycleTime)
                : 0;

            return {
                ...a,
                jobName: job?.name || a.job,
                jobIcon: job?.icon || '?',
                cycleProgress: Math.round(cycleProgress * 100),
                hasPendingOutput: a.pendingOutput.length > 0,
                pendingCount: a.pendingOutput.length,
                expeditionTimeLeft: a.isOnExpedition
                    ? Math.max(0, a.expeditionReturn - now)
                    : 0,
            };
        });
    }

    function getShiftSchedule(jobKey) {
        return assignments.filter(a => a.job === jobKey).map(a => ({
            id: a.id,
            creatureName: a.creatureName,
            shiftSlot: a.shiftSlot,
        }));
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        if (initialized) return;
        initialized = true;

        load();
        setInterval(update, 5000);

        console.log(`[OK] WorkerSystem geladen: ${assignments.length} Arbeiter aktiv`);
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.WorkerSystem = {
        init,
        JOB_DEFINITIONS,
        assignWorker,
        removeWorker,
        collectOutput,
        sendOnExpedition,
        getWorkerStatus,
        getShiftSchedule,
        getAssignments: () => [...assignments],

        // Player work (Learning by Doing!)
        playerStartWork,
        playerStopWork,
        isPlayerWorking: () => playerCurrentJob !== null,
        getPlayerJob: () => playerCurrentJob,

        // Clear on death
        clearAllAssignments: () => {
            assignments = [];
            save();
        },
    };

    console.log('[OK] WorkerSystem geladen');
})();
