import pytest
from app.core.config import settings
from app.db.redis import RedisSessionManager


@pytest.mark.anyio
async def test_redis_connection_and_lock():
    manager = RedisSessionManager()
    await manager.init(settings.REDIS_URL)
    try:
        client = manager.get_client()
        # 1. Ping check live Upstash cluster
        pong = await client.ping()
        assert pong is True

        # 2. Test Atomic Distributed Lock (Appointment double-booking preventer)
        lock_key = "lock:doctor_1:slot_10am"
        # Pehla patient lock acquire karta hai -> True
        acquired_first = await manager.acquire_lock(lock_key, expire_seconds=5)
        assert acquired_first is True

        # Doosra patient same time par koshish karta hai -> False (Blocked!)
        acquired_second = await manager.acquire_lock(lock_key, expire_seconds=5)
        assert acquired_second is False

        # Pehla booking complete karke release karta hai
        await manager.release_lock(lock_key)

        # Ab lock free ho gaya
        acquired_third = await manager.acquire_lock(lock_key, expire_seconds=5)
        assert acquired_third is True
        await manager.release_lock(lock_key)
    finally:
        await manager.close()
