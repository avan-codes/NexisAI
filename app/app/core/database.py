from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings

class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.MONGODB_DB_NAME]
    # Create indexes
    await db.db.users.create_index("github_id", unique=True)
    await db.db.users.create_index("username")
    await db.db.repositories.create_index("full_name", unique=True)
    await db.db.repositories.create_index("user_id")
    await db.db.commands.create_index("user_id")
    await db.db.commands.create_index("repo_id")
    await db.db.commands.create_index("created_at")
    await db.db.executions.create_index("user_id")
    await db.db.executions.create_index("status")
    await db.db.executions.create_index("created_at")
    await db.db.audit_logs.create_index("execution_id")
    await db.db.audit_logs.create_index("actor")
    await db.db.audit_logs.create_index("action")
    await db.db.audit_logs.create_index("timestamp")

async def close_mongo_connection():
    db.client.close()
