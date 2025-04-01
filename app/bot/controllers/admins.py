from sqlalchemy.future import select

from app.api.models import AdminUsers
from app.core.databases.postgres import get_session_without_depends


async def get_user_by_telegram_id(telegram_id: int) -> AdminUsers | None:
    async with get_session_without_depends() as session:
        user = await session.execute(
            select(AdminUsers).where(AdminUsers.telegram_id == telegram_id)
        )
        return user.scalar_one_or_none()
