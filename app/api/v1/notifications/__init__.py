from fastapi import APIRouter

from .notifications import router

notifications_router = APIRouter()
notifications_router.include_router(router, tags=["Notifications"])

__all__ = ["notifications_router"]
