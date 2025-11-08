"""
Najika Browser API - PC Remote Browser Control

This extends the Terminal API to provide browser control functionality.
Works with existing najika_tor.py for Tor integration.

Features:
- Start/Stop Firefox with different profiles (tor, vpn, nsfw)
- Navigate, back, forward, refresh
- Screenshot streaming
- Mouse/keyboard input simulation
- Tab management

Requires:
- najika_terminal_api.py (for session management)
- najika_tor.py (for Tor browser)
- Selenium WebDriver
- pyautogui (for mouse/keyboard)
"""

import os
import sys
import time
import base64
import subprocess
from typing import Dict, Optional, Tuple
from datetime import datetime
from io import BytesIO

# Browser control
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Input simulation
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False
    print("⚠️ Warning: pyautogui not installed. Mouse/keyboard input will not work.")

# Import Terminal API for session management
try:
    from najika_terminal_api import TerminalAPI, SHELL_SESSIONS
except ImportError:
    print("❌ Error: najika_terminal_api.py not found!")
    print("Browser API requires Terminal API for session management.")
    sys.exit(1)

# Import Tor integration
try:
    from najika_tor import NajikaTor
    HAS_TOR = True
except ImportError:
    HAS_TOR = False
    print("⚠️ Warning: najika_tor.py not found. Tor mode will not work.")


# ============================================================
# BROWSER SESSION MANAGEMENT
# ============================================================

