import pytest

# =============================================================================
# BASIC ENDPOINT TESTS
# =============================================================================

def test_root_endpoint(client):
    """The root endpoint should return a welcome message."""
    response = client.get("/")

    assert response.status_code == 200
    assert "Welcome to TaskFlow API" in response.json()["message"]


def test_health_check(client):
    """The health endpoint should confirm the API is running."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# =============================================================================
# CREATE TASK TESTS
# =============================================================================

def test_create_simple_task(client):
    """Creating a task with just a title should work."""
    response = client.post("/tasks", json={"title": "Buy groceries"})

    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Buy groceries"
    assert task["status"] == "todo"  # Default status
    assert "id" in task


def test_create_complete_task(client):
    """Creating a task with all fields should preserve all data."""
    task_data = {
        "title": "Fix authentication bug",
        "description": "Users can't log in with special characters",
        "status": "in_progress",
        "priority": "high",
        "assignee": "alice"
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Fix authentication bug"
    assert task["description"] == "Users can't log in with special characters"
    assert task["status"] == "in_progress"
    assert task["priority"] == "high"
    assert task["assignee"] == "alice"


def test_create_task_without_title(client):
    """Creating a task without a title should fail."""
    response = client.post("/tasks", json={"description": "No title here"})

    assert response.status_code == 422  # Validation error


def test_create_task_with_empty_title(client):
    """Creating a task with an empty title should fail."""
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422


# =============================================================================
# READ TASK TESTS
# =============================================================================

def test_list_tasks_when_empty(client):
    """Listing tasks when there are none should return empty list."""
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_with_data(client):
    """Listing tasks should return all created tasks."""
    # Create two tasks
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_specific_task(client):
    """Getting a task by ID should return that task."""
    # Create a task
    create_response = client.post("/tasks", json={"title": "Find me"})
    task_id = create_response.json()["id"]

    # Get the task
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_get_nonexistent_task(client):
    """Getting a task that doesn't exist should return 404."""
    response = client.get("/tasks/999")  # Use integer ID

    assert response.status_code == 404


# =============================================================================
# FILTER TASKS TESTS
# =============================================================================

def test_filter_by_status(client):
    """Filtering tasks by status should only return matching tasks."""
    # Create tasks with different statuses
    client.post("/tasks", json={"title": "Todo task", "status": "todo"})
    client.post("/tasks", json={"title": "Done task", "status": "done"})

    # Filter for done tasks
    response = client.get("/tasks?status=done")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Done task"


def test_filter_by_priority(client):
    """Filtering tasks by priority should only return matching tasks."""
    client.post("/tasks", json={"title": "Urgent", "priority": "high"})
    client.post("/tasks", json={"title": "Not urgent", "priority": "low"})

    response = client.get("/tasks?priority=high")

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Urgent"


def test_filter_by_assignee(client):
    """Filtering tasks by assignee should only return their tasks."""
    client.post("/tasks", json={"title": "Alice task", "assignee": "alice"})
    client.post("/tasks", json={"title": "Bob task", "assignee": "bob"})

    response = client.get("/tasks?assignee=alice")

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["assignee"] == "alice"


# =============================================================================
# UPDATE TASK TESTS
# =============================================================================

def test_update_task(client):
    """Updating a task should change its fields."""
    # Create a task
    create_response = client.post("/tasks", json={"title": "Original"})
    task_id = create_response.json()["id"]

    # Update it
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated"})

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_task_status(client):
    """Updating task status should work."""
    create_response = client.post("/tasks", json={"title": "Work in progress"})
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"status": "done"})

    assert response.json()["status"] == "done"


def test_update_nonexistent_task(client):
    """Updating a task that doesn't exist should return 404."""
    response = client.put("/tasks/999", json={"title": "Won't work"})  # Use integer ID

    assert response.status_code == 404


# =============================================================================
# DELETE TASK TESTS
# =============================================================================

def test_delete_task(client):
    """Deleting a task should remove it."""
    # Create a task
    create_response = client.post("/tasks", json={"title": "Delete me"})
    task_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task(client):
    """Deleting a task that doesn't exist should return 404."""
    response = client.delete("/tasks/999")  # Use integer ID

    assert response.status_code == 404


# =============================================================================
# COMPLETE WORKFLOW TEST
# =============================================================================

def test_complete_task_lifecycle(client):
    """Test creating, reading, updating, and deleting a task."""
    # 1. Create a task
    create_response = client.post("/tasks", json={
        "title": "Complete workflow test",
        "status": "todo"
    })
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # 2. Read the task
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Complete workflow test"

    # 3. Update the task
    update_response = client.put(f"/tasks/{task_id}", json={"status": "done"})
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "done"

    # 4. Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # 5. Verify it's deleted
    final_get = client.get(f"/tasks/{task_id}")
    assert final_get.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
