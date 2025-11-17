"""
End-to-End Encryption Module
Provides encryption/decryption utilities for secure communication
"""

import base64
import hashlib
import secrets
from typing import Tuple, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


class AESEncryption:
    """
    AES-256 symmetric encryption
    """

    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize AES encryption

        Args:
            key: 32-byte encryption key (generated if not provided)
        """
        if key is None:
            self.key = self.generate_key()
        else:
            if len(key) != 32:
                raise ValueError("Key must be 32 bytes for AES-256")
            self.key = key

    @staticmethod
    def generate_key() -> bytes:
        """Generate a random 256-bit key"""
        return secrets.token_bytes(32)

    @staticmethod
    def derive_key_from_password(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """
        Derive a key from a password using PBKDF2

        Args:
            password: Password string
            salt: Salt for key derivation (generated if not provided)

        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = kdf.derive(password.encode())
        return key, salt

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt data using AES-256-GCM

        Args:
            plaintext: Data to encrypt

        Returns:
            Encrypted data (IV + ciphertext + tag)
        """
        # Generate random IV
        iv = secrets.token_bytes(12)

        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv),
            backend=default_backend()
        )

        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        # Return IV + ciphertext + tag
        return iv + ciphertext + encryptor.tag

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt AES-256-GCM encrypted data

        Args:
            ciphertext: Encrypted data (IV + ciphertext + tag)

        Returns:
            Decrypted plaintext

        Raises:
            cryptography.exceptions.InvalidTag: If authentication fails
        """
        # Extract IV, ciphertext, and tag
        iv = ciphertext[:12]
        tag = ciphertext[-16:]
        actual_ciphertext = ciphertext[12:-16]

        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv, tag),
            backend=default_backend()
        )

        decryptor = cipher.decryptor()
        plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        return plaintext

    def encrypt_string(self, plaintext: str) -> str:
        """
        Encrypt a string and return base64-encoded result

        Args:
            plaintext: String to encrypt

        Returns:
            Base64-encoded encrypted data
        """
        encrypted = self.encrypt(plaintext.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt_string(self, ciphertext: str) -> str:
        """
        Decrypt a base64-encoded encrypted string

        Args:
            ciphertext: Base64-encoded encrypted data

        Returns:
            Decrypted string
        """
        encrypted = base64.b64decode(ciphertext.encode('utf-8'))
        decrypted = self.decrypt(encrypted)
        return decrypted.decode('utf-8')


class RSAEncryption:
    """
    RSA asymmetric encryption
    """

    def __init__(self, private_key: Optional[rsa.RSAPrivateKey] = None,
                 public_key: Optional[rsa.RSAPublicKey] = None):
        """
        Initialize RSA encryption

        Args:
            private_key: RSA private key (generated if not provided)
            public_key: RSA public key (derived from private key if not provided)
        """
        if private_key is None:
            self.private_key = self.generate_key_pair()
            self.public_key = self.private_key.public_key()
        else:
            self.private_key = private_key
            self.public_key = public_key or private_key.public_key()

    @staticmethod
    def generate_key_pair(key_size: int = 2048) -> rsa.RSAPrivateKey:
        """
        Generate RSA key pair

        Args:
            key_size: Key size in bits (2048 or 4096 recommended)

        Returns:
            RSA private key (public key can be derived from it)
        """
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )

    def export_private_key(self, password: Optional[str] = None) -> bytes:
        """
        Export private key to PEM format

        Args:
            password: Password to encrypt private key (optional)

        Returns:
            PEM-encoded private key
        """
        encryption = serialization.NoEncryption()
        if password:
            encryption = serialization.BestAvailableEncryption(password.encode())

        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )

    def export_public_key(self) -> bytes:
        """
        Export public key to PEM format

        Returns:
            PEM-encoded public key
        """
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @staticmethod
    def import_private_key(pem_data: bytes, password: Optional[str] = None) -> rsa.RSAPrivateKey:
        """
        Import private key from PEM format

        Args:
            pem_data: PEM-encoded private key
            password: Password if key is encrypted

        Returns:
            RSA private key
        """
        return serialization.load_pem_private_key(
            pem_data,
            password=password.encode() if password else None,
            backend=default_backend()
        )

    @staticmethod
    def import_public_key(pem_data: bytes) -> rsa.RSAPublicKey:
        """
        Import public key from PEM format

        Args:
            pem_data: PEM-encoded public key

        Returns:
            RSA public key
        """
        return serialization.load_pem_public_key(
            pem_data,
            backend=default_backend()
        )

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt data using RSA public key

        Args:
            plaintext: Data to encrypt (max size depends on key size)

        Returns:
            Encrypted data
        """
        return self.public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt data using RSA private key

        Args:
            ciphertext: Encrypted data

        Returns:
            Decrypted plaintext
        """
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def sign(self, message: bytes) -> bytes:
        """
        Sign a message using RSA private key

        Args:
            message: Message to sign

        Returns:
            Digital signature
        """
        return self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        Verify a signature using RSA public key

        Args:
            message: Original message
            signature: Digital signature

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            self.public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False


