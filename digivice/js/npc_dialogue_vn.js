/**
 * NPC Dialogue Visual Novel UI - Najika World
 * =============================================
 * Visual Novel Style Dialog-System:
 * - Character Portraits (links/rechts)
 * - Typewriter Text-Effekt mit Skip
 * - Branching Choices mit Konsequenzen-Preview
 * - Emotion System (NPC Gesichtsausdruecke)
 * - Dialogue History (Scroll-Back)
 * - Affinity-Anzeige bei Gespraechsende
 * - Choice-Memory (erinnert sich an Entscheidungen)
 * - Auto-Mode + Skip-Mode
 *
 * Ergaenzt npc_dialogue_system.js mit VN-Layer.
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

(function() {
    'use strict';

    // ==========================================
    // NPC DATABASE
    // ==========================================

    const NPC_PORTRAITS = {
        // Hauptcharaktere
        najika: {
            name: 'Najika',
            defaultEmotion: 'neutral',
            color: '#E91E63',
            emotions: {
                neutral:  '\uD83D\uDE10', happy: '\uD83D\uDE0A', angry: '\uD83D\uDE20',
                sad:      '\uD83D\uDE22', surprised: '\uD83D\uDE32', embarrassed: '\uD83D\uDE33',
                love:     '\uD83D\uDE0D', mischievous: '\uD83D\uDE0F', thinking: '\uD83E\uDD14',
                excited:  '\uD83E\uDD29'
            }
        },
        haendler_zan: {
            name: 'Zan der Haendler',
            defaultEmotion: 'neutral',
            color: '#FF9800',
            emotions: {
                neutral: '\uD83D\uDE10', happy: '\uD83D\uDE04', greedy: '\uD83E\uDD11',
                suspicious: '\uD83E\uDD28', impressed: '\uD83D\uDE2E'
            }
        },
        schmiedin_hilda: {
            name: 'Schmiedin Hilda',
            defaultEmotion: 'neutral',
            color: '#FF5722',
            emotions: {
                neutral: '\uD83D\uDE10', happy: '\uD83D\uDE0A', angry: '\uD83D\uDE24',
                proud: '\uD83D\uDE0E', working: '\uD83E\uDD14'
            }
        },
        hexe_moira: {
            name: 'Hexe Moira',
            defaultEmotion: 'neutral',
            color: '#9C27B0',
            emotions: {
                neutral: '\uD83D\uDE10', mysterious: '\uD83D\uDE0F', cackling: '\uD83D\uDE06',
                dark: '\uD83D\uDE08', wise: '\uD83E\uDDD0'
            }
        },
        ritter_alaric: {
            name: 'Ritter Alaric',
            defaultEmotion: 'neutral',
            color: '#2196F3',
            emotions: {
                neutral: '\uD83D\uDE10', brave: '\uD83D\uDE24', sad: '\uD83D\uDE1E',
                angry: '\uD83D\uDE21', respectful: '\uD83D\uDE07'
            }
        },
        waldgeist_fenn: {
            name: 'Waldgeist Fenn',
            defaultEmotion: 'neutral',
            color: '#4CAF50',
            emotions: {
                neutral: '\uD83D\uDE10', playful: '\uD83D\uDE1C', scared: '\uD83D\uDE28',
                peaceful: '\uD83D\uDE0C', curious: '\uD83E\uDD14'
            }
        },
        pirat_costa: {
            name: 'Kapitaen Costa',
            defaultEmotion: 'neutral',
            color: '#00BCD4',
            emotions: {
                neutral: '\uD83D\uDE10', laughing: '\uD83D\uDE02', drunk: '\uD83E\uDD2A',
                serious: '\uD83D\uDE11', adventurous: '\uD83E\uDD29'
            }
        },
        schleim: {
            name: 'Schleim',
            defaultEmotion: 'happy',
            color: '#8BC34A',
            emotions: {
                happy: '\uD83D\uDE0A', excited: '\uD83E\uDD29', scared: '\uD83D\uDE30',
                sleepy: '\uD83D\uDE34', love: '\uD83D\uDE0D', confused: '\uD83D\uDE15'
            }
        }
    };

    // ==========================================
    // STATE
    // ==========================================

    let vnState = {
        isOpen: false,
        container: null,
        currentNpcId: null,
        currentDialogue: null,
        currentNodeId: null,
        dialogueHistory: [],
        choiceMemory: {},      // dialogueId -> chosen option index
        typewriterTimer: null,
        typewriterText: '',
        typewriterIndex: 0,
        typewriterDone: false,
        autoMode: false,
        skipMode: false,
        leftSpeaker: null,     // npcId
        rightSpeaker: null,    // npcId
        activeSpeaker: 'left', // which side is talking
        affinityChange: 0      // accumulated during conversation
    };

    // Load choice memory
    try {
        const saved = JSON.parse(localStorage.getItem('najika_vn_choices'));
        if (saved) vnState.choiceMemory = saved;
    } catch(e) { /* default */ }

    function saveChoices() {
        try {
            localStorage.setItem('najika_vn_choices', JSON.stringify(vnState.choiceMemory));
        } catch(e) { /* silent */ }
    }

    // ==========================================
    // DIALOGUE DATA FORMAT
    // ==========================================
    // Dialogues are trees:
    // {
    //   id: 'talk_zan_01',
    //   startNode: 'intro',
    //   nodes: {
    //     intro: { speaker: 'haendler_zan', emotion: 'happy', text: '...', next: 'choice1' },
    //     choice1: { type: 'choice', choices: [
    //       { text: 'Option A', next: 'node_a', affinity: +5, preview: 'Freundlich' },
    //       { text: 'Option B', next: 'node_b', affinity: -3, preview: 'Unhöflich' }
    //     ]},
    //     node_a: { speaker: 'haendler_zan', emotion: 'impressed', text: '...', next: null }
    //   }
    // }

    // Sample dialogues
    const SAMPLE_DIALOGUES = {
        talk_zan_01: {
            id: 'talk_zan_01',
            startNode: 'intro',
            nodes: {
                intro: {
                    speaker: 'haendler_zan', emotion: 'happy',
                    text: 'Ah, ein neuer Kunde! Willkommen in meinem bescheidenen Laden. Ich habe heute ganz besondere Waren...',
                    next: 'choice1'
                },
                choice1: {
                    type: 'choice',
                    choices: [
                        { text: 'Zeig mir deine besten Waren!', next: 'eager', affinity: 3, preview: 'Begeistert' },
                        { text: 'Ich schau nur.', next: 'browse', affinity: 0, preview: 'Neutral' },
                        { text: 'Deine Preise sind Wucher!', next: 'rude', affinity: -5, preview: 'Konfrontativ' }
                    ]
                },
                eager: {
                    speaker: 'haendler_zan', emotion: 'greedy',
                    text: 'Ein Kenner! Komm, ich zeige dir etwas Besonderes aus dem Hinterzimmer...',
                    next: 'offer'
                },
                browse: {
                    speaker: 'haendler_zan', emotion: 'neutral',
                    text: 'Natuerlich, nimm dir Zeit. Aber fass nichts an, was du nicht kaufen willst!',
                    next: null
                },
                rude: {
                    speaker: 'haendler_zan', emotion: 'suspicious',
                    text: 'Wucher?! Das sind FAIRE Preise fuer SELTENE Waren! Vielleicht bist du einfach zu arm.',
                    next: 'choice2'
                },
                choice2: {
                    type: 'choice',
                    choices: [
                        { text: 'Entschuldigung, das war unhöflich.', next: 'apologize', affinity: 2, preview: 'Entschuldigung' },
                        { text: '*Gehen*', next: null, affinity: -3, preview: 'Abgang' }
                    ]
                },
                apologize: {
                    speaker: 'haendler_zan', emotion: 'happy',
                    text: 'Na gut, ich vergebe dir. Hier, als Friedensangebot - 10% Rabatt auf deinen naechsten Einkauf!',
                    next: null
                },
                offer: {
                    speaker: 'haendler_zan', emotion: 'impressed',
                    text: 'Ein magischer Kompass, der zu verborgenen Schaetzen fuehrt! Nur 500 Gold, ein Schnaeppchen!',
                    next: null
                }
            }
        }
    };

    // ==========================================
    // VN UI CREATION
    // ==========================================

    function openDialogue(npcId, dialogueId) {
        if (vnState.isOpen) closeDialogue();

        const dialogue = SAMPLE_DIALOGUES[dialogueId];
        if (!dialogue) {
            console.warn(`[VN] Dialogue not found: ${dialogueId}`);
            return;
        }

        vnState.isOpen = true;
        vnState.currentNpcId = npcId;
        vnState.currentDialogue = dialogue;
        vnState.currentNodeId = dialogue.startNode;
        vnState.dialogueHistory = [];
        vnState.affinityChange = 0;
        vnState.autoMode = false;
        vnState.skipMode = false;
        vnState.leftSpeaker = npcId;
        vnState.rightSpeaker = 'najika';

        createVNContainer();
        renderCurrentNode();
    }

    function createVNContainer() {
        const existing = document.getElementById('vn-dialogue-container');
        if (existing) existing.remove();

        const container = document.createElement('div');
        container.id = 'vn-dialogue-container';
        container.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            z-index:10500;
            font-family:'Courier New',monospace;
            cursor:pointer;
        `;

        // Background overlay (darkened)
        container.innerHTML = `
            <div id="vn-bg" style="position:absolute;top:0;left:0;width:100%;height:100%;
                background:rgba(0,0,0,0.6);"></div>

            <!-- Portrait Left -->
            <div id="vn-portrait-left" style="position:absolute;bottom:180px;left:40px;
                text-align:center;transition:all 0.3s ease;opacity:0.4;
                transform:scale(0.9);"></div>

            <!-- Portrait Right -->
            <div id="vn-portrait-right" style="position:absolute;bottom:180px;right:40px;
                text-align:center;transition:all 0.3s ease;opacity:0.4;
                transform:scale(0.9);"></div>

            <!-- Text Box -->
            <div id="vn-textbox" style="position:absolute;bottom:0;left:0;width:100%;
                background:linear-gradient(0deg, rgba(5,5,15,0.98), rgba(10,10,25,0.95));
                border-top:2px solid rgba(255,255,255,0.1);
                padding:20px 30px 24px;min-height:160px;">

                <!-- Speaker Name -->
                <div id="vn-speaker" style="position:absolute;top:-14px;left:30px;
                    background:rgba(10,10,25,0.95);border:1px solid rgba(255,255,255,0.15);
                    border-radius:4px;padding:4px 14px;font-size:12px;
                    font-weight:bold;color:white;"></div>

                <!-- Text Area -->
                <div id="vn-text" style="color:rgba(255,255,255,0.9);font-size:14px;
                    line-height:1.8;padding-top:10px;min-height:60px;
                    max-width:800px;"></div>

                <!-- Choice Area (hidden by default) -->
                <div id="vn-choices" style="display:none;padding-top:10px;
                    max-width:700px;"></div>

                <!-- Controls -->
                <div style="position:absolute;bottom:8px;right:16px;display:flex;gap:8px;">
                    <button id="vn-btn-auto" onclick="window.NPCDialogueVN._toggleAuto()"
                        style="padding:4px 10px;font-size:8px;font-family:inherit;
                        background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                        color:rgba(255,255,255,0.3);border-radius:3px;cursor:pointer;">AUTO</button>
                    <button id="vn-btn-skip" onclick="window.NPCDialogueVN._toggleSkip()"
                        style="padding:4px 10px;font-size:8px;font-family:inherit;
                        background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                        color:rgba(255,255,255,0.3);border-radius:3px;cursor:pointer;">SKIP</button>
                    <button id="vn-btn-log" onclick="window.NPCDialogueVN._showHistory()"
                        style="padding:4px 10px;font-size:8px;font-family:inherit;
                        background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                        color:rgba(255,255,255,0.3);border-radius:3px;cursor:pointer;">LOG</button>
                </div>

                <!-- Click indicator -->
                <div id="vn-click-indicator" style="position:absolute;bottom:8px;left:50%;
                    transform:translateX(-50%);font-size:8px;
                    color:rgba(255,255,255,0.15);display:none;">
                    Klicken zum Fortfahren \u25BC
                </div>
            </div>
        `;

        // Click to advance
        container.addEventListener('click', (e) => {
            // Don't advance if clicking buttons or choices
            if (e.target.tagName === 'BUTTON' || e.target.closest('#vn-choices')) return;
            advanceDialogue();
        });

        // Keyboard
        vnState._keyHandler = (e) => {
            if (e.key === 'Escape') closeDialogue();
            if (e.key === ' ' || e.key === 'Enter') advanceDialogue();
        };
        document.addEventListener('keydown', vnState._keyHandler);

        document.body.appendChild(container);
        vnState.container = container;
    }

    // ==========================================
    // RENDER NODE
    // ==========================================

    function renderCurrentNode() {
        const node = vnState.currentDialogue.nodes[vnState.currentNodeId];
        if (!node) {
            closeDialogue();
            return;
        }

        if (node.type === 'choice') {
            renderChoices(node);
        } else {
            renderTextNode(node);
        }
    }

    function renderTextNode(node) {
        const npc = NPC_PORTRAITS[node.speaker] || NPC_PORTRAITS.najika;
        const emotion = node.emotion || npc.defaultEmotion;
        const emotionIcon = npc.emotions[emotion] || npc.emotions[npc.defaultEmotion] || '\uD83D\uDE10';

        // Update speaker name
        const speakerEl = document.getElementById('vn-speaker');
        if (speakerEl) {
            speakerEl.textContent = npc.name;
            speakerEl.style.borderColor = npc.color + '66';
            speakerEl.style.color = npc.color;
        }

        // Update portraits
        const isLeft = node.speaker === vnState.leftSpeaker;
        updatePortrait('left', vnState.leftSpeaker,
            node.speaker === vnState.leftSpeaker ? emotionIcon : null,
            node.speaker === vnState.leftSpeaker);
        updatePortrait('right', vnState.rightSpeaker,
            node.speaker === vnState.rightSpeaker ? emotionIcon : null,
            node.speaker === vnState.rightSpeaker);

        // Hide choices
        const choicesEl = document.getElementById('vn-choices');
        if (choicesEl) choicesEl.style.display = 'none';

        // Show click indicator
        const indicator = document.getElementById('vn-click-indicator');
        if (indicator) indicator.style.display = 'none';

        // Typewriter effect
        startTypewriter(node.text, () => {
            if (indicator) indicator.style.display = 'block';

            // Add to history
            vnState.dialogueHistory.push({
                speaker: npc.name,
                text: node.text,
                emotion: emotionIcon
            });

            // Auto mode
            if (vnState.autoMode) {
                setTimeout(() => advanceDialogue(), 2000);
            }
        });
    }

    function renderChoices(node) {
        const choicesEl = document.getElementById('vn-choices');
        if (!choicesEl) return;

        // Hide click indicator
        const indicator = document.getElementById('vn-click-indicator');
        if (indicator) indicator.style.display = 'none';

        // Check if already made this choice
        const dialogueKey = `${vnState.currentDialogue.id}_${vnState.currentNodeId}`;
        const previousChoice = vnState.choiceMemory[dialogueKey];

        choicesEl.style.display = 'block';
        choicesEl.innerHTML = node.choices.map((choice, idx) => {
            const wasPrevious = previousChoice === idx;
            const affinityColor = choice.affinity > 0 ? '#4CAF50' :
                                 choice.affinity < 0 ? '#FF4444' : 'rgba(255,255,255,0.3)';
            const affinityText = choice.affinity > 0 ? `+${choice.affinity}` :
                                choice.affinity < 0 ? `${choice.affinity}` : '';

            return `
                <button onclick="window.NPCDialogueVN._choose(${idx})"
                    style="display:block;width:100%;text-align:left;
                    padding:10px 16px;margin-bottom:6px;
                    background:${wasPrevious ? 'rgba(233,30,99,0.08)' : 'rgba(255,255,255,0.03)'};
                    border:1px solid ${wasPrevious ? 'rgba(233,30,99,0.2)' : 'rgba(255,255,255,0.08)'};
                    border-radius:6px;cursor:pointer;font-family:inherit;
                    color:white;font-size:12px;
                    transition:all 0.15s;"
                    onmouseover="this.style.background='rgba(255,255,255,0.06)';this.style.borderColor='rgba(255,255,255,0.2)'"
                    onmouseout="this.style.background='${wasPrevious ? 'rgba(233,30,99,0.08)' : 'rgba(255,255,255,0.03)'}';this.style.borderColor='${wasPrevious ? 'rgba(233,30,99,0.2)' : 'rgba(255,255,255,0.08)'}'"
                >
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span>
                            <span style="color:rgba(255,255,255,0.3);margin-right:8px;">${idx + 1}.</span>
                            ${choice.text}
                        </span>
                        <span style="display:flex;gap:8px;align-items:center;">
                            ${choice.preview ? `<span style="font-size:9px;color:rgba(255,255,255,0.3);
                                padding:2px 6px;background:rgba(255,255,255,0.04);
                                border-radius:3px;">${choice.preview}</span>` : ''}
                            ${affinityText ? `<span style="font-size:9px;color:${affinityColor};
                                font-weight:bold;">${affinityText} \u2764</span>` : ''}
                        </span>
                    </div>
                    ${wasPrevious ? `<div style="font-size:8px;color:rgba(233,30,99,0.5);
                        margin-top:4px;">Letzte Wahl</div>` : ''}
                </button>
            `;
        }).join('');

        // Keyboard shortcuts for choices (1, 2, 3...)
        vnState._choiceKeyHandler = (e) => {
            const num = parseInt(e.key);
            if (num >= 1 && num <= node.choices.length) {
                makeChoice(num - 1, node);
            }
        };
        document.addEventListener('keydown', vnState._choiceKeyHandler);
    }

    // ==========================================
    // PORTRAITS
    // ==========================================

    function updatePortrait(side, npcId, emotionIcon, isActive) {
        const el = document.getElementById(`vn-portrait-${side}`);
        if (!el) return;

        const npc = NPC_PORTRAITS[npcId];
        if (!npc) { el.innerHTML = ''; return; }

        const icon = emotionIcon || npc.emotions[npc.defaultEmotion] || '\uD83D\uDE10';

        el.style.opacity = isActive ? '1' : '0.3';
        el.style.transform = isActive ? 'scale(1)' : 'scale(0.9)';
        el.style.filter = isActive ? 'none' : 'brightness(0.5)';

        el.innerHTML = `
            <div style="font-size:64px;margin-bottom:6px;
                transition:transform 0.3s ease;
                ${isActive ? 'transform:scale(1.05);' : ''}">${icon}</div>
            <div style="font-size:10px;color:${isActive ? npc.color : 'rgba(255,255,255,0.3)'};
                font-weight:bold;">${npc.name}</div>
        `;
    }

    // ==========================================
    // TYPEWRITER EFFECT
    // ==========================================

    function startTypewriter(text, onComplete) {
        if (vnState.typewriterTimer) clearInterval(vnState.typewriterTimer);

        vnState.typewriterText = text;
        vnState.typewriterIndex = 0;
        vnState.typewriterDone = false;

        const textEl = document.getElementById('vn-text');
        if (!textEl) return;

        if (vnState.skipMode) {
            textEl.textContent = text;
            vnState.typewriterDone = true;
            if (onComplete) onComplete();
            return;
        }

        const speed = 30; // ms per char

        vnState.typewriterTimer = setInterval(() => {
            vnState.typewriterIndex++;
            textEl.textContent = text.substring(0, vnState.typewriterIndex);

            if (vnState.typewriterIndex >= text.length) {
                clearInterval(vnState.typewriterTimer);
                vnState.typewriterDone = true;
                if (onComplete) onComplete();
            }
        }, speed);
    }

    function skipTypewriter() {
        if (vnState.typewriterTimer) {
            clearInterval(vnState.typewriterTimer);
        }
        const textEl = document.getElementById('vn-text');
        if (textEl) textEl.textContent = vnState.typewriterText;
        vnState.typewriterDone = true;
        vnState.typewriterIndex = vnState.typewriterText.length;

        const indicator = document.getElementById('vn-click-indicator');
        if (indicator) indicator.style.display = 'block';
    }

    // ==========================================
    // DIALOGUE FLOW
    // ==========================================

    function advanceDialogue() {
        // If typewriter is still running, skip it
        if (!vnState.typewriterDone) {
            skipTypewriter();
            return;
        }

        const node = vnState.currentDialogue.nodes[vnState.currentNodeId];
        if (!node) { closeDialogue(); return; }

        // Don't advance if it's a choice node
        if (node.type === 'choice') return;

        // Go to next node
        if (node.next) {
            vnState.currentNodeId = node.next;
            renderCurrentNode();
        } else {
            // End of dialogue
            closeDialogue();
        }
    }

    function makeChoice(choiceIdx, node) {
        if (!node || !node.choices) return;

        const choice = node.choices[choiceIdx];
        if (!choice) return;

        // Remove choice key handler
        if (vnState._choiceKeyHandler) {
            document.removeEventListener('keydown', vnState._choiceKeyHandler);
        }

        // Remember choice
        const dialogueKey = `${vnState.currentDialogue.id}_${vnState.currentNodeId}`;
        vnState.choiceMemory[dialogueKey] = choiceIdx;
        saveChoices();

        // Apply affinity
        if (choice.affinity) {
            vnState.affinityChange += choice.affinity;
        }

        // Add to history
        vnState.dialogueHistory.push({
            speaker: 'Spieler',
            text: choice.text,
            isChoice: true
        });

        // Go to next node
        if (choice.next) {
            vnState.currentNodeId = choice.next;
            renderCurrentNode();
        } else {
            closeDialogue();
        }
    }

    // ==========================================
    // DIALOGUE HISTORY
    // ==========================================

    function showHistory() {
        const existing = document.getElementById('vn-history-overlay');
        if (existing) { existing.remove(); return; }

        const overlay = document.createElement('div');
        overlay.id = 'vn-history-overlay';
        overlay.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.9);z-index:10600;
            overflow-y:auto;padding:40px;
            font-family:'Courier New',monospace;
        `;

        let html = `
            <div style="max-width:600px;margin:0 auto;">
                <div style="display:flex;justify-content:space-between;align-items:center;
                    margin-bottom:20px;">
                    <div style="font-size:14px;color:white;font-weight:bold;">
                        Gespraechsverlauf</div>
                    <button onclick="document.getElementById('vn-history-overlay').remove()"
                        style="padding:4px 12px;font-size:10px;font-family:inherit;
                        background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                        color:rgba(255,255,255,0.5);border-radius:4px;cursor:pointer;">
                        Schliessen</button>
                </div>
        `;

        vnState.dialogueHistory.forEach(entry => {
            const npc = Object.values(NPC_PORTRAITS).find(n => n.name === entry.speaker);
            const color = npc ? npc.color : 'rgba(255,255,255,0.5)';

            html += `
                <div style="margin-bottom:12px;padding:10px;
                    ${entry.isChoice ? 'padding-left:30px;border-left:2px solid rgba(233,30,99,0.3);' : ''}">
                    <div style="font-size:10px;color:${color};font-weight:bold;margin-bottom:4px;">
                        ${entry.emotion || ''} ${entry.speaker}
                        ${entry.isChoice ? '<span style="color:rgba(233,30,99,0.5);font-size:8px;"> (Wahl)</span>' : ''}
                    </div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.7);line-height:1.6;">
                        ${entry.text}
                    </div>
                </div>
            `;
        });

        html += `</div>`;
        overlay.innerHTML = html;
        document.body.appendChild(overlay);
    }

    // ==========================================
    // CLOSE + AFFINITY SUMMARY
    // ==========================================

    function closeDialogue() {
        if (vnState.typewriterTimer) clearInterval(vnState.typewriterTimer);
        if (vnState._keyHandler) document.removeEventListener('keydown', vnState._keyHandler);
        if (vnState._choiceKeyHandler) document.removeEventListener('keydown', vnState._choiceKeyHandler);

        // Show affinity change if any
        if (vnState.affinityChange !== 0 && vnState.currentNpcId) {
            const npc = NPC_PORTRAITS[vnState.currentNpcId];
            const color = vnState.affinityChange > 0 ? '#4CAF50' : '#FF4444';
            const sign = vnState.affinityChange > 0 ? '+' : '';

            if (window.QuestTrackerV2) {
                window.QuestTrackerV2.showNotification(
                    'ZUNEIGUNG',
                    `${npc ? npc.name : vnState.currentNpcId}: ${sign}${vnState.affinityChange} \u2764`,
                    color
                );
            }
        }

        vnState.isOpen = false;
        vnState.currentDialogue = null;
        vnState.currentNodeId = null;

        const container = document.getElementById('vn-dialogue-container');
        if (container) {
            container.style.transition = 'opacity 0.3s';
            container.style.opacity = '0';
            setTimeout(() => container.remove(), 300);
        }

        const history = document.getElementById('vn-history-overlay');
        if (history) history.remove();
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.NPCDialogueVN = {
        NPC_PORTRAITS,
        SAMPLE_DIALOGUES,
        open: openDialogue,
        close: closeDialogue,
        isOpen: () => vnState.isOpen,
        getChoiceMemory: () => ({ ...vnState.choiceMemory }),
        addDialogue: (id, data) => { SAMPLE_DIALOGUES[id] = data; },
        addNPC: (id, data) => { NPC_PORTRAITS[id] = data; },
        // Internal (for button onclick)
        _choose: (idx) => {
            const node = vnState.currentDialogue?.nodes[vnState.currentNodeId];
            if (node && node.type === 'choice') makeChoice(idx, node);
        },
        _toggleAuto: () => {
            vnState.autoMode = !vnState.autoMode;
            const btn = document.getElementById('vn-btn-auto');
            if (btn) {
                btn.style.color = vnState.autoMode ? '#4CAF50' : 'rgba(255,255,255,0.3)';
                btn.style.borderColor = vnState.autoMode ? 'rgba(76,175,80,0.3)' : 'rgba(255,255,255,0.1)';
            }
        },
        _toggleSkip: () => {
            vnState.skipMode = !vnState.skipMode;
            const btn = document.getElementById('vn-btn-skip');
            if (btn) {
                btn.style.color = vnState.skipMode ? '#FF9800' : 'rgba(255,255,255,0.3)';
                btn.style.borderColor = vnState.skipMode ? 'rgba(255,152,0,0.3)' : 'rgba(255,255,255,0.1)';
            }
        },
        _showHistory: showHistory
    };

    console.log(`[OK] NPC Dialogue VN geladen: ${Object.keys(NPC_PORTRAITS).length} NPCs, Visual Novel Style`);

})();
