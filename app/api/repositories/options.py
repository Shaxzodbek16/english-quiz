from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Sequence
from sqlalchemy.future import select

from app.api.schemas.options import (
    OptionsResponseSchema,
    OptionsCreateSchema,
    OptionsUpdateSchema,
)
from app.core.databases.postgres import get_general_session
from app.api.models.options import Option


class OptionsRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session: AsyncSession = session

    async def get_all_options(self) -> Sequence[OptionsResponseSchema]:
        q = await self.__session.execute(select(Option))
        options = q.scalars().all()
        return [OptionsResponseSchema.model_validate(option) for option in options]

    async def get_option_by_id(self, option_id: int) -> OptionsResponseSchema | None:
        q = await self.__session.execute(select(Option).where(Option.id == option_id))
        option = q.scalars().first()
        if option is None:
            return None
        return OptionsResponseSchema.model_validate(option)

    async def create_option(self, data: OptionsCreateSchema) -> OptionsResponseSchema:
        option = Option(**data.model_dump())
        self.__session.add(option)
        await self.__session.commit()
        await self.__session.refresh(option)
        return OptionsResponseSchema.model_validate(option)

    async def update_option(
        self, option_id: int, data: OptionsUpdateSchema
    ) -> OptionsResponseSchema:
        q = await self.__session.execute(select(Option).where(Option.id == option_id))
        option = q.scalars().first()
        option.update(data.model_dump())  # type: ignore
        self.__session.add(option)
        await self.__session.commit()
        await self.__session.refresh(option)
        return OptionsResponseSchema.model_validate(option)

    async def delete_option(self, option_id: int) -> None:
        q = await self.__session.execute(select(Option).where(Option.id == option_id))
        option = q.scalars().first()
        if option is None:
            return None
        await self.__session.delete(option)
        await self.__session.commit()
        return None
