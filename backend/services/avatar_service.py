"""
Avatar Service
Generates placeholder avatars for users
"""

from pathlib import Path
from typing import Optional
import hashlib


class AvatarService:
    """Service for generating user avatars"""

    def __init__(self):
        self.avatar_dir = Path("backend/static/avatars")
        self.avatar_dir.mkdir(parents=True, exist_ok=True)

    def get_avatar_url(self, user_id: int, username: str) -> str:
        """
        Get avatar URL for user

        Args:
            user_id: User ID
            username: Username

        Returns:
            URL to avatar image
        """
        # Use Gravatar-style hash for consistency
        email_hash = hashlib.md5(f"{username}@najika.local".encode()).hexdigest()

        # Use DiceBear API for placeholder avatars
        # https://avatars.dicebear.com/
        avatar_style = "avataaars"  # Fun, customizable avatars

        return f"https://api.dicebear.com/7.x/{avatar_style}/svg?seed={email_hash}"

    def get_avatar_data_url(self, user_id: int, username: str) -> str:
        """
        Generate simple SVG avatar as data URL

        Args:
            user_id: User ID
            username: Username

        Returns:
            Data URL with SVG avatar
        """
        # Generate color based on user_id
        hue = (user_id * 137) % 360  # Golden angle for distribution

        # Get initials from username
        initials = self._get_initials(username)

        # Create simple SVG avatar
        svg = f'''<svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
  <rect width="128" height="128" fill="hsl({hue}, 70%, 60%)"/>
  <text x="50%" y="50%" text-anchor="middle" dy=".35em"
        font-family="Arial, sans-serif" font-size="48" fill="white" font-weight="bold">
    {initials}
  </text>
</svg>'''

        # Convert to data URL
        import base64
        svg_base64 = base64.b64encode(svg.encode()).decode()
        return f"data:image/svg+xml;base64,{svg_base64}"

    def _get_initials(self, username: str) -> str:
        """Extract initials from username"""
        if not username:
            return "?"

        # Split by common separators
        parts = username.replace("_", " ").replace("-", " ").split()

        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        else:
            return username[:2].upper()


# Global instance
avatar_service = AvatarService()
