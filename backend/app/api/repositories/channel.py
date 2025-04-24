from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from typing import Sequence

from app.api.models import Channel
from app.api.schemas.channel import ChannelCreateSchema, ChannelUpdateSchema
from app.core.databases.postgres import get_general_session


class ChannelRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_all_channels(self) -> Sequence[Channel]:
        channels = await self.__session.execute(select(Channel))
        return channels.scalars().all()

    async def get_channel_by_id(self, *, channel_id: int) -> Channel | None:
        channel = await self.__session.execute(
            select(Channel).where(Channel.id == channel_id)
        )
        return channel.scalar_one_or_none()

    async def get_channel_by_channel_id(self, *, channel_id: int) -> Channel | None:
        channel = await self.__session.execute(
            select(Channel).where(Channel.channel_id == channel_id)
        )
        return channel.scalar_one_or_none()

    async def create_channel(self, *, channel: ChannelCreateSchema) -> Channel:
        new_channel = Channel(**channel.model_dump())
        self.__session.add(new_channel)
        await self.__session.commit()
        await self.__session.refresh(new_channel)
        return new_channel

    async def update_channel(
        self, *, channel_id: int, channel: ChannelUpdateSchema
    ) -> Channel:
        update_channel = await self.get_channel_by_id(channel_id=channel_id)
        if update_channel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
            )
        update_channel.update(**channel.model_dump())
        await self.__session.commit()
        await self.__session.refresh(update_channel)
        return update_channel

    async def delete_channel(self, *, channel_id: int) -> None:
        channel = await self.get_channel_by_id(channel_id=channel_id)
        if channel is None:
            return
        await self.__session.delete(channel)
        await self.__session.commit()
