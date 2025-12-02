from datetime import datetime
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.models.admin import AuditLog
from app.schemas import SuccessExtra
from app.schemas.apis import *

router = APIRouter()


@router.get("/list", summary="ViewOperation Log")
async def get_audit_log_list(
    page: int = Query(1, description="page number"),
    page_size: int = Query(10, description="per page count"),
    username: str = Query("", description="ActionspersonName"),
    module: str = Query("", description="Function Module"),
    method: str = Query("", description="Request method"),
    summary: str = Query("", description="API Description"),
    path: str = Query("", description="Request Path"),
    status: int = Query(None, description="Status Code"),
    start_time: datetime = Query("", description="Start Time"),
    end_time: datetime = Query("", description="End Time"),
):
    q = Q()
    if username:
        q &= Q(username__icontains=username)
    if module:
        q &= Q(module__icontains=module)
    if method:
        q &= Q(method__icontains=method)
    if summary:
        q &= Q(summary__icontains=summary)
    if path:
        q &= Q(path__icontains=path)
    if status:
        q &= Q(status=status)
    if start_time and end_time:
        q &= Q(created_at__range=[start_time, end_time])
    elif start_time:
        q &= Q(created_at__gte=start_time)
    elif end_time:
        q &= Q(created_at__lte=end_time)

    audit_log_objs = await AuditLog.filter(q).offset((page - 1) * page_size).limit(page_size).order_by("-created_at")
    total = await AuditLog.filter(q).count()
    data = [await audit_log.to_dict() for audit_log in audit_log_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)
