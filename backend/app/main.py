from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import sessionmanager
from app.db.mongo import mongomanager
from app.db.redis import redismanager

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Medora AI application")
    try:
        # 1. PostgreSQL (Relational Source of Truth)
        sessionmanager.init(str(settings.DATABASE_URL))
        logger.info("PostgreSQL connected successfully")

        # 2. MongoDB (Voice Transcripts & AI Telemetry)
        await mongomanager.init(settings.MONGODB_URL, settings.MONGODB_DB_NAME)
        logger.info("MongoDB Atlas connected successfully")

        # 3. Redis (Session Cache & Distributed Locks)
        await redismanager.init(settings.REDIS_URL)
        logger.info("Upstash Redis connected successfully")

        yield
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        raise
    finally:
        await redismanager.close()
        await mongomanager.close()
        await sessionmanager.close()
        logger.info("All database connections closed successfully")
        logger.info("Application shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        }

    @app.get("/health", tags=["Health"])
    async def top_level_health():
        return {"status": "healthy"}

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
