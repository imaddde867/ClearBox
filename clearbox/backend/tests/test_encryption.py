import contextlib
import os
import subprocess
import sys
from pathlib import Path

import pytest
from cryptography.fernet import Fernet, InvalidToken
from unittest.mock import patch

from app.encryption import encrypt_message, decrypt_message, get_encryption_key

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_in_new_process(code, encryption_key=None, extra_env=None):
    """Import the app in a fresh interpreter, with ENCRYPTION_KEY under test."""
    env = os.environ.copy()
    env.pop("ENCRYPTION_KEY", None)
    env.pop("LEGACY_ENCRYPTION_KEY", None)
    if encryption_key is not None:
        env["ENCRYPTION_KEY"] = encryption_key
    if extra_env:
        env.update(extra_env)
    env["PYTHONPATH"] = BACKEND_DIR
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        cwd=BACKEND_DIR,
    )


@contextlib.contextmanager
def _env_file_with(contents):
    """Temporarily replace backend/.env, restoring any existing file afterwards."""
    env_path = Path(BACKEND_DIR) / ".env"
    backup = env_path.read_bytes() if env_path.exists() else None
    env_path.write_text(contents)
    try:
        yield
    finally:
        if backup is None:
            env_path.unlink(missing_ok=True)
        else:
            env_path.write_bytes(backup)


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

    def test_env_file_with_key_initializes_settings(self):
        with _env_file_with("ENCRYPTION_KEY=env-file-key-0123456789abcdef\n"):
            result = _run_in_new_process(
                "import app.config as c; print(c.settings.encryption_key)"
            )

        assert result.returncode == 0, result.stderr
        assert result.stdout.strip().splitlines()[-1] == "env-file-key-0123456789abcdef"

    def test_app_imports_with_full_env_template(self):
        template = (Path(BACKEND_DIR) / ".env.template").read_text()
        contents = template.replace(
            "\nENCRYPTION_KEY=\n",
            "\nENCRYPTION_KEY=startup-test-key-0123456789\n",
        ).replace(
            "\n# LEGACY_ENCRYPTION_KEY=\n",
            "\nLEGACY_ENCRYPTION_KEY=supersecretkey\n",
        )
        with _env_file_with(contents):
            result = _run_in_new_process(
                "import app.main; print('APP IMPORT OK')",
                extra_env={
                    "DATABASE_URL": "sqlite://",
                    "MQTT_BROKER": "127.0.0.1",
                    "MQTT_PORT": "1",
                    "MQTT_USE_SSL": "false",
                },
            )

        assert result.returncode == 0, result.stderr
        assert "APP IMPORT OK" in result.stdout

    def test_legacy_key_decrypts_old_ciphertext(self):
        # Ciphertext produced by the former hardcoded 14-character default.
        legacy = Fernet(get_encryption_key(b"supersecretkey"))
        ciphertext = legacy.encrypt(b"old message").decode()

        result = _run_in_new_process(
            f"import app.encryption as e; print(e.decrypt_message({ciphertext!r}))",
            "new-strong-key-0123456789abcdef",
            {"LEGACY_ENCRYPTION_KEY": "supersecretkey"},
        )

        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "old message"

    def test_new_messages_use_current_key_not_legacy(self):
        result = _run_in_new_process(
            "import app.encryption as e; print(e.encrypt_message('new message'))",
            "new-strong-key-0123456789abcdef",
            {"LEGACY_ENCRYPTION_KEY": "supersecretkey"},
        )
        assert result.returncode == 0, result.stderr
        ciphertext = result.stdout.strip()

        current = Fernet(get_encryption_key(b"new-strong-key-0123456789abcdef"))
        assert current.decrypt(ciphertext.encode()) == b"new message"

        legacy = Fernet(get_encryption_key(b"supersecretkey"))
        with pytest.raises(InvalidToken):
            legacy.decrypt(ciphertext.encode())

    def test_old_ciphertext_fails_without_legacy_key(self):
        legacy = Fernet(get_encryption_key(b"supersecretkey"))
        ciphertext = legacy.encrypt(b"old message").decode()

        result = _run_in_new_process(
            f"import app.encryption as e; e.decrypt_message({ciphertext!r})",
            "new-strong-key-0123456789abcdef",
        )

        assert result.returncode != 0
        assert "InvalidToken" in result.stderr