class BrowserSession:
    """Represents a Firefox browser session"""

    def __init__(self, session_id: str, mode: str = "tor"):
        self.session_id = session_id
        self.mode = mode  # 'tor', 'vpn', 'nsfw'
        self.driver: Optional[webdriver.Firefox] = None
        self.tor_instance: Optional[NajikaTor] = None
        self.firefox_pid: Optional[int] = None
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.is_active = False

        self._start_browser()

    def _start_browser(self):
        """Start Firefox based on mode"""
        try:
            options = FirefoxOptions()

            if self.mode == "tor" and HAS_TOR:
                # Use Tor
                self.tor_instance = NajikaTor()
                # Configure Firefox to use Tor SOCKS proxy
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.socks", "127.0.0.1")
                options.set_preference("network.proxy.socks_port", 9150)
                options.set_preference("network.proxy.socks_remote_dns", True)

            elif self.mode == "nsfw":
                # NSFW profile (if exists)
                # You can customize Firefox profile here
                pass

            # Start Firefox
            self.driver = webdriver.Firefox(options=options)
            self.firefox_pid = self._get_firefox_pid()
            self.is_active = True

            print(f"✅ Browser session {self.session_id} started (mode: {self.mode}, PID: {self.firefox_pid})")

        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            self.is_active = False

    def _get_firefox_pid(self) -> Optional[int]:
        """Get Firefox process ID"""
        try:
            # This is a simplified version, may need adjustment based on OS
            if sys.platform == "linux":
                result = subprocess.run(
                    ["pgrep", "-f", "firefox"],
                    capture_output=True,
                    text=True
                )
                pids = result.stdout.strip().split('\n')
                return int(pids[-1]) if pids and pids[0] else None
            elif sys.platform == "win32":
                # Windows: use tasklist
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq firefox.exe"],
                    capture_output=True,
                    text=True
                )
                # Parse output to get PID
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if "firefox.exe" in line.lower():
                        parts = line.split()
                        if len(parts) >= 2:
                            return int(parts[1])
            return None
        except Exception as e:
            print(f"⚠️ Failed to get Firefox PID: {e}")
            return None

    def navigate(self, url: str) -> bool:
        """Navigate to URL"""
        if not self.is_active or not self.driver:
            return False

        try:
            self.driver.get(url)
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False

    def back(self) -> bool:
        """Go back"""
        if not self.is_active or not self.driver:
            return False

        try:
            self.driver.back()
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Back error: {e}")
            return False

    def forward(self) -> bool:
        """Go forward"""
        if not self.is_active or not self.driver:
            return False

        try:
            self.driver.forward()
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Forward error: {e}")
            return False

    def refresh(self) -> bool:
        """Refresh page"""
        if not self.is_active or not self.driver:
            return False

        try:
            self.driver.refresh()
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Refresh error: {e}")
            return False

    def screenshot(self) -> Optional[bytes]:
        """Get screenshot as PNG bytes"""
        if not self.is_active or not self.driver:
            return None

        try:
            screenshot_base64 = self.driver.get_screenshot_as_base64()
            self.last_activity = datetime.now()
            return base64.b64decode(screenshot_base64)
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None

    def click(self, x: int, y: int) -> bool:
        """Simulate mouse click at coordinates"""
        if not HAS_PYAUTOGUI:
            print("⚠️ pyautogui not available")
            return False

        try:
            # Get browser window position
            # Note: This is simplified, may need adjustment
            pyautogui.click(x, y)
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Click error: {e}")
            return False

    def type_text(self, text: str) -> bool:
        """Type text"""
        if not self.is_active or not self.driver:
            return False

        try:
            # Find active element and type
            active_element = self.driver.switch_to.active_element
            active_element.send_keys(text)
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Type error: {e}")
            return False

    def send_shortcut(self, keys: str) -> bool:
        """Send keyboard shortcut (e.g., 'ctrl+t')"""
        if not self.is_active or not self.driver:
            return False

        try:
            # Parse shortcut
            key_mapping = {
                'ctrl': Keys.CONTROL,
                'shift': Keys.SHIFT,
                'alt': Keys.ALT,
                'enter': Keys.ENTER,
                'tab': Keys.TAB,
                't': 't',
                'w': 'w',
                # Add more as needed
            }

            parts = keys.lower().split('+')
            active_element = self.driver.switch_to.active_element

            # Build key combination
            if len(parts) == 2:
                modifier = key_mapping.get(parts[0])
                key = key_mapping.get(parts[1], parts[1])
                active_element.send_keys(modifier, key)
            else:
                key = key_mapping.get(parts[0], parts[0])
                active_element.send_keys(key)

            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Shortcut error: {e}")
            return False

    def scroll(self, delta_y: int) -> bool:
        """Scroll page"""
        if not self.is_active or not self.driver:
            return False

        try:
            self.driver.execute_script(f"window.scrollBy(0, {delta_y});")
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            print(f"❌ Scroll error: {e}")
            return False

    def close(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver.quit()
            if self.tor_instance:
                # Stop Tor if we started it
                pass
            self.is_active = False
            print(f"✅ Browser session {self.session_id} closed")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")


# Global browser sessions
BROWSER_SESSIONS: Dict[str, BrowserSession] = {}


# ============================================================
# BROWSER API
# ============================================================

class BrowserAPI:
    """API for browser control"""

    @staticmethod
    def start_browser(session_id: str, mode: str = "tor") -> Dict:
        """
        Start Firefox browser

        Args:
            session_id: Terminal session ID (for auth)
            mode: Browser mode ('tor', 'vpn', 'nsfw')

        Returns:
            {
                'success': bool,
                'firefox_pid': int,
                'mode': str,
                'error': str (if failed)
            }
        """
        # Verify terminal session exists (for auth)
        if session_id not in SHELL_SESSIONS:
            return {'success': False, 'error': 'Invalid session'}

        # Check if browser already running
        if session_id in BROWSER_SESSIONS:
            browser = BROWSER_SESSIONS[session_id]
            if browser.is_active:
                return {
                    'success': True,
                    'firefox_pid': browser.firefox_pid,
                    'mode': browser.mode,
                    'message': 'Browser already running'
                }

        # Start new browser session
        browser = BrowserSession(session_id, mode)

        if browser.is_active:
            BROWSER_SESSIONS[session_id] = browser
            return {
                'success': True,
                'firefox_pid': browser.firefox_pid,
                'mode': browser.mode,
            }
        else:
            return {
                'success': False,
                'error': 'Failed to start browser'
            }

    @staticmethod
    def stop_browser(session_id: str) -> Dict:
        """Stop browser"""
        if session_id not in BROWSER_SESSIONS:
            return {'success': False, 'error': 'No browser session'}

        browser = BROWSER_SESSIONS[session_id]
        browser.close()
        del BROWSER_SESSIONS[session_id]

        return {'success': True}

    @staticmethod
    def navigate(session_id: str, url: str) -> Dict:
        """Navigate to URL"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.navigate(url)
        return {'success': success}

    @staticmethod
    def back(session_id: str) -> Dict:
        """Go back"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.back()
        return {'success': success}

    @staticmethod
    def forward(session_id: str) -> Dict:
        """Go forward"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.forward()
        return {'success': success}

    @staticmethod
    def refresh(session_id: str) -> Dict:
        """Refresh page"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.refresh()
        return {'success': success}

    @staticmethod
    def screenshot(session_id: str) -> Dict:
        """Get screenshot"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        screenshot_bytes = browser.screenshot()
        if screenshot_bytes:
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            return {
                'success': True,
                'screenshot': screenshot_base64
            }
        else:
            return {'success': False, 'error': 'Screenshot failed'}

    @staticmethod
    def click(session_id: str, x: int, y: int) -> Dict:
        """Simulate click"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.click(x, y)
        return {'success': success}

    @staticmethod
    def type_text(session_id: str, text: str) -> Dict:
        """Type text"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.type_text(text)
        return {'success': success}

    @staticmethod
    def send_shortcut(session_id: str, keys: str) -> Dict:
        """Send keyboard shortcut"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.send_shortcut(keys)
        return {'success': success}

    @staticmethod
    def scroll(session_id: str, delta_y: int) -> Dict:
        """Scroll page"""
        browser = BROWSER_SESSIONS.get(session_id)
        if not browser:
            return {'success': False, 'error': 'No browser session'}

        success = browser.scroll(delta_y)
        return {'success': success}


# ============================================================
# HTTP ENDPOINTS (for integration with najika_server.py)
# ============================================================

"""
Add these endpoints to your najika_server.py:

# Browser endpoints
if self.path == "/api/browser/start":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    mode = data.get('mode', 'tor')
    result = BrowserAPI.start_browser(session_id, mode)
    self._send_json(result)

elif self.path == "/api/browser/stop":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    result = BrowserAPI.stop_browser(session_id)
    self._send_json(result)

elif self.path == "/api/browser/navigate":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    url = data.get('url')
    result = BrowserAPI.navigate(session_id, url)
    self._send_json(result)

elif self.path == "/api/browser/back":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    result = BrowserAPI.back(session_id)
    self._send_json(result)

elif self.path == "/api/browser/forward":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    result = BrowserAPI.forward(session_id)
    self._send_json(result)

elif self.path == "/api/browser/refresh":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    result = BrowserAPI.refresh(session_id)
    self._send_json(result)

elif self.path.startswith("/api/browser/screenshot"):
    # GET endpoint
    query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
    session_id = query.get('session_id', [None])[0]
    result = BrowserAPI.screenshot(session_id)
    self._send_json(result)

elif self.path == "/api/browser/click":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    x = data.get('x')
    y = data.get('y')
    result = BrowserAPI.click(session_id, x, y)
    self._send_json(result)

elif self.path == "/api/browser/type":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    text = data.get('text')
    result = BrowserAPI.type_text(session_id, text)
    self._send_json(result)

elif self.path == "/api/browser/shortcut":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    keys = data.get('keys')
    result = BrowserAPI.send_shortcut(session_id, keys)
    self._send_json(result)

elif self.path == "/api/browser/scroll":
    data = json.loads(self.rfile.read(content_length).decode('utf-8'))
    session_id = data.get('session_id')
    delta_y = data.get('delta_y')
    result = BrowserAPI.scroll(session_id, delta_y)
    self._send_json(result)
"""


if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA BROWSER API")
    print("=" * 60)
    print("This module provides browser control functionality.")
    print("It should be imported by najika_server.py")
    print("=" * 60)
