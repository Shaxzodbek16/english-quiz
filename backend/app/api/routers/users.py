from fastapi import Depends, APIRouter, status

from app.api.controllers.users import UserController
from app.api.models import AdminUsers, User
from app.api.schemas.users import UserUpdateSchema, UserResponseSchema
from app.api.utils.admins import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    redirect_slashes=False,
)


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
    summary="Get current user",
    description="Get current user",
)
async def get_me(
    current_user: User | AdminUsers = Depends(get_current_user),
    user_controller: UserController = Depends(),
) -> UserResponseSchema:
    return await user_controller.get_me(current_user=current_user)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
    summary="Update user",
    description="Update user",
)
async def update_user(
    user_data: UserUpdateSchema,
    current_user: User | AdminUsers = Depends(get_current_user),
    user_controller: UserController = Depends(),
) -> UserResponseSchema:
    return await user_controller.update_user(current_user=current_user, data=user_data)
