from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Sequence

from app.api.schemas.tests import TestCreateSchema, TestUpdateSchema
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

    async def get_test_by_id(self, test_id: int) -> Test | None:
        query = select(Test).where(Test.id == test_id)
        result = await self.__session.execute(query)
        return result.scalars().first()

    async def create_test(self, data: TestCreateSchema) -> Test:
        if not data.option_ids:
            data.option_ids = []
        test = Test(**data.model_dump())
        self.__session.add(test)
        await self.__session.commit()
        await self.__session.refresh(test)
        return test

    async def update_test(self, test_id: int, test: TestUpdateSchema) -> Test:
        existing_test = await self.get_test_by_id(test_id)
        if existing_test is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
            )
        existing_test.update(**test.model_dump())
        await self.__session.commit()
        await self.__session.refresh(existing_test)
        return existing_test

    async def add_option_to_test(self, *, test_id: int, option_id: int) -> None:
        test = await self.get_test_by_id(test_id)
        if test is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
            )
        test.option_ids.append(option_id)
        await self.__session.commit()
        await self.__session.refresh(test)

    async def delete_test(self, test_id: int) -> None:
        test = await self.get_test_by_id(test_id)
        if test is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
            )
        await self.__session.delete(test)
        await self.__session.commit()
