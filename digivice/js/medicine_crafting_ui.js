/**
 * Medicine Crafting System UI - Najika World
 * ============================================
 * Echtes medizinisches Wissen als Fantasy-Kräuterkunde.
 * Real → Fantasy mapping (Kamille → Kristall-Kamille)
 *
 * Features:
 * - 64 Pflanzen in 4 Rarity-Stufen (Common, Uncommon, Rare, Legendary)
 * - Rezepte basieren auf echtem medizinischen Wissen
 * - 3 Tabs: Sammeln, Rezeptbuch, Crafting
 * - Region-basiertes Sammeln
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

class MedicineCraftingUI {
    constructor() {
        this.plants = this.initPlants();
        this.recipes = this.initRecipes();
        this.inventory = {};
        this.discoveredRecipes = new Set();
        this.currentTab = 'gather';
        this.currentRegion = 'wiese';
        this.isOpen = false;
        this.panel = null;

        this.init();
    }

    init() {
        this.createUI();
        this.loadState();
        console.log('[OK] Medicine Crafting UI geladen');
    }

    // ==========================================
    // PFLANZEN-DATENBANK (64 Pflanzen)
    // ==========================================

    initPlants() {
        return {
            // === COMMON (30) ===
            kamille: {
                fantasyName: 'Kristall-Kamille',
                realEffect: 'Beruhigend, entzuendungshemmend',
                rarity: 'common', icon: '🌼',
                regions: ['wiese', 'wald'], gatherChance: 0.8
            },
            pfefferminz: {
                fantasyName: 'Frost-Minze',
                realEffect: 'Kuehlend, schmerzlindernd',
                rarity: 'common', icon: '🌿',
                regions: ['berg', 'fluss'], gatherChance: 0.8
            },
            salbei: {
                fantasyName: 'Silber-Salbei',
                realEffect: 'Antibakteriell, entzuendungshemmend',
                rarity: 'common', icon: '🍃',
                regions: ['wiese', 'huegel'], gatherChance: 0.75
            },
            thymian: {
                fantasyName: 'Donnerkraut',
                realEffect: 'Schleimlösend, antiseptisch',
                rarity: 'common', icon: '🌱',
                regions: ['wiese', 'berg'], gatherChance: 0.8
            },
            brennnessel: {
                fantasyName: 'Flammen-Nessel',
                realEffect: 'Durchblutungsfoerdernd, eisenreich',
                rarity: 'common', icon: '🌿',
                regions: ['wald', 'sumpf'], gatherChance: 0.85
            },
            fenchel: {
                fantasyName: 'Windsaat-Fenchel',
                realEffect: 'Verdauungsfoerdernd, krampfloesend',
                rarity: 'common', icon: '🌾',
                regions: ['wiese', 'garten'], gatherChance: 0.8
            },
            ingwer: {
                fantasyName: 'Feuer-Wurzel',
                realEffect: 'Waermend, uebelkeitslindernd',
                rarity: 'common', icon: '🫚',
                regions: ['dschungel', 'sumpf'], gatherChance: 0.7
            },
            baldrian: {
                fantasyName: 'Schlummer-Baldrian',
                realEffect: 'Beruhigend, schlaffoerdernd',
                rarity: 'common', icon: '🌸',
                regions: ['wald', 'wiese'], gatherChance: 0.75
            },
            ringelblume: {
                fantasyName: 'Sonnen-Calendula',
                realEffect: 'Wundheilend, entzuendungshemmend',
                rarity: 'common', icon: '🌻',
                regions: ['wiese', 'garten'], gatherChance: 0.8
            },
            holunder: {
                fantasyName: 'Aether-Holunder',
                realEffect: 'Immunstaerkend, schweisstreibernd',
                rarity: 'common', icon: '🫐',
                regions: ['wald', 'huegel'], gatherChance: 0.75
            },
            loewenzahn: {
                fantasyName: 'Licht-Loewenzahn',
                realEffect: 'Harntreibend, leberstuetzend',
                rarity: 'common', icon: '🌼',
                regions: ['wiese', 'garten'], gatherChance: 0.85
            },
            spitzwegerich: {
                fantasyName: 'Klingen-Wegerich',
                realEffect: 'Hustenstillend, wundheilend',
                rarity: 'common', icon: '🍃',
                regions: ['wiese', 'weg'], gatherChance: 0.85
            },
            rosmarin: {
                fantasyName: 'Gedaechtnis-Kraut',
                realEffect: 'Konzentrationsfoerdernd, durchblutungsfoerdernd',
                rarity: 'common', icon: '🌿',
                regions: ['huegel', 'kueste'], gatherChance: 0.75
            },
            melisse: {
                fantasyName: 'Mond-Melisse',
                realEffect: 'Beruhigend, antivirale Wirkung',
                rarity: 'common', icon: '🍃',
                regions: ['garten', 'wald'], gatherChance: 0.8
            },
            schafgarbe: {
                fantasyName: 'Krieger-Schafgarbe',
                realEffect: 'Blutstillend, krampfloesend',
                rarity: 'common', icon: '🌸',
                regions: ['wiese', 'berg'], gatherChance: 0.75
            },
            kuemmel: {
                fantasyName: 'Stern-Kuemmel',
                realEffect: 'Verdauungsfoerdernd, entblaehend',
                rarity: 'common', icon: '🌰',
                regions: ['wiese', 'garten'], gatherChance: 0.8
            },
            oregano: {
                fantasyName: 'Vulkan-Oregano',
                realEffect: 'Antibakteriell, antioxidativ',
                rarity: 'common', icon: '🌿',
                regions: ['berg', 'huegel'], gatherChance: 0.75
            },
            petersilie: {
                fantasyName: 'Smaragd-Petersilie',
                realEffect: 'Harntreibend, vitaminreich',
                rarity: 'common', icon: '🌱',
                regions: ['garten', 'wiese'], gatherChance: 0.85
            },
            hopfen: {
                fantasyName: 'Traum-Hopfen',
                realEffect: 'Beruhigend, schlaffoerdernd',
                rarity: 'common', icon: '🌿',
                regions: ['wald', 'garten'], gatherChance: 0.75
            },
            wacholder: {
                fantasyName: 'Geister-Wacholder',
                realEffect: 'Harntreibend, verdauungsfoerdernd',
                rarity: 'common', icon: '🫐',
                regions: ['berg', 'wald'], gatherChance: 0.7
            },
            linde: {
                fantasyName: 'Heilige Linde',
                realEffect: 'Schweisstreibernd, beruhigend',
                rarity: 'common', icon: '🍃',
                regions: ['wald', 'dorf'], gatherChance: 0.75
            },
            anis: {
                fantasyName: 'Sternanis-Kristall',
                realEffect: 'Schleimlösend, krampfloesend',
                rarity: 'common', icon: '⭐',
                regions: ['garten', 'wiese'], gatherChance: 0.8
            },
            wermut: {
                fantasyName: 'Bitter-Wermut',
                realEffect: 'Verdauungsfoerdernd, appetitanregend',
                rarity: 'common', icon: '🌿',
                regions: ['sumpf', 'weg'], gatherChance: 0.7
            },
            eisenkraut: {
                fantasyName: 'Stahl-Eisenkraut',
                realEffect: 'Fiebersenkend, entzuendungshemmend',
                rarity: 'common', icon: '🌱',
                regions: ['wiese', 'weg'], gatherChance: 0.75
            },
            hagebutte: {
                fantasyName: 'Rubin-Hagebutte',
                realEffect: 'Vitamin-C-reich, immunstaerkend',
                rarity: 'common', icon: '🫐',
                regions: ['wald', 'huegel'], gatherChance: 0.8
            },
            birke: {
                fantasyName: 'Silber-Birkenrinde',
                realEffect: 'Entzuendungshemmend, harntreibend',
                rarity: 'common', icon: '🌳',
                regions: ['wald', 'fluss'], gatherChance: 0.7
            },
            himbeere: {
                fantasyName: 'Blut-Himbeere',
                realEffect: 'Gebaermutterstaerkend, vitaminreich',
                rarity: 'common', icon: '🍇',
                regions: ['wald', 'garten'], gatherChance: 0.8
            },
            kurkuma: {
                fantasyName: 'Gold-Wurzel',
                realEffect: 'Entzuendungshemmend, antioxidativ',
                rarity: 'common', icon: '🟡',
                regions: ['dschungel', 'garten'], gatherChance: 0.7
            },
            knoblauch: {
                fantasyName: 'Vampir-Knoblauch',
                realEffect: 'Antibakteriell, blutdrucksenkend',
                rarity: 'common', icon: '🧄',
                regions: ['garten', 'dorf'], gatherChance: 0.85
            },
            zimt: {
                fantasyName: 'Drachen-Zimt',
                realEffect: 'Blutzuckerregulierend, waermend',
                rarity: 'common', icon: '🟤',
                regions: ['dschungel', 'markt'], gatherChance: 0.7
            },

            // === UNCOMMON (20) ===
            lavendel: {
                fantasyName: 'Traum-Lavendel',
                realEffect: 'Beruhigend, schlaffoerdernd, angstloesend',
                rarity: 'uncommon', icon: '💜',
                regions: ['hochland', 'garten'], gatherChance: 0.5
            },
            arnika: {
                fantasyName: 'Berg-Arnika',
                realEffect: 'Gegen Prellungen, schmerzlindernd',
                rarity: 'uncommon', icon: '🌼',
                regions: ['berg', 'hochland'], gatherChance: 0.45
            },
            johanniskraut: {
                fantasyName: 'Sonnen-Johanniskraut',
                realEffect: 'Stimmungsaufhellend, antidepressiv',
                rarity: 'uncommon', icon: '☀️',
                regions: ['wiese', 'huegel'], gatherChance: 0.5
            },
            weissdorn: {
                fantasyName: 'Herz-Weissdorn',
                realEffect: 'Herzstaerkend, blutdruckregulierend',
                rarity: 'uncommon', icon: '❤️',
                regions: ['wald', 'huegel'], gatherChance: 0.45
            },
            mistel: {
                fantasyName: 'Druiden-Mistel',
                realEffect: 'Blutdrucksenkend, immunmodulierend',
                rarity: 'uncommon', icon: '🌿',
                regions: ['wald', 'heiliger_hain'], gatherChance: 0.4
            },
            suessholz: {
                fantasyName: 'Honig-Suessholz',
                realEffect: 'Hustenstillend, magenschuetzend',
                rarity: 'uncommon', icon: '🍯',
                regions: ['sumpf', 'fluss'], gatherChance: 0.45
            },
            eibisch: {
                fantasyName: 'Seiden-Eibisch',
                realEffect: 'Schleimhautschuetzend, hustenstillend',
                rarity: 'uncommon', icon: '🌸',
                regions: ['sumpf', 'fluss'], gatherChance: 0.5
            },
            passionsblume: {
                fantasyName: 'Traum-Passionsblume',
                realEffect: 'Angstloesend, schlaffoerdernd',
                rarity: 'uncommon', icon: '🌺',
                regions: ['dschungel', 'garten'], gatherChance: 0.4
            },
            mariendistel: {
                fantasyName: 'Silber-Distel',
                realEffect: 'Leberschuetzend, entgiftend',
                rarity: 'uncommon', icon: '🌵',
                regions: ['wiese', 'weg'], gatherChance: 0.45
            },
            teufelskralle: {
                fantasyName: 'Daemonen-Klaue',
                realEffect: 'Entzuendungshemmend, schmerzlindernd',
                rarity: 'uncommon', icon: '👹',
                regions: ['wueste', 'berg'], gatherChance: 0.4
            },
            beinwell: {
                fantasyName: 'Knochen-Beinwell',
                realEffect: 'Knochenbruch-heilend, wundheilend',
                rarity: 'uncommon', icon: '🦴',
                regions: ['wiese', 'sumpf'], gatherChance: 0.45
            },
            enzian: {
                fantasyName: 'Azur-Enzian',
                realEffect: 'Verdauungsfoerdernd, appetitanregend',
                rarity: 'uncommon', icon: '💙',
                regions: ['berg', 'hochland'], gatherChance: 0.4
            },
            myrrhe: {
                fantasyName: 'Heilige Myrrhe',
                realEffect: 'Antiseptisch, entzuendungshemmend',
                rarity: 'uncommon', icon: '🟤',
                regions: ['wueste', 'tempel'], gatherChance: 0.35
            },
            weihrauch: {
                fantasyName: 'Tempel-Weihrauch',
                realEffect: 'Entzuendungshemmend, beruhigend',
                rarity: 'uncommon', icon: '💨',
                regions: ['tempel', 'berg'], gatherChance: 0.35
            },
            klette: {
                fantasyName: 'Eisen-Klette',
                realEffect: 'Blutreinigend, hautpflegend',
                rarity: 'uncommon', icon: '🌰',
                regions: ['wald', 'weg'], gatherChance: 0.5
            },
            suessdolde: {
                fantasyName: 'Zucker-Dolde',
                realEffect: 'Verdauungsfoerdernd, harntreibend',
                rarity: 'uncommon', icon: '🌿',
                regions: ['wald', 'berg'], gatherChance: 0.45
            },
            maedesuess: {
                fantasyName: 'Koenigin-Maedesuess',
                realEffect: 'Fiebersenkend, schmerzlindernd (natuerliches Aspirin)',
                rarity: 'uncommon', icon: '👑',
                regions: ['sumpf', 'fluss'], gatherChance: 0.4
            },
            augentrost: {
                fantasyName: 'Kristall-Augentrost',
                realEffect: 'Augenheilend, entzuendungshemmend',
                rarity: 'uncommon', icon: '👁️',
                regions: ['wiese', 'berg'], gatherChance: 0.4
            },
            aktivkohle: {
                fantasyName: 'Void-Kohle',
                realEffect: 'Toxin-bindend, entgiftend',
                rarity: 'uncommon', icon: '⬛',
                regions: ['hoehle', 'vulkan'], gatherChance: 0.5
            },
            aloe: {
                fantasyName: 'Wuesten-Aloe',
                realEffect: 'Wundheilend, hautpflegend, kuehlend',
                rarity: 'uncommon', icon: '🌵',
                regions: ['wueste', 'garten'], gatherChance: 0.45
            },

            // === RARE (10) ===
            ginseng: {
                fantasyName: 'Kaiser-Ginseng',
                realEffect: 'Adaptogen, energiesteigernd, immunstaerkend',
                rarity: 'rare', icon: '🏮',
                regions: ['berg', 'heiliger_hain'], gatherChance: 0.2
            },
            echinacea: {
                fantasyName: 'Sonnen-Echinacea',
                realEffect: 'Immunsystem-Booster, erkaeltungslindernd',
                rarity: 'rare', icon: '🌺',
                regions: ['wiese', 'hochland'], gatherChance: 0.2
            },
            ginkgo: {
                fantasyName: 'Uralter Ginkgo',
                realEffect: 'Durchblutungsfoerdernd, gedaechtnisstaerkend',
                rarity: 'rare', icon: '🍂',
                regions: ['heiliger_hain', 'tempel'], gatherChance: 0.15
            },
            ashwagandha: {
                fantasyName: 'Schlaf-Beere',
                realEffect: 'Stresslindernd, adaptogen, kraftsteigernd',
                rarity: 'rare', icon: '🫐',
                regions: ['wueste', 'dschungel'], gatherChance: 0.2
            },
            rhodiola: {
                fantasyName: 'Frost-Rhodiola',
                realEffect: 'Adaptogen, ausdauersteigernd, stressresistent',
                rarity: 'rare', icon: '❄️',
                regions: ['berg', 'tundra'], gatherChance: 0.15
            },
            safran: {
                fantasyName: 'Sonnentraenen-Safran',
                realEffect: 'Stimmungsaufhellend, antioxidativ',
                rarity: 'rare', icon: '🧡',
                regions: ['wueste', 'garten'], gatherChance: 0.1
            },
            baldachin_moos: {
                fantasyName: 'Sternenmoos',
                realEffect: 'Antiseptisch, wundheilend',
                rarity: 'rare', icon: '🌌',
                regions: ['hoehle', 'tiefer_wald'], gatherChance: 0.15
            },
            schwarzkuemmel: {
                fantasyName: 'Nacht-Kuemmel',
                realEffect: 'Immunstaerkend, entzuendungshemmend, antiallergisch',
                rarity: 'rare', icon: '🌑',
                regions: ['wueste', 'tempel'], gatherChance: 0.2
            },
            cordyceps: {
                fantasyName: 'Geister-Pilz',
                realEffect: 'Energiesteigernd, ausdauerfoerdernd',
                rarity: 'rare', icon: '🍄',
                regions: ['hoehle', 'berg'], gatherChance: 0.15
            },
            reishi: {
                fantasyName: 'Ewiger Reishi',
                realEffect: 'Immunmodulierend, stresslindernd, leberstaerkend',
                rarity: 'rare', icon: '🍄',
                regions: ['tiefer_wald', 'heiliger_hain'], gatherChance: 0.15
            },

            // === LEGENDARY (4) ===
            alraune: {
                fantasyName: 'Schreiende Alraune',
                realEffect: 'Narkotisch, schmerzstillend (historisch als Anaesthetikum)',
                rarity: 'legendary', icon: '🌑',
                regions: ['friedhof', 'tiefer_wald'], gatherChance: 0.05
            },
            mondblume: {
                fantasyName: 'Mond-Orchidee',
                realEffect: 'Legendaere Allheilpflanze (mythisch)',
                rarity: 'legendary', icon: '🌙',
                regions: ['goetterfels'], gatherChance: 0.03
            },
            phoenix_farn: {
                fantasyName: 'Phoenix-Farn',
                realEffect: 'Regenerativ, zellerneuernd (legendaer)',
                rarity: 'legendary', icon: '🔥',
                regions: ['vulkan'], gatherChance: 0.03
            },
            weltenbaum_rinde: {
                fantasyName: 'Weltenbaum-Rinde',
                realEffect: 'Universalheilmittel, magiefoerdernd',
                rarity: 'legendary', icon: '🌳',
                regions: ['goetterfels', 'heiliger_hain'], gatherChance: 0.02
            }
        };
    }

    // ==========================================
    // REZEPTE
    // ==========================================

    initRecipes() {
        return {
            heiltrank_klein: {
                name: 'Kleiner Heiltrank',
                icon: '🧪',
                ingredients: { kamille: 2, salbei: 1 },
                effect: 'HP +50',
                gameEffect: { hp: 50 },
                realBasis: 'Kamille (entzuendungshemmend) + Salbei (antibakteriell)',
                difficulty: 'einfach'
            },
            heiltrank_gross: {
                name: 'Grosser Heiltrank',
                icon: '🧪',
                ingredients: { kamille: 3, ringelblume: 2, beinwell: 1 },
                effect: 'HP +150',
                gameEffect: { hp: 150 },
                realBasis: 'Kamille + Calendula (wundheilend) + Beinwell (knochenstaerkend)',
                difficulty: 'mittel'
            },
            beruhigungstrank: {
                name: 'Beruhigungstrank',
                icon: '😌',
                ingredients: { kamille: 2, lavendel: 1, baldrian: 1 },
                effect: 'Stress -50, Schlaf +30',
                gameEffect: { happiness: 30, energy: 20 },
                realBasis: 'Kamille + Lavendel + Baldrian = bewaehrte Schlaf-Kombination',
                difficulty: 'einfach'
            },
            energietrank: {
                name: 'Energietrank',
                icon: '⚡',
                ingredients: { pfefferminz: 2, ginseng: 1 },
                effect: 'Energie +100, Ausdauer +50',
                gameEffect: { energy: 100 },
                realBasis: 'Minze (belebend) + Ginseng (adaptogen, energiesteigernd)',
                difficulty: 'mittel'
            },
            gegengift: {
                name: 'Gegengift',
                icon: '💚',
                ingredients: { aktivkohle: 2, ingwer: 1, mariendistel: 1 },
                effect: 'Gift-Resistenz +80%',
                gameEffect: { cure_poison: true },
                realBasis: 'Aktivkohle bindet Toxine, Ingwer beruhigt Magen, Mariendistel schuetzt Leber',
                difficulty: 'mittel'
            },
            schmerzmittel: {
                name: 'Natuerliches Schmerzmittel',
                icon: '💊',
                ingredients: { maedesuess: 2, arnika: 1, pfefferminz: 1 },
                effect: 'Schmerz -80%, DEF +10',
                gameEffect: { defense: 10 },
                realBasis: 'Maedesuess (natuerliches Aspirin!) + Arnika (Prellungen) + Minze (kuehlend)',
                difficulty: 'mittel'
            },
            fiebertrank: {
                name: 'Fiebertrank',
                icon: '🌡️',
                ingredients: { holunder: 2, linde: 2, eisenkraut: 1 },
                effect: 'Fieber heilen, Immun +20',
                gameEffect: { cure_fever: true },
                realBasis: 'Holunder + Linde (schweisstreibernd) + Eisenkraut (fiebersenkend)',
                difficulty: 'einfach'
            },
            konzentrationselixier: {
                name: 'Konzentrations-Elixier',
                icon: '🧠',
                ingredients: { rosmarin: 2, ginkgo: 1, pfefferminz: 1 },
                effect: 'INT +15 (30min)',
                gameEffect: { intelligence: 15 },
                realBasis: 'Rosmarin + Ginkgo (durchblutungsfoerdernd) = Gedaechtnis-Boost',
                difficulty: 'schwer'
            },
            immunbooster: {
                name: 'Immun-Booster',
                icon: '🛡️',
                ingredients: { echinacea: 1, hagebutte: 3, schwarzkuemmel: 1 },
                effect: 'Krankheits-Resistenz +60%',
                gameEffect: { immunity: 60 },
                realBasis: 'Echinacea (Immunsystem) + Hagebutte (Vitamin C) + Schwarzkuemmel',
                difficulty: 'schwer'
            },
            wundsalbe: {
                name: 'Heilsalbe',
                icon: '🩹',
                ingredients: { ringelblume: 2, aloe: 1, baldachin_moos: 1 },
                effect: 'Regeneration +5 HP/s (60s)',
                gameEffect: { regen: 5 },
                realBasis: 'Calendula (wundheilend) + Aloe (hautpflegend) + Moos (antiseptisch)',
                difficulty: 'mittel'
            },
            stimmungsaufheller: {
                name: 'Stimmungsaufheller',
                icon: '😊',
                ingredients: { johanniskraut: 2, safran: 1, melisse: 1 },
                effect: 'Happiness +50, Mood: happy',
                gameEffect: { happiness: 50 },
                realBasis: 'Johanniskraut (natuerliches Antidepressivum) + Safran + Melisse',
                difficulty: 'schwer'
            },
            adaptogen_tonic: {
                name: 'Adaptogen-Tonikum',
                icon: '💪',
                ingredients: { ashwagandha: 1, rhodiola: 1, ginseng: 1, reishi: 1 },
                effect: 'Alle Stats +10 (10min)',
                gameEffect: { all_stats: 10 },
                realBasis: 'Vier maechtige Adaptogene - maximale Stressresistenz',
                difficulty: 'legendaer'
            },
            phoenix_elixier: {
                name: 'Phoenix-Elixier',
                icon: '🔥',
                ingredients: { phoenix_farn: 1, mondblume: 1, alraune: 1, weltenbaum_rinde: 1 },
                effect: 'Volle HP + Wiederbelebung (einmalig)',
                gameEffect: { full_heal: true, revive: true },
                realBasis: 'Alle 4 legendaeren Pflanzen vereint - das ultimative Heilmittel',
                difficulty: 'legendaer'
            }
        };
    }

    // ==========================================
    // UI CREATION
    // ==========================================

    createUI() {
        const container = document.createElement('div');
        container.id = 'medicine-crafting-panel';
        container.innerHTML = `
            <style>
                #medicine-crafting-panel {
                    position: fixed;
                    top: 50%; left: 50%;
                    transform: translate(-50%, -50%);
                    width: 700px; max-height: 85vh;
                    background: linear-gradient(135deg, #1a2a1a 0%, #0d1f0d 100%);
                    border: 2px solid #4a4;
                    border-radius: 15px;
                    z-index: 10000;
                    display: none;
                    overflow: hidden;
                    box-shadow: 0 0 40px rgba(0, 255, 0, 0.15);
                    font-family: 'Segoe UI', sans-serif;
                    color: #fff;
                }
                #medicine-crafting-panel.open { display: block; animation: medFadeIn 0.3s ease; }
                @keyframes medFadeIn {
                    from { opacity: 0; transform: translate(-50%, -50%) scale(0.9); }
                    to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                }
                .med-header {
                    background: linear-gradient(90deg, #2a5a2a 0%, #1a3a1a 100%);
                    padding: 15px 20px;
                    display: flex; justify-content: space-between; align-items: center;
                }
                .med-header h2 { margin: 0; font-size: 20px; }
                .med-close {
                    background: none; border: none; color: #fff;
                    font-size: 24px; cursor: pointer;
                }
                .med-tabs {
                    display: flex; border-bottom: 2px solid #333;
                }
                .med-tab {
                    flex: 1; padding: 12px; text-align: center;
                    background: #1a1a1a; border: none; color: #888;
                    cursor: pointer; font-size: 14px; transition: all 0.2s;
                }
                .med-tab:hover { background: #252525; color: #aaa; }
                .med-tab.active { background: #2a3a2a; color: #4f4; border-bottom: 2px solid #4f4; }
                .med-content {
                    padding: 15px; overflow-y: auto; max-height: 60vh;
                }
                .med-region-select {
                    display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px;
                }
                .med-region-btn {
                    padding: 6px 12px; background: #222; border: 1px solid #444;
                    border-radius: 6px; color: #aaa; cursor: pointer; font-size: 12px;
                }
                .med-region-btn:hover { border-color: #4a4; color: #fff; }
                .med-region-btn.active { border-color: #4f4; background: #1a3a1a; color: #4f4; }
                .plant-grid {
                    display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 10px;
                }
                .plant-card {
                    background: rgba(255,255,255,0.03); border: 1px solid #333;
                    border-radius: 10px; padding: 12px; cursor: pointer;
                    transition: all 0.2s;
                }
                .plant-card:hover { border-color: #4a4; transform: scale(1.02); }
                .plant-card.rarity-common { border-left: 3px solid #aaa; }
                .plant-card.rarity-uncommon { border-left: 3px solid #4a4; }
                .plant-card.rarity-rare { border-left: 3px solid #44f; }
                .plant-card.rarity-legendary { border-left: 3px solid #fa0; box-shadow: 0 0 10px rgba(255,170,0,0.1); }
                .plant-icon { font-size: 24px; }
                .plant-name { font-size: 14px; font-weight: bold; margin-top: 4px; }
                .plant-effect { font-size: 11px; color: #888; margin-top: 2px; }
                .plant-count { font-size: 12px; color: #4f4; margin-top: 4px; }
                .plant-gather-btn {
                    margin-top: 8px; padding: 4px 10px;
                    background: #2a4a2a; border: 1px solid #4a4;
                    border-radius: 5px; color: #4f4; cursor: pointer; font-size: 11px;
                    width: 100%;
                }
                .plant-gather-btn:hover { background: #3a5a3a; }
                .plant-gather-btn:disabled { opacity: 0.4; cursor: not-allowed; }
                .recipe-card {
                    background: rgba(255,255,255,0.03); border: 1px solid #333;
                    border-radius: 10px; padding: 15px; margin-bottom: 10px;
                }
                .recipe-card.can-craft { border-color: #4a4; }
                .recipe-card.cannot-craft { opacity: 0.6; }
                .recipe-name { font-size: 16px; font-weight: bold; }
                .recipe-effect { color: #4f4; font-size: 13px; margin: 4px 0; }
                .recipe-ingredients { font-size: 12px; color: #aaa; margin: 6px 0; }
                .recipe-real { font-size: 11px; color: #666; font-style: italic; }
                .recipe-craft-btn {
                    margin-top: 8px; padding: 8px 16px;
                    background: linear-gradient(135deg, #2a5a2a, #1a3a1a);
                    border: 1px solid #4a4; border-radius: 8px;
                    color: #fff; cursor: pointer; font-size: 13px;
                }
                .recipe-craft-btn:hover { background: linear-gradient(135deg, #3a6a3a, #2a4a2a); }
                .recipe-craft-btn:disabled { opacity: 0.4; cursor: not-allowed; }
                .med-notification {
                    position: fixed; top: 20px; left: 50%;
                    transform: translateX(-50%);
                    background: #1a3a1a; border: 1px solid #4a4;
                    border-radius: 10px; padding: 12px 20px;
                    color: #4f4; font-size: 14px; z-index: 10001;
                    animation: medNotifIn 0.3s ease;
                }
                @keyframes medNotifIn {
                    from { opacity: 0; top: 0; }
                    to { opacity: 1; top: 20px; }
                }
                .difficulty-einfach { color: #4f4; }
                .difficulty-mittel { color: #fa0; }
                .difficulty-schwer { color: #f44; }
                .difficulty-legendaer { color: #f0f; text-shadow: 0 0 5px #f0f; }
                .inv-summary {
                    background: rgba(0,255,0,0.05); border: 1px solid #333;
                    border-radius: 8px; padding: 10px; margin-bottom: 15px;
                    font-size: 12px; color: #888;
                }
                .inv-summary strong { color: #4f4; }
            </style>
            <div class="med-header">
                <h2>🌿 Kraeuterkunde</h2>
                <button class="med-close" id="med-close-btn">&times;</button>
            </div>
            <div class="med-tabs">
                <button class="med-tab active" data-tab="gather">🌱 Sammeln</button>
                <button class="med-tab" data-tab="recipes">📖 Rezeptbuch</button>
                <button class="med-tab" data-tab="crafting">⚗️ Brauen</button>
            </div>
            <div class="med-content" id="med-content"></div>
        `;

        document.body.appendChild(container);
        this.panel = container;

        // Events
        document.getElementById('med-close-btn').addEventListener('click', () => this.close());
        container.querySelectorAll('.med-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                container.querySelectorAll('.med-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                this.currentTab = tab.dataset.tab;
                this.renderContent();
            });
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) this.close();
        });
    }

    // ==========================================
    // OPEN / CLOSE
    // ==========================================

    open() {
        this.panel.classList.add('open');
        this.isOpen = true;
        this.renderContent();
    }

    close() {
        this.panel.classList.remove('open');
        this.isOpen = false;
    }

    toggle() {
        if (this.isOpen) this.close();
        else this.open();
    }

    // ==========================================
    // RENDER
    // ==========================================

    renderContent() {
        const content = document.getElementById('med-content');
        switch (this.currentTab) {
            case 'gather': this.renderGatherTab(content); break;
            case 'recipes': this.renderRecipesTab(content); break;
            case 'crafting': this.renderCraftingTab(content); break;
        }
    }

    renderGatherTab(content) {
        const regions = this.getAvailableRegions();
        const plantsInRegion = this.getPlantsInRegion(this.currentRegion);

        content.innerHTML = `
            <div class="med-region-select">
                ${regions.map(r => `
                    <button class="med-region-btn ${r === this.currentRegion ? 'active' : ''}"
                            onclick="medicineCrafting.setRegion('${r}')">
                        ${this.getRegionIcon(r)} ${this.formatRegionName(r)}
                    </button>
                `).join('')}
            </div>
            <div class="inv-summary">
                Inventar: <strong>${Object.values(this.inventory).reduce((a, b) => a + b, 0)}</strong> Pflanzen gesammelt
            </div>
            <div class="plant-grid">
                ${plantsInRegion.map(([id, plant]) => `
                    <div class="plant-card rarity-${plant.rarity}">
                        <span class="plant-icon">${plant.icon}</span>
                        <div class="plant-name">${plant.fantasyName}</div>
                        <div class="plant-effect">${plant.realEffect}</div>
                        <div class="plant-count">Vorrat: ${this.inventory[id] || 0}</div>
                        <button class="plant-gather-btn"
                                onclick="medicineCrafting.gatherPlant('${id}')">
                            Sammeln (${Math.round(plant.gatherChance * 100)}%)
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderRecipesTab(content) {
        const recipes = Object.entries(this.recipes);

        content.innerHTML = `
            <div class="inv-summary">
                Rezepte entdeckt: <strong>${this.discoveredRecipes.size}</strong> / ${recipes.length}
            </div>
            ${recipes.map(([id, recipe]) => {
                const discovered = this.discoveredRecipes.has(id);
                const canCraft = this.canCraftRecipe(id);
                return `
                    <div class="recipe-card ${canCraft ? 'can-craft' : 'cannot-craft'}">
                        <div class="recipe-name">
                            ${recipe.icon} ${discovered ? recipe.name : '??? Unbekanntes Rezept'}
                            <span class="difficulty-${recipe.difficulty}">[${recipe.difficulty}]</span>
                        </div>
                        ${discovered ? `
                            <div class="recipe-effect">${recipe.effect}</div>
                            <div class="recipe-ingredients">
                                Zutaten: ${Object.entries(recipe.ingredients).map(([plant, count]) => {
                                    const p = this.plants[plant];
                                    const have = this.inventory[plant] || 0;
                                    const enough = have >= count;
                                    return `<span style="color: ${enough ? '#4f4' : '#f44'}">${p ? p.fantasyName : plant} x${count} (${have})</span>`;
                                }).join(', ')}
                            </div>
                            <div class="recipe-real">${recipe.realBasis}</div>
                        ` : `
                            <div class="recipe-effect" style="color: #666;">Sammle mehr Pflanzen um dieses Rezept zu entdecken...</div>
                        `}
                    </div>
                `;
            }).join('')}
        `;
    }

    renderCraftingTab(content) {
        const craftableRecipes = Object.entries(this.recipes)
            .filter(([id]) => this.discoveredRecipes.has(id));

        content.innerHTML = `
            <div class="inv-summary">
                Braubare Traenke: <strong>${craftableRecipes.filter(([id]) => this.canCraftRecipe(id)).length}</strong> / ${craftableRecipes.length} entdeckt
            </div>
            ${craftableRecipes.length === 0 ? `
                <div style="text-align: center; color: #666; padding: 40px;">
                    Noch keine Rezepte entdeckt!<br>
                    Sammle Pflanzen um Rezepte freizuschalten.
                </div>
            ` : craftableRecipes.map(([id, recipe]) => {
                const canCraft = this.canCraftRecipe(id);
                return `
                    <div class="recipe-card ${canCraft ? 'can-craft' : 'cannot-craft'}">
                        <div class="recipe-name">${recipe.icon} ${recipe.name}</div>
                        <div class="recipe-effect">${recipe.effect}</div>
                        <div class="recipe-ingredients">
                            ${Object.entries(recipe.ingredients).map(([plant, count]) => {
                                const p = this.plants[plant];
                                const have = this.inventory[plant] || 0;
                                return `<span style="color: ${have >= count ? '#4f4' : '#f44'}">${p ? p.fantasyName : plant} x${count} (${have})</span>`;
                            }).join(' + ')}
                        </div>
                        <button class="recipe-craft-btn" ${canCraft ? '' : 'disabled'}
                                onclick="medicineCrafting.craftRecipe('${id}')">
                            ${canCraft ? '⚗️ Brauen!' : 'Nicht genug Zutaten'}
                        </button>
                    </div>
                `;
            }).join('')}
        `;
    }

    // ==========================================
    // GAME LOGIC
    // ==========================================

    gatherPlant(plantId) {
        const plant = this.plants[plantId];
        if (!plant) return;

        const success = Math.random() < plant.gatherChance;

        if (success) {
            this.inventory[plantId] = (this.inventory[plantId] || 0) + 1;
            this.showNotification(`${plant.icon} ${plant.fantasyName} gesammelt!`);
            this.checkRecipeDiscovery();
        } else {
            this.showNotification(`Nichts gefunden... Versuch es nochmal!`, false);
        }

        this.saveState();
        this.renderContent();
    }

    craftRecipe(recipeId) {
        const recipe = this.recipes[recipeId];
        if (!recipe || !this.canCraftRecipe(recipeId)) return;

        // Zutaten verbrauchen
        for (const [plant, count] of Object.entries(recipe.ingredients)) {
            this.inventory[plant] -= count;
            if (this.inventory[plant] <= 0) delete this.inventory[plant];
        }

        this.showNotification(`${recipe.icon} ${recipe.name} gebraut! ${recipe.effect}`);

        // Effekt anwenden (falls Backend verfuegbar)
        if (recipe.gameEffect) {
            this.applyEffect(recipe.gameEffect);
        }

        this.saveState();
        this.renderContent();
    }

    canCraftRecipe(recipeId) {
        const recipe = this.recipes[recipeId];
        if (!recipe) return false;
        return Object.entries(recipe.ingredients).every(
            ([plant, count]) => (this.inventory[plant] || 0) >= count
        );
    }

    checkRecipeDiscovery() {
        // Rezepte werden entdeckt wenn man mindestens 1 von jeder Zutat hat
        for (const [id, recipe] of Object.entries(this.recipes)) {
            if (this.discoveredRecipes.has(id)) continue;
            const hasAllIngredients = Object.keys(recipe.ingredients).every(
                plant => (this.inventory[plant] || 0) > 0
            );
            if (hasAllIngredients) {
                this.discoveredRecipes.add(id);
                this.showNotification(`📖 Neues Rezept entdeckt: ${recipe.name}!`);
            }
        }
    }

    async applyEffect(effect) {
        try {
            if (effect.hp) {
                await fetch('http://127.0.0.1:8000/api/v2/care/heal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
            }
            if (effect.energy) {
                await fetch('http://127.0.0.1:8000/api/state/najika/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ updates: { energy: Math.min(100, 70 + effect.energy) } })
                });
            }
            if (effect.happiness) {
                await fetch('http://127.0.0.1:8000/api/state/najika/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ updates: { happiness: Math.min(100, 70 + effect.happiness) } })
                });
            }
        } catch (e) {
            // Backend nicht erreichbar - nur Frontend-Effekt
        }
    }

    // ==========================================
    // HELPERS
    // ==========================================

    getAvailableRegions() {
        const regions = new Set();
        for (const plant of Object.values(this.plants)) {
            plant.regions.forEach(r => regions.add(r));
        }
        return [...regions].sort();
    }

    getPlantsInRegion(region) {
        return Object.entries(this.plants)
            .filter(([, plant]) => plant.regions.includes(region));
    }

    setRegion(region) {
        this.currentRegion = region;
        this.renderContent();
    }

    getRegionIcon(region) {
        const icons = {
            wiese: '🌾', wald: '🌲', berg: '🏔️', fluss: '🏞️',
            sumpf: '🌿', garten: '🏡', huegel: '⛰️', dschungel: '🌴',
            hochland: '🗻', kueste: '🏖️', wueste: '🏜️', tempel: '🏛️',
            hoehle: '🕳️', vulkan: '🌋', heiliger_hain: '✨', tundra: '❄️',
            tiefer_wald: '🌑', friedhof: '⚰️', goetterfels: '🗿',
            dorf: '🏘️', weg: '🛤️', markt: '🏪'
        };
        return icons[region] || '📍';
    }

    formatRegionName(region) {
        return region.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    }

    showNotification(msg, success = true) {
        const notif = document.createElement('div');
        notif.className = 'med-notification';
        notif.style.borderColor = success ? '#4a4' : '#a44';
        notif.style.color = success ? '#4f4' : '#f44';
        notif.textContent = msg;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 3000);
    }

    // ==========================================
    // PERSISTENCE (localStorage)
    // ==========================================

    saveState() {
        try {
            localStorage.setItem('najika_medicine', JSON.stringify({
                inventory: this.inventory,
                discoveredRecipes: [...this.discoveredRecipes]
            }));
        } catch (e) { /* Silent */ }
    }

    loadState() {
        try {
            const saved = localStorage.getItem('najika_medicine');
            if (saved) {
                const data = JSON.parse(saved);
                this.inventory = data.inventory || {};
                this.discoveredRecipes = new Set(data.discoveredRecipes || []);
            }
        } catch (e) { /* Silent */ }
    }
}

// ==========================================
// GLOBAL INIT
// ==========================================

let medicineCrafting = null;

document.addEventListener('DOMContentLoaded', () => {
    medicineCrafting = new MedicineCraftingUI();
});

if (document.readyState !== 'loading') {
    medicineCrafting = new MedicineCraftingUI();
}

if (typeof window !== 'undefined') {
    window.MedicineCraftingUI = MedicineCraftingUI;
    window.medicineCrafting = medicineCrafting;
}
