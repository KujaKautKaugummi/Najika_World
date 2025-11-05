"""
Najika Backend Test
Version: 2.5
"""
import requests
import json

def test_backend():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing Najika Backend...")
    print()
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Health check
    print("2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Chat endpoint
    print("3. Testing chat endpoint...")
    try:
        response = requests.post(
            f"{base_url}/chat",
            json={"message": "Hallo Najika!", "mode": "public"}
        )
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("🎉 Tests completed!")

if __name__ == "__main__":
    test_backend()
