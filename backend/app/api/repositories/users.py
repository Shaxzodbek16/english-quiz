from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from sqlalchemy import select

from app.api.models import User
from app.api.schemas.users import UserUpdateSchema
from app.core.databases.postgres import get_general_session


class UserRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_general_session),
    ):
        self.__session = session

    async def get_all_users(self, page: int, size: int) -> Sequence[User]:
        users = await self.__session.execute(
            select(User).offset(page * size).limit(size)
        )
        return users.scalars().all()

    async def get_users_count(self) -> int:
        count = await self.__session.execute(select(User))
        return len(count.scalars().all()) or 0

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        user = await self.__session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return user.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.__session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()

    async def update_user(self, data: UserUpdateSchema, user_id: int) -> User:
        user = await self.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.update(**data.model_dump())
        await self.__session.commit()
        await self.__session.refresh(user)
        return user
