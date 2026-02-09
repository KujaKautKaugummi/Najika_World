// ============================================================
// LAW NOTIFICATION SYSTEM - Gesetz-Warnungen & Kopfgeld-Alerts
// Zeigt Warnungen bei Regionswechsel, Verbrechen, Kopfgeldern
// Integration mit survival_system.js
// ============================================================
(function() {
    'use strict';

    const REGION_NAMES = {
        samtmoos: 'Samtmoos', reich_der_drei: 'Reich der Drei',
        heisse_duenen: 'Heiße Dünen', salzwind: 'Salzwind',
        magmastroeme: 'Magmaströme', gruenschlamm: 'Grünschlamm',
        blitzebene: 'Blitzebene', tiefenhoehlen: 'Tiefenhöhlen',
        goetterfels: 'Götterfels',
    };

    class LawNotificationSystem {
        constructor() {
            this.lastRegion = null;
            this.notificationQueue = [];
            this.isShowingNotification = false;
            this.bountyBanner = null;
            this.checkInterval = null;
            this.init();
        }

        init() {
            // Check every 5 seconds for region changes and bounty updates
            this.checkInterval = setInterval(() => this.tick(), 5000);
            // Initial bounty check
            setTimeout(() => this.updateBountyBanner(), 2000);
        }

        tick() {
            const currentRegion = this._getCurrentRegion();

            // Region changed? Show law warning
            if (currentRegion && currentRegion !== this.lastRegion) {
                const oldRegion = this.lastRegion;
                this.lastRegion = currentRegion;
                if (oldRegion !== null) {
                    this.onRegionEnter(currentRegion);
                }
            }

            // Update bounty banner
            this.updateBountyBanner();
        }

        _getCurrentRegion() {
            if (window.Scene3D?.getCurrentBiome) return window.Scene3D.getCurrentBiome();
            if (window.currentBiome) return window.currentBiome;
            return null;
        }

        // ==========================================
        // REGION ENTER - Law Warning
        // ==========================================

        onRegionEnter(region) {
            const ss = window.SurvivalSystem;
            if (!ss) return;

            const laws = ss.REGIONAL_LAWS?.[region];
            const bounties = ss.getBounties?.() || {};
            const regionBounty = bounties[region] || 0;

            // Show region law info
            if (laws) {
                const strictnessLabel = laws.strictness >= 0.8 ? 'STRENG'
                    : laws.strictness >= 0.5 ? 'MODERAT'
                    : laws.strictness >= 0.2 ? 'LOCKER' : 'MINIMAL';
                const strictnessColor = laws.strictness >= 0.8 ? '#e74c3c'
                    : laws.strictness >= 0.5 ? '#f39c12'
                    : laws.strictness >= 0.2 ? '#2ecc71' : '#3498db';

                let body = `⚖️ ${laws.name}\nStrenge: ${strictnessLabel}`;
                if (laws.bribable) body += `\n💰 Bestechung möglich (${Math.round(laws.briberyCost * 100)}% Kosten)`;
                else body += '\n🚫 Bestechung NICHT möglich!';
                if (laws.illegal?.length > 0) {
                    const illegalNames = laws.illegal.map(id => {
                        const g = window.EconomySystem?.GOODS?.[id];
                        return g ? `${g.icon} ${g.name}` : id;
                    });
                    body += `\n🚫 Illegal: ${illegalNames.join(', ')}`;
                }

                this.showNotification({
                    title: `📍 ${REGION_NAMES[region] || region}`,
                    body,
                    color: strictnessColor,
                    duration: 5000,
                    icon: '⚖️',
                });

                // Wanted warning!
                if (regionBounty > 0) {
                    setTimeout(() => {
                        this.showNotification({
                            title: '🚨 ACHTUNG - KOPFGELD!',
                            body: `Du bist hier GESUCHT!\nKopfgeld: ${regionBounty} Gold\n${laws.bribable ? '💰 Bestechung möglich: ' + Math.round(regionBounty * laws.briberyCost) + 'g' : '🚫 Nicht bestechbar!'}`,
                            color: '#e74c3c',
                            duration: 6000,
                            icon: '🚨',
                            pulse: true,
                        });
                    }, 1500);
                }
            } else {
                // Lawless region
                this.showNotification({
                    title: `📍 ${REGION_NAMES[region] || region}`,
                    body: '☠️ GESETZLOSE WILDNIS\nKeine Gesetze, keine Wachen, keine Hilfe!',
                    color: '#888',
                    duration: 4000,
                    icon: '☠️',
                });
            }
        }

        // ==========================================
        // CRIME COMMITTED - Flash Warning
        // ==========================================

        onCrimeCommitted(crimeType, region, result) {
            if (result.caught) {
                this.showNotification({
                    title: '🚨 ERWISCHT!',
                    body: `${result.description || crimeType}\nKopfgeld: +${result.bounty || 0} Gold\n${result.jailOffer ? '⛓️ Gefängnis: ' + result.jailTime + ' Tage oder FLUCHT!' : ''}`,
                    color: '#e74c3c',
                    duration: 6000,
                    icon: '🚨',
                    pulse: true,
                    shake: true,
                });
            } else {
                this.showNotification({
                    title: '😈 Nicht erwischt!',
                    body: `${result.description || crimeType}\n${result.reason || 'Niemand hat es gesehen...'}`,
                    color: '#2ecc71',
                    duration: 3000,
                    icon: '🤫',
                });
            }
            this.updateBountyBanner();
        }

        // ==========================================
        // BOUNTY BANNER (persistent top bar)
        // ==========================================

        updateBountyBanner() {
            const ss = window.SurvivalSystem;
            if (!ss) return;

            const isWanted = ss.isWanted?.() || false;
            const bounties = ss.getBounties?.() || {};
            const totalBounty = Object.values(bounties).reduce((sum, b) => sum + b, 0);

            if (isWanted && totalBounty > 0) {
                if (!this.bountyBanner) {
                    this.bountyBanner = document.createElement('div');
                    this.bountyBanner.id = 'law-bounty-banner';
                    this.bountyBanner.style.cssText = `
                        position: fixed; bottom: 0; left: 0; right: 0;
                        background: linear-gradient(90deg, rgba(192,57,43,0.9), rgba(231,76,60,0.9));
                        padding: 6px 20px;
                        font-family: 'Courier New', monospace; font-size: 12px;
                        color: white; z-index: 600;
                        display: flex; justify-content: space-between; align-items: center;
                        animation: bountyPulse 2s ease-in-out infinite;
                    `;
                    // Add pulse animation
                    if (!document.getElementById('law-notification-styles')) {
                        const style = document.createElement('style');
                        style.id = 'law-notification-styles';
                        style.textContent = `
                            @keyframes bountyPulse { 0%,100%{opacity:0.85;} 50%{opacity:1;} }
                            @keyframes lawSlideIn { from{transform:translateX(120%);opacity:0;} to{transform:translateX(0);opacity:1;} }
                            @keyframes lawShake { 0%,100%{transform:translateX(0);} 10%,30%,50%,70%,90%{transform:translateX(-3px);} 20%,40%,60%,80%{transform:translateX(3px);} }
                            @keyframes lawPulse { 0%,100%{box-shadow:0 0 5px currentColor;} 50%{box-shadow:0 0 20px currentColor;} }
                        `;
                        document.head.appendChild(style);
                    }
                    document.body.appendChild(this.bountyBanner);
                }

                const regionList = Object.entries(bounties)
                    .filter(([, b]) => b > 0)
                    .map(([r, b]) => `${REGION_NAMES[r] || r}: ${b}g`)
                    .join(' | ');

                this.bountyBanner.innerHTML = `
                    <span>🚨 <strong>GESUCHT!</strong> Kopfgeld: <span style="color: #FFD700; font-weight: bold;">${totalBounty} Gold</span></span>
                    <span style="font-size: 10px; color: #ffcccc;">${regionList}</span>
                `;
            } else {
                // Not wanted - remove banner
                if (this.bountyBanner) {
                    this.bountyBanner.remove();
                    this.bountyBanner = null;
                }
            }
        }

        // ==========================================
        // NOTIFICATION DISPLAY
        // ==========================================

        showNotification(opts) {
            this.notificationQueue.push(opts);
            if (!this.isShowingNotification) {
                this._showNext();
            }
        }

        _showNext() {
            if (this.notificationQueue.length === 0) {
                this.isShowingNotification = false;
                return;
            }

            this.isShowingNotification = true;
            const opts = this.notificationQueue.shift();

            const el = document.createElement('div');
            el.style.cssText = `
                position: fixed; top: 80px; right: 15px; z-index: 10001;
                background: rgba(10, 10, 30, 0.95);
                border: 2px solid ${opts.color || '#f39c12'};
                border-left: 4px solid ${opts.color || '#f39c12'};
                padding: 12px 18px; border-radius: 8px;
                font-family: 'Courier New', monospace;
                max-width: 380px; min-width: 250px;
                animation: lawSlideIn 0.4s ease-out${opts.shake ? ', lawShake 0.5s ease-in-out 0.4s' : ''};
                ${opts.pulse ? 'animation: lawSlideIn 0.4s ease-out, lawPulse 1.5s ease-in-out infinite;' : ''}
                color: ${opts.color || '#f39c12'};
            `;

            el.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                    <div style="font-size: 14px; font-weight: bold; color: ${opts.color || '#f39c12'};">${opts.title}</div>
                    <span style="font-size: 18px;">${opts.icon || '⚖️'}</span>
                </div>
                <div style="font-size: 12px; color: #ccc; white-space: pre-line; line-height: 1.5;">${opts.body}</div>
            `;

            el.onclick = () => {
                el.remove();
                this._showNext();
            };

            document.body.appendChild(el);

            const duration = opts.duration || 4000;
            setTimeout(() => {
                el.style.transition = 'opacity 0.5s, transform 0.5s';
                el.style.opacity = '0';
                el.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    el.remove();
                    this._showNext();
                }, 500);
            }, duration);
        }

        // ==========================================
        // PUBLIC: Manual triggers
        // ==========================================

        warnIllegalItem(itemId) {
            const good = window.EconomySystem?.GOODS?.[itemId];
            if (!good || good.legal) return;

            const region = this._getCurrentRegion();
            const ss = window.SurvivalSystem;
            const laws = ss?.REGIONAL_LAWS?.[region];

            if (laws && laws.illegal?.includes(itemId)) {
                this.showNotification({
                    title: '⚠️ ILLEGALE WARE!',
                    body: `${good.icon} ${good.name} ist in ${REGION_NAMES[region] || region} VERBOTEN!\nBesitz = Schmuggel-Strafe!`,
                    color: '#e74c3c',
                    duration: 4000,
                    icon: '🚫',
                });
            }
        }

        warnBountyRegion(region) {
            const ss = window.SurvivalSystem;
            const bounties = ss?.getBounties?.() || {};
            if (bounties[region] > 0) {
                this.showNotification({
                    title: '⚠️ KOPFGELD AKTIV!',
                    body: `In ${REGION_NAMES[region] || region} bist du GESUCHT!\nKopfgeld: ${bounties[region]} Gold`,
                    color: '#e74c3c',
                    duration: 4000,
                    icon: '🚨',
                    pulse: true,
                });
            }
        }
    }

    window.lawNotification = new LawNotificationSystem();
    console.log('⚖️ LawNotificationSystem geladen');
})();
