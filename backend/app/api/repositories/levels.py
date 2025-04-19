from fastapi import HTTPException
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

from app.api.schemas.levels import (
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
    ) -> Sequence[Level]:
        result = await self.__session.execute(select(Level))
        return result.scalars().all()

    async def get_level_by_id(self, level_id: int) -> Level | None:
        result = await self.__session.execute(select(Level).where(Level.id == level_id))
        return result.scalar_one_or_none()

    async def get_level_by_name(self, name: str) -> int:
        result = await self.__session.execute(select(Level).where(Level.name == name))
        levels = result.scalars().all()
        return len(levels)

    async def create_level(self, level: CreateLevelSchema) -> Level:
        new_level = Level(**level.model_dump())
        self.__session.add(new_level)
        await self.__session.commit()
        await self.__session.refresh(new_level)
        return new_level

    async def update_level(
        self, level: UpdateLevelSchema, level_id: int
    ) -> Level | None:
        result = await self.__session.execute(select(Level).where(Level.id == level_id))
        existing_level = result.scalars().first()
        new_level = existing_level.update(level.model_dump())  # type: ignore
        await self.__session.commit()
        await self.__session.refresh(new_level)
        return existing_level

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
