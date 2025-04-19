from typing import Sequence
from fastapi import Depends, APIRouter, status

from app.api.constants.options.docs import OPTIONS_DOCS
from app.api.models import AdminUsers, User
from app.api.schemas.options import (
    OptionsResponseSchema,
    OptionsCreateSchema,
    OptionsUpdateSchema,
)
from app.api.controllers.options import OptionsController
from app.api.utils.admins import get_current_user

router = APIRouter(
    prefix="/options",
    tags=["Options"],
    redirect_slashes=False,
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[OptionsResponseSchema],
    summary=OPTIONS_DOCS["get"]["summary"],
    description=OPTIONS_DOCS["get"]["description"],
)
async def get_all_options(
    current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    options_controller: OptionsController = Depends(OptionsController),
) -> Sequence[OptionsResponseSchema]:
    return await options_controller.get_all_options()


@router.get(
    "/{option_id}/",
    status_code=status.HTTP_200_OK,
    response_model=OptionsResponseSchema,
    summary=OPTIONS_DOCS["get_one"]["summary"],
    description=OPTIONS_DOCS["get_one"]["description"],
)
async def get_option_by_id(
    option_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    options_controller: OptionsController = Depends(OptionsController),
) -> OptionsResponseSchema:
    return await options_controller.get_option_by_id(option_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=OptionsResponseSchema,
    summary=OPTIONS_DOCS["create"]["summary"],
    description=OPTIONS_DOCS["create"]["description"],
)
async def create_option(
    option: OptionsCreateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),
    options_controller: OptionsController = Depends(OptionsController),
) -> OptionsResponseSchema:
    return await options_controller.create_option(option=option, user=current_user)


@router.put(
    "/{option_id}/",
    status_code=status.HTTP_200_OK,
    response_model=OptionsResponseSchema,
    summary=OPTIONS_DOCS["update"]["summary"],
    description=OPTIONS_DOCS["update"]["description"],
)
async def update_option(
    option_id: int,
    option: OptionsUpdateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),
    options_controller: OptionsController = Depends(OptionsController),
) -> OptionsResponseSchema:
    return await options_controller.update_option(
        option_id=option_id, option=option, user=current_user
    )


@router.delete(
    "/{option_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=OPTIONS_DOCS["delete"]["summary"],
    description=OPTIONS_DOCS["delete"]["description"],
)
async def delete_option(
    option_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),
    options_controller: OptionsController = Depends(OptionsController),
) -> None:
    return await options_controller.delete_option(
        option_id=option_id, user=current_user
    )
