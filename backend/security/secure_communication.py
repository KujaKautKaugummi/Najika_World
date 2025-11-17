"""
Secure Communication Module
Provides secure communication protocols with encryption and authentication
"""

import json
import time
import secrets
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from backend.security.encryption import AESEncryption, RSAEncryption, HybridEncryption


logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Message types for secure communication"""
    HANDSHAKE = "handshake"
    KEY_EXCHANGE = "key_exchange"
    DATA = "data"
    ACK = "acknowledgment"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


@dataclass
class SecureMessage:
    """
    Secure message structure
    """
    message_type: str
    sender_id: str
    recipient_id: str
    timestamp: float
    nonce: str
    payload: Any
    signature: Optional[str] = None
    encrypted: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecureMessage':
        """Create from dictionary"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'SecureMessage':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class SecureChannel:
    """
    Secure communication channel with encryption and authentication
    """

    def __init__(
        self,
        channel_id: str,
        my_id: str,
        my_rsa_key: RSAEncryption,
        peer_public_key: Optional[Any] = None
    ):
        """
        Initialize secure channel

        Args:
            channel_id: Unique channel identifier
            my_id: My identifier
            my_rsa_key: My RSA encryption instance
            peer_public_key: Peer's RSA public key (can be set later)
        """
        self.channel_id = channel_id
        self.my_id = my_id
        self.my_rsa_key = my_rsa_key
        self.peer_id: Optional[str] = None
        self.peer_public_key = peer_public_key

        # Session key for symmetric encryption
        self.session_key: Optional[bytes] = None
        self.aes_encryption: Optional[AESEncryption] = None

        # Message tracking
        self.sent_nonces = set()
        self.received_nonces = set()
        self.max_nonce_age = 300  # 5 minutes

        # State
        self.established = False
        self.last_activity = time.time()

    def generate_nonce(self) -> str:
        """Generate unique nonce for message"""
        nonce = secrets.token_hex(16)
        self.sent_nonces.add(nonce)
        return nonce

    def is_nonce_valid(self, nonce: str) -> bool:
        """
        Check if nonce is valid (not replayed)

        Args:
            nonce: Nonce to check

        Returns:
            True if nonce is valid
        """
        if nonce in self.received_nonces:
            logger.warning(f"Replay attack detected: nonce {nonce} already used")
            return False

        self.received_nonces.add(nonce)

        # Clean old nonces
        if len(self.received_nonces) > 1000:
            self.received_nonces.clear()

        return True

    def create_message(
        self,
        message_type: MessageType,
        recipient_id: str,
        payload: Any,
        encrypt: bool = True
    ) -> SecureMessage:
        """
        Create a secure message

        Args:
            message_type: Type of message
            recipient_id: Recipient identifier
            payload: Message payload
            encrypt: Whether to encrypt the message

        Returns:
            Secure message
        """
        message = SecureMessage(
            message_type=message_type.value,
            sender_id=self.my_id,
            recipient_id=recipient_id,
            timestamp=time.time(),
            nonce=self.generate_nonce(),
            payload=payload,
            encrypted=encrypt
        )

        # Encrypt payload if requested and session key is available
        if encrypt and self.aes_encryption:
            encrypted_payload = self.aes_encryption.encrypt_string(
                json.dumps(payload) if not isinstance(payload, str) else payload
            )
            message.payload = encrypted_payload
            message.encrypted = True

        # Sign message
        message_bytes = json.dumps({
            'type': message.message_type,
            'sender': message.sender_id,
            'recipient': message.recipient_id,
            'timestamp': message.timestamp,
            'nonce': message.nonce,
            'payload': message.payload
        }).encode()

        signature = self.my_rsa_key.sign(message_bytes)
        message.signature = signature.hex()

        return message

    def verify_message(self, message: SecureMessage) -> bool:
        """
        Verify message signature and authenticity

        Args:
            message: Message to verify

        Returns:
            True if message is valid
        """
        # Check recipient
        if message.recipient_id != self.my_id:
            logger.warning(f"Message not for me: {message.recipient_id} != {self.my_id}")
            return False

        # Check nonce
        if not self.is_nonce_valid(message.nonce):
            return False

        # Check timestamp (prevent old messages)
        age = time.time() - message.timestamp
        if age > self.max_nonce_age or age < -10:  # Allow 10s clock skew
            logger.warning(f"Message too old or from future: {age}s")
            return False

        # Verify signature
        if not message.signature or not self.peer_public_key:
            logger.warning("Cannot verify message: missing signature or peer public key")
            return False

        message_bytes = json.dumps({
            'type': message.message_type,
            'sender': message.sender_id,
            'recipient': message.recipient_id,
            'timestamp': message.timestamp,
            'nonce': message.nonce,
            'payload': message.payload
        }).encode()

        signature = bytes.fromhex(message.signature)
        rsa_temp = RSAEncryption(public_key=self.peer_public_key)

        if not rsa_temp.verify(message_bytes, signature):
            logger.warning("Message signature verification failed")
            return False

        return True

    def decrypt_message(self, message: SecureMessage) -> Any:
        """
        Decrypt message payload

        Args:
            message: Message to decrypt

        Returns:
            Decrypted payload
        """
        if not message.encrypted:
            return message.payload

        if not self.aes_encryption:
            raise ValueError("No session key available for decryption")

        decrypted_str = self.aes_encryption.decrypt_string(message.payload)

        try:
            return json.loads(decrypted_str)
        except json.JSONDecodeError:
            return decrypted_str

    def initiate_handshake(self) -> SecureMessage:
        """
        Initiate handshake with peer

        Returns:
            Handshake message
        """
        # Generate session key
        self.session_key = AESEncryption.generate_key()
        self.aes_encryption = AESEncryption(self.session_key)

        # Encrypt session key with peer's public key
        if not self.peer_public_key:
            raise ValueError("Peer public key not set")

        hybrid = HybridEncryption(self.my_rsa_key)
        encrypted_key = hybrid.rsa.public_key = self.peer_public_key
        encrypted_key_data = RSAEncryption(public_key=self.peer_public_key).encrypt(self.session_key)

        payload = {
            'channel_id': self.channel_id,
            'session_key': encrypted_key_data.hex(),
            'public_key': self.my_rsa_key.export_public_key().decode('utf-8')
        }

        return self.create_message(
            MessageType.HANDSHAKE,
            self.peer_id or "peer",
            payload,
            encrypt=False
        )

    def handle_handshake(self, message: SecureMessage) -> SecureMessage:
        """
        Handle handshake message from peer

        Args:
            message: Handshake message

        Returns:
            Acknowledgment message
        """
        if not self.verify_message(message):
            raise ValueError("Invalid handshake message")

        payload = message.payload

        # Import peer's public key
        peer_public_key_pem = payload['public_key'].encode('utf-8')
        self.peer_public_key = RSAEncryption.import_public_key(peer_public_key_pem)
        self.peer_id = message.sender_id

        # Decrypt session key
        encrypted_key = bytes.fromhex(payload['session_key'])
        self.session_key = self.my_rsa_key.decrypt(encrypted_key)
        self.aes_encryption = AESEncryption(self.session_key)

        self.established = True
        logger.info(f"✅ Secure channel established with {self.peer_id}")

        # Send acknowledgment
        return self.create_message(
            MessageType.ACK,
            self.peer_id,
            {'status': 'handshake_complete'},
            encrypt=True
        )

    def send_data(self, data: Any) -> SecureMessage:
        """
        Send encrypted data

        Args:
            data: Data to send

        Returns:
            Data message
        """
        if not self.established:
            raise ValueError("Channel not established. Perform handshake first.")

        return self.create_message(
            MessageType.DATA,
            self.peer_id,
            data,
            encrypt=True
        )

    def receive_data(self, message: SecureMessage) -> Any:
        """
        Receive and decrypt data

        Args:
            message: Data message

        Returns:
            Decrypted data
        """
        if not self.verify_message(message):
            raise ValueError("Invalid data message")

        return self.decrypt_message(message)

    def ping(self) -> SecureMessage:
        """Send ping message"""
        return self.create_message(
            MessageType.PING,
            self.peer_id,
            {'timestamp': time.time()},
            encrypt=True
        )

    def pong(self, ping_message: SecureMessage) -> SecureMessage:
        """
        Respond to ping message

        Args:
            ping_message: Ping message

        Returns:
            Pong message
        """
        return self.create_message(
            MessageType.PONG,
            self.peer_id,
            {'ping_timestamp': ping_message.timestamp, 'pong_timestamp': time.time()},
            encrypt=True
        )

    def close(self):
        """Close secure channel"""
        self.established = False
        self.session_key = None
        self.aes_encryption = None
        logger.info(f"Secure channel {self.channel_id} closed")


