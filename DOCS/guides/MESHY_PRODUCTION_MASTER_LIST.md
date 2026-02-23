# 🎨 MESHY AI PRODUCTION MASTER LIST
## Najika World - Complete Asset Production Guide

**Format:** Jedes Asset hat:
- **Name/ID** (Platzhalter für Meshy)
- **Beschreibung** (Prompt-Basis)
- **Animations** (falls beweglich/kämpfbar)
- **Priority** (1-3)

---

## 📐 ANIMATION REQUIREMENTS

### KAMPF-TIERE/MONSTER (Combat-Ready):
**Benötigte Animations:**
- `idle` - Steht herum, atmet
- `walk` - Normale Bewegung
- `run` - Schnelle Bewegung
- `attack_1` - Basis-Angriff (Biss, Kratzen, Schlag)
- `attack_2` - Spezial-Angriff (Element, Skill)
- `hit` - Wird getroffen, reagiert
- `die` - Stirbt, fällt um
- `victory` - Gewinnt, jubelt

### SLIMES (Companion-System):
**Benötigte Animations:**
- `idle` - Wackelt leicht
- `hop` - Hüpf-Bewegung (wie Slime)
- `attack` - Ramm-Attacke
- `cheer` - Anfeuern (Digimon-Style)
- `happy` - Freude (nach Sieg)
- `sad` - Traurig (nach Niederlage)
- `evolve` - Evolution-Animation (Shell→Slime→Rainbow)

### NPCs (Quest-Geber, Händler):
**Benötigte Animations:**
- `idle` - Steht, wartet
- `talk` - Redet (Arm-Gesten)
- `walk` - Geht herum (Patrol)
- `point` - Zeigt auf etwas
- `trade` - Gibt Item (Handel)

### GEBÄUDE (Static/Animated):
- **Static:** Keine Animation
- **Animated:** Türen öffnen, Fahnen wehen, Feuer flackert

---

# 🔴 PRIORITY 1 - MVP CORE ASSETS

---

## 🌲 GENERIC REUSABLE NATURE PACK (überall nutzbar)

### TREES_PACK_001
**Name:** `generic_tree_oak`
**Beschreibung:** Fantasy Oak tree, medium size, thick trunk, lush green leaves, stylized low-poly fantasy style, suitable for various biomes
**Animations:** Static (wind sway optional)
**Varianten:** 3 (klein, mittel, groß)
**Priority:** 1

### TREES_PACK_002
**Name:** `generic_tree_pine`
**Beschreibung:** Pine tree, tall conical shape, dark green needles, fantasy forest style, adaptable for multiple regions
**Animations:** Static
**Varianten:** 3
**Priority:** 1

### TREES_PACK_003
**Name:** `generic_tree_dead`
**Beschreibung:** Dead tree, bare branches, dark bark, spooky fantasy style, usable in swamp/dark areas
**Animations:** Static
**Varianten:** 2
**Priority:** 1

### TREES_PACK_004
**Name:** `generic_tree_palm`
**Beschreibung:** Palm tree, tropical style, long leaves, sandy brown trunk, desert/coast suitable
**Animations:** Static (leaves sway)
**Varianten:** 2
**Priority:** 1

### TREES_PACK_005
**Name:** `generic_tree_willow`
**Beschreibung:** Weeping willow, drooping branches, mystical fantasy style, magical forest aesthetic
**Animations:** Static
**Varianten:** 2
**Priority:** 1

---

### ROCKS_PACK_001
**Name:** `rock_boulder_generic`
**Beschreibung:** Large boulder, gray stone, weathered texture, fantasy realistic, multiple biomes
**Animations:** Static
**Varianten:** 5 (verschiedene Größen/Formen)
**Priority:** 1

### ROCKS_PACK_002
**Name:** `rock_cliff_face`
**Beschreibung:** Cliff face section, vertical rock wall, modular, stackable for mountains
**Animations:** Static
**Varianten:** 3
**Priority:** 1

### ROCKS_PACK_003
**Name:** `rock_crystal_formation`
**Beschreibung:** Crystal rock formation, glowing edges, magical fantasy style, mountain/cave use
**Animations:** Static (glow effect)
**Varianten:** 3
**Priority:** 2

---

### GROUND_COVER_001
**Name:** `grass_patch_generic`
**Beschreibung:** Grass patch, low poly, green, fantasy style, ground cover for plains/forest
**Animations:** Static (wind sway optional)
**Varianten:** 5
**Priority:** 1

### GROUND_COVER_002
**Name:** `bush_generic`
**Beschreibung:** Small bush, round shape, green leaves, fantasy style, filler vegetation
**Animations:** Static
**Varianten:** 3
**Priority:** 1

### GROUND_COVER_003
**Name:** `flower_patch_wild`
**Beschreibung:** Wildflower patch, colorful, fantasy style, decorative ground cover
**Animations:** Static
**Varianten:** 3 (verschiedene Farben)
**Priority:** 2

---

## 🏗️ MODULAR BUILDING SYSTEM (Western-Fantasy Mix)

### BUILDING_MODULE_001
**Name:** `wall_wooden_western`
**Beschreibung:** Wooden wall panel, western style, weathered planks, modular building piece
**Animations:** Static
**Varianten:** 3 (gerade, Ecke, Fenster)
**Priority:** 1

### BUILDING_MODULE_002
**Name:** `roof_wooden_western`
**Beschreibung:** Wooden roof piece, western style shingles, angled, modular
**Animations:** Static
**Varianten:** 4 (gerade, Ecke, Giebel, Dach-Spitze)
**Priority:** 1

### BUILDING_MODULE_003
**Name:** `door_western_saloon`
**Beschreibung:** Saloon-style swinging doors, western fantasy, wooden, functional
**Animations:** Door_swing (öffnen/schließen)
**Varianten:** 2
**Priority:** 1

### BUILDING_MODULE_004
**Name:** `window_western_shutters`
**Beschreibung:** Western window with shutters, wooden frame, glass pane, fantasy style
**Animations:** Shutter_open (optional)
**Varianten:** 2
**Priority:** 1

### BUILDING_MODULE_005
**Name:** `foundation_stone`
**Beschreibung:** Stone foundation block, gray stone, modular base for buildings
**Animations:** Static
**Varianten:** 2
**Priority:** 1

### BUILDING_MODULE_006
**Name:** `pillar_wooden_support`
**Beschreibung:** Wooden support pillar, western style, vertical beam for structures
**Animations:** Static
**Varianten:** 2 (kurz, lang)
**Priority:** 1

### BUILDING_MODULE_007
**Name:** `balcony_western`
**Beschreibung:** Western-style balcony with railing, second floor extension
**Animations:** Static
**Varianten:** 2
**Priority:** 2

---

## 🏔️ GÖTTERFELS ZENTRUM (Berg-Zentrum der Map)

