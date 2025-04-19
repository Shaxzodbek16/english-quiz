from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

from app.api.models import UserTest
from app.api.schemas.user_tests import UserTestCreateSchema

from app.core.databases.postgres import get_general_session


class UserTestRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session = session

    async def create_user_test(
        self, *, data: UserTestCreateSchema, user_id: int
    ) -> UserTest:
        user_test = UserTest(**data.model_dump(), user_id=user_id)
        self.__session.add(user_test)
        await self.__session.commit()
        await self.__session.refresh(user_test)
        return user_test

    async def get_user_test_by_id(self, *, user_test_id: int) -> UserTest | None:
        user_test = await self.__session.execute(
            select(UserTest).where(UserTest.id == user_test_id)
        )
        return user_test.scalars().first()

    async def get_all_user_tests(self, *, page: int, size: int) -> Sequence[UserTest]:
        user_tests = await self.__session.execute(
            select(UserTest).offset(page * size).limit(size)
        )
        return user_tests.scalars().all()
