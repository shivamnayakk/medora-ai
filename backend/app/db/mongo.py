from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class MongoSessionManager:
    """
    Asynchronous MongoDB Connection Lifecycle Manager using Motor.
    Manages connection pools, health checks, and database access.
    """
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def init(self, mongodb_url: str, db_name: str) -> None:
        try:
            logger.info("Initializing MongoDB Async connection...")
            self.client = AsyncIOMotorClient(
                mongodb_url,
                serverSelectionTimeoutMS=5000,
            )
            self.db = self.client[db_name]
            # Verify live connection
            await self.client.admin.command("ping")
            logger.info(f"MongoDB connected successfully to database: '{db_name}'")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}", exc_info=True)
            raise

    async def close(self) -> None:
        try:
            if self.client:
                self.client.close()
                self.client = None
                self.db = None
                logger.info("MongoDB connection closed successfully")
        except Exception as e:
            logger.error(f"Error while closing MongoDB connection: {e}")
            raise

    def get_database(self) -> AsyncIOMotorDatabase:
        if self.db is None:
            raise RuntimeError("MongoDB is not initialized. Call init() first.")
        return self.db


mongomanager = MongoSessionManager()


async def get_mongo_db() -> AsyncIOMotorDatabase:
    """FastAPI Dependency for injecting MongoDB database instance into routes."""
    return mongomanager.get_database()
