import os
import subprocess
import sys
from pathlib import Path

import pytest
from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.encryption import get_encryption_key
from app.models import Message, User

BACKEND_DIR = Path(__file__).resolve().parent.parent
NEW_KEY = "migration-new-key-0123456789"
OLD_KEY = "supersecretkey"


def test_reencrypt_messages_migrates_legacy_ciphertext(tmp_path):
    db_path = tmp_path / "clearbox.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    legacy = Fernet(get_encryption_key(OLD_KEY.encode()))
    session.add_all([
        User(id=1, username="alice", email="alice@example.com", password="x"),
        Message(
            id=1,
            sender_id=1,
            content=legacy.encrypt(b"historical message").decode(),
            encrypted=True,
            delivered=True,
        ),
    ])
    session.commit()
    session.close()
    engine.dispose()

    env = os.environ.copy()
    env.update({
        "ENCRYPTION_KEY": NEW_KEY,
        "LEGACY_ENCRYPTION_KEY": OLD_KEY,
        "DATABASE_URL": f"sqlite:///{db_path}",
        "PYTHONPATH": str(BACKEND_DIR),
    })
    result = subprocess.run(
        [sys.executable, "migrations/reencrypt_messages.py", "--apply"],
        capture_output=True,
        text=True,
        env=env,
        cwd=BACKEND_DIR,
    )

    assert result.returncode == 0, result.stderr
    assert "Re-encrypted 1 message(s)" in result.stdout

    engine = create_engine(f"sqlite:///{db_path}")
    session = sessionmaker(bind=engine)()
    stored = session.get(Message, 1).content
    session.close()
    engine.dispose()

    current = Fernet(get_encryption_key(NEW_KEY.encode()))
    assert current.decrypt(stored.encode()) == b"historical message"
    with pytest.raises(InvalidToken):
        legacy.decrypt(stored.encode())
