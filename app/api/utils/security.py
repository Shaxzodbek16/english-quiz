import uuid
from jose import jwt

from app.core.settings import get_settings, Settings

settings: Settings = get_settings()


def hash_telegram_id(telegram_id: int) -> str:
    return jwt.encode(
        {"telegram_id": telegram_id, "_": str(uuid.uuid4())[:2]},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def get_telegram_id(hashed_telegram_id: str) -> int:
    decoded_data = jwt.decode(
        hashed_telegram_id, settings.SECRET_KEY, algorithms=["HS256"]
    )
    return decoded_data["telegram_id"]
