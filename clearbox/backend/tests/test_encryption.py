import pytest
import os
from unittest.mock import patch, MagicMock
from cryptography.fernet import Fernet
from app.encryption import encrypt_message, decrypt_message, get_encryption_key, fernet


class TestEncryptionFailClosed:
    """Test that encryption failures prevent message storage (fail-closed behavior)"""

    def test_encrypt_message_succeeds_with_valid_input(self):
        """Test that encryption works with valid input"""
        message = "Hello, World!"
        encrypted = encrypt_message(message)
        assert encrypted != message
        assert isinstance(encrypted, str)

    def test_decrypt_message_succeeds_with_valid_ciphertext(self):
        """Test that decryption works with valid ciphertext"""
        message = "Hello, World!"
        encrypted = encrypt_message(message)
        decrypted = decrypt_message(encrypted)
        assert decrypted == message

    def test_encrypt_message_raises_on_invalid_key(self):
        """Test that encrypt_message raises exception when Fernet fails"""
        with patch('app.encryption.fernet') as mock_fernet:
            mock_fernet.encrypt.side_effect = Exception("Encryption failed")
            with pytest.raises(Exception, match="Encryption failed"):
                encrypt_message("test message")

    def test_decrypt_message_raises_on_invalid_ciphertext(self):
        """Test that decrypt_message raises exception with invalid ciphertext"""
        with pytest.raises(Exception):
            decrypt_message("invalid_ciphertext")

    def test_decrypt_message_raises_on_mismatched_key(self):
        """Test that decrypt_message fails with wrong key"""
        # Encrypt with one key
        message = "Secret message"
        encrypted = encrypt_message(message)

        # Try to decrypt with a different key by patching fernet
        different_fernet = Fernet(Fernet.generate_key())
        with patch('app.encryption.fernet', different_fernet):
            with pytest.raises(Exception):
                decrypt_message(encrypted)

    def test_fernet_initialization_requires_valid_key(self):
        """Test that Fernet initialization fails with invalid key"""
        with pytest.raises(Exception):
            Fernet(b"invalid_key_that_is_not_32_bytes")

    def test_get_encryption_key_returns_valid_key(self):
        """Test that get_encryption_key returns a valid Fernet key"""
        key = get_encryption_key()
        # Should be able to initialize Fernet with this key
        fernet_instance = Fernet(key)
        assert fernet_instance is not None

    def test_encrypt_decrypt_roundtrip(self):
        """Test full encrypt-decrypt roundtrip"""
        original = "This is a secret message"
        encrypted = encrypt_message(original)
        decrypted = decrypt_message(encrypted)
        assert decrypted == original
        assert encrypted != original

    def test_encrypt_message_with_bytes_input(self):
        """Test that encrypt_message handles bytes input"""
        message = b"Hello, World!"
        encrypted = encrypt_message(message)
        assert isinstance(encrypted, str)
        decrypted = decrypt_message(encrypted)
        assert decrypted == "Hello, World!"

    def test_decrypt_message_with_bytes_input(self):
        """Test that decrypt_message handles bytes input"""
        message = "Hello, World!"
        encrypted = encrypt_message(message).encode()
        decrypted = decrypt_message(encrypted)
        assert decrypted == message
