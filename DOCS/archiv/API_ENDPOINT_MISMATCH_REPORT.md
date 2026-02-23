# API ENDPOINT MISMATCH REPORT - Najika World
**Generated:** 2026-02-09
**Frontend Location:** `c:\Najika_World\digivice\js\`
**Analysis:** All frontend API calls vs registered FastAPI routes

---

## EXECUTIVE SUMMARY

- **Total API calls found:** 172
- **Matched endpoints:** 30 (17%)
- **Missing endpoints:** 75 (44%)
- **Prefix mismatches:** 16 (9%)
- **Path mismatches:** 1 (1%)
- **Total issues:** 92 (53% of all calls)

---

## 1. MISSING ENDPOINTS (75 Found)

These endpoints are called from the frontend but DO NOT exist in the backend at all.

### High Priority - Core Functionality

#### Battle System
- **`/api/battle/reset`** - POST
  - File: `battle_api.js:152`
  - Note: No reset endpoint exists in backend battle routes
  - Impact: Players cannot reset/leave battles

- **`/api/battle/status`** - GET (without player_id)
  - File: `battle_api.js:50`
  - Note: Backend requires `/api/battle/status/{player_id}` but frontend calls without ID
  - Impact: Battle status checks will fail

#### File Management (Code Editor)
- **`/api/file/read`** - POST
  - File: `code_editor.js:169`
- **`/api/file/write`** - POST
  - File: `code_editor.js:237`, `code_editor.js:353`, `file_manager.js:323`
- **`/api/file/list`** - POST
  - File: `code_editor.js:261`, `file_manager.js:105`
- **`/api/file/delete`** - POST
  - File: `file_manager.js:387`, `file_manager.js:670`
- **`/api/file/rename`** - POST
  - File: `file_manager.js:415`
- **`/api/code/execute`** - POST
  - File: `code_editor.js:208`
- Impact: Code editor and file manager completely non-functional

#### Slime Companion System
- **`/api/slime/types`** - GET
  - File: `slime_companion_ui.js:708`
- **`/api/slime/all`** - GET
  - File: `slime_companion_ui.js:742`
- **`/api/slime/update`** - POST
  - File: `slime_companion_ui.js:766`
- **`/api/slime/feed`** - POST
  - File: `slime_companion.js:250`, `slime_companion_ui.js:1122`
- **`/api/slime/train`** - POST
  - File: `slime_companion.js:274`, `slime_companion_ui.js:1138`
- **`/api/slime/play`** - POST
  - File: `slime_companion.js:300`, `slime_companion_ui.js:1154`
- **`/api/slime/sleep`** - POST
  - File: `slime_companion_ui.js:1170`
- **`/api/slime/heal`** - POST
  - File: `slime_companion_ui.js:1186`
- **`/api/slime/evolve`** - POST
  - File: `slime_companion.js:324`, `slime_companion_ui.js:1202`
- **`/api/slime/rename`** - POST
  - File: `slime_companion_ui.js:1228`
- **`/api/slime/activate`** - POST
  - File: `slime_companion_ui.js:1245`
- **`/api/slime/create`** - POST
  - File: `slime_companion.js:224`, `slime_companion_ui.js:1270`
- **`/api/slime/status`** - POST
  - File: `slime_companion.js:205`

**Note:** Backend has `/api/slime/*` wildcard, but these specific endpoints might not be implemented.

#### Echoharp/Bard System (Entire system missing)
- **`/api/echoharp/status`** - GET (`echoharp_ui.js:659`)
- **`/api/echoharp/witness-item`** - GET (`echoharp_ui.js:682`)
- **`/api/echoharp/stories`** - GET (`echoharp_ui.js:702`)
- **`/api/echoharp/deeds`** - GET (`echoharp_ui.js:721`)
- **`/api/echoharp/quests`** - GET (`echoharp_ui.js:967`)
- **`/api/echoharp/quest/accept`** - POST (`echoharp_ui.js:992`)
- **`/api/echoharp/witness/activate`** - POST (`echoharp_ui.js:1020`, `echoharp_ui.js:1050`)
- **`/api/bard/status`** - GET (`echoharp_ui.js:662`)
- **`/api/bard/item/status`** - GET (`echoharp_ui.js:685`)
- **`/api/bard/stories`** - GET (`echoharp_ui.js:704`)
- **`/api/bard/player/deeds`** - GET (`echoharp_ui.js:723`)
- **`/api/bard/quest`** - GET (`echoharp_ui.js:971`)
- **`/api/bard/item/activate/before`** - POST (`echoharp_ui.js:1030`)
- **`/api/bard/item/activate/after`** - POST (`echoharp_ui.js:1060`)

Impact: Entire Echoharp/Bard storytelling system non-functional

#### Quests System
- **`/api/quests/stats`** - GET (`quest_ui.js:113`)
- **`/api/quests/active`** - GET (`quest_ui.js:114`)
- **`/api/quests/available`** - GET (`quest_ui.js:115`)
- **`/api/quests/start`** - POST (`quest_ui.js:449`)
- **`/api/quests/complete`** - POST (`quest_ui.js:483`)

**Note:** Backend has `/api/v1/game/quests/*` but frontend calls `/api/quests/*` - This is a PREFIX MISMATCH (see section 2)

#### Najika Care
- **`/api/najika/praise`** - POST (`command_system.js:250`)
- **`/api/najika/scold`** - POST (`command_system.js:315`)

Backend only has: `/api/najika/drink`, `/api/najika/equipment`, `/api/najika/feed`, `/api/najika/sleep`, `/api/najika/status`, `/api/najika/wash`

#### Dungeon System
- **`/api/dungeon/biomes`** - GET (`dungeon_ui.js:565`)
- **`/api/dungeon/difficulties`** - GET (`dungeon_ui.js:574`)

#### Chaos Events
- **`/api/chaos/check_event`** - GET (`chaos_event_ui.js:60`)
- **`/api/chaos/execute_choice`** - POST (`chaos_event_ui.js:139`)

#### Minigames
- **`/api/minigame/garden`** - POST (`safe_functions.js:54`, `safe_functions.js:61`)
- **`/api/minigame/rhythm`** - POST (`safe_functions.js:65`)
- **`/api/minigame/reflex`** - POST (`safe_functions.js:90`)

#### NPC/Shop System
- **`/api/player/gold`** - GET (`npc_dialogue_system.js:965`, `npc_interaction.js:323`)
- **`/api/shop/buy`** - POST (`npc_dialogue_system.js:979`, `npc_interaction.js:273`)
- **`/api/service/use`** - POST (`npc_dialogue_system.js:1100`)
- **`/api/player/session`** - GET (`world_map_api.js:61`)

#### Voice Call System
- **`/api/voice_call/start`** - POST (`voice_call.js:63`)
- **`/api/voice_call/audio`** - POST (`voice_call.js:167`)
- **`/api/voice_call/end`** - POST (`voice_call.js:305`)

**Note:** Backend has `/api/v1/voice/*` but frontend calls `/api/voice_call/*`

#### Other Missing Endpoints
- **`/api/room/actions`** - POST (`safe_functions.js:3`)
- **`/api/heal`** - POST (`safe_functions.js:69`)
- **`/api/event/next`** - POST (`safe_functions.js:82`, `oregon.js:3`)
- **`/api/crafting`** - POST (`safe_functions.js:86`)
- **`/api/training/status`** - GET (`system_monitor.js:230`)
- **`/api/security/status`** - GET (`system_monitor.js:274`)
- **`/api/memory/export`** - GET (`system_monitor.js:275`)
- **`/api/log/claude`** - POST (`najika_logger.js:38`, `najika_logger.js:72`)

---

## 2. PREFIX MISMATCHES (16 Found)

Frontend calls the wrong prefix but similar endpoint exists in backend.

### Arena System - All calls use `/api/arena/*` or `/api/game/arena/*`
**Should be:** `/api/v1/game/arena/*`

#### From `nemesis_arena_frontend.js`:
1. **Line 215:** `/api/arena/status` → `/api/v1/game/arena/status`
2. **Line 236:** `/api/arena/monsters` → `/api/v1/game/arena/monsters`
3. **Line 326:** `/api/arena/challenge` → `/api/v1/game/arena/challenge`
4. **Line 522:** `/api/arena/battle/action` → `/api/v1/game/arena/battle/action`
5. **Line 672:** `/api/arena/monster/{monsterId}` → `/api/v1/game/arena/monster/{monsterId}`
6. **Line 1010:** `/api/arena/wave-battle` → `/api/v1/game/arena/wave-battle`
7. **Line 1143:** `/api/arena/hierarchy` → `/api/v1/game/arena/hierarchy`

#### From `nemesis_arena_ui.js`:
8. **Line 162:** `/api/game/arena/hierarchy` → `/api/v1/game/arena/hierarchy`
9. **Line 311:** `/api/game/arena/challengers` → `/api/v1/game/arena/challengers`
10. **Line 336:** `/api/game/arena/my-nemesis` → `/api/v1/game/arena/my-nemesis`
11. **Line 393:** `/api/game/arena/regions` → `/api/v1/game/arena/regions`
12. **Line 444:** `/api/game/arena/challenge` → `/api/v1/game/arena/challenge`
13. **Line 509:** `/api/game/arena/monster/{monsterId}` → `/api/v1/game/arena/monster/{monsterId}`

#### From `finisher_category_selector.js`:
14. **Line 19:** `/api/game/arena/finisher/categories` → `/api/v1/game/arena/finisher/categories`
15. **Line 126:** `/api/game/arena/finisher/random-ingredients` → `/api/v1/game/arena/finisher/random-ingredients`
16. **Line 209:** `/api/game/arena/finisher/create` → `/api/v1/game/arena/finisher/create`

**Impact:** All Arena/Nemesis system calls will return 404

---

## 3. PATH MISMATCHES (1 Found)

Similar endpoint exists but path is different.

1. **`/api/battle/action`** (Frontend) vs **`/api/battle/player-action`** (Backend)
   - File: `battle_api.js:81`
   - Frontend calls: `POST /api/battle/action`
   - Backend has: `POST /api/battle/player-action`
   - Impact: Player battle actions will fail

---

## 4. PARAMETER MISMATCHES

### Battle Status
- **Frontend:** `GET /api/battle/status` (no params)
  - File: `battle_api.js:50`
- **Backend:** `GET /api/battle/status/{player_id}` (requires player_id)
- **Impact:** Will return 404, requires path parameter

---

## 5. RECOMMENDATIONS

### Immediate Fixes Required:

1. **Battle System** (`battle_api.js`):
   - Line 50: Add player_id to `/api/battle/status/{player_id}`
   - Line 81: Change `/api/battle/action` to `/api/battle/player-action`
   - Line 152: Either create `/api/battle/reset` backend endpoint OR remove from frontend

2. **Arena System** (ALL arena files):
   - Global search/replace: `/api/arena/` → `/api/v1/game/arena/`
   - Global search/replace: `/api/game/arena/` → `/api/v1/game/arena/`
   - Files affected: `nemesis_arena_frontend.js`, `nemesis_arena_ui.js`, `finisher_category_selector.js`

3. **Missing Systems** - Need backend implementation:
   - File management API (`/api/file/*`, `/api/code/execute`)
   - Echoharp/Bard system (entire `/api/echoharp/*` and `/api/bard/*`)
   - Chaos events (`/api/chaos/*`)
   - Dungeon system (`/api/dungeon/*`)
   - Minigames (`/api/minigame/*`)
   - Voice calls (`/api/voice_call/*` or use existing `/api/v1/voice/*`)
   - NPC/Shop system (`/api/player/gold`, `/api/shop/buy`, `/api/service/use`)
   - Various Najika endpoints (`praise`, `scold`)
   - Slime companion endpoints (verify `/api/slime/*` implementation)

4. **Quest System**:
   - Change frontend calls from `/api/quests/*` to `/api/v1/game/quests/*`
   - Files: `quest_ui.js` (lines 113, 114, 115, 449, 483)

### Verification Needed:

1. Check if `/api/slime/*` wildcard actually implements all the called endpoints:
   - types, all, update, feed, train, play, sleep, heal, evolve, rename, activate, create, status

2. Verify `/api/oregon/*` wildcard covers `/api/event/next`

---

## 6. MATCHED ENDPOINTS (Working Fine)

These endpoints match correctly between frontend and backend:

- `/api/chat` and `/api/chat/history`
- `/api/najika/feed`, `/api/najika/sleep`, `/api/najika/wash`, `/api/najika/status`
- `/api/battle/start`, `/api/battle/skills`
- `/api/status`
- `/api/combat-magic/grab`, `/api/combat-magic/grab/execute`, `/api/combat-magic/tids`
- `/api/living/state`, `/api/living/proactive`
- `/api/cards` (covered by `/api/cards/*`)
- `/api/room/actions`

---

## APPENDIX: Files Analyzed

Total: 140 JavaScript files in `c:\Najika_World\digivice\js\`

**Key files with issues:**
- `battle_api.js` - Battle system API calls
- `nemesis_arena_frontend.js` - Arena system (prefix mismatches)
- `nemesis_arena_ui.js` - Arena UI (prefix mismatches)
- `finisher_category_selector.js` - Finisher system (prefix mismatches)
- `quest_ui.js` - Quest system (prefix mismatches)
- `echoharp_ui.js` - Echoharp/Bard system (completely missing)
- `code_editor.js` - File management (missing)
- `file_manager.js` - File operations (missing)
- `slime_companion.js` - Slime companion (needs verification)
- `slime_companion_ui.js` - Slime UI (needs verification)
- `chaos_event_ui.js` - Chaos events (missing)
- `dungeon_ui.js` - Dungeon system (missing)
- `voice_call.js` - Voice calls (missing/prefix mismatch)
- `safe_functions.js` - Various minigames and utilities (missing)
- `npc_dialogue_system.js` - NPC/Shop system (missing)
- `command_system.js` - Najika commands (missing)
- `system_monitor.js` - System monitoring (missing)

---

**End of Report**
