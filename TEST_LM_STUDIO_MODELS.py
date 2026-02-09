"""
Test Script um LM Studio Models zu checken
"""
import requests
import json

LM_STUDIO_URL = "http://localhost:1234/v1"

print("=" * 60)
print("LM STUDIO MODEL CHECK")
print("=" * 60)

try:
    # 1. Check if LM Studio is running
    print("\n[1/3] Checking LM Studio connection...")
    response = requests.get(f"{LM_STUDIO_URL}/models", timeout=5)

    if response.status_code == 200:
        print("✅ LM Studio is running!")

        # 2. List available models
        print("\n[2/3] Available models:")
        models_data = response.json()

        if "data" in models_data:
            models = models_data["data"]
            print(f"\nFound {len(models)} model(s):")
            for i, model in enumerate(models, 1):
                model_id = model.get("id", "unknown")
                print(f"  {i}. {model_id}")
        else:
            print("⚠️ No models found in response")
            print(f"Response: {models_data}")

        # 3. Test chat completion with first model
        if models:
            test_model = models[0].get("id")
            print(f"\n[3/3] Testing chat with model: {test_model}")

            test_payload = {
                "model": test_model,
                "messages": [{"role": "user", "content": "Hallo! Antworte nur mit 'Test erfolgreich!'"}],
                "temperature": 0.7,
                "max_tokens": 50,
                "stream": False
            }

            chat_response = requests.post(
                f"{LM_STUDIO_URL}/chat/completions",
                json=test_payload,
                timeout=30
            )

            if chat_response.status_code == 200:
                result = chat_response.json()
                message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"✅ Chat test successful!")
                print(f"Response: {message}")
            else:
                print(f"❌ Chat test failed: {chat_response.status_code}")
                print(f"Error: {chat_response.text}")
        else:
            print("\n[3/3] No models to test")

    else:
        print(f"❌ LM Studio returned status {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to LM Studio!")
    print("\nMAKE SURE:")
    print("1. LM Studio is open")
    print("2. A model is loaded")
    print("3. Server is started (green button)")
    print("4. Port 1234 is not blocked")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("TIPPS:")
print("=" * 60)
print("1. Model-Namen MÜSSEN EXAKT übereinstimmen!")
print("2. In LM Studio: Check welches Model geladen ist")
print("3. Model-ID aus dem Output oben verwenden")
print("4. In najika_server.py anpassen wenn nötig")
print("=" * 60)