### GOETTERFELS_001
**Name:** `schwarze_muehle_exterior`
**Beschreibung:** Large black windmill, gothic fantasy style, 4 floors visible, stone/dark wood, iconic safe zone building, mystical aura, western-gothic fusion
**Animations:** Windmill_blades_rotate (langsam)
**Varianten:** 1 (unique)
**Priority:** 1
**Note:** Interior (12 Räume) später separat

### GOETTERFELS_002
**Name:** `village_house_alpine_small`
**Beschreibung:** Small alpine house, stone base, wooden upper floor, slanted roof, mountain village style
**Animations:** Static, door_open
**Varianten:** 3
**Priority:** 1

### GOETTERFELS_003
**Name:** `village_house_alpine_medium`
**Beschreibung:** Medium alpine house, two floors, stone and wood, cozy mountain home
**Animations:** Static, door_open
**Varianten:** 2
**Priority:** 1

### GOETTERFELS_004
**Name:** `stone_bridge_mountain`
**Beschreibung:** Stone bridge, arched, spans river/ravine, fantasy medieval style
**Animations:** Static
**Varianten:** 2 (kurz, lang)
**Priority:** 1

### GOETTERFELS_005
**Name:** `river_section_flowing`
**Beschreibung:** River water section, flowing animation, clear water, rocks in stream
**Animations:** Water_flow (animated texture)
**Varianten:** 3 (gerade, Kurve, Wasserfall)
**Priority:** 1

### GOETTERFELS_006
**Name:** `mountain_path_stone`
**Beschreibung:** Stone path/steps, mountain trail, weathered, winds up slopes
**Animations:** Static
**Varianten:** 4 (gerade, Kurve, Stufen, Rampe)
**Priority:** 1

### GOETTERFELS_007
**Name:** `lantern_post_gothic`
**Beschreibung:** Gothic lantern post, black iron, glowing light, mystical atmosphere
**Animations:** Light_flicker
**Varianten:** 2 (stehend, hängend)
**Priority:** 2

---

## 🏜️ HANDELSFESTE - CAPITAL CITY (Wüsten-Western Hauptstadt)

### HANDELSFESTE_001
**Name:** `pvp_arena_colosseum`
**Beschreibung:** Large PVP arena building, western-colosseum fusion, sandstone structure, circular/octagonal, tiered seating, grand entrance gates, desert architecture with western saloon elements, imposing and iconic
**Animations:** Static (flags wave)
**Varianten:** 1 (unique, sehr wichtig!)
**Priority:** 1

### HANDELSFESTE_002
**Name:** `slime_arena_building`
**Beschreibung:** Small arena building next to PVP arena, square structure, sandstone western style, single entrance, compact turn-based battle arena, desert-western architecture
**Animations:** Static, door_open
**Varianten:** 1 (unique)
**Priority:** 1

### HANDELSFESTE_003
**Name:** `city_gate_handelsfeste`
**Beschreibung:** Massive city gate, western-fantasy style, sandstone pillars, wooden reinforced gates, "Handelsfeste" carved above, desert capital entrance
**Animations:** Gate_open_slow
**Varianten:** 1 (unique)
**Priority:** 1

### HANDELSFESTE_004
**Name:** `trading_hub_market_center`
**Beschreibung:** Central trading hub building, large covered marketplace, sandstone pillars, canvas roofs, multiple stalls inside, western bazaar style
**Animations:** Static, canvas_flap (wind)
**Varianten:** 1 (unique)
**Priority:** 1

### HANDELSFESTE_005
**Name:** `player_shop_small`
**Beschreibung:** Small player shop, 1-story western building, sandstone/wood, desert style, shopfront with display window
**Animations:** Static, door_open
**Varianten:** 3 (verschiedene Fassaden)
**Priority:** 1

### HANDELSFESTE_006
**Name:** `player_shop_medium`
**Beschreibung:** Medium player shop, 2-story western building, balcony, larger footprint, desert capital style
**Animations:** Static, door_open
**Varianten:** 2
**Priority:** 1

### HANDELSFESTE_007
**Name:** `player_shop_large`
**Beschreibung:** Large player shop, 2-3 stories, corner building, premium location design, desert western architecture
**Animations:** Static, door_open, window_shutters
**Varianten:** 1
**Priority:** 2

### HANDELSFESTE_008
**Name:** `saloon_tavern`
**Beschreibung:** Western saloon tavern, 2 floors, swinging doors, balcony, "Taverne" sign, iconic western design with fantasy touches
**Animations:** Door_swing, piano_sound (ambient)
**Varianten:** 1 (unique)
**Priority:** 1

### HANDELSFESTE_009
**Name:** `residence_house_tier1`
**Beschreibung:** Basic residential house, 1-story, sandstone, simple western home, desert city dwelling
**Animations:** Static, door_open
**Varianten:** 4 (oft wiederholt in Stadt)
**Priority:** 1

### HANDELSFESTE_010
**Name:** `residence_house_tier2`
**Beschreibung:** Better residential house, 2-story, decorative elements, desert western middle-class
**Animations:** Static, door_open
**Varianten:** 3
**Priority:** 1

### HANDELSFESTE_011
**Name:** `residence_house_tier3`
**Beschreibung:** Luxury residential house, 2-story, balcony, ornate details, wealthy district design
**Animations:** Static, door_open, fountain (if garden)
**Varianten:** 2
**Priority:** 2

### HANDELSFESTE_012
**Name:** `blacksmith_forge_desert`
**Beschreibung:** Blacksmith building, open forge front, anvil visible, chimney smoke, western-desert style
**Animations:** Fire_flicker, smoke_rise, hammer_sound (ambient)
**Varianten:** 1
**Priority:** 1

### HANDELSFESTE_013
**Name:** `bank_treasury_building`
**Beschreibung:** Bank/treasury, solid stone building, reinforced doors, western frontier bank style, secure appearance
**Animations:** Static, vault_door (special)
**Varianten:** 1
**Priority:** 2

### HANDELSFESTE_014
**Name:** `stable_building`
**Beschreibung:** Stables, open structure, horse/mount stalls, hay storage, western ranch style
**Animations:** Static, door_open, animals_idle
**Varianten:** 1
**Priority:** 2

### HANDELSFESTE_015
**Name:** `fountain_oasis_center`
**Beschreibung:** Central fountain/oasis, sandstone basin, water feature, desert city centerpiece
**Animations:** Water_flow, splash
**Varianten:** 1 (unique)
**Priority:** 1

### HANDELSFESTE_016
**Name:** `market_stall_small`
**Beschreibung:** Small market stall, canvas roof, wooden frame, vendor stand, repeatable
**Animations:** Canvas_flap
**Varianten:** 5 (verschiedene Waren-Typen)
**Priority:** 1

### HANDELSFESTE_017
**Name:** `street_lamp_desert`
**Beschreibung:** Desert street lamp, metal/wood post, lantern top, western city lighting
**Animations:** Light_glow
**Varianten:** 2
**Priority:** 1

