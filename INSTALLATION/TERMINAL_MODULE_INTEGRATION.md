# 🖥️ NAJIKA TERMINAL MODULE - Integration Guide

**Version:** 1.0
**Date:** 2025-11-07
**Status:** ✅ Ready for Integration

---

## 📋 Overview

Das Terminal Modul ermöglicht **vollständige PC-Kontrolle** vom Najika Digivice aus jedem Netzwerk.

### Features:
- ✅ Persistent Shell Sessions (bash/PowerShell/cmd)
- ✅ Beliebige Befehle ausführen
- ✅ Prozess-Management
- ✅ Command History & Auto-Complete
- ✅ Passwort-Authentifizierung
- ✅ Verschlüsselte Befehls-Übertragung
- ✅ GitHub-style Terminal UI

---

## 📂 Files Created

```
INSTALLATION/
├── backend/
│   └── najika_terminal_api.py          # Backend API (361 Zeilen)
│
└── flutter_app/najika_digivice/lib/modules/terminal/
    ├── terminal_screen.dart            # Terminal UI (488 Zeilen)
    └── terminal_service.dart           # Service Layer (288 Zeilen)
```

---

## 🚀 Backend Integration

### Step 1: Import Terminal API

**In `/home/user/Najika_World/backend/najika_server.py`:**

```python
# Add at top with other imports
from najika_terminal_api import TerminalAPI, handle_terminal_api

# Initialize Terminal API (after load_dotenv())
TERMINAL_PASSWORD = os.getenv("TERMINAL_PASSWORD", "change-me-in-production")
TerminalAPI.initialize(TERMINAL_PASSWORD)
print(f"✅ Terminal API initialized")
```

### Step 2: Add API Endpoints

**In `najika_server.py` → `do_POST()` method:**

```python
# Add after existing /api/ endpoints (around line 1870)

# ===== TERMINAL API ENDPOINTS =====
if self.path.startswith("/api/terminal/"):
    try:
        body_str = body.decode("utf-8")
    except UnicodeDecodeError:
        body_str = body.decode("latin-1")

    data = json.loads(body_str)

    # Get auth token from headers or generate
    auth_token = self.headers.get('Authorization', f'token_{time.time()}')

    # Handle request
    result = handle_terminal_api(self.path, data, auth_token)

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(result).encode())
    return
```

### Step 3: Add Authentication Endpoint

**In `najika_server.py` → `do_POST()` method:**

```python
if self.path == "/api/terminal/authenticate":
    try:
        body_str = body.decode("utf-8")
    except UnicodeDecodeError:
        body_str = body.decode("latin-1")

    data = json.loads(body_str)
    password = data.get('password', '')

    if TerminalAPI.authenticate(password):
        # Generate auth token
        import hashlib
        auth_token = hashlib.sha256(f"{password}{time.time()}".encode()).hexdigest()

        result = {
            'success': True,
            'auth_token': auth_token
        }
    else:
        result = {
            'success': False,
            'error': 'Invalid password'
        }

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(result).encode())
    return
```

### Step 4: Copy Terminal API File

```bash
cp INSTALLATION/backend/najika_terminal_api.py /home/user/Najika_World/backend/
```

### Step 5: Set Terminal Password

**In `.env` or environment:**

```bash
TERMINAL_PASSWORD=your-secure-password-here
```

---

## 📱 Flutter App Integration

### Step 1: Copy Terminal Module

```bash
cp -r INSTALLATION/flutter_app/najika_digivice/lib/modules/terminal \
      /path/to/active/najika_digivice/lib/modules/
```

### Step 2: Add TerminalService to Providers

**In `main.dart`:**

```dart
import 'modules/terminal/terminal_service.dart';

// In MultiProvider:
MultiProvider(
  providers: [
    // ... existing providers ...
    ChangeNotifierProvider(create: (_) => TerminalService.instance),
  ],
  // ...
)
```

### Step 3: Add Navigation to Terminal

**Option A: From gesicherter Bereich (Die Mühle)**

In your Mühle/Secure Area screen:

```dart
ListTile(
  leading: Icon(Icons.terminal),
  title: Text('Terminal'),
  subtitle: Text('Full PC Control'),
  onTap: () {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => TerminalScreen(),
      ),
    );
  },
)
```

**Option B: From Settings**

Add to your settings screen as a secure module.

### Step 4: Update Server URL

**In `lib/core/constants/app_constants.dart`:**

Make sure `serverUrl` points to your backend:

```dart
static const String serverUrl = 'http://192.168.1.100:8000'; // Local
// OR
static const String serverUrl = 'https://najika.yourdomain.com'; // Remote
```

---

## 🔒 Security Configuration

### Terminal Password

Set a **strong** password in backend:

```bash
# In .env
TERMINAL_PASSWORD=My$ecure!Password123
```

### Network Security

**Always use with:**
- ✅ ExpressVPN active
- ✅ Cloudflare Tunnel or Tailscale
- ✅ TLS encryption

### Command Restrictions (Optional)

Edit `najika_terminal_api.py` to restrict commands:

```python
# Add command whitelist/blacklist
BLOCKED_COMMANDS = ['rm -rf /', 'format', 'del /f']

def execute_command(command, ...):
    # Check against blocked commands
    if any(blocked in command for blocked in BLOCKED_COMMANDS):
        return {'success': False, 'error': 'Command blocked'}
    # ... rest of code
```

---

## 🎨 UI Customization

### Terminal Colors

In `terminal_screen.dart`:

