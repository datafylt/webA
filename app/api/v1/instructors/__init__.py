from fastapi import APIRouter

from .instructors import router

instructors_router = APIRouter()
instructors_router.include_router(router, tags=["Formateurs"])

__all__ = ["instructors_router"]
