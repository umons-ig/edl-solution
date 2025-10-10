# Workshop 3: Production Deployment & Cloud CI/CD

**Duration**: 3 hours
**Branch**: Based on workshops 1 & 2 completion
**Level**: Intermediate to Advanced
**Prerequisites**: Workshops 1 & 2 (full-stack application) completed

## 🎯 Objectives

By the end of this workshop, you will be able to:

- Add **database persistence** with MongoDB Atlas (cloud database)
- Set up **production CI/CD pipelines** with GitHub Actions
- **Deploy to production** using Render cloud platform
- Configure **environment-based settings** for dev/staging/prod
- Implement **health checks and monitoring** patterns
- Understand **secrets management** and production best practices

## 📋 Prerequisites

### Completed Previous Workshops

- ✅ Workshop 1: Backend API with FastAPI and comprehensive tests
- ✅ Workshop 2: Frontend React application with API integration
- ✅ GitHub repository with existing CI/CD workflows
- ✅ Full-stack application running locally

### Additional Requirements

- ✅ **GitHub account** with repository access
- ✅ **MongoDB Atlas account** (free tier) - https://www.mongodb.com/cloud/atlas/register
- ✅ **Render account** (free tier with 750 hours)
- ✅ Understanding of environment variables and secrets management

## 🚀 Getting Started

### Workshop Evolution

This workshop builds upon the foundation from Workshops 1 & 2:

```mermaid
graph LR
    A[Workshop 1<br/>FastAPI Backend<br/>In-Memory Storage] --> B[Workshop 2<br/>React Frontend<br/>Full Integration]
    B --> C[Workshop 3<br/>Database + Cloud<br/>Production Ready]

    style A fill:#e1f5ff
    style B fill:#b3e5fc
    style C fill:#4fc3f7
```

### Current vs Target Architecture

```mermaid
graph TB
    subgraph "After Workshop 2"
        A1[React App<br/>localhost:5173]
        A2[FastAPI Backend<br/>localhost:8000<br/>In-Memory Storage]
        A1 -->|HTTP| A2
    end

    subgraph "After Workshop 3"
        B1[React App<br/>Cloud Deployed]
        B2[FastAPI Backend<br/>Cloud Deployed]
        B3[(MongoDB Atlas<br/>Cloud Database)]
        B4[GitHub Actions<br/>CI/CD Pipeline]

        B1 -->|HTTPS| B2
        B2 -->|MongoDB Protocol| B3
        B4 -->|Auto Deploy| B1
        B4 -->|Auto Deploy| B2
    end

    style B3 fill:#4caf50
    style B4 fill:#ff9800
```

## 📚 Workshop Structure

### Part 1: Database Integration with MongoDB Atlas (50 min)

- MongoDB Atlas setup (cloud database, no local installation!)
- Motor (async MongoDB driver) integration
- Update API endpoints to use database
- Test database integration

### Part 2: Cloud Deployment Setup (40 min)

- Environment variable configuration
- Health check endpoints
- Deploy to Render
- Test production deployment

### Part 3: Production CI/CD (60 min)

- GitHub Actions workflow for automated testing
- Automated deployment on push to main
- Environment secrets management
- Branch-based deployment strategies

### Part 4: Production Configuration (20 min)

- CORS configuration for production
- Logging and monitoring setup
- Error handling improvements

### Part 5: Verification & Testing (10 min)

- Test the live application
- Monitor logs and health checks
- Celebrate! 🎉

---

## 🗄️ Part 1: Database Integration with MongoDB Atlas (50 min)

### 1A: MongoDB Atlas Setup

**Concept**: Moving from in-memory storage to a cloud-hosted MongoDB database. No local database installation required!

#### Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Create a new **M0 Free Cluster** (512MB storage, perfect for learning!)
   - Choose a cloud provider (AWS/GCP/Azure)
   - Select a region close to you
   - Name your cluster: `taskflow-cluster`

#### Step 2: Configure Database Access

1. **Create Database User**:
   - Go to "Database Access" → "Add New Database User"
   - Authentication Method: Password
   - Username: `taskflow_user`
   - Password: Generate a secure password (save it!)
   - Database User Privileges: **Read and write to any database**

