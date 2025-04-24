from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from sqlalchemy.future import select

from app.api.models import AdminUsers
from app.api.schemas.admins import AdminCreateSchema, AdminUpdateSchema
from app.core.databases.postgres import get_general_session


class AdminRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_general_session),
    ):
        self.__session = session

    async def get_admin_by_telegram_id(self, telegram_id: int) -> AdminUsers | None:
        query = select(AdminUsers).where(AdminUsers.telegram_id == telegram_id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def get_admin_by_email(self, email: str) -> AdminUsers | None:
        query = select(AdminUsers).where(AdminUsers.email == email)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_admins(self) -> Sequence[AdminUsers]:
        query = select(AdminUsers)
        result = await self.__session.execute(query)
        return result.scalars().all()

    async def get_admin_by_id(self, admin_id: int) -> AdminUsers | None:
        query = select(AdminUsers).where(AdminUsers.id == admin_id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def create_admin(self, admin: AdminCreateSchema) -> AdminUsers:
        new_admin = AdminUsers(**admin.model_dump())
        self.__session.add(new_admin)
        await self.__session.commit()
        return new_admin

    async def update_admin(self, admin_id: int, admin: AdminUpdateSchema) -> AdminUsers:
        current_admin = await self.get_admin_by_id(admin_id)
        if not current_admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        current_admin.update(admin.model_dump())
        await self.__session.commit()
        return current_admin

    async def delete_admin(self, admin_id: int) -> None:
        current_admin = await self.get_admin_by_id(admin_id)
        if not current_admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        await self.__session.delete(current_admin)
        await self.__session.commit()
