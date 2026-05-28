from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.shared.object_id import PyObjectId


class UserDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId | None = Field(default=None, alias="_id")
    email: EmailStr
    username: str
    display_name: str | None = None

    avatar: str | None = None
    bio: str | None = None
    password_hash: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
