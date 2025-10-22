"""
TaskFlow Backend - FastAPI Task Management Service

A RESTful API for task management with TDD approach.
"""

from contextlib import asynccontextmanager
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
import os

# Import database and models
from .database import get_db, init_db
from .models import TaskModel, TaskStatus, TaskPriority

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("taskflow")


# Pydantic Models (for API validation)
class TaskBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initialize and cleanup resources.
    """
    # Startup
    logger.info("🚀 TaskFlow backend starting up...")

    # Only init database if not in test mode (no dependency overrides)
    if not app.dependency_overrides:
        logger.info("Initializing database...")
        init_db()
        logger.info("✅ Database ready!")
    else:
        logger.info("Test mode - skipping database initialization")

    yield
    # Shutdown
    logger.info("🛑 TaskFlow backend shutting down...")


app = FastAPI(
    title="TaskFlow API",
    description="Production-ready task management API",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Welcome to TaskFlow API - Workshop 3 Complete!",
        "version": "2.1.0",
        "docs": "/docs",
        "health": "/health",
        "status": "healthy"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for monitoring."""
    environment = os.getenv("ENVIRONMENT", "development")

    # Check database connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "error"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": environment,
        "version": "2.1.0",
        "storage": "postgresql" if "postgresql" in os.getenv("DATABASE_URL", "") else "sqlite",
        "database": db_status
    }


@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all tasks with optional filtering.

    Query parameters:
    - status: Filter by task status (todo, in_progress, done)
    - priority: Filter by priority level (low, medium, high)
    - assignee: Filter by assigned person
    """
    query = db.query(TaskModel)

    # Apply filters
    if status:
        query = query.filter(TaskModel.status == status.value)
    if priority:
        query = query.filter(TaskModel.priority == priority.value)
    if assignee:
        query = query.filter(TaskModel.assignee == assignee)

    tasks = query.all()
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    Returns the created task with generated ID and timestamps.
    """
    logger.info(f"Creating task: {task_data.title}")

    # Create database model
    db_task = TaskModel(
        id=str(uuid4()),
        **task_data.model_dump()
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    logger.info(f"Task created successfully: {db_task.id}")
    return db_task


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.

    Returns 404 if task not found.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")

    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update_data: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing task.

    Returns the updated task or 404 if not found.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")

    # Update fields that are provided
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete a task by ID.

    Returns 204 on success, 404 if not found.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")

    db.delete(task)
    db.commit()

    return


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)