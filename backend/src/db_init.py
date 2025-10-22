"""
Database initialization script.

Run this script to initialize the database with tables.
Can also be used to reset the database for development.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import init_db, drop_db, engine
from src.models import TaskModel  # Import to register models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("taskflow")


def main():
    """Initialize database tables."""
    logger.info("Starting database initialization...")

    try:
        # Create all tables
        init_db()
        logger.info("✅ Database initialized successfully!")

        # Show created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {', '.join(tables)}")

    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


def reset():
    """Reset database by dropping and recreating all tables."""
    logger.warning("⚠️  RESETTING DATABASE - ALL DATA WILL BE LOST!")

    try:
        # Drop all tables
        drop_db()

        # Recreate all tables
        init_db()

        logger.info("✅ Database reset successfully!")

    except Exception as e:
        logger.error(f"❌ Failed to reset database: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database management utilities")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset database (drop and recreate all tables)"
    )

    args = parser.parse_args()

    if args.reset:
        confirm = input("Are you sure you want to RESET the database? (yes/no): ")
        if confirm.lower() == "yes":
            reset()
        else:
            logger.info("Reset cancelled.")
    else:
        main()
