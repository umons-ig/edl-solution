"""
TaskFlow Backend - FastAPI Task Management Service

A RESTful API for task management with TDD approach.
"""

from contextlib import asynccontextmanager
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("taskflow")


# Pydantic Models
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


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


# In-memory storage
tasks_db: List[Task] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initialize and cleanup resources.
    """
    # Startup
    logger.info("🚀 TaskFlow backend starting up...")
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
async def health_check():
    """Health check endpoint for monitoring."""
    environment = os.getenv("ENVIRONMENT", "development")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": environment,
        "version": "2.1.0",
        "storage": "in-memory"
    }


@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
):
    """
    List all tasks with optional filtering.

    Query parameters:
    - status: Filter by task status (todo, in_progress, done)
    - priority: Filter by priority level (low, medium, high)
    - assignee: Filter by assigned person
    """
    tasks = tasks_db.copy()

    # Apply filters
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if assignee:
        tasks = [t for t in tasks if t.assignee == assignee]

    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate):
    """
    Create a new task.

    Returns the created task with generated ID and timestamps.
    """
    logger.info(f"Creating task: {task_data.title}")
    now = datetime.utcnow()

    task = Task(
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
        **task_data.model_dump()
    )

    tasks_db.append(task)
    logger.info(f"Task created successfully: {task.id}")
    return task


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """
    Get a specific task by ID.

    Returns 404 if task not found.
    """
    for task in tasks_db:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update_data: TaskUpdate):
    """
    Update an existing task.

    Returns the updated task or 404 if not found.
    """
    for task in tasks_db:
        if task.id == task_id:
            # Update fields that are provided
            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(task, field, value)

            # Update timestamp
            task.updated_at = datetime.utcnow()
            return task

    raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """
    Delete a task by ID.

    Returns 204 on success, 404 if not found.
    """
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return

    raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return {
        "detail": "Internal server error",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)