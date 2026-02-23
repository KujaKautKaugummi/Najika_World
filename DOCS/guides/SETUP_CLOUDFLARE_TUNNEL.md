# 🌐 Cloudflare Tunnel Setup Guide

**Purpose:** Expose local backend (localhost:8000) to internet for Digivice APK remote access

**Cost:** ✅ FREE (Cloudflare Tunnel is free)

---

## 📋 Prerequisites

- ✅ Backend running on Windows (najika_server.py)
- ✅ Internet connection
- ✅ Email for Cloudflare account

---

## Step 1: Create Cloudflare Account

1. Go to: https://dash.cloudflare.com/sign-up
2. Enter email & password
3. Verify email
4. Login to Dashboard

---

## Step 2: Install Cloudflared

### Windows Installation:

**Option A: Download Binary (Already have cloudflared.exe!)**

✅ You already have: `C:\cloudflared.exe`

**Option B: Fresh Download (if needed)**

1. Go to: https://github.com/cloudflare/cloudflared/releases
2. Download: `cloudflared-windows-amd64.exe`
3. Rename to: `cloudflared.exe`
4. Place in: `C:\cloudflared.exe`

**Verify Installation:**
```powershell
C:\cloudflared.exe --version
# Should output: cloudflared version X.X.X
```

---

## Step 3: Login to Cloudflare

```powershell
C:\cloudflared.exe tunnel login
```

**What happens:**
1. Browser opens with Cloudflare login
2. Select domain (or "I don't have a domain yet")
3. Authorize cloudflared
4. Certificate saved to: `C:\Users\<You>\.cloudflared\cert.pem`

**Success message:**
```
You have successfully logged in.
```

---

## Step 4: Create Tunnel

```powershell
C:\cloudflared.exe tunnel create najika-backend
```

**Output:**
```
Tunnel credentials written to C:\Users\<You>\.cloudflared\<TUNNEL_ID>.json
Created tunnel najika-backend with id <TUNNEL_ID>
```

