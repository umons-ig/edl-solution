# Workshop 1: TaskFlow Backend & TDD Fundamentals

**Duration**: 4 hours
**Branch**: `main` (students start here)
**Level**: Beginner to Intermediate

## 🎯 Objectives

By the end of this workshop, you will be able to:
- Implement **Test-Driven Development (TDD)** in a real project
- Build a RESTful API with **FastAPI** and **Python**
- Use **UV** for modern Python package management
- Write comprehensive unit tests with **pytest**
- Follow the **Red-Green-Refactor** development cycle
- Understand **API design patterns** and error handling
- Use **GitHub Actions** for automated testing

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ **Python 3.11+** installed
- ✅ **Git** installed and configured
- ✅ **GitHub account**
- ✅ Basic Python knowledge
- ✅ Understanding of web APIs (REST concepts)

### Verification Commands
```bash
# Check Python version
python --version

# Check Git configuration
git config --list --local
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/taskflow-workshops.git
cd taskflow-workshops
```

### 2. Navigate to Backend
```bash
cd backend
```

### 3. Install Dependencies with UV
```bash
# Install dependencies
uv sync

# Verify installation
uv run python --version
uv run pytest --version
```

## 📚 Workshop Structure

This workshop follows a **guided TDD approach**. Each section:
1. **Starts with failing tests** (Red)
2. **Implements minimal code** (Green)
3. **Refactors for quality** (Refactor)

### TDD Cycle Reminder
```
🔴 RED    → Write failing test
🟢 GREEN → Make it pass with minimal code
🔵 REFACTOR → Improve code quality
```

---

## 🎭 Part 1: Project Setup & First Test (30 min)

### 1A: Create Your First Test

**TDD starts with tests!** Even before writing any implementation code.

#### Step 1: Understand the Test Structure
Your project already has a `tests/` directory. Let's examine the existing test file:

```bash
# Check the directory structure
ls -la
# You should see: src/ tests/ pyproject.toml

# Look at the test file
head -20 tests/test_api.py
```

#### Step 2: Write Your First Failing Test

**Concept**: In TDD, we write tests for behavior BEFORE implementing the code.

**Goal**: Create a test for the root endpoint that returns API information.

**Instructions:**
1. Open `tests/test_api.py`
2. Add this test at the end of `TestHealthCheck` class:

```python
def test_root_endpoint(self, client):
    """Test that root endpoint returns welcome message."""
    # This is our RED phase - test will fail because endpoint doesn't exist
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "TaskFlow" in data["message"]
    assert "version" in data
```

#### Step 3: Run the Test (Should Fail)
```bash
uv run pytest tests/test_api.py::TestHealthCheck::test_root_endpoint -v
```

**Expected Result**: ❌ The test fails because no API endpoint exists yet.

---

## 🏗️ Part 2: FastAPI Application Foundation (40 min)

### 2A: Create Your First FastAPI App

**Goal**: Implement the minimal code to make the test pass.

#### Step 1: Create the App Structure
Check the existing `src/app.py` - it might have some starter code or be empty.

#### Step 2: Implement Basic FastAPI App
```python
# Add this to src/app.py
from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow API",
    description="Task management API built with FastAPI",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TaskFlow API",
        "version": "0.1.0",
        "status": "healthy"
    }
```

#### Step 3: Update Test Fixtures
You may need to add pytest fixtures at the top of `tests/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    return TestClient(app)
```

**Important**: Make sure your test methods use the `client` fixture parameter.

#### Step 4: Run the Test
```bash
uv run pytest tests/test_api.py::TestHealthCheck::test_root_endpoint -v
```

**Expected Result**: ✅ Test passes!

### 2B: Understand What Just Happened

**Key Concepts Learned:**
- **FastAPI**: Modern, fast Python web framework
- **TestClient**: Simulates HTTP requests without a server
- **API Endpoint**: Defines routes and response formats
- **TDD Flow**: Red (failing test) → Green (minimal working code)

---

## 📝 Part 3: Task Data Models & Pydantic (50 min)

### 3A: Define Task Data Structure

**Concept**: Modern APIs use **data validation** and **type safety**.

**Tools**: **Pydantic** provides automatic validation and serialization.

#### Step 1: Add Task Models
```python
# Add to src/app.py (at the top)
from typing import Optional
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime
```

#### Step 2: Write Tests for Data Models
Add these tests to verify your models work:

```python
class TestDataModels:
    """Test Pydantic data models."""

    def test_task_create_with_minimal_data(self):
        """Test creating task with only required fields."""
        task_data = TaskCreate(title="Test task")
        assert task_data.title == "Test task"
        assert task_data.status == "todo"  # Default value
        assert task_data.priority == "medium"  # Default value

    def test_task_create_validation(self):
        """Test that validation works."""
        # Empty title should fail
        with pytest.raises(ValueError):
            TaskCreate(title="")

    def test_task_status_enum(self):
        """Test enum values."""
        task = TaskCreate(title="Test", status="in_progress")
        assert task.status == TaskStatus.IN_PROGRESS
```

