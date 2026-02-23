from fastapi import APIRouter

from app.core.dependency import DependPermission

from .base import base_router
from .roles import roles_router
from .users import users_router
from .auditlog import auditlog_router
from .students import students_router
from .programs import programs_router
from .sessions import sessions_router
from .invoices import invoices_router
from .instructors import instructors_router
from .notifications import notifications_router
from .email import email_router
from .dashboard import router as dashboard_router

v1_router = APIRouter()

# Base (login, etc.)
v1_router.include_router(base_router, prefix="/base")

# Système (users, roles, auditlog)
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermission])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermission])
v1_router.include_router(auditlog_router, prefix="/auditlog", dependencies=[DependPermission])

# Formation Électro - Modules métier
v1_router.include_router(students_router, prefix="/student", dependencies=[DependPermission])
v1_router.include_router(programs_router, prefix="/program", dependencies=[DependPermission])
v1_router.include_router(sessions_router, prefix="/session", dependencies=[DependPermission])
v1_router.include_router(invoices_router, prefix="/invoice", dependencies=[DependPermission])
v1_router.include_router(instructors_router, prefix="/instructor", dependencies=[DependPermission])
v1_router.include_router(notifications_router, prefix="/notification", dependencies=[DependPermission])
v1_router.include_router(email_router, prefix="/email", dependencies=[DependPermission])
v1_router.include_router(dashboard_router, prefix="/dashboard", dependencies=[DependPermission], tags=["Dashboard"])
