from fastapi import APIRouter
from app.api.routes import health, ping, welcome

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(ping.router, prefix="/ping", tags=["Ping"])
api_router.include_router(welcome.router, prefix="/welcome", tags=["Welcome"])
