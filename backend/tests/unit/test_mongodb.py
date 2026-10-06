import pytest
from app.core.config import settings
from app.db.mongo import MongoSessionManager


@pytest.mark.anyio
async def test_mongodb_connection():
    manager = MongoSessionManager()
    await manager.init(settings.MONGODB_URL, settings.MONGODB_DB_NAME)
    try:
        db = manager.get_database()
        assert db is not None
        # Ping check live Atlas cluster
        ping_res = await manager.client.admin.command("ping")
        assert ping_res.get("ok") == 1.0
    finally:
        await manager.close()
