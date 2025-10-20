"""
Test Configuration for TaskFlow - Workshop Version

This file sets up the test environment for pytest.
Fixtures are reusable test components.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, tasks_storage


@pytest.fixture(autouse=True)
def reset_storage():
    """
    Clean the task storage before and after each test.

    This ensures each test starts with a fresh, empty list.
    The 'autouse=True' means this runs automatically for every test.
    """
    tasks_storage.clear()  # Clean before test
    yield                  # Run the test
    tasks_storage.clear()  # Clean after test


@pytest.fixture
def client():
    """
    Provide a test client for making API requests.

    Usage in tests:
        def test_something(client):
            response = client.get("/tasks")
    """
    with TestClient(app) as test_client:
        yield test_client
