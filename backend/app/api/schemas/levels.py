from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BaseLevel(BaseModel):
    name: str
    image: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateLevelSchema(BaseLevel):
    model_config = ConfigDict(from_attributes=True)


class UpdateLevelSchema(BaseLevel):
    model_config = ConfigDict(from_attributes=True)


class ResponseLevelSchema(UpdateLevelSchema):
    id: int
    created_at: datetime | None
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)
