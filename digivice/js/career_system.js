/**
 * NAJIKA WORLD - CAREER / BERUFSPFAD SYSTEM
 * ===========================================
 * Mount & Blade 2 / Kenshi / Konosuba Gilde Style
 *
 * LEARNING BY DOING: Jeder Beruf hat 50 Level.
 * Lvl 1 Koch = Matsch. Lvl 50 Koch = Buff-Essen aus Resten.
 * Erfahrener Koch schneidet Schlechtes weg, behält Gutes.
 * Das gilt SINNBILDLICH für ALLE Berufe!
 *
 * Du kannst HEUTE Bäcker und ABENDS Fischer sein.
 * Aber echte Erfahrung kommt nur mit der Zeit.
 *
 * Aufträge an Gilde / Kneipe / Gildenhaus oder in der Welt
 * 24+ Berufspfade für die ultimative Lebenssimulation!
 */

(function() {
    'use strict';

    // ==========================================
    // LEARNING BY DOING - Kern-Mechanik
    // ==========================================
    // Jeder Beruf: Level 1-50, XP durch AUSÜBEN
    // Skill-Effekt skaliert mit Level:
    //   effectiveness = baseEffect * (1 + (level - 1) * 0.04)
    //   → Lvl 1 = 1.0x, Lvl 25 = 1.96x, Lvl 50 = 2.96x

    function calcEffectiveness(level) {
        return 1.0 + (Math.max(1, level) - 1) * 0.04;
    }

    // XP-Tabelle: Level N braucht N*50 + (N-1)*25 XP
    function xpForLevel(level) {
        return level * 50 + (level - 1) * 25;
    }

    function totalXPForLevel(level) {
        let total = 0;
        for (let i = 1; i <= level; i++) total += xpForLevel(i);
        return total;
    }

    // ==========================================
    // CAREER DEFINITIONS (24+ Berufe!)
    // ==========================================
    // Jeder Beruf hat:
    //   category: Gruppe (kampf, handwerk, handel, natur, sozial, wissen)
    //   levelEffects: Was sich mit Level verbessert (Learning by Doing!)
    //   tasks: Mögliche Aufgaben die man annehmen kann

    const CAREERS = {

        // ========== KAMPF & SCHUTZ ==========

        postman: {
            id: 'postman', name: 'Postman-Ranger', icon: '📮', category: 'kampf',
            description: 'Einsamer Bote. Zu Fuß. Allein. Heldenhaft. Wie die NCR Rangers.',
            color: '#8B4513', systemRef: 'PostmanSystem',
            levelEffects: {
                1:  'Kann einfache Nachrichten zustellen',
                10: 'Erkennt Hinterhalte 25% besser',
                25: '-30% Stamina beim Laufen, kennt Abkürzungen',
                40: 'Banditen fliehen manchmal (20%)',
                50: 'Legende! NPCs erkennen dich überall. Respekt. Geheimnisse.',
            },
            tasks: [
                { type: 'deliver_message', description: 'Liefere Nachricht von A nach B' },
                { type: 'deliver_herbs', description: 'Bringe seltene Kräuter zum Empfänger' },
                { type: 'deliver_artifact', description: 'Transportiere wertvolles Artefakt' },
                { type: 'secret_message', description: 'Geheimbotschaft überbringen' },
            ],
        },

        soeldner: {
            id: 'soeldner', name: 'Söldner / Kopfgeldjäger', icon: '⚔️', category: 'kampf',
            description: 'Kampf ist dein Geschäft. Kopfgelder, Dungeon-Raids, Auftragsarbeit.',
            color: '#B22222',
            levelEffects: {
                1:  'Kann einfache Kopfgelder jagen',
                10: '+15% Schaden gegen Kopfgeld-Ziele',
                25: 'Kann Dungeon-Raids leiten (Gruppenanführer)',
                40: 'Gefürchtet! Feinde haben -10% Moral in deiner Nähe',
                50: 'Legendärer Krieger. Arenen-Champion. Könige fürchten dich.',
            },
            tasks: [
                { type: 'bounty_hunt', description: 'Jage gesuchte Person' },
                { type: 'dungeon_clear', description: 'Säubere Dungeon gegen Bezahlung' },
                { type: 'monster_hunt', description: 'Töte bestimmtes Monster' },
                { type: 'arena_fight', description: 'Kämpfe in der Arena' },
                { type: 'guard_duty', description: 'Bewache Ort gegen Angriffswellen' },
            ],
        },

        eskorte: {
            id: 'eskorte', name: 'Eskorte / Geleitschutz', icon: '🛡️', category: 'kampf',
            description: 'Beschütze Reisende, NPCs und Karawanen. MIT Planwagen!',
            color: '#4169E1', planwagen: true,
            levelEffects: {
                1:  'Kann 1 Person eskortieren',
                10: 'Erkennt Gefahren 30% früher, kann 3 Personen schützen',
                25: 'Kann Karawanen mit Planwagen führen (bis 6 Personen)',
                40: 'Schutzaura: Schützlinge nehmen -15% Schaden',
                50: 'Legendärer Beschützer. Niemand stirbt unter deinem Schutz.',
            },
            tasks: [
                { type: 'npc_escort', description: 'Bringe NPC sicher ans Ziel' },
                { type: 'caravan_guard', description: 'Beschütze Handelskarawane' },
                { type: 'vip_protection', description: 'Beschütze wichtige Person' },
                { type: 'prisoner_transport', description: 'Transportiere Gefangenen' },
            ],
        },

        // ========== HANDWERK ==========

        schmied: {
            id: 'schmied', name: 'Schmied', icon: '🔨', category: 'handwerk',
            description: 'Schmiede Waffen und Rüstungen. Repariere Ausrüstung.',
            color: '#FF6347',
            levelEffects: {
                1:  'Kann einfache Eisenwaffen reparieren (50% Chance auf Pfusch)',
                10: 'Stahlwaffen schmieden, Reparatur zuverlässig',
                25: 'Seltene Materialien verarbeiten, eigene Designs',
                40: 'Meisterwerke: +15% Stats auf gecraftete Items',
                50: 'Götterschmied: Legendäre Waffen mit einzigartigen Effekten',
            },
            tasks: [
                { type: 'forge_weapon', description: 'Schmiede Waffe nach Auftrag' },
                { type: 'repair_gear', description: 'Repariere beschädigte Ausrüstung' },
                { type: 'custom_order', description: 'Spezialanfertigung' },
                { type: 'bulk_order', description: 'Massenproduktion für Armee' },
            ],
        },

        zimmermann: {
            id: 'zimmermann', name: 'Zimmermann / Baumeister', icon: '🪚', category: 'handwerk',
            description: 'Baue Gebäude, Möbel, Planwagen. Repariere Brücken und Häuser.',
            color: '#DEB887',
            levelEffects: {
                1:  'Kann einfache Holzmöbel zimmern (wackelig)',
                10: 'Solide Konstruktionen, kann Planwagen bauen',
                25: 'Brücken bauen/reparieren, Häuser errichten',
                40: 'Befestigungen und Verteidigungsanlagen',
                50: 'Meisterarchitekt: Gebäude mit besonderen Funktionen',
            },
            tasks: [
                { type: 'build_furniture', description: 'Baue Möbel für Auftraggeber' },
                { type: 'repair_bridge', description: 'Repariere zerstörte Brücke' },
                { type: 'build_wagon', description: 'Baue Planwagen' },
                { type: 'build_house', description: 'Errichte Gebäude' },
            ],
        },

        schneider: {
            id: 'schneider', name: 'Schneider / Weber', icon: '🧵', category: 'handwerk',
            description: 'Nähe Kleidung, Rüstungspolster, Taschen. Mode UND Funktion.',
            color: '#DA70D6',
            levelEffects: {
                1:  'Kann Lumpen zusammenflicken (hält kaum)',
                10: 'Ordentliche Kleidung, leichte Rüstungspolster',
                25: 'Spezialkleidung: Postman-Mäntel, Tarnumhänge',
                40: 'Magisch verstärkte Stoffe (+Buff-Effekte)',
                50: 'Meisterschneider: Legendäre Roben und Mäntel',
            },
            tasks: [
                { type: 'sew_clothes', description: 'Nähe Kleidung nach Maß' },
                { type: 'craft_armor_padding', description: 'Fertige Rüstungspolster' },
                { type: 'special_uniform', description: 'Spezialuniform herstellen' },
                { type: 'repair_clothing', description: 'Repariere beschädigte Kleidung' },
            ],
        },

        lederer: {
            id: 'lederer', name: 'Gerber / Lederer', icon: '🦌', category: 'handwerk',
            description: 'Verarbeite Häute zu Leder. Taschen, Gürtel, Lederrüstungen.',
            color: '#8B4513',
            levelEffects: {
                1:  'Kann rohes Leder grob zuschneiden',
                10: 'Solide Lederwaren, Gürtel, einfache Taschen',
                25: 'Leichte Lederrüstungen, verstärkte Taschen',
                40: 'Exotische Häute verarbeiten (Drake, Wurm)',
                50: 'Meistgerber: Drachenleder-Rüstungen, unzerstörbar',
            },
            tasks: [
                { type: 'tan_hides', description: 'Gerbe Tierhäute zu Leder' },
                { type: 'craft_bag', description: 'Fertige Taschen und Beutel' },
                { type: 'leather_armor', description: 'Stelle Lederrüstung her' },
                { type: 'exotic_leather', description: 'Verarbeite exotische Häute' },
            ],
        },

        // ========== NAHRUNG & NATUR ==========

        koch: {
            id: 'koch', name: 'Koch / Bäcker', icon: '🍳', category: 'natur',
            description: 'Koche Essen das Buffs gibt. Oder Matsch der den Hunger stillt.',
            color: '#FF8C00',
            levelEffects: {
                1:  'Kann Zutaten zusammenwerfen (stillt Hunger, mehr nicht)',
                10: 'Ordentliche Mahlzeiten, kleine HP-Regeneration',
                25: 'Buff-Essen! +10% Stats für 5 Minuten. Schneidet Schlechtes weg.',
                40: 'Gourmet-Essen: +20% Stats, heilt, entgiftet',
                50: 'Meisterkoch: Aus Resten zaubert er Buff-Festmahle. Legendär!',
            },
            tasks: [
                { type: 'cook_meal', description: 'Koche Mahlzeit für Auftraggeber' },
                { type: 'supply_inn', description: 'Beliefere Gasthaus mit Essen' },
                { type: 'field_cooking', description: 'Koche für Reisegruppe unterwegs' },
                { type: 'banquet', description: 'Bereite Festmahl vor' },
            ],
        },

        fischer: {
            id: 'fischer', name: 'Fischer', icon: '🎣', category: 'natur',
            description: 'Fische in Flüssen, Seen und am Meer. Seltene Fische = Gold!',
            color: '#4682B4',
            levelEffects: {
                1:  'Kann mit Stock und Schnur fischen (langsam, kleine Fische)',
                10: 'Ordentliche Angel, weiß wo Fische sind',
                25: 'Seltene Fische fangen, kennt Geheimspots',
                40: 'Riesenfische, magische Fische, Schätze aus dem Wasser',
                50: 'Fischer-Legende: Kann alles aus dem Wasser ziehen. Sogar Artefakte.',
            },
            tasks: [
                { type: 'catch_fish', description: 'Fange bestimmte Fische' },
                { type: 'supply_market', description: 'Beliefere Fischmarkt' },
                { type: 'rare_catch', description: 'Fange seltenen Fisch' },
                { type: 'deep_sea', description: 'Tiefseefischen (gefährlich!)' },
            ],
        },

        gaertner: {
            id: 'gaertner', name: 'Gärtner / Bauer', icon: '🌾', category: 'natur',
            description: 'Pflanze an, ernte, züchte. Nahrung und seltene Pflanzen.',
            color: '#228B22',
            levelEffects: {
                1:  'Kann einfaches Gemüse anpflanzen (langsam, kleiner Ertrag)',
                10: 'Bessere Erträge, kennt Jahreszeiten',
                25: 'Seltene Pflanzen züchten, Heilkräuter anbauen',
                40: 'Magische Pflanzen, beschleunigtes Wachstum',
                50: 'Meistergärtner: Alles wächst. Überall. Sogar in der Wüste.',
            },
            tasks: [
                { type: 'plant_crops', description: 'Pflanze und ernte Feldfrüchte' },
                { type: 'grow_herbs', description: 'Züchte bestimmte Kräuter' },
                { type: 'supply_food', description: 'Beliefere Stadt mit Nahrung' },
                { type: 'rare_plant', description: 'Züchte seltene Pflanze' },
            ],
        },

        sammler: {
            id: 'sammler', name: 'Sammler / Kräuterkundler', icon: '🌿', category: 'natur',
            description: 'Finde Kräuter, Pilze, Beeren, Materialien in der Wildnis.',
            color: '#32CD32',
            levelEffects: {
                1:  'Erkennt grundlegende Kräuter (verwechselt giftige manchmal)',
                10: 'Sichere Erkennung, weiß wo was wächst',
                25: 'Findet seltene Materialien, doppelter Ertrag',
                40: 'Magische Kräuter erkennen, geheime Fundorte',
                50: 'Natur-Weise: Sieht ALLES. Jede Pflanze, jedes Material. 3x Ertrag.',
            },
            tasks: [
                { type: 'gather_herbs', description: 'Sammle bestimmte Kräuter' },
                { type: 'rare_material', description: 'Finde seltenes Material' },
                { type: 'biome_survey', description: 'Kartografiere Ressourcen' },
                { type: 'poison_antidote', description: 'Sammle Gegengift-Zutaten' },
            ],
        },

        holzfaeller: {
            id: 'holzfaeller', name: 'Holzfäller', icon: '🪓', category: 'natur',
            description: 'Fälle Bäume, sammle Holz. Grundmaterial für Baumeister und Schmiede.',
            color: '#8B6914',
            levelEffects: {
                1:  'Kann dünne Bäume fällen (langsam, viel Verschnitt)',
                10: 'Effizientes Fällen, kennt Holzarten',
                25: 'Riesenbäume fällen, seltene Hölzer erkennen',
                40: 'Magisches Holz ernten (Lebende Bäume!)',
                50: 'Meisterholzfäller: Ein Schlag, ein Baum. Perfektes Holz.',
            },
            tasks: [
                { type: 'chop_wood', description: 'Fälle Bäume und liefere Holz' },
                { type: 'rare_wood', description: 'Finde seltenes Holz (Eisenholz etc.)' },
                { type: 'clear_path', description: 'Räume Waldweg frei' },
                { type: 'supply_carpenter', description: 'Beliefere Zimmermann' },
            ],
        },

        minenarbeiter: {
            id: 'minenarbeiter', name: 'Minenarbeiter / Bergmann', icon: '⛏️', category: 'natur',
            description: 'Grabe nach Erzen, Kristallen, Edelsteinen. Tief unter der Erde.',
            color: '#708090',
            levelEffects: {
                1:  'Kann oberflächliche Erze abbauen (langsam)',
                10: 'Tiefere Adern finden, effizienterer Abbau',
                25: 'Seltene Erze und Kristalle, Gefahren erkennen',
                40: 'Magische Mineralien, geheime Adern',
                50: 'Meisterbergmann: Spürt Erze durch Stein. Legendäre Kristalle.',
            },
            tasks: [
                { type: 'mine_ore', description: 'Baue bestimmtes Erz ab' },
                { type: 'find_vein', description: 'Finde neue Erzader' },
                { type: 'crystal_mining', description: 'Baue Kristalle ab' },
                { type: 'deep_mining', description: 'Tiefenmine erkunden' },
            ],
        },

        jaeger: {
            id: 'jaeger', name: 'Jäger / Fallensteller', icon: '🏹', category: 'natur',
            description: 'Jage Wild, stelle Fallen, liefere Fleisch und Häute.',
            color: '#556B2F',
            levelEffects: {
                1:  'Kann Hasen und Vögel jagen (trifft selten)',
                10: 'Sichere Jagd, Fallen stellen, Fährten lesen',
                25: 'Großwild jagen, seltene Tiere aufspüren',
                40: 'Magische Kreaturen jagen, perfekte Häute',
                50: 'Meisterjäger: Jagt alles. Selbst Drakes fürchten ihn.',
            },
            tasks: [
                { type: 'hunt_game', description: 'Jage bestimmtes Wild' },
                { type: 'set_traps', description: 'Stelle Fallen auf' },
                { type: 'deliver_meat', description: 'Liefere Fleisch an Koch/Markt' },
                { type: 'rare_hunt', description: 'Jage seltenes Tier' },
            ],
        },

        // ========== HANDEL & WIRTSCHAFT ==========

        haendler: {
            id: 'haendler', name: 'Händler / Kaufmann', icon: '🏪', category: 'handel',
            description: 'Kaufe günstig, verkaufe teuer. Handelsrouten. Karawanen.',
            color: '#DAA520', planwagen: true,
            levelEffects: {
                1:  'Kann mit NPCs handeln (schlechte Preise)',
                10: 'Bessere Preise, erkennt Schnäppchen',
                25: 'Eigene Handelsrouten, Karawanen führen',
                40: 'Marktmanipulation, Monopole aufbauen',
                50: 'Handelsfürst: Kontrolliert Märkte. Könige verhandeln mit dir.',
            },
            tasks: [
                { type: 'trade_route', description: 'Kaufe in Biom A, verkaufe in Biom B' },
                { type: 'supply_run', description: 'Liefere Mangelware an Stadt' },
                { type: 'caravan_lead', description: 'Führe Handelskarawane' },
                { type: 'negotiate', description: 'Verhandle Handelsabkommen' },
            ],
        },

        gastwirt: {
            id: 'gastwirt', name: 'Gastwirt / Tavernenwirt', icon: '🍺', category: 'handel',
            description: 'Betreibe eine Taverne. Informationsquelle. Gilden-Auftragsboard.',
            color: '#CD853F',
            levelEffects: {
                1:  'Kann Getränke ausschenken (verschüttet die Hälfte)',
                10: 'Solider Service, hört Gerüchte',
                25: 'Gilden-Auftragsboard verwalten, beste Infos',
                40: 'Berühmte Taverne: NPCs kommen VON WEIT zu dir',
                50: 'Legendäre Taverne: DER Treffpunkt. Könige trinken hier.',
            },
            tasks: [
                { type: 'serve_guests', description: 'Bediene Gäste in der Taverne' },
                { type: 'gather_rumors', description: 'Sammle Gerüchte und Informationen' },
                { type: 'manage_board', description: 'Verwalte Gilden-Auftragsboard' },
                { type: 'host_event', description: 'Organisiere Event in der Taverne' },
            ],
        },

        // ========== SOZIAL & WISSEN ==========

        barde: {
            id: 'barde', name: 'Barde / Unterhalter', icon: '🎵', category: 'sozial',
            description: 'Musik und Geschichten. Buffs. Nachrichtennetzwerk.',
            color: '#9932CC',
            levelEffects: {
                1:  'Kann schief singen (NPCs gehen weg)',
                10: 'Ordentliche Lieder, kleine Buffs (+5%)',
                25: 'Inspirierende Musik: +15% Buffs, Massen begeistern',
                40: 'Magische Melodien: Heilen, stärken, Feinde verwirren',
                50: 'Legendärer Barde: Ein Lied und Armeen marschieren. Oder weinen.',
            },
            tasks: [
                { type: 'perform', description: 'Tritt auf für Gold und Buffs' },
                { type: 'spread_news', description: 'Verbreite Nachrichten' },
                { type: 'inspire_group', description: 'Buffe Gruppe vor Kampf' },
                { type: 'gather_stories', description: 'Sammle Geschichten für Lore' },
            ],
        },

        spion: {
            id: 'spion', name: 'Spion / Informant', icon: '🎭', category: 'sozial',
            description: 'Informationen sammeln. Infiltriere. Sabotiere.',
            color: '#483D8B',
            levelEffects: {
                1:  'Kann lauschen (wird oft erwischt)',
                10: 'Diskretes Beobachten, einfache Verkleidungen',
                25: 'Infiltration, Schlösser knacken, Geheimgänge finden',
                40: 'Meisterspion: Überall unerkannt, perfekte Tarnung',
                50: 'Schattenmeister: Unsichtbar. Weiß alles. Überall.',
            },
            tasks: [
                { type: 'gather_intel', description: 'Sammle Informationen über Ziel' },
                { type: 'infiltrate', description: 'Infiltriere Organisation' },
                { type: 'sabotage', description: 'Sabotiere feindliche Operation' },
                { type: 'lockpick', description: 'Knacke Schlösser und Tresore' },
            ],
        },

        heiler: {
            id: 'heiler', name: 'Heiler / Medikus', icon: '💊', category: 'wissen',
            description: 'Heile Verwundete. Braue Tränke. Rette Leben.',
            color: '#FF69B4',
            levelEffects: {
                1:  'Kann Wunden verbinden (schlecht, 50% Infektionsrisiko)',
                10: 'Ordentliche Heilung, einfache Tränke brauen',
                25: 'Gifte heilen, Knochen richten, starke Tränke',
                40: 'Magische Heilung, Wiederbelebung kleiner Wunden',
                50: 'Meisterheiler: Heilt fast alles. Kann vom Rand des Todes retten.',
            },
            tasks: [
                { type: 'heal_wounded', description: 'Heile verwundeten NPC' },
                { type: 'brew_potion', description: 'Braue Heiltrank' },
                { type: 'cure_poison', description: 'Heile vergiftete Person' },
                { type: 'field_medic', description: 'Medizinische Versorgung unterwegs' },
            ],
        },

        alchemist: {
            id: 'alchemist', name: 'Alchemist', icon: '⚗️', category: 'wissen',
            description: 'Transmutation. Elixiere. Bomben. Mysteriöse Substanzen.',
            color: '#9400D3',
            levelEffects: {
                1:  'Kann einfache Mischungen herstellen (explodieren manchmal)',
                10: 'Stabile Tränke, Grundlagen der Transmutation',
                25: 'Bomben, Gifte, Spezialelixiere',
                40: 'Magische Substanzen, temporäre Verwandlungen',
                50: 'Meisteralchemist: Kann fast alles transmutieren. Gold aus Blei? Fast.',
            },
            tasks: [
                { type: 'brew_elixir', description: 'Braue Spezialelixier' },
                { type: 'craft_bomb', description: 'Stelle Bomben her' },
                { type: 'transmute', description: 'Transmutiere Material' },
                { type: 'research', description: 'Erforsche neue Rezeptur' },
            ],
        },

        kartograph: {
            id: 'kartograph', name: 'Kartograph / Entdecker', icon: '🗺️', category: 'wissen',
            description: 'Kartografiere die Welt. Finde Geheimgänge. Entdecke Neues.',
            color: '#20B2AA',
            levelEffects: {
                1:  'Kann grobe Karten zeichnen (oft ungenau)',
                10: 'Zuverlässige Karten, Wegpunkte markieren',
                25: 'Geheime Orte finden, Dungeons kartografieren',
                40: 'Verborgene Eingänge entdecken, antike Karten lesen',
                50: 'Meisterentdecker: Kennt jeden Stein. Findet die Zeitstadt.',
            },
            tasks: [
                { type: 'map_region', description: 'Kartografiere unbekanntes Gebiet' },
                { type: 'find_secret', description: 'Finde geheimen Ort' },
                { type: 'map_dungeon', description: 'Kartografiere Dungeon' },
                { type: 'ancient_map', description: 'Entschlüssle antike Karte' },
            ],
        },

        gelehrter: {
            id: 'gelehrter', name: 'Gelehrter / Forscher', icon: '📚', category: 'wissen',
            description: 'Studiere die Welt. Lore. Geschichte. Runen. Magie-Theorie.',
            color: '#4B0082',
            levelEffects: {
                1:  'Kann einfache Texte lesen (versteht wenig)',
                10: 'Historische Zusammenhänge verstehen, alte Sprachen',
                25: 'Runen lesen, magische Texte entschlüsseln',
                40: 'Antikes Wissen, verborgene Lore entdecken',
                50: 'Allwissend: Kennt die Geschichte. Versteht die Götter. Weiß von der Zeitstadt.',
            },
            tasks: [
                { type: 'research_topic', description: 'Erforsche Thema für Auftraggeber' },
                { type: 'translate_runes', description: 'Übersetze Runen-Inschrift' },
                { type: 'write_book', description: 'Schreibe Wissens-Band' },
                { type: 'teach_npc', description: 'Unterrichte NPC' },
            ],
        },

        // ========== SPEZIAL ==========

        tiermeister: {
            id: 'tiermeister', name: 'Tiermeister / Zähmer', icon: '🐾', category: 'natur',
            description: 'Zähme Tiere. Züchte Begleiter. Reittiere und Kampfgefährten.',
            color: '#FF7F50',
            levelEffects: {
                1:  'Kann Hühner und Katzen streicheln (beißen manchmal)',
                10: 'Hunde zähmen, Pferde reiten',
                25: 'Wölfe, Bären zähmen, Zucht-Programme',
                40: 'Exotische Kreaturen zähmen (Drakes!)',
                50: 'Meisterzähmer: Sogar Nebel-Titanen gehorchen dir.',
            },
            tasks: [
                { type: 'tame_animal', description: 'Zähme bestimmtes Tier' },
                { type: 'breed_mount', description: 'Züchte Reittier' },
                { type: 'train_companion', description: 'Trainiere Kampfgefährten' },
                { type: 'exotic_capture', description: 'Fange exotische Kreatur' },
            ],
        },

        dieb: {
            id: 'dieb', name: 'Dieb / Taschendieb', icon: '🤏', category: 'sozial',
            description: 'Stehle. Plündere. Hehle. Riskant aber lukrativ.',
            color: '#2F4F4F',
            levelEffects: {
                1:  'Kann Taschen durchwühlen (wird fast immer erwischt)',
                10: 'Geschickter Taschendieb, einfache Schlösser',
                25: 'Tresore knacken, Wachen umgehen',
                40: 'Unerkannt stehlen, perfekte Hehler-Kontakte',
                50: 'Meisterdieb: Stiehlt was er will. Sogar unter Aufsicht.',
            },
            tasks: [
                { type: 'pickpocket', description: 'Bestehle Ziel-NPC' },
                { type: 'burglary', description: 'Einbruch in Gebäude' },
                { type: 'fence_goods', description: 'Hehle gestohlene Waren' },
                { type: 'heist', description: 'Großer Raub (Teamwork!)' },
            ],
        },

        brauer: {
            id: 'brauer', name: 'Brauer / Winzer', icon: '🍺', category: 'handwerk',
            description: 'Braue Bier, Wein, Met. Getränke mit Buff-Effekten.',
            color: '#B8860B',
            levelEffects: {
                1:  'Kann trübes Gebräu herstellen (schmeckt furchtbar)',
                10: 'Trinkbares Bier, einfacher Wein',
                25: 'Guter Met, Spezialgebräu mit leichten Buffs',
                40: 'Magische Getränke: Mut-Trunk, Kraft-Bier',
                50: 'Meisterbrauer: Legendäre Getränke. Könige bestellen bei dir.',
            },
            tasks: [
                { type: 'brew_beer', description: 'Braue Bier-Charge' },
                { type: 'wine_making', description: 'Stelle Wein her' },
                { type: 'special_brew', description: 'Braue Spezial-Getränk' },
                { type: 'supply_tavern', description: 'Beliefere Taverne' },
            ],
        },

        gerber: {
            id: 'gerber', name: 'Sattler / Gerüstbauer', icon: '🏗️', category: 'handwerk',
            description: 'Baue Gerüste, Leitern, Belagerungsgeräte. Praktisch überall nützlich.',
            color: '#A0522D',
            levelEffects: {
                1:  'Kann einfache Leitern zusammenbauen',
                10: 'Gerüste für Bauarbeiten, Seilbrücken',
                25: 'Belagerungstürme, Rammen',
                40: 'Komplexe Konstruktionen, Aufzüge',
                50: 'Meisterkonstrukteur: Baut alles. Überall.',
            },
            tasks: [
                { type: 'build_scaffolding', description: 'Errichte Gerüst' },
                { type: 'siege_equipment', description: 'Baue Belagerungsgerät' },
                { type: 'rope_bridge', description: 'Spanne Seilbrücke' },
                { type: 'construction_support', description: 'Unterstütze Bauprojekt' },
            ],
        },

        navigator: {
            id: 'navigator', name: 'Navigator / Fährmann', icon: '⛵', category: 'wissen',
            description: 'Navigiere Boote, finde Seerouten. Unverzichtbar am Salzwind.',
            color: '#1E90FF',
            levelEffects: {
                1:  'Kann ein Floß paddeln (dreht sich im Kreis)',
                10: 'Kleines Boot steuern, Küstennavigation',
                25: 'Segeln, Sturmnavigation, Geheime Buchten finden',
                40: 'Große Schiffe steuern, Unterwasser-Routen kennen',
                50: 'Meisternavigator: Überquert jeden Ozean. Findet jede Insel.',
            },
            tasks: [
                { type: 'ferry_passengers', description: 'Setze Passagiere über' },
                { type: 'sea_trade', description: 'Seehandelsroute befahren' },
                { type: 'explore_coast', description: 'Erforsche Küstenlinie' },
                { type: 'shipwreck_salvage', description: 'Bergung aus Schiffswrack' },
            ],
        },

        henker: {
            id: 'henker', name: 'Henker / Vollstrecker', icon: '⚖️', category: 'kampf',
            description: 'Das Gesetz durchsetzen. Urteile vollstrecken. Düster aber nötig.',
            color: '#1C1C1C',
            levelEffects: {
                1:  'Kann Gefangene bewachen',
                10: 'Verhöre durchführen, Geständnisse erlangen',
                25: 'Urteile vollstrecken, Flüchtlinge jagen',
                40: 'Gefürchtet: Kriminelle ergeben sich freiwillig',
                50: 'Oberster Vollstrecker: Das wandelnde Gesetz.',
            },
            tasks: [
                { type: 'guard_prisoner', description: 'Bewache Gefangenen' },
                { type: 'interrogate', description: 'Verhöre Verdächtigen' },
                { type: 'execute_sentence', description: 'Vollstrecke Urteil' },
                { type: 'hunt_criminal', description: 'Jage Flüchtigen' },
            ],
        },

        diplomat: {
            id: 'diplomat', name: 'Diplomat / Gesandter', icon: '🤝', category: 'sozial',
            description: 'Verhandle zwischen Städten, Fraktionen, Königreichen.',
            color: '#FFD700',
            levelEffects: {
                1:  'Kann höflich grüßen (mehr nicht)',
                10: 'Einfache Verhandlungen, Konflikte schlichten',
                25: 'Handelsabkommen, Bündnisse vermitteln',
                40: 'Kriege verhindern, Friedensverträge aushandeln',
                50: 'Meisterdiplomat: Bringt Feinde an einen Tisch. Könige hören auf dich.',
            },
            tasks: [
                { type: 'negotiate', description: 'Verhandle zwischen Parteien' },
                { type: 'peace_treaty', description: 'Vermittle Frieden' },
                { type: 'trade_agreement', description: 'Handelsabkommen ausarbeiten' },
                { type: 'ambassador', description: 'Vertrete Stadt als Gesandter' },
            ],
        },
    };

    // ==========================================
    // CAREER CATEGORIES
    // ==========================================

    const CAREER_CATEGORIES = {
        kampf:    { name: 'Kampf & Schutz', icon: '⚔️', color: '#B22222' },
        handwerk: { name: 'Handwerk',       icon: '🔨', color: '#FF6347' },
        natur:    { name: 'Natur & Ernte',  icon: '🌿', color: '#228B22' },
        handel:   { name: 'Handel',         icon: '💰', color: '#DAA520' },
        sozial:   { name: 'Sozial',         icon: '🎭', color: '#9932CC' },
        wissen:   { name: 'Wissen',         icon: '📚', color: '#4B0082' },
    };

    // ==========================================
    // PLAYER CAREER STATE
    // ==========================================

    let careerState = loadCareerState();

    function loadCareerState() {
        try {
            return JSON.parse(localStorage.getItem('najika_careers') || 'null') || {
                activeCareers: [],
                careerData: {},     // Pro Beruf: { level, xp, completedTasks }
                totalXP: 0,
                careerHistory: [],
            };
        } catch { return { activeCareers: [], careerData: {}, totalXP: 0, careerHistory: [] }; }
    }

    function saveCareerState() {
        localStorage.setItem('najika_careers', JSON.stringify(careerState));
    }

    // ==========================================
    // CAREER MANAGEMENT
    // ==========================================

    function joinCareer(careerId) {
        if (!CAREERS[careerId]) {
            console.error(`❌ Beruf nicht gefunden: ${careerId}`);
            return false;
        }

        if (careerState.activeCareers.includes(careerId)) {
            console.warn(`⚠️ Du bist bereits ${CAREERS[careerId].name}!`);
            return false;
        }

        const career = CAREERS[careerId];
        careerState.activeCareers.push(careerId);
        careerState.careerData[careerId] = careerState.careerData[careerId] || {
            level: 1,
            xp: 0,
            completedTasks: 0,
            joinedAt: Date.now(),
        };

        saveCareerState();

        console.log(`🎉 Beruf beigetreten: ${career.icon} ${career.name}!`);
        if (typeof notify === 'function') {
            notify(`${career.icon} Du bist jetzt ${career.name}! (Lvl ${careerState.careerData[careerId].level})`, 'success');
        }

        // Postman-System synchronisieren
        if (careerId === 'postman' && window.PostmanSystem) {
            PostmanSystem.becomePostman();
        }

        return true;
    }

    function leaveCareer(careerId) {
        const idx = careerState.activeCareers.indexOf(careerId);
        if (idx === -1) return false;

        const career = CAREERS[careerId];
        careerState.activeCareers.splice(idx, 1);
        // Daten bleiben! Kann jederzeit wieder beitreten auf gleichem Level!
        saveCareerState();

        console.log(`📤 Beruf pausiert: ${career.icon} ${career.name} (Lvl bleibt!)`);
        if (typeof notify === 'function') {
            notify(`${career.icon} ${career.name} pausiert. Dein Level bleibt gespeichert!`, 'info');
        }
        return true;
    }

    // LEARNING BY DOING: XP durch Ausüben!
    function addCareerXP(careerId, xp) {
        const data = careerState.careerData[careerId];
        if (!data) return;

        data.xp += xp;

        // Level-Up Check
        while (data.level < 50) {
            const needed = xpForLevel(data.level + 1);
            if (data.xp >= needed) {
                data.xp -= needed;
                data.level++;
                const career = CAREERS[careerId];
                console.log(`⬆️ ${career.icon} ${career.name} Level ${data.level}!`);

                // Milestone-Effekte anzeigen
                const milestone = career.levelEffects[data.level];
                if (milestone && typeof notify === 'function') {
                    notify(`⬆️ ${career.icon} Lvl ${data.level}: ${milestone}`, 'success');
                }
            } else {
                break;
            }
        }

        careerState.totalXP += xp;
        saveCareerState();
    }

    function completeCareerTask(careerId, taskResult) {
        const data = careerState.careerData[careerId];
        if (!data) return null;

        data.completedTasks++;
        const difficulty = taskResult?.difficulty || 1;
        const baseXP = 15 + difficulty * 12;
        addCareerXP(careerId, baseXP);

        return { xp: baseXP, newLevel: data.level };
    }

    // ==========================================
    // TASK GENERATION
    // ==========================================

    function generateTask(careerId, biome) {
        const career = CAREERS[careerId];
        if (!career || !career.tasks) return null;

        const taskTemplate = career.tasks[Math.floor(Math.random() * career.tasks.length)];
        const data = careerState.careerData[careerId];
        const level = data ? data.level : 1;

        const difficulty = Math.max(1, Math.floor(level / 5) + Math.floor(Math.random() * 3));
        const effectiveness = calcEffectiveness(level);
        const basePay = 30 + difficulty * 25;

        return {
            careerId,
            type: taskTemplate.type,
            description: taskTemplate.description,
            biome: biome || 'reich_der_drei',
            difficulty,
            pay: Math.floor(basePay * effectiveness),
            xpReward: 15 + difficulty * 12,
            playerLevel: level,
            effectiveness,
            status: 'available',
            createdAt: Date.now(),
        };
    }

    // ==========================================
    // GETTERS
    // ==========================================

    function getActiveCareers() {
        return careerState.activeCareers.map(id => ({
            ...CAREERS[id],
            data: careerState.careerData[id],
            effectiveness: calcEffectiveness(careerState.careerData[id]?.level || 1),
        }));
    }

    function getCareerInfo(careerId) {
        const career = CAREERS[careerId];
        if (!career) return null;
        const data = careerState.careerData[careerId];
        return {
            ...career,
            data: data || null,
            isActive: careerState.activeCareers.includes(careerId),
            effectiveness: calcEffectiveness(data?.level || 1),
            nextLevelXP: data ? xpForLevel(data.level + 1) : xpForLevel(2),
        };
    }

    function getAllCareers() {
        return Object.entries(CAREERS).map(([id, career]) => ({
            id,
            ...career,
            data: careerState.careerData[id] || null,
            isActive: careerState.activeCareers.includes(id),
        }));
    }

    function getCareersByCategory(category) {
        return Object.entries(CAREERS)
            .filter(([, c]) => c.category === category)
            .map(([id, c]) => ({ id, ...c, data: careerState.careerData[id] || null }));
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.CareerSystem = {
        CAREERS,
        CAREER_CATEGORIES,

        // Learning by Doing
        calcEffectiveness,
        xpForLevel,
        totalXPForLevel,

        // Management
        joinCareer,
        leaveCareer,
        addCareerXP,
        completeCareerTask,
        generateTask,

        // Getters
        getActiveCareers,
        getCareerInfo,
        getAllCareers,
        getCareersByCategory,
        getState: () => ({ ...careerState }),

        saveCareerState,
    };

    const count = Object.keys(CAREERS).length;
    const cats = Object.keys(CAREER_CATEGORIES).length;
    console.log(`🎭 Career-System: ${count} Berufspfade in ${cats} Kategorien geladen`);
    console.log(`📊 Learning by Doing: Lvl 1 = 1.0x | Lvl 25 = 1.96x | Lvl 50 = 2.96x Effektivität`);
    if (careerState.activeCareers.length > 0) {
        const active = careerState.activeCareers.map(id => {
            const c = CAREERS[id];
            const d = careerState.careerData[id];
            return `${c?.icon} ${c?.name} Lvl${d?.level || 1}`;
        }).join(', ');
        console.log(`📋 Aktive Berufe: ${active}`);
    }

})();
