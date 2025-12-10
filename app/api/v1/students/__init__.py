from fastapi import APIRouter

from .students import router

students_router = APIRouter()
students_router.include_router(router, tags=["Étudiants"])

__all__ = ["students_router"]
