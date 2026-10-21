import os
import subprocess
import sys

import pytest
from cryptography.fernet import Fernet
from unittest.mock import patch

from app.encryption import encrypt_message, decrypt_message, get_encryption_key

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_in_new_process(code, encryption_key):
    """Import the app in a fresh interpreter, with ENCRYPTION_KEY under test."""
    env = os.environ.copy()
    env.pop("ENCRYPTION_KEY", None)
    env["ENCRYPTION_KEY"] = encryption_key
    env["PYTHONPATH"] = BACKEND_DIR
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        cwd=BACKEND_DIR,
    )


class TestEncryptionFailClosed:
    """Test that encryption failures prevent message storage (fail-closed behavior)"""

    def test_encrypt_message_succeeds_with_valid_input(self):
        message = "Hello, World!"
        encrypted = encrypt_message(message)
        assert encrypted != message
        assert isinstance(encrypted, str)

    def test_decrypt_message_succeeds_with_valid_ciphertext(self):
        message = "Hello, World!"
        assert decrypt_message(encrypt_message(message)) == message

    def test_encrypt_message_raises_on_invalid_key(self):
        with patch('app.encryption.fernet') as mock_fernet:
            mock_fernet.encrypt.side_effect = Exception("Encryption failed")
            with pytest.raises(Exception, match="Encryption failed"):
                encrypt_message("test message")

    def test_decrypt_message_raises_on_invalid_ciphertext(self):
        with pytest.raises(Exception):
            decrypt_message("invalid_ciphertext")

    def test_decrypt_message_raises_on_mismatched_key(self):
        encrypted = encrypt_message("Secret message")
        different_fernet = Fernet(Fernet.generate_key())
        with patch('app.encryption.fernet', different_fernet):
            with pytest.raises(Exception):
                decrypt_message(encrypted)

    def test_get_encryption_key_returns_valid_key(self):
        assert Fernet(get_encryption_key()) is not None

    def test_encrypt_decrypt_roundtrip(self):
        original = "This is a secret message"
        encrypted = encrypt_message(original)
        assert decrypt_message(encrypted) == original
        assert encrypted != original

    def test_encrypt_message_with_bytes_input(self):
        encrypted = encrypt_message(b"Hello, World!")
        assert isinstance(encrypted, str)
        assert decrypt_message(encrypted) == "Hello, World!"

    def test_decrypt_message_with_bytes_input(self):
        message = "Hello, World!"
        assert decrypt_message(encrypt_message(message).encode()) == message


class TestEncryptionKeyConfiguration:
    """The process must refuse to start without an explicit, non-trivial key."""

    def test_empty_key_prevents_startup(self):
        result = _run_in_new_process("import app.encryption", "")
        assert result.returncode != 0
        assert "ENCRYPTION_KEY environment variable is required" in result.stderr

    def test_short_key_prevents_startup(self):
        result = _run_in_new_process("import app.encryption", "short")
        assert result.returncode != 0
        assert "at least 16 characters" in result.stderr

    def test_configured_key_is_reused_across_restarts(self):
        key = "restart-test-key-0123456789abcdef"
        encrypted = _run_in_new_process(
            "import app.encryption as e; print(e.encrypt_message('across-restart'))",
            key,
        )
        assert encrypted.returncode == 0, encrypted.stderr
        ciphertext = encrypted.stdout.strip()

        decrypted = _run_in_new_process(
            f"import app.encryption as e; print(e.decrypt_message({ciphertext!r}))",
            key,
        )
        assert decrypted.returncode == 0, decrypted.stderr
        assert decrypted.stdout.strip() == "across-restart"

    def test_different_key_cannot_decrypt_existing_ciphertext(self):
        ciphertext = encrypt_message("existing message")

        result = _run_in_new_process(
            f"import app.encryption as e; e.decrypt_message({ciphertext!r})",
            "a-different-key-0123456789abcdef",
        )

        assert result.returncode != 0
        assert "InvalidToken" in result.stderr
