"""
TOR Integration Module
Provides TOR proxy support for anonymous connections
"""

import socket
import socks
import requests
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


class TORProxy:
    """
    TOR proxy manager for anonymous connections
    """

    def __init__(
        self,
        tor_proxy_host: str = '127.0.0.1',
        tor_proxy_port: int = 9050,
        control_port: int = 9051,
        control_password: Optional[str] = None
    ):
        """
        Initialize TOR proxy

        Args:
            tor_proxy_host: TOR SOCKS proxy host
            tor_proxy_port: TOR SOCKS proxy port
            control_port: TOR control port
            control_password: TOR control password (if authentication is enabled)
        """
        self.tor_proxy_host = tor_proxy_host
        self.tor_proxy_port = tor_proxy_port
        self.control_port = control_port
        self.control_password = control_password

        self.session = None
        self.enabled = False

    def is_tor_running(self) -> bool:
        """
        Check if TOR is running

        Returns:
            True if TOR is accessible, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.tor_proxy_host, self.tor_proxy_port))
            sock.close()
            return result == 0
        except Exception as e:
            logger.error(f"Error checking TOR status: {e}")
            return False

    def enable(self) -> bool:
        """
        Enable TOR proxy for requests

        Returns:
            True if TOR was enabled successfully, False otherwise
        """
        if not self.is_tor_running():
            logger.error("TOR is not running")
            return False

        try:
            # Create session with TOR proxy
            self.session = requests.Session()

            # Set SOCKS5 proxy
            self.session.proxies = {
                'http': f'socks5h://{self.tor_proxy_host}:{self.tor_proxy_port}',
                'https': f'socks5h://{self.tor_proxy_host}:{self.tor_proxy_port}'
            }

            # Verify TOR connection by checking IP
            response = self.session.get('https://check.torproject.org/api/ip', timeout=30)
            data = response.json()

            if data.get('IsTor'):
                logger.info(f"✅ TOR enabled successfully. Exit IP: {data.get('IP')}")
                self.enabled = True
                return True
            else:
                logger.error("TOR connection test failed - not using TOR network")
                self.enabled = False
                return False

        except Exception as e:
            logger.error(f"Failed to enable TOR: {e}")
            self.enabled = False
            return False

    def disable(self):
        """Disable TOR proxy"""
        self.session = None
        self.enabled = False
        logger.info("TOR disabled")

    def get_session(self) -> requests.Session:
        """
        Get requests session (with or without TOR)

        Returns:
            Requests session
        """
        if self.enabled and self.session:
            return self.session
        else:
            return requests.Session()

    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Make GET request through TOR

        Args:
            url: URL to request
            **kwargs: Additional arguments for requests.get()

        Returns:
            Response object
        """
        session = self.get_session()
        return session.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """
        Make POST request through TOR

        Args:
            url: URL to request
            **kwargs: Additional arguments for requests.post()

        Returns:
            Response object
        """
        session = self.get_session()
        return session.post(url, **kwargs)

    def get_current_ip(self) -> Optional[str]:
        """
        Get current exit IP address

        Returns:
            Current IP address or None if TOR is not enabled
        """
        if not self.enabled:
            return None

        try:
            response = self.session.get('https://api.ipify.org?format=json', timeout=10)
            data = response.json()
            return data.get('ip')
        except Exception as e:
            logger.error(f"Failed to get current IP: {e}")
            return None

    def renew_identity(self) -> bool:
        """
        Request new TOR identity (new circuit)

        Returns:
            True if identity was renewed, False otherwise
        """
        if not self.enabled:
            logger.error("TOR is not enabled")
            return False

        try:
            # Connect to TOR control port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.tor_proxy_host, self.control_port))

                # Authenticate if password is provided
                if self.control_password:
                    sock.send(f'AUTHENTICATE "{self.control_password}"\r\n'.encode())
                    response = sock.recv(1024).decode()
                    if '250 OK' not in response:
                        logger.error(f"TOR authentication failed: {response}")
                        return False

                # Request new identity
                sock.send(b'SIGNAL NEWNYM\r\n')
                response = sock.recv(1024).decode()

                if '250 OK' in response:
                    logger.info("✅ TOR identity renewed")
                    return True
                else:
                    logger.error(f"Failed to renew TOR identity: {response}")
                    return False

        except Exception as e:
            logger.error(f"Error renewing TOR identity: {e}")
            return False

    def get_circuit_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about current TOR circuit

        Returns:
            Circuit information or None if not available
        """
        if not self.enabled:
            return None

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.tor_proxy_host, self.control_port))

                if self.control_password:
                    sock.send(f'AUTHENTICATE "{self.control_password}"\r\n'.encode())
                    sock.recv(1024)

                sock.send(b'GETINFO circuit-status\r\n')
                response = sock.recv(4096).decode()

                # Parse circuit info (simplified)
                circuits = []
                for line in response.split('\r\n'):
                    if line.startswith('250'):
                        parts = line.split()
                        if len(parts) >= 3:
                            circuits.append({
                                'id': parts[1],
                                'status': parts[2] if len(parts) > 2 else 'unknown'
                            })

                return {
                    'circuits': circuits,
                    'total': len(circuits)
                }

        except Exception as e:
            logger.error(f"Error getting circuit info: {e}")
            return None


class TORHiddenService:
    """
    TOR Hidden Service (.onion) utilities
    """

    @staticmethod
    def is_onion_address(url: str) -> bool:
        """
        Check if URL is a TOR hidden service

        Args:
            url: URL to check

        Returns:
            True if URL is .onion address
        """
        parsed = urlparse(url)
        hostname = parsed.hostname or parsed.path
        return hostname.endswith('.onion')

    @staticmethod
    def validate_onion_address(address: str) -> bool:
        """
        Validate .onion address format

        Args:
            address: Onion address to validate

        Returns:
            True if address format is valid
        """
        if not address.endswith('.onion'):
            return False

        # Remove .onion suffix
        name = address[:-6]

        # V2 addresses: 16 characters (base32)
        # V3 addresses: 56 characters (base32)
        if len(name) not in [16, 56]:
            return False

        # Check if base32
        try:
            import base64
            base64.b32decode(name.upper())
            return True
        except Exception:
            return False


class SOCKSSocket:
    """
    SOCKS proxy socket wrapper
    """

    def __init__(
        self,
        proxy_host: str = '127.0.0.1',
        proxy_port: int = 9050,
        proxy_type: int = socks.SOCKS5
    ):
        """
        Initialize SOCKS socket

        Args:
            proxy_host: SOCKS proxy host
            proxy_port: SOCKS proxy port
            proxy_type: SOCKS version (SOCKS4 or SOCKS5)
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_type = proxy_type

    def create_connection(self, address: tuple, timeout: Optional[float] = None) -> socket.socket:
        """
        Create socket connection through SOCKS proxy

        Args:
            address: Tuple of (host, port)
            timeout: Connection timeout

        Returns:
            Connected socket
        """
        sock = socks.socksocket()
        sock.set_proxy(
            self.proxy_type,
            self.proxy_host,
            self.proxy_port
        )

        if timeout:
            sock.settimeout(timeout)

        sock.connect(address)
        return sock

    def patch_socket_module(self):
        """
        Patch default socket module to use SOCKS proxy
        WARNING: This affects all socket connections in the application
        """
        socks.set_default_proxy(
            self.proxy_type,
            self.proxy_host,
            self.proxy_port
        )
        socket.socket = socks.socksocket
        logger.warning("⚠️ Default socket module patched to use SOCKS proxy")

    def restore_socket_module(self):
        """
        Restore default socket module
        """
        import importlib
        importlib.reload(socket)
        logger.info("Default socket module restored")