**Save the Tunnel ID!** (You'll need it)

---

## Step 5: Configure Tunnel

### Create Config File

**Location:** `C:\Users\<You>\.cloudflared\config.yml`

**Content:**
```yaml
tunnel: <TUNNEL_ID>
credentials-file: C:\Users\<You>\.cloudflared\<TUNNEL_ID>.json

ingress:
  # Route for Backend API
  - hostname: najika-backend.yourusername.workers.dev
    service: http://localhost:8000

  # Route for WebSocket (Voice Chat)
  - hostname: najika-ws.yourusername.workers.dev
    service: ws://localhost:8000

  # Catch-all rule (required)
  - service: http_status:404
```

**Replace:**
- `<TUNNEL_ID>` with your tunnel ID
- `yourusername` with your Cloudflare username/subdomain

---

## Step 6: Route DNS (Optional - Custom Domain)

### If you have a domain (e.g., najika.com):

```powershell
C:\cloudflared.exe tunnel route dns najika-backend api.najika.com
C:\cloudflared.exe tunnel route dns najika-backend ws.najika.com
```

### If NO domain (use workers.dev subdomain):

Cloudflare automatically provides:
- `<tunnel-name>.<username>.workers.dev`
- Free subdomain, no DNS config needed

---

## Step 7: Run Tunnel

### Test Run (Foreground):
```powershell
C:\cloudflared.exe tunnel run najika-backend
```

**Output:**
```
INF Starting tunnel tunnelID=<ID>
INF Connection registered connIndex=0
INF +----------------------------------------------------------+
INF | Your tunnel is now active!                               |
INF | https://najika-backend.yourusername.workers.dev          |
INF +----------------------------------------------------------+
```

**Test:**
Open browser: `https://najika-backend.yourusername.workers.dev`

Should see backend response (or 404 if backend not running)

---

## Step 8: Run Backend + Tunnel Together

### Option A: Separate Windows (Manual)

**Terminal 1:**
```powershell
cd C:\Najika_World\backend
python najika_server.py
```

**Terminal 2:**
```powershell
C:\cloudflared.exe tunnel run najika-backend
```

### Option B: Batch Script (Automated)

**Create:** `C:\Najika_World\START_BACKEND_WITH_TUNNEL.bat`

```batch
@echo off
echo Starting Najika Backend + Cloudflare Tunnel
echo ==========================================

:: Start Backend in background
start "Najika Backend" cmd /c "cd C:\Najika_World\backend && python najika_server.py"

:: Wait 5 seconds for backend to start
timeout /t 5 /nobreak

:: Start Cloudflare Tunnel
echo Starting Cloudflare Tunnel...
C:\cloudflared.exe tunnel run najika-backend

pause
```

**Run:**
```powershell
C:\Najika_World\START_BACKEND_WITH_TUNNEL.bat
```

---

## Step 9: Install as Windows Service (24/7 Auto-Start)

### Make Tunnel Run on Boot:

```powershell
C:\cloudflared.exe service install
```

**This will:**
- Install cloudflared as Windows Service
- Auto-start on Windows boot
- Run in background (no console window)

**Manage Service:**
```powershell
# Start service
net start cloudflared

# Stop service
net stop cloudflared

# Check status
sc query cloudflared
```

### Auto-Start Backend on Boot (Optional):

**Create:** `C:\Najika_World\backend\START_BACKEND_SERVICE.bat`

```batch
@echo off
cd C:\Najika_World\backend
python najika_server.py
```

**Add to Windows Startup:**
1. Press `Win + R`
2. Type: `shell:startup`
3. Create shortcut to `START_BACKEND_SERVICE.bat`

Or use **Task Scheduler:**
1. Open: Task Scheduler
2. Create Task: "Najika Backend"
3. Trigger: At startup
4. Action: Run `python C:\Najika_World\backend\najika_server.py`

---

## Step 10: Configure Digivice APK

### Update Backend URL in UE5 Project

**In:** `C:\NajikaDigivice_UE5\NajikaDigivice\Config\DefaultGame.ini`

Add:
```ini
[/Script/NajikaDigivice.NajikaGameSettings]
BackendBaseURL=https://najika-backend.yourusername.workers.dev
WebSocketURL=wss://najika-backend.yourusername.workers.dev
```

**Or in C++ code:**

```cpp
// In NajikaHttpClient.cpp or Config
const FString BackendBaseURL = TEXT("https://najika-backend.yourusername.workers.dev");
const FString WebSocketURL = TEXT("wss://najika-backend.yourusername.workers.dev");
```

**Replace:** `yourusername` with your actual Cloudflare subdomain

---

## Step 11: Test End-to-End

### Test from Phone (Different Network):

1. **Disable WiFi on phone** (use Mobile Data)
2. **Open Browser on phone**
3. **Navigate to:** `https://najika-backend.yourusername.workers.dev`
4. **Should see:** Backend response (or API welcome message)

### Test with Digivice APK:

1. Install APK on phone
2. Launch app
3. App should connect to remote backend
4. Check logs: "Connected to backend"

---

## 🔧 Troubleshooting

### Issue: Tunnel won't start
**Error:** `tunnel credentials not found`

**Solution:**
```powershell
# Re-login
C:\cloudflared.exe tunnel login

# Recreate tunnel
C:\cloudflared.exe tunnel create najika-backend
```

---

### Issue: 502 Bad Gateway
**Cause:** Backend not running or wrong port

**Check:**
1. Backend running? `netstat -an | findstr 8000`
2. Config.yml has correct port? (`http://localhost:8000`)
3. Restart tunnel

---

### Issue: Connection Refused on Phone
**Cause:** DNS not updated or tunnel not running

**Check:**
1. Tunnel running? Check cloudflared process
2. Try workers.dev URL directly (no custom domain)
3. Check firewall (shouldn't block outgoing connections)

---

### Issue: WebSocket not working
**Cause:** Config missing WebSocket route

**Solution:**
Add to `config.yml`:
```yaml
ingress:
  - hostname: najika-ws.yourusername.workers.dev
    service: ws://localhost:8000
```

Then restart tunnel.

---

## 📊 Monitoring & Logs

### View Tunnel Logs:
```powershell
C:\cloudflared.exe tunnel info najika-backend
```

### View Live Connections:
Cloudflare Dashboard → Traffic → Analytics

### Check Tunnel Status:
```powershell
C:\cloudflared.exe tunnel list
```

---

## 🔒 Security Best Practices

### 1. Enable Access Policies (Optional)
Restrict who can access your tunnel:

1. Cloudflare Dashboard → Zero Trust
2. Access → Applications
3. Add Application: `najika-backend.workers.dev`
4. Policy: Allow only your IP or email

### 2. Rate Limiting
Protect from abuse:

1. Dashboard → Security → WAF
2. Add Rate Limiting Rule
3. Limit: 100 requests/minute per IP

### 3. HTTPS Only
Cloudflare automatically provides HTTPS ✅
- Certificate auto-renewed
- TLS 1.3 encryption

---

## 💰 Costs

**Cloudflare Tunnel:** ✅ FREE
**Bandwidth:** ✅ Unlimited (Free)
**Custom Domain:** ✅ FREE (if you own domain)
**workers.dev Subdomain:** ✅ FREE

**Total Cost:** **$0/month** 🎉

---

## 🎯 Summary

After setup, you have:
- ✅ Backend accessible from anywhere
- ✅ HTTPS encryption
- ✅ No port forwarding needed
- ✅ No router configuration
- ✅ Works behind firewall/NAT
- ✅ Free forever

**Your URLs:**
- HTTP API: `https://najika-backend.yourusername.workers.dev`
- WebSocket: `wss://najika-backend.yourusername.workers.dev`

**Use these URLs in Digivice APK!**

---

## 📝 Next Steps

1. ✅ Complete this setup
2. ✅ Test from phone browser
3. ✅ Update APK backend URL
4. ✅ Rebuild & test APK
5. ✅ Setup auto-start (optional)

**Questions?** Check Cloudflare Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps

**Done!** 🚀