### HANDELSFESTE_018
**Name:** `wooden_fence_western`
**Beschreibung:** Western wooden fence, weathered, separates areas, classic frontier style
**Animations:** Static
**Varianten:** 3 (gerade, Ecke, Tor)
**Priority:** 1

### HANDELSFESTE_019
**Name:** `cactus_desert_large`
**Beschreibung:** Large saguaro cactus, desert decoration, iconic western plant
**Animations:** Static
**Varianten:** 3
**Priority:** 1

### HANDELSFESTE_020
**Name:** `cactus_desert_small`
**Beschreibung:** Small barrel cactus, ground decoration, desert filler
**Animations:** Static
**Varianten:** 2
**Priority:** 1

### HANDELSFESTE_021
**Name:** `banner_flag_handelsfeste`
**Beschreibung:** City banner/flag, "Handelsfeste" emblem, hangs from buildings, capital city pride
**Animations:** Flag_wave
**Varianten:** 2 (hängend, stehend)
**Priority:** 2

### HANDELSFESTE_022
**Name:** `water_barrel_wooden`
**Beschreibung:** Wooden water barrel, western prop, street decoration, functional look
**Animations:** Static
**Varianten:** 2
**Priority:** 2

### HANDELSFESTE_023
**Name:** `crate_wooden_cargo`
**Beschreibung:** Wooden cargo crate, stackable, western shipping, market prop
**Animations:** Static
**Varianten:** 3
**Priority:** 1

---

## 🎨 SLIME COMPANIONS (9 Colors × 3 Stages = 27 Models)

**ANIMATION SET (alle Slimes):**
- `idle` - Wackelt, atmet
- `hop` - Hüpf-Bewegung
- `attack` - Ramm-Attacke
- `cheer` - Anfeuern (Digimon-Style, Arme hoch)
- `happy` - Freut sich (bounce)
- `sad` - Traurig (sackt zusammen)
- `evolve` - Evolution (Leuchten, größer werden)

---

### SLIME_STAGE_1 (Shell/Egg Form)

