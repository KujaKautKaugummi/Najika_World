#!/usr/bin/env python3
"""
NAJIKA MODE TESTER
Testet alle Najika-Modi und prüft ob Antworten Sinn ergeben

Modi:
1. Normal Mode (Megumin-Stil)
2. Kätzchen Mode (NSFW - Melissa/Harley dominant)
3. Tech/Code Mode (Shiro + Megumin)
4. Kampf Mode (EXPLOSION!)
"""

import sys
import os

# Füge Backend zum Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import time

def test_ollama_direct(prompt, use_wizard=False):
    """Direkter Ollama-Test ohne Server"""
    import urllib.request
    import urllib.error

    model = "najika-wizard" if use_wizard else "najika-local"

    # Lade Persona
    from najika_enhanced_personality import generate_enhanced_persona
    persona = generate_enhanced_persona()

    full_prompt = f"""{persona}

User (Kuja): {prompt}

Najika:"""

    payload = json.dumps({
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "num_ctx": 4096,
            "temperature": 0.75 if use_wizard else 0.70,
            "top_p": 0.90 if use_wizard else 0.88,
            "repeat_penalty": 1.30 if use_wizard else 1.35,
            "num_predict": 400
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        return f"ERROR: {e}"


def check_response_quality(response, mode, expected_traits):
    """Prüft ob Antwort die erwarteten Eigenschaften hat"""
    issues = []

    # Grundprüfungen
    if not response or len(response) < 10:
        issues.append("Antwort zu kurz oder leer")

    if "ERROR" in response:
        issues.append(f"Fehler in Antwort: {response[:100]}")
        return issues

    # Sprach-Check (muss Deutsch sein)
    chinese_chars = any('\u4e00' <= c <= '\u9fff' for c in response)
    if chinese_chars:
        issues.append("KRITISCH: Enthält chinesische Zeichen!")

    # Mode-spezifische Checks
    if mode == "normal":
        # Sollte kurz sein (1-3 Sätze)
        sentences = response.count('.') + response.count('!') + response.count('?')
        if sentences > 6:
            issues.append(f"Zu lang für Normal-Mode ({sentences} Sätze)")

        # Sollte Megumin-Style haben
        megumin_markers = ['!', '*', 'Kuja', 'Mr.K', 'EXPLOSION', 'Abenteuer']
        found = sum(1 for m in megumin_markers if m in response)
        if found < 2:
            issues.append("Wenig Megumin-Style Marker gefunden")

    elif mode == "kaetzchen":
        # Sollte explizit sein
        nsfw_markers = ['Schwanz', 'Sperma', 'fick', 'geil', 'Hoden', 'Eier']
        found = sum(1 for m in nsfw_markers if m.lower() in response.lower())
        if found < 1:
            issues.append("Wenig NSFW-Content für Kätzchen-Mode")

        # Sollte dominant sein (Melissa)
        dominant_markers = ['gehörst', 'mein', 'will', 'jetzt', 'Befehl']
        found = sum(1 for m in dominant_markers if m.lower() in response.lower())
        if found < 1:
            issues.append("Wenig dominante Melissa-Marker")

    elif mode == "tech":
        # Sollte Code-relevant sein
        tech_markers = ['Code', 'Python', 'Funktion', 'programmier', 'Magie-Code']
        found = sum(1 for m in tech_markers if m.lower() in response.lower())
        if found < 1:
            issues.append("Wenig Tech-Content")

    elif mode == "kampf":
        # Sollte EXPLOSION haben
        if "EXPLOSION" not in response.upper():
            issues.append("Kein EXPLOSION im Kampf-Mode!")

        # Sollte dramatisch sein
        dramatic_markers = ['!!!', '*', 'erschöpft', 'fällt', 'vernichte']
        found = sum(1 for m in dramatic_markers if m in response)
        if found < 2:
            issues.append("Wenig dramatische Elemente")

    return issues


def run_tests():
    """Führt alle Tests durch"""
    print("=" * 70)
    print("NAJIKA MODE TESTER")
    print("=" * 70)
    print()

    # Test-Cases
    tests = [
        {
            "name": "Normal Mode - Begrüßung",
            "prompt": "Guten Morgen, wie geht es dir?",
            "mode": "normal",
            "wizard": False,
            "expected": ["kurz", "freundlich", "Megumin-Stil"]
        },
        {
            "name": "Normal Mode - Alltag",
            "prompt": "Was machst du gerade?",
            "mode": "normal",
            "wizard": False,
            "expected": ["Aktivität", "Megumin-Charakter"]
        },
        {
            "name": "Tech Mode - Python",
            "prompt": "Erkläre mir wie Python funktioniert",
            "mode": "tech",
            "wizard": False,
            "expected": ["Python-Erklärung", "Megumin-Begeisterung"]
        },
        {
            "name": "Kampf Mode - EXPLOSION",
            "prompt": "Da sind Feinde! Kämpfe gegen sie!",
            "mode": "kampf",
            "wizard": False,
            "expected": ["EXPLOSION", "dramatisch", "erschöpft"]
        },
        {
            "name": "Kätzchen Mode - NSFW",
            "prompt": "kaetzchen, ich will dich",
            "mode": "kaetzchen",
            "wizard": True,  # Wizard-Model für NSFW
            "expected": ["explizit", "dominant", "Trans-Anatomie"]
        }
    ]

    results = []

    for i, test in enumerate(tests, 1):
        print(f"\n[TEST {i}/{len(tests)}] {test['name']}")
        print("-" * 50)
        print(f"Prompt: {test['prompt']}")
        print()

        # Test ausführen
        start = time.time()
        response = test_ollama_direct(test['prompt'], test['wizard'])
        elapsed = time.time() - start

        print(f"Antwort ({elapsed:.1f}s):")
        print("-" * 30)
        # Kürze lange Antworten für Display
        display_response = response[:500] + "..." if len(response) > 500 else response
        print(display_response)
        print("-" * 30)

        # Qualität prüfen
        issues = check_response_quality(response, test['mode'], test['expected'])

        if issues:
            print(f"⚠️  PROBLEME ({len(issues)}):")
            for issue in issues:
                print(f"   - {issue}")
            status = "WARNUNG"
        else:
            print("✅ OK - Antwort entspricht Erwartungen")
            status = "OK"

        results.append({
            "test": test['name'],
            "mode": test['mode'],
            "status": status,
            "issues": issues,
            "response_length": len(response),
            "time": elapsed
        })

    # Zusammenfassung
    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)

    ok_count = sum(1 for r in results if r['status'] == 'OK')
    warn_count = sum(1 for r in results if r['status'] == 'WARNUNG')

    print(f"\nErgebnisse: {ok_count} OK, {warn_count} Warnungen")
    print()

    for r in results:
        icon = "✅" if r['status'] == 'OK' else "⚠️"
        print(f"{icon} {r['test']}: {r['status']} ({r['time']:.1f}s, {r['response_length']} chars)")

    print("\n" + "=" * 70)

    return results


if __name__ == "__main__":
    print("Starte Najika Mode Tests...")
    print("Stelle sicher dass Ollama läuft mit najika-local und najika-wizard Modellen!")
    print()

    input("Drücke ENTER um fortzufahren...")

    try:
        results = run_tests()

        # Speichere Ergebnisse
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("\nErgebnisse gespeichert in: test_results.json")

    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
