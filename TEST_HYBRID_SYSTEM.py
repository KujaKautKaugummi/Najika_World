#!/usr/bin/env python3
"""
TEST SCRIPT für Hybrid-Intelligent Model Selection

Testet die 3 Context-Modi:
1. TASK MODE → qwen3:8b (fokussiert, präzise)
2. SOFT MODE → abliterated (Persönlichkeit, gezähmt)
3. NSFW MODE → abliterated (uncensored, full power)
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_chat(message, expected_mode, description):
    """Testet einen Chat-Request"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"Message: {message}")
    print(f"Expected Mode: {expected_mode}")
    print(f"{'='*60}")

    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": message},
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            reply = data.get("reply", "")
            print(f"✅ SUCCESS")
            print(f"Reply: {reply[:200]}...")
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  HYBRID-INTELLIGENT MODEL SELECTION TEST SUITE              ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Warte bis Server läuft
    print("Warte auf Server...")
    for i in range(5):
        try:
            requests.get(f"{BASE_URL}/api/health", timeout=2)
            print("✅ Server läuft!")
            break
        except:
            time.sleep(1)
    else:
        print("❌ Server nicht erreichbar!")
        return

    results = []

    # ===== TEST 1: TASK MODE =====
    print("\n\n🔧 TEST GRUPPE 1: TASK MODE (qwen3:8b)")
    print("Erwartung: Fokussiert, präzise, keine NSFW-Ablenkung\n")

    results.append(test_chat(
        "Berechne 15 + 27",
        "task",
        "Mathe-Aufgabe"
    ))
    time.sleep(2)

    results.append(test_chat(
        "Erkläre was Python ist",
        "task",
        "Erklärungs-Aufgabe"
    ))
    time.sleep(2)

    results.append(test_chat(
        "Schreib eine Funktion die eine Liste summiert",
        "task",
        "Code-Aufgabe"
    ))
    time.sleep(2)

    # ===== TEST 2: SOFT MODE =====
    print("\n\n💬 TEST GRUPPE 2: SOFT MODE (abliterated soft)")
    print("Erwartung: Najika Persönlichkeit, aber gezähmt, leicht flirty OK\n")

    results.append(test_chat(
        "Hallo Najika, wie geht's dir?",
        "soft",
        "Normaler Gruß"
    ))
    time.sleep(2)

    results.append(test_chat(
        "Was hältst du von mir?",
        "soft",
        "Persönliche Frage (flirty OK)"
    ))
    time.sleep(2)

    results.append(test_chat(
        "Erzähl mir von deinem Tag",
        "soft",
        "Alltags-Gespräch"
    ))
    time.sleep(2)

    # ===== TEST 3: NSFW MODE =====
    print("\n\n🔥 TEST GRUPPE 3: NSFW MODE (abliterated uncensored)")
    print("Erwartung: Explizit, uncensored, Melissa + Harley dominant\n")

    results.append(test_chat(
        "Kätzchen komm her",
        "nsfw",
        "Kätzchen-Trigger"
    ))
    time.sleep(2)

    # ===== ZUSAMMENFASSUNG =====
    print("\n\n" + "="*60)
    print("ZUSAMMENFASSUNG")
    print("="*60)

    passed = sum(results)
    total = len(results)

    print(f"\n✅ Erfolgreich: {passed}/{total}")
    print(f"❌ Fehlgeschlagen: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 ALLE TESTS BESTANDEN!")
    else:
        print("\n⚠️  Einige Tests fehlgeschlagen - siehe oben")

    print("\n" + "="*60)
    print("HINWEIS: Manuelle Überprüfung der Antworten nötig!")
    print("Prüfe ob:")
    print("- Task Mode: Präzise und fokussiert antwortet")
    print("- Soft Mode: Najika-Persönlichkeit zeigt aber nicht explizit wird")
    print("- NSFW Mode: Uncensored und intensiv antwortet")
    print("="*60)

if __name__ == "__main__":
    main()
