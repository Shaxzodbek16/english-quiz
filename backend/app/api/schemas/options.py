from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class OptionsBaseSchema(BaseModel):
    option: str
    is_correct: bool
    model_config = ConfigDict(from_attributes=True)


class OptionsCreateSchema(OptionsBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class OptionsUpdateSchema(OptionsBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class OptionsResponseSchema(OptionsBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