class SecureChannelManager:
    """
    Manager for multiple secure channels
    """

    def __init__(self, my_id: str, my_rsa_key: RSAEncryption):
        """
        Initialize channel manager

        Args:
            my_id: My identifier
            my_rsa_key: My RSA encryption instance
        """
        self.my_id = my_id
        self.my_rsa_key = my_rsa_key
        self.channels: Dict[str, SecureChannel] = {}

        # Message handlers
        self.message_handlers: Dict[str, Callable] = {
            MessageType.HANDSHAKE.value: self._handle_handshake,
            MessageType.DATA.value: self._handle_data,
            MessageType.PING.value: self._handle_ping,
            MessageType.PONG.value: self._handle_pong
        }

        # Custom data handlers
        self.data_handlers: Dict[str, Callable] = {}

    def create_channel(
        self,
        peer_id: str,
        peer_public_key: Optional[Any] = None
    ) -> SecureChannel:
        """
        Create a new secure channel

        Args:
            peer_id: Peer identifier
            peer_public_key: Peer's public key (optional)

        Returns:
            Secure channel
        """
        channel_id = f"{self.my_id}_{peer_id}_{secrets.token_hex(8)}"

        channel = SecureChannel(
            channel_id=channel_id,
            my_id=self.my_id,
            my_rsa_key=self.my_rsa_key,
            peer_public_key=peer_public_key
        )

        channel.peer_id = peer_id
        self.channels[channel_id] = channel

        logger.info(f"Created secure channel: {channel_id}")
        return channel

    def get_channel(self, channel_id: str) -> Optional[SecureChannel]:
        """Get channel by ID"""
        return self.channels.get(channel_id)

    def get_channel_by_peer(self, peer_id: str) -> Optional[SecureChannel]:
        """Get channel by peer ID"""
        for channel in self.channels.values():
            if channel.peer_id == peer_id and channel.established:
                return channel
        return None

    def register_data_handler(self, data_type: str, handler: Callable):
        """
        Register handler for specific data type

        Args:
            data_type: Data type identifier
            handler: Handler function
        """
        self.data_handlers[data_type] = handler

    def handle_message(self, message: SecureMessage) -> Optional[SecureMessage]:
        """
        Handle incoming message

        Args:
            message: Incoming message

        Returns:
            Response message (if any)
        """
        handler = self.message_handlers.get(message.message_type)

        if handler:
            return handler(message)
        else:
            logger.warning(f"No handler for message type: {message.message_type}")
            return None

    def _handle_handshake(self, message: SecureMessage) -> Optional[SecureMessage]:
        """Handle handshake message"""
        # Create or get channel
        channel_id = message.payload.get('channel_id')
        channel = self.channels.get(channel_id)

        if not channel:
            # Create new channel for incoming handshake
            channel = self.create_channel(message.sender_id)

        return channel.handle_handshake(message)

    def _handle_data(self, message: SecureMessage) -> Optional[SecureMessage]:
        """Handle data message"""
        # Find channel
        channel = self.get_channel_by_peer(message.sender_id)

        if not channel:
            logger.error(f"No established channel with {message.sender_id}")
            return None

        # Decrypt and process data
        data = channel.receive_data(message)

        # Call custom handler if registered
        if isinstance(data, dict) and 'type' in data:
            handler = self.data_handlers.get(data['type'])
            if handler:
                handler(data, channel)

        return None

    def _handle_ping(self, message: SecureMessage) -> Optional[SecureMessage]:
        """Handle ping message"""
        channel = self.get_channel_by_peer(message.sender_id)

        if channel:
            return channel.pong(message)

        return None

    def _handle_pong(self, message: SecureMessage) -> Optional[SecureMessage]:
        """Handle pong message"""
        # Calculate latency
        data = message.payload
        if 'ping_timestamp' in data and 'pong_timestamp' in data:
            latency = (time.time() - data['ping_timestamp']) * 1000
            logger.info(f"Ping latency: {latency:.2f}ms")

        return None

    def close_channel(self, channel_id: str):
        """Close a channel"""
        channel = self.channels.get(channel_id)
        if channel:
            channel.close()
            del self.channels[channel_id]

    def close_all(self):
        """Close all channels"""
        for channel in list(self.channels.values()):
            channel.close()
        self.channels.clear()


# Example usage functions
def create_secure_channel_pair() -> tuple[SecureChannel, SecureChannel]:
    """
    Create a pair of secure channels for testing

    Returns:
        Tuple of (channel_a, channel_b)
    """
    # Create RSA keys for both parties
    rsa_a = RSAEncryption()
    rsa_b = RSAEncryption()

    # Create channels
    channel_a = SecureChannel(
        channel_id="test_channel",
        my_id="alice",
        my_rsa_key=rsa_a,
        peer_public_key=rsa_b.public_key
    )
    channel_a.peer_id = "bob"

    channel_b = SecureChannel(
        channel_id="test_channel",
        my_id="bob",
        my_rsa_key=rsa_b,
        peer_public_key=rsa_a.public_key
    )
    channel_b.peer_id = "alice"

    return channel_a, channel_b
