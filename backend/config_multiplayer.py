"""
Multiplayer Feature Flag & Whitelist Configuration
==================================================

Environment-based toggles for multiplayer functionality

Phases:
1. PRIVATE (Whitelist only, testing)
2. BETA (Extended whitelist, closed beta)
3. PUBLIC (Open for all)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

import os
from enum import Enum
from typing import List, Optional


class MultiplayerPhase(Enum):
    """Multiplayer Release Phases"""
    DISABLED = "disabled"
    PRIVATE = "private"
    BETA = "beta"
    PUBLIC = "public"


class MultiplayerConfig:
    """Multiplayer Feature Configuration"""

    def __init__(self):
        # Feature Toggle (Environment Variable)
        self.enabled = os.getenv("MULTIPLAYER_ENABLED", "false").lower() == "true"

        # Release Phase
        phase_str = os.getenv("MULTIPLAYER_PHASE", "disabled").lower()
        try:
            self.phase = MultiplayerPhase(phase_str)
        except ValueError:
            self.phase = MultiplayerPhase.DISABLED

        # Whitelist (for PRIVATE and BETA phases)
        self.whitelist_file = os.getenv("MULTIPLAYER_WHITELIST_FILE", "multiplayer_whitelist.txt")

        # Max Players
        self.max_players_per_room = int(os.getenv("MULTIPLAYER_MAX_PLAYERS", "10"))
        self.max_total_players = int(os.getenv("MULTIPLAYER_MAX_TOTAL", "100"))

    def is_enabled(self) -> bool:
        """Check if multiplayer is enabled"""
        return self.enabled and self.phase != MultiplayerPhase.DISABLED

    def can_join(self, user_id: int, username: str) -> tuple[bool, str]:
        """
        Check if user can join multiplayer

        Returns:
            (can_join: bool, reason: str)
        """
        # Check if multiplayer enabled
        if not self.is_enabled():
            return False, "Multiplayer ist derzeit deaktiviert"

        # PUBLIC phase: everyone can join
        if self.phase == MultiplayerPhase.PUBLIC:
            return True, "OK"

        # PRIVATE/BETA phase: check whitelist
        if self.phase in [MultiplayerPhase.PRIVATE, MultiplayerPhase.BETA]:
            if self._is_whitelisted(user_id, username):
                return True, "OK"
            else:
                return False, f"Du bist nicht für die {self.phase.value.upper()} Phase freigeschaltet"

        return False, "Unbekannter Fehler"

    def _is_whitelisted(self, user_id: int, username: str) -> bool:
        """Check if user is whitelisted"""
        whitelist = self._load_whitelist()

        # Check by user_id or username
        return (
            str(user_id) in whitelist or
            username.lower() in [w.lower() for w in whitelist]
        )

    def _load_whitelist(self) -> List[str]:
        """Load whitelist from file"""
        try:
            with open(self.whitelist_file, 'r') as f:
                # Read lines, strip whitespace, ignore comments
                lines = [
                    line.strip()
                    for line in f.readlines()
                    if line.strip() and not line.strip().startswith('#')
                ]
                return lines
        except FileNotFoundError:
            # No whitelist file = empty whitelist
            return []
        except Exception as e:
            print(f"Error loading whitelist: {e}")
            return []

    def add_to_whitelist(self, identifier: str) -> bool:
        """
        Add user_id or username to whitelist

        Args:
            identifier: user_id or username

        Returns:
            Success
        """
        try:
            # Load existing whitelist
            whitelist = self._load_whitelist()

            # Check if already whitelisted
            if identifier in whitelist:
                return True

            # Append to file
            with open(self.whitelist_file, 'a') as f:
                f.write(f"{identifier}\n")

            return True

        except Exception as e:
            print(f"Error adding to whitelist: {e}")
            return False

    def remove_from_whitelist(self, identifier: str) -> bool:
        """
        Remove user_id or username from whitelist

        Args:
            identifier: user_id or username

        Returns:
            Success
        """
        try:
            # Load existing whitelist
            whitelist = self._load_whitelist()

            # Remove identifier
            whitelist = [w for w in whitelist if w != identifier]

            # Write back to file
            with open(self.whitelist_file, 'w') as f:
                for entry in whitelist:
                    f.write(f"{entry}\n")

            return True

        except Exception as e:
            print(f"Error removing from whitelist: {e}")
            return False

    def get_status(self) -> dict:
        """Get multiplayer configuration status"""
        return {
            "enabled": self.enabled,
            "phase": self.phase.value,
            "max_players_per_room": self.max_players_per_room,
            "max_total_players": self.max_total_players,
            "whitelist_count": len(self._load_whitelist()) if self.phase in [MultiplayerPhase.PRIVATE, MultiplayerPhase.BETA] else None
        }


# Global instance
_multiplayer_config: Optional[MultiplayerConfig] = None


def get_multiplayer_config() -> MultiplayerConfig:
    """Get global multiplayer config instance"""
    global _multiplayer_config

    if _multiplayer_config is None:
        _multiplayer_config = MultiplayerConfig()

    return _multiplayer_config


"""
USAGE EXAMPLE:
==============

# In environment / .env file:
MULTIPLAYER_ENABLED=true
MULTIPLAYER_PHASE=private
MULTIPLAYER_WHITELIST_FILE=multiplayer_whitelist.txt
MULTIPLAYER_MAX_PLAYERS=10
MULTIPLAYER_MAX_TOTAL=100

# In code:
from backend.config_multiplayer import get_multiplayer_config

config = get_multiplayer_config()

if config.is_enabled():
    can_join, reason = config.can_join(user.id, user.username)
    if can_join:
        # Allow multiplayer access
        pass
    else:
        # Deny access, show reason
        pass
"""
