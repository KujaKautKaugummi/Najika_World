"""
TOR Browser Service - Najika World
===================================

Service für TOR Browser Integration (nur Browser/Terminal Modul)

WICHTIG: Dieses Feature ist NUR für das Browser/Terminal Modul verfügbar,
         NICHT für die REST API!

Features:
- Anonymes Browsing im Spiel
- Darknet Zugang (In-Game)
- Hidden Services (NPC Märkte, Quest Informationen)

Technische Umsetzung:
- Lokaler TOR Client (nur wenn Browser-Modul aktiv)
- Keine API Endpoints (nur Standalone Service)
- Separater Process für TOR Daemon

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

import subprocess
import os
from typing import Optional, Dict, Any


class TORBrowserService:
    """
    TOR Browser Service für anonymes In-Game Browsing

    WICHTIG: Nur für Browser/Terminal Modul, NICHT für REST API!
    """

    def __init__(self):
        self.tor_process: Optional[subprocess.Popen] = None
        self.socks_port = 9050
        self.control_port = 9051
        self.is_running = False

    def start_tor(self) -> Dict[str, Any]:
        """
        Start TOR daemon (nur für Browser Modul)

        Returns:
            Status dict
        """
        if self.is_running:
            return {
                "success": False,
                "message": "TOR daemon bereits aktiv"
            }

        try:
            # Prüfe ob TOR installiert ist
            tor_path = self._find_tor_executable()

            if not tor_path:
                return {
                    "success": False,
                    "message": "TOR nicht installiert. Bitte installiere TOR Browser Bundle."
                }

            # Start TOR daemon (Hintergrund)
            self.tor_process = subprocess.Popen(
                [tor_path, "--SOCKSPort", str(self.socks_port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.is_running = True

            return {
                "success": True,
                "message": "TOR daemon gestartet",
                "socks_port": self.socks_port,
                "control_port": self.control_port
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Fehler beim Starten: {str(e)}"
            }

    def stop_tor(self) -> Dict[str, Any]:
        """Stop TOR daemon"""
        if not self.is_running or not self.tor_process:
            return {
                "success": False,
                "message": "TOR daemon nicht aktiv"
            }

        try:
            self.tor_process.terminate()
            self.tor_process.wait(timeout=5)
            self.is_running = False

            return {
                "success": True,
                "message": "TOR daemon gestoppt"
            }

        except subprocess.TimeoutExpired:
            self.tor_process.kill()
            self.is_running = False

            return {
                "success": True,
                "message": "TOR daemon zwangsbeendet"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Fehler beim Stoppen: {str(e)}"
            }

    def get_status(self) -> Dict[str, Any]:
        """Get TOR daemon status"""
        return {
            "is_running": self.is_running,
            "socks_port": self.socks_port if self.is_running else None,
            "control_port": self.control_port if self.is_running else None,
            "message": "TOR daemon aktiv" if self.is_running else "TOR daemon inaktiv"
        }

    def _find_tor_executable(self) -> Optional[str]:
        """Find TOR executable on system"""
        # Common TOR paths
        possible_paths = [
            "/usr/bin/tor",
            "/usr/local/bin/tor",
            "tor",  # PATH lookup
        ]

        for path in possible_paths:
            if os.path.exists(path) or path == "tor":
                return path

        return None


# Global instance (nur für Browser Modul!)
_tor_service: Optional[TORBrowserService] = None


def get_tor_service() -> TORBrowserService:
    """Get global TOR service instance"""
    global _tor_service

    if _tor_service is None:
        _tor_service = TORBrowserService()

    return _tor_service


# WICHTIG: Keine REST API Endpoints!
# Diese Funktionen sind nur für das Browser/Terminal Modul verfügbar.
