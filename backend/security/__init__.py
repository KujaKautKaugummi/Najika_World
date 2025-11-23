"""
Najika World Security Module
Provides encryption, TOR integration, and secure communication protocols
"""

from backend.security.encryption import (
    AESEncryption,
    RSAEncryption,
    HybridEncryption,
    FernetEncryption,
    HashUtility,
    get_aes_encryptor,
    get_rsa_encryptor
)

from backend.security.tor_integration import (
    TORProxy,
    TORHiddenService,
    SOCKSSocket,
    AnonymousHTTPClient,
    get_tor_proxy,
    enable_tor,
    disable_tor,
    is_tor_enabled
)

from backend.security.secure_communication import (
    SecureMessage,
    SecureChannel,
    SecureChannelManager,
    MessageType,
    create_secure_channel_pair
)


__all__ = [
    # Encryption
    'AESEncryption',
    'RSAEncryption',
    'HybridEncryption',
    'FernetEncryption',
    'HashUtility',
    'get_aes_encryptor',
    'get_rsa_encryptor',

    # TOR Integration
    'TORProxy',
    'TORHiddenService',
    'SOCKSSocket',
    'AnonymousHTTPClient',
    'get_tor_proxy',
    'enable_tor',
    'disable_tor',
    'is_tor_enabled',

    # Secure Communication
    'SecureMessage',
    'SecureChannel',
    'SecureChannelManager',
    'MessageType',
    'create_secure_channel_pair'
]

__version__ = '1.0.0'
