from pydantic import BaseModel
from datetime import datetime


class BaseLevel(BaseModel):
    name: str
    image: str | None = None


class CreateLevel(BaseLevel):
    pass


class UpdateLevel(BaseLevel):
    created_at: datetime | None
    updated_at: datetime | None


class ResponseLevel(UpdateLevel):
    id: int
