import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

# Load encryption key from environment or generate one
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "supersecretkey").encode()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_encryption_key():
    """
    Generate an encryption key from the master key
    """
    salt = b'clearbox_salt_value'  # Should be stored securely in a real app
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(ENCRYPTION_KEY))
    return key

# Initialize Fernet with our key
try:
    fernet = Fernet(get_encryption_key())
except Exception as e:
    logger.error(f"Failed to initialize encryption: {e}")
    # For demo purposes, create a dummy encryption that just passes through
    class DummyFernet:
        def encrypt(self, data):
            if isinstance(data, str):
                data = data.encode()
            return data

        def decrypt(self, data):
            if isinstance(data, bytes):
                try:
                    return data.decode()
                except:
                    return str(data)
            return str(data)

    fernet = DummyFernet()
    logger.warning("Using dummy encryption for demo purposes")

def encrypt_message(message):
    """
    Encrypt a message
    """
    try:
        if isinstance(message, str):
            message = message.encode()
        encrypted = fernet.encrypt(message)
        return encrypted.decode() if isinstance(encrypted, bytes) else encrypted
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        return message

def decrypt_message(encrypted_message):
    """
    Decrypt a message
    """
    try:
        if isinstance(encrypted_message, str):
            encrypted_message = encrypted_message.encode()
        decrypted = fernet.decrypt(encrypted_message)
        return decrypted.decode() if isinstance(decrypted, bytes) else decrypted
    except Exception as e:
        # Don't log every single error with empty message to avoid console spam
        if str(e):
            logger.error(f"Decryption error: {e}")
        return "[Encrypted message]"

# Generate a Fernet key to be used for message encryption/decryption
def generate_key():
    """Generate a new Fernet key."""
    return Fernet.generate_key().decode()