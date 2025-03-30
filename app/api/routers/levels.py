from fastapi import Depends, APIRouter, status, Path
from typing import Sequence

from app.api.models import AdminUsers
from app.api.utils.admins import get_current_user
from app.api.controllers.levels import LevelController
from app.api.schemas.levels import (
    ResponseLevelSchema,
    CreateLevelSchema,
    UpdateLevelSchema,
)
from app.api.constants.levels.docs import LEVEL_DOCS


router = APIRouter(
    prefix="/levels",
    tags=["Levels"],
    redirect_slashes=False,
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[ResponseLevelSchema],
    summary=LEVEL_DOCS["get"]["summary"],
    description=LEVEL_DOCS["get"]["description"],
)
async def get_all_levels(
    level_controller: LevelController = Depends(),
) -> Sequence[ResponseLevelSchema]:
    return await level_controller.get_all_levels()


@router.get(
    "/{level_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseLevelSchema,
    summary=LEVEL_DOCS["get_one"]["summary"],
    description=LEVEL_DOCS["get_one"]["description"],
)
async def get_level(
    level_id: int = Path(..., ge=1),
    level_controller: LevelController = Depends(),
) -> ResponseLevelSchema:
    return await level_controller.get_level(level_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseLevelSchema,
    summary=LEVEL_DOCS["create"]["summary"],
    description=LEVEL_DOCS["create"]["description"],
)
async def create_level(
    level: CreateLevelSchema,
    level_controller: LevelController = Depends(),
    current_user: AdminUsers = Depends(get_current_user),
) -> ResponseLevelSchema:

    return await level_controller.create_level(level)


@router.put(
    "/{level_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseLevelSchema,
    summary=LEVEL_DOCS["update"]["summary"],
    description=LEVEL_DOCS["update"]["description"],
)
async def update_level(
    level: UpdateLevelSchema,
    level_id: int = Path(..., ge=1),
    level_controller: LevelController = Depends(),
) -> ResponseLevelSchema:
    return await level_controller.update_level(level, level_id)


@router.delete(
    "/{level_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=LEVEL_DOCS["delete"]["summary"],
    description=LEVEL_DOCS["delete"]["description"],
)
async def delete_level(
    level_id: int = Path(..., ge=1), level_controller: LevelController = Depends()
) -> None:
    return await level_controller.delete_level(level_id)
