/**
 * NAJIKA WEIGHT & ENCUMBRANCE SYSTEM
 * ===================================
 * Zentrales Gewichtssystem + Speed-Modifier-Aggregation.
 *
 * Hybrid-Modell:
 *   0-100% maxWeight  → Normalgeschwindigkeit
 * 100-150% maxWeight  → Progressiver Slowdown (1.0 → 0.5)
 *    >150% maxWeight  → Blockiert (kann nichts aufheben)
 */
(function() {
    'use strict';

    const ENCUMBRANCE_CONFIG = {
        baseMaxWeight: 50,
        strengthScaling: 2.0,
        overburdenThreshold: 1.0,
        hardCapThreshold: 1.5,
        minSpeedMultiplier: 0.5,
        wagonDragPenalty: 0.6,
        injuryPenalty: 0.15,
    };

    // ==========================================
    // WEIGHT CALCULATION
    // ==========================================

    function getStrength() {
        return window.player?.stats?.strength
            || window.player?.strength
            || 0;
    }

    function getEquipmentCarryBonus() {
        let bonus = 0;
        const inv = window.InventoryV2;
        if (!inv) return bonus;

        const equipped = inv.getEquipped ? inv.getEquipped() : {};
        if (equipped && typeof equipped === 'object') {
            Object.values(equipped).forEach(item => {
                if (item && typeof item.carryBonus === 'number') {
                    bonus += item.carryBonus;
                }
            });
        }
        return bonus;
    }

    function getMaxWeight() {
        return ENCUMBRANCE_CONFIG.baseMaxWeight
            + getStrength() * ENCUMBRANCE_CONFIG.strengthScaling
            + getEquipmentCarryBonus();
    }

    function getCurrentWeight() {
        if (window.InventoryV2?.getCurrentWeight) {
            return window.InventoryV2.getCurrentWeight();
        }
        return 0;
    }

    function getEncumbranceRatio() {
        const max = getMaxWeight();
        if (max <= 0) return 0;
        return getCurrentWeight() / max;
    }

    function canPickUp(additionalWeight) {
        const max = getMaxWeight();
        const current = getCurrentWeight();
        return (current + additionalWeight) <= max * ENCUMBRANCE_CONFIG.hardCapThreshold;
    }

    function isOverburdened() {
        return getEncumbranceRatio() > ENCUMBRANCE_CONFIG.overburdenThreshold;
    }

    function isBlocked() {
        return getEncumbranceRatio() > ENCUMBRANCE_CONFIG.hardCapThreshold;
    }

    // ==========================================
    // SPEED MULTIPLIER
    // ==========================================

    function getEncumbranceSpeedMultiplier() {
        const ratio = getEncumbranceRatio();
        if (ratio <= ENCUMBRANCE_CONFIG.overburdenThreshold) return 1.0;
        if (ratio >= ENCUMBRANCE_CONFIG.hardCapThreshold) return ENCUMBRANCE_CONFIG.minSpeedMultiplier;

        // Linear interpolation: 100% → 1.0, 150% → 0.5
        const t = (ratio - ENCUMBRANCE_CONFIG.overburdenThreshold)
                / (ENCUMBRANCE_CONFIG.hardCapThreshold - ENCUMBRANCE_CONFIG.overburdenThreshold);
        return 1.0 - t * (1.0 - ENCUMBRANCE_CONFIG.minSpeedMultiplier);
    }

    function getEquipmentSpeedBonus() {
        let bonus = 0;
        const inv = window.InventoryV2;
        if (!inv) return bonus;

        const equipped = inv.getEquipped ? inv.getEquipped() : {};
        if (equipped && typeof equipped === 'object') {
            Object.values(equipped).forEach(item => {
                if (item && typeof item.speedBonus === 'number') {
                    bonus += item.speedBonus;
                }
            });
        }

        // Also check EquipmentCombat for armor speed bonuses
        const ec = window.EquipmentCombat;
        if (ec?.getEquippedStats) {
            const stats = ec.getEquippedStats();
            if (stats?.speedBonus) bonus += stats.speedBonus;
        }

        return bonus;
    }

    function getMountSpeedMultiplier() {
        const ct = window.CreatureTaming;
        const mount = ct?.getActiveMount?.();
        if (!mount) return 1.0;
        return mount.speedBonus || 1.5;
    }

    function getWagonDragMultiplier() {
        const ws = window.WagonSystem;
        if (!ws || !ws.isPlayerPulling || !ws.isPlayerPulling()) return 1.0;
        return ENCUMBRANCE_CONFIG.wagonDragPenalty;
    }

    function getInjuryMultiplier() {
        const ss = window.SurvivalSystem;
        if (!ss?.getInjuries) return 1.0;

        const injuries = ss.getInjuries();
        if (!injuries || !Array.isArray(injuries)) return 1.0;

        const severeCount = injuries.filter(i =>
            i.severity === 'schwer' || i.severity === 'severe'
        ).length;

        if (severeCount === 0) return 1.0;
        return Math.max(0.3, 1.0 - severeCount * ENCUMBRANCE_CONFIG.injuryPenalty);
    }

    /**
     * THE central speed function. Called from 3d_scene.js updateCharacter().
     * Combines ALL speed modifiers into one multiplier.
     */
    function getMovementSpeedMultiplier() {
        const encumbrance = getEncumbranceSpeedMultiplier();
        const equipBonus = getEquipmentSpeedBonus();
        const injury = getInjuryMultiplier();

        // Mount and wagon drag are mutually exclusive
        const mount = getMountSpeedMultiplier();
        const wagonDrag = getWagonDragMultiplier();

        let multiplier;
        if (mount > 1.0) {
            // Mounted: use mount speed, ignore wagon drag
            multiplier = encumbrance * (1 + equipBonus) * mount * injury;
        } else if (wagonDrag < 1.0) {
            // Pulling wagon: apply drag penalty
            multiplier = encumbrance * (1 + equipBonus) * wagonDrag * injury;
        } else {
            // Normal walking
            multiplier = encumbrance * (1 + equipBonus) * injury;
        }

        return Math.max(0.1, multiplier);
    }

    // ==========================================
    // ENCUMBRANCE STATUS (for UI)
    // ==========================================

    function getStatus() {
        const ratio = getEncumbranceRatio();
        const current = getCurrentWeight();
        const max = getMaxWeight();

        let level, color, label;
        if (ratio <= 1.0) {
            level = 'normal';
            color = '#4CAF50';
            label = 'Normal';
        } else if (ratio <= 1.5) {
            level = 'overburdened';
            color = '#FF9800';
            label = 'Überladen';
        } else {
            level = 'blocked';
            color = '#F44336';
            label = 'BLOCKIERT';
        }

        return {
            current: Math.round(current * 10) / 10,
            max: Math.round(max * 10) / 10,
            ratio: Math.round(ratio * 100),
            level,
            color,
            label,
            speedMultiplier: Math.round(getMovementSpeedMultiplier() * 100),
        };
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.WeightSystem = {
        getMaxWeight,
        getCurrentWeight,
        getEncumbranceRatio,
        getEncumbranceSpeedMultiplier,
        canPickUp,
        isOverburdened,
        isBlocked,
        getMovementSpeedMultiplier,
        getMountSpeedMultiplier,
        getWagonDragMultiplier,
        getInjuryMultiplier,
        getEquipmentSpeedBonus,
        getStatus,
        ENCUMBRANCE_CONFIG,
    };

    console.log('[OK] WeightSystem geladen');
})();
