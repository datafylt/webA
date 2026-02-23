import logging

from fastapi import APIRouter, Body, Query
from tortoise.expressions import Q

from app.controllers.user import user_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.users import *

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="ViewUserList")
async def list_user(
    page: int = Query(1, description="page number"),
    page_size: int = Query(10, description="per page count"),
    username: str = Query("", description="Username，forSearch"),
    email: str = Query("", description="EmailAddress"),
):
    q = Q()
    if username:
        q &= Q(username__contains=username)
    if email:
        q &= Q(email__contains=email)
    total, user_objs = await user_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict(m2m=True, exclude_fields=["password"]) for obj in user_objs]

    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="ViewUser")
async def get_user(
    user_id: int = Query(..., description="UserID"),
):
    user_obj = await user_controller.get(id=user_id)
    user_dict = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=user_dict)


@router.post("/create", summary="CreateUser")
async def create_user(
    user_in: UserCreate,
):
    user = await user_controller.get_by_email(user_in.email)
    if user:
        return Fail(code=400, msg="The user with this email already exists in the system.")
    new_user = await user_controller.create_user(obj_in=user_in)
    await user_controller.update_roles(new_user, user_in.role_ids)
    return Success(msg="Created Successfully")


@router.post("/update", summary="UpdateUser")
async def update_user(
    user_in: UserUpdate,
):
    user = await user_controller.update(id=user_in.id, obj_in=user_in)
    await user_controller.update_roles(user, user_in.role_ids)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="DeleteUser")
async def delete_user(
    user_id: int = Query(..., description="UserID"),
):
    await user_controller.remove(id=user_id)
    return Success(msg="Deleted Successfully")


@router.post("/reset_password", summary="ResetPassword")
async def reset_password(user_id: int = Body(..., description="UserID", embed=True)):
    await user_controller.reset_password(user_id)
    return Success(msg="PasswordalreadyResetfor123456")
