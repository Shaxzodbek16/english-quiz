from fastapi import HTTPException
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

from app.api.schemas.levels import (
    ResponseLevelSchema,
    CreateLevelSchema,
    UpdateLevelSchema,
)
from app.core.databases.postgres import get_general_session
from app.api.models.levels import Level


class LevelRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_all_levels(
        self,
    ) -> Sequence[ResponseLevelSchema]:
        result = await self.__session.execute(select(Level))
        levels = result.scalars().all()
        return [ResponseLevelSchema.model_validate(level) for level in levels]

    async def get_level_by_id(self, level_id: int) -> ResponseLevelSchema | None:
        result = await self.__session.execute(select(Level).where(Level.id == level_id))
        level = result.scalar_one_or_none()
        if level is None:
            return None
        return ResponseLevelSchema.model_validate(level)

    async def get_level_by_name(self, name: str) -> int:
        result = await self.__session.execute(select(Level).where(Level.name == name))
        levels = result.scalars().all()
        return len(levels)

    async def create_level(self, level: CreateLevelSchema) -> ResponseLevelSchema:
        new_level = Level(**level.model_dump())
        self.__session.add(new_level)
        await self.__session.commit()
        await self.__session.refresh(new_level)
        return ResponseLevelSchema.model_validate(new_level)

    async def update_level(
        self, level: UpdateLevelSchema, level_id: int
    ) -> ResponseLevelSchema:
        result = await self.__session.execute(select(Level).where(Level.id == level_id))
        existing_level = result.scalars().first()
        new_level = existing_level.update(level.model_dump())  # type: ignore
        await self.__session.commit()
        await self.__session.refresh(new_level)
        return ResponseLevelSchema.model_validate(existing_level)

    async def delete_level(self, level_id: int) -> None:
        result = await self.__session.execute(select(Level).where(Level.id == level_id))
        level = result.scalar_one_or_none()
        if level is None:
            raise HTTPException(
                status_code=404,
                detail=f"Level with id {level_id} not found",
            )
        await self.__session.delete(level)
        await self.__session.commit()
