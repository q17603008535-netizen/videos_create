from pydantic import BaseModel, SecretStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: SecretStr


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    username: str
    password: SecretStr


class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserResponse] = None
