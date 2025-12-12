from fastapi import APIRouter

from .invoices import router

invoices_router = APIRouter()
invoices_router.include_router(router, tags=["Facturation"])

__all__ = ["invoices_router"]
