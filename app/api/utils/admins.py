from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models.admins import AdminUsers
from app.api.models.users import User
from app.core.databases.postgres import get_general_session
from app.core.settings import Settings, get_settings

settings: Settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/admin/authentication/login/",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class JWTHandler:
    def __init__(self, _settings: Settings) -> None:
        self.__settings = _settings

    def create_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, self.__settings.SECRET_KEY, algorithm=self.__settings.ALGORITHM
        )

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        return self.create_token(
            data,
            expires_delta
            or timedelta(minutes=self.__settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        return self.create_token(
            data,
            expires_delta or timedelta(days=self.__settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

    async def __find_user(
        self, payload: dict, session: AsyncSession
    ) -> AdminUsers | User:
        email = payload.get("email", None)
        telegram_id = payload.get("telegram_id", None)
        if telegram_id in self.__settings.get_superusers:
            res = await session.execute(
                select(AdminUsers).where(AdminUsers.telegram_id == telegram_id)
            )
            user = res.scalar_one_or_none()
            if user is not None:
                return user
        if telegram_id is not None:
            res = await session.execute(
                select(AdminUsers).where(AdminUsers.telegram_id == telegram_id)
            )
            user = res.scalar_one_or_none()
            if user is not None:
                return user

            res = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = res.scalar_one_or_none()
            if user is not None:
                return user
        if email is not None:
            res = await session.execute(
                select(AdminUsers).where(AdminUsers.email == email)
            )
            user = res.scalar_one_or_none()
            if user is not None:
                return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    async def get_user_by_token(
        self, token: str, session: AsyncSession
    ) -> AdminUsers | User:
        try:
            payload = jwt.decode(
                token,
                self.__settings.SECRET_KEY,
                algorithms=[self.__settings.ALGORITHM],
            )
            return await self.__find_user(payload, session)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )


jwt_handler = JWTHandler(get_settings())


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_general_session),
) -> AdminUsers | User:
    return await jwt_handler.get_user_by_token(token, session)
