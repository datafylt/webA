from fastapi import APIRouter

from .apis import router

apis_router = APIRouter()
apis_router.include_router(router, tags=["APIModule"])

__all__ = ["apis_router"]
