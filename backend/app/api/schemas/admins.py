from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AdminBaseSchema(BaseModel):
    first_name: str
    last_name: str | None = None
    email: str
    telegram_id: int
    password: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class AdminUpdateSchema(AdminBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class AdminCreateSchema(AdminBaseSchema):
    is_admin: bool = True
    model_config = ConfigDict(from_attributes=True)


class AdminResponseSchema(AdminBaseSchema):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
