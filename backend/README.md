# TaskFlow Backend

FastAPI backend service with PostgreSQL database integration.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [UV package manager](https://docs.astral.sh/uv/)
- PostgreSQL (optional for local development)

### Installation

```bash
# Install dependencies
uv sync

# Copy environment variables
cp .env.example .env
```

### Running Locally

#### Option 1: With SQLite (Easiest)

```bash
# Start the server (uses SQLite by default)
uv run uvicorn src.app:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

#### Option 2: With PostgreSQL (Production-like)

1. **Start PostgreSQL with Docker:**

```bash
docker run --name taskflow-postgres \
  -e POSTGRES_DB=taskflow_dev \
  -e POSTGRES_USER=taskflow \
  -e POSTGRES_PASSWORD=dev_password \
  -p 5432:5432 \
  -d postgres:15
```

2. **Update .env:**

```bash
DATABASE_URL=postgresql://taskflow:dev_password@localhost:5432/taskflow_dev
```

3. **Start the server:**

```bash
uv run uvicorn src.app:app --reload
```

### Database Management

#### Initialize Database

The database is automatically initialized on application startup. To manually initialize:

```bash
uv run python src/db_init.py
```

#### Reset Database (Development Only)

⚠️ **Warning**: This will delete all data!

```bash
uv run python src/db_init.py --reset
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_api.py -v

# Run with verbose output
uv run pytest -vv
```

Tests use an in-memory SQLite database, so no PostgreSQL setup is needed.

## 📁 Project Structure

```
backend/
├── src/
│   ├── app.py           # FastAPI application & endpoints
│   ├── database.py      # Database configuration & session
│   ├── models.py        # SQLAlchemy ORM models
│   ├── db_init.py       # Database initialization scripts
│   └── __init__.py
├── tests/
│   ├── conftest.py      # Pytest fixtures & configuration
│   ├── test_api.py      # API endpoint tests
│   └── __init__.py
├── pyproject.toml       # Dependencies & configuration
├── .env.example         # Environment variables template
├── .gitignore
└── README.md
```

## 🗄️ Database

### Schema

**Table: tasks**

| Column | Type | Constraints |
|--------|------|-------------|
| id | String | PRIMARY KEY |
| title | String(200) | NOT NULL |
| description | String(1000) | NULL |
| status | Enum | NOT NULL, DEFAULT 'todo' |
| priority | Enum | NOT NULL, DEFAULT 'medium' |
| assignee | String(100) | NULL |
| due_date | DateTime | NULL |
| created_at | DateTime | NOT NULL, DEFAULT now() |
| updated_at | DateTime | NOT NULL, ON UPDATE now() |

### Enums

**TaskStatus**: `todo`, `in_progress`, `done`
**TaskPriority**: `low`, `medium`, `high`

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Environment
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./taskflow.db

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Debug
DEBUG=true
LOG_LEVEL=INFO
```

### Render Production Variables

In Render dashboard, set:

```bash
ENVIRONMENT=production
DATABASE_URL=<provided-by-render>
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com
DEBUG=false
```

## 📚 API Endpoints

### Health Check

```bash
GET /health
```

### Tasks

```bash
# List all tasks
GET /tasks
GET /tasks?status=todo
GET /tasks?priority=high&assignee=john

# Create task
POST /tasks
Content-Type: application/json
{
  "title": "New task",
  "description": "Task description",
  "status": "todo",
  "priority": "medium"
}

# Get task
GET /tasks/{task_id}

# Update task
PUT /tasks/{task_id}
Content-Type: application/json
{
  "status": "in_progress",
  "assignee": "alice"
}

# Delete task
DELETE /tasks/{task_id}
```

## 🧪 Testing

### Test Configuration

Tests use:
- **In-memory SQLite** database
- **Fresh database** for each test
- **Dependency injection** override for test DB

### Writing Tests

```python
def test_create_task(client):
    """Test creating a task."""
    response = client.post("/tasks", json={
        "title": "Test task",
        "status": "todo",
        "priority": "high"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
```

### Database Fixtures

```python
def test_with_database(db_session):
    """Test using database directly."""
    task = TaskModel(id="1", title="Test")
    db_session.add(task)
    db_session.commit()

    result = db_session.query(TaskModel).first()
    assert result.title == "Test"
```

## 🚀 Deployment

### Render Configuration

**Build Command:**
```bash
pip install uv && uv sync
```

**Start Command:**
```bash
uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT
```

### Database Setup on Render

1. Create PostgreSQL database on Render
2. Add `DATABASE_URL` environment variable to web service
3. Deploy - tables are created automatically on startup

## 🔍 Debugging

### Check Database Connection

```bash
curl http://localhost:8000/health
```

Should return `"database": "connected"`.

### Access PostgreSQL

```bash
# Via Docker
docker exec -it taskflow-postgres psql -U taskflow -d taskflow_dev

# Via Render (get command from dashboard)
PGPASSWORD=<password> psql -h <host> -U <user> <database>
```

### SQL Queries

```sql
-- List all tasks
SELECT * FROM tasks;

-- Count tasks by status
SELECT status, COUNT(*) FROM tasks GROUP BY status;

-- Show table schema
\d tasks
```

## 📝 Common Commands

```bash
# Development
uv run uvicorn src.app:app --reload        # Start dev server
uv run pytest -v                           # Run tests
uv run pytest --cov=src                    # Test with coverage

# Database
uv run python src/db_init.py               # Initialize DB
uv run python src/db_init.py --reset       # Reset DB

# Dependencies
uv add <package>                           # Add dependency
uv sync                                    # Install dependencies
uv lock                                    # Update lock file
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sqlalchemy'"

**Solution:**
```bash
uv sync
```

### Issue: "Relation 'tasks' does not exist"

**Solution:** Tables not created. Restart the app or run:
```bash
uv run python src/db_init.py
```

### Issue: "Connection refused" to PostgreSQL

**Solution:** Check that PostgreSQL is running:
```bash
docker ps  # Should show taskflow-postgres
```

### Issue: Tests fail with database errors

**Solution:** Tests use in-memory DB. Check `conftest.py` fixtures are correct.

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📄 License

Educational material for workshops.

---

**Version 2.2.0** - With PostgreSQL Integration 🚀
