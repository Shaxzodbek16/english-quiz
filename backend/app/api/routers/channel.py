from fastapi import APIRouter, status, Depends

from app.api.controllers.channel import ChannelController
from app.api.models import AdminUsers, User
from app.api.schemas.channel import (
    ChannelResponseSchema,
    ChannelCreateSchema,
    ChannelUpdateSchema,
)
from app.api.utils.admins import get_current_user

router = APIRouter(
    prefix="/channel",
    tags=["Channel Management"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ChannelResponseSchema],
    description="Get all channels",
    summary="Get all channels",
)
async def get_all_channels(
    current_user: User | AdminUsers = Depends(get_current_user),
    channel_controller: ChannelController = Depends(),
) -> list[ChannelResponseSchema]:
    return await channel_controller.get_all_channels(user=current_user)


@router.get(
    "/{channel_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChannelResponseSchema,
    description="Get channel by ID",
    summary="Get channel by ID",
)
async def get_channel_by_id(
    channel_id: int,
    current_user: User | AdminUsers = Depends(get_current_user),
    channel_controller: ChannelController = Depends(),
) -> ChannelResponseSchema:
    return await channel_controller.get_channel_by_id(
        channel_id=channel_id, user=current_user
    )


@router.post(
    "/{channel_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChannelResponseSchema,
    description="Create channel",
    summary="Create channel",
)
async def create_channel(
    channel: ChannelCreateSchema,
    current_user: User | AdminUsers = Depends(get_current_user),
    channel_controller: ChannelController = Depends(),
) -> ChannelResponseSchema:
    return await channel_controller.create_channel(channel=channel, user=current_user)


@router.put(
    "/{channel_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChannelResponseSchema,
    description="Update channel",
    summary="Update channel",
)
async def update_channel(
    channel_id: int,
    channel: ChannelUpdateSchema,
    current_user: User | AdminUsers = Depends(get_current_user),
    channel_controller: ChannelController = Depends(),
) -> ChannelResponseSchema:
    return await channel_controller.update_channel(
        channel=channel, channel_id=channel_id, user=current_user
    )


@router.delete(
    "/{channel_id}/",
    status_code=status.HTTP_200_OK,
    description="Delete channel",
    summary="Delete channel",
)
async def delete_channel(
    channel_id: int,
    current_user: User | AdminUsers = Depends(get_current_user),
    channel_controller: ChannelController = Depends(),
) -> None:
    return await channel_controller.delete_channel(
        channel_id=channel_id, user=current_user
    )
