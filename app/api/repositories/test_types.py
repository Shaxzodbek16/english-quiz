from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Sequence

from app.api.schemas.test_types import (
    TestTypeResponseSchema,
    TestTypeCreateSchema,
    TestTypeUpdateSchema,
)
from app.core.databases.postgres import get_general_session
from app.api.models import TestTypes


class TestTypesRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session = session

    async def get_all_test_types(self) -> Sequence[TestTypeResponseSchema]:
        result = await self.__session.execute(select(TestTypes))
        test_types = result.scalars().all()
        return [
            TestTypeResponseSchema.model_validate(test_type) for test_type in test_types
        ]

    async def get_test_type_by_id(
        self, test_type: int
    ) -> TestTypeResponseSchema | None:
        result = await self.__session.execute(
            select(TestTypes).where(TestTypes.id == test_type)
        )
        test_res = result.scalar_one_or_none()
        if test_res is None:
            return None
        return TestTypeResponseSchema.model_validate(test_res)

    async def get_test_type_by_name(self, name: str) -> int:
        result = await self.__session.execute(
            select(TestTypes).where(TestTypes.name == name)
        )
        test_type = result.scalars().all()
        return len(test_type)

    async def create_test_type(
        self, test_type: TestTypeCreateSchema
    ) -> TestTypeResponseSchema:
        test_type = TestTypes(**test_type.model_dump())  # type: ignore
        self.__session.add(test_type)
        await self.__session.commit()
        await self.__session.refresh(test_type)
        return TestTypeResponseSchema.model_validate(test_type)

    async def update_test_type(
        self, test_type_id: int, test_type: TestTypeUpdateSchema
    ) -> TestTypeResponseSchema:
        q = await self.__session.execute(
            select(TestTypes).where(TestTypes.id == test_type_id)
        )
        old_test_type = q.scalars().first()
        old_test_type.update(test_type.model_dump())  # type: ignore
        await self.__session.commit()
        await self.__session.refresh(old_test_type)
        return TestTypeResponseSchema.model_validate(old_test_type)

    async def delete_test_type(self, test_type_id: int) -> None:
        q = await self.__session.execute(
            select(TestTypes).where(TestTypes.id == test_type_id)
        )
        test_type = q.scalars().first()
        if test_type is None:
            return
        await self.__session.delete(test_type)
        await self.__session.commit()