```dart
// GitHub Dark Theme (current)
backgroundColor: Color(0xFF0D1117),
promptColor: Color(0xFF58A6FF),
outputColor: Color(0xFFC9D1D9),
errorColor: Color(0xFFF85149),

// Or customize:
backgroundColor: Colors.black,
promptColor: Colors.greenAccent,
// etc.
```

### Terminal Font

```dart
TextStyle(
  fontFamily: 'Courier', // or 'Roboto Mono', 'Fira Code'
  fontSize: 14,
)
```

---

## 🧪 Testing

### Test Backend

```bash
cd /home/user/Najika_World/backend
python najika_terminal_api.py
```

Expected output:
```
🧪 Testing Terminal API...
✅ Shell session abc123 started
Created session: abc123
Output: Hello from Terminal!
Active sessions: 1
✅ Shell session abc123 closed
✅ Test completed!
```

### Test Flutter App

1. Run app: `flutter run`
2. Navigate to Terminal module
3. Enter terminal password
4. Try commands:
   ```
   pwd
   ls -la
   echo "Hello from Digivice!"
   python --version
   ```

---

## 📊 API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/terminal/authenticate` | POST | Authenticate with password |
| `/api/terminal/session/create` | POST | Create new shell session |
| `/api/terminal/session/close` | POST | Close shell session |
| `/api/terminal/session/list` | POST | List active sessions |
| `/api/terminal/execute` | POST | Execute command |
| `/api/terminal/processes` | POST | List running processes |
| `/api/terminal/kill` | POST | Kill process by PID |

### Example Request

```json
POST /api/terminal/execute
{
  "password": "your-password",
  "session_id": "abc123",
  "command": "ls -la",
  "timeout": 30
}
```

### Example Response

```json
{
  "success": true,
  "stdout": "total 24\ndrwxr-xr-x  5 user  staff  160 Nov  7 10:00 .\n...",
  "stderr": "",
  "returncode": 0
}
```

---

## 🔧 Troubleshooting

### Backend Issues

**"Authentication failed"**
- Check TERMINAL_PASSWORD in .env
- Verify password in app matches

**"Session not found"**
- Session might have timed out (30min)
- Create new session

**"Command timeout"**
- Increase timeout in request
- Check if command hangs

### Flutter Issues

**"Not authenticated"**
- Re-enter password
- Check server URL in app_constants.dart

**"HTTP error"**
- Verify backend is running
- Check firewall rules
- Test with `curl http://your-server:8000/health`

**"No response"**
- Check network connection
- Verify VPN/Tunnel is active
- Test with browser: http://your-server:8000/api/status

---

## 🎯 Usage Examples

### Basic Commands

```bash
# Navigation
cd /path/to/directory
pwd
ls -la

# File Operations
cat file.txt
nano file.txt
mv old.txt new.txt

# System Info
whoami
hostname
uname -a
df -h

# Process Management
ps aux
top
kill -9 <PID>

# Python
python --version
python script.py

# Git
git status
git pull
git log --oneline
```

### Advanced Usage

**Start long-running process:**
```bash
python long_script.py &
```

**Monitor logs:**
```bash
tail -f /var/log/najika.log
```

**System monitoring:**
```bash
htop
```

---

## 📝 Feature Roadmap

### Phase 1 (Current):
- ✅ Basic shell execution
- ✅ Session management
- ✅ Command history
- ✅ Process management

### Phase 2 (Future):
- ⬜ File upload/download
- ⬜ Syntax highlighting
- ⬜ Tab completion
- ⬜ Multi-session support

### Phase 3 (Advanced):
- ⬜ Terminal multiplexer (tmux-style)
- ⬜ Screen sharing
- ⬜ Collaborative terminal
- ⬜ AI command suggestions (Najika)

---

## ⚠️ Important Notes

1. **Security First:**
   - NEVER expose terminal without password
   - ALWAYS use VPN/Tunnel
   - NEVER run untrusted commands

2. **Resource Management:**
   - Sessions auto-close after 30min inactivity
   - Long commands use timeout
   - Monitor CPU/memory usage

3. **Backup Important Data:**
   - Terminal has full PC access
   - One wrong command can delete files
   - Always backup before testing

4. **Production Deployment:**
   - Change default password
   - Enable audit logging
   - Restrict command whitelist
   - Use certificate pinning

---

## 🐛 Known Limitations

- Interactive commands (like `vim`, `nano`) may not work perfectly
- Large outputs (>1MB) might be slow
- Real-time streaming not yet implemented
- Windows PowerShell support is basic

---

## 📚 Additional Resources

- **Flutter Terminal Package:** https://pub.dev/packages/xterm
- **SSH for Flutter:** https://pub.dev/packages/dartssh2
- **WebSocket Upgrade:** For real-time streaming

---

## ✅ Integration Checklist

Backend:
- [ ] Copy `najika_terminal_api.py` to backend/
- [ ] Import in `najika_server.py`
- [ ] Add API endpoints
- [ ] Set TERMINAL_PASSWORD
- [ ] Test with Python script

Flutter:
- [ ] Copy terminal module to lib/modules/
- [ ] Add TerminalService to providers
- [ ] Add navigation to Terminal
- [ ] Update server URL
- [ ] Test on device

Security:
- [ ] Set strong password
- [ ] Enable VPN
- [ ] Test authentication
- [ ] Review command restrictions

---

**✓ Integration Complete!** 🚀

You now have full PC control from your Najika Digivice! 🎉

---

**Author:** Claude Code
**Project:** Najika World - Digivice Terminal Module
**Contact:** For issues or questions, check the main project documentation
