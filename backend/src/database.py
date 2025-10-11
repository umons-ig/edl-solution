from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB configuration
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://localhost:27017"  # Fallback for local dev
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
    Returns the 'taskflow_db' database (or test database in tests).
    """
    # Use test database if in test environment
    db_name = "taskflow_test" if os.getenv("TEST_MODE") == "true" else "taskflow_db"
    return mongodb_client[db_name]


def get_tasks_collection():
    """
    Get the tasks collection.
    This is where we store all task documents.
    """
    db = get_database()
    return db.tasks
