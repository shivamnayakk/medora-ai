import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.main import app


@pytest.mark.anyio
async def test_root_endpoint():
    """Verify root endpoint returns app metadata."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["app"] == settings.APP_NAME
        assert data["version"] == settings.APP_VERSION
        assert data["environment"] == settings.APP_ENV


@pytest.mark.anyio
async def test_api_v1_health_endpoint():
    """Verify modular /api/v1/health endpoint returns structured HealthResponse."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["app"] == settings.APP_NAME
        assert data["version"] == settings.APP_VERSION
        assert "timestamp" in data
        assert "services" in data
        assert isinstance(data["services"], dict)


@pytest.mark.anyio
async def test_top_level_health_alias():
    """Verify top-level /health alias works for container health checks."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
