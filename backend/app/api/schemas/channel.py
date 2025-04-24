from pydantic import BaseModel, ConfigDict


class ChannelBaseSchema(BaseModel):
    name: str
    link: str
    channel_id: int
    must_subscribe: bool = False

    model_config = ConfigDict(from_attributes=True)


class ChannelCreateSchema(ChannelBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class ChannelUpdateSchema(ChannelBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class ChannelResponseSchema(ChannelBaseSchema):
    id: int
    created_at: str
    updated_at: str
    model_config = ConfigDict(from_attributes=True)
