"""
Najika World - Automatischer Browser-Test V3
=============================================================
Testet UI, API, Steuerung und Gameplay-Systeme.
V3: Erweitert um Bewegung, Teleportation, Kamera, Combat,
    Inventar, Quests, Crafting, Fishing, Garden, Housing,
    Survival, Slime Companion, Dungeon, Triple Triad.
"""

import json
import time
import sys
import io
from playwright.sync_api import sync_playwright

# Fix Windows Unicode output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000/digivice/"
RESULTS = {"passed": 0, "failed": 0, "errors": [], "warnings": []}

def log_pass(test_name):
    RESULTS["passed"] += 1
    print(f"  [PASS] {test_name}")

def log_fail(test_name, reason=""):
    RESULTS["failed"] += 1
    RESULTS["errors"].append(f"{test_name}: {reason}")
    print(f"  [FAIL] {test_name} - {reason}")

def log_warn(msg):
    RESULTS["warnings"].append(msg)
    print(f"  [WARN] {msg}")

def safe_click(page, selector, timeout=3000):
    """Klickt ein Element per JavaScript - umgeht Overlay-Blockaden."""
    try:
        result = page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (!el) return 'not_found';
                el.click();
                return 'clicked';
            }}
        """)
        return result == "clicked"
    except:
        return False

def run_tests():
    with sync_playwright() as p:
        print("=" * 60)
        print("NAJIKA WORLD - BROWSER TEST V3 (Gameplay)")
        print("=" * 60)

        browser = p.firefox.launch(headless=False, slow_mo=100)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Console-Errors sammeln
        console_errors = []
        console_warnings = []
        network_errors = []

        page.on("console", lambda msg: (
            console_errors.append(msg.text) if msg.type == "error"
            else console_warnings.append(msg.text) if msg.type == "warning"
            else None
        ))

        page.on("requestfailed", lambda req: network_errors.append(f"{req.method} {req.url} - {req.failure}"))

        # ============================================================
        # TEST 1: Seite laden
        # ============================================================
        print("\n--- TEST 1: Seite laden ---")
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=15000)
            log_pass("Seite geladen (DOM ready)")
        except Exception as e:
            log_fail("Seite laden", str(e)[:80])
            browser.close()
            return

        # Warte auf JS-Initialisierung
        time.sleep(6)
        log_pass(f"Warte 6s fuer JS Init")

        # ============================================================
        # TEST 2: UI-Elemente vorhanden
        # ============================================================
        print("\n--- TEST 2: UI-Elemente pruefen ---")

        ui_check = page.evaluate("""
            () => {
                const ids = [
                    'ui-top-bar', 'canvas-container', 'btn-chat', 'btn-info',
                    'btn-najika', 'btn-minimap', 'btn-controls', 'btn-praise',
                    'btn-criticize', 'btn-triad', 'btn-dice', 'btn-garden',
                    'btn-fishing', 'btn-housing', 'btn-charstats', 'btn-quests',
                    'btn-bestiary', 'btn-creatures', 'btn-slime', 'btn-inventory',
                    'btn-activities', 'btn-settings'
                ];
                const result = {};
                for (const id of ids) {
                    result[id] = !!document.getElementById(id);
                }
                return result;
            }
        """)

        for elem_id, exists in ui_check.items():
            if exists:
                log_pass(f"#{elem_id} vorhanden")
            else:
                log_fail(f"#{elem_id} fehlt")

        # ============================================================
        # TEST 3: Alle Top-Bar Buttons klicken (via JS)
        # ============================================================
        print("\n--- TEST 3: Top-Bar Buttons klicken ---")

        button_tests = [
            ("btn-info", "Info Panel"),
            ("btn-najika", "Najika Stats"),
            ("btn-minimap", "Minimap"),
            ("btn-controls", "Controls"),
            ("btn-charstats", "Character Stats"),
            ("btn-quests", "Quest Log"),
            ("btn-bestiary", "Bestiary"),
            ("btn-creatures", "Kreaturen"),
            ("btn-slime", "Slime Companion"),
            ("btn-inventory", "Inventar"),
            ("btn-activities", "Aktivitaeten"),
            ("btn-settings", "Settings"),
        ]

        for btn_id, name in button_tests:
            try:
                # Klick via JS (umgeht Overlay)
                clicked = page.evaluate(f"""
                    () => {{
                        const btn = document.getElementById('{btn_id}');
                        if (!btn) return 'not_found';
                        btn.click();
                        return 'ok';
                    }}
                """)
                time.sleep(0.4)

                if clicked == "ok":
                    log_pass(f"Button '{name}' geklickt")
                    # Schliessen: nochmal klicken + Escape
                    page.evaluate(f"document.getElementById('{btn_id}')?.click()")
                    page.keyboard.press("Escape")
                    time.sleep(0.2)
                else:
                    log_fail(f"Button '{name}' nicht gefunden")
            except Exception as e:
                log_fail(f"Button '{name}'", str(e)[:60])

        # ============================================================
        # TEST 4: Chat Button
        # ============================================================
        print("\n--- TEST 4: Chat oeffnen ---")

        try:
            page.evaluate("window.chatUI?.toggleChat()")
            time.sleep(1)
            log_pass("Chat geoeffnet (toggleChat)")

            # Chat Input suchen
            has_chat_input = page.evaluate("""
                () => {
                    const inputs = document.querySelectorAll('input, textarea');
                    for (const inp of inputs) {
                        if (inp.offsetParent !== null) {  // sichtbar
                            return inp.id || inp.className || 'unnamed_input';
                        }
                    }
                    return null;
                }
            """)
            if has_chat_input:
                log_pass(f"Chat Input gefunden: {has_chat_input}")
            else:
                log_warn("Kein sichtbares Chat Input gefunden")

            page.evaluate("window.chatUI?.toggleChat()")
            time.sleep(0.3)
        except Exception as e:
            log_fail("Chat Test", str(e)[:80])

        # ============================================================
        # TEST 5: Lob und Tadel
        # ============================================================
        print("\n--- TEST 5: Lob & Tadel ---")

        for action, name in [("togglePraise(true)", "Lob"), ("togglePraise(false)", "Tadel")]:
            try:
                page.evaluate(f"if(typeof {action.split('(')[0]} === 'function') {action}")
                time.sleep(0.8)
                log_pass(f"{name} ausgefuehrt")
            except Exception as e:
                log_fail(f"{name}", str(e)[:60])

        # ============================================================
        # TEST 6: Aktivitaeten-Panel Buttons
        # ============================================================
        print("\n--- TEST 6: Aktivitaeten-Panel ---")

        # Oeffne Panel
        page.evaluate("document.getElementById('btn-activities')?.click()")
        time.sleep(0.5)

        activity_results = page.evaluate("""
            () => {
                const btns = document.querySelectorAll('#activities .activity-btn');
                const results = [];
                for (const btn of btns) {
                    try {
                        const text = btn.textContent.trim();
                        btn.click();
                        results.push({text: text, status: 'clicked'});
                    } catch(e) {
                        results.push({text: btn.textContent.trim(), status: 'error', msg: e.message});
                    }
                }
                return results;
            }
        """)

        for r in activity_results:
            if r["status"] == "clicked":
                log_pass(f"Aktivitaet '{r['text'][:30]}' geklickt")
            else:
                log_fail(f"Aktivitaet '{r['text'][:30]}'", r.get("msg", ""))

        # Alles schliessen
        page.keyboard.press("Escape")
        time.sleep(0.5)
        page.evaluate("document.getElementById('btn-activities')?.click()")
        time.sleep(0.3)

        # ============================================================
        # TEST 7: API Endpoints aus Browser
        # ============================================================
        print("\n--- TEST 7: GET API Endpoints ---")

        api_results = page.evaluate("""
            async () => {
                const endpoints = [
                    '/api/status', '/api/state', '/health',
                    '/api/world/time', '/api/world/weather/samtmoos_tiefwald',
                    '/api/player/session', '/api/player/gold',
                    '/api/quests/stats', '/api/quests/active', '/api/quests/available',
                    '/api/arena/status', '/api/arena/monsters', '/api/arena/hierarchy',
                    '/api/echoharp/status',
                    '/api/v2/living/state', '/api/v2/living/proactive',
                    '/api/world-map/map', '/api/world-map/position/kuja',
                    '/api/housing/house/kuja', '/api/farming/plots/kuja',
                    '/api/magic/schools', '/api/cards', '/api/pvp/stats/kuja',
                    '/api/slime/companion/1', '/api/region-boss/state/export',
                    '/api/personality', '/api/combat/stats',
                    '/api/dungeon/biomes', '/api/dungeon/difficulties',
                    '/api/training/status', '/api/chaos/check_event',
                    '/api/slime/types', '/api/combat-magic/tids',
                    '/api/chat/history', '/api/bond/status',
                    '/api/security/status', '/api/memory/export',
                ];
                const results = [];
                for (const ep of endpoints) {
                    try {
                        const resp = await fetch('http://127.0.0.1:8000' + ep);
                        const text = await resp.text();
                        let isJson = false;
                        try { JSON.parse(text); isJson = true; } catch(e) {}
                        results.push({
                            endpoint: ep, status: resp.status,
                            isJson: isJson, size: text.length,
                            hasHtml: text.startsWith('<!DOCTYPE') || text.startsWith('<html')
                        });
                    } catch(e) {
                        results.push({endpoint: ep, error: e.message});
                    }
                }
                return results;
            }
        """)

        for r in api_results:
            ep = r["endpoint"]
            if r.get("error"):
                log_fail(f"GET {ep}", r["error"][:60])
            elif r.get("hasHtml"):
                log_fail(f"GET {ep}", f"HTML statt JSON! Status={r['status']}")
            elif not r.get("isJson"):
                log_fail(f"GET {ep}", f"Kein JSON! Status={r['status']}")
            elif r["status"] == 200:
                log_pass(f"GET {ep} (200, {r['size']}B)")
            elif r["status"] == 404:
                log_pass(f"GET {ep} (404 JSON)")
            else:
                log_warn(f"GET {ep} Status={r['status']}")

        # ============================================================
        # TEST 8: POST Endpoints
        # ============================================================
        print("\n--- TEST 8: POST API Endpoints ---")

        post_results = page.evaluate("""
            async () => {
                const tests = [
                    {ep: '/api/v2/care/feed', body: {}},
                    {ep: '/api/v2/care/praise', body: {}},
                    {ep: '/api/battle/start', body: {player_id: 'kuja'}},
                    {ep: '/api/shop/buy', body: {item: 'heiltrank', player_id: 'kuja'}},
                    {ep: '/api/world-map/travel', body: {destination: 'kristallwald'}},
                    {ep: '/api/farming/plant', body: {plot_id: 1}},
                    {ep: '/api/housing/upgrade', body: {player_id: 'kuja'}},
                    {ep: '/api/instrument/play-note', body: {note: 'C'}},
                    {ep: '/api/combat-magic/grab', body: {}},
                    {ep: '/api/pvp/mercy/decide', body: {decision: 'spare'}},
                    {ep: '/api/nonexistent/test', body: {}},
                ];
                const results = [];
                for (const t of tests) {
                    try {
                        const resp = await fetch('http://127.0.0.1:8000' + t.ep, {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(t.body)
                        });
                        const text = await resp.text();
                        let isJson = false;
                        try { JSON.parse(text); isJson = true; } catch(e) {}
                        results.push({
                            endpoint: t.ep, status: resp.status,
                            isJson: isJson, size: text.length,
                            hasHtml: text.startsWith('<!DOCTYPE') || text.startsWith('<html')
                        });
                    } catch(e) {
                        results.push({endpoint: t.ep, error: e.message});
                    }
                }
                return results;
            }
        """)

        for r in post_results:
            ep = r["endpoint"]
            if r.get("error"):
                log_fail(f"POST {ep}", r["error"][:60])
            elif r.get("hasHtml"):
                log_fail(f"POST {ep}", "HTML statt JSON!")
            elif not r.get("isJson"):
                log_fail(f"POST {ep}", f"Kein JSON! Status={r['status']}")
            elif r["status"] in (200, 404):
                log_pass(f"POST {ep} ({r['status']}, {r['size']}B)")
            else:
                log_warn(f"POST {ep} Status={r['status']}")

        # ============================================================
        # TEST 9: 3D Scene & Canvas
        # ============================================================
        print("\n--- TEST 9: 3D Scene ---")

        scene_check = page.evaluate("""
            () => {
                return {
                    three: typeof THREE !== 'undefined',
                    scene3d: typeof window.Scene3D !== 'undefined',
                    canvas: !!document.querySelector('canvas'),
                    canvasSize: document.querySelector('canvas')
                        ? {w: document.querySelector('canvas').width, h: document.querySelector('canvas').height}
                        : null,
                    webgl: !!document.querySelector('canvas')?.getContext('webgl2')
                        || !!document.querySelector('canvas')?.getContext('webgl')
                };
            }
        """)

        if scene_check["three"]: log_pass("THREE.js geladen")
        else: log_fail("THREE.js nicht geladen")

        if scene_check["scene3d"]: log_pass("Scene3D vorhanden")
        else: log_warn("Scene3D nicht im window-Scope")

        if scene_check["canvas"]:
            s = scene_check.get("canvasSize", {})
            log_pass(f"Canvas vorhanden ({s.get('w', '?')}x{s.get('h', '?')})")
        else:
            log_fail("Kein Canvas gefunden")

        # ============================================================
        # TEST 10: Globale JS-Objekte pruefen
        # ============================================================
        print("\n--- TEST 10: Globale JS-Objekte ---")

        globals_check = page.evaluate("""
            () => {
                const objs = [
                    'Scene3D', 'chatUI', 'questUI', 'slimeCompanion',
                    'characterStatsUI', 'bestiaryUI', 'creatureUI',
                    'LivingSystemUI', 'worldInfoUI', 'NajikaConfig',
                    'SurvivalSystem', 'pvpUI', 'tripleTriad',
                    'NemesisArenaUI', 'slimeArenaUI',
                    'gameSystemsUIInitialized'
                ];
                const result = {};
                for (const name of objs) {
                    result[name] = window[name] !== undefined;
                }
                return result;
            }
        """)

        for name, exists in globals_check.items():
            if exists:
                log_pass(f"window.{name} vorhanden")
            else:
                log_warn(f"window.{name} nicht definiert")

        # ============================================================
        # TEST 11: Keyboard Controls + Bewegung
        # ============================================================
        print("\n--- TEST 11: Keyboard + Bewegung ---")

        try:
            # Focus auf Canvas setzen
            page.evaluate("document.querySelector('canvas')?.focus()")
            time.sleep(0.3)

            # Startposition merken
            start_pos = page.evaluate("""
                () => {
                    const cg = window.Scene3D?.characterGroup;
                    if (!cg) return null;
                    return {x: cg.position.x, y: cg.position.y, z: cg.position.z};
                }
            """)
            if start_pos:
                log_pass(f"Startposition: x={start_pos['x']:.0f} y={start_pos['y']:.0f} z={start_pos['z']:.0f}")
            else:
                log_warn("characterGroup nicht verfuegbar")

            # WASD Bewegung testen - W fuer 1 Sekunde halten
            page.keyboard.down("w")
            time.sleep(1.0)
            page.keyboard.up("w")
            time.sleep(0.3)

            after_w = page.evaluate("""
                () => {
                    const cg = window.Scene3D?.characterGroup;
                    if (!cg) return null;
                    return {x: cg.position.x, y: cg.position.y, z: cg.position.z};
                }
            """)

            if start_pos and after_w:
                dx = abs(after_w['x'] - start_pos['x'])
                dz = abs(after_w['z'] - start_pos['z'])
                moved = dx + dz
                if moved > 1:
                    log_pass(f"W-Taste: Charakter bewegt (delta={moved:.1f})")
                else:
                    log_warn(f"W-Taste: Kaum Bewegung (delta={moved:.1f})")
            else:
                log_warn("Position nicht vergleichbar")

            # Sprint testen (Shift + W)
            pos_before_sprint = page.evaluate("() => { const c = window.Scene3D?.characterGroup; return c ? {x:c.position.x,z:c.position.z} : null; }")
            page.keyboard.down("Shift")
            page.keyboard.down("w")
            time.sleep(0.8)
            page.keyboard.up("w")
            page.keyboard.up("Shift")
            time.sleep(0.2)
            pos_after_sprint = page.evaluate("() => { const c = window.Scene3D?.characterGroup; return c ? {x:c.position.x,z:c.position.z} : null; }")

            if pos_before_sprint and pos_after_sprint:
                sprint_delta = abs(pos_after_sprint['x'] - pos_before_sprint['x']) + abs(pos_after_sprint['z'] - pos_before_sprint['z'])
                log_pass(f"Sprint (Shift+W): delta={sprint_delta:.1f}")
            else:
                log_warn("Sprint-Test nicht moeglich")

            # Seitenwaerts testen (A und D)
            for key_name, key in [("A (links)", "a"), ("D (rechts)", "d")]:
                pos_before = page.evaluate("() => { const c = window.Scene3D?.characterGroup; return c ? {x:c.position.x,z:c.position.z} : null; }")
                page.keyboard.down(key)
                time.sleep(0.5)
                page.keyboard.up(key)
                time.sleep(0.1)
                pos_after = page.evaluate("() => { const c = window.Scene3D?.characterGroup; return c ? {x:c.position.x,z:c.position.z} : null; }")
                if pos_before and pos_after:
                    d = abs(pos_after['x'] - pos_before['x']) + abs(pos_after['z'] - pos_before['z'])
                    log_pass(f"{key_name}: delta={d:.1f}")
                else:
                    log_warn(f"{key_name}: Test nicht moeglich")

            # Rueckwaerts (S)
            page.keyboard.down("s")
            time.sleep(0.5)
            page.keyboard.up("s")
            time.sleep(0.1)
            log_pass("S (rueckwaerts) gedrueckt")

            # Space (Dodge/Block)
            page.keyboard.press(" ")
            time.sleep(0.3)
            log_pass("Space (Dodge/Block) gedrueckt")

            # Escape
            page.keyboard.press("Escape")
            time.sleep(0.2)
            log_pass("Escape gedrueckt")

        except Exception as e:
            log_fail("Bewegungs-Test", str(e)[:80])

        # ============================================================
        # TEST 12: Kamera-Modi
        # ============================================================
        print("\n--- TEST 12: Kamera-Modi ---")

        try:
            camera_results = page.evaluate("""
                () => {
                    const results = [];
                    const modes = ['orbit', 'third', 'first'];
                    for (const mode of modes) {
                        try {
                            window.Scene3D.setCameraMode(mode);
                            const current = window.Scene3D.getCameraMode();
                            results.push({mode, current, ok: current === mode});
                        } catch(e) {
                            results.push({mode, error: e.message});
                        }
                    }
                    // Zurueck auf Orbit
                    try { window.Scene3D.setCameraMode('orbit'); } catch(e) {}
                    return results;
                }
            """)

            for r in camera_results:
                if r.get("ok"):
                    log_pass(f"Kamera-Modus '{r['mode']}' gesetzt")
                elif r.get("error"):
                    log_fail(f"Kamera '{r['mode']}'", r["error"][:60])
                else:
                    log_warn(f"Kamera '{r['mode']}' -> current='{r.get('current','?')}'")

            time.sleep(0.5)
        except Exception as e:
            log_fail("Kamera-Test", str(e)[:60])

        # ============================================================
        # TEST 13: Teleportation
        # ============================================================
        print("\n--- TEST 13: Teleportation ---")

        try:
            teleport_results = page.evaluate("""
                () => {
                    const results = [];
                    const ts = window.TeleporterSystem;
                    if (!ts) return [{error: 'TeleporterSystem nicht verfuegbar'}];

                    // Aktueller State
                    try {
                        const state = ts.getState ? ts.getState() : null;
                        results.push({test: 'getState', ok: !!state, data: state ? 'vorhanden' : 'null'});
                    } catch(e) {
                        results.push({test: 'getState', error: e.message});
                    }

                    // Position vor Teleport
                    const cg = window.Scene3D?.characterGroup;
                    const posBefore = cg ? {x: cg.position.x, z: cg.position.z} : null;

                    // Teleport zu Kristallwald
                    try {
                        ts.teleportTo('kristallwald');
                        results.push({test: 'teleportTo_kristallwald', ok: true});
                    } catch(e) {
                        results.push({test: 'teleportTo_kristallwald', error: e.message});
                    }

                    // Position nach Teleport
                    const posAfter = cg ? {x: cg.position.x, z: cg.position.z} : null;
                    if (posBefore && posAfter) {
                        const moved = Math.abs(posAfter.x - posBefore.x) + Math.abs(posAfter.z - posBefore.z);
                        results.push({test: 'position_changed', ok: moved > 100, delta: Math.round(moved)});
                    }

                    // Teleport zu Frostvulkan
                    try {
                        ts.teleportTo('frostvulkan');
                        const posFrost = cg ? {x: Math.round(cg.position.x), z: Math.round(cg.position.z)} : null;
                        results.push({test: 'teleportTo_frostvulkan', ok: true, pos: posFrost});
                    } catch(e) {
                        results.push({test: 'teleportTo_frostvulkan', error: e.message});
                    }

                    // Zurueck zum Start (Goetterfels)
                    try {
                        ts.teleportTo('goetterfels');
                        results.push({test: 'teleportTo_goetterfels', ok: true});
                    } catch(e) {
                        results.push({test: 'teleportTo_goetterfels', error: e.message});
                    }

                    return results;
                }
            """)

            for r in teleport_results:
                t = r.get("test", "?")
                if r.get("error"):
                    if "TeleporterSystem" in r["error"]:
                        log_warn(r["error"])
                    else:
                        log_fail(f"Teleport {t}", r["error"][:60])
                elif r.get("ok"):
                    extra = ""
                    if r.get("delta"): extra = f" (delta={r['delta']})"
                    if r.get("pos"): extra = f" (pos={r['pos']})"
                    if r.get("data"): extra = f" ({r['data']})"
                    log_pass(f"Teleport {t}{extra}")
                else:
                    log_fail(f"Teleport {t}", f"ok=False delta={r.get('delta','?')}")

            time.sleep(1)
        except Exception as e:
            log_fail("Teleportation", str(e)[:80])

        # ============================================================
        # TEST 14: Teleporter UI (M-Taste)
        # ============================================================
        print("\n--- TEST 14: Teleporter UI ---")

        try:
            page.evaluate("document.querySelector('canvas')?.focus()")
            time.sleep(0.2)
            page.keyboard.press("m")
            time.sleep(0.8)

            tp_ui_visible = page.evaluate("""
                () => {
                    // Suche nach Teleporter-UI-Elementen
                    const tpUI = document.getElementById('teleporter-ui')
                        || document.getElementById('teleporter-overlay')
                        || document.querySelector('.teleporter-panel')
                        || document.querySelector('[class*="teleport"]');
                    if (tpUI) return {found: true, id: tpUI.id || tpUI.className, visible: tpUI.style.display !== 'none'};

                    // Fallback: TeleporterSystem.open()
                    if (window.TeleporterSystem?.open) {
                        window.TeleporterSystem.open();
                        return {found: true, method: 'open()'};
                    }
                    return {found: false};
                }
            """)

            if tp_ui_visible.get("found"):
                log_pass(f"Teleporter UI geoeffnet")
            else:
                log_warn("Teleporter UI nicht gefunden")

            # Schliessen
            page.keyboard.press("Escape")
            time.sleep(0.3)
            page.evaluate("window.TeleporterSystem?.close?.()")
            time.sleep(0.2)
        except Exception as e:
            log_fail("Teleporter UI", str(e)[:60])

        # ============================================================
        # TEST 15: Charakter-Position direkt setzen
        # ============================================================
        print("\n--- TEST 15: Position direkt setzen ---")

        try:
            pos_test = page.evaluate("""
                () => {
                    const cg = window.Scene3D?.characterGroup;
                    if (!cg) return {error: 'characterGroup nicht verfuegbar'};

                    // Setze auf bekannte Position
                    cg.position.set(500, 0, 500);
                    const p1 = {x: cg.position.x, z: cg.position.z};

                    // Setze auf andere Position
                    cg.position.set(-1000, 0, -1000);
                    const p2 = {x: cg.position.x, z: cg.position.z};

                    // Zurueck zum Spawn
                    cg.position.set(0, 0, 0);
                    const p3 = {x: cg.position.x, z: cg.position.z};

                    return {p1, p2, p3, ok: (p1.x === 500 && p2.x === -1000 && p3.x === 0)};
                }
            """)

            if pos_test.get("error"):
                log_warn(pos_test["error"])
            elif pos_test.get("ok"):
                log_pass("Position direkt setzen funktioniert (500,0,500 -> -1000,0,-1000 -> 0,0,0)")
            else:
                log_fail("Position setzen", f"Werte stimmen nicht: {pos_test}")
        except Exception as e:
            log_fail("Position setzen", str(e)[:60])

        # ============================================================
        # TEST 16: Inventar-System
        # ============================================================
        print("\n--- TEST 16: Inventar ---")

        try:
            inv_test = page.evaluate("""
                () => {
                    const results = [];
                    const inv = window.inventoryUI;
                    if (!inv) return [{test: 'inventoryUI', error: 'nicht verfuegbar'}];

                    // Inventar oeffnen
                    try {
                        if (inv.open) inv.open();
                        else if (inv.toggle) inv.toggle();
                        results.push({test: 'open', ok: true});
                    } catch(e) { results.push({test: 'open', error: e.message}); }

                    // Items abfragen
                    try {
                        const items = inv.getInventory ? inv.getInventory() : null;
                        results.push({test: 'getInventory', ok: items !== null, count: items ? (Array.isArray(items) ? items.length : Object.keys(items).length) : 0});
                    } catch(e) { results.push({test: 'getInventory', error: e.message}); }

                    // Equipped Items
                    try {
                        const eq = inv.getEquippedItems ? inv.getEquippedItems() : null;
                        results.push({test: 'getEquippedItems', ok: eq !== null});
                    } catch(e) { results.push({test: 'getEquippedItems', error: e.message}); }

                    // Schliessen
                    try {
                        if (inv.close) inv.close();
                        results.push({test: 'close', ok: true});
                    } catch(e) { results.push({test: 'close', error: e.message}); }

                    return results;
                }
            """)

            for r in inv_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Inventar: {r['error']}")
                    else:
                        log_fail(f"Inventar {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = f" ({r['count']} Items)" if "count" in r else ""
                    log_pass(f"Inventar {r['test']}{extra}")
                else:
                    log_fail(f"Inventar {r['test']}", "ok=False")

            page.keyboard.press("Escape")
            time.sleep(0.3)
        except Exception as e:
            log_fail("Inventar", str(e)[:60])

        # ============================================================
        # TEST 17: Quest-System
        # ============================================================
        print("\n--- TEST 17: Quest-System ---")

        try:
            quest_test = page.evaluate("""
                () => {
                    const results = [];
                    const q = window.questUI;
                    if (!q) return [{test: 'questUI', error: 'nicht verfuegbar'}];

                    // Quest-Log oeffnen
                    try {
                        if (q.toggleQuestLog) q.toggleQuestLog();
                        results.push({test: 'toggleQuestLog', ok: true});
                    } catch(e) { results.push({test: 'toggleQuestLog', error: e.message}); }

                    // Aktive Quests
                    try {
                        const active = q.getActiveQuests ? q.getActiveQuests() : null;
                        results.push({test: 'getActiveQuests', ok: active !== null, count: active ? active.length : 0});
                    } catch(e) { results.push({test: 'getActiveQuests', error: e.message}); }

                    // Verfuegbare Quests
                    try {
                        const avail = q.getAvailableQuests ? q.getAvailableQuests() : null;
                        results.push({test: 'getAvailableQuests', ok: avail !== null, count: avail ? avail.length : 0});
                    } catch(e) { results.push({test: 'getAvailableQuests', error: e.message}); }

                    // Abgeschlossene Quests
                    try {
                        const done = q.getCompletedQuests ? q.getCompletedQuests() : null;
                        results.push({test: 'getCompletedQuests', ok: done !== null, count: done ? done.length : 0});
                    } catch(e) { results.push({test: 'getCompletedQuests', error: e.message}); }

                    // Schliessen
                    try {
                        if (q.toggleQuestLog) q.toggleQuestLog();
                    } catch(e) {}

                    return results;
                }
            """)

            for r in quest_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Quest: {r['error']}")
                    else:
                        log_fail(f"Quest {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = f" ({r['count']})" if "count" in r else ""
                    log_pass(f"Quest {r['test']}{extra}")
                else:
                    log_fail(f"Quest {r['test']}", "ok=False")

            page.keyboard.press("Escape")
            time.sleep(0.3)
        except Exception as e:
            log_fail("Quest-System", str(e)[:60])

        # ============================================================
        # TEST 18: Survival-System
        # ============================================================
        print("\n--- TEST 18: Survival-System ---")

        try:
            survival_test = page.evaluate("""
                () => {
                    const results = [];
                    const ss = window.SurvivalSystem;
                    if (!ss) return [{test: 'SurvivalSystem', error: 'nicht verfuegbar'}];

                    // Beduerfnisse abfragen
                    try {
                        const needs = ss.getNeeds ? ss.getNeeds() : null;
                        if (needs) {
                            results.push({test: 'getNeeds', ok: true,
                                hunger: needs.hunger, thirst: needs.thirst,
                                energy: needs.energy, hp: needs.hp});
                        } else {
                            results.push({test: 'getNeeds', ok: false});
                        }
                    } catch(e) { results.push({test: 'getNeeds', error: e.message}); }

                    // Mood abfragen
                    try {
                        const mood = ss.getCurrentMood ? ss.getCurrentMood() : null;
                        results.push({test: 'getCurrentMood', ok: mood !== null, value: mood});
                    } catch(e) { results.push({test: 'getCurrentMood', error: e.message}); }

                    // Essen testen
                    try {
                        if (ss.eat) {
                            ss.eat('bread', 10);
                            results.push({test: 'eat', ok: true});
                        } else {
                            results.push({test: 'eat', error: 'no eat function'});
                        }
                    } catch(e) { results.push({test: 'eat', error: e.message}); }

                    // Trinken testen
                    try {
                        if (ss.drink) {
                            ss.drink('water', 10);
                            results.push({test: 'drink', ok: true});
                        } else {
                            results.push({test: 'drink', error: 'no drink function'});
                        }
                    } catch(e) { results.push({test: 'drink', error: e.message}); }

                    // Moodlets
                    try {
                        const moodlets = ss.getMoodlets ? ss.getMoodlets() : null;
                        results.push({test: 'getMoodlets', ok: moodlets !== null, count: moodlets ? moodlets.length : 0});
                    } catch(e) { results.push({test: 'getMoodlets', error: e.message}); }

                    // Traits
                    try {
                        const traits = ss.getTraits ? ss.getTraits() : null;
                        results.push({test: 'getTraits', ok: traits !== null, count: traits ? traits.length : 0});
                    } catch(e) { results.push({test: 'getTraits', error: e.message}); }

                    return results;
                }
            """)

            for r in survival_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Survival: {r['error']}")
                    else:
                        log_fail(f"Survival {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = ""
                    if "hunger" in r:
                        extra = f" (H={r.get('hunger','?')} T={r.get('thirst','?')} E={r.get('energy','?')} HP={r.get('hp','?')})"
                    elif "value" in r:
                        extra = f" (={r['value']})"
                    elif "count" in r:
                        extra = f" ({r['count']})"
                    log_pass(f"Survival {r['test']}{extra}")
                else:
                    log_fail(f"Survival {r['test']}", "ok=False")
        except Exception as e:
            log_fail("Survival-System", str(e)[:60])

        # ============================================================
        # TEST 19: Slime Companion
        # ============================================================
        print("\n--- TEST 19: Slime Companion ---")

        try:
            slime_test = page.evaluate("""
                () => {
                    const results = [];
                    const sc = window.slimeCompanion;
                    if (!sc) return [{test: 'slimeCompanion', error: 'nicht verfuegbar'}];

                    // Status
                    try {
                        const status = sc.getStatus ? sc.getStatus() : null;
                        results.push({test: 'getStatus', ok: status !== null, data: status ? JSON.stringify(status).substring(0,80) : ''});
                    } catch(e) { results.push({test: 'getStatus', error: e.message}); }

                    // Trust Level
                    try {
                        const trust = sc.getTrust ? sc.getTrust() : null;
                        results.push({test: 'getTrust', ok: trust !== null, value: trust});
                    } catch(e) { results.push({test: 'getTrust', error: e.message}); }

                    // Forms
                    try {
                        const forms = sc.getForms ? sc.getForms() : null;
                        results.push({test: 'getForms', ok: forms !== null, count: forms ? (Array.isArray(forms) ? forms.length : Object.keys(forms).length) : 0});
                    } catch(e) { results.push({test: 'getForms', error: e.message}); }

                    // Feed
                    try {
                        if (sc.feed) {
                            sc.feed('meat');
                            results.push({test: 'feed', ok: true});
                        }
                    } catch(e) { results.push({test: 'feed', error: e.message}); }

                    // Play
                    try {
                        if (sc.play) {
                            sc.play();
                            results.push({test: 'play', ok: true});
                        }
                    } catch(e) { results.push({test: 'play', error: e.message}); }

                    return results;
                }
            """)

            for r in slime_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Slime: {r['error']}")
                    else:
                        log_fail(f"Slime {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = ""
                    if "value" in r: extra = f" (={r['value']})"
                    elif "count" in r: extra = f" ({r['count']})"
                    elif "data" in r and r["data"]: extra = f" ({r['data'][:50]})"
                    log_pass(f"Slime {r['test']}{extra}")
                else:
                    log_fail(f"Slime {r['test']}", "ok=False")
        except Exception as e:
            log_fail("Slime Companion", str(e)[:60])

        # ============================================================
        # TEST 20: Battle/Combat System
        # ============================================================
        print("\n--- TEST 20: Battle/Combat ---")

        try:
            battle_test = page.evaluate("""
                async () => {
                    const results = [];
                    const ba = window.battleAPI;

                    // battleAPI pruefen
                    if (!ba) {
                        results.push({test: 'battleAPI', error: 'nicht verfuegbar'});
                        return results;
                    }
                    results.push({test: 'battleAPI_exists', ok: true});

                    // Backend check
                    try {
                        if (ba.checkBackend) {
                            const ok = await ba.checkBackend();
                            results.push({test: 'checkBackend', ok: !!ok});
                        }
                    } catch(e) { results.push({test: 'checkBackend', error: e.message}); }

                    // Battle starten
                    try {
                        if (ba.startBattle) {
                            const status = await ba.startBattle();
                            results.push({test: 'startBattle', ok: !!status, data: status ? 'gestartet' : 'null'});

                            // Wenn Battle laeuft, Aktion ausfuehren
                            if (status) {
                                try {
                                    const actionResult = await ba.executeAction('attack');
                                    results.push({test: 'executeAction_attack', ok: !!actionResult});
                                } catch(e) {
                                    results.push({test: 'executeAction_attack', error: e.message});
                                }

                                // Battle beenden
                                try {
                                    if (ba.resetBattle) ba.resetBattle();
                                    results.push({test: 'resetBattle', ok: true});
                                } catch(e) { results.push({test: 'resetBattle', error: e.message}); }
                            }
                        }
                    } catch(e) { results.push({test: 'startBattle', error: e.message}); }

                    return results;
                }
            """)

            for r in battle_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Battle: {r['error']}")
                    else:
                        log_fail(f"Battle {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    log_pass(f"Battle {r['test']}")
                else:
                    log_warn(f"Battle {r['test']} ok=False")
        except Exception as e:
            log_fail("Battle/Combat", str(e)[:60])

        # ============================================================
        # TEST 21: Fishing System
        # ============================================================
        print("\n--- TEST 21: Fishing ---")

        try:
            fishing_test = page.evaluate("""
                () => {
                    const results = [];
                    const fs = window.FishingSystem;
                    if (!fs) return [{test: 'FishingSystem', error: 'nicht verfuegbar'}];
                    results.push({test: 'FishingSystem_exists', ok: true});

                    // Collection
                    try {
                        const col = fs.getCollection ? fs.getCollection() : null;
                        results.push({test: 'getCollection', ok: col !== null});
                    } catch(e) { results.push({test: 'getCollection', error: e.message}); }

                    // Collection Progress
                    try {
                        const prog = fs.getCollectionProgress ? fs.getCollectionProgress() : null;
                        results.push({test: 'getCollectionProgress', ok: prog !== null, value: prog});
                    } catch(e) { results.push({test: 'getCollectionProgress', error: e.message}); }

                    // Inventory
                    try {
                        const inv = fs.getInventory ? fs.getInventory() : null;
                        results.push({test: 'getInventory', ok: inv !== null});
                    } catch(e) { results.push({test: 'getInventory', error: e.message}); }

                    // Equipped Rod
                    try {
                        const rod = fs.getEquippedRod ? fs.getEquippedRod() : null;
                        results.push({test: 'getEquippedRod', ok: true, value: rod});
                    } catch(e) { results.push({test: 'getEquippedRod', error: e.message}); }

                    return results;
                }
            """)

            for r in fishing_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Fishing: {r['error']}")
                    else:
                        log_fail(f"Fishing {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = f" (={r['value']})" if "value" in r else ""
                    log_pass(f"Fishing {r['test']}{extra}")
                else:
                    log_fail(f"Fishing {r['test']}", "ok=False")
        except Exception as e:
            log_fail("Fishing", str(e)[:60])

        # ============================================================
        # TEST 22: Garden/Farming System
        # ============================================================
        print("\n--- TEST 22: Garden/Farming ---")

        try:
            garden_test = page.evaluate("""
                () => {
                    const results = [];
                    const gs = window.GardenSystem;
                    if (!gs) return [{test: 'GardenSystem', error: 'nicht verfuegbar'}];
                    results.push({test: 'GardenSystem_exists', ok: true});

                    // Current Region
                    try {
                        const reg = gs.getCurrentRegion ? gs.getCurrentRegion() : null;
                        results.push({test: 'getCurrentRegion', ok: true, value: reg});
                    } catch(e) { results.push({test: 'getCurrentRegion', error: e.message}); }

                    // All Regions
                    try {
                        const regs = gs.getAllRegions ? gs.getAllRegions() : null;
                        results.push({test: 'getAllRegions', ok: regs !== null, count: regs ? (Array.isArray(regs) ? regs.length : Object.keys(regs).length) : 0});
                    } catch(e) { results.push({test: 'getAllRegions', error: e.message}); }

                    // Unlocked Regions
                    try {
                        const unlocked = gs.getUnlockedRegions ? gs.getUnlockedRegions() : null;
                        results.push({test: 'getUnlockedRegions', ok: unlocked !== null, count: unlocked ? unlocked.length : 0});
                    } catch(e) { results.push({test: 'getUnlockedRegions', error: e.message}); }

                    // Plot States
                    try {
                        const plots = gs.getPlotStates ? gs.getPlotStates() : null;
                        results.push({test: 'getPlotStates', ok: plots !== null});
                    } catch(e) { results.push({test: 'getPlotStates', error: e.message}); }

                    // Available Crops
                    try {
                        const crops = gs.getAvailableCrops ? gs.getAvailableCrops() : null;
                        results.push({test: 'getAvailableCrops', ok: crops !== null, count: crops ? crops.length : 0});
                    } catch(e) { results.push({test: 'getAvailableCrops', error: e.message}); }

                    return results;
                }
            """)

            for r in garden_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Garden: {r['error']}")
                    else:
                        log_fail(f"Garden {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = ""
                    if "value" in r: extra = f" (={r['value']})"
                    elif "count" in r: extra = f" ({r['count']})"
                    log_pass(f"Garden {r['test']}{extra}")
                else:
                    log_fail(f"Garden {r['test']}", "ok=False")
        except Exception as e:
            log_fail("Garden/Farming", str(e)[:60])

        # ============================================================
        # TEST 23: Housing System
        # ============================================================
        print("\n--- TEST 23: Housing ---")

        try:
            housing_test = page.evaluate("""
                () => {
                    const results = [];
                    const hs = window.HousingSystem;
                    if (!hs) return [{test: 'HousingSystem', error: 'nicht verfuegbar'}];
                    results.push({test: 'HousingSystem_exists', ok: true});

                    // State
                    try {
                        const state = hs.getState ? hs.getState() : null;
                        results.push({test: 'getState', ok: state !== null});
                    } catch(e) { results.push({test: 'getState', error: e.message}); }

                    // Catalog
                    try {
                        const cat = hs.getCatalog ? hs.getCatalog() : null;
                        results.push({test: 'getCatalog', ok: cat !== null, count: cat ? (Array.isArray(cat) ? cat.length : Object.keys(cat).length) : 0});
                    } catch(e) { results.push({test: 'getCatalog', error: e.message}); }

                    // Rooms
                    try {
                        const rooms = hs.getRooms ? hs.getRooms() : null;
                        results.push({test: 'getRooms', ok: rooms !== null, count: rooms ? (Array.isArray(rooms) ? rooms.length : Object.keys(rooms).length) : 0});
                    } catch(e) { results.push({test: 'getRooms', error: e.message}); }

                    return results;
                }
            """)

            for r in housing_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Housing: {r['error']}")
                    else:
                        log_fail(f"Housing {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = f" ({r['count']})" if "count" in r else ""
                    log_pass(f"Housing {r['test']}{extra}")
                else:
                    log_fail(f"Housing {r['test']}", "ok=False")
        except Exception as e:
            log_fail("Housing", str(e)[:60])

        # ============================================================
        # TEST 24: Crafting System
        # ============================================================
        print("\n--- TEST 24: Crafting ---")

        try:
            crafting_test = page.evaluate("""
                () => {
                    const results = [];
                    const cm = window.CraftingMinigame;
                    if (!cm) return [{test: 'CraftingMinigame', error: 'nicht verfuegbar'}];
                    results.push({test: 'CraftingMinigame_exists', ok: true});

                    // Recipes
                    try {
                        const recipes = cm.RECIPES || null;
                        const count = recipes ? Object.keys(recipes).length : 0;
                        results.push({test: 'RECIPES', ok: count > 0, count: count});
                    } catch(e) { results.push({test: 'RECIPES', error: e.message}); }

                    // Open/Close
                    try {
                        if (cm.open) cm.open();
                        results.push({test: 'open', ok: true});
                    } catch(e) { results.push({test: 'open', error: e.message}); }

                    try {
                        if (cm.close) cm.close();
                        results.push({test: 'close', ok: true});
                    } catch(e) { results.push({test: 'close', error: e.message}); }

                    return results;
                }
            """)

            for r in crafting_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Crafting: {r['error']}")
                    else:
                        log_fail(f"Crafting {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = f" ({r['count']})" if "count" in r else ""
                    log_pass(f"Crafting {r['test']}{extra}")
                else:
                    log_fail(f"Crafting {r['test']}", "ok=False")

            page.keyboard.press("Escape")
            time.sleep(0.2)
        except Exception as e:
            log_fail("Crafting", str(e)[:60])

        # ============================================================
        # TEST 25: Dungeon Crawler
        # ============================================================
        print("\n--- TEST 25: Dungeon Crawler ---")

        try:
            dungeon_test = page.evaluate("""
                () => {
                    const results = [];

                    // DungeonGenerator
                    const dg = window.DungeonGenerator;
                    if (dg) {
                        results.push({test: 'DungeonGenerator_exists', ok: true});
                    } else {
                        results.push({test: 'DungeonGenerator', error: 'nicht verfuegbar'});
                    }

                    // DungeonCrawler
                    const dc = window.DungeonCrawler;
                    if (dc) {
                        results.push({test: 'DungeonCrawler_exists', ok: true});

                        // isActive
                        try {
                            const active = dc.isActive;
                            results.push({test: 'isActive', ok: true, value: active});
                        } catch(e) { results.push({test: 'isActive', error: e.message}); }

                        // Enter/Exit Dungeon (kurz testen)
                        try {
                            dc.enterCrawlerDungeon(1);
                            const inDungeon = dc.isActive;
                            results.push({test: 'enterCrawlerDungeon', ok: inDungeon});

                            if (inDungeon) {
                                const stats = dc.stats;
                                results.push({test: 'dungeon_stats', ok: stats !== null});

                                dc.exitCrawlerDungeon();
                                results.push({test: 'exitCrawlerDungeon', ok: !dc.isActive});
                            }
                        } catch(e) { results.push({test: 'enterCrawlerDungeon', error: e.message}); }
                    } else {
                        results.push({test: 'DungeonCrawler', error: 'nicht verfuegbar'});
                    }

                    return results;
                }
            """)

            for r in dungeon_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Dungeon: {r['error']}")
                    else:
                        log_fail(f"Dungeon {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = f" (={r['value']})" if "value" in r else ""
                    log_pass(f"Dungeon {r['test']}{extra}")
                else:
                    log_fail(f"Dungeon {r['test']}", "ok=False")

            time.sleep(0.5)
        except Exception as e:
            log_fail("Dungeon Crawler", str(e)[:60])

        # ============================================================
        # TEST 26: Overworld Enemies
        # ============================================================
        print("\n--- TEST 26: Overworld Enemies ---")

        try:
            enemy_test = page.evaluate("""
                () => {
                    const results = [];
                    const oe = window.OverworldEnemies;
                    if (!oe) return [{test: 'OverworldEnemies', error: 'nicht verfuegbar'}];
                    results.push({test: 'OverworldEnemies_exists', ok: true});

                    // Active Enemies
                    try {
                        const active = oe.getActiveEnemies ? oe.getActiveEnemies() : null;
                        results.push({test: 'getActiveEnemies', ok: active !== null, count: active ? active.length : 0});
                    } catch(e) { results.push({test: 'getActiveEnemies', error: e.message}); }

                    // Current Biome
                    try {
                        const biome = oe.getCurrentBiome ? oe.getCurrentBiome() : null;
                        results.push({test: 'getCurrentBiome', ok: biome !== null, value: biome});
                    } catch(e) { results.push({test: 'getCurrentBiome', error: e.message}); }

                    // Player Level
                    try {
                        const lvl = oe.getPlayerLevel ? oe.getPlayerLevel() : null;
                        results.push({test: 'getPlayerLevel', ok: lvl !== null, value: lvl});
                    } catch(e) { results.push({test: 'getPlayerLevel', error: e.message}); }

                    // Debug Spawn
                    try {
                        if (oe.debugSpawn) {
                            oe.debugSpawn('samtmoos');
                            results.push({test: 'debugSpawn', ok: true});
                        }
                    } catch(e) { results.push({test: 'debugSpawn', error: e.message}); }

                    // Clear
                    try {
                        if (oe.clearAll) {
                            oe.clearAll();
                            results.push({test: 'clearAll', ok: true});
                        }
                    } catch(e) { results.push({test: 'clearAll', error: e.message}); }

                    return results;
                }
            """)

            for r in enemy_test:
                if r.get("error"):
                    if "nicht verfuegbar" in str(r.get("error","")):
                        log_warn(f"Enemies: {r['error']}")
                    else:
                        log_fail(f"Enemies {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = ""
                    if "value" in r: extra = f" (={r['value']})"
                    elif "count" in r: extra = f" ({r['count']})"
                    log_pass(f"Enemies {r['test']}{extra}")
                else:
                    log_fail(f"Enemies {r['test']}", "ok=False")
        except Exception as e:
            log_fail("Overworld Enemies", str(e)[:60])

        # ============================================================
        # TEST 27: Player State / XP
        # ============================================================
        print("\n--- TEST 27: Player State ---")

        try:
            player_test = page.evaluate("""
                () => {
                    const results = [];

                    // Player-Objekt
                    try {
                        const pid = window.getPlayerId ? window.getPlayerId() : null;
                        results.push({test: 'getPlayerId', ok: pid !== null, value: pid});
                    } catch(e) { results.push({test: 'getPlayerId', error: e.message}); }

                    // XP Info
                    try {
                        const xp = window.getPlayerXPInfo ? window.getPlayerXPInfo() : null;
                        results.push({test: 'getPlayerXPInfo', ok: xp !== null,
                            level: xp?.level, xp: xp?.xp});
                    } catch(e) { results.push({test: 'getPlayerXPInfo', error: e.message}); }

                    // Player gold
                    try {
                        const gold = window.player?.gold ?? window.playerGold ?? null;
                        results.push({test: 'player_gold', ok: gold !== null, value: gold});
                    } catch(e) { results.push({test: 'player_gold', error: e.message}); }

                    return results;
                }
            """)

            for r in player_test:
                if r.get("error"):
                    log_fail(f"Player {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = ""
                    if "value" in r: extra = f" (={r['value']})"
                    elif "level" in r: extra = f" (Lvl={r.get('level','?')} XP={r.get('xp','?')})"
                    log_pass(f"Player {r['test']}{extra}")
                else:
                    log_warn(f"Player {r['test']} not available")
        except Exception as e:
            log_fail("Player State", str(e)[:60])

        # ============================================================
        # TEST 28: Gebaeude betreten / verlassen
        # ============================================================
        print("\n--- TEST 28: Gebaeude ---")

        try:
            building_test = page.evaluate("""
                () => {
                    const results = [];
                    const s3d = window.Scene3D;
                    if (!s3d) return [{test: 'Scene3D', error: 'nicht verfuegbar'}];

                    // Gebaeude betreten
                    try {
                        if (s3d.loadBuildingInterior) {
                            s3d.loadBuildingInterior('Schwarze Muehle');
                            results.push({test: 'loadBuildingInterior', ok: true});
                        } else {
                            results.push({test: 'loadBuildingInterior', error: 'function not found'});
                        }
                    } catch(e) { results.push({test: 'loadBuildingInterior', error: e.message}); }

                    // Muehle Stockwerke
                    try {
                        if (s3d.muehleFloors && s3d.muehleFloors.length > 0) {
                            results.push({test: 'muehleFloors', ok: true, count: s3d.muehleFloors.length});
                        }
                    } catch(e) { results.push({test: 'muehleFloors', error: e.message}); }

                    // Current Floor
                    try {
                        const floor = s3d.currentFloor;
                        results.push({test: 'currentFloor', ok: floor !== undefined, value: floor});
                    } catch(e) { results.push({test: 'currentFloor', error: e.message}); }

                    // Gebaeude verlassen
                    try {
                        if (s3d.exitBuilding) {
                            s3d.exitBuilding();
                            results.push({test: 'exitBuilding', ok: true});
                        }
                    } catch(e) { results.push({test: 'exitBuilding', error: e.message}); }

                    return results;
                }
            """)

            for r in building_test:
                if r.get("error"):
                    log_fail(f"Gebaeude {r['test']}", r["error"][:60])
                elif r.get("ok"):
                    extra = ""
                    if "count" in r: extra = f" ({r['count']} Stockwerke)"
                    elif "value" in r: extra = f" (={r['value']})"
                    log_pass(f"Gebaeude {r['test']}{extra}")
                else:
                    log_fail(f"Gebaeude {r['test']}", "ok=False")

            time.sleep(1)
        except Exception as e:
            log_fail("Gebaeude", str(e)[:60])

        # ============================================================
        # TEST 29: NPC Dialog System
        # ============================================================
        print("\n--- TEST 29: NPC Dialog ---")

        try:
            npc_test = page.evaluate("""
                () => {
                    const results = [];

                    // NPC System
                    const npc = window.npcSystem || window.NPCInteractionSystem;
                    if (npc) {
                        results.push({test: 'npcSystem_exists', ok: true});
                    } else {
                        results.push({test: 'npcSystem', error: 'nicht verfuegbar'});
                    }

                    // NPC Dialogue System
                    const dlg = window.npcDialogueSystem;
                    if (dlg) {
                        results.push({test: 'npcDialogueSystem_exists', ok: true});
                        try {
                            if (dlg.closeDialogue) dlg.closeDialogue();
                            results.push({test: 'closeDialogue', ok: true});
                        } catch(e) {}
                    } else {
                        results.push({test: 'npcDialogueSystem', error: 'nicht verfuegbar'});
                    }

                    return results;
                }
            """)

            for r in npc_test:
                if r.get("error"):
                    log_warn(f"NPC: {r['error']}")
                elif r.get("ok"):
                    log_pass(f"NPC {r['test']}")
        except Exception as e:
            log_fail("NPC Dialog", str(e)[:60])

        # ============================================================
        # TEST 30: Alle Gameplay-Globals vorhanden
        # ============================================================
        print("\n--- TEST 30: Gameplay-Globals ---")

        gameplay_globals = page.evaluate("""
            () => {
                const checks = {
                    'TeleporterSystem': !!window.TeleporterSystem,
                    'battleAPI': !!window.battleAPI,
                    'FishingSystem': !!window.FishingSystem,
                    'GardenSystem': !!window.GardenSystem,
                    'HousingSystem': !!window.HousingSystem,
                    'CraftingMinigame': !!window.CraftingMinigame,
                    'DungeonCrawler': !!window.DungeonCrawler,
                    'DungeonGenerator': !!window.DungeonGenerator,
                    'OverworldEnemies': !!window.OverworldEnemies,
                    'SurvivalSystem': !!window.SurvivalSystem,
                    'slimeCompanion': !!window.slimeCompanion,
                    'inventoryUI': !!window.inventoryUI,
                    'questUI': !!window.questUI,
                    'TripleTriadUI': !!window.TripleTriadUI,
                    'WeightSystem': !!window.WeightSystem,
                    'EconomySystem': !!window.EconomySystem,
                    'FactionSystem': !!window.FactionSystem,
                    'CareerSystem': !!window.CareerSystem,
                    'DeathSystem': !!window.DeathSystem,
                    'CompanionSwapSystem': !!window.CompanionSwapSystem,
                };
                return checks;
            }
        """)

        for name, exists in gameplay_globals.items():
            if exists:
                log_pass(f"window.{name}")
            else:
                log_warn(f"window.{name} nicht vorhanden")

        # ============================================================
        # TEST 31: Console Errors auswerten
        # ============================================================
        print("\n--- TEST 31: Console Errors ---")

        time.sleep(2)

        # Filtere irrelevante
        real_errors = [e for e in console_errors if
            "favicon" not in e.lower() and
            "serviceworker" not in e.lower() and
            "manifest" not in e.lower() and
            "devtools" not in e.lower() and
            "downloadable font" not in e.lower() and
            "woff" not in e.lower()]

        json_errors = [e for e in real_errors if "JSON" in e or "SyntaxError" in e or "Unexpected token" in e]
        api_errors = [e for e in real_errors if "fetch" in e.lower() or "api" in e.lower() or "404" in e]
        other_errors = [e for e in real_errors if e not in json_errors and e not in api_errors]

        if json_errors:
            log_fail(f"JSON Parse Errors: {len(json_errors)}")
            for e in json_errors[:5]:
                print(f"    -> {e[:150]}")
        else:
            log_pass("KEINE JSON Parse Errors!")

        if api_errors:
            log_warn(f"{len(api_errors)} API-bezogene Errors")
            for e in api_errors[:5]:
                print(f"    -> {e[:150]}")
        else:
            log_pass("Keine API Errors")

        print(f"\n  Gesamt Console: {len(console_errors)} errors, {len(console_warnings)} warnings")
        if other_errors:
            print(f"  Andere Errors ({len(other_errors)}):")
            for e in other_errors[:8]:
                print(f"    -> {e[:150]}")

        if network_errors:
            print(f"\n  Network Errors ({len(network_errors)}):")
            for e in network_errors[:5]:
                print(f"    -> {e[:150]}")

        # ============================================================
        # ERGEBNIS
        # ============================================================
        print("\n" + "=" * 60)
        print("ERGEBNIS")
        print("=" * 60)
        print(f"  Bestanden:       {RESULTS['passed']}")
        print(f"  Fehlgeschlagen:  {RESULTS['failed']}")
        print(f"  Warnungen:       {len(RESULTS['warnings'])}")

        if RESULTS["errors"]:
            print(f"\n  FEHLER ({len(RESULTS['errors'])}):")
            for e in RESULTS["errors"]:
                print(f"    - {e[:120]}")

        total = RESULTS["passed"] + RESULTS["failed"]
        pct = (RESULTS["passed"] / total * 100) if total > 0 else 0

        if pct >= 90:
            grade = "SEHR GUT"
        elif pct >= 75:
            grade = "GUT"
        elif pct >= 50:
            grade = "OKAY"
        else:
            grade = "SCHLECHT"

        print(f"\n  Erfolgsrate: {pct:.1f}% ({RESULTS['passed']}/{total}) - {grade}")
        print("=" * 60)

        # Screenshot machen
        page.screenshot(path="test_screenshot.png", full_page=False)
        print("\nScreenshot gespeichert: test_screenshot.png")

        print("Browser bleibt 8 Sekunden offen...")
        time.sleep(8)
        browser.close()
        print("Test beendet.")

if __name__ == "__main__":
    run_tests()
