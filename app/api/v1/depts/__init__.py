from fastapi import APIRouter

from .depts import router

depts_router = APIRouter()
depts_router.include_router(router, tags=["DepartmentModule"])

__all__ = ["depts_router"]
