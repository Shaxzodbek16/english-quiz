from fastapi import Depends, HTTPException, status

from app.api.models import AdminUsers, User
from app.api.repositories.channel import ChannelRepository
from app.api.schemas.channel import (
    ChannelResponseSchema,
    ChannelCreateSchema,
    ChannelUpdateSchema,
)


class ChannelController:
    def __init__(self, channel_repository: ChannelRepository = Depends()) -> None:
        self.__channel_repository = channel_repository

    @staticmethod
    async def _is_admin(user: User | AdminUsers) -> None:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )

    async def get_all_channels(
        self, *, user: AdminUsers | User
    ) -> list[ChannelResponseSchema]:
        await self._is_admin(user)
        res = await self.__channel_repository.get_all_channels()
        return [ChannelResponseSchema.model_validate(r) for r in res]

    async def get_channel_by_id(
        self, *, channel_id: int, user: User | AdminUsers
    ) -> ChannelResponseSchema:
        await self._is_admin(user)
        res = await self.__channel_repository.get_channel_by_id(channel_id=channel_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
            )
        return ChannelResponseSchema.model_validate(res)

    async def create_channel(
        self, *, channel: ChannelCreateSchema, user: User | AdminUsers
    ) -> ChannelResponseSchema:
        await self._is_admin(user)
        is_exist = await self.__channel_repository.get_channel_by_channel_id(
            channel_id=channel.channel_id
        )
        if is_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Channel with this channel_id already exists",
            )
        res = self.__channel_repository.create_channel(channel=channel)
        return ChannelResponseSchema.model_validate(res)

    async def update_channel(
        self, *, channel_id: int, channel: ChannelUpdateSchema, user: AdminUsers | User
    ) -> ChannelResponseSchema:
        await self._is_admin(user)
        if (
            await self.__channel_repository.get_channel_by_id(channel_id=channel_id)
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
            )
        res = await self.__channel_repository.update_channel(
            channel_id=channel_id, channel=channel
        )
        return ChannelResponseSchema.model_validate(res)

    async def delete_channel(self, *, channel_id: int, user: AdminUsers | User) -> None:
        await self._is_admin(user)
        if (
            await self.__channel_repository.get_channel_by_id(channel_id=channel_id)
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
            )
        await self.__channel_repository.delete_channel(channel_id=channel_id)
