from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserTestBaseSchema(BaseModel):
    test_id: int
    selected_option_id: int
    correct_option_id: int
    model_config = ConfigDict(from_attributes=True)


class UserTestCreateSchema(UserTestBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class UserTestResponseSchema(UserTestBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
