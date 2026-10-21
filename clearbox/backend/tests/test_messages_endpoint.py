import asyncio
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.encryption import (
    UNDECRYPTABLE_PLACEHOLDER,
    encrypt_message,
)
from app.models import Contact, Group, Message, User
from app.routes import websockets
from app.routes.messages import get_group_messages, get_user_messages, send_message
from app.routes.websockets import send_undelivered_messages
from app.schemas import MessageCreate


def _seed_direct_chat(db):
    alice = User(id=1, username="alice", email="alice@example.com", password="x")
    bob = User(id=2, username="bob", email="bob@example.com", password="x")
    db.add_all([alice, bob, Contact(user_id=alice.id, contact_id=bob.id)])
    db.commit()
    return alice, bob


class TestSendMessageFailClosed:
    """Encryption failures must abort before anything is written."""

    def test_direct_send_returns_500_and_writes_nothing(self, monkeypatch):
        db = MagicMock()
        db.query.return_value.filter.return_value.first.side_effect = [
            MagicMock(),  # receiver
            MagicMock(),  # contact
        ]
        monkeypatch.setattr(
            "app.routes.messages.encrypt_message",
            MagicMock(side_effect=RuntimeError("encryption unavailable")),
        )
        current_user = MagicMock(id=1)

        with pytest.raises(HTTPException) as exc_info:
            send_message(
                MessageCreate(receiver_id=2, content="hello"),
                MagicMock(),
                db,
                current_user,
            )

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Message encryption failed"
        db.add.assert_not_called()
        db.commit.assert_not_called()

    def test_group_send_returns_500_and_writes_nothing(self, monkeypatch):
        db = MagicMock()
        group = MagicMock(creator_id=1)
        db.query.return_value.filter.return_value.first.side_effect = [
            group,        # group
            MagicMock(),  # membership
        ]
        monkeypatch.setattr(
            "app.routes.messages.encrypt_message",
            MagicMock(side_effect=RuntimeError("encryption unavailable")),
        )
        current_user = MagicMock(id=1)

        with pytest.raises(HTTPException) as exc_info:
            send_message(
                MessageCreate(group_id=1, content="hello"),
                MagicMock(),
                db,
                current_user,
            )

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Message encryption failed"
        db.add.assert_not_called()
        db.commit.assert_not_called()


class TestMessageRetrievalStorageInvariant:
    """Reading messages must never persist decrypted content."""

    def test_fetch_does_not_persist_plaintext(self, db):
        alice, bob = _seed_direct_chat(db)
        ciphertext = encrypt_message("top secret")
        message = Message(
            sender_id=bob.id,
            receiver_id=alice.id,
            content=ciphertext,
            encrypted=True,
            delivered=False,
        )
        db.add(message)
        db.commit()
        message_id = message.id

        result = get_user_messages(
            user_id=bob.id, limit=50, db=db, current_user=alice
        )

        assert result[0].content == "top secret"
        assert result[0].delivered is True

        # Re-read from the database: delivery update committed, ciphertext intact.
        db.expire_all()
        stored = db.get(Message, message_id)
        assert stored.content == ciphertext
        assert stored.encrypted is True
        assert stored.delivered is True

    def test_undecryptable_message_returns_placeholder_without_hiding_others(self, db):
        alice, bob = _seed_direct_chat(db)
        readable = Message(
            sender_id=bob.id,
            receiver_id=alice.id,
            content=encrypt_message("readable"),
            encrypted=True,
            delivered=True,
        )
        corrupt = Message(
            sender_id=bob.id,
            receiver_id=alice.id,
            content="not-a-fernet-token",
            encrypted=True,
            delivered=True,
        )
        db.add_all([readable, corrupt])
        db.commit()

        result = get_user_messages(
            user_id=bob.id, limit=50, db=db, current_user=alice
        )
        by_id = {message.id: message for message in result}

        assert by_id[readable.id].content == "readable"
        assert by_id[corrupt.id].content == UNDECRYPTABLE_PLACEHOLDER

        db.expire_all()
        assert db.get(Message, corrupt.id).content == "not-a-fernet-token"

    def test_group_fetch_returns_placeholder_for_undecryptable_message(self, db):
        alice = User(id=1, username="alice", email="alice@example.com", password="x")
        group = Group(id=1, name="team", creator_id=alice.id)
        db.add_all([alice, group])
        db.commit()
        corrupt = Message(
            group_id=group.id,
            sender_id=alice.id,
            content="not-a-fernet-token",
            encrypted=True,
            delivered=True,
        )
        db.add(corrupt)
        db.commit()

        result = get_group_messages(group_id=group.id, limit=50, db=db, current_user=alice)

        assert result[0].content == UNDECRYPTABLE_PLACEHOLDER
        db.expire_all()
        assert db.get(Message, corrupt.id).content == "not-a-fernet-token"


class TestUndeliveredWebSocketMessages:
    def test_legacy_plaintext_is_sent_as_stored_and_corrupt_is_placeholder(self, db, monkeypatch):
        alice, bob = _seed_direct_chat(db)
        legacy = Message(
            sender_id=bob.id,
            receiver_id=alice.id,
            content="legacy plaintext",
            encrypted=False,
            delivered=False,
        )
        corrupt = Message(
            sender_id=bob.id,
            receiver_id=alice.id,
            content="not-a-fernet-token",
            encrypted=True,
            delivered=False,
        )
        db.add_all([legacy, corrupt])
        db.commit()

        sent = []

        async def fake_send(message_data, user_id):
            sent.append(message_data)
            return True

        monkeypatch.setattr(websockets.manager, "send_personal_message", fake_send)

        asyncio.run(send_undelivered_messages(alice.id, db))

        by_id = {message["messageId"]: message["content"] for message in sent}
        assert by_id[legacy.id] == "legacy plaintext"
        assert by_id[corrupt.id] == UNDECRYPTABLE_PLACEHOLDER
