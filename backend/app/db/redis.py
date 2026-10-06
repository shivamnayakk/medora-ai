from typing import Any
import redis.asyncio as aioredis
from redis.asyncio import Redis

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class RedisSessionManager:
    """
    Asynchronous Redis Connection Manager using redis.asyncio.
    Provides in-memory caching, distributed locks for appointment booking,
    and rate limiting capabilities.
    """
    def __init__(self) -> None:
        self.client: Redis | None = None

    async def init(self, redis_url: str) -> None:
        try:
            logger.info("Initializing Redis Async connection...")
            self.client = aioredis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_timeout=5.0,
                protocol=2,
            )
            # Verify live connection
            await self.client.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}", exc_info=True)
            raise

    async def close(self) -> None:
        try:
            if self.client:
                await self.client.aclose()
                self.client = None
                logger.info("Redis connection closed successfully")
        except Exception as e:
            logger.error(f"Error while closing Redis connection: {e}")
            raise

    def get_client(self) -> Redis:
        if self.client is None:
            raise RuntimeError("Redis is not initialized. Call init() first.")
        return self.client

    # 🛡️ Atomic Distributed Lock for Double-Booking Prevention
    async def acquire_lock(self, lock_key: str, expire_seconds: int = 15) -> bool:
        """
        Acquires an atomic distributed lock using SET NX EX.
        Prevents race conditions when two patients try to book the same doctor slot.
        """
        client = self.get_client()
        # NX = set only if not exists, EX = expire after seconds
        acquired = await client.set(lock_key, "LOCKED", nx=True, ex=expire_seconds)
        return bool(acquired)

    async def release_lock(self, lock_key: str) -> None:
        """Releases the distributed lock after booking completes or fails."""
        client = self.get_client()
        await client.delete(lock_key)


redismanager = RedisSessionManager()


async def get_redis() -> Redis:
    """FastAPI Dependency for injecting Redis client into routes."""
    return redismanager.get_client()
