from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class SupportData(BaseModel):
    url: str
    text: str


class ResponseModel(BaseModel):
    data: UserData
    support: SupportData


class UserCreateRequest(BaseModel):
    name: str
    job: str


class UserCreateResponse(UserCreateRequest):
    id: str
    created_at: datetime

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    token: str


class UpdateUserRequest(BaseModel):
    name: str | None = None
    job: str | None = None


class UpdatedUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: str