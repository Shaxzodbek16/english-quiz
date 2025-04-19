from pydantic import BaseModel, ConfigDict


class AdminLoginSchema(BaseModel):
    telegram_id_or_email: int | str
    password: str
    model_config = ConfigDict(from_attributes=True)


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    model_config = ConfigDict(from_attributes=True)


class TokenResponseSchema(RefreshTokenResponseSchema):
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)
