/**
 * RADIO NAJIKA - Fallout-Style Radio System
 * ==========================================
 *
 * Wie Galaxy News Radio in Fallout - der Spieler KANN zuhören, MUSS aber nicht.
 * - R-Taste: Radio EIN/AUS
 * - Najika kommentiert Welt-Events, Gerüchte, Tipps
 * - Verschiedene "Sender" (später: Echoharp hat eigenen Sender)
 * - In bestimmten Regionen: Lautsprecher die automatisch senden
 * - Passt sich an Biome/Situation an
 *
 * KEINE nervige Erzählerin - Radio kann jederzeit abgeschaltet werden!
 */

const RadioNajika = (function() {
    'use strict';

    // ==========================================
    // RADIO STATE
    // ==========================================

    const state = {
        isOn: false,
        volume: 0.8,
        currentStation: 'radio_najika',
        currentMessage: null,
        messageQueue: [],
        lastMessageTime: 0,
        messageCooldown: 15000,   // 15 Sekunden zwischen Messages
        loudspeakerRange: 30,     // Range für Stadt-Lautsprecher
        nearLoudspeaker: false,
        displayElement: null,
        lastBiome: '',
        lastEventCheck: 0,
        messagesPlayed: 0
    };

    // ==========================================
    // RADIO STATIONEN
    // ==========================================

    const STATIONS = {
        radio_najika: {
            name: 'Radio Najika',
            host: 'Najika',
            icon: '📻',
            color: '#ff6b9d',
            // DJ-Persönlichkeit: Megumin-Style enthusiastisch
            greeting: [
                "Hier ist Radio Najika! Eure Lieblings-Explosions-Expertin am Mikrofon!",
                "Moshi moshi~! Hier ist Najika, live aus der Schwarzen Mühle!",
                "EXPLOSION-Radio ist ON AIR! Kuja, hörst du mich?",
                "Radio Najika meldet sich! Die Stimme der Crimson Magic Clan auf Sendung!"
            ]
        },
        echoharp_fm: {
            name: 'Echoharp FM',
            host: 'Echoharp',
            icon: '🎵',
            color: '#9b59b6',
            greeting: [
                "...Echoharp FM... Melodien aus der Tiefe...",
                "*leises Summen* ...die Saiten der Welt vibrieren...",
                "Echoharp FM. Stille. Dann Musik."
            ]
        }
    };

    // ==========================================
    // MESSAGE-DATENBANK (Biome-basiert)
    // ==========================================

    const BIOME_MESSAGES = {
        samtmoos: [
            "Achtung Reisende! Im Samtmoos-Tiefwald wurden wieder Wolfrudel gesichtet. Passt auf eure Vorräte auf!",
            "Gerücht aus dem Wald: Angeblich hat jemand den Sporax gesehen... den PILZFÜRST! Wer sich traut, dem winkt reiche Beute!",
            "Die Bäume im Samtmoos flüstern heute besonders laut. Druide Kaito sagt, das bedeutet Regen. Oder Monster. Eines von beiden.",
            "Tipp vom Profi: Wildschweine droppen Fleisch! Perfekt zum Kochen am Lagerfeuer!"
        ],
        reich_der_drei: [
            "BRRR! Wer in Richtung Reich der Drei unterwegs ist - packt warme Kleidung ein! Die Eiskönigin Crystalia ist NICHT gastfreundlich!",
            "Eiswölfe haben einen Karawanen-Konvoi angegriffen! Die Händler bitten um Hilfe!",
            "Fun Fact: Yeti-Fell ist das wärmste Material der Welt! Wenn man einen Yeti findet... und überlebt.",
            "Vorsicht in den Schneewüsten! Frost-Riesen können einen mit einem Schlag plattmachen!"
        ],
        heisse_duenen: [
            "Die Heißen Dünen sind heute extra heiß! Wasser mitnehmen, Leute!",
            "Sandwürmer! SANDWÜRMER! Bleibt auf festem Boden und sie können euch nichts tun... theoretisch.",
            "Der Feuerfürst Ignis wurde letzte Nacht in der Ferne gesehen. Seine Flammen leuchteten bis zum Götterfels!",
            "Scorpion-Schwänze sind übrigens super Alchemie-Zutaten! Nur nicht stechen lassen!"
        ],
        salzwind: [
            "Ahoi! Die Salzwind-Küste ist heute ruhig. Perfekt zum Fischen!",
            "WARNUNG: Der Kraken wurde wieder gesichtet! Bleibt weg vom tiefen Wasser!",
            "Riesenkrabben haben wieder den Strand übernommen. Gratis Seafood für alle Mutigen!",
            "Kapitän Akira sucht immer noch seinen Schatz. Wer hilft, bekommt reichlich Belohnung!"
        ],
        magmastroeme: [
            "Die Magmaströme brodeln heute besonders stark! Feuer-Resistenz empfohlen!",
            "BREAKING: Der Vulkantitan Pyroclast schläft noch... aber seine Diener sind hellwach!",
            "Obsidian-Scherben gibt's hier massenhaft! Perfekt für Waffen-Crafting!",
            "Lavadrachen = Gefahr Level EXPLOSION! Nur für erfahrene Abenteurer!"
        ],
        gruenschlamm: [
            "Der Grünschlamm-Sumpf stinkt heute besonders schlimm. Giftfrösche überall!",
            "Die Sumpfkönigin Morbia verbreitet wieder ihren Giftnebel. Antidote einpacken!",
            "Tipp: Sumpfschleim-Gel ist super zum Craften! Nur nicht anfassen ohne Handschuhe.",
            "Jemand hat im Sumpf seltene Heilkräuter gefunden! Die Kräuterhexe Midori zahlt gut dafür!"
        ],
        blitzebene: [
            "ACHTUNG! Gewitter über der Blitzebene! Metallrüstung vielleicht NICHT die beste Wahl!",
            "Blitzfalken sind die schnellsten Kreaturen der Welt! Versuch mal einen zu fangen... ha!",
            "Der Donnerfürst Voltaris kontrolliert das Wetter hier. Bei Sonnenschein hat er gute Laune. Bei Gewitter... nicht.",
            "Sturmkristalle sind MEGA wertvoll! Aber nur während eines Gewitters zu finden!"
        ],
        tiefenhoehlen: [
            "Die Tiefenhöhlen... dunkel, gefährlich und voller Schätze! Fackeln nicht vergessen!",
            "WARNUNG: Der Kristalldrache wurde in den unteren Ebenen gesichtet! Nicht alleine runtergehen!",
            "Höhlenpilze leuchten im Dunkeln! Kostenlose Taschenlampe der Natur!",
            "Der Tiefenkönig Abyssal... sie sagen er existiert nicht. Aber ich habe seine Schreie gehört!"
        ],
        goetterfels: [
            "Willkommen am Götterfels! Die sicherste Zone der ganzen Welt!",
            "Der Reisende Händler Tomoe hat heute frische Waren! Schaut mal vorbei!",
            "Abenteurer Hiro sucht Helfer für verschiedene Aufträge. Gold winkt!",
            "Die Schwarze Mühle steht wie immer stolz am Götterfels. Home sweet home!",
            "Die Kräuterhexe Midori hat neue Tränke im Angebot! Vorbeischauen lohnt sich!"
        ]
    };

    // Allgemeine Messages (biome-unabhängig)
    const GENERAL_MESSAGES = [
        "Denkt dran: J für Zauber, K für Schwert, Q für Parry, Space für Dodge! Tastatur-Krieger-Style!",
        "Quest-Tipp: Sprecht mit NPCs in der Nähe! Die haben immer was zu tun für mutige Abenteurer!",
        "Hey Kuja! Vergiss nicht ab und zu beim Schmied vorbeizuschauen. Gute Ausrüstung rettet Leben!",
        "FUN FACT: Combo J-K-J-K macht den 'Todestanz'! Extra Schaden, extra cool!",
        "Crafting-Tipp: Kristallscherben + Eisen = starke Waffen! Sammelt alles was glitzert!",
        "Die Welt ist groß! 8 verschiedene Regionen warten auf euch. Habt ihr alle schon besucht?",
        "Gold-Tipp: Bosse droppen das meiste Gold! Hohes Risiko, hohe Belohnung!",
        "Combo-Erinnerung: L-R = Schneller Doppelschlag, R-R-L = Wirbel-Angriff!",
        "Euer Inventar ist fast voll? Verkauft Sachen beim Händler oder craftet was Besseres!"
    ];

    // Event-basierte Messages (getriggert durch GameEvents)
    const EVENT_MESSAGES = {
        enemyKilled: [
            "BOOM! Wieder ein Monster weniger! So muss das, Kuja!",
            "HA! Der hatte keine Chance! *Mikrofon-Drop*",
            "Und wieder ein Sieg! Die Monster sollten langsam Angst kriegen!",
            "EXPLOSION-würdig! So kämpft ein wahrer Held!"
        ],
        questCompleted: [
            "QUEST GESCHAFFT! Najika ist stolz auf dich! *applaudiert ins Mikrofon*",
            "Belohnung kassiert! Weiter so, Kuja! Die Welt braucht dich!",
            "Ein weiterer Auftrag erledigt! Du bist der beste Abenteurer den ich kenne!"
        ],
        regionEntered: [
            "Neue Region betreten! Passt auf euch auf da draußen!",
            "Oh, neues Gebiet! Mal sehen was es hier zu entdecken gibt!"
        ],
        bossKilled: [
            "EIN BOSS IST GEFALLEN! EXPLOSION! EXPLOSIVE NACHRICHTEN AUF RADIO NAJIKA!",
            "BREAKING NEWS: Kuja hat einen Boss besiegt! Die ganze Welt feiert!",
            "DAS WAR... EXPLOSION-LEVEL EPIC! Boss down! BOSS DOWN!"
        ],
        playerDied: [
            "Ähm... Kuja? Alles okay? Du siehst etwas... tot aus. Aber das wird schon!",
            "Okay okay, Rückschlag. Passiert den Besten! Steh auf und zeig es ihnen!"
        ]
    };

    // ==========================================
    // RADIO UI
    // ==========================================

    function createRadioUI() {
        // Haupt-Container
        const container = document.createElement('div');
        container.id = 'radio-najika-container';
        container.style.cssText = `
            position: fixed; bottom: 15px; right: 15px;
            width: 300px; z-index: 900;
            font-family: 'Courier New', monospace;
            pointer-events: none; transition: all 0.5s ease;
            opacity: 0;
        `;

        // Radio-Box
        container.innerHTML = `
            <div id="radio-box" style="
                background: linear-gradient(180deg, rgba(20,10,5,0.95), rgba(40,20,10,0.9));
                border: 2px solid #8B4513; border-radius: 12px;
                padding: 10px 15px; color: #FFD700;
                box-shadow: 0 0 15px rgba(255,107,157,0.3);
            ">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                    <span id="radio-station-name" style="font-size:12px; color:#ff6b9d;">📻 Radio Najika</span>
                    <span id="radio-status" style="font-size:10px; color:#666;">OFF</span>
                </div>
                <div id="radio-message" style="
                    font-size: 13px; color: #ddd; line-height: 1.4;
                    max-height: 60px; overflow: hidden;
                    text-overflow: ellipsis;
                ">
                    Drücke [R] zum Einschalten
                </div>
                <div id="radio-bar" style="
                    height: 3px; background: #333; border-radius: 2px; margin-top: 8px;
                    overflow: hidden;
                ">
                    <div id="radio-bar-fill" style="
                        height: 100%; width: 0%; background: linear-gradient(90deg, #ff6b9d, #FFD700);
                        transition: width linear;
                    "></div>
                </div>
            </div>
        `;

        document.body.appendChild(container);
        state.displayElement = container;
    }

    // ==========================================
    // RADIO CONTROLS
    // ==========================================

    function toggleRadio() {
        state.isOn = !state.isOn;

        const container = state.displayElement;
        const statusEl = document.getElementById('radio-status');
        const msgEl = document.getElementById('radio-message');

        if (state.isOn) {
            container.style.opacity = '1';
            statusEl.textContent = 'ON AIR';
            statusEl.style.color = '#00ff00';

            // Begrüßung
            const station = STATIONS[state.currentStation];
            const greeting = station.greeting[Math.floor(Math.random() * station.greeting.length)];
            showMessage(greeting);

            // Message-Loop starten
            startMessageLoop();

            console.log('📻 Radio Najika: ON');
        } else {
            statusEl.textContent = 'OFF';
            statusEl.style.color = '#666';
            msgEl.textContent = 'Drücke [R] zum Einschalten';

            // Fade out nach kurz
            setTimeout(() => {
                if (!state.isOn) container.style.opacity = '0.3';
            }, 2000);

            console.log('📻 Radio Najika: OFF');
        }
    }

    function showMessage(text) {
        const msgEl = document.getElementById('radio-message');
        const barFill = document.getElementById('radio-bar-fill');
        if (!msgEl) return;

        state.currentMessage = text;
        state.lastMessageTime = Date.now();

        // Typewriter-Effekt
        msgEl.textContent = '';
        let charIndex = 0;
        const typeSpeed = 30; // ms pro Zeichen

        const typeInterval = setInterval(() => {
            if (charIndex < text.length) {
                msgEl.textContent += text[charIndex];
                charIndex++;
                // Progress-Bar
                if (barFill) {
                    barFill.style.width = `${(charIndex / text.length) * 100}%`;
                    barFill.style.transition = `width ${typeSpeed}ms linear`;
                }
            } else {
                clearInterval(typeInterval);
                // Bar bleibt voll, dann langsam zurück
                setTimeout(() => {
                    if (barFill) {
                        barFill.style.transition = 'width 2s ease';
                        barFill.style.width = '0%';
                    }
                }, 3000);
            }
        }, typeSpeed);

        state.messagesPlayed++;
    }

    // ==========================================
    // MESSAGE SELECTION (Biome + Events)
    // ==========================================

    function getNextMessage() {
        const biome = getCurrentBiome();

        // 60% Biome-spezifisch, 40% allgemein
        if (Math.random() < 0.6 && BIOME_MESSAGES[biome]) {
            const msgs = BIOME_MESSAGES[biome];
            return msgs[Math.floor(Math.random() * msgs.length)];
        } else {
            return GENERAL_MESSAGES[Math.floor(Math.random() * GENERAL_MESSAGES.length)];
        }
    }

    function getCurrentBiome() {
        if (window.OverworldEnemies) {
            return window.OverworldEnemies.getCurrentBiome() || 'goetterfels';
        }
        return 'goetterfels';
    }

    // ==========================================
    // MESSAGE LOOP
    // ==========================================

    let messageLoopInterval = null;

    function startMessageLoop() {
        if (messageLoopInterval) clearInterval(messageLoopInterval);

        messageLoopInterval = setInterval(() => {
            if (!state.isOn) {
                clearInterval(messageLoopInterval);
                return;
            }

            const now = Date.now();
            if (now - state.lastMessageTime < state.messageCooldown) return;

            // Queued Messages haben Priorität
            if (state.messageQueue.length > 0) {
                showMessage(state.messageQueue.shift());
            } else {
                showMessage(getNextMessage());
            }
        }, 3000); // Check alle 3 Sekunden
    }

    // ==========================================
    // GAME EVENT REACTIONS
    // ==========================================

    function connectToGameEvents() {
        if (!window.GameEvents) return;

        window.GameEvents.on('enemyKilled', (data) => {
            if (!state.isOn) return;

            // Boss-Kill = besondere Nachricht
            if (data.rarity === 'boss') {
                const msgs = EVENT_MESSAGES.bossKilled;
                state.messageQueue.push(msgs[Math.floor(Math.random() * msgs.length)]);
            } else if (Math.random() < 0.2) {
                // 20% Chance auf Kommentar bei normalem Kill
                const msgs = EVENT_MESSAGES.enemyKilled;
                state.messageQueue.push(msgs[Math.floor(Math.random() * msgs.length)]);
            }
        });

        window.GameEvents.on('questCompleted', (data) => {
            if (!state.isOn) return;
            const msgs = EVENT_MESSAGES.questCompleted;
            state.messageQueue.push(msgs[Math.floor(Math.random() * msgs.length)]);
        });

        window.GameEvents.on('regionEntered', (data) => {
            if (!state.isOn) return;
            const biome = data.biome;
            if (biome !== state.lastBiome) {
                state.lastBiome = biome;
                // Region-spezifische Begrüßung
                if (BIOME_MESSAGES[biome]) {
                    state.messageQueue.push(BIOME_MESSAGES[biome][0]); // Erste Message = Begrüßung
                }
                if (Math.random() < 0.5) {
                    const msgs = EVENT_MESSAGES.regionEntered;
                    state.messageQueue.push(msgs[Math.floor(Math.random() * msgs.length)]);
                }
            }
        });
    }

    // ==========================================
    // LOUDSPEAKER SYSTEM (Stadt-Lautsprecher)
    // ==========================================

    const LOUDSPEAKER_POSITIONS = [
        { x: 4800, z: 4800, name: 'Götterfels-Zentrum' },
        { x: 4850, z: 4850, name: 'Händlerplatz' },
        { x: 4700, z: 4900, name: 'Schmiede' }
    ];

    function checkLoudspeakers() {
        if (!window.character || !window.character.position) return;

        const px = window.character.position.x;
        const pz = window.character.position.z;

        let nearSpeaker = false;
        LOUDSPEAKER_POSITIONS.forEach(speaker => {
            const dx = px - speaker.x;
            const dz = pz - speaker.z;
            const dist = Math.sqrt(dx * dx + dz * dz);
            if (dist < state.loudspeakerRange) {
                nearSpeaker = true;
            }
        });

        // Auto-Einschalten bei Lautsprecher, Auto-Aus wenn weg
        if (nearSpeaker && !state.nearLoudspeaker) {
            state.nearLoudspeaker = true;
            if (!state.isOn) {
                // Temporär einschalten
                state.isOn = true;
                const container = state.displayElement;
                if (container) {
                    container.style.opacity = '1';
                    const statusEl = document.getElementById('radio-status');
                    if (statusEl) { statusEl.textContent = '🔊 LAUTSPRECHER'; statusEl.style.color = '#00bfff'; }
                }
                showMessage("*Lautsprecher-Durchsage* " + getNextMessage());
                startMessageLoop();
            }
        } else if (!nearSpeaker && state.nearLoudspeaker) {
            state.nearLoudspeaker = false;
            // Nicht ausschalten wenn manuell eingeschaltet
        }
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        createRadioUI();

        // R-Taste für Radio Toggle
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            if (e.code === 'KeyR' && !e.ctrlKey && !e.altKey) {
                e.preventDefault();
                toggleRadio();
            }
        });

        // GameEvents verbinden
        connectToGameEvents();

        // Loudspeaker-Check Loop
        setInterval(checkLoudspeakers, 2000);

        console.log('📻 Radio Najika System loaded! Press [R] to toggle!');
    }

    // Auto-init wenn DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    return {
        toggle: toggleRadio,
        isOn: () => state.isOn,
        queueMessage: (msg) => state.messageQueue.push(msg),
        showMessage,
        setStation: (stationId) => {
            if (STATIONS[stationId]) {
                state.currentStation = stationId;
                const nameEl = document.getElementById('radio-station-name');
                const station = STATIONS[stationId];
                if (nameEl) nameEl.textContent = `${station.icon} ${station.name}`;
            }
        },
        getStations: () => Object.keys(STATIONS),
        addBiomeMessages: (biome, messages) => {
            if (!BIOME_MESSAGES[biome]) BIOME_MESSAGES[biome] = [];
            BIOME_MESSAGES[biome].push(...messages);
        }
    };
})();

window.RadioNajika = RadioNajika;
