from multiprocessing.util import is_exiting

from fastapi import Depends, HTTPException, status
from typing import Sequence

from app.api.models import AdminUsers, User
from app.api.repositories.levels import LevelRepository
from app.api.schemas.levels import ResponseLevelSchema

from app.api.schemas.levels import CreateLevelSchema, UpdateLevelSchema


class LevelController:
    def __init__(self, level_repository: LevelRepository = Depends()):
        self.__level_repository = level_repository

    async def get_all_levels(self) -> Sequence[ResponseLevelSchema]:
        return await self.__level_repository.get_all_levels()

    async def get_level_by_id(self, level_id: int) -> ResponseLevelSchema:
        level = await self.__level_repository.get_level_by_id(level_id)
        if level is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Level with id {level_id} not found",
            )
        return level

    async def create_level(
        self, level: CreateLevelSchema, current_user: AdminUsers | User
    ) -> ResponseLevelSchema:
        if isinstance(current_user, User):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )
        if await self.__level_repository.get_level_by_name(level.name) >= 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Level with name {level.name} already exists",
            )
        return await self.__level_repository.create_level(level)

    async def update_level(
        self,
        *,
        level: UpdateLevelSchema,
        level_id: int,
        current_user: AdminUsers | User,
    ):
        if isinstance(current_user, User):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )
        if await self.__level_repository.get_level_by_name(level.name) >= 2:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Level with name {level.name} already exists",
            )

        return await self.__level_repository.update_level(level, level_id)

    async def delete_level(
        self, *, level_id: int, current_user: AdminUsers | User
    ) -> None:
        if isinstance(current_user, User):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )
        level = await self.__level_repository.get_level_by_id(level_id)
        if level is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Level with id {level_id} not found",
            )
        return await self.__level_repository.delete_level(level_id)
