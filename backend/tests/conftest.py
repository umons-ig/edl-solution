"""
Test configuration for TaskFlow backend.
Sets up test fixtures for in-memory storage.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, tasks_db


@pytest.fixture(autouse=True)
def reset_database():
    """Reset in-memory storage before each test."""
    # Clear before test
    tasks_db.clear()
    yield
    # Clear after test
    tasks_db.clear()


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
