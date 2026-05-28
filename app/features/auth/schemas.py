from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.shared.object_id import PyObjectId


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id")
    email: EmailStr
    username: str
    display_name: str | None = None
    avatar: str | None = None
    bio: str | None = None
    role: str
    created_at: datetime


class LogoutRequest(BaseModel):
    refresh_token: str
