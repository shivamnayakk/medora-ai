from datetime import datetime, timezone
from typing import Dict
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(
        default="healthy",
        description="Overall health status of the application",
    )
    app: str = Field(description="Application name")
    version: str = Field(description="Application version")
    environment: str = Field(description="Deployment environment")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Current UTC timestamp in ISO 8601 format",
    )
    services: Dict[str, str] = Field(
        default_factory=lambda: {
            "database": "standby (Phase 4)",
            "redis": "standby (Phase 8)",
            "vector_store": "standby (Phase 8)",
        },
        description="Status of connected external services",
    )
