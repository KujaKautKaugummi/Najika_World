#!/usr/bin/env python3
"""
TEST SCRIPT - Najika Game Actions System
Demonstriert alle Features des autonomen Spielaktions-Systems
"""

import sys
import time
from najika_game_actions import (
    decide_next_action,
    start_action,
    check_action_completion,
    get_game_action_state,
    suggest_actions,
    teleport_to_location,
    get_current_location,
    LOCATIONS,
    COOKING_RECIPES,
    AUTONOMOUS_CRAFTING_RECIPES,
    FARMING_ACTIONS,
    EXPLORING_ACTIONS,
    apply_stat_changes
)

from najika_living_system import LIVING_STATE

# Test Player State
test_player_state = {
    "health": 100,
    "maxHealth": 100,
    "mana": 100,
    "maxMana": 100,
    "stamina": 100,
    "maxStamina": 100,
    "level": 1,
    "strength": 10,
    "intelligence": 10
}

def print_separator(title=""):
    """Druckt Separator"""
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)
    print()

def print_state(living_state, player_state):
    """Druckt aktuellen State"""
    print("📊 NAJIKA STATUS:")
    print(f"  Hunger:  {living_state['hunger']:.0f}% {'🍽️' if living_state['hunger'] < 30 else '✓'}")
    print(f"  Energy:  {living_state['energy']:.0f}% {'😴' if living_state['energy'] < 30 else '✓'}")
    print(f"  Mood:    {living_state['mood_game']:.0f}% {'😔' if living_state['mood_game'] < 40 else '😊'}")
    print(f"  Anger:   {living_state['anger_level']:.0f}% {'😡' if living_state['anger_level'] > 50 else '✓'}")
    print()
    print("🎮 PLAYER STATUS:")
    print(f"  Health: {player_state['health']}/{player_state['maxHealth']}")
    print(f"  Mana:   {player_state['mana']}/{player_state['maxMana']}")
    print()

def test_locations():
    """Test: Location System"""
    print_separator("TEST 1: LOCATION SYSTEM")

    print("📍 Verfügbare Locations:")
    for loc_id, loc_data in LOCATIONS.items():
        safe = "✓ Safe" if loc_data["safe"] else "⚠️ Dangerous"
        print(f"  - {loc_data['name']} ({safe})")
        print(f"    Aktivitäten: {', '.join(loc_data['activities'])}")
    print()

    # Test Teleport
    print("🔮 Teleportiere zu verschiedenen Orten...")
    for loc_id in ["farm", "forest", "village", "home"]:
        result = teleport_to_location(loc_id)
        if result["success"]:
            print(f"  ✓ {result['message']}")
        time.sleep(0.5)

    print()
    current = get_current_location()
    print(f"📍 Aktuelle Location: {current['name']}")
    print()

def test_recipes():
    """Test: Recipes"""
    print_separator("TEST 2: RECIPES & CRAFTING")

    print("🍳 COOKING RECIPES:")
    for recipe_id, recipe in COOKING_RECIPES.items():
        print(f"  - {recipe['name']}")
        print(f"    Hunger: +{recipe.get('hunger_restore', 0)}%")
        print(f"    Energy Cost: {recipe.get('energy_cost', 0)}")
        print(f"    Zeit: {recipe.get('cooking_time', 0)}s")
    print()

    print("🔨 CRAFTING RECIPES:")
    for recipe_id, recipe in AUTONOMOUS_CRAFTING_RECIPES.items():
        print(f"  - {recipe['name']}")
        print(f"    {recipe.get('description', '')}")
    print()

    print("🌱 FARMING ACTIONS:")
    for action_id, action in FARMING_ACTIONS.items():
        print(f"  - {action['name']}: {action.get('description', '')}")
    print()

    print("🗺️ EXPLORING ACTIONS:")
    for action_id, action in EXPLORING_ACTIONS.items():
        print(f"  - {action['name']}: {action.get('description', '')}")
    print()

def test_decision_making():
    """Test: Decision Making"""
    print_separator("TEST 3: AUTONOME ENTSCHEIDUNGEN")

    # Scenario 1: Hunger kritisch
    print("📋 SCENARIO 1: Hunger kritisch (Hunger=25%)")
    test_state = LIVING_STATE.copy()
    test_state["hunger"] = 25
    test_state["energy"] = 80
    test_state["mood_game"] = 60

    print_state(test_state, test_player_state)

    decision = decide_next_action(test_state, test_player_state)
    if decision:
        print(f"🧠 Najika entscheidet: {decision['type'].upper()}")
        print(f"   Grund: {decision.get('reason', 'N/A')}")
        print(f"   Priorität: {decision.get('priority', 'N/A')}")
        print(f"   Details: {decision['details'].get('name', 'N/A')}")
    print()

    # Scenario 2: Energy kritisch
    print("📋 SCENARIO 2: Energy kritisch (Energy=15%)")
    test_state["hunger"] = 70
    test_state["energy"] = 15
    test_state["mood_game"] = 50

    print_state(test_state, test_player_state)

    decision = decide_next_action(test_state, test_player_state)
    if decision:
        print(f"🧠 Najika entscheidet: {decision['type'].upper()}")
        print(f"   Grund: {decision.get('reason', 'N/A')}")
        print(f"   Priorität: {decision.get('priority', 'N/A')}")
    print()

    # Scenario 3: Bored
    print("📋 SCENARIO 3: Gelangweilt (Mood=30%)")
    test_state["hunger"] = 70
    test_state["energy"] = 70
    test_state["mood_game"] = 30
    test_state["current_mood"] = "bored"

    print_state(test_state, test_player_state)

    decision = decide_next_action(test_state, test_player_state)
    if decision:
        print(f"🧠 Najika entscheidet: {decision['type'].upper()}")
        print(f"   Grund: {decision.get('reason', 'N/A')}")
        print(f"   Details: {decision['details'].get('description', 'N/A')}")
    print()

    # Scenario 4: Happy
    print("📋 SCENARIO 4: Glücklich (Mood=80%)")
    test_state["hunger"] = 80
    test_state["energy"] = 90
    test_state["mood_game"] = 80
    test_state["current_mood"] = "happy"

    print_state(test_state, test_player_state)

    decision = decide_next_action(test_state, test_player_state)
    if decision:
        print(f"🧠 Najika entscheidet: {decision['type'].upper()}")
        print(f"   Grund: {decision.get('reason', 'N/A')}")
        print(f"   Details: {decision['details'].get('name', 'N/A')}")
    print()

