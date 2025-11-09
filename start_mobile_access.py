"""
Start Najika with Mobile Access
Starts the server and Cloudflare tunnel, displays mobile URL
"""

import subprocess
import time
import re
import sys

print("="*60)
print("   NAJIKA - MOBILE ACCESS")
print("="*60)
print()

# Step 1: Kill old processes
print("[1/3] Stopping old servers...")
try:
    subprocess.run(["taskkill", "/F", "/IM", "python.exe"],
                   capture_output=True, timeout=5)
    subprocess.run(["taskkill", "/F", "/IM", "cloudflared.exe"],
                   capture_output=True, timeout=5)
    time.sleep(2)
except:
    pass

# Step 2: Start Najika Server
print("[2/3] Starting Najika Server...")
server_process = subprocess.Popen(
    [sys.executable, "backend/najika_server.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
)

# Wait for server to start
print("Waiting for server to start...")
time.sleep(5)

# Step 3: Start Cloudflare Tunnel
print("[3/3] Starting Cloudflare Tunnel...")
print()
print("="*60)
print("  DEINE MOBILE URL ERSCHEINT GLEICH!")
print("  Kopiere sie und öffne sie auf deinem Handy!")
print("="*60)
print()

try:
    tunnel_process = subprocess.Popen(
        [r"C:\cloudflared.exe", "tunnel", "--url", "http://localhost:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Read output and look for URL
    url_found = False
    for line in tunnel_process.stdout:
        print(line.rstrip())

        # Look for the URL in output
        if "trycloudflare.com" in line and not url_found:
            match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
            if match:
                url = match.group(0)
                print()
                print("="*60)
                print(f"  DEINE MOBILE URL:")
                print(f"  {url}")
                print(f"  {url}/digivice/")
                print("="*60)
                print()
                url_found = True

    tunnel_process.wait()

except KeyboardInterrupt:
    print("\nStopping...")
    tunnel_process.terminate()
    server_process.terminate()
except Exception as e:
    print(f"Error: {e}")
    server_process.terminate()
