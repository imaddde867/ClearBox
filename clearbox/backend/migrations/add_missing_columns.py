#!/usr/bin/env python
"""
Database Migration Script: Add Missing Columns

This script adds missing columns to the PostgreSQL database for the ClearBox application.
It specifically adds the full_name, bio, and avatar_url columns to the users table.

Usage:
    python add_missing_columns.py --pg-url postgresql://user:pass@host:port/db

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
import psycopg2
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"migration_add_columns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Add missing columns to PostgreSQL database")
    parser.add_argument("--pg-url", help="PostgreSQL connection URL", required=False)
    parser.add_argument("--env-file", help="Path to .env file", default=".env")
    return parser.parse_args()

def add_missing_columns(pg_url):
    """Add missing columns to the users table."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(pg_url)
        conn.autocommit = False
        cursor = conn.cursor()
        
        # Check if columns exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'")
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Add missing columns
        columns_to_add = []
        if 'full_name' not in existing_columns:
            columns_to_add.append("ADD COLUMN full_name VARCHAR")
        
        if 'bio' not in existing_columns:
            columns_to_add.append("ADD COLUMN bio TEXT")
        
        if 'avatar_url' not in existing_columns:
            columns_to_add.append("ADD COLUMN avatar_url VARCHAR")
        
        if columns_to_add:
            alter_sql = f"ALTER TABLE users {', '.join(columns_to_add)}"
            logger.info(f"Executing SQL: {alter_sql}")
            cursor.execute(alter_sql)
            logger.info(f"Added {len(columns_to_add)} columns to users table")
        else:
            logger.info("No missing columns to add")
        
        # Commit the transaction
        conn.commit()
        logger.info("Migration completed successfully")
    
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error during migration: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def main():
    """Main migration function."""
    args = parse_args()
    
    # Load environment variables
    load_dotenv(args.env_file)
    
    # Get database URL
    pg_url = args.pg_url or os.getenv("DATABASE_URL")
    if not pg_url or not pg_url.startswith("postgresql"):
        logger.error("PostgreSQL URL is required and must start with 'postgresql://'")
        sys.exit(1)
    
    logger.info(f"Adding missing columns to database at {pg_url}")
    
    # Add missing columns
    add_missing_columns(pg_url)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)