#### SLIME_001_SHELL
**Name:** `slime_egg_ice_blue`
**Beschreibung:** Slime egg, shell form, icy blue color (#00aaff), smooth surface, fantasy egg design, small
**Animations:** idle (leichtes Wackeln)
**Region:** Samtmoos-Tiefwald
**Priority:** 1

#### SLIME_002_SHELL
**Name:** `slime_egg_mountain_gray`
**Beschreibung:** Slime egg, shell form, mountain gray color (#888888), stone-like texture
**Animations:** idle
**Region:** Reich der Drei
**Priority:** 1

#### SLIME_003_SHELL
**Name:** `slime_egg_ocean_turquoise`
**Beschreibung:** Slime egg, shell form, ocean turquoise (#00dddd), smooth with water shimmer
**Animations:** idle
**Region:** Salzwind-Küste
**Priority:** 1

#### SLIME_004_SHELL
**Name:** `slime_egg_electric_yellow`
**Beschreibung:** Slime egg, shell form, electric yellow (#ffff00), slight glow effect
**Animations:** idle (spark effect optional)
**Region:** Blitzebene
**Priority:** 1

#### SLIME_005_SHELL
**Name:** `slime_egg_swamp_green`
**Beschreibung:** Slime egg, shell form, swamp green (#00ff00), toxic/murky appearance
**Animations:** idle
**Region:** Grünschlamm-Sumpf
**Priority:** 1

#### SLIME_006_SHELL
**Name:** `slime_egg_magma_red`
**Beschreibung:** Slime egg, shell form, magma red (#ff0000), hot glow, ember cracks
**Animations:** idle (glow pulse)
**Region:** Magmaströme
**Priority:** 1

#### SLIME_007_SHELL
**Name:** `slime_egg_desert_orange`
**Beschreibung:** Slime egg, shell form, desert orange (#ff8800), sandy texture
**Animations:** idle
**Region:** Heiße Dünen
**Priority:** 1

#### SLIME_008_SHELL
**Name:** `slime_egg_heaven_purple`
**Beschreibung:** Slime egg, shell form, heaven purple (#aa00ff), ethereal glow
**Animations:** idle (shimmer)
**Region:** Götterfels
**Priority:** 1

#### SLIME_009_SHELL
**Name:** `slime_egg_cave_black`
**Beschreibung:** Slime egg, shell form, cave black (#444444), dark matte surface
**Animations:** idle
**Region:** Tiefenhöhlen
**Priority:** 1

---

### SLIME_STAGE_2 (Basic Slime Form)

#### SLIME_001_BASIC
**Name:** `slime_basic_ice_blue`
**Beschreibung:** Basic slime form, cute blob shape, large eyes, icy blue (#00aaff), classic Dragon Quest slime style, friendly face
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Samtmoos-Tiefwald
**Priority:** 1

#### SLIME_002_BASIC
**Name:** `slime_basic_mountain_gray`
**Beschreibung:** Basic slime, gray (#888888), rocky texture, cute face
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Reich der Drei
**Priority:** 1

#### SLIME_003_BASIC
**Name:** `slime_basic_ocean_turquoise`
**Beschreibung:** Basic slime, turquoise (#00dddd), water droplet aesthetic, cute
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Salzwind-Küste
**Priority:** 1

#### SLIME_004_BASIC
**Name:** `slime_basic_electric_yellow`
**Beschreibung:** Basic slime, electric yellow (#ffff00), spark effects, energetic face
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Blitzebene
**Priority:** 1

#### SLIME_005_BASIC
**Name:** `slime_basic_swamp_green`
**Beschreibung:** Basic slime, swamp green (#00ff00), toxic bubbles, mischievous face
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Grünschlamm-Sumpf
**Priority:** 1

#### SLIME_006_BASIC
**Name:** `slime_basic_magma_red`
**Beschreibung:** Basic slime, magma red (#ff0000), ember glow, fiery expression
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Magmaströme
**Priority:** 1

#### SLIME_007_BASIC
**Name:** `slime_basic_desert_orange`
**Beschreibung:** Basic slime, desert orange (#ff8800), sandy texture, cheerful face
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Heiße Dünen
**Priority:** 1

#### SLIME_008_BASIC
**Name:** `slime_basic_heaven_purple`
**Beschreibung:** Basic slime, heaven purple (#aa00ff), ethereal glow, angelic face
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Götterfels
**Priority:** 1

#### SLIME_009_BASIC
**Name:** `slime_basic_cave_black`
**Beschreibung:** Basic slime, cave black (#444444), shadow aura, mysterious face
**Animations:** idle, hop, attack, cheer, happy, sad
**Region:** Tiefenhöhlen
**Priority:** 1

---

### SLIME_STAGE_3 (Rainbow Final Form)

#### SLIME_001_RAINBOW
**Name:** `slime_rainbow_ice_origin`
**Beschreibung:** Rainbow slime final form, larger than basic, rainbow gradient colors shifting, icy blue base tones, majestic appearance, glowing eyes, crown or aura detail
**Animations:** idle, hop, attack, cheer, happy, sad, evolve (transformation)
**Region:** Samtmoos-Tiefwald (evolved)
**Priority:** 1

#### SLIME_002_RAINBOW
**Name:** `slime_rainbow_mountain_origin`
**Beschreibung:** Rainbow slime, gray base tones, rainbow shimmer, crystal details
**Animations:** Full set + evolve
**Region:** Reich der Drei (evolved)
**Priority:** 1

#### SLIME_003_RAINBOW
**Name:** `slime_rainbow_ocean_origin`
**Beschreibung:** Rainbow slime, turquoise base, water sparkle rainbow effect
**Animations:** Full set + evolve
**Region:** Salzwind-Küste (evolved)
**Priority:** 1

#### SLIME_004_RAINBOW
**Name:** `slime_rainbow_electric_origin`
**Beschreibung:** Rainbow slime, yellow base, electric arc rainbow trails
**Animations:** Full set + evolve
**Region:** Blitzebene (evolved)
**Priority:** 1

#### SLIME_005_RAINBOW
**Name:** `slime_rainbow_swamp_origin`
**Beschreibung:** Rainbow slime, green base, toxic rainbow glow
**Animations:** Full set + evolve
**Region:** Grünschlamm-Sumpf (evolved)
**Priority:** 1

#### SLIME_006_RAINBOW
**Name:** `slime_rainbow_magma_origin`
**Beschreibung:** Rainbow slime, red base, flame rainbow aura
**Animations:** Full set + evolve
**Region:** Magmaströme (evolved)
**Priority:** 1

#### SLIME_007_RAINBOW
**Name:** `slime_rainbow_desert_origin`
**Beschreibung:** Rainbow slime, orange base, sand sparkle rainbow effect
**Animations:** Full set + evolve
**Region:** Heiße Dünen (evolved)
**Priority:** 1

#### SLIME_008_RAINBOW
**Name:** `slime_rainbow_heaven_origin`
**Beschreibung:** Rainbow slime, purple base, divine rainbow halo
**Animations:** Full set + evolve
**Region:** Götterfels (evolved)
**Priority:** 1

#### SLIME_009_RAINBOW
**Name:** `slime_rainbow_cave_origin`
**Beschreibung:** Rainbow slime, black base, shadow rainbow contrasts
**Animations:** Full set + evolve
**Region:** Tiefenhöhlen (evolved)
**Priority:** 1

---

# 🟡 PRIORITY 2 - REGION SPECIFIC ASSETS

---

## 🌲 SAMTMOOS-TIEFWALD (Mystischer Wald)

### REGION BUILDINGS:

#### SAMTMOOS_BUILD_001
**Name:** `dampf_hain_onsen_building`
**Beschreibung:** Onsen hot spring building, Japanese-fantasy fusion, wooden structure, steam rising, mystical forest aesthetic
**Animations:** Steam_rise (constant)
**Varianten:** 1
**Priority:** 2

#### SAMTMOOS_BUILD_002
**Name:** `dampf_hain_restaurant`
**Beschreibung:** Forest restaurant, wooden structure, cozy, fantasy steamed buns theme, lanterns
**Animations:** Static, door_open, lantern_glow
**Varianten:** 1
**Priority:** 2

#### SAMTMOOS_BUILD_003
**Name:** `druid_circle_stone_ring`
**Beschreibung:** Druid stone circle, ancient stones arranged in circle, mystical runes glowing, forest ritual site
**Animations:** Rune_glow (pulse)
**Varianten:** 1
**Priority:** 2

#### SAMTMOOS_BUILD_004
**Name:** `forest_house_basic`
**Beschreibung:** Basic forest dwelling, wood and moss, integrated into trees, fantasy cottage
**Animations:** Static, door_open
**Varianten:** 3
**Priority:** 2

---

### NATURE ASSETS:

#### SAMTMOOS_NATURE_001
**Name:** `glowing_mushroom_large`
**Beschreibung:** Large glowing mushroom, bioluminescent blue/green, mystical forest feature, fantasy size
**Animations:** Glow_pulse
**Varianten:** 3
**Priority:** 2

#### SAMTMOOS_NATURE_002
**Name:** `mystical_tree_ancient`
**Beschreibung:** Ancient mystical tree, huge trunk, glowing veins, face in bark (optional), magical aura
**Animations:** Leaves_sway, glow_pulse
**Varianten:** 2
**Priority:** 2

#### SAMTMOOS_NATURE_003
**Name:** `moss_covered_rock`
**Beschreibung:** Large rock covered in thick green moss, forest floor element
**Animations:** Static
**Varianten:** 3
**Priority:** 2

#### SAMTMOOS_NATURE_004
**Name:** `forest_fern_cluster`
**Beschreibung:** Cluster of ferns, lush green, forest undergrowth
**Animations:** Static (sway optional)
**Varianten:** 2
**Priority:** 2

#### SAMTMOOS_NATURE_005
**Name:** `fog_wisp_particle`
**Beschreibung:** Fog/mist effect, particle system base model, mystical atmosphere
**Animations:** Float_drift
**Varianten:** 1
**Priority:** 2

---

### TIERE (Combat-Ready):

#### SAMTMOOS_TIER_001
**Name:** `mooshorn_deer`
**Beschreibung:** Deer with moss-covered antlers, forest green tones, peaceful but strong, fantasy forest creature
**Animations:** idle, walk, run, attack_1 (antler charge), attack_2 (stomp), hit, die, victory
**Priority:** 2

#### SAMTMOOS_TIER_002
**Name:** `mushroom_owl`
**Beschreibung:** Owl with mushroom patterns on feathers, wise appearance, forest magic creature
**Animations:** idle, walk (hop), run (fly), attack_1 (peck), attack_2 (wing gust), hit, die, victory
**Priority:** 2

#### SAMTMOOS_TIER_003
**Name:** `tree_root_snake`
**Beschreibung:** Snake made of tree roots/vines, green-brown, mystical forest serpent
**Animations:** idle, walk (slither), run, attack_1 (bite), attack_2 (vine whip), hit, die, victory
**Priority:** 2

#### SAMTMOOS_TIER_004
**Name:** `firefly_swarm_creature`
**Beschreibung:** Swarm of fireflies forming creature shape, glowing, magical forest entity
**Animations:** idle (float), walk, run, attack_1 (ram), attack_2 (blind flash), hit, die, victory
**Priority:** 2

#### SAMTMOOS_TIER_005
**Name:** `bark_bear`
**Beschreibung:** Bear with bark-like fur texture, forest guardian, strong and sturdy
**Animations:** idle, walk, run, attack_1 (claw swipe), attack_2 (roar), hit, die, victory
**Priority:** 2

---

## ❄️ REICH DER DREI (Eis/Nekromantie)

### NATURE/ENVIRONMENT:

#### REICH_NATURE_001
**Name:** `ice_cave_entrance`
**Beschreibung:** Ice cave entrance, frozen stalactites, blue glow from within, ominous
**Animations:** Static, ice_shimmer
**Varianten:** 2
**Priority:** 2

#### REICH_NATURE_002
**Name:** `glacier_cliff_section`
**Beschreibung:** Glacier ice wall, blue-white ice, jagged surface, mountain ice feature
**Animations:** Static
**Varianten:** 3
**Priority:** 2

#### REICH_NATURE_003
**Name:** `frozen_tree_dead`
**Beschreibung:** Dead tree encased in ice, eerie, necromancy zone decoration
**Animations:** Static
**Varianten:** 2
**Priority:** 2

#### REICH_NATURE_004
**Name:** `ice_crystal_spike`
**Beschreibung:** Large ice crystal spike, jutting from ground, magical ice formation
**Animations:** Static, glow
**Varianten:** 3
**Priority:** 2

#### REICH_NATURE_005
**Name:** `frozen_undead_statue`
**Beschreibung:** Undead creature frozen in ice, decorative creepy element
**Animations:** Static (breaks free optional for event)
**Varianten:** 2
**Priority:** 2

---

### TIERE:

#### REICH_TIER_001
**Name:** `crystal_horn_goat`
**Beschreibung:** Mountain goat with crystal horns, white fur, ice element creature
**Animations:** idle, walk, run, attack_1 (horn bash), attack_2 (ice breath), hit, die, victory
**Priority:** 2

#### REICH_TIER_002
**Name:** `frost_eagle`
**Beschreibung:** Large eagle, white and blue feathers, ice element bird of prey
**Animations:** idle, walk (hop), run (fly), attack_1 (talon strike), attack_2 (frost gust), hit, die, victory
**Priority:** 2

#### REICH_TIER_003
**Name:** `ice_yeti`
**Beschreibung:** Yeti creature, white fur, large and intimidating, mountain guardian
**Animations:** idle, walk, run, attack_1 (punch), attack_2 (ground slam), hit, die, victory
**Priority:** 2

#### REICH_TIER_004
**Name:** `glacier_wolf`
**Beschreibung:** Wolf with ice-blue fur, frost aura, pack hunter appearance
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (howl buff), hit, die, victory
**Priority:** 2

#### REICH_TIER_005
**Name:** `ice_lich_minion`
**Beschreibung:** Small undead ice creature, skeletal, frozen aura, necromancy minion
**Animations:** idle, walk (shamble), run, attack_1 (claw), attack_2 (ice bolt), hit, die, victory
**Priority:** 2

---

## 🌊 SALZWIND-KÜSTE (Strand/Meer)

### BUILDINGS:

#### SALZWIND_BUILD_001
**Name:** `lighthouse_tower`
**Beschreibung:** Tall lighthouse, stone tower, rotating light at top, coastal landmark
**Animations:** Light_rotate (constant), light_beam
**Varianten:** 1
**Priority:** 2

#### SALZWIND_BUILD_002
**Name:** `harbor_dock_wooden`
**Beschreibung:** Wooden dock/pier, extends into water, boat mooring, coastal structure
**Animations:** Static, wave_sway (slight)
**Varianten:** 2
**Priority:** 2

#### SALZWIND_BUILD_003
**Name:** `fish_market_stall`
**Beschreibung:** Fish market stall, wooden, display area for fish, coastal vendor stand
**Animations:** Static
**Varianten:** 2
**Priority:** 2

#### SALZWIND_BUILD_004
**Name:** `coastal_house_basic`
**Beschreibung:** Basic coastal house, wood and stone, weathered by sea, sailor home
**Animations:** Static, door_open
**Varianten:** 3
**Priority:** 2

---

### NATURE:

#### SALZWIND_NATURE_001
**Name:** `beach_sand_dune`
**Beschreibung:** Sand dune, beach terrain element, grass tufts on top
**Animations:** Static
**Varianten:** 3
**Priority:** 2

#### SALZWIND_NATURE_002
**Name:** `coastal_rock_formation`
**Beschreibung:** Coastal rock, weathered by waves, tide pool base
**Animations:** Static
**Varianten:** 3
**Priority:** 2

#### SALZWIND_NATURE_003
**Name:** `seaweed_cluster`
**Beschreibung:** Seaweed cluster, washed up on beach or in shallow water
**Animations:** Static (sway in water)
**Varianten:** 2
**Priority:** 2

#### SALZWIND_NATURE_004
**Name:** `wooden_boat_small`
**Beschreibung:** Small wooden fishing boat, beached or floating, coastal prop
**Animations:** Float_bob (in water)
**Varianten:** 2
**Priority:** 2

---

### TIERE:

#### SALZWIND_TIER_001
**Name:** `wave_dolphin`
**Beschreibung:** Dolphin, playful, water element, sleek blue-gray
**Animations:** idle, walk (swim), run (fast swim), attack_1 (ram), attack_2 (water jet), hit, die, victory
**Priority:** 2

#### SALZWIND_TIER_002
**Name:** `shell_crab`
**Beschreibung:** Large crab, hardshell, pincers, coastal crustacean
**Animations:** idle, walk (sidestep), run, attack_1 (pinch), attack_2 (bubble spray), hit, die, victory
**Priority:** 2

#### SALZWIND_TIER_003
**Name:** `sand_seal`
**Beschreibung:** Seal, beach dweller, friendly but defensive, water creature
**Animations:** idle, walk (waddle), run (belly slide), attack_1 (bite), attack_2 (splash), hit, die, victory
**Priority:** 2

#### SALZWIND_TIER_004
**Name:** `coral_fish_large`
**Beschreibung:** Large colorful fish, coral reef style, water element
**Animations:** idle, walk (swim), run, attack_1 (ram), attack_2 (water pulse), hit, die, victory
**Priority:** 2

#### SALZWIND_TIER_005
**Name:** `seagull_hybrid`
**Beschreibung:** Seagull, coastal bird, can be aggressive, scavenger
**Animations:** idle, walk (hop), run (fly), attack_1 (peck), attack_2 (dive bomb), hit, die, victory
**Priority:** 2

---

## ⚡ BLITZEBENE (Highland/Magie)

### BUILDINGS:

#### BLITZEBENE_BUILD_001
**Name:** `magic_academy_tower`
**Beschreibung:** Tall magic tower, spire, glowing windows, arcane architecture, highland magic school
**Animations:** Window_glow, lightning_strike (occasional)
**Varianten:** 1
**Priority:** 2

#### BLITZEBENE_BUILD_002
**Name:** `rune_altar_platform`
**Beschreibung:** Stone altar platform, carved runes glowing, magic ritual site, highland mystical
**Animations:** Rune_glow (pulse)
**Varianten:** 1
**Priority:** 2

#### BLITZEBENE_BUILD_003
**Name:** `totem_pole_magic`
**Beschreibung:** Wooden totem pole, carved faces, magic symbols, highland tribal element
**Animations:** Static, glow (optional)
**Varianten:** 3
**Priority:** 2

#### BLITZEBENE_BUILD_004
**Name:** `weather_altar_stone`
**Beschreibung:** Stone altar controlling weather, lightning rod, glowing crystals, open air structure
**Animations:** Lightning_channel (effect)
**Varianten:** 1
**Priority:** 2

---

### NATURE:

#### BLITZEBENE_NATURE_001
**Name:** `highland_grass_tall`
**Beschreibung:** Tall grass, windswept, highland plains vegetation
**Animations:** Wind_sway (strong)
**Varianten:** 2
**Priority:** 2

#### BLITZEBENE_NATURE_002
**Name:** `cliff_edge_highland`
**Beschreibung:** Cliff edge, steep drop, highland terrain feature
**Animations:** Static
**Varianten:** 2
**Priority:** 2

#### BLITZEBENE_NATURE_003
**Name:** `lightning_struck_tree`
**Beschreibung:** Tree charred by lightning, split trunk, smoldering, dramatic
**Animations:** Static, smoke (faint)
**Varianten:** 2
**Priority:** 2

---

### TIERE:

#### BLITZEBENE_TIER_001
**Name:** `lightning_gazelle`
**Beschreibung:** Gazelle with electric aura, fast, highland plains runner
**Animations:** idle, walk, run (very fast), attack_1 (horn charge), attack_2 (lightning bolt), hit, die, victory
**Priority:** 2

#### BLITZEBENE_TIER_002
**Name:** `thunder_bird`
**Beschreibung:** Large bird, electric element, thundercloud aura, majestic
**Animations:** idle, walk (hop), run (fly), attack_1 (talon), attack_2 (lightning strike), hit, die, victory
**Priority:** 2

#### BLITZEBENE_TIER_003
**Name:** `steppe_lion_electric`
**Beschreibung:** Lion with crackling mane, electric element, highland predator
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (roar + shock), hit, die, victory
**Priority:** 2

#### BLITZEBENE_TIER_004
**Name:** `prairie_dog_magic`
**Beschreibung:** Prairie dog, small, electric element, cute but zappy
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (static shock), hit, die, victory
**Priority:** 2

#### BLITZEBENE_TIER_005
**Name:** `electric_snake`
**Beschreibung:** Snake with electric scales, yellow-blue, highland serpent
**Animations:** idle, walk (slither), run, attack_1 (bite), attack_2 (shock), hit, die, victory
**Priority:** 2

---

## 🐸 GRÜNSCHLAMM-SUMPF (Toxic Swamp)

### BUILDINGS/STRUCTURES:

#### SUMPF_BUILD_001
**Name:** `swamp_hut_stilts`
**Beschreibung:** Hut on wooden stilts, raised above swamp water, witch dwelling style
**Animations:** Static, door_open
**Varianten:** 2
**Priority:** 2

#### SUMPF_BUILD_002
**Name:** `witch_circle_stones`
**Beschreibung:** Stone circle, witch ritual site, cauldron in center, dark magic aura
**Animations:** Cauldron_bubble, fog_rise
**Varianten:** 1
**Priority:** 2

#### SUMPF_BUILD_003
**Name:** `funkelnest_cave_entrance`
**Beschreibung:** Hidden cave entrance, overgrown with vines, treasure cave, concealed
**Animations:** Static, vines_sway
**Varianten:** 1
**Priority:** 2

---

### NATURE:

#### SUMPF_NATURE_001
**Name:** `swamp_tree_twisted`
**Beschreibung:** Twisted dead tree, dark bark, gnarled branches, swamp atmosphere
**Animations:** Static
**Varianten:** 3
**Priority:** 2

#### SUMPF_NATURE_002
**Name:** `poison_mushroom_cluster`
**Beschreibung:** Poisonous mushrooms, toxic colors, swamp danger indicator
**Animations:** Static, spore_release (optional)
**Varianten:** 2
**Priority:** 2

#### SUMPF_NATURE_003
**Name:** `murky_water_pool`
**Beschreibung:** Murky swamp water pool, green-brown, fog rising, dangerous looking
**Animations:** Water_ripple, fog_rise
**Varianten:** 2
**Priority:** 2

#### SUMPF_NATURE_004
**Name:** `hanging_moss_vines`
**Beschreibung:** Hanging moss, draped from trees, swamp decoration
**Animations:** Sway
**Varianten:** 2
**Priority:** 2

---

### TIERE:

#### SUMPF_TIER_001
**Name:** `poison_frog_giant`
**Beschreibung:** Giant poison dart frog, bright toxic colors, swamp amphibian
**Animations:** idle, walk (hop), run, attack_1 (tongue lash), attack_2 (poison spit), hit, die, victory
**Priority:** 2

#### SUMPF_TIER_002
**Name:** `swamp_alligator`
**Beschreibung:** Alligator, dark green, swamp predator, powerful jaws
**Animations:** idle, walk, run (swim), attack_1 (bite), attack_2 (tail swipe), hit, die, victory
**Priority:** 2

#### SUMPF_TIER_003
**Name:** `bog_spider_large`
**Beschreibung:** Large spider, dark colors, poisonous, swamp hunter
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (web shot), hit, die, victory
**Priority:** 2

#### SUMPF_TIER_004
**Name:** `toxic_snake`
**Beschreibung:** Snake, green with black markings, venomous, swamp serpent
**Animations:** idle, walk (slither), run, attack_1 (bite), attack_2 (poison spray), hit, die, victory
**Priority:** 2

#### SUMPF_TIER_005
**Name:** `swamp_rat_mutant`
**Beschreibung:** Mutant rat, larger than normal, diseased appearance, swamp scavenger
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (disease cloud), hit, die, victory
**Priority:** 2

---

## 🔥 MAGMASTRÖME (Vulkan/Feuer)

### BUILDINGS:

#### MAGMA_BUILD_001
**Name:** `master_forge_building`
**Beschreibung:** Large forge building, open front, lava channels, anvils, blacksmith paradise
**Animations:** Fire_flicker, lava_flow, hammer_sound
**Varianten:** 1
**Priority:** 2

#### MAGMA_BUILD_002
**Name:** `lava_dock_platform`
**Beschreibung:** Stone platform/dock on lava river, loading area for ore/materials
**Animations:** Static, heat_shimmer
**Varianten:** 1
**Priority:** 2

#### MAGMA_BUILD_003
**Name:** `volcano_house_basic`
**Beschreibung:** House built into volcanic rock, heat-resistant, glowing cracks
**Animations:** Static, door_open, glow_pulse
**Varianten:** 2
**Priority:** 2

---

### NATURE:

#### MAGMA_NATURE_001
**Name:** `lava_river_section`
**Beschreibung:** Flowing lava river, glowing orange-red, volcanic terrain feature
**Animations:** Lava_flow (animated), heat_shimmer
**Varianten:** 3 (straight, curve, pool)
**Priority:** 2

#### MAGMA_NATURE_002
**Name:** `volcanic_rock_formation`
**Beschreibung:** Black volcanic rock, jagged, heat-cracked, terrain obstacle
**Animations:** Static, glow (cracks)
**Varianten:** 3
**Priority:** 2

#### MAGMA_NATURE_003
**Name:** `ember_geyser`
**Beschreibung:** Geyser shooting embers/steam, volcanic feature, danger zone
**Animations:** Erupt (periodic), steam_rise
**Varianten:** 2
**Priority:** 2

#### MAGMA_NATURE_004
**Name:** `charred_tree_stump`
**Beschreibung:** Burnt tree stump, smoldering, volcanic devastation
**Animations:** Static, smoke (faint)
**Varianten:** 2
**Priority:** 2

---

### TIERE:

#### MAGMA_TIER_001
**Name:** `lava_salamander`
**Beschreibung:** Salamander, fire element, glowing body, walks on lava
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (fire breath), hit, die, victory
**Priority:** 2

#### MAGMA_TIER_002
**Name:** `magma_hound`
**Beschreibung:** Dog/wolf made of lava and rock, fire creature, molten appearance
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (ember burst), hit, die, victory
**Priority:** 2

#### MAGMA_TIER_003
**Name:** `volcano_bird_phoenix`
**Beschreibung:** Phoenix-like bird, fire element, majestic, volcanic flyer
**Animations:** idle, walk (hop), run (fly), attack_1 (talon), attack_2 (fire dive), hit, die, victory
**Priority:** 2

#### MAGMA_TIER_004
**Name:** `fire_fox_spirit`
**Beschreibung:** Fox with flame tail and mane, fire spirit, elegant fire creature
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (fireball), hit, die, victory
**Priority:** 2

#### MAGMA_TIER_005
**Name:** `ember_lizard`
**Beschreibung:** Lizard with glowing scales, fire element, volcanic reptile
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (tail flame whip), hit, die, victory
**Priority:** 2

---

## 🕳️ TIEFENHÖHLEN (Unterirdisch/Dunkel)

### STRUCTURES:

#### HOEHLEN_BUILD_001
**Name:** `cave_entrance_large`
**Beschreibung:** Large cave entrance, dark opening, ominous, connects to underground
**Animations:** Static, ambient_echo (sound)
**Varianten:** 2
**Priority:** 2

#### HOEHLEN_BUILD_002
**Name:** `dark_altar_stone`
**Beschreibung:** Dark altar, shadowy aura, ritualistic, underground temple element
**Animations:** Shadow_pulse
**Varianten:** 1
**Priority:** 2

#### HOEHLEN_BUILD_003
**Name:** `mine_cart_tracks`
**Beschreibung:** Mine cart and tracks, abandoned mining equipment, cave prop
**Animations:** Static (cart_roll optional)
**Varianten:** 2
**Priority:** 2

---

### NATURE:

#### HOEHLEN_NATURE_001
**Name:** `cave_stalactite_cluster`
**Beschreibung:** Stalactites hanging from cave ceiling, dripping water
**Animations:** Drip (water)
**Varianten:** 3
**Priority:** 2

#### HOEHLEN_NATURE_002
**Name:** `cave_stalagmite_cluster`
**Beschreibung:** Stalagmites rising from cave floor, rocky formations
**Animations:** Static
**Varianten:** 3
**Priority:** 2

#### HOEHLEN_NATURE_003
**Name:** `glowing_crystal_cave`
**Beschreibung:** Glowing crystals in cave wall, light source, mystical
**Animations:** Glow_pulse
**Varianten:** 2
**Priority:** 2

#### HOEHLEN_NATURE_004
**Name:** `underground_mushroom_giant`
**Beschreibung:** Giant underground mushroom, bioluminescent, cave flora
**Animations:** Glow_pulse
**Varianten:** 2
**Priority:** 2

---

### TIERE:

#### HOEHLEN_TIER_001
**Name:** `cave_bat_giant`
**Beschreibung:** Giant bat, dark element, cave dweller, nocturnal predator
**Animations:** idle, walk (hang), run (fly), attack_1 (bite), attack_2 (sonic screech), hit, die, victory
**Priority:** 2

#### HOEHLEN_TIER_002
**Name:** `shadow_rat_mutant`
**Beschreibung:** Dark rat, shadow aura, cave scavenger, disease carrier
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (shadow bolt), hit, die, victory
**Priority:** 2

#### HOEHLEN_TIER_003
**Name:** `cave_spider_venomous`
**Beschreibung:** Spider, dark colors, large, venomous, cave hunter
**Animations:** idle, walk, run, attack_1 (bite), attack_2 (venom spit), hit, die, victory
**Priority:** 2

#### HOEHLEN_TIER_004
**Name:** `shadow_snake`
**Beschreibung:** Snake made of shadows, dark element, cave serpent, ethereal
**Animations:** idle, walk (slither), run, attack_1 (bite), attack_2 (shadow strike), hit, die, victory
**Priority:** 2

#### HOEHLEN_TIER_005
**Name:** `cave_bear_dark`
**Beschreibung:** Bear, dark fur, cave dweller, large and dangerous
**Animations:** idle, walk, run, attack_1 (claw), attack_2 (roar), hit, die, victory
**Priority:** 2

---

# 🟢 PRIORITY 3 - EXPANSION ASSETS

---

## 🎸 INSTRUMENTS (Instrument System)

**ANIMATION SET:**
- `idle` - Platziert, nicht gespielt
- `play_1` - Grundmelodie spielen
- `play_2` - Solo/Special spielen
- `pickup` - Aufheben
- `putdown` - Ablegen

---

### INSTRUMENT_001
**Name:** `acoustic_guitar_western`
**Beschreibung:** Acoustic guitar, western style, wood finish, classic shape
**Animations:** idle, play_1, play_2, pickup, putdown
**Priority:** 3

### INSTRUMENT_002
**Name:** `electric_guitar_fantasy`
**Beschreibung:** Electric guitar, fantasy design, glowing elements, magical tech
**Animations:** idle, play_1, play_2, pickup, putdown
**Priority:** 3

### INSTRUMENT_003
**Name:** `drum_set_complete`
**Beschreibung:** Complete drum set, bass drum, snare, toms, cymbals, fantasy style
**Animations:** idle, play_1 (basic beat), play_2 (solo), pickup (sticks), putdown
**Priority:** 3

### INSTRUMENT_004
**Name:** `bass_guitar`
**Beschreibung:** Bass guitar, 4-string, western-modern fusion
**Animations:** idle, play_1, play_2, pickup, putdown
**Priority:** 3

### INSTRUMENT_005
**Name:** `keyboard_synth_magical`
**Beschreibung:** Keyboard synthesizer, glowing keys, magical music tech
**Animations:** idle, play_1, play_2, pickup (portable), putdown
**Priority:** 3

---

## ⚔️ WEAPONS (Combat Equipment)

**ANIMATION SET (für Spieler):**
- `idle_equipped` - In Hand/am Gürtel
- `attack_swing` - Schwingen
- `attack_thrust` - Stoßen
- `block` - Blocken
- `sheath` - Wegstecken
- `draw` - Ziehen

---

### WEAPON_SWORD_001
**Name:** `sword_starter_rusty`
**Beschreibung:** Rusty old sword, beginner weapon, worn blade
**Animations:** Weapon animation set
**Priority:** 3

### WEAPON_SWORD_002
**Name:** `sword_steel_common`
**Beschreibung:** Steel sword, common quality, standard blade
**Animations:** Weapon animation set
**Priority:** 3

### WEAPON_SWORD_003
**Name:** `sword_flame_rare`
**Beschreibung:** Flaming sword, rare quality, fire enchantment, glowing blade
**Animations:** Weapon animation set + fire_trail
**Priority:** 3

---

## 🍖 FOOD ITEMS (Consumables)

**Diese Models können SEHR klein/simple sein:**

### FOOD_SAMTMOOS_001
**Name:** `mushroom_soup_bowl`
**Beschreibung:** Bowl of mushroom soup, steaming, forest specialty
**Animations:** Steam_rise
**Priority:** 3

### FOOD_HANDELSFESTE_001
**Name:** `grilled_meat_skewer`
**Beschreibung:** Meat skewer, grilled, desert capital specialty, western BBQ style
**Animations:** Static (smoke optional)
**Priority:** 3

### FOOD_GENERIC_001
**Name:** `healing_potion_small`
**Beschreibung:** Small red potion bottle, health recovery, glowing liquid
**Animations:** Glow_pulse
**Priority:** 3

---

## 🎭 NPCs (Non-Combat Characters)

**ANIMATION SET:**
- `idle` - Steht, wartet
- `walk` - Geht herum
- `talk` - Spricht, Gesten
- `point` - Zeigt auf etwas
- `trade` - Übergibt Item
- `work` - Arbeitet (je nach Beruf)

---

### NPC_HANDELSFESTE_001
**Name:** `merchant_trader_male`
**Beschreibung:** Male merchant NPC, western clothing, friendly, trader appearance
**Animations:** NPC animation set + trade
**Priority:** 3

### NPC_HANDELSFESTE_002
**Name:** `merchant_trader_female`
**Beschreibung:** Female merchant NPC, western-fantasy dress, shopkeeper
**Animations:** NPC animation set + trade
**Priority:** 3

### NPC_HANDELSFESTE_003
**Name:** `guard_city_watch`
**Beschreibung:** City guard, armor, spear, patrolling, western-fantasy military
**Animations:** NPC animation set + patrol, alert
**Priority:** 3

### NPC_HANDELSFESTE_004
**Name:** `citizen_male_casual`
**Beschreibung:** Male citizen, casual western clothing, background NPC
**Animations:** NPC animation set
**Priority:** 3

### NPC_HANDELSFESTE_005
**Name:** `citizen_female_casual`
**Beschreibung:** Female citizen, casual western-fantasy dress, background NPC
**Animations:** NPC animation set
**Priority:** 3

### NPC_HANDELSFESTE_006
**Name:** `blacksmith_male`
**Beschreibung:** Blacksmith NPC, apron, muscular, hammer in hand, craftsman
**Animations:** NPC animation set + work (hammering)
**Priority:** 3

### NPC_HANDELSFESTE_007
**Name:** `tavern_bartender`
**Beschreibung:** Bartender NPC, saloon style, friendly, serving drinks
**Animations:** NPC animation set + serve (drink)
**Priority:** 3

---

## 📦 PROPS & DECORATION

### PROP_GENERIC_001
**Name:** `treasure_chest_wooden`
**Beschreibung:** Wooden treasure chest, classic RPG style, loot container
**Animations:** Open (lid), close
**Varianten:** 3 (small, medium, large)
**Priority:** 3

### PROP_GENERIC_002
**Name:** `campfire_wood`
**Beschreibung:** Campfire, burning wood, stones around, rest area
**Animations:** Fire_flicker, smoke_rise
**Varianten:** 1
**Priority:** 3

### PROP_GENERIC_003
**Name:** `signpost_wooden_western`
**Beschreibung:** Wooden signpost, directional, western style, path marker
**Animations:** Static (sway in wind)
**Varianten:** 2
**Priority:** 3

---

# 📊 PRODUCTION SUMMARY

## ASSET COUNTS:

### PRIORITY 1 (MVP Core):
- **Generic Nature Pack:** 15 Models (Trees, Rocks, Ground Cover)
- **Modular Buildings:** 7 Modules (Walls, Roofs, Doors, etc.)
- **Götterfels Zentrum:** 7 Assets
- **Handelsfeste Capital:** 23 Buildings/Props
- **Slime Companions:** 27 Models (9 colors × 3 stages)

**Priority 1 Total: ~79 Models**

### PRIORITY 2 (Region Expansions):
- **Samtmoos:** 9 Buildings/Nature + 5 Tiere = 14
- **Reich der Drei:** 5 Nature + 5 Tiere = 10
- **Salzwind:** 4 Buildings + 4 Nature + 5 Tiere = 13
- **Blitzebene:** 4 Buildings + 3 Nature + 5 Tiere = 12
- **Grünschlamm:** 3 Buildings + 4 Nature + 5 Tiere = 12
- **Magmaströme:** 3 Buildings + 4 Nature + 5 Tiere = 12
- **Tiefenhöhlen:** 3 Buildings + 4 Nature + 5 Tiere = 12

**Priority 2 Total: ~85 Models**

### PRIORITY 3 (Expansion):
- **Instruments:** 5 Models
- **Weapons:** 3 Swords (+ mehr später)
- **Food:** 3 Items (+ mehr später)
- **NPCs:** 7 Characters
- **Props:** 3 Items (+ mehr später)

**Priority 3 Total: ~21 Models**

---

## 🎯 GRAND TOTAL: ~185 MODELS (für komplette MVP + Region Expansion)

**Mit 3 Monaten Meshy AI:**
- **12 Wochen** = ~15 Models pro Woche = **MACHBAR!**
- Mehr Zeit für Iterations/Variations

---

# 🚀 NEXT STEPS

1. **Du gibst Feedback/Änderungen zu dieser Liste**
2. **Ich erstelle Meshy-Prompts für Priority 1**
3. **Du generierst in Meshy AI**
4. **Ich baue Import/Animation System**
5. **Integration in Najika World**

**BEREIT ZUM START? 🎨**
