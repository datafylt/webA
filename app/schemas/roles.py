from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseRole(BaseModel):
    id: int
    name: str
    desc: str = ""
    users: Optional[list] = []
    menus: Optional[list] = []
    apis: Optional[list] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class RoleCreate(BaseModel):
    name: str = Field(example="Admin")
    desc: str = Field("", example="AdminRole")


class RoleUpdate(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Admin")
    desc: str = Field("", example="AdminRole")


class RoleUpdateMenusApis(BaseModel):
    id: int
    menu_ids: list[int] = []
    api_infos: list[dict] = []
