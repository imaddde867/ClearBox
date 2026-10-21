import os
import sys

# Must be set before any app module is imported: app.encryption is fail-closed.
os.environ.setdefault("ENCRYPTION_KEY", "test-only-key-not-for-production")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app import models  # noqa: F401 - registers tables on Base.metadata


@pytest.fixture
def db():
    """Real in-memory SQLite session, so tests observe what is actually persisted."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
