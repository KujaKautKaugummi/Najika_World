/**
 * NAJIKA WORLD - POSTMAN SYSTEM
 * ==============================
 * Paper Boy meets Postman (Kevin Costner) in einer Fallout-Welt
 *
 * Postman = Ranger-Status in Najika World
 * - Sonderboten für wichtige Nachrichten, Kräuter, seltene Güter
 * - NICHT Alltags-Post an 1000 Häuser!
 * - Spezielle Postman-Kleidung (Maske + Mantel) = PFLICHT
 * - Transport: IMMER zu Fuß! Allein. Mutig. Wie ein Ranger.
 * - PvP-Risiko: Andere Spieler können überfallen
 * - Strafe: König jagt Angreifer (nur wenn identifiziert!)
 * - Empfänger = Schräge Borderlands-NPCs
 *
 * Die Außenwelt regeneriert bei jedem Verlassen der Städte
 * → Oregon Trail Events + Postman-Routen = Endlose Abenteuer!
 */

(function() {
    'use strict';

    // ==========================================
    // POSTMAN RANG-SYSTEM
    // ==========================================

    const POSTMAN_RANKS = {
        novize:     { name: 'Novize',          level: 1,  icon: '📮', payMulti: 1.0, routeSlots: 1 },
        bote:       { name: 'Bote',            level: 5,  icon: '📬', payMulti: 1.3, routeSlots: 2 },
        kurier:     { name: 'Kurier',          level: 10, icon: '📨', payMulti: 1.6, routeSlots: 3 },
        fernbote:   { name: 'Fernbote',        level: 20, icon: '🏇', payMulti: 2.0, routeSlots: 4 },
        postmeister:{ name: 'Postmeister',     level: 35, icon: '👑', payMulti: 2.5, routeSlots: 5 },
        legende:    { name: 'Postman-Legende', level: 50, icon: '⭐', payMulti: 3.0, routeSlots: 6 },
    };

    // ==========================================
    // POSTMAN-KLEIDUNG (Erkennungs-Pflicht!)
    // ==========================================

    const POSTMAN_GEAR = {
        mantel: {
            name: 'Postman-Mantel',
            slot: 'body',
            icon: '🧥',
            defense: 8,
            speed: -0.05, // Leicht langsamer (schwerer Mantel)
            buff: { stamina_regen: 1.15 }, // +15% Ausdauer-Regeneration
            description: 'Der legendäre Mantel der Postman. Markiert den Träger klar als Boten.',
            required: true, // MUSS getragen werden für Aufträge
        },
        maske: {
            name: 'Postman-Maske',
            slot: 'head',
            icon: '🎭',
            defense: 3,
            buff: { perception: 1.2 }, // +20% Wahrnehmung (Gefahren erkennen)
            description: 'Die markante Maske. Jeder erkennt einen Postman an ihr.',
            required: true,
        },
        tasche: {
            name: 'Postman-Tasche',
            slot: 'accessory',
            icon: '👜',
            carryCapacity: 5, // Max 5 Lieferungen gleichzeitig
            buff: { loot_protection: 0.3 }, // 30% Chance Loot bei Tod zu behalten
            description: 'Spezielle Tasche für Lieferungen. Schützt teilweise vor Verlust.',
            required: true,
        },
    };

    // ==========================================
    // LIEFERUNGS-TYPEN
    // ==========================================

    const DELIVERY_TYPES = {
        nachricht: {
            name: 'Wichtige Nachricht',
            icon: '📜',
            weight: 0.1,
            basePay: 50,
            riskLevel: 1,
            description: 'Ein versiegelter Brief. Inhalt unbekannt.',
        },
        krauter: {
            name: 'Seltene Kräuter',
            icon: '🌿',
            weight: 0.5,
            basePay: 120,
            riskLevel: 2,
            description: 'Medizinische Kräuter die schnell geliefert werden müssen.',
        },
        artefakt: {
            name: 'Mystisches Artefakt',
            icon: '🔮',
            weight: 1.0,
            basePay: 300,
            riskLevel: 3,
            description: 'Ein magisches Objekt von großem Wert. Vorsicht!',
        },
        waffen: {
            name: 'Waffenlieferung',
            icon: '⚔️',
            weight: 2.0,
            basePay: 200,
            riskLevel: 3,
            description: 'Geschmiedete Waffen für einen wichtigen Kunden.',
        },
        gold_transport: {
            name: 'Goldtransport',
            icon: '💰',
            weight: 3.0,
            basePay: 500,
            riskLevel: 4,
            description: 'Reiner Goldtransport. Höchste Gefahr!',
        },
        geheimbotschaft: {
            name: 'Geheimbotschaft',
            icon: '🔒',
            weight: 0.1,
            basePay: 400,
            riskLevel: 4,
            description: 'Verschlüsselte Nachricht. Darf NICHT geöffnet werden.',
        },
        heilmittel: {
            name: 'Dringendes Heilmittel',
            icon: '💊',
            weight: 0.3,
            basePay: 250,
            riskLevel: 2,
            timeLimit: 300, // 5 Minuten!
            description: 'Ein Leben hängt davon ab! Schnell liefern!',
        },
        handelsware: {
            name: 'Exotische Handelsware',
            icon: '📦',
            weight: 1.5,
            basePay: 180,
            riskLevel: 2,
            description: 'Seltene Güter aus fernen Biomen.',
        },
    };

    // ==========================================
    // EMPFÄNGER-NPCs (Borderlands-Style Persönlichkeiten!)
    // ==========================================

    const DELIVERY_NPCS = [
        {
            name: 'Verrückter Viktor',
            biome: 'samtmoos',
            icon: '🤪',
            personality: 'Redet mit Pilzen. Glaubt er sei selbst ein Pilz.',
            dialogue_happy: 'HAHA! Endlich! Die Pilze sagten mir du kommst! Die PILZE wissen ALLES!',
            dialogue_late: 'Zu spät! Die Pilze sind WÜTEND! Du weißt nicht was wütende Pilze tun!',
            tipMulti: 1.5, // Gibt ordentlich Trinkgeld
        },
        {
            name: 'Eiserne Else',
            biome: 'reich_der_drei',
            icon: '💪',
            personality: 'Ex-Schmiedin. Bricht Türen statt sie zu öffnen.',
            dialogue_happy: '*zerquetscht Paket beim Öffnen* Oh. Ups. Danke trotzdem.',
            dialogue_late: '*biegt Laternenpfahl* Du hast mich warten lassen. Ich HASSE warten.',
            tipMulti: 0.8, // Geizig
        },
        {
            name: 'Sandflüsterer Mahmud',
            biome: 'heisse_duenen',
            icon: '🏜️',
            personality: 'Spricht nur in Rätseln. Niemand versteht ihn.',
            dialogue_happy: 'Wenn der Sand spricht und der Wind schweigt, dann ist die Lieferung... ja.',
            dialogue_late: 'Der Sand weinte drei Tränen. Das bedeutet... naja, du weißt schon.',
            tipMulti: 1.2,
        },
        {
            name: 'Kapitänin Salz',
            biome: 'salzwind',
            icon: '🏴‍☠️',
            personality: 'Ex-Piratin. Alles ist "Beute". Auch die Post.',
            dialogue_happy: 'YARRR! Feine Beute! Ich meine... feine POST! *hustet*',
            dialogue_late: 'In meiner Zeit hätten wir den Boten über die Planke geschickt!',
            tipMulti: 1.0,
        },
        {
            name: 'Flammen-Fiona',
            biome: 'magmastroeme',
            icon: '🔥',
            personality: 'Pyromantikerin. Testet ALLES mit Feuer.',
            dialogue_happy: '*hält Brief ans Feuer* Nur zum Prüfen... OH es brennt! Egal, danke!',
            dialogue_late: '*zündelt nervös* Weißt du was passiert wenn ich ZU LANGE warte?!',
            tipMulti: 1.3,
        },
        {
            name: 'Sumpf-Opa Krötrich',
            biome: 'gruenschlamm',
            icon: '🐸',
            personality: 'Sehr alt. Erzählt 4-Stunden-Geschichten. Hat 47 Kröten.',
            dialogue_happy: 'Ahhh, setz dich Kind! Lass mich dir von 1847 erzählen, als ich...',
            dialogue_late: 'In MEINER Zeit... *3 Stunden später* ...und DESHALB war Post pünktlich!',
            tipMulti: 0.5, // Arm aber nett
        },
        {
            name: 'Blitz-Baronin Zara',
            biome: 'blitzebene',
            icon: '⚡',
            personality: 'Alles muss SCHNELL gehen. Spricht in Stakkato.',
            dialogue_happy: 'Gut. Schnell. Danke. Geh. Tschüss. Nächster!',
            dialogue_late: 'LANGSAM! ZU! LANGSAM! Inakzeptabel! Schneller! SCHNELLER!',
            tipMulti: 2.0, // Zahlt gut für schnelle Lieferung
        },
        {
            name: 'Tiefen-Thaddäus',
            biome: 'tiefenhoehlen',
            icon: '🕯️',
            personality: 'Lebt seit 20 Jahren unter der Erde. Hat Angst vor Himmel.',
            dialogue_happy: '*flüstert* Danke... bitte kein Sonnenlicht reinlassen...',
            dialogue_late: '*panisch* Die Decke... bewegt sie sich?! IST DAS DER HIMMEL?!',
            tipMulti: 1.1,
        },
        {
            name: 'Götterfels-Orakel Iris',
            biome: 'goetterfels',
            icon: '🔮',
            personality: 'Sieht die Zukunft. Spoilert ständig Quests.',
            dialogue_happy: 'Ich WUSSTE dass du pünktlich kommst. Auch, pass morgen auf der Straße auf.',
            dialogue_late: 'Ich habe dein Zuspätkommen vorhergesehen. Hat mich trotzdem enttäuscht.',
            tipMulti: 1.8,
        },
    ];

    // ==========================================
    // POSTMAN STATE
    // ==========================================

    let postmanState = loadState();

    function loadState() {
        try {
            const saved = JSON.parse(localStorage.getItem('najika_postman') || 'null');
            return saved || {
                isPostman: false,
                rank: 'novize',
                xp: 0,
                deliveriesCompleted: 0,
                deliveriesFailed: 0,
                totalGoldEarned: 0,
                reputation: 50, // 0-100
                activeDeliveries: [],
                wantedLevel: 0, // Falls Postman angegriffen
                completedRoutes: [],
            };
        } catch { return { isPostman: false, rank: 'novize', xp: 0, deliveriesCompleted: 0, deliveriesFailed: 0, totalGoldEarned: 0, reputation: 50, activeDeliveries: [], wantedLevel: 0, completedRoutes: [] }; }
    }

    function saveState() {
        localStorage.setItem('najika_postman', JSON.stringify(postmanState));
    }

    // ==========================================
    // ROUTEN-GENERIERUNG
    // ==========================================

    function generateDeliveryRoute(playerBiome) {
        const biomes = ['samtmoos', 'reich_der_drei', 'heisse_duenen', 'salzwind',
                        'magmastroeme', 'gruenschlamm', 'blitzebene', 'tiefenhoehlen', 'goetterfels'];

        // Zielbiom (nicht gleiches Biom, außenwelt regeneriert = immer anderes Terrain!)
        const otherBiomes = biomes.filter(b => b !== playerBiome);
        const targetBiome = otherBiomes[Math.floor(Math.random() * otherBiomes.length)];

        // Empfänger aus Zielbiom
        const possibleNPCs = DELIVERY_NPCS.filter(n => n.biome === targetBiome);
        const npc = possibleNPCs.length > 0
            ? possibleNPCs[Math.floor(Math.random() * possibleNPCs.length)]
            : DELIVERY_NPCS[Math.floor(Math.random() * DELIVERY_NPCS.length)];

        // Lieferungstyp
        const typeKeys = Object.keys(DELIVERY_TYPES);
        const typeKey = typeKeys[Math.floor(Math.random() * typeKeys.length)];
        const deliveryType = DELIVERY_TYPES[typeKey];

        // Distanz-Berechnung (Biom-zu-Biom)
        const distance = calcBiomeDistance(playerBiome, targetBiome);

        // Bezahlung
        const rank = POSTMAN_RANKS[postmanState.rank] || POSTMAN_RANKS.novize;
        const pay = Math.floor(deliveryType.basePay * rank.payMulti * (1 + distance * 0.2));

        const route = {
            id: `delivery_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
            type: typeKey,
            typeName: deliveryType.name,
            typeIcon: deliveryType.icon,
            description: deliveryType.description,
            recipient: npc,
            fromBiome: playerBiome,
            toBiome: targetBiome,
            distance: distance,
            pay: pay,
            riskLevel: deliveryType.riskLevel,
            timeLimit: deliveryType.timeLimit || null,
            startTime: null, // Gesetzt bei Annahme
            status: 'available', // available, active, completed, failed, stolen
            weight: deliveryType.weight,
            // Für PvP: Spieler wissen NICHT was drin ist!
            hiddenValue: Math.floor(Math.random() * 500) + deliveryType.basePay,
        };

        return route;
    }

    function calcBiomeDistance(from, to) {
        // Vereinfachte Distanz basierend auf Biom-Position auf der Map
        // Götterfels ist zentral, andere drumherum
        if (from === to) return 0;
        if (from === 'goetterfels' || to === 'goetterfels') return 1;

        const biomeOrder = ['samtmoos', 'reich_der_drei', 'heisse_duenen', 'salzwind',
                            'magmastroeme', 'gruenschlamm', 'blitzebene', 'tiefenhoehlen'];
        const i1 = biomeOrder.indexOf(from);
        const i2 = biomeOrder.indexOf(to);
        if (i1 === -1 || i2 === -1) return 3;

        const diff = Math.abs(i1 - i2);
        return Math.min(diff, 8 - diff); // Kürzester Weg im Kreis
    }

    // ==========================================
    // POSTMAN AKTIONEN
    // ==========================================

    function becomePostman() {
        if (postmanState.isPostman) return false;

        postmanState.isPostman = true;
        postmanState.rank = 'novize';
        postmanState.xp = 0;
        saveState();

        console.log('📮 Du bist jetzt ein POSTMAN! Zieh deine Ausrüstung an und nimm Aufträge an.');
        if (typeof notify === 'function') {
            notify('📮 Willkommen bei den Postman! Dein Dienst am Königreich beginnt!', 'success');
        }
        return true;
    }

    function acceptDelivery(route) {
        if (!postmanState.isPostman) {
            if (typeof notify === 'function') notify('❌ Du musst erst Postman werden!', 'error');
            return false;
        }

        const rank = POSTMAN_RANKS[postmanState.rank];
        if (postmanState.activeDeliveries.length >= rank.routeSlots) {
            if (typeof notify === 'function') notify(`❌ Max ${rank.routeSlots} aktive Lieferungen (Rang: ${rank.name})`, 'error');
            return false;
        }

        route.status = 'active';
        route.startTime = Date.now();
        postmanState.activeDeliveries.push(route);
        saveState();

        console.log(`📨 Lieferung angenommen: ${route.typeName} → ${route.recipient.name} (${route.toBiome})`);
        if (typeof notify === 'function') {
            notify(`${route.typeIcon} ${route.typeName} → ${route.recipient.icon} ${route.recipient.name}`, 'info');
        }
        return true;
    }

    function completeDelivery(deliveryId) {
        const idx = postmanState.activeDeliveries.findIndex(d => d.id === deliveryId);
        if (idx === -1) return false;

        const delivery = postmanState.activeDeliveries[idx];
        delivery.status = 'completed';

        // Zeitung / Trinkgeld
        const tipMulti = delivery.recipient.tipMulti || 1.0;
        const finalPay = Math.floor(delivery.pay * tipMulti);

        // XP
        const xpGain = Math.floor(20 + delivery.riskLevel * 15 + delivery.distance * 10);
        postmanState.xp += xpGain;
        postmanState.deliveriesCompleted++;
        postmanState.totalGoldEarned += finalPay;
        postmanState.reputation = Math.min(100, postmanState.reputation + 2);

        // Rang-Check
        checkRankUp();

        // Entferne aus aktiven
        postmanState.activeDeliveries.splice(idx, 1);
        postmanState.completedRoutes.push({
            id: delivery.id,
            type: delivery.type,
            recipient: delivery.recipient.name,
            pay: finalPay,
            completedAt: Date.now(),
        });

        saveState();

        console.log(`✅ Lieferung abgeschlossen! +${finalPay}g +${xpGain}XP`);
        if (typeof notify === 'function') {
            notify(`✅ ${delivery.recipient.icon} ${delivery.recipient.name}: "${delivery.recipient.dialogue_happy}" (+${finalPay}g)`, 'success');
        }
        return { pay: finalPay, xp: xpGain, dialogue: delivery.recipient.dialogue_happy };
    }

    function failDelivery(deliveryId, reason) {
        const idx = postmanState.activeDeliveries.findIndex(d => d.id === deliveryId);
        if (idx === -1) return false;

        const delivery = postmanState.activeDeliveries[idx];
        delivery.status = reason === 'stolen' ? 'stolen' : 'failed';

        postmanState.deliveriesFailed++;
        postmanState.reputation = Math.max(0, postmanState.reputation - 5);
        postmanState.activeDeliveries.splice(idx, 1);
        saveState();

        console.log(`❌ Lieferung ${reason || 'fehlgeschlagen'}: ${delivery.typeName}`);
        if (typeof notify === 'function') {
            notify(`❌ Lieferung ${reason || 'fehlgeschlagen'}! Reputation -5`, 'error');
        }
        return true;
    }

    // ==========================================
    // RANG-SYSTEM
    // ==========================================

    function checkRankUp() {
        const rankOrder = Object.keys(POSTMAN_RANKS);
        const currentIdx = rankOrder.indexOf(postmanState.rank);
        const nextRank = rankOrder[currentIdx + 1];

        if (nextRank && postmanState.xp >= getXPForRank(nextRank)) {
            postmanState.rank = nextRank;
            const rank = POSTMAN_RANKS[nextRank];
            console.log(`🎉 RANG-AUFSTIEG! Du bist jetzt ${rank.icon} ${rank.name}!`);
            if (typeof notify === 'function') {
                notify(`🎉 RANG-AUFSTIEG! ${rank.icon} ${rank.name}! (${rank.routeSlots} Routen-Slots)`, 'success');
            }
        }
    }

    function getXPForRank(rank) {
        const xpTable = {
            novize: 0,
            bote: 100,
            kurier: 350,
            fernbote: 800,
            postmeister: 2000,
            legende: 5000,
        };
        return xpTable[rank] || 0;
    }

    // ==========================================
    // PvP-ÜBERFALL MECHANIK
    // ==========================================

    function reportPostmanAttack(attackerName, wasIdentified) {
        // Ein Postman wurde überfallen!
        if (wasIdentified) {
            // Angreifer wurde erkannt → König jagt ihn
            console.log(`🚨 POSTMAN-ÜBERFALL! ${attackerName} wurde IDENTIFIZIERT! Der König schickt Jäger!`);
            if (typeof notify === 'function') {
                notify(`🚨 ${attackerName} wird vom König gejagt! Postman-Überfall!`, 'warning');
            }
            return {
                identified: true,
                attacker: attackerName,
                bounty: 500 + (postmanState.rank === 'legende' ? 2000 : 0),
                kingHunters: true,
            };
        } else {
            // Angreifer unbekannt → Lieferung gestohlen, aber keine Jagd
            console.log(`🥷 POSTMAN-ÜBERFALL! Angreifer UNBEKANNT. Lieferung gestohlen.`);
            if (typeof notify === 'function') {
                notify('🥷 Überfall! Angreifer unbekannt. Lieferung verloren.', 'error');
            }
            return {
                identified: false,
                attacker: null,
                bounty: 0,
                kingHunters: false,
                // ABER: Gestohlene Güter könnten den Dieb verraten!
                traceable: Math.random() < 0.3, // 30% Chance dass Güter verfolgbar sind
            };
        }
    }

    // Kann der Angreifer identifiziert werden?
    function calcIdentificationChance(attackerStealth, postmanPerception, witnesses) {
        let chance = 0.5; // Basis 50%

        // Zeugen in der Nähe (Overworld Props = Camps, Händler, etc.)
        chance += witnesses * 0.15;

        // Tageszeit (Tag = leichter zu erkennen)
        const hour = new Date().getHours();
        if (hour >= 6 && hour < 20) chance += 0.2; // Tageslicht

        // Skills
        chance -= (attackerStealth || 0) * 0.05;
        chance += (postmanPerception || 0) * 0.05;

        return Math.max(0.1, Math.min(0.95, chance));
    }

    // ==========================================
    // RANGER-PERKS (Postman = Ranger von Najika!)
    // Immer zu Fuß. Allein. Heldenhaft. Wie Fallout NV Rangers.
    // ==========================================

    const RANGER_PERKS = {
        lone_wolf: {
            name: 'Einsamer Wolf',
            icon: '🐺',
            description: 'Alleine unterwegs = +15% Schaden, +10% Speed',
            effect: { damage: 1.15, speed: 1.10 },
            requiredRank: 'novize',
        },
        eyes_of_the_road: {
            name: 'Augen der Straße',
            icon: '👁️',
            description: '+25% Chance Hinterhalte zu erkennen',
            effect: { ambush_detection: 0.25 },
            requiredRank: 'bote',
        },
        hardened_soles: {
            name: 'Gehärtete Sohlen',
            icon: '🥾',
            description: '-30% Stamina-Verbrauch beim Laufen',
            effect: { stamina_reduction: 0.30 },
            requiredRank: 'kurier',
        },
        kings_authority: {
            name: 'Autorität des Königs',
            icon: '👑',
            description: 'Banditen fliehen manchmal statt anzugreifen (20%)',
            effect: { bandit_flee_chance: 0.20 },
            requiredRank: 'fernbote',
        },
        legend_walks: {
            name: 'Die Legende wandert',
            icon: '⭐',
            description: 'NPCs erkennen dich. Bessere Preise, Geheimnisse, Respekt.',
            effect: { shop_discount: 0.15, secret_chance: 0.30 },
            requiredRank: 'legende',
        },
    };

    // ==========================================
    // AVAILABLE ROUTES GENERATOR
    // ==========================================

    function getAvailableRoutes(playerBiome, count) {
        const routes = [];
        const num = count || 3;

        for (let i = 0; i < num; i++) {
            routes.push(generateDeliveryRoute(playerBiome || 'reich_der_drei'));
        }

        return routes;
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.PostmanSystem = {
        // State
        getState: () => ({ ...postmanState }),
        isPostman: () => postmanState.isPostman,
        getRank: () => POSTMAN_RANKS[postmanState.rank],

        // Aktionen
        becomePostman,
        acceptDelivery,
        completeDelivery,
        failDelivery,
        getAvailableRoutes,
        generateDeliveryRoute,

        // PvP
        reportPostmanAttack,
        calcIdentificationChance,

        // Daten
        POSTMAN_RANKS,
        POSTMAN_GEAR,
        DELIVERY_TYPES,
        DELIVERY_NPCS,
        RANGER_PERKS,
    };

    console.log('📮 Postman-System geladen!');
    if (postmanState.isPostman) {
        const rank = POSTMAN_RANKS[postmanState.rank];
        console.log(`📬 Aktiver Postman: ${rank.icon} ${rank.name} | ${postmanState.deliveriesCompleted} Lieferungen | ${postmanState.totalGoldEarned}g verdient`);
    }

})();
