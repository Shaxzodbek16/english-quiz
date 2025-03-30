from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.future import select

from app.api.models import AdminUsers
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
