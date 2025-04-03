from fastapi import Depends, HTTPException
from typing import Sequence

from app.api.models import AdminUsers, User
from app.api.repositories.test_types import TestTypesRepository
from app.api.schemas.test_types import (
    TestTypeResponseSchema,
    TestTypeCreateSchema,
    TestTypeUpdateSchema,
)


class TestTypesController:
    def __init__(
        self,
        test_types_repository: TestTypesRepository = Depends(),
    ) -> None:
        self.__test_type_repository = test_types_repository

    async def get_all_test_types(self) -> Sequence[TestTypeResponseSchema]:
        return await self.__test_type_repository.get_all_test_types()

    async def get_test_type_by_id(self, test_type: int) -> TestTypeResponseSchema:
        res = await self.__test_type_repository.get_test_type_by_id(test_type)
        if res is None:
            raise HTTPException(status_code=404, detail="test_type not found")
        return res

    async def create_test_type(
        self, *, user: AdminUsers | User, test_type: TestTypeCreateSchema
    ) -> TestTypeResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=404, detail="Not found")
        if await self.__test_type_repository.get_test_type_by_name(test_type.name) > 0:
            raise HTTPException(
                status_code=400, detail=f"{test_type.name} already exists"
            )
        return await self.__test_type_repository.create_test_type(test_type)

    async def update_test_type(
        self,
        *,
        test_type_id: int,
        user: AdminUsers | User,
        test_type: TestTypeUpdateSchema,
    ) -> TestTypeResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=404, detail="Not found")
        res = await self.__test_type_repository.get_test_type_by_id(test_type_id)
        if res is None:
            raise HTTPException(status_code=404, detail="test_type not found")
        if await self.__test_type_repository.get_test_type_by_name(test_type.name) > 1:
            raise HTTPException(
                status_code=400, detail=f"{test_type.name} already exists"
            )
        return await self.__test_type_repository.update_test_type(
            test_type_id, test_type
        )

    async def delete_test_type(
        self, *, test_type_id: int, user: AdminUsers | User
    ) -> None:
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=404, detail="Not found")
        res = await self.__test_type_repository.get_test_type_by_id(test_type_id)
        if res is None:
            raise HTTPException(status_code=404, detail="test_type not found")
        return await self.__test_type_repository.delete_test_type(test_type_id)
