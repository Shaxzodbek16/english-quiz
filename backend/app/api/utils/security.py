import uuid

from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from app.core.settings import get_settings, Settings

settings: Settings = get_settings()


def hash_telegram_id(telegram_id: int) -> str:
    return jwt.encode(
        {"telegram_id": telegram_id, "_": str(uuid.uuid4())[:2]},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def get_telegram_id(hashed_telegram_id: str) -> int:
    try:
        decoded_data = jwt.decode(
            hashed_telegram_id, settings.SECRET_KEY, algorithms=["HS256"]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid telegram id"
        )
    return decoded_data["telegram_id"]


if __name__ == "__main__":
    print(hash_telegram_id(211980759318))
