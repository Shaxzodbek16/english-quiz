from fastapi import Depends, APIRouter, HTTPException, status
from app.core.settings import get_settings, Settings
from app.api.schemas.admins import (
    AdminResponseSchema,
    AdminCreateSchema,
    AdminUpdateSchema,
)
from app.api.controllers.admins import AdminsController
from app.api.models import AdminUsers, User
from app.api.utils.admins import get_current_user

settings: Settings = get_settings()

router = APIRouter(
    prefix="/admins",
    tags=["Admins Management"],
    redirect_slashes=False,
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[AdminResponseSchema],
    summary="Get all admins",
    description="Returns a list of all admins.",
)
async def get_all_admins(
    current_user: AdminUsers | User = Depends(get_current_user),
    admin_controller: AdminsController = Depends(),
) -> list[AdminResponseSchema]:
    return await admin_controller.get_all_admins(user=current_user)


@router.get(
    "/{admin_id}/",
    status_code=status.HTTP_200_OK,
    response_model=AdminResponseSchema,
    summary="Get admin by ID",
    description="Returns an admin by ID.",
)
async def get_admin_by_id(
    admin_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),
    admin_controller: AdminsController = Depends(),
):
    return await admin_controller.get_admin_by_id(admin_id=admin_id, user=current_user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AdminResponseSchema,
    summary="Create a new admin",
    description="Creates a new admin.",
)
async def create_admin(
    admin: AdminCreateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),
    admin_controller: AdminsController = Depends(),
):
    return await admin_controller.create_admin(admin=admin, user=current_user)


@router.put(
    "/{admin_id}/",
    status_code=status.HTTP_200_OK,
    response_model=AdminResponseSchema,
    summary="Update an admin",
    description="Updates an admin by ID.",
)
async def update_admin(
    admin_id: int,
    admin: AdminUpdateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),
    admin_controller: AdminsController = Depends(),
):
    return await admin_controller.update_admin(
        admin_id=admin_id, admin=admin, user=current_user
    )


@router.delete(
    "/{admin_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an admin",
    description="Deletes an admin by ID.",
)
async def delete_admin(
    admin_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),
    admin_controller: AdminsController = Depends(),
):
    await admin_controller.delete_admin(admin_id=admin_id, user=current_user)
