from fastapi import APIRouter

from .sessions import router

sessions_router = APIRouter()
sessions_router.include_router(router, tags=["Sessions"])

__all__ = ["sessions_router"]
