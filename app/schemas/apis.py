from pydantic import BaseModel, Field

from app.models.enums import MethodType


class BaseApi(BaseModel):
    path: str = Field(..., description="API path", example="/api/v1/user/list")
    summary: str = Field("", description="API summary", example="View user list")
    method: MethodType = Field(..., description="API method", example="GET")
    tags: str = Field(..., description="API tags", example="User")


class ApiCreate(BaseApi): ...


class ApiUpdate(BaseApi):
    id: int
