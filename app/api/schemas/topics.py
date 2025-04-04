from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BaseTopic(BaseModel):
    name: str
    image: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateTopicSchema(BaseTopic):
    model_config = ConfigDict(from_attributes=True)


class UpdateTopicSchema(BaseTopic):
    model_config = ConfigDict(from_attributes=True)


class ResponseTopicSchema(UpdateTopicSchema):
    id: int
    created_at: datetime | None
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)
