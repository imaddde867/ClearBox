from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clearbox.db")

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    logger.info("Using SQLite database")
elif DATABASE_URL.startswith("postgresql"):
    # PostgreSQL settings
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,                 # Connection pool size
        max_overflow=10,             # Allow 10 connections to exceed pool_size if needed
        pool_timeout=30,             # Wait time for connection from pool (seconds)
        pool_recycle=1800,           # Recycle connections after 30 minutes
        pool_pre_ping=True,          # Verify connections before using
        echo=True                    # SQL echo for debugging
    )
    logger.info("Using PostgreSQL database")
else:
    engine = create_engine(DATABASE_URL)
    logger.info(f"Using database: {DATABASE_URL}")

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()