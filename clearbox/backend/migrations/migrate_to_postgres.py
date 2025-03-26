#!/usr/bin/env python
"""
Database Migration Script: SQLite to PostgreSQL

This script migrates data from a SQLite database to a PostgreSQL database
for the ClearBox application.

Usage:
    python migrate_to_postgres.py --sqlite-path path/to/clearbox.db --pg-url postgresql://user:pass@host:port/db

Requirements:
    - psycopg2-binary
    - sqlalchemy
    - python-dotenv
"""

import argparse
import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, select, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Migrate from SQLite to PostgreSQL")
    parser.add_argument("--sqlite-path", help="Path to SQLite database file", required=False)
    parser.add_argument("--pg-url", help="PostgreSQL connection URL", required=False)
    parser.add_argument("--env-file", help="Path to .env file", default=".env")
    return parser.parse_args()

def create_backup(sqlite_path):
    """Create a backup of the SQLite database."""
    import shutil
    backup_path = f"{sqlite_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(sqlite_path, backup_path)
    logger.info(f"Created backup at {backup_path}")
    return backup_path

def get_engine_from_url(url):
    """Create a SQLAlchemy engine from a URL."""
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url)

def setup_postgres_tables(pg_engine):
    """Set up PostgreSQL tables with SQLAlchemy models."""
    # Import and create tables using models
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from app.models import Base
    
    Base.metadata.create_all(pg_engine)
    logger.info("Created PostgreSQL tables")

def get_tables(engine):
    """Get a list of all tables in the database."""
    inspector = inspect(engine)
    return inspector.get_table_names()

def migrate_data(sqlite_engine, pg_engine):
    """Migrate data from SQLite to PostgreSQL."""
    # Get SQLite metadata
    sqlite_meta = MetaData()
    sqlite_meta.reflect(bind=sqlite_engine)
    
    # Get tables common to both databases
    sqlite_tables = set(get_tables(sqlite_engine))
    pg_tables = set(get_tables(pg_engine))
    common_tables = sqlite_tables.intersection(pg_tables)
    
    logger.info(f"Found {len(common_tables)} tables to migrate: {', '.join(common_tables)}")
    
    # Create sessions
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    PGSession = sessionmaker(bind=pg_engine)
    
    sqlite_session = SQLiteSession()
    pg_session = PGSession()
    
    try:
        # Migrate data for each table
        for table_name in common_tables:
            # Get table objects
            sqlite_table = Table(table_name, sqlite_meta, autoload_with=sqlite_engine)
            
            # Get all rows from SQLite
            query = select(sqlite_table)
            rows = sqlite_engine.execute(query).fetchall()
            
            if not rows:
                logger.info(f"Table {table_name} has no data to migrate")
                continue
            
            logger.info(f"Migrating {len(rows)} rows from table {table_name}")
            
            # Insert rows into PostgreSQL
            for row in rows:
                # Convert row to dict
                row_dict = dict(row)
                
                # Insert into PostgreSQL
                pg_table = Table(table_name, MetaData(), autoload_with=pg_engine)
                insert_stmt = pg_table.insert().values(**row_dict)
                pg_engine.execute(insert_stmt)
            
            logger.info(f"Successfully migrated {len(rows)} rows to table {table_name}")
        
        # Commit the transaction
        pg_session.commit()
        logger.info("Migration completed successfully")
    
    except Exception as e:
        pg_session.rollback()
        logger.error(f"Error during migration: {e}")
        raise
    finally:
        sqlite_session.close()
        pg_session.close()

def main():
    """Main migration function."""
    args = parse_args()
    
    # Load environment variables
    load_dotenv(args.env_file)
    
    # Get database URLs
    sqlite_path = args.sqlite_path or os.getenv("SQLITE_PATH", "clearbox.db")
    sqlite_url = f"sqlite:///{sqlite_path}"
    
    pg_url = args.pg_url or os.getenv("DATABASE_URL")
    if not pg_url or not pg_url.startswith("postgresql"):
        logger.error("PostgreSQL URL is required and must start with 'postgresql://'")
        sys.exit(1)
    
    logger.info(f"Migrating from {sqlite_url} to {pg_url}")
    
    # Create backup
    if os.path.exists(sqlite_path):
        create_backup(sqlite_path)
    
    # Create engines
    sqlite_engine = get_engine_from_url(sqlite_url)
    pg_engine = get_engine_from_url(pg_url)
    
    # Set up PostgreSQL tables
    setup_postgres_tables(pg_engine)
    
    # Migrate data
    migrate_data(sqlite_engine, pg_engine)
    
    logger.info("Migration completed successfully")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1) 