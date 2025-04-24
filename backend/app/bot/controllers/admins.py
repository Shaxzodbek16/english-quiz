from sqlalchemy.future import select

from app.api.models import AdminUsers
from app.core.databases.postgres import get_session_without_depends


async def get_admin_by_telegram_id(telegram_id: int) -> AdminUsers | None:
    async with get_session_without_depends() as session:
        user = await session.execute(
            select(AdminUsers).where(AdminUsers.telegram_id == telegram_id)
        )
        return user.scalar_one_or_none()


async def get_admin_users() -> list[AdminUsers]:
    async with get_session_without_depends() as session:
        users = await session.execute(select(AdminUsers))
        return users.scalars().all()
