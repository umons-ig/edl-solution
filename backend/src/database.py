"""
Database configuration and session management.

This module handles SQLAlchemy setup for PostgreSQL database.
Supports both production (PostgreSQL) and testing (SQLite) environments.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator
import logging

logger = logging.getLogger("taskflow")

# Database URL - Render provides DATABASE_URL automatically
# For local development, use SQLite by default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./taskflow.db"  # Local SQLite fallback
)

# Fix for Render's postgres:// URL (SQLAlchemy requires postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

logger.info(f"Connecting to database: {DATABASE_URL.split('@')[0]}...")  # Don't log credentials

# Create engine
# For SQLite, we need check_same_thread=False
# For PostgreSQL, we can use connection pooling
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # PostgreSQL connection pool settings
    engine_kwargs.update({
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,  # Verify connections before using
    })

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.

    Usage in FastAPI:
        @app.get("/tasks")
        def list_tasks(db: Session = Depends(get_db)):
            tasks = db.query(TaskModel).all()
            return tasks
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.

    This should be called on application startup.
    """
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")


def drop_db() -> None:
    """
    Drop all database tables.

    WARNING: This will delete all data!
    Only use for testing or development reset.
    """
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.warning("All tables dropped!")