### 3B: Add In-Memory Storage

**Concept**: For now we'll use in-memory storage. Later workshops use databases.

```python
# Add after models in src/app.py
tasks_db: List[Task] = []
```

---

## 🎯 Part 4: CRUD Operations - The Core API (90 min)

### 4A: Create Task Endpoint

**TDD Approach**: Write test first, then implement.

#### Step 1: Write Test for Task Creation
```python
class TestTaskCreation:
    """Test task creation functionality."""

    def test_create_task_success(self, client):
        """Test successful task creation."""
        task_data = {
            "title": "Implement user authentication",
            "description": "Add login and signup functionality",
            "status": "in_progress",
            "priority": "high",
            "assignee": "alice"
        }

        response = client.post("/tasks", json=task_data)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == task_data["title"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_minimal(self, client):
        """Test creating with minimal data."""
        response = client.post("/tasks", json={"title": "Simple task"})
        assert response.status_code == 201

        data = response.json()
        assert data["status"] == "todo"  # Default
        assert data["priority"] == "medium"  # Default
```

#### Step 2: Implement Create Endpoint
```python
# Add to src/app.py
from uuid import uuid4

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate):
    """Create a new task."""
    now = datetime.utcnow()

    task = Task(
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
        **task_data.dict()
    )

    tasks_db.append(task)
    return task
```

#### Step 3: Test and Verify
```bash
uv run pytest tests/test_api.py::TestTaskCreation -v
```

### 4B: Read Tasks Endpoints

**Concepts**: List endpoint with filtering, individual task retrieval.

#### Step 1: Write Tests for Reading Tasks
```python
class TestTaskRetrieval:
    """Test task retrieval functionality."""

    def test_get_task_by_id(self, client):
        """Test getting a specific task."""
        # Create a task first
        create_response = client.post("/tasks", json={"title": "Test task"})
        task_id = create_response.json()["id"]

        # Now get it
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test task"

    def test_get_nonexistent_task(self, client):
        """Test getting a task that doesn't exist."""
        response = client.get("/tasks/nonexistent-id")
        assert response.status_code == 404

    def test_list_all_tasks(self, client):
        """Test listing all tasks."""
        # Create a couple tasks
        client.post("/tasks", json={"title": "Task 1"})
        client.post("/tasks", json={"title": "Task 2"})

        response = client.get("/tasks")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) >= 2  # At least our tasks
```

#### Step 2: Implement Read Endpoints
```python
# Add to src/app.py
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task by ID."""
    for task in tasks_db:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")

@app.get("/tasks", response_model=List[Task])
async def list_tasks():
    """List all tasks."""
    return tasks_db
```

#### Step 3: Test and Verify
```bash
uv run pytest tests/test_api.py::TestTaskRetrieval -v
```

### 4C: Update Task Endpoint

**Concepts**: Partial updates, validation, error handling.

#### Step 1: Write Update Test
```python
class TestTaskUpdates:
    """Test task update functionality."""

    def test_update_task_status(self, client):
        """Test updating task status."""
        # Create task
        create_response = client.post("/tasks", json={"title": "Original task"})
        task_id = create_response.json()["id"]

        # Update status
        update_data = {"status": "in_progress"}
        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "in_progress"
        assert data["title"] == "Original task"  # Unchanged

    def test_update_nonexistent_task(self, client):
        """Test updating task that doesn't exist."""
        update_data = {"title": "Updated"}
        response = client.put("/tasks/nonexistent-id", json=update_data)
        assert response.status_code == 404
```

#### Step 2: Implement Update Endpoint
```python
# Add HTTPException import
from fastapi import FastAPI, HTTPException

# Add this endpoint
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update_data: TaskUpdate):
    """Update an existing task."""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            # Get updated data
            update_dict = update_data.dict(exclude_unset=True)
            updated_task_data = task.dict()
            updated_task_data.update(update_dict)

            # Update timestamp and create new task
            updated_task_data["updated_at"] = datetime.utcnow()
            updated_task = Task(**updated_task_data)

            tasks_db[i] = updated_task
            return updated_task

    raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")
```

### 4D: Delete Task Endpoint

**Concepts**: HTTP DELETE method, resource removal.

#### Step 1: Write Delete Test
```python
class TestTaskDeletion:
    """Test task deletion functionality."""

    def test_delete_task(self, client):
        """Test successful task deletion."""
        # Create task
        create_response = client.post("/tasks", json={"title": "Task to delete"})
        task_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204  # No content

        # Verify it's gone
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404
```

