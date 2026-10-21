#!/usr/bin/env python
"""
Re-encrypt messages written with LEGACY_ENCRYPTION_KEY using ENCRYPTION_KEY.

Run from clearbox/backend with both keys set:
    ENCRYPTION_KEY=<new> LEGACY_ENCRYPTION_KEY=<old> python migrations/reencrypt_messages.py --apply

Without --apply it only reports how many messages would change.
"""
import argparse
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from cryptography.fernet import InvalidToken

from app.database import SessionLocal
from app.encryption import decrypt_message, encrypt_message, fernet
from app.models import Message


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write new ciphertext")
    args = parser.parse_args()

    if not os.getenv("LEGACY_ENCRYPTION_KEY"):
        sys.exit("LEGACY_ENCRYPTION_KEY must be set to the old key for this migration")

    db = SessionLocal()
    rewritten = unreadable = 0
    try:
        for message in db.query(Message).filter(Message.encrypted.is_(True)):
            if not message.content:
                unreadable += 1
                continue

            try:
                fernet.decrypt(message.content.encode())
                continue  # already encrypted with the current key
            except InvalidToken:
                pass

            try:
                plaintext = decrypt_message(message.content)
            except Exception:
                unreadable += 1
                continue

            if args.apply:
                message.content = encrypt_message(plaintext)
            rewritten += 1

        if args.apply:
            db.commit()
    finally:
        db.close()

    action = "Re-encrypted" if args.apply else "Would re-encrypt"
    print(f"{action} {rewritten} message(s); {unreadable} could not be decrypted.")
    if unreadable:
        sys.exit(1)


if __name__ == "__main__":
    main()
