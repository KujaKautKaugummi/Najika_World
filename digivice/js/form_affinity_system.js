/**
 * Form-Affinitaet System - Najika World
 * =======================================
 * Erweitert die Form-Boni aus slime_companion.js mit:
 * - Aura-Element Synergien (Form + passende Aura = Mega-Bonus)
 * - UI: Boni-Anzeige im Form-Dialog
 * - Dynamische Berechnung basierend auf Aura-Level & Element
 *
 * Formen geben +5-10% Base-Bonus.
 * Mit passender Aura: bis zu +50% bei Goettlich-Level!
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // FORM-AFFINITAET DATENBANK
    // ==========================================
    // Jede Form hat einen Base-Bonus + Aura-Synergie

    const FORM_AFFINITIES = {
        // Region-Key : { base Bonus, welche Aura synergisiert, Synergie-Bonus }
        heisse_duenen: {
            name: 'Wuesten-Echse',
            icon: '\uD83E\uDD8E',
            element: 'Earth',
            baseBonuses: [
                { type: 'Hitze-Resistenz', value: 0.05, icon: '\uD83D\uDD25' },
                { type: 'Wuesten-Schaden', value: 0.10, icon: '\u2694' }
            ],
            auraSynergy: {
                element: 'flammen',
                bonus: 'Feuer-Schaden',
                maxValue: 0.50,
                description: 'Feuer + Wueste = Glutwandler'
            }
        },
        samtmoos_tiefwald: {
            name: 'Wald-Wolf',
            icon: '\uD83D\uDC3A',
            element: 'Nature',
            baseBonuses: [
                { type: 'Bewegung im Wald', value: 0.15, icon: '\uD83C\uDFF3' },
                { type: 'Faehrten-Findung', value: 0.10, icon: '\uD83D\uDC3E' }
            ],
            auraSynergy: {
                element: 'natur',
                bonus: 'Natur-Heilung',
                maxValue: 0.50,
                description: 'Natur + Wald = Waldwaechter'
            }
        },
        salzwind_kueste: {
            name: 'Wellen-Qualle',
            icon: '\uD83C\uDF0A',
            element: 'Water',
            baseBonuses: [
                { type: 'Schwimm-Speed', value: 0.12, icon: '\uD83C\uDFCA' },
                { type: 'Fisch-Qualitaet', value: 0.15, icon: '\uD83C\uDF4C' }
            ],
            auraSynergy: {
                element: 'wasser',
                bonus: 'Wasser-Meisterschaft',
                maxValue: 0.50,
                description: 'Wasser + Kueste = Tidenherrscher'
            }
        },
        blitzebene: {
            name: 'Blitz-Vogel',
            icon: '\u26A1',
            element: 'Lightning',
            baseBonuses: [
                { type: 'Angriffs-Speed', value: 0.10, icon: '\u26A1' },
                { type: 'Paralyse-Chance', value: 0.08, icon: '\uD83D\uDCA5' }
            ],
            auraSynergy: {
                element: 'blitz',
                bonus: 'Blitz-Kettenreaktion',
                maxValue: 0.50,
                description: 'Blitz + Ebene = Sturmrufer'
            }
        },
        gruenschlamm_sumpf: {
            name: 'Sumpf-Molch',
            icon: '\uD83D\uDC38',
            element: 'Poison',
            baseBonuses: [
                { type: 'Gift-Resistenz', value: 0.15, icon: '\u2620' },
                { type: 'Alchemie-Effektivitaet', value: 0.12, icon: '\uD83E\uDDEA' }
            ],
            auraSynergy: {
                element: 'gift',
                bonus: 'Gift-Meisterschaft',
                maxValue: 0.50,
                description: 'Gift + Sumpf = Seuchenbringer'
            }
        },
        reich_der_drei: {
            name: 'Eis-Hase',
            icon: '\uD83D\uDC30',
            element: 'Ice',
            baseBonuses: [
                { type: 'Kaelte-Resistenz', value: 0.15, icon: '\u2744' },
                { type: 'Eis-Schaden', value: 0.10, icon: '\u2744' }
            ],
            auraSynergy: {
                element: 'frost',
                bonus: 'Frost-Schild',
                maxValue: 0.50,
                description: 'Frost + Eis = Frostkaiser'
            }
        },
        magmastroeme: {
            name: 'Vulkan-Salamander',
            icon: '\uD83D\uDD25',
            element: 'Fire',
            baseBonuses: [
                { type: 'Feuer-Schaden', value: 0.12, icon: '\uD83D\uDD25' },
                { type: 'Schmiede-Bonus', value: 0.15, icon: '\uD83D\uDD28' }
            ],
            auraSynergy: {
                element: 'flammen',
                bonus: 'Magma-Ruestung',
                maxValue: 0.50,
                description: 'Feuer + Magma = Vulkangeist'
            }
        },
        tiefenhoehlen: {
            name: 'Kristall-Spinne',
            icon: '\uD83D\uDC8E',
            element: 'Crystal',
            baseBonuses: [
                { type: 'Nacht-Crit', value: 0.20, icon: '\uD83C\uDF19' },
                { type: 'Licht-Radius', value: 0.15, icon: '\uD83D\uDCA1' }
            ],
            auraSynergy: {
                element: 'kristall',
                bonus: 'Kristall-Reflexion',
                maxValue: 0.50,
                description: 'Kristall + Hoehle = Prismenspinne'
            }
        },
        // Spezial-Formen
        regenbogen_blob: {
            name: 'Regenbogen-Blob',
            icon: '\uD83C\uDF08',
            element: 'All',
            baseBonuses: [
                { type: 'Alle Resistenzen', value: 0.05, icon: '\uD83C\uDF08' },
                { type: 'Glueck', value: 0.10, icon: '\uD83C\uDF40' }
            ],
            auraSynergy: {
                element: 'goettliche',
                bonus: 'Regenbogen-Schild',
                maxValue: 0.75,
                description: 'Goettlich + Regenbogen = Kosmischer Blob'
            }
        },
        koenig_schleim: {
            name: 'Koenig-Schleim',
            icon: '\uD83D\uDC51',
            element: 'Royal',
            baseBonuses: [
                { type: 'NPC-Handelspreise', value: 0.15, icon: '\uD83D\uDCB0' },
                { type: 'Trust-Gain', value: 0.10, icon: '\u2764' }
            ],
            auraSynergy: {
                element: 'heilig',
                bonus: 'Koenigsaura',
                maxValue: 0.50,
                description: 'Heilig + Koenig = Himmlischer Herrscher'
            }
        }
    };

    // ==========================================
    // BERECHNUNG
    // ==========================================

    function calculateBonuses(formKey, auraElement, auraLevel) {
        const affinity = FORM_AFFINITIES[formKey];
        if (!affinity) return null;

        const auraMultiplier = getAuraMultiplier(auraLevel);
        const hasSynergy = affinity.auraSynergy.element === auraElement;

        // Base Boni (skaliert mit Aura-Level)
        const bonuses = affinity.baseBonuses.map(b => ({
            type: b.type,
            icon: b.icon,
            baseValue: b.value,
            scaledValue: b.value * auraMultiplier,
            display: `+${(b.value * auraMultiplier * 100).toFixed(1)}%`
        }));

        // Synergie-Bonus (nur wenn passende Aura)
        let synergyBonus = null;
        if (hasSynergy) {
            const synergyValue = affinity.auraSynergy.maxValue * (auraLevel / 5);
            synergyBonus = {
                type: affinity.auraSynergy.bonus,
                value: synergyValue,
                display: `+${(synergyValue * 100).toFixed(1)}%`,
                title: affinity.auraSynergy.description
            };
        }

        return {
            form: affinity.name,
            icon: affinity.icon,
            element: affinity.element,
            bonuses,
            synergyBonus,
            hasSynergy,
            auraLevel,
            totalPower: bonuses.reduce((sum, b) => sum + b.scaledValue, 0) +
                        (synergyBonus ? synergyBonus.value : 0)
        };
    }

    function getAuraMultiplier(level) {
        const multipliers = [1.0, 1.05, 1.10, 1.20, 1.35, 1.50];
        return multipliers[level] || 1.0;
    }

    // ==========================================
    // UI: BONI-ANZEIGE
    // ==========================================

    function showAffinityPanel(formKey) {
        const existing = document.getElementById('form-affinity-panel');
        if (existing) existing.remove();

        // Hole aktuelle Aura-Daten vom Slime
        let auraElement = null;
        let auraLevel = 0;
        if (window.slimeCompanion) {
            auraLevel = window.slimeCompanion.auraLevel || 0;
            auraElement = window.slimeCompanion.currentAura || null;
        }

        const result = calculateBonuses(formKey, auraElement, auraLevel);
        if (!result) return;

        const affinity = FORM_AFFINITIES[formKey];
        const panel = document.createElement('div');
        panel.id = 'form-affinity-panel';
        panel.style.cssText = `
            position:fixed; bottom:120px; left:20px;
            background:linear-gradient(135deg, rgba(10,10,30,0.95), rgba(5,5,15,0.98));
            border:2px solid rgba(255,215,0,0.3);
            border-radius:12px; padding:15px; color:white;
            font-family:'Courier New',monospace; z-index:600;
            min-width:250px; max-width:300px;
            box-shadow:0 8px 32px rgba(0,0,0,0.8);
        `;

        let bonusHtml = result.bonuses.map(b => `
            <div style="display:flex;justify-content:space-between;align-items:center;
                padding:4px 0;font-size:11px;">
                <span>${b.icon} ${b.type}</span>
                <span style="color:#4CAF50;font-weight:bold;">${b.display}</span>
            </div>
        `).join('');

        let synergyHtml = '';
        if (result.hasSynergy && result.synergyBonus) {
            synergyHtml = `
                <div style="margin-top:8px;padding:8px;background:rgba(255,215,0,0.1);
                    border:1px solid rgba(255,215,0,0.3);border-radius:8px;">
                    <div style="font-size:10px;color:#FFD700;margin-bottom:4px;font-weight:bold;">
                        SYNERGIE AKTIV!</div>
                    <div style="display:flex;justify-content:space-between;font-size:11px;">
                        <span>${result.synergyBonus.type}</span>
                        <span style="color:#FFD700;font-weight:bold;">${result.synergyBonus.display}</span>
                    </div>
                    <div style="font-size:9px;color:rgba(255,215,0,0.6);margin-top:4px;font-style:italic;">
                        "${result.synergyBonus.title}"</div>
                </div>
            `;
        } else if (affinity.auraSynergy) {
            synergyHtml = `
                <div style="margin-top:8px;padding:8px;background:rgba(255,255,255,0.03);
                    border:1px dashed rgba(255,255,255,0.15);border-radius:8px;">
                    <div style="font-size:10px;color:rgba(255,255,255,0.4);">
                        Synergie moeglich mit: ${affinity.auraSynergy.element}-Aura</div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px;">
                        ${affinity.auraSynergy.description}</div>
                </div>
            `;
        }

        panel.innerHTML = `
            <button onclick="document.getElementById('form-affinity-panel').remove()"
                style="position:absolute;top:6px;right:8px;background:none;border:none;
                color:rgba(255,255,255,0.5);font-size:16px;cursor:pointer;">x</button>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <span style="font-size:28px;">${result.icon}</span>
                <div>
                    <div style="font-size:13px;font-weight:bold;">${result.form}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.4);">
                        Element: ${result.element} | Aura Lv.${auraLevel}
                    </div>
                </div>
            </div>
            <div style="font-size:10px;color:rgba(255,215,0,0.6);margin-bottom:6px;
                letter-spacing:1px;">BASE BONI</div>
            ${bonusHtml}
            ${synergyHtml}
            <div style="margin-top:10px;text-align:center;font-size:10px;color:rgba(255,255,255,0.3);">
                Gesamtstaerke: ${(result.totalPower * 100).toFixed(1)}%
            </div>
        `;

        document.body.appendChild(panel);

        // Auto-close nach 10s
        setTimeout(() => {
            const el = document.getElementById('form-affinity-panel');
            if (el) el.remove();
        }, 10000);
    }

    // ==========================================
    // COMBAT INTEGRATION
    // ==========================================

    function getActiveBonuses() {
        if (!window.slimeCompanion) return null;

        const formKey = window.slimeCompanion.currentForm;
        const auraLevel = window.slimeCompanion.auraLevel || 0;
        const auraElement = window.slimeCompanion.currentAura || null;

        return calculateBonuses(formKey, auraElement, auraLevel);
    }

    function applyCombatBonuses(baseDamage, damageType) {
        const bonuses = getActiveBonuses();
        if (!bonuses) return baseDamage;

        let modifier = 1.0;

        bonuses.bonuses.forEach(b => {
            if (b.type.toLowerCase().includes('schaden') || b.type.toLowerCase().includes('damage')) {
                modifier += b.scaledValue;
            }
        });

        if (bonuses.synergyBonus) {
            modifier += bonuses.synergyBonus.value;
        }

        return Math.round(baseDamage * modifier);
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.FormAffinitySystem = {
        FORM_AFFINITIES,
        calculateBonuses,
        showAffinityPanel,
        getActiveBonuses,
        applyCombatBonuses,
        getAuraMultiplier,
    };

    const formCount = Object.keys(FORM_AFFINITIES).length;
    console.log(`[OK] Form-Affinitaet System geladen: ${formCount} Formen mit Synergien`);

})();
