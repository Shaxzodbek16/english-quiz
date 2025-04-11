from typing import Sequence
from fastapi import Depends, HTTPException, status

from app.api.schemas.options import (
    OptionsResponseSchema,
    OptionsUpdateSchema,
    OptionsCreateSchema,
)
from app.api.repositories.options import OptionsRepository
from app.api.models import AdminUsers, User


class OptionsController:

    def __init__(self, options_repository: OptionsRepository = Depends()) -> None:
        self.__options_repository = options_repository

    async def get_all_options(self) -> Sequence[OptionsResponseSchema]:
        return [
            OptionsResponseSchema.model_validate(option)
            for option in await self.__options_repository.get_all_options()
        ]

    async def get_option_by_id(self, option_id: int) -> OptionsResponseSchema:
        res = await self.__options_repository.get_option_by_id(option_id)
        if res is None:
            raise HTTPException(status_code=404, detail="Option not found")
        return OptionsResponseSchema.model_validate(
            await self.__options_repository.get_option_by_id(option_id)
        )

    async def create_option(
        self, *, option: OptionsCreateSchema, user: AdminUsers | User
    ) -> OptionsResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        return OptionsResponseSchema.model_validate(
            await self.__options_repository.create_option(option)
        )

    async def update_option(
        self, *, option_id, option: OptionsUpdateSchema, user: AdminUsers | User
    ) -> OptionsResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        res = await self.__options_repository.get_option_by_id(option_id)
        if res is None:
            raise HTTPException(status_code=404, detail="Option not found")
        return OptionsResponseSchema.model_validate(
            await self.__options_repository.update_option(option_id, option)
        )

    async def delete_option(self, *, option_id, user: AdminUsers | User) -> None:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        res = await self.__options_repository.get_option_by_id(option_id)
        if res is None:
            raise HTTPException(status_code=404, detail="Option not found")
        return await self.__options_repository.delete_option(option_id)
