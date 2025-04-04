from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TestTypeBaseSchema(BaseModel):
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TestTypeCreateSchema(TestTypeBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class TestTypeUpdateSchema(TestTypeBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class TestTypeResponseSchema(TestTypeBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
