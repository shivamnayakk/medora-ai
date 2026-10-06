import pytest
from sqlalchemy import text

from app.core.config import settings
from app.db.session import DatabaseSessionManager


@pytest.mark.asyncio
async def test_database_connection():
    manager = DatabaseSessionManager()
    manager.init(str(settings.DATABASE_URL))
    try:
        async with manager.session() as session:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
    finally:
        await manager.close()
