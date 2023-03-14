from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class BaseOut(BaseModel):
    id: int
    created: datetime = None
    modified: datetime = None
    external_id: str = None
    is_deleted: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class PasswordIn(BaseModel):
    password: str


class ResetPasswordIn(BaseModel):
    email: str


class ListResource(BaseModel):
    total: int
    data: List[Any]  # TODO: I think pydantic has a generic model that can be used


class UserIn(BaseModel):
    id: int = None
    email: str
    company: str = None
    first_name: str = None
    last_name: str = None
    is_disabled: bool = None
    reset_token: str = None
    scopes: List[str] = []

    class Config:
        orm_mode = True


class UserOut(BaseOut):
    email: str
    first_name: str = None
    last_name: str = None
    disabled: bool = None
    reset_token: str = None
    scopes: List[str] = None
    last_login: str = None

    class Config:
        orm_mode = True
