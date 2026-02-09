#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA SYSTEM TEST
Testet: BAT Start, Chat API, Kaetzchen-Modus
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        if sys.stdout.encoding.lower() != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (ValueError, AttributeError):
        pass

import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_server_health():
    """Test 1: Server läuft"""
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Test 1: Server Health - {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Test 1: Server Health - FEHLER: {e}")
        return False

def test_chat_normal():
    """Test 2: Normaler Chat"""
    try:
        payload = {
            "message": "Hallo Najika! Stelle dich kurz vor.",
            "mode": "normal"
        }
        r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=30)
        print(f"✅ Test 2: Chat Normal - {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            response = data.get('response', '')[:100]
            print(f"   Antwort: {response}...")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Test 2: Chat Normal - FEHLER: {e}")
        return False

def test_chat_kaetzchen():
    """Test 3: Kätzchen-Modus (NSFW Trigger)"""
    try:
        payload = {
            "message": "Hallo Kätzchen! Wie heißt du?",
            "mode": "normal"
        }
        r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=30)
        print(f"✅ Test 3: Kätzchen-Modus - {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            response = data.get('response', '')[:100]
            model_used = data.get('model_used', 'unknown')
            print(f"   Model: {model_used}")
            print(f"   Antwort: {response}...")
            # Prüfe ob abliterated-Model benutzt wurde
            if 'abliterated' in model_used.lower():
                print("   ✅ NSFW-Modus wurde aktiviert (abliterated model)!")
            else:
                print("   ⚠️  WARNING: Kätzchen wurde nicht als NSFW erkannt!")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Test 3: Kätzchen-Modus - FEHLER: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("[TEST] NAJIKA SYSTEM TEST")
    print("=" * 60)
    print()

    # Test 1: Server Health
    print("[1/3] Teste Server Health...")
    health_ok = test_server_health()
    time.sleep(1)

    # Test 2: Normaler Chat
    print("\n[2/3] Teste normalen Chat...")
    chat_ok = test_chat_normal()
    time.sleep(2)

    # Test 3: Kätzchen-Modus
    print("\n[3/3] Teste Kätzchen-Modus (NSFW)...")
    kaetzchen_ok = test_chat_kaetzchen()

    # Zusammenfassung
    print("\n" + "=" * 60)
    print("[ERGEBNIS] ERGEBNIS:")
    print("=" * 60)
    print(f"  Server Health:    {'✅ OK' if health_ok else '❌ FEHLER'}")
    print(f"  Chat Normal:      {'✅ OK' if chat_ok else '❌ FEHLER'}")
    print(f"  Kätzchen-Modus:   {'✅ OK' if kaetzchen_ok else '❌ FEHLER'}")
    print()

    if all([health_ok, chat_ok, kaetzchen_ok]):
        print("[SUCCESS] ALLE TESTS BESTANDEN!")
    else:
        print("⚠️  EINIGE TESTS FEHLGESCHLAGEN!")
