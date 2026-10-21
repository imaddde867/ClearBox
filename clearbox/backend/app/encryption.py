import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv

load_dotenv()

# Load encryption key from environment - required for security
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError(
        "ENCRYPTION_KEY environment variable is required. "
        "Set a strong, unique secret key before starting the application."
    )
if len(ENCRYPTION_KEY) < 16:
    raise ValueError(
        "ENCRYPTION_KEY must be at least 16 characters long for security. "
        "Use a strong, randomly generated secret."
    )
ENCRYPTION_KEY = ENCRYPTION_KEY.encode()

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
fernet = Fernet(get_encryption_key())

# Shown instead of ciphertext when a stored message cannot be decrypted
UNDECRYPTABLE_PLACEHOLDER = "[Encrypted message - cannot be decrypted]"

def encrypt_message(message):
    """
    Encrypt a message
    """
    if isinstance(message, str):
        message = message.encode()
    encrypted = fernet.encrypt(message)
    return encrypted.decode() if isinstance(encrypted, bytes) else encrypted

def decrypt_message(encrypted_message):
    """
    Decrypt a message
    """
    if isinstance(encrypted_message, str):
        encrypted_message = encrypted_message.encode()
    decrypted = fernet.decrypt(encrypted_message)
    return decrypted.decode() if isinstance(decrypted, bytes) else decrypted

# Generate a Fernet key to be used for message encryption/decryption
def generate_key():
    """Generate a new Fernet key."""
    return Fernet.generate_key().decode()