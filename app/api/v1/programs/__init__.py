from fastapi import APIRouter

from .programs import router

programs_router = APIRouter()
programs_router.include_router(router, tags=["Programmes"])

__all__ = ["programs_router"]
