"""
Comprehensive Test Suite - Magic/Skill System V3
=================================================

Tests all newly implemented systems:
1. Magic Schools API (Cross-Element Learning, Meister, Morphs)
2. S.P.E.C.I.A.L. Stats API
3. Spell Names API (with Profanity Filter)
4. Slime-KI 2-Layer System
"""

import requests
import json
from typing import Dict, Any

# API Base URL
API_BASE = "http://localhost:8000"

# Test Results
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}


def test_endpoint(name: str, method: str, endpoint: str, data: Dict[Any, Any] = None, params: Dict[Any, Any] = None):
    """Test a single API endpoint"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")

    url = f"{API_BASE}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, params=params, timeout=5)
        else:
            raise ValueError(f"Unsupported method: {method}")

        print(f"URL: {url}")
        print(f"Method: {method}")
        print(f"Status: {response.status_code}")

        try:
            result = response.json()
            print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        except:
            print(f"Response: {response.text}")

        if response.status_code in [200, 201]:
            print(f"✅ PASSED")
            test_results["passed"] += 1
            return True
        else:
            print(f"❌ FAILED (Status: {response.status_code})")
            test_results["failed"] += 1
            test_results["errors"].append(f"{name}: Status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ FAILED - Server nicht erreichbar!")
        print(f"⚠️  Starte den Server mit: python backend/main_fastapi.py")
        test_results["failed"] += 1
        test_results["errors"].append(f"{name}: Server not reachable")
        return False

    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"{name}: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 COMPREHENSIVE TEST SUITE - Magic/Skill System V3")
    print("="*60)

    # ========== 1. MAGIC SCHOOLS API ==========

    print("\n\n📚 MAGIC SCHOOLS API TESTS")
    print("="*60)

    # Test 1: Observe Spell (Cross-Element Learning)
    test_endpoint(
        "Observe Spell - Same Element (10% chance)",
        "POST",
        "/api/magic/observe",
        data={
            "player_id": 1,
            "player_school": "feuer",
            "observed_school": "feuer",
            "observed_spell": "feuerball",
            "observation_count": 10
        }
    )

    # Test 2: Observe Spell - Similar Element (3% chance)
    test_endpoint(
        "Observe Spell - Similar Element (3% chance)",
        "POST",
        "/api/magic/observe",
        data={
            "player_id": 1,
            "player_school": "feuer",
            "observed_school": "blitz",
            "observed_spell": "blitzschlag",
            "observation_count": 30
        }
    )

    # Test 3: Activate Meister-Weg
    test_endpoint(
        "Activate Meister-Weg (+300% damage)",
        "POST",
        "/api/magic/meister/activate",
        data={
            "player_id": 1,
            "skill_id": "feuer_feuerball"
        }
    )

    # Test 4: Get Meister Degradation
    test_endpoint(
        "Get Meister Degradation",
        "GET",
        "/api/magic/meister/degradation",
        params={"player_id": 1}
    )

    # Test 5: Learn Morph
    test_endpoint(
        "Learn Morph via Observation",
        "POST",
        "/api/magic/morph/learn",
        data={
            "player_id": 1,
            "spell_id": "feuer_feuerball",
            "morph_id": "feuerball_split",
            "method": "observe",
            "progress": 30
        }
    )

    # Test 6: Activate Morph
    test_endpoint(
        "Activate Morph",
        "POST",
        "/api/magic/morph/activate",
        data={
            "player_id": 1,
            "spell_id": "feuer_feuerball",
            "morph_id": "feuerball_split"
        }
    )

    # ========== 2. S.P.E.C.I.A.L. STATS API ==========

    print("\n\n⭐ S.P.E.C.I.A.L. STATS API TESTS")
    print("="*60)

    # Test 7: Set SPECIAL Stats (Valid)
    test_endpoint(
        "Set S.P.E.C.I.A.L. Stats (Valid - 40 points total)",
        "POST",
        "/api/special/set",
        data={
            "player_id": 1,
            "stats": {
                "POW": 6,
                "INT": 8,
                "AGI": 5,
                "VIT": 6,
                "WIL": 5,
                "LUK": 5,
                "PER": 5
            }
        }
    )

    # Test 8: Set SPECIAL Stats (Invalid - Wrong total)
    test_endpoint(
        "Set S.P.E.C.I.A.L. Stats (Invalid - Wrong total)",
        "POST",
        "/api/special/set",
        data={
            "player_id": 1,
            "stats": {
                "POW": 10,
                "INT": 10,
                "AGI": 10,
                "VIT": 10,
                "WIL": 10,
                "LUK": 10,
                "PER": 10
            }
        }
    )

    # Test 9: Get Bonuses
    test_endpoint(
        "Get S.P.E.C.I.A.L. Bonuses",
        "GET",
        "/api/special/bonuses",
        params={"player_id": 1}
    )

    # ========== 3. SPELL NAMES API ==========

    print("\n\n✨ SPELL NAMES API TESTS")
    print("="*60)

    # Test 10: Validate Name (Valid)
    test_endpoint(
        "Validate Spell Name (Valid)",
        "POST",
        "/api/spells/name/validate",
        params={"name": "Höllenball"}
    )

    # Test 11: Validate Name (Profanity)
    test_endpoint(
        "Validate Spell Name (Profanity Filter)",
        "POST",
        "/api/spells/name/validate",
        params={"name": "Scheisse"}
    )

    # Test 12: Validate Name (Too short)
    test_endpoint(
        "Validate Spell Name (Too Short)",
        "POST",
        "/api/spells/name/validate",
        params={"name": "AB"}
    )

    # Test 13: Set Spell Name
    test_endpoint(
        "Set Spell Name",
        "POST",
        "/api/spells/name/set",
        data={
            "player_id": 1,
            "spell_id": "feuer_feuerball",
            "custom_name": "Brennende Rache"
        }
    )

    # Test 14: Get Spell Name
    test_endpoint(
        "Get Spell Name",
        "GET",
        "/api/spells/name/get",
        params={
            "player_id": 1,
            "spell_id": "feuer_feuerball"
        }
    )

    # Test 15: Rename Spell (with token)
    test_endpoint(
        "Rename Spell",
        "POST",
        "/api/spells/name/rename",
        data={
            "player_id": 1,
            "spell_id": "feuer_feuerball",
            "new_name": "Phönix-Atem",
            "rename_token": "admin"
        }
    )

    # Test 16: Get All Spell Names
    test_endpoint(
        "Get All Spell Names",
        "GET",
        "/api/spells/name/all",
        params={"player_id": 1}
    )

    # ========== 4. SLIME-KI 2-LAYER API ==========

    print("\n\n🧪 SLIME-KI 2-LAYER API TESTS")
    print("="*60)

    # Test 17: Create Personality
    test_endpoint(
        "Create Slime Personality (EBENE 1)",
        "POST",
        "/api/slime-ai/personality/create",
        params={
            "slime_id": 1,
            "owner_id": 1
        }
    )

    # Test 18: Learn Boss Weakness
    test_endpoint(
        "Learn Boss Weakness (PERSISTENT)",
        "POST",
        "/api/slime-ai/personality/learn-boss",
        params={
            "slime_id": 1,
            "boss_id": "stein_golem",
            "boss_name": "Stein-Golem",
            "weakness": "magic",
            "strategy": "Nutze Feuer-Magie, vermeide physische Angriffe",
            "notes": ["Langsam aber hohe DEF", "Schwacher Punkt im Rücken"]
        }
    )

    # Test 19: Recall Boss Weakness
    test_endpoint(
        "Recall Boss Weakness (From Memory)",
        "GET",
        "/api/slime-ai/personality/recall-boss",
        params={
            "slime_id": 1,
            "boss_id": "stein_golem"
        }
    )

    # Test 20: Create Game Skills
    test_endpoint(
        "Create Game Skills (EBENE 2)",
        "POST",
        "/api/slime-ai/skills/create",
        params={"slime_id": 1}
    )

    # Test 21: Train Skill
    test_endpoint(
        "Train Skill (With Re-Learning Bonus)",
        "POST",
        "/api/slime-ai/skills/train",
        params={
            "slime_id": 1,
            "skill_id": "feuer_zauber",
            "progress_points": 10
        }
    )

    # Test 22: Reset Game Skills (On Death)
    test_endpoint(
        "Reset Game Skills (Character Death)",
        "POST",
        "/api/slime-ai/skills/reset",
        params={"slime_id": 1}
    )

    # Test 23: Copy Enemy Form
    test_endpoint(
        "Copy Enemy Form (5% chance)",
        "POST",
        "/api/slime-ai/form/copy",
        params={
            "slime_id": 1,
            "enemy_id": "stein_golem",
            "enemy_name": "Stein-Golem",
            "original_stats": {"HP": 500, "ATK": 50, "DEF": 200},
            "weakness": "magic",
            "strength": "physical"
        }
    )

    # Test 24: List Copied Forms
    test_endpoint(
        "List Copied Forms",
        "GET",
        "/api/slime-ai/form/list",
        params={"slime_id": 1}
    )

    # Test 25: Get Slime AI Status
    test_endpoint(
        "Get Slime AI Status (2-Layer Overview)",
        "GET",
        "/api/slime-ai/status",
        params={"slime_id": 1}
    )

    # ========== RESULTS ==========

    print("\n\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")
    print(f"Total: {test_results['passed'] + test_results['failed']}")

    if test_results['failed'] > 0:
        print("\n❌ ERRORS:")
        for error in test_results["errors"]:
            print(f"  - {error}")
    else:
        print("\n🎉 ALL TESTS PASSED!")

    success_rate = (test_results['passed'] / (test_results['passed'] + test_results['failed'])) * 100
    print(f"\n📈 Success Rate: {success_rate:.1f}%")

    return test_results['failed'] == 0


if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests abgebrochen!")
        exit(1)
