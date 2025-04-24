from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str | None
    profile_picture: str
    language: str | None


class UserUpdateSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(UserBaseSchema):
    id: int
    telegram_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