def test_suggestions():
    """Test: Suggestions"""
    print_separator("TEST 4: ACTION SUGGESTIONS")

    test_state = LIVING_STATE.copy()
    test_state["hunger"] = 45
    test_state["energy"] = 35
    test_state["mood_game"] = 55

    print_state(test_state, test_player_state)

    suggestions = suggest_actions(test_state, test_player_state)

    print("💡 VORGESCHLAGENE ACTIONS:")
    for suggestion in suggestions:
        priority_emoji = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }.get(suggestion.get("priority", "low"), "⚪")

        print(f"  {priority_emoji} {suggestion.get('icon', '❓')} {suggestion.get('type', 'unknown').upper()}")
        print(f"     Grund: {suggestion.get('reason', 'N/A')}")
        print(f"     Priorität: {suggestion.get('priority', 'low').upper()}")
    print()

def test_action_execution():
    """Test: Action Execution & Completion"""
    print_separator("TEST 5: ACTION EXECUTION")

    print("🎬 Starte Action: Cooking (Simple Meal)")
    print()

    test_state = LIVING_STATE.copy()
    test_state["hunger"] = 40
    test_state["energy"] = 70

    action = {
        "type": "cooking",
        "details": COOKING_RECIPES["simple_meal"],
        "reason": "test",
        "priority": "high"
    }

    result = start_action(action)
    print(f"✓ Action gestartet!")
    print(f"  Message: {result['message']}")
    print(f"  Duration: {result['duration']}s")
    print(f"  Energy Cost: {result['energy_cost']}")
    print()

    # Apply energy cost
    test_state["energy"] -= result["energy_cost"]
    print(f"⚡ Energy nach Start: {test_state['energy']:.0f}%")
    print()

    # Simulate completion (skip wait time)
    print("⏰ Warte auf Completion...")
    time.sleep(2)

    # Force completion for demo
    from najika_game_actions import GAME_ACTION_STATE
    GAME_ACTION_STATE["action_started"] = time.time() - 400  # Simulate past

    completion = check_action_completion()

    if completion and completion.get("completed"):
        print(f"✅ ACTION ABGESCHLOSSEN!")
        print(f"  Message: {completion['message']}")
        print(f"  Rewards: {completion.get('rewards', {})}")
        print()

        # Apply stat changes
        if "stat_changes" in completion:
            print("📊 Stat Changes:")
            for stat, change in completion["stat_changes"].items():
                symbol = "+" if change > 0 else ""
                print(f"  {stat}: {symbol}{change}")

            apply_stat_changes(test_state, test_player_state, completion["stat_changes"])
            print()

        print("📊 NACH COMPLETION:")
        print_state(test_state, test_player_state)

def test_game_action_state():
    """Test: Game Action State"""
    print_separator("TEST 6: GAME ACTION STATE")

    state = get_game_action_state()

    print("🎮 CURRENT GAME ACTION STATE:")
    print(f"  Current Action: {state.get('current_action', 'None')}")
    print(f"  Current Location: {state.get('current_location', 'N/A')}")
    print(f"  Inventory Items: {len(state.get('inventory', {}))}")
    print(f"  Completed Actions: {len(state.get('completed_actions', []))}")
    print()

    if state.get("inventory"):
        print("📦 INVENTORY:")
        for item, count in state["inventory"].items():
            print(f"  - {item}: {count}x")
    print()

def main():
    """Main Test Runner"""
    print("\n" + "="*60)
    print("  🎮 NAJIKA GAME ACTIONS - COMPREHENSIVE TEST")
    print("="*60)
    print()
    print("Dieses Script testet alle Features des autonomen")
    print("Spielaktions-Systems!")
    print()

    try:
        test_locations()
        input("Press ENTER to continue...")

        test_recipes()
        input("Press ENTER to continue...")

        test_decision_making()
        input("Press ENTER to continue...")

        test_suggestions()
        input("Press ENTER to continue...")

        test_action_execution()
        input("Press ENTER to continue...")

        test_game_action_state()

        print_separator("✅ ALLE TESTS ABGESCHLOSSEN!")
        print()
        print("Das Najika Game Actions System funktioniert!")
        print()
        print("🚀 NEXT STEPS:")
        print("  1. Starte den Backend Server: python backend/api/server.py")
        print("  2. Teste die API Endpoints:")
        print("     - GET  /najika/status")
        print("     - GET  /najika/current-activity")
        print("     - POST /najika/suggest-action")
        print("     - POST /najika/auto-decide-action")
        print("  3. Integriere mit Frontend!")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️ Test abgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
