from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Sequence
from app.core.databases.postgres import get_general_session
from app.api.models import Test


class TestsRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session: AsyncSession = session

    async def get_all_tests(
        self, *, level_id: int, topic_id: int, type_id: int, page: int, size: int
    ) -> Sequence[Test]:
        query = (
            (select(Test).where(Test.level_id == level_id))
            .where(Test.topic_id == topic_id)
            .where(Test.type_id == type_id)
            .offset(page * size)
            .limit(size)
        )
        result = await self.__session.execute(query)
        return result.scalars().all()
