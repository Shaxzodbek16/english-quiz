from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.future import select

from app.api.models import User
from app.core.databases.postgres import get_general_session


class UserRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_general_session),
    ):
        self.__session = session

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        user = await self.__session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return user.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.__session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()
