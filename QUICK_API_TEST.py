"""
Quick API Test - Check if endpoints are registered
"""

import requests

API_BASE = "http://localhost:8000"

print("\n" + "="*60)
print("QUICK API TEST - Check Registered Routes")
print("="*60 + "\n")

# Test root
try:
    r = requests.get(f"{API_BASE}/", timeout=2)
    print(f"✅ Root endpoint: {r.status_code}")
except Exception as e:
    print(f"❌ Root endpoint failed: {e}")

# Test docs
try:
    r = requests.get(f"{API_BASE}/docs", timeout=2)
    print(f"✅ /docs endpoint: {r.status_code}")
except Exception as e:
    print(f"❌ /docs failed: {e}")

# Test OpenAPI schema
try:
    r = requests.get(f"{API_BASE}/openapi.json", timeout=2)
    if r.status_code == 200:
        data = r.json()
        print(f"\n📋 Registered API Paths:")
        paths = list(data.get("paths", {}).keys())

        # Filter for our new APIs
        new_apis = [p for p in paths if any(x in p for x in ["/special", "/spells/name", "/slime-ai"])]

        if new_apis:
            print("\n✅ NEW APIs FOUND:")
            for path in sorted(new_apis):
                print(f"   {path}")
        else:
            print("\n❌ NEW APIs NOT FOUND!")
            print("\nAll registered paths:")
            for path in sorted(paths)[:20]:  # Show first 20
                print(f"   {path}")

except Exception as e:
    print(f"❌ OpenAPI schema failed: {e}")

print("\n" + "="*60)
