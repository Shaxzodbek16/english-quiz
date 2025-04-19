from pydantic import BaseModel, ConfigDict


class ContentResponseSchema(BaseModel):
    upload_to: str
    link: str

    model_config = ConfigDict(from_attributes=True)
