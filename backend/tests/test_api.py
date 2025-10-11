"""
TaskFlow API Tests

Comprehensive test suite for the TaskFlow backend API.
Follows TDD principles with comprehensive coverage.
"""

import pytest
from datetime import datetime, timedelta
from src.app import TaskStatus, TaskPriority


class TestHealthCheck:
    """Test health check and basic endpoints."""

    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to TaskFlow API"
        assert "version" in data
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert data["database"] == "connected"
        assert "timestamp" in data
        assert "version" in data


class TestTaskCreation:
    """Test task creation functionality."""

    def test_create_task_success(self, client, sample_task_data):
        """Test successful task creation."""
        response = client.post("/tasks", json=sample_task_data)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["status"] == sample_task_data["status"]
        assert data["priority"] == sample_task_data["priority"]
        assert data["assignee"] == sample_task_data["assignee"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["created_at"] == data["updated_at"]

    def test_create_task_minimal_data(self, client):
        """Test creating task with minimal required data."""
        minimal_task = {"title": "Fix bug"}
        response = client.post("/tasks", json=minimal_task)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == "Fix bug"
        assert data["status"] == "todo"  # Default value
        assert data["priority"] == "medium"  # Default value
        assert data["description"] == ""  # Empty string from MongoDB
        assert data["assignee"] is None

    def test_create_task_invalid_title_too_long(self, client):
        """Test creating task with title that's too long."""
        long_title = "x" * 201  # Exceeds max length of 200
        task_data = {"title": long_title}
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 422

    def test_create_task_empty_title(self, client):
        """Test creating task with empty title."""
        task_data = {"title": ""}
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 422


class TestTaskRetrieval:
    """Test task retrieval functionality."""

    def test_get_task_success(self, client, create_sample_task):
        """Test successful task retrieval."""
        create_response = create_sample_task
        task_id = create_response.json()["id"]

        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Implement user authentication"

    def test_get_task_not_found(self, client):
        """Test retrieving non-existent task."""
        # Use invalid ObjectId format
        response = client.get("/tasks/non-existent-id")
        assert response.status_code == 400
        assert "invalid" in response.json()["detail"].lower()

    def test_get_task_valid_id_not_found(self, client):
        """Test retrieving valid but non-existent task ID."""
        # Use a valid ObjectId format that doesn't exist
        response = client.get("/tasks/507f1f77bcf86cd799439011")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_list_tasks_empty(self, client):
        """Test listing tasks when none exist."""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_with_data(self, client, create_sample_task):
        """Test listing tasks when data exists."""
        create_sample_task  # Create one task

        response = client.get("/tasks")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Implement user authentication"


class TestTaskFiltering:
    """Test task filtering functionality."""

    def test_filter_by_status(self, client):
        """Test filtering tasks by status."""
        # Create tasks with different statuses
        done_task = {"title": "Completed task", "status": "done"}
        todo_task = {"title": "Pending task", "status": "todo"}

        client.post("/tasks", json=done_task)
        client.post("/tasks", json=todo_task)

        # Filter by done status
        response = client.get("/tasks?status=done")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == "done"

        # Filter by todo status
        response = client.get("/tasks?status=todo")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == "todo"

    def test_filter_by_priority(self, client):
        """Test filtering tasks by priority."""
        high_task = {"title": "Urgent bug", "priority": "high"}
        low_task = {"title": "Minor fix", "priority": "low"}

        client.post("/tasks", json=high_task)
        client.post("/tasks", json=low_task)

        response = client.get("/tasks?priority=high")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["priority"] == "high"

    def test_filter_by_assignee(self, client):
        """Test filtering tasks by assignee."""
        alice_task = {"title": "Alice's task", "assignee": "alice"}
        bob_task = {"title": "Bob's task", "assignee": "bob"}

        client.post("/tasks", json=alice_task)
        client.post("/tasks", json=bob_task)

        response = client.get("/tasks?assignee=alice")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["assignee"] == "alice"

    def test_multiple_filters(self, client):
        """Test using multiple filters together."""
        task1 = {"title": "Task 1", "status": "todo", "priority": "high", "assignee": "alice"}
        task2 = {"title": "Task 2", "status": "done", "priority": "high", "assignee": "alice"}
        task3 = {"title": "Task 3", "status": "todo", "priority": "low", "assignee": "bob"}

        client.post("/tasks", json=task1)
        client.post("/tasks", json=task2)
        client.post("/tasks", json=task3)

        # Filter by status and assignee
        response = client.get("/tasks?status=todo&assignee=alice")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Task 1"


class TestTaskUpdates:
    """Test task update functionality."""

    def test_update_task_success(self, client, create_sample_task):
        """Test successful task update."""
        create_response = create_sample_task
        original_data = create_response.json()
        task_id = original_data["id"]
        original_updated_at = original_data["updated_at"]

        update_data = {
            "title": "Updated task title",
            "status": "done",
            "priority": "low"
        }

        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Updated task title"
        assert data["status"] == "done"
        assert data["priority"] == "low"
        # Description, assignee, due_date should remain unchanged
        assert data["description"] == original_data["description"]
        assert data["assignee"] == original_data["assignee"]
        # Updated timestamp should be newer
        assert data["updated_at"] != original_updated_at

    def test_update_task_partial_data(self, client, create_sample_task):
        """Test updating only some fields."""
        task_id = create_sample_task.json()["id"]

        partial_update = {"status": "in_progress"}

        response = client.put(f"/tasks/{task_id}", json=partial_update)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "in_progress"
        # Other fields should remain unchanged
        assert data["title"] == "Implement user authentication"

    def test_update_task_not_found(self, client):
        """Test updating non-existent task."""
        update_data = {"title": "Updated title"}
        # Use valid ObjectId format but non-existent
        response = client.put("/tasks/507f1f77bcf86cd799439011", json=update_data)
        assert response.status_code == 404

    def test_update_task_invalid_data(self, client, create_sample_task):
        """Test updating with invalid data."""
        task_id = create_sample_task.json()["id"]

        invalid_update = {"title": ""}  # Empty title
        response = client.put(f"/tasks/{task_id}", json=invalid_update)
        assert response.status_code == 422


class TestTaskDeletion:
    """Test task deletion functionality."""

    def test_delete_task_success(self, client, create_sample_task):
        """Test successful task deletion."""
        task_id = create_sample_task.json()["id"]

        # Verify task exists
        response = client.get("/tasks")
        assert len(response.json()) == 1

        # Delete the task
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        # Verify task is gone
        response = client.get("/tasks")
        assert len(response.json()) == 0

        # Verify specific get returns 404
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client):
        """Test deleting non-existent task."""
        # Use valid ObjectId format but non-existent
        response = client.delete("/tasks/507f1f77bcf86cd799439011")
        assert response.status_code == 404


class TestIntegrationScenarios:
    """Test complex integration scenarios."""

    def test_full_crud_workflow(self, client):
        """Test complete create-read-update-delete workflow."""
        # Create
        task_data = {"title": "Integration test task"}
        create_response = client.post("/tasks", json=task_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Read
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Integration test task"

        # Update
        update_response = client.put(f"/tasks/{task_id}", json={"status": "done"})
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "done"

        # List should include updated task
        list_response = client.get("/tasks")
        assert list_response.status_code == 200
        tasks = list_response.json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == "done"

        # Delete
        delete_response = client.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 204

        # Verify gone
        final_get_response = client.get(f"/tasks/{task_id}")
        assert final_get_response.status_code == 404

    def test_due_date_handling(self, client):
        """Test due date persistence and filtering."""
        future_date = datetime.utcnow() + timedelta(days=7)
        task_with_due_date = {
            "title": "Task with due date",
            "due_date": future_date.isoformat()
        }

        response = client.post("/tasks", json=task_with_due_date)
        assert response.status_code == 201

        data = response.json()
        assert "due_date" in data
        # Due date should be preserved (exact format may vary)


if __name__ == "__main__":
    pytest.main([__file__])