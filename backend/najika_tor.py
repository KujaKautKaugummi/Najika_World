"""
NAJIKA TOR BROWSER INTEGRATION
Tor Browser Control für Darknet-Zugriff
"""

import subprocess
import time
import os
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NajikaTor:
    def __init__(self, tor_browser_path=None):
        """
        Initialisiert Tor Browser Control

        Args:
            tor_browser_path: Pfad zu Tor Browser (optional, auto-detect auf Windows)
        """
        self.tor_browser_path = tor_browser_path or self._find_tor_browser()
        self.tor_process = None
        self.driver = None
        self.is_running = False

        print("[NAJIKA TOR] >> Tor Browser Integration bereit")
        if self.tor_browser_path:
            print(f"[NAJIKA TOR] >> Tor Browser Pfad: {self.tor_browser_path}")
        else:
            print("[NAJIKA TOR] WARNING Tor Browser nicht gefunden!")

    def _find_tor_browser(self):
        """Findet Tor Browser Installation (Windows)"""
        possible_paths = [
            r"C:\Users\%USERNAME%\Desktop\Tor Browser\Browser\firefox.exe",
            r"C:\Program Files\Tor Browser\Browser\firefox.exe",
            r"C:\Program Files (x86)\Tor Browser\Browser\firefox.exe",
            r"D:\Tor Browser\Browser\firefox.exe"
        ]

        username = os.getenv("USERNAME", "User")
        for path in possible_paths:
            expanded = path.replace("%USERNAME%", username)
            if os.path.exists(expanded):
                return expanded

        return None

    def is_onion_url(self, url):
        """Prüft ob URL eine .onion Adresse ist"""
        return url.endswith(".onion") or ".onion/" in url

    def needs_tor(self, query):
        """
        Erkennt ob eine Suche Tor benötigt

        Triggers:
        - "darknet", "dark web", "onion"
        - ".onion" URLs
        - "tor search"
        """
        query_lower = query.lower()

        triggers = [
            r"\bdarknet\b",
            r"\bdark web\b",
            r"\bonion\b",
            r"\.onion",
            r"\btor\b.*\bsuche\b",
            r"\btor\b.*\bsearch\b",
            r"\bhidden service\b"
        ]

        for trigger in triggers:
            if re.search(trigger, query_lower):
                print(f"[TOR] >> Tor-Trigger erkannt: {trigger}")
                return True

        return False

    def start_tor_browser(self):
        """Startet Tor Browser (ohne Selenium, nur Prozess)"""
        if not self.tor_browser_path:
            return {"ok": False, "msg": "Tor Browser nicht installiert!"}

        if self.is_running:
            return {"ok": True, "msg": "Tor Browser läuft bereits"}

        try:
            # Starte Tor Browser als Hintergrund-Prozess
            self.tor_process = subprocess.Popen(
                [self.tor_browser_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            self.is_running = True
            print("[TOR] OK Tor Browser gestartet")
            return {"ok": True, "msg": "Tor Browser gestartet! Warte auf Verbindung..."}

        except Exception as e:
            print(f"[TOR] ERROR Start-Fehler: {e}")
            return {"ok": False, "msg": f"Fehler: {e}"}

    def stop_tor_browser(self):
        """Stoppt Tor Browser"""
        if self.tor_process:
            try:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=5)
                print("[TOR] >> Tor Browser gestoppt")
            except:
                self.tor_process.kill()

        self.is_running = False
        self.tor_process = None

    def search_duckduckgo_onion(self, query, max_results=5):
        """
        Sucht über DuckDuckGo Onion Service

        DuckDuckGo Onion: https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion
        """
        try:
            # Verwende SOCKS Proxy für Tor (localhost:9150 für Tor Browser)
            import socks
            import socket
            from urllib.request import urlopen, Request
            from urllib.parse import quote

            # Backup original socket
            original_socket = socket.socket

            # Set SOCKS proxy
            socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
            socket.socket = socks.socksocket

            # DuckDuckGo Onion Service
            onion_url = f"https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/html/?q={quote(query)}"

            req = Request(onion_url, headers={"User-Agent": "Mozilla/5.0"})

            print(f"[TOR] >> Suche über DuckDuckGo Onion: {query}")

            with urlopen(req, timeout=30) as response:
                html = response.read().decode("utf-8")

            # Restore original socket
            socket.socket = original_socket

            # Parse Ergebnisse (einfaches Parsing)
            results = self._parse_ddg_results(html, max_results)

            print(f"[TOR] OK {len(results)} Ergebnisse gefunden")
            return results

        except Exception as e:
            print(f"[TOR] WARNING Onion Search Fehler: {e}")
            # Restore socket on error
            try:
                socket.socket = original_socket
            except:
                pass
            return []

    def _parse_ddg_results(self, html, max_results):
        """
        Parst DuckDuckGo HTML-Ergebnisse (simpel)
        """
        results = []

        # Einfaches Regex-basiertes Parsing (nicht perfekt aber funktional)
        # Match: <a class="result__a" href="URL">Title</a>
        import re

        pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)

        for url, title in matches[:max_results]:
            # Snippet extrahieren (nächster Text nach Title)
            snippet = ""  # Könnte verbessert werden

            results.append({
                "title": title.strip(),
                "url": url,
                "snippet": snippet
            })

        return results

    def format_tor_results(self, results, query):
        """Formatiert Tor-Ergebnisse für Najika"""
        if not results:
            return f"Keine Tor-Ergebnisse für '{query}' gefunden."

        formatted = [f"# TOR SEARCH RESULTS (via DuckDuckGo Onion) für: '{query}'\n"]
        formatted.append("[DARKNET MODE AKTIV - .onion Links]\n")

        for i, result in enumerate(results, 1):
            title = result.get("title", "N/A")
            url = result.get("url", "N/A")
            snippet = result.get("snippet", "")

            formatted.append(f"{i}. **{title}**")
            if snippet:
                formatted.append(f"   {snippet}")
            formatted.append(f"   Onion URL: {url}\n")

        formatted.append("\n---")
        formatted.append("**WARNUNG:** Diese Ergebnisse stammen aus dem Darknet. Vorsicht bei unbekannten Links!")
        formatted.append("**ANWEISUNG:** Nutze diese Informationen, um Kujas Frage zu beantworten. Bleib in deiner Najika-Persönlichkeit!")

        return "\n".join(formatted)

    def check_tor_connection(self):
        """Prüft ob Tor-Verbindung aktiv ist"""
        try:
            import socks
            import socket
            from urllib.request import urlopen, Request

            # Backup
            original_socket = socket.socket

            # SOCKS Proxy
            socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
            socket.socket = socks.socksocket

            # Test: check.torproject.org
            req = Request("https://check.torproject.org/api/ip", headers={"User-Agent": "Mozilla/5.0"})

            with urlopen(req, timeout=10) as response:
                data = response.read().decode("utf-8")

            # Restore
            socket.socket = original_socket

            import json
            result = json.loads(data)

            if result.get("IsTor"):
                print(f"[TOR] OK Verbindung aktiv! IP: {result.get('IP')}")
                return {"ok": True, "ip": result.get("IP"), "is_tor": True}
            else:
                print(f"[TOR] WARNING Keine Tor-Verbindung! IP: {result.get('IP')}")
                return {"ok": False, "ip": result.get("IP"), "is_tor": False}

        except Exception as e:
            print(f"[TOR] WARNING Connection Check Fehler: {e}")
            try:
                socket.socket = original_socket
            except:
                pass
            return {"ok": False, "error": str(e)}

    def __del__(self):
        """Cleanup beim Beenden"""
        self.stop_tor_browser()


# Test-Funktion
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA TOR INTEGRATION TEST")
    print("=" * 60)

    tor = NajikaTor()

    # Test 1: Tor Erkennung
    print("\n" + "=" * 60)
    print("TEST 1: Tor Trigger Detection")
    print("=" * 60)

    test_queries = [
        "Was ist das Darknet?",
        "Suche normale Website",
        "Tor Suche nach xyz",
        "http://example.onion"
    ]

    for query in test_queries:
        needs = tor.needs_tor(query)
        print(f"'{query}' -> Tor benötigt: {needs}")

    # Test 2: Tor Browser Path
    print("\n" + "=" * 60)
    print("TEST 2: Tor Browser Detection")
    print("=" * 60)
    print(f"Tor Browser gefunden: {tor.tor_browser_path is not None}")
    if tor.tor_browser_path:
        print(f"Pfad: {tor.tor_browser_path}")

    print("\n" + "=" * 60)
    print("OK NAJIKA TOR TEST ABGESCHLOSSEN")
    print("=" * 60)
