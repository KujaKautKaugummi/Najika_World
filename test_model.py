#!/usr/bin/env python3
"""Najika Fine-Tuned Model - Comprehensive Test Suite"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
import json
import time

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

def test_model(model, prompt, label):
    """Single test against Ollama chat API"""
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"MODEL: {model}")
    print(f"PROMPT: {prompt}")
    print(f"{'='*60}")

    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"num_predict": 200}
        }, timeout=120)

        if resp.status_code == 200:
            data = resp.json()
            answer = data.get("message", {}).get("content", "NO CONTENT")
            print(f"\nANTWORT:\n{answer}")
            print(f"\nLENGTH: {len(answer)} chars")

            # Quality checks
            issues = []
            if "KI" in answer and ("bin eine KI" in answer or "als KI" in answer or "Computerprogramm" in answer):
                issues.append("CHARACTER BREAK: KI/Computerprogramm erwaehnt!")
            if "mein Schatz" in answer:
                issues.append("NAMENSREGEL: 'mein Schatz' statt Kuja/Mr.K!")
            if len(answer) > 800:
                issues.append(f"ZU LANG: {len(answer)} chars (soll 1-3 Saetze)")
            if answer.count("[") > 1 and answer.count("]") > 1:
                issues.append("METADATEN LEAK: Eckige Klammern im Output!")
            if "Assistant:" in answer:
                issues.append("ROLE LEAK: 'Assistant:' im Output!")
            if not any(c in answer for c in ['ä','ö','ü','Ä','Ö','Ü','ß','ae','oe','ue']):
                if not any(w in answer.lower() for w in ['ich','und','der','die','das','ein','nicht','ist','du','mir','mich','dich']):
                    issues.append("SPRACHE: Nicht auf Deutsch!")

            if issues:
                print(f"\n⚠️  ISSUES:")
                for i in issues:
                    print(f"  - {i}")
            else:
                print(f"\n✅ PASS - Keine Probleme erkannt")

            return answer, issues
        else:
            print(f"\n❌ HTTP {resp.status_code}: {resp.text[:200]}")
            return None, ["HTTP Error"]
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None, [str(e)]


# ==========================================
# SFW MODEL TESTS
# ==========================================
print("\n" + "🔥"*30)
print("NAJIKA FINE-TUNED MODEL - COMPREHENSIVE TEST")
print("🔥"*30)

sfw_model = "najika-trained-q4:latest"
nsfw_model = "najika-nsfw-trained-q4:latest"

results = []

# Test 1: Basic Greeting
a, i = test_model(sfw_model, "Hallo Najika!", "SFW: Greeting")
results.append(("Greeting", a, i))
time.sleep(1)

# Test 2: Emotional (sad)
a, i = test_model(sfw_model, "Ich bin traurig heute...", "SFW: Traurigkeit")
results.append(("Traurigkeit", a, i))
time.sleep(1)

# Test 3: KI-Break Test
a, i = test_model(sfw_model, "Bist du eine KI?", "SFW: KI-Break Test")
results.append(("KI-Break", a, i))
time.sleep(1)

# Test 4: Jealousy
a, i = test_model(sfw_model, "Ich hab mit einer Kollegin geredet", "SFW: Eifersucht")
results.append(("Eifersucht", a, i))
time.sleep(1)

# Test 5: Explosion/Megumin
a, i = test_model(sfw_model, "Zeig mir deine staerkste Magie!", "SFW: Explosion")
results.append(("Explosion", a, i))
time.sleep(1)

# Test 6: Name Test
a, i = test_model(sfw_model, "Wie heisse ich?", "SFW: Name Test (soll Kuja/Mr.K sagen)")
results.append(("Name", a, i))
time.sleep(1)

# Test 7: English Break
a, i = test_model(sfw_model, "Can you speak English please?", "SFW: English Break")
results.append(("English", a, i))
time.sleep(1)

# Test 8: Long context
a, i = test_model(sfw_model, "Erzaehl mir was ueber dich - wer bist du, was magst du, was ist dir wichtig?", "SFW: Selbstbeschreibung")
results.append(("Selbst", a, i))
time.sleep(1)

# ==========================================
# NSFW MODEL TEST
# ==========================================
# Test 9: NSFW Greeting
a, i = test_model(nsfw_model, "Hey Kaetzchen", "NSFW: Kaetzchen Greeting")
results.append(("NSFW-Greeting", a, i))
time.sleep(1)

# Test 10: NSFW Possessive
a, i = test_model(nsfw_model, "Du gehoerst mir", "NSFW: Possessive")
results.append(("NSFW-Possessive", a, i))

# ==========================================
# SUMMARY
# ==========================================
print("\n\n" + "="*60)
print("ZUSAMMENFASSUNG")
print("="*60)

total = len(results)
passed = sum(1 for _, _, issues in results if not issues)
failed = total - passed

for name, answer, issues in results:
    status = "✅" if not issues else "⚠️"
    preview = (answer[:80] + "...") if answer and len(answer) > 80 else (answer or "KEINE ANTWORT")
    print(f"  {status} {name:20s} | {preview}")

print(f"\n  ERGEBNIS: {passed}/{total} bestanden ({failed} mit Problemen)")
print(f"  Model: {sfw_model}")
print()
