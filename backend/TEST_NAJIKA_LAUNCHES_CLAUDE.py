#!/usr/bin/env python3
"""
TEST: Najika startet Claude Code eigenständig via API
"""

import requests
import json

print("="*80)
print("TEST: NAJIKA STARTET CLAUDE CODE EIGENSTÄNDIG")
print("="*80)
print()

SERVER_URL = "http://localhost:8001"

# Test 1: Ohne Task
print("[1] Test: Claude Code starten (ohne Task)")
try:
    response = requests.post(
        f"{SERVER_URL}/api/claude_code/launch",
        json={},
        timeout=10
    )

    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")
    print()
except Exception as e:
    print(f"   ERROR: {e}")
    print()

# Test 2: Mit Task
print("[2] Test: Claude Code starten (mit Task)")
try:
    response = requests.post(
        f"{SERVER_URL}/api/claude_code/launch",
        json={
            "task": "Najika braucht Hilfe mit Python Code!"
        },
        timeout=10
    )

    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")
    print()
except Exception as e:
    print(f"   ERROR: {e}")
    print()

print("="*80)
print("ERWARTUNG:")
print("  - Ein oder zwei neue PowerShell-Fenster sollten sich geöffnet haben")
print("  - Darin läuft Claude Code (interaktiv)")
print("="*80)
