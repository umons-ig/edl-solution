"""
TaskFlow Backend - FastAPI Task Management Service

A RESTful API for task management with TDD approach.
"""

from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from bson import ObjectId
import logging

from src.database import (
    connect_to_mongo,
    close_mongo_connection,
    get_tasks_collection
)
from src.models import task_helper, task_to_db
from src.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("taskflow")

# Get settings
settings = get_settings()


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initialize and cleanup resources.
    """
    # Startup
    logger.info("🚀 TaskFlow backend starting up...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("🛑 TaskFlow backend shutting down...")
    await close_mongo_connection()


app = FastAPI(
    title="TaskFlow API",
    description="Production-ready task management API with MongoDB",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint for monitoring."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "version": "2.0.0"
    }

    # Check database connection
    try:
        collection = get_tasks_collection()
        await collection.database.command('ping')
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["database"] = "disconnected"
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

    return health_status


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


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate):
    """
    Create a new task in MongoDB.

    Returns the created task with generated ID and timestamps.
    """
    logger.info(f"Creating task: {task_data.title}")
    collection = get_tasks_collection()

    # Prepare task for database
    db_task = task_to_db(task_data.model_dump())

    # Insert into MongoDB
    result = await collection.insert_one(db_task)

    # Retrieve the created task
    created_task = await collection.find_one({"_id": result.inserted_id})

    logger.info(f"Task created successfully: {str(result.inserted_id)}")
    return task_helper(created_task)


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """
    Get a specific task by ID.

    Returns 404 if task not found.
    """
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
    """
    Update an existing task.

    Returns the updated task or 404 if not found.
    """
    collection = get_tasks_collection()

    # Validate ObjectId
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    # Prepare update data
    update_dict = {k: v for k, v in update_data.model_dump(exclude_unset=True).items() if v is not None}
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
    """
    Delete a task by ID.

    Returns 204 on success, 404 if not found.
    """
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