class HybridEncryption:
    """
    Hybrid encryption combining RSA and AES
    Uses RSA to encrypt AES key, then AES to encrypt data
    """

    def __init__(self, rsa_encryption: RSAEncryption):
        """
        Initialize hybrid encryption

        Args:
            rsa_encryption: RSA encryption instance
        """
        self.rsa = rsa_encryption

    def encrypt(self, plaintext: bytes, recipient_public_key: rsa.RSAPublicKey) -> bytes:
        """
        Encrypt data using hybrid encryption

        Args:
            plaintext: Data to encrypt
            recipient_public_key: Recipient's RSA public key

        Returns:
            Encrypted data (encrypted AES key + AES-encrypted data)
        """
        # Generate random AES key
        aes_key = AESEncryption.generate_key()
        aes = AESEncryption(aes_key)

        # Encrypt data with AES
        encrypted_data = aes.encrypt(plaintext)

        # Encrypt AES key with RSA
        rsa_temp = RSAEncryption(public_key=recipient_public_key)
        encrypted_key = rsa_temp.encrypt(aes_key)

        # Return encrypted key (256 bytes for 2048-bit RSA) + encrypted data
        key_length = len(encrypted_key).to_bytes(4, 'big')
        return key_length + encrypted_key + encrypted_data

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt hybrid-encrypted data

        Args:
            ciphertext: Encrypted data (encrypted AES key + AES-encrypted data)

        Returns:
            Decrypted plaintext
        """
        # Extract encrypted key length
        key_length = int.from_bytes(ciphertext[:4], 'big')

        # Extract encrypted AES key
        encrypted_key = ciphertext[4:4+key_length]

        # Extract AES-encrypted data
        encrypted_data = ciphertext[4+key_length:]

        # Decrypt AES key with RSA
        aes_key = self.rsa.decrypt(encrypted_key)

        # Decrypt data with AES
        aes = AESEncryption(aes_key)
        plaintext = aes.decrypt(encrypted_data)

        return plaintext


class FernetEncryption:
    """
    Simple encryption using Fernet (symmetric encryption)
    Easier to use than AES but less flexible
    """

    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize Fernet encryption

        Args:
            key: Fernet key (generated if not provided)
        """
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key

        self.fernet = Fernet(self.key)

    @staticmethod
    def generate_key() -> bytes:
        """Generate a Fernet key"""
        return Fernet.generate_key()

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt data

        Args:
            plaintext: Data to encrypt

        Returns:
            Encrypted data
        """
        return self.fernet.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt data

        Args:
            ciphertext: Encrypted data

        Returns:
            Decrypted plaintext
        """
        return self.fernet.decrypt(ciphertext)

    def encrypt_string(self, plaintext: str) -> str:
        """
        Encrypt a string

        Args:
            plaintext: String to encrypt

        Returns:
            Base64-encoded encrypted data
        """
        encrypted = self.encrypt(plaintext.encode('utf-8'))
        return encrypted.decode('utf-8')

    def decrypt_string(self, ciphertext: str) -> str:
        """
        Decrypt a string

        Args:
            ciphertext: Base64-encoded encrypted data

        Returns:
            Decrypted string
        """
        decrypted = self.decrypt(ciphertext.encode('utf-8'))
        return decrypted.decode('utf-8')


class HashUtility:
    """
    Hashing utilities for passwords and data integrity
    """

    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:
        """
        Hash a password using PBKDF2

        Args:
            password: Password to hash
            salt: Salt for hashing (generated if not provided)

        Returns:
            Tuple of (hashed_password, salt) as base64 strings
        """
        if salt is None:
            salt = secrets.token_bytes(16)

        key, salt = AESEncryption.derive_key_from_password(password, salt)

        return (
            base64.b64encode(key).decode('utf-8'),
            base64.b64encode(salt).decode('utf-8')
        )

    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """
        Verify a password against a hash

        Args:
            password: Password to verify
            hashed_password: Base64-encoded hashed password
            salt: Base64-encoded salt

        Returns:
            True if password matches, False otherwise
        """
        salt_bytes = base64.b64decode(salt.encode('utf-8'))
        key, _ = AESEncryption.derive_key_from_password(password, salt_bytes)
        expected_hash = base64.b64encode(key).decode('utf-8')

        return secrets.compare_digest(hashed_password, expected_hash)

    @staticmethod
    def sha256(data: bytes) -> str:
        """
        Calculate SHA-256 hash

        Args:
            data: Data to hash

        Returns:
            Hex-encoded hash
        """
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def sha256_file(file_path: str) -> str:
        """
        Calculate SHA-256 hash of a file

        Args:
            file_path: Path to file

        Returns:
            Hex-encoded hash
        """
        sha256_hash = hashlib.sha256()

        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()


# Singleton instances for easy access
_default_aes = None
_default_rsa = None


def get_aes_encryptor(key: Optional[bytes] = None) -> AESEncryption:
    """Get default AES encryptor instance"""
    global _default_aes
    if _default_aes is None or key is not None:
        _default_aes = AESEncryption(key)
    return _default_aes


def get_rsa_encryptor() -> RSAEncryption:
    """Get default RSA encryptor instance"""
    global _default_rsa
    if _default_rsa is None:
        _default_rsa = RSAEncryption()
    return _default_rsa
