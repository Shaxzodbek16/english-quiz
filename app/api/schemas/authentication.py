from pydantic import BaseModel


class LoginSchema(BaseModel):
    telegram_id: int
    email: str | None = None
    password: str | None = None


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"