class AnonymousHTTPClient:
    """
    HTTP client with built-in anonymization features
    """

    def __init__(self, use_tor: bool = True):
        """
        Initialize anonymous HTTP client

        Args:
            use_tor: Whether to use TOR for requests
        """
        self.tor = TORProxy() if use_tor else None
        self.session = requests.Session()

        # Set random user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        if use_tor and self.tor:
            self.tor.enable()

    def get(self, url: str, **kwargs) -> requests.Response:
        """Make anonymous GET request"""
        if self.tor and self.tor.enabled:
            return self.tor.get(url, **kwargs)
        return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """Make anonymous POST request"""
        if self.tor and self.tor.enabled:
            return self.tor.post(url, **kwargs)
        return self.session.post(url, **kwargs)

    def get_current_ip(self) -> str:
        """Get current IP address"""
        try:
            response = self.get('https://api.ipify.org?format=json', timeout=10)
            return response.json().get('ip', 'Unknown')
        except Exception as e:
            logger.error(f"Failed to get IP: {e}")
            return 'Unknown'

    def renew_identity(self) -> bool:
        """Renew TOR identity if TOR is enabled"""
        if self.tor and self.tor.enabled:
            return self.tor.renew_identity()
        return False


# Global TOR proxy instance
_tor_proxy = None


def get_tor_proxy() -> TORProxy:
    """
    Get global TOR proxy instance

    Returns:
        TOR proxy instance
    """
    global _tor_proxy
    if _tor_proxy is None:
        _tor_proxy = TORProxy()
    return _tor_proxy


def enable_tor() -> bool:
    """
    Enable TOR globally

    Returns:
        True if TOR was enabled successfully
    """
    tor = get_tor_proxy()
    return tor.enable()


def disable_tor():
    """Disable TOR globally"""
    tor = get_tor_proxy()
    tor.disable()


def is_tor_enabled() -> bool:
    """
    Check if TOR is enabled globally

    Returns:
        True if TOR is enabled
    """
    tor = get_tor_proxy()
    return tor.enabled
