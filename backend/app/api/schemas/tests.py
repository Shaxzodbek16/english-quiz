from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Sequence

from app.api.schemas.options import OptionsResponseSchema


class TestBaseSchema(BaseModel):
    level_id: int
    topic_id: int
    type_id: int
    question: str
    image: str | None = None
    answer_explanation: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TestCreateSchema(TestBaseSchema):
    option_ids: Sequence[int] = []
    model_config = ConfigDict(from_attributes=True)


class TestUpdateSchema(TestBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class TestResponseSchema(TestBaseSchema):
    id: int
    options: Sequence[OptionsResponseSchema]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
