from pydantic import BaseModel
from datetime import datetime


class BaseLevel(BaseModel):
    name: str
    image: str | None = None


class CreateLevelSchema(BaseLevel):
    pass


class UpdateLevelSchema(BaseLevel):
    created_at: datetime | None
    updated_at: datetime | None


class ResponseLevelSchema(UpdateLevelSchema):
    id: int
