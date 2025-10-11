from typing import Optional
from datetime import datetime


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
