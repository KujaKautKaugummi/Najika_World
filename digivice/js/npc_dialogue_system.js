// =============================================================================
// NPC DIALOGUE TREE SYSTEM - Verzweigte Dialoge mit Najika-Reaktionen
// =============================================================================
// Erstellt: 2026-01-29
// Features:
// - Dialogue Trees mit Choices
// - Najika-Reaktionen (Megumin/Harley/Shiro/Melissa)
// - Shop-Integration
// - Quest-Integration
// - Oregon Trail Events
// =============================================================================

class NPCDialogueSystem {
    constructor() {
        this.currentNPC = null;
        this.currentDialogue = null;
        this.dialogueHistory = [];
        this.dialogueUI = null;
        this.najikaReactionUI = null;

        // Najika's aktive Persoenlichkeit (von Personality Engine)
        this.activePersonality = 'megumin'; // default

        // NPC Daten Cache
        this.npcDataCache = {};

        // Callbacks
        this.onShopOpen = null;
        this.onQuestAccept = null;
        this.onQuestComplete = null;

        this.setupUI();
        this.loadNPCData();

        console.log('[DIALOGUE] NPC Dialogue Tree System initialized');
    }

    // =========================================================================
    // UI SETUP
    // =========================================================================

    setupUI() {
        // Main Dialogue Container
        this.dialogueUI = document.createElement('div');
        this.dialogueUI.id = 'npc-dialogue-ui';
        this.dialogueUI.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 800px;
            background: linear-gradient(135deg, rgba(0,0,0,0.95), rgba(30,30,50,0.95));
            border: 3px solid #FFD700;
            border-radius: 15px;
            padding: 0;
            z-index: 10000;
            display: none;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.3), inset 0 0 20px rgba(0,0,0,0.5);
            font-family: 'Segoe UI', Arial, sans-serif;
            overflow: hidden;
        `;

        this.dialogueUI.innerHTML = `
            <!-- NPC Header -->
            <div id="dialogue-header" style="
                background: linear-gradient(90deg, #FFD700, #FFA500);
                padding: 12px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div id="npc-portrait" style="
                        width: 50px;
                        height: 50px;
                        border-radius: 50%;
                        background: #333;
                        border: 3px solid #fff;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                    ">NPC</div>
                    <div>
                        <div id="npc-name" style="font-weight: bold; font-size: 18px; color: #000;">NPC Name</div>
                        <div id="npc-title" style="font-size: 12px; color: #333;">Occupation</div>
                    </div>
                </div>
                <button id="dialogue-close" style="
                    background: rgba(0,0,0,0.3);
                    color: #fff;
                    border: none;
                    width: 35px;
                    height: 35px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 18px;
                    transition: all 0.2s;
                " onmouseover="this.style.background='#f44336'" onmouseout="this.style.background='rgba(0,0,0,0.3)'">X</button>
            </div>

            <!-- Dialogue Content -->
            <div id="dialogue-content" style="padding: 20px;">
                <!-- NPC Text -->
                <div id="npc-text" style="
                    color: #fff;
                    font-size: 16px;
                    line-height: 1.6;
                    margin-bottom: 15px;
                    min-height: 60px;
                "></div>

                <!-- Najika Reaction (appears when relevant) -->
                <div id="najika-reaction" style="
                    background: linear-gradient(135deg, rgba(255,100,150,0.2), rgba(150,100,255,0.2));
                    border-left: 4px solid #FF69B4;
                    padding: 10px 15px;
                    margin: 15px 0;
                    border-radius: 0 8px 8px 0;
                    display: none;
                ">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 20px;">Najika</span>
                        <span id="najika-personality-badge" style="
                            background: #FF69B4;
                            color: #fff;
                            padding: 2px 8px;
                            border-radius: 10px;
                            font-size: 11px;
                            font-weight: bold;
                        ">MEGUMIN</span>
                    </div>
                    <div id="najika-reaction-text" style="
                        color: #FFB6C1;
                        font-style: italic;
                        margin-top: 8px;
                        font-size: 14px;
                    "></div>
                </div>

                <!-- Choices -->
                <div id="dialogue-choices" style="
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    margin-top: 20px;
                "></div>
            </div>

            <!-- Quick Actions (Shop, Quest, etc.) -->
            <div id="dialogue-actions" style="
                background: rgba(0,0,0,0.3);
                padding: 15px 20px;
                display: none;
                gap: 10px;
                flex-wrap: wrap;
            "></div>
        `;

        document.body.appendChild(this.dialogueUI);

        // Event Listeners
        document.getElementById('dialogue-close').addEventListener('click', () => this.closeDialogue());

        // ESC to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.dialogueUI.style.display !== 'none') {
                this.closeDialogue();
            }
        });
    }

    // =========================================================================
    // NPC DATA LOADING
    // =========================================================================

    async loadNPCData() {
        const regions = [
            'dampfhain', 'goetterfels', 'gruenschlamm', 'handelsfestung',
            'salzigebucht', 'tiefenhoehlen', 'reichderdrei', 'funkensiedlung', 'runenheim'
        ];

        for (const region of regions) {
            try {
                const response = await fetch(`/digivice/data/npcs_${region}.json`);
                if (response.ok) {
                    const data = await response.json();
                    this.npcDataCache[region] = data;
                    console.log(`[DIALOGUE] Loaded NPCs for ${region}: ${data.npcs?.length || 0} NPCs`);
                }
            } catch (err) {
                // Ignoriere fehlende Dateien
            }
        }
    }

    // =========================================================================
    // DIALOGUE START
    // =========================================================================

    startDialogue(npcId, npcData = null) {
        // Finde NPC Daten
        if (!npcData) {
            npcData = this.findNPCById(npcId);
        }

        if (!npcData) {
            console.warn(`[DIALOGUE] NPC not found: ${npcId}`);
            return false;
        }

        this.currentNPC = npcData;
        this.dialogueHistory = [];

        // Update Najika's aktive Persoenlichkeit
        this.updateActivePersonality();

        // UI Update
        this.updateNPCHeader(npcData);

        // Start mit Greeting
        const greeting = this.getRandomGreeting(npcData);
        this.showDialogueNode({
            text: greeting,
            choices: this.buildInitialChoices(npcData),
            najikaReaction: this.getNajikaReaction(npcData, 'greeting')
        });

        // Show UI
        this.dialogueUI.style.display = 'block';

        console.log(`[DIALOGUE] Started dialogue with: ${npcData.name}`);
        return true;
    }

    findNPCById(npcId) {
        for (const region of Object.values(this.npcDataCache)) {
            if (region.npcs) {
                const npc = region.npcs.find(n => n.id === npcId);
                if (npc) return npc;
            }
        }
        return null;
    }

    updateActivePersonality() {
        // Versuche Persoenlichkeit von Personality Engine zu holen
        if (window.PERSONALITY_ENGINE) {
            const state = window.PERSONALITY_ENGINE.getState();
            if (state && state.dominant_personality) {
                this.activePersonality = state.dominant_personality.toLowerCase();
            }
        }

        // Update Badge
        const badge = document.getElementById('najika-personality-badge');
        if (badge) {
            const colors = {
                megumin: '#FF4500',
                harley: '#9932CC',
                shiro: '#4169E1',
                melissa: '#2E8B57'
            };
            badge.textContent = this.activePersonality.toUpperCase();
            badge.style.background = colors[this.activePersonality] || '#FF69B4';
        }
    }

    // =========================================================================
    // UI UPDATES
    // =========================================================================

    updateNPCHeader(npcData) {
        const portrait = document.getElementById('npc-portrait');
        const name = document.getElementById('npc-name');
        const title = document.getElementById('npc-title');

        // Portrait Icon basierend auf Typ
        const typeIcons = {
            'pvp_arena_master': 'Fighters',
            'food_vendor': 'Cooks',
            'weapon_vendor': 'Swords',
            'armor_vendor': 'Shields',
            'general_store': 'Shops',
            'inn_keeper': 'Hotels',
            'blacksmith': 'Hammers',
            'quest_giver': 'Quests',
            'trainer': 'Teachers',
            'vendor': 'Merchants',
            'citizen': 'Citizens'
        };

        portrait.textContent = typeIcons[npcData.type] || 'NPC';
        name.textContent = npcData.name;
        title.textContent = npcData.occupation || npcData.type || 'Bewohner';
    }

    showDialogueNode(node) {
        const textEl = document.getElementById('npc-text');
        const choicesEl = document.getElementById('dialogue-choices');
        const reactionEl = document.getElementById('najika-reaction');
        const reactionTextEl = document.getElementById('najika-reaction-text');

        // Typewriter Effect fuer NPC Text
        this.typewriterEffect(textEl, node.text);

        // Najika Reaction
        if (node.najikaReaction) {
            reactionEl.style.display = 'block';
            reactionTextEl.textContent = node.najikaReaction;
        } else {
            reactionEl.style.display = 'none';
        }

        // Choices
        choicesEl.innerHTML = '';
        if (node.choices && node.choices.length > 0) {
            node.choices.forEach((choice, index) => {
                const btn = document.createElement('button');
                btn.style.cssText = `
                    background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,165,0,0.2));
                    border: 2px solid #FFD700;
                    color: #FFD700;
                    padding: 12px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 14px;
                    text-align: left;
                    transition: all 0.2s;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                `;

                // Hotkey
                const hotkey = index + 1;
                btn.innerHTML = `
                    <span style="
                        background: #FFD700;
                        color: #000;
                        width: 24px;
                        height: 24px;
                        border-radius: 4px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        font-size: 12px;
                    ">${hotkey}</span>
                    <span>${choice.text}</span>
                `;

                btn.onmouseover = () => {
                    btn.style.background = 'linear-gradient(135deg, rgba(255,215,0,0.4), rgba(255,165,0,0.4))';
                    btn.style.transform = 'translateX(5px)';
                };
                btn.onmouseout = () => {
                    btn.style.background = 'linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,165,0,0.2))';
                    btn.style.transform = 'translateX(0)';
                };

                btn.onclick = () => this.selectChoice(choice);
                choicesEl.appendChild(btn);
            });

            // Keyboard shortcuts
            this.setupChoiceHotkeys(node.choices);
        }

        // Quick Actions
        this.updateQuickActions();
    }

    typewriterEffect(element, text, speed = 20) {
        element.textContent = '';
        let i = 0;

        const type = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        };

        type();
    }

    setupChoiceHotkeys(choices) {
        const handler = (e) => {
            const num = parseInt(e.key);
            if (num >= 1 && num <= choices.length) {
                this.selectChoice(choices[num - 1]);
                document.removeEventListener('keydown', handler);
            }
        };

        // Remove old handler
        if (this._choiceHandler) {
            document.removeEventListener('keydown', this._choiceHandler);
        }
        this._choiceHandler = handler;
        document.addEventListener('keydown', handler);
    }

    updateQuickActions() {
        const actionsEl = document.getElementById('dialogue-actions');
        const npc = this.currentNPC;

        if (!npc) {
            actionsEl.style.display = 'none';
            return;
        }

        const actions = [];

        // Shop Button
        if (npc.shop) {
            actions.push({
                text: 'Shop oeffnen',
                icon: 'Shops',
                action: () => this.openShop()
            });
        }

        // Quest Button
        if (npc.quests && npc.quests.length > 0) {
            actions.push({
                text: 'Quests ansehen',
                icon: 'Quests',
                action: () => this.showQuests()
            });
        }

        // Services
        if (npc.services) {
            if (npc.services.rest) {
                actions.push({
                    text: `Ausruhen (${npc.services.rest.price}g)`,
                    icon: 'Sleep',
                    action: () => this.useService('rest')
                });
            }
            if (npc.services.repair) {
                actions.push({
                    text: `Reparieren (${npc.services.repair.price}g)`,
                    icon: 'Tools',
                    action: () => this.useService('repair')
                });
            }
        }

        if (actions.length > 0) {
            actionsEl.style.display = 'flex';
            actionsEl.innerHTML = actions.map(a => `
                <button onclick="window.npcDialogueSystem.${a.action.name ? a.action.name + '()' : ''}" style="
                    background: linear-gradient(135deg, #4CAF50, #45a049);
                    border: none;
                    color: #fff;
                    padding: 10px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    transition: all 0.2s;
                " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    ${a.icon} ${a.text}
                </button>
            `).join('');

            // Re-attach event handlers
            const buttons = actionsEl.querySelectorAll('button');
            buttons.forEach((btn, i) => {
                btn.onclick = actions[i].action;
            });
        } else {
            actionsEl.style.display = 'none';
        }
    }

    // =========================================================================
    // DIALOGUE LOGIC
    // =========================================================================

    getRandomGreeting(npcData) {
        const dialogues = npcData.dialogues;

        if (dialogues && dialogues.greeting) {
            const greetings = Array.isArray(dialogues.greeting)
                ? dialogues.greeting
                : [dialogues.greeting];
            return greetings[Math.floor(Math.random() * greetings.length)];
        }

        // Fallback
        return `Willkommen, Reisender! Ich bin ${npcData.name}.`;
    }

    buildInitialChoices(npcData) {
        const choices = [];

        // Shop
        if (npcData.shop) {
            choices.push({
                text: 'Was verkaufst du?',
                action: 'open_shop',
                nextNode: {
                    text: this.getShopDialogue(npcData),
                    choices: [
                        { text: 'Shop oeffnen', action: 'open_shop_ui' },
                        { text: 'Zurueck', action: 'back' }
                    ],
                    najikaReaction: this.getNajikaReaction(npcData, 'shop')
                }
            });
        }

        // Quests
        if (npcData.quests && npcData.quests.length > 0) {
            choices.push({
                text: 'Hast du Auftraege fuer mich?',
                action: 'show_quests',
                nextNode: {
                    text: this.getQuestDialogue(npcData),
                    choices: this.buildQuestChoices(npcData),
                    najikaReaction: this.getNajikaReaction(npcData, 'quest')
                }
            });
        }

        // Services
        if (npcData.services) {
            if (npcData.services.rest) {
                choices.push({
                    text: 'Ich moechte mich ausruhen',
                    action: 'rest',
                    nextNode: {
                        text: this.getRestDialogue(npcData),
                        choices: [
                            { text: `Ja, ausruhen (${npcData.services.rest.price}g)`, action: 'confirm_rest' },
                            { text: 'Nein, danke', action: 'back' }
                        ],
                        najikaReaction: this.getNajikaReaction(npcData, 'rest')
                    }
                });
            }
        }

        // Small Talk / Info
        if (npcData.dialogues && npcData.dialogues.story) {
            choices.push({
                text: 'Erzaehl mir etwas',
                action: 'story',
                nextNode: {
                    text: this.getStoryDialogue(npcData),
                    choices: [{ text: 'Interessant!', action: 'back' }]
                }
            });
        }

        // Rumors
        if (npcData.dialogues && npcData.dialogues.rumor) {
            choices.push({
                text: 'Hast du Geruechte gehoert?',
                action: 'rumor',
                nextNode: {
                    text: this.getRumorDialogue(npcData),
                    choices: [{ text: 'Danke fuer die Info!', action: 'back' }],
                    najikaReaction: this.getNajikaReactionForRumor()
                }
            });
        }

        // Goodbye
        choices.push({
            text: 'Auf Wiedersehen',
            action: 'close'
        });

        return choices;
    }

    getShopDialogue(npcData) {
        const dialogues = npcData.dialogues;
        if (dialogues && dialogues.shop) {
            const shops = Array.isArray(dialogues.shop) ? dialogues.shop : [dialogues.shop];
            return shops[Math.floor(Math.random() * shops.length)];
        }
        return 'Schau dir meine Waren an!';
    }

    getQuestDialogue(npcData) {
        const dialogues = npcData.dialogues;
        if (dialogues && dialogues.quest_available) {
            return dialogues.quest_available;
        }
        if (dialogues && dialogues.quest_intro) {
            const intros = Array.isArray(dialogues.quest_intro) ? dialogues.quest_intro : [dialogues.quest_intro];
            return intros[Math.floor(Math.random() * intros.length)];
        }
        return 'Ich habe eine Aufgabe fuer dich...';
    }

    getRestDialogue(npcData) {
        const dialogues = npcData.dialogues;
        if (dialogues && dialogues.rest) {
            const rests = Array.isArray(dialogues.rest) ? dialogues.rest : [dialogues.rest];
            return rests[Math.floor(Math.random() * rests.length)];
        }
        return 'Moechtest du dich ausruhen?';
    }

    getStoryDialogue(npcData) {
        const dialogues = npcData.dialogues;
        if (dialogues && dialogues.story) {
            const stories = Array.isArray(dialogues.story) ? dialogues.story : [dialogues.story];
            return stories[Math.floor(Math.random() * stories.length)];
        }
        return 'Es gibt viel zu erzaehlen...';
    }

    getRumorDialogue(npcData) {
        const dialogues = npcData.dialogues;
        if (dialogues && dialogues.rumor) {
            const rumors = Array.isArray(dialogues.rumor) ? dialogues.rumor : [dialogues.rumor];
            return rumors[Math.floor(Math.random() * rumors.length)];
        }
        return 'Ich habe gehoert...';
    }

    buildQuestChoices(npcData) {
        const choices = [];

        if (npcData.quests) {
            npcData.quests.slice(0, 3).forEach(questId => {
                choices.push({
                    text: `Quest: ${this.formatQuestName(questId)}`,
                    action: 'accept_quest',
                    questId: questId
                });
            });
        }

        choices.push({ text: 'Vielleicht spaeter', action: 'back' });

        return choices;
    }

    formatQuestName(questId) {
        return questId
            .replace(/_/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase());
    }

    // =========================================================================
    // NAJIKA REACTIONS
    // =========================================================================

    getNajikaReaction(npcData, context) {
        // Check for specific reactions in NPC data
        if (npcData.najika_reaction) {
            const reaction = npcData.najika_reaction[this.activePersonality];
            if (reaction) return reaction;

            // Check context-specific
            const contextKey = `on_${context}`;
            if (npcData.najika_reaction[contextKey]) {
                return npcData.najika_reaction[contextKey];
            }
        }

        // Generic reactions based on personality and NPC type
        return this.getGenericNajikaReaction(npcData, context);
    }

    getGenericNajikaReaction(npcData, context) {
        const reactions = {
            megumin: {
                greeting: [
                    '*aufgeregt* Ein neuer Freund, Mr. K!',
                    'Ob der mir EXPLOSION beibringen kann?!',
                    '*Augen leuchten* Spannend!'
                ],
                shop: [
                    'Haben die EXPLOSIONS-Zubehoer?!',
                    '*schaut sich um* Ooh, shiny!',
                    'Mr. K, kauf mir was!'
                ],
                quest: [
                    'Ein ABENTEUER! ENDLICH!',
                    '*huepft aufgeregt* Quest! Quest! Quest!',
                    'Kann ich dabei Sachen EXPLODIEREN lassen?!'
                ],
                food_vendor: [
                    '*sabbert* FLEISCH! ICH WILL AUCH!',
                    'Das riecht SO GUT!',
                    'Mr. K! Hunger!'
                ]
            },
            harley: {
                greeting: [
                    '*grinst* Ooh, interessant~',
                    'Let the games begin!',
                    '*kichert* Neue Spielkameraden!'
                ],
                shop: [
                    'Got anything... explosive?',
                    '*prueft Waren* Boring, boring... THAT one!',
                    'Mr. K, I want the shiny one!'
                ],
                quest: [
                    'Chaos-Mission? Count me IN!',
                    '*evil grin* Time to cause some mayhem~',
                    'Sounds like FUN!'
                ],
                food_vendor: [
                    '*stibitzt was* Oops!',
                    'Got any candy?',
                    'MEAT! Harley like!'
                ]
            },
            shiro: {
                greeting: [
                    '*analysiert* NPC Typ erkannt. Bedrohungsstufe: Niedrig.',
                    'Daten werden gesammelt...',
                    '*nickt* Akzeptabel.'
                ],
                shop: [
                    '*berechnet* Preis-Leistungs-Verhaeltnis: Suboptimal.',
                    'Item-Statistiken werden analysiert...',
                    'Effizienz: 73.2%'
                ],
                quest: [
                    '*kalkuliert* Erfolgswahrscheinlichkeit: 87.3%',
                    'Quest-Parameter akzeptabel.',
                    'Belohnung-zu-Risiko-Ratio: Positiv.'
                ],
                food_vendor: [
                    '*analysiert* Kalorien: Ausreichend. Geschmack: Irrelevant.',
                    'Nahrungsaufnahme empfohlen.',
                    'HP-Regeneration: Effizient.'
                ]
            },
            melissa: {
                greeting: [
                    '*laechelt sanft* Wie schoen, neue Leute zu treffen.',
                    '*beobachtet still* Interessant...',
                    'Guten Tag.'
                ],
                shop: [
                    '*schaut sich um* So viele Geschichten hinter diesen Dingen...',
                    'Jedes Item hat eine Vergangenheit.',
                    '*nickt anerkennend* Gute Qualitaet.'
                ],
                quest: [
                    '*nachdenklich* Ob wir helfen koennen?',
                    'Jede Quest hat ihren Sinn.',
                    '*laechelt* Lass uns Gutes tun.'
                ],
                food_vendor: [
                    '*schnuppert* Riecht nach Heimat.',
                    'Gemeinsames Essen verbindet.',
                    '*dankbar* Wie freundlich.'
                ]
            }
        };

        const personalityReactions = reactions[this.activePersonality] || reactions.megumin;

        // Check NPC type specific
        if (npcData.type === 'food_vendor' && personalityReactions.food_vendor) {
            const r = personalityReactions.food_vendor;
            return r[Math.floor(Math.random() * r.length)];
        }

        // Context specific
        const contextReactions = personalityReactions[context];
        if (contextReactions) {
            return contextReactions[Math.floor(Math.random() * contextReactions.length)];
        }

        return null;
    }

    getNajikaReactionForRumor() {
        const rumors = {
            megumin: '*Ohren spitzen* Geheime Schatz-Hoehlen?! Mit EXPLOSIONEN?!',
            harley: '*grinst* Secrets, secrets! I LOVE secrets!',
            shiro: '*speichert* Information archiviert. Relevanz: Hoch.',
            melissa: '*interessiert* Jedes Geruecht hat einen wahren Kern...'
        };
        return rumors[this.activePersonality] || rumors.megumin;
    }

    // =========================================================================
    // CHOICE HANDLING
    // =========================================================================

    selectChoice(choice) {
        console.log(`[DIALOGUE] Choice selected: ${choice.action}`);

        switch (choice.action) {
            case 'close':
                this.closeDialogue();
                break;

            case 'back':
                // Zurueck zum Start
                const greeting = this.getRandomGreeting(this.currentNPC);
                this.showDialogueNode({
                    text: greeting,
                    choices: this.buildInitialChoices(this.currentNPC)
                });
                break;

            case 'open_shop':
            case 'open_shop_ui':
                this.openShop();
                break;

            case 'accept_quest':
                this.acceptQuest(choice.questId);
                break;

            case 'confirm_rest':
                this.useService('rest');
                break;

            default:
                // Navigate to next node
                if (choice.nextNode) {
                    this.dialogueHistory.push(this.currentDialogue);
                    this.currentDialogue = choice.nextNode;
                    this.showDialogueNode(choice.nextNode);
                }
                break;
        }
    }

    // =========================================================================
    // ACTIONS
    // =========================================================================

    openShop() {
        if (!this.currentNPC || !this.currentNPC.shop) return;

        console.log(`[DIALOGUE] Opening shop: ${this.currentNPC.name}`);

        // Trigger custom callback or use built-in
        if (this.onShopOpen) {
            this.onShopOpen(this.currentNPC);
        } else {
            this.showShopUI(this.currentNPC);
        }
    }

    showShopUI(npcData) {
        const shop = npcData.shop;

        // Create Shop Modal
        const shopModal = document.createElement('div');
        shopModal.id = 'shop-modal';
        shopModal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 10001;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        const shopContent = document.createElement('div');
        shopContent.style.cssText = `
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border: 3px solid #FFD700;
            border-radius: 15px;
            padding: 25px;
            max-width: 700px;
            max-height: 80vh;
            overflow-y: auto;
            color: #fff;
        `;

        // Shop Items
        const itemsHTML = (shop.items || []).map(item => `
            <div class="shop-item" style="
                background: rgba(255,255,255,0.05);
                border: 2px solid rgba(255,215,0,0.3);
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.2s;
                cursor: pointer;
            " onmouseover="this.style.borderColor='#FFD700'" onmouseout="this.style.borderColor='rgba(255,215,0,0.3)'">
                <div>
                    <div style="font-weight: bold; font-size: 16px;">${this.formatItemName(item.id)}</div>
                    ${item.damage ? `<div style="color: #f44336; font-size: 12px;">Schaden: ${item.damage}</div>` : ''}
                    ${item.defense ? `<div style="color: #4CAF50; font-size: 12px;">Verteidigung: ${item.defense}</div>` : ''}
                    ${item.special ? `<div style="color: #9C27B0; font-size: 12px;">Spezial: ${item.special}</div>` : ''}
                    ${item.stock ? `<div style="color: #888; font-size: 11px;">Vorrat: ${item.stock}</div>` : ''}
                </div>
                <div style="text-align: right;">
                    <div style="color: #FFD700; font-weight: bold; font-size: 18px;">${item.price}g</div>
                    <button onclick="window.npcDialogueSystem.buyItem('${item.id}', ${item.price})" style="
                        background: #4CAF50;
                        color: #fff;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-top: 5px;
                    ">Kaufen</button>
                </div>
            </div>
        `).join('');

        shopContent.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="color: #FFD700; margin: 0;">${npcData.name}'s Shop</h2>
                <button onclick="document.getElementById('shop-modal').remove()" style="
                    background: #f44336;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                ">Schliessen X</button>
            </div>
            <div style="margin-bottom: 15px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 8px;">
                Dein Gold: <span id="shop-gold" style="color: #FFD700; font-weight: bold;">???</span>
            </div>
            <div id="shop-items">${itemsHTML}</div>
        `;

        shopModal.appendChild(shopContent);
        document.body.appendChild(shopModal);

        // Load player gold
        this.loadPlayerGold();

        // Close on outside click
        shopModal.addEventListener('click', (e) => {
            if (e.target === shopModal) shopModal.remove();
        });
    }

    formatItemName(itemId) {
        return itemId
            .replace(/_/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase());
    }

    async loadPlayerGold() {
        try {
            const response = await fetch('http://localhost:8000/api/player/gold');
            const data = await response.json();
            const goldEl = document.getElementById('shop-gold');
            if (goldEl) goldEl.textContent = data.gold || 1000;
        } catch (err) {
            const goldEl = document.getElementById('shop-gold');
            if (goldEl) goldEl.textContent = '1000 (Offline)';
        }
    }

    async buyItem(itemId, price) {
        console.log(`[SHOP] Buying: ${itemId} for ${price}g`);

        try {
            const response = await fetch('http://localhost:8000/api/shop/buy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: 'kuja',
                    item_id: itemId,
                    price: price
                })
            });

            const data = await response.json();

            if (data.success) {
                // Najika Reaction
                this.showBuyReaction(itemId);
                this.loadPlayerGold();
                this.showPurchaseNotification(itemId, price, true);

                // GameEvent
                if (window.GameEvents) {
                    window.GameEvents.emit('itemPurchased', { itemId, price, npcId: this.currentNPC?.id });
                    window.GameEvents.emit('itemCollected', { itemId, quantity: 1, source: 'shop' });
                }

                // Frontend-Inventar synchronisieren
                if (window.inventorySystem) {
                    window.inventorySystem.addItem(itemId, 1);
                }
            } else {
                this.showPurchaseNotification(itemId, price, false, data.error || 'Nicht genug Gold!');
            }
        } catch (err) {
            // Offline Mode
            this.showBuyReaction(itemId);
            this.showPurchaseNotification(itemId, price, true, 'Offline-Modus');

            if (window.inventorySystem) {
                window.inventorySystem.addItem(itemId, 1);
            }
            if (window.GameEvents) {
                window.GameEvents.emit('itemCollected', { itemId, quantity: 1, source: 'shop_offline' });
            }
        }
    }

    showPurchaseNotification(itemId, price, success, extraMsg) {
        const notif = document.createElement('div');
        notif.style.cssText = `
            position: fixed; top: 20px; right: 20px;
            background: ${success ? 'rgba(0,100,0,0.9)' : 'rgba(150,0,0,0.9)'};
            color: #fff; padding: 12px 20px; border-radius: 10px; z-index: 5000;
            border: 2px solid ${success ? '#00ff00' : '#ff4444'}; font-family: Arial;
            animation: fadeInDown 0.3s ease; min-width: 200px;
        `;
        const itemName = this.formatItemName ? this.formatItemName(itemId) : itemId;
        notif.innerHTML = success
            ? `<div style="font-weight:bold;">✅ ${itemName} gekauft!</div><div style="font-size:12px; color:#aaffaa;">-${price} Gold ${extraMsg ? '(' + extraMsg + ')' : ''}</div>`
            : `<div style="font-weight:bold;">❌ Kauf fehlgeschlagen</div><div style="font-size:12px; color:#ffaaaa;">${extraMsg || ''}</div>`;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 3000);
    }

    showBuyReaction(itemId) {
        const reactions = {
            megumin: `YEAH! ${this.formatItemName(itemId)}! *huepft aufgeregt*`,
            harley: `Ooh shiny! ${this.formatItemName(itemId)}! *grabby hands*`,
            shiro: `Kauf registriert. Item: ${this.formatItemName(itemId)}. Effektiv.`,
            melissa: `*laechelt* Eine gute Wahl, Mr. K.`
        };

        // Show temporary reaction
        const reactionEl = document.getElementById('najika-reaction');
        const reactionTextEl = document.getElementById('najika-reaction-text');

        if (reactionEl && reactionTextEl) {
            reactionEl.style.display = 'block';
            reactionTextEl.textContent = reactions[this.activePersonality] || reactions.megumin;

            setTimeout(() => {
                reactionEl.style.display = 'none';
            }, 3000);
        }
    }

    acceptQuest(questId) {
        console.log(`[DIALOGUE] Quest accepted: ${questId}`);

        if (this.onQuestAccept) {
            this.onQuestAccept(questId, this.currentNPC);
        }

        // Show acceptance dialogue
        const acceptDialogues = this.currentNPC.dialogues?.quest_complete ||
            'Gut! Ich zaehle auf dich!';

        this.showDialogueNode({
            text: Array.isArray(acceptDialogues)
                ? acceptDialogues[Math.floor(Math.random() * acceptDialogues.length)]
                : acceptDialogues,
            choices: [{ text: 'Ich werde es erledigen!', action: 'close' }],
            najikaReaction: this.getQuestAcceptReaction(questId)
        });
    }

    getQuestAcceptReaction(questId) {
        const reactions = {
            megumin: `QUEST ANGENOMMEN! Zeit fuer EXPLOSION und ABENTEUER!`,
            harley: `*evil grin* Quest time! Let's cause some CHAOS!`,
            shiro: `Quest akzeptiert. Optimaler Pfad wird berechnet...`,
            melissa: `*nickt* Wir werden unser Bestes tun.`
        };
        return reactions[this.activePersonality] || reactions.megumin;
    }

    async useService(serviceType) {
        const service = this.currentNPC?.services?.[serviceType];
        if (!service) return;

        console.log(`[DIALOGUE] Using service: ${serviceType}`);

        try {
            const response = await fetch('http://localhost:8000/api/service/use', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: 'kuja',
                    service: serviceType,
                    npc_id: this.currentNPC.id,
                    price: service.price
                })
            });

            const data = await response.json();

            if (data.success) {
                this.showServiceCompleteDialogue(serviceType);
            } else {
                alert(`Fehler: ${data.error || 'Nicht genug Gold!'}`);
            }
        } catch (err) {
            // Offline mode
            this.showServiceCompleteDialogue(serviceType);
        }
    }

    showServiceCompleteDialogue(serviceType) {
        const dialogues = {
            rest: {
                text: this.currentNPC.dialogues?.heal_full || 'Du bist vollstaendig erholt!',
                najikaReaction: {
                    megumin: '*gaehnt* Schlafen ist gut fuer EXPLOSION-Power!',
                    harley: '*kuschelt sich ein* Sleepy time~',
                    shiro: 'HP/MP vollstaendig regeneriert. Effizienz: 100%.',
                    melissa: '*laechelt* Suesse Traeume, Mr. K.'
                }
            },
            repair: {
                text: 'Deine Ausruestung ist repariert!',
                najikaReaction: {
                    megumin: '*prueft Stab* Bereit fuer EXPLOSION!',
                    harley: '*schwingt Waffe* Good as new!',
                    shiro: 'Equipment-Haltbarkeit: 100%. Optimal.',
                    melissa: '*nickt* Gut gepflegte Ausruestung ist wichtig.'
                }
            }
        };

        const dialogue = dialogues[serviceType] || { text: 'Service abgeschlossen!' };

        this.showDialogueNode({
            text: dialogue.text,
            choices: [{ text: 'Danke!', action: 'back' }],
            najikaReaction: dialogue.najikaReaction?.[this.activePersonality]
        });
    }

    showQuests() {
        // Navigate to quest selection
        this.showDialogueNode({
            text: this.getQuestDialogue(this.currentNPC),
            choices: this.buildQuestChoices(this.currentNPC),
            najikaReaction: this.getNajikaReaction(this.currentNPC, 'quest')
        });
    }

    // =========================================================================
    // CLOSE
    // =========================================================================

    closeDialogue() {
        this.dialogueUI.style.display = 'none';
        this.currentNPC = null;
        this.currentDialogue = null;
        this.dialogueHistory = [];

        // Remove choice handler
        if (this._choiceHandler) {
            document.removeEventListener('keydown', this._choiceHandler);
        }

        // Close any open shop modals
        const shopModal = document.getElementById('shop-modal');
        if (shopModal) shopModal.remove();

        console.log('[DIALOGUE] Dialogue closed');
    }
}

// =========================================================================
// GLOBAL INSTANCE
// =========================================================================

window.npcDialogueSystem = new NPCDialogueSystem();

// Integration mit NPC Interaction System
if (window.NPCInteractionSystem) {
    const originalOpenDialog = window.NPCInteractionSystem.prototype.openDialog;
    window.NPCInteractionSystem.prototype.openDialog = function(npc) {
        const npcId = npc.userData.npcId || npc.userData.npcName;
        if (window.npcDialogueSystem.startDialogue(npcId)) {
            return; // Neues System uebernimmt
        }
        // Fallback zum alten System
        originalOpenDialog.call(this, npc);
    };
}

console.log('[DIALOGUE] NPC Dialogue Tree System loaded!');
