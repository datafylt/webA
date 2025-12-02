from fastapi import APIRouter, Query

from app.controllers.dept import dept_controller
from app.schemas import Success
from app.schemas.depts import *

router = APIRouter()


@router.get("/list", summary="ViewDepartmentList")
async def list_dept(
    name: str = Query(None, description="Department Name"),
):
    dept_tree = await dept_controller.get_dept_tree(name)
    return Success(data=dept_tree)


@router.get("/get", summary="ViewDepartment")
async def get_dept(
    id: int = Query(..., description="DepartmentID"),
):
    dept_obj = await dept_controller.get(id=id)
    data = await dept_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="CreateDepartment")
async def create_dept(
    dept_in: DeptCreate,
):
    await dept_controller.create_dept(obj_in=dept_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="UpdateDepartment")
async def update_dept(
    dept_in: DeptUpdate,
):
    await dept_controller.update_dept(obj_in=dept_in)
    return Success(msg="Update Successfully")


@router.delete("/delete", summary="DeleteDepartment")
async def delete_dept(
    dept_id: int = Query(..., description="DepartmentID"),
):
    await dept_controller.delete_dept(dept_id=dept_id)
    return Success(msg="Deleted Success")