2. **Configure Network Access**:
   - Go to "Network Access" → "Add IP Address"
   - For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
   - ⚠️ **Note**: In real production, you'd whitelist specific IPs

#### Step 3: Get Connection String

1. Go to "Database" → Click "Connect" on your cluster
2. Choose "Connect your application"
3. Driver: **Python**, Version: **3.12 or later**
4. Copy the connection string, it looks like:
   ```
   mongodb+srv://taskflow_user:<password>@taskflow-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. **Replace `<password>`** with your actual database user password

#### Step 4: Create Database and Collection

MongoDB will create these automatically when you first write data, but let's verify:

1. Go to "Database" → "Browse Collections"
2. Click "Add My Own Data"
3. Database name: `taskflow_db`
4. Collection name: `tasks`

### 1B: Install MongoDB Driver

```bash
cd backend

# Add Motor (async MongoDB driver for FastAPI)
uv add motor pymongo
```

### 1C: Create Database Configuration

Create `backend/src/database.py`:

```python
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB configuration
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://localhost:27017"  # Fallback for local dev (though we use Atlas)
)

# Global MongoDB client
mongodb_client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo():
    """
    Connect to MongoDB Atlas.
    Called on application startup.
    """
    global mongodb_client
    mongodb_client = AsyncIOMotorClient(MONGODB_URL)

    # Verify connection
    try:
        await mongodb_client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection.
    Called on application shutdown.
    """
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("✅ MongoDB connection closed")


def get_database():
    """
    Get the database instance.
    Returns the 'taskflow_db' database.
    """
    return mongodb_client.taskflow_db


def get_tasks_collection():
    """
    Get the tasks collection.
    This is where we store all task documents.
    """
    db = get_database()
    return db.tasks
```

### 1D: Update Models for MongoDB

MongoDB uses `_id` as the primary key. Let's create helper functions in `backend/src/models.py`:

```python
from typing import Optional
from datetime import datetime
from bson import ObjectId


def task_helper(task) -> dict:
    """
    Helper to convert MongoDB document to Task dict.
    MongoDB stores documents with _id (ObjectId), we convert to id (string).
    """
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description", ""),
        "status": task["status"],
        "priority": task["priority"],
        "assignee": task.get("assignee"),
        "due_date": task.get("due_date"),
        "created_at": task.get("created_at"),
        "updated_at": task.get("updated_at"),
    }


def task_to_db(task_data: dict) -> dict:
    """
    Prepare task data for MongoDB insertion.
    Adds timestamps and removes None values.
    """
    now = datetime.utcnow()

    db_task = {
        "title": task_data["title"],
        "description": task_data.get("description", ""),
        "status": task_data.get("status", "todo"),
        "priority": task_data.get("priority", "medium"),
        "assignee": task_data.get("assignee"),
        "due_date": task_data.get("due_date"),
        "created_at": task_data.get("created_at", now),
        "updated_at": now,
    }

    # Remove None values
    return {k: v for k, v in db_task.items() if v is not None}
```

### 1E: Update API to Use MongoDB

Update `backend/src/app.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from src.database import (
    connect_to_mongo,
    close_mongo_connection,
    get_tasks_collection
)
from src.models import task_helper, task_to_db

# Import your existing Pydantic models
from src.app import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority

app = FastAPI(
    title="TaskFlow API",
    description="Production-ready task management API with MongoDB",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup/Shutdown events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check database connection
        collection = get_tasks_collection()
        await collection.database.command('ping')

        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )


# CRUD Operations with MongoDB

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate):
    """Create a new task in MongoDB."""
    collection = get_tasks_collection()

    # Prepare task for database
    db_task = task_to_db(task_data.dict())

    # Insert into MongoDB
    result = await collection.insert_one(db_task)

    # Retrieve the created task
    created_task = await collection.find_one({"_id": result.inserted_id})

    return task_helper(created_task)


@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None
):
    """List all tasks with optional filtering."""
    collection = get_tasks_collection()

    # Build query filter
    query = {}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    if assignee:
        query["assignee"] = assignee

    # Query MongoDB
    tasks = []
    async for task in collection.find(query):
        tasks.append(task_helper(task))

    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task by ID."""
    collection = get_tasks_collection()

    # Validate ObjectId
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    # Find task
    task = await collection.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found"
        )

    return task_helper(task)


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update_data: TaskUpdate):
    """Update an existing task."""
    collection = get_tasks_collection()

    # Validate ObjectId
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    # Prepare update data
    update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()

    # Update in MongoDB
    result = await collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found"
        )

    # Return updated task
    updated_task = await collection.find_one({"_id": ObjectId(task_id)})
    return task_helper(updated_task)


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete a task by ID."""
    collection = get_tasks_collection()

    # Validate ObjectId
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    # Delete from MongoDB
    result = await collection.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found"
        )


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Welcome to TaskFlow API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }
```

### 1F: Configure Environment Variables

Create `backend/.env`:

```bash
# MongoDB Atlas connection string
MONGODB_URL=mongodb+srv://taskflow_user:<password>@taskflow-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority

# Replace <password> with your actual MongoDB Atlas password
```

Add `.env` to `.gitignore`:

```bash
# In your .gitignore file
.env
.env.*
!.env.example
```

Create `backend/.env.example` (safe to commit):

```bash
# MongoDB Atlas connection string
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

### 1G: Test Database Integration

```bash
# Start the backend
cd backend
uv run uvicorn src.app:app --reload

# Test creating a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MongoDB test task",
    "description": "Testing MongoDB Atlas integration",
    "status": "todo",
    "priority": "high"
  }'

# List all tasks
curl http://localhost:8000/tasks

# Check health endpoint
curl http://localhost:8000/health
```

Verify in MongoDB Atlas:

1. Go to your MongoDB Atlas dashboard
2. Click "Browse Collections"
3. Navigate to `taskflow_db` → `tasks`
4. You should see your tasks stored as documents!

---

## ☁️ Part 2: Cloud Deployment (40 min)

### 2A: Deployment Options

We'll use **Render** - a beginner-friendly platform that **auto-detects** your app:

| Feature | Render | Railway (Alternative) |
|---------|--------|----------------------|
| **Free Tier** | ✅ 750 hours/month | ✅ $5 credit/month |
| **Auto-detection** | ✅ Detects FastAPI/React | ✅ Detects FastAPI/React |
| **Database** | MongoDB Atlas (our choice) | PostgreSQL/MongoDB |
| **Custom Domain** | ✅ | ✅ |
| **Documentation** | ✅ Extensive | ✅ Good |

Render automatically detects your FastAPI + React stack and deploys without needing Docker!

### 2B: Deploy to Render

#### Backend Deployment

1. **Sign up** at [render.com](https://render.com)

2. **Connect GitHub Repository**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Grant Render access

3. **Configure Backend Service**:
   ```
   Name: taskflow-backend
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install uv && uv sync
   Start Command: uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**:
   - Go to "Environment" tab
   - Add: `MONGODB_URL` = (your MongoDB Atlas connection string)
   - Add: `PORT` = 8000

5. **Deploy**: Click "Create Web Service"

#### Frontend Deployment

1. **Create New Static Site**:
   - Click "New +" → "Static Site"
   - Select your repository

2. **Configure Frontend**:
   ```
   Name: taskflow-frontend
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

3. **Add Environment Variables**:
   - `VITE_API_URL` = (your backend URL from step above)

4. **Deploy**: Click "Create Static Site"

### 2C: Alternative - Railway

If you prefer Railway over Render, you can use these commands:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# For each service (backend/frontend):
cd backend  # or cd frontend
railway init
railway variables set MONGODB_URL="your-connection-string"
railway up
railway domain  # Get your deployment URL
```

### 2D: Update CORS Configuration

After deployment, update your backend's CORS settings to allow requests from your production frontend:

```python
# backend/src/app.py

import os

# CORS configuration
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173"  # Default for local dev
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Set environment variable in your cloud platform:

```bash
CORS_ORIGINS=http://localhost:5173,https://your-frontend-url.com
```

### 2E: Test Production Deployment

```bash
# Test health endpoint
curl https://your-backend-url.com/health

# Test creating a task via production API
curl -X POST https://your-backend-url.com/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Production test", "status": "todo", "priority": "medium"}'

# Open frontend in browser
open https://your-frontend-url.com
```

---

## 🚀 Part 3: Production CI/CD with GitHub Actions (60 min)

### 3A: Understanding CI/CD Concepts

```mermaid
graph LR
    A[Developer<br/>Pushes Code] --> B[GitHub Actions<br/>Triggered]
    B --> C[Run Tests]
    C --> D{Tests Pass?}
    D -->|Yes| E[Deploy to Cloud]
    D -->|No| F[Notify Developer]
    E --> G[Application Live]

    style C fill:#4caf50
    style D fill:#ff9800
    style E fill:#2196f3
    style F fill:#f44336
```

**Key Concepts**:

- **Continuous Integration (CI)**: Automatically test code on every commit
- **Continuous Deployment (CD)**: Automatically deploy passing code to production
- **GitHub Actions**: GitHub's built-in CI/CD automation platform
- **Workflows**: YAML files defining automated processes
- **Secrets**: Encrypted environment variables for sensitive data

### 3B: Essential CI/CD Workflow

Create `.github/workflows/ci-cd.yml`:

```yaml
name: TaskFlow CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Test backend
  backend-test:
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

      - name: Run tests
        env:
          MONGODB_URL: mongodb://localhost:27017/taskflow_test
        run: |
          cd backend
          uv run pytest --cov=src --cov-report=term

      - name: Run linting
        run: |
          cd backend
          uv run ruff check src/

  # Test frontend
  frontend-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run linting
        run: |
          cd frontend
          npm run lint

      - name: Run tests
        run: |
          cd frontend
          npm run test -- --run

      - name: Build frontend
        run: |
          cd frontend
          npm run build

  # Deploy to production (only on main branch)
  deploy:
    needs: [backend-test, frontend-test]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to Render
        env:
          RENDER_DEPLOY_HOOK_URL: ${{ secrets.RENDER_DEPLOY_HOOK_URL }}
        run: |
          if [ -n "$RENDER_DEPLOY_HOOK_URL" ]; then
            curl "$RENDER_DEPLOY_HOOK_URL"
            echo "✅ Deployment triggered on Render"
          else
            echo "⚠️ RENDER_DEPLOY_HOOK_URL not set, skipping deployment"
          fi
```

### 3C: GitHub Actions Features Explained

#### 1. Parallel Testing

Tests run in parallel to save time:

```mermaid
graph LR
    A[Push to GitHub] --> B[Backend Tests]
    A --> C[Frontend Tests]
    B --> D{Both Pass?}
    C --> D
    D -->|Yes| E[Deploy]
    D -->|No| F[Fail Build]

    style B fill:#4caf50
    style C fill:#4caf50
    style E fill:#2196f3
```

#### 2. Conditional Deployment

Only deploy when:
- Tests pass ✅
- Branch is `main` ✅
- Event is `push` (not pull request) ✅

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

#### 3. Caching Dependencies

Speed up workflows by caching dependencies:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '18'
    cache: 'npm'  # ← Caches node_modules
```

### 3D: Secrets Management

Store sensitive data securely in GitHub Secrets:

1. **Go to Repository Settings** → "Secrets and variables" → "Actions"

2. **Add Secrets**:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `RENDER_DEPLOY_HOOK_URL`: Your Render deploy hook (optional)

3. **Use in Workflows**:
   ```yaml
   env:
     MONGODB_URL: ${{ secrets.MONGODB_URL }}
   ```

**⚠️ Security Notes**:
- Secrets are encrypted and never exposed in logs
- Never commit `.env` files with sensitive data
- Rotate secrets periodically

### 3E: Branch-Based Deployment Strategy

```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    commit
    commit id: "Deploy to Staging"
    checkout main
    merge develop
    commit id: "Deploy to Production"
```

**Recommended Strategy**:

| Branch | Environment | Auto-Deploy? | Use Case |
|--------|-------------|--------------|----------|
| `main` | Production | ✅ Yes | Live application |
| `develop` | Staging | ✅ Yes | Test before prod |
| `feature/*` | None | ❌ No | Development |

Create `.github/workflows/deploy-staging.yml`:

```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to staging
        env:
          STAGING_DEPLOY_HOOK: ${{ secrets.STAGING_DEPLOY_HOOK }}
        run: |
          curl "$STAGING_DEPLOY_HOOK"
          echo "✅ Deployed to staging environment"
```

### 3F: Advanced CI/CD Features (Optional)

#### Pull Request Checks

Prevent merging broken code:

```yaml
name: PR Checks

on:
  pull_request:
    branches: [main, develop]

jobs:
  pr-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check code quality
        run: |
          echo "Running quality checks..."
          # Add your checks here

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '✅ All checks passed! Ready to merge.'
            })
```

#### Deployment Notifications

Get notified when deployments complete:

```yaml
- name: Notify on deployment
  if: success()
  run: |
    echo "🚀 Deployment successful!"
    # Add Slack/Discord webhook notification here
```

---

## ⚙️ Part 4: Production Configuration (20 min)

### 4A: Environment-Based Settings

Create `backend/src/config.py`:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""

    # Application
    app_name: str = "TaskFlow API"
    environment: str = "development"
    debug: bool = True

    # Database
    mongodb_url: str = "mongodb://localhost:27017"

    # CORS
    cors_origins: str = "http://localhost:5173"

    # Monitoring (optional)
    sentry_dsn: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

Use in your app:

```python
from src.config import get_settings

settings = get_settings()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4B: Structured Logging

Add proper logging for production:

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("taskflow")

# Use in routes
@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate):
    logger.info(f"Creating task: {task_data.title}")
    # ... rest of code
    logger.info(f"Task created successfully: {created_task['id']}")
    return task_helper(created_task)
```

### 4C: Error Handling

Add global exception handler:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 4D: Health Checks with Database Status

Enhance health check endpoint:

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "version": "2.0.0"
    }

    # Check database
    try:
        collection = get_tasks_collection()
        await collection.database.command('ping')
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["database"] = "disconnected"
        raise HTTPException(status_code=503, detail="Database unavailable")

    return health_status
```

---

## ✅ Part 5: Verification & Testing (10 min)

### 5A: Test Your Production Application

**Backend Health Check**:

```bash
curl https://your-backend-url.com/health

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected",
#   "environment": "production",
#   "version": "2.0.0",
#   "timestamp": "2025-10-09T12:00:00"
# }
```

**Create a Task**:

```bash
curl -X POST https://your-backend-url.com/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Production deployment test",
    "description": "Testing the live application",
    "status": "done",
    "priority": "high"
  }'
```

**Test Frontend**:

1. Open your production frontend URL in browser
2. Create a new task
3. Move tasks between columns (todo → in progress → done)
4. Edit and delete tasks
5. Verify data persists on page refresh

### 5B: Monitor Your Deployment

**View Application Logs**:

**Render**:
```bash
# View logs in dashboard
# Or use Render CLI
render logs taskflow-backend
```

**Railway**:
```bash
railway logs
```

**Check GitHub Actions**:

1. Go to your repository → "Actions" tab
2. View workflow runs
3. Check deployment status

### 5C: Verification Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Health check endpoint returns "healthy"
- [ ] Can create tasks via API
- [ ] Frontend can load tasks
- [ ] Data persists in MongoDB Atlas
- [ ] GitHub Actions workflow runs successfully
- [ ] No secrets exposed in logs or code

---

## 🎉 Workshop 3 Complete!

### What You Built

```mermaid
graph TB
    subgraph "Production Architecture"
        A[React Frontend<br/>Deployed on Cloud]
        B[FastAPI Backend<br/>Deployed on Cloud]
        C[(MongoDB Atlas<br/>Cloud Database)]
        D[GitHub Actions<br/>CI/CD Pipeline]
        E[GitHub Repository<br/>Version Control]

        E -->|Push Code| D
        D -->|Run Tests| D
        D -->|Deploy| A
        D -->|Deploy| B
        A -->|HTTPS API Calls| B
        B -->|Async Queries| C
    end

    style A fill:#61dafb
    style B fill:#009688
    style C fill:#4caf50
    style D fill:#ff9800
    style E fill:#333
```

### ✅ Achievements

- ✅ **Cloud database** with MongoDB Atlas (no local DB needed!)
- ✅ **Cloud deployment** on Render (no Docker needed!)
- ✅ **Automated CI/CD** with GitHub Actions
- ✅ **Environment configuration** for dev/staging/prod
- ✅ **Health checks** for monitoring
- ✅ **Secrets management** with GitHub Secrets
- ✅ **Production-ready** full-stack application

### 🎓 Concepts Mastered

| Category | Skills Learned |
|----------|----------------|
| **Database** | Cloud databases, async MongoDB driver (Motor), document storage |
| **Deployment** | PaaS deployment, environment variables, health checks |
| **CI/CD** | GitHub Actions workflows, automated testing, automated deployment |
| **Security** | Secrets management, CORS configuration, environment separation |
| **Monitoring** | Logging, health endpoints, error tracking |
| **DevOps** | Branch-based deployment, parallel testing, deployment strategies |

### 📊 CI/CD Pipeline Flow

```mermaid
graph TB
    A[Developer Pushes Code] --> B{Which Branch?}
    B -->|feature/*| C[Run Tests Only]
    B -->|develop| D[Tests + Deploy Staging]
    B -->|main| E[Tests + Deploy Production]

    C --> F{Tests Pass?}
    D --> F
    E --> F

    F -->|Yes| G[✅ Success]
    F -->|No| H[❌ Fail Build]

    G -->|If main| I[Live in Production]
    G -->|If develop| J[Live in Staging]

    style G fill:#4caf50
    style H fill:#f44336
    style I fill:#2196f3
```

### 🚀 Next Steps & Advanced Topics

**Immediate Improvements**:

- Add **rate limiting** to prevent API abuse
- Implement **caching** with Redis for better performance
- Add **API versioning** (/api/v1/, /api/v2/)
- Create **database indexes** for faster queries

**Advanced Features**:

- **Authentication**: JWT tokens, OAuth2, user sessions
- **Real-time updates**: WebSockets, Server-Sent Events
- **File uploads**: Cloud storage (S3/GCS), image processing
- **Search**: Full-text search with MongoDB Atlas Search
- **Analytics**: Track usage metrics, performance monitoring

**Scaling & Performance**:

- **Horizontal scaling**: Multiple backend instances
- **Database optimization**: Indexes, query optimization
- **CDN**: Content delivery network for frontend
- **Load balancing**: Distribute traffic across servers

**Testing & Quality**:

- **Integration tests**: Test full API flows
- **E2E tests**: Playwright/Cypress for frontend
- **Load testing**: k6, Locust for performance
- **Security scanning**: OWASP ZAP, Bandit

### 📚 Resources

**Cloud Platforms**:
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)

**CI/CD**:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

**Database**:
- [Motor (Async MongoDB)](https://motor.readthedocs.io/)
- [MongoDB Python Tutorial](https://www.mongodb.com/languages/python)

**General**:
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [The Twelve-Factor App](https://12factor.net/)

---

## 📋 Assessment Criteria

### Technical Implementation (60 points)

- [ ] MongoDB Atlas successfully integrated (15 pts)
- [ ] All CRUD operations work with database (15 pts)
- [ ] Application deployed to cloud platform (15 pts)
- [ ] Health check endpoint functional (5 pts)
- [ ] Environment variables properly configured (10 pts)

### CI/CD Pipeline (25 points)

- [ ] GitHub Actions workflow created (10 pts)
- [ ] Automated tests run on every push (5 pts)
- [ ] Automated deployment configured (10 pts)

### Production Readiness (15 points)

- [ ] CORS properly configured for production (5 pts)
- [ ] Error handling and logging implemented (5 pts)
- [ ] Secrets not exposed in code or logs (5 pts)

---

**Duration**: 3 hours | **Level**: Intermediate to Advanced

**Congratulations!** 🎉 You've built and deployed a production-ready full-stack application with cloud database, automated CI/CD, and professional DevOps practices!
