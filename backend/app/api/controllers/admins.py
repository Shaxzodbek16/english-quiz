from fastapi import Depends, HTTPException

from app.api.models import AdminUsers, User
from app.api.repositories.admins import AdminRepository
from app.api.schemas.admins import (
    AdminResponseSchema,
    AdminCreateSchema,
    AdminUpdateSchema,
)


class AdminsController:
    def __init__(self, admin_repository: AdminRepository = Depends()):
        self.__admin_repository: AdminRepository = admin_repository

    async def get_all_admins(
        self, user: AdminUsers | User
    ) -> list[AdminResponseSchema]:
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=403, detail="Forbidden")
        admins = await self.__admin_repository.get_all_admins()
        return [AdminResponseSchema.model_validate(admin) for admin in admins]

    async def get_admin_by_id(
        self, *, admin_id: int, user: AdminUsers | User
    ) -> AdminResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=403, detail="Forbidden")
        admin = await self.__admin_repository.get_admin_by_id(admin_id=admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return AdminResponseSchema.model_validate(admin)

    async def create_admin(self, *, admin: AdminCreateSchema, user: AdminUsers | User):
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=403, detail="Forbidden")
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="Forbidden")
        is_exist = await self.__admin_repository.get_admin_by_telegram_id(
            admin.telegram_id
        )
        if is_exist:
            raise HTTPException(status_code=400, detail="Admin already exists")
        new_admin = await self.__admin_repository.create_admin(admin)
        return AdminResponseSchema.model_validate(new_admin)

    async def update_admin(
        self, *, admin_id: int, admin: AdminUpdateSchema, user: AdminUsers | User
    ) -> AdminResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=403, detail="Forbidden")
        existing_admin = await self.__admin_repository.get_admin_by_id(
            admin_id=admin_id
        )
        if not existing_admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        if not user.telegram_id != existing_admin.telegram_id:
            if not user.is_superuser:
                raise HTTPException(status_code=403, detail="Forbidden")

        updated_admin = await self.__admin_repository.update_admin(
            admin_id=admin_id, admin=admin
        )
        return AdminResponseSchema.model_validate(updated_admin)

    async def delete_admin(self, admin_id: int, user: AdminUsers | User) -> None:
        if not isinstance(user, AdminUsers):
            raise HTTPException(status_code=403, detail="Forbidden")
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="Forbidden")

        existing_admin = await self.__admin_repository.get_admin_by_id(
            admin_id=admin_id
        )
        if not existing_admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        await self.__admin_repository.delete_admin(admin_id=admin_id)
