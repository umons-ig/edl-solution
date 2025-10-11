"""
Test configuration for TaskFlow backend.
Sets up test database and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from src.app import app
import os

# Set test MongoDB URL
TEST_MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
TEST_DATABASE_NAME = "taskflow_test"


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ["MONGODB_URL"] = TEST_MONGODB_URL
    os.environ["TEST_MODE"] = "true"
    yield
    # Cleanup
    if "TEST_MODE" in os.environ:
        del os.environ["TEST_MODE"]


@pytest.fixture(autouse=True)
def reset_database():
    """Reset test database before each test."""
    # Create MongoDB client for cleanup
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    db = client[TEST_DATABASE_NAME]

    # Clear database synchronously using run_sync helper
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Clean before test
    loop.run_until_complete(db.tasks.delete_many({}))

    yield

    # Clean after test
    loop.run_until_complete(db.tasks.delete_many({}))
    client.close()
    loop.close()


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        "title": "Implement user authentication",
        "description": "Add login and signup functionality",
        "status": "in_progress",
        "priority": "high",
        "assignee": "alice",
        "due_date": "2024-12-31T23:59:59"
    }


@pytest.fixture
def create_sample_task(client, sample_task_data):
    """Create a sample task and return the response."""
    response = client.post("/tasks", json=sample_task_data)
    return response
