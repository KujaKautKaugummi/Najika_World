"""
Systematischer Test ALLER Najika Systeme
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
RESULTS = {"passed": [], "failed": [], "warnings": []}

def test(name, func):
    """Test wrapper mit Result tracking"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)
    try:
        result = func()
        if result:
            print(f"✅ PASSED: {name}")
            RESULTS["passed"].append(name)
        else:
            print(f"⚠️ WARNING: {name}")
            RESULTS["warnings"].append(name)
        return result
    except Exception as e:
        print(f"❌ FAILED: {name}")
        print(f"Error: {e}")
        RESULTS["failed"].append(name)
        return False

# =============================================================================
# BACKEND TESTS
# =============================================================================

def test_backend_running():
    """Test 1: Backend läuft"""
    try:
        r = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"Status: {r.status_code}")
        return r.status_code == 200
    except:
        print("Backend nicht erreichbar!")
        return False

def test_najika_status():
    """Test 2: Najika Status API"""
    r = requests.get(f"{BASE_URL}/api/najika/status", timeout=5)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Najika: {data.get('najika', {}).get('name', 'Unknown')}")
        print(f"Mood: {data.get('najika', {}).get('mood', 'Unknown')}")
        return True
    return False

def test_temperature_status():
    """Test 3: Temperature System"""
    r = requests.get(f"{BASE_URL}/api/temperature/status", timeout=5)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Temperature: {data.get('temperature', 'N/A')}°C")
        return True
    return False

def test_chat_api():
    """Test 4: Chat API (LM Studio)"""
    payload = {"message": "Test"}
    r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        response = data.get('response', '')
        print(f"Response: {response[:50]}...")
        return len(response) > 0
    else:
        print(f"Error: {r.text[:200]}")
        return False

def test_slime_arena_leaderboard():
    """Test 5: Slime Arena Leaderboard"""
    r = requests.get(f"{BASE_URL}/api/slime-arena/leaderboard?limit=5", timeout=5)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Leaderboard entries: {len(data.get('leaderboard', []))}")
        return True
    return False

def test_slime_arena_start_duel():
    """Test 6: Slime Arena Start Duel"""
    payload = {
        "player_id": "test_player",
        "mode": "normal",
        "combat_mode": "manual"
    }
    r = requests.post(f"{BASE_URL}/api/slime-arena/start-duel", json=payload, timeout=5)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        duel_id = data.get('duel_id')
        print(f"Duel ID: {duel_id}")
        return duel_id is not None
    else:
        print(f"Error: {r.text[:200]}")
        return False

def test_database_tables():
    """Test 7: Database Tables existieren"""
    try:
        from backend.database import engine
        from sqlalchemy import inspect

        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"Total tables: {len(tables)}")

        required_tables = [
            'slime_duels',
            'slime_tournaments',
            'slime_fame',
            'cards',
            'dice_monsters'
        ]

        missing = []
        for table in required_tables:
            if table in tables:
                print(f"  ✅ {table}")
            else:
                print(f"  ❌ {table} MISSING")
                missing.append(table)

        return len(missing) == 0
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

def test_static_files():
    """Test 8: Static Files erreichbar"""
    files = [
        "/digivice/index.html",
        "/digivice/najika_world_UNIFIED.html",
        "/digivice/js/ui/card_game_ui.js",
        "/digivice/js/ui/dice_monsters_ui.js",
        "/digivice/js/ui/housing_ui.js",
        "/digivice/js/ui/slime_arena_ui.js",
        "/digivice/js/3d_dice_system.js"
    ]

    failed = []
    for file in files:
        r = requests.get(f"{BASE_URL}{file}", timeout=5)
        if r.status_code == 200:
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Status {r.status_code}")
            failed.append(file)

    return len(failed) == 0

# =============================================================================
# LM STUDIO TESTS
# =============================================================================

def test_lm_studio_connection():
    """Test 9: LM Studio Connection"""
    try:
        r = requests.get("http://localhost:1234/v1/models", timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            models = data.get('data', [])
            print(f"Models loaded: {len(models)}")
            for model in models:
                print(f"  - {model.get('id')}")
            return len(models) > 0
        return False
    except:
        print("LM Studio nicht erreichbar!")
        return False

def test_lm_studio_chat():
    """Test 10: LM Studio Chat direkt"""
    try:
        payload = {
            "model": "dolphin-2.9.2-qwen2-7b",
            "messages": [{"role": "user", "content": "Sag nur 'OK'"}],
            "max_tokens": 10,
            "temperature": 0.7
        }
        r = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=30
        )
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            response = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"Response: {response}")
            return len(response) > 0
        else:
            print(f"Error: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"LM Studio chat failed: {e}")
        return False

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def run_all_tests():
    """Führt alle Tests aus"""
    print("\n" + "="*60)
    print("NAJIKA WORLD - SYSTEM TEST")
    print("="*60)
    print(f"Zeitstempel: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Backend Tests
    test("Backend Running", test_backend_running)
    test("Najika Status API", test_najika_status)
    test("Temperature API", test_temperature_status)
    test("Chat API", test_chat_api)
    test("Slime Arena Leaderboard", test_slime_arena_leaderboard)
    test("Slime Arena Start Duel", test_slime_arena_start_duel)
    test("Database Tables", test_database_tables)
    test("Static Files", test_static_files)

    # LM Studio Tests
    test("LM Studio Connection", test_lm_studio_connection)
    test("LM Studio Chat Direct", test_lm_studio_chat)

    # Results
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)

    total = len(RESULTS["passed"]) + len(RESULTS["failed"]) + len(RESULTS["warnings"])

    print(f"\n✅ PASSED: {len(RESULTS['passed'])}/{total}")
    for name in RESULTS["passed"]:
        print(f"  ✅ {name}")

    if RESULTS["warnings"]:
        print(f"\n⚠️ WARNINGS: {len(RESULTS['warnings'])}/{total}")
        for name in RESULTS["warnings"]:
            print(f"  ⚠️ {name}")

    if RESULTS["failed"]:
        print(f"\n❌ FAILED: {len(RESULTS['failed'])}/{total}")
        for name in RESULTS["failed"]:
            print(f"  ❌ {name}")

    print("\n" + "="*60)

    if len(RESULTS["failed"]) == 0:
        print("🎉 ALLE TESTS BESTANDEN!")
        if len(RESULTS["warnings"]) > 0:
            print("⚠️ Aber es gibt Warnings zu beachten")
    else:
        print(f"❌ {len(RESULTS['failed'])} Tests fehlgeschlagen")

    print("="*60)

    return len(RESULTS["failed"]) == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