#### Step 2: Implement Delete Endpoint
```python
@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete a task by ID."""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return

    raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")
```

---

## 🔍 Part 5: Advanced Features (60 min)

### 5A: Query Parameters & Filtering

**Concept**: REST APIs often support filtering via query parameters.

#### Step 1: Update List Endpoint
```python
@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
):
    """List all tasks with optional filtering."""
    tasks = tasks_db.copy()

    # Apply filters
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if assignee:
        tasks = [t for t in tasks if t.assignee == assignee]

    return tasks
```

#### Step 2: Test Filtering
```python
class TestTaskFiltering:
    """Test task filtering functionality."""

    def test_filter_by_status(self, client):
        """Test filtering by status."""
        client.post("/tasks", json={"title": "Done task", "status": "done"})
        client.post("/tasks", json={"title": "Todo task", "status": "todo"})

        response = client.get("/tasks?status=done")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == "done"

    def test_filter_by_assignee(self, client):
        """Test filtering by assignee."""
        client.post("/tasks", json={"title": "Alice's task", "assignee": "alice"})
        client.post("/tasks", json={"title": "Bob's task", "assignee": "bob"})

        response = client.get("/tasks?assignee=alice")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["assignee"] == "alice"
```

### 5B: Error Handling & Validation

**Concept**: Good APIs provide helpful error messages and proper status codes.

#### Step 1: Test Validation
```python
def test_create_task_invalid_title(self, client):
    """Test creating task with invalid title."""
    # Too long
    response = client.post("/tasks", json={"title": "x" * 201})
    assert response.status_code == 422

    # Empty
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422
```

#### Step 2: Add TaskUpdate Model
```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
```

---

## 🚀 Part 6: GitHub Actions CI/CD (40 min)

### 6A: Understanding CI/CD

**Concept**: **Continuous Integration/Continuous Deployment**
- Automatically test code on every push
- Prevents bugs from reaching production
- Ensures code quality standards

### 6B: Create GitHub Actions Workflow

#### Step 1: Create the Workflow File
```bash
# Create directory
mkdir -p .github/workflows

# Create workflow file
touch .github/workflows/test.yml
```

#### Step 2: Add CI/CD Configuration
```yaml
# .github/workflows/test.yml
name: TaskFlow Backend Tests

on:
  push:
    branches: [ main, workshop-1 ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Install UV
      uses: astral-sh/setup-uv@v3
      with:
        version: "latest"

    - name: Set up Python
      run: uv python install 3.11

    - name: Install dependencies
      run: |
        cd backend
        uv sync --dev

    - name: Run tests with coverage
      run: |
        cd backend
        uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95

    - name: Upload coverage reports
      uses: codecov/codecov-action@v4
      with:
        file: ./backend/coverage.xml
```

#### Step 3: Test Locally First
```bash
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95
```

#### Step 4: Commit and Push
```bash
git add .
git commit -m "Add Workshop 1 backend implementation and CI/CD"
git push origin main
```

#### Step 5: Check GitHub Actions
Visit your repository's Actions tab to see tests running automatically.

---

## ✅ Part 7: Workshop Verification (20 min)

### Interactive API Testing

Test your complete API:

```bash
# Start the server
uv run uvicorn src.app:app --reload

# In another terminal, test endpoints:

# Get API info
curl http://localhost:8000/

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My first task", "description": "Learning TDD!"}'

# List all tasks
curl http://localhost:8000/tasks

# Filter tasks
curl "http://localhost:8000/tasks?status=todo"
```

### Complete Test Suite
```bash
uv run pytest -v --cov=src --cov-report=html
# Look at htmlcov/index.html for detailed coverage report
```

---

## 🎉 Workshop 1 Complete!

### What You Built:
- ✅ **Complete REST API** with CRUD operations
- ✅ **Comprehensive test suite** (20+ tests)
- ✅ **Filtering and validation**
- ✅ **Proper error handling**
- ✅ **CI/CD pipeline** with automated testing
- ✅ **Modern Python practices** (FastAPI, UV, pytest)

### TDD Concepts Mastered:
- 🔴 **Red**: Writing failing tests first
- 🟢 **Green**: Minimal code to pass tests
- 🔵 **Refactor**: Improving code quality
- 🔄 **Cycle**: Repeating the process

### Next Steps:
**Workshop 2: React Frontend** - Build the user interface that consumes your API!

### Resources:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [UV Package Manager](https://docs.astral.sh/uv/)

---

## 📋 Assessment Criteria

- [ ] API responds on all endpoints
- [ ] All tests pass (95%+ coverage)
- [ ] Error handling implemented
- [ ] TDD approach followed
- [ ] GitHub Actions workflow runs successfully
- [ ] Code is well-documented and clean

---

**Questions?** Ask your instructor or refer to the [troubleshooting guide](../docs/troubleshooting.md).