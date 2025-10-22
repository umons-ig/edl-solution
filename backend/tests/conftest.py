"""
Test Configuration for TaskFlow - Workshop Version

This file sets up the test environment for pytest.
Fixtures are reusable test components with database support.
"""

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app import app
from src.database import Base, get_db
from src.models import TaskModel  # Import models to register them with Base

# Use SQLite file-based database for testing (shared across threads)
import tempfile
import os as os_module

# Create a temporary database file for each test session
TEST_DB_FILE = tempfile.mktemp(suffix=".db")
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create database tables once for the entire test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    # Clean up test database file
    if os_module.path.exists(TEST_DB_FILE):
        os_module.remove(TEST_DB_FILE)


@pytest.fixture(autouse=True)
def clean_database():
    """Clean all data between tests."""
    yield
    # Delete all tasks after each test
    session = TestSessionLocal()
    try:
        session.query(TaskModel).delete()
        session.commit()
    finally:
        session.close()


@pytest.fixture
def db_session():
    """
    Provide a database session for tests.

    Usage in tests:
        def test_something(db_session):
            task = TaskModel(id="1", title="Test")
            db_session.add(task)
            db_session.commit()
    """
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    """
    Provide a test client for making API requests with test database.

    Usage in tests:
        def test_something(client):
            response = client.get("/tasks")
    """
    def override_get_db():
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()

    # Override BEFORE creating TestClient so lifespan sees it
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